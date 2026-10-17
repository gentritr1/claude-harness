---
name: reddit-access-recipe
description: How to read Reddit from this machine when reddit.com JSON/WebFetch/WebSearch are blocked (Arctic Shift listings + local grep, live RSS for confirmation)
metadata:
  type: reference
---

Verified 2026-09-30. reddit.com `.json` returns 403, WebFetch/WebSearch refuse the domain, the in-app browser blocks it.

What works:
- **Arctic Shift archive** `https://arctic-shift.photon-reddit.com/api/` — plain listings are fast and near-real-time:
  `posts/search?subreddit=X&limit=100&sort=desc&before=<epoch>&fields=id,title,selftext,created_utc,score,num_comments`
  (paginate with `before=` = oldest `created_utc`), `posts/ids?ids=`, `comments/search?link_id=<id>&limit=100`,
  `subreddits/search?subreddit=X` (subscriber count is stale). About one call per second is tolerated.
- **Full-text search (`query=`, `title=`) is refused under load** (HTTP 422 "Timeout. Maybe slow down a bit").
  Download the most recent N posts of a subreddit and grep locally instead; this also gives honest "k of n posts, date range" counts.
- **Live Reddit RSS** `https://www.reddit.com/r/<sub>/comments/<id>/.rss` confirms a thread on live Reddit, but only about one call per 45 s.
- Stored scores/comment counts are early snapshots (often too low): count the comment list instead.

A working tool (`reddit.py`: posts/stats/dump/post/comments/sub/live, machine-wide lock, disk cache) was written in the
idea-research session's `research_notes/Indie app ideas build plan/tools/`; its cache and subreddit copies live in `~/.cache/indie-research/`.
Related: [[research-fanout-scars]]
