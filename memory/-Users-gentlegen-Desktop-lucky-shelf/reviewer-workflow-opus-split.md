---
name: reviewer-workflow-opus-split
description: "Since Fable is unavailable, Lane B reviews use a fresh-context Opus reviewer subagent — the implementer never signs off their own work."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

On 2026-07-07 the relay flagged that Opus 4.8 was acting as BOTH Lane B implementer and reviewer of its own UI work — the judge grading their own homework, which is the weakest kind of review and violates the independent-verification discipline in the global harness §6.

**Decision:** Fable (the usual independent reviewer + contract/scoring/item-table sign-off per [AGENTS.md](AGENTS.md)) is unavailable right now, so the reviewer seat is filled by a **separate Opus 4.8 with fresh context** — spawned as a subagent that does NOT see the implementer's reasoning, re-runs the scenario itself, and writes the verdict. Same model, separated roles + separated context.

**Why:** self-review misses the implementer's own blind spots; independence (not model identity) is what makes a review worth anything.

**How to apply:**
- This session (Opus) = Lane B implementer only. Never APPROVE my own Lane B work.
- After implementing, spawn a fresh general-purpose/Opus reviewer with a self-contained §6 brief (context, non-goals, observable acceptance criteria, and the exact verify commands to run). Tell it to verify from scratch, enumerate evidence, and emit an APPROVE/REQUEST CHANGES/UNCERTAIN verdict block — not "LGTM".
- Device/eyeball FEEL acceptance still belongs to the human, separate from the reviewer's code-correctness pass.
- When real Fable is back, route milestone + contract/scoring/item-table sign-off to it (the `*-fable-review.md` convention); the Opus reviewer is a stand-in, not a replacement for that authority.

First use: the cascade self-fire→pop polish ([[cascade-self-fire-pop]]) — fresh Opus reviewer enumerated all 9 ruleFire emission sites in scoring.ts and returned an evidence-backed APPROVE. Worked well.

**Scar (2026-07-07) — reconcile the tree file-set against the packet before any verdict/commit.** While the orchestrator was mid-review of Phase 2a ([[loop-v2-phase2a-tag-synergy]]), Codex layered Phase 2b ([[loop-v2-phase2b-build-steering]]) into the SAME working tree in parallel. The tree then contained `contracts/index.ts` + `engine.ts` changes that directly contradicted the 2a packet's "no GameState/Action/schema changes" claim; the tell was a mid-review "file modified since read" error and `git status` growing from 6→10 files. **Detection rule:** at review START and again BEFORE committing, diff the `git status` file-set against the packet's "files changed / no X changed" claims — a mismatch means out-of-band/parallel work; stop and reconcile (whose change is it, is it reviewed) rather than committing a blended tree under one phase's banner. Both phases were ultimately reviewed (own scenario + own mutation each) and merged together in `5e0797a` because the shared refactors in `bots.ts`/`economy.ts` made a safe two-commit split impossible without interactive hunk staging.
