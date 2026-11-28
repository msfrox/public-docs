---
title: Infinity Hub
repo: infinity-hub
---
# Infinity Hub

Internal knowledge base and tool hub for **Infinity Media / Infinity Solutions**.  
Built with [Astro + Starlight](https://starlight.astro.build/), served from **[hub.inf8.app](https://hub.inf8.app)** by a Cloudflare Worker (static site plus an API backed by D1 and R2).  
See [ROADMAP.md](https://github.com/msfrox/infinity-hub/blob/main/ROADMAP.md) for what is planned and [DEPLOY.md](https://github.com/msfrox/infinity-hub/blob/main/DEPLOY.md) for how it runs.

---

## What's in here

| Section | Contents |
| ------- | -------- |
| **Clients** | Positioning, personas, and brand guidelines for each managed brand (Cykel, Gearz, Reboot, TecRoot) |
| **Meta Ads** | Full Meta Ads Playbook v2.0 — 11 chapters from foundations to reporting |
| **SOPs** | Standard operating procedures — graphic design specs, morning standup, daily tasks |
| **Tools** | In-hub tools under `/tools/` (Meta Ads Dashboard, planner, whiteboard, post tracker), gated per user |
| **Dashboard & admin** | Home page launcher at `/`, admin console at `/admin-console` (users, apps, grants) |
| **Maintainers** | How to edit the site via the in-browser `/admin` editor or with Claude Code |

---

## Quick start

```bash
npm install       # install dependencies
npm run dev       # dev server at http://localhost:4321
npm run build     # production build → /dist
npm run preview   # serve the built /dist locally
```

---

## Deploying

The hub is a **Cloudflare Worker with Static Assets**, not a Pages site. `wrangler.jsonc` points
the Worker at `worker/index.js` and serves `./dist` (the Astro build) as static assets.

Cloudflare Workers Builds runs `npm run build` (per the comment in `wrangler.jsonc`). Whether a
push to `main` triggers it, and the exact dashboard build settings: **not verified from the
repo** — treat a push to `main` as live. See [`DEPLOY.md`](https://github.com/msfrox/infinity-hub/blob/main/DEPLOY.md).

## Project structure

```
src/content/docs/
  index.mdx                   # Landing page (hero + cards)
  clients/                    # One page per client brand (5 files)
  meta-ads/                   # Meta Ads Playbook chapters (11 files)
  sops/                       # Standard operating procedures
  maintainers/                # How to edit this site
src/styles/custom.css         # Theme: black/gray/white + mango (#FFB020)
src/assets/                   # Infinity logo (light + dark PNG)
public/
  tools/meta-ads/index.html   # Standalone Meta Ads Dashboard app
  admin/                      # Sveltia CMS in-browser editor at /admin
  assets/hub-store.js         # Shared-data helper (Gist Worker proxy)
  assets/infinity-ui.css      # Shared UI kit (canonical; copied into the other apps)
  assets/sidebar-toggle.js    # Desktop sidebar tab toggle + mobile hide
  clients/<client>/           # Per-client logos and brand assets
  sops-assets/<sop>/          # Images used inside SOPs
  Meta-Ads-Playbook.pdf       # Downloadable playbook PDF
worker/index.js               # Worker: /api/*, access gating, serves static assets
worker/lib/hub-auth.js        # Canonical Access-JWT verify + grant check (copied to other apps)
worker/schema.sql             # D1 schema
wrangler.jsonc                # Worker config and bindings
decisions/                    # ADRs 0001-0004 (platform boundaries)
astro.config.mjs              # Sidebar, title, logo, favicon, head scripts
DEPLOY.md                     # Full deploy & setup guide
CLAUDE.md                     # Instructions for Claude Code / AI editing
```

---

## Editing content

| Method | How |
| ------ | --- |
| **In-browser editor** | Go to `hub.inf8.app/admin` — sign in with GitHub (Infinity team only) |
| **Claude Code** | Open this repo; use the prompts in **Maintainers → Edit with Claude** |
| **Direct edit** | Edit `.md` files in `src/content/docs/`, commit, and push |

Every page needs frontmatter:

```md
---
title: Page Title
description: One-line summary (used by search).
sidebar:
  order: 1        # optional, controls ordering within the section
---
```

New `.md` files in an existing folder are picked up automatically (sections use `autogenerate`).  
New top-level sections require a new folder **and** a group entry in `astro.config.mjs`.

---

## Infrastructure

| Piece | Purpose |
| ----- | ------- |
| Worker `infinity-hub` | Serves `dist/` and handles `/api/*`; gates `/tools/*`, `/admin*` per user |
| Static assets (`ASSETS`) | The Astro/Starlight site |
| D1 `DB` (`infinity-hub-authz`) | Users, apps, grants, audit, and `tool_data` (light in-hub tools only; see ADR 0001) |
| R2 `R2` (`infinity-hub-files`) | File uploads (`/api/files`); KV `FILES` is the legacy fallback |
| Workers AI `AI` | `/api/ai` |
| Cloudflare Access | Google sign-in on `hub.inf8.app`; the Worker verifies the Access JWT on every request |
| `gist-proxy.shehan.workers.dev` | Gist Worker, still used by the Meta Ads dashboard only |
| `sveltia-cms-auth.shehan.workers.dev` | OAuth backend for the `/admin` editor |

`wrangler.jsonc` also binds the same D1 a second time as `infinity_hub_authz`; that is under
review (HUB-T3 in [TASKS.md](https://github.com/msfrox/infinity-hub/blob/main/TASKS.md)).

---

## Version history

| Version | Date | Summary |
| ------- | ---- | ------- |
| **2.0** | Jun 2026 | Meta Ads Playbook v2.0 (2026 updates): budget tiers, Shopify tracking, analytics, per-client blueprints, recruitment ads, reporting workbook. Neutral black/gray/white theme, dark/light mode sync, desktop sidebar tab toggle, mobile sidebar hide. |
| **1.1** | Jun 2026 | PDF modal viewer. Sveltia CMS `/admin` editor with Infinity branding. Maintainers section (Edit with Claude + Adding pages guides). Single-line header, background-contrast separator. |
| **1.0** | Jun 2026 | Initial launch. Astro + Starlight. Meta Ads Dashboard embedded at `/tools/meta-ads/`. Client pages: Cykel, Gearz, Reboot, TecRoot. Meta Ads Playbook chapters (v1). Graphic Design + Morning Standup SOPs. Mango accent theme. |

Current version: **2.0** (`package.json` → `"version": "2.0.0"`)
