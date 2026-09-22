# public-docs

Jekyll (cayman theme) site, published on GitHub Pages, that mirrors selected docs out of
Shehan's other repos into `repos/<repo-name>/`.

## How a doc gets here

1. Each source repo has `.github/workflows/sync-docs.yml` + `.github/docs-sync.yml`. On push to
   its own main branch, it copies the files listed in `docs-sync.yml` into
   `repos/<repo-name>/` here (destination filenames are lowercased by convention, e.g.
   `README.md` -> `readme.md`) and pushes straight to this repo's main branch. That sync is a
   dumb `rm -rf + cp` — it does **not** touch front matter or rewrite links.
2. `.github/workflows/normalize-mirrors.yml` in *this* repo runs on every push that touches
   `repos/**` and calls `scripts/normalize_mirrors.py`, which:
   - adds YAML front matter (`title`, `repo`) to every mirrored file, so Jekyll actually renders
     it as a page instead of copying it verbatim as a static file;
   - rewrites relative links so they resolve to what the mirror actually contains — a link to a
     file that *is* mirrored gets pointed at the mirrored (lowercased) filename; a link to a file
     that was never mirrored gets pointed at that file on GitHub instead;
   - regenerates `repos/<repo-name>/index.md` and the document list on the root `index.md`.

   This has to live here rather than in each source repo's sync-docs.yml because the sync step
   only knows about one repo at a time and has no way to know what got lowercased or omitted on
   the mirror side; and it has to re-run on every sync rather than being a one-off hand-edit,
   because step 1 overwrites `repos/<repo-name>/` wholesale on every push from that repo.
3. `_config.yml` sets `defaults: layout: default` for all pages, sets `url`/`baseurl` to match
   where this actually lives (`https://msfrox.github.io/public-docs` — a *project* Pages site,
   not a user/org site or custom domain, so it is not served at the domain root), and enables the
   `jekyll-relative-links` and `jekyll-seo-tag` plugins (both on GitHub Pages' safe-mode plugin
   whitelist, so this works on Pages' own classic build without needing a custom Actions-based
   Pages deploy). `jekyll-relative-links` turns `[x](readme.md)` into a link to the page's real
   permalink (`readme.html`); `jekyll-seo-tag` has to be listed explicitly even though nothing
   here calls it directly, because the cayman theme's own layout does (`{% seo %}`) — see
   `_config.yml`'s comment and `docs/link-check-ci.md` for how big a deal that turned out to be.

Re-run the normalizer locally any time with `python3 scripts/normalize_mirrors.py` from the repo
root — it's idempotent.

## Local preview

```
bundle install
PAGES_REPO_NWO=msfrox/public-docs bundle exec jekyll serve -H 0.0.0.0 --safe
```

`--safe` matters: it's the only way to reproduce GitHub Pages' own plugin whitelist locally (see
`docs/link-check-ci.md`) rather than a looser build that passes here and fails on Pages. Because
`baseurl` is set, the site is served under `/public-docs/`, e.g.
`http://localhost:4000/public-docs/` — matching production rather than `jekyll serve`'s bare
root. `PAGES_REPO_NWO` stands in for the repo-name auto-detection GitHub's own builder does; the
build works without it too, just with a lint warning about missing GitHub metadata.

## CI: link checking

`.github/workflows/link-check.yml` builds the site exactly as above and runs
`scripts/check_links.rb` (html-proofer) against the **built HTML**, not the markdown source —
the 2026-09-20 mirror-link bug (every cross-document link 404ing) only became visible after
Jekyll rendered a link. A broken internal link fails the build; a broken external link is only
reported, never fails it (several of the GitHub-fallback links below point at private repos and
404 for anyone without access, by design). See `docs/link-check-ci.md` for the full writeup,
including a real production outage this work found and fixed along the way (the site's own
GitHub Pages build had been failing since 2026-09-21).

## Known limitations

- The GitHub fallback links assume the source repo's default branch (hardcoded per-repo in
  `scripts/normalize_mirrors.py`'s `DEFAULT_BRANCH` map; everything not listed there defaults to
  `main`). They also point at *private* repos, so a visitor without access will hit a normal
  GitHub 404/permission page rather than the doc — that's expected, not a bug.
- The GitHub-fallback rewrite fires for any non-absolute markdown link target (not just `.md`),
  so it also covers things like `[LICENSE](LICENSE)`. It's a text substitution, so a target that
  happens to share a mirrored file's basename but lives in a subdirectory (e.g.
  `public/data/README.md` vs. the mirrored top-level `readme.md`) is correctly told apart by
  checking for a `/` in the link path — don't simplify that check away.
