---
name: buyout-reroll-duplicate-bug
description: "Latent save-corrupting bug — buying out the shop then rerolling reproduced the day's offer set (salt collapsed to ''), minting duplicate instanceIds; fixed by folding coins+live instanceIds into the reroll salt"
metadata: 
  node_type: memory
  type: project
  originSessionId: d2f754bd-8615-4d94-82b0-739f8ebff536
---

**Found 2026-07-08 during the Fable economy pass.** The reroll salt was
`currentOffers.map(id).join('|')` — buy out the whole shop and the salt collapses to `''`, the
same salt as the day's opening generation, so the reroll deterministically reproduced identical
offerIds. Re-buying minted a **duplicate `instanceId` on the shelf → `GameStateSchema.parse`
fails → corrupted save**. Latent in v1 too (rich late-game players can buy out 3 offers + reroll);
exposed when an economy tweak made day-2 buyouts affordable to bots.

Fix (engine-wide, `src/sim/engine.ts` reroll case): salt now folds `coins`, the held item's
instanceId, every shelf instanceId, and the offer ids — any salt that could re-issue a bought
offer's id is structurally different from the salt that created it. Regression test:
`loopV2.test.ts` "never re-issues a bought offer id when the shop is bought out and rerolled"
(two full buyout+reroll cycles). Verified the operationalized OFF floor untouched: the pinned
determinism trajectories contain **zero rerolls** (checked by instrumenting `playRun`), so pin
`8d48e1c5a6ad14c9`, goldens, and fixtures all stay green.

**Scar → rule:** economy/number tuning changes bot affordability and thereby REACHES new code
paths — the [[fable-signoff-pass]] invariant fuzz across flag configs is the net that caught it.
Detection rule: every new resource mechanic gets a *degenerate-state probe* (empty shop, zero
coins, full shelf, buy-everything) in its brief; "deterministic without an RNG cursor" designs
must state what makes each regeneration's salt unique across ALL reachable states, not typical
ones.
