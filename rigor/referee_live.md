# REF-LIVE: the published site and three cards (2026-09-22)

Fourteenth pass, and the first since the repository became world-readable. Order of work as the
brief set it: what is now public, then the repository and its history as a stranger sees them,
then the release and the new GitHub surfaces, then the three cards, then the README, then the
gates.

**A note on this file.** It carries no hexadecimal fragment of any object, because two live
measurements in `repo-split-public-private` count the tracked files that carry them ("the notes
carry fifteen such tokens", "Seven public-tracked files in this repository gave the route in
words") and a report that quotes one moves the number it is checking. Both were re-measured
today and both still hold. For the same reason this file does not reproduce the URL named in
E-1: it is tracked publicly and would republish the thing it is asking to have withdrawn.

**Verdicts: all three FAIL,** each on a field the rewrite did not follow through into, and each
now false on the public site. One exposure, E-1, is not about the three cards and comes first.

---

## 0. EXPOSED — the address of the private plan page is published, and the site tells the reader to open it

**E-1. BLOCKING, and the most serious thing in this pass.** The deployed
`data/extra-claim-map.json` ships the `plan-page` card verbatim, and
`explore/claim-map.html` renders its Statement and its How-to-verify as text (`claim-map.html`
lines 367-368, `h('p', { class: 'statement', text: c.statement })` and `'How to verify: ' +
c.verify`). The Statement prints, in full, the `https://claude.ai/code/artifact/<uuid>` address
of the programme plan/status page, with its version and date, and ends `Republish with the
Artifact tool passing this URL.` The How-to-verify reads `open the URL; grep 'Status (10 Sep)'
in the source.`

That page is precisely the document this project spent 2026-09-21 removing from the public
history. In the same sentence the site masks the file — `plan_page/petz_program_plan.html
(held privately)` — and prints the address of the hosted copy of the same document beside it.
The `held privately` mechanism masks *evidence paths*; it does not look at prose, so a URL
written into a Statement is published untouched.

How I reached it: fetched the deployed Pages artifact of run 35787249180, walked every served
file, and enumerated every absolute URL in the shipped claim map by card. Four hosts appear;
three are `github.com`, `alexander-stottmeister.github.io` and the site's own address. The
fourth is this one, and it is reachable at
`https://alexander-stottmeister.github.io/cft-cmi/data/extra-claim-map.json`.

**What I could and could not confirm about reachability.** An anonymous `curl --no-netrc` of
the artifact URL returns **200** — but that is the Claude wrapper page, 22,776 B, titled
`Claude Artifact`, carrying none of the plan text. The frame host that serves the artifact's
own content returns **404** anonymously. So the plan page's *content* is not world-readable
today. What is world-readable is its permanent address, its version number, and an instruction
to open it. That address is a capability: it cannot be guessed, it does not expire, and it is
now in a JSON file on a public web server and in the git history of a public repository. If the
artifact is ever shared, or its sharing default ever changes, the address is already out. I am
reporting it as exposed for that reason, not because content leaked today.

**Repair E-1, verbatim.** In `kb/projects/cft_cmi/claims/plan-page.md` replace the whole
Statement with

> The programme plan/status page is a Claude artifact, held privately; its source is kept in
> the project at plan_page/petz_program_plan.html, which is tracked in the private companion and
> is in no commit of the public history (it was lost once when the scratchpad was wiped). The
> artifact URL and the version to republish are recorded in PRIVATE.md and deliberately not
> here, because this card's Statement is published verbatim on the public site.

and replace the whole How-to-verify with

> grep 'Status (10 Sep)' in plan_page/petz_program_plan.html; the artifact URL is in PRIVATE.md.

Move the URL and `version 13, 14 Sep 2026` into `PRIVATE.md` (private-tracked) in the same
commit, then `make docs data` and commit the regenerated `docs/data/extra-claim-map.json`. The
check that the repair landed is `grep -c 'claude.ai' docs/data/extra-claim-map.json` → 0; it is
1 today.

**Recommended, not required.** `tools/build_site_data_extra.py` should refuse to ship a card
whose `statement`, `verify` or `next` contains an absolute URL outside the host allow-list
`check_links.py` already maintains (`github.com`, `alexander-stottmeister.github.io`,
`projecteuclid.org`). The masking rule is currently path-shaped and the leak was prose-shaped;
a host allow-list closes the class rather than the instance.

---

## 1. Everything else served: audited file by file, and clean

I did not sample. I downloaded the `github-pages` artifact of the deploying run, unpacked it,
and compared it to the working tree: **188 files, every one sha256-identical to `docs/`, no
file deployed that is not tracked and no tracked file missing.** `docs/` on disk equals `docs/`
at HEAD (`git status` clean), so the deployed tree is exactly the committed one. Layout: 9 at
the root, 5 `assets/`, 9 `data/`, 10 `explore/`, 8 `lib/` + 23 under `lib/katex`, 7 `read/`,
59 `read/results/`, 58 `results/`.

| class the brief named | found | how |
|---|---|---|
| page excerpt | **0** | no raster or vector excerpt anywhere; the 5 `assets/*.svg` are the generated figures; the release PDFs carry 0 image XObjects |
| source PDF | **0** | no `.pdf` is deployed or tracked; the six private papers appear only as evidence *names*, each rendered `held privately` without a link |
| compendium | **0** | `cited_R1` and `cited_results_all` appear as names in two result pages and the claim map, never as content |
| plan page | **0 content** | `plan_page/petz_program_plan.html` appears only as a masked evidence path — but see **E-1** for its address |
| local filesystem path | **1** | `/Users/alex` occurs once, in the `repo-split-public-private` statement inside the claim map ("the 24 python scripts that hardcoded /Users/alex"). No absolute path is served |
| hash naming a discarded object | **0** | **0** full 40-hex tokens in the whole deployed tree; **0** occurrences of any of the nine discarded-object prefixes; of 349 hex-shaped tokens, 61 contain a letter and all 61 are scientific-notation numbers or KaTeX path data |

Also checked and clean: no e-mail address, no token, no key, no host or machine name, and no
Actions run id — REF-CLEARED's defect C-1 (three destroyed run ids reaching the site) stays
repaired, `grep -oE '3[0-9]{10}'` over the deployed tree returning only a KaTeX constant.
Negative probes confirm only `docs/` is published: `README.md`, `CHECKLIST.md`, `PRIVATE.md`,
`pgit`, `rigor/shots/`, `rigor/cited_results_all.tex`, `plan_page/petz_program_plan.html`,
`refs/VWZ_2307.14434.pdf`, `.git/config` and `../README.md` all 404, while
`read/results/`, `assets/geometry.svg`, `lib/katex/katex.min.css`, `data/extra-claim-map.json`
and `explore/claim-map.html` all 200 with the right type.

Referee *Notes* are not shipped: the claim map carries `statement`, `verify`, `next` and a
one-line `review` only (longest `review`/`verdicts` value in the whole file: 74 characters).
Ninety Statements are published verbatim, which is the general lesson E-1 teaches — anything
written into a card Statement is now a public document.

---

## 2. The repository as a stranger sees it, from a fresh clone

`git clone https://github.com/alexander-stottmeister/cft-cmi.git` into a scratch directory,
nothing read from disk.

- **626 tracked files, 8,371,581 B; 79 commits; refs `main` and the tag `v0.1.0-draft` only.**
- **626 distinct paths ever added over all refs, 0 ever deleted.** Not one matches
  `rigor/shots/`, `*.pdf`, `rigor/cited_R[1-4].tex`, `rigor/cited_results_all.tex` or
  `plan_page/`. 645 object names over the whole history, same result. No `.pdf` is tracked; the
  only tracked images are the four `numerics/lattice/*.png` plots.
- **Tag `v0.1.0-draft`: 403 paths, none forbidden.**
- **No secret of any kind**: 0 hits for `ghp_`, `github_pat_`, `AKIA`, `BEGIN … PRIVATE KEY`,
  `xox…`. The only e-mail-shaped strings are numpy expressions (`Fi@np.diag`). Every commit is
  authored by the owner's GitHub noreply address.

**The exposure probes, re-run rather than carried.** Fifteen full 40-character tokens in four
tracked notes, unchanged. Ten of the fifteen are absent from the public clone (the nine
discarded objects plus the private companion's recorded head); five resolve. I probed each of
the ten on all four REST routes — `commits/`, `git/commits/`, `git/blobs/`, `git/trees/` — as
the owner: **40 probes, 40 failures**, `No commit found for SHA` or `Not Found`. I did not run
`git fetch`, which writes.

Being public opens routes that did not exist before, so I ran those too, **anonymously**, with
a positive control on the same route at the live head:

| route, anonymous | discarded object | live head (control) |
|---|---|---|
| `github.com/OWNER/REPO/tree/<sha>` | 404 | 200 |
| `github.com/OWNER/REPO/commit/<sha>` | 404 | — |
| `github.com/OWNER/REPO/blob/<sha>/<compendium>` | 404 | — |
| `raw.githubusercontent.com/OWNER/REPO/<sha>/<compendium>` | 404 | 200 for `README.md` |
| `raw.githubusercontent.com/OWNER/REPO/<sha>/<plan page>` | 404 | — |
| `codeload.github.com/OWNER/REPO/tar.gz/<sha>` | 404 | 200 |
| `api.github.com/…/commits/<sha>` | 422 | — |
| `api.github.com/…/git/blobs/<blob>` | 404 | — |
| `api.github.com/…/git/trees/<subtree>` | 404 | — |

**The history walk.** Every feed that is now anonymously readable, with every 40-hex token in
it resolved against the public clone: repository events **13 SHAs / 0 unresolved**, network
events 13 / 0, `repos/…/activity` 14 / 1 (the all-zero SHA of a branch creation), Actions runs
26 / 0, `commits/main.atom` 20 / 0, REST commits 158 / 0, deployments 2 / 0, tags 1 / 0,
branches 1 / 0. The owner's public timeline shows two unresolved SHAs; **both belong to a
different repository** (`alexander-stottmeister/pphi2-cutoff-removal`), not to this one. The
card's "44 discarded commits between them" is history: the feeds publish nothing that is not in
this history.

**So the clearance holds against the stranger, not only against the owner.** The seven
public-tracked notes that give the recovery route in words are now world-readable, and I re-read
them as an attacker would: they name the objects and the exact REST calls, and every one of
those calls is dead. The soft-delete residual the card records is additionally blocked now,
because the deleted repository's name is occupied by the new one.

**What is world-readable and was a recorded decision, not a surprise.** Fourteen tracked capture
files carry the absolute path `/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/…` (ten
`.out`, two `.txt`, one `.err`, plus `numerics/optimality_all/F2_RESULTS.md`) — exactly
CHECKLIST item 4's fourteen, whose own last sentence is "leaving it exposes a local directory
layout". Twenty-two tracked files name `/Users/alex` in some form; the twenty-second is
`docs/data/extra-claim-map.json`, which now carries the string because the `repo-split` Statement
does. This is the decision the project took, and it is unchanged; I record it so that nobody
later reads it as a leak.

---

## 3. The release, the tag, and the surfaces that are new to a public repository

- **Release `v0.1.0-draft`**, pre-release, published 2026-09-21T20:00:26Z, two assets and no
  third. Downloaded both anonymously: `cft-cmi-paper1-free-fermion.pdf` 629,891 B and
  `cft-cmi-paper2-universality.pdf` 607,822 B, **sha256-identical to `paper1/main.pdf` and
  `paper2/main.pdf` on disk**. Neither contains a single image XObject, so no page excerpt rides
  in a PDF; metadata is `LaTeX with hyperref` / `pdfTeX-1.40.29` and carries no path.
- **Tag tree clean** (403 paths, none forbidden), target unchanged.
- **NEW AND FALSIFYING A CARD CLAUSE: the repository has a second collaborator.**
  `repos/…/collaborators?affiliation=direct` lists **two**: the owner (admin) and
  `tobiasosborne` with **write** (`push: true`). The repository events feed carries the
  `MemberEvent` at **2026-09-22T14:35:52Z**, and that feed is now anonymously readable.
  REF-CLEARED measured "1 collaborator" on 2026-09-21, so this is new today, and it landed
  *before* the flip. See R-5.
- **Forks 0, `allow_forking: true`.** "is unforked" is true; it is no longer structurally
  guaranteed, which matters only if a history rewrite ever happens again.
- **`secret_scanning`, push protection and Dependabot security updates are all `disabled`** on a
  now-public repository. Nothing was found by hand, but this is free for public repositories and
  is the one setting I would turn on before the next commit.
- Issues are enabled and anonymously listable, the three issue templates are live, `has_wiki`
  false, `has_discussions` false, `github-pages` environment with one protection rule. Actions
  secrets and variables 401 to a stranger, as they must.
- **A dating trap.** The `PublicEvent` for this repository reports
  `created_at: 2026-09-21T19:55:13Z`, which is the repository's *creation* time, not the flip.
  Its event id is higher than the `MemberEvent` of 2026-09-22T14:35:52Z, so the flip is after
  that; the two Pages deployments (2026-09-22T21:28:35Z and 21:32:21Z) and the first
  non-skipped `pages` job (2026-09-22T21:28:39Z) are the timestamps of record. Anyone who
  re-checks "made public on 2026-09-22" against that feed will read a date that contradicts the
  cards; the cards are right and the feed is misleading.

**Pages itself.** `repos/…/pages` → `build_type: workflow`, `public: true`,
`https_enforced: true`, source branch `main` path `/`. Two deployments, both 2026-09-22. The
`pages` job is `skipped` in every earlier run and `success` for the first time at
2026-09-22T21:28:39Z, so ci-green's "ran for the first time on 2026-09-22" is exact.

---

## 4. `ci-green` — FAIL

The rewrite is confined to the Statement, and the Statement is **true on every clause I could
reach**: the three jobs of run 35787249180 are all `success`; its log carries
`NOT CHECKED, no knowledge base at /home/runner/work/cft-cmi/kb/projects/cft_cmi:
docs/data/extra-claim-map.json` exactly once and `41 document(s), 0 failing, 0 known`, which is
README:417's number; the `pages` job first ran on 2026-09-22; `configure-pages@v5` is present
with no `enablement:` and no `token:`; the workflow comment at `check.yml:5-6` and `62-67` says
what the Statement says. The three conditions are consistent with the evidence in the stated
order: the flip is after 14:35:52Z, Pages must have existed before the first deploy at
21:28:39Z, and the `if: false` came off in the push at 21:28:32Z.

### DEFECT L-1 — BLOCKING. The How-to-verify field was not touched, and its last clause is now the negation of the Statement

The Statement says `the if: false was removed`. Nine lines later the card instructs a reader to
check that `the pages job still carries if: false`. No job in `.github/workflows/check.yml` carries an `if:` key; the
`pages` job is lines 68-78 and the only occurrence of the string in the file is the comment at
line 6 recording that `if: false` was removed. The false instruction ships:
it is in `docs/data/extra-claim-map.json` on the live site and module 10 renders it. This is the
signature failure of this chain — the edit is right and the field beside it now says the
opposite — and the word diff shows the author changed the Statement, the `review` key and the
`updated` key, and nothing else.

**Repair R-1, verbatim.** In `How to verify` replace

> the pages job still carries if: false.

with

> the pages job carries no if: at all (.github/workflows/check.yml:68-78), ran to success for the
> first time on 2026-09-22 and is skipped in every earlier run; gh api
> repos/alexander-stottmeister/cft-cmi/pages reports build_type workflow.

### DEFECT L-2 — the `next` field names two of five deprecated actions

`next` says the Node 20 warning is on `actions/checkout@v4` and `actions/setup-python@v5`. The
`pages` job that this pass switched on adds three more, and the runner says so in the same log
the card points at: `Node.js 20 is deprecated. The following actions target Node.js 20 …
actions/checkout@v4, actions/configure-pages@v5, actions/deploy-pages@v4,
actions/upload-artifact@v4`. The card's only open item now understates its own scope.

**Repair R-2, verbatim.** In `next` replace

> The Node 20 deprecation warning on actions/checkout@v4 and actions/setup-python@v5 will become
> an error at some point and wants a version bump.

with

> The Node 20 deprecation warning now covers five actions -- actions/checkout@v4 and
> actions/setup-python@v5 in the two original jobs, and actions/configure-pages@v5,
> actions/upload-pages-artifact@v3 (which runs actions/upload-artifact@v4) and
> actions/deploy-pages@v4 in the pages job -- and will become an error at some point, so all five
> want a version bump.

---

## 5. `docs-pages-rendering` — FAIL

The Statement's new sentences are true and, for the first time, the card's founding claim is a
measurement instead of a citation. Live, anonymously, against GitHub Pages itself:
`status.md`, `index.md`, `history.md` and `notation.md` are each served **200
`text/markdown; charset=utf-8`**, verbatim, generator comment and all; `read/status.html` is
**200 `text/html; charset=utf-8`**. Site root, `read/index.html`, `read/status.html` and
`read/results/index.html` all 200 `text/html`, as the Statement says. `README` carries the
address at lines 29, 35, 36, 337, 338, 339, with section 1 at 40 and section 9 at 307-349 —
exact. The publication paragraph is gone from the README. `build_type workflow` confirmed.

### DEFECT L-3 — BLOCKING. How to verify still says Pages has never been enabled, and denies the measurement the site now makes possible

The field reads `… and Pages has never been enabled on this repository, so the content-type
claim about Pages itself rests on the documented static-file rule and not on a measurement.`
The Statement, four sentences earlier, reads `Pages is enabled on this repository with
build_type workflow, serving https://alexander-stottmeister.github.io/cft-cmi/ since
2026-09-22.` One card, two fields, flat contradiction, and the false one is served to the world
in the claim map. The word diff confirms the author repaired `Pages has never been enabled on
this repository (has_pages false).` in the Statement and left the identical claim standing in
the neighbouring field.

**Repair R-3, verbatim.** In `How to verify` replace the whole sentence

> python3 -m http.server in docs/ then curl -o /dev/null -w '%{content_type}' gives text/html for
> read/status.html and text/markdown for status.md; that measures Python's mimetypes table, not
> GitHub's, and Pages has never been enabled on this repository, so the content-type claim about
> Pages itself rests on the documented static-file rule and not on a measurement.

with

> curl -o /dev/null -w '%{content_type}' against the live site gives text/html for
> https://alexander-stottmeister.github.io/cft-cmi/read/status.html and text/markdown;
> charset=utf-8 for https://alexander-stottmeister.github.io/cft-cmi/status.md, so since
> 2026-09-22 the content-type claim is a measurement of GitHub Pages itself and no longer rests
> on the documented static-file rule alone; python3 -m http.server in docs/ gives the same two
> answers from Python's mimetypes table.

### DEFECT L-4 — the new sentence asserts something the collaborator record refutes

The rewrite turned a hedge into a historical claim: `For one day the README pointed at an
address that did not serve and said nothing about it, visible to nobody but the repository's
owner`. The README first carried the address at `e1ed92b` (2026-09-21 15:09:47 +0200) and the
explaining paragraph came off at `d3ca565` (2026-09-22 07:57:37 +0200); the site went live at
23:32 +0200. **From 2026-09-22T14:35:52Z the repository had a second collaborator with write
access** (§3), so for roughly the last seven hours of that window the state was visible to two
people, not one. "For one day" is a fair rounding of a 32-hour window and I do not fail on it;
"visible to nobody but the repository's owner" is a factual claim and it is false.

**Repair R-4, verbatim.** Replace

> For one day the README pointed at an address that did not serve and said nothing about it,
> visible to nobody but the repository's owner; all three publication steps landed on 2026-09-22
> and the address serves.

with

> From 2026-09-21 the README pointed at an address that did not serve, and from the morning of
> 2026-09-22 it said nothing about that either; the repository was private throughout, so the
> only readers were its owner and, from 14:35 UTC on 2026-09-22, the one collaborator added that
> afternoon. All three publication steps landed on 2026-09-22 and the address serves.

---

## 6. `repo-split-public-private` — FAIL

Everything measurable in the Statement still measures. `./pgit check` exit 0: `public : 626
files`, `private: 235 files`, `overlap: 0`, `uncommitted: public 0, private 0`, `shots on disk
178, tracked 178`. Private set **235 files, 48,393,112 B = 48.39 MB**, the ten enumerated paths
outside `rigor/shots` and `refs` and nothing else. `.out`: **97 = 83 + 14**, and **23** distinct
`.out` paths are named by a `doc:`/`num:`/`ref:` token, all 23 tracked. Compendium **299,915 B**
on disk. Release assets byte-identical to the local builds. **Fifteen** 40-character tokens in
four tracked notes; **nine** discarded objects, every route dead on both the owner's and the
stranger's side (§2). **Seven** public-tracked files carry a discarded-object prefix, so
"Seven … gave the route in words" reproduces. Nine private targets cited by ten cards; `make
check` prints the same nine. `623 paths on 2026-09-22` is **626** today, which is the hedge in
the same parenthesis working as designed and not a defect.

### DEFECT L-5 — BLOCKING. The card says in one sentence that the repository was made public and in another that it has never been public, and its collaborator count is wrong

The rewrite inserted `the project remote was private from its recreation on 2026-09-21 until
2026-09-22, when it was made public and the site went live` and left standing, later in the same
Statement,

> What bounded the exposure while it lasted was access control alone -- the repository has never
> been public, is unforked and has no other collaborators -- …

Two failures in one clause. `has never been public` is present-perfect and is now false, and it
is the direct negation of a sentence the same edit added — the card contradicts itself, and both
halves ship to the site. `has no other collaborators` is false as of 2026-09-22T14:35:52Z
(§3), and false already when the card was rewritten at 21:32 that evening. The
"while it lasted" framing rescues neither: both clauses are written in the present tense about
the repository as it is.

**Repair R-5(a), verbatim.** Replace

> the repository has never been public, is unforked and has no other collaborators

with

> until 2026-09-22 the repository was private, and throughout the exposure it was unforked and
> the owner was its only collaborator

**Repair R-5(b), verbatim.** Immediately after `…with a new id and holds this history and
nothing else.` insert

> Since the flip it is public, forking is allowed and there are no forks, and one further
> collaborator has held write access since 2026-09-22; none of that restores an object the
> recreation destroyed, and every route was re-run against the public remote and against an
> unauthenticated client after the flip.

---

## 7. What the rewrites left saying the opposite elsewhere

The brief asks for this explicitly, and there is more of it than in the three cards.

**X-1. `public-site-plan` — two fields, both live on the public site, both now false.** This
card is `review: passed` and was not in my packet, so I cannot fail it; it must go back to the
queue.

- `How to verify` ends `P5 is partly done (Makefile and workflow exist, Pages deployment is
  written and disabled under D1).` **Repair:** replace with `P5 is done: the Makefile and the
  workflow exist, and the Pages deployment ran for the first time on 2026-09-22, when D1's three
  steps were taken.`
- `next` begins `P5: keep the Pages job disabled until D1 is satisfied;`. **Repair:** replace
  that clause with `P5 is done: D1's three steps were taken on 2026-09-22 and the Pages job
  deploys on every push to main;` and keep the rest of the field unchanged.
- Set `review: pending` in the same commit.

**X-2. `rigor/public_site_plan.md` is world-readable and D1 and D2 now misdescribe the state.**
Line 227 reads `the Pages deployment step of P5 is written but left disabled` and line 234 reads
`marked pre-release because the papers are drafts and the repository is private`. It is not a
referee note, so it may be amended; but `ci-green` cites `public_site_plan.md:226` for the words
`one line plus one click`, so append rather than rewrite. **Repair:** add, as a new indented line
under D1 after `No paid plan is needed.`,

> Done 2026-09-22: the three steps were taken in this order -- the repository was made public,
> Pages was enabled by a REST call with a user token and build_type workflow, and the `if: false`
> came off the deploy job. The site serves.

and in D2 replace `and the repository is private` with `and the repository was private when the
tag was cut`.

**X-3. `CHECKLIST.md` item 6 survived the flip un-struck.** It reads `**Private first.** Nothing
forces an immediate public repository. Pushing privately now with these exclusions in place keeps
the public option open at no cost …`, which item 3f has superseded. CHECKLIST.md is
private-tracked, so this is a consistency defect, not an exposure. **Repair:** replace item 6's
heading and first sentence with `6. ~~**Private first.**~~ SUPERSEDED 2026-09-22 by item 3f: the
repository is public.` and keep the rest as the record of why it was safe to wait.

Checked and *not* contradicting: `generated-docs`, `interactive-site`,
`interactive-site-modules-3-4-5`, `interactive-site-modules-7-10`, `readme-and-figures`,
`plan-page` (apart from E-1), `PRIVATE.md`, and CHECKLIST items 1-5 including 3f. I ran the
pattern sweep over all 90 shipped cards rather than over the ones I expected: the six false
sentences now on the public site are ci-green's `verify`, docs-pages-rendering's `verify` and one
statement clause, public-site-plan's `verify` and `next`, and repo-split's statement clause.

---

## 8. The README, read as a stranger meets it

**Nothing in it misdescribes the state.** No sentence says the repository is private, that the
site does not serve, or that anything remains to be done to publish; the paragraph that explained
publication was removed on 2026-09-22 and nothing replaced it. Section 9 describes the mirror as
served, which it is. Section 13's "All 41 rigor documents in this repository compile" is the
number the CI log prints in a clone without the private material, and the parenthesis names the
five that are held privately. Section 12's page-excerpt and compendium paragraph matches what is
and is not in the public tree.

**The AI-provenance and human-verification framing is accurate and as prominent as it can be
made.** It is the first block on the page, above the author line and above the physics, and it
says, in bold, `Human verification is ongoing and is not finished.` and `Nothing here has yet
been checked by a human other than me, so every status on this page records what the AI review
pipeline concluded and not what a human referee confirmed.` It defines the three load-bearing
status words in the same breath, says the pipeline has missed things and that the errata are kept,
and points at section 11. Section 11 reproduces paper 1's provenance paragraph verbatim,
including `AI systems are not authors of this paper` and the author's acceptance of
responsibility, and closes with `checked twice by machine and not yet by a human referee`. I
tried to break this and could not: the framing is not buried, not hedged away, and not
contradicted anywhere else in the file.

One thing worth the author's attention rather than a repair: a second collaborator with write
access now exists, and the README's `no human other than me` is about *checking*, not about
access, so it is still true — but if that person reviews anything, the sentence becomes the first
one to update.

**One public overclaim, outside the README.** The release body says `the PDFs are the same length
as before`; `repo-split-public-private` is careful that the original assets' lengths were never
recorded, so this is "an inference from that rebuild and not a comparison". The card is right and
the release note states the inference as a fact. One word fixes it: `the PDFs are the same length
as the rebuild from the unchanged sources`.

---

## 9. Gates, printed exactly

`make check` — **exit 0**:

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
      cards awaiting a referee pass: 3 (ci-green, docs-pages-rendering, repo-split-public-private)
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

`../kb/bin/kb -p cft_cmi lint` — `0 issue(s), 3 awaiting review`.

The only change from REF-COUNTS-B's gate output is the awaiting-review line, 2 → 3, which is this
pass's three cards entering the queue.

---

## 10. Verdicts

- **`ci-green`: FAIL.** L-1, blocking: the Statement now says the `if: false` was removed and the
  untouched How-to-verify tells a reader to check that the pages job still carries it; there is no
  `if:` in the workflow and the false instruction is on the public site. L-2: `next` names two of
  the five actions the Node 20 warning now covers. Everything else re-measured and exact — three
  green jobs, the NOT CHECKED line, 41 documents, the first non-skipped pages job on 2026-09-22.
  Repairs R-1 and R-2 above, verbatim.
- **`docs-pages-rendering`: FAIL.** L-3, blocking: How to verify still says Pages has never been
  enabled, which the Statement four sentences earlier denies, and which the live site refutes —
  `.md` is served `text/markdown; charset=utf-8` by GitHub Pages itself, so the card's founding
  claim is now a measurement and the field says it cannot be. L-4: `visible to nobody but the
  repository's owner` is false for the last seven hours of the window it describes. The rest of
  the rewrite is true, including all four URLs returning 200 `text/html`. Repairs R-3 and R-4.
- **`repo-split-public-private`: FAIL.** L-5, blocking: `the repository has never been public, is
  unforked and has no other collaborators` contradicts the sentence the same edit added, and
  `no other collaborators` is false since 2026-09-22T14:35:52Z. The clearance itself I re-ran from
  a fresh clone and as an unauthenticated stranger, on the four REST routes and on the HTML, raw
  and codeload routes that only a public repository exposes, with a live-head control on each: 
  everything discarded is gone, every feed publishes only this history, and every other number in
  the Statement re-measures exactly. Repairs R-5(a) and R-5(b).
- **Outside the three cards: E-1 must be fixed before anything else** — the private plan page's
  address is on the public site with an instruction to open it — and X-1, X-2 and X-3 are
  three more places the flip left saying the opposite.
