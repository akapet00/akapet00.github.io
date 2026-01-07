# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Commands

```bash
# Start local server
hugo server

# Build for production
hugo --minify

# Update publications (after editing bibtex/publications.bib)
uv run python scripts/parse_bibtex.py
```

## Structure

```
content/           # Markdown content (homepage, about, blog posts, projects)
layouts/           # Hugo templates
assets/css/        # Stylesheet
bibtex/            # BibTeX source file
data/              # Generated publications.json (do not edit)
scripts/           # BibTeX parser script
static/            # Static files (favicon)
```

## Key Patterns

- **Theming**: CSS variables in `assets/css/main.css`, toggled via `data-theme` attribute
- **Math**: Add `math: true` to frontmatter to enable KaTeX
- **Publications**: Edit `bibtex/publications.bib`, run parser script to regenerate JSON
- **Homepage data**: Experience timeline is defined in `content/_index.md` frontmatter

## Adding Content

```bash
hugo new blog/my-post.md
hugo new projects/my-project.md
```
