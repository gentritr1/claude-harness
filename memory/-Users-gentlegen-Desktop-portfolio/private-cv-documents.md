---
name: private-cv-documents
description: The portfolio repo is PUBLIC; the reference letter lives in cv/ but is excluded locally and never committed. CV PDF is printed from HTML with headless Chrome.
metadata:
  node_type: memory
  type: project
  originSessionId: 8eaeb68c-6838-434f-85c9-73a8e9e0c2b5
  modified: 2026-10-13T22:23:09.800Z
---

The repo gentritr1/portfolio is PUBLIC (checked 2026-10-14). Anything in `public/` ships with the site.

- `cv/Gentrit-Rashiti-Reference-Letter.{html,pdf}` is a draft for Vianova to sign. It is listed in `.git/info/exclude` and must never be committed or copied to `public/`.
- `public/Gentrit-Rashiti-CV.pdf` is printed from `cv/Gentrit-Rashiti-CV.html` with `"Google Chrome" --headless=new --no-pdf-header-footer --print-to-pdf=...`. Check that it stays 1 page and that the bottom margin survives (render it with `qlmanage -t`).
- On 2026-10-14 a merge conflict in the CV was settled by keeping the rewrite on the branch and adding main's facts: 41 components, the coaching app, AvahiTech as frontend only (no FastAPI), and Node.js, PostgreSQL and MongoDB.

**Why:** a signed reference letter in a public repo would leak a private document. When the CV conflicts, the facts the owner corrected on main beat older wording.
**How to apply:** after any CV edit, re-print the PDF and check the page count. Never stage files from the cv/ reference letter.
