# C2 report — Theorem B (universality) — REF-COUNCIL-C2

## 0. Scope and method
Seat C2, actor REF-COUNCIL-C2, adversarial. Documents read: rigor/universality_theorem_B.tex (UB, 1179 l.),
rigor/implementation_C11.tex (C11, 1058 l.), rigor/lemma_second_variation.tex (LSV, imported halves),
universality_normalization.tex (Note 7), paper2/main.tex + sec_setting/sec_intro/sec_outlook (inheritance only).
Cards: thm-b-universality, implementer-hypotheses, second-variation-lemma, bures-three-faces,
const-gb-general-nets, stress-tensor-normalisation, boson-check (+ const-gb, petz-zero-collar-channel,
mobius-reduction-cross-ratio for inheritance). PDFs opened with pdftotext: refs/P1_CarpiWeiner_math-0407190.pdf
(CW05), refs/CDIT_1808.02384.pdf, refs/FewsterHollands05_math-ph-0412028.pdf. KB read-only; no kb writes.

## 1. Verdict table
| statement (file:label, line) | verdict | step / reason |
|---|---|---|
| UB thm:B eq:B (l. 857-891), half-line chart, under (H1)-(H3) | STANDS | <1>1-<1>4 re-derived; uses (H1) only via Psi_s = U_s^* Omega |
| UB thm:B combined with C11 thm:main ("every net") | STANDS WITH REPAIR | F3: UB (H1) contains a locality clause for C^{1,1} phi that C11 does not prove; eq:B does not use it -> state (H1) in C11's (C7) form |
| paper2 lem:ext (sec_setting.tex) | FAILS (proof) | F3: U(phi) for C^{1,1} phi undefined; fix = C11 thm:H1 <1>7 (s >= 0, class E only) |
| paper2 title / sec_outlook l. 2 ("Petz recovery error") | FAILS (overclaim) | F1: Petz = compression proved for the free fermion only |
| paper2 abstract l. 32, sec_setting l. 43-45 (general cross ratio) | STANDS WITH REPAIR | F2: Moebius reduction carded for the free fermion only; general-net proof missing (short) |
| UB prop:H3 (lower bound on -log F, l. 290-357) | STANDS | Alberti-Uhlmann step and *-strong density step checked; sign of phi checked |
| UB prop:H2 (upper bound, l. 392-426) | STANDS | (H2) = (V) of LSV; LSV thm:lower (l. 871-910) re-checked |
| UB prop:geom (l. 428-474) | STANDS WITH REPAIR | postulates e^{i tau T(h)} = U(phi'_tau) for C^{1,1} h; only e^{i tau T(h)} in M' is needed, which C11 thm:H1 <1>2 proves |
| UB lem:ext (l. 178-210) | STANDS (conditional) | true given UB's postulated clause; the clause is unproved (F3) |
| UB lem:gauge, def:a | STANDS | |
| UB lem:reduce, prop:reduce, thm:linear (c-linearity, l. 517-622) | STANDS | robust: the transported Delta_0, J_0 are the actual geometric action, identical for all nets with BW; a sign slip in the description could not break universality |
| UB rem:klein (graded fermion) | STANDS | Z = 1 on even vectors; H_T is even |
| UB thm:value gamma_0 = 2/(3 pi^2) (l. 734-776) | STANDS (conditional on C1 scope) | rests on uhlmann_upper_bound prop:infimum + quadratic_limit Prop 5.1; independent numerical support section 8 |
| UB lem:RST, lem:standard(4) | GAP (admitted, unused by thm:B) | numerically supported to 5.9e-5 (section 8) |
| C11 thm:reg (b),(c),(f) | STANDS | (f) and the n^-3 tail with |J| = 1/L confirmed numerically (section 8) |
| C11 lem:dirsum, lem:phase, lem:loc-HT | STANDS | lem:dirsum unnecessary (CW05 S4 is for reducible reps); F6 MINOR |
| C11 thm:H1 (i),(ii) s >= 0, (iii) all s; thm:H23; thm:main | STANDS | for (C7)-form hypotheses, every conformal net in the CDIT S4 sense |
| LSV thm:lower, thm:upper, thm:main (fidelity half under (V)) | STANDS | |

KB: thm-b-universality [refereed] OK, Statement should name the half-line chart (F2, MINOR);
implementer-hypotheses [refereed] OK for the (C7) form, not for UB's (H1) (F3); second-variation-lemma [proved] OK;
const-gb-general-nets [proved] OK (half-line chart); bures-three-faces [proved] not re-derived;
stress-tensor-normalisation [proved]: normalisation consistency of UB eq:normTg and C11 thm:reg(f) confirmed
numerically, check_notes_6_7.tex thm:TT not opened; boson-check [numerical] not rerun.

## 2. Findings (BREAK / GAP / MINOR) with inheritance (kb deps)
No [BREAK] found in the proof of eq:B (UB l. 865-868) for the half-line geometry it states. The two [BREAK]s
below are for paper 2 (a paper sentence stronger than its card; a paper proof using an undefined object), and
neither touches eq:B.

F1 [BREAK, paper 2 only] paper2/main.tex:19 (title "Universality of the Petz recovery error"), paper2/sec_outlook.tex:2
("Theorem B computes the error of \emph{the} zero-collar Petz recovery"), paper2/sec_intro.tex:5-19 --
Theorem B is a statement about omega_s = omega o Ad U_s|_{A(I)}, U_s implementing the geometric compression
(UB thm:B l. 860-861; C11 thm:H23). That this curve is the zero-collar (t -> infinity) limit of the FHSW rotated
Petz maps is proved ONLY for the free fermion (card petz-zero-collar-channel: "For the r-component free chiral
fermion ..."; Note 4 uses CAR quasi-equivalence). No document or card proves it for a general net. The paper
sentence is stronger than any card. Repair: either prove Petz(t) -> Ad U_s for general nets (BW makes the modular
flows geometric, but the Petz map also contains the adjoint of the inclusion, whose geometric form is the quasi-free
content of Note 4), or retitle/reword "error of the geometric (zero-collar) recovery". Inherits: paper2 title,
abstract l. 27-31 ("the recovery error"), sec_outlook l. 2; card thm-b-universality's TITLE is safe (it says f2),
but its use as "Petz" error in paper 2 is not.

F2 [GAP] paper2/sec_setting.tex:43-45 and paper2 abstract l. 32 ("zeta the cross ratio of the four endpoints") --
the passage from a finite configuration (-a, 0, L) to the half-line chart a = infinity for a GENERAL net is
attributed to "[Note5, Lemma 1.1]". Card mobius-reduction-cross-ratio states it "For the chiral free fermion"
(proof via the half-density action and the Hardy projection; finite configurations only, a = infinity via the
fermionic prop:closed). UB (S3) l. 90-92 uses the same citation. UB thm:B itself is stated only for
A = (-infinity, 0) (l. 859-860), so thm:B is unaffected; the general-a statement is unproved, though a short
argument exists (Moebius U(g) with vacuum invariance, g o k_s o g^{-1} again parabolic fixing g(0), plus
extension independence C11 thm:H1 <1>7). Inherits: paper2 abstract, sec_setting; card thm-b-universality if read
for finite a (its Statement does not fix the geometry -- [MINOR] there: it should say "half-line chart, zeta = s").

F3 [GAP] UB (S4) (H1), l. 116-126, versus C11 (C7) (H1), l. 120 -- UB's (H1) contains a locality clause
"U_s = U(phi) U_s^sharp (up to a phase) whenever U_s, U_s^sharp implement two C^{1,1} extensions that differ by
phi" with U(phi) for a C^{1,1} (non-smooth) phi; U is only defined on smooth Diff+(S^1) (CDIT axiom (10)), and C11
neither defines nor proves this clause. C11 thm:main (l. 792-800) proves the weaker (C7) form. Hence the KB claim
"(H1)-(H3) hold for all nets" discharges thm:B's hypothesis (H1) only after the clause is dropped. Not load-bearing
for eq:B: thm:B <1>1-<1>4 (l. 869-881) use (H1) only through Psi_s = U_s^* Omega (prop:H3 <1>1, prop:H2 <1>1).
It IS load-bearing for UB lem:ext (l. 178-210, extension independence) and prop:geom <1>1 (l. 444-448, where
U(phi'_tau) for C^{1,1} h is also postulated). Repair: in thm:B replace (H1) by C11's (C7) form, and replace lem:ext
by C11 thm:H1 <1>7, which proves extension independence -- but only for s >= 0 and within C11's class E
(C11 l. 633: "For x in A(I) and s >= 0").
PAPER 2 IS WORSE: paper2/sec_setting.tex H1 (l. 100-112) restricts the clause to smooth phi in Diff+(S^1), but its
lem:ext proof then applies it to phi = k~_s o (k~_s^sharp)^{-1}, which is only C^{1,1} ("By the locality clause
(eq:H1loc) with K = J_s' we get U(phi) in A(J_s')"). U(phi) is undefined there and the step is invalid as written;
that U_s (U_s^sharp)^* acts trivially on A(J_s) is exactly what has to be proved (C11 <1>7 does it by Trotter, s >= 0,
class E). F3b [BREAK, paper 2 only, not load-bearing for eq:B]: paper2 lem:ext proof invalid as written;
its statement (arbitrary C^{1,1} extensions, both signs of s) is unproved, true for s >= 0 within class E by C11. Inherits: cards thm-b-universality (assumes implementer-hypotheses),
const-gb-general-nets; paper2 sec_setting l. 95-96 ("stated here in the exact form in which they are used, and
they are verified for every ... net") if paper2 copies UB's form (not checked line by line: C6).

F4 [MINOR] UB summary table l. 1039-1040 says lem:ext is "proved, from (HD) and the locality clause"; the proof
(l. 199-201) explicitly avoids (HD). UB l. 1025 "I = ABC" vs (S3) "I = AD": naming drift.

F5 [MINOR] universality_normalization.tex (Note 7) title l. 140 "f_2 = c/(12 pi^2) and s_2 = c/12" and l. 202,
l. 317 box state s_2 = c/12 as derived; card conj-s2 is conjectural. l. 157 states the remainder
"c_3 f_2 zeta^3 + O(zeta^4), c_3 = -0.99(1)" as established; card remainder-c3-c4-values is heuristic. The body
(l. 301) carries the correction, the title and boxes do not.

F6 [MINOR] C11 lem:phase <1>3 (l. 491-495) relies on simplicity/perfectness of Diff(I_f), cited, not verified
(C11 says so). Avoidable (see section 3).

## 3. Cited-source hypothesis checks (Carpi-Weiner, Fewster-Hollands, ...)
Checked against the PDFs (pdftotext; page = printed page):
- CW05 Thm 4.4 (p. 13): closability / e.s.a. of sum a_n L_n on D^fin when sum |a_n||n|^{3/2} < inf. Section 4 of CW05
  (p. 10, "Throughout this section let V be a positive energy representation of Diff+(S^1)") is stated for a
  GENERAL (reducible) positive-energy representation; Lemma 4.1's constant r depends on c only. So the hypotheses
  are met in the vacuum representation of any conformal net directly; C11 lem:dirsum (via CDIT Prop 3.14, irreducible
  decomposition) is correct but not needed. OK.
- CW05 Prop 4.5 (p. 14): energy bound ||T(f)v|| <= r ||f||_{3/2} ||(1+L0)v|| and e^{iT(f_n)} -> e^{iT(f)} strongly
  for continuous real f, f_n of finite 3/2-norm. Quoted verbatim correctly in C11 l. 283-290. OK.
- CW05 Lemma 4.6 (p. 14): support-preserving mollification. C11's caveat (support must be compact in I; conclude by
  semicontinuity) is correct and is applied in C11 thm:H1 <2>1-<2>4. OK.
- CW05 Prop 5.4 (p. 17): Trotter + localisation template. Used correctly in thm:H1 <1>4 (s >= 0 only). OK.
- CDIT S4 axioms (p. 22): Diff+(I') := {gamma : gamma(z) = z for all z in I}, i.e. support in the CLOSED arc;
  this is the form (H1loc) of UB (S4) l. 123-126 and C11 lem:loc-HT(i). Additivity/semicontinuity automatic. OK.
- CDIT Prop 4.1 (p. 23): approximation + additivity + semicontinuity. Rerun in C11 thm:H1 <1>6 with Stone's
  theorem replacing CDIT Prop 3.6; the substitution is legitimate (only strong convergence U(phi_n) -> U_s and
  uniform convergence phi_n -> k~_s are used, both proved in <1>5). OK.
- FH05 Prop 5.1 (p. 27): global multiplier section for the irreducible U^(c,h), quoted verbatim correctly.
  C11 lem:phase <1>3 additionally cites perfectness of Diff(I_f) from memory-level literature (C11 itself marks it
  "cited but not re-verified"); [MINOR], and avoidable: on a positive-energy rep the generator T(f) is fixed globally
  by the Virasoro relations, so U(Exp(tf)) = scalar * e^{itT(f)} already from the one-parameter lift.
- Not obtained/not checked by me: Brunetti-Guido-Longo 1993 and Longo's notes (UB lem:RST, (BW1)); UB itself marks
  them NOT VERIFIED and they are not used by thm:B (confirmed: thm:B <1>1-<1>4 cite only prop:H3, prop:H2,
  thm:linear, thm:value). Foit RIMS 1983 (twisted duality, used in thm:value via uhlmann_upper_bound prop:infimum)
  is cited without screenshot (uhlmann_upper_bound.tex l. 1263-1264).

## 4. (H1)-(H3): all nets or a class?
ALL conformal nets in the sense of CDIT S4 axioms (1)-(10) (separable H, Moebius covariance, positive energy,
unique vacuum, Diff+(S^1) covariance with the closed-support clause), any c > 0, for the half-line chart with
g_tot in C11's class E (E1)-(E3) (UB's g_tot = -x^2 beta(x-1) on x > 0 is in E for every a > 0, L = 1). This
holds for the (C7) form of (H1) (C11 l. 116-130): implementers of k~_s on every interval, for every s. Inputs
verified against the PDFs (section 3); essential self-adjointness needs only ||g_tot||_{3/2} < inf, which holds
(single jump of G'' -> |G_n| ~ |J|/(2 pi n^3), confirmed numerically: tail model with |J| = 1/L reproduces the
direct line-quadrature norm to 1.3e-11). NOT covered: (a) UB's extra locality clause for C^{1,1} phi (F3);
(b) extension independence for s < 0 (C11 <1>7 is s >= 0 only); (c) several touching points / compositions
(C11 S8(b) says so); (d) graded (fermionic) nets: C11 thm:main is for local nets; for the Dirac net (H1)-(H3) are
in uhlmann_upper_bound (one component; (H2') and r >= 2 open per UB Correction C2) -- immaterial for Theorem B,
because the fermion enters only through thm:value, which uses neither (H1)-(H3) of the fermion nor thm:B.

## 5. c-linearity (H_T) argument
Re-derived step by step (UB lem:reduce, prop:reduce, thm:linear). The argument is correct and does not depend on
the analytic-continuation prescription of Note 7:
(i) H_T = closed complex span of T(f)Omega, f in C_c^infinity(R; R), is invariant under Delta^{it} (dilations about
x = L, Moebius, so no Schwarzian c-number) and under J (reflection; for the fermion J = Z Theta with Z = 1 on even
vectors), hence reduces Delta and J; (ii) the real-orthogonal projection E'a onto H_M' is a bounded Borel function
of Delta applied to a and Ja, hence lies in H_T when a does ((H2'), proved in C11 lem:loc-HT(ii)); (iii)
<T(f)Omega, T(g)Omega> = (c/48 pi^2) int_0^inf p^3 conj(f^) g^ dp, so V: K -> H_T is unitary up to c, and
Delta|H_T, J|H_T are the SAME geometric action transported, for every net with BW. Robustness: the conclusion
"g_B/c is net independent" survives any sign slip in the written description of BW, because Delta_0 is defined as
the actual action; the value is then taken from one net (the fermion). Hypotheses used: (TT) normalisation, BW,
(H2'); not HD, RS, locality (true as claimed). The fermion's M = F(I) (full CAR algebra, twisted duality) and a
local net's M = A(I) give the same reduced data on H_T, so the transfer is legitimate.

## 6. Constant chain c/(12 pi^2)
(TT) <T(x)T(y)> = (c/8 pi^2)(x-y-i0)^{-4} (generator normalisation; BPZ T/(2 pi)) -> FT of (u-i0)^{-4} is
(2 pi/3!)|p|^3 theta(-p) (re-derived from 1/(u-i0) -> 2 pi i theta(-p)) -> ||T(f)Omega||^2 = (c/48 pi^2) int_0^inf
p^3 |f^|^2 dp (UB eq:normTg) = (c/12) sum_{n>=2} n(n^2-1)|G_n|^2 (C11 thm:reg(f)); the two agree numerically to
2e-16 on exp(-x^2) (exact 1/(24 pi)) and to 1.3e-11 on g_tot (section 8). -> fermion dist^2 = 1/(6 pi^2) at c = 1
(uhlmann_upper_bound prop:infimum, C1 scope) -> g_B = 4 dist^2 = 2c/(3 pi^2) -> -log F = (s^2/8) g_B
(LSV: 1 - F = (s^2/2) dist^2 + o(s^2), and -log F = 1 - F + O((1-F)^2)) -> f_2 = g_B/8 = c/(12 pi^2) = 0.0084434 c,
zeta = s at a = infinity. Every factor checked; no drift between UB, C11 and paper 2 found. Note 7's spectral
route (eq:gB-int) is correctly labelled a prescription by UB (verdict box l. 793-822).

## 7. Direction ledger
| evidence | quantity | model | direction |
|---|---|---|---|
| UB prop:H3 | -log F(omega, omega_s) exact | any net, (H3) | lower bound >= (s^2/8) g_B + o(s^2) |
| UB prop:H2 | same | any net, (H2) | upper bound <= (s^2/8) g_B + o(s^2) |
| UB thm:value | g_B exact | fermion value + c-linearity | equality |
| UB prop:geom | -log F | any net | upper bound (s^2/2)||T(g_tot+h)Omega||^2 for each h |
| this seat, c2_gB_check (B) | inf_h ||T(g_tot+h)Omega||^2 | c = 1, Rayleigh-Ritz | UPPER bound on inf_h, hence (with inf_h >= g_B/4) an UPPER bound g_B <= 4 U_N |
| UB sec:num, referee box-free check | same as above | line chart | upper bounds on inf_h |
eq:B needs the lower and upper bound of the same exact quantity: both present. The numerics of section 8 can only
REFUTE (if U_N < g_B/4) or be consistent; they bound g_B from above, never from below, so they confirm neither the
fermion value nor lem:RST by themselves.

## 8. Independent numerical checks
Script rigor/council/c2_gB_check.py, output rigor/council/c2_gB_check.out; command (repo root):
`${PYTHON:-python3} rigor/council/c2_gB_check.py > rigor/council/c2_gB_check.out` (system python3, numpy 2.5.2,
scipy 1.18.1; the scratchpad venv build had failed). c = 1, L = 1, beta = smooth exp-ratio step. Tolerances fixed
in the script before the run. Modes: circle Fourier modes 2 <= n <= 16384 resolved (FFT, M = 2^18); n > 16384
added by the analytic tail |G_n| = |J|/(2 pi n^3), J = -1/L (C11 thm:reg(b)); weight of the tail ~ 3e-11.
- (V) validation, exactly known case f = exp(-x^2): circle sum 0.013262911924325 vs 1/(24 pi) = 0.013262911924325,
  rel. dev 2.2e-16 < tol 1e-9. PASS. (Validates that UB eq:normTg and C11 thm:reg(f) are the same normalisation.)
- (A) ||T(g_tot)Omega||^2 / c: line Gauss-Legendre quadrature (+ p^-3 tail) 0.1947699503; circle FFT (+ n^-3
  tail) 0.1947699503; rel. dev 1.3e-11 < tol 1e-6. PASS (two algorithms, no shared code beyond numpy/scipy).
  Ratio to the claimed g_B/4 = 1/(6 pi^2) = 0.0168868639: 11.53 >= 1, as dist(a, H_M')^2 <= ||a||^2 requires.
- (B) Rayleigh-Ritz on the compact arc I' = (pi/2, pi) (circle chart; basis Chebyshev x (theta-pi/2)^2(pi-theta)^2,
  least squares by SVD): U_N / (1/(6 pi^2)) = 1.7197 (N=16), 1.0752 (32), 1.01018 (48), 1.00210 (64),
  1.000188 (96), 1.000059 (128); monotone from above, never below (refutation threshold 1 - 1e-6 not crossed).
  This is a check independent of UB sec:num (line chart, FFT box) and of the earlier referee's box-free line
  check (2.547971 = (1 + 5.9e-4) 8/pi): different chart, basis and solver; it tightens the bracket to
  inf_h ||T(g_tot+h)Omega||^2 in [g_B/4, 1.000059/(6 pi^2)] at c = 1, i.e. g_B <= 2c/(3 pi^2) (1 + 5.9e-5).
  Single-method statement for the upper bound; not a proof of the value (direction ledger, section 7).
No other number in the C2 cards was recomputed (boson-check NOT rerun; see section 10).

## 9. Earlier referee reports: were repairs applied?
(Read after forming the view above.)
- rigor/referee_universality_theorem_B.tex S r:edits (l. 667-685), five edits: (1) (H2') clause -- APPLIED
  (UB l. 141-150); (2) locality clause restated as U(Diff(K)) in A(K) -- APPLIED (UB l. 116-126), but the
  referee did not object to the second half of the clause, "U_s = U(phi) U_s^sharp" for C^{1,1} phi, which is
  the residue F3; (3) graded/Klein -- APPLIED (rem:klein, thm:value <1>2, thm:linear statement); (4) prop:H3 <1>4
  density -- APPLIED (l. 320-322); (5) rem:H2H3 -- APPLIED; "Haag duality -> locality" -- APPLIED in the proofs,
  NOT in the summary table (F4). The referee's box-free numerics reproduce (section 8 agrees and tightens).
- rigor/referee_implementation_C11.tex sec:verdict (l. 569-588): phase gap -- APPLIED (lem:phase, R1); form-bound
  BREAK -- APPLIED (prop:form, R2); factor 4, sign, standing assumptions, numerics box, Moebius unitaries -- listed
  as R3-R7 in C11 S corrections (l. 940-987). The referee itself records that Ad U_s|_{A(D)} is supplied only for
  s >= 0 ("which is the sign used"), consistent with F3's s >= 0 restriction. MINOR residue: C11 (C7) lists
  (H2') twice (l. 121-126).
- Card-level reviews (REF-DEP-CFT-B1/B2/B4, REF-CARD-OVER) checked locators and deps; none compared UB's (H1) with
  C11's (C7) (F3) or the Petz identification for general nets (F1).

## 10. NOT DONE
- uhlmann_upper_bound prop:infimum and quadratic_limit Prop 5.1 (the fermion value 1/(6 pi^2) feeding thm:value):
  not re-derived (seat C1 scope); section 8 bounds g_B only from above.
- bures-three-faces / LSV thm:three: not re-derived (accepted as imported; LSV lem:proj used in prop:reduce).
- stress-tensor-normalisation evidence rigor/check_notes_6_7.tex thm:TT: not opened; the (TT) -> eq:normTg step
  was re-derived by hand and validated numerically instead.
- boson-check (numerics/boson/boson_recovery.py): not rerun (time).
- paper2 copy of UB/C11 checked only for lem:ext, H1, title/abstract/outlook; line-by-line paper-vs-card table is C6.
- Brunetti-Guido-Longo 1993, Longo's notes (lem:RST, (BW1)): NOT OBTAINED (not in refs/); unused by thm:B.
- Foit RIMS 1983 (twisted duality, enters thm:value via prop:infimum): not checked (no PDF located in refs/).
