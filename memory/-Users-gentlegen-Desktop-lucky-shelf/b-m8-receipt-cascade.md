---
name: b-m8-receipt-cascade
description: "B-M8 receipt model — pure receiptFromTrace, cause-then-effect grammar, built + tested, awaiting Fable/look gate"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7fcfb780-0a23-4aba-bf27-7b52ced94633
---

B-M8 (2026-07-09): the pure receipt core is built and green — `src/juice/receipt/receiptModel.ts`
(`receiptFromTrace(trace, deps)` → `ReceiptLine[]`), `print.ts` (cadence selector), `index.ts`,
+ tests. 25 tests pass, tsc-clean for the new files. **Additive-only: zero sim/trace/contract
changes**, determinism pin `8d48e1c5a6ad14c9` + 6 M0 goldens untouched. Packet:
`docs/review-packets/B-M8-receipt-cascade-review.md`. Awaiting Fable (model) + human (look).

Grammar = *source → affected → delta → total*. Each trace event → 1 receipt line tagged with the
`eventIndex` that reveals it, so the receipt prints on the cascade player's existing `stepIndex`
clock (no second timer; reduced motion = `revealAll`). See [[cascade-self-fire-pop]].

Non-obvious calls (for the reviewer / future me):
- **The R-6 beneficiary decides which window a cause nests under** — the OPEN window slot, NOT
  `targetSlot`. A cause names the *source* item (`sourceSlot`) but sits under the *affected*
  window, which is the arrow's source in fixture 1 and its target in fixture 4 (honey→wine).
  Mirrors `cascadeState` (`openSlot ?? targetSlot`).
- **Row-aura → subtotal jump is attributed IN THE MODEL, not by a new event.** A rowAura is
  emitted once at its source and applied at each row item's `itemTotal`, so a subtotal can exceed
  the last cause's running total (fixture 4: 8 → 12). The `rowAura` event already carries
  sourceSlot+mult+row, so the model tags the subtotal `(row ×m)` — the trace WAS sufficient, no
  escalation. This is the answer if Fable asks "why isn't the 12 an orphan."
- `itemTotal` prints a subtotal only when the item took ≥1 cause; a plain item stays one line.
- Grammar guarantee is deps-agnostic: unknown shelf slot → `Slot r,c` fallback, so a cause is
  never sourceless (tested). The 50-trace fuzz proves no orphan deltas.

Gotcha: the synergy+spotlight+signature attribution test must spotlight an item that scores > 0
(the spotlight lever emits no ruleFire when the spotlighted item totals 0 — mult on 0 is a no-op).
Spotlighting shop-cat (base 0) made the assertion vacuous; moved it to maneki-neko. Verify a
lever-coverage test actually fires the lever, don't just guard-and-skip.

Repo state caveat: a **parallel uncommitted B-M7 accessibility-floor** change (tokens.ts,
tokens.test.ts, contrast-check.ts, AppText, settings, _layout, prefs) leaves repo-wide `tsc` and
one vitest suite red. That is NOT B-M8 — my work is isolated to `src/juice/receipt/`. Don't touch
those files; coordinate on the tokens overlap the brief warned about.
