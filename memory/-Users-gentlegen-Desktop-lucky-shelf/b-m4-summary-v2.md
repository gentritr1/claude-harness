---
name: b-m4-summary-v2
description: "B-M4 Summary v2 retention (implemented, awaiting Fable + device gate): persisted personal bests + New record!, build recap, near-miss line; additive save/contract fields kept off the determinism pin."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5bc41c48-dd7b-4ca8-8eff-56611ee9e0d8
---

B-M4 (Lane B, summary retention) **implemented 2026-07-08, not yet reviewed** — packet
`docs/review-packets/B-M4-summary-v2-review.md`, screenshots in `B-M4-screens/`. Five items
in `src/app/summary.tsx`: daily New Run button, Best-day via CoinCounter, persisted personal
bests + celebratory **★ New record!** (respects reduced-motion), synergy-gated build recap,
and a near-miss "paid rent with N to spare" line (≤5).

**Two additive persisted/contract fields, both engineered to stay OFF the graduation floor:**
- `CatalogStats.longestRun` — `nonNegativeIntSchema.default(0)`, **no** `CatalogSchemaVersion`
  bump. Old catalogs (stats without the key) still parse (Zod fills 0), never wiped. Load
  test written BEFORE the UI (`catalog.test.ts`). Catalog isn't in the hashed GameState, so
  it can't touch the pin/goldens.
- `RunStats.closestRentMargin?` (item-5 CCR for Fable) — optional, **written only on a
  *successful* rent payment** in `engine.ts`. The M0 goldens hash scoring *traces* (not
  runStats) so they're unaffected; the pinned determinism fixture dies day-3 **before** paying
  rent (`deepestRentSurvived:0`, probed), so the field stays undefined there and
  stableStringify drops it → pin `8d48e1c5a6ad14c9` unchanged. **Scar/risk flagged to Fable:**
  that safety rests on the pinned fixture dying pre-rent; a future re-pin with a rent-surviving
  fixture would pull the field into the hash (deterministically).

Screens stayed boundary-clean: new data via store view-models `personalBestsView`
(catalogStore), `buildIdentityView` + `nearMissView` (store) — no `@/sim`/`@/items` in `src/app`.
`prevStats` (standing bests for "is this a record?") is frozen at summary mount via
`useCatalogStore.getState().catalog.stats` BEFORE `recordRunEnd` merges — post-merge would
always tie. See [[ios-ui-verify-on-simulator]] for how the 4+SE screenshots were captured.

**Human device-gate polish (2026-07-08, same session):** (1) "New record!" boxed pill →
light gold ★ star-text (no box) — stacked pills read heavy. (2) Coin digit sat 1px low in the
pill; trimmed the shared `baloo2IconNudge` from +2→+1 for `CoinCounter.amount` **pill only**
(slam keeps helper) — this is the shared HUD chip too, so it's app-wide. (3) **Font FOUT**:
the title flashed the system fallback before Baloo2 loaded. Fix in `_layout.tsx` —
`SplashScreen.preventAutoHideAsync()` (expo-router's optional-native-module wrapper) + gate
the first render on `useFonts` `[loaded]` (`return null` until ready; `fontError` still passes
through as fail-safe). **Transferable Expo scar:** never render before `useFonts` resolves if
any display face is load-bearing — hold the splash and gate, don't "render regardless".
(4) **Title wordmark clipped** ("Lucky Shelf" f-hook/ascenders cut off): the `index.tsx` title
override was `fontSize:44 / lineHeight:48` (1.09×) — **Baloo 2's natural line box is ~1.58× em**,
so a tight lineHeight clips ascender tops on iOS. Fixed to lineHeight 60 (~1.36×). Audited the
shared Baloo2 tokens (display 1.235, title 1.25, heading 1.33) — clean at their sizes, left
untouched. **Scar:** for Baloo 2 (and other tall-metric rounded faces) keep lineHeight ≥ ~1.3×
fontSize, especially on size overrides; see [[text-centering-pattern]].
(5) **Run screen** (out of B-M4 scope, same device pass): `BuildSignpost` empty title was
`'YOUR SHELF'` — collided with the `SectionLabel` "YOUR SHELF" above the grid; renamed panel
empty title to "YOUR BUILD". (6) Spotlight "✨ WINDOW ×N" badge wrapped/overhung — it was an
absolute tag clamped to ~slot width; wrapped in a centred full-width band (`spotlightTagWrap`)
+ `numberOfLines={1}`. **Gotcha:** `src/juice/ShelfScene.tsx` is under concurrent edit — an
external reformat silently REVERTED my SpotlightMarker change once; re-apply and re-grep to
confirm it stuck. Also: `engine.ts`/`economy.ts`/`contracts.test.ts` etc. carry parallel Lane A
(A-M6a shelf-expansion) edits in the same tree — stage the B-M4 commit selectively.
