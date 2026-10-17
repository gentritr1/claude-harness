---
name: merge-spawn-escape-bug
description: Rapid/chain merges eject planets through the 0.35-thick chamber floor — solver depenetration from unclamped merge-spawn overlap; 3-layer fix briefed 2026-07-03
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f83faef-f3fc-4cd6-85b7-1dcbadcd9448
---

User-reported (2026-07-03): during merge chains, planets sometimes fall through the container. Root cause chain (verified in code, not speculation): `MergeResolver.CompleteMerge` spawns the next-tier body at the raw parent midpoint with no radius clamp → bottom merges start up to ~0.3 into the floor (radius grows per tier, e.g. 2.02→2.3) → solver depenetration squeezes neighbors → chamber boxes are only 0.35 thick, so a center pushed 0.175 past the inner face crosses the midplane and gets ejected OUT the far side. Continuous CD does not prevent this (it guards swept motion, not overlapped-start ejection). Convergence (0.12s colliders-off) deepens neighbor overlap; world gravity 42 amplifies. No containment/recovery code existed.

**Why:** thin-box containers + spawn-overlap is a generic physics trap (applies to Stormhaven too — [[stormhaven-brief-carries-planetdrop-lessons]]): any "replace two bodies with a bigger one" mechanic must clamp the spawn to fit, and container colliders should be much thicker than the largest single-step depenetration.

**How to apply:** 3-layer fix MERGED to main 2026-07-03 via PR #35 (squash `4d29a00`): A) `MergeResolver.ClampSpawnPosition` on live `chamber.InnerBounds` inside `CompleteMerge` after nextTier resolves (MergedEvent uses the clamped position); B) physics boxes thickened to 2.0 via collider offset, inner faces + 0.35 glass visuals unchanged; C) `ContainmentSweep` (1 Hz, Playing-only, 0.5 grace below floor) warps escapees back and logs `body_escaped` analytics. Confirmation signal: `body_escaped` should now never appear in console/harness logs — if it does, layers A/B didn't fully close the hole ([[open-verification-gaps]]).
