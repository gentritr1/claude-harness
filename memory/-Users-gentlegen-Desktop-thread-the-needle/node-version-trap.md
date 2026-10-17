---
name: node-version-trap
description: "Fresh shells can pick nvm Node 14 which breaks `node --test`; prefix PATH with v23"
metadata: 
  node_type: memory
  type: project
  originSessionId: c8dea768-0576-4c80-a808-455bfec9c3e0
---

After a session resume, the Bash tool's shell resolved `node` to nvm v14.19.3, and `npm run check` failed with `node: bad option: --test` (node:test needs 18+). Fix: `export PATH="/Users/gentlegen/.nvm/versions/node/v23.3.0/bin:$PATH"` before npm/node commands in this project. Verify with `node --version` if `--test` errors appear.

Related: [[retention-v1-status]]
