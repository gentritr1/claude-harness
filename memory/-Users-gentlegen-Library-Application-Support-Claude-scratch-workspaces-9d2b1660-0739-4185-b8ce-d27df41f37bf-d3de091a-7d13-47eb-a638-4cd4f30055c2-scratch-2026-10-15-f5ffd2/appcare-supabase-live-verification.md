---
name: appcare-supabase-live-verification
description: "AppCare (Snaxx Tech Supabase security scanner) — catalog/API checks must be verified against a REAL hosted Supabase project, not just PGlite; the scars from Probe 2.0 (PR SnaxxTech/SlopRemover#5, 2026-10-15)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f843166c-822c-4b5b-9f9b-5c4780b06fcf
  modified: 2026-10-15T20:00:31.894Z
---

AppCare is Snaxx Tech's paid security scanner for Supabase apps (repo SnaxxTech/SlopRemover; scanner on `feat/dashboard`, which is 33 commits AHEAD of `main` — `main` lacks `src/lib/content.ts`). Building "Probe 2.0" (PR #5) produced scars that PGlite/unit tests could not catch — only a live run against the owner's seeded test project did.

**Pattern → detection → fix (promote these before claiming a Supabase catalog check VERIFIED):**

1. **PGlite ≠ a hosted Supabase project.** The read-only role `appcare_readonly` is created with only `grant usage on schema public`, so on any real project with Storage it CANNOT read the `storage` schema. `db-lints`'s `publicBucketsListable` lint (`from storage.buckets`) threw `permission denied for schema storage`, and because `runLints` runs ~22 queries in one `Promise.all`, that single rejection aborted the ENTIRE catalog scan → db-lints returned nothing on real projects. Fixed two ways: (a) per-lint error isolation in `runLints` (one failing lint → `[]` + a `db-lints:lint-skipped` note, never aborts); (b) added `grant usage on schema storage` + `grant select on storage.buckets to appcare_readonly` to the setup SQL (connection-steps.tsx). **Detection rule:** run the real code (`withOwnerDatabase` + `runLints`, `findSupabaseProject`, `probeTables`) against a seeded throwaway project before VERIFIED; a cross-check file reader like PGlite grants everything the author seeds, so it never surfaces role-permission failures.

2. **Docs/changelog status ≠ live status.** The spec predicted `GET /rest/v1/` returns 403 "Access to schema is forbidden" (from a Feb-2026 changelog). Live on 2026-10-15 it returns **401** — publishable key → "Secret API key required"; legacy anon → "Invalid API key / only service_role". Re-probe live before pinning a status/body.

3. **`write-exposed` must honor RESTRICTIVE policies.** Fable's final review reproduced a FALSE "critical": a table with RLS on + anon write grant + a permissive `using(true)` policy AND a restrictive per-user policy was flagged "anyone can delete". Postgres: a write needs (a permissive policy passes) AND (all restrictive pass). Fix required a `hasRestrictivePolicy` guard on both `write-exposed` and the pre-existing `policy-always-true` lint. A grant-present-but-RLS-on-no-policy table is a true negative (not exposed) — verified live on `orders`.

**Process notes:** the live harness drives the real code and is gated behind `PROBE2_LIVE=1` (skips in CI). Subagent implementers kept defaulting commit trailers to their own model instead of the owner's required `Co-Authored-By: Claude Opus 5.5`; the controller amended them. Owner rulings this session: keep the scanner reading committed `.env` CONTENTS (finding committed secrets is the product's job — the "never read .env" rule is an AGENT constraint, not a scanner guarantee); `feat/dashboard` is the canonical copy line and is already honest (Gitleaks/Splinter/ZAP overclaims live only on `feat/landing-next-level`). See [[appcare-next-projects-research]].
