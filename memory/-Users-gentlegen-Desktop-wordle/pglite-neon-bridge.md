---
name: pglite-neon-bridge
description: How to execute the Neon adapter against real Postgres with no database — pglite + fetchEndpoint shim
metadata: 
  node_type: memory
  type: reference
  originSessionId: 693f3995-82ac-4e0b-97b8-77d524a0e390
  modified: 2026-08-04T19:32:55.286Z
---

To execute `api/_lib/store-neon.js` (and any future Neon SQL) without a real Neon project:
install `@electric-sql/pglite` OUTSIDE the repo (scratchpad), run a tiny HTTP server that
speaks `@neondatabase/serverless`'s fetch protocol — request `POST {query, params}`,
response `{rows, fields:[{name,dataTypeID:25}], command, rowCount}` with values as raw text
(bool→'t'/'f', null→null; the adapter formats dates in SQL via to_char so text is faithful),
errors as HTTP 400 `{message, code}` so the SQLSTATE reaches `mapError` — then preload a
module that sets `neonConfig.fetchEndpoint` to it and run:

```
RRETHI_TEST_NEON_URL='postgres://bridge:bridge@bridge.local/bridge' \
  node --import <bridge.mjs> --test tests/rrethi-store.test.js
```

Proven 2026-08-04: all 24 conformance tests including the whole Neon block passed
(RETURNING conflict mapping, FK SQLSTATE translation, cascades, takeToken rollover).
Honest residual: real Postgres semantics, but not Neon-the-service (network, pooling).

**Productionized 2026-08-04 (commit 27aeb65):** lives at `scripts/neon-pglite-bridge.mjs`,
run with `npm run test:neon-bridge` (self-contained — the preload defaults the env var).
`@electric-sql/pglite` 0.5.4 exact-pinned devDependency (zero transitive deps). CI has a
dedicated `neon-bridge` job — the ONLY job that runs `npm ci`; the `check` job deliberately
installs nothing so the zero-runtime-deps posture stays proven from a bare checkout
(`rm -rf node_modules && npm test` re-verified green, Neon block skips gracefully).
Protocol details verified against `@neondatabase/serverless` 1.1.0 source (headers
Neon-Raw-Text-Output / Neon-Array-Mode, 400-error field list incl. `code`).
See [[retention-plan-2026-08]].
