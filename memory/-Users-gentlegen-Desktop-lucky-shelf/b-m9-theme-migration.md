---
name: b-m9-theme-migration
description: B-M9 runtime-theme migration — static StyleSheets → useThemedStyles factories on every screen
metadata: 
  node_type: memory
  type: project
  originSessionId: fe3ed2ec-1ac1-4973-b113-f9c43b788d90
---

B-M9 (runtime-theme migration) **Fable-APPROVED 2026-07-10 + pushed** (`b1956d8`..`4e7f58c`, 9 screen
commits + packet; verdict in `docs/review-packets/FABLE-REVIEWS-2026-07-10-round6.md`). Adopted the
B-M7 comfort funnels app-wide so high-contrast/large-text actually reach screens that baked type/color
into module-load `StyleSheet.create`. Device gate (1.3×/HC shots on SE) still open — batched in the
round-6 doc. `run.tsx` migrated too (`cdba62a`, Fable-implemented after the WIP window closed) —
src/app grep fully clean; ShelfScene Skia canvas is now the ONLY remaining theme gap.

**Pattern (reuse for any new screen):** each screen's sheet lives in a sibling `src/app/<screen>.styles.ts`
as `export function makeStyles(palette: Palette) { return StyleSheet.create({… palette.X …}) }` (reads
the PASSED palette, never the module token). Screen does `const styles = useThemedStyles(makeStyles)`
(new helper in `src/ui/useThemedStyles.ts`, memoized on textScale+highContrast) and
`const palette = usePalette()` (new selector in prefs.ts) for inline `AppText color={…}` props. Do NOT
reintroduce a static themed `StyleSheet.create` in a screen `.tsx`.

**Why the `.styles.ts` split:** the factory-at-defaults equality test must import `makeStyles` headlessly;
the vitest RN stub only covers Platform/StyleSheet, so the factory can only import `@/ui/tokens` (pure) —
importing the screen `.tsx` (expo-router/Skia/RN components) would blow up in node.

**Equality-test recipe (byte-identity proof):** transcribe the ORIGINAL sheet independently as
`expected(p)`, assert `makeStyles(palette)===expected(palette)` (default byte-identity) AND
`makeStyles(highContrastPalette)===expected(highContrastPalette)` (leak-guard: a prop that read module
`palette` wouldn't re-theme and diverges). `resolvePalette(false)===palette` by identity → default path
byte-identical for free.

**Scars/gotchas hit:**
- `usePalette()` needed because AppText only HC-remaps its DEFAULT color; screens passing explicit
  `color={palette.ink}` stay fixed unless the color is threaded from usePalette.
- Rules-of-Hooks: catalog `ItemStamp` had an early `return <LockedStamp>` — moved `useThemedStyles`
  above it.
- Raw-`<Text>` exceptions that must NOT go through AppText (would change font/byte-identity): bespoke
  numerals with no type role (share heroNumber, restock signatureBadgeText), coin-nudge digits needing
  baloo2IconNudge (restock rerollCost/shopBuyText), emoji/glyph icons (draft supplierEmoji, restock
  sellGlyph/shopThumbGlyph). Colors still parametrized so they re-theme.
- Known limit: **ShelfScene** colors are Skia canvas-side — `useThemedStyles` can't reach them; HC
  won't re-theme the shelf until a separate Skia pass. `run.tsx` left static (human WIP, per brief).
- Flaky sim tests `sim/unlocks` + `sim/balanceHarness` fail intermittently (fuzz, ~750s) — OUTSIDE any
  UI diff's import graph (they import no @/ui/@/app); don't chase them for a UI change. See
  [[balance-target-bands]], [[b-m7-accessibility-floor]].
