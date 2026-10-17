---
name: android-sdk-versions-come-from-rn-catalog
description: "targetSdk/compileSdk resolve to 36 from React Native's version catalog, not from Expo's \"35\" fallback — read the build log, never the Kotlin default"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-09T18:23:05.213Z
---

The app **already targets API 36** and satisfies Play's requirement. Verified
2026-09-09 by running Gradle, not by reading config:

```
$ cd android && ./gradlew :app:dependencies
[ExpoRootProject] Using the following versions:
  - buildTools:  36.0.0
  - compileSdk:  36
  - targetSdk:   36
```

Merged release manifest (`app/build/intermediates/merged_manifests/release/
processReleaseManifest/AndroidManifest.xml`) carries
`<uses-sdk android:minSdkVersion="24" android:targetSdkVersion="36" />`.

**How resolution actually works.** `android/build.gradle` has **no `ext` block** and
`android/gradle.properties` has no SDK versions, so it looks like nothing sets them.
It resolves like this: `settings.gradle` calls `expoAutolinking.useExpoVersionCatalog()`,
which builds the `expoLibs` catalog from `react-native/gradle/libs.versions.toml`
(RN 0.81.5 declares `targetSdk = "36"`, `compileSdk = "36"`, `buildTools = "36.0.0"`).
`ExpoRootProjectPlugin.kt:30` then does
`getVersionOrDefault("targetSdk", "35")` — the `"35"` is only a **fallback that never
fires**.

To override, set Gradle properties in `android/gradle.properties` — Expo maps
`android.targetSdkVersion` → `targetSdk`, `android.compileSdkVersion` → `compileSdk`,
`android.buildToolsVersion` → `buildTools`. Do **not** run `expo prebuild`: `android/`
is tracked (43 files) and hand-edited (AdMob `tools:replace`, signing config pointing at
`../credentials/upload-keystore.jks`).

**Why this memory exists:** I claimed the app targeted 35 and could not be uploaded to
Play, and built a whole mandatory "compliance release" on it. Both I and an independent
critic agent read the Kotlin *fallback* as the *resolved value*. One `./gradlew` run
(100 s) disproved two rounds of source-reading.

**How to apply:** for any Gradle-derived value — SDK levels, versionCode, AGP, NDK —
read it from the `[ExpoRootProject]` build log or the merged manifest. Never report a
resolved version from a default in plugin source. Toolchain present on this machine:
android-36 platform, build-tools 36.0.0, AGP 8.11.0, Java 17.

Related: [[dont-pipe-long-builds-through-tail]], [[geoguesser-release-build-steps]],
[[playerstore-wipes-profile-on-slow-read]]
