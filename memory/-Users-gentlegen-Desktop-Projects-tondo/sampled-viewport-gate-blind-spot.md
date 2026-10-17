---
name: sampled-viewport-gate-blind-spot
description: A geometry gate that samples a few viewports passes while unsampled common sizes overlap — measure the whole band, and distrust a single-digit clearance
metadata:
  type: feedback
---

Tondo's `seat-plaque-gap` group sampled 1024x768, 1280x800 and 1440x900 and was
green. Measuring the whole band found **1366x768 at -2.5px and 1280x740 at
-5.9px** — 1366x768 is one of the commonest laptop sizes shipped. The gate could
not see them because only 1440x900 had real room; 1280x800's +1.4px was the tell
and I had read it as "passing".

**Why:** a sampled gate proves the sampled points, nothing between them. A
clearance in the single-digit pixels is not a pass, it is the edge of a band
whose shape has not been measured.

**How to apply:**
- A measured clearance under ~5px means *sweep the band* (both axes, ~40px
  steps) before trusting any gate that samples it. Find where the sign flips.
- Scope the fix to the measured band plus margin, and name the first
  comfortable row that proves the boundary (here 1280x860 at +8.7 sits outside
  `max-height: 850px`).
- The same family as [[2026-09-16-round-boundary]]: the bug lives in the state
  or size nobody sampled. Compressed/bar-open states are the *easy* case; the
  resting state is where geometry breaks.
- A remedy that works on phones may not transfer: the phone band gets clip +
  lift, this band gets clip only, because headroom here (8-11px) is smaller
  than the lift (~16.6px) and the avatar would clip through the stage top.
