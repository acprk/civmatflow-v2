#!/usr/bin/env python3
"""Theory-depth tally (V0): count what accepted papers actually contain.

Reads pdftotext output (one .txt per paper, form-feed between pages) and tallies per paper:
pages, words, numbered equations, figures, tables, appendix presence, hold-out /
validation vocabulary, baseline-comparison vocabulary, error-metric vocabulary, data set
vocabulary and derivation vocabulary. The qualitative columns (derivation type, true
hold-out, number of baselines re-run on the same data) are left blank for the agent
to fill after reading, because they cannot be counted reliably.

Outputs: <out>.csv (one row per paper) and <out>.md (P10 / P50 / P90 per numeric column
and a draft "target depth band" statement to be confirmed by reading).

Usage: depth_tally.py TEXT_DIR --out venue/theory_depth_tally [--glob "*.txt"]
Standard library only.
"""
import argparse
import csv
import pathlib
import re
import statistics

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]+")
PATTERNS = {
    "holdout_terms": r"\b(hold[- ]?out|held[- ]out|test set|validation set|unseen data|blind (prediction|test)|out[- ]of[- ]sample|cross[- ]validation|leave[- ]one[- ]out|pre[- ]registered)\b",
    "baseline_terms": r"\b(baseline\w*|benchmark\w*|compared with|comparison with|existing models?|code models?|fib|aci 209|eurocode|model code|b3|b4)\b",
    "metric_terms": r"\b(rmse|mae|mape|r\^?2|r²|coefficient of variation|cov|mean ratio|bias|residual\w*|standard error)\b",
    "dataset_terms": r"\b(database|data ?set|data base|data bank|compiled|collected from the literature|experimental data from)\b",
    "derivation_terms": r"\b(derive[ds]?|derivation|it follows that|substituting|assuming that|integrating|differentiating|closed[- ]form|analytical solution|dimensional analysis|asymptotic)\b",
    "ml_terms": r"\b(machine learning|neural network|random forest|xgboost|gradient boosting|deep learning)\b",
}


def tally(text):
    pages = text.split("\f")
    words = WORD.findall(text)
    low = text.lower()
    eqn = [int(x) for x in re.findall(r"^\s*\((\d{1,3})[a-z]?\)\s*$", text, flags=re.M)]
    eqn += [int(x) for x in re.findall(r"\bEqs?\.\s*\(?(\d{1,3})\)?", text)]
    eqn = [e for e in eqn if e < 200]
    n_figs = max([int(x) for x in re.findall(r"\bFig(?:ure|s?\.)\s*(\d{1,2})", text)] or [0])
    n_tab = max([int(x) for x in re.findall(r"\bTable\s+(\d{1,2})\b", text)] or [0])
    appendix = int(bool(re.search(r"^\s*appendix\b", low, flags=re.M)))
    row = {"pages": len([p for p in pages if p.strip()]), "words": len(words), "n_eqs": max(eqn) if eqn else 0,
           "n_figs": n_figs, "n_tables": n_tab, "appendix": appendix}
    for k, pat in PATTERNS.items():
        row[k] = len(re.findall(pat, low))
    return row


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
    ap.add_argument("text_dir")
    ap.add_argument("--out", required=True, help="output prefix (writes <out>.csv and <out>.md)")
    ap.add_argument("--glob", default="*.txt")
    a = ap.parse_args()
    files = sorted(pathlib.Path(a.text_dir).glob(a.glob))
    if not files:
        raise SystemExit(f"no files matching {a.glob} in {a.text_dir}")
    rows = []
    for f in files:
        r = {"key": f.stem, **tally(f.read_text(encoding="utf-8", errors="ignore")),
             "derivation_type": "", "true_holdout": "", "n_baselines_rerun": "", "n_datasets": "", "notes": ""}
        rows.append(r)
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = list(rows[0])
    with open(str(out) + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    num = [c for c in cols if c not in ("key", "derivation_type", "true_holdout", "n_baselines_rerun", "n_datasets", "notes")]
    lines = [f"# Theory-depth tally ({len(rows)} papers from `{a.text_dir}`)", "",
             "| metric | P10 | P50 | P90 | mean |", "|---|---|---|---|---|"]
    med = {}
    for c in num:
        vals = [r[c] for r in rows]
        med[c] = quant(vals, .5)
        lines.append(f"| {c} | {quant(vals, .1):.3g} | {med[c]:.3g} | {quant(vals, .9):.3g} | {statistics.mean(vals):.3g} |")
    lines += ["", "## Draft target band (confirm by reading; fill derivation_type / true_holdout / n_baselines_rerun in the CSV)", "",
              f"- numbered equations in the main text: about {quant([r['n_eqs'] for r in rows], .25):.0f}–{quant([r['n_eqs'] for r in rows], .75):.0f} (median {med['n_eqs']:.0f})",
              f"- figures: median {med['n_figs']:.0f}; tables: median {med['n_tables']:.0f}; pages: median {med['pages']:.0f}",
              f"- papers mentioning hold-out / validation vocabulary: {sum(1 for r in rows if r['holdout_terms'] > 0)}/{len(rows)} "
              "(vocabulary only — a true hold-out must be confirmed by reading)",
              f"- papers with an appendix: {sum(1 for r in rows if r['appendix'])}/{len(rows)}",
              f"- papers mentioning ML: {sum(1 for r in rows if r['ml_terms'] > 0)}/{len(rows)}", "",
              "Rule (civmat2, lesson 14): match the accepted-paper band; put anything deeper in an appendix. "
              "What is scarce in accepted papers is a fair baseline comparison and a true hold-out, not mathematics."]
    pathlib.Path(str(out) + ".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}.csv and {out}.md ({len(rows)} papers)")


if __name__ == "__main__":
    main()
