---
name: pizzuno-setup
description: "Za! (ex-Pizzuno) repo origin, rebrand rationale, port 3000 conflict"
metadata: 
  node_type: memory
  type: project
  originSessionId: 36810674-ff73-4118-8cbb-668e7af1b950
  modified: 2026-08-06T18:06:04.548Z
---

The game formerly named Pizzuno was rebranded to **Za!** on 2026-08-06 and lives at git@github.com:gentritr1/za-game.git (renamed from uno-variant; GitHub redirects the old URL). The local folder is still `~/Desktop/pizzuno`.

- Rebrand reason: pizz.uno is an existing UNO-like web game literally named "Pizzuno" (by Comfort Food Games), and the old name contained Mattel's UNO mark. User chose "Za!" (slang for pizza) over "Last Slice", accepting weaker SEO for the shout-word appeal.
- Naming convention: the brand is "Za!" (with bang) in titles/logo, "Za" in prose, and the in-game shout is "ZA!". Wire protocol action, CSS classes, and localStorage keys use plain `za`.
- Branded art (logo-wordmark.png, card-back.png) was regenerated with GPT Image 2 via Higgsfield MCP using the old assets as reference images; "transparent background" comes back as a baked checkerboard — run the remove_background tool on the job, then verify a corner pixel's alpha is 0 before trusting it.
- Port 3000 is usually taken locally by the Apollonia Events Next.js dev server — never kill it; run with `PORT=<other> npm start` (server reads `process.env.PORT`, server/index.js:17).
- Test suite: `npm test` runs test/rules.test.js — 43 tests, green after the rebrand.
