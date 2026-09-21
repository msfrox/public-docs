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
3. `_config.yml` sets `defaults: layout: default` for all pages and enables the
   `jekyll-relative-links` plugin (on GitHub Pages' safe-mode whitelist, so it works on Pages'
   own classic build without needing a custom Actions-based Pages deploy) to turn `[x](readme.md)`
   into a link to the page's real permalink (`readme.html`).

Re-run the normalizer locally any time with `python3 scripts/normalize_mirrors.py` from the repo
root — it's idempotent.

## Local preview

```
gem install --user-install jekyll bundler jekyll-theme-cayman jekyll-relative-links
export PATH="$HOME/.local/share/gem/ruby/3.1.0/bin:$PATH"   # or wherever `gem env gempath` says
jekyll serve -H 0.0.0.0
```

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
