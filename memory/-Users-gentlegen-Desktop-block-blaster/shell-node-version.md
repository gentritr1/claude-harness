---
name: shell-node-version
description: Default shell Node is v14 — must prepend nvm Node 20.19.4 to PATH before any npm/node command
metadata: 
  node_type: memory
  type: project
  originSessionId: b210a702-b20c-481f-9b18-2ae106e26af4
---

The login shell on this machine defaults to Node v14.19.3 (nvm default), which breaks `npm run verify` with the cryptic error `node: bad option: --import`. Rowflare requires Node 20.19.4 (installed via nvm).

**Why:** Expo SDK 56 and the tsx-based test runner need Node >=20.19.4; the failure message doesn't say so.

**How to apply:** Before any npm/node command in this repo run
`export PATH="$HOME/.nvm/versions/node/v20.19.4/bin:$PATH"`.
As of 2026-07-17 a `.nvmrc` + preflight guard script was being added so wrong-Node runs fail with a clear message.
