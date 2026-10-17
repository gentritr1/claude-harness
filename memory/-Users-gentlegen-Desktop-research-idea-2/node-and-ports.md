---
name: node-and-ports
description: "Use nvm Node 24 (shell default 14 breaks everything); dev server port 8090 (8081 is lucky-shelf's)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 34efc46f-cf4b-48ec-91db-1c0e87da9387
---

Shell default Node is v14 — breaks vitest, native TS type-stripping, most tooling. Always:
`export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24` (v24.18.0 verified working
2026-07-18; fallback 20.19.4). `node tools/fuseline-solver.ts <mode>` runs directly on 24
(native type-stripping, no tsx needed).

Dev server: use port **8090** — 8081 belongs to lucky-shelf (inherited scar). Also check
`lsof` + curl the title before trusting localhost (stray IPv6 listener scar from
block-blaster).

Related: [[project-overview]].
