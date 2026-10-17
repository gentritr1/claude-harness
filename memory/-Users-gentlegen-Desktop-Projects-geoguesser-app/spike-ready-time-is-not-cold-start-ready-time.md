---
name: spike-ready-time-is-not-cold-start-ready-time
description: The Skia spike was ready in 16-43 ms on an idle JS thread; on a cold start the same prep took 0.5-3.3 s (8/8 skips) because it queued behind app startup
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T08:01:22.747Z
---

ART-4b 2026-10-08. The bake-off measured Skia readiness inside a QA modal with the app idle: 16-43 ms. On a cold start of the art_v2 home on the Pixel_8_Pro AVD, the same work (require, effect compile, mask fetch+decode, surface size, warm-up ticks) took 503-3259 ms from mount. All 8 cold starts skipped against the brief's 200 ms deadline. That deadline was never measured: it came from the FadeIn length. Even the base APK drew only 5-30 of ~90 frames in its first 1.5 s.

Follow-up the same day: a redesign that let the spin "come alive" ~0.5-1 s after a cold start JANKED even when it was ready in time: 11 UI ticks of 31, a 350 ms stall. Two fix rounds of fade-through and touch-race machinery followed. The final design is ONE move: the spin plays under the hero FadeIn at the first home entrance after Skia is warm, warmed on an idle turn. The cold-start mount never spins.

**Why:** a spike run in isolation measures the work, not the contention. App startup owns the JS and UI threads for the first seconds.

**How to apply:** pattern -> detection rule -> brief update.
- Pattern: a readiness or latency number taken from a spike.
- Detection rule: before any deadline is written into a brief, measure it in the REAL trigger context (cold start, with the app's own startup running), with a QA-only late-ready probe that logs each component from mount.
- Brief update: design the entrance so nothing visible waits on it (here the hero never waits; the spin runs on the first entrance where it is ready).
Related: [[gfxinfo-rows-are-not-frames]], [[a-min-over-a-sampled-matrix-is-an-artefact]].
