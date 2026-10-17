---
name: arrows-release-signing
description: "Local release signing — credentials/ keystore, withUploadKeystore plugin, Desktop release kit pattern from Rowflare"
metadata: 
  node_type: memory
  type: project
  originSessionId: 030fc7e5-cf70-4c1f-bc34-ef34df6c38e9
---

Arrows 1.0.0 release kit built + signed locally 2026-07-18 (same pattern as
block-blaster/Rowflare at ~/Desktop/Rowflare-release-1.0.0, but signing survives
prebuild via a config plugin instead of manual gradle re-editing).

- `credentials/` (gitignored): `arrows-upload.keystore` (alias arrows-upload, CN=Arrows,
  SHA-256 24f7fa0b…7a50f8) + `keystore.properties` (ARROWS_UPLOAD_* keys).
- `plugins/withUploadKeystore.js` injects the release signingConfig at prebuild;
  falls back to debug keystore when credentials/ absent.
- `credentials.backup.enc` at repo root: AES-256-CBC/PBKDF2-600k tar of credentials/;
  passphrase in the Desktop kit's KEYSTORE-PRIVATE folder (user told to move it to a
  password manager). Restore cmd in docs/KEYSTORE_BACKUP.md.
- Kit: ~/Desktop/Arrows-release-1.0.0/ (1-TEST apk 90MB / 2-STORE aab 63MB / KEYSTORE-PRIVATE).
- Build cmd: `npx expo prebuild -p android --clean` (then write android/local.properties
  with sdk.dir) + `./gradlew :app:assembleRelease :app:bundleRelease` (~13 min).
- Release APK smoke-tested on emulator-5554: boots (embedded bundle, no Metro),
  LevelPlay inits, rewarded test ad plays. See [[levelplay-ads]].
- Play: user must enroll in Play App Signing on first upload; EAS flow in RELEASE.md is
  now an alternative path, not the one used.
- 2026-07-18 R8 enabled (Play flagged "App optimization Low"): expo-build-properties
  `enableMinifyInReleaseBuilds` + `enableShrinkResourcesInReleaseBuilds` + extraProguardRules
  keeping com.ironsource.** / com.unity3d.** (ad SDK ships no on-disk consumer rules).
  versionCode bumped to 2 — Play burns a versionCode per uploaded bundle, rebuilds must bump.
  mapping.txt (35MB) goes in kit 2-STORE/ for Play's ReTrace upload. Ads verified working
  under R8. SCAR: mid-test "Killing ... remove task" app deaths with empty crash buffer were
  the USER closing the app on the shared emulator — ask the user before deep-diving
  unexplained device-state changes on a machine they're actively using.
- 2026-07-18 permission strip (kit rebuilt same day): expo-audio's plugin defaults added
  RECORD_AUDIO + FOREGROUND_SERVICE(_MEDIA_PLAYBACK), and the Expo template manifest adds
  SYSTEM_ALERT_WINDOW — all removed via `["expo-audio", {recordAudioAndroid:false,
  enableBackgroundPlayback:false}]` + `android.blockedPermissions` in app.json.
  aapt-verified gone from the shipped APK; audio playback + rewarded ad re-verified on
  emulator. Rule: aapt-dump the release APK's permissions before any store submission —
  plugin defaults add sensitive permissions silently.
