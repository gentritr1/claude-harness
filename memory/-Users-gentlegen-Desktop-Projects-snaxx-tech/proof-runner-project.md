---
name: proof-runner-project
description: "Proof Runner v0 (Oct 2026) — repo, branches, jira-sheets worktree, evidence numbers, open owner decisions, and the review lesson about rehashed forgeries"
metadata:
  node_type: memory
  type: project
  originSessionId: 085731ec-3fcf-4cd7-933c-43b37ee3cc1b
  modified: 2026-10-15T14:01:30.181Z
---

Proof Runner: a CLI plus a GitHub Action that turns a repo's written claims (proof.yaml) into re-runnable checks and an evidence page. It is the "Proof House" bet. See [[notes-mining-opportunity-map]] and [[deeper-version-planning-prompt]].

**Where things are (15 Oct 2026):**
- Repo: ~/Desktop/Projects/proof-runner, remote SnaxxTech/proof-runner (private; the owner created it on 15 Oct 2026). `main` holds the spec and the plan. `feat/v0` holds the build, made with subagent-driven development; the ledger is in .superpowers/sdd/.
- jira-sheets work: branch `proof/v0` in the worktree ~/Desktop/Projects/jira-sheets-proof-v0. It is local only and not pushed. The main jira-sheets checkout was left on feat/v1, because other sessions use it.
- First real run (jira-sheets fd65a56): PASS. crash-sweep: 766 fault points and 1728 kill pairs. lifecycle-fuzz: 750 steps.
- The planted mutant revert-i1 turns the fuzz red on seeds 115, 169 and 231, while the crash sweep stays green.

**Open owner decisions:**
- Push jira-sheets proof/v0 and its workflow, so the Action can run and the second-machine check can happen.
- Pick a signing option. The key pair is recommended; keyless writes a public log entry.
- Merge feat/v0 to main.
- The /brag video.

**Review lesson (final review, 15 Oct 2026): pattern → detection rule → future brief/test update.**
- Pattern: a tamper suite that only edits fields, and never recomputes the hashes, cannot test the re-run defence. A self-consistent forgery (a duplicate-id claim with recomputed results_sha256) got MATCH, because verify trusted a label-keyed diff instead of comparing the hashes.
- Detection rule: verify's MATCH must compare the recomputed hashes, and the diff only explains a mismatch.
- Brief/test update: tamper tests must include rehashed forgeries.
- Same review: a `proof page` render of untrusted JSON needs every field escaped, including numbers, and an origin URL can carry user:token into evidence.

**State on the evening of 15 Oct 2026:**
- PR SnaxxTech/proof-runner#1 (feat/v0 into main) is open and mergeable.
- jira-sheets proof/v0 is pushed (fd65a56).
- The brag video is done; it is in the brag-output/ folder of the side-session notes.
- The C1 forgery hole is fixed, and the re-review approved it.

**Still open:**
- No jira-sheets workflow file yet, so the Action has never run on GitHub and the second-machine check has not happened.
- The signing choice.
- Items parked for v0.1: the overclaim at signing-evaluation.md:3; a huge derived count can run out of memory; the CLI MATCH line does not mention the unhashed fields.

**First Action run, 15 Oct 2026:** jira-sheets proof/v0 @ 709153c, run 38767548385, success. Linux x64 and Mac arm64 records have equal hashes (results e5b7adfa…); Mac verify of the Linux record gives MATCH. Recorded in proof-runner PR #2 (docs/v0-action-run → feat/v0). proof-runner Actions access is now `organization` (works on the Free plan). Gotchas: workflow_dispatch needs the workflow on the default branch, so a push trigger on proof/v0 was used. Seeds are commit-derived, so a new workflow commit changes the results hash: compare same-commit records, never the old Mac record. Open finding: the CI record has runner.commit null (action_path has no .git).
**Merged, 15 Oct 2026:** PRs #2 and #3 into feat/v0, then #1 into main (merge commits; main = ec621bf). The runner.commit fix (#3, 32b549b) is proven in CI: run 38771889907 recorded runner.commit 32b549b. jira-sheets proof/v0 (bc98d11) is pinned to 32b549b, which is reachable from main.
**jira-sheets main, 15 Oct 2026:** proof/v0 merged via jira-sheets PR #2 (affc5ba). First proof run on main 38773382601: PASS (results 6950c866…), ci green. proof.yml still lists proof/v0 in its push branches (cleanup later). Launch video v2 (27.6 s, adds the Linux=Mac scene): side-session-notes/local_e7935713…/brag-v2/proof-runner-v0.mp4; owner look-acceptance pending.
- 17 Oct 2026 Fable attack review: main ec621bf, 109 tests pass (README still says 88). Broken by EXECUTED attacks: (A) a control patch may touch the test itself, and a check asserting nothing still passes, so a broken lib got a full PASS; (B) the derived seed sha256(commit:claim:0) can be mined by amending until green. Also: no sandbox (verify = running a stranger's code with your HOME); environment/runner/created_at sit outside the hashes; no LICENSE file. Differentiator: the catch matrix (claim × planted bug, re-runnable). Fixes before NLnet 3 Nov: verifier-chosen seeds, mutant scope rule + assertion check, hash all fields, one outside verifier, a spec page, README + license. CHECK: NLnet's reported draft policy on mostly-LLM-generated work (nlnet.nl/news/2026/20260903-call.html) before applying.

- 17 Oct 2026, owner decision: NO NLnet application. Proof Runner stays a free, open project (Apache-2.0). The v1 hardening continues on feat/v1-hardening. The GenAI statement draft (in the side-session notes) is still wanted for honesty, not for a grant.

- 17 Oct 2026, v1 hardening done on local branch feat/v1-hardening (ec621bf..0968cdb, NOT pushed), 146 tests.
  - Closed: seed mining (verifier --seed-salt challenge, exit 5); planted bugs editing the check (scope rule + must-fail contract, patch-rejected); every field hashed (format v1: context_sha256, manual_evidence in inputs, self-reported ci).
  - Added: docs/format spec, JSON Schema, tools/verify_integrity.py (20k-value differential fuzz agreed with the JS).
  - Real jira-sheets 2e3e66c run: PASS, MATCH, challenge PASS, Python OK.
  - Lesson: reviewers kept finding doc sentences that overstate (e.g. "likely to fail" a challenge). Every doc claim about a probabilistic defence needs the per-seed rate caveat.
  - Open: Task 6 (README first screen, LICENSE Apache-2.0, GenAI section) waits for the owner's edited text; push/PR needs the owner's yes; CI still pins the v0 runner.
