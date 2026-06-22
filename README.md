# Codinghub Docs

Cloudflare Pages-ready static tutorial site for Codinghub.

## Local Preview

```bash
python3 -m http.server 4173
```

Open:

```text
http://localhost:4173
```

## Cloudflare Pages Settings

Use Git integration with this repository.

```text
Framework preset: None
Build command: leave empty
Build output directory: /
Root directory: leave empty
Production branch: main
```

If Cloudflare does not accept `/` as the output directory, use `.`.

## Custom Domain

After the first deployment succeeds, open the Pages project and add a custom domain under `Custom domains`. If the domain is already hosted on Cloudflare, the required DNS record is usually created automatically.

## Content Updates

- Edit page content directly in the root HTML files.
- Replace `assets/images/docs-hero.png` with real screenshots or guide artwork when available.
- Keep shared styles in `assets/css/styles.css`.
- Keep shared interactions in `assets/js/main.js`.

## Verification

```bash
python3 -m unittest tests/test_site_structure.py
```
