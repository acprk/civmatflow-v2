#!/usr/bin/env python3
"""Hold-out freezing, guarding, sealing and one-shot evaluation for civmatflow v2.

Subcommands
  freeze    Group-wise split of a tidy CSV (groups = source / laboratory / reference).
            Writes holdout_ids.csv, calibration_ids.csv and split.json (with sha256 of
            the data and of both id files) and makes them read-only.
  check     Assert zero overlap between the ids in a CSV and the frozen hold-out.
  seal      sha256-seal PREREG.md (-> PREREG.sha256) and write FROZEN_MANIFEST.json with
            the sha256 of every file in the given code directories and of the split.
  evaluate  Verify the PREREG sha256 (and FROZEN_MANIFEST.json when given), refuse if the
            hold-out was already consumed, run the evaluation command exactly once, then
            write HOLDOUT_CONSUMED whatever the outcome and append to evaluations.log.
  status    Print the split metadata and whether the hold-out has been consumed.

Library use (put this at the top of every baseline / candidate-model script):

    import sys; sys.path.insert(0, "<repo>/tools")
    from holdout_guard import load_calibration
    rows = load_calibration("data/processed/tidy.csv", "HOLDOUT")   # never the hold-out

Only the script launched by `evaluate` may call load_holdout(); it refuses unless the
environment variable CIVMAT2_HOLDOUT_EVAL=1 is set (which `evaluate` sets for its child).
Standard library only.
"""
import argparse
import csv
import hashlib
import json
import os
import pathlib
import random
import shlex
import stat
import subprocess
import sys
import time

READ_ONLY = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def make_read_only(p):
    try:
        os.chmod(p, READ_ONLY)
    except OSError:
        pass


# ----------------------------------------------------------------------------- freeze
def freeze(a):
    rows = read_csv(a.data)
    if not rows:
        sys.exit("freeze: data file has no rows")
    for col in (a.id, a.group):
        if col not in rows[0]:
            sys.exit(f"freeze: column '{col}' not found; columns are {list(rows[0])}")
    ids = [r[a.id] for r in rows]
    dupes = sorted({i for i in ids if ids.count(i) > 1}) if len(set(ids)) != len(ids) else []
    if dupes:
        sys.exit(f"freeze: id column '{a.id}' is not unique, e.g. {dupes[:5]}")
    groups = sorted({r[a.group] for r in rows})
    if len(groups) < a.min_groups:
        sys.exit(f"freeze: only {len(groups)} group(s) in '{a.group}'; need at least {a.min_groups} "
                 "for a group-wise split (use a coarser grouping or the simulation route)")
    rng = random.Random(a.seed)
    rng.shuffle(groups)
    n_hold = max(1, min(len(groups) - 1, round(len(groups) * a.frac)))
    hold = set(groups[:n_hold])
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("holdout_ids.csv", "calibration_ids.csv", "split.json"):
        if (out / name).exists():
            sys.exit(f"freeze: {out / name} already exists; a frozen split is never overwritten")
    for name, sel in (("holdout_ids.csv", True), ("calibration_ids.csv", False)):
        with open(out / name, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([a.id, a.group])
            for r in rows:
                if (r[a.group] in hold) == sel:
                    w.writerow([r[a.id], r[a.group]])
    n_hold_rows = sum(1 for r in rows if r[a.group] in hold)
    meta = {"data": str(a.data), "data_sha256": sha(a.data), "group_col": a.group, "id_col": a.id,
            "seed": a.seed, "frac": a.frac, "n_rows": len(rows), "n_groups": len(groups),
            "holdout_groups": sorted(hold), "n_holdout_groups": len(hold), "n_holdout_rows": n_hold_rows,
            "n_calibration_rows": len(rows) - n_hold_rows,
            "holdout_ids_sha256": sha(out / "holdout_ids.csv"),
            "calibration_ids_sha256": sha(out / "calibration_ids.csv"),
            "frozen_utc": utc(), "note": a.note}
    (out / "split.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    for name in ("holdout_ids.csv", "calibration_ids.csv", "split.json"):
        make_read_only(out / name)
    print(json.dumps({"holdout_groups": len(hold), "groups": len(groups),
                      "holdout_rows": n_hold_rows, "calibration_rows": len(rows) - n_hold_rows,
                      "split_dir": str(out)}))


# ----------------------------------------------------------------------------- library
def _meta(split_dir):
    p = pathlib.Path(split_dir) / "split.json"
    if not p.exists():
        raise FileNotFoundError(f"no split.json in {split_dir}; run `holdout_guard.py freeze` first")
    return json.loads(p.read_text())


def holdout_ids(split_dir):
    """Return (set of hold-out ids, id column). Verifies the id file against its frozen sha256."""
    meta = _meta(split_dir)
    p = pathlib.Path(split_dir) / "holdout_ids.csv"
    if sha(p) != meta["holdout_ids_sha256"]:
        raise RuntimeError("hold-out id file changed since freezing; refuse to continue")
    return {r[meta["id_col"]] for r in read_csv(p)}, meta["id_col"]


def load_calibration(data_csv, split_dir):
    """Return calibration rows only; asserts zero overlap with the frozen hold-out."""
    hold, idc = holdout_ids(split_dir)
    rows = [r for r in read_csv(data_csv) if r[idc] not in hold]
    assert not ({r[idc] for r in rows} & hold), "calibration rows overlap the hold-out"
    return rows


def load_holdout(data_csv, split_dir):
    """Return hold-out rows. Allowed only inside the command run by `evaluate`."""
    if os.environ.get("CIVMAT2_HOLDOUT_EVAL") != "1":
        raise PermissionError("load_holdout() is only allowed inside `holdout_guard.py evaluate` "
                              "(CIVMAT2_HOLDOUT_EVAL=1); use load_calibration() everywhere else")
    hold, idc = holdout_ids(split_dir)
    return [r for r in read_csv(data_csv) if r[idc] in hold]


# ----------------------------------------------------------------------------- check
def check(a):
    hold, idc = holdout_ids(a.split)
    rows = read_csv(a.data)
    if rows and idc not in rows[0]:
        sys.exit(f"check: id column '{idc}' not in {a.data}")
    ids = {r[idc] for r in rows}
    bad = ids & hold
    if bad:
        sys.exit(f"OVERLAP with frozen hold-out: {len(bad)} ids, e.g. {sorted(bad)[:5]}")
    print(f"zero overlap OK ({len(ids)} ids checked against {len(hold)} hold-out ids)")


# ----------------------------------------------------------------------------- seal
def file_manifest(dirs, skip=("__pycache__", ".git", "pdfs", "text")):
    files = {}
    for d in dirs:
        d = pathlib.Path(d)
        if d.is_file():
            files[str(d)] = sha(d)
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file() and not any(s in p.parts for s in skip):
                files[str(p)] = sha(p)
    return files


def seal(a):
    prereg = pathlib.Path(a.prereg)
    out = pathlib.Path(a.out) if a.out else prereg.parent
    out.mkdir(parents=True, exist_ok=True)
    digest = sha(prereg)
    sha_file = out / (prereg.name + ".sha256") if prereg.suffix != ".md" else out / (prereg.stem + ".sha256")
    sha_file.write_text(f"{digest}  {prereg.name}\n")
    manifest = {"sealed_utc": utc(), "prereg": {"path": str(prereg), "sha256": digest},
                "split": None, "files": file_manifest(a.code or [])}
    if a.split:
        meta = _meta(a.split)
        manifest["split"] = {"dir": str(a.split), "holdout_ids_sha256": meta["holdout_ids_sha256"],
                             "data_sha256": meta["data_sha256"], "frozen_utc": meta["frozen_utc"]}
    mf = out / "FROZEN_MANIFEST.json"
    mf.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    make_read_only(prereg)
    print(json.dumps({"prereg_sha256": digest, "sha_file": str(sha_file), "manifest": str(mf),
                      "n_files": len(manifest["files"])}))


def verify_manifest(path):
    m = json.loads(pathlib.Path(path).read_text())
    changed = [p for p, h in m.get("files", {}).items() if not pathlib.Path(p).exists() or sha(p) != h]
    return m, changed


# ----------------------------------------------------------------------------- evaluate
def evaluate(a):
    split = pathlib.Path(a.split)
    consumed = split / "HOLDOUT_CONSUMED"
    if consumed.exists():
        sys.exit("hold-out already consumed (HOLDOUT_CONSUMED exists); refuse to evaluate again. "
                 "A new idea needs a new, never-evaluated hold-out.")
    want = pathlib.Path(a.sha).read_text().split()[0]
    got = sha(a.prereg)
    if got != want:
        sys.exit(f"PREREG sha256 mismatch (sealed {want[:12]}…, now {got[:12]}…); refuse")
    if a.manifest:
        m, changed = verify_manifest(a.manifest)
        if m.get("prereg", {}).get("sha256") not in (None, want):
            sys.exit("FROZEN_MANIFEST.json refers to a different PREREG; refuse")
        if changed:
            sys.exit("code changed since sealing; refuse:\n  " + "\n  ".join(changed[:20]))
    # fail-closed: mark as consumed BEFORE running so an interrupted run cannot be repeated silently
    record = {"started": utc(), "finished": None, "prereg_sha256": want, "cmd": a.cmd,
              "manifest": a.manifest, "returncode": None, "status": "running"}
    consumed.write_text(json.dumps(record, indent=2))
    env = dict(os.environ, CIVMAT2_HOLDOUT_EVAL="1")
    try:
        rc = subprocess.call(shlex.split(a.cmd), env=env)
    except Exception as e:  # command could not even start
        rc = -1
        record["error"] = str(e)
    record.update(finished=utc(), returncode=rc, status="finished")
    consumed.write_text(json.dumps(record, indent=2))
    make_read_only(consumed)
    with open(split / "evaluations.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print(f"evaluation finished, rc = {rc}; hold-out marked consumed ({consumed})")
    if rc != 0:
        sys.exit(rc if rc > 0 else 1)


# ----------------------------------------------------------------------------- status
def status(a):
    meta = _meta(a.split)
    consumed = pathlib.Path(a.split) / "HOLDOUT_CONSUMED"
    meta["consumed"] = json.loads(consumed.read_text()) if consumed.exists() else None
    try:
        holdout_ids(a.split)
        meta["integrity"] = "OK"
    except Exception as e:
        meta["integrity"] = f"FAILED: {e}"
    print(json.dumps(meta, indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd_name", required=True)
    f = sub.add_parser("freeze", help="freeze a group-wise hold-out split")
    f.add_argument("--data", required=True, help="tidy CSV with one row per record")
    f.add_argument("--group", required=True, help="column that identifies the source / lab / reference")
    f.add_argument("--id", default="record_id", help="unique record id column (default record_id)")
    f.add_argument("--frac", type=float, default=0.3, help="fraction of groups held out (default 0.3)")
    f.add_argument("--seed", type=int, required=True)
    f.add_argument("--min-groups", type=int, default=2)
    f.add_argument("--note", default="", help="free text stored in split.json (e.g. why this grouping)")
    f.add_argument("--out", required=True, help="split directory, e.g. <ws>/HOLDOUT")
    c = sub.add_parser("check", help="assert zero overlap between a CSV and the frozen hold-out")
    c.add_argument("--data", required=True)
    c.add_argument("--split", required=True)
    s = sub.add_parser("seal", help="seal PREREG.md and write FROZEN_MANIFEST.json")
    s.add_argument("--prereg", required=True)
    s.add_argument("--split", default=None, help="split directory to record in the manifest")
    s.add_argument("--code", nargs="*", default=[], help="code directories / files to fingerprint")
    s.add_argument("--out", default=None, help="where to write PREREG.sha256 and FROZEN_MANIFEST.json")
    e = sub.add_parser("evaluate", help="one-shot hold-out evaluation")
    e.add_argument("--split", required=True)
    e.add_argument("--prereg", required=True)
    e.add_argument("--sha", required=True, help="PREREG.sha256 written by seal")
    e.add_argument("--manifest", default=None, help="FROZEN_MANIFEST.json written by seal (recommended)")
    e.add_argument("--cmd", required=True, help="evaluation command, quoted as one string")
    st = sub.add_parser("status", help="show split metadata and consumption state")
    st.add_argument("--split", required=True)
    a = ap.parse_args()
    {"freeze": freeze, "check": check, "seal": seal, "evaluate": evaluate, "status": status}[a.cmd_name](a)


if __name__ == "__main__":
    main()
