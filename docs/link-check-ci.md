# Link-check CI — how it works, and what it found

Away-task, 2026-09-22, `away/2026-09/public-docs-link-ci`. Task spec: add CI that builds the
site and checks the **built output** for broken links, failing on internal breaks and staying
lenient on external ones, so the class of bug fixed on 2026-09-20 (every mirrored cross-document
link 404ing, live, unnoticed) can't happen silently again.

## Where this stands (read this first if you're resuming)

**Done, all verified locally, nothing left queued:**
- `Gemfile` + `Gemfile.lock` pinning `github-pages` (the exact gem GitHub Pages' classic builder
  uses) and `html-proofer ~> 4.4.3`.
- `_config.yml`: added `url`/`baseurl` (this is a *project* Pages site, not root-served — see
  finding 2) and `jekyll-seo-tag` to `plugins:` (see finding 3, the one that mattered most).
- `scripts/check_links.rb` — internal links fail the build, external links are reported but
  never fail it.
- `.github/workflows/link-check.yml` — builds with `--safe` (matching production) then runs the
  checker.
- README updated: local preview now uses `bundle exec jekyll serve --safe`, and documents why.
- Proved the checker fails: injected a broken internal link into `repos/mysite/readme.md`,
  rebuilt, watched `check_links.rb` exit 1 and name the exact broken link, reverted, rebuilt,
  confirmed clean (exit 0) again. Diff after revert was empty (`diff` against a pre-edit backup).

**Not done / can't be done from here:**
- GitHub Actions itself was never run — no way to from this box. Everything below is "verified
  locally with the exact pinned gems," not "verified in Actions." The one thing that could still
  differ in Actions and not here: `actions/checkout`'s git remote naming (handled by setting
  `PAGES_REPO_NWO` explicitly rather than relying on remote detection — see finding 3's addendum).
- Did not attempt to fix the *content* of the 60 external-link "failures" the checker reports
  (they're expected — see "What the external report actually contains" below). Nothing to do
  there; flagging so nobody mistakes silence for oversight.

**Nothing was left mid-flight.** If this doc is being read because a resumed session picked this
back up: check `git log` on this branch first — if `.github/workflows/link-check.yml` exists and
this file's "Done" list matches what's on disk, the task is complete and this is just the record.

## What actually shipped

| file | purpose |
|---|---|
| `Gemfile`, `Gemfile.lock` | pins `github-pages` (GH Pages' exact classic-builder gem set) + `html-proofer ~> 4.4.3` |
| `_config.yml` | added `url`/`baseurl`, added `jekyll-seo-tag` to `plugins:` |
| `scripts/check_links.rb` | runs html-proofer against `_site/`: internal strict, external lenient |
| `.github/workflows/link-check.yml` | builds `--safe`, runs the checker, on push/PR/dispatch |

Run it locally:

```bash
bundle install
PAGES_REPO_NWO=msfrox/public-docs JEKYLL_ENV=production bundle exec jekyll build --safe
bundle exec ruby scripts/check_links.rb
```

## Why this took three real bugs to get working, not one script

The task said "check the built output, not the source" and "prove it can fail." Doing that
honestly — actually building the site the way GitHub Pages builds it, not just running plain
`jekyll build` — surfaced three independent, real, already-live bugs. Two of them explain why
**the production site had stopped deploying entirely three days before this task started**,
which is a bigger deal than the link-check task itself. Recording all three here because each
one would cost a fresh session real time to re-derive.

### Finding 1 — html-proofer 5.x silently checks nothing

`gem install html-proofer` gets 5.2.2 by default. Run against this site's `_site/`, it reports
`Checking 0 internal links` / `Ran on 26 files!` / **finished successfully** — on a directory
that (as shown below) actually had 71 broken links at the time. Two independent causes stack:

1. **Locale.** This container's `LANG` is unset (`POSIX`/`C`), so Ruby's default external
   encoding is `US-ASCII`. `Nokogiri::HTML5` (5.x switched to the stricter HTML5 parser) throws
   `Encoding::InvalidByteSequenceError` on the first non-ASCII byte it hits — an em dash in a
   mirrored title is enough — and html-proofer does not surface that exception; it just yields
   nothing for that file. `export LANG=C.utf8` (confirmed present via `locale -a`) fixes this
   half on its own.
2. **A concurrency bug, independent of the locale fix.** `HTMLProofer::Runner#process_files`
   (5.2.2) does:
   ```ruby
   def process_files
     loaded_files = []
     files.each do |file|
       Async do |task|
         task.async { loaded_files << load_file(file[:path], file[:source]) }
       end
     end
     loaded_files
   end
   ```
   Reproduced directly: `runner.send(:process_files).size` returns **0** even with `LANG` fixed,
   even in-process (no CLI/subprocess involved) — confirmed with `html-proofer` required at the
   exact `5.2.2` version via `gem "html-proofer", "5.2.2"`. The `Async`/`async`-gem version this
   release depends on returns before the nested `task.async` blocks finish, so `loaded_files` is
   read empty. Whatever the exact async-gem regression is, the practical fact is: **html-proofer
   5.2.2, on this box, passes on a site with 71 real broken links.** Did not chase the exact
   `async` gem version at fault — not worth it once 4.4.3 was confirmed to work correctly and
   fail correctly (see "Proof it can fail" below); a checker that can't fail is worse than none,
   so 5.x was simply ruled out rather than patched.

**Fix:** pin `html-proofer ~> 4.4.3` (the last pre-Async-rewrite major version) in the `Gemfile`.
Confirmed 4.4.3 finds real breaks (see below) and passes clean once they're fixed.

**Do not re-litigate this by upgrading html-proofer without re-running the "prove it fails" step
in this doc.** A silent-pass regression here is exactly the failure mode this whole task exists
to prevent.

### Finding 2 — the site has been serving broken root-absolute links since it started using them

`_config.yml` had no `url`/`baseurl`. This repo's GitHub Pages URL (confirmed via
`gh api repos/msfrox/public-docs/pages` → `"html_url": "https://msfrox.github.io/public-docs/"`)
means it's a **project** Pages site, served under `/public-docs/`, not at the domain root. Every
root-absolute link Jekyll emits — the cayman theme's own `/assets/css/style.css`, and every
permalink `jekyll-relative-links` rewrites a `[x](readme.md)` into (e.g.
`/repos/mysite/backlog.html`) — resolved one level too high and 404s on the *live* site, even
though `jekyll build` locally (served from `_site`'s own root) never showed it.

**Fix:** set `url: "https://msfrox.github.io"` and `baseurl: "/public-docs"` in `_config.yml`.
Confirmed both the CSS link and mirrored-doc links pick up the `/public-docs/` prefix correctly
afterward — `jekyll-relative-links`'s permalink generation already respects `site.baseurl`, no
plugin-side fix needed, just the missing config.

This is exactly the class of bug the task asked the checker to catch — and it did, the moment
the checker was pointed at a build with the correct `baseurl` (see "swap_urls" below for the one
bit of checker plumbing this required).

### Finding 3 — the actual reason the site had stopped deploying: `jekyll-seo-tag` isn't loaded without being listed, and GitHub Pages' classic build always runs `--safe`

This is the one that matters most, because it isn't hypothetical — it's why
`gh api repos/msfrox/public-docs/pages/builds` showed **three consecutive `errored` builds**
(`b7348b67`, `3b207a98`, `a76eb80` — the site's current `main` HEAD) going back to
2026-09-21T16:08, meaning **the live site has not deployed anything in over a day** and is quietly
still serving whatever the last successful build (`a1fe1c05`, 2026-09-19) produced.

Root-caused by reproducing GitHub Pages' actual build, not just `jekyll build`:

```bash
bundle exec jekyll build --safe --trace
# => Liquid Exception: Liquid syntax error (line 6): Unknown tag 'seo' in /_layouts/default.html
```

Why: `jekyll-theme-cayman`'s own `_layouts/default.html` calls `{% seo %}` (from
`jekyll-seo-tag`, one of the theme's own gemspec runtime dependencies). A gem-based theme's
runtime-dependency plugins get auto-required during a **normal** Jekyll build regardless of
`_config.yml`'s `plugins:` list — but GitHub Pages' classic/legacy builder always builds with
`safe: true`, and in safe mode `Jekyll::PluginManager#plugin_allowed?` requires the plugin's name
to appear in `site.config["whitelist"]`, a *different* key from `plugins:`. The `github-pages`
gem itself force-populates `whitelist` (to its full supported-plugin list, which does include
`jekyll-seo-tag`) via a `Jekyll::Hooks.register(:site, :after_reset)` hook — but that only fires
if `github-pages` actually got `require`d, which only happens through
`Jekyll::PluginManager.require_from_bundler`'s `Bundler.require(:jekyll_plugins)`, which only
runs if a `Gemfile` exists **in the site's own directory** naming it in that group. None of that
existed here. Separately, and this is the part that's actually load-bearing regardless of
`whitelist`: `require_gems` only requires plugins that are in `config["plugins"]` in the first
place — `jekyll-seo-tag` is in GitHub's `PLUGIN_WHITELIST` (allowed) but **not** in its
`DEFAULT_PLUGINS` (auto-activated), so it has to be requested explicitly. It never was.

**Fix:** added `jekyll-seo-tag` to `_config.yml`'s `plugins:` list, and added a `Gemfile` pinning
`github-pages` so both this repo and CI build against the exact plugin/whitelist behavior
production uses, instead of a plain `jekyll` gem that never enforces the whitelist at all and
would have hidden this forever. Confirmed fixed: `bundle exec jekyll build --safe` now completes
(`_site/index.html`'s `<title>` renders via the `seo` tag correctly), with only a benign warning
about missing GitHub API credentials for `jekyll-github-metadata` (see next paragraph).

**Local-repro-only wrinkle, not a real bug:** reproducing `--safe` locally also needs
`jekyll-github-metadata` (another `DEFAULT_PLUGINS` entry, needed by `jekyll-seo-tag` to look up
repo metadata) to know the repo's `owner/name`. On GitHub's own infra this is always supplied via
the `PAGES_REPO_NWO` environment variable; locally (and in the CI workflow, since
`actions/checkout` doesn't reliably leave an `origin` remote in the exact form this plugin wants)
it has to be set by hand: `PAGES_REPO_NWO=msfrox/public-docs`. Without it, the build fails with
*"No repo name found"* — a real Liquid Exception, but purely an artifact of not being on GitHub's
own build servers, not a site bug. The CI workflow sets this from `${{ github.repository }}`.

**This was not caused by this task's own changes.** `b7348b67` and `3b207a98` (the two commits
that started erroring) are plain docs-sync-bot commits with zero `_config.yml`/theme changes —
they branch directly off the last known-good build (`a1fe1c0`, per `git log --graph`). The
missing `jekyll-seo-tag` entry has been wrong since `_config.yml` first gained a `plugins:` list
at all (`e8477f5`, the 2026-09-20 away-task); it just hadn't broken a build until GitHub Pages
happened to queue one for a commit descended from it. **Recommend Shehan spot-check
`https://msfrox.github.io/public-docs/` after this branch merges** to confirm the live build goes
green — that can't be verified from here, since this box can't watch GitHub's own build queue
complete (`gh api .../pages/builds` only shows history, not something to poll usefully; the fix
is proven correct by exact-gem local reproduction instead).

## The checker itself

`scripts/check_links.rb`, run against `_site/` after `bundle exec jekyll build --safe`:

- **Internal links: strict.** Any `Links > Internal` failure (missing target, missing anchor
  hash) fails the build (`exit 1`).
- **External links: informational only, never fails the build.** Deliberate, per the task spec
  and confirmed necessary in practice — several of this repo's own GitHub-fallback links
  (`scripts/normalize_mirrors.py`'s design) point at **private** repos and legitimately 404 for
  anyone without access; a strict external check would be permanently red from day one and train
  everyone to ignore it.
- **`swap_urls`**, not `--root-dir` tricks: because of finding 2, every internal link in the built
  HTML is prefixed `/public-docs/...`. html-proofer resolves a root-absolute link against the
  directory it's given, so without stripping that prefix first, *every* internal link would look
  broken. `swap_urls: { %r{^/public-docs/} => "/" }` strips it before resolution. (Tried
  `--swap-urls` as a CLI flag first — it silently didn't apply under html-proofer 4.4.3's CLI arg
  parsing, both space- and `=`-separated; switched to calling the Ruby API directly, which took
  it immediately. Didn't chase the CLI parsing bug further once the API path worked.)

### What the external report actually contains

Run today, 60 external-link lines get reported (informational, doesn't fail the build):
- **GitHub-fallback links to private repos** (`normalize_mirrors.py`'s intentional design) — 404,
  expected, documented in the README's "Known limitations" already.
- **`https://fonts.gstatic.com`** (bare origin, no path) — 404, because the cayman theme links a
  font *preconnect* origin with no resource path; nothing to fix, it's not a real page.
Nothing in the current external report looks like an actual regression worth chasing further.

### Proof it can fail

```bash
# inject a broken internal link (front matter is lines 1-4; insert after it)
sed -i '4a\
\
See also [broken](totally-nonexistent-file.md).' repos/mysite/readme.md
bundle exec jekyll build --safe && bundle exec ruby scripts/check_links.rb
# => "internally linking to totally-nonexistent-file.md, which does not exist"; exit 1

# revert
git checkout -- repos/mysite/readme.md
bundle exec jekyll build --safe && bundle exec ruby scripts/check_links.rb
# => "HTML-Proofer finished successfully."; exit 0
```

Both runs done for real as part of this task (not simulated) — see the "Where this stands"
section above.

## What's unverified from here

- **GitHub Actions has never actually run this workflow.** Everything above is "reproduced
  exactly, locally, with the pinned production gems" — the strongest verification available from
  this box, but not the same as a green check on a real PR. First real push to `main` (or a PR)
  will be the first live signal.
- **Whether the live site actually redeploys and goes green after this merges** — can't be
  watched from here in a way that resolves faster than just checking
  `https://msfrox.github.io/public-docs/` in a browser after the fact.
