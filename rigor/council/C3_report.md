# C3 Foundations — council report (REF-COUNCIL-C3, adversarial referee)

Scope: continuum_petz_free_fermion.tex (Note 4, Thm 7.1), fidelity_recovered_quasifree.tex (Note 5, Thm 2.1/3.1/3.2),
rigor/check_note4.tex, rigor/check_note5_theory.tex, rigor/collar_and_invariant_formula.tex,
adjacent_interval_cmi_longo_xu.tex; cards petz-zero-collar-channel, quasi-free-fidelity-formula, longo-xu-cmi,
cmi-markov-defect-interpretation, phi-derivative-nondecreasing, two-chirality-*.
Key question: is the zero-collar Petz map a well-defined normal map on the type III algebra, and is
Phi = -log F given by the determinant formula there, with every limit justified?

## 0. Cards read and their status
Read with `kb -p cft_cmi show`: petz-zero-collar-channel [proved, passed REF-DEP-CFT-B4], quasi-free-fidelity-formula
[proved, passed REF-DEP-CFT-B2], longo-xu-cmi [proved], cmi-markov-defect-interpretation [proved],
phi-derivative-nondecreasing [refuted], two-chirality-law [proved], two-chirality-minimum-at-lambda-zero [conjectural],
two-chirality-law-general-cft [conjectural]. Sources opened: refs/Araki77_PRIMS13.pdf (Thm 3.8, 3.9, via pdftotext,
pp. 181-182), further sources listed per item below.

Answer to the key question (details in sections 1-2):
* Well-definedness: YES. beta-bar_s, s >= lambda, is a normal *-isomorphism F_r(I) -> F_r(J_s) (Note 4 thm:normal-extension,
  continuum_petz_free_fermion.tex:730-747); the route (one-particle unitary W_s: H_I -> H_{J_s}, Bogoliubov
  *-isomorphism CAR(H_I) -> CAR(H_{J_s}), Powers-Stormer quasi-equivalence from the trace-class defect, Reeh-Schlieder
  for the GNS identification) is sound. The zero-collar map is a normal unital *-homomorphism, hence a channel.
* Phi = -log F on the type-III algebra: given ONLY as a monotone limit of finite-dimensional determinant formulas
  (Note 5 thm:det-rep, fidelity_recovered_quasifree.tex:294-330), not as a closed infinite-dimensional determinant;
  the limit is justified (Note 4 lem:fidelity-below for F, Araki77 Thm 3.9(2) for D). See section 2 for the
  residual items.

## 1. Verdict table
(N4 = continuum_petz_free_fermion.tex, N5 = fidelity_recovered_quasifree.tex; line numbers of the files as of 2026-11-19.)

| # | Theorem | Verdict | Step / reason |
|---|---|---|---|
| 1 | N4 thm:trace-norm (6.2), l. 670-690: ||R_s||_1 = (1/2)log(1+zeta) | STANDS | independently recomputed (sec. 5, R1): 4 parameter sets, rel. dev. <= 6e-13 |
| 2 | N4 thm:normal-extension (7.1), l. 730-747 | STANDS | quasi-equivalence route checked: PS inequality (eq:powers-stormer) + PS-Araki criterion; the pulled-back rep pi o beta_s is the GNS rep of omega~_s because Omega is cyclic for F(J_s) (Reeh-Schlieder) and W_s maps H_I ONTO H_{J_s}; range F(J_s) because beta_s(CAR(H_I)) = CAR(H_{J_s}). See F4 (MINOR) |
| 3 | N4 lem:tensorization, l. 418-441 | STANDS (MINOR F5) | FHSW hypotheses (rho, sigma normal, sigma faithful; FHSW Thm 1, refs/FHSW20 eq. (24)-(25)) met by sigma_eps = omega_A x omega_D (faithful product). Klein bookkeeping only asserted (l. 412-414); I checked it (F5) |
| 4 | N4 eq:s-t derivation, l. 318-338 | STANDS | Delta_N^{-it} U(2 lambda) Delta_M^{it} = U(lambda) U(e^{-2 pi t} lambda) = U(s_t) rederived from the +hsm relation and Delta_N = U(lambda) Delta_M U(lambda)^* |
| 5 | N4 lem:fidelity-below, l. 855-878 | STANDS | Alberti variational formula (AlbertiUhlmann02 Thm 2); Kaplansky for the *-algebra union, functional calculus clamps spectra to [m, M_0], inversion continuous there; bounded strong convergence -> normal states converge |
| 6 | N4 eq:fixed-t-integrated-bound and eq:zero-collar-fidelity, l. 880-912 | STANDS | eps -> 0: integrand increases pointwise (M_eps increasing; union generates F_r(I) since L^2(I) = L^2(-a,0) + L^2(0,L) for the free fermion), monotone convergence licensed; concavity used in integral form, which follows from the inf-formula (inf of an integral >= integral of inf) |
| 7 | N5 thm:finite-fidelity (2.1), l. 225-243 | STANDS | independently recomputed against brute-force Jordan-Wigner density matrices (sec. 5, R2): |diff| <= 8e-38 |
| 8 | N5 thm:det-rep (3.1), l. 294-330 | STANDS (MINOR F3, F13) | F: lem:fidelity-below applies (M_n finite-dimensional factors, increasing, union strongly dense). D: Araki77 Thm 3.9(2) ("If N_alpha is an AF algebra for all alpha, then lim S(E_N psi/E_N phi) = S(psi/phi)", refs/Araki77_PRIMS13.pdf p. 181-182; proof p. 190 via Thm 3.9(1) and 3.8(2)(gamma)) - hypotheses met. Strict 0 < Q_n < 1 argued correctly (l. 314) |
| 9 | N5 lem:mobius (1.1), l. 200-221 | STANDS (MINOR F6) | the glued construction is determined by (g(A), g(D), the parabolic fixing g(0) with g(L) -> g(L/(1+s))), unique; 4 ordered points have one invariant |
| 10 | rigor/check_note5_theory.tex prop:mono (8.1), l. 1233-1258: Phi and D nondecreasing | STANDS (MINOR F7) | isotony + uniqueness of the normal extension (k_s independent of a) + data processing; <1>5 realises any zeta_1 < zeta_2. beta-bar_s exists for every s > 0 (s >= lambda only places the range in AB), so <1>5's choice s > zeta_2 is legitimate |
| 11 | N5 cor:collapse (5.1), l. 409-420 | STANDS | zeta(s_t) = z(1+e^{-2 pi t}) rederived (L = b+c) |
| 12 | check_note5_theory.tex prop:chirality <1>1-<1>7, l. 1369-1411 (card two-chirality-law) | STANDS (MINOR F8) | independently rederived: the left chirality on (0,L) is, by parity, the right chirality on (-L,0), a hsm inclusion of the opposite type; the ordinary Petz map is the same point map h_{2 lambda}, the modular flow is reversed, so alpha^-_t = alpha^+_{-t}, s^-_t = lambda(1+e^{2 pi t}). <1>6 particle-hole: omega_Q -> omega_{1 - conj Q}, checked. <1>8 (minimum at 0) correctly withdrawn |
| 13 | N4 eq:LX-MI, eq:delta-eps, eq:CMI-LX (l. 785-812); adjacent_interval_cmi_longo_xu.tex eq:abc-formula (l. 254); card longo-xu-cmi | STANDS | rederived: LX Thm 3.18 + G of Thm 4.1(4) (refs/LongoXu p. 20-21) give MI_r(I_1,I_2) = (r/6) log[(a2-a1)(b2-b1)/((a2-b1)(b2-a1))]; delta_eps and its eps -> 0 limit (r/6) log(1+z) recomputed by hand. Normalisation r/6 with c = r confirmed from the source: LX Sec. 3.1 (p. 9) generate A_r(I) by c(xi) = a(xi) + a(xi)^*, xi in the COMPLEX space L^2(I, C^r), i.e. the full CAR algebra of r complex fermions (c = r); see F15 |
| 14 | check_note4.tex prop:limit (11.4, l. 1554-1578) = N4 eq:fixed-t-integrated-bound | STANDS | FHSW Thm 1 (refs/FHSW20 eq. (24): rho, sigma normal, sigma faithful; root fidelity (23)) applies at eps > 0; direction: CMI >= -2 int p log F, an upper bound on the averaged recovery error - the only direction used downstream (card phi-derivative-nondecreasing step (1)) |
| 15 | card cmi-markov-defect-interpretation | STANDS (MINOR F14) | finite-dimensional identity checked; the type-III equivalences are literature with the stated hypotheses (faithful normal, D_M < infinity); the card does not claim a zero-collar Petz equivalence (no normal product state exists at zero collar) |
| 16 | card quasi-free-fidelity-formula | STANDS (MINOR F13) | the eigenvalue form and the stable C-form are equal (C = G1^{1/2} G2^{1/2} since (1-Q)^{-1/2} Q^{1/2} = G^{1/2}) |
| 17 | card petz-zero-collar-channel | STANDS | every clause traced (rows 1-4); the implementer clause rests on c11-extension-implementer (C1 scope: index-zero / Shale-Stinespring NOT OBTAINED there) but normality does NOT depend on it (quasi-equivalence route) |
| 18 | card two-chirality-law | STANDS (MINOR F8, F9) | row 12 |
| - | "Note 5 Thm 3.2" named in the brief | n/a | Note 5 has no Theorem 3.2 (fidelity_recovered_quasifree.aux: thm:det-rep = 3.1 is the only theorem of Section 3) |

## 2. Findings (most severe first; no [BREAK] found in scope)

F1 [GAP] fidelity_recovered_quasifree.tex:150 (main box), :477, :484 (conclusions: "the exact small-cross-ratio law
\(\Phi(\zeta)=f_2\zeta^2[1+O(\log^{-2}(1/\zeta))]\)"). The same document's corrected cor:structure (l. 401-402) says
"the \(\log^{-2}\) rate stated in an earlier version was wrong" and that proved is only lim Phi/zeta^2 = f2 and
limsup (Phi - f2 zeta^2)/zeta^3 <= 0. No lower-side rate is proved anywhere in scope, so any two-sided rate is stronger
than proved; the three stale sentences contradict l. 401-402. Inherited by: no card (rate-of-remainder states it
correctly; KB grep for log^-2 finds only rate-of-remainder, tail-bound, notes-errata, which record the refutation);
paper1/sec_fidelity.tex:238-240 is already correct. Repair: replace by "Phi = f2 zeta^2 (1+o(1)); Phi - f2 zeta^2 <=
f2^2 zeta^4/(1 - 2 f2 zeta^2) in the range of rate-of-remainder".

F2 [GAP] fidelity_recovered_quasifree.tex:435 ("\(-\log F^{(0)}(\eta_{\mathrm V})=2\Phi(\ldots)=8f_2\eta_{\mathrm V}^2+O(\eta_{\mathrm V}^3)\)")
and :465 ("\(-\log F^{(0)}_{\mathrm{Dirac}}(\eta)=8f_2\eta^2+O(\eta^3)\)"). Direction ledger: the upper side
-log F^(0) <= 8 f2 eta^2 + O(eta^3) follows from the global bound (rate-of-remainder (2)) since 2 eta/(1-eta) =
2 eta + O(eta^2); the lower side has only (1+o(1)) (quadratic_limit thm:lower). A two-sided O(eta^3) is open
(paper1/sec_outlook.tex:56 lists "two-sided O(zeta^3) remainder" as open). Inherited by: no card found; the paper
uses the corrected form. Repair: "8 f2 eta^2 (1+o(1)), with upper bound 8 f2 eta^2 + O(eta^3)".

F3 [MINOR] fidelity_recovered_quasifree.tex:336-340 ("Then \(\widetilde Q_N=Q_N-\widehat D\) is exactly the
compression of \(\widetilde Q_s\), and every value ... reported below is a rigorous lower bound") and :452 ("rigorous
lower ends"): D-hat is a double-precision 2D quadrature, not certified (rigor/certified_numerics.tex:421, :619; the
same document l. 565 concedes it). The lower-bound property is a theorem for the exact compression only. Inherited by:
large-zeta-values [numerical] ("the rigorous windowed lower bounds Phi_sub"), phi-derivative-nondecreasing [refuted]
(numerical paragraph "rigorous lower bound Phi(4.267) >= 2.187e-2"); the refutation itself is analytic (steps (1)-(3)
of that card, rechecked here: FHSW + collapse + monotonicity give Phi(zeta) <= (r/6) log(1+zeta/2)) and unaffected.

F4 [MINOR] N4 thm:normal-extension proof (continuum_petz_free_fermion.tex:745) and l. 244-250: the PS/Araki
quasi-equivalence criterion and "a C*-isomorphism whose source and pulled-back target representations are
quasi-equivalent extends uniquely to a normal *-isomorphism" carry no theorem/page locator in N4 (AGENTS.md §4).
Likewise N4 l. 897-912 cites nothing for joint concavity of root fidelity on von Neumann algebras or for the
Fuchs-van de Graaf step (check_note4 MINOR l. 1636, unapplied).
The mathematics is correct (checked); rigor/check_note4.tex thm:normal <1>1-<1>8 (l. 1139-1170) supplies the steps (Dixmier definition of quasi-equivalence, surjectivity of beta_s).

F5 [MINOR] N4 lem:tensorization (l. 405-441): the graded-tensor-product/Klein bookkeeping is only asserted (l. 412-414).
Checked: for even omega the product state on F(A_eps) x F(D) equals the product state on F(A_eps) x Z F(D) Z^*
(Z = (1 + i Gamma)/(1+i) fixes Omega, odd parts have zero vacuum expectation), and alpha^{D->B} = Ad U(s_t) commutes
with Gamma, so Ad Z o alpha o Ad Z^* = alpha; the factorisation holds.

F6 [MINOR] N5 lem:mobius (l. 211-213): "Its half-density action U(g) ... commutes with P_+" holds for the
Neveu-Schwarz choice (g')^{1/2} = 1/(cx+d), whose sign flips across the pole; the sign choice is not stated.

F7 [MINOR] check_note5_theory.tex prop:mono <1>4 (l. 1248-1250) cites Araki77 Thm 3.8(2)(gamma), whose hypothesis
is "N approximately finite" (refs/Araki77_PRIMS13.pdf p. 181); hyperfiniteness of F_r(I_1) is used, not stated.

F8 [MINOR] check_note5_theory.tex prop:chirality <1>7 (l. 1406-1408): "Fid of a tensor product of states in a
factorised vacuum is the product": the chiral halves of the Dirac field anticommute (graded product). Multiplicativity
still holds (thm:det-rep with block-diagonal compressions P_n^+ + P_n^-; the finite formula factorises), but the
document does not say so.

F9 [MINOR] N5 cor:collapse (l. 411): "the family is monotone in t ... and its best member is the limit t -> +infinity"
- the limit is not a member and only non-strict monotonicity is proved (prop:mono). Card two-chirality-law was
corrected on 2026-09-23; the document sentence was not.

F10 [MINOR, cross-seat C4] N5 rem. l. 423: "every normal recovery channel's recovered symbol lies in the quasi-free
feasible set, so the second-order problem over all channels is the convex programme": a non-quasi-free recovered
state's fidelity is not a function of its symbol; N5 gives no argument. Its validity rests on C4's cards
(all-channel-equals-quasi-free, all-channels-symbol-feasible), not checked here.

F11 [MINOR, cross-seat C2/C6] rigor/collar_and_invariant_formula.tex:410-414 (sec:collar (c), dated 2026-09-05):
"Theorem B remains conditional exactly on Note 7's Lemma 3.2 / Gap 2" - stale against card thm-b-universality
[refereed]; the status list is not marked as superseded.

F12 [MINOR] refs/LongoXu_1712.07283.pdf p. 2 prints eta = (b1-a2)(b2-a1)/((b1-a1)(b2-a2)), which is negative for
b1 < a2 (a typo in the source). The project correctly uses LX Thm 3.18 with G of Thm 4.1(4) (pp. 20-21), which gives
N4 eq:LX-MI; rederived here. No inheritance; recorded so that nobody copies the intro formula.

F13 [MINOR] card quasi-free-fidelity-formula: "For infinite-dimensional h the formula is obtained as the monotone
limit ... when the two states are quasi-equivalent". The individual factors diverge (Q_I has spectrum [0,1],
det(1-Q_n) -> 0); only the combined finite-n expression converges, and thm:det-rep uses normality of both states on
F_r(I), not quasi-equivalence. Suggested wording: "-log F_{F_r(I)} = lim_n of the finite formula on P_n H_I
(nondecreasing), thm:det-rep".

F14 [MINOR] cmi_as_quantum_markov_defect.tex:311-321: "Petz's sufficiency theorem" and the Connes-cocycle criterion
are cited without paper/theorem/page (AGENTS.md §4); refs/JencovaPetz06 is available.

F15 [MINOR] rigor/check_note4.tex:36-42 (abstract: "One genuine proof-breaking issue is found ... factor 2"),
thm:break l. 1282-1354, l. 1639, l. 1699, l. 1775: the factor-2 BREAK (LX r/6 = Majorana) is false and is retracted only
in the appended "Orchestrator's correction" (l. 1811-1814). I confirm the retraction independently (row 13). The
document is an evidence token of petz-zero-collar-channel (#thm:normal); a reader of the abstract gets the wrong
verdict. Repair: mark the abstract, thm:break and l. 1639/1699/1775 as withdrawn in place.

F16 [MINOR] N4 l. 832-836 (measurability of t -> beta-bar_{s_t}(x)): the repaired text tests measurability on a countable
separating family of normal functionals but still says "bounded strong approximation", which yields a net. Correct
repair: F_r(I) acts on a separable space, so its unit ball is strongly metrisable and Kaplansky gives a SEQUENCE x_n in
CAR(H_I); each beta-bar_{s_t} is normal, so phi(beta-bar_{s_t}(x)) is a pointwise limit of measurable functions.

## 3. Inheritance (kb deps)
No [BREAK] in scope. The two [GAP]s (F1, F2) are stale or overstated sentences in fidelity_recovered_quasifree.tex
that no card carries: `kb -p cft_cmi deps` / grep of kb/projects/cft_cmi/claims finds the log^-2 rate only on
rate-of-remainder, tail-bound, notes-errata (which refute it), and no card with a two-sided O(eta^3). Paper 1
(paper1/sec_fidelity.tex:238-240, sec_outlook.tex:56) already uses the corrected statements; paper sentences are
C6's scope. F3 reaches large-zeta-values [numerical] and the numerical paragraph of phi-derivative-nondecreasing
[refuted] (wording "rigorous" only). petz-zero-collar-channel is used by 34 proofs and quasi-free-fidelity-formula by
41 (`kb -p cft_cmi deps ID`): both STAND, so nothing propagates. The only upstream edge, petz-zero-collar-channel ->
c11-extension-implementer, concerns the implementer clause, which normality does not need.

## 4. Direction ledger (AGENTS.md §3)
| Evidence | Quantity | Model | Direction |
|---|---|---|---|
| N4 eq:fixed-t-integrated-bound / check_note4 prop:limit | int p(t) [-log F_{F(I)}(omega, omega~_t)] dt | exact, free fermion, zero collar | upper bound by CMI/2 = (r/12) log(1+z) |
| N4 eq:zero-collar-fidelity | F(omega, omega-bar) of the twirled channel | exact | lower bound e^{-CMI/2} |
| N5 thm:det-rep, finite n | F_n (compressed) | exact compression | F_n >= F (upper bound on F, lower bound on Phi) |
| check_note5_theory prop:mono | Phi(zeta) | exact | monotone (nondecreasing), not strict |
| phi-derivative-nondecreasing step (2) | Phi(zeta) | exact | upper bound (r/6) log(1+zeta/2) |
| N5 l. 435/465 (F2) | -log F^(0) - 8 f2 eta^2 | exact | only the UPPER side is O(eta^3); lower side o(eta^2) |
Every verdict above uses only directions that hold for the exact quantity. The refutation of Phi' nondecreasing needs
an upper bound on Phi (step 2) and the lower bound Phi > 0 near 0 (Theorem A) - both available.

## 5. Independent recomputations (tolerances fixed in the scripts before the run)
R1 `python3 rigor/council/c3_trace_norm.py > rigor/council/c3_trace_norm.out` - Nystrom SVD on log-graded
Gauss-Legendre nodes of the scalar kernel R_s on L^2(0,a) -> L^2(0,L). Validation: rank-one kernel, exact trace norm,
rel. dev. 2.3e-14. Results: (a,L,s) = (1,1,1), (2,0.7,3.1), (0.3,5,0.5), (1,3,20), zeta from 0.028 to 5:
max rel. dev. from (1/2) log(1+zeta) = 6.1e-13 at the finest resolution (n = 800, cut-off e^{-60}), finest two
agree to 4.5e-13 < tol 1e-7; tol 1e-6 met. Resolved: all modes with u, v > a e^{-60}, L e^{-60}; the cut-off corner
has kernel <= s/(4L), its Hilbert-Schmidt weight is printed (<= 3e-26). Single method (one discretisation).
Analytic cross-check: from the Szegő kernel (i/2pi)/(x-y) and W_s = 1 + V_s, the A-D block of Q - W^*QW at
(x,y) = (-u,v) is proportional to 1/(u+v) - (L/(L+sv))/(u + Lv/(L+sv)) = -R_s(u,v); hence the kernel R_s of N5
eq:defect-recall is rederived (the A-A and D-D blocks vanish by Moebius covariance of h_s on D).
R2 `python3 rigor/council/c3_finite_fidelity.py > rigor/council/c3_finite_fidelity.out` - Jordan-Wigner density
matrices exp(-sum h_ij a_i^* a_j)/Z, root fidelity by eigendecomposition, mpmath dps 40. Symbol convention check
Tr rho a_i^* a_j = Q_ji: residual 8e-41. thm:finite-fidelity vs brute force: |diff| = 1.3e-39 (n = 3), 8.1e-38
(n = 4) < tol 1e-25. Nested compressions (n = 5): F_k nonincreasing in k, as thm:det-rep asserts.

## 6. Earlier referee reports: were repairs applied?
* check_note4.tex factor-2 BREAK (l. 1316-1354): correctly withdrawn by the orchestrator (l. 1811-1814), but the
  withdrawn text still stands in the abstract and body (F15).
* check_note4.tex GAP l. 1419 (twirled channel measurability, "norm-dense"): (i) applied ("ultraweakly dense",
  N4 l. 833); (ii) the net/sequence point is only half applied (F16).
* check_note4.tex GAP l. 672 (graded vs ordinary tensor product in lem:tensorization): applied as an assertion with
  the LX Lemma 3.1 Klein identification (N4 l. 412-414); I supplied the check (F5).
* check_note4.tex MINOR l. 1636 (concavity/Fuchs-van de Graaf uncited): not applied in N4 l. 897 (no citation for
  joint concavity in the von Neumann setting); folded into F4.
* check_note5_theory.tex verdict box l. 1223-1225 ("limit point, not a member"): applied on card two-chirality-law,
  not in N5 cor:collapse (F9).
* REF-DEP-CFT-B1/B4 on petz-zero-collar-channel (constants, implementer, range F_r(AB)): all applied on the card
  (verified against N4 l. 270-293, 446-458, 670-690, 730-747).
* N5 Corrections C2/C5 (remainder, two-chirality minimum): applied in cor:structure and l. 437, but not in the main
  box l. 150, l. 435, l. 465, l. 477, l. 484 (F1, F2).

## 7. NOT DONE
* N4 Sections 5-6 (Hankel reduction, lem:J-unitary, the rank-one Laplace factorisation) not re-proved line by line;
  thm:trace-norm was instead recomputed numerically (R1, single method) and the kernel rederived analytically.
* check_note5_theory.tex GAP verdicts at l. 495, 574, 766, 1111, 1165, 1289, 1304, 1504 (modular-basis and numerics
  items of Note 5 Sections 4 and 6) not re-examined: they concern f2 and the numerics (C1 scope).
* The half-line case a = infinity of lem:mobius (card mobius-reduction-cross-ratio, check_note5_theory prop:closed)
  not checked.
* FHSW Sec. 4.2 sign issue (check_note4 thm:fhsw167) not re-derived from the source; N4 eq:s-t was rederived from
  the +hsm relation alone (row 4), which suffices.
* Source excerpts: Araki77, LX, FHSW were read via pdftotext/page image; no screenshots made (snap.py not run; a
  referee writes only its report and scripts).
* The scratchpad venv was empty when checked; R1/R2 ran with the system python3 (numpy 2.5.2, scipy 1.18.1, mpmath).
