---
name: ui-thread-sampling-needs-runonjs
description: useFrameCallback silently never ticks in a component that re-renders every frame — its callback identity must be memoised
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T15:03:01.965Z
---

**Root cause, confirmed by reading reanimated's source.** `useFrameCallback` registers via
`useEffect(..., [callback, autostart])` (`react-native-reanimated/lib/module/hook/useFrameCallback.js`).
The Babel plugin builds a **fresh worklet closure object on every render**, so in any component that
re-renders every frame — e.g. a game screen redrawing at 60 fps — `callback` identity changes 60×/s,
the frame callback is unregistered and re-registered continuously, and **it never survives long
enough to tick**.

Fix: `useCallback` with only stable deps (shared values are stable refs), then pass that to
`useFrameCallback`. Same defence `useJsFrameLoop` already used — it holds its callback in a ref
precisely so a re-render cannot restart the loop.

**Why this was expensive: the symptom looks like a data-storage bug.** merge-kit's UI-thread frame
sampler reported 1229 samples of an expected ~1800, then 0, then 1 — depending on how many frames
registration happened to survive. I misdiagnosed it twice (first "JS-side reads of shared values lose
UI-side writes", then "in-place mutation of a shared value doesn't persist"), rewrote the storage
layer twice, and neither was the problem. Both wrong diagnoses were plausible and both were written
into code comments before being disproved.

**Detection rules:**
- For any cross-thread or callback-driven sampling, **reconcile sample count against
  `windowSeconds × expectedRate` before trusting a single percentile.** A plausible-looking p95 over
  1 sample is what this bug produces. That reconciliation check is the only reason it was caught.
- When a metric comes back partial/empty, suspect **registration/lifecycle before storage** —
  especially any hook whose effect deps include a function created during render.
- A worklet or RN-render change closes only with a sim/device run. tsc, vitest and a Metro bundle all
  passed happily through all three broken versions. To confirm the *transform* is fine (as opposed to
  the wiring), bundle with `npx expo export --no-bytecode` and grep for `__workletHash`.

Related: [[perf-gates-need-jitter-and-resolution-tolerance]], [[v02-spike-outcome-matter-js-fails-120]]
