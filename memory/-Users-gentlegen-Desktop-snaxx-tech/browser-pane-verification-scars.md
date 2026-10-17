---
name: browser-pane-verification-scars
description: In-app browser pane cannot prove keyboard activation (empty key field) and paint-starves when idle — how to verify UI claims despite it.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2eb1b0e0-08b6-44ed-bf4d-6e74e478f00e
  modified: 2026-08-04T23:08:55.516Z
---

Two verification scars from reviewing the Annex Acoustic Shadow implementation (2026-07-23):

1. The in-app Browser pane's `key` action delivers keydown/keyup with an EMPTY `key` value, and `type` uses insertText (no key events on buttons) — so native-button Space/Enter activation can NEVER be proven through the pane. A raw-CDP `Input.dispatchKeyEvent` script (see the-annex-mvp `evidence/acoustic-shadow-evidence.mjs`) is the only trusted-keyboard proof. Tab/focus movement DOES work through the pane.
2. When the pane isn't being screenshotted, rAF and paint starve: transitions driven by requestAnimationFrame appear permanently "stuck" (e.g. travel→closeup promotion) and screenshots can render loaded rasters as black. Force a `screenshot` to flush frames BEFORE diagnosing a "stuck" transition or "missing" image as an app bug.

**Why:** Both artifacts mimic real app failures; each cost a false-alarm investigation during review.

**How to apply:** In any pane-driven UI review — verify keyboard claims via CDP script or native-semantics reasoning + reachability; take a throwaway screenshot before judging animation/mount state. Also: probe computed `opacity` on the ANCESTOR chain, not the leaf (opacity doesn't inherit — a hidden parent reports children at 1). And synchronous JS clicks race React 19 commits: read state in a SEPARATE javascript_exec call, never the same tick.

Added 2026-08-05 (almanac hero session):

3. **Hidden tabs never load `<video>` at all** — Chrome (pane AND real Chrome via extension) leaves media at `readyState 0 / networkState 2` forever in a `visibilityState: hidden` tab; `fetch()` of the same URL succeeds, which makes perfectly good files look corrupt. Cost ~30 min chasing "broken" mp4s that a control file disproved. Check `document.visibilityState` FIRST; `<video>` playback proof requires a visible tab (user glance) — an injected `visibilitychange` probe that samples state into `window.__probe` makes that verification self-serve.
4. **Pane raster workarounds:** post-`scrollTo` screenshots return stale/blank rasters, and CSS `scroll-behavior: smooth` never completes (rAF starved — use `behavior:'instant'`). But `document.body.style.transform = 'translateY(-Npx)'` DOES repaint — translate instead of scrolling to screenshot below-the-fold content. IO-gated reveal sections stay `opacity-0` (nothing to paint, looks blank); force-reveal via JS before theming screenshots.
