---
name: prototype-lab-state
description: "Prototype Lab grew to 18 games on 2026-08-18; fixes applied, six agent-built combos, verification gaps and playtest signals"
metadata: 
  node_type: memory
  type: project
  originSessionId: c927a751-c000-4ecf-8ab6-a97f66ccbc68
  modified: 2026-08-18T21:31:06.029Z
---

Prototype Lab (updated 2026-08-18 evening): **18** dependency-free browser prototypes. Shell contract: `window.PrototypeGames[id] = { mount(root, hooks) }` returning `{start, destroy}`; catalog lives in app.js, scripts in index.html. Server: `server.mjs` on port 3000, no-store caching (but an externally-started node process may hold the port — attach, don't restart).

Fixes shipped 2026-08-18 (all VERIFIED in-browser except where noted):
- Tilt Four tilts every 5th move (was 4th — always fired after P2's move, systematic seat advantage). Verified live.
- Twin Spark pads overheat after 1.5s held alone (parking no longer beats the synchronized-arrival hypothesis). Overheat timer is rAF-driven — code-trace only.
- Orbit Relay rings burn down while ridden (2.4 radius/s, collapse <10 = lost life). Decay pacing needs eyeball.
- Gravity Thread: dead "Best thread" stat → Flips counter.
- Hidden Bid / Pinwheel / Sky Stack labeled "known-loop baseline" in the UI (≈ Goofspiel / aa / Stack).

Six new games built in parallel by Opus agents (each wrote only games/<id>.js + concepts/<id>.md; I integrated catalog/scripts/CSS): Ember Orbit, Bid Four, Echo Courier, Shear Tower, Pin Duel, Freight Shift. Agent harness pattern that worked well: stub-DOM/canvas headless drivers executing the REAL module (Bid Four 56 assertions; Echo Courier 120 random playthroughs; Shear Tower geometry-reading frame driver; Freight Shift autopilot with dodge-headroom arithmetic).

Open verification gaps (as of 2026-08-18):
- Canvas-game FEEL unverified for all four canvas newcomers — the hidden Browser pane suspends rAF entirely (measured 0 frames/3s), so only DOM/setTimeout games are fully verifiable headless. Needs human eyeball with visible pane.
- Freight Shift: weight/drag flattens above ~200 carried (slide cap reached) — greed becomes free; playtest watch-item.
- Bid Four: clash-jam spam as pure blocking — metrics in concepts/bid-four.md.
- Pin Duel seat balance (who faces more pins) — needs win-rate-by-seat over real matches.

A CONCURRENT session (not this one) ran a 27-run playtest and added AUDIT.md "Playtest signal follow-up" + clarity copy passes mid-session: replay pull = Echo Vault, Tilt Four, Pinwheel; clarity risks = Bloom Circuit, Pocket Heist, Hidden Bid. Expect concurrent edits in this repo; re-read shared files before editing.

Lab UI quirk: navigate/hash changes do NOT re-execute app.js; after editing shared files, a hard location.reload() in the pane is required to pick up changes.

Echo Courier v0.2 "Sonar Array" (2026-08-18 late): reimplemented from the user's Claude Design project "Sonar phosphor memory courier" (claude.ai/design id 8059673a-0ec6-4b02-8a1c-b031e9e1b7a6) via DesignSync. Endless depth descent, 4-contact hull, depth-rule stack (shadow/track/drift/pressure), re-ping at half gain. Port pattern that worked: keep the .dc.html logic verbatim, but replace React keyed rendering with persistent DOM nodes + cssText mutation so CSS transitions survive (innerHTML rebuilds kill the phosphor-decay wave). Fonts Chakra Petch + Sora via Google Fonts link in index.html. Verified by DOM-probe autoplay in the live page (reads walls/parcel/depot from mark styles, BFS, key events) — full delivery, descent, hull loss, restart, destroy all pass; feel still needs human eyeball. Probe gotcha: computed cssText serializes rgba with spaces, authored innerHTML keeps authored syntax — match accordingly.

**Scar (2026-08-18): `hidden` attribute vs inline display.** The depth-card overlay shipped permanently visible because the element had inline `display:flex` — the HTML `hidden` attribute (UA `display:none`) loses to any inline display. My headless probe checked the `.hidden` PROPERTY and passed while the screen was actually broken; the user's screenshot caught it. Detection rule: overlay/visibility assertions must read `getComputedStyle(el).display`, never the hidden property or attribute. Fix pattern: drive `style.display` directly on elements that carry inline display styles.

Echo Courier v0.3 (2026-08-18, latest): ported from the user's downloaded Claude Design zip (~/Downloads, extracted to scratchpad). Structured variety: 6 terrain archetypes via shuffle bag (no consecutive repeats), 5 modifiers from depth 3 (Convoy/Cache/Brittle/Drifting parcel/Decoys, dparcel deferred until drift rule active), par-corridor generation (reject unless BFS-optimal in 12–22 std / 18–30 survey), par-scaled ping timings, Trench Survey hard mode (10×14, hull 3, glimpse-only from depth 3, mode + bests in localStorage: echo-courier-mode / -best / -best-survey). Geometry is now dynamic — stage rebuilt per start() from makeGeo(hard). Verified via reusable in-page autoplay probe (window.__p: scans marks, reads courier from transform, BFS per-step so currents/drift can't break it) — 5 std depths + 2 survey depths delivered, optimal-play equals par. The concurrent session also edits sonar.html — merge carefully, read before editing.

Standalone build (2026-08-18): `sonar.html` at repo root — fullscreen Echo Courier reusing games/echo-courier.js unchanged (mount + custom hooks; transform-scale-to-fit via wrapper offsetWidth/Height which ignore transforms; best score in localStorage "sonar-array-best-v1"; fullscreen API toggle). Verified end-to-end by DOM-probe autoplay: delivery, hull loss, best persistence, card overlay computed-display correct in both lab and standalone.
