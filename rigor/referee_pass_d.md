# REF-PASS-D: fourth pass on docs-pages-rendering, generated-docs, repo-split-public-private (2026-09-21)

Scope: the three cards REF-PASS-C failed, against `referee_pass_c.md` (REF-PASS-C) and, behind it,
`referee_ci_pages.md`, `referee_ci_pages_b.md` and `referee_plan_split.md`.

Verdicts: **`docs-pages-rendering` PASS, `generated-docs` FAIL, `repo-split-public-private` FAIL.**

Everything marked [D] is measured by me at HEAD = `bbaa665`, the parent being `6100643`, which is the
state REF-PASS-C reviewed. `git status --porcelain` was empty before I started and is empty now; the
three files I touched for the drift-guard test were restored by file copy or removed. No git command that writes
was run: the remote is probed by REST only.

The brief I was given was that each of the three previous passes found a repair that introduced a new
defect, twice in the same pair of helper functions, and to look there first. **This time the pair is
clean.** §1.1 is the evidence. The new defects are elsewhere: one in each of the two rewritten
sentences that answered REF-PASS-C, and a third created by deleting a number that turns out to have
been exact all along.

---

## 1. `docs-pages-rendering` — **PASS**

### 1.1 The helper pair, attacked as a pair

`pipes_in_code_spans` (`build_docs.py:830`) now hands the whole span, backticks included, to
`_escape_bare_pipes` (`build_docs.py:808`, moved up the file but otherwise byte-identical to the
version REF-PASS-C verified). The composition is what C-R3 asked for and it survives everything I
built:

| property | instrument | result [D] |
|---|---|---|
| `pipes_in_code_spans` idempotent | 300,000 random strings over ``|`\ab␣`` of length 1-10, plus every string of length ≤ 7 over ``|`\a`` (21,844) | **0 failures** |
| `_escape_bare_pipes` idempotent | same corpus | **0 failures** |
| `_escape_bare_pipes` leaves no live pipe (one not preceded by an odd backslash run) | same corpus | **0 failures** |

The four attacks the brief named, run through `md_to_html.split_row` for the cell count GFM would
give the rewritten row:

```
| `a|b` | c |        -> | `a\|b` | c |        2 cells  ['`a|b`', 'c']
| `a\|b` | c |       -> unchanged             2 cells  ['`a|b`', 'c']      <- C1 is fixed
| `a\\|b` | c |      -> | `a\\\|b` | c |      2 cells
| `a\\\|b` | c |     -> unchanged             2 cells
| `a | b |           -> unchanged             2 cells  (odd backtick count, = GFM)
| a`b | c`d |        -> | a`b \| c`d |        1 cell   (span over a cell boundary; unchanged
                                                        behaviour, the function's stated intent)
| x \| y | `p|q` |   -> | x \| y | `p\|q` |   2 cells  (already-escaped bar OUTSIDE a span)
| `a\` | b |         -> unchanged             2 cells  (span ending in a backslash)
| `\\` | b |         -> unchanged             2 cells
| ``a | b`` | c |    -> unchanged             (raises later: doubled backtick)
```

`docs/history.md:219` is **2 cells** and both `||u||^2` occurrences survive into the cell text
(`REF-P5-KB1 minor: \`||u||^2 stable to four digits\` ... (untapered \`||u||^2 = 0.014889\`)`).

**No other table anywhere in `docs/` changed.** `git diff 6100643 HEAD -- docs/` touches three files
and none is a page with a table body: `docs/status.md` and `docs/read/status.html` (four lines, the
review markers) and `docs/data/extra-claim-map.json`. The 65 sources hold **19 tables over 233 rows**
and every one parses. Independently: I reimplemented the parent's blind-`replace` version and ran both
over all **597** table lines in `rigor/*.md`; they differ on **24** of them, every one inside a referee
note, and none in a file the generator reads (`history_page` reads only `rigor/PHASE*_STATUS.md`, whose
29 table rows carry no `\|` inside a code span). So the fix changes the emitted corpus by nothing and
changes the flagged construct by exactly the right amount.

### 1.2 `autolink` through the emphasis recursion

`md_to_html.py:192-194` now passes the flag positionally into the recursion. No nested anchor by any
route I could find [D]:

* **Fuzz:** 400,000 random and 111,000 exhaustive `inline()` inputs over
  `[ ] ( ) * _ \` \\ a b ␣ https://x.y b.md` — **0** occurrences of `<a …>…<a `.
* **Targeted routes**, all clean: `[*see URL*](a.md)`, `[**URL**](a.md)`, `[_a URL_](a.md)`,
  `[*a **b URL** c*](a.md)`, the same inside a **table cell**, inside a **blockquote**, inside a
  **blockquote that contains a table**, inside a **list item**, inside an **`<h1>`**, with a **code
  span** in the label, and a **link inside a link label** (`[a [b URL](c.md) d](e.md)` →
  `<a href="c.html">a [b https://x.com/y</a> d](e.md)` — mangled, but one anchor, and the URL inside
  the inner label is correctly not linked).

The card's "never inside a link label" is now true.

### 1.3 The alignment-row invariant

`render_table` compares `split_row(rows[1])` with the header before it looks at the body. I could not
get through it [D]. Eighteen attacks; the mirror's answer and whether GitHub makes a table:

| attack | mirror | GitHub tables? |
|---|---|---|
| align 2 / head 3, align 3 / head 2 | RAISE, names both counts | no |
| code span with a bare pipe in the header (head 3, align 2) | RAISE | no |
| code span with a bare pipe in the alignment row | RAISE (no alignment row) | no |
| empty alignment cell `\|---\|\|` | RAISE | no |
| alignment row carrying `\|---\|---\\|\|` | RAISE | no |
| header, alignment and body all missing the trailing bar | RAISE (no closing pipe) | yes |
| only the header missing it | RAISE (2 vs 1) | yes |
| body row short / surplus / trailing spaces | RAISE | yes |
| header with an escaped bar; 1×1 table; alignment row last | correct table | yes |
| `:-:` (single dash) | RAISE (no alignment row) | **yes** — the one remaining divergence, and it fails loud |

The only way the mirror still differs from GitHub on a table is by raising where GitHub renders, never
by rendering where GitHub does not. Sentence 7 of the Statement is now true as written and needs no
caveat; C5 is closed.

### 1.4 The mid-line comment guard

`(?<!^)<!--|-->\s*\S`. Behaviour [D]: raises on `text <!-- note -->`, `a <!-- c --> b`, `x<!-- c --> y`,
` <!-- c -->` and `\t<!-- c -->`; does not raise on `<!-- c -->` or `<!--x-->` at column 0.

It rejects no legitimate line. All **67** comment openings in the 65 sources start at column 0 (the
generated banner on 63 pages, and `<!-- Assembled once … -->` plus `<!-- hand-edited: no -->` on
`notation.md` and `definitions.md`), and all 65 sources render: `build_docs --check` prints
`131 pages up to date` and exits 0.

**The sharpest instrument I have for "did the repair break something": a differential test of the
parent's `md_to_html.py` against HEAD's over 200,000 random documents** built from
`| \` \\ * _ a ␣ <!-- --> [ ] ( ) --- \n URL .md # - > A : --` [D]:

* documents both versions accept, with **different HTML**: **0**;
* documents the parent raised on and HEAD accepts: **0**;
* documents HEAD raises on and the parent accepted: 1,602, with exactly **two** distinct reasons —
  `HTML comment inside a line` and `alignment row has N cells, header has M`.

The commit is a pure tightening. There is no third effect hiding in it.

### 1.5 The "still silently wrong" list, probed entry by entry

Each rendered through the real `render_body` and through `gh api /markdown --mode gfm` [D]:

| entry | mirror | GitHub | still wrong? |
|---|---|---|---|
| a table with no leading bars | `<p>A \| B ---\|--- c \| d</p>` | a table | **yes** |
| a row missing its leading bar | table with an empty body, then `<p>c \| d \|</p>` | a 1-row table | **yes** |
| lazy blockquote continuation | `<blockquote><p>a</p></blockquote><p>b</p>` | `<blockquote><p>a<br>b</p></blockquote>` | **yes** |
| balanced parentheses in a link target | `<a href="results/f(1">t</a>.md)` | `<a href="results/f(1).md">t</a>` | **yes** |
| `---` after a paragraph line | `<p>foo</p><hr>` | `<h2>foo</h2>` | **yes** |
| same-character nesting `*a **b** c*` | `<em>a **b</em>* c*` | `<em>a <strong>b</strong> c</em>` | **yes** |

and the two negatives are right: ` ``a ` b`` ` raises (`doubled backtick code span`) and `***x***` /
`___x___` raise (`triple emphasis`). Also checked, and correctly **absent** from the list because the
commit fixed them: the alignment row, and a comment opened mid-line after a space. This is the first
pass at which the list is wrong in neither direction.

**Omissions.** Three constructs are silently wrong and unlisted: a bare URL carrying `esc()`'s
backslash into the `href` (C8, below); a link inside a link label (mirror makes an anchor, GitHub does
not); and a block construct indented by one to three spaces (` | A | B |`, ` # x`) which GFM accepts
and the mirror drops into a paragraph. None is live. **I am not counting these against the card**,
because the same paragraph says in capitals that the subset is NOT closed, that `reject_unsupported`
is "a BLACKLIST … a guard, not a proof" and that it "leaves the rest silent". A list introduced by that
sentence does not claim to be exhaustive, and over-listing — the failure mode of the last three passes
— is gone. They belong in the list the next time the card is touched.

### 1.6 The GFM comparison, re-measured not accepted

I rendered all **65** sources through `gh api /markdown -f mode=gfm`, stripped tags and whitespace from
both streams and diffed character by character [D]:

* **58 of 58** result pages: character-identical.
* `index.md`, `open.md`, `sources.md`, `status.md`: character-identical.
* `history.md`: **6** — six `*` of `M_*`, `lambda_min(M_*)/||M_*||`, `M_*-tau_*`, `M_*(0,0)`, `M_*(y,y)`.
* `notation.md`: **6** — six `_` inside `$\|f\|_{\beta}=\sum_{n}…$`, `$\|G\|_{3/2}^{2}=\int_{\mathbb R}…$`,
  `…\|_{\mathfrak S_{2}}^{2}…`.
* `definitions.md`: **2** — two `_` inside `$k_{s}\|_{A}=\mathrm{id},\qquad k_{s}(x)…$`.

**14, and every one of them GitHub deleting mathematics the mirror keeps.** The figure reproduces
exactly. One qualification the card does not make: `notation.md` also differs at **three** further
positions where GitHub's `<math-renderer>` double-escapes `<` and `>` inside `$…$`
(`${k<0}$` → `${k&lt;0}$`), so a verifier who follows the How-to-verify sentence literally sees 17
differing sites, not 14, and three of them are not GitHub deleting anything. REF-PASS-C set the same
three aside as "not a Markdown difference", which is the right call; the card should say so in five
words. Non-blocking, §1.9.

### 1.7 Every other number and claim

All measured, none accepted [D].

| claim | measurement |
|---|---|
| "113 in 12 HTML files plus one built at runtime in claim-map.html from the JSON field 'page'" | at `9aed69a`, the pre-mirror tree: **113** relative `.md` strings in **12** HTML files (118 `.md` hrefs less 5 blob URLs, plus the `#anchor` forms); the runtime one is `claim-map.html:390`, `if (c.page) … href: '../read/results/' + c.page.replace(/\.md$/,'.html')` |
| `tools/md_to_html.py (stdlib only)` | `import html, posixpath, re` and nothing else. The line count is **gone**, which is right: it is 546 today, having moved 494 → 542 → 546 in three commits and cost two referee findings |
| "It now raises on …" and "blocks() raises on …" | **every construct the Statement lists raises**, each with a named reason. I ran 35 spellings covering all of them, including both halves of "a comment opened or closed inside a line" and `make_link`'s "link escapes the repository" |
| "every table row must have the header's cell count and a closing bar" | true, alignment row included — §1.3 |
| "65 pages became 131 in total, namely 65 Markdown and 66 HTML" | 7 + 58 = **65** `.md`; `docs/read/` holds **66** `.html` (7 top-level + 59 under `results/`, the 59th the generated index); **131**, all git-tracked |
| "--check covers it (a changed byte, a deleted mirror page, and an orphan anywhere under read/)" | retested: a byte appended to `read/results/gap-law.html` → `differs read/results/gap-law.html`; a byte appended to `index.md` → `differs index.md`; a planted `read/results/archive_orphan.html` → `stale … (no claim generates it any more)`; all restored → `131 pages up to date`, exit 0 |
| "A page a human has taken over … is mirrored from what is on disk" | `build_docs.py:1284-1290`: the skipped list is read back off disk and rendered into `read/` |
| "loses no source word … all 8 anchor ids survive" | word multisets of source and rendering agree on **64 of 65** pages once link targets are excluded, and on the 65th (`definitions.md`) the rendering has only EXTRA tokens, from `\[h''/h'\](p)`; nothing is lost anywhere. The 8 `<a id="area-…">` in `status.md` are 8 `id=` attributes in `read/status.html` |
| "27 result pages now render it as emphasis"; "history.html now carries no em span at all" | `_None recorded._` on **27** result pages, `<em>` on exactly those **27**; `grep -c '<em>' docs/read/history.html` = **0** |
| "check_links.py … the pattern now applies to Markdown only" | `check_links.py:41`, `pattern = MD_LINK if rel.endswith((".md",".markdown")) else HTML_LINK` |
| README "six times, three in the introduction (lines 27, 33, 34) and three in section 9 (339, 340, 341)" | exactly those six lines; `## 1.` is 42, `## 9.` is 309, `## 10.` is 352 |
| "configure-pages … is not set"; "has_pages false" | no `enablement` key in `check.yml`; `gh api repos/…/cft-cmi` → `private true, has_pages false, fork false, forks_count 0` |
| "two pages link to results/" | `docs/index.md:24` and `docs/status.md:21` |
| How to verify: "check_links 155 pages and 2211 links resolve, build_docs --check 131 pages up to date, all nine data files ok" | `make check` prints exactly that and **exits 0** |
| "the divergence is confined to emphasis" | true of all 14 Markdown-difference characters — §1.6 |

### 1.8 Why this is a pass

All six of REF-PASS-C's blocking findings are repaired and each one re-measured rather than read:
C-R1 (2211), C-R2 (the line count dropped), C-R3 (the helper pair, §1.1), C-R4 (§1.2), C-R5 (§1.4),
C-R6 (§1.5). I attacked the commit with 511,000 fuzz inputs for nested anchors, 321,844 for the helper
pair, 200,000 for a differential test against the parent and 65 real pages against GitHub's own
renderer, and found no clause of the Statement or of How to verify that is false.

### 1.9 Carried, non-blocking — but the first of these is now on its fourth pass

**D-R1 (= C-R7, = B-R8 second half).** `tools/md_to_html.py` is an evidence token of this card, and its
own prose still asserts three things the Statement denies, one of them in capitals. Lines 5-7:
"`docs/.nojekyll` turns Jekyll off, **so** a `.md` file is served as a raw download" — the Statement
says "with or without `docs/.nojekyll`". Lines 10-11: "a relative link … is the **same string** in both
trees" — the Statement says the prefix is preserved and the suffix changes. Lines 13-18: "so the subset
**is closed** and small … **A construct outside that subset raises `Unsupported`**" and "Nothing here
guesses" — the Statement opens that paragraph with "THE SUBSET IS NOT CLOSED" and then lists six
constructs outside the subset that do not raise. The comment above `UNSUPPORTED_LINE` (now ~244) still
reads "This is what makes the subset closed". Repair: delete those four passages. A maintainer opens
the file before the card, and the file currently promises a renderer that fails closed. Two referees
have asked; I am asking a third time and recording that the next pass should treat it as blocking,
because the file ships with the repository when it goes public.

**D-R2 (= C7).** "with CommonMark's intraword rule kept for `_`" still describes dead code.
Re-measured my own way: over every 4- and 5-character string on the alphabet `a *_(.)␣`, **26,754**
delimiter positions, the `_`-specific clause changes **0** verdicts, because `opens = left and
_ws(before)` already forces `right` false. `*` and `_` behave identically. The promised behaviour holds
for a different reason. One clause: "and `*` and `_` behave identically under it".

**D-R3 (= C8).** Still live as a class: `esc()` in `build_docs.py` writes `https://example.com/a_\_b`
and `https://example.com/x\*y`, and `BARE_URL` swallows the backslash into the `href`
(`href="https://example.com/a_\_b"`), which `check_links` never fetches. The one URL in the corpus has
no metacharacter.

**D-R4.** How to verify: "they differ in 14 characters, all of them GitHub deleting mathematics" →
add "(setting aside three positions on `notation.md` where GitHub's `<math-renderer>` double-escapes
`<` and `>` inside `$…$`, which is not a Markdown difference)".

**D-R5.** Two small wording slips, both pre-existing and neither introduced here. "REF-CI-PAGES-B then
found that the repair itself had introduced **two** more, both now fixed:" is followed by a colon-list
of **five** items, four of which are REF-CI-PAGES's; B's own two are listed correctly further down.
And `blocks()` still has `line.lstrip().startswith("<!--")`, which the widened guard has made
unreachable for any indented comment.

---

## 2. `generated-docs` — **FAIL**

### 2.1 What is repaired

| REF-PASS-C finding | state now [D] |
|---|---|
| **C-R8**, the line count stale for a third pass (1300 → 1400 → 1427 → 1452) | **dropped entirely**, which is the better of the two options offered. `wc -l` is 1452 today; nothing in the card depends on it and no fifth finding can be spent on it |
| **C-R9**, "65 files" false of a generator that writes 131 | the count is now **131** and `docs/read/` is named — but the sentence that carries it is new and is wrong in two ways. See D-D1 |

Everything else in the Statement re-measured, not read [D]: 7 + 58 = **65** `.md` and **66** `.html`,
**131** total, all git-tracked; `build_docs --check` prints `claims 90 (3 refereed, 30 proved, 22
numerical, 3 conjectural, 5 verified, 5 open, 14 active, 5 done, 2 superseded, 1 refuted)` and
`pages under results/: 58`, so 58 and 30/3/22/3 of 90 are exact; **783** internal link targets over the
65 sources with **0** external; **36** source rows in `refs/REFERENCES.md` (38 lines start with a bar,
less header and alignment); the nine privately held evidence pointers are printed by name on every run
and there are exactly nine; "held privately, not redistributed" appears on **7** bullets across **6**
result pages (`sequential-recovery-bound-type-iii` twice), all six the source PDFs; the drift guard
fires on a changed byte in `index.md`, a changed byte under `read/`, and a planted orphan under
`read/results/`, and returns to `131 pages up to date` when they are restored.

### 2.2 The new defect

**D-D1 — the rewritten first sentence says two things that are false, and one of them is the
arithmetic this card has already been failed for once.** It now reads:

> "… 131 files, namely 65 Markdown sources -- seven top-level pages (index, status, notation,
> definitions, open, sources, history) and 58 per-claim pages under docs/results/ -- **and their 66
> HTML renderings under docs/read/, which is the mirror docs-pages-rendering describes for every card
> at status proved, refereed, numerical or conjectural** (30 proved, 3 refereed, 22 numerical, 3
> conjectural of the 90 cards the knowledge base now lists; …)"

*(i) "their 66 HTML renderings".* "Their" is the 65 Markdown sources. Sixty-five sources do not have
sixty-six renderings. Sixty-five of the files under `docs/read/` are renderings of a source; the
sixty-sixth, `read/results/index.html`, is generated and renders nothing — as this card's own dated
correction note spells out ("7 + 58 mirrors + the generated read/results/index.html"), and as
REF-CI-PAGES's DEFECT 3 already established when it failed the earlier note for double-counting that
same index. C-R9 gave the parenthesis "(7 top-level, 58 mirrors and a generated results index)"
precisely to stop this; it was dropped.

*(ii) The qualifier is attached to the wrong noun.* Before this commit the sentence read "… and 58
per-claim pages under docs/results/ **for every card at status proved, refereed, numerical or
conjectural** (30 proved, 3 refereed, 22 numerical, 3 conjectural …)", where the rule and its
breakdown explained the **58**. The insertion moved the rule and its breakdown across the em-dash so
that they now qualify the **66** renderings and the mirror. There is no reading in which that is true:
the 66 are not one per qualifying card, and 30 + 3 + 22 + 3 = 58, so the sentence supplies its own
refutation. The seven top-level pages, which the same sentence lists, are not per-card at all.

This is the fourth consecutive pass on this one sentence and the third referee to be spent on it. Both
errors are of exactly the kind the card is supposed to be immune to — its second sentence is "Every
count is computed, never typed", and these two are typed.

### 2.3 Exact repair

**D-R6.** Replace

> "generates the public documentation subfolder from the knowledge base: 131 files, namely 65 Markdown sources -- seven top-level pages (index, status, notation, definitions, open, sources, history) and 58 per-claim pages under docs/results/ -- and their 66 HTML renderings under docs/read/, which is the mirror docs-pages-rendering describes for every card at status proved, refereed, numerical or conjectural (30 proved, 3 refereed, 22 numerical, 3 conjectural of the 90 cards the knowledge base now lists; the count moves with the knowledge base, and docs/status.md carries the current figure and is inside the drift guard)."

with

> "generates the public documentation subfolder from the knowledge base: 131 files. Sixty-five are Markdown sources -- seven top-level pages (index, status, notation, definitions, open, sources, history) and one per-claim page under docs/results/ for every card at status proved, refereed, numerical or conjectural, 58 of them (30 proved, 3 refereed, 22 numerical, 3 conjectural of the 90 cards the knowledge base now lists; the count moves with the knowledge base, and docs/status.md carries the current figure and is inside the drift guard). The other 66 are the HTML mirror under docs/read/ that md_to_html.py writes and docs-pages-rendering describes: 7 top-level pages, 58 result pages and one generated results index, which is a page in its own right and not a rendering of any source. All 131 are inside the drift guard."

The last sentence is C-R9's and is still worth having: the Statement's own drift-guard sentence lists
"a changed byte, a stale results page, a deleted results page and a changed card, and now also an
orphan top-level page" and never mentions `docs/read/`, although `--check` covers it recursively and I
retested that it does.

**D-R7, non-blocking.** `## How to verify` has been **empty** through five referee passes. For a tool
card that is the one field a reader can execute. Suggested: "`make check` — `build_docs.py --check`
prints `131 pages up to date`, the claim counts, `pages under results/: 58` and the nine privately
held evidence pointers by name, and exits 0 on a clean tree; break any of a byte in a page, a planted
page under `docs/results/` or `docs/read/`, or a card in the knowledge base, and it exits 1 naming the
file."

---

## 3. `repo-split-public-private` — **FAIL**

### 3.1 The REF-PASS-C findings

| finding | state now [D] | verdict |
|---|---|---|
| **C12 / C-R15**, the `next` field contradicted the Statement and `CHECKLIST.md` | rewritten, and the contradiction is gone: it now says publication is BLOCKED by one open item and names both remedies. But the rewrite ends in a new false sentence — **D-D2** | **REPAIRED, and newly broken** |
| **C11 / C-R14**, the events endpoint is a wider publisher | the Statement now carries "44 pre-rewrite commits across 53 push events, 29 of which were never a workflow head, so the Actions list is not even the widest publisher". Re-measured: **53 PushEvents, 55 distinct SHAs, 44 absent from the local history, 29 of those never a workflow head** — exact | **REPAIRED, exact** |
| **C-R12**, "the 97 result captures" | the number is gone and the sentence now reads "**and the the** result captures the KB cites as evidence" -- and deleting it was the wrong half of the fix, because **97 is exact**. See D-D3 | **BOTH HALVES WRONG — D-D3** |
| **C-R10**, the private enumeration is six files short of its own count | **unchanged.** "the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude" is 178 + 47 + 4 = **229**, in a parenthesis whose own count is 235 | **NOT REPAIRED — D-D4** |
| **C-R11**, "(196 MB)" | **unchanged** | **NOT REPAIRED — D-D5** |
| **C-R13**, "614 files, 7.93 MB" | **unchanged** | **NOT REPAIRED — D-D6** |
| **C-R16**, the comma splice | gone with the sentence | **REPAIRED** |

Unbroken and re-measured [D]: overlap **0** (`comm -12` over both `ls-files`); `rigor/shots` **178**
files, all 178 privately tracked; `refs/*.pdf` **47**, all 47 privately tracked; **256** `\shot`/`\shotc`
invocations across 20 `.tex` files less the one in the `\shotc` definition in `rigor_preamble.tex` =
**255 in 19 documents**; **24** tracked `.py` files define a computed `_ROOT`; **49** `rigor/*.tex` on
disk against **44** public-tracked, the difference being the five compendia; the remote is `private:
true`, `fork: false`, `forks_count: 0`, **1** collaborator; the single tag `v0.1.0-draft` resolves to
`5ad78cb` and its tree does contain `plan_page/petz_program_plan.html`; the release carries exactly
`cft-cmi-paper1-free-fermion.pdf` and `cft-cmi-paper2-universality.pdf`.

### 3.2 The counts, re-measured

| card says | measured at `bbaa665` [D] |
|---|---|
| public `.git`: **614 files, 7.93 MB** | **617 files, 8,062,559 B = 8.06 MB** |
| private `.git-private`: **235 files, 48.4 MB** | **235 files, 48,390,067 B = 48.39 MB** — exact |
| the private enumeration | 178 + 47 + 4 = **229**. The real 235 is 178 excerpts + 47 PDFs + **the five compendia** + **plan_page/petz_program_plan.html** + CHECKLIST.md + PRIVATE.md + pgit + pgit-exclude; `git --git-dir=.git-private ls-files` outside `rigor/shots/` and `refs/*.pdf` lists exactly those ten |
| tracked by neither: **(196 MB)** | **423 files, 198,646,582 B = 198.6 MB** |
| **15 of the 28** Actions head SHAs | `/actions/runs` now serves **29** runs (24 failure, 5 success), 29 distinct head SHAs, **15** absent locally. The 29th is run 35617651060 at **`bbaa665` — the commit under review**, exactly as the line counts did to `generated-docs` |
| **44 across 53 push events, 29 never a workflow head** | exact |

### 3.3 The exposure, and who publishes it

**Unchanged, re-derived by REST only** [D]: `GET /repos/…/commits/5d64c77…` resolves and returns
"referee report on the build repairs", `GET /repos/…/contents/rigor/cited_results_all.tex?ref=5d64c77…`
returns **299,915** bytes, and `git cat-file -t` on the same SHA fails locally
("could not get object info"). Nothing about the exposure has moved.

**D-D7 — a further publisher that no note has named: `GET /repos/{owner}/{repo}/activity`.** It serves
**58** entries — 56 `push`, one `branch_creation`, one **`force_push`** — carrying `before` and `after`
for each, **44** of the 58 distinct SHAs absent from the local history. It adds no SHA the other two
endpoints lack, so the extent of the exposure is unchanged; what it adds is worse than a new SHA. The
single `force_push` row is

```
activity_type force_push   before 8b96354352eec21a57631f994e9816ea53c72147   -> after 8bbd412e1b…
timestamp 2026-09-21T10:28:34Z
```

so the endpoint does not merely leak hashes among which some are pre-rewrite: it **labels the rewrite**,
timestamps it and hands the reader the discarded head by name. Every other publisher leaves a reader to
work out which SHAs the rewrite dropped. A fifth publisher carries the same 44:
`GET /users/alexander-stottmeister/events` (55 events for this repository, 53 pushes, 55 distinct SHAs,
44 pre-rewrite), which is the actor's timeline rather than the repository's and would survive the
repository's own event feed ageing out.

**D-D8 — the Statement stopped spelling out the route on the ground that it ships to the public site,
and the route ships anyway, in four files of the same repository, two of which the Statement now names.**

The public *site* is clean, and I checked that properly rather than assuming it: every `[0-9a-f]{7,40}`
token anywhere under `docs/` — **352** distinct strings across the JSON, HTML, Markdown, JS and CSS —
resolves to a local commit in three cases (`5a3988b`, `7cae480`, `9aed69a`) and in **zero** cases to a
commit that the remote serves and the local history lacks. `docs/data/extra-claim-map.json` carries the
Statement and `next` verbatim and neither contains a hash, a `git fetch`, a `?ref=` or a `git/blobs`
path. Module 10 renders nothing more. That part of the repair works.

But `git ls-files` tracks these four, and the repository is what goes public:

| public-tracked file | what it publishes |
|---|---|
| `rigor/referee_compendia_move.md` | "They entered in `8ab5a32` (initial import) … Deleting them from the tip left the blobs intact: **`git show ba14962^:rigor/cited_R1.tex` returns all 70,874 bytes**, and all five recover byte-for-byte (~600 kB, every one of the 144 transcriptions)" — a one-line recipe, simpler than any REST route |
| `rigor/referee_plan_split.md` | 17 hits. The full 40-character commit SHA, the full 40-character blob SHA, **`git --git-dir=<mirror> fetch origin 5d64c77…`**, **`gh api repos/…/contents/rigor/cited_results_all.tex?ref=5d64c77…`**, **`gh api repos/…/git/blobs/18cc05ab…`**, the five byte sizes, and eight short SHAs with the note that every one "resolves through the API right now" |
| `rigor/referee_pass_c.md` | 7 hits. `GET /commits/5d64c77…`, `GET /contents/…?ref=5d64c77…`, `GET /git/blobs/18cc05ab…`, and `04af962…` as a worked example of a SHA that was never a workflow head |
| `rigor/referee_repo_split.md` | 1 hit |

So the Statement's sentence — "the routes are recorded in `rigor/referee_plan_split.md` and
`rigor/referee_pass_c.md` and are deliberately not spelled out here, because this Statement itself ships
to the public site" — removes nothing from the public surface and adds a signpost to two of the four
files that hold it. If the reason is sound, it applies with more force to a file that can be read with
`cat`.

**Does it need to change?** My judgement, stated plainly as asked: **the referee notes should not be
rewritten, and they should not stay public.** Rewriting them is barred by the author rule and would in
any case destroy the record that the exposure was found and confirmed. But "the pre-rewrite hashes are
not confidential" — which the card argues correctly, since the API publishes them — is an argument about
*hashes*, not about a copy-pasteable command that yields 600 kB of third-party quotations, and it is an
argument about a repository that is private today. The four notes should move to the private companion
(`pgit`'s `PRIVATE_PATHS`) before the repository is made public, or, if the record must stay public,
each command should be reduced to a sentence that says a route exists without giving the ref. The Statement
should then say where they went. Either way the card cannot go on justifying its own redaction by a
property the repository does not have.

### 3.4 The `next` field

It now agrees with the Statement (publication blocked, one gating item, the same two remedies) and with
`CHECKLIST.md` item 3 ("RESIDUAL, AND IT BLOCKS GOING PUBLIC", the same two remedies) and with
`PRIVATE.md:79-81` ("Residual, and it blocks going public"). It ships verbatim into
`docs/data/extra-claim-map.json`, where I read it rather than the card, and the two are identical.
C12 is properly closed. Its last sentence, however, is new and false:

**D-D2 — "CHECKLIST.md item 3 records both" is false of the second of the two.** `grep -c
'plan_page\|petz_program' CHECKLIST.md` = **0**: the word does not occur anywhere in the file, let alone
in item 3, which is about the compendia and only the compendia. `PRIVATE.md` does not record it either —
it names `plan_page/petz_program_plan.html` twice (lines 13 and 63) as private *material*, never as a
path still reachable in the public history and in the tree of the pushed tag. So the one document a
reader is sent to for the second item does not contain it. This is the same species as C12: a sentence
in the one field of this card that a reader of the public site meets, asserting something about its own
evidence document that the document does not say.

One smaller mismatch in the same family, non-blocking: `CHECKLIST.md` item 3 says "the repository's own
Actions API publishes the pre-rewrite head SHAs", while the Statement and `next` now say Actions **and**
events. Item 3 should gain "and its events and activity endpoints, more widely still".

### 3.5 Exact repair

**D-R8.** In `next`, replace

> "A second, lesser item: plan_page/petz_program_plan.html is reachable in the public history and in the tree of the pushed tag v0.1.0-draft. CHECKLIST.md item 3 records both."

with

> "A second, lesser item, which CHECKLIST.md does not yet record: plan_page/petz_program_plan.html is reachable in the public history and in the tree of the pushed tag v0.1.0-draft, and clearing it needs the same purge or recreation. CHECKLIST.md item 3 records the first."

and add the path to `CHECKLIST.md` item 3 (or open an item 7 for it), since the card's own evidence must
carry what the card says it carries.

**D-D3 — "97" reproduces exactly, my two predecessors both missed it by scanning one directory, and
the repair deleted a true number and left the sentence ungrammatical.** The clause now reads
"numerics scripts and **the the** result captures the KB cites as evidence", which no reader can parse
and which no proof-read survives.

REF-PLAN-SPLIT (R-B2) and REF-PASS-C (C-R12) both reported that no rule produces 97; REF-PASS-C listed
".out 83, +.txt 102, +.err 104, +.raw 110, +.md 116". Those figures are `numerics/` only. Over the
whole public repository [D]:

```
git ls-files '*.out' | wc -l        ->  97      (83 under numerics/, 14 under rigor/)
git ls-files '*.txt' | wc -l        ->  19
git ls-files '*.err' | wc -l        ->   2
```

**97 is exactly the number of tracked `.out` run captures**, and it was exact at `6100643` too. What
was false in the clause was not the count but the qualifier: only **23** `.out` files are named by a
card (23 by the front-matter `evidence:` key, 23 by any `doc:`/`num:`/`ref:` token anywhere in the 322
cards, all 23 tracked), so "the 97 result captures **the KB cites as evidence**" describes 23 files with
a count of 97.

**D-R9.** Restore the number and fix what was actually wrong. Replace "and the the result captures the
KB cites as evidence" with

> "and the 97 tracked .out run captures, 23 of which a card cites as evidence"

That is checkable in one command each, and it closes C-R12 properly: the rule is stated and the figure
is right.

**D-R10 (= C-R10, verbatim from REF-PASS-C, still not applied).** Replace

> "(235 files, 48.4 MB as of 2026-09-21: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude)"

with

> "(235 files, 48.4 MB as of 2026-09-21: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, the five cited-result compendia rigor/cited_R1-R4.tex and cited_results_all.tex, plan_page/petz_program_plan.html, CHECKLIST.md, PRIVATE.md, pgit and pgit-exclude -- the list pgit's PRIVATE_PATHS enforces, and it adds to 235)"

I re-derived the ten non-shot, non-PDF entries from `git --git-dir=.git-private ls-files`; 178 + 47 + 10
= 235 exactly.

**D-R11 (= C-R11).** `(196 MB)` → **`(about 199 MB over 423 files)`**.

**D-R12 (= C-R13).** `614 files, 7.93 MB as of 2026-09-21` → **`617 files, about 8 MB at bbaa665`**, or
drop the byte figure and keep the hedge that already follows it. This number has now been wrong at four
consecutive passes and the hedge "the figure moves with every commit" is doing no work while an exact
figure sits in front of it.

**D-R13.** `15 of the 28 head SHAs it serves` → **`15 of the 29 it currently lists`**, and restore the
clause C-R14 asked for and the repair dropped: **"both counts grow with ordinary use"**. The 28 became
29 because the commit that wrote "28" triggered a run.

**D-R14.** Act on D-D7 and D-D8. In the Statement, after the events clause:

> "and /repos/.../activity, a third endpoint, serves the before and after SHA of all 58 recorded pushes and, in one row, labels the force-push itself with the pre-rewrite head it replaced, so a reader does not even have to work out which SHAs the rewrite discarded; the same 44 appear in /users/<owner>/events."

and, for the redaction:

> "The routes are not spelled out here because this Statement ships to the public site; they are recorded in the referee notes rigor/referee_compendia_move.md, referee_plan_split.md, referee_pass_c.md and referee_repo_split.md, which are TRACKED BY THE PUBLIC REPOSITORY and must be moved to the private companion before it is made public."

---

## 4. The gates, run by me

`make check` — **exit 0** on a clean tree:

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
      refs/Sion1958_minimax.pdf … plan_page/petz_program_plan.html, PRIVATE.md,
      CHECKLIST.md, refs/Uhlmann76.pdf, refs/VWZ_2307.14434.pdf
  cards never refereed: 0 of the 90 listed (0 with a page); 232 of the 322 …
  cards awaiting a referee pass: 3 (docs-pages-rendering, generated-docs,
             repo-split-public-private)
  cards whose last referee pass failed: 0
  … nine data files ok, page record references: all resolve
```

`make rigor` — **exit 0**: `46 document(s), 0 failing, 0 known`.

`kb -p cft_cmi lint` — `0 issue(s), 3 awaiting review`, the three under review here.

This is the second consecutive pass at which both gates are green at HEAD.

I then ran both again **after** recording the three verdicts. `make rigor` is unchanged, exit 0,
`46 document(s), 0 failing, 0 known`. `make check` is **exit 2**, and the whole drift is the review
state the verdicts just moved: `docs/status.md:23` and `docs/read/status.html:54`
"**0 carry a failed referee pass**" → "**2**", and three table rows going `review pending` →
`referee pass failed` / `review passed`. `check_links` still prints `155 pages, 2211 links resolve`.
That is rule (c) working as REF-DOCS-1c agreed, not a regression; run `make docs data` and commit.
The only file I added to the working tree is this one.

---

## 5. Consistency

`kb -p cft_cmi q --text` over *compendia*, *docs/read*, *Pages* and *mirror*, plus a grep of every card
for `compendia`. **No card contradicts another.** `ci-green`'s "49 rigor/*.tex on disk, 44 tracked, the
5 untracked cited_R* compendia making the difference" reproduces exactly. `longo-xu-cmi` carries a
referee note that publishes `8ab5a32` and `ba14962` with the `git show` recipe, but that note lives in
the knowledge base, not in `cft_cmi`, and is not rendered onto its result page
(`grep -c '[0-9a-f]\{7\}' docs/results/longo-xu-cmi.md` = 0); its public counterpart
`rigor/referee_compendia_move.md` is covered by D-D8.

The one contradiction that remains is inside `repo-split-public-private`, between its `next` field and
`CHECKLIST.md` — the same place as last time, in the same field, for a different sentence.
