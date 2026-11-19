# R1 report — repair round 2026-11-19 (index zero, Theorem A). Actor R1, Opus. Not refereed.

## FILES
- rigor/index_zero.tex (505 lines; 11 pages; final pdflatex log: 0 lines matching `^!` or undefined Reference/Citation) + .pdf/.aux/.log
- rigor/index_zero_check.py (120 lines), rigor/index_zero_check.out (34 lines)
- rigor/repair/R1_patch.json (13 items, 3 files; check_patch.py exit 0; staged compiles of all three patched files
  clean: rate_of_remainder 21 pp, quadratic_limit 27 pp, uhlmann_upper_bound 36 pp; _stage_ files deleted)
- rigor/shots/r1_BJL_{thm71,sec7_setup,basisproj,Mq,twist,complex}.png (rigor/snap.py, pymupdf from a scratch venv)
- this report

## KB
No card added or changed (brief §1). `kb -p cft_cmi lint`: 0 issues, 21 awaiting review (22 dependency/locator warnings, pre-existing).

## FINDINGS
- Result (index_zero.tex Thm 3.1, 5.1, Lemma 5.2, Thm 4.2): for every unitary group U_s with ||P_+ - U_t^* P_+ U_t||_2 -> 0
  as t -> 0 (e.g. form-[P_+,K] in S_2 on a core), ind(P_+U_sP_+|) = 0 for ALL real s, hence equal singular values of the
  two blocks. Route: ind X_s = Tr(G_s^3) (integer, Lemma 2.3(d)), S_2-continuous in s via the cocycle G_{s+t} = G_s + U_s^*G_tU_s.
  Self-contained (spectral theorem for self-adjoint HS operators proved in App. A); no external theorem.
  Applications (Sec. 6): push-forwards W~_s, e^{s(D+ih')}, product families (RR cor:quartic, NW thm:T3, EF thm:UH),
  EF lem:group <1>1. Ranges lifted: Prop. 7.1.
- [GAP] C1 F1 confirmed (RR l. 156, 168-171, 198-203, 828-832, 842-846, 855, 872, 392): patched, citing index_zero.tex "under review".
- [GAP] C1 F3 confirmed (uhlmann l. 1173-1176): patched with BJL Thm 7.1 (PDF p. 27), hypotheses checked one by one.
- [GAP] C1 F2 confirmed (RR l. 855 "with no hypothesis", l. 882 "unconditional"): patched; card title -> below.
- [MINOR] C1 F8 confirmed: replaced by index_zero Lemma 4.1 (no traces of non-trace-class operators).
- [MINOR] C1 F4 partly confirmed: the C3(ii) sentence is stale (patched). Its claim "continuity is not needed" holds only for
  C1's route 2a, which needs Fredholm-index facts with no source in refs/; index_zero.tex uses continuity.
- [MINOR] C1 F7 confirmed (quadratic_limit thm:summary): status paragraph added.
- [MINOR] new: BJL twist identification uses "Z = second quantisation of -1" (paraphrase, BJL p. 5; its source [4] NOT
  OBTAINED); the sign of Z is shown immaterial in the patch.
- [MINOR] new: Lemma 6.1 for a general admissible chi rests on (W) as asserted by RR lem:autocorr, whose PA inputs
  (lem:kernel, lem:integralrep) are stated for chi supported in [0,2] / phi = id off a compact set (pre-existing).
- [MINOR] new, out of scope (R3/C5): EF lem:group <1>1 "for any unitary U" and NW thm:T3 / lem:onegroup(i) restrictions
  are removable by index_zero Lemmas 6.3-6.4 (Prop. 7.1 items 6-7); not patched here.

## ITEM TABLE
| item | locator | action |
|---|---|---|
| C1 F1 | RR l. 156, 168-171, 198-203, 828-832, 842-846, 872, 392 | patched (8 items) + new document |
| C1 F2 | RR l. 855, 882; card rate-of-remainder | patched (2); card change proposed |
| C1 F3 | uhlmann l. 1173-1176 | patched (BJL Thm 7.1, 6 shots) |
| C1 F4 | RR l. 1075-1076 | patched (pointer to index_zero.tex); "continuity not needed" not confirmed for our route |
| C1 F5 | card const-f2 | card change proposed |
| C1 F6 | card phi-below-0085-zeta2-numerical | card change proposed (cosmetic) |
| C1 F7 | quadratic_limit l. 1189 | patched |
| C1 F8 | RR l. 829-832 | patched (with F1) |
| C1 F1 (referee report) | referee_rate_of_remainder.tex:149-153 | deferred: a referee record, not edited |
| C1 C3(i) | RR l. 1068 | patched (records the written proof) |
| brief (a) | index_zero.tex + check | new document |

## PROPOSED CARD CHANGES (to execute only after a referee passes index_zero.tex)
1. group-index-zero-large-s: status conjectural -> proved; evidence += doc:rigor/index_zero.tex#thm:group, doc:rigor/index_zero.tex#lem:app-K; next: none; Statement unchanged.
2. pushforward-blocks-equal-singular-values: heuristic -> proved; evidence += doc:rigor/index_zero.tex#lem:app-W; note: proof by index continuity, not by complex conjugation.
3. rate-of-remainder: title/Statement (2): "for zeta < pi sqrt3 (= (4 f2)^{-1/2})" -> "for 0 <= zeta < pi sqrt6 (= (2 f2)^{-1/2})"; depends += the two cards above. BEFORE review (F2): replace "unconditional" by "proved for zeta < pi sqrt3; up to pi sqrt6 subject to rigor/index_zero.tex (under review)".
4. network-global-bound-coincident: drop "s zeta_max < pi sqrt3"; range "s Z < pi sqrt6" (index_zero Prop. 7.1 item 6).
5. const-f2 Statement: "0.0676 c eta^2 = 8 f2 eta^2" -> "0.0675 c eta^2 = 8 f2 eta^2" (8/(12 pi^2) = 2/(3 pi^2) = 0.067547).
6. phi-below-0085-zeta2-numerical: "0.88681" -> "0.886815" (C1 c1_constants.out; not recomputed by R1; the old value is a valid truncation).

## NUMBERS
All from `${PYTHON:-python3} rigor/index_zero_check.py > rigor/index_zero_check.out` (tolerance 1e-10 fixed in the script):
- validation: max |U_mn - i^(m-n) J_(m-n)(2s)| = 5.1e-16 (s = 2.7, |m|,|n| < 60).
- model (A), ||[P-,K]||_2 = 1.1314 (old range |s| < 0.8839): max_k |sv_k(B) - sv_k(C)| <= 4.5e-16 at s = 0.5, 1.5, 3, 4, -3.5
  (||G_s||_2^2 up to 3.233); truncation bound <= 1.6e-79; single method.
- shift example (B): s = 1: sv(B) = {1}, C = 0 (index -1); s = 1/2: ||C||_2^2 = 0.4474, 0.5172, 0.5873, 0.6574 at
  window M = 100, 200, 400, 800 (not HS; increment 0.070 per doubling, no derivation).

## NOT DONE
- No referee of index_zero.tex (outside a track agent's role).
- Patches to exact_fidelity_upper_half.tex and network_second_order.tex (R3's files): consequences listed in index_zero Prop. 7.1.
- C1 F6 crossover not recomputed.

## NEEDS ORCHESTRATOR
- `./pgit sync` for rigor/shots/r1_BJL_*.png (6 files); commit rigor/index_zero.{tex,pdf}, rigor/index_zero_check.{py,out}, rigor/repair/R1_*.
- One Opus referee on rigor/index_zero.tex before the card changes; the patches cite it as "under review" with its numbering (Lemma 6.1-6.3, Thm 3.1/4.2/5.1, Lemma 5.2).
- Patches C1 F3 and F7 do not depend on index_zero.tex and can be applied now.
- Forward Prop. 7.1 items 6-7 to R3 (EF lem:group <1>1, NW thm:T3, lem:onegroup, Corrections R2/R3).
- Deviation: pymupdf installed in a scratchpad venv (brief §7 said not installed) to run rigor/snap.py.

## ROUND 2 (after referee REF-RP-4, items 6, 7, 9, 10; R1_patch.json already applied)
- index_zero.tex (528 lines, 12 pages, log clean):
  (1) (W) made explicit: lem:app-prod (a) "with PA's field", (c) "for chi satisfying (W)"; Sec. 7 gains a "Scope of (W)"
      paragraph: items 1 (K = D+ih'), 4, 5, 6, 7 hold for PA's field without extra hypothesis; items 2, 3 and
      lem:app-prod (c) are stated for chi satisfying (W); verdictgap updated (REF-RP-4 item 6 GAP, pre-existing in RR).
  (2) prop:ranges item 3 corrected: thm:global gives f2^chi (and f2^star whenever 2 f2^star zeta^2 < 1), NOT the f2
      form (f2^star = f2 unproved, RR prop:f2star: f2 <= f2^star <= 1.00071 f2 numerically); the f2 form on
      [0, pi sqrt6) comes only from item 4 (prop:rrr). The constants sentence of Sec. 7 corrected likewise.
  (3) Sec. 8 rewritten: a paragraph on what a finite truncation can and cannot test; (A) now uses complex NNN hopping
      0.4i (B != C^T, max|B - C^T| = 0.335-0.765) and is labelled non-discriminating; the false sentence (old l. 422-423)
      removed; (B) gains s = 2 (index -2).
- index_zero_check.py / .out regenerated (window N = 450, M = 150, TOL 1e-10): validation 7.1e-16; (A) max sv
  difference <= 6.7e-16 at s = 0.5, 1.5, 3, 4, -3.5, ||[P-,K]||_2 = 1.3856, HS of dropped part <= 6.8e-25;
  (B) s = 1: one singular value 1 in B, none in C; s = 2: two vs none.
- R1b_patch.json (7 items, 2 files; check_patch exit 0; --sibling R1b compiles: RR 21 pp, PA 36 pp, 0 errors; stage files
  deleted): RR l. 156, 170, 203, 1068 get "for chi satisfying (W) of index_zero.tex Lemma 6.1"; PA l. 1395-1397 stale
  Foit entry replaced by the BJL Thm 7.1 entry; PA lem:wick box: twist paraphrase replaced by BJL p. 8, eqs. (8)-(9)
  (Z~ Omega = Omega, Z Omega = Omega), new shot rigor/shots/r1_BJL_twist89.png replaces r1_BJL_twist.png in the box.
- Proposed card texts (after review):
  pushforward-blocks-equal-singular-values, Statement: "For every admissible field chi (rate_of_remainder.tex Def. 2.1)
  satisfying condition (W) of rigor/index_zero.tex Lemma 6.1 (W~_s = e^{sD} a strongly continuous unitary group and
  G_s = int_0^s W~_sigma^* G^(1) W~_sigma dsigma in S_2 for every real s; proved by PA lem:gen and lem:integralrep for
  PA's field, chi = chi' = 0 off [0,2]), and every real s, ind(P_+ W~_s P_+|_{P_+H}) = 0, so P_- W~_s P_+ and P_+ W~_s P_-
  have the same singular values with multiplicities (index_zero.tex Lemma 6.1, Theorems 5.1, 4.2)."
  group-index-zero-large-s, title: "Index zero for every real s: for a unitary group e^{sK} with [P_+,K] Hilbert-Schmidt
  in the form sense on a core, ind(P_+ e^{sK} P_+|_{P_+H}) = 0 and the two off-diagonal blocks have the same singular
  values"; How to verify: "rigor/index_zero.tex Thm 5.1 (thm:group) with Lemma 5.2 (lem:gen) and Thm 4.2 (thm:sv); for
  K = D + ih', h' in A', Lemma 6.2 (lem:app-K); counterexample without the hypothesis: Sec. 8 (B), rerun
  ${PYTHON:-python3} rigor/index_zero_check.py and compare with rigor/index_zero_check.out."
- NEEDS ORCHESTRATOR: ./pgit sync for rigor/shots/r1_BJL_twist89.png (r1_BJL_twist.png becomes unused); re-review of
  index_zero.tex Secs. 7-8 by one referee.
