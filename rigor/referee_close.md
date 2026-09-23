# REF-CLOSE: plan-page and repo-split-public-private (2026-09-23)

Eighteenth pass, and the fourth on the leak class. The order of work is the brief's: the three
repairs REF-ROTATE wrote out, the rebuilt guard in both directions, everything else in the two
cards re-measured, the exposure, the gates.

**Is it safe to publish?** Yes, on both readings.

*This file* is safe to publish and is public-tracked. It carries no address, old or new, no
UUID, no object, commit, tree or blob hash, and no repository id. Every demonstration below uses
the placeholder label `notallowed` — on the reserved `.example` wherever the suffix does not
matter, and on other suffixes only in §2.3, where the suffix *is* the finding; none of them is
the address of anything. It names no route that is not already named in a published field or
already visible to anyone who runs `git log` against the public remote. There is the same second reason there was last time: this note held
privately would move the private file count to 236 and the enumeration to eleven, and falsify
both halves of the parenthesis `repo-split-public-private` fixes at 235; published, it moves only
the public count, which the sentence before it hedges by name.

*The two cards* are safe to publish. Nothing either of them says is false, nothing private
reaches the public site, and the exposure is closed and stays closed.

**Verdicts: two PASS.** This is the first pass in eighteen on which the diff of the shipped
fields is exactly the repairs that were asked for and nothing else.

---

## 1. The three repairs: applied verbatim, true, and no neighbour falsified

I did not read the repairs on their own. For each I read the sentence before and the sentence
after, then the sibling card, then `CHECKLIST.md`, then `PRIVATE.md`, then the record the site
actually serves.

### T-1 — applied, true, and it repairs the sentence it sits in rather than only the clause

`plan-page`'s Statement now reads `… that address is in 41 blobs of the public history and
**could be withdrawn from it only by a second history rewrite**, and it was closed instead by
rotation on 2026-09-23 …`, character for character as REF-ROTATE gave it.

- **41 is exact, measured and not read.** Over every blob in the public object store,
  reachable *and* unreachable — 1080 of them — the old identifier occurs in exactly **41**,
  all of them versions of one generated data file, in **50** of the **85** commits now reachable
  from `main`, and in **no other path**. It is in **0** commit messages and **0** tag messages.
- **"only by a second history rewrite" is true, and it is the load-bearing half.** The 41 copies
  sit in commits *reachable* from `main`, so the one route `CHECKLIST.md` item 3 records for
  unreachable objects — a support purge — cannot touch them. What can is a rewrite of the local
  history followed by a force-push or a recreation, which is exactly the operation this project
  ran on 2026-09-21 and which the sibling card describes. Both private registers keep the same
  qualifier: item 3g says "without a second rewrite", `PRIVATE.md` says "without another history
  rewrite". The three documents now agree.
- **The neighbour survives the edit.** "It was closed **instead** by rotation" previously hung
  off "cannot be withdrawn"; it now hangs off "only by a second history rewrite", and reads
  better for it — *instead of* running the rewrite, rather than *instead of* an impossibility.
  The clause before ("this card's Statement is published verbatim on the public site") and the
  clause after ("the page was republished at a new address and the old artifact deleted, so every
  published copy of the old address is now dead") are untouched and both hold.
- **It is live.** The claim map served today is byte-identical to the one on disk, and carries the
  repaired clause; "cannot be withdrawn" returns **0** from it.

### T-2 — applied, true, and it closes the third recurrence of K-6/G-3

`PRIVATE.md` now reads "… the old artifact **was deleted on 2026-09-23**, at which point every
published copy of the old address **became inert**. **CHECKLIST item 3g is closed.**", verbatim.

The document this Statement sends the reader to now says what the Statement says. Read with its
neighbours: the sentence before it ("It cannot be withdrawn from there without another history
rewrite") is the qualifier T-1 restored to the card, and the sentence that introduces the
replacement ("The chosen close was to rotate: this page now lives at the address above, and …")
runs into it cleanly. Nothing else in that section moved, and the two figures it carries — 41
blobs, 50 reachable commits — are the two I measured. `PRIVATE.md` records the publication date
and the source length in place of the version to republish; the length it gives is the file's,
which is 167 lines, and no card claims `PRIVATE.md` records a version.

### T-3 — applied, true, and consistent with the register it points at

`repo-split-public-private`'s `next` now reads "**One item survives, and one was closed on
2026-09-23. The closed one** is in this repository and is recorded in CHECKLIST.md item 3g rather
than here, because a published field is where it was leaked in the first place; **what remains of
it is inert. The one that survives:** the knowledge-base repository carries …", verbatim.

- Item 3g is struck through and headed `CLOSED 2026-09-23 by rotation`. The field no longer counts
  it among the survivors, and "what remains of it is inert" is the same thing the sibling card
  says on the same page ("now dead") and the same thing item 3g says.
- The surviving item is the knowledge-base sweep, and item 3d is where it lives. Item 3d now also
  records the files of that repository which still carry the dead address, folded into the same
  sweep — so `next`'s "one item survives" is not undercounting: there is one sweep, with two
  things in it, and the field points at the item that holds both.
- Neighbours: "Publication is done: decision D1's three steps were run on 2026-09-22, in that
  order, and the site serves" before, "CHECKLIST.md items 3 to 3e record the clearance …" after.
  Neither is touched and both still hold.

### What else changed in the shipped fields — nothing

I diffed the claim map as it stood when REF-ROTATE reviewed it against the one served today,
field by field and sentence by sentence. The entire difference is: T-1; T-3; the two measured
drifts; the `review` key; and `verdicts` 3→4 and 27→28. **No third deletion, no spliced clause,
no orphaned punctuation, nothing silently dropped.** The chain has failed five consecutive passes
on a repair that moved a value and left the sentence beside it standing; this time there is
nothing beside the repairs to have left standing.

The two drifts are right, and taken in the right form:

- `436 files, 201.6 MB on 2026-09-23` for the set tracked by neither repository. I measure
  **437 files, 201,942,812 B** today; removing this review's own packet leaves **436** files and
  **201,688,861 B**, which is 201.6 MB under the card's own truncating convention. The one-file
  difference is precisely the mechanism the following clause names.
- The private-count hedge now reads "it moves on every private commit — a new page excerpt, a new
  source PDF, or a note held here rather than published", which is the substance of R-3(d): it
  names the two ordinary ways the count moves and not only the one that broke it last time.

---

## 2. The guard, both directions — and an eleventh

I called the real functions on every form, and drove the survivors end to end through the real
`build_claim_map()` against a **copy** of the knowledge base, reading the string back out of the
JSON that would be written. The knowledge base itself was not edited.

### 2.1 Everything the last three passes found, re-run

| form | previous guard | rebuilt guard |
|---|---|---|
| `https://notallowed.example/x` (the control) | caught | **caught** |
| `https:/notallowed.example/x` — REF-ROTATE's tenth | passed | **caught** |
| `_notallowed.example/x_` — Markdown emphasis | passed | **caught** |
| `…notallowed.example/x` — ellipsis before a bare host | passed | **caught** |
| `.notallowed.example/x`, `/notallowed.example/x` | passed | **caught** |
| `https:\\notallowed.example\x` | caught | **caught** |
| soft hyphen, ZWSP, ZWNJ, ZWJ, word joiner, BOM as separators | caught | **caught** |
| fullwidth full stop | caught | **caught** |
| `?@` and `#@` authority (REF-GUARD 2.2) | caught | **caught** |
| userinfo `@`, `host:port@` (REF-GUARD 2.1) | caught | **caught** |
| `file:`, `data:`, `javascript:` and the rest of the deny-list | caught | **caught** |
| uppercase host | caught | **caught** |

All three of REF-ROTATE's tenth-finding regressions are closed, and closed the right way: the
authority branch now tolerates any run of slashes after a scheme, exactly as a WHATWG parser
does, and the lookbehind that caused them is gone. The source comment has also stopped claiming
what NFKC does not do — the sentence that said the ideographic stops were covered is no longer
there. (One residual inaccuracy in that comment: a soft hyphen does not "IDNA-normalise to a
dot"; UTS #46 *ignores* it. The code does the right thing; only the reason given is wrong.)

Known and previously judged tolerable, all unchanged: a percent-encoded separator
(`notallowed%2Eexample/x`), a bare IP address, the ideographic and halfwidth-ideographic stops,
the ignored code points UTS #46 strips and `_INVISIBLE` does not list. To those I add three more
of the same species, from the lookahead rather than the lookbehind: a bare host followed by `?`,
by `\`, or by a trailing dot is not seen. None of them is new in kind.

### 2.2 The other direction: the rebuild is right where it was wrong

Called on the sentences REF-ROTATE tabled: "What this card is about: …", "Data: the 97 tracked
.out files …", "File: rigor/referee_leak.md …", "The two documents are CHECKLIST.md/PRIVATE.md",
`w3.org/1998/Math/MathML`, `raw.githubusercontent.com/…`, `en.wikipedia.org/…`, `dx.doi.org/…`,
`gist.github.com/…`, `api.github.com/…`, `packages.ubuntu.com/…`, `main.log`,
`branch.main.remote`, `docs/data/extra-claim-map.json`, `rigor/cited_R1..R4.tex`,
`plan_page/petz_program_plan.html`, `./pgit check:`, `v0.1.0-draft:` — **every one passes.** The
author can write these cards again.

Swept over the full text of all **330** card files, every section and not only the three that
ship, what remains is **four** patterns in **three** cards, down from five: `file:` in a card
documenting the scheme (one), and `about:`/`Data:`/`File:` quoted with a closing apostrophe
inside REF-ROTATE's own note about these very false positives (three). The fourth,
`example.com` inside a full URL, is a correct refusal of a harmless host, not a false positive.
All of them are in Notes, which do not ship. Over the **shipped** fields — Statement, How-to-verify
and `next` of all cards — **0 trip the guard**, and `make check` is green.

The `(?=\S)` repair is therefore right but one notch too narrow: a deny-listed word followed by a
quote, an apostrophe or the end of a field still counts as a URL. REF-ROTATE's other option —
require a `/` — would have cost nothing and closed it.

### 2.3 The eleventh, and it is the tenth's twin

    _TLDS = {"com", "org", "net", … "tv", "ly", "example"}   # about fifty
    def _is_hostlike(host): return "." in host and host.rsplit(".", 1)[-1] in _TLDS

This gate is new in this rebuild, and it is applied to **both** branches — the authority branch
as well as the bare-host branch. So it is not a heuristic for bare hosts; it is the last word on
every candidate the guard finds.

**A complete, scheme-bearing, two-slash URL on a real registrable TLD that is not on the list
passes the guard entirely.** Of 54 real TLDs I tried — `.store`, `.link`, `.tech`, `.blog`,
`.online`, `.space`, `.pub`, `.sh`, `.me`, `.to`, `.wiki`, `.is`, `.so`, `.id`, `.fi`, `.no`,
`.be`, `.pl`, `.cz`, `.us`, `.kr`, `.tw`, `.sg`, `.il`, `.pt`, `.ro`, `.hu`, `.ie`, `.gr`,
`.click`, `.live`, `.today`, and the rest — **54 of 54 pass**, in every form:

| form | previous guard | rebuilt guard |
|---|---|---|
| `https://notallowed.store/code/artifact/AAAA` | **caught** | **passes** |
| `notallowed.store/code/artifact/AAAA` | **caught** | **passes** |
| `https://github.com@notallowed.store/x` | **caught** | **passes** |

I reconstructed the previous version from the repository's own history rather than from a
description of it, and ran both. And I drove three of these end to end: written into a card's
Statement in a scratch knowledge base, `build_claim_map()` completes, `check_payload` raises
nothing, and the address appears **verbatim** in the JSON that would be written to the claim map
and rendered by module 10. The two-slash control on an on-list TLD raises, as it should.

**Why this is the chain's signature failure and not a new class.** REF-GUARD's finding 2.4 was
"nine hard-coded suffixes". The previous rebuild answered it with `[a-z]{2,}` — any TLD — and
REF-ROTATE certified 2.4 as answered. This rebuild needed something to stop `main.log` and
`branch.main.remote` being read as hosts once the lookbehind was removed, and reached for a
suffix list again: fifty instead of nine. **The repair for the tenth re-opened the finding the
repair before it had closed.** It is the same one-character-wide gap logic as the tenth, in the
same function, introduced by the same kind of narrowing.

**And the list cuts both ways, which is the argument against the approach rather than against the
list.** The same fifty entries that let `notallowed.store/x` through make the guard refuse any
dotted token whose last label happens to collide with them. `user.name:` — a git configuration
key, the exact species of `branch.main.remote` that the list was added to protect — is
**refused**, because `name` is a TLD. So is `scipy.io:`. Neither occurs in the cards today; both
are one sentence away. A rule that admits `.store` and refuses `user.name` is not calibrated; it
is a coincidence table.

**One mercy, and it is only that.** The hosts this project actually has to refuse all sit on TLDs
that happen to be on the list, so today's instance stays closed and nothing ships. The *class*
does not.

**Repair.** Two lines would stop the bleeding — allow any `[a-z]{2,}` final label again and
exempt a short list of file extensions instead — but that is the third swing of the same pendulum,
and the pendulum is the problem. The right move is REF-GUARD's recommendation 3 and REF-ROTATE's,
restated once more and now with a second, independent reason to take it: **stop deciding what a
host is with a character class.** Fold with UTS #46, percent-decode, extract with a real URL
parser, and allow-list what the parser returns. That closes the eleventh, the tenth's three
residuals, 2.3, 2.5 and the ideographic stops together, and it removes the false-positive
direction entirely, because a parser knows `user.name` is not a URL without being told.

### 2.4 Two smaller things

- **The sweep got slower, as a direct cost of the tenth's repair.** Removing the lookbehind
  removed the pruning with it: a pathological dotted run now takes 2.4 s at 8 kB, 9.1 s at 16 kB,
  29 s at 32 kB and **126 s at 64 kB**, against 0.34 / 1.5 / 7.3 / 29 s for the version
  REF-ROTATE measured — four to seven times slower, same quadratic exponent. The real claim map,
  265 kB and not pathological, sweeps in **0.11 s**, so this is not an operational problem; it is
  a cost that was paid without being noticed.
- **All four places the guard does not run are unchanged.** CI still passes
  `--allow-missing-kb`, which drops the claim map — the one payload built from card prose — so the
  guard has still never run in CI. `build_docs.py` still has no guard at all
  (`grep -c 'ALLOWED\|foreign\|check_payload'` is **0**), and it is the generator that ships
  *prose*. The `pages` job still carries no `needs:`, so a push deploys `docs/` whether or not
  the other jobs pass. `make data` still ends in `|| true`.

### 2.5 Is the guard fit for the job?

**No, and the approach should change.** As an *instance* defence it is sound today: it catches
every form the last three passes found, it no longer refuses ordinary prose or this project's own
filenames or the hosts the cards legitimately cite, the hosts that matter here are on the list,
and nothing trips it in anything that ships. As a *class* defence — which is the only thing it
was written to be, since the class is "an address nobody thought about reaching the site" — it is
not. Three rebuilds in three days have each closed the previous finding by narrowing a regular
expression and each opened the next one by the same act. That is not a run of bad luck; it is what
happens when a URL is recognised by pattern instead of parsed. Parse it.

---

## 3. Everything else in the two cards, re-measured

### `plan-page`

| claim | measured today |
|---|---|
| source at `plan_page/petz_program_plan.html` | present, **167** lines |
| `grep 'Status (10 Sep)'` | **1** |
| tracked in the private companion | **1** in the private index |
| in no commit of the public history | `git ls-files` **0**; **0** of the paths ever added over **all** refs; **0** in the tree of the draft tag |
| the artifact URL is recorded in `PRIVATE.md` and not here | present there; **0** occurrences of an artifact host or route in the card |
| the Statement is published verbatim on the public site | true, and in exactly **one** of the 188 deployed files |
| `verdicts` / `refereed` in the served claim map | **4** / true (REF-ROTATE measured 3 before its own verdict) |
| How to verify, executed as written | both steps run and return what they say |
| evidence token | resolves |

The 2026-09-14 History line is in place, immediately after `- 2026-09-14 created`, and it is what
carries the count. The `review` key still names only the last failure; REF-ROTATE judged that a
preference rather than a defect and I agree — the generator reads History, and History is right.

**The one limit, restated so the next reader does not mistake a green probe for proof.** The
Statement asserts a deletion. No anonymous observation can confirm or refute a deletion for an
address of the old shape, because the route serves the same bytes for a deleted artifact, a
private one, and an identifier that cannot exist. §4 says exactly what I could measure. The claim
is not therefore wrong; it is attested by the owner and by item 3g, and everything measurable is
consistent with it.

### `repo-split-public-private`

| claim | measured today |
|---|---|
| public / private / overlap, `./pgit check` | **630** / **235** / **0**, uncommitted 0 and 0 |
| `shots` on disk and tracked | **178** / **178**; `refs/*.pdf` **47** |
| the ten private paths outside those two directories | exactly the **ten** the Statement names, and exactly what `ls-files` lists |
| 97 tracked `.out`, 83 + 14, one a bookmark file | **97 = 83 + 14**; exactly **one** opens with a bookmark |
| 23 named by a card's evidence token | **23**, under the any-token rule *and* the front-matter rule |
| 255 `\shot`/`\shotc` call sites in 19 documents | **256** across 20 `.tex` less the one in the preamble = **255 in 19** |
| 24 python scripts resolve against a computed `_ROOT` | **24** (**25** counting the rewriter); **0** tracked `.py` carries the machine literal |
| four shell scripts honour `$PYTHON` | **4** |
| local builds unchanged: 42 pp with images | `network_corner_calculus` **42 pp**, **10** embedded images, 10 call sites |
| 27 pp / 8 images locally | `quadratic_limit` **27 pp**, **8** embedded images |
| the compendium at its full length | **299,915 B** |
| release rebuilt with the same two assets | **629,891 B** and **607,822 B**, exact |
| created 2026-09-21, new id, public, unforked, one further collaborator | created **2026-09-21T19:55:13Z**; private false, fork false, forks **0**, `allow_forking` true, collaborators **2** |
| the companion remote private since 2026-09-20 | **private**, created **2026-09-20**, its head equal to the local one |
| the tag's tree is clean | **403** files, **0** forbidden |
| paths ever added, "623 on 2026-09-22", hedged | **630** ever added, **649** ever present in any tree of any ref; **0** private, **0** hidden by the ignore rules |
| tracked by neither, 436 / 201.6 MB | **437** / 201.9 MB, i.e. **436** and 201.6 MB less this review's packet |
| nine private targets cited by ten cards | **9** / **10**, and `make check` prints the same nine |
| `restore.sh` recovers one of the six under the cited name | **one** (VWZ); Uhlmann76 tabled `MANUAL -- paywalled`; CDIT tabled as CDIW21; the other three are bullets, not table rows |
| licensing, `THIRD-PARTY.md` | MIT for code, CC BY 4.0 for documents, "None of that material is redistributed here" |
| `./pgit (status, sync, check, push)` | `sync` and `check` are implemented, `status` and `push` pass through to git; all four work |
| the review packets are tracked by neither | **35** on disk, **0** and **0** |
| `rigor/README_AGENTS.md` section named in How to verify | present |
| every evidence pointer resolves | `kb -p cft_cmi lint` — **0 issues** |

**Recorded, not defects.**

- The K-8 parenthesis is still doing two jobs. "…so neither of those two counts is fixed here" is
  followed twelve words later by "(235 files on 2026-09-23…)", which fixes one of them. It is
  dated, it is hedged, and the number is right — so this is wording and not falsehood, and I say
  so and pass, as the last two passes did. But it is the fourth pass to land on this parenthesis,
  and the cheap fix has been available all along: say "so the public count is not fixed here", or
  drop the clause. The expensive fix is the right one and REF-ROTATE named it — nothing in a
  Statement should be a number that a referee's own artefact moves.
- Both dated figures are, by construction, one review packet stale the moment this packet exists.
  That is what the hedge predicts and it predicted it correctly.
- `CHECKLIST.md` item 3d now records the knowledge-base files still carrying the dead address,
  as REF-ROTATE asked. Its count of **six** is right today: I find six, but they are distributed
  differently from the way REF-ROTATE described them — two generated, **three** under `import/`
  and **one** under `seed/`, not four under `import/`. Item 3d gives only the total, so it is
  correct as written; the breakdown is recorded here so the sweep looks in the right places.
- `secret_scanning` and its push protection are still disabled. This is now REF-LIVE's
  recommendation unanswered for the fifth pass, and it is the one control that would have caught
  this class at the push rather than four referee passes later.

---

## 4. The exposure: still closed, and nothing private reaches the site

Everything below was run unauthenticated, with no cookie and no token, and everything that could
be run against a control was.

**The old address yields nothing.** Four routes plus the short-host redirect, each against an
identifier of the same shape that cannot exist: every status code identical, every body length
identical to the byte, and `grep` for `Status (10 Sep)`, `Petz`, `CMI`, `quadratic`, `recovery`
and `programme plan` returns **0** on every body. The Internet Archive's index returns **no
snapshot** for the primary form; for two of the other forms the index was serving its own
"temporarily offline" page while I worked, which I record rather than count as a clean result.

**The 41 copies are still there and still inert.** All four routes item 3g records serve them
anonymously today — the raw file host, the blob view, the blob API and the tarball, all **200**,
and the file they return carries the old identifier. They were not removed, and no document says
they were. That is exactly the state item 3g, the card and `PRIVATE.md` describe.

**The new address is published nowhere.**

- The deployed site: I fetched **all 188 files anonymously**, one request each — **188 of 188 at
  200**, and **0 of 188** differing from `docs/` on disk by a byte, so the tree I swept is the
  tree the world is served. Over those 188 files: **0** occurrences of the new identifier, **0**
  of the old one, **0** of any artifact host or publish route in any case.
- The public repository: **0** in all **1080** blobs of the object store, reachable and
  unreachable; **0** in every commit message and in the tag message.
- The knowledge base: **0** in all **1741** files of its working tree.
- On this machine, outside the two git directories, the new identifier occurs in **exactly one
  file**, which is private-tracked and in the public `.gitignore`.

**Nothing private reaches the site.** The only private material that appears in the 188 deployed
files is private *path names*, each rendered with the "(held privately)" marker the extractor
adds and none of them a link — the nine `make check` prints. No excerpt, no source PDF, no
compendium, no line of the plan page. Over all **649** paths that have ever been present in any
tree of any ref of the public repository, **0** is an excerpt, a PDF, a compendium, the plan page,
`PRIVATE.md`, `CHECKLIST.md` or `pgit`, and `git check-ignore` hides none of them.

Both Statements ship verbatim, and in exactly one deployed file each: the claim map. The served
copy of that file is byte-identical to the one on disk.

---

## 5. Gates, printed exactly

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
      cards awaiting a referee pass: 2 (plan-page, repo-split-public-private)
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

`make rigor` — **exit 0**: `python3 tools/check_rigor_builds.py`, then **46** `ok` lines, then

    46 document(s), 0 failing, 0 known

`../kb/bin/kb -p cft_cmi lint` — `[cft_cmi] 0 issue(s), 2 awaiting review`, the two being the
cards of this packet.

All three were run **before** the verdicts were recorded, which is the state in which I found the
project. The standing contradiction REF-GUARD recorded is unchanged and I did not treat it as a
defect: `make check` prints `cards whose last referee pass failed: 0` while the claim map on the
same site marks both cards `review_failed: true`. Neither number is false under its own
definition and nothing compares them.

**After the verdicts**, as the Makefile's own header predicts, `make check` is red at
`tools/build_docs.py --check` — exit 2, `build_docs --check: the committed documentation has
drifted from the knowledge base`, the whole difference being `review pending` going blank for
these two cards in `read/status.html` and `status.md`, with `cards awaiting a referee pass: 0`
and `cards whose last referee pass failed: 0`. `make rigor` is unaffected and stays exit 0.
`kb lint` is `[cft_cmi] 0 issue(s), 0 awaiting review`. Rebuilding and committing is the author's
step, not mine — and this time the rebuild will also make the two counts agree for the first time
in this chain, because a passed verdict clears `review_failed` in the claim map as well.

---

## 6. Verdicts

- **`plan-page`: PASS.** T-1 is applied verbatim, is true — 41 blobs measured over every object
  in the store, and the qualifier it restores is the one both private registers keep — and
  repairs rather than damages the clause that follows it. T-2 is applied verbatim, and the
  document this Statement sends the reader to now agrees with it. Everything else re-measures:
  167 lines, one `Status (10 Sep)`, nothing in any commit of any ref, tracked privately, the
  address recorded only in the one private file, the Statement published verbatim in exactly one
  deployed file. The deletion is the one claim anonymous work cannot settle, and the card does not
  claim more than the evidence bears.
- **`repo-split-public-private`: PASS.** T-3 is applied verbatim and true: item 3g is closed, and
  the field no longer counts it among the survivors. Both drifts were taken, both are right, and
  the private-count hedge now names the two ordinary ways the count moves rather than only the one
  that broke it. The whole clearance re-runs. The K-8 parenthesis is still wording I would have
  written differently, and I say so and pass.
- **The exposure is closed.** The old address returns nothing but the shell on every route,
  byte-indistinguishable from an identifier that cannot exist; the 41 copies remain in the public
  history, still served, and dead; the new address is in no deployed file, no object, no message,
  no metadata surface and no part of the knowledge base, and lives in one private-tracked file.
- **The guard: not fit as a class defence, and the approach should change.** It now catches every
  form the last three passes found and refuses none of the prose, filenames or hosts it was
  wrongly refusing. But the new TLD allow-list is an **eleventh** finding and it is the tenth's
  twin: fifty hard-coded suffixes in place of "any TLD", which REF-GUARD had already failed at
  nine and the previous rebuild had already fixed. A complete two-slash URL on any of 54 real
  TLDs I tried passes end to end into a claim-map payload, and the same list refuses `user.name:`.
  Nothing ships today and the hosts this project must stop are on the list, so no card fails for
  it. Parse the URL; stop matching it.

**This report is safe to publish.** It carries no address, old or new, no UUID, no object,
commit, tree or blob hash and no repository id, and every demonstration uses the placeholder
label `notallowed`, which is the address of nothing.
