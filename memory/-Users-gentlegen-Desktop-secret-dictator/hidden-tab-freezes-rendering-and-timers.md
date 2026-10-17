---
name: hidden-tab-freezes-rendering-and-timers
description: "A hidden browser-preview tab clamps setInterval to ~1-2s AND stops compositing, so getBoundingClientRect returns creation-time values — three measurements were wrong before I noticed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d90e3f0-7698-483d-a615-b31b363ed1c5
  modified: 2026-08-08T20:20:30.501Z
---

Driving Secret Dictator through the Browser preview tools, `document.visibilityState`
was `"hidden"` for most of the session (JS eval does not front the tab; screenshots
and `resize_window` do). Two independent distortions came from that, and both
produced measurements that looked plausible:

1. **Timers clamp to ~1-2s.** A 400ms sampler ran at ~1000-2000ms, and a 62s
   `setInterval` window silently never resolved at all. Reconcile sample count
   against `window / interval` before quoting anything derived from it — 62 samples
   over a 62s window means the interval was 1000ms, not the 500ms requested.
2. **Rendering freezes entirely.** `getBoundingClientRect()` kept returning each
   standee's *creation-time* rect (gate spawn point) and `getComputedStyle().opacity`
   kept returning the `at-gate` value `0`, ten minutes and twelve game-days after
   those were true. Inline `style.left/top` were correct the whole time.

**Detection rule:** when verifying rendered geometry in a preview tab, either
(a) read the *style* values, which are never stale, or (b) force a paint first —
`resize_window` reliably does it, a plain screenshot request sometimes serves a
cached frame. If a rect looks like an initial/spawn value, suspect the freeze before
suspecting the code. Screenshots taken without forcing a paint can be a whole phase
out of date (this cost two wrong "the reveal is broken" conclusions).

Related: [[grid-center-degrades-to-start-on-overflow]]
