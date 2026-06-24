# Infinity Hub — Backlog

_Internal-only (repo root, not published to the site). Started 2026-06-10._

## North star

Evolve the Hub from a knowledge base into a **work management platform that actually
fits how we work** — eventually replacing ClickUp (bloated, slow, bad on mobile).

> **Cross-cutting rule for everything below: mobile-first + fast.** Most of the team
> works from phones; the #1 complaint about ClickUp is the mobile experience. Every
> tool must be designed for a phone first and feel instant.

- [ ] **ClickUp audit:** inventory every ClickUp feature we actually use today
      (spaces/folders/lists structure, custom fields, statuses, content calendar
      workflow, post tracker sync, reminders, time tracking…) — that list is the
      baseline feature set the Hub platform must cover before we can switch.
- [ ] **Ongoing research:** keep researching work-management / agency-ops tooling and
      add more feature ideas to this backlog as they come up. Living document.

## Platform foundation

- [x] **Dashboard + access layer** (2026-06-13) — personalized dashboard (now the home
      page at `hub.gear.lk/`), D1-backed user/app/grant model, `/admin-console`, access
      enforced server-side in `worker/index.js` against the Cloudflare Access (Google)
      token. See *Maintainers → Dashboard & access*.
- [x] **Security hardening + per-tool data + UX** (2026-06-18):
      - Dashboard is the site home; theme matched to Starlight; **Log out** button (Access logout).
      - **Member route-gating** — direct links to restricted app pages (`/admin`,
        `/admin-console`, `/tools/*`) are blocked server-side unless granted. KB/docs stay open.
      - **Per-tool data isolation** — `GET/PUT /api/data/<tool>?key=…` with shared or
        per-user (`key=me`) scope; access requires the app grant. Use this for every new tool.
      - **Protected admins** — bootstrap admins (from `BOOTSTRAP_ADMINS`) can't be demoted,
        suspended, or deleted by anyone via the UI/API. (Answers: a new admin cannot remove you.)
      - Moved KB landing to `/start/` (normal page, has the sidebar); removed app links from KB.
- [~] **Custom fields engine** (shared across Post Tracker / planner / future boards).
      v1 built in Post Tracker (2026-06-18): add/edit/delete/reorder fields via a Fields
      manager; types = **text, number, date, dropdown (select), labels/tags (multi),
      checkbox, url**; values render in the task dialog + as chips on cards. **Still to do:**
      formula & rollup types; show as List columns; per-field filtering/grouping; promote
      to a shared module so planner & future boards reuse it (not copy-paste).
- [ ] **ClickUp REST integration (Worker)** — read tasks by custom id (INF-xxx / TR604-xx),
      map ClickUp custom fields → our fields. Needs a ClickUp API token as a **Worker secret
      (user-set, not Claude)**. Powers Post Tracker import + post-tracker sync.

## Architecture decision — where heavy apps live & how they stay consistent

**Context:** the work-management app and whiteboard are becoming heavyweight (React/build
step, R2 file storage, real-time sync, video proofing, client sharing, an API). The hub's
own value is being a **fast static knowledge base + light dashboard**; bundling those big
apps into it would bloat builds and couple deploys/failures.

**Recommended approach (phased — separate the heavy apps, keep one identity + one look):**
1. **Keep light single-file tools in-hub** (e.g. the current Post Tracker). They're fine here.
2. **When an app needs a framework/build step** (whiteboard = Excalidraw/React; full
   work-management), give it its **own repo + own Cloudflare Worker**, on its **own subdomain**
   under `gear.lk` (e.g. `pm.gear.lk`, `board.gear.lk`). Subdomains > path-routing (cleaner
   separation, independent deploy/perf, no route-precedence headaches).
3. **One login (SSO):** put those subdomains behind the **same Cloudflare Access org** → one
   Google sign-in works across all of them. Each app's Worker verifies the same Access JWT
   (reuse the hub's existing verify code).
4. **Shared identity + data:** **bind the same D1** (`infinity-hub-authz`) to each app Worker
   (D1 can bind to multiple Workers). Users / apps / grants / tool_data are shared — no second
   user system. Extract JWT-verify + grant-check + tool_data helpers into a shared module
   (`@infinity/hub-auth`) so the logic isn't copy-pasted.
5. **Dashboard stays the launcher** — tiles already link by URL, so they point to whichever
   origin/subdomain an app lives on. No change needed.
6. **Shared "UI engine" for one consistent look:** a single **Infinity UI kit** — design tokens
   (mango/neutral palette, fonts, spacing) + base components — served from a **stable versioned
   URL** (`hub.gear.lk/assets/infinity-ui.css`) that every app links, plus a written **UI/brand
   guide** in the KB. Update the kit → every app picks it up. (Later: a component lib if apps
   share a framework.) **This should be built first**, regardless of the rest, so all apps —
   in-hub or separate — already align and future extraction is painless.

**First pilot of the pattern:** build the **whiteboard as the first separate app** (it needs
Excalidraw/build anyway) — own subdomain + Worker, bound to the shared D1, behind the same
Access, linking the shared UI kit. Proves the whole approach on a contained app before the
much larger work-management migration.

**Requires the user (Cloudflare dashboard):** create each subdomain's Worker + custom domain,
add it to the same Access application/policy, bind the shared D1. (Claude provides exact steps;
no production secrets involved — same as the hub setup.)

## In progress

- [~] **Post Tracker** (`/tools/post-tracker/`, built 2026-06-18 as the first real app) —
      Board + List + Capacity views, add/edit dialog, filters (client/designer/month/search),
      caption truncation checker. **Default view = List.** Capacity uses the **Design Weight
      System** (weighted units, 25-unit cap; videos vs 15 cap; toggle). **Custom fields** done
      (see engine above; seeded Ad Type/Tags/Reference/File Link from the ClickUp screenshots).
      Data via per-tool store. **Next layers:**
      - ClickUp import: paste INF-xxx → Worker pulls fields → exec adjusts. (needs token; **deferred — user will spec later**)
      - Caption **generate** button — needs our brand-voice rules per client (define rules first).
      - Drag-and-drop between columns; due/start dates; attachments/thumbnails.
      - Campaign Template + Variation model (1.5 + 0.5×n) as a quick-add helper.
      - Custom fields as **List columns** + filtering by them.
      - NOTE: weight values live in the tool's own data (editable); the source-of-truth pay
        doc is confidential and stays in `_private/` — never put salary figures in committed code.

## Work management / collaborative app (the full ClickUp replacement)

> **PLAN ONLY — do not build yet.** Documented from the team's current ClickUp space
> (screenshots in `_private/`, 2026-06-18). The **Post Tracker** above is the first slice
> of this. This is the big, heavyweight app — see *Architecture decisions* for whether it
> lives in-hub or as its own deployment. Build incrementally; every item is mobile-first.

### Hierarchy & structure
- **Spaces → Folders → Lists → Tasks → Subtasks**, plus **Checklists** inside tasks.
- Folders we use: one per client (TecRoot, Gearz, Cykel, Reboot) + *Old Lists*,
  *Creative Team Capacity*. Lists like `2603 GZ Mar`, `Unmade Ideas`, `Planning`, `Daily Tasks`.
- **Custom Task IDs** per list (e.g. `TR604-19`, `GZ2606-03`, `CY606-04`) — must be supported.

### Views (per list, switchable tabs)
- **List** — grouped by status, sortable columns, inline add-task. ✅ (basic version in Post Tracker)
- **Board** — Kanban by status, drag between columns. ✅ (basic)
- **Calendar** — month/week; tasks on their post/due date, colour-coded. (Post Tracker: TODO)
- **Team / Workload** — one column per assignee; per-person **Not done / Done counts +
  completion % ring + workload bar**; grouped by status. This is the live capacity view.
- **Timeline (Gantt)** — tasks across time.
- **Table** — spreadsheet view.
- **Overview / Dashboard** — composable **widget cards**: Recent, Docs, Bookmarks, Folders,
  Lists (with progress bars e.g. `1/17`, start/end/priority/owner), Resources (file drop),
  **Workload-by-status pie chart**, auto-refresh, **+ Card** to add widgets.
- **Ads** and **Content Calendar** — saved/custom views of the same data.

### Statuses (content workflow)
Backlog → Need to Shoot → Needs Revisions → In Progress → Ready for Review → Strat Review →
Approved → Scheduled → Posted, plus On Hold / Abandoned / Rejected / Done. Colour-coded,
collapsible groups with counts. (Statuses must be **editable per space**.)

### Task detail (the card)
- Custom fields panel: **Title, Type (dropdown), Post Date, Reference, Caption (long text),
  File Link (url), Ad Type (dropdown: Awareness / ADV+ Traffic / T2T2-Retention / …),
  Tags (multi-label), Category, Priority (Normal/High/Urgent), Assignee(s), Due/Start dates,
  Track time.** (Custom-field types ✅ in Post Tracker.)
- Description / "Visual Direction" rich text.
- **Attachments** with drag-drop upload + thumbnails.
- **Subtasks**, **relate items / dependencies**, **create checklist**.
- **Assigned comments** — checklist-style action items assigned to people (from review notes).
- **Activity log** + **threaded comments** with **@mentions** and **reactions**.
- AI helpers: generate/summarise subtasks, "find similar tasks".

### Collaboration & notifications
- **Daily Tasks chat channel** — standup posting (Today's Tasks / Carryovers / Blockers per
  person, tag the task to auto-pull details, urgent flag, OOO, meeting times). Work starts
  10:00 (grace 10:30), post by 10:20, standup 10:35. *(was its own backlog item)*
- **Channel** chat per space; **Notifications inbox** (Primary / Other / Later / Cleared,
  unread counts, grouped by time, per-item reply counts, filters, clear-all).
- **Share** (internal + external links), **Docs** (in-app documents with templates), **Bookmarks**.

### Reporting / capacity
- Workload-by-status pie, per-person workload %, list progress bars, **Creative Team Capacity**
  (weighted-unit tracking — already prototyped in Post Tracker → Capacity).

### Cross-cutting
- **Filters** (by list/location/field, **saved filters**), **sort**, global **search (Ctrl-K)**,
  **auto-refresh**, real-time multi-user sync (needs a sync backend — Durable Objects / D1 +
  polling; decide in architecture), per-task permissions.

### File proofing & versioning (high priority — biggest current pain) — added 2026-06-18
- **File versioning** — upload **new versions of the same file** instead of new files each
  time. Today designers re-upload and delete the old → the files panel clutters AND all prior
  comments are lost. Versions keep history + comments attached to the file, not the upload.
- **Image proofing / annotation** — open an image, **click a spot to drop a pin comment**,
  assign it to someone to resolve. Pins are numbered markers on the image (see screenshots
  303/302). Comments appear in the **activity feed** *and* a dedicated **Assigned comments**
  section; show **Resolved** once done. Resolver uploads the revised version against the same file.
- **Video proofing** — click the video to **pause + add a comment at that timestamp** (comment
  flashes ~2–3s on the frame). **Click a comment → video seeks** to it. **Seekbar shows markers**
  where comments sit; click a marker to seek (screenshot 304).
- **Compare tool** — open two files (image or video) **side by side** to compare versions/options.
- **Auto-rename on upload** → `[task code]_[Title]_[File number]_[Version].[ext]` (configurable pattern).
- **Auto-preview image** — use the **first uploaded image** as the card/thumbnail preview in
  gallery/board views.
- *Implementation note:* needs real file storage → **Cloudflare R2** (Worker-signed uploads),
  metadata in D1 (file → versions → comments[{x,y or timestamp, assignee, resolved}]).

### Codes, views & client sharing — added 2026-06-18
- **Auto task code / tag** = `[2-letter brand][last digit of year][2-digit month]-[NN]` where NN
  is the content number from `01` (e.g. `TR604-01`). Auto-increment per brand/month. Make the
  pattern configurable per brand.
- **Multiple instances of the same view type, keyed on different date fields.** We have two
  dates — **due date** and **post date**. One Calendar keyed on due date = the task calendar;
  another keyed on post date = the **content calendar**. Views must let you pick which date
  field drives them, and you can save several of the same type.
- **Granular client sharing of views** — share a **specific view** with a client (read or
  limited), scoped to what they're allowed to see.
- **Folder-level persistent share codes** — a client folder holds the current + previous two
  months' boards/lists. Share **one code for a folder view** (e.g. the content calendar);
  the client keeps using the **same link every month** — we just add/remove boards/lists in the
  folder and their view updates. (No new link per month.) Client auth = pre-shared key, separate
  from staff Cloudflare Access (ties into *Client dashboards*).

### Permissions — added 2026-06-18
- **Per-folder / per-board permissions** — only authorised people can open specific folders or
  boards (granular, *beyond* the app-level grant that gates the whole tool). Model: ACL rows
  (folder/board id → user/role → view/edit) checked in the Worker.

### Claude / API connector — added 2026-06-18
- **An API/connector so Claude can read & update tasks** (a major existing workflow — the
  founder ideates and updates tasks via Claude through ClickUp's MCP today). Build an MCP server
  / REST API over the work-management data that exposes: list/get tasks + details, create/update
  tasks & fields, move status, comment. **Crucially, expose attachments** (Claude can read the
  task's files) — ClickUp's connector currently **can't pull attachments**; ours should, so
  Claude can see a task's images/videos and make requested changes.
- Reference the existing **`content-calendar` skill** (and `post-tracker` skill) for the current
  ClickUp folder/type/field IDs and the brand content standards we'd mirror.

## Personal productivity (for the founder — "ClickUp didn't click")

- [~] **Personal planner** (`/tools/planner/`, v1 built 2026-06-18) — single-user, private
      (`key=me`). Has: **My Day** (overdue/due-today + an "All todos" tab to tackle one small
      thing at a time), **Lists**, **Board**, **Calendar** (tasks + todos on due dates),
      **Recurring** (daily/weekly/monthly with auto-*missed* + streaks). Tasks have todos
      (subtasks) with their own dates; priority; notes.
      **v2 added 2026-06-18 (GTD / time-blocking):** ✅ **Capture inbox** (quick-capture bar →
      Inbox view with triage-to-list); ✅ **1-3-5 My Day** (☀ add-to-today, big/small counter);
      ✅ **Daily review** (roll overdue/earlier-day items forward / done / drop); ✅ **time-blocking
      fields** (start time + duration) with a **Today Agenda** sub-view; task **size** (big/small).
      **Still next:**
      - **Weekly review** flow (prompted checklist) — daily done, weekly TODO.
      - **Pomodoro timer** for execution; reminders/notifications.
      - Drag-and-drop ordering; list management UI (add/rename/recolor lists).
      - **Pin a task/todo onto a whiteboard** (cross-link into planner) once the whiteboard ships.
      - Recurring instances projected into the calendar view; calendar time-grid (drag to time-block).
- [~] **Whiteboard** — `/tools/whiteboard/`, **full native app (v2) built 2026-06-18**.
      Engine (`app.js`): infinite pan/zoom world coords; SVG vector layer + HTML cards.
      **Tools** (keyboard V/S/T/R/O/L/C/P/F): select, sticky, text, rectangle, ellipse, line,
      connector, pen (smoothed), frame. **Cards:** sticky + text with **markdown**, task
      (shows subtasks, expand-to-edit writes back to Planner, add-task-from-board), image
      (paste/drag/upload → **KV**), link (URL → OG link-preview), table, timer (countdown).
      **Smart connectors** (arrow or end-to-end) that follow cards on move. **Frames** move
      children. Undo/redo, **command palette (⌘K)**, search, **minimap**, colour palette,
      **export PNG/SVG/JSON + JSON import**, **AI assist** (Workers AI: brainstorm/tasks/
      expand/summarize → drops a note). Private `key=me` data. Backend added: `/api/files`
      (KV), `/api/ai` (Workers AI), `/api/linkpreview`.
      **v3 (2026-06-18):** **R2** now used for files (account enabled it) with **Range/streaming**
      (KV kept as fallback). Added **video**, **file/PDF** (inline iframe), and **YouTube** cards;
      paste/drop any file; paste a YouTube/URL → embed. Fixed: panels toggle/close + mutually
      exclusive; **connector tool** works (drag card→card); **shapes selectable by clicking
      interior** (+ wide invisible hit-pads on lines/connectors); **frame colour** applies;
      **rich-text** now stored as HTML with a **floating format toolbar** (bold/italic/H/list,
      select-text-then-style); **curved/flowy connectors**; **middle-mouse pan**; **board
      background colour**; add-task button creates a task. AI only runs deployed.
      **Still TODO (from user's 2026-06-18 list — Excalidraw screenshots are the target UX):**
      - **Pivot to Excalidraw + move to its own repo + subdomain** ("proper app I can update
        separately"). Excalidraw gives shapes/properties-panel/opacity/layers/fonts/eraser/
        flowchart shapes for free. This is the big strategic item — see *Architecture decision*.
      - **Edit lines/connectors after placing** (drag endpoints); **text along a line/connector**.
      - **More shapes + a shape tool-group/flyout** (Photoshop-style); **flowchart shapes**.
      - **Custom colour picker + transparency/opacity** controls (have an opacity field on notes only).
      - **Properties panel** (stroke, font family/size, align, opacity, layers/z-order, duplicate).
      - **Unify task UI**: whiteboard task-edit should reuse the **Planner's** task editor so it
        shows all planner fields/features (currently a reduced modal).
      - **Board management page**: list/manage boards, **tags** to find them, **archive**, **bin**
        (deleted boards kept 30 days then purged; restore or permanently delete), **show R2 bucket
        usage**.
      - **Share a board via public link (view without login)** — needs an unauthenticated
        read-only route + share token (separate from Access). Ties into client-sharing work.
      - **Mobile**: pinch-to-zoom, collapsible toolbar, hide-able top bar.
      - Real-time collab; marquee multi-select; group/align; PDF/file thumbnails.
      **Engine note:** current build is native (zero deps, themed). Given the Excalidraw target,
      next major step is the **separate Excalidraw-based app** (own repo + subdomain, shared D1 +
      R2 + Access SSO, links the Infinity UI kit).

## Team operations

- [ ] **Daily Tasks channel** — chat-style feed to post daily tasks + morning-standup
      updates (matches the ClickUp "Daily Tasks" chat we use now: Today's Tasks / Blockers
      per person, with post codes + statuses). Feeds the standup. *(was: standup view)*
- [ ] **Content approval pipeline** — client-facing link; brand owner sees the week's posts
      (visual + caption) and taps approve / request-change. Kills the WhatsApp-screenshot loop.
- [ ] **SOP runner** — SOPs as checkable run-throughs (an instance per execution, who/when).
- [ ] **Monthly report generator** — pull ad metrics, render branded client report (page/PDF).
- [ ] **Brand asset vault** — per-client logos/colors/fonts/dos-and-don'ts, one-click copy.
- [ ] **Ad cost dashboard** — spend vs budget per client per month, alert thresholds.

## Client-facing

- [ ] **Client dashboards** — clients log in to see their analytics, ad spend, etc.
      *Needs research first.* Ideas (not decided): gate each client dashboard behind a
      **pre-shared key** (separate from staff Cloudflare Access); a **modular** layout so
      each client sees only relevant widgets (some have ads, some don't; different platforms).
      Research the right auth model (per-client token vs. Access service tokens vs. signed links).

## Bigger / integrations

- [ ] **Video chat** — embedded in the hub. First pass: integrate an existing service
      (research: Jitsi embed, Whereby embed, Daily.co, LiveKit) before considering building.
- [ ] **Knowledge base UX redesign** — the `/start/` landing should *greet with knowledge*
      and guide even a confused or brand-new employee to a starting point; current layout
      feels like an unintuitive "block." (User will add screenshots.) Sidebar now present;
      full re-think pending.

## Research notes

- **ClickUp clones / references (for the platform build):**
  - **Plane** (open-source, modern ClickUp/Jira-like; great UX reference) — github.com/makeplane/plane
  - **Focalboard** (boards + table + cards + custom fields; self-hosted) — github.com/mattermost/focalboard
  - Also: Taiga, OpenProject. *Recommendation: don't fork a whole platform — our Worker+D1
    stack wants a lightweight native build; use Plane/Focalboard as UX + data-model references.*
- **ClickUp custom field types** (to replicate in the custom-fields engine): dropdown,
  label (multi-select), text, number, date, checkbox, money, formula, rollup. Fields live
  at list/space level and appear in views/filters/grouping/reporting.

## Notes

- Stack precedent: everything fits the existing Astro + Cloudflare setup (Workers/D1/KV).
- When an idea graduates, spec it properly before building (data model, who uses it,
  **mobile flow first**).
- Production secrets (ClickUp token, any client keys) are **set by the user**, never by Claude.
