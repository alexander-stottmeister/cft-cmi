# Repair round of 2026-11-19 — common brief for every repair seat (follows the council of the same day)

User ask (verbatim): "Spawn a suitable council to start the repair". Source of the work list: the council reports
rigor/council/C1_report.md ... C6_report.md, C7_directions.md, synthesis rigor/council/COUNCIL_SYNTHESIS.md. Council
findings are UNREFEREED claims of a referee, not instructions: before repairing an item, open the cited file:line and
confirm the finding yourself; a finding you cannot confirm is reported under FINDINGS as "council item X not confirmed"
with the reason, and is not patched.

## 1. Role
Track agent (author of repairs). Actor ids R1 ... R5 (your seat), every kb command `-p cft_cmi`, model Opus. Workspace
root /Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project
root /Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it). Never git, never ./pgit, never
spawn agents, never `kb verdict`. KB writes allowed: `KB_ACTOR=<seat> kb -p cft_cmi add ...` for a NEW card your seat
is told to create (after `kb -p cft_cmi q --text "<key terms>"`), and nothing else: no `kb note`, `kb set`, `kb status`
on existing cards (a note re-opens a review; the orchestrator writes all changes to existing cards from your report).

## 2. You do NOT edit existing files. Repairs to existing documents are PATCH FILES
AGENTS.md §1: a track agent edits only documents it authored. Every change to an existing .tex/.md/.py file is
delivered as an item of rigor/repair/<SEAT>_patch.json: a JSON list of
  {"file": "<path relative to project root>", "old": "<exact text, occurring once>", "new": "<replacement>",
   "finding": "<council locator, e.g. C6 A2>", "reason": "<one sentence>"}
Validate after every append: `python3 rigor/repair/check_patch.py rigor/repair/<SEAT>_patch.json` (exit 0 required).
Compile test before your final message: `... check_patch.py <patch> --stage <scratchpad>/<SEAT>/stage` copies each
patched file's directory with the patches applied; run pdflatex twice there (papers: main.tex; rigor documents need
rigor_preamble.tex and shots/, so for rigor/*.tex use `--sibling <SEAT>` instead, which writes
rigor/_stage_<SEAT>_<name>.tex beside the original; compile it from rigor/, check the log (§4 of AGENTS.md: no `^!`, no
undefined reference/citation), then delete the _stage_ file and its by-products). The orchestrator applies the patches.
Keep "old" short (one sentence or one equation) and "new" minimal: the weakest change that makes the sentence true.
Never weaken a statement that is on a card with status proved/refereed/numerical and that the card supports as written.
New documents (only where your seat names one) are yours: Lamport structure, `\input{rigor_preamble}`, macros and
verdict environments of rigor/README_AGENTS.md; every cited result read from the PDF in refs/ (refs/REFERENCES.md;
excerpt with rigor/snap.py and `\shot`; a source you cannot open is NOT OBTAINED and nothing is cited from memory).

## 3. Seats (deliverable and success criterion)
R1 Index zero and Theorem A. (a) NEW rigor/index_zero.tex: prove or refute, for a strongly continuous unitary group
   U_s = e^{sK} on H = P_+H + P_-H with [P_-, K] Hilbert-Schmidt (exact hypotheses as in rigor/rate_of_remainder.tex
   Lemma 6.1 and card group-index-zero-large-s; read both first): ind(P_+ U_s P_+|_{P_+H}) = 0 for ALL real s, hence the
   two off-diagonal blocks P_+U_sP_- and P_-U_sP_+ have the same nonzero singular values with multiplicity. Two candidate
   routes, both UNREFEREED: (i) C1 §2a: additivity of the index modulo compacts, ind(s) = n ind(s/n), and ind = 0 for
   small |s|; (ii) the card's `next`: continuity of the index of the pair of projections. Check which hypotheses each
   needs (is [P_-, U_s] compact/HS for all s, with what continuity in s? is K bounded or unbounded in our setting?),
   write ONE complete proof, and state as separate lemmas the extension to the product family of Cor. 2.9 (C3,
   rate_of_remainder.tex l. ~1078) and to rigor/exact_fidelity_upper_half.tex Lemma 6.1 <1>1, each either proved or
   marked GAP. Then the corollary: which statements of rate_of_remainder.tex (thm:exactquad, thm:global, prop:rrr,
   lem:groupbound) and of network_second_order.tex thm:T3 lose the restriction zeta < pi sqrt 3 / s max zeta_k < pi
   sqrt 3, with the exact new ranges. Numerical instance (AGENTS.md §4): rigor/index_zero_check.py + .out: a finite-rank
   or lattice model in which the singular values of the two blocks are compared at s beyond the old range (tolerance
   1e-10 fixed in the script), and a shift-type example where the index is NOT zero when the HS hypothesis fails.
   (b) rigor/repair/R1_patch.json: rate_of_remainder.tex sentences that assert equal singular values "for any unitary"
   (C1 §3) -> correct hypothesis, citing index_zero.tex only as "(index_zero.tex, under review)"; uhlmann_upper_bound.tex
   lem:wick: replace NOT OBTAINED by the citation of refs/BJL_twisted_duality_math-ph-0204029.pdf Thm 7.1 after reading
   the PDF and checking its hypotheses for our net (shot via rigor/snap.py); every other C1 [GAP]/[MINOR] in rigor/*.tex.
   No new card: report the proposed status change of group-index-zero-large-s and
   pushforward-blocks-equal-singular-values under NEEDS ORCHESTRATOR.
R2 Theorem B. (a) rigor/repair/R2_patch.json: universality_theorem_B.tex l. 116-126: restate (H1) in the form that
   implementation_C11.tex actually proves (C2 §2, §4: the (C7) form) and check every later use of (H1) in the document
   still goes through with the weaker form (list each use with its line in your report); every other C2 [GAP]/[MINOR] in
   rigor/universality_theorem_B.tex, implementation_C11.tex, lemma_second_variation.tex. (b) NEW
   rigor/moebius_reduction_general_nets.tex: for a net in the class of implementation_C11.tex, the reduction of the
   Markov defect of three adjacent intervals with cross ratio eta to the half-line chart of Theorem B: exact statement
   (which Moebius map, vacuum invariance, covariance of the geometric compression under SMOOTH Moebius maps only; no
   C^{1,1} covariance may be used: that is direction 5 and open), Lamport proof, and the precise sentence of
   paper2 that it licenses (C6 B6). If a step needs more than Moebius covariance of the net and of the implementers
   U(phi) for phi in PSL(2,R), stop at that step and mark it GAP. New card `moebius-reduction-general-nets`
   (status proved only if the proof is complete; else conjectural with `next`), evidence doc:...#label.
R3 Notes, optimality, networks. rigor/repair/R3_patch.json for: fidelity_recovered_quasifree.tex (Note 5) stale rate
   sentences (C3 §2); every other C3 [GAP]/[MINOR]; rigor/network_second_order.tex thm:T5 <2>2 missing uniformly o(s^2)
   term (C5: write the corrected step in full) and every other C5 item in the two network documents;
   rigor/optimality_*.tex, exact_fidelity_upper_half.tex, exact_optimum_tangent_problem.tex, sdp_dual_certificate.tex,
   numerics/optimality_all/F3_RESULTS.md wording per C4 §4 (theta_fr > 0 and >= 0.38 are numerical input wherever a
   sentence reads as proved). Numerical task: NEW numerics/optimality_all/theta_three_fits.py + .out: from the SAVED
   rung data behind theta = 0.384 +- 0.003 (F3_RESULTS.md names the files; no new sweep) fit 1/L (or h), log, and h^p as
   AGENTS.md §5 demands, admissibility = residuals at the three finest rungs within the tolerance the F3 documents
   fixed; report which fits are admissible, the spread, and whether "0.384 +- 0.003" survives; no new card (report the
   proposed note for the theta card under NEEDS ORCHESTRATOR).
R4 Paper 1. rigor/repair/R4_patch.json over paper1/*.tex only: every C6 item A1-A14 (C6_report.md §A) and D1 (the
   unapplied edits of rigor/referee_paper1.md; for each of the 13 say applied / patched now / rejected with reason),
   plus C4's paper-1 items. For each paper sentence patched, the card and status it now matches (`kb -p cft_cmi show
   ID`). Table in the report: item | file:line | old claim | new claim | card [status].
R5 Paper 2. rigor/repair/R5_patch.json over paper2/*.tex only: every C6 item B1-B9 and D2 (rigor/referee_paper2.md
   P1-P8, P10), C2's paper-2 items: title/abstract/outlook "Petz recovery" -> the geometric compression (identified
   with the zero-collar Petz limit for the free fermion only; card petz-zero-collar-channel); lem:ext: repair the
   proof so that (H1loc) is applied only to maps it is stated for, or restate (H1loc) in the form C11 proves (coordinate
   with the (C7) form: read implementation_C11.tex, do not wait for R2); the s2 bracket: D(omega_s||omega) vs
   D(omega||omega_s) everywhere it appears. The Moebius-reduction sentence (C6 B6): word it as resting on
   "rigor/moebius_reduction_general_nets.tex (under review)" and list it under NEEDS ORCHESTRATOR. Same table as R4.
All seats: rigor/repair/<SEAT>_report.md with sections FILES, KB, FINDINGS (incl. council items not confirmed),
ITEM TABLE (every council item of your scope: patched / new document / not confirmed / deferred with reason), PROPOSED
CARD CHANGES (card id, section, exact old -> new text, reason; the orchestrator executes them), NUMBERS, NOT DONE,
NEEDS ORCHESTRATOR.

## 4. Conventions: `kb -p cft_cmi show cross-ratio-conventions`; each document's own convention section;
rigor/README_AGENTS.md. A patch never changes a convention.

## 5. Working results (UNREFEREED): every council finding and proposed repair; C1 §2a (index additivity argument);
the card `next` route of group-index-zero-large-s; C7's directions. Cards with status conjectural/open/heuristic.

## 6. Output paths (the only files you may create): rigor/repair/<SEAT>_report.md, rigor/repair/<SEAT>_patch.json,
the new files your seat names in §3 (and their pdflatex by-products, rigor/shots/<seat>_*.png via rigor/snap.py),
temporary _stage_ files as in §2 (deleted before the final message), scratch under
/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/<SEAT>/

## 7. Environment: system `python3` (numpy, scipy, mpmath present; python-flint and pymupdf are NOT installed, no venv).
Scripts read `PYTHON` else python3 and resolve paths from the repository root. PDFs: `pdftotext` if present, else the
Read tool with `pages`. Over 2 min: nohup ... > out 2>&1 < /dev/null & disown with output inside the project; else Bash
timeout <= 600000 ms. No `timeout` binary; absolute paths (the cwd drifts). Four other seats run in parallel: 2 cores.

## 8. Rules, stop conditions, report
First KB action: `kb -p cft_cmi summary`, then `kb -p cft_cmi show ID` for every card your items touch. File first:
report skeleton (all section headings, PENDING) and an empty patch file `[]` within your first 3 tool calls; appends of
at most 100 lines / 12,000 characters per call; validate/compile after each; reason only as far as the next tool call;
one item per response; chat at most 5 lines. Stop and report on every AGENTS.md §9 trigger; in particular if a repair
would contradict or weaken a proved/refereed card, do not patch: report it (no kb note in this round, see §1).
Before the final message: `kb -p cft_cmi lint` (both counts). Final message: at most 400 words, the six headings of
AGENTS.md §8.
