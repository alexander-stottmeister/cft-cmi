# KERNEL_RESULTS -- the corner kernel Ghat(Delta) in two independent frames (Phase 6, track G3)

Author: G3 (track agent). Brief: rigor/phase6_g3_brief.md. Script: numerics/networks/corner_kernel.py.
All numbers below come from that script and the named output files; reproducing commands are given with each.

## Quantity, grid, tolerance (fixed before any run)
- G(Delta) := g_Q(delta_0, delta_Delta), the REAL bilinear form of g_Q(d) = (1/4) sum_ij |d_ij|^2/W_ij,
  W_ij = w_i(1-w_j) + w_j(1-w_i), in the eigenbasis of the symbol Q (w_i its eigenvalues):
  G = (1/4) Re sum_ij conj(d0_ij) dD_ij / W_ij. delta_Delta = y-translate by Delta of the first-order corner defect.
  R(Delta) := G(Delta)/G(0); c = 1 (one chirality of the free fermion), so G = Ghat and Ghat(0) = f2 = 1/(12 pi^2).
- Grid Delta in {0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8} (code: DGRID). Two-frame tolerance |R_T0 - R_box| <= 1e-3 (TOL_FRAMES).
- h-fits admissible iff residuals at the three finest h are <= 1e-4 (TOL_FIT); polarisation vs direct sum 1e-10 (TOL_POL).
- Off the diagonal the identity Phi = g_Q presupposes W2 (UNREFEREED); this file measures the bilinear form only.

## Conventions and frame conversions
- (C1) T0 frame (f3_t0.py): I = (-inf, 1), y = -log(1-x); defect ddot(y1,y2) = -(i/2pi) sinh(y1/2) sinh(y2/2)/
  sinh^2((y1-y2)/2) on y1 < 0 < y2, + h.c. (f3_t0.kern times i/2pi); delta_Delta(y1,y2) = ddot(y1 - Delta, y2 - Delta)
  (corner_kernel.t0_defect = f3_t0.ddot on the edges shifted by the node y = Delta). Q: exact Galerkin matrix of the
  multiplier in the cell basis (kkt_continuum.Qmat).
- (C2) Box frame (defect_matrix.py, compression_box.py): I = (-a, L), xi = y_I(x) = log((x+a)/(L-x)) (= the y of
  rigor/phase6_brief.md "Setting and conventions"), beta_I(x) = (x+a)(L-x)/(a+L); a = 1, L = 2. Corner 1 at x = 0
  (xi0 = log(a/L)), 'first' kernel with s = 1, zeta = a s/(a+L) = 1/3.
- (C3) Second corner: p'(Delta) = a L (e^Delta - 1)/(L + a e^Delta), i.e. y_I(p') - y_I(0) = Delta; it is the corner
  x = 0 of the shifted frame (a', L') = (a + p', L - p') (same interval I, same xi), with s' = zeta (a+L)/a' so that its
  strength zeta' = sigma' beta_I(p') = (s'/L')(p'+a)(L-p')/(a+L) equals zeta (lem:field: zeta = sigma beta_I(p);
  lem:density: zeta is Moebius invariant; rigor/network_corner_calculus.tex).
- (C4) Box <-> T0 kernel identity (checked in K0(e) in 30-digit arithmetic, 10 x 40 random points, worst 6e-27):
  sqrt(beta_I(x) beta_I(x')) (s/L) u v/(u+v)^2 |_{u=-x, v=x'} = zeta * f3_t0.kern(xi - xi0, xi' - xi0), and the corner-2
  kernel equals the corner-1 kernel translated by Delta in xi. Hence both frames discretise the SAME continuum quantity,
  G(Delta) = g_Q(delta_0, delta_Delta) with delta = zeta * ddot(. - y_p): box values are divided by zeta1 zeta2 = 1/9.
- (C5) Box modes: e_j = e^{i k_j xi}/sqrt(Lam) on the window [xi_c - Lam/2, xi_c + Lam/2], k_j = 2 pi j/Lam,
  |j| <= M = floor(kappa_max Lam/(4 pi^2)), kappa = 2 pi k; window centred at corner 1 (xi_c = xi0) for every Delta.
  Q_box = compression_box.Q_box(kappa, Lam, xi0 = xi_c) (exact compression, trapezoid with 400001 nodes);
  LINE symbol q(kappa_j) = 1/(1 + e^{kappa_j}) on the same modes = numerics/line_so.py's weights.

## K0 Validation
Command: `$PYTHON numerics/networks/corner_kernel.py K0` -> numerics/networks/kernel_validate.out (about 1 min).
- (a) T0, Y = 6, Ymax = 20: g_Q(ddot)/f2 = 0.9115757, 0.9545448, 0.9765373, 0.9869870, 0.9901862 at h = 0.24, 0.12,
  0.06, 0.03, 0.02; f3_t0_final.out: 0.91158, 0.95454, 0.97654, 0.98699, 0.99019 -- equal to all 5 printed digits
  (max |diff| 4.8e-6 < half a unit of the 5th digit). Mine at h = 0.02: 0.99019 (published 0.990). PASS.
- (b) bilinear code at Delta = 0 vs f3_gal.theta's g0 on the same matrices: rel. diff <= 2.1e-16 < 1e-12. PASS.
- (c) box, 'first', one corner, compression_box path (Q_box, qfi_c2): f2_box = 0.008369783 at (Lam, kappa_max) =
  (60, 30) vs 0.00836978 (numerics/results_batch3.txt:8) and 0.0083698 (numerics/line_so.txt:1). PASS.
  At (120, 45) the compression_box path is NOT EVALUABLE in double precision: Q_box has eigenvalues ~ e^{-44.7} ~ 4e-20,
  computed as -1.2e-15 (min) and 1 + 4.9e-15 (max), so W_ij <= 0 and qfi_c2 = inf. The published (120, 45) value
  0.0084112 (numerics/line_so.txt:4, rigor/check_note5_numerics.tex:677) is the LINE-symbol value of line_so.py.
- (c') LINE symbol on the same box modes: f2_line = 0.008369789 (60,30), 0.008370596 (120,30), 0.008411248 (120,45)
  [published 0.0083698, -, 0.0084112: PASS]; where Q_box is resolved, |f2_line - f2_box| = 5.3e-9 (60,30), 3.7e-10
  (120,30). So the line weights and the compression agree to < 1e-6 relative where both are computable.
- (d) corner_kernel.box_corner (window-general quadrature) at xi_c = xi0 vs defect_matrix.run: max|diff|/max|D| =
  1.8e-16 (60,30), 3.5e-16 (120,45). PASS. (d') the cancellation-free evaluation used in production differs from
  defect_matrix.run by 7.0e-12 (60,30) and 2.5e-8 (120,45) of max|D| (defect_matrix.run's L - x cancels; see K2).
- (e) (C3) and (C4) in 30-digit arithmetic: |y(p') - y(0) - Delta| <= 5.5e-28, |zeta' - zeta| = 0, kernel identities to
  <= 6.0e-27 at every Delta of the grid. PASS.
- Consequence for K2: (120, 45) and (120, 60) cannot use Q_box's eigenbasis in double precision without a regulator;
  K2 reports (i) Q_box with a spectral window on the unresolved clusters (eps-dependence shown) and (ii) the regulator-
  free LINE symbol on the same modes, and their difference (AGENTS.md sec. 5, regulator rule); (ii) turned out to be
  numerically stable only up to kappa_max = 60 (K2).

## K1 T0 frame: R(Delta) on the h-ladder
Commands: `$PYTHON numerics/networks/corner_kernel.py K1` (-> kernel_t0.out, kernel_t0.npz; ~40 min), `... K1b` (h = 1/128
-> kernel_t0b.out, kernel_t0b.npz; ~10 min), `... K1fit` (-> kernel_t0_fits.out, kernel_t0_est.npz; seconds).
- Ladder. The brief's h = 0.24, 0.12, 0.06, 0.03 cannot carry the grid: a corner at Delta must be a mesh node for delta_Delta
  to be the translate of delta_0 on the same mesh, and Delta/h is an integer for all four rungs only at Delta = 0, 6 (and
  Delta = 3 for h <= 0.12). Production therefore uses the dyadic ladder h = 1/4, 1/8, ..., 1/128 (every Delta of the grid
  is a node); the brief's ladder is run at Delta = 0, 3, 6 as a cross-check ([B] in kernel_t0.out). Mesh [-Y, Ymax] =
  [-14, 20] (Y >= Delta + 6, Ymax >= Delta + 10 for all Delta <= 8), N = 136 ... 4352.
- Checks: polarisation identity <= 2.2e-16 G0; translate check max|delta_Delta[i+s,j+s] - delta_0[i,j]|/max|delta_0| <=
  3.6e-16 (delta_Delta IS the translate); the vectorised path of K1b (corner_kernel.t0_ddot_fast) equals f3_t0.ddot to
  3.6e-16 and reproduces the K1 values at h = 1/8, 1/64 to 2.1e-16. Ymax = 20 -> 24 changes R_h(8) by +2.3e-7 at every h
  and G0/f2 by < 1e-8 (kernel_t0_fits.out, last block): the window is not a limiting systematic.
- Diagonal (cut-off weight of the sub-cell modes): G0/f2 = 0.914136, 0.958294, 0.980944, 0.991713, 0.996545, 0.998611 at
  h = 1/4 ... 1/128. NOTE: F3's ladder (f3_t0_final.out, reproduced in K0) uses Y = 6, where the A-side window removes a
  further ~0.6 % (f3_t0_Y.out: 0.95443 at Y = 6 vs 0.96000 at Y >= 14, h = 0.12); with Y = 14 the cut-off weight at h
  = 1/32 is 0.83 %, not 1.3 %.
- Convergence variable h, measured: local exponents p_loc DRIFT upward, e.g. R_h(1): 0.61, 0.78, 0.94, 1.07 (all Delta
  alike, kernel_t0_fits.out), G0/f2: 0.96, 1.07, 1.16, 1.23. Admissible fits (residual <= 1e-4 at the 3 finest rungs):
  lin and pow on the 4 finest rungs for every Delta, and the fits on the 4 rungs one step coarser for every Delta; also
  log-4f (no finite limit) at Delta = 0.5 (residual 8.2e-5) and 8 (6.6e-5) for R_h [corrected 2026-10-05: the first
  version said 'log never']. log is excluded from the estimate: a log h drift has constant increments per halving, the
  measured increments shrink by factors 0.47 ... 0.69 per halving (p_loc) -- a data argument, not a proof. Calibration on the known diagonal limit (G0 -> f2, Theorem A): the same procedure applied to G0/f2 gives 1.00028
  (pow-4f, the only admissible fit), i.e. the h-extrapolation of this frame overshoots by ~3e-4 when p_loc still drifts.
- T0 estimates (R_h = G_h/G0_h; centre of the admissible finite-limit fits; u = half spread + 3e-4, the calibrated
  overshoot, corner_kernel.T0_SYST; kernel_t0_est.npz), Delta = 0.5 ... 8: 0.89844(41), 0.74573(44), 0.60090(46),
  0.47713(47), 0.29468(46), 0.17991(43), 0.10939(40), 0.06642(38), 0.02445(34). [Repaired 2026-10-05 after REF-P6-5:
  the first version quoted the half spreads alone, (11) ... (37), which do not cover the overshoot; the refereed closed
  form (card corner-kernel-closed-form) lies 0.5 ... 1.06 half spreads, <= 0.4 u, below every value.] The second
  estimator S_h = G_h/f2 gives 0.898672, 0.745892, 0.600998, 0.477190, 0.294699, 0.180019, 0.109480, 0.066473, 0.024475,
  each +- (half spread + 3e-4) (kernel_decay.out).
- Brief's ladder at Delta = 6: R_h = 0.062244, 0.064013, 0.065128, 0.065756 (h = 0.24, 0.12, 0.06, 0.03), pow fit 0.066750
  (the only admissible fit), 3.4e-4 above the dyadic estimate: four rungs ending at h = 0.03 do not reach the regime where
  p_loc ~ 1; at Delta = 3 only three rungs exist (no fit).


## K2 Box frame: two 'first' kernels in one box
Commands: `$PYTHON numerics/networks/corner_kernel.py K2` (boxes (60,30), (120,30), (120,45), (120,60) -> kernel_box.out,
kernel_box.npz), `... K2b` (Lam = 120, kappa_max = 75, 90, 105, 120 -> kernel_boxb.out, kernel_boxb.npz), `... K2fit`
(-> kernel_box_fits.out). Each run takes 1-3 min. Setting (C2), (C3), (C5): corner 1 at x = 0, corner 2 at p'(Delta), one
window centred at corner 1, zeta = 1/3 each, G = g_Q(D1, D2)/zeta^2. (120, 30) is added to the brief's ladder so that
kappa_max can be varied at fixed Lam; (120, 75 ... 120) because the kappa-convergence turned out to oscillate (below).
- Three symbols on the same modes and defect matrices. [box] = eigenbasis of Q_box, no regulator: resolved only for
  kappa_max ~ 30 (smallest eigenvalue 2.8e-13 at (60,30), 1.3e-13 at (120,30); negative in double precision from 45 on).
  [win] = [box] with the pairs dropped whose two eigenvalues are both < eps or both > 1 - eps (a regulator); eps = 1e-13,
  1e-12, 1e-11 give the same R to <= 2e-9 at every box and Delta, and [win] = [box] to <= 1e-9 where [box] is resolved.
  [line] = line_so.py weights: agrees with [win] to <= 8.5e-6 in R at (60,30) and <= 1.7e-7 at Lam = 120 up to
  kappa_max = 60 ([win] vs [box] where resolved: <= 7.5e-11), numerically unstable from 75 on
  (its weights e^{kappa} amplify quadrature noise; kernel_boxb.out). Production symbol: [win] with eps = 1e-12.
- Polarisation: (qfi_c2(D1 + D2) - qfi_c2(D1 - D2))/4 equals the direct bilinear sum to <= 2.3e-16 relative to G(0)
  wherever [box] is resolved (tolerance 1e-10, PASS); the same identity with the [line] weights holds to <= 2e-16 up to
  kappa_max = 60 (4e-14 beyond, where those weights are unstable anyway); [win] is evaluated by the direct sum only.
- Code fix needed on the way: defect_matrix.run evaluates beta_I(x) with L - x, which cancels for large |xi - xi0|; in
  the shifted frame (a', L') this produced NaN at Lam = 120 (first K2 pass). corner_kernel.box_corner(stable=True) uses
  the same functions in cancellation-free form; it differs from defect_matrix.run by 7.0e-12 (60,30) and 2.5e-8 (120,45)
  relative to max|D| (K0 (d')). [MINOR] the published (120,45) line value 0.0084112 (numerics/line_so.txt:4) carries this
  error: with the cancellation-free kernel the same line computation gives G0/f2 = 0.99617060, i.e. 0.0084111.
- Window effect (Lam = 60 vs 120 at kappa_max = 30, kappa_max_eff 29.61 vs 29.94): |dR| <= 1.7e-4, |d(G/f2)| <= 9.6e-5,
  both of the size the kappa_max_eff difference alone produces; the window is not the limiting systematic.
- Cut-off weight. Diagonal: 1 - G0/f2 = 8.63e-3, 3.83e-3, 2.13e-3, 1.37e-3, 9.5e-4, 6.9e-4, 5.3e-4 at kappa_max = 30,
  45, ..., 120 (local exponent 2.02, 2.01: the known kappa^-2 law). Cross terms: G(Delta)/f2 changes by at most
  3.9e-3 (Delta = 0.5), 2.2e-3 (1), 1.2e-3 (1.5), 3.8e-4 (2), 2.6e-4 (3), 1.2e-4 (4), 4.4e-5 (5), 3.7e-5 (6), 1.1e-5
  (8) between kappa_max = 30 and 120, and it OSCILLATES in kappa_max (e.g. Delta = 1: 0.74340, 0.74618, 0.74548,
  0.74562, 0.74565, 0.74559, 0.74563) -- a sharp cut-off of a Fourier integral of e^{i kappa Delta/2pi}, period ~
  4 pi^2/Delta in kappa. Hence no smooth fit in 1/kappa_max is admissible at Delta = 0.5 (kernel_box_fits.out) and the box
  estimate is the finest rung kappa_max = 120 with uncertainty = max deviation of the rungs 75, 90, 105 from it
  (envelope) -- at EVERY Delta, a deviation from the sec. 5 fit spread: where fits are admissible (Delta >= 1) they can
  miss (Delta = 3: 0.2945479 +- 1.95e-5 excludes the closed-form 0.2945231, which the envelope contains). At kappa_max =
  75 ... 120 no regulator-free computation exists on the same mesh ([box] not evaluable, [line] unstable), so S is
  regulator-dependent, with spread <= 2e-9 over eps = 1e-13 ... 1e-11 (sec. 5; added 2026-10-05 after REF-P6-5). R = G/G0 in the box is biased upward by R (1 - G0/f2) = R * 5.3e-4 at kappa_max = 120 (diagonal cut-off),
  so the box estimator of R is S := G/f2 (G(0) = f2 exactly, Theorem A).
- Box values (S = G/f2 at Lam = 120, kappa_max = 120, envelope in brackets; single frame, single method):
  0.89835(19), 0.745633(47), 0.600737(21), 0.476965(19), 0.294525(10), 0.1797849(56), 0.1092993(23), 0.0663499(6),
  0.0244192(3) at Delta = 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8.

## K3 Decay and sign
Command: `$PYTHON numerics/networks/corner_kernel.py K3` (-> kernel_decay.out). Primary estimators: T0 R_h (above), box S.
- Local decay rates -dlog R/dDelta on [3,4], [4,5], [5,6], [6,8]: 0.4934, 0.4975, 0.4990, 0.4997 (T0); 0.4936, 0.4977,
  0.4991, 0.4998 (box): increasing towards 1/2 from below in both frames.
- Fits on Delta in {3, 4, 5, 6, 8}: A e^{-alpha Delta}: alpha = 0.4981 (T0), 0.4982 (box), A = 1.317, max |residual in
  log R| = 3.1e-3 (the pure exponential does not fit to 1e-3); A Delta^b e^{-alpha Delta}: alpha = 0.5058 (T0), 0.5058
  (box), b = +0.040, max residual 6.2e-4. Over both models, both frames and R +- u: alpha = 0.504 +- 0.009 with the
  repaired T0 u (0.502 +- 0.004 with the fit spreads alone); the spread is the model dependence, the rates above are the
  cleaner statement, and the rate 1/2 is proved (card corner-kernel-closed-form (d)).
- Sign: R(Delta) exceeds its uncertainty by a factor >= 72 (T0 at Delta = 8 with the repaired u; >= 600 with the fit
  spreads alone, as first written) at every Delta of the grid in both frames: R > 0 is established numerically at the
  nine grid points (not beyond Delta = 8, and not between grid points).
- No value exceeds 1: R < 1 at the nine grid points in both frames. For all Delta != 0, R > 0 and R < 1 are proved
  (card corner-kernel-closed-form (e)); the numerics say nothing between grid points.

## K4 Finite zeta, two corners
Commands: `$PYTHON numerics/networks/corner_kernel.py K4` (eps = 1e-8 -> kernel_k4.out, ~10 min), `... K4b` (eps = 1e-11 ->
kernel_k4b.out, ~20 min), `... K4v` (-> kernel_k4_validate.out). Box (Lam, kappa_max) = (60, 30), corners at x = 0 and
p'(Delta), zeta1 = zeta2 = zeta, sigma1 = zeta (a+L)/(aL), sigma2 = zeta (a+L)/((a+p')(L-p')).
- Kernel: exact composite of Phi = k1 o k2 (corner_kernel.box_composite). Between the three Moebius pieces of Phi,
  D(x,y) = (i/2pi)[sqrt(m'(y))/(x - m(y)) - 1/(x - y)], m = g_i^-1 o g_j (Moebius covariance of the vacuum kernel), i.e.
  defect_matrix's 'exact' kernel at each corner for the adjacent pieces and, for the outer pair, m = k1 o k2 written with
  all terms positive. With sigma2 = 0 (sigma1 = 0) it equals box_corner's single-corner 'exact' kernel to 5.2e-13 of
  max|D|. Phi_A(zeta_i) = the same routine with the other sigma = 0 (same modes, nodes, window: discretisation errors
  common to Phi_2 and Phi_A cancel at first order). G = the 'first'-kernel bilinear form in the same window.
- Fidelity: compression_box.fid_relent is not usable: in double precision it returns O(1) noise of either sign for exact
  kernels already at (60,30) (numerics/results_batch3.txt:1-7 range from -9.4 to +3.1; the first version said '< 0', which
  describes one draw). Used: the Theorem A pipeline's method (numerics/fidelity_hp.py):
  sub-compression onto the eigenvectors of Q_box with eigenvalue in [eps, 1 - eps] (a compression, so -log F_eps <=
  -log F), Note 5's quasi-free fidelity in 30-digit mpmath, sqrt(tau) as singular values (eighe of W W^* failed to converge
  at eps = 1e-11). Validation (kernel_k4_validate.out): -log F_sub = 5.679016216e-07 and 8.863062300e-06 for one corner at
  s = 0.025, 0.1, eps = 1e-8, published 5.679016e-07, 8.863062e-06 (numerics/results_A2.txt:1,3); at eps = 1e-11 the
  value differs from numerics/results_hp.txt:1 by 8.8e-6 relative (cause not investigated; irrelevant at the level below).
- Window = cut-off: eps = 1e-8 keeps 61 of 91 modes (|kappa| <~ 18.4, G_eps(0)/f2 = 0.976711), eps = 1e-11 keeps 81
  (|kappa| <~ 25.3, 0.987844); the cut-off is common to all four terms.
- Results, rem := Phi_2 - Phi_A(zeta1) - Phi_A(zeta2) - 2 zeta^2 G_eps(Delta), as rem/zeta^3 at zeta = 0.05 / 0.1 / 0.2:

| Delta | eps = 1e-8 | eps = 1e-11 | rem/(2 zeta^2 G) at zeta = 0.05, 0.1, 0.2 (eps = 1e-11) |
|---|---|---|---|
| 1 | -0.02442 / -0.02265 / -0.01975 | -0.02443 / -0.02267 / -0.01976 | -0.097, -0.181, -0.315 |
| 2 | -0.01365 / -0.01278 / -0.01131 | -0.01363 / -0.01276 / -0.01129 | -0.084, -0.158, -0.280 |
| 4 | -0.004553 / -0.004293 / -0.003848 | -0.004549 / -0.004290 / -0.003845 | -0.075, -0.142, -0.254 |
| 8 | -0.000582 / -0.000551 / -0.000497 | -0.000584 / -0.000553 / -0.000498 | -0.071, -0.134, -0.242 |

- Reading (numerical, (60, 30) box, these Delta and zeta only; repaired 2026-10-05 after REF-P6-5): in the spectral
  window the problem is finite-dimensional and analytic, so rem = O(zeta^3) holds there AUTOMATICALLY; the numerics
  measure the coefficient c(Delta) = rem/zeta^3, which DEcreases with Delta (0.024 at Delta = 1 to 0.0006 at Delta = 8),
  and show that the next order is <= 20 % (of the largest value) over zeta in [0.05, 0.2]. The order of the continuum
  (window-free) remainder of W2 is NOT tested. rem/(2 zeta^2 G) ~ -(1.4 to 2.0) zeta, i.e. the cross term itself
  carries a relative correction of first order in zeta, of the size of the single-corner one (Phi_A/(zeta^2 G_eps(0)) - 1
  = -0.0479, -0.0919, -0.170 at zeta = 0.05, 0.1, 0.2, eps = 1e-11). The window changes rem/zeta^3 by <= 2.2e-5.
- Clustering at Delta = 8: (Phi_2 - Phi_A1 - Phi_A2)/(Phi_A1 + Phi_A2) = 0.0241 at zeta = 0.05 (eps = 1e-11): Phi_2 ->
  Phi_A + Phi_A up to the cross term 2 zeta^2 G(8) (R(8) = 0.0244), which is what W2 predicts at this separation.
- Not tested: Delta < 1, a second box, the uniformity of the remainder for Delta -> 0 or zeta -> 0 with Delta growing.

## Two-frame comparison and diagnosis
kernel_decay.out (first block). Tolerance 1e-3 (fixed in the brief). Primary estimators: T0 R_h extrapolated in h, box
S = G/f2 at kappa_max = 120 with the envelope of kappa_max = 75 ... 120.

| Delta | R_T0 (K1) | S_box (K2) | |diff| | all four estimators within | agreed value (both frames) |
|---|---|---|---|---|---|
| 0.5 | 0.89844(41) | 0.89835(19) | 9.1e-5 | 4.8e-4 | 0.8984(5) |
| 1 | 0.74573(44) | 0.745633(47) | 9.4e-5 | 4.0e-4 | 0.7457(5) |
| 1.5 | 0.60090(46) | 0.600737(21) | 1.6e-4 | 3.2e-4 | 0.6008(6) |
| 2 | 0.47713(47) | 0.476965(19) | 1.6e-4 | 2.5e-4 | 0.4770(6) |
| 3 | 0.29468(46) | 0.294525(10) | 1.6e-4 | 1.7e-4 | 0.2946(6) |
| 4 | 0.17991(43) | 0.1797849(56) | 1.3e-4 | 2.3e-4 | 0.1798(5) |
| 5 | 0.10939(40) | 0.1092993(23) | 9.2e-5 | 1.8e-4 | 0.1093(5) |
| 6 | 0.06642(38) | 0.0663499(6) | 6.5e-5 | 1.2e-4 | 0.06638(41) |
| 8 | 0.02445(34) | 0.0244192(3) | 2.9e-5 | 5.6e-5 | 0.02443(36) |

- VERDICT: the two frames agree within the tolerance at every Delta (max |R_T0 - S_box| = 1.6e-4 <= 1e-3; all four
  estimators R_T0, S_T0, S_box, R_box within 4.8e-4). Agreed value = midpoint of the two frames, uncertainty = |diff|/2 +
  the larger single-frame uncertainty, rounded up; both frames lie inside it, so the quoted digits are common to both.
  [Repaired 2026-10-05: the T0 column now includes the calibrated overshoot 3e-4; with the fit spreads alone the agreed
  uncertainties were (3), (2), (3), (3), (3), (2), (2), (11), (6), and the refereed closed form lies inside even those.]
- What each discretisation resolves (no disagreement to diagnose, recorded as the brief asks): T0 resolves piecewise-
  constant functions of width h on [-14, 20]; it cuts off the sub-cell structure, whose weight is 1 - G0/f2 = 1.4e-3 of
  the diagonal at h = 1/128 and is removed by the h-extrapolation (systematic of that extrapolation ~3e-4, calibrated on
  the diagonal). The box resolves |kappa| <= kappa_max on a window of length 120; the cut-off weight of the diagonal is
  5.3e-4 at kappa_max = 120 (kappa^-2 law), that of the cross terms oscillates and is <= 1.9e-4 at kappa_max >= 75 (the
  envelope); the window weight is below 1.7e-4 already at Lam = 60. The residual T0 - box differences (+3e-5 ... +1.6e-4,
  all of one sign) are of the size and sign of the T0 extrapolation overshoot measured on the diagonal.
- Comparison with G1b (rigor/g1b_kernel.out, 17:37, continuum quadrature of the cosine transform of rho; unrefereed when
  this was written, since refereed by REF-P6-4 as card corner-kernel-closed-form; compared only, nothing fitted or adjusted): Ghat(Delta)/Ghat(0) = 0.898387, 0.745615, 0.600745,
  0.476960, 0.294523, 0.179784, 0.109299, 0.0663498, 0.0244192. Box S minus G1b: -3.8e-5, +1.8e-5, -8e-6, +5e-6, +2e-6,
  +6e-7, +3e-7, +1e-7, 0 (each inside the box envelope); T0 R minus G1b: +5.3e-5, +1.1e-4, +1.5e-4, +1.7e-4, +1.6e-4,
  +1.3e-4, +9.2e-5, +6.5e-5, +2.9e-5 (0.5 ... 1.06 times the T0 fit half-spread, <= 0.4 times the repaired T0 u,
  one-signed as above). The three methods agree to <= 1.7e-4 at every Delta of the grid; G1b's quadrature shares no code
  with either frame, the two frames share only corner_kernel.sld/bil (the definition-level evaluation of g_Q from (Q, D);
  corrected 2026-10-05, the first version said 'three methods with no shared code').

## Not done / open
- Deviations from the brief, each forced by a measured obstruction: (1) K1 ladder: the brief's h = 0.24 ... 0.03 puts most
  grid Deltas off the mesh; production on h = 1/4 ... 1/128, the brief's ladder only at Delta = 0, 3, 6. (2) K2: Q_box's
  eigenbasis is not resolvable in double precision beyond kappa_max ~ 33 (eigenvalues ~ e^{-kappa_max}); the pairs in
  the unresolved clusters are dropped (eps-independent to 2e-9, equal to the unregulated value where that exists); the
  cross terms oscillate in kappa_max, so the box uncertainty is the envelope of the last four rungs, not the spread of
  admissible fits, at every Delta (none is admissible at Delta = 0.5; where they are, they can miss, K2). (3) K0(c) at (120, 45) is validated against line_so.py's value
  with its weights, because compression_box.qfi_c2 returns inf there. (4) K4 does not use compression_box.fid_relent
  (it returns O(1) noise of either sign in double precision for exact kernels already at (60, 30)); it uses the Theorem A pipeline's
  spectral window and 30-digit fidelity, at (60, 30) only.
- Not computed: Delta between grid points and beyond 8; Delta < 1 in K4; K4 at a second box; any interval-certified
  number (all values are numerical, double precision except the 30-digit identities of K0(e) and the K4 fidelities).
- Open for the orchestrator: status of corner-correlation-kernel (sign and decay are now measured numerically in two
  frames, and G1b reports a closed form, unrefereed); the defect_matrix.run cancellation (dhat-quadrature-certification
  note) for any future Lam >= 120 run.
- KB (all numerical, KB_ACTOR = G3, awaiting review): corner-kernel-pipeline-validation (K0), corner-kernel-t0-frame
  (K1), corner-kernel-box-frame (K2), corner-kernel-two-frames (K3 + comparison), two-corner-remainder-finite-zeta (K4);
  notes on corner-correlation-kernel, network-second-order-law, dhat-quadrature-certification, corner-kernel-closed-form
  (G1b's card; the comparison above is with its quadrature output rigor/g1b_kernel.out).

## Repairs after REF-P6-5 (2026-10-05; report rigor/referee_corner_kernel.tex)
- corner-kernel-pipeline-validation: STANDS. The other four cards: STANDS WITH REPAIR; numbers unchanged, repaired here and
  on the cards: (1) T0 uncertainties = fit half-spread + 3e-4 (calibrated overshoot; corner_kernel.T0_SYST), log-4f
  disclosed with the reason for excluding it; kernel_t0_fits.out, kernel_t0_est.npz, kernel_decay.out regenerated
  (centres identical). (2) Box: no regulator-free computation at kappa_max = 75 ... 120 (S regulator-dependent, spread
  <= 2e-9); the envelope replaces the fit spread at every Delta; envelopes rounded up. (3) Two frames: sign margin >= 72;
  R < 1 claimed at the grid points only; agreed uncertainties widened by (1); alpha = 0.504 +- 0.009 with the repaired u.
  (4) K4: O(zeta^3) is automatic in the window; the coefficient c(Delta) is what is measured; the eps = 1e-11 validation
  mismatch (8.8e-6 with results_hp.txt:1) disclosed; fid_relent returns noise of either sign. The headers of
  kernel_k4.out and kernel_k4b.out (written 2026-10-03) still say '-log F < 0'; the script text is corrected for reruns.
