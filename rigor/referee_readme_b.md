# REF-README-B: docs-pages-rendering and repo-split-public-private (2026-09-22)

Eleventh pass. Scope: the four repairs the author took from REF-README (R-1, X-R1, N-1, N-3), the
neighbours of each of them in both cards and in both directions, both Statements read end to end,
and everything about the README, the link total and the publication steps that reaches the public
site. Everything below was measured or executed at HEAD `5415b50` (2026-09-22 10:12:17 +0200), not
read off a previous report.

**Verdicts: `docs-pages-rendering` PASS. `repo-split-public-private` FAIL** on three items, none of
them X-R1, all three of them counts and a contradiction that REF-FINAL wrote out one pass ago and
that were not applied. And the chain's signature failure recurred once more, this time inside
REF-README's own sweep: R-1 corrected the link total in the card that owns it and left the *same*
integer false in `generated-docs`, where it still ships. That is X-R2.

Context, from the user: publication was declined for now. The repository is private, Pages is not
enabled, `if: false` is in place. Every statement below is judged against that state.

---

## 1. R-1 — the author did not apply my predecessor's literal substitution, and was right not to

REF-README asked for `2211` → `2210`. `How to verify` now reads:

> After make docs data, make check is green: check_links resolving every link it finds over the
> tracked pages (**155 pages and 2210 links on 2026-09-22; the total moves whenever any tracked page
> gains or loses a link, so read what the run prints rather than this figure**), build_docs --check
> 131 pages up to date, all nine data files ok.

**Is it true?** Yes, clause by clause. `make check` exits 0 and prints `155 pages, 2210 links
resolve` — so the dated figure is right today, to the digit. `build_docs --check: 131 pages up to
date`. Nine `ok` lines, for `quadratic-law`, `constants`, `theta`, `universality`, `networks`,
`extra-separation`, `extra-off-criticality`, `extra-relative-entropy`, `extra-claim-map`. The new
head clause, "check_links resolving every link it finds over the tracked pages", is the tool's
actual contract and holds: 0 broken, exit 0.

**Does it still verify what the field exists to verify?** Yes, and better. The thing under test is
that every link on every tracked page resolves — a property, not an integer. The old form promised a
number, so a reader who got 2210 where 2211 was promised had to decide whether the card or the tool
was wrong. The new form promises the property, gives the number as a dated measurement, and names
the mechanism by which it moves. A reader still executes exactly one command and still gets a
green/red answer.

**Does it remove the recurrence?** Yes. This integer failed three passes — B6, C-R1, and F-1 in
REF-README — always the same way: a commit changed a link somewhere and the card did not follow. A
figure that is dated and explicitly handed back to the run cannot fail that way again. It is also
the pattern that the three items in §4 below still need.

**Does it ship?** Yes, verbatim. `docs/data/extra-claim-map.json`, `verify` field of
`docs-pages-rendering`, carries the new sentence word for word, so the site and the card agree.

R-1 is answered. I would not have written it differently.

## 2. X-R1 — applied verbatim; both sentences are true and the contradiction is gone

Both substitutions are in `repo-split-public-private`'s `next`, character for character as
REF-README wrote them, and both are in the shipped claim map.

**Sentence 1** — "Publishing now needs only the three Pages steps of decision D1: the repository
going public, the if: false removed from the Pages job, and Pages enabled once with GitHub Actions
as its source."

- *"only"*: no CHECKLIST item gates it. Items 1, 2, 3, 3b are struck and DONE; 3c is MOOT; 3d says
  in its own words "Nothing gates the cft-cmi release on it"; 3e is advice on reading old hashes;
  4 records a decision to leave the captured logs alone; 5 says publication "is gated only on the
  decision to publish"; 6 is the private-first option. Nothing outstanding.
- *step 1*: `gh api repos/alexander-stottmeister/cft-cmi` → `private: true`, `visibility: private`,
  `fork: false`.
- *step 2*: `.github/workflows/check.yml:70` is still `if: false`.
- *step 3*: `has_pages: false`; `gh api .../pages` → 404 Not Found.

**Sentence 2** — "CHECKLIST.md items 3 to 3e record the clearance; the three Pages steps are in
decision D1 and in the workflow comment, and were dropped from the README on 2026-09-22 because a
published README does not need them."

- CHECKLIST.md carries items `3`, `3b`, `3c`, `3d`, `3e` at lines 16, 27, 31, 43, 49, and they are
  the clearance record.
- **D1** is `rigor/public_site_plan.md:226-228`, under `## 6. Decisions — taken 2026-09-21 by the
  user`: "**Pages goes live only when the repository goes public.** … the Pages deployment step of
  P5 is written but left disabled, and enabling it is one line plus one click once `CHECKLIST.md` is
  clear." Public + one line + one click: the three steps are there, in that order, and `ci-green`'s
  Statement reads D1 the same way ("which is what rigor/public_site_plan.md:226 means by 'one line
  plus one click'").
- **The workflow comment** is `.github/workflows/check.yml:62-68` and is explicit: "Publishing needs
  THREE things, as decision D1 says (rigor/public_site_plan.md): the repository going public,
  because the free tier serves Pages for public repositories only; this `if: false` removed; and
  Pages enabled once on the repository."
- **Dropped from the README on 2026-09-22**: `d3ca565`, 2026-09-22 07:57:37 +0200, README.md only.
  I re-ran the sweep rather than trusting it: a case-insensitive grep of the 428 lines for
  `public|private|publish|not yet|404|enabl|if: false|serve` returns ten hits, and not one states a
  condition on publication. The ten are: the two bare present-tense statements that the address
  serves (33, 335-336), "not yet certified" about a result (113), the private knowledge base (342),
  third-party redistribution (385, 403, 412), "not yet by a human" (394), and the rigor build count
  (417).

**No contradiction left.** `docs-pages-rendering` says "It no longer explains what publication
requires"; `repo-split-public-private` now says the steps "were dropped from the README". The two
cards agree, and `docs/data/extra-claim-map.json` no longer contains "the README lists" or "are in
the README" anywhere.

One wording note, not a defect: the third step is now worded three ways in three places — "Pages
enabled once with GitHub Actions as its source" (`repo-split` `next`), "Pages enabled once on the
repository" (`docs-pages-rendering`, the workflow comment), "one click" (D1). The extra clause is
true — `actions/deploy-pages@v4` only serves a site whose build source is GitHub Actions — but it is
in neither of the two documents the sentence cites for it. See N-B4.

## 3. N-1 and N-3 — taken, and the replacement is clean

The author did not use my predecessor's literal N-1 sentence. The paragraph now reads:

> The consequence while the repository stays private is that the README points at an address that
> does not serve and says nothing about it; **that** is visible to nobody but **the repository's
> owner**, and it resolves **when all three publication steps have landed, not merely when the
> repository goes public**.

- **The pronoun (N-1).** `which` is gone. `that` opens a new clause and takes the whole preceding
  clause — the README pointing at a dead address and saying nothing about it — which is what is
  meant. The wrong readings REF-README identified ("no caveat", "an address") are no longer
  available, because there is no relative pronoun hanging off a noun phrase.
- **N-3, both sites.** "at the author's instruction" → "**at the user's instruction**", and the
  ambiguous "the author" later in the same sentence pair → "**the repository's owner**". Both
  readings of "the author" are now impossible, in both places. This is more than N-3 asked for and
  it is right.
- **The scope of "resolves" (this was N-2, and it is now closed too).** "when all three publication
  steps have landed, not merely when the repository goes public" is exactly the distinction that
  DEFECT 3(b) and B1 failed two cards for. It is also true: after the three steps, the deploy job
  runs and the address serves.
- **Truth of each clause, re-measured.** `curl -o /dev/null -w '%{http_code}'` → **404** for
  `https://alexander-stottmeister.github.io/cft-cmi/` and for `.../cft-cmi/read/status.html`;
  `has_pages` false; `/pages` 404 — "does not serve". The grep above — "says nothing about it".
  `private: true`, `fork: false`, one collaborator (`alexander-stottmeister`), the only release
  being a release of that private repository — "visible to nobody but the repository's owner".
- **Every other reference in the paragraph.** "It no longer explains…" → README, the subject of the
  sentence before. "that paragraph" → the one `d3ca565` deleted. "What publication requires is
  unchanged and is recorded in decision D1, in the workflow comment and on ci-green" → all three
  carry it and agree (§2), and "unchanged" holds because `d3ca565` touched README.md only.
  "so it cannot do the third step and is not set" → `actions/configure-pages@v5` is declared at
  `check.yml:76` with no `with:` block.
- **Re-measured, all exact**: README is 428 lines; `grep -n github.io` gives six hits at **29, 35,
  36, 337, 338, 339**; `## 1.` at **40**, `## 9.` at **307**, `## 10.` at **350**, so three hits are
  before section 1 and three inside 307-349.

## 4. `repo-split-public-private` — the three FAILs

All three were written out by REF-FINAL one pass ago as F-2 and F-3, ruled non-blocking on the
reading that the clearance paragraph is dated by "Verified afterwards", and not applied. I am
failing them now for two reasons the previous pass did not have: the drift has gone from +1 to +6
and, on one count, to four times the stated value; and one of the four is not in the dated sentence
at all. The substance of the clearance is untouched — I re-verified it below — and the repairs cost
three substitutions.

### B-1 — BLOCKING. "holds only the 68 commits of this history": it holds 74

The sentence, in full:

> What bounded the exposure while it lasted was access control alone — the repository has never been
> public, is unforked and has no other collaborators — and what ends it is that the objects no
> longer exist: the repository serving this name was created at 2026-09-21T19:55:13Z with a new id
> and **holds only the 68 commits of this history**.

`git rev-list --count HEAD` → **74**. `git ls-remote origin` → `refs/heads/main` and `HEAD` both
`5415b504`, the local HEAD, and `refs/tags/v0.1.0-draft` `f52aa419`, so the remote holds the same 74.
The repository id (1380449076) and `created_at` (2026-09-21T19:55:13Z) in the same sentence are both
exact.

This clause is in **present tense**, it is **not** inside the "Verified afterwards" sentence, and it
carries no date and no instruction to re-measure, so the exemption for a dated figure does not
reach it. It was 69 when REF-FINAL measured it; it is 74; it will be 75 when this report is
committed. It ships: the Statement is carried verbatim in `docs/data/extra-claim-map.json`.

**Repair R-B1, verbatim** (this is REF-FINAL's F-2c, unchanged). In the Statement replace

    with a new id and holds only the 68 commits of this history

with

    with a new id and holds this history and nothing else

### B-2 — BLOCKING. The clearance sentence's three counts are 15, 8 and 623, not 3, 2 and 621

> Verified afterwards, and this is the check that matters rather than the clone: all five recovery
> routes fail — the four REST routes with 'No commit found' or 'Not Found', and git fetch of a
> discarded SHA with 'upload-pack: not our ref' — for **all three full 40-character tokens the
> tracked notes carry**, the two commits and the compendium blob; **the four feeds publish two
> hashes between them** and both resolve in the local history; **621 distinct paths** were ever
> added and none is an excerpt, a source PDF, a compendium or the plan page; and no path in the
> whole history is one the current ignore rules would hide.

| clause | says | measured 2026-09-22 |
|---|---|---|
| "all three full 40-character tokens the tracked notes carry" | 3 | **15** |
| "the four feeds publish two hashes between them" | 2 | **8** |
| "621 distinct paths were ever added" | 621 | **623** |

- **Tokens.** `git ls-files -z \| xargs -0 grep -hoE '[0-9a-f]{40}' \| sort -u` → 17 distinct
  forty-character strings, two of which are decimal run output in
  `numerics/optimality_all/exact_fid_L96.out` and `exact_fid_L160.out`. Fifteen are hashes, in four
  tracked notes (`rigor/referee_cleared.md`, `referee_pass_c.md`, `referee_pass_d.md`,
  `referee_plan_split.md`). Same 15 REF-FINAL found; the card still says three.
- **Feeds.** `/actions/runs` → `total_count` 8, eight distinct `head_sha`; `/activity` → eight rows
  (seven `push`, one `branch_creation`) whose `before`/`after` are that same set plus the zero SHA;
  `/events` → six entries; the owner timeline → three `PushEvent` for this repository. Union:
  **eight** real SHAs — `0b7a2f1`, `5415b50`, `a318d25`, `a573248`, `c52a2dc`, `c9d77b0`, `d3ca565`,
  `fac463d` — and every one of them resolves in the local history. The card says two. It is four
  times that, and it is the sentence a reader checks the clearance with.
- **Paths.** `git log --all --diff-filter=A --name-only` → **623** distinct paths.

**The substance is intact, and stronger than the sentence**, which is why this is a wording-and-count
repair and not a retraction. I checked the conclusion, not just the counts: of the 623 paths, **0**
match `rigor/shots/`, `*.pdf`, `rigor/cited_R[1-4].tex`, `rigor/cited_results_all.tex` or
`plan_page/`; `git check-ignore` over all 623 hides **0**; all eight published hashes resolve
locally; and the repository id and creation time are unchanged.

**Repair R-B2, verbatim.** In the Statement replace

    for all three full 40-character tokens the tracked notes carry, the two commits and the compendium blob; the four feeds publish two hashes between them and both resolve in the local history; 621 distinct paths were ever added and none is an excerpt, a source PDF, a compendium or the plan page

with

    for every full 40-character token the tracked notes carry: the two discarded commits, the compendium blob, and the five further private blob names and the one reconstructed subtree that the eighth pass added to the test; every hash the four feeds publish resolves in the local history; and every path ever added is checked, none of them an excerpt, a source PDF, a compendium or the plan page (623 paths on 2026-09-22, one more with every commit, so this is a check to re-run and not a number to carry)

### B-3 — BLOCKING. CHECKLIST.md, an evidence token of this card, contradicts the Statement

`evidence:` includes `doc:CHECKLIST.md`. Item 3 closes:

> Verified after the push: all five recovery routes return "No commit found" or "Not Found"; the
> four feeds publish two hashes and both resolve locally; 621 paths ever added, none an excerpt, a
> PDF, a compendium or the plan page.

The Statement says the opposite about the fifth route: "the four REST routes with 'No commit found'
or 'Not Found', **and git fetch of a discarded SHA with 'upload-pack: not our ref'**". The Statement
is the correct one — REF-CLEARED measured that string — so the card is contradicted by the document
it cites as evidence for the clearance, on the one route that is not a REST call. The same sentence
also repeats both counts B-2 corrects. REF-FINAL wrote this as F-3 and it was not applied; it is
private-tracked and does not reach the site, which is why it is last of the three and not first.

**Repair R-B3, verbatim** (REF-FINAL's F-3, unchanged). In CHECKLIST.md item 3 replace that sentence
with

    Verified after the push: all five recovery routes fail — the four REST routes with "No commit found" or "Not Found", and git fetch of a discarded SHA with "upload-pack: not our ref"; every hash the four feeds publish resolves locally; every path ever added is checked, and none is an excerpt, a PDF, a compendium or the plan page.

After R-B1 and R-B2, run `make docs data` so `docs/data/extra-claim-map.json` carries them, then
`make check`.

## 5. X-R2 — NOT either card under review, live, shipped, and the same integer R-1 just repaired

This is the finding of this pass. REF-README wrote, in its own §6, "**One** false number does ship,
and it is F-1." Two did. The README edit `d3ca565` took the site's link total from 2211 to 2210 and
falsified **two** `verify` fields, not one. R-1 repaired `docs-pages-rendering`'s. The other is still
there, in a card that is `review: passed 2026-09-21 by REF-PASS-F`:

`kb/projects/cft_cmi/claims/generated-docs.md`, `How to verify`:

> 783 internal link targets by a scan of the 65 sources (**check_links.py's own totals, 155 pages and
> 2211 links**, are over the whole site and are a different corpus)

`grep -rn 2211 docs/` finds it at `docs/data/extra-claim-map.json`, the `verify` field of
`generated-docs` (the only other hit under `docs/` is a byte sequence inside
`docs/lib/katex/katex.min.js`). `make check` prints 2210. The figure is undated, unhedged, and told
to nobody to re-measure, so it is exactly the class R-1 was written to end — and the knowledge base
now ships **both** 2210 and 2211 for the same tool's output, one card apart, both rendered by module
10. `docs-pages-rendering` is the one that is right, which is why this is here and not in its
verdict, but it has to move in the same pass.

**Repair X-R2, verbatim.** In `generated-docs`'s `How to verify` replace

    783 internal link targets by a scan of the 65 sources (check_links.py's own totals, 155 pages and 2211 links, are over the whole site and are a different corpus)

with

    783 internal link targets by a scan of the 65 sources (check_links.py's own totals are over the whole site and are a different corpus: 155 pages and 2210 links on 2026-09-22, a total that moves whenever any tracked page gains or loses a link, so read what the run prints)

then `make docs data` and re-run `make check`.

## 6. Both Statements read end to end; everything that reaches the public site

**Contradictions between the two cards: none.** The publication-steps pair is now consistent in both
directions (§2). Nothing else in either card speaks about the other's subject.

**Inside `docs-pages-rendering`: none that is false.** The `.nojekyll` rule, the blacklist-not-a-proof
paragraph, the three link classes, the emphasis rule, the fidelity paragraph and the README paragraph
do not collide; `How to verify`'s hedge ("that measures Python's mimetypes table, not GitHub's, and
Pages has never been enabled on this repository") agrees with the Statement's "Pages has never been
enabled on this repository (has_pages false)". `next`'s two claims hold: `grep -c '<a id=' docs/status.md`
= **8**, and `docs/lib/katex/` is vendored while the mirror has no renderer.

**Inside `repo-split-public-private`**: the three of §4, plus the non-blocking items in §7.

**CHECKLIST.md**: item 3, B-3. Everything else agrees with the card — 3d's "five … ten" and "Nothing
gates the cft-cmi release on it" are `next`'s words, and 5's "gated only on the decision to publish"
is consistent with "No item gates publication any more".

**PRIVATE.md**: agrees. Lines 10-11 give 178 excerpts and 47 PDFs; line 61 says "Ten knowledge-base
cards cite nine files that live here", which is the card's "NINE targets … cited by TEN cards" and
the nine names `make check` prints.

**`docs/data/extra-claim-map.json`**: `2211` once, X-R2. `the README lists`, `are in the README`,
`does not serve anything yet`, `serves nothing yet`, `deliberately disabled`, `Once the repository is
public these pages`, `No result here has yet been refereed`: **0** occurrences anywhere under
`docs/`. `README[.:]NN` in any form: **0**. No page under `docs/` states a condition on publication
or claims the site is live. Nothing false about the README, the publication steps or the link total
reaches the site **except X-R2**, and I cannot confirm item 5 until it is applied.

## 7. Non-blocking

- **N-B1, still open from REF-FINAL F-1.** "BOTH REMOTES ARE PRIVATE, the companion since 2026-09-20
  and the public one since its recreation on 2026-09-21; **the first** is public-ready but not
  public." The nearest enumeration puts the companion first, and the companion is the one that must
  never be public. Repair, unchanged: `; the project remote is public-ready but not public.`
- **N-B2, new.** "the 97 tracked .out **run captures**, 83 under numerics/ and 14 under rigor/, **96
  of them run captures** and one (rigor/_probe.out) a stray LaTeX bookmark file" — the appositive
  calls all 97 run captures and the next clause corrects it to 96. All three counts are right
  (97 = 83 + 14, and `rigor/_probe.out` is tracked and opens with `\BOOKMARK [1][-]{section.1}`), so
  it is only the noun: `the 97 tracked .out files`.
- **N-B3, still open from REF-FINAL F-4.** "CLEARED on 2026-09-21 by **the second** of the two
  recorded routes" — the enumeration the ordinal counted into was deleted by R-B1 two passes ago.
  Repair on file in `referee_final.md` §F-4.
- **N-B4.** The third Pages step is worded three ways (§2, end). If `next` keeps "with GitHub
  Actions as its source", the workflow comment is the natural place to say it too.
- **N-B5, out of scope, pre-existing, and now two cards.** `readme-and-figures` says README is
  "about 390 lines" with "12 numbered sections"; it is 428 with 13 (REF-README's N-4, still open).
  `public-site-plan` says the README "came out at 430 lines"; it is 428 since `d3ca565`. The latter
  is past tense about what P1 produced, so it is still true as written, but both figures now
  disagree with the file and both ship.
- **N-B6.** `docs-pages-rendering`: "Every link from the interactive site into the generated
  documentation therefore **landed** a reader on a text file" sits oddly three sentences from "Pages
  has never been enabled on this repository", since no reader has ever landed anywhere. The
  "therefore" makes it a consequence of the static-file rule rather than an observation, so nothing
  is false; "would have landed" would say it.
- **N-B7.** The consequence sentence carries three pronouns with three referents — "says nothing
  about **it**; **that** is visible…, and **it** resolves". Correct on every reading I could
  construct, and I would still have split it.

## 8. Re-measured this pass, and exact

Figures neither of the last two passes certified as correct, plus the cheap ones worth re-running.

- `docs-pages-rendering`: README 428 lines; six `github.io` hits at 29, 35, 36, 337, 338, 339;
  section 1 at 40, section 9 307-349; 8 `<a id>` in `docs/status.md`; 65 tracked `docs/*.md` + 66
  tracked `docs/read/*.html` = **131**; 58 `docs/results/*.md` and 59 `docs/read/results/*.html`
  (58 + the generated index); `if: false` at `check.yml:70`; `actions/configure-pages@v5` with no
  `with:`; `has_pages` false and `/pages` 404. The 14-character GFM divergence was not re-derived:
  the only change to any `docs/*.md` since REF-PASS-C measured it is two table cells in
  `docs/status.md` gaining the words "review pending" (`c52a2dc`, `5415b50`), which carry no
  mathematics, so the figure cannot have moved.
- `repo-split-public-private`: 97 tracked `.out` = 83 `numerics/` + 14 `rigor/`, of which **23** are
  named by a card's evidence token (measured over `areas/`, `claims/`, `evidence/`); private repo
  **235** files, **48,392,400 B = 48.39 MB**; 178 excerpts on disk and 178 tracked; 47 `refs/*.pdf`;
  **255** `\shot`/`\shotc` call sites in **19** documents (a raw grep gives 256 in 20 files, the
  twentieth being `\shot` inside `\shotc`'s own definition at `rigor_preamble.tex:48`); **24** python
  scripts with a computed `_ROOT` and exactly **37** non-assignment uses of it (`tools/fix_paths.py`,
  the converter, is the 25th file naming `_ROOT` and is not one of the 24); the four shell scripts
  `numerics/run_hp14.sh`, `run_largezeta.sh`, `run_largezeta2.sh`, `certified/runhp.sh` all read
  `PYTHON`; release `v0.1.0-draft` assets **629,891 B** and **607,822 B**; repo id 1380449076,
  `created_at` 2026-09-21T19:55:13Z, private, unforked, `has_pages` false; `rigor/README_AGENTS.md:36`
  is the section `How to verify` names. `next`'s "five … ten" knowledge-base hash counts are
  explicitly flagged in the field itself as measured and needing re-measurement, and REF-FINAL
  certified 5 and 10 one pass ago; not re-derived here.
- **`./pgit check` executes as `How to verify` says**, exit 0:
  `public : 623 files`, `private: 235 files`, `overlap: 0  (must be 0)`,
  `uncommitted: public 0, private 0`, `shots on disk 178, tracked 178`.
- `kb -p cft_cmi lint` — `0 issue(s), 2 awaiting review`.

## 9. Gates

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
      cards awaiting a referee pass: 2 (docs-pages-rendering, repo-split-public-private)
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

## 10. Verdicts

- **`docs-pages-rendering`: PASS.** R-1 is answered better than it was asked, and the dated figure
  is right today. N-1 and N-3 are both taken, in both places, and the replacement sentence closes
  N-2 as well; the pronoun, the scope of "resolves" and every other reference in the paragraph hold.
  Nothing else in the card moved. Apply X-R2 in the same pass: the number this card's own repair was
  about is still false one card away, and it ships.
- **`repo-split-public-private`: FAIL** on B-1, B-2, B-3 — R-B1, R-B2, R-B3 above. X-R1 itself is
  correct and is not the reason: both sentences are true, the cross-card contradiction is gone, and
  decision D1 and the workflow comment really do hold the three steps. What fails is the clearance
  paragraph's arithmetic, which REF-FINAL wrote out one pass ago and which nobody applied: 68 is 74,
  two published hashes are eight, three tokens are fifteen, 621 paths are 623, and CHECKLIST.md item
  3 tells a reader the fifth recovery route returns a string it does not return. The clearance itself
  I re-verified and it holds: 0 forbidden paths of 623, 0 hidden by the ignore rules, every published
  hash resolving locally, `has_pages` false, both remotes private.
