---
name: retention-v1-status
description: "Retention loop v1 shipped 2026-07-13 — what is verified vs open gaps, and iteration-2 candidates"
metadata: 
  node_type: memory
  type: project
  originSessionId: c8dea768-0576-4c80-a808-455bfec9c3e0
---

Retention v1 (committed 2026-07-13, Opus 4.8 implemented, reviewed + runtime-verified via debug hook): best-score chase w/ NEW BEST beat, phases every 15 gates (speed cap +40/phase, max 720, hue shift), goal ladder (`src/goals.js`, key `ttn-goals-v1`), daily streak (`src/streak.js`, key `ttn-streak-v1`, injectable date), death stats + 120ms hit-stop, `?debug=1` hook. Original best key `thread-the-needle-best` preserved.

**Open verification gaps (device-only, blocked in preview):**
- Audio (chimes/newBest/phaseUp/goalComplete mixes) — never heard by anyone.
- Feel: hit-stop timing, touch latency, spring snap on real device — needs user eyeball/hands.
- Goal-complete toast pixels mid-run (logic verified, not screenshotted).
- rAF-driven motion smoothness — all my frames were stepped, not real-time.

**Iteration-2 candidates (need user taste input first):** difficulty curve tuning (autopilot suggests wave patterns at speed 600+ may be reaction-limited), audio polish, first-session tutorialless onboarding check with a real human.

Remote: `git@github.com:gentritr1/thread-the-needle.git` — `main` at 5579a48 (2026-07-13): iteration 2 shipped (Flappy-hard difficulty via pure seeded `src/spawn.js` + viewport-fairness speed cap; 60fps rendering via baked glow sprites/cached background — flushed frame 364→17.5ms). Difficulty tuning is bot-measured: 250ms/100ms/0ms-reaction bot medians 6/13/25 desktop, mobile capped at reactable limit (946 px/s at 375w). Suite: 31 tests. User feedback drove it: "too easy" + "not smooth 60fps". User has NOT yet confirmed on-device smoothness or fun — that eyeball is still open.

Harness gotcha: bot runs that outlive the step guard leave `state.mode === "running"`, and `start()` early-returns — subsequent bot() calls silently continue the leaked run and corrupt gate counts (fired once: a "250ms bot" reported 314 gates). Reset with `state.mode = "ready"` before each `start()`.

Related: [[headless-canvas-verification]], [[node-version-trap]]
