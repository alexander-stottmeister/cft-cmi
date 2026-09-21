# Third-party material

This repository analyses, quotes and checks published work by other authors. None of
that material is redistributed here.

## Source papers (`refs/`)

`refs/REFERENCES.md` lists every source the notes and the rigor documents rely on, with
the exact results used. The PDFs themselves are **not** in the repository. Restore the
openly available ones with

    refs/restore.sh          # list what would be fetched
    refs/restore.sh --fetch  # download from arXiv and Project Euclid

Of the 36 listed entries the script can fetch 20 from arXiv or open Project Euclid; the
remaining 16 are journal articles that need library access. The script reports them as
MANUAL. The rigor
documents cite them by exact locator, so they can be checked against any copy.

## Page excerpts (`rigor/shots/`)

The verification workflow screenshots the exact theorem or equation being relied upon,
so that a reader can see what was cited without trusting a transcription. Those 178
images are excerpts of third-party publications and are **not** redistributed.

Every document compiles without them. The macro `\shot` in `rigor/rigor_preamble.tex`
inserts the image when `rigor/shots/` is present and otherwise prints a framed note
naming the missing excerpt; the exact locator always appears in the accompanying
cited-result box. Two of the 178 excerpts are from public-domain or NIST sources
(Abramowitz and Stegun, and the DLMF); the rest are from journals and preprints.

## The cited-result compendia, available on request

Five documents collected, in one place, what every external result this project relies on actually
says: `rigor/cited_R1.tex` to `cited_R4.tex`, one per reviewer, and `cited_results_all.tex`, their
union. Together they hold 144 of the project's 221 transcriptions and 176 of its excerpt images,
257 pages in all. Each entry is a passage transcribed from the source, its exact locator, an image
of the passage, how this project uses it, and a verdict on whether the hypotheses are satisfied.

They are **not** published here. The verdicts make each entry criticism rather than reproduction,
which is what the quotation right protects, but a hundred and forty-four transcriptions gathered
into one place reads as a reader's copy of other people's work whatever the framing, and the
images they depend on are withheld anyway. Excluding them is the safer choice and costs a public
reader little, because the originals are better sources than our transcriptions of them:
`refs/REFERENCES.md` lists every one with the exact result used, and `refs/restore.sh` fetches the
openly available ones.

**Their content is available on request.** Open an issue, or write to the author. A specific
question, of the form "which locator does the project use for result X and what is its verdict",
can usually be answered in the issue itself without sending anything.

## Quotations in the text

The rigor documents contain 221 `citedbox` environments, each transcribing a theorem,
definition or equation from a source, followed by our own verdict on how it is used.
These are short attributed quotations made for the purpose of checking the cited result,
which is what the quotation right (§51 UrhG) and fair use are for. If you are a rights
holder and consider a particular quotation too long, open an issue and it will be
shortened to a paraphrase plus locator.

## Vendored software (`docs/lib/katex/`)

The site renders mathematics with **KaTeX 0.18.7**, vendored rather than loaded from a content
delivery network, so that a reader's browser makes no third-party request and the pages work from
a clone with no network at all. KaTeX is MIT-licensed; its licence travels with it in
`docs/lib/katex/LICENSE`, and the copyright stays with its authors. Only the `.woff2` fonts are
shipped, and the stylesheet's references to the older `.woff` and `.ttf` formats were removed to
match. Nothing else on the site is third-party.
