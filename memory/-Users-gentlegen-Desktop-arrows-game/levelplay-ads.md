---
name: levelplay-ads
description: "LevelPlay ads state — unity-levelplay-mediation 9.2.0, verified on emulator 2026-07-18, account pending approval"
metadata: 
  node_type: memory
  type: project
  originSessionId: 030fc7e5-cf70-4c1f-bc34-ef34df6c38e9
---

LevelPlay (ironSource) ads integrated and device-verified 2026-07-18.

- Package: `unity-levelplay-mediation@^9.2.0` (native SDK 9.4.0). The old `ironsource-mediation` is deprecated on npm; 9.x removed `withLegacyAdFormats`/`AdFormat` from init.
- Keys in `src/ui/ads.tsx`: app key 27012eed5, interstitial tme2lh9p1pkvk1bl, rewarded smim4g4z79173hcw (same as Unity build; dashboard app "arrows game").
- `plugins/withLevelPlay.js` config plugin injects 3 play-services gradle deps (appset 16.0.2, ads-identifier 18.0.1, basement 18.3.0) into app/build.gradle at prebuild — required by the 9.x README, not bundled by the lib.
- ironSource ACCOUNT WAS PENDING APPROVAL at verify time — test ads ("ironSource Demo" video) serve anyway; real fill/revenue needs approval. Re-check dashboard before release.
- Verified end-to-end on emulator-5554 (Pixel API 31): init success → interstitial isAdReady=true → rewarded test video shown via in-game hint button → onAdRewarded + onAdClosed(earned=true) → hint applied on board. Interstitial SHOW path not yet eyeballed (only load/ready) — same callback mechanism as rewarded; verify after 2 finished games when convenient.
- `LevelPlay.launchTestSuite()` exported as `launchAdTestSuite()` in ads.tsx, enabled via `is_test_suite` metadata in __DEV__ only; not wired to UI.
- See [[levelplay-init-race]] and [[emulator-metro-port-gotcha]] for the two scars found during review.
