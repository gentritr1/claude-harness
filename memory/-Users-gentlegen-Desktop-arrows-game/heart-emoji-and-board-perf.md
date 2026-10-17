---
name: heart-emoji-and-board-perf
description: Two fixes — ♥ emoji ignored text color (lost hearts stayed full); board re-rendered all ~155 arrows per interaction
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 864b6b08-3524-4c0f-854a-a863fa1e1806
  modified: 2026-07-20T18:50:57.086Z
---

Two GameScreen/BoardView fixes, device-verified on emulator 2026-07-19.

**1. Lost heart showed as full.** `HeartPip` rendered a bare `<Text>♥</Text>` (U+2665).
Android gives that glyph EMOJI PRESENTATION → paints its own red and IGNORES the `color`
style. So hearts showed red (not theme magenta-rose #E4327D) AND a spent pip (color→
heartLost) never dimmed. Fix: render the heart as an SVG `<Path fill=...>` (react-native-svg
already a dep) — SVG fill honours the color. Verified: forced real collisions, header showed
1 magenta + 2 dim pips.
**Why:** color-emoji glyphs override text `color` on Android. **How to apply:** never rely on
text `color` to tint a symbol glyph (♥ ★ ● etc.) on Android — use SVG/vector or a
variation-selector-forced text presentation (VS is unreliable; prefer SVG). Detection: if a
themed glyph renders in a stock color (red/black) instead of your hex, it's emoji presentation.

**2. Board re-rendered every arrow on every interaction.** BoardView draws the whole board as
one `<Svg>` with `board.arrows().map(<StaticArrow/>)`; `StaticArrow` was NOT `React.memo`'d and
`arrows()` returns the live array re-mapped each render. On SuperHard (~155 arrows ≈ 310 SVG
paths) a single tap → 273 StaticArrow re-renders (parent re-renders twice: setShaking +
setHearts, each reconciling all nodes) mid-animation = jank. Fix: `React.memo(StaticArrow)`
(props arrow identity + ink string, both stable; key=arrow.toLine()). After: same tap → 1
re-render (273→1). Arrows don't depend on neighbors so memo is safe.
**Why:** unmemoized children + live-array .map re-reconcile the whole SVG on any parent state
change. **How to apply:** for large mapped SVG/canvas node lists, memo the leaf and keep props
referentially stable; measure with per-render console.count, not just gfxinfo (swiftshader
emulator pins jank% ~95% regardless — render-count delta is the hardware-independent signal).
Device fps still needs a real-device spot-check. See [[arrows-release-signing]].
