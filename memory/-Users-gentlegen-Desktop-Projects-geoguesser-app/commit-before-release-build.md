---
name: commit-before-release-build
description: The 1.3.1 (10) AAB shipped from an uncommitted working tree — always commit (and tag) the exact tree before building a release
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8cc01d9f-953c-4c68-8443-67b91ef3a0c2
  modified: 2026-09-07T21:37:58.842Z
---

On 2026-09-07 I found the whole 1.3.1 (10) release (haptics, PressableScale,
persisted high score, redesigned start/summary screens, version bump) sitting
**uncommitted** in the working tree a week after it was uploaded to Play on
2026-08-31. `main` was still at 1.2.2 and the feature branch at 1.3.0. Nothing
in git corresponded to the binary testers were running.

**Why:** a release you can't check out can't be diffed, bisected or hot-fixed;
stale branches also can't be judged "merged" when the real work is untracked.

**How to apply:** before `./scripts/build-aab.sh`, require `git status --short`
empty, commit as `release: x.y.z (N) — …`, tag `vx.y.z`, and push. Record the
tag in [[geoguesser-release-build-steps]]. When asked to "merge stale
branches", run `git status` first — the uncommitted tree is often the newest
branch.
