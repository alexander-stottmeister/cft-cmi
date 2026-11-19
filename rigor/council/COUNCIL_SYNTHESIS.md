# Council of 2026-11-19 — synthesis (orchestrator)
Sources: C1_report.md ... C6_report.md, C7_directions.md. All findings are council findings, not yet on KB cards.

## Proofs: no BREAK in any theorem examined
- C1 Theorem A: thm:lower, thm:upper(i), prop:gB, thm:det, thm:main-upper, thm:A STAND. rate_of_remainder lem:groupbound,
  thm:exactquad, thm:global, prop:rrr STAND WITH REPAIR (equal singular values asserted for any unitary; valid in the
  recorded range zeta < pi sqrt3 only). Twisted duality in uhlmann_upper_bound lem:wick marked NOT OBTAINED though
  refs/BJL_twisted_duality_math-ph-0204029.pdf Thm 7.1 is the statement.
- C2 Theorem B: eq:B STANDS under (H1)-(H3); C11 proves them for all CDIT nets in the (C7) form. GAP: (H1) as stated in
  universality_theorem_B.tex l.116-126 asks U_s = U(phi) U_s-sharp for C^{1,1} phi (not proved, not needed for eq:B).
  GAP: Moebius reduction from general cross ratio to the half-line chart is carded only for the free fermion.
- C3 Foundations: Note 4 / Note 5 theorems STAND; zero-collar map normal; determinant formula as monotone limit justified.
  GAPs are stale sentences in Note 5 (O(log^-2) rate; two-sided O(eta^3)).
- C4 Optimality: thm:UH, thm:UHall, thm:main, cor:sandwich STAND; theta_fr > 0 and theta_fr >= 0.38 are NUMERICAL
  (rho = 0.0147 recomputed taper-free); 0.384 rests on one fit family (h^0.77) only.
- C5 Networks: second referee, all STAND; thm:T5 <2>2 misses a uniformly o(s^2) term (MINOR). Card wording GAP:
  c-linear law covers chains of GEOMETRIC COMPRESSIONS; "Petz chains" only for the free fermion.

## Papers: sentences stronger than their cards (C6, C2, C4)
Paper 1: prop:twobranch for every 2D CFT (card conjectural); "+O(eta^3)" remainder (only o(eta^2)); abstract "to 1e-4";
D = (c/12) zeta^2 stated as fact (conj-s2); "not optimal among all normal recovery maps" (numerical); global remainder
bound without its range; "5.6 times" stale (6.49). Paper 2: title/outlook identify the geometric compression with the
Petz recovery for general nets (proved for the free fermion only); lem:ext proof applies (H1loc) to a C^{1,1} map;
the s2 bracket is for D(omega_s||omega), the conjecture for D(omega||omega_s). 9/13 and 9/10 earlier referee edits unapplied.

## KB bookkeeping
rate-of-remainder (title "global", "unconditional") and tail-bound are 'proved' on weaker cards; 7 of 8 dependency
warnings real (missing H1/H2 assumes), deps edges of network-global-bound-coincident to the index cards spurious;
paper results without cards (eq:unconditional, h2, prop:tail, Moebius reduction for general nets); const-f2 0.0676 -> 0.0675.

## Directions (C7 ranking, with C1's addition)
1 index zero (C1 proposes: ind(P+ U_s P+) additive in s modulo compacts, hence ind = n ind(s/n) for all n, hence 0);
2 certified theta_fr > 0 in ball arithmetic; 3 uniform lower bound (U1), numerical sup-over-Delta test first;
4 s2 = r/12 for the free fermion via quasi-free relative entropy; 5 Moebius covariance of the C^{1,1} implementer;
6 D-hat certification; 7 sectors; 8 Longo-Xu Rem. 4.3 (literature check only). Paper 3 (networks) after 1 and 3.
