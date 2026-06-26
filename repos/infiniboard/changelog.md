# Changelog

All notable changes to Infiniboard. Versions follow [semver](https://semver.org/); dates are
release dates. Pending work lives in [BACKLOG.md](BACKLOG.md).

## 4.1.0 — 2026-06-26

A batch of P1 + P2 fixes from testing — colour/eyedropper/text correctness, frame-wrap theme, note
z-order, transparent frames, note fonts/bold — plus a transparency control, reset-to-natural-size,
the connector skill on MCP, an in-app guide, and the Cloudflare-Access finding for the connector.

### Added
- **Transparency control in the colour picker.** The **Custom** tab of every colour popup now has an
  **alpha slider** (checkerboard + transparent→solid gradient). It emits `#rrggbb` when opaque and
  `#rrggbbaa` when not (the 8-digit form Excalidraw already stores); the SV/hue pickers preserve the
  current alpha. The direct-hex workaround still works. Fork: `ColorPicker/SVPicker.tsx`,
  `ColorPicker/ColorPicker.scss`.
- **Excalidraw's own fonts in the note font picker.** Excalifont (the hand-drawn default), Virgil,
  Nunito, Comic Shanns and Lilita One are now selectable for note bodies — Excalidraw registers them in
  `document.fonts` at init, so the note HTML uses them by name (no fragile per-subset `@font-face`).
  Fork: `components/NoteFormatPanel.tsx`.
- **Reset image/video to natural size.** A command-palette action ("Reset image/video to natural size")
  resizes the selected image(s) to their file's natural pixels, or video card(s) to their stored w/h,
  keeping each element centred. `src/App.tsx`.
- **In-app guide + repo link.** The Help dialog's links now point at Infiniboard's own GUIDE.md and repo
  (was Excalidraw docs/blog/issues/YouTube). Fork: `components/HelpDialog.tsx`.
- **Connector: Cloudflare Access support.** The MCP server now forwards Access **service-token** headers
  (`CF_ACCESS_CLIENT_ID` / `CF_ACCESS_CLIENT_SECRET`) when set, so it can authenticate *past* Access
  while `IB_TOKEN` still identifies the user. `tools/mcp-server.mjs`; setup in AI-CONNECTOR.md.

### Fixed
- **Transparent frames: no blue tint, and grabbable from inside.** A frame with a transparent background
  still painted a faint blue wash (`rgba(0,0,200,0.04)`) and couldn't be selected/dragged by its empty
  interior (only the border/name). Now: no fill is painted when transparent, and frames are always
  draggable-from-inside (clicking a child still selects the child first). Fork:
  `element/renderElement.ts`, `element/collision.ts`.
- **Bold/italic work for the bundled note fonts.** Their `@font-face` rules declared `font-weight: 100
  900` on single-weight (400) files, so the browser thought 700 was covered and never synthesized bold
  (only the variable Google Sans Flex worked). Declared at `400` now (+ explicit `font-synthesis`), so
  bold/italic render via synthesis for every family. `src/styles.css`. (Real variable weights are a
  tracked follow-up — see BACKLOG.)
- **Text colour can be changed again.** The fork's `actionChangeStrokeColor` skipped **every** text
- **Text colour can be changed again.** The fork's `actionChangeStrokeColor` skipped **every** text
  element (to stop a shape's Stroke recolouring its bound label), which also blocked **standalone**
  text (the text tool) from taking any colour — clicking swatches/hex did nothing. It now skips only
  *bound* labels (`!(isTextElement(el) && el.containerId)`); standalone text recolours via Stroke as
  before. Fork: `actions/actionProperties.tsx`.
- **Wrap-selection-in-frame no longer flips the board to light mode.** When an action returns an
  appState without a `theme` and the host passes no `theme` prop, `syncActionResult` recomputed
  `theme = …?.theme || props.theme || THEME.LIGHT` and reset to light; `wrapSelectionInFrame` returned
  only `{ selectedElementIds }`. Fixed at the root (fall back to the live `this.state.theme` before
  LIGHT) and made the action spread `...appState` like its siblings. Fork: `components/App.tsx`,
  `actions/actionFrame.ts`.
- **Eyedropper is dark-mode correct.** This fork bakes the dark filter into the static canvas at render
  time, so the sampled pixel is in *display* space while colour fields are *storage* space — the picker
  returned the non-inverted value. It now converts the sample back through `applyDarkModeFilter` in dark
  mode (≈involutive, so it round-trips: the picked value matches the palette and re-renders as the
  sampled colour). Fork: `components/EyeDropper.tsx`.
- **Note stroke follows z-order.** A note's border was only canvas-drawn (behind every note's DOM
  overlay), so it rendered behind all other notes regardless of order. It's now mirrored into the DOM
  card as a CSS border (like the background already was) so it sits in the overlay layer and follows the
  same z-order. `src/embeddables/cards.tsx`. (Notes still composite above native shapes — inherent to
  Excalidraw's HTML-overlay embeddables; see BACKLOG.)
- **VS Code TypeScript deprecation warnings.** The vendored Excalidraw configs used the deprecated
  `moduleResolution: node10` (`"node"`/`"Node"`) + `baseUrl`. `ignoreDeprecations: "6.0"` is rejected by
  the fork's build TS (5.9.3), so modernized instead: `moduleResolution: "bundler"` and dropped
  `baseUrl` (paths resolve without it). No deprecated options remain; the fork build still passes.
  `excalidraw/tsconfig.json`, `excalidraw/packages/tsconfig.base.json`.

### Changed
- **Connector Claude skill now leads with live MCP sync.** `.claude/skills/infiniboard-board/SKILL.md`
  rewritten around the MCP tools (`read_board` / `draw` / `list_boards` / `create_board` /
  `set_active_board`) as the preferred path, with the file-import workflow as the fallback. Rebuilt the
  distributable `infiniboard-board.zip`; both stay in the repo.
- **GUIDE.md** expanded into a full usage reference: complete keyboard shortcuts
  (tools/edit/arrange/view/file), per-tool nuances (arrow binding, multi-point lines, crop, convert
  type, resize-from-centre, grid/snap), the transparency control + eyedropper, and the web-embed
  first-link note.

### Known / investigated
- **The live MCP/REST connector is blocked by Cloudflare Access.** Access fronts board.gear.lk and
  redirects token-only API calls to its login page (302) before the Worker runs, so the `ibk_` token
  can't authenticate externally (the in-app bridge + file import are unaffected). The connector code is
  correct (verified against the local Worker). Resolve by adding an Access **service token** or a
  **bypass** policy for the connector paths — see [AI-CONNECTOR.md](AI-CONNECTOR.md) §4 and BACKLOG (P1).
- **Embed first-link race** still open (diagnosed; workaround in GUIDE) — needs interactive debugging.

### Fork edits (require `npm run fork:build`)
- `components/App.tsx` — preserve current theme in `syncActionResult`.
- `actions/actionFrame.ts` — `wrapSelectionInFrame` spreads `...appState`.
- `actions/actionProperties.tsx` — Stroke recolours standalone text, not bound labels.
- `components/EyeDropper.tsx` — dark-mode colour-space conversion.
- `components/ColorPicker/SVPicker.tsx` + `ColorPicker.scss` — alpha slider.
- `components/NoteFormatPanel.tsx` — Excalidraw's own fonts in the note picker.
- `components/HelpDialog.tsx` — Infiniboard guide + repo links.
- `element/renderElement.ts` + `element/collision.ts` — transparent frames (no tint, grabbable inside).
- `tsconfig.json` + `packages/tsconfig.base.json` — `bundler` resolution, no `baseUrl`.

## 4.0.1 — 2026-06-23

### Fixed
- **Images no longer reload as placeholders.** A pasted/dropped image starts as a `data:` URL;
  `syncFiles` uploads it to R2 and rewrites the reference, but `onChange` skipped `data:` files and its
  signature dedup could skip the files-only rewrite — so the R2 reference never reached
  `board.scene.files` and the image was lost on reload. `syncFiles` now writes the R2 reference into the
  saved snapshot directly, and `onChange` keeps a referenced file (preferring an R2 copy, otherwise the
  live file even if still `data:`) instead of dropping it.
- **Note undo works when closing by clicking away,** not just via Escape. The commit-on-close
  checkpoint was debounced (500 ms), so a quick click-away + Ctrl+Z raced it. It's now committed
  synchronously on close (Escape and click-away alike).

## 4.0.0 — 2026-06-23

The **Board ⇄ Claude connector** plus a batch of board fixes and CI/deploy hardening.

### Added — connector (read & draw the board with Claude)
- **Live two-way sync (MCP).** A personal **connector token** (menu → "Connect to Claude (token)";
  minted server-side, shown once, only its hash stored) lets Claude read and draw on the live board.
  `tools/mcp-server.mjs` is a zero-dep stdio **MCP server** (`read_board`, `list_boards`, `draw`,
  `create_board`, `set_active_board`) — add it with `claude mcp add`. Claude's `draw` queues a spec
  (`POST /api/connect/draw`); the app imports it on load / window focus. Setup + limits in
  [AI-CONNECTOR.md](AI-CONNECTOR.md). (Real-time-while-both-edit still needs the planned collab DO.)
- **`window.infiniboard` bridge** (signed-in user, same-origin): READ (`text`/`getScene`/`getCards`),
  DRAW (`draw(spec)`/`addElements`/`loadScene`), CARDS (`addCard`/`addNote`/`updateCard`), BOARDS
  (`boards`/`newBoard`/`useBoard`), `exportScene`.
- **Scene-spec builder** (`src/scene-spec.ts`): a high-level spec (`nodes`+`edges`+`notes`+`cards`;
  `tree`/`grid`/`columns`/`free` layout) → Excalidraw elements with auto-layout + bound arrows. Diagrams
  use **native elements** (editable/undoable/exportable); `cards` ride in `customData` and rehydrate.
- **"Import diagram (Claude)"** menu item — open a SceneSpec or `.excalidraw` file.
- **CLI** `tools/board-from-spec.mjs` (validate / `--push` a spec) and the **`infiniboard-board`**
  Claude skill (author a board from a description — great in Cowork).
- **Docs:** [GUIDE.md](GUIDE.md) (master usage guide) and [AI-CONNECTOR.md](AI-CONNECTOR.md).

### Added — editor
- **Separate "Text" colour for shape labels.** A shape's Stroke no longer recolours its bound-text
  label; a dedicated **Text** picker (in the properties panel when a label is present) sets the label
  colour independently. Fork change in `actionProperties.tsx` / `Actions.tsx` (+ a distinct
  `boundTextColor` popup key, like the note "Text colour").

### Fixed
- **Native copy/paste of elements works again; image paste no longer doubles.** The fork's `onPaste`
  contract is inverted (return **`false`** = handled/suppress-native; **`true`** = let native run) and
  the app had it backwards — it suppressed native element/text paste and double-pasted images. Images
  now paste natively (one copy; `syncFiles` still offloads to R2); the custom image path was removed.
- **Board-level undo for card content.** Note text / table cells etc. are now revertible with Ctrl+Z:
  the `customData` mirror is a history checkpoint (debounced, `IMMEDIATELY`) tagged with a `_rev`, and
  `onChange` syncs `board.cards` back from `customData` when an undo/redo (or paste/import) changes it.
- **Cards are scene-portable** — copy/paste (incl. cross-board), export, re-import — via the
  `customData.card` mirror; `board.cards` rehydrates when missing.
- **Duplicating a note/card makes an independent copy** — `onChange` reconciles a card id referenced by
  >1 element, re-homing the extras onto fresh ids with deep-cloned data.
- **Personal library persists across reloads** — stored on the board store (`library` field), loaded
  into `initialData.libraryItems`, saved via `onLibraryChange`.
- **Custom fonts no longer break on the GitHub auto-deploy** — the vendored `excalidraw/.gitignore`
  silently dropped the 24 custom-font dirs from git, so CI rebuilt without them (404 → fallback). All
  33 font dirs are committed.

### Changed
- **perf:** the note editor (TipTap + lowlight, ~1.4 MB) is **lazy-loaded** (React.lazy) — off the
  initial bundle, loaded on first note edit.
- **build/deploy:** the app `dist/` is **no longer committed** (CI rebuilds it; local `npm run deploy`
  uploads the on-disk build) — only the fork's `dist/prod` + `dist/types` stay committed.
  **`fork:build` auto-stages** its output and **`build` runs a guard** (`verify-fork-assets.mjs`,
  `npm run verify:assets`) that fails if any fork output is untracked. See DEPLOY.md →
  "Build & commit model".

### Notes
- Card data is intentionally stored in **both** `board.cards` (the live, per-keystroke autosave store)
  and `element.customData.card` (the portable, history-captured copy). The small duplication is
  load-bearing — dropping it risked losing the last in-flight edit on reload.

## 3.0.0 — 2026-06-22

Final 3.0 release — includes all rc.3 fixes plus frame colour rendering and interaction.

### Fixed (3.0.0 final)
- **Frame colour no longer covers elements inside it.** When a frame had a background colour its
  fill was painted on top of child elements (the frame element was at a higher z-index than its
  children in the scene). The renderer now ensures each frame is always drawn before its own children
  regardless of their order in the elements array, so the background appears behind them.
- **Clicking elements inside a coloured frame now works.** Previously the frame's filled interior
  intercepted all pointer events, making child elements unreachable. The hit-test now prefers a
  child element over its parent frame when both are hit at the same point. Clicking empty space
  inside the frame still selects / drags the frame as expected.

### Fixed (rc.3)

### Fixed
- **Web embeds actually render now.** Two real causes, both fixed: (1) the host `renderEmbeddable`
  always returned a `<CardRouter>` (truthy), so Excalidraw never fell back to its native `<iframe>`
  and our router drew nothing for non-card URLs → it now returns `null` for plain web embeds; (2) the
  fork cached each embed's URL-validation result once, so setting a URL after placing an empty embed
  kept the stale "invalid" status and the embed never rendered ("tries to render and resets") → it now
  re-validates every pass. (With `validateEmbeddable` accepting any `http(s)` and the link editor
  adding `https://` to bare domains.) Sites that send `X-Frame-Options`/CSP still refuse to frame.
- **Note "Text colour" no longer changes the stroke.** Our note colour picker used the same popup key
  (`elementStroke`) as the native Stroke picker, so opening one opened the other — on mobile you'd hit
  the stroke popup. It now uses a distinct `noteText` popup type. The native **Stroke** control is
  unchanged (still there for the border).
- **Code blocks get a proper dark theme.** Code blocks now **opt out** of the note-wide invert filter
  (which turned grey comments into unreadable mid-grey) and use an explicit GitHub light/dark palette
  per mode — comments and tokens stay readable in both. Applies to the card and the editor.
- **Minimap resize grip** points the right way on mobile (was flipped 180°).

### Added
- **Canvas background colour picker.** The hamburger-menu "Canvas background" had `palette={null}`,
  so only the preset swatches showed — it now opens the full Palette / Custom colour picker.

## 3.0.0-rc.2 — 2026-06-21

The rc.1 features (below) **plus** these fixes and a performance / responsiveness / security pass.

### Fixed
- **Web embeds work with any URL.** `validateEmbeddable` previously fell back to Excalidraw's
  built-in domain allowlist (YouTube/Figma/…), so arbitrary URLs rendered blank. It now accepts any
  `http(s)` URL, and the embed prompt **adds `https://` to a bare domain** (a missing scheme was the
  main reason embeds stayed blank). (Sites that send `X-Frame-Options`/CSP `frame-ancestors` still
  refuse to load — that's the remote site's choice.)
- **Unified, explicit card-link editing.** Editing a card's URL goes through one chokepoint
  (`actionLink`) — so **right-click "Edit link", Ctrl+K, and the properties-panel link button** all
  work and stay consistent, for **web embeds, YouTube and Link cards**. Our cards route to the host
  editor by kind; **native web embeds use a reliable prompt** (the built-in hyperlink popup did
  nothing here). Double-click still works for our cards too.
- **Note format panel cleanup.** The B/I/heading/list buttons were removed from the *properties
  panel* — clicking them stole focus from the open editor and closed it. Only **Text font / Text
  colour / Text size** remain (they work whether or not the note is being edited). Use the note's own
  floating toolbar for inline formatting.
- **Note editor opens in the current theme** (was always light). It's inverted with the same filter
  as the rendered card in dark mode; the floating toolbar is counter-inverted so it stays readable.
- **Code blocks readable in dark mode again.** Removed the dark-mode `.hljs-*` overrides — the note
  is inverted as a whole, so those double-inverted and washed out comments. Light hljs colours +
  the note filter now produce correct dark-mode colours. Code-block background darkened for contrast.
- **Colour-picker swatch spacing** tightened to 2px to match the native picker (was 5px).

### Added — per-note fonts
- **Text font picker** in the note properties panel (22 bundled families) — sets the note body font
  via `customData.noteFont`; persists; works in the card and the editor.
- **Code uses Google Sans Code** (bundled mono) everywhere in notes, independent of the body font.
- Bundled fonts now have `@font-face` rules so note HTML (not just the canvas) can use them.
- _Deferred (verified):_ per-text-run inline font (select text → set font). Implemented with a TipTap
  FontFamily mark, but confirmed the font run is **dropped on `getMarkdown()`** (notes are stored as
  Markdown, which can't carry font spans) — so it would silently lose the font on close. Reverted;
  needs an HTML/rich storage model or a custom Markdown serializer — backlogged.
- **Font fetching is documented** in [FONTS.md](FONTS.md) (Fontsource CDN pattern + where files go).
- **Minimap position is now responsive:** bottom-right on desktop (unchanged), **top-right on mobile
  only** (so the bottom tool island doesn't cover it); the resize grip flips to the reachable corner.
- **Note colour picker:** the preset swatches now have spacing (they were touching).
- **Note code blocks** use a darker background for legibility (held through the dark-mode invert).

### Performance / responsiveness / security pass
- **Security — stored-XSS hardening.** Uploaded files served from `/api/files/<key>` now send
  `X-Content-Type-Options: nosniff`, and anything that isn't safe-inline media (images except SVG,
  video, audio, PDF) is forced to **download** (`Content-Disposition: attachment`). This stops an
  uploaded `.html`/`.svg` from executing scripts in our origin and reaching the Access session.
- **Security — SSRF guard.** The server-side link-preview fetch now rejects private / loopback /
  link-local / cloud-metadata hosts (10.x, 127.x, 169.254.x, 192.168.x, 172.16–31.x, localhost, …).
- **Security headers.** App responses send `X-Content-Type-Options: nosniff`, `Referrer-Policy:
  strict-origin-when-cross-origin`, `X-Frame-Options: SAMEORIGIN`; API JSON sends `nosniff` +
  `no-store`.
- **Performance — caching.** R2 files are immutable (a new opaque key per upload), so they're now
  served `Cache-Control: public, max-age=31536000, immutable` (was 1 day). Hashed JS/CSS keep the
  asset system's long cache; HTML revalidates.
- **Audit.** `npm audit`: the remaining advisories (lodash via Mermaid's parser; nanoid; esbuild/
  miniflare) are all in **lazy-loaded diagram tooling** or **dev/build tools** (not the eager runtime
  path), have no upstream fix, and only run on the user's own input. Documented; revisit if Mermaid
  is dropped.
- **Notes on accepted trade-offs:** `GET /api/files/<key>` stays public (required so shared boards
  render media — keys are opaque/unguessable); arbitrary web embeds are allowed but run in
  cross-origin sandboxed iframes (can't touch our origin).

---

## 3.0.0-rc.1 — 2026-06-21

**Feature-complete release candidate.** A big round of UX, theming, media, fonts and backend work.
Everything below is in addition to the 2.x features. (Promoted to 3.0.0 after the performance /
responsiveness / security pass — see above.)

### Navigation
- **Minimap is a navigator.** Click or drag anywhere in the minimap to jump the viewport there —
  no zoom/scroll needed. **Resizeable** from the bottom-left grip (size persists in localStorage).
  Anchored **top-right** so the mobile bottom toolbar never covers it. Perf: the element layer is
  cached to an offscreen canvas and only rebuilt when the scene changes; pan/drag just blits the
  cache + the viewport rect, drawn in a rAF loop that runs only while the minimap is open.
- Horizontal scroll: use **Shift + wheel** (Excalidraw built-in). The experimental Alt+wheel
  handler was removed.

### Notes (Markdown cards)
- **Text colour + size moved into the properties panel** ("Format note" section) — on **desktop,
  tablet and mobile** (mobile/tablet show a "Format note" popover button). The colour control is
  Excalidraw's own fast picker (Palette + Custom SV), not a slow OS dialog.
- **Theme-aware text, the native way.** Note text colour is just a colour; in dark mode the whole
  note is inverted with the *exact same* `--theme-filter` Excalidraw applies to the canvas, so notes
  track native elements in lockstep. No more "auto" button or custom contrast logic.
- Direct **numeric font size** (px) + S/M/L/XL presets; default base size 16px.

### Colour & theme (replicating native)
- **Frame fill now inverts with the theme** (`applyDarkModeFilter`), like every other element — it
  no longer stays a fixed colour in dark mode. Fill *style* (hachure / cross-hatch / solid) is
  honoured too.
- The **custom SV colour picker is WYSIWYG in dark mode** — its gradient is shown through
  `--theme-filter`, so the colour you pick is the colour you get on the (inverted) canvas.

### Media / cards
- **Dedicated Video tool.** Inserts a playable video sized to the video's own aspect ratio (no more
  black bars). Separate from files.
- **File card holds many files.** Add / remove files, download one or all; click a name to open.
  No on-canvas preview (it's a file list, by design). Replaces the old single-file chip.
- **Editable cards.** Link and YouTube cards: double-click to edit. Native **web embeds**: edit via
  the built-in "Edit embeddable link" (right-click / Ctrl+K) — no accidental double-click edits.

### Fonts
- **23 fonts bundled** (woff2 from fontsource, lazy-loaded): Inter, Poppins, IBM Plex Sans, Work
  Sans, Manrope, Outfit, Google Sans Flex, Space Grotesk, Bricolage Grotesque, Syne, Unbounded,
  Sora, Barlow Condensed, EB Garamond, Playfair Display, Merriweather, Fraunces, Instrument Serif,
  Geist Mono, Space Mono — plus **Noto Sans Sinhala, Noto Serif Sinhala, Noto Sans Tamil**.
- **Google Sans (Flex) is the app UI font** — bundled variable woff2, used across the chrome and the
  Excalidraw editor UI. Canvas text + code keep their own fonts.

### Toolbar
- Extra-tools dropdown **regrouped** (Insert: Video · Link · Upload file(s) · YouTube · Task · Timer
  · Web embed; then Note) with a proper line-style note icon, on **desktop and mobile**.

### Backend
- **R2 garbage collection.** Files removed from a board are now reclaimed: opening Manage Boards runs
  a sweep that deletes owned R2 objects no longer referenced by any board (with a 10-minute upload
  grace so in-progress edits aren't reaped). Storage usage finally goes *down* after deletions.

### Maintenance
- Verified the whole properties panel (incl. our note controls and frame fill) is ported to the
  mobile/compact panels. Font list scrolls on touch (`touch-action: pan-y`). Card error boundaries
  show a Retry. Version bumped to 3.0.0.

### Fork edits (require `npm run fork:build`)
- `element/src/renderElement.ts` — frame fill: dark-mode filter + fill styles.
- `excalidraw/components/Actions.tsx` — note Format panel on desktop/compact/mobile; dropdown regroup; Video item.
- `excalidraw/components/MobileToolBar.tsx` — dropdown regroup; Video item.
- `excalidraw/components/NoteFormatPanel.tsx` — native colour picker + size controls.
- `excalidraw/components/LayerUI.tsx` — pass setAppState to SelectedShapeActions.
- `excalidraw/components/App.tsx` — (reverted the embed double-click broadening).
- `common/src/constants.ts`, `excalidraw/fonts/*` — 21 new font families.

---

## 2.6.0 — 2026-06-21

**The v2.3/2.4 fork features actually ship now.** Root cause: those features live in the
vendored Excalidraw fork, but the committed pre-built bundle
(`excalidraw/packages/excalidraw/dist/prod/index.js`) was never rebuilt after the fork source was
edited — `npm run build` does not run `npm run fork:build`. So the custom colour picker, bundled
fonts, note format panel, frame fill, and mobile tools dropdown were all written but never made it
into the deployed app. Rebuilt the fork; all of them are now live. Added a Release checklist to
[MAINTAINING.md](MAINTAINING.md) so this can't silently recur.

### Fixed (were "not showing up" — stale fork build)
- **Custom colour picker** (Palette / Custom tabs, SV square + hue strip). Verified rendering.
- **Bundled fonts** Inter / Lato / Poppins in the native font picker.
- **Note format panel** ("Format note" section when a note is selected).
- **Frame fill + opacity** (colourable frames).
- **Mobile "more tools" dropdown** (Note/Task/Timer/Upload/YouTube/Link) — verify on device.

### Fixed (genuine bugs)
- **Minimap viewport rect now tracks pan/zoom.** `api.onChange` doesn't fire on pure pan/zoom, so
  the rect went stale. Replaced with a `requestAnimationFrame` watcher that redraws on any
  scroll / zoom / scene change. Verified the minimap redraws on scroll.
- **Right-click menu unreadable in light mode.** The app forced a dark surface + light-text palette
  onto `.excalidraw` for *all* themes, so in light mode the context menu was white-on-white. Dark
  overrides are now scoped to `.excalidraw.theme--dark`; light mode uses Excalidraw's native
  readable palette. Verified via computed CSS variables.
- **Card error fallback now has a Retry button.** `ErrorBoundary` gained a `fallbackRender(retry)`
  prop; the card fallback shows "⚠ This card failed to render" + Retry.
- **iOS PWA black bar.** The app container is now `position: fixed; inset: 0` so it fills the visual
  viewport even when `window.innerHeight` is briefly wrong on first standalone paint (the
  "rotate to fix it" bug). html/body background matches the app. Verify on an installed iPhone PWA.

### Added / changed
- **Per-board storage usage.** `GET /api/usage` now also returns per-file sizes (`files: {key:bytes}`);
  the Board Manager shows each board's R2 usage next to its media count (computed client-side by
  matching the `/api/files/<key>` references each board holds). Verify totals after deploy.
- **Note text colour moved to the properties panel.** Removed the text-colour button from the note
  editor toolbar; the "Format note" panel now has a colour swatch + an **Auto** button. The colour
  is stored on the element (`customData.noteFg`) so it persists and the card re-renders instantly.
- **Theme-adaptive note text.** A note with no explicit colour and a transparent background now
  flips its text light/dark with the canvas theme (like native Excalidraw text); solid-fill notes
  keep dark text. Note text is no longer coupled to `strokeColor`.
- **Direct numeric note font size.** The note editor has S/M/L/XL presets (now 14/16/20/26 px) plus
  a numeric px input; default base size raised from 13 → 16 px. Legacy notes' `scale` is mapped up.

### Fork edits (require `npm run fork:build`)
- `packages/excalidraw/components/NoteFormatPanel.tsx` — added a text-colour swatch + Auto (dispatches `ib:note-color`).

---

## 2.5.0 — 2026-06-21

Real R2 storage usage, minimap, and error boundaries.

### Added
- **Exact R2 storage usage.** `GET /api/usage` sums the real byte sizes of every file the
  current user has uploaded to R2 (paginates automatically). The Board Manager now shows e.g.
  _"4.2 MB in R2 (17 files)"_ instead of an approximate media count. Usage loads lazily when
  the manager opens.
- **Minimap.** A small canvas overlay appears in the bottom-right corner of the board showing
  all elements at reduced scale with a yellow viewport indicator. Toggle with the `M` key or
  via the Command palette → "View: Toggle minimap". Redraws are throttled to 120 ms.
- **Error boundaries.** A `ErrorBoundary` class component wraps every card renderer — a crash
  inside one card (bad data, extension bug, etc.) now shows a ⚠ inline fallback with a Retry
  button instead of crashing the whole whiteboard.

### Changed
- Rotatable arrow labels assessed as a 2-3 day fork edit (angle=0 enforced in 4+ places);
  moved to low-priority backlog.

---

## 2.4.0 — 2026-06-21

Colour picker upgrade, bundled fonts, note format panel, and code-block syntax highlighting.

### Added
- **2D SV colour picker.** Every colour popup now has a **Palette / Custom** tab toggle.
  The Custom tab shows a saturation-value gradient square (drag to pick hue+saturation+value)
  plus a hue strip below it. Fully draggable; syncs with palette selection.
- **Google Fonts bundled locally.** Three new font families appear in Excalidraw's native font
  picker — **Inter** (clean UI sans-serif), **Lato** (humanist sans-serif), and **Poppins**
  (geometric sans-serif). Latin woff2 files are committed; no runtime Google CDN requests.
- **Note format panel in the properties panel.** When a note card is selected, a "Format note"
  section appears in the left properties panel with B / I / S / `</>` / H1 / H2 / H3 / bullet /
  numbered / code-block buttons. Buttons dispatch window events caught by the open editor.
- **Code-block syntax highlighting.** The WYSIWYG note editor uses `CodeBlockLowlight` (TipTap +
  lowlight) to highlight code blocks live. The canvas-card display (`marked`) also highlights
  via `highlight.js`. Supports JS/TS, Python, Bash, CSS, HTML/XML, JSON, SQL, Go, Rust, Markdown.
  GitHub-style light/dark CSS theme included.

### Fork edits
- `packages/excalidraw/components/ColorPicker/SVPicker.tsx` — new SV + hue picker component.
- `packages/excalidraw/components/ColorPicker/Picker.tsx` — Palette / Custom tab mode.
- `packages/excalidraw/components/ColorPicker/ColorPicker.scss` — tab + picker styles.
- `packages/excalidraw/components/NoteFormatPanel.tsx` — new format-button panel component.
- `packages/excalidraw/components/Actions.tsx` — note-format fieldset when note selected.
- `packages/common/src/constants.ts` — `Inter: 11`, `Lato: 12`, `Poppins: 13` in `FONT_FAMILY`.
- `packages/common/src/font-metadata.ts` — metrics for the three new fonts.
- `packages/excalidraw/fonts/Fonts.ts` — `init("Inter"…)`, `init("Lato"…)`, `init("Poppins"…)`.
- `packages/excalidraw/fonts/Inter|Lato|Poppins/` — woff2 files + `index.ts` per font.

## 2.3.0 — 2026-06-21

Mobile tools, frame fill, note font size, and note text colour wired to the properties panel.

### Added
- **Mobile tool dropdown** — Infiniboard inserts (Note, Task, Timer, Upload, YouTube, Link) now
  appear in the mobile toolbar's "extra tools" dropdown (was missing; only the desktop dropdown had
  them).
- **Frame background colour + opacity** — select a frame and use the Background colour swatch and
  Opacity slider in the properties panel. Colour and opacity are rendered on the canvas.
- **Note font size** — S / M / L / XL size buttons in the note editor toolbar; scales the base font
  size (stored as `card.scale`).
- **Note text colour → native Stroke swatch.** Note text colour is now driven by the element's
  `strokeColor`; change it via the properties panel or the "A" button in the editor toolbar (both
  stay in sync). New notes default to `#1a1205` (readable on the yellow default background).

### Fixed
- **PWA fullscreen on iPhone** — removed the `.ib-app` padding approach (caused dark bars when the
  canvas background is light); replaced with per-element safe-area offsets on Excalidraw's top bar
  and bottom toolbar.

### Fork edits
- `packages/element/src/comparisons.ts` — added "frame" and "magicframe" to `hasBackground` so
  the Background colour picker shows for frames in the properties panel.
- `packages/element/src/renderElement.ts` — frame fill now uses `element.backgroundColor`
  (fallback: original faint-blue tint); also applies `element.opacity`; calls `fill()` before
  `stroke()` so the colour actually renders.
- `packages/excalidraw/components/MobileToolBar.tsx` — added the Infiniboard inserts block to the
  mobile extra-tools dropdown (mirrors the desktop `Actions.tsx` block).

## 2.2.0 — 2026-06-21

Note tool rebuilt as a true WYSIWYG editor, plus a round of card/tool polish from testing.

### Added
- **Native in-place WYSIWYG note editor (TipTap).** Double-click / Enter / insert opens an editor
  positioned over the note (no modal). WYSIWYG by default with a live **Raw ⇄ Formatted** toggle and
  a floating toolbar (headings, bold/italic/strike, inline code, lists, checklists, quote, code
  block, link, divider, **tables with add/remove row & column**, text colour). Stores GFM Markdown
  (paste-friendly, round-trips).
- **Custom inserts moved into Excalidraw's native "more tools" dropdown** (Note, Task, Timer, Upload
  file, YouTube, Link) — fixes mobile, where the floating "+" button was lost when the toolbar
  docks to the bottom.
- **Double-click a card to edit it** — notes open the editor; links prompt to change the URL.
- **Multiple file upload** — the Upload file tool accepts several files at once.

### Changed
- **Cards own a clean native surface.** Background / Stroke / Edges come from the element (the
  properties panel) and render on the canvas; the note content is transparent and inset so it sits
  *on* that surface — no HTML frame, no double border. Cards default to a transparent stroke.
- **Link card** is larger by default (so the preview + link are visible without resizing) and the
  host/URL is pinned to the bottom; clicking the card opens the link in a new tab.

### Fixed
- **Blue "open link" arrow removed from our cards** — it's canvas-drawn (`renderLinkIcon`), now
  suppressed in the fork for `card.infiniboard.app` links (CSS couldn't reach it).
- **Transparent note background stays transparent** (no longer falls back to yellow).
- **Raw toggle is clickable** (was overlapped by the hidden colour-picker input).
- **App-mount crash (React #310)** — `insertRef` was a hook declared *after* the gate early-returns,
  so the hook count differed between the loading and authed renders. Moved it above the gates. Also
  hardened React resolution with explicit Vite aliases so the fork's nested `react@19.0.0` can never
  shadow the app's copy.

### Fork edits
- `renderer/staticScene.ts` — skip the blue link handle for our card embeddables.
- `components/App.tsx` — double-click on a card embeddable dispatches `ib:card-dblclick`.
- `components/Actions.tsx` — Infiniboard inserts added to the native "more tools" dropdown
  (dispatch `ib:insert`).

## 2.1.0 — 2026-06-20

Forked-Excalidraw polish round.

### Changed
- **Themed Excalidraw to the hub palette** — mapped surface / border / text + accent CSS variables
  onto the Infinity UI tokens so the editor reads as one app.
- **Markdown note went fully native** — colours from the native element via the properties panel;
  removed MDXEditor and its modal (smaller bundle). AI assist drops a Markdown note.
- **Toolbar cleanup** — the insert set is only genuinely custom tools (Note, Task, Timer, File,
  YouTube, Link); removed Sticky and the separate Frame/Lasso/Table UI (Frame + Lasso are native;
  Markdown tables replace the Table card).

### Added
- **Infiniboard keybinds in the native Help dialog** (appended as their own island).
- **Mobile** — `100dvh` full height (fixes the Safari address-bar gap); insert UI as a bottom sheet.

## 2.0.0 — 2026-06-20

**Forked Excalidraw.** Vendored upstream `master` into `excalidraw/` (git subtree), React 19,
consumed via npm workspaces; the built `dist` (prod + types) is committed so deploys are a single app
build (no yarn/esbuild in CI). Upstream sync via `git subtree pull`.

- Native toolbar slot (`ToolbarCustomToolsTunnel` + exported `<ToolbarCustomTools>`) for custom
  inserts — no DOM injection.
- Native lasso (newer than npm 0.18.1).
- Markdown note cards — full GFM (marked + DOMPurify) on canvas + share view.

## 1.1.2 — 2026-06-19

Testing round 2: native Help dialog restored (full shortcut list) + reachable from the menu; custom
tools grouped behind one toolbar "Insert" button (no mobile overflow); proper lasso icon; "Frame"
uses the native frame tool (moves its children); **PWA** — installable, standalone, iPhone safe-area
insets + theme colour.

## 1.1.1 — 2026-06-19

Testing round 1b: merged custom tools into the native toolbar (one bar); full shortcuts reference;
save status moved into the menu with a timestamp; lasso shortcut Q→M; mobile help-button overlap
fixed.

## 1.1.0 — 2026-06-19

Testing round 1: hamburger chrome + tool island; mango/yellow theme; working command palette (⌘K) +
shortcuts; freeform lasso; table + Area cards; full Planner task editor; save-loop fix.

## 1.0.0 — 2026-06-18

Initial Excalidraw-based build: multi-board (switch / new / rename / archive / 30-day bin), board
manager (tags, media count), autosave to D1, R2 file sync, custom cards (task / timer / link /
YouTube / video / file), Planner integration, AI assist (Workers AI), public read-only share links.
Plus everything Excalidraw provides natively (properties panel, shapes, lines/arrows, eraser,
group/align, command palette, export/import, mobile pinch-zoom).
