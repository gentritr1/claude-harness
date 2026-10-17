---
name: phone-controller
description: "Phone-as-controller dev prototype (work/phone-controller, 2026-10-04) — HTTPS POST + SSE transport, security gates, measured latency, iPhone eyeball gaps, scars"
metadata:
  node_type: memory
  type: project
  originSessionId: 5286607d-0486-4a1e-bcb7-cfc03c010f23
  modified: 2026-10-03T23:17:24.415Z
---

Built 2026-10-04; merged to main in d25e529/b93ff29 (see [[consolidation-2026-10-04]]). Steering round 2 after the first iPhone playtest ("a bit late, too hard"): phone steer integrates at 18/s (τ 56 ms) via InputFrame.steerResponse instead of the game's 6.2/s (τ 161 ms — the dominant lag); MEDIUM preset 40° lock expo 1.4 (15° → 0.22, was 0.49), SOFT/SHARP on the phone; fused gravity. Latency log: dev server prints input→send / wifi↑ / relay→game / wait→frame / TOTAL every 5 s and writes .phone-logs/latency.jsonl. `npm run dev:phone` → Vite `--mode phone`: HTTPS (openssl self-signed, `.cert/`, gitignored + fs.deny), bound to the Wi-Fi IP only. Game at `https://<lan-ip>:5173/?controller=phone` shows a QR; phone opens `controller.html#k=<token>`. Dev-only: `import.meta.env.DEV` gate in main.ts, controller.html not a build input. Gate: `npm run validate:phone` (in test:code).

**Transport is POST + SSE, NOT WebSockets** — Fable research (sourced): iOS Safari refuses wss to a self-signed cert even after the page warning is accepted; fetch/EventSource honour the exception. So no root CA on the phone. `ws` dependency was dropped.

Measured (separate headless Chromes, same Mac, no Wi-Fi leg, 625/625 motion events reconciled): one-way phone page → receiver p50 2.9 / p95 4.5 / p99 9.8 / max 16 ms, 378/378 delivered.

**Open eyeball gaps (UNVERIFIED until the owner tries on iPhone):** cert-warning flow + motion permission on iOS, tilt direction/feel (28° full lock, 2.5° deadzone), Wi-Fi RTT (pad shows median/p95), touch layout on a real phone.

Scars:
- A `ws` server socket with no `error` listener crashes the whole Vite dev server on an oversized frame (validator caught it). Any socket attached to Vite's httpServer needs an error handler.
- Headless Chrome renders the game on CPU; with that running, a latency run measured a starved machine (10 s window took 13.1 s, 22 sends/s vs 60). Reconcile event counts against window × rate before quoting any number, and measure transport with a bare receiver page.
- `pkill -f "Google Chrome.*--headless"` killed other sessions' headless Chromes too. Kill only PIDs you launched (puppeteer `browser.process().pid`), and wrap drive scripts so a timeout still closes browsers.
- Fable code review (REQUEST CHANGES → fixed): `<meta name=referrer content=no-referrer>` can make WebKit send `Origin: null` on a same-origin POST → relay 403 looks like a bad token (use `same-origin`); a single-slot SSE game stream let two tabs evict each other at 1 Hz (now fan-out). `test:code` rewrites art/evidence/dreamisland-v1/phase-c/validators/painted-validation.json (pre-existing hash drift) — restore it after each run.
- `server.fs.deny` REPLACES Vite's default list — repeat the defaults.

Related: [[futurisma-architecture-facts]], [[hud-integration-scars]] (input.ts must stay duck-typed for the Node-stub validators).
