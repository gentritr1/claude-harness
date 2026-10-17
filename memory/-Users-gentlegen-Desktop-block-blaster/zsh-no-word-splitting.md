---
name: zsh-no-word-splitting
description: "The shell here is zsh — unquoted $VAR does NOT word-split, so `for f in $FILES` silently passes the whole list as one argument"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T19:12:06.241Z
---

2026-07-27 on Blockrow: a bulk rename written as

```sh
FILES=$(grep -ril rowflare .)
for f in $FILES; do sed -i '' 's/a/b/g' "$f"; done
```

did **nothing**. In bash this word-splits on newlines; in **zsh it does not**, so
`sed` received all 30 filenames concatenated as a single path and failed with one
`No such file or directory`. The error was easy to skim past because it printed
the whole file list and looked like successful output.

**Why:** zsh omits the SH_WORD_SPLIT option by default. This environment's shell
is zsh (see the platform block), so bash idioms copied from habit fail silently
or near-silently.

**How to apply:** For multi-file loops, pipe into `while IFS= read -r f`, or use
`grep -l ... | xargs sed -i ''`, rather than `for f in $VAR`. After any bulk edit,
**re-grep for the old string** and assert zero hits instead of trusting the loop's
own output — that is what caught it here.
