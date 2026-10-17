---
name: model-split-ui-experiment
description: Testing Opus 4.8 for UI/visual work while Codex keeps logic; home screen is the A/B testbed
metadata: 
  node_type: memory
  type: project
  originSessionId: 5614bdd9-89d8-439f-aca8-908096a187fc
---

Started 2026-07-05: user suspects Codex is strong at logic but weak at UI taste (art-integration branch UI "not in tune" — code correct, visually flat, even left the wordmark scrim it built switched off). Experiment: give UI passes to Opus 4.8 in Claude Code instead.

Test brief: `docs/briefs/2026-07-05-opus-ui-test-home-screen.md` — home-screen redesign on branch `post-mvp/9b-opus-home-ui` off `post-mvp/9-art-integration`, screenshot-iteration loop mandatory, user eyeball is the gate.

**Round 1 shipped 2026-07-05** (commit 833759b on `post-mvp/9b-opus-home-ui`): Opus's home pass — lifted wordmark out of the Earth into a cyan light pool below the planet cluster, added a hero bloom to dissolve the art-rect seam into the starfield, retuned UITheme to the painting (CosmicCyan/NebulaViolet/PanelGlass/TileGlass/GlassRim), replaced the opaque menu slab with a feathered light-pool, gave Play a cyan halo, rebuilt tiles + best pill as cyan-rimmed glass, deleted the dead scrim code. Awaiting first user screenshot (19.5:9) to iterate.

**Outcome: PENDING** — record verdict here after the user compares. If Opus wins, split future briefs: logic/systems → Codex, visual/UI → Opus. Related: [[planet-drop-orchestrator-workflow]], [[visual-calibration-briefs-lesson]], [[reviewing-codex-output]].
