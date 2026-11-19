# Council of 2026-11-19 — assessment of cft_cmi: common brief for every seat

User ask (verbatim): "Assess the current status of the project using a suitable council of agents. Scrutinize the proof
for any critical issues. Also suggest further directions." The orchestrator split it into seven fixed seats.

## 1. Role
Seats C1-C6: referee, adversarial (the burden of proof is on the documents). Seat C7: track agent (advisory memo).
Actor ids REF-COUNCIL-C1 ... REF-COUNCIL-C6, C7; project `-p cft_cmi`; model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it).
THE KB IS READ-ONLY FOR THE COUNCIL: no `kb verdict`, `kb note`, `kb set`, `kb add`, `kb status` (other sessions may be
reviewing; §2 review race). Everything you find goes into your report file; the orchestrator writes the KB afterwards.
Never git, never ./pgit, never spawn agents, never edit any existing document, script or output.

## 2. Object (all seats)
First: `kb -p cft_cmi summary`, then `kb -p cft_cmi show ID` for the cards of your seat; `kb -p cft_cmi deps ID` shows
what a card rests on. rigor/README_AGENTS.md (pipeline conventions), rigor/INDEX.md, refs/REFERENCES.md (note list;
source PDFs in refs/, never cite from memory; a source you cannot open is NOT OBTAINED). Status files rigor/PHASE*_STATUS.md.
Earlier referee reports rigor/referee_*.tex exist for most documents: read them AFTER forming your own view of a proof,
then check whether their repairs were really applied. Record of this council: rigor/council/COUNCIL_STATUS.md.

## 3. Deliverable per seat: rigor/council/<SEAT>_report.md
Success criterion: every theorem in your scope gets one line STANDS / STANDS WITH REPAIR / FAILS with the step and the
counter-argument (quote the objected sentence or equation, file:line); every finding is classified
[BREAK] (statement false or proof invalid), [GAP] (missing argument, statement not shown false), [MINOR]; for each
[BREAK]/[GAP] say which KB cards and which paper statements inherit it (use `kb deps`). Apply the direction ledger of
AGENTS.md §3 to every verdict that compares quantities. Hunt specifically for: hypotheses of cited theorems not
checked; interchanges of limits; type-III statements justified by finite-dimensional formulas; sign/normalisation
drift between documents; circular dependencies; 'proved' cards resting on conjectural/heuristic/numerical cards;
results true-but-stronger-than-proved. Where a claim has a computable instance, recompute it independently
(own script in rigor/council/<seat>_*.py, output beside it; tolerance fixed before the run).

C1 Theorem A (free fermion): rigor/quadratic_limit.tex (thm:lower, thm:upper), rigor/uhlmann_upper_bound.tex (thm:det,
   thm:three-faces, thm:main-upper, thm:A), rigor/rate_of_remainder.tex (thm:exactquad, thm:global, thm:third and its
   corrections C1-C3), rigor/kernel_identity.tex, rigor/tail_bound.tex. Cards thm-a-quadratic-law, const-f2,
   rate-of-remainder, group-index-zero-large-s, pushforward-blocks-equal-singular-values, remainder-c3-c4-values,
   tail-constants-numerical, phi-below-0085-zeta2-numerical. Key question: does any 'proved'/'refereed' statement use
   the equal-singular-values / index-zero facts outside the range where they are proved?
C2 Theorem B (universality): rigor/universality_theorem_B.tex, rigor/implementation_C11.tex, rigor/lemma_second_variation.tex,
   universality_normalization.tex. Cards thm-b-universality, implementer-hypotheses, second-variation-lemma,
   bures-three-faces, const-gb-general-nets, stress-tensor-normalisation, boson-check. Key questions: Carpi-Weiner /
   Fewster-Hollands hypotheses for the C^{1,1} field actually met (open the PDFs); is (H1)-(H3) proved for ALL nets or a class;
   the c-linearity (H_T) argument; the constant chain c/(12 pi^2).
C3 Foundations: continuum_petz_free_fermion.tex (Note 4: zero-collar Petz map = geometric compression, Thm 7.1),
   fidelity_recovered_quasifree.tex (Note 5: Thm 2.1/3.1/3.2), rigor/check_note4.tex, rigor/check_note5_theory.tex,
   rigor/collar_and_invariant_formula.tex, adjacent_interval_cmi_longo_xu.tex. Cards petz-zero-collar-channel,
   quasi-free-fidelity-formula, longo-xu-cmi, cmi-markov-defect-interpretation, phi-derivative-nondecreasing,
   two-chirality-*. Key question: is the object 'zero-collar Petz map' a well-defined normal map on the type III algebra
   and is Phi = -log F given by the determinant formula there, with every limit justified?
C4 Optimality: rigor/optimality_second_order.tex, rigor/optimality_all_channels.tex, rigor/exact_fidelity_upper_half.tex,
   rigor/exact_optimum_tangent_problem.tex, rigor/sdp_dual_certificate.tex, numerics/optimality_all/F3_RESULTS.md. Cards
   compression-not-optimal-exact-fidelity, compression-not-second-order-minimiser, all-channel-equals-quasi-free,
   all-channels-symbol-feasible, exact-fidelity-optimality-open, theta-value (q --text theta), kkt-noise-*, tangent-h1/h2/h3,
   theta-modular-wiener-hopf. Key questions: which half of 'E_rec <= (1-theta) f2 z^2' is proved for the EXACT fidelity
   and which is numerical input; are the 8 dependency warnings of `kb -p cft_cmi deps --check` real gaps?
C5 Networks (Phase 6): rigor/network_corner_calculus.tex, rigor/network_second_order.tex. Cards corner-calculus,
   network-law-free-fermion, corner-kernel-closed-form, network-upper-uniform-two-corners, network-law-c-linear,
   network-global-bound-coincident, vwz-protocol-ordering. These were refereed in October (REF-P6-3/4): act as a SECOND,
   independent referee; concentrate on what a first referee misses: thm:T1's lem:taylor replacing analyticity, thm:T2's
   product of flows and prop:inf, thm:T6's use of Theorem B, thm:state (state depends only on the Schwarzian), cor:vwz.
C6 Papers and bookkeeping: paper1/*.tex, paper2/*.tex against the KB: every theorem, constant and adjective in the
   papers traced to a card and its status (a paper sentence stronger than its card is a [BREAK] for the paper);
   abstract/introduction overclaims; `kb -p cft_cmi deps --check` (22 warnings: which are real); cards with status
   proved whose evidence document has an unrepaired referee item. Output also a table: paper statement | card | status | ok?
C7 Directions (advisory; AGENTS.md §6 scope-narrowing applies): read the KB open/conjectural cards, open_problems_plan.tex
   (Note 8), rigor/PHASE6_STATUS.md, cross-project links (`kb links --project cft_cmi`). Deliver
   rigor/council/C7_directions.md: at most 8 candidate directions, each with (i) the exact first statement to prove,
   refute or compute, (ii) the document/script it would live in, (iii) what existing cards it rests on, (iv) the obstacle
   named concretely, (v) payoff for papers 1/2 or a paper 3, (vi) an honest difficulty/risk estimate with its reason;
   then a ranking with one paragraph of justification. Candidates to assess at least: the uniform lower bound (U1) of
   network-remainder-uniformity; the Moebius implementer step for non-canonical orders; theta as a Wiener-Hopf constant;
   s2 = c/12 / the Kubo-Mori gauge lemma; sectors-o11; index zero at large s; certification of the D-hat quadrature;
   Longo-Xu Remark 4.3 beyond free fermions; a paper 3 on networks. No new mathematics is to be claimed as established.

## 4. Conventions: kb -p cft_cmi show cross-ratio-conventions; rigor/phase6_brief.md "Setting and conventions";
each document's own convention section. A mismatch between documents is a finding; write the conversion out.

## 5. Working results: everything on a card with status conjectural/open/heuristic is UNREFEREED; statuses proved/
refereed/numerical are the claims under scrutiny, not assumptions.

## 6. Output paths (the only files you may create): rigor/council/<SEAT>_report.md (C7: C7_directions.md),
rigor/council/<seat>_*.py and their outputs rigor/council/<seat>_*.out; temporary files only under
<scratchpad>/<SEAT>/ with <scratchpad> = /private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad

## 7. Environment: V=<scratchpad>/venv (numpy, scipy, mpmath, python-flint, pymupdf; check it imports before use, it
was rebuilt today). Scripts read `PYTHON` else python3 and resolve paths from the repository root. Over 2 min: nohup
... & disown with output in rigor/council/; else Bash timeout <= 600000 ms. No `timeout` binary; absolute paths.

## 8. Rules, stop conditions, report
File first: report skeleton with every section heading and PENDING within your first 3 tool calls; appends of at most
100 lines / 12,000 characters per call; reason only as far as the next tool call; one theorem or one check per
response; chat at most 5 lines. If you run short of budget, finish the verdict table for what you did and list the
rest under NOT DONE: an honest partial report beats a complete shallow one. Stop and report on every §9 trigger.
Final message: at most 350 words: findings most severe first (`[BREAK|GAP|MINOR] file:locator — one sentence`), the
verdict lines, NOT DONE, and the path of your report.
