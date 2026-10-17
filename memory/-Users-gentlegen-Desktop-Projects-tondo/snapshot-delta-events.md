---
name: snapshot-delta-events
description: public/js/events.js derives game events from snapshot deltas — the keystone for sound and one-shot motion, plus the audio-timing rule
metadata:
  type: project
---

Tondo's client repaints EVERYTHING from every `state` snapshot, so nothing in the
render path can tell a real move from the same board painted twice. Anything
that must fire once per event needs that difference, and PROTOCOL v1 carries
state, not events.

`public/js/events.js` (2026-09-09) solves it: pure, DOM-free,
`deriveEvents(prev, snap)` → 13 event types. Tested in `test/events.test.mjs`
against the REAL `server/game.js` diffing real `viewFor()` output — not
fixtures, which would only prove the deriver agrees with my idea of the wire.

**The three derivations that are easy to get wrong:**
- A **SKIP's victim** must be read from the PREVIOUS turn order — by the time the
  snapshot arrives the turn has already moved past them.
- A **REVERSE** likewise: `direction` has already flipped.
- A **callout** is the only way a hand grows by two with NO new card on the pile.
  A +2 always arrives together with the PLUS2 that caused it. Without that test
  the two are indistinguishable.

Deliberately NOT reduced-motion aware — less movement is not less information;
filtering belongs at each consumer.

**AUDIO TIMING RULE (a defect that shipped and was caught the same day):** the
played card is still in flight for `MS.flight` (260ms) when the snapshot lands,
so a sound fired immediately arrives ~260ms BEFORE the card it describes. Audio
leading video is more noticeable than trailing it. `sound.playForEvents()` takes
`{impactAt}` and every voice takes a start offset — the same delay `ledgerAdd`
already used at app.js:518. **Any new per-event effect must ask "when does the
thing I describe actually appear on screen?" before it fires.**

`events.js` also computes actor/victim (`youHit`, `byYou`, `youSkipped`); using
it is what makes a +2 landing on YOU sound different from one across the table.
