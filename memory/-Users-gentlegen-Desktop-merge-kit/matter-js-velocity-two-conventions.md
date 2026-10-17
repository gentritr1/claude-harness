---
name: matter-js-velocity-two-conventions
description: matter-js body.velocity means per-substep mid-step but per-baseDelta after Engine.update — one converter for both is a silent 2x error
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:08:47.580Z
---

In matter-js 0.20, `body.velocity` has **two different units depending on when you read it**:

- Inside a `collisionStart` handler (Engine.js:79, before `solveVelocity`): displacement per the
  **actual substep** that just ran, and pre-collision-response.
- After `Engine.update` returns: displacement per **`Common._baseDelta` (1/60 s)**, because the
  update ends with `Engine._bodiesUpdateVelocities` (Engine.js:109) which renormalises via
  `timeScale = _baseDelta / body.deltaTime`.

`Body.setVelocity` / `Body.setAngularVelocity` always take **per-baseDelta**.

**Why:** with `substeps: 2` a single shared converter is wrong by exactly 2× in one of the two
contexts. Symptom is not a crash — the game just feels wrong, and impact damping thresholds fire
at the wrong speeds. My first version of `physicsTune.ts` had this bug.

**How to apply:** `matterToWorldVelocity(v)` for settled reads, `matterMidStepToWorldVelocity(v, substepSeconds)`
for reads inside collision handlers; `midStepToBaseDelta()` for angular. Never assert a conversion
against arithmetic — assert it against a running engine (`packages/merge-shell/test/physicsTune.test.ts`
measures fall time and does a velocity round-trip; that suite is what caught it).

Related: [[merge-kit-physics-port-seam]]
