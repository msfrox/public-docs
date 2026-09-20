---
title: Infinity Consultants — Website
repo: infinity-consultants-site
---
# Infinity Consultants — Website

Public marketing website for **Infinity Consultants** — strategy-first digital marketing.

- **URL:** https://infin8.agency
- **Hosting:** Cloudflare Workers (static assets) — account "infinity", worker `infinity-site`; auto-deploy on push to `main` via Workers Builds
- **Stack:** Pure HTML / CSS / vanilla JS — **no build step, no dependencies**

---

## Editing the site

Everything lives in `public/`:

| File | What it is |
| ---- | ---------- |
| `public/index.html` | The whole site (single page) — all text/content is here |
| `public/css/styles.css` | All styling. Design tokens (colors, fonts) are CSS variables at the top |
| `public/js/main.js` | Interactions: nav, reveal, FAQ, plan builder, WhatsApp prefill, Clients modal + Feed lightbox |
| `public/data/clients.json` | **Work** section content (edit this to add clients — see `data/README.md`) |
| `public/data/media.json` | **Feed** section content (edit this to add videos/images) |
| `public/assets/` | Logos, favicon, social-share image, plus `clients/` and `media/` uploads |
| `public/admin/` | Scaffolded visual CMS (inactive — needs GitHub OAuth to turn on) |

To change wording, prices, or packages: edit `public/index.html`, commit, push to `main`.
To add clients or feed media: edit the JSON in `public/data/` (see **[data/README.md](https://github.com/msfrox/infinity-consultants-site/blob/main/public/data/README.md)**).
The site deploys automatically — no Cloudflare access needed.

### Conventions
- Keep the **strict black / white / gray** monochrome theme — no color accents.
- Prices shown on the site must match the latest **Infinity Consultants – Pricing Guide**.
- Images: put new files in `public/assets/` and reference with root-relative paths (`/assets/...`).
- The brand logos are black-on-white JPEGs rendered white via the `logo-invert` CSS class — don't replace them with pre-inverted files unless you also remove that class.
- **Work** and **Feed** sections auto-hide until their JSON has published (non-`draft`) items — safe to push partial content.
- Don't commit copyrighted / reference material — `Other sources/` is gitignored.

## Run locally

No server needed — open `public/index.html` in a browser, or:

```bash
npx wrangler dev   # serves at http://localhost:8787, same as production
```

## Deploy

Pushes to `main` auto-deploy (Workers Builds). Manual deploy:

```bash
npx wrangler deploy
```

See [DEPLOY.md](https://github.com/msfrox/infinity-consultants-site/blob/main/DEPLOY.md) for the full setup and the go-live checklist.

---

## Version history

| Version | Date | Summary |
| ------- | ---- | ------- |
| **1.3** | Jul 2026 | Populated **Work** with four real clients (TecRoot, Gearz, Reboot, Cykel) and the **Feed** with 93 web-optimized items (83 graphics + 10 videos, transcoded from ~700 MB of source down to ~54 MB). Homepage Feed now shows a 5-item teaser (2 videos + 3 graphics); the full Instagram-style grid moved to a dedicated **`/feed/`** page. Raw source `Media/` gitignored. |
| **1.2** | Jul 2026 | Finalized on the **Pulse** direction (promoted to `/`, variants removed). Swapped in a Cinema-style **Info** statement and a Studio-style **Process timeline**. Added data-driven **Work** (Paper-Crowns-style hover index + case-study modal) and **Feed** (Instagram-style grid + lightbox) sections, both fed from `public/data/*.json` and auto-hiding when empty. Scaffolded an inactive Decap/Sveltia CMS in `public/admin/`. Moved to production domain **infin8.agency** (account "infinity", worker `infinity-site`); dropped the `ic.gear.lk` test domain. |
| **1.1** | Jun 2026 | Strict monochrome re-theme (mango removed). Five design variants deployed for selection (`/v1`–`/v5` + chooser at `/`): Pulse, Editorial, Terminal, Cinema, Studio. V1 gains particle hero, custom cursor, magnetic buttons, tilt cards, plan builder. Real WhatsApp number wired in (pending owner confirmation). |
| **1.0** | Jun 2026 | Initial site: hero, approach, services, 8-step process, Essential/Growth packages, add-ons, FAQ, contact. Dark monochrome + mango theme. |
