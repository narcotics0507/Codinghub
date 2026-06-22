# Codinghub Static Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Cloudflare Pages-ready static tutorial website with original content and a polished documentation-center layout.

**Architecture:** Use plain HTML, CSS, and JavaScript with no build step. Shared visual primitives live in `assets/css/styles.css`; shared browser behavior lives in `assets/js/main.js`; each page is an independently deployable static document.

**Tech Stack:** HTML5, CSS custom properties, vanilla JavaScript, Python `unittest` for structure checks, Cloudflare Pages static hosting.

---

## File Structure

- Create `tests/test_site_structure.py`: verifies required files, navigation links, scripts, styles, and absence of copied source-domain assets.
- Create `index.html`: overview page and entry point.
- Create `codex.html`, `cherry-studio.html`, `gpt-image-skill.html`, `openclaw.html`, `deployment.html`: tutorial pages.
- Create `assets/css/styles.css`: responsive visual system and component styling.
- Create `assets/js/main.js`: reveal, copy, lightbox, side-rail, homepage switcher, command generator, and progress interactions.
- Create `assets/favicon.svg`: original simple mark.
- Create `README.md`: Cloudflare Pages deployment instructions.
- Create `.gitignore`: ignore local server and OS artifacts.

## Tasks

### Task 1: Structure Test

**Files:**
- Create: `tests/test_site_structure.py`

- [ ] Add Python `unittest` checks for required pages, shared assets, navigation hrefs, Cloudflare-friendly static shape, and blocked source-domain strings.
- [ ] Run `python3 -m unittest tests/test_site_structure.py`.
- [ ] Confirm it fails because the site files do not exist yet.

### Task 2: Static Site Implementation

**Files:**
- Create: `index.html`
- Create: `codex.html`
- Create: `cherry-studio.html`
- Create: `gpt-image-skill.html`
- Create: `openclaw.html`
- Create: `deployment.html`
- Create: `assets/css/styles.css`
- Create: `assets/js/main.js`
- Create: `assets/favicon.svg`
- Create: `README.md`
- Create: `.gitignore`

- [ ] Build the shared navigation and page layout.
- [ ] Add original homepage content and tutorial content.
- [ ] Add all expected data attributes used by JavaScript.
- [ ] Add responsive styling and visual panels without external dependencies.
- [ ] Add README deployment settings for Cloudflare Pages.

### Task 3: Verification

**Files:**
- Read: all generated site files.

- [ ] Run `python3 -m unittest tests/test_site_structure.py`.
- [ ] Run a local server with `python3 -m http.server`.
- [ ] Check representative URLs return `200`.
- [ ] Confirm Git status only includes the intended new project files.

### Task 4: Git Handoff

**Files:**
- Stage all project files.

- [ ] Set `origin` to `https://github.com/narcotics0507/Codinghub.git` if missing.
- [ ] Rename the initial branch to `main`.
- [ ] Commit the generated site.
- [ ] Push `main` to GitHub if credentials are available.
