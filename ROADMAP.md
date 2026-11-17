# public-docs — roadmap

The public mirror at https://msfrox.github.io/public-docs. Eight source repos push selected
docs here through their own `.github/workflows/sync-docs.yml`; this repo normalises and
publishes them. `README.md` explains the mechanism. This repo is small, so the tracker, the
cards and the resume block all live in this one file.

**Triage, sprint S16 (2026-11-16): keep.** It is live, automated and in use.

## Shipped

- [x] Mirror, normaliser, link-check CI; Pages build repaired (2026-09)

## Phase H — housekeeping (planned 2026-11-16, sprint S16)

| ID | Card | Model | Status |
|---|---|---|---|
| T1 | Tighten `.gitattributes` to force LF | Sonnet | done 2026-11-17 (`90a90b3`) |
| T2 | Audit what each source repo publishes | Sonnet | done 2026-11-17 (`63697ff`); audit awaits Shehan's read, nothing removed |
| T3 | Record the sync token: owner, scope, expiry | Sonnet | done 2026-11-17 (`6c58877`); expiry marked "Shehan to supply" |

## Resume

**Model: Sonnet 5.5. Effort: medium.** T1–T3 are done and committed locally on `main`; **nothing is pushed** (a push to `main` publishes the site, and the repo is public).
Waiting on Shehan: (1) read `docs/mirror-audit-2026-11.md` and approve or change each repo's proposed `files:` list; (2) decide whether old versions need purging from this repo's history; (3) supply the `DOCS_SYNC_TOKEN` expiry (README, "Sync token"); (4) say when to push.
After he approves: applying each list is a follow-up in that source repo, by its own session. Coach's list should be trimmed before coach's held commits are pushed. Then run link-check here, since pages linking to removed `readme.md`/`backlog.md` will break.
Note: the audit is excluded from the Pages build in `_config.yml`, but pushing it still puts its text in a public repo. Decide before pushing.

## Cards

### T1 — Force LF line endings                     [Sonnet] · effort medium · ~10 min
Why: `.gitattributes` here says `* text=auto`, which normalises what is committed but lets a checkout on another system write CRLF. The other repos are getting `* text=auto eol=lf` (S16-PLAN § Line endings); this one should match.
Do: change the line to `* text=auto eol=lf`, run `git add --renormalize .`, commit.
Done when: `git ls-files --eol | grep -cE 'i/crlf|w/crlf'` prints 0 and the Pages build and link check stay green.
Don't: touch `repos/**` by hand; the sync overwrites it.

### T2 — Audit what each source repo publishes        [Sonnet] · effort medium · ~45 min
Why: every source repo copied the same template `docs-sync.yml`, which lists `CHANGELOG.md`, `README.md`, `BACKLOG.md` and `GUIDE.md`. So the README and the idea backlog of **private** repos (70-labs, coach, mysite, Sakina, infinity-hub, infinity-consultants-site, infiniboard) are on a public site, chosen by a template and not by a decision. Nobody has checked them for client names, internal URLs or security notes.
Context to read: `README.md` here; each source repo's `.github/docs-sync.yml`; `repos/*/` here.
Do: read every mirrored file and list, per repo, anything that should not be public (client names, staff names, internal hostnames, account ids, security weaknesses, unreleased plans). Write the findings to `docs/mirror-audit-2026-11.md` with a recommended `files:` list per repo. Rule (Q9, Shehan 2026-11-17, took the recommendation): a user guide and a changelog may be public; a backlog and a README of a private repo are not.
Done when: the audit file exists with one section per mirrored repo and a proposed `docs-sync.yml` for each; nothing has been removed yet.
Don't: edit other repos' `docs-sync.yml` or delete mirrored files in this card. Applying the lists is a follow-up in each source repo, owned by that repo's session, after Shehan has read the audit.

### T3 — Record the sync token                     [Sonnet] · effort medium · ~15 min
Why: all eight source repos push here with a `DOCS_SYNC_TOKEN` secret. If it is a personal access token with an expiry, every sync fails silently on the same day. Nothing written down says what it is.
Do: add a "Sync token" section to `README.md`: where the secret is set (list the repos with `gh secret list -R msfrox/<repo>`), what scope it needs (contents write on this repo only), and its expiry date, which Shehan reads from GitHub settings. Recommend a fine-grained token limited to this repo.
Done when: README has the section and the expiry date is filled in or marked "Shehan to supply".
Don't: print, rotate or create a token.
