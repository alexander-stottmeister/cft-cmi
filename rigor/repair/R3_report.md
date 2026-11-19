# R3 report (repair round 2026-11-19)

## FILES
- /Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/rigor/repair/R3_patch.json (407 lines, 58 items over 13 files; check_patch.py: 0 problems)
- /Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/rigor/repair/R3_report.md (this file)
- /Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/optimality_all/theta_three_fits.py (175 lines), theta_three_fits.out (67 lines)
- Compile test of the patched files (pdflatex twice; log check: no `^!`, no undefined reference/citation): fidelity_recovered_quasifree 18 pp, continuum_petz_free_fermion 17 pp, cmi_as_quantum_markov_defect 9 pp (via --stage); rigor/ check_note4 39, check_note5_theory 37, collar_and_invariant_formula 8, exact_fidelity_upper_half 23, optimality_all_channels 14, sdp_dual_certificate 17, exact_optimum_tangent_problem 31, network_second_order 29, network_corner_calculus 42 (via --sibling R3). All stage files and by-products deleted.

## KB
No card added or changed (no new card for this seat). `kb -p cft_cmi lint`: 0 issues, 0 awaiting review (22 dependency/locator warnings).

## FINDINGS
- No council item of C3, C4, C5 in scope was unconfirmed; none was a BREAK. All patched or turned into card proposals (ITEM TABLE).
- [GAP] numerics/optimality_all/F3_RESULTS.md fixes no tolerance; theta_three_fits.py fixes 1e-4 (primary) and 1e-3 (secondary) before the run. 0.384 +- 0.003 survives only at the 1e-4 criterion (only h^p admissible); at 1e-3 the linear fit (0.3781-0.3810) leaves [0.381, 0.387].
- [MINOR] rigor/sdp_dual_certificate.tex:606-612, 861-863 still assert taper stability and theta = 0.300 +- 0.005 as the full supremum without pointing to F3; marked superseded (item 52).
- [MINOR] C4 F2(a) also applies to "taper-suppressed lower bound" in exact_optimum_tangent_problem.tex:1484, 1576, optimality_all_channels.tex:678, F3_RESULTS.md:7,15,225 (patched).
- [MINOR] fidelity_recovered_quasifree.tex:477 also asserted "the log^-2 corrections are a genuine zero-collar phenomenon" (not in C3's line list; patched, item 3).
- Rule note: one read-only `git status` was run by mistake (piped into a failing `head`); AGENTS.md section 1 forbids git for track agents. Nothing was changed.

## ITEM TABLE
Patch item numbers are 0-based indices into rigor/repair/R3_patch.json.

| council item | file:line (2026-11-19) | disposition |
|---|---|---|
| C3 F1 | fidelity_recovered_quasifree.tex:144, 150, 477 (two sentences), 484 | confirmed; patched (items 0-4): lim form + one-sided bound Phi - f2 zeta^2 <= f2^2 zeta^4/(1-2 f2 zeta^2) for zeta < pi sqrt 3 (card rate-of-remainder, its index-zero range) |
| C3 F2 | fidelity_recovered_quasifree.tex:435, 465 | confirmed; patched (items 5-6): 8 f2 eta^2 (1+o(1)), upper side + O(eta^3) |
| C3 F3 | fidelity_recovered_quasifree.tex:336, 452 | confirmed (certified_numerics.tex:421, 619); patched (items 7-8); card wording under PROPOSED CARD CHANGES |
| C3 F4 | continuum_petz_free_fermion.tex:252, 745, 897, 912 | confirmed; patched (items 9-12): PS70 Thm 5.1 p. 25 + Def. 1.1/p. 4; pointer to check_note4.tex Thm 8.2 (thm:normal) <1>1-<1>8; concavity derived from the Alberti formula already cited in lem:fidelity-below; Fuchs-van de Graaf = FHSW20 Lemma 3(3) eq. (58), p. 11 |
| C3 F5 | continuum_petz_free_fermion.tex:412 | confirmed (asserted only); patched (item 13): the Klein check written out |
| C3 F6 | fidelity_recovered_quasifree.tex:208 | confirmed; patched (item 14): NS sign choice stated |
| C3 F7 | rigor/check_note5_theory.tex:1249-1250 | confirmed (Araki77 Thm 3.8(2)(gamma), p. 181: "N approximately finite"); patched (item 15) |
| C3 F8 | rigor/check_note5_theory.tex:1409 | confirmed; patched (item 16): multiplicativity via block-diagonal compressions |
| C3 F9 | fidelity_recovered_quasifree.tex:415 | confirmed; patched (item 17) |
| C3 F10 | fidelity_recovered_quasifree.tex:423 | confirmed; patched (item 18): cites optimality_all_channels.tex thm:range, thm:main; restricted to even channels (the scope of thm:range / card all-channels-symbol-feasible) |
| C3 F11 | rigor/collar_and_invariant_formula.tex:411-412 | confirmed; patched (item 19): dated, marked superseded |
| C3 F12 | refs/LongoXu p. 2 (source typo) | confirmed; no repair (project uses LX Thm 3.18 + Thm 4.1(4)); recorded only |
| C3 F13 | card quasi-free-fidelity-formula | card wording; PROPOSED CARD CHANGES |
| C3 F14 | cmi_as_quantum_markov_defect.tex:311, 316 | confirmed; patched (items 20-22): Jencova-Petz arXiv:math-ph/0412093v1 Thm 2 pp. 12-13, Remark p. 14, Thm 1 (i)<=>(iv) p. 7; new bibitem (arXiv data only) |
| C3 F15 | rigor/check_note4.tex:37, 1283, 1317, 1639, 1699, 1775 | confirmed (C3 row 13; withdrawal at l. 1811-1814); patched (items 23-28): marked WITHDRAWN in place |
| C3 F16 | continuum_petz_free_fermion.tex:833 | confirmed; patched (item 29): Kaplansky sequence on the separable space |
| C4 F1 | paper1/sec_outlook.tex:72-73, 102 | paper sentence: seat R4 (not patched here); inherited rigor sentences patched: exact_fidelity_upper_half.tex abstract l. 32-34 (item 30), l. 849-852 (item 33), l. 1066 (item 36); fidelity_recovered_quasifree.tex l. 423 (item 39); optimality_all_channels.tex l. 681 (item 45); F3_RESULTS.md l. 228 (item 51) |
| C4 F2 | exact_fidelity_upper_half.tex:827, 846-852, 953, 957, 1067, 1085; fidelity_recovered_quasifree.tex:423; optimality_all_channels.tex:678, 681, 485; F3_RESULTS.md:7, 13, 15, 225; sdp_dual_certificate.tex:863; exact_optimum_tangent_problem.tex:1484, 1576 | confirmed; patched (items 30-37, 39-41, 44-54): "theta_fr >= 0.38" -> extrapolated estimate theta_fr ~ 0.384 +- 0.003, numerical input, not a bound; "taper-suppressed lower bound" -> taper-suppressed value (no proved direction). F2(c) (three fits): new script, see NUMBERS. Cards: PROPOSED CARD CHANGES |
| C4 F3 | paper1/sec_outlook.tex:102 ("5.6 times") | paper: seat R4; not patched here |
| C4 F4 | rigor/optimality_all_channels.tex:351-361 (thm:main <1>1) | confirmed (x -> x^2(1-cx) decreases on [2/(3c), 1/c)); patched (item 42): eps chosen from Delta_z(t) in eq:single; statement (1) unchanged |
| C4 S12 thm:main(2) [MINOR] | optimality_all_channels.tex:338-339 | confirmed; patched (item 43): bound D_z(1-o(1)) only for a near-optimal family |
| C4 F5 | card kkt-noise-criterion-numerics | PROPOSED CARD CHANGES |
| C4 F6 | card ac-lower-bound-zero | PROPOSED CARD CHANGES |
| C4 F7 | exact_fidelity_upper_half.tex:1162-1163 | confirmed; patched (item 38) |
| C4 Sec. 3 W4-W7 | card tangent-sdp-noise-directions | C4: checker artefact, not real; nothing to patch |
| C5 1 | cards network-law-c-linear, network-second-order-law | confirmed (network_second_order.tex:1099-1100 restricts T6 to geometric-compression steps; the document itself does not say "Petz"); PROPOSED CARD CHANGES |
| C5 2 | network_second_order.tex:1011-1021 (thm:T5 <1>5, <2>2) | confirmed (the third term Tr(A2* R1* B1 R2) is missing); patched (items 55-56): corrected step written in full, E(s) gains 2 zeta1 zeta2 eta(s zeta1) eta(s zeta2); <1>6 unchanged (sup E -> 0 still) |
| C5 3 | card network-global-bound-coincident (kb deps "modulo") | confirmed by reading thm:T3 <1>5 (uses RR C3(ii) small-norm index only); PROPOSED CARD CHANGES (dated note) |
| C5 4 | card vwz-protocol-ordering | PROPOSED CARD CHANGES |
| C5 5 | network_corner_calculus.tex:904-909 (thm:state <1>5) | confirmed; patched (item 57): normality of both states stated |
| C5 [K2](v) MINOR | network_second_order.tex:211 | C5: hypothesis met, "no repair needed"; not patched |

## PROPOSED CARD CHANGES
(The orchestrator executes them; R3 wrote nothing to the KB.)
1. quasi-free-fidelity-formula, Statement (C3 F13): old "For infinite-dimensional h the formula is obtained as the monotone limit over finite-dimensional compressions (Note 5, Thm det-rep) when the two states are quasi-equivalent." -> new "For infinite-dimensional h (two normal states on F_r(I)), -log F_{F_r(I)} = lim_n of the finite formula on P_n H_I, nondecreasing in n (Note 5 thm:det-rep); the individual factors diverge (det(1-Q_n) -> 0), only the combined finite-n expression converges, and the proof uses normality of both states, not quasi-equivalence." Reason: C3 F13, confirmed at fidelity_recovered_quasifree.tex:294-330.
2. large-zeta-values, Statement (C3 F3): old "rigorous windowed lower bounds Phi_sub" -> new "windowed lower bounds Phi_sub (lower bounds for the exact compression; computed with the uncertified double-precision D-hat quadrature, rigor/certified_numerics.tex:421, so not certified)". Same wording fix for the numerical paragraph of phi-derivative-nondecreasing ("rigorous lower bound Phi(4.267) >= 2.187e-2" -> "lower bound, modulo the uncertified D-hat quadrature"); its refutation (steps (1)-(3), analytic) is unaffected.
3. compression-not-optimal-exact-fidelity (C4 F1, F2): title old "...: the zero-collar compression is NOT optimal in exact fidelity" -> new "...: numerically, the zero-collar compression is not optimal in exact fidelity (theta_fr > 0 rests on the numerical E_D u E_D != 0)". Statement: replace "theta_fr >= 0.38, hence kappa_opt <= 0.616" and "theta_fr >= 0.38 is as well supported as theta = 0.384 +- 0.003" by "theta_fr ~ 0.384 +- 0.003 (extrapolated estimate, not a bound: every computed finite-mesh value is < 0.38, the largest 0.3789; finite-mesh values have no proved direction), hence kappa_opt <= 0.616 +- 0.003 numerically"; evidence add num:numerics/optimality_all/theta_three_fits.py. Status numerical unchanged.
4. exact-fidelity-optimality-open, Statement (C4 F2): "Numerical: theta_fr >= 0.38" -> "Numerical (extrapolated, not a bound): theta_fr ~ 0.384 +- 0.003"; and "theta_fr >= 0.38 / kappa_opt <= 0.616" likewise.
5. theta-value: title "(S10's 0.300 is a taper-suppressed lower bound)" -> "(S10's 0.300 is taper-suppressed; no proved direction)". Proposed dated note: "2026-11-19 (R3, theta_three_fits.py/.out): of the fits h, log(1/h), h^p on the finest five rungs, only h^p is admissible (residuals at the three finest rungs <= 1e-4) in all five families; h -> 0 values 0.38388-0.38445 raw, 0.38393-0.38436 y_max-corrected (spread 6e-4 < the quoted 3e-3); at tolerance 1e-3 the linear fit is admissible too for A, C, C' with 0.3781-0.3810, which leaves [0.381, 0.387]. 0.384 +- 0.003 survives at the 1e-4 criterion; it is an extrapolation (+0.008 beyond the largest computed value), not a bound." Evidence add num:numerics/optimality_all/theta_three_fits.py.
6. kkt-noise-criterion-numerics (C4 F5): "The numerics are consistent with the isometric orbit carrying the tangent optimum and kappa_opt = 1 - theta" -> "... and the tangent-programme value being (1 - theta) f2 z^2 (equal to kappa_opt only under H1 and H2, thm:value)"; or add assumes: tangent-h1-gq-differentiability, tangent-h2-minimiser-localisation.
7. ac-lower-bound-zero (C4 F6): split: keep the implication (prop:AC-zero) as proved; move "Application: ... on these three chains E_AC = 0" to a clause labelled "numerical (card ac-intertwiner-exists-hopping-chain)", or let the card cite it with `ev:` and say "proved implication; application numerical".
8. network-law-c-linear and network-second-order-law, Statement (C5 1): old "(all L->R Petz chains, VWZ Protocols 1(A) and 2)" -> new "(all L->R chains whose step maps are the geometric compressions; for the free fermion these are the Petz chains, by petz-zero-collar-channel; VWZ Protocols 1(A) and 2)".
9. network-global-bound-coincident, dated note (C5 3): "thm:T3 (network_second_order.tex l. 688-733) uses RR lem:groupbound, prop:rrr and the small-norm index argument of RR C3(ii) only, for e^{sK}, K = Dc + i h', restricted to s zeta_max < pi sqrt 3; it uses neither group-index-zero-large-s nor pushforward-blocks-equal-singular-values, so the 'modulo' of kb deps is inherited through the whole-card edge to rate-of-remainder and is not a gap of this card (nor of network-upper-uniform-two-corners)."
10. vwz-protocol-ordering, Statement (C5 4): "At second order and fixed geometry: Phi(2)/Phi(1) = ..." and "Phi(2) <= f2 (zeta_2 + zeta_3)^2 < f2 (2 zeta_1)^2 = Phi(3)" -> prefix "For the second-order coefficients of the scaled family (s -> 0 at fixed geometry), not the values at the protocols' own s = 1:" and write the inequality between those coefficients.
11. uhlmann-upper-half-proved: no change (C4 F7 was a document sentence; patched).

## NUMBERS
Command (repository root): `${PYTHON:-python3} numerics/optimality_all/theta_three_fits.py > numerics/optimality_all/theta_three_fits.out` (system python3, about 2 s). Saved rung data only (f3_t0_hladder*.out, f3_t0_final.out, f3_gal_uni.out, f3_gal_lam.out, f3_gal_ladder8.out, f3_mimic*.out; y_max law from f3_t0_ymax*.out, reproducing F3's c = 0.0315, 0.0208, order 0.599).
- Validation: synthetic 0.4 - 0.2 h^0.77 and 0.4 - 0.1 h recovered with |t - 0.4| <= 5e-12 (tol 1e-8); control 1/L fit to the h^0.77 data has residual 2.8e-3 > TOL. PASS.
- Fits on the finest 5 rungs, admissible iff max |residual| at the 3 finest <= 1e-4: h^p admissible in all 5 families (p = 0.750-0.774), 1/L and log(1/h) in none (residuals 2.9e-4 to 6.3e-3). h -> 0 values: raw 0.38388-0.38445 (spread 5.7e-4), y_max-corrected 0.38393-0.38436 (4.3e-4). All inside [0.381, 0.387].
- At 1e-3: 1/L admissible for A, C, C' (0.3781-0.3810); spread 6.3e-3 raw. log(1/h) never admissible at 1e-3 except A y_max-corrected (9.7e-4); it has no finite limit.
- Largest computed finite-mesh value: 0.37893 (circle mesh L = 2048); T0 h = 0.015: 0.37544 raw, 0.37635 corrected. Not bounds (single computations; no proved direction).

## NOT DONE
- Screenshots (`\shot`) for the new citations of PS70, FHSW20 Lemma 3, Araki77 Thm 3.8, Jencova-Petz: rigor/snap.py needs pymupdf, not installed (brief section 7). The statements were read from the PDFs with pdftotext; locators are in the patches.
- Paper sentences (paper1/sec_outlook.tex, C4 F1, F3): seat R4.
- No new sweep of theta (brief: saved data only); no second independent method for theta.
- C3 F4: the Kadison-Ringrose II section 7.1 citation already in N4 (automatic normality of a *-isomorphism) could not be checked: the book is not in refs/; left as is, the proof now also points to check_note4.tex Thm 8.2.

## NEEDS ORCHESTRATOR
- Apply rigor/repair/R3_patch.json (`check_patch.py ... --apply`) and commit it, R3_report.md, numerics/optimality_all/theta_three_fits.py/.out.
- Execute PROPOSED CARD CHANGES 1-10 (KB writes outside R3's column), then referee review.
- Items 0, 2, 4 cite the range zeta < pi sqrt 3 of rate-of-remainder; if R1's index_zero.tex is accepted the range can be widened (coordinate with R1).
- Shots for the four new citations once pymupdf is available (rigor/snap.py), then `./pgit sync`.
