---
name: spike-scenarios-need-rules-paced-drops
description: "A perf \"worst case\" measured cheaper than the ramp because per-step respawns kept bodies airborne — pace synthetic load from the real rules"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:09:20.916Z
---

The v0.2 spike's "worst case @120 bodies" scenario initially measured **cheaper** than the ramp's
120-body stage. Cause: "continuous drops" was implemented as retire-oldest-and-respawn on every
fixed step (60 drops/second), so bodies spent their lives in free fall instead of resting in a
contact-heavy pile — and contacts, not bodies, are what the solver pays for.

**Why:** a synthetic load scenario paced by an invented number can be *easier* than real play while
looking adversarial on paper. The give-away was the ordering anomaly (worst case < ramp); without
noticing that, the gate would have been judged against a scenario that under-loads the solver.

**How to apply:**
- Pace synthetic load from the real rules constant (here `board.dropCooldownSeconds` = 0.4 s), never
  per-step or a hand-picked interval.
- Sanity-check scenario results against each other: if the scenario labelled "worst" isn't the most
  expensive, the scenario is wrong before the engine is.
- Still true after the fix: a **settled-but-awake** pile (ramp final stage) is the most expensive
  state measured — disturbing the stack scatters bodies and *reduces* contact count. Judge the gate
  against the worst stage across all scenarios, not only the one named "worst case".

Also derived rather than guessed: board composition. 120 bodies only fit a ~5.9 × 12 chamber if
they are almost all tier-1/2 (area budget), so `resolveComposition()` picks the mix from chamber
area and reports the achieved fill fraction in the JSON.
