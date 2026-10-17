---
name: dont-pipe-long-builds-through-tail
description: Piping a background build through `| tail` hides all output and made me wrongly call a successful build failed
metadata:
  type: feedback
---

On 2026-08-28 I ran `./scripts/build-aab.sh 2>&1 | tail -40` in the background.
`tail` buffers everything until the stream closes, so the log read empty the
whole time. I then checked for the `.aab` while gradle was still writing it,
saw no gradle process at that instant, and announced the build had failed —
it had not. It exited 0 with `BUILD SUCCESSFUL in 4m 39s`. I started a
redundant second build on top of it.

**Why:** "no output + artifact missing" is indistinguishable from failure when
the output is buffered and the check is mid-write. Absence of evidence got
reported as evidence of failure.

**How to apply:** redirect long builds to a real log file
(`cmd > build.log 2>&1; echo "EXIT: $?" >> build.log`), never through `tail`.
Judge success by the recorded exit code and the tool's own success line — never
by "is the process gone" or "does the file exist yet". Related:
[[geoguesser-release-build-steps]].
