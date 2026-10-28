export const meta = {
  name: 'civmat2-direction',
  description: 'civmatflow v2 V1: per-candidate scoop scan, data gate and detectability check, then adversarial ranking',
  phases: [{ title: 'Gate' }, { title: 'Rank' }],
}

// args: { candidates: [{key, brief}], out_dir }
const A = args || {}
const VERDICT = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    g0_data: { type: 'string', enum: ['PASS', 'PARTIAL', 'FAIL'] },
    g05_scoop: { type: 'string', enum: ['CLEAR', 'UNRESOLVED', 'SCOOPED'] },
    competitor_fulltext_readable: { type: 'boolean' },
    detectability: { type: 'string', enum: ['WITHIN_SOURCE', 'SIMULATION', 'SWAMPED', 'UNKNOWN'] },
    closest_prior: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['key', 'g0_data', 'g05_scoop', 'competitor_fulltext_readable', 'detectability', 'summary'],
}

const gated = await pipeline(A.candidates || [],
  c => agent(
    `Candidate ${c.key}: ${c.brief}\nRun civmatflow v2 V1 gates (see /home/luck/xzy/0970project/civmatflow2/skills/civmat2-direction/SKILL.md): ` +
    `download/licence check of the named public data into ${A.out_dir}/${c.key}/, 24-month scoop scan with full-text reading of the closest works, ` +
    `and a detectability estimate. Return the verdict object.`,
    { label: `gate:${c.key}`, phase: 'Gate', agentType: 'civmat-scout', schema: VERDICT }),
  (v, c) => v && agent(
    `Try to kill candidate ${c.key} (${c.brief}). Prior verdict: ${JSON.stringify(v)}. Look for prior art the scout missed, ` +
    `non-identifiability, and whether inter-source scatter swamps any mechanistic gain. Return the corrected verdict object.`,
    { label: `kill:${c.key}`, phase: 'Gate', agentType: 'civrev-adversary', schema: VERDICT }))

const alive = gated.filter(Boolean).filter(v => v.g05_scoop !== 'SCOOPED' && v.g0_data !== 'FAIL' && v.detectability !== 'SWAMPED')
log(`${alive.length}/${(A.candidates || []).length} candidates survive the gates`)
return { all: gated.filter(Boolean), alive }
