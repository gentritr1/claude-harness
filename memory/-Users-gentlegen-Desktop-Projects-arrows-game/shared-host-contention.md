---
name: shared-host-contention
description: This Mac runs other Claude sessions (e.g. geoguesser-app) that boot emulators and eat disk mid-run; name the emulator explicitly and re-check df right before builds
metadata: 
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-16T15:15:25.705Z
---

Observed 2026-09-16 during next-level Phase 0: free disk fell 11 GB → 1.8 GB over ~2 h while
this session's agents were only building one APK/AAB. A separate Claude Code session in
`~/Desktop/Projects/geoguesser-app` was running at the same time; it booted AVD `Pixel_8_Pro`
on port 5580 with `-tcpdump` (from a boot script in that project's scratchpad), and AVD
`tablet_api36` disappeared without this session deleting it.

Owner-approved cleanup that session: removed repo `ios/` (gitignored), `~/.gradle/caches`,
AVD `Pixel_6_Pro` → 11 GB free. Remaining AVDs: `fleet_floor_api31` (this project) and
`Pixel_8_Pro` (geoguesser — do not touch).

**Why:** `adb devices` can list two emulators, so an unqualified `adb shell` or
`expo run:android` can hit the wrong one; and a `df` check done at the start of a long task is
stale by the time the build starts. Same failure class as the "something consumed ~4 GB while
idle" note in [[tap-forgiveness-and-verification-gaps]].

**How to apply:** always `adb -s emulator-5556` / `--device emulator-5556`; run `df -h /`
immediately before each native build (gate ≥5 GB; builds need ~4 GB); never delete outside the
repo without an explicit owner yes.

**2026-09-26 disk pattern:** each emulator task leaves ~150–300 MB of frames in the session scratchpad (t5..t12 = 1.7 GB) plus 3–16 superseded APKs (43 MB each) under artifacts/<TASK>/apk/; free disk fell to 117 MiB once while parallel agents ran. After committing each task, delete its superseded APKs (keep the installed one + release/baseline builds) and its scratchpad frame dirs. ~/Library/Caches and ~/.gradle regrow ~2–4 GB within a day of an owner-approved clear.

**2026-09-26 same-project collision (W2-09):** parallel subagents of ONE controller both drove emulator-5556 (another agent seeded level 109, `am start`, wm size 1080x2340) while W2-09 uninstalled/installed a repack — each killed the other's app and the other ran on W2-09's APK. Before any device step, watch `adb -s emulator-5556 logcat -v time | grep -E "Start proc .*com.danteb|Force stopping com.danteb|START u0.*com.danteb"` for foreign launches (monkey = LAUNCHER intent; `am start -n` = flg=0x10000000); controllers must grant the emulator to ONE agent at a time. Also: port 8097 may be held by another agent's web preview — use 8098.

**2026-09-27 cleanup mistake:** an emergency `find artifacts -name "*.mp4" -mtime +0 ! -path "*/owner/*" -delete` also deleted 8 owner-acceptance videos that tasks had named `owner-*.mp4` outside an `owner/` folder (POLISH-T5/T6/T9/T10/T12, W2-01). Rule: before deleting evidence, build the keep-list from the reports (`grep -rhoE "artifacts/[^ )]*\.(mp4|png)" docs/next-level/reports`) and exclude every referenced file and any `*owner*` name; prefer deleting raw frame dumps and build outputs first.

2026-09-28/29: `~/.gradle/caches` vanished twice between builds (not deleted by this session). A cold gradle release build re-downloads ~2.8 GB and writes ~4 GB into node_modules/*/android/{build,.cxx} — budget ~7 GB, not 5. Stopping the 6-day-old emulator took free disk from 3.5 to 14 GB (likely swap/purgeable released; cause not proven). Use a watchdog that pkills gradle under 500 MB; resume without `prebuild --clean` keeps the compiled natives.

**2026-09-29 orphaned wait loops:** 7 subagent background loops (`until ! pgrep -f "loopps.mjs"`, `"acceptance.sh"`, `"perf-ab-ff.sh"`) ran ~42 h after their targets finished — `pgrep -f NAME` matches the loop's own zsh command line, so it never goes false. Controller could not kill them (classifier: other session's workload); owner had to stop them. Briefs must say: wait on a PID (`while kill -0 $PID`) or a sentinel file, never `pgrep -f <name>` from a shell whose command line contains the name.

**2026-09-29 Node drift:** the Bash tool's shell suddenly resolved `node` to nvm v14.19.3 (nvm default alias still v20.19.4). `expo prebuild` printed "Node.js (v14.19.3) is outdated" but exited 0, gradle then failed "Cannot convert '' to File", and the build script copied the PREVIOUS AAB under the new vc name (same sha256). Rules: build scripts pin `export PATH=$HOME/.nvm/versions/node/v20.19.4/bin:$PATH`, check `android/app/build.gradle` exists after prebuild, exit on gradle failure before copying, and compare the output sha against the previous build.

**2026-10-01 disk root cause:** 170 GB (as counted by du) in `/var/folders/<user>/X/com.google.Chrome.code_sign_clone` (139 clones, Chrome bug) — but deleting them freed only a few GB (APFS clones share blocks). The real wins were 4 old iOS simulator runtimes (~33 GB via `xcrun simctl runtime delete <id>`; the multi-id form only deleted the first id). Free space 324 MB → 21 GB. Remaining big items: ~/.codex/sessions 9.4 GB, staged macOS update ~18 GB in Preboot, CoreSimulator caches 20 GB.
