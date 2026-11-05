# Tool reference (`civmat2 <cmd>`)

All tools are standard-library Python 3 (`python-docx` and `PyMuPDF` are optional) and live in `tools/`. `bin/civmat2` resolves the repo root from its own location, sources `.civmat2.env` (written by `install.sh`) and dispatches. `civmat2 env` prints the resolved `CIVMAT2_HOME`, `CIVMAT2_PROJECT`, `CIVMAT2_PYTHON`.

## Workspace layout (`civmat2 init <ws>`)

```
<ws>/
  DIRECTION.md  BASELINES.md  FALSIFY.md  PREREG.md  (PREREG.sha256, FROZEN_MANIFEST.json after seal)
  data/raw/<dataset>/PROVENANCE.md (+ download.sh, sha256sum.txt)    data/processed/tidy.csv
  HOLDOUT/ split.json holdout_ids.csv calibration_ids.csv (HOLDOUT_CONSUMED, evaluations.log)
  lit/pdfs/ lit/text/ lit/cards/ (fetch_log.jsonl, LICENSES.tsv, NEED_FROM_USER.md)
  notes/G1_REPORT.md   ideas/<slug>.md  ideas/<slug>.FALSIFY.md  ideas/checks/  ideas/diag/
  code/run_all.sh  code/evaluate_holdout.py  code/make_numbers.py   results/   expected_output/
  paper/OUTLINE.md CLAIM_EVIDENCE.csv NUMBERS_USED.json draft/ sections/ figures/ latex/ 作者待办.md
  review/ R1_theory.md … R5_adversary.md meta.md codex_R1.md codex_R2.md response_table.md
  submit/   (built by civmat2 package)
```

## `civmat2 venue` — V0 topic map
```
civmat2 venue journals                                   # built-in key → ISSN table (verify!)
civmat2 venue fetch --journals CCR,CBM,MS --years 2023-2025 --out venue --mailto you@x.org [--source openalex] [--max N]
civmat2 venue classify --out venue [--sample 60 --seed 1]
civmat2 venue score --sample venue/sample_for_manual_check.csv
```
Outputs `venue/raw/<key>_<year>.jsonl`, `venue/classified.csv`, `venue/topic_map.md` (class share per journal; per-topic counts per year, growth = later-half share / earlier-half share, pure-ML share, median citations, top-cited DOIs), `venue/sample_for_manual_check.csv`. Title-only classification is approximate: fill `manual_class` for ≥50 rows and report the agreement rate from `score` next to every count. Topic and class lexicons are the `TOPICS`, `REVIEW`, `ML`, `COMP`, `EXP` regexes at the top of `tools/venue_profile.py`.

## `civmat2 depth` — V0 theory-depth tally
```
civmat2 depth venue/depth_corpus/text --out venue/theory_depth_tally
```
Per paper: pages, words, numbered equations, figures, tables, appendix, and counts of hold-out / baseline / metric / data-set / derivation / ML vocabulary → `<out>.csv` + `<out>.md` with P10/P50/P90 and a draft target band. Qualitative columns (`derivation_type`, `true_holdout`, `n_baselines_rerun`, `n_datasets`) are filled by reading.

## `civmat2 fetch` — V2 legal full text
```
civmat2 fetch DOI [DOI…] --out lit/pdfs --email you@x.org [--list] [--sleep 1]
civmat2 fetch --from-file dois.txt --out lit/pdfs
```
Order: Unpaywall (needs `--email`) → OpenAlex `best_oa_location`/`locations` → Semantic Scholar `openAccessPdf` → arXiv → CORE (`~/.config/core.key`) → Elsevier TDM (`~/.config/elsevier.key`, 10.1016/ only) → `NEED_FROM_USER.md`. Retries 429/5xx with back-off. Logs: `fetch_log.jsonl` (every attempt), `LICENSES.tsv` (every success). `--list` prints candidates without downloading.

## `civmat2 cards` — V3 literature cards
```
civmat2 cards lit/pdfs --cards lit/cards [--text lit/text] [--force] [--max-lines 40]
```
Needs `pdftotext` (poppler) or PyMuPDF. Produces one skeleton card per PDF with DOI guess, candidate equation lines `(N)` and metric lines (RMSE, MAE, R², CoV …) with page numbers. The agent completes it against the original and sets `status: FULLTEXT` or `ABSTRACT-ONLY=UNVERIFIED`.

## `civmat2 holdout` — V4/V6 frozen hold-out and one-shot evaluation
```
civmat2 holdout freeze  --data tidy.csv --group source [--id record_id] [--frac 0.3] --seed 1 --out HOLDOUT [--note "…"]
civmat2 holdout check   --data calibration.csv --split HOLDOUT
civmat2 holdout seal    --prereg PREREG.md --split HOLDOUT --code code/ [--out .]
civmat2 holdout evaluate --split HOLDOUT --prereg PREREG.md --sha PREREG.sha256 --manifest FROZEN_MANIFEST.json --cmd "python3 code/evaluate_holdout.py"
civmat2 holdout status  --split HOLDOUT
```
* `freeze` splits whole groups (sources / labs / references), writes `split.json` with the data and id-file sha256, makes the files read-only and refuses to overwrite an existing split. Needs unique ids and ≥2 groups (`--min-groups`).
* `check` fails with the overlapping ids.
* `seal` writes `PREREG.sha256` and `FROZEN_MANIFEST.json` (sha256 of every file under `--code` and of the split) and makes PREREG.md read-only.
* `evaluate` verifies the PREREG hash (and the manifest when given), refuses if `HOLDOUT_CONSUMED` exists, writes the marker **before** running (fail-closed), runs the command with `CIVMAT2_HOLDOUT_EVAL=1`, then records the outcome and appends to `evaluations.log`.
* Library: `from holdout_guard import load_calibration` (asserts zero overlap) and `load_holdout` (raises `PermissionError` unless run under `evaluate`).

## `civmat2 residuals` — V4 residual map and variance decomposition
```
civmat2 residuals data.csv --obs y --pred B0,M1 --source source --by age_d,w_b,size_mm --out results [--log] [--bins 4] [--boot 1000] [--seed 1] [--min-n 5]
```
Residual = pred − obs, or log10(pred/obs) with `--log`. Outputs `stratified_errors.csv` (per model × variable × quantile bin or category: n, sources, bias, MAE, RMSE, sign consistency across sources, Spearman trend), `variance_decomposition.json` (pooled and source-equal-weight RMSE, ICC(1) with between/within variances and a source-bootstrap 95 % CI, detectability verdict OK < 0.4 ≤ MARGINAL ≤ 0.6 < SWAMPED) and `residual_map.md`. Use calibration rows only.

## `civmat2 numcheck` — V8/V9 traceable numbers
```
civmat2 numcheck fill  draft.md --numbers paper/NUMBERS_USED.json [--out filled.md]
civmat2 numcheck check draft.md --numbers paper/NUMBERS_USED.json [--allow 0.3,95] [--allow-years] [--tol 0] [--report paper/NUMBER_CHECK.md]
```
`NUMBERS_USED.json` entries are bare numbers or `{"value", "fmt", "unit", "source"}`; keys starting with `_` are metadata. `fill` replaces `{{key}}` / `{{key:.2f}}` and errors on unknown keys. `check` ignores math, code, citations, figure/table/equation/section references, DOIs/URLs and (with `--allow-years`) years; every remaining numeral must equal a value after rounding to the digits shown. Exit 1 on any untraceable numeral or unresolved placeholder.

## `civmat2 refcheck` — V9/V11 citations
```
civmat2 refcheck refs.bib manuscript.md [--report paper/CITATION_CHECK.md] [--offline] [--require-doi] [--strict]
```
Resolves every DOI via Crossref → DataCite → doi.org, compares registered and .bib titles (token Jaccard, WARN < 0.5), caches results in `.refcheck_cache.json`. Exit 1 on NOT_FOUND / BAD_SYNTAX (and NETWORK_ERROR with `--strict`).

## `civmat2 style <key>` — V9/V10 style checker
```
civmat2 style ms-cemchem draft.md [--json] [--sections introduction,conclusions]
civmat2 style efm-sizeeffect draft.tex
```
Runs `style/<key>/style_check.py`; score = share of (section, metric) pairs inside the corpus P10–P90 band; the gate is 90 % of the corpus leave-one-out median (printed). Keys and corpus sizes are in `style/INDEX.md`.

## `civmat2 package` — V11 submission package
```
civmat2 package --ws <ws> --name <方向中文名> --journal <journal> [--out <dir>] [--no-zip]
```
Builds `<ws>/submit/` (01–07 + `00_作者参考_勿上传/`), `07_Supplementary_data_and_code.zip` (raw data only when `PROVENANCE.md` has no BY-NC / BY-ND / all-rights-reserved marker; otherwise provenance + download script only), `PACKAGE_MANIFEST_sha256.json`, the upload-order README with the missing-item checklist, and `<out>/投稿包_<name>_<date>.zip` + `.sha256`. Missing items are listed, never fabricated.

## `civmat2 codex C# N [LANE]` — Codex miner iteration
Renders `codex/PLAYBOOK.md` with the project root and interpreter, appends `codex/C#/brief.txt`, `feedback.txt`, `STATE.txt` and the lane brief, runs `codex exec` (model `CODEX_MODEL`, effort `CODEX_EFFORT`, timeout `CODEX_TIMEOUT`) in `codex/C#/iterN[_LANE]/` with the project added read-only, and writes `last.txt`, `codex.log`, `done.txt`. Without a `codex` binary it still writes `prompt.txt` and exits 127.

## `civmat2 init`, `civmat2 template`, `civmat2 test`
`init <ws>` scaffolds the layout above from `templates/`; `template <NAME>` prints one (`PREREG`, `FALSIFY`, `PROVENANCE`, `DIRECTION_CARD`, `BASELINES`, `G1_REPORT`, `IDEA`, `LIT_CARD`, `OUTLINE`, `CLAIM_EVIDENCE`, `NUMBERS_USED`, `response_table`, `作者待办`, `run_all`, `brief`, `feedback`, `STATE`, `STATUS`); `test` runs the offline smoke test.
