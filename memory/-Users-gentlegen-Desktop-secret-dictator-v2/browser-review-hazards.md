# Browser-review hazards on this repo

Scars from the Gate 1 pass (2026-08-09), all found by driving the page, none by reading code.

## Vite HMR re-deals the match under a scripted review
Editing any file under `src/` while a console review is in flight reloads `play.html`,
which re-runs `restart(1000, 7, 0)`. A review that believes it is still driving seed 19
silently starts reading a different deal — it looked like "the human's role changed
mid-match" and cost ~30 min. The tell was the fingerprint: 61 steps + loyalist win is
seed 1000's record in docs/step-04.md.

**Detection rule:** a scripted browser probe must re-assert its own premise
(`__play.state()` → players.length, you.id, you.role, plus the seed box) after any edit,
not just read the thing being measured. Briefs that ask for a browser pass must say so.

## `focus()` inside a `focusin` handler is ignored
The browser is still mid-transfer, so a focus-trap backstop written the obvious way runs,
does nothing, and reports no error. Defer by `setTimeout(..., 0)`.
Related: `inert` on the elements outside the dialog is the real fix; the focus fight is
only the backstop.

## State that changes on a frame is invisible to every automated check
Gate 1.5's deliberation beat ends on a clock; nothing calls `refresh()` when it does, so the
objective line was re-derived only in the rAF loop. A human sees it flip in 16 ms; a scripted
probe (and a backgrounded tab) sees the podium light up with the stale sentence still on it.
**Fix: re-derive from the `setTimeout` loop too — it runs when rAF does not.** Same family as
`look()`. Rule: if a transition is only observable on a frame, it is not observable.

## A parallel agent's broad `git add` can swallow your in-progress files
2026-08-09: a Gate 2 art agent committed `art(env-dais-a): …` including four of my
mid-edit Gate 1.5 files, leaving HEAD failing `npm run verify` (source moved, matching test
not yet written). Check `git log --oneline -3` and `git status` before committing, and if
another agent may be running, commit early rather than holding a large working tree.
Do not rewrite another agent's commit — report the collision instead.

## rAF is stalled in this browser pane until something forces a paint
`__walk.basis()` reads values only written inside the render loop, so it returns all
zeros right after a navigate. Take a screenshot (or otherwise force a frame) before
reading anything the render loop computes. Same family as the `look()` note in step-04.

## Contrast over a 3D scene must be computed against the worst case
A HUD colour is not "AA" against `--bg`; it is only AA against `--bg` blended with
whatever the scene is doing behind it. Compute against a blown-out white backdrop at the
declared alpha, or raise the alpha until it does not matter.
