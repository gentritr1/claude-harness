---
name: rubble-warm-budget-lives-in-dusk
description: "The frozen-scene pair harness showed facade albedo has zero trial-warm cost (no warm pool reaches the facades at trial), so the per-asset zero-allowance rule constrains dusk, and a cold plaster hue is not required by the trial ceiling"
metadata: 
  node_type: memory
  type: project
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-06T09:35:42.929Z
---

Measured 2026-09-06 on the first phase-2 facade (scripts/measure-facade-warm-pair.mjs, reproduced by the orchestrator): swapping all seven facades between the 73a154c GLB and the candidate at three frozen trial instants changed trial warm by 0 scene pixels and -3 HUD pixels. The same swap changed dusk warm by about -11.6 points (18.9% → 5.1%) because the old warm plaster caught the dusk key light and the new cool grey plaster does not. Trial's tight ceiling margin (about 0.15 to 0.3 points) comes from the dais pool and lanterns, which phase 5 retunes, not from facade albedo.

**Why:** the brief's "0.00 pp positive trial allowance per asset" is satisfiable by any facade hue, so it must not be read as a reason to desaturate plaster. The dusk mood frame measures 15.9% warm with the same classifier; the game's dusk after this facade is 5.1%, which is the real drift to watch. See [[rubble-floor-threshold-unmeasured]] for the earlier threshold lesson.

**How to apply:** when a phase-2 or phase-4 asset comes in cold, ask whether the pair harness at trial actually shows a cost before accepting the hue; judge dusk against the 15.9% mood-frame figure and expect phase 5 to recover dusk warmth through light on the plaster, which only works if the plaster albedo is warm enough to catch it.
