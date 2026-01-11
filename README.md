# antekapetanovic.com

Personal website built with [Hugo](https://gohugo.io/).

## Prerequisites

- [Hugo](https://gohugo.io/) (extended edition)
- [uv](https://github.com/astral-sh/uv) (for Python scripts)

```bash
brew install hugo uv
```

## Local Development

```bash
hugo server        # Start dev server at localhost:1313
hugo server -D     # Include draft content
```

## Adding Content

```bash
hugo new blog/my-post.md        # Create blog post
hugo new projects/my-project.md # Create project
```

Set `draft: false` in frontmatter to publish.

## Publications

Edit `bibtex/publications.bib`, then regenerate JSON:

```bash
uv run python scripts/parse_bibtex.py
```

## Features

- Dark/light theme with system preference detection
- KaTeX math rendering (enable with `math: true` in frontmatter)
- Responsive mobile-first design
- Privacy-friendly analytics (GoatCounter)
- BibTeX to JSON publication parsing

## Analytics

Privacy-friendly analytics via [GoatCounter](https://www.goatcounter.com/) — no cookies, GDPR-compliant.

- Dashboard: https://antekapetanovic.goatcounter.com

## Deployment

Pushes to `main` trigger GitHub Actions to build and deploy to GitHub Pages.

## License

MIT
