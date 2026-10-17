---
name: reanimated-loop-parking
description: withRepeat(withSequence(...)) loops can park after one cycle; use a single phase ramp
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2051cf29-c6f2-47e3-8fbd-76df141b5684
  modified: 2026-08-31T22:10:39.373Z
---

Pattern → detection → fix from the 2026-09-01 casino-polish review: a periodic sheen built as `withRepeat(withSequence(sweep, withDelay(hold, withTiming(0,{duration:0}))))` swept once and parked at phase 1 (caught by DOM sampling: value frozen 38s). Reanimated 4 on web at least does not re-loop that shape reliably.

**Why:** zero-duration timings/withDelay inside a repeated sequence can end the repeat contract.

**How to apply:** For any periodic effect, drive ONE linear phase shared value `withRepeat(withTiming(1,{duration:cycle, easing:linear}),-1)` and carve the active window out in the worklet (pattern proven in Tutorial.tsx / FloatingBlock / the new sheen + marquee chase). At review time, verify loops by sampling the animated value twice a few seconds apart — a frozen value = parked loop.
