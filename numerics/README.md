# numerics/ — result files and which table uses them (state 2026-09-05, corrected basis)

Code: `compression_box.py` (box compression Q_box with absolute-basis phase `xi0=log(a/L)`), `fidelity_flint.py`
(exact fidelity/relative entropy in the spectral window, python-flint 40 digits; first-order coefficients f2, s2 in the window
+ UV tail), `fidelity_hp.py` (Q_box itself in mpmath for eps=1e-11 runs), `make_tables.py` (writes ../fidelity_tables.tex).

| file | content | used in |
|---|---|---|
| results_final2.txt | Phi(1/15) for 9 (Lambda, kappa_max) combinations, eps=1e-8 | Table "convergence" |
| results_A2.txt | zeta scan, Lambda=60, kappa_max=30, eps=1e-8 | Table "scan", column A |
| results_L120_2.txt | zeta scan, Lambda=120, kappa_max=45, eps=1e-8 | Table "scan", column B |
| results_hp2.txt | zeta scan, Lambda=60, kappa_max=30, eps=1e-11 (Q in 40 digits) | Table "scan", column C and S_inf |
| results_first_window.txt | first-order coefficients f2_sub(+tail), s2_sub for eps=1e-8, 1e-11, 1e-14, 1e-16 | Table "second-order" (1e-16 omitted: double-precision floor) |
| results_first3.txt | same at eps=1e-8 for all 13 Dhat_first files | consistency check |
| results_A.txt, results_final.txt, results_L120.txt, results_hp.txt, line_so.txt | OLD (basis-phase bug, 5e-5 relative effect on Phi) | superseded, kept for the audit rigor/check_note5_numerics.tex |

Regenerate the tables with `python3 make_tables.py` (from this directory), then recompile ../fidelity_recovered_quasifree.tex.

Independent checks by verification agents: `v4_*.py` (V4, fidelity numerics), `v5chk.py`, `v5en.py` (V5: <TT> normalization, Liouville energy functional).

Checks behind the corrections of 2026-09-23 (two refutations, narrowed statements, errors found in printed proofs):
[`kb-checks-2026-09-23/`](kb-checks-2026-09-23/README.md), eleven scripts with their outputs; its README says which result cites which.

### Track C (2026-09-08): eps = 1e-14 runs (results_hp14.txt)
At eps = 1e-14 (kappa_c = 32.2) the window contains ALL box modes for Lambda = 60, kappa_max = 30 (n_sub = N = 91): nothing is
discarded, the "sub" value is the full box-compression value, and the residual error is the BOX cutoff, not the window. The tail
must then be taken with min(kappa_c, kappa_max): with kappa_max = 29.6 the box-cutoff asymptotics of the second-order coefficient
(g_B - g_B^(Lambda) = 0.513 r/Lambda^2, rigor/referee_quadratic_limit.tex) gives a tail 0.0641 zeta^2/kappa_max^2 (window formula: 0.0667 zeta^2/kappa_c^2).
Example zeta = 1/15: raw 3.48658e-5 + 3.25e-7 = 3.5191e-5, consistent with the eps = 1e-8 (3.5193e-5) and eps = 1e-11 (3.5199e-5) corrected values to 2e-4 relative.
The printed "+tail" column of results_hp14.txt uses kappa_c and is therefore slightly too small for these files (3.5151e-5); use the corrected recipe above.

Lattice (O7a, agent PL): `lattice/petz_lattice.py` (Gaussian rotated Petz map on the hopping chain, flint ball arithmetic), `lattice/petz_lattice.out`, `lattice/sweep.raw`, `lattice/collapse.png`, `lattice/README.md`. Large-zeta continuum run: `run_largezeta.sh` -> `results_largezeta.txt`.

### Large-zeta continuum values (2026-09-08, results_largezeta.txt; Lambda=60, kappa_max=30, eps=1e-8)
zeta = 1.067, 2.133, 4.267, 8.533, 17.07: Phi_sub = 4.230e-3, 1.012e-2, 2.010e-2, 3.343e-2, 4.779e-2 (rigorous lower bounds).
Local log-slopes of Phi_sub: 1.26, 0.99, 0.73, 0.52 -- flattening, while the lattice (lattice/petz_lattice.out) finds Phi ~ zeta^1.1 up to zeta ~ 23.
CAVEAT: the printed "+tail" column uses the small-zeta second-order tail zeta^2/(15 kappa_c^2), which is meaningless at large zeta (it exceeds
the raw value at zeta = 17). The window/box systematics at large zeta are under study (run_largezeta2.sh -> results_largezeta2.txt:
eps = 1e-8/1e-11/1e-14 and Lambda = 120, kappa_max = 45). Until then, use Phi_sub as a lower bound only.

### Large-zeta systematics (2026-09-08, results_largezeta2.txt)
zeta = 2.133: Phi_sub = 1.012e-2 (kappa_c 18.4), 1.046e-2 (25.3), 1.057e-2 (32.2 = full box, kappa_max 30); Lambda = 120 changes the 18.4 value by -3e-5 only.
zeta = 8.533: Phi_sub = 3.343e-2, 3.598e-2, 3.696e-2 (same windows).  The window dependence grows with zeta: the small-zeta tail formula is useless here.
Two-point extrapolations (kappa_c = 25.3, 32.2): 1/kappa_c^2 law -> Phi(2.133) = 1.074e-2, Phi(8.533) = 3.85e-2; 1/kappa_c law -> 1.096e-2, 4.05e-2.
Brackets: Phi(2.13) in [1.06, 1.10]e-2 (4%), Phi(8.53) in [3.7, 4.05]e-2 (10%). Extrapolated slope between them ~0.93 (raw sub values gave 0.73; lattice ~1.1).
TODO (numerics item for paper 1 / Note 6 P3): larger kappa_max boxes (Lambda = 120, kappa_max = 60-90 in 40-digit arithmetic) and a
fitted tail law at fixed large zeta, to certify Phi for zeta >~ 1 to 1%.
Lattice comparison at large zeta (lattice/petz_lattice.out): Phi_lat(1.986) = 1.004e-2 and Phi_lat(11.52) = 5.61e-2; rescaled with slope ~1 these give
~1.07e-2 at zeta = 2.13 and ~4.2e-2 at zeta = 8.53, i.e. inside the continuum brackets and favouring the 1/kappa_c extrapolation (per-mode UV tail ~ kappa^-2 at large zeta).

### Certified large-zeta continuum values (2026-09-08, agent PZ; `results_largezeta_certified.txt`, `fidelity_table_largezeta.tex`)
New pipeline `run_largezeta_cert.py` (+ `analyze_largezeta.py`): box compression Q and its **high-precision eigendecomposition in
python-flint** (`acb_mat.eig`, cached per box in `qeig_*.pkl`; quadratures cached per Lambda in `quads_*.pkl`), sub-compression
`Qs = diag(w) - P^H D P`, and the tau-step (`tau = eig(W W^H)`, `W = D_w U D_q`) in **mpmath `eighe`** — arb's `eig` returns nan
on that matrix, and it also fails on Q itself once the spectral range exceeds ~1e-20, which caps the usable box at kappa_max <= 45
(kappa_max = 60, range 1e-26, gives `w in (nan,nan)`). Reproduces `fidelity_hp.py`/`fidelity_flint.py` to 7 digits at
(Lambda,kappa_max) = (60,30) and (120,45) for eps = 1e-8, 1e-11, 1e-14. Windows extended to eps = 1e-17, 1e-19 (kappa_c = 39.1, 43.7).
* **Box dependence is negligible**: at fixed kappa_c, Lambda = 60/120/180 (kappa_max = 45, N = 137/273/411) agree to 5e-4..1.6e-3
  relative at zeta = 2.13 and 8.53, decreasing with kappa_c. The whole systematics is the *window*.
* **Window (UV) tail law.** `Phi_sub(kappa_c) = Phi_inf - b kappa_c^{-p}` fits the four/five windows with an effective exponent that
  *drifts down with zeta*: p = 2.49, 2.31, 1.98, 1.76, 1.21 at zeta = 1.07, 2.13, 4.27, 8.53, 17.07. So the small-zeta law
  (p = 2, from the kappa^-3 occupation tail) survives only up to zeta ~ 4; at large zeta the discarded UV weight decays like
  kappa^-2 per mode and p -> 1. Fixed-p fits bracket the answer: p = 2 undershoots, p = 1 overshoots by up to 4%.
* **Certified values** Phi(zeta) = -log F (bracket [Phi_sub(kappa_c^max), Phi_inf], best = free-p extrapolation):
  zeta = 1.067: 4.410e-3 (0.45%); 2.133: 1.0797e-2 (0.46%); 4.267: 2.2414e-2 (0.60%); 8.533: 3.974e-2 (1.8%); 17.07: 6.41e-2 (6.6%).
  The 1% target is met for zeta <~ 8; at zeta = 17 the window extrapolation is not yet converged (needs kappa_c >~ 60, i.e. an
  eigensolver that survives a 1e-26 spectral range).
* **Local log-slope** d log Phi/d log zeta = 1.29, 1.17, 0.94, 0.76, 0.69 at zeta = 1.07, 2.13, 4.27, 8.53, 17.07 — Phi flattens
  steadily, it is *not* a power law. Lattice (`lattice/petz_lattice.out`, log-log interpolated) gives 1.41, 1.18, 0.98, 0.87, 0.68
  and Phi_lat/Phi_cont = 1.011, 1.017, 1.030, 1.114, 1.281: agreement at the 1-3% level for zeta <= 4 (within the lattice's
  3-7% finite-L UV effect), growing to 11%/28% at zeta = 8.5/17 where both sides are least controlled.

Note (2026-09-08): fidelity_hp.py fails at N = 273 (Lambda = 120, kappa_max = 45) with eps = 1e-14: mpmath's tridiag_eigen does not converge
(results_hp14_L120.err). Use PZ's pipeline (run_largezeta_cert.py: python-flint eigendecomposition of Q, mpmath only for the tau step) for large
boxes at small eps; it reproduces fidelity_hp.py to 7 digits at (60,30) and (120,45).

Bosonic check (O6, agent QN): `boson/boson_recovery.py`, `boson/boson_recovery.out`, `boson/check_forms.py`, `boson/README.md` — U(1) current net f_2 = 0.00844(2), s_2 = 0.083(2); c-linearity of the vacuum overlap.
