---
name: 2026-09-16-action-legibility-fx
description: Tondo Task 3 (fx.js skip duck / +2 lob / reverse sweep) — three gotchas measured in headless Chrome: animation-name fallback replays a pop, timer-vs-WAAPI-ready drift, mock transition probes contaminated by their BEFORE snapshot
metadata:
  type: project
---

Commit 2cbba02 (branch next-level). Report: .superpowers/sdd/2026-09-16-tondo-tier2-tier3/task-3-report.md.

1. **A one-shot class that overrides another class's `animation` replays the other one when it comes off.**
   The seat note made `.plate.is-loud` (tondo-pop); the duck added `.plate.is-skipped`; removing
   `is-skipped` at 380ms put `tondo-pop` back in `animation-name` → it RESTARTED (opacity 0.40 flash,
   measured at 406ms). Detection: per-frame `getComputedStyle(el).animationName`/opacity after the
   one-shot ends. Fix: the note keeps the pill loud but not the plate (`&& !note`).
2. **Don't chain an effect to a WAAPI animation's arrival with a timer started at `animate()`.** The WAAPI
   delay counts from the ready frame (after the whole snapshot task); a 200ms injected task-tail stall made
   the timer punch the badge exactly 200ms early (3/3). Chain off the last animation's `finished` + guard.
   Stall injection that works: busy-wait inside a MutationObserver callback (runs at task end).
3. **`window.__mock.transition()` emits BEFORE then AFTER; BEFORE replaces whatever the previous watch left**, so
   comparing kinds run back-to-back mixes in YOUR TURN banners, deal ghosts and live-now rewrites.
   The brief's `differsFromNumber` came out true on RED and GREEN alike (vacuous). Seal by priming each
   watch with an unobserved `transition('number', same seats)` (task-3-probes/sealed-legibility.js).
   Also: `mock:yourTurn` boots with a 700ms YOUR TURN banner that covers the top seat at 390px — wait
   ~1500ms before triggering a frame capture.

**Why:** all three pass every name-based probe; only timelines / computed styles expose them.
**How to apply:** when adding a class-driven one-shot to a node that already has class-driven animations,
sample animationName after it ends; when sequencing effects on WAAPI, chain promises, not timers.

**Fix round 1 (commit 0234e87), two more:**
4. **The duck became WAAPI `composite:'add'` (id `seat-skipped`)**, because a vulnerable seat must keep `.plate.is-loud`
   through a note, and ANY class-driven one-shot on that plate swaps animation-name and replays the alarm pop when it
   comes off. WAAPI fires no `animationstart` — probes must scan `getAnimations()` for `a.id`.
5. **A deferred live-region write clobbers the snapshot's own "Your turn" line** (the region keeps only its last text).
   Announce synchronously and fold the turn into the same line.
Probe hygiene: a probe's `valid` must come from the watched event's own landing (startTime ≥ landing frame), proven
with a negative control whose watched card never lands. CDP `Runtime.evaluate` times out at 30s — cap live probes.
