---
name: offbeat-pass3-review
description: "OFFBEAT portfolio project state after the 2026-10-02 browser review; brief NEXT-PASS.md, QA scripts, verified bugs, chosen concept"
metadata:
  node_type: memory
  type: project
  originSessionId: 1dcc955e-d230-4e7b-a170-720a969b4385
  modified: 2026-10-01T22:11:44.457Z
---

2026-10-02: first real browser review of OFFBEAT (Codex built passes 1-2 without any browser). Brief for the implementer is `NEXT-PASS.md` at the repo root (A bugs, B identity system, C features). QA instruments are in `scripts/qa/` (shots.mjs, color.mjs, frames.mjs). They use installed Google Chrome via `channel: "chrome"`; no Playwright browsers are cached.

Verified bugs that tsc, tests and build all missed: the hero 3D was 0px wide on mobile (`align-self: center` on an abs-children flex item); the 3D finish chroma was 50-74% of the swatch (ACES tone mapping); dark mode showed a light finish disc; studio playback re-rendered the whole tree each step (janks at 4x throttle).

Update 2026-10-02 later: Claude implemented A (bugs) and B (identity: Archivo + Martian Mono, tinted neutrals, transport-key buttons, faders, key banks, late-bar logo, record-back specs, groovebox copy) in-session, uncommitted, awaiting owner screenshot approval. A and B committed on branch pass-3-polish (7c68f30, 16fc743). C1 swing dial built and verified end to end (uncommitted at time of writing); swing formula is the standard late = (swing-50)/50 of a step, not the brief's x0.5. Node test runner needs explicit .ts import paths (tsconfig allowImportingTsExtensions). C2 (speaker plays along) committed 484bdc0: motion specified in px at render size (brief's +0.04 units was invisible; first measurement showed 136px speaker / 2px squash, fixed with zoom 1.3 + 4%). 3D-BRIEF.md (uncommitted) is the handoff prompt for a 3D specialist: perf foundation (worker/OffscreenCanvas, instancing, contact shadow) then step-LED strip, touchable 3D swing dial, analyser-driven radiator, staged anatomy.

Concept direction proposed (pending owner approval): "a speaker with a drum machine inside", with a swing dial as the literal "offbeat" feature. The groove link codec must keep v1 decoding; fixture `1.112.8822bb94`.

**Why:** pass 2 shipped "verified" claims without eyes. Every blocking bug was visual or layout-related.
**How to apply:** review pass 3 by re-running `scripts/qa/*` and comparing with the baselines in NEXT-PASS.md, not by reading the diff. See [[offbeat-env-gotchas]].

2026-10-02 afternoon: the implementer pushed 7669a73 straight to origin/main without review, then published the private site from the unpushed branch fix/resume-polish-review (3ce0640). Reviewed both afterwards: APPROVE.
- Idle-to-motion jump: reproduced pre-fix on 7669a73 (first frame at 43% of the explode, 3/3 runs); fixed in 3ce0640 (starts at 0%).
- The anatomy grille swing-aside is a clear visual improvement.
- First explode: better at 1x, unchanged at 4x (~67-75ms median).
Rule going forward: implementer work lands on a branch; main only after review. Brief update: say "do not push to main".
