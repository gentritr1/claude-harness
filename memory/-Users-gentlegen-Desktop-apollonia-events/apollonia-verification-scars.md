---
name: apollonia-verification-scars
description: "How to actually verify Apollonia UI changes — preview pane limits, headless-Chrome harness, form gotchas"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6cc4e8c9-9d9e-4243-a4d4-79b57c5662b7
  modified: 2026-08-01T15:17:07.693Z
---

Verification lessons from the 2026-07-11 UX pass (see [[apollonia-stack]]):

- **Browser-pane preview is unreliable for this project when backgrounded**: when the
  user isn't viewing the pane, `document.visibilityState === "hidden"` and
  `requestAnimationFrame` NEVER fires → React hydration stalls, CDP scroll/input
  times out, screenshots show stale frames. Do NOT conclude "my change broke
  hydration" from the pane — reproduce on baseline first (this exact mistake cost a
  full git-stash bisect; baseline failed identically).
- **Working harness**: puppeteer-core@23 + system Chrome `headless: "new"` against
  the dev server hydrates fine. Scripts live in the session scratchpad pattern
  (`verify-ux.mjs` style: assert strip dates, prefills, wizard steps, submit E2E,
  375px header). Radix Select options need pointerdown/pointerup + click dispatched.
- **React `<ViewTransition>` (experimental) was removed** from the public layout on
  2026-07-11: it threw `InvalidStateError: Transition was aborted because of invalid
  state` on hidden documents (dev overlay showed "1 Issue" on every load) and could
  wedge painting. Replaced with `(public)/template.tsx` + `.page-enter` CSS
  animation. The `site-header` viewTransitionName + gallery-lightbox native
  `startViewTransition` are still used and fine (user-initiated, document visible).
- **RHF register() inputs lose their DISPLAYED value if their subtree unmounts**
  (state persists, display doesn't). The reservation wizard therefore keeps both
  step fieldsets mounted and toggles `hidden` — don't "simplify" back to a ternary.
- **Global focus ring**: `globals.css` has an UNLAYERED `:where(...):focus-visible`
  gold outline that beats ALL Tailwind utilities (cascade layers). Suppressing it
  requires another unlayered rule, not `focus:outline-none`.
- Codebase is prettier@3-default formatted (no config file). After hand-edits run
  `pnpm dlx prettier@3 --write` on touched files or diffs look alien.
- E2E submits write real PENDING rows to Neon; use email `ux-test@apollonia.events`
  and delete after (`cleanup-test-rows.ts` pattern: `pnpm exec tsx --tsconfig
  tsconfig.json <script>` resolves the `@/` alias).
- FULL OWNER ANSWERS applied 2026-07-12 (round 6): address Rr. Demush Shabani,
  60000 Gjilan; phones +38344376237 / +38348190599 (WhatsApp on first); Instagram
  apollonia.events; email UNCONFIRMED (removed from site/JSON-LD); NO kitchen
  (client brings catering+drinks — sold as a feature); no coordinator; venue
  provides DJ/sound; noise curfew 23:00, stay till ~00:00–01:00; deposit 50%,
  cancel 48–72h; UP TO 2 EVENTS/DAY (exclusivity promise removed everywhere incl.
  OG-image tagline; booking logic still blocks on confirmed dates — deliberate);
  seated 30–35 / standing 60; time slots now generated 10:00–22:00 half-hourly
  (buildTimeSlots() in content.ts, admin aligned); fictional testimonials replaced
  by ONE real epigraph (first event: ekspozita "Kujtesë e Vlerave artistike");
  heritage angle owner-approved KEEP; timeline now 10/17/20/23. Still open: name
  spelling (domain will be Apolloniaevents.com), pricing (recommendation delivered:
  ~€200 weekend / €140 weekday evening w/ sound, €80 daytime block, publish "nga
  €90" — Kosovo comparables are per-person restaurant models), email, photos.
- VENUE TRUTH (2026-07-12, owner-confirmed): single ~60 m² hall in GJILAN, KOSOVO
  (addressCountry XK), capacity 50–60 (site publishes "deri në 60"; schema +
  manual-reservation validation cap 60). NOT near the sea, no olives/terrace/
  courtyard/marble — all such copy rewritten ("Një sallë, tri kohë" concept on
  /venue). Heritage band stays as a NAME story only. VENUE-QUESTIONS.md renumbered
  to 39 open questions with ✅ RESOLVED rows.
- Round 5 gotchas: shadcn SelectTrigger sized via `data-[size=default]:h-8` beats
  className h-11 (fixed: plain classes before className in cn()); double-click on
  "Vazhdo" hit the submit button that replaces it → 400ms entry-grace ref in
  handleFormSubmit; free-date chips moved INSIDE ReservationForm (hidden after
  submit); "Printo ftesën" print CSS — Turbopack/Lightning SILENTLY DROPS a whole
  `@media print` block if `@page` is nested inside it (keep @page top-level).
- Hero sub-lg fix (Sonnet-implemented): text column needed `mx-auto lg:mx-0` +
  CTA row `justify-center lg:justify-start` (block was left-pinned while its text
  centered); mobile-only spacing tightened (py-14/mb-6/mt-6/mt-8/gap-y-12 at base,
  originals restored at sm:) so the full hero incl. primary CTA sits above the
  375×812 fold (measured CTA bottom 592px).
- Round 4 (2026-07-12, Opus): meander draws on reveal via `.reveal-ready.is-visible
  .meander-line` (transition ONLY on the drawn-state rule — on the base rule it
  visibly un-draws at hydration); wizard `step-panel` entrance gated by
  `form[data-stepped]`; `.date-chip` hover; occasion-tinted invitation via
  `--invitation-accent` (aegean #2c5c6b / olive #6f7245 / gold-text #8a6b3c /
  ink-soft #475158 for marble — marble tokens fail AA on cream). VENUE-QUESTIONS.md
  at repo root = 45-question owner questionnaire + assumptions inventory; content
  rewrite is blocked on its answers (no olives / single-room reality expected).
- **An empty table hides server/client boundary bugs** (2026-08-01): `getCloudinaryBlurUrl`
  lived in a `"use client"` module but was called during server render by
  `CloudinaryGalleryTile`. `/gallery` never tripped it (rendered inside the client
  lightbox); the home page renders the tile on the server and threw
  "Attempted to call … from the server". The branch was unreachable for weeks
  because `GalleryImage` had 0 rows — **the first real data was the trigger**. Fixed by
  moving the pure URL builder to `src/lib/cloudinary-blur.ts`. Rule: after seeding a
  table for the first time, re-exercise EVERY page that reads it, not just the
  obvious one.
- **Neon free tier scales to zero and genuinely goes away** — on 2026-08-01 it was
  unreachable three separate times, once for several minutes across fresh processes
  (TCP 5432 connected, DNS resolved, Prisma still said "Can't reach database server";
  both pooled AND direct failed; it came back on its own with all data intact). Public
  reads therefore go through `getPublicGalleryImages` (`src/server/gallery-read.ts`),
  which logs and returns `[]`. **Verify resilience by building against a deliberately
  dead URL** — `DATABASE_URL="postgresql://u:p@127.0.0.1:1/none" pnpm build` must reach
  21/21 static pages. Testing while the DB is merely *flaky* proves nothing: one such
  "test" passed only because Neon had quietly recovered mid-run.
- **`next/image` can 200 on every variant and still paint NOTHING** (2026-08-01,
  logo badge): at `deviceScaleFactor: 2` the header's 2x srcset entry
  (`/_next/image?...&w=96`) never completed — `complete:false`, `naturalWidth:0` —
  while the same element at dsf=1 loaded fine, and curl fetched every variant in
  2-3ms. The element still occupied its 40px slot, so the LAYOUT looked right and
  only the bitmap was missing. Detection rule: never trust `img.complete` or a
  200 from curl — **sample the screenshot's pixels** in the element's rect
  (`dark px N/total`) at the SAME deviceScaleFactor you ship. Fix: a fixed-size
  decorative mark should be `unoptimized` off a pre-sized file
  (`logo-badge-96/192.png`), which also stops burning Vercel image-optimization
  quota. See [[apollonia-brand-logo]].
- `next start` readiness races produce FALSE failures (2026-08-01): a
  `for i in …; do curl && break; done` warmup loop exits as soon as curl returns 0,
  but the very next request can still get `code=000` or an empty body. Two scares
  came from this (a `000` on `/` and an apparently-empty free-dates strip on
  `/reserve`) — both were 3/3 correct on retry. Always retry a smoke assertion 3×
  before calling it a regression.
- `getUpcomingFreeDates` / `getConfirmedReservationDates` in `src/server/reservations.ts`
  SWALLOW DB errors (`catch → return []`), so a 200 on `/reserve` does NOT prove
  database connectivity. Discriminating test: DB up → 3 free-Saturday chips render
  (`date=YYYY-MM-DD` in HTML); DB down → strip is empty and a
  "Failed to fetch confirmed reservation dates" line appears in the server log.
  By contrast `/` (which prerenders `db.galleryImage.findMany()`) does NOT catch,
  so a bad DB URL is a hard build failure there. See [[apollonia-neon-env]].
- Recursive `grep -rIn` from the repo root silently SKIPPED `.env` and `.env.bak`
  while matching `.env.example` — never conclude "no stale config references" from a
  recursive grep alone; grep the env files by explicit path.
- Preview-managed dev server (launch.json "apollonia-dev") dies between turns —
  always `curl localhost:3000` before a headless run and preview_start if dead.
- Round 3 (2026-07-12, Opus-implemented): calendar cells sized via shadcn
  `--cell-size` var in calendar.tsx (`--spacing(9)` fine / `--spacing(11)` via
  `pointer-coarse:` = 44px); skip link is unlayered `.skip-link` in globals.css
  (sr-only utility LOSES to unlayered `.btn` — same cascade-layer trap as the
  focus ring); reservation draft persists in sessionStorage key
  `apollonia-reservation-draft` (URL params win; cleared on submit); JSON-LD
  EventVenue/LocalBusiness in root layout + FAQPage on /reserve; error.tsx added.
- Testing gotchas: React 19 ABSORBS a single client render/hydration throw by
  retrying — an error.tsx test must throw ≥3 consecutive times to reach the
  boundary; `_`-prefixed app-router folders are PRIVATE (route 404s — a probe
  page there tests not-found, not what you think); SSR runs module code, so
  module-level one-shot throw flags latch on the server and never re-throw.
- Shipped 2026-07-12 (Opus-implemented, Claude-briefed, all headless-verified):
  4-phase "living light" hero arch via `html[data-daypart]` (dawn 6–9 / day 10–16 /
  golden 17–19 / night, set in the same toneScript as data-tone), scroll-tracked
  timeline gnomon dot (`day-timeline-gnomon.tsx`, hero-arch rAF pattern), and
  stroke-only `invitation-seal.tsx` shown only on `state="received"`. Gotcha: the
  static `.timeline-dot`s sit ~13px ABOVE `.timeline-line` (pre-existing); the
  gnomon rides the line, so it passes slightly below station dots — intentional.
  When measuring `.timeline-line` geometry, wait ≥1300ms for its scaleX draw.
