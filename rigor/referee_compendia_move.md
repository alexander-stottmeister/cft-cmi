# Referee REF-MOVE-1: moving the five cited-result compendia (ba14962) — FAIL
**1. The public history still holds them.** They entered in `8ab5a32` (initial import) and were tracked
publicly until this commit. Deleting them from the tip left the blobs intact: `git show
ba14962^:rigor/cited_R1.tex` returns all 70,874 bytes, and all five recover byte-for-byte (~600 kB, every
one of the 144 transcriptions). `ba14962` is already pushed — `origin/main` points at it. Nothing has
leaked, because `alexander-stottmeister/cft-cmi` is still PRIVATE; but making it public today would
publish all five in full. The history must be rewritten (`git filter-repo`, or a squashed orphan root) and
force-pushed first. Handled correctly by contrast: `rigor/shots/` and `refs/*.pdf` were never committed
publicly (`--diff-filter=A` finds nothing), and the companion has its own remote.
**2. Two pointers dangle.** `check_links.py` resolves 1103 links; a clone from `git archive HEAD` runs
`check_rigor_builds.py` to "41 document(s), 0 failing"; no `\input`/`\include` names the five;
`build_all.sh` globs and degrades cleanly. But `rigor/FINAL_REPORT.md:46` still sends a reader to
`rigor/cited_results_all.pdf` (130 pp), and `rigor/combine.py` still globs `cited_R*.tex` to rebuild the
compendium — in a public clone it finds nothing. The commit message names both and fixes neither.
**3. One public claim is wrong, two are stale.** True: 257 pages (31+32+26+38+130); 144 of 221
transcriptions by `citedbox` count (a clone has 77), though the union double-counts on both sides, so 72
of 149 are distinct; 41 documents; `INDEX.md` lost exactly the five rows (46→41) and nothing else.
**Wrong:** "176 of its excerpt images" counts literal `\shot` substrings (`\shotc`, `\shotmissing`
included). Really 172 image insertions of 256; 86 distinct images, 79 exclusive to the five, 80 still used
publicly — beside the file's own "178 images" it reads as 176/178. Stale: `.github/ISSUE_TEMPLATE/build.md`
still says "all 46 rigor documents build"; `THIRD-PARTY.md:54` and `README:375` still put 221 quotations
"in the text" (77 remain). "Each entry" overstates: 72 entries, 69 with an image, 64 verdict boxes.
**4. Only one of the two request routes exists.** An issue can be opened (blank issues are on), but
neither template fits — `claim.md` and `build.md` only. "Write to the author" is not real: no address
anywhere public, `CITATION.cff` carries none, the commit address is `users.noreply`.
**5. Cards.** The `longo-xu-cmi` edit is correct and renders as prose, not a link; `build_docs.py --check`
is clean. No other card's recipe names the five. But `docs/results/implementer-hypotheses.md:23` and
`all-channels-symbol-feasible.md:15` still point a reader at `rigor/shots/` with no caveat, and
`docs/index.md:132`'s list of privately-held material named in recipes was not extended to the compendia.
