#!/usr/bin/env ruby
# frozen_string_literal: true

# Checks the BUILT site (_site/), not the markdown source -- the 2026-09-20
# mirror-link bug only showed up after Jekyll rendered a link, so a
# source-level check would have missed it. Run this after `jekyll build`.
#
# Two passes, on purpose:
#   1. Internal links: strict. Any failure fails the build (exit 1).
#   2. External links: informational only. A third-party site being flaky or
#      gone should not turn the build red -- several of this repo's own
#      GitHub-fallback links point at private repos and 404 for anyone
#      without access by design (see README's "Known limitations"), so a
#      strict external check would be permanently red and get ignored.
#
# Usage: bundle exec ruby scripts/check_links.rb [path-to-built-site]

require "html-proofer"

site_dir = ARGV[0] || File.join(__dir__, "..", "_site")
unless Dir.exist?(site_dir)
  warn "#{site_dir} does not exist -- run `jekyll build` first."
  exit 1
end

# This is a GitHub Pages *project* site (see _config.yml's own comment for
# how that was confirmed), so every root-absolute link Jekyll emits is
# prefixed with the baseurl. html-proofer resolves a root-absolute link
# against the directory it was given, so without stripping that prefix
# first, EVERY internal link would look broken -- swap it back off here
# rather than passing --root-dir tricks around.
baseurl = "/public-docs"

common_options = {
  allow_missing_href: true,
  swap_urls: { %r{^#{Regexp.escape(baseurl)}/} => "/" },
}

def run_check(label, options)
  puts "== #{label} =="
  HTMLProofer.check_directory(options.delete(:dir), options).run
  puts
  true
rescue SystemExit => e
  puts
  e.status.zero?
end

internal_ok = run_check(
  "Checking internal links (failures fail the build)",
  common_options.merge(dir: site_dir, disable_external: true),
)

external_ok = run_check(
  "Checking external links (informational only -- never fails the build)",
  common_options.merge(dir: site_dir, disable_external: false),
)

unless external_ok
  puts "(external link issues reported above -- not failing the build on them; " \
       "worth a human glance, especially anything that isn't a private-repo 404)"
end

exit(internal_ok ? 0 : 1)
