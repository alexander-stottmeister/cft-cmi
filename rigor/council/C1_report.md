# Council seat C1 — Theorem A (free fermion): adversarial referee report

Actor: REF-COUNCIL-C1 (Opus). Date 2026-11-19. KB read-only; no kb writes.
Scope: rigor/quadratic_limit.tex (thm:lower, thm:upper), rigor/uhlmann_upper_bound.tex (thm:det, thm:three-faces,
thm:main-upper, thm:A), rigor/rate_of_remainder.tex (thm:exactquad, thm:global, thm:third, C1-C3),
rigor/kernel_identity.tex, rigor/tail_bound.tex; cards thm-a-quadratic-law, const-f2, rate-of-remainder,
group-index-zero-large-s, pushforward-blocks-equal-singular-values, remainder-c3-c4-values,
tail-constants-numerical, phi-below-0085-zeta2-numerical.

## 1. Verdict table
| theorem (file:label, line) | verdict | step / reason |
|---|---|---|
| rate_of_remainder.tex lem:groupbound (l. 818-846) as printed ("for all s", "for any unitary") | STANDS WITH REPAIR | <1>1 (l. 828-832) and <1>4 (l. 842-846) assert equal block singular values "for any unitary": false in general (index; refb9_winding.out). Repair: the Fredholm argument of section 2a (index additive along the group, hence 0). Without the repair it holds only for abs(s) ||[P-,K]||_2 < 1 (RoR Correction C3 (ii)). |
| rate_of_remainder.tex thm:exactquad (l. 146-174) | STANDS WITH REPAIR | <1>1 (l. 156) uses Tr(G^2) = 2 ||P-W P+||_2^2 and <1>4 (l. 168-171) the CS claim; both need ind X_s = 0; repaired by section 2a (or by the conjugation argument C3 (i), l. 1062-1068, which is correct but unwritten). |
| rate_of_remainder.tex thm:global (l. 180-208) | STANDS WITH REPAIR | <1>1 applies PA thm:det, which needs ||P+UP-|| < 1 too; only ||V|| < 1 checked ("so no smallness assumption beyond 2 f2^chi zeta^2 < 1 is used", l. 199-201). Repair: section 2a gives ||P+UP-|| = ||V||. |
| rate_of_remainder.tex prop:rrr (l. 848-880) | STANDS WITH REPAIR | <1>3 via lem:groupbound and PA thm:det; same repair; "with no hypothesis" (l. 856) true only after it. KB card rate-of-remainder already restricts to zeta < pi sqrt3. |
| rate_of_remainder.tex cor:c3sign (l. 247-262) | STANDS | small zeta only; inside the settled range. Direction: upper bound on Phi only (limsup <= 0); the card says "c3 <= 0 IF the expansion exists": correct direction. |
| rate_of_remainder.tex thm:third, sec:c3eval, C1-C3 values | not a theorem claim | card remainder-c3-c4-values is heuristic (scripts not in repo); I agree with that status. Not re-derived (NOT DONE). |
| quadratic_limit.tex thm:lower (l. 410-488) | STANDS | data processing Phi >= Phi_P (<1>3), finite-dim analyticity at a faithful state (<1>4), Bures expansion (<1>5), Legendre bound (<1>6); <2>3 trace identity checked by hand. No interchange of limits: liminf over zeta of a bound valid for each fixed P, then sup over l. |
| quadratic_limit.tex thm:upper (l. 807-868) | STANDS (unconditional part (i)) | Phi <= tau/(1-tau); conditional (ii) superseded by uhlmann thm:main-upper; stale "open" text in thm:summary/verdictgap (l. 1191-1245), MINOR, flagged by the status update l. 1296. |
| quadratic_limit.tex prop:gB, value g_B = 2/(3 pi^2) | STANDS (numerically confirmed) | independent recomputation, section 5. |
| uhlmann_upper_bound.tex thm:det (l. 489-597) | STANDS | both ||V||,||A|| < 1 assumed, so X invertible and index 0 built in; annihilator characterisation checked. |
| uhlmann_upper_bound.tex thm:three-faces (l. 1068-1079) | imported (C2/C3 seat) | used with a = -i Pm D Pp, Im<Om,a> = 0 (lem:tangentvec). |
| uhlmann_upper_bound.tex thm:main-upper (l. 1276-1295) | STANDS | limsup over zeta for each h', then inf over h' (valid order); all uses at s -> 0 where both block norms <= C0 s (Corrections C6, C7). |
| uhlmann_upper_bound.tex thm:A (l. 1297-1315) | STANDS | liminf >= g_B/8 (thm:lower) and limsup <= g_B/8 (thm:main-upper) with the SAME g_B: thm:gBvalue identifies PA's sup with quadratic_limit Def. 4.1 (l. 1081-1094; sign of D^(1) vs Qdot handled by l -> -l). Rests on twisted duality (lem:wick <2>1), see finding F3. |
| kernel_identity.tex thm:main | STANDS (numerically confirmed) | |D^(1)(k,k')| from direct quadrature of the position kernel equals the closed form to 1e-15 at 3 points (section 5). Contour argument not re-derived. |
| tail_bound.tex thm:block, thm:tau, thm:main, cor:rate | not re-derived (NOT DONE) | not used by Theorem A (thm:A verdict box l. 1316-1320); constants are numerical (card tail-constants-numerical); arithmetic of cor:rate inputs rechecked (section 5). |

## 2. Key question: equal singular values / index zero used outside their proved range?
Answer: Theorem A itself (thm:A = thm:lower + thm:main-upper) does NOT use them outside the proved range.
thm:det (uhlmann_upper_bound.tex:489-494) assumes both ||V||<1 and ||A||<1, which forces X = P+UP+ invertible
(index 0) by its <1>1; it is applied only as s -> 0 (cor:varupper, thm:main-upper), where both blocks are
<= C0 s (Correction C6/C7, l. 1642-1684). lem:integralrep <1>5 (l. 735-741) equates the two blocks of the
GENERATOR D (Pp D Pm = -(Pm D Pp)^*, from D^* = -D): a derivative-level identity, no index enters. OK.

Where they ARE used beyond the proved range: rate_of_remainder.tex thm:exactquad <1>1,<1>4 (l. 156, 168-171),
lem:groupbound <1>1,<1>4 (l. 822-846), thm:global <1>1 (needs ||P+UP-||<1 for PA thm:det, only ||V||<1
checked), prop:rrr <1>3, cor:quartic. The document records this itself (Correction C3, l. 1026-1079) and the
card rate-of-remainder restricts "proved" to zeta < pi sqrt3 = 5.44, routing the rest to the heuristic card
pushforward-blocks-equal-singular-values and the conjectural card group-index-zero-large-s.
The printed proof of lem:groupbound <1>1 (l. 828-832, "for any unitary") is FALSE as an argument for a general
unitary (winding counterexample, refb9_winding.out: squared block norms differ by exactly 1); C3 says so.

### 2a. The gap closes for every s by a short Fredholm argument (proposed repair; needs a referee before any card
change; the orchestrator decides)
Setting: U_s = e^{sK} a unitary group on H = P+H (+) P-H whose blocks B_s = P+U_sP-, C_s = P-U_sP+ are compact
for every real s (true for W~_s by PA Correction C2 and for e^{s(D+ih')} = W~_s c_s by RoR Correction C2).
 <1>1 X_s := P+U_sP+|P+H is Fredholm for every s.  By: unitarity gives X_s^*X_s = 1 - C_s^*C_s and
      X_sX_s^* = 1 - B_sB_s^*, so X_s^* inverts X_s modulo compacts (Atkinson's theorem).
 <1>2 X_{s+t} = X_s X_t + B_s C_t.  By: P+U_sU_tP+ = P+U_s(P+ + P-)U_tP+ and the group law.
 <1>3 ind X_{s+t} = ind X_s + ind X_t.  By: <1>2, B_sC_t compact, index invariant under compact perturbation
      and additive under products of Fredholm operators (logarithmic law of the index).
 <1>4 ind X_s = 0 for every s.  By: <1>3 gives ind X_s = n ind X_{s/n} for every n >= 1, so the integer
      ind X_s is divisible by every n.  (No smallness of s is needed; continuity is not used either.)
 <1>5 C_s and B_s have the same singular values, with multiplicity.  By: RoR Correction C3's own mechanism
      (l. 1037-1043): they differ only in the multiplicity of the value 1, dim ker X vs dim ker X^*, both finite
      by <1>1, equal by <1>4.
Consequences: ||G_s||_2^2 = 2||V_s||_2^2 and evenness of det(1-V_s^*V_s) hold for every s (lem:groupbound,
thm:exactquad); ||P+U_sP-|| = ||V_s|| < 1 whenever ||V_s|| < 1, so PA thm:det applies in thm:global <1>1 and
prop:rrr <1>3 on the whole range 2 f2^K zeta^2 < 1. For the non-group product family of cor:quartic,
U_s = W~_s e^{ish'}, the index is ind X(W~_s) + ind X(e^{ish'}) = 0 + 0 by <1>2-<1>3 applied to the product of
two unitaries with compact blocks. So group-index-zero-large-s (conjectural) and
pushforward-blocks-equal-singular-values (heuristic) are both settled by this argument, and rate-of-remainder (2)
would hold on its full stated range zeta < (2 f2)^{-1/2} = pi sqrt6 = 7.70 -- subject to referee review.
Citation needed for the two index facts of <1>3 (e.g. a functional-analysis textbook with locator); I did not
open one, so in a document they must be cited from a PDF (AGENTS.md section 4), not from this report.

## 3. Findings (most severe first)
No [BREAK] in scope: no statement of Theorem A or of a proved card is false, and no proved card uses index zero
outside the range where the documents settle it (section 2; downstream cards checked in section 7).
- F1 [GAP] rate_of_remainder.tex:828-832 and 842-846 (lem:groupbound <1>1, <1>4), :156 and :168-171
  (thm:exactquad <1>1, <1>4), :198-201 (thm:global <1>1), :872-876 (prop:rrr <1>3) -- "for any unitary U,
  Pm U Pp and Pp U Pm have the same singular values (CS decomposition ...)" is false for unitaries of nonzero
  index; the documents (Correction C3, l. 1026-1079) and the KB already record this and restrict to
  zeta < pi sqrt3. The first referee report repeats the same error (referee_rate_of_remainder.tex:149-153,
  "V and B have the same singular values"). Proposed closure for all s: section 2a (index additivity along the
  group + divisibility). Not in any document; needs one referee pass before the cards change.
- F2 [GAP, bookkeeping] KB card rate-of-remainder: title "global upper bound Phi <= -(1/2) log(1-2 f2 zeta^2)"
  and Statement item (2) "(thm:global with prop:rrr, unconditional)" are stronger than what the same Statement
  later says is proved (zeta < pi sqrt3; the rest rests on a conjectural and a heuristic card). A reader of the
  title gets the stronger claim. Either the repair of 2a is refereed (then the title becomes true for
  zeta < pi sqrt6) or the title/word "unconditional" is narrowed. Same wording in rate_of_remainder.tex
  prop:rrr l. 856 "with no hypothesis" and the verdictok l. 882-884 ("now unconditional").
- F3 [GAP, citation] uhlmann_upper_bound.tex:1173-1178 (lem:wick <2>1): twisted duality M' = Z F(I') Z^* is
  load-bearing for thm:A (it gives dist(a, K-bar) = dist(a, H_M'), prop:infimum <1>2; without the inclusion
  M' contained in Z F(I') Z^* the inf over h' could exceed g_B/4 and the upper bound would not meet the lower).
  It is cited to Foit 1983 with "screenshot NOT OBTAINED", but refs/BJL_twisted_duality_math-ph-0204029.pdf is in
  the repository and its Theorem 7.1 (printed p. 26, PDF p. 27: "M(q)' = Z M(q-perp) Z^*" for every closed
  Gamma-invariant q and every basis projection P) is exactly the needed statement (I read it from the PDF).
  Repair: cite BJL Thm 7.1 with a \shot, and check in a step that the chiral-fermion Fock state is the basis
  projection P of BJL's self-dual formalism and q = L^2(I) (+) its conjugate. Not a mathematical gap.
- F4 [MINOR] rate_of_remainder.tex:1072-1075 (Correction C3 (ii)) says the remaining range "needs a standard
  Fredholm-index continuity argument". Continuity is not needed: index additivity under products of Fredholm
  operators plus divisibility (section 2a <1>3-<1>4) suffices and also covers the non-group product family of
  cor:quartic and the network composite of thm:T3 (card network-global-bound-coincident), whose condition
  s zeta_max < pi sqrt3 would then drop (C5's scope; consequence only).
- F5 [MINOR] KB card const-f2 Statement: "0.0676 c eta^2 = 8 f2 eta^2"; 8/(12 pi^2) = 0.067547, which rounds
  to 0.0675 (c1_constants.out). The comparison with VWZ's 0.070 is unaffected in direction.
- F6 [MINOR] card phi-below-0085-zeta2-numerical: crossover printed 0.88681, exact 0.8868154 (c1_constants.out);
  0.88681 is a valid lower truncation, so "rigorous on (0, 0.8868]" stands. Its remark that the ratio
  -(1/2)log(1-2 f2 z^2)/z^2 increases on (0,1] is true (power series with nonnegative coefficients).
- F7 [MINOR] quadratic_limit.tex thm:summary and the verdictgap after it (l. 1191-1245) still say the sharp
  upper bound and the existence of the limit are open; only the closing status update (l. 1296) says
  otherwise. A reader stopping at thm:summary gets a weaker, outdated picture (no overclaim).
- F8 [MINOR] lem:groupbound <1>1 (l. 828-832) "both sides being monotone" for the truncation Pi_n G_s Pi_n:
  even where the identity is true the limit argument for Tr(Pp U^* Pp U) "with divergent traces cancelling in
  pairs" is not a proof; the identity ||G||_2^2 = ||V||_2^2 + ||Pp U Pm||_2^2 follows directly from
  ||G||_2 = ||U G||_2 = ||[U,Pp]||_2 and [U,Pp] = Pm U Pp - Pp U Pm (insert Pp + Pm = 1), two blocks in
  HS-orthogonal positions -- no traces of non-trace-class operators; this should replace the printed argument.

## 4. Direction ledger (AGENTS.md section 3)
| evidence | quantity | model | direction |
|---|---|---|---|
| quadratic_limit thm:lower | Phi(zeta) exact (type III, F(I)) via Phi >= Phi_P | free chiral fermion, zero-collar compression | lower bound on liminf Phi/zeta^2 |
| uhlmann thm:main-upper | Phi exact via Uhlmann trial vector Gamma(U)^*Om | same | upper bound on limsup Phi/zeta^2 |
| uhlmann prop:infimum | inf_h' ||Pm(D+ih')Pp||_2^2 | quasi-free h' only | equality with g_B/4 (both inclusions of lem:wick) |
| RoR thm:global / prop:rrr | Phi exact | same | upper bound for all zeta in range (range: section 2) |
| RoR cor:c3sign | limsup (Phi - f2 z^2)/z^3 | same | upper bound (<= 0) only; no lower rate |
| card phi-below-0085 (b) | Phi(1.0667) | extrapolated, upper side NOT certified | estimate, not a bound: (b) stays numerical (agreed) |
Verdicts: thm:A needs one lower and one upper bound on the exact Phi with equal constants: both present.
"c3 <= 0" is an upper statement only and the card says so. No ratio of one-sided bounds is used.

## 5. Independent numerical checks (tolerances fixed in the scripts before the runs)
- rigor/council/c1_constants.py -> c1_constants.out (`python3 rigor/council/c1_constants.py`): f2 = 1/(12 pi^2)
  = 0.00844343197; pi sqrt3 = 5.44140, pi sqrt6 = 7.69530; crossover 0.886815429 (card 0.88681: truncated, F6);
  ratio at zeta = 1: 0.0085155364 (card OK); 2 sqrt(0.875*0.008516) = 0.17264 (card 0.1726 OK); C2 = 4 pi 0.0374
  = 0.46998 (OK); 8 f2 = 0.067547 (card 0.0676: F5). The two "MISMATCH" lines of the output are F5 and F6.
- rigor/council/c1_gB.py -> c1_gB.out (`python3 rigor/council/c1_gB.py`, several minutes):
  (a) J = int tanh(u/2)/(u(u^2+4pi^2)) du = 1/pi^2: deviation 0 at 25 digits (tol 1e-8).
  (b) 2 iint |D1|^2/N dk dk' (closed form of kernel_identity) = 0.0675474557615585143 = 2/(3 pi^2), rel dev 4.8e-23 (tol 1e-8;
      mpmath nested quadrature). Two earlier scipy attempts are recorded in the script header (box truncation missed 6.9e-4
      because the u-tail decays like u^-3; this is a property of my first quadrature, not of the document).
  (c) kernel identity: |D1(k,k')| by direct 2-d quadrature of the position-space kernel of quadratic_limit
      def:D1 vs the closed form, at (1,-2), (3,0.5), (-4,2): rel dev 1.4e-15, 5.6e-16, 2.2e-16 (tol 2e-4);
      phases 0 or pi (a real kernel up to sign), consistent.
  Independence: (c) uses no digamma/contour step of kernel_identity.tex; (a),(b) use mpmath quadrature only.
  Single method for each number (one quadrature route each); no discretisation or regulator is involved
  except the truncation X = 70 in (c), whose cut-off weight is below e^{-35} (kernel decays like e^{-|x|/2}).

## 6. Earlier referee reports: were the repairs applied?
- referee_uhlmann_upper_bound.tex and the c11-extension-implementer notes (B6, B9, B10): Corrections C1-C10 of
  uhlmann_upper_bound.tex (l. 1522-1718) are present and I checked C1-C3, C6, C7, C9 against the text: applied.
  C7's new identity P+U_sP- = W~_s P+ e^{ish'} P- + G^v_s W~_s e^{ish'} P- verified by hand
  (G^v_s W~_s = P+W~_s - W~_s P+).
- referee_rate_of_remainder.tex prop:repair: carried into rate_of_remainder.tex prop:rrr; but the referee's
  own step (l. 149-153) uses the same false "for any unitary" singular-value claim (F1); Correction C3 records
  the gap without changing proof text (by design, l. 1028-1030).
- referee_quadratic_limit.tex (V7): the Prop. 7.1 <1>5 BREAK is marked repaired (l. 1277-1279); I did not
  re-derive Prop. 7.1 (not used by thm:A).

## 7. Inheritance (kb impact)
`kb -p cft_cmi impact group-index-zero-large-s` and `... pushforward-blocks-equal-singular-values`: rate-of-remainder,
network-global-bound-coincident, network-upper-uniform-two-corners, petz-not-optimal (all proved). I read the
Statements of rate-of-remainder, network-global-bound-coincident and petz-not-optimal: each restricts its claim to
the settled range (zeta < pi sqrt3, resp. s zeta_max < pi sqrt3, resp. leading order only), so none uses index
zero outside its proved range. network-upper-uniform-two-corners not read (C5's scope). F1/F2 are inherited by
these four cards only as range restrictions; if 2a is refereed, all four lose the restriction.
thm-a-quadratic-law and const-f2 do not depend on the two gap cards (`kb deps`).

## 8. NOT DONE
- tail_bound.tex thm:block, thm:tau, thm:main, cor:rate: not re-derived (budget); not used by Theorem A.
- rate_of_remainder.tex thm:third, sec:c3eval, sec:c (lower rates), cor:quartic proof: not re-derived; c3/c4
  scripts are not in the repository (card remainder-c3-c4-values, heuristic) so no rerun is possible.
- kernel_identity.tex: the contour/digamma proof not re-derived; only its identity checked numerically (5 (c)).
- uhlmann_upper_bound.tex prop:HS, prop:expansion, cor:varupper, lem:commutant, prop:uhlmann (parity of the
  commutant implementer): read only where the corrections touch them; not re-derived line by line.
- quadratic_limit.tex prop:gB lemmas lem:V, lem:U: replaced by the numerical recomputation 5 (a)-(b).
- Section 2a cites two textbook index facts (Atkinson; additivity and compact stability of the index) from
  knowledge, not from a PDF: a document adopting it must cite them with locators (AGENTS.md section 4).
- Imports from other seats taken as given: thm:three-faces (C2/C3), Note 4 Lemma 10.1 and Note 5 Thm 2.1/3.1
  (C3), mobius-reduction-cross-ratio (C3).
- No KB writes (council rule). Suggested for the orchestrator: a referee pass on section 2a; if it stands,
  group-index-zero-large-s and pushforward-blocks-equal-singular-values can be proved (document needed) and
  the range restrictions of rate-of-remainder, network-global-bound-coincident (thm:T3), rrr-bound-small-zeta
  lifted; fix F2, F3, F5.
