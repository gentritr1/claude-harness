---
name: consolidation-2026-10-04
description: Where FUTURISMA work lives after the 2026-10-04 merge to main (b93ff29) — what was merged, left out, backed up, and which folders are now stale
metadata:
  type: project
---

On 2026-10-04 everything was consolidated onto GitHub `main` = **b93ff29** (fast-forward from a6445a4, user-approved push). Built in worktree `~/Desktop/Projects/futurisma-race/.claude/worktrees/integrate` (branch integrate/all-2026-10-04).

Merged: origin/codex/b2-garage (garage line + ad473a0 launch fixes); the uncommitted handoff tree from `~/Desktop/futurisma-race/minimap-aplus-handoff` (Frostline Map 09, Afterglow Map 08, A+ minimap default, garage/launch polish up to an Oct 2 surface pass) as commit 670e5b6; work/minimap-aplus recorded as superseded (`-s ours`: its unscoped .hud-gate phone rules would fight the A+ layout); trusting-thompson 8820746 was already contained in the handoff; phone controller (see [[phone-controller]]).

Left out by user choice (kept as backup refs): polarity_work hangar/grand-tour experiments (`refs/backup/polarity-work-2026-10-04` in that clone), craft-art-review garage-lighting (`refs/backup/craft-art-review-2026-10-04` in the craft-art-review clone). v16_integration_work is an Aug-28 clone already in main.

Pre-existing handoff test failures fixed on the way: map registry 7→9 (validate-nightshift), polarity-minimap window stub needs `?minimap=classic`, seam budget 2584→2589 (wiring itemised), build ceilings — the handoff was ~1 KiB over its own ceilings with NO itemised reason (flagged to user), re-pinned 997 raw / 276.6 gzip / 289 shell.

**Stale now:** `~/Desktop/futurisma-race/*` folders (minimap-aplus-handoff, craft-art-review, launch-review-fixes, polarity_work) and their CURRENT_GAME.md play instructions; the main checkout `~/Desktop/Projects/futurisma-race` still sits on work/phone-controller with superseded uncommitted phone code. New work should start from main.

**2026-10-05 disk cleanup (user-approved):** disk hit 100% (629 MB free) — an Agent `isolation: worktree` checkout of this repo (multi-GB evidence) died mid-checkout. Pushed to GitHub and verified by ls-remote SHA: `backup/polarity-work-2026-10-04` (66e9fa4), `backup/craft-art-review-2026-10-04` (c380eec), `backup/handoff-2026-10-04` (acd46a6); then deleted ~/Desktop/futurisma-race/{polarity_work, craft-art-review, launch-review-fixes} and cleared the npm cache → 30 GB free. NOT deleted: `minimap-aplus-handoff` — holds 335 evidence files (236 MB) + 3 art/references files that exist nowhere else (owner to decide). launch.json entries `dreamisland-dev`/`dreamisland-preview` point at the deleted polarity_work.
- Scar: pushing from a clone whose `origin` is a LOCAL path makes git upload all history (GitHub drops the SSH connection); fetch the ref into the main repo and push from there (sends only the new 55 MB). GitHub SSH was flaky — verify every push with a retried `git ls-remote`, never trust the push line alone.
- Check free disk before any `isolation: worktree` agent (`df -h /System/Volumes/Data`); a full checkout needs several GB.
