# Phase 2b brief (2026-09-09): Kubo-Mori gauge lemma, rate, certified numerics, paper 2

## Track RK: Kubo-Mori second variation for the recovery curve (s_2 = c/12 for general nets)
Setting: M = A(I), I = (-a, L) (or the normal form a = infinity of universality_theorem_B.tex), recovered state omega_s = omega o Ad U_s|_M,
U_s = exp(isT(g_tot)) implements the C^{1,1} circle map k~_s (identity on A and left of -a). Facts: U_s is NOT in M and NOT in M'; but
k~_s = id on the arc (-a, 0) subset A, hence U_s in A(K) for every interval K containing the support of k~_s - id, e.g. K_delta = S^1 \ (-a, -a+delta),
0 < delta < a (locality of implementers, implementation_C11.tex Lemma 4.4). Also U_s commutes with A(A) = A((-a,0)).
Known (kubo_mori_second_variation.tex, QK): for u in U(N) and Omega cyclic separating for N,
   D_N(omega_{uOmega} || omega_Omega) = || h(Delta_N)^{1/2} (u - 1) Omega ||^2,  h(lambda) = lambda - 1 - log lambda,
with liminf s^-2 D >= g_KM/2 unconditionally and D = (s^2/2) g_KM + o(s^2) under modular analyticity (U_eps).
UPPER bound route (new): monotonicity of relative entropy under restriction, D_M(omega_s|_M || omega|_M) <= D_{A(K_delta)}(omega_{Psi_s} || omega_Omega)
with Psi_s = U_s^* Omega a vector representative of omega_s on M and U_s^* in A(K_delta): the right side is QK's exact expression for the big
interval algebra, whose modular operator Delta_{K_delta} is geometric (BW dilation of K_delta). Hence
   limsup s^-2 D_M <= (1/2) g_KM^{(K_delta)}(T(g_tot)Omega) = int (lambda - 1) log lambda d mu_{K_delta}(T(g_tot)Omega)   (under (U_eps) for A(K_delta)),
for every delta and every extension h of the field beyond L (the extension changes U_s but not omega_s|_M). The gauge lemma to prove:
   inf_{delta, h} g_KM^{(K_delta)}(T(g_tot + h)Omega) = g_KM^{(M)}(phi) := the Kubo-Mori form of the tangent functional phi on M,
and that this equals c/6 (Note 7: g_KM = c/6, s_2 = g_KM/2 = c/12). Expect the same mechanism as for Bures: the T-subspace H_T reduces the modular data
of every interval algebra, the KM form on H_T is c times a universal form, and the free fermion fixes the constant (Note 7 Thm 5.2: int dk/(k^2+1) = pi).
LOWER bound route: martingale/monotone approximation D_M >= D_{M_n} for finite-dimensional M_n increasing to M (Araki 1977 Thm 3.9; local algebras of
conformal nets are hyperfinite), finite-dimensional expansion D_{M_n} = (s^2/2) g_KM^{(n)} + o(s^2), and monotone convergence g_KM^{(n)} -> g_KM^{(M)}
(analogue of the Bures monotone-convergence proposition in lemma_second_variation.tex). Alternatively adapt QK's lower-semicontinuity argument.
Free-fermion check: everything is computable in the modular eigenbasis (numerics/, kernel_identity.tex), g_KM = 1/6 exactly (QK's reduction).

## Track RR: the rate of the remainder — reformulate
Numerics (Note 5 Table 3, corrected basis): Phi/zeta^2 = 0.008376 (zeta = 1/120), 0.008308 (1/60), 0.008175 (1/30): deficit relative to f_2 = 0.0084434 is
0.80%, 1.60%, 3.2% -- LINEAR in zeta: Phi = f_2 zeta^2 (1 - 0.96 zeta + ...). The Uhlmann-Bogoliubov bound with the optimal geometric extension exceeds
Phi by +0.22%, +0.45%, +1.3%, +4.1% at zeta = 1/120, 1/60, 1/30, 1/15 (p1_bogoliubov.out): also linear, bound = Phi (1 + 0.27 zeta + ...), i.e. the bound
is f_2 zeta^2 (1 - 0.69 zeta + ...). So the log^-2 law of Note 5 Cor 4.2 is NOT what the data show; the natural conjecture is
   Phi(zeta) = f_2 zeta^2 (1 + c_3 zeta + O(zeta^2)),  c_3 ~ -0.96  (free fermion, per component).
Tasks: (a) UPPER bound with rate: make step 4 of uhlmann_upper_bound.tex quantitative: ||V_zeta||_2^2 = zeta^2 ||P_- K P_+||_2^2 + O(zeta^3) with an explicit
constant (from the exact identity G_s = int_0^s W~_sigma^* G^(1) W~_sigma d sigma and Lipschitz continuity of sigma -> W~_sigma^* G^(1) W~_sigma in
Hilbert-Schmidt norm), giving Phi <= f_2 zeta^2 (1 + C zeta); compute the exact next coefficient of the optimal-extension bound (expect -0.69).
(b) THIRD-order coefficient of Phi itself: from the quasi-free fidelity formula (Note 5 Thm 3.2) expanded to third order in the defect D = zeta D^(1) + zeta^2 D^(2) + ...
(exact kernel from check_note5_theory.tex; D^(2) needed), evaluate c_3 numerically to 3 digits and, if possible, in closed form.
(c) LOWER bound with rate: P2's route (quadratic_limit.tex) with an explicit cubic constant for the compressed curve (Problem 7.2): |Phi_P - zeta^2 g_B^(P)/8| <= C(Lambda) zeta^3;
with the cutoff error 0.513 r/Lambda^2 this gives Phi >= f_2 zeta^2 (1 - 0.513/(f_2 8 Lambda^2) - C(Lambda) zeta / f_2); optimise Lambda(zeta). Report the best proved
lower rate (log^-2 if C(Lambda) ~ e^{Lambda}, better if C(Lambda) grows polynomially — check numerically how the cubic coefficient of Phi_P grows with Lambda).
Deliverable: rigor/rate_of_remainder.tex; correct Note 5 Cor 4.2's rate statement accordingly (report what to write).

## Track RC: tight certified numerics
Open items from tail_bound.tex (PT): (i) a bound on || sqrt(Q~) - sqrt(X_11 (+) X_22) ||_2 quadratic in the off-diagonal block X_12, which would upgrade the
tail decay from 1/kappa_c to 1/kappa_c^2 and shrink the certified brackets from ~80% to ~1%; (ii) an interval-arithmetic audit of Dhat and Q_N (the 3%
arithmetic margin). Also PZ's blocker: arb acb_mat.eig returns nan for spectral range > 1e-20 (kappa_max > 45); find a workaround (e.g. eigen-decomposition
of Q via its known structure: Q_box is a compression of a projection, or use mpmath eigsy at higher dps only for the window block, or flint's real symmetric
eig on the Hermitian part). Deliverable: rigor/certified_numerics.tex (+ scripts), certified Phi(zeta) brackets at the 1% level for Table 3 of Note 5 if the
quadratic bound is proved; otherwise the best rigorous brackets plus a clear statement of what is missing.

## Track RW: paper 2 draft (paper2/main.tex skeleton): sections from universality_theorem_B.tex, implementation_C11.tex, lemma_second_variation.tex,
kubo_mori_second_variation.tex (conditional s_2), numerics/boson, with the referee reports' corrections included; placeholder citations for internal documents.

## Results so far (2026-09-09)
- RW: paper2/main.pdf 24 pp draft.
- RR (rigor/rate_of_remainder.tex, 15 pp; under referee RRr): with the FLOW extension (W~_s a one-parameter group), ||V_s||_2^2 <= s^2 ||P_- D P_+||_2^2 exactly,
  hence the global bound Phi <= -(1/2) log(1 - 2 f_2 zeta^2) = f_2 zeta^2 (1 + f_2 zeta^2 + ...), even in s (no cubic term) => c_3 <= 0 and the log^-2 remainder
  of Note 5 Cor 4.2 is refuted. Third-order formula for -log Fid of quasi-free states derived; c_3 = -0.99(1), c_4 = +0.9(1). Lower rate: the cubic constant
  of the compressed curve is bounded (C(kappa_c) -> 0.00838 = |c_3| f_2), so the best lower rate is linear, conditional on a uniform Problem 7.2. The -0.69 of
  the brief was a property of PN's non-group family. GAP: f_2^star = f_2 over flow extensions is numerical (<= 1.00036 f_2).
- RC (rigor/certified_numerics.tex, 10 pp; under referee RCr): unweighted quadratic bound FALSE (2x2 counterexample); weighted Sylvester identity + Schur
  positivity gives weighted norm <= tau; cross term removed (block-diagonal optimal Uhlmann unitary for the pinched pair, operator Jensen); 0 <= Phi - Phi_W
  <= Phi_22 - log|det(1+T)|, computable; certified enclosure widths 0.64-1.19% (box value, kappa_c = 25.3), 1.7-2.4% with the box-cutoff term; Q_N enclosed to
  5.6e-18/entry by ball arithmetic; trapezoid Q_box accurate only to 4.7e-11; arb eig bypassed (Gershgorin + Sylvester). Remaining: rigorous 2-D quadrature for
  Dhat, box cutoff beyond kappa_max (dominant), constant c_0 ~ 18-42 in the a priori form.

## Track RK result (rigor/kubo_mori_gauge_lemma.tex, 18 pp, 2026-09-09): GAUGE LEMMA REFUTED
Proved: admissible gauges (K = (-inf,R) superset I, g^ = g_tot on I, 0 on K') give U^_s in A(K); exact unconditional bound D_M <= ||h(Delta_K)^{1/2}(U^_{-s}-1)Omega||^2;
spectral theorem: for T(f) affiliated with A(K) the KM form is the local Sobolev expression (c/12) int (f~''^2 + f~'^2) d xi in the modular frame (c-linear, net-independent);
lower bound liminf s^-2 D >= G(M,phi)/2 >= g_B/2 = c/(3 pi^2) = 0.034c via Petz-Donald (used in the working direction).
REFUTED: inf over gauges of the big-interval KM form = (11+5 sqrt5) c/12 = 1.848c = 11.09 x c/6 (the fixed part -x^2 on D costs 2R^2 sinh(2 xi_1), divergent as R -> 1 and R -> inf).
Also: QK's (U_eps)/(A_eps) fail for every admissible gauge (compact frame support => polynomial decay); replacement hypothesis (V) (uniform integrability of log_-)
gives limsup s^-2 D <= 0.924c. Bracket: 0.034c <= liminf <= limsup <= 0.924c. Diagnosis: Note 7's c/6 is the analytic continuation of a divergent integral
(Phi_ren = 2 vs honest 22.18) because g_tot(L) != 0; any proof must renormalise (collar family) or use a fermion-type exact cancellation.
=> s_2 = c/12 for general nets remains CONJECTURAL (numerically confirmed for fermion and boson). Paper 2 states it conditionally (fine).

## Referee RCr (rigor/referee_certified_numerics.tex, 12 pp, 2026-09-09): BREAK — the Phi_off column of RC's Table 3 is float64 noise (control identity off by
1.0e-4 = 180x the quantity); the theory is right (identity verified in mpmath dps 60). Quotable as certified today: the Q_N ball enclosure (5.62e-18/entry) and
the a priori bracket Phi_W <= Phi <= 1.20 Phi_W (widths 17.8-19.9%). NOT quotable: the 0.64-1.19% / 1.7-2.4% widths until recomputed in high precision.
Also: Cor 2.6 GAP (commutation assumption, E- weight, uses 0 <= Q~ <= 1); Phi_W taken from the trapezoid results_hp2.txt; the "8%" margin claim wrong
(3.3/21.7/204% with PT's eta); Sec. 1 overclaims. RC asked to repair (high-precision Phi_off, corrections).

## Referee RRr (rigor/referee_rate_of_remainder.tex, 15 pp, 2026-09-09): RR's results STAND. (a) group = PA's own, generator identical, kink harmless; "for all s" -> s >= 0;
||V_s||_2^2 <= s^2||P_-KP_+||_2^2 holds for any one-parameter unitary group with [P_-,K] HS (Bochner); ||G_s||_2^2 = 2||V_s||_2^2 exact; evenness a theorem (CS).
Gap f_2* = f_2 CLOSABLE: U_s = e^{s(D+ih')}, h' in A', is a group whose Dyson cocycle stays in I' -> PA Prop 7.6 gives f_2* = f_2 exactly -> global bound and
c_3 <= 0 UNCONDITIONAL (referee's Prop 3.1). (b) third-order formula re-derived and verified; c_3 = -0.99(1), c_4 = +0.9(1) reproduced; Table 3 col A matched to 2e-6
for zeta <= 1/30. BREAK (write-up only): Prop 4.2's verdictbreak against Problem 7.2 mis-scoped (two-sided constant grows like e^{kappa_c}/(225 kappa_c^6); P2's e^Lambda
right); restate one-sidedly. Refutation of the log^-2 remainder STANDS. Corrections applied to N5 Cor 4.2, N7, paper 1 (rigor/apply_rate_corrected.py). RR asked to repair.
