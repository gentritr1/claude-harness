# fg-wait-guard baseline (frozen 2026-10-07T12:16+02:00)

Window 2026-09-07T00:00+02:00 .. 2026-10-07T11:45+02:00 (call start time, local host clock). Parser `harness-audit/1.5`. Metrics sha `2ff107eba1779564`. Written by `harness-audit --fg-wait-baseline`; do not edit, rebuild only with `--force` and a recorded reason.

Rebuilt with --force: rebuilt the same day before any judgement: parser 1.5 treats heredoc bodies as data (1.4, frozen 12:13 and never used, counted edit scripts that merely mention sleep( or a wait script)

| metric | arrows-game | geoguesser-app | all |
|---|---|---|---|
| Bash calls (denominator) | 16169 | 18087 | 52624 |
| foreground Bash calls | 15784 | 17617 | 51347 |
| A: foreground calls >= 300 s | 271 | 193 | 584 |
| A per 1,000 Bash calls | 16.76 | 10.671 | 11.098 |
| B: foreground call-hours on calls >= 120 s | 52.81 | 40.6 | 122.93 |
| B hours per 1,000 Bash calls | 3.266 | 2.245 | 2.336 |
| NULL: zsh `=` failures | 99 | 63 | 224 |
| NULL per 1,000 | 6.123 | 3.483 | 4.257 |
| WA: workaround forms (total) | 38 | 12 | 180 |
| WA per 1,000 | 2.35 | 0.663 | 3.42 |
| WA wa:py-sleep | 13 | 1 | 15 |
| WA wa:node-sleep | 18 | 4 | 29 |
| WA wa:read-t | 0 | 0 | 0 |
| WA wa:timeout-tail | 0 | 0 | 118 |
| WA wa:wait-script | 1 | 0 | 1 |
| WA wa:bg-wait-timeout | 6 | 7 | 17 |
| gap form gap:for (not judged) | 40 | 17 | 77 |
| gap form gap:cd (not judged) | 96 | 8 | 108 |
| calls the hook predicate would deny | 140 | 146 | 336 |

Reconciliation: A <= foreground calls <= Bash calls in every column; `all` >= the sum of the two strata.

Workaround forms (foreground only, except the last): inline python sleeps (`python -c`/heredoc with `sleep(`), inline node/bun/deno `setTimeout`/`setInterval`/`sleep(`, `read -t N`, `timeout N tail -f`, scripts or tools named `*wait*` (`wait-for-it`, `wait-on`, `wait_ready.py`), and background wait loops whose task ended `failed` or `killed` (the digest has no exit code, so this is the proxy for "ended by its timeout").

## Pre-registered rule FG-WAIT-R1 (registered 2026-10-07)

- **success:** A per 1,000 Bash calls is down >= 50 % vs the baseline in BOTH strata, and in each stratum the post count is below the 5th percentile of Poisson(baseline rate x post Bash calls), i.e. the drop beats count noise
- **workaround_flat:** in each stratum the post workaround count (sum of WA_KEYS) is at or below the 95th percentile of Poisson(baseline rate x post Bash calls); above it in either stratum = ROSE
- **null_flat:** in each stratum the post zsh `=` failure count lies inside the central 95 % Poisson interval of baseline rate x post Bash calls; outside it in either stratum = the population moved
- **not_judged:** B (call-hours) and gap forms (for loops, cd && prefixes) are reported only; they are legal by design
- **min post Bash calls per stratum:** 1000
- **INSUFFICIENT:** a stratum has fewer than min_post_bash_calls post Bash calls, or a zero baseline A count
- **REMOVE-HOOK:** the workaround detector ROSE (§11: remove the hook if workarounds rise)
- **INCONCLUSIVE:** the null moved, so a change in A cannot be attributed to the hook
- **SUCCESS:** success condition met, workarounds flat, null flat
- **NO-EFFECT:** anything else

Judge: `harness-audit --judge-fg-wait` (post window = baseline end .. now, same parser features).
