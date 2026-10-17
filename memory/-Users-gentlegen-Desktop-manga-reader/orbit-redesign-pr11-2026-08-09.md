---
name: orbit-redesign-pr11-2026-08-09
description: "2026-08-09 Manga Orbit redesign PR #11 — verification results, two pre-existing bugs found, and the driving gotchas that nearly produced false findings"
metadata: 
  node_type: memory
  type: project
  originSessionId: d3990f63-8234-4070-83de-a9592946c6ab
  modified: 2026-08-09T10:09:54.959Z
---

PR #11 (branch `redesign/manga-orbit-cohesive-units`, commits 4cb9205 + 4ad2fad): Yomi → **Manga Orbit** rebrand, home collapsed from nine widgets to three units (Hero / Yours / The shelf), per-chapter `ReadingHistoryEntry`. Brand contradiction resolved: coral retired, `--shelf-edge` now violet→cyan. **localStorage/cookie keys deliberately keep the `yomi-` prefix** — renaming wipes every existing reader's progress, prefs and language.

**Verified 2026-08-09:** migration applies on a DB holding the older chain and its seed clause copies real pre-existing `ReadingProgress` rows into history with `createdAt` = original `updatedAt` (dates survive). Authed run wrote 3 `ReadingHistoryEntry` rows (ch 2,3,4) against 1 `ReadingProgress` row — the feature's core claim holds. `/history`, `/favorites` (toggle persists), `/shelves`, `SeriesSpine` (null at zero progress, renders after) all confirmed.

**Two bugs found, both pre-existing on `main` — confirmed by checking out main, not assumed:**
1. **Next chapter is a dead end.** `app/read/[chapterId]/page.tsx:60` skips dedupe so `findIndex` can locate the current row, so "next" from ch.1-readable resolves to ch.1's *external Viz row* (`pages: 0`) → "Chapter 1 is an official release", plus 5× 404 from the prefetcher. Same trap `pickFirstReadableChapter` already fixes for "Start reading". Fix = dedupe by chapter number preferring the readable row, index by number not row id.
2. **Duplicate `ViewTransition name="cover-{mangaId}"`** whenever one title sits in two units → kills the cover morph. `cover-transition.tsx` untouched by the PR; `manga-card.tsx` has the same 8 usages on both branches.

**Open, genuinely unverified:** page-position tracking never advanced past page 1 and `ReadingSession` stayed empty, so `/analytics` shows header "4 pages · 1 min" next to tiles "0 PAGES READ / 0m / 0 SERIES" — tiles read `prisma.readingSession` (`lib/reading-analytics.ts:62`), header reads client-side stats. Needs a human scrolling a chapter in a normal browser to tell app bug from harness artifact.

**Driving gotchas that nearly produced false findings (all three cost real time):**
- `preview` screenshots misrender the reader as a narrow left-pinned column; `getBoundingClientRect` showed the DOM correct (768px centred in 1280). **Measure geometry before reporting a layout bug from a screenshot.**
- Global CSS sets `scroll-behavior: smooth`, so `window.scrollBy` / successive `scrollTo` calls silently no-op or cap. Use `scrollTo({top, behavior:'instant'})`.
- Harness pointer clicks miss (screenshot-space coordinate scaling) — `elementFromPoint` confirmed the button was under the reported coordinate. Dispatch a real `MouseEvent` to exercise React handlers; that is also the discriminating test for "is this control broken".
- 36×36 controls are NOT tap-target violations — computed `::after` inset `-4px` yields 44×44. Check the pseudo-element before flagging.

Permission classifier blocks `prisma migrate deploy` and any script reading `AUTH_SECRET` to mint a session JWT. The latter is a good block — the path forward is the user signing in themselves, then driving the authed surfaces.

Related: [[reader-audit-2026-07-12]], [[running-yomi-locally]]
