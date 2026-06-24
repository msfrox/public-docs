# Infiniboard — the master guide

How to actually *use* Infiniboard (board.gear.lk) well — every tool, the settings that matter, and
recipes for the things you'll reach for (mindmaps, diagrams, plans). Written for anyone on the team,
no prior whiteboard experience assumed. For the technical/maintenance side see
[HANDOFF.md](HANDOFF.md) / [MAINTAINING.md](MAINTAINING.md); for driving the board with Claude see
[AI-CONNECTOR.md](AI-CONNECTOR.md).

## The 30-second model

An **infinite canvas** you draw on. Two kinds of things live on it:

- **Native shapes** — rectangles, arrows, text, frames, images. Fast, universal, the bread and butter
  of diagrams and mindmaps. Fully editable, undoable, exportable.
- **Cards** — Infiniboard's richer widgets: Markdown **notes**, **task** cards (linked to the Planner),
  **timers**, **link**/**YouTube**/**video**/**file** cards, **tables**. Use these when you want
  interactivity, not just a drawing.

Everything autosaves to your private space (you'll see "Saving… / Saved" in the menu). You can keep
many **boards** and switch between them.

---

## The toolbar (native tools)

The top toolbar — numbers are the keyboard shortcuts:

| Key | Tool | Use |
|----|------|-----|
| `1` / `V` | Selection | Select, move, resize, rotate. |
| `2` / `R` | Rectangle | Boxes (the workhorse of diagrams). |
| `3` / `D` | Diamond | Decisions / datastores. |
| `4` / `O` | Ellipse | Start/end nodes, bubbles. |
| `5` / `A` | Arrow | Connectors — **drag from one shape's edge to another to bind** them (the arrow then follows when you move either shape). |
| `6` / `L` | Line | Plain lines / dividers. |
| `7` / `P` | Draw | Freehand pen. |
| `8` / `T` | Text | Free-floating text. |
| `9` | Image | Insert an image (also: paste or drag a file in). |
| `0` | Eraser | Delete by scrubbing. |
| `F` | Frame | A named container/region — great for grouping a section (e.g. one "swimlane" or a phone screen). Frames can have a background colour. |
| — | Lasso | Free-form selection (command palette → "Lasso"). |

**Tips**
- Double-click empty canvas = quick text. Double-click a shape = edit its label.
- Hold `Space` (or scroll-wheel drag) to pan; scroll to pan, `Ctrl`+scroll to zoom.
- Select a shape and an arrow you draw from its edge snaps + **binds**.

## Infiniboard cards (the extras)

Insert from the toolbar's **"more tools"** (the extra-tools dropdown) or the shortcut:

| Shortcut | Card | What it is |
|---------|------|-----------|
| `N` | **Note** | A Markdown text card. Double-click (or Enter when selected) opens a rich editor with a formatting toolbar and a **Raw ⇄ Formatted** toggle. Supports headings, lists, tables, code blocks (syntax-highlighted), links. |
| `G` | **Task** | Pin/create a **Planner** task; the card mirrors its title/status/todos and edits write back to the Planner. |
| `I` | **Timer** | A countdown timer (start/pause/reset, +1m). |
| `Y` | **YouTube** | Paste a URL/ID → playable embed. |
| `J` | **Link** | A URL → link-preview card (title/description/image). |
| `U` | **File** | Upload one or many files (images inline-ish, videos playable, anything downloadable). |
| — | **Video** | A dedicated, aspect-correct playable video. |
| — | **Table** | A simple editable grid. |

You can also **paste**: a URL becomes a Link/YouTube card; an **image** drops straight onto the board
(`Ctrl/Cmd+V`); other files become a File card.

## Web embeds

Paste/insert any `https://` URL as an **embeddable** to show a live site in a frame (use right-click →
"Edit link" or Ctrl+K to set/change the URL). Sites that block framing (`X-Frame-Options`/CSP) won't
load — that's the remote site's choice.

---

## Styling — the properties panel

Select something and the left panel shows its style. Key controls:

- **Background** — fill colour. Click the swatch for the full picker: a **Palette** tab and a **Custom**
  tab with a draggable colour square + hue strip. (In dark mode the picker shows the colour as it will
  actually appear on the canvas.)
- **Stroke** — the outline/border colour (and, for plain text/shape labels, the text colour).
- **Fill style** — hachure / cross-hatch / solid. **Stroke width / style** — thin→bold, solid/dashed/dotted.
- **Edges** — sharp or rounded corners. **Opacity** — transparency.
- **Font family / size** — for text elements.
- **Frames** show a Background swatch + fill style (the fill renders *behind* the frame's children and
  inverts correctly in dark mode).

### Notes have their own format controls
With a note selected, the panel shows **Format note**: **Text font** (22 bundled families), **Text
colour** (a dedicated picker — separate from the shape Stroke), and **Text size**. The note's
background comes from the element's Background swatch. Note text auto-inverts with light/dark.

**Shape label colour** is now independent of Stroke: select a shape that has a label and the panel
shows a separate **Text** colour picker (next to Stroke/Background). Changing **Stroke** affects only
the outline; **Text** sets the label colour.

---

## Boards, sharing, view

**Boards** (hamburger menu, top-left):
- Switch with the dropdown; **+ Board** to create.
- **Manage boards** — rename, tag, **archive**, **bin** (30-day retention, then auto-purged),
  **delete forever**, and see per-board element/media/storage counts. Garbage collection frees R2
  storage for files no longer referenced when you open this panel.

**Share** (menu → Share board) — creates a public, read-only link (`board.gear.lk/share?t=…`) that
renders the board without a login (media included). Delete the link any time to revoke.

**View**
- `M` toggles the **minimap** (click/drag it to navigate; drag its corner to resize).
- Theme toggle (light/dark) and **Canvas background** colour are in the menu.
- **Fit to content**, **grid**, **zoom** controls available (zoom bottom-left).
- **Command palette**: `Ctrl/Cmd+K` — search every action.

**Export / import** (menu)
- **Save as image** (PNG/SVG) — bundled fonts are embedded so exports look right offline.
- **Export** / **Load scene** — read/write the `.excalidraw` file format.
- **Import diagram (Claude)** — open a Claude-authored diagram: an Infiniboard *SceneSpec* (`nodes`/
  `cards`) or an `.excalidraw` scene. This is how you bring a board Claude drew for you onto the canvas
  (see [AI-CONNECTOR.md](AI-CONNECTOR.md) and the `infiniboard-board` skill).

**AI assist** (menu) — summarize the board's contents into bullets (Workers AI).

**Connect to Claude** (menu → "Connect to Claude (token)") — mint a personal token so Claude can read
and draw on your live board via the MCP server. Setup + usage in [AI-CONNECTOR.md](AI-CONNECTOR.md) §4.

---

## Keyboard shortcuts cheat-sheet

`1`–`0` tools · `V` select · `F` frame · `M` minimap · `Ctrl/Cmd+K` command palette · `N` note ·
`G` task · `I` timer · `Y` YouTube · `J` link · `U` upload · `Enter` edit selected note ·
`Ctrl/Cmd+Z` undo · `Ctrl/Cmd+D` duplicate · `Ctrl/Cmd+C/V` copy/paste · `Del` delete ·
`Ctrl/Cmd`+scroll zoom · `Space`-drag pan.

---

## Recipes (mapped to real work)

**Mindmap / brainstorm** — Start with one central idea (a coloured rectangle), branch out with arrows
to child boxes. Or have Claude draft the skeleton (`layout:"tree"`) and you expand it. Use frames to
group themes; sticky notes (`#fff9b1`) for loose thoughts.

**Flowchart / process / SOP** — Rectangles = steps, diamonds = decisions, arrows = flow (label the
branches "yes/no"). Lay stages out in **columns**. Frames make clean swimlanes. Great for documenting
a process before writing the SOP.

**System / app architecture** — Boxes = components/services, diamonds = datastores, arrows = data flow
(label with the call/protocol), dashed arrows = async. Keep one frame per layer (client / Worker /
data). This is exactly what "explain how our app works" produces — and you can edit it and send it
back to Claude to update docs or code.

**Org chart / company structure** — `layout:"tree"` from a root (CEO) → departments → functions
(hiring, capacity, SOPs, budget). Expand into a full plan, then have Claude turn branches into hiring
plans / SOP docs / budgets.

**Plan / roadmap / content calendar** — **Columns** per phase or week; cards (notes/tasks) for items;
link task cards to the Planner so the board and your task list stay in sync. Export the final structure
to drive the actual tasks (e.g. into ClickUp via the content-calendar skill).

**Wireframe / UI sketch** — Frames as screens; rectangles/text/images as UI; arrows for navigation.

---

## Gotchas & good habits

- **It autosaves**, but watch the "Saved" indicator before closing on a flaky connection.
- **Bind your arrows** (draw from a shape's edge) so they stay attached when you rearrange.
- **Copy/paste & duplicate** (`Ctrl/Cmd+C`/`V`/`D`) work for shapes *and* cards now — a duplicated or
  pasted card is an **independent copy** (edits don't leak to the original), and cards survive
  copy/paste across boards and export/import.
- **Paste an image** with `Ctrl/Cmd+V` to drop it straight on the board (single copy, auto-uploaded).
- **Library** (the panel on the right) — your saved/custom stencils now **persist** across reloads.
- Big boards stay snappy because heavy tooling (Mermaid/diagram libs) loads only when used; media is
  offloaded to storage automatically.
- On mobile, the same tools live in the bottom island and the "more tools" menu; the minimap moves to
  the top-right.
