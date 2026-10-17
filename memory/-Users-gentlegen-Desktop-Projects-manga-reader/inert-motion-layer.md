---
name: inert-motion-layer
description: Manga Orbit ships animation classes and motion tokens that compile to nothing — verify motion by compiling, not by reading JSX.
metadata:
  type: project
---

As of 2026-09-09, a large part of Manga Orbit's motion layer is written but silently inert:

- `animate-in`, `fade-in`, `slide-in-from-bottom-2/4`, `slide-in-from-top-2`, `fill-mode-both`
  are used in 4 shipping components, but `tailwindcss-animate` / `tw-animate-css` is **neither
  installed nor imported**. Those animations emit no CSS.
- `--duration-fast/base` and `--ease-standard` are defined in `:root` but never registered in
  the `@theme` block, so the bare utilities `duration-base ease-standard`
  (`components/reader/reader.tsx:1416`) compile to nothing. 13 other call sites work around it
  with `duration-[var(--duration-fast)]` arbitrary syntax.

**Why:** reading JSX makes the motion look implemented; only compiling the real `globals.css`
against the candidate class strings reveals the no-op. A reviewer who reads the diff and nods
will approve motion that does not exist.

**How to apply:** for any animation claim in this repo, compile and check the emitted CSS, or
observe it in the browser. Never accept "the class is there" as evidence. See
[[yomi-localstorage-wipe-risk]] and the full audit in `docs/next-level-plan.md`.
