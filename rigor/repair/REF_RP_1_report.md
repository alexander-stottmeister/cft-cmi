# REF-RP-1 report — Theorem B and the Moebius reduction (repair round 2026-11-19)

Referee: REF-RP-1 (Opus), adversarial. Objects: rigor/moebius_reduction_general_nets.tex; rigor/repair/R2_patch.json;
R5_patch.json items 11-18. Cards: moebius-reduction-general-nets, thm-b-universality, implementer-hypotheses,
mobius-reduction-cross-ratio.

## (1) New document: Moebius map g, zeta, cross ratio
STANDS. lem:geom (l. 160-209) recomputed independently in exact rational arithmetic:
`${PYTHON:-python3} rigor/repair/ref_rp_1_geometry.py > rigor/repair/ref_rp_1_geometry.out` (tolerance: exact equality,
fixed before the run). 2000 random rational (a, L, s > 0, y): g(0)=0, g(L)=1, g o g^-1 = id; (3) g'(x) m(x) = kappa (-y^2)
at y = g(x); (5) g(h_s(x)) = hhat_{kappa s}(g(x)); h_s, hhat_t solve the flow ODEs of m, mhat; z = l_A l_C/(l_B(l_A+l_B+l_C))
= a s/(a+L) = kappa s; cross ratio (x3-x1)(x4-x2)/((x3-x2)(x4-x1)) of -a<0<L/(1+s)<L equals 1+z; z = eta_V/(1-eta_V)
(card cross-ratio-conventions); g(L/(1+s)) = 1/(1+zeta). 0 failures. (6): Schwarzian of (pz+q)/(qbar z+pbar),
|p|^2-|q|^2 = 1, vanishes (max 9.7e-49 at 50 digits, 200 samples, tol 1e-40); the document's hand computation in
<1>8 is also right (6 qbar^2/(.)^2 - (3/2)(4 qbar^2/(.)^2) = 0). g_B/8 = c/(12 pi^2) exact.
(4) uses only C^1 phi and Lipschitz f (Picard-Lindeloef): correct; (7): g is a smooth circle diffeomorphism with
g(0) = 0, g((-a,0]) = (-inf,0] (with g(-a) = infinity, where g_tot vanishes by continuity), g([0,L]) = [0,1]; so
(E1)-(E3) transfer. Direction ledger: all items are equalities. No finding.
## (2) prop:cov (CDIT Prop. 2.1, H^2 approximation)
STANDS (one MINOR). Read in the PDFs (pdftotext): CDIT refs/CDIT_1808.02384.pdf p. 5, Prop. 2.1: "U(gamma)T(f)U(gamma)^* =
T(gamma_*(f)) + c/(24 pi) int {gamma,z} f e^{i2 theta} d theta on vectors in Hfin(c,h), for f in Vect(S^1) and gamma in
Diff~+(S^1)", Schwarzian in d/dz := -i zbar d/dtheta (p. 5-6). Box C2's verbatim text matches.
- Domain/closure: CDIT cites FH05 Prop. 5.1 / 3.1 for it. refs/FewsterHollands05_math-ph-0412028.pdf Prop. 3.1 (eq. 3.27)
  states the law "on vectors in D", D a domain of C^1-regularity, and its proof (3.30) evaluates U(rho)Theta(f)U(rho)^-1 psi
  by differentiating s -> U(exp(s f_rho)) psi, which needs U(rho)^-1 psi in D(Theta(f)), Theta(f) the self-adjoint generator;
  FH05 Prop. 5.1: U^(c,h) leaves H^infty = cap_n D(L0^n) (contains Hfin) invariant. So the document's paraphrase
  (V^* Hfin in D(closure T(f)), closure on the left) is what the source proves. MINOR: box C2 should cite FH05
  Prop. 3.1 + 5.1 for the domain reading instead of leaving it as an unsupported paraphrase (sec:open item 1 is thereby
  answered in the affirmative). Phase: V_j = mu_j U^(c,h_j)(gamma), cancels in Ad (<1>1, <1>2); decomposition from CDIT
  Prop. 3.14 (p. 21, read) via the refereed C11 lemma.
- Central term: for Moebius gamma the z-Schwarzian vanishes (item (1), lem:geom(6)); CDIT's d/dz agrees with the
  holomorphic derivative on restrictions of holomorphic functions, so iterating it is legitimate. Correct.
- Approximation: the document does NOT use strong resolvent convergence (CDIT Prop. 2.2(5), which would need g_*
  continuous in the 3/2-norm, the multiplier problem). It uses: p_k -> f in H^2 (Fourier truncation, <2>1); lem:Th2
  (on a fixed L0-eigenvector, ||T(F)psi|| <= sqrt2 r (1+E) ||F||_{H^2} ||psi||; checked: orthogonality of L_n psi from
  [L0,L_n] = -n L_n, (1+|n|^{3/2})^2 <= 2(1+|n|^3) <= 2(1+n^2)^2 for all integers n); lem:push (g_* bounded on real
  H^2 for smooth g: Leibniz and change of variables, both checked); then equality of matrix elements <T(f)phi, V^*psi> =
  <phi, V^* T(g_*f) psi> on the core Hfin_j gives V^*psi in D((T|Hfin)^*) = D(closure) (<1>4), and maximality of the
  self-adjoint closure gives V closure(T(f)) V^* = closure(T(g_*f)) (<1>5-<1>6). Each step is correct; topology H^2,
  g_* continuous in it (lem:push), no SRC needed. Exponentials by Stone. For f = g_tot: g_tot in H^2 (C^1 with g_tot''
  piecewise smooth, one jump; lem:push <1>1 converse) and ||g_* g_tot||_{3/2} < inf by CDIT Prop. 2.3 (p. 6, read).
## (3) g_* g_tot in class E (E1)-(E3)
STANDS. C11 def:gtot (implementation_C11.tex l. 135-150): (E1) 0 on (-a,0], (E2) m on [0,L], (E3) C^inf off 0, C^1 on S^1.
g is a smooth (Moebius) diffeomorphism of S^1 with g(0) = 0, g((-a,0]) = (-inf,0] (g(-a) = infinity is not in (-a,0]),
g([0,L]) = [0,1]; push-forward is local (eq:push), so g_* g_tot = 0 on (-inf,0] [(E1)], = g_* m = kappa mhat on [0,1]
[(E2), item (1)], and smooth off g(0) = 0, C^1 on S^1 [(E3)]; hence kappa^-1 g_* g_tot in E_inf (lem:geom(7), l. 199-205).
E_inf is a subset of E(a',1) for every a' > 0 (checked against (E1)-(E3)). UB's -chi (universality_theorem_B.tex
eq:chi, l. 103-108: 0 on (-inf,0], -x^2 on [0,1], supp [0,2], C^1, smooth off 0) is in E_inf. Converse direction
(g^-1)_* with kappa (g^-1)_* mhat = m: correct. Remark (not a finding): for a < L the field g^flat = kappa (g^-1)_*(-chi)
passes through infinity (g^-1 has its pole at y = 1 + a/L < 2), i.e. it is a C11 type-(ii) extension; it is still in
E(a,L) because (E1) only constrains (-a,0].
## (4) part (b): extension independence
STANDS. s >= 0: zeta = kappa s >= 0 and lem:ext (moebius doc l. 340-371) with sigma = zeta, ghat^sharp = -chi. lem:ext
checked step by step (same argument as item (8)): <1>1 C11 thm:H1 <1>2 (l. 557-578: phi real, finite 3/2-norm, phi = 0 on
an open interval I_0 => e^{it T(phi)} in A(I_0)', via CW05 L. 4.6, lem:loc-HT(i), semicontinuity and (HD)) applies with
I_0 = Ihat = (-inf,1), a proper open arc; <1>2 the flow of ghat^sharp fixes (-inf,0] (field 0 there, so also infinity by
continuity) and equals hhat_b on [0,1) for b >= 0 ([0,1) is forward invariant under ydot = -y^2), so the image of Ihat is
(-inf, 1/(1+b)) in Ihat; C11 thm:H1(iii) (l. 554-556: every s, every interval J) applies since E_inf is in E(1,1).
"One explicit extension for every real s": g^flat := kappa (g^-1)_*(-chi) in E(a,L) (lem:geom(7)), and
kappa^-1 g_* g^flat = -chi by functoriality of push-forward, so part (a) (valid for all real s, cor:conj) gives the
normal-form state directly, without lem:ext. Correct and explicit.
## (5) part (c): hypotheses of Theorem B used, s -> 0+
STANDS. <1>6: Alberti-Uhlmann Thm 2(3) (box C4) in the representation pi = alpha = Ad V|A(I) of A(I) on H:
S_{alpha}(nu o alpha) = S_{id}(nu) because alpha is onto A(Ihat); vector representatives Omega and Uhat_zeta^* Omega
(omegahat_sigma(X) = <Uhat^* Omega, X Uhat^* Omega>): correct. <1>8 uses thm:B (UB l. 874-899) with: standing (HD),
(BW), (RS) (UB (S2)); (H1) in the (C7) form = C11 thm:H1(iii) for -chi in E(1,1); (H2), (H2') = C11 thm:H23(i),
lem:loc-HT(ii); (H3) = C11 thm:H23(ii), whose proof (l. 666-672) holds for every bounded X, hence on
M = A((-inf,1)) although C11 states it for A((-a,L)); also redundant by UB rem:H2H3. thm:B's expansion is two-sided
(s -> 0, o(s^2)); thm:main(c) uses it only for zeta -> 0+ (general extension) and zeta -> 0 (g^flat); o(zeta^2) = o(s^2)
for fixed kappa > 0. Direction ledger: (a), first part of (c) equalities of states/exact fidelity; the asymptotic law
inherits both bounds from thm:B <1>1 (lower, prop:H3) and <1>2 (upper, prop:H2). For s < 0 the "three intervals" reading
fails (L/(1+s) > L), but the theorem states the identity of states on A(I), which remains meaningful; the card says
"both signs for that extension": consistent.
## (6) sec:open checkpoints
(i) Domain reading of box C2: resolved affirmatively by FH05 Prop. 3.1 + 5.1 (item 2). (ii) H_j = H(c,h_j) and the lift:
CDIT Prop. 3.14 (p. 21, read: U is a direct sum of irreducible positive-energy projective reps; U|PSL lifts to a true
rep) via the refereed C11 lemma; phases cancel. OK. (iii) s < 0 for a general extension: not covered, correctly
disclosed in thm:main(b), the abstract, the card ("Not covered: s < 0 for a general extension"). (iv) No covariance
under non-smooth or non-Moebius maps: confirmed; box C2 enters only at prop:cov <1>2 with trigonometric polynomials p
and Moebius g. Compilation: pdflatex twice in my scratch copy: 0 lines matching ^! or (Reference|Citation).*undefined,
14 pages; the project log (14 pages, clean) agrees. New excerpt rigor/shots/R2_CDIT_axioms15.png viewed: CDIT p. 22,
axioms (1)-(5), matches box C1. MINOR (AGENTS.md 5): sec:open reports "maximal deviation 5e-15, tolerance 1e-12" from a
scratch computation with no project script; repair: cite rigor/repair/ref_rp_1_geometry.py (.out) (exact, item 1) or
drop the number. MINOR: thm:main <1>8 (and sec:paper2) attribute "(H1) in the form (C7), which is all that Theorem B's
proof uses" to council C2 F3 (an unrefereed council claim); it is confirmed by my item (7), so no repair needed.
## (7) R2 patch item 0: restated (H1) vs implementation_C11.tex; later uses
STANDS (one MINOR). C11 thm:H1 (implementation_C11.tex l. 548-556) verbatim: "For every s in R: ... (iii)
U_s A(J) U_s^* = A(ktil_s J) for every interval J subset S^1, including intervals containing the singular point 0."
UB (S4)(H1) (l. 119-122) now: "For |s| < s_0 there are unitaries U_s with U_s A(K) U_s^* = A(ktil_s(K)) for every
interval K"; ktil_s = flow of -chi, -chi in E(1,1), so C11 proves it with U_s = e^{is T(-chi)} for every s. Exactly
(C7) (C11 l. 125). Every later use checked:
- prop:H3 <1>1 (l. 315) and prop:H2 <1>1 (l. 415): use only that U_s are unitaries and omega_s = <Psi_s, . Psi_s>,
  Psi_s = U_s^* Omega. Weaker (H1) suffices.
- thm:B <1>1-<1>2: only through prop:H3, prop:H2. Unaffected; thm:B uses neither lem:ext nor prop:geom (grep: prop:geom
  is referenced only in the variational-form discussion l. 671, 736, 1024, 1064).
- prop:geom: now via C11 thm:H1 <1>2 (item 9).
- prop:tensor <1>2 (l. 973): (U1 (x) U2)(A1(K) (x) A2(K))(U1 (x) U2)^* = A1(ktil K) (x) A2(ktil K): the (C7) form is
  closed under tensor products. Fine.
- prop:fermion <1>1 (l. 916-932): (H1) for F_r with Gamma(W_s); the (C7) form follows from the Bogoliubov covariance
  cited there. MINOR: l. 931-932 still cites "Lemma Commutant elements from I' plus Remark The graded structure for the
  locality clause"; (H1) no longer has a locality clause, so this clause of the By-justification is stale (harmless).
- MINOR: the corrections list item (d) (l. 1130-1133) still says Haag duality "was replaced by locality" in lem:ext
  and prop:geom; after the repair both use (HD) (inside C11 thm:H1 <1>2). (HD) is a standing hypothesis of thm:B, so no
  mathematical consequence, but (d) should carry a "superseded 2026-11-19" note like R2 (l. 1110). Consequence for the
  graded free-fermion net (no HD): prop:geom/lem:ext in their repaired form do not apply to it; nothing for the fermion
  (prop:fermion (3) is quoted from uhlmann_upper_bound.tex) depends on them.
## (8) new proof of lem:ext (Trotter)
Proof steps STAND; the STATEMENT (R2 item 3) needs a repair: GAP.
- <1>1: C11 thm:H1 <1>2 hypotheses (phi real, ||phi||_{3/2} < inf, phi = 0 on an open interval I_0): met with I_0 = I
  = (-inf,1); uses (HD). OK.
- <1>2: "ktil_b^sharp fixes (-inf,0] pointwise (g_tot^sharp = 0 there)". GAP: the statement (UB l. 182-184) quantifies
  over "two fields of the class E ... (E1)-(E3), with L = 1 and some a > 0, which agree on I". (E1) only gives 0 on
  (-a,0]; agreeing with each other on I = (-inf,1) does not make them vanish on (-inf,-a]. For such fields the flow
  can move the end infinity of I and ktil_b^sharp I subset I is unproved (and the lemma is then not about extensions
  of k_s). Quote: "Let g_tot and g_tot^sharp be two fields of the class E ... which agree on I". Repair: require both
  fields to vanish on (-inf,0] (i.e. lie in E_inf of moebius_reduction_general_nets.tex sec:conv, or agree with -chi on
  I), as the new document's lem:ext does. Not load-bearing for thm:B (which does not use lem:ext).
- ktil_b I subset I for b >= 0: correct under that repair ([0,1) forward invariant under ydot = -y^2).
- <1>4 Trotter: Reed-Simon VIII.31 needs A, B self-adjoint and A + B essentially self-adjoint on D(A) cap D(B). With
  A = closure T(phi), B = closure T(g^sharp): A + B on D(A) cap D(B) contains Hfin, is symmetric and extends T(g_tot)|Hfin,
  which is e.s.a. (CW05 Thm 4.4 / CDIT Prop. 2.2(3), read p. 6). For a symmetric S extending an e.s.a. T0:
  closure(T0) subset closure(S) subset S^* subset T0^* = closure(T0), so S is e.s.a. with the same closure. The principle
  "a symmetric extension of an e.s.a. operator has the same closure" is applied correctly. (Reed-Simon itself is not in
  refs/: the statement of VIII.31 used here is the hypothesis list as C11 quotes it, NOT OBTAINED by me in PDF.)
- <1>5 induction: W^{k+1} X W^{k+1 *} = W (Ad U^sharp_{k b} X) W^*, Ad U^sharp_{kb} X in M by <1>2: correct.
- <1>6: W_n -> W strongly (unitaries) implies W_n^* -> W^* strongly (||W_n^* xi - W^* xi|| = ||(W - W_n) W^* xi||), so
  W_n X W_n^* -> W X W^* strongly; states follow by evaluation at Omega. Correct.
Same verdict for C11 thm:H1 <1>7 as patched (R2 item 14): correct there, because in C11 all class-E fields vanish on
(-a,0] and I = (-a,L).
## (9) prop:geom <1>1 under ||h||_{3/2} < infinity
STANDS. supp h compact in the open arc I' = (1,inf) gives h = 0 on the open interval I; C11 thm:H1 <1>2 with phi = h,
I_0 = I gives e^{i tau closure T(h)} in A(I)' (uses HD). Omega in Hfin subset D(T(h)); <2>1 by Stone; <2>3 linearity
of f -> T(f)Omega on Hfin for g_tot and h (both finite 3/2-norm). <1>2 (Alberti-Uhlmann ">=") and <1>3-<1>5 unchanged and
correct. The class of h changed from "C^{1,1} with the postulate e^{i tau T(h)} = U(phi')" to "finite 3/2-norm"; it
contains all smooth compactly supported h, so the infimum in the variational form is not raised. R2 items 6-8, 10 OK.
## (10) paper-2 versions (R5 items 11-18)
STANDS (MINORs). Checked against the applied text (paper2/sec_setting.tex l. 100-125, 158-190; sec_implementation.tex
l. 86-140; sec_universality.tex prop:geom) and against C11 (numbering from implementation_C11.aux: Def. 2.1 = def:gtot,
Thm. 2.3 = thm:reg, Thm. 4.7 = thm:H1, Lemma 4.4 = lem:loc-HT; the paper's citations are right).
- Item 11/12 (lem:ext): the paper's class description "0 on A and equal to m on D" with A = (-inf,0) (paper eq:geom)
  is the correct E_inf, so the paper version does NOT have the UB quantifier GAP of item (8). The proof matches C11
  thm:H1 <1>7 and the new rigor lem:ext step by step (Trotter, s >= 0, closure argument). MINOR: [RigorC, Def. 2.1]
  is cited for a class that is defined there with (E1) on (-a,0] only; the paper's paraphrase is the stronger
  (correct) condition; one clause "with A = (-inf,0)" would make the citation exact.
- Item 13 (remark on eq:H1loc): correct. MINOR: paper-2 Hypothesis H1 (l. 102-112) still lists eq:H1loc as part of
  the hypothesis ("and the representation is local in the form"), whereas rigor UB (S4) now lists it as a standing
  fact proved by C11 lem:loc-HT(i). Since the clause is restricted to smooth phi there, it is true and harmless; the two
  versions differ only in where the clause sits.
- Item 14: thm:H1(ii) "for s >= 0" now agrees with C11 l. 555 ("for 0 <= s"). Correct.
- Items 15-16 (prop:geom): ||h||_{3/2} < inf; h = 0 on the component I_0 of S^1 minus supp h containing closure(I)
  (an open interval, since supp h is a nonempty compact subset of the open arc I'), lem:loc(i), isotony. Correct.
  MINOR (not in a patch item): paper-2 lem:loc(i) proof ends "intersecting over eps > 0 and using additivity gives
  e^{itT(f)} in A(I_0') subset A(I_0)'"; C11 obtains cap_eps A(I_eps) = A(I_0') from semicontinuity, which rests on
  (HD) (C11 l. 576-578); "additivity" should read "semicontinuity (eq:sem of C11, using (HD))".
- Items 17-18: "for smooth h, so that g_tot + h in E, and s >= 0": correct (smooth h supported in I' keeps (E1)-(E3)).
- sec_setting l. 43-47 (R5 wording, REF-RP-3's seat): the general-net reduction is attributed to the document under
  review and thm:B is said not to use it: correct (item 7).
## (11) the four cards
- moebius-reduction-general-nets [proved]: FAIL (repair). Statement (a) says the result "rests on U(g) T(f) U(g)^* =
  T(g_* f) for real f with finite 3/2-norm in H^2(S^1)"; prop:cov (moebius doc l. 269-270) also assumes
  ||g_* f||_{3/2} < infinity, which is not implied: H^2 is not contained in S^{3/2} (Cauchy-Schwarz gives
  sum |f_n| n^{3/2} <= ||f||_{H^2} (sum n^3/(1+n^2)^2)^{1/2}, a divergent sum), and Moebius invariance of
  H^2 cap S^{3/2} is not proved anywhere. The card states the proposition more strongly than the document. Repair: add
  "and ||g_* f||_{3/2} < infinity" (for f = g_tot it holds by CDIT Prop. 2.3, cor:conj <1>2). Everything else in the
  Statement matches thm:main (quantifiers, kappa^-1 = (a+L)/a, s >= 0 vs one explicit extension for all s, s -> 0+,
  HD/BW/RS, 1 + zeta the cross ratio, Not covered list); status proved is the weakest that fits (not yet refereed);
  locators #thm:main, #prop:cov exist; depends right. Document MINORs to fix at the same time: cite FH05 Prop. 3.1 + 5.1
  in box C2 (item 2); sec:open's scratch number (item 6).
- thm-b-universality [refereed]: FAIL (repair). Theorem B itself and its proof are unaffected by the repair (item 7),
  and the (H1) clause of the Statement is exactly C11's (C7)/thm:H1(iii). Two defects: (1) the Statement now reads
  "where zeta = s,, g_B = ..." (double comma introduced by card_changes_1.json); (2) the repaired UB lem:ext
  (R2 item 3, universality_theorem_B.tex l. 182-184), described in this card's 2026-11-19 note as "re-proved for
  class-E fields and s >= 0", quantifies over class-E fields that merely agree with each other on I = (-inf,1), while
  its step <1>2 needs them to vanish on (-inf,0] (item 8, GAP). Repair: restrict lem:ext to fields vanishing on
  (-inf,0] (E_inf, as in moebius_reduction_general_nets.tex lem:ext and paper-2 lem:ext), fix the double comma. Also
  MINOR: UB corrections item (d) l. 1130-1133 and prop:fermion l. 931-932 are stale (item 7).
- implementer-hypotheses [refereed]: PASS. New sentence "(H1) is proved in the (C7) form; independence of omega_s of
  the extension is proved for fields of class E and s >= 0 only (thm:H1 <1>7)" matches implementation_C11.tex
  thm:H1 (l. 548-556) and the patched <1>7 (R2 item 14), where class E is C11's (with (E1) on (-a,0], I = (-a,L)), so
  no gap there. Rest of the Statement unchanged from the refereed version.
- mobius-reduction-cross-ratio [proved]: FAIL (repair). The only change is the 2026-11-19 note, which is accurate
  (it omits "both signs for one explicit extension", not an overstatement). But the How to verify section is empty,
  which AGENTS.md 2 forbids ("Every card's How to verify gives a command to run, or a file:label to open"); flagged
  as MINOR by REF-DEP-CFT-A2 and REF-DEP-CFT-B8 on 2026-09-23 and never filled. Repair: How to verify =
  fidelity_recovered_quasifree.tex lem:mobius (l. 197-208); rigor/check_note5_theory.tex prop:closed with the paragraph
  of eq:Fclosed (l. 189-208) and lem:sinh at beta = L - x for a = infinity; plus, if wanted, the exact cross-ratio
  check rigor/repair/ref_rp_1_geometry.py. Statement otherwise right (checked identities in item 1).
## Verdicts
Per theorem / repaired step: lem:geom STANDS; lem:push STANDS; lem:Th2 STANDS; prop:cov STANDS (MINOR citation);
cor:conj STANDS; moebius lem:ext STANDS; thm:main (a)(b)(c) STANDS; UB (H1) restatement (R2 item 0) STANDS;
UB lem:ext (R2 items 3-4) STANDS WITH REPAIR (statement quantifier); UB prop:geom (R2 items 6-8) STANDS;
C11 thm:H1 <1>7 (R2 item 14) STANDS; paper-2 R5 items 11-18 STAND (MINORs).
Cards: moebius-reduction-general-nets fail; thm-b-universality fail; mobius-reduction-cross-ratio fail;
implementer-hypotheses pass.
