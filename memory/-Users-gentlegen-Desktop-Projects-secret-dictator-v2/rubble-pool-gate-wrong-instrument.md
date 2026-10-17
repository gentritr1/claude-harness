---
name: rubble-pool-gate-wrong-instrument
description: "A \"beam preserved\" gate written as warm-pixel count inside a fixed platform mask (±9 px) rejected the ambient-lift retune it was meant to allow; gates for lighting changes must measure luminance of the protected region, not classifier membership"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-06T18:10:31.258Z
---

On 2026-09-06 I specified the phase-3 trial retune's beam-preservation gate as "warm pixel count inside a fixed platform-top mask unchanged within the nine-pixel tolerance", reusing the tolerance from the asset-swap pair harness. Codex's stronger candidate (exploration-03: hemisphere ambient lifted, lantern intensity cut) saved about 1.3 percentage points of trial warm but lost 109–137 of 48,691 mask pixels to the HSL classifier's hue threshold at the pool's dim edge, and was rejected on that alone. The conservative candidate that passed lifted the ground by an amount nobody can see and funded nothing.

**Why:** the nine-pixel tolerance was measured for swaps that do not touch light. An ambient change moves every pixel's hue slightly, so classifier membership at region edges is the wrong statistic for "the beam still dominates". This is a variant of the §6 red flag "threshold compared with no allowance for measurement resolution": the resolution of a classifier-count gate under a global lighting change is hundreds of pixels, not nine.

**How to apply:** for lighting retunes, protect a region by (a) asserting the light's own settings unchanged in the live state table and (b) the region's mean luma not lower than before beyond measured jitter, with the classifier count recorded but not gated. Ask "what does this gate's resolution become under the change it is meant to permit?" before writing the tolerance. Related: [[rubble-pair-gate-resolution]], [[rubble-warm-budget-lives-in-dusk]].
