import { createHash } from 'node:crypto'

export const REVISION_CYCLE_VERSION = '1.0.0'
export const REVISION_CYCLE_SCHEMA = 'halveth.hypothesis-revision-cycle.v1'
const ID = /^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$/
const DIGEST = /^sha256:[a-f0-9]{64}$/
const OUTCOMES = new Set(['OPEN', 'INCONCLUSIVE', 'SUPPORTED_WITHIN_SCOPE', 'CONTRADICTED_WITHIN_SCOPE'])
const LABELS = ['Hypothese festhalten', 'Modelle unterscheiden', 'Beobachtung planen', 'Minimum-Evidenz vorab binden', 'Änderungsbedingung benennen', 'Ergebnis und offene Fragen festhalten']

function plain(value, depth = 0, seen = new Set()) {
  if (depth > 18) throw new TypeError('Zyklus überschreitet die maximale Datentiefe.')
  if (value === null || typeof value === 'boolean') return
  if (typeof value === 'string') {
    if (!value.isWellFormed()) throw new TypeError('Text muss wohlgeformtes Unicode enthalten.')
    return
  }
  if (typeof value === 'number' && Number.isFinite(value)) return
  if (typeof value !== 'object' || seen.has(value)) throw new TypeError('Nur endliche, azyklische JSON-Daten sind erlaubt.')
  seen.add(value)
  const array = Array.isArray(value)
  if (Object.getPrototypeOf(value) !== (array ? Array.prototype : Object.prototype)) throw new TypeError('Nur einfache JSON-Daten sind erlaubt.')
  if (array && (Reflect.ownKeys(value).length !== value.length + 1 || Object.keys(value).some((key, index) => key !== String(index)))) throw new TypeError('Array muss vollständig und ohne Zusatzfelder sein.')
  for (const key of Reflect.ownKeys(value)) {
    if (array && key === 'length') continue
    const d = Object.getOwnPropertyDescriptor(value, key)
    if (typeof key !== 'string' || !d.enumerable || !Object.hasOwn(d, 'value')) throw new TypeError('Verdeckte Felder und Getter sind nicht erlaubt.')
    plain(d.value, depth + 1, seen)
  }
  if (array && Object.keys(value).length !== value.length) throw new TypeError('Array muss vollständig belegt sein.')
  seen.delete(value)
}
function object(value, keys, at) {
  if (!value || Array.isArray(value) || typeof value !== 'object') throw new TypeError(`${at}: Objekt fehlt.`)
  if (Object.keys(value).sort().join('|') !== [...keys].sort().join('|')) throw new TypeError(`${at}: erwartet genau ${keys.join(', ')}.`)
  return value
}
function text(value, at, max = 6000) {
  if (typeof value !== 'string' || !value.trim() || value.length > max) throw new TypeError(`${at}: nichtleerer Text bis ${max} Zeichen erforderlich.`)
  return value
}
function id(value, at) {
  if (!ID.test(text(value, at, 96))) throw new TypeError(`${at}: ASCII-Kennung erforderlich.`)
}
function date(value, at, nullable = false) {
  if (nullable && value === null) return
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/.test(value) || !Number.isFinite(Date.parse(value))) throw new TypeError(`${at}: UTC-Zeitpunkt oder ausdrücklich erlaubtes null erforderlich.`)
  const iso = new Date(value).toISOString()
  if (iso.slice(0,19) !== value.slice(0,19)) throw new TypeError(`${at}: ungültiges Kalenderdatum.`)
}
function list(value, at, max = 64) {
  if (!Array.isArray(value) || value.length > max) throw new TypeError(`${at}: Array mit höchstens ${max} Einträgen erforderlich.`)
  return value
}
function strings(value, at, ids = false) {
  list(value, at).forEach((v, i) => ids ? id(v, `${at}[${i}]`) : text(v, `${at}[${i}]`))
  if (new Set(value).size !== value.length) throw new TypeError(`${at}: doppelte Einträge.`)
}
function canonical(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`
  return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`
}
function hash(value) { return `sha256:${createHash('sha256').update(canonical(value), 'utf8').digest('hex')}` }
function distinctText(value) { return value.normalize('NFKC').trim().toLowerCase().replace(/ß/gu, 'ss').replace(/\s+/gu, ' ') }
function uniqueIds(rows, at) {
  const ids = rows.map(row => row.id)
  if (new Set(ids).size !== ids.length) throw new TypeError(`${at}: Kennungen müssen eindeutig sein.`)
  return new Set(ids)
}

// The digest freezes the declared hypothesis, competing models and plan together.
// It does not independently attest who created them or when they existed.
export function revisionPlanDigest(cycle) {
  plain(cycle)
  return hash({ schema: REVISION_CYCLE_SCHEMA, version: REVISION_CYCLE_VERSION, id: cycle.id, hypothesis: cycle.hypothesis, models: cycle.models, plan: cycle.plan })
}

export function createRevisionCycle(idValue, statement, sourceRef, recordedAt) {
  id(idValue, 'id'); text(statement, 'statement'); text(sourceRef, 'sourceRef'); date(recordedAt, 'recordedAt')
  return { schema: REVISION_CYCLE_SCHEMA, version: REVISION_CYCLE_VERSION, id: idValue, recordedAt,
    hypothesis: { statement, sourceRef, eventTime: null }, models: [], plan: null, observations: [], result: null }
}

export function reviewHypothesisRevisionCycle(input) {
  plain(input)
  object(input, ['schema', 'version', 'id', 'recordedAt', 'hypothesis', 'models', 'plan', 'observations', 'result'], 'cycle')
  if (input.schema !== REVISION_CYCLE_SCHEMA || input.version !== REVISION_CYCLE_VERSION) throw new TypeError('Unbekannte Zyklusversion.')
  id(input.id, 'id'); date(input.recordedAt, 'recordedAt')
  const steps = LABELS.map((label, index) => ({ step: index + 1, label, state: 'BOUND', missing: [] }))
  const gap = (step, code, message) => { steps[step - 1].state = 'NEEDS_WORK'; steps[step - 1].missing.push({ code, message }) }
  const beforeSnapshot = (value, at) => { if (Date.parse(value) > Date.parse(input.recordedAt)) throw new TypeError(`${at}: liegt nach der Zyklusaufzeichnung.`) }
  if (input.hypothesis === null) gap(1, 'HYPOTHESIS_MISSING', 'Formuliere die Hypothese und binde ihre Quelle.')
  else {
    object(input.hypothesis, ['statement', 'sourceRef', 'eventTime'], 'hypothesis')
    text(input.hypothesis.statement, 'hypothesis.statement'); text(input.hypothesis.sourceRef, 'hypothesis.sourceRef')
    date(input.hypothesis.eventTime, 'hypothesis.eventTime', true)
    if (input.hypothesis.eventTime) beforeSnapshot(input.hypothesis.eventTime, 'hypothesis.eventTime')
  }
  list(input.models, 'models', 12).forEach((m, i) => {
    object(m, ['id', 'kind', 'explanation'], `models[${i}]`); id(m.id, 'model.id'); text(m.explanation, 'model.explanation')
    if (!['HYPOTHESIS_MODEL', 'COUNTERMODEL'].includes(m.kind)) throw new TypeError('model.kind ist unbekannt.')
  })
  const modelIds = uniqueIds(input.models, 'models')
  if (input.models.length < 2 || !input.models.some(m => m.kind === 'HYPOTHESIS_MODEL') || !input.models.some(m => m.kind === 'COUNTERMODEL')) gap(2, 'COMPETING_MODELS_MISSING', 'Binde mindestens ein Hypothesenmodell und ein Gegenmodell.')
  if (new Set(input.models.map(m => distinctText(m.explanation))).size !== input.models.length) gap(2, 'MODELS_TEXTUALLY_DUPLICATED', 'Gib den Modellen unterschiedliche Erklärungen; neue Namen allein unterscheiden sie nicht.')
  const plan = input.plan
  let criteria = []
  if (plan === null) {
    gap(3, 'TEST_IDEA_MISSING', 'Benenne eine Beobachtung, die die Modelle unterscheiden würde.')
    gap(4, 'MINIMUM_EVIDENCE_MISSING', 'Lege vor der Beobachtung fest, welche Evidenz mindestens erforderlich ist.')
    gap(5, 'REVISION_CONDITION_MISSING', 'Benenne, welcher Befund deine Einschätzung ändern würde.')
  } else {
    object(plan, ['boundAt', 'question', 'method', 'scope', 'predictions', 'minimumEvidence', 'changeMyMind'], 'plan')
    date(plan.boundAt, 'plan.boundAt'); beforeSnapshot(plan.boundAt, 'plan.boundAt')
    text(plan.question, 'plan.question'); text(plan.method, 'plan.method'); text(plan.scope, 'plan.scope')
    list(plan.predictions, 'plan.predictions', 12).forEach(p => {
      object(p, ['modelId', 'observable', 'targetTime'], 'prediction'); id(p.modelId, 'prediction.modelId'); text(p.observable, 'prediction.observable'); date(p.targetTime, 'prediction.targetTime', true)
      if (!modelIds.has(p.modelId)) throw new TypeError('Vorhersage referenziert unbekanntes Modell.')
      if (p.targetTime && Date.parse(p.targetTime) <= Date.parse(plan.boundAt)) throw new TypeError('Künftige Vorhersage muss nach der Planbindung liegen; historische Ereigniszeit gehört zur Quelle.')
    })
    const predictedIds = plan.predictions.map(p => p.modelId)
    if (new Set(predictedIds).size !== predictedIds.length) throw new TypeError('Nur eine gebundene Vorhersage je Modell.')
    if (modelIds.size < 2 || predictedIds.length !== modelIds.size) gap(3, 'MODEL_PREDICTION_MISSING', 'Binde für jedes Modell eine Vorhersage zur gleichen Prüffrage.')
    if (new Set(plan.predictions.map(p => distinctText(p.observable))).size < 2) gap(3, 'NO_DISCRIMINATING_PREDICTION', 'Die angegebenen Vorhersagen müssen sich in einer beobachtbaren Eigenschaft unterscheiden.')
    criteria = list(plan.minimumEvidence, 'plan.minimumEvidence')
    criteria.forEach(c => {
      object(c, ['id', 'criterion', 'minimumCount'], 'criterion'); id(c.id, 'criterion.id'); text(c.criterion, 'criterion.criterion')
      if (!Number.isInteger(c.minimumCount) || c.minimumCount < 1 || c.minimumCount > 256) throw new TypeError('minimumCount muss zwischen 1 und 256 liegen.')
    })
    const criterionIds = uniqueIds(criteria, 'minimumEvidence')
    if (!criteria.length) gap(4, 'MINIMUM_EVIDENCE_EMPTY', 'Definiere mindestens ein überprüfbares Mindestkriterium.')
    list(plan.changeMyMind, 'plan.changeMyMind', 12).forEach(c => {
      object(c, ['modelId', 'condition', 'criterionIds'], 'changeMyMind'); id(c.modelId, 'changeMyMind.modelId'); text(c.condition, 'changeMyMind.condition'); strings(c.criterionIds, 'changeMyMind.criterionIds', true)
      if (!modelIds.has(c.modelId) || c.criterionIds.some(x => !criterionIds.has(x))) throw new TypeError('Änderungsbedingung hat eine unbekannte Modell-/Kriterienreferenz.')
      if (!c.criterionIds.length) gap(5, 'UNBOUND_REVISION_CONDITION', 'Binde die Änderungsbedingung an mindestens ein Mindestkriterium.')
    })
    const revisionIds = plan.changeMyMind.map(c => c.modelId)
    if (new Set(revisionIds).size !== revisionIds.length) throw new TypeError('Doppelte Änderungsbedingung je Modell.')
    if (revisionIds.length !== modelIds.size || !revisionIds.length) gap(5, 'MODEL_REVISION_CONDITION_MISSING', 'Benenne für jedes Modell den Befund, der seine Bewertung ändern würde.')
  }
  const criterionIds = new Set(criteria.map(c => c.id))
  list(input.observations, 'observations', 256).forEach(o => {
    object(o, ['id', 'sourceRef', 'eventTime', 'observedAt', 'recordedAt', 'content', 'criterionIds'], 'observation')
    id(o.id, 'observation.id'); text(o.sourceRef, 'observation.sourceRef'); text(o.content, 'observation.content')
    date(o.eventTime, 'observation.eventTime', true); date(o.observedAt, 'observation.observedAt'); date(o.recordedAt, 'observation.recordedAt')
    strings(o.criterionIds, 'observation.criterionIds', true)
    if (o.criterionIds.some(x => !criterionIds.has(x))) throw new TypeError('Beobachtung referenziert unbekanntes Mindestkriterium.')
    if (Date.parse(o.observedAt) > Date.parse(o.recordedAt) || (o.eventTime && Date.parse(o.eventTime) > Date.parse(o.observedAt))) throw new TypeError('Ereignis-, Beobachtungs- und Aufzeichnungszeit sind nicht konsistent.')
    beforeSnapshot(o.recordedAt, 'observation.recordedAt')
    if (plan && Date.parse(plan.boundAt) >= Date.parse(o.observedAt)) gap(4, 'RETROSPECTIVE_CRITERIA', 'Kriterien wurden nicht vor dieser Beobachtung gebunden; führe sie als explorativ und beginne einen neuen vorab gebundenen Zyklus.')
  })
  const observationIds = uniqueIds(input.observations, 'observations')
  const planDigest = plan && input.hypothesis ? revisionPlanDigest(input) : null
  let evidenceCounts = criteria.map(c => ({ criterionId: c.id, required: c.minimumCount, referenced: 0 }))
  if (input.result === null) gap(6, 'RESULT_OPEN', 'Erfasse Beobachtungen und anschließend das Ergebnis mit offenem Rest und Wiederaufnahmebedingung.')
  else {
    const r = object(input.result, ['recordedAt', 'planDigest', 'outcome', 'modelId', 'observationIds', 'reasoning', 'remainingUnknowns', 'reopenTrigger'], 'result')
    date(r.recordedAt, 'result.recordedAt'); beforeSnapshot(r.recordedAt, 'result.recordedAt')
    if (!OUTCOMES.has(r.outcome)) throw new TypeError('Ergebnisstatus ist unbekannt; TRUE, SELECTED und EXECUTED sind keine Ergebniswerte.')
    if (r.modelId !== null && !modelIds.has(r.modelId)) throw new TypeError('Ergebnis referenziert unbekanntes Modell.')
    if (['SUPPORTED_WITHIN_SCOPE', 'CONTRADICTED_WITHIN_SCOPE'].includes(r.outcome) && r.modelId === null) gap(6, 'RESULT_MODEL_MISSING', 'Eine modellbezogene Bewertung braucht das konkrete Modell.')
    strings(r.observationIds, 'result.observationIds', true); text(r.reasoning, 'result.reasoning'); strings(r.remainingUnknowns, 'result.remainingUnknowns'); text(r.reopenTrigger, 'result.reopenTrigger')
    if (r.observationIds.some(x => !observationIds.has(x))) throw new TypeError('Ergebnis referenziert unbekannte Beobachtung.')
    if (!r.remainingUnknowns.length) gap(6, 'OPEN_REMAINDER_MISSING', 'Benenne den offenen Rest der begrenzten Prüfung.')
    if (!DIGEST.test(r.planDigest) || r.planDigest !== planDigest) gap(4, 'PLAN_DIGEST_MISMATCH', 'Das Ergebnis muss exakt den vorab gebundenen Hypothesen-, Modell- und Planstand referenzieren.')
    if (!plan || Date.parse(plan.boundAt) >= Date.parse(r.recordedAt)) gap(4, 'CRITERIA_NOT_BEFORE_RESULT', 'Der gebundene Plan muss vor der Ergebnisaufzeichnung liegen.')
    const used = input.observations.filter(o => r.observationIds.includes(o.id))
    if (used.some(o => Date.parse(o.recordedAt) > Date.parse(r.recordedAt))) throw new TypeError('Ergebnis verwendet erst später aufgezeichnete Beobachtung.')
    evidenceCounts = criteria.map(c => ({ criterionId: c.id, required: c.minimumCount, referenced: new Set(used.filter(o => o.criterionIds.includes(c.id)).map(o => `${o.sourceRef}\u0000${o.content}`)).size }))
    if (!used.length || evidenceCounts.some(c => c.referenced < c.required) || !criteria.length) gap(6, 'MINIMUM_EVIDENCE_NOT_REFERENCED', 'Die referenzierten Quellen decken die vorab festgelegte Mindestmenge nicht ab. Mehrere IDs derselben Quelle und Aussage zählen einmal.')
  }
  const missing = steps.flatMap(s => s.missing.map(m => ({ step: s.step, ...m })))
  return {
    schema: 'halveth.hypothesis-revision-receipt.v1', version: REVISION_CYCLE_VERSION,
    coreCompatibility: '3.5.1_ADDITIVE', cycleId: input.id, inputDigest: hash(input), planDigest,
    state: missing.length ? 'NEEDS_WORK' : 'DECLARED_CYCLE_STRUCTURALLY_BOUND', steps, missing,
    nextStep: steps.find(s => s.missing.length)?.label ?? 'Quelleninhalt und unterscheidende Aussage fachlich prüfen.',
    evidenceCounts, declaredResult: input.result?.outcome ?? 'OPEN',
    timeBinding: 'CALLER_DECLARED_ORDER_NOT_INDEPENDENT_PREREGISTRATION_PROOF',
    modelDifference: 'TEXTUAL_DISTINCTNESS_CHECKED_SEMANTIC_DISCRIMINATION_REQUIRES_REVIEW',
    evidenceBinding: 'REFERENCES_AND_COUNTS_ONLY_SOURCE_CONTENT_NOT_FETCHED',
    claimCeiling: 'LOCAL_STRUCTURE_AND_NEXT_STEP_ONLY',
    authorityEffect: 'NONE', externalTestsExecuted: false, hypothesisConfirmed: false
  }
}
