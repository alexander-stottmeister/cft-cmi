# Phase 6 brief — multi-interval networks (O10, second half) (2026-09-16)

Card: `kb -p cft_cmi show phase6-plan` (decision) and `multi-interval-networks` (question). Status file: rigor/PHASE6_STATUS.md.

## Question
Chains A_1 ... A_n of adjacent intervals and sequential ONE-SIDED zero-collar recovery (each step is the geometric
compression of Note 4 / Theorem A applied to the block recovered so far). What is the recovery error of the composite,
how does it depend on the ORDER of the steps (Note 3's "recovery holonomy"), does it telescope against the CMI chain
rule, and what of it is universal (c times a universal function)? Vardhan-Wei-Zou (refs/VWZ_2307.14434.pdf, Sec. 5,
Fig. 24-25) define Protocols 1(A), 1(B), 2, 3 for four intervals and report lattice numerics (<= 8 sites per interval);
our exact machinery (Note 4, Note 5 Thm 2.1/3.2, Theorem A tables, the modular-frame code of Phase 5) decides them.

## Setting and conventions (fixed for the whole phase; every track uses these symbols)
- Points p_1 < ... < p_{n+1}; A_k = (p_k, p_{k+1}), l_k = p_{k+1} - p_k, L_k = p_{k+1} - p_1 = l_1 + ... + l_k, T = L_n,
  I = (p_1, p_{n+1}). c = central charge per chirality; f2 = c/(12 pi^2) (const-f2). The hopping chain has two
  chiralities: dictionary in numerics/lattice/README.md.
- ONE-SIDED STEP: block J (a union of consecutive A's, hence an interval), conditioning interval A_B = the interval of J
  adjacent to the new interval A_new, corner point p = the INNER end of A_B (its junction with the rest of J; for J = A_B
  alone, the end of A_B away from A_new). The zero-collar (rotated or ordinary) Petz map of the half-sided modular
  inclusion F(A_B) subset F(A_B u A_new) is the parabolic Moebius compression fixing p that pushes A_B u A_new toward p:
  in an affine coordinate, h(x) = p + (x-p)/(1 + sigma (x-p)) for A_new to the right of p (sigma > 0), the mirror
  image for A_new to the left; sigma = s/(l_B + l_new), s in [lambda, 2 lambda], lambda = l_new/l_B; s = 2 lambda is the
  ordinary Petz map (VWZ's lambda = 0), s_t = lambda (1 + e^{-2 pi t}) the rotated maps (paper1/sec_petz.tex Def. zeta;
  Note 4 Thm 7.1). The step acts as the identity on J \ A_B. Compression strength of the corner: kappa := -[h''/h'](p)/2
  = sigma > 0 for a compression toward p from EITHER side (both give the same sign of the jump).
- MODULAR FRAME of I: y = log((x-p_1)/(p_{n+1}-x)), beta_I(x) = dx/dy = (x-p_1)(p_{n+1}-x)/T. The first-order field of a
  corner (p, kappa) is EXACTLY zeta w(y - y_p) d/dy with w(u) = -4 sinh^2(u/2) 1_{u>0} (Phase 5 F1 Prop 6.2, f3_t0.py)
  and zeta = kappa beta_I(p).  [Derivation: in the (0,inf)-frame X = e^y, -sigma'(X-X_p)^2 d/dX = -sigma' X_p (X/X_p - 2
  + X_p/X) d/dy = sigma' X_p w(y-y_p) d/dy, and sigma' X_p = sigma beta_I(p) by the (-1)-density law sigma' = sigma/M'(p)
  of parabolic parameters under a Moebius change of coordinate M. Theorem A's zeta = a s/(a+L) is the case p = 0,
  I = (-a, L): beta_I(0) = aL/(a+L), sigma = s/L.]
- STEP FRAME vs CHAIN FRAME (amplification): the same corner has zeta_step = kappa beta_{I_step}(p) in the interval I_step
  = (kept block) u A_B u A_new of its own Theorem-A triple, and zeta^(I) = kappa beta_I(p) in the frame of the whole chain;
  zeta^(I)/zeta_step = beta_I(p)/beta_{I_step}(p) = 1 + z', z' = cross ratio of (p_1, p, far end of I_step, p_{n+1}) =
  the Markov variable z = a c/(b (a+b+c)) of the coarse triple (kept block | A_B u A_new | rest of the chain). >= 1,
  = 1 for the last step.
- L->R PETZ CHAIN (start with A_1 A_2, add A_3, ..., A_n; ordinary Petz): corner k at p_k, k = 2..n-1,
  kappa_k = 2 l_{k+1}/(l_k (l_k + l_{k+1})), zeta_k^(I) = kappa_k L_{k-1} (T - L_{k-1})/T,
  y_k = log(L_{k-1}/(T - L_{k-1})). With r_k = l_{k+1}/l_k, u_k = l_k/L_{k-1}, v_k = l_k/(T - L_k):
  e^{Delta_k} = e^{y_{k+1} - y_k} = (1+u_k)(1+v_k) and zeta_k^(I) = 2 r_k (1+v_k)/((1+r_k)(e^{Delta_k} - 1)).
- SCHWARZIAN of a C^1 piecewise-Moebius map: S(Phi) = sum_k [Phi''/Phi'](p_k) delta_{p_k} (no square term: h' is
  continuous); parabolic corner: [h''/h'](p) = -2 kappa. Composition: S(Phi_1 o Phi_2) = S(Phi_2) + (Phi_2')^2 S(Phi_1) o Phi_2.
- Fidelity conventions: Phi := -log F on F(I) (paper 1); Note 5 Thm 2.1 (symbols) / Thm 3.2 (finite matrices);
  g_Q(delta) = (1/4) sum |delta_ij|^2/(w_i(1-w_j)+w_j(1-w_i)) in the eigenbasis of Q (f3_gal.theta: g0), Phi ~ g_Q(delta).

## Working results (orchestrator, 2026-09-16; UNREFEREED — each is a target to prove, sharpen or refute, never an assumption)
W1 (corner calculus, exact). HYPOTHESIS (added after REF-P6-0, 2026-09-16): every step's conditioning region A_B is a
  SINGLE interval of the chain AND the starting block has >= 2 chain intervals, or, more generally, no earlier corner lies
  in the interior of a later step's moving part A_B u A_new (the weaker condition is the one the proof uses; G1a Ex. 5.6:
  single-interval conditioning with a single-interval start lets an earlier corner be swallowed; VWZ 1(B) conditions on the
  union BC and satisfies the weaker condition, its two corners coinciding at p_2). PROVED: rigor/network_corner_calculus.tex
  Thm 5.3 (under (H)) and Thm 5.2 (unconditional rule); REF-P6-3: stands. Then the composite
  point map Phi is C^1 piecewise-Moebius and
  S(Phi) = -2 sum_k kappa_k delta_{p_k},  kappa_k = sum of the sigma's of all steps whose corner is p_k.
  Without the hypothesis the masses sit at the preimages of the junctions under the later maps, scaled by the derivative
  there (S(f o g) = S(g) + (g')^2 S(f) o g): REF-P6-0's counterexample rigor/ref_p6_0_w1_counterexample.out, lengths
  (1.3, 2.1, 0.9, 1.7), start A_2A_3, add A_4 on A_3 then A_1 on A_2A_3, has its mass at k_2^{-1}(p_3) = 3.2006 with weight
  -2 sigma_1 k_2'(x_0), k_2' = 0.670 (71% of the naive total). Reason for the hypothesis case: near its corner p each
  step's map is preceded (in point order) by later steps, which are the identity near p or fix p with derivative 1, and
  followed by earlier steps, which are Moebius near the image of p; the parabolic subgroup fixing
  p is abelian, so parameters at a common point add, and a left- and a right-compression at the same point differ only
  by a GLOBAL Moebius map. The recovered state omega o beta_Phi depends only on S(Phi): post-composition with a Moebius
  map g does not change it (omega o Ad U_g = omega). Consequences: (i) VWZ Protocol 1(B) = 1(A) exactly, because
  2c/(b(b+c)) + 2d/((b+c)(b+c+d)) = 2(c+d)/(b(b+c+d)) (also for every common rotation t) — reproduces the identity VWZ
  state; (ii) VWZ Protocol 3 (start BC, add A conditioning on B and D conditioning on C, in either order) has ONE double
  corner at p_3 and equals, up to post-composition with a global Moebius map, the over-compressed single-step map of
  Theorem A, hence as a fidelity  Phi^(3) = Phi_A(zeta_eff),
  zeta_eff = (sigma_1 + sigma_2) beta_I(p_3) = zetabar_3^(I) + zeta_3^(I), sigma_1 = 2a/(b(a+b)), sigma_2 = 2d/(c(c+d)),
  exactly and for all sizes (Phi_A from paper 1's tables); (iii) exact recovery never occurs: every kappa_k > 0, plus
  'corner measure != 0 => Phi > 0' (Theorem A for one corner, part of W2 for several);
  (iv) the "recovery holonomy" of Note 3 is the corner measure kappa = sum kappa_k delta_{p_k}: protocols with the same
  corner measure give the same state (Protocol 3 in either order); in the vacuum sector it is pure geometry (Schwarzian
  data), so categorical data can only enter through charged sectors (O11), not through the order of vacuum recoveries.
W2 (second-order network law). For corners (y_k, zeta_k) in the modular frame of I,
  Phi_tot = sum_{j,k} zeta_j zeta_k G(y_j - y_k) + o(|zeta|^2),  G(Delta) = c Ghat(Delta),  Ghat(0) = 1/(12 pi^2),
  Ghat even and POSITIVE-DEFINITE (which does NOT imply Ghat >= 0 pointwise; the sign for Delta > 0 is open):
  G(Delta) = g_Q(delta_0, delta_Delta) (real polarisation of the quadratic form) with delta_Delta the y-translate of the closed-form
  first-order kernel ddot(y1,y2) = -(i/2 pi) sinh(y1/2) sinh(y2/2)/sinh^2((y1-y2)/2), y1 < 0 < y2, + h.c. (f3_t0.py; frame
  I = (-inf,1), y = -log(1-x)); with Q a Fourier multiplier in y, G is the Fourier transform of the positive spectral
  density rho(q) = (1/4) int dp |dhat_0(p,p-q)|^2 / W(p,p-q). Lower bound: data processing + Legendre form
  (quadratic_limit.tex Thm "lower") is linear in the defect, hence verbatim. Upper bound: Uhlmann + C^{1,1} flow
  extension (uhlmann_upper_bound.tex Sec. 1, rate_of_remainder.tex) with finitely many second-derivative jumps; the
  three-way identity inf_ext = SLD form = 4 dist(., commutant)^2 is Hilbert-space geometry and extends. Expected global
  bound: Phi_tot <= -(1/2) log(1 - 2 sum zeta zeta G) (group extension, as in rate-of-remainder).
W3 (separation constraint; wording repaired after REF-P6-0). Admissible protocols (s >= lambda) ALL OF WHOSE corners are
  weak (zeta_j <= eps for EVERY j) cannot place two of them close at distinct points: for the L->R chain
  (e^{Delta_k} - 1) zeta_k^(I) = 2 r_k (1+v_k)/(1+r_k) >= 2 r_k/(1 + r_k), and zeta_j <= eps for all j forces
  e^{Delta_k} >~ 2/eps: the numerical minimum of e^{Delta} over L->R chains is 2/eps to 4 digits (20.05, 66.68, 200.0,
  666.7 at eps = 0.1, 0.03, 0.01, 0.003, rigor/ref_p6_0_separation.out; the optimum saturates every zeta_j = eps); the
  bound is PROVED for all-weak L->R Petz chains (network_corner_calculus.tex Thm 11.1, sharp as eps -> 0; REF-P6-3: stands). With only the PAIR weak the separation can
  stay O(1) (zeta_2 = zeta_3 = 0.01 at Delta ~ 1.3, paid for by a large zeta elsewhere). Sketch of the all-weak case: Delta_k small => u_k, v_k small => l_k << L_{k-1} and
  l_k << T - L_k; zeta_k small then forces r_k small; zeta_{k+1} small forces l_{k+2} << l_{k+1} << l_k while T - L_k >> l_k
  needs a later long interval, whose own step has zeta >> 1). Coincident corners (Delta = 0) ARE allowed (Protocol 3).
  Hence at strict second order, for all-weak protocols and PROVIDED the o(|zeta|^2) remainder of W2 is uniform in the
  corner separations AND the separation bound e^{Delta} >= 2/eps holds (both to be proved),  Phi_tot = f2 sum_{points} ( sum_{steps at the point} zeta )^2 + O(eps^2 sup_{Delta >= log(2/eps)} |Ghat(Delta)|):
  strengths add coherently at a common point, distinct corners are additive in zeta^2, and the cross term is subleading
  of an order set by the decay of Ghat (Ghat ~ e^{-Delta/2} would give O(eps^{5/2}), invisible to a zeta^3 expansion).
W4 (order dependence, four intervals). Distinct corner measures: {p_2, p_3} (L->R), {p_3, p_4} (R->L), {2 x p_3}
  (middle-out = Protocol 3). VWZ symmetric setup (L_A = L_D, L_B = L_C, eta = a/(a+2b) -> 0): single step zeta = a/b ~ 2 eta;
  L->R: corners ~2 eta at p_2 and p_3 with Delta_23 = log((a+2b)/a) -> inf; Protocol 3: one corner 4 eta. Prediction
  Phi^(1) : Phi^(3) -> 1 : 4 UNCONDITIONALLY (Theorem A twice: Phi_A(a/b) vs Phi_A(2a/b)), and, CONDITIONAL on W2 with a
  remainder uniform in the separation and on Ghat(Delta) -> 0 as Delta -> inf (both open), Phi^(2) -> 2 Phi^(1); exactly
  Phi^(2)/Phi^(1) = (zeta_2^2 + zeta_3^2)/zeta_1^2 + (2 zeta_2 zeta_3/zeta_1^2) Ghat(log 1/eta)/Ghat(0). VWZ (5.10)-(5.11)
  and Fig. 25 (eta^2 up to 0.4, i.e. Delta_23 = log(1/eta) <~ 2.3): '-log F^(2) ~ -log F^(3) ∝ f' c eta^2 with f' < f,
  confirming that the sequential recovery is less effective than the single-step case' — the inequality and the prose
  point opposite ways; the calculus gives f'_3 = 4f exactly (given the corner calculus, open) and f'_2 = (2 + 2 Ghat(Delta)/
  Ghat(0)) f. Their single-step coefficient (2.13) f2 ~ 0.070 c is our ordinary-Petz prediction 8 f2 = 0.0675 c (zeta = 2z).
  Fig. 25 CANNOT be read as a measurement of Ghat (REF-P6-1, rigor/ref_p6_1_fig25.py): Delta_23 = log(1/eta) is bounded
  BELOW by their axis (eta^2 <= 0.4 gives Delta_23 >= 0.46), the corner strengths there are O(1) (zeta_1 = 2 eta/(1-eta)
  >= 0.22 at eta >= 0.1), so the second-order law does not apply, and Phi^(2) = Phi^(3) at second order would need
  Ghat(Delta_23)/Ghat(0) = 1.1 ... 2.1 > 1, which positive-definiteness forbids; no value or sign of Ghat may be extracted
  — G3 measures it directly. Middle-out is the worst order at second order with NO sign hypothesis: by Cauchy-Schwarz
  Phi^(2) <= f2 (zeta_2 + zeta_3)^2 < f2 (2 zeta_1)^2 = Phi^(3) since zeta_2 < zeta_1.
W5 (universality). W1 uses only Moebius covariance of the vacuum and the hsmi structure of Note 4: valid for every net for
  which the zero-collar map is the geometric compression (Theorem B's setting, implementer-hypotheses). Ghat is c-linear by
  the H_T argument of universality_theorem_B.tex; (H1)-(H3) for fields with finitely many second-derivative jumps
  (implementation_C11.tex; the Carpi-Weiner 3/2-norm is additive over jumps).
W6 (general sequential bound, type III). Bures-angle triangle inequality + FHSW data processing: arccos sqrt(F_tot) <=
  sum_steps arccos sqrt(F_step) for any sequential recovery of a normal state along a chain of von Neumann inclusions;
  second-order form Phi_tot <= (sum_k sqrt(Phi_k^(I)))^2, saturated iff all corners coincide. This is Note 3's "first
  theorem", with W2 showing when it is far from sharp.

## Tracks
G1a (analytic, Opus): rigor/network_corner_calculus.tex — W1 (with the normality of the composite: Note 4 Thm 7.1 per step),
  the amplification lemma, W3 sharp, W6, the exact reduction of Protocol 3 and the identity 1(B) = 1(A), the corner data
  of ALL one-sided protocols for n = 4 and n = 5 (which orders coincide), the twirled (t-averaged) variant as a mixture.
  Lamport; cited results with locators and screenshots (Note 4 Thm 7.1, paper 1 Def. zeta, Schwarzian rules).
G1b (analytic, Opus): rigor/network_second_order.tex — W2 (lower bound, multi-corner upper bound, three-way identity,
  global bound), Ghat as the Fourier transform of an explicit spectral density (closed form attempt by Note 7's three routes;
  NO fitting of closed-form candidates to numerics), positivity, decay rate, W5. Uses the conventions above; cites G1a's
  amplification lemma as a hypothesis until G1a is refereed.
G2 (numerical, Opus): numerics/networks/lattice_chain.py + NETWORK_RESULTS.md — sequential Gaussian Petz maps on the hopping
  chain (import numerics/lattice/petz_lattice.py; ball arithmetic); validation against exact 2^n density matrices, n <= 10;
  ALSO protocols with union conditioning regions (VWZ 1(B); the REF-P6-0 counterexample geometry) to test the general
  transformation rule of W1;
  production n <= 72: VWZ Protocols 1(A), 1(B), 2, 3 at L_A = L_D, L_B = L_C over a range of eta (1(B) = 1(A) as a pipeline
  check; the 1:2:4 prediction; Protocol 3 against Phi_A(zeta_eff) from paper 1's tables, lattice/two-branch ratio
  1 - 0.15/L in mind); L->R chains of 4-6 blocks: Phi_tot vs f2 sum (zeta_k^(I))^2 vs sum_k Phi_step (amplification);
  the VWZ CMI bounds (5.3)-(5.5) and sum_k I_k; equal-block chains Phi_tot(n_blocks); relative entropy alongside F.
G3 (numerical, Opus): numerics/networks/corner_kernel.py — Ghat(Delta)/Ghat(0) for Delta in [0, 8] by polarisation of g_Q in
  the T0 modular frame (f3_t0.py machinery: h-ladder 0.24 ... 0.03, Ymax >= Delta + 10, extrapolation as in F3, order check)
  and INDEPENDENTLY in the box frame (defect_matrix.py 'first' kernels for two corners in one box, i.e. (a', L') = (a + p',
  L - p') for the second corner, then compression_box.qfi_c2 polarised); agreement to 3 digits or a diagnosis
  (discretisation-faithfulness lesson; the T0 frame converges like h^0.77 and reaches g/f2 = 0.990 only at h = 0.02, so a
  1-digit disagreement is to be diagnosed, not reported as a failure); decay law and sign (nothing about Ghat can be read
  off VWZ Fig. 25, see W4); exact two-corner Phi at finite zeta (exact composite kernel:
  sqrt(Phi'(x) Phi'(y)) Q(Phi(x), Phi(y)) - Q(x,y) between different pieces) to measure the o(zeta^2) remainder of W2 and
  the clustering Phi_2 -> Phi_A + Phi_A at large Delta.
Rules: a KB card for every result (kb -p cft_cmi add ..., KB_ACTOR = G1a/G1b/G2/G3, tag phase6, area lattice-thermal);
  Opus referees afterwards (never Fable); file-first (skeleton, then <= 200-line appends, compile after each append); never
  run git; reason only to the next tool call; on a rate limit or output cap resume, do not relaunch.

## Environment
The Phase 5 venv is gone (session restart). Rebuild: V=<this session's scratchpad>/venv; python3 -m venv $V &&
$V/bin/pip install numpy scipy mpmath python-flint cvxpy clarabel scs pymupdf. Long jobs: nohup $V/bin/python x.py > x.out
2>&1 < /dev/null & disown; outputs stay in numerics/networks/. No `timeout` binary on this Mac; use absolute paths.
