# civmatflow v2 — notes for Claude Code working in this repository

This repository is a workflow (skills, agents, tools, Workflow scripts, templates, style corpora) for civil-engineering-materials papers built on theory + local simulation + public data. The Chinese master skill `skills/civmat2/SKILL.md` is the source of truth for the pipeline; `docs/PIPELINE.md` is the stage-by-stage runbook; `docs/TOOLS.md` documents the CLI.

## Conventions
- **No absolute machine paths** in `skills/`, `agents/`, `workflows/`, `codex/`, `templates/`. Use the placeholders `{{CIVMAT2_HOME}}` (this repo), `{{CIVMAT2_PROJECT}}` (research workspace) and `{{CIVMAT2_PYTHON}}`; `install.sh` renders them. In `codex/PLAYBOOK.md` and `templates/codex/*` use `{{PROJECT_ROOT}}` / `{{PYTHON}}` (rendered by `codex/run_iter.sh`). Workflow scripts take `home` / `project` / `ws` in `args`.
- Tools in `tools/` are **standard library only** (python-docx and PyMuPDF optional, imported lazily). Every tool has a module docstring with usage and is reachable through `bin/civmat2`.
- `style/<key>/` holds distilled artefacts only; `pdfs/`, `text/`, `work/` are gitignored and never committed.
- `docs/WORKFLOW-DESIGN.md` §10 is a historical execution log: append, do not rewrite.
- Chinese file names inside the submission package (`00_作者参考_勿上传`, `作者待办.md`, `投稿包_*.zip`) are part of the 0961 layout; keep them.

## Checks before committing
```bash
make lint      # py_compile, bash -n, workflow parse
make test      # tests/smoke_test.sh — offline, synthetic data, ~10 s
```
When adding a tool: add a `civmat2` subcommand in `bin/civmat2`, a section in `docs/TOOLS.md`, a row in README's tool table and a smoke-test step.

## Hard rules carried by the workflow (do not weaken them in code or prose)
Legal literature channels only · hold-outs frozen by source, guarded by `load_calibration`, evaluated once (`HOLDOUT_CONSUMED`) · PREREG sealed before evaluation · no fabricated data, citations or numbers · parity is parity · external submission only by the authors.
