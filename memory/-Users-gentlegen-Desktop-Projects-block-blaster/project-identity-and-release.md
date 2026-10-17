---
name: project-identity-and-release
description: "Block Destroy identity, signing, versioning, and local .aab build path"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2051cf29-c6f2-47e3-8fbd-76df141b5684
  modified: 2026-08-31T21:51:15.826Z
---

Block Destroy (package `com.blockrow.game`, npm name `blockrow`, formerly "Rowflare") — Expo SDK 56 block puzzle. Android release signing lives in `credentials/keystore.properties` + `credentials/rowflare-upload.keystore` (gradle picks release signing only when the properties file exists — `android/app/build.gradle` ~line 100). Version is duplicated in `app.json` (`expo.android.versionCode`) AND `android/app/build.gradle` — bump both. As of 2026-08-31: versionName 1.0.0, versionCode 3. Local .aab: `cd android && ./gradlew bundleRelease` (EXPO_PUBLIC_* env is inlined at JS bundle time, so .env must be right BEFORE building). See [[env-fail-closed-ads]].

Gradle in non-interactive shells here has no `ANDROID_HOME`; prefix builds with `ANDROID_HOME="$HOME/Library/Android/sdk"` (no `android/local.properties` exists).
