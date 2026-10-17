---
name: appcare-css-and-motion-gotchas
description: AppCare landing (Next 16 + Tailwind v4 + motion/react) runtime gotchas found 2026-10-09 that passed tsc/tests/detector
metadata:
  node_type: memory
  type: project
  originSessionId: 4c6ca233-30a5-409f-8b36-6a97f716a4b6
  modified: 2026-10-09T14:03:52.884Z
---

Gotchas on the AppCare landing page found by the 2026-10-09 five-way audit. All of them passed tsc, the vitest suite and the impeccable detector, which returned 0 findings both before and after.

- **Unlayered custom CSS beats Tailwind v4 utilities.** `.glass`, `.press` and `:focus-visible` sat outside any layer. As a result, `bg-*` on glass did nothing, `transition-colors` on buttons was wiped (hovers snapped), and a focused rounded-full input became a 4px rectangle.
  - Custom classes now live in `@layer components`, and focus in `@layer base`.
  - Detection rule: read *computed* styles in a headless probe, never class names.
- **Motion's `useReducedMotion` causes a hydration mismatch** for reduced-motion visitors whenever a component branches markup on it. Use `src/components/motion/use-reduced-motion.ts`, which returns false until hydrated.
- **`cn()` is a plain join with no tailwind-merge**, so conflicting classes resolve by CSS order. Add a Button variant instead of overriding colours via `className`.
- **Scroll-driven 3D in the hero** spread over the copy below `lg`, where the hero isn't pinned. The P0 was "the stack covers the CTA on mobile". Use an `elementFromPoint` hit-probe for any decorative layer near a CTA.
- **Environment:** `@testing-library/dom`, an undeclared peer, was pruned by every `npm install`, and then 6 test files failed to load. It has been declared as a devDependency since 2026-10-10 (PR #1). If it disappears again, check `package.json` first.

**Why:** each of these looked fine in code review and in the green suite. Only runtime probes caught them.

**How to apply:** for any visual or CSS change here, verify with the scratchpad-style playwright probes (computed styles, hit-tests, `document.getAnimations()`, reduced-motion console errors) plus screenshots. See [[appcare-landing-open-questions]].
- **Git near-miss, 2026-10-10.** A failed `git merge --abort` was followed, through `;`, by a `git commit`, which committed mid-merge on the wrong branch. It was caught and amended before push. This is the §6 red flag "bookkeeping chained after a state change" firing again. Rule: run each merge, checkout or commit as its own call and read its exit code first.
- **`feat/dashboard`'s `.gitignore` `.env*` hid `.env.example`,** although its README points to it. Fixed on `feat/landing-next-level` with `!.env.example`.
- **The hero scan sync, 2026-10-10.** Markers on fixed delays drifted from the plane once the scroll spread the layers.
  - The fix has three parts: fixed layer depths, `scaleZ` on the scene for the spread, and one `crossAt(z)` formula in `scan-timing.ts` that mirrors `--animate-scan-z`. Change the keyframe and that file together.
  - To verify, pause all animations at `crossAt(z)+0.25`s and check that the plane's m43 equals the layer's z, and that the markers read 1 at scroll 0, 0.5 and 1.
  - Probes that select `a[href='#report']` must scope to `main`, because the nav now links there too.
