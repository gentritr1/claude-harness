---
name: front-window-spotlight
description: "Prototype daily spotlight-slot mechanic added to fix \"too short / no mechanic\" device feedback; flagged, awaiting device feel-gate."
metadata: 
  node_type: memory
  type: project
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

On 2026-07-07 the owner played B-M3 on device and judged the whole loop shallow ("too short / no mechanic / straightforward") — endorsed all four emptiness axes (placement no stakes, nothing to chase mid-run, too few choices/day, passive scoring). Root cause from code: a delivery day = draft 1-of-3 + drop into ~12 slots (3 free moves, free sell → nothing committal) + watch a deterministic cascade. Adjacency depth only bites once the shelf is dense, which is late — most runs die at rent cycle 7 before it blooms.

**Fix shipped as a flagged prototype: "Front Window" spotlight.** One deterministic slot/day (`rngFor(seed,'spotlight',day).pick(rowMajorSlots)`) multiplies whatever item's total lands there (×3). Chosen because one lever hits all four axes at once, and it's the lowest engine risk (a mult at itemTotal, like the existing row auras).

- Flag: `SPOTLIGHT_ENABLED` / `SPOTLIGHT_MULT` in [economy.ts](src/sim/economy.ts). OFF restores the pre-prototype loop byte-for-byte.
- `spotlight?: Slot | null` is an **additive optional** field on GameState/GameStateSchema — deliberately did NOT bump ContractSchemaVersion, so v1 saves keep loading and M0 golden fixtures (which omit it) reproduce identical traces. Scoring only boosts when `state.spotlight` is present, emitted as a `ruleFire` mult with `ruleId:'spotlight'` (no new trace-event kind; cascade renders it with zero changes).
- Visual: golden ring + "✨ WINDOW ×N" tag on the slot in [ShelfScene.tsx](src/juice/ShelfScene.tsx) (plain RN Views + Reanimated, not Skia → would render on web too).

**Verified:** tsc clean; 59/59 tests incl. golden traces (moat) unchanged; replay-determinism holds. Same-machine fuzz A/B (100 runs): greedy/combo median deepest rent 7→8, bestDay median 77→~113 (+45%), combo bestDay max 205→427 (+108%). Bots understate it — they don't steer their best item into the window, a human should push deeper.

**UNVERIFIED (the whole point):** device feel — does the window read as "the storefront," does the ×3 cascade pop land, does placement now feel like a decision, is ×3 the right magnitude, is 1 window/day enough. Web preview cannot prove this (see [[lane-b-web-verification]]). Owner holds the feel-gate. Known cosmetic: spotlight ruleFire is a zero-length self-arrow in the cascade — refine only after feel is accepted.

**Gotcha:** adding a per-day RNG derivation shifts the pinned state hash in [determinism.test.ts](src/sim/determinism.test.ts) — that's the intended "conscious update" gate, not a regression (replay-equality still passes). Updated 768bffb…→f5301201….
