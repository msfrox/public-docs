# Mirror audit — what the public docs site publishes (2026-11-17)

Card T2. Policy from Q9 (Shehan, 2026-11-17, took the recommendation): a user guide and a
changelog may be public; the README and backlog of a **private** repo are not. A public repo may
keep everything. **Nothing has been removed**: this file is the proposal; Shehan reads it first.

## How this was done

- Read every file under `repos/*/` on `main` (commit `90a90b3`), and each source repo's
  `.github/docs-sync.yml` and `.github/workflows/sync-docs.yml` (read-only, nothing edited).
- Repo visibility checked with `gh repo view`. Secret *names* checked with `gh secret list`
  (no values).
- Read in full: all READMEs and backlogs except Prayer-Time-Site's README. **Scanned, not read
  line by line:** `infiniboard/changelog.md` (47 KB), `infiniboard/guide.md`, and
  `Prayer-Time-Site/readme.md` (keyword scan for secrets, numbers, emails, internal hostnames).
  A reader who wants certainty on those three should skim them once.
- "Sensitive" below is my judgement. Client brand names (TecRoot, Gearz, Reboot, Cykel) are
  already shown on the public site infin8.agency, so they are rated low.

## Top findings

1. **All eight repos use the unedited template list** (changelog, README, backlog, guide), so the
   backlog and README of seven private repos are public. Only `infiniboard` has a CHANGELOG and
   GUIDE; the other seven have neither. Under Q9 their list becomes empty, and they vanish from
   the site entirely (the sync does `rm -rf` on its folder, then copies nothing).
2. **Removing files does not unpublish them.** `msfrox/public-docs` is a **public** repo. Every
   earlier version of every mirrored file stays readable in its git history and to anyone who
   cloned it. Trimming the lists stops new exposure only. Whether to rewrite history is Shehan's
   call (see Decisions).
3. **Security weaknesses stated in plain text:** infiniboard's backlog says public file reads
   (`GET /api/files/<key>`) are unauthenticated and "revisit if boards ever hold sensitive files",
   that Cloudflare Access blocks the connector, and the `ibk_` token format. Sakina's README
   documents its crypto design, that `PHONE_HASH_KEY` can't be rotated, and the names of its
   dev-only login endpoints.
4. **Personal and operational identifiers:** infinity-consultants-site backlog has a WhatsApp
   number and the old/new Cloudflare account split; Sakina's README has an admin
   phone number as an example; mysite has a SteamID and says the first Steam API
   key "was shared in a chat" and still needs rotating.
5. **A repo's own backlog contradicts the mirror:** infinity-hub's backlog says "Internal-only
   (repo root, not published to the site)" while it is on the site. It also describes the staff
   workflow and a confidential pay document (kept in `_private/`, figures not included).

## Per repo

Severity: **High** = should come off before anything else; **Med**; **Low**.

### 70-labs (private) — mirrored: readme.md, backlog.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Live URLs (`7.gear.lk`, `seventy-labs.shehan.workers.dev`), the Coach spin-out plan, "work for Infinity Media & its brands" | Low |
| backlog.md | 100+ unreleased ideas, several naming client brands and internal plans (Stock-Lookup for Gearz/TecRoot stock, ClickUp sync, "Home server dashboard — unraid stats tile (ties to your homelab)") | Med |

Recommended `files:` — nothing qualifies (no changelog or guide exists):

```yaml
files: []
```

### coach (private) — mirrored: readme.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Names the secrets the Worker accepts (`ANTHROPIC_API_KEY`, Strava, VAPID), says "Claude AI ... off by default", and describes sync-by-code. Useful to anyone probing the live site `coach.gear.lk` | Med |
| backlog.md (**not yet mirrored**) | Coach's held local `main` (11 commits ahead of origin) adds a `BACKLOG.md`. Pushing it would publish that file at once. Content is low-risk (module-split leftovers, a Playwright note), but it is a backlog | Low |

I diffed only the four mirrored filenames against `origin/main`: the README gains a link to
ROADMAP.md/DEPLOY.md and BACKLOG.md is new. The security-fix text lives in files that are **not**
mirrored (ROADMAP, ADRs, TASKS), so I found nothing in the held commits that would leak through
the sync. That is a finding about those four files, not a review of the whole 11 commits.
**Advice:** trim coach's list (or push with the mirror workflow held) *before* pushing coach.

```yaml
files: []
```

### mysite (private) — mirrored: readme.md, backlog.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Secrets table: `STEAM_API_KEY` "set — **rotate** (the first key was shared in a chat)", `SHARE_PIN` and `EMAIL` setup status, the PIN-gate design for locked shares, SteamID64 (stated public) | Med |
| backlog.md | Repeats the Steam key remark and the PIN-lock design; "Working mode" says WIP builds are deployed to the live domain as a phone test bench; unfinished personal items | Med |

```yaml
files: []
```

### Sakina (private) — mirrored: readme.md, backlog.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Full security model (AES-GCM phone storage, keyed-HMAC lookup, session design, trust engine); states `PHONE_HASH_KEY` effectively can't be rotated once real users exist; names dev-only endpoints `/api/auth/dev-login`, `/api/auth/dev-suspend`; an admin phone number given as an example (a Sri Lankan mobile, may be real); how admin access is granted (`ADMIN_PHONES` secret); SMS sender IDs; PDPA design. Also says the site is "not yet publicly promoted" | **High** |
| backlog.md | Planned moderator-role RBAC, the unfixed gap that banned users get no reason, pre-launch secret-handling and key-backup details, "prod DB was wiped" history, CI token scoping plan | **High** |

```yaml
files: []
```

### infinity-hub (private) — mirrored: readme.md, backlog.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Internal worker hostnames (`gist-proxy.shehan.workers.dev`, `sveltia-cms-auth.shehan.workers.dev`), that `hub.gear.lk` is gated by Cloudflare Access, the `/admin` login route, and the Gist-backed data sync | Med |
| backlog.md | 22 KB internal strategy: plan to replace ClickUp, staff workflow and working hours, D1 database name `infinity-hub-authz`, the shared-Access architecture, client-sharing and permission designs, client brand and folder names, the pay-weight system and its confidential source doc. States "Internal-only (not published)" but it is published | **High** |

```yaml
files: []
```

### infinity-consultants-site (private) — mirrored: readme.md, backlog.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Cloudflare account label ("infinity") and worker name `infinity-site`; deploy method; version history naming the four clients. The site itself is public, so most of this is low | Low |
| backlog.md | "_Internal-only_"; a WhatsApp number; `TODO(owner)` placeholders for the real email and phone; a note that the old test worker still serves on `ic.gear.lk` from a different Cloudflare account; owner-action list; case-study and testimonial plans needing client permission | **High** |

```yaml
files: []
```

### infiniboard (private) — mirrored: readme.md, backlog.md, changelog.md, guide.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Architecture and shared bindings (D1 `infinity-hub-authz`, R2 `infinity-hub-files`), `ALLOW_DEV_AUTH` / `DEV_EMAIL` dev-auth mechanism, fork structure | Med |
| backlog.md | **P1: Cloudflare Access blocks the live connector**, with the exact `curl` and the two possible fixes; `ibk_` token format and how it is stored; "public file reads are unauthenticated"; "Security follow-ups" (no CSP, files not scoped). A map of this app's weaknesses | **High** |
| changelog.md | 47 KB history. Keyword scan shows connector-token and Access service-token mechanics (`CF_ACCESS_CLIENT_ID/SECRET` names, no values) and `board.gear.lk`. Fine under Q9; skim once | Low |
| guide.md | End-user guide. Mentions `board.gear.lk` and how to mint a connector token. Fine under Q9 | Low |

```yaml
files:
  - source: CHANGELOG.md
    dest: changelog.md
  - source: GUIDE.md
    dest: guide.md
```

### Prayer-Time-Site (**public** repo) — mirrored: readme.md, backlog.md

| File | Finding | Sev |
|---|---|---|
| readme.md | Keyword scan only: ACJU's published contact details (public information), an unreleased design list. Nothing secret | Low |
| backlog.md | Design-pick tasks, a boundary data question. Nothing secret | Low |

The repo is public, so Q9 does not apply and the template list can stay. Recommended: leave it as
is (add nothing, remove nothing).

```yaml
files:
  - source: CHANGELOG.md
    dest: changelog.md
  - source: README.md
    dest: readme.md
  - source: BACKLOG.md
    dest: backlog.md
  - source: GUIDE.md
    dest: guide.md
```

## Decisions for Shehan

1. **Approve the lists above?** Once he does, each is applied in its own source repo, by that
   repo's session. Not done here.
2. **History.** Do the old versions need purging from `public-docs`? The realistic options are
   (a) accept it, then rotate anything real; (b) rewrite `public-docs` history with
   `git filter-repo` and force-push (a destructive step that also invalidates clones, so it needs
   his explicit yes). Ordinary deletions do not remove anything from history.
3. **Rotate or confirm** the things an outsider may already hold: the Steam API key (mysite
   says it still needs rotating), whether the phone numbers in Sakina's README and the consultants backlog are real numbers he
   wants public, and the infiniboard connector exposure (fix the Access setup so that backlog
   item stops being a live weakness).
4. **Order when applying.** Merging trimmed lists does not take effect until each repo next
   pushes to its `main`. When it does, the sync deletes that repo's folder here and the
   normaliser rebuilds the root index. Run link-check afterwards: pages that linked to
   `readme.md` or `backlog.md` of a removed repo will break, including the root `index.md`.
5. **Coach:** trim its list before the held commits are pushed, so its new BACKLOG.md never
   goes out.

## Not checked

- The three files named above were scanned, not read.
- I did not read source repos beyond the four documentation files, `docs-sync.yml` and the
  workflow, so claims about their internals come from those docs, not from code.
- I did not check whether any listed number is real or whether the Steam key was rotated.
