---
name: verification-recipe
description: "How to serve and screenshot the Morse Trainer locally (existing server on 4173, headless Chrome screenshot command)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1228ee92-125a-44af-96df-2cd8fa10ba9b
  modified: 2026-08-22T15:45:08.078Z
---

- A `python3 -m http.server 4173` is usually already running from the repo root (the README's command). Don't start a second one; `.claude/launch.json` just attaches to `http://localhost:4173`.
- Deterministic screenshots: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,1500 --screenshot=out.png "http://localhost:4173/?theme=pocket&mode=drill"` (390×1400 for mobile). URL params `theme=` and `mode=` are honored by `src/app.js`.
- Headless Chrome `--window-size=390,…` screenshots CLIP the right edge (the window floor is wider than 390); this is a capture artifact, not overflow — it appears identically on pre-change commits. For mobile truth use the in-app browser resized to 390 (or CDP emulation) and read `document.documentElement.scrollWidth`.
- `?guide=off` (added 2026-08-22) suppresses the first-run guide dialog for screenshots.
- The first-run guide opens whenever `localStorage["morse-trainer-onboarding-complete"] !== "true"` — headless Chrome always starts with empty storage, so machine-only screenshots need the guide dismissed (use `?guide=off`).

**Why:** Port 4173 collided with the preview tool on 2026-08-22 and cost a detour; screenshots are the only honest acceptance for visual/feel work in this repo.
**How to apply:** Reuse the command above for before/after comparisons; never call visual work done from CSS alone. See [[design-pass-2026-08]].

- CDP driver scripts need **node 24** (`/Users/gentlegen/.nvm/versions/node/v24.18.0/bin/node`): the repo's default node 20.19 has no global `WebSocket`, so `scratchpad/cdp*.mjs` throws `ReferenceError` on the default binary (2026-08-22).
- Synthetic `KeyboardEvent` dispatch only exercises the app's own `document` handlers. To test a **native button default action** (Enter on a focused button) send CDP `Input.dispatchKeyEvent` as `rawKeyDown` + `char` + `keyUp`; a bare `keyDown` silently does nothing and looks like a product bug.
- Clicking a full-screen scrim by its element centre can land on the sheet above it — click explicit coordinates near the top of the viewport instead.

- Pass 11 harness (2026-08-23): `scratchpad/run11.sh <script> <seconds>` launches a **fresh** headless Chrome per script and kills it afterwards — a long-lived instance wedges after ~15–20 s of round driving. `scratchpad/keys11.mjs` has `press` (real CDP keys), `focusOn`, `activeElement`, `waitKeys`, `stage`, and `gate` (asserts `visibilityState === "visible"` + `document.fonts.ready`). `scratchpad/cdp11.mjs` is `cdp2.mjs` with dual-stack target discovery.
- The settings toggle buttons respond to `.click()` while the popover is closed; driving them that way avoids opening the blurred `::backdrop`, which is expensive in headless.
- **Real keys need a visible pane.** When the Browser pane is collapsed (the user is in their own Chrome), `computer key` does not reach the page at all — a capture-phase listener records nothing — and `visibilityState` is `hidden`. For keyboard checks use CDP `Input.dispatchKeyEvent` against a headless Chrome with the page visible, as the pass-11 agent did (`scratchpad/keys11.mjs`, `run11.sh`).
