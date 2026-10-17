---
name: npmrc-legacy-peer-deps-lockfile
description: "The owner's ~/.npmrc has legacy-peer-deps=true, so locally written lockfiles omit peer deps and a host's strict `npm ci` fails (EUSAGE); regenerate with --legacy-peer-deps=false"
metadata:
  node_type: memory
  type: reference
  originSessionId: 3fb08f38-07c3-4529-b2e2-21cde8419a74
  modified: 2026-10-10T12:36:21.804Z
---

On this machine `~/.npmrc` sets `legacy-peer-deps=true`. A lockfile written here leaves out peer dependencies. On 2026-10-10 that meant 7 `@electric-sql/pglite-*` peers of the dev-only `pglite-socket`. Render's strict `npm ci --omit=dev` then failed with `EUSAGE … Missing: … from lock file`. Local `npm ci` passed, because it inherits the same setting.

**Fix and check:** run `npm install --package-lock-only --legacy-peer-deps=false`. Then verify with `npm ci --omit=dev --legacy-peer-deps=false --dry-run`. Do this after ANY dependency change, before a deploy.

Applies to every project on this machine that deploys with `npm ci`. Related: [[2026-10-10-crew-retention-shipped]].
