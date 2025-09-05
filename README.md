# My CV

Personal CV setup with PDF and web versions generated from YAML data.

## Live Site

<https://cv.vlcdn.dev>

## How it works

- `data.yaml` contains all my CV content
- Typst generates PDF from `typst/cv.typ`
- Jinja2 template renders HTML from `web/index.html.j2`
- GitHub Actions builds and deploys to Cloudflare Pages on push to main

## Local commands

```bash
# Build PDF
typst compile --root . typst/cv.typ --font-path typst/fonts/ cv.pdf

# Build HTML
uv run scripts/render.py web/index.html.j2 data.yaml build/index.html

# Generate favicons
uv run scripts/generate_favicons.py vadim.jpeg --output-dir build/

# Copy CSS
cp web/styles.css build/
```

## To update CV

1. Edit `data.yaml`
2. Push to main branch
3. Site updates automatically
