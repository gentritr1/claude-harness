---
name: deploy-caching
description: "How the Vercel deploy artifact is built and verified (scripts/build.mjs hashing, vercel.json headers, request-count harness)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1228ee92-125a-44af-96df-2cd8fa10ba9b
  modified: 2026-08-23T19:45:53.872Z
---

Added 2026-08-23 (pass 14, deploy to Vercel).

- **Development stays build-free; only deployment builds.** `node scripts/build.mjs` (zero deps) writes `dist/`. The repo root still serves unhashed under `python3 -m http.server 4173`. `dist/` is gitignored.
- **`posix.join(posix.dirname("./config.js"), name)` returns a BARE specifier** (`"config.abc.js"`), which resolves fine on the filesystem and not at all in a browser. Rewrite import specifiers by replacing the basename only: `specifier.replace(/[^/]+$/, hashedBasename)`. → An integrity check that only asks "does the target exist on disk?" cannot see this; assert the specifier *shape* (`./` or `../` prefix) separately.
- **Hash in dependency order** (DFS from `src/app.js`, leaves first) so a module's hash covers its rewritten imports. Verified by editing `src/data/morse.js` in a scratch copy: 13 transitive importers changed hash, the 5 non-importers (config, words, transmissions, storage, elements) did not.
- **Measured request counts** (server-side log = what Vercel bills as edge requests): unbuilt root cold 27 / reload 27 (25× 304) / fresh return 26; `dist/` with the headers applied cold 27 / reload **1** / fresh return **1**. Google Fonts adds 5 third-party requests either way (67.9 KB), billed by nobody.
- **CSP needs no `'unsafe-inline'`.** No inline `<script>`, no `<style>`, no `style=` attribute; the JS only calls `element.style.setProperty(...)` and assigns `element.style.transform` — CSSOM writes CSP does not govern. 0 violations across the full guide + rounds + settings flow.
- **Verification harness:** `scratchpad/serve14.mjs` serves any directory applying `vercel.json` verbatim (path-to-regexp v6 subset compiler) and logs every request; `patterns14.mjs` asserts every `source` matches a real `dist/` path *and* every path has a cache policy (the global rule's named failure mode is a pattern that matches nothing); `requests14.mjs` counts cold/reload/return; `flow14.mjs` drives the whole product with real CDP keys; `cdp14.mjs` is `cdp11.mjs` with the HTTP cache **left on** (cdp11 disables it, which silently destroys any cache measurement).
- **Reset is two-click** (arm → "Confirm reset" within 5 s). A single `.click()` on `#resetProgress` changes nothing and reads as a broken reset.
- Brief 14 predicted a minifier would save "a few KB after compression". Measured: stripping comments/indentation alone takes `dist/` from 84.5 KB brotli to 54.6 KB (−35 %), and a real minifier would save more. Still declined — the saving is one-time per visitor under `immutable`, and it does not touch the edge-request axis this pass targeted — but the brief's number was wrong by an order of magnitude. → A brief that justifies a decision with a size claim must name the script that measured it.

**How to apply:** any change to `index.html`'s asset links, or a new file under `src/`/`styles/`, must be re-run through `node scripts/build.mjs` + `patterns14.mjs` before deploying. Related: [[verification-recipe]].

**Deployed and verified 2026-08-23** — https://morse-code-amber.vercel.app (commit `665fe37`). Live results, all measured, not inferred:
- Document `public, max-age=0, must-revalidate`, `x-vercel-cache: HIT`, revalidates **304 / 0 bytes**. Deployed `index.html` is **byte-identical** to a local `node scripts/build.mjs` run (the build is reproducible end to end).
- All four asset classes `public, max-age=31536000, immutable`, `x-vercel-cache: HIT` — **including both `:hash([0-9a-f]{8})` patterns** (`/styles.<hash>.css`, `/favicon.<hash>.svg`), which were the one piece of `vercel.json` syntax that could not be verified locally. They work.
- `Vercel-CDN-Cache-Control` correctly **absent** from client responses (stripped at the edge, as designed).
- **Warm reload = 1 request.** 25 subresources all served from browser cache, 0 bytes wire; only a 300-byte document revalidation. Cold = 26 requests, 107 KB wire / 312 KB decoded (brotli ~29 %: trainer.js 53,228→15,718).
- CSP/nosniff/referrer-policy present on every response **including 404s**; HSTS `max-age=63072000; includeSubDomains; preload` (Vercel default). Zero console errors, zero `securitypolicyviolation` events across guide → live preview → seeded session.
- `cleanUrls` works: `/index.html` → 308 → `/`. A stale hash 404s rather than serving old code — correct for content-addressed assets.
