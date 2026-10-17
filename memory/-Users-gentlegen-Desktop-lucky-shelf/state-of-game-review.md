---
name: state-of-game-review
description: "2026-07-08 whole-game strategic review — verdict + 4 promoted gaps (unlock ladder, playtest, ghost dailies, spectacle-without-swing)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4803b0d5-f969-42f2-adae-650b535f229a
---

2026-07-08 whole-game review (human-requested, recorded in `docs/state-of-game-review-2026-07-08.md`,
wired into STATUS §3). Verdict: **structurally excellent, experientially unproven** — infra/tuning
ahead of most shipped indies, but shipping default is still pre-v2; everything waits on the device
feel-gate.

Promoted gaps, priority order (none block the day-2-starter + feel-gate critical path):
- **P1 Unlock ladder** — no between-run meta-progression anywhere in the plan; all 36 items
  available from run 1. Needs a lane-A brief (`UNLOCK_LADDER_ENABLED`, additive save field,
  wipe-check first, pin untouched). Also fixes content-volume *perception* cheaply.
- **P2 Real-playtest milestone** — TestFlight ~10×3 days after flags graduate; all balance evidence
  is bot-derived and bots understate intent mechanics ([[todays-order-demand]] scar).
- **P3 Daily seed + ghosts** — S-3 promoted from the moat ledger; flagship post-graduation feature
  on the trace moat.
- **P4 Spectacle without swing** — principle for all future feel work: economic bands stay gentle
  ([[balance-target-bands]] are Fable's), top cascade tier gets the full juice budget.

Deliberately NOT promoted (post-launch): raw item-pool growth, customers-as-characters,
beautiful-shelf décor. **Why:** the honest weakness vs Balatro/LbaL is retention spine
(meta-progression + real-player evidence), not more intra-run depth. **How to apply:** at each
milestone review check P1 brief / P2 schedule / P3 sizing; the tune-vs-graduating-flag-SET scar
([[fable-signoff-pass]]) applies to the unlock ladder too.
