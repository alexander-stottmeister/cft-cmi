# REF-CLEARED: verification of the compendia clearance, and four cards (2026-09-21)

Scope: the four cards of packet `rigor/review_packet_h.md` — `repo-split-public-private`,
`ci-green`, `docs-pages-rendering`, `public-site-plan` — and, before them, the claim that the
cited-result compendia exposure is CLEARED.

Everything below was measured on 2026-09-21 (evening, after the 20:08 UTC push) against the live
GitHub remote, the two local git directories, a fresh `--mirror` clone in a scratch directory, the
working tree and the knowledge base. No git command that writes was run against either project
repository; the only writes were into a scratch directory and a throwaway `git init` used to compute
one tree SHA. Actor `REF-CLEARED`.

**THE EXPOSURE IS CLEARED.** Every recovery route the earlier notes recorded is dead, the seed set
is empty of discarded objects, the local history and object store are clean, the private companion
still holds everything, and I found no publisher and no route — named or unnamed — that returns any
compendium or the plan page. Section 1 is the evidence, route by route, re-runnable.

The card that asserts the clearance nevertheless **FAILS**, and so do two others, for text
defects — not for the clearance. Section 6 has the verdicts and the exact repair wording.

---

## 0. What the remote is now

    gh api repos/alexander-stottmeister/cft-cmi \
      --jq '{id,created_at,pushed_at,private,fork,forks_count,network_count,size,has_pages}'

    id 1380449076   created_at 2026-09-21T19:55:13Z   pushed_at 2026-09-21T20:08:29Z
    private true    fork false   forks_count 0   network_count 0   size 0   has_pages false

The repository **id is new**, and `created_at` is 19:55:13Z today. This is not the repository the
earlier passes measured; it is a different object store that happens to carry the same name. That
is the structural reason every route below fails, and it is worth recording separately from the
route results, because it is the fact that makes them robust rather than incidental.

    git ls-remote https://github.com/alexander-stottmeister/cft-cmi.git
      a5732487ca3b1a1c74f1d03926750aa7cde63355  HEAD
      a5732487ca3b1a1c74f1d03926750aa7cde63355  refs/heads/main
      f52aa4194c302623d3566dfaae2513369127ed73  refs/tags/v0.1.0-draft

Two refs, both post-recreation, both resolving locally. `gh api repos/.../commits --paginate` returns
**68** commits; `git rev-list --all --count` locally is **68**. The remote and the local history are
the same 68 commits and nothing else.

---

## 1. The recorded recovery routes, re-run against the live remote

The hashes are the ones in `rigor/referee_plan_split.md`:
commit `5d64c77d4b513b4005e2ad3a19c0f26086e96be0`, the force-push "before"
`8b96354352eec21a57631f994e9816ea53c72147`, blob `18cc05ab438b307f64fd7b4ee35834b30c06f0d6`, and the
short forms `ba14962 8ab5a32 f9ffae4 51b11c3 ade3048 b9307d8 04af962 03e2e48 5ad78cb b9daa45 a09ab81
bbaa665 e2c5260 8bbd412`.

### 1.1 Route A — the commit endpoint, by full 40-character SHA

    gh api repos/alexander-stottmeister/cft-cmi/commits/5d64c77d4b513b4005e2ad3a19c0f26086e96be0
    gh api repos/alexander-stottmeister/cft-cmi/commits/8b96354352eec21a57631f994e9816ea53c72147

Both: **HTTP 422**, `{"message":"No commit found for SHA: <sha>"}`.
Also `GET /git/commits/<sha>` (the plumbing form, which no note had tried): **HTTP 404 Not Found**.

### 1.2 Route B — the contents endpoint at a discarded ref

    for f in rigor/cited_R1.tex rigor/cited_R2.tex rigor/cited_R3.tex rigor/cited_R4.tex \
             rigor/cited_results_all.tex plan_page/petz_program_plan.html; do
      gh api "repos/alexander-stottmeister/cft-cmi/contents/$f?ref=5d64c77d4b513b4005e2ad3a19c0f26086e96be0"
    done

All six: **HTTP 404**, `{"message":"No commit found for the ref 5d64c77…"}`. The same call with
`rigor/cited_R1.tex` at each of the thirteen short refs above: **404 for every one**, including
`5ad78cb` (the old tag target) and `03e2e48` (the initial import).

### 1.3 Route C — the blobs endpoint, by full blob SHA

    gh api repos/alexander-stottmeister/cft-cmi/git/blobs/18cc05ab438b307f64fd7b4ee35834b30c06f0d6

**HTTP 404 Not Found.** I did not stop at the one recorded blob. I computed the blob SHA of all six
private files from the working tree and asked for each:

    for f in plan_page/petz_program_plan.html rigor/cited_R{1,2,3,4}.tex rigor/cited_results_all.tex; do
      b=$(git hash-object "$f"); gh api "repos/alexander-stottmeister/cft-cmi/git/blobs/$b"; done

    3aa2e00b99151d7b012316d9a0903b65afbb62d4  plan_page/petz_program_plan.html   35,086 B  -> 404
    a1dc319b1f08cd144e8f2b066d014ca12c59c5dc  rigor/cited_R1.tex                 70,874 B  -> 404
    c8fb6e69dadddd19aee4893554da41ed809136d4  rigor/cited_R2.tex                 72,489 B  -> 404
    4ef4814d467043b5471dd3882754f50538918ba7  rigor/cited_R3.tex                 66,304 B  -> 404
    07ca78ac87faf76b997d7baf68d03057a4d83541  rigor/cited_R4.tex                 90,433 B  -> 404
    18cc05ab438b307f64fd7b4ee35834b30c06f0d6  rigor/cited_results_all.tex       299,915 B  -> 404

Each of the six is confirmed to be the right object name by `git --git-dir=.git-private cat-file -t`,
which returns `blob` for all six, and `git --git-dir=.git-private log --all --follow` shows exactly
one blob version per path, so these are the only object names those files ever had.

### 1.4 Route D — the `commits?sha=` history walk

    for h in <the 16 hashes above>; do
      gh api "repos/alexander-stottmeister/cft-cmi/commits?sha=$h&per_page=100"; done

**HTTP 404 Not Found for every seed.** This was the widest route (one seed, one paginated call, 48
commits) and it now returns nothing from any seed.

### 1.5 Route E — `git fetch` of a discarded SHA into a scratch clone

    git clone --mirror https://github.com/alexander-stottmeister/cft-cmi.git <scratch>/mirror.git
    git --git-dir=<scratch>/mirror.git fetch origin 5d64c77d4b513b4005e2ad3a19c0f26086e96be0
    git --git-dir=<scratch>/mirror.git fetch origin 8b96354352eec21a57631f994e9816ea53c72147

    fatal: remote error: upload-pack: not our ref 5d64c77d4b513b4005e2ad3a19c0f26086e96be0
    fatal: remote error: upload-pack: not our ref 8b96354352eec21a57631f994e9816ea53c72147

and for the short forms, `fatal: couldn't find remote ref <sha>`. The mirror itself carries
**1393 objects** — identical to the local store — and two refs.

**All five recorded routes fail.**

---

## 2. The seed set, re-derived from scratch

I did not reuse any earlier seed list. I enumerated what the four feeds publish *today*.

    gh api --paginate repos/alexander-stottmeister/cft-cmi/actions/runs?per_page=100
    gh api --paginate repos/alexander-stottmeister/cft-cmi/events?per_page=100
    gh api --paginate repos/alexander-stottmeister/cft-cmi/activity?per_page=100
    gh api --paginate users/alexander-stottmeister/events?per_page=100

then, from the JSON, every `head_sha`, every `head_commit.id`, every `head_commit.tree_id`, every
`payload.before`, `payload.head`, `payload.commits[].sha`, and every `before`/`after` of the activity
rows.

| feed | entries | commit-ish SHAs it publishes |
|---|---|---|
| `/actions/runs` | `total_count` **2** | `a5732487ca3b…`, `fac463d27d1a…` |
| `/events` | **1** (a single `ReleaseEvent`) | none |
| `/activity` | **2** (1 `branch_creation`, 1 `push`; **0 force_push**) | `fac463d27d1a…`, `a5732487ca3b…`, and the null SHA `000…0` |
| `/users/alexander-stottmeister/events` | 245 total, **1** for this repository (a `ReleaseEvent`) | none |

**Union: exactly two real SHAs.** Both resolve locally:

    git cat-file -t a5732487ca3b1a1c74f1d03926750aa7cde63355   -> commit
    git cat-file -t fac463d27d1a6ac1eb2396c6264ffa099b2ee131   -> commit

**The tree route (G-N1), specifically.** The run list publishes two `head_commit.tree_id` values:

    57a979e1f73020e6a788b4d36598aa1c828d1f89   (= a5732487…^{tree})
    9bfa50952ff4abf9b7b070e43a88f7c3b69de044   (= fac463d2…^{tree})

Both resolve locally (`git cat-file -t` -> `tree`, and `git rev-parse <commit>^{tree}` reproduces
them). `GET /git/trees/<id>?recursive=1` resolves both, `truncated: false`, **645 entries each**
(621 files + 24 directories), and in both listings:

    compendia / plan page / rigor/shots / *.pdf  entries: 0

So the two-call route that used to reach the files now reaches a clean tree. There is no third tree
id to try, because there is no third run.

I also probed a tree id that is *known to have existed in the old repository*: the old `plan_page/`
subtree, reconstructed exactly from the one blob it contained —

    printf '100644 blob 3aa2e00b99151d7b012316d9a0903b65afbb62d4\tpetz_program_plan.html\n' | git mktree --missing
      -> c6c9235a1691e39ab1d435b1397f74ad03f3e921

`git --git-dir=.git-private cat-file -p c6c9235a…` prints that exact entry, so the object name is
right and that tree really existed. `gh api repos/…/git/trees/c6c9235a…` -> **404 Not Found.**

---

## 3. Publishers and routes no note has named

Everything below was probed against the live repository. None of it returns any discarded object.

| probe | result |
|---|---|
| `/repos/…/commits` (list) | 68 commits, all 68 in the local history |
| `/repos/…/branches`, `/git/refs`, `/tags` | one branch, one tag, both post-recreation |
| `/repos/…/deployments` | `[]` |
| `/repos/…/actions/artifacts` | `total_count 0` |
| `/repos/…/actions/caches` | `total_count 0` |
| `/repos/…/pages` | 404 (never enabled) |
| `/repos/…/hooks`, `/comments`, `/issues?state=all`, `/pulls?state=all`, `/forks`, `/keys`, `/subscribers`, `/stargazers` | all `[]` |
| `/repos/…/environments`, `/actions/secrets`, `/actions/runners` | `total_count 0` |
| code-scanning / secret-scanning / Dependabot alerts | disabled (403/404) |
| `/search/commits?q=repo:…` | 0 items (index not yet built for the new repository) |
| `/search/commits?q=hash:5d64c77…` and `q=repo:…+hash:5d64c77…` | `total_count 0` |
| `/search/code?q=repo:…+cited_results_all` / `+petz_program_plan` / `+filename:cited_R1.tex` | `total_count 0` each |
| `/repos/…/compare/5d64c77…...main` | 404 |
| `/repos/…/zipball/<discarded>` and `/tarball/<discarded>`, redirect followed | 302 -> codeload -> **404**, 14 bytes |
| `codeload.github.com/…/zip/<discarded>` and `/zip/5ad78cb` | 404 |
| `raw.githubusercontent.com/…/<discarded>/rigor/cited_results_all.tex` | 404 |
| `raw.githubusercontent.com/…/<discarded>/plan_page/petz_program_plan.html` | 404 |
| `raw.githubusercontent.com/…/main/plan_page/petz_program_plan.html` | 404 |
| `raw.githubusercontent.com/…/main/README.md` (control) | **200** — the probes are live |
| `/repos/…/zipball/main` and `/zipball/refs/tags/v0.1.0-draft` (controls) | **200**, 3,534,683 B and 2,352,541 B |

The controls matter: the archive and raw probes are not failing because of authentication.

**Residual, not an exposure (N-1).** GitHub keeps a deleted repository restorable by its owner for a
window (documented as 90 days), and nothing in the API exposes that state. Restoring would need the
owner to act deliberately and to rename, since the name is taken. No principal with read access can
reach anything through it, so it does not qualify the clearance — but it is the one thing "deleted"
does not yet mean, and no card records it.

---

## 4. The local history and object store

    git count-objects -v                -> 8 loose + 1385 in-pack = 1393
    git cat-file --batch-all-objects    -> 1393 objects: 68 commits, 300 trees, 1025 blobs
    git rev-list --objects --all | wc -l-> 1393
    comm -23 <all objects> <reachable>  -> 0
    git fsck --unreachable --dangling --no-reflogs -> (silent)

**Zero unreachable objects.** The reflog holds two entries, both post-recreation.

**Every path ever added.**

    git log --all --no-renames --diff-filter=A --name-only --pretty=format: | sed '/^$/d' | sort -u

**621** distinct paths. Of them: `rigor/shots/` **0**, `*.pdf` **0**, `cited_R[1-4].tex` /
`cited_results_all.tex` **0**, `petz_program_plan` **0**. And
`git log --all --oneline -- plan_page rigor/cited_R1.tex … rigor/cited_results_all.tex` returns
**0 commits**: no commit in the whole history so much as touches those paths.

`git check-ignore --stdin --no-index` over all 621: **0 ignored**, so no path in the history is one
the current ignore rules would hide.

**The tag.** `v0.1.0-draft` is a lightweight tag at `f52aa4194c302623d3566dfaae2513369127ed73`
locally and on the remote (`git ls-remote` agrees). Its tree holds **403 files** and **0** compendia,
plan page, excerpts or PDFs.

**Content, not just names.** I read every one of the 1025 blobs in the local store and every one of
the 1025 in the mirror clone through `git cat-file --batch`, and searched each for five byte-exact
probes taken from the private files (a 60-byte slice from the middle and the head of
`cited_results_all.tex`, a 60-byte slice from the middle of `cited_R1.tex`, and the head and a
mid-file slice of `petz_program_plan.html`):

    PUBLIC local : 1025 blobs -> 0 hits on four probes, 2 on 'compendium_all_head'
    MIRROR       : 1025 blobs -> identical

The two hits are the two committed versions of `rigor/combine.py`, the *generator* script, which
contains the compendium's `\title{…}` template as a literal. It quotes no third-party text; its
docstring already says its inputs and output are private. Not a leak; recorded so the next pass does
not re-discover it.

---

## 5. The release, and the private companion

### 5.1 The release

    gh api repos/alexander-stottmeister/cft-cmi/releases

One release, `v0.1.0-draft`, prerelease, `published_at 2026-09-21T20:00:26Z`, **exactly two assets**:

    cft-cmi-paper1-free-fermion.pdf   629,891 B   application/pdf   downloads 0
    cft-cmi-paper2-universality.pdf   607,822 B   application/pdf   downloads 0

I downloaded both through the assets API and `cmp`'d them: **byte-identical** to `paper1/main.pdf`
(629,891 B) and `paper2/main.pdf` (607,822 B) on disk.

**Sources unchanged**: `git diff --stat v0.1.0-draft..HEAD -- paper1 paper2 fidelity_bib.tex` is
**empty**, so the assets were built from the same sources as the tag.

**The checksum explanation, tested rather than accepted.** I copied the whole tree into a scratch
directory and rebuilt `paper1/main.tex` three times with `pdflatex -halt-on-error
-interaction=nonstopmode`, then `cmp -l` against the released PDF:

    rebuilt size 629,891 B  (identical length)
    differing bytes: 66, in exactly three runs:
      623744-623746 and 623779-623781  ->  /CreationDate and /ModDate  (D:20260921215958 vs …222558)
      627348-627414                    ->  the two trailer /ID hex digests

So the mechanism is length-preserving and the explanation is essentially right. It is **not exact**:
the differences are the timestamp *and* the trailer `/ID`, which pdftex derives from the creation
time. See R-B4.

**What I could not check.** The byte lengths of the *original* assets are recorded nowhere — not in
any referee note, not in a card, not in CHECKLIST.md or PRIVATE.md — and the old release is gone with
the old repository. "At their original byte lengths" is therefore supported by inference (unchanged
sources + a demonstrably length-preserving rebuild) and not by any measurement of the old assets. It
is a reasonable claim, but the card states it as a fact that no record can now confirm. See R-B4.

### 5.2 The private companion

    git --git-dir=.git-private ls-files | grep -E 'petz_program_plan|cited_R|cited_results_all'
      plan_page/petz_program_plan.html
      rigor/cited_R1.tex  rigor/cited_R2.tex  rigor/cited_R3.tex  rigor/cited_R4.tex
      rigor/cited_results_all.tex

All six present and tracked; `plan_page/petz_program_plan.html` is on disk at 35,086 B. Public
tracking of any of the six: **0**. `./pgit check`: public 621, private 235, overlap 0, uncommitted
0/0, shots on disk 178 / tracked 178, exit 0. Private bytes 48,392,273 = **48.39 MB**.

**The private remote is untouched and has never been force-pushed.**

    gh api repos/alexander-stottmeister/cft-cmi-private --jq '{id,created_at,pushed_at,private}'
      id 1378425175   created_at 2026-09-20T14:29:14Z   pushed_at 2026-09-21T20:08:33Z   private true

    gh api --paginate repos/…-private/activity?per_page=100
      17 entries: 1 branch_creation + 16 push, chained before -> after with no gap
      force_push rows: 0

The id is the original one from 2026-09-20 — this repository was never deleted. Local HEAD, local
`refs/heads/main` and `git ls-remote` all agree at `53e81a2a8d9fe5741761a7361a776ddb9bd2f87c`, and the
local reflog shows only `commit:` and `update by push` entries, never a forced update. **Nothing was
lost.**

---

## 6. The cards

### 6.1 `repo-split-public-private` — **FAIL**

The clearance itself is real and every new figure in the rewritten paragraph is exact. The card fails
because the **old tail of the same paragraph was left standing**, in the present tense, and it
contradicts the clearance the same paragraph just announced. This is the sixth consecutive pass at
which a sentence of this paragraph says the opposite of its neighbours, and — as at C12, D-D2 and
F-D1 — it **ships**: `docs/data/extra-claim-map.json` carries all of it verbatim.

**Verified exact** (re-measured, not read): 621 public-tracked files; 235 private files at
48,392,273 B = 48.39 MB with exactly the ten enumerated paths outside `rigor/shots` and `refs`;
overlap 0; 97 tracked `.out` (83 `numerics/`, 14 `rigor/`); 178 excerpts on disk and tracked; 47
private `refs/*.pdf`; **256** `\shot`/`\shotc` call forms across 20 tracked `.tex` less the one inside
`\shotc`'s definition at `rigor_preamble.tex:48` = **255 in 19**; 25 tracked `.py` mention `_ROOT`
(the 25th is `fix_paths.py`, the rewriter) and **0** contain a `/Users/alex` literal; both remotes
private, fork false, forks_count 0, 1 collaborator; nine private evidence targets rendered without a
link, exactly the nine `make check` names; all five evidence tokens resolve;
`rigor/README_AGENTS.md:36` is the named section. The seven public-tracked files that carry a
discarded **commit** prefix reproduce exactly (see R-B3 for the rule). `make check` exit 0,
`make rigor` exit 0, `kb lint` 0 issues.

**FAIL B-1 — the paragraph announces the clearance and then withdraws it.** Sentences S19–S24 of the
Statement (numbering as printed in §6.5) are the pre-clearance text, unedited:

- S19 "…what does not move is the 44 pre-rewrite commits they publish and the 15 of them that were
  workflow heads." **False now.** The four feeds publish **two** SHAs, both post-recreation; the run
  list has **two** runs and **zero** discarded heads. The clause also begins "All **three** feeds",
  while S12 names four publishers, and hedges "the entry counts here are the measurement of
  2026-09-21" when the same edit deleted every entry count from the paragraph, so the hedge qualifies
  nothing.
- S20 "The rewrite therefore bought unreachability, not deletion, and the mirror-clone check
  REF-MOVE-1e ran cannot see server-side retention…" — a verbatim duplicate of S10 and S14, now in a
  paragraph whose point is that the objects are gone.
- S21 "What bounds the exposure is access control alone…" — present tense, false: what bounds it now
  is that the objects do not exist.
- S22 "Deletion requires one of two routes: a GitHub Support purge…, or deleting the remote and
  recreating it…" — present tense, and S15 says the second route was executed seven sentences
  earlier.
- S23 "UNTIL ONE OF THEM IS DONE, 'removed from the remote' MUST NOT BE CLAIMED, AND THE REPOSITORY
  MUST NOT BE MADE PUBLIC" — **directly contradicts** `next:` ("No item gates publication any more"),
  CHECKLIST.md item 3 ("**DONE and CLEARED 2026-09-21**") and PRIVATE.md's closing paragraph. This is
  the one sentence of the card that most needs to be right, and it is the one a reader of the site
  meets: `grep -c 'MUST NOT BE MADE PUBLIC' docs/data/extra-claim-map.json` = **1**.
- S24 "One designated-private path is still recoverable from the public history,
  `plan_page/petz_program_plan.html`, which entered in the initial import and is in the tree of the
  pushed tag v0.1.0-draft." — **False, measured four ways**: 621 paths ever added, `petz_program`
  **0**; `git log --all -- plan_page` **0 commits**; `git ls-tree -r v0.1.0-draft` 403 files, **0**
  hits; `contents/plan_page/petz_program_plan.html?ref=<any discarded ref>` **404**, and at `main`
  raw returns **404**. `grep -c 'One designated-private path is still recoverable'
  docs/data/extra-claim-map.json` = **1**.

**Repair R-B1.** Delete S19 through S24 entirely and put in their place, immediately after S18:

> What bounded the exposure while it lasted was access control alone — the repository has never been
> public, is unforked and has no other collaborators — and what ends it is that the objects no longer
> exist: the repository serving this name was created at 2026-09-21T19:55:13Z with a new id and holds
> only the 68 commits of this history. The other recorded route, a GitHub Support purge of the
> unreachable objects, was therefore not needed and is not open work. `plan_page/petz_program_plan.html`
> went with the compendia: it is in no commit of the history and not in the tree of the retagged
> v0.1.0-draft, and it is tracked privately. One residual that is not an exposure: GitHub keeps a
> deleted repository restorable by its owner for a window, so "deleted" is soft from the owner's side
> and hard from every reader's.

**FAIL B-2 — "seven files" is wrong for the knowledge base, and it ships.** `next:` says "the
knowledge-base repository carries the same discarded hashes in seven files of its own", and
CHECKLIST.md item 3d says the same. Measured under the project's own rule — take the discarded
commit prefixes, `git ls-files | xargs grep -l` — the knowledge base has **five**:

    projects/cft_cmi/claims/longo-xu-cmi.md               8ab5a32 ba14962
    projects/cft_cmi/claims/paper2-status.md              2c73e22 de02792
    projects/cft_cmi/claims/readme-and-figures.md         2c73e22 de02792
    projects/cft_cmi/claims/repo-split-public-private.md  13 prefixes
    projects/cft_cmi/events-Alexanders-MacBook-Pro-8.jsonl 14 prefixes

Widening the set to *every* cft-cmi commit hash that no longer resolves (which is what the
recreation actually invalidated) gives **ten** files, not seven either: the five above plus
`ci-green.md`, `docs-pages-rendering.md`, `generated-docs.md`, `paper1-status.md` and
`public-site-plan.md`. Seven reproduces under no rule I could construct. The same sentence is in
`docs/data/extra-claim-map.json`.

**Repair R-B2.** In `next:` replace
`the knowledge-base repository carries the same discarded hashes in seven files of its own and needs
the same measurement before IT is ever made public`
with
`the knowledge-base repository carries discarded cft-cmi hashes in five of its own files under the
strict rule, ten if every hash the recreation invalidated is counted; the count is measured, not
remembered, and it needs re-measuring before that repository is ever made public`.
Make the identical correction in CHECKLIST.md item 3d.

**FAIL B-3 — two figures inside the verification sentence.** S16 is the sentence the whole clearance
rests on, so its two inaccuracies matter more than their size.
(i) "all five recovery routes return 'No commit found' or 'Not Found'" — the fifth route does not.
`git fetch origin <sha>` returns `fatal: remote error: upload-pack: not our ref <sha>`.
(ii) "both full 40-character hashes included" — there are **three** full 40-character tokens in the
tracked tree (`git ls-files | xargs grep -ohE '\b[0-9a-f]{40}\b' | sort -u`): two commits and the
compendium blob `18cc05ab…`. I tested all three; all three fail.

**Repair R-B3.** Replace
`all five recovery routes return 'No commit found' or 'Not Found', both full 40-character hashes included`
with
`all five recovery routes fail — the four REST routes with "No commit found" or "Not Found", and
git fetch of a discarded SHA with "upload-pack: not our ref" — for all three full 40-character tokens
the tracked notes carry, the two commits and the compendium blob`.

**FAIL B-4 — the release sentence claims more than the record can support.** "both papers at their
original byte lengths" cannot be checked: no note, card or checklist ever recorded the old assets'
sizes, and the old release went with the old repository. And "their checksums differ only by the
timestamp" is incomplete: a controlled rebuild differs in 66 bytes, the two timestamps *and* the two
trailer `/ID` digests.

**Repair R-B4.** Replace
`The release was recreated with both papers at their original byte lengths, rebuilt from unchanged
sources, so their checksums differ only by the timestamp pdflatex embeds.`
with
`The release was recreated with the same two assets, rebuilt from sources that git diff shows are
unchanged since the tag (629,891 B and 607,822 B, byte-identical to the local builds). A controlled
rebuild of paper 1 reproduces the length exactly and differs in 66 bytes: the /CreationDate and
/ModDate and the two trailer /ID digests pdflatex derives from them. The original assets' lengths
were never recorded, so "unchanged length" is an inference from that rebuild and not a comparison.`

**NON-BLOCKING, with wording (no verdict rests on these).**
- **N-B5.** S08 says "620 distinct paths were ever added" and S16 says "621" — the same quantity,
  twice, differing, in one paragraph. It is 621 today. Drop the figure from S08 (its clause is about
  a mirror clone of a repository that no longer exists) and keep S16's.
- **N-B6.** S02 "BOTH REMOTES ARE PRIVATE as of 2026-09-20" — the public remote is four hours old.
  PRIVATE.md already says "recreated 2026-09-21". Read "as of 2026-09-20 for the private companion
  and since its recreation on 2026-09-21 for the public one".
- **N-B7.** `next:` ends "CHECKLIST.md records all of this." CHECKLIST records the clearance (3),
  the plan page (3b), the kept notes (3c), the knowledge base (3d) and the dead hashes (3e); it does
  **not** record the three Pages steps, which live in the README and the workflow comment. Say
  "CHECKLIST.md items 3 to 3e record the clearance; the three Pages steps are in the README and in
  the workflow comment."
- **N-B8.** G-N2 was never applied: S10 still reads "three independent REST routes each returned the
  files, one byte-identical to the private copy" — `referee_plan_split.md` records all five as
  `cmp`-identical. "the largest of them byte-identical" is the fix.
- **N-B9.** "tracked by neither (423 files, 198.6 MB on 2026-09-21…)" measures **427 files,
  199.4 MB** now (25 review packets among them). The card hedges the mechanism, so this is drift, not
  a defect.
- **N-B10.** `.github/workflows/check.yml:47` carries `9aed69a`, a hash that no longer resolves, in a
  comment. It is not a referee note, so the author rule does not protect it; CHECKLIST 3e covers it
  generically. Worth replacing with "before the CI repair of 14:53 on 2026-09-21".

**Consistency.** No other card contradicts this one. `plan-page`, `open-problems-plan-note8`,
`longo-xu-cmi`, `generated-docs` and `public-site-plan` are all consistent with the clearance;
CHECKLIST 3, 3b, 3c, 3d, 3e and PRIVATE.md agree with `next` and with S09–S18, and disagree with
S19–S24 — the contradiction is again internal, in the same field, for the same reason.

### 6.2 `ci-green` — **FAIL**

Both hash replacements are **accurate**:
- "9aed69a:" -> "the repair commit of that afternoon:" — that commit is now `fcd2fac`,
  `2026-09-21T14:53:05+02:00`, "CI: give the two failing jobs what they were missing", touching
  `.github/workflows/check.yml`, `Makefile` and `tools/build_site_data_extra.py`. Accurate.
- "5a3988b" -> "the commit before the regeneration" — that commit is now `e1ed92b` (15:09:47). I
  checked the substance rather than the label: `git show e1ed92b:docs/data/extra-claim-map.json |
  grep -c '"ci-green"'` = **0**, and at the next commit `de2d49c` it is **4**, and `de2d49c`'s diffstat
  shows `docs/data/extra-claim-map.json | 194 ++++---`. Accurate.

No commit hash remains anywhere in the card's Statement, How-to-verify or `next`. Also re-verified
live: `--allow-missing-kb` is in `tools/build_site_data_extra.py`; `rigor` is in `.PHONY`; the papers
target prints the last 40 lines of `main.log` on failure; `pages:` carries `if: false`; `has_pages`
is false; and the current run log still prints `41 document(s), 0 failing, 0 known` and the
`NOT CHECKED … docs/data/extra-claim-map.json` line, so the card's substance is intact.

**FAIL C-1 — the card names three Actions runs that no longer exist, and its How-to-verify is now
false.** The recreation destroyed the Actions history along with the repository. All three IDs 404:

    gh api repos/alexander-stottmeister/cft-cmi/actions/runs/35602149545   -> 404 Not Found
    gh api …/actions/runs/35595433844                                      -> 404 Not Found
    gh api …/actions/runs/35603853632                                      -> 404 Not Found

and the card's own instruction now returns the opposite of what it says:

    gh run list --repo alexander-stottmeister/cft-cmi
      completed success  the compendia exposure is cleared…  35649200491
      completed success  all seven infrastructure cards pass 35648285382

Two runs, both successes, no failures. "shows 24 failures then success at 35602149545" is false as an
instruction and unexecutable as a check. The three dead IDs **reach the public site**:
`grep -oE '\b3[0-9]{10}\b' docs/data/extra-claim-map.json` returns all three. (The site is clean of
dead *commit* hashes: 0 of the 352 distinct hex tokens under the 188 tracked `docs/` files matches any
invalidated cft-cmi commit, and all 313 `github.com/.../blob/` URLs pin `main`, not a SHA — so the
hash replacement did its job; the run IDs are simply a class the edit did not cover.)

**Repair R-C1.** In the Statement replace
`REF-CI-PAGES established this after the fact by diffing the apt 'NEW packages will be installed'
lists of runs 35595433844 (28 packages) and 35602149545 (31: the same 28 plus lmodern,
xfonts-encodings, xfonts-utils)`
with
`REF-CI-PAGES established this after the fact by diffing the apt 'NEW packages will be installed'
lists of the last failing run (28 packages) and the first passing one (31: the same 28 plus lmodern,
xfonts-encodings, xfonts-utils)`;
replace `Run 35602149545 is the first success:` with `The first success came on the repair commit:`;
and replace `run 35603853632 was green over it` with `the next run was green over it`.

**Repair R-C2.** Add one sentence at the end of the Statement, because the evidence is now
unrecoverable and a reader must be told:
`The 24 failing runs and the first passing one were destroyed on 2026-09-21 when the remote was
deleted and recreated to clear the compendia exposure; the run history now starts at the recreation,
so the failure sequence is no longer checkable on GitHub and this Statement is the record of it.`

**Repair R-C3.** Replace the whole How-to-verify line with:
`The failing runs no longer exist (the remote was deleted and recreated on 2026-09-21), so the run
sequence cannot be re-checked; what can: gh run list --repo alexander-stottmeister/cft-cmi shows the
current runs, and gh run view <latest> --log shows the NOT CHECKED line naming extra-claim-map.json
and '41 document(s), 0 failing, 0 known'. Locally: make rigor dispatches to the checker instead of
printing 'up to date'; grep -c allow-missing-kb tools/build_site_data_extra.py is 1; the pages job
still carries if: false.`

### 6.3 `docs-pages-rendering` — **PASS**

One replacement, and it is accurate: "committed at 5a3988b," -> "as first committed,". `5a3988b` is
now `e1ed92b`, and `git log --all --diff-filter=A --name-only -- 'docs/read/*'` shows `docs/read/`
first appearing there, 66 files in that one commit. "As first committed" is exactly right, and it is
better than the hash was, because it no longer depends on an identifier at all.

Nothing else changed: the word-level diff against `HEAD` shows only `review:` and that one phrase.
No hex token and no run ID appears anywhere in the Statement, How-to-verify or `next`.

Re-measured rather than read: `make check` prints `155 pages, 2211 links resolve` and
`build_docs --check: 131 pages up to date`, and the mirror is 65 Markdown + 66 HTML (7 top-level +
59 under `read/results/`, of which 58 are result pages and one the index) = 131. `grep -c '<a id='
docs/status.md` = **8**. `has_pages` false. The README carries the Pages address **six** times at
lines **27, 33, 34, 339, 340, 341** — exactly as claimed — and its three publishing conditions are
word-for-word the workflow comment at `check.yml:60-68` and the `if: false` at line 68. Nine private
evidence pointers rendered without a link, matching `make check`.

### 6.4 `public-site-plan` — **FAIL**

Replacement (1) is accurate: "7cae480 (2026-09-21 11:07)," -> "the repair of 2026-09-21 11:07," —
that commit is now `7157f4d`, `2026-09-21T11:07:47+02:00`, "rigor: repair the two documents that did
not build". Correct to the minute.

**FAIL P-1 — replacement (2) is a splice, and it makes the sentence say something false.** The edit
turned `and CI went green only at 9aed69a (14:53) after the two unrelated repairs recorded in
ci-green` into `and CI went green only **with the workflow repair** at 14:53 after the two unrelated
repairs recorded in ci-green`. The hash was the thing that identified 14:53 as *the same commit* as
the two repairs; replacing it with a third named repair leaves a sentence that reads as three
repairs in sequence — a workflow repair *after* two unrelated ones. There were two, in one commit,
`fcd2fac` at 14:53, and only one of them was in the workflow (the other is the `--allow-missing-kb`
flag in `tools/build_site_data_extra.py`; the commit also touched the `Makefile`). This is the same
species as F-D2, and like F-D2 it ships: the Statement is carried verbatim in
`docs/data/extra-claim-map.json`.

**Repair R-P1.** Replace
`and CI went green only with the workflow repair at 14:53 after the two unrelated repairs recorded in
ci-green`
with
`and CI went green only at 14:53 that day, with the single commit that carried both of the unrelated
repairs recorded in ci-green — lmodern added to the workflow, and --allow-missing-kb added to the
site-data extractor`.

**FAIL P-2 — two stale figures in the budget sentence.** "The 3 MB asset budget holds
(docs/{assets,lib,data} = 1.26 MB, public repository 7.93 MB)". Measured now:
`du -sk docs/assets docs/lib docs/data` = **1.30 MB**; `git ls-tree -r -l HEAD | awk '{s+=$4}'` =
8,210,509 B = **8.21 MB** over 621 files. The budget does hold, so the load-bearing half is true, but
both parenthesised numbers are wrong and `7.93 MB` is the figure REF-PLAN-SPLIT measured at a commit
that no longer exists — it has been wrong at four consecutive passes in one card or another.

**Repair R-P2.** Replace the parenthesis with
`(docs/{assets,lib,data} = 1.30 MB and the public repository 8.21 MB on 2026-09-21; both grow with
every generated page, so these are dated measurements and the budget is the fixed figure)`.

**Verified exact, so nothing else is failed for**: `rigor/public_site_plan.md` is **237** lines; the
knowledge base holds **89** claim cards and `docs/status.md:5` says "90 cards: 89 claim cards … plus
1 finding"; `plan_page/petz_program_plan.html` is indeed out of the public repository and tracked
privately (now out of the whole history, which is stronger than the card claims and contradicts
nothing); `CITATION.cff` and `.github/ISSUE_TEMPLATE/` exist; the five SVGs are in `docs/assets/`; the
ten module pages are in `docs/explore/`; `docs/.nojekyll` exists. No hex token or run ID appears in
the Statement, How-to-verify or `next`.

### 6.5 Statement sentence numbering used above

S01 begins "Since 2026-09-20 the cft_cmi directory…"; S09 "THEY REMAINED RECOVERABLE…"; S15 "CLEARED
on 2026-09-21…"; S16 "Verified afterwards…"; S17 the release sentence; S18 "The seven files that gave
the route are kept…"; S19 "All three feeds grow with ordinary use…"; S20 "The rewrite therefore
bought unreachability…"; S21 "What bounds the exposure is access control alone…"; S22 "Deletion
requires one of two routes…"; S23 "UNTIL ONE OF THEM IS DONE…"; S24 "One designated-private path is
still recoverable…"; S25 "Licensing:…". Reproduce with:

    python3 - <<'PY'
    import re
    t=open('../kb/projects/cft_cmi/claims/repo-split-public-private.md').read()
    s=t.split('---',2)[2].split('## Statement',1)[1].split('## How to verify')[0].strip()
    for i,p in enumerate(re.split(r'(?<=[.;])\s+(?=[A-Z(])', s),1): print(f"[S{i:02d}] {p}")
    PY

---

## 7. Gates

    make check   exit 0   (155 pages / 2211 links resolve; build_docs --check 131 pages up to date;
                           claims 90; 58 result pages; 9 private evidence pointers; all nine data
                           files ok, extra-claim-map.json included)
    make rigor   exit 0   (46 document(s), 0 failing, 0 known)
    kb lint      0 issues, 4 awaiting review

Sixth consecutive pass with both green.

---

## 8. Verdicts

- **The compendia exposure is CLEARED.** Five recorded routes, six blob SHAs, one reconstructed tree
  SHA, four feeds, twenty-odd further endpoints, the archive and raw hosts, and a byte-level scan of
  every object in the local store and in a fresh mirror: nothing returns a compendium or the plan
  page, and nothing publishes a seed that would reach one. The local history and the release are
  clean, and the private companion still has all six files with its remote untouched and
  never force-pushed.
- `repo-split-public-private`: **FAIL** — B-1 (S19–S24 are the pre-clearance text, still present
  tense, contradicting the clearance, `next`, CHECKLIST 3 and PRIVATE.md, and shipping to the site;
  S24 is simply false), B-2 (the knowledge base has five such files, not seven), B-3 (two figures
  inside the verification sentence), B-4 (the release sentence claims an unrecorded comparison).
- `ci-green`: **FAIL** — C-1: three Actions run IDs that 404, in the Statement and in a How-to-verify
  whose live result contradicts the card; all three reach the public site. The two hash replacements
  are accurate.
- `docs-pages-rendering`: **PASS** — the one replacement is accurate and better than the hash;
  nothing else changed; every figure re-measured exact.
- `public-site-plan`: **FAIL** — P-1 (the second replacement is a splice that invents a third repair;
  it ships), P-2 (both figures in the asset-budget parenthesis are stale). The first replacement is
  accurate to the minute.
