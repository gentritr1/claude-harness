---
name: cdp-capture-harness
description: scripts/shoot.js — the headless-Chrome CDP harness for Tondo, and the three traps that made it lie before it was fixed
metadata:
  type: reference
---

`scripts/shoot.js` (added 2026-09-09) is the only trustworthy way to verify Tondo
visually or in motion. It drives real headless Chrome over CDP, plays a REAL bot
game over a real WebSocket (not `?mock=1`), asserts `document.hidden === false`
before capturing, finishes animations before measuring, and reports page errors.

```
node scripts/shoot.js --out DIR --scene game|lobby|roundOver|pieComplete --w 1440 --h 900
node scripts/shoot.js --scene game --reduced --probe "<js expression>"
TONDO_URL=http://localhost:4610 node scripts/shoot.js ...
```

**Three traps it hit, all of which produced a confident wrong answer first:**

1. **A fixed debug port attaches to a ZOMBIE.** `--headless=new` detaches a
   process tree that outlives its launcher, so the next run on port 9333
   attached to a browser still sitting on `about:blank`. Symptom: 628 no-op
   driver ticks that looked exactly like a broken app. Fix: `--remote-debugging-port=0`
   plus read the real port from `DevToolsActivePort`, and kill only processes
   matching this run's unique `--user-data-dir`. **Never `process.kill(-pid)`** —
   a recycled pid makes that a random process-group kill; it is the likeliest
   cause of "my dev server keeps dying".
2. **The round-over detector fired on the wrong banner.** `#banner` carries both
   "YOUR TURN" and the win, so watching it captured a mid-round screen and
   labelled it `roundOver`. Detect a win by the `win` tone class AND the host's
   deal button.
3. **The driver must match the BREAKPOINT.** `.btn-draw` is `display:none` on
   desktop (the deck beside the hand takes over) and the deck is hidden in the
   phone band. Driving only one stalled every desktop run at `wait`. Also: the
   wild picker must be handled BEFORE the drawn-card bar — a drawn WILD opens
   the picker while the drawn bar is still up, and checking drawn first
   re-clicks "Play it" forever (1855 no-op clicks in one run).

**Rule:** a probe that reports success without evidence it exercised the path is
a vacuous pass. The seat-survival probe returned 3/3 surviving with ZERO
repaints observed — it now drives moves itself and reports `valid: false` when
nothing changed. Always print the count of the thing that was supposed to happen
next to the verdict. See [[browser-pane-click-flakiness]], [[headless-cdp-media-emulation]].
