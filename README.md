# Conditional mutual information of adjacent intervals as a quantum-Markov defect

Author: Alexander Stottmeister, Institut für Theoretische Physik, Leibniz Universität Hannover.

For three adjacent intervals in the vacuum of a chiral conformal field theory the
Longo–Xu conditional mutual information is finite and strictly positive. This project
reads that number as the failure of a Petz recovery map, constructs the recovery channel
directly at zero collar width in the type-III setting, and measures how well it works.

## What is established

- **Theorem A.** For the zero-collar geometric compression of the free chiral fermion the
  recovery error obeys `-log F(ζ)/ζ² → c/(12π²)` exactly, with a rigorous lower bound from
  data processing and an upper bound from an Uhlmann–Bogoliubov extension.
- **Theorem B.** The same second-order coefficient `c/(12π²)` holds for every
  diffeomorphism-covariant net on the circle, under implementer hypotheses that are proved
  for all such nets.
- **Optimality.** Over all recovery channels the second-order optimum is a quasi-free
  convex programme. Its value is `(1-θ) c/(12π²) ζ²` with `θ = 0.384 ± 0.003` numerically,
  conditional on three stated hypotheses. Non-isometric channels do not help.
- **Networks.** Sequential recovery along a chain of intervals composes to a piecewise
  Möbius map whose Schwarzian is a sum of point masses at the interval junctions. The
  recovered state depends only on that corner measure, exact recovery never occurs, and
  under a stated hypothesis the outcome depends only on which pair the chain starts from.

The relative-entropy analogue `s₂ = c/12` remains a conjecture with a proved bracket, and
one gauge lemma that would have implied it is refuted here.

## Status vocabulary

Every claim in this project carries a status, and the documents use it consistently:
**proved** (a complete structured proof, refereed), **refereed** (proved and independently
reviewed), **numerical** (measured, with error bars and a convergence order),
**conjectural**, **open**, **refuted**, **superseded**. The current tally is 80 claims:
30 proved, 21 numerical, 5 verified, 3 refereed, 3 conjectural, 5 open, 1 refuted,
2 superseded, and the remainder administrative.

These statuses are maintained in a separate, private knowledge base rather than in this
repository, which is why the counts above appear here only as a summary.

Nothing labelled numerical should be read as proved. Several results here were wrong at
some point and were corrected; the errata are kept rather than erased (`rigor/errata_log.md`).

## Layout

    *.tex                 Notes 1-7: the programme, the continuum Petz map, fidelity formulas
    paper1/, paper2/      the two papers (free fermion; universality)
    rigor/                structured (Lamport-style) proofs, referee reports, phase briefs
    rigor/*_STATUS.md     what each phase did, with dates and verdicts
    numerics/             all computations: continuum, lattice, SDP, modular frames
    numerics/*/           *_RESULTS.md summarise each campaign; *.out are the raw captures
    refs/REFERENCES.md    every source relied upon, with the exact results used

## Building

Documents: `cd rigor && pdflatex -halt-on-error <file>.tex` twice, or `rigor/build_all.sh`.
They compile without the excerpt images (see THIRD-PARTY.md).

Numerics: Python with `numpy scipy mpmath python-flint cvxpy clarabel scs`. Scripts resolve
paths relative to the repository, so any checkout works. The cached intermediates
(`*.npz`, `*.pkl`) are not distributed; the scripts regenerate them, which takes hours for
the large boxes.

## How this was produced

The proofs, the referee passes, the numerics and most of the prose in `rigor/` were produced
by AI agents (Claude) working under my direction, in a fixed pipeline: every result is
written as a structured proof with an explicit hypothesis list, then attacked by an
independent referee agent that must try to break it, then repaired, then re-reviewed. Cited
external results are downloaded and checked against the source rather than quoted from
memory. Referee reports are kept in the repository next to the documents they judge.

This pipeline catches a great deal, and the errata log shows it also misses things. Treat
the structured proofs as careful mathematics that has been checked twice by machine and not
yet by a human referee, and the numerics as reproducible measurements with stated error bars.

## Licence

Code under MIT, documents and data under CC BY 4.0; see LICENSE. Third-party material is
not redistributed; see THIRD-PARTY.md.
