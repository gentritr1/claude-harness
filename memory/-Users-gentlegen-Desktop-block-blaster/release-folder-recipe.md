---
name: release-folder-recipe
description: "How the Desktop release + Play listing folders are built for this publisher (mirrors the Arrows convention), including the scripts that regenerate the art"
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T20:38:13.984Z
---

2026-07-27: built `~/Desktop/Block-Destroy-release-1.0.0` and
`~/Desktop/Google-Play-Block-Destroy-Listing`, mirroring the publisher's
existing `Arrows-release-1.0.0` / `Google-Play-Arrows-Listing` convention.

**Release folder:** `README.txt` + `1-TEST/` (APK for testers) + `2-STORE/`
(AAB + `mapping.txt` for ReTrace) + `KEYSTORE-PRIVATE-DO-NOT-SEND/` (keystore,
properties, `credentials.backup.enc`). Each subfolder gets its own README.
**Never** invent a BACKUP-PASSPHRASE.txt — the passphrase is the user's and is
not in the repo; the Arrows folder has one because the user put it there.

**Listing folder:** numbered dirs `1-descriptions` … `6-tablet-10inch-screenshots`,
each screenshot dir holding raw captures plus a `framed/` set (the set to upload).

**Repeatable scripts now in the repo:**
- `scripts/generate-store-assets.mjs` → `icon-512.png` (resized from
  `assets/icon.png`) and `feature-graphic-1024x500.png` drawn from the real
  palette + wordmark, so listing art cannot drift from the app.
- `scripts/generate-store-frames.mjs` → takes a JSON manifest of
  `{src,out,caption,width,height}` and composites captures onto the brand
  gradient with a caption and rounded corners.

**Screenshot capture recipe (one emulator, three sizes):**
`adb shell wm size 1080x1920 / 1200x1920 / 1600x2560` with density
`440 / 240 / 320`, force-stop + relaunch between sizes. The **saved run
persists across resolution changes**, so build one good board at phone size and
every later size restores the identical board — no replaying.
Clean status bar via SystemUI demo mode
(`settings put global sysui_demo_allowed 1`, then broadcasts for clock/battery/
network); `exit` command afterwards, and `wm size reset` + `wm density reset`.
Use **tap-to-place** (tap tray shape, then tap the board cell = shape's
top-left) rather than simulating drags — far more reliable over adb.

**Gotcha:** `Read` on a 1600x2560 screenshot reports coordinates at a scaled-down
display size; multiply by the stated factor before feeding them to `adb input tap`.
See also [[local-android-build-traps]].
