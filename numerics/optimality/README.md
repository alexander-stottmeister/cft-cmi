# numerics/optimality — S8 / problem O8 (second-order optimality of the Petz map)

Model: half-filled hopping chain, `Q_ij = sin(pi(i-j)/2)/(pi(i-j))`; regions A, B, C are
`L_A, L_B, L_C` consecutive sites, `z = L_A L_C / (L_B (L_A+L_B+L_C))`.
Continuum references (two chiralities, c = 1): Petz `8 f2 z^2 = 0.067547 z^2`,
spatial geometric compression `2 f2 z^2 = 0.016887 z^2`, `f2 = c/(12 pi^2)`.

| file | content |
|---|---|
| `opt_gaussian.py` | convex programme of rigor/optimality_second_order.tex Thm. 3.1: variables `(X,Z)`, feasible set `X Q_B X* <= Z <= 1 - X(1-Q_B)X*`; capped quantum-Fisher objective; log-barrier + damped Newton (analytic gradient, FD Hessian). Also `neglogF_grad` (double precision, gradient of the exact -log F). |
| `petz_ref.py` | Gaussian Petz recovered symbol (VWZ eq. (2.9), lambda = 0) and the exact quasi-free root fidelity (Note 5 Thm. 2.1) in mpmath at 90 digits, eigenvalues clipped consistently to `[1e-25, 1-1e-25]`. |
| `run_opt.py` | symbol assembly, `z`, first (windowed) scan — kept because it documents the window pathology. |
| `run_exact.py` | main driver: cap ladder -> candidate channel -> EXACT -log F as arbiter; writes `best_LA_LB_LC.npz`. |
| `lower_bound.py` | A-C restriction bound: convex minimisation over `(T,Zc)` of the exact A-C fidelity. |
| `compression.py` | lattice transcription of the continuum Mobius squeeze `h(x)=x/(1+lam x/L)` (fails: singular values 0.47-0.62). |
| `cp_check.py` | Prop. 2.2: explicit 4-mode Jordan-Wigner Stinespring dilation vs the covariance rule (agreement 6.7e-16). |
| `famA.log famB.log famA2.log famD.log famD2.log famE.log q416.log lb.log` | run logs (the caps and exact values quoted in Table 1). |

Key numbers (exact -log F, 90 digits): `(4,8,2)` Petz 3.2164e-4, best 8.6695e-5 (ratio 0.2695);
`(8,16,4)` Petz 3.1044e-4, best 8.6962e-5 (0.2801); `(4,12,2)` Petz 9.1816e-5, best 2.6045e-5 (0.2837).
A-C lower bound: 1.5e-9 and 9.8e-10 at `(4,8,2)`, `(4,12,2)` — i.e. zero.

CAVEAT: minimising the quantum-Fisher form on a spectral WINDOW (dropping modes) produces a
minimiser that is 880x worse than Petz — it dumps the defect into the discarded modes. Always cap
the weights instead, and always re-evaluate the candidate with the exact fidelity.
