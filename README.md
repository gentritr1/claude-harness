# claude-harness

The cross-project Claude Code setup that belongs to no single project: the Working Harness rules, the process
ledger, every project's memory, the custom agent and the skill-update scripts. Private repo, because the memory
notes describe client and personal projects.

Each item here is the real file; `~/.claude/...` holds a symlink to it, so whatever Claude writes lands in this
repo. Commit and push from here like any other repo.

| In this repo | Linked from |
|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` (loaded in every project) |
| `process-metrics/` | `~/.claude/process-metrics` (§10 ledger, `bin/` tools, `reports/`) |
| `memory/<folder>/` | `~/.claude/projects/<folder>/memory`, one per project |
| `agents/` | `~/.claude/agents` |
| `skill-updates/` | `~/.claude/skill-updates` (scripts, upstream list, state, reports) |
| `launchd/com.gentlegen.skill-updates.plist` | a copy, not a link: install by hand (below) |

Kept on the computer only (`.gitignore`): `process-metrics/cache/` (66 MB of transcript digests, rebuilt by
`harness-audit`), `process-metrics/hooks/` (the fg-wait hook log, written on every Bash call),
`skill-updates/logs/` and `skill-updates/removed-*/` (copies of third-party skills).

The gold-pdf-bot memory is not here: it lives in that project's repo at `docs/agent-memory/`.

## Restore on a new computer

```bash
git clone git@github.com:gentritr1/claude-harness.git ~/claude-harness && ~/claude-harness/link.sh
```

`link.sh` is safe to re-run. It never overwrites: if a real file already exists on both sides it prints `STOP` and
exits 1, so merge that one by hand and run it again. Run it again later to move any new project memory folder into
the repo.

Keep the clone at `~/claude-harness` (not under Desktop, Documents or Downloads): the daily skill-update job runs
`/bin/bash` from launchd, and macOS privacy protection blocks that from reading those folders.

**Memory folder names hold absolute paths** (`-Users-gentlegen-Desktop-lucky-shelf` is `/Users/gentlegen/Desktop/lucky-shelf`).
They link correctly only when the username and project paths are the same. Otherwise rename the folder in
`memory/` to the new path with `/` and `.` replaced by `-`, then run `link.sh`.

### Not in this repo: reinstall by hand

- **settings.json** (permissions, hooks) is never copied. Re-add the fg-wait hook as a `PreToolUse` Bash hook with
  the command `sh <agent-playbooks clone>/tools/hooks/fg-wait-guard.sh`.
- **Plugins** (user scope, 17 Oct 2026): superpowers 7.0.0 and expo 1.13.9 (`anthropics/claude-plugins-official`),
  paddle and ponytail 4.9.0 (`anthropics/claude-plugins-community`), pinescript-plugin 0.5.0
  (`jpantsjoha/pinescript-plugin`), agent-playbooks (`gentritr1/agent-playbooks`, public; working copy at
  `~/Desktop/Projects/agent-playbooks`). Add each marketplace with `/plugin marketplace add <owner/repo>` and install.
- **Third-party skills** in `~/.claude/skills`: the sources are in `skill-updates/upstream.txt` and
  `skill-updates/skills.txt`. Also `~/.agents/skills` (pr, retro, writing-for-agents and others) and
  `~/.codegpt/skills` (browser-automation, game-development), which `~/.claude/skills` links into.
- **earshot** (`~/.claude/tools/earshot`, 2.8 GB with models): `git clone https://github.com/Leonxlnx/earshot
  ~/.claude/tools/earshot && git -C ~/.claude/tools/earshot checkout 108763c`, then create `.venv` and
  `pip install -e .` there; link `skills/earshot` and `skills/real-sound` into `~/.claude/skills`; register the
  `earshot` MCP server at user scope.
- **Skill-update schedule**: `cp launchd/com.gentlegen.skill-updates.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.gentlegen.skill-updates.plist`
  (the plist names `/Users/gentlegen`; edit it if the username differs).
