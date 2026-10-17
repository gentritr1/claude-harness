---
name: gfxinfo-rows-are-not-frames
description: "gfxinfo framestats rows are renders, not vsyncs (a Modal doubles them), and duration > 16.7 ms is not jank; group by IntendedVsync and use FrameDeadline"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T05:21:13.198Z
---

2026-10-08 globe bake-off: my first parser reported 85 "frames" in a 700 ms spin (about 43 vsyncs) and ~100% "janky" in BOTH arms and even at idle. Two instrument bugs:
- **Rows are renders.** A Modal window and the activity, or a TextureView update and a traversal, can share one IntendedVsync: 46 of 166 rows had a 0.0 ms delta.
- **Latency is not jank.** FrameCompleted − IntendedVsync > one period is normal triple-buffered pipelining. Android's own summary said "Janky frames: 1 (0.43%)" against a legacy 76%.

**Why:** a sample count that does not reconcile against window × rate was the tell, exactly as CLAUDE.md §6 warns. I almost quoted p95 = 35 ms as the spin's smoothness.

**How to apply:**
- Use scripts/framestats.py (device-2026-10-07): group rows by IntendedVsync.
- Count dropped frames from vsync gaps and deadline misses from FrameCompleted > FrameDeadline.
- Read GPU time as GpuCompleted − IssueDrawCommandsStart.
- Window the spin with the app's start/end log lines read through `logcat -v monotonic`: same clock as gfxinfo, checked against /proc/uptime.
- Always print vsyncs next to the expected count, and attack the parser with a synthetic dump first.

Related: [[a-min-over-a-sampled-matrix-is-an-artefact]], [[every-gate-we-write-ships-a-silent-pass]].
