---
name: gate-commits-on-the-exit-code
description: "Chain the commit to the test exit code, and keep every run's full output — a red run once got committed and the failing test could not be named"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-02T04:33:43.695Z
---

On 2026-10-02 I ran `npm test` and a `git commit` in the same shell call, reading only the summary line. The run was
**904/905 — one failure** — and the commit (3b6ecef) went in anyway, because nothing tied the commit to the test result.
I had also printed only the `# fail` count, so the failing test's name was gone. Five further full runs were green, so it
was intermittent, and with no saved output it could not be identified — only guessed at. The guess (a background fill
leaking into the next test's stub) was WRONG: the cause turned out to be timer floors with zero slack
([[timer-floor-assertions-need-slack]]), found only once a later run's full output was kept.

**Why:** a flaky failure is exactly the kind you get one chance to read. Summarising a run before checking it, and
committing in the same breath, throws that chance away and puts an unverified state on the branch.

**How to apply:**
- Write every test run to a file first (`npm test > $S/run.out 2>&1`), then read the summary from the file. Keep the file.
- Gate the commit on the exit code: `npm test > out 2>&1 && git commit …`, never `npm test …; git commit …`.
- On any failure, grep the saved output for `not ok` and its `error:` before re-running anything — a re-run that passes
  erases the evidence of a flake.
- Same for the ledger: never append a "merged / done" line in a separate statement after a `&&` chain — on 2026-10-04 a
  fast-forward merge failed (main had diverged), the chain stopped, and the separately appended ledger line still said
  "ff onto feat/next-level". Chain the ledger line to the action, or check the result first. When a reviewed branch
  cannot fast-forward and the files are disjoint, merge with `--no-ff` (keeps the reviewed hashes) and re-run the suite.
- **It happened AGAIN on 2026-10-04 (D2-2):** `git merge --ff-only ... && git log; <gate>; <row edit>; <ledger echo>; git commit && git push && git worktree remove && git worktree add` — the ff failed (an assets commit landed after the branch point), and every `;`-separated step still ran: a false "ff" ledger line, a pushed handoff row, the reviewed worktree removed, and a new worktree cut from a tree WITHOUT the unit. The gate's test count (2219, not 2275) was the tell I printed and did not read. Rule now: run the merge in its own call, read its result, then do the bookkeeping; or wrap the whole sequence in `set -e`. Check the merged suite's COUNT against the branch's before any bookkeeping.
- An intermittent failure is a finding in its own right: record it with the suspect and the run count, never let "the
  next run was green" close it.

Related: [[every-gate-we-write-ships-a-silent-pass]], [[dont-pipe-long-builds-through-tail]].
