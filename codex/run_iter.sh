#!/bin/bash
# Usage: run_iter.sh C# N [LANE]
#   runs Codex iteration N for direction C# (gpt-6.1-sol, xhigh, multi_agent_v2)
#   cwd = C#/iterN[_LANE]; project root readable via --add-dir
[ -f "$HOME/.codex/stella.env" ] && . "$HOME/.codex/stella.env"
D=$1; N=$2; L=$3
B=/home/luck/xzy/0970project/codex
R=$B/$D
if [ -n "$L" ]; then I=$R/iter${N}_$L; else I=$R/iter$N; fi
mkdir -p $I
cat $B/PLAYBOOK.md $R/brief.txt > $I/prompt.txt
if [ -f $R/feedback.txt ]; then
  printf '\n\n## REVIEWER FEEDBACK (Claude, latest first)\n' >> $I/prompt.txt
  cat $R/feedback.txt >> $I/prompt.txt
fi
if [ -f $R/STATE.txt ]; then
  printf '\n\n## STATE SO FAR\n' >> $I/prompt.txt
  cat $R/STATE.txt >> $I/prompt.txt
fi
if [ -n "$L" ] && [ -f $R/lanes/$L.txt ]; then
  printf '\n\n## YOUR LANE: %s\n' "$L" >> $I/prompt.txt
  cat $R/lanes/$L.txt >> $I/prompt.txt
fi
printf '\n\nThis is iteration %s of direction %s (lane: %s). Your cwd is %s. Compute: at most 3 threads.\n' "$N" "$D" "${L:-main}" "$I" >> $I/prompt.txt
timeout 6h nice -n 10 codex exec --skip-git-repo-check -m gpt-6.1-sol -c model_reasoning_effort=xhigh \
  --enable multi_agent_v2 -s workspace-write -c sandbox_workspace_write.network_access=true \
  -C $I --add-dir /home/luck/xzy/0970project -o $I/last.txt - < $I/prompt.txt > $I/codex.log 2>&1
echo "exit=$?" > $I/done.txt
