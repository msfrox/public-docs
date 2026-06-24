# Infinity Consultants — Website

Public marketing website for **Infinity Consultants** — strategy-first digital marketing.

- **Test URL:** https://ic.gear.lk
- **Hosting:** Cloudflare Workers (static assets), auto-deploy on push to `main` via Workers Builds
- **Stack:** Pure HTML / CSS / vanilla JS — **no build step, no dependencies**

---

## Editing the site

Everything lives in `public/`:

| File | What it is |
| ---- | ---------- |
| `public/index.html` | The whole site (single page) — all text/content is here |
| `public/css/styles.css` | All styling. Design tokens (colors, fonts) are CSS variables at the top |
| `public/js/main.js` | Interactions: nav, reveal animations, FAQ accordion, WhatsApp prefill |
| `public/assets/` | Logos, favicon, social-share image |

To change wording, prices, or packages: edit `public/index.html`, commit, push to `main`.
The site deploys automatically — no Cloudflare access needed.

### Conventions
- Keep the **black / white + mango (`#ffb020`)** theme. Accent is used sparingly — don't spray it around.
- Prices shown on the site must match the latest **Infinity Consultants – Pricing Guide**.
- Images: put new files in `public/assets/` and reference with root-relative paths (`/assets/...`).
- The brand logos are black-on-white JPEGs rendered white via the `logo-invert` CSS class — don't replace them with pre-inverted files unless you also remove that class.

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

See [DEPLOY.md](DEPLOY.md) for the full setup and the go-live checklist.

---

## Version history

| Version | Date | Summary |
| ------- | ---- | ------- |
| **1.1** | Jun 2026 | Strict monochrome re-theme (mango removed). Five design variants deployed for selection (`/v1`–`/v5` + chooser at `/`): Pulse, Editorial, Terminal, Cinema, Studio. V1 gains particle hero, custom cursor, magnetic buttons, tilt cards, plan builder. Real WhatsApp number wired in (pending owner confirmation). |
| **1.0** | Jun 2026 | Initial site: hero, approach, services, 8-step process, Essential/Growth packages, add-ons, FAQ, contact. Dark monochrome + mango theme. |
