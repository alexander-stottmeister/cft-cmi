# REF-ROTATE: the closed exposure and two cards (2026-09-23)

Seventeenth pass, and the third on the leak class. The order of work is the brief's: whether
the exposure is really closed, then the rebuilt guard, then the two cards and whether a repair
falsified a neighbour, then the figures, then the gates.

**A note on this file, and on why it is public-tracked.** It carries no address, old or new, no
UUID, no object or commit hash, and no identifier of any kind that would let a reader reach
anything. Every demonstration below uses the reserved placeholder host `notallowed.example`,
never a real one. It names no route that is not already named in a published field or already
visible to anyone who runs `git log` against the public remote.

There is a second reason, and it is the same measurement that caught the last two passes.
`repo-split-public-private` now fixes the private set at **235 files on 2026-09-23** and
enumerates ten paths as *exactly* what `ls-files` shows outside two directories. Holding this
note privately would make that 236 and eleven, and would falsify both halves of the same
parenthesis on the day they were repaired -- which is precisely what K-8 did to the figure and
G-2 to the list. Published, it moves only the public file count, which the sentence immediately
before it hedges by name. The safe place for this note is again the place that leaves the card
true; the trap has now been sprung three times by the same instrument, and section 4 says what
should be done about the instrument rather than about the notes.

**Verdicts: two FAIL.** The exposure itself is closed; the failures are in what the two cards
say about it.

---

## 1. Is the exposure closed? Yes -- and here is what "yes" can and cannot mean

### 1.1 The old address, probed anonymously by every route I could construct

I built the route list from three sources: the four that `CHECKLIST.md` item 3g records, the
ones the application's own markup discloses, and forms no note in this chain has named. Every
request was unauthenticated, with no cookie and no token, and every one was run against a
**control**: an identifier of the same shape that cannot exist.

| route | old address | control | plan content |
|---|---|---|---|
| the code-artifact page | 200, 23,038 B | 200, 23,038 B | none |
| the code-artifact page with a query string | 200, same length | -- | none |
| the public-artifact page | 200, 124,501 B | 200, 124,501 B | none |
| the public-artifact page, `/raw` | 200, 124,093 B | 200, 124,093 B | none |
| the short publish host (redirects to the above) | 200, same | 200, same | none |
| the `/artifact/`, `/artifacts/`, `/chat/artifacts/` and three `/api/` forms | 403 | 403 | none |
| the code-artifact page's `/raw` | 404 | -- | none |
| **the per-artifact frame content host**, which the page's own markup discloses and which no note in this chain has named | **404**, `not found` | 404 | none |
| the bare user-content host with the identifier as a path | 200, but it is the marketing home page, for any input | same | none |
| the Internet Archive CDX index, for the old address on both hosts it ever had | **no snapshot** | -- | -- |

The two bodies that do come back at 200 are the application shell. I diffed them against the
control byte for byte: the only differences are a nonce, a served-at timestamp, and the
identifier echoed back into the markup. `grep 'Status (10 Sep)'` over every body returns **0**,
and so does every other marker of the plan (`Petz`, `CMI`, `quadratic`, `recovery`, `plan`).

**The honest limit, and it matters.** For an address of the old shape, anonymous probing cannot
distinguish a deleted artifact from a private one, because the route echoes any identifier of
that shape back into the shell and serves the same bytes either way. That was already true
before the rotation -- REF-LEAK measured the same shell, at the same length class, with the same
control -- so *no* anonymous observation could ever have confirmed the deletion. What I can say
is the strongest thing the anonymous position allows: **every route yields no plan content, none
of them distinguishes the old address from an impossible one, the content host is gone, and
nothing in the public record contradicts the deletion.** The deletion itself is attested by the
owner and by item 3g, and only a holder of the old address with an account could falsify it.

I found exactly one anonymous oracle, and it works on the **new** shape rather than the old one:
the code-artifact page resolves a short identifier to an internal frame identifier and embeds it
in the markup, and returns an empty one for an identifier that does not exist. So anyone who
obtains the new address can confirm, without credentials, that the artifact exists, and can read
a second identifier out of the page. Its content host 404s, so nothing is readable -- but the
rotation's whole value is that the address is secret, and it is worth knowing that the address
is now a confirmable handle rather than an inert string. Recorded, not a defect.

### 1.2 The 41 copies are still there, and they are inert

Verified from a **fresh anonymous clone** of the public remote made for this pass, not from the
working copy:

- **41** distinct blobs of one generated data file carry the old address, in **50** of the
  **84** commits reachable from `main`, and in **no other path** of any tree of any ref.
- The tag's tree is clean. **648** distinct paths have ever existed in any tree of any ref, and
  **none** of them is an excerpt, a source PDF, a compendium, `plan_page/`, `PRIVATE.md`,
  `CHECKLIST.md` or `pgit`.
- All four routes item 3g records still serve them anonymously: the raw file host **200**, the
  blob view **200**, the blob API **200**, the tarball **200**. The file fetched anonymously
  carries the old address.

So the copies are **present and served, and dead** -- which is exactly what the card and item 3g
claim, and exactly the state the discarded-object hashes in the seven kept notes are in. They
were not removed and nobody says they were.

### 1.3 The new address is published nowhere

Swept for the new identifier, and for every fragment of it, in each of these places:

- **The deployed site.** I fetched all **188** files of the deployed tree anonymously, one
  request each: **188 of 188 returned 200**, and **0 of 188** differ from `docs/` on disk by a
  byte. The latest `github-pages` deployment, `origin/main` and local `HEAD` are one commit, and
  the public tree is clean, so the tree I swept is the tree the world is served. Over those 188
  files: **0** occurrences of the new identifier, **0** of the old one, **0** of the artifact
  host in any case, **0** of any artifact or publish route.
- **The whole public repository.** Every object in the local object store, reachable *and*
  unreachable, and every object of the fresh anonymous clone: **0**.
- **Commit and tag messages**, which the object sweep does not reach: **0**.
- **The repository's public metadata**: description, homepage, topics, releases, issues, tags,
  events, activity, the Pages record, the owner's profile, repository list, public timeline and
  gists: **0** in every one.
- **The knowledge base**, working tree and full history: **0**. (It is 404 anonymously in any
  case.)

On this machine the new address exists in **exactly one file**, `PRIVATE.md`, which is
private-tracked, in the private companion's index, and in the public `.gitignore`. That is the
state the rotation was supposed to produce.

### 1.4 Two things the sweep turned up that no register holds

1. **Every commit message in the public history carries a Claude session link** in its
   attribution trailer -- **84** of them, plus the tag message. Probed anonymously it returns
   **403**, byte-identical to a fabricated session identifier, so it is not a readable
   capability. But it is an address of the same class, on a published surface that no guard
   sweeps and no checklist item names, and it arrived without anyone deciding to publish it.
   Recorded here because the register should know it exists; it is not an exposure.
2. **Six files of the knowledge base still carry the old address** -- two generated
   (`SUMMARY.md`, `INDEX.md`, which reproduce the pre-repair Statement) and four under
   `import/`. That repository is private and the address is now dead, so this is inert. It is
   worth one line in item 3d, which today records only the discarded hashes: before the rotation
   these were a second live copy of the address, outside the register, in a repository item 3d
   contemplates publishing.

---

## 2. The rebuilt guard: REF-GUARD's nine verified, and a tenth

I called the real functions on every form and, for the ones that survived, drove the real
`build_claim_map()` against a **copy** of the knowledge base and read the string back out of the
JSON that would be written. The knowledge base was not edited; `git status` in it is unchanged
by this pass.

### 2.1 The nine, one at a time

| REF-GUARD | answered? | measured today |
|---|---|---|
| 2.1 invisible or lookalike label separator | **half** | soft hyphen and the fullwidth stop are closed by `_INVISIBLE` + NFKC. **The ideographic stops are not** -- see 2.2 below |
| 2.2 `?@` / `#@` authority | **yes** | both raise; `?` and `#` are in the terminator class |
| 2.3 percent-encoded separator | **no** (judged tolerable) | `notallowed%2Eexample/x` still passes, and WHATWG resolves it to `notallowed.example` |
| 2.4 nine hard-coded suffixes | **yes** | `[a-z]{2,}` takes any TLD; `.cloud`, `.xyz`, `.co.uk` all raise |
| 2.5 bare IP address | **no** (judged tolerable) | still passes: the last label must be letters |
| 2.6 `file:` and `data:` | **yes**, by a deny-list | both raise, as do `ftp:`, `ws:`, `blob:`, `javascript:`… A scheme *not* on the list is caught only incidentally, by the bare-host branch, and only when a path follows: `mailto:user@notallowed.example` with no path still passes |
| 2.7 non-ASCII lookalike labels | unchanged, not a route here | curiosity for the record: because the patterns are case-insensitive, U+212A and U+017F *do* fold into `k` and `s`, so `notallowed.ſtore/x` raises as `notallowed.store` |
| 2.8 what could not be got past it | **re-verified, and it holds** | a host cannot span a JSON string boundary. I re-ran value/value, list-item/list-item and key/value: the sweep sees `", "` and the file gets `,\n  `, and neither can be a host. Escapes do not help either: a newline or a quote inside a value becomes two characters in the sweep, and the truncated host is still refused |
| 2.9 the sweep is quadratic | still quadratic, **and faster** | 8 kB of a dotted run 0.34 s, 16 kB 1.5 s, 32 kB 7.3 s, 64 kB **29 s**. The lookahead prunes about sevenfold; the exponent is unchanged. The real claim map, 254 kB, sweeps in 0.18 s |
| 2.10 `www.w3.org` was added for nothing | **unchanged** | **0** occurrences in all four guarded payloads. It now also buys an asymmetry: `www.w3.org` is allowed and bare `w3.org` is refused |

**NFKC is not UTS #46, and the source comment says it is.** The comment above the patterns lists,
as one of the four structural answers, "a label separator a browser accepts and ASCII does not --
soft hyphen, zero width, fullwidth and ideographic stops -- so the text is NFKC-normalised". NFKC
maps the *fullwidth* stop to `.`; it does **not** map the ideographic stop, and it maps the
halfwidth ideographic stop to the ideographic one, which is also not `.`. Both therefore pass,
and a WHATWG URL parser resolves both to the plain host, which I verified rather than assumed.
The same gap covers the code points UTS #46 *ignores* and `_INVISIBLE` does not list -- the
variation selectors and the Mongolian free variation selectors among them: they pass the guard
and a WHATWG parser strips them. The list of six was written from the attack rather than from the
standard, and the comment claims the standard.

### 2.2 The tenth, and it is a regression the rebuild introduced

    https:/notallowed.example/code/artifact/AAAA          -- one slash

**It passes.** I drove it end to end: written into a card's Statement in a scratch knowledge
base, `build_claim_map()` completes, `check_payload` raises nothing, and the string appears
verbatim in the JSON that would be written to the claim map and rendered by module 10. The plain
two-slash form of the same address raises, which is the control.

**A browser resolves it.** Node's WHATWG URL parser -- the same algorithm every browser runs --
returns `https://notallowed.example/code/artifact/AAAA`. For a special scheme the parser skips
any number of slashes, forward or back, between the colon and the authority; one is as good as
two.

**Why it passes, and why this is the chain's signature failure rather than a new class.** The
rebuild answered two of REF-GUARD's findings with two boundary assertions, and the tenth lives
exactly between them:

- `_AUTHORITY` matches only after a literal `//`. One slash is not two, so it never fires.
- `_BARE_HOST` is new in this rebuild and carries `(?<![/\w.-])`, added so that a dotted filename
  is not read as a host. The character before the host here is `/`, so the lookbehind refuses to
  let the match start, and no later start position works either, because every one of them is
  preceded by a word character.

The gap is one character wide, and it was **created by the repair**. I reconstructed the previous
bare-host branch from REF-GUARD's description of it -- nine suffixes, no lookbehind -- and ran
both:

| form | previous guard | rebuilt guard |
|---|---|---|
| `https:/HOST/path` | **caught** | **passes** |
| `_HOST/path_` (Markdown emphasis) | **caught** | **passes** |
| `…HOST/path` (an ellipsis, which NFKC turns into three dots) | **caught** | **passes** |
| `https://HOST/path` | caught | caught |
| `HOST/path` | caught | caught |

All three of the new passes were driven end to end into a claim-map payload. The second is the
one to worry about in practice: `_host/path_` is how a card italicises an address, and the
original leak's prose was of exactly that shape. The third needs no intent at all -- an ellipsis
immediately before a bare host is ordinary prose, and these notes are full of ellipses.

**The same lookbehind, stated as a rule.** Any of `/`, `_`, `.` or a hyphenless word character
immediately before a bare host disables the bare-host branch entirely. And the matching lookahead
`(?=/)` disables it whenever the host is followed by anything other than `/`: a port, a
percent-encoded slash, a query, a backslash. (I am not claiming the port form as a browser
bypass -- a WHATWG parser reads `host:443/path` as a *scheme*, so it is a gap in the pattern
rather than a route.)

**Repair, and it is one line.** Make the authority branch tolerate the slashes a special scheme
tolerates -- `(?:[a-z][a-z0-9+.-]*:)?[/\\]{1,}` instead of `//` -- and drop `/` from the
lookbehind class, which the authority branch then covers. Better, and this is REF-GUARD's own
recommendation 1 and 3 restated: stop deciding what a host is with a character class. Fold with
UTS #46 rather than NFKC, percent-decode, then extract with a real URL parser and allow-list what
comes back. Two of the three regressions above and three of the five unrepaired findings die
together.

### 2.3 The other direction: what the guard now wrongly refuses

This is its own failure mode and the rebuild made it much larger. The scheme deny-list matches a
**word followed by a colon**, with no authority, no slash and no path required; and the bare-host
branch now reads **any** `label.label/` as a host. Calling the real function on sentences that
belong in these very cards:

| a sentence a card could contain | the guard |
|---|---|
| "What this card is about: two git repositories over one work tree." | **refused**, "a about: URL" |
| "Data: the 97 tracked .out files, 83 under numerics/ and 14 under rigor/." | **refused**, "a data: URL" |
| "File: rigor/referee_leak.md was released on 2026-09-23." | **refused**, "a file: URL" |
| "The guard rejects file: and data: URLs outright." | **refused** -- a card cannot document the guard |
| "The two documents are CHECKLIST.md/PRIVATE.md, both private-tracked." | **refused**, host `checklist.md` |
| "The MathML namespace is w3.org/1998/Math/MathML." | **refused**, host `w3.org` |
| "Fetched anonymously from raw.githubusercontent.com/owner/repo/main/x.json." | **refused** |
| "See en.wikipedia.org/wiki/… " / "Resolve it through dx.doi.org/10.…" / "A gist at gist.github.com/…" | **refused**, all three |

"This guard may only be too strict, never too lax" is the comment's own defence, and it is the
right policy; but a guard that refuses "what this card is about:" is not too strict, it is
wrong, and the person it stops is the author it exists for.

**And it is not hypothetical.** Running the guard's two patterns over the full text of every
claim card -- all sections, not only the three that ship -- they already match **five distinct
false positives**: `data:` four times, `file:` once, `api.github.com` four times,
`packages.ubuntu.com` twice, and -- the two that make the point -- `main.log` twice and
`branch.main.remote` twice, a log filename and a git configuration key read as hosts. Every one
of them is in Notes or History today, which the claim map does not ship, so `make check` is
green: I checked all three shipped fields of all 90 cards and **0** trip the guard. One sentence
moved from a note into a Statement and the build stops with "publishes a link on main.log".

**Repair.** Require the scheme deny-list to be followed by `/` or by a non-space payload, so that
an English word and a colon is not a URL; and exempt a dotted token whose last label is a known
file extension, which is REF-GUARD's own suggestion under its recommendation 3.

### 2.4 Where the guard still does not run: all four, unchanged

1. **Continuous integration still drops the claim map.** The workflow runs the generator with
   `--allow-missing-kb`, which pops the one payload built from card prose. This is now *documented*
   in the workflow's own comment -- "the claim map, the one payload built from the knowledge base" --
   but documenting it is not running it. REF-LEAK's recommendation 4 is still unapplied.
2. **`build_docs.py` still has no guard at all**: `grep -c 'ALLOWED\|foreign\|check_payload'` is
   **0**. It publishes Statement, How-to-verify, Evidence and Review into `docs/results/<id>.md`
   and the `docs/read/` mirrors. Neither card in this packet has a generated page, so neither
   rides that surface today -- but the tenth above is a *prose* form, and prose is what that
   generator ships.
3. **The `pages` job still carries no `needs:`.** A push deploys `docs/` whether or not the other
   two jobs pass.
4. **`make data` still ends in `|| true`**, so a `Drift` from the guarded generator is reported
   as success. `make check` has no `|| true` and does catch it.

---

## 3. `plan-page` -- FAIL

**G-1 is applied, and it is live.** `## History` now carries, immediately after
`- 2026-09-14 created`, the line REF-LEAK gave verbatim as R-1(b) and REF-GUARD repeated as G-1.
The consequence on the site is the one the two previous passes were arguing about: the claim map
served today gives this card **`verdicts: 3`** and `refereed: true`, against 1 when REF-GUARD
measured it, so the 2026-09-14 pass is now in the public record and not only the two failures of
2026-09-23. The false note is answered the way the author rule requires -- not rewritten, but
followed by a new dated note saying that the line was not in fact restored until today and why
the earlier attempt was lost. That is exactly right, and it is the first time in this chain that
a false note has been corrected rather than superseded.

**Everything else in the Statement re-measures**: the source is **167** lines,
`grep 'Status (10 Sep)'` returns **1**, `git ls-files plan_page` is **0** and the path is in no
tree of any ref of the public remote, the private companion tracks it, the new address is in
`PRIVATE.md`, and the Statement is published verbatim in the claim map and nowhere else on the
site. The How-to-verify executes as written. The evidence token resolves.

### DEFECT T-1 -- BLOCKING. "cannot be withdrawn from it" is false, and the sibling card on the same site is the refutation

The repaired Statement reads, and the deployed claim map carries it verbatim:

> that address is in 41 blobs of the public history **and cannot be withdrawn from it**, and it
> was closed instead by rotation on 2026-09-23

It can be withdrawn. Both private registers say so and both keep the qualifier this sentence
dropped: item 3g says "It cannot be withdrawn from the history **without a second rewrite**", and
`PRIVATE.md` says "It cannot be withdrawn from there **without another history rewrite**." The
qualifier is load-bearing, because the operation it names is not hypothetical -- this project ran
it two days earlier. `repo-split-public-private`, published verbatim on the same page of the same
site, spends a paragraph on it: the remote was deleted and recreated empty, and
`plan_page/petz_program_plan.html` "was removed from every local commit and the tag retagged".
So the site tells a reader, in one card, that a path was removed from every commit of this public
history, and in the card beside it that an address in that same history cannot be withdrawn from
it.

This is the chain's recurring failure in its plainest form: the repair carried the conclusion and
dropped the hedge, and the hedge is the only thing that made the sentence true. Both documents
that are *not* published kept it; the one that is published lost it.

**Repair T-1, verbatim.** Replace

> that address is in 41 blobs of the public history and cannot be withdrawn from it

with

> that address is in 41 blobs of the public history and could be withdrawn from it only by a second history rewrite

### DEFECT T-2 -- BLOCKING. The document this Statement sends the reader to still says the exposure is open

The Statement's operative clause is "the page was republished at a new address and the old
artifact deleted", and the sentence before it sends the reader to `PRIVATE.md` for the address.
`PRIVATE.md`, under the heading that holds the address, still reads:

> the old artifact **is to be deleted**, at which point every published copy of the old address
> is inert. **Until the old artifact is deleted the old address is still a live capability, so
> CHECKLIST item 3g stays open.**

Item 3g says `CLOSED 2026-09-23 by rotation` and "the old artifact **was** deleted". So of the
three documents that speak to the closure, two say it happened and the third -- the one the card
names, and the only one a reader is pointed at -- says it has not happened and that the register
entry is open. `PRIVATE.md` is private-tracked, so this is not an exposure; but it is not a
consistency defect of the K-6 and G-3 kind either, because it contradicts the operative claim of
a published Statement rather than a detail beside it. A reader of the card who does what the card
says is told the opposite of what the card says.

This is the third pass in a row on which an edit updated the cards and the checklist and left
`PRIVATE.md` standing: K-6 (the remotes line), G-3 (the private-set list), and now the closure
itself.

**Repair T-2, verbatim.** In `PRIVATE.md`, replace

> the old artifact is to be deleted, at which point every published copy of the old address is inert. Until the old artifact is deleted the old address is still a live capability, so CHECKLIST item 3g stays open.

with

> the old artifact was deleted on 2026-09-23, at which point every published copy of the old address became inert. CHECKLIST item 3g is closed.

### Recorded, not defects

- The `review` key reads `pending (was FAILED 2026-09-23 by REF-GUARD)`, not the form REF-LEAK's
  addendum and REF-GUARD both asked for, which also named the 2026-09-14 pass. The key ships, so
  a reader of the site still sees only the last failure in that field -- but the History line is
  the half that carries the record and the half the generator counts, and it is there, so the
  substance of R-1(b)/G-1 is discharged and this is a preference, not a defect.
- `PRIVATE.md` no longer records the version to republish (it now records the publication date
  and the source length instead). No card claims it does, so nothing is falsified; noted because
  two previous passes certified that string by name.
- The anonymous-verification limit of §1.1 belongs to this card more than to any other: its
  Statement asserts a deletion that no anonymous observation can confirm or refute. The sentence
  is not therefore wrong; it is simply not the kind of claim this chain's method can settle, and
  a later pass should not read a green probe as having settled it.

**Verdict: FAIL** on T-1 and T-2.

---

## 4. `repo-split-public-private` -- FAIL

**G-2 and G-3 are both answered, and by the cleanest route available.** Rather than weaken the
identity claim or add a filename to a published field, the project released the note and returned
the world to the sentence. Measured today:

- `./pgit check`: public **629**, private **235**, overlap **0**, uncommitted 0 and 0, shots on
  disk **178** and tracked **178**.
- `git --git-dir=.git-private ls-files` outside `rigor/shots/` and `refs/` lists **exactly ten**
  paths, and they are exactly the ten the Statement enumerates, in that order. G-2 is closed.
- `PRIVATE.md`'s list under "What this is" is the same ten. `pgit-exclude` and `PRIVATE_PATHS`
  no longer carry the note, and the public `.gitignore` rule that held it, and its comment, are
  gone. G-3 is closed in all three places.

**The whole clearance re-runs**, from a fresh anonymous clone made for this pass: refs `main`
and the draft tag only, **84** commits, **648** paths ever present in any tree of any ref and
**none** of them an excerpt, a PDF, a compendium or the plan page, the tag's tree clean.
`refs/*.pdf` **47**; `.out` **97 = 83 + 14**; the compendium **299,915 B**; nine private
evidence targets cited by **ten** cards, and `make check` printing those same nine; the
repository created 2026-09-21T19:55:13Z, `allow_forking` true, forks **0**. R-3(a), R-3(b),
R-3(c), R-5(a) and R-5(b) are all applied and all still true.

### DEFECT T-3 -- BLOCKING. Closing item 3g falsified this card's `next`, and `next` ships

`next` reads, and module 10 renders it verbatim:

> **Two items survive.** One is in this repository and is recorded in CHECKLIST.md item 3g rather
> than here, because a published field is where it was leaked in the first place. The other: the
> knowledge-base repository carries discarded cft-cmi hashes…

Item 3g is closed. Its heading is struck through and reads `CLOSED 2026-09-23 by rotation`. So
the published open-work field of the card that is *the register of what survives* counts a closed
item among the survivors, and sends the reader to an entry that says the opposite. On the same
site, the sibling card says the same thing is "now dead".

The shape is exact: K-5 put the item into `next` as a survivor and into item 3g as a register
entry; the rotation closed the register entry and nobody went back to `next`. **The repair for
K-2 created T-3 the way the repair for K-8 created G-2 and X-2 created K-3.** It is the fifth
consecutive pass on which a number or a list was updated and the sentence beside it was not, and
the first on which the stale half is a *state* rather than a count.

The 41 copies do still exist, so a sentence saying so is not wrong; what is wrong is calling them
a surviving item of open work when the entry they are recorded in is closed.

**Repair T-3, verbatim.** In `next`, replace

> Two items survive. One is in this repository and is recorded in CHECKLIST.md item 3g rather than here, because a published field is where it was leaked in the first place. The other: the knowledge-base repository carries

with

> One item survives, and one was closed on 2026-09-23. The closed one is in this repository and is recorded in CHECKLIST.md item 3g rather than here, because a published field is where it was leaked in the first place; what remains of it is inert. The one that survives: the knowledge-base repository carries

### Recorded, non-blocking

- **The K-8 trap is re-armed, and the card says so itself.** The parenthesis fixes the private
  set at 235 and then hedges it with "and it moves whenever a note is held here rather than
  published" -- which is true, and narrower than the truth: the count also moves on every new
  page excerpt and every new source PDF, which is the ordinary way it moves and the reason
  `./pgit sync` exists. R-3(d) offered "both of which move with every private commit"; the
  applied form names only the mechanism that broke it last time. Combined with the identity
  claim at the end of the same parenthesis, which REF-GUARD asked to remove and which was kept,
  a single private commit still falsifies two clauses of one sentence. Three passes have now
  landed on this parenthesis. The measurement is right today and dated, so I record it rather
  than fail the card for it -- but the instrument, not the note, is what should change: nothing
  in the Statement should be a number that a referee's own artefact moves.
- **"423 files, 198.6 MB on 2026-09-21" is 436 files, 201.6 MB today.** Dated and hedged
  ("rises by one per review"), and the drift is exactly what the hedge predicts: about thirteen
  review packets at roughly a quarter of a megabyte each. REF-GUARD measured 435 / 201.5 MB
  yesterday. Not a defect; re-measured so the next pass does not read it as fresh.
- `PRIVATE.md`, this card's **first** evidence token, contradicts item 3g about whether item 3g
  is open -- defect T-2 of §3. It is listed there because it falsifies the operative clause of
  the *other* card; here it is the third recurrence of K-6 and G-3 in this card's own evidence,
  and repair T-2 closes both.
- `secret_scanning` and its push protection are still `disabled`, which remains REF-LIVE's one
  untaken recommendation, and the one that would have caught this class at the push.

**Verdict: FAIL** on T-3.

---

## 5. Figures re-measured

| figure, and where it is | measured today |
|---|---|
| `plan-page`: the address is in 41 blobs of the public history | **41** blobs, in **50** of **84** commits reachable from `main`, and no other path |
| `plan-page`: source 167 lines, one `Status (10 Sep)`, private-tracked, 0 in any public commit | 167 / 1 / tracked privately / 0 |
| `plan-page`: the new address is in `PRIVATE.md` | present, and in no other file on this machine |
| `plan-page`: the claim map's record of this card | `verdicts` **3** (was 1), `refereed` true, `review_failed` true |
| `repo-split`: private **235 files on 2026-09-23** | **235** |
| `repo-split`: the enumeration is exactly what `ls-files` shows outside two directories | **true today** -- ten named, ten listed |
| `repo-split`: overlap 0 / public 627 / shots 178 on disk and tracked / refs 47 | 0 / **629** (hedged) / 178 / 178 / 47 |
| `repo-split`: 97 = 83 + 14 `.out`; compendium 299,915 B | exact |
| `repo-split`: nine private targets, ten citing cards; nine printed by `make check` | 9 / 10 / 9 |
| `repo-split`: 423 files, 198.6 MB tracked by neither, dated 2026-09-21 | **436**, **201.6 MB**; dated and hedged |
| `repo-split`: paths ever added, "623 on 2026-09-22", hedged as a check to re-run | **648** ever present in any tree of any ref; **0** private among them |
| `repo-split`: created 2026-09-21T19:55:13Z, forks 0, `allow_forking` true, tag tree clean | exact |
| the deployed tree | **188** files, **188** fetched 200 anonymously, **0** differing from disk |
| the guard: `www.w3.org` occurrences in the four guarded payloads | **0** |
| the guard: shipped fields of all 90 cards that trip it | **0** (and five distinct false-positive patterns already in the unshipped text) |

---

## 6. Gates, printed exactly

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

`make rigor` -- **exit 0**: `python3 tools/check_rigor_builds.py`, 46 `ok` lines and
`46 document(s), 0 failing, 0 known`.

`../kb/bin/kb -p cft_cmi lint` -- `[cft_cmi] 0 issue(s), 2 awaiting review`, the two being this
packet.

All three were run **before** the verdicts were recorded, which is the state in which I found the
project. Note that `make check` prints `cards whose last referee pass failed: 0` while the claim
map on the same site marks both of these cards `review_failed: true`: the standing contradiction
REF-GUARD recorded in its §8, unchanged, neither number false under its own definition, and
nothing comparing them.

**After the verdicts**, `make check` is red at `tools/build_docs.py --check`, as the Makefile's
own header predicts: `build_docs --check: the committed documentation has drifted from the
knowledge base`, the first difference being `0 carry a failed referee pass` -> `2 carry a failed
referee pass` in `read/status.html` and `status.md`; `cards awaiting a referee pass: 0`;
`cards whose last referee pass failed: 2 (plan-page, repo-split-public-private)`. `make rigor` is
unaffected and stays exit 0. `kb lint` is `0 issue(s), 2 awaiting review`, both of them the failed
cards. Rebuilding and committing is the author's step, not mine -- and note again what that diff
shows: the number `build_docs.py` prints will drop back to 0 the moment the author resets the
`review` key to `pending (was FAILED ...)`, while the claim map, which reads History, will still
say 2. The gate is green over the gap in both directions.

---

## 7. Verdicts

- **The exposure is closed.** The old address yields no plan content on any of the routes above,
  including the frame content host and the archive index, which no note in this chain has named;
  every response is indistinguishable from one for an identifier that cannot exist; the 41 copies
  are still in the public history, still served, and inert; and the new address is in no file, no
  object, no commit message and no metadata surface of the public repository, in none of the 188
  deployed files, and in no part of the knowledge base. It lives in one private-tracked file. The
  one thing anonymous probing cannot do is confirm a deletion, and §1.1 says so rather than
  claiming more than it measured.
- **`plan-page`: FAIL.** G-1 is applied, live and correctly annotated -- `verdicts` is 3 and the
  2026-09-14 pass is back in the public record. T-1, blocking: the Statement says the address
  "cannot be withdrawn" from the public history, dropping the qualifier that both private
  registers keep, and the sibling card on the same site describes doing exactly that to a
  different path two days earlier. T-2, blocking: `PRIVATE.md`, the document this Statement sends
  the reader to, still says the old artifact is *to be* deleted and that item 3g *stays open*.
  Repairs T-1 and T-2.
- **`repo-split-public-private`: FAIL.** G-2 and G-3 are both answered, and answered well: the
  note was released, the private set is 235, and the enumeration is again exactly what `ls-files`
  lists. The whole clearance re-runs from a fresh anonymous clone. T-3, blocking: `next`, which
  ships, still counts CHECKLIST item 3g among the items that survive, and item 3g is closed --
  the repair for one card falsified the published field of its neighbour, for the fifth
  consecutive pass. Repair T-3, and T-2 in passing, since `PRIVATE.md` is this card's first
  evidence token.
- **Outside the cards: the guard.** Four of REF-GUARD's nine are answered and hold; one is
  answered only half -- NFKC is not UTS #46, the ideographic stops and the ignored code points
  still pass, and the source comment claims they do not; the rest are unrepaired as judged. The
  tenth is a **regression the rebuild introduced**: the lookbehind added to stop filenames being
  read as hosts also stops the guard seeing a host preceded by `/`, `_` or a dot, so
  `https:/host/path`, `_host/path_` and `…host/path` all pass where the previous guard caught
  them, and a WHATWG parser resolves the first to the plain address. All three were driven end to
  end into a claim-map payload. In the other direction the rebuild is now wrong as often as it is
  right: the scheme deny-list refuses "what this card is about:", the bare-host branch refuses
  "CHECKLIST.md/PRIVATE.md" and every legitimate sibling host, and five distinct false-positive
  patterns -- including a log filename and a git configuration key -- already occur in the cards'
  unshipped text. None of it blocks a card. §2.2 and §2.3 give the repairs, and §2.4 records that
  the four places the guard does not run are unchanged.

**This report is safe to publish.** It carries no address, old or new, no UUID, no object or
commit hash, and no identifier of anything. It names no route that is not already public, and
every demonstration uses a reserved placeholder host.
