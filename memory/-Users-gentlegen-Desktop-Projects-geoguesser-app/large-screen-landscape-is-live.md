---
name: large-screen-landscape-is-live
description: "The app already runs forced-landscape on Android 16 tablets (portrait lock ignored) — it does not break, but the guess map shows ~3 copies of the world"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-09T19:00:10.860Z
---

Verified 2026-09-09 on a `medium_tablet` AVD (Android 16, SDK 36, 2560x1600 @ 320dpi =
**1280 x 800 dp**), running a real release APK.

`dumpsys window displays` for the app's window:

```
sw800dp w1280dp h800dp 320dpi xlrg land
bounds=[0,0][2560,1600]
```

**`land`** — Android 16 ignores `android:screenOrientation="portrait"` at >=600dp for
apps targeting SDK 36 (this app targets 36; see
[[android-sdk-versions-come-from-rn-catalog]]). There is no compat opt-out property in
the manifest. **This is already shipping**, not a future risk.

**It does not break.** Home, loading, panorama and the guess sheet all render correctly;
the wide panorama is arguably better than portrait. `GuessMap`'s
`sheetHeight = height * 0.85` was the predicted failure and is fine.

Three real defects, none fatal:
1. **Guess map repeated the world (1.77 copies at 1280 px). FIXED 2026-09-09** —
   zoom/minZoom now `max(0.5, log2(containerWidth / 512))`, recomputed on resize.
   Measured before/after in a browser: phone 390 px unchanged at 0.5; tablet 1280 px
   went 1.77 -> 1.00 copies. **MapLibre's world is `512 * 2^zoom` CSS px — measure it
   with `map.project([180,0]).x - map.project([-180,0]).x` rather than assuming a tile
   size; I first assumed 256 and got the copy count wrong by 2x.**
2. **Footer links clip in the error state.** `isCompact = height < 700 || width < 350`
   (`StartScreen.tsx:54`) — tablet landscape is 800dp so compact never triggers, but
   800dp cannot fit the full layout plus an error card. Phone landscape (~360dp) does
   trigger compact; the tablet falls in the gap.
3. 728x90 banner sits in black letterboxing.

**How to apply:** to re-run this check, recreate the AVD (deleted 2026-09-16 for disk space; see [[gradle-bundle-ignores-expo-public-env]]) then `emulator -avd tablet_api36` (AVD created
2026-09-09 from `system-images;android-36;google_apis_playstore_ps16k;arm64-v8a`;
delete with `avdmanager delete avd -n tablet_api36`). **Always build with
`EXPO_PUBLIC_FORCE_TEST_ADS=1` before installing on an emulator** — the default `.env`
has it empty, so a release build requests REAL ad units, which is invalid traffic
against the AdMob account. Confirm from logcat that only `ca-app-pub-3940256099942544/*`
(Google test units) are requested, and look for the "Test Ad" badge on the banner.

Emulator networking on this Mac is flaky: the guest came up with no `wlan0` and
"Active default network: none" twice, and recovered on its own. A dead network makes the
app say *"Could not find street-level imagery"* — a coverage message for a connectivity
failure, confirming that audit finding on-device.

Related: [[verify-webview-maps-without-a-device]], [[dont-pipe-long-builds-through-tail]]
