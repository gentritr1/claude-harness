---
name: w4-11-store-review-gotchas
description: W4-11 (2026-09-26) store-review ask - emulator Play is a stub (review bind fails), expo-store-review 57.0.3 isAvailableAsync = Play package present, star spring mass 4 wobbles to ~4.2 s, zsh one-word flag set caught by bundle proof, gradle --no-daemon JVM hang
metadata:
  type: project
---
- emulator-5556's com.android.vending is a stub (versionName 1.8, 0 accounts): PlayCore logs `ReviewService : requestInAppReview` then `Failed to bind` (BIND_IN_APP_REVIEW_SERVICE not found); requestReview rejects in 8-80 ms. The Play card is UNVERIFIED-DEVICE until an internal-test-track install on a phone. That PlayCore line is a good positive-control detector for "the call happened".
- expo-store-review 57.0.3 Android `isAvailableAsync` = "com.android.vending installed", not "Android 5+" as the v57 docs say; requestReview resolves only after launchReviewFlow completes (read StoreReviewModule.kt).
- Reanimated 4 withSpring defaults mass 4: the win-panel stars (damping 11, stiffness 260) visibly wobble until ~mount+4.2 s (screenrecord diff). Any "after the celebration" timing must use that, not the 590 ms last-star start.
- Third zsh no-word-split hit: `repack.sh $CAP` passed the whole flag set as ONE arg -> ADMOB_TEST_ADS not '1' -> owner units in bundle; prove-bundle caught it before install. Keep flag sets in a file and `read -r -a` in bash. macOS bash 3.2 has no `mapfile`.
- build-final.sh gradle `--no-daemon` JVM stayed alive ~24 min after BUILD SUCCESSFUL (APK already written); SIGTERM its wrapper/GradleMain/kotlin-daemon children. First gradle build after the cache clear took 9m51s.
- Perf driver artifacts/W4-11/scripts/w411-clear.mjs: CAPTURE_DIAG markers + Play by coords (menu never idles at scale 1) + fit-camera solver with per-batch "N left" guard; once saw 57/60 left before any scripted tap (cause unknown) and aborted cleanly.
