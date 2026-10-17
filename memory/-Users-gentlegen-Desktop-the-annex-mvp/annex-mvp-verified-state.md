---
name: annex-mvp-verified-state
description: "Verified state of The Annex MVP as of 2026-07-19 review (what held, what was overstated)"
metadata: 
  node_type: memory
  type: project
  originSessionId: bbb02cb4-bacc-420f-823a-32ec093c9721
  modified: 2026-07-19T10:21:16.216Z
---

Full-path review on 2026-07-19 (Fable orchestrator + 3 Opus 4.8 executors + live browser journey):

**VERIFIED (executed and observed):** lint clean, 16/16 tests, tsc+vite build pass; full desktop journey start→covert approach→forge→care ward→reconstruction (emergent-self)→illicit tribunal finding→debrief→run-2 residue echo; save/resume via reload; two-step confirms on field actions/filing/tribunal; determinism (zero Date.now/Math.random in src/, counter-based event ids).

**Overstated claims from the build session:**
- "strict validation and recovery": saveGame/loadGame/clearGame localStorage wrappers have ZERO test coverage; schemaVersion rejection and malformed-JSON paths untested; no recovery-fallback test.
- "initialized Git repository": `git init` only — ZERO commits as of review date.
- "bounded residue": gameplay residue bounded (±1, last run only) but `previousRuns` array grows unbounded in the persisted save (~250B/run).
- 390px mobile journey: claimed by build session, NOT re-verified in review (screenshot pipeline was broken).

**Known minor defects (all confirmed against code):** approach selection in [[Briefing]] is irreversible but skips the two-step confirm (engine.ts:178 guard makes it permanent); decodeGameState doesn't enforce tribunal-gate reachability (hand-edited save can skip to tribunal); alarm can never exceed 1 so "N traces" plural UI is dead; ChoiceButton armed state has no aria-live announcement.

**Core design facts (from code, stable):** trust is written but NEVER read for gating; only gate on endings is the single `tribunalOverride` boolean (granted only by forge-authority at maintenance site); reconstruction model (4 outcomes from 6 pairings, new-dream→emergent-self in any pair) gates nothing and is never referenced at tribunal; tribunal needs only 2/4 sites; case content is byte-identical every run — residue is text-only. See [[annex-mvp-next-features]].
