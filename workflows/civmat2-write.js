export const meta = {
  name: 'civmat2-write',
  description: 'civmatflow v2 V8-V9: section-wise drafting by the journal×field writer agent from the claim list and traceable numbers, then style check and a writing review',
  phases: [{ title: 'Draft', detail: 'one writer call per section' }, { title: 'Polish', detail: 'style_check + civrev-writing' }],
}

// args: { home, ws, style_key, writer_agent, sections: ['abstract','introduction',...], journal }
const A = args || {}
const HOME = A.home || ''
const WS = A.ws || ''
const KEY = A.style_key || ''
const WRITER = A.writer_agent || (KEY ? `${KEY}-writer` : '')
const SECTIONS = A.sections && A.sections.length ? A.sections : ['abstract', 'introduction', 'methods', 'results', 'discussion', 'conclusions']

phase('Draft')
const drafts = await parallel(SECTIONS.map(s => () =>
  agent(
    `Write / rewrite the "${s}" section of the manuscript in ${WS}/paper. Inputs: ${WS}/paper/OUTLINE.md, ${WS}/paper/CLAIM_EVIDENCE.csv (claims and the hedging that must be kept), ` +
    `the author's draft ${WS}/paper/draft/${s}.md (facts and {{number}} placeholders; do not replace placeholders with literal numbers), and the style guide ${HOME}/style/${KEY}/STYLE.md + phrasebank.md. ` +
    `Change expression only: no new facts, numbers, citations or claims; keep every placeholder and every hedge; mark missing information as [TODO: ...]. ` +
    `Write the result to ${WS}/paper/sections/${s}.md and list the changes and every [TODO] in your final reply.`,
    { label: `draft:${s}`, phase: 'Draft', agentType: WRITER })))

phase('Polish')
const review = await agent(
  `Target journal ${A.journal || KEY}; style key ${KEY} (STYLE.md, phrasebank.md and style_check.py under ${HOME}/style/${KEY}/). ` +
  `Assemble ${WS}/paper/sections/*.md in OUTLINE order into ${WS}/paper/manuscript_draft.md, fill numbers with ` +
  `"civmat2 numcheck fill ${WS}/paper/manuscript_draft.md --numbers ${WS}/paper/NUMBERS_USED.json", run "civmat2 style ${KEY} ${WS}/paper/manuscript_draft.md" and ` +
  `"civmat2 numcheck check ${WS}/paper/manuscript_draft.md --numbers ${WS}/paper/NUMBERS_USED.json --allow-years --report ${WS}/paper/NUMBER_CHECK.md". ` +
  `Then review as R4: structure vs the corpus bands, rhetorical moves, claim–evidence alignment against CLAIM_EVIDENCE.csv, exaggeration, AI-flavoured lexicon, captions. ` +
  `Write ${WS}/review/R4_writing_draft.md with sentence-level suggestions (expression only). Final reply: style score, number-check result, and the list of Major issues.`,
  { label: 'polish:R4', phase: 'Polish', agentType: 'civrev-writing' })

return { drafts, review }
