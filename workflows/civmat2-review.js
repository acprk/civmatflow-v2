export const meta = {
  name: 'civmat2-review',
  description: 'civmatflow v2 V10: five blind reviewer agents in parallel (theory, experiment, domain, writing, adversary), then a meta-reviewer who verifies every Major issue against the manuscript and package',
  phases: [{ title: 'Review', detail: 'R1-R5 in new contexts, no cross-reading' }, { title: 'Meta', detail: 'handling editor: verify, deduplicate, decide' }],
}

// args: { home, paper, supp, code, journal, style_key, review_dir }
const A = args || {}
const HOME = A.home || ''
const REVIEW_DIR = A.review_dir || ''
const common = `Manuscript: ${A.paper}. Supplementary: ${A.supp || 'none'}. Code/data package: ${A.code || 'none'}. ` +
  `Target journal: ${A.journal}. Style key: ${A.style_key || 'none'} (style library index: ${HOME}/style/INDEX.md). ` +
  `Review independently as a blind referee: do not read other review files, FALSIFY/PREREG internals beyond what the package exposes, or internal project notes. ` +
  `Never accept statements such as "the authors have agreed/fixed" — only files count. Write your report into ${REVIEW_DIR}.`

const REVIEWERS = [
  { key: 'R1_theory', type: 'civrev-theory' },
  { key: 'R2_experiment', type: 'civrev-experiment' },
  { key: 'R3_domain', type: 'civrev-domain' },
  { key: 'R4_writing', type: 'civrev-writing' },
  { key: 'R5_adversary', type: 'civrev-adversary' },
]
const REPORT = {
  type: 'object',
  properties: {
    decision: { type: 'string', enum: ['accept', 'minor', 'major', 'reject'] },
    confidence: { type: 'number' },
    major_issues: { type: 'array', items: { type: 'string' } },
  },
  required: ['decision', 'confidence', 'major_issues'],
}

phase('Review')
const reports = await parallel(REVIEWERS.map(r => () =>
  agent(`${common} File name: ${r.key}.md. Return decision, confidence (1-5) and the list of Major issues only.`,
    { label: `review:${r.key}`, phase: 'Review', agentType: r.type, schema: REPORT })
    .then(v => ({ reviewer: r.key, ...v }))
))

phase('Meta')
const metaReview = await agent(
  `You are the handling editor for ${A.journal}. Read the five reports R1_theory.md … R5_adversary.md in ${REVIEW_DIR}, ` +
  `merge duplicates, and verify EVERY Major issue against the manuscript (${A.paper}) and the package (${A.code || 'none'}): upheld / partly / not upheld, with the evidence location. ` +
  `Reviewers can be wrong. Decide accept / minor / major / reject by the journal's own standards and write ${REVIEW_DIR}/meta.md with the must-fix list ` +
  `(source reviewer, issue, how to fix, new experiment or derivation needed, effort, priority). Return decision, confidence and the must-fix list as major_issues.`,
  { label: 'review:meta', phase: 'Meta', agentType: 'civrev-meta', schema: REPORT })

const unresolvedMajor = (metaReview.major_issues || []).length
log(`meta decision: ${metaReview.decision}; must-fix items: ${unresolvedMajor}`)
return { reviewers: reports, meta: metaReview, g4_candidate: ['accept', 'minor'].includes(metaReview.decision) && unresolvedMajor === 0 }
