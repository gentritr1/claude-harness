---
name: appcare-landing-open-questions
description: Owner decisions pending after the 2026-10-09 landing revision on branch feat/landing-next-level (commit 90e8b38)
metadata:
  node_type: memory
  type: project
  originSessionId: 4c6ca233-30a5-409f-8b36-6a97f716a4b6
  modified: 2026-10-09T14:03:58.236Z
---

The 2026-10-09 landing revision (branch `feat/landing-next-level`, commit 90e8b38) left these decisions open for the owner:

- **Pre-sale CTA dead end.** "Scan my app" goes to /check, which says "come back Nov 15". Should it collect an email? That needs a backend and a sender, plus the §12 monitoring plan first.
- **Base44 and v0.** Resolved 2026-10-10: Base44 doesn't run on Supabase, so it was removed. v0 stays, named only for apps that use Supabase. Whether v0 can export to GitHub is still unverified.
- **Dedupe fact.** "An issue two tools both catch is listed once" was removed along with the carousel. Bring it back?
- **Footer** says "AppCare is a working name". Terms and Privacy links are hidden until real pages exist.
- **Sample health score** of 61 renders amber despite two criticals.
- **Missing FAQ answers** (do not invent them): does code or data go to an AI model? What if the fix prompt fails? How long does setup take?
- **Taste acceptance pending.** The paper report, Newsreader serif and motion feel need the owner's yes on the screenshots. This is UNVERIFIED until they give it.

**Why:** these are product facts or taste calls that agents must not decide.

**How to apply:** ask before touching these areas. The full record is in `docs/audits/2026-10-09-landing-next-level.md`. Related: [[appcare-css-and-motion-gotchas]].

**Update 2026-10-10.** The research is done; it lives in `research/out/` on branch `feat/claude-platform`. Landing fixes landed on `feat/landing-next-level` (commits 4ffa7a5, 93aafb5): Base44 removed, the Escape.tech credit fixed, the lead stat is now Palmer's CVE figure, and two scope FAQs were added. Still waiting on the owner:
- a free instant check, which the research recommends but contradicts the confirmed "no free check" rule;
- refund terms, plus the EU/UK consent checkbox at checkout (not sourced yet);
- founder names and faces;
- a security.txt contact;
- an original data study (legal review first);
- a demo app for a real sample report;
- a manual check of Lovable Cloud SQL access;
- a redesign of the anonymous probe for Supabase's new keys (product work).

**Update 2026-10-10, later.** PR #1 (`feat/landing-next-level` into `feat/landing-page`) is landing-only again, at commit 61c4aa6. PR #2 (`feat/claude-platform`, research) is stacked on it. `feat/dashboard` is NOT merged and has no PR yet.
- Its 2 conflicts with #1 are in `content.ts` and `scan-form.tsx`. Resolution notes are in the #1 description.
- Its missing `.env.example` fix exists only on the local branch `backup/landing-with-dashboard`.
- Lesson: don't merge another feature branch into a focused PR just to pre-resolve conflicts. It hides the PR's own diff.
