# REF-RP-3 report — repair round 2026-11-19 (papers: R4_patch.json, R5_patch.json)

Referee: REF-RP-3 (Opus). Adversarial stance. Brief: rigor/repair/REFEREE_BRIEF.md §3.

## Cards under verdict (failures first)
- paper1-status: FAIL. R4 items 25, 26 (sec_outlook.tex:105-106: "theta_fr >= 0.38", "at least 4/0.62 = 6.4") and
  31, 43 (sec_2d_lattice.tex:132, sec_intro.tex:101: "rigorous lower bounds") are stronger than the cards
  compression-not-optimal-exact-fidelity and large-zeta-values as changed this round; the outlook's bracket "[dual
  value, 0.616 f2 z^2]" (sec_outlook.tex:82, :105) has an estimated upper end. The card Statement itself repeats
  "E_rec <= (1 - theta_fr) f2 z^2 (1+o(1)) with theta_fr >= 0.38" and "the bracket [dual value, 0.616 f2 z^2]", and
  calls the S10 value "a taper-suppressed lower bound" (theta-value title: "no proved direction"). Repairs in (1), (2).
- two-branch-law-lattice: FAIL. Recomputed from numerics/lattice/petz_lattice.out (rigor/repair/ref_rp_3_lattice.py ->
  ref_rp_3_lattice.out): exponents 1.986, 1.912, 1.635, 1.151 ([3], eta <= 0.1) OK; factor exactly 2 at lambda = 0 ([2])
  OK; max single-branch factor 7574 ("7.6e3") OK. But (a) "between 4 and 7.6e3": section [2] has factors 3.87, 3.59,
  3.42, 3.24, 2.80 (lambda = 0.5, eta_V = 0.83-0.92) and 3.86 (lambda = 1, eta_V = 0.92), minimum 2.80; these rows are
  starred only because the LARGE branch of the two-branch prediction is extrapolated (out l. 284), which the
  single-branch value does not use. (b) "constant in eta": [6] at L = 4, lambda = 0.5 the ratio is 0.961-0.962 for
  eta_V <= 0.04 but 0.950, 0.922, 0.850, 0.752, 0.726 at eta_V = 0.08-0.33. (c) "1 - 0.15/L": [8] gives L(1 - ratio)
  = 0.1525, 0.1444, 0.1357 at L = 4, 6, 8 (mean over eta <= 0.05), drifting by 11%. Repair: "factors between 2.8 and
  7.6e3 (4.0 and up on the rows of [2] whose large branch lies in the range of Phi_lat)", "ratio 1 - a/L with
  a = 0.15, 0.14, 0.14 at L = 4, 6, 8, constant in eta for eta_V <= 0.05 only". Same wording in paper1/
  sec_2d_lattice.tex:118-120 ("between 4 and 7600 over the same data").
- phi-unconditional-linear-bound: FAIL (STANDS WITH REPAIR): How to verify cites only <1>1-<1>3; see (5).
- conj-s2: PASS. Statement verified against rigor/kubo_mori_gauge_lemma.tex eq:final (l. 597-603: limsup
  D_M(omega_s||omega)/s^2 <= 0.92418 c IF a gauge satisfies (V)) and eq:lowerb (l. 703-706, liminf of D_M(omega_s||omega));
  (11+5 sqrt5)/24 = 0.924180, 1/(3 pi^2) = 0.033774, c/12 / (c/(12 pi^2)) = pi^2, fermion 0.0837(5) covers my 0.08337
  and 0.08410 (fidelity_tables), boson 0.083(2) recomputed in (3). The 2026-09-24 REVIEW FAILED notes concern a note
  sentence that the author's second and third notes superseded; nothing in them is open against the Statement.
- boson-check: PASS. f2 = 0.00844(2) = midpoint of the fit range 0.008426-0.008457; s2 ranges free p / p = 1 / p = 2
  recomputed by an own refit (3); "-log F_b ~ (s^2/96 pi^2) int k^3 |ghat|^2": boson_recovery.out section 4 gives
  -log F_b = 1.16226e-5 vs s^2 Q/2 = 1.2095e-5 at s = 0.025, ratio 0.961 -> 1 linearly as s -> 0 (0.927 at 0.05; Tr(B*B)/(2 E_quad) = 0.997), with
  Q = (1/48 pi^2) int k^3 |ghat|^2: consistent with the stated second-order coefficient. Wording "a computation, not
  refereed as a proof" matches paper2 (R5 items 25, 26).
- paper2-status: PASS. All 38 R5 items checked: none stronger or weaker than its card (1); abstract, intro, outlook
  re-scanned (2); numbers (3); cor:tensor and the Fourier claim (4); 26 pp, clean log (6). MINOR, non-blocking:
  sec_outlook.tex "The free fermion the companion note" (ungrammatical after item 4); "Prop. 3.1" is Prop. 6.2 of the
  compiled rate_of_remainder.tex; cor:tensor should name U = U_1 x U_2. Statement "25 pp", "refereed (26 edits)" is
  dated 2026-09-24 and the 2026-11-19 note records 26 pp: true as dated.
- hellinger-coefficient-h2: PASS; see (5).

## (1) Patched sentences against their cards
### R4_patch.json (paper 1, 47 items) -- checked item by item against the current card texts
Items 0-11 (C6 A1/A2: Dirac restriction, o(eta^2), 8 f2 = two-chirality total, rem:twobranch-general): agree with
two-chirality-law [proved], two-chirality-law-general-cft [conjectural], const-f2, thm-a-quadratic-law,
two-chirality-minimum-at-lambda-zero (b) (not uniform in lambda). OK. (c+cbar)/(3pi^2) = 2 x 4 f2 per chirality: OK.
Items 13, 15, 44 (s2 vs g_KM): agree with const-gb [proved: g_KM = r/6] and conj-s2 [conjectural]. OK.
Items 14, 33-35, 38, 41, 42, 45, 46: locators/hypotheses; spot-checked (aux numbers in item 34/35 checked in (5)). OK.
Items 16, 20, 21 (range zeta < pi sqrt 3, r = 1): agree with rrr-bound-small-zeta [proved]. OK.
Items 17-19 (c3 ~ -1, no error bar): agree with remainder-c3-c4-values [heuristic]. OK.
Items 22, 24 ("Numerically, ... not the minimiser/not optimal"): agree with compression-not-second-order-minimiser. OK.
Items 27-29 (infimum attained only in the limit t -> infinity, factor 4 at leading order): agree with two-chirality-law. OK.
Item 30 (1 - 0.15/L, continuum exactness an extrapolation): agrees with two-branch-law-lattice. OK.

FAILS (stronger than the current card):
- [GAP] item 25, paper1/sec_outlook.tex:105: "$\theta_{\rm fr}\ge0.38$ (numerical: an extrapolation over finite meshes,
  every computed finite-mesh value lying below $0.38$, not a rigorous bound)". Card compression-not-optimal-exact-fidelity
  (Statement, changed this round, card_changes_1.json) reads "theta_fr ~ 0.384 +- 0.003 (extrapolated estimate, not a
  bound: ... finite-mesh values have no proved direction)". An inequality sign on an estimate the card says is not a
  bound is stronger than the card, and the sentence contradicts itself (">= 0.38" while every computed value is < 0.38).
  Repair: "$\theta_{\rm fr}\approx0.384\pm0.003$ (an extrapolated estimate, not a bound; every computed finite-mesh value
  is below 0.38)". The patch's reason quotes the card's pre-round wording.
- [GAP] item 26, same paragraph: "worse than the best channel by a factor of at least $4/0.62\approx6.4$ ... (numerical
  input $\theta_{\rm fr}\ge0.38$)". Direction ledger: Petz = 4 f2 z^2(1+o(1)) (equality, Theorem A at 2z); best channel
  <= (1 - theta_fr) f2 z^2 (1+o(1)) (upper bound, proved); a LOWER bound on the ratio needs a LOWER bound on theta_fr,
  which no card supplies (only theta_fr >= 0.0143 from G = R_a). "At least 6.4" is therefore not supported; the card
  supports "about 4/0.616 = 6.5 (numerical estimate)" or "at least 4/(1-0.0143)" if that bound is on a card.
- [GAP] items 31 and 43, paper1/sec_2d_lattice.tex:132 "The best rigorous lower bounds from thm:detrep ... give
  Phi_sub = 4.381e-3, ..." and paper1/sec_intro.tex:101 "rigorous lower bounds plus uncertified extrapolation".
  Card large-zeta-values (Statement changed this round) says the windowed bounds are "lower bounds for the exact
  compression; computed with the uncertified double-precision D-hat quadrature (rigor/certified_numerics.tex:421), so
  not certified"; certified_numerics.tex l. 418-420: "$\widehat D$ ... is \emph{not} certified here". Both reasons quote
  the old card wording ("rigorous windowed lower bounds", "certified ones"). Repair: "lower bounds (modulo the
  uncertified $\widehat D$ quadrature)". Item 32 (sec_numerics.tex:158, "produced by the certified pipeline" in its
  reason) is harmless in the text itself.

### R5_patch.json (paper 2, 38 items)
Items 0-3 (title "zero-collar compression error", Petz identification free-fermion only): agree with
petz-zero-collar-channel [proved, free fermion]. OK.
Item 4 (outlook rate): -1/2 log(1-2 f2 z^2) = f2 z^2 + f2^2 z^4 + ..., so "f2 z^2 (1+O(z^2))" and
"limsup (Phi - f2 z^2)/z^3 <= 0" follow; range z < pi sqrt 3 and c3 "about -1, unreproduced" agree with
rrr-bound-small-zeta and remainder-c3-c4-values. [MINOR] "rate_of_remainder.tex, Prop. 3.1": the compiled document
numbers prop:rrr as Proposition 6.2 (rate_of_remainder.aux:73, title "RRr Prop. 3.1"); a reader of that PDF finds 6.2.
Items 5, 33, 34, 36: OK (c = r for r Dirac fermions; aux locators prop:findim-id, thm:main 5.9 with 5.8 as stated).
Items 6-10, 35 (bracket for the REVERSED entropy D(omega_s||omega), conditional at both ends): checked against
rigor/kubo_mori_gauge_lemma.tex eq:final l. 601 (limsup D_M(omega_s||omega)/s^2 <= 0.92418 c IF a gauge satisfies (V)),
eq:lowerb l. 704 (liminf D_M(omega_s||omega)/s^2 >= ...), prop:Afails l. 272 ("(U_eps) fails for every admissible
gauge"). Agrees with conj-s2 [conjectural]. OK.
Items 11-18 (wording only; mathematics is REF-RP-1's): "class E", "s >= 0", "(C7) form", "no locality clause for
non-smooth maps" agree with card_changes_2.json (thm-b-universality, implementer-hypotheses). Item 17 "smooth h, so that
g_tot + h in E": supp h compact in I' = (L, infinity) (sec_setting.tex:49), disjoint from A = (-inf, 0) and D = (0, L),
so g_tot + h stays 0 on A and m on D: consistent. OK.
Items 19-21 (Moebius reduction for general nets "rests on an internal document under review"): card
moebius-reduction-general-nets is [proved] but its review is pending this round; the paper's wording matches the
review state, not weaker than a refereed card. OK (to be updated if REF-RP-1 passes that card).
Items 22-26 (boson): agree with boson-check [numerical]: s2 rests on the p = 1 tail law; c-linearity "a computation,
not a refereed proof". Numbers in (3). OK.
Item 27 (cor:tensor): see (4).
Items 28-31 (DIT NOT OBTAINED): refs/CDIT_1808.02384.pdf p. 24 (pdftotext), Outlook: "For all positive integers n and
some h, the irreducible unitary representation U(n,h) can be extended to D^s(S^1), s > 2 [DIT19]". The new sentence
reproduces this ("for every positive integer n and some h", sigma > 2) and marks DIT not obtained. OK.
Item 32 (BW1 named as companion gap; unsourced "known in the models" removed): OK.
Item 37 (Fourier convention): see (4).

## (2) Re-scan of abstract, introduction, outlook (both papers), after the patches
Paper 1 -- sentences stronger than their card:
- [GAP] paper1/sec_outlook.tex:105 and :106 (items 25, 26 of (1)): "theta_fr >= 0.38", "a factor of at least 4/0.62".
- [GAP] paper1/sec_outlook.tex:105 "The exact optimum is bracketed between the dual value of the programme and
  0.616 f2 z^2" and :80-82 (O-list) "bracketed between the dual value and (1-theta) f2 z^2 = 0.616 f2 z^2": the upper
  end is (1 - theta_fr) f2 with theta_fr an extrapolated ESTIMATE, not a bound (card compression-not-optimal-exact-
  fidelity: "kappa_opt <= 0.616 +- 0.003", estimate). Repair: "between the dual value and (1-theta_fr) f2 z^2, with
  1 - theta_fr = 0.616 +- 0.003 estimated numerically" (also note the upper end needs theta_HS = theta_fr, card rem. (i)).
- [GAP] paper1/sec_intro.tex:101 (tab:summary) "rigorous lower bounds": see (1), items 31/43.
- [MINOR] paper1/sec_outlook.tex:102-103 "the smaller value theta >= 0.30 of the spectral circle model ... is a lower
  bound" and :78 "a taper-suppressed lower estimate": card theta-value's TITLE (changed this round) says "S10's 0.300 is
  taper-suppressed; no proved direction", while its Statement and compression-not-second-order-minimiser still say
  "LOWER BOUND". The cards disagree with each other (REF-RP-2's seat); the paper follows the Statement. "lower
  estimate" is acceptable; ":102 theta >= 0.30 ... is a lower bound" is not, if the title is the intended content.
- Not stronger (OK): abstract (Dirac restriction, "conjecturally" for general CFTs; KM form c/12 "proved", D follows
  numerically to 0.5%: 0.0837(5)/0.083333 = 1.0044; 1e-4 and 0.3-1% checked in (3)); intro l. 71-73, 78-79, 86, 99, 114;
  outlook (O1) l. 55-62: Phi - f2 z^2 <= f2^2 z^4/(1-2 f2 z^2) follows from -1/2 log(1-x) <= x/2 + x^2/(4(1-x)),
  x = 2 f2 z^2 (checked by hand), range z < pi sqrt 3 stated.
- [MINOR, weaker] paper1/sec_outlook.tex:31 "Two gaps separate this from a theorem" (universality): Theorem B (card
  thm-b-universality, refereed) now is that theorem; the cross-reference was deferred (paper1-status note, C6 A13).
Paper 2 -- no sentence stronger than its card found in abstract, intro or outlook. Checked: abstract "we prove ...
c/(12 pi^2) zeta^2 + o(zeta^2) in the half-line normal form" against thm-b-universality [refereed] with
implementer-hypotheses [refereed: (H1)-(H3) hold for all nets]; "unconditional lower bound for generators in the
algebra" against km-exact-identity (thm:lower, "no further hypothesis"); "(11+5 sqrt5) c/12 = 11.09 c/6" against
km-gauge-lemma-refuted; bracket wording against conj-s2; boson wording against boson-check; outlook optimality against
two-chirality-law and two-chirality-minimum-at-lambda-zero; outlook DIT paragraph "not proved here".
- [MINOR] paper2/sec_outlook.tex, "The rate of the remainder": the patch (R5 item 4) left the sentence "The free fermion
  the companion note (...) proves the upper bound" ungrammatical (presumably "For the free fermion, the companion
  note"); same paragraph: "Prop. 3.1" is Proposition 6.2 of the compiled rate_of_remainder.tex.
- [MINOR] paper2/sec_intro.tex:21 "holds for every diffeomorphism covariant conformal net on S^1": the standing
  assumptions (separability, BW, HD, RS) are named only at l. 67-68; acceptable as the intro's summary.

## (3) Numbers introduced by the patches, recomputed
Script rigor/repair/ref_rp_3_numbers.py (own code; tolerances fixed in its docstring: half a unit of the last quoted
digit), output rigor/repair/ref_rp_3_numbers.out; validation: 1/k extrapolation of the exact law 1 - 2/k returns 1.0.
Command: `python3 rigor/repair/ref_rp_3_numbers.py > rigor/repair/ref_rp_3_numbers.out` (repository root).
- R4 item 39, fidelity_tables.tex: two-point 1/kappa_c extrapolation (kappa_c = log 1/eps) of 0.071785, 0.074268
  (Lambda = 120, kmax = 45) = 0.083372 -> "0.0834" OK (|diff| 2.8e-5 < 5e-5); 18.4/25.3 pair = 0.084100 -> "0.0841" OK.
  The Lambda = 240 rows give 0.08325 ("0.0833" in the reason) OK; Lambda = 120, kmax = 90: 0.08339. Naming the rows is
  right. Remark: the 25.3/32.2 spread over boxes (0.08325-0.08339) is 1.4e-4, comparable to the quoted 0.0837(5).
- R4 item 31, sec_2d_lattice.tex:133: largest-kappa_c Phi_sub at box 120/45 from numerics/results_largezeta_certified.txt
  = 4.381243e-3 (kc 39.14), 1.067246e-2 (39.14), 2.187202e-2 (39.14), 3.825878e-2 (43.75), 5.739516e-2 (39.14): all five
  quoted values reproduced within 5e-7. (Numbers OK; the word "rigorous" fails, see (1).) [MINOR] at zeta = 2.13 the
  Lambda = 60/kmax = 45 run gives a larger bound 1.067402e-2; "best" holds only within the 120/45 table.
- R4 item 26: 4/0.62 = 6.4516 ("~6.4" is a truncation; rounded 6.5). With the card's estimate 1 - theta_fr = 0.616 +-
  0.003 the factor is 6.46-6.53 (estimate). The only proved lower bound on theta_fr on the card (0.0143) gives 4.058.
  "At least 6.4" therefore is not supported (see (1)).
- R5 items 22, 24, boson (numerics/boson/boson_recovery.out, own refit of X = Xinf - b k^-p over kappa_c >= 2.3, three
  bases): header columns 3.41, 4.14 carry f2 0.0083508/0.0083832, s2 0.0724870/0.0745522 (N = 120, sigma = 1.6), and
  every other column of the table matches the same basis to the printed digits: OK. s2 free p: 0.080976-0.082376
  ("0.0810-0.0824" OK); p = 1: 0.083770-0.084193 ("0.0838-0.0842" OK); p = 2: 0.078183-0.078472 ("0.0782-0.0785" OK);
  f2 free and p = 2: 0.008426-0.008457 (OK); raw 0.0763 at kappa_c = 5.24 (0.0763220): OK.
- R4 item 12, abstract "0.3--1%" and "0.008 <= zeta <= 0.53": the zeta range is that of tab:scan (0.0083-0.5333): OK.
  The 0.3-1% is sec_numerics.tex:46, from rigor/check_note5_numerics.tex l. 576-586: at zeta = 1/120, eps = 1e-8 the
  applied correction 1.364e-8 exceeds the measured 8.724e-9 by 4.9e-9 = 0.84% of Phi = 5.8155e-7; at 1/15 the audit's
  12% of a 2.5% correction is 0.30%; the audit's own summary (l. 815) says "0.1--0.9%". Consistent: OK. "agrees with
  c/(12 pi^2) to 1e-4 relative": 0.008444(1) vs 0.0084434, relative 7e-5 (heuristic tail correction stated): OK.

## (4) R4 item 40 (prop:monotone), R5 item 27 (cor:tensor), R5 item 37 (Fourier sign)
- R4 item 40, paper1/sec_fidelity.tex:271-278: STANDS. The transcription matches card phi-monotone-in-zeta [proved,
  passed REF-DEP-CFT-B4] and rigor/check_note5_theory.tex prop:mono step for step: zeta(a) = as/(a+L) is increasing in
  a; I_1 = (-a_1, L) subset I_2; restriction of the normal map (uniqueness, thm:normal); root fidelity increases under
  restriction to a subalgebra, so -log F decreases: direction Phi(zeta_1) <= Phi(zeta_2) correct; realisation:
  a_i = zeta_i/(s - zeta_i), L = 1 gives a_i s/(a_i + 1) = zeta_i exactly (checked by hand), a_i > 0 iff s > zeta_i.
  The old semigroup sketch is gone. [MINOR] thm:normal (sec_petz.tex:108) is stated "for every s >= lambda",
  lambda = c/b; the proof fixes s without saying that lambda <= s is chosen (always possible, e.g. lambda = s, since
  Phi depends only on (a, L, s)); one clause would close it. Leftover fragment "It is also visible in tab:scan" is fine.
- R5 item 27, paper2/sec_universality.tex cor:tensor: STANDS WITH REPAIR (wording). The new proof is correct given its
  hypothesis: Theorem B applied to A_1, A_2 and A gives f2 = c/(12 pi^2) each, and c = c_1 + c_2 for T = T_1 x 1 +
  1 x T_2; the remark that additivity of ||T(g)Omega||^2 does not give additivity of g_B (a distance) is right and is
  why the old one-line proof failed. Repair [MINOR]: "assume that A = A_1 x A_2 does too" should say with the
  covariance U = U_1 x U_2 (Theorem B's c is that of the given representation; that T is the stress tensor of A, and
  hence c = c_1 + c_2, holds for this U, and otherwise needs uniqueness of the diffeomorphism symmetry, not cited).
- R5 item 37, paper2/sec_boson.tex:10-13: STANDS. With <J(x)J(y)> = -(1/4 pi^2)(x-y-i0)^{-2} and
  -(u - i0)^{-2} = int_0^inf p e^{-ipu} dp, <J(f)J(g)> = (1/4 pi^2) int_0^inf p [int f e^{-ipx}][int g e^{+ipy}] dp, i.e.
  conj(fhat) ghat for fhat = int f e^{+ipx} and fhat conj(ghat) for e^{-ipx} (app_conventions.tex:6). Numerically
  confirmed: rigor/repair/ref_rp_3_fourier.py -> ref_rp_3_fourier.out (Gaussian test functions, eps = 0.05,
  tolerance 1e-6 fixed first): e^{+ipx} with conj on fhat matches the position-space value to 6.3e-13, the other
  placement differs by 160%. "changes none of the quoted numbers": the quoted numbers use |fhat|^2 only: OK.

## (5) New cards phi-unconditional-linear-bound, hellinger-coefficient-h2
### thm:upper, first part (rigor/quadratic_limit.tex l. 807-858, Thm 6.3 in the current aux) -- read step by step
<1>1 Phi = sup_n Phi_{P_n}: Note 5 Thm 3.1 eq. (17) with Note 4 Lemma 10.1 (citedbox l. 248-260); covered by card
quasi-free-fidelity-formula (in depends). <1>2 lem:hell on P_nH (0 < Q_P < 1 shown after def:PhiP): Hell = det(S1S2 +
C1C2) re-derived (Gamma(G) calculus, C1 G1^{1/2} = S1), F >= |Tr rho1^{1/2} rho2^{1/2}| = Hell: OK. <1>3: Re A = 1 -
Theta/2 (S^2 + C^2 = 1 on P_nH, re-derived); ||S_n - S~_n||^2 <= ||P_n delta P_n|| (operator monotone sqrt, Bhatia
X.1.1) <= ||delta||_1 = tau (Note 4 Thm 7.1, card petz-zero-collar-channel: ||Q_I - Q~_s||_1 = (r/2pi) log(1+zeta));
||Theta_n|| <= 2 tau < 2: OK. <1>4 Ostrowski-Taussky det(Re A) <= |det A| (direction correct; Re A > 0 by <1>3;
det A > 0 by lem:hell): OK. <1>5 -log(1-t) <= t/(1-t_max) for 0 <= t <= t_max < 1, summed over eigenvalues of
Theta_n/2 <= tau: OK. <1>6 Powers-Stormer (||S^{1/2}-T^{1/2}||_2^2 <= ||S-T||_1) twice: Tr Theta_n <= 2 tau, h_n <= tau:
OK. <1>7 tau/(1-tau) = (r/2pi) zeta + O(zeta^2): OK. Direction ledger: every inequality is an upper bound on the exact
Phi, as the card says. STANDS. The card does not include the conditional second sentence (lem:H is a GAP): right.
### prop:h2 (l. 943-968, Prop 6.5) -- read step by step
<1>1 |D1|^2/W from kernel_identity thm:main (D1 = (q_k - q_k') v/(u(u^2+4pi^2))) and eq:NWuv; <1>2 dk dk' = du dv/2,
Tonelli (nonnegative integrand), lem:V for the v-integral, sinh^2(u/2)/((1+cosh(u/2)) sinh(u/2)) = tanh(u/4) (checked);
<1>3 lem:U second integral = log2/pi^2, h2 = (r/2)(1/3)(log2/pi^2) = r log2/(6 pi^2); h2/(g_B/8) = 2 log 2. STANDS.
prop:hell2's bracket g_B/8 <= coefficient <= g_B/4 (N <= W <= 2N) contains h2 = 1.386 g_B/8: consistent.
Independent quadrature: see below.
### Status
rigor/referee_quadratic_limit.tex (2026-09-05; numbering of an earlier version: "Thm 6.4", "Prop 6.5/6.6") verified
the unconditional bound and h2 ("Theorem 6.4(i) ... and Propositions 6.5, 6.6 ... are proved", l. 834-836); the
document has changed since (today's timestamp, new numbering 6.3/6.5; this round's R1 item 12 added a status line to
sec:summary). No re-review of the current version exists, so `refereed` is not available and `proved` (structured
proof in a named document, read here step by step) is the right, weakest supported status.
### Independent quadrature of h2 (tolerance 1e-10 relative, fixed first)
rigor/repair/ref_rp_3_h2.py -> ref_rp_3_h2.out (run: `python3 rigor/repair/ref_rp_3_h2.py > rigor/repair/ref_rp_3_h2.out`,
26 s). 2D integral in (u, v) with D1 from kernel_identity thm:main (middle member) and W built from q_k = 1/(1+e^k)
directly (eq:NW), NOT from eq:NWuv or lem:V; inner v-range follows the ridge v ~ u. Validation (same code, W -> N):
g_B/8 = 0.008443431970196678 vs 1/(12 pi^2), rel.dev 2.2e-13. Result: h2 = 0.01170508212878632 vs log2/(6 pi^2) =
0.0117050821287805, rel.dev 5.0e-13 < 1e-10: OK; h2/f2 = 1.38629436112058 = 2 log 2. The 1D form (1/6) int tanh(u/4)/
(u(u^2+4pi^2)) du agrees to working precision (mpmath). (scipy prints roundoff IntegrationWarnings into the .out at
1e-12/1e-13 requested; the achieved agreement is 5e-13.)
### Card verdicts
- phi-unconditional-linear-bound: Statement correct (quantifiers "every zeta > 0 with tau < 1", direction, "linear,
  not quadratic", second sentence excluded). STANDS WITH REPAIR: How to verify says "its proof steps <1>1-<1>3
  following"; the first part needs <1>1-<1>7 (<1>4 Ostrowski-Taussky, <1>5, <1>6 Powers-Stormer carry the bound).
  Repair: "<1>1-<1>7". kb verdict fail on this locator only.
- hellinger-coefficient-h2: STANDS; every number recomputed. NEEDS ORCHESTRATOR: its evidence num:rigor/council/
  c6_constants.py is untracked (git status: rigor/council/ ??).

## (6) Compilation of both papers
Copies of paper1/, paper2/ and numerics/fidelity_table_largezeta.tex in the scratchpad
(.../scratchpad/REF_RP_3/build), aux files removed, pdflatex -interaction=nonstopmode three times each (no bibtex:
manual thebibliography). paper1: 30 pages; paper2: 26 pages; in both final logs 0 lines matching `^!` and 0 matching
`(Reference|Citation).*undefined`. Agrees with the 2026-11-19 notes on paper1-status (30 pp) and paper2-status (26 pp).
The card Statements still give 29 pp and 25 pp, dated 2026-09-24 (true as dated; stale as a description).

## Verdicts recorded (kb -p cft_cmi verdict, KB_ACTOR=REF-RP-3, 2026-11-19)
FAIL: paper1-status, two-branch-law-lattice, phi-unconditional-linear-bound (locator repair only).
PASS: paper2-status, conj-s2, boson-check, hellinger-coefficient-h2.
Procedural: my fail note on phi-unconditional-linear-bound lost the word "proved" to shell quoting; I added a
one-line erratum note (kb note) instead of editing the note. kb -p cft_cmi lint: 0 issues, 12 awaiting review.
NEEDS ORCHESTRATOR: commit rigor/repair/REF_RP_3_report.md, ref_rp_3_{numbers,fourier,h2,lattice}.py/.out;
rigor/council/ (evidence of hellinger-coefficient-h2) is untracked; the theta-value card's title ("no proved
direction") and Statement ("LOWER BOUND") disagree (REF-RP-2's seat), which decides paper1/sec_outlook.tex:102.
