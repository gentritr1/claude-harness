# The product HUD (Gate D3, 2026-08-10) — branch `discussion-d3`, unpushed

Sidebar retired; tray (`src/play/tray.js`) + private card (`src/play/card.js`) +
the one grammar (`src/play/seat.js`). 15th gate: `npm run test:hud`.

## Detection rules earned here

- **"Unchanged" needs a pre-change fingerprint, not a diff.** The objective
  line's behaviour is hashed against 466 lines produced by running
  `git show 02e44a6:src/play/objective.js` — a fingerprint generated after the
  change proves nothing. Pattern → any "X is unchanged" acceptance criterion
  must be pinned to a value computed from the pre-change artifact, and the
  command that produced it written next to it.
- **Copy the project's own measurement rule, never invent a plausible one.** My
  first warm-pixel classifier (RGB thresholds) read 5.81% where `lighting.js`'s
  own rule (hue 15–70°, s > 0.16, l > 0.18) reads 7.29% on the identical frame.
  Only the second is comparable to the declared 10% budget. Pattern → when
  measuring against an existing budget, lift the classifier verbatim from where
  the budget is declared.
- **A leak sweep must separate CHANNEL from WORDS.** "Role colour on exactly one
  element" cannot be a hex sweep: the palette law forbids new colours, so role
  blue *is* Reform blue. Enforce the semantic class (`r-*`), and treat role
  *words* separately — banned on permanent surfaces, allowed as rules copy on a
  panel but never within 40 chars of a citizen's name.
- **Coverage gates must run after the constructed fixtures.** Three tray rows
  (Block, Foresight, and the human-speaker cases) are rarer than a 50-match
  sweep; running the REQUIRED check before them fails honestly and uselessly.
- **The sweep found two real spec bugs** the code review would not have: a role
  word inside the Peek/Purge blurbs on a permanent surface, and three
  `empty:*` ids unreachable while the seat is alive (a living seat always owes a
  ballot; both acknowledge gates fire for every seat) — same shape as
  `objective.js`'s three starred ids.

## Decisions to carry forward

- Tray rows are **offered** (E at the object) then **armed** (keys live, body
  frozen, Esc steps back). Always-live keys would let a strafe (`A`) cast a
  ballot. In council view arming becomes the whole interaction and the
  wireframe's always-live keys are literal.
- `acknowledge` (morning / chaos / tally) stays a centred card: ceremonies, not
  decisions, and Gate 1.5 tuned where each opens.
- Card is a FIXED 232×96 with the 4th line's row always in the layout — the
  acceptance list beats the wireframe's taller box. Measured
  `{232,96,12,12}` in every browser state.
- `screenBias = 0` on every page now; the correction existed only for the 330 px
  sidebar. `walk.html` behaviour unchanged (always 0 there).
- `#objective` CSS is frozen byte for byte (top 52 / left 346 / right 16) —
  346 still clears the card, which ends at 244.
- Ledger routing is proved by ABSENCE: nothing on screen, everything in
  `__play.ledger()`.
- Panel bodies for the four tray decisions are dead on the page but kept —
  `test/objective.test.js` still renders the Emergency Vote panel through
  `panels.open`.

## Numbers (measured 2026-08-10, 1280×720)

- night `trial` with HUD **7.29%** warm vs 6.61% without (budget 10%); second
  trial frame 3.40 / 2.53. Dusk (budget 45%) 14.30 / 14.42 — HUD ≈ 0.
- seed 1000 / 7p fingerprint unchanged: 61 steps, 38 decisions, LOYALIST.
- `test:hud` 133,972 checks over 50 matches, 13,628 tray states.
