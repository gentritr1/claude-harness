---
name: localhost-port-collision
description: "localhost may resolve to a stray IPv6 listener owned by another app — verify with curl + lsof, use 127.0.0.1"
metadata: 
  node_type: memory
  type: user
  originSessionId: 2292c2f0-72df-48de-8be3-5f18015153bb
---

On this machine, stray dev servers linger (e.g. a "Manga Orbit" node process bound to IPv6 `*:3000`). A new server binding IPv4 `127.0.0.1:3000` coexists with it, and `localhost` resolves to the IPv6 one first — so the browser/curl silently shows the *wrong app* with no error.

**Why:** Two listeners on the same port across IP stacks don't conflict; name resolution picks the winner.

**How to apply:** Before browser-verifying any local server, `curl` the URL and check the `<title>` matches the app; if wrong, `lsof -nP -iTCP:<port> -sTCP:LISTEN` to find both listeners and address the server by explicit `127.0.0.1`, or pick a free port. Related: [[shell-node-version]].
