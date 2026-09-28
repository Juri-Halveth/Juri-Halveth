import { reviewHypothesisRevisionCycle } from './hypothesis-revision-cycle.mjs'

// The host supplies and enforces its request gate, bounded JSON reader and reply
// function. This module starts no listener and performs no external request.
export async function handleHypothesisRevisionRequest(request, response, { requireLocalAgentRequest, readJsonBody, jsonResponse }) {
  requireLocalAgentRequest(request)
  try {
    return jsonResponse(response, 200, reviewHypothesisRevisionCycle(await readJsonBody(request)))
  } catch (error) {
    if (error instanceof TypeError || error instanceof RangeError) error.statusCode = 400
    throw error
  }
}
