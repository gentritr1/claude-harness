---
name: jira-sheets-project
description: "Jira → Google Sheets add-on (Oct 2026) — repo, spec rev 4.1 status, phase plan A–D, Gmail-only Google setup, test deployment, which account/project to use"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bb56d09-6e53-4a9f-87a4-708273fd5c90
  modified: 2026-10-14T22:38:37.925Z
---

Repo `SnaxxTech/jira-sheets` (private; local `~/Desktop/Projects/jira-sheets`, branch `feat/v1`). Spec `docs/superpowers/specs/2026-10-14-jira-sheets-design.md` is at **rev 4.1, approved 2026-10-14**. §9.8 overrides §9.1–9.7.

Phases:
- **A (done 2026-10-15):** UI pass, red/amber tab health, change diff, Key links, empty-result guard. Acceptance is recorded in `docs/verification/acceptance-2026-10.md`.
- **B:** OAuth probes P1–P7.
- **C:** Sign in with Atlassian for the owner.
- **D:** team sign-in, which needs Atlassian "Sharing" and a privacy URL. The privacy page is PR gentritr1/snaxx-tech#4, at `/jira-sheets/privacy`.

Google side:
- Everything is in the **S** Gmail (snaxxtechadm). Cloud project `cobalt-carver-511619-v0`; script ID in `.clasp.json`.
- **Test sheet:** "Jira Sheets – test". Jira site `techsnaxx.atlassian.net`, project SCRUM, 250 seed issues plus SCRUM-255.
- **Comparison sheet:** "Atlassian Sheets – side by side", which has Atlassian's "Jira Cloud for Sheets" installed (it can access all spreadsheets: uninstall when done).
- Never use the Vianova account.

**Claude in Chrome runs in the owner's personal "g" profile, not S**, so it can't open S sheets. Use the built-in browser pane, which is signed in as S.

Owner wants, after phase A:
1. a UI review with ui-ux-pro-max, emil-design-eng and impeccable;
2. an "Ours vs Atlassian" comparison page on GitHub mapping each user complaint to our answer;
3. a `/brag` demo video added to the repo.

`/brag` and `/brag-slim` were installed globally in `~/.claude/skills/` on 2026-10-15 from latent-spaces/brag@069432c.

**Why:** the owner wants a more reliable Jira → Sheets connector than Atlassian's (Atlassian's still wipes the tab on a JQL typo, renders mentions as raw account IDs, and asks for access to all spreadsheets). It might later become a Paddle product.

**How to apply:** this file describes progress up to 2026-10-15. For later work, trust the SDD ledgers in `.superpowers/sdd/` and `git log` over this file. Claude never pastes tokens or approves OAuth for the owner.

Related: [[notes-mining-opportunity-map]]

- 2026-10-15 lesson: my "Old rows kept." fix only changed the status line, but the same promise lived in 3 more places (banner, A1 note, cleanup throw), and the audit script exited 0 on every failure. Pattern → rule: when fixing a false user-facing claim, grep every surface that renders that state (status, banner, A1 note, toast) and run a harness that counts true-hits before vs after. Every e2e script must be proven to exit 1 on a broken input.
- 2026-10-15: feat/v1 pushed to origin at 02c12f4 (255 tests). The mp4 was stripped from history before the push; the video is hosted as prerelease asset `video-2026-10-15` (sha256 d17ded8c…). docs/media/brag/*.mp4 is gitignored. Local backup branch backup/feat-v1-before-mp4-removal still holds the mp4 and can be deleted. Build deployed to the test add-on; real-sheet checks pending.
- 2026-10-15 lesson (Batch 3): the Sheets API can't tell a typed value from a spilled array-formula value (getFormulas is '' for both). Two guessing rounds both moved user data wrongly, so the third was a redesign: refuse the move when a user column holds any spill-capable formula. Rule: when an API can't distinguish two states, refuse rather than guess, and delete the guessing code.
- 2026-10-15: Batch 1 (pre-write check, clear errors, sidebar refresh) and Batch 3 (your columns follow their issue) are done, real-sheet accepted and owner-approved. The switch defaults on for new tabs (8583439). 587 tests. Pushed to origin/feat/v1 at 8583439 on 15 Oct 2026. Open: R10 timing on the 250-issue tab; real hourly trigger cycle (R13) never run.
- Real-sheet driving gotchas: the browser pane can't type into Google's grid (use the formula bar, or a QA seed item); cmd+a doesn't work in the sidebar iframe (use BackSpace/Delete ×100); a grey box with a name label is another open tab's collaborator cursor, not formatting.
- 2026-10-15: PR SnaxxTech/jira-sheets#1 (feat/v1 → main) merged at 7748275 after 2/2 CI checks passed. feat/v1 is kept for phases B–D.
