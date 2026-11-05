#!/usr/bin/env bash
# Reproduce every number in the manuscript from data/ to results/ (≤3 threads, nice 10).
# Usage: bash code/run_all.sh   (from the workspace root); outputs are compared with expected_output/.
set -euo pipefail
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=3 MKL_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3
PY="${CIVMAT2_PYTHON:-python3}"
start=$(date +%s)
# 1. clean data          nice -n 10 "$PY" code/01_clean.py
# 2. baselines (calibration only; uses holdout_guard.load_calibration)
#                        nice -n 10 "$PY" code/02_baselines.py
# 3. residual map        civmat2 residuals data/processed/tidy.csv --obs y --pred B0 --source source --by ... --out results/
# 4. candidate model     nice -n 10 "$PY" code/03_model.py
# 5. numbers for paper   nice -n 10 "$PY" code/make_numbers.py > paper/NUMBERS_USED.json
echo "run_all finished in $(( $(date +%s) - start )) s (wall); CPU seconds: see /usr/bin/time output if used"
