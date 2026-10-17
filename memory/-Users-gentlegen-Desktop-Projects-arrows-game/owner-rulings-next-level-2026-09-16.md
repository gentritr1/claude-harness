---
name: owner-rulings-next-level-2026-09-16
description: "Owner's binding product rulings for executing docs/NEXT-LEVEL-PLAN.md: Track A attention game, branch next-level, only the ad-counter fix approved, notification rejected"
metadata: 
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-16T12:29:08.501Z
---

Rulings the owner gave on 2026-09-16 before plan execution started (via a structured question,
not inferred). They override any draft step that disagrees.

- **Game identity = Track A.** Arrows is a calm attention / visual-search game. PRODUCT.md gets
  rewritten to say so. No ordering mechanic, no "puzzle depth" work. See [[game-design-truths-measured]].
- **Git:** all plan work lands on branch `next-level` as reviewed commits. The pre-existing working
  tree was landed there as 77f73d9 (tap forgiveness), ec03073 (pop ladder audio), da93dcd (web
  preview + plan). Nothing merged to main, pushed, or released without an explicit yes.
- **Ads:** ONLY "persist the interstitial counter across cold start" is approved. **Rejected:**
  interstitial after a loss, free hint when no rewarded ad loads, wall-clock cooldown / session cap /
  new-player grace. An honest "no ad available" state is still a defect fix, but must not grant a
  free hint.
- **Retention:** approved daily board + forgiving streak, shape gallery, store-review prompt at a
  perfect clear. **Rejected:** the evening notification. The share artifact was never asked about —
  it stays flagged OFF pending a ruling.
- Every new player-visible feature ships behind a flag defaulted OFF until the owner accepts it from
  a screenshot.

**Why:** these change what gets built; re-asking wastes the owner's time and silently re-adding a
rejected item (e.g. a loss interstitial) would contradict a direct decision.

**How to apply:** check `docs/next-level/progress.md` "Pre-flight rulings" before starting any
task; treat a rejected item reappearing in a brief as a review failure.

**Push 2026-10-01 (owner: "push these"):** next-level 87ec519..1d61234 (78 commits) to origin, after checking no artifacts/credentials/APK/AAB/keystore/secrets in the range. Each push still needs its own explicit yes; nothing merged to main, no PR.
