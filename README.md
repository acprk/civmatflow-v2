# civmatflow v2

An agent/skill workflow for civil-engineering-materials papers built on **theory + local simulation + public data**, from venue profiling to a submission package, including a loop in which Claude Code steers Codex miners.

总纲（中文）：`skills/civmat2/SKILL.md`；设计与执行日志：`docs/WORKFLOW-DESIGN.md`；Codex 矿工规则：`codex/PLAYBOOK.md`。

## Pipeline
V0 venue profiling + theory-depth calibration → V1 direction gates (G0 data/licence/compute, G0.5 scoop scan, detectability) → V2–V3 legal retrieval + literature cards + baseline ledger → V2s journal×field style distillation → V4 SOTA reproduction with the hold-out frozen first (G1) → V5 mechanism/idea with falsify-first → V6 pre-registration + one-shot hold-out (G3) → V7 independent falsification → V8–V9 writing/polishing → V10 five-reviewer panel + meta-review + two Codex rounds (G4) → V11 submission package.

Admissible contributions: **M** (mechanism-derived relation that wins on a pre-registered hold-out), **E** (pre-registered evaluation + physically interpretable systematic-error diagnosis + one-shot remedy), and the **simulation-ground-truth** route.

## Contents
| Path | What |
|---|---|
| `skills/` | 11 skills: `civmat2` (master) + venue, direction, lit, sota, idea, prereg, write, review, package, codex-loop |
| `agents/` | civmat-scout, civmat-librarian, civmat-theorist, civmat-style-distiller, civmat-packager; reviewers civrev-theory/experiment/domain/writing/adversary/meta; style writers ms-cemchem-writer, efm-sizeeffect-writer |
| `style/` | style index + distilled STYLE.md / phrasebank / style_check.py / stats / corpus DOI list per journal×field (no PDFs or full texts) |
| `tools/` | `fetch_fulltext.py` (legal OA chain only), `pdf2cards.py`, `holdout_guard.py` (freeze / overlap check / one-shot evaluate), `build_package.py` |
| `workflows/` | `civmat2-direction.js`, `civmat2-review.js` (Claude Code Workflow scripts) |
| `codex/` | `PLAYBOOK.md`, `run_iter.sh` (Codex miner iteration runner) |
| `tests/smoke_test.sh` | synthetic smoke test for holdout_guard |

## Install
```bash
./install.sh ~/xzy/.claude      # symlinks skills, agents and style keys into a Claude Code config dir
```
Paths inside some files point to the original workspace (`/home/luck/xzy/0970project`); adjust if you move it.

## Rules baked in
No fabricated data or citations; legal literature channels only (no shadow libraries); hold-outs frozen by source with sha256 and evaluated once; parity is reported as parity; external submission only by the authors.
