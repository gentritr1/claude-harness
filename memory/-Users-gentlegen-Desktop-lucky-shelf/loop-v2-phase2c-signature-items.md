---
name: loop-v2-phase2c-signature-items
description: Signature items flag (Phase 2c) + dominance gate CLOSED — no item >2× median at scale.
metadata: 
  node_type: memory
  type: project
  originSessionId: 055e11c1-e558-4c66-b0dc-b4986591cb9e
---

Phase 2c = 5 run-defining **signature items** (brass-scale, ledger-book, lucky-cat, consignment-sign,
window-display) behind `SIGNATURE_ITEMS_ENABLED` (default OFF). New scoring rule kinds in
`src/sim/scoring.ts` (`tagFilteredShelfMultiplier`, `flatPerTagCount`, `copyHighestScoringOther`,
`shelfMultiplierIfAnyTagCount`, `highestBaseValueMultiplier`) resolve **post-window** off a
`baselineTotals` snapshot (no circular copies). APPROVED behind flag; see `docs/review-packets/A-M5b-*`.

**Dominance gate CLOSED 2026-07-07** (`docs/review-packets/A-M5b-signature-dominance-gate.md`). The
"lucky-cat 2.45× median" yellow flag was a **tiny-sample artifact (n≈1)** — it does NOT reproduce.
Evidence at scale (forced-seeding, equal n per item; the natural-pickup fuzz metric is too small-n to
trust — window-display's 2.01× there was n=2):
- Random boards (n=3000/item): top item = window-display, **1.13×** all-sig median. No item dominates.
- Favorable/ceiling boards (each item on the board built around it, vs strongest filler): max **1.74×**
  (consignment-sign); lucky-cat is **≤1×** (copies best *other* item but wastes a scoring slot).
- Run-level: withSignature bestDayTotal ~1.28× withoutSignature.

**Scar/rule:** per-item fuzz dominance ratios are noise-dominated at natural pickup (~18% split 5 ways).
To judge per-item power, **force equal large-n seeding via `makeState`** — don't trust ratios off a
handful of natural pickups. **Caveat still open for the feel-gate:** the probe ran levers OFF; lucky-cat
copies a *post-window* total, so next to a spotlighted ×3 hero its live ceiling is higher (still one
copy, bounded). Remaining gates: Fable sign-off on the rule kinds + device feel-gate. See
[[front-window-spotlight]], [[loop-v2-phase2a-tag-synergy]], [[reviewer-workflow-opus-split]].
