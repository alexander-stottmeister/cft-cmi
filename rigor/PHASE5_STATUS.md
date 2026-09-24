# Phase 5 status — exact value of the all-channel optimum (started 2026-09-15)

Question: is the isometric-orbit value (1 - theta) f2 z^2 the exact all-channel second-order optimum, or do
non-isometric quasi-free channels (isometry loss N >= 0, noise 0 <= Y <= N) lower it further? And what is theta?
Brief: rigor/phase5_brief.md. Decision card: kb -p cft_cmi show phase5-plan.

## Tracks
- F1 analytic (rigor/exact_optimum_tangent_problem.tex): exact parametrisation of F by (V co-isometry, N, Y);
  tangent problem; KKT sign criterion for the noise directions; theta closed form attempt.       [done; refereed three times (REF-P5-1, REF-P5-3, REF-P5-4); repairs R1-R15, S1-S6 and D1-D3 applied; 31 pp after the corrections of 2026-09-24 (27 pp before), correction C17 below]
- F2 numerics (numerics/optimality_all/f2_*.py, F2_RESULTS.md): tangent SDP with noise in the spectral circle
  model; KKT eigenvalue check; full-F primal SDP in the Galerkin frame vs orbit.  [done 2026-09-15; cards awaiting review]
- F3 numerics (numerics/optimality_all/f3_*.py, F3_RESULTS.md): theta reconciliation between the circle model
  (0.300) and the Galerkin frame (>= 0.336, rising).                          [done 2026-09-15; cards awaiting review]

## Results
- F1 (2026-09-15): exact chart of F: (X,Z) in F iff N = 1 - XX* >= 0 and 0 <= Y = Z - X Q_BB X* <= N; X = (1-N)^{1/2} V
  with V a co-isometry iff 1 is not an eigenvalue of N (sharp). First-order defect delta^(1) = [Q,d] + A(zeta,N_1,Y_1),
  A_AD = -Q_AD zeta + (1/2) Q_AD N_1, A_DD = -(zeta* Q_DD + Q_DD zeta) + (1/2){N_1,Q_DD} - Y_1. Boundary-moving
  (non-surjective) isometry families are not a new stratum (Thm 3.11) [superseded 2026-09-24: see C5]. KKT (Thm 4.4): with t_* the SLD of the orbit
  optimum, tau_* = E_D t_* E_D, M_* = Herm((t_* Q)_DD), the orbit optimum is the global tangent optimum iff
  M_* >= 0 and M_* >= tau_* [superseded 2026-09-24: see C6]; failure gives an explicit better channel. Consistent with S10's multipliers
  (Sigma_1 = Sigma_2 - t_DD >= 0 is the noise condition). theta = geometry-free Wiener-Hopf constant in the modular
  frame (Q = (1+e^{-2 pi p})^{-1}, w(y) = -4 sinh^2(y/2) 1_{y>0}, kernel K); closed form open. Hypotheses: H1
  (differentiability along the scaled family) for the upper bound, H2 (minimisers within O(s) of the compression) [superseded 2026-09-24: see C14]
  for the lower bound; unconditional substitute = finite-s weak-duality certificate.
- F3 interim (files, 2026-09-15 16:30): the two discretisations have the SAME limit. S10's 0.300 is a taper-suppressed lower
  bound (circle model at L=256: taper (0.30,0.42) 0.2896, (0.35,0.47) 0.3618, no taper 0.1718 because of the second Fermi
  point). Galerkin uni-mesh ladder theta(h) = 0.2980, 0.3152, 0.3336, 0.3435, 0.3542, 0.3601, 0.3664, 0.3696, 0.3735 at
  h = 0.32 ... 0.02; the parameter-free modular frame of F1 Prop 6.2 (f3_t0.py) reproduces it to 0.001 at matched h and reaches
  0.3754 at h = 0.015; Lambda irrelevant; y_max converges (+0.002).
- F3 FINAL (2026-09-15): theta = 0.384 +- 0.003 (1 - theta = 0.616 +- 0.003). Convergence order h^0.77 +- 0.02 (increment
  ratio 0.586 per octave, stable over four octaves; fractional because the T0 defect kernel is homogeneous of degree 0 at the
  corner y = 0). Extrapolations: T0 uniform 0.38436/0.38421, T0 y_max=20 0.38431, Galerkin Lam=12 0.38415, Lam=8 0.38444,
  Galerkin-on-circle-mesh 0.3837+0.001; geometry spread 5e-4 over (a,L) = (1,2),(2,1),(1,4),(inf,1). Diagnosis: the circle
  model's smoothstep UV taper suppresses theta (0.278/0.290/0.362 for windows (0.20,0.32)/(0.30,0.42)/(0.35,0.47)); there is
  no taper-free lattice limit (second Fermi point: |u|^2 doubles, theta 0.172); the Galerkin functional on the circle model's own
  mesh gives the Galerkin values (0.341 ... 0.379 at L = 128 ... 2048); S10's theta_circ rises linearly in log L, so its 1/L
  Richardson used the wrong variable. S10's 0.300 +- 0.005 is a taper-suppressed LOWER bound; S10's qualitative conclusions
  stand and strengthen. Closed forms: 26 candidates tested, 3 inside [0.381, 0.387] (1 - pi^2/16 = 0.38315, 2 ln 2 - 1 = 0.38629,
  2/pi - 1/4 = 0.38662), ~0.3 expected by chance: NO selection. Cards: theta-value, circle-model-taper-suppresses-theta,
  common:taper-dependence-of-first-order-constants. Consequence once refereed: kappa_opt <= 1 - theta = 0.616 +- 0.003
  (replaces 0.71 in optimality_all_channels.tex, exact_fidelity_upper_half.tex, paper1 outlook, KB cards).
- F2 interim (files): conventions reproduced (theta 0.28958 at L=256; SLD identity 1e-10; F1's derivative formula 1e-9 by finite
  differences; stationarity check 1e-6). KKT criterion in the circle model FAILS at every L (lambda_min(M_*) < 0,
  lambda_min(M_* - tau_*) < 0) but the rank-one gain is ~1e-10 g_Q(d_c), the violation scales with the weight cap and the
  lattice violates Moebius rigidity at O(1/L) (|d_c,DD|/|d_c| = 0.075 at L=256, weighted up to the cap): artefact-suspect,
  re-evaluation in the rigid modular frame (T4) running. Tangent SDP with noise: kappa_full <= 1 - theta - 2e-4 at L=64,
  no gain found at L=128, 256 (several sub-solves failed). Galerkin full-F SDP: 8.4 g_Q(d_c) at h=0.4 — the finite frame cannot
  realise the compression (S11), uninformative.
- F2 FINAL T4 (2026-09-15, rigid parameter-free modular frame of F1 Prop 6.2, f3_t0.py machinery; ||d_c,DD|| = 0 exactly, no
  weight cap needed): the F1 identities hold to <= 3.5e-7 (SLD identity 1e-10, FD derivative formula <= 3e-8, AntiHerm((t_*Q)_DD)/||M_*|| = 2.8e-9 ... 3.5e-7; correction C13 below); lambda_min(M_*)/g_Q(d_c) = -7.0e-2, -3.8e-2, -1.9e-2, -1.0e-2 and
  lambda_min(M_*)/||M_*|| = -4.1e-3, -1.9e-3, -8.2e-4, -3.7e-4 at h = 0.24, 0.12, 0.06, 0.03; lambda_min(M_* - tau_*) identical;
  rank-one gain/g_Q(d_c) = 3.9e-4, 1.2e-4, 3.5e-5, 9.7e-6. Violation ~ h^1.15 -> 0, gain ~ h^1.85 -> 0, and at fixed h the
  violation is ~1/Ymax (outer y-truncation; the violating vector sits at y ~ (0.37-0.6) Ymax; correction C15 below), A-side cutoff irrelevant.
  VERDICT (numerical) [superseded 2026-09-24: see C7]: M_* >= 0 and M_* - tau_* >= 0 hold for the exact problem; the isometric orbit is the global optimum of the
  tangent problem, optimal N_1 = Y_1 = 0 [superseded 2026-09-24: see C7], kappa_opt = 1 - theta = 0.616 +- 0.003. Non-isometric quasi-free recoveries do not
  lower the second-order error. Cards: kkt-noise-criterion-numerics, tangent-sdp-noise-directions, galerkin-full-f-uninformative.
- F2 FINAL T5 (2026-09-15, endpoint condition (e) of the repaired criterion, rigid frame, f2_t5_endpoint.out): E(zeta_0)/g_Q(d_c) =
  +34.1, +66.9, +131.3, +258.0 at h = 0.24, 0.12, 0.06, 0.03 for the admissible (backward/dissipative) scheme; centred scheme 0 (the
  linear class), forward (inadmissible) the negative; corner term (1/2) M_*(0,0)/h = +10.3, +16.1, +24.7, +37.2 ~ h^-0.6 (M_*(y,y) ->
  +inf as y -> 0+: the junction direction is infinitely penalised at first order); saturates in Ymax, Y-independent; cross-check
  E(zeta_inf) = 2(1 - theta_h) g_Q exact to 1e-15; A-block (absorption) form = boundary form to 2e-10..7.5e-8 (correction C12 below). Correction to F1: the
  commutator form -2 b(delta_*,[Q,zeta]) is blind to the boundary form (valid only for bounded zeta); E must be defined via A(zeta,0,0).
  VERDICT (numerical) [superseded 2026-09-24: see C8]: (e) holds with a large margin; with T4, the isometric orbit is the global tangent optimum.
- Union-of-referees fix pass (2026-09-15 evening; two referees had reviewed the F2/F3 cards concurrently, PASS x5 vs FAIL x5; user
  decision relayed by session claude-team-84: authors fix all defects from the union, then ONE referee re-reviews, nobody flips
  verdicts): F3 repaired theta-value (candidate script f3_candidates.py: 26 candidates, 3 in [0.381,0.387], chance expectation 0.28,
  no selection; per-family rho 0.577..0.592; spread 5.1e-4 Galerkin / 2.0e-3 incl. T0) and the common lesson (matched same-mesh
  comparison 0.358 vs 0.290 at L=256, 0.369 vs 0.295 at L=512); F2 repaired kkt-noise-criterion-numerics (retitled as the
  extrapolation; max w ~ h^-1.65; f2_t4_h024.out; cap scan in one normalisation f2_capscan_L128.out; T5 folded in),
  tangent-sdp-noise-directions (f2_sub_gain.py broadcasting bug fixed and rerun: best gains 2.1e-4 at L=64, 5.6e-10 at L=128;
  cond 2.5e18..2.5e26 in f2_gram_cond.out; k=8 point cone-feasible), galerkin-full-f-uninformative (h=0.3 rung 7.126 vs 8.411,
  runtimes, 'factor 12' dropped). Result card all-channel-optimum-value added (orchestrator).

## Referee passes (Opus only)
- REF-P5-1 (document referee, rigor/referee_exact_optimum_tangent_problem.tex, 16 pp): STANDS for the chart of F, the first-order
  defect (recomputed), exact feasibility, Thm 3.9/Cor 3.10, Thm 4.4 (a)<=>(b)<=>(c) (no counterexample in 60 000 random triples),
  Prop 4.6/Rem 4.7, Lemma 6.1, Prop 6.2. FAILS: Thm 3.11(3) (cone equality for boundary-moving isometry directions: +lambda D_chi
  generates an outward flow; the absorption identity is vacuous on C_c^infty) => Lemma 4.2's last clause fails and Thm 4.4 needs an
  additional one-sided endpoint condition (e); Rem 6.4 and the closed-form box superseded by F3. Repairs R1-R15 (R6 semigroup,
  R7 inclusion, R10 endpoint conditions, R11 M_*, tau_* as forms with domain, R14 finite g_Q(eta) for strictness, R15 delta_* as
  projection residual, R12 theta = 0.384 +- 0.003). Factor-2 slip in S10 (C4) adjudicated (errata_log.md). F1 applied all repairs (17:30): Thm 3.11(3) -> inclusion + Rem 4.8;
  Def 4.9 (M_*, tau_* as forms on a domain); Thm 4.4 gains condition (e): E(zeta) := 2 b(delta_*, A(zeta,0,0)) = -2 b(delta_*,[Q,zeta]) [superseded 2026-09-24: see C9]
  >= 0 for every admissible isometry generator zeta; Prop 4.10: E vanishes on the linear class, E is the cyclicity anomaly (a pure
  boundary functional E = (1/2) Tr((-2 sigma_zeta) M_*) [superseded 2026-09-24: only when -2 sigma_zeta lies in the form domain of M_*, see C16]), modulo the linear class the cone [superseded 2026-09-24: see C10] is generated by zeta_0 = -E_D d/dy E_D
  (shift semigroup at the junction y = 0) and zeta_inf = -lambda D_chi|_D (moving endpoint), and E(zeta_inf) = 2 lambda (1-theta)
  g_Q(deltadot) >= 0 is PROVED (> 0 iff theta < 1, which is not proved; correction C1 below); so (e) reduces to the single number E(zeta_0) = 2 b(delta_*, [Q, E_D d/dy E_D]) >= 0 [superseded 2026-09-24: see C9 and C10], which F2 is
  computing (T5). Sec. 6 rewritten to theta = 0.384 +- 0.003. Cards repaired: tangent-problem-exact-parametrisation,
  theta-modular-wiener-hopf, kkt-noise-sign-criterion (all re-pending).
- F1 correction (21:04): E(zeta) := 2 b(delta_*, A(zeta,0,0)) only; new Prop 4.10(2'): A(zeta,0,0) = -[Q,zeta] holds only for bounded
  anti-self-adjoint zeta (deletes the boundary term otherwise); new Rem 4.11 with F2's T5 table and the reading 'the junction direction
  is infinitely penalised at first order'; Sec. 7 concludes kappa_opt = 1 - theta = 0.616 +- 0.003 conditional on H1, H2, with (a),(e)
  as numerical input. Document 25 pp (26 pp after S1-S6). Final single referee REF-P5-3 (document + all 14 pending cards) launched 21:05.
- REF-P5-3 (21:29; rigor/referee2_exact_optimum_tangent_problem.tex, 7 pp): R1-R15 applied, no regressions; NEW FINDING S1: the
  reduction of the admissible cone of boundary-moving isometry generators to the two model directions is proved only for vector
  fields (multiplicity > 1 shift semigroups and unbounded skew-adjoint multiplication operators escape) => condition (e) is reduced to
  E(zeta_0) >= 0 only under a hypothesis H3 (cone hypothesis) [superseded 2026-09-24: see C11]; repairs S1-S6 (H3 declared and every '(e) holds' hedged; the T5 total is
  the scheme-dependent upwind-viscosity quantity ~h^-0.97, the corner term ~h^-0.60 is the invariant piece; E in [-inf,+inf] with the
  form domain a subspace; Thm 3.11 <1>4 core hypothesis; Sec. 7 item 5; minor slips). Cards: 9 pass (theta-value,
  tangent-sdp-noise-directions, galerkin-full-f-uninformative, the 5 propagated cards, common lesson, referee-race lesson), 5 fail:
  three F1 cards because 'kb set statement=' had written front-matter keys instead of the Statement sections (tool pitfall; fixed in
  kb/kbcore/store.py: set_meta now routes statement/verify/notes into the sections, lint flags leftover keys; lesson card
  claude-team-knowledge:kb-set-section-keys), kkt-noise-criterion-numerics (FD tolerance regression; fixed by F2, total vs corner
  labelled), all-channel-optimum-value (unproved reduction of (e); hedged with H3 by the orchestrator). F1 applying S1-S6 and moving
  its three cards' repaired text into the sections; one small referee pass follows, then kb sync.
  RESULT AS IT STANDS: kappa_opt = 1 - theta = 0.616 +- 0.003 numerically, conditional on H1, H2, H3; unconditional bracket
  E_rec in [dual form, 0.616 f2 z^2 (1+o(1))].
- REF-P5-4 (21:55; rigor/referee3_exact_optimum_tangent_problem.tex, 4 pp): S1-S6 all applied, H3 usage sound (bilinearity of b and
  b(delta_*, closure of L) = 0 by g_Q-continuity); document ACCEPTED with three residual defects on the H3 wording: D1 the
  'equivalently ... boundary form' clause of Def 4.12 is not equivalent to eq. (33) and is trivially met by the excluded family
  zeta = i m(y); D2 Thm 3.11(3) is stated with 'G an isometry generator' while <1>4 no longer proves it; D3 the ambient space of (33)
  is unspecified and, with A(zeta_0,0,0) outside the form domain, forces alpha = 0 so that under H3 condition (e) collapses to the
  proved E(zeta_inf) >= 0 (not > 0, which needs theta < 1, not proved; correction C1 below) — i.e. the content of H3 is the exclusion of non-vector-field generators (F1 fixing D1-D3). Cards: seven
  pass (tangent-problem-exact-parametrisation, theta-modular-wiener-hopf, kkt-noise-sign-criterion, kkt-noise-criterion-numerics,
  phase5-plan, claude-team-knowledge:kb-set-section-keys, dmax_mbz:no-reduction-as-progress); all-channel-optimum-value FAILED for a
  title omitting H3 and for quoting the scheme-dependent total as a margin (fixed 21:52: title 'H1, H2, H3'; corner row quoted; (e)
  vacuous at zeta_0 / proved at zeta_inf, model cone only) — re-verdict pending. Minor stale clauses recorded in the pass notes
  (CG-residual range on kkt-noise-sign-criterion; swapped FD values on kkt-noise-criterion-numerics; 'one such card remains in
  dmax_mbz' on kb-set-section-keys; 'review state kept' in the dmax note).
- F1 D1-D3 fix (22:05, 27 pp): H3 (Def 4.12) is eq. (33) alone, read in the form domain F: every admissible isometry generator with
  A(zeta,0,0) in F has A(zeta,0,0) = alpha A(zeta_0,0,0) + beta A(zeta_inf,0,0) + eta, alpha, beta >= 0, eta in the closure of L; new
  Rem 4.14: given that A(zeta_0,0,0) is not in F (numerical, not proved: F2's divergent corner term; correction C4 below), alpha = 0 is forced, so H3 says 'every admissible generator carrying a feasible first-order
  datum is, modulo the closure of L, a non-negative multiple of zeta_inf', and (e) holds outright under H3 via the proved
  E(zeta_inf) = 2 lambda (1 - theta) g_Q >= 0 (> 0 iff theta < 1, not proved; correction C1 below); the content of H3 is the EXCLUSION of the two non-vector-field families (multiplicity > 1
  shift semigroups; unbounded skew-adjoint multiplication operators); the scalar test (31) is operative only for regularised junction
  directions (what F2 T5 measures). Thm 3.11(3) restated (G = sigma - zeta*, not claimed to generate a semigroup; sign corrected, correction C2 below). Card
  kkt-noise-sign-criterion rewritten accordingly (re-verdict by REF-P5-4 pending), then a second kb sync.
- Phase 5 closes with: theta = 0.384 +- 0.003 (refereed); the KKT criterion (a)+(e) proved for the tangent problem; the reduction of
  (e) to the model cone is hypothesis H3 (exclusion of non-vector-field generators); (a) numerically in the limit; (e) numerically on the
  model cone (not proved: there (e) is equivalent to E(zeta_0) >= 0, given the proved E(zeta_inf) >= 0, and it is vacuous at zeta_0 by F2 T5; correction C3 below); kappa_opt = 1 - theta = 0.616 +- 0.003 numerically under H1-H3; unconditional bracket E_rec in [dual form,
  0.616 f2 z^2 (1+o(1))]. KB commit 12a64a6 (22:00) + follow-up sync.
- KB card referees: REF-opus-cft-2026-09-15 (F1 cards: kkt-noise-sign-criterion passed; tangent-problem-exact-parametrisation and
  theta-modular-wiener-hopf FAILED on locators/superseded numerics — under repair); REF-P5-KB1 on the F2/F3 cards: running.

## Propagation (2026-09-15)

Editor P5-EDIT propagated the refereed F3 result (card `theta-value`, passed REF-P5-KB1;
`numerics/optimality_all/F3_RESULTS.md`): **theta = 0.384 +- 0.003**, hence **1 - theta = 0.616 +- 0.003**;
geometry independent, measured order h^0.77, two independent discretisations (modular Galerkin;
parameter-free modular Wiener-Hopf, `rigor/exact_optimum_tangent_problem.tex` Prop 6.2) agreeing to 3e-4
after extrapolation.  S10's `theta = 0.300 +- 0.005` (`rigor/sdp_dual_certificate.tex` Sec. 7) is a
**taper-suppressed lower bound** and stays as the historical record (erratum: `rigor/errata_log.md`).
`kappa_opt = 1 - theta` is NOT claimed as settled: the KKT endpoint condition is still under evaluation
(Phase 5, F1/F2).  Nothing renumbered; every touched .tex recompiles with `pdflatex -halt-on-error`.

### Documents

| file | lines | old -> new |
|---|---|---|
| `rigor/optimality_all_channels.tex` | 468-475 (new) | sentence added after the S10 paragraph: 0.300 +- 0.005 superseded by F3, taper-suppressed lower bound; S10 table kept |
| | 482 | `theta > 0 (numerical, 0.30)` -> `(numerical, 0.384 +- 0.003; F3)` |
| | 485 | bracket `[D_z, 0.71 f2 z^2]` -> `[D_z, 0.616 f2 z^2]` |
| | 583-584 | `at least 0.30 and plausibly 0.34-0.40` -> kept, plus `the Phase 5 reconciliation gives 0.384 +- 0.003 (F3)` |
| | 678-681 | Verdict: `theta = 0.300 +- 0.005` -> lower bound + reconciled `0.384 +- 0.003`; `<= 0.71 f2 z^2` -> `<= 0.616 f2 z^2` |
| | 690, 701 | `D_z <= 0.71 f2 z^2` -> `D_z <= 0.616 f2 z^2` (twice) |
| `rigor/exact_fidelity_upper_half.tex` | 33 | abstract: `theta_fr >= 0.30` -> `theta_fr >= 0.38 (Phase 5, F3: theta = 0.384 +- 0.003)` |
| | 823-852 (Rem. `rem:thetafr`) | title `to 0.30` -> `to 0.38`; `theta = 0.300 +- 0.005` -> `0.384 +- 0.003`; `E_rec <= 0.71 f2 z^2` -> `<= 0.616 f2 z^2`; item (iii) rewritten to the reconciled two-frame statement (Galerkin + Wiener-Hopf, S10 a taper-suppressed lower bound); `kappa_opt <= 0.71` -> `<= 0.616 +- 0.003`; the `0.34-0.40` sentence replaced by the Phase-5 clause on non-isometric channels |
| | 949-958 | Verdict gap: `theta = 0.300 +- 0.005 in two independent discretisations` -> reconciled statement, E2's 0.708-0.711 labelled as the tapered circle-model value; `theta_fr >= 0.30` -> `>= 0.38`; `kappa_opt <= 0.71` -> `<= 0.616 +- 0.003` |
| | 1000-1005 (R1) | `kappa_opt <= 0.71 moved to Rem. 7.4` -> `kappa_opt <= 1 - theta_fr (then 0.71, now 0.616 +- 0.003; see the addendum)`; `both discretisations behind theta ~ 0.30` -> `the discretisations behind the numerical theta` |
| | 1067 | `theta_fr >= 0.30` -> `theta_fr >= 0.38 (theta = 0.384 +- 0.003, F3)` |
| | 1070-1087 (new) | dated addendum at the end of Sec. 10, `Addendum (2026-09-15): the value of theta` -- records the reconciliation, the taper mechanism, the log-L vs 1/L extrapolation error, and that nothing proved changes |
| `paper1/sec_outlook.tex` | 78-82 | `theta >= 0.30 numerically \cite{RigorS10}` -> `theta = 0.384 +- 0.003 numerically \cite{RigorS10,RigorF3}`; bracket upper end -> `0.616 f2 z^2` |
| | 102 | `theta >= 0.30 in two independent discretisations, the spectral circle model (RigorS10, RigorE2) and the modular Galerkin frame (RigorAll)` -> `theta = 0.384 +- 0.003` from Galerkin (RigorAll) + modular Wiener-Hopf (RigorF3), agreeing to 3e-4, the circle model's value a taper-suppressed lower bound; `theta_fr >= 0.30` -> `>= 0.38`; `0.71 f2 z^2` -> `0.616 f2 z^2` |
| `paper1/main.tex` | 122 | new `\bibitem{RigorF3}` after `RigorE2` (F3, theta reconciliation, `numerics/optimality_all/F3_RESULTS.md`, 2026-09-15) |
| `fidelity_recovered_quasifree.tex` | 423 | remark `Optimality beyond the rotated family`: `theta >= 0.30` -> `theta = 0.384 +- 0.003` (S10's value flagged as a taper-suppressed lower bound), `theta_fr >= 0.30` -> `>= 0.38`, bound `<= 0.616 f2 z^2` added |
| `numerics/optimality_all/F2_RESULTS.md` | T2 cap table | `lam_min(M_*)` and `rank-1 gain` rows labelled `half-SLD conv.` with a one-line note: they are 1/2 resp. 1/4 of `f2_capscan.py`'s output (script at L=128, cap 1e10: `-3.4771e-02`, `3.534e-11`, `f2_capscan_L128.out`) |

Compiles: `optimality_all_channels.pdf` 14 pp; `exact_fidelity_upper_half.pdf` 21 pp;
`paper1/main.pdf` 28 pp (pdflatex twice, unchanged); `fidelity_recovered_quasifree.pdf` 15 pp.
Untouched by instruction: `rigor/exact_optimum_tangent_problem.tex`, `rigor/referee_*.tex`,
`rigor/sdp_dual_certificate.tex`, all numerics scripts.

### KB cards (KB_ACTOR=P5-EDIT; no existing referee note edited, each card carries a dated note)

| card | old -> new |
|---|---|
| `cft_cmi:compression-not-second-order-minimiser` | `theta = 0.300(5)` (S10) and `0.29 -> 0.34` (Galerkin) -> `theta = 0.384 +- 0.003`, S10 read as a taper-suppressed lower bound, Galerkin extrapolating to the same value; `min_F g_Q <= 0.71 f2 z^2` -> `<= (0.616 +- 0.003) f2 z^2`; `related` += `theta-value` |
| `cft_cmi:compression-not-optimal-exact-fidelity` | `theta_fr >= 0.30` -> `>= 0.38`; `kappa_opt <= 0.71` -> `<= 0.616 +- 0.003`; item (iii) rewritten; `next` added: Phase-5 endpoint condition pending, `kappa_opt = 1 - theta` not to be recorded as settled |
| `cft_cmi:exact-fidelity-optimality-open` | `theta_fr >= 0.30 ... kappa_opt <= 0.71` -> `theta_fr >= 0.38 ... kappa_opt <= 0.616 +- 0.003`; `next`: bracket `[D_z, 0.71 f2 z^2]` -> `[D_z, (0.616 +- 0.003) f2 z^2]` + endpoint condition pending |
| `cft_cmi:paper1-status` | outlook description updated (`theta >= 0.30` -> `0.384 +- 0.003`, bracket `0.71` -> `0.616`, `theta_fr >= 0.38`, RigorF3 bibitem, 28 pp unchanged) |
| `cft_cmi:theta-value` | REF-P5-KB1 minor: `19 further candidates are EXCLUDED` -> `16` |
| `cft_cmi:kkt-noise-criterion-numerics` | REF-P5-KB1 minors: cap-scan row labelled half-SLD convention (1/2 of the script's `lam_min`, 1/4 of its gain) and anchored to `f2_capscan_L128.out` (`-3.4771e-02`, `3.534e-11` at L=128, cap 1e10; added to `evidence`); `kappa_max = 5.4-7.7, max w = 1.1e2-1.1e3` restricted to h = 0.24-0.06 (h = 0.03: 8.84, 3.4e3); `FD to 4e-9` -> `FD to <= 3e-8` |
| `cft_cmi:tangent-sdp-noise-directions` | REF-P5-KB1 minor: `homogeneity x4` stated for the ORBIT-ONLY optimum |
| `common:taper-dependence-of-first-order-constants` | REF-P5-KB1 minor: `||u||^2 stable to four digits` restricted to the taper windows S10's gate accepted (untapered `||u||^2 = 0.014889`) |

Not changed, deliberately: `open-problems-plan-note8` and the `e2-*` cards -- their Statements quote no
`0.30`/`0.71` as a current value (the `e2-*` ratios 0.708-0.711 are within-model measurements of the
circle model's own `1 - theta`, and the `0.30` hits are the taper parameter `uv = (0.30,0.42)`).

## Corrections of 2026-09-24

Each changed line was replaced by exactly one line, so the line numbers are those of the version of 2026-09-23.
"Tex Cn" refers to the corrections section of rigor/exact_optimum_tangent_problem.tex (Sec. 8).

- C1 (lines 87, 113, 124; knowledge-base card kkt-noise-sign-criterion). Said: "E(zeta_inf) = 2 lambda (1-theta)
  g_Q(deltadot) > 0 is PROVED" (87), "the proved E(zeta_inf) > 0" (113), "via the proved E(zeta_inf) = 2 lambda (1 - theta)
  g_Q > 0" (124). Says now: E(zeta_inf) >= 0 is proved; > 0 iff theta < 1, which is not proved. Why: step <1>4 of the tex's
  Prop 4.10(4) gives only the identity E(zeta_inf) = 2 lambda g_Q(delta_*) = 2 lambda (1-theta) g_Q(deltadot) >= 0, and the
  tex records theta < 1 as not proved (Rem 6.3(i); verdict box after Rem 6.4); numerically 1 - theta = 0.616 +- 0.003. The
  arguments that use this term (the model-cone reduction, (e) under H3) need only >= 0. Tex C2.
- C2 (line 126; knowledge-base card tangent-problem-exact-parametrisation). Said: "G = zeta* - sigma". Says now:
  G = sigma - zeta*. Why: the tex's eq. (13) continues G = -(1/2)(zeta* - zeta**) = sigma - zeta*, and the tex uses
  zeta* = -G + sigma (line 506, Thm 3.11 step <1>2); with the other sign the absorption identity of Thm 3.11(2) and the
  inclusion (3) are false. Tex C1.
- C3 (lines 129-130; knowledge-base cards kkt-noise-sign-criterion and all-channel-optimum-value). Said: "(e) proved on the
  model cone". Says now: (e) holds numerically on the model cone, not proved. Why: on the model cone (e) is equivalent to
  E(zeta_0) >= 0 (tex Prop 4.10(5)), which is not proved; kkt-noise-sign-criterion lists "E(zeta_0) > 0 on the model cone"
  as numerical, all-channel-optimum-value lists an analytic proof of (e) as open; F2 T5 finds A(zeta_0,0,0) outside the form
  domain, so (e) is vacuous at zeta_0 rather than satisfied with a margin. Tex C3.
- C4 (line 122; knowledge-base card kkt-noise-sign-criterion). Said: "since A(zeta_0,0,0) is not in F, alpha = 0 is forced".
  Says now: that A(zeta_0,0,0) is not in F is marked as numerical, not proved. Why: the card states that "A(zeta_0,0,0) is
  not in F ... rests on F2's divergent corner term (rem:T5 (ii)), i.e. it is numerical". Repeat of tex C4.

Superseded log entries (C5-C11). These dated entries are not rewritten; each carries the inline marker
"[superseded 2026-09-24: see Cn]", and the current statement is given here.

- C5 (line 19, F1 entry of 2026-09-15; card tangent-problem-exact-parametrisation). Entry: "Boundary-moving (non-surjective)
  isometry families are not a new stratum (Thm 3.11)". Current: Thm 3.11(3) gives only an INCLUSION of cones; the
  boundary-moving isometry generators form a genuine one-sided cone, which is why the criterion needs condition (e)
  (tex Thm 3.11(3), Rem 4.8; the right-hand side must not be enlarged to all anti-symmetric G).
- C6 (lines 20-21, same entry; card kkt-noise-sign-criterion). Entry: "the orbit optimum is the global tangent optimum iff
  M_* >= 0 and M_* >= tau_*". Current: (a) M_* >= 0 and M_* - tau_* >= 0 is necessary but not sufficient; the orbit point
  is a global minimiser of the tangent programme iff (a) AND the endpoint condition (e) hold (tex Thm 4.4(d)).
- C7 (lines 55-56, F2 FINAL T4 entry; card kkt-noise-criterion-numerics). Entry: "VERDICT (numerical): M_* >= 0 and
  M_* - tau_* >= 0 hold for the exact problem; the isometric orbit is the global optimum of the tangent problem, optimal
  N_1 = Y_1 = 0". Current: every finite run FAILS (a) (CRITERION False); the violation extrapolates to 0^-
  (lambda_min/||M_*|| ~ h^1.15 and ~ 1/Ymax, rank-one gain ~ h^1.85/Ymax^2), so (a) holds only as an extrapolation.
  The numerics are consistent with the isometric orbit carrying the tangent optimum and kappa_opt = 1 - theta, but they
  do NOT establish that the optimal N_1, Y_1 vanish: Thm 4.4(d) delivers a global minimiser, not uniqueness.
- C8 (line 64, F2 FINAL T5 entry; cards kkt-noise-criterion-numerics and kkt-noise-sign-criterion). Entry: "VERDICT
  (numerical): (e) holds with a large margin". Current: the corner row (1/2) M_*(0,0)/h = +10.3, +16.1, +24.7, +37.2
  (~ h^-0.60) represents the continuum E(zeta_0) and diverges, so A(zeta_0,0,0) is (numerically) not in F and (e) is
  VACUOUS at zeta_0 rather than satisfied with a margin; E(zeta_inf) >= 0 is proved (> 0 numerically, theta_h < 1); (e)
  holds numerically on the model cone, and beyond it only under H3.
- C9 (lines 83 and 87, F1 entry of 17:30; card kkt-noise-sign-criterion). Entry: "E(zeta) := 2 b(delta_*, A(zeta,0,0)) =
  -2 b(delta_*,[Q,zeta])" and "E(zeta_0) = 2 b(delta_*, [Q, E_D d/dy E_D])". Current: E is evaluated on the blocks of
  A(zeta,0,0) only; the commutator form is valid only for bounded anti-self-adjoint zeta and deletes exactly the boundary
  term (tex Prop 4.10(2')), as the 21:04 entry of this log (line 90) already records.
- C10 (lines 85 and 87, same entry; card kkt-noise-sign-criterion). Entry: "modulo the linear class the cone is generated
  by zeta_0 ... and zeta_inf" and "so (e) reduces to the single number E(zeta_0)". Current: modulo the closure of L,
  zeta_0 and zeta_inf generate the VECTOR-FIELD subcone only (tex Prop 4.10(3)); on the model cone (e) is equivalent to
  E(zeta_0) >= 0 (Prop 4.10(5)); the whole admissible cone is Hypothesis H3 (as the REF-P5-3 entry, lines 94-97, records).
- C11 (line 97, REF-P5-3 entry; card kkt-noise-sign-criterion). Entry: "condition (e) is reduced to E(zeta_0) >= 0 only
  under a hypothesis H3". Current: on the model cone (e) is equivalent to E(zeta_0) >= 0 without H3; H3 is what extends
  (e) beyond the model cone, and under H3 read in F, given A(zeta_0,0,0) not in F (numerical), (e) holds outright and the
  junction inequality is not invoked (tex Rem 4.13, Rem 4.13(1); tex C3).
- C12 (line 62, F2 FINAL T5 entry; card kkt-noise-criterion-numerics). Said: "A-block (absorption) form = boundary form to
  2e-10..2e-8". Says now: "2e-10..7.5e-8". Why: numerics/optimality_all/f2_t5_endpoint.out prints the relative deviations
  2.0e-10, 5.4e-9, 1.8e-8, 7.5e-8 at h = 0.24, 0.12, 0.06, 0.03 (lines 7, 17, 27, 37) for the admissible scheme; the card
  records "holds to <= 7.5e-8". A transcription of the output, corrected in place (not a superseded statement). Repeat of
  tex C7.
- C13 (line 51, F2 FINAL T4 entry; card kkt-noise-criterion-numerics). Said: "all F1 identities hold to 1e-9". Says now:
  "the F1 identities hold to <= 3.5e-7 (SLD identity 1e-10, FD derivative formula <= 3e-8, AntiHerm((t_*Q)_DD)/||M_*|| =
  2.8e-9 ... 3.5e-7)". Why: numerics/optimality_all/f2_t4_h024.out l.4-5, f2_t4_hladder.out l.4-5 and l.12-13, and
  f2_t4_h003.out l.4-5 print AntiHerm/||M_*|| = 2.762e-9, 8.500e-8, 1.520e-7, 3.499e-7 and FD rel = 3.94e-10, 1.08e-8,
  7.56e-9, 2.63e-8 at h = 0.24, 0.12, 0.06, 0.03; the SLD identity prints 1.0000000000 (f2_t4_h024.out l.1,
  f2_t4_hladder.out l.1 and l.9, f2_t4_h003.out l.1). A copied number, corrected in place.
- C14 (line 24, F1 entry of 2026-09-15; card tangent-problem-exact-parametrisation). Entry: "H2 (minimisers within O(s) of
  the compression)". Current: H2 (tex Def 3.16) says that for small s a minimiser EXISTS and is of the scaled-family form
  for a first-order datum with ||N_1|| + ||Y_1|| <= C and a remainder g_Q(delta(s) - s delta^(1)) = o(s^2) uniformly -
  i.e. H2 is the lower bound in disguise; it is not proved: the coercivity g_Q >= (1/4)||.||_2^2 (Prop 3.14) gives O(s)
  defect blocks but does not localise (X,Z), because Q_AB has 0 in its essential spectrum (Rem 3.15).
- C15 (line 54, F2 FINAL T4 entry; card kkt-noise-criterion-numerics). Said: "the violation is exactly ~ 1/Ymax" and "the
  violating vector sits at y ~ 0.5 Ymax". Says now: "~1/Ymax" and "y ~ (0.37-0.6) Ymax". Why: the card records
  lam_min/||M_*|| * Ymax = -0.0181 ... -0.0191 (a slow drift, not exactly 1/Ymax) and the violating mode at
  y ~ (0.37-0.6) Ymax (0.37 Ymax at Ymax = 30, f2_t4_ymax12.out). Copied values, corrected in place.
- C16 (line 85, F1 entry of 17:30; card kkt-noise-sign-criterion). Entry: "a pure boundary functional E = (1/2) Tr((-2
  sigma_zeta) M_*)". Current: E(zeta) = (1/2) Tr((-2 sigma_zeta) M_*) holds whenever -2 sigma_zeta lies in the form domain
  of M_* (tex eq. (28), Prop 4.10(2)); at zeta_0 it does not (-2 sigma_{zeta_0} = delta_0 (x) delta_0, Prop 4.10(5)). The
  card: "equal to (1/2)Tr((-2 sigma_zeta) M_*) whenever -2 sigma_zeta lies in the form domain of M_*".
- C17 (line 9). Said: "27 pp". Says now: "31 pp after the corrections of 2026-09-24 (27 pp before)". Why: the tex compiles
  to 31 pages after its corrections section (tex C1-C10). A copied number, corrected in place.
