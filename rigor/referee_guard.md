# REF-GUARD: the hardened payload guard and four cards (2026-09-23)

Sixteenth pass, and the second on the leak class. The order of work is the brief's: break the
rebuilt guard, then the four cards and whether any applied repair falsified a neighbour, then
the deployed tree, then the figures the last two passes did not certify, then the gates.

**A note on this file, and on why it is public-tracked where its predecessor is not.** It
carries no address, no UUID, no object or commit hash, and it does not name the host, the file
or the route of the exposure that `CHECKLIST.md` item 3g registers. Every demonstration below
uses reserved placeholder hostnames, never the real one. Its predecessor had to be held
privately because its section 0 told a reader that the address was still recoverable and from
which file; nothing here does that, and item 3g is already named in a published `next` field and
in the public `.gitignore`, so this file adds no signpost that is not already public.

There is a second reason, and it is a measurement. `repo-split-public-private` now fixes the
private set at **236 files and 48.44 MB, dated 2026-09-23**, which is exactly the figure K-8
moved by holding the previous note privately. Holding *this* note privately would make it 237
and falsify that figure on the same day it was dated -- the same trap, sprung twice by the same
instrument. Published, it moves only the public file count, which the sentence immediately
before it hedges by name. So the safe place for this note is also the place that leaves the card
true.

**Verdicts: two PASS and two FAIL.** E-2 is excluded from the card findings on the brief's
instruction; it is not closed, and nothing below should be read as saying it is.

---

## 1. The rebuilt guard, and REF-LEAK's six

`ALLOWED_PROSE_HOSTS` is now eight hosts; `_URLISH` is case-insensitive and has two branches, a
scheme or scheme-relative `//host` and a bare host whose last label is one of nine suffixes;
`_host_of` takes the text after the last `@`, strips a port, lower-cases and strips a trailing
dot; and `check_payload()` sweeps `json.dumps(payload)` for every payload `dump()` writes, so it
is no longer a field list. `_no_foreign_url` survives as the per-field diagnosis and runs first.

I called the real functions on every form, and drove the real `build_claim_map()` against a
scratch copy of the knowledge base for the ones that survived, reading the result back out of
the emitted JSON. The scratch copy is a copy; the knowledge base was not edited.

**REF-LEAK's six, one at a time.**

| form it broke | today |
|---|---|
| 1. uppercase or mixed-case scheme, `HTTPS://`, `Https://` | **caught** (`re.I`) |
| 2. scheme-relative `//host/` | **caught** |
| 3. bare host `host/path` | **caught**, if the last label is one of nine suffixes -- see 2.4 |
| 4. another scheme: `ftp:`, `mailto:` | **caught**, but incidentally, not by design |
| 4. another scheme: `file:///Users/...`, `data:...` | **NOT caught**, see 2.6 |
| 5. `https://allowed.example:1234@notallowed.example/` | **caught** (`_host_of` after the last `@`) |
| 6. the field list: `title`, `review`, `area`, `status`, `page`, a dict **key**, a nested list | **caught**; the serialised sweep is the real repair and it is sound |

The false positive REF-LEAK named is also gone: `see https://github.com.` no longer raises,
because `_host_of` strips the trailing dot.

So five and a half of six. Item 4 is the half: `ftp://` is caught only because it happens to
carry `//`, and `mailto:a@host` only because the bare-host branch happens to see `host`.
`file:` and `data:` carry neither and pass. Nothing in the guard knows about schemes it has not
been shown.

---

## 2. Nine ways past it, six of them confirmed end to end

For each of the six marked **shipped** I put the form into `plan-page`'s Statement in the
scratch knowledge base, ran the real `build_claim_map()`, ran `check_payload` on the result, and
confirmed the string appears verbatim in the JSON that would be written to
`docs/data/extra-claim-map.json` and rendered by module 10. The plain form of the same address
raises, as it should, which is the control.

### 2.1 The seventh, and the sharpest: an invisible or lookalike label separator -- SHIPPED

The bare-host branch is `(?:[a-z0-9-]+\.)+(?:com|org|net|io|ai|dev|app|edu|de)`. It needs an
ASCII full stop between the labels. A browser does not. UTS #46 *ignores* U+00AD SOFT HYPHEN and
U+200B/U+200C/U+2060, and *maps* U+FF0E FULLWIDTH FULL STOP, U+3002 IDEOGRAPHIC FULL STOP and
U+FF61 to `.`, before it ever looks up the name. I confirmed all six with Python's own IDNA
encoder: each of

    notallowed{U+00AD}.com/path      notallowed{U+200B}.com/path
    notallowed{U+FF0E}com/path       notallowed{U+3002}com/path

normalises to `notallowed.com`, and every one of them passes both `_no_foreign_url` and
`check_payload`. The soft-hyphen form is the worst of them: it is **invisible** in the rendered
page, so a reader sees the address exactly as written, and it **resolves** in any browser. A
full path rides along, because the guard never matched anything to stop at.

This is not an exotic attack. A soft hyphen is what a word processor, a PDF copy-paste or a
line-wrapping editor inserts on its own.

### 2.2 The eighth: the userinfo repair overshot, and now reads an allowed host out of a disallowed URL -- SHIPPED

`_host_of` was rewritten to take the text after the last `@`, which is right for userinfo. But
the character class the host is captured with, `[^/\s)>\]"'\\]+`, does not stop at `?` or `#`,
and both of those end the authority in RFC 3986 and in WHATWG. So

    https://notallowed.example?@github.com
    https://notallowed.example#@github.com

are captured whole, `_host_of` returns `github.com`, and the guard allows them. Python's own
`urlsplit` returns `notallowed.example` for both, and so does every browser. The first branch
also *consumes* the text, so the bare-host branch never gets a second look at the real host.

This is a regression introduced by the repair for form 5: before it, `split(":")[0]` got the
host wrong in the defender's favour; now `rsplit("@")[-1]` gets it wrong in the leaker's.
Contrived as an attack, but it is the one case where the guard and the browser disagree about
what the host *is*, and that is the class the rebuild was for. Add `?` and `#` to the
terminator class and it is closed; `;` needs no change, because `;` does not end an authority
and the guard is right about it.

### 2.3 The ninth: percent-encoding the separator, in the bare form -- SHIPPED

`notallowed%2Ecom/path` has no full stop, so the bare-host branch cannot see it; there is no
`//`, so the other branch cannot either. Host parsing percent-decodes before IDNA, so a browser
resolves it. With a scheme it is caught, on the mangled host -- so this is specifically a hole
in the branch that was added to catch the scheme-less form.

### 2.4 The bare-host branch covers nine suffixes, not "a public suffix" -- SHIPPED

`com|org|net|io|ai|dev|app|edu|de`. Bare hosts on `co.uk`, `cloud`, `xyz`, `me`, `co`, `gov`,
`info`, `page`, `link`, `site`, `eu`, `fr`, `ch`, `nl`, `tv`, `cc` and the other ~1,500 all pass.
Each is caught if it carries a scheme; none is caught bare. The comment in the source says "a
bare host with a known public suffix", which reads as a policy and is a list of nine.

### 2.5 Bare IP addresses -- SHIPPED

`93.184.216.34/path` passes: the bare-host branch matches `93.184.216.` and then needs a listed
suffix, and `34` is not one. With a scheme it is caught. IPv6 in brackets is caught with a
scheme and passes bare.

### 2.6 `file:` and `data:` -- SHIPPED

`file:///Users/<name>/...` and `data:text/html;base64,...` match neither branch. The first
publishes a local directory layout; `check_links.py` skips `data:` and `mailto:` hrefs by name
before it ever tests a host, so nothing else looks at them either.

### 2.7 Non-ASCII lookalike labels -- not caught, and not a route here

`{Cyrillic es}laude.example` passes, because `[a-z0-9-]` is ASCII. It resolves to a *different*
name, so it is a class gap rather than a way to publish an address we hold. Punycode (`xn--...`)
is caught, because it is ASCII.

### 2.8 What I could NOT get past it

- **Concatenation across JSON boundaries.** Two adjacent fields whose ends would join into a
  host do not: `json.dumps` puts `", "` between them, and neither branch can span it. I tried
  the value/value, key/value and list-item/list-item forms. One caveat for the record: the sweep
  serialises with the default separators and `dump()` writes with `indent=1`, so the text swept
  is not byte-identical to the text written -- but indentation only inserts whitespace, and
  whitespace cannot create a host, so the file can carry no host the sweep did not see.
- **A URL in a key**, in a nested list, in `title`, in `review`, in `area`, in `status`, in
  `page`. All caught. This half of the rebuild is genuinely sound and is the part worth keeping.
- **Hiding a host behind `_mark_private`**, or behind a backslash, a newline, a tab or a quote:
  all of those terminate the capture and the truncated host is still not on the allow-list, so
  the guard raises -- with a wrong diagnosis but the right answer.
- **A subdomain or lookalike of an allowed host.** The allow-list is exact-match, so
  `gist.github.com`, `www.github.com`, `sub.github.com` and
  `github.com.notallowed.example` all raise. That is the correct direction, and it is also a
  false-positive source: a legitimate `gist.github.com` link in a Statement will stop a build.

### 2.9 A very long payload: the sweep is quadratic and can be made to hang

`(?:[a-z0-9-]+\.)+` restarts at every offset, so a long dotted run costs O(n^2):

| a dotted run of | sweep takes |
|---|---|
| 1,000 labels (2 kB) | 0.15 s |
| 2,000 labels (4 kB) | 0.59 s |
| 4,000 labels (8 kB) | 2.4 s |

40 kB of it is about a minute, 100 kB about six. Not a bypass, and the author writes the cards,
so this is a footgun rather than an attack: one Statement with a long dotted expression makes
`make check` look hung. Anchoring the branch or bounding the label count fixes it.

### 2.10 One loosening, for the record

`www.w3.org` was added to `ALLOWED_PROSE_HOSTS` in the rebuild. It occurs **0 times** in all four
payloads this guard sweeps: the 13 occurrences in the deployed tree are `xmlns` declarations in
SVG and MathML, in files this guard never sees. It is the only direction in which the guard was
widened, and it buys nothing.

---

## 3. Where the guard still does not run, re-verified

1. **Continuous integration.** `.github/workflows/check.yml` runs
   `build_site_data_extra.py --check --allow-missing-kb`, and with the knowledge base absent
   `main()` pops the claim-map builder off the list. I ran it with `KB` pointed at a
   non-existent path and traced `check_payload`: it is called for
   `extra-separation.json`, `extra-off-criticality.json` and `extra-relative-entropy.json`, and
   **never for the claim map**, exit 0. Card prose is the only thing the guard is for, and card
   prose is the one payload CI drops. The guard is still a local pre-commit gate only; the
   rebuild did not change this, and REF-LEAK's recommendation 4 is unapplied.

2. **`tools/build_docs.py`, still unguarded.** `grep -c 'ALLOWED\|foreign\|check_payload'` is
   **0**. It publishes Statement, How-to-verify, Evidence and Review into `docs/results/<id>.md`,
   Statements into `docs/open.md`, and titles into `docs/status.md` and `docs/index.md`, plus the
   `docs/read/` mirrors of all of them. `check_links.py` covers it only by accident, and less
   than REF-LEAK allowed: `md_to_html.py` autolinks a bare URL **only when it starts with
   lowercase `http://` or `https://`** (`BARE_URL`, and the `startswith` that guards it), so an
   uppercase scheme, a scheme-relative URL and every scheme-less form in section 2 never become
   an `href` and are never host-checked anywhere. None of the four cards in this packet has a
   generated page, so nothing in this packet rides that surface today -- but the next card that
   does will.

3. **The `pages` job carries no `needs:`.** A push deploys `docs/` whether or not the other two
   jobs pass. A guard that fails a build therefore does not stop a deployment.

4. **New: `make data` swallows the guard.** The recipe is
   `test -f tools/build_site_data_extra.py && python3 tools/build_site_data_extra.py || true`.
   A `Drift` exits 2, `|| true` turns the line into exit 0, and `make data` reports success. I
   confirmed the shell semantics. `make docs` has no such `|| true`, so the sequence
   `make docs data` writes the leaked prose into `docs/` through the unguarded generator and
   then reports success from the guarded one. `make check` does catch it -- it runs the same
   script without `|| true` -- so the hole is only for someone who regenerates and commits
   without running the gate, which is also the only person the guard exists for.

**Verdict on the guard.** The serialised-payload sweep is the right instrument and it closes
REF-LEAK's form 6 completely, which was the largest of the six. The *host* determination did not
keep up with it: the extractor still decides what a host is by a character class and a
nine-item suffix list, and a browser decides by IDNA and an authority terminator, and section 2
is the gap between those two answers. In decreasing order of value, none of it blocking a card:

1. Normalise before matching: NFKC the text, drop the characters UTS #46 ignores, map the three
   full-stop lookalikes, percent-decode, and only then extract. Two of the three shipped
   findings in section 2 die at once.
2. Add `?` and `#` to the host-capture terminator class, which closes 2.2.
3. Invert the bare-host rule: match `label.label` for **any** suffix and allow-list the result,
   rather than enumerating nine suffixes. That closes 2.4, 2.5 and 2.6 together, at the cost of
   false positives on filenames, which an extension list handles.
4. Apply the same sweep in `build_docs.py`, which is the other half of the surface and has none.
5. Make CI fail when it cannot check the claim map and the diff touches a card, or say in
   `ci-green` that it cannot.
6. Drop the `|| true` in `make data`, and give the `pages` job a `needs:`.

---

## 4. `plan-page` -- FAIL

Everything the Statement asserts re-measures: the source is 167 lines, `grep 'Status (10 Sep)'`
returns **1**, `git ls-files plan_page` is **0** and the path is in **no commit of any public
ref**, the private companion tracks it, the address and `version 13, 14 Sep 2026` are both in
`PRIVATE.md`, and the Statement is published verbatim in the claim map and nowhere else on the
site. The evidence token resolves. Nothing in the Statement is false.

### DEFECT G-1 -- BLOCKING. R-1(b) was not applied, and a note on the card says it was

`## History` reads, in full:

    - 2026-09-14 created
    - 2026-09-23 review FAILED (REF-LEAK): ...
    - 2026-09-23 note
    - 2026-09-23 note

The line R-1(b) gave verbatim -- `- 2026-09-14 review passed (phase referees): ...` -- is not
there. The `review` key is `pending (was FAILED 2026-09-23 by REF-LEAK)`, not the form REF-LEAK's
addendum specified once the verdict had been recorded. The knowledge base's event log shows
`plan-page` receiving one `set` (the E-1 rewrite, 00:03:52), one `review` (00:57:23) and two
`note`s (00:59:52, 01:02:36) -- no edit that could have inserted the line.

What was added instead is the third note, dated 2026-09-23, which reads in part

> REF-LEAK K-1 repaired: the E-1 rewrite replaced the whole card and dropped the History line
> carrying the 2026-09-14 phase-referee pass ... **The line is restored.**

It is not restored. The card's own record now asserts a repair that was not made, which is worse
than the omission, because the next pass reads the note before it reads the History.

**And the consequence is live.** The claim map served today gives `plan-page`
`verdicts: 1`, `review_failed: true`, against `15`, `26`, `9` and `7` for its four siblings. The
only referee verdict the public site records for this card is the failure of 2026-09-23. The
2026-09-14 pass is in no field, no History line and no event, exactly as REF-LEAK found it, and
`count.never_refereed` is **0** only because a FAILED verdict counts as a verdict -- which is
precisely the masking REF-LEAK's addendum warned the next reader not to mistake for a repair.

**Repair G-1, verbatim.** In `## History`, immediately after `- 2026-09-14 created`, insert

> - 2026-09-14 review passed (phase referees): the phase-referee sweep of 2026-09-14, recorded in rigor/referee_*.tex and the findings ledger; this line restores the verdict that was overwritten when the card was rewritten for E-1 on 2026-09-23.

then `make docs data`. When the card returns to the queue the `review` key should read
`pending (was FAILED 2026-09-23 by REF-LEAK; passed 2026-09-14 by phase referees)`. And because
a note is never rewritten, the false sentence needs a new dated note saying that the line was
not in fact restored until today, and when it was.

**Verdict: FAIL** on G-1.

---

## 5. `public-site-plan` -- PASS

**R-2 is applied, and it is true.** `wc -l rigor/public_site_plan.md` is **240**; the Statement
says "240 lines on 2026-09-23 ... the count moves with every amendment, so read what wc -l prints
rather than this figure", and it is live on the site. The two commits that touched the document
today are +4/-1 (X-2) and +1/-1 (R-2b), so the dating is right as well as the count.

**R-2b is applied verbatim**, at line 2, one line for one line. Every line reference into the
plan still resolves: `:224` is `## 6. Decisions -- taken 2026-09-21 by the user`, `:226` and
`:226-228` are D1's first line and the `one line plus one click` phrase, `:229-231` is X-2's
`Done 2026-09-22:` block, `:208-213` is the phase table.

Everything else re-measures: README **428** lines; **89** claim cards and `status.md:5` carrying
"90 cards: 89 claim cards ... plus 1 finding"; **3** refereed + **30** proved = **33**, and
33 + 12 = **45**; **ten** modules under `docs/explore/`; **four** PNGs and **five** generated
SVGs; zeta in `[0.0083, 17.067]`; `docs/{assets,lib,data}` **1.31 MB** and the public repository
**8.41 MB** against a fixed 3 MB budget, both dated and hedged in the card; **D1 to D4** and no
others in section 6; six phases P0-P5. The claim "no runtime external requests" holds: **0**
`script`, `link`, `img` or `iframe` in the whole deployed tree fetches an absolute URL.

Three carried items, none of them blocking and none of them new today:

- **REF-FINAL F-7 is still unapplied.** `next` says `close D6 (the --line contrast) in the
  shared layer`; `grep 'D5\|D6' rigor/public_site_plan.md` returns nothing, and the Statement of
  the same card says the plan has four decisions. D6 is a REF-SITE-P3 defect id. REF-FINAL gave
  the repair verbatim, REF-COUNTS carried it as open and not owed by this card's text, and the
  gloss in parentheses saves it for a reader. It ships in module 10.
- **X-2's append moved `rigor/public_site_plan.md:235`.** D3 is now at 238. Seven references to
  `:235` exist; all seven are in Notes, History, the CHANGELOG, the event log and two referee
  notes, **none in a published field** and none in a file that may be edited. Recorded so the
  next pass does not read it as fresh drift.
- The Statement lists the plan's amendments as "repaired after REF-SITE-1, extended with phase
  P0 and amended under D1 and D2 on 2026-09-23" and does not mention R-2b's line-2 amendment,
  also of 2026-09-23. The sentence does not claim to be exhaustive and the count it guards is
  hedged, so this is an observation, not a defect -- but it is the same shape as G-2 below, and
  it is the shape this chain keeps producing: the number is updated and the list beside it is not.

**Verdict: PASS.**

---

## 6. `repo-split-public-private` -- FAIL

R-3(a) is applied, verbatim plus one accurate closing sentence; R-3(b) and R-3(c) are applied
verbatim and both are live; R-5(a) and R-5(b) still hold (collaborators **2**, forks **0**,
`allow_forking` true, the repository created 2026-09-21T19:55:13Z). The clearance re-runs:
overlap **0**, public **627**, private **236**, shots **178** on disk and **178** tracked,
`refs/*.pdf` **47**, `.out` **97 = 83 + 14** with **23** named by an evidence token, compendium
**299,915 B**, the tag's tree carrying **0** private paths, **15** forty-character tokens in
**four** tracked notes of which **ten** do not resolve against the public object store and
**seven** public-tracked files carry one of their prefixes, **nine** private evidence targets
cited by **ten** cards, and `make check` printing those same nine. Tracked by neither
repository: **435** files, **201.5 MB** (the card's 423 / 198.6 MB is dated 2026-09-21 and
hedged).

### DEFECT G-2 -- BLOCKING. R-3(d) fixed the count and falsified the list in the same parenthesis

The repaired clause reads

> .git-private holds what must not be published (**236 files, 48.44 MB on 2026-09-23**, and
> rising as referee notes are held here: the 178 page excerpts in rigor/shots, the 47 source
> PDFs in refs, the five cited-result compendia rigor/cited_R1..R4.tex and cited_results_all.tex,
> plan_page/petz_program_plan.html, CHECKLIST.md, PRIVATE.md, pgit and pgit-exclude, **which is
> exactly what git --git-dir=.git-private ls-files lists outside the first two directories**)

The count is right: 236 files, 48,443,214 B = 48.44 MB, measured today. The identity claim at the
end is not. `git --git-dir=.git-private ls-files` lists **eleven** paths outside `rigor/shots/`
and `refs/`, and the enumeration names **ten**. The eleventh is the referee note that the
project moved into the private companion on 2026-09-23 -- the same file, and the only file, that
made the count 236 rather than 235. **The edit that repaired the number is the edit that
falsified the list, in the same parenthesis, in the same commit**, and the clause even has the
hedge "and rising as referee notes are held here" bolted on immediately before it, so the author
knew a note had been added and updated everything except the list that claims to be exact.

This is the failure this chain has hit at every pass, and it is now in its purest form: the
repair for K-8 created G-2 exactly as X-2 created K-3.

It ships. The Statement is rendered verbatim by module 10.

**Repair G-2, verbatim.** Replace

> which is exactly what git --git-dir=.git-private ls-files lists outside the first two directories

with

> plus any referee note held here under CHECKLIST.md item 3g; git --git-dir=.git-private ls-files is the list, and this enumeration is a summary of it that moves whenever a note is added or released, so run the command rather than reading the sentence

That is the form I recommend, because it stops the sentence asserting an identity that a single
private commit can break, and because it does not add a filename to a published field. If the
project would rather keep the identity claim, the alternative is to name the note in the
enumeration -- its path is already world-readable in the public `.gitignore` -- and to accept
that the clause must be re-edited on every private note.

### DEFECT G-3 -- the same omission in the card's own evidence document and in the whitelist

`PRIVATE.md`, this card's first evidence token, lists the private set under "What this is" in
the same order and with the same ten entries, and also omits the note. `pgit-exclude`, the
tracked whitelist, is `/rigor/*` with re-inclusions for `shots/` and the five compendia and no
re-inclusion for the note; only `PRIVATE_PATHS` in `pgit`, which force-adds, was updated. The
file stays tracked because it is already tracked and `./pgit sync` force-adds it, so nothing
breaks today; but the whitelist that a bare clone reinstalls does not describe the set that
repository holds. Both are private-tracked, so this is a consistency defect and not an exposure,
and it is the same shape as K-6.

**Repair G-3.** Add the note to `PRIVATE.md`'s list under "What this is", and a
`!/rigor/referee_leak.md` line to `pgit-exclude` beside the compendia.

### Not a defect, recorded

The public `.gitignore` rule that holds the note says, in its comment, that the address was
*withdrawn* and that a file and a route still carry it. That is a shade more than REF-LEAK
described when it accepted the rule ("says that a withheld note about an unclosed exposure
exists"). It still names neither the file nor the route, and item 3g is named in a published
`next` field in any case, so I record it rather than object to it.

`secret_scanning` and its push protection are still `disabled`, which remains REF-LIVE's one
untaken recommendation.

**Verdict: FAIL** on G-2, with G-3.

---

## 7. `docs-pages-rendering` -- PASS

**R-4 is applied verbatim** and every clause of it is true. The `MemberEvent` is
2026-09-22T14:35:52Z; the `PublicEvent` carries a higher id in the same sequence but a
`created_at` equal to the repository's own creation timestamp, so it dates the creation and not
the flip, and the id ordering is the only thing that places the flip after 14:35:52Z; the first
Pages deployment is 2026-09-22T21:28:35Z. "Somewhere between 14:35 and 21:28 UTC, which is as
closely as the feeds date the flip" is exactly what the feeds support, and the card is the only
document in the chain that says so rather than rounding. The two sentences no longer refute each
other.

R-3 still holds against the live site: `read/status.html` is served
`text/html; charset=utf-8` and `status.md` `text/markdown; charset=utf-8`, and the root,
`read/index.html` and `read/results/index.html` are all 200 and `text/html`.

Everything structural re-measures: **65** Markdown and **66** HTML mirror pages = the **131**
`build_docs --check` reports; **58** result pages and **59** mirrored; **8** `<a id>` anchors in
`status.md` and **8** in `read/status.html`, and no others; README lines 29, 35, 36, 337, 338,
339; section 1 at 40, section 9 running 307-349 with section 10 at 350; `build_type: workflow`;
155 pages and 2210 links from `check_links.py`, which the card hedges. `read/history.html`
carries **no** `<em>` span at all, as the card says. I probed the six constructs the card lists
as "still silently wrong, none of it occurring in what the generator emits today" across all 65
pages and found **none** of them occurring.

**The 14-character divergence, re-measured**, which neither of the last two passes certified. I
rendered all 65 sources through `gh api /markdown --mode gfm` and compared the visible text
against `docs/read/` ignoring whitespace: **62 of 65 pages are character-identical**, and the
three that differ do so by exactly **14 characters** -- two `_` in `definitions.md`, six `*` in
`history.md`, six `_` in `notation.md` -- every one of them an emphasis delimiter GitHub
consumes out of mathematics and the mirror keeps. That is the card's figure, to the character.
(Three further apparent differences in `notation.md` are an artefact of GitHub wrapping `$...$`
in a `math-renderer` element and double-escaping inside it; they are not divergences in what a
reader sees.)

**Verdict: PASS.**

---

## 8. The deployed tree, swept anonymously

Local `HEAD`, `origin/main`, the remote's `main` and the sha of the latest `github-pages`
deployment are one and the same commit, the public working tree is clean, and
`git diff HEAD -- docs` is empty. So `docs/` on disk is `docs/` at `HEAD` is what the world is
served, and I verified it rather than inferring it: I fetched **all 188 files** of the deployed
tree anonymously, one request each, **188 of 188 returned 200**, and **0 of 188** differ from
disk by a byte.

Over those 188 files: **0** occurrences of the withdrawn address, of its UUID, of any fragment of
either, or of the host in any case. **0** GitHub, AWS or Slack tokens, **0** PEM private keys,
**0** e-mail addresses, **0** Windows paths, **0** forty-hex tokens, **0** UUIDs of any kind,
**0** scheme-relative URLs, **0** real `file:`, `ftp:`, `mailto:` or `data:` URLs (the two
regex hits are a JavaScript object key and a comment). `/Users/alex` occurs **once**, in the
`repo-split` Statement, which CHECKLIST item 4 and REF-LIVE both record as a decision. The
withheld referee note is named **0 times**.

Every absolute URL in the tree, by host, enumerated over every byte rather than read off the
claim map:

| host | occurrences |
|---|---|
| `github.com` | 316 (314 on this repository, 1 on the private companion, 1 punctuation split) |
| `www.w3.org` | 13, all `xmlns` |
| `projecteuclid.org` | 3 |
| `alexander-stottmeister.github.io` | 3 |

Four hosts, all in `check_links.py`'s allowed set, unchanged from the last pass. The two private
repositories that are named and not linked both return **404** anonymously. Negative probes, all
**404**: `README.md`, `CHECKLIST.md`, `PRIVATE.md`, `pgit`, `pgit-exclude`, `.gitignore`,
`Makefile`, `plan_page/petz_program_plan.html`, `rigor/public_site_plan.md`, the two referee
notes, `rigor/shots/`, `data/`.

**Nothing false or private reaches the public site.** The one thing the site publishes that this
report would add to is the `review_failed` state of `plan-page`, which is true as the claim map
defines it and incomplete as a record -- see G-1.

**One standing contradiction, unchanged and not newly caused.** `docs/status.md` line 23 says
"**0 have never been refereed** and **0 carry a failed referee pass**", from `build_docs.py`,
which reads the `review` key; the claim map on the same site gives `count.review_failed` **4**
and module 10 paints four cards with the chip `last verdict failed`, from
`build_site_data_extra.py`, which reads History. The two generators are answering different
questions in the same words, both ship, and `make check` is green over it because nothing
compares them. Neither number is false under its own definition, so I record it rather than fail
a card for it; REF-LEAK named the same gap from the other side.

---

## 9. Figures re-measured

| figure, and the card it is in | measured today |
|---|---|
| `repo-split`: private **236 files, 48.44 MB** on 2026-09-23 (K-8's new figure) | 236; 48,443,214 B = **48.44 MB** |
| `repo-split`: the enumeration is "exactly" what `ls-files` shows outside two directories | **false** -- eleven paths, ten named. G-2 |
| `repo-split`: overlap 0 / public 627 / shots 178 on disk and tracked / refs 47 | 0 / 627 / 178 / 178 / 47 |
| `repo-split`: 97 = 83 + 14 `.out`, 23 cited; compendium 299,915 B | exact |
| `repo-split`: 15 tokens in 4 notes, 10 unresolved, 7 files with a prefix | 15 / 4 / 10 / 7 |
| `repo-split`: nine private targets, ten citing cards; nine printed by `make check` | 9 / 10 / 9 |
| `repo-split`: 423 files, 198.6 MB tracked by neither, dated 2026-09-21 | **435**, **201.5 MB**; dated and hedged |
| `repo-split`: collaborators 2, forks 0, `allow_forking` true; tag tree clean | exact; 0 private paths in the tag |
| `public-site-plan`: plan **240 lines on 2026-09-23** (R-2's new figure) | 240, and both of today's commits to it confirmed |
| `public-site-plan`: README 428; 89 cards; 33 = 3 + 30; 45; ten modules; 4 PNG; 5 SVG | all exact |
| `public-site-plan`: zeta 0.0083-17.07; 1.30 MB / 8.21 MB dated | [0.0083, 17.067]; **1.31 MB** / **8.41 MB**, both hedged, budget holds |
| `public-site-plan`: four decisions D1-D4; no runtime external requests | D1-D4 only; **0** external `src`/`href` fetches |
| `docs-pages-rendering`: 131 = 65 + 66; 58 + 59; 8 anchors; README 29/35/36/337/338/339, S1 40, S9 307-349 | all exact |
| `docs-pages-rendering`: the corpus diverges from GitHub by **14 characters** | **14**, on 3 of 65 pages, all of them deleted mathematics |
| `docs-pages-rendering`: the flip, and the first deployment | MemberEvent 14:35:52Z; first deploy 21:28:35Z; R-4 exact |
| `plan-page`: 167 lines, one `Status (10 Sep)`, two tracking states | 167 / 1 / private-tracked / 0 in any public commit |
| `plan-page`: address and version in `PRIVATE.md` | both present |

---

## 10. Gates, printed exactly

`make check` -- **exit 0**:

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
      cards awaiting a referee pass: 4 (docs-pages-rendering, plan-page, public-site-plan, repo-split-public-private)
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

`make rigor` -- **exit 0**: `python3 tools/check_rigor_builds.py`, 46 `ok` lines and
`46 document(s), 0 failing, 0 known`.

`../kb/bin/kb -p cft_cmi lint` -- `[cft_cmi] 0 issue(s), 4 awaiting review`, the four being this
packet.

All three were run **before** the verdicts were recorded, which is the state in which I found the
project.

**After the verdicts**, `make check` is red at `tools/build_docs.py --check`, as the Makefile's
own header predicts: `build_docs --check: the committed documentation has drifted from the
knowledge base`, the diff being `0 carry a failed referee pass` -> `2 carry a failed referee
pass` in both `status.md` and its mirror, plus two rows gaining `referee pass failed`;
`cards awaiting a referee pass: 0`; `cards whose last referee pass failed: 2 (plan-page,
repo-split-public-private)`. `make rigor` is unaffected and stays exit 0. `kb lint` is
`0 issue(s), 2 awaiting review`, both of them the failed cards. Rebuilding and committing is the
author's step, not mine.

Note what that diff shows about section 8's standing contradiction: `build_docs.py` counts a
card as carrying a failed pass only while its `review` key literally begins `FAILED`, so the
number it prints will drop back to 0 the moment the author resets the key to
`pending (was FAILED ...)` -- while the claim map, which reads History, will still say 2 and
still paint the chips. The gate is green over the gap in both directions.

---

## 11. Verdicts

- **`plan-page`: FAIL.** G-1, blocking: R-1(b) was not applied -- the History line recording the
  2026-09-14 phase-referee pass is still absent -- and a note added to the card on 2026-09-23
  says "The line is restored", which is false. The claim map served today gives this card
  `verdicts: 1` and `review_failed: true` against 15, 26, 9 and 7 for its siblings, so the only
  referee verdict the public site records for it is the failure of 2026-09-23.
  `count.never_refereed` is 0 only because a failed verdict is still a verdict, which is exactly
  the masking REF-LEAK's addendum told the next reader not to mistake for a repair. Everything
  the Statement asserts is true and re-measured. Repair G-1.
- **`repo-split-public-private`: FAIL.** G-2, blocking: R-3(d) corrected the private set to 236
  files and 48.44 MB -- both exact today -- and left standing, in the same parenthesis, the claim
  that the ten paths it enumerates are "exactly what `git --git-dir=.git-private ls-files` lists
  outside the first two directories". `ls-files` lists eleven, and the eleventh is the very file
  that made the count 236. The repair for K-8 created G-2 the way X-2 created K-3, and it ships.
  G-3: the same omission is in `PRIVATE.md`, this card's first evidence token, and in the tracked
  whitelist `pgit-exclude`. R-3(a), R-3(b), R-3(c), R-5(a) and R-5(b) are applied and true, and
  the whole clearance re-runs. Repairs G-2 and G-3.
- **`public-site-plan`: PASS.** R-2 and R-2b are applied, true and live; the document is 240
  lines and both of today's commits to it confirm the dating; every line reference into the plan
  still resolves; every figure re-measures. Three carried, non-blocking items are recorded in
  section 5, the oldest of them REF-FINAL's F-7.
- **`docs-pages-rendering`: PASS.** R-4 is applied verbatim and is the most careful sentence in
  the chain about what the feeds do and do not date; R-3 re-verifies against the live site;
  every structural figure is exact; and the 14-character divergence from GitHub, which neither
  of the last two passes certified, re-measures to the character.
- **Outside the cards: the guard.** The serialised-payload sweep closes REF-LEAK's field-list
  break completely and is worth keeping. The host determination did not keep up with it: an
  invisible or lookalike label separator, a `?@` or `#@` authority, a percent-encoded separator,
  a bare host on any of ~1,500 unlisted suffixes, a bare IP address, and `file:` and `data:` URLs
  all pass, and I drove six of them end to end into a claim-map payload. The guard still never
  runs in continuous integration, `build_docs.py` still has none at all, `make data` swallows its
  failure with `|| true`, and the `pages` job still deploys without it. Section 3 lists the six
  repairs in order of value; none of them blocks a card.
