---
name: local-android-build-traps
description: Local gradle builds need ANDROID_HOME exported; piping gradle through tail masks BUILD FAILED; always check APK mtime before adb install
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 233ace99-1005-4f16-b3d0-c413c72eb3ae
  modified: 2026-07-27T19:53:05.880Z
---

Two traps hit on 2026-07-18 while device-verifying the ads privacy fix:

1. Non-interactive shells have no ANDROID_HOME → `./gradlew assembleRelease` fails at configuration with "SDK location not found". Fix: `export ANDROID_HOME=/Users/gentlegen/Library/Android/sdk` before gradle. (Companion to [[shell-node-version]] — the shell also lacks nvm Node 20.)

2. `./gradlew ... | tail -5` reports the pipe's exit code, so a BUILD FAILED surfaced as "exit 0" and a 2-hour-stale APK got installed on the emulator, silently re-running the pre-fix build as if it were the fix.

**Why:** both failures were invisible in the happy-path output; the giveaway was the APK mtime (17:11) vs wall clock (19:15).

**How to apply:** run gradle with output to a log file and echo `$?` separately; before `adb install`, `ls -la` the APK and require mtime newer than the source edit; after install, confirm the new behavior marker in logcat (e.g. absence of `is_deviceid_optout`) rather than trusting the install step.

Three more, 2026-07-27, device-testing the AdMob rewarded path:

3. **`expo run:android --device` wants the AVD name, not the adb serial.** Passing
   `emulator-5554` fails with "Could not find device with name". Omit `--device`
   entirely when exactly one emulator is attached.

4. **A backgrounded command's "exit code 0" is not the command's exit code.** The
   task notification reported success while the log's last line was
   `CommandError: Could not find device`. Same family as trap 2 — always read the
   log tail, never trust the wrapper's status. See
   [[gradle-false-green-cached-task]].

5. **The long-lived emulators fill up.** `Pixel_8_Pro` hit
   `INSTALL_FAILED_INSUFFICIENT_STORAGE` at 93% of a 5.8G `/data` — this project's
   own dead package IDs (`com.rowflare.game`, `com.blockblast.game`) plus sibling
   projects were still installed. `adb uninstall` the stale predecessors before
   assuming a build problem; `adb shell df -h /data` tells you in one command.
   Note ~443M free was still not enough for an 84M debug APK — Android needs
   several times the APK size for extraction.
