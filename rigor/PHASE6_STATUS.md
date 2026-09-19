# Phase 6 status — multi-interval networks (O10, second half) (opened 2026-09-16)

Question: recovery error, order dependence ("holonomy") and universality of sequential one-sided zero-collar recovery along
chains A_1 ... A_n; decision of Vardhan-Wei-Zou's Protocols 1(A), 1(B), 2, 3. Brief: rigor/phase6_brief.md.
Decision card: kb -p cft_cmi show phase6-plan. Target cards: corner-calculus, network-second-order-law,
corner-correlation-kernel, vwz-protocol-ordering (all opened 2026-09-16 by the orchestrator, unrefereed).

## Tracks
- G1a analytic (rigor/network_corner_calculus.tex): corner calculus W1, amplification lemma, separation constraint W3,
  type-III sequential bound W6, Protocol 3 = over-compressed Theorem A, 1(B) = 1(A).           [done 2026-09-16, 42 pp incl. REF-P6-3 repairs; G1b, G2, G3 not yet launched]
- G1b analytic (rigor/network_second_order.tex): second-order network law W2 with the universal kernel Ghat(Delta),
  positivity, decay, closed form attempt, universality W5.                                       [not started]
- G2 numerics (numerics/networks/lattice_chain.py): sequential Gaussian Petz maps on the hopping chain, VWZ protocols,
  1:2:4 test, amplification, CMI telescoping, equal-block chains.                                [not started]
- G3 numerics (numerics/networks/corner_kernel.py): Ghat(Delta) in two independent frames (T0 modular cells, box modes),
  exact two-corner Phi at finite zeta, clustering.                                                [not started]

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
