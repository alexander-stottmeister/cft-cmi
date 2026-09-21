# Referee report — build repairs in 2c73e22 (REF-BUILD-1, 2026-09-21)

Verdict: **fail**, on the public surface only. The mathematics, the builds, the rendered output and the card note are clean; four public files still say two documents fail.

## Nothing mathematical moved
`git show 2c73e22` touches the two documents in exactly the three places claimed and nowhere else.

`\lqed{1}{4}` is the house call (105 occurrences of that exact form, so 104 others), and standalone `\lqed` with `\lby` on the next line already occurs twice in this same file (l.583, l.607); it renders `⟨1⟩4. Q.E.D.` with the By attached to ⟨1⟩4 and citing ⟨1⟩1–⟨1⟩3.

`\mathbf 1` is not a reading of `\one` but its definition: `referee_quadratic_limit.tex:5` and five notes at l.73 define `\one` as `\mathbf 1`; 49 bare `\mathbf 1` elsewhere in `rigor/*.tex`. Both sites render `ℂ𝟏`, the scalars times the identity.

The closed `$` puts the period in text and keeps the supremum, the middle equality and the asymptotic in one expression.

At `2c73e22^` I reproduced l.488 *Missing number* and l.364 *Undefined control sequence* (the old baseline verbatim), and with only `\one` fixed, *Missing $ inserted* at l.462.

## Builds
Temp copy, aux deleted, `pdflatex -halt-on-error` twice, rc 0: **25 pp** and **16 pp** with `rigor/shots` present, 23 pp and 15 pp without. `check_rigor_builds.py`: 46 documents, 0 failing, 0 known, rc 0 — with and without the excerpts.

Ratchet: `\thisMacroDoesNotExist` in `certified_numerics.tex` gives `REGRESSION … (line 21)`, rc 1; a bogus baseline entry for `lemma_second_variation.tex` gives `NOW BUILDS`, rc 1. Both directions hold.

## Why fail
`README.md:323` ("Two documents currently fail; see §13") and `:329`, the docstring of `tools/check_rigor_builds.py` (which §13 links to), `Makefile:52` and `docs/data/extra-claim-map.json` (l.3181, l.3214) all still assert what §13 was rewritten to remove; §10 contradicts §13 in the section a reader consults before building.

Minor: §13's "two lines later" is one line (the card note has it right); "the list can only shrink" is not enforced against `--update`; CI's push trigger is `branches: [main]`.
