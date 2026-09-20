#!/usr/bin/env python3
"""
Normalize the mirrored docs under repos/<repo>/ so the site actually works:

  1. Add YAML front matter (title + repo) to every mirrored .md file that
     lacks it, so Jekyll renders it as a real page instead of copying it as
     a static file.
  2. Rewrite cross-document markdown links so they resolve to what the
     mirror actually contains: a link to a file that IS mirrored gets
     pointed at the mirrored (lowercased) filename; a link to a file that
     was never mirrored gets pointed at the source file on GitHub instead.
  3. (Re)generate a repos/<repo>/index.md listing the mirrored docs for
     that repo, and the document list in the root index.md.

This is idempotent and safe to re-run: it is re-run by
.github/workflows/normalize-mirrors.yml after every sync, because the sync
job in each source repo overwrites repos/<repo>/ wholesale (rm -rf + cp),
which would otherwise wipe the front matter and link fixes on every push.

Run with no arguments from the repo root.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS_DIR = os.path.join(REPO_ROOT, "repos")
GITHUB_ORG = "msfrox"

# Default branch per source repo, for the GitHub fallback link. Everything
# not listed here is assumed to default to "main" (true for every mirrored
# repo as of 2026-09-21 except Sakina).
DEFAULT_BRANCH = {
    "Sakina": "master",
}

# Any markdown link whose target isn't a scheme URL, an in-page anchor, or
# a site-absolute path is a relative reference into the source repo -- not
# just the .md ones (e.g. Prayer-Time-Site/readme.md links to `LICENSE`,
# which has no extension and 404s exactly the same way).
LINK_RE = re.compile(r"(\]\()(?!https?://|//|mailto:|#|/)([^)\s#]+)((?:#[^)]*)?)(\))")


def default_branch(repo):
    return DEFAULT_BRANCH.get(repo, "main")


def split_front_matter(text):
    """Return (front_matter_lines_or_None, body)."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :]
        end2 = text.find("\n---\r\n", 4)
        if end2 != -1:
            return text[4:end2], text[end2 + 6 :]
    return None, text


def derive_title(body, filename):
    m = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    if m:
        # Strip inline markdown emphasis/code markers for a clean title.
        title = m.group(1)
        title = re.sub(r"[`*_]", "", title)
        return title.strip()
    stem = os.path.splitext(filename)[0]
    words = re.split(r"[-_]+", stem)
    return " ".join(w.capitalize() for w in words if w)


def rewrite_links(body, repo, mirrored_basenames):
    def repl(m):
        prefix, path, fragment, suffix = m.groups()
        if path.startswith(("http://", "https://", "//", "mailto:")):
            return m.group(0)
        clean_path = path[2:] if path.startswith("./") else path
        basename_lower = os.path.basename(clean_path).lower()
        # Only treat this as "mirrored" if it's a bare filename (no directory
        # component) -- mirrored files always live flat at repos/<repo>/, so
        # a link into a subdirectory (e.g. public/data/README.md) must not
        # be matched by basename alone, or it'll collide with an unrelated
        # top-level file of the same name.
        no_dir = "/" not in clean_path
        if no_dir and basename_lower in mirrored_basenames:
            new_target = basename_lower + fragment
        else:
            branch = default_branch(repo)
            new_target = (
                f"https://github.com/{GITHUB_ORG}/{repo}/blob/{branch}/{clean_path}"
                + fragment
            )
        return prefix + new_target + suffix

    return LINK_RE.sub(repl, body)


def process_file(path, repo, mirrored_basenames):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    _front_matter, body = split_front_matter(text)
    filename = os.path.basename(path)
    title = derive_title(body, filename)
    new_body = rewrite_links(body, repo, mirrored_basenames)

    front_matter = (
        "---\n"
        f"title: {yaml_quote(title)}\n"
        f"repo: {repo}\n"
        "---\n"
    )
    new_text = front_matter + new_body
    if new_text != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        return True
    return False


def yaml_quote(s):
    if any(c in s for c in ':#"\'{}[]&*!|>%@`') or s.strip() != s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def write_repo_index(repo, repo_dir, files):
    lines = [
        "---",
        f"title: {yaml_quote(repo)}",
        f"repo: {repo}",
        "---",
        "",
        f"# {repo}",
        "",
        "Mirrored documents from this repo:",
        "",
    ]
    for fname in sorted(files):
        title = None
        fpath = os.path.join(repo_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            fm, _body = split_front_matter(f.read())
        if fm:
            m = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
            if m:
                title = m.group(1).strip().strip('"')
        if not title:
            title = derive_title("", fname)
        lines.append(f"- [{title}]({fname})")
    lines.append("")
    lines.append(f"[View this repo's docs on GitHub](https://github.com/{GITHUB_ORG}/{repo})")
    lines.append("")
    with open(os.path.join(repo_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_root_index(repos_to_files):
    lines = [
        "---",
        "title: Public Docs",
        "---",
        "",
        "# Public Docs",
        "",
        "Documentation mirrored from private repos, organized by source repo.",
        "",
    ]
    for repo in sorted(repos_to_files, key=str.lower):
        lines.append(f"## [{repo}](repos/{repo}/)")
        lines.append("")
        for fname in sorted(repos_to_files[repo]):
            fpath = os.path.join(REPOS_DIR, repo, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                fm, _body = split_front_matter(f.read())
            title = None
            if fm:
                m = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
                if m:
                    title = m.group(1).strip().strip('"')
            if not title:
                title = derive_title("", fname)
            lines.append(f"- [{title}](repos/{repo}/{fname})")
        lines.append("")
    lines.append(
        "Or link directly to a file's raw content: "
        "`https://raw.githubusercontent.com/msfrox/public-docs/main/repos/<repo-name>/<doc-path>`"
    )
    lines.append("")
    with open(os.path.join(REPO_ROOT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    if not os.path.isdir(REPOS_DIR):
        print("No repos/ directory found, nothing to do.")
        return 0

    changed = 0
    repos_to_files = {}

    for repo in sorted(os.listdir(REPOS_DIR)):
        repo_dir = os.path.join(REPOS_DIR, repo)
        if not os.path.isdir(repo_dir):
            continue
        md_files = sorted(
            f for f in os.listdir(repo_dir)
            if f.lower().endswith(".md") and f.lower() != "index.md"
        )
        if not md_files:
            continue
        mirrored_basenames = {f.lower() for f in md_files}
        repos_to_files[repo] = md_files

        for fname in md_files:
            fpath = os.path.join(repo_dir, fname)
            if process_file(fpath, repo, mirrored_basenames):
                changed += 1
                print(f"normalized {os.path.relpath(fpath, REPO_ROOT)}")

        write_repo_index(repo, repo_dir, md_files)

    write_root_index(repos_to_files)

    print(f"Done. {changed} mirrored file(s) updated; "
          f"{len(repos_to_files)} repo index page(s) and the root index "
          f"regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
