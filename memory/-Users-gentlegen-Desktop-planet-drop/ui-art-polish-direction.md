---
name: ui-art-polish-direction
description: Post-MVP
metadata: 
  node_type: memory
  type: project
  originSessionId: 6539bd1a-7772-4fc8-b91c-0e14e2366a49
---

Post-MVP Task #3 = the greybox→real visual/UI polish pass, on branch `post-mvp/3-ui-art-polish`. **User directive (2026-06-21): stay in polish longer and raise the quality bar — this is the customer-acquisition step and there's time, so go beyond "good enough" toward truly premium.**

**Decisions:** Art strategy = **HYBRID** (procedural/shader planets backbone + a few AI hero textures). Pipeline = **URP 2D Renderer**. UI = **uGUI + TextMeshPro**, built programmatically by Codex. Glow = layered alpha + URP bloom (mobile-safe). Perf budget set upfront, device-tested at the end.

**Committed on the branch (newest first):** 4b booster bar uGUI · 4a uGUI foundation (`UIRoot`/`UITheme`/`UIKit`) + HomeScreen · Chunk 3 merge VFX & juice (`MergeVfxController`/`CameraShake` + MergeBody squash) · bloom enable (camera post-processing + Global Volume) · Chunk 2 nebula background + starfield · dev all-tiers preview (F8) · Chunk 1 planet shader (`CosmicBody.shader` + `PlanetVisualTable`) + brightness tuning · URP migration · Chunk 0 `docs/ART_DIRECTION.md`.

**STATUS 2026-06-23 — menus AND in-game polish are DONE & committed on the branch.** All screens migrated to the premium uGUI/TMP modal scaffold (Home/Settings/Daily/Boosters/Pause/Result/Codex/Cosmos), unlockable background themes shipped. This session completed the IN-GAME polish arc (commits 7c9dbab→3805a6d): G1 physics+merge juice, G3 atmosphere tone-down + theme tint 0.35, modal scrims (incl. Merge Chart), G2 HUD (score HUD, floating +N popups, combo banner→uGUI + burst gate, booster icon chips, top-right canvas Next box), research-driven animation timing pass (docs/ANIMATION_TIMINGS.md), responsive container + fit-to-chamber camera + premium drop guideline + glowing fail line, weightier physics + spawn spin (fixed column-stacking), and the planet shading passes (Stage A de-plastic/soft-terminator/fwidth AA, B per-tier theme-tint reweight, C1 gas latitude bands, C2 supernova broken shell). See [[cosmicbody-shader-already-sophisticated]] and docs/PLANET_VISUAL_RESEARCH.md.

**Still deferred / optional (not blockers):** the pre-merge convergence layer (see [[merge-feel-convergence-gap]] — instant teleport-swap; only Approach A would fix it, heavy); reduce-motion is plumbed but has no Settings UI toggle; exotic-style galaxy/black-hole surfaces were already good (left as-is). Branch not yet merged to main.

**Gotchas:** Play from **Boot.unity** not Main (Main-only play floods 100+ ServiceLocator errors — benign). Before any Android build: add `PlanetDrop/CosmicBody` + `PlanetDrop/Starfield` to Project Settings ▸ Graphics ▸ Always Included Shaders (runtime Shader.Find else strips). Delete stray `Assets/_Project/Scenes/New Folder`. See [[planet-drop-orchestrator-workflow]], [[monetization-kosovo-constraint]].
