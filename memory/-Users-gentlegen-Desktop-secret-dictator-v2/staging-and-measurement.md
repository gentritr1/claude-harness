# Staging (Gate 14) — and the measurement scars it left

Branch `juice-map`, 2026-08-11. The design doc's juice map (five moments) plus
the player's avatar swap. `src/play/stage.js` is the schedule; `src/play/main.js`
drives it; `test/stage.test.js` is gate 12; `test/tell.test.js` gained four rows.

## Facts about the build

- **The accusation aimed at you cannot fire in a shipped match.**
  `src/engine/orator.js` excludes `ctx.humanSeat` from `targets()` AND from
  `beatOrder()` — one field, two uses, so it cannot be lifted for targeting only
  without editing the engine. It is a deliberate D2 decision tied to the intent
  strip (work item 4). Staging + trigger are built; `__play.accuseMe()` drives
  the same path for review.
- Three presentation clocks now: rAF, the match `setTimeout` chain, and a
  dedicated 40 ms `setInterval` for the moments. **Never shorten `nextDelay()`
  to pump presentation** — that value is how long bots THINK, and shortening it
  made autopilot race whole days during a ballot reveal (the reveal then never
  appeared). Cost an hour to diagnose.
- Overrides on the lighting rig (`aim` / `setFocus` / `setRim`) rest at null and
  `release()` is a complete undo, so the states table and its warm budgets are
  untouched. The focus multiplier sits AFTER the weather in `push()`, so a
  lantern a Seize put out stays out.
- Adding a cue is blocked by `test/ambience.test.js`: it asserts
  `cuesFor(...).join() === 'tile:reform'` exactly AND that every `CUE_ID` is
  reachable. A sixth cue breaks both. Silences went in as a master-gain envelope
  instead (`HUSH` in audio.js).
- `?body=capsule` restores the graybox player body, the `?tone=linear` idiom.

## Detection rules earned this gate

| pattern | detection rule | brief/test update |
| --- | --- | --- |
| a staged camera push leaked across a restart, and the warm budget read +1.23 pt — nearly blamed on a parallel session's art | **a warm delta must be A/B'd on ONE tree with a switch, not compared across branches** | ship a URL switch (`?body=capsule`) with any change that alters what is in frame; `scripts/capture-warm-body.mjs` |
| ballot stagger "measured" at 183.8 ms against a declared 180 — while the sampler's own frame interval was 179 ms | **a sampled interval is meaningless when the sample period ≈ the signal period; report the SPAN (errors telescope) and print the frame interval beside the number** | capture scripts record the frame interval on the frames that took the sample, never a session median |
| a tell-gate channel was swept 1,769 times and produced a non-empty value 0 times (curtain call — the loop exits before projecting game over) | **every channel needs an exercise floor asserting it was actually produced**, not just that it agreed | `check(curtainsSeen > 0, …)`; one extra projection after the match |
| a code comment reasoned "hue 218 is outside the amber band, so a cool light cannot spend warm budget" — false: it lifts painted timber over the classifier's floors | **never argue a measurement from a property; take it** | comments beside tuned constants must quote the measured before/after |
| `view.players.slice()` inside a Proxy-audited function forces `players.slice` onto the public whitelist | copy arrays with a `for…of` loop in anything the recording Proxy drives | whitelist stays about the game, not about JavaScript |

## Numbers worth keeping

- Warm, 1280×720, podium mark, forced `trial`, HUD composited, project
  classifier: **8.08% before → 8.43% after**, ceiling 10. The avatar is +0.37 of
  that; the five moments are ~0. HUD cost +0.63 (was +0.68 twice before — the
  instrument has not drifted). **1.57 points of headroom left.**
- Accusation: last beat 620 ms of a 700 ms cap; reduced motion 380 ms.
- Purge: master gain exactly 0 for 800 ms, gavel at 800.
- Curtain: 250 ms/figure, Dictator last at 1500 ms, observed 1519/1617.
- Fingerprint still seed 1000 / 7p → 61 steps, 38 human decisions, LOYALIST.
- walk.html regression unchanged to the digit (wall 11.6499, corner 6.3499 /
  3.5001, ramp15 y 1.5005, obstacle -2.3999).

## Environment caveat

The headless Playwright pane renders this square at **143–196 ms per frame** at
1280×720 (≈5–7 fps) and the main thread blocks for over a second at a time. Any
sub-200 ms timing observed there is resolution-limited. 640×360 gets it to
~53 ms. Editing source mid-run triggers Vite HMR and wipes injected recorders —
finish source edits before measuring (3rd occurrence of the HMR scar).
