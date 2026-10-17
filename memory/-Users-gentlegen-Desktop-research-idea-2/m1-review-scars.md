---
name: m1-review-scars
description: "M1 review scars: stale vite bundle + 0x0 browser viewport produce false readings; Opus stalls on long file writes; target-whipsaw design finding."
metadata: 
  node_type: memory
  type: project
  originSessionId: 34efc46f-cf4b-48ec-91db-1c0e87da9387
---

M1 review session (2026-07-18, commit f738465):

- **Stale-bundle scar fired again (browser flavor):** dev server reused from the builder's
  session served an OLD bundle — first browser reading showed benchmark 32,075 vs the true
  64,660.5 and target computed with the WRONG f-index. Detection rule: any browser number
  that contradicts a vitest/CLI number -> force-reload the page (navigate force) BEFORE
  debugging code. Also: the in-app browser pane can report viewport 0x0 (canvas collapses
  to 0px) until an explicit resize_window call — resize to a preset before concluding
  layout is broken.
- **Opus stalls on long generations:** builder agent hit the 600s stream watchdog twice,
  both times mid-large-file (stylesheet, HUD wiring). Fix that worked: resume with a
  surgical finish-list + "Edit small diffs only, never rewrite whole files". Future briefs:
  instruct chunked writes up front for files >~200 lines.
- **Certificate paths are exposed in getState().certificate** (flat cell indices) — a
  reviewer can drive full runs headlessly by replaying them (won a full 8-round run this
  way). acceptCharm takes plain string ids from draftOffers; unknown ids silently no-op.
- **Design finding (routed, priority for next design loop): target whipsaw.** Per-board
  benchmark spans ~627 -> ~825k within one run (multiplier-tile density drives exponential
  scores); one board was 94% of run score. Parity node==browser verified — it's the spec,
  not the build. Candidate fixes are data-level: %-of-par round scoring, log display,
  generator variance bands. Decide BEFORE M2 styles counter/summary.
- runScore rounds fractional charge (7.5 -> 8) vs spec "sum of charge banked" — pin a
  decision + test in M2. [RESOLVED in M2: banks raw, test pins 7.5; whipsaw RESOLVED via
  Round Points = 100 x charge/B0 cap 1000, ruling in docs/reviews/FABLE-RULING-whipsaw.md]

M2 cycle additions (commit cddd3fd):
- **Browser pane throttles rAF even when fronted** (0 frames captured) — animations
  complete via non-rAF paths but live-motion/frame-stats claims are UNVERIFIABLE in-pane;
  use synchronous probes (measureRenderCost) + stageFx-staged frames for screenshots; the
  literal rAF check is device-gated. Corollary trick: frozen rAF makes reduced-motion
  testable — spawned particles would persist, so their absence is proof.
- **Eyeball passes catch what criteria don't:** the FX-persist-across-loadSeed defect was
  found only by screenshotting a "clean" board after animated activity. Keep a mandatory
  fresh-load + post-activity screenshot pair in every UI review.
- Chunked-writes rule eliminated Opus stalls (0 in M2 vs 2 in M1). Keep it in every brief.

Related: [[project-overview]], [[loop-discipline]], [[node-and-ports]].

M4 cycle additions (design-system + 60fps, commit c406b4f baseline):
- **Layered canvas is a huge perf win, and makes measureRenderCost lie by default.** Caching
  the static board (tiles/glyphs/text) to an offscreen layer + blitting dropped the
  heaviest-frame p95 from 1.1ms (old, redrew everything/frame) to ~0.2-0.3ms. BUT the old
  measureRenderCost set no wire/flame, so it under-measured the real resolve frame. Fix:
  the proxy must reproduce the WORST frame — full 21-tile wire + full flame glow-sprites +
  saturated particle pool. Rule: a perf proxy that omits the animated layers isn't a proxy.
- **?fps overlay pause-gap artifact:** the preview pane pauses rAF between tool calls; on
  resume one frame-delta is multi-second, spiking the overlay p95 to 71579ms. Filter deltas
  >1000ms out of the fps ring (pause, not a frame). Same class as the wall-clock-vs-tick FX scar.
- Path2D tile glyphs (24-grid path data shared by canvas + legend SVG) killed the fuzzy
  font-glyph rendering AND gave the how-to legend pixel-identical shapes for free.
- Fonts: vendored @fontsource woff2 into src/assets/fonts + hand-written @font-face (not the
  @fontsource CSS import) = fully self-hosted, survives without node_modules; dist scan
  confirmed zero external/CDN URLs. Chunked-writes rule held (0 stalls; style.css + render.ts
  written in 3-4 chunks each).
