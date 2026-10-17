---
name: design-system
description: "The enforced layout/border/radius token system — theme from these, never raw numbers, so screens stop drifting."
metadata: 
  node_type: memory
  type: project
  originSessionId: 20ac0a0c-8bf3-4a85-8236-545a804b58ac
---

Codified 2026-07-07 to stop recurring per-screen spacing/border fixes. Full spec: `docs/lane-b/design-system.md`. Source of truth: `src/ui/tokens.ts`.

**Three ladders (all in tokens.ts, re-exported via `src/ui/index.ts`):**
- `layout` — screen rhythm: `screenPadX` (20, every screen's horizontal inset), `screenTopGap` (12), `screenBottomGap` (20), `sectionGap` (16), `stackGap` (12), `controlGap` (8), `cardPad` (16).
- `borders` — width ladder, a nested border is never thicker than its parent: `frame` 3 → `strong` 2 → `regular` 1.5 → `hairline` 1.
- Radius ladder: top-level surface `radii.lg` (16) → one level in `md` (12) → wells/chips `sm` (8) → pips/planks `xs` (4). Helper `innerRadius(outer, pad)` for the true edge-hugging concentric case; a *centered* child just steps down one tier.

**Rule of thumb:** never write a raw `borderRadius: 22` / `borderWidth: 2.5` / `paddingHorizontal: 24` again — reach for a token. If you're hand-tuning one screen, add/adjust a token instead.

**What the sweep fixed:** title screen used `xxl` (24) edge padding while every other screen used `xl` (20) → all on `screenPadX` now; magic `22` gear radius → `radii.pill`; `Panel` was `md`-radius while cards/frame were `lg` → all top-level surfaces unified to `lg` (user chose 16px). Border widths across CoinCounter/RentChip/MovesPips/OfferCard/WoodButton/ShelfPreview/ShelfScene/ItemSprite mapped onto the ladder (mostly same values, now tokenized).

**How the screen sweep was done:** `sed -i ''` across `src/app/{run,draft,restock,settings,catalog,share,summary}.tsx` for the mechanical bits (`paddingHorizontal: spacing.xl → layout.screenPadX`, `insets.top + spacing.sm|md → + layout.screenTopGap`, `insets.bottom + spacing.lg|xl → + layout.screenBottomGap`), then added `layout` to each `@/ui` import by hand. `cascade-harness.tsx` is a dev-only 9th screen, intentionally left out.

**Verified:** tsc strict clean, 59/59 vitest green, mobile-preset screenshots on title/settings/draft/catalog/run (restock/share/summary verified by parity — identical mechanical edit). Shelf border/radius values were tokenized to the SAME numbers, so no shelf visual change — the earlier [[art-chrome]]-era shelf-margin (symmetric top/bottom) and item-centering fixes still hold. See [[audio-system]] for the sibling gateway pattern.
