# REF-FINAL: ci-green, public-site-plan, repo-split-public-private (2026-09-21)

Ninth pass. Scope as set by the brief: REF-CLEARED's clearance is taken as established and
spot-checked, not re-derived; the effort goes into the prose, into whether each of
REF-CLEARED's repairs is applied *and true*, into the fields that reach the public site,
into the `How to verify` lines as instructions, and into every figure REF-CLEARED did not
already certify.

No hash and no Actions run id is quoted below. Every identifier in this repository has been
invalidated twice already; naming one here would only add a fifteenth dead token to the
tracked tree. Commits are named by message and time, runs by position.

**VERDICT: all three PASS.** Nothing in the three Statements is false, missing or
contradicted by its own evidence. Nine items of wording remain, all non-blocking, all with
exact repair text in §5; the first of them (F-1) is the ninth instance of the recurring
failure mode and was introduced by REF-CLEARED's own N-B6.

---

## 1. The clearance, spot-checked

Three routes plus the identity of the store, re-run live:

| check | result |
|---|---|
| `repos/<r>` id and `created_at` | unchanged from what the Statement records: a different object store, created 2026-09-21T19:55:13Z, `private`, `fork` false, `forks_count` 0, `has_pages` false |
| `/commits/<full sha>` at a discarded commit | **422 "No commit found for SHA"** |
| `/git/blobs/<full sha>` at the compendium blob | **404 Not Found** |
| `/contents/rigor/cited_results_all.tex?ref=<discarded>` | **404 "No commit found for the ref"** |
| `/git/trees/<reconstructed old plan_page subtree>` | **404 Not Found** |
| `/activity` | 3 entries, all `push`/`branch_creation`, **zero force_push**, every `before`/`after` resolving locally |
| `/actions/runs` | 3 runs, all success, every `head_sha` and `head_commit.tree_id` resolving locally |
| `./pgit check` | public 622 / private 235 / overlap 0 / shots 178 = 178, exit 0 |

The clearance holds. The private companion still tracks exactly the ten paths outside
`rigor/shots` and `refs` that the Statement enumerates, 47 `refs/*.pdf` and 178 excerpts:
178 + 47 + 10 = 235, to the file.

---

## 2. REF-CLEARED's repairs: applied, and true

| repair | applied | true |
|---|---|---|
| **R-B1** replacement paragraph | **yes, verbatim** — S19–S24 are gone; the three replacement sentences are S21–S23 | yes; `grep` on the shipped claim map: `MUST NOT BE MADE PUBLIC` **0**, `One designated-private path is still recoverable` **0**, `Deletion requires one of two routes` **0**, `What bounds the exposure` **0**, `44 pre-rewrite commits` **0** |
| **R-B2** five-and-ten | **yes**, in `next` and identically in CHECKLIST 3d | **re-measured, exact.** Strict rule (the discarded commit prefixes, `git ls-files \| xargs grep -l` over the knowledge base) hits **exactly five** files: `claims/longo-xu-cmi.md`, `claims/paper2-status.md`, `claims/readme-and-figures.md`, `claims/repo-split-public-private.md`, `events-Alexanders-MacBook-Pro-8.jsonl`. Widening to every cft-cmi hash the recreation invalidated adds `ci-green.md`, `docs-pages-rendering.md`, `generated-docs.md`, `paper1-status.md`, `public-site-plan.md` = **ten**. I checked the residue by hand: every other hex-looking token under `projects/cft_cmi` is scientific notation or a claude.ai artifact UUID, not a git hash |
| **R-B3** five routes, three hashes | **yes, verbatim** (S16) | the substance is true and now understated; see **F-2** |
| **R-B4** release sentence | **yes, verbatim** (S17–S19) | yes. S17's "byte-identical to the local builds" (assets vs the files they were uploaded from) and S18's "differs in 66 bytes" (a fresh rebuild vs those files) are different comparisons and do not collide; S19 says exactly which of the two the record cannot supply |
| **R-C1** three run-ID replacements | **yes, all three** — S08 "the last failing run (28 packages) and the first passing one (31 …)", S11 "The first success came on the repair commit:", S15 "the next run was green over it" | yes. `grep -oE '\b3[0-9]{10}\b' docs/data/extra-claim-map.json` returns **nothing**, and the only hex tokens in that file are three scientific-notation numbers and one artifact UUID — **no commit hash at all** reaches the site |
| **R-C2** destroyed-evidence sentence | **yes, verbatim** (S17 of `ci-green`) | yes, and it ships (`destroyed on 2026-09-21 when the remote was deleted` = 1 in the claim map) |
| **R-C3** rewritten How-to-verify | **yes, verbatim** | **executed; see §3** |
| **R-P1** CI sentence | **yes, verbatim** (S11) | yes. The sentence now says one commit carrying two repairs, which is what happened; "that day" binds correctly to the 11:07 repair named earlier in the same sentence |
| **R-P2** budget figures | **yes, verbatim** (S13) | yes when written, and declared dated. Re-measured: `du -sk docs/{assets,lib,data}` = 1336 KB = **1.30** (unchanged); the public tree is **8.25 MB** over 622 files against the card's dated 8.21. The budget — the fixed figure — holds with room to spare |
| **N-B5** drop the 620 | **yes** — S08 carries no path count | — |
| **N-B6** both-remotes dating | **yes** | the new clause is true, **but it broke the back-reference that follows it: F-1** |
| **N-B7** CHECKLIST over-reach | **yes, verbatim** | yes: CHECKLIST 3–3e record the clearance, and the three Pages steps are in the README and in the workflow comment above `if: false`, not in CHECKLIST |
| **N-B8** "the largest of them" | **yes** (S10) | yes |
| **N-B10** (not in the brief's list) | **not applied** — `.github/workflows/check.yml:47` still names a dead hash in a comment | REF-CLEARED marked it non-blocking and CHECKLIST 3e covers it generically. Restated as **F-9** |

---

## 3. The three `How to verify` lines, executed as written

**`repo-split-public-private`** — "`./pgit check` (expects overlap 0 and equal shots counts);
git log in both repos; `rigor/README_AGENTS.md` section 'Two repositories over one work
tree'." Run: `./pgit check` prints `overlap: 0  (must be 0)` and `shots on disk 178, tracked
178`, exit 0; `git log` works in both; the named section is `README_AGENTS.md:36`. **Does
what it says.**

**`ci-green`** — run in full. `gh run list` prints three runs, all successes, exactly as the
line predicts ("shows the current runs" — it no longer promises a failure sequence).
`gh run view <latest> --log` prints `41 document(s), 0 failing, 0 known` and
`NOT CHECKED, no knowledge base at …: docs/data/extra-claim-map.json`, both verbatim as
claimed. Locally: `make rigor` dispatches to the checker (46 documents) instead of printing
"up to date"; `grep -c allow-missing-kb tools/build_site_data_extra.py` is **1**; the pages
job carries `if: false` at `check.yml:68`. **Does what it says, on every clause.** This is
the field R-C3 replaced, and the replacement is the first version of it in three passes that
a reader can actually run.

**`public-site-plan`** — the plan file is 237 lines; all five named build cards exist
(`readme-and-figures`, `generated-docs`, `interactive-site`,
`interactive-site-modules-3-4-5`, `interactive-site-modules-7-10`); "P5 is partly done
(Makefile and workflow exist, Pages deployment is written and disabled under D1)" is exactly
right — `deploy-pages` is written in the workflow and the job is disabled. **Does what it
says.**

---

## 4. Figures re-measured that REF-CLEARED did not certify

All correct unless marked.

- `repo-split`: 97 tracked `.out`, 83 under `numerics/`, 14 under `rigor/` (83 + 14 = 97);
  the ten enumerated private paths outside `shots` and `refs` are **exactly** what
  `ls-files` lists there; 47 `refs/*.pdf`; 178 excerpts; private total 48.39 MB.
- `repo-split` S27, **nine private targets cited by ten cards** — measured over `areas/`,
  `claims/` and `evidence/`, excluding the generated files: **9 distinct targets, 10
  distinct citing cards**, 36 occurrences. PRIVATE.md's closing paragraph says the same
  ("Ten knowledge-base cards cite nine files that live here"). The REF-INFRA-2 error that
  PRIVATE.md once repeated is gone.
- `repo-split` S28–S29, **restore.sh recovers exactly one of the six under the cited
  filename** — executed. `getref.sh` writes `<short>_<id>.pdf`, so the VWZ row reproduces
  the cited filename exactly; the CDIT row is tabled as `CDIW21` and would write a different
  name; `Uhlmann76` and `Alberti83` come back `MANUAL … paywalled`; and
  `AlbertiUhlmann02`, `BJL_twisted_duality` and `Sion1958_minimax` are bullets at
  `refs/REFERENCES.md:49–51`, not table rows. Every clause of both sentences is true.
- `repo-split` S13/S20, **seven public-tracked files gave the route** — reproduces: before
  the two referee reports of this evening were committed, exactly seven tracked files
  carried a discarded commit prefix. CHECKLIST 3c says the same. The historical claim is
  fixed and correct; the *current* count is nine and rises with every referee report, which
  is why S13/S20 are properly in the past tense.
- `repo-split` S03, tracked by neither: **428 files, 199.6 MB** against a dated 423 / 198.6.
  Drift, and the sentence hedges the mechanism. Not a defect (N-B9 said so; it still holds).
- `ci-green`: `extra-claim-map.json` is indeed the **fourth** payload of
  `build_site_data_extra.py` and the other three are built from result files in this
  repository; `paper1/main.tex` loads `lmodern` on **line 2**; `rigor` is in `.PHONY` at
  `Makefile:8`; README §13 says "All 41 rigor documents", matching the run log, and
  `make rigor` locally says 46 = 41 + the five private compendia; `actions/checkout@v4` and
  `actions/setup-python@v5` are what the workflow uses, so `next` is accurate.
- `public-site-plan`: plan **237** lines; README **430**; **30 proved + 3 refereed = 33**;
  the plan's module table names **11** numerical-status claim cards plus the finding
  `circle-model-taper-suppresses-theta` = **12 headline numericals**, so **33 + 12 = 45**
  claims — the Statement's arithmetic and its parenthetical explanation of the 11→12 move
  are both exact; **89** claim cards and `docs/status.md` says "90 cards: 89 claim cards …
  plus 1 finding"; **5** SVGs in `docs/assets/`, **4** tracked PNGs, 3 + 5 = **8** figure
  slots; **10** module pages; `.nojekyll` present; `rigor/public_site_plan.md:224` is
  `## 6. Decisions — taken 2026-09-21 by the user` and the plan carries **D1–D4 only**,
  matching "Four decisions"; the plan's module-9 row (line 110) still shows the bracket
  unconditionally, so `next`'s "repair the plan's module-9 bracket wording" is still
  genuinely owed.

**Gates.** `make check` **exit 0** — 155 pages / 2211 links resolve; `build_docs --check:
131 pages up to date`; claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural,
5 verified, 5 open, 14 active, 5 done, 2 superseded, 1 refuted); 58 result pages; 9 private
evidence pointers rendered without a link; `cards never refereed: 0 of the 90 listed`;
`cards whose last referee pass failed: 0`; all nine data files `ok`, `extra-claim-map.json`
included. `make rigor` **exit 0** — `46 document(s), 0 failing, 0 known`. `kb lint` —
`0 issue(s), 3 awaiting review`.

---

## 5. The nine remaining items, with exact wording

None of these is a FAIL. F-1 and F-2 are the ones worth doing.

### F-1 — `repo-split`, S02: N-B6's repair broke the back-reference in its own sentence

This is the ninth consecutive pass at which a repair damages the sentence next to it, and
this time the repair was mine to inherit. S02 now reads:

> BOTH REMOTES ARE PRIVATE, the companion since 2026-09-20 and the public one since its
> recreation on 2026-09-21; **the first** is public-ready but not public.

Before N-B6 the sentence was "BOTH REMOTES ARE PRIVATE as of 2026-09-20; the first is
public-ready but not public", and "the first" counted into S01, where the publishable
`.git` is named first and `.git-private` second. N-B6 inserted a two-item list in between —
and it puts **the companion first**. English binds an ordinal to the nearest enumeration, so
"the first" now points at the private companion, the repository that holds 178 third-party
page excerpts and 47 source PDFs and must never be published. Read that way the clause is
false. It ships: the Statement is carried verbatim in `docs/data/extra-claim-map.json`.

I have not failed the card for it, because the reading that makes it false is the nearest-
antecedent reading and not the only one, and because the card says at length and in several
other places that the companion is exactly what must not be published, so no reader ends up
misinformed. It is still one word in the wrong place, in the sentence that tells a reader
which of the two repositories is ready to go public.

**Repair F-1.** Replace

`; the first is public-ready but not public.`

with

`; the project remote is public-ready but not public.`

### F-2 — `repo-split`, S16 and S21: four counts the repair commit itself invalidated

R-B1 and R-B3 were written against a tree that the act of applying them changed. Committing
the referee report moved every one of these:

| clause | said | is |
|---|---|---|
| S16 "all three full 40-character tokens the tracked notes carry" | 3 | **15** tokens in the tracked tree |
| S16 "the four feeds publish two hashes between them" | 2 | **3** |
| S16 "621 distinct paths were ever added" | 621 | **622** |
| S21 "holds only the 68 commits of this history" | 68 | **69**, locally and on the remote |

Nothing is at risk. I resolved all fifteen tokens: five are objects of the current history
(two commits, the tag, two published trees), one is the private companion's head, and the
remaining nine are precisely the ones REF-CLEARED tested and found 404 — the two discarded
commits, the six private blob SHAs and the reconstructed old subtree. The three published
hashes all resolve locally. None of the 622 paths is an excerpt, a PDF, a compendium or the
plan page. So the substance is *stronger* than the sentence, and the sentence is a record of
a verification performed at a stated moment ("Verified afterwards"), which the brief treats
as dated.

But S16 is the sentence the whole clearance rests on and S21 is the sentence that says the
objects are gone, and both now carry a number that is one commit out of date and will be two
after the next referee report. The fix is to stop counting things that grow.

**Repair F-2a.** In S16 replace

`for all three full 40-character tokens the tracked notes carry, the two commits and the compendium blob`

with

`for every full 40-character token the tracked notes carry: the two discarded commits, the compendium blob, and the five further private blob names and one reconstructed subtree that the eighth pass added to the test`

**Repair F-2b.** In S16 replace

`the four feeds publish two hashes between them and both resolve in the local history; 621 distinct paths were ever added and none is an excerpt, a source PDF, a compendium or the plan page`

with

`every hash the four feeds publish resolves in the local history; every path ever added — 622 on 2026-09-21, one more with every commit — is checked, and none is an excerpt, a source PDF, a compendium or the plan page`

**Repair F-2c.** In S21 replace

`with a new id and holds only the 68 commits of this history`

with

`with a new id and holds this history and nothing else`

### F-3 — CHECKLIST.md item 3 was not given R-B3's correction

R-B2 said "make the identical correction in CHECKLIST.md item 3d", and it was made. R-B3
said nothing about CHECKLIST, so item 3 still closes with the exact phrasing R-B3 identified
as inaccurate, plus the two counts F-2 moves:

> Verified after the push: all five recovery routes return "No commit found" or "Not Found";
> the four feeds publish two hashes and both resolve locally; 621 paths ever added, none an
> excerpt, a PDF, a compendium or the plan page.

The fifth route does not return either string; it returns `upload-pack: not our ref`.
CHECKLIST.md is an evidence token of the card (`doc:CHECKLIST.md`) and it is now less
accurate than the Statement it supports. It is private-tracked and does not reach the site.

**Repair F-3.** In CHECKLIST item 3 replace that sentence with

`Verified after the push: all five recovery routes fail — the four REST routes with "No commit found" or "Not Found", and git fetch of a discarded SHA with "upload-pack: not our ref"; every hash the four feeds publish resolves locally; every path ever added is checked, and none is an excerpt, a PDF, a compendium or the plan page.`

### F-4 — `repo-split`, S15: an ordinal whose list R-B1 deleted

S15 says the exposure was cleared "by **the second** of the two recorded routes". The
enumeration that made "second" countable was old S22, which R-B1 correctly deleted; the
surviving S22 names the other route but does not number it. The colon after "routes"
supplies the content, so nothing is false and nothing is unrecoverable — the ordinal simply
has no list to count in any more.

**Repair F-4.** In S15 replace `by the second of the two recorded routes:` with
`by the second of the two routes the notes had recorded, the one that removes the objects rather than waiting for them to be purged:`

### F-5 — `ci-green`, S09: "also" attached to a fact already given

S05 says the cause was isolated only afterwards "because the Makefile sent pdflatex's output
to `/dev/null` and no run ever recorded the error". S09 then says "The Makefile **also** sent
pdflatex's output to `/dev/null`, so the log recorded a non-zero exit with no reason
attached". It is the same redirection, not a second one, and "also" makes it read as an
additional failing. Both sentences are true; the connective is not.

**Repair F-5.** Replace S09 with

`That same redirection is why the log recorded a non-zero exit with no reason attached; on failure the papers target now prints the last 40 lines of main.log.`

### F-6 — `ci-green`, S15–S16: a circular back-reference left by R-C1

R-C1 correctly turned a run id into "the next run". What is left reads "at **the commit
before the regeneration** the committed claim map was missing … and the next run was green
over it. It was regenerated in **the following commit**." True, but it defines the commit by
the regeneration and then announces the regeneration as news.

**Repair F-6.** Replace those two sentences with

`This is not hypothetical: one commit shipped a claim map that was missing the ci-green and docs-pages-rendering nodes and six edges, the run over it was green, and the drift was caught and regenerated only in the next commit (REF-CI-PAGES).`

### F-7 — `public-site-plan`, `next`: two identifier namespaces in one sentence

`next` reads "keep the Pages job disabled until **D1** is satisfied; … close **D6** (the
`--line` contrast)". D1 is a plan decision; D6 is a defect id from REF-SITE-P3. The
Statement of the same card says the plan has four decisions, D1–D4, which is correct, so a
reader who takes D6 for a fifth decision is looking for something that does not exist. The
gloss "(the `--line` contrast)" saves it, and the field ships to module 10.

**Repair F-7.** In `next` replace `close D6 (the --line contrast) in the shared layer`
with `close the open accessibility item REF-SITE-P3 numbered D6, the --line contrast, in the shared layer`.

### F-8 — `public-site-plan`, S01 of `repo-split`, and one stale figure in the plan document

Three record-keeping observations, no repair owed by these cards:

- The card's P4a note records D6 as "`--line` at 1.35-1.54:1" and says `docs/index.html`
  lists only modules 1, 2 and 6. The later REF-MOD345 note *in the same card* measures
  2.99:1 on `--bg` and 3.81:1 in dark and records that index.html links all three new pages.
  The later note carries the correction, the author rule protects both, and the record is
  layered rather than wrong.
- `rigor/public_site_plan.md:235` (D3) still says "33 refereed-or-proved claims plus 11
  headline numericals". The card says 12 and explains the move; the card is right and the
  plan document is the stale one. It should go into the same edit `next` already owes for
  the module-9 bracket at line 110.
- `repo-split` S01 calls the set "the 97 tracked `.out` **run captures**" and then, four
  clauses later, "96 of them run captures and one (`rigor/_probe.out`) a stray LaTeX
  bookmark file". The head noun over-claims by one and the apposition corrects it inside the
  same sentence. Suggested: `the 97 tracked .out files`. (S27 also wants a comma after the
  closing parenthesis of the six-paper list.)

### F-9 — the workflow comment still names a dead hash

`.github/workflows/check.yml:47` reads "its absence is what failed every papers job before
`9aed69a`". That hash resolves nowhere. It is not a referee note, so nothing protects it,
and CHECKLIST 3e covers it only generically. REF-CLEARED raised this as N-B10 and it was not
applied.

**Repair F-9.** Replace `before 9aed69a` with `before the CI repair of 14:53 on 2026-09-21`.

---

## 6. Consistency

No card in the knowledge base contradicts any of the three. The only other cards that
mention the compendia, recoverability or the force-push are `ci-green`, whose references are
all in referee notes, and `longo-xu-cmi`, whose own later note (REF-MOVE-1j) clears its
earlier failure and records the rewrite. `grep` over every claim card for "still
recoverable", "not cleared" and "MUST NOT BE MADE PUBLIC" outside referee notes returns
nothing.

CHECKLIST.md and PRIVATE.md agree with all three Statements and with all three `next`
fields, with the single wording exception at F-3. CHECKLIST item 4 (absolute paths in
fourteen tracked capture files) is the only item in that file neither struck through nor
marked SUPERSEDED or MOOT, but its own text records the decision to leave the captures
alone rather than an outstanding action, so `next`'s "No item gates publication any more"
stands.

## 7. Verdicts

- `repo-split-public-private`: **PASS**. All four blocking repairs applied verbatim and true;
  the five-and-ten count and the nine-targets/ten-cards count reproduce exactly; the
  clearance holds on every route I re-ran. F-1 is one word and F-2 is four counts that the
  repair commit itself moved.
- `ci-green`: **PASS**. All three repairs applied verbatim; no run id and no commit hash
  survives anywhere in the card or in the shipped claim map; the rewritten `How to verify`
  runs and returns precisely what it promises.
- `public-site-plan`: **PASS**. Both repairs applied verbatim and true; every figure
  re-measured, including the 12-numericals recount that gives 45; the budget holds and its
  parenthesis is now correctly declared dated.
