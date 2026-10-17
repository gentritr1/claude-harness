---
name: document-learnings-as-we-go
description: User wants iteration mistakes/fixes captured durably so future choices compound
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ff41d5f6-0426-49ce-8d49-05351091651a
---

The user explicitly wants every mistake/iteration we hit and fix to be written down somewhere durable, so future decisions get smarter instead of re-learning the same lesson.

**Why:** They think in terms of compounding — a fix that isn't recorded is a lesson half-wasted. Raised during Planet Drop Task 17 (QA hardening) after several review catches (Test Runner dirtying ProjectSettings, Object ambiguity, IMGUI footer clipping, half of §13 analytics unwired).

**How to apply:** Three homes, by kind of lesson —
- **Engine/runtime gotchas that only surface at run time** → append a bullet to `docs/ARCHITECTURE.md` §14 ("Unity Runtime Constraints & Conventions"), matching its format (end with *(Hit in Task N: …)*). This file is fed into Codex prompts, so it actively prevents repeats.
- **Project history / per-task review notes** → `docs/SESSION_LOG.md` (one entry per task/session at close-out) and the DEVELOPMENT_PLAN review notes.
- **Cross-session workflow/process preferences** → memory here.

Do this proactively as we go, not only when asked. Related: [[planet-drop-orchestrator-workflow]].
