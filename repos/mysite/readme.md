---
title: "shehanferoze.com — \"Shehan's Desktop\""
repo: mysite
---
# shehanferoze.com — "Shehan's Desktop"

The personal site of Shehan Feroze, built as an operating system. Visitors "log in"
to Shehan's machine: a fake boot → login → a desktop with a taskbar, draggable/
resizable windows, desk clutter, and one app per section of the site. On phones the
same machine becomes Shehan's phone — lock screen, homescreen, full-screen app sheets.

**Live:** https://shehanferoze.com · Cloudflare Worker `shehanferoze-com`
**Concept doc:** [VISION.md](https://github.com/msfrox/mysite/blob/main/VISION.md) · **Plan / session handoff:** [BACKLOG.md](backlog.md)

## The apps

| Route | App metaphor | What it is |
|---|---|---|
| `/` | Browser (Firefox-ish chrome) | Homepage: hero, pinned intro scene, modules that boot one-by-one, the deck, ledger, terminal |
| `/work/` | ClickUp-style "taskpile" | Experience as a grouped task list; entries open as task-detail panels |
| `/projects/` | VS Code-style "code" | One file per project; frontmatter rendered as syntax-colored pseudo-code |
| `/notes/` | PowerPoint-style "slides" | Articles as decks: slide sorter index, slide rail navigation |
| `/photos/` | Photoshop-style "photo lab" | Layers panel = photos, properties panel = the story behind each |
| `/gaming/` | Steam-style "library" | Favorites shelf, live stats + achievements via the Steam Web API, Discord/Twitch cards |
| `/shares/` | Cloud-drive "shared with you" | Share anything with anyone (links/albums/files/notes), optional PIN lock |
| `/contact/` | Mail compose window | Pre-addressed message to Shehan; address-book sidebar with socials |
| `/the-glitch` (404) | — | Glitch page; future console easter egg |

All app chrome is hand-built CSS — homage layouts with generic icons, no official
logos or marks. Reference screenshots live in `_private/` (gitignored, never shipped).

There are also **8 hidden collectibles**. Find them by playing with the odd little
things. (Spoilers, if you must: `src/scripts/eggs.ts`.)

## Stack & architecture

- **Astro 6** — prerendered pages + a few server endpoints, deployed to
  **Cloudflare Workers** (`@astrojs/cloudflare`, assets binding + custom domains).
- **OS shell** (loaded on every page, ~9 KB raw JS total):
  - `src/os/registry.ts` — app ↔ route map + SVG icons (taskbar, desktop, homescreen, start menu all render from it; adding an app = one entry here + a page)
  - `src/scripts/os-shell.ts` — window manager (drag, 8-way resize, maximize/minimize, multi-window z-order), taskbar, start menu, boot/login, clocks, mobile shell
  - `src/scripts/eggs.ts` — the collectibles system (localStorage `sf_eggs`)
  - `src/styles/os.css` — all shell styling; `src/components/os/*` — shell markup
- **The containment trick**: pages scroll inside `.os-client`; its parent
  `.os-viewport` is a size container with `contain: paint`, so page-level
  `position: fixed` pins to the *window* and `100cqh` = the window viewport.
  Any page dropped into a window just works.
- **App shells**: `src/components/apps/` (WorkShell, CodeShell) or page-level
  (photo lab, slides, library, drive, mail). App pages pass `bare` to
  `Base.astro` and provide their own chrome.
- **Server endpoints** (`prerender = false`):
  - `POST /api/contact` — contact form (honeypot + rate limit; 503s politely until the Email Sending binding exists)
  - `GET /api/steam` — Steam Web API proxy, edge-cached 1h (player summary, library totals, recent games, achievement progress)
  - `POST /api/share` — PIN check for locked shares (URL never reaches the browser otherwise)

## Editing content

| What | Where |
|---|---|
| Work / projects / notes entries | `src/content/{work,projects,notes}/*.md` (schemas in `src/content.config.ts`) |
| Photos + stories | `src/data/photos.ts` + `src/assets/photos/` |
| Gaming favorites, Discord/Twitch links | `src/data/gaming.ts` |
| Shares (and PIN-locked items) | `src/data/shares.ts` |
| Social card image | `node scripts/make-og.mjs` → `public/og.png` |

## Development

```sh
npm run dev      # local dev server (localhost:4321)
npm run build    # production build into dist/
npm run deploy   # build + wrangler deploy to the live domain
npm run test:e2e # Playwright: window manager + collectibles (tests/)
```

Local secrets for testing server endpoints go in `.dev.vars` (gitignored).

`test:e2e` builds the site and serves it on `0.0.0.0` itself (see
`playwright.config.ts`'s `webServer`) — no separate `npm run dev` needed first.
On a minimal container without a system browser, it first sources
`scripts/playwright-container-libs.sh`, which fetches (no root needed) the
handful of shared libraries Playwright's bundled Chromium is missing there;
on a normal machine with a working browser that script is a no-op.

## Secrets & owner-only setup

Secrets are set **by the owner, in his own terminal** — never generated or handled
by an AI agent (see global security practice). Current state:

| Name | Purpose | Status |
|---|---|---|
| `STEAM_API_KEY` (secret) | Steam Web API | ✅ set — **rotate** (the first key was shared in a chat) |
| `STEAM_ID` (var) | SteamID64 (public, committed) | ✅ `76561198014859271` |
| `SHARE_PIN` (secret) | Unlocks PIN-locked shares | ⬜ `wrangler secret put SHARE_PIN` |
| `EMAIL` (send_email binding) | Contact form delivery | ⬜ enable Email Sending in dashboard, then uncomment in `wrangler.jsonc` |
| Turnstile | Bot protection on /api/contact | ⬜ together with EMAIL |

## Version history

| Version | Date | What |
|---|---|---|
| 3.0.0 | 2026-06 | **The OS rebuild** — window shell, eight apps, mobile phone shell, collectible easter eggs, Steam/shares/mail endpoints |
| 2.0.0 | 2026-06 | Astro 6 + Cloudflare Workers rebuild of the scraped site (ledger/desk/darkroom design language) |
| 1.x | —2026 | Original Framer site, later self-hosted as a static scrape |
