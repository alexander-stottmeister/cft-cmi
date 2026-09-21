#!/usr/bin/env python3
"""Check the public surface without needing the knowledge base.

The documentation generator reads a private repository, so CI cannot regenerate
the pages.  What it can check is that the committed surface is sound: every
relative link resolves to a tracked file, nothing points into the private
companion, and the only external links are the ones we mean to have.
"""
import re, subprocess, sys
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
# alexander-stottmeister.github.io is this project's own Pages site, served from
# docs/ on the default branch.  It is live only while the repository is public.
ALLOWED_HOSTS = {"github.com", "alexander-stottmeister.github.io",
                 "creativecommons.org", "arxiv.org", "doi.org",
                 "projecteuclid.org", "orcid.org"}
# A Markdown link is `](target)`, but an ESCAPED bracket in mathematics, as in
# `\\[Phi''/Phi'\\](p_k)`, is not one: require the `]` to be unescaped.  That
# pattern is looked for in Markdown only.  An HTML page links with href and src,
# and the same mathematics reaches it as rendered text with the backslashes
# already resolved, so scanning HTML for `](...)` reports links that do not exist.
HTML_LINK = re.compile(r'(?:href|src)="([^"]+)"')
MD_LINK = re.compile(r'(?:href|src)="([^"]+)"|(?<!\\)\]\(([^)\s]+)\)')


def tracked() -> set:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
    return set(out.stdout.split())


def main() -> int:
    files = tracked()
    targets = [p for p in files
               if p.endswith((".md", ".html")) and not p.startswith("rigor/")]
    dead, untracked, external, ok = [], [], set(), 0
    for rel in sorted(targets):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8", errors="ignore")
        pattern = MD_LINK if rel.endswith((".md", ".markdown")) else HTML_LINK
        for m in pattern.finditer(text):
            raw = m.group(1) or (m.group(2) if pattern is MD_LINK else None)
            if not raw or raw.startswith(("#", "mailto:", "data:", "javascript:")):
                continue
            if raw.startswith(("http://", "https://", "//")):
                host = urlsplit(raw if "//" in raw[:8] else "https:" + raw).hostname or ""
                external.add(host)
                if host not in ALLOWED_HOSTS:
                    dead.append("%s: external host %s not in the allowed set" % (rel, host))
                continue
            target = unquote(raw.split("#")[0].split("?")[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                as_rel = resolved.relative_to(ROOT).as_posix()
            except ValueError:
                dead.append("%s: %s escapes the repository" % (rel, raw))
                continue
            if resolved.is_dir():
                ok += 1
                continue
            if not resolved.exists():
                dead.append("%s: %s does not exist" % (rel, raw))
            elif as_rel not in files:
                untracked.append("%s: %s exists but is not tracked "
                                 "(a clone would 404)" % (rel, raw))
            else:
                ok += 1

    print("  %d pages, %d links resolve" % (len(targets), ok))
    print("  external hosts: %s" % ", ".join(sorted(external)))
    for msg in dead + untracked:
        print("  BROKEN %s" % msg)
    if dead or untracked:
        print("\n%d broken link(s)." % (len(dead) + len(untracked)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
