#!/usr/bin/env bash
# Install civmatflow v2 into a Claude Code config directory.
#
#   ./install.sh [TARGET_CLAUDE_DIR] [--project DIR] [--python BIN] [--bin DIR] [--no-bin]
#
# TARGET_CLAUDE_DIR  the .claude directory Claude Code reads (default: ./.claude of the cwd,
#                    e.g. ~/.claude for a user-level install)
# --project DIR      research workspace that holds venue/, data/, D*/ and codex/C#/ (default: cwd)
# --python BIN       interpreter used by all tools (default: python3)
# --bin DIR          where to symlink bin/civmat2 (default: ~/.local/bin; --no-bin to skip)
#
# What it does
#   * renders skills/ and agents/ into TARGET (copies with {{CIVMAT2_HOME}}, {{CIVMAT2_PROJECT}}
#     and {{CIVMAT2_PYTHON}} substituted) — edit the repo copies and re-run to update;
#   * symlinks each style/<key>/ into TARGET/agents/style/<key> and copies style/INDEX.md once;
#   * writes <repo>/.civmat2.env (gitignored) so `civmat2` knows the project and interpreter.
# Nothing outside TARGET, ~/.local/bin and the repo is touched. Re-running is idempotent.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST=""; PROJECT="$PWD"; PY="python3"; BIN="$HOME/.local/bin"; DO_BIN=1
while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --python) PY="$2"; shift 2 ;;
    --bin) BIN="$2"; shift 2 ;;
    --no-bin) DO_BIN=0; shift ;;
    -h|--help) sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) DST="$1"; shift ;;
  esac
done
DST="${DST:-$PWD/.claude}"
DST="$(mkdir -p "$DST" && cd "$DST" && pwd)"
PROJECT="$(mkdir -p "$PROJECT" && cd "$PROJECT" && pwd)"
command -v "$PY" >/dev/null 2>&1 || { echo "python interpreter not found: $PY"; exit 1; }

render() {  # render SRC DST
  sed -e "s|{{CIVMAT2_HOME}}|$HERE|g" -e "s|{{CIVMAT2_PROJECT}}|$PROJECT|g" -e "s|{{CIVMAT2_PYTHON}}|$PY|g" "$1" > "$2"
}

mkdir -p "$DST/skills" "$DST/agents/style"
n_sk=0; n_ag=0; n_st=0
for d in "$HERE"/skills/civmat2*; do
  name="$(basename "$d")"
  # a symlink from an older install would point at the repo; replace it with a rendered copy
  [ -L "$DST/skills/$name" ] && rm "$DST/skills/$name"
  mkdir -p "$DST/skills/$name"
  render "$d/SKILL.md" "$DST/skills/$name/SKILL.md"
  n_sk=$((n_sk + 1))
done
for f in "$HERE"/agents/*.md; do
  name="$(basename "$f")"
  [ -L "$DST/agents/$name" ] && rm "$DST/agents/$name"
  render "$f" "$DST/agents/$name"
  n_ag=$((n_ag + 1))
done
for d in "$HERE"/style/*/; do
  ln -sfn "${d%/}" "$DST/agents/style/$(basename "$d")"
  n_st=$((n_st + 1))
done
[ -f "$DST/agents/style/INDEX.md" ] || cp "$HERE/style/INDEX.md" "$DST/agents/style/INDEX.md"

cat > "$HERE/.civmat2.env" <<ENV
# written by install.sh $(date -u +%Y-%m-%dT%H:%M:%SZ); sourced by bin/civmat2
CIVMAT2_PROJECT="\${CIVMAT2_PROJECT:-$PROJECT}"
CIVMAT2_PYTHON="\${CIVMAT2_PYTHON:-$PY}"
CIVMAT2_CLAUDE_DIR="\${CIVMAT2_CLAUDE_DIR:-$DST}"
ENV

if [ "$DO_BIN" = 1 ]; then
  mkdir -p "$BIN"
  ln -sfn "$HERE/bin/civmat2" "$BIN/civmat2"
  case ":$PATH:" in *":$BIN:"*) ;; *) echo "note: $BIN is not on PATH; add it or call $HERE/bin/civmat2" ;; esac
fi

echo "installed into $DST: $n_sk skills, $n_ag agents, $n_st style keys (symlinked)"
echo "CIVMAT2_HOME=$HERE  CIVMAT2_PROJECT=$PROJECT  CIVMAT2_PYTHON=$PY"
echo "Note: style corpora (PDFs / extracted text) are NOT in this repo; re-run civmat-style-distiller to rebuild them locally."
