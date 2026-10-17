---
name: hidden-browser-pane-artifacts
description: The in-app Browser pane often reports document.visibilityState hidden; screenshots are stale frames and rAF never fires, so entrance animations look broken when they are not
metadata:
  type: feedback
---

Twice in this project (2026-09-09 and 2026-09-11) the Browser pane ran with
`document.visibilityState === "hidden"`. Consequences: `requestAnimationFrame` never fires (a
JS probe awaiting it times out at 45s), CSS entrance animations sit at their 0% frame, and
screenshots return a stale frame — so a `.hero-sequence` with `opacity:0 → 1` looks permanently
invisible on both production and the fix branch, which is NOT evidence about the fix.

**Why it matters:** I nearly reported "the hero fix didn't work" from a screenshot.

**How to apply:** for anything animated, verify with `getComputedStyle` / `document.getAnimations()`
/ DOM semantics via `javascript_tool` and `read_page` (they work hidden), and state plainly
that the rendered look is UNVERIFIED until the pane is visible or a device screenshot exists.
Never await rAF inside a probe. Also: `[...document.fonts].filter(f => f.includes('loaded'))`
matches "unloaded" — read the raw status strings.
