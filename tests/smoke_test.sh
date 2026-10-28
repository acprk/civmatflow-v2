#!/bin/bash
# Smoke test for civmatflow v2 tools (synthetic data only; writes under /tmp/civmat2_smoke).
set -e
T=/tmp/civmat2_smoke
PY=/home/luck/xzy/0970project/.venv/bin/python
TOOLS=/home/luck/xzy/0970project/civmatflow2/tools
rm -rf $T; mkdir -p $T/ws/paper $T/ws/results $T/ws/code $T/ws/data/processed $T/ws/data/raw/demo
printf 'record_id,source,y\n' > $T/data.csv
for i in $(seq 1 40); do echo "r$i,s$((i % 8)),$i" >> $T/data.csv; done
$PY $TOOLS/holdout_guard.py freeze --data $T/data.csv --group source --seed 1 --out $T/split
head -3 $T/data.csv > $T/cal_ok.csv
$PY $TOOLS/holdout_guard.py check --data $T/data.csv --split $T/split && exit 1 || echo "overlap detection works"
echo "# PREREG demo" > $T/PREREG.md
sha256sum $T/PREREG.md > $T/PREREG.sha256
$PY $TOOLS/holdout_guard.py evaluate --split $T/split --prereg $T/PREREG.md --sha $T/PREREG.sha256 --cmd "true"
$PY $TOOLS/holdout_guard.py evaluate --split $T/split --prereg $T/PREREG.md --sha $T/PREREG.sha256 --cmd "true" && exit 1 || echo "second evaluation refused"
echo "licence: CC BY 4.0" > $T/ws/data/raw/demo/PROVENANCE.md
echo "x" > $T/ws/results/r.csv
echo "echo run" > $T/ws/code/run_all.sh
echo "ok"
