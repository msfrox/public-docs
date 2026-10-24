source "https://rubygems.org"

# Pin to the exact plugin/theme set GitHub Pages' classic builder uses, so a
# local `bundle exec jekyll build` (and CI) fails the same way production
# would rather than passing locally on a newer standalone `jekyll` gem that
# doesn't enforce GitHub Pages' plugin whitelist. See docs/link-check-ci.md.
gem "github-pages", group: :jekyll_plugins

# html-proofer 5.x's internal-link check silently finds zero links under
# Ruby's default US-ASCII external encoding (common on minimal containers)
# and, separately, is broken by an `async`-gem regression that makes
# `process_files` return before any file has actually loaded -- both make it
# report a clean pass on a site full of broken links. 4.4.3 is the last
# pre-rewrite release and was verified working here 2026-09-22.
gem "html-proofer", "~> 4.4.3", require: false
