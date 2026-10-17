---
name: merge-kit-physics-port-seam
description: "merge-kit's physics fallback insurance — one interface, one adapter, one swap point, enforced by a test not a comment"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:09:37.897Z
---

merge-kit's v0.2 fallback plan against matter-js failing the 120-bodies-at-60-fps gate:

- `packages/merge-shell/src/physics/PhysicsPort.ts` — the whole interface. World units, **Y-up**,
  origin at camera centre, velocities in units/second (matter-js is Y-down and per-step; the adapter
  converts).
- `packages/merge-shell/src/physics/matterAdapter.ts` — **the only file allowed to import matter-js**.
- `packages/merge-shell/src/physics/createPhysics.ts` — the swap point apps call. No app names an
  adapter.
- `packages/merge-shell/test/seam.test.ts` — enforces all of the above by scanning sources, plus
  "no React in anything the spike measures" and "no hardcoded 4.3 / chamberSize".
- `packages/merge-shell/test/gameRuntime.test.ts` — runs the entire game loop against a **fake port**,
  so the insurance is demonstrated, not asserted.

**Why:** a comment saying "don't import matter-js here" decays; a test doesn't. And a fake-port test
suite means swapping to Rapier is provably a one-file change.

**How to apply:** anything engine-specific (matter's `slop`, `Resolver._restingThresh`, its
millisecond deltas, its 40:1 world scale) stays behind the adapter. If a rule or a feel value needs
to reach the app, it goes through `PhysicsPort`/`PhysicsTune`, not through a matter import.

Related: [[matter-js-velocity-two-conventions]], [[core-emits-failwarning-on-change-only]]
