# REF-COUNTS-B: repo-split-public-private and readme-and-figures (2026-09-22)

Thirteenth pass. Both cards **PASS**. No FAIL, so this report carries no repair wording.

The brief for this pass was narrow: twelve passes in a row have each found that a repair
damaged the sentence it was inside or next to, and the last two failures were both of that
kind. So R-C1, R-C2, R-C3 and N-C1 are taken one at a time, each read back into its sentence
and both neighbours, before anything else is looked at.

**A note on this file.** It deliberately carries no full 40-character hash and no 7-character
prefix of a discarded one. Two live measurements in the card are measurements over the tracked
notes -- "the notes carry fifteen such tokens" and "Seven public-tracked files in this
repository gave the route in words" -- and a referee report that quotes the hashes moves the
numbers it is checking. `rigor/referee_counts.md` already sits inside the second of those two
sets. Tokens below are named by role or by a six-character fragment.

---

## 1. R-C1 -- applied verbatim, true, and it damaged no neighbour

The Statement reads

> numerics scripts and the 97 tracked .out files, 83 under numerics/ and 14 under rigor/, 96 of
> them run captures and one (rigor/_probe.out) a stray LaTeX bookmark file, of which 23 are
> named by a card's evidence token

**Applied.** `stray LaTeX bookmark` occurs once in the Statement and once in
`docs/data/extra-claim-map.json`; the duplicated appositive is gone from both.

**The arithmetic closes.** `git ls-files '*.out'` **97**; `numerics/` **83**; `rigor/` **14**;
83 + 14 = 97, and no `.out` is tracked outside those two directories. Exactly **one** of the 97
opens with `\BOOKMARK`, and it is `rigor/_probe.out`; 96 + 1 = 97. **23** distinct `.out` paths
are named by a `doc:`/`num:`/`ref:` token in `areas/`, `claims/`, `evidence/`, and all 23 are in
the tracked 97.

**Neighbours.** The diff of the whole Statement against the last committed version
(`kb@d9cc6f6`) shows, in this region, one substitution and nothing else: `run captures,` ->
`files,`. The sentence before (`Since 2026-09-20 ... no tool was reconfigured.`) and everything
after the repaired clause are byte-identical to text that four passes have read. So the repair
put the sentence back exactly where REF-BUILD read it, with the noun N-B2 asked for.

**The quantifier is robust either way.** `of which 23` can attach to the 97 files or to the 96
run captures. `rigor/_probe.out` is not one of the 23, so the sentence is true under both
readings. This is worth recording because it is precisely the hinge the duplicated clause had
broken.

**Carried, not re-opened.** `(./pgit check prints the file count of each repository, and both
move with every commit, so neither of those two counts is fixed here)` is followed twelve words
later by `(235 files, 48.39 MB ...)`, which fixes one of them, and the private count has now
been 235 at seven consecutive passes. REF-PASS-G adjudicated this and REF-COUNTS carried it;
R-C1 did not touch it and I do not re-open it. REF-COUNTS's one-line fix, if the clause is ever
edited, is still the right one.

---

## 2. R-C2 -- applied verbatim; the nine, the fifteen and the six are all exact today

The Statement reads

> all five recovery routes fail -- the four REST routes with 'No commit found' or 'Not Found',
> and git fetch of a discarded SHA with 'upload-pack: not our ref' -- **for all nine discarded
> objects the tracked notes name by a full 40-character token, each probed by the endpoints
> that can reach it**: the two discarded commits, the compendium blob, and the five further
> private blob names and the one reconstructed subtree that the eighth pass added to the test
> **(the notes carry fifteen such tokens; the other six name objects of this history or the
> private companion's head, and resolve rather than fail)**

**Applied**, word for word, including the parenthesis; `every full 40-character token` returns 0
from `extra-claim-map.json`.

**The fifteen, re-measured after both new notes were committed.** This is the number the brief
asked me to move. `git ls-files -z | xargs -0 grep -IhoE '\b[0-9a-f]{40}\b' | sort -u` gives
**15**, in four tracked notes: `referee_cleared.md`, `referee_pass_c.md`, `referee_pass_d.md`,
`referee_plan_split.md`. Without the word boundaries it gives 17 in six files, the extra two
being decimal run output in `numerics/optimality_all/exact_fid_L96.out` and `exact_fid_L160.out`
-- the same 17/15 split REF-COUNTS measured. **`rigor/referee_counts.md` and
`rigor/referee_readme_b.md` are both tracked and neither carries a single full 40-character
token**; both truncate with an ellipsis. The private repository's 235 tracked files carry none
either. So the fifteen has not moved, and the sentence's construction does not have to survive a
change, because there is none.

**The nine and the six, resolved one by one.** Of the 15, nine name objects absent from the
local history and six resolve:

| the nine (all absent locally) | the six (all resolve) |
|---|---|
| the two discarded commits (`5d64c7…`, `8b9635…`) | two commits of this history (`a57324…`, `fac463…`) |
| the compendium blob (`18cc05…`) | the `v0.1.0-draft` tag target (`f52aa4…`) |
| the five further private blobs (`3aa2e0…`, `a1dc31…`, `c8fb6e…`, `4ef481…`, `07ca78…`) | the two published root trees (`57a979…`, `9bfa50…`) |
| the reconstructed `plan_page/` subtree (`c6c923…`) | the private companion's recorded head (`53e81a…`) |

2 + 1 + 5 + 1 = **9**; 9 + 6 = **15**. The enumeration after the colon matches its stated
number and the parenthesis accounts for the remainder exactly.

**I ran the routes rather than accepting them.** `commits/` returns `No commit found for SHA` for
both discarded commits; `git/blobs/` returns `Not Found` for the compendium blob, for
`a1dc31…` (`rigor/cited_R1.tex`) and for `3aa2e0…` (`plan_page/petz_program_plan.html`);
`git/trees/` returns `Not Found` for the reconstructed subtree. On the other side, `commits/`
returns the commit for `a57324…` and `f52aa4…`, `git/trees/` returns the tree for `57a979…` and
`9bfa50…`, and `53e81a…` is a commit that `git --git-dir=.git-private cat-file -t` resolves. So
"resolve rather than fail" is true of the six, and the six are exactly the ones that are not
discarded. I did not run `git fetch`, which writes.

**Neighbours.** Nothing doubled, no count broken, no pronoun re-pointed. `each probed by the
endpoints that can reach it` -- "it" is each of the nine. `the other six` -- of the fifteen, not
of the nine. The three clauses after the parenthesis (`every hash the four feeds publish
resolves in the local history`; `every path ever added is checked ...`; `no path in the whole
history is one the current ignore rules would hide`) are the ones R-B3 rewrote a pass ago and
R-C2 left untouched; re-measured today they are still true: **625** paths ever added over all
refs, **0** of them under `rigor/shots/`, `refs/*.pdf`, `rigor/cited_*` or `plan_page/`, and
**0** returned by `git check-ignore` over the whole list.

**Three observations, none of them a defect.**
- The sentence now reads `A; B; and C; and D` -- two coordinating "and"s across three
  semicolon-separated items. Clumsy, not false.
- `623 paths on 2026-09-22` is **625** today. The card dates it and says in the same breath "one
  more with every commit, so this is a check to re-run and not a number to carry"; two commits
  have landed. This is the treatment the brief calls correct, not drift to fail on.
- `the private companion's head` was the head when `referee_cleared.md` recorded it; today
  `53e81a…` is an ancestor of the private head. It still resolves, which is all the clause
  claims of it, but the descriptor is dated. One word ("recorded head") if the clause is ever
  touched.
- REF-COUNTS asked the repair to carry the point that the subtree was probed at `/git/trees/`,
  which is not one of the five recorded routes. `each probed by the endpoints that can reach it`
  carries it, and the five do also fail for a tree SHA, so the head of the sentence is not false
  either. Closed.

---

## 3. R-C3 -- applied verbatim; twelve and thirteen both verified, and the enumeration no longer over-counts

The Statement reads

> README.md (**428 lines on 2026-09-22; the line count grows as results are added, so re-measure
> rather than quote it, while the thirteen numbered sections are the plan's twelve plus the
> build section and do not move**) follows section 1 of rigor/public_site_plan.md: **its twelve
> numbered sections**, per-result status badges ..., and a final section recording that every
> rigor document builds, with what the two former failures were.

**Applied**, and the closing clause is untouched, as the repair asked. `13 numbered sections`
returns 0 from `extra-claim-map.json`; `twelve numbered sections` and `thirteen numbered
sections` return 1 each.

**The plan's twelve.** `rigor/public_site_plan.md` lines 28-51, `## 1. Deliverable A -- an
extensive README`, enumerates items 1 to 12, *Title, one-paragraph statement of the problem*
through *Licensing and third-party material*. There is no thirteenth item.

**The README's thirteen.** `grep -c '^## [0-9]' README.md` = **13**, at lines 40, 62, 80, 115,
148, 190, 233, 281, 307, 350, 368, 397, 415. The first twelve are the plan's twelve in the
plan's order, heading for heading; the thirteenth, at 415, is `## 13. Every document builds`.
So 12 + the build section = 13, and the parenthetical states the identity the arithmetic needs.
`wc -l README.md` = **428**, exact on the stated date.

**The enumeration does not over-count.** After the colon the card names: the twelve numbered
sections, per-result status badges, hypotheses named for (H1,H2,H3) and (H), PDFs linked to the
release, open problems verbatim, the paper1 provenance text verbatim, LICENSE and
THIRD-PARTY.md, and a final section. Only the first and the last are sections; the six in
between are properties of sections already counted (badges live in S1's table, open problems are
S8, provenance is S11, licensing is S12). 12 + 1 = 13 things about a thirteen-section file. The
species of self-refuting arithmetic that failed REF-CI-PAGES DEFECT 3, REF-PASS-D D-D1(i) and
REF-COUNTS C-3(ii) is not present.

**The hedge now covers only what moves.** `the line count grows ... so re-measure rather than
quote it` applies to the 428 alone; the section count is asserted as fixed and given its
mechanism. The card's own History is no longer contradicted: this is REF-BUILD-1b's reading
("12 planned sections ... and the build section is the final section the clause then names,
giving the 13 `## N.` headings the file actually has"), restored and now written out.

**Neighbours.** The sentence is the last of the Statement, so it has one neighbour: `Every
parser asserts against its source file and the script fails loudly on drift; no number is typed
in.` It is byte-identical to the version REF-README-1c passed, and the repair touched nothing in
it. `no number is typed in` is about the figure script, not about the README figures, so the
dated 428 beside it is not a contradiction.

**One observation.** In `follows section 1 of rigor/public_site_plan.md: its twelve numbered
sections`, `its` attaches to the plan (nearest antecedent, and the only reading on which the
clause is true); a reader who attached it to README.md would read a twelve the parenthetical has
just called thirteen. The parenthetical pre-empts that, so nothing is false, and `the plan's
twelve numbered sections` would close it in one word if the clause is ever edited for another
reason. The forward reference in `the plan's twelve` (the plan is named in the next clause) is
the same observation.

---

## 4. N-C1 -- the new How to verify, executed exactly as written

The field now reads

> make figures regenerates all five SVGs into docs/assets/ and git status stays clean, because
> every number is parsed from the file its caption cites and the parsers assert rather than
> accept. wc -l README.md and grep -c '^## [0-9]' README.md give the two figures above.

Two departures from REF-COUNTS's suggested text, both harmless: `assert rather than accept` for
`assert`, and a full stop for the semicolon. It ships: `extra-claim-map.json` carries it as the
card's `verify` field.

| command | claim | what it did |
|---|---|---|
| `make figures` | regenerates all five SVGs into `docs/assets/`, and `git status` stays clean | **exit 0**. Five files written: `geometry.svg` 7,768 B, `quadratic-law.svg` 14,754 B, `universality.svg` 9,337 B, `theta-ladder.svg` 11,189 B, `corner-calculus.svg` 12,862 B. All five sha256 digests unchanged, `git status --porcelain` empty before and after. **Does what it claims.** |
| `wc -l README.md` | gives the first figure above | **428**, the Statement's figure. **Does what it claims.** |
| `grep -c '^## [0-9]' README.md` | gives the second figure above | **13**, the Statement's "thirteen". **Does what it claims.** |

The `because` clause is a summary of the Statement rather than the strict cause of the clean
status (determinism is), and it is the card's own framing. `tools/make_figures.py` imports only
`math`, `re`, `sys` and `pathlib`, so "stdlib only" holds; it is 1010 lines with 27 `assert`s.

**One observation, non-blocking.** `give the two figures above` will go false for the line count
the next time the README grows, in a field that does not repeat the Statement's date. The
Statement two lines up already says to re-measure rather than quote it, so a reader is not
misled, and per the brief a dated figure that drifts is not a defect. If the field is ever
touched: `... give the line count and the section count above, the first on its stated date.`

---

## 5. Both Statements read end to end: no sentence contradicts another

I read both Statements, both `next` fields, both `How to verify` fields, `CHECKLIST.md`,
`PRIVATE.md` and `docs/data/extra-claim-map.json`, and found no contradiction.

- **What ships.** `extra-claim-map.json` carries both Statements character for character, apart
  from six `(held privately)` annotations the site build inserts at private paths -- with those
  stripped, both strings are equal to the card. The three defects of the last pass are gone from
  the site: `13 numbered sections` 0 hits, `every full 40-character token` 0 hits, `stray LaTeX
  bookmark` exactly 1.
- **CHECKLIST.md.** Item 3's clearance sentence states the five routes without the nine/fifteen
  scope; the card is the narrower statement, so there is nothing to disagree with. 3c's "Seven
  tracked files gave the commit and blob hashes" is the Statement's "Seven public-tracked files
  ... gave the route in words" and its "The seven files ... are kept rather than moved". 3d's
  "Nothing gates the cft-cmi release on it" is `next`'s "No item gates publication any more"
  plus "One item survives elsewhere". Item 4's fourteen captures plus seven scratchpad
  references is **21** tracked files naming `/Users/alex` -- measured 21, and **0** of them a
  `.py`, which is what makes the Statement's "the 24 python scripts ... now resolve paths
  against a computed `_ROOT`" and item 4 describe disjoint sets.
- **PRIVATE.md.** 178 excerpts, 47 PDFs, "Ten knowledge-base cards cite nine files that live
  here". I re-derived both independently: **nine** distinct private targets across **ten**
  distinct cards (`all-channel-equals-quasi-free`, `all-channels-symbol-feasible`,
  `fidelity-formula-correction`, `implementer-hypotheses`, `open-problems-plan-note8`,
  `plan-page`, `repo-split-public-private`, `sequential-recovery-bound-type-iii`,
  `single-observable-bound`, `vwz-protocol-ordering`), and `build_docs --check` prints the same
  nine names.
- **`next` against the world.** The three Pages steps are in the `check.yml` comment at 62-68
  ("Publishing needs THREE things, as decision D1 says") and in D1 at `public_site_plan.md`
  226-228; `if: false` is at `check.yml:70`; the README names none of them, which is what
  "dropped from the README on 2026-09-22" asserts. `has_pages` false, both remotes private, repo
  id 1380449076, `created_at` 2026-09-21T19:55:13Z, `fork` false -- all as the Statement says.
  N-B4 (the third step worded three ways) is unchanged and still non-blocking.
- **The one place the two cards touch.** `public-site-plan` says the README "came out at 428
  lines on 2026-09-22 and moves with every edit"; `readme-and-figures` says "428 lines on
  2026-09-22; the line count grows as results are added". Same figure, same date, same
  direction. Neither states a section count that could disagree, and the plan-outline remark
  about the README's 'Status vocabulary' is about bold text inside S1, not a `## N.` heading.
- **The word "superseded" in `readme-and-figures`.** The Statement's "the superseded
  taper-suppressed circle value" is adjectival. The README it describes says at l.175
  "superseded by the reconciliation (though no card carries that status)", and
  `theta-ladder.svg` says "its value is superseded, not a competing one"; no card status is
  asserted anywhere, and `build_docs` still counts 2 superseded cards. D7/D7b stay closed.

---

## 6. Re-measured this pass, and exact

Figures neither of the last two passes certified, plus the cheap ones worth re-running.

- **The private set, item by item.** `git --git-dir=.git-private ls-files` = **235** =
  178 `rigor/shots/` + 47 `refs/` + exactly the ten files the Statement lists outside those two
  directories (`CHECKLIST.md`, `PRIVATE.md`, `pgit`, `pgit-exclude`,
  `plan_page/petz_program_plan.html`, `rigor/cited_R1..R4.tex`, `rigor/cited_results_all.tex`).
  "which is exactly what `git --git-dir=.git-private ls-files` lists outside the first two
  directories" is true with nothing left over.
- **299,915 bytes.** `rigor/cited_results_all.tex` is 299,915 B on disk and the recorded
  compendium blob is 299,915 B in the private object store; it is the largest of the five
  (70,874 / 72,489 / 66,304 / 90,433). "the largest of them byte-identical to the private copy
  at its full 299,915 bytes" holds.
- **`refs/restore.sh` recovers exactly one.** The script reads `REFERENCES.md`, skips every line
  that is not a table row, and names the output from the *Short* column. VWZ is a row carrying
  `arXiv:2307.14434` -> recovered under the cited filename. Uhlmann76 is a row whose source cell
  is "paywalled: find open restatement", with no arXiv id and no URL -> MANUAL. CDIT is tabled
  under the short name `CDIW21` -> a different filename. AlbertiUhlmann02,
  BJL_twisted_duality and Sion1958_minimax are bullets at `REFERENCES.md` 49-51, not rows.
  **One of six**, exactly as the Statement says, and for the reasons it gives.
- **Files tracked by neither: 432 / 200.4 MB** today, against the card's dated `423 files,
  198.6 MB on 2026-09-21` and REF-COUNTS's 431 / 200.2 MB yesterday. The difference from
  yesterday is **+1**, and it is this review's packet -- the mechanism the hedge names, behaving
  exactly as the hedge predicts.
- **`./pgit check`** exit 0: `public : 625 files`, `private: 235 files`, `overlap: 0`,
  `uncommitted: public 0, private 0`, `shots on disk 178, tracked 178`. `git log` runs in both
  repositories and `rigor/README_AGENTS.md:36` is the section `How to verify` names, so that
  field executes as written too.
- **README S11 provenance** is verbatim in `paper1/main.tex` (compared after normalising LaTeX
  markup and whitespace: the whole 1,642-character block is a substring).
- **README S8 open problems** -- all **five** `next:` lines are character-for-character the
  `next` fields of `sectors-o11`, `multi-interval-networks`, `corner-correlation-kernel`,
  `theta-modular-wiener-hopf` and `dhat-quadrature-certification`, and `build_docs` prints
  `5 open`, so "Five items carry status `open`" and "verbatim from the KB" both hold.
- **README status badges** -- every backticked status word in the file
  (`proved` 11, `refereed` 6, `numerical` 14, `verified` 1, `conjectural` 5, `open` 4,
  `refuted` 4, `superseded` 1) is in the vocabulary S1 declares. "per-result status badges in
  the project vocabulary" holds with no stray label.
- **`kb -p cft_cmi lint`** -- `0 issue(s), 2 awaiting review`.

Not re-derived, and why: the 44 discarded commits and the 66-byte controlled rebuild are
historical facts about a remote that no longer exists and about a build whose inputs the card
says were never recorded -- the card itself marks the second as "an inference from that rebuild
and not a comparison". `next`'s five/ten knowledge-base hash counts are flagged in the field as
measured and needing re-measurement, and REF-FINAL certified them; REF-COUNTS could not
reproduce the strict rule's definition either, and the rule still deserves one naming sentence
wherever it is next touched.

---

## 7. Gates

`make check` -- **exit 0**, printing:

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
      cards awaiting a referee pass: 2 (readme-and-figures, repo-split-public-private)
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

`make rigor` -- **exit 0**, `python3 tools/check_rigor_builds.py`, 46 `ok` lines and
`46 document(s), 0 failing, 0 known`.

`make figures` -- **exit 0**, five SVGs written and byte-identical, `git status` clean.

The only difference from REF-COUNTS's gate output is the awaiting-review line, 4 -> 2, which is
that pass's two PASSes landing.

---

## 8. Verdicts

- **`repo-split-public-private`: PASS.** R-C1 and R-C2 are applied verbatim, each is true, and
  neither damaged the sentence it landed in or either neighbour. The two numbers the last pass
  failed the card over now close: 96 + 1 = 97 with exactly one `\BOOKMARK` file, and the
  quantifier covers nine discarded objects out of fifteen tokens with the other six named and
  shown to resolve. I re-ran the conclusion rather than accepting it -- the discarded objects
  still 404 at `commits/`, `git/blobs/` and `git/trees/`, the six resolving tokens still
  resolve, 625 paths ever added with 0 forbidden and 0 hidden -- and re-derived the private set,
  the compendium size, the restore.sh disposition and the nine-targets/ten-cards count from
  scratch. Four wordings I would have written differently are in §2 and §1; none is a defect.
- **`readme-and-figures`: PASS.** R-C3 is applied verbatim and both its counts verify against
  the two files: the plan's section 1 enumerates twelve, the README has thirteen `## N.`
  headings, the thirteenth is the build section, and the enumeration after the colon now names
  twelve plus one rather than thirteen plus one. The hedge sits on the line count, which moves,
  and not on the section count, which has not. N-C1 is applied and all three of its commands do
  what they claim: `make figures` exits 0 with five byte-identical SVGs and a clean tree, and
  the two counting commands return 428 and 13. Two wordings are in §3 and §4; neither is a
  defect.
