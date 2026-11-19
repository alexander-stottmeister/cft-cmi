# Referee brief — repair round of 2026-11-19 (seats REF-RP-1 ... REF-RP-4)

## 1. Role
Referee, adversarial: the burden of proof is on the documents, patches and cards. `KB_ACTOR=REF-RP-<n>` inline on every
kb write, every kb command `-p cft_cmi`, model Opus. Workspace root /Users/alex/Documents/Uni/Hannover/claude-team
(AGENTS.md there binds you; kb = kb/bin/kb at that root); project root .../claude-team/cft_cmi (paths relative to it).
Never git, never ./pgit, never spawn agents, never edit a reviewed document, script, patch file or card text (§1: only
`kb verdict`, `kb note`, `kb set ID evidence=` for a wrong locator). Never edit a referee note; read each card's Notes
first; a competing verdict is a new note. Nothing from memory: every cited external result is checked in the PDF under
refs/ (pdftotext is installed) or marked NOT OBTAINED.

## 2. Object
The repair round changed existing documents ONLY through exact-replacement patch files rigor/repair/R<k>_patch.json
(JSON list of {file, old, new, finding, reason}); all are ALREADY APPLIED, so the "new" texts are in the files and the
"old" texts show what was there. Seat reports rigor/repair/R<k>_report.md; brief of the seats rigor/repair/REPAIR_BRIEF.md;
status file rigor/repair/REPAIR_STATUS.md; the council findings that triggered the repairs rigor/council/C1..C6_report.md
(claims of earlier referees, not truth). Card changes made by the orchestrator: rigor/repair/card_changes_1.json,
card_changes_2.json (old -> new per card section) plus dated notes (`kb -p cft_cmi show ID`, `kb -p cft_cmi history ID`).
First: `kb -p cft_cmi summary`, then `kb -p cft_cmi show ID` for each card of your seat.

## 3. Seats, checklists, deliverables (report file rigor/repair/REF_RP_<n>_report.md; scripts/outputs rigor/repair/ref_rp_<n>_*)
Per theorem/repaired step one verdict STANDS / STANDS WITH REPAIR / FAILS with the step and the counter-argument (quote
the objected sentence); per card `kb verdict ID pass` or `kb verdict ID fail --note "<repair, locator>"`. A patch that
makes a sentence true but weaker than its card supports, or stronger, fails. Direction ledger (AGENTS.md §3) for every
comparison. Every number in a card Statement under verdict recomputed independently (own script, tolerance fixed first).

REF-RP-1 Theorem B and the Moebius reduction. Objects: rigor/moebius_reduction_general_nets.tex (NEW, 14 pp, author R2);
 rigor/repair/R2_patch.json (universality_theorem_B.tex, implementation_C11.tex); the paper-2 copies in R5_patch.json
 items 11-18 (paper2/sec_setting.tex lem:ext, sec_universality.tex prop:geom, sec_implementation.tex thm:H1(ii)).
 Cards: moebius-reduction-general-nets [proved], thm-b-universality, implementer-hypotheses, mobius-reduction-cross-ratio.
 Checklist: (1) new document, every lemma: the Moebius map g, zeta = a s/(a+L) and the cross ratio (recompute exactly);
 (2) prop:cov U(g) T(f) U(g)^* = T(g_* f) for real f in H^2 with finite 3/2-norm: the smooth case as CDIT states it
 (refs/, Prop. 2.1: read the PDF; domains, closure, phase), the H^2 approximation (which topology, which Carpi-Weiner
 estimate gives strong resolvent convergence, is g_* continuous in it, does the Schwarzian/central term vanish for
 Moebius g); (3) is g_* g_tot again in the class E of the half-line chart (each of (E1)-(E3)); (4) part (b): extension
 independence for s >= 0, and "for one explicit extension for every real s": which extension and why; (5) part (c):
 exactly which hypotheses of Theorem B are used and the range s -> 0+; (6) the document's sec:open checkpoints;
 (7) R2 patch item 0: is the restated (H1) exactly what implementation_C11.tex proves (quote its theorem), and does every
 later use of (H1) in universality_theorem_B.tex (prop:H3, prop:H2, thm:B, the tensor-product proposition, prop:fermion)
 go through with the weaker form: check each use; (8) new proof of lem:ext (Trotter): each step: e^{it T(phi)} in A(I)'
 from C11 thm:H1 <1>2 (hypotheses), ktilde_b I subset I for b >= 0, T(g) = T(phi) + T(g#) on the core and essential
 self-adjointness of the sum (is "a symmetric extension of an essentially self-adjoint operator has the same closure"
 applied correctly; Trotter's hypotheses as in Reed-Simon VIII.31), passage from strong convergence of unitaries to
 Ad on M and to the states; (9) prop:geom <1>1 under ||h||_{3/2} < infinity; (10) paper-2 versions agree with the rigor
 versions and with C11 (s >= 0 in thm:H1(ii)); (11) the four cards against all of this (quantifiers, "s >= 0", "class E").
REF-RP-2 Notes, optimality, networks. Objects: rigor/repair/R3_patch.json (58 items, 13 files);
 numerics/optimality_all/theta_three_fits.py/.out. Cards: theta-value, compression-not-optimal-exact-fidelity,
 exact-fidelity-optimality-open, network-law-c-linear, network-second-order-law, vwz-protocol-ordering,
 network-global-bound-coincident, quasi-free-fidelity-formula, large-zeta-values, phi-derivative-nondecreasing.
 Checklist: (1) item 42, optimality_all_channels.tex thm:main <1>1: the new argument line by line (choice eps =
 Delta_z(t)/(2V'), eps N < 1, monotonicity in x, each inequality's direction, the claim that the old argument fails on
 [2V'/(3||t||_1), 2V'/||t||_1)); statement (1) unchanged and proved; (2) item 43; (3) items 55-56,
 network_second_order.tex thm:T5 <1>5/<2>2: the expansion with the third term, the corrected E(s), sup E -> 0 uniformly;
 (4) item 57, thm:state <1>5; (5) Note 4 items 9-13, 29 (Powers-Stormer Thm 5.1 p. 25, the concavity/Jensen derivation,
 Fuchs-van de Graaf locator, the Klein-transformation check, the Kaplansky sequence) and check_note5 items 15-16 (Araki
 1977 Thm 3.8 hypothesis; multiplicativity over graded halves): each against the PDF or by proof; (6) Note 5 items 0-8,
 14, 17-18, 39-41: each new sentence against its card (rate-of-remainder, thm-a-quadratic-law, two-chirality-law,
 all-channels-symbol-feasible); (7) items 20-22 (Jencova-Petz locators, PDF); (8) items 23-28 (check_note4 withdrawal
 markers: is the withdrawn finding really withdrawn at the end of that document); (9) items 30-54 theta wording: no
 sentence left that reads theta_fr > 0 or >= 0.38 as proved (grep the documents yourself), none over-weakened;
 (10) theta_three_fits: rerun (output to rigor/repair/ref_rp_2_theta_rerun.out, diff), re-fit family A and D with your
 own code, confirm admissibility at 1e-4 and 1e-3, the quoted ranges, "largest finite-mesh value 0.37893"; is the
 tolerance choice after the fact disclosed; (11) the ten cards (Statement, title, notes, evidence locators).
REF-RP-3 Papers. Objects: rigor/repair/R4_patch.json (paper1, 47 items), R5_patch.json (paper2, 38 items; items 11-18
 mathematics is REF-RP-1's, you check only their wording against cards). Cards: paper1-status, paper2-status,
 two-branch-law-lattice, conj-s2, boson-check, phi-unconditional-linear-bound [new, proved], hellinger-coefficient-h2
 [new, proved]. Checklist: (1) every patched sentence against the card it cites in "reason" (`kb show`): neither stronger
 nor weaker than the card; (2) after the patches, re-scan abstract, introduction and outlook of both papers for any
 remaining sentence stronger than its card (list each with file:line); (3) numbers introduced by the patches recomputed:
 0.08337/0.0834 (fidelity_tables), the large-zeta lower bounds against numerics/results_largezeta_certified.txt, 4/0.62,
 boson table headers 3.41, 4.14 and the s2 ranges against numerics/boson/boson_recovery.out, 0.3-1 % in the abstract;
 (4) R4 item 40 (new monotonicity proof in prop:monotone) against card phi-monotone-in-zeta and its document; R5 item 27
 (cor:tensor proof); R5 item 37 (Fourier convention claim: recompute <J(f)J(g)> sign); (5) the two new cards against
 rigor/quadratic_limit.tex thm:upper (first part only) and prop:h2: proof read step by step, h2 recomputed by your own
 quadrature (tolerance 1e-10); is `proved` the weakest status the evidence supports (were these theorems ever refereed:
 rigor/referee_*.tex); (6) both papers compile (copy the paper directory to your scratch, pdflatex twice; log check).
REF-RP-4 Index zero (launched after seat R1 reports): rigor/index_zero.tex, rigor/index_zero_check.py/.out,
 rigor/repair/R1_patch.json; cards group-index-zero-large-s, pushforward-blocks-equal-singular-values, rate-of-remainder
 (checklist sent with the launch message).

## 4. Conventions: `kb -p cft_cmi show cross-ratio-conventions`; each document's own convention section.
## 5. Working results: the council findings and the seats' reports are UNREFEREED; cards with status conjectural/open/
heuristic are not established; refereed cards outside your seat may be cited with locators.
## 6. Output paths (the only files you may create): rigor/repair/REF_RP_<n>_report.md, rigor/repair/ref_rp_<n>_*.py/.out,
scratch under /private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/REF_RP_<n>/
## 7. Environment: system python3 (numpy, scipy, mpmath; no flint, no pymupdf, no venv). Scripts read `PYTHON` else
python3, paths from the repository root. Over 2 min: nohup ... > out 2>&1 < /dev/null & disown, output in rigor/repair/;
else Bash timeout <= 600000 ms. No `timeout` binary; absolute paths. Other referees run in parallel: 2 cores.
## 8. Rules, report
File first: report skeleton (one section per checklist item, PENDING) within your first 3 tool calls; appends <= 100
lines / 12,000 characters; reason only to the next tool call; one checklist item per response; chat <= 5 lines. Stop
and report on every AGENTS.md §9 trigger. If budget runs short: verdicts only for what you checked, the rest under NOT
DONE, and NO `kb verdict pass` on a card whose items you did not finish. Final message: at most 400 words; one line per
card and per checklist item, failures first, each with reason and locator; `kb -p cft_cmi lint` counts; NEEDS ORCHESTRATOR.
