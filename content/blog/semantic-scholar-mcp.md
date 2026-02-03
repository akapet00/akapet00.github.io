---
title: "Semantic Scholar MCP: Academic Research Tools for Your AI Agent"
date: 2026-02-03
categories: ["Agentic AI"]
tags: ["Claude Code", "Codex", "MCP", "Semantic Scholar", "Research Tools", "Academic Papers"]
description: "An MCP server that gives Claude full access to Semantic Scholar's API: search papers, explore citations, find authors, get recommendations, and export BibTeX."
math: false
draft: false
---

What if your favourite AI agent could search millions of academic papers, explore citation graphs, find researchers, get ML-powered paper recommendations, and export everything to BibTeX + all this without leaving the conversation?

That's what the [Semantic Scholar MCP server](https://github.com/akapet00/semantic-scholar-mcp) does.
It gives any [MCP](https://modelcontextprotocol.io) client full access to [Semantic Scholar's API](https://www.semanticscholar.org/product/api).

![Semantic Scholar MCP architecture: Claude clients connect via MCP to Semantic Scholar API](/images/blog/semantic-scholar-mcp/semantic-scholar-mcp-1.png)

## Why Not Just Use a Web-Based Alternative?

There are plenty of tools nowadays that may work great (take a look at [Google Scholar Labs](https://blog.google/products-and-platforms/products/education/google-scholar-labs/) for example). However, all those tools let you search, but one lets you *work*. Papers are tracked locally (not dumped into your conversation), so you can explore dozens of papers, go through citation networks, and export everything to BibTeX without switching tabs or hitting context limits (or waiting for hours for it to be done &mdash; I'm talking to you [Deep Research](https://openai.com/index/introducing-deep-research/)).


## Available Tools

The server exposes 13 tools organized into four categories:

**Paper Tools**
- `search_papers` &mdash; keyword search with year, citation count, and field-of-study filters
- `get_paper_details` &mdash; full metadata via Semantic Scholar ID, DOI, or ArXiv ID
- `get_paper_citations` &mdash; papers that cite a given work
- `get_paper_references` &mdash; papers that a given work cites

**Author Tools**
- `search_authors` &mdash; find researchers by name
- `get_author_details` &mdash; profile, h-index, affiliations, publications
- `get_author_top_papers` &mdash; author's most-cited work
- `find_duplicate_authors` &mdash; identify duplicate records by ORCID/DBLP
- `consolidate_authors` &mdash; preview merged author records

**Recommendations**
- `get_recommendations` &mdash; ML-based similar paper suggestions
- `get_related_papers` &mdash; find related work using positive/negative paper examples

**Session & Export**
- `list_tracked_papers` &mdash; view papers retrieved in current session
- `clear_tracked_papers` &mdash; reset session tracking
- `export_bibtex` &mdash; export tracked papers to BibTeX format


## Quick Example: Literature Review

One use case is quick-and-dirty literature reviews. Here's an example prompt to Claude Code (Opus 4.5 under the hood) on a topic from my PhD days

> Do a quick literature review on the topic: Human exposure to EMF fields above 6 GHz. Focus only on numerical studies on realistic body models. Papers from the last 10 years. Max half-page. IEEE-style references.

And here's the output:
```text
I have sufficient papers to write the literature review. Let me compile
a concise half-page review based on the key numerical studies found.

---

Literature Review:
Numerical Studies on Human Exposure to EMF Above 6 GHz Using Realistic
Body Models

The deployment of fifth-generation (5G) wireless systems operating at
millimeter-wave (mmWave) frequencies above 6 GHz has prompted extensive
numerical dosimetry research to assess human exposure. At these
frequencies, electromagnetic energy is absorbed primarily within
superficial tissues, making the skin the critical tissue for dosimetric
evaluation.

Several studies have employed the finite-difference time-domain (FDTD)
method with anatomically realistic human models to compute absorbed
power density (APD) and specific absorption rate (SAR).

Kodera et al. [1] computed whole-body average SAR from 1 to 100 GHz
using high-resolution anatomical models with fine-tuned skin thickness,
demonstrating that skin thickness significantly affects absorption at
frequencies up to 20 GHz. Morelli et al. [2] used FDTD simulations with
adult and child voxel models to evaluate 28 GHz exposure from 5G
handsets, finding that all scenarios complied with ICNIRP limits while
noting differences in SAR distribution between age groups. Comparative
studies have examined the accuracy of different modeling approaches.
Colella et al. [3] compared multilayer planar slabs with the Virtual
Population (ViP) anatomical model (Duke) at 24-28 GHz, revealing
non-negligible differences and emphasizing the need for realistic body
geometries. Kapetanović et al. [4] developed averaging techniques for
APD assessment on anatomically accurate ear models at 26 and 60 GHz,
showing that spatial maximum APD on curved surfaces can be up to 20%
larger than on flat models. An international intercomparison study by
Li et al. [5] involving 11 research groups validated computed absorbed
(epithelial) power density values at 10-90 GHz, establishing benchmarks
for dosimetry accuracy. Diao and Hirata [6] employed hybrid spherical
near-field transformation with FDTD to assess 28 GHz array antenna
exposure on stratified and anatomical partial body models, validating
results against full-wave simulations. In the recent work by Gallucci
et al. [7], it is demonstrated that skin stratification (stratum
corneum vs. homogeneous dermis) affects APD estimates by 16-30% at 28
GHz when using realistic anthropomorphic models. 

These numerical studies collectively indicate that exposure levels from
typical 5G devices remain within international safety guidelines, while
highlighting the importance of using realistic anatomical models and
proper skin layer representation for accurate dosimetry above 6 GHz.

---

References
[1] S. Kodera, K. Taguchi, Y. Diao, T. Kashiwa, and A. Hirata,
"Computation of whole-body average SAR in realistic human models from 1
to 100 GHz," IEEE Trans. Microw. Theory Tech., vol. 72, 2024.
[2] M. S. Morelli, S. Gallucci, B. Siervo, and V. Hartwig, "Numerical
analysis of electromagnetic field exposure from 5G mobile
communications at 28 GHz in adults and children users for real-world
exposure scenarios," Int. J. Environ. Res. Public Health, vol. 18, no.
3, p. 1073, 2021.
[3] M. Colella, S. Di Meo, M. Liberti, M. Pasian, and F. Apollonio,
"Advantages and disadvantages of computational dosimetry strategies in
the low mmW range: Comparison between multilayer slab and
anthropomorphic models," IEEE Trans. Microw. Theory Tech., vol. 71,
2023.
[4] A. Kapetanović, G. Sacco, D. Poljak, and M. Zhadobov,
"Area-averaged transmitted and absorbed power density on a realistic
ear model," IEEE J. Electromagn. RF Microw. Med. Biol., vol. 7, 2023.
[5] K. Li et al., "Calculated epithelial/absorbed power density for
exposure from antennas at 10–90 GHz: Intercomparison study using a
planar skin model," IEEE Access, vol. 11, pp. 11586–11600, 2023.
[6] Y. Diao and A. Hirata, "Exposure assessment of array antennas at 28
GHz using hybrid spherical near-field transformation and FDTD method,"
IEEE Trans. Electromagn. Compat., vol. 63, no. 5, pp. 1549–1558 2021.
[7] S. Gallucci et al., "Impact of anthropomorphic shape and skin
stratification on absorbed power density in mmWaves exposure
scenarios," Sensors, vol. 25, 2025.
```

Claude searched for relevant papers, filtered by year, and produced a half-page summary with seven properly formatted references, all in one shot. It even found my own paper [4], so, yeah, I'm calling this a success.

But literature reviews are just one application. You can also use it to explore citation networks ("what papers cite this one?"), look up specific authors and their most influental work, find related work based on papers you already like, or just quickly grab metadata for a paper you're citing.


## Setup

**Claude Code** (one command):

```bash
claude mcp add semantic-scholar -s user -- uvx --from git+https://github.com/akapet00/semantic-scholar-mcp semantic-scholar-mcp
```

**Claude Desktop** (add to `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/akapet00/semantic-scholar-mcp",
        "semantic-scholar-mcp"
      ]
    }
  }
}
```

**API key** (optional but recommended for heavy use): Without a key, you share a pool of 5,000 requests per 5 minutes with other unauthenticated users. With a key, you get a dedicated 1 req/sec rate limit. Get one free at [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api).


## Under the Hood

**Client-side session tracking.** Papers are tracked locally by the MCP server, not in the conversation context. You can retrieve dozens of papers without bloating your context window, then export them all at once.

**Production-grade reliability.** The server includes caching (15-minute TTL), rate limiting, circuit breaker patterns, and retry logic with exponential backoff.

**Works with any MCP client.** Claude Desktop, Claude Code, VS Code with the Claude extension, Cursor, really anything that supports MCP can use this server.


## Disclaimer

This is an experimental, open-source tool. It may have bugs, and results depend on Semantic Scholar's API availability and data coverage.

This project is not affiliated with, endorsed by, or sponsored by Semantic Scholar or the Allen Institute for AI. It simply uses their public API.

The code is open and available at [github.com/akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp). Contributions welcome.
