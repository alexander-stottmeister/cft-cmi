# REF-README: docs-pages-rendering after the README edit of 2026-09-22 (2026-09-22)

Tenth pass on `docs-pages-rendering`, scoped to the paragraph the author rewrote when
`README.md` changed at `d3ca565` (2026-09-22 07:57:37 +0200) and to its immediate neighbours.
Everything below was counted or executed, not read off the previous pass.

**Verdict: FAIL**, on one thing, and it is the failure mode this chain has been warned about for
ten passes: the edit is correct in itself and it silently falsified a neighbouring field. The
rewritten paragraph is true on every clause I could test. `How to verify` is not, and it is the same
single number that failed at REF-CI-PAGES-B (B6) and again at REF-PASS-C (C-R1).

---

## 1. What the edit to README.md actually did

`git show d3ca565 -- README.md`: 8 insertions, 10 deletions, one file, nothing else in the commit.
Three hunks.

1. The banner (lines 6-9 → 6-11). `\`conjectural\` means neither. No result here has yet been
   refereed by a human other than me.` became `\`conjectural\` means neither. **Human verification
   is ongoing and is not finished.** Nothing here has yet been checked by a human other than me, so
   every status on this page records what the AI review pipeline concluded and not what a human
   referee confirmed. Read the whole repository as work under review.`
2. The introduction. Deleted in full: `**That address does not serve anything yet.** The site is
   built and committed, but the repository is private and the Pages deploy job in
   [\`.github/workflows/check.yml\`](.github/workflows/check.yml) is deliberately disabled.
   Publishing needs three things: the repository going public, because the free tier serves Pages
   for public repositories only; the \`if: false\` on that job being removed; and Pages enabled once
   on the repository, which the workflow cannot do for itself. Until then the same content is in
   [\`docs/\`](docs/), and GitHub renders the Markdown when you browse it here.` Replaced by one
   sentence that keeps only the `docs/` half.
3. Section 9: `Once the repository is public these pages are served` → `Those pages are served`.

README is 428 lines, having been 430.

## 2. The rewritten paragraph, clause by clause

> README carries the Pages address six times, three in the introduction (lines 29, 35, 36; section 1
> begins at 40) and three in section 9 (337, 338, 339; the section runs 307 to 349).

`grep -n github.io README.md` → **29, 35, 36, 337, 338, 339**. Six, exact. `grep -n '^## ' README.md`
→ `## 1.` at **40**, `## 9.` at **307**, `## 10.` at **350**, so section 9 is **307-349**. All three
intro hits are below 40; all three section-9 hits are inside 307-349. **Every number holds.**

> It no longer explains what publication requires: that paragraph was written for a private
> repository and was removed on 2026-09-22 at the author's instruction, because a published README
> does not need it.

The paragraph quoted in §1.2 above is the one, and it is gone. Nothing replaced it: a case-insensitive
grep of README.md for `public|private|publish|live|serve|404|not yet|enabled|Pages` returns eleven
hits, and not one of them states a condition on publication — they are the private knowledge base
(342), third-party redistribution (385, 403, 412), the `\shot` placeholder (364, 406), the rigor
build count (417) and unrelated prose. The date matches the commit to the minute. **Holds.**

The card makes no claim about the banner text; its only claim that touches the banner is "with no
caveat", checked next. For the record, the banner now does say human verification is ongoing and
unfinished, which is a caveat about *status*, not about the address.

## 3. The consequence sentence — the four clauses

> The consequence while the repository stays private is that the README points at an address that
> does not serve, with no caveat, which is visible to nobody but the author and resolves itself on
> publication.

- **"points at an address that does not serve"** — `curl -s -o /dev/null -w '%{http_code}'` gives
  **404** for both `https://alexander-stottmeister.github.io/cft-cmi/` and
  `.../cft-cmi/read/status.html`. `gh api repos/alexander-stottmeister/cft-cmi/pages` → 404 Not
  Found. `has_pages` is **false**. **True.**
- **"with no caveat"** — the only caveat there ever was is the deleted `**That address does not
  serve anything yet.**`, and the grep above finds no replacement anywhere in the 428 lines. The
  two surviving statements are both bare present tense: `The same address serves the generated
  documentation as pages you can read in a browser` (33) and `Those pages are served at …` (336-337).
  **True.**
- **"visible to nobody but the author"** — `gh api repos/alexander-stottmeister/cft-cmi` →
  `private: true`, `visibility: private`, `fork: false`, `archived: false`; `/collaborators` returns
  exactly one login, `alexander-stottmeister`. The only release, `v0.1.0-draft`, is a release of the
  same private repository. **True.**
- **"resolves itself on publication"** — true under the definition the very next sentence supplies,
  where publication is the three-step act and not just the visibility flip. See N-2 for the reading
  it invites on a first pass.

## 4. "recorded in decision D1, in the workflow comment and on ci-green"

All three say it, and they agree with each other and with the card's three-item list.

- **D1**, `rigor/public_site_plan.md:226-228`: "**Pages goes live only when the repository goes
  public.** … the Pages deployment step of P5 is written but left disabled, and enabling it is one
  line plus one click once `CHECKLIST.md` is clear." Public + one line + one click = the same three.
- **The workflow comment**, `.github/workflows/check.yml:62-68`: "Publishing needs THREE things, as
  decision D1 says (rigor/public_site_plan.md): the repository going public, because the free tier
  serves Pages for public repositories only; this `if: false` removed; and Pages enabled once on the
  repository." Word for word the card's list, in the card's order. `if: false` is still at line 70.
- **`ci-green`**, Statement: "Going public enables nothing by itself: publishing needs three things,
  the repository public, that line removed, and Pages enabled once on the repository, which is what
  rigor/public_site_plan.md:226 means by 'one line plus one click'."

"is unchanged" also holds: `d3ca565` touched `README.md` only, so neither the workflow nor the plan
document moved. `actions/configure-pages@v5` is still declared with no `with:` block, so "is not set"
is still true.

## 5. The rest of the card

`git diff HEAD` on `kb/projects/cft_cmi/claims/docs-pages-rendering.md` is **one hunk, three changed
lines**: `review: passed 2026-09-21 by REF-CLEARED` → `review: pending`, `updated: 2026-09-21` →
`2026-09-22`, and the Statement. A word-level diff of the Statement shows **one** changed region,
the paragraph above; every other word of 2,400 is identical. `next` and `How to verify` were not
touched. `grep -c '<a id=' docs/status.md` = **8**, matching `next`. Nothing else in the card needed
re-checking and nothing else moved.

## 6. What reaches the public site

The docs were regenerated for the edit at `c52a2dc` (`docs/data/extra-claim-map.json`,
`docs/read/status.html`, `docs/status.md`), and `build_docs --check` reports 131 pages up to date, so
the shipped claim map carries the **new** paragraph, verbatim and complete.

- The removed README phrases — `does not serve anything yet`, `serves nothing yet`, `deliberately
  disabled`, `Once the repository is public these pages`, `No result here has yet been refereed` —
  occur **0 times** anywhere under `docs/`.
- Stale README line numbers — `27, 33, 34`, `339, 340, 341`, `README:NN` in any form — occur **0
  times** in `docs/data/extra-claim-map.json`. A `grep -o 'README[.:a-z]*:[0-9]\{1,4\}'` over the
  whole file returns nothing at all.

One false number does ship, and it is F-1.

---

## F-1 — BLOCKING. `How to verify` says 2211 links; `make check` prints 2210, because of this very edit

`How to verify`, first sentence: "After make docs data, make check is green: check_links 155 pages
and **2211** links resolve, build_docs --check 131 pages up to date, all nine data files ok."

`make check` at HEAD prints, verbatim:

    155 pages, 2210 links resolve

155 is right, 131 is right, nine data files is right (quadratic-law, constants, theta, universality,
networks, extra-separation, extra-off-criticality, extra-relative-entropy, extra-claim-map). The link
count is one too high, and the cause is the README edit: the deleted paragraph carried the README's
only link to `.github/workflows/check.yml`, and its `[\`docs/\`](docs/)` was re-used in the
replacement sentence, so the net change is exactly −1. Counting relative links the way
`tools/check_links.py` counts them (`MD_LINK`, resolve, tracked-or-directory) gives **81** in
`git show d3ca565^:README.md` and **80** in `README.md` at HEAD. 2211 − 1 = 2210. REF-CLEARED
measured 2211 on 2026-09-21 and was right; the number went stale at 07:57 the next morning.

This is the third pass on one integer: REF-CI-PAGES-B raised it as B6 (card said 2210, tool said
2211), REF-PASS-C failed it as C-R1 ("Second pass in a row"), REF-PASS-D and REF-CLEARED cleared it,
and it is now wrong again in the other direction.

It also ships. `docs/data/extra-claim-map.json:1559` is the `verify` field of this card, carrying
`check_links 155 pages and 2211 links resolve`, and module 10 renders that field. A reader running
the one instruction the card gives gets a different number from the one the card promises.

**Repair R-1, verbatim.** In `How to verify`, replace

    check_links 155 pages and 2211 links resolve

with

    check_links 155 pages and 2210 links resolve

then `make docs data` so `docs/data/extra-claim-map.json` carries the corrected field, and re-run
`make check` to confirm it still prints 2210 after the regeneration.

---

## X-1 — NOT this card, but live, shipped, and created by the same edit: `repo-split-public-private`

`repo-split-public-private`'s `next` field now says two things about the README that stopped being
true at `d3ca565`, and both are in `docs/data/extra-claim-map.json`:

> Publishing now needs only the three Pages steps **the README lists**: the repository going public,
> the if: false removed from the Pages job, and Pages enabled once with GitHub Actions as its source.

> CHECKLIST.md items 3 to 3e record the clearance; the three Pages steps **are in the README** and in
> the workflow comment.

The README lists nothing of the kind any more. This is the direct complement of the sentence
`docs-pages-rendering` now carries ("It no longer explains what publication requires"), so the
knowledge base currently asserts both. `docs-pages-rendering` is the one that is right, which is why
this is recorded here and not in its verdict, but the sibling has to move in the same pass or the
public claim map ships a contradiction.

**Repair X-R1, verbatim.** In `repo-split-public-private`'s `next`, replace

    Publishing now needs only the three Pages steps the README lists: the repository going public, the if: false removed from the Pages job, and Pages enabled once with GitHub Actions as its source.

with

    Publishing now needs only the three Pages steps of decision D1: the repository going public, the if: false removed from the Pages job, and Pages enabled once with GitHub Actions as its source.

and replace

    CHECKLIST.md items 3 to 3e record the clearance; the three Pages steps are in the README and in the workflow comment.

with

    CHECKLIST.md items 3 to 3e record the clearance; the three Pages steps are in decision D1 and in the workflow comment, and were dropped from the README on 2026-09-22 because a published README does not need them.

---

## Non-blocking

**N-1, the relative pronoun.** "…points at an address that does not serve, with no caveat, **which**
is visible to nobody but the author…" — the nearest antecedents are "no caveat" and "an address that
does not serve", and neither is what is meant: an address is visible to anyone who types it; the
thing only the author can see is the uncaveated README. It reads correctly on the second pass and
wrongly on the first. If the sentence is touched again:

    The consequence while the repository stays private is that the README points at an address that
    does not serve and says nothing about it; that is visible to nobody but the author, and it
    resolves on publication.

**N-2, the scope of "while the repository stays private".** Being private is sufficient for the dead
address, not necessary: the address also fails in the window between the repository going public and
the other two steps landing. The paragraph is coherent because the next sentence defines publication
as all three steps, but "resolves itself on publication" invites the reading "resolves itself when
the repository goes public", which is the exact error REF-CI-PAGES failed this card for as DEFECT 3(b)
and REF-CI-PAGES-B failed `ci-green` for as B1. Nothing to repair; worth not losing next time the
sentence is edited.

**N-3, "at the author's instruction".** The same sentence pair uses "the author" for the repository
owner ("visible to nobody but the author"), so the usage is internally consistent and I read it as
true. In knowledge-base usage "the author" is also the agent that writes the card, and that reading
would make it false. "at the user's instruction" would remove the ambiguity at no cost.

**N-4, out of scope, pre-existing.** `readme-and-figures` describes README.md as "about 390 lines"
with "12 numbered sections"; it is 428 lines with 13. Both were already wrong before `d3ca565` (which
moved the count by −2), the line figure is hedged with "it grows as results are added", and neither
belongs to this card. Recorded so the next pass on that card does not have to find it again.

**N-5, closed.** D-R1 (= C-R7, = B-R8), on its fifth pass through these reports, is **done**: the
module docstring of `tools/md_to_html.py` now reads "served verbatim, with or without
`docs/.nojekyll`", "the directory prefix … is preserved and only the suffix changes" and "The subset
is NOT closed, and saying otherwise cost three referee passes", and the comment above
`UNSUPPORTED_LINE` no longer claims closure. It agrees with the Statement on all three.

## Gates

- `make check` — **exit 0**. `155 pages, 2210 links resolve`; external hosts
  `alexander-stottmeister.github.io, github.com, projecteuclid.org`; `build_docs --check: 131 pages
  up to date`; `claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, 5 verified, 5 open,
  14 active, 5 done, 2 superseded, 1 refuted)`; `pages under results/: 58`; 9 privately held evidence
  pointers rendered without a link; `cards never refereed: 0 of the 90 listed`; `cards awaiting a
  referee pass: 1 (docs-pages-rendering)`; `cards whose last referee pass failed: 0`; nine `ok` lines
  for the nine data files.
- `make rigor` — **exit 0**. `46 document(s), 0 failing, 0 known`.

## Verdict

`docs-pages-rendering`: **FAIL** on F-1 only. The rewritten paragraph is accurate on all six address
positions, both section boundaries, the removal, the banner, and every one of the four clauses of the
consequence; the three sources for what publication requires all say it and agree. The edit did not
break a sentence inside the Statement — it broke `How to verify`, by removing a link the count
depended on. Apply R-1, regenerate, and X-R1 with it.
