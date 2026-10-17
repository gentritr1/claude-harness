---
name: offbeat-measurement-traps
description: "Instrument errors hit while measuring OFFBEAT on 2026-10-02 - load-tail misattribution, empty computed font shorthand, double rAF probe, DOM watermark mistaken for a 3D artifact"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1dcc955e-d230-4e7b-a170-720a969b4385
  modified: 2026-10-01T22:50:46.165Z
---

Four of my own measurement mistakes from the 2026-10-02 pass. Each one produced a confident wrong reading until I checked it.

1. **Load tail blamed on the first interaction.** "First explode" showed a 41-116ms stall. It was load-time scene building still running 1.5s after load. A swatch click (the control) stalled the same way. The rule: settle at least 4s, run a control interaction, and take 5 runs before blaming a feature. `scripts/qa/frames.mjs` now waits 4s.
2. **`getComputedStyle(el).font` is `""`** when `font-stretch` is a percentage (Archivo set to 112%). A probe span built from it measured in a fallback font: 8.14x instead of the real 8.68x. Measure text by cloning the real element.
3. **Two rAF probe loops overlapped**, recording 288 frames where 151 were expected. A boolean on/off flag lets the old loop survive a quick restart. Use a generation token. Always print frames next to expected.
4. **A soft grey square that looked like a shadow artifact** was the full stop of the DOM watermark "ob." showing behind the canvas. Hiding meshes one at a time changed nothing, which proved it wasn't three.js.

**Why:** each one would have shipped a wrong fix or a wrong number (CLAUDE.md §6 red flags: sample reconciliation and instrument audits).
**How to apply:** before quoting any OFFBEAT perf or layout number, reconcile the count, run a control, and confirm the instrument reads the real element. See [[offbeat-pass3-review]] and [[offbeat-env-gotchas]].

5. **Worker rendering blinds the main-thread frame probe** (2026-10-02, review of 49a9455). Once the 3D moved to an OffscreenCanvas worker, `frames.mjs` (main-thread rAF) could no longer see render jank. Measure the worker's frames from a Chrome trace (`FireAnimationFrame` on the DedicatedWorker thread). Also force the fallback path (delete `transferControlToOffscreen` in an init script), or the main-thread renderer ships untested.
6. **An implementer without a browser shipped a visible regression it had disclosed but could not see**: the empty poster manifest makes the loading state show the living-room *photo*, then snap to the 3D. Detection rule: screenshot the first ~150ms at 4x throttle. Brief update: poster capture is a release gate, not optional.
