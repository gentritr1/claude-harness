---
name: v02-spike-outcome-matter-js-fails-120
description: "v0.2 spike result (2026-07-25) — matter-js on Hermes crosses the 60fps budget at ~97 bodies, not 120; the wall is Hermes's missing JIT"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:32:32.542Z
---

**Outcome of the v0.2 kill-switch spike, 2026-07-25.** Release build, iPhone 16 Pro **simulator**
(inadmissible for a formal pass; physical-device run still outstanding).

matter-js physics cost is linear at **0.181 ms per body per 60 Hz step** at `substeps: 2`:

| bodies | 40 | 60 | 80 | 100 | 120 |
|---|---|---|---|---|---|
| physics p50 ms/step | 6.11 | 10.04 | 13.70 | 17.30 | 20.61 |
| JS thread p50 ms | 16.67 | 16.67 | 16.14 | 89.17 | 106.14 |

- Physics alone crosses the 16.7 ms budget at **~97 bodies**, with nothing left for rendering.
- The JS thread holds a locked 60 fps through **80 bodies**, then collapses: past the crossing point
  each frame owes more fixed steps than it can afford and the accumulator pins at its 5-step
  catch-up cap (5 × 20.6 = 103 ms ≈ observed 106 ms). Those numbers describe the spiral, not
  per-body cost — quote the physics-per-step curve for engine decisions.
- UI thread held 60 fps throughout. This is a **JS-thread** failure.
- Same scenario under node/V8: 1.81 ms/step — **11× cheaper**. The wall is Hermes having no JIT, not
  matter-js's algorithm. That is exactly the gap a native/WASM engine closes.

**Before writing any Rapier code**, test the cheaper hypothesis: `substeps: 2` is a 2× multiplier on
the dominant cost and exists *only* to prevent tunneling (peak fall speed 31.7 units/s = 1.65 ×
tier-1 radius per frame). At `substeps: 1`, 120 bodies projects to ~10.3 ms/step, which fits. So ask:
can tunneling be fixed without doubling solver work — bigger tier-1 radius, lower gravity with the
cooldown re-derived to hold §10's `cooldown ≈ 0.5 × fall time`, or a harder speed clamp?

Related: [[merge-kit-physics-port-seam]], [[spike-scenarios-need-rules-paced-drops]]
