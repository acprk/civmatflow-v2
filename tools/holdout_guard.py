#!/usr/bin/env python3
"""Hold-out freezing, guarding and one-shot evaluation for civmatflow v2.

freeze:   group-wise split of a tidy CSV; writes holdout_ids.csv, calibration_ids.csv,
          split.json with sha256; files are made read-only.
check:    assert zero overlap between a CSV's ids and the frozen hold-out.
evaluate: verify PREREG sha256, refuse if HOLDOUT_CONSUMED exists, run the command,
          then write HOLDOUT_CONSUMED (whatever the outcome).
Library use:  from holdout_guard import load_calibration
"""
import argparse
import csv
import hashlib
import json
import os
import pathlib
import random
import stat
import subprocess
import sys
import time


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def read_csv(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def freeze(a):
    rows = read_csv(a.data)
    groups = sorted({r[a.group] for r in rows})
    rng = random.Random(a.seed)
    rng.shuffle(groups)
    n_hold = max(1, round(len(groups) * a.frac))
    hold = set(groups[:n_hold])
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    idc = a.id
    for name, sel in (("holdout_ids.csv", True), ("calibration_ids.csv", False)):
        with open(out / name, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([idc, a.group])
            for r in rows:
                if (r[a.group] in hold) == sel:
                    w.writerow([r[idc], r[a.group]])
    meta = {"data": str(a.data), "data_sha256": sha(a.data), "group_col": a.group, "id_col": idc,
            "seed": a.seed, "frac": a.frac, "holdout_groups": sorted(hold),
            "holdout_ids_sha256": sha(out / "holdout_ids.csv"),
            "calibration_ids_sha256": sha(out / "calibration_ids.csv"),
            "frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (out / "split.json").write_text(json.dumps(meta, indent=2))
    for name in ("holdout_ids.csv", "calibration_ids.csv", "split.json"):
        os.chmod(out / name, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    print(json.dumps({"holdout_groups": len(hold), "groups": len(groups)}))


def holdout_ids(split_dir):
    meta = json.loads((pathlib.Path(split_dir) / "split.json").read_text())
    p = pathlib.Path(split_dir) / "holdout_ids.csv"
    assert sha(p) == meta["holdout_ids_sha256"], "hold-out id file changed since freezing"
    return {r[meta["id_col"]] for r in read_csv(p)}, meta["id_col"]


def load_calibration(data_csv, split_dir):
    """Return calibration rows only; asserts zero overlap with the frozen hold-out."""
    hold, idc = holdout_ids(split_dir)
    rows = [r for r in read_csv(data_csv) if r[idc] not in hold]
    assert not ({r[idc] for r in rows} & hold)
    return rows


def check(a):
    hold, idc = holdout_ids(a.split)
    ids = {r[idc] for r in read_csv(a.data)}
    bad = ids & hold
    if bad:
        sys.exit(f"OVERLAP with frozen hold-out: {len(bad)} ids, e.g. {sorted(bad)[:5]}")
    print("zero overlap OK")


def evaluate(a):
    split = pathlib.Path(a.split)
    consumed = split / "HOLDOUT_CONSUMED"
    if consumed.exists():
        sys.exit("hold-out already consumed; refuse to evaluate again")
    want = pathlib.Path(a.sha).read_text().split()[0]
    if sha(a.prereg) != want:
        sys.exit("PREREG sha256 mismatch; refuse")
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rc = subprocess.call(a.cmd.split())
    consumed.write_text(json.dumps({"started": started, "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    "prereg_sha256": want, "cmd": a.cmd, "returncode": rc}, indent=2))
    print("evaluation finished, rc =", rc, "; hold-out marked consumed")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd_name", required=True)
    f = sub.add_parser("freeze")
    f.add_argument("--data", required=True)
    f.add_argument("--group", required=True)
    f.add_argument("--id", default="record_id")
    f.add_argument("--frac", type=float, default=0.3)
    f.add_argument("--seed", type=int, required=True)
    f.add_argument("--out", required=True)
    c = sub.add_parser("check")
    c.add_argument("--data", required=True)
    c.add_argument("--split", required=True)
    e = sub.add_parser("evaluate")
    e.add_argument("--split", required=True)
    e.add_argument("--prereg", required=True)
    e.add_argument("--sha", required=True)
    e.add_argument("--cmd", required=True)
    a = ap.parse_args()
    {"freeze": freeze, "check": check, "evaluate": evaluate}[a.cmd_name](a)


if __name__ == "__main__":
    main()
