# REF-CI-PAGES-B: second pass on ci-green, docs-pages-rendering, generated-docs (2026-09-21)

All three FAIL again, but not for the same reasons and not to the same degree.

`generated-docs` fixed all three numbers it was failed for and has one more stale number in the
same Statement, which I found by running the generator rather than by reading the card.
`ci-green` fixed both findings exactly and completely; it fails on one sentence, and on a new
false comment the repair commit put into its own evidence file, about enabling Pages.
`docs-pages-rendering` is the serious one. The five named character-level defects are repaired,
verified line by line. But the repair that fixed them introduced four new ones on the two pages
this card exists to make readable, it left six more asterisks of mathematics deleted on a page it
declares repaired, and the closure claim — which the first pass refuted — has been *escalated*
rather than withdrawn, and is still false.

Measurements marked [REF-B] are mine, made at HEAD = b9daa45 unless a commit is named. The failing
state the first pass reviewed is 5a3988b. The working tree was clean before and after every test
(`git status --porcelain` empty, checked after each; `make rigor` and the one claim-map
regeneration were both restored/left byte-identical). No git command that writes was run.

---

## 0. Method for "is anything NEW broken"

I extracted the visible text of all **66** mirror pages at 5a3988b and at HEAD and diffed them
page by page. 66/66 pages exist at both commits, none added, none removed; **37** pages differ in
their rendered text and 37 differ in their raw bytes, i.e. there is no page whose HTML changed
without its text changing. Every one of the 37 is accounted for below; four of them are
regressions.

| difference | pages | intended? |
|---|---|---|
| `_None recorded._` → emphasis | 27 result pages | yes (underscore emphasis) |
| `_no result recorded in the table_` → emphasis, ×7 | `sources.html` | yes |
| three `<title>`/`<meta>` de-escapings (`\~20%`, `\<=`, `V^\V`) | 3 result pages + `results/index.html` | yes |
| `history.md:143` adjoint stars restored | `history.html` | yes |
| `history.md:219` row back to 2 cells, `\|\|u\|\|^2` intact | `history.html` | yes |
| `notation.md:119,123` rows back to 3 cells | `notation.html` | yes |
| `done 3 → 5`, `88 → 90 cards`, two new status rows, `review pending` markers | `index.html`, `status.html` | yes (knowledge base moved) |
| **LaTeX subscripts swallowed by new `_` emphasis** | **`notation.html` ×3, `definitions.html` ×1** | **NO — regression** |

---

## 1. `ci-green` — **FAIL** (one sentence, plus a new false comment in its own evidence file)

### The two first-pass findings

| first-pass finding | state now [REF-B] | verdict |
|---|---|---|
| DEFECT 1: "texlive-pictures was not [named] … lmodern was missing on the same argument" — cause inverted | Statement rewritten. Re-checked from scratch: `git show 9aed69a^:.github/workflows/check.yml` line 41 shows the old apt line was `texlive-latex-recommended texlive-latex-extra texlive-science texlive-fonts-recommended` — texlive-pictures indeed **not named**; and `gh run view 35595433844 --log` on that same (failing) run prints `Unpacking texlive-pictures (2023.20240207-1)` and `Setting up texlive-pictures (2023.20240207-1)`, so it arrived as a dependency and was present the whole time. `Setting up fonts-lmodern (2.005-1)` is in the same failing log. `paper1/main.tex:2`, `paper2/main.tex:2` and `rigor/rigor_preamble.tex:2` are each `\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{microtype}`; `\usepackage{tikz}` is `paper1/main.tex:6`. | **REPAIRED, exactly** |
| DEFECT 1 (b): the same false explanation committed as a code comment at `check.yml:43-46` | replaced, and the replacement is accurate on every clause I can check | **REPAIRED** |
| DEFECT 2: `--allow-missing-kb` presented as closed while CI is the place the claim map rots | the `WHAT THE FLAG DOES NOT DO` sentences are added and are honest: they name the drift, say nothing on the runner can rebuild it, and name `make check` beside the knowledge base as the only catch. The flag's code is byte-unchanged (`tools/build_site_data_extra.py` is not in `git diff 5a3988b HEAD`), so the first pass's four-way test still stands. | **REPAIRED** |
| DEFECT 2 (b): the claim map was drifted at 5a3988b | **regenerated, verified against the file not the claim**: cards 88 → 90 with exactly `ci-green` and `docs-pages-rendering` added; edges 147 → **153**, the six new ones being exactly `ci-green→{generated-docs, interactive-site, repo-split-public-private}` and `docs-pages-rendering→{generated-docs, interactive-site, public-site-plan}`, which are precisely the two cards' `related:` fields. Both node ids occur 5× each in the committed JSON. | **REPAIRED, exact** |

Counts re-measured, not accepted: `gh run list --limit 200` now gives **24 failure, 3 success**
(the third is 35608586477 on b9daa45 — CI is green on the repair commit); 35602149545 is still the
first success; 24 → 0 successes before it holds. `make rigor` runs: see §4.

### DEFECT B1 — the pages sentence, and the new comment under it. **BLOCKING.**

The repair commit added this to `.github/workflows/check.yml:59-62`, which is a `doc:` evidence
token of this card:

> "Removing the `if: false` is the whole of what publishing needs once the repository is public:
> `enablement: true` turns Pages on and sets its source to this workflow, so no click in Settings is
> required…"

and `with: { enablement: true }` on `actions/configure-pages@v5`.

`enablement` is a real input, and it does call `POST /repos/{owner}/{repo}/pages` with
`build_type: 'workflow'` (`src/api-client.js`, `enablePagesSite`, at ref v5). But the action's own
`action.yml` **at the pinned ref v5** documents it as:

> "Try to enable Pages for the repository if it is not already enabled. **This option requires a
> token other than `GITHUB_TOKEN` to be provided.** In the context of a Personal Access Token, the
> `repo` scope or Pages write permission is required. In the context of a GitHub App, the
> `administration:write` and `pages:write` permissions are required."

The job passes no `token:`, so `githubToken` defaults to `${{ github.token }}` — the GITHUB_TOKEN
the action says will not do. `permissions: { pages: write, id-token: write }` cannot close the gap:
`administration` is not a key of the workflow `permissions:` schema, so the default token can never
carry it, and `POST /repos/{owner}/{repo}/pages` requires Administration (write) as well as Pages
(write). `index.js` has no soft path: `findOrCreatePagesSite` rethrows, `main()` calls
`core.setFailed(error); process.exit(1)`. So removing `if: false` on a public repository with Pages
still off gives a **failed pages job**, not a published site.

I cannot run the job (it is `if: false` and the repository is private), so this rests on the
action's own documentation at the ref the workflow pins, which is the same standard the card itself
uses for `--no-install-recommends`.

Consequently the card's own last-but-one sentence is wrong in the same way the first pass failed the
sibling card for:

> "The pages job stays behind `if: false` by decision D1; it is enabled when the repository goes public."

Going public enables nothing: someone must delete a line, and someone must turn Pages on. The
project's own D1, at `rigor/public_site_plan.md:226-228`, still says it correctly — "enabling it is
one line **plus one click**". The card and the new comment now contradict the decision document they
are implementing.

Smaller, non-blocking: the TeX Live comment says lmodern's "absence is what failed **every run**
before 9aed69a". It failed every *papers* job; the `generated-artefacts` job failed independently on
the claim map, as this card's own "(1)" says. In a comment on the TeX Live step a reader will read
it locally, but the wording overstates.

### Exact repair (two edits; nothing else changes)

**B-R1.** Replace, in the Statement:

> "The pages job stays behind if: false by decision D1; it is enabled when the repository goes public."

with:

> "The pages job stays behind `if: false` by decision D1. Publishing needs three things, not one: the
repository going public (the free tier serves Pages for public repositories only), that `if: false`
being deleted, and Pages being enabled on the repository — `gh api repos/alexander-stottmeister/cft-cmi`
still reports `has_pages: false` and `/pages` 404s. The `enablement: true` now passed to
actions/configure-pages@v5 does NOT remove the third: the action's own action.yml at v5 says the
option 'requires a token other than GITHUB_TOKEN to be provided', the job passes no token: override,
and `POST /repos/{owner}/{repo}/pages` needs Administration (write), which is not a key of the
workflow permissions schema. As written the job would fail rather than publish. `rigor/public_site_plan.md:226`
states the real condition: one line plus one click."

**B-R2.** Replace the `check.yml` comment above the `pages:` job:

> "Removing the `if: false` is the whole of what publishing needs once the repository is public:
> `enablement: true` turns Pages on and sets its source to this workflow, so no click in Settings is
> required, and the free tier serves Pages for public repositories only, which is why it waits
> (decision D1)."

with:

> "Written and disabled. The free tier serves Pages for public repositories only, which is why it
> waits (decision D1). Enabling it needs the `if: false` removed AND Pages turned on for the
> repository. `enablement: true` is here so that the second step can be automated later, but it does
> not work with the default GITHUB_TOKEN — actions/configure-pages@v5 documents the input as
> requiring a token with Administration (write), which a workflow `permissions:` block cannot grant —
> so either enable Pages once in Settings, or pass a PAT as `token:`."

Either keep `enablement: true` with that honest comment, or supply the token; do not leave the
claim that it removes the click.

---

## 2. `docs-pages-rendering` — **FAIL**

### The three first-pass findings

| first-pass finding | state now [REF-B] | verdict |
|---|---|---|
| DEFECT 1 (instance): `history.md:143` "N = 1 - XX* >= 0 … X* <= N", both adjoint stars deleted, 40 chars italicised | `docs/read/history.html:132` now reads `N = 1 - XX* &gt;= 0 and 0 &lt;= Y = Z - X Q_BB X* &lt;= N`. No `<em>` anywhere on the line; the page's `<em>` count fell from 3 lines to 2. Flanking is why: the star is preceded by `X` and followed by a space, so it is not left-flanking and cannot open. | **REPAIRED** |
| DEFECT 1 (instance): `notation.md:119,123` → 5- and 9-cell rows in a 3-column table | both are **3 cells** at `docs/read/notation.html:127,131`. The fix is **upstream and real**: `docs/notation.md` itself changed (`\\|` → `\|`), so GitHub's own rendering of that file is repaired too — GFM resolves `\|` to a literal pipe at table-parse time, giving 3 cells there as well. `tabular_to_md` now escapes only an unescaped bar, `re.sub(r"(?<!\\)\|", r"\\|", c)`. `split_row`'s new `.replace("\\|", "|")` is not a paper-over: GFM resolves the escape before inline parsing, so the renderer has to do the same. | **REPAIRED, upstream, and GitHub is repaired with it** |
| DEFECT 1 (instance): `history.md:219` → 10-cell row under a 2-column header | `docs/read/history.html:204` has **exactly 2 `<td>`** and `<code>||u||^2</code>` twice, intact. Upstream again: `docs/history.md:219` now carries `\|\|u\|\|^2` inside the code spans, which is what GFM needs (spec example 200: `\|` is resolved inside a code span in a table), so GitHub renders 2 cells too. | **REPAIRED, upstream** |
| DEFECT 1 (instance): underscore emphasis unimplemented, literal `_` on 28 of 66 pages | implemented. 27 result pages (`_None recorded._`) plus 7 sites on `sources.html` = the 28. The intraword rule works: 1068 literal `_…_`-shaped runs remain in the bodies and they are LaTeX subscripts, correctly untouched. | **REPAIRED — and see B2, it broke four other places** |
| DEFECT 1 (instance): three `<title>`s disagree with their own `<h1>` | **0 mismatches in 66/66 pages**, checked mechanically (`<title>` minus `" — cft-cmi"` against the tag-stripped `<h1>`). `title_of` now renders through `plain()`. | **REPAIRED, and better than asked** |
| DEFECT 2: "loses no source word (only the anchor ids)" | the parenthetical is gone; the Statement now says word-level fidelity is not character-level fidelity and names the five defects | wording repaired, **but the substance is not** — see B2, B3 |
| DEFECT 3 (a): "the Pages address … in section 9" | still false, differently — see B4 | **STILL FALSE** |
| DEFECT 3 (b): "the site goes live when this repository becomes public" | README:34-37 rewritten and now opens **"That address does not serve anything yet."** That much is right and prominent. But the two-condition claim under it is false — see B5 | **half repaired** |
| ALSO: loose `.nojekyll` causality | Statement rewritten to "a .md file with no YAML front matter is a static file and is served verbatim … with or without docs/.nojekyll" | **REPAIRED** |
| ALSO: content-type measured with the wrong instrument | "How to verify" now says outright that it measures Python's mimetypes table, not GitHub's, and that Pages has never been enabled | **REPAIRED, honest** |
| VERIFIABILITY: `make check` exits 2 | the recipe is now conditional ("After `make docs data`, make check is green"), which is fair. But one number in it is stale — see B6 | **conditionally repaired** |
| NON-BLOCKING: fourth link class | added: "A fourth, per page and by design: each mirror page's footer links to its own .md source on github.com" | **ADDRESSED** |
| NON-BLOCKING: "the same string in both trees" | reworded to "the directory prefix … is preserved and only the suffix changes" | **ADDRESSED in the card** (not in the module docstring, `md_to_html.py:10-11`, which still says the false version) |

Also verified at HEAD: `tools/md_to_html.py` is 494 lines and imports only `html`, `posixpath`, `re`
(stdlib only, as claimed); 65 Markdown + 66 HTML = **131** files, recounted; `check_links.py`'s
Markdown-pattern fix is exact — applying the old pattern to HTML reports exactly **three** phantom
links, all in `docs/read/definitions.html` (`](p)`, `](p_k)`, `](p)`).

### DEFECT B1 — "THE SUBSET IS CLOSED" is still false, and it has been escalated. **BLOCKING.**

The first pass's R1 asked the card to say "It is **not** closed". The card now says the opposite,
in capitals:

> "THE SUBSET IS CLOSED, and this is enforced rather than intended: reject_unsupported() raises
> Unsupported on … ; the paragraph branch is the fallback for prose, never for an unrecognised
> construct."

`reject_unsupported()` is a blacklist of seven line patterns and seven inline patterns. A blacklist
does not make a subset closed; it makes the named constructs loud and leaves everything else
silent. Twenty constructs, all tested through `md_to_html.render_page` with the real `make_link`:

| construct | result | CommonMark / GFM | verdict |
|---|---|---|---|
| `Copyright &copy; 2026` | `&amp;copy;` — reader sees `&copy;` | `©` | **wrong, silent** |
| `&#189;`, `&lt;` (incl. in a table cell) | shown literally | `½`, `<` | **wrong, silent** |
| `See https://example.com/x.` | plain text | GFM autolink → a link | **wrong, silent.** LIVE: `docs/sources.md:25` → `docs/read/sources.html:59`, a bare Project Euclid URL that is a link on GitHub and dead text in the mirror |
| `a <b and c` (mid-line `<` + letter) | `a &lt;b and c` | same | correct |
| `x<sub>2</sub>`, `One<br>Two` mid-line | escaped, shown as text | raw HTML | **wrong, silent** (the guard is anchored `^\s*<`, line start only). Not live: the generator escapes `\<`, e.g. `docs/results/stress-tensor-normalisation.md:11` |
| table with no leading pipes | one paragraph | a table | **wrong, silent** |
| **table row with the trailing pipe missing** (`\| c \| d`) | **1 cell; the cell `d` is deleted** | 2 cells | **wrong, silent, destructive** |
| a row without a leading pipe among rows that have one | table truncated, row becomes a paragraph | GFM spec ex. 206: it is a row | **wrong, silent** |
| heading with one trailing space | fine | fine | correct |
| heading with two trailing spaces | raises "hard line break" | a heading | spurious, but **fails closed** |
| `+ one` bullets | one paragraph | a list | **wrong, silent** |
| `> foo` / `bar` (lazy continuation) | blockquote + separate paragraph | one blockquote | **wrong, silent** |
| `` `a``b` `` | `<code>a</code><code>b</code>` | `<code>a``b</code>` | **wrong, silent** |
| ``` ``a ` b`` ``` (code span containing a backtick) | `<code></code>a <code> b</code>` + a loose backtick | `<code>a ` b</code>` | **wrong, silent** |
| `*foo` / `bar*` across a line break | `<em>foo\nbar</em>` | same | correct |
| `[t](results/f(1).md)` | `href="../results/f(1"` then literal `.md)` | balanced parens are legal | **wrong, silent** |
| `[t](my file.md)` | a link, `href="my file.html"` | **not a link at all** | **wrong** (caught downstream: `check_links` reports it) |
| `[t](<my file.md>)` | `href="&lt;my file.md&gt;"` | `href="my file.md"` | **wrong, silent** |
| `___` on its own line | `<p>___</p>` | `<hr>` | **wrong, silent** (`***` raises) |
| `___foo___` | `<strong>_foo</strong>_` | `<em><strong>foo</strong></em>` | **wrong, silent** (`***foo***` raises — the triple-emphasis guard covers `*` only, and `_` is the delimiter this commit just added) |
| `* * *` | `<ul><li>* *</li></ul>` | `<hr>` | **wrong, silent** |
| `foo\` + newline | literal backslash | `<br />` | **wrong, silent** (the two-space form raises) |
| `1) one` | one paragraph | an ordered list | **wrong, silent** (`1. one` raises) |
| `before <!-- x --> after` | the reader sees `<!-- x -->` | comment, invisible | **wrong, silent** |
| `[t](index.md 'the title')` | `href="../index.md 'the title'"` | `href="index.md"`, title attribute | **wrong** (the link-title guard matches `"` only) |
| `\*a* b` | `*a* b` | same | correct |

Six of the guard's own entries have a near neighbour it misses (`***`/`___`, `1.`/`1)`,
two-space break/backslash break, `"`-titles/`'`-titles, line-start HTML/mid-line HTML,
`~~`/entities). That is the signature of a blacklist, and it is exactly what the module docstring
warns against: "rendering an unknown line as a paragraph is how a generated page starts quietly
lying."

Two of these are not hypothetical for this generator. `build_docs.history_page` copies **any** line
that starts with `|` verbatim out of `rigor/PHASE*_STATUS.md` and calls it a table row; a prose line
beginning with a norm bar (`|u|^2 moves only 4.7%.` — `rigor/errata_log.md:246`, and four more in
`rigor/phase2_brief.md`, `rigor/phase2b_brief.md`) would become a one-cell row with its tail
deleted. Those files are not the ones `history_page` reads today, so it is latent, not live.

### DEFECT B2 — the flanking repair broke four sites it was not asked about. **BLOCKING, LIVE.**

Adding `_` emphasis put a spurious `<em>` over LaTeX in four places that were correct at 5a3988b.
All four are `|` or `\` immediately before `_`, which makes the underscore punctuation-preceded and
therefore able to open under rule 2:

| source | at 5a3988b | at HEAD | `_` deleted |
|---|---|---|---|
| `docs/notation.md:89` `$\|f\|_{\beta}=\sum_{n}…` | correct | `docs/read/notation.html:98` `$\|f\|<em>{\beta}=\sum</em>{n}…` | 2 |
| `docs/notation.md:90` `$\|G\|_{3/2}^{2}=\int_{\mathbb R}…` | correct | `:99` `$\|G\|<em>{3/2}^{2}=\int</em>{\mathbb R}…` | 2 |
| `docs/notation.md:109` `$\|\Pi_{-}…\Pi_{+}\|_{\mathfrak S_{2}}^{2}…` | correct | `:114` `…\|<em>{\mathfrak S</em>{2}}^{2}…` | 2 |
| `docs/definitions.md:93` `k_{s}\|_{A}=\mathrm{id},\qquad k_{s}(x)…` | correct | `docs/read/definitions.html:100` `k_{s}\|<em>{A}=\mathrm{id},\qquad k</em>{s}(x)…` | 2 |

Eight underscores deleted and four spans of mathematics italicised, on `notation` and
`definitions` — the two pages the first pass named as "precisely the pages the mirror exists to
make readable". This is the same defect as `history.md:143`, transplanted from `*` to `_` by the
repair for `history.md:143`.

I accept that a conforming CommonMark parser does the same thing here (rule 2 admits a
punctuation-preceded `_` as an opener, and the rule of three does not bite at 1+1). That makes the
mirror *faithful to GitHub* and does not make the page *right*. The card's framing —
"REF-CI-PAGES found five character-level defects … all now repaired" — invites the reader to
conclude the character-level account is closed. It is not: the net effect of the commit is 2 lost
asterisks recovered and 8 lost underscores created.

### DEFECT B3 — "a bare adjoint star is not an emphasis delimiter" is false, and live on the page the card says it fixed. **BLOCKING.**

> "Emphasis follows CommonMark's flanking rules for both * and _, so intraword underscores stay
> literal and **a bare adjoint star is not an emphasis delimiter**."

`docs/history.md:147` and `:148` write the adjoint as `M_*`, so the star is preceded by `_` and
followed by `)` or `/` — punctuation on both sides, which *is* left-flanking. At HEAD:

- `docs/read/history.html:136` — source has 5 asterisks, the rendered text has **1**: 4 deleted,
  two `<em>` spans over `lambda_min(M_*)/g_Q(d_c) = -7.0e-2, …` and `||M_*|| = -4.1e-3, …`.
- `docs/read/history.html:137` — source has 2, rendered has **0**: 2 deleted, one `<em>` over
  `(1/2) M_*(0,0)/h = +10.3, …`.

Six asterisks of mathematics are still deleted on the published history page, in the same file and
the same failure mode as the defect the card declares fixed, two lines below it. The author
repaired the instance the referee cited and did not look for the class. `grep -c '<em>'` on
`docs/read/history.html` is 2 at HEAD; one of the two is this.

### DEFECT B4 — the README count is wrong again. **BLOCKING (it is the third attempt at this sentence).**

> "README carries the Pages address four times, three in the introduction and one in section 9."

`grep -n github.io README.md` gives **six** occurrences: lines 27, 33, 34 (introduction — `## 1.` is
line 42) and lines **339, 340, 341** (section 9 — `## 9.` is 309, `## 10.` is 352). Three in the
intro is right; section 9 carries **three**, not one, and the total is **six**, not four. Under the
only other reading — counting the bare root address — the intro has one and section 9 has one.
There is no convention under which the sentence is true.

### DEFECT B5 — the two-condition statement does not hold. **BLOCKING.**

> "README … says that the address serves nothing yet and that publishing needs two things: the
> repository going public and the if: false on the Pages job being removed. configure-pages now
> passes enablement: true, so no click in Settings is needed."

See §1 B1: `enablement: true` with the default `GITHUB_TOKEN` cannot create the Pages site — the
action's own `action.yml` at v5 says so, `createPagesSite` needs Administration (write), and
`administration` is not a key of the workflow `permissions:` schema. Removing `if: false` on a
public repository with `has_pages: false` gives a failed job. The condition is still three, as the
first pass said and as `rigor/public_site_plan.md:226` says ("one line plus one click"). README
lines 35-38 carry the same false two-condition claim, so the file needs the same edit.

Confirmed unchanged: `gh api repos/alexander-stottmeister/cft-cmi` → `has_pages: false`,
`private: true`; `/pages` → 404. The URL form
`https://alexander-stottmeister.github.io/cft-cmi/read/…` is the correct project-pages form for
owner `alexander-stottmeister`, repo `cft-cmi`, with the workflow uploading `path: docs`.

### DEFECT B6 — a stale number in "How to verify". Non-blocking on its own, blocking with the rest.

"check_links 155 pages and **2210** links resolve" — `tools/check_links.py` prints
**`155 pages, 2211 links resolve`** at HEAD. The extra one is the `[.github/workflows/check.yml](.github/workflows/check.yml)`
link the same commit added to README:36 (README internal link tokens 80 → 81); the three new
github.io links are external and are not counted in the total.

### Exact repair (six edits)

**B-R3.** Replace:

> "THE SUBSET IS CLOSED, and this is enforced rather than intended: reject_unsupported() raises
> Unsupported on an ordered list, … and blocks() raises on an indented code block, … ; the paragraph
> branch is the fallback for prose, never for an unrecognised construct."

with:

> "reject_unsupported() and blocks() raise Unsupported on fourteen constructs that would otherwise be
mis-rendered in silence — an ordered list written `1.`, a fenced code block, a nested bullet, a
setext underline, a raw HTML block at the start of a line other than the anchor pattern, a closed
ATX heading, a two-space hard break, an image, an `<…>` autolink, a reference link, a
double-quoted link title, strikethrough, `***`, an indented code block, a pipe table with no
alignment row, a link target escaping the repository, an unterminated HTML comment and text after a
comment's close. That is a blacklist, not a closure property: the paragraph branch remains the
default, and constructs outside the list are still rendered wrongly and in silence. Measured by
REF-CI-PAGES-B: HTML entity references, a GFM bare-URL autolink, raw HTML in the middle of a line,
a pipe table with no leading bars, a table row whose trailing bar is missing (its last cell is
DELETED), a row without a leading bar inside a table, `+` bullets, a lazy blockquote continuation,
adjacent backtick runs, a code span containing a backtick, a link target with balanced parentheses
or with spaces or in angle brackets, `___` as a rule, `___foo___`, `* * *`, a backslash hard break,
an ordered list written `1)`, an HTML comment in the middle of a line and a single-quoted link title
are all silently wrong. Six of them are near neighbours of entries the blacklist does have. None
occurs in what build_docs.py emits today except the bare URL at docs/sources.md:25, which GitHub
links and the mirror does not; `history_page` copies any `rigor/PHASE*_STATUS.md` line beginning
with a bar into a table verbatim, so the missing-trailing-bar path is one file away from live."

**B-R4.** Replace:

> "Emphasis follows CommonMark's flanking rules for both * and _, so intraword underscores stay
> literal and a bare adjoint star is not an emphasis delimiter."

with:

> "Emphasis implements CommonMark's flanking predicates (rules 1-4) for both `*` and `_`, correctly:
intraword underscores stay literal, and a star between a letter and a space — `XX* >=` at
history.md:143 — can no longer open. It does NOT implement rule 9: the rule of three is absent
(`*foo**bar*` gives `<em>foo</em><em>bar</em>` where CommonMark gives `<em>foo**bar</em>`), and
same-character nesting is wrong (`*(*foo*)*` gives `<em>(*foo</em>)*` where CommonMark gives
`<em>(<em>foo</em>)</em>`). And flanking is not a defence for mathematics: an adjoint star written
`M_*`, punctuation on both sides, still opens, so docs/read/history.html:136,137 still delete SIX
asterisks and italicise three spans of numerics."

**B-R5.** Replace:

> "…all now repaired and each verified against the source line: history.md:143 … ; _underscore_
> emphasis was unimplemented …"

by appending to that sentence:

> "The underscore repair introduced four new losses of its own, at notation.md:89, 90, 109 and
definitions.md:93, where a LaTeX subscript follows a norm bar: `\|f\|_{\beta}=\sum_{n}` renders as
`$|f|<em>{\beta}=\sum</em>{n}`, eight underscores deleted and four spans of mathematics italicised,
on the two pages this mirror most exists for. A conforming CommonMark parser does the same, so the
mirror is faithful to GitHub and the pages are still wrong; the net character change of the repair
commit is two asterisks recovered and eight underscores lost. A math renderer, or `$…$` treated as
a protected span, is the only real fix."

**B-R6.** Replace:

> "README carries the Pages address four times, three in the introduction and one in section 9"

with:

> "README carries the Pages address six times, three in the introduction (lines 27, 33, 34) and
three in section 9 (lines 339, 340, 341)"

**B-R7.** Replace:

> "…and says that the address serves nothing yet and that publishing needs two things: the
> repository going public and the if: false on the Pages job being removed. configure-pages now
> passes enablement: true, so no click in Settings is needed; as of this card Pages has never been
> enabled on the repository (has_pages false)."

with the B-R1 wording, i.e. three conditions, with `enablement: true` described as written but
inoperative under the default `GITHUB_TOKEN`; and make the same edit to README:35-38.

**B-R8.** "How to verify": `2210` → `2211`. While there, the module docstring of
`tools/md_to_html.py` still carries two sentences the card has already corrected —
"`docs/.nojekyll` turns Jekyll off, **so** a `.md` file is served as a raw download" (lines 5-7) and
"a relative link between two documentation pages is the **same string** in both trees" (lines
10-11) — plus "A construct outside that subset raises `Unsupported`" (line 17). Fix the code
comment or the card will be true while the file a reader opens first is not.

---

## 3. `generated-docs` — **FAIL** (one stale number, found by running the generator)

| first-pass finding | state now [REF-B] | verdict |
|---|---|---|
| DEFECT 1: "about 1300 lines" | Statement says **1427**; `wc -l tools/build_docs.py` → **1427** (the file grew by 27 lines in b9daa45, and the card was updated to the new figure, not to the first pass's 1400) | **REPAIRED, exact** |
| DEFECT 2: "of the 85 cards listed" | Statement says "the 90 cards the knowledge base now lists"; a fresh `build_docs.py --check` prints `claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, 5 verified, 5 open, 14 active, 5 done, 2 superseded, 1 refuted)` and `pages under results/: 58` | **REPAIRED, exact** |
| DEFECT 3: the note's "131 plus a results index" | a new dated note of 2026-09-21 says "131 files in TOTAL, namely 65 Markdown sources (7 top-level and 58 under results/) and 66 HTML renderings (7 and 58 mirrors plus the generated read/results/index.html)". Recounted on disk: 7 + 58 = 65 `.md`; `docs/read/` has 66 `.html` = 7 top + 59 under `results/` (58 mirrors + the generated index); 65 + 66 = **131**. The note also correctly adds that the guard ignores `docs/explore/`, `docs/lib/`, `docs/assets/`, `docs/data/`. The earlier note is left in place and appended to, as the author rule requires. | **REPAIRED, arithmetic exact** |

Other numbers in the Statement, re-measured rather than read:

| clause | measured [REF-B] | verdict |
|---|---|---|
| "58 per-claim pages … (30 proved, 3 refereed, 22 numerical, 3 conjectural…)" | 58, and 30/3/22/3 | exact |
| "783 internal links with 0 dead, 0 untracked and 0 missing anchors" | the `.md` sources gained no link in b9daa45 (only the pipe escapes and two counts changed), so the first pass's recount at 5a3988b carries over | unchanged |
| "36 source rows" of `refs/REFERENCES.md` | 38 lines start with `|`, minus header and alignment = **36** | exact |
| "20 fetchable … verified against a live refs/restore.sh --list" | not re-run; unchanged since REF-DOCS-1c | accepted |
| **"the evidence pointers held only in the private companion are DETECTED (8: six source PDFs plus PRIVATE.md and CHECKLIST.md)"** | a fresh run prints **9** and lists them: `refs/Sion1958_minimax.pdf`, `refs/BJL_twisted_duality_math-ph-0204029.pdf`, `refs/AlbertiUhlmann02_math-ph-0202038.pdf`, `refs/CDIT_1808.02384.pdf`, **`plan_page/petz_program_plan.html`**, `PRIVATE.md`, `CHECKLIST.md`, `refs/Uhlmann76.pdf`, `refs/VWZ_2307.14434.pdf` | **STALE** |
| "and RENDERED without a link where a page cites them (6, since the two Markdown files are cited only by a card that reaches no displayed status)" | 6 is still right — 7 bullets across 6 result pages, all of them the 6 PDFs — but the reason now needs **three** exclusions, not two | **count right, reason stale** |
| the drift guard, hand-edit reporting, rule (a)/(b)/(c) | unchanged since REF-DOCS-1c and REF-CI-PAGES; `--check` at HEAD is red only on two `review pending` markers (§4), which is the guard working | holds |

`plan_page/petz_program_plan.html` was marked private in a30256b, which predates 5a3988b, so this
number was already stale when the first pass read it and I am naming it rather than passing it on.
It is one clause, the card's substance is in good order, and the standard this project applies is
that a number in a Statement is measured.

### Exact repair (one edit)

**B-R9.** Replace, in the Statement:

> "the evidence pointers held only in the private companion are DETECTED (8: six source PDFs plus
> PRIVATE.md and CHECKLIST.md) by a genuine git ls-files membership test rather than a hardcoded
> list and RENDERED without a link where a page cites them (6, since the two Markdown files are
> cited only by a card that reaches no displayed status)"

with:

> "the evidence pointers held only in the private companion are DETECTED (9: six source PDFs,
plan_page/petz_program_plan.html, PRIVATE.md and CHECKLIST.md) by a genuine git ls-files membership
test rather than a hardcoded list and RENDERED without a link where a page cites them (6, on 7
bullets across 6 result pages — the six PDFs; the other three are cited only by cards that reach no
displayed status)"

and, since this number moves whenever a path is marked private, add: "the generator prints the list
on every run, so the figure is checkable rather than typed".

---

## 4. The gates, run by me

`make check` — **exits 2** at HEAD on a clean tree:

```
python3 tools/check_links.py
  155 pages, 2211 links resolve
  external hosts: alexander-stottmeister.github.io, github.com
python3 tools/build_docs.py --check
build_docs --check: the committed documentation has drifted from the knowledge base
  differs   read/status.html
      @@ -249 +249 @@  …Plan: public presentation…</td><td></td></tr>
                    +  …Plan: public presentation…</td><td>review pending</td></tr>
      @@ -251 +251 @@  …Two git repositories over one work tree…</td><td></td></tr>
                    +  …Two git repositories over one work tree…</td><td>review pending</td></tr>
  differs   status.md      (the same two rows)
Run `tools/build_docs.py` (or `make docs`) and commit the result.
  claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, 5 verified, 5 open,
             14 active, 5 done, 2 superseded, 1 refuted)
  pages under results/: 58
  evidence pointers held privately, rendered without a link: 9   [the nine listed in §3]
  cards never refereed: 0 of the 90 listed (0 with a page); 232 of the 322 cards in the
             whole knowledge base …
  cards awaiting a referee pass: 5 (ci-green, docs-pages-rendering, generated-docs,
             public-site-plan, repo-split-public-private)
  cards whose last referee pass failed: 0
Makefile:48: recipe for target 'check' failed
make: *** [check] Error 1        (exit 2)
```

Run separately, past the abort: `build_site_data.py --check` → **exit 0**, five files ok;
`build_site_data_extra.py --check` → **exit 1**, `DRIFTED docs/data/extra-claim-map.json`. I
regenerated it into a scratch copy and diffed: the whole drift is 33 lines — `public-site-plan` and
`repo-split-public-private` moving to `review: pending` with their Statements updated, and
`count.awaiting_review` 3 → 5. None of it is the `ci-green`/`docs-pages-rendering` hole; that is
genuinely closed. This is the churn the Makefile header and REF-DOCS-1c already agreed to, not a
regression, and `make docs data` clears it.

`make rigor` — **exit 0**:

```
python3 tools/check_rigor_builds.py
  … (46 lines, every document "ok") …
46 document(s), 0 failing, 0 known
```

which matches the first pass's local figure of 46 against CI's 41 (the five untracked `cited_R*`
compendia). The working tree was clean afterwards.

---

## 5. Non-blocking items from the first pass

| item | state |
|---|---|
| `docs-pages-rendering`: the fourth link class (footer blob link to the page's own `.md`) | **addressed** in the Statement |
| `docs-pages-rendering`: "the same string in both trees" | **addressed** in the card, **not** in `tools/md_to_html.py:10-11` |
| `generated-docs`: the Statement's inventory says "65 files" and never mentions `docs/read/` | **still open**; the two notes carry the correction. Should not block — but one clause in the Statement would end it. |
| `public-site-plan` (outside the packet): "CI is red until implementation_C11.tex…" and "Four decisions open" | **both repaired** since the first pass — the card now says CI is green and that all four decisions were taken on 2026-09-21 |
| `ci-green` `next:` Node 20 deprecation | still accurate, still non-blocking |

New non-blocking, for the author's judgement, all latent:

- `pipes_in_code_spans()` toggles `in_code` on every single backtick, so a `` `` ``-delimited code
  span is not protected, and a row with an **odd** number of backticks escapes the row's own
  terminating bar: `| \`a | b |` → `split_row` returns `[]`, the whole row silently empty. No
  `rigor/PHASE*_STATUS.md` row has an odd backtick count today; `rigor/referee_ci_pages.md:134`
  does, which is how close this is.
- `tabular_to_md`'s `(?<!\\)\|` leaves a pipe preceded by an escaped backslash (`\\|`) unescaped.
- `\S {2,}$` in the hard-break guard fires on any line ending in two spaces, including a heading,
  which CommonMark cannot give a hard break at all. Fails closed, so harmless, but it will reject a
  legitimate page one day.
- `blocks()` reads a table only from a line starting with `|`, while `history_page` writes a table
  row from any `rigor/PHASE*_STATUS.md` line starting with `|`. The two rules disagree about what a
  table is at the first prose line that opens with a norm bar.

---

## 6. Consistency

`kb -p cft_cmi q --text Pages` (15 cards) and `--text "continuous integration"` (2). No card
contradicts another **except on Pages enablement**, where `ci-green` ("it is enabled when the
repository goes public"), `docs-pages-rendering` ("publishing needs two things … no click in
Settings is needed") and README:35-38 all now disagree with `rigor/public_site_plan.md:226-228`,
which both cards name as their governing decision and which says "enabling it is one line plus one
click". The plan document is right and the two cards are wrong; fix the cards, not D1.

---

## 7. Verdicts

- `ci-green` — **FAIL**. Both first-pass findings repaired exactly. Fails on B1.
- `docs-pages-rendering` — **FAIL**. Five character-level repairs verified; fails on B1-B5.
- `generated-docs` — **FAIL**. All three stale numbers repaired; fails on one more, B-R9.
