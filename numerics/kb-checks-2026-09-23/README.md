# numerics/kb-checks-2026-09-23/ — checks behind the corrections of 2026-09-23

On 2026-09-23 every proved or refereed result of this project was re-read against its proof: what each proof uses was
recorded, and each result was reviewed adversarially. That pass refuted two statements that proofs relied on (Hypothesis
(U) and the step "Phi' is nondecreasing"), narrowed several results and found errors in some of the proofs as printed.
The eleven scripts in this folder are the stored computations that the corrected results cite. The result pages cite ten
of them under "How to verify" and "Evidence"; the eleventh, `hypU_m2.py`, belongs to a refuted result that has no page
of its own and appears only in the claim map. The corrections can therefore be checked without the private knowledge
base.

The header of each script names who wrote it: `AUTH-CFT-*` are the agents that repaired the results and `REF-DEP-CFT-*`
are the referee agents.

## Running them

From the repository root, run `python3 numerics/kb-checks-2026-09-23/NAME.py` and compare the printout with `NAME.out`.
`phi_prime_check.py` finds its input `numerics/results_largezeta_certified.txt` relative to its own location, so it can be
run from any directory. Four scripts need numpy: `hypU_m2`, `refb9_winding`, `tcond_check` and `tcond_check_extra`. The
others use only the standard library. The slowest takes about 30 seconds.

On 2026-09-24 all eleven were re-run from this folder with Python 3.9.6 and numpy 2.0.2. Every printout was byte-identical
to its stored `.out` file.

## What each script checks

| script | checks | cited by |
|---|---|---|
| `tcond_check.py` | Moore-Penrose choice T = Q_AB^+ Q_AC satisfies (eq:Tcond) on the half-filled hopping chain, (L_A,L_B,L_C) = (4,8,2), (4,12,2), (4,16,2): residuals, norm of T, both margins | [ac-intertwiner-exists-hopping-chain](../../docs/results/ac-intertwiner-exists-hopping-chain.md), [ac-lower-bound-zero](../../docs/results/ac-lower-bound-zero.md) |
| `tcond_check_extra.py` | the same T violates (eq:Tcond) at (6,12,3) and (8,16,4) | both of the above |
| `hypU_m2.py` | counterexample to Hypothesis (U) in the standard form of M_2: the natural-cone inner product Tr(rho^{1/2} sigma^{1/2}) differs from the fidelity | `hypothesis-u-natural-cone-fidelity` (refuted, no page of its own) |
| `phi_prime_check.py` | the large-zeta values (rigorous lower ends, extrapolated estimates) against a nondecreasing Phi': Phi(zeta)/zeta decreases from zeta = 4.267 on, and every extrapolated continuum estimate of Phi(8.533) (at most 4.306e-2) is below twice the rigorous lower bound on Phi(4.267); the last column is zeta Phi'(zeta) | `phi-derivative-nondecreasing` (refuted, no page of its own), [two-chirality-minimum-at-lambda-zero](../../docs/results/two-chirality-minimum-at-lambda-zero.md) |
| `refb6_flow.py` | flow of the vector field -chi d/dx of def:ext for several admissible beta, and, for the standard step, the maximum of \|x - k~_s(x)\| over the grid x = 0.02, 0.04, ..., 1.98 at s = 0.25, ±0.5, ±1 | [c11-extension-implementer](../../docs/results/c11-extension-implementer.md) |
| `refb9_winding.py` | Hilbert-Schmidt norms of both off-diagonal blocks of one smoothly truncated Blaschke winding; their squares differ by exactly 1 for R/b = 5, 20, 80 | [c11-extension-implementer](../../docs/results/c11-extension-implementer.md) |
| `tailcheck.py` | the printed eq:Psi of thm:main, with the T of eq:taunu, against the claimed 0.173 zeta^2/kappa_c + 0.88 zeta^2/kappa_c^2 of Cor. 5.2 (cor:rate): grid maximum 0.97917 at (0.3325, 10), 0.97954 at the admissible point (0.3322, 10) in the same printout, and the supremum, 0.97957 at the corner, in `refb10_tail_sup.out`; also Cor. 5.2's own route through T <= 1.75 zeta^2/kappa_c^2, which exceeds the claim (ratio 1.032 at (1, 10)) | [tail-bound](../../docs/results/tail-bound.md) |
| `tailcheck_ext.py` | the same on 5.25e6 admissible points, zeta down to 1e-8, kappa_c up to 200, and with f = 0.008516 | [tail-bound](../../docs/results/tail-bound.md) |
| `refb6_psi_check3.py` | eq:Psi of thm:main in the saturating case of the Bures-angle triangle inequality, printed bound against corrected bound | [tail-bound](../../docs/results/tail-bound.md) |
| `refb6_tailcheck_corrected.py` | eq:final with the corrected chain of thm:main (step <1>5) | [tail-bound](../../docs/results/tail-bound.md) |
| `refb10_tail_sup.py` | the chain ratios along the edge kappa_c = 10, along the boundary curve kappa_c = kappa_dagger(zeta) for kappa_c up to 30, and on a small patch at the corner (11 e^{-3.5}, 10), where all three maxima sit; with the grid of `refb6_tailcheck_corrected.py` (kappa_c up to 200) this puts the supremum over the scanned region at that corner | [tail-bound](../../docs/results/tail-bound.md) |

## Differences from the knowledge-base copies

The scripts were first stored in the private knowledge base. The copies here differ in three places, none of which
changes a printout: the input path in `phi_prime_check.py`, a comment in `refb6_tailcheck_corrected.py` that named the old
folder, and a comment in `tcond_check_extra.py` that said the script was not cited by any result.
