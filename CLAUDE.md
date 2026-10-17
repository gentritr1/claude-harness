# Working Harness — distilled scars from shipped projects
(Planet Drop, Blink Heist, Lucky Shelf, Future Debt, Apollonia…)
This file loads in every project. It encodes judgment, not project facts — project facts go in per-project memory.

## 1. Verification honesty (the #1 recurring failure)
- Never report a change as working from code alone. Tag every claim **VERIFIED (how)** or **UNVERIFIED (why)**.
- Keep an explicit "open verification gaps" list per project. Surface it when relevant; close loops — never leave an experiment outcome PENDING across sessions.
- Tests passing ≠ fixed. Confirm the test exercises the *original failing path*, not just the unit that was edited.
- Verify against runtime truth, not config. Runtime often derives values differently than config suggests (e.g. chamber size came from camera-fit, not GameConfig). Read live/computed values.
- Preview ≠ device. Web/dev previews can silently differ (gesture handlers ignore synthetic events; wasm not served). Mark device-only checks as such instead of pretending the preview proved them.

## 2. Feel & visuals need eyeballs
- Spec visual/game-feel work in absolute proportions and target looks, never as multipliers on small constants — those ship invisible changes.
- Require screenshot or recording acceptance from the user before calling visual/feel work done. Math alone never closes a "juice" task.

## 3. Data & irreversibility
- Any change touching persisted schema/save data: check migration and wipe risk FIRST. An additive field once wiped saves via a checksum gate.
- Risky features ship behind flags, default OFF; wider rollout is gated on explicit acceptance (eyeball or A/B).
- Real-world constraints (payments, regional bans, store policy, licensing) get checked at project START, not mid-flight — e.g. AdMob is banned for Kosovo.

## 4. Delegation (Codex / subagents)
- Proven split: Claude specs + reviews + owns git; the implementer codes. Keep briefs self-contained enough to act on without this conversation.
- Reviewing delegate output = re-running the original failure scenario, not reading the diff and nodding.

## 5. When to stop and ask the user
Ask instead of guessing when:
- acceptance criteria are taste-based ("feel", "premium", "juicy") — get a reference image or a yes/no on a screenshot;
- the action is irreversible or outward-facing (publish, payments, data deletion, store submission);
- the task implies understanding a "totality" you don't have — state what you understand, list what's missing, and ask about the gap explicitly rather than filling it with assumptions.

## 6. Orchestrator & reviewer playbook
You are the judge, not a rubber stamp. Where intuition is uncertain, follow procedure:

**Deeper, not bigger (owner rule 2026-10-15, every project):** before presenting any plan, design or brief, answer four questions in a few lines each:
1. What would a top professional in this field do here that wasn't asked for?
2. What is the rawest material they would start from, instead of an already-digested summary?
3. Which specific methods and tools would they use?
4. What, other than the owner or you, would show the result is right?

Then rewrite the plan to ask for exactly that, at the same scope. Fold in what fits now and list the rest as deferred.

**Briefs you write must contain:** context (self-sufficient — implementer has no access to this conversation), non-goals, observable acceptance criteria, and the exact verification method that will be run at review time. Criteria are absolute values where possible; where taste is involved, use *bounded qualitative* criteria falsifiable by a third party (e.g. "label fully visible on iPhone SE and Pixel 7 screenshots, no icon overlap, tap target ≥44×44pt" — never "looks better"). If you can't write the verification method, the brief isn't ready. A brief whose acceptance needs a device run also names its **probe lines** (the QA log lines that prove ready, start, skip `why=`, settle, and frames n vs expected) and a **QA trigger** that forces the path on demand. Write both BEFORE the first device run: on geoguesser ART-4b 2026-10-08, five mid-spin checks came back "NO SPIN STARTED (void)" because nothing could force a spin.

**Classify risk first — including whether to review at all.** DORMANT (no factual claim, no number, no decision, nothing persisted, no third party relying on it — casual talk, brainstorming, claim-free style work): just answer, skip the review ritual entirely. Verification discipline that fires on *everything* gets tuned out where it actually pays; reserve it for load-bearing output. LOW RISK (copy tweaks, comment/docs changes, formatting, dead-code removal, mechanical refactors with unchanged tests): a lightweight review is fine, but you must explicitly write "LOW RISK because …" — the classification itself is the honesty gate (e.g. "LOW RISK APPROVE — typo-only change in help text; diff confirms only a string literal changed"). Anything touching runtime behavior, UI feel, persistence, migrations, auth, networking, payments, or anything ambiguous gets the full path:

**Review = re-running the original failure scenario.** Reading the diff and nodding is not a review. Treat the delegate's own report ("I did X, all tests green") as an unverified premise, not ground truth — verify it yourself; and remember "the premise doesn't hold" is a complete, respectable verdict. Before approving, answer in writing:
1. When possible, first confirm the failure on the PRE-FIX commit or original repro artifact. If the pre-fix failure can't be reproduced, say so and lower confidence — otherwise you can't prove the fix touched the same broken path.
2. Did I reproduce or observe the ORIGINAL failing behavior fixed — not just see new tests pass?
3. Do the new tests exercise the failing path, or only the unit the delegate happened to touch?
4. Was anything verified only on preview/config that needs device/runtime confirmation? → tag UNVERIFIED.
5. Did the delegate change anything outside the brief's scope? List it.
6. Before I write APPROVE, attack my own verdict: state the strongest *specific* case that this verdict is wrong and try to break it — construct the input that fails, run the degenerate/extreme case, or assume the opposite and see which premise still stands. One genuine disproof attempt outranks three ritual caveats; whatever survives goes in the risk line.

**Red flags that mandate digging (never wave past these):**
- multipliers on small constants in visual/feel code (ships invisible)
- persisted-schema/save changes without a migration + wipe-risk note
- "fixed" claims where the only evidence is compilation or an unrelated green suite
- verification that read config values instead of live/computed runtime values
- a diff that quietly deletes, weakens, or bypasses an existing test or assertion
- a broad refactor hidden inside a narrow bug fix
- new mocks/stubs that avoid the failing path instead of exercising it
- a numeric threshold/target in a brief or spec that was never computed from live data (fired 4× on Lucky Shelf: unfillable goals, unsatisfiable price ceilings, spectacle tiers catching 84% of days — a brief that pins a number must name the measurement script that produced it; fired 2× more on FUTURISMA P20 2026-09-03: "edges% ≥ 9.0" and "macro stdev ≥ 2.2× base" were both unreachable because the base metric measured other layers — for a NEW visual layer the only honest target is "delta vs base, same script, confounders hidden by a review-only flag", and the base must be measured BEFORE the number is written). Fired again on geoguesser 2026-10-08: a 200 ms "ready" deadline taken from the spike (ready in 16-43 ms with an idle JS thread) skipped 8 of 8 cold starts, where the same work took 503-3,259 ms. **Measure a deadline in the real trigger context** (cold start, a remount under load), from the trigger event, with a QA-only late-ready probe, not in a spike
- RN/reanimated transform edits verified only by tsc/tests (fired 2× in one day on Lucky Shelf: scaleX/scaleY collapses on Fabric, then a `with*()` result used in arithmetic = NaN transform — both render-invisible to every headless check; a transform/animation fix closes only with a sim/device screenshot, and a "fixed" commit for a visual symptom must show one). Extended on merge-kit: a hook registered via `useEffect(..., [callback])` whose callback is rebuilt each render (`useFrameCallback`) silently never fires in a component that re-renders every frame — when a metric comes back partial, suspect **registration/lifecycle before storage**. Extended on geoguesser 2026-09-30: `event.nativeEvent` read *inside* a `setState` updater — RN recycles the event once the handler returns, so it is null when React runs the updater. A FATAL TypeError on every round start that passed tsc, 521 tests, `check`, a task review, a re-review and a QA build, and put an unplayable APK in the owner's hands for 10 days. **An edit to any screen's layout, measurement or event path closes only by launching the app and reaching that screen**, and a QA build handed to the owner must have played one full round first. Again on geoguesser 2026-10-08: a UI-thread worklet writing to a Skia Canvas after its unmount SIGSEGV'd in librnskia (`setJsiProperty`). It passed 4307 tests and three reviews, because fakes cannot segfault. For any native view driven from a worklet: stop the writers and take a UI-thread ack before React unmounts; fakes THROW on a post-unmount write; device harnesses clear and check `logcat -b crash` after every step; "the app went back to the launcher" is a crash until proven otherwise
- a sampled metric quoted without **reconciling sample count against `window × expected rate`** (fired 4× in one merge-kit session: a UI-thread sampler reported 1229 of ~1800 frames, then 0, then 1 — each with a perfectly plausible p95; and an engine monitor gave 8→43 ms for identical work). A percentile over an unverified sample count is not a measurement; print the reconciliation next to the number
- a threshold compared with **no allowance for jitter or measurement resolution** (fired 2× in one session: p95 vs exactly 16.667 ms failed a vsync-locked 60 fps thread with zero dropped frames; a 0.5 ms histogram bucket midpoint read as "0.08 ms over budget"). It nearly aimed an engine decision at 40 bodies when the real crossing was ~97 — never report a shortfall smaller than the instrument's resolution
- a **config-matrix self-check skipped** before quoting a benchmark: vary the known costs. Refined on merge-kit v0.3: an inversion (cost OFF measuring slower) is only meaningful if it **replicates with non-overlapping ranges across shuffled runs** — when the true difference is ~0, any single-run ordering is a coin toss, so a one-shot inversion proves nothing about the instrument either way. A *replicated* inversion is a real anomaly: park it, disclose it, and check whether any headline number depends on the affected config. An implausible *direction* (native code measuring 5× slower than interpreted) is still a cue to audit the harness, never a finding to publish
- a **visibility-critical property that only reaches its resting value if an animation completes** (opacity/scale mounted at 0, an `onDone` fired from an animation callback): give it a deterministic settle that changes the React tree (swap the animated wrapper for a plain view via a JS timer + AppState-active fallback; JS timers do NOT fire while Android has the app paused) and review it by backgrounding *during* the animation, not before it
- a **reproduction whose expected state transition was never confirmed** (Block Destroy 2026-09-08: an emulator 'lost pieces' repro was the harness cancelling the placement tap — `adb shell sh -c "input tap; input keyevent HOME"` — so the redeal never happened; two fixes were built against a phantom). Before fixing, prove the transition occurred (a log line for the state change, not a screenshot), read every unexpected label in the evidence ("Shape selected" was the tell), and check that a pixel-scan window contains only the thing being measured
- an **"independent" oracle that shares the implementation's reading** (fired 3× on LOMN 2026-10-07: byte-swapped FourCC constants, a sign-decaying ternary accepted as "same bits", and a native modelled as "scale on true, no-op on false" by both sides when the decomp showed an overwrite on both branches — each time the full-corpus sweep agreed 100 %). Agreement proves only consistency; every constant and every modelled native needs its own citation from the binary/docs, and the review counts real call sites per branch. Again on LOMN 2026-10-08 (M2a-1): a C++ VM, an independently written oracle AND the conformance-expectation calculator all wrapped `atoi` (the CRT's `_strtol` saturates), and the calculator dropped the sign of exact-zero float results — while a 521-program corpus passed 100 % on both implementations. A corpus authored from the same table cannot catch a reading every party shares; keep an asm-first review of each implementation even after the two agree
- **a census, disassembly window or "no other site" claim bounded by the decompiler's function size** (fired 2× on LOMN: M2a-1 T7's disassembly window overran into the next function, and on 2026-10-09 the decomp gave `GcAreaLoader::LoadArea` 7,431 bytes when it runs to `ret` at 0x500fe4, so a catch census missed a third swallowing block). Decompiler function bounds are a hint, not a fact: take a function's extent from the binary (its `ret`/next-entry, or the `.exc`/unwind tables) before claiming completeness, and have the reviewer re-run the census with true extents
- **bookkeeping chained after a state change with `;`** (fired 2× on geoguesser 2026-10-04: a failed `merge --ff-only` was followed by a "merged" ledger line, a pushed handoff row, the reviewed worktree's removal and a new worktree cut from a tree WITHOUT the unit — the printed test count, 2219 not 2275, was the unread tell). Run a merge/commit/push in its own step and read its result, or `set -e` the whole sequence; check the merged suite's count against the branch's before any ledger line
- a **third fix round on one symptom** (geoguesser ART-4b 2026-10-08: fade-through, cover-disc and touch-race machinery each bred new review findings, then everything was removed for ONE move. arrows: "optimization is complete only when rejected complexity is also cleaned up"). Stop, redesign to the single path the measurements support, and DELETE the losing machinery and the losing spike (no flags left behind). More fixes on a design that the data says cannot work are the waste
- **a backtest entry scored from a candle the detector had not yet confirmed, or a candidate set chosen by a later event** (fired 2× in one hour on gold-pdf-bot 2026-10-16: an "early entry" at the second-leg candle scored 62-83% because the bot confirms a leg two candles later; a "zone entry" on the first legs of patterns that *later* became sightings scored 54% in both years, 50-52% on every swing visible at the time). Score at the event's own `bar_close`, never at the leg; build the candidate set from what was knowable then, never from patterns that completed; print the unconditioned number next to the every-candle control before any number is shown
- **timing or lifecycle evidence captured at animator scale 0 / reduced motion** (fired 2×: arrows P-02, and geoguesser SND-1 2026-10-08, where the cue was lost only with animations ON and every test used reduceMotion: true). Animator scale 0 covers one branch. Run timing bugs with motion ON and OFF, print the read-back scales in the evidence, and restore them. Note (geoguesser 2026-10-09): React Native and Reanimated read reduced motion from `transition_animation_scale == 0`, NOT the animator scale, so `animator_duration_scale 0` alone never puts an RN app in reduced motion; set the transition scale (or all three) for the reduced branch

**Verdict format:** APPROVE / REQUEST CHANGES / UNCERTAIN. "LGTM" without evidence is banned. UNCERTAIN is a first-class verdict: state exactly what you couldn't verify and what would resolve it (user eyeball, device run, targeted test). A confident wrong verdict costs more than an honest uncertain one. Full-path reviews fill this evidence block (LOW RISK = verdict + one-line reason only):

```
Verdict: …
Pre-fix failure reproduced: yes/no/not possible — evidence:
Fix verified against original scenario: command/device/runtime used:
Tests added/changed — failing path they cover:
Runtime/device verification: VERIFIED/UNVERIFIED — details:
Out-of-scope changes: none / list
Risks remaining: none / list
```
Evidence must name the exact command, runtime/device, artifact, failing scenario, or observed before/after behavior — **and explain why that command/device/artifact exercises the original failing behavior.** "Ran npm test; all green" verifies nothing unless the test is shown to cover the broken path. "Tests pass," "looks good," "verified locally," and "matches the brief" are banned as standalone evidence. Label each evidence line by register, inline at the claim: what you **executed and observed** vs what you're **inferring from reading** (didn't run) vs stable knowledge you can stand behind. A guess dressed as a finding is the reviewer's own version of fluent propagation — no "definitely" on an inference, no hedging on something you actually ran.

**Escalate to the user instead of deciding when:** the call is taste-based, the change is irreversible/outward-facing, or two plausible readings of the requirements diverge. Present your recommendation WITH the escalation — never a bare "what do you want?".

## 7. Compound the learning
Every review should leave the system slightly harder to fool next time. Don't only fix the bug — fix the review system that let it reach review.
- After each REQUEST CHANGES or meaningful UNCERTAIN, record one compact line in project memory: **pattern → detection rule → future brief/test update**. E.g. "preview passed but device failed → require smallest-device screenshot for spacing bugs → briefs must name target devices"; "config verified instead of runtime value → require live/computed value check → add runtime assertion".
- Same failure pattern twice → promote it to the §6 red-flags list in this file.
- Record every non-obvious fix, gotcha, and wrong assumption in project memory *as it happens* — even small projects deserve 1 line. Uneven memory (25 entries in one project, 0 in another) means repeated mistakes.
- Convert relative dates to absolute. Mark experiment outcomes when known.
- When starting a new project, skim the sibling project memories in `~/.claude/projects/` for transferable scars.

## 8. Vercel is the default host — cache like it costs money (it does)
Vercel bills **bandwidth, edge requests, function invocations + duration, ISR operations, image transformations and build minutes**. The one that surprises people: **a CDN cache HIT still bills an edge request.** Only a request the browser never makes is free. Value order: browser cache > CDN cache > origin. Design for the first.

- **Never ship an unhashed asset with a long `max-age`, and never ship a hashed one without it.** Content-hash every JS/CSS/font/image filename at build, then `Cache-Control: public, max-age=31536000, immutable`. If a project has no build step it has no hashes — either add a ~40-line zero-dependency stamp script or accept revalidation on every visit, and **say in the report which you chose**.
- **Use the three layers deliberately:** `Cache-Control` (browser), `CDN-Cache-Control` (any CDN), `Vercel-CDN-Cache-Control` (Vercel only, stripped before the client). HTML pattern: browser `max-age=0, must-revalidate`, Vercel CDN `max-age=31536000` — the edge answers instantly and a deploy purges it.
- **`stale-while-revalidate` for anything that changes but tolerates staleness** — one background revalidation instead of a blocking miss.
- **A route that could be a file should be a file.** Functions bill invocation + duration; a static file bills one edge request. Prefer prerender/static output; reach for a function only when the response genuinely depends on the request.
- **Cut the module waterfall**, not just the bytes: `modulepreload` for a deep ES-module graph, `preconnect` for third-party origins. Latency is free to fix and does not change the bill.
- **Third-party CDN assets (Google Fonts, etc.) cost nothing on Vercel** but cost the visitor a connection. Self-host only when the perf/privacy win is real — then hash them and cache for a year.
- **Verify by observation, not by config.** After deploy read the real headers (`curl -sI`) and `x-vercel-cache` (`HIT`/`MISS`/`STALE`) per asset class. A `vercel.json` `headers` block whose `source` never matches a real path is the most common silent failure — assert each pattern against an actual URL.
- **Know the bill's shape before optimizing.** Bandwidth, edge requests and function duration have different fixes; optimizing the wrong axis wastes a pass. State which axis a change targets and the expected requests-per-visit before/after.

## 9. Wall-clock is a budget — never block on a wait
Measured 2026-10-05 over 123k tool calls (2026-06-24..10-05; superseded by §11's 2026-10-07 split): foreground `until`/`while`+`sleep` loops and runaway commands were the biggest controllable cost — 219 Bash calls ran into the 10-min cap (37h), every one in the foreground; the same loops run with `run_in_background` cost ~0. Fresh-browser screenshot harnesses ran 30s–2.6min each.
- **Never wait in the foreground.** "Tell me when X is ready/done" → Bash `run_in_background: true` with a command that exits on the condition (`until grep -q "Ready" dev.log; do sleep 0.5; done`) — you're re-invoked on exit. A stream of events → the Monitor tool. Foreground `sleep`/poll only when bounded ≤30s.
- **Every wait matches failure too; a foreground `timeout` above the 2-min default is the signal to background the command, never a convenience** (2026-10-07: 218 of 257 foreground cap hits ran at a self-raised ~10-min timeout). The condition must also fire on crash/exit (`grep -qE "Ready|Error|FAILED"`, or check the PID is alive) — a loop that only greps for success waits out the cap on a dead process. Harness scripts exit non-zero on the first missing element. A call that hits its timeout is a harness bug, not "slow".
- **Screenshot/evidence harnesses reuse one browser and wait on state, not time.** Launch once (`chromium.launchServer()` / an already-open dev browser) and `connect`/`connectOverCDP` per run; wait with `waitForSelector`/`waitForFunction`/a log line, never fixed `waitForTimeout`/`setTimeout` sleeps (2026-10-05: 24 of 50 harnesses launched a fresh browser, 21 used fixed sleeps, 0 reused one).
- **Type-check and test incrementally while iterating.** `npx tsc --noEmit --incremental --tsBuildInfoFile node_modules/.cache/tsc.tsbuildinfo` (arrows-game 2026-10-05: 6.8s → 2.7s warm). Tests: `vitest related <files> --run` / `jest --findRelatedTests <files>` per edit; the full suite once before handoff.

## 10. Self-harness: measure the work, optimise the route with facts (owner rule 2026-10-07; revised after an adversarial review)
Every project should get faster over time, **from measured data, never at the cost of quality or the owner's time**. Stay on the current route while the data says it is best; search for a better one when a pattern, not a one-off, says the process is slow. This section governs *our process*: builds, tests, devices, waits, re-reads and hand-offs. Product runtime, bills and UI go through §6/§8 and the owner.
- **The controller appends one JSON line per brief** to `~/.claude/process-metrics/<project>.jsonl`.
  - Format: append-only, under 4 KB per line, no prompt text or secrets, with a `schema` field. Corrections are new lines, never edits.
  - What to record:
    - task id plus class (build-fix, feature, capture, review…), date and purpose;
    - wall-clock, tool calls and tokens: from the usage block or transcript; `null` if unknown, never estimated;
    - minutes by category: builds (count × min, full vs incremental), device/emulator, tests, waits/timeouts, retries, re-reads;
    - **conditions:** host loadavg at start and end, shared emulator y/n, disk free;
    - **owner cost:** round-trips, and minutes blocked on the owner;
    - **outcome:** approved first time / changes requested / reverted / reopened later, plus the route version used.
  - Follow-ups attach to the parent id, so splitting a task cannot dodge a threshold.
  - Routes rank by *approved-first-time per hour*, never by minutes alone.
- **Patterns, not one-offs.** Answer "why is this slow" from the ledger with hours, share and a reconciliation against total wall-clock; show owner-blocked time separately. Open a route experiment only when at least 5 tasks are logged and one of these holds:
  - a recurring step sums to at least 60 min, or 15% of logged wall-clock, over the last 5+ tasks;
  - a task class runs more than 2× its class median *and* more than 60 min over it, on 2+ tasks, with no reason given in its note;
  - the owner says it feels slow: answer from the ledger first, then experiment if the numbers agree.

  If the slowdown correlates with conditions (loadavg, shared emulator, disk), the route is not the suspect: fix the condition (§9, serialise across sessions) and record it. Run at most one open experiment per project. Its projected saving over the next 10 tasks must exceed its own cost at least 3×, and the experiment is itself logged as a task.
- **A new route is a hypothesis; test it.** The spec contains:
  - the expected saving, from the ledger;
  - the exact commands;
  - the **precondition** under which the route is valid (e.g. a JS-only repack only when no native file changed since the last full build);
  - a **quality guard** at least as strict as the gates the artifact already passes: the project's own perf and pixel gates with their tolerances and a null control; the same evidence class for verification (same device, same failing path); owner acceptance wherever a human could see a difference.

  Run old vs new on the same input, interleaved (ABAB), at least 3 reps per arm under comparable load, judged by §6: null spread from old-vs-old, replicated median shift, nothing below instrument resolution. A one-shot win is a coin toss. Adopt only if the saving beats the null spread *and* the guard holds. Record the result either way, with numbers, in the project's process doc and memory, so a rejected route is not retried without a new reason.
- **Who decides.**
  - An agent may adopt a route that cannot change any artifact or evidence once it is measured: caching, background waits, browser reuse, incremental tsc, smaller re-reads.
  - Any route that changes a build artifact, a capture, the evidence class, or anything the owner could see goes to the owner with the numbers (§5).
  - Loosening a gate's threshold is never part of a route change.
- **Keep it honest over time.**
  - Tag each ledger line with the route version.
  - If the approved-first-time rate or the time regresses after adoption across 3+ tasks, revert to the previous route and record why.
  - Re-run old vs new once when tool versions, host or project size change (SDK/Gradle/Xcode bump, new machine), or after 20 tasks.
  - A route proven on one project transfers to another only as a hypothesis with its number; its first use there is an experiment.
- **Project memory and caches never go stale silently.** This covers any index, knowledge graph (e.g. Graphify) or summary used instead of re-reading sources.
  - Stamp it with the git commit and a hash of the uncommitted changes it was built from, and check the stamp before every use.
  - On a mismatch, rebuild or read the sources.
  - A cache is a map, not evidence: a claim in a review still comes from the file or the run.
  - Adopting one is a route experiment: grade its accuracy on real questions against the code, run an invalidation test (edit a file, and the old answer must not come back), and measure the saving. Third-party installs need the owner's yes.
- **No novelty bias; quality is not a cost.** Keeping the current route is the right answer when the data says so. Release/store builds, visual/contrast/perf gates, §1/§6 verification and owner acceptance are never optimisation targets. Verification may be made cheaper (faster to the same evidence), never thinner. Faster with worse UI, worse perf, worse evidence or more owner round-trips is a downgrade.
- **Parallelise what is independent.** Use separate git worktrees for work that shares no files and no device. Serialise on truly shared resources: one emulator, one native build at a time, the host-load budget (§9), including other sessions on the same host. Bring branches back by cherry-pick or merge after review.

## 11. Tool use, measured (2026-10-07; adversarially reviewed)
Measured 2026-10-07 over 135k tool calls across 34 projects, 2026-06-24..10-07. Report: `~/.claude/process-metrics/reports/tool-reliability-2026-10-07.md`. Hours are agent-blocked time, not a counterfactual.
- **[invariant] No tool call blocks the agent for longer than the 2-min default; longer work runs detached** (background Bash or Monitor). 218 of 257 foreground-wait cap hits ran ≥590 s on a 120 s default, because the agent raised its own `timeout`. A foreground `timeout` above 120000 is a defect to justify in the call description.
- **[invariant] Every wait terminates on failure and on a deadline, not only on success** (grep the failure signatures or check the PID). One background `until` loop ran 13 h.
- **[fact] A cap hit is blocked time, not a dead command.** 218 of 257 foreground-wait cap hits ran to the 10-min cap, and 202 of 261 long-command timeouts were moved to the background by the harness and kept running; of 269 non-wait timeouts, only 8 were later followed by a passing identical rerun. Read the background output; never rerun the command.
- **[heuristic; re-measure with a harness-audit run on 2026-11-06 — the hook logs no outcomes] A repeated identical call states what changed since the last one** (time, input, environment); otherwise change the input. 41 identical-retry loops cost 3.7–10 h, and 21 of them eventually succeeded, so a hard stop would also cut successes.
- **[fact] zsh quoting:** quote words that start with `=`, quote globs passed as arguments, and never execute an unquoted `$VAR` of arguments (284 + 129 + 15 failures). `sh -c` is not the fix (OR 0.65 [0.41–1.04]). `find` here is a `bfs` wrapper that errors on directories whose names begin with `-` (exit 1 alone, but silent and exit 0 inside a pipeline); pass them as `./-dir`.
- **[heuristic; expires when the permission mode or sandbox changes] Prefer Read/Edit/Write for file I/O; use the shell for pipelines, aggregates and scripts.** Within-agent odds ratios are 0.23 / 0.43 / 0.09, but part of the gap is the classifier and worktree guard that Bash hits and the file tools do not. The saving is turns, not hours. The Grep and Glob tools are not exposed here (0 of 135k calls).
- **[fact] In a worktree agent the guard rejects compound, `cd` and mutating shell forms** (298 rejections). Elsewhere keep compound commands: they fail 3.8 % vs 2.0 % per call (OR 2.07, measured), but [inferred] a chained call does several units of work, so splitting is unlikely to lower total failures.
- **[fact] Browser pane:** when an error says the pane is hidden or stuck, bring it to the front or ask; a repeat fails identically (233 pane timeouts; 3 identical retry loops, all still failing — n = 3). Wrap `javascript_tool` code in an async IIFE (41 errors from top-level `await` or `return`).
- **[invariant] A blocked subagent hands back a partial report and stops. A coordinator answers or stops every live subagent before ending its turn.** 134 agents sat parked (median 15 min, p90 107 min, one for 9.7 days). Every brief carries the hand-back line.
- **[invariant] A condition is not a cause until an identical rerun passes.** The failure rate is flat at 2.5–2.9 % with 1 to 4+ concurrent projects, while fs-read latency rises 13×. Record loadavg at brief time, because transcripts do not carry it.
- **[fact] The permission layer costs turns, not fixes** (classifier unavailable 93, denied 71, about 3 h). Back off once, then continue with other work. The owner can run `/fewer-permission-prompts` per project; record the denied count before and after.
- **[heuristic, INFERRED] Run your own analysis script on one input before running it on the full set** (86 Python + 84 Node tracebacks, 1.8 h).
- **Experiment (approved 2026-10-07; starts when the owner registers the hook, since agents may not edit Claude settings):** a PreToolUse hook (`agent-playbooks/tools/hooks/fg-wait-guard.sh`) denies only Bash calls with `run_in_background` false, `timeout` ≥ 300000, and a first statement that is an `until`/`while` loop containing `sleep`. Running 2026-10-07..11-06, it is judged against the previous 30 days on these measures, per project:
  - foreground Bash calls ≥300 s per 1,000 calls (success = down ≥50 %);
  - foreground call-hours ≥120 s;
  - a workaround detector (Python/Node sleeps, `read -t`, `timeout N tail -f`) that must stay flat;
  - zsh `=` failures as the null.

  Kill switch: `CLAUDE_HOOK_FG_WAIT_OFF=1`. Remove the hook if the workaround detector rises. The hook enforces only the worst third of the 2-min invariant on purpose: bounded 2–5 min waits and `for`/`cd &&` forms stay legal and are covered by the invariant, not the hook. The baseline window and the workaround detector are frozen in `~/.claude/process-metrics/reports/fg-wait-baseline-2026-10-07.*` before judging.


## 12. Monitoring is part of the build (owner rule 2026-10-08, after gold-pdf-bot incident 1)
A critical module is anything others depend on to keep working: a webhook, a database, a scheduler, a message sender, a data feed, a credential. **Before building or changing one, the plan answers five questions, and if an answer is missing, ask the owner instead of guessing:**
1. **Alive:** which live signal shows it works (existing traffic first, e.g. a recurring send or a check-in; a new probe only when no traffic proves it)?
2. **Why it failed:** the reason in our own words (never secrets or driver text), kept somewhere that survives that failure (a log line plus the next message that goes out; not only the store that just failed).
3. **Where the owner sees it, and how fast:** dashboard line, message, or email; the worst-case delay is written down.
4. **Cost:** requests and compute per month on the free tier, computed (e.g. a 5-min database pinger on Neon free = ~180 CU-h, over the 100 limit).
5. **Drill:** the test that simulates the failure (wrong password, wrong address format, wrong host, missing variable, sender refused) and shows the monitor turn red with the right reason. The module is not done until the drill passes.
Also: a credential or env change is a deploy. Test the exact value first, redeploy at once, and confirm with the next real arrival; record each incident (what, when, how noticed, cause, fix, the new check) in the project's incident log.

## 13. Sound needs ears: listen with earshot (owner rule 2026-10-16)
You cannot hear. Any time you make, pick, trim, mix or review audio (a /brag or brag-slim video, a launch film, Hyperframes/Remotion/three.js soundtracks, game or UI SFX, a code-synthesized sound), listen with **earshot** before you call it done or say how it sounds. Load the `earshot` skill (how to listen, how to read the numbers); for a full soundtrack from real licensed recordings, `real-sound`.
- **Install:** `~/.claude/tools/earshot` (pinned clone of github.com/Leonxlnx/earshot), Python `~/.claude/tools/earshot/.venv/bin/python` (`-m earshot …`). The MCP server `earshot` is registered at user scope (models stay warm); prefer it, or one Python script with `from earshot import api`, over many CLI calls (each CLI call reloads the models, ~20-40 s). Wherever a skill says `/path/to/earshot` or `{{PY}}`, use these paths.
- **Minimum loop for a rendered video:** `timeline film.mp4 --cues cues.json` (sync, events, loudness) → `sheet film.mp4 -o sheet.png` and OPEN the PNG → `critique film.mp4` (scorecard vs pro launch films) → fix the FIX FIRST rows → re-run on the new render. For a single SFX: `describe` / `match --alts` / `realness`. For a made sound: `earshot forge`.
- **Report with the numbers** ("strong match z +3.9; -14.2 LUFS; offset +12 ms"). A sound is "VERIFIED (earshot …)" only with the command and reading; without a run it is UNVERIFIED (§1).
- **Limits (Goodhart):** earshot measures what a sound is and how it sits, not taste. Forge-made sounds can satisfy its models without being better: judge them by the model-free tone/tail numbers and spectrograms, and the owner decides on taste (§2). `earshot llm` uploads audio to Google: only with the owner's explicit yes.
- Run long `forge` / `critique` jobs in the background (§9).
