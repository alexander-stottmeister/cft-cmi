# Phase 5 referee brief (referees run on Claude Opus; never Fable unless the user explicitly requires it)

Object under review: the Phase 5 claim set on the exact value of the all-channel second-order optimum.
  - rigor/exact_optimum_tangent_problem.tex (F1): exact parametrisation of the quasi-free feasible set F by
    (co-isometry V, isometry loss N = 1 - XX*, noise Y = Z - X Q_BB X*, 0 <= Y <= N); the tangent (first-order)
    problem; the KKT sign criterion for noise directions at the isometric optimum; theta closed-form attempt.
  - numerics/optimality_all/F2_RESULTS.md + f2_*.py/.out (F2): tangent SDP with noise in the spectral circle
    model, KKT eigenvalue check, full-F primal SDP in the Galerkin frame.
  - numerics/optimality_all/F3_RESULTS.md + f3_*.py/.out (F3): theta reconciliation (circle model vs Galerkin).

Adversarial stance. Try to break each claim; the burden of proof is on the document.
Checklist for the analytic document (write rigor/referee_exact_optimum_tangent_problem.tex, Lamport style,
one verdict per theorem: STANDS / STANDS WITH REPAIR / FAILS, with the exact step and the counter-argument):
  1. Parametrisation lemma: both directions; the extension of the partial isometry to a co-isometry (dimension
     argument); the case where 1 - N has a kernel.
  2. First-order defect: every block and every sign, including the hermitisation of the DA/AD blocks and the
     factor 1/2 from (1 - sN_1)^{1/2}. Recompute independently from delta = Q - Q_rec.
  3. Tangent problem vs second-order value: is the UPPER bound (constructive) really feasible at finite s
     (check 0 <= sY_1 <= sN_1 <= 1 and X X* <= 1 exactly)? Is the LOWER bound proved or only hypothesised?
     Is the limit interchange (z -> 0 vs minimisation) handled honestly? Any circularity with S10 or E1?
  4. KKT criterion: the gradient normalisation of g_Q (SLD form; check g_Q(delta) = (1/4) Tr(t delta) against S8);
     convexity of the tangent problem in (zeta, N_1, Y_1) (the map to delta^(1) is linear, g_Q convex — but is
     the admissible zeta-class convex and closed?); necessity (rank-one directions) and sufficiency
     (Y_1 = N_1^{1/2} C N_1^{1/2}) arguments; the claim that the zeta-directional derivatives vanish at the orbit
     optimum (this needs the optimum to be attained or a limiting argument).
  5. Consistency with S10 Thm 3.2 at the compression point (multipliers Sigma_1) — same criterion?
  6. Non-surjective isometry families (skew-symmetric, non-skew-adjoint generators): is the claim about the
     closure of the admissible class proved, or open? Do not accept "expected".
  7. theta closed form: any claim beyond "open" needs a proof; numerics-fitted constants are NOT acceptable.
Checklist for the numerics (write rigor/referee_phase5_numerics.tex):
  a. Conventions: does the orbit-only optimum reproduce S10's theta at the same L (0.2895 at L = 256)? If the
     code cannot reproduce a published number, everything downstream is unverified.
  b. Homogeneity and scaling tests; solver status; duality gaps; sensitivity to cap/taper.
  c. KKT eigenvalues: independent recomputation of M_* from the definition (finite differences of g_Q along
     random noise directions), not only via the formula.
  d. Galerkin full-F vs orbit: same code path for both numbers? Solver accuracy vs the reported gap?
  e. F3: is the extrapolation order measured or assumed? Are the error bars honest (spread of variants)? Does a
     class dependence, if claimed, survive matched-class comparison (theta(K) agreement between frames)?
  f. Any closed-form candidate: multiple-comparison caveat; reject unless within the error bar AND motivated.
Output: verdict per claim; a list of required repairs; a list of KB cards whose status must change
(use kb -p cft_cmi verdict ID pass|fail|minor --note "..." with KB_ACTOR=REF-P5-x). Never edit the documents
under review; never edit existing referee notes on KB cards.
