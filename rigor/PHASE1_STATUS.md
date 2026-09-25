# Phase 1 status — 2026-09-08 (day 1)

## Milestone M1: "make Theorem A a theorem and certify the numbers"
- **Theorem A proved.** lim_{zeta->0} Phi/zeta^2 = c/(12 pi^2). Lower bound: rigor/quadratic_limit.tex Thm 4.2 (P2, refereed by V7).
  Upper bound: rigor/uhlmann_upper_bound.tex Thms 8.1-8.2 (PA) — Uhlmann's inequality with the vector representative Gamma(W~_s)^* Omega
  from a Bogoliubov extension of the compression map (flow of -x^2 d/dx on D), vacuum overlap det(1-V^*V)^{1/2}, exact identity
  G_s = int W~^* G^(1) W~, infimum over extensions = g_B/8 via the three-way identity; refereed by PR (rigor/referee_uhlmann_upper_bound.tex),
  three repairs applied (Sec. 11). Numerics (numerics/p1_bogoliubov.out): bound/Phi = 1.0022 at zeta = 1/120; first-order infimum 0.0084465.
  Correction learned: the extension must be a circle diffeomorphism (asymptotically affine), not identity at infinity (factor-8 trap).
- **Tail bound proved** (rigor/tail_bound.tex, PT): 0 <= Phi - Phi_W <= 0.173 zeta^2/kappa_c + 0.88 zeta^2/kappa_c^2 [corrected 2026-09-24: the shape of this bound is proved; the explicit constants 0.173 and 0.88 (tail_bound.tex Cor. 5.2, eq:final) rest on numerical inputs, A_1 <= 2.0 and A_3 <= 0.0374 in double precision, not certified, and f = 0.0085 (tail_bound.tex Correction C10); card tail-bound] for
  kappa_c >= max{10, 2 log(1/zeta) + 2 log(1+kappa_c) + 3}; Note 5 Prop 4.1 upgraded to a theorem with explicit remainder; c_2 = -zeta^2/30.
  Certified brackets [corrected 2026-09-24: not certified; their upper end is eq:final of tail_bound.tex Cor. 5.2, whose constants rest on the numerical inputs above (tail_bound.tex Correction C8); card tail-bound] are wide (Phi(1/15) in [3.49, 6.53]e-5) because the proved decay is 1/kappa_c. The log^-2 rate is NOT reachable
  by window-tail + cubic-remainder arguments (incompatible requirements on kappa_c); it stays heuristic.
- **Lattice (O7a) done** (numerics/lattice, PL): Gaussian rotated Petz map in ball arithmetic up to 72 sites; exponents 1.986, 1.912, 1.635, 1.151
  at lambda = 0, 0.5, 1, 1.5 (VWZ: 2.0, 1.9, 1.7, 1.2); lattice/two-branch ratio = 1 - 0.15/L constant in eta_V; single-branch law off by 22-5000.
  Erratum: the continuum exponents 2.04/2.04/1.96/1.31 quoted earlier rested on extrapolating Phi beyond zeta = 0.53 — withdrawn.
- **Large cross ratios certified** [corrected 2026-09-24: not certified; the lower ends Phi_sub are rigorous, the quoted values are extrapolations with an estimated uncertainty; card large-zeta-values] (numerics/results_largezeta_certified.txt, PZ): Phi(1.07) = 4.410(20)e-3, Phi(2.13) = 1.0797(50)e-2,
  Phi(4.27) = 2.241(14)e-2, Phi(8.53) = 3.974(72)e-2, Phi(17.1) = 6.41(43)e-2; window exponent drifts 2.5 -> 1.2; slopes 1.29 -> 0.69 vs lattice.
  Blocker: arb eig fails for spectral range > 1e-20 (kappa_max > 45 inaccessible).
- **Paper 1 draft** (paper1/main.pdf, 26 pp, PW): all sections written; placeholder citations for internal documents; certified brackets [corrected 2026-09-24: these are the brackets of tail_bound.tex, which are not certified, see the tail-bound entry above; card tail-bound] and
  large-zeta table included; honest gap statements (s_2 = c/12 for the KM form; rate heuristic).
- **eps = 1e-14 runs**: window contains all box modes at Lambda = 60 -> residual is the box cutoff; recipe min(kappa_c, kappa_max) with box asymptotics
  0.0641 zeta^2/kappa_max^2; Phi(1/15) consistent across windows to 2e-4.

## Corrections applied today to the notes
N5: apparent exponents (PL), 'ten times' -> pi^2 (PW), Prop 4.1 status (PT), Cor 4.2 status (PA/PR), large-zeta paragraph + table (PZ).
N7: Theorem A statement, Sec. 8 items 2 (PA/PR/PT). N8: O1, O4, O7 status paragraphs. rigor/quadratic_limit.tex: status update (superseded upper bound).

## Open after day 1
- Rate of the remainder (log^-2 claim): heuristic; would need a bound on ||sqrt(Q~) - sqrt(X11 (+) X22)||_2 quadratic in X12.
- Tight certified error bars (need kappa_c^-2 decay or interval-arithmetic audit of Dhat, Q_N; 3% arithmetic margin at present).
- O7(b) chiral lattice model; O11 collar-Gaussianity lemma (deferred; Phase 2 route changed).
- Phase 2 reordering: the Uhlmann-Bogoliubov construction gives, for any diffeomorphism covariant net with U(k~) implemented, the universal
  upper bound Phi <= -log |<Omega, U(k~_zeta) Omega>| (Virasoro coherent-state overlap, c-linear at second order): O5 now yields the
  upper half of Theorem B directly; O3 is needed only for the lower half.

## Agents used today
PA (proof), PN (HS numerics), PL (lattice), PR (referee), PT (tail bound), PZ (large-zeta), PW (paper draft). Rules that worked: write-first,
<= 80-120 lines per tool call, compile/run after every append, plain LaTeX in findings entries.
