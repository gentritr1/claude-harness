---
name: custom-font-android-gotchas
description: "Overpass (art_v2) on Android, device-verified 2026-09-16: the middle dot is a GDEF mark (zero width), fontWeight next to a custom family draws Roboto, tabular-nums works; GMS Ads no longer logs ad unit IDs"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T17:12:21.569Z
---

Found building E1a (design system, `src/design/`) on the Pixel_8_Pro AVD (API 36) with a
`build:qa-apk` release APK. Each was measured on device by `DesignPreview`'s Font check
(Text `onLayout` widths), not reasoned from source.

1. **Upstream Overpass 4.000 classes U+00B7 `·` (and `` ` ¨ ¯ ´ ¸ ``) as GDEF combining marks.**
   HarfBuzz (Android and Chrome) gives marks zero advance, so every " · " separator rendered as
   "ON ·showing". Fixed in `scripts/fetch-fonts.mjs` (reclassify to base glyphs after subsetting);
   `overpass-metrics.json` records `spacingGlyphsClassedAsMarks: []` and a test guards it.
2. **`fontWeight: '700'` next to `fontFamily: 'Overpass-Bold'` draws Roboto Bold.** RN looks for
   `fonts/Overpass-Bold_bold.ttf`, misses, falls back to the system family (268.7 vs 256.7 dp).
   Weight must come from the family file only; `check:type-tokens` bans fontWeight in v2 styles.
3. **`fontVariant: ['tabular-nums']` does reach an asset font on RN 0.81** — "111,111" and
   "000,000" both 111.3 dp (73.7 / 120.0 dp without). The brief's top UNVERIFIED risk is closed.
4. Accented capitals overshoot Overpass's 1.266 em line box but were NOT clipped at 40/52 or 40/48.
5. **`setprop log.tag.Ads VERBOSE` no longer shows ad unit IDs or request URLs** (GMS Ads container
   26.33.32), even after force-stopping Play services — EXECUTION.md §3's recipe didn't work here.
   Only the manifest app ID appears. Test-unit proof is the build stamp, not logcat.

**How to apply:** E1b migrating screens to Overpass needs none of 1-3 rediscovered; keep the
font check in the QA design preview as the device instrument. Related:
[[verify-webview-maps-without-a-device]], [[web-preview-qa-gotchas]].
