export const meta = {
  name: 'civmat2-sota',
  description: 'civmatflow v2 V2-V4: literature cards + baseline ledger, frozen hold-out, baseline reproduction with residual map, then an independent G1 audit',
  phases: [{ title: 'Literature', detail: 'legal full text, cards, BASELINES.md' }, { title: 'Reproduce', detail: 'freeze hold-out, implement baselines, residual map' }, { title: 'Audit', detail: 'civrev-experiment checks G1' }],
}

// args: { home, ws, direction, dois: [...], data_csv, group_col, id_col, seed, obs_col, pred_cols, by_cols }
const A = args || {}
const HOME = A.home || ''
const WS = A.ws || ''
const SKILLS = `${HOME}/skills`

const G1 = {
  type: 'object',
  properties: {
    g1: { type: 'string', enum: ['PASS', 'CONDITIONAL', 'FAIL'] },
    holdout_frozen: { type: 'boolean' },
    zero_overlap_asserted: { type: 'boolean' },
    reproduction_within_10pct: { type: 'boolean' },
    icc_between_source: { type: 'number' },
    detectability: { type: 'string', enum: ['OK', 'MARGINAL', 'SWAMPED', 'UNKNOWN'] },
    failure_regions: { type: 'array', items: { type: 'string' } },
    must_fix: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['g1', 'holdout_frozen', 'zero_overlap_asserted', 'reproduction_within_10pct', 'detectability', 'summary'],
}

phase('Literature')
const lit = await agent(
  `Direction ${A.direction} in workspace ${WS}. Read ${SKILLS}/civmat2-lit/SKILL.md. ` +
  `Fetch these DOIs through legal channels only (civmat2 fetch ... --out ${WS}/lit/pdfs): ${(A.dois || []).join(', ') || '(take them from DIRECTION.md and BASELINES.md)'}. ` +
  `Build cards with civmat2 cards and complete equations (with equation numbers) and metric values (with page/table) against the originals; ` +
  `spot-check 3 values per card. Update ${WS}/BASELINES.md (template ${HOME}/templates/BASELINES.md). List unreadable key competitors as BLOCKERS in your final reply.`,
  { label: 'lit:cards', phase: 'Literature', agentType: 'civmat-librarian' })

phase('Reproduce')
const repro = await agent(
  `Direction ${A.direction} in ${WS}. Read ${SKILLS}/civmat2-sota/SKILL.md and ${WS}/BASELINES.md. Literature summary: ${JSON.stringify(lit).slice(0, 2000)}.\n` +
  `Order is fixed: (1) civmat2 holdout freeze --data ${A.data_csv} --group ${A.group_col || 'source'} --id ${A.id_col || 'record_id'} --seed ${A.seed || 1} --out ${WS}/HOLDOUT; ` +
  `(2) every script loads data through holdout_guard.load_calibration and asserts zero overlap; ` +
  `(3) implement each baseline from the original equations (check official worked examples first); ` +
  `(4) reproduce the paper's reported error on the same subset and metric (±10 % or explain precisely; if the paper's selection cannot be rebuilt, use our frozen explicit selection and treat the paper's number as background); ` +
  `(5) civmat2 residuals ${A.data_csv} --obs ${A.obs_col || 'y'} --pred ${(A.pred_cols || []).join(',') || '<baseline columns>'} --source ${A.group_col || 'source'} --by ${(A.by_cols || []).join(',') || '<physical variables>'} --out ${WS}/results --log (calibration rows only). ` +
  `Write ${WS}/notes/G1_REPORT.md (template ${HOME}/templates/G1_REPORT.md). Compute ≤3 threads, nice 10.`,
  { label: 'repro:baselines', phase: 'Reproduce', agentType: 'civmat-theorist' })

phase('Audit')
const audit = await agent(
  `Independent G1 audit of ${WS}/notes/G1_REPORT.md for direction ${A.direction}. You only read files; do not trust the report's own claims. ` +
  `Check: HOLDOUT/split.json exists and is read-only; civmat2 holdout check passes for every calibration file; no script reads hold-out rows (grep for load_holdout / holdout_ids outside code/evaluate_holdout.py); ` +
  `the reproduction table matches the papers' values within 10 % or has a precise explanation; the residual map was computed on calibration rows only; ` +
  `results/variance_decomposition.json gives the ICC and the detectability verdict. Re-run one baseline yourself in a temporary directory. ` +
  `Write ${WS}/review/G1_audit.md and return the verdict object.`,
  { label: 'audit:G1', phase: 'Audit', agentType: 'civrev-experiment', schema: G1 })

log(`G1 ${audit.g1}: detectability ${audit.detectability}; failure regions: ${(audit.failure_regions || []).join('; ') || 'none listed'}`)
return { literature: lit, reproduction: repro, audit }
