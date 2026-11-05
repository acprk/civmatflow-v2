# civmatflow v2

An agent + skill workflow for **civil-engineering-materials papers built on theory, local simulation and public data** — from venue profiling to a submission package — including a loop in which Claude Code steers Codex miners. No new laboratory tests; evidence comes from public data sets, local simulation and derivation.

中文总纲：[`skills/civmat2/SKILL.md`](skills/civmat2/SKILL.md) · 分阶段 runbook：[`docs/PIPELINE.md`](docs/PIPELINE.md) · 工具参考：[`docs/TOOLS.md`](docs/TOOLS.md) · 设计与执行日志：[`docs/WORKFLOW-DESIGN.md`](docs/WORKFLOW-DESIGN.md) · Codex 矿工规则：[`codex/PLAYBOOK.md`](codex/PLAYBOOK.md)

## Pipeline and gates

```
V0 venue profiling + theory-depth calibration
 └─ V1 direction gates ── G0 data/licence/compute · G0.5 scoop scan · detectability (ICC)
     └─ V2–V3 legal retrieval → literature cards → baseline ledger   (V2s style distillation in parallel)
         └─ V4 SOTA reproduction, hold-out frozen FIRST ─────────── G1 reproduction ±10 %
             └─ V5 mechanism / idea, FALSIFY.md first, adversary ── G2 identifiable · detectable · novel
                 └─ V6 pre-registration sealed, ONE hold-out run ── G3 pre-registered criteria
                     └─ V7 independent falsification (adversary + experiment)
                         └─ V8–V9 writing from claims + traceable numbers, style check
                             └─ V10 five blind reviewers + meta + two Codex rounds ── G4 no open major
                                 └─ V11 submission package (zip + sha256)
```

Admissible contributions: **M** (mechanism-derived relation that wins on a pre-registered hold-out), **E** (pre-registered evaluation + physically interpretable systematic-error diagnosis + one-shot remedy, positive or negative), and the **simulation-ground-truth** route. Parity is reported as parity.

## Contents

| Path | What |
|---|---|
| `skills/` | 11 skills: `civmat2` (master, with the 15 lessons from 15 closed directions) + venue, direction, lit, sota, idea, prereg, write, review, package, codex-loop |
| `agents/` | 13 agents: scouts and builders (`civmat-scout`, `civmat-librarian`, `civmat-theorist`, `civmat-style-distiller`, `civmat-packager`), reviewers (`civrev-theory/experiment/domain/writing/adversary/meta`), style writers (`ms-cemchem-writer`, `efm-sizeeffect-writer`) |
| `tools/` | 9 standard-library Python tools (see below) |
| `bin/civmat2` | one CLI for all tools, templates and workspace scaffolding |
| `workflows/` | 5 Claude Code Workflow scripts: direction, sota, idea (ideate / falsify), write, review |
| `templates/` | PREREG, FALSIFY, PROVENANCE, DIRECTION card, BASELINES, G1 report, IDEA, literature card, OUTLINE, CLAIM_EVIDENCE, NUMBERS_USED, response table, author to-do, run_all.sh, Codex brief/feedback/STATE/STATUS |
| `style/` | style index + distilled `STYLE.md` / `phrasebank.md` / `style_check.py` / `stats.json` / `CORPUS.md` per journal×field (`efm-sizeeffect`, `ms-cemchem`); no PDFs or full texts |
| `codex/` | `PLAYBOOK.md` (miner rules), `run_iter.sh` (iteration runner) |
| `docs/` | pipeline runbook, tool reference, design draft + execution log |
| `tests/smoke_test.sh` | offline synthetic test of every tool, the CLI, the installer and the workflow syntax |

### Tools (`civmat2 <cmd>`; all standard library, `python3 ≥ 3.9`)

| Command | Stage | Does |
|---|---|---|
| `venue fetch / classify / score` | V0 | Crossref/OpenAlex records per journal-year → class (experimental / computational-theory / pure ML / review) and topic map with growth and crowding; manual-sample agreement rate |
| `depth` | V0 | equation / figure / table / hold-out-vocabulary tallies of accepted papers → draft target depth band |
| `fetch` | V2 | legal full text only: Unpaywall → OpenAlex → Semantic Scholar → arXiv → CORE / Elsevier TDM (keys) → `NEED_FROM_USER.md`; every attempt logged |
| `cards` | V3 | PDF → text → literature-card skeleton (DOI guess, candidate equations and metric lines with page numbers) |
| `holdout freeze / check / seal / evaluate / status` | V4–V6 | group-wise frozen hold-out with sha256 and read-only files; zero-overlap assertion; PREREG + code sealing; fail-closed one-shot evaluation (`HOLDOUT_CONSUMED`); `load_calibration()` library guard |
| `residuals` | V4 | stratified residual map (bias, sign consistency across sources, Spearman trend) and between/within-source variance decomposition: ICC(1) with source-bootstrap CI and a detectability verdict |
| `numcheck fill / check` | V8–V9 | `{{key}}` placeholders filled from `NUMBERS_USED.json`; every numeral in the prose must trace back to a generated value |
| `refcheck` | V9–V11 | every DOI resolves (Crossref → DataCite → doi.org), title similarity for .bib entries, `CITATION_CHECK.md` |
| `style <key>` | V9–V10 | journal×field style checker (score = share of metrics inside the corpus P10–P90 band) |
| `package` | V11 | submission package in the 0961 ES layout; non-redistributable data replaced by provenance + download instructions; manifest, zip, sha256 |
| `init`, `template` | any | scaffold a direction workspace; print a template |
| `codex C# N [LANE]` | loop | one Codex miner iteration with the rendered PLAYBOOK, brief, feedback and state |

## Install

```bash
git clone https://github.com/acprk/civmatflow-v2 && cd civmatflow-v2
./install.sh ~/.claude --project ~/research/0970project      # or any .claude dir Claude Code reads
civmat2 test                                                 # offline smoke test
```

`install.sh` renders `skills/` and `agents/` into the target directory with the three placeholders `{{CIVMAT2_HOME}}` (this repo), `{{CIVMAT2_PROJECT}}` (your research workspace) and `{{CIVMAT2_PYTHON}}` substituted, symlinks each `style/<key>/` into `agents/style/`, writes `.civmat2.env` (gitignored) and links `bin/civmat2` into `~/.local/bin`. Edit the repo copies and re-run to update. Optional extras: `pip install -r requirements-optional.txt` (python-docx for .docx drafts, PyMuPDF when `pdftotext` is absent).

## Quick start for a new direction

```bash
civmat2 init ~/research/0970project/D7_slug          # workspace with templates
civmat2 fetch 10.xxxx/yyy --out D7_slug/lit/pdfs --email you@example.org
civmat2 cards D7_slug/lit/pdfs --cards D7_slug/lit/cards
civmat2 holdout freeze --data D7_slug/data/processed/tidy.csv --group source --seed 1 --out D7_slug/HOLDOUT
civmat2 residuals D7_slug/data/processed/calibration.csv --obs y --pred B0 --source source --by age_d,w_b --out D7_slug/results --log
civmat2 holdout seal --prereg D7_slug/PREREG.md --split D7_slug/HOLDOUT --code D7_slug/code
civmat2 holdout evaluate --split D7_slug/HOLDOUT --prereg D7_slug/PREREG.md --sha D7_slug/PREREG.sha256 \
    --manifest D7_slug/FROZEN_MANIFEST.json --cmd "python3 D7_slug/code/evaluate_holdout.py"
civmat2 numcheck check D7_slug/paper/manuscript_draft.md --numbers D7_slug/paper/NUMBERS_USED.json --allow-years
civmat2 refcheck D7_slug/paper/refs.bib --report D7_slug/paper/CITATION_CHECK.md
civmat2 package --ws D7_slug --name 方向名 --journal "Cement and Concrete Research"
```

In Claude Code, start with the `civmat2` skill; each stage names its skill, agents and Workflow script (`workflows/*.js`, run with `Workflow({scriptPath, args: {home, project|ws, ...}})` once the user has opted into multi-agent orchestration).

## Rules baked in

No fabricated data, citations or numbers · legal literature channels only (no shadow libraries; paywalled key competitors are a reason to drop a target) · hold-outs frozen by source with sha256, guarded in code and evaluated exactly once · pre-registration sealed before evaluation · parity reported as parity, recalibration never called a mechanism · theory depth matched to accepted papers, derivations in the appendix · ≤3 threads per process, `nice 10` · external submission only by the authors.

## Development

```bash
make test        # tests/smoke_test.sh (also run by GitHub Actions)
make lint        # py_compile + bash -n + workflow parse
make install DST=~/.claude PROJECT=~/research/0970project
```
