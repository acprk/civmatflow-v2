export const meta = {
  name: 'civmat2-review',
  description: 'civmatflow v2 V10: five blind reviewer agents in parallel, then a meta-reviewer',
  phases: [{ title: 'Review' }, { title: 'Meta' }],
}

// args: { paper, supp, code, journal, style_key, review_dir }
const A = args || {}
const common = `Manuscript: ${A.paper}. Supplementary: ${A.supp || 'none'}. Code/data package: ${A.code || 'none'}. ` +
  `Target journal: ${A.journal}. Style key: ${A.style_key || 'none'} (see /home/luck/xzy/.claude/agents/style/INDEX.md). ` +
  `Review independently; do not read other review files or internal project notes. Write your report into ${A.review_dir}.`

const REVIEWERS = [
  { key: 'R1_theory', type: 'civrev-theory' },
  { key: 'R2_experiment', type: 'civrev-experiment' },
  { key: 'R3_domain', type: 'civrev-domain' },
  { key: 'R4_writing', type: 'civrev-writing' },
  { key: 'R5_adversary', type: 'civrev-adversary' },
]

phase('Review')
const reports = await parallel(REVIEWERS.map(r => () =>
  agent(`${common} File name: ${r.key}.md. Final reply: decision, confidence, and the list of Major issues only.`,
    { label: `review:${r.key}`, phase: 'Review', agentType: r.type })
))

phase('Meta')
const meta = await agent(
  `You are the handling editor. Read the five reports R1_theory.md … R5_adversary.md in ${A.review_dir}, ` +
  `verify every Major issue against the manuscript/package, and write ${A.review_dir}/meta.md with decision and must-fix list. ` +
  `Manuscript: ${A.paper}. Journal: ${A.journal}. Final reply: decision + must-fix list.`,
  { label: 'review:meta', phase: 'Meta', agentType: 'civrev-meta' })

return { reviewers: reports, meta }
