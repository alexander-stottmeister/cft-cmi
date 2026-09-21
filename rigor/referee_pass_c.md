# REF-PASS-C: third pass on the five infrastructure cards (2026-09-21)

Scope: `generated-docs`, `public-site-plan`, `repo-split-public-private`, `ci-green`,
`docs-pages-rendering`, against the three prior notes `referee_ci_pages.md` (REF-CI-PAGES),
`referee_ci_pages_b.md` (REF-CI-PAGES-B) and `referee_plan_split.md` (REF-PLAN-SPLIT).

Verdicts: **`docs-pages-rendering` FAIL, `generated-docs` FAIL, `repo-split-public-private` FAIL;
`ci-green` PASS, `public-site-plan` PASS.**

Everything marked [C] is measured by me at HEAD = `6100643`, with the working tree clean before and
after every test (`git status --porcelain` empty, checked after each; the three planted files for
the drift-guard test were restored by file copy, not by git). No git command that writes was run;
`git fetch` was therefore *not* used for §3 — the remote probes are REST only, which is a strictly
weaker instrument and still sufficient. Two new instruments this pass:

* **GitHub's own renderer.** `gh api /markdown --mode gfm` renders a string with GFM. I used it to
  settle the emphasis question against GitHub itself rather than against a reading of the spec.
* **The events API.** `/repos/{owner}/{repo}/events`, which turns out to matter in §3.

---

## 1. `docs-pages-rendering` — **FAIL**

### 1.1 The REF-CI-PAGES-B findings

| finding | state now [C] | verdict |
|---|---|---|
| **B1** "THE SUBSET IS CLOSED" is false and escalated | withdrawn. The card now opens the paragraph "THE SUBSET IS NOT CLOSED, and the card said the opposite twice", calls `reject_unsupported()` a blacklist and "a guard, not a proof", lists what it now raises on and lists what is still silently wrong | **REPAIRED in substance** — but the list is wrong in three places, see C4/C5 |
| **B2** the `_` repair broke four LaTeX sites (`notation.md:89,90,109`, `definitions.md:93`), 8 underscores deleted | all four intact. `docs/read/notation.html:98,99,114` read `$\|f\|_{\beta}=\sum_{n}…`, `$\|G\|_{3/2}^{2}=\int_{\mathbb R}…`, `…\|_{\mathfrak S_{2}}^{2}…`; `docs/read/definitions.html:100` reads `k_{s}\|_{A}=\mathrm{id},\qquad k_{s}(x)…` | **REPAIRED** |
| **B3** `M_*` at `history.md:147,148` still lost six asterisks | `grep -c '<em>' docs/read/history.html` = **0**. Both lines carry all five and both stars respectively | **REPAIRED, and the class not the instance** |
| **B4** "the Pages address four times, three in the intro and one in section 9" | card now says "six times, three in the introduction (lines 27, 33, 34) and three in section 9 (339, 340, 341)". `grep -n github.io README.md` gives exactly those six lines; `## 1.` is line 42, `## 9.` is 309, `## 10.` is 352 | **REPAIRED, exact** |
| **B5** the two-condition publishing claim | card, README:34-38 and `.github/workflows/check.yml:59-65` all now say **three**: public, `if: false` removed, Pages enabled once. `with: { enablement: true }` is reverted (`git diff b9daa45 HEAD -- .github/workflows/check.yml`). See §5 | **REPAIRED** |
| **B6 / B-R8** "check_links 155 pages and **2210** links resolve" in How to verify | `make check` at HEAD prints **`155 pages, 2211 links resolve`**. The card still says 2210 | **NOT REPAIRED** |
| **B-R8, second half**: the module docstring of `tools/md_to_html.py` still carries three sentences the card has corrected | still uncorrected, and now contradicted harder. Lines 5-7 "`docs/.nojekyll` turns Jekyll off, **so** a `.md` file is served as a raw download"; lines 10-11 "a relative link … is the **same string** in both trees"; line 13 "the subset **is closed** and small"; line 17 "A construct outside that subset raises `Unsupported`". And `md_to_html.py:240-242`, untouched by this commit, still reads "**This is what makes the subset closed**: the paragraph branch is the fallback for PROSE, never for an unrecognised construct" | **NOT REPAIRED** |

### 1.2 Emphasis: what I measured

**(a) The B2 and B3 sites.** Intact, as tabled above.

**(b) Nothing that should be emphasised stopped being.** `docs/read/` holds 66 HTML files at
`b9daa45` and 66 at HEAD; `diff -rq` over the two trees shows exactly **five** differing files, so
61 of 66 pages are byte-identical and their rendered text cannot have moved. The five, every
difference accounted for:

| page | difference | cause |
|---|---|---|
| `definitions.html:100` | `k_{s}\|<em>{A}=…k</em>{s}(x)` → `k_{s}\|_{A}=…k_{s}(x)` | B2, intended |
| `notation.html:98,99` | two subscript pairs restored | B2, intended |
| `notation.html:114` | one subscript pair restored | B2, intended |
| `history.html:136,137` | six asterisks restored, two `<em>` gone | B3, intended |
| `sources.html:59` | the Project Euclid URL became `<a href=…>` | bare-URL autolink, intended |
| `status.html:249,251` | two `review pending` cells | `docs/status.md` changed in the same commit; not the renderer |

Tag counts over all 66 pages: `<em>` 57 → **50** (the seven above), `<strong>` 366 → **366**,
`<a href` 1303 → **1304** (the one autolink). No emphasis was lost anywhere.

Independently, I patched a copy of `md_to_html.py` back to the CommonMark `_can_open_close` of
`b9daa45` and rendered all **65** sources under both rules. Exactly **3** pages differ
(`definitions`, `history`, `notation`) and in every case the strict rule is the one that is right.
There is no site in the corpus where CommonMark emphasises and the strict rule does not.

**(c) The generator's own markup.** `**bold**`, `*em*` and `_italic_` all still render:
`**bold** x`, `a *em* b`, `_None recorded._` (27 result pages), `see _no result recorded in the
table_ here` (7 sites on `sources.html`), `**b**.`, `tail *em*`, `*em*, tail`,
`**the N rows of [`a`](b.md)**. rest` (closer after `)`, opener after a space), `[**bold**](x.md)`
(label passed to `inline()` at index 0), and `| **total** | **7** |` in a table cell — all correct.
**After an opening parenthesis they do not**: `(**bold**) tail` → `(**bold**) tail`,
`(*em*) tail`, `(_em_) tail`, `"**bold**" tail`, `word—**bold**`, `co-**bold**` all stay literal.
This does not bite today: `grep -rE '\([*_]{1,2}[^ *_]' docs/*.md docs/results/*.md` returns **0**.

**(d) Does the strict rule lose emphasis GitHub would show?** Yes, out of corpus; no, in it.
Measured with `gh api /markdown --mode gfm`:

| input | GitHub | mirror |
|---|---|---|
| `(**bold**) tail` | `(<strong>bold</strong>) tail` | literal |
| `*em*s tail` | `<em>em</em>s tail` | literal |
| `lambda_min(M_*)/g_Q … \|\|M_*\|\|` | `lambda_min(M_<em>)/g_Q … \|\|M_</em>\|\|` — **GitHub deletes the stars** | keeps them |
| `$\|f\|_{\beta}=\sum_{n}…$` | `$\|f\|<em>{\beta}=\sum</em>{n}…$` — **GitHub deletes them** | keeps them |

So the card's "GitHub renders those files exactly that badly" is not an argument from the spec; it
is now a measurement against GitHub's own renderer. I then rendered **all 65 sources** through
`gh api /markdown` and compared the whitespace-stripped character stream with the mirror's:

* 58 of 58 result pages: **character-identical**.
* `index.md`, `open.md`, `sources.md`, `status.md`: **character-identical**.
* `history.md`: 6 differing characters — six `*` the mirror keeps.
* `notation.md`: 6 differing characters — six `_` the mirror keeps (plus a `&lt;`/`&gt;` artefact of
  GitHub's `<math-renderer>` double-escaping inside `$…$`, not a Markdown difference).
* `definitions.md`: 2 differing characters — two `_` the mirror keeps.

**Fourteen characters over 65 pages, every one of them the mirror being right.** The card's
sentence "the divergence is confined to emphasis" is exact, and stronger than it claims.

### 1.3 The twenty constructs of B1, re-run

Through `render_body` with the real `make_link`.

**Now raise (15 of the 20, plus 5 of the six "near neighbours" B1 named):** HTML entities
(`&copy;`, `&#189;`, `&lt;`, including in a table cell); mid-line raw HTML (`a <b and c`,
`x<sub>2</sub>`, `One<br>Two`); a row whose trailing bar is missing (`table row has 1 cells,
header has 2` — the destructive case); adjacent backticks `` `a``b` ``; a code span containing a
backtick ``` ``a ` b`` ```; a link target with a space or a single- or double-quoted title; a
pointy-bracket target; `___`; `___foo___`; `* * *` and `- - -`; a backslash hard break; `1) one`;
`before <!-- x --> after`. Plus every other entry the card enumerates: `1.`, fences, nested
bullets, `+` lists, setext `=`, block/inline raw HTML, closed ATX, two-space break, images, `<>`
autolinks, e-mail autolinks, reference links, `~~`, `***`, indented code (spaces **and** tab), a
table with no alignment row, a target escaping the repository, an unterminated comment, text after
`-->`.

**Now correct:** the bare URL (`See https://example.com/x.` → a link, trailing stop stripped);
`*foo\nbar*`; `\*a* b`; a heading with one trailing space.

**Still silently wrong, and listed by the card:** a table with no leading bars; a row without a
leading bar inside a table (table truncated, row becomes a paragraph); lazy blockquote
continuation; balanced parentheses in a link target (`[t](results/f(1).md)` →
`href="../results/f(1"` plus a literal `.md)`).

**Still silently wrong and NOT listed** — see C4 and C5 below.

### 1.4 The structural invariant, attacked

`render_table` raises when a body row's cell count differs from the header's, and when any row
lacks a closing bar. I could not defeat the destructive cases:

| attack | result |
|---|---|
| `\| c \| d` (no trailing bar) | RAISE, 1 vs 2 |
| `\| c \| d \| e \|` (surplus) | RAISE, 3 vs 2 |
| `\| c \| d \|\|` (empty last cell) | RAISE, 3 vs 2 |
| a bare bar inside a code span in a cell | RAISE, 3 vs 2 |
| a cell whose content ends in a bar inside a code span | RAISE, 3 vs 2 |
| header of one cell, body `\| a\|b \|` | RAISE, 2 vs 1 |
| trailing spaces after the closing bar | RAISE (hard line break) |
| escaped bar `\|` in a cell | correct, 2 cells |
| **compensating split** `\| p\|q \| r \|` in a 3-column table | accepted — but this is exactly what GFM does with an unescaped bar, so the mirror and GitHub agree and nothing is dropped. Not a defeat |
| **the alignment row** | **DEFEATED** — see C5 |

### 1.5 The two hardened helpers

`_escape_bare_pipes` (`build_docs.py:988`) is correct on every input I could construct. It counts
the backslash run and escapes only when the run is even: `a|b`→`a\|b`, `a\|b`→unchanged,
`a\\|b`→`a\\\|b`, `a\\\|b`→unchanged, `a\\\\|b`→`a\\\\\|b`, `\\\\|x|y`→`\\\\\|x\|y`. B-note's
lookbehind hole is closed.

`pipes_in_code_spans` (`build_docs.py:808`) fixes the odd-backtick hole — `| \`a | b |` returned
`[]` (the whole row silently empty) at `b9daa45` and now returns 2 cells, which is what GFM gives —
**and introduces a new one of the same family.** See C1.

### 1.6 Bare-URL autolinking

Fires correctly: after a space, at the start of a line, inside a table cell, after `(`. Never
inside a code span (the backtick branch consumes the span first). Trailing `.,;:!?` stripped;
`(see https://ex.com/x). rest` keeps the stop and the parenthesis outside; a balanced
`https://en.wikipedia.org/wiki/A_(b)` keeps both parens; `&` is attribute-escaped.
`docs/sources.md:25` is now `<a href="https://projecteuclid.org/…">` at `docs/read/sources.html:59`,
and `check_links` sees the new host: `external hosts: alexander-stottmeister.github.io, github.com,
projecteuclid.org`. **But "never inside a link label" is false** — see C2.

### 1.7 New findings

**C1 — `pipes_in_code_spans` DOUBLE-ESCAPES an already-escaped bar inside a code span. BLOCKING as
a claim; latent as an effect.**

The new branch takes the whole span and runs `.replace("|", "\\|")` on it, without looking at the
backslashes inside. An escaped bar in the source therefore becomes `\\|` — an escaped backslash
followed by a live delimiter, which is *precisely* the shredding bug `_escape_bare_pipes` was
written to fix in the sibling function, in this same commit. Measured, old against new:

```
| `a\|b` | c |     b9daa45 -> '| `a\|b` | c |'      cells ['`a|b`', 'c']        (2, correct)
                   HEAD    -> '| `a\\|b` | c |'     cells ['`a\\', 'b`', 'c']   (3, shredded)
```

GitHub renders the source as 2 cells with `<code>a|b</code>` (measured). The card says both latent
bugs are "fixed … both now count the backslashes or find the closing tick": the closing tick is
found, the backslashes are not. It fails closed downstream — the new cell-count invariant raises
and `build_docs` has no `except Unsupported`, so the build dies rather than writing a corrupt page
— but `make docs` and `make check` would then be red with a traceback and unfixable from the
generator. Not live: no `rigor/PHASE*_STATUS.md` row (29 rows, all in PHASE5) carries `\|` inside a
code span. Fifteen lines in `rigor/*.md` do, eight of them in `referee_ci_pages_b.md` — the same
one-file distance B-note recorded for the bug this replaces.

**C2 — "bare URLs are now linked, and never inside a link label" is false. The `autolink` flag does
not survive the emphasis recursion.**

`inline()` passes `autolink=False` into a link's label (`md_to_html.py:181`), but the emphasis
branch at `:194` calls `inline(text[i + run:j], link)` with no `autolink=` argument, so it resets to
the default `True`. Measured:

```
[*see https://example.com/x*](a.md)
  -> <a href="a.html"><em>see <a href="https://example.com/x">https://example.com/x</a></em></a>
[**https://example.com/x**](a.md)
  -> <a href="a.html"><strong><a href="…">…</a></strong></a>
```

A nested `<a>` inside an `<a>`, which is invalid HTML and which the flag exists to prevent. Latent:
of the 783 link labels in the 65 sources, 0 contain a URL (239 contain an unescaped `*` or `_`).

**C3 — "a comment opened … inside a line" does not raise when a space precedes it, and the reader
sees the comment.** The guard is `\S<!--|-->\s*\S`. Measured:

```
x<!-- c --> y      RAISE  (\S before <!--)
a <!-- c --> b     RAISE  (\S after -->)
text <!-- note -->   OK   -> <p>text &lt;!-- note --&gt;</p>
```

GitHub renders the third as `<p>text </p>` — the comment is invisible. So the one spelling a person
would actually write, a trailing comment after a space, is the one that escapes the guard and
prints itself to the reader. Not live: 0 comments anywhere in the 65 sources occur other than at
the start of a line.

**C4 — the card's list of what is still silently wrong is wrong in both directions.**

*Over-listed.* "a code span containing a backtick" is listed as silently wrong; it **raises**
(`doubled backtick code span`), and must, because any code span containing a backtick needs a
delimiter run of two or more.

*Mis-described.* "CommonMark's rule of three for runs of three or more delimiters" — runs of three
or more now **raise** (`***`, `___`). What is actually still wrong is same-character *nesting*, and
one form of it mangles content. Measured against GitHub:

| input | GitHub | mirror |
|---|---|---|
| `*foo**bar*` | `<em>foo**bar</em>` | `<em>foo**bar</em>` — correct |
| `*(*foo*)*` | `<em>(<em>foo</em>)</em>` | `<em>(*foo</em>)*` |
| `*a **b** c*` | `<em>a <strong>b</strong> c</em>` | `<em>a **b</em>* c*` — **one `*` eaten, two left stray** |
| `**a *b* c**` | `<strong>a <em>b</em> c</strong>` | same — correct |

*Under-listed.* A `---` underline directly after a paragraph line is a **setext H2** in GFM and an
`<hr>` here: `foo\n---` → GitHub `<h2>foo</h2>`, mirror `<p>foo</p><hr>`. The blacklist has
`^=+\s*$` for the `=` form and nothing for the `-` form, because `---` is already claimed by
`RULE`. Not live: 0 such sites in the 65 sources.

**C5 — the alignment row is the one table row the structural invariant does not check, and it
defeats the invariant's own statement.** `render_table` checks `rows[2:]` against `len(head)` and
never compares `split_row(rows[1])` with the header. Measured:

```
| A | B |        mirror: a 2-column table with one body row
|---|            GitHub: NOT A TABLE — <p>| A | B |<br>|---|<br>| c | d |</p>
| c | d |
```

Header 3 / alignment 2 behaves the same way. The card says "every table row must have the header's
cell count and a closing bar"; the alignment row is a row, it is exempt, and the exemption is the
one place where the mirror invents a table GitHub does not show. Not live: 0 tables in the 65
sources have a mismatched alignment row.

**C6 — `tools/md_to_html.py (494 lines)` is stale. It is 542.** `wc -l` at HEAD = **542**; the file
grew 48 lines in this very commit. "stdlib only" still holds (`html`, `posixpath`, `re`).

**C7, non-blocking — "with CommonMark's intraword rule kept for `_`" describes dead code.** Under
`opens = left and _ws(before)`, the added `_`-clause `(not right or _punct(before))` can never
change the verdict, because `_ws(before)` forces `right` false; the closing clause is inert for the
same reason. Brute force over all 5-character strings on the alphabet `a *_(.)␣`: **0 positions**
where the `_`-specific clause changes either answer. `*` and `_` now behave identically. The
promised behaviour (intraword underscores stay literal) does hold — for a different reason, and for
`*` too.

**C8, non-blocking — a bare URL containing a Markdown metacharacter carries the escape into the
`href`.** `esc()` escapes `*` always and `_` when not preceded by an alphanumeric, and `BARE_URL`
then swallows the backslash: a source URL `…/a__b` yields `href="…/a\_\_b"`. `check_links` does not
fetch external links, so this would be silently broken. The one URL in the corpus has no such
character.

### 1.8 Exact repair

**C-R1.** In How to verify, `2210` → **`2211`**. (Second pass in a row for this number.)

**C-R2.** `tools/md_to_html.py (494 lines, stdlib only)` → **`tools/md_to_html.py (542 lines,
stdlib only)`**.

**C-R3.** Fix `pipes_in_code_spans` to count backslashes inside the span as `_escape_bare_pipes`
does — escape a bar only when the backslash run before it is even — and replace the card's clause

> "pipes_in_code_spans() toggled on every backtick, so an odd count left the rest of a row unprotected, and tabular_to_md's lookbehind left \\| unescaped; both now count the backslashes or find the closing tick."

with

> "pipes_in_code_spans() toggled on every backtick, so an odd count left the rest of a row unprotected, and tabular_to_md's lookbehind left `\\|` unescaped. Both are fixed and both now count the backslash run: the first finds the closing tick and escapes only a bar whose preceding backslash run is even, the second does the same per cell. An earlier version of the first repair escaped the whole span blindly and turned an already-escaped `\|` inside a code span into `\\|`, which is the shredding the second repair exists to prevent."

**C-R4.** Propagate the flag: `inline(text[i + run:j], link, autolink=autolink)` at
`md_to_html.py:194`. Until then the card's "never inside a link label" must read "never inside a
link label, except that the flag is currently lost inside emphasis within a label, which would nest
one anchor in another; no label in the 65 sources contains a URL".

**C-R5.** Widen the comment guard to `(?<!^)\s*<!--|-->\s*\S` (or simply: any `<!--` that is not at
the start of the line after optional indentation), or strike "a comment opened or closed inside a
line" from the card's list of what raises and move the *opened* case to the list of what is
silently wrong.

**C-R6.** Replace, in the Statement:

> "What is still silently wrong, none of it occurring in what the generator emits today: a table with no leading bars, a row missing its leading bar, lazy blockquote continuation, a code span containing a backtick, balanced parentheses in a link target, and CommonMark's rule of three for runs of three or more delimiters."

with

> "What is still silently wrong, none of it occurring in what the generator emits today: a table with no leading bars; a row missing its leading bar; lazy blockquote continuation; balanced parentheses in a link target; a `---` underline after a paragraph line, which GFM makes a setext h2 and this renders as a rule; a pipe table whose alignment row has a different cell count from its header, which GFM does not make a table at all and this does; same-character nested emphasis, where `*a **b** c*` renders as `<em>a **b</em>* c*` against GitHub's `<em>a <strong>b</strong> c</em>`; and a comment opened mid-line after a space, which GitHub hides and this prints. A code span containing a backtick is NOT in this list: it needs a doubled delimiter and so raises."

and extend the invariant sentence to say that the alignment row is the one row it does not check.

**C-R7.** `tools/md_to_html.py`, the module docstring and the comment above `UNSUPPORTED_LINE`.
Delete "so a `.md` file is served as a raw download" (lines 5-7, the false causality the card fixed
two passes ago), "so a relative link between two documentation pages is the same string in both
trees" (10-11), "so the subset is closed and small … A construct outside that subset raises
`Unsupported`" (13-17) and "This is what makes the subset closed: the paragraph branch is the
fallback for PROSE, never for an unrecognised construct" (240-242). A reader opens the file before
the card, and the file now asserts in two places the exact property the card spent this commit
withdrawing.

---

## 2. `generated-docs` — **FAIL**

### 2.1 The prior findings

| finding | state now [C] | verdict |
|---|---|---|
| REF-CI-PAGES 1: "about 1300 lines" | see C9 | superseded, **stale again** |
| REF-CI-PAGES 2: "the 85 cards listed" | Statement says "the 90 cards the knowledge base now lists"; `build_docs.py --check` prints `claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, 5 verified, 5 open, 14 active, 5 done, 2 superseded, 1 refuted)`; the ten sum to 90 | **REPAIRED, exact** |
| REF-CI-PAGES 3: the note's "131 plus a results index" | the dated correction note stands, appended not rewritten. Recounted: 7 + 58 = 65 `.md`, `docs/read/` holds 66 `.html`, total 131 | **REPAIRED** |
| **B-R9**: "DETECTED (8: six source PDFs plus PRIVATE.md and CHECKLIST.md)" | Statement now reads "DETECTED (9: six source PDFs, plan_page/petz_program_plan.html, PRIVATE.md and CHECKLIST.md; the generator prints the list on every run, so the figure is checkable rather than typed)". `--check` prints exactly nine and names them | **REPAIRED, verbatim as asked** |
| B-R9 second half: "RENDERED … (6, on 7 bullets across 6 result pages)" | measured: 7 bullets carrying "held privately, not redistributed" across 6 result pages (`sequential-recovery-bound-type-iii` has two), naming exactly the six PDFs | **exact** |
| carried non-blocking (REF-CI-PAGES MINOR, then B "STILL OPEN"): the inventory never mentions `docs/read/` | still absent. Third pass | see C10 |

Other numbers re-measured, not read: 58 pages under `results/` ✓; 30/3/22/3 ✓; **783** internal
link targets over `docs/*.md` + `docs/results/*.md` with 0 external ✓; **36** source rows in
`refs/REFERENCES.md` (38 lines start with a bar, less header and alignment) ✓; `docs/status.md:5`
"90 cards: 89 claim cards … plus 1 finding", consistent with `ls claims/*.md` = 89 ✓. The drift
guard I re-tested rather than accepted: a byte appended to `docs/index.md` → `differs index.md`; a
byte appended to `docs/read/results/gap-law.html` → `differs read/results/gap-law.html`; a planted
`docs/results/archive_stale.md` → `stale … (no claim generates it any more)`; all three cleared and
`131 pages up to date` again. The guard code is byte-identical to what REF-DOCS-1c and REF-CI-PAGES
verified (`git diff b9daa45 HEAD -- tools/build_docs.py` touches only `pipes_in_code_spans`,
`_escape_bare_pipes` and `tabular_to_md`).

### 2.2 New findings

**C9 — the line count is stale for the third consecutive pass, and this commit is what made it
stale.** `wc -l tools/build_docs.py` = **1452**. The Statement says 1427. The file grew 25 net
lines in `6100643`, the commit whose purpose was to answer the referee, and the card was not
updated. The packet's own evidence rendering says it: `num:tools/build_docs.py: file present, 1452
lines`. This is 1300 → 1400 → 1427 → 1452; two referees have already spent a finding on it.

**C10 — "65 files" is false of the generator, and the two notes that correct it are not the
Statement.** The first sentence says the script "generates the public documentation subfolder from
the knowledge base: 65 files, namely seven top-level pages … and 58 per-claim pages under
docs/results/". It writes **131**: 65 Markdown and 66 HTML, all inside the drift guard, as the
card's own dated note and `docs-pages-rendering` both say. REF-CI-PAGES asked for one clause,
REF-CI-PAGES-B repeated the ask and called it non-blocking; at the third pass a sentence that is
wrong about the thing the card is named for is no longer non-blocking on its own.

Nothing else in the Statement is false. Everything REF-DOCS-1c, REF-CI-PAGES and REF-CI-PAGES-B
asked for is present and correct, and B-R9 was applied word for word.

### 2.3 Exact repair

**C-R8.** `tools/build_docs.py (1427 lines)` → **`tools/build_docs.py (about 1450 lines)`**, or drop
the count. Three passes have now been spent on this number; it moves with every commit that touches
the file, and nothing in the card depends on it. If it stays, it must be 1452 today.

**C-R9.** Replace

> "generates the public documentation subfolder from the knowledge base: 65 files, namely seven top-level pages (index, status, notation, definitions, open, sources, history) and 58 per-claim pages under docs/results/"

with

> "generates the public documentation subfolder from the knowledge base: 131 files, namely 65 Markdown sources — seven top-level pages (index, status, notation, definitions, open, sources, history) and 58 per-claim pages under docs/results/ — and the 66 HTML renderings of them under docs/read/ that md_to_html.py produces (7 top-level, 58 mirrors and a generated results index; see docs-pages-rendering). All 131 are inside the drift guard."

---

## 3. `repo-split-public-private` — **FAIL**

### 3.1 The REF-PLAN-SPLIT findings

| finding | state now [C] | verdict |
|---|---|---|
| **B13**, serious: the compendia are still recoverable from the remote | the Statement now says so, in capitals, and says the repository must not be made public. **I re-derived it independently and it holds** — see 3.2 | **REPAIRED, and the claim is true** |
| **B14**: the mirror-clone check is the wrong instrument | Statement says "the mirror-clone check REF-MOVE-1e ran cannot see server-side retention, because a clone carries only reachable objects" | **REPAIRED** |
| the new dated note | present, 2026-09-21, states the three routes, the Actions-API publication, why the mirror clone could not see it, and that going public is blocked. The two older notes are left intact and appended to, as the author rule requires | **REPAIRED** |
| **R-B23(i)+(ii)**: `PRIVATE.md` | "currently public, which is defensible" is gone; the last section now says the five were moved on 2026-09-21 and that "Residual, and it blocks going public: GitHub still serves the pre-rewrite objects by SHA". The "What this is" bullet names the five compendia and `plan_page/petz_program_plan.html`. "Ten knowledge-base cards cite nine files that live here", with `plan_page/petz_program_plan.html` enumerated | **REPAIRED, all three parts** |
| **R-B23(iii)**: `CHECKLIST.md` item 3 | struck and marked, in the style of items 1, 2 and 5, with "RESIDUAL, AND IT BLOCKS GOING PUBLIC" and both remedies | **REPAIRED, and stronger than asked** |
| **R-B19**: "EIGHT targets … EIGHT cards" | Statement says NINE and TEN. Recounted under the card's own rule: **9 targets, 10 cards** — the six PDFs, `CHECKLIST.md`, `PRIVATE.md`, `plan_page/petz_program_plan.html`; cards `all-channel-equals-quasi-free`, `all-channels-symbol-feasible`, `fidelity-formula-correction`, `implementer-hypotheses`, `open-problems-plan-note8`, `plan-page`, `repo-split-public-private`, `sequential-recovery-bound-type-iii`, `single-observable-bound`, `vwz-protocol-ordering` | **REPAIRED, exact** |
| **R-B1**: "406 files, 5.9 MB" | now "614 files, 7.93 MB as of 2026-09-21; the figure moves with every commit". At HEAD: **616 files, 8,013,110 B = 8.01 MB** | partly repaired, **stale by 2 files** |
| **R-B2**: "the 97 result captures" — drop it or state the rule | **unchanged**, still in the Statement. No rule reproduces 97: `.out` 83, `+.txt` 102, `+.err` 104, `+.raw` 110, `+.md` 116; front-matter evidence targets under `numerics/` 54, of which non-script **27**; all non-document evidence targets 75, non-document-non-script **33** | **NOT REPAIRED** |
| **R-B3**: the private enumeration is six files short | the count was changed to 235 and 48.4 MB (measured: **235 files, 48,390,067 B = 48.39 MB**, exact) but **the enumeration was not touched**: "the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude" is 178 + 47 + 4 = **229**. The five compendia and `plan_page/petz_program_plan.html` are still missing from it, in the same sentence whose own count is 235 and two sentences before the card says the compendia were moved there | **NOT REPAIRED** |
| **R-B6**: "(196 MB)" → "about 198 MB" | **unchanged**. Measured: 422 files, 198,466,382 B = **198.5 MB** | **NOT REPAIRED** |
| **R-B25**: the comma splice in `next` | **unchanged**: "removed from the public history, that gate is discharged" | **NOT REPAIRED** (and now the least of that field's problems — C12) |

Unbroken, re-measured: overlap **0** (`comm -12` over both `ls-files`); 178 excerpts and 47 source
PDFs tracked privately; **256** `\shot`/`\shotc` invocations across 20 `.tex` files, less the one
inside the `\shotc` definition in `rigor_preamble.tex` = **255 in 19**; both remotes `PRIVATE`,
`fork: false`, `forks_count: 0`, one collaborator, **0** deploy keys, one branch; the tag
`v0.1.0-draft` resolves on the remote to `5ad78cb`, which exists locally and whose tree contains
**0** compendia, excerpts or PDFs; the release carries exactly the two paper PDFs; no tracked
`.tex` inputs a compendium.

### 3.2 The exposure, re-derived from scratch

I did not run `git fetch` (it writes). REST only, which is weaker and still enough:

* `GET /repos/…/commits/5d64c77d4b513b4005e2ad3a19c0f26086e96be0` → `2026-09-21T09:38:37Z`,
  "referee report on the build repairs". `git cat-file -t` on the same SHA locally:
  **`fatal: could not get object info`**. The remote serves a commit the local history does not have.
* `GET /repos/…/contents/rigor/{cited_R1,cited_R2,cited_R3,cited_R4,cited_results_all}.tex?ref=5d64c77…`
  → **70,874 / 72,489 / 66,304 / 90,433 / 299,915 bytes**, the five sizes the card states.
* `GET /repos/…/git/blobs/18cc05ab438b307f64fd7b4ee35834b30c06f0d6` → 299,915 bytes decoded,
  **`cmp` byte-identical to the private `rigor/cited_results_all.tex`**.
* `GET /repos/…/commits?sha=5d64c77…&per_page=100` → **43** commits, and **43 of 43** are absent
  from the local history. The card's "43 pre-rewrite commits" is exact.

So the card's central claim is true, and its remedies are the right two: a GitHub Support purge of
the unreachable objects, or deleting and recreating the remote (the two release assets are indeed
the only assets, and the one tag would have to be re-pushed — worth adding).

**C11 — the exposure has a second, wider publisher of pre-rewrite SHAs that the card does not
mention.** The card says "this repository's own Actions run list publishes them as the head SHA of
every run before 9aed69a, and 15 of the 27 head SHAs it serves are commits the rewrite discarded".
Measured:

* `/repos/…/actions/runs` now serves **28** runs (24 failure, 4 success), 28 distinct head SHAs, of
  which **15** are gone from the local history. The 15 is exact; the denominator is 28, not 27,
  because the review commit itself triggered a run.
* `/repos/…/events` serves **53 PushEvents**, whose `before` and `head` fields give **55 distinct
  SHAs, of which 44 are pre-rewrite commits** — nearly three times as many, and **29 of them appear
  nowhere in the Actions run list**. Demonstrated, not inferred: `04af962a9a29…` ("README: ten
  defects from REF-README-1"), a SHA that was never a workflow head, resolves through
  `/commits/{sha}` and `/contents/rigor/cited_R1.tex?ref=04af962…` returns the file at 70,874 bytes.

A third, smaller one: the card's own Statement — which names `5d64c77` and the recovery command —
is published verbatim in `docs/data/extra-claim-map.json`, is committed to the public repository and
is what module 10 renders. That is consistent with the card's position that the hashes are not
confidential, but it means the repository now ships the recipe as well as the hashes, and the
"delete and recreate" remedy would carry it across to the new remote.

**C12 — the `next` field says publication is gated on nothing, the Statement says it is blocked, and
`CHECKLIST.md` now agrees with the Statement. The false one is the published one.** The field reads:

> "The still-open items of CHECKLIST.md before making cft-cmi public are four, of which the two that
> gate publication are: none, but the two former gates were closed differently … one was DISCHARGED
> by action and cannot reopen … The five cited-result compendia were moved to the private companion
> on 21 September and removed from the public history, that gate is discharged."

Against, in the same card, "UNTIL ONE OF THEM IS DONE, 'removed from the remote' MUST NOT BE
CLAIMED, AND THE REPOSITORY MUST NOT BE MADE PUBLIC"; and in the card's own evidence document,
`CHECKLIST.md` item 3, "RESIDUAL, AND IT BLOCKS GOING PUBLIC". The compendia gate is not discharged,
it did reopen, and "the two that gate publication are: none" is now flatly false. REF-PLAN-SPLIT
called four "defensible … fix by marking item 3"; item 3 has been marked, and marking it is what
falsified the field. `docs/data/extra-claim-map.json` carries the field verbatim, so this is the
one sentence of this card a reader of the site meets. This is exactly the defect REF-PLAN-SPLIT
failed the sibling card for (A26).

### 3.3 Exact repair

**C-R10.** Replace the private enumeration

> "(235 files, 48.4 MB as of 2026-09-21: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude)"

with

> "(235 files, 48.4 MB as of 2026-09-21: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, the five cited-result compendia rigor/cited_R1-R4.tex and cited_results_all.tex, plan_page/petz_program_plan.html, CHECKLIST.md, PRIVATE.md, pgit and pgit-exclude — the list pgit's PRIVATE_PATHS enforces, and it adds to 235)"

**C-R11.** `(196 MB)` → **`(about 198 MB over 422 files)`**.

**C-R12.** Drop "the 97 result captures the KB cites as evidence" or state the rule that produces
97. Nothing I tried does, and nothing REF-PLAN-SPLIT tried did. Suggested: "…numerics scripts and
their run captures (104 tracked `.out`, `.txt` and `.err` files, of which 27 are named by a card's
evidence field)".

**C-R13.** `614 files, 7.93 MB as of 2026-09-21` → **`616 files, 8.01 MB at 6100643`**, or drop the
byte figure and keep only the hedge that already follows it.

**C-R14.** Replace, in the Statement,

> "this repository's own Actions run list publishes them as the head SHA of every run before 9aed69a, and 15 of the 27 head SHAs it serves are commits the rewrite discarded."

with

> "the repository publishes them itself, through two endpoints. /actions/runs serves the head SHA of every run, and 15 of the 28 it currently lists are commits the rewrite discarded; /repos/.../events serves the before and head SHA of all 53 push events, and 44 of the 55 distinct SHAs there are pre-rewrite commits, 29 of which were never a workflow head. Both counts grow with ordinary use. Any principal with read access can enumerate the discarded history from either, without being handed a hash; this card's own Statement, published verbatim in docs/data/extra-claim-map.json, is a third source."

**C-R15.** Rewrite the `next` field. It is published verbatim on the public surface and it currently
contradicts both the Statement and `CHECKLIST.md`. Suggested:

> "Publication is BLOCKED. CHECKLIST.md has three items still open before cft-cmi can go public, and
> one of them gates it absolutely: item 3, the cited-result compendia, which were moved to the
> private companion on 21 September and removed from every reachable commit, but which GitHub still
> serves from the remote by SHA; that gate was discharged by action and REOPENED by measurement
> (REF-PLAN-SPLIT, confirmed REF-PASS-C), and it closes only when GitHub Support purges the
> unreachable objects or the remote is deleted and recreated from this local history with the tag
> and the two release assets re-pushed. The other two are item 4, fourteen tracked captures carrying
> the absolute path of the machine they ran on, left alone because rewriting a capture would edit
> evidence, and item 6, that nothing forces an immediate public repository. Item 5, arXiv-first
> sequencing, was WITHDRAWN by decision rather than discharged and can return as a preference when
> the papers are ready. Item 1, the author block, closed on 2026-09-20."

**C-R16.** While rewriting it, the comma splice R-B25 named goes away with the sentence.

---

## 4. `ci-green` — **PASS**

| finding | state now [C] | verdict |
|---|---|---|
| **B1**: "The pages job … is enabled when the repository goes public" | replaced: "Going public enables nothing by itself: publishing needs three things, the repository public, that line removed, and Pages enabled once on the repository, which is what rigor/public_site_plan.md:226 means by 'one line plus one click'." Line 226 of the plan is D1 and says exactly that | **REPAIRED** |
| **B1(b)**: the new false comment in `check.yml` | the whole comment is rewritten to the three conditions, and `with: { enablement: true }` is **removed** from `actions/configure-pages@v5` | **REPAIRED** |
| the `enablement` reasoning | verified at source, not accepted: `repos/actions/configure-pages/contents/action.yml?ref=v5` documents `enablement` as "This option requires a token other than `GITHUB_TOKEN` to be provided … the `administration:write` and `pages:write` permissions are required", and `token` defaults to `${{ github.token }}`. The job passes no `token:` | **exact** |
| B1 smaller: "its absence is what failed **every run**" | comment now reads "every **papers job** … (the other job failed independently, on the claim map)" | **REPAIRED** |
| REF-CI-PAGES 1 and 2 (cause inverted; `--allow-missing-kb` presented as closed) | both repaired at `b9daa45` and unchanged; `tools/build_site_data_extra.py` is not in `git diff b9daa45 HEAD` | hold |

Numbers re-measured: `/actions/runs` gives 24 `failure` and 4 `success`; the lowest-id success is
**35602149545** at `9aed69a`, so "24 runs, 0 successes" before it is exact. `49` `rigor/*.tex` on
disk, `44` public-tracked, difference = the five compendia, so CI's 41 against the local 46 is
right. `README.md:419` "All 41 rigor documents in this repository compile", inside section 13
(lines 417-…). The claim map at `5a3988b` has 88 cards and 147 edges and no `ci-green` node; at HEAD
it has 90 and 153 — so "it was regenerated in the following commit" is exact. `make rigor` runs the
checker rather than printing "up to date". `Makefile` prints the last 40 lines of `main.log` on a
papers failure and has `rigor` in `.PHONY`.

I looked for something new and did not find it. The one thing I would add if the card is ever
touched again: it says the `enablement` input "cannot supply the third" without saying that it was
briefly set and has been removed; `docs-pages-rendering` says "and is not set", which is the better
wording. That is not a defect.

---

## 5. The Pages statements, cross-checked

| source | what it says | agrees? |
|---|---|---|
| `rigor/public_site_plan.md:226` (D1) | "enabling it is one line plus one click once `CHECKLIST.md` is clear" | the governing decision |
| `.github/workflows/check.yml:59-65` | "Publishing needs THREE things, as decision D1 says … the repository going public … this `if: false` removed; and Pages enabled once on the repository", plus why `enablement` cannot do the third, and it is not set | ✓ |
| `README.md:37-40` | "Publishing needs three things: the repository going public … the `if: false` on that job being removed; and Pages enabled once on the repository, which the workflow cannot do for itself" | ✓ |
| `ci-green` Statement | three things, naming `public_site_plan.md:226` and the `action.yml` reason | ✓ |
| `docs-pages-rendering` Statement | three things, "as decision D1 says", plus "is not set" and "has_pages false" | ✓ |
| `public-site-plan` Statement | "Four decisions, all TAKEN … recorded at rigor/public_site_plan.md:224 … D1 when Pages goes live" — line 224 is exactly `## 6. Decisions — taken 2026-09-21 by the user` | ✓ |

`gh api repos/alexander-stottmeister/cft-cmi` → `private: true`, `has_pages: false`, `fork: false`,
`forks_count: 0`; `/pages` → 404. All five statements agree with each other and with D1.

**The github.io count is right.** `grep -n github.io README.md` returns exactly six lines: 27, 33,
34 (introduction; `## 1.` is line 42) and 339, 340, 341 (section 9; `## 9.` is 309, `## 10.` is
352). Six, three and three, at the stated line numbers.

---

## 6. `public-site-plan` — **PASS**

Every one of REF-PLAN-SPLIT's thirteen repairs is applied, and I re-measured each rather than
reading it.

| repair | state now [C] |
|---|---|
| R-A1 237 lines | `wc -l rigor/public_site_plan.md` = **237** ✓ |
| R-A2 README 430 lines | **430** ✓ (the predecessor was 77, and "80" is the plan's own word, quoted) |
| R-A3 eight slots, three reusing four PNGs, five new SVG | plan table: F1-F5 new, F6 `collapse.png`, F7 `gap_decay.png`+`thermal_shield.png`, F8 `cfun_flow.png`. `docs/assets/` holds exactly the five SVGs named ✓ |
| R-A7/R-A8 12 numericals, 45 claims, 89 claim cards | the module table names **51** ids: 30 proved, 3 refereed, **12 numerical**, 3 conjectural, 2 verified, 1 refuted. 33 + 12 = **45** ✓. `ls claims/*.md` = **89** ✓, and `docs/status.md:5` says "90 cards: 89 claim cards … plus 1 finding", consistent ✓ |
| R-A9 module 10 is the exception | ✓, and the claim map carries all 90 cards |
| R-A11 the (H) wording | the card now carries the plan's own repaired sentence, VWZ 1(A)/1(B) included ✓ |
| R-A15 C6 was never the cause | `7cae480` is 2026-09-21 11:07:47, `9aed69a` is 14:53:05 ✓ |
| R-A18 three done, DOI outstanding | `CITATION.cff` tracked, `.github/ISSUE_TEMPLATE/{build,cited-result,claim}.md` tracked, `plan_page` public-tracked = **0** ✓ |
| R-A19 six phases, four passes | plan §5 rows P0-P5; P0 "it is itself the pass", P5 "the workflow is its own check" ✓ |
| R-A21 cut P4 to modules 4 and 6 | ✓ |
| R-A23 D2 as taken | plan D2: releases now, `docs/pdf/` as a Pages artefact, never committed, ignore rule intact ✓ |
| R-A25 How to verify | replaced with the phase list ✓ |
| R-A26 `next` | replaced, and `docs/data/extra-claim-map.json` carries the new text ✓ |

Also re-measured: `docs/.nojekyll` exists; `docs/lib/katex` is vendored; `docs/explore/` holds ten
module pages; 30 proved + 3 refereed; `make check` has a `check:` target that fails on drift; and
"every displayed number ships as a JSON record {value, error, source, line, status}" is true of
**1160** records across the nine data files, with `source` a string in every one.

**One stale figure, not blocking.** "The 3 MB asset budget holds (docs/{assets,lib,data} = 1.26 MB,
public repository 7.93 MB)". Measured: `docs/{assets,lib,data}` is 1,265,533 B, i.e. **1.27 MB**
rounded and 1.26 truncated, which is how this card writes its other figures; the public repository
is now **8.01 MB**, because the commit under review added the two referee notes. The budget claim
itself — 3 MB for site assets — holds with room. Repair when the card is next touched:
`public repository 7.93 MB` → `public repository about 8 MB`. I am not failing a 26-clause card on
a 1% drift that the reviewed commit itself caused and that no fixed number can survive.

**Minor, carried:** "D4 whether the site carries the AI provenance (recommended yes, in the papers
wording)" still says "recommended", inside a sentence that opens "Four decisions, all TAKEN"; and
the plan's D3 still reads "33 refereed-or-proved claims plus 11 headline numericals" where the card
says 12 — but the card explains the change and names its cause, and D3's decision (all ten modules)
is unaffected. Neither is wrong as written.

---

## 7. The gates, run by me

`make check` — **exit 0**, clean tree:

```
python3 tools/check_links.py
  155 pages, 2211 links resolve
  external hosts: alexander-stottmeister.github.io, github.com, projecteuclid.org
python3 tools/build_docs.py --check
build_docs --check: 131 pages up to date
  claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, 5 verified, 5 open,
             14 active, 5 done, 2 superseded, 1 refuted)
  pages under results/: 58
  evidence pointers held privately, rendered without a link: 9
      refs/Sion1958_minimax.pdf
      refs/BJL_twisted_duality_math-ph-0204029.pdf
      refs/AlbertiUhlmann02_math-ph-0202038.pdf
      refs/CDIT_1808.02384.pdf
      plan_page/petz_program_plan.html
      PRIVATE.md
      CHECKLIST.md
      refs/Uhlmann76.pdf
      refs/VWZ_2307.14434.pdf
  cards never refereed: 0 of the 90 listed (0 with a page); 232 of the 322 cards in the
             whole knowledge base, the rest being findings that reach no displayed status
  cards awaiting a referee pass: 5 (ci-green, docs-pages-rendering, generated-docs,
             public-site-plan, repo-split-public-private)
  cards whose last referee pass failed: 0
ok       docs/data/quadratic-law.json
ok       docs/data/constants.json
ok       docs/data/theta.json
ok       docs/data/universality.json
ok       docs/data/networks.json
  page record references: all resolve
ok       docs/data/extra-separation.json
ok       docs/data/extra-off-criticality.json
ok       docs/data/extra-relative-entropy.json
ok       docs/data/extra-claim-map.json
```

Note that this is the first pass at which `make check` is green at HEAD — the two previous passes
both found it red on the `review pending` markers, and the author regenerated. `check_links` prints
**2211**, which is the number `docs-pages-rendering`'s How to verify still gives as 2210, and it now
lists `projecteuclid.org` as a third external host, which is the new autolink.

`make rigor` — **exit 0**: `46 document(s), 0 failing, 0 known`.

`kb -p cft_cmi lint` reports no issue beyond the five cards awaiting this review.

---

## 8. Consistency

`kb -p cft_cmi q --text Pages` (15 cards), plus a grep of every card for `enablement`, `goes
public`, `has_pages` and `compendia`. **No card contradicts another.** The Pages-enablement
disagreement REF-CI-PAGES-B recorded between two cards, the README and D1 is gone: all five sources
now say three conditions (§5). `ci-green`'s "the 5 untracked `cited_R*` compendia" is right (49
`rigor/*.tex` on disk, 44 public-tracked), and no card other than `repo-split-public-private` makes
a claim about whether the compendia are removed from the remote.

The one contradiction left is **inside** `repo-split-public-private`, between its Statement, its
`next` field and `CHECKLIST.md` item 3 (C12).

---

## 9. Note for the build agent

`make check` was green at HEAD when I ran it and is red again now that the five verdicts have
landed, because `docs/status.md` and `docs/read/status.html` carry each card's review state: the
whole drift is three `review pending` cells becoming `referee pass failed` and the aggregate
"0 carry a failed referee pass" becoming 3. That is rule (c) working as REF-DOCS-1c agreed, not a
regression. Run `make docs data` and commit. The working tree was otherwise clean when I finished;
the only file I added is this one.
