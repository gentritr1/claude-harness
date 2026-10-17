---
name: core-emits-failwarning-on-change-only
description: "merge-core emits failWarning only on change, so an intents-only HUD freezes graceProgress and the warning flash never ramps"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:09:44.885Z
---

`merge-core`'s tick emits the `failWarning` intent only on the tick the warning turns **on or off**
(`tickFailLine` returns `warningChanged`, not a per-tick value). A shell HUD driven purely by intents
therefore latches `graceProgress` at whatever it was when the warning appeared — the fail-line flash
never ramps as the grace burns down.

**Why:** this is invisible to core unit tests (the core is behaving as designed) and invisible to a
diff review. It surfaced only because a runtime test asserted the *ramp*, not the intent.

**How to apply:** the runtime projects continuous values off core state each tick —
`view.graceProgress = state.failLine.sustainedSeconds / rules.fail.graceSeconds`. Reading core state
is not a rules decision; the core already computed it. Expect the same pattern for any other
change-only intent (`dangerLevel` is emitted with a 0.001 dead-band, so treat it the same way if
smooth easing is ever needed).

Regression guard: "ramps graceProgress every tick, not only when the warning appears" in
`packages/merge-shell/test/gameRuntime.test.ts`.

Related: [[merge-kit-physics-port-seam]]
