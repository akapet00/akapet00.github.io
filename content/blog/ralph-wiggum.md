---
title: "Ralph Wiggum: Running Coding Agents in Autonomous Loops"
date: 2026-01-15
categories: ["Agentic AI"]
tags: ["Claude Code", "Autonomous Agents", "LLM", "Context Engineering", "Refactoring", "DevTools"]
description: "A practical guide to running coding agents in autonomous loops using the Ralph Wiggum technique. Learn how to set up sandboxing, write PRDs, and let your agent iterate until tasks are complete."
math: false
draft: false
---

The overarching idea of AI (or, more ambitiously, AGI) is to perform work autonomously on the user's behalf.

Yet, most current state-of-the-art coding agents just introduce an additional layer of abstraction rather than fundamentally changing how software is produced.

This means that, in practice, we have shifted from writing code like this:

```python
def compute_monthly_revenue(transactions: list[dict]) -> float:
    return sum(t["price"] * t["quantity"] for t in transactions)
```

to issuing prompts such as:

> Write me a function that computes monthly revenue from a list of transactions.

Conceptually, this is not that radical a departure. It mirrors the historical transition from low-level languages to higher-level procedural languages. We replaced assembly with C, then C with Python, and now Python with natural language. Each step raises the level of abstraction, but the underlying mental model remains the same: the human specifies how the work should be done, but in a more concise or expressive form.

This pattern has repeated often enough that it has given rise to a familiar trope: "real programmers" do not rely on abstractions. A classic example of this sentiment can be found in the satirical article titled [Real Programmers Don't Use PASCAL](https://homepages.inf.ed.ac.uk/rni/papers/realprg.html). History has consistently shown this belief to be misguided as it often turns out that abstractions are precisely what enable leverage and scale.

However, the true value proposition of AI is *not* that it acts as a highly knowledgeable code companion that answers your questions well, but has the memory of a goldfish. Such a system still requires us, the user, to micromanage intent, design, and execution. The real breakthrough would be an AI operating at a [J.A.R.V.I.S.](https://en.wikipedia.org/wiki/J.A.R.V.I.S.)-level of competence. It should understand *what* needs to be done, *why* it matters, *how* it should be approached, and *when* it should be executed after receiving a clear, but very high-level instruction.

We are still far away from this, but the Ralph Wiggum technique, a not-so-new-but-recently-very-hyped paradigm for agentic coding, could be a step toward that vision.

## But What is Ralph Wiggum?

If you have ever watched The Simpsons, then you must remember Ralph.

![Ralph Wiggum](/images/blog/ralph-wiggum.jpg)

Ralph Wiggum is a [well-meaning boy who suffers from either severe learning and social disabilities, and/or some other form of childhood psychiatric disorder](https://simpsons.fandom.com/wiki/Ralph_Wiggum). He is perpetually confused but *extremely persistent*.

This extreme persistence motivated the creator of the Ralph Wiggum technique, Geoffrey Huntley, to run a coding agent in a continuous and fully autonomous loop. Geoffrey described Ralph as, [in its purest form, just a bash loop](https://ghuntley.com/ralph/). It solves the common problem of agents finishing too early by forcing them to keep working and checking until the task is truly complete.

Ralph works great for tasks that are long running, for projects where you are sure that you know what you're building, and for tasks that benefit from continuous iteration without a human in the loop.

This means that Ralph is not ideal for exploratory work where the main evaluator still has to be a human. Also for small tasks that are easily one-shotted and fit the context fairly easily, far away from the "[dumb zone](https://www.youtube.com/watch?v=rmvDxxNubIg)"—the performance degradation that tends to occur at or around 40% of context usage, where models start to lose coherence.

But let's see how Ralph works in practice.

## Running Ralph

I decided to try out Ralph on something that is fairly common to all of us and that pretty much nobody likes to do: *refactoring* and *testing*. No matter what type of code you write, you still have to do your due diligence and keep your code [decoupled](https://goodresearch.dev/decoupled), [tested](https://goodresearch.dev/testing), and [well documented](https://goodresearch.dev/docs).

### Step 1. Enable Sandboxing

This is critical, but very little talked about.

The very idea is to leave Ralph (remember that it is just a simple way of looping your coding agent until all the tasks are done) to cook without your constant input. This means that if you have to manually intervene to give permission prompts—the whole purpose of Ralph falls through.

There are two ways to go about it.

First, if you want to go full YOLO, you can run any agent (let's use Claude Code as an example) with the [`--dangerously-skip-permissions`](https://docs.anthropic.com/en/docs/claude-code/cli-reference#cli-flags) flag and pray.

What you actually should do to avoid [`rm -rf ~`](https://old.reddit.com/r/ClaudeAI/comments/1pgxckk/claude_cli_deleted_my_entire_home_directory_wiped/) is to create `.claude/settings.json` in your project with configuration that you'll adjust to yourself. Here's mine:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false,
    "network": {
      "allowLocalBinding": true
    }
  },
  "permissions": {
    "allow": [
      "Bash(uv:*)",
      "Bash(uvx:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "Glob(*)",
      "Grep(*)"
    ]
  }
}
```

Simple yet effective.

### Step 2. Write a Product Requirements Document

Now, you have to flesh out your idea and start with a comprehensive product requirements document (PRD).

What I did is just started to talk to an instance of Claude Code and used a skill I wrote specifically for writing PRDs. I got the inspiration for this from [Ryan Carson's guide to Ralph](https://x.com/ryancarson/status/1879228371712135632) and [his version of the PRD skill](https://github.com/snarktank/ralph/blob/main/skills/prd/SKILL.md). In a nutshell, the PRD should present a blueprint defining what a product or feature should do, its purpose, target users, and goals, serving as a central guide for development, design, and stakeholders, focusing on user needs rather than implementation.

After a lot of back and forth, it took around 39% of the context window available with Claude Opus (roughly 80k tokens out of ~200k) to complete the PRD for the task of refactoring a part of my codebase.

This means that just the process of brainstorming and writing the PRD led me to the brink of the dumb zone...

### Step 3. Convert PRD to User Stories

Based on [Anthropic's effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), you should structure your plan with tasks that can be marked as passing/failing.

Again, I ran a fresh instance of Claude Code and used a skill for this specific purpose.

After a bit less back and forth compared to step 2, Claude created the plan with 7 tasks decomposed from the PRD. This all took around 12% of the available context.

The plan is a simple markdown file with user stories written in JSON format. Here's an example of a user story:

```json
{
  "category": "refactor",
  "id": "US-4",
  "title": "Merge experiment modules",
  "description": "As a developer, I want all experiment orchestration in one module so that I maintain one set of experiment running logic",
  "steps": [
    "Create `_create_error_dataframe()` helper in experiment.py for error DataFrame creation",
    "Create `_sanitize_and_save_results()` helper for DataFrame processing and saving with CSV fallback",
    "Move `run_multimodal_experiment_async()` from experiment_multimodal.py to experiment.py",
    "Move `run_multimodal_multi_task_experiment_async()` from experiment_multimodal.py to experiment.py",
    "Move `run_multimodal_multi_task_experiment()` from experiment_multimodal.py to experiment.py",
    "Move `get_models_for_modality()` from experiment_multimodal.py to experiment.py",
    "Delete experiment_multimodal.py",
    "Add type hints where applicable",
    "All tests pass"
  ],
  "passes": true
}
```

### Step 4. Create an Activity Log for Progress Tracking

Since you have to run a coding agent headless, I created an activity log file. This file logs what the agent accomplishes during each iteration and it looks something like this:

```markdown
# Project Build - Activity Log

## Current Status

**Last Updated:** ...

**Tasks Completed:** ...

**Current Task:** ...

---

## Session Log

<!-- Agent will append dated entries here -->
```

This is in line with what [Anthropic suggests](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) for long-running agents:

> When experimenting internally, we addressed these problems using a two-part solution:
>
> 1. Initializer agent: The very first agent session uses a specialized prompt that asks the model to set up the initial environment: an `init.sh` script, a **claude-progress.txt** file that keeps a log of what agents have done, and an initial git commit that shows what files were added.
> 2. Coding agent: Every subsequent session asks the model to make incremental progress, then leave structured updates.
>
> The key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the **claude-progress.txt** file alongside the git history. Inspiration for these practices came from knowing what effective software engineers do every day.

In my case, I don't want to give away too much info to other agents to avoid context pollution—I just want agents to know what was done previously and what to do next. However, it is good to have some kind of log to be able to track any errors that may occur.

## Is Ralph Expensive?

Well, it could be. But since the core idea of Ralph is to use as little of the context window as possible to solve each task, it shouldn't be. Namely, with specs written well enough—which means writing an elaborate PRD and decomposing it into a number of user stories that fit at most 1 context window—costs should be under control. If you set max number of iterations `N` to solve `N` tasks, a rough estimate for the upper bound on costs is:

```
cost = N * (input_tokens * input_price + output_tokens * output_price)
```

Keep in mind that output tokens are typically 5x more expensive than input tokens. For Claude Opus, that's roughly $15 per million input tokens and $75 per million output tokens. A single iteration that fills the context might cost $3-5, so 10 iterations could run $30-50.

Is that a lot? Depends on who you ask I guess...

And yes, it could happen that 1 task needs more than 1 context window, but this is on you.

### Step 5. Let Ralph Ralph

Remember that Ralph is just a loop?

Then just let Ralph do its thing with a very simple bash command:

```bash
while :; do cat PROMPT.md | claude --print ; done
```

The `--print` flag runs Claude Code in non-interactive mode, which is essential for headless operation. To stop the loop when all tasks are complete, you can either hit `Ctrl+C` manually, or wrap it with a check:

```bash
for i in {1..10}; do
  output=$(cat PROMPT.md | claude --print)
  echo "$output"
  if echo "$output" | grep -q "<promise>COMPLETE</promise>"; then
    echo "All tasks completed!"
    break
  fi
done
```

This version also caps iterations at 10 to prevent runaway costs.

Oh yes, you do have to have your input prompt. Mine was very simple (note that `@filename` is Claude Code's syntax for referencing files):

```markdown
Analyze the @PLAN.md and read @ACTIVITY.md to fill the context.

Your task is to refactor the @src/ codebase by keeping the best coding practices, following DRY principle, using high-quality docstrings and types extensively.

Avoid overengineering - write your code as simple as possible, but not simpler!

**Steps:**
  - Open @PLAN.md and choose the single highest priority task where the `passes` flag is set to "false". If multiple tasks have the same priority, start in the order they are written.
  - Work on exactly ONE task and implement the needed changes.
  - Append a dated progress entry to @ACTIVITY.md at the bottom of the file.
  - Update that task's `passes` flag in PLAN.md from "false" to "true".
  - Make one git commit for that task only with a clear message, make sure to note that the commit is made by you, e.g., set [RALPH] at the beginning of the commit message
  - Do NOT git init, do NOT change remotes, do NOT push.

**Important:** Work on ONE task and ONE task only!

Only when ALL tasks have passes set to true, output <promise>COMPLETE</promise>.
```

Overall, it ran for about half an hour and refactored my codebase successfully in 7 iterations!

## A Note on the Claude Code Plugin

There is also an [official Claude Code plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) available that after installation enables Ralph out of the box. It turns out, however, that the [loop doesn't work as intended](https://www.reddit.com/r/ClaudeCode/comments/1lc4vg0/trust_me_bro_most_people_are_running_ralph_wiggum/):

> The official Claude Code Ralph plugin misses the point because it runs everything in a single context window and is triggered by a stop hook, yet the stop hook isn't even triggered at compaction. That means as tasks pile up, your context gets more bloated, more hallucinations, and I had to stop and manually compact mid-run anyway.
>
> The original bash loop (from Geoffrey Huntley) starts a fresh context window each iteration. That's a fundamental difference and IMHO the bash loop is way better for actual long-running tasks (but since it runs headless, it can be a bit more difficult to set up/understand what's going on).

Also check out [this guide](https://github.com/JeredBlu/guides/blob/main/Ralph_Wiggum_Guide.md) by Jered Blumenfeld where he shows how the plugin is inferior to the original and much simpler Ralph technique.

## Criticism

There are [a few critics](https://www.reddit.com/r/ClaudeCode/comments/1l91bwp/comment/lyrt55m/):

> Ralph repeatedly runs the same prompt against the same model while deliberately discarding all prior cognition. No policy changes, no new constraints, no learning signal, no structured negative memory. The only thing that changes between iterations is whatever happened to get written to disk; or sampling noise.
>
> That means the loop is not "iterative learning," it's stateless resampling. In January 2025, this is the opposite of what should be done. Modern frontier models already self-correct, reconsider hypotheses, and abandon prior reasoning within a single context, when instructed. Resetting cognition does not prevent lock-in anymore; it throws away useful abstractions, invariants, and failed path knowledge, forcing the model to rediscover them. If you erase cognition without enforcing hard constraints or negative knowledge, you guarantee repetition. That's not exactly determinism; but, repeatable inefficiency.
>
> Resetting cognition is only defensible when: the external world state is untrusted, or a new constraint/objective is introduced. Ralph does neither. It just presses replay.
>
> Bottom line: Running the same prompt while making the model forget is not disciplined—it's just re-rolling. Determinism without memory is just wasted compute.

And even though this critique is fairly elaborate, it misses the point. The point is that Ralph wasn't really known for being intelligent. Persistent—yes, but intelligent... not his thing.

This means that running the same prompt over and over isn't a limitation per se. You can instruct it to use particular files for task lists, planning, and executing specs to ensure it's ready to move onto the next phase. The best approach is to spend time developing a plan and breaking it down into small tasks (user stories) you would give a junior engineer (your own Ralph) and let them do their thing.

## Key Takeaways

- Always use sandbox for safety
- Always set max iterations to have the cost under control
- Plan thoroughly before running Ralph
- Use the bash loop for true iteration separation; don't use the Claude Code plugin
- Give feedback mechanisms so the agent can verify its work, but don't let agents share too much information otherwise
- Monitor the activity and use git commits to track progress wisely

## Outro

Let's wrap up with Ralph's creator's beautiful description of Ralph:

> The beauty of Ralph is that it is deterministically bad in an undeterministic world.

---

*Note: I wrote this article myself, not an LLM. So if you see em dashes here and there—that's how I roll ¯\(ツ)/¯*
