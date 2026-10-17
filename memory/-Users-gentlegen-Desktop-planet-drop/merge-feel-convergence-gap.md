---
name: merge-feel-convergence-gap
description: "The merge is an instant teleport-swap with no convergence; that — not post-merge timings — is the real \"feels forced\" cause"
metadata: 
  node_type: memory
  type: project
  originSessionId: b7b5666e-42d5-4a69-918e-ab5a27fc74d2
---

The "feels forced when two bodies come together" complaint is NOT fixable by animation
timing constants. Root cause confirmed in `MergeResolver.TryMerge`
(Assets/_Project/Scripts/Gameplay/MergeResolver.cs): on merge it does
`pool.Release(first); pool.Release(second);` then `pool.Acquire(merged)` at the midpoint —
the two source bodies teleport-vanish and the merged body pops in the **same frame**. All
the pop/squash/glow/particle/shake juice polishes what happens *after* this hard swap.

The research-driven timing pass (commit 72903af, values in [[ui-art-polish-direction]] /
docs/ANIMATION_TIMINGS.md) tuned every post-merge knob and is committed. The actual feel
fix is still **deferred**: a brief (~0.10–0.16s) eased pre-merge convergence layer before
the swap, which touches pooling, chain resolution, the dedupe queue, fail-line/active
counts, and MergeBodyPlayModeTests — so it needs an investigation pass first and the user's
playtesting. Should sit behind `MotionPreferences.ReduceMotion` (instant swap when reduced).

**Approach C (ghost/decoy + delayed reveal) was tried and REVERTED — it looked worse.**
The fatal flaw: the merged body is held invisible (scale 0) for ~0.12s while it keeps
FALLING (it has the damped velocity + gravity), so the ghosts ease toward a moving target
and the real planet reveals lower/displaced with an empty gap where the merge happened —
a visible "gap then displaced pop." Delayed-reveal only works for stationary merges; most
merges here happen mid-fall. If convergence is revisited, it must be **Approach A** (keep
the two REAL source bodies, disable their colliders, ease them together over ~0.12s, THEN
release+swap) so there's never a hidden/empty moment — heavier (pending-merge state +
MergeBodyPlayModeTests updates) but the only shape that actually shows "coming together."
Don't retry C.

Also deferred: `MotionPreferences.ReduceMotion` is now a real get/set but nothing wires it
to a Settings toggle or OS preference yet (plumbed but unreachable by players). See
[[reviewing-codex-output]] — verify any convergence implementation on the real merge path,
not just the unit touched.

**UPDATE 2026-07-02: Approach A IMPLEMENTED** on branch `codex/game-feel-art-polish`
(NOT yet playtested/merged). MergeResolver got a pending-merge layer: TryMerge now
MarkConsumed()s both bodies, calls MergeBody.BeginMergeConvergence() (simulated=false +
collider disabled), and eases both real bodies into the fixed midpoint over 0.12s with
ease-in (t²) in FixedUpdate, then EndMergeConvergence + CompleteMerge (the old
release+acquire+publish+chain path). Chains converge one link at a time (ResolveChain's
TryMerge just starts the next pending). Safety rails: valid = activeInHierarchy && Consumed
(a pool-recycled body has Consumed=false → abort, restore survivor via
CancelMergeConvergence); non-Playing states / OnDisable cancel all pendings;
MergeBody.Configure re-enables the collider so pooled bodies can't come back as ghosts;
ReduceMotion takes the instant path. MergeResolver.IsIdle (queue+pendings empty) added for
tests; MergeBodyPlayModeTests now WaitForResolverToSettle instead of one WaitForFixedUpdate.
Needs the user's editor playtest before merging.
