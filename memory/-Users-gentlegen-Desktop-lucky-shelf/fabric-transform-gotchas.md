---
name: fabric-transform-gotchas
description: "Fabric (newArchEnabled) sprite-vanish class: separate scaleX/scaleY collapse the view, AND reanimated with*() return values used in arithmetic = NaN transform — both invisible to tsc/vitest, sim screenshot required"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3bb5b22f-cf63-495e-be5e-4f3f9b194708
---

**Scar (2026-07-11):** the cascade item sprites all went INVISIBLE (only the count chips
rendered) after a "receive squash" animation split a sprite's single `{ scale }` transform into
separate `{ scaleX }` + `{ scaleY }` entries. Root cause: `app.json` has **`newArchEnabled: true`**
(Fabric), and on Fabric separate scale axes compose badly / collapse the view. It was the ONLY
`scaleX`/`scaleY` usage in the whole codebase (everything else uses uniform `scale`), so it was an
unproven pattern here. Fix (`62e3588`): revert to a single `{ scale }`; express any "squash" as a
uniform bump (grow + spring back), not a non-uniform scaleX/scaleY.

**Detection/rule:** for animated transforms in this app, prefer a single uniform `scale`. If a
non-uniform effect is truly needed, verify it ON THE iOS SIMULATOR first ([[ios-ui-verify-on-simulator]])
— tsc + vitest pass regardless (no RN runtime in tests), so a broken transform ships silently.
Also: the bug looked "combo-specific" to the human (that's just when they watched the cascade), but
it was in EVERY CascadeItem's style worklet — when a symptom seems scoped, confirm the code path
before assuming the scope.

**Scar 2 (2026-07-11, same symptom, SECOND cause):** the `62e3588` fix didn't bring the sprites
back — the combo-hop commit (`8e4c467`) had ALSO broken them, differently: it changed the
open-window lift from `translateY: withTiming(...)` (valid — animation object assigned directly to
a style prop) to `translateY: activeLift - hopY * hop.value` where `activeLift = withTiming(...)`.
**Reanimated `with*()` returns an animation OBJECT, not a number** — arithmetic on it is `NaN`
every frame, and Fabric drops a view with a NaN transform. So every cascade sprite was invisible
statically, on every screen, badges-only (the user's Day-1 screenshot). Fix (`6c037c3`): drive the
lift through its own `useSharedValue` + `withTiming` in an effect, then do numeric math on
`.value` in the worklet.

**Rule:** a `with*()` result may ONLY be (a) assigned to `sharedValue.value`, (b) assigned
directly to a style/transform prop, or (c) returned from `useDerivedValue`. The moment it appears
in an arithmetic expression, it's NaN. Sweep: `grep -rn "with(Timing|Spring|Delay|Sequence)"` and
check each non-`.value =` hit. Note `src/juice/motion.ts` helpers `spring()`/`timing()` are typed
`: number` — a lie that invites this exact bug (unused as of 2026-07-11).

**Meta-scar:** the first fix commit claimed "fixed" without a sim screenshot — two independent
sprite-killers had landed back-to-back, and removing one looked complete from the diff. Any
sprite/transform fix here closes ONLY with a fresh `xcrun simctl io booted screenshot` showing the
sprites (works headlessly, no computer-use needed).

Related: [[cascade-juice-plan]] [[text-centering-pattern]] (transform-override RN gotcha)
