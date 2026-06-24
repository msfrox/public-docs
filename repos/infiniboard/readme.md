# Infiniboard

Infinity Media's infinite whiteboard — **built on [Excalidraw](https://github.com/excalidraw/excalidraw)**,
deployed as its own Cloudflare Worker on its own subdomain (**board.gear.lk**), but sharing the
Infinity Hub's identity and data layer (one Google sign-in, one user/grant model, one file store).

It replaces the hub's previous in-house whiteboard (`/tools/whiteboard/`). Pivoting to Excalidraw
gives us, for free, a huge slice of the old "planned" list: full shape set + flyout, a real
properties panel (stroke / fill / opacity / font family & size / align / layers / z-order /
duplicate), editable lines & arrows, eraser, marquee multi-select, group/align, a native command
palette (⌘K) and search, image support, and proper mobile (pinch-zoom, collapsible UI). On top of
that we add the Infinity-specific features below.

## Stack

- **Vite + React 19 + TypeScript**, on a **vendored fork of Excalidraw** (`excalidraw/`, a
  git subtree of upstream `master`) consumed via npm workspaces — not the npm package. This lets us
  edit Excalidraw's source (toolbar, frames, etc.) natively and pull newer upstream features (e.g.
  native lasso) ahead of npm releases. See **Working on the fork** below.
- **Cloudflare Worker** (`worker/index.js`) serves the built app (`dist/`) and the `/api/*` endpoints.
- **Shared with the Hub** (same bindings as `infinity-hub`):
  - D1 `infinity-hub-authz` — users / apps / grants / per-tool data (boards live here; planner too).
  - R2 `infinity-hub-files` — images, video, PDFs (range/streaming).
  - Workers AI — the AI assist.
  - Cloudflare **Access** — the same Google SSO. One sign-in works across hub + board.
- Self-hosted Excalidraw fonts (copied into `public/excalidraw-assets/` at build, no CDN runtime dep).

## Run it locally

```bash
npm install
npm run dev          # vite dev server (UI only, no /api) at http://localhost:5273
# — or, to run the full app incl. the Worker + local D1/R2: —
npm run build
npx wrangler dev --port 8787 --local
```

For the Worker route to authenticate you locally (Access doesn't front localhost), copy
`.dev.vars.example` → `.dev.vars` (already git-ignored). It sets `ALLOW_DEV_AUTH=true` and a
`DEV_EMAIL`, so the Worker treats you as that signed-in user. **Never** set `ALLOW_DEV_AUTH` in prod.

First local run needs the D1 schema (it's the Hub's shared DB; apply against the local copy):

```bash
npx wrangler d1 execute infinity-hub-authz --local --file=../infinity-hub/worker/schema.sql
npx wrangler d1 execute infinity-hub-authz --local --file=./worker/schema-additions.sql
```

See [DEPLOY.md](DEPLOY.md) for production (custom domain, Access, public-share bypass, grants).

## Working on the fork

Excalidraw's source lives in `excalidraw/` (git subtree of upstream `master`). The app consumes the
**built** packages (committed `dist/prod` + `dist/types`) via npm workspaces, so a normal
`npm install` + `npm run build` (and Cloudflare deploy) needs no Excalidraw build step.

When you **edit Excalidraw source** (`excalidraw/packages/*/src`):

```bash
cd excalidraw && corepack yarn install   # one-time (installs the fork's build deps)
cd .. && npm run fork:build              # rebuild the fork's dist (esbuild + types)
npm run build                            # rebuild the app against it
git add -f excalidraw/packages/*/dist/prod excalidraw/packages/*/dist/types  # commit the new dist
```

**Sync upstream Excalidraw** (keeps our edits, 3-way merge):

```bash
git subtree pull --prefix excalidraw upstream-excalidraw master --squash
# then: cd excalidraw && corepack yarn install && cd .. && npm run fork:build && npm run build
```

Our fork edits so far:
- Infiniboard custom inserts in the native **"more tools" dropdown** (`components/Actions.tsx`,
  dispatch `ib:insert`) — works on mobile where a floating button doesn't.
- **Double-click a card to edit it** — `components/App.tsx` dispatches `ib:card-dblclick`.
- The blue "open link" handle suppressed for our cards — `renderer/staticScene.ts`.
- An "Infiniboard" shortcut island appended to the native `components/HelpDialog.tsx`.
- (Earlier) a `ToolbarCustomToolsTunnel` host slot + exported `<ToolbarCustomTools>`.

Next planned fork edit: **frame background fill + opacity** (renderer in `packages/element` + the
properties panel in `packages/excalidraw/components/Actions.tsx`). See [BACKLOG.md](BACKLOG.md).

## Project layout

```
worker/index.js            Worker: Access JWT verify, /api/me, /api/data, /api/files (R2),
                           /api/ai, /api/linkpreview, /api/share (public read-only).
worker/schema-additions.sql  Registers "infiniboard" in the shared apps table.
src/App.tsx                Main shell: auth gate, multi-board store, autosave, R2 file sync,
                           inserts, planner integration, the Excalidraw canvas + custom menu.
src/share.tsx              Public, read-only share viewer (share.html entry).
src/embeddables/cards.tsx  Custom cards rendered as Excalidraw "embeddable" elements
                           (note / task / timer / link / youtube / video / file / table).
src/components/NoteEditor.tsx  In-place WYSIWYG Markdown editor (TipTap) for note cards.
src/components/            Overlays: task editor, planner pin panel, AI, share, board manager.
src/api.ts                 Typed client for the /api/* endpoints.
src/boards.ts              Board store helpers (normalize, bin retention, card links).
```

## How features map

**Carried over from the old whiteboard:** multiple boards (switch / new / rename / archive / bin),
infinite pan-zoom, sticky notes, text, freehand pen, shapes, connectors (arrows that bind & follow),
frames that move their children, undo/redo, image paste/drop/upload, link preview cards, YouTube /
video / PDF / file cards, **task cards wired to the Planner** (pin, edit-writes-back, create-new),
a countdown **timer** card, **AI assist** (Workers AI), export (PNG / SVG / `.excalidraw`) + import,
command palette, search, private per-user data, board background colour.

**Now delivered via the Excalidraw pivot:** properties panel, opacity/transparency, custom colour
picker, fonts, layers/z-order, duplicate, editable lines/arrows + arrow labels, full shape set &
flyout, eraser, marquee select, group/align, mobile pinch-zoom.

**New in Infiniboard:** board manager (tags, archive, 30-day bin with restore/purge), public
read-only **share links** (live — always show the latest version).

**Known gaps / next (see [BACKLOG.md](BACKLOG.md)):** real-time multi-user collaboration (needs a
sync backend), table cards (Excalidraw has no native table), exact R2 usage stats, full Planner
task-editor parity, minimap.

## Documentation

- **[GUIDE.md](GUIDE.md)** — master usage guide: every tool, the settings, and recipes (mindmaps,
  flowcharts, system diagrams, plans). Start here to *use* the board.
- **[AI-CONNECTOR.md](AI-CONNECTOR.md)** — read/draw the board with Claude (scene-spec builder,
  `window.infiniboard` bridge, the file round-trip, and the Phase-2 live-sync plan).
- **[MAINTAINING.md](MAINTAINING.md)** — plain-English owner's guide. **[HANDOFF.md](HANDOFF.md)** —
  engineering orientation. **[DEPLOY.md](DEPLOY.md)** — production + the build/commit model.
- **[BACKLOG.md](BACKLOG.md)** — what's next. **[CHANGELOG.md](CHANGELOG.md)** — per-release notes.

## Version history

Full notes per release are in **[CHANGELOG.md](CHANGELOG.md)**. Current: **4.0.0** (2026-06-23) — the
**Board ⇄ Claude connector** (live MCP sync + scene-spec + `window.infiniboard` + Import diagram +
the `infiniboard-board` skill), separate shape **Text** colour, card-content **undo**, scene-portable
cards (copy/paste/export), native copy/paste + image-paste fixes, library persistence, lazy note
editor, and CI font-deploy hardening. Prior: **3.0.0** — frame fill, 2D colour picker, 23 fonts,
video/multi-file cards, R2 GC, minimap.
