# Pacing decisions for the square (play.html)

## Where each acknowledge beat opens — REVISED 2026-08-09 (Gate 1.5)

The routing rule lives in exactly ONE place: `objectFor(kind, gate)` in
`src/play/objective.js`. `src/play/main.js` builds the podium and bell interactables
out of it, and `test/objective.test.js` asserts against it. Never write it out a second time.

| beat | opens at | status |
| --- | --- | --- |
| morning report | bell | unchanged — one ritual trip per day |
| ballot tally | **podium** | MOVED in Gate 1.5 (was bell) |
| Chaos | bell | unchanged — news worth the walk |
| every real decision | podium | unchanged |

Owner played Gate 1: "intuitive overall what to do" (the objective line worked), but
"it feels like a chore going to the bell" and "a bit repetitive but okay".

Measured effect of the move (200 matches/table size): bell visits −50% (18.8→9.4 at 5p,
28.4→14.6 at 10p) but bell↔podium **crossings** only −10…−20%, because the morning bell
still bookends every day. Report both numbers; the second is the honest one.
Next lever if it still drags: auto-advance the morning report. The `acknowledge` beats
consume nothing from the seeded stream, so they are always free to move.

## Bot deliberation — added Gate 1.5

`src/play/pace.js`. Per-phase bands (legislative longest, bookkeeping shortest) plus a
0.9–1.7 s "beat" after a human submission that immediately owes another decision — those
two transitions (nominate→vote, vote→tally) were literally instantaneous because both are
one `Driver.step` triggered by the human's own submit, with no timer involved.

Cost: ~66 s added per 7-player match at 1× (88 s of machine time vs 22 s). 4× reproduces
the old flat 900 ms. **Nobody has felt these numbers yet** — the bands are one object
literal; treat them as a first guess pending a hands-on verdict.

## The bands were never actually elapsing — FIXED 2026-08-09 (Gate 3)

The deliberation above did not happen after a *human* submission, and had not
since Gate 1.5 shipped. While the rules wait on you the match loop polls every
`IDLE_INTERVAL` (200 ms); the tick that notices your answer takes the bot's
action **immediately** and only afterwards computes a `pace.delayFor` delay. So
every human submit was followed by a bot action within 200 ms at every speed.

Found by the Gate 3 audio timestamps — the bell cue and the gavel cue were
**157 ms apart** against a declared 1500–3000 ms nomination band. The visible
symptom was that the `dusk` lighting state was unreachable: the square went from
morning straight to a ballot without ever gathering.

Fix: `panels.onSubmit` calls `stopLoop(); startLoop();` after `refresh()`. No
band changed. **Consequence for the numbers above:** every per-match total in
`docs/step-05.md` §7b was measured without this and understates real elapsed
time by up to 200 ms per human submission.

## The beat has to hold the ambience too — Gate 3

Casting a ballot resolves the whole election in one `Driver.step`, so the light,
the tally sting and every seat's AYE/NAY badge fired in the same frame as your
keypress — you knew the result before walking to the podium to open the ballots.
Not a leak (`lastVote` is genuinely public then); it just spends the beat and
spoils the panel. During a beat, YOUR OWN cue fires at once and every public
announcement queues until the beat ends. Seal→tally went 0 ms → 1730 ms apart.

**General rule: anything that reacts to the view must respect `holding`, not
just the objective line.**

## The hard constraint, and how it is proven

Timing must never consume `G.rng()` or alter an outcome. `pace.js` imports nothing, owns a
salted mulberry32 (NOT `Math.random`, so the `grep -rn "rng(\|Math.random" src/play/` gate
stays meaningful), and returns only `setTimeout` durations.

`test/pace.test.js` plays each seeded match twice — plainly, and with the clock hammered at
every seam at 0.5/1/2/4× — and requires byte-identical logs. **Crucially it also runs a
positive control**: the same interleave with one `G.rng()` per seam MUST diverge (40/40).
Without that control the green result would prove nothing about the probe's sensitivity.
