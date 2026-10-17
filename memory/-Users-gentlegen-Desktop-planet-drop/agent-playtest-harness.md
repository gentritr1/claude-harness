---
name: agent-playtest-harness
description: dev-only bot harness that plays the real game for balance analytics — chosen INSTEAD of the deferred deterministic sim core
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b5a9fa8-484c-49c8-883a-5ce1cc257310
---

After Post-MVP #4 retention pass shipped ([[retention-addictiveness-plan]]), user wanted "let agents play it for analytics to improve the game." I pushed back and **reframed**: that goal does NOT need the deterministic fixed-point sim core (the heavy rewrite that stays DEFERRED) — agent-driven balance analytics run fine on the existing Unity physics; run-to-run variance is fine/wanted. Determinism only buys bit-exact replay/cross-platform/regression, none of which is needed pre-traction.

**Decision (2026-06-26):** build an **agent playtest harness on the existing core**; determinism stays deferred. User picked: Phase-1-skeleton-first, heuristic policies.

**Phase 1 ✅ DONE** (commit `e99349b` on branch `tooling/playtest-harness`, NOT yet PR'd). Dev/editor-only: all files `#if UNITY_EDITOR || DEVELOPMENT_BUILD` in `PlanetDrop.Dev.Playtest`, touches NO production code (resolves via ServiceLocator + FindObjectOfType), excluded from release builds. Drives drops via `AimController.SetAimX` + `Dropper.TryDropCurrent`, observes via `MergeBodyPool.GetActiveBodies`/`Dropper.CurrentTier`, restarts like `ResultScreen.Retry` (ReleaseAllActive + TryTransitionTo Playing), runs at `Time.timeScale=8`, writes CSV to `Application.persistentDataPath`. Files: BotObservation, IBotPolicy, GreedyMatchBotPolicy (topmost same-tier → widest-gap fallback), BotPlaytestDriver, + EditMode policy test.
- **Mac gotcha:** F9 is intercepted by macOS — added an OnGUI Start/Stop button (primary trigger) + spawn Debug.Log. Batch only starts from Home or GameOver state.
- **Verified working:** 50-game greedy batch, all natural game_over (no drop_cap), clean CSV — score 5656–20590, **best tier 8–11 (never reaches tier 12)**, greedy mean score ~11k already beats the human best 5994. Real balance signal.

**Phase 2 ✅ DONE** (commit `a525a55` on `tooling/playtest-harness`, NOT yet PR'd). Added RandomDrop + LowestColumn policies, `PlaytestStats` (mean/median/nearest-rank percentile), driver runs greedy→random→lowest (gamesToPlay = games PER policy) + writes `playtest_<ts>_summary.csv` with per-policy mean/median/p10/p90 score, best-tier, tier12_rate, mean drops/duration/occupancy. EditMode tests for both policies + stats.

**Phase 3 ✅ DONE** (chamber×spawn experiment matrix). First Phase-3 run was INVALID — chamber sized from dead config values ([[chamber-is-camera-fit-not-config]]); fixed to use live `chamber.InnerBounds` + width SCALE. Real runtime chamber width = **8** (camera-fit), not config's 5.

**ALL THREE PHASES MERGED to main via PR #29 (squash `4f7c093`), branch deleted.** Harness complete.

**VALIDATED FINDINGS (600 valid games, baseline reproduces real game ~tier 9.3/338 drops/10.6k):**
- Width 8→11.2 (greedy): tier 9.32→9.90 (median 10), drops 338→550, score ~2×. Width is a strong ceiling/session-length lever (but ~60% longer games).
- **tier12_rate = 0.000 even at 11.2 width / 550 drops.** Tier 12 is a MERGE-ECONOMICS wall (~2048 tier-1-equiv needed in one body), NOT geometry/config. Config levers can't unlock it — would need a dedicated endgame "concentration" mechanic.
- Mid-tier spawn (tier 6/7) HURTS: big bodies crowd the board → fewer drops → lower tier. Don't ship it.

**OPEN ITEMS:** (1) combo `COMBO ×N` popup overlaps the B3 Risk-Bank SECURE badge top-center — small reposition fix pending; (2) tier-12 endgame mechanic = future design; (3) housekeeping: untracked AGENTS.md + tools/ (cache-clear util), Unity churn, git prune. LLM/RL policy = possible later IBotPolicy swap-in.
