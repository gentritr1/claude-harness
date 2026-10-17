---
name: verification-gotchas
description: Browser-verification scars from cryptid-rush animation/QA passes
metadata: 
  node_type: memory
  type: project
  originSessionId: 08b7d6ff-99c6-48f9-a148-270af845d6ae
  modified: 2026-08-15T13:24:24.399Z
---

Scars from verifying [[project-overview]] in the Browser pane:

- **Hidden pane = rAF suspended.** When the Browser pane isn't on screen, `document.visibilityState`
  is 'hidden' and requestAnimationFrame never fires → any rAF-based frame sampler times out.
  Synchronous `performance.now()` timing and screenshots still work. For cadence numbers, run a
  self-reporting harness in headless Chrome (`--headless=new --enable-logging=stderr`, console.log
  a tagged JSON line, grep stderr).
- **Never cancel() all document.getAnimations().** That sweep includes CSS keyframe loops
  (hudpulse/arrowpulse/slide); on reused DOM nodes a canceled CSSAnimation stays dead — re-render
  doesn't restart it because ui.js writes the same animation string (no style invalidation).
  Scope cancels to the WAAPI animations you created, or reload the page after probing.
- **fx.js has a ~3000 ms safety cleanup** that removes FX elements even while their animations are
  paused — to hold a frozen FX frame for a screenshot, suppress setTimeout(fn, ms>=2500) around
  the CRFX.handle() call, then restore.
- Headless bench numbers (2026-08-15, software compositing, 3x worst-case storm, 55 concurrent
  anims): median frame 8.3 ms, p95 16.7 ms, one 50 ms hitch in 3.5 s; live main-thread costs:
  CRUI.render 0.07 ms avg, full FX storm handle 1.6 ms.
