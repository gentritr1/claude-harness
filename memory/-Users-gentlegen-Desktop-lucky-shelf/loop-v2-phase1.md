---
name: loop-v2-phase1
description: "Loop Redesign v2 Phase 1 (daily buy-multiple shop) exists behind LOOP_V2_ENABLED, orchestrator-APPROVED, pending device feel-gate + Fable sign-off."
metadata: 
  node_type: memory
  type: project
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

The device play-test verdict (too linear / "1 item a day") triggered a full loop redesign — spec at [docs/loop-redesign-v2-spec.md](docs/loop-redesign-v2-spec.md), phased. Split: **Codex = Lane A logic, Opus = Lane B UI** (see [[reviewer-workflow-opus-split]]).

**Phase 1 (decision density) — LANDED behind a flag, 2026-07-07.** Codex built it; I (orchestrator) reviewed → APPROVE.
- Flag `LOOP_V2_ENABLED` in [economy.ts](src/sim/economy.ts) (default OFF; also honors `LOOP_V2_ENABLED=1` env). OFF = today's loop byte-identical (determinism pin 8d48… unchanged, goldens green).
- v2 flow in [engine.ts](src/sim/engine.ts): day-1 free 3-offer *starter* (delivery) → placing it routes into a **paid buy-multiple shop every day** by reusing the existing `restock` phase (`isLoopV2StarterPlacement` + the openShop routing branch). Starting coins 8; `dailyShopCost` curve. No new contract fields — reuses restock.
- **Verified (executed):** fuzz A/B — day-3 board occupancy 3→6, buys/run 3→11; deepest-rent survival unchanged at 8 (density up, not trivialized). tsc clean, 71 tests.
- **Latent footgun — FIXED `ab83c8d` (2026-07-08).** `loopV2Enabled()` read `process.env` at several call sites → a mid-run flag flip (hot reload / fuzz) could make a half-v1/half-v2 run. Fix: snapshot the flag onto `GameState.loopV2?` (additive optional, only set `true` under v2 → OFF path undefined → determinism pin `8d48…` byte-identical) once in `createRun`; all dispatch reads go through `runLoopV2(state)` (strict `=== true`, so v1/older saves stay v1). `goalLadderEnabled()` + `generateOffers()` take the run flag as a param; the bot reads the snapshot too. Verified: M0 green + 30-run v2 fuzz clean + a scripted probe that pins both directions (v2 run stays v2 with env OFF, v1 stays v1 with env ON). **Compound-learning:** *engine re-reading a global flag per-call across one logical unit → snapshot it onto the unit's state at creation and read the snapshot; test helpers that seed state via `makeState` must set the new snapshot field or they silently fall back to the default branch.*

**Key handoff for my (Lane B) UI:** the v2 daily shop IS the `/restock` screen. So making restock present as a proper daily shop = the same work as fixing the "restock looks way off" device bug (plus the selection-contrast + OfferCard tier-pip "dot" reports). That's the next Lane B piece.

**Open loops:** device feel-gate (does the fuller board *feel* like real decisions — fuzz only proves density) + Fable sign-off on the economy/flow change before it graduates from the flag. Phases 2 (tag-set build identity), 3 (daily score-goal ladder), 4 (balance + UI polish) still ahead. Also pending device confirm: CoinCounter alignment + run.tsx top-bar true-centering ([[performance-assets]] not yet a file — sprites/bg were shrunk ~96%).
