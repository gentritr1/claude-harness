---
name: speed-audit-2026-10-07
description: "Measured where helper time goes (93 agents, 101 active h); builds only 6%; test-APK template regressed to clean+x86_64; ledger seeded"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-10-06T23:24:36.301Z
---

Audit 2026-10-07 (docs/process/speed-audit-2026-10-07.md, scripts/process/agent_time_audit.py, commit 12ab855): 101.3 active helper-hours = model time 34% (≈11 s per 1k output tokens, independent of context size), emulator perf/gate series 23%, analysis/driver scripts 9.5%, jest 7% (55 s quiet vs 219–777 s under host load), builds only 6%. 80% of calendar time nothing ran; helpers mostly ran one at a time.

My earlier guess that builds were the main bottleneck was WRONG — check the ledger before claiming. Real waste: October test-APK template regressed to `prebuild --clean` + `arm64-v8a,x86_64` (5.7–35 min) vs September incremental arm64-only (~1 min); both emulators are arm64, x86_64 never runs. Top experiments: arm64-only test APKs, offline replay of an early-stop rule on archived perf series (7–9 h), incremental gradle with byte-identical guard, host-load gate before perf/builds.

**Why:** the owner's §10 self-harness rule (global CLAUDE.md) requires decisions from the ledger `~/.claude/process-metrics/arrows-game.jsonl` (89 lines seeded; re-run the script with the session's subagents dir to append).
**How to apply:** route changes that alter a build artifact go to the owner with numbers; Play AAB recipe stays clean + both ABIs. Related: [[w3-15-w7-09-gotchas]], [[shared-host-contention]].

**Graphify trial 2026-10-07: REJECTED** (docs/process/graphify-trial-2026-10-07.md, 449194e). graphifyy 0.9.78: 3/12 correct, 9 partial, confidently-wrong answers labelled EXTRACTED; no query-time freshness check (4/4 stale after edits, exit 0, no warning); "incremental" update ≈ cold build (~23 s); realistic cost: median per question −7.5 %, total +11.5 % vs grep+read; venv 120 MB in scratch. A stamp guard (commit + diff + untracked hash) worked (0.3 s). Don't retry without a new reason (new major version with query-time freshness + value extraction). Cheap alternative pending owner yes: hand-tagged index of engineering-lessons.md with a hash test (~4k tokens/agent saved).

**fg-wait-guard hook LIVE 2026-10-07 11:45** (owner registered it in ~/.claude/settings.json; script agent-playbooks/tools/hooks/fg-wait-guard.sh; log ~/.claude/process-metrics/hooks/fg-wait.jsonl). Judge on 2026-11-06 per CLAUDE.md §11: fg Bash ≥300 s per 1,000 down ≥50 % in arrows-game and geoguesser, workaround detector flat, zsh `=` null. Agents cannot edit Claude settings themselves (auto-mode Self-Modification block) — owner applies config.

**Skill listing budget raised 2026-10-07:** owner set `skillListingBudgetFraction: 0.02` (default 0.01; undocumented, found in CLI 2.1.269) because 126 installed skills need ~43k listing chars vs ~8k budget and new agent-playbooks skills showed name-only. Verify in the NEXT session that agent-playbooks descriptions appear; if not, recommend disabling unused plugins (pinescript, miro, unused expo/eas) instead.

**Memory-tool trial 2026-10-08 (Obsidian etc.):** refined grep (file + `description:` line, then read one note) won: 12/12, total −41 %. MCPVault REJECT (write tools on memory, 10.9k schema chars/session); basic-memory REJECT (first sync rewrote 528/536 notes; AGPL); Hindsight NOT TRIALLED (needs a cloud LLM over all notes incl. keys — owner decision); Obsidian app OK for OWNER browsing only, on a read-only rsync copy (`~/MemoryVault`), never on live memory (a rename rewrote MEMORY.md). Doc: docs/process/obsidian-memory-trial-2026-10-08.md.
