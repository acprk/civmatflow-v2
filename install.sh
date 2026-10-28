#!/bin/bash
# Install civmatflow v2 into a Claude Code config directory.
# Usage: ./install.sh [TARGET_CLAUDE_DIR]   (default: ./.claude of the current project, e.g. ~/xzy/.claude)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DST="${1:-$PWD/.claude}"
mkdir -p "$DST/skills" "$DST/agents/style"
for d in "$HERE"/skills/civmat2*; do ln -sfn "$d" "$DST/skills/$(basename "$d")"; done
for f in "$HERE"/agents/*.md; do ln -sfn "$f" "$DST/agents/$(basename "$f")"; done
for d in "$HERE"/style/*/; do ln -sfn "${d%/}" "$DST/agents/style/$(basename "$d")"; done
[ -f "$DST/agents/style/INDEX.md" ] || cp "$HERE/style/INDEX.md" "$DST/agents/style/INDEX.md"
echo "installed into $DST"
echo "Note: style corpora (PDFs/text) are NOT in this repo; re-run civmat-style-distiller to rebuild them locally."
