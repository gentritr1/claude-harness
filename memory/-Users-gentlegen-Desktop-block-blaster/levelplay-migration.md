---
name: levelplay-migration
description: "2026-07-17 migrated ads from direct Unity Ads SDK to Unity LevelPlay 9.5.0 — dashboard is platform.ironsrc.com, credentials are App Key + Ad Unit ID"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4741634e-f8cf-4547-b358-69c71e789c65
---

On 2026-07-17 the Android rewarded-ad path moved from direct Unity Ads
(`com.unity3d.ads:unity-ads:4.19.0`, Game ID + placement) to Unity LevelPlay
(`com.unity3d.ads-mediation:mediation-sdk:9.5.0`, App Key + Rewarded Ad Unit ID)
because Unity de-prioritized direct integration after 2026-04-01. Module lives in
`modules/levelplay-ads/`; env vars are `EXPO_PUBLIC_LEVELPLAY_ANDROID_APP_KEY`
and `EXPO_PUBLIC_LEVELPLAY_ANDROID_REWARDED_AD_UNIT_ID`.

Gotchas that cost time / were nearly wrong:
- LevelPlay AAR bundles its own manifest activities + provider — do NOT copy the
  docs' manual manifest snippet into the module manifest (merger duplicates).
- LevelPlay AAR declares `ACCESS_ADSERVICES_ATTRIBUTION`; `app.json`
  deliberately strips it (contextual-ads privacy posture). Rewarded fill with the
  permission absent is UNVERIFIED until the signed-device §7 matrix.
- Reward name/amount are defined on the dashboard ad unit, not per show call —
  the `rewardKey` param is dead weight kept for API compatibility; keep dashboard
  reward amount at 1.
- Verification pattern that worked: download the AAR from Maven Central and
  `javap` the classes before writing Java against docs — the docs' snippets were
  correct but the package paths (`com.unity3d.mediation[.rewarded]`) were only
  confirmed by the jar listing.
- The docs claim onAdRewarded fires before onAdClosed; client adds a 2s grace
  window after close for late rewards anyway ([[shell-node-version]] still
  applies for all verify runs).

Device verification 2026-07-17 (minified release APK on Pixel_8_Pro emulator,
app key 273ad018d):
- VERIFIED: SDK 9.5.0 inits with correct app key; GDPR/CCPA/is_deviceid_optout
  privacy metadata applied (seen in logcat); load attempt runs; no-fill returns
  fail-closed — "Ad unavailable" dialog, NO reward, helpers unchanged, no crash,
  clean recovery. ProGuard/minify did NOT strip LevelPlay classes.
- UNVERIFIED (blocked): a real ad rendering + onAdRewarded → +1 helper. Fresh
  app has no fill.
- GOTCHA: our privacy config sets is_deviceid_optout=true (contextual ads), so
  LevelPlay reports advertisingIdType=UUID with a random id (e.g.
  4f0bc588-...), NOT the device's real GAID. So registering the real GAID under
  Test Devices will NEVER match. To get test fill, register the UUID LevelPlay
  actually reports (grep logcat "advertisingId=") AND set up at least one
  Mediation network/instance for the rewarded ad unit; or temporarily disable
  optout for a test build so the real GAID matches.

2026-07-18 clean cold-restart trace (test device 4f0bc588 registered w/
ironSource Bidding): logcat shows the full correct round-trip —
  LevelPlayRewardedAd <init> adUnitId: is5ip5vqegmu1q1g  (correct ad unit)
  loadAd()
  onAdLoadFailed errorCode:509 "Mediation No fill"
So App Key, Ad Unit ID, and test-device UUID are ALL correct and the SDK reaches
mediation — the only blocker is error 509 = no fillable instance for the ad unit.
Fix is dashboard-side: Setup → Instances must have an ironSource instance
attached to Helper_Rewarded (a traditional/non-bidding ironSource instance gives
the most reliable test fill), then wait ~30-60min for server config propagation.
Reward-grant path (onAdRewarded → +1 helper) remains device-UNVERIFIED until an
instance fills. Everything up to fill is VERIFIED on minified release.
