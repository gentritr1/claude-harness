---
name: w3-08-legibility-capture-gotchas
description: W3-08 (2026-09-26) fit-to-view capture gotchas - capture.mjs wm reset logs a post-shot relayout; seed campaign pointer instead of per-level DEV_LEVEL APKs; every campaign board is width-bound
metadata:
  type: project
---
- capture.mjs resets wm in `finally` AFTER the screencap; the app relayouts at the intermediate 1440px@480 config and logs `[board-viewport] w=480 h=949`. "Last logged viewport" of a wm-override capture is WRONG; snapshot logcat before the shot (artifacts/W3-08/scripts/cap308.mjs). The PNG itself is fine (pixel-identical to a manual 360x689 capture).
- Non-PERF level capture without per-level APKs: seed `arrows_current_level` + `arrows_dark_mode` via `su 0 sqlite3 .../RKStorage` while force-stopped (artifacts/W3-08/scripts/seed.sh), tap Play (720,1924 native; 540,1483 @1080x2340/480; 540,1273 @1080x1920/480). DEV_GEN_VERSION picks v1/v2; prove the board with `[ftue] board_mount`.
- No camera-scale log exists in tracked code; W3-08 used a scratch-tree `[board-camera]` patch (artifacts/W3-08/scripts/board-camera-diag.patch).
- Measured: every campaign board 1-10000 (v1+v2) is width-bound on 360/411 dp phones (max rows/cols 1.353 vs viewport 1.525+), so cellPt = 0.94*vw/cols. Brief premise "Bolt = smallest cells" was wrong (it's tallest); smallest = level 390 Crescent 46x46, 7.36 pt @360dp.
