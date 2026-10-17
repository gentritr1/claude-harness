---
name: apps-contain-unity-ads
description: Arrows APK = Unity Ads/LevelPlay + AD_ID; Rowflare renamed Blockrow and switched to Google AdMob-only (2026-07-27); legal pages must disclose ads
metadata: 
  node_type: memory
  type: project
  originSessionId: ebf2c9b8-c60a-4285-89fa-82ae22905d6e
  modified: 2026-07-27T21:19:23.571Z
---

Verified 2026-07-18 via `aapt2 dump permissions` on the actual release APKs (`~/Desktop/Arrows-release-1.0.0/1-TEST/Arrows-1.0.0.apk`, same for Rowflare):

- Both apps bundle **Unity Ads SDK + Unity LevelPlay (ironSource) mediation** (`assets/iads/*`, `META-INF/com/unity3d/ads-mediation/*`, `play-services-ads-identifier`).
- Both request `com.google.android.gms.permission.AD_ID`, INTERNET, ACCESS_NETWORK_STATE.
- Packages: Arrows = `com.danteb.arrows` (Unity engine game), Rowflare = `com.rowflare.game` (**React Native app, NOT Unity** — user-confirmed 2026-07-19; the unity3d/iads files in its APK are just the LevelPlay/Unity Ads SDK). Rowflare is a utility ("focused mobile utility"), legal appKind = "mobile app".
- Arrows ALSO requests `RECORD_AUDIO`, `SYSTEM_ALERT_WINDOW`, FOREGROUND_SERVICE(+MEDIA_PLAYBACK), READ/WRITE_EXTERNAL_STORAGE (maxSdk 32) — likely leftover Unity plugin permissions. **Play review risk; strip before submission** (open item, app-side, not website-side).

**STALE for Rowflare as of 2026-07-27** — user reports the app is now named **Blockrow** and its only ad provider is **Google AdMob** (consent via Google UMP; in-app "Ad Privacy Choices" in the Privacy & Support screen). Legal pages updated accordingly; the APK facts above were never re-verified against a post-switch build. Arrows is unchanged (still Unity Ads/LevelPlay). See [[block-destroy-legal-2026-07-27]].

**Why:** the original site privacy policy claimed "no ads SDKs / no advertising identifiers / data never leaves device" — false, and a Play Data Safety contradiction → rejection/takedown risk. Policy rewritten 2026-07-18 to disclose Unity Ads.

**How to apply:** any future legal-page edit or Data Safety form must match APK reality — re-run `aapt2 dump permissions` on the current release build first, never trust site copy. Play Data Safety form must declare: ads yes, device/other IDs (advertising ID) collected by SDK, shared with ad partners.
