---
name: visual-calibration-briefs-lesson
description: "Visual-polish briefs must spec on-screen proportions and layered structure, not multipliers on tiny constants — vessel V1 shipped correct-but-invisible"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2f83faef-f3fc-4cd6-85b7-1dcbadcd9448
---

Chamber vessel presence V1 (2026-07-03, branch `post-mvp/7-chamber-vessel-presence`): Codex implemented my brief exactly, and the result still read as a hairline — user: "doesn't quite look premium." The brief specced relative multipliers ("0.022 → 0.055", "alpha ×1.5") on values that were already near-invisible, so 2.5× of nothing was still nothing.

**Why:** for visual weight, correctness of implementation ≠ the intended look. Multiplier specs inherit the old calibration's error.

**How to apply:** in any visual-weight brief, specify (1) target size as a **proportion of a reference dimension** (e.g. "rail structure ≈ 4–5% of chamber inner width"), (2) **layered structure** for glow (hot near-white core ~0.9 alpha + tight glow ~0.4 + wide faint halo ~0.1 — a single soft line never reads premium), (3) dark-on-dark alpha floor: anything under ~0.3 alpha in a dark scene on a dark backdrop is invisible, glass must read via bright sheen not dark fill, and (4) require a **screenshot at a reference aspect as the acceptance artifact**, then expect one calibration iteration. Also: hold merges on visual briefs until the user accepts the screenshot — EditMode green means nothing for looks. Related: [[reviewing-codex-output]], [[document-learnings-as-we-go]].

**OUTCOME:** vessel arc V1→V3.1 SHIPPED via PR #38 (squash `19393d5`, 2026-07-04) — user-accepted screenshot, 264/264 incl. previously-unrun candy tests. The additive+bloom unlock was the decisive fix; the calibration lessons below remain the playbook for future visual briefs.

**V3 root cause (2026-07-03, the deeper layer):** two calibration rounds underperformed because the project renders with glow OFF — DefaultVolumeProfile Bloom intensity 0, no camera in Main.unity enables post-processing, all chamber sprites on default alpha blend. Neon/premium-glow looks REQUIRE additive blending + bloom; check the render pipeline BEFORE tuning sprite constants (constants can't exceed what the renderer can express). V3 spec in the vessel brief: `PlanetDrop/AdditiveSprite` shader for emissive layers, `renderPostProcessing = true` on gameplay camera, Bloom 0.65/threshold 0.75; bake/RT cameras must keep post OFF (thumbnails), expect to halve alphas after.
