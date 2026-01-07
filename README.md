# antekapetanovic.com

Personal website built with [Hugo](https://gohugo.io/).

## Local Development

```bash
# Install Hugo
brew install hugo

# Start dev server
hugo server

# Open http://localhost:1313
```

## Adding Content

```bash
hugo new blog/my-post.md
hugo new projects/my-project.md
```

## Publications

Edit `bibtex/publications.bib`, then regenerate JSON:

```bash
uv run python scripts/parse_bibtex.py
```

## Deployment

Pushes to `main` trigger GitHub Actions to build and deploy to GitHub Pages.

## License

MIT
