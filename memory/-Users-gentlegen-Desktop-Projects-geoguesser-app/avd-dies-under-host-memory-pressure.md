---
name: avd-dies-under-host-memory-pressure
description: "The Pixel_8_Pro AVD's system_server watchdog-dies when another session builds — a quiet host at boot is not enough; gate each run on no foreign Gradle"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T03:18:07.274Z
---

On 2026-10-02 the Pixel_8_Pro AVD's system_server died twice in one day: a watchdog reboot loop for the whole of B2-5's
first device window (host swap 10.8/12 GB, disk 99 %), and again at 12:31 mid-measurement (swap 12-14.6 GB, load up
to 69, another project's Gradle build running). Each time installs failed or the measurement had to be abandoned, and
the stale emulator proxy came back after the restart.

On 2026-10-07 it died a third time (phone session, A1 run 1). The boot-time check was fine: swap 4.3/5 GB, no other
AVD. Then another session started an arrows-game `expo prebuild` + Gradle build; swap climbed to 6.5/8 GB, qemu fell to
375 MB resident (guest RAM paged out), `android.io` blocked 304 s, Watchdog killed system_server, and every app,
ours included, logged DeadSystemException. So the threshold is not a swap number: **any foreign Gradle build during a
run is enough.** The owner chose "wait for it to finish": watch for no gradlew/prebuild/jest + load < 12 + swap < 5 GB,
sustained 2 min, before each run.

On 2026-10-08 it died 4 more times, and every crash came during an `adb install` of a 33-45 MB QA APK. The host has 8
cores (6 performance), so load 25-45 from Spotlight (mds/mdworker) and other sessions is 4-5× oversubscribed. The crash
buffer showed `am_kill networkstack ... bg anr`, then system_server's own "Lost network stack" FATAL: the guest's
install-time dexopt starved the network stack into an ANR, and system_server took itself down. The low-memory killer
was not involved. Installs worked at load ~11 the same night. My own clone and scratchpad were not being indexed
(mdfind 0). An install also left the device with no `settings` service, so a scale restore silently failed. Always
re-check the animator scales after a crash.

**Why:** the emulator gets starved when other projects and agent sessions fill the host; nothing in this repo causes it.

**How to apply:** before a device run longer than a few minutes, read `sysctl vm.swapusage`, the load average, and
system_server's ELAPSED (`adb shell ps -A -o PID,ELAPSED,NAME`); log them through the run, and treat an ELAPSED drop as
"stop, report BLOCKED". If swap is above ~10 GB, ask the owner to close other heavy work first rather than burning a
45-minute run. Re-clear the proxy after any restart ([[avd-stale-global-proxy]]).
