---
name: hermes-bundle-not-greppable
description: Grepping a release Hermes bundle for a string returns 0 even when the string is present — verify env inlining through app behaviour instead
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T21:52:38.831Z
---

2026-07-27, verifying that `EXPO_PUBLIC_ADMOB_*` values reached the release
bundle: `unzip -p app-release.apk assets/index.android.bundle | grep ca-app-pub`
returned **0 matches**, which looked like proof that ads were silently dead in
production. It was wrong.

**The disproof that saved it:** grepping the same bundle for `"Watch Ad"` — a
string that unquestionably exists in the app — also returned 0. The instrument
was broken, not the build. Hermes bytecode (`index.android.bundle`, magic
`c61fbc03`) does not store literals as plain contiguous ASCII, so `grep`/`strings`
find nothing regardless of what is actually in there.

A prior memory ([[levelplay-pending-approval]]) claimed a release APK "verified
to contain both env values in the Hermes bundle". Treat that claim as suspect —
the same method would have produced a false negative, so whatever confirmed it
was probably not this grep.

**How to actually verify env inlining in a release build:** find a piece of UI
that only renders when the env value is present, install the release APK, and
look for it. Here `canShowRewardedHelperAds()` requires both the app ID and the
rewarded unit ID, and it gates the "Watch Ad · +1" affordance — so seeing that
button in a release build proves the values reached the bundle, and costs
**zero ad impressions** because you never tap it. That last part matters: loading
a live unit from an unregistered emulator is invalid traffic.

**Rule:** before believing a negative grep, run the same grep for a control
string you know is present. A search that cannot find the control has proved
nothing. Generalises well beyond Hermes — see [[gradle-false-green-cached-task]]
for the same "the check didn't actually run" failure in Gradle.
