---
name: delegation-model-rule
description: "Standing rule from the user: Opus 5 implements, Fable 5 only orchestrates and reviews — set model:'opus' on every implementer/planner Agent dispatch"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 346e76cc-1f12-4cf6-853c-98f993733660
  modified: 2026-08-29T13:53:28.120Z
---

The user's standing instruction (2026-08-29, repeated twice): **Fable 5 must not delegate to other Fable 5 agents. Every delegated agent — implementers, planners, diagnostic/explore sweeps — runs as Opus 5** (`model: "opus"` on the Agent call). Fable 5's role is orchestration and review only: writing briefs, running stage-2 verification (soaks, probes, screenshots), merging, and judging.

**Why:** the user wants the expensive frontier model reserved for judgment (specs, reviews, catching what implementers miss) and the implementation volume carried by Opus. An Agent call with no `model` param silently inherits Fable — that is the failure mode to watch for.

**How to apply:** on every `Agent` dispatch and any Workflow `agent()` call in this project (and by default in the user's other projects), pass `model: "opus"` explicitly. The only exception is a sub-agent whose entire job is review/verdict on Fable's behalf — and prefer doing that review directly in the main loop instead. See [[futurisma-architecture-facts]] for the per-phase briefing conventions this pairs with (merge main first, name the expected tip commit, diagnostics-counter gates for art phases).
