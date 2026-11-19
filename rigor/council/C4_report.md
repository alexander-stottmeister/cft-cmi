# C4 report: Optimality (council 2026-11-19, actor REF-COUNCIL-C4, adversarial referee)

## 0. Scope and sources read
Read in full or in the load-bearing parts: rigor/exact_fidelity_upper_half.tex (sec:second, sec:main, Corrections
of 2026-09-24 C1-C3, l.650-884, 1091-1208); rigor/sdp_dual_certificate.tex (S10; sec:num l.560-610, cor:maximal and
verdict l.820-880); numerics/optimality_all/F3_RESULTS.md (all 277 lines); KB cards compression-not-optimal-exact-fidelity,
exact-fidelity-optimality-open and the list `kb q --area optimality` (38 cards); `kb deps --check`.
Further parts of the other scope documents are listed with what was read in the sections below; what was not read is
in Sec. 8.

## 1. Verdict table (one line per theorem)
E1 = rigor/exact_fidelity_upper_half.tex, S12 = rigor/optimality_all_channels.tex, S10 = rigor/sdp_dual_certificate.tex.
| theorem | verdict | step / reason |
|---|---|---|
| E1 prop:uhl (l.110) as stated for every element of E(W_I) | STANDS WITH REPAIR | <1>3 false for non-zero index (E1 C3, l.1156-1203, own counterexample); restriction to index zero recorded on card uhlmann-upper-half-proved; only index-zero U_s are used downstream |
| E1 lem:group <1>1 (l.662) | STANDS WITH REPAIR | identity ||P-U*PU||_2^2 = 2||P^perp U P||_2^2 needs ind = 0 (C3); flagged in-line |
| E1 thm:UH (l.677-734) | STANDS | C3's small-s argument checked: ||[P,U_s]||_2 -> 0 by <1>2 alone, so blocks < 1, X invertible, ind 0; not circular |
| E1 thm:UHall (l.737-765) | STANDS | <1>2 takes inf over Z_e of an s-independent bound; uses thm:reduction, thm:Q (not re-audited, Sec. 8) |
| E1 thm:main (l.781-821) | STANDS | structural bound with theta_fr := sup over finite-rank G; theta_fr > 0 iff R_a != 0 |
| E1 rem:thetafr (iii) (l.837-852) | numerical; wording GAP (F2) | theta_fr >= 0.38 rests on extrapolation; no finite mesh reaches 0.38 |
| E1 cor:sandwich (l.857-884) | STANDS | directions correct; lower half kept in dual form, identification with D_z conditional, as stated |
| S12 thm:main(1) (l.325-366) | STANDS WITH REPAIR (F4) | <1>1's monotonicity argument is invalid for Tr t delta^beta >= 2V'/(3||t||_1); repair: pick eps from Delta_z(t) in eq:single |
| S12 thm:main(2) (l.338-342, 367-371) | STANDS | eq:liminf correct; the phrase "E_rec >= D_z(1-o(1)) along any family" needs "near-optimal family" [MINOR] |
| S12 thm:main(3) (l.343-405) | STANDS | Sion (Cor. 3.3) hypotheses checked in <2>1-<2>2: K WOT-compact convex, L affine continuous in delta, concave in t (V convex) |
| S10 cor:maximal (l.834-857) | STANDS | E_D u E_D + (E_D u E_D)^* = -E_D ddot E_D = 0; I reproduced it numerically (Sec. 6 N2, 8e-14) |
| S10 verdictbreak "E_D u E_D != 0" (l.862-868) | NUMERICAL, CONFIRMED | rho = 0.0147 in a taper-free second frame (Sec. 6 N2); not proved |
| optimality_second_order.tex prop:AC-zero (l.408-434) | STANDS (implication) | its hypothesis on three chains independently confirmed (Sec. 6 N1) |

## 2. Key question (a): which half of E_rec <= (1-theta) f2 z^2 is proved for the EXACT fidelity
Direction: E_rec <= ... is an UPPER bound on the exact recovery error (E_rec = inf over channels of -log F, and
thm:main <1>1 bounds it by one explicit channel). Its pieces:
1. PROVED (structural, exact fidelity, no numerics): for every finite-rank anti-self-adjoint G = E_D G E_D and every
   lambda, limsup z^-2 E_rec <= (1/2)||Pi P^perp (D_chi + lambda G) P||_2^2 (exact_fidelity_upper_half.tex thm:UH,
   thm:UHall, thm:main <1>1, l.677-800). Hence E_rec <= (1 - theta_fr) f2 z^2 (1+o(1)) with theta_fr the SUP over
   finite-rank G (thm:main, l.781-790). I checked thm:UH <1>1-<1>5 and the C3 repair (index zero for small s, l.1185-
   1196): the repair is correct (||[P,U_s]|| < 1 makes both blocks strict contractions, so X = P U_s P|_{PH} is
   invertible, ind X = 0, and lem:group <1>1's identity holds), and it is not circular (<1>2 alone gives
   ||[P,U_s]||_2 -> 0). The constant (1/2)||u||^2 = f2 (thm:main <1>3) imports Theorem A / PA Prop. 7.6 (twisted
   duality), as the document says.
2. PROVED: theta_fr > 0 iff R_a != 0 iff E_D u E_D != 0 (thm:main <1>4; S10 cor:maximal: E_D u E_D purely
   anti-self-adjoint, l.834-857).
3. NUMERICAL, and the document says so (S10 verdictbreak l.862-868): E_D u E_D != 0, i.e. theta_fr > 0. Its only
   evidence is ||E_D u E_D||_2^2/||u||_2^2 = 0.0143 in S10's spectral circle model, the model F3 Sec. 5 shows to be
   taper-dependent with "no taper-free limit" (F3_RESULTS.md l.207-213) and that card spectral-model-uv-pollution
   calls unable to resolve exact fidelities. So the QUALITATIVE claim "the zero-collar compression is NOT optimal in
   exact fidelity" (card title) is itself numerical, not only the value 0.616. See finding F1.
4. NUMERICAL, extrapolated: theta_fr >= 0.38, hence kappa_opt <= 0.616 +- 0.003 (rem:thetafr (iii), l.837-852).
   See finding F2: no computed finite-h value reaches 0.38 (largest 0.37635 at h = 0.015, F3 Sec. 4(iii)), and the
   finite-h values are not one-sided bounds on theta_fr.
5. NOT CLAIMED, correctly: the lower half kappa_opt >= 1 - theta (needs the all-channel minimiser at the isometric
   orbit = KKT endpoint condition, card kkt-noise-criterion-numerics under H3; tangent-h1/h2/h3 conjectural); the
   lower half of cor:sandwich (l.857-884) is the dual bound over admissible test families, its identification with
   D_z = min_F g_Q conditional on S12 Thm 4.1(2)'s test-family conditions.

## 3. Key question (b): the dependency warnings of `kb -p cft_cmi deps --check`
`kb -p cft_cmi deps --check` (run 2026-11-19): 0 errors, 8 dependency warnings, 14 locator warnings. Seven of the 8
dependency warnings are in my scope; the eighth (sequential-recovery-angle-form-under-u assumes the refuted
hypothesis-u-natural-cone-fidelity) is outside it and is C6's.
- W1-W3 kkt-noise-criterion-numerics [numerical] uses kkt-noise-sign-criterion [proved, assumes H1,H2,H3] and
  tangent-problem-exact-parametrisation [proved, assumes H1]; it declares only `assumes: tangent-h3`. PARTLY REAL.
  The measured numbers (lam_min(M_*)/||M_*||, E(zeta_0), E(zeta_inf), rank-one gains) are finite-mesh computations
  and need no continuum hypothesis. But the card's conclusion sentence "The numerics are consistent with the
  isometric orbit carrying the tangent optimum and kappa_opt = 1 - theta" names kappa_opt, the EXACT second-order
  constant, and the passage tangent programme -> E^(2) is thm:value of exact_optimum_tangent_problem.tex, which
  needs H1 and H2 (the sign-criterion card itself says "under H1 and H2 (Thm. thm:value) E^(2) = (1-theta) f2 z^2").
  Repair: either add `assumes: tangent-h1, tangent-h2` or replace "kappa_opt" by "the tangent-programme value".
  [MINOR, bookkeeping; no numerical claim is affected.]
- W4-W7 tangent-sdp-noise-directions [numerical] uses the same two cards without assuming H1-H3. NOT REAL. The card is
  about a finite-dimensional SDP in the S10 circle model at fixed L; H1 (g_Q-differentiability), H2 (localisation of
  minimisers) and H3 (cone of admissible unbounded generators) are continuum statements that are void in finite
  dimension, where the chart and the derivative formula are exact algebra. The card explicitly makes no statement
  about kappa_opt; its "kappa_full <= 0.6488 at L = 64" is a statement about the finite model and is labelled so.
  The warnings are an artefact of the checker's transitive "uses" rule.
- Not flagged by the checker but in scope: ac-lower-bound-zero [proved] depends on ac-intertwiner-exists-hopping-chain
  [numerical]. The card is honest (an implication is proved; its application to three chains is numerical), but a
  'proved' status for a Statement whose second half "on these three chains E_AC = 0 exactly" rests on a numerical
  card is the pattern the brief asks to flag. [MINOR]; I recomputed the hypothesis independently (Sec. 6, check N1).
- 'proved' cards of the optimality area resting on numerical/conjectural cards: none besides ac-lower-bound-zero.
  Checked depends of all-channel-equals-quasi-free, all-channels-symbol-feasible, uhlmann-upper-half-proved,
  kkt-certificate, petz-not-optimal, quasi-free-sdp, theta-wiener-hopf-frame, exterior-exhaust-invisible,
  single-observable-bound, mobius-reduction-cross-ratio, quasi-free-second-order-fidelity-expansion,
  compression-defect-commutator-form: every dependency is proved or refereed. kkt-noise-sign-criterion and
  tangent-problem-exact-parametrisation carry their conjectural H1-H3 as declared `assumes`, which is correct.

## 4. Findings ([BREAK]/[GAP]/[MINOR], with inheriting cards and paper statements)
No mathematical BREAK was found in the proofs read. Most severe first:
F1 [BREAK for the paper, wording only; brief Sec. 3 rule] paper1/sec_outlook.tex:72-73 -- "It is \emph{not} optimal
  among all normal recovery maps" is stated without qualifier, but the only input that makes it true, E_D u E_D != 0
  (theta_fr > 0), is numerical (S10 verdictbreak l.866-868: "The one ingredient that is numerical rather than proved
  is the non-vanishing of E_D u E_D"). The cards compression-not-optimal-exact-fidelity and
  compression-not-second-order-minimiser are status numerical; the paper sentence is stronger than both. Line 102 of
  the same file is correctly qualified ("(proved)" for the iff, "(numerical)" for theta_fr >= 0.38) but its opening
  "The zero-collar compression is not the minimiser" is likewise unqualified. Repair: "numerically, it is not ...".
  Mitigation: my independent taper-free recomputation (Sec. 6 N2) gives rho = 0.0147, so the claim is well supported
  numerically.
F2 [GAP, numerical wording] E1 rem:thetafr (iii), l.846-850, and card compression-not-optimal-exact-fidelity
  ("theta_fr >= 0.38 is exactly as well supported numerically as theta = 0.384 +- 0.003"). Direction ledger: (a) F3's
  finite-h values are theta_h = sup over a finite cell class of cos^2 computed with g_Q restricted to a finite
  t-space (their g/f2 = 0.89-0.99 < 1, F3 Sec. 1(b)); the restricted Legendre sup is a lower bound on each g_Q, so
  cos^2 = b^2/(g g) at finite h is NEITHER a lower NOR an upper bound on the continuum cos^2 of that G; (b) every
  computed value is < 0.38 (largest 0.37635 at h = 0.015, F3 Sec. 4(iii)); 0.384 is reached only by Richardson
  extrapolation with the fitted order h^0.77 (+0.008, about 2.7 times the quoted error bar); (c) only the h^p fit
  was tried, not 1/L and log L as AGENTS.md Sec. 5 requires. So "theta_fr >= 0.38" is an extrapolated estimate, not
  a bound witnessed by any finite-rank G. Inherited by: compression-not-optimal-exact-fidelity (Statement, next),
  exact-fidelity-optimality-open, theta-value, paper1/sec_outlook.tex:82 and :102 ("0.616 f2 z^2"). Repair: say
  "theta_fr >= 0.376 at h = 0.015 in two frames (not a rigorous bound), extrapolated 0.384 +- 0.003".
F3 [MINOR] paper1/sec_outlook.tex:102 "the Petz map, at 4f_2z^2, is at least 5.6 times worse than the best channel":
  with the paper's own bracket the best channel is <= 0.616 f2 z^2, so the ratio is >= 4/0.616 = 6.49; 5.6 = 4/0.71
  is the pre-F3 value (theta >= 0.29). True but stale; also numerical (inherits F2). No card carries "5.6"
  (`kb q --text "5.6 times"`: 0 cards).
F4 [MINOR] S12 thm:main <1>1 (l.351-361): "the right side of eq:red is increasing in Tr t delta^beta on the range
  where the bracket is positive ... in which case use x = 2/(3c) instead": the bound of Prop. red is available only
  at x = Tr t delta^beta, and f(x) = x^2(1-cx) falls to 0 as x -> 1/c, so for x in [2/(3c), 2/c) the argument does not
  give the claimed bound. Repair (one line): in eq:single take eps := Delta_z(t)/(2V') with Delta_z(t) <= x; the right
  side 1 - eps x/2 + ... is decreasing in x, so 1 - F >= Delta^2/(8V') (1 - Delta N/V')/(1 - Delta N/(2V')), which
  implies statement (1). Statement unchanged; cards all-channel-equals-quasi-free, single-observable-bound unaffected.
F5 [MINOR] kkt-noise-criterion-numerics: names kappa_opt (exact constant) though it does not assume H1, H2 (Sec. 3).
F6 [MINOR] ac-lower-bound-zero is 'proved' with a Statement that includes a numerical application (Sec. 3);
  confirmed numerically (N1).
F7 [MINOR] E1 C3, l.1162-1163: "The item is not recorded on a knowledge-base card" is stale: card
  uhlmann-upper-half-proved now records it (Statement, 'Correction C3').

## 5. Direction ledger
| evidence | quantity | model | direction |
|---|---|---|---|
| E1 thm:main | E_rec (exact, per chirality) | continuum free fermion | UPPER: <= (1-theta_fr) f2 z^2 (1+o(1)), proved |
| E1 cor:sandwich lower half | liminf E_rec/z^2 | continuum | LOWER: >= sup over admissible t_z of liminf Delta^2/(8V z^2), proved; = D_z/z^2 only conditionally |
| S12 thm:main(3) | D_z = min_F g_Q (second-order functional) | fixed geometry | EQUALITY (Sion), proved; not a statement about E_rec |
| S10 cor:maximal + N2 | rho = ||E_D u E_D||^2/||u||^2 | tapered circle (S10) / taper-free cell frame (N2) | numerical value 0.0143 / 0.0147; no direction proved for finite-h values |
| F3 theta_h | theta at finite h | Galerkin, T0 | approximation, no proved direction (F2); extrapolated 0.384 +- 0.003 |
| kkt-noise-criterion-numerics | lam_min(M_*) | T0 frame | < 0 at every h, extrapolates to 0^- |
Verdicts that need a direction: "compression NOT optimal in exact fidelity" needs an UPPER bound on E_rec below f2 z^2:
thm:main supplies it with the factor (1 - theta_fr), so the verdict needs theta_fr > 0, i.e. E_D u E_D != 0 --
numerical (F1). "kappa_opt <= 0.616" needs theta_fr >= 0.384 as a LOWER bound on theta_fr; only an extrapolated
estimate exists (F2). "kappa_opt = 1 - theta" needs the LOWER bound E_rec >= (1-theta) f2 z^2: not proved (needs
H1-H3 and (a),(e)); correctly not claimed by any card in scope. The ratio Petz/best >= 6.49 (F3) uses the exact
Phi(2z) = 4 f2 z^2 (1+o(1)) (equality) over the upper bound for the best channel: direction correct.

## 6. Independent recomputations
Interpreter: system python3 (numpy 2.5.2, scipy 1.18.1); the scratchpad venv had no numpy at the time of the run.
N1. Tcond on the hopping chain (hypothesis of ac-lower-bound-zero's application). Command, from the cft_cmi root:
  `${PYTHON:-python3} rigor/council/c4_tcond.py > rigor/council/c4_tcond.out`. Own code (no import from numerics/).
  Tolerance fixed in the script: residual <= 1e-10, margins >= -1e-12. Result: (4,8,2), (4,12,2), (4,16,2) HOLD with
  residual <= 3.6e-17, ||T|| = 0.5524, 0.3779, 0.2894, margins 0.1216, 0.1510, 0.1630; (6,12,3) and (8,16,4) FAIL with
  margins -0.1330, -0.4641 (and ||T|| = 1.2850 > 1 at (8,16,4)). All agree with tcond_check.out / tcond_check_extra
  values quoted on the card to the printed 4 digits. Card ac-lower-bound-zero / ac-intertwiner-exists-hopping-chain:
  CONFIRMED (single method each; exact finite-dimensional linear algebra, so no discretisation issue).
N2. The only numerical input of "the compression is not optimal in exact fidelity": ||E_D u E_D||_2^2/||u||_2^2
  (S10 cor:maximal eq:thetalb, 0.0143 in the TAPERED circle model). Recomputed in the taper-free, parameter-free
  Wiener-Hopf frame (exact vacuum kernel in a cell basis; closed-form defect kernel of F3 Sec. 3), with my own
  construction: u = P^perp l P, S_Q(l) = -ddot solved in the Q eigenbasis, E_D u E_D = E_D(1-Q) l Q E_D, ||u||^2 =
  Tr(l(1-Q)lQ) (all within I; invariant under Q -> 1-Q and conjugation, so convention-proof). Command:
  `${PYTHON:-python3} rigor/council/c4_rdd.py > rigor/council/c4_rdd.out` (about 7 s).
  Validation (tolerance 1e-3, fixed before the run): g_Q(ddot)/f2 = 0.95989 at h = 0.12, Y = Ymax = 10, equal to F3's
  T0 value 0.95989 (F3_RESULTS.md Sec. 3(b)); g/f2 = 0.91733, 0.95989, 0.98164, 0.99193 at h = 0.24 ... 0.03 -> 1
  (Theorem A normalisation); (1/2)||u||^2/g_Q = 1.0000000000 at every h (the identity (1/2)||u||^2 = f2 of thm:main
  <1>3 in discretised form). Rigidity: ||R + R^*||/||R|| <= 8e-14 (E_D u E_D purely anti-self-adjoint, cor:maximal).
  RESULT: rho = 0.01404, 0.01462, 0.01474, 0.01473 at h = 0.24, 0.12, 0.06, 0.03 (Y = Ymax = 10); at h = 0.06 the
  window scan (Y,Ymax) = (6,10), (10,16), (10,20) gives 0.01474 each. Stable digits (two finest h, all windows):
  rho = 0.0147 (|change| 1e-5 < 20% criterion), at the meshes computed, not extrapolated; single method (no second
  method run in this frame). This is about 3% above S10's tapered 0.0143, consistent with F3's finding that the taper
  suppresses UV modes. Consequence: theta_fr >= cos^2(u, v_{R_a}) > 0 is supported by a second, taper-free
  discretisation; it remains NUMERICAL (finite-h values of rho are not proved one-sided bounds of the continuum rho).
N3 (not run): theta itself, i.e. the sup over G in the T0 frame; F3's ladder was not recomputed (see Sec. 8).

## 7. Earlier referee reports: were repairs applied
Formed my own view first (Secs. 2, 4), then checked: referee_exact_fidelity_upper_half.tex repairs R2 (g_Q-form not
stated as theorem: rem:gQform l.767-780) and R5 (sandwich identification conditional: cor:sandwich l.874-884) are
applied in the text; R7 (twisted duality caveat) is applied at thm:main <1>3 (l.806-816). The 2026-09-24 corrections
C1-C2 are applied in-line (thm:UH <1>1 now carries both blocks, l.694-699); C3 is a documented gap whose small-s repair
I verified (Sec. 2). referee_exact_optimum_tangent_problem.tex: the FAILED Thm 3.11(3) (cone equality) is now an
inclusion (exact_optimum_tangent_problem.tex l.27-29, 519-524, 839, 967, 1534), and R10's one-sided boundary
directions are carried by the amended Thm 4.4(d)/(e) as recorded on card kkt-noise-sign-criterion. I did not audit
R1, R3, R4, R6, R8-R9 of E1 or R1-R9, R11-R15 of the tangent report line by line.

## 8. NOT DONE
- Not re-audited (budget): E1 thm:reduction, thm:Q, thm:Qdual (l.341-648; used by thm:UHall <1>2); S12 thm:range
  (l.284-312, every recovered symbol quasi-free feasible: Kadison-Schwarz, Tomita, lem:domain); S10 thm:kkt and
  thm:value; rigor/optimality_second_order.tex beyond prop:AC-zero (quasi-free-sdp, petz-not-optimal);
  rigor/exact_optimum_tangent_problem.tex Secs. 3-6 (thm:kktmain, prop:bdryfun, Prop 6.2 theta frame). Their verdicts
  above rest on the earlier refereed status, not on this council.
- theta itself not recomputed (would need the sup over G in a second frame; F3's two frames share the mesh logic and
  the y_max/Lambda correction, so they are not fully independent by the AGENTS.md Sec. 5 definition: both are
  "f3_*" code by the same author).
- N2 is a single method in one frame; the continuum rho has no proved bound.
- No KB writes (council rule); the orchestrator should record F1-F7.
NEEDS ORCHESTRATOR: new files rigor/council/C4_report.md, c4_tcond.py, c4_tcond.out, c4_rdd.py, c4_rdd.out (untracked;
commit decision). Scratchpad venv at the brief's path had no numpy at run time; system python3 was used.
