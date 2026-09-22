# REF-COUNTS: four cards after the count repairs (2026-09-22)

Twelfth pass. Scope: `repo-split-public-private`, `generated-docs`, `readme-and-figures`,
`public-site-plan`; the four repairs of REF-README-B (R-B1, R-B2, R-B3, X-R2) and its five
carried non-blocking items; every neighbour of every edit the author's one commit made, in the
four cards, in `CHECKLIST.md`, in `PRIVATE.md` and in what `docs/data/extra-claim-map.json`
ships; and a re-measurement of everything the last two passes did not certify.

Everything below was measured or executed at cft-cmi HEAD `7099ab1` (2026-09-22 10:40:05 +0200)
against the knowledge-base working tree, not read off a previous report.

**Verdicts: `generated-docs` PASS. `public-site-plan` PASS. `repo-split-public-private` FAIL**
on two items, both introduced by this commit's repairs. **`readme-and-figures` FAIL** on one
item with three faces, also introduced by this commit's repair.

Context, from the user: publication was declined for now. `private: true`, `has_pages: false`,
`/pages` → 404, `if: false` at `.github/workflows/check.yml:70`. Every statement is judged
against that state, and every card describes it as it is.

---

## 1. The strategy, judged on its merits

The author's answer to eleven passes of count drift is to replace the number with the check
that produces it, to date the figure where a number is still worth having, and to tell the
reader to re-measure. It is the right answer, and this pass is the first in the chain at which
the *number* class of defect is genuinely closed rather than moved:

- `every hash the four feeds publish resolves in the local history` — no integer at all. I
  enumerated the four feeds today: **18** distinct SHAs (9 commits, 9 trees), every one
  resolving locally. REF-FINAL saw 3, REF-README-B saw 8, I see 18, and the sentence is true at
  all three values. That is what a count replaced by a check looks like.
- `every path ever added is checked … (623 paths on 2026-09-22, one more with every commit, so
  this is a check to re-run and not a number to carry)` — it is **624** today, because the
  commit that wrote 623 added `rigor/referee_readme_b.md`. The hedge names exactly that
  mechanism, so this is the change working, not drifting. The conclusion re-verified: of the
  624, **0** match `rigor/shots/`, `*.pdf`, `rigor/cited_R[1-4].tex`,
  `rigor/cited_results_all.tex` or `plan_page/`, and `git check-ignore` hides **0**.
- `holds this history and nothing else` — the 68→69→74→75 thread is ended, not corrected a
  fourth time. `git rev-list --count HEAD` is 75 and the sentence cannot notice.
- `155 pages and 2210 links on 2026-09-22, a total that moves whenever any tracked page gains
  or loses a link, so read what the run prints` — `make check` prints `155 pages, 2210 links
  resolve`. Both cards that carry this figure now carry the same words, and `2211` is gone from
  everything under `docs/` except a byte sequence inside `katex.min.js`.

Two of the eight edits went wrong, and both went wrong in the way this chain always goes wrong:
the repair damaged the sentence it was inside, or the sentence next to it. Neither is a
retraction and neither touches the substance. They are §3 and §4.

---

## 2. The four repairs: applied, and true except where §3 says otherwise

### R-B1 — applied verbatim, and true

The Statement now closes that sentence `…created at 2026-09-21T19:55:13Z with a new id and
holds this history and nothing else.` Measured: repo id **1380449076**, `created_at`
**2026-09-21T19:55:13Z**, `private: true`, `fork: false`, `has_pages: false`. `git rev-list
--count HEAD` = 75; `git ls-remote origin` gives the same head. No integer remains, the
neighbours on both sides still read (`The other recorded route, a GitHub Support purge…`
follows and still refers to something), and it ships in `extra-claim-map.json`.

### R-B2 — applied verbatim, and the clause overstates what the eighth pass did. See C-2

The text is in the card character for character as REF-README-B wrote it. Two of its three
limbs are right and the third is not; the analysis is C-2 below.

### R-B3 — applied verbatim, and true

`CHECKLIST.md` item 3 now closes exactly as R-B3 asked, naming the fifth route and its own
string. Committed to the private repository at `bc9dc02`, working tree clean. The contradiction
between an evidence token of the card and the card is gone. Items `3`, `3b`, `3c`, `3d`, `3e`
are all present, so `next`'s "CHECKLIST.md items 3 to 3e record the clearance" still holds, and
3d's wording is still `next`'s wording.

### X-R2 — applied, and true

`generated-docs`'s `How to verify` now reads `(check_links.py's own totals are over the whole
site and are a different corpus: 155 pages and 2210 links on 2026-09-22, a total that moves
whenever any tracked page gains or loses a link, so read what the run prints)`. `make check`
prints 2210. `grep -rn 2211 docs/` outside `katex.min.js`: **0**. The knowledge base no longer
ships two totals for the same tool.

### The clearance itself, re-run rather than accepted

Not because it was doubted, but because C-2 is about the *scope* of the sentence that records
it and I had to know the substance was sound before failing the wording. All nine discarded
objects still 404 on the live remote: `git/blobs/` for `3aa2e00b`, `a1dc319b`, `c8fb6e69`,
`4ef4814d`, `07ca78ac`, `18cc05ab`, `git/trees/` for `c6c9235a`, and
`commits/5d64c77d…` → HTTP 422 `No commit found`. 624 paths, 0 forbidden, 0 hidden. The
clearance holds.

---

## 3. `repo-split-public-private` — FAIL

### C-1 — BLOCKING. The N-B2 repair duplicated its own appositive: 96 + 1 + 1 = 98

N-B2 asked for one noun: `the 97 tracked .out run captures` → `the 97 tracked .out files`. The
noun was changed. A clause was also inserted. The sentence now reads

> and the 97 tracked .out **files**, 83 under numerics/ and 14 under rigor/, 96 of them run
> captures **and one a stray LaTeX bookmark file** and one (rigor/_probe.out) a stray LaTeX
> bookmark file, of which 23 are named by a card's evidence token

The word diff against the last committed version is `-run captures, +files,` and, four clauses
later, a bare insertion of `+a stray LaTeX bookmark file and one`. The sentence now asserts two
stray LaTeX bookmark files and totals 98 where it has just said 97.

Measured: `git ls-files '*.out'` = **97**, `numerics/` **83**, `rigor/` **14**, `83 + 14 = 97`,
and exactly **one** of the 97 opens with `\BOOKMARK` — `rigor/_probe.out`. So the three counts
the card gives are right, and the clause the repair added is false about the one thing it
names. 23 named by a card's evidence token is also exact (re-measured over `areas/`, `claims/`,
`evidence/`).

It ships: `docs/data/extra-claim-map.json` carries the duplicated clause verbatim, and module 10
renders it.

**Repair R-C1, verbatim.** In the Statement replace

    96 of them run captures and one a stray LaTeX bookmark file and one (rigor/_probe.out) a stray LaTeX bookmark file

with

    96 of them run captures and one (rigor/_probe.out) a stray LaTeX bookmark file

### C-2 — BLOCKING. R-B2's quantifier is false of six of the fifteen tokens

The clearance sentence now reads

> all five recovery routes fail — the four REST routes with 'No commit found' or 'Not Found',
> and git fetch of a discarded SHA with 'upload-pack: not our ref' — **for every full
> 40-character token the tracked notes carry: the two discarded commits, the compendium blob,
> and the five further private blob names and the one reconstructed subtree that the eighth
> pass added to the test**

**What the eighth pass actually did.** `rigor/referee_cleared.md` §1 and §2: Route A, the
commits endpoint, on the two discarded commit SHAs. Route B, the contents endpoint, on six
paths at one discarded ref and `cited_R1.tex` at thirteen short refs. Route C, the blobs
endpoint, on six blob SHAs computed from the working tree — `18cc05ab` (the recorded compendium
blob) and **five further** private blob names. Route D, the `commits?sha=` walk, on sixteen
seeds. Route E, `git fetch`, on the two commit SHAs. Then, in §2 and outside the five routes,
`GET /git/trees/c6c9235a…` on the reconstructed old `plan_page/` subtree.

So the *enumeration* after the colon is exactly right: 2 commits + 1 compendium blob + 5 further
private blobs + 1 reconstructed subtree = the nine objects REF-CLEARED probed, and REF-FINAL's
own F-2 says so in as many words — "the remaining nine are precisely the ones REF-CLEARED
tested and found 404". The **quantifier in front of it is not**.

The tracked notes carry **fifteen** full 40-character hash tokens, not nine. `git ls-files -z |
xargs -0 grep -hoE '[0-9a-f]{40}' | sort -u` gives 17 strings in six files, two of them decimal
run output in `numerics/optimality_all/exact_fid_L96.out` and `exact_fid_L160.out`; the fifteen
hashes live in four tracked notes (`referee_cleared.md`, `referee_pass_c.md`,
`referee_pass_d.md`, `referee_plan_split.md`). This is the same 15 REF-FINAL resolved and the
same 15 REF-README-B failed the card for. Resolving all fifteen today:

| token | what it is | do the routes fail for it? |
|---|---|---|
| `5d64c77d…`, `8b96354…` | the two discarded commits | yes, 422 / 404 |
| `18cc05ab…` | the compendium blob | yes, 404 |
| `3aa2e00b…`, `a1dc319b…`, `c8fb6e69…`, `4ef4814d…`, `07ca78ac…` | the five further private blobs | yes, 404 |
| `c6c9235a…` | the reconstructed `plan_page/` subtree | yes, 404 — but at `/git/trees/`, a sixth endpoint |
| `a5732487…`, `fac463d2…` | commits of **this** history | **no** — `gh api repos/…/commits/a5732487…` returns the commit |
| `f52aa419…` | the `v0.1.0-draft` tag target | **no** — returns the commit |
| `57a979e1…`, `9bfa5095…` | the two published root trees | **no** — `git/trees/57a979e1…` returns the tree, `truncated: false` |
| `53e81a2a…` | the **private companion's** head | not a public object at all |

I ran the first three of those "no" rows rather than reasoning about them. So the sentence, read
as it is written, is false for six of the fifteen tokens it quantifies over, and the colon
presents nine as an exhaustive list of what the notes carry. This is the same integer that
failed the card one pass ago — "all three … the tracked notes carry" measured 15 — repaired by
generalising the quantifier instead of narrowing the class, and it ships verbatim in
`docs/data/extra-claim-map.json`.

Two smaller things fall out of the same clause and the repair should take them with it: the
reconstructed subtree was probed at `/git/trees/`, which is not one of the five recorded
routes, and each of the nine was probed by the endpoints that could reach it rather than by all
five.

**The substance is intact and I checked the conclusion, not only the scope**: all nine discarded
objects 404 today, 0 forbidden paths of 624, 0 hidden by the ignore rules, every one of the 18
SHAs the four feeds publish resolving locally, `has_pages` false, both remotes private. This is
a scope-and-wording repair, not a retraction, and the defect is inherited from a verbatim
referee repair rather than authored here.

**Repair R-C2, verbatim.** In the Statement replace

    for every full 40-character token the tracked notes carry: the two discarded commits, the compendium blob, and the five further private blob names and the one reconstructed subtree that the eighth pass added to the test

with

    for all nine discarded objects the tracked notes name by a full 40-character token, each probed by the endpoints that can reach it: the two discarded commits, the compendium blob, and the five further private blob names and the one reconstructed subtree that the eighth pass added to the test (the notes carry fifteen such tokens; the other six name objects of this history or the private companion's head, and resolve rather than fail)

The short form, if the parenthesis is unwelcome: `for every full 40-character token the tracked
notes carry that names a discarded object: the two discarded commits, the compendium blob, and
the five further private blob names and the one reconstructed subtree that the eighth pass added
to the test`. That is true as written and costs six words; I prefer the long form because the
fifteen is the number a reader who repeats the measurement will get.

After R-C1 and R-C2, `make docs data` then `make check`.

---

## 4. `readme-and-figures` — FAIL

### C-3 — BLOCKING. The README-length repair turned a true clause into a false one

The commit changed the parenthetical and, four words later, a `12` into a `13`:

> README.md (**428 lines and 13 numbered sections on 2026-09-22; both grow as results are
> added, so re-measure rather than quote this**) follows section 1 of
> rigor/public_site_plan.md: **13** numbered sections, per-result status badges …, and a final
> section recording that every rigor document builds, with what the two former failures were.

Three things are wrong with the `13`, and they are the same thing seen from three sides.

**(i) Section 1 of the plan lists twelve.** `rigor/public_site_plan.md` lines 28–51, `## 1.
Deliverable A — an extensive README`, enumerates items 1 to 12, Title through *Licensing and
third-party material*. There is no thirteenth. The clause says the README follows that section
in having thirteen numbered sections; it does not, and cannot.

**(ii) The list now double-counts the section it ends on.** README `## 13. Every document
builds` *is* the thirteenth of the thirteen. Naming "13 numbered sections" and then, as a
further item of the same list, "a final section recording that every rigor document builds",
enumerates fourteen things about a thirteen-section file. This is the species of
self-refuting arithmetic that REF-CI-PAGES DEFECT 3 and REF-PASS-D D-D1(i) already failed this
project for, in a sentence one clause long.

**(iii) The card now contradicts its own History.** REF-BUILD-1b's note, in this card, reads:
"'12 numbered sections' is right as written, since rigor/public_site_plan.md section 1 lists
exactly 12 planned sections (Title … Licensing) and the build section is the 'final section' the
clause then names, giving the 13 '## N.' headings the file actually has." REF-BUILD-1c
re-confirmed it. The repair deleted the only reading under which the sentence was true, and
kept the "final section" clause that reading depended on.

**The over-hedge, same sentence.** `both grow as results are added, so re-measure rather than
quote this` is true of the line count and false of the section count. Across all fourteen
commits that have touched the new README the line count went 377, 388, 392, 391, 391, 392, 392,
394, 403, 407, 422, 430, 430, 428 — and the section count was **13 at every one of them**. It is
not a measurement that drifts; it is the plan's twelve plus the build section, and it moves only
if the outline moves. This is the other failure mode the brief names: a constant dressed as a
measurement, which invites the next reader to treat a fixed structural fact as a figure that may
already be stale.

Measured today: `wc -l README.md` = **428**, `grep -c '^## [0-9]' README.md` = **13**, headings
`## 1.` at 40 through `## 13.` at 415. So both figures in the parenthetical are right on their
stated date; it is the conformance claim and the hedge that are wrong. It ships:
`extra-claim-map.json` carries "13 numbered sections" twice.

**Repair R-C3, verbatim.** In the Statement replace

    README.md (428 lines and 13 numbered sections on 2026-09-22; both grow as results are added, so re-measure rather than quote this) follows section 1 of rigor/public_site_plan.md: 13 numbered sections, per-result status badges

with

    README.md (428 lines on 2026-09-22; the line count grows as results are added, so re-measure rather than quote it, while the thirteen numbered sections are the plan's twelve plus the build section and do not move) follows section 1 of rigor/public_site_plan.md: its twelve numbered sections, per-result status badges

and leave the closing clause `and a final section recording that every rigor document builds,
with what the two former failures were` exactly as it stands — it is what makes the thirteenth
heading accounted for, and it is true: README §13 is titled *Every document builds*, says all 41
public rigor documents compile, names both former failures, and `make rigor` exits 0 with
`46 document(s), 0 failing, 0 known` (41 public + the 5 privately held compendia).

**N-C1, non-blocking.** `## How to verify` has been empty for six passes on a tool card, which
is the one field a reader executes. `generated-docs` was given one at D-R7 and it is now the
best field on that card. Suggested: `make figures regenerates all five SVGs into docs/assets/
and git status stays clean, because every number is parsed from the file its caption cites and
the parsers assert; wc -l README.md and grep -c '^## [0-9]' README.md give the two figures
above.` I ran all three: exit 0, five files byte-identical, 428 and 13.

---

## 5. `generated-docs` — PASS

X-R2 is applied and true (§2). Everything else in the card was re-measured rather than carried:

`git ls-files 'docs/*.md'` **65** (7 top-level + 58 under `results/`); `git ls-files
'docs/read/*.html'` **66** (7 + 59 under `read/results/`, the 59th the generated index);
65 + 66 = **131**. `build_docs --check` prints `131 pages up to date`, `claims 90 (3 refereed,
30 proved, 22 numerical, 3 conjectural, …)`, `pages under results/: 58`, and the **nine**
privately held pointers by name. 30 + 3 + 22 + 3 = 58. `docs/status.md` line 5 says `90 cards:
89 claim cards … plus 1 finding`, which is where the Statement sends the reader and which is why
this card's 90 and `public-site-plan`'s 89 are not a contradiction. **786** internal link
targets over the 65 sources, 0 external, less the three LaTeX artefacts in `definitions.md` =
**783**. `grep -c '^|' refs/REFERENCES.md` = 38, less header and alignment = **36** source rows.
`bash refs/restore.sh --list` ends `20 fetchable, 16 need library access`. `held privately` on
**7** bullets across **6** result pages (`sequential-recovery-bound-type-iii` twice), all six
targets the source PDFs.

**Two wordings I would have written differently, neither a defect.**

- `Every count is computed, never typed.` reads, in place, as a claim about the generator, and
  REF-PASS-E adjudicated it that way when it wrote E-R1 to sit beside it. A reader who takes it
  as a claim about the card meets `The Statement's other figures are measured outside it` three
  sentences later. One word fixes it: `Every count the generator prints is computed, never
  typed.`
- In `How to verify`, seven of the eight recipes are commands (`git ls-files …`, `grep -c '^|'
  …`, `bash refs/restore.sh --list`, `grep -c 'held privately' …`). The eighth, `783 internal
  link targets by a scan of the 65 sources`, is a description. It is the only figure in the card
  that can go quietly false — it is outside the drift guard, which checks bytes and not link
  totals — and it is the one recipe a reader cannot paste. It has been 783 at eight consecutive
  passes because the sources are generated, so this is a suggestion and not a finding.

---

## 6. `public-site-plan` — PASS

The only edit is `430 lines)` → `428 lines on 2026-09-22 and moves with every edit)`, and 428 is
what `wc -l README.md` gives today. Re-measured, all exact: `rigor/public_site_plan.md` **237**
lines; 30 proved + 3 refereed = **33**; 33 + 12 = **45**; **89** claim cards with
`docs/status.md` named as the live figure; **ten** module pages in `docs/explore/`; **five**
SVGs in `docs/assets/`; `docs/.nojekyll` present; six phase rows P0–P5 at lines 208–213 of which
**four** carry a referee pass, P0 being one itself and P5 checked by the workflow; the four
decisions at `rigor/public_site_plan.md:224`, `## 6. Decisions — taken 2026-09-21 by the user`;
`docs/{assets,lib,data}` **1.30 MB** against the fixed 3 MB budget, the public repository
**8.31 MB** against the card's dated 8.21 MB on 2026-09-21, which the card declares dated and
growing; release assets **629,891 B** and **607,822 B**.

**Wording, not defects.**

- `built in P1; it came out at 428 lines on 2026-09-22 and moves with every edit` puts a
  past-tense production verb on a present measurement: P1 produced 430 lines on 2026-09-21, and
  428 is what `d3ca565` left on 2026-09-22. `it is 428 lines on 2026-09-22` would say it.
- The 2026-09-21 P4b note says module 10 "currently shows 86 cards" and "naming 8 distinct
  files, exactly the eight PRIVATE.md lists". It is 90 and 9 today, and `PRIVATE.md` line 61 now
  says "Ten knowledge-base cards cite nine files that live here". The note is dated, the author
  rule forbids rewriting it, and every live field of every card says nine, so the record is
  layered rather than wrong. If it ever needs to stop being layered, a new dated note is the
  instrument.
- Still open and recorded elsewhere, neither owed by this card's text: REF-FINAL F-7 (`next`
  carries `D6`, a REF-SITE-P3 defect id, in a field whose Statement says the plan has four
  decisions D1–D4) and REF-FINAL F-8's third bullet (`rigor/public_site_plan.md:235`, D3, still
  says "11 headline numericals" where the card correctly says 12 and explains the move). The
  card is the accurate one in both.

---

## 7. The carried non-blocking items of REF-README-B

| item | state |
|---|---|
| **N-B1 / REF-FINAL F-1**, "the first is public-ready" | **REPAIRED.** Reads `the project remote is public-ready but not public`. Unambiguous, and the sentence's neighbours (`BOTH REMOTES ARE PRIVATE, the companion since 2026-09-20 and the public one since its recreation on 2026-09-21`) are untouched. `the first is public-ready` returns 0 from `extra-claim-map.json`. |
| **N-B2**, the self-correcting `.out` appositive | **REPAIRED IN THE NOUN AND BROKEN IN THE APPOSITIVE.** C-1. |
| **N-B3 / REF-FINAL F-4**, "the second of the two recorded routes" | **STILL OPEN.** The ordinal is unchanged. The later sentence `The other recorded route, a GitHub Support purge of the unreachable objects, was therefore not needed` does supply a second member after the fact, so nothing is false; F-4's replacement is still the clean fix. Non-blocking. |
| **N-B4**, the third Pages step worded three ways | **STILL OPEN.** `next`: `Pages enabled once with GitHub Actions as its source`. `check.yml:62-68`: `Pages enabled once on the repository`. D1 at `public_site_plan.md:226-228`: `one line plus one click`. The extra clause is true of `actions/deploy-pages@v4` and is still in neither cited document. Non-blocking. |
| **N-B5**, the two README-length figures | **ONE REPAIRED, ONE BROKEN.** `public-site-plan`'s is now 428, dated, hedged and right (§6). `readme-and-figures`'s line count is now 428, dated and right, but the repair carried a `12`→`13` with it and hedged a constant: C-3. |

---

## 8. Cross-card consistency, and the four counts named in the brief

Read end to end, the four Statements contradict each other nowhere. Specifically:

- **Link total.** `generated-docs` and `docs-pages-rendering` both say `155 pages and 2210
  links on 2026-09-22` in the same words; `make check` prints 2210. `generated-docs`'s Statement
  figure of 783 is over a different corpus and says so. `2211` appears in no live field of any
  card and nowhere under `docs/` outside `katex.min.js`. **Agreement.**
- **Path count.** Only `repo-split` states one: 623 on 2026-09-22, dated, with the mechanism;
  624 today. `./pgit check` prints `public : 624 files`, which the card deliberately does not
  fix. No other card states a path count. **No contradiction.**
- **Commit count.** No card states one any more. **Closed.**
- **Leaking files.** `repo-split`: `NINE targets … cited by TEN cards`. I re-derived it over
  `areas/`, `claims/`, `evidence/` excluding the generated indices, resolving `#anchor` suffixes:
  **nine** distinct private targets in **twelve** evidence-token occurrences across **ten**
  distinct cards, and the nine names are exactly the nine `build_docs --check` prints.
  `generated-docs`: `DETECTED (9 …) … RENDERED … (6, on 7 bullets across 6 result pages)` —
  9 printed by the run, 7 bullets on 6 pages measured. `PRIVATE.md:61`: "Ten knowledge-base
  cards cite nine files that live here", same nine names. **Three documents, one number.** The
  only 8 left in the corpus is inside `public-site-plan`'s dated P4b note (§6).

`CHECKLIST.md`: item 3 now agrees with the Statement on all three clauses; 3d's "five … ten" is
`next`'s wording; 5's "gated only on the decision to publish" is consistent with `next`'s "No
item gates publication any more". `PRIVATE.md`: 178 excerpts, 47 PDFs, nine files, ten cards —
agrees with the card at every figure. `docs/data/extra-claim-map.json` carries all four
Statements verbatim, including both defects of §3 and §4; nothing else false about the README,
the publication steps, the link total or the private set reaches the site.

**One pre-existing tension I am not failing for, because REF-PASS-G adjudicated it.** `(./pgit
check prints the file count of each repository, and both move with every commit, so neither of
those two counts is fixed here)` is followed twelve words later by `(235 files, 48.39 MB …)`,
which fixes one of exactly those two counts — and the private count does not in fact move with
every commit: it has been 235 at REF-PASS-E, REF-PASS-F, REF-CLEARED, REF-FINAL, REF-README-B
and today, while `48,392,507 B` = 48.39 MB is also unchanged to the stated precision.
REF-PASS-G listed "235 files and 48.39 MB" under *asserted without a hedge, and exact*, which
is the reading that makes the card consistent. If it is ever touched: `the public file count
./pgit check prints moves with every commit and is not fixed here`.

---

## 9. Re-measured this pass, and exact

Figures the last two passes did not certify, plus the cheap ones worth re-running.

- **`repo-split`:** 97 tracked `.out` = 83 `numerics/` + 14 `rigor/`, exactly one a
  `\BOOKMARK` file, 23 named by a card's evidence token; private repo 235 files /
  48,392,507 B; 178 excerpts on disk and tracked; 47 `refs/*.pdf`; **255** `\shot`/`\shotc`
  call sites in **19** documents, derived from scratch across both repositories (256 sites in
  20 `.tex` files on disk — 84 in 15 public files and 172 in the five private compendia — less
  the definition at `rigor_preamble.tex`); **24** python scripts with a computed `_ROOT` and
  exactly **37** non-assignment uses (`tools/fix_paths.py` is the 25th file naming `_ROOT` and
  is the converter); the four shell scripts all read `PYTHON`; overlap 0, uncommitted 0/0;
  release assets 629,891 B and 607,822 B; repo id, creation time, `private`, `fork`,
  `has_pages` all as the card says. Files tracked by neither are **431 / 200.2 MB** against the
  card's dated `423 files, 198.6 MB on 2026-09-21`, which the card declares dated and rising.
- **`readme-and-figures`:** `make figures` exits 0 and all five SVGs are byte-identical to HEAD
  (`git status docs/assets/` clean); README 428 lines, 13 `## N.` headings at 40…415; §13 titled
  *Every document builds*, naming both former failures; `make rigor` 46 documents, 0 failing.
- **`next`'s knowledge-base hash counts** ("five of its own files under the strict rule, ten if
  every hash the recreation invalidated is counted"): I could not reproduce the strict rule's
  definition from the notes, and a blunt scan (every 7–40 hex token in the kb that does not
  resolve in cft-cmi) is not comparable — it returns 31 files, most of them numerics artefacts
  and legacy import dumps. REF-FINAL certified 5 and 10 two passes ago, and the field itself
  says the count is measured, not remembered, and needs re-measuring before that repository is
  published. Not a finding; the hedge is doing its job, and the rule deserves one sentence
  naming it wherever it is next touched.

---

## 10. Gates

`make check` — **exit 0**, printing:

    python3 tools/check_links.py
      155 pages, 2210 links resolve
      external hosts: alexander-stottmeister.github.io, github.com, projecteuclid.org
    python3 tools/build_docs.py --check
    build_docs --check: 131 pages up to date
      claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, 5 verified, 5 open, 14 active, 5 done, 2 superseded, 1 refuted)
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
      cards never refereed: 0 of the 90 listed (0 with a page); 232 of the 322 cards in the whole knowledge base, the rest being findings that reach no displayed status
      cards awaiting a referee pass: 4 (generated-docs, public-site-plan, readme-and-figures, repo-split-public-private)
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

`make rigor` — **exit 0**, `python3 tools/check_rigor_builds.py`, 46 `ok` lines and
`46 document(s), 0 failing, 0 known`.

`./pgit check` — exit 0: `public : 624 files`, `private: 235 files`, `overlap: 0  (must be 0)`,
`uncommitted: public 0, private 0`, `shots on disk 178, tracked 178`.

---

## 11. Verdicts

- **`repo-split-public-private`: FAIL** on C-1 and C-2 — R-C1 and R-C2 above. R-B1 and R-B3 are
  applied and true, N-B1 is finally closed, and the clearance itself I re-ran rather than
  accepted: nine discarded objects still 404, 0 forbidden paths of 624, 0 hidden by the ignore
  rules, every feed-published SHA resolving locally. What fails is a repair that duplicated its
  own appositive into 96 + 1 + 1 = 98, and a repair that generalised a quantifier past the
  measurement it was correcting — the tracked notes carry fifteen 40-character tokens, six of
  which the recovery routes return rather than refuse. Both ship. Neither is authored here:
  C-2 is a verbatim referee repair, and C-1 is one clause more than a verbatim referee repair
  asked for.
- **`readme-and-figures`: FAIL** on C-3 — R-C3 above. The dated 428 is right and is the right
  kind of figure. The `12` → `13` that travelled with it makes the card say the README follows a
  section of the plan that lists twelve, double-counts the section the same clause then names,
  and contradicts the REF-BUILD-1b note in this card's own History; and the hedge covers a count
  that has been 13 in all fourteen versions of the file.
- **`generated-docs`: PASS.** X-R2 applied and true, 2211 gone from the knowledge base and the
  site, every figure in the card re-measured and exact. Two wordings in §5 I would have written
  differently and neither is a defect.
- **`public-site-plan`: PASS.** The one edit is dated, hedged and right today, and everything
  else re-measures exact. The tense of "came out at" and the dated P4b note are in §6 as
  observations.
