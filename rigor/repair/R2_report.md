# R2 report — repair round 2026-11-19 (Theorem B; Moebius reduction)

## FILES
- rigor/repair/R2_patch.json (17 items; `check_patch.py` exit 0). Files patched: rigor/universality_theorem_B.tex (14 items), rigor/implementation_C11.tex (2 items).
  Compile test (`--sibling R2`, pdflatex x2 from rigor/): UB 25 pp, C11 26 pp, 0 lines `^!` / undefined; stage files deleted.
- NEW rigor/moebius_reduction_general_nets.tex (483 lines, 14 pp; final log: 0 `^!`, 0 undefined reference/citation).
- NEW rigor/shots/R2_CDIT_axioms15.png (CDIT p. 22, axioms (1)-(5); cut with pdftoppm because snap.py needs pymupdf, absent).
- this report.

## KB
- added `moebius-reduction-general-nets` [proved], awaiting review. `kb -p cft_cmi lint`: 0 issues, 14 awaiting review.

## FINDINGS
- [GAP, confirmed] C2 F3: UB (S4) (H1) l. 116-126 postulated `U_s = U(phi) U_s^sharp` for C^{1,1} phi (U(phi) undefined); used in lem:ext <1>2-<1>4 and prop:geom <1>1 (eq:H1loc applied to the C^{1,1} flow phi'_tau). Repaired: items 0-8.
- [GAP, own] old lem:ext statement (arbitrary implementers, arbitrary C^{1,1} extensions, both signs of s) is unsupported once the clause is dropped; restated for C11's groups, class E, s >= 0 (C11 thm:H1 <1>7 adapted to I = (-inf,1)).
- [GAP, confirmed] C2 F2 / C6 B6: Moebius reduction for general nets had no proof; now Theorem thm:main of the new document (s >= 0 every extension; all s for one explicit extension).
- [MINOR, confirmed] C2 F4 (summary row lem:ext; "I = ABC"): items 9, 11. [MINOR, own] UB summary row "(H1)-(H3) for general nets: open (track QB)" contradicts refereed card implementer-hypotheses: item 12. Correction R2 (l. 1084) superseded note: item 13.
- [MINOR, confirmed] C2 sec. 9: C11 (C7) lists (H2') twice: item 14. [MINOR, own] C11 thm:H1 <1>7 uses `a` for both the endpoint and the Trotter step, and ktil for the flow of widehat g_tot: item 15.
- Uses of (H1) in UB after the repair: l. 116-126 (definition, patched); lem:ext l. 178-210 (re-proved without the clause); prop:H3 l. 291/300 and prop:H2 l. 393/400 (only Psi_s = U_s^* Omega: unaffected); prop:geom l. 429-445 (repaired: ||h||_{3/2} < inf, C11 thm:H1 <1>2); thm:B l. 861-875 (via prop:H2/H3: unaffected); prop:fermion l. 900-915 (cites lemmas "for the locality clause": now superfluous, harmless, not patched); tensor products l. 944-956 (covariance form holds for U^(1) x U^(2): unaffected); summary rows l. 1039-1063 and correction R2 (patched).
- Note for direction 5 (C7 D2 (iv)(a)): the 3/2-norm multiplier problem is avoidable for Moebius maps: on a fixed finite-energy vector ||T(F)psi|| <= C ||F||_{H^2}, and H^2 is stable under smooth push-forward (new doc lem:Th2, lem:push).

## ITEM TABLE
| item | disposition |
|---|---|
| C2 F1 (paper 2 title/outlook "Petz") | out of R2 scope (paper2) -> R5 |
| C2 F2 / C6 B6 | new document + UB item 16 |
| C2 F3 (UB H1, lem:ext, prop:geom) | patched, items 0-13 |
| C2 F3b (paper2 lem:ext) | out of scope -> R5 (new doc lem:ext / UB item 4-5 give the repaired proof) |
| C2 F4 | patched, items 9, 11 |
| C2 F5 (universality_normalization.tex title/boxes) | deferred: file not in R2's list (brief sec. 3); no seat named |
| C2 F6 (C11 lem:phase perfectness) | deferred: the alternative proof needs the generator identification read from CDIT/FH05; not used by the new document |
| C2 sec. 9 (H2') duplicate | patched, item 14 |
| C2 KB MINOR (thm-b-universality chart) | proposed card change 1 |
| LSV (lemma_second_variation.tex) | C2 found no item; none patched |

## PROPOSED CARD CHANGES
1. thm-b-universality, Statement: "with (H1) an implementation U_s of the C^{1,1} map" -> "in the half-line chart A = (-infinity, 0), D = (0, 1), zeta = s, with (H1) unitaries U_s with U_s A(K) U_s^* = A(ktilde_s K) for every interval K (the (C7) form of implementation_C11.tex; no locality clause for non-smooth maps)". Reason C2 F3 + KB MINOR.
2. implementer-hypotheses, Statement, append: "(H1) is proved in the (C7) form; extension independence of omega_s is proved for fields of class E and s >= 0 only (thm:H1 <1>7)."
3. mobius-reduction-cross-ratio, note: "general-net version (C11 implementers, s >= 0): moebius-reduction-general-nets (under review)".

## NUMBERS
none in the project. Scratch-only float check of lem:geom (3), (5) and the cross-ratio identity: max deviation 5e-15 (tol 1e-12).

## NOT DONE
- project script for the geometric instance (no script path in the brief).
- C2 F5, F6 (above); relative entropy in the new document (Araki definition not re-read).

## NEEDS ORCHESTRATOR
- apply R2_patch.json; `./pgit sync` for rigor/shots/R2_CDIT_axioms15.png; commit the new .tex.
- referee for moebius-reduction-general-nets (checkpoints: new doc sec:open, esp. the domain reading of CDIT Prop. 2.1).
- R5: paper2 sec_setting l. 43-45 wording proposed in new doc sec:paper2.
- card changes 1-3.
