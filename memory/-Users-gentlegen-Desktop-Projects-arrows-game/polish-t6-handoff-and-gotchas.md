---
name: polish-t6-handoff-and-gotchas
description: POLISH-T6 (2026-09-24) native board vs Skia overlay are unordered pipelines; fix = never hide, cover; cold first-paint cost of new Skia draw types; zsh "$FILES" tar near-loss
metadata:
  type: project
---
- Native ArrowsBoardView (Fabric mount -> postInvalidateOnAnimation, +1 frame) and the Skia overlay (runOnUI picture) have NO ordering: any hide/show of one arrow in one React commit can blank a frame (pre-fix: reduced motion 18/18 unmount blanks, motion-on 9/18). Fix shipped: native never hides the shaking arrow; Skia draws a bg-coloured unmoved cover under the moving overlay; a new mark is handed to native at 170 ms (FirstPaintCleanupTimer.handBack). Grid dots under the path stay hidden during the flash (owner eyeball pending).
- Cold first overlay paint after app launch is sensitive to NEW Skia draw types: a stroked closed triangle or a path-op union delayed it ~1 frame (318 vs 334 ms heart run); a plain grown-triangle fill did not. Measure with a relaunch-per-sample "cold tap" harness (artifacts/POLISH-T6/scripts/coldtap.mjs).
- Owner mp4s from VFR screenrecord: resample on the union of recorded pts, not a 60 fps grid (a 14 ms blank fell between grid points).
- show_touches does not render into screenrecord for app_process-injected taps; no tap->paint latency reference that way.
- zsh does NOT word-split "$FILES": `tar -cf x.tar $FILES` silently omitted six sources before they were overwritten with HEAD versions (recovered byte-identical from scratch copies; git diff hash check). Use arrays or ${=FILES}, and check `tar -tf` before overwriting.
- Gradle JS-only rebuild keeping app data: pin android/app/build.gradle versionCode to the installed one (controller's real build leaves it at 8; test APK is 6), install -r (same release signer), restore after.
