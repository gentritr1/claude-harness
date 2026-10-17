---
name: node-and-ports
description: Shell defaults to Node 14 which breaks vitest; use nvm Node 24. Port 8081 belongs to lucky-shelf.
metadata: 
  node_type: memory
  type: project
  originSessionId: 2b50cf8f-d345-445f-acf6-221a183ff5b7
---

The login shell resolves to Node v14.19.3 (nvm default), which crashes vitest (`??=` SyntaxError). Prefix every npm/npx command with `export PATH="$HOME/.nvm/versions/node/v24.18.0/bin:$PATH"`. Include this in every subagent brief.

Port 8081 is occupied by the [[lucky-shelf]] project's Expo dev server — never kill it. This project's web preview runs on port 8090 via .claude/launch.json ("expo-web").
