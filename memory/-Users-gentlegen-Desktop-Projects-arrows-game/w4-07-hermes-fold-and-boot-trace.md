---
name: w4-07-hermes-fold-and-boot-trace
description: W4-07 (2026-09-25) collection fold costs on Hermes, menu start-up burst, and a reusable boot-trace recipe (su seeding, monotonic alignment)
metadata:
  type: project
---
- Hermes (API 31 emulator, release bundle): `shapeNameForLevel` ~26 us and ~6.6 KB garbage per level (5000 levels = 128 ms one-shot, 33 MB alloc, GC only 2-3 ms). V8 is ~5x cheaper and ~30x less alloc: never size JS work from node.
- Menu's first ~1.6 s after mount share the CPU with ad-SDK start-up (AdMob/WebView preloads): work started there got preempted (5 ms chunks stretched to 29-56 ms; JS rAF max 55-405 vs 31-43 off). Deferring 2 s fixed it. First-2-s null spread on this emulator is huge (JS max 30-674 ms): interleave arms, n>=5.
- RN Android `setTimeout(0)` fires on the next frame, so rAF->setTimeout(0) chunking = one chunk per 2 frames.
- Boot-trace recipe (artifacts/W4-07/scripts): release APK is not debuggable but `adb -s emulator-5556 shell su 0 sqlite3 /data/data/com.danteb.arrows/databases/RKStorage` works (table catalystLocalStorage; chown u0_a233 + restorecon after); `performance.now()` == CLOCK_MONOTONIC ms == `logcat -v monotonic` == framestats IntendedVsync/1e6, so windows align exactly; framestats holds ~2 s, dump every ~1.3 s without reset.
- zsh does not word-split `$var`/`set -- $w`: use `${=var}` or run bash (a mutation check silently ran 0 tests).
