---
name: parity-covers-order-not-payloads
description: driver-parity proves rng call order only — event payload fields need their own checks; also v1 reference repo drifts on disk
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-08T23:55:54.787Z
---

Two review-system learnings from Step 2 (2026-08-08):

1. **Parity fingerprints call order, not payloads.** `scripts/driver-parity.js` proving wins/endings/steps identical to the test does NOT validate event payload fields — Opus shipped `G.lastVote.deputy` (engine stores `nominee`) and parity stayed green; the log read "Gita and null take office". **Why:** parity compares aggregate outcomes, which only depend on the rng-consuming call order. **How to apply:** any consumer of `ev.detail`/payload fields needs its own assertion (e.g. a snapshot test of one match's serialized log, or null-field lint on events); add this to Step 6 briefs when UI starts rendering event text.

2. **Scripted review APIs can bypass the very seam that breaks** (Step 3, 2026-08-08): the walk workbench's A/D keys were swapped (camera right-vector sign error) while 50/50 controller tests AND my scripted `setInput` review scenarios stayed green — both feed the sim direct vectors, so the keyboard→camera basis was the one untested seam, and the owner's hands caught it. **How to apply:** for any input/feel feature, the review must include at least one end-to-end check through the real input path (a real keypress moving the avatar in the expected screen direction), and the owner feel gate is structural, not a formality. Basis sanity: three.js screen-right = forward × up.

3. **Advertised options must round-trip** (Step 4, 2026-08-09): `waitingFor().options` said `[0,1]` but `submit(options[0])` threw — the UI worked via a different internal shape, so only scripted driving exposed it. Also: an `auto()` helper that silently latched autopilot made an alive human answer once per match. **How to apply:** any API that advertises legal actions gets a contract test asserting every advertised value is accepted verbatim, plus accounting checks (decisions asked == decisions owed, e.g. ballots == elections survived). Helpers named `step`/`auto` must never do more than their name.

4. **The v1 reference repo drifts.** v1's `ai.js` was edited on disk at 21:06 on 2026-08-08 by something outside our sessions (chatter-only polish; adopted into v2 as commit 2f5380d after proving tests unchanged). **How to apply:** never state "byte-identical to v1" as a standing invariant — pin comparisons to what v1 looked like at port time, and diff against v1 fresh at each review, treating drift as a decision point (adopt or document), not an error. Related: [[rng-stream-discipline]] — the new chatter dedupe loop draws extra rng, reinforcing that chatter needs a derived RNG before UI use.
