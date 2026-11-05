export const meta = {
  name: 'civmat2-idea',
  description: 'civmatflow v2 V5/V7: parallel mechanism routes + recalibration control, adversarial kill pass on FALSIFY.md (stage ideate); or independent falsification of a finished hold-out result (stage falsify)',
  phases: [{ title: 'Theorize', detail: 'competing mechanism routes' }, { title: 'Kill', detail: 'adversary attacks each FALSIFY.md' }, { title: 'Falsify', detail: 'V7: adversary + experiment reviewer on the result' }],
}

// args: { home, ws, direction, stage: 'ideate'|'falsify', routes: [{slug, hint}], result_dir }
const A = args || {}
const HOME = A.home || ''
const WS = A.ws || ''
const SKILL = `${HOME}/skills/civmat2-idea/SKILL.md`

const IDEA = {
  type: 'object',
  properties: {
    slug: { type: 'string' },
    status: { type: 'string', enum: ['ALIVE', 'KILLED', 'NEEDS_DATA'] },
    mechanism: { type: 'string' },
    n_params_vs_baseline: { type: 'string' },
    identifiable: { type: 'boolean' },
    novelty_checked: { type: 'boolean' },
    prior_art: { type: 'array', items: { type: 'string' } },
    testable_predictions: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['slug', 'status', 'mechanism', 'identifiable', 'novelty_checked', 'summary'],
}
const VERDICT = {
  type: 'object',
  properties: {
    severity: { type: 'string', enum: ['NONE', 'MINOR', 'MAJOR', 'FATAL'] },
    issues: { type: 'array', items: { type: 'string' } },
    would_change_verdict_if: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['severity', 'issues', 'summary'],
}

if ((A.stage || 'ideate') === 'ideate') {
  phase('Theorize')
  const routes = (A.routes && A.routes.length ? A.routes : [{ slug: 'route_a', hint: '' }, { slug: 'route_b', hint: '' }])
  const control = { slug: 'recalibration_control', hint: 'pure re-calibration of the baseline parameters on the calibration set — no new physics. This is the control every mechanism must beat.' }
  const ideas = await parallel([...routes, control].map(r => () =>
    agent(
      `Direction ${A.direction}, workspace ${WS}, idea slug ${r.slug}. Read ${SKILL}, ${WS}/notes/G1_REPORT.md and ${WS}/results/residual_map.md. ` +
      `Route hint: ${r.hint || 'none; choose a physically distinct mechanism from the other routes'}. ` +
      `Steps: residual diagnosis on calibration rows only → ≤3 physical explanations with the functional form each predicts → equations (≤ baseline + 2 parameters, 4–10 derivation steps in the main text, long derivations to an appendix) → ` +
      `sympy self-checks in ${WS}/ideas/checks/ (dimensions, limits, reduction to baseline, monotonicity, dissipation) → identifiability BEFORE fitting (profile likelihood / Fisher) → novelty check against the 3 closest papers (full text). ` +
      `Write ${WS}/ideas/${r.slug}.md (template ${HOME}/templates/IDEA.md) and ${WS}/ideas/${r.slug}.FALSIFY.md (template ${HOME}/templates/FALSIFY.md). Never touch the hold-out. Return the idea object.`,
      { label: `idea:${r.slug}`, phase: 'Theorize', agentType: 'civmat-theorist', schema: IDEA })))

  phase('Kill')
  const attacked = await parallel(ideas.filter(i => i && i.status === 'ALIVE').map(i => () =>
    agent(
      `Attack idea ${i.slug} in ${WS}: read ${WS}/ideas/${i.slug}.md and ${WS}/ideas/${i.slug}.FALSIFY.md. Idea object: ${JSON.stringify(i)}. ` +
      `Try at least 5 routes (prior art under different terminology, trivial explanation by the recalibration control ${WS}/ideas/recalibration_control.md, leakage, counter-examples in the calibration data, robustness to seeds/settings, inter-source scatter). ` +
      `Run your own scripts (calibration rows only; never the hold-out). Record every attack and its outcome in the FALSIFY.md attack table and return the verdict object.`,
      { label: `kill:${i.slug}`, phase: 'Kill', agentType: 'civrev-adversary', schema: VERDICT })
      .then(v => ({ ...i, attack: v }))))
  const survivors = attacked.filter(i => i.attack && i.attack.severity !== 'FATAL' && i.slug !== 'recalibration_control')
  log(`G2: ${survivors.length} idea(s) survive the kill pass: ${survivors.map(i => i.slug).join(', ') || 'none'}`)
  return { ideas, attacked, survivors }
}

phase('Falsify')
const RES = A.result_dir || `${WS}/results`
const [adv, exp] = await parallel([
  () => agent(
    `V7 independent falsification (new context). Direction ${A.direction}, workspace ${WS}, results in ${RES}, pre-registration ${WS}/PREREG.md (+ PREREG.sha256, FROZEN_MANIFEST.json). ` +
    `Default stance: the result is wrong. Check novelty, trivial explanations (recalibration control), leakage (civmat2 holdout status/check; grep for hold-out access), robustness, in-sample claims disguised as out-of-sample, and whether parity is reported as a win. ` +
    `Write ${WS}/review/V7_adversary.md and return the verdict object.`,
    { label: 'falsify:adversary', phase: 'Falsify', agentType: 'civrev-adversary', schema: VERDICT }),
  () => agent(
    `V7 reproduction audit (new context). Direction ${A.direction}, workspace ${WS}. Copy code/ and data/ to a temporary directory and run code/run_all.sh (≤3 threads); ` +
    `compare every number in ${RES} and ${WS}/paper/NUMBERS_USED.json (if present); verify PREREG sha256 vs PREREG.sha256 and the FROZEN_MANIFEST; confirm HOLDOUT_CONSUMED records exactly one evaluation; ` +
    `check that the pre-registered win criteria were applied verbatim. Write ${WS}/review/V7_experiment.md and return the verdict object.`,
    { label: 'falsify:experiment', phase: 'Falsify', agentType: 'civrev-experiment', schema: VERDICT }),
])
const worst = ['NONE', 'MINOR', 'MAJOR', 'FATAL'].indexOf(adv.severity) > ['NONE', 'MINOR', 'MAJOR', 'FATAL'].indexOf(exp.severity) ? adv.severity : exp.severity
log(`V7 verdict: ${worst} (adversary ${adv.severity}, experiment ${exp.severity})`)
return { adversary: adv, experiment: exp, verdict: worst, proceed_to_writing: worst === 'NONE' || worst === 'MINOR' }
