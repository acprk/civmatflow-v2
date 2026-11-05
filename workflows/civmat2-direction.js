export const meta = {
  name: 'civmat2-direction',
  description: 'civmatflow v2 V1: per-candidate data gate (G0), scoop scan (G0.5) and detectability check by civmat-scout, then an adversarial kill pass; survivors are ranked',
  phases: [{ title: 'Gate', detail: 'G0 data/licence/compute, G0.5 scoop scan, detectability' }, { title: 'Rank', detail: 'adversarial kill pass and ranking' }],
}

// args: { home, project, candidates: [{key, brief}], out_dir }
//   home     civmatflow v2 repo root (CIVMAT2_HOME); skills live in <home>/skills
//   project  research workspace root (CIVMAT2_PROJECT); data goes to <project>/data/raw/<key>/
const A = args || {}
const HOME = A.home || ''
const PROJECT = A.project || ''
const OUT = A.out_dir || `${PROJECT}/directions`
const SKILL = `${HOME}/skills/civmat2-direction/SKILL.md`

const VERDICT = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    g0_data: { type: 'string', enum: ['PASS', 'PARTIAL', 'FAIL'] },
    g05_scoop: { type: 'string', enum: ['CLEAR', 'UNRESOLVED', 'SCOOPED'] },
    competitor_fulltext_readable: { type: 'boolean' },
    detectability: { type: 'string', enum: ['WITHIN_SOURCE', 'SIMULATION', 'SWAMPED', 'UNKNOWN'] },
    closest_prior: { type: 'array', items: { type: 'string' } },
    kill_list: { type: 'array', items: { type: 'string' } },
    score: { type: 'number', description: '0-5 overall (civmat2-direction scoring dimensions)' },
    summary: { type: 'string' },
  },
  required: ['key', 'g0_data', 'g05_scoop', 'competitor_fulltext_readable', 'detectability', 'summary'],
}

phase('Gate')
const gated = await pipeline(A.candidates || [],
  c => agent(
    `Candidate ${c.key}: ${c.brief}\n` +
    `Run the civmatflow v2 V1 gates (read ${SKILL} first and ${HOME}/skills/civmat2/SKILL.md for the 15 lessons). ` +
    `1) G0: actually download the named public data into ${PROJECT}/data/raw/${c.key}/ with a PROVENANCE.md (template: ${HOME}/templates/PROVENANCE.md), sha256 and licence; ` +
    `2) G0.5: 24-month scoop scan (journals, preprints, Zenodo/figshare/MDPI, cited-by, authors' later work) and read the closest works in full text through legal channels only; ` +
    `3) detectability: estimate between-source vs within-source scatter (civmat2 residuals if a baseline prediction exists, otherwise from the literature) and whether within-source contrasts or the simulation route exist. ` +
    `Write the direction card to ${OUT}/${c.key}/DIRECTION.md (template ${HOME}/templates/DIRECTION_CARD.md) and return the verdict object.`,
    { label: `gate:${c.key}`, phase: 'Gate', agentType: 'civmat-scout', schema: VERDICT }),
  (v, c) => v && agent(
    `Try to kill candidate ${c.key} (${c.brief}). Scout verdict: ${JSON.stringify(v)}. Card: ${OUT}/${c.key}/DIRECTION.md. ` +
    `Look for prior art the scout missed (change terminology, check cited-by and the authors' later papers), parameter non-identifiability, ` +
    `whether inter-source scatter swamps any mechanistic gain, and whether the key competitor is unreadable (paywalled, no OA) — which is itself a reason to drop. ` +
    `Append your attack record to the card and return the corrected verdict object (be explicit when you downgrade the scout).`,
    { label: `kill:${c.key}`, phase: 'Rank', agentType: 'civrev-adversary', schema: VERDICT }))

phase('Rank')
const all = gated.filter(Boolean)
const alive = all
  .filter(v => v.g05_scoop !== 'SCOOPED' && v.g0_data !== 'FAIL' && v.detectability !== 'SWAMPED')
  .sort((a, b) => (b.score || 0) - (a.score || 0))
log(`${alive.length}/${(A.candidates || []).length} candidates survive the gates: ${alive.map(v => v.key).join(', ') || 'none'}`)
return { all, alive, primary: alive[0] || null, backup: alive[1] || null }
