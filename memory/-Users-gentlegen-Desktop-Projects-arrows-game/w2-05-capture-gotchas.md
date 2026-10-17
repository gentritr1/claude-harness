---
name: W2-05 capture gotchas (2026-09-24)
description: screenrecord --bugreport clock sync, TEST rewarded ad closing, Reanimated detach, port-8097 kill mistake
type: project
---
- `screenrecord --bugreport` stamps each frame with device wall-clock; `log -t MARK` before each `input` puts taps and frames on one clock (±1 frame). Offset = overlay time − pts, check on 3 frames.
- Google TEST rewarded creatives vary; the ✕ position is not fixed. Close with BACK after ~32 s (worked, aclk 0) — never a coordinate tap (a blind tap at 1320,122 closed one creative on blank space; lucky).
- After an ad closes the emulator redraws the game window from black top-down over ~200 ms; motion started at ad close is partly hidden (W2-05 Concern 1).
- Reanimated 4.5.1 does not revert detached animated styles (AnimatedComponent TODO) -> snap the shared value to rest before swapping to a static style; swapping element type remounts children (star stagger restarts).
- Stock reanimated/mock has no useReducedMotion; jest.setup.ts now adds it.
- `lsof -ti tcp:8097` also lists the Claude app's Chromium network helper (browser pane client) — kill only the expo PID (pkill -f "expo start --web").
