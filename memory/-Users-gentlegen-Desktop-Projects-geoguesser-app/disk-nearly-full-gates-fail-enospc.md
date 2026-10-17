---
name: disk-nearly-full-gates-fail-enospc
description: "The Mac's disk was at 100% (464 MiB free) on 2026-10-05; `npm run check` failed with ENOSPC in check-contrast's compile, and the re-run after freeing space passed"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-05T19:41:06.305Z
---

On 2026-10-05 the merged gate after D3-1 reported `check=1`. The cause was not the code: the shell printed
"no space left on device", and `scripts/check-contrast.mjs` → `compile-design.cjs` died in `execFileSync` (status 2,
with no stderr). `df -h ~` showed 415 of 460 GiB used, with 464 MiB free. Freeing about 150 MB of regenerable scratchpad
BASE copies was enough to re-run `check` and get exit 0.

**Why:** a red gate that comes from the environment looks exactly like a code failure, and could have sent a fix round
after a phantom.

**How to apply:**
- When a gate fails with no assertion, an empty stderr, or a bare `execFileSync` status, run `df -h ~` before
  diagnosing anything.
- Check free space before long runs too: the device session's R48 rule stops below 2.5 GiB.
- The gitignored evidence in `docs/plan/evidence/` is 2.2 GiB and the session scratchpad holds about 1 GiB. Delete only
  regenerable copies (BASE worktrees, pulled APKs), never the only copy of evidence
  ([[worktree-remove-deletes-evidence]]).
- Most of the used space is outside this project. Tell the owner rather than deleting their files.

Related: [[avd-dies-under-host-memory-pressure]], [[gate-commits-on-the-exit-code]].
