# Phase 2 status — 2026-09-08 (day 1 of Phase 2)

## Milestone M2 (Bures part) REACHED 2026-09-08: universality of f_2 = c/(12 pi^2) for every diffeomorphism covariant net on S^1
- **Theorem B for general nets** (rigor/universality_theorem_B.tex, QA, 22 pp; refereed by QR1: stands; 4 write-up repairs applied, Sec. 9; 24 pp):
  under Haag duality / locality, Bisognano-Wichmann, Reeh-Schlieder and the implementer hypotheses (H1)-(H3) [+ (H2')],
  -log F(omega, omega_s) = (s^2/8) g_B + o(s^2), g_B = 4 dist(T(g_tot)Omega, cl A(I)'_sa Omega)^2 = c * 2/(3 pi^2).
  Mechanism: lower bound from Alberti's inequality (needs only (H3)); upper bound from Uhlmann with commutant unitaries U(phi') and (H2);
  c-linearity structural: the T-subspace H_T reduces Delta and J (only Moebius maps act, no Schwarzian), the minimiser lies in H_T, the inner
  product on H_T is c times a universal form; gamma_0 = 2/(3 pi^2) from the free fermion (Phase 1 theorem). Tensor additivity.
- **Implementer hypotheses for every diffeomorphism covariant net** (rigor/implementation_C11.tex, QB, 26 pp; refereed by QR2: stands; repairs
  applied incl. the scalar-phase lemma via Fewster-Hollands Prop 5.1 and (H2')): g_tot is C^1 + piecewise smooth with one jump of g'' at the
  touching point => ||g_tot||_{3/2} finite => Carpi-Weiner Thm 4.4 (e.s.a.), Stone, covariance by Trotter + localisation and approximation +
  additivity. Closed in the negative: D(L_0)-invariance via commutator/Nelson (form bound needs beta = 1, sharp).
- **Bosonic check** (numerics/boson, QN): U(1) current net f_2 = 0.00844(2), s_2 = 0.083(2); c-linearity of the vacuum overlap proved analytically
  at second order (boson and fermion both give (s^2/(96 pi^2)) int k^3 |g_hat|^2). Week-8 decision point resolved: proceed to paper 2.
- **Kubo-Mori** (rigor/kubo_mori_second_variation.tex, QK): exact identity for unitary orbits with affiliated generator; lower bound with no
  hypothesis; full expansion under modular analyticity; Kosaki/Petz-Donald route refuted (suprema). Open for Theorem B: T(g_tot) not affiliated
  with A(I) -> Kubo-Mori gauge lemma modulo cl(M'_sa Omega). s_2 = c/12 remains conditional.
- Free fermion (H2),(H3): rigor/uhlmann_upper_bound.tex Sec. 10 (PA).

## Corrections to the Phase 2 brief made during the day
- The smooth extension does NOT legitimise the x-space Mellin evaluation of g_B (g(L) != 0 obstruction survives); the value rests on c-linearity.
- Kosaki/Petz-Donald variational expressions are suprema: useless for the Kubo-Mori upper bound.
- The Trotter split is g_tot = (g_tot - m) + m, not g_A + g_D. Sign [L_0, T(g)] = +iT(g').
- Standard-subspace lemma (one-particle Reeh-Schlieder/BW for T-vectors) is NOT needed for Theorem B; still a GAP for the variational form.

## Open after Phase 2 day 1
- DONE: QA's repairs applied; the theorem is recorded in Note 7 (Theorem B header, Sec. 8), Note 8 (main box) and paper 2 (abstract).
- Kubo-Mori: gauge lemma REFUTED 2026-09-09 (rigor/kubo_mori_gauge_lemma.tex): inf over admissible gauges = 11.09 c/6; proved bracket 0.034c <= liminf <= limsup <= 0.924c; s_2 = c/12 for general nets stays conjectural (numerically confirmed for fermion and boson). Rate of the remainder: rigor/rate_of_remainder.tex, REFEREED (RRr): global bound Phi <= -(1/2)log(1-2 f_2 zeta^2) unconditional via the group extension, c_3 = -0.99(1), c_4 = +0.9(1), log^-2 claim refuted; Note 5 Cor 4.2, Note 7, paper 1 corrected. Certified numerics: rigor/certified_numerics.tex, REFEREED (RCr): theory right, Phi_off column was float64 noise; certified: Q_N enclosure (5.62e-18/entry); a priori Phi_W <= Phi^box <= 1.20 Phi_W; 60-digit enclosures of the box value with widths 0.71-1.01% (zeta = 1/120 ... 8/15, kappa_c = 25.3), repairs (1)-(6) applied (Sec. 9). Not certified: Dhat quadrature, box cutoff beyond kappa_max.
- DONE 2026-09-09: paper 2 draft (paper2/main.pdf, 24 pp, RW). Phase 2b running: Kubo-Mori gauge lemma (RK), rate of the remainder (RR), certified numerics (RC). Then Phase 3: optimality (O8), thermal states (O9), networks (O10), sectors (O11).

## Agents used in Phase 2 (day 1)
QA, QB, QN, QK, QR1, QR2 (+ PA resumed). Ledger: rigor/findings.pdf, 174+ entries.
