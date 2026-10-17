---
name: headless-cdp-media-emulation
description: How to verify prefers-reduced-motion (and other media features) at runtime — the Browser pane cannot emulate them; headless Chrome over CDP can
metadata:
  type: reference
---

The Browser pane cannot flip `prefers-reduced-motion` (see [[2026-08-animation-pass]]), and
`chrome --headless --dump-dom` hangs on Tondo (the mock WebSocket keeps the page busy).

What worked 2026-08-22 — script kept at the review session's scratchpad as `rm-check.js`,
recreate from this recipe:
1. `spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new',
   '--remote-debugging-port=9333', '--user-data-dir=<scratch>', 'about:blank'])` — first start
   with a fresh profile takes ~30s before `/json` answers; poll up to 60s.
2. Connect `ws` (already a Tondo dependency) to the page target's `webSocketDebuggerUrl`.
3. `Emulation.setEmulatedMedia({features:[{name:'prefers-reduced-motion', value:'reduce'}]})`,
   then `Page.navigate` to `?mock=1&scene=roundOver`, then poll `Runtime.evaluate` every 100ms
   until `body.dataset.screen === 'game'` BEFORE reading (the first read at 700ms was still on
   "home" — an invalid control). Result shape is `msg.result.result.value`.
4. Read the DOM in the same evaluation (piece count, computed display, `matchMedia().matches`).

Also the only way to measure FLIGHTS: the pane tab stayed `visibilityState: "hidden"` even after
`tabs_select` (rAF ticks = 0 over 20s), while headless ran rAF at 60Hz and a scripted real bot
game (create table → 3× add bot → deal → click a `— playable` hand button) captured the ghost's
last frame and the pile's 0% frame (`anim.pause(); currentTime = 0` inside the same rAF).
Recipe in the scratchpad's `handoff-check.js`; poll the lobby for ~10s — the WebSocket takes a
moment to connect.

Outcome: CONTROL 24 confetti / display block; REDUCE 0 confetti / display none / tp transition
0.001s. This closes the "reduced-motion only reasoned from CSS" gap in [[2026-08-polish-pass]].
