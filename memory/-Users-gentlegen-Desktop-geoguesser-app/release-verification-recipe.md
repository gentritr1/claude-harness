---
name: release-verification-recipe
description: How to build+verify a Geo Guesser Android release (emulator gotchas included)
metadata: 
  node_type: memory
  type: project
  originSessionId: a067363c-ba38-4d38-8a74-8d9d95ca553e
  modified: 2026-08-08T13:34:37.788Z
---

Release recipe that worked for v1.2.2 (2026-08-08):
1. Bump `versionName`/`versionCode` in BOTH `android/app/build.gradle` and `app.json` (android/ is checked in; app.json alone does nothing without prebuild).
2. Build: `android/gradlew -p android assembleRelease` (APK for testing) and `bundleRelease` (AAB for Play), with `GRADLE_USER_HOME=./.gradle-user-home`, `NODE_ENV=production`. Signed automatically via `credentials/keystore.properties` + `upload-keystore.jks`.
3. Verify the token/env made it in: `unzip` the APK/AAB, `strings assets/index.android.bundle | grep 28648898844710860` (Hermes bytecode — plain `grep` on the file fails, use `strings`).
4. Emulator gotchas: Pixel_8_Pro AVD is ~full (INSTALL_FAILED_INSUFFICIENT_STORAGE); use Pixel_6_Pro. Toggle nav mode with `adb shell cmd overlay enable com.android.internal.systemui.navbar.threebutton` (or `...navbar.gestural`). ALWAYS smoke-test bottom-anchored UI in 3-button mode: the app is edge-to-edge (targetSdk 36), and v1.2.2 fixed buttons hidden under the bar by adding `useSafeAreaInsets().bottom` in GuessMap/StreetView/RoundResult/GameSummary — new bottom-anchored UI must do the same.
5. Full verification = start screen without token warning → Play → real street imagery loads → drop pin → score screen. Related: [[mapillary-token-baked-in]].
