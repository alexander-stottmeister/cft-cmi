# REF-PASS-E: fifth pass on generated-docs and repo-split-public-private (2026-09-21)

Scope: the two cards REF-PASS-D failed, against `referee_pass_d.md` (REF-PASS-D) and, behind it,
`referee_pass_c.md`, `referee_ci_pages.md`, `referee_ci_pages_b.md` and `referee_plan_split.md`.

Verdicts: **`generated-docs` FAIL, `repo-split-public-private` FAIL.**

Everything marked [E] is measured by me at HEAD = `85a2d4a`; the state REF-PASS-D reviewed is
`bbaa665`, two commits back. `git status --porcelain` was empty before I started and is empty now;
the five files I touched for the drift-guard tests were restored by file copy or removed. No git
command that writes was run — the remote is probed by REST only, and I did not clone it.

The brief was that four consecutive passes have each found that a repair introduced a new defect,
three of them in the same handful of sentences, and to look there first. **That is what happened
again, in both cards, and both times in the sentence the previous pass asked for.** The repairs
themselves are right: D-R6 is applied verbatim and its arithmetic holds; the `repo-split` regex
damage is fully undone and nothing else was lost with it. What is wrong is one new sentence in each
card, and in both cases the new sentence is a *generalisation* the author added on top of the repair.

---

## 1. `generated-docs` — **FAIL**

### 1.1 D-R6 is applied verbatim, and it is now true

I reconstructed D-R6's replacement text out of `referee_pass_d.md` and compared it character by
character with the card. **Applied verbatim, byte for byte** [E]. Both errors it was written to fix
are gone: "their 66 HTML renderings" is now "The other 66 … 7 top-level pages, 58 result pages and
one generated results index, which is a page in its own right and not a rendering of any source",
and the status rule and its breakdown are back on the 58 where they belong.

Every figure in it, re-measured and not read [E]:

| clause | measurement |
|---|---|
| 131 files | `build_docs --check` prints `131 pages up to date`; `git ls-files 'docs/*.md'` = **65**, `git ls-files 'docs/read/*.html'` = **66**, 65 + 66 = **131**, all tracked, 0 untracked under `docs/` |
| 65 = 7 top-level + 58 results | 7 top-level are exactly index, status, notation, definitions, open, sources, history — the seven the sentence lists; `docs/results/*.md` = **58** |
| 66 = 7 + 58 + 1 index | `docs/read/*.html` top level **7**, `docs/read/results/*.html` **59**, the 59th `index.html`; 7 + 58 + 1 = 66 |
| 58 of 90; 30 / 3 / 22 / 3 | `claims 90 (3 refereed, 30 proved, 22 numerical, 3 conjectural, …)` and `pages under results/: 58`, straight out of a fresh run. 30 + 3 + 22 + 3 = 58 |
| agreement with the dated correction note | the note says "65 Markdown sources (7 top-level and 58 under results/) and 66 HTML renderings (7 and 58 mirrors plus the generated `read/results/index.html`)" — same split, same total, no double count |
| agreement with `docs-pages-rendering` | that card says "65 pages became 131 in total, namely 65 Markdown and 66 HTML" and "one `.html` per `.md`, the same directory structure". No conflict |

Everything else in the Statement, re-measured [E]:

| claim | measurement |
|---|---|
| "783 internal links with 0 dead, 0 untracked and 0 missing anchors" | **786** `[..](..)` targets over the 65 sources, 0 external; three of the 786 are the LaTeX artefact `\[h''/h'\](p)` / `(p_k)` in `definitions.md`, not links; **783** real targets, **0** dead, **0** at an untracked file (the two "untracked" hits are the directory `results/`), **0** missing anchors |
| DETECTED 9, named on every run | the run prints nine and names them: the six PDFs, `plan_page/petz_program_plan.html`, `PRIVATE.md`, `CHECKLIST.md`. 6 + 3 = 9 |
| RENDERED "6, on 7 bullets across 6 result pages, all of them the six PDFs" | `grep 'held privately' docs/results/*.md`: **7** bullets on **6** pages (`sequential-recovery-bound-type-iii` twice), **6** distinct targets, all six PDFs |
| "the other three are cited only by cards that reach no displayed status" | `CHECKLIST.md`/`PRIVATE.md` ← `repo-split-public-private`; `plan_page/petz_program_plan.html` ← `plan-page`, `open-problems-plan-note8`, `repo-split-public-private`. All three cards are `status: active`, none has a page |
| rule (a), the three conditional pages | `all-channel-optimum-value` "rests on H1, H2, H3", `corner-calculus` "(H)", `sequential-recovery-bound-type-iii` "(U)", each with `**Conditional.**` in the status line and a `## Hypotheses` section |
| "36 source rows", "only the 20 fetchable are verified against a live `refs/restore.sh --list`" | 38 lines of `refs/REFERENCES.md` begin with a bar, less header and alignment = **36**; a live `bash refs/restore.sh --list` ends `20 fetchable, 16 need library access`. `docs/sources.md:5` carries the GUESS admission in bold and names `DaleckiiKrein` and `Petz96` |
| notation/definitions admission on the page | first paragraph of both: "assembled mechanically from the LaTeX conventions appendices … there is no curated symbol table yet: a human pass is still owed" |
| history.md admission on the page | "The lead of every entry of those status files is reproduced below, in order" |

The drift guard, retested rather than accepted [E]: a byte appended to `docs/index.md` →
`differs index.md`, exit 1; `docs/read/results/gap-law.html` deleted → `missing
read/results/gap-law.html`, exit 1; a planted `docs/read/results/zzz_orphan.html` → `stale …
(no claim generates it any more)`, exit 1; a planted `docs/zzz_orphan.md` → `stale zzz_orphan.md …
(top level: delete it by hand)`, exit 1; a planted `docs/results/zzz_stale.md` → `stale
results/zzz_stale.md`, exit 1. Each restored → `131 pages up to date`, exit 0. The hand-edit report
is alive: with `<!-- hand-edited: yes -->` on `notation.md` the run prints `130 pages up to date`,
then `NOT CHECKED, marked hand-edited: notation.md` and "a hand-edited page is never compared, so it
can go stale silently", exit 0 — and with the page also falsified it goes red on the mirror
(`differs read/notation.html`), so the marker can no longer hide a stale page in a committed tree.

### 1.2 The new defect

**E-D1 — `## How to verify` is no longer empty, which is the repair D-R7 asked for, and the sentence
the author added to it is false.** The field now reads:

> "python3 tools/build_docs.py --check, or make check, which prints the page count, the claim tally,
> the privately held evidence pointers by name and the review state, and exits non-zero on any drift.
> **Every count in the Statement is one that run prints; none is typed.** To test the guard itself,
> change a byte in docs/index.md, delete a page under docs/read/, or plant an orphan under
> docs/read/results/: each is reported, and restoring it returns the run to '131 pages up to date'."

Everything in it except the bolded sentence is exact, and I executed all of it (§1.1): the four
things it says the run prints are printed, the exit code is non-zero on drift, and all three guard
tests fire and clear.

The bolded sentence is not. I took the full output of `make check` — `check_links.py`,
`build_docs.py --check` and `build_site_data.py --check` together — and looked for every number the
Statement asserts [E]:

| Statement count | printed by the run? |
|---|---|
| 131, 58, 30, 3, 22, 3, 90, 9 | **yes** |
| **65** ("Sixty-five"), **66**, **7** (top-level, twice), the generated results index | **no** |
| **783** internal links, 0 dead / 0 untracked / 0 missing anchors | **no** — `make check` prints `155 pages, 2211 links resolve`, which is `check_links.py` over the whole site, a different corpus and a different number |
| **6** rendered, on **7** bullets across **6** result pages | **no** |
| **36** source rows, **20** fetchable | **no** — these come from `refs/REFERENCES.md` and `refs/restore.sh --list` |
| a never-refereed card marked in **four** places | **no** |

So of the Statement's figures the run prints eight and does not print at least nine. A reader who
follows the field literally looks for 783 in the output of the command the field names and does not
find it. The sentence also overreaches in the other direction: it says "none is typed", but 783, 36,
20 and 6/7/6 are typed into the card from measurements made elsewhere — correctly typed, as I
re-derived every one of them, but typed.

This matters more than a wording slip for three reasons. It is the one field of a tool card a reader
executes, and the brief for this whole review says so. It ships: `docs/data/extra-claim-map.json`
carries the `verify` string verbatim, so this sentence is on the published surface. And it is a new
over-claim laid on top of a correct repair, in a card whose Statement already carries the true and
narrower version of the same idea ("Every count is computed, never typed", which is about what the
generator computes for the pages, and which holds).

### 1.3 Exact repair

**E-R1.** In `## How to verify`, replace

> "Every count in the Statement is one that run prints; none is typed."

with

> "That run prints the Statement's 131, the claim tally (90 listed, 30 proved, 3 refereed, 22 numerical, 3 conjectural), pages under results/: 58, and the nine privately held pointers by name. The Statement's other figures are measured outside it, each in one command: 65 and 66 by git ls-files 'docs/*.md' and git ls-files 'docs/read/*.html'; 783 internal link targets by a scan of the 65 sources (tools/check_links.py's own totals, 155 pages and 2211 links, are over the whole site and are a different corpus); 36 source rows by grep -c '^|' refs/REFERENCES.md less the header and alignment rows; 20 fetchable by bash refs/restore.sh --list; and 6 pointers on 7 bullets across 6 pages by grep -c 'held privately' docs/results/*.md."

I ran every command in that replacement and each returns the figure the Statement states.

If the author prefers the short fix, **delete the sentence**. Nothing else in the field depends on
it, and the Statement's own "Every count is computed, never typed" already says the true thing.

### 1.4 Non-blocking

**E-N1.** The Statement's drift-guard sentence still enumerates "a changed byte, a stale results
page, a deleted results page and a changed card, and now also on an orphan top-level page" and never
mentions `docs/read/`. The first sentence's closing "All 131 are inside the drift guard" now carries
that load, and I retested that `--check` does cover `read/` recursively, so this is no longer false —
but the two sentences would read better with one clause moved.

**E-N2.** "REF-DOCS-1 verified … 0 problems in 58" and "a card never refereed is marked in four
places, tested on a temporary knowledge-base copy" are attributions to earlier passes, re-verified by
REF-DOCS-1c and REF-PASS-C. I did not rebuild the temporary knowledge-base copy; the marker machinery
is present and the run reports `cards never refereed: 0 of the 90 listed`.

---

## 2. `repo-split-public-private` — **FAIL**

### 2.1 The regex damage, and what the diff accounts for

The task was to check whether the author's regex edit removed anything besides the clause that was
put back. I diffed the Statement word by word against the version REF-PASS-D reviewed
(`rigor/review_packet_d.md`, which is the card as D read it) and against `docs/data/extra-claim-map.json`
at `bbaa665`. **Eight changes, and every one is accounted for. Nothing else was dropped or mangled**
[E]:

| # | change | why |
|---|---|---|
| 1 | `project (614 files, 7.93 MB as of 2026-09-21; the figure moves with every commit:` → `project:` | D-R12, taken by dropping the figure rather than correcting it — the right half of the choice offered |
| 2 | `and the the result captures the KB cites as evidence)` → `and the 97 tracked .out run captures, 83 under numerics/ and 14 under rigor/, of which 23 are cited by a card as evidence (./pgit check prints the file count of each repository, and both move with every commit, so no figure is fixed here)` | D-R9, plus the replacement hedge for #1. The "the the" is gone |
| 3 | `48.4 MB as of 2026-09-21:` → `48.39 MB:` | more precise; measured below |
| 4 | the private enumeration gains the five compendia, `plan_page/petz_program_plan.html` and the `ls-files` rule | D-R10, verbatim in substance |
| 5 | `(196 MB)` → `(423 files, 198.6 MB)` | D-R11, and sharper than the `about 199 MB` D offered |
| 6 | `15 of the 28 head SHAs` → `15 of the head SHAs … a count that can only grow as runs accumulate` | D-R13, taken by deleting the denominator. **This is where the new defect is — E-D3** |
| 7 | the activity-endpoint and actor-timeline sentence added | D-R14, first half |
| 8 | the "AND THE ROUTE IS PUBLISHED IN THIS REPOSITORY" paragraph added | D-R14, second half. **This is where the other new defect is — E-D2** |

The only two deletions in the whole diff are the `614 files, 7.93 MB` parenthesis (#1, intended) and
the two words `the 28` (#6, intended). No third deletion, no mangled clause, no orphaned punctuation.
**The regex damage is properly repaired.**

### 2.2 The numbers, re-measured

All [E], at HEAD, by the rule named in each row.

| card says | measured |
|---|---|
| **97** tracked `.out` run captures | `git ls-files '*.out' \| wc -l` = **97** — exact |
| **83** under `numerics/`, **14** under `rigor/` | by first path component: numerics **83**, rigor **14**, nothing elsewhere; 83 + 14 = 97 — exact |
| **23** of them "cited by a card as evidence" | **23**, under this rule: a `doc:`/`num:`/`ref:` token, anchor stripped, naming a tracked `.out` file, anywhere in the 330 card files of `kb/projects/cft_cmi/{claims,areas,evidence}`. The same 23 come out of the front-matter `evidence:` key alone, and all 23 are tracked. All 23 are under `numerics/optimality_all/`. Two sensitivities worth knowing: restricted to `claims/` only it is **22** (5 come from `evidence/` cards, 4 of them shared); and **37** distinct `.out` files are named by bare path *somewhere* in a card, so "as evidence" is doing real work and the card does not say what the rule is |
| private `.git-private` **235 files, 48.39 MB** | `ls-files` **235**; 48,391,154 B = **48.39 MB** — exact |
| the private enumeration "which is exactly what `git --git-dir=.git-private ls-files` lists outside the first two directories" | outside `rigor/shots/` and `refs/` the private repo tracks exactly ten paths: `CHECKLIST.md`, `PRIVATE.md`, `pgit`, `pgit-exclude`, `plan_page/petz_program_plan.html`, `rigor/cited_R1..R4.tex`, `rigor/cited_results_all.tex` — the enumeration, and nothing else. `rigor/shots` **178**, `refs/*.pdf` **47**, `refs/` holds no non-PDF. 178 + 47 + 10 = **235** — exact |
| overlap **0** | `comm -12` over the two `ls-files` = **0**; `./pgit check` prints `overlap: 0` |
| "`./pgit check` prints the file count of each repository" | it does: `public : 618 files / private: 235 files / overlap: 0 / uncommitted: public 0, private 0 / shots on disk 178, tracked 178`, exit 0 |
| tracked by neither: **423 files, 198.6 MB** | **424** files / 198.8 MB right now, and the 424th is `rigor/review_packet_e.md`, the packet written for *this* review (158,366 B). Excluding it: **423 files, 198,647,442 B = 198.6 MB** — **exact** |
| **255** `\shot`/`\shotc` call sites in **19** documents | `\shotc?\s*[\[{]` over every `.tex` on disk: **256** in 20 files, one of which is the invocation inside the `\shotc` definition in `rigor_preamble.tex`; 256 − 1 = **255 in 19 documents** — exact |
| **24** python scripts resolving against a computed `_ROOT` | 25 tracked `.py` files mention `_ROOT`; the 25th is `tools/fix_paths.py`, the rewriter that inserts it. **24** scripts resolve against it — exact. No tracked `.py` still contains a `/Users/alex` literal |
| four shell scripts honour `$PYTHON` | `numerics/certified/runhp.sh`, `numerics/run_hp14.sh`, `numerics/run_largezeta.sh`, `numerics/run_largezeta2.sh` — **4** |
| "**620** distinct paths were ever added and none is an excerpt or a PDF" | the load-bearing half is exact: **0** of the paths ever added is under `rigor/shots/`, is a `refs/*.pdf`, or is a `cited_R*`/`cited_results_all` file. The count I get from the local history, which `git ls-remote` shows is byte-identical to the remote's refs, is **619** (`git log --all --no-renames --diff-filter=A --name-only`), not 620. Pre-existing, from REF-MOVE-1e's mirror clone, under a rule I cannot reproduce without cloning; non-blocking |
| **299,915** bytes | `GET /contents/rigor/cited_results_all.tex?ref=<discarded commit>` returns `size 299915`, blob `18cc05ab…`; the local private copy is **299,915** B; `git cat-file -t` on that commit fails locally — **exposure unchanged** |
| remote private, unforked, no other collaborators | `private true, fork false, forks_count 0`, collaborators **1** |
| tag and release | one tag `v0.1.0-draft` → `5ad78cb`, whose tree does contain `plan_page/petz_program_plan.html`; the release carries exactly `cft-cmi-paper1-free-fermion.pdf` and `cft-cmi-paper2-universality.pdf` |
| restore.sh recovers exactly one of the six under the cited name | `--list`: `arXiv VWZ (2307.14434)`; `MANUAL Uhlmann76 -- paywalled`; `arXiv CDIW21 (1808.02384)`, so the file lands as `CDIW21_…`, not `CDIT_…`; `BJL_twisted_duality`, `Sion1958_minimax` and `AlbertiUhlmann02` are bullet entries at `refs/REFERENCES.md:49-51`, not table rows — exact |
| NINE private targets cited by TEN cards | **9** targets, **10** distinct citing cards, counting `doc:`/`num:`/`ref:` tokens in `claims/`, `areas/` and `evidence/` with the anchor stripped — exact, and `PRIVATE.md:60` says the same |
| "the review packets the KB writes into `rigor/` are tracked by neither" | 22 on disk, **0** tracked publicly, **0** tracked privately — exact |

### 2.3 E-D2 — "four referee notes are public-tracked" is five, and the fifth is the note the same commit added

The Statement's new paragraph says:

> "AND THE ROUTE IS PUBLISHED IN THIS REPOSITORY: **four referee notes are public-tracked** and
> between them give the commit and blob SHAs, a one-line git show recipe and all three REST calls."

`next` says the same — "and **four** public-tracked referee notes publish the recovery route" — and
`CHECKLIST.md` item 3c, which is new in this commit, names them: `referee_compendia_move.md`,
`referee_plan_split.md`, `referee_pass_c.md`, `referee_repo_split.md`.

**`rigor/referee_pass_d.md` is a fifth, it is public-tracked, and `git log` says it entered the
public repository in `f7f3822` — the same commit that wrote the sentence and item 3c** [E]. It is not
a marginal fifth: it is the most complete of the five. In §3.3 and §3.4 it carries, in a quoted
table, the one-line `git show <discarded>^:rigor/cited_R1.tex` recipe with the byte count, the mirror
`git … fetch origin <discarded>` command, `gh api …/contents/rigor/cited_results_all.tex?ref=<discarded>`,
`gh api …/git/blobs/18cc05ab…`, `GET /repos/…/commits/<discarded>`, and the force-push row with
`before` and `after` at full forty characters. Ten of its hash tokens resolve to commits the rewrite
discarded.

So the one sentence of this card whose whole purpose is to bound the public exposure understates it,
in the Statement, in the field that ships verbatim to `docs/data/extra-claim-map.json`, and in the
evidence document the field points at. This is the same species as C12 and D-D2 and it is now the
third consecutive pass on this field.

### 2.4 E-D3 — two further public-tracked publishers of pre-rewrite hashes that no note has named, and a REST route wider than all three the card lists

Asked to look once more, I scanned **every** file `git ls-files` tracks — not the referee notes only —
for a `[0-9a-f]{7,40}` token whose seven-character prefix matches one of the 44 discarded commits I
derived from the three endpoints. **Seven public-tracked files hit** [E]:

| public-tracked file | hits | named by a note before? |
|---|---|---|
| `rigor/referee_plan_split.md` | 12 | yes |
| `rigor/referee_pass_d.md` | 10 | **no — E-D2** |
| `rigor/referee_build_repairs.md` | 6 | **no** |
| `rigor/referee_pass_c.md` | 6 | yes |
| `rigor/referee_compendia_move.md` | 3 | yes |
| `rigor/referee_repo_split.md` | 1 | yes |
| `rigor/referee_author_disclosure.md` | 1 | **no** |

`rigor/referee_build_repairs.md` names two discarded commits in its **title line** and gives
`git show <discarded>` and `<discarded>^` as recipes; `rigor/referee_author_disclosure.md` names one
in its title line. I confirmed by REST that all three still resolve on the remote and none resolves
locally [E]. They do not publish the compendia route, but they do publish the seeds, and a seed is
all the route needs.

**And the seed is enough for more than the card allows.** The Statement lists three publishers of
pre-rewrite hashes — the Actions run list (15), the events endpoint (44 across the push events) and
the activity endpoint (44 across 58 entries) — plus the actor's timeline (the same 44). There is a
fourth, and it is strictly the widest [E]: **`GET /repos/{owner}/{repo}/commits?sha=<any discarded
commit>`** walks the discarded history from that seed and returns **48** commits, **all 48** absent
from the local history, **4 of them published by none of the other endpoints**, each with its
message, author, date and tree SHA. One seed, one paginated call, the whole pre-rewrite history. The
three endpoints the card names hand out the seed; every one of the seven files above hands out the
seed; the activity feed's single `force_push` row hands out the best seed of all, labelled.

I am deliberately **not** writing a live seed SHA into this note, for the reason the card itself
gives. The route above can be reproduced from the `before` field of the one `force_push` row of
`GET /repos/{owner}/{repo}/activity`.

Nothing else about the exposure has moved: 299,915 bytes still served, blob `18cc05ab…`, repository
still private, unforked, one collaborator. **The exposure is unchanged in extent and has one more
route than any note has recorded.**

### 2.5 E-D4 — the hedge is attached to the one count that cannot grow, and two denominators beside it are already stale

The Statement now reads:

> "… and **15 of the head SHAs it serves are commits the rewrite discarded, a count that can only
> grow as runs accumulate**; the repository events endpoint publishes more still, 44 pre-rewrite
> commits across **53** push events, 29 of which were never a workflow head … the repository activity
> endpoint serves **58** entries …"

D-R13 asked for `15 of the 29 it currently lists` plus C-R14's clause "both counts grow with ordinary
use", where *both counts* were the two denominators. The author instead deleted the denominator and
moved the hedge onto the numerator. Measured [E]:

| | REF-PASS-C | REF-PASS-D | REF-PASS-E (now) |
|---|---|---|---|
| Actions runs served | 28 | 29 | **31** |
| of those, heads the rewrite discarded | **15** | **15** | **15** |

Three measurements, a denominator that grew twice, and a numerator that did not move once — and
cannot, because every run added since the rewrite has a post-rewrite head. "A count that can only
grow as runs accumulate" is true of the number the author deleted and false of the number it is now
attached to. This is the same failure as D-D1(ii): a qualifier carried across to the wrong noun
during a repair.

Two more in the same paragraph, both exact when written and both already stale, and both moved by the
two commits that carry the text [E]:

| card says | measured now |
|---|---|
| "**53** push events" | `/repos/…/events`: **55** PushEvents, 57 distinct SHAs |
| "44 pre-rewrite commits … 29 of which were never a workflow head" | **44** and **29** — exact |
| "the repository activity endpoint serves **58** entries of which one is the force-push" | **60** entries (58 `push`, 1 `branch_creation`, 1 `force_push`), 44 of the 60 distinct SHAs absent locally; the single `force_push` row and its `before`/`after` and timestamp are exactly as D recorded them — exact |
| "the actor's own events timeline carries the same 44" | `/users/<owner>/events`: 57 entries for this repository, 55 pushes, **44** absent locally — exact |
| "the generated site is clean (**352** distinct hex tokens under docs/, none resolving to a discarded commit)" | **355** distinct `[0-9a-f]{7,40}` tokens under `docs/` now, and **0** of them matches any of the 44 discarded commits. The substantive half is exact; the count moved with the regeneration in `85a2d4a` |

### 2.6 The `next` field, `CHECKLIST.md` 3, 3b, 3c and `PRIVATE.md`

`next` ships verbatim: I read it out of `docs/data/extra-claim-map.json` rather than the card and the
two agree word for word, modulo the generator's own `(held privately)` annotations [E]. The same is
true of the Statement.

| `next` says | document | verdict |
|---|---|---|
| "CHECKLIST.md item 3 records it" (the gating item) | item 3: "RESIDUAL, AND IT BLOCKS GOING PUBLIC: GitHub still serves the pre-rewrite objects by SHA … Clearing it needs a GitHub Support purge …, or the remote deleted and recreated" | **true**, and `PRIVATE.md:79-81` says the same ("Residual, and it blocks going public") |
| "recorded as CHECKLIST.md 3b": `plan_page/petz_program_plan.html` reachable in the public history and in the tree of the pushed tag `v0.1.0-draft` | item 3b says exactly that, and adds the initial-import SHA `03e2e48`. I checked both halves: `03e2e48` is the initial import of the post-rewrite history and touches that path, and `git ls-tree -r v0.1.0-draft` contains it | **true** |
| "recorded as CHECKLIST.md 3c": "four public-tracked referee notes publish the recovery route, so if the repository is ever published before the first item is cleared they must move to the private companion first" | item 3c says exactly that, in those words, and names the four | **the item says what `next` claims — and both are wrong by one, E-D2** |

Item 3b and item 3c are both new in this commit and both are real: this closes D-D2 and D-R8, which
asked for the second item to be recorded rather than asserted. The failure is not that the items are
missing; it is that item 3c was written from D's table of four and the fifth note landed in the same
commit.

One non-blocking mismatch carried from D-D2 and still not done: item 3 says only "the repository's own
**Actions** API publishes the pre-rewrite head SHAs", while the Statement and `next` now say Actions,
events, activity and the actor's timeline. Item 3 should gain them, and now also the commits-walk of
E-D3.

### 2.7 Exact repair

**E-R2 (blocking, E-D2).** In the Statement, replace

> "AND THE ROUTE IS PUBLISHED IN THIS REPOSITORY: four referee notes are public-tracked and between them give the commit and blob SHAs, a one-line git show recipe and all three REST calls."

with

> "AND THE ROUTE IS PUBLISHED IN THIS REPOSITORY: five referee notes are public-tracked and between them give the commit and blob SHAs, a one-line git show recipe and all three REST calls, and two further public-tracked notes publish a discarded commit SHA in their title line, so seven tracked files carry a usable seed; the count rises with every referee pass, since each new note is tracked publicly and records what it measured."

**E-R3 (blocking, E-D2).** In `next`, replace

> "and four public-tracked referee notes publish the recovery route, so if the repository is ever published before the first item is cleared they must move to the private companion first."

with

> "and seven public-tracked files carry a pre-rewrite commit SHA, five of them referee notes that give the recovery route in full, so if the repository is ever published before the first item is cleared they must all move to the private companion first; a referee pass adds one, so the list is checked rather than remembered."

**E-R4 (blocking, E-D2).** In `CHECKLIST.md` item 3c, replace the enumeration of four with the seven
measured above — `rigor/referee_plan_split.md`, `rigor/referee_pass_d.md`, `rigor/referee_pass_c.md`,
`rigor/referee_compendia_move.md`, `rigor/referee_repo_split.md`, `rigor/referee_build_repairs.md`,
`rigor/referee_author_disclosure.md` — and add the rule that produced it, so the next pass does not
have to rediscover it:

> "The list is not remembered, it is measured: `git ls-files | xargs grep -lE '\b[0-9a-f]{7,40}\b'` filtered to the SHAs that `GET /repos/OWNER/REPO/activity` reports and `git cat-file -t` does not resolve locally. Every referee pass adds one file to it."

**E-R5 (blocking, E-D4).** In the Statement, replace

> "and 15 of the head SHAs it serves are commits the rewrite discarded, a count that can only grow as runs accumulate"

with

> "and 15 of the head SHAs it serves are commits the rewrite discarded -- a numerator fixed by the rewrite, under a denominator that grows with every run (28, 29 and 31 at the last three passes)"

**E-R6 (repair in the same edit, E-D4).** `53 push events` → `55 push events as of 2026-09-21, one
per push`; `serves 58 entries` → `serves 60 entries`; `352 distinct hex tokens` → `355 distinct hex
tokens`. Or, better and stale-proof, follow the idiom this card already uses for the repository file
counts and write, once, after the activity clause: "all three feeds grow with ordinary use, so the
entry counts here are the measurement of 2026-09-21 and not a fixed figure; what does not move is the
44 pre-rewrite commits they publish and the 15 of them that were workflow heads."

**E-R7 (blocking-adjacent, E-D3).** Add to the Statement, after the activity clause:

> "A fourth route is wider than all three: /repos/OWNER/REPO/commits?sha= a single discarded SHA walks the whole discarded history and returns 48 commits with their messages and tree SHAs, four of which no feed lists. Every publisher above, and every public-tracked note, hands out that one seed."

**E-R8 (non-blocking).** State the rule behind the 23: "of which 23 are named by a card's evidence
token" is what is true and checkable; "cited by a card as evidence" reads as prose and 37 `.out` files
are named by a card somewhere.

**E-R9 (non-blocking).** One of the 14 tracked `.out` files under `rigor/` is not a run capture.
`rigor/_probe.out` is a LaTeX hyperref bookmark file (`\BOOKMARK [1][-]{section.1}{…}`), a build
product of a `_probe.tex` that is neither on disk nor tracked; the other 96 are genuine captures, and
it is the only one of the 97 that is not. Either untrack it or write "97 tracked `.out` files, 96 of
them run captures".

**E-R10 (non-blocking).** In `CHECKLIST.md` item 3, "the repository's own Actions API publishes the
pre-rewrite head SHAs" → "the repository's Actions, events and activity endpoints and the owner's
event timeline publish the pre-rewrite head SHAs, and a single one of them seeds a walk of the whole
discarded history".

**E-R11 (non-blocking, wording only).** "(./pgit check prints the file count of each repository, and
both move with every commit, so no figure is fixed here)" sits immediately after four figures that
*are* fixed there — 97, 83, 14 and 23 — and immediately before two more, 235 and 48.39 MB. The
intended reading is "no repository file count is fixed here". Worth two words: "so neither of those
two is fixed here".

---

## 3. The gates, run by me

`make check` — **exit 0** on a clean tree at HEAD [E]:

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
      refs/Sion1958_minimax.pdf, refs/BJL_twisted_duality_math-ph-0204029.pdf,
      refs/AlbertiUhlmann02_math-ph-0202038.pdf, refs/CDIT_1808.02384.pdf,
      plan_page/petz_program_plan.html, PRIVATE.md, CHECKLIST.md,
      refs/Uhlmann76.pdf, refs/VWZ_2307.14434.pdf
  cards never refereed: 0 of the 90 listed (0 with a page); 232 of the 322 cards in the
             whole knowledge base, the rest being findings that reach no displayed status
  cards awaiting a referee pass: 2 (generated-docs, repo-split-public-private)
  cards whose last referee pass failed: 0
ok  docs/data/quadratic-law.json … constants.json, theta.json, universality.json,
    networks.json, extra-separation.json, extra-off-criticality.json,
    extra-relative-entropy.json, extra-claim-map.json   (nine files)
  page record references: all resolve
```

`make rigor` — **exit 0**: `46 document(s), 0 failing, 0 known` (every one of the 46 printed `ok`).

`kb -p cft_cmi lint` — `0 issue(s), 2 awaiting review`, the two under review here.

This is the third consecutive pass at which both gates are green at HEAD.

I then ran both again **after** recording the two verdicts. `make rigor` is unchanged, exit 0.
`make check` is **exit 1**, and the whole drift is the review state the verdicts just moved:
`docs/status.md:23` and `docs/read/status.html:54` "**0 carry a failed referee pass**" → "**2**",
and the two table rows going `review pending` → `referee pass failed`. `check_links` still prints
`155 pages, 2211 links resolve`. That is rule (c) working as REF-DOCS-1c agreed, not a regression;
run `make docs data` and commit. The only file I added to the working tree is this one.

---

## 4. `tools/md_to_html.py` — a note, not a verdict

`docs-pages-rendering` is passed and is not in my packet, but `generated-docs` cites the generator
this file belongs to, so I read it. **The docstring is now true** [E]. Checked clause by clause
against the card and against the code:

* "a `.md` file with no YAML front matter is a static file and is served verbatim, with or without
  `docs/.nojekyll`" — matches the card; the false causality is gone.
* "the directory prefix of a relative link between two documentation pages is preserved and only the
  suffix changes" — matches the card and `make_link`; "the same string in both trees" is gone.
* "The subset is NOT closed … `reject_unsupported` is a blacklist … a guard and not a proof" —
  matches the card's capitalised sentence. "Nothing here guesses", "the subset is closed and small"
  and "A construct outside that subset raises `Unsupported`" are all gone.
* "a table's alignment row and every body row must carry the header's cell count and a closing bar" —
  matches `render_table`, alignment row included, as REF-PASS-D measured.
* "Emphasis is deliberately stricter than CommonMark. A run may open only after the start of a line
  or whitespace and close only before the end of a line, whitespace or punctuation" — matches the
  card, and it wisely omits the card's "with CommonMark's intraword rule kept for `_`", which D-R2
  showed describes dead code.

**One passage of D-R1 was not repaired.** D-R1 named four passages, three in the docstring and one
further down: the comment above `UNSUPPORTED_LINE`. At `tools/md_to_html.py:259-262` it still reads

```
# Constructs outside the subset.  None of them occurs in what build_docs.py emits
# today, and each would be rendered wrongly and in silence if one appeared, so each
# is a hard error instead.  This is what makes the subset closed: the paragraph
# branch is the fallback for PROSE, never for an unrecognised construct.
```

"This is what makes the subset closed" contradicts line 18 of the same file — "The subset is NOT
closed, and saying otherwise cost three referee passes" — and contradicts `docs-pages-rendering`.
Deleting that one sentence finishes D-R1. Also, the docstring's "Three link classes occur" is four in
`make_link`: a documentation page, a file elsewhere in the repository, a directory, and a non-`.md`
file inside `docs/`, which takes the `"../" + path` branch. Neither is a card claim and neither is
part of any verdict.

---

## 5. Consistency

`kb -p cft_cmi q --text` over *docs/read*, *compendia*, *Pages*, *mirror* and *pgit*, plus a grep of
every card for `compendia` and for `docs/read`. **No card contradicts either of these two.**
`docs-pages-rendering` and `generated-docs` now give the same inventory (65 + 66 = 131) and the same
description of the mirror. `PRIVATE.md:60-63` and the Statement agree on nine private targets cited
by ten cards; `PRIVATE.md:79-81` and `CHECKLIST.md` item 3 and the Statement agree that the residual
blocks going public. `ci-green`'s "49 `rigor/*.tex` on disk, 44 tracked, the 5 untracked `cited_R*`
compendia making the difference" still reproduces.

The one contradiction that remains is again inside `repo-split-public-private`, between the Statement,
its `next` field and `CHECKLIST.md` item 3c on one side and the contents of `git ls-files` on the
other — the same field as the last two passes, for the third different sentence.
