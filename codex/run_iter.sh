#!/usr/bin/env bash
# Run one Codex miner iteration for a direction.
#
#   codex/run_iter.sh C# N [LANE]          (or: civmat2 codex C# N [LANE])
#
# Layout (under CIVMAT2_PROJECT, default: cwd):
#   codex/C#/brief.txt        direction brief (template: templates/codex/brief.txt)
#   codex/C#/feedback.txt     reviewer (Claude) feedback, latest first      [optional]
#   codex/C#/STATE.txt        state carried between iterations               [optional]
#   codex/C#/lanes/<LANE>.txt lane brief for parallel lanes                  [optional]
#   codex/C#/iterN[_LANE]/    this iteration's cwd: prompt.txt, codex.log, last.txt, done.txt
#
# Environment (all optional): CIVMAT2_PROJECT, CIVMAT2_HOME, CIVMAT2_PYTHON, CODEX_BIN (default codex),
#   CODEX_MODEL (default gpt-6.1-sol), CODEX_EFFORT (default xhigh), CODEX_TIMEOUT (default 6h),
#   CODEX_EXTRA (extra flags), CODEX_ENV_FILE (sourced first, e.g. ~/.codex/stella.env).
set -uo pipefail
D="${1:-}"; N="${2:-}"; L="${3:-}"
[ -n "$D" ] && [ -n "$N" ] || { sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
SELF="$(readlink -f "${BASH_SOURCE[0]}")"
export CIVMAT2_HOME="${CIVMAT2_HOME:-$(cd "$(dirname "$SELF")/.." && pwd)}"
[ -f "$CIVMAT2_HOME/.civmat2.env" ] && . "$CIVMAT2_HOME/.civmat2.env"
ENVF="${CODEX_ENV_FILE:-$HOME/.codex/stella.env}"; [ -f "$ENVF" ] && . "$ENVF"
PROJECT="${CIVMAT2_PROJECT:-$PWD}"
PY="${CIVMAT2_PYTHON:-python3}"
MODEL="${CODEX_MODEL:-gpt-6.1-sol}"; EFFORT="${CODEX_EFFORT:-xhigh}"; TMO="${CODEX_TIMEOUT:-6h}"; BIN="${CODEX_BIN:-codex}"
B="$PROJECT/codex"; R="$B/$D"
[ -f "$R/brief.txt" ] || { echo "missing $R/brief.txt (template: $CIVMAT2_HOME/templates/codex/brief.txt)"; exit 2; }
if [ -n "$L" ]; then I="$R/iter${N}_$L"; else I="$R/iter$N"; fi
mkdir -p "$I"
# PLAYBOOK with the local paths rendered in
sed -e "s|{{PROJECT_ROOT}}|$PROJECT|g" -e "s|{{PYTHON}}|$PY|g" -e "s|{{CIVMAT2_HOME}}|$CIVMAT2_HOME|g" "$CIVMAT2_HOME/codex/PLAYBOOK.md" > "$I/prompt.txt"
printf '\n\n## DIRECTION BRIEF\n' >> "$I/prompt.txt"
sed -e "s|{{PROJECT_ROOT}}|$PROJECT|g" "$R/brief.txt" >> "$I/prompt.txt"
if [ -f "$R/feedback.txt" ]; then printf '\n\n## REVIEWER FEEDBACK (Claude, latest first)\n' >> "$I/prompt.txt"; cat "$R/feedback.txt" >> "$I/prompt.txt"; fi
if [ -f "$R/STATE.txt" ]; then printf '\n\n## STATE SO FAR\n' >> "$I/prompt.txt"; cat "$R/STATE.txt" >> "$I/prompt.txt"; fi
if [ -n "$L" ] && [ -f "$R/lanes/$L.txt" ]; then printf '\n\n## YOUR LANE: %s\n' "$L" >> "$I/prompt.txt"; cat "$R/lanes/$L.txt" >> "$I/prompt.txt"; fi
printf '\n\nThis is iteration %s of direction %s (lane: %s). Your cwd is %s. Compute: at most 3 threads, nice 10.\n' "$N" "$D" "${L:-main}" "$I" >> "$I/prompt.txt"
command -v "$BIN" >/dev/null 2>&1 || { echo "codex binary not found ($BIN); prompt written to $I/prompt.txt"; echo "exit=127" > "$I/done.txt"; exit 127; }
echo "started=$(date -u +%Y-%m-%dT%H:%M:%SZ) model=$MODEL effort=$EFFORT" > "$I/done.txt"
# shellcheck disable=SC2086
timeout "$TMO" nice -n 10 "$BIN" exec --skip-git-repo-check -m "$MODEL" -c "model_reasoning_effort=$EFFORT" \
  --enable multi_agent_v2 -s workspace-write -c sandbox_workspace_write.network_access=true \
  -C "$I" --add-dir "$PROJECT" ${CODEX_EXTRA:-} -o "$I/last.txt" - < "$I/prompt.txt" > "$I/codex.log" 2>&1
rc=$?
echo "exit=$rc finished=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$I/done.txt"
head -1 "$I/last.txt" 2>/dev/null || true
exit $rc
