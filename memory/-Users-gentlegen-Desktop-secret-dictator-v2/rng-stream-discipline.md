---
name: rng-stream-discipline
description: "All chance (deck, roles, bot decisions, chatter) draws from one seeded G.rng() stream — driver call order defines the match"
metadata: 
  node_type: memory
  type: project
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-08T19:00:28.404Z
---

In the v2 engine (ported byte-identical from v1 on 2026-08-08, see [[v1-exists-and-is-reusable]]), every random decision — deck shuffle, role deal, bot choices in ai.js, and `AI.chatter` — consumes the single seeded `G.rng()` stream on the game object. A seed therefore reproduces a match only if the driver calls the AI hooks in the exact order `test/engine.test.js` uses.

**Why:** `AI.chatter` draws from the same stream but is called by neither the test nor `scripts/simulate.js`. Wiring chatter (or any new rng consumer) into the 3D presentation will silently change every downstream draw and break seed-reproducibility against the headless harnesses.

**How to apply:** any future presentation-side driver must either mirror the test's call order exactly, or chatter/presentation randomness must be given its own derived RNG (e.g. a second `makeRng(seed ^ const)`), never `G.rng()`. Flag this at review time on Step 2+ whenever presentation code touches the engine. Documented in v2 `docs/step-01.md` "Notes for later steps".
