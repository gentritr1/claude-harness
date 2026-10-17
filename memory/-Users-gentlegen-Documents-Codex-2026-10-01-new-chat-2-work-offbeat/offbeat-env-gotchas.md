---
name: offbeat-env-gotchas
description: "Environment traps in the OFFBEAT repo - Node version for tests, dev server already running, browser pane hidden"
metadata:
  node_type: memory
  type: project
  originSessionId: 1dcc955e-d230-4e7b-a170-720a969b4385
  modified: 2026-10-01T22:11:47.948Z
---

- `npm test` uses `--experimental-strip-types`, so it needs Node 22+. The default `node` is nvm v20.19.4 and fails with "bad option". Use `PATH=~/.nvm/versions/node/v24.18.0/bin:$PATH`.
- The project's own `next dev` was often already running on :3000 (started 2026-10-01). Check with `lsof` and reuse it rather than starting another.
- The built-in browser pane can be hidden, which makes screenshots time out. Headed Playwright with `--window-position=-2400,0` gives real GPU compositing for frame probes. The display is 120Hz, so reconcile frame counts against 120, not 60.

**Why:** each of these cost a round trip in the 2026-10-02 review. See [[offbeat-pass3-review]].
**How to apply:** set these up before any QA run.
- If studio playback freezes at step 0 in automation, check the audio clock first: on 2026-10-02 the macOS output stalled (`AudioContext.currentTime` advanced 6ms in 800ms while `state` was "running"). Launch Chrome with `--disable-audio-output` (timer-driven fake output) for timing checks. Do not change system audio settings.
