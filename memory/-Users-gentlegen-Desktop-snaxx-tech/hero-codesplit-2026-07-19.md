# Hero code-split + resilience — 2026-07-19

Stabilization pass on the 3D hero for stable-release push.

## What shipped
- **Code-split three/drei/fiber out of the entry chunk.** New `src/components/HeroCanvas.tsx`
  owns the `<Canvas>` + `<HeroScene/>`; `Hero.tsx` loads it via `React.lazy` + `Suspense`.
  `App.tsx` also lazy-loads `LegalPage` + `NotFound`. Result: entry **1,252 KB → 301 KB**
  (gzip 353 → 95); three lives only in `HeroCanvas-*.js` (924 KB). VERIFIED via build output +
  `grep -o three dist/assets/index-*.js` = 0.
- **Fixed 4 lint errors** → `npx eslint src` = 0. (a) Hero.tsx conditional hooks: moved
  useState/useEffect above the `if (!heroConfig…) return null` guard. (b) HeroScene HintRing
  refs-during-render: replaced `{[ringA,ringB].map(…)}` with two explicit `<mesh>` elements
  (refs only touched in useFrame). No eslint-disable used.
- **WebGL feature-detect** in Hero.tsx (`detectWebGL()` on a throwaway canvas, try/catch) —
  if unavailable, render static `HeroBackdrop` instead of the Canvas (chunk never downloads).
- **Reduced-motion** handled via `frameloop` lever in HeroCanvas: reduced → `"demand"` (scene
  renders once, fully composed but still; also freezes drei's internal Float/Sparkles/Distort
  which can't be gated per-component). A toy-box click briefly resumes `"always"` for ~2.8 s so
  the user-initiated confetti plays, then settles. matchMedia listened once with change handler.
- **Sparkles halved on small screens** (`window.innerWidth < 640`, measured once at mount):
  90→40 and 50→22. dpr already capped [1,2]. h1 "SNAXX" intact; canvas wrapper `aria-hidden`.

## GOTCHA (pre-existing, NOT my regression): dev preview blanks the whole app
- On the running dev server (:7100), the page mounts to an **empty #root**. Root cause captured
  via a temp window 'error' listener: `stats.min.js does not provide an export named 'default'`
  — drei's optimized-dep interop is in a bad state (matches the Avast-quarantine note in
  vite.config's optimizeDeps). Confirmed pre-existing: `git stash` to HEAD → still blank.
- The throw is inside drei module-eval, propagates past Suspense to the nearest error boundary.
  There was none → the **entire site** unmounted (not just the hero).
- **Fix that also hardens prod:** added `CanvasBoundary` (class error boundary) around the
  Suspense/HeroCanvas in Hero.tsx, falling back to `HeroBackdrop`. Now any 3D failure (chunk
  404, WebGL loss, drei/runtime throw) degrades to the static hero and the rest of the page
  survives. VERIFIED: after boundary, dev page renders full site + static hero (screenshot),
  h1=SNAXX, 5 sections. Detection rule → **any lazy 3D/heavy chunk needs an error boundary, not
  just Suspense**; Suspense only covers the pending state, not eval/runtime throws.

## Open verification gap
- The actual **3D toys never render in this dev environment** (same stats.js crash, now caught
  by the boundary → shows fallback). Could not eyeball floating arrows/torus/confetti or the
  reduced-motion freeze at runtime. Prod build is clean + correctly split, but the live 3D
  scene + confetti-under-reduced-motion resume are **UNVERIFIED at runtime** — need a working
  preview (fix the drei dep-optimize / AV quarantine, or a device) to confirm.
