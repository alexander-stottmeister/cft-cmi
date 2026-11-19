# C5 report — Networks (Phase 6), second independent referee
Actor REF-COUNCIL-C5. Scope: rigor/network_corner_calculus.tex, rigor/network_second_order.tex; cards corner-calculus,
network-law-free-fermion, corner-kernel-closed-form, network-upper-uniform-two-corners, network-law-c-linear,
network-global-bound-coincident, vwz-protocol-ordering. KB read-only.

## 1. Verdict table
Seat C5, second independent referee of Phase 6. Burden of proof on the documents. No BREAK found.
| Theorem (file:label) | Card | Verdict |
|---|---|---|
| network_second_order.tex lem:taylor | network-law-free-fermion | STANDS |
| thm:T1 (lower bound, with lem:frame, lem:canon, lem:implementer, lem:Dtot, lem:polar) | network-law-free-fermion | STANDS |
| lem:prodexp, prop:inf, thm:T2 (product of flows) | network-law-free-fermion | STANDS |
| cor:law (fixed configuration) | network-law-free-fermion, network-second-order-law | STANDS |
| lem:nogroup, thm:T3 (after R1) | network-global-bound-coincident | STANDS (deps warning spurious, MINOR) |
| thm:T4 (a)-(e), closed form | corner-kernel-closed-form | STANDS (recomputed, section 8) |
| lem:onegroup, thm:T5 | network-upper-uniform-two-corners | STANDS WITH REPAIR (MINOR: product term in <2>2, l. 1018) |
| cor:vwz | network-upper-uniform-two-corners, vwz-protocol-ordering | STANDS |
| thm:T6 | network-law-c-linear | STANDS for the geometric-compression product; CARD over-states "Petz chains" (GAP, wording) |
| network_corner_calculus.tex lem:compose, lem:same-schwarz, thm:general, thm:corner | corner-calculus | STANDS |
| thm:state, cor:phiA | corner-calculus | STANDS (MINOR: normality sentence at l. 901) |
| lem:2pt, lem:F1, thm:rigidity | corner-calculus (item 4) | STANDS |
| prop:prot2 and the Protocol 1(A) corner data used by cor:vwz (prop:1B1A itself not re-checked) | corner-calculus, vwz-protocol-ordering | STANDS (exact check; VWZ source matched) |
Findings, most severe first:
1. [GAP, card wording] KB cards network-law-c-linear and network-second-order-law say the c-linear law covers "all
   L->R Petz chains"; rigor/network_second_order.tex l. 1099-1100 proves it for steps that ARE the geometric
   compression; Petz = geometric compression is proved only for the free fermion (petz-zero-collar-channel).
2. [MINOR] network_second_order.tex l. 1018-1019 (thm:T5 <2>2): the remainder bound omits the term
   Tr(A_2* R_1* B_1 R_2) <= s^2 zeta_1 zeta_2 eta(s zeta_1) eta(s zeta_2); o(s^2) uniformly, theorem unaffected.
3. [MINOR] `kb deps` marks network-global-bound-coincident "modulo group-index-zero-large-s,
   pushforward-blocks-equal-singular-values"; thm:T3 uses neither (section 7).
4. [MINOR] card vwz-protocol-ordering: second-order coefficients of the scaled family written as inequalities
   between Phi(2), Phi(3) (section 7).
5. [MINOR] network_corner_calculus.tex l. 901-904: passage from C*-level equality to F(J_N) needs "both states
   normal by (1)" stated.

## 2. thm:T1 and lem:taylor (replacing analyticity)
Read: rigor/network_second_order.tex l. 445-538 (lem:taylor, thm:T1), l. 288-443 (lem:frame, lem:canon,
rem:scaled, lem:implementer, lem:Dtot, lem:polar), PA rigor/uhlmann_upper_bound.tex prop:expansion l. 757-797.

lem:taylor (l. 450-489): STANDS. Checked step by step:
- <1>1 f(Z) = -log F(omega_X, omega_Z) is real-analytic on the open set {0<Z<1}: with rho_X fixed and faithful,
  F = Tr (rho_X^{1/2} rho_Z rho_X^{1/2})^{1/2}, the square root of a positive-definite matrix is analytic, F > 0.
- <1>2 Df(X) = 0 (interior minimum of f >= 0, f(X) = 0). <1>3-<1>4: Bures box -log F = eps^2 g_B/8 + O(eps^3)
  gives D^2 f(X)[Z,Z] = g_B/4; consistent (f = eps^2/2 D^2f).
- <1>5-<1>6: C^3 Taylor remainder on a ball, H_s = s Ydot + o(s) in operator norm: f(Y_s) = s^2/2 D^2f[Ydot,Ydot]
  + o(s^2). Correct; only first-order differentiability of s -> Y_s is used, as claimed.
- <1>7: the Legendre bound. Independent check (eigenbasis of X): sup_l [2 Tr(Ydot l) - Tr(X l (1-X) l)]
  = 2 sum_ij |Ydot_ij|^2 / N_ij, N_ij = x_i(1-x_j)+x_j(1-x_i), attained at l = 2 Ydot/N; this is <= g_B (QL
  Prop 3.3), so the inequality direction is the one T1 needs (a LOWER bound on Phi_P).
thm:T1 (l. 491-538): STANDS. Direction ledger: <1>3 data processing (Phi_tot >= Phi_P, lower bound, exact
quantity, restriction to the finite CAR algebra M_P, omega_s normal by lem:implementer(iv)); <1>6 lem:taylor
(equality of the s^2 coefficient of Phi_P, then a lower bound by the Legendre form); <1>2 sup over finite rank l
of Omega_tot = 8 g_Q(D_tot) ([K2](i)). Every direction is "lower bound on the exact Phi_tot". liminf >= each
Omega_tot(l)/8, hence >= sup. <1>4: 0 < X, Y_s < 1 on the finite-dimensional PH holds because 0 < Q_J < 1 has no
eigenvector with eigenvalue 0 or 1 and PH is finite-dimensional (compression keeps strict bounds). <1>7: I
recomputed Tr_{PH}(PQP l (1-PQP) l) = Tr(Q l (1-Q) l) for l = PlP: both equal Tr(PQP l^2) - Tr(PQP l PQP l).
lem:Dtot (the input of <1>5): STANDS. lem:implementer <1>1 rechecked: chi = x^2 on [0,1] and chi >= 0 makes the
flow move points of (0,1) leftwards inside [0,1), so kt_s|_I = R_{0,s}; d_k affine with slope 1-q_k, and
conjugating R_{0,sigma} by an affine map of slope lambda gives R_{q, sigma/lambda}: parameter s zeta_k/(1-q_k)
= s kappa_k. Correct. <1>2 cites PA prop:expansion <1>2 (||G_s - s G^(1)||_2 <= s eps(s)), present at PA l. 771.
<1>3 (U_k(s) -> 1 strongly, hence conjugation of a fixed HS operator converges in ||.||_2) is correct.
[MINOR] network_second_order.tex l. 211 ([K2](v)) and lem:taylor <1>3 cite the Bures box for "C^3 curves of
faithful finite-dimensional states"; lem:taylor uses it on the analytic straight line X + eps Z only, so the
hypothesis is met; no repair needed beyond noting it.

## 3. thm:T2: product of flows, prop:inf
Read: network_second_order.tex l. 540-657 (lem:prodexp, prop:inf, thm:T2, cor:law).
lem:prodexp: STANDS. <1>2 rederived: W*P_- W = P_- + G_tot, so W* P_- W e^{ish'} P_+ = Z_s + G_tot P_+ +
G_tot P_+(e^{ish'}-1)P_+ + G_tot P_- e^{ish'} P_+ (insert 1 = P_+ + P_- after G_tot; P_- P_+ = 0). The last two
terms are O(s^2) since ||G_tot||_2 <= C_0 s sum zeta_k and ||e^{ish'}-1|| <= s mu, ||P_- e^{ish'} P_+|| <= s mu.
<1>4 uses lem:Dtot <1>4 (o(s) for G_tot - s sum zeta_k T_k), correct.
thm:T2 <2>2 (Uhlmann): STANDS. I checked the point a first referee may skip: Gamma(e^{ish'}) commutes with
F(I) (not only with its even part), because Gamma(u) a(f) Gamma(u)* = a(uf) = a(f) for f in H_I when u = 1 on
H_I; so Gamma(U_s)* Omega and Gamma(W_tot)* Omega represent the same state omega_s on F(I), and
F(omega, omega_s) >= |<Omega, Gamma(U_s) Omega>|. <2>3 (thm:det): the hypothesis ||P_+ U_s P_-|| < 1 is what
makes P_+ U_s P_+ invertible (both it and its adjoint are bounded below), i.e. index zero; it is supplied by
lem:prodexp(ii). Unlike T3/T5 no group index lemma is needed here. Direction: upper bound on the exact Phi_tot.
prop:inf: STANDS. The chain uses D_tot only through P_- D_tot P_+ in S_2 and linearity of the commutator; the
value 2 g_Q(D_tot) = (1/4) sup Omega_tot is consistent with the single-corner normalisation: g_Q(D^(1)) =
(1/4)(1/(3 pi^2)) = 1/(12 pi^2) = Ghat(0), and T1 (liminf >= g_Q) meets T2 (limsup <= (1/2) 2 g_Q = g_Q).
<1>1 imports PA's identification dist(a, closure K) = dist(a, H_{F(I)'}) (three faces); for the fermion the
algebra is the field algebra F(I) and the commutant is the plain commutant F(I)', which is what PA's three-faces
uses; the trial h' (supported in I') gives elements of F(I)', consistent.
cor:law: STANDS as stated (fixed configuration, no uniformity). Note (MINOR, wording only): for a protocol the
"scaled family" at s < 1 is not a family of recovery maps (C8, l. 155-162 says so); cor:law is therefore a
statement about a mathematical interpolation, and its physical content is only through T5/cor:vwz and the
uniformity question. The card network-law-free-fermion says "carries the recovered state of the scaled family",
which is accurate.

## 4. thm:T6: use of Theorem B
Read: network_second_order.tex l. 1089-1154; rigor/universality_theorem_B.tex (S4) l. 117-160, prop:H3
l. 290-357, rem:H2H3 l. 358-367, prop:H2 l. 392-418. Cards thm-b-universality [refereed],
implementer-hypotheses [refereed], petz-zero-collar-channel [proved].
thm:T6: STANDS (for the object it defines: omega o Ad U(s) with U(s) the canonical product (eq:Ugen) of
geometric-compression implementers).
- <1>1/<1>2 (H2) for the product: rederived the induction. U(s)* Omega = U^(M)* ... U^(1)* Omega; at each stage
  U^(m+1)*(Omega - i s sum_{k<=m} zeta_k a_k + o(s)) = Omega - i s zeta_{m+1} a_{m+1} - i s sum_{k<=m} zeta_k a_k
  - i s sum_{k<=m} zeta_k (U^(m+1)* - 1) a_k + o(s), the last term s.o(1) by strong continuity. Correct.
  U(s) implements Psi_s: Ad U^(1)...U^(M) maps A(K) to A(R_1(...R_M(K))) = A(Psi_s(K)), canonical order (C6). OK.
  Ad U(s) on A(I) does not depend on the chosen extensions: two implementers of extensions agreeing on I differ by
  U(phi) in A(J_s') which commutes with the image algebra A(J_s) (TB l. 180-204); this applies factor by factor.
- <1>3: I checked the claim "no group property is used". prop:H2 uses only Psi_s = U_s* Omega and (H2)
  (l. 398-410). prop:H3 uses (H3) on a *-strongly dense algebra and <a, Omega> = 0 (l. 345); rem:H2H3 derives
  (H3) from (H2) by expanding <Psi_s, X Psi_s> (l. 358-362), again no group property. For a_tot:
  <Omega, Delta^{i tau} a> = <Delta^{-i tau} Omega, a> = <Omega, a> = 0. Confirmed.
- <1>4: a_k = Delta^{i tau_k} T(g) Omega lies in H_T (H_T is Delta^{it}-invariant, TB lem:reduce(3)); the
  reduction of TB thm:linear uses only a in H_T and Im<Omega,a> = 0. Confirmed at the level of the cited proof
  structure; the c-linearity itself is inherited from TB (seat C2's scope).
- <1>5: the free-fermion evaluation: T(f)Omega = P_-(-i L_f)P_+ is linear in f, L_g = -Dc (g = -chi), and the
  fermion modular group acts on H^(1,1) by conjugation with W_{d_t}; so a_tot = i P_- Dc_tot P_+ and
  (1/4) g_B = 2 g_Q(D_tot) by prop:inf. The step inherits TB's use of the GRADED (field) net of the fermion as a
  "net" for which thm:linear holds (TB thm:value <2>2); on H_T (even sector) the twist acts trivially, so the
  modular data restricted to H_T are geometric. No new issue; inherited from thm-b-universality.
- Sign of the modular flow: (C2)/T6 put Delta_I^{i tau} = dilation u -> e^{2 pi tau} u about the endpoint 1 of
  the LEFT half-line I = (-inf,1); this is the BW direction for a left half-line. Even with the opposite sign the
  stated formula would be unchanged (Ghat is even), so the value is robust; the implementation claim <1>2 needs
  the sign as stated, and it is.
[GAP, card wording] KB card network-law-c-linear, Statement: "Covers every protocol whose steps are right
compressions in the canonical order (all L->R Petz chains, VWZ Protocols 1(A) and 2)". For a general net the
document proves the law only for steps that ARE geometric compressions ("when every step map is the geometric
compression (the setting of W5 and of TB)", network_second_order.tex l. 1099-1100). That the ordinary
(or zero-collar) Petz map of a general net is the geometric compression is proved only for the free fermion
(card petz-zero-collar-channel; thm-b-universality is about the geometric compression, not the Petz map).
"Petz chains" in the card is therefore stronger than the document for c not a free-fermion value. Repair: replace
"all L->R Petz chains" by "all L->R chains whose step maps are the geometric compressions (for the free fermion:
the Petz chains, by petz-zero-collar-channel)". Inheritance: any paper sentence asserting the network law for
Petz recovery in a general CFT (seat C6 to check against paper2/*.tex).

## 5. thm:state (state depends only on the Schwarzian)
Read: network_corner_calculus.tex l. 833-968 (lem:moebius-inv, thm:state, rem:caveat, cor:phiA), lem:same-schwarz
l. 569ff. thm:state: STANDS.
- (1) Order: the recovered state on F(J_N) is omega o beta_1 o ... o beta_N (step 1 acts last in the Heisenberg
  picture), and beta_{V_k1} beta_{V_k2} = beta_{V_{k1 o k2}}, so Phi = k_1 o ... o k_N (first step outermost)
  is the right composite. Each step is the zero-collar map of its OWN inclusion (A = J_{m-1} minus A_B, B = A_B,
  C = A_new); Note 4 Thm 7.1 needs s_m >= lambda_m = l_new/l_B, i.e. h_s(D) inside B; the ordinary Petz value
  s = 2 lambda satisfies it. Normality of the composite comes from composing normal maps, not from Thm 7.1
  applied to Phi (rem:caveat(i)); correct.
- (2)/(3): equality is first proved on the CAR C*-algebra (two-point functions: V_g unitary on all of H and
  [V_g, P] = 0), then extends to F(J_N) because both states are normal and agree on a weakly dense
  *-subalgebra. The proof writes only the C*-level identity; the passage to the von Neumann algebra uses
  normality from (1). [MINOR] network_corner_calculus.tex l. 901-904 (<1>4): the sentence should say that both
  states are normal (by (1)) so that C*-level equality gives equality on F(J_N); one line.
- lem:same-schwarz (independent re-derivation): g := Phi_2 o Phi_1^{-1} is C^1 piecewise Moebius on Phi_1(J);
  by the composition rule Sch(g) = 0 as a measure, so every jump of g''/g' vanishes and adjacent Moebius pieces
  agree to second order at the breakpoint, hence coincide (a Moebius map is fixed by its 2-jet). Correct.
cor:phiA (single corner, depends only on zeta and not on the side): STANDS; L = G o R with G Moebius rechecked
in the coordinate w = 1/(x-p).

## 6. cor:vwz
Read: network_second_order.tex l. 1035-1087 (cor:vwz), l. 955-1033 (lem:onegroup, thm:T5), G1a prop:prot2.
Corner data rechecked by hand (independent derivation from the protocol definitions, frame I = (0, 2a+2b)):
Protocol 1(A) = start AB, condition on B, add CD: lambda = (a+b)/b, ordinary Petz s = 2 lambda, sigma =
s/(b+b+a) = 2(a+b)/(b(a+2b)), beta_I(p_2) = a(a+2b)/(2(a+b)), zeta_1 = a/b. Protocol 2 (L->R): step 1 (B, add C)
lambda = 1, sigma_2 = 2/(2b) = 1/b, corner p_2; step 2 (C, add D) lambda = a/b, sigma_3 = (2a/b)/(a+b),
corner p_3; composite R_{p2} o R_{p3} = canonical order; zeta_2 = a(a+2b)/(2b(a+b)), zeta_3 = (a+b)/2 . sigma_3 =
a/b; y_3 - y_2 = log((a+2b)/a) = log(1/eta). Restriction to J = (p_2, p_5): zeta^(J) = sigma_3 b(a+b)/(a+2b) =
2a/(a+2b). All as in the document (script check in section 8).
Direction ledger: upper half = T5 upper bound on the exact Phi^(2) divided by Theorem A (two-sided asymptotic
equality) for Phi^(1); lower half = data processing (exact lower bound on Phi^(2)) by Phi_A(2s/(s+2)), divided by
Theorem A. Every direction needed holds for the exact quantities. cor:vwz: STANDS.
Point a first referee may miss: the configuration (y_3 - y_2 = log((s+2)/s)) moves with s = a/b, so cor:law
(fixed configuration) would NOT suffice; the proof correctly uses T5's uniformity in the positions, with the
rescaled strengths (zeta_2/s, 1) in the compact Z = [3/4,1] x {1}. Correct.
thm:T5: STANDS WITH (MINOR) REPAIR. lem:onegroup (i)-(iii) rederived: P_- U P_+ = U G P_+, G_sigma =
int_0^sigma U*[P_-,K]U, [P_-,K]P_+ = k; in the index-zero range ||P_- U P_+||_2^2 = (1/2)||G||_2^2 <=
sigma^2 ||k||_2^2 (||[P_-,K]||_2^2 = 2||k||_2^2 for skew K). <1>2-<1>3: tau_t commutes with the real projection
Pi because W_{d_t} preserves A' (d_t(I') = I') and commutes with P_+-; a SINGLE h' (depending on delta only)
serves all positions: this is what makes the bound uniform in y. <2>3 checked: k_{y2}(A_2 - P_+)* =
k_{y2}(U^(2)* - 1)P_+ and k_{y1}*(B_1 - P_-) = k_{y1}*(U^(1) - 1)P_-, each conjugated by the same W_{d_y} as its
own k, so the bound is y-independent. Uhlmann step: U^(1)U^(2) restricted to H_I equals V_{Psi_s} (each
e^{sK} = Wt_s c_s with c_s = 1 on H_I, RR prop:rrr), so prop:vector applies.
[MINOR] network_second_order.tex l. 1018-1019 (thm:T5 <2>2): the stated bound
s^2 zeta_1 zeta_2 ||k||_2 [eta(s zeta_1) + eta(s zeta_2)] omits the product term Tr(A_2* R_1* B_1 R_2), of size
<= s^2 zeta_1 zeta_2 eta(s zeta_1) eta(s zeta_2). It is o(s^2) uniformly, so E(s) -> 0 still holds and the
theorem is unaffected; repair: add eta(s zeta_1) eta(s zeta_2) to E(s).

## 7. Other theorems (corner calculus, closed-form kernel, global bound)
G1a (network_corner_calculus.tex):
- lem:compose, lem:same-schwarz (l. 538-605): STAND (re-derived, section 5). thm:general (l. 622-656): STANDS; the
  rule only sees breakpoints of k_1 inside G_1(J_N), hence swallowed corners contribute nothing; masses are
  pulled back with factor G_m'(x_m) (composition rule for a point mass: (g')^2 delta_r o g = g'(x) delta_x).
- thm:corner (l. 658-710): STANDS. <2>2-<2>3 is the crux: an earlier corner can meet a later closed moving part
  only at the later corner itself (the far end f_{m'} lies outside the closure of J_{m'-1}); (H) excludes the
  interior. Then every G_m fixes p^(m) with derivative 1.
- thm:rigidity (l. 1041-1100): STANDS. Off-diagonal two-point kernels plus lem:2pt give Moebius; all masses
  negative so no cancellation; the last corner is interior when the last step keeps a non-empty part.
- prop:prot2, prop:1B1A (used by cor:vwz): corner data reproduced in exact arithmetic (section 8, K5) and the
  protocol definitions checked against the source: VWZ arXiv:2307.14434, Sec. 5 (pdf p. 43-46; extracted with
  pdftotext): Protocol 1(A) = Fig. 1 with CD in the role of C (start AB, P_{B->BCD}); Protocol 2 = start AB,
  P_{B->BC}, then P_{C->CD}; Protocol 3 = start BC, P_{B->AB}, then P_{C->CD}; "lambda = 0 for each Petz map"
  (ordinary Petz); eta (5.9) = L_A(L_C+L_D)/((L_A+L_B)(L_B+L_C+L_D)) = a/(a+2b) for L_A=L_D=a, L_B=L_C=b. All
  match the documents.
network_second_order.tex:
- thm:T4 (a)-(e) (l. 749-947): STANDS; recomputed independently (section 8): the v-integral S(u) from the KI
  kernel as printed, the Fourier integral of rho, the closed form and the series agree; the bounds of (d) and
  the monotonicity/positivity of (e) hold on a grid; the card's five ratios reproduce. Not C^2 at 0: Ghat''(0)
  would be -int rho q^2, and rho q^2 ~ 1/(48 pi^2 |q|) is not integrable; C^1 since int rho |q| < inf. Agrees.
- thm:T3 (l. 688-733): STANDS (after Correction R1, applied). <1>5 rechecked: ||P_- AB P_+||_2 <=
  ||P_- A P_+||_2 + ||P_- B P_+||_2 for unitaries; each factor in the index-zero range of RR C3(ii)
  (rate_of_remainder.tex l. 1069-1079: ||G_s||_2 < 1 makes both blocks of norm < 1, so P_+ U P_+ is invertible).
  <1>6: det(1 - V*V) >= 1 - ||V||_2^2. <1>7: inf ||P_- K P_+||_2^2 = g_B/4 = 2 f2hat.
- lem:nogroup (l. 664-686): STANDS (mass at q_2 of Psi_s o Psi_t is -2 t kappa_2 since Psi_t^{-1}(q_2) != q_2).
[MINOR, bookkeeping] card network-global-bound-coincident is shown by `kb deps` as "proved . modulo
group-index-zero-large-s [conjectural], pushforward-blocks-equal-singular-values [heuristic]", inherited through
the whole-card edge to rate-of-remainder. thm:T3 uses neither: it uses RR lem:groupbound, prop:rrr and the
small-norm index argument C3(ii) only, for e^{sK} with K = Dc + ih' (not a push-forward, so the heuristic
conjugation argument would not even apply), and it is restricted to s zeta_max < pi sqrt 3. The warning is not a
real gap for this card (nor for network-upper-uniform-two-corners, which inherits it); a dated note saying so
would clear it. Same pattern for any other network card whose only path to the weak links is rate-of-remainder.
[MINOR, card wording] vwz-protocol-ordering (conjectural): "At second order and fixed geometry: Phi(2)/Phi(1) =
... and middle-out is the worst order: Phi(2) <= f2 (zeta_2+zeta_3)^2 < f2 (2 zeta_1)^2 = Phi(3)". These are
second-order coefficients of the SCALED family (s -> 0 at fixed geometry), not values at the protocols' own
s = 1; written as equalities/inequalities for Phi(2), Phi(3) they read stronger than proved. What IS proved for
the actual protocols: limsup Phi(2)/Phi(3) <= 1/2 as a/b -> 0 (T5 for Phi(2), Theorem A for Phi(3) =
Phi_A(2a/b)). Suggest rewording "second-order coefficients of the scaled family".

## 8. Independent numerical checks
Script rigor/council/c5_kernel.py, output rigor/council/c5_kernel.out. Command (repository root):
`${PYTHON:-python3} rigor/council/c5_kernel.py > rigor/council/c5_kernel.out` (system python3: mpmath, scipy;
the scratchpad venv had no numpy at run time and was not touched). Written from the printed formulas only, no
code shared with rigor/g1b_kernel.py. Tolerances fixed in the docstring before the run. Result: OVERALL PASS.
- V0 (validation, exact case): int rho = 1/(12 pi^2) = 0.008443431970194814287, rel. deviation 0 (tol 1e-12).
- K1: Ghat(Delta) by mpmath quadosc of the Fourier integral, by the boxed closed form and by the series, at
  Delta = 0.1, 0.5, 1, 2, 4, 8, 12: max |diff|/Ghat(0) <= 6.1e-29 (tol 1e-10).
- K2: S(u) = int |D^(1)|^2/N dv computed from the KI kernel (eq:KI) as printed, v in [-150,150] (cut-off weight
  < 1e-28), against (2/3) tanh(u/2)/(u(u^2+4 pi^2)) at u = 0.3, 1, 2.5, 6, 15: max rel. deviation 7.5e-13 (tol
  1e-7). This checks [K2](ii) and hence the density rho independently of QL.
- K3: thm:T4(d) bounds and (e) positivity/strict decrease at Delta = 1/8, 2/8, ..., 10 (80 points, 30 digits):
  all hold.
- K4: card corner-kernel-closed-form ratios Ghat/Ghat(0) at Delta = 0.5,1,2,4,8 = 0.8983865801, 0.7456151411,
  0.4769603380, 0.1797843036, 0.02441921332; max |diff| to the card = 4.1e-8 (tol 6e-8, card gives 7 decimals).
- K5: cor:vwz corner data (zeta_1 = a/b, zeta_2 = a(a+2b)/(2b(a+b)), zeta_3 = a/b, e^{y_3-y_2} = (a+2b)/a,
  zeta^(J) = 2a/(a+2b)) as exact rational identities for 200 random (a,b): all hold.
Not computed: no instance of T1/T2/T5 (an infinite-dimensional fidelity) was recomputed; the lattice cards are
outside this seat.

## 9. Inheritance (kb deps)
- [GAP, card wording] "all L->R Petz chains" for general c: cards network-law-c-linear (Statement) and
  network-second-order-law (Statement, "c-LINEAR / UNIVERSAL" clause, which repeats it); the parent summary card
  multi-interval-networks says "c-linear for canonical-order protocols under Theorem B's hypotheses" (fine).
  Paper statements: none found; paper2/sec_outlook.tex l. 36-42 (Networks of intervals) predates Phase 6 and
  under-claims (it calls the off-diagonal Hessian entries future work) -- for seat C6.
- [MINOR] thm:T5 <2>2 missing product term: no card statement changes (network-upper-uniform-two-corners,
  vwz-protocol-ordering unaffected).
- [MINOR] spurious "modulo" on network-global-bound-coincident -> network-upper-uniform-two-corners (via
  depends), vwz-protocol-ordering (ev:). No real gap.
- Inherited from outside this seat (not re-refereed here): T6 rests on thm-b-universality (c-linearity, the use
  of the graded fermion net in TB thm:value) and implementer-hypotheses (seat C2); T3/T5 rest on RR C3(ii) and
  T1/T2 on PA/QL (seat C1); cor:vwz and the protocol states rest on petz-zero-collar-channel (seat C3).

## 10. Earlier referee reports: were repairs applied?
- referee_network_second_order.tex (REF-P6-4): R1 (T3 range s zeta_max < pi sqrt 3) present in the theorem
  statement l. 689-692 and in <1>5/<1>7; R2 (lem:onegroup(i) range) present l. 957; R3 (T5 third side
  condition) present l. 1003-1005; R4 (T4(e) C^1 not C^2) present in the statement; [K4] box keeps RR's verbatim "for all s" (l. 245) but its Verdict
  restricts the use to the index-zero range (l. 249-254). The card network-global-bound-coincident carries the restricted range. All applied.
  REF-P6-4 did not record the omitted product term of T5 <2>2 (section 6) -- new, MINOR.
- referee_network_corner_calculus.tex (REF-P6-3): derivative G_m'(x_m) in the card and in thm:general
  (eq:general-rule); pole on the OPEN interval in lem:same-schwarz with the counterexample; interior junctions in
  thm:corner; "last step keeps a non-empty part" in thm:rigidity and rem:degenerate. All applied.

## 11. NOT DONE
- No independent recomputation of an infinite-dimensional instance of T1/T2/T5 (e.g. a finite-rank-P lower
  bound or a product-trial upper bound for M = 2 at fixed s): reason, budget; the kernel, the corner data and
  the closed form were recomputed instead.
- Upstream results were checked only at the interface (statement and hypotheses as used): PA prop:expansion,
  prop:infimum, lem:tangentvec; RR lem:groupbound, C3(ii); TB thm:linear, thm:value; C11 thm:main;
  Note 4 Thm 7.1. Their proofs belong to seats C1-C3.
- G1a sections not in the brief's focus were not re-refereed: prop:H-suff, Prop 9.1/Lem 9.2 (holonomy classes,
  n = 4, 5 tables), thm:sep, thm:w6/w6chord, prop:twirl, lem:LRdata.
- The lattice cards (lattice-*) and their scripts were not rerun (outside this seat).
- KB untouched (read-only council); no git.
