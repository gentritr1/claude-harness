---
name: next-level-implementation-status
description: What of NEXT-LEVEL-PLAN.md was implemented on 2026-09-11, the deploy prerequisite (prisma db push for publicToken), and what is still owner-gated
metadata:
  type: project
---

On 2026-09-11 four Opus 5 agents implemented the non-owner-gated parts of `NEXT-LEVEL-PLAN.md`
(Waves 1, 2, 3, 4, 5, 7 — ~32 files, uncommitted at time of writing). Build 23/23, tsc clean,
lint 0 errors.

**Deploy prerequisite — must happen BEFORE the next deploy:** `pnpm db:push` against the
production Neon DB to add `Reservation.publicToken String? @unique`. Until then every
`/reserve` submission fails at the insert (generic submit error) and admin full-row `findMany`
calls throw "column does not exist". Additive + nullable, no wipe risk. Old rows keep NULL →
their `/ftesa/<token>` 404s; admin must hide the share link for NULL tokens (not yet built).

**Still owner-gated, deliberately NOT built:** price band, photography commission, gold-text
hex, ornament retirement (temple/wave/coastline), dark lightbox, warm shadows, image grade,
sundial-on-mobile rework, `.ics` attachments, `GUEST_AFTER` reminder, analytics layer.

**Taste calls I made that need an eyeball:** the home CTA plate is now flat gold-soft with an
aegean-deep label (gold-deep plate measured 1.66:1 against the band); five meander/wave call
sites got dimmer on dark grounds because `text-*` colours finally take effect.

**Spec corrections the agents found (fold back into the specs):** `hero-reveal + backwards`
would not animate at all — needs a from-only keyframe (`hero-rise`); temple loop "1272ms" is
really 1560ms with the 24ms stagger; `/ftesa` belongs INSIDE `(public)` (review note beat the
main spec); `#reservation-form dl > dt` selector is wrong when pairs are wrapped in divs.
See [[reserve-route-is-uncached]] — the cache fix landed (300s, tag-invalidated) but `/reserve`
is still ƒ dynamic because `searchParams` is read server-side (spec part (c) not done).
