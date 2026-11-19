# REF-RP-4 report — index zero (repair round 2026-11-19)

Referee REF-RP-4 (Opus), adversarial. Objects: rigor/index_zero.tex, rigor/index_zero_check.py/.out,
rigor/repair/R1_patch.json. Cards: group-index-zero-large-s, rate-of-remainder, const-f2 (verdicts);
pushforward-blocks-equal-singular-values (report only).

## 0. Cards read (Notes first)
Read `kb -p cft_cmi show` for group-index-zero-large-s (notes 2026-09-24, 2026-11-19), pushforward-blocks-equal-singular-values,
rate-of-remainder (statement changed 2026-11-19 14:20:08 by orchestrator), const-f2 (statement changed 2026-11-19 14:20:07:
0.0676 -> 0.0675). Brief rigor/repair/REFEREE_BRIEF.md read in full.

## 1. lem:kernels, lem:sym — STANDS
Re-derived each step (rigor/index_zero.tex l. 60-96).
- lem:kernels <1>1: for Ax = x, ||x||^2 = <x,Px> - <x,Qx> = ||Px||^2 - ||Qx||^2 <= ||x||^2 - ||Qx||^2 forces Qx = 0,
  ||Px|| = ||x||, so x in PH cap ker Q; converse direct. <1>3: for x in PH, ||PUx||^2 = <x, U^*PU x> = ||Qx||^2, so
  ker X_U = PH cap ker Q. <1>4: z = U^*y, y in PH with PU^*y = 0 gives Pz = 0, Qz = U^*Py = z; converse checked;
  U^* injective. Hence dim ker X = m_A(1), dim ker X^* = m_A(-1), finite since A compact (thm:spec (iii), lambda = +-1).
- lem:sym: AS = QP - PQ = -SA and A^2 + S^2 = 1 re-expanded by hand (both correct). For 0 < |lambda| < 1, S maps
  ker(A - lambda) into ker(A + lambda), injective since S^2 x = (1 - lambda^2) x. Both directions give equal (finite)
  multiplicities. The eigenvalues +-1 are correctly EXCLUDED from the symmetry (S = 0 on ker(A -+ 1) since S^2 = 1 - A^2);
  their multiplicities are exactly dim ker X and dim ker X^* (lem:kernels). ||A|| <= 1 from A^2 + S^2 = 1. No objection.

## 2. lem:cubic — STANDS
Formula and sign: ind X_U = dim ker X_U - dim ker X_U^* = m_G(1) - m_G(-1) = tau(G_U) = Tr(G_U^3), G_U = P_+ - U^* P_+ U.
Independent derivation: lem:kernels gives the two multiplicities; lem:sym cancels lambda^3 against (-lambda)^3 for
0 < |lambda| < 1 in the absolutely convergent sum sum_k lambda_k^3 (sum |lambda_k|^3 <= sum lambda_k^2 since |lambda_k| <= 1).
This is the Avron-Seiler-Simon index of a pair, but the document does NOT cite ASS (grep: no hit) and proves it from
lem:kernels, lem:sym, thm:spec; no source needed, so nothing is NOT OBTAINED. (No ASS/Kato/Effros PDF is in refs/.)
Trace class: the document never claims G^3 trace class; lem:cubic (a) bounds sum_j |<f_j, XYZ f_j>| <= ||X||_2 ||Y||_2 ||Z||
(Cauchy-Schwarz, ||YZ||_2 <= ||Y||_2 ||Z||), which is all that is used; (b) basis independence via the absolutely
convergent double series <Af_j,e_i><e_i,A^2 f_j> (bounded by ||A||_2 ||A^2||_2) — correct. (c) telescoping identity
A^3 - A'^3 = AA(A-A') + A(A-A')A' + (A-A')A'A' expanded and checked; bound correct.
Numerical test (own script, TOL = 1e-10 fixed in the script before the run):
`python3 rigor/repair/ref_rp_4_cubic.py > rigor/repair/ref_rp_4_cubic.out`.
 (a) finite rank / finite dimension, random unitaries n = 6, 11, 40: |Tr G^3| <= 4.3e-15 < TOL, block singular values
     agree to 4.4e-16 (index 0 automatically).
 (b) l^2(Z), multiplication by u = exp(i a sin theta) (index 0, infinitely many eigenvalues of G) and by
     u = e^{i theta} exp(i a sin theta) (Toeplitz index -1), a = 0.7, 3.0, window |n| <= 60, inner sum to |n| <= 120:
     Tr G_W^3 = 0 (dev <= 1.1e-16) resp. -1 (dev <= 7.8e-16), m(1) - m(-1) = 0 resp. -1; HS weight captured to
     the exact ||G||_2^2 = sum |n| |uhat(n)|^2 within double rounding (<= 2.2e-16). Honest caveat: my a-priori
     truncation bound 3 ||G||_2^2 sqrt(discarded) is limited by double-precision cancellation to <= 4.5e-8, i.e. it
     does NOT certify 1e-10; the observed deviations are <= 7.8e-16 and the tail of J_n(a) beyond |n| = 60 is < 1e-60.
     Index-1 case: the singular values of B carry an extra 1 and otherwise coincide with those of C (to 12 digits),
     the C3 mechanism exactly: index zero cannot be dropped from thm:sv.
 (c) exact bilateral shift: G = -|e_{-1}><e_{-1}|, Tr G^3 = -1 = ind X.

## 3. thm:path — STANDS
(index_zero.tex l. 125-148.) <1>1: ind X_s = tau(G_s) needs only G_s in S_2 (P1) (lem:kernels + lem:cubic (d)).
<1>2: continuity of s -> tau(G_s) follows from lem:cubic (c), |tau(A) - tau(A')| <= (||A||_2^2 + ||A||_2||A'||_2 +
||A'||_2^2) ||A - A'||_2, i.e. a Hoelder-type estimate (effectively S_3 control by S_2), with the prefactor locally
bounded under (P2). <1>3: integer-valued continuous on an interval => constant (IVT argument correct; connectedness of
the interval J is used and stated: J an interval). Start value: (P3) ind X_0 = 0 is an explicit hypothesis, satisfied
for U_0 = 1 (X_0 = identity) or U_0 commuting with P_+ (X_0 unitary). Nothing beyond (P1)-(P3) is used; no smallness.
lem:products (a),(b) (l. 150-178): checked; G^{UV} = G^V + V^* G^U V (add/subtract V^*P_+V) correct; S_2-continuity of
s -> V_s^* T V_s by finite-rank approximation uniform in s, correct.

## 4. thm:sv — STANDS
(l. 180-222.) No polar decomposition is used. <1>1: on P_+H, X^*X + C^*C = 1 and XX^* + BB^* = 1 (unitarity; checked:
C^*C = P_+U^*P_-UP_+, BB^* = P_+UP_-U^*P_+). <1>2: X^*X and XX^* are isospectral off 0 with multiplicities (X maps
eigenspaces injectively both ways); same for BB^*, B^*B. <1>4: for 0 < sigma < 1, m_{C^*C}(sigma^2) = m_{X^*X}(1 - sigma^2)
= m_{XX^*}(1 - sigma^2) = m_{BB^*}(sigma^2) (eigenvectors for nonzero eigenvalues lie in P_+H; correct). <1>5: sigma = 1
is exactly where index zero enters: m_{C^*C}(1) = dim ker X, m_{BB^*}(1) = dim ker X^*. Statement is about the NONZERO
singular values (convention (C3), l. 30-32: singular values := nonzero eigenvalues of T^*T, square-rooted), which is
what the uses need (||.||_2, operator norm, Fredholm determinant, all insensitive to zeros). Index zero is necessary
and sufficient for this (converse visible in <1>4-<1>5); my ref_rp_4_cubic.out case (b) index -1 shows the extra
singular value 1 of B. Consequences ||G||_2^2 = 2||C||_2^2 via lem:blocks (UG = C - B, S_2-orthogonal positions; a
correct trace-free replacement of RR lem:groupbound <1>1's 'divergent traces cancel') and C_{U^*} = B_U^*: correct.

## 5. thm:group, lem:gen — STANDS
thm:group (l. 224-241): <1>1 G_{s+t} = G_s + U_s^* G_t U_s from U_{s+t} = U_t U_s and lem:products <1>4 (U = U_t, V = U_s):
re-derived. <1>2 G_s in S_2 for all s (n-fold sum of conjugates of G_{s/n}). <1>3 ||G_{s+t} - G_s||_2 = ||G_t||_2 -> 0:
S_2-continuity at EVERY s from (G) at 0 alone; thm:group does not even need strong continuity. (P3) from U_0 = 1.
lem:gen (l. 243-283), domains: D(K) = {phi: lim h^{-1}(U_h phi - phi) exists}, dense by Stone; <1>1 extension of the form
identity from a core to D(K) by graph-norm density (P_+, C bounded) correct; <1>2 U_sigma D(K) = D(K) and
d/dsigma U_sigma phi = K U_sigma phi = U_sigma K phi (standard, proved in the step); <1>3 product rule for
f(sigma) = <U_sigma phi, P_+ U_sigma psi>, f' = <KU phi, P_+ U psi> + <P_+ U phi, K U psi> = <U phi, C U psi> by <1>1 with
x = U phi, y = U psi (both in D(K) by <1>2) — the core need NOT be invariant, because <1>1 has already extended (K) to
D(K), which is invariant. f' continuous. <1>4 FTC for the C^1 scalar function, then density in (phi, psi) of a bounded
form: correct. No Duhamel formula for unbounded operators and no Bochner integral are needed: the S_2 bound <1>5-<1>6
comes from finite-section Cauchy-Schwarz + Parseval + monotone limit, correct. Sign: (K) <P_+x,Ky> + <Kx,P_+y> =
<x,Cy> is the form of [P_+,K] (K^* = -K), so C = [P_+,K] = -[P_-,K], and ||C||_2 = ||[P_-,K]||_2.
lem:app-K (l. 312-338): with (W), C = -G^(1) + i[P_+,h'] on D(K) = D(D); sign consistent with PA eq:intrep/lem:integralrep
(G^(1) = [P_-,D], G_s = int W~^* G^(1) W~): <W~_s x, P_+ W~_s y> = <x,(P_+ - G_s)y>, derivative -<x,G^(1)y>. <1>3
re-derived: <P_+x, ih'y> + <ih'x, P_+y> = <x, i[P_+,h']y>. D + ih' generates e^{sK} (bounded skew perturbation of a
skew-adjoint operator). Strong vs S_2 continuity: lem:gen gives S_2-Lipschitz bound directly; no gap.

## 6. Applications lem:app-W, lem:app-K, lem:app-prod, lem:app-EF — STAND for PA's field; GAP (inherited) for general chi
Opened the cited lines.
- lem:app-W (l. 290-305): a conditional lemma, (W) is its hypothesis; proof (<1>1 Bochner triangle inequality, thm:group)
  correct. For PA's field (chi = chi' = 0 off [0,2]) (W) is PA lem:gen (l. 638-670: strongly continuous group, Stone,
  Nelson core) + PA lem:integralrep eq:intrep (l. 671-735; Bochner in S_2 for all s, <1>3-<1>4) — verified.
  For a general admissible chi (RR def:flow (F1)-(F3), l. 87-103) (W) is only ASSERTED by RR lem:autocorr <1>1 (l. 125-131),
  which cites PA Lemma 4.2 <1>2-<1>3: <1>2 (the pointwise identity d/ds Psi_s = F_s) is local and holds for any C^{1,1}
  chi with complete flow, but <1>3 identifies the kernel of W~^* G^(1) W~ and of G_s via PA lem:kernel (l. 220), which is
  stated for phi = id off a compact set, and PA <1>1 uses supp chi in [0,2]; RR def:flow allows chi growing linearly,
  so k~_s is not id off a compact set. Verdict: GAP (not BREAK; the extension is a change of variables but is written in
  no document). It is PRE-EXISTING in RR lem:autocorr (a proved document) and R1 flags it honestly (verdictgap after
  prop:ranges, l. 391-396). It affects only the general-chi uses: prop:ranges items 2 and 3 (thm:exactquad, thm:global
  with f2^chi) and lem:app-prod (c) (EF thm:UH takes a general admissible chi). It does NOT affect the f2 bound of
  card rate-of-remainder, which comes from prop:rrr with K = D + ih', h' in PA's A' and PA Prop. 7.6 (the infimum is
  PA's, for PA's D), where (W) holds by PA itself.
- lem:app-K (l. 307-338): STANDS (see item 5). D(K) = D(D) is trivially a core; C = -G^(1) + i[P_+,h'] in S_2
  (P_+h'P_- = (P_-h'P_+)^* in S_2 by def:admissible, PA l. 737-740).
- lem:app-prod (l. 340-362): (a) PA U_s = W~_s e^{ish'} (PA l. 742-744) — STANDS (e^{ish'} norm-continuous, <1>1;
  lem:products (b)). (b) NW thm:T3 <1>2 (NW l. 700-704): W_{d_k} preserve H_I, H_I' and commute with P_+ (stated there);
  each factor is a reparametrised group satisfying (P1)-(P2) — STANDS. (c) EF thm:UH (EF l. 677-684: G, Z_e bounded,
  anti-self-adjoint, P^perp(.)P in S_2 — hypotheses checked) — STANDS WITH REPAIR (MINOR): the statement of (c) omits
  that chi must satisfy (W) (its proof <1>2 uses lem:app-W); add 'for chi satisfying (W) of Lemma 6.1'.
- lem:app-EF (l. 364-375): EF lem:group (EF l. 652-660) assumes the S_2-valued identity for unbounded Z, which gives
  ||P - U_t^*PU_t||_2 <= |t| ||[P,Z]||_2 (EF <1>2, independent of <1>1), i.e. (G); thm:group — STANDS. The objection
  to EF <1>1's 'for any unitary U' is right (my case (b), index -1: ||G||_2^2 = 1.0071 vs 2||C||_2^2 = 0.0071).

## 7. prop:ranges — STANDS WITH REPAIR (item 3 wording; item 2 inherits the item-6 GAP)
Constants recomputed (`python3 rigor/repair/ref_rp_4_constants.py > rigor/repair/ref_rp_4_constants.out`, mpmath 30 digits;
criterion: quoted decimal within half a unit of its last digit): f2 = 1/(12 pi^2) = 0.00844343197; (4 f2)^{-1/2} =
pi sqrt3 = 5.44139809; (2 f2)^{-1/2} = pi sqrt6 = 7.69529898 — all quoted values (5.4414, 7.6953) round correctly.
Direction ledger: every bound here is an UPPER bound on Phi (exact quantity, free-fermion zero-collar model); the
ranges only enlarge the domain where an upper bound holds; no comparison verdict is drawn.
Other steps needing the old restriction, checked in the printed proofs:
- item 1, RR lem:groupbound (l. 818-847): <1>2 (S_2 bound) has no range; <1>1 and <1>4 used index zero only. STANDS.
- item 2, RR thm:exactquad (l. 146-174): <1>1 and <1>4 used index zero only; <1>2-<1>3 rest on lem:autocorr (no range,
  but the general-chi (W) GAP of item 6). STANDS for PA's chi; general chi inherits the GAP (flagged by R1).
- item 3, RR thm:global (l. 180-208): <1>1 needs ||V|| < 1 and ||P_+W~P_-|| < 1; the first from <1>3
  (||V||_2^2 <= 2 f2^chi zeta^2 < 1), the second from thm:sv; no other range. The f2^chi-statement STANDS for every
  zeta with 2 f2^chi zeta^2 < 1. REPAIR (MINOR): the sentence 'at the infimum, Phi <= -(1/2)log(1 - 2 f2 zeta^2) for
  0 <= zeta < pi sqrt6' is not a consequence of thm:global: its infimum is f2^* over flows, and f2^* = f2 is NOT proved
  (RR prop:f2star and its verdictgap, l. 210-246: f2 <= f2^* <= 1.00071 f2). The f2-form on [0, pi sqrt6) comes only from
  prop:rrr (item 4). Replace 'at the infimum, ... f2 ...' in item 3 by 'with f2^star in place of f2^chi whenever
  2 f2^star zeta^2 < 1; the form with f2 is item 4'.
- item 4, RR prop:rrr (l. 848-880; s >= 0 only, cocycle <1>1): <1>3 needs ||V||_2^2 <= 2 f2^K zeta^2 < 1 (lem:groupbound,
  now every s) and ||P_+U P_-|| = ||V|| (thm:sv); <1>4: for zeta < pi sqrt6, f2 < 1/(2 zeta^2), so the qualifying h'
  still have infimum f2 (PA prop:infimum, l. 1247). <1>2 (both blocks HS, PA Cor. 2.7 after PA C2) has no range. STANDS.
  This is the range of the card rate-of-remainder; (W) there is PA's own lemma, no GAP.
- item 5, cor:quartic (l. 365-378): the product-family range zeta <= zeta_0 is from PA Prop. 4.5, unchanged. STANDS.
- item 6, NW thm:T3 (l. 688-736): removing s zeta_max < pi sqrt3: <1>5 needs per factor ||P_- e^{+-sigma K}P_+||_2 <=
  sigma ||P_-KP_+||_2 (lem:groupbound with index zero, now every sigma; lem:app-K, lem:app-prod (b)); <1>6 needs
  ||V||, ||P_+UP_-|| < 1, implied by s^2 Z^2 ||P_-KP_+||_2^2 < 1; <1>7 then needs only 2 f2^ s^2 Z^2 < 1, i.e.
  sZ < pi sqrt6. No other step uses the restriction. STANDS. lem:onegroup (i) (l. 955-962): only the same index use; STANDS.
- item 7, EF lem:group <1>1: STANDS for U_t (lem:app-EF).

## 8. Appendix A — STANDS (complete)
(l. 438-505.) lem:hsbasics (a)-(c): Tonelli on the double series, ||Tx|| <= ||T||_2 by completing x to a basis,
||T - T Pi_N|| -> 0, compactness by diagonal extraction + completeness: correct. lem:numrad: polarisation +
parallelogram, correct. thm:spec: <1>1 maximising sequence, ||Ax_n - lambda x_n||^2 <= 2 lambda^2 - 2 lambda <x_n,Ax_n>
-> 0 plus compactness gives an eigenvector with |lambda| = ||A||; <1>2 recursion on invariant subspaces H_k; <1>3-<1>6
expansion, Parseval, multiplicity bound m_A(lambda) <= ||A||_2^2/lambda^2. Separability is assumed and stated
(L^2(R), l^2(Z)). No external theorem; Sources section (l. 425-436) correctly marks Avron-Seiler-Simon and the
Fredholm logarithmic law NOT OBTAINED and NOT USED (lem:cubic (d) proved directly). The only external inputs of the
whole document are Stone's theorem and Nelson's core theorem, taken via PA lem:gen (a proved project document).

## 9. index_zero_check.py — reproduces; STANDS WITH REPAIR (the instance is valid but non-discriminating; one sentence false)
Rerun: `python3 rigor/index_zero_check.py > rigor/repair/ref_rp_4_rerun.out` (9.6 s); `diff rigor/index_zero_check.out
rigor/repair/ref_rp_4_rerun.out`: IDENTICAL. Validation (0) 5.1e-16 < 1e-10; (A) max |sv(B) - sv(C)| <= 4.4e-16 at
s = 0.5, 1.5, 3, 4, -3.5 (|s| ||[P-,K]||_2 up to 4.53 > 1, beyond the old range 0.8839 = 1/(0.8 sqrt2), recomputed);
(B) s = 1: sv 1 once in B, none in C; s = 1/2: ||C||_2^2 = 0.4474, 0.5172, 0.5873, 0.6574 (+0.070 per doubling; I recomputed
log2/pi^2 = 0.0702, 'no derivation here' correctly said). Faithfulness: (A) is an instance of lem:gen/thm:group
(K = iH bounded, [P-,K] rank 2, ||.||_2 = 0.8 sqrt2) — yes. Truncation bounds: (window) and (dropped |m-n| >= M) are
correct in kind; 'singular values move by at most the HS norm' summed over infinitely many dropped entries is stated
loosely ((window size) x entry bound), harmless at 1.6e-79.
FINDINGS (`python3 rigor/repair/ref_rp_4_model_check.py > rigor/repair/ref_rp_4_model_check.out`):
 (i) [MINOR] (A) cannot fail: H_A is real symmetric, so U_s = e^{isH_A} = U_s^T and B = C^T exactly (measured
     max |B - C^T| <= 2.9e-16 at s = 3, 4); equal singular values follow by transposition for every s, with no index
     theorem. 'no reflection symmetry' (l. 406-407) is true but beside the point.
 (ii) [MINOR] index_zero.tex l. 422-423 'The finite windows of (A) are not unitaries of index zero by construction' is
     inaccurate: U_N = expm(isH_N) IS a finite-dimensional unitary, whose full blocks have equal singular values
     automatically; the inner read-out differs from them only by the truncation error. Demonstration: the circular
     (unitary-window) version of the index -1 shift gives sv 1 in BOTH blocks. Hence (A) checks the instance (true)
     but cannot discriminate the theorem from a false one; (B) is a different read-out (non-unitary sinc window).
 (iii) A model without (i) (complex next-nearest-neighbour hopping i*0.4, not gauge-removable; ||[P-,K]||_2 = 1.3254,
     old range |s| < 0.7545): at s = 2, 4, -3.5, max |B - C^T| = 0.57-0.68 but max |sv(B) - sv(C)| <= 5.6e-16 < TOL and
     Tr G^3 (inner window) <= 1.3e-15: the instance agrees; same finite-window caveat (ii).
 Repair: replace the sentence of (ii) by 'U_N is a finite unitary, so (A) checks the instance up to truncation and
 cannot detect a failure of the theorem'; use a model without transposition symmetry or say that (A) has it.
 A discriminating check needs an unbounded K with U_s not norm continuous (where Fredholm stability does not already
 give the result); none is in the project. This does not affect the proofs, which I verified line by line.

## 10. R1_patch.json — items 1-11 STAND WITH REPAIR (general-chi qualifier); item 0 STANDS (one stale entry); item 12 STANDS
Items 1-11 (rate_of_remainder.tex): every new sentence carries 'under review' (checked all 11). Label numbers checked
against rigor/index_zero.aux: Lemma 4.1 = lem:blocks, Thm 4.2 = thm:sv, Thm 5.1 = thm:group, Lemma 5.2 = lem:gen,
Lemma 6.1 = lem:app-W, 6.2 = lem:app-K, 6.3 = lem:app-prod, Thm 3.1 = thm:path — all correct.
- Items 4, 5 (lem:groupbound <1>1, <1>4), 6, 7, 8 (prop:rrr, its box), 9 (C3 (ii) 'settled for every s ... until that
  review passes it is open'), 11 (cor:quartic product family, PA's chi, lem:app-prod (a)): true and not stronger than
  index_zero.tex. STAND.
- Items 1, 2, 3 (thm:exactquad <1>1, <1>4; thm:global <1>3) and 10 (C3 (i)) say index zero holds for W~_s 'for every real s'
  by Lemma 6.1, in theorems stated 'for every admissible field chi'. Lemma 6.1 is conditional on (W), which for a
  general admissible chi is the item-6 GAP. [MINOR] STRONGER than index_zero.tex supports for general chi: add
  'for chi satisfying (W) of index_zero.tex Lemma 6.1 (PA's field; for general admissible chi as asserted in
  lem:autocorr)'. Item 10's 'is proved' should read 'is proved for chi satisfying (W)'.
  (Alternative repair: the complex-conjugation argument of card pushforward-blocks-equal-singular-values gives index
  zero of W~_s for every admissible chi without (W), once G_s in S_2 is known.)
Item 0 (uhlmann_upper_bound.tex lem:wick <2>1; BJL Theorem 7.1). Read refs/BJL_twisted_duality_math-ph-0204029.pdf
(pdftotext): Thm 2.1 (i)-(iii) p. 4; basis projection P + Gamma P Gamma = 1 and Fock state eq. (2) p. 4; Z 'the
implementation on F of the even-oddness automorphism', Z = Z^* = Z^{-1}, eq. (4), p. 5; M(q) eq. (7) and twist
Z~ = (1 + iZ)/(1+i), eqs. (8)-(9), p. 7-8; complex case h = H + H, Gamma = [[0,gamma],[gamma,0]], diag(P, gamma P^perp gamma),
p. 25 (Sec. 6); Sec. 7 set-up 'any basis projection, any closed Gamma-invariant q' and Thm 7.1 M(q)' = Z~ M(q^perp) Z~^*,
p. 26-27. Hypotheses re-checked one by one: Gamma anti-unitary involution; a(f + g) := a(f) + a^*(gamma g) antilinear,
a(F)^* = a(Gamma F), {a(F), a(G)^*} = <F,G> (expanded); frak P = diag(P_-, gamma P_+ gamma) a basis projection (sum = 1
computed); omega = omega_frakP: with PA eq:qf (l. 53) omega(a^*(f)a(g)) = <g, P_+ f>, so omega(a^*(f)a(f)) = 0 for
f in P_-H and omega(a(h)a^*(h)) = <h, P_- h> = 0 for h = gamma g in P_+H, cross terms vanish by gauge invariance — correct;
q = L^2(I) + L^2(I) closed, Gamma-invariant, M(q) = M, q^perp gives F(I') (null set) — correct.
Twist identification: R1 marks it as resting on a paraphrase of p. 5 with source [4] NOT OBTAINED. I find it is
fully supported by the PDF itself: p. 8 states Z~(p_1 ^ ... ^ p_n) = eta(n) p_1 ^ ... ^ p_n with eta = 1 (n even),
-i (n odd), and Z~ = E+ - iE-, eq. (9); with Z~ = (1+iZ)/(1+i) this gives Z = +1 on even, -1 on odd n, so Z Omega =
Omega; together with 'Z implements the even-oddness automorphism' (p. 5) and irreducibility of the Fock
representation, Z = V (both implement the grading and fix Omega). The sign-irrelevance argument (Z -> -Z gives
-i Z~^*; Z~^2 = Z; Z~^* N Z~ = Z~ (Z N Z) Z~^*) I re-derived: correct. Verdict on item 0: STANDS; the
'paraphrase / NOT OBTAINED' caveat is unnecessary (p. 8, eqs. (8)-(9) suffice) — not an error.
[MINOR] stale entry: uhlmann_upper_bound.tex l. 1394-1396 ('Imported, with locator') still lists twisted duality as
'Foit ... Thm 1. Used only in Lemma lem:wick <1>1. Screenshot NOT OBTAINED'; it should name BJL Thm 7.1 with the
shots r1_BJL_*.png (present in rigor/shots/). The shots are new files: ./pgit sync needed (orchestrator).
Item 12 (quadratic_limit.tex sec:summary status line): true — the status update at l. 1302 exists and card
thm-a-quadratic-law is refereed. STANDS.

## 11. Cards
- rate-of-remainder [proved, modulo two weak-link cards] — PASS. The 2026-11-19 Statement: (2) 'proved for zeta < pi sqrt3
  = (4 f2)^{-1/2}; for pi sqrt3 <= zeta < pi sqrt6 = (2 f2)^{-1/2} subject to index zero of e^{sK}, rigor/index_zero.tex,
  under review' — accurate: the f2-bound route is prop:rrr (PA's chi, (W) holds by PA), whose remaining hypothesis is
  exactly lem:app-K/thm:sv, which I find STANDS. Numbers pi sqrt3 = 5.4414 -> '5.44', pi sqrt6 = 7.6953 -> '7.70'
  recomputed (ref_rp_4_constants.out). The Index-gap passage still describes the documents correctly (C3 now says
  'settled ... by index_zero.tex, under review; until that review passes it is open'). Nothing stronger than the
  evidence; depends unchanged and right. After promotion of group-index-zero-large-s the card may drop 'subject to'.
- const-f2 [proved] — PASS. 8/(12 pi^2) = 0.0675474558 -> 0.0675 (the old 0.0676 mis-rounded the exact value; it is the
  rounding of 8 x 0.008444(1) = 0.06755(1), so fidelity_recovered_quasifree.tex:464 '0.0676(1)' stays consistent within
  its uncertainty); 2 f2 = 0.0168869 -> 0.0169; f2 = 0.0084434 c. Recomputed, mpmath, ref_rp_4_constants.out.
- group-index-zero-large-s [conjectural] — FAIL (card as it stands is inaccurate, not the claim): the title says
  '(open; no document contains an argument)' and How to verify quotes C3 'The rest needs a standard Fredholm-index
  continuity argument that no document contains, and is open' — that sentence was REPLACED by R1 patch item 9
  (rate_of_remainder.tex l. 1076-1078 now: 'settled for every s by rigor/index_zero.tex ... until that review passes it
  is open'). The Statement itself is correct and is proved by index_zero.tex thm:group + lem:gen + lem:app-K (the
  reading of '[P_-,K] Hilbert-Schmidt' as the form condition (K) on a core is the one RR lem:groupbound <1>2 uses).
  RECOMMENDATION: PROMOTE to proved: status proved, evidence doc:rigor/index_zero.tex#thm:group,
  doc:rigor/index_zero.tex#lem:gen, doc:rigor/index_zero.tex#lem:app-K, doc:rigor/index_zero.tex#thm:sv; title without
  '(open; no document contains an argument)'; How to verify: 'index_zero.tex thm:path (l. 125-148), thm:sv, thm:group,
  lem:gen, lem:app-K; numerical instance rigor/index_zero_check.py (non-discriminating, REF_RP_4 item 9)'. Then a
  second look by one referee (status change re-opens review).
- pushforward-blocks-equal-singular-values [heuristic] — report only. Its Statement is 'for EVERY admissible chi'.
  index_zero.tex lem:app-W proves it only for chi satisfying (W): PA's field (fully) and general admissible chi only via
  the assertion of RR lem:autocorr (item 6 GAP). RECOMMENDATION: DO NOT PROMOTE as stated on the basis of index_zero.tex.
  Either (a) narrow the Statement to chi satisfying (W) (PA's field) and promote with evidence
  doc:rigor/index_zero.tex#lem:app-W; or (b) write the one-line complex-conjugation argument (W~_s C = C W~_s,
  C P_+ C = P_-; it needs no (W) and no index theory) as a proof in a document, then promote for every admissible chi.

## Summary of verdicts and promotion recommendation
Proofs of index_zero.tex: lem:kernels, lem:sym, lem:cubic, thm:path, lem:products, lem:blocks, thm:sv, thm:group,
lem:gen, lem:app-K, lem:app-prod (a),(b), lem:app-EF, Appendix A: STAND. lem:app-W: STANDS (conditional on (W)); (W)
for general admissible chi is a pre-existing GAP (RR lem:autocorr). lem:app-prod (c): STANDS WITH REPAIR (state (W)).
prop:ranges: STANDS WITH REPAIR (item 3 wording; f2-form only via item 4). index_zero_check: reproduces bit-for-bit;
STANDS WITH REPAIR (non-discriminating, l. 422-423 inaccurate). R1 patch: items 4-9, 11, 12, 0 STAND; items 1-3, 10
MINOR (general-chi qualifier); item 0 leaves a stale Foit entry at uhlmann_upper_bound.tex l. 1394-1396.
kb verdicts: rate-of-remainder pass; const-f2 pass; group-index-zero-large-s fail (stale title/How to verify; promote).
Promotion: group-index-zero-large-s PROMOTE; pushforward-blocks-equal-singular-values DO NOT PROMOTE as stated.
No AGENTS.md §9 trigger: no proved/refereed card is contradicted; the general-chi GAP is pre-existing and recorded.
