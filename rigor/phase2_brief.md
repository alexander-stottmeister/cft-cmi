# Phase 2 brief (2026-09-08): universality (Theorem B) after the Phase 1 result

## What Phase 1 changed
The free-fermion theorem lim Phi/zeta^2 = c/(12 pi^2) was proved with an UPPER bound from Uhlmann's inequality applied to the
vector U(k~_s)^* Omega, where U(k~_s) implements an extension k~_s of the compression map k_s (identity on A, h_s(x) = Lx/(L+sx) on D)
to a C^{1,1} diffeomorphism of the circle (smooth extension beyond L, moving the point at infinity), and a LOWER bound via a
variational (Legendre/Alberti) inequality. Both halves have net-independent counterparts:

## Conditional Theorem B (target of track QA)
Hypotheses for a diffeomorphism covariant net (A, U, Omega) with central charge c on S^1, intervals A = (-a,0), D = (0,L), I = ABC:
 (H1) [implementation] for small s there are unitaries U_s with U_s A(J) U_s^* = A(k~_s(J)) for all intervals J (covariance under the
      C^{1,1} piecewise-Moebius map k~_s), U_s Omega =/= Omega in general; on A(I) the recovered state is omega_s := omega o Ad U_s|_{A(I)}
      (independent of the extension beyond L, since k~_s = k_s on I).
 (H2) [differentiability on the vacuum] U_s Omega = Omega + i s T(g_tot) Omega + o(s) in norm, with g_tot the first-order field of k~_s
      (= -x^2/L on D, 0 on A, smooth beyond L), T(g_tot) Omega in H.
 (H3) [first-order differentiability of the curve on a core] omega_s(X) = omega(X) + s phi(X) + o(s), phi(X) = i omega([T(g_tot), X]),
      for X in a *-strongly dense subalgebra of A(I) (e.g. smeared fields), and omega_s(X^2) -> omega(X^2).
 Standing facts: Haag duality A(I)' = A(I'); Bisognano-Wichmann (Delta, J geometric); Reeh-Schlieder.
Claims:
 (B-lower) -log F(omega, omega_s) >= (s^2/8) g_B + o(s^2), g_B := 4 dist(T(g_tot)Omega, closure A(I)'_sa Omega)^2, from Alberti's inequality
      F^2 <= omega(x) omega_s(x^{-1}) with x = 1 + sK (rigor/lemma_second_variation.tex, theorem "Upper bound" / "Three faces"); needs only (H3).
 (B-upper) -log F(omega, omega_s) <= -log |<Omega, U_s u' Omega>| for every unitary u' in A(I') (Uhlmann; u' = U(phi') with phi' a diffeo
      supported in I' realizes a different extension); expansion via (H2): = (s^2/2) ||T(g_tot + h) Omega||^2 + o(s^2); infimum over
      extensions h (real fields supported in I') equals g_B/4 because the T-subspace H_T = closure{T(f)Omega} is invariant under Delta^{it}, J,
      so the distance to closure A(I)'_sa Omega is attained in H_T, and the standard subspace of H_T for I' is closure{T(h)Omega: supp h in I'}
      (two standard subspaces with the same Tomita operator coincide; needs Reeh-Schlieder for T-vectors).
 (B-value) g_B = 2 c/(3 pi^2) (in the normalization of Note 7 with zeta): all ingredients (two-point function of T, geometric Delta and J)
      are linear in c; the x-space Mellin evaluation (rigor/collar_and_invariant_formula.tex) is legitimate for the smoothly extended field.
 => f_2 = c/(12 pi^2) for every net satisfying (H1)-(H3). The Kubo-Mori coefficient s_2 = c/12 additionally needs the KM second variation (O2).

## Track QB (O5): verify (H1)-(H3)
 - Free fermion: U_s = Gamma(W~_s) (done in rigor/uhlmann_upper_bound.tex).
 - Tensor products / integer c: Fock representations extend to D^s(S^1), s > 2 (CDIT, arXiv:1808.02384, outlook section; also for the
   fermion via Shale-Stinespring); k~_s is in C^{1,1} = W^{2,inf} subset H^{5/2 - eps}, so covered when the s>2 extension applies.
 - General c: CDIT's theorem covers D^s for s > 3 only; k~_s is not in H^3 (jump of the second derivative at the touching point).
   Routes: (a) energy bounds ||T(f)psi|| <= C ||f||_{3/2} ||(1+L_0)psi|| (Carpi-Weiner; CDIT Prop 2.2(4)) with ||f||_{3/2} = sum |f_n|(1+|n|^{3/2}),
   finite for piecewise smooth C^{1,1} f (CDIT Prop 2.3); essential self-adjointness of T(g_tot) on the finite-energy domain (Nelson commutator
   theorem needs a bound on [L_0, T(g_tot)] = -i T(g_tot'), where g_tot' has a kink: check what norm is needed); then U_s := exp(i s T(g_tot))
   and the covariance (H1) by the standard "flow" argument (differentiate U_s A(J) U_s^*). (b) strong limits of U(phi_n) for smooth phi_n -> k~_s
   with uniformly bounded energy (Route B of Note 6, corrected: compact sets need a norm bound).
 - Deliverable: exact statement of what class of nets satisfies (H1)-(H3), with proofs or precise gaps.

## Track QN (O6): bosonic check
 U(1) current net (chiral free boson, c = 1): Gaussian (quasi-free bosonic) states, symplectic one-particle space; geometric compression by
 the weight-1 push-forward of the current; recovered state Gaussian; fidelity/relative entropy of Gaussian states (symplectic eigenvalues).
 Compute f_2, s_2 numerically and compare with 1/(12 pi^2), 1/12. Also test c-linearity of the overlap: the bosonic vacuum overlap
 |<Omega, Gamma_b(S~_s) Omega>| for the same diffeomorphism k~_s should equal the fermionic det(1 - V^*V)^{1/2} (both c = 1).

## Track QK (O2): Kubo-Mori second variation in type III
 D(omega_s || omega) = (s^2/2) g_KM + o(s^2), g_KM = int (lambda - 1) log lambda d mu(lambda), for unitary orbits omega_s = omega o Ad e^{isA};
 route: lower bound from Araki's martingale/monotonicity (finite-dimensional expansions + g_KM^(n) up to g_KM), upper bound from the relative
 modular operator along the orbit (Delta_{u Omega, Omega} = u Delta u^* for u in M) and a Daleckii-Krein formula for log on unbounded Delta.

## Corrections after track QA (rigor/universality_theorem_B.tex, 2026-09-08)
- Theorem B (Thm 7.1 there) proved under (HD)+(BW)+(RS)+(H1)-(H3): -log F = (s^2/8) g_B + o(s^2), g_B = 4 dist(T(g_tot)Omega, cl A(I)'_sa Omega)^2
  = c gamma_0 with gamma_0 = 2/(3 pi^2) from the free fermion; universality and c-linearity are UNCONDITIONAL given (H1)-(H3), because
  H_T reduces Delta and J and the minimiser lies in H_T (Thm 5.5) -- the standard-subspace lemma is NOT needed for Theorem B, only for the
  variational (inf over T(h)) form; that lemma remains a GAP (one-particle Reeh-Schlieder / BW for T-vectors, BGL 1993 / Longo).
- The claim in this brief that the smooth extension legitimises the x-space Mellin evaluation is WRONG: the disjoint-strip obstruction is
  caused by g(L) != 0 and survives the extension; Note 7's spectral formula also uses Lemma 2.1(2) (hypothesis A in M fails). The value
  gamma_0 = 2/(3 pi^2) stands via c-linearity + the free-fermion theorem.
- (H2) for the free fermion was not written in uhlmann_upper_bound.tex: requested from PA (2026-09-08).
- Numerics (rigor/vB2.py): the net-free problem inf ||G||_{3/2}^2 = 2.5678, 2.5630, 2.5579 (boxes 512/1024/2048) -> 8/pi = 2.5465, continuation-independent.

## Track QB result (rigor/implementation_C11.tex, 2026-09-08) — under referee QR2
(H1)-(H3) claimed for EVERY diffeomorphism covariant net on S^1, any c (Thm 5.1): g_tot is C^1 + piecewise smooth with one jump of g'' at 0,
hat g_n = J/(2 pi (in)^3) + O(n^-4), ||g_tot||_{3/2} finite -> Carpi-Weiner Thm 4.4 (e.s.a. on the finite-energy domain), Stone, covariance
by Trotter + localisation (CW05 Prop 5.4) and approximation + additivity/semicontinuity (CDIT Prop 4.1 method); (H2),(H3) from Omega in D(L_0).
Missing estimate appears only one order higher: ||g_tot'||_{3/2} = infinity, T(g_tot)Omega in D(L_0^{1/2}) \ D(L_0) (log divergence, coefficient
c J^2/(48 pi^2)); a FORM bound |<psi, T(f) psi>| <= C ||f||_beta ||(1+L_0)^{1/2} psi||^2 with 1/2 <= beta < 1 is open (operator analogue false for beta < 3/2).
||T(g)Omega||^2 = (c/12) ||g||^2_{dot H^{3/2}} (Weil-Petersson norm). If QR1 and QR2 confirm: Theorem B holds for all diffeomorphism covariant nets
(with HD, BW, RS standard) => universality f_2 = c/(12 pi^2) is a THEOREM (milestone M2, Bures part).

## Track QK result (rigor/kubo_mori_second_variation.tex, 2026-09-08)
Exact identity for unitary orbits with A affiliated with M: D(omega||omega_s) = ||h(Delta)^{1/2}(e^{isA}-1)Omega||^2, h = lambda - 1 - log lambda;
lower bound liminf s^-2 D >= g_KM/2 with NO hypothesis; upper bound (hence D = (s^2/2) g_KM + o(s^2)) under (U_eps): ||Delta^{-eps/2}(e^{isA}-1)Omega|| = O(s),
e.g. A analytic for the modular group in a strip. REFUTED: the Kosaki/Petz-Donald variational route of the plan (suprema -> lower bounds only).
OPEN for Theorem B: A = T(g_tot) is not affiliated with A(I) -> need a Kubo-Mori gauge lemma modulo closure(M'_sa Omega). Bonus: closed-form
reduction of Note 7's KM double integral, g_KM = 1/6 exactly.
- (H2)/(H3) for the free fermion now proved: rigor/uhlmann_upper_bound.tex Sec. 10 (Lemmas 10.1-10.2; 31 pp): Gamma_s Omega = Omega + s :dGamma(D): Omega + o(s),
  ||T(g_tot)Omega|| = ||P_- D P_+||_2 < inf; omega~_s(X) = omega(X) + s i omega([T(g_tot),X]) + o(s) on the CAR *-algebra (bounded fields, no domain hypothesis).

## Referee QR2 (rigor/referee_implementation_C11.tex, 2026-09-08): Theorem 5.1 STANDS for all diffeomorphism covariant nets (CDIT Sec. 4 axioms,
separable H), subject to a one-sentence phase repair (global Virasoro-group lift, FH05 Prop 5.1) — QB asked to apply it. CW05 Thm 4.4 needs only
||f||_{3/2} < inf (its proof uses ||[L_n, e^{-eps L_0}]|| <= sqrt(q)|n|^{3/2}, not Nelson). The "open window 1/2 <= beta < 1" for the form bound is
EMPTY: beta >= 1 is forced, beta = 1 true and sharp; the Nelson route to D(L_0)-invariance is closed. Sign correction: [L_0, T(g)] = +iT(g').
The Trotter split is g_tot = (g_tot - m) + m, not g_A + g_D (the latter has discontinuous truncations since g_tot(L) = -L != 0).

## Track QN result (numerics/boson, 2026-09-08): universality CONFIRMED on the U(1) current net (c = 1): f_2 = 0.00844(2), s_2 = 0.083(2)
(covariance symbol pi kappa coth(pi kappa) in the modular frame; Hermite compression + window; tail exponents 2.3 (f_2), 1.15 (s_2)).
No extension of k_s needed (global Moebius on D -> defect = one A x D integral). c-linearity of the vacuum overlap PROVED analytically at second order:
boson and fermion both give (s^2/(96 pi^2)) int k^3 |g_hat|^2 dk. Decision point (week 8): boson agrees -> proceed to paper 2.

## Referee QR1 (rigor/referee_universality_theorem_B.tex, 2026-09-08): Theorem 7.1 STANDS, no proof-breaking issue. Repairs (sent to QA; (H2') also to QB):
(1) add to (H2) the clause (H2'): T(g_tot)Omega in H_T (limit of T(f_n)Omega, f_n -> g_tot in H^{3/2}) — carries the c-linearity theorem; follows from the
Carpi-Weiner energy bound. (2) restate (H1)'s locality clause as U(Diff(K)) subseteq A(K), Diff(K) = {phi: phi|_{K'} = id} (the "supp phi subset K" form is ill-posed:
supp phi = closure(J_s')). (3) graded case: Haag duality FAILS for the fermion, twisted duality holds; Thm 5.6 needs no (HD); Ad Z trivial on even operators.
(4) minor: Prop 3.2 <1>4 wording; hypothesis lists; (H2) => (H3). Verified independently: zeta = s normal form; no cross term in the Uhlmann expansion;
Schwarzian absent (only Moebius delta_t, r act on H_T); normalization chain incl. ||Pi_-(f d + f'/2)Pi_+||_2^2 = (1/48 pi^2) int p^3 |f_hat|^2 (1.5e-11);
box-free inf ||G||^2_{3/2} = 2.547971 vs 8/pi = 2.546479 (geometric trial family optimal to 0.06%).
=> With QR2: UNIVERSALITY THEOREM f_2 = c/(12 pi^2) for every diffeomorphism covariant net on S^1 (separable, CDIT Sec. 4 axioms), once the repairs are in.
