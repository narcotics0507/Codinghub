# Codinghub Static Docs Site Design

## Goal

Build a Cloudflare Pages-ready static tutorial site for the `narcotics0507/Codinghub` repository. The site should use the same broad structure and visual language as the referenced Yeelight tutorial center while using original, replaceable content and assets.

## Audience

The site is for teammates or readers who need a clean entry point for Coding Hub-related tutorials, setup paths, and operational guides.

## Visual Direction

- Bright, polished documentation center with a sticky top navigation, soft glass panels, subtle light accents, rounded controls, and spacious guide cards.
- Green is the primary accent, supported by cyan, yellow, coral, and violet path accents.
- Avoid copying Yeelight text or exported Feishu images. Use original content and CSS-generated visual panels until the user provides real screenshots.

## Site Structure

- `index.html`: overview page with hero, scenario switcher, path cards, and visual preview cards.
- `codex.html`: Codex setup guide.
- `cherry-studio.html`: Cherry Studio guide.
- `gpt-image-skill.html`: image generation guide with a small command generator.
- `openclaw.html`: local agent guide.
- `deployment.html`: Cloudflare Pages deployment guide.

Each tutorial page uses a hero section, a visual guide panel, sticky side navigation, and stacked content cards with tables, steps, code examples, and callouts.

## Interactions

- Reveal elements as they enter the viewport.
- Copy code snippets to the clipboard.
- Open visual panels in a lightbox.
- Highlight tutorial side navigation while scrolling.
- Switch the homepage scenario panel.
- Generate a sample image command from form fields on the image guide page.
- Show page scroll progress on tutorial pages.

## Deployment

The project is pure static HTML/CSS/JS. Cloudflare Pages should use:

```text
Framework preset: None
Build command: empty
Build output directory: /
```

If Cloudflare asks for a relative output directory, use `.`.

## Verification

- Run the Python structure test suite.
- Serve the site locally with `python3 -m http.server`.
- Use a browser or HTTP checks to verify key pages return `200`.
- Confirm no generated page links to the original Yeelight domain or original Feishu image paths.
