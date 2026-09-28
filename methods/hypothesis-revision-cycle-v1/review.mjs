import { readFile, stat } from 'node:fs/promises'
import { createRevisionCycle, reviewHypothesisRevisionCycle } from './hypothesis-revision-cycle.mjs'

const args = process.argv.slice(2)
try {
  if (args.length === 1 && args[0] === '--template') {
    console.log(JSON.stringify(createRevisionCycle('IDEA-1', 'Hier die eigene Hypothese eintragen.', 'USER:OWN_IDEA', new Date().toISOString()), null, 2))
  } else if (args.length === 1 && !args[0].startsWith('--')) {
    if ((await stat(args[0])).size > 1_000_000) throw new Error('Eingabedatei überschreitet 1 MB.')
    const bytes = await readFile(args[0])
    if (bytes.length > 1_000_000) throw new Error('Eingabedatei überschreitet 1 MB.')
    const input = JSON.parse(new TextDecoder('utf-8', { fatal:true }).decode(bytes))
    console.log(JSON.stringify(reviewHypothesisRevisionCycle(input), null, 2))
  } else {
    throw new Error('Aufruf: node review.mjs --template | <zyklus.json>')
  }
} catch (error) {
  console.error(error.message)
  process.exitCode = 1
}
