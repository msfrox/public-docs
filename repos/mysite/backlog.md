# Backlog — shehanferoze.com

_Forward plan for the "Shehan's Desktop" build (see VISION.md — the source of truth
for all concept details). Phases are shippable chunks, in order._

## Phase 1 — Window shell foundation ✅ (2026-06-11, verified locally, not deployed)
- [x] Window manager: Windows-style chrome [ — □ ✕ ], draggable, resizable (8 handles),
      multi-window (desk items spawn windows + taskbar entries), z-order on focus,
      maximize/restore (dbl-click titlebar too), minimize
- [x] Taskbar (bottom): start menu (apps + lock), app icons → sections, Colombo clock tray
- [x] Desktop scene (wallpaper + dot grid + ෂෙ glyph, icon column, desk items:
      sticky note / polaroid / cv doc → spawn windows)
- [x] Boot/lock screen + fake login (BIOS lines → avatar/password/Welcome) → browser
      opens maximized; sessionStorage-gated (`sf_os`); Enter/click skips; reduced-motion skips
- [x] Mobile shell skeleton: Android lock screen → full-screen app sheets, status bar,
      nav pill → homescreen overlay (clock widget, app grid, dock)
- Architecture notes: `src/os/registry.ts` (app↔route map + icons), `src/scripts/os-shell.ts`
  (one shared WM module), `src/styles/os.css`, `src/components/os/*`. Pages scroll inside
  `.os-client`; `.os-viewport` is a size container with `contain: paint` so page-level
  `position: fixed` pins to the window and `100cqh` = window viewport (used by Deck,
  404, photos pages). Keyboard scrolling handled (focused client + body-key fallback).
- Phase-1 leftovers (cosmetic, superseded by later phases): photos-desk items can poke
  past window edges (Phase 4 restyles that app); closing the home browser minimizes to
  desktop (re-open via taskbar); "ship only active shell's JS/CSS" deferred to Phase 9.

## Phase 2 — Homepage v2 (inside browser chrome) ✅ (2026-06-11, deployed)
- [x] Keep hero (boot lines, kinetic name, lede)
- [x] Pinned text scene ("Thirteen years of operations…") ported from v3-scroll
      (PinnedIntro.astro — phrases, parallax float chips, progress dots, reduced-motion static)
- [x] **Modules as pinned scroll scene** — modules boot one-by-one ("mounting…" line +
      loading bar → content), kicker counts n/4, settles into the hoverable grid
- [x] Deck ("Things I shipped") stays
- [x] Ledger hover gray → slightly transparent (done 2026-06-11)
- [~] Composition shipped = Shehan's sketch (hero → pinned text → pinned modules → deck →
      ledger → terminal → footer). Alternatives offered for consideration (not built):
      (a) "boot order" — modules scene FIRST as if the OS loads the person, then hero as
      the "login complete" moment; (b) "ledger-led" — pinned text merges INTO the ledger
      (each phrase pins a ledger row), deck after. Shehan: pick/ignore at leisure.
- [~] **HOMEPAGE LAB** (2026-06-12, deployed): /lab/ = a boot-menu selector linking 5
      experimental full-page homepage redesigns, all sharing src/data/home-lab.ts.
      Linked from a dashed callout on the real homepage (after the terminal). The
      stable homepage stays default — these are throwaway candidates for Shehan to
      pick a winner from (or none):
      - v1 SF-BIOS SETUP — 90s blue BIOS utility, tabbed, arrow-key nav
      - v2 THE VOID — infinite pannable star-canvas, content floats, minimap
      - v3 THE FEROZE LEDGER — printed annual report, cream paper, the only light build
      - v4 POSTER MODE — brutalist scroll-snap chapters, giant type, marquees
      - v5 SYS-MONITOR — live htop dashboard (uptime counter, load bars, process table,
        canvas load-graph, real session stats from the visitor's own browser)
      → Shehan picks; winner can replace src/pages/index.astro, then delete src/pages/lab/.

## Phase 3 — Apps wave 1 (work tools) ✅ (2026-06-11, built from _private screenshots)
- [x] ClickUp-style Experience app ("taskpile"): workspace sidebar w/ spaces, list/board/
      calendar view tabs, grouped rows (in progress/delivered auto-split by period),
      task codes (SF-26xx), colored role pills, priority flags, SF assignee avatars;
      detail = task panel (status pill, fields table, description, fake activity feed)
- [x] VS Code-style Projects app ("code"): activity bar, explorer tree (README.md +
      projects/*.md), tabs, breadcrumb, frontmatter rendered as syntax-colored
      pseudo-code const block, per-block line numbers, decorative minimap, status bar
- Both pages are `bare` now (own app chrome replaces StatusBar/footer inside the window);
  work/projects detail pages no longer use Entry.astro (notes still do, until Phase 4)

## Phase 4 — Apps wave 2 (creative tools) ✅ (2026-06-11, built from _private screenshots)
- [x] Photoshop-style Photos app ("photo lab"): menu bar, tool strip, the_album.psd tab,
      checkerboard canvas w/ prev/next + ←/→ keys, Properties panel (title/meta/story),
      Layers panel grouped by chapter w/ thumbnails (PS-blue selection). Replaces both
      the desk page AND the standalone darkroom (/photos/album/ → redirect to /photos/);
      desk vocabulary already lives on the OS desktop
- [x] PowerPoint-style Notes app ("slides"): index = slide sorter (ribbon + 16:9 title-
      slide cards); article = reading view w/ slide rail (title + per-h2 thumbs, click
      scrolls, scroll highlights), "slide n —" section labels, depth-entrance h2s
      (translateZ) + subtle body rise, reduced-motion static, images supported in md

## Phase 5 — Steam gaming app ✅ code-complete (2026-06-11; live stats await Shehan's key)
- [x] Steam-style library UI at /gaming/ ("library", new app in registry/taskbar/
      homescreen): store/library/community nav, sidebar game list, Recent-activity
      shelf (live), Favorites shelf w/ generic CSS capsule art (PUBG, Timberborn,
      No Man's Sky, GTA V, Rocket League — edit src/data/gaming.ts), about + stats
- [x] Worker proxy /api/steam: recently-played + owned-games, edge-cached 1h,
      graceful "cartridge not inserted" fallback when no key
- [x] LIVE 2026-06-12: STEAM_API_KEY secret set + STEAM_ID var (76561198014859271,
      resolved from vanity "no999"); profile Game details confirmed public; /api/steam
      returns real data (243 games, 1367h, recent: Wallpaper Engine + Timberborn)
- [x] 2026-06-12 expansion: player strip (avatar/name/level/online state/profile link),
      per-game achievement progress bars (GetPlayerAchievements, first 6 recent games),
      "Squad & streams" shelf — Discord server + Twitch cards from src/data/gaming.ts
      (mock entries; buttons say "link coming soon" until Shehan pastes real URLs)
- [ ] **Shehan**: paste real Discord invite + Twitch URL into src/data/gaming.ts
      (community[].url) — everything else lights up automatically
- [ ] **Shehan**: REGENERATE the Steam key (the one shared in chat is a throwaway —
      rotate it at steamcommunity.com/dev, then `wrangler secret put STEAM_API_KEY`
      with the new value yourself). Optional: real profile URL → src/data/gaming.ts

## Phase 6 — Easter eggs v3: desktop collectibles (concept pivoted 2026-06-11, see VISION)
- [x] Remove 404s auto-redirect (timer stays as a curiosity object) — done 2026-06-11
- [x] v1 shipped 2026-06-11 (src/scripts/eggs.ts): 7 hidden triggers, one per app —
      dial ×3 clicks (home), "+ add task" (work), node_modules/ (projects), a layer's
      eye (photos), "▶ present" (notes), "+ add a game" (gaming), 📎 attach (mail).
      Found egg → sticker pinned to desktop (mobile: homescreen sticker row), toast,
      localStorage persistence, "eggs: n/7" counter in start menu
- [x] Mobile gap closed 2026-06-12: alternate mobile-visible triggers added (editor
      status bar "⎇ main", the_album.psd tab "×", library "store" tab); plus a new
      8th egg in the shares app (the activity tab / drive footer line) → now n/8
- [ ] Decide the full-set reward (about_you.exe? secret folder? personal note from
      Shehan) — toast currently teases "something more is coming…"
- [ ] 404 page: no longer the finale — hide one egg there later (then n/8)

## Phase 7 — Shares app ✅ code-complete (2026-06-12; broadened: share ANYTHING with anyone)
- [x] Cloud-drive style app at /shares/ ("drive — shared with you", new registry app):
      items of any kind — link / album / file / video / note — kind icons, audience
      chips, dates, open buttons; inline PIN unlock flow for locked items
- [x] One data file (src/data/shares.ts) drives everything; 3 placeholder demo items
      live until Shehan replaces them (a read-me note, a public example, a locked example)
- [x] PIN gate: locked items keep their URL server-side (lockedUrl never rendered);
      POST /api/share {id, pin} checks env.SHARE_PIN, rate-limited 10/10min
- [ ] **Shehan**: `wrangler secret put SHARE_PIN` (any PIN you'd give family), then
      replace the placeholder items in src/data/shares.ts with real shares

## Phase 8 — Contact as email client ✅ UI done (2026-06-11; sending awaits Shehan)
- [x] Compose-window UI ("mail — new message"): send toolbar, To pre-addressed pill,
      From (name+email), Subject (folded into the message body client-side), full-height
      body, signature line, address-book sidebar (reveal email + socials). Same
      /api/contact backend (honeypot + rate limit intact).
- [ ] **Shehan**: enable Email Sending for shehanferoze.com in dashboard; then add
      `"send_email": [{ "name": "EMAIL" }]` to wrangler.jsonc
- [ ] Turnstile on the endpoint (do together with Email Sending — pointless before)

## Phase 9 — Mobile full pass + launch
- [ ] Android shell complete (widgets, app icons, crash-to-homescreen)
- [x] a11y audit (2026-09-21, away session): axe-core ran in a real browser (Playwright,
      against a local `wrangler dev --local` build, all 8 pages: /, /work/, /projects/,
      /notes/, /photos/, /gaming/, /shares/, /contact/) under wcag2a/aa + wcag21a/aa +
      best-practice. Before: 77 color-contrast violation nodes (shared `--dim`/`--mut`
      tokens plus half a dozen hardcoded near-duplicates rendering 1.5–2.5:1 against dark
      backgrounds, need 4.5:1), 1 heading-order skip (homepage h1→h3, no h2 anywhere), 1
      nested-landmark (`gaming`'s `<main>` inside the OS window's own landmark `<section>`).
      After: 0 violations on all 8 pages. Also found and fixed a real keyboard-blocker: the
      three desk-item buttons (sticky note/photo/CV) sat inside `aria-hidden="true"` (whole
      desktop was hidden from screen readers) and only listened for pointer events, so Tab
      + Enter did nothing even for sighted keyboard users — confirmed broken, then confirmed
      fixed, live in the browser both times. Added a document-level Escape (closes the start
      menu with focus returned to Start, or closes/minimizes whichever window focus is
      inside) — neither had a keyboard dismissal before, only outside-click. `prefers-
      reduced-motion`: window open/resize were already gated in JS; added CSS coverage for
      three transform transitions that weren't (start menu slide-in, mobile lock unlock
      swipe, egg toast) — opacity fade stays, position change is now instant; verified both
      branches with `page.emulateMedia` against the live dev server. Full writeup + before/
      after evidence: `docs/a11y-phase9-2026-09-21.md`.
      - [ ] **Shehan**: Lighthouse ≥95 mobile is unverified — this container has no local
            Chrome and can't build one (`libnspr4.so` etc. missing, no root/apt to install
            them; confirmed by downloading Playwright's Chromium and trying to launch it).
            Run `npx lighthouse http://localhost:4321 --preset=mobile` on RUBY2 or from a
            machine with a real browser.
      - [ ] One accepted, low-priority contrast exception left as-is (not a bug): CodeShell's
            line-number gutter — explicitly decorative (existing code comment) and matches
            real code-editor convention of a muted gutter.
- [ ] Cloudflare Web Analytics snippet
- [ ] Content review pass (case studies "needsReview", placeholder photo stories)
- [x] OG image — public/og.png generated 2026-06-12 (scripts/make-og.mjs, window-chrome
      themed social card; rerun the script to regenerate)
- [ ] Deploy + verify live

## Working mode (while Shehan is away, w/e of 2026-06-13)
- Deploy WIP builds to the live domain (`npm run deploy`) — it's Shehan's remote test
  bench (phone browser beats remote desktop for testing the mobile shell). No visitors
  yet; contact API is inert without the EMAIL binding, so no security exposure.
- Each session ends with: BACKLOG updated (this file is the handoff), build deployed,
  and a short "what changed / what to look at" note in the session summary.
- Shehan resumes ~every 5h with "continue the site" — memory + this file carry context.
- Decision made: apps open **windowed** over the desktop (keep!) — desktop is part of
  the experience, not an easter egg.

## Parked / decisions
- [ ] Real photo stories + locations from Shehan (placeholders live in src/data/photos.ts)
- [ ] Updated CV when ready (current one outdated; ledger uses it + known additions)
- [ ] Draft articles pending review: running-my-own-corner-of-the-internet,
      shipping-free-software-with-an-ai-pair

## Done
- [x] 2026-06-10 — Hosting migrated GitHub Pages → CF Workers; repo private; Pages removed
- [x] 2026-06-10 — Phase 1–2 design concepts (ledger/systems/darkroom, album, desk, scroll scenes, 404)
- [x] 2026-06-11 — Astro 6 + CF adapter build: home, work, projects, notes (4 published
      + 2 drafts), photos desk + album, contact + /api/contact, 404, RSS/sitemap/robots,
      compile-time images. Verified locally incl. mobile. Not yet deployed.
