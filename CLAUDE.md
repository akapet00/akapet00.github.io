# CLAUDE.md

Guidance for Claude Code when working on antekapetanovic.com.

## Quick Commands

```bash
hugo server              # Start local dev server at localhost:1313
hugo --minify            # Build for production
uv run python scripts/parse_bibtex.py   # Regenerate publications.json from BibTeX
hugo new blog/my-post.md                # Create new blog post
hugo new projects/my-project.md         # Create new project
```

## Project Structure

```
├── .github/workflows/deploy.yml   # GitHub Actions: builds & deploys on push to main
├── archetypes/                    # Templates for `hugo new` command
│   ├── blog.md                    # Blog post template
│   └── project.md                 # Project template
├── assets/css/main.css            # Single stylesheet with CSS variables
├── bibtex/publications.bib        # BibTeX source (edit this)
├── config.toml                    # Hugo configuration
├── content/
│   ├── _index.md                  # Homepage (has experience data in frontmatter)
│   ├── about.md                   # About page
│   ├── blog/                      # Blog posts
│   ├── projects/                  # Project pages
│   └── publications/_index.md     # Publications listing page
├── data/publications.json         # Generated from BibTeX (gitignored)
├── layouts/
│   ├── _default/                  # Base templates
│   ├── blog/                      # Blog-specific templates
│   ├── projects/                  # Project-specific templates
│   ├── publications/              # Publications list template
│   ├── index.html                 # Homepage template
│   └── partials/                  # Reusable components
├── scripts/parse_bibtex.py        # BibTeX to JSON converter
└── static/favicon.svg             # Lambda (λ) favicon
```

## Architecture

### Theming
- CSS variables defined in `:root` (light) and `[data-theme="dark"]` (dark)
- Theme toggle in `partials/theme-toggle.html`
- Theme preference saved to localStorage, respects system preference
- No flash of wrong theme (script in `<head>` sets theme before render)

### Navigation
- Menu items defined in `config.toml` under `[menu]`
- First 2 items (Home, About) always visible on mobile
- Items 3+ (Blog, Projects, Publications) collapse into hamburger menu on mobile
- Hamburger transforms to X with CSS animation

### Math Rendering
- KaTeX loaded conditionally when `math: true` in frontmatter
- Supports `$...$` (inline) and `$$...$$` (block)
- Goldmark passthrough extension enabled in config.toml

### Publications
- Source: `bibtex/publications.bib`
- Parsed to: `data/publications.json` (gitignored)
- GitHub Actions runs parser automatically on deploy
- Author name "Kapetanovic" or "Kapetanović" is bolded automatically

### Animations
- `.fade-in` class triggers scroll-based fade animation
- IntersectionObserver in `baseof.html` handles visibility

## Key Files to Know

### config.toml
- `baseURL`: Production URL
- `[params.social]`: Social links (used in footer)
- `[params.social.emailUser/emailDomain]`: Email split to prevent scraping
- `[taxonomies]`: Categories and tags for blog posts
- `[markup.goldmark.extensions.passthrough]`: Math delimiter config

### content/_index.md
Homepage content with experience timeline in YAML frontmatter:
```yaml
experience:
  - years: "2023 – now"
    title: "Research Scientist"
    org: "Company Name"
    org_url: "https://..."
    desc: "Description"
```

### Frontmatter Options

**Blog posts** (`archetypes/blog.md`):
```yaml
title: "Post Title"
date: 2024-01-01
categories: ["Category"]
tags: ["tag1", "tag2"]
description: "SEO description"
math: false  # Set true for KaTeX
draft: true  # Set false to publish
```

**Projects** (`archetypes/project.md`):
```yaml
title: "Project Name"
date: 2024-01-01
description: "Short description"
tags: ["Python", "ML"]
featured: false
links:
  github: "https://github.com/..."
  demo: "https://..."
  paper: "https://..."
```

## Partials Reference

| Partial | Purpose |
|---------|---------|
| `head.html` | Meta tags, CSS, theme init, KaTeX (conditional) |
| `header.html` | Navigation with mobile hamburger menu |
| `footer.html` | Contact section with email (JS-assembled) and social links |
| `theme-toggle.html` | Dark/light mode button |
| `project-links.html` | GitHub/Demo/Paper links for projects |
| `post-list-by-year.html` | Posts grouped by year with dates |

## CSS Classes

Main component classes in `assets/css/main.css`:
- `.nav`, `.nav-top`, `.nav-links`, `.nav-primary`, `.nav-secondary`
- `.menu-toggle`, `.menu-icon`, `.menu-icon-bar` (hamburger)
- `.home-section`, `.home-intro`, `.section-header`
- `.timeline`, `.timeline-item`, `.timeline-date`, `.timeline-content`
- `.post-list`, `.post-card`, `.post-header`, `.post-footer`, `.post-content`
- `.project-list`, `.project-item`, `.project-card`, `.project-links`
- `.publication`, `.publication-title`, `.publication-authors`, `.publication-venue`
- `.pub-cards`, `.pub-card`
- `.fade-in` (animation trigger)
- `.categories`, `.tags`, `.category`, `.tag`

## Deployment

Automatic via GitHub Actions on push to `main`:
1. Checkout code
2. Setup uv and parse BibTeX
3. Setup Hugo extended
4. Build with `--minify`
5. Deploy to GitHub Pages

Custom domain: `antekapetanovic.com` (configured in GitHub Pages settings)

## Common Tasks

### Add a blog post
```bash
hugo new blog/my-new-post.md
# Edit content/blog/my-new-post.md
# Set draft: false when ready
```

### Add a project
```bash
hugo new projects/my-project.md
# Edit content/projects/my-project.md
# Set draft: false when ready
```

### Update publications
1. Edit `bibtex/publications.bib`
2. Run `uv run python scripts/parse_bibtex.py`
3. Commit both files (JSON is gitignored, regenerated on deploy)

### Modify navigation
Edit `config.toml` under `[[menu.main]]` entries. Weight determines order.

### Change colors
Edit CSS variables in `assets/css/main.css` under `:root` and `[data-theme="dark"]`.

### Add social link
1. Add to `config.toml` under `[params.social]`
2. Add corresponding line in `layouts/partials/footer.html`
