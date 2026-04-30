---
title: "Replacing the Semantic Scholar MCP with a Skill?"
date: 2026-04-30
categories: ["Agentic AI"]
tags: ["Claude Code", "MCP", "Semantic Scholar", "Skills", "Context Engineering"]
description: "A Claude Code skill matched the Semantic Scholar MCP at 100% recall with fewer tool calls and zero context overhead. Same API, fewer layers."
math: false
draft: false
---

In the [previous post](/blog/mcp-vs-vanilla-agent/), the Semantic Scholar MCP beat a vanilla agent on a reference extraction task with 100% recall vs. 85%, 3x fewer tool calls, and zero side effects. But since everybody's buzzing how *MCP is dead, skill is all you really need,* yada yada yada... in this post I'll show is this really true. Can a skill actually do the same thing, but cheaper?

## What Changed

So, I built a `/scholar` skill. It's extremely simple: three Python scripts calling the same Semantic Scholar API, using stdlib `urllib` and running via `uv`. No async framework, no rate limiter, no circuit breaker, no nothing. The agent (with frontier model that it's using, of course) is more than capable enough to retry if a call fails.

The biggest difference from the MCP is that there is no server process. Hence, there's no persistent context cost. The skill loads only when `/scholar` is invoked and is really short:

```txt
Search, analyze, and export academic papers using the Semantic Scholar API.

Before acting, read the relevant doc for the task:

- Paper search/details/citations/references/recommendations: docs/papers.md
- Author search/details/top papers/duplicates: docs/authors.md
- BibTeX export and paper tracking: docs/export.md

Run scripts from this skill's directory: cd ~/.claude/skills/semantic-scholar && uv run scripts/<name>.py <subcommand> [args]
```

Much of it is hidden for the sake of context optimization, but the idea is that only these few tokens are available to the model at all times. The rest is on demand. Now compare that to the MCP that takes up ~7.8K token of the active context window.

Additionally, I added the `--name` flag to the author script. It searches all name variants, deduplicates papers across profiles, and returns a merged result in one call. The MCP requires a manual search-then-consolidate workflow to handle duplicate author profiles.


## Simple Experiment

Just like in the previous post: same prompt, three independent runs. The without-MCP and with-MCP runs used Opus 4.6 (from the [previous post](/blog/mcp-vs-vanilla-agent/)). The skill run ([unfortunatelly](https://www.reddit.com/r/ClaudeCode/comments/1so9uta/opus_47_is_legendarily_bad_i_cannot_believe_this/)) used Opus 4.7.

> Find the first journal paper by Ante Kapetanovic and extract all references from that paper.

## Results

| Metric | Without MCP | With MCP | With Skill |
|---|---|---|---|
| Recall | 85.3% (58/68) | 100.0% (68/68) | 100.0% (68/68) |
| Precision | 100.0% | 100.0% | 100.0% |
| Missing references | 10 | 0 | 0 |
| Tool calls (total) | 40 | 14 | 10 |
| Tool calls (failed) | 30 | 6 | 3 |
| Tool success rate | 25.0% | 57.1% | 70.0% |
| Distinct failure types | 12 | 3 | 1 |
| Assistant turns | 30 | 10 | 9 |
| Side effects on environment | 3 | 0 | 0 |

The model difference (Opus 4.6 vs. 4.7) is a confound, but all the structural advantages (zero base context cost, auto-merge, on-demand loading) are architecture-level and not model-level so it's still a fair game (considering how much worse Opus 4.7 is compared to 4.6, it's actually not fair... but in reverse).


## What Happened

I have three Semantic Scholar profiles under two name variants. The skill's `--name` flag searched all variants and merged the results in one call, returning 22 papers. The agent identified the 2021 Nonlinear Dynamics paper as the earliest journal article.

Reference retrieval hit the same Springer publisher block that tripped up the MCP. Three failed calls, all from the same root cause. The agent pivoted to Crossref and got all 68 references. Nine turns, ten tool calls, one failure type. Not that bad.


## Why It Worked

Don't know how these freaking skills are so effective, but they truly are. And with practically **zero base cost**. The MCP injects ~7.8k tokens of tool definitions into every prompt turn. The skill injects zero until invoked.

Ok, yes, I did this thing, which is not available in the MCP, and that's **author auto-merge**. The `--name` flag searches all author profiles, deduplicates papers, and returns a merged list. With the MCP, the agent had to search, spot duplicates, consolidate, and only then get details.

It's also very interesting to observe how these models are so capable that handle retry mechanism by their own. This means that I can use the **same exact API, but with fewer layers**. Skill calls the same Semantic Scholar endpoints with stdlib `urllib` instead of an async server with rate limiting, caching, and circuit breaking. 


## Tradeoffs

The MCP is a [production-grade tool](https://github.com/akapet00/semantic-scholar-mcp) with built-in rate limiting, caching, and structured error handling. The skill is a personal script with basic retry logic. For a single user running occasional queries, that works. For anything shared or high-throughput, the MCP is much better choice.

The MCP also works out of the box for any Claude Code user who installs it. The skill requires building and maintaining your own scripts.

And this is still `N=1`. Same task, same paper, same caveats as the previous post.


## Takeaway

The skill matched MCP recall with fewer tool calls and zero context overhead. For single-user workflows with domain tools you use regularly, a skill can replace an MCP server and save context budget.

Links: [previous post](/blog/mcp-vs-vanilla-agent/), [MCP repo](https://github.com/akapet00/semantic-scholar-mcp), [skill source](https://github.com/akapet00/dotclaude/tree/main/skills/scholar).
