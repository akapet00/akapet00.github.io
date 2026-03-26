# DevDays 2026 — Session Summary

## Presentation

**Title:** Context Engineering: From Zero to Hero
**File:** `index.html` (Reveal.js, single file)
**Slides:** 66
**Target:** 15-17 min speaking + 10 min Q&A
**Pace:** 10-15s per slide
**References:** `references.txt` (28 refs with URLs, separate from slides)

---

## Style Guide

All new and existing slides must follow these rules:

- **all lowercase** for headings (`<h1>`, `<h2>`, `<h3>`) — no capitalization except proper nouns (GPT, CRS, MCP) and filenames (CLAUDE.md, AGENTS.md)
- **no terminal punctuation** — no periods on slide text, question marks and commas are ok
- **bullet points appear one by one** using `class="fragment" data-fragment-index="N"` — title shows first, then each bullet sequentially
- **simplicity** — plain text over boxes, bars, flow diagrams. no grey helper text. direct statements.
- **footnotes** — uniform format: `Author, "Full Title", source, year`. Always wrapped in `<div class="footnote"><p>...</p></div>`. No numbering. Pinned to bottom of slide via CSS.
- **speaker notes** — conversational, short sentences, timing at end (e.g., `15s`)
- **emphasis (two-tier system):**
  - **orange bold** (`<span class="orange" style="font-weight:700;">`) for labels/terms at start of a bullet
  - **`<strong>`** for mid-sentence emphasis
  - never use uppercase for emphasis (exception: `HOW` on slide 15)
- **code/filenames** in `<code>` tags
- **Infobip palette only:** orange `#FF6600`, dark blue `#1A1A2E`, grey `#999`
- **no memes full screen** — keep them small if used (exception: Emanuel reveal on CRS closing slide)
- **no TED talk hooks** — casual, conversational tone
- **Reveal.js config:** `center: false`, sections use flexbox for centering. Progress bar is a flex item (not absolute positioned).

---

## Current Section Structure

### S1: Hook (slides 1-5)
Title, relatable scenario (greentext), "You're absolutely right." punchline (large, centered, outside greentext container), context rot reveal, transition to capabilities.
**Status:** done.

### S2: LLM Capabilities (slides 6-12b)
Benchmark data (intelligence, agentic, coding indexes from Artificial Analysis), open-weight models (Qwen 3.5), local performance. Concludes: what determines performance is the context.
**Status:** done.

### S3: Context Engineering (slides 13-16)
Three definitions (Anthropic, Elastic, Chroma), HOW > WHAT, "context engineering is the art of avoiding context rot."
**Status:** done.

### S4: AI-Era Timeline (slides 17-26) + Context Window Anatomy
Seven-stage timeline (text prediction → persistent agents), inflection point at tool use. Then: "what fills a context window?" (fragment bullets). Followed by standalone: "the window is finite and expensive, and it fills fast."
**Status:** done.

### S5: Context Rot (slides ~28-40)
Chroma's 7 stages of context degradation with figures. Chroma hero plot inserted right after Stage 4 (the dumb zone). Concludes: more context ≠ better results → better context = better results.
**Status:** done.

### S6: Solutions (slides ~41-56)
Section header. Then:
- **Early restart** — 4 fragment bullets (kill before dumb zone, ~40% utilization, one task one session, cheapest technique)
- **Intentional compaction** — 4 fragment bullets (auto-compaction is blind, agent writes but you decide, steer what survives, `/compact` with explicit instructions)
- **Spec-driven development** — 4 fragment bullets (spec before code, spec as contract, explicit/bounded requirements, fresh window per spec). Boeckeler reference.
- **RPI (research, plan, implement)** — 4 fragment bullets (each phase with fresh window, human reviews at every boundary). Horthy + ACE-FCA references.
- **Context optimization** — 4 fragment bullets with orange labels (remove, add, trim, target 40-60%). Horthy + ACE-FCA references.
- **Ralph loops** — code snippet + 4 fragment bullets (plan first, atomic tasks, run the loop, track in files & git). Ralph Wiggum images appear at each bullet (2 left, 2 right, rotated).
- **GSD** — file pills (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md) + 4 fragment bullets (state in files, XML plans, fresh window per wave, crash/restart/resume).
- **Full autonomy** — 3 fragment bullets (Gas Town, OpenClaw, human out of the loop).
- **Why I didn't go there** — 4 fragment bullets. Lead: researcher loses ownership of idea/hypothesis/execution. Then: can't track code, security concerns, ralph + sandboxing = controlled autonomy.
- **Planner → Generator → Evaluator** — flow diagram + 4 fragment bullets (self-eval bias, GAN-inspired, Playwright testing, solo vs harness cost). Rajasekaran 2026 + Building Effective Agents 2024.
**Status:** done.

### S7: Proof — Agentic CRS (slides ~57-66)
- **Section header** — progress bar, clean.
- **The problem** — 4 fragment bullets (real POC for taw9eel.com, multi-agent bilingual RAG, scope breakdown, cannot be solved in one session). Emanuel backstory in notes.
- **Architecture** — improved diagram: greeting fast-path + orchestrator top row, elicitor/searcher/reranker/selector bottom row (no connector lines), tech stack pills. Two explanation lines below.
- **Built in 3 phases** — 3 wider phase cards (ralph loop × 2, manual RPI), lowercase black text. Two lines below about fresh context and human review.
- **Conversation flow** — 6-step fragment demo (hello → greeter no-LLM → vague request → elicitor with Eid/cultural awareness → user details → searcher → reranker → diversity selector → top 5). Confluence reference.
- **Patterns and guardrails** — 4 fragment bullets with orange labels (protocol abstraction, DI, guardrails including off-topic refusal/bounded elicitor/rerank fallback, caching).
- **Emanuel approves** — 3 fragment bullets then Emanuel image covers the entire slide on 4th click.
**Status:** done.

### S8: Playbook (slides ~67-end, 7 slides)
Section header. Then:
- **Agent hygiene** — merged CLAUDE.md + session hygiene: /init then subtract, positive instructions, one task one session, track in files. Fragment bullets. Pocock + Mohsenimofidi references.
- **Subtract** — merged AGENTS.md data + compaction priority: 20% stat, caveat, compaction order (incorrect → missing → noisy), "less instruction = more autonomy". Fragment bullets. Gloaguen + HumanLayer references.
- **Test oracles** — tests as contract, write before implementation. Fragment bullets. Anthropic harness design reference.
- **State of the art** — merged what's next + research horizon: RLM (automated CE via sub-LLM calls) + TTT-E2E (context compressed into weights). Framed as automated CE techniques. Fragment bullets with orange labels. "until these ship, context engineering is your edge." Zhang + Tandon references.
- **Three takeaways** — fragment bullets with orange numbered markers: (1) CE is #1 AI-era skill, (2) LLMs stateless: input = output quality, (3) structure > volume.
- **Thank you** — QR code linking to GitHub repo with references and README.
**Status:** done.

---

## Key Decisions Made

1. **Removed "Vibe Coding vs Context Engineering" section** — the distinction is implicit throughout.
2. **Context window anatomy collapsed to 1 slide + 1 punchline** — plain text with fragment bullets, no diagrams.
3. **Chroma hero plot moved after Stage 4 (dumb zone)** — data lands harder right after the failure mode.
4. **Spec-driven dev separated from RPI** — Boeckeler reference for spec-driven dev, Horthy/ACE-FCA for RPI.
5. **Solutions slides simplified** — all use fragment bullet points, consistent content density.
6. **Progress bar changed from absolute to flex** — `center: false` in Reveal config, sections use flexbox. Progress bar and labels are flex items, not absolute positioned.
7. **"best practices" renamed to "playbook"** — reflects expanded scope.
8. **Harness + generator-evaluator merged** — single planner → generator → evaluator slide with Rajasekaran 2026 reference.
9. **Harness patterns slide cut** — concepts covered in playbook section.
10. **"Not a bigger model / Better structure" slide cut** — Emanuel slide closes the section.
11. **CRS section restructured** — first 3 slides merged into section header + problem slide. Architecture diagram improved. Demo shows full flow with greeter fast-path. Guardrails highlighted.
12. **References moved to `references.txt`** — removed from thank you slide, 28 refs with full URLs in separate file.
13. **Footnote format normalized** — all use `Author, "Full Title", source, year` in `<p>` tags, no numbering.
14. **Emphasis two-tier system** — orange bold for labels at start of bullets, `<strong>` for mid-sentence.
15. **Figures flattened** — all in `figures/` root, no subfolders, shorter names.
16. **Author corrections** — Ghazal → Gloaguen, Fowler → Boeckeler, Horthy dated 2026, Anthropic harness posts dated 2026.
17. **Playbook section cut from 13 to 7 slides** — merged CLAUDE.md + session hygiene, AGENTS.md data + compaction priority, what's next + research horizon. Cut: my CLAUDE.md, claude code as harness. All slides use fragment bullets, no gray text, no def-stack boxes.
18. **Thank you slide uses QR code** — links to GitHub repo with references.txt and README.md.
19. **Hosted on GitHub Pages** — `static/devdays2026/` in akapet00.github.io, accessible at antekapetanovic.com/devdays2026/.

---

## Figures

All in `figures/`, flat structure. No subfolders.

- `bench-intelligence.png` — Artificial Analysis intelligence index
- `bench-agentic.png` — Artificial Analysis agentic index
- `bench-coding.png` — Artificial Analysis coding index
- `bench-huggingface.png` — Chaumond/HF Qwen 3.5 post
- `bench-qwen-local.png` — local Qwen benchmark results
- `rot-stage-1.png` through `rot-stage-7.png` — Chroma context rot stages
- `chroma-hero-plot.png` — performance degradation chart
- `ralph.webp` — Ralph Wiggum
- `emanuel.png` — Emanuel approves
- `qr-code.png` — QR code to GitHub repo with references

---

## References

28 references with full URLs stored in `references.txt`. Key corrections from this session:
- Ghazal → **Gloaguen** et al. (ETH Zurich)
- Fowler → **Boeckeler** (actual author, martinfowler.com, 2026)
- Horthy Heavybit article dated **2026** (not 2025)
- Anthropic harness posts split: Young (Nov 2025) + Rajasekaran (Mar 2026)
- Scientific computing post dated **2026** (Mishra-Sharma)
- Zhang et al. (MIT CSAIL) for RLM, not Prime Intellect
- Tandon et al. (Stanford/Berkeley/NVIDIA) for TTT, not just NVIDIA
- Added: Kapetanovic, "Agentic CRS Prototype", Infobip Confluence, 2026
