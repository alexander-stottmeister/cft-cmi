# Phase 6 status — multi-interval networks (O10, second half) (opened 2026-09-16)

Question: recovery error, order dependence ("holonomy") and universality of sequential one-sided zero-collar recovery along
chains A_1 ... A_n; decision of Vardhan-Wei-Zou's Protocols 1(A), 1(B), 2, 3. Brief: rigor/phase6_brief.md.
Decision card: kb -p cft_cmi show phase6-plan. Target cards: corner-calculus, network-second-order-law,
corner-correlation-kernel, vwz-protocol-ordering (all opened 2026-09-16 by the orchestrator, unrefereed).

## Tracks
- G1a analytic (rigor/network_corner_calculus.tex): corner calculus W1, amplification lemma, separation constraint W3,
  type-III sequential bound W6, Protocol 3 = over-compressed Theorem A, 1(B) = 1(A).           [done 2026-09-16, 42 pp incl. REF-P6-3 repairs]
- G1b analytic (rigor/network_second_order.tex): second-order network law W2 with the universal kernel Ghat(Delta),
  positivity, decay, closed form attempt, universality W5.                                       [launched 2026-10-03 on Opus; brief rigor/phase6_g1b_brief.md; agent add86472833e623fc; done 2026-10-03, 27 pp; REF-P6-4 done 2026-10-03: 5 STAND, network-global-bound-coincident STANDS WITH REPAIR, repair by G1b 2026-10-05, REF-P6-4b PASS 2026-10-05: all six G1b cards pass]
- G2 numerics (numerics/networks/lattice_chain.py): sequential Gaussian Petz maps on the hopping chain, VWZ protocols,
  1:2:4 test, amplification, CMI telescoping, equal-block chains.                                [launched 2026-10-03 on Opus; brief rigor/phase6_g2_brief.md; agent a6c15c78d903e36b3; done 2026-10-03; REF-P6-6 2026-10-05: 3 pass, 5 stand with repair (wording/precision/disclosure); repairs applied by G2 2026-10-05; REF-P6-6b PASS 2026-10-05: all six G2 cards pass]
- G3 numerics (numerics/networks/corner_kernel.py): Ghat(Delta) in two independent frames (T0 modular cells, box modes),
  exact two-corner Phi at finite zeta, clustering.                                                [launched 2026-10-03 on Opus; brief rigor/phase6_g3_brief.md; agent a862fc647f54879c8; done 2026-10-03; REF-P6-5 2026-10-05: 1 pass, 4 stand with repair (wording/uncertainties); repairs applied by G3 2026-10-05; REF-P6-5b PASS 2026-10-05: all five G3 cards pass]

## Results
- G1a (2026-09-16, rigor/network_corner_calculus.tex, 42 pp after the REF-P6-3 repairs, Lamport; g1a_calculus.py 33/33,
  g1a_separation.py 15/15). PROVED: W1 under (H) (Thm 5.3) plus the UNCONDITIONAL rule S(Phi) = -2 sum_m sigma_m G_m'(x_m)
  delta_{x_m} (Thm 5.2); normality and dependence of the state on S(Phi) alone (Thm 6.3), single-corner universality (Cor
  6.5); vacuum rigidity, so exact recovery never occurs for any protocol WHOSE LAST STEP KEEPS A NON-EMPTY PART (Thm 7.3; a
  degenerate step conditioning on the whole block is a pure Moebius map and does recover exactly); VWZ 1(B) = 1(A) literally
  and for every common t (Prop 8.2); Protocol 3 in either order is literally one map and equals Phi_A(zeta_eff) with s' > 2
  lambda' (Thm 8.5); amplification (Lem 10.1); W3 with the constant e^{Delta_k} >= 2/eps, sharp as eps -> 0 (Thm 11.1; exact
  minima 6.8134, 20.0499, 66.6817, 200.0050, 666.6682), from the new modular identity zeta_k = sinh(D_{k+1}/2)/(sinh(D_k/2)
  sinh((D_k+D_{k+1})/2)) and e^{D_k} <= 1 + 2/zeta_k with equality at the last corner (Lem 10.3); W6 in the Bures-ANGLE form
  under hypothesis (U) (Thm 12.5) and in the Bures-DISTANCE form with NO hypothesis (Thm 12.6, Alberti-Uhlmann Prop 1(1)),
  so the second-order bound Phi_tot <= (sum sqrt(Phi_k))^2 is UNCONDITIONAL (Cor 12.7). NEW: with single-interval
  conditioning the corner measure depends only on the STARTING BLOCK and distinct pairs give distinct measures (Prop 9.1,
  Lem 9.2; n = 4, 5 tables). CORRECTION to W1: single-interval conditioning ALONE does not imply (H) (Ex. 5.6). KB: corner-
  calculus -> proved; proved cards frame-strength-amplification, vacuum-rigidity-exact-recovery, corner-separation-
  constraint, sequential-recovery-bound-type-iii, protocol-corner-data-n4-n5 (all updated after REF-P6-3).

## Referee passes (Opus only)
- REF-P6-3 (launched 2026-09-16 evening; brief rigor/phase6_referee_brief.md): document referee of G1a's
  rigor/network_corner_calculus.tex + the eight pending cards. Report rigor/referee_network_corner_calculus.tex (21 pp + second
  pass), scripts rigor/ref_p6_3_{calculus,separation}.py (76 exact checks). First pass: no theorem FAILS; 26 STAND, 5 STAND WITH
  REPAIR; [BREAK] Thm 7.3(3) overclaimed 'every non-empty protocol' (needs 'last step keeps a non-empty part'); [BREAK] FHSW weight
  pi/2(...) instead of pi (cosh 2 pi t + 1)^{-1} in Box [G5]/Prop 13.1; [GAP] Lem 10.3 (29) equality at k = n-1; [GAP] Lem 4.5 pole
  clause; [GAP] Prop 9.1 distinctness of the n-1 classes; MINORs incl. Uhlmann76 on disk (no standard-form statement; (U) stays for
  the angle form) and a (U)-free chordal route for the second-order W6 bound. G1a applied all repairs (42 pp, Sec. 15). Second pass
  (REF-P6-3b): all eight cards PASS; every repaired theorem STANDS; Cor 12.7(2) confirmed (U)-free. Four residual wording
  items (Thm 12.6/Cor 12.7 not inheriting (U) through 'in the situation of Thm 12.5'; abstract 'sharp as eps -> 0' and the
  unconditional Cor 12.7(2); Prop 8.2 theta_t range; check-script print) applied by the orchestrator 2026-09-16 23:19,
  document recompiled clean (42 pp, 0 undefined references; residual-repairs paragraph at the end). [done]
- REF-P6-0/1/2 (2026-09-16, rigor/referee_phase6_plan.md, scripts rigor/ref_p6_*.py): adversarial review of the plan and
  target cards. Verified EXACTLY: zeta = kappa beta_I(p) is the coefficient of w(y) = -4 sinh^2(y/2) 1_{y>0} (50 000 rational
  cases); same-point addition R(s1) o R(s2) = R(s1+s2); VWZ 1(B) = 1(A) as point maps; the amplification identity
  1 + z' = z of the coarse triple; the L->R chain formulas. Defects found and repaired: W1 needs the hypothesis 'every step
  conditions on a single chain interval (or no earlier corner interior to a later moving part)' -- counterexample with a
  union conditioning region moves the Schwarzian mass off the junction (ref_p6_0_w1_counterexample.out); Protocol 3 equals
  the Theorem-A map only up to a global Moebius map; the separation constraint needs ALL corners weak, numerical minimum
  e^{Delta} = 2/eps (bound unproved); 1:2:4 split into unconditional 1:4 (given the calculus) and conditional 1:2; VWZ's
  single-step coefficient 0.070 c IS our ordinary-Petz 8 f2 = 0.0675 c (the earlier '4x' reading was wrong); VWZ Fig. 25
  carries no information on Ghat (Delta_23 = log(1/eta) >= 0.46 on their axis, strengths O(1), and Phi^(2) = Phi^(3) would
  need Ghat/Ghat(0) > 1). Final: all six cards PASS (third pass).

## G1b result (2026-10-03, rigor/network_second_order.tex, 27 pp, Lamport, log clean; rigor/g1b_kernel.py -> g1b_kernel.out)
PROVED (cards, all awaiting REF-P6-4): second-order network law for the free fermion at fixed configuration, lower
(thm:T1) and upper (thm:T2) halves, cor:law [network-law-free-fermion]; the kernel in closed form, Ghat(Delta) =
(1/12 pi^2)[cosh(Delta/2) - sinh^2(Delta/2) log coth(|Delta|/4)] = int rho(q) cos(q Delta) dq with rho(q) =
tanh(pi q)/(48 pi^2 q (1+q^2)) > 0, Ghat(0) = 1/(12 pi^2), Ghat > 0, strictly decreasing, (4/3) Ghat(0) e^{-|Delta|/2}
(1 + O(e^{-|Delta|})), rate 1/2 sharp (thm:T4) [corner-kernel-closed-form]; global bound with the coincident-corner
constant Phi_tot <= -(c/2) log(1 - 2 s^2 (sum zeta_k)^2/(12 pi^2)) (thm:T3), and lem:nogroup: distinct corners do not
compose as a flow, so the conjectured network-form global bound of W2 is NOT proved [network-global-bound-coincident];
uniform UPPER bound in the separation for M = 2 (thm:T5) and 1 <= liminf <= limsup Phi(2)/Phi(1) <= 2 for VWZ (cor:vwz)
[network-upper-uniform-two-corners]; c-linearity for canonical-order right-compression protocols (L->R chains, VWZ 1(A),
2; NOT Protocol 3) under Theorem B's hypotheses (thm:T6) [network-law-c-linear]. OPEN [network-remainder-uniformity]:
uniform lower bound (M >= 2; would give Phi(2)/Phi(1) -> 2) and uniform upper bound for M >= 3; no rate in s.
Numbers (g1b_kernel.out): Ghat/Ghat(0) at Delta = 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8 = 0.8983866, 0.7456151, 0.6007454,
0.4769603, 0.2945231, 0.1797843, 0.1092990, 0.0663498, 0.0244192 (closed form, mpmath and QUADPACK agree to 2.3e-14).
Pending for the orchestrator: ./pgit sync (7 shots g1b_*.png), commit, status of network-second-order-law,
corner-correlation-kernel, vwz-protocol-ordering after REF-P6-4; G1b also recompiled rigor/findings.tex (by-products).

## Referee passes, Phase 6 second round
- REF-P6-4 (launched 2026-10-03; brief rigor/phase6_referee_g1b_brief.md; agent a7c520af4dcb14eb6): document referee of
  G1b's rigor/network_second_order.tex and the six G1b cards (verdicts on those only; G3's cards and the three
  orchestrator cards wait for G2/G3 to finish). Report rigor/referee_network_second_order.tex, scripts rigor/ref_p6_4_*.py.

## G3 result (2026-10-03, numerics/networks/corner_kernel.py 612 lines, KERNEL_RESULTS.md; outputs kernel_*.out/.npz)
NUMERICAL (cards, all awaiting REF-P6-5): R(Delta) = Ghat(Delta)/Ghat(0) at Delta = 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8 in two
independent discretisations -- T0 cells extrapolated in h = 1/4 ... 1/128 [corner-kernel-t0-frame], box modes up to
kappa_max = 120 with the envelope of kappa_max = 75 ... 120 [corner-kernel-box-frame] -- agreeing to max |R_T0 - S_box|
= 1.6e-4 (tolerance 1e-3): agreed values 0.8984(3), 0.7457(2), 0.6008(3), 0.4770(3), 0.2946(3), 0.1798(2), 0.1093(2),
0.06638(11), 0.02443(6) [corner-kernel-two-frames]; R > 0 at every grid point (R/u >= 600); decay alpha = 0.502 +- 0.004
on [3, 8] (G1b proves 1/2); the box values differ from G1b's closed form (rigor/g1b_kernel.out) by <= 3.8e-5 (comparison,
nothing fitted). K0 reproduces f3_t0_final.out, results_batch3.txt:8, line_so.txt:4 [corner-kernel-pipeline-validation].
K4: two-corner exact fidelity on box (60,30): rem/zeta^3 = -0.024, -0.014, -0.0045, -0.0006 at Delta = 1, 2, 4, 8, zeta in
[0.05, 0.2] (varies <= 20 %) [two-corner-remainder-finite-zeta]. Deviations from the brief, disclosed on the cards, for
REF-P6-5 to judge: h-ladder 1/4 ... 1/128 (grid Delta on mesh nodes) instead of 0.24 ... 0.03; a spectral-window regulator
above kappa_max ~ 33 (effect <= 2e-9 against the unregulated kappa_max = 30); fidelity by the windowed 30-digit method of
numerics/fidelity_hp.py instead of compression_box.fid_relent (which returns -log F < 0 for exact kernels at (60,30)).
MINOR code findings (not edited; orchestrator decision): numerics/defect_matrix.py computes beta_I through L - x, which
cancels for |xi - xi0| >~ 30 (2.5e-8 of max|D| at (120,45); NaN in shifted frames; the published f2 line value at (120,45)
moves 0.0084112 -> 0.0084111); compression_box.qfi_c2 returns inf at kappa_max >= 45. Noted on dhat-quadrature-certification.
- REF-P6-5 (launched 2026-10-03; brief rigor/phase6_referee_g3_brief.md; agent a92b34b7e298ece88): numerics referee of
  G3's corner_kernel.py, its outputs and five cards (verdicts on those only), with an independent recomputation of
  R(Delta) by a third algorithm. Report rigor/referee_corner_kernel.tex, scripts rigor/ref_p6_5_*.py.

## G2 result (2026-10-03, numerics/networks/lattice_chain.py 978 lines, NETWORK_RESULTS.md; outputs validate.out, N1-N6.out, *.raw)
NUMERICAL (cards, all awaiting REF-P6-6; hopping chain, ordinary Petz, two chiralities, flint ball arithmetic; sizes up to
189 sites, beyond the brief's 72, for three resolutions): V0 23/23 against exact 2^n states (|dD| = |d(-logF)| = 0 in
double precision). N1 [lattice-vwz-1b-equals-1a]: 1(B) = 1(A) exactly on the lattice (operator identity; validates the
union-conditioning pipeline, does not test the continuum limit). N2 [lattice-protocol3-equals-theorem-a]: Protocol 3 /
matched single step = 1.0001(21), 1.0006(29), 0.9999(19) at eta = 0.1, 0.2, 0.3 (thm:prot3 confirmed); against paper 1's
tables 1.007-1.020 with linear log-log interpolation (quadratic removes it: phi_cont underestimates Phi_A by 0.65-1.8 %
between nodes). N3 [lattice-vwz-protocol-ratios]: Phi(3)/Phi(1) matches Phi_A(2a/b)/Phi_A(a/b) within 0.7 %; Phi(2)/Phi(1)
= 2.21-2.50 for eta = 0.05-0.4 (a large POSITIVE cross term; the limit 2 is not approached at these eta); Phi1 < Phi2 <
Phi3 in all 26 rows, contradicting VWZ (5.10) f' < f; at eta = 0.05 (all zeta <= 0.21) the lattice estimate of
Ghat(3.00)/Ghat(0) is X = 0.281(5) against G3's 0.2951 (ratio 0.954 +- 0.015; the deficit (1 - X/S)/zeta_1 ~ 0.44 is
roughly constant over eta, i.e. a third-order correction). N4 [lattice-lr-chains-cross-terms]: the brief's "weak corners"
premise is FALSE for geometric chains (zeta = 0.49-1.04 by lem:LRdata); Phi_tot/sum Phi_step = 1.4828(4) (4 blocks) to
2.070(19) (6 blocks); chordal bound Thm 12.6 holds (max ratio 0.8695). N5 [lattice-general-rule-where-h-fails]: Ex. 5.6
exact on the lattice; REF-P6-0 geometry with a degenerate second step: lattice/prediction = 1.0012(4) under the general
rule Thm 5.2 vs 0.4988(2) under the naive rule. N6 [lattice-vwz-bounds-equal-block-chains]: VWZ (5.3)-(5.5) hold with
margin >= 4.5 (ratio <= 0.219); equal-block Phi_tot for 2-6 blocks = 0, 4.3918e-3, 1.8602e-2, 4.2301e-2, 7.3895e-2.
Notes added by G2 on corner-calculus, frame-strength-amplification (re-opened; REF-P6-6 verdicts), vwz-protocol-ordering,
network-second-order-law (orchestrator cards, updated after REF-P6-4/5). Process: G2 ran `git status` once (read-only;
§1 breach, no effect); production sweeps started after 18/23 V0 cases (all 23 passed). Orchestrator: sizes > 72 accepted.
- REF-P6-6 (launched 2026-10-03; brief rigor/phase6_referee_g2_brief.md; agent ac52db970d7bc5900): numerics referee of G2's lattice_chain.py, its
  outputs, its six cards and the two re-opened G1a cards (corner-calculus, frame-strength-amplification). Report
  rigor/referee_lattice_chain.tex, scripts rigor/ref_p6_6_*.py.
- 2026-10-03 18:33:58-18:34:58 (transcripts, REF-P6-7): all three referees died of an API rate limit (session limit). REF-P6-4 had finished its
  report (rigor/referee_network_second_order.tex, 16 pp, log clean) and recorded its six verdicts at 18:33: network-law-
  free-fermion, corner-kernel-closed-form, network-upper-uniform-two-corners, network-law-c-linear STAND; network-
  remainder-uniformity STANDS as an open question; network-global-bound-coincident STANDS WITH REPAIR (thm:T3's range
  2 s^2 Z^2/(12 pi^2) < 1 rests on RR lem:groupbound beyond its proved range |sigma| ||[P_-,K]||_2 < 1; repair: add the
  hypothesis s max_k zeta_k < pi sqrt3; also depends += corner-kernel-closed-form; MINORs on rem:kernelshape, lem:onegroup
  side conditions, g1b_kernel.py docstring). Only its final chat message was lost. REF-P6-5 and REF-P6-6 had written their
  skeletons and scripts; both resumed 2026-10-05 by SendMessage (agent-resumption), G1b resumed for the thm:T3 repair.
- 2026-10-05: G1b applied the REF-P6-4 repairs (rigor/network_second_order.tex now 29 pp, Sec. 11 'Corrections after
  REF-P6-4' R1-R6; thm:T3 under s max_k zeta_k < pi sqrt3; lem:onegroup(i)/thm:T5 side conditions; T4(e) C^1-not-C^2
  proved in the theorem; g1b_kernel.py wording; findings entry; card network-global-bound-coincident Statement + depends;
  new note on network-second-order-law). REF-P6-4b (second pass, same agent, resumed) re-reviews that card only.
- REF-P6-4b (2026-10-05, second pass, report rigor/referee_network_second_order.tex sec:pass2, 17 pp): network-global-
  bound-coincident PASSES; thm:T3 stands under s zeta_max < pi sqrt3; R1-R6 accurate; corrected g1b_kernel.py reproduces
  g1b_kernel.out byte for byte. Two residual wording items (thm:T3 <1>6 to carry <1>5's assumption; thm:T5 <1>5 to state
  <1>4's side conditions) applied by the orchestrator 2026-10-05 in rigor/network_second_order.tex (noted at the head of
  Sec. 11), recompiled (29 pp, log clean). All six G1b cards pass.
- REF-P6-5 (2026-10-05, report rigor/referee_corner_kernel.tex, 12 pp, scripts rigor/ref_p6_5_*): all G3 numbers reproduce;
  independent continuum recomputation of R(Delta) (own quadrature, Delta = 0 check 5e-12) agrees with G1b's refereed closed
  form to 4e-10 and with G3's agreed two-frame values to <= 8.5e-5 (T0 single-frame values differ by up to 1.7e-4, box by
  <= 3.7e-5). corner-kernel-pipeline-validation PASS. STANDS WITH REPAIR (verdict fail + note): corner-kernel-t0-frame
  (uncertainties omit the frame's measured extrapolation overshoot +2.8e-4; log-4f fit dropped without reason),
  corner-kernel-box-frame (no regulator-free computation on the same mesh at kappa_max = 75-120 must be stated; envelope
  replaces the fit spread at every Delta), corner-kernel-two-frames ('R < 1 at every Delta > 0' -> nine grid points; R/u
  >= 72 after the repair), two-corner-remainder-finite-zeta (inside the window the remainder is O(zeta^3) automatically:
  the coefficient is measured, not the order; eps = 1e-11 misses results_hp.txt:1 by 8.8e-6). Notes: G3's note on
  network-second-order-law overclaims O(zeta^3); on dhat-quadrature-certification fid_relent fails already at kappa_max =
  30 (noise of either sign). Process: REF-P6-5 ran `git status --porcelain rigor/` once (read-only; §1); a stderr file
  outside its permitted names was moved to the scratchpad; another agent's fill.py overwrote its own in the shared
  scratchpad (rule from now on: agents use <scratchpad>/<actor>/). K4b (2250 s) not rerun. G3 resumed for the repairs.
- 2026-10-05: G3 applied the REF-P6-5 repairs (corner_kernel.py 623 lines, T0_SYST = 3e-4; KERNEL_RESULTS.md 255 lines;
  kernel_t0_fits.out, kernel_decay.out, kernel_t0_est.npz regenerated, central values identical): t0-frame uncertainties
  now fit half-spread + 3e-4; box card states the missing regulator-free value at kappa_max = 75-120 and the envelope rule;
  two-frames: nine grid points, R/u >= 72, agreed 0.8984(5) ... 0.02443(36), alpha = 0.504 +- 0.009; K4 card retitled
  (coefficient c(Delta), O(zeta^3) automatic in the window), 8.8e-6 mismatch disclosed. Corrective notes on
  dhat-quadrature-certification, network-second-order-law, corner-correlation-kernel. K4/K4b not rerun (headers '< 0'
  disclosed). REF-P6-5b (same agent, resumed) re-reviews the four cards.
- REF-P6-5b (2026-10-05, second pass, rigor/referee_corner_kernel.tex 14 pp, checks rigor/ref_p6_5_second.out): all four
  repaired G3 cards PASS; the referee's independent R lies inside every repaired interval (0.09-0.36 of the uncertainty);
  redirected reruns of K1fit and K3 match the regenerated outputs line for line. All five G3 cards pass.
- REF-P6-6 (2026-10-05, report rigor/referee_lattice_chain.tex, 16 pp, scripts rigor/ref_p6_6_*): every G2 number
  reproduces (V0 identical; independent mpmath path to 3.5e-18; displaced corner exact; chains regenerate identically).
  PASS: lattice-vwz-1b-equals-1a, corner-calculus, frame-strength-amplification. STANDS WITH REPAIR: lattice-vwz-protocol-
  ratios (X = 0.281(5) is 3.1 spreads below the refereed closed form 0.29514; 0-dof fits; deficit O(zeta_1): X/S = 0.997 -
  0.439 zeta_1; unnormalised ratio fits), lattice-protocol3-equals-theorem-a (Q1 = 0.9940(10) is 6 spreads from 1, within
  the table interpolation uncertainty), lattice-lr-chains-cross-terms (chordal range 0.707-0.870; single-resolution chain
  1.102 omitted; 0-dof flags; 'second-order form holds' tests nothing), lattice-general-rule-where-h-fails (title '0.1 %'
  vs 0.45 % table uncertainty), lattice-vwz-bounds-equal-block-chains (title 'margin >= 5' false at eta = 0.4, n = 14:
  4.57; checks presented as results). Note on network-second-order-law: 'zeta >= 0.2' -> 'zeta_1 >= 0.5'. Orchestrator
  rule on §5 stable digits for extrapolated values: digits of the fit spread, labelled extrapolated, beside the digits
  stable across the two finest raw resolutions. G2 resumed for the repairs; then REF-P6-6b.
- 2026-10-05 orchestrator: target cards updated from the verdicts -- corner-correlation-kernel open -> PROVED (answered:
  closed form + two-frame measurement), network-second-order-law conjectural -> PROVED at fixed configuration (Statement
  separates the proved law, the open uniformity, the unproved network-form global bound; broken locator thm:sep fixed),
  vwz-protocol-ordering restated (stays conjectural: the limit 2 needs (U1)), multi-interval-networks (open items listed),
  dhat-quadrature-certification (cancellation finding absorbed; fix proposed as next), phase6-plan (all tracks done;
  next = user decisions). These six go to the final packet referee after REF-P6-6b.
- 2026-10-05: G2 applied the REF-P6-6 repairs (lattice_chain.py 1033 lines: closed-form kernel in the X comparison, 0-dof
  flags, normalised fits, NRM task -> nrm.out with largest normalisation defect 3.0e-39; NETWORK_RESULTS.md 350 lines;
  N1-N6.out regenerated from the same raw data, byte-for-byte reproducible). Five cards repaired (titles, precision,
  disclosures; no number changed; normalised R31 = 3.36(2), X/S = 0.953(15) with the linear fit 0.9975 - 0.440 zeta_1);
  corrective note on network-second-order-law. REF-P6-6b (same agent, resumed) re-reviews the five cards.
- REF-P6-6b (2026-10-05, second pass, rigor/referee_lattice_chain.tex 18 pp): all five repaired G2 cards PASS; N2-N6 and
  NRM rerun byte-identical (rigor/ref_p6_6_rerun2_*.out); normalised R31(eta = 0.1) = 3.3614(18) vs the referee's 3.3619(19).
  One stale label noted on lattice-general-rule-where-h-fails ('(W2, conjectural)'; W2 is now proved) -- left for the
  next content change of that card. All 17 Phase 6 track cards (6 G1b, 5 G3, 6 G2) and the two re-opened G1a cards pass.
- REF-P6-7 (2026-10-05; agent ab7af4071a23f0808): final packet referee (kb review --all --packet; kb/REVIEW_BRIEF.md) on the six updated
  orchestrator cards (corner-correlation-kernel, network-second-order-law, vwz-protocol-ordering, multi-interval-networks,
  dhat-quadrature-certification, phase6-plan) and the two notes in common (scratchpad-venv-fragility, agent-resumption).
- REF-P6-7 (2026-10-05, rigor/referee_phase6_cards.md, scripts rigor/ref_p6_7_*): the two common notes PASS; the six
  orchestrator cards FAIL with repairs (vwz-protocol-ordering: the rewrite had reversed the sense of the VWZ contradiction
  -- Phi1 < Phi2 < Phi3 CONFIRMS their prose and contradicts only their inequality f' < f; (5.11) is the CMI formula;
  network-second-order-law: chain range 1.46-2.07, the O(eps^{5/2}) statement restricted to all-weak L->R chains with
  cor:W3W4's proviso, thm:T3 range both conditions, c-normalised network form; corner-correlation-kernel: depends,
  uncertainties 3.6e-4-6e-4, 3.0 spreads; dhat-quadrature-certification: the 'every published number' sentence replaced by
  the two sourced facts, How to verify extended; multi-interval-networks: How to verify written, addition credited to
  corner-calculus, C11 locator Sec. 5(b); phase6-plan: G2 review state). Outside the packet: C11 Sec. 8(b) -> Sec. 5(b) in
  rigor/network_second_order.tex l. 1152 and on network-law-c-linear; c-normalisation on network-global-bound-coincident and
  in rigor/phase6_brief.md W2. All applied by the orchestrator 2026-10-05; REF-P6-7b re-reviews the eight changed cards.
- REF-P6-7b (2026-10-05, second pass, rigor/referee_phase6_cards.md): all eight repaired cards PASS; kb lint --all: 0 issues,
  0 awaiting review in every KB. Out-of-packet items: network_second_order.tex l. 1137 'C11 §8(a)' -> '§5(a)' (applied,
  dated in Sec. 11, recompiled); card two-corner-remainder-finite-zeta discloses an 8.8e-6 mismatch against
  numerics/results_hp.txt:1, a file numerics/README.md:15 marks superseded -- the current results_hp2.txt:1 agrees with
  kernel_k4_validate.out:8 to all 7 digits (REF-P6-7b); to be put on the card at its next content change (a note now
  would only re-open a passed card). Phase 6 closed 2026-10-05: 17 track cards + 2 re-opened G1a cards + 6 orchestrator
  cards + 2 common notes refereed and passed; four referee reports (REF-P6-4/4b, 5/5b, 6/6b, 7/7b).
