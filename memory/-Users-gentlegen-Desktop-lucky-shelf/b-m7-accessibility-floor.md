---
name: b-m7-accessibility-floor
description: "B-M7 accessibility floor built (prefs persistence, textScale, HC palette, color+shape) + the static-StyleSheet architectural scar"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9a3f4fc3-9fec-4013-b589-1964d5ba05b7
---

B-M7 accessibility floor implemented 2026-07-09 (Opus, Lane B), packet
`docs/review-packets/B-M7-accessibility-review.md`, **not committed** (three-lane dirty tree:
B-M7 mine, pre-existing run.tsx/ShelfScene-spotlight WIP, and B-M8 `src/juice/receipt/`). Awaiting Fable.

**Delivered (headless-green, 32 files/230 tests, tsc clean, 6 M0 fixtures intact):**
- `usePrefs` **did NOT persist** — was in-memory zustand, reset every launch. Added
  `src/persistence/prefs.ts` (zod, all fields optional → old-shape loss-free like B-M5 streak) +
  boot hydrate in `_layout` + **load-guarded** writes (catalog-wipe scar). Old-shape test written first.
- `textScale` (1/1.15/1.3) via `scaleTypeStyle` in tokens, applied ONLY in `AppText` (no per-screen math).
- High contrast = `highContrastPalette` + `resolvePalette()` token mapping (no per-component fork).
  Measured ratios (`scripts/contrast-check.ts`): normal body/coin already **AAA** (11.11/12.74);
  normal faint hint/tag text only AA-large (3.3–3.7); HC lifts **everything to AAA ≥7.59**.
- Color+shape: only genuine color-only STATE was the red/green drop glow (`ShelfScene SlotGlow`) —
  fixed with ✓/✕ overlay. Everything else already glyph-paired (build accents+tagEmoji, spotlight,
  record ★, streak 🔥, rent day-count text, arrows=CB-safe grouping). See [[design-system]] [[text-centering-pattern]].

**TRANSFERABLE SCAR → detection rule → brief update:** the brief assumed `AppText`/`typeScale` and
`palette` are universal funnels. **They are not** — 8 screens render raw `<Text>` with `...typeScale.*`
baked into static `StyleSheet.create` at module load, and `palette` is read statically everywhere. A
runtime pref (textScale, high contrast, theming, dark mode) therefore **cannot re-theme those reads
live** without migrating them to a runtime hook (`useTheme()`/`usePalette()` + AppText-everywhere).
→ **Detection:** before promising any runtime-switchable visual pref, grep for `StyleSheet.create` +
`typeScale`/`palette` reads; if screens bake them statically, live app-wide effect needs a theme-context
migration (a broad refactor — don't smuggle it into a feature brief; escalate).
→ **Brief rule:** an "accessibility/theming pref" brief must state whether the consuming layer is
runtime-themed or static-baked, and scope the migration explicitly. B-M7 delivered the central
mechanism + tokens + ratios; the app-wide wiring is a staged follow-up escalated to Fable.

**Gotcha:** no test imported `react-native` before B-M7; testing the ui/token layer needs a vitest
`react-native` stub alias (`src/test/react-native.stub.ts`, Platform+StyleSheet only) — tokens.ts
imports `Platform` at load and vitest's node env can't parse RN's Flow source. Added to `vitest.config.ts`.

Verification: all headless. Visual accept (✓/✕ legibility, 1.3× no-truncation on SE, HC look) is the
DEFERRED human device gate — seed recipes in the packet (`luckyShelf:prefs:v1`). See [[ios-ui-verify-on-simulator]].
