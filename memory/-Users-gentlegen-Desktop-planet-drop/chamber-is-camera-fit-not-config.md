---
name: chamber-is-camera-fit-not-config
description: "the runtime play chamber is camera/aspect-fit, NOT the GameConfig chamberSize.x / failLineY — those config values are dead at runtime"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0b5a9fa8-484c-49c8-883a-5ce1cc257310
---

**Gotcha (found 2026-06-27 via the playtest harness):** the live play chamber is sized by `GameplayController.FitCameraToChamber()`, not by `GameConfig`. At runtime:
- **Width** = derived from SCREEN ASPECT (`visibleWidth * (1 - reserves)`), clamped to `[ChamberWidthMin, ChamberWidthMax]`. `gameConfig.chamberSize.x` (=5) is NOT the real width.
- **Fail line** = `bounds.yMax - FailLineMarginFromTop` (near the top). `gameConfig.failLineY` (=4.3) is NOT the real fail line.
- Height = `chamberSize.y` (=12) is used.

So `gameConfig.GetChamberBounds(...)` and `GetFailLineY(...)` return values that DO NOT match the actual runtime chamber. Anything that resizes/reasons about the chamber must read the LIVE `chamber.InnerBounds` / `chamber.FailLineY`, never the config getters.

**Bit us in:** [[agent-playtest-harness]] Phase 3 chamber-width experiment sized arms from the config getters → narrower box + lower fail line than the real game → baseline collapsed to ~146 drops/tier 8 vs the real ~350 drops/tier 9.3. Fix = base experiment bounds on captured live `chamber.InnerBounds`/`FailLineY`; express width arms as a SCALE on the real width. Acceptance: baseline arm must reproduce Phase 2 (~tier 9.3 / ~350 drops / ~11k).

**Also corrected a reasoning error:** earlier I explained "tier 12 unreachable" via "chamber is 5 wide, two tier-11 bodies (diam 4.04) can't fit." The 5 was the dead config width, not the real width. The EMPIRICAL finding (tier 12 = 0, ceiling ~9, measured in the real chamber in Phase 1/2) still holds — but the width-specific mechanism was overstated. Re-derive any geometry from the real camera-fit width. See [[reviewing-codex-output]] / [[document-learnings-as-we-go]].
