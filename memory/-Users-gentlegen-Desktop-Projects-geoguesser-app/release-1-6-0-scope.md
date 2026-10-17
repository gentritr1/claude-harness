---
name: release-1-6-0-scope
description: "Owner rulings 2026-10-10 for store release 1.6.0 (13) — which 13 flags default ON, which 6 stay OFF and why, defaults accepted, real-ads APK + AAB"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-10T15:13:04.650Z
---

**Owner asked 2026-10-10** for a store AAB plus a release APK with real ads (the owner's choice) and NO QA panel, with the features ON by default.

**Branches.** The next-level stack was merged into feat/next-level as a9e49c7. Release work is on branch release-1.6.0 (scratchpad worktree rel-160). Tag v1.6.0 locally; never push.

**Scope.** "All 19 ON" was not shippable: the audit found daily inert without a manifest, rewarded_ads with no code, and many PROVISIONAL timings. The owner chose the ready set, plus a TODO with a plan for the rest:
- **ON (13):** reveal_motion, scoring_v2, modes, share_grid, challenge_code, passport, art_v2, motion_v2, sun_catch_up, sound, hint_tiers, new_day_slide, globe_drag.
- **OFF (6):** daily, reminders, today_fill_wipe, rewarded_ads, ump_consent (the owner keeps it OFF until the AdMob GDPR message and policy are ready), interstitial_after_summary.
- The owner accepted the code defaults for TIMED_ROUND_MS, NEAR_WEIGHT, DAY_EPOCH (frozen by this build) and the copy.

**Before the store build:**
- measure the PROVISIONAL timings on the emulator: WebView ready timeouts (the release guard blocks on them), the A8 reveal budget, banner mount, the spin deadline, and sound with motion ON and OFF;
- then a full emulator trip with the ready set ON.

**Ads.** Sign intel is a score penalty, not an ad, so no AdMob unit is needed. A rewarded hint would be future work.

Related: [[living-globe-resume-point]], [[commit-before-release-build]], [[gradle-bundle-ignores-expo-public-env]].
