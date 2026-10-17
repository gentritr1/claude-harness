---
name: browser-pane-hidden-rendering
description: "FORM suspends WebGL when document.hidden; the Claude browser pane (and an occluded Chrome tab) report hidden, so previews look blank, transitions never advance and fps is meaningless there"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7144205e-fbda-47a3-975d-e55755cb416c
  modified: 2026-10-01T23:47:04.567Z
---

In the Claude desktop browser pane, `document.hidden` is `true` whenever the user isn't looking at the pane. FORM's `Sculpture.request()` refuses to render while hidden, so gallery previews screenshot as empty frames. rAF ran at ~28 fps early in the session and at 0 fps later (0 callbacks in 1200 ms); CSS transitions do not advance at all (an opacity transition stayed at its start value after 1 s). A tab opened through Claude in Chrome was hidden too (window occluded), 0 frames.

**Why:** this looked like a "blank gallery" bug and then like "the material crossfade never reaches its target" on review (2026-10-02); both were the harness.

**How to apply:**
- Static look: `Object.defineProperty(document,'hidden',{get:()=>false,configurable:true})`, then `allSculptures.forEach(s=>{s.last=0;s.request()})`, or call `s.draw(w,h)` directly.
- Token/end-state checks: set `document.documentElement.style.transition='none'` before reading computed values.
- Motion construction: trigger the change, then read `document.getAnimations()` (property, duration, easing), `pause()` + set `currentTime` to sample mid-states, `finish()` to settle. This proves the transition is built as specified; it says nothing about smoothness.
- rAF-gated code (e.g. `.tab-indicator[data-ready]`) never runs in the pane; set the flag by hand to test what depends on it.
- Pixel regression of the WebGL output: `s.draw(400,300)` then `gl.readPixels` in the same task and hash; repeatable across runs on the same machine.
- Never quote a frame rate from the pane. 60 fps needs a visible browser with frame count reconciled against window × 60, or the owner's eyeball. See [[form-design-direction]].
