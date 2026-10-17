---
name: merge-kit-rn-spinoff
description: "New project — reusable RN merge-game factory extracted from Planet Drop; lives at ~/Desktop/merge-kit; Opus 5 executes, Fable specs/reviews"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7a4e5eb0-f270-46e7-8db0-750996f56e56
  modified: 2026-07-25T12:31:13.096Z
---

Remote: git@github.com:SnaxxTech/merge-kit.git (pushed 2026-07-25; I own git/push, agents don't push).

Started 2026-07-25. User wants Planet Drop's merge-tier design reused as a factory for
skinned React Native apps (cakes first). Decision: rebuild-with-a-spec, NOT a code port —
C#/physics don't transfer; the portable value is tuning constants + rules + EditMode test
scenarios. Plan at `/Users/gentlegen/Desktop/merge-kit/PLAN.md`.

Architecture: pnpm monorepo — `merge-core` (pure TS deterministic reducer, zero deps),
`merge-shell` (RN: matter-js + react-native-skia), `theme-contract`, `apps/<skin>`.
Extensibility exam: app #2 must ship touching only `apps/` + theme pack.

Version plan: v0.1 spec+core DONE & APPROVED 2026-07-25 (Opus 5 executed; 88 vitest tests,
zero-dep core, spec numbers diffed vs sources; checksum gate deliberately not ported) →
v0.2 greybox + 120-bodies-at-60fps physics spike (RN kill-switch) → v0.3 feel parity
(eyeball gate) → v1.0 cakes app → v1.1 second theme (architecture pass/fail).

Model split: this is the second Opus-execution experiment after [[model-split-ui-experiment]].
Planet Drop repo stays read-only reference. Unity-engine-scaled physics constants
(gravity 42, dampings) are ratios-only spec — never copy as absolutes into matter-js.
