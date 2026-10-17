---
name: gradle-bundle-ignores-expo-public-env
description: Gradle reuses a stale JS bundle across builds with different EXPO_PUBLIC_* values — a store AAB could ship test ads + the QA panel; fixed with env inputs + an artifact build stamp
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T15:02:35.728Z
---

**Reproduced 2026-09-16 (unit A2).** `:app:createBundleReleaseJsAndAssets` only tracks JS source files
as inputs — not `EXPO_PUBLIC_*` values and not `.env` files. Build a QA APK with
`EXPO_PUBLIC_FORCE_TEST_ADS=1 EXPO_PUBLIC_QA_PANEL=1`, then run a store build with both unset and no
source edit in between: the task reports `UP-TO-DATE` and the store artifact carries the QA bundle
(identical sha256). A store AAB could ship **test ads (zero revenue) and the QA panel** to players.

Fixed in `android/app/build.gradle`: a digest of `EXPO_PUBLIC_*`/`NODE_ENV`/`BABEL_ENV`/`EXPO_NO_DOTENV`
and the production `.env*` files is a declared input of that task. Second layer: a build stamp
(`src/config/buildInfo.ts`, `geoguesser-build;test-ads=…;qa-panel=…;`) survives into the Hermes bytecode,
and both `scripts/build-aab.sh` and `scripts/build-qa-apk.sh` read it out of the finished artifact and
**delete** a wrong one. Booleans alone leave no trace in bytecode, which is why the stamp is a string.
Both scripts also `unset CI` — with `CI` set, Expo skips Metro's `--reset-cache`.

**Why:** the owner's build flow now has two build kinds from one checkout; this bug makes the second
build silently inherit the first's switches.

**How to apply:** after ANY change to how `EXPO_PUBLIC_*` values reach a build, re-run the A→F
sequence: QA build, then an unset build, and confirm `expoBundleEnvironmentSha256` "has changed" and the
artifact stamp flips. Never trust a store artifact's switches without reading its stamp:
`unzip -p <artifact> assets/index.android.bundle | strings -a | grep geoguesser-build` (for an AAB the
path is `base/assets/index.android.bundle`).

Other device-QA facts from the same unit:
- `adb shell setprop log.tag.Ads VERBOSE` makes the Ads SDK log every request URL — the reliable way to
  prove only `ca-app-pub-3940256099942544/*` test units are requested.
- The emulator's `-tcpdump` is blind on API 36 (2 DNS packets). Route traffic through a logging proxy:
  `adb shell settings put global http_proxy 10.0.2.2:<port>` (and `settings delete global http_proxy`).
- `uiautomator dump` silently leaves a stale file on screens with endless animations (the home hero).
- `expo-file-system` merges READ/WRITE_EXTERNAL_STORAGE into the manifest; removing them needs
  `tools:node="remove"`, deleting the lines is not enough.
- Disk on this Mac was at 100% (1.4 GiB free) on 2026-09-16. `.gradle-user-home` (4.5 GB, used by
  build-aab.sh) and `~/.gradle` (4.0 GB) largely duplicate each other. The `tablet_api36` AVD was deleted
  to free space; recreate with
  `avdmanager create avd -n tablet_api36 -k "system-images;android-36;google_apis_playstore_ps16k;arm64-v8a" -d medium_tablet`.

Related: [[large-screen-landscape-is-live]], [[commit-before-release-build]], [[geoguesser-release-build-steps]]
