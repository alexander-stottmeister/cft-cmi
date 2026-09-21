# Referee report — build repairs in 2c73e22 (REF-BUILD-1 / 1b, 2026-09-21)

First pass: **fail**, on the public surface only. Second pass, after de02792: **pass**.

## Nothing mathematical moved
`git show 2c73e22` touches the two documents in exactly the three places claimed and nowhere else.

`\lqed{1}{4}` is the house call (105 occurrences of that exact form, so 104 others), and standalone `\lqed` with `\lby` on the next line already occurs twice in this same file (l.583, l.607); it renders `⟨1⟩4. Q.E.D.` with the By attached to ⟨1⟩4 and citing ⟨1⟩1–⟨1⟩3.

`\mathbf 1` is not a reading of `\one` but its definition: `referee_quadratic_limit.tex:5` and five notes at l.73 define `\one` as `\mathbf 1`; 49 bare `\mathbf 1` elsewhere in `rigor/*.tex`. Both sites render `ℂ𝟏`, the scalars times the identity.

The closed `$` puts the period in text and keeps the supremum, the middle equality and the asymptotic in one expression.

At `2c73e22^` I reproduced l.488 *Missing number* and l.364 *Undefined control sequence* (the old baseline verbatim), and with only `\one` fixed, *Missing $ inserted* at l.462.

## Builds
Temp copy, aux deleted, `pdflatex -halt-on-error` twice, rc 0: **25 pp** and **16 pp** with `rigor/shots` present, 23 pp and 15 pp without. `check_rigor_builds.py`: 46 documents, 0 failing, 0 known, rc 0 — with and without the excerpts.

Ratchet: `\thisMacroDoesNotExist` in `certified_numerics.tex` gives `REGRESSION … (line 21)`, rc 1; a bogus baseline entry for `lemma_second_variation.tex` gives `NOW BUILDS`, rc 1. Both directions hold.

## Why the first pass failed, and what de02792 did
`README.md:323` ("Two documents currently fail; see §13") and `:329`, the docstring of `tools/check_rigor_builds.py` (which §13 links to), `Makefile:52` and `docs/data/extra-claim-map.json` (l.3181, l.3214, through the cards `readme-and-figures` and `repo-split-public-private`) all still asserted what §13 was rewritten to remove. All four are now corrected, the two cards at source with the data regenerated (`build_site_data_extra.py --check` ok, 0 occurrences left, 1103 links resolve), and §13's "two lines later" now reads "on the next line", which is what I measured. The two `.tex` files are byte-identical to 2c73e22 and `check_rigor_builds.py` still reports 46/0/0 at HEAD.

Residual minor: README §13 still says "the list can only shrink", while the docstring and Makefile it links to now say `--update` rewrites the baseline deliberately. On the CI trigger: leave `branches: [main]`; `pull_request` covers what lands, so the sentence, not the trigger, is what is loose.
