# REF-CI-PAGES: adversarial review of ci-green, docs-pages-rendering, generated-docs (2026-09-21)

All three FAIL. The engineering is sound in every case; what fails is what the cards *say* about it.
`ci-green` names the wrong package as the cause and gets the mechanism backwards.
`docs-pages-rendering` asserts a closure property its renderer does not have, and the violation is
not hypothetical: it is shipped, in `docs/read/notation.html` and `docs/read/history.html`, where a
published page silently mangles mathematics. `generated-docs` is stale in two numbers the appended
note does not correct.

Measurements marked [REF] are mine. The working tree was clean at `5a3988b` before and after; every
file I touched was restored by hand (`git status --porcelain` empty, checked after each test). No
git command that writes was run.

---

## 1. `ci-green` — **FAIL**

| # | claimed | measured [REF] | verdict |
|---|---|---|---|
|1| "24 runs, 0 successes" before the fix | `gh run list --limit 200`: 26 runs total, 24 `failure` + 2 `success`; the 24 failures are contiguous from 35578842239 (08:37:09Z) to 35595433844 (11:41:48Z) | **exact** |
|1| "Run 35602149545 is the first success" | first `success` in creation order; both jobs green, `pages` skipped. (35603853632, commit 5a3988b, is the second) | **exact** |
|2| "texlive-pictures was not [named]: paper1 loads tikz directly" | the failing runs **already installed texlive-pictures**. Old run 35595433844 apt log: `The following NEW packages will be installed: … texlive-pictures …`, `Setting up texlive-pictures (2023.20240207-1)`, TeX Live step conclusion `success` | **FALSE** |
|2| "`--no-install-recommends` … means every package must be named" | `--no-install-recommends` suppresses **Recommends**, not **Depends**. `texlive-latex-extra` **Depends: texlive-pictures (>= 2023.20230613)** (packages.ubuntu.com/noble/texlive-latex-extra), so it could never have been omitted | **FALSE** |
|2| (what actually changed) | diff of the two "NEW packages" lists: old 28, new 31. The only additions are **`lmodern`** and its two deps `xfonts-encodings`, `xfonts-utils`. `fonts-lmodern` was in *both* | isolated |
|2| (which package carries the missing file) | `lmodern.sty` is in the **`lmodern`** binary package, `/usr/share/texmf/tex/latex/lm/lmodern.sty`. `fonts-lmodern` (present in the failing runs) ships **no `.sty` file at all** | isolated |
|2| "lmodern was missing on the same argument" | inverted: **lmodern was the only thing missing.** `paper1/main.tex:2` is `\usepackage[T1]{fontenc}\usepackage{lmodern}…`; `\usepackage{tikz}` is line 6. With `-halt-on-error` the run aborts at line 2, so tikz is never reached even counterfactually | **cause inverted** |
|2| "the Makefile also sent pdflatex's output to /dev/null, so the log recorded a non-zero exit with no reason" | old run 35595433844, step `the two papers build`, in full: `cd paper1 && pdflatex … >/dev/null && …` / `make: *** [Makefile:36: papers] Error 1` / `Process completed with exit code 2`. Nothing else | **exact** |
|2| "on failure it now prints the last 40 lines of main.log" | reproduced with a stub `pdflatex` that writes a log and exits 1: prints `--- paper1/main.log, last 40 lines ---` then the log, aborts before `paper1 and paper2 built`, make exits 2 | **works** |
|3| "the figure-reproducibility check and check_rigor_builds.py had never executed once" | all **24** failing runs queried via the jobs API: `figures are reproducible = skipped` and `the rigor documents … = skipped` in 24/24 | **exact** |
|3| "each of the two jobs stopped at its second step" | `generated-artefacts` stopped at run-step 5/13, `papers` at 4/11 — the second of three *script* steps in each job, after checkout/setup-python | true as meant |
|4| "41 document(s), 0 failing, 0 known" in CI | green run log, step `the rigor documents…`: `41 document(s), 0 failing, 0 known` | **exact** |
|4| "which is the number README section 13 claims" | README:411 "All 41 rigor documents in this repository compile." Locally the same checker reports **46** — 49 `rigor/*.tex` on disk, 44 tracked, 5 untracked (`cited_R1..R4`, `cited_results_all`); 46 − 41 = those 5. The card's "in a clone that carries no private material" is the right qualifier | **exact** |
|5| "WITHOUT the flag a missing knowledge base is still an error" | driver test, `KB` monkeypatched to a nonexistent path: `--check` → exit **2**, `EXTRACTION FAILED: the knowledge base is not at …`; `--check --allow-missing-kb` → exit 0 with `NOT CHECKED, no knowledge base at …: docs/data/extra-claim-map.json` and the other three `ok`; with a **real** KB the flag does **not** suppress the claim-map check (`builders.pop()` is guarded by `not KB.is_dir()`) | **exact, and well built** |
|5| "so a working clone cannot quietly stop checking the claim map" | true of a *working clone*. But the hole is already open on `main`: the committed `docs/data/extra-claim-map.json` is **drifted right now** — it has `"n": 11` where the KB gives 13, and is missing the `ci-green` and `docs-pages-rendering` nodes plus 6 edges (260-line diff). CI run 35603853632 was **green** over exactly that file | **incomplete** |
|6| "make rigor had never run at all … absent from .PHONY" | reproduced in isolation with a `rigor/` directory present: old `.PHONY` line → `make: 'rigor' is up to date.`, exit 0, recipe not run; with `rigor` added → recipe runs. `git show 9aed69a^:Makefile` line 8 confirms it was absent, line 56 confirms the target existed | **exact** |
| — | `next:` "Node 20 deprecation warning on actions/checkout@v4 and actions/setup-python@v5" | green run: `##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 … actions/checkout@v4, actions/setup-python@v5` | **exact** |

### Why FAIL

Twelve of the fourteen claims are exact, several of them impressively so. The card fails on **one
sentence, and it is the causal one.** The orchestrator never saw the LaTeX error — the card says so
itself — and then asserted a cause anyway. The assertion is refutable from the evidence that was
already in the failing run's own log: `texlive-pictures` appears in that log's "NEW packages will be
installed" list and in a `Setting up texlive-pictures (2023.20240207-1)` line. It was never missing,
it could not have been missing (it is a hard `Depends` of `texlive-latex-extra`, which
`--no-install-recommends` does not touch), and even if it had been, `-halt-on-error` would have
stopped at `\usepackage{lmodern}` on line 2 before reaching `\usepackage{tikz}` on line 6.

The cause **can** be isolated, and I have isolated it: the commit changed three files; the Makefile
change is a log dump that cannot affect compilation and the extractor change is in the other job; so
the papers fix is exactly the apt line, and within the apt line exactly one package is new,
`lmodern`, which is the Debian/Ubuntu package that carries `lmodern.sty`. Naming `texlive-pictures`
was a no-op. The card states the no-op as the cause and the cause as an afterthought.

This is not a wording quibble. The same false explanation is committed as a code comment in
`.github/workflows/check.yml:43-46`, where it will teach the next reader the wrong rule about
`--no-install-recommends`, and it is in the commit message of 9aed69a, which cannot be repaired.

Second, smaller: the `--allow-missing-kb` design is right, but the card presents it as closed
("cannot quietly stop checking") when the flag's one intended consumer, CI, is the place where the
claim map is now rotting unobserved. It is the same class of hole this project has spent the day
closing: a gate that is green because it does not look.

### Exact repair (three edits; nothing else changes)

**R1.** Replace, in the Statement:

> "(2) The papers job failed compiling paper1. apt-get ran with --no-install-recommends, which means every package must be named, and texlive-pictures was not: paper1 loads tikz directly and tcolorbox pulls it in for every rigor document. lmodern was missing on the same argument."

with:

> "(2) The papers job failed compiling paper1, and the cause was isolated only afterwards, because the Makefile sent pdflatex's output to /dev/null and no run ever recorded the error. The missing package was **lmodern**, which carries lmodern.sty (/usr/share/texmf/tex/latex/lm/lmodern.sty); paper1/main.tex loads it on line 2, so with -halt-on-error nothing past line 2 was ever reached. The commit also names texlive-pictures, which was a no-op: it is a hard Depends of texlive-latex-extra and appears in the failing runs' own apt log ('Setting up texlive-pictures (2023.20240207-1)'), and --no-install-recommends suppresses Recommends, not Depends. The fonts-lmodern package, installed in both the failing and the passing runs, ships no .sty file. This was established after the fact by diffing the apt 'NEW packages will be installed' lists of runs 35595433844 (28 packages) and 35602149545 (31: the same 28 plus lmodern, xfonts-encodings, xfonts-utils), not by reading a LaTeX error, which no run produced."

**R2.** Replace the `.github/workflows/check.yml` comment at lines 43-46:

> "--no-install-recommends keeps the download small, so every package has to be named. texlive-pictures carries tikz, which paper1 loads directly and which tcolorbox pulls in for every rigor document; lmodern is the text font of both papers and of rigor_preamble.tex."

with:

> "--no-install-recommends suppresses Recommends, not Depends: texlive-pictures arrives anyway as a Depends of texlive-latex-extra and is named here only for the record. lmodern is the one package that has to be named — it carries lmodern.sty, which paper1/main.tex, paper2/main.tex and rigor_preamble.tex all load on line 2, and its absence is what failed every run before 9aed69a. fonts-lmodern is not a substitute: it ships fonts, no .sty."

**R3.** Append to the Statement, after the `--allow-missing-kb` sentence:

> "What the flag does not do is protect CI: with the knowledge base absent, a drifted docs/data/extra-claim-map.json is announced as unchecked and then waved through, and nothing else in the repository can rebuild it. That is live, not hypothetical — at 5a3988b the committed claim map is missing the ci-green and docs-pages-rendering nodes and six edges, and run 35603853632 was green over it. Only `make check` in a clone that has the knowledge base beside it will catch this, i.e. a human before committing."

---

## 2. `docs-pages-rendering` — **FAIL**

| # | claimed | measured [REF] | verdict |
|---|---|---|---|
|1| "Jekyll converts only pages carrying front matter and front matter would then appear in the Markdown that GitHub renders" | correct, and the escape hatch does not exist: Jekyll's `defaults` cannot rescue a file with **no** front-matter block, because such a file is a static file and is never processed | **sound** |
|1| ".nojekyll turns Jekyll off, **so** Pages serves a .md as a raw download" | the outcome is right but the "so" is not: a front-matter-less `.md` is copied verbatim with or without `.nojekyll`. `.nojekyll` is not the cause of the raw download | loose causality |
|1| content-type `text/markdown` **on GitHub Pages** | unverifiable from here and **not** tested by the card's own recipe. `has_pages: false` on this repository — Pages has never been enabled — so there is no site to measure | **unsupported claim, weak evidence** |
|2| "renders only the closed subset … and **raises Unsupported on anything else rather than falling back to a paragraph**" | `Unsupported` is reachable in exactly **three** places: `md_to_html.py:226` (indented code block), `:236` (pipe table with no alignment row), `:303` (link escaping the repo). `:284` is commented "unreachable". Paragraph fallback is the **default** branch | **FALSE** |
|2| (is anything silently mis-rendered?) | yes, in the *shipped* pages. Verified by hand, not by sampling — see the table below | **FALSE, and live** |
|3| "another documentation page keeps its relative path with .md swapped for .html" | 0 relative `.md` hrefs remain anywhere under `docs/`; 1104 relative `href`/`src` in `docs/read/`, **all 1104 resolve** | **exact** |
|3| "a file elsewhere in the repository becomes an absolute blob URL" | 265 `github.com/.../blob/main/...` links; **265/265 resolve to a git-tracked file**, 0 dangling | **exact** |
|3| "a directory gets its index … two pages link to results/" | exactly two: `docs/status.md:21` and `docs/index.md:24`, both `](results/)`; both render to `href="results/index.html"`; that index has 58 result links + 5 nav | **exact** |
|3| "no link in docs/read/ points at a path Pages will not serve" | 0 of 1104 relative targets leave `docs/`; 64 fragment links all resolve, against the 8 `<a id>` anchors which are all in `status.html` (matching `next:`) | **exact** |
|3| (unstated fourth class) | each of the 65 mirror pages carries a footer blob link to **its own** `docs/…md` source — 65 links into the deployed namespace, by design, not covered by the three stated rules | undocumented |
|4| "65 pages became 131" | 7 + 58 = 65 `.md`; 7 + 59 = 66 `.html` (the 59th is the generated `read/results/index.html`); 65 + 66 = **131**. Confirmed by regenerating into a scratchpad: exactly 131 files | **exact** |
|4| "155 pages and 2210 links resolve" | `tools/check_links.py` → `155 pages, 2210 links resolve`, exit 0. Independently recounted: 155, 2210, 0 broken | **exact** |
|4| (but what is a "page" there?) | any tracked `.md`/`.html` outside `rigor/`: 143 under `docs/` + `README.md`, `THIRD-PARTY.md`, `refs/REFERENCES.md`, 3 issue templates, 6 `numerics/**.md`. 131 + 24 = 155. Also: 318 external links excluded, all fragments stripped before checking, 7 directory targets accepted unconditionally | ambiguous, not wrong |
|4| "all 66 module imports resolve" | `docs/read/` has 66 HTML files with **exactly 66** import specifiers, one per page, all resolving. Repo-wide under `docs/` there are 91, all resolving. **No committed tool checks any of them** — `check_links.py` matches only `href`/`src` and `](…)` | **true as scoped**; the 66 is the page count restated |
|4| "the rendered text loses no source word (only the anchor ids, which are attributes)" | word claim **holds 65/65** on two independent extractors and against a markdown-it-py GFM baseline; all 8 anchor ids present. The **parenthetical is false**: see the loss table below | **half FALSE** |
|5| "a local server returns text/html for read/status.html where status.md returns text/markdown" | reproduced: `read/status.html` → `text/html`, `status.md` → `text/markdown`. But this measures `python3 -m http.server`'s `mimetypes` table, not GitHub Pages | reproduces; **wrong instrument** |
|6| "grep … finds no link whose visible text still names a Markdown file" | 0 links matching `read/…\.html">[^<]*\.md`. (65 footer links *do* show a `.md` name, but point at `github.com`, so the claim as worded holds) | **exact** |
|6| "one built at runtime in claim-map.html from the JSON field 'page'" … fixed | `'../read/results/' + c.page.replace(/\.md$/, '.html')`; `c.page` is a bare filename (`gap-law.md`), so all **58** runtime hrefs resolve to a real file; `git show 5a3988b` confirms the old form was `'../results/' + c.page` | **exact** |
|6| "113 in 12 HTML files" | pre-commit tree: 121 `.md` hrefs in 12 HTML files, of which 8 are absolute blob URLs → **113 relative**, in **12** files | **exact** |
|7| escaped characters | recounted over the 65 sources: `\*` **212**, `\<` **137**, `\_` **39**, `\]` **37** — all four exact. Sentinel test on all 425: **0** produce a wrong literal in the body. (The list is not exhaustive: `\~` 45, `\[` 37, `\|` 14, `\\` 9 are the ones that break) | counts **exact**, body escaping **correct** |
|7| fidelity, 3 random pages (seed 20260921) | `vacuum-rigidity-exact-recovery`, `e2-exact-fidelity-optimised-extension`, `all-channel-optimum-value`: visible character streams **byte-identical**, 3013/3013, 2116/2116, 6791/6791 chars; structural counts match | **exact** |
|8| generated shell | 66/66 pages: exactly one `<title>`, exactly one `<h1>`, well-formed under `html.parser`, `<!doctype html>` first, `<html lang="en">`, `<meta charset>`, `<meta viewport>`. All content is static; the only JS is a theme bootstrap and `initTheme`, and the toggle ships `hidden` and is unhidden by JS, so with JS off the page reads correctly and the control stays invisible rather than dead. No XSS: the sole raw-HTML passthrough is the fully anchored `^<a id="[A-Za-z0-9_-]+"></a>\s*$` | **sound, unclaimed and better than claimed** |
|9| "README carries the Pages address at the top **and in section 9**" | the address occurs at README:27, 33, 34 — **all three in the intro**, before `## 1.` at line 38. Section 9 is lines 305-344 and contains **no** github.io address | **FALSE** |
|9| the URL itself | `https://alexander-stottmeister.github.io/cft-cmi/` is the correct project-pages form for owner `alexander-stottmeister`, repo `cft-cmi`; the workflow uploads `path: docs`, so `read/index.html` and `read/status.html` are the right sub-paths | **correct** |
|9| "the site goes live when this repository becomes public" (README:34-35) | going public is **necessary and not sufficient**. The deploy job is gated `if: false`, and `gh api repos/…` reports `has_pages: false` — Pages has never been enabled. The project's own D1 (`rigor/public_site_plan.md:226`) says it correctly: "one line plus one click" | **FALSE as written** |
| — | "How to verify": "make check: 155 pages, 2210 links resolve; build_docs --check: 131 pages up to date" | `make check` **exits 2**. `check_links` passes; `build_docs --check` reports `differs index.md, read/index.html, read/status.html, status.md` and exits 1; `build_site_data_extra --check` also fails but is masked because make aborts first | **does not reproduce** |
| — | "The mirror is generated by build_docs.py, so --check covers it" | tested four ways: one byte appended to `read/results/gap-law.html` → `differs`; the file deleted → `missing`; an orphan at `read/orphan.html` → `stale`; a nested orphan at `read/results/archive/stale.html` → `stale`. A planted file under `docs/explore/` correctly does **not** fire | **exact** |

### The closure claim, in the pages that are published

Every one of these is in the committed `docs/read/` tree, not in a test fixture. All were confirmed
by reading the source line and the rendered line side by side.

| source | rendered | what a reader sees |
|---|---|---|
| `docs/history.md:143` `N = 1 - XX* >= 0 and 0 <= Y = Z - X Q_BB X* <= N` | `docs/read/history.html:132` `N = 1 - XX<em> &gt;= 0 … X</em> &lt;= N` | **both adjoint stars deleted**, 40 characters of mathematics italicised. CommonMark's flanking rules refuse emphasis here; `inline()`'s naive `*` scan does not |
| `docs/notation.md:123`, a **3-column** table row using `\\|` for LaTeX norm bars | `docs/read/notation.html:131` | a **9-cell** row: `<td>$\</td><td>T(g_{\rm tot})\Omega\</td><td>^{2}$</td>…`. `split_row()` eats `\\` as an escape pair and then splits on the bare `|` |
| `docs/notation.md:119`, same construct | `docs/read/notation.html:127` | a **5-cell** row in a 3-column table |
| `docs/history.md:219`, code spans containing `\|` | `docs/read/history.html:204` | a **10-cell** row under a **2-column** header, with the code spans re-paired across cell boundaries and two literal backticks leaking into the prose. `split_row()` does not honour code spans, unlike `_closing()` and `_link_text_end()` |
| `docs/notation.md:25` `$\{k<0\}$` | `docs/read/notation.html:43` `${k&lt;0}$` | LaTeX set braces silently become grouping braces (`PUNCT` contains `\ { } % \|`, so the backslash is stripped) |
| `docs/notation.md:89,109`, `docs/definitions.md` ×4 — `$\|f\|_{\beta}$` | `docs/read/notation.html:98` etc. `$|f|_{\beta}$` | **norm degraded to absolute value**, 10 sites. (Here the mirror matches GFM, so the fault is upstream in the source Markdown — but the mirror ships no KaTeX, so the reader sees the degraded text raw) |
| `_None recorded._`, `_no result recorded in the table_` | `<p>_None recorded._</p>` etc. | underscore emphasis is **not implemented**; literal underscores on **28 of the 66** pages, 27 result pages plus 7 occurrences in `sources.html` |
| `# Exact -1/2 log det(1-V^\*V) …` | `docs/read/results/e2-exact-fidelity-optimised-extension.html:6` `det(1-V^\V)` | `title_of()` runs ``re.sub(r"[`*]", "", …)`` on the **raw** Markdown, so the `*` is deleted and the backslash kept. The `<h1>` on line 31 of the same file is correct — tab title and heading disagree |
| two more titles | `compression-not-optimal-exact-fidelity.html:6,7`, `circle-model-taper-suppresses-theta.html:6,7` | stray backslash in `<title>` and `<meta description>` |

Latent but not currently triggered (constructs absent from the 65 sources): ordered lists, fenced
code blocks, setext headings, images, autolinks, reference links, hard breaks, `***`, `~~`, closed
ATX, nested bullets at 2 spaces, link titles, and a `)` inside a link target — each silently
mis-rendered rather than raising. Two further silent content-loss paths in `blocks()`: an
unterminated `<!--` swallows the rest of the file, and visible text on the same line as `-->` is
discarded.

### Why FAIL

Three separate failures.

**(a) The closure claim is the load-bearing safety argument of this module and it is false.** The
docstring says it correctly as an intention — "rendering an unknown line as a paragraph is how a
generated page starts quietly lying" — and the code does exactly what the docstring warns against,
by default, in every branch but three. The card repeats the intention as an achieved property. The
consequence is on the public pages today: two of the seven top-level documents,
`notation.md` and `history.md`, ship rows of shredded LaTeX and a line of mathematics with its
adjoint stars deleted. These are precisely the pages the mirror exists to make readable.

**(b) "The rendered text loses no source word" is true and misleading together.** I checked it two
ways and it holds 65/65 on alphanumeric words. But the parenthetical — "only the anchor ids, which
are attributes" — presents that as the complete account of what changes, and it is not: two literal
`*` carrying mathematical meaning are gone, norm bars are gone, three table rows are re-partitioned,
and 28 pages show raw underscores. A referee reading only the card would conclude the mirror is
faithful. It is faithful *at word granularity*, which is the wrong granularity for a mathematics
site.

**(c) Two statements about the README are simply wrong.** The Pages address is not in section 9; all
three occurrences are in the intro. And "the site goes live when this repository becomes public" is
not true of this repository: the deploy job is `if: false` and Pages has never been enabled
(`has_pages: false`). The project's own decision D1 states the real condition — "one line plus one
click" — and the README states a weaker one, on the most prominent line of the file, under a URL
that will 404 for every reader until all three things happen.

Everything else in the card is exact, including several numbers I expected to break: 113 in 12
files, 65→131, 155/2210, 66 imports, the three link classes, and the escape counts. The link work is
genuinely complete — 265 blob URLs, 1104 relative targets and 64 fragments, zero failures between
them — and the generated shell is better than the card claims for it.

### Exact repair (five edits)

**R1.** Replace, in the Statement:

> "It renders only the closed subset build_docs.py emits (…) and raises Unsupported on anything else rather than falling back to a paragraph."

with:

> "It renders the subset build_docs.py emits (ATX headings, paragraphs, bullet lists, pipe tables honouring escaped bars, block quotes, rules, HTML comments and bare anchor tags; code spans, bold, italic, links and backslash escapes inline). It is **not** closed: Unsupported is raised in three places only — an indented code block, a pipe table with no alignment row, and a link target that escapes the repository — and everything else outside the subset falls through to the paragraph branch and is rendered wrongly in silence. Known consequences in the committed mirror: `split_row()` does not honour code spans or `\\\\` before a bar, so `notation.md:119,123` become 5- and 9-cell rows in a 3-column table and `history.md:219` a 10-cell row in a 2-column one; `inline()`'s `*` scan ignores CommonMark flanking, so `history.md:143` loses both adjoint stars to a spurious `<em>`; `_underscore_` emphasis is not implemented and shows as literal underscores on 28 of the 66 pages; `PUNCT` strips the backslash from LaTeX `\\{ \\} \\% \\|`, so set braces and norm bars degrade; and `title_of()` de-escapes wrongly, so three `<title>`s disagree with their own `<h1>`. Ordered lists, fenced code, setext headings, images, autolinks, reference links and hard breaks are all silently mis-rendered too, and none of them occurs in the current sources."

**R2.** Replace:

> "the rendered text loses no source word (only the anchor ids, which are attributes)"

with:

> "the rendered text loses no source *word*: all 65 pages match at alphanumeric-word granularity, against two independent extractors and a markdown-it GFM baseline, and all 8 anchor ids survive as attributes. It does lose characters — two adjoint `*` on history.md:143, the doubled norm bars in notation.md and definitions.md, and the cell boundaries of three table rows — so word-level fidelity is not page-level fidelity, and this mirror should not be described as faithful without that qualification."

**R3.** Replace:

> "README carries the Pages address at the top and in section 9, saying that the site goes live only when the repository becomes public."

with:

> "README carries the Pages address three times, all in the introduction (lines 27, 33, 34); section 9 explains the Markdown-versus-`docs/read/` split but gives no address."

and repair README:34-35, replacing

> "The site goes live when this repository becomes public, which it is not yet"

with

> "The site is built and committed but not published: the repository is private, the Pages deploy job in `.github/workflows/check.yml` is deliberately disabled (`if: false`), and Pages is not enabled on the repository. Publishing needs all three — going public, removing that one line, and enabling Pages (decision D1)."

**R4.** Replace, in the Statement:

> "docs/.nojekyll turns Jekyll off, so GitHub Pages serves a .md file as a raw download: content-type text/markdown, which a browser shows as plain text or saves."

with:

> "GitHub Pages does not render Markdown: a `.md` file with no YAML front matter is a static file and is served verbatim (content-type `text/markdown`), with or without `docs/.nojekyll`, so a browser shows it as plain text or saves it. This has not been measured on Pages for this repository, which has never had Pages enabled; the local `http.server` check in 'How to verify' measures Python's mimetypes table, not GitHub's."

and amend the "How to verify" line accordingly, or drop the content-type recipe, which does not test the claim it is offered for.

**R5.** Amend "How to verify". `make check` exits 2 on the committed tree: `build_docs --check`
reports `differs index.md, read/index.html, read/status.html, status.md` because the knowledge base
has gained two `done` cards (one of them this card) since the docs were last generated, and
`build_site_data_extra --check` fails too but is masked because make aborts first. Either say "after
`make docs data`, `make check` is green: 155 pages, 2210 links, 131 pages up to date", or state that
the gate is red until the pages are regenerated after this review.

**Non-blocking, for the author's judgement.** The three stated link classes do not cover the
per-page footer link to the page's own `.md` source (65 of them, into `docs/` on `github.com`); a
fourth clause would make the rule set complete. And "a relative link between two documentation pages
is the same string in both trees" is not literally true — `../index.md` becomes `../index.html`;
what is preserved is the directory prefix.

---

## 3. `generated-docs` — **FAIL**

Reviewing the appended note of 2026-09-21 and asking whether the Statement is now stale in any
respect the note does not correct.

| # | claimed | measured [REF] | verdict |
|---|---|---|---|
|1| note: "65 files became 131 **plus a results index**" | the true output set is **131 files including** `read/results/index.html` (7 + 58 md, 7 + 59 html). As written the sentence reads 132 | **off by one as worded** |
|2| note: "The Markdown is unchanged and remains the source" | `git show 5a3988b --stat`: no `docs/*.md` or `docs/results/*.md` changed; only `docs/read/**` added, plus the three tools and the site HTML | **exact** |
|3| Statement: "tools/build_docs.py (**about 1300 lines**)" | `wc -l tools/build_docs.py` → **1400** (1372 before 5a3988b) | **stale** |
|4| Statement: "65 files, namely seven top-level pages … and 58 per-claim pages" | now 131 files. The note corrects the count but the Statement's inventory is still the only one given and does not mention `docs/read/` | stale, partly covered |
|5| Statement: "of the **85 cards** listed" | `docs/status.md:5` (committed) says **88 cards**; a fresh run reports **90 listed**. No note corrects this | **stale, uncorrected** |
|6| Statement: "measured **783** internal links with 0 dead, 0 untracked and 0 missing anchors" | recounted over `docs/*.md` + `docs/results/*.md`: **783** internal, 0 external | **still exact** |
|7| Statement: the drift-guard list ("a changed byte, a stale results page, a deleted results page, a changed card, and now also on an orphan top-level page") | all still fire, and the guard now also covers `docs/read/` recursively — a changed byte, a deletion, a top-level orphan and a nested orphan under `read/results/archive/` are all caught, and a planted file under `docs/explore/` correctly is not | **true, and now stronger than stated** |
|8| Statement: "it reports rather than hides pages skipped by the hand-edit marker" | `check()` takes `skipped` as an argument and prints `NOT CHECKED, marked hand-edited`; the scope logic (`owned()`, `write_out()`) is now one namespace for detection and repair | **repaired as REF-DOCS-1c asked** |
|9| Statement: "58 qualifying claims (30 proved, 3 refereed, 22 numerical, 3 conjectural)" | 58 pages under `docs/results/`, 58 `page` fields in the claim map | **exact** |

### Why FAIL

Three stale numbers, two of which no note corrects.

"about 1300 lines" is now 1400 — it was already 1372 when the card was written, so this was a
rounding the wrong way that has since drifted further. "85 cards listed" is contradicted by the
generator's own page (`docs/status.md` says 88) and by a fresh run (90). The note's own arithmetic,
"65 files became 131 plus a results index", double-counts the index: 131 already contains it.

The substance of the card is in good order, including everything REF-DOCS-1c asked for, and the
drift guard is now genuinely stronger than the Statement claims. These are three numbers, and this
project's standard is that a number in a Statement is measured.

### Exact repair (three edits)

**R1.** "tools/build_docs.py (about 1300 lines)" → "tools/build_docs.py (1400 lines)".

**R2.** "3 conjectural of the 85 cards listed" → "3 conjectural of the 90 cards the knowledge base
now lists (the count moves with the knowledge base; docs/status.md carries the current figure and is
inside the drift guard)".

**R3.** Amend the note of 2026-09-21 — or, since a note is not rewritten, add a new dated one:

> "2026-09-21 correction: the generator's output set is 131 files in total — 65 Markdown sources (7 top-level + 58 under results/) and 66 HTML renderings (7 + 58 mirrors + the generated read/results/index.html). The earlier note's '131 plus a results index' double-counts that index. docs/read/ is inside the drift guard: --check catches a changed byte, a deleted mirror page and an orphan anywhere under read/, including a nested one."

---

## 4. Consistency with the other infrastructure cards

Checked with `kb -p cft_cmi q --text Pages` (15 cards) and `--text "continuous integration"` (2),
then read `interactive-site`, `public-site-plan` and `repo-split-public-private` in full.

**No card contradicts the three under review.** Two staleness items in `public-site-plan`, which is
outside this packet and which I am not failing:

- its Statement still lists "CI is red until implementation_C11.tex and its referee report build" as
  a live constraint. Both build, and CI is green for an unrelated reason; `ci-green` supersedes it.
- its Statement still says "Four decisions open: D1 when Pages goes live", while
  `rigor/public_site_plan.md:224` heads the section "Decisions — taken 2026-09-21 by the user" and
  the card's own notes say "D1 of the plan is unchanged". `ci-green` and `docs-pages-rendering` both
  treat D1 as taken, which matches the document, not the plan card's Statement.

`repo-split-public-private` ("BOTH REMOTES ARE PRIVATE as of 2026-09-20; the first is public-ready
but not public") agrees with the workflow's `if: false` and with `has_pages: false`, and is the card
the README's "goes live when public" sentence should be reconciled with.

`interactive-site` is consistent: its `next:` anticipates "P5 adds the Makefile targets … and the
Pages workflow", which is what `ci-green` describes. Its claim that `docs/data/*.json` cannot drift
is now qualified by the `--allow-missing-kb` hole in `ci-green` R3, but only for the claim map,
which `interactive-site` does not own.
