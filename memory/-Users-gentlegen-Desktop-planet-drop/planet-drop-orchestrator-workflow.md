---
name: planet-drop-orchestrator-workflow
description: "How the user runs Planet Drop dev — I orchestrate/review, Codex codes, user runs Unity"
metadata: 
  node_type: memory
  type: project
  originSessionId: ff41d5f6-0426-49ce-8d49-05351091651a
---

Planet Drop (Android-first Unity 6 physics merge game, greybox MVP) is built with a strict division of labor the user wants kept:

- **I (Claude) am orchestrator/reviewer only** — I write per-task Codex prompts, review Codex output against acceptance + ARCHITECTURE §14 + Global DoD, tell the user what to verify by eye, and handle **all** git (commit/PR/merge/branch). The user never commits.
- **Codex writes all game code.** It cannot run Unity (licensing), so everything lands EditMode/PlayMode-**unverified** — "logic-green ≠ engine-green." Review for compile errors first, then spec gaps.
- **The user runs Unity** (6000.5.0f1): Test Runner (EditMode/PlayMode) + play-check, often on the Android emulator (no physical device).
- **Cadence:** one task/chunk at a time. I give prompt → Codex implements on the branch → user pastes report → I review → user runs tests/play-check → I commit. Branch-per-task → PR → merge to main, delete branch.

**How to apply:** Don't write game code myself (docs/checklists/memory are mine to edit). Don't tell the user to commit. Always have the user run tests before I sign off. After any PlayMode test run, revert `ProjectSettings.asset` before committing (Test Runner dirties the app id). Related: [[document-learnings-as-we-go]].
