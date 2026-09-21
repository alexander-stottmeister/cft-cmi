# REF-PLAN-SPLIT: adversarial review of public-site-plan and repo-split-public-private (2026-09-21)

Scope: exactly two cards of the 2026-09-21 packet, `public-site-plan` and `repo-split-public-private`.
`ci-green`, `docs-pages-rendering` and `generated-docs` were read for consistency only; no verdict is
recorded on them here and nothing of theirs is touched.

Everything below was measured on 2026-09-21 against the working tree, the two local git directories, a
fresh `--mirror` clone of `https://github.com/alexander-stottmeister/cft-cmi.git`, the GitHub REST API and
the GitHub Actions run list. No git command that writes was run. Both verdicts are **FAIL**.

The two clauses the orchestrator had just edited were treated as unverified and re-derived from scratch.
One of them (`public-site-plan`, the CI clause) is still false; the other (the decisions clause) holds.
The edited clause of `repo-split-public-private` holds on the refs and **fails on the remote**, which is
the most serious finding of this pass and is written up in section B.13.

---

## A. public-site-plan — FAIL

### A.1 Claim table

| # | Claimed (Statement, verbatim unless quoted short) | Measured | Verdict |
|---|---|---|---|
| A1 | "rigor/public_site_plan.md (227 lines, repaired after REF-SITE-1)" | `wc -l` = **237**. REF-SITE-1c already measured 230 | FAIL, stale |
| A2 | "a README of about 250 lines replacing the current 80" | README.md is **430 lines**, 31,628 B; it was replaced at f61cc5f (09-21 01:20, P1). There is no 80-line README to replace | FAIL, stale |
| A3 | "eight figures, four of which already exist (collapse, gap_decay, thermal_shield, cfun_flow) and **four** generated as SVG by tools/make_figures.py (geometry schematic; Phi against zeta …; the coefficient across models …; the theta convergence ladder; the corner calculus)" | The parenthesis lists **five**. The plan's figure table is F1-F8: F1-F5 **new SVG**, F6-F8 the existing PNGs (F7 carries two of the four PNGs). `docs/assets/` holds exactly five SVGs: geometry, quadratic-law, universality, theta-ladder, corner-calculus. So 5 new + 3 existing slots = 8, not 4 + 4 | FAIL, false and self-contradictory in one sentence |
| A4 | "(B) … .nojekyll, plain ES modules, vendored KaTeX, no runtime external requests, ten modules" | plan §2 says all of this; `docs/.nojekyll` exists; `docs/explore/` holds ten pages | PASS |
| A5 | "(C) docs/{index,status,notation,definitions,open,sources,history}.md plus docs/results/<id>.md … with a make check that fails on drift" | plan §3 lists exactly those eight targets; `Makefile` has `check:` | PASS |
| A6 | "the 33 refereed-or-proved claims (30 proved, 3 refereed)" | `kb -p cft_cmi q --status`: proved **30**, refereed **3** | PASS |
| A7 | "plus the **11** headline numericals the modules display" | The module table (plan l.99-110) now names **12** numerical ids: the eleven REF-SITE-1b listed **plus `circle-model-taper-suppresses-theta`**, which REF-P0-TAPER-b passed on 2026-09-21 (`review: passed 2026-09-21 by REF-P0-TAPER-b`) and which module 5 was then built to display (P4a note, `docs/explore/theta-reconciliation.html`). REF-SITE-1b's own reasoning said 11 "and not 12" *because* the card was unrefereed; that reason has lapsed | FAIL |
| A8 | "**44** of the **81** cards" | Numerator 33 + 12 = **45**. Denominator: `projects/cft_cmi/claims/` holds **89** card files (81 was exact at kb commit d8c70e1, 2026-09-21 00:09, when this card was written); `docs/status.md:5` says **90 cards**; `kb q` lists 98 including the 8 area cards. **81 matches nothing today** | FAIL, both numbers |
| A9 | "a card that has never been refereed is not displayed **at all**" | False as an absolute. Module 10 (`claim-map.html`, `docs/data/extra-claim-map.json`) displays **90 cards** and marks the unrefereed ones instead. The card's own P4b note says so: "The plan's rule … cannot apply to module 10, whose subject is the record itself" | FAIL, contradicted by this card's own note |
| A10 | "which makes a referee pass on circle-model-taper-suppresses-theta a prerequisite for module 5" | It was; the pass ran (P0, REF-P0-TAPER-b) and module 5 is built | Stale tense, minor |
| A11 | "implementing only the junction form would teach a false theorem: **(H) fails for single-interval starts and for union conditioning**, and there the naive corner measure is wrong" | **This is the exact sentence REF-SITE-1b failed the plan for.** The plan was repaired (l.119-124): "(H) **can** fail … It does not always fail in those shapes: VWZ 1(A) and 1(B) both condition on a union and both satisfy (H), 1(B) because its two corners coincide, while 'add D on C, then A on BC' does not." The card's own dated note of 2026-09-21 says the same. The Statement was never repaired, so the card still asserts the falsehood, contradicts its own note, and misstates twice-refereed mathematics (`protocol-corner-data-n4-n5`) | FAIL, substantive, not staleness |
| A12 | "the Protocol 3 panel must state that its map equals the over-compressed Theorem-A map only up to post-composition with a global Moebius map" | plan l.129-131, verbatim in substance | PASS |
| A13 | "Every displayed number ships as a JSON record {value, error, source, line, status} whose source is a repository path, and make check fails on drift" | plan §2 "The data pipeline"; `make check` runs both extractors with `--check` | PASS |
| A14 | constraints: no third-party excerpt on the public surface; PDFs gitignored; free-tier Pages serves public repositories only; the browser cannot redo ball arithmetic, SDPs or Galerkin solves | plan C1, C2, C3, C4, faithfully | PASS |
| A15 | "**CI was red until implementation_C11.tex and its referee report build**" | **False.** The workflow was added at e2c5260 (09-21 10:36). The two documents were repaired at **7cae480 (09-21 11:07)**. CI then failed **twelve more times** and did not go green until **9aed69a (09-21 14:53)**, run 35602149545. Worse, the documents could not have been the cause at all: `tools/check_rigor_builds.py` is the *third* step of the papers job and, per ci-green (re-measured by REF-CI-PAGES), **never executed once** in any of the 24 failing runs. CI was never red because of these two documents | FAIL |
| A16 | "both build since 2026-09-21" | Re-compiled both myself, `pdflatex -halt-on-error -interaction=nonstopmode` into a scratch dir: **rc 0** for `implementation_C11.tex` (1,457,253 B PDF) and for `referee_implementation_C11.tex` (619,581 B). `rigor/known_build_failures.json` is `{}` | PASS |
| A17 | "and CI is green since the unrelated repairs recorded in ci-green" | `gh run list`: 27 runs, 24 failures then 3 successes. The two causes (missing `lmodern`; `build_site_data_extra.py --check` without the knowledge base) are both unrelated to the two documents | PASS — but see A15: the same sentence asserts the opposite in its first half |
| A18 | "**Also planned**: CITATION.cff and a Zenodo DOI, a .github issue template, deletion or marking of the frozen plan_page/petz_program_plan.html, and a 3 MB budget for site assets" | Three of the four are **done**, not planned: `CITATION.cff` is tracked; `.github/ISSUE_TEMPLATE/` exists (incl. `cited-result.md`); `plan_page/petz_program_plan.html` was deleted from the public tip at e2c5260 and is now private-only. Only the DOI is outstanding, and the plan gates it on "once the papers are on arXiv", which the 2026-09-21 user decision withdrew. Budget met: docs/{assets,lib,data} = 1.26 MB, public repo 7.93 MB | FAIL, stale |
| A19 | "**Five** phases with a referee pass **each**" | The plan's §5 table has **six** rows, P0-P5 (P0 was added at b2f3c18 after REF-SITE-1c). Two of the six have no referee pass: P0's referee column reads "it is itself the pass", P5's reads "the workflow is its own check" | FAIL |
| A20 | "4-6 agent-days, an estimated 4M-6M tokens" | plan §5, verbatim | PASS |
| A21 | "with a stated reduction to **two modules** if that is too much" | The plan says "cut **P4** to modules 4 and 6", which leaves modules 1, 2, 4 and 6 — four modules on the site, not two | Minor, imprecise paraphrase |
| A22 | "Four decisions, all TAKEN by the user on 2026-09-21 and **recorded at rigor/public_site_plan.md:224**" | Line 224 is exactly `## 6. Decisions — taken 2026-09-21 by the user`; D1, D2, D3, D4 all follow, each stated as taken. Notes do not contradict it: the closing note says "Decision D1 of the plan is unchanged" | **PASS** — the edited clause holds, on all three points asked |
| A23 | "D2 how readers get the PDFs (**option (c)** also needs an exception to the *.pdf ignore rule)" | The plan contains **no (a)/(b)/(c) option list anywhere** (`grep -n '(a)\|(b)\|(c)'` returns nothing). D2 as taken publishes PDFs "under `docs/pdf/` as a Pages artefact, **without committing them, which keeps the `*.pdf` ignore rule intact**", i.e. it needs no exception. The parenthesis is a dangling reference to a deleted option and contradicts the decision it annotates | FAIL |
| A24 | "D4 whether the site carries the AI provenance (recommended yes, in the papers wording)" | Decided yes and built (P3: `docs/index.html`, 1642-character verbatim blockquote) | Minor, stale "recommended" |
| A25 | How to verify: "**nothing is built yet**, so the card is a plan, not a description of the repository" | P0, P1, P2, P3, P4a and P4b are all built and recorded in **this card's own notes**: ten module pages, 131 generated documentation files, five SVGs, two extractors, a Makefile and a green CI. The one-line verification instruction of the card is flatly false | FAIL |
| A26 | `next:` "User decisions D1-D4, then phase P1 (figures and README) and P2 (docs generator) in parallel" | Decisions taken; P1 and P2 finished at 01:06-01:20 on 09-21; P3, P4a and P4b are finished too. This field is **published verbatim** on the public surface — `docs/data/extra-claim-map.json` carries it as `next` for this card, and module 10 renders it | FAIL |

### A.2 Exact repair wording

**R-A1.** `(227 lines, repaired after REF-SITE-1)` → `(237 lines, repaired after REF-SITE-1 and extended with phase P0)`.

**R-A2.** `a README of about 250 lines replacing the current 80` → `a README of about 250 lines replacing the 80-line one (built in P1; it came out at 430 lines)`.

**R-A3.** `with eight figures, four of which already exist (collapse, gap_decay, thermal_shield, cfun_flow) and four generated as SVG by tools/make_figures.py` → `with eight figure slots, three of which reuse the four existing PNGs (collapse, gap_decay and thermal_shield sharing slot F7, cfun_flow) and five generated as SVG by tools/make_figures.py`.

**R-A7 + R-A8.** `plus the 11 headline numericals the modules display, 44 of the 81 cards` → `plus the 12 headline numericals the modules display (11 when the card was written; circle-model-taper-suppresses-theta joined them when REF-P0-TAPER-b passed it on 2026-09-21 and module 5 was built around it), 45 claims; the knowledge base now holds 89 claim cards and docs/status.md carries the current figure`.

**R-A9.** `and a card that has never been refereed is not displayed at all, which makes a referee pass on circle-model-taper-suppresses-theta a prerequisite for module 5` → `and a card that has never been refereed is not displayed in modules 1-9, which made a referee pass on circle-model-taper-suppresses-theta a prerequisite for module 5 (phase P0, done 2026-09-21); module 10 is the exception the rule cannot cover, since its subject is the record itself, so it displays every card and marks the unrefereed ones`.

**R-A11.** `because implementing only the junction form would teach a false theorem: (H) fails for single-interval starts and for union conditioning, and there the naive corner measure is wrong` → `because implementing only the junction form would teach a false theorem: (H) CAN fail when a step conditions on a union of chain intervals or the chain starts from a single interval, and where it fails the naive corner measure is wrong; it does not always fail in those shapes — VWZ 1(A) and 1(B) both condition on a union and both satisfy (H), 1(B) because its two corners coincide, while "add D on C, then A on BC" does not — so the module tests (H) itself rather than inferring it from the shape of the protocol`. (This is the plan's own repaired wording; the card must not be left holding the version REF-SITE-1b refuted.)

**R-A15.** `CI was red until implementation_C11.tex and its referee report build; both build since 2026-09-21, and CI is green since the unrelated repairs recorded in ci-green` → `constraint C6 predicted that CI would be red until implementation_C11.tex and its referee report built; both have built since 7cae480 (2026-09-21 11:07), but C6 was never in fact the cause — tools/check_rigor_builds.py never ran in any of the 24 failing runs — and CI went green only at 9aed69a (14:53) after the two unrelated repairs recorded in ci-green`.

**R-A18.** `Also planned: CITATION.cff and a Zenodo DOI, a .github issue template, deletion or marking of the frozen plan_page/petz_program_plan.html, and a 3 MB budget for site assets.` → `Also in the plan and now done: CITATION.cff, the .github issue templates, and the removal of the frozen plan_page/petz_program_plan.html from the public repository (it is tracked privately). The 3 MB asset budget holds (docs/{assets,lib,data} = 1.26 MB, public repository 7.93 MB). Still outstanding: the Zenodo DOI, which the plan gates on an arXiv posting that the 2026-09-21 user decision withdrew.`

**R-A19.** `Five phases with a referee pass each` → `Six phases, P0 to P5, four of them with a referee pass (P0 is itself a referee pass and P5 is checked by the workflow it builds)`.

**R-A21.** `with a stated reduction to two modules if that is too much` → `with a stated reduction of P4 to modules 4 and 6 if that is too much, leaving four modules interactive and the rest as static figures`.

**R-A23.** `D2 how readers get the PDFs (option (c) also needs an exception to the *.pdf ignore rule)` → `D2 how readers get the PDFs (decided: release assets now, and once CI is green a docs/pdf/ Pages artefact that is never committed, so the *.pdf ignore rule stands unamended)`.

**R-A25.** Replace the whole How-to-verify line with: `rigor/public_site_plan.md for the plan; for what has been built from it see the progress notes below and the cards readme-and-figures (P1), generated-docs (P2), interactive-site (P3), interactive-site-modules-3-4-5 (P4a) and interactive-site-modules-7-10 (P4b). Phases P0 to P4b are done; P5 is partly done (Makefile and workflow exist, Pages deployment is written and disabled under D1).`

**R-A26.** Replace the `next:` field with: `P5: keep the Pages job disabled until D1 is satisfied; repair the plan's module-9 bracket wording as P4b asked; close D6 (the --line contrast) in the shared layer.` — this field is published verbatim in docs/data/extra-claim-map.json and must not stay at "User decisions D1-D4".

### A.3 Consistency

No other card contradicts this one, but three of its own notes do: the P4b note contradicts A9, the 2026-09-21
overcorrection note contradicts A11, and the P1/P2/P3/P4a/P4b notes contradict A25 and A26. A card whose notes
refute its Statement in four places cannot pass. Note also that `docs/data/extra-claim-map.json` ships the
Statement's "227 lines" and "44 of the 81 cards" and the stale `next` to the public site today.

---

## B. repo-split-public-private — FAIL

### B.1 Claim table

| # | Claimed | Measured | Verdict |
|---|---|---|---|
| B1 | ".git holds the publishable project (**406 files, 5.9 MB** …)" | `git ls-files` = **614**; blob bytes at HEAD b9daa45 = **7,930,986 B = 7.93 MB (7.56 MiB)**. 406 was exact on 2026-09-20 and the rewrite even preserves it: the rewritten 09-20 tip a09ab81 now carries 401 = 406 − the five compendia | FAIL, stale |
| B2 | "… and the **97 result captures** the KB cites as evidence" | No rule reproduces 97. Public-tracked under `numerics/`: 83 `.out`, 19 `.txt`, 2 `.err`, 6 `.md`, 6 `.raw` → 104 (.out+.txt+.err), 116 (+md+raw), 121 non-script. Front-matter evidence targets under `numerics/` that are not scripts: 27. All non-document evidence targets: 37. Identical at the 09-20 tip, so the figure was not derivable then either | FAIL / unverifiable as stated |
| B3 | ".git-private holds … (**229 files, 47.7 MB**: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude)" | **235 files, 48,389,337 B = 48.39 MB**. The enumeration is short by six: `plan_page/petz_program_plan.html` and `rigor/cited_R{1,2,3,4}.tex` + `rigor/cited_results_all.tex`. All six are in `pgit`'s own `PRIVATE_PATHS`, and the same Statement says two sentences later that the compendia were moved there | FAIL, stale and internally inconsistent |
| B4 | "BOTH REMOTES ARE PRIVATE as of 2026-09-20; the first is public-ready but not public" | `gh repo view`: both `PRIVATE`, `isFork` false, `forkCount` 0 | PASS |
| B5 | "The two tracked sets are disjoint (**overlap 0**)" | `comm -12` over the two sorted `ls-files` outputs: **0** | PASS |
| B6 | "the files tracked by neither are regenerable build products and caches (**196 MB**)" | 421 files, **197,745,228 B = 197.7 MB (188.6 MiB)**. Largest are `.npz`, `.pkl`, `.log`, `.pdf`, `.aux`; the 19 `.md` are the review packets | Minor drift, not blocking |
| B7 | "**255 call sites in 19 documents** were converted" | 256 `\shot`/`\shotc` invocations across 20 `.tex` files; one of them is the `\shot[#1]{#2}` inside the `\shotc` definition at `rigor_preamble.tex:48`. Net **255 in 19** | PASS. Remark: 172 of the 255 now live in the five private compendia, so the public surface carries 83 call sites in 14 documents |
| B8 | "the 24 python scripts … now resolve paths against a computed _ROOT (37 literals), and the four shell scripts … honour $PYTHON" | **0** tracked `.py` contains `/Users/alex`; 25 tracked `.py` mention `_ROOT`; `numerics/{run_hp14,run_largezeta,run_largezeta2}.sh` and `numerics/certified/runhp.sh` all read `PY=${PYTHON:-python3}` | PASS (historical conversion count) |
| B9 | "./pgit sync force-stages them and ./pgit check fails on either an overlap or untracked excerpts; … the whitelist is tracked as pgit-exclude and ./pgit reinstalls it on every run" | All three verified in the `pgit` source; `check` also prints the two file counts and the shots tally. Measured by hand: overlap 0, shots on disk 178 / tracked 178 | PASS |
| B10 | "**The public history never contained an excerpt or a source PDF** (verified against a clone of the remote)" | Verified far beyond the claim. Over the mirror clone's reachable history **and** the 43 pre-rewrite commits I recovered from the remote: **620 distinct paths ever added, 0 under `rigor/shots`, 0 `*.pdf` in any tree of any commit** | PASS, stronger than claimed |
| B11 | "It DID contain the five cited-result compendia" | Yes. `ba14962` (run 35585764998) removes all five; the rewrite shrank every tree, e.g. the 09-20 tip from 406 to 401 files | PASS |
| B12 | "they were **removed from every commit** and force-pushed" | True of the refs. Post-rewrite, neither the local `.git` (1310 objects, reachable = total, `fsck` clean) nor the mirror clone holds any compendium object; the tag's tree is clean | PASS on refs only — see B13 |
| B13 | "**verified from mirror clones**" (and the addendum: "the five blob SHAs are absent … ba14962, 8ab5a32, f9ffae4 and 51b11c3 are no longer valid object names") | **SERIOUS FAILURE. All five compendia are still fully recoverable from the public remote today.** Three independent routes, all executed: (i) `git --git-dir=<mirror> fetch origin 5d64c77d4b513b4005e2ad3a19c0f26086e96be0` **succeeds** and brings back 43 pre-rewrite commits whose tree contains `rigor/cited_R1..R4.tex` and `cited_results_all.tex`; (ii) `gh api repos/…/contents/rigor/cited_results_all.tex?ref=5d64c77…` returns 299,915 bytes that `cmp` byte-identical to the private copy, and likewise `cited_R1` 70,874 B, `cited_R2` 72,489 B, `cited_R3` 66,304 B, `cited_R4` 90,433 B — all four `cmp`-identical; (iii) `gh api repos/…/git/blobs/18cc05ab438b307f64fd7b4ee35834b30c06f0d6` returns the blob directly by SHA. Every one of ba14962, 8ab5a32, f9ffae4, 51b11c3, 5d64c77, ade3048, b9307d8 and 8b96354 **resolves through the API right now**. And the SHAs are not a secret anyone must be told: the repository's own **GitHub Actions run list publishes them as `headSha`** (runs 35585764998, 35588006441, 35584449606, …), so any principal with read access can enumerate the pre-rewrite history without being handed a hash | **FAIL, serious** |
| B14 | addendum: "REF-MOVE-1e confirmed from a mirror clone that the five blob SHAs are absent …" | The observation is true and the inference a reader draws from it is false. A clone by construction carries only reachable objects, so a mirror clone can never detect server-side retention; it is the wrong instrument for the question. The addendum's hedge ("may retain … could in principle still resolve") understates a one-command, reproducible recovery | FAIL as evidence for B13 |
| B15 | "One designated-private path is still recoverable from the public history, **plan_page/petz_program_plan.html**, which **entered in the initial import** and is **in the tree of the pushed tag v0.1.0-draft**" | All parts hold. Added at `03e2e48` "cft_cmi: initial import"; removed from the tip at `e2c5260`; present in `ls-tree -r refs/tags/v0.1.0-draft` both locally and in the mirror clone; `git ls-remote` shows `5ad78cb… refs/tags/v0.1.0-draft`, so the tag is on the remote; the file is private-tracked (public 0, private 1) | **PASS**, all four parts |
| B16 | "Licensing: MIT for code, CC BY 4.0 for documents and data, no third-party material redistributed (THIRD-PARTY.md)" | `LICENSE-CODE` is MIT, `LICENSE-DOCS` is CC BY 4.0, `LICENSE` states the split, `THIRD-PARTY.md` opens "None of that material is redistributed here" and has been updated to say the compendia are not published | PASS on the documents. But B13 means third-party transcriptions the project deliberately withdrew are still served by the remote to anyone with read access, so the sentence is true of the working tree and not of the remote |
| B17 | "KNOWLEDGE BASE: unaffected … a third repository (claude-team-kb, ../kb) with its own sync" | `../kb` is a separate repository with its own remote | PASS |
| B18 | "Every evidence pointer resolves on a machine carrying all three clones, and none fails" | 330 card files in areas/claims/evidence; **155 distinct front-matter `evidence:` targets, 0 missing on disk**. A free-text scan of every `doc:`/`num:`/`ref:` token gives 159 targets of which 3 fail, and all 3 are prose artefacts inside referee notes (`f3_t0.py`, `/num:/ref`, `/ref`), exactly as REF-INFRA-2c described | PASS |
| B19 | "**EIGHT** targets live in the private repo and are cited by **EIGHT** cards (counting doc:, num:, ref: tokens in areas/, claims/ and evidence/, excluding the generated INDEX, SUMMARY and CHANGELOG)" | Under the card's own stated rule: **NINE targets, TEN cards.** The ninth target is `plan_page/petz_program_plan.html`, cited by **`plan-page`** and **`open-problems-plan-note8`**. The same nine/ten come out of the front-matter-only rule. The eight originals and the six paper names are all correct | FAIL |
| B20 | restore.sh sentence (one of six recoverable under the cited name; Uhlmann76 paywalled; CDIT tabled as CDIW21; the other three bullet-only) | `refs/REFERENCES.md` has 36 table rows; `restore.sh --list` prints "20 fetchable, 16 need library access". `arXiv VWZ (2307.14434)`; `MANUAL Uhlmann76 -- paywalled`; `arXiv CDIW21 (1808.02384)`; AlbertiUhlmann02, BJL_twisted_duality and Sion1958_minimax occur once each, as bullets at REFERENCES.md:49-51, outside the pipe table restore.sh parses | PASS, exact |
| B21 | "The review packets the KB writes into rigor/ are tracked by neither repository" | 19 packets on disk; each `pub=0 priv=0` | PASS |
| B22 | "A new machine needs three clones as siblings … with the fetch refspec, upstream and ./pgit check that PRIVATE.md spells out" | `PRIVATE.md` carries the refspec, `core.worktree`, `--set-upstream-to` and the closing `./pgit check`, as described. REF-INFRA-2b's end-to-end run was not repeated | PASS on the document |
| B23 | Consistency with the card's own evidence documents | **`PRIVATE.md` still says the compendia "are currently public, which is defensible"** and still says "Eight knowledge-base cards cite eight files … CHECKLIST.md, PRIVATE.md", and its "What this is" bullet still omits plan_page and the compendia. **`CHECKLIST.md` item 3 is unstruck** and reads as an open question about material that is still public, although the card's `next` calls that gate discharged (items 1, 2 and 5 all carry their DONE/SUPERSEDED marks, so the omission is visible). `THIRD-PARTY.md` has been updated correctly | FAIL |
| B24 | `next:` "The still-open items of CHECKLIST.md … are four" | Items 3, 4, 6 are unstruck and item 5 is SUPERSEDED-but-alive, so four is defensible — but only because item 3 was never marked (B23) | Defensible; fix by marking item 3 |
| B25 | `next:` grammar (REF-MOVE-1h defect 3) | The lower-case sentence start is fixed. "removed from the public history, that gate is discharged" is still a comma splice | Minor, partly unfixed |

### B.2 Exact repair wording

**R-B1/R-B2/R-B3.** `.git holds the publishable project (406 files, 5.9 MB: papers, notes, rigor documents, numerics scripts and the 97 result captures the KB cites as evidence)` → `.git holds the publishable project (614 files, 7.93 MB as of 2026-09-21: papers, notes, rigor documents, numerics scripts and their run captures, and since 2026-09-21 the generated documentation and the interactive site under docs/)`; and `.git-private holds what must not be published (229 files, 47.7 MB: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude)` → `.git-private holds what must not be published (235 files, 48.4 MB: the 178 page excerpts in rigor/shots, the 47 source PDFs in refs, the five cited-result compendia rigor/cited_R1-R4.tex and cited_results_all.tex, plan_page/petz_program_plan.html, CHECKLIST.md, PRIVATE.md, pgit, pgit-exclude — the list pgit's PRIVATE_PATHS enforces)`. Either drop "97 result captures" or state the rule that produces it; nothing I tried does.

**R-B6.** `(196 MB)` → `(about 198 MB)`.

**R-B13 — the one that matters.** Replace `they were removed from every commit and force-pushed, verified from mirror clones (see the compendia cards and rigor/referee_compendia_move.md)` with:

> they were removed from every commit and force-pushed, and no ref of the remote reaches them any more (verified from a fresh mirror clone: 0 objects bear their names, the tag's tree is clean, 620 distinct paths were ever added and none is an excerpt or a PDF). **They are nevertheless still recoverable from the remote.** GitHub retains the unreachable objects and serves them by SHA: on 2026-09-21 `git fetch origin 5d64c77` against the remote returned 43 pre-rewrite commits with all five files in the tree, and the REST contents and blobs endpoints returned each compendium byte-identical to the private copy. The pre-rewrite hashes are not confidential — this repository's own Actions run list publishes them as the head SHA of every run before 9aed69a. The rewrite therefore bought unreachability, not deletion. What bounds the exposure is access control alone: the repository has never been public, is unforked and has no other collaborators. Deletion requires one of the two routes already recorded — a GitHub Support purge of the unreachable objects, or deleting the remote and recreating it from this local history with the two release assets re-uploaded — **and until one of them is done, "removed from the remote" must not be claimed.**

The same correction belongs in a new dated note (the existing addendum is a referee note and is not to be rewritten), stating plainly that the mirror-clone check REF-MOVE-1e ran cannot see server-side retention and that the three recovery routes above were executed and succeeded.

**R-B19.** `EIGHT targets live in the private repo and are cited by EIGHT cards (counting …): six source papers (…) plus doc:CHECKLIST.md and doc:PRIVATE.md` → `NINE targets live in the private repo and are cited by TEN cards (counting …): six source papers (AlbertiUhlmann02_math-ph-0202038, BJL_twisted_duality_math-ph-0204029, CDIT_1808.02384, Sion1958_minimax, Uhlmann76, VWZ_2307.14434), doc:CHECKLIST.md, doc:PRIVATE.md, and doc:plan_page/petz_program_plan.html, which plan-page and open-problems-plan-note8 cite and which became private-only on 2026-09-21`.

**R-B23.** Three edits outside the card, all of which the card's own Statement now contradicts:
(i) `PRIVATE.md`, last section: delete "The open case is `rigor/cited_R1..R4.tex` and `cited_results_all.tex` … They are currently public, which is defensible …" and replace with "`rigor/cited_R1..R4.tex` and `cited_results_all.tex` were moved here on 2026-09-21 and removed from the public history; see CHECKLIST.md item 3."
(ii) `PRIVATE.md`, "What this is" bullet and the pointer paragraph: add `plan_page/petz_program_plan.html` and the five compendia to the private list, and change "Eight knowledge-base cards cite eight files that live here" to "Ten knowledge-base cards cite nine files that live here", adding `plan_page/petz_program_plan.html` to the enumeration.
(iii) `CHECKLIST.md` item 3: strike the heading and mark it, in the style of items 1, 2 and 5 — "~~**The cited-result compendia.**~~ DONE 2026-09-21: moved to the private companion and removed from the public history by a filter-branch rewrite. Residual: GitHub still serves the pre-rewrite objects by SHA; see repo-split-public-private."

**R-B25.** `removed from the public history, that gate is discharged` → `removed from the public history; that gate is discharged`.

### B.3 What I could not break

The edited clause's two strongest parts survive scrutiny and deserve to be recorded as verified, not merely
asserted: (1) no excerpt and no source PDF was ever added to the public history — 0 across 620 distinct paths
over both the reachable and the recovered pre-rewrite history, which is a wider test than the card claims;
(2) `plan_page/petz_program_plan.html` is exactly as described — initial import, in the tag's tree, tag on the
remote. `overlap 0`, the `pgit` mechanism, the restore.sh sentence, the pointer-resolution claim and the
packet-tracking claim are all exact.

---

## C. Verdicts

- `public-site-plan`: **FAIL** — thirteen defects, of which A11 (a refuted statement about hypothesis (H)
  reinstated in the Statement), A15 (a false causal claim about CI), A25 ("nothing is built yet") and A26
  (a stale, publicly rendered `next`) are the blocking ones.
- `repo-split-public-private`: **FAIL** — six defects, of which B13 is serious: the five cited-result
  compendia are still byte-recoverable from the public remote by three separate routes, and the pre-rewrite
  commit hashes are published by the repository's own Actions history.
