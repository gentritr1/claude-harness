---
name: living-globe-resume-point
description: RESUMED 2026-10-08 20:48 (was PAUSED ~18:45) by the owner ("stop, resume later") - exact state of ART-4c/4d and what to do on "resume"
metadata:
  type: project
---
The owner paused all work on 2026-10-08 and said they will type "resume". Nothing was committed after the briefs. Worktrees live under the session scratchpad: /private/tmp/claude-501/-Users-gentlegen-Desktop-Projects-geoguesser-app/8af59ba5-d560-4c15-8328-20f7ae41a70b/scratchpad/. If /private/tmp was wiped, the uncommitted work below is LOST: re-dispatch from the committed briefs.

**ART-4c** (branch art-4c, worktree art-4c, brief commit e8aa630 on top of art-4b 4c79060): the sun catches up.
- Implementation done, but UNCOMMITTED. Review verdict: REQUEST CHANGES.
- Fix round 1 was sent and STOPPED MID-WAY. The working tree holds partial F1/F2/F3 edits; its last words were "staged pure plumbing test (F2) and the brief's device-bound comment (F3)".
- The fixes:
  - F1: anchor the QA replay departure to the band instant (atMs - away), plus a 150-second-old-band test.
  - F2: the controller ruled `why=stale`: no sweep when the entrance comes more than 10 s after the return.
  - F3: a worst-case sunErr layer test, plus the device bound sunErr <= 0.17 for 8 h at 60 Hz.
- I already re-pinned the d3-3a qa-panel hashes to 1535376...: legitimate, a new flag row, with all 8 home rows unchanged.

**ART-4d** (branch art-4d, worktree art-4d, brief commit fba8bbf): today fills from the pole.
- Implementation done and UNCOMMITTED. The implementer reports gates 4395/4395 twice and its qa-panel pin at 116e1cc2.
- Its independent review was STOPPED before reporting: re-dispatch it.

**Flaky test:** "the warm cap" in tests/art-4b-home-spin.test.ts failed 3/8 on art-4c, at load 27-71.
- Passes so far: art-4s (unchanged art-4b) 2/2, and the art-4d full suite 2/2.
- ART-4c's diff does not touch the warm path. The flake is not proven to be pre-existing: finish the art-4s runs before committing 4c.

**On "resume":**
1. Check the scratchpad worktrees still exist, and that the load is OK.
2. Resume the ART-4c fixer: SendMessage to it, or re-dispatch with the F1-F3 text, letting it inspect its partial edits first.
3. Re-dispatch the ART-4d review.
4. Finish the flake comparison: never two test.cjs runs in one worktree.
5. Then gate, commit and stack (4c and 4d onto art-4b), build the QA APK, run the emulator acceptance, and send recordings to the owner.
6. Next units: ART-4e (new-day slide when the app stayed open) and ART-4f (drag/flick with react-native-gesture-handler ~2.28.0, owner approved).

Related: [[globe-after-entrance-direction]].

**Update 2026-10-08 evening**
- **ART-4d COMMITTED, 707a025** on branch art-4d: review fixed, re-review APPROVE, controller gate 4398/4398 x2.
- **ART-4c REDESIGNED:** the owner chose "Night sweeps on return". The v2.1 brief is e624cce, with Fable's GO WITH CHANGES folded in.
  - The land stays still; the night sweeps from the band last seen to now.
  - Coast in the shader (coastAlpha uniform, declared last).
  - Cross-fade in over 120 ms.
  - Duration clamp(8.33 ms/deg, 500, 1400), inOut cubic.
  - Deadline 1000 ms, provisional.
  - No markSpun: the ART-4b spin stays owed.
- The v2 implementer was dispatched on top of the uncommitted v1 code, deleting the entrance-sweep path.
- Open owner questions to raise at the end: the 16 h sweep cap (it peaks ~8.6 deg per frame), and the measured return deadline.
- **Flake verdict (interleaved, 2026-10-08):** the art-4b "warm cap" test failed 4/14 on art-4c v1 vs 0/16 on art-4b, at the same load. I called that a regression: WRONG.
  - The implementer A/B'd 100 runs per arm on a harness: base 4/100, v1 1/100.
  - Mechanism: the warm-budget retry warmer mounts in the same act(), and the test's regex matches the new warmer. A test-precision bug that exists at 4c79060.
  - Ruling: fix the art-4b test (identify the retired instance) as a separate commit, with mutation proof and 20/20.

**Owner request, 2026-10-09 ~00:30 (do it at the end, once 4c/4d/4e/4f are done):**
- "do the v2 of all this next level, so we can test it all". That means one QA build containing all the next-level work, plus a test script.
- "give an artifact with /eli5 and asdt 100 and visual learning with all that we did on this branch and how we took it to next level". An interactive visual explainer artifact (ELI5 tone) of the whole feat/next-level journey.
- No /eli5 skill is installed (the `learn` skill exists). "asd 100" is ASD-STE100 Simplified Technical English, confirmed by the owner ("simple english but in another way"). Write the artifact text to STE rules: max 20 words per instruction sentence, 25 per descriptive; one meaning per word; active voice; one instruction per sentence; approved simple vocabulary.

**State 2026-10-09 ~01:40**
- **art-4c committed:** 62c2c8a (feature), 45aac88 (art-4b test fix) and c3bb1df (stable tree position).
- **art-4cd = art-4c + art-4d merged, 29da7cc:** gate 4474 x2. QA APK at docs/plan/evidence/art-4cd/build/art4cd-29da7cc.apk; bundle strings verified.
- **Emulator verification agent** running; evidence goes to docs/plan/evidence/art-4cd/device/RESULT.md.
- **ART-4e v1.1 brief** at ac27e76 on art-4e (from 29da7cc), with Fable's GO WITH CHANGES folded in. Implementer dispatched.
- **Still to do:**
  - ART-4f (drag, react-native-gesture-handler ~2.28.0, owner-approved);
  - the final "v2" QA build of all next-level work;
  - the STE100 ELI5 artifact.
  - Cherry-pick 45aac88 onto art-4b (art-4s worktree) later.

**2026-10-09 ~03:00. The device run of art-4cd (29da7cc):**
- **ART-4c, simulated returns:** ready in 46-84 ms, frames n == expected, missed_vsyncs 0.
- **ART-4c, REAL returns:** 0/8 met 1000 ms. The late time was 1.2-3.7 s, mostly missing=ticks: the UI thread is starved after resume. A forced post-resume sweep janked (41/81 frames drawn).
- **Owner decision 2026-10-09: "Once smooth, up to ~4 s".** Hold the old night, start the sweep when a run of on-time frames shows, cap ~4 s, else an instant update. This is the next unit, ART-4g, on top of art-4e.
- **Parity:** 2.2% of disc pixels > 8/255 (coastlines); heatmap at art-4cd/device/a4/.
- **ART-4d is BLOCKED on device:** the QA build has no daily manifest (`setDailyManifest` is never called outside tests). It needs a QA-only fixture manifest.
- **ART-4e:** scoped re-review APPROVE. The controller gate is running.
- **ART-4e committed:** 6a60809 (gate 4525 x2).
- **ART-4g brief** at 0cbed56 on art-4g (from 6a60809). Implementer dispatched with two parts:
  - (A) the smooth-start gate: 6 on-time frames, cap 4 s;
  - (B) the QA in-memory test daily: install + mark-played, no persistence.
- **Next:**
  1. ART-4g review, gate and commit;
  2. ART-4f drag: npx expo install react-native-gesture-handler ~2.28.0, GestureHandlerRootView at the App root, coast already in the shader;
  3. the final v2 QA APK plus a device pass;
  4. the STE100 artifact.
- **ART-4g committed:** 0195573 (smooth start: rate evidence, a one-vsync on-time window, cap 4 s) and 99b86b3 (QA in-memory test daily). Gate 4576 x2. art-4g is now the top of the stack: art-4b -> 4c -> 4cd(+4d) -> 4e -> 4g.
- **QA APK build** for art-4g is running, to docs/plan/evidence/art-4g/build/. Then a full device pass for A (4c real returns with the smooth gate), B (4d fill via the test daily) and E (4e slide via Daily clock +1 d, plus the emulator-clock 23:59 withSweep=1).
- **Watch period= on a 60 Hz AVD** (the stray-fast-frame lock risk).
- **2026-10-09 ~14:30.** Device pass 2 (art4g-99b86b3.apk) has been running in the emulator agent since ~14:00.
- **ART-4f:** gesture-handler is committed (fb87a20; audit unchanged at 40, none in the new packages). The v1.1 brief is at 783e39a, with Fable's GO WITH CHANGES folded in:
  - the worklet directive is proven statically;
  - mount at onStart;
  - a drag warm reason;
  - the nearest-rest physics table + clamp;
  - no reduced-motion drag in v1.
- **ART-4f implementer dispatched.**

**Owner 2026-10-09: PLAYBOOK PROMOTION WAITS for the END.** Only after the final APK is confirmed stable (no crashes; all effects verified on device):
- promote the ART-4c..4g/4f lessons into agent-playbooks as v0.6.0, delegated with the 11-candidate list, in the order rn-render-perf, testing, android, expo, ui-motion, agent-process;
- include a NEW process rule: before reusing a playbook route, run a freshness check of library versions and newer approaches, recorded in the brief.

I started a promotion agent too early and stopped it at once; the playbook repo is untouched at e213479.

**Final order at the end:**
1. All effects pass on device.
2. Build the v2 QA APK of everything.
3. Run the stability pass (no crashes).
4. Promote to the playbook.
5. Make the STE100 ELI5 artifact.

**Device pass 2 (art4g-99b86b3), 2026-10-09 ~15:30. Docs: art-4g/device/RESULT.md.**
- **Return sweeps (fail):** all 9 started REAL-return sweeps janked: hwui 7-23 of ~60 frames, GPU p50 38-150 ms (warm: 14). They had passed the smooth gate (6 frames at 16.7 ms). So UI-tick smoothness does NOT predict the post-resume GPU cost.
- **What passed:**
  - the fill wipe and new-day slide lines;
  - E2, the midnight rollover + return, at 61/61;
  - reduced motion;
  - no app crashes.
  - Fill and slide frames dropped some at host load 10-19.
- **Silent pass:** the frames line's `expected` uses the median delta.
- **Owner decision 2026-10-09: "Measure on my phone first".**
  1. Fix the frames counter (expected from the period, plus dropped=).
  2. Make the QA readout show the return lines.
  3. Build a QA APK with 4f included.
  4. Write the owner a phone test script.
  - If the phone janks too: fall back to the cheap opacity dissolve (no Skia) on return.
- **Third round on this symptom:** NO more gate tweaks without phone data.
- **ART-4f committed:** f8cec3e (the art-4g flake fix) and 31b4383 (drag/flick + the frames-line dropped= fix + QA ring 20). Gate 4647 x2.
- **Stack:** art-4b -> 4c -> 4cd(+4d) -> 4e -> 4g -> 4f, so art-4f has EVERYTHING.
- **Full-stack QA APK** building to docs/plan/evidence/art-4f/build/.
- **Next:**
  1. An emulator smoke/crash pass + the drag device items.
  2. Owner phone test: return-sweep data via QA readout screenshots, plus feel.
  3. Owner decision on the return sweep: keep it, or the fallback dissolve.
  4. Then the v2 stability pass, then playbook promotion, then the STE100 artifact.

**2026-10-09 ~17:00. Device pass 3 on art4f-31b4383 (art-4f/device/RESULT.md):**
- No app crash in any step. OFF and ON smokes pass, and the map pan/pinch works under GestureHandlerRootView.
- **Drag:** touchToReady p80 37 ms (so NO resident canvas needed), idle 0 frames, native +7 MB, vertical scroll OK, flick -> one turn.
- **One app ANR + a SystemUI ANR** at guest load 36, 1 min after a reboot, before any test step: read as emulator starvation (UNPROVEN).

**Owner handed:**
- the APK (desktop-only: 43.7 MB is over the 30 MB phone upload limit);
- PHONE-TEST.md;
- 4 recordings.

**WAITING ON the owner's phone screenshots and keep/tweak/drop per effect.** Then:
- decide the return sweep: keep, or fall back to a dissolve;
- run the v2 stability pass;
- promote to the playbook;
- make the STE100 artifact.

**Owner docs (2026-10-09). Two artifacts in STE100 / ELI5:**
- **Test Guide**, https://claude.ai/artifact/MEL9i3DMSS9FrsMbUpXE9S: 14 sessions, flags, tick steps, "good result". The source is scratchpad/next-level-guide/index.html.
- **Before and After**, https://claude.ai/artifact/AxEhvPhQozvRJ1ETgNd4AH: 57 rows covering features, always-on changes, fixes, caught bugs, QA tools and not-done items. The source is scratchpad/before-after/index.html.
- **When anything changes** (phone results, merges), update both: same file path, same URL.
- **Repo copy:** docs/handoff/NEXT-LEVEL-TEST-GUIDE.md was offered, not yet asked for.

**2026-10-10. ART-5m (map look A, "Globe match").** The owner picked A from browser renders of the guess map (now/A/B/C, sent as files).
- **Look:** sea #0B1326, land #24345C, ice #2E416E, coastline #5B6F9E, borders rgba(127,144,175,.45), labels #C9D3E6, English-only names, a dark zoom control, the credit collapsed. art_v2 only; V1 bytes unchanged.
- **Plumbing:** brief 4a7ee94 on branch art-5m (from art-4f 31b4383). Implementer dispatched.
- **Then:** review, gate, commit, and a new QA APK. The APK on the Desktop is geoguesser-qa-art4f-31b4383.apk.
- **Tester how-to** was answered: QA APK sideload; 7 quick taps on the "Geo Guesser" name within 3 s; a Play-installed copy may need uninstalling (signature).

**2026-10-10 03:58: ART-5m done.**
- Commit e0ce9d8 on branch art-5m (on top of art-4f 31b4383). Full Opus review REQUEST CHANGES, fixed over 3 rounds. Sonnet scoped review APPROVE.
- Gates: tsc 0, tests 4664 x2, check 0.
- QA APK `~/Desktop/geoguesser-qa-art5m-e0ce9d8.apk`, sha256 84bef986...0043. Evidence: `docs/plan/evidence/art-5m/{build,device}`.
- Emulator pass: all 7 steps PASS, 0 FATAL / 0 ANR.
- Open:
  - orange focus ring on the credit "i" after a tap (WebView default; fix in the next batch);
  - owner taste calls: rivers in the sea colour, maritime border lines;
  - owner phone test of this APK;
  - icon concept pick.

**2026-10-10 13:51: ART-5m fix 61edf2a (Spain + focus ring).**
- Sonnet review APPROVE. Gates: 4665 x2.
- QA APK `~/Desktop/geoguesser-qa-art5m-61edf2a.apk`, sha256 2363cb1c...ce8e3. It supersedes e0ce9d8.
- Emulator pass r2 PASS: SPAIN drawn, no ring, HUNGARY and SWITZERLAND drawn at about z3.25.
- Open:
  - owner taste: rivers, maritime lines, the see-through zoom box;
  - owner phone test;
  - icon pick.
