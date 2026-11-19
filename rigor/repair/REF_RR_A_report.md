# REF-RR-A report: re-review after author repairs, repair round 2026-11-19

Referee REF-RR-A (Opus), adversarial. Single re-review of seven cards after the first-round failures
(REF-RP-1, REF-RP-3, REF-RP-4) and the author repairs (ORCH_patch_1.json, R1b_patch.json, card_changes_4.json,
card_changes_6.json).

## 1. group-index-zero-large-s
Notes and history read first (REF-RP-4 FAIL of today: stale title/verify, PROMOTE; orchestrator set title, evidence,
next, verify and status conjectural -> proved at 14:37).

Mathematics (index_zero.tex, 12 pp, read as it stands): lem:kernels, lem:sym, lem:cubic (a)-(d), thm:path,
lem:products, lem:blocks, thm:sv, thm:group, lem:gen, lem:app-K re-read step by step. STANDS. Checks of my own:
thm:group <1>1 is lem:products <1>4 with U=U_t, V=U_s (G_{s+t}=G_s+U_s^*G_tU_s); lem:gen sign:
<P+x,Ky>+<Kx,P+y> = <x,[P+,K]y> = -<x,[P-,K]y> with K^*=-K, consistent with C=-[P-,K]; f(t)-f(0) =
<phi,(U_t^*P+U_t-P+)psi> = -<phi,G_t psi>; lem:cubic (a) bound sum|<f_j,XYZf_j>| <= ||X||_2||YZ||_2.
Direction ledger: ||G_s||_2 <= |s| ||[P-,K]||_2 (upper bound, exact quantity, lem:gen) so ||G_s||_2 >= 1 implies
|s| ||[P-,K]||_2 >= 1 (the direction the Statement uses); ||[P-,K]||_2^2 = 2||P-KP+||_2^2 = 4 f2^K (RR lem:groupbound <1>3),
so |s| >= (4 f2^K)^{-1/2}. Correct.

Hypothesis. lem:gen needs (K): the form identity on a core. The title carries "(form sense on a core)"; the
Statement says "[P_-,K] Hilbert-Schmidt (the setting of RR Lemma 6.1)", and RR lem:groupbound <1>2 itself uses the
derivative "on a core" (verdict box after prop:rrr: "weak on the core H^1_c cap D(h')"). Together the card states the
hypothesis lem:gen needs; the Statement alone would be weaker-hypothesis (stronger claim) if read as an operator
commutator on a non-core domain. MINOR: the Statement should repeat "(form sense on a core, (K) of lem:gen)".
"Same singular values": index_zero.tex (C3) defines singular values as the square roots of the NONZERO eigenvalues of
T^*T, and thm:sv is stated in that convention; the title says "nonzero". Consistent; MINOR to say "nonzero" in the
Statement too (the zero singular values, i.e. dim ker of the blocks, are not claimed equal and need not be).
"In particular K = D + ih', Prop. 6.2": lem:app-K assumes chi satisfies (W); RR prop:rrr is PA's field (index_zero.tex
prop:ranges item 4; prop:rrr <1>2, <1>4 use PA Cor. 2.7 and PA Prop. 7.6), where (W) holds by PA lem:gen,
lem:integralrep. True as stated, but the field is not named on the card (MINOR).

Evidence: thm:group l.225, lem:gen l.242, thm:sv l.186, lem:app-K l.305, RR corr0924:C3 l.1026 all resolve (grep -n).
num:rigor/index_zero_check.py exists.

How to verify, run exactly as written from the project root with PYTHON = scratch venv:
${PYTHON:-python3} rigor/index_zero_check.py > rigor/repair/ref_rr_a_index_check.out ; diff against
rigor/index_zero_check.out: IDENTICAL (exit 0). Test (B): index -1 at s=1, -2 at s=2, as the card says.
Test (A) honestly described (index_zero.tex sec:num, l. 417-439 and script header): complex NNN hopping 0.4i, H not
real, max|B-C^T| in [0.335, 0.765] printed; ||[P-,K]||_2 = sqrt(2(0.8^2+0.4^2+0.4^2)) = 1.3856 recomputed by hand;
Gershgorin ||H|| <= 1+1+0.4+0.4+0.5 = 3.3; the document says explicitly that a finite unitary has index zero
automatically and (A) cannot detect a failure (non-discriminating). Honest.

Dependencies: `kb deps` shows "depends: none recorded". The "in particular K = D + ih'" clause rests on lem:app-K, whose
<1>1 cites PA l. 758 and whose hypothesis (W) is supplied for PA's field by PA lem:gen and lem:integralrep
(rigor/uhlmann_upper_bound.tex, evidence document of card thm-a-quadratic-law). Missing edge: depends should list
thm-a-quadratic-law (or the card should drop the "in particular" clause). The abstract theorem itself uses no card.
Stale Notes paragraph 1 ("Status conjectural ... no argument") is history, answered by the dated notes; not a failure.
Card type field is still "conjecture" while status is proved (cosmetic).

VERDICT: FAIL (small repair). Repair: kb set depends=thm-a-quadratic-law (PA lem:gen, lem:integralrep, l. 638-686,
for (W) of PA's field in lem:app-K); in the Statement write "[P_-,K] Hilbert-Schmidt in the form sense on a core
((K) of index_zero.tex lem:gen)", "same nonzero singular values", and "K = D + ih' with D the generator of PA's field".
The mathematics STANDS; after this edit a pass needs no further check of the document.

## 2. pushforward-blocks-equal-singular-values
Notes/history read first (REF-CARD-ROR pass of 2026-09-24 on the heuristic version; REF-RP-4 report item 6 and 11:
"do not promote as stated"; orchestrator narrowed to (W) and set proved).

Statement vs index_zero.tex lem:app-W (l. 291-304): hypothesis "chi admissible (RR def:flow) with (W): W~_s = e^{sD}
strongly continuous unitary group and G_s = int_0^s W~_sigma^* G^(1) W~_sigma dsigma (Bochner in S_2), G^(1) in S_2,
every real s"; conclusion "index 0 and equal singular values, every real s". The card restates exactly this; "with
multiplicities" comes from thm:sv (allowed). Proof: <1>1 triangle inequality for Bochner integrals, <1>2 thm:group.
STANDS.

(W) for PA's field, checked in the PA source (rigor/uhlmann_upper_bound.tex): lem:gen l. 638-645 (W~_s = e^{sD}
strongly continuous unitary group, D = chi d_x + chi'/2, core H^1_c); lem:integralrep l. 670-686, eq:intrep (G_s =
int_0^s W~_sigma^* G^(1) W~_sigma dsigma as a Bochner integral in S_2, "for all s"; kappa^(1) in L^2 so G^(1) in S_2);
chi = chi' = 0 off K = [0,2] at l. 698-699 (lem:integralrep <1>1). PA lem:ext (l. 118 ff.) states (E1)-(E4) for s >= 0;
for s < 0 (W) follows from the s >= 0 case by the group law: G_{-s} = -W~_s G_s W~_s^* (from G_0 = 0 =
G_s + W~_s^* G_{-s} W~_s), and substituting tau = sigma - s turns -W~_s (int_0^s ...) W~_s^* into int_0^{-s}
W~_tau^* G^(1) W~_tau dtau. So (W) holds for every real s for PA's field (my derivation; thm:group needs (G) only
near t = 0 anyway). Line citations correct.

General chi: the Statement says "that case is not claimed here", the title "(W) is only asserted", next names the
lemma to write. Nothing about a general chi is claimed. The first Notes paragraph (heuristic, "every admissible chi")
is history, superseded by the dated status note.

Status: proved is the weakest status for a proof in a document that a referee (REF-RP-4 item 6) found to STAND for
chi with (W); right.

Dependencies: `depends: none` (and the Notes reason "uses only PA's definitions ... and no card") is now WRONG. The
proof is lem:app-W <1>2 = thm:group + thm:sv, which are the content of card group-index-zero-large-s (index zero for a
unitary group with (G)); the parenthetical "proved by PA lem:gen and lem:integralrep for PA's field" rests on
rigor/uhlmann_upper_bound.tex, evidence document of card thm-a-quadratic-law. Missing edges: group-index-zero-large-s,
thm-a-quadratic-law. (No cycle: neither depends on this card.)

VERDICT: FAIL (small repair). Repair: kb set depends=group-index-zero-large-s,thm-a-quadratic-law (index_zero.tex
lem:app-W <1>2 uses thm:group, thm:sv; (W) for PA's field from PA lem:gen l. 638, lem:integralrep l. 670).
Statement, title, status and evidence otherwise STAND.

## 3. rate-of-remainder
Notes/history read first (REF-RP-4 PASS of today on the range wording "subject to ... under review"; orchestrator
note of today: range sentence updated after the promotion of group-index-zero-large-s, card_changes_6.json item 4).

Constants recomputed (python3): pi sqrt 3 = 5.441398 = (4 f2)^{-1/2}, pi sqrt 6 = 7.695299 = (2 f2)^{-1/2} with
f2 = 1/(12 pi^2). Card's 5.44 and 7.70 correct.

The new range sentence in (2) against the documents: "proved for zeta < pi sqrt 3; for pi sqrt 3 <= zeta < pi sqrt 6 by
index zero of e^{sK} for every real s, index_zero.tex lem:app-K" = index_zero.tex prop:ranges item 4 (prop:rrr, PA's
field, no (W) beyond PA) and RR prop:rrr l. 855-856 after R1_patch ("rests on index zero of e^{sK}, index_zero.tex, under
review, Lemma 6.2"). "the f2 form on this larger range comes from prop:rrr only, for PA's field" = prop:ranges item 3
("It does not give the form with f2 ... the form with f2 on 0 <= zeta < pi sqrt 6 is item 4") and item 4 ("the only
source of the form with f2"). "for a general admissible chi the statements with f2^chi need condition (W)" =
prop:ranges items 2, 3 and the R1b_patch items 0-3 in RR l. 156, 170, 203, 1068. These clauses STAND.
Title ("global upper bound Phi <= -(1/2) log(1 - 2 f2 zeta^2); c3 <= 0 as a limsup; no positive log^-2 term"): accurate.
depends (thm-a-quadratic-law, const-gb, c11-extension-implementer, mobius-reduction-cross-ratio,
pushforward-blocks-equal-singular-values, group-index-zero-large-s): complete for the new range (lem:app-K is on
group-index-zero-large-s). OK.

FAILURE (BREAK of the card text, not of the mathematics): the Statement now contradicts itself. The new parenthetical
in (2) says the range pi sqrt 3 <= zeta < pi sqrt 6 is settled by index zero (card proved), but the older "Index gap"
passage, left unchanged further down, still says: "The documents settle this while ||G_s||_2 < 1 ... Beyond that, i.e.
for |s| ||[P_-, K]||_2 >= 1 in (1), for (4 f2^K)^{-1/2} <= zeta < (2 f2^K)^{-1/2} in (2) and for pi sqrt(3) <= zeta <
(2 f2)^{-1/2} = pi sqrt(6) = 7.70 in the bound with f2, they rest on the cards pushforward-blocks-equal-singular-values
(heuristic) for the push-forwards W~_s = e^{sD} (h' = 0; thm:global with f2^chi) and group-index-zero-large-s
(conjectural) for every other e^{sK}". Both status words are stale (both cards are now proved), and "the documents
settle this while ||G_s||_2 < 1" is no longer the whole story (index_zero.tex settles every real s). Also (1) is stated
"for [P_-,K] Hilbert-Schmidt" while prop:ranges item 1 needs (K) of lem:gen (form sense on a core) (MINOR).

VERDICT: FAIL (small repair). Repair: in the Index-gap passage replace "The documents settle this while ... for every
other e^{sK};" by: "The documents first settled this only while ||G_s||_2 < 1 (|s| ||[P_-,K]||_2 < 1, i.e. zeta <
(4 f2^K)^{-1/2}; for the f2 form zeta < pi sqrt 3 = 5.44); rigor/index_zero.tex settles it for every real s: for e^{sK},
K = D + ih' with PA's field, by lem:app-K (card group-index-zero-large-s), and for the push-forwards W~_s by lem:app-W
for chi satisfying (W) (card pushforward-blocks-equal-singular-values); hence (1) holds for every real s, (2) with
f2^K for 2 f2^K zeta^2 < 1 and with f2 for zeta < pi sqrt 6 = 7.70 (prop:rrr, PA's field), and thm:global with f2^chi
for 2 f2^chi zeta^2 < 1 for chi satisfying (W);" and in (1) write "[P_-,K] Hilbert-Schmidt in the form sense on a core".

## 4. thm-b-universality
Notes/history read first (REF-RP-1 FAIL of today: (1) double comma, (2) lem:ext quantifier, MINOR stale (d) and
prop:fermion "for the locality clause"; orchestrator answer: card_changes_4.json item 0, ORCH_patch_1.json).

(1) Statement: "where zeta = s, with g_B = 4 dist(...)^2 = 2c/(3 pi^2)": double comma gone; half-line chart A =
(-inf,0) named; (H1) in the (C7) form (REF-RP-1 checked it equals implementation_C11.tex thm:H1(iii)). FIXED.
(2) lem:ext (universality_theorem_B.tex l. 181-200) now quantifies over two fields of C11 def:gtot class E (E1)-(E3)
with L=1, both 0 on (-inf,0] and -x^2 on [0,1] (class E_inf of moebius_reduction_general_nets.tex l. 77-80, which lies in
E(a',1) for every a' > 0, so C11's lemmas apply). Step by step: <1>1 phi = gtot - gtot# vanishes on (-inf,1] hence on I;
<1>2 kt#_b fixes (-inf,0] (gtot# = 0 there) and equals k_b on [0,1), so kt#_b I = (-inf, 1/(1+b)) subset I for b >= 0:
the restricted quantifier now supplies exactly what <1>2 uses; <1>3-<1>7 unchanged (Trotter, RS VIII.31, as REF-RP-1
checked). FIXED in the lemma.
Later references to lem:ext in the document (grep -n lem:ext: l. 133, 1049, 1057, 1103-1111, 1133):
 - l. 133 ("Lemma ext does not use it"), l. 1103-1111 (R2, "Superseded on 2026-11-19 ... proved by the Trotter
   argument"): consistent.
 - l. 1049 ("the recovered state does not either (Lemma ext)") justifies the smooth compactly supported extension of
   rem:vector (l. 163-165, "gtot is real, C^{1,1} and compactly supported"); such a field need not vanish on
   (-inf,-a], so lem:ext as now restricted covers it only if the chosen extension is in E_inf. Not load-bearing
   (thm:B does not use lem:ext; REF-RP-1 item 7). MINOR.
 - l. 1057-1058, Summary table: "proved for fields of class E and s >= 0" -- WIDER than the lemma now proves (E_inf).
   GAP in the document's summary (stale after ORCH_patch_1).
 - l. 1131-1134 item R4(d) "Haag duality was replaced by locality in ... Lemmas ext, gauge, prop:geom": stale, lem:ext
   <1>1 now uses (HD) (verdict box l. 221); and l. 933 "for the locality clause": both REF-RP-1 MINORs, not answered.
Compilation: scratch copy (scratchpad/REF_RR_A), pdflatex twice: 0 lines '^!', 0 '(Reference|Citation).*undefined',
25 pages; the project's own log (19 Nov 14:28, same time as the .tex) agrees.
How to verify (card): "25 pp, rigor/universality_theorem_B.log of 2026-09-24, with its section 'Corrections of
2026-09-24', l. 1128-1177": the log is now of 2026-11-19 and the section is at l. 1146-1197 (grep -n corr0924:sec gives
1146; \end{document} 1197). Wrong locator.
Evidence tokens: thm:B l. 875, referee r:edits l. 654, universality_normalization.tex sec:setting l. 166: resolve.
Statement wording (pre-existing, MINOR): "(H3) first-order differentiability on a core: -log F = ..." runs the
conclusion into (H3); a "Then" before "-log F" would separate hypothesis and conclusion.

VERDICT: FAIL (small repair; Theorem B itself STANDS). Repairs: (a) universality_theorem_B.tex Summary row l. 1058:
"class E" -> "class E_inf (0 on (-inf,0], -x^2 on [0,1])"; R4(d) l. 1131-1134 and l. 933: mark superseded (lem:ext uses
(HD) through C11 thm:H1 <1>2); l. 1049: say the smooth extension is taken in E_inf (e.g. C11 representative (i) with L=1);
(b) card How to verify: "log of 2026-11-19", "Corrections of 2026-09-24, l. 1146-1197".

## 5. moebius-reduction-general-nets
Notes/history read first (REF-RP-1 FAIL of today: prop:cov's second hypothesis ||g_* f||_{3/2} < infinity missing on
the card; document STANDS; orchestrator answer card_changes_4.json item 1).

prop:cov (moebius_reduction_general_nets.tex l. 268-271) assumes: g in PSL(2,R), f real continuous, ||f||_{3/2} <
infinity, f in H^2(S^1), ||g_* f||_{3/2} < infinity. The card now says "real f in H^2(S^1) with ||f||_{3/2} < infinity
and ||g_* f||_{3/2} < infinity (both are hypotheses of Prop. prop:cov ...)". Continuity is implied by H^2(S^1) (one
dimension, H^2 subset C^1), so all hypotheses are on the card. FIXED. "it holds for the fields used, since g_* g_tot
is again in the extension class": lem:geom (7) (l. 167-168) gives kappa^{-1} g_* g_tot in E_inf subset E(a',1), whose
fields have finite 3/2-norm by C11's regularity theorem (c) (as in UB lem:ext <1>1). Correct.

Rest of the Statement against thm:main (l. 374-390): net = CDIT sec. 4 axioms (1)-(10) plus (HD) (sec:conv l. 45-51);
(a) every real s, Ad V maps A(I) onto A(I^), I = (-a,L), I^ = (-inf,1), ghat = kappa^{-1} g_* g_tot with kappa^{-1} =
(a+L)/a; (b) s >= 0 every extension, every real s for g_tot^flat; (c) fidelity equality, and under (HD), (BW), (RS)
Theorem B as s -> 0+ (both signs for g_tot^flat). Card = document, nothing stronger. My own check of the geometry:
g(x) = (a+L)x/(L(x+a)) has g(-a+) = -inf, g(0) = 0, g(L) = 1, g(L/(1+s)) = (a+L)/(L+a+as) = 1/(1+zeta) with zeta =
as/(a+L); cross ratio (x3-x1)(x4-x2)/((x3-x2)(x4-x1)) of -a < 0 < L/(1+s) < L equals (L+a(1+s))/(L+a) = 1 + zeta.
Correct (direction: an equality, no inequality involved).
How to verify executed: scratch copy, pdflatex twice: 0 '^!', 0 undefined, 14 pages, as the card says. Labels thm:main
l. 374, lem:geom l. 160, lem:push l. 216, lem:Th2 l. 242, prop:cov l. 268, cor:conj l. 316, lem:ext l. 340,
sec:open l. 462 resolve. Evidence tokens resolve.
depends implementer-hypotheses (C11 (H1), Carpi-Weiner package) and thm-b-universality (part (c)): the edges the proof
uses. Status proved (document proof, REF-RP-1 STANDS on every lemma): weakest supported.
Document MINORs of REF-RP-1 (FH05 locator in box C2; 5e-15 from a scratch computation in sec:open) are not answered;
they do not affect the card.

VERDICT: PASS.

## 6. mobius-reduction-cross-ratio
Notes/history read first (REF-RP-1 FAIL of today: How to verify empty; orchestrator filled it, Statement unchanged).

How to verify run exactly as written, from the project root:
 grep -n 'label{lem:mobius}' fidelity_recovered_quasifree.tex  -> 200
 grep -n 'label{prop:closed}' rigor/check_note5_theory.tex     -> 894
 python3 rigor/repair/ref_rp_1_geometry.py > scratchpad/REF_RR_A/geom.out (system python3, exit 0); diff against
 rigor/repair/ref_rp_1_geometry.out: IDENTICAL ("2000 samples, 0 failures (exact)"; Schwarzian 9.68e-49 < tol 1e-40).
Labels resolve; the command is executable; FIXED.
Statement locators: fidelity_recovered_quasifree.tex:208 ("Let g be a Moebius transformation ... with g(I) bounded")
and check_note5_theory.tex:180-185 (hypothesis (a): "g maps closure(I) into R") correct; prop:closed (l. 894-916)
states the kernel zeta S_p S_p' / (sinh M (sinh M + 2 zeta S_p S_p')) with zeta = s beta_0/L = as/(a+L): matches.
Cross ratio recomputed by hand: (L/(1+s)+a) L / ((L/(1+s)) (L+a)) = 1 + as/(a+L). Equality, no direction issue.
a = infinity: the document states prop:closed at finite a (beta_0 = aL/(a+L), l. 71); "holds unchanged at a = infinity"
is the substitution beta(x) = L - x, xi = -log(L - x) (after the shift by log a), beta_0 = L, zeta = s, recorded in the
2026-09-23 referee note (REF-DEP-CFT-B7) and not in a document. I re-derived lem:sinh (l. 645-660) at a = infinity:
sqrt((L-y)/(L-x)) - sqrt((L-x)/(L-y)) = (x-y)/sqrt((L-x)(L-y)). True. MINOR: How to verify could add "lem:sinh with
beta = L - x" (REF-RP-1's suggestion); the a = infinity remark could be written into check_note5_theory.tex.
depends none: lem:mobius and prop:closed use no other card. Status proved, unchanged and previously passed.

VERDICT: PASS.

## 7. phi-unconditional-linear-bound
Notes/history read first (REF-RP-3 FAIL of today: How to verify cited <1>1-<1>3 only; proof STANDS, proved right;
orchestrator: card_changes_6.json item 1).

How to verify now: "rigor/quadratic_limit.tex l. 807-816 (label thm:upper) and its proof steps <1>1-<1>7 following
(l. 818-856; the bound eq:upper-master is concluded in <1>7); compare paper1/sec_quadratic.tex eq:unconditional
(l. 31-33)". Checked (grep -n, sed -n): thm:upper l. 807-815 (l. 816 blank); <1>1 starts l. 817; <1>7 is l. 852-853 and
concludes eq:upper-master; <1>8 (conditional part, not on the card) l. 854-857; <1>9 l. 858. Paper: the
"unconditionally ... tau < 1" sentence l. 31-32, eq:unconditional l. 33-35. The step range <1>1-<1>7 is right (FIXED);
the line range 818-856 is off by one at the start and reaches 3 lines into <1>8 (exact: 817-853); paper lines 31-35.
MINOR, the steps are named unambiguously by their Lamport labels.
Statement vs thm:upper (l. 808-813): hypothesis zeta > 0 with tau(zeta) = (r/2pi) log(1+zeta) < 1; chain Phi <=
sup_n h_n/(1-tau) <= tau/(1-tau) = (r/2pi) zeta + O(zeta^2); "Phi = O(zeta) unconditionally" (l. 813). Card matches;
direction ledger: both inequalities upper bounds on the exact Phi (as REF-RP-3 checked); the conditional second
sentence excluded. depends petz-zero-collar-channel (||delta||_1 = tau, <1>6) and quasi-free-fidelity-formula (<1>1-<1>2)
unchanged from the first review.

VERDICT: PASS (MINOR: exact line range 817-853, paper l. 31-35).

## Verdicts and kb lint
Recorded 2026-11-19 (KB_ACTOR=REF-RR-A), no competing verdict on any card (history checked immediately before):
- group-index-zero-large-s: FAIL (missing depends thm-a-quadratic-law; Statement to say form sense on a core, nonzero
  singular values, PA's field). Mathematics STANDS.
- pushforward-blocks-equal-singular-values: FAIL (depends: none wrong; needs group-index-zero-large-s,
  thm-a-quadratic-law). Statement STANDS.
- rate-of-remainder: FAIL (Statement self-contradictory: stale Index-gap passage calls the two index cards heuristic /
  conjectural and the range beyond ||G_s||_2 < 1 unsettled).
- thm-b-universality: FAIL (document Summary row l. 1058 still says class E; How to verify log date and l. 1128-1177
  stale; REF-RP-1 MINORs l. 933, l. 1131-1134 unanswered). Theorem B STANDS.
- moebius-reduction-general-nets: PASS.
- mobius-reduction-cross-ratio: PASS (MINOR: a = infinity substitution only in a referee note).
- phi-unconditional-linear-bound: PASS (MINOR: exact lines 817-853, paper l. 31-35).
kb -p cft_cmi lint: 0 issues, 6 awaiting review (22 dependency/locator warnings, kb deps --check).
Files: rigor/repair/REF_RR_A_report.md, rigor/repair/ref_rr_a_index_check.out (rerun of index_zero_check.py);
scratch compile copies in scratchpad/REF_RR_A/.
