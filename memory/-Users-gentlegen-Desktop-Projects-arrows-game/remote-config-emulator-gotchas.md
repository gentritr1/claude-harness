---
name: remote-config-emulator-gotchas
description: W6-02 (2026-09-17) - release builds block http://localhost fetch (cleartext); RN Android revalidates with 304; how the kill-switch flip was built and observed
metadata:
  node_type: memory
  type: project
---
- A release APK (targetSdk 36, no usesCleartextTraffic) rejects fetch to http://localhost via adb reverse: `UnknownServiceException: CLEARTEXT communication to localhost not permitted`. A JS repack cannot fix it; W6-02 used a temp edit of gitignored android/app/src/main/AndroidManifest.xml + incremental `:app:assembleRelease` (2m12s after deleting android/app/build), restored the manifest with cmp, then deleted android/app/build so the diagnostic APK can't be reused by mistake.
- RN Android networking sent conditional requests: python http.server logged 304 on later cold starts while JS still read the body (an HTTP cache exists) - matters for W6-03 caching claims.
- `process.env.EXPO_PUBLIC_X ?? ''` IS inlined (bundle grep count 1), despite a docs summary claiming otherwise. Stop the gradle daemon before a build that depends on EXPO_PUBLIC_ env, and grep the bundle.
- Native marker for LevelPlay contact without app logs: logcat `LevelPlaySDK: API: tb c - LevelPlay.init() appkey:`.
- emulator-5556 is often NOT running at task start; another session boots Pixel_8_Pro on 5554 mid-run.
