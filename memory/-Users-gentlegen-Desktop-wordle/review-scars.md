---
name: review-scars
description: Patterns that escaped FJALË reviews — detection rules for future briefs
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a376e78-fea1-4e3f-b833-76f2dbc19ef6
  modified: 2026-08-11T21:17:03.261Z
---

Escapes caught only by a second independent review (2026-07-16):

1. **Live-timer boundary never exercised** — countdown verified ticking mid-interval, but at Tirana midnight it flipped to 24:00:00 (helper always measures to *next* midnight; `<= 0` branch was dead code).
   **Why:** "it ticks" proves the steady state, not the terminal instant.
   **How to apply:** any countdown/rollover feature closes only with a fake-clock run STARTING ~30s before the boundary; briefs must name that exact scenario. Dead branches (`if (x <= 0)`) are a smell that the boundary was never hit.

2. **Fixed min-size cells in a grid clip at 320px** — calendar cells `min-height:40px; aspect-ratio:1` × 7 columns overflow a 320px viewport; only 390px was checked.
   **Why:** smallest-device check was in the global harness but not named in the brief, so it didn't happen.
   **How to apply:** any new grid/row UI needs 320px AND 390px screenshots named as acceptance criteria.

3. **LLM-drafted Albanian copy carries agreement errors** (gender/number: "E bardhë" for masc., adjective–noun disagreement) and occasional non-words ("buneshme", "thelbinj").
   **How to apply:** treat generated Albanian as UNVERIFIED until a native pass; grep-able checklist: adjective agreement, definite forms, plural clusters.

4. **Clue/hint features can leak the answer through DATA, not code** — hint round 2026-07-19: code correctly stopped printing syllable spelling, but two editorial clues contained the word's own stem (ROSAK → "Rosa…", FJALË → "fjali"), one inside the daily pool.
   **Why:** the delegate verified the rendering path; nobody audited the 138 clue strings the path now charges an attempt for.
   **How to apply:** any feature surfacing per-word editorial data closes only with a data sweep (script: flag clue containing the word or a ≥4-char stem); briefs must name the sweep. See [[hint-attempt-design]].

5. **Interactive chips fail in state COMBINATIONS, not single states** — 2026-07-20 production report: Besa button unreadable when `[aria-pressed="true"]` (ink fill) met global `button:disabled { opacity:.48 }` (game over), and `<select>` flashed the fat blue ring on every mouse click because Chromium marks mouse-opened selects :focus-visible.
   **How to apply:** any stateful control ships only after checking the full matrix — default/hover/pressed/disabled/pressed+disabled — in BOTH themes; `color-mix(in oklch, …)` between amber and near-white drifts salmon-pink, prefer designed token pairs (primary-pale + primary-deep, the spent-hint-row combo).

6. **"Flag-off = byte-identical" claims leak through NON-JS surfaces** — PR #1 review 2026-08-03: the JS gating was airtight (host-checked override, hidden DOM, a11y-clean), but flag-off users still got (a) a real behavior change in the game layer (`if (mode === "daily")` collection gate not tied to any flag — old vs new game.js executed with same input gave opposite results), (b) 24 avatars added to the SW precache/APP_SHELL, (c) a hidden `<img src>` that still fetches (executed: performance.getEntriesByType showed the request), (d) unconditional copy edits.
   **How to apply:** a byte-identical claim closes only by executing OLD vs NEW logic modules with identical inputs AND diffing the SW precache list, network waterfall, and rendered copy with the flag off. "The flag gates the UI" is not evidence — flags don't reach HTML, service workers, or ungated logic branches.

7. **A spec that pins BOTH an algorithm and an acceptance case can contradict itself** — Rrethi M1 2026-08-11: §4.2 specified `seat = MAX(seat)+1` while §4.3(a) required a claim to succeed after a *middle* seat is freed. With `CHECK (seat BETWEEN 1 AND 10)` those cannot both hold — nine members on seats 1..3,5..10 compute seat 11 and raise 23514 (not the 23505 the retry loop handles), so a once-full circle becomes permanently unjoinable. Same round, §0 put the `rate_bucket` prune in M2 while §3.1 had M1 running it, and §10's line 2 ("no store method is called") contradicted its own line 40.
   **Why:** long specs get reviewed section by section; nobody hand-simulates the acceptance case against the algorithm two sections earlier.
   **How to apply:** before implementing a spec that states an algorithm AND a numbered acceptance case, hand-simulate each acceptance case against the stated algorithm and list the contradictions FIRST. Implement the fix, record it as a numbered deviation in the spec itself, and flag it — do not silently satisfy the test.

8. **Never identify a row by roster position in a test** — the week-masking test used `listMembers(code)[0]` to mean "Ana" and failed 6 runs in 8: two members created in the same millisecond share a `joined_at`, and that tie breaks by `member_key`, which is an HMAC (effectively random order). The symptom looked like a masking bug in the implementation.
   **How to apply:** tests name the entity by its key, never by index into a sorted-by-timestamp list. A test that fails intermittently after a *code-free* edit is a data-ordering tell, not a flake to re-run.

9. **Editing any file in the service-worker precache trips three separate pins** — adding one `export` keyword to `src/game.js` failed `npm run check` via `scripts/check-cache-version-bump.mjs`, then failed `tests/launch.test.js` in three places (the `readCacheVersion` pin, the `did not advance beyond fjale-shell-vNN` regex, and the `{previousVersion, currentVersion}` deepEqual).
   **How to apply:** touching `src/*.js` means bumping `CACHE_NAME` in `service-worker.js` AND updating all four pins in `tests/launch.test.js` in the same commit.

See [[archive-verification-technique]] and [[retention-plan-2026-08]].
