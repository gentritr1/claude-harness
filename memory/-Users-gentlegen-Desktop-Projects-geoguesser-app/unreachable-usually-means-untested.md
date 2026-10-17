---
name: unreachable-usually-means-untested
description: "\"Unreachable\", \"redundant\", \"unobservable\" have meant \"untested\" every time they were checked on feat/next-level"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-02T03:39:22.234Z
---

Each time someone on feat/next-level — controller or implementer — said a piece of code could not or need not be
tested, checking it proved otherwise:

- **R107 (me, wrong twice):** I called two generation guards redundant because deleting them left the suite green. Both
  were load-bearing — one stranded the store in `loading`, the other let a dead game's hint clear a live game's flag.
- **M19 (B2-3):** "unobservable by construction" — reachable through `setState`, exactly as F6 reaches its own guard.
- **B2-4:** ten wiring sites called "unit-unreachable". A 20-line source-scan test killed all ten; one (mutant F)
  silently undid the deliberate "back is consumed until the screen changes" behaviour.

**Why:** "the suite stays green when I delete it" is evidence about the suite, not about the code. The claim is
comfortable to make because it ends the work, and nothing pushes back on it until a reviewer mutates the line.

**How to apply:**
- Treat "unreachable", "redundant", "unobservable" and "device-only" as findings to verify, not conclusions. Mutate the
  line and show a test fails, or construct the interleaving that reaches it.
- When something genuinely needs a device, pin what *is* reachable without one: move the logic into a pure factory and
  unit-test it, and pin one-line wiring with a source scan (`compact-layout.test.ts` is the precedent).
- 2026-10-04, D2-4: "the generation check after the pre-flight await is unreachable (graphFetch settles a cancel first)" — disproved by bumping the generation 2-3 microtasks AFTER the fetch body resolved (resetGame/startGame), so the fetch returns ok and only that check stops a 0-round trip. Probe the microtask window after a successful await, not only the cancel path.
- Reaching a generation guard needs an `AbortController` whose `abort()` does nothing — a deaf fetch is not enough.

Related: [[every-gate-we-write-ships-a-silent-pass]], [[a-min-over-a-sampled-matrix-is-an-artefact]].
