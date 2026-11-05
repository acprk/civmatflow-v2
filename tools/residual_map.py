#!/usr/bin/env python3
"""Stratified residual map and between/within-source variance decomposition (V4 / G1).

Input: a tidy CSV with the observed value, one or more model predictions, a source
column (laboratory / reference / batch) and the physical variables to stratify by.

Outputs (in --out):
  stratified_errors.csv   per model x variable x bin: n, n_sources, bias, MAE, RMSE,
                          sign consistency across sources, Spearman trend of residual vs variable
  variance_decomposition.json  per model: pooled RMSE, source-equal-weight RMSE, between-source
                          and within-source variance, ICC(1) with a source-bootstrap CI,
                          and the share of residual variance that inter-source scatter explains
  residual_map.md         human-readable summary with the detectability verdict

Residual definition: r = pred - obs (or log10(pred/obs) with --log, recommended for
positive quantities such as shrinkage, diffusion coefficients, carbonation depth).

Usage:
  residual_map.py data.csv --obs y --pred B4,MC2010 --source source \
      --by age_d,w_b,size_mm,rh --out results/ [--log] [--bins 4] [--boot 1000] [--seed 1]
Standard library only.
"""
import argparse
import csv
import json
import math
import pathlib
import random
import statistics
import sys


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def spearman(x, y):
    if len(x) < 3:
        return None
    rx, ry = rank(x), rank(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def rmse(v):
    return math.sqrt(sum(a * a for a in v) / len(v)) if v else None


def icc1(groups):
    """One-way random-effects ICC(1) for unbalanced groups: dict source -> list of residuals."""
    gs = [g for g in groups.values() if len(g) >= 1]
    k = len(gs)
    n = sum(len(g) for g in gs)
    if k < 2 or n <= k:
        return None
    grand = sum(sum(g) for g in gs) / n
    ssb = sum(len(g) * (statistics.mean(g) - grand) ** 2 for g in gs)
    ssw = sum((x - statistics.mean(g)) ** 2 for g in gs for x in g)
    msb = ssb / (k - 1)
    msw = ssw / (n - k)
    n0 = (n - sum(len(g) ** 2 for g in gs) / n) / (k - 1)
    var_b = max(0.0, (msb - msw) / n0)
    icc = var_b / (var_b + msw) if (var_b + msw) > 0 else 0.0
    return {"icc": icc, "var_between": var_b, "var_within": msw, "k_sources": k, "n": n}


def quant(a, q):
    a = sorted(a)
    if not a:
        return None
    k = (len(a) - 1) * q
    f = int(k)
    c = min(f + 1, len(a) - 1)
    return a[f] + (a[c] - a[f]) * (k - f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data")
    ap.add_argument("--obs", required=True)
    ap.add_argument("--pred", required=True, help="comma-separated prediction columns (one per model)")
    ap.add_argument("--source", required=True)
    ap.add_argument("--by", default="", help="comma-separated physical variables to stratify by")
    ap.add_argument("--out", required=True)
    ap.add_argument("--log", action="store_true", help="residual = log10(pred/obs)")
    ap.add_argument("--bins", type=int, default=4, help="quantile bins per numeric variable (default 4)")
    ap.add_argument("--boot", type=int, default=1000, help="source bootstrap replicates for the ICC CI")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--min-n", type=int, default=5, help="minimum rows per stratum to report")
    a = ap.parse_args()
    preds = [p.strip() for p in a.pred.split(",") if p.strip()]
    byv = [v.strip() for v in a.by.split(",") if v.strip()]
    with open(a.data, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("residual_map: empty data")
    for col in [a.obs, a.source] + preds + byv:
        if col not in rows[0]:
            sys.exit(f"residual_map: column '{col}' missing; columns: {list(rows[0])}")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)

    # residuals per model
    res = {}  # model -> list of (residual, row)
    for m in preds:
        lst = []
        for r in rows:
            o, p = fnum(r[a.obs]), fnum(r[m])
            if o is None or p is None:
                continue
            if a.log:
                if o <= 0 or p <= 0:
                    continue
                lst.append((math.log10(p / o), r))
            else:
                lst.append((p - o, r))
        res[m] = lst

    # stratified table
    strat_rows = []
    for m in preds:
        lst = res[m]
        for v in byv:
            vals = [(fnum(r[v]), e, r) for e, r in lst]
            numeric = [t for t in vals if t[0] is not None]
            if len(numeric) >= max(2 * a.min_n, 0.5 * len(vals)) and len({t[0] for t in numeric}) > a.bins:
                edges = [quant([t[0] for t in numeric], i / a.bins) for i in range(1, a.bins)]

                def label(x):
                    for i, e in enumerate(edges):
                        if x <= e:
                            return i
                    return len(edges)
                bins = {}
                for x, e, r in numeric:
                    bins.setdefault(label(x), []).append((x, e, r))
                names = {}
                for i in sorted(bins):
                    xs = [t[0] for t in bins[i]]
                    names[i] = f"[{min(xs):.4g}, {max(xs):.4g}]"
                items = [(names[i], bins[i]) for i in sorted(bins)]
                trend = spearman([t[0] for t in numeric], [t[1] for t in numeric])
            else:  # categorical
                cats = {}
                for e, r in lst:
                    cats.setdefault(r[v] or "(missing)", []).append((None, e, r))
                items = sorted(cats.items())
                trend = None
            for name, grp in items:
                if len(grp) < a.min_n:
                    continue
                errs = [t[1] for t in grp]
                per_src = {}
                for _, e, r in grp:
                    per_src.setdefault(r[a.source], []).append(e)
                src_means = [statistics.mean(x) for x in per_src.values()]
                bias = statistics.mean(errs)
                same_sign = (sum(1 for s in src_means if (s > 0) == (bias > 0)) / len(src_means)) if src_means else None
                strat_rows.append({"model": m, "variable": v, "stratum": name, "n": len(grp), "n_sources": len(per_src),
                                   "bias": round(bias, 5), "MAE": round(statistics.mean(abs(e) for e in errs), 5),
                                   "RMSE": round(rmse(errs), 5), "sign_consistency": round(same_sign, 3) if same_sign is not None else "",
                                   "spearman_trend": round(trend, 3) if trend is not None else ""})
    with open(out / "stratified_errors.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["model", "variable", "stratum", "n", "n_sources", "bias", "MAE", "RMSE",
                                          "sign_consistency", "spearman_trend"])
        w.writeheader()
        w.writerows(strat_rows)

    # variance decomposition
    decomp = {"residual": "log10(pred/obs)" if a.log else "pred-obs", "seed": a.seed, "boot": a.boot, "models": {}}
    for m in preds:
        groups = {}
        for e, r in res[m]:
            groups.setdefault(r[a.source], []).append(e)
        errs = [e for e, _ in res[m]]
        base = icc1(groups)
        entry = {"n": len(errs), "k_sources": len(groups), "bias": statistics.mean(errs) if errs else None,
                 "rmse_pooled": rmse(errs),
                 "rmse_source_equal_weight": (math.sqrt(statistics.mean([statistics.mean([x * x for x in g]) for g in groups.values()]))
                                              if groups else None),
                 "icc1": base}
        if base and len(groups) >= 3 and a.boot > 0:
            keys = list(groups)
            boots = []
            for _ in range(a.boot):
                samp = {f"{k}#{i}": groups[k] for i, k in enumerate(rng.choices(keys, k=len(keys)))}
                r = icc1(samp)
                if r:
                    boots.append(r["icc"])
            if boots:
                entry["icc1_ci95_source_bootstrap"] = [quant(boots, 0.025), quant(boots, 0.975)]
        if base:
            icc = base["icc"]
            entry["detectability"] = ("SWAMPED (inter-source scatter > ~60 % of residual variance: a mechanistic gain is "
                                      "unlikely to be detectable on pooled data; use within-source contrasts or the "
                                      "simulation-ground-truth route)" if icc > 0.6 else
                                      "MARGINAL (ICC 0.4-0.6: pre-register source-equal-weight metrics and within-source "
                                      "contrasts)" if icc > 0.4 else
                                      "OK (inter-source scatter is a minority of residual variance)")
        decomp["models"][m] = entry
    (out / "variance_decomposition.json").write_text(json.dumps(decomp, indent=2))

    # markdown summary
    lines = [f"# Residual map ({decomp['residual']})", "", f"Data: `{a.data}`; source column `{a.source}`; models: {', '.join(preds)}", "",
             "## Variance decomposition", "", "| model | n | sources | bias | RMSE pooled | RMSE source-eq | ICC(1) | 95 % CI (source bootstrap) | detectability |",
             "|---|---|---|---|---|---|---|---|---|"]
    for m, e in decomp["models"].items():
        icc = e["icc1"]["icc"] if e["icc1"] else None
        ci = e.get("icc1_ci95_source_bootstrap")
        lines.append(f"| {m} | {e['n']} | {e['k_sources']} | {e['bias']:.4g} | {e['rmse_pooled']:.4g} | "
                     f"{(e['rmse_source_equal_weight'] or float('nan')):.4g} | {icc if icc is None else f'{icc:.3f}'} | "
                     f"{'' if not ci else f'[{ci[0]:.3f}, {ci[1]:.3f}]'} | {e.get('detectability', '')} |")
    lines += ["", "## Stratified errors (|bias| sorted, strata with n ≥ %d)" % a.min_n, "",
              "| model | variable | stratum | n | sources | bias | MAE | RMSE | sign consistency | trend ρ |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(strat_rows, key=lambda r: -abs(r["bias"])):
        lines.append(f"| {r['model']} | {r['variable']} | {r['stratum']} | {r['n']} | {r['n_sources']} | {r['bias']} | {r['MAE']} | {r['RMSE']} | {r['sign_consistency']} | {r['spearman_trend']} |")
    lines += ["", "Reading guide: a systematic failure region is a stratum whose bias has the same sign in most sources "
              "(sign consistency ≥ 0.7) and a monotone trend (|ρ| ≥ 0.3). Candidate mechanisms must predict the sign, "
              "the monotonicity and, ideally, the functional form of that trend (civmat2-idea)."]
    (out / "residual_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({m: {"icc1": (e["icc1"] or {}).get("icc"), "detectability": e.get("detectability", "")}
                      for m, e in decomp["models"].items()}, indent=1))


if __name__ == "__main__":
    main()
