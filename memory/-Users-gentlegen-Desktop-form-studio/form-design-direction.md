---
name: form-design-direction
description: "FORM portfolio site: identity idea, what shipped on 2026-10-02, the pending 3D brief, and what is still open with the owner"
metadata:
  node_type: memory
  type: project
  originSessionId: 7144205e-fbda-47a3-975d-e55755cb416c
  modified: 2026-10-04T21:28:42.336Z
---

FORM (form-studio, remote `gentritr1/form`) is a fictional sculpture-exhibition portfolio piece: dependency-free WebGL, `dist/` + standalone `FORM.html`. The first two commits were built without any browser visual review.

Shipped 2026-10-02 as commit `3781ea5` on branch `feat/identity-and-cast-a-word` (not pushed, not merged to main), two Opus delegations reviewed by me:
- Identity idea: "the room takes the temperature of the material". `html[data-material]` drives page tint + accent (copper / chrome / porcelain × light / dark), tokens registered with `@property` and crossfaded 420ms.
- Segmented radio groups instead of dropdowns; "placard" buttons (label + square action cell, SVG icons); wall-label equations in the gallery.
- "Cast a word": typed word → deterministic sculpture (FNV-1a → mulberry32), shader uniforms `uLobes/uWave/uRipple`, ripple gate keeps lobes integer, share link `#study=v1.…&name=`.

Next step handed to the owner: `briefs/3d-depth-pass.md` (uncommitted), a prompt for a 3D-specialist model: measure first, single GL context, contact shadow, room-aware reflections, construction morphs + touchable equation terms, cast as a material event.

3D depth pass (reviewed 2026-10-02): done by a Codex/ChatGPT model in a SEPARATE clone, `~/.codex/.chatgpt-projects/g-p-6abea21425488191a141b3ed5d4ce626/form-depth-pass`, branch `feat/3d-depth-pass`, tip `0ffb4a9` (4 commits on top of `3781ea5`). It is not in the Desktop repo; fetch it from that path to merge. Everything is behind `?layers=direct,shadow,room,construction,cast,adaptive`; no flag = baseline. My review: layers-off output pixel-identical to `3781ea5` (8 hashes), context loss/restore and poster work with layers on. Not ready to be default: hero shadow hard-clipped at the canvas edge; construction makes the studio object mostly absent while typing (125 of 164 frames in my slow-typist model); scrubber is a native 16px range; equation-term buttons are 47×21px; 5.5 MB of raw results committed. Its own perf data shows both baseline and depth pass dropping frames (baseline delivered 55–88% of expected in twist/material segments), measured under browser automation.

Merged and fixed 2026-10-02: branch `feat/identity-and-cast-a-word` now at `20a48ad` (fast-forward of the depth branch + my fixes; not pushed, main untouched). Fixed: shadow edge fade (12%), studio keeps the morph (construction only on hero + construction study), scrubber uses studio slider styling, 44px term targets, room colours from JS token tables (no computed-style reads in draw; `tests/tokens.cjs` guards the tables). Depth layers are still opt-in behind `?layers=`.

Depth pass is the DEFAULT since `5664451` (2026-10-02, owner's decision): no `layers` param = all six layers; `?layers=none` = baseline (8 pixel hashes still equal `3781ea5`); failed depth start reloads once with `layers=none`. Branch `feat/identity-and-cast-a-word` is PUSHED to `origin` (github.com/gentritr1/form), 10 commits ahead of `main`; Merged to `main` by fast-forward and pushed on 2026-10-02: `origin/main` = `5664451`; the local checkout is now on `main`. The feature branch still exists locally and on origin.

Deploy setup (2026-10-02): commit `fd0d71b`, fast-forwarded into `main` and pushed (`origin/main` = `fd0d71b`). Cleanup 2026-10-04: only `main` remains (local + origin); feature branches deleted after merge check. Stale files moved to `~/.Trash/form-cleanup-2026-10-04/` (Desktop diagnostic downloads, old `FORM-portfolio-project.zip`, empty `.sites-runtime/`). Kept on purpose: `.openai/hosting.json` (an OpenAI-sites hosting config pointing at `dist/`, may be live), `tests/results/form-perf-*.json` (raw data behind MEASUREMENTS.md), `public/` (build output), The merged Codex clone was moved to the Trash on 2026-10-04 at the owner's request (verified clean, no stash, all branches in `main` first). `npm run build` → `stamp.mjs` writes `public/` (gitignored) with `static/<name>.<10-hex hash>.<ext>`; `vercel.json` sets buildCommand/outputDirectory, `/static/(.*)` immutable 1y, `/` + `/index.html` max-age=0 + Vercel-CDN-Cache-Control 1y. `tests/site.mjs` asserts each header rule against real paths. Repo is NOT connected to a Vercel project (no `.vercel`, no CLI, no GitHub deployments), so live `curl -sI` header verification is still OPEN; commands are in README "Deploy". The owner pushes explicitly each time; don't push unasked.

Frame-rate status: MEASURED 2026-10-02 by the owner in an ordinary Chrome 152 window (M1 Pro, 1800×875 DPR 2, 120 Hz), commit `63e289a`, `tests/results/MEASUREMENTS.md`: baseline and all six depth layers both deliver 238–241 of ~241 frames per 2 s segment, 0 intervals >50 ms, one 25 ms interval (first studio draw) each; depth layers cost ~+1.3 ms GPU, ≤1.5 ms CPU p95. The 3D model's stalls were automation noise. Quick re-run: `/tests/perf.html?layers=none&batch=1&quick=1` (~80 s; the tab must stay visible — switching back to Claude hides it and aborts the run). Remaining gate for making the depth pass default: owner's visual acceptance + a second device. Earlier note, kept for context: it was unmeasured in an ordinary visible browser. The owner DECLINED computer-use access to Chrome (do not ask again; ask them to open `http://127.0.0.1:4173/tests/perf.html?layers=none&batch=1` themselves, ~5 min, then `npm run report`). The 3D model's numbers were taken under browser automation; rotation-only baseline shows hitches with 0.1 ms CPU draws, so that data is a noise floor, not app jank. My CPU microbenchmarks (valid in a hidden tab): shadow support probe 0.3–0.5 ms/call, full style recalc per crossfade step ~1.3 ms. Two hypotheses I formed from their data (style recalc 12–17 ms; shadow probe 7–9 ms) were both disproved by measuring — measure before redesigning.

**Why:** the sculptures were strong but the shell was anonymous gray Helvetica with an accent colour that was never visible.

**How to apply:** keep new UI inside this system; contrast values in the token table were computed with a script, recompute if any token changes. Open with the owner: eyeball acceptance of motion/feel and 60 fps (never measured, see [[browser-pane-hidden-rendering]]); typeface (Helvetica Neue stack falls back to Arial/Roboto off macOS; self-hosting a font needs their OK to download); deployment caching (no hashing, no vercel.json yet). "Impeccable" and "Taste" skills are not installed in `~/.claude/skills`.

Review lessons from this session (pattern → detection → brief update):
- Responsive check sampled only 375 and 1440; the control row broke at 900–1240 and the owner found it → sweep 320/375/620/768/925/1100/1240/1440 and test label overflow (`scrollWidth > clientWidth`) → briefs must list the widths.
- A shader range was prototyped at low screenshot scale and missed a tear where the surface crosses the `atan` axis → view worst-case parameter corners at full size and from several angles before pinning ranges in a brief.
- My own brief contradicted itself (44px track with 44px labels inside 3px padding) → compute box sizes before pinning them.
