---
name: admob-migration
description: 2026-07-27 replaced LevelPlay with Google AdMob inside the existing custom Expo module; play-services-ads pinned at 25.2.0 by a Kotlin metadata ceiling
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T19:52:41.646Z
---

2026-07-27: Blockrow (renamed from Rowflare — see [[rowflare-to-blockrow-rename]])
moved rewarded ads from Unity LevelPlay to **Google AdMob**, at the user's
explicit direction after being re-told that AdMob payouts are unavailable for
Kosovo. They reaffirmed, so it was built; **the payout-country wall is unresolved
and will surface at AdMob account setup, not in code.** Supersedes
[[levelplay-migration]] and [[levelplay-pending-approval]].

**Approach chosen and why.** Kept the existing custom Expo module and swapped the
SDK inside it (`modules/levelplay-ads` → `modules/admob-ads`, package
`expo.modules.blockrowadmobads`, native name `BlockrowAdMobAds`) rather than
adopting `react-native-google-mobile-ads`. That library's own support table marks
**Android Full Screen Ads as "To-Do"** for Turbo Native Modules — and Android is
this app's only ad platform while Expo SDK 56 makes the New Architecture
mandatory. The Expo Modules API is natively New-Arch clean, so the in-house
module avoids the legacy-interop gamble entirely. `rewardedAdsCore.ts` and its
tests survived the swap unchanged in shape.

**Key API/behaviour deltas from LevelPlay:**
- No runtime app key. The AdMob **application ID** lives in the merged manifest
  as `com.google.android.gms.ads.APPLICATION_ID`; `/android` is prebuild-generated
  so it is injected by `plugins/withAndroidAdMob.js`, which falls back to a
  placeholder ID when the env var is unset (ads stay disabled; game still builds).
- Env vars renamed `EXPO_PUBLIC_LEVELPLAY_*` → `EXPO_PUBLIC_ADMOB_ANDROID_APP_ID`
  and `..._REWARDED_AD_UNIT_ID`. **App ID uses `~`, ad unit uses `/`** — trivially
  swapped, so `release-preflight.mjs` now shape-checks both and rejects Google's
  reserved test publisher `ca-app-pub-3940256099942544`.
- `testMode` is no longer inert (it was under LevelPlay). The native client
  substitutes Google's reserved test rewarded unit whenever `__DEV__`, because
  self-generated impressions on a live unit are invalid traffic and a documented
  suspension cause.
- Reward ordering is simpler: AdMob guarantees `onUserEarnedReward` before
  `onAdDismissedFullScreenContent`, so LevelPlay's 10s reward-grace hack is gone.
- Consent is now real: UMP (`user-messaging-platform:4.0.0`) is gathered inside
  `initializeAsync` before `MobileAds.initialize`, with a 10s timeout so a stalled
  consent request cannot wedge init. `configurePrivacyAsync` is deleted.

**Verified 2026-07-27 (executed, not inferred):** `npm run verify` green
(40 tests); `expo prebuild --clean` + `:app:assembleRelease` BUILD SUCCESSFUL with
R8/minify on; built APK inspected with aapt2 → `package=com.blockrow.game`,
`application-label=Blockrow`, AdMob `APPLICATION_ID` meta-data present.
**DEVICE-VERIFIED 2026-07-27 on Pixel_8_Pro emulator (API 36, Google APIs)**, with
the user's real AdMob IDs in `.env` (publisher `ca-app-pub-9813…`, Poland account
— the earlier Kosovo payout blocker is moot). Full chain observed by screenshot:
Shuffle x3 → exhausted → "Watch Ad · +1" appears → tap → "Loading…" → Google test
rewarded creative plays full-screen ("Test Ad" watermark) → "Reward granted" →
close → **Shuffle x1** credited → spend it → **"Shuffle Used"**, no second ad
offered (`MAX_REWARDED_USES_PER_HELPER = 1` holds). logcat confirmed UMP ran,
`MobileAds` initialized, and "This request is sent from a test device" — the
`__DEV__` → test-unit substitution works, so no live-unit impressions were made.

**Still UNVERIFIED:** live-unit fill (needs the AdMob app approved), the UMP
consent form itself (emulator is not in the EEA, so no form was presented), and
the RN-Modal-vs-UMP-dialog z-order in `PrivacySupportModal`.
