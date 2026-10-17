# harness-audit

Cross-project self-harness audit of Claude Code transcripts (`~/.claude/projects/**/*.jsonl`).
python3 stdlib only, no installs. Built 2026-10-07; parser ported from
`arrows-game/scripts/process/agent_time_audit.py` v1 (same Bash categories, call pairing and exclusive time attribution).

## Run

```sh
# full pass, all projects (first run ~4-10 min on 4 GB; later runs reuse the digest cache)
nice -n 10 ~/.claude/process-metrics/bin/harness-audit
# one project, a date window, no ledger writes
nice -n 10 ~/.claude/process-metrics/bin/harness-audit --project geoguesser-app --since 2026-09-01 --no-ledger
# self-test on a synthetic fixture (classifier, redaction, loops, ledger idempotency, cache invalidation)
~/.claude/process-metrics/bin/harness-audit --self-test
```

Run a full pass in the background (`run_in_background`) and wait for its exit; it prints progress to stderr.

### fg-wait-guard experiment (CLAUDE.md §11)

```sh
# frozen baseline (done 2026-10-07; refuses to overwrite; --force needs --reason, which is stored in the file)
harness-audit --fg-wait-baseline --since 2026-09-07 --until 2026-10-07T11:45 --no-ledger
# judgement on or after 2026-11-06: post window = baseline end .. now, rule FG-WAIT-R1 read from the frozen file
harness-audit --judge-fg-wait
```

The hook's own log (`hooks/fg-wait.jsonl`) records decisions, never outcomes, so it cannot judge the experiment;
the judgement comes from transcripts. Baseline: `reports/fg-wait-baseline-2026-10-07.{json,md}` (A = foreground
Bash calls >= 300 s per 1,000 Bash calls; B = foreground call-hours on calls >= 120 s; WA = workaround detector;
NULL = zsh `=` failures; strata arrows-game and geoguesser-app, plus `all`). `fg_wait.py` holds the metrics, the
Poisson noise bounds and the pre-registered rule; `selftest.py` checks the detector on positive and negative
fixtures and the judge on synthetic SUCCESS / NO-EFFECT / REMOVE-HOOK / INCONCLUSIVE / INSUFFICIENT data.

## Ledger check (§10 grade)

```sh
ledger-check arrows-game            # which §10 thresholds are computable, and field coverage
ledger-check --migrate-v1 PROJECT   # dry run; --write appends MIGRATION lines for schema-less v1 records
ledger-check --self-test
```

Thresholds: T1 >= 5 tasks; T2 class median (>= 3 tasks in a class other than the fallback `other`); T3 the last 5
tasks carry wall_min and cat_min (60 min / 15 % share); T4 approved-first-time per hour (>= 5 tasks with a recognised
outcome, wall_min and route_version). Transcripts cannot give conditions, outcome or route version, so T4 stays
NOT COMPUTABLE until the controller appends lines like the template below.

### Controller line template (one per brief, appended by the controller; corrections are new lines)

```json
{"schema": "process-metrics/2", "task_id": "W7-12", "parent_id": null, "kind": "brief", "project": "arrows-game",
 "class": "feature", "date": "2026-10-08", "purpose": "short label, no prompt text",
 "wall_min": 42.0, "active_min": 38.5, "tool_calls": 131, "tokens": 51234,
 "cat_min": {"builds": 6.1, "tests": 3.2, "adb_capture": 4.0, "waits": 1.5, "model": 20.3, "other": 3.4},
 "builds": {"n": 3, "min": 6.1, "full_vs_incremental": "1 clean / 2 incremental"},
 "tests": {"n": 4, "full_n": 1, "min": 3.2}, "timeouts": {"n": 0, "min": 0}, "retries": {"n": 1}, "rereads": {"n": 2},
 "conditions": {"loadavg_start": 7.9, "loadavg_end": 12.4, "disk_free_gb": 31.5, "shared_emulator": true},
 "owner": {"round_trips": 1, "blocked_min": 12.0},
 "outcome": "approved-first-time", "route_version": "test-apk-route/E3-2026-10-07",
 "source": "controller (loadavg from `sysctl -n vm.loadavg` at brief start and end; disk from `df -g .`)"}
```

`outcome` is one of `approved-first-time`, `changes-requested`, `reverted`, `reopened` (a later line with the same
`task_id` records a reopen). Unknown values are `null`, never estimated.

## Outputs

| path | what |
|---|---|
| `reports/tool-reliability-<date>[-<project>].md` | method, count reconciliation, per-tool reliability, failure causes (ENV / TOOL / BEHAVIOUR / SIGNAL), loops and double work, tool-choice comparisons, skills, host concurrency, per-project summary. A `<!-- BEGIN MANUAL -->...<!-- END MANUAL -->` block in an existing report is preserved on regeneration. |
| `reports/...json` | the same aggregates as JSON |
| `<project>.jsonl` | §10 ledger: one line per transcript (subagent or main session), `schema: process-metrics/2`; schema-less v1 lines are kept and overlaid by `migrates` lines. Append-only and idempotent on `task_id`; transcripts active in the last 30 min are skipped until a later run. Fields that transcripts cannot give (loadavg, disk, shared emulator, route version) are `null`, never estimated. |
| `cache/digests/*.json` | one digest per transcript, keyed by path + size + mtime + parser version; a changed file is re-parsed. |

## Privacy

Digests, reports and ledger lines hold tool names, categories, timings, hashes, program names (`npx jest`, never arguments)
and, for failures only, one redacted signature line of at most 120 characters (user paths -> `~`, keys, tokens, emails and long
opaque strings removed). No prompt text, file content or command text is stored. Subagent `purpose` is the dispatcher's short
description label, redacted.

## Files

- `harness_core.py` - streaming parser, Bash categories, error-cause classifier, redaction, digest cache.
- `harness_analysis.py` - aggregation: reliability, loops, double work, comparisons (within-agent Mantel-Haenszel), skills, concurrency, ledger.
- `harness-audit` - CLI and markdown rendering.
- `selftest.py` - synthetic fixture and checks.
- `fg_wait.py` - fg-wait-guard baseline, workaround metrics and the judge.
- `ledger-check` - §10 threshold computability, field coverage, v1 migration.

## Known limits

- Error cause = first matching rule on the result text; extend `classify_error` when the report's "other" share passes 10 %.
- "Unchanged tree" for rebuilds and test reruns is inferred within one transcript (no Edit/Write and no mutating shell command
  in between). Changes made by another agent or the owner in the same checkout are invisible, so treat those counts as upper bounds.
- Near-duplicate dispatch uses 5-word-shingle Jaccard on bottom-128 sketches; fix rounds that reuse a brief template can score high.
- Skill effects are associations only; the contradiction checks are heuristics over tool sequences.
