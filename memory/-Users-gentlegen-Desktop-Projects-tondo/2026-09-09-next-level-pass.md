---
name: 2026-09-09-next-level-pass
description: The next-level pass — the pie match layer, sound, events.js, delivery, and the bugs found along the way (2026-09-09, against fee48df)
metadata:
  type: project
---

Research + plan + build pass. Plan: `docs/NEXT-LEVEL.md`. Fresh captures:
`docs/qa-2026-09/`. Tests went 44 → 75.

**Retention position taken (JUDGEMENT, not measured):** Tondo cannot win solo
daily retention — no accounts, no push, no DB — and should not try, because
every mechanism for it is casino-shaped AND non-functional here (a localStorage
streak evaporates on a cleared cache, and with no push the game can never tell
you it is at risk). It can win "again, right now" and "call the same four people
on Friday". Everything built serves that.

**Shipped:** the pie (4-round match, UNO-scale scoring, standings, round-over
scoreboard replacing the dead hand); `sound.js` (13 synthesised voices, 0 bytes);
`events.js` (see [[snapshot-delta-events]]); keyed `renderSeats`;
`server/assets.js` (brotli + ETag + transitive content hashing, 242KB → 65KB
first load, 304s after); favicon; `scripts/shoot.js` ([[cdp-capture-harness]]);
`scripts/measure-scoring.js`; PROTOCOL v1.1 (`match` block, purely additive).

**Why the pie is 4 fixed rounds, not "first to N":** measured 2000 bot rounds per
seat count — winner banks a median of **51 / 85 / 137** points at 2 / 3 / 4
players. A round is worth 2.7x more at four seats, so any single target runs ~4
rounds at one table size and ~8 at another, and at four players the first round
win usually decides it. Reproduce with `node scripts/measure-scoring.js`. A
research agent independently measured 49/86/136 — two methods agreeing.

**Bugs found and fixed, each with a pre-fix reproduction:**
- **A CSS rule matching ZERO elements.** `.stage.is-compressed + .tray` — but
  `#celebration` sits between them, so the *adjacent* combinator never matched.
  The carefully-measured tray-scroll block had never applied, and at 360x640
  with the callout bar open the Leave button sat **104px below the viewport,
  unreachable** (page not scrollable, tray not scrollable). `~` fixes it.
  **Rule: assert a selector's match count; a selector that matches nothing is
  indistinguishable from a rule nobody wrote.** Same class as the `vercel.json`
  `source`-never-matches trap in the global harness.
- **`renderSeats` rebuilt every seat via innerHTML on any change** → restarted a
  vulnerable player's alarm on other people's moves, made the seats' own opacity
  transitions permanently dead, and was the most DOM churn in the app. Measured:
  0/3 seat nodes survived 9 repaints before, 3/3 survived 11 after.
- **Sound led the card by 260ms** — see [[snapshot-delta-events]].
- **Two-player REVERSE announced a reversal that never happened**
  (`game.js:374-380` — it acts as a SKIP and never touches `direction`).
- **Drawn WILD showed two decision bars at once**, and the drawn bar's "Play it"
  re-opened the picker already on screen.
- **The win banner contradicted the scoreboard** on the final slice (round winner
  vs pie champion are usually different people).
- **Forfeit scoring trap, caught before it shipped:** `removePlayer` returns a
  leaving hand to the deck at `game.js:451` BEFORE `endRound` at `:458`, so the
  obvious scoring implementation banks those cards as zero. `endRound` takes
  `forfeited` as an argument.

**Tier 2 started — the round boundary (PROTOCOL v1.2).** `newRound` is no longer
host-gated (any seated human deals), a 10s countdown deals the next slice
itself, and `hold` stops it stickily. It NEVER arms on a finished pie — that
boundary earns a pause. `nextDueAt` goes on the wire as an ABSOLUTE epoch ms, so
the client renders the countdown from its own clock and the server never ticks at
it. The countdown must stay a quiet line in the tray's type: a counting digit
turns a pause into pressure. Verified: dealt itself at exactly 10s with nothing
clicked; Hold still not dealt 14s later; `npm run smoke` seats TWO humans and
proves the non-host's deal is accepted (a single client cannot test this).

**Warm ground landed.** `--page`/`--page-glow`/`--shell`/`--tray-bg` plus the two
hand-fade stops that hard-coded the old navy. Doing THREE of the four left the
tray navy and put a visible seam across the screen — a partial palette swap is
worse than none. `npm run contrast` (new) composites the live ink ladder against
every live surface; worst case 6.18 → 5.58:1 against a 4.5 floor. **Never claim a
contrast-neutral palette change without running it.**

**Open / UNVERIFIED:** iOS audio (written to the documented unlock pattern,
verified only in headless Chrome — needs a device); sound *character* (nobody has
listened to it); the warm-ground palette (captured side-by-side, awaiting a taste
call); the win banner still covers the top seat.

**Next, by judged priority:** bots that can be caught (`bot.js:73` declares TONDO unconditionally, so
the game's signature mechanic is unreachable solo); two-player action-card
legibility; motion for the remaining silent events.

**Deliberately rejected** (full list in the doc): durable named tables (an empty
named table says "your friends chose not to come"); streaks/dailies/XP; badges;
chasing bot strength (a threat-aware heuristic went 1973-2027 over 4000 rounds —
a coin flip); idle card sway; screen shake.
