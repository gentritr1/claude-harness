---
name: godot-prototype-and-perf-measurement-traps
description: Godot greybox prototype exists and plays; Performance.TIME_PHYSICS_PROCESS is NOT a usable per-tick metric and produced three invalid measurement attempts
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T15:49:01.037Z
---

`prototypes/godot-greybox/` (Godot 4.7.1, GDScript) is a full parallel prototype of the merge loop:
`core/` is a rules port of `packages/merge-core` keeping the same events→intents boundary, `game/` is
the scene layer, `spike/` runs the same three scenarios as the RN harness. **770 headless checks pass**
(`--headless --script tests/run_tests.gd`), and the loop plays — verified by a self-captured screenshot
via `-- --demo=25` (45 drops → 24 merges → tier 6).

## Godot perf is UNMEASURED — three invalid attempts, and why

1. **Headless viewport lies.** The headless display server reported 874×874, so the §7 camera fit
   clamped the chamber to its 8.0 max instead of 5.835 — different geometry, incomparable numbers. Pin
   the design viewport explicitly for any benchmark.
2. **Uncapped main loop.** Headless has no vsync, so Godot ran up to `max_physics_steps_per_frame` (8)
   ticks per frame while `TIME_PHYSICS_PROCESS` reports per-*frame* physics time. Identical config
   measured **8 ms to 43 ms**. Set `Engine.max_fps = Engine.physics_ticks_per_second`.
3. **`Performance.TIME_PHYSICS_PROCESS` is still not trustworthy** even capped: it returned values
   exceeding the capped frame time, and a config matrix came out incoherent (contact monitoring **off**
   measuring slower than **on**). Use Godot's own profiler / a `--debug` session instead.

**Detection rule that saved this:** a configuration matrix is a free sanity check — if switching a
known cost *off* makes it slower, the instrument is broken, not the engine. Run the matrix before
quoting any number. Also: an implausible direction (native physics measuring 5× slower than matter-js
in node) is a signal to audit the harness, not a finding to report.

## Structural facts that need no benchmark

Godot needed far less §10 translation than matter-js: `linear_damp`/`angular_damp` are per-second
rates so Unity's 0.18/0.55 port literally (matter-js has one combined per-step knob); `linear_velocity`
is px/s with one convention (matter-js has two, depending on read site); and `continuous_cd` solves
tunneling natively, so substeps stay at **1** — matter-js needed 2, doubling the dominant cost, which
is precisely what broke the RN frame budget.

## Cross-engine parity

`merge-core` is float64; Godot `Vector2`/`Rect2` are **float32**. The camera fit agrees to ~7
significant figures (hence 1e-5 tolerances in four assertions). Integer/threshold decisions (tier
draws, merge legality, scoring) stay identical across engines; **trajectories diverge**, so
deterministic replay is per-engine, not portable.

Related: [[v02-spike-outcome-matter-js-fails-120]], [[perf-gates-need-jitter-and-resolution-tolerance]]
