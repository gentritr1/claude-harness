---
name: levelplay-pending-approval
description: 2026-07-18 ironSource Ads account PENDING APPROVAL — no live fill until approved; only pre-approval ad path is a dashboard-registered test device (SDK testMode flag is deliberately inert)
metadata: 
  node_type: memory
  type: project
  originSessionId: 233ace99-1005-4f16-b3d0-c413c72eb3ae
---

As of 2026-07-18 the ironSource/LevelPlay Ads account for Rowflare (app key 273ad018d, rewarded ad unit is5ip5vqegmu1q1g "Helper_Rewarded") is **pending approval** — banner on platform.ironsrc.com. No production ad fill until approved; on device this surfaces as the generic "No ad is available right now" alert.

Key facts (all VERIFIED 2026-07-18 by APK inspection + code read):
- `RowflareLevelPlayAdsClient.java` intentionally ignores `testMode` — LevelPlay test ads come ONLY from dashboard-registered test devices (Setup → Test devices, needs the device's advertising ID). No SDK flag exists.
- Dashboard test devices (checked live 2026-07-18): 5 registered, but only "Rowflare Publish Emulator" and "Rowflare Emulator 2" have an ad network configured (ironSource Bidding, all formats). "Test Emulator", "Rowflare Emulator", "Pixel 7 emulator" have NO network selected → no test ads on those. No physical phone is registered. Mediation: 1 group "All Countries" with ironSource Bidding instance — structurally correct. Only ironSource Ads network is set up (27 others untouched).
- Release APK (`Rowflare-1.0.0-release.apk`) verified to contain both env values in the Hermes bundle, all ironSource/LevelPlay dex classes, and correct merged-manifest entries — the build is code-complete; "no ads" is dashboard-side.
- Release builds suppress LevelPlay error codes (`console.warn` is dev-gated in `rewardedAdsCore.ts`); diagnose on device via `adb logcat` filtered to ironSource/Unity tags.
- eas.json production profile outputs an **AAB**; the APK at repo root is a preview artifact, not the store submission artifact.

**2026-07-18 RESOLVED — fix device-verified.** Removed the hardcoded `configurePrivacyAsync(false,true,true)` (JS goes straight to init; native no longer requires privacy-before-init). A/B on emulator-5554 with release builds: pre-fix build → logcat `is_deviceid_optout=true` set → `errorCode:509 Mediation No fill` → "Ad unavailable" alert; post-fix build (APK 19:21) → no optout metadata → demo ad played full-screen → close → run continued (reward granted). Ads work even while the account is pending approval. Remaining store gates: account approval email, rest of checklist §7 matrix, AAB via eas production profile, app-ads.txt, Play declarations.

**2026-07-18 diagnosis update — pending approval is NOT the whole story.** Sibling project arrows-game (app key 27012eed5, same pending-approval account) served "ironSource Demo" test ads on an unregistered emulator the same day. The delta: Rowflare hardcodes `configurePrivacyAsync(false, true, true)` in `rewardedAdsCore.ts:54` → `setGDPRConsent(false)` + `setCCPA(true)` + `is_deviceid_optout=true`, while arrows sets no privacy restrictions. `is_deviceid_optout` blocks the SDK from reading the GAID (per ironSource regulation-advanced-settings docs), and dashboard test devices are matched BY advertising ID → registered test devices can never match → no test ads. This posture is deliberate (RELEASE_CHECKLIST.md §3 "contextual/non-personalized ads") but makes the §7 device matrix unrunnable as-is. Decision pending with user: gate the flags per build type vs relax posture.

Related: [[levelplay-migration]]
