---
name: event-horizon-draft
description: /drafts/event-horizon three.js journey; startup must warm up hidden; frame harness and open gaps
metadata:
  node_type: memory
  type: project
  originSessionId: 71d00c39-45c1-490a-8542-7433d53286cb
  modified: 2026-10-10T22:12:34.952Z
---

`src/drafts/event-horizon` is a three.js particle journey through the 8 featured projects (PR gentritr1/portfolio#1, branch `claude/relaxed-lamport-u3jkmy`).

The owner called the opening "spinning, not smooth" on 2026-10-11. Measured cause: the intro animation ran while the shaders compiled and the textures decoded (stalls of 100-150 ms in production, 300-650 ms in dev). Fix: `compileAsync` plus one hidden composer frame before the canvas fades in, then `ImageBitmapLoader` textures uploaded one per frame. Result: 240 of 240 frames in the 4 s after reveal.

**Why:** an intro that moves fastest in its first frames exposes every startup stall. Warm up first, reveal second.

**How to apply:** any WebGL page with an intro reveals only after `eh:ready`-style warm-up. Measure with the frame harness (headless Chrome `--use-angle=metal`, rAF deltas counted from the ready mark, frames reconciled against 60 x window).

Open gap: an intermittent GPU-side stall of 500-770 ms about 2.8 s into a scripted scroll, seen in 3 of 14 runs. It shows no long task. Not reproduced on demand, so no fix yet. See [[three-composer-clear-colour]].

Gotcha (2026-10-11): `camera.lookAt` from almost straight above, with world up, leaves the roll undefined. A 0.02-unit hover lean rolled the hero view 63 degrees, and that was the owner's "keeps spinning aggressively". Fix: keep any looking-down keyframe about 12 degrees off vertical, and compute roll against sideways shift before shipping a camera pose. Lesson: when motion feels like spinning, check the camera basis before tuning speeds. Two earlier passes tuned rotation speed and damping and missed this.
