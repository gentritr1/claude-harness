---
name: stormhaven-brief-carries-planetdrop-lessons
description: "Stormhaven (new game) orchestrator brief must carry Planet Drop's Unity lessons; keep it synced each new convo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3bf28429-aada-455e-a8fe-68105387ae9d
---

The user is starting a second Unity game, **Stormhaven Workshop: Harbor Slice** (block-puzzle → salvage → merge board → villager orders → harbor restoration → idle workshop → save). Project folder: `/Users/gentlegen/Desktop/stormhaven-workshop-prototype` (do NOT nest inside planet-drop). Same orchestrator workflow as [[planet-drop-orchestrator-workflow]]: I orchestrate/review + own all git, Codex codes, user runs Unity.

The brief lives at `/Users/gentlegen/Desktop/stormhaven-workshop-prototype/ORCHESTRATOR_BRIEF.md` (moved into the project folder 2026-06-24; a `KICKOFF.md` next to it holds the paste-ready next-chat starter). On 2026-06-24 I added a "Lessons Carried From Planet Drop (READ FIRST)" section folding in our hard-won Unity lessons: save gate-ordering wipe ([[save-additive-schema-safety]]), Codex verification discipline ([[reviewing-codex-output]]), merge convergence feel ([[merge-feel-convergence-gap]]), Kosovo monetization gate ([[monetization-kosovo-constraint]]), URP/TMP gotchas ([[unity6-urp-ui-gotchas]]), and the cheatable local-clock idle note.

**Monetization decision (2026-06-24): Stormhaven is ads-only for now.** Ads via Unity LevelPlay without the AdMob adapter (same stack as Planet Drop). Real IAP is DEFERRED indefinitely — `IStore` stays a fake/local stub, no real store integration, until the Kosovo Google Play merchant-payout gate is resolved. See [[monetization-kosovo-constraint]].

**Why:** user wants each new game to start ahead of the bugs we already paid for, and explicitly asked that this brief be kept in sync with Planet Drop learnings across conversations.

**How to apply:** at the start of any Stormhaven convo, and whenever a new Unity lesson lands on either project, update that section of the brief. It's a living doc and the source of truth that outranks generic best-practice advice. See [[document-learnings-as-we-go]].
