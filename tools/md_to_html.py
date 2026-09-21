#!/usr/bin/env python3
"""Render the generated Markdown documentation as HTML for GitHub Pages.

`docs/*.md` stays the source: it is what GitHub renders when someone browses the
repository, and what `build_docs.py` compares against the knowledge base.  GitHub
Pages renders none of it.  `docs/.nojekyll` turns Jekyll off, so a `.md` file is
served as a raw download, and every link from the interactive site into the
documentation used to land a reader on a text file.  This module writes the
mirror those links point at instead: `docs/read/`, one `.html` per `.md`, same
directory structure, so a relative link between two documentation pages is the
same string in both trees.

The Markdown is not arbitrary.  `build_docs.py` wrote it, so the subset is closed
and small: ATX headings, paragraphs, bullet lists, pipe tables, block quotes,
horizontal rules, HTML comments and bare anchor tags as blocks; code spans, bold,
italic, links and backslash escapes inline.  Nothing here guesses.  A construct
outside that subset raises `Unsupported`, because rendering an unknown line as a
paragraph is how a generated page starts quietly lying.

Three link classes occur, and each has one correct answer on Pages, where only
`docs/` is published:

  * another documentation page      ->  the same relative path, `.md` -> `.html`
  * a file elsewhere in the repo    ->  an absolute blob URL, since it is not deployed
  * a directory                     ->  its `index.html` inside the mirror
"""
import html
import posixpath
import re

# The same spelling as REPO in docs/lib/ui.js.  Both point a reader at the file
# a number came from; neither is fetched at runtime.
REPO_BLOB = "https://github.com/alexander-stottmeister/cft-cmi/blob/main/"

PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")


class Unsupported(Exception):
    """A Markdown construct this renderer was not told about."""


def esc(text: str) -> str:
    """Escape a text node.  Quotes are left alone; attributes use attr()."""
    return html.escape(text, quote=False)


def attr(text: str) -> str:
    return html.escape(text, quote=True)


# --------------------------------------------------------------------- inline

def _link_text_end(text: str, start: int) -> int:
    """Index of the `]` closing the `[` at `start`, or -1.  Nesting is not a
    case the generator produces, so one level is enough."""
    i = start + 1
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            i += 2
            continue
        if c == "`":
            j = text.find("`", i + 1)
            i = len(text) if j < 0 else j + 1
            continue
        if c == "]":
            return i
        i += 1
    return -1


# CommonMark's flanking rules, which decide whether a run of `*` or `_` can open
# or close emphasis.  Without them a naive scan turns the adjoints of
# `N = 1 - XX* >= 0 and 0 <= Y = Z - X Q_BB X* <= N` into an <em> and DELETES both
# stars, which is what the first version of this file shipped.
_ASCII_PUNCT = re.compile(r"[!-/:-@\[-`{-~]")


def _ws(c: str) -> bool:
    return c == "" or c.isspace()


def _punct(c: str) -> bool:
    return bool(c) and bool(_ASCII_PUNCT.match(c))


def _flanking(text: str, start: int, n: int) -> tuple:
    before = text[start - 1] if start > 0 else ""
    after = text[start + n] if start + n < len(text) else ""
    left = (not _ws(after)) and (not _punct(after) or _ws(before) or _punct(before))
    right = (not _ws(before)) and (not _punct(before) or _ws(after) or _punct(after))
    return left, right, before, after


def _can_open_close(ch: str, text: str, start: int, n: int) -> tuple:
    """Stricter than CommonMark, deliberately.

    This corpus is mathematics written as plain text, and CommonMark's flanking
    rules delete characters that carry meaning in it: `XX* >= 0 ... X* <= N` loses
    both adjoint stars, `M_*` loses four more, and `$\\|f\\|_{\\beta}$` loses its
    subscript underscores, because a delimiter next to punctuation is a legal
    opener.  GitHub renders those files exactly that badly.  Here an emphasis run
    may open only after the start of a line or whitespace, and close only before
    the end of a line, whitespace or punctuation, which is what the generator's
    own `**bold**` and `*em*` always look like and what a norm bar never does."""
    left, right, before, after = _flanking(text, start, n)
    opens = left and _ws(before)
    closes = right and (_ws(after) or _punct(after))
    if ch == "_":                     # and never inside a word
        opens = opens and (not right or _punct(before))
        closes = closes and (not left or _punct(after))
    return opens, closes


def _run_length(text: str, i: int, ch: str) -> int:
    n = 0
    while i + n < len(text) and text[i + n] == ch:
        n += 1
    return n


def _find_closer(text: str, start: int, ch: str, n: int) -> int:
    """Index of a run of `ch` at or after `start`, at least n long, that can close."""
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            i += 2
            continue
        if c == "`":
            j = text.find("`", i + 1)
            i = len(text) if j < 0 else j + 1
            continue
        if c == ch:
            m = _run_length(text, i, ch)
            if m >= n and _can_open_close(ch, text, i, m)[1]:
                return i
            i += m
            continue
        i += 1
    return -1


BARE_URL = re.compile(r"https?://[^\s<>\"]+")


def inline(text: str, link, autolink: bool = True) -> str:
    """Render one run of inline Markdown.  `link` rewrites a link target.

    `autolink` is false inside a link's own label, where a bare URL would nest
    one anchor inside another."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n and text[i + 1] in PUNCT:
            out.append(esc(text[i + 1]))
            i += 2
        elif c == "`":
            j = text.find("`", i + 1)
            if j < 0:                            # an unpaired tick is literal
                out.append(esc(c))
                i += 1
            else:
                out.append("<code>%s</code>" % esc(text[i + 1:j]))
                i = j + 1
        elif c == "[":
            end = _link_text_end(text, i)
            if end < 0 or end + 1 >= n or text[end + 1] != "(":
                out.append(esc(c))
                i += 1
                continue
            close = text.find(")", end + 2)
            if close < 0:
                out.append(esc(c))
                i += 1
                continue
            label = text[i + 1:end]
            target = text[end + 2:close]
            out.append('<a href="%s">%s</a>'
                       % (attr(link(target)), inline(label, link, autolink=False)))
            i = close + 1
        elif c in "*_":
            run = min(_run_length(text, i, c), 2)
            opens = _can_open_close(c, text, i, run)[0]
            j = _find_closer(text, i + run, c, run) if opens else -1
            if j < 0:
                out.append(esc(c * run))
                i += run
            else:
                tag = "strong" if run == 2 else "em"
                out.append("<%s>%s</%s>"
                           % (tag, inline(text[i + run:j], link, autolink), tag))
                i = j + run
        elif autolink and text.startswith(("http://", "https://"), i):
            m = BARE_URL.match(text, i)
            url = m.group(0).rstrip(".,;:!?")
            while url.endswith(")") and url.count("(") < url.count(")"):
                url = url[:-1]
            out.append('<a href="%s">%s</a>' % (attr(url), esc(url)))
            i += len(url)
        else:
            out.append(esc(c))
            i += 1
    return "".join(out)


# --------------------------------------------------------------------- blocks

HEADING = re.compile(r"^(#{1,6}) +(.*)$")
BULLET = re.compile(r"^[-*] +(.*)$")
RULE = re.compile(r"^-{3,}\s*$")
ANCHOR = re.compile(r'^<a id="[A-Za-z0-9_-]+"></a>\s*$')
ALIGN = re.compile(r"^:?-{2,}:?$")


def _starts_block(line: str) -> bool:
    s = line.rstrip()
    return bool(not s.strip() or HEADING.match(s) or RULE.match(s) or ANCHOR.match(s)
                or BULLET.match(s) or s.startswith(("|", ">", "<!--")))


def split_row(row: str) -> list:
    """Split a table row on unescaped pipes."""
    cells, cur, i = [], [], 0
    while i < len(row):
        c = row[i]
        if c == "\\" and i + 1 < len(row):
            cur.append(row[i:i + 2])
            i += 2
        elif c == "|":
            cells.append("".join(cur))
            cur = []
            i += 1
        else:
            cur.append(c)
            i += 1
    cells.append("".join(cur))
    # GFM resolves the escape at table-parse time, so `\\|` inside a cell -- including
    # inside a code span, where a backslash escape would otherwise be literal -- is a
    # pipe in the cell's text, not a delimiter.
    return [c.strip().replace("\\|", "|") for c in cells[1:-1]]


# Constructs outside the subset.  None of them occurs in what build_docs.py emits
# today, and each would be rendered wrongly and in silence if one appeared, so each
# is a hard error instead.  This is what makes the subset closed: the paragraph
# branch is the fallback for PROSE, never for an unrecognised construct.
UNSUPPORTED_LINE = [
    (re.compile(r"^\s*\d+[.)] "), "ordered list"),
    (re.compile(r"^\s*(```|~~~)"), "fenced code block"),
    (re.compile(r"^\s+[-*+] "), "nested bullet"),
    (re.compile(r"^\s*\+ "), "list with a + marker"),
    (re.compile(r"^=+\s*$"), "setext heading underline"),
    (re.compile(r"^_{3,}\s*$"), "underscore thematic break"),
    (re.compile(r"^\s*([-*_])( +\1){2,} *$"), "spaced thematic break"),
    (re.compile(r"^\s*<(?!!--)(?!a id=\")[A-Za-z!/?]"), "raw HTML block"),
    (re.compile(r"^#{1,6} .*[^\\]#\s*$"), "closed ATX heading"),
    (re.compile(r"\S {2,}$"), "hard line break"),
    (re.compile(r"[^\\]\\$"), "backslash line break"),
    (re.compile(r"``"), "doubled backtick code span"),
]
UNSUPPORTED_INLINE = [
    (re.compile(r"(?<!\\)!\["), "image"),
    (re.compile(r"(?<!\\)<https?://"), "autolink"),
    (re.compile(r"(?<!\\)<[^\s>]+@"), "e-mail autolink"),
    (re.compile(r"(?<!\\)<[A-Za-z/][A-Za-z0-9-]*[\s/>]"), "inline raw HTML tag"),
    (re.compile(r"(?<!\\)&(?:#[0-9]+|#[xX][0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);"),
     "HTML entity"),
    (re.compile(r"(?<!\\)\]\["), "reference link"),
    (re.compile(r"(?<!\\)\]\([^)]*\s"), "link target with whitespace or a title"),
    (re.compile(r"(?<!\\)\]\(<"), "pointy-bracket link target"),
    (re.compile(r"(?<!\\)~~"), "strikethrough"),
    (re.compile(r"(?<!\\)(\*\*\*|___)"), "triple emphasis"),
    (re.compile(r"(?<!^)<!--|-->\s*\S"), "HTML comment inside a line"),
]
_CODE_SPAN = re.compile(r"`[^`\n]*`")


def reject_unsupported(lines: list):
    """Raise on any construct this renderer would mis-render without noticing."""
    for n, raw in enumerate(lines, 1):
        if ANCHOR.match(raw.rstrip()):        # the one raw tag the subset allows
            continue
        for pattern, name in UNSUPPORTED_LINE:
            if pattern.search(raw):
                raise Unsupported("%s at line %d: %r" % (name, n, raw[:70]))
        bare = _CODE_SPAN.sub(lambda m: " " * len(m.group(0)), raw)
        for pattern, name in UNSUPPORTED_INLINE:
            if pattern.search(bare):
                raise Unsupported("%s at line %d: %r" % (name, n, raw[:70]))


def blocks(lines: list):
    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.lstrip().startswith("<!--"):     # generator notes, not for a reader
            j = i
            while j < n and "-->" not in lines[j]:
                j += 1
            if j >= n:
                raise Unsupported("unterminated HTML comment at line %d" % (i + 1))
            tail = lines[j].split("-->", 1)[1].strip()
            if tail:
                raise Unsupported("text after --> at line %d: %r" % (j + 1, tail[:60]))
            i = j + 1
            continue
        if ANCHOR.match(line):
            yield ("anchor", line.strip())
            i += 1
            continue
        m = HEADING.match(line)
        if m:
            yield ("heading", (len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if RULE.match(line):
            yield ("rule", None)
            i += 1
            continue
        if line.startswith("|"):
            j = i
            while j < n and lines[j].rstrip().startswith("|"):
                j += 1
            yield ("table", [l.rstrip() for l in lines[i:j]])
            i = j
            continue
        if line.startswith(">"):
            j = i
            while j < n and lines[j].rstrip().startswith(">"):
                j += 1
            yield ("quote", [re.sub(r"^> ?", "", l.rstrip()) for l in lines[i:j]])
            i = j
            continue
        if BULLET.match(line):
            j = i
            while j < n and BULLET.match(lines[j].rstrip()):
                j += 1
            yield ("list", [BULLET.match(l.rstrip()).group(1) for l in lines[i:j]])
            i = j
            continue
        if lines[i].startswith(("    ", "\t")):
            raise Unsupported("indented code block at line %d: %r" % (i + 1, lines[i]))
        j = i
        while j < n and lines[j].strip() and not _starts_block(lines[j]):
            j += 1
        yield ("paragraph", [l.rstrip() for l in lines[i:j]])
        i = j


def render_table(rows: list, link) -> str:
    if len(rows) < 2 or not all(ALIGN.match(c) for c in split_row(rows[1])):
        raise Unsupported("a pipe table without an alignment row: %r" % rows[:2])
    head = split_row(rows[0])
    if len(split_row(rows[1])) != len(head):
        raise Unsupported("alignment row has %d cells, header has %d: %r"
                          % (len(split_row(rows[1])), len(head), rows[1][:90]))
    # Structural invariant rather than a pattern: a row whose cell count differs
    # from the header's means the row was split somewhere it should not have been,
    # and the surplus or missing cell is content the reader would never see.
    for row in rows[2:]:
        got = len(split_row(row))
        if got != len(head):
            raise Unsupported("table row has %d cells, header has %d: %r"
                              % (got, len(head), row[:90]))
    if not all(r.rstrip().endswith("|") for r in rows):
        raise Unsupported("table row without a closing pipe: %r"
                          % next(r for r in rows if not r.rstrip().endswith("|"))[:90])
    aligns = ["num" if c.endswith(":") and not c.startswith(":") else ""
              for c in split_row(rows[1])]

    def cls(k):
        a = aligns[k] if k < len(aligns) else ""
        return ' class="%s"' % a if a else ""

    out = ["<table>", "<thead><tr>"]
    out += ["<th%s>%s</th>" % (cls(k), inline(c, link)) for k, c in enumerate(head)]
    out.append("</tr></thead>")
    if len(rows) > 2:
        out.append("<tbody>")
        for row in rows[2:]:
            cells = split_row(row)
            out.append("<tr>" + "".join(
                "<td%s>%s</td>" % (cls(k), inline(c, link)) for k, c in enumerate(cells)
            ) + "</tr>")
        out.append("</tbody>")
    out.append("</table>")
    return "\n".join(out)


def render_body(text: str, link) -> tuple:
    """Return (title, body html).  The title is the first level-1 heading."""
    title, out = "", []
    lines = text.splitlines()
    reject_unsupported(lines)
    for kind, payload in blocks(lines):
        if kind == "anchor":
            out.append(payload)
        elif kind == "heading":
            level, content = payload
            if level == 1 and not title:
                title = plain(content)
            out.append("<h%d>%s</h%d>" % (level, inline(content, link), level))
        elif kind == "rule":
            out.append("<hr>")
        elif kind == "table":
            out.append(render_table(payload, link))
        elif kind == "quote":
            _, inner = render_body("\n".join(payload), link)
            out.append("<blockquote>\n%s\n</blockquote>" % inner)
        elif kind == "list":
            out.append("<ul>\n%s\n</ul>" % "\n".join(
                "<li>%s</li>" % inline(item, link) for item in payload))
        elif kind == "paragraph":
            out.append("<p>%s</p>" % inline("\n".join(payload), link))
        else:                                    # unreachable; blocks() is closed
            raise Unsupported("block kind %r" % kind)
    return title, "\n".join(out)


# ----------------------------------------------------------------- link rules

def make_link(md_rel: str):
    """Rewrite a link target found in docs/<md_rel> for the mirror page."""
    here = posixpath.dirname(md_rel)

    def link(target: str) -> str:
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            return target
        path, sep, frag = target.partition("#")
        frag = sep + frag
        if not path:
            return target
        repo_rel = posixpath.normpath(posixpath.join("docs", here, path))
        if repo_rel.startswith("../"):
            raise Unsupported("link escapes the repository: %r in %s" % (target, md_rel))
        if not (repo_rel == "docs" or repo_rel.startswith("docs/")):
            return REPO_BLOB + repo_rel + frag   # not deployed to Pages
        if path.endswith("/"):
            return path + "index.html" + frag
        if path.endswith(".md"):
            return path[:-3] + ".html" + frag    # same shape in both trees
        return "../" + path + frag               # the mirror sits one level deeper

    return link


# ---------------------------------------------------------------------- shell

def shell(title: str, body: str, html_rel: str, md_rel: str = "") -> str:
    depth = html_rel.count("/")
    to_read = "../" * depth                      # root of the mirror
    to_docs = "../" * (depth + 1)                # root of docs/
    nav = [("Interactive site", to_docs + "index.html"),
           ("Documentation", to_read + "index.html"),
           ("All claims", to_read + "status.html"),
           ("Open problems", to_read + "open.html"),
           ("Notation", to_read + "notation.html")]
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; cft-cmi</title>
<meta name="description" content="{title}. Generated documentation of the cft-cmi project, rendered for GitHub Pages.">
<link rel="stylesheet" href="{to_docs}lib/site.css">
<script>try{{var s=localStorage.getItem('cftcmi-theme');if(s)document.documentElement.setAttribute('data-theme',s);}}catch(e){{}}</script>
<style>
  main.wrap {{ padding-top: .5rem; }}
  main.wrap table {{ margin: .6rem 0 1.2rem; }}
  main.wrap blockquote {{ margin: 0 0 1rem; border-left: 3px solid var(--line); padding-left: 1rem; }}
  main.wrap hr {{ border: 0; border-top: 1px solid var(--line-soft); margin: 2rem 0; }}
  main.wrap li {{ margin: .18rem 0; }}
</style>
</head>
<body>
<header class="site"><div class="wrap">
  <span class="brand"><a href="{to_docs}index.html">cft-cmi</a></span>
  <nav>
{nav}
  </nav>
  <button class="theme" type="button" hidden></button>
</div></header>
<main class="wrap">
{body}
</main>
<footer class="site"><div class="wrap">
  <p>{source}This mirror exists because GitHub Pages serves Markdown as a raw file rather than
    rendering it, and <code>docs/</code> is the only directory it publishes. Written by
    <code>tools/build_docs.py</code>; edit nothing here by hand.</p>
</div></footer>
<script type="module">
  import {{ initTheme }} from '{to_docs}lib/ui.js';
  initTheme(document.querySelector('button.theme'));
</script>
</body>
</html>
""".format(title=attr(title or "Documentation"), body=body, to_docs=to_docs,
           source=("" if not md_rel else
                   'Rendered from <a href="%sdocs/%s"><code>docs/%s</code></a>, which is the '
                   "source and is what GitHub shows when you browse the repository. "
                   % (REPO_BLOB, attr(md_rel), esc(md_rel))),
           nav="\n".join('    <a href="%s">%s</a>' % (attr(href), esc(label))
                         for label, href in nav))


def render_page(md_text: str, md_rel: str) -> str:
    title, body = render_body(md_text, make_link(md_rel))
    return shell(title, body, md_rel[:-3] + ".html", md_rel)


def plain(md: str) -> str:
    """Inline Markdown as plain text: escapes resolved, markup dropped.

    Stripping "[`*]" from the raw source instead, as the first version did, turns
    an escaped star into a stray backslash and makes a page's <title> disagree
    with its own <h1>."""
    return html.unescape(re.sub(r"<[^>]+>", "", inline(md, lambda t: t)))


def title_of(md_text: str) -> str:
    """The first level-1 heading, without inline markup.  Empty if there is none."""
    for line in md_text.splitlines():
        m = HEADING.match(line.rstrip())
        if m and len(m.group(1)) == 1:
            return plain(m.group(2).strip())
    return ""


def results_index(titles: dict) -> str:
    """The mirror needs a page at read/results/, because two documentation pages
    link to the directory and Pages does not list directories."""
    rows = "\n".join(
        '<li><a href="%s.html">%s</a></li>' % (attr(name), esc(titles[name]))
        for name in sorted(titles))
    body = ("<h1>Result pages</h1>\n"
            "<p>One page per consequential claim, %d in all, generated from the "
            "knowledge base. The same list with statuses and areas is on "
            "<a href=\"../status.html\">All claims</a>.</p>\n"
            "<ul>\n%s\n</ul>" % (len(titles), rows))
    return shell("Result pages", body, "results/index.html")
