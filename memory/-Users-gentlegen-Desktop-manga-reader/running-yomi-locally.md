---
name: running-yomi-locally
description: How to run the Yomi manga-reader dev server (Node version + preview harness gotcha)
metadata: 
  node_type: memory
  type: project
  originSessionId: a3cca45a-bb97-4532-a9b3-1638a0b7c75d
---

The machine's default `node` is **v14.19.3** — too old for Next 16 (crashes on `??=` and `Object.hasOwn`, which also breaks eslint). Use Node 20: `nvm use 20` (e.g. `/Users/gentlegen/.nvm/versions/node/v20.19.4/bin/node`).

The Claude Preview harness launches `.claude/launch.json` with the old default node and ignores an absolute `runtimeExecutable` node path, so the dev server dies instantly. Workaround that worked: set launch.json to `runtimeExecutable: "bash"` with `runtimeArgs: ["-lc", "export PATH=.../v20.19.4/bin:$PATH; exec node node_modules/next/dist/bin/next dev --webpack"]`. Revert launch.json to `npm run dev` afterward (don't commit the machine-specific path).

`framer-motion` and `html-to-image` may be missing from node_modules and the Prisma client ungenerated → app 500s until `npm install` (under Node 20; postinstall runs `prisma generate`). This does not change package-lock.json.

Preview screenshot gotcha (2026-07-05): `preview_screenshot` returns a blank/solid-background image whenever the page is scrolled (`scrollY > 0`), even though the DOM, a11y snapshot, and computed styles are all fine — it only captures correctly at scroll position 0. Workaround: `window.scrollTo(0,0)` then `preview_resize` the viewport taller (e.g. 1280×2200) so the region of interest fits at the top. Also saw the viewport spontaneously collapse to height 1px after a reload; fix with an explicit `preview_resize`.

**Local DB (2026-07-12, corrected 2026-07-13):** local dev runs on `prisma dev` (Prisma's PGlite-based local Postgres) — **must run under Node ≥ 23.4 (v24.18.0 now installed; `nvm use 24 && npx prisma dev`)**. Node 23.3 + the experimental flag APPEARS to work but `node:sqlite` there lacks `StatementSync.iterate` → the WAL/write path silently fails ("touch processor failed prisma-wal this.stmt.iterate is not a function" spam, queries eventually ConnectorError, login/signup break). Node 20 fails outright. Also: `prisma dev` dies with the session that spawned it — if login throws CredentialsSignin, check the DB is up FIRST (port 51214). It serves `postgres://postgres:postgres@localhost:51214/template1?...`; that URL is set as DATABASE_URL + DIRECT_URL in both `.env` (Prisma CLI reads this) and `.env.local` (Next reads this). Schema created via `prisma db push` — **`migrate deploy` cannot bootstrap a fresh DB: the migrations folder has no baseline init migration** (prod Neon was bootstrapped with db push; flagged in README). Neon creds never existed locally; before this fix .env.local had a stale `file:` SQLite URL against the postgresql provider. See README "Local database".

Two more harness gotchas that fake app regressions (2026-07-12):
1. **Harness key dispatch never triggers native default actions** — `computer key Enter/space` reaches JS listeners but does NOT activate focused buttons or follow focused links (CDP key events without text payload). Diagnose keyboard-activation "bugs" only with a discriminating test (Enter on a handler-free `<a>`: if it doesn't navigate, it's the harness). JS-listener shortcuts (arrows/j/k/z) DO work via this dispatch.
1b. **prisma-dev "prepared statement s0 already exists" — real fix is `&pgbouncer=true` on the connection string** (2026-07-13; restarting only clears it temporarily). The proxy multiplexes sessions so Prisma's named prepared statements collide intermittently — register/login 500 randomly while other queries succeed. Both .env files now carry the param; the URL prisma dev prints does NOT include it.

2. **`window.location.reload()` can wedge the Browser pane into `document.visibilityState === "hidden"`** (persists across navigate/tabs_select/resize and even new tabs). While hidden: key events aren't delivered at all (a capture-phase window listener sees zero events), rAF is paused so smooth-scroll and framer-motion exit animations freeze mid-flight (state flips but DOM looks unchanged — looks exactly like a broken toggle). Check `document.visibilityState` FIRST when keyboard/animation behavior "breaks"; synthetic `KeyboardEvent` dispatch + checking `ev.defaultPrevented` still exercises app JS handlers while hidden.
