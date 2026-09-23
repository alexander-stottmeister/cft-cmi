# REF-LEAK: the prose-leak repair and five cards (2026-09-23)

Fifteenth pass, and the first after E-1. The order of work is the brief's: whether the leak is
actually closed on the live site rather than only on disk, then whether the new guard is sound,
then the five cards, then X-2 and X-3, then the repository's new description and homepage, then
the figures REF-LIVE did not certify, then the gates.

**A note on this file.** It carries no hexadecimal token of any object, no commit hash, no blob
name, and it does not reproduce the artifact address. Two live measurements inside
`repo-split-public-private` count the tracked files that carry such tokens ("the notes carry
fifteen such tokens", "Seven public-tracked files in this repository gave the route in words");
both were re-measured today and both still hold after this file is added, and a report that
quoted one would move the number it is checking. The address is the thing being withdrawn, so
quoting it here would republish it a second time, in a second public-tracked file.

**And a warning about where this file goes — acted on while the pass was running.** Every other
`rigor/*.md` is public-tracked, so this note would have been world-readable, and §0 tells a
reader that the address is still recoverable and which file carries it. That is a signpost to an
exposure that is still open, so I withheld the enumeration recipe as well as the address, and
recommended that the note be held in the private companion until E-2 is closed. Between my
writing that and my recording the verdicts, the project did it: `.gitignore` gained a rule for
this path with a comment naming CHECKLIST item 3g, `pgit`'s `PRIVATE_PATHS` gained it, and the
private companion committed it as "hold the leak note until E-2 is closed". **This file is
therefore private-tracked and is not published**, which is the right answer and was taken before
the note ever entered the public history. Two consequences, both in this report: `./pgit sync`
is still needed, because I edited the file after that commit; and moving it changed a figure a
card asserts — see K-8. The `.gitignore` rule itself is public, and its comment says that a
withheld note about an unclosed exposure exists; that is a much weaker signpost than the note,
and I record it rather than object to it.

**Verdicts: one PASS and four FAIL.** The exposure is *not* closed and comes first; it is not a
finding about any one card, and the repair for it is an action before it is a sentence.

---

## 0. STILL EXPOSED — the address was withdrawn from the tip of the branch, not from the public record

**E-1 is applied exactly as REF-LIVE wrote it, and the check it named passes.** The address and
the version are in `PRIVATE.md` under a new heading; the Statement and the How-to-verify are the
two replacement paragraphs word for word; `docs/data/extra-claim-map.json` was regenerated and
committed; and `grep -c 'claude.ai' docs/data/extra-claim-map.json` is **0**, as E-1 required.
Anonymously, over the whole deployed tree, there are **0** occurrences of the address, **0** of
its UUID, **0** of any fragment of it, and **0** of the string `claude.ai` in any case (§1).

**And the address is still world-readable, anonymously, from this repository, today.** The card
generated it into a tracked file for two days, so it is in the history of a public branch:

| measured on an anonymous clone and by anonymous HTTP | value |
|---|---|
| commits on `main` whose tree carries the address | **50** of 81 |
| distinct blobs of `docs/data/extra-claim-map.json` that carry it | **41** |
| window | first commit 2026-09-21 09:24 +0200, last 2026-09-22 23:32 +0200 |
| other tracked paths that ever carried it, over all refs | **0** (two notes name the host, neither the address) |
| tree of the tag `v0.1.0-draft` | clean |

It is not merely present; it is *served*, with no credentials and no clone, on four routes, each
checked today with a live-head control:

| anonymous route | result |
|---|---|
| `raw.githubusercontent.com/OWNER/REPO/<commit>/docs/data/extra-claim-map.json` | **200**, carries the address |
| `github.com/OWNER/REPO/blob/<commit>/docs/data/extra-claim-map.json` | **200** |
| `api.github.com/repos/OWNER/REPO/git/blobs/<blob>` | **200**, decodes to the address |
| `codeload.github.com/OWNER/REPO/tar.gz/<commit>` | **200**, the file in the tarball carries it |

**No hash has to be guessed, and nothing has to be brute-forced.** The commits are reachable
from `main`, so the ordinary public listing of that path's history hands over every SHA needed,
and on a clone a single stock `git` invocation finds the string. I verified this end to end and
am deliberately not writing the two calls out here, because this note is itself public-tracked.
This is not the situation the nine discarded objects are in: those are unreachable and every
route against them 404s, which I re-ran (§5). These 41 blobs are *reachable from `main`* and
every route against them succeeds.

**What is out is the capability, not the document.** I re-ran REF-LIVE's reachability probe and
extended it. An anonymous `GET` of the artifact address returns **200**, 22,796 B, titled
`Claude Artifact`, carrying none of the plan text; `grep 'Status (10 Sep)'` over it returns 0.
The public-artifact route returns 200 and 124,362 B, but so does the same route with a UUID that
cannot exist, byte-for-byte the same length — it is the application shell, not the artifact. So
the plan page's *content* is still not world-readable, exactly as REF-LIVE reported. What is
world-readable is a permanent, unguessable, non-expiring address, and it is now trivially
discoverable rather than merely present.

**Repair E-2, and it is an action before it is a sentence.** Withdrawing the address from the
tip did not withdraw it. Close it by whichever route the user prefers:

- **(a), recommended and cheap:** republish the plan page as a **new** artifact, delete the old
  one, and record only the new address in `PRIVATE.md`. Every one of the 41 copies then becomes
  inert, exactly as the discarded-object hashes in the seven kept notes are inert, and nothing
  in git has to move.
- **(b):** clear the blobs from the public history by the second of the two routes CHECKLIST
  item 3 already records for the compendia.

Then, and only then, replace the Statement's last sentence

> The artifact URL and the version to republish are recorded in PRIVATE.md and deliberately not
> here, because this card's Statement is published verbatim on the public site.

with

> The artifact URL and the version to republish are recorded in PRIVATE.md and deliberately not
> here, because this card's Statement is published verbatim on the public site; an earlier
> version of this Statement published an address, and that address has since been withdrawn and
> is dead.

**Until it is closed, nothing published may name it.** Do not write the address, the file that
carries it, or the route to it into any Statement, How-to-verify or `next` field: those three
are precisely what module 10 ships, and a published field is where this leaked in the first
place. The register entry belongs in `CHECKLIST.md`, which is private-tracked; see Repair R-3(a).

---

## 1. Everything else served, swept file by file, and clean

I did not sample and I did not trust the claim map. I fetched **all 188 files** of the deployed
tree anonymously, one request each, every one **200**; the mirror is byte-identical to `docs/`
on disk, and `docs/` on disk equals `docs/` at HEAD, and the latest `github-pages` deployment is
HEAD. So the tree I swept is the tree the world is served.

**Every absolute URL in the whole deployed tree, by host** — enumerated by regular expression
over every byte of every file, not read off the claim map:

| host | occurrences | where |
|---|---|---|
| `github.com` | 316 | 313 `blob/main/…`, 1 releases, 1 repository root, **1 `cft-cmi-private`** |
| `www.w3.org` | 13 | SVG and MathML namespace declarations |
| `projecteuclid.org` | 3 | `sources.md` and its mirror |
| `alexander-stottmeister.github.io` | 3 | the site's own address, in the repaired `docs-pages-rendering` How-to-verify |

Four hosts, all in `check_links.py`'s allowed set. **No `claude.ai`, in any case.** Also swept
for, and absent: scheme-relative `//host/` URLs (**0**), bare hostnames outside the two above
(**0**), `file:`, `mailto:`, `data:` and `ftp:` URLs (**0**), e-mail addresses (**0**), GitHub /
AWS / Slack tokens and PEM private keys (**0**), Windows paths (**0**), full 40-hex tokens
(**0**), UUIDs (**0**), Actions run ids (**0** — the only match is a KaTeX constant), `/home/…`
paths (**0**). The 20 vendored KaTeX fonts carry no URL or path in their strings.

**The wider class, and the two things that *are* pointed at and are not public.** Both are in
the `repo-split-public-private` Statement and both are deliberate:

- `https://github.com/alexander-stottmeister/cft-cmi-private` — the companion remote. Verified
  **404 anonymously**; a private repository's URL is a name, not a capability.
- `claude-team-kb`, the knowledge-base repository, named but not linked. Verified **404
  anonymously**.

Neither is an exposure, and I record them so that a later pass does not read them as one. The
same goes for `/Users/alex`, which occurs **once** in the deployed tree, inside the `repo-split`
Statement, and for the private paths the site prints as `… (held privately)` — CHECKLIST item 4
and REF-LIVE both record those as decisions.

**Negative probes**, all **404**: `README.md`, `CHECKLIST.md`, `PRIVATE.md`, `pgit`,
`pgit-exclude`, `.gitignore`, `Makefile`, `plan_page/petz_program_plan.html`,
`rigor/public_site_plan.md`, `rigor/referee_live.md`, `rigor/shots/`, `.git/config`,
`../README.md`, `data/` as a directory.

---

## 2. Is the guard sound? `_no_foreign_url` — what it catches, what it does not, and where it never runs

I read it and then tried to get a foreign URL past it, by calling the real function and, for the
forms that survived, by driving the real `build_claim_map()` against a scratch copy of the
knowledge base and reading the address back out of the emitted JSON.

`ALLOWED_PROSE_HOSTS` is `{github.com, alexander-stottmeister.github.io, projecteuclid.org,
arxiv.org, doi.org, creativecommons.org, orcid.org}` and the extractor is
`_URL = re.compile(r"https?://([^/\s)>\]\"']+)")`, compared as `host.lower().split(":")[0]`.

**Caught** (each raises `Drift` naming the card, the field and the host): a plain `https://`
URL; an **uppercase host**, because the host is lower-cased before the test; a URL inside a
**code span**; a **Markdown link** target; an **angle-bracket autolink**; a URL with a **port**
(the port is stripped and the host still tested); **userinfo** of the form `user@host` and
`u:p@host`; a punycode host. It is field-blind in the right way: the delimiter class stops the
host at `/`, `)`, `>`, `]`, a quote or whitespace, so Markdown never hides one.

**Not caught.** Five forms pass, and I confirmed the first three end to end — written into
`plan-page`'s Statement they appear verbatim in the rebuilt claim map:

1. **An uppercase or mixed-case scheme.** `_URL` is compiled without `re.I`, so `HTTPS://…` and
   `Https://…` are not matched at all. The host is lower-cased, the scheme is not.
2. **A scheme-relative URL**, `//claude.ai/…`. Browsers resolve it; the guard does not see it.
3. **A bare host**, `claude.ai/code/artifact/…`. This is the form the original leak was
   *nearly* in, and it is the form a human writes when trimming a long line.
4. **Any other scheme**: `ftp:`, `file:///Users/…`, `mailto:`, `data:`.
5. **A userinfo that contains a colon and begins with an allowed host**:
   `https://github.com:1234@claude.ai/…`. `split(":")[0]` yields `github.com`, which is
   allowed, and the real host is `claude.ai`. Contrived, but it is the one case where the
   host-vs-userinfo confusion resolves in the attacker's favour rather than the defender's.

**One false positive**, worth knowing before it stops a build: an *allowed* host-only URL
followed by punctuation — `see https://github.com.` — is extracted as `github.com.` and raises.
Any URL with a path is unaffected, because `/` terminates the host.

**The `(held privately)` masking cannot smuggle a URL past it.** `_mark_private` runs first, as
the inner call, and inserts only the literal ` (held privately)`. I checked the two ways it
could interfere and neither works: it cannot *introduce* a host, and it cannot *hide* one,
because every private path it matches lies in the path part of a URL, after the `/` at which
`_URL` has already stopped. A private token inside a hostname (`https://pgit.example/…`) is
still caught, on the mangled host.

**The fields it covers are not the only ones that reach the site.** `_no_foreign_url` is applied
to `statement`, `verify` and `next`. The same card dictionary also ships, unguarded and
unmasked: **`title`**, **`review`**, `evidence[].path`, `evidence[].anchor`,
`evidence[].target`, `area`, `status`, `type`, `confidence`, and every area card's `title`. I
tested `title` and `review`: with a foreign URL in each, `build_claim_map()` succeeds and both
strings appear in the payload, so both would be served.

**And there is a second generator, with no guard at all.** `tools/build_docs.py` also publishes
card prose verbatim — `docs/results/<id>.md` carries Statement, How-to-verify, Evidence and
Review, `docs/open.md` carries the Statement of any open or conjectural card that has no page,
`docs/status.md` and `docs/index.md` carry titles — and their HTML mirrors under `docs/read/`
ship too. `grep -c 'ALLOWED\|foreign' tools/build_docs.py` is **0**. Its output is partly covered
by `check_links.py`, but only accidentally: `md_to_html.py` autolinks a bare URL, so a foreign
URL in a *mirrored* page becomes an `href` that `check_links.py` rejects. `check_links.py` does
not scan `.json` at all, and does not see a bare URL in a `.md`. That is exactly why the original
leak was invisible to `make check`: it lived in a JSON payload, which nothing links-checks, and
`plan-page` has no generated page, so the only surface that carried it was the one with no
coverage.

**Where the guard does not run: continuous integration.** `.github/workflows/check.yml:32` runs
`build_site_data_extra.py --check --allow-missing-kb`, and with the knowledge base absent
`main()` *pops the claim-map builder off the list entirely* — `build_claim_map()` is never
called, so `_no_foreign_url` is never called. The guard is a **local pre-commit gate only**, and
it holds exactly as far as `ci-green`'s own `WHAT THE FLAG DOES NOT DO` paragraph says the drift
check holds: as far as a human running `make check` in a clone with the knowledge base beside
it. The `pages` job additionally carries no `needs:`, so a push deploys `docs/` whether or not
the other two jobs pass.

**Verdict on the guard.** It closes the instance and most of the class, and its diagnostic is
good — it names the card, the field and the host, and it tells the author where to put the
address instead. It does not close the class. Recommended, in decreasing order of value, and none
of it blocking a card:

1. Compile `_URL` with `re.I` and widen it to `(?:[a-z][a-z0-9+.-]*:)?//` plus a bare-host
   alternative, or, better, strip any `userinfo@` before the host test and run the whole field
   through a second pattern for "anything host-shaped".
2. Apply it to `title` and `review` as well, which costs two lines.
3. Apply it in `build_docs.py`, which is the other half of the surface.
4. Have CI fail when it cannot check the claim map *and* the diff touches a card, or accept in
   the card that it cannot.

---

## 3. `plan-page` — FAIL

The rewrite is exact and every clause of it is true, measured rather than accepted: the source
is on disk at 167 lines; `grep 'Status (10 Sep)'` in it returns 1; the private companion tracks
it and the public repository does not, at HEAD or in **any** commit of **any** ref (646 paths
ever added over the whole public history, none matching `plan_page`); the address *and*
`version 13, 14 Sep 2026` are in `PRIVATE.md`; `PRIVATE.md` is private-tracked and clean; and
the Statement is indeed published verbatim on the public site, which is the reason the sentence
gives for itself. The evidence token resolves. Nothing in the Statement is false.

### DEFECT K-1 — BLOCKING. The rewrite deleted the card's referee record, and the site now tells the world this card has never been refereed

To send the card back to the queue the author overwrote the `review:` key. It previously read

> passed 2026-09-14 by phase referees (rigor/referee_*.tex, findings ledger)

— I read it out of the pre-repair blob of the claim map — and it now reads bare `pending`. The
card's History records only `- 2026-09-14 created`, and the knowledge base's event log records
the `statement=` and `verify=` change and nothing about `review`. So the record of that pass is
gone from the card, gone from History and gone from the event log. Thirty-four other cards still
carry that identical review line; the four siblings in this very packet all kept theirs, in the
form `pending (was FAILED 2026-09-23 by REF-LIVE)`.

It is not a bookkeeping matter, because the two generators define "refereed" differently and
both publish. `build_site_data_extra.py` needs an actual verdict, in `review` or in History, so
it emits `"refereed": false` for `plan-page`, `count.never_refereed` **1**, and
`explore/claim-map.html` paints the card with the chip `never refereed`.
`build_docs.py` counts any non-empty `review` as reviewed, so `docs/status.md` line 23 says, on
the same site, **"Of the cards listed here, 0 have never been refereed"**, and line 179 marks
this very card `review pending`. The site publishes both numbers. Before this edit the claim map
listed **no** never-refereed card; this pass created the contradiction, and the half of it that
is false is the half that says a refereed card was never refereed.

**Repair R-1(a), verbatim.** In the frontmatter replace

> review: pending

with

> review: pending (was passed 2026-09-14 by phase referees)

**Repair R-1(b), verbatim.** In `## History`, immediately after `- 2026-09-14 created`, insert

> - 2026-09-14 review passed (phase referees): the phase-referee sweep of 2026-09-14, recorded in rigor/referee_*.tex and the findings ledger; this line restores the verdict that was overwritten when the card was rewritten for E-1 on 2026-09-23.

then `make docs data`. I applied both to a scratch copy of the knowledge base and rebuilt: the
card comes back as `refereed: true`, `awaiting_review: true`, `verdicts: 1`,
`review_failed: false`, and `count.never_refereed` returns to **0**, agreeing with `status.md`.
`R-1(a)` alone does not do it — the `review` key is matched with `^(passed|FAILED)`, so the
parenthesis is read and published but does not count; the History line is what carries it.

**Recording this FAIL has masked the symptom and not the defect, and the note must say so.**
`kb verdict` writes `FAILED 2026-09-23 by REF-LEAK` into `review` and a matching
`- 2026-09-23 review FAILED (REF-LEAK): …` into History, and both satisfy the claim map's test.
I rebuilt after recording: `refereed: true`, `verdicts: 1`, `count.never_refereed` **0**. So the
`never refereed` chip will come off this card the moment the author runs `make docs data`, and
the contradiction with `status.md` will disappear with it — for the wrong reason. The record of
the 2026-09-14 pass is still deleted, and the card now reads as though it had been refereed
once, on 2026-09-23, and never before, which is false about its history and is what the site
will then publish. **R-1(b) is still required**; R-1(a) can no longer be applied as written,
because `review` no longer says `pending`, so when the repairs are absorbed and the card returns
to the queue the key should read `pending (was FAILED 2026-09-23 by REF-LEAK; passed 2026-09-14
by phase referees)`. An addendum saying this is on the card.

### DEFECT K-2 — BLOCKING, and it is §0. The withdrawal is incomplete

The Statement's closing sentence tells a reader that the address is kept out of this card
*because the card is published*. The inference a reader draws — that the address is therefore
not published — is false: this card put it on a public branch for two days and it is served
there today, on four anonymous routes, discoverable in two requests (§0). The card is both the
cause of the exposure and the document a reader is sent to for the plan page's privacy status,
and it is silent, while `PRIVATE.md` — which the card points at — already says "treat it as
compromised". **Repair E-2 in §0**, which is an action first and one sentence afterwards.

**Verdict: FAIL** on K-1 and K-2.

---

## 4. `public-site-plan` — FAIL

X-1 is applied, verbatim and in both fields: the How-to-verify's `P5 is partly done …` is gone
and the replacement sentence is there word for word; `next` begins with the replacement clause
and the rest of the field is unchanged; `review:` is `pending` and the card is in the queue and
in the packet. Both are live on the site. Every other figure I could reach re-measures: README
**428** lines, **89** claim cards (and `docs/status.md` line 5 does carry the current figure:
"90 cards: 89 claim cards … plus 1 finding"), **33** refereed-or-proved (`make check`: 3
refereed + 30 proved) and 33 + 12 = **45**, **ten** modules under `docs/explore/`, **four** PNGs
and **five** generated SVGs, the measured zeta range `0.0083`–`17.067`, the 3 MB asset budget
holding at 1.31 MB against a dated 1.30, six phases P0–P5. Its two published line references
into the plan both still resolve (§7).

### DEFECT K-3 — BLOCKING. X-2 falsified this card's count of the document it cites, and the false count ships

The Statement opens

> Plan of 2026-09-21 for the public surface of cft-cmi, in rigor/public_site_plan.md (**237
> lines**, repaired after REF-SITE-1 and extended with phase P0)

X-2 told the author to append three lines to that file, and the author did. `wc -l` on
`rigor/public_site_plan.md` is **240**; at the commit before the leak commit it was **237**; the
diffstat of the leak commit on that path is `4 insertions(+), 1 deletion(-)`. So the single
commit that applied X-2 falsified a sibling card's Statement by exactly the amount X-2 asked
for, and `237 lines` is served on the public site in `data/extra-claim-map.json` today. This is
the failure this chain has hit at every pass, and it is the only unhedged count in a Statement
that hedges every other one it carries ("it came out at 428 lines on 2026-09-22 and moves with
every edit"; "both grow with every generated page, so these are dated measurements").

**Repair R-2, verbatim.** Replace

> in rigor/public_site_plan.md (237 lines, repaired after REF-SITE-1 and extended with phase P0)

with

> in rigor/public_site_plan.md (240 lines on 2026-09-23, repaired after REF-SITE-1, extended with phase P0 and amended under D1 and D2 on 2026-09-23; the count moves with every amendment, so read what wc -l prints rather than this figure)

### DEFECT K-4 — the evidence document's second line still says the repository is private

`rigor/public_site_plan.md` is this card's only evidence token and is world-readable at
`github.com`. X-2 repaired D1 and D2, which is what X-2 asked for, and left **line 2** standing:

> Written 2026-09-21. Target: the public-ready repository `cft-cmi` (currently private).

`currently` is present tense and it is now false, on the second line of the document, above
everything a reader meets. It is not a referee note, so it may be amended.

**Repair R-2b, verbatim.** Replace line 2 with

> Written 2026-09-21. Target: the public-ready repository `cft-cmi` (private when this was written; public since 2026-09-22).

One line for one line: nothing below it moves, so `ci-green`'s reference to line 226 and this
card's own reference to line 224 both survive the edit (§7).

**Verdict: FAIL** on K-3, with K-4.

---

## 5. `repo-split-public-private` — FAIL

R-5(a) and R-5(b) are applied verbatim, both are true, and both are live on the site: `until
2026-09-22 the repository was private, and throughout the exposure it was unforked and the owner
was its only collaborator` has replaced the self-contradicting clause, and the new sentence
about the flip, forking and the second collaborator is there word for word. `has never been
public` survives only in the Notes and History, which module 10 does not ship.

**The clearance holds, re-run and not carried over.** From a fresh anonymous clone: 81 commits,
refs `main` and `v0.1.0-draft` only, **646** paths ever added over all refs and **0** of them
matching `plan_page`, `rigor/shots`, `*.pdf`, `cited_R[1-4].tex` or `cited_results_all`; the
tag's tree clean. `./pgit check`, before this note was moved into the private companion: public
627, private **235**, overlap **0**, uncommitted 0 and 0, shots on disk **178** tracked **178**,
private set **48,393,896 B = 48.39 MB**; after the move, private **236** and **48,439,401 B =
48.44 MB**, overlap still 0 and shots still 178/178 (see K-8). `.out` files
**97 = 83 + 14**. Compendium **299,915 B**. Fifteen 40-character tokens in **four** tracked
notes; **ten** of them do not resolve against the public clone; **seven** public-tracked files
carry a discarded-object prefix, so "Seven … gave the route in words" reproduces to the file.
`make check` prints the same **nine** private pointers the card counts. Collaborators **2**,
forks **0**, `allow_forking` true — R-5(b) exact. `623 paths on 2026-09-22` is 646 ever-added /
627 tracked today, which is the hedge in the same parenthesis working as designed.

### DEFECT K-5 — BLOCKING. This card is the register of what survives in the public history, and it says one item survives when two do

`next` reads

> **One item survives elsewhere:** the knowledge-base repository carries discarded cft-cmi
> hashes in five of its own files …

A second item survives, and it is not elsewhere — it is in this repository's own public history,
it is a **live** capability rather than a discarded object, and every route against it succeeds
where all forty probes against the nine discarded objects fail (§0). The card's whole thesis is
"what ends it is that the objects no longer exist"; this object does exist, is reachable from
`main`, and was put there by a sibling card. `next` is also the field module 10 renders, so
"No item gates publication any more" and "One item survives elsewhere" are both on the public
site.

The register entry must not go into `next`, because `next` is published and naming the thing
would republish it. It goes where `CHECKLIST.md` items 3–3f already live.

**Repair R-3(a), verbatim,** in `CHECKLIST.md` (private-tracked), as a new item after 3f:

> 3g. **The plan-page address is in the public history, and it is NOT cleared.** The card
> `plan-page` published the Claude artifact address of `plan_page/petz_program_plan.html` in its
> Statement from 2026-09-21 until 2026-09-23. The generator wrote it into
> `docs/data/extra-claim-map.json`, so it is in 41 blobs of that file, in 50 of the 81 commits
> reachable from `main`, and it is served today with no credentials by
> `raw.githubusercontent.com`, by the blob view on `github.com`, by
> `api.github.com/…/git/blobs/` and inside a `codeload` tarball; no hash has to be guessed,
> because the commits are reachable from `main` and the ordinary public listing of that path's
> history hands over every one. The artifact's content is not anonymously readable — the wrapper page carries
> none of the plan and the public-artifact route returns the same application shell for a UUID
> that cannot exist — so what is out is the capability, not the document. Two routes close it:
> republish the artifact at a new address and delete the old one, which makes every copy inert
> at no cost in git; or clear the blobs from the public history by the route item 3 records. The
> first is recommended. Until one of them is done, do not name the address, the file that
> carries it or the route to it in any Statement, How-to-verify or `next` field: those three are
> what module 10 ships, and a published field is where this leaked in the first place.

**Repair R-3(b), verbatim,** in `next`, replace

> One item survives elsewhere: the knowledge-base repository carries

with

> Two items survive. One is in this repository and is recorded in CHECKLIST.md item 3g rather than here, because a published field is where it was leaked in the first place. The other: the knowledge-base repository carries

### DEFECT K-6 — the card's first evidence document contradicts the card, in the paragraph next to the one this pass edited

`PRIVATE.md` is this card's first evidence token. Line 59 reads

> Remotes (**both private**): `cft-cmi`, recreated 2026-09-21 and pushed from a rewritten local
> history, and `cft-cmi-private`, untouched since 2026-09-20 and never force-pushed.

`cft-cmi` has been public since 2026-09-22 — which is what the card's own repaired Statement now
says. `PRIVATE.md` was edited in this very commit, to receive the address, and the false clause
eleven lines above the new heading was left standing. `PRIVATE.md` is private-tracked, so this is
a consistency defect and not an exposure.

**Repair R-3(c), verbatim.** Replace `Remotes (both private):` with

> Remotes: `cft-cmi`, public since 2026-09-22, recreated 2026-09-21 and pushed from a rewritten local

### DEFECT K-8 — the private set's two figures have moved, and this report is what moved them

REF-COUNTS-B and REF-PASS-G both noticed that the Statement's hedge, "`./pgit check` prints the
file count of each repository, and both move with every commit, so neither of those two counts
is fixed here", is followed twelve words later by the fixed `(235 files, 48.39 MB)`. Neither
failed the card for it, and the reason given was empirical: the private count "does not move
with every commit — it has been 235 at six consecutive passes and 48,392,507 B is still 48.39
MB". That reason has lapsed. Holding this note privately made the private set **236 files and
48,439,401 B = 48.44 MB**, so both figures are now simply wrong, and the referee's own artefact
is what broke them. It would have broken the other way too: left public, the note would have
moved the public count instead. A figure that a referee note changes by existing should not be
fixed in a Statement at all.

**Repair R-3(d), verbatim.** Replace

> .git-private holds what must not be published (235 files, 48.39 MB:

with

> .git-private holds what must not be published (236 files and 48.44 MB on 2026-09-23, both of which move with every private commit, exactly as the parenthesis above says of the public side:

**Verdict: FAIL** on K-5, with K-6 and K-8.

---

## 6. `docs-pages-rendering` — FAIL

R-3 and R-4 are both applied verbatim, and R-3 is right on every clause: I ran it against the
live site and `read/status.html` is served `text/html; charset=utf-8` and `status.md`
`text/markdown; charset=utf-8`, so the card's founding claim is now a measurement of GitHub
Pages itself. `Pages has never been enabled` survives only in Notes and History. Everything
structural re-measures: **65** Markdown and **66** HTML mirror pages = the **131** that
`build_docs --check` reports; **58** result pages and **59** mirrored; **8** anchor ids in
`status.md`; README lines 29, 35, 36, 337, 338, 339 each carry the address; section 1 at line 40
and section 9 running 307–349 (section 10 opens at 350); `build_type: workflow`.

### DEFECT K-7 — BLOCKING. R-4 replaced one false visibility claim with another, and this one is refuted by the card's own next sentence

The applied sentence is

> … the repository was **private throughout**, so the only readers were its owner and, from
> 14:35 UTC on 2026-09-22, the one collaborator added that afternoon. All three publication
> steps landed on 2026-09-22 and the address serves.

The window it describes runs from 2026-09-21, when the README first pointed at an address that
did not serve, to the moment the address served — the first Pages deployment, 2026-09-22T21:28:35Z.
The first of the three publication steps *is* the flip, and it necessarily precedes the other
two: `ci-green`'s Statement, the workflow comment and CHECKLIST item 3f all give the order as
public → Pages enabled → `if: false` removed, and the `if: false` came off in the push at
21:28:32Z. So the repository was public for the last stretch of the very window the sentence
says it was private for, and during that stretch the non-serving address sat in a
world-readable README. The two sentences refute each other, and no dating is needed to see it.

Dating it only sharpens it. The `MemberEvent` is 2026-09-22T14:35:52Z and the `PublicEvent`
carries a higher id in the same sequence, so the flip is after 14:35:52Z; the deploy is at
21:28:35Z. The feeds do not fix it more closely than that, which is itself worth saying in the
card rather than papering over. `for one day` REF-LIVE was willing to round; `private
throughout` is a factual claim of the same kind as the `visible to nobody but the repository's
owner` that L-4 failed, and it is false the same way.

**Repair R-4, verbatim.** Replace

> the repository was private throughout, so the only readers were its owner and, from 14:35 UTC on 2026-09-22, the one collaborator added that afternoon.

with

> the repository was private until the flip on 2026-09-22, so until then the only readers were its owner and, from 14:35 UTC that day, the one collaborator added that afternoon; the flip was the first of the three steps and so came before the address served, and for that last stretch -- somewhere between 14:35 and 21:28 UTC, which is as closely as the feeds date the flip -- the non-serving address was in a world-readable README.

**Verdict: FAIL** on K-7.

---

## 7. `ci-green` — PASS

R-1 and R-2 are applied verbatim, both are true, and both are live on the site; the negated
clause survives only in Notes and History. I executed the whole of the repaired How-to-verify
rather than reading it:

- `gh run list` prints the current runs, all successes, which is what the field now predicts.
- `gh run view <latest> --log`: the `NOT CHECKED, no knowledge base at
  /home/runner/work/cft-cmi/kb/projects/cft_cmi: docs/data/extra-claim-map.json` line, **exactly
  once**, and `41 document(s), 0 failing, 0 known`, which is README line 417 inside section 13
  (which opens at 415).
- `make rigor` dispatches to the checker; `rigor` is in `.PHONY` at `Makefile:8`.
- `grep -c allow-missing-kb tools/build_site_data_extra.py` is **1**.
- The `pages` job is `.github/workflows/check.yml:68-78` and **no job in the file carries an
  `if:` key**; it is `skipped` in every earlier run and `success` from 2026-09-22 onward, across
  the six runs I checked job by job.
- `gh api repos/alexander-stottmeister/cft-cmi/pages` reports `build_type: workflow`, `public:
  true`, `https_enforced: true`.

R-2's five actions are the five the runner names: the latest log carries
`actions/checkout@v4, actions/configure-pages@v5, actions/deploy-pages@v4,
actions/upload-artifact@v4` in the pages job and `actions/checkout@v4, actions/setup-python@v5`
in the other two, and the card's attribution of `upload-artifact@v4` to
`upload-pages-artifact@v3` matches `check.yml:75`. The Statement's reference to
`public_site_plan.md:226` survived X-2 (§8). Nothing this pass changed falsified anything in it.

**Not a defect, for the record.** The card's `WHAT THE FLAG DOES NOT DO` paragraph is now true of
one more thing than it says: the new `_no_foreign_url` guard is inside the payload
`--allow-missing-kb` drops, so it too runs only in a clone that has the knowledge base beside it
(§2). The card does not claim otherwise, so I do not fail it; if the paragraph is ever touched,
"a drifted claim map" could become "a drifted claim map, or one that leaks".

**Verdict: PASS.**

---

## 8. X-2 and X-3, and the line reference `ci-green` makes into the plan

**X-2 landed, exactly.** The three-line `Done 2026-09-22:` block is at `public_site_plan.md:229-231`,
word for word as REF-LIVE wrote it, and D2 now reads `and the repository was private when the
tag was cut`. It was **appended**, as X-2 required, not inserted: lines 1–228 are untouched.

**The line reference survived.** `ci-green` cites `rigor/public_site_plan.md:226` for `one line
plus one click`. Line 226 is still D1's first line and the phrase still spans 227–228 — the same
arrangement REF-PASS-C and REF-LIVE both read as pointing at the decision. The insertion begins
at 229, so nothing the reference depends on moved. `public-site-plan`'s `:224` still lands on
`## 6. Decisions — taken 2026-09-21 by the user`. Those are the only two line references into
the plan in any published field; the others are in Notes, History and CHANGELOG. **What X-2 did
break is not a line number but a line count** — see K-3 — and it left line 2 saying the
repository is private — see K-4.

**X-3 landed on the heading and not on the sentence it also named.** Item 6 now reads

> 6. ~~**Private first.**~~ SUPERSEDED 2026-09-22 by item 3f: the repository is public. Nothing
> forces an immediate public repository. Pushing privately now with these exclusions in place …

X-3 asked for "item 6's heading **and first sentence**" to be replaced. The heading was; the
first sentence, `Nothing forces an immediate public repository.`, was kept, so the item now says
the repository is public and then that nothing forces an immediate public repository, in
consecutive sentences. Under the strike-through and the SUPERSEDED marker the item no longer
misdescribes the state, `CHECKLIST.md` is private-tracked, and nothing depends on it, so this is
**non-blocking**. If it is touched, delete that one sentence and keep the rest, which is what
X-3 asked for.

---

## 9. The repository description and the homepage

Both are set and both were checked anonymously against the live repository.

**Homepage** `https://alexander-stottmeister.github.io/cft-cmi/` — **correct**: it is the address
Pages serves, it returns 200, and it is the address the README carries six times.

**Description** — accurate, and one of its four items is flattered by omission. "an exact
quadratic law" is `thm-a-quadratic-law`, `refereed`; "a universality theorem" is
`thm-b-universality`, `refereed`; "a Schwarzian corner calculus for recovery networks" is
`corner-calculus`, `proved`, and the phrase matches the card's own title. "a **conditional**
optimality value" is `all-channel-optimum-value`, which is `numerical` — `kappa_opt = 1 - theta
= 0.616 ± 0.003`, conditional on H1–H3. The description says *conditional* but not *numerical*,
and it is the one of the four that is not proved or refereed; a reader of the GitHub sidebar
would take it for an established conditional theorem. The closing clause, "AI-assisted and
ongoing; human verification is not finished", is the same framing as the README's first block
and is the strongest caveat the field has room for, so I do not call the description a
misdescription. **Suggested, non-blocking:** "a numerical, conditional optimality value".

Nothing else about the two fields is stale: neither says the repository is private, neither
promises a page that does not serve. `secret_scanning` and push protection remain `disabled`,
which is REF-LIVE's one untaken recommendation; neither would have caught this leak, and both
are free on a public repository.

---

## 10. Figures REF-LIVE did not certify, re-measured

| figure, and the card it is in | measured today |
|---|---|
| `public-site-plan`: plan **237 lines** | **240** — see K-3 |
| `public-site-plan`: README **428 lines** on 2026-09-22 | 428 |
| `public-site-plan`: **89** claim cards; `status.md` carries the current figure | 89; `status.md:5` "90 cards: 89 claim cards … plus 1 finding" |
| `public-site-plan`: **33** refereed-or-proved (30 proved, 3 refereed), plus 12 = **45** | 3 + 30 = 33; 33 + 12 = 45 |
| `public-site-plan`: **ten** modules; four PNGs; five generated SVGs | 10 `docs/explore/*.html`; 4; 5 |
| `public-site-plan`: zeta range **0.0083–17.07** | `quadratic-law.json` x ∈ [0.0083, 17.067] |
| `public-site-plan`: 3 MB budget, 1.30 MB and 8.21 MB dated 2026-09-21 | 1.31 MB and 8.41 MB; both dated and hedged in the card, budget holds |
| `plan-page`: source, its marker, its two tracking states | 167 lines; `Status (10 Sep)` 1 hit; private-tracked; 0 occurrences in any commit of any public ref |
| `plan-page`: address and version in `PRIVATE.md` | both present |
| `docs-pages-rendering`: **131** = 65 + 66; **58** result pages; **8** anchors | 65, 66, 58 (+59 mirrored), 8 |
| `docs-pages-rendering`: README lines 29/35/36/337/338/339, §1 at 40, §9 at 307–349 | all exact |
| `repo-split`: 235 / 48.39 MB / overlap 0 / 178 shots / 97 = 83 + 14 / 299,915 B | all exact |
| `repo-split`: 15 tokens in 4 notes, 10 unresolved, 7 files with a discarded prefix, 9 private pointers | 15, 4, 10, 7, 9 |
| `ci-green`: 41 documents, the NOT CHECKED line, README §13's number, five deprecated actions | all exact |

---

## 11. Gates, printed exactly

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
      cards awaiting a referee pass: 5 (ci-green, docs-pages-rendering, plan-page, public-site-plan, repo-split-public-private)
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

`make rigor` — **exit 0**: `python3 tools/check_rigor_builds.py`, 46 `ok` lines and
`46 document(s), 0 failing, 0 known`.

`../kb/bin/kb -p cft_cmi lint` — `[cft_cmi] 0 issue(s), 5 awaiting review`, the five being this
packet.

All three were run **before** the five verdicts were recorded, which is the state in which I
found the project.

Two of these numbers are worth reading against §3. `make check` says **0** cards have never been
refereed, from `build_docs.py`'s definition; the claim map it validates in the same run says
**1**, from `build_site_data_extra.py`'s. Both ship. The gate is green over a contradiction it
cannot see, because no check compares the two generators' counts.

**After the verdicts**, `make check` is **exit 2**, as the Makefile's own header predicts ("a
referee verdict makes `make check` fail until both are rebuilt"): `build_docs --check: the
committed documentation has drifted from the knowledge base`, the diff being
`0 carry a failed referee pass` → `4 carry a failed referee pass` and four rows gaining
`referee pass failed`; `cards awaiting a referee pass: 0`; `cards whose last referee pass
failed: 4 (docs-pages-rendering, plan-page, public-site-plan, repo-split-public-private)`.
`make rigor` is unaffected and stays exit 0. `kb lint` is `0 issue(s), 4 awaiting review`, all
four being the failed cards. Rebuilding and committing is the author's step, not mine.

---

## 12. Verdicts

- **`plan-page`: FAIL.** K-1, blocking: the rewrite overwrote the `review:` key that recorded
  the 2026-09-14 pass and put nothing in History, so module 10 now paints the card
  `never refereed` and publishes `count.never_refereed = 1` while `status.md`, on the same site,
  says 0 have never been refereed; the card was refereed and passed. Recording this FAIL masks
  the symptom and not the defect — see the end of §3 and the addendum on the card. K-2, blocking and the
  subject of §0: E-1's withdrawal moved the address off the tip and not out of the public
  record, where 41 blobs reachable from `main` still serve it to an anonymous client on four
  routes, with no hash to guess. Everything the Statement actually asserts is true and
  re-measured. Repairs R-1(a), R-1(b) and E-2.
- **`public-site-plan`: FAIL.** K-3, blocking: X-2 appended three lines to the document this
  card measures, and the Statement still says 237 lines where `wc -l` says 240 — the count was
  237 at the previous commit and the same commit that applied X-2 falsified it; it ships. K-4:
  the cited document's second line still says the repository is `(currently private)`. X-1 is
  applied verbatim in both fields and every other figure re-measures. Repairs R-2 and R-2b.
- **`repo-split-public-private`: FAIL.** K-5, blocking: the card is the register of what
  survives in the public history and its `next` says one item survives, elsewhere; a second
  survives here, it is a live capability rather than a discarded object, and every route against
  it succeeds. K-6: `PRIVATE.md`, this card's first evidence token, still says both remotes are
  private, in the file this pass edited. K-8: `235 files, 48.39 MB` is now 236 and 48.44 MB, and
  this report, held privately, is what moved it — the empirical reason two earlier passes gave
  for tolerating the fixed figure has lapsed. R-5(a) and R-5(b) are applied verbatim and true,
  and I re-ran the whole clearance from a fresh anonymous clone: everything discarded is still
  gone. Repairs R-3(a), R-3(b), R-3(c) and R-3(d).
- **`docs-pages-rendering`: FAIL.** K-7, blocking: R-4's replacement says the repository was
  private throughout a window whose last stretch it was public for, which the card's own next
  sentence refutes — the flip was the first of the three steps and so preceded the address
  serving. R-3 is applied verbatim and I confirmed both content types against the live site.
  Repair R-4.
- **`ci-green`: PASS.** R-1 and R-2 applied verbatim; I executed every clause of the repaired
  How-to-verify against the live repository and the live run log, and every one returns what the
  card predicts. Nothing this pass changed falsified anything in it.
- **Outside the cards: the leak is not closed** (§0), and **the guard closes the instance and
  most of the class but not the class** (§2) — an uppercase scheme, a scheme-relative URL and a
  bare host all ship end to end; `title` and `review` are published and unguarded; a second
  generator publishes card prose with no guard at all; and the guard never runs in continuous
  integration, because the payload it lives in is the one `--allow-missing-kb` drops.
