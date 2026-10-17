---
name: open-verification-gaps
description: "Running list of user-side verification gaps deliberately deferred — surface these when the user asks \"what's pending\" or opens an editor session"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f83faef-f3fc-4cd6-85b7-1dcbadcd9448
---

User explicitly chose (2026-07-03) to keep shipping and batch verification gaps for later — "u can tell me". Surface this list whenever they open an editor session or ask what's pending. Remove items as they're confirmed.

0. **Android device perf check for bloom** (vessel PR #38 introduced the project's first post-effect: camera post-processing + Bloom 0.65): verify frame rate on a real/mid-range Android device during a busy board; if it hurts, bloom becomes a quality-tier setting. Also visually confirm codex thumbnails did NOT double-bloom (bake camera should have post off).
1. **Gravity wells step-zero feel check** (Phase 1 merged PR #32 default OFF): DEV drawer → Wells ON, tier-9+ on board → drop curves visibly, settled pile still, danger meter quiet. Tune `gravityWellMaxAccel`/`gravityWellRangeRadii` if off. See [[gravity-wells-feature]].
2. **Gravity wells A/B batches** (tooling merged PR #33): two ≥30-run GreedyMatch batches via `ConfigureGravityWellsForBatch(false/true)`, then I evaluate the pre-committed gate from the CSVs (runbook in code at that method).
3. **Visual identity sweep eyeball pass** (SHIPPED to main via PR #34, squash `1b3c74e`): Stardust/Living World names in HUD/codex, tier-11 galaxy spiral reads at gameplay size and ≠ tier-12 Egg (also check the codex thumbnail), notice survives pause, resonance notices still appear after dead-panel deletion.
4. **Merge-escape fix confirmation** (PR #35 merged 2026-07-03): play a chain-merge-heavy session — no planet falls out, and `body_escaped` never appears in the console (its appearance means the containment sweep is catching what the clamp+thick-walls should have prevented). See [[merge-spawn-escape-bug]].
5. **iOS taptics** (audio pass, PR #23): still UNVERIFIED — no device. See [[audio-polish-next]].
6. **Monetization**: IAP flow + Google Play merchant payout for Kosovo still unverified. See [[monetization-kosovo-constraint]].

7. **Playability-audit wave (2026-07-13, uncommitted on post-mvp/9b-opus-home-ui)**: (a) run FULL EditMode + PlayMode suites in the editor — the whole wave (overflow spawn-exemption, coach-mark resume, 3-slot preview, reduce-motion, schema-4 bump + `Load_V3FileMissingReduceMotion_PreservesDataDespiteStaleChecksum`) has only been COMPILE-checked, never executed; (b) eyeball: 3-thumbnail Next preview layout (container widened 184→220, tertiary at x=76), merge coach-mark position (its center-screen special-case was deleted), Reduce Motion toggle in Settings actually damps animations, first-win banner reads "Cosmic chain! / You created a Molten World."; (c) confirm on-device save survives the update (schema 3→4 migration preserves coins/progress).

Related lesson recorded 2026-07-03: two memories (shader gaps, bible renames) had gone stale enough to nearly mis-scope a brief — re-verify memory claims against code before writing briefs, staleness compounds fast when Codex ships in parallel.
