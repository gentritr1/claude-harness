---
name: todays-order-demand
description: "Second flagged depth-prototype — a daily tag-collection \"order\" bonus, built alongside the spotlight for a side-by-side device feel test."
metadata: 
  node_type: memory
  type: project
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

Companion to [[front-window-spotlight]], built 2026-07-07 so the owner can feel two different depth levers on one device build. Where the spotlight adds a *positional* decision, "Today's Order" adds a *selection/collection* decision.

**Mechanic:** a customer wants `DEMAND_COUNT` items carrying one tag, chosen deterministically from a pool of well-represented tags (≥4 items: fancy/food/antique/lucky/fragile/utility/drink/perishable/sweet/plant). Fill the order (≥count of that tag placed at Open Shop) and every matching item's window is ×`DEMAND_MULT` (1.5).

**Tuning pass (2026-07-07), before device build — found a real bug:** the order was originally re-rolled EVERY day (keyed on `day`), but you draft only one item/day, so a 3-of-a-tag order whose target changed each morning was structurally unfillable-on-purpose — which is the actual reason the demand barely moved the fuzz, not a weak mult. Fix: `pickCycleOrder(seed, rent.cycle)` so the order HOLDS for the whole 3-day rent cycle and only rotates when rent resets → a real multi-delivery chase. Also `DEMAND_COUNT` 3→2 so it reliably fills across a cycle and the reward gets felt. Verified directly by tracing a run: order stayed `plant x2` across days 1-3 (cycle 1) while the spotlight rotated daily. Detection rule for future: a per-day goal that needs multi-day accumulation against a 1-draft/day loop is unfillable — align goal horizon with the resource cadence. Order-met is a shelf-wide set check computed before window resolution (like ambient auras); the mult is applied per matching item before the spotlight cap, emitted as a `ruleFire` (ruleId 'order') so the cascade renders it with no new trace-event kind.

- Flags: `DEMAND_ENABLED` / `DEMAND_MULT` / `DEMAND_COUNT` / `DEMAND_TAG_POOL` in [economy.ts](src/sim/economy.ts), independent of the spotlight flag so each lever toggles alone.
- `dailyOrder?: DailyOrder | null` — same additive/optional save-safety as spotlight (no ContractSchemaVersion bump).
- UI: `OrderBanner` in [run.tsx](src/app/run.tsx) shows the demand + live shelf progress (turns green when fillable).

**Verified:** tsc clean; 59/59 tests incl. golden traces unchanged; determinism pin re-updated (f530…→879b4ce2…). Fuzz A/B (100 runs, combo strategy): baseline both-off bestDay med 77 / rent 7 → demand-only bestDay med 87 / rent 7 → spotlight-only bestDay med ~113 / rent 8 → **both-on bestDay med 123, rent 8, combo max 807** (the two mults stack into jackpot days).

**Key insight / honest caveat:** demand barely moves *bot* survival (7→7) because greedy/combo bots don't draft toward the wanted tag — the demand rewards *intent*, which bots don't have and the fuzz can't measure. So it is the most human-dependent of the two levers and its bot numbers understate it more than the spotlight's do. This is the whole reason it needs the device feel-gate, not a fuzz verdict.

**UNVERIFIED:** device feel of both levers, individually and stacked — is the order a real draft driver, is ×1.5 enough, does the banner read, do stacked jackpot days feel great or broken. Owner holds the gate. To isolate: toggle either flag in economy.ts.
