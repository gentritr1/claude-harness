---
name: tap-forgiveness-and-verification-gaps
description: "2026-09-08 input/feel revision (nearest-ink hit test, heart-once ledger, blocker flash, press preview, momentum) — what was verified where, and the disk blocker that stopped device + perf runs"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e3eac07-acf0-4073-aef8-01f415e172cd
  modified: 2026-09-07T22:16:52.645Z
---

**What changed (2026-09-08, uncommitted at time of writing):** `src/ui/hitTest.ts`
(nearest-ink within 22 pt, seam tiebreak toward an exitable arrow),
`src/ui/tapRules.ts` (a blocked arrow costs a heart once per level; ghost-tap
window 350 ms on just-freed cells), `BoardLogic.blockerOf`, blocker flash +
directional bump + touch-down press preview in both Skia and SVG layers
(`feedbackCurves.ts`), pan momentum via `withDecay` + rubber band, 72 pt edge
pad once zoomed past the viewport, max zoom = max(3.5x fit, 64 pt/cell),
pan slop 12 pt, tap maxDuration 900 ms, new `'nudge'` feedback event
(haptic only) in both native feedback modules.

**Why the harness had to change:** `scripts/perf/android/benchmark.mjs`
validation tapped cell (35,19) three times and asserted "Out of hearts"; with
the ledger only the first tap charges, so it now taps three distinct blocked
arrows ((35,19), (31,14), (30,21) on level 3827). Any future rule about
repeated taps must be checked against that validation step first.

**Evidence provenance:** tap logic VERIFIED on the web preview (real
mouse clicks: nearest snap from outside the shape, blocked bump + blocker
flash, second tap on the same blocked arrow kept the heart, press preview
renders and "what is highlighted fires"). On the API 31 emulator the harness validation
VERIFIED: cell-centre taps remove arrows through the new hit test, and three
distinct blocked arrows drain three hearts. UNVERIFIED anywhere: momentum /
rubber band feel, pinch focal-follow, ghost-tap timing, Android/iOS haptic
for 'nudge', and the absolute frame gate (see perf outcome). Hit-test cost measured in node: ~3 us per tap
on the 250-arrow board at fit zoom (`tsx` microbench), so the JS cost is
noise; the unmeasured part is the two extra React renders per touch
(press start / press end) on the Skia overlay.

**Perf outcome (2026-09-08, `docs/perf-tap-forgiveness-ab-2026-09-08.md`):**
A/B/A on the harness, five samples in one emulator session. No regression:
revision ALL p95 23.9-25.1 ms vs HEAD 37.4-37.6 (both HEAD reruns agree),
memory flat. BUT the unchanged HEAD measured 3x worse than the 2026-09-01
record because the Mac was loaded (Avast daemon ~97% CPU, ANECompilerService,
load 5-7): absolute gates are unevaluable on a loaded machine; only paired
differences count. The 120-frame `exit` phase swung 21.0 vs 36.1 ms between
identical-APK runs, i.e. ~15 ms resolution: never quote an exit delta
smaller than that from one run. Press preview was then delayed to 64 ms
(`PRESS_PREVIEW_DELAY_MS`) so instant taps skip the extra React commit +
Skia draw; that was a mechanism fix, not a measured one.

**Harness gotchas:** `--skip-prebuild` fails "Release APK is not
shell-profileable" because the `<profileable>` tag comes from
`plugins/withPerfProfileable.js` only when `ARROWS_PERF_BUILD=1` at prebuild;
let the harness prebuild (android/ is gitignored + generated). The emulator
must already be running on port 5556: `emulator -avd fleet_floor_api31 -port
5556 -gpu host -no-snapshot-load`. Validation runs BEFORE the build, so boot
first. Save APKs and use `--skip-build --apk` for cheap replication runs.

**Disk:** the Mac had 6.7 GB free; a 4-ABI `gradlew assembleDebug` filled it
(ENOSPC). Freed by deleting `node_modules/*/android/build`,
`android/{app/,}build`, and (user-approved) the Pixel_8_Pro AVD userdata
(8.7 GB). The harness build is arm64-only and fits in ~4 GB. Something else on
this Mac consumed ~4 GB in 10 minutes while idle; check `df` before builds
(same class of failure as the 2026-09-01 iOS attempt in
[[perf-architecture-and-evidence]]).

**Web preview gotchas:** `expo start --web` failed before this session because
`unity-levelplay-mediation` is statically bundled on web; `metro.config.js`
now aliases it to `scripts/emptyModule.js` for web only. Port 8081 is often
held by another project (geoguesser-app); `.claude/launch.json` pins 8097.

**Deliberately NOT done (candidates):** touch-offset up-shift (needs tap-log
data before picking a number), double-tap zoom (delays single taps in a tap
game), auto-zoom on dense boards at level start (the shape is the level's
identity), hint-triggered focus untouched.
