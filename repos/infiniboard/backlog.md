# Infiniboard — Backlog

**Pending work only.** Shipped work lives in [CHANGELOG.md](CHANGELOG.md). Spun out of the Infinity Hub
backlog (the `Whiteboard` section) on 2026-06-18.

**Cross-cutting rule (like the hub): mobile-first + fast.** Prefer doing things *natively* — edit the
fork (slots, element fields, the properties panel) or reuse Excalidraw's own UI rather than bolting on
parallel components. Anything under `excalidraw/` needs `npm run fork:build` (see [MAINTAINING.md](MAINTAINING.md)).

Priority: **P1** = next up · **P2** = wanted · **P3** = nice-to-have / someday.

---

## Connector (Board ⇄ Claude)

- [ ] **P1 — Cloudflare Access blocks the live MCP/REST connector.** ⚠️ *Infra setup, not code.* Verified:
      `curl -H "authorization: Bearer ibk_…" https://board.gear.lk/api/data/…` → **302 → Access login**.
      Cloudflare Access sits in front of the Worker, so the `ibk_` token never reaches it. The in-app
      bridge + file import work (browser has an Access session); the **external** MCP server does not.
      Fix (pick one, in the Zero Trust dashboard): **(a)** create an Access **service token** and a Service
      Auth policy on the board.gear.lk app — the MCP server already sends `CF_ACCESS_CLIENT_ID/SECRET`
      when set; or **(b)** an Access **Bypass** policy for `/api/connect*` + the token-authed `/api/data*`
      (safe — the Worker authenticates those itself). Full steps in [AI-CONNECTOR.md](AI-CONNECTOR.md) §4.
- [ ] **P2 — Real-time multi-user collaboration.** A Cloudflare **Durable Object** per board (WebSocket)
      reconciling Excalidraw elements; reuse the Access JWT for auth. Composes with the connector token.
      Biggest remaining backend item.
- [ ] **P3 — `tools/` CLI to emit a spec/`.excalidraw` from outside the app** (pure Node port of
      `scene-spec.ts`) so Cowork can write a file without the app open.
- [ ] **P3 — GitHub connector.** Put GitHub Markdown docs on the board (TipTap render; two-way sync?).
      Vision: edit a repo's BACKLOG/README from the board. Needs private-repo access; public-doc
      workaround exists (docsify-this.net over raw.githubusercontent.com).

## Cards / embeddables

- [ ] **P3 — Embeddable z-order vs native shapes (architectural).** Cards (notes/tasks/video/…) are HTML
      overlays in a DOM layer that always composites *above* the whole element canvas, so a card can't sit
      *behind* a native shape regardless of scene order. (Card-vs-card order works; card stroke now follows
      z-order — 4.1.0.) Only true fix = render cards as canvas bitmaps (rasterize) interleaved at the right
      z, with a live-overlay/snapshot hybrid for interactivity. Multi-day; shares its core with the export
      item below. Document + revisit.
- [ ] **P2 — Export / copy-as-image renders cards as the placeholder URL, not their content.** Same root
      cause as z-order: cards are DOM, Excalidraw only rasterizes canvas. Fix: on export, rasterize each
      card's DOM (`html-to-image`) and composite at its rect (or swap in an image element during export).
- [ ] **P2 — Undo for card *content* (note text / table cells / timer).** 4.0 added board-level undo via a
      `customData` history checkpoint; verify it covers all card kinds and that note-content reverts at
      *edit-session* granularity (on editor close), guarding against reverting mid-edit.
- [ ] **P3 — Drop the dual storage of card data** (`board.cards` + `element.customData.card`). Make
      `customData` the source of truth, derive `board.cards` as a cache; shrinks the saved D1 blob.
- [ ] **P3 — Task card ⇄ Planner: undo + delete.** Undo changes pushed to the Planner via a task card;
      add a "delete this task + clear its board card" action in the task UI.
- [ ] **P3 — Full Planner task-editor parity** — keep the task-card editor in sync with the Planner
      schema; ideally a shared component.
- [ ] **P3 — Pin a board onto the Planner** (reverse cross-link), once both ship together.

## Media (images / video)

- [ ] **P2 — Paste / insert image: drag-to-place instead of auto-size.** Route clipboard images through a
      drag-to-place flow like the native image tool. *Note (user):* the native image insert's drag-place
      also isn't working now — investigate that regression first.
- [ ] **P3 — Reset-to-natural-size: add a right-click context-menu entry.** The action ships as a
      command-palette item ("Reset image/video to natural size", 4.1.0); a fork context-menu entry would
      make it discoverable.
- [ ] **P3 — Eyedropper from a video card.** Infeasible via the canvas today (video is a DOM overlay, not
      on `app.canvas`); would need to rasterize the current video frame. Deferred. (Image sampling works.)

## Notes / fonts / editor

- [ ] **P3 — Variable-font migration for note bodies (futureproof bold/italic).** Note fonts currently
      bundle single-weight (400) static woff2; bold/italic render via browser *synthesis* (works — 4.1.0).
      For crisp real weights + italics, swap the families that have them to **variable** woff2 (Fontsource)
      and restore `font-weight: 100 900`. Caveats: not all 22 families have a variable file (Poppins, Lato,
      Space Mono, Instrument Serif, Barlow Condensed are static-only — keep synthesis for those), and
      variable files add ~several MB — do deliberately with a size review, per-font.
- [ ] **P3 — Per-text-run inline font.** Select text in a note → set its font. Blocked by `@tiptap/markdown`
      dropping the fontFamily mark on `getMarkdown()`; needs a custom Markdown serializer (emit/parse
      `<span>`) or HTML note storage.

## Frames

- [ ] **P3 — Rotatable arrow labels** (snap to arrow direction / horizontal). Requires breaking the
      `angle: 0` invariant for arrow-bound text across `bounds.ts` / `renderElement.ts` / `textElement.ts`
      — multi-day; not worth risking the core render path. Revisit leisurely.

## Toolbar / UI

- [ ] **P3 — Card inserts as buttons in the top tool island** (instead of the extra-tools dropdown). Uses
      the `ToolbarCustomTools` tunnel slot; bigger toolbar redesign (shortcuts, layout, mobile widths).

## Templates & sharing

- [ ] **P3 — Library of pre-made board templates.** Pick a template or blank when creating a board; save
      the current board as a template; update/edit/delete/manage templates.
- [ ] **P3 — Folder-level / per-client persistent share** — one stable link surfacing a rotating set of
      boards (ties into wider client-sharing work).
- [ ] **P3 — Per-board permissions (ACLs)** beyond the app-level Access grant, if boards get shared
      internally.

## Performance / responsiveness / security (follow-ups to the 3.0 pass)

- [ ] **Perf / bundle.** Large chunks (Mermaid/KaTeX/Cytoscape/CodeMirror) are lazy-loaded; dropping
      Mermaid would shed several hundred KB + the lodash advisory. Audit committed-`dist` vs building in CI.
- [ ] **Responsiveness.** Verify a real installed iPhone PWA (black-bar rework, 2.6.0); test popovers/
      dialogs at very small Android widths and embeddable-card touch interactions.
- [ ] **Security follow-ups.** Decide whether to scope `GET /api/files/<key>` (signed/short-lived or
      share-token-gated) vs public-by-opaque-key. Consider a CSP (tricky with Excalidraw blob/worker/inline).
- [ ] **General.** Offline / service-worker story; a written smoke-test checklist.

---

## Reference notes

- **Production secrets: none** — Access JWT verified against public JWKS; `ACCESS_*` / `BOOTSTRAP_ADMINS`
  are non-secret config. `ALLOW_DEV_AUTH` / `DEV_EMAIL` are local-only (`.dev.vars`). See [DEPLOY.md](DEPLOY.md).
- **Connector token** (`ibk_…`) is held by the user; only its SHA-256 hash is stored. Revoke all via
  `DELETE /api/connect`. The token alone can't reach the live Worker until Access is configured (top item).
- **Public file reads** (`GET /api/files/<key>`) are unauthenticated so shared boards render media.
  Revisit if boards ever hold sensitive files.
- **Old whiteboard data not migrated.** The hub's in-house whiteboard (`tool_data` scope `whiteboard`) is
  a different engine/format; Infiniboard starts fresh under scope `infiniboard`.
