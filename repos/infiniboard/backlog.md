# Infiniboard — Backlog

Pending work only. Shipped work lives in [CHANGELOG.md](CHANGELOG.md). Spun out of the Infinity Hub
backlog (the `Whiteboard` section) on 2026-06-18.

**Cross-cutting rule (like the hub): mobile-first + fast.** Prefer doing things *natively* — edit the
fork (slots, element fields, the properties panel) or reuse Excalidraw's own UI rather than bolting
on parallel components.

Rough priority: **P1** = next up · **P2** = wanted · **P3** = nice-to-have / someday.

---

## Bug Reports from the user
- [x] **P2 - the images placed on the board after an update goes blank** _(done version 4.0.1)_
      the images that are placed on a board, after an update the browser refreshes, the images go blank
      and just show an placeholder 
- [ ] **P2 - Frame persistant background + hitbox error** even when the background is set to transparent
      there is a slight blue tint in the frame. Cannot select or drag the frame by empety spaces when the
      background is set to transparent. - we did a fix to the hitbx error previously. please
      check that as well. currently im getting around this issue by setting the frame colour to #00000001
- [ ] **P1 md notes do not follow Z order** no matter the order note is always placed on the top. earlier
      there was an issue with the background staying at the bottom. not sure if that fix is causing
      this bug now. + the stroke of the note is rendered at the back as well. i.e. notes follow z order
      among the other notes. but when the top most note adds a stroke this stroke is rendered at the bottom
      behind all other notes. while the text and the background colour of the note is rendered at the front.
- [ ] **P1 update the claude skill to use mcp sync** it still refers to the old way. once updated bundle
      it in a zip file os its easier to add it to claude. add the skill to repo.
- [ ] **P1 errors found when using VS Code** when opening the project through VS Code the following erros
      came up not sure if they are relevant to us. please take a look
      - Option 'moduleResolution=node10' is deprecated and will stop functioning in TypeScript 7.0. Specify compilerOption '"ignoreDeprecations": "6.0"' to silence this error.
       Visit https://aka.ms/ts6 for migration information.
      - The common source directory of 'tsconfig.json' is '..'. The 'rootDir' setting must be explicitly set to this or another path to adjust your output's file layout. - did this with help from haiku
       Visit https://aka.ms/ts6 for migration information.
      - Option 'moduleResolution=node10' is deprecated and will stop functioning in TypeScript 7.0. Specify compilerOption '"ignoreDeprecations": "6.0"' to silence this error.
       Visit https://aka.ms/ts6 for migration information.
      - Option 'baseUrl' is deprecated and will stop functioning in TypeScript 7.0. Specify compilerOption '"ignoreDeprecations": "6.0"' to silence this error.
       Visit https://aka.ms/ts6 for migration information.
- [ ] **P1 Cannot change colour of text** cannot change colour of text placed with the text tool. clicking
      text colours does nothing. when placing the text on the board it picks up the last colour selected by
      the previous object that was in focus. cannot change colours even using the direct hex code. just
      just resets to the current colour.
- [ ] **P1 waraping objects in a frame changes to light mode.** when you select a few objects right click
      then select wrap selection in frame, it changes the board to the light theme from dark. does not go
      from light to dark. only from dark to light.
- [ ] **P1 Update all documents** the backlog is not updated. guide is barebones. guide needs all the minute
      details like shortcuts, nuances and best way to use each tool. all details like these are missing from
      it. please do some web reaserch and update guide. add proper use cases and how to make them guide.
- [ ] **P2 Bold does not work for custom fonts in Note card** when bolding a selection or the whole note after
      changing the font to a custom font does nothing. only google sans flex works.
- [ ] **P2 native fonts like the excalifont is missing from the note card**
- [ ] **P1 eyedropper does not work properly in dark mode** it picks up the non inverted colour even when in
      dark mode.

## Feature requests from User
- [ ] **P2 task card changes the planner data** since we can add new data to planner through the task card
      we need the "undo" to be able to undo any changes we made to the data through the tasks card. Add
      the ability to delete planner cards through the planner tasks ui. so if we want we can delete a placed
      task and clear its data from the board ui.
- [ ] **P1 Transparency controls in the colour picker** colour transparency already works on all the places
      where we have a colour picker. Adding the last two hex codes does this. so we only need to add a
      transparency control to the colour picker. (currently as a workaround i can add the desired hex value
      directly in the hex code for the transparency)
- [ ] **P3 Libraty of pre-made board templates to start from** when creating a new board we can pick from a
      selection of premade templates or a blank board. Option to add the current board as an template. 
      Update template with current board structure. delete/edit and manage templates.
- [ ] **P2 eyedropper to sample from images placed on the board** right now eyedropper only pickup the images
      placed only as black. we cannot pick a colour from an image we placed. would be really useful for
      sampling colours for a brand guide or so.
- [ ] **P3 Github connector** connect to github so we can put github documents (Markdown) directly on the board. We can use tiptap to render. two way sync possible? _vision is that i can directly import the docs of the apps im working on to the board. so for example i can see or edit a backlog directly from the board itself._ - need the connector so we can access the files in our private repo. also make this tool so we can put public docs as well -> i found a workaround for public docs - https://docsify-this.net/?basePath=https://raw.githubusercontent.com/msfrox/Prayer-Time-Site/main&homepage=README.md#/

## Reported from testing (4.0) — deferred, with a plan

- [ ] **P2 — Export/copy-as-image of cards shows the link, not the content.** Copy-as-PNG / Export of
      a board renders each card embeddable as its placeholder URL (`https://card.infiniboard.app/?id=…`)
      instead of the rendered card, because cards are HTML/React overlays, not canvas-drawn — Excalidraw
      only rasterizes canvas elements. Fix is non-trivial: on export, rasterize each card's DOM to an
      image (e.g. `html-to-image`) and composite it at the element's rect (or temporarily swap each card
      embeddable for an image element during export). Affects all card kinds. Until then, note bodies
      export as a blank box with the URL.
- [ ] **P1 — Embed tool: first link doesn't stick (resets/blank until re-entered).** Placing a web
      embed and setting its URL the first time often resets to blank on blur; editing the link again
      makes it stick, and subsequent edits work. Likely the create→validate→render order for a brand-new
      embeddable (the element exists before the link/validation settles). Investigate the fork embed
      create + `validateEmbeddable` caching/timing (we already "re-validate every pass" — see CHANGELOG
      3.0 — but the *initial* set still races). **Also:** after drawing an embed, auto-open the
      "edit link" prompt so the user doesn't have to invoke it manually. Fork change.
- [ ] **P2 — Paste image: draw the placement instead of auto-sizing.** When pasting an image, offer a
      drag-to-place/size tool (like the native image tool's click-drag) rather than dropping it at a
      fixed size at the cursor. Native image *insert* already supports drag-place; route clipboard
      images through that same flow.
- [ ] **P3 — "Reset to 100% / natural size" for images & videos.** A context-menu / properties action
      that resets a selected image (or video card) to its natural pixel dimensions (or a 1:1 scale).
      Fork action (read the file's natural size; for video cards we already store `w`/`h` in card data).

---

## Fork edits (we own the source now)

> ⚠️ **The fork features below were written in 2.3/2.4 but only actually shipped in 2.6.0** — the
> committed pre-built fork bundle was never rebuilt (`npm run build` ≠ `npm run fork:build`). Always
> run `npm run fork:build` after editing anything in `excalidraw/`. See the Release checklist in
> [MAINTAINING.md](MAINTAINING.md).

- [x] **P1 — Frame fill (colour + style) + opacity.** _(colour 2.3.0; fill styles + dark-mode
      inversion 3.0.0)_ Frames render their `backgroundColor` (Background swatch shown for frames),
      honour fill style (hachure / cross-hatch / solid), and the fill now inverts in dark mode via
      `applyDarkModeFilter` like every other element.
- [x] **P2 — Note format controls in the properties panel.** _(2.4.0; rebuilt 3.0.0)_ "Format note"
      section with B/I/S/code/headings/lists, plus (3.0) the **native colour picker** + **text size**
      controls — on desktop, tablet and mobile. Fork: `NoteFormatPanel.tsx`, `Actions.tsx`.
- [x] **P3 — 2D colour-map (SV) picker.** _(2.4.0; WYSIWYG-in-dark 3.0.0)_ Palette / Custom tab in
      every colour popup; Custom shows a draggable SV square + hue strip. 3.0: the gradient is shown
      through `--theme-filter` in dark mode so the picked colour matches the canvas.
- [ ] **P3 — Rotatable arrow labels** (snap to arrow direction / horizontal) — edit linear-element
      bound-text rendering in `packages/element`. _Deferred (do leisurely): requires breaking the
      `angle: 0` invariant for arrow-bound text across `bounds.ts` / `renderElement.ts` /
      `textElement.ts` (incl. an invariant assertion) — a multi-day change. Not worth risking the
      core render path; revisit when there's time._
- [ ] **P2 — Separate shape label colour from Stroke (font colour for shapes).** For *plain* shapes
      (rectangle/ellipse/diamond/arrow), the bound-text colour is the element's `strokeColor`, so you
      can't have a dark border with light text, etc. Notes already solved this (independent
      `customData.noteFg` + a dedicated picker + CSS invert). Do the equivalent for native bound text:
      add a `customData.labelColor`, a "Text colour" control in the properties panel when a shape with
      a label is selected, and render the bound text with it (`packages/element` text rendering reads
      the override, falling back to `strokeColor`). **Fork change → needs `npm run fork:build`.**
      Mirror the note's approach (see CHANGELOG 3.0 "Note Text colour" + `NoteFormatPanel.tsx`).
- [ ] **P3 — Card inserts as buttons in the top tool island** (instead of the extra-tools dropdown).
      _Deferred (do leisurely)._ There's a `ToolbarCustomTools` tunnel slot for this. Current state:
      inserts are grouped in the extra-tools dropdown (desktop + mobile), which works well; promoting
      them to top-island buttons is a bigger toolbar redesign (shortcuts, layout, mobile widths).
- [x] **P3 — Bundle a few Google Fonts locally.** _(shipped 2.4.0)_ Inter (11), Lato (12), Poppins
      (13) added to the native font picker. Latin woff2 files bundled; registered in constants.ts,
      font-metadata.ts, Fonts.ts. Zero runtime Google CDN requests.

## Board ⇄ Claude connector

> Phase 1 **shipped** (this thread): `scene-spec` builder (nodes/edges/notes/**cards**) +
> `window.infiniboard` bridge (read + draw + **create/edit cards + boards**) + **"Import diagram
> (Claude)"** menu + the `infiniboard-board` **Claude skill** + Export round-trip. See
> [AI-CONNECTOR.md](AI-CONNECTOR.md) and [GUIDE.md](GUIDE.md).

- [x] **In-app spec/scene import** _(this thread)_ — "Import diagram (Claude)" reads a SceneSpec or
      `.excalidraw` and drops it on the board.
- [ ] **P2 — Live two-way sync (MCP endpoint on the Worker).** Let Claude read/write the live board
      without manual export/import. Plan (full design in AI-CONNECTOR.md §4): `POST /api/connect` mints
      a personal connector token (hashed at rest, **user generates/holds it** per the secrets rule); a
      small MCP server (Worker / agents-sdk) exposes `read_board` / `write_elements` / `replace_board` /
      `create_board` / `list_boards`, auth = the token → same D1 row the app uses. Composes with the
      realtime-collab DO below.
- [ ] **P3 — `tools/` CLI to emit a spec/`.excalidraw` from outside the app** (e.g. for Cowork to write
      a file without the app open). Pure Node port of `scene-spec.ts`; the in-app importer already
      handles the spec format, so the CLI only needs to emit the JSON.

## Notes / editor

- [x] **Cards are scene-portable** _(this thread)_ — copy/paste (incl. cross-board), export, re-import.
      Card data is mirrored to `element.customData.card` (debounced, `captureUpdate: NEVER`) and
      `board.cards` is rehydrated from it when missing.
- [ ] **P2 — Undo for card *content* (notes/tasks/timers/table).** The customData mirror above uses
      `captureUpdate: NEVER`, so board-level Ctrl+Z still doesn't revert a note's text / table cells
      (the note editor's own Ctrl+Z works while editing). To fix: write the mirror with
      `captureUpdate: IMMEDIATELY` at **edit-session granularity** (e.g. on editor close, not per
      keystroke) and, in `onChange`, sync `board.cards` *from* `customData` when they diverge (so an
      undo that reverts customData also reverts the card) — but guard against reverting mid-edit. Tricky
      interplay; do deliberately.
- [ ] **P3 — Drop the dual storage of card data.** Card data now lives in both `board.cards` and
      `element.customData.card` (notes store markdown twice). Could make `customData` the single source
      of truth and derive `board.cards` as a cache, shrinking the saved D1 blob for note-heavy boards.

- [x] **P2 — Code-block syntax highlighting** _(shipped 2.4.0)_ TipTap `CodeBlockLowlight` +
      `lowlight` (all langs) in the WYSIWYG editor; `marked` renderer uses `highlight.js` for the
      canvas card; GitHub-style light/dark CSS theme.
- [x] **P2 — Dedicated Video tool.** _(shipped 3.0.0)_ A separate **Video** insert uploads a video
      and creates a playable card sized to the video's own aspect ratio (no black bars). Files card
      is now a plain multi-file list (no inline preview).
- [x] **P3 — Per-note (body) font picker.** _(shipped 3.0.0)_ "Text font" dropdown in the note panel
      (22 bundled families via `@font-face`) → `customData.noteFont`; code blocks always use Google
      Sans Code.
- [ ] **P3 — Per-text-run inline font.** Select text in a note → set its font (like bold). _Tried in
      3.0 with a TipTap FontFamily mark + toolbar control; reverted_ — `@tiptap/markdown`'s
      `getMarkdown()` drops the textStyle/fontFamily mark (Markdown can't carry font runs), so it lost
      the font on close. Needs a custom Markdown serializer for the mark (emit/parse `<span>`), or
      switching note storage to HTML. Revisit if worth the rework.
- [ ] **P3 — Bold / italic per font.** Each bundled font ships only weight 400. Real bold/italic
      needs extra woff2 weights AND a fork UI toggle (Excalidraw has no native bold/italic toggle for
      canvas text — weight is encoded in the family). Note bodies already support bold/italic via
      Markdown.

## Backend / data

- [x] **P2 — Exact R2 usage + per-board breakdown.** _(total 2.5.0; per-board 2.6.0)_ `GET /api/usage`
      sums R2 object sizes for the user's files and returns per-file sizes (`files: {key:bytes}`);
      Board Manager shows real total bytes + file count, and each board's own usage (matched
      client-side from its `/api/files/<key>` references). Loads lazily when the manager opens.
- [x] **P2 — R2 garbage collection.** _(shipped 3.0.0)_ Opening Manage Boards calls `/api/usage?gc=1`,
      which deletes owned R2 objects no longer referenced by any board (10-min upload grace). Storage
      usage now decreases after deletions.
- [ ] **P3 — Full Planner task-editor parity.** The task card editor already mirrors the Planner
      (list / status / priority / due / repeat / size / start / duration / My-Day / todos / notes);
      keep it in sync if the Planner schema changes. Ideally a shared component.

## Bigger features

- [ ] **P2 — Real-time multi-user collaboration.** Excalidraw supports it but needs a sync backend.
      Plan: a Cloudflare **Durable Object** per board (WebSocket) reconciling Excalidraw elements;
      reuse the Access JWT for auth. Biggest remaining item.
- [x] **P3 — Minimap.** _(2.5.0; viewport tracking 2.6.0; navigator + resize 3.0.0)_ Overview map,
      toggle `M`. 3.0: **click/drag to navigate**, **resizeable** (persisted), offscreen-cached for
      perf; bottom-right on desktop, top-right on mobile (clear of the bottom tool island).
- [ ] **P3 — Pin a board onto the Planner** (the reverse cross-link) once both ship together.
- [ ] **P3 — Folder-level / per-client persistent share** (from the hub backlog) — one stable link
      that surfaces a rotating set of boards. Ties into the wider client-sharing work.
- [ ] **P3 — Per-board permissions** beyond the app-level grant (ACLs), if boards get shared
      internally.

## Performance / responsiveness / security pass

> First pass done in **3.0.0** (see CHANGELOG). Remaining items below are follow-ups.

- [x] **Security — uploaded-file XSS hardening.** _(3.0.0)_ `/api/files/<key>` serves `nosniff` and
      forces `Content-Disposition: attachment` for non-media (so uploaded HTML/SVG can't run in our
      origin). Security headers (`nosniff` / `Referrer-Policy` / `X-Frame-Options`) added app-wide.
- [x] **Security — SSRF guard** _(3.0.0)_ on the server-side link-preview fetch (blocks private /
      loopback / link-local / metadata hosts).
- [x] **Perf — immutable file caching** _(3.0.0)_ R2 files now `max-age=31536000, immutable`.
- [x] **Security — npm audit reviewed** _(3.0.0)_ remaining advisories are in lazy Mermaid tooling +
      dev/build deps (no eager-path impact, no upstream fix). DOMPurify allowlist reviewed (links get
      `rel="noopener noreferrer"`). No secrets committed (Access JWT verified vs public JWKS).
- [ ] **Perf / bundle (follow-up).** Large chunks (Mermaid/KaTeX/Cytoscape/CodeMirror) are
      lazy-loaded, so initial load is the Excalidraw core (~728 KB gzip) + our small main. If Mermaid
      is dropped, several hundred KB + the lodash advisory go away. Audit the committed-`dist`
      approach (noisy diffs) vs building in CI.
- [~] **Responsiveness.** Mobile minimap/notes-panel/font-scroll fixed in 3.0; iOS PWA black-bar
      reworked in 2.6.0 — **verify on a real installed iPhone PWA**. Still to test: popovers/dialogs
      at very small Android widths; embeddable-card touch interactions.
- [ ] **Security follow-ups.** Decide whether to scope `GET /api/files/<key>` (signed/short-lived or
      share-token-gated) instead of public-by-opaque-key. Consider a CSP (tricky with Excalidraw's
      blob/worker/inline usage).
- [x] **General — Error boundaries.** _(shipped 2.5.0; card Retry fixed 2.6.0)_ `ErrorBoundary` wraps
      every card renderer (crash in one card no longer crashes the board). 2.6.0: added
      `fallbackRender(retry)` so the card fallback shows "⚠ This card failed to render" + a Retry
      button (the 2.5.0 card fallback was static, with no Retry).
- [ ] **General.** Offline/SW story, smoke-test checklist.

---

## Reference notes

- **Production secrets: none** — Access JWT verified against public JWKS; `ACCESS_*` /
  `BOOTSTRAP_ADMINS` are non-secret config. `ALLOW_DEV_AUTH` / `DEV_EMAIL` are local-only
  (`.dev.vars`). See [DEPLOY.md](DEPLOY.md).
- **Public file reads** (`GET /api/files/<key>`) are unauthenticated so shared boards render media.
  Revisit if boards ever hold sensitive files (security pass, above).
- **Old whiteboard data not migrated.** The hub's in-house whiteboard (`tool_data` scope
  `whiteboard`) is a different engine/format; Infiniboard starts fresh under scope `infiniboard`.
  The old tool still works in the hub during the transition.
