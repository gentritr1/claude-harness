---
name: reserve-route-is-uncached
description: /reserve is fully dynamic with an uncached DB query per render and is the slowest page; the homepage RSC-prefetches it
metadata:
  type: project
---

Measured 2026-09-09 against https://www.apolloniaevents.com (n=5 per route, single location):

| Route | cache | median TTFB |
|---|---|---|
| `/`, `/venue`, `/events`, `/gallery` | `x-vercel-cache: HIT`, prerendered | ~209 ms |
| `/reserve` | `private, no-cache, no-store`, `MISS` | ~345 ms (range 298–704) |

**Why:** `src/app/(public)/reserve/page.tsx` awaits `searchParams` (for `?date=` / `?occasion=`),
which makes the route dynamic, and it calls `getConfirmedReservationDates`
(`src/server/reservations.ts:207`) which is **not** wrapped in `unstable_cache` — unlike
`getUpcomingFreeDates`, which is. So the booking page runs a Neon query on every single render,
and Neon's free tier scales to zero (cold starts explain the 704 ms sample).

Worse: the homepage **RSC-prefetches `/reserve`** (observed two `/reserve?_rsc=…` requests in one
page view), so merely rendering the homepage costs a serverless invocation on the dynamic route.

**How to apply:** the conversion page being the slowest page is both a Vercel cost problem
(invocation + duration + DB per visit) and a UX one. Fix candidates: cache the confirmed-dates
query behind the existing `RESERVATION_AVAILABILITY_TAG`, and read the query params on the client
so the shell can prerender. Verify any fix with `curl -sI` for `x-vercel-cache`, not with config.
