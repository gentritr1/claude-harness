---
name: retention-addictiveness-plan
description: Post-MVP
metadata: 
  node_type: memory
  type: project
  originSessionId: 850e7893-b922-41ed-8c73-91471c684f4f
---

Post-MVP **#4 = retention / "addictiveness"** pass, derived from two deep-research docs the user
provided (a game-design "Design Bible" + a "Telemetry/Balancing/Simulation Framework"). Full plan
lives in `docs/RETENTION_PLAN.md`. Follows the visual ([[ui-art-polish-direction]]) and audio
([[audio-polish-next]]) passes; same workflow ([[planet-drop-orchestrator-workflow]]): one chunk →
user verifies in Unity → I review → commit.

**Key framing:** most of the research's "MVP" is ALREADY built in Planet Drop (Codex, 9 themes,
dailies, boosters, coins, combo, fail line, seeded `WeightedTierQueue`, **3-object preview**, FTUE).
So this pass fills specific gaps, not a rebuild. Thesis: clearer/fairer/more recombinable, NOT
louder/manipulative; "never end on You Failed."

**Roadmap (3 threads, chunked):**
- **A — Competence & Fairness ✅ COMPLETE:** A1 post-loss recap (`bedb6c2`), A2 bounded
  spawn bag (`6a6083e`), A3 free reroll/run (`deb8584` — 4th booster-bar chip, no inventory).
  All on branch `post-mvp/4-retention-depth` (not yet PR'd to main).
- **B — Variety & Anti-solve (IN PROGRESS):** B1 per-run optional objective ✅ MERGED to main via
  PR #26. **B2 family resonance ✅ DONE** (commit `842674a` on branch `post-mvp/4-thread-b`, NOT yet
  PR'd). User picked the "on-board family resonance" rule: each merge counts live same-family bodies
  (family = `PlanetVisualTable.Get(tier).Style`, reuses `PlanetStyle` — NO schema change), bonus =
  `floor(baseScore * min(cap, step*(count-minStacks)))` added AFTER combo multiply (additive, not
  compounded). New: `IBoardFamilyCensus`/`MergeBodyPoolFamilyCensus` (alloc-free), `FamilyResonance`/
  `IFamilyAffinity` (pure), `FamilyResonanceEvent`, `FamilyResonanceHud` (top-right badge), config
  step 0.12/cap 0.5/min 1 + remote keys, EditMode tests. **B3 risk bank ✅ DONE** (commit `9300f5f`
  on `post-mvp/4-thread-b`, NOT yet PR'd). User picked "clutch-merges-in-danger" fill + "score pop"
  payout: while fail-warning active, each merge banks `floor(baseScore*share)` (cap 750); recover →
  arm N=3-drop survival countdown → cash out via new `IScoreService.AddBonus` (score pop); re-danger
  un-arms+resumes; GameOver forfeits (RiskBankLostEvent). `RiskBankController` state machine,
  `RiskBankHud` (top-center under score; BANKING red heartbeat / SECURE amber pips / CASHED green /
  LOST shake — HUD placement+polish was a 2nd Codex pass after first version overlapped the play
  field). Config share/cap/surviveDrops + remote keys. EditMode tests. NEXT: ONE PR (Thread B =
  B2+B3) to main — confirm full EditMode suite green first (B3 tests were compile-verified, not yet
  run in interactive Unity at commit time).
  NOTE: opening Unity re-serializes LevelPlay/URP/ProjectSettings assets — that churn is unrelated;
  keep it OUT of feature commits (stage `Assets/_Project` + `Assets/Tests` only). Codex also drops an
  unrelated root `AGENTS.md` — do not commit it.
- **B — Variety & Anti-solve ✅ COMPLETE:** B1 (#26), **B2+B3 MERGED to main via PR #27 (squash
  `ec86109`), branch deleted.** Thread B done.
- **C — Measurement (light):** C1 hidden-fun metrics ✅ DONE (commit `9353294` on
  `post-mvp/4-thread-c`, NOT yet PR'd). `HiddenMetricsRecorder` (emit-only via `IAnalytics`, kept
  OUT of save-critical RunStatsRecorder): emits `first_merge`/`first_combo`/`near_miss`/
  `run_abandoned` + `run_metrics` aggregate {reason, duration, occupancy_peak, near_miss_count} on
  any termination (GameOver or ->Home abandon). Occupancy via injected `Func<int>`(=pool.ActiveCount),
  clock injected for tests. User chose to DEFER `failed_merge_opportunity` (needs real board/adjacency
  analysis) — future chunk. EditMode tests. NEXT: PR Thread C to main → that COMPLETES Post-MVP #4
  retention pass (deterministic-sim core stays DEFERRED).

**BIG DECISION — deterministic sim core DEFERRED.** Doc 2's headless fixed-point deterministic
sim + nightly 100k-run AI-persona balancing + BigQuery dashboard is live-ops-studio scale; rewriting
the working Unity-physics core to fixed-point isn't worth it pre-traction. Take the cheap 80%
(config-driven + seeded, already have) + Thread C metrics; revisit only with a real audience.

User chose (2026-06-25): start **Thread A**, save plan to docs+memory. First chunk = **A1**.
