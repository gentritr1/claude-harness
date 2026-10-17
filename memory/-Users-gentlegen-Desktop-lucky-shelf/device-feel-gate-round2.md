---
name: device-feel-gate-round2
description: 2nd device feel-gate (day 9) — found a full-shelf softlock (fixed 06771cf) + data-backed loose-economy signal for Fable.
metadata: 
  node_type: memory
  type: project
  originSessionId: a55d034b-799c-4add-95d3-38f4c5c38f10
---

Second device feel-gate, 2026-07-08 (Relay, day-9 arrange screenshot, all depth flags ON: LOOP_V2,
SIGNATURE, TAG_SYNERGY, BUILD_STEERING, GOAL_LADDER, spotlight/order). Two findings:

**1. Full-shelf softlock — FIXED `06771cf`.** Drafting a delivery item onto a full shelf → a held item
that can't be placed (no empty slot), and `openShop` throws while holding → the Arrange screen offered no
exit but abandon. The **engine already anticipated it** (`legalActions` keeps `sellItem` legal while
holding — the "F-1" comment in [engine.ts](src/sim/engine.ts) ~526), but the UI never surfaced selling.
Fix: [run.tsx](src/app/run.tsx) Arrange now shows a "shelf full — sell to make room" hint + tappable
"Sell +N" chips (reuse `sellShelfView` + `sellItem`) when holding + no empty slot. Verified: sim shot +
an engine probe (sell → freed slot → placeItem legal → openShop legal). **Scar/rule:** when the engine
keeps an escape action legal "so it doesn't softlock", grep that the UI actually exposes it — the comment
is a smell that the affordance may be missing on some screen.

**2. Economy too loose with all flags ON — data-backed, logged for Fable** (FABLE-SIGNOFF-QUEUE.md).
120-run fuzz: earnings **~4–7× the rent burden** (day 9 ~118 earn/day vs ~17 rent/day), bots survive
**median 30 days**. Money piles up (167 coins day 9), only sink is the 12-slot shelf → overflow → the
softlock above. Rent `×1.6` late curve never catches the stacked multipliers. Fable's tuning call
(tighten rent / multipliers / add a sink). **Important:** none of this session's work (signposting, art,
nav) touched economy numbers — it's pre-existing provisional balance the feel-gate surfaced. See
[[device-feel-gate-round1]], [[lane-b-signposting]], [[loop-v2-phase3-goal-ladder]].

**3. Liveness harness — generalized the softlock into a permanent test (`de056fa`, `2558e1c`).** Key
insight: the existing `scripts/fuzz.ts` drives engine `legalActions`, so it can't see UI↔engine
mismatches (it just "sold" past the softlock). New `src/sim/uiAffordances.ts` models what each SCREEN
exposes; `src/sim/liveness.test.ts` fuzzes runs through ONLY those and asserts (a) no non-terminal state
with zero screen actions (dead-end), (b) no exposed-but-illegal action. **Proven to bite:** reverting the
fix in the model fails the fuzz at `arrange/held/empty=0` within ~40 random **baseline** runs — so the
softlock was reachable in the *default* game, not just the depth build. `scripts/balance.ts` prints
money-on-hand-vs-rent surplus (its greedy is a naive FLOOR that dies day-3; the strategy bot is the
CEILING ~30d — the gap is a **skill cliff**, so a real balance pass measures both). Codex brief to extend
this into the full economy-band harness: `docs/lane-a/balance-harness-brief.md` — **blocked only on the
soft-spot target bands (Fable/human), which the harness enforces but can't invent.** Rule: model UI
affordances and fuzz THOSE, not just engine legality, to catch screen-level dead-ends.

**4. Harness built out + reviewed (`b2f2cce` + trace fix `97deee1`, 2026-07-08).** Codex/user made
`uiAffordances` the AUTHORITATIVE screen-action source: store exposes `draft/arrange/restockAffordanceView`
and [draft.tsx](src/app/draft.tsx)/[run.tsx](src/app/run.tsx)/[restock.tsx](src/app/restock.tsx) derive
their buttons from it (drift now hard). Added `balanceHarness.ts` (floor+ceiling reports),
`invariants.test.ts` (fuzzed state properties), and a skipped `TODO(fable)` band gate (bands still unset —
the one intentional skip). **Review scars, both fired:** (a) the delegate reported "116 passed" but
re-running found **2 flaky FAILURES** — the two fuzz tests exceeded vitest's 5s default and set no
timeout; added explicit 30s timeouts → stable. *Always re-run the delegate's green.* (b) the new invariant
test immediately **caught a real pre-existing trace bug** (edge `copiesNeighbor` emitted `targetSlot.col=-1`,
fixed `97deee1`, score/determinism-neutral) — the harness paid for itself on day one. Verified: liveness
guard still bites post-refactor; all 3 rewired screens render identically on the sim; pin/goldens/fixtures
unchanged. **Still open:** the `TODO(fable)` soft-spot bands (`docs/lane-a/balance-harness-brief.md` §6).
