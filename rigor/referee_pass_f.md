# REF-PASS-F: sixth pass on generated-docs and repo-split-public-private (2026-09-21)

Scope: the two cards REF-PASS-E failed, against `referee_pass_e.md` and, behind it,
`referee_pass_d.md`, `referee_pass_c.md`, `referee_plan_split.md`, `referee_ci_pages.md` and
`referee_ci_pages_b.md`.

Verdicts: **`generated-docs` PASS, `repo-split-public-private` FAIL.**

Everything marked [M] is measured by me at HEAD = `0e9f168` (`git ls-remote` shows the remote's
`main` at the same commit). `git status --porcelain` was empty before I started and is empty now;
the four files I touched for the guard tests (`docs/index.md`, `docs/notation.md`,
`docs/read/results/gap-law.html`, and two planted orphans) were restored by file copy or removal and
the tree is clean. No git command that writes was run; the remote was probed by REST only and I did
not clone it. **This note deliberately contains no discarded commit SHA** — see §3.2.

The brief was that five consecutive passes have each found that a repair introduced a new defect, and
to look there first. **It happened again, in one of the two cards, and again in the sentence the
previous pass rewrote.** `generated-docs` is the exception: E-R1 is applied, every command it names
runs, and every figure it and the Statement assert is exact. In `repo-split-public-private` the two
verbatim repairs E-R2 and E-R6 are each correct in themselves and, between them, have left the
Statement saying **four** where it has just finished saying seven, and have cut a clause loose from
the sentence it qualified.

---

## 1. `generated-docs` — **PASS**

### 1.1 E-R1 is applied, and everything in the field is executable and true

The `## How to verify` field now reads (one wording change from E-R1, `tools/check_links.py` →
`check_links.py`, which changes nothing):

> "python3 tools/build_docs.py --check, or make check, which prints the page count, the claim tally,
> the privately held evidence pointers by name and the review state, and exits non-zero on any drift.
> That run prints the Statement's 131, the claim tally (90 listed, 30 proved, 3 refereed, 22
> numerical, 3 conjectural), pages under results/: 58, and the nine privately held pointers by name.
> The Statement's other figures are measured outside it, each in one command: 65 and 66 by git
> ls-files 'docs/\*.md' and git ls-files 'docs/read/\*.html'; 783 internal link targets by a scan of
> the 65 sources (check_links.py's own totals, 155 pages and 2211 links, are over the whole site and
> are a different corpus); 36 source rows by grep -c '^|' refs/REFERENCES.md less the header and
> alignment rows; 20 fetchable by bash refs/restore.sh --list; and 6 pointers on 7 bullets across 6
> pages by grep -c 'held privately' docs/results/\*.md. To test the guard itself, change a byte in
> docs/index.md, delete a page under docs/read/, or plant an orphan under docs/read/results/: each is
> reported, and restoring it returns the run to '131 pages up to date'."

E-D1's false sentence is gone. I ran every command the field names [M]:

| # | command as written | result | Statement's figure |
|---|---|---|---|
| 1 | `python3 tools/build_docs.py --check` | `131 pages up to date`, exit 0 | 131 ✓ |
| 2 | `make check` | same plus `155 pages, 2211 links resolve` and the nine `ok` data files, exit 0 | ✓ |
| 3 | `git ls-files 'docs/*.md'` | **65**, of which 7 at top level and exactly the seven named (index, status, notation, definitions, open, sources, history) | 65, 7 ✓ |
| 4 | `git ls-files 'docs/read/*.html'` | **66** = 7 top level + 59 under `read/results/`, the 59th the generated index | 66, 7, 58, +1 ✓ |
| 5 | a scan of the 65 sources for `[text](target)` | **783** targets, **0** external, **0** dead, **0** at an untracked file, **0** missing anchors (2 targets are the directory `results/`) | 783 / 0 / 0 / 0 ✓ |
| 6 | `grep -c '^|' refs/REFERENCES.md` | **38**, less header and alignment = **36** | 36 ✓ |
| 7 | `bash refs/restore.sh --list` | ends `20 fetchable, 16 need library access` | 20 ✓ |
| 8 | `grep -c 'held privately' docs/results/*.md` | 58 lines, **6** of them non-zero, summing to **7**; the 7 bullets name **6** distinct targets, all six PDFs | 6 / 7 / 6 ✓ |
| 9 | guard: byte appended to `docs/index.md` | `differs index.md`, exit 1 | ✓ |
| 10 | guard: `docs/read/results/gap-law.html` deleted | `missing read/results/gap-law.html`, exit 1 | ✓ |
| 11 | guard: orphan planted at `docs/read/results/` | `stale … (no claim generates it any more)`, exit 1 | ✓ |
| — | each of 9–11 restored | `131 pages up to date`, exit 0 | ✓ |

Row 5 is the one item of the list that is not literally a command — "a scan of the 65 sources" is a
description, and a reader has to write the scan. It reproduces the figure exactly (mine is a
`(?<!\\)\[…\]\(…\)` match over `git ls-files 'docs/*.md'`, which gives 783 directly, where REF-PASS-E's
looser pattern gave 786 less three LaTeX artefacts). "Each in one command" is therefore true of four
of the five items and generous about the fifth. That is the only thing I would have written
differently in the whole field, and it is not a false statement.

Row 8 deserves one sentence in the author's defence and one against: the command prints a line for
every one of the 58 pages, most of them `:0`, so the reader filters; but the three figures the field
claims (6 pages, 7 bullets, 6 distinct targets) are all readable off its output.

### 1.2 The Statement, re-measured rather than read [M]

| claim | measurement |
|---|---|
| 131 files, 65 + 66 | `git ls-files` 65 `.md` + 66 `.html`, all tracked, 0 untracked under `docs/`; the run says 131 |
| one page per card at proved/refereed/numerical/conjectural, 58 of them | I took the status of all 330 card files: **58** qualify, **58** pages exist, **0** qualifying cards without a page and **0** pages without a qualifying card |
| 30 proved, 3 refereed, 22 numerical, 3 conjectural of 90 | my own count of the qualifying cards is exactly 30 / 3 / 22 / 3; the run prints `claims 90 (…)` |
| "REF-DOCS-1 verified all 58 result pages byte-faithful … 0 problems in 58" | re-done independently at word granularity: for all **58** pages the Statement and the How-to-verify match the card word for word, **0** differences; **292** evidence and related tokens all rendered; every page's badge is its card's own status |
| 783 internal links, 0 dead / 0 untracked / 0 missing anchors | as row 5 above |
| DETECTED 9, printed by name on every run | the run prints nine and names them; 6 PDFs + `plan_page/petz_program_plan.html` + `PRIVATE.md` + `CHECKLIST.md` |
| RENDERED 6, on 7 bullets across 6 pages | the seven bullets are on `all-channels-symbol-feasible`, `all-channel-equals-quasi-free`, `single-observable-bound`, `implementer-hypotheses`, `sequential-recovery-bound-type-iii` (twice) and `vwz-protocol-ordering`; 6 distinct targets, all six PDFs |
| "the other three are cited only by cards that reach no displayed status" | `CHECKLIST.md`/`PRIVATE.md` ← `repo-split-public-private`; `petz_program_plan.html` ← `plan-page`, `open-problems-plan-note8`, `repo-split-public-private`; all three `status: active`, none with a page |
| "a card never refereed is marked in four places, tested on a temporary knowledge-base copy with the review field stripped" | **re-done, not accepted** (REF-PASS-E did not rebuild it): I copied the KB to a scratchpad, deleted the `review:` line of `gap-law`, and built with `--kb <copy> --docs <scratch>`. Four places, exactly: the result page's `Review record: never refereed`, the `status.md` row, the `status.md` count sentence (`**1 has never been refereed**`) and the `index.md` list entry. The run also reports `cards never refereed: 1 of the 90 listed (1 with a page)` |
| the guard "fails on … a changed card, and now also on an orphan top-level page" | changed card: `--check` against that same modified KB copy → `differs index.md`, exit 1. Top-level orphan: planted `docs/zzz_f_orphan.md` → `stale zzz_f_orphan.md … (top level: delete it by hand)`, exit 1 |
| "it reports rather than hides pages skipped by the hand-edit marker" | flipping `notation.md`'s banner to `<!-- hand-edited: yes -->` gives `130 pages up to date`, then `NOT CHECKED, marked hand-edited: notation.md` and "a hand-edited page is never compared, so it can go stale silently", exit 0. (`hand_edited()` reads only the first 20 lines, which is what the banner tells a human to edit; a marker appended at the foot of the file is correctly not honoured and the page simply `differs`) |
| the three admissions on the pages | `docs/sources.md:5` opens with the **guess** admission in bold and names `DaleckiiKrein` and `Petz96`; `notation.md` and `definitions.md` both open with "assembled mechanically … there is no curated symbol table yet"; `history.md:5` says "The lead of every entry of those status files is reproduced below" |
| rule (a), the three conditional pages | unchanged since REF-PASS-E and re-read: H1–H3, (H) and (U) each under `## Hypotheses` with `**Conditional.**` |

### 1.3 Why this is a PASS

Nothing in the card is false, missing or contradicted by its own evidence. The one substantive item
left open is E-N1, which REF-PASS-E already declared non-blocking and which is unchanged: the
Statement's drift-guard sentence still enumerates only the Markdown breakages ("a changed byte, a
stale results page, a deleted results page and a changed card, and now also on an orphan top-level
page") and never names `docs/read/`, while "All 131 are inside the drift guard" three sentences
earlier carries that load — and I retested that `--check` does cover `read/` recursively. One clause
would end it, and I would have written it; it is not a defect.

**F-N1 (non-blocking, wording).** In the drift-guard sentence, "a changed byte, a stale results page,
a deleted results page and a changed card, and now also on an orphan top-level page" → "…and now also
on an orphan top-level page, and the same four failures under docs/read/, an orphan there included at
any depth".

**F-N2 (non-blocking, wording).** "each in one command" in How-to-verify covers four commands and one
scan; either say "each by one command or one short scan" or give the scan.

---

## 2. `repo-split-public-private` — **FAIL**

### 2.1 What the repairs did, accounted for change by change

I word-diffed the Statement against the version REF-PASS-E reviewed (`rigor/review_packet_e.md`) and
against `docs/data/extra-claim-map.json` [M]. **Eight changes, no deletion that was not asked for, no
mangled clause.** Every one of E-R2 … E-R11 is applied:

| repair | applied? | true today? |
|---|---|---|
| E-R2 five notes / seven tracked files | verbatim | **yes** — §2.2 |
| E-R3 the same in `next` | verbatim | **yes** |
| E-R4 CHECKLIST 3c rewritten with the seven and the rule | yes, and more than asked | **list yes, two faults** — §2.3 |
| E-R5 numerator fixed, denominator grows (28, 29, 31) | verbatim | **yes** — §2.4 |
| E-R6 53→55, 58→60, 352→355 *and* the stale-proof sentence | both halves taken | **yes, but the splice broke a clause** — §2.5 |
| E-R7 the `commits?sha=` walk | yes, reworded | **yes, 48 and 4 confirmed** — §2.4 |
| E-R8 the evidence-token rule behind the 23 | yes | **yes**, 23 [M] |
| E-R9 `rigor/_probe.out` is not a run capture | yes, "96 of them run captures and one (rigor/_probe.out) a stray LaTeX bookmark file" | **yes** — the file begins `\BOOKMARK [1][-]{section.1}{…}` |
| E-R10 CHECKLIST item 3 credits all the publishers | yes, including the walk | **yes** |
| E-R11 "so neither of those two counts is fixed here" | yes | **yes** |

### 2.2 The seven leaking files are still exactly seven, and my predecessor's note is not one of them

The task put to me was that `rigor/referee_pass_e.md` is now public-tracked and may have made the
count stale on the day it was written. **It has not** [M].

`rigor/referee_pass_e.md` is tracked publicly and entered in `0e9f168`, the same commit that wrote
the seven-file list. Its only hex tokens are `03e2e48`, `5ad78cb`, `85a2d4a`, `bbaa665`, `f7f3822`
(all of which resolve locally), the two arXiv fragments `0202038`/`0204029`, and the **eight**-character
blob prefix `18cc05ab…`. That last one is the interesting case, and it is not a leak: the blobs
endpoint answers a truncated SHA with `422 The sha parameter must be exactly 40 characters and
contain only [0-9a-f]`. REF-PASS-E's "I deliberately did not write a live seed SHA into this note"
is exact, and its note is therefore not an eighth file.

Independently re-derived, not read off the card: I took the 48 discarded commits (§2.4), reduced them
to seven-character prefixes, and scanned every one of the 619 tracked files. **Seven files hit, and
they are the seven the card and CHECKLIST 3c name** — `referee_plan_split.md`, `referee_pass_d.md`,
`referee_build_repairs.md`, `referee_pass_c.md`, `referee_compendia_move.md`, `referee_repo_split.md`,
`referee_author_disclosure.md`. The two title-line claims hold: `referee_build_repairs.md` is headed
"Referee report — build repairs in `<discarded>` (REF-BUILD-1 / 1b, 2026-09-21)" and
`referee_author_disclosure.md` "REF-AUTHOR-1 — author block and AI-use disclosure (`<discarded>`),
2026-09-21".

Three **full forty-character** tokens exist in the tracked tree, all absent locally: one discarded
commit, in `referee_pass_c.md` and `referee_plan_split.md`; the compendium blob, in the same two
files (and it still answers: `GET /git/blobs/<40 chars>` returns `size 299915`, the exact size of the
local private `rigor/cited_results_all.tex`); and the force-push `before`, in `referee_pass_d.md`.
All three files are already on the list, so "seven tracked files carry a usable seed" survives the
sharper test.

**So the card's seven and CHECKLIST 3c's seven are correct today, and I am not failing anything for a
number that moved.** What I am failing is a number that did not move and should have: see §2.3.

One consequence the author should notice, because it is the opposite of what the card predicts: the
count **did not rise** with the fifth pass, and it does not rise with this one either.

### 2.3 F-D1 — the Statement still says FOUR where it has just said seven, and so does CHECKLIST 3c

This is the defect the repair introduced, and it is in both places the repair touched.

The Statement, in one paragraph [M]:

> "… **five referee notes are public-tracked** and between them give the commit and blob SHAs, a
> one-line git show recipe and all three REST calls, and two further public-tracked notes publish a
> discarded commit SHA in their title line, so **seven tracked files** carry a usable seed …
> The generated site is clean (355 distinct hex tokens under docs/, none resolving to a discarded
> commit). All three feeds grow with ordinary use, … and the 15 of them that were workflow heads, but
> the notes are not, so the ORDER matters: clearing the exposure first makes the recipes inert;
> **publishing first would require moving those four notes to the private companion**, which is the
> only option since a referee note is never edited."

E-R2 corrected the antecedent from four to five-plus-two-equals-seven and left the back-reference two
sentences later at four. The one sentence of this card that says *what to do before publishing* now
names three files fewer than the sentence that counts them, and the three it drops include
`referee_pass_d.md`, which REF-PASS-E called the most complete recovery recipe of the set, and
`referee_build_repairs.md`, which carries a seed in its title. It is false, it is contradicted by its
own paragraph, and it contradicts this card's own `next` field, which says "they must **all** move".
It ships: `docs/data/extra-claim-map.json` carries the string `those four notes` once, and
`they must all move` once, in the same record [M].

`CHECKLIST.md` item 3c has the identical fault, in the item the same commit wrote:

> "**Seven public-tracked files carry a pre-rewrite commit SHA**, five of them referee notes … the
> other two … name a discarded commit in their title line … If the repository is ever published
> before item 3 is cleared, **these four** must move to the private companion first."

The heading counts seven, the enumeration lists seven, the instruction moves four.

This is the sixth consecutive pass on which the operative sentence of this field is wrong by a
count, and the third in which a repair carried a qualifier or a back-reference to the wrong noun
(D-D1(ii), E-D4, now this).

### 2.4 The exposure, re-measured in full [M]

Nothing here is a defect; it is the check the task asked for, and it also settles the `commits?sha=`
clause.

| card says | measured now |
|---|---|
| Actions run list: "15 of the head SHAs it serves are commits the rewrite discarded — a numerator fixed by the rewrite, under a denominator that grows with every run (28, 29 and 31 at the last three passes)" | runs served **32** (C 28, D 29, E 31, F 32); discarded heads among them **15**, for the fourth measurement running. E-R5 is exactly right, and my own pass is a fourth confirmation of it |
| "44 pre-rewrite commits across 55 push events as of 2026-09-21, one per push, 29 of which were never a workflow head" | `/events`: **55** PushEvents, 55 distinct SHAs, **44** absent locally; 44 − 15 = **29** never a workflow head, and all 15 run heads are inside the 44 — exact |
| "the repository activity endpoint serves 60 entries of which one is the force-push itself, labelled and timestamped" | **61** entries now (59 `push`, 1 `branch_creation`, 1 `force_push`), the single labelled `force_push` row unchanged. 60 → 61 within the same day. **Not a defect:** the card's own next sentence says the entry counts "are the measurement of 2026-09-21 and not fixed figures", and the two figures it declares fixed, 44 and 15, are exact |
| "the actor's own events timeline carries the same 44" | `/users/<owner>/events`: 57 entries for this repository, 55 pushes, **44** absent locally — exact |
| "A fourth REST route … /repos/OWNER/REPO/commits?sha= a single discarded SHA walks the whole discarded history and returns **48** commits with their messages and tree SHAs, **four** of which no feed lists" | **48** commits returned from one seed, **all 48** absent from the local history, each carrying `commit.message`, `commit.tree.sha`, author and date. Against the union of *all four* publishers the card names — Actions runs, `/events`, `/activity` and the actor's timeline — **exactly 4** of the 48 are published by none of them. Both figures exact |
| "The generated site is clean (355 distinct hex tokens under docs/, none resolving to a discarded commit)" | **355** distinct `[0-9a-f]{7,40}` tokens under `docs/`, **0** matching any of the 48 — exact |
| "299,915 bytes", exposure unchanged | `GET /contents/rigor/cited_results_all.tex?ref=<discarded>` and `GET /git/blobs/<40>` both report `size 299915`; the local private copy is 299,915 B; the seed does not resolve locally |
| "the repository has never been public, is unforked and has no other collaborators" | `private true`, `fork false`, `forks_count 0`, collaborators **1** |
| tag, release, `plan_page/petz_program_plan.html` | one tag `v0.1.0-draft` → `5ad78cb`, whose tree contains that path; `03e2e48` touches it; the release carries exactly the two paper PDFs |
| "620 distinct paths were ever added and none is an excerpt or a PDF" | **620** now, exactly (`git log --all --no-renames --diff-filter=A --name-only`), REF-PASS-E's 619 plus `rigor/referee_pass_e.md` added in `0e9f168`. The load-bearing half is unchanged: 0 excerpts, 0 `refs/*.pdf`, 0 compendia ever added |

### 2.5 F-D2 — the stale-proof sentence was spliced into the middle of another one

E-R6's sentence was inserted between `…none resolving to a discarded commit)` and `, but the notes
are not`, and the comma became a full stop. The clause "but the notes are not" was the contrast to
"The generated site is clean"; it now follows "what does not move is the 44 pre-rewrite commits they
publish and the 15 of them that were workflow heads", so on the page it reads as "the notes are not
[what does not move]" — which is true, vacuous, and not what the sentence is for. The reader who needs
the point ("the site carries no seed, the notes do") no longer gets it, and the ORDER clause that
depends on it now hangs off the wrong subject. Same species as D-D1(ii) and E-D4; repaired together
with F-D1 by F-R1 below.

### 2.6 F-D3 — "the count rises with every referee pass" is false, and its own next instance refutes it

E-R2's closing clause, applied verbatim, is "the count rises with every referee pass, since each new
note is tracked publicly and records what it measured", and CHECKLIST 3c hardens it to "EVERY REFEREE
PASS ADDS ONE, so re-measure rather than trust this list". Measured [M]: the fifth pass added
`rigor/referee_pass_e.md` to the public repository and the count stayed at **seven**, because that
note quotes no discarded SHA; this note adds none either. The reason the clause gives — that a
referee note is tracked publicly and records what it measured — does not entail that it carries a
seed, and two consecutive notes now show it does not.

The error is conservative, unlike F-D1, and on its own I would have let it stand as wording. It is in
the repair list because the same edit fixes it and because a checklist that over-warns in capitals is
the one the next author stops reading.

### 2.7 The `next` field, CHECKLIST 3 / 3b / 3c and PRIVATE.md: mutual agreement

`next` ships verbatim; I read it out of `docs/data/extra-claim-map.json` rather than the card and the
two agree word for word [M].

| `next` says | the document | verdict |
|---|---|---|
| "CHECKLIST.md item 3 records it" (the gating residual) | item 3: "RESIDUAL, AND IT BLOCKS GOING PUBLIC: GitHub still serves the pre-rewrite objects by SHA … Clearing it needs a GitHub Support purge …, or the remote deleted and recreated" | **true**, and E-R10 is applied: item 3 now credits "the repository's Actions, events and activity endpoints and the owner's event timeline … and a single one of them seeds a walk of the whole discarded history" |
| "recorded as CHECKLIST.md 3b": `plan_page/petz_program_plan.html` reachable in the public history and in the tree of the tag | 3b says exactly that and names the initial import `03e2e48`; both halves re-verified | **true** |
| "recorded as CHECKLIST.md 3c": seven public-tracked files, five of them referee notes, "they must **all** move … a referee pass adds one, so the list is checked rather than remembered" | 3c's heading, enumeration and measuring rule match; its closing instruction says "these **four** must move" | **the item says what `next` claims, except on the one line that matters — F-D1** |
| Statement ↔ `next` | Statement: "moving those **four** notes"; `next`: "they must **all** move" | **they contradict each other**, and both ship |
| PRIVATE.md | `PRIVATE.md:60-63` agrees on nine files cited by ten cards and on `restore.sh` not being a substitute; `PRIVATE.md:79-81` agrees with item 3 and the Statement that the residual blocks going public. It says nothing about the seven notes, and the card does not claim it does | **consistent** |

### 2.8 CHECKLIST 3c's measuring command does not reproduce its own list

Asked for explicitly, so here it is in full. 3c says:

> "The list is not remembered, it is measured: `git ls-files | xargs grep -lE '\b[0-9a-f]{7,40}\b'`,
> filtered to the SHAs that `GET /repos/OWNER/REPO/activity` reports and `git cat-file -t` does not
> resolve locally."

Run verbatim at HEAD [M]: it completes cleanly, exit 0, no stderr. 619 tracked files, **no filename
contains a space**, so the `xargs` word-splitting hazard is not live here; `xargs` batches the list
and `grep -l` behaves identically per batch. `\b` is honoured by both greps on this machine (the
`grep` on PATH is ugrep 7.8.4, and `/usr/bin/grep`, BSD grep 2.6.0-FreeBSD, gives the identical
answer), so there is no portability defect either.

**It returns 215 files, not seven**, and the filter the sentence names cannot be applied to that
output, because `grep -l` prints filenames and throws away the tokens the filter needs. The seven are
among the 215, so the recipe is a correct first step described as if it were the whole thing.

I built and ran a two-step version that does reproduce the list exactly [M] — seven files, the seven
named — and offer it as F-R4.

### 2.9 Everything else in the Statement, re-measured [M]

| card says | measured |
|---|---|
| 97 tracked `.out`, 83 under `numerics/`, 14 under `rigor/`, 96 captures + `rigor/_probe.out` | 97 / 83 / 14, and `_probe.out` is a hyperref bookmark file — exact |
| "of which 23 are named by a card's evidence token" | **23**, over the 330 card files of `claims/`, `areas/` and `evidence/`; the same 23 come out of the front-matter `evidence:` key alone; all 23 tracked, all under `numerics/optimality_all/` — exact, and the rule is now stated |
| private repo 235 files, 48.39 MB, and the ten paths outside `rigor/shots` and `refs` | 235 files; 178 + 47 + the ten enumerated paths = 235; 48,391,681 B = **48.39 MB** — exact |
| overlap 0; "`./pgit check` prints the file count of each repository" | `public : 619 files / private: 235 files / overlap: 0 / uncommitted: public 0, private 0 / shots on disk 178, tracked 178`, exit 0 |
| "255 call sites in 19 documents" | 256 `\shot`/`\shotc` invocations in 20 `.tex`, less the one inside the definition in `rigor_preamble.tex` = **255 in 19** — exact |
| "the 24 python scripts … resolve paths against a computed `_ROOT` (37 literals)" | 25 tracked `.py` mention `_ROOT`, the 25th being the rewriter `tools/fix_paths.py`, so **24**; **0** tracked `.py` still holds a `/Users/alex` literal; and the **37** — which no pass had checked — reproduces: 37 `_ROOT`-rooted path expressions across those 24 files |
| "the four shell scripts … honour `$PYTHON`" | `numerics/certified/runhp.sh`, `numerics/run_hp14.sh`, `numerics/run_largezeta.sh`, `numerics/run_largezeta2.sh` — 4 |
| "NINE targets … cited by TEN cards" | 9 targets, 10 distinct citing cards, listed to my satisfaction; `PRIVATE.md:60` says the same |
| restore.sh recovers exactly one of the six under the cited name | `--list`: VWZ as `arXiv`, `Uhlmann76` MANUAL paywalled, CDIT tabled as `CDIW21`, and BJL / Sion1958 / AlbertiUhlmann02 are bullet entries at `REFERENCES.md:49-51`, not table rows — exact |
| "the review packets the KB writes into rigor/ are tracked by neither" | 23 on disk, 0 tracked publicly, 0 privately — exact |
| licensing, `THIRD-PARTY.md`, `rigor/README_AGENTS.md` section | `LICENSE-CODE` MIT, `LICENSE-DOCS` CC BY 4.0, `THIRD-PARTY.md` present, `README_AGENTS.md:36` heads "Two repositories over one work tree (2026-09-20)" |
| "the files tracked by neither are regenerable build products and caches (**423 files, 198.6 MB**)" | **425 files, 199.0 MB** now. The two extra are `rigor/review_packet_e.md` and `rigor/review_packet_f.md`, the packets the KB wrote for the fifth and sixth reviews. The figure was exact when written and moves by one per review — the very mechanism this card's own last paragraph names. Non-blocking; F-R5 offers the hedge the card already uses twice elsewhere |

### 2.10 Exact repairs

**F-R1 (blocking, F-D1 and F-D2 together).** In the Statement, replace

> "The generated site is clean (355 distinct hex tokens under docs/, none resolving to a discarded commit). All three feeds grow with ordinary use, so the entry counts here are the measurement of 2026-09-21 and not fixed figures; what does not move is the 44 pre-rewrite commits they publish and the 15 of them that were workflow heads, but the notes are not, so the ORDER matters: clearing the exposure first makes the recipes inert; publishing first would require moving those four notes to the private companion, which is the only option since a referee note is never edited."

with

> "The generated site is clean (355 distinct hex tokens under docs/, none resolving to a discarded commit), but those seven tracked files are not, so the ORDER matters: clearing the exposure first makes the recipes inert; publishing first would require moving all seven to the private companion, which is the only option since a referee note is never edited. All three feeds grow with ordinary use, so the entry counts here are the measurement of 2026-09-21 and not fixed figures; what does not move is the 44 pre-rewrite commits they publish and the 15 of them that were workflow heads."

That restores the contrast E-R6's insertion cut in half, keeps E-R6's hedge where it belongs (on the
feed counts it qualifies), and makes the instruction agree with the count and with `next`.

**F-R2 (blocking, F-D1).** In `CHECKLIST.md` item 3c, replace

> "If the repository is ever published before item 3 is cleared, these four must move to the private companion first."

with

> "If the repository is ever published before item 3 is cleared, all seven must move to the private companion first."

**F-R3 (blocking, F-D3).** In the Statement, replace

> "the count rises with every referee pass, since each new note is tracked publicly and records what it measured"

with

> "the list is re-measured at each pass rather than remembered, since any new note that quotes a discarded SHA joins it"

and in `CHECKLIST.md` item 3c replace

> "EVERY REFEREE PASS ADDS ONE, so re-measure rather than trust this list."

with

> "ANY PASS CAN ADD ONE, so re-measure rather than trust this list; the notes for the fifth and sixth passes deliberately quote no discarded SHA and added none."

The same clause in `next` ("a referee pass adds one, so the list is checked rather than remembered")
should become "any pass can add one, so the list is checked rather than remembered".

**F-R4 (non-blocking, §2.8).** In `CHECKLIST.md` item 3c, replace the measuring recipe with one that
reproduces the list. Tested by me at HEAD, and it returns exactly the seven files:

> "The list is not remembered, it is measured — but `grep -l` throws the tokens away, so take the SHAs first:
>
>     gh api /repos/OWNER/REPO/activity --paginate -q '.[].before, .[].after' | sort -u \
>       | while read -r s; do git cat-file -t "$s" >/dev/null 2>&1 || echo "$s"; done \
>       | grep -v '^0*$' > /tmp/discarded          # 44 of them on 2026-09-21
>     git ls-files | xargs grep -lE "$(cut -c1-7 /tmp/discarded | paste -sd'|' -)"
>
> The bare scan `git ls-files | xargs grep -lE '\b[0-9a-f]{7,40}\b'` is only the candidate set: it
> returns 215 of the 619 tracked files."

**F-R5 (non-blocking, the untracked count).** "(423 files, 198.6 MB)" → "(423 files, 198.6 MB on
2026-09-21; the KB writes one review packet per review into rigor/ and they are tracked by neither,
so this count rises by one per review)".

**F-R6 (non-blocking, wording).** "(28, 29 and 31 at the last three passes)" is a record of what three
named passes measured, and a fourth has now measured 32. Either write "(28, 29, 31 and 32 at passes
C, D, E and F)" or drop the parenthesis: the sentence's point is that the numerator is fixed, and
that is now confirmed four times.

---

## 3. The gates, run by me

### 3.1 Exactly what they print

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
  cards awaiting a referee pass: 2 (generated-docs, repo-split-public-private)
  cards whose last referee pass failed: 0
ok       docs/data/quadratic-law.json … constants.json, theta.json, universality.json,
         networks.json, extra-separation.json, extra-off-criticality.json,
         extra-relative-entropy.json, extra-claim-map.json   (nine files)
  page record references: all resolve
```

`make rigor` (`python3 tools/check_rigor_builds.py`) — **exit 0**, every document `ok`, closing with
`46 document(s), 0 failing, 0 known`.

`kb -p cft_cmi lint` — `0 issue(s), 2 awaiting review`, the two under review here.

This is the fourth consecutive pass at which both gates are green at HEAD.

I then ran `make check` again **after** recording the two verdicts, as at the last three passes. It is
**exit 2**, and the whole drift is the review state the verdicts just moved [M]: `status.md` and
`read/status.html` at "**0 carry a failed referee pass**" → "**1 carries a failed referee pass**", and
the two table rows going `review pending` → blank (passed) and `referee pass failed`. `check_links`
still prints `155 pages, 2211 links resolve`, and `make rigor` is unchanged at exit 0. That is rule
(c) working as REF-DOCS-1c agreed, not a regression; run `make docs data` and commit. The only file I
added to the working tree is this one.

### 3.2 A word on this note

`rigor/referee_pass_f.md` will be tracked publicly the moment it is committed, like its five
predecessors. It contains no discarded commit SHA, no full blob SHA and no `before` field, and the
recipe in F-R4 derives its seeds at run time instead of quoting them, so committing it leaves the
count at seven. That is a property of how the note was written, not a law about referee notes — which
is the whole of F-D3.

---

## 4. `tools/md_to_html.py:259-262` — a note, not a verdict

The comment above `UNSUPPORTED_LINE`, the one passage of D-R1 that REF-PASS-E found unrepaired, has
been rewritten and now reads:

```
# Constructs outside the subset.  None of them occurs in what build_docs.py emits
# today, and each would be rendered wrongly and in silence if one appeared, so each
# is a hard error instead.  This does NOT close the subset: it is a blacklist, so it
# makes the constructs it names loud and leaves the rest silent.  The paragraph
# branch is still the fallback for anything unrecognised, which is why the table
# invariant in render_table() is checked structurally instead of by pattern.
```

**True on every clause, and consistent both ways** [M]:

* "This does NOT close the subset: it is a blacklist" matches line 18 of the same file ("The subset
  is NOT closed, and saying otherwise cost three referee passes") and the capitalised sentence of
  `docs-pages-rendering` ("THE SUBSET IS NOT CLOSED … reject_unsupported() is a BLACKLIST").
* "The paragraph branch is still the fallback for anything unrecognised" is what the code does:
  `blocks()` falls through to `yield ("paragraph", …)` for any run of non-blank lines that starts no
  recognised block, and only an indented code block raises there. The previous text asserted the
  opposite ("never for an unrecognised construct"); that contradiction is gone.
* "which is why the table invariant in render_table() is checked structurally instead of by pattern"
  matches `render_table`, which raises on a cell-count mismatch and on a row without a closing pipe,
  and matches the docstring's "One property is structural rather than pattern-matched".
* "None of them occurs in what build_docs.py emits today" is consistent with a full regeneration:
  `--check` rebuilds all 131 pages and raises nothing.

D-R1 is therefore finished. The one inaccuracy left in the file is the docstring's "Three link
classes occur", which is four in `make_link` (the fourth being a non-`.md` file inside `docs/`, which
takes the `"../" + path` branch) — REF-PASS-E named it, it is not a card claim, and `docs-pages-rendering`
itself says "Three link classes … A fourth, per page and by design".

---

## 5. Consistency

`kb -p cft_cmi q --text` over *docs/read*, *compendia*, *pgit*, *private repository*, *history
rewrite*, *GitHub Pages* and *drift guard*, plus a grep of every card for `public-tracked`, `423
files` and `198.6 MB`. **No card contradicts either of these two.** `generated-docs` and
`docs-pages-rendering` give the same inventory (65 + 66 = 131) and the same account of the mirror;
`repo-split-public-private` is the only card that speaks about the split, the rewrite or the residual,
and `ci-green`, `public-site-plan`, `paper1-status` and `paper2-status` say nothing that conflicts
with it. Both cards' `related:` targets exist (`rigor-pipeline`, `numerics-stack`), and all ten
evidence tokens across the two cards resolve.

The only contradiction in either card is internal, and it is again in
`repo-split-public-private`'s exposure paragraph: the Statement against itself, and the Statement
against its own `next` and against `CHECKLIST.md` item 3c. Sixth pass, same field, fourth different
sentence.
