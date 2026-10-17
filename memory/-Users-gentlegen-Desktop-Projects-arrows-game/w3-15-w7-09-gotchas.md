---
name: w3-15-w7-09-gotchas
description: W3-15/W7-09 (2026-10-06) - SF history overflow came from post-window frames during the slow meminfo dump; Play needs 24-bit PNG (screencap is RGBA); nohup builds survive session loss
metadata:
  type: project
---
- benchmark.mjs gesture phases tripped "filled the SurfaceFlinger history" 3/3 times on a v2 board under load ~50: diag showed 122 = 1 before + 48 inside + 73 AFTER the driver window (meminfo dump ~1 s). Fix: read SF latency before meminfo (window frames unchanged). Old-order sessions archived as series-pre-reorder.
- Play screenshot rule (read 2026-10-06): JPEG or 24-bit PNG no alpha, long side <= 2x short, 320..3840 px. Emulator screencap is RGBA -> prove alpha 255 then convert to RGB.
- A session loss mid-build: the nohup'd gradle build kept running and finished; check PIDs before restarting anything.
- Single-level harness now takes --level/--gen-version; PERF builds log `[gen] ... ms=` per deal; v1 3827 ~100 ms cold on emulator.
