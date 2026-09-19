# Phase 5 brief — the exact value of the all-channel optimum (2026-09-15)

## What is known (kb -p cft_cmi q --area optimality)
- Second-order problem over ALL channels = quasi-free convex programme  min_F g_Q(Q - Q_rec(X,Z)),
  F = {X: h_B -> h_D, Z = Z* on h_D : X Q_BB X* <= Z <= 1 - X(1-Q_BB)X*}, Q_rec = [[Q_AA, Q_AB X*],[X Q_BA, Z]]
  (S8 rigor/optimality_second_order.tex Thm 3.1; all channels: rigor/optimality_all_channels.tex Thm 3.5, 4.1).
  g_Q(delta) = (1/8) sup_t (Tr t delta)^2 / V(t), V(t) = Tr(t Q t (1-Q)) = ||P^perp t P||_2^2 (Legendre form).
- Isometric orbit (Y = 0, X X* = 1, V* = W unitary L^2(D) -> L^2(B)): value (1 - theta) f2 z^2 with theta = sup_G cos^2(u, v_G)
  over anti-self-adjoint G supported in D (S10 Lemma 6.1, Thm 6.2); exact fidelity follows (E1 Thms 7.1, 7.3).
- Sandwich (E1 Cor 7.5): min_F g_Q  <=  E_rec^(2)  <=  inf_isom g_Q = (1 - theta_fr) f2 z^2.  So the exact all-channel value is
  min_F g_Q at leading order in z, and the gap to the isometric orbit is the contribution of NON-ISOMETRIC data.
- theta: spectral circle model 0.300 +- 0.005 (S10; E2 confirms 0.289-0.292 raw at L = 256-384), modular Galerkin frame
  0.286 -> 0.336 for h = 0.4 -> 0.15 and still rising (rigor/optimality_all_channels.tex Sec. 5.2). The two do NOT agree.
  "Exact value" is meaningless while theta is uncertain by 10%.

## The tangent problem (leading order in s ~ z)
Polar decomposition of a feasible X: X X* <= 1 - Y <= 1, so X X* = 1 - N with N >= 0 and Y <= N, and X = (1 - N)^{1/2} V with
V: h_B -> h_D a co-isometry (V* : h_D -> h_B an isometry, not necessarily onto). Write N = s N_1, Y = s Y_1 (0 <= Y_1 <= N_1), and
V* = W U with W the compression unitary and U: h_D -> h_D an isometry (onto <=> V* onto). First-order data therefore consist of
  (i) the isometry direction: U = 1 + s Zeta + o(s) with Zeta the generator of an isometric (contractive-semigroup) family on
      L^2(D): interior rotations Zeta = G anti-self-adjoint on L^2(D) (the isometric orbit) AND boundary-moving generators
      (e.g. further compression onto a subinterval, Zeta = (mu - 1) D_chi|_D with mu >= 1, dissipative at the endpoint L);
  (ii) N_1 >= 0 on h_D (loss of isometry), (iii) 0 <= Y_1 <= N_1 (noise).
Then, to first order,
  Q_rec_DA = (1 - s N_1/2) V Q_BA,   Z = V Q_BB V* - (s/2){N_1, V Q_BB V*} + s Y_1,
so delta = delta_isom(Zeta) + s * L(N_1, Y_1) with L linear, and the tangent problem is
  E^(2) = min over (Zeta admissible, N_1 >= 0, 0 <= Y_1 <= N_1) of g_Q(first-order defect)   — a convex programme with two
  semidefinite cone constraints (an SDP in the one-particle space). Its value is kappa_opt f2 z^2; the isometric restriction gives
  kappa = 1 - theta.
Questions: (Q1) Is the minimiser noise-free (N_1 = Y_1 = 0) and surjective (mu = 1)? Then kappa_opt = 1 - theta EXACTLY.
(Q2) If not, what is kappa_opt? (Q3) What is theta (reconcile the discretisations; closed form?).

## KKT criterion for (Q1) (to derive and check)
At the isometric optimum (X_*, Z_*) with optimal SLD t_* = SLD of the optimal defect, the tangent problem is convex, so the
isometric optimum is the GLOBAL optimum iff the directional derivative of g_Q along every admissible non-isometric direction is
>= 0:  Tr( t_* L(N_1, Y_1) ) >= 0 for all N_1 >= 0, 0 <= Y_1 <= N_1 (and along boundary-moving Zeta with mu >= 1). Since L is
linear, this is a SIGN condition on explicit compressions of t_*: e.g. the coefficient of Y_1 is the DD block of t_* (Y_1 enters
Z with + sign, delta with -), the coefficient of N_1 involves (1/2)(t_* Q_rec + Q_rec t_*)_DD-type terms and the DA block. If the
sign conditions hold, (Q1) is proved by weak duality (no constraint qualification needed, as in S10 Thm 3.2); if they fail, the
violating direction is an explicit better channel.

## Tracks
F1 (analytic, Opus): rigor/exact_optimum_tangent_problem.tex — (1) prove the polar/first-order parametrisation and that the tangent
   problem is the leading-order value (interchange of min and z -> 0 must be justified or stated as the definition of E^(2));
   (2) derive the KKT sign conditions for (Q1) precisely (all blocks, both signs, including the boundary-moving direction);
   (3) attempt a closed form for theta: theta = <R_a, A^{-1} R_a>/||u||^2 (S10 Thm 6.2) with everything explicit in the modular
   frame of I; test candidates against the numerics (3/pi^2 = 0.3040, 1/3, 1 - 2/3 ... only if the numerics converge).
F2 (numerical, Opus): numerics/optimality_all/f2_*.py — pose the tangent SDP in the spectral circle model (E2's e2_common.py:
   exact P, Riesz map, weights; cvxpy + Clarabel/SCS): variables G (anti-Hermitian on D), mu or a general dissipative boundary
   generator, N_1 >= 0, Y_1 with 0 <= Y_1 <= N_1; objective the SLD form of the first-order defect (use the EXACT weights: the
   circle model resolves the visible functional); report kappa_opt vs 1 - theta at L = 96..256 and the optimal N_1, Y_1 norms; then
   evaluate the KKT sign conditions numerically at the isometric optimum (eigenvalues of the relevant blocks of t_*).
F3 (numerical, Opus): theta reconciliation — compute theta in the modular Galerkin frame (kkt_continuum.py machinery) with the
   FULL rotation class and Richardson extrapolation in h, and in the spectral model without/with different tapers, at matched
   physics; identify which model under-resolves; produce theta to 3 digits with an error bar or explain why the two limits differ
   (hint: the Galerkin frame of I cannot represent a Moebius squeeze exactly — S11 Sec. 3 — but theta is a first-order quantity;
   the spectral taper removes the UV where G_* lives — S10 Sec. 10 Remark). Test closed-form candidates only against the
   reconciled value.
Rules: KB cards for every result (kb -p cft_cmi add ..., KB_ACTOR=F1/F2/F3, tag phase5); Opus referees afterwards (never Fable);
small appends; compile after each append; never run git; think only to the next tool call.

## Environment
Python with numpy/scipy/mpmath/cvxpy(+CLARABEL, SCS): $V/bin/python with
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team/2a3c5aab-2bd9-408c-811f-f4144c2149e4/scratchpad/venv
If it is gone (session restart): python3 -m venv $V && $V/bin/pip install numpy scipy mpmath cvxpy clarabel scs.
Long jobs: nohup $V/bin/python script.py > script.out 2>&1 < /dev/null & disown ; outputs stay in numerics/optimality_all/.
