---
name: build-workers-share-the-db
description: next build runs lib/store.ts schema setup in ~7 worker processes at once against the same SQLite file; migrations must tolerate a concurrent winner
metadata:
  node_type: memory
  type: project
  originSessionId: 2336fd90-e02c-4aed-9ba0-569ef7381ed7
  modified: 2026-10-13T21:34:51.420Z
---

`next build` imports lib/store.ts in several workers (7 on this Mac) against one DATABASE_PATH, so schema setup runs concurrently. The check-then-ALTER in `addColumn` raced: the first build of feat/resend-setup (2026-10-13) failed with `duplicate column name: email_failed_at`. Fixed in fc09171 by ignoring that error. Plain "start 7 at once" scripts did NOT reproduce it (window < 1 ms); a forced interleave (A checks, B alters, A alters) did.

**Why:** any new migration step (backfill UPDATE, index, column) runs N times in parallel on the first build after it lands.
**How to apply:** make every schema step idempotent under concurrency; to test one, build against a pre-migration copy of the DB (DATABASE_PATH=copy) and force the interleaving in a script rather than trusting one green build. See [[typed-date-intermediate-values]] for another date/env-dependent trap.
