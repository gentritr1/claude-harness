---
name: codex-delegation-setup
description: How next-level leftovers are delegated to Codex CLI (flags that work in its sandbox, no-commit rule, where prompts live)
metadata:
  type: project
---

From 2026-09-19 the owner asked that the remaining next-level tasks be implemented by Codex, with
Claude reviewing. Setup that works (probed with `codex sandbox`): `codex exec -C <repo> -s
workspace-write -c approval_policy='"never"' -c sandbox_workspace_write.network_access=true --add-dir
~/.gradle --add-dir ~/.android --add-dir ~/.npm --output-schema <schema> -o <result.json> - < prompt.md`.
In that sandbox adb (-s emulator-5556), Gradle cache writes, repo writes and docs.expo.dev all work.

Prompts, shared constraints (GLOBAL.md) and results live in the gitignored
`.superpowers/sdd/TASKS/codex/`. Codex never runs state-changing git; Claude reviews the working-tree
diff and commits (owner's "Claude owns git" split, see [[owner-rulings-next-level-2026-09-16]]).

**Why:** Codex doesn't get CLAUDE.md, so the owner's verification rules have to be restated in
GLOBAL.md; without network/add-dir flags gradle and adb fail inside its sandbox.

**How to apply:** one Codex run at a time (shared emulator + disk, see [[shared-host-contention]]);
run it with run_in_background and review when notified.

**Gotcha (2026-09-19, W6-08):** the Android emulator cannot start inside Codex's seatbelt sandbox
(exit 132 headless; Qt ARM NEON detection fails with -gpu host), even with ~/.android writable. Claude
must boot `fleet_floor_api31 -port 5556` itself before an emulator task. Codex also once ran a bare
`adb reconnect` that bounced the other session's emulator-5554 — GLOBAL.md now forbids any adb call
without `-s emulator-5556`.

**Gotcha (2026-09-19, W6-11):** an `npm install` inside Codex's sandbox left 4 build packages out of
package-lock (`@react-native/{metro-config,metro-babel-transformer,babel-preset}`, hermes-parser), so
`npm ci` failed EUSAGE and CI (ci.yml runs npm ci) went red while every version diff looked clean.
Review rule: any diff touching package.json/package-lock must have `npm ci --dry-run` run against it.
A later real `npm ci` also shrank node_modules from 12 GB to 1.9 GB — repeated installs had been
leaving junk behind, and that was most of the disk pressure.

**Gotcha (2026-10-13, TF-01):** Codex runs fail in ~5 s with `The '<model>' model is not supported when using Codex with a ChatGPT account` — both the config default `gpt-6.1-sol` and the previously working `gpt-5.6-sol` (`-m`). Account/plan issue, not the brief; owner must fix it in Codex. Fallback used: a Claude general-purpose subagent implementing the same brief (GLOBAL.md rules unchanged), Claude reviewing. Also run.sh refuses a dirty tree — an unrelated uncommitted docs/engineering-lessons.md diff (workflow-studio, 2026-10-07) blocked it; record `git diff` as `<task>.prediff` instead of committing someone else's work.
