# Infinity Hub

Internal knowledge base and tool hub for **Infinity Media / Infinity Solutions**.  
Built with [Astro + Starlight](https://starlight.astro.build/), deployed to **[hub.gear.lk](https://hub.gear.lk)** via Cloudflare Pages (auto-deploy on push to `main`).

---

## What's in here

| Section | Contents |
| ------- | -------- |
| **Clients** | Positioning, personas, and brand guidelines for each managed brand (Cykel, Gearz, Reboot, TecRoot) |
| **Meta Ads** | Full Meta Ads Playbook v2.0 — 11 chapters from foundations to reporting |
| **SOPs** | Standard operating procedures — graphic design specs, morning standup, daily tasks |
| **Tools** | Live Meta Ads Dashboard at `/tools/meta-ads/` — checklists, per-client tabs, ClickUp sync |
| **Maintainers** | How to edit the site via the in-browser `/admin` editor or with Claude Code |

---

## Quick start

```bash
npm install       # install dependencies (re-run if OneDrive locks a file mid-install)
npm run dev       # dev server at http://localhost:4321
npm run build     # production build → /dist
npm run preview   # serve the built /dist locally
```

> **OneDrive note:** `node_modules/` and `dist/` are gitignored and never synced.  
> If `npm install` fails with `ENOTEMPTY` / `EPERM`, just run it again — it resumes.

---

## Deploying

Push to `main` → Cloudflare Pages automatically builds and deploys to **hub.gear.lk**.

| Setting | Value |
| ------- | ----- |
| Build command | `npm run build` |
| Output directory | `dist` |
| Node version | 20+ (set `NODE_VERSION=20` env var if needed) |

See [`DEPLOY.md`](DEPLOY.md) for the full one-time Cloudflare Pages setup.

---

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
  assets/hub-store.js         # Shared-data helper (Gist Worker read/write)
  assets/sidebar-toggle.js    # Desktop sidebar tab toggle + mobile hide
  clients/<client>/           # Per-client logos and brand assets
  sops-assets/<sop>/          # Images used inside SOPs
  Meta-Ads-Playbook.pdf       # Downloadable playbook PDF
astro.config.mjs              # Sidebar, title, logo, favicon, head scripts
DEPLOY.md                     # Full deploy & setup guide
CLAUDE.md                     # Instructions for Claude Code / AI editing
```

---

## Editing content

| Method | How |
| ------ | --- |
| **In-browser editor** | Go to `hub.gear.lk/admin` — sign in with GitHub (Infinity team only) |
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

| Service | Purpose |
| ------- | ------- |
| Cloudflare Pages | Hosting + auto-deploy on push to `main` |
| Cloudflare Access | Team-only access gating at `hub.gear.lk` |
| `gist-proxy.shehan.workers.dev` | Gist Worker — Meta Ads Dashboard data sync |
| `sveltia-cms-auth.shehan.workers.dev` | OAuth backend for the `/admin` editor |

---

## Version history

| Version | Date | Summary |
| ------- | ---- | ------- |
| **2.0** | Jun 2026 | Meta Ads Playbook v2.0 (2026 updates): budget tiers, Shopify tracking, analytics, per-client blueprints, recruitment ads, reporting workbook. Neutral black/gray/white theme, dark/light mode sync, desktop sidebar tab toggle, mobile sidebar hide. |
| **1.1** | Jun 2026 | PDF modal viewer. Sveltia CMS `/admin` editor with Infinity branding. Maintainers section (Edit with Claude + Adding pages guides). Single-line header, background-contrast separator. |
| **1.0** | Jun 2026 | Initial launch. Astro + Starlight. Meta Ads Dashboard embedded at `/tools/meta-ads/`. Client pages: Cykel, Gearz, Reboot, TecRoot. Meta Ads Playbook chapters (v1). Graphic Design + Morning Standup SOPs. Mango accent theme. |

Current version: **2.0** (`package.json` → `"version": "2.0.0"`)
