# Conventions for the rigor documents (read fully before writing)

Goal: an in-depth, critical, complete check of the notes N1-N7 in `cft_cmi/` (see refs/REFERENCES.md for the note list),
written as Lamport-style structured proofs, plus a compendium of every cited external result with screenshots.

## Files
* Each document is a standalone `\documentclass[11pt]{article}\input{rigor_preamble}` file in `cft_cmi/rigor/`, compiled with `pdflatex` (run it twice) from that directory.
* Screenshots go in `cft_cmi/rigor/shots/` as PNG, made with `rigor/snap.py <pdf> <page> <out.png> [--clip x0 y0 x1 y1] [--find "text"]`
  (fractions of the page; use `--find` to locate a theorem and choose a tight clip). Include with `\includegraphics[width=...]{shots/NAME.png}`.
* Reference PDFs go in `cft_cmi/refs/` via `refs/getref.sh <arxiv-id> <Short>` or `refs/getref.sh <URL> <Short>`. Never claim to have checked a source you could not open; write "NOT OBTAINED" and say why.
* Python for numerics: `/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team/2a3c5aab-2bd9-408c-811f-f4144c2149e4/scratchpad/venv/bin/python` (numpy, scipy, mpmath, pymupdf). Existing scripts: `cft_cmi/numerics/`.

## Lamport style (mandatory for every proof and every verification)
Follow L. Lamport, "How to Write a 21st Century Proof" (2012). Every theorem/lemma is proved by a hierarchy of numbered steps:
`\lstep{1}{1}{...}`, `\lstep{1}{2}{...}`, ...; each step is a precise assertion, or an `\lassume ... \lprove ...`, `\lsuffices`, `\lcase`, `\ldefine`, `\lpick` step;
a non-leaf step is followed by `\lproof` and its own lower-level steps `\lstep{2}{1}{...}`; a leaf step is followed by `\lby{...}` citing earlier steps
(as $\langle1\rangle3$), definitions, or an external result with an exact locator (paper, theorem number, page, equation). Every proof ends with `\lqed{level}{n}`.
Rules: state every hypothesis (domains, self-adjointness, faithfulness, convergence); no "clearly", "it is easy to see", "standard"; every equation manipulation is its own step;
every sign and normalization convention is written down once and then cited; every interchange of limits/integrals is a step with its justification.

## Verdicts
After each checked result put exactly one of `\begin{verdictok}`, `\begin{verdictgap}`, `\begin{verdictbreak}` with a one-paragraph explanation.
A **proof-breaking issue** is an error that invalidates a stated theorem/formula as written (wrong sign, wrong factor, false lemma, unjustified interchange that fails).
A **gap** is a missing argument that is likely repairable. Quote the exact sentence/equation of the note you are objecting to.

## Cited results
For every external result you rely on or that a note cites: a `\begin{citedbox}{Author Year, Theorem X}` with (i) the statement transcribed exactly (or a faithful paraphrase
marked as such), (ii) page/theorem/equation locator, (iii) a screenshot, (iv) how the note uses it, (v) verdict on the usage (conventions, hypotheses satisfied?).

## Report back
Final message to the orchestrator: at most 450 words. List: files written; each issue found as `[BREAK|GAP|MINOR] note:location - one sentence`; anything you could not obtain or finish.

## Findings entries: plain LaTeX only (added 2026-09-08)
Entries appended to findings_entries.tex are compiled inside findings.tex with rigor_preamble.tex ONLY. Do not use private macros from your own document (\Wt, \Gm, ...) and do not use the notes' shortcuts \norm, \abs, \ip, \dist, \Sone, \Stwo, \one, \dd, \Ad, \CMI, \MI: write \lVert x\rVert, \lvert x\rvert, \langle x,y\rangle, \operatorname{dist}, \mathfrak S_1, ... explicitly. (Adding these macros to rigor_preamble breaks documents that define them with \newcommand.)
