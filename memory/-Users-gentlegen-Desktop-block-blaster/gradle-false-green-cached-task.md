---
name: gradle-false-green-cached-task
description: Bumping a gradle dependency version and re-running the compile task reports success from cache — a bad version looks green without --rerun-tasks
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T19:11:47.689Z
---

2026-07-27, bisecting `play-services-ads` versions on Blockrow: editing the
version string in `build.gradle` and re-running
`gradlew :admob-ads:compileDebugKotlin` returned **exit 0 for 25.3.0**, which was
false. The task was satisfied from cache/UP-TO-DATE rather than recompiling
against the newly resolved classpath. I reported "25.3.0 works" and only caught it
because the subsequent full `:app:assembleRelease` failed on
`:admob-ads:compileReleaseKotlin` with the very error the targeted run had
"passed". The true ceiling is **25.2.0**.

**Why:** Gradle's up-to-date checks did not treat the swapped dependency as an
input change for that invocation, so the compiler never ran and the exit code
described nothing.

**How to apply:** When bisecting or bumping a native dependency version, always
pass `--rerun-tasks` (or clean the module's build dir) between candidates, and
confirm the winner with a full `:app:assembleRelease` rather than a targeted
compile task. Treat any green from a task whose *inputs you just edited by hand*
as suspect until it recompiles. This is the gradle instance of the standing rule
that a passing check must be shown to exercise the changed path —
see also [[local-android-build-traps]].

Concrete ceiling recorded: `play-services-ads` 25.3.0+ ships **Kotlin 2.3.0
binary metadata**; Expo SDK 56's Kotlin **2.1.0** compiler rejects it
("Module was compiled with an incompatible version of Kotlin"). Raising the pin
requires a Kotlin toolchain bump first. See [[admob-migration]].
