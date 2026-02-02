# My CV

Personal CV setup with PDF and web versions generated from YAML data.

## Live Site

<https://cv.vlcdn.dev>

## How it works

- `data.yaml` contains all my CV content
- Typst generates PDF from `typst/cv.typ`
- Astro generates HTML from `src/` using `data.yaml`
- Deno handles task running and TypeScript execution
- GitHub Actions builds and deploys to Cloudflare Pages on push to main

## Local commands

```bash
# Start development server
deno task dev

# Build for production (HTML + PDF + Favicons)
deno task build

# Preview production build
deno task preview

# Check types
deno task check
```

## To update CV

1. Edit `data.yaml`
2. Push to main branch
3. Site updates automatically
