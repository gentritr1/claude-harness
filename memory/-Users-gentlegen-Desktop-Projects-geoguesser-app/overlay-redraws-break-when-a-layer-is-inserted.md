---
name: overlay-redraws-break-when-a-layer-is-inserted
description: "GlobeOverlay redraws the coast over the Globe; ART-4a put the night band above the Globe's coast, so the overlay's unclipped coast brightened every night-side coastline"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T00:33:34.624Z
---

ART-4a review (2026-10-08): the reward overlay re-paints a copy of a base layer (the coast) above the Globe. That was invisible until ART-4a inserted a new layer (the night caps) between the Globe's coast and the overlay. After that, the copy painted undarkened coasts across the whole night side (×1.47 luminance, the whole post-daily visit). 4225 tests and 68 proven re-pins passed: the pins proved the TREE diff, not what it composites to.

**Why:** a "redraw above" overlay is only correct while nothing sits between the original and the copy. Any new layer breaks it silently, and tree-hash pins cannot see compositing.

**How to apply:** pattern → detection rule → brief update. A unit that inserts a layer into a stack that some overlay duplicates → grep for overlays that redraw base paths (GlobeOverlay, reveal layers) and composite reveal vs static → briefs that add a Globe layer must name every overlay and require an in-clip, self-contained overlay or a raster comparison (rsvg-convert is on the host). Related: [[mockup-code-is-not-trusted-math]].
