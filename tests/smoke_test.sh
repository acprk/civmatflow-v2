#!/usr/bin/env bash
# Smoke test for civmatflow v2 (synthetic data only, no network). Run: bash tests/smoke_test.sh
# Covers: civmat2 CLI, init scaffold, holdout_guard (freeze/check/seal/evaluate/status + library
# guard), residual_map, number_check, refcheck --offline, venue_profile classify (offline),
# depth_tally, pdf2cards (when pdftotext is present), build_package, install.sh rendering,
# and syntax checks of every script.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${CIVMAT2_PYTHON:-python3}"
C="$HERE/bin/civmat2"
T="${TMPDIR:-/tmp}/civmat2_smoke_$$"
rm -rf "$T"; mkdir -p "$T"
trap 'rm -rf "$T"' EXIT
pass() { echo "  ok  $1"; }
fail() { echo "FAIL  $1"; exit 1; }
expect_fail() { if "$@" >/dev/null 2>&1; then return 1; else return 0; fi; }

echo "[1] syntax"
for f in "$HERE"/tools/*.py "$HERE"/style/*/style_check.py; do "$PY" -m py_compile "$f"; done
for f in "$HERE"/bin/civmat2 "$HERE"/install.sh "$HERE"/codex/run_iter.sh "$HERE"/templates/run_all.sh; do bash -n "$f"; done
if command -v node >/dev/null 2>&1; then
  # Workflow scripts run inside an async function (top-level return/await, agent/parallel globals):
  # wrap them the same way before parsing.
  for f in "$HERE"/workflows/*.js; do
    { echo 'async function __wf(args, agent, parallel, pipeline, phase, log) {'; sed 's/^export const meta/const meta/' "$f"; echo '}'; } | node --input-type=module --check
  done
  pass "workflows parse as ES modules"
fi
pass "python/bash syntax"

echo "[2] cli + init"
[ "$("$C" home)" = "$HERE" ] || fail "civmat2 home"
"$C" init "$T/ws" >/dev/null
for f in DIRECTION.md BASELINES.md FALSIFY.md PREREG.md notes/G1_REPORT.md paper/OUTLINE.md paper/NUMBERS_USED.json code/run_all.sh; do
  [ -f "$T/ws/$f" ] || fail "init missing $f"
done
"$C" template FALSIFY | grep -q "FALSIFY" || fail "template"
pass "init scaffold + templates"

echo "[3] holdout_guard"
WS="$T/ws"
printf 'record_id,source,x,y,B0,M1\n' > "$WS/data/processed/tidy.csv"
"$PY" - "$WS/data/processed/tidy.csv" <<'PYEOF'
import random, sys
rng = random.Random(3)
with open(sys.argv[1], "a") as f:
    for i in range(1, 121):
        src = f"lab{i % 8}"
        x = rng.uniform(1, 100)
        off = ((i % 8) - 3.5) * 0.08    # symmetric source offsets -> between-source variance
        y = 2.0 + 0.1 * x + off + rng.gauss(0, 0.2)
        b0 = 2.0 + 0.1 * x + 0.004 * x  # baseline with a trend in x
        m1 = 2.0 + 0.1 * x
        f.write(f"r{i},{src},{x:.3f},{y:.4f},{b0:.4f},{m1:.4f}\n")
PYEOF
"$C" holdout freeze --data "$WS/data/processed/tidy.csv" --group source --seed 1 --out "$WS/HOLDOUT" >/dev/null
[ -f "$WS/HOLDOUT/split.json" ] || fail "freeze"
expect_fail "$C" holdout freeze --data "$WS/data/processed/tidy.csv" --group source --seed 1 --out "$WS/HOLDOUT" || fail "re-freeze must be refused"
expect_fail "$C" holdout check --data "$WS/data/processed/tidy.csv" --split "$WS/HOLDOUT" || fail "overlap must be detected"
"$PY" - "$HERE" "$WS" <<'PYEOF'
import sys, csv
sys.path.insert(0, sys.argv[1] + "/tools")
from holdout_guard import load_calibration, load_holdout
ws = sys.argv[2]
cal = load_calibration(ws + "/data/processed/tidy.csv", ws + "/HOLDOUT")
assert 0 < len(cal) < 120, len(cal)
with open(ws + "/data/processed/calibration.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cal[0])); w.writeheader(); w.writerows(cal)
try:
    load_holdout(ws + "/data/processed/tidy.csv", ws + "/HOLDOUT"); raise SystemExit("load_holdout must refuse outside evaluate")
except PermissionError:
    pass
PYEOF
"$C" holdout check --data "$WS/data/processed/calibration.csv" --split "$WS/HOLDOUT" >/dev/null || fail "calibration overlap"
pass "freeze / check / library guard"
cat > "$WS/code/evaluate_holdout.py" <<PYEOF
import os, sys, json
sys.path.insert(0, "$HERE/tools")
from holdout_guard import load_holdout
rows = load_holdout("$WS/data/processed/tidy.csv", "$WS/HOLDOUT")
os.makedirs("$WS/results", exist_ok=True)
json.dump({"n_holdout": len(rows)}, open("$WS/results/holdout_metrics.json", "w"))
print("evaluated", len(rows), "hold-out rows")
PYEOF
"$C" holdout seal --prereg "$WS/PREREG.md" --split "$WS/HOLDOUT" --code "$WS/code" >/dev/null
[ -f "$WS/PREREG.sha256" ] && [ -f "$WS/FROZEN_MANIFEST.json" ] || fail "seal outputs"
echo "# tampered" >> "$WS/code/evaluate_holdout.py" 2>/dev/null || true
expect_fail "$C" holdout evaluate --split "$WS/HOLDOUT" --prereg "$WS/PREREG.md" --sha "$WS/PREREG.sha256" --manifest "$WS/FROZEN_MANIFEST.json" --cmd "$PY $WS/code/evaluate_holdout.py" || fail "changed code must be refused"
[ ! -f "$WS/HOLDOUT/HOLDOUT_CONSUMED" ] || fail "refused evaluation must not consume"
rm -f "$WS/PREREG.sha256" "$WS/FROZEN_MANIFEST.json"; chmod u+w "$WS/PREREG.md"
"$C" holdout seal --prereg "$WS/PREREG.md" --split "$WS/HOLDOUT" --code "$WS/code" >/dev/null
"$C" holdout evaluate --split "$WS/HOLDOUT" --prereg "$WS/PREREG.md" --sha "$WS/PREREG.sha256" --manifest "$WS/FROZEN_MANIFEST.json" --cmd "$PY $WS/code/evaluate_holdout.py" >/dev/null
[ -f "$WS/results/holdout_metrics.json" ] || fail "evaluation did not run"
expect_fail "$C" holdout evaluate --split "$WS/HOLDOUT" --prereg "$WS/PREREG.md" --sha "$WS/PREREG.sha256" --cmd "true" || fail "second evaluation must be refused"
"$C" holdout status --split "$WS/HOLDOUT" | grep -q '"status": "finished"' || fail "status"
pass "seal / one-shot evaluate / consumed"

echo "[4] residual_map"
"$C" residuals "$WS/data/processed/calibration.csv" --obs y --pred B0,M1 --source source --by x --out "$WS/results" --boot 200 >/dev/null
[ -f "$WS/results/stratified_errors.csv" ] && [ -f "$WS/results/variance_decomposition.json" ] && [ -f "$WS/results/residual_map.md" ] || fail "residual outputs"
"$PY" - "$WS/results/variance_decomposition.json" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1]))["models"]
assert d["B0"]["icc1"]["icc"] >= 0 and "detectability" in d["B0"]
assert d["M1"]["rmse_pooled"] < d["B0"]["rmse_pooled"]
PYEOF
pass "stratified errors + ICC"

echo "[5] number_check"
cat > "$WS/paper/NUMBERS_USED.json" <<'JEOF'
{"_meta": {"generated_by": "test"}, "mae_b0": {"value": 1.3391, "fmt": ".2f", "unit": "mm"}, "n_sources": 32, "r2": 0.812}
JEOF
cat > "$WS/paper/draft.md" <<'MEOF'
# Abstract
The baseline reached an MAE of {{mae_b0}} mm on {{n_sources}} sources (R² = {{r2}}), see Fig. 2 and Eq. (4) [12].
## 2.1 Data
Records from 2019–2024 were used; the hold-out fraction was 0.3. Doubtful value: 7.77 mm.
MEOF
"$C" numcheck fill "$WS/paper/draft.md" --numbers "$WS/paper/NUMBERS_USED.json" --out "$WS/paper/filled.md" >/dev/null
grep -q "1.34 mm on 32 sources" "$WS/paper/filled.md" || fail "fill"
expect_fail "$C" numcheck check "$WS/paper/filled.md" --numbers "$WS/paper/NUMBERS_USED.json" --allow 0.3 --allow-years || fail "7.77 must be flagged"
"$C" numcheck check "$WS/paper/filled.md" --numbers "$WS/paper/NUMBERS_USED.json" --allow 0.3,7.77 --allow-years --report "$WS/paper/NUMBER_CHECK.md" >/dev/null
grep -q "untraceable numerals: \*\*0\*\*" "$WS/paper/NUMBER_CHECK.md" || fail "number check report"
pass "fill + check"

echo "[6] refcheck (offline)"
cat > "$WS/paper/refs.bib" <<'BEOF'
@article{ok1, title={Some paper}, doi={10.1617/s11527-022-01947-3}, year={2022}}
@article{nodoi, title={Old standard}, year={1999}}
@article{bad, title={Broken}, doi={10.1617}, year={2020}}
BEOF
expect_fail "$C" refcheck "$WS/paper/refs.bib" --offline --report "$WS/paper/CITATION_CHECK.md" || fail "bad DOI syntax must fail"
grep -q "BAD_SYNTAX" "$WS/paper/CITATION_CHECK.md" && grep -q "NO_DOI" "$WS/paper/CITATION_CHECK.md" || fail "refcheck report"
pass "syntax + report"

echo "[7] venue_profile classify (offline) + depth_tally"
mkdir -p "$T/venue/raw"
cat > "$T/venue/raw/CCR_2024.jsonl" <<'JEOF'
{"doi":"10.1/a","title":"A thermodynamic model of alkali uptake by C-S-H","abstract":"","year":2024,"journal":"CCR","key":"CCR","cited":12}
{"doi":"10.1/b","title":"Experimental study on the effect of fly ash on chloride ingress","abstract":"","year":2024,"journal":"CCR","key":"CCR","cited":5}
{"doi":"10.1/c","title":"Machine learning prediction of carbonation depth","abstract":"","year":2024,"journal":"CCR","key":"CCR","cited":30}
{"doi":"10.1/d","title":"A review of size effect in quasi-brittle fracture","abstract":"","year":2024,"journal":"CCR","key":"CCR","cited":40}
JEOF
cat > "$T/venue/raw/CCR_2023.jsonl" <<'JEOF'
{"doi":"10.1/e","title":"Numerical simulation of creep and shrinkage in concrete","abstract":"","year":2023,"journal":"CCR","key":"CCR","cited":8}
{"doi":"10.1/f","title":"Properties of recycled aggregate concrete","abstract":"","year":2023,"journal":"CCR","key":"CCR","cited":3}
JEOF
"$C" venue classify --out "$T/venue" --sample 3 >/dev/null
grep -q "thermodynamics_hydration" "$T/venue/topic_map.md" || fail "topic map"
grep -q "pure_ml" "$T/venue/classified.csv" && grep -q "review" "$T/venue/classified.csv" || fail "classes"
printf 'doi,title,auto_class,manual_class\n10.1/a,x,computational_theory,computational_theory\n10.1/b,x,experimental,experimental\n' > "$T/venue/sample.csv"
"$C" venue score --sample "$T/venue/sample.csv" | grep -q '"agreement": 1.0' || fail "score"
mkdir -p "$T/depth"
printf 'Abstract\nThis paper derives a model.\n1 Introduction\nThe hold-out set was used. RMSE was 0.3.\n(1)\n(2)\nFig. 3 shows. Table 2 lists.\fAppendix A\n' > "$T/depth/p1.txt"
printf 'Abstract\nData.\n1 Introduction\nMachine learning. Fig. 10.\n(5)\n' > "$T/depth/p2.txt"
"$C" depth "$T/depth" --out "$T/depth/tally" >/dev/null
grep -q "n_eqs" "$T/depth/tally.csv" && grep -q "target band" "$T/depth/tally.md" || fail "depth tally"
pass "venue classify/score + depth tally"

echo "[8] pdf2cards"
if command -v pdftotext >/dev/null 2>&1 && "$PY" -c "import reportlab" 2>/dev/null; then
  "$PY" - "$T/lit" <<'PYEOF'
import sys, pathlib
from reportlab.pdfgen import canvas
d = pathlib.Path(sys.argv[1]); d.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(d / "demo.pdf")); c.drawString(72, 750, "A demo paper on size effect https://doi.org/10.1016/j.engfracmech.2020.000001")
c.drawString(72, 730, "sigma_N = B f_t (1 + D/D0)^(-1/2)   (1)"); c.drawString(72, 710, "The RMSE was 2.3 %."); c.save()
PYEOF
  "$C" cards "$T/lit" --cards "$T/lit/cards" >/dev/null
  grep -q "doi: 10.1016/j.engfracmech.2020.000001" "$T/lit/cards/demo.md" || fail "card doi"
  pass "card skeleton from PDF"
else
  echo "  skip pdf2cards (needs pdftotext + reportlab)"
fi

echo "[9] build_package"
mkdir -p "$WS/data/raw/demo" "$WS/data/raw/nc"
echo "licence: CC BY 4.0" > "$WS/data/raw/demo/PROVENANCE.md"; echo "1,2" > "$WS/data/raw/demo/data.csv"
echo "licence: CC BY-NC 4.0" > "$WS/data/raw/nc/PROVENANCE.md"; echo "secret" > "$WS/data/raw/nc/data.csv"
echo "x" > "$WS/results/r.csv"; echo "# demo" > "$WS/review/meta.md"
"$C" package --ws "$WS" --name 冒烟 --journal CCR --out "$T/out" > "$T/pkg.json"
grep -q '"package"' "$T/pkg.json" || fail "package"
ls "$T"/out/投稿包_冒烟_*.zip >/dev/null || fail "zip"
"$PY" - "$WS/submit/07_Supplementary_data_and_code.zip" <<'PYEOF'
import sys, zipfile
names = zipfile.ZipFile(sys.argv[1]).namelist()
assert "data/raw/demo/data.csv" in names, names
assert "data/raw/nc/data.csv" not in names and "data/raw/nc/PROVENANCE.md" in names, names
PYEOF
grep -q "01 cover letter" "$WS/submit/README_投稿上传顺序与作者待办.md" || fail "missing list"
pass "package layout + licence filter"

echo "[10] install.sh rendering"
[ -f "$HERE/.civmat2.env" ] && cp "$HERE/.civmat2.env" "$T/env.bak"   # keep the user's settings
"$HERE/install.sh" "$T/claude" --project "$T/proj" --no-bin >/dev/null
[ -f "$T/claude/skills/civmat2/SKILL.md" ] && [ -f "$T/claude/agents/civrev-meta.md" ] && [ -L "$T/claude/agents/style/ms-cemchem" ] || fail "install layout"
! grep -rq "{{CIVMAT2_" "$T/claude/skills" "$T/claude/agents"/*.md || fail "unrendered placeholders"
grep -q "$HERE" "$T/claude/skills/civmat2/SKILL.md" || fail "home not rendered"
if [ -f "$T/env.bak" ]; then cp "$T/env.bak" "$HERE/.civmat2.env"; else rm -f "$HERE/.civmat2.env"; fi
pass "placeholders rendered"

echo "ALL SMOKE TESTS PASSED"
