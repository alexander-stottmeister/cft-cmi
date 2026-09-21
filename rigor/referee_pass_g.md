# REF-PASS-G: seventh pass on repo-split-public-private (2026-09-21)

Scope: the one card REF-PASS-F failed, against `referee_pass_f.md` and, behind it,
`referee_pass_e.md`, `referee_pass_d.md`, `referee_pass_c.md` and `referee_plan_split.md`.

Verdict: **`repo-split-public-private` PASS.**

Everything marked [M] is measured by me at HEAD = `5a93923`; `git ls-remote` puts the remote's `main`
at the same commit. `git status --porcelain` was empty before I started and is empty now. No git
command that writes was run, and the remote was probed by REST only — I did not clone it.
**This note contains no discarded commit SHA, no full blob SHA and no force-push `before` value**;
see §6.

Six passes each found that a repair had introduced a new defect, and three of those were the same
error — a clause spliced in so that a qualifier or a contrast attached to the wrong sentence. F-R1
was written to undo the third instance. **It did not happen a seventh time.** The Statement reads
correctly end to end, the exposure paragraph included, and every figure it does not declare a dated
measurement reproduces exactly except one, which has moved by one because the previous referee's
note was committed. That one is not worth a seventh failure, and it is written out as G-R1 below.

---

## 1. The Statement read as prose, start to finish

I read the field as forty sentences and chased every pronoun, back-reference, contrast and
qualifier to its antecedent. **The paragraph about the exposure now reads correctly end to end.**
Sentence by sentence, for the part that has been broken three times:

* "THEY ARE NEVERTHELESS STILL RECOVERABLE FROM THE REMOTE" — *they* = the five compendia, named two
  sentences earlier and not displaced by anything in between. Correct.
* "the routes are recorded in `rigor/referee_plan_split.md` and `rigor/referee_pass_c.md`" — *the
  routes* = the three of the previous sentence, and both notes do record them [M].
* "a numerator fixed by the rewrite, under a denominator that grows with every run" — the appositive
  attaches to "15 of the head SHAs it serves", which is what it is about. Correct.
* "so the Actions list is not even the widest publisher" — *the Actions list*, not the events
  endpoint, is the subject being demoted, and the comparison is with the sentence's own subject.
  Correct.
* "Two more, found by REF-PASS-D: … ; and the actor's own events timeline carries the same 44" —
  *two more* is discharged by exactly two clauses, and *the same 44* points back to the 44 of the
  previous sentence, which is the same set [M].
* "so seven tracked files carry a usable seed; the list is re-measured at each pass rather than
  remembered, since any new note that quotes a discarded SHA joins it" — *the list* = the seven, *it*
  = the list. Correct, and F-R3 is applied verbatim.
* "so every publisher above hands out that one seed" — *that one seed* = the single discarded SHA the
  clause opens with. This is the sharpest sentence in the paragraph and it survives the sharpest
  test I could build: see §4.2.
* **"The generated site is clean (…), but those seven tracked files are not, so the ORDER matters"** —
  this is the contrast E-R6's insertion cut in half and F-R1 restored. *Those seven tracked files* is
  six sentences after "seven tracked files carry a usable seed" and nothing plural intervenes that
  could capture it; *are not* completes "is clean". The contrast is whole again, and the ORDER clause
  now hangs off it rather than off the feed counts.
* "publishing first would require moving all seven to the private companion" — agrees with the count
  in the same sentence, with `next`, and with `CHECKLIST.md` item 3c. F-D1 is gone from all three.
* "All three feeds grow with ordinary use, so the entry counts here are the measurement of
  2026-09-21 and not fixed figures; what does not move is the 44 pre-rewrite commits they publish and
  the 15 of them that were workflow heads." — E-R6's hedge now sits after the sentences whose figures
  it qualifies, and *they* = the three feeds, which is what publishes the 44 [M]. Correct.

Two attachments elsewhere in the field are loose rather than wrong, and I would have written them
differently; neither is a defect (G-N2, G-R2 below).

## 2. F-R1, F-R3, F-R5, F-R6, and F-R2 / F-R4 in the checklist

| repair | where | applied? | true? |
|---|---|---|---|
| **F-R1** (F-D1 + F-D2, blocking) | Statement | **verbatim**, both halves in the order F wrote them | **yes** — §1, and `those four` now occurs 0 times in the shipped record [M] |
| **F-R2** (blocking) | `CHECKLIST.md` 3c | **verbatim**: "all seven must move to the private companion first" | **yes** |
| **F-R3** (blocking) | Statement, 3c, `next` | all three; the Statement takes F's sentence verbatim, 3c takes "ANY PASS CAN ADD ONE … the notes for the fifth and sixth passes deliberately quote no discarded SHA and added none", `next` takes "any pass can add one, so the list is checked rather than remembered" | **yes** — and this pass is the third note in a row to add none, §6 |
| **F-R4** (non-blocking) | `CHECKLIST.md` 3c | the two-step recipe is in, character for character, plus the "215 of the 619" candidate-set sentence | **yes, it returns the seven** — below; one wording fault left, G-R3 |
| **F-R5** (non-blocking) | Statement | applied with `the KB` expanded to `the knowledge base`, which changes nothing | **yes**, and it is doing its job: 423 → 426 [M] |
| **F-R6** (non-blocking) | Statement | the author took the second option and **dropped the parenthesis** | **yes**; the numerator is now fixed at 15 for the fifth measurement running (C 28, D 29, E 31, F 32, G 33 runs served, 15 discarded heads every time) [M] |

**F-R4's recipe, run exactly as `CHECKLIST.md` 3c now writes it** [M] — copied out of the file, not
retyped, with `OWNER/REPO` filled in and nothing else changed:

```
gh api /repos/OWNER/REPO/activity --paginate -q '.[].before, .[].after' | sort -u \
  | while read -r s; do git cat-file -t "$s" >/dev/null 2>&1 || echo "$s"; done \
  | grep -v '^0*$' > /tmp/discarded
git ls-files | xargs grep -lE "$(cut -c1-7 /tmp/discarded | paste -sd'|' -)"
```

First step: **44** SHAs, the number the comment in the checklist predicts. Second step: **exactly the
seven files**, in this order —

```
rigor/referee_author_disclosure.md
rigor/referee_build_repairs.md
rigor/referee_compendia_move.md
rigor/referee_pass_c.md
rigor/referee_pass_d.md
rigor/referee_plan_split.md
rigor/referee_repo_split.md
```

exit 0, no stderr, and the same seven that 3c enumerates and the Statement counts. The recipe works
as advertised. It also still works after this note is added to the tree (§6).

## 3. `next`, the Statement, `CHECKLIST.md` 3 / 3b / 3c and `PRIVATE.md`

`next` ships verbatim into `docs/data/extra-claim-map.json`, so I read it there as well as on the
card. The two are identical except for the `(held privately)` markers `build_docs.py` inserts after a
private path, and the same is true of the whole Statement: word-diffed, the only differences are six
inserted `(held privately)` markers [M].

| claim | document | verdict |
|---|---|---|
| `next`: "CHECKLIST.md item 3 records it" | item 3 is the residual, "RESIDUAL, AND IT BLOCKS GOING PUBLIC", with both clearance routes and the four publishers | **agree** |
| `next`: "recorded as CHECKLIST.md 3b" | 3b: reachable in the public history and in the tree of the pushed tag, initial import named | **agree**, re-verified [M] |
| `next`: "seven public-tracked files … they must all move" | 3c: heading **seven**, enumeration **seven**, instruction **all seven** | **agree** — F-D1 repaired on every line |
| Statement ↔ `next` | Statement "moving all seven"; `next` "they must all move" | **agree** |
| Statement ↔ 3c ↔ `next` on the measuring rule | "the list is re-measured at each pass" / "ANY PASS CAN ADD ONE" / "any pass can add one" | **agree** |
| `PRIVATE.md` | `:60-63` nine files cited by ten cards, `restore.sh` not a substitute, the other three "not in the table at all"; `:79-81` the residual blocks going public | **consistent**; it says nothing about the seven notes and the card does not claim it does |

The count and the instruction now agree in all four places. The word `four` in this connection
survives nowhere [M].

## 4. The exposure

### 4.1 Unchanged, and re-measured [M]

| card says | measured 2026-09-21 |
|---|---|
| both remotes private, "never been public, is unforked and has no other collaborators" | `visibility PRIVATE`, `isFork false`, `forkCount 0`, collaborators **1**; the private companion likewise private |
| "no ref of the remote reaches them any more" | `git ls-remote --refs` returns exactly two refs, `main` and `v0.1.0-draft`, both post-rewrite |
| Actions run list, 15 discarded heads, "every run before `9aed69a`" | **33** runs served, **15** distinct discarded heads, all of them on runs earlier than the first run at `9aed69a` and **0** on any run from it onward |
| "44 pre-rewrite commits across 55 push events" | `/events`: **55** PushEvents, 57 distinct SHAs once each event's `before` is counted alongside its `head`, **44** of them absent locally. (Heads alone give 43; the 44th is published only as a `before`. The endpoint publishes both fields, so the card's 44 is right, and it is worth knowing that one of the 44 is reachable only through the `before` field) |
| "29 of which were never a workflow head" | 44 − 15 = **29**, and all 15 run heads lie inside the 44 |
| "the activity endpoint serves 60 entries of which one is the force-push" | **62** now (60 `push`, 1 `branch_creation`, 1 `force_push`), the single labelled force-push row unchanged. Declared a dated figure by the card's own next sentence |
| "the actor's own events timeline carries the same 44" | `/users/<owner>/events`: 57 entries for this repository, 55 pushes, **44** absent locally, and **set-identical** to the events endpoint's 44 and to the activity endpoint's 44. "The same 44" is exact in the strong sense |
| "what does not move is the 44 … and the 15 of them that were workflow heads" | **44** and **15**, for the fourth and fifth consecutive measurement respectively |
| "48 commits … four of which no feed lists" | **48** from one seed, all 48 absent locally, each with `commit.message`, `commit.tree.sha`, author and date; **exactly 4** are published by none of the four publishers the card names |
| "one of them byte-identical to the private copy at its full 299,915 bytes" | `GET /git/blobs/<40>` reports `size 299915`; the local private `rigor/cited_results_all.tex` is 299,915 B |
| "The generated site is clean (355 distinct hex tokens under docs/, none resolving to a discarded commit)" | **355** distinct `[0-9a-f]{7,40}` tokens over all 188 tracked files under `docs/`, `docs/data/*.json` included, and **0** of them is a prefix of any of the 48 — exact on both halves |
| tag, initial import, release | one tag at `5ad78cb`, whose tree carries `plan_page/petz_program_plan.html`; `03e2e48` is the initial import; the release carries the two paper PDFs |

**The exposure is unchanged.** Nothing has been cleared, nothing new has been exposed by the
repository's own movement, and the gate in item 3 still stands for the reason it was written.

### 4.2 The one seed, tested rather than read

The Statement's tightest sentence is "a single discarded SHA walks the whole discarded history and
returns 48 commits … so every publisher above hands out that one seed". Both halves need care,
because they are not the same claim, and I checked them separately [M].

I pulled the 48 commits with their parent lists and computed, locally, how far each published SHA
reaches. **Of the 44 published pre-rewrite commits, exactly one walks all 48**; the rest reach
between 5 and 47, median 27. So "a single discarded SHA walks the whole discarded history" is a
claim about one particular SHA, not about any of them — and the second half of the sentence is
exactly the claim that that one is not hard to come by. It is not: that SHA is the force-push
`before` the activity endpoint labels and timestamps, it is a `before` in the events feed and in the
actor's timeline, **and it is also one of the 15 Actions run heads**. All four publishers hand out
that one seed. The sentence is precise, and it is the strongest sentence in the card.

### 4.3 G-N1 — a publisher no note has named, and it is shorter than the route the card records

Asked for, and found. It is not a new endpoint; it is a **field of an endpoint the card already
names**, and it shortens the recovery by a whole step.

Every entry of the Actions run list carries a `head_commit` object, and its keys are
`id`, `tree_id`, `message`, `timestamp`, `author`, `committer`. The card credits the run list with
publishing "the head SHA of every run before `9aed69a`". It also publishes, for each of those runs,
the **root tree SHA** of that commit and its full commit message and author. Measured [M]:

* the 15 discarded run heads carry **10 distinct `tree_id` values that do not resolve locally** —
  ten pre-rewrite root trees, handed out by name;
* `GET /repos/OWNER/REPO/git/trees/<tree_id>?recursive=1` resolves **all ten**, and **all ten**
  list `rigor/cited_R1.tex`, `cited_R2`, `cited_R3`, `cited_R4` and `cited_results_all.tex` with
  their blob SHAs;
* `GET /git/blobs/<that blob>` then returns `size 299915` for `cited_results_all.tex`.

So a reader who never learns a *commit* SHA, and who therefore never triggers the
`commits?sha=` walk the card calls the fourth route, still reaches the compendia in two calls from
the run list alone. This does not contradict anything the card says — the card's claim is that the
material is recoverable by SHA and that the run list publishes the SHAs, and both are true and are
if anything understated. It changes neither the gate nor either clearance route. It belongs in the
record because the card's own framing ("the pre-rewrite *hashes*", "that one *seed*") invites a
reader to think the exposure runs through commits, and one of its five publishers skips them.

Exact wording, for the Statement, replacing

> "this repository's own Actions run list publishes them as the head SHA of every run before 9aed69a, and 15 of the head SHAs it serves are commits the rewrite discarded"

with

> "this repository's own Actions run list publishes them as the head SHA of every run before 9aed69a, and 15 of the head SHAs it serves are commits the rewrite discarded, each with its commit message and its root tree SHA, so ten pre-rewrite trees are published by name and the compendia are two calls away without any commit SHA at all"

and, in `CHECKLIST.md` item 3, after "publish the pre-rewrite head SHAs", inserting

> ", and the run list publishes each of those commits' root tree SHA beside it, which reaches the files without the commit,".

Nothing else I probed publishes a pre-rewrite hash [M]: there is no Pages site and no build list, no
deployments, no artifacts, no Actions caches, no webhooks, no commit comments, no issues or pull
requests, no code-scanning, secret-scanning or Dependabot alerts, and the commit **search** index
(`/search/commits`, which does serve this private repository to its owner) returns 32 commits, **0**
of them discarded — the index follows the live history only.

### 4.4 G-N3 — the seven are seven files of *this* repository, and that is the right scope

For completeness, since the card's sentence is about "public-tracked files": the knowledge base
carries the same seeds in seven files of its own (`CHANGELOG.md`, one events log and the cards
`longo-xu-cmi`, `paper1-status`, `paper2-status`, `readme-and-figures` and this card's own Notes) [M].
They are outside the list, correctly: `../kb` is a third, private repository with its own sync, which
the card says, and none of it reaches the generated site — the 355-token scan of `docs/` finds zero.
Worth one line in the checklist all the same, because the KB is the one companion whose contents
*are* rendered into a public artefact, and the filter that keeps the seeds out of `docs/` is that
Notes are not rendered, not that the seeds are absent.

## 5. Everything else the Statement asserts, re-measured [M]

Each of these is one command unless noted.

| card says | measured |
|---|---|
| 97 tracked `.out`, 83 under `numerics/`, 14 under `rigor/`; `rigor/_probe.out` a stray bookmark file | 97 / 83 / 14; the file begins `\BOOKMARK [1][-]{section.1}` — exact (one wording fault, G-R2) |
| "of which 23 are named by a card's evidence token" | **23**, over the 330 card files of `areas/`, `claims/`, `evidence/`; all 23 tracked publicly, all under `numerics/optimality_all/` — exact |
| private repo "235 files, 48.39 MB", and the ten paths outside `rigor/shots` and `refs` | 235 files, **48,392,316 B = 48.39 MB**; 178 + 47 + the ten enumerated paths = 235, and the ten are exactly the ten — exact |
| overlap 0; `./pgit check` prints each repository's file count | `public : 620 / private: 235 / overlap: 0 / uncommitted: public 0, private 0 / shots on disk 178, tracked 178`, exit 0 |
| "255 call sites in 19 documents" | **256** `\shot`/`\shotc` call forms in **20** tracked `.tex` with comments stripped, less the one inside `\shotc`'s own definition in `rigor_preamble.tex` = **255 in 19** — exact. (The five compendia hold 176 of the 255 and are private-tracked, so this only reproduces over both repositories) |
| "local builds are unchanged (network_corner_calculus 42 pp with images)" and "27 pp / 8 locally" | `network_corner_calculus.pdf` **42 pp**, `quadratic_limit.pdf` **27 pp** with 8 `\shot` call sites — exact |
| "the 24 python scripts … a computed `_ROOT`", "the four shell scripts … honour `$PYTHON`" | 25 tracked `.py` name `_ROOT`, the 25th being the rewriter `tools/fix_paths.py`, so **24**; **0** tracked `.py` still holds a `/Users/alex` literal; the four shell scripts are `numerics/certified/runhp.sh`, `run_hp14.sh`, `run_largezeta.sh`, `run_largezeta2.sh` |
| "NINE targets … cited by TEN cards", under the rule the card states | **9** targets, **10** distinct citing cards, and they are exactly the nine and the ten named — exact; `PRIVATE.md:60` says the same |
| `restore.sh` recovers exactly one of the six under the cited filename | `--list` ends "20 fetchable, 16 need library access"; VWZ, Uhlmann76 (MANUAL, paywalled) and CDIW21 are the only table rows of the six, and AlbertiUhlmann02, BJL and Sion1958 have **0** table rows and are bullets — exact |
| "the review packets the KB writes into rigor/ are tracked by neither" | 24 on disk, **0** tracked publicly, **0** privately — exact |
| licensing, `THIRD-PARTY.md`, `README_AGENTS.md` section | `LICENSE-CODE` MIT, `LICENSE-DOCS` CC BY 4.0, `THIRD-PARTY.md` present, `README_AGENTS.md:36` heads "Two repositories over one work tree (2026-09-20)" |
| "Every evidence pointer resolves …, and none fails" | `kb -p cft_cmi lint` → `0 issue(s)`; all five of this card's evidence tokens and both `related:` targets exist |
| "620 distinct paths were ever added and none is an excerpt or a PDF" | **621** [G-R1]. The load-bearing half is exact: **0** excerpts, **0** `refs/*.pdf`, **0** compendia ever added |
| "423 files, 198.6 MB on 2026-09-21 … rises by one per review" | **426 files, 199.1 MB** — the hedge F-R5 put there is what makes this a record rather than a defect, and +3 is exactly the three review packets written since |

### 5.1 Which figures the card declares dated, and which it declares fixed

Asked for explicitly, because it is what decides whether a moved number is a defect.

**Declared dated, with the mechanism named:** the two repository file counts ("both move with every
commit, so neither of those two counts is fixed here"); the untracked total ("423 files, 198.6 MB on
2026-09-21 … this count rises by one per review"); every feed entry count ("the entry counts here are
the measurement of 2026-09-21 and not fixed figures"), which covers the 55 push events and the 60
activity entries; the seven-file list ("re-measured at each pass rather than remembered"); and the
Actions denominator ("a denominator that grows with every run"). Every one of these has moved, and
every one has moved in the direction and by the mechanism the card predicts.

**Declared fixed:** the 44 pre-rewrite commits and the 15 workflow heads among them. Both exact [M].

**Asserted without a hedge, and exact:** 97 / 83 / 14 / 23; 235 files and 48.39 MB; overlap 0; 255
call sites in 19 documents; 42 pp and 27 pp / 8; 178 and 47; 24 python scripts and four shell
scripts; 9 targets and 10 cards; 48 commits and 4 unlisted; 355 hex tokens under `docs/`; 299,915
bytes; one tag, one force-push row, one collaborator.

**Asserted without a hedge, and now off by one:** the 620. That is the whole of G-R1, and it moved
because the sixth pass's note was committed — the same mechanism the card hedges twice elsewhere and
did not hedge here.

## 6. Does committing this note change the seven?

**No** [M], and I checked it rather than asserting it, the way F-D3 says the claim has to be checked.

This file quotes no discarded commit SHA, no full blob SHA and no force-push `before` value. Its only
hex tokens are `5a93923`, `0e9f168`, `9aed69a`, `5ad78cb`, `03e2e48` and the two arXiv fragments
`0202038` and `0204029`; each of the five commit SHAs resolves locally and is absent from the 48 [M]. Where a SHA was needed to make a point — the seed
that walks all 48, the ten pre-rewrite trees, the compendium blob — it is described by its role and
derived at run time, never written down.

With this note added to the work tree, the checklist's two-step recipe returns **the same seven
files**; this one is not an eighth. That is now three consecutive notes that added none, which is the
whole of what F-R3 replaced "every referee pass adds one" with.

## 7. The gates, run by me

`make check` — **exit 0** on a clean tree at HEAD [M]:

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
  cards awaiting a referee pass: 1 (repo-split-public-private)
  cards whose last referee pass failed: 0
ok       docs/data/quadratic-law.json … constants.json, theta.json, universality.json,
         networks.json, extra-separation.json, extra-off-criticality.json,
         extra-relative-entropy.json, extra-claim-map.json   (nine files)
  page record references: all resolve
```

`make rigor` (`python3 tools/check_rigor_builds.py`) — **exit 0**, every document `ok`, closing with
`46 document(s), 0 failing, 0 known`.

`kb -p cft_cmi lint` — `0 issue(s), 1 awaiting review`, the card under review here.

Fifth consecutive pass with both gates green at HEAD. `git status --porcelain` is empty after all
three; the only file I add to the work tree is this one (`rigor/review_packet_g.md` was written by
the knowledge base, and is tracked by neither repository).

I ran `make check` again **after** recording the verdict, as at the last four passes. It is **exit 2**,
and the whole drift is the review state the verdict just moved [M]: `differs status.md` and
`differs read/status.html`, with `cards awaiting a referee pass` going 1 to 0. `check_links` still
prints `155 pages, 2211 links resolve` and `make rigor` is unchanged at exit 0. That is rule (c)
working, not a regression; run `make docs data` and commit.

## 8. Repairs — none blocking

**G-R1 (the one figure now false, non-blocking).** In the Statement, replace

> "620 distinct paths were ever added and none is an excerpt or a PDF"

with

> "621 distinct paths had ever been added on 2026-09-21 and none is an excerpt or a PDF; that count rises with every commit that adds a file, the load-bearing half does not"

It was 620 when the sixth pass measured it and 621 by the time the card was edited, because the same
commit added `rigor/referee_pass_f.md`. It will be 622 when this note is committed. It is the twin of
the untracked total three sentences earlier, which F-R5 hedged; this one was left bare.

**G-R2 (wording).** The Statement opens the inventory with "the 97 tracked .out run captures … 96 of
them run captures and one (`rigor/_probe.out`) a stray LaTeX bookmark file", which calls all 97 run
captures and then says 96 are. E-R9 fixed the second half and left the first. Replace

> "the 97 tracked .out run captures, 83 under numerics/ and 14 under rigor/, 96 of them run captures"

with

> "the 97 tracked .out files, 83 under numerics/ and 14 under rigor/, 96 of them run captures"

**G-R3 (wording, `CHECKLIST.md` 3c).** F-R4 landed, but it was inserted after the recipe it replaces
instead of over it, so the item now states the broken method as the method and then refutes it:
"The list is not remembered, it is measured: `git ls-files | xargs grep -lE …`, filtered to the SHAs
that `GET /repos/OWNER/REPO/activity` reports and `git cat-file -t` does not resolve locally.
`grep -l` throws the tokens away, so take the SHAs first:". Replace those two sentences with

> "The list is not remembered, it is measured — but `grep -l` prints filenames and throws the tokens away, so the SHAs have to come first:"

and leave the two-step block and the candidate-set sentence exactly as they are.

**G-R4 (dating, `CHECKLIST.md` 3c).** "it returns 215 of the 619 tracked files" was exact when written
and is **216 of 620** today [M], for the same reason as G-R1. Replace with

> "it returned 216 of the 620 tracked files on 2026-09-21, both figures rising with the tree".

**G-R5 (wording, `CHECKLIST.md` 3c and `next`).** Both say "five of them referee notes that give the
recovery route in full", which reads distributively and is not true of all five: `referee_plan_split`,
`referee_pass_c`, `referee_pass_d` and `referee_compendia_move` each give route material, while
`rigor/referee_repo_split.md` carries only an `ls-remote` line with a discarded head in it [M]. The
Statement already has the accurate form — "between them give the commit and blob SHAs, a one-line git
show recipe and all three REST calls". In 3c and in `next`, replace "five of them referee notes that
give the recovery route in full" with

> "five of them referee notes that between them give the recovery route in full"

**G-N1** is written out in §4.3 and **G-N3** in §4.4. **G-N2 (wording):** "three independent routes
each returned the files, one of them byte-identical to the private copy at its full 299,915 bytes" —
*one of them* is meant to be one of the files, and can be read as one of the routes; and it
understates what `referee_plan_split.md` records, which is that all five came back byte-identical.
"…each returned the files, the largest of them byte-identical to the private copy at its full 299,915
bytes" would fix both.

---

## 9. Why this is a PASS

Nothing in the card is false, missing, or contradicted by its own evidence documents, with the single
exception of a path count that moved by one when the previous referee's note was committed, and that
is written out above with its replacement. The three repairs that blocked at the sixth pass are
applied verbatim and are true; the two that landed in the checklist are applied and its recipe
reproduces its own list; the `next` field, the Statement, items 3, 3b and 3c and `PRIVATE.md` agree
on the count and on the instruction, in the shipped record as well as on the card; the exposure is
unchanged and every figure the card declares fixed about it is exact; both gates are green.

The one substantive thing this pass adds is G-N1, and it makes the finding the card exists to record
*stronger*, not weaker. That finding — that a history rewrite bought unreachability and not deletion,
and that the repository publishes its own seeds — was found by this review chain, is correct, and is
now correct in a seventh independent measurement.

Seven passes, and the sentence that says what to do before publishing finally says the same thing in
all four places it appears.
