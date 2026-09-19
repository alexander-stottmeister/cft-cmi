# `numerics/boson/` — chiral free boson (U(1) current net, c = 1): Petz-recovery defect

Track QN (O6) of the Phase-2 brief: repeat the Note-5 recovery computation for the U(1) current net
and test the universality prediction `f_2 = c/(12 pi^2)`, `s_2 = c/12` proved/measured for the Dirac
fermion (`f_2 = 0.008444(1)`, `s_2 = 0.0837(5)`, both with c = 1).

Code: `boson_recovery.py` (self-contained; `PYTHONPATH=.. python boson_recovery.py run` -> `boson_recovery.out`,
which is the log of every table quoted below).  Screenshot of the fidelity formula used:
`rigor/shots/QN_BBP_fidelity.png` (Banchi-Braunstein-Pirandola, arXiv:1507.01941 = `refs/BBP_1507.01941.pdf`, Eq. (15)).

## 1. Conventions

Current `J`, weight 1, `<J(x)J(y)> = -1/(4 pi^2 (x-y-i0)^2)`; the Sugawara tensor then has
`<T T> = (1/(8 pi^2))(x-y-i0)^{-4}`, i.e. **c = 1**.  Smeared `J(f) = int f J dx`, real `f in C_c^inf`:

* `<J(f)J(g)> = (1/(4 pi^2)) int_0^inf p conj(fhat(p)) ghat(p) dp`,  `fhat(p) = int f e^{ipx} dx`;
* commutator `[J(f),J(g)] = (i/(2 pi)) int f g' dx`.

Gaussian conventions are those of BBP / Weedbrook: `[x_j,x_k] = 2i Om_jk`, `V_jk = (1/2)<{x_j,x_k}>`,
**vacuum `V = 1`**, symplectic eigenvalues `nu >= 1`.  With `x_j = J(b_j)` this means

    Om(f,g) = (1/(4 pi)) int f g' dx,
    V(f,g)  = (1/(8 pi^2)) int int (f(x)-f(y))(g(x)-g(y))/(x-y)^2 dx dy    (Moebius invariant).

Test functions carry weight 0 (`f |-> f o k^{-1}`), i.e. the current is pushed forward with weight 1,
`U_s J(f) U_s^* = J(f o k~_s^{-1})`.  Hence on `A(I)` the recovered state is the Gaussian state with

    V_s(f,g) = V(f o k_s^{-1}, g o k_s^{-1}),      Om unchanged (Om is diffeo invariant).

`k_s` = Note-4/5 map: identity on `A = (-a,0)`, `h_s(x) = Lx/(L+sx)` on `D = (0,L)`; `a = 1`, `L = 2`, `zeta = s/3`.

## 2. Modular frame and the mode compression

`I = (-a,L)`, `y = (x+a)/(L-x)`, `t = log y` maps `I -> R`.  In this frame

    Om(f,g) = (1/(4 pi)) int_R f dg/dt dt,
    V(f,g)  = (1/(8 pi^3)) int_R M(k) conj(fhat) ghat dk,   M(k) = pi k coth(pi k),

so the symplectic-eigenvalue density is the **Bose factor** `nu(k) = M(k)/(pi|k|) = coth(pi k)
= 1 + 2/(e^{2 pi |k|}-1)` — the exact bosonic counterpart of the fermionic Fermi symbol.
(The `-1` of the interior kernel `1/(4 sinh^2((t-t')/2))`, symbol `pi k coth(pi k) - 1`, is cancelled by the
collar term `2 int f g dt` coming from `y` outside `I`.)

**Mode compression.**  `N` Hermite modes `psi_n(t) = sig^{-1/2} phi_n((t-t_c)/sig)`, `t_c = tau(0) = -log 2`
(the kink).  Effective box `Lam = 2 sig sqrt(2N)`, UV cutoff `kap_max = sqrt(2N)/sig`; these are smooth and
Schwartz, so the linearly growing symbol `M ~ pi|k|` is harmless.  `Om` is exact (tridiagonal), `V` exact by
Gauss-Legendre on the Hermite Fourier transform.  Restricting both states to the Weyl algebra over a finite
symplectic subspace is a restriction to a subalgebra, so by monotonicity every number below is a **lower bound**.

**Localisation of the perturbation (exact).**  `k_s = id` on `A` and `k_s = h_s` (a *global* Moebius map) on `D`,
and `V` is Moebius invariant, so `V_s - V` vanishes on `A x A` and on `D x D`.  With `f = f_A + f_D`,

    (V_s - V)(f,g) = -(1/(4 pi^2)) int_A du int_D dv [f(u) G_g(v) + g(u) G_f(v)] / (4 sinh^2((u-v)/2)),
    G_f(v) = f(beta_s(v)) - f(v),   beta_s = tau o h_s^{-1} o tau^{-1}   (= 0 for v > tau(L/(1+s))).

No FFT of a log-squeezed function and no extension of `k_s` beyond `I` is needed.

**Spectral window.**  Williamson-diagonalise the vacuum block; keep the modes with `nu - 1 > eps`
(`kappa_c = log(2/eps)/(2 pi)`), discard the numerically pure UV modes; restrict both states to that
symplectic subspace.  Double precision allows `eps` down to `1e-14`, i.e. `kappa_c = 5.24`.

## 3. Validation (section 0-1 of `boson_recovery.out`)

* **Gaussian formulas vs exact density matrices in a truncated Fock space**, 1/2/3 random modes:
  covariance round trip, BBP fidelity Eq. (15) and the Gaussian relative entropy
  `D = S(V_2) - S(V_1) + (1/4) Tr[G_2 (V_1 - V_2)]`, `G = 2 i Om arccoth(V i Om)`, all agree to the Fock
  truncation level (1 mode / ncut 60: `2e-13`, `5e-10`, `1e-12`; 2 modes: `2e-6`; 3 modes: `6e-3`, both
  truncation-limited, the covariance error being the same size).
* **Flat symbol test**: replacing `M` by `pi|k|` (the vacuum of the theory whose line is `R_t`) must give a
  *pure* state.  Obtained: `nu_flat >= 1` with median `1.000000000` (only the few edge modes of the Hermite
  span reach 1.65).  This fixes the relative normalisation of `V` and `Om`.
(The last two are in `check_forms.py`, which also re-derives `V` and `Om` from position space.)

* **Moebius invariance** `V(f o beta_s) = V(f)` for `f` supported in `D`: relative error `4e-15`.
* **Localisation formula** for `V_s - V` against a direct FFT evaluation of `V(f o k_s^{-1})`: `8e-8`.

## 4. Results

Everything is converged in `Lam` and `kap_max`: at `s = 0.2`, `(N,sig) = (60,1.6) ... (240,3.2)`
(`Lam = 35 ... 140`, `kap_max = 6.9 ... 15.4`) give `Phi/zeta^2 = 0.00789 +- 0.00005` and
`D/zeta^2 = 0.0645 +- 0.001`.  **The whole systematics is the spectral window.**

### Exact second-order coefficients (no finite-s extrapolation, no cancellation)

`E' = d(V_s-V)/ds` at `s = 0` is computed analytically (`G_f'(v) = psi'(v) gam(v)`,
`gam(v) = (L e^v - a)^2/(L(L+a)e^v)`), and then
`Phi = Phi_2 s^2`, `D = D_2 s^2` follow from the Bures metric (BBP Eq. (27)) and the Kubo-Mori metric
`g_KM = -(1/2) Tr(G' V'_BBP)`; `f_2 = 9 Phi_2`, `s_2 = 9 D_2`.

| `kappa_c` | 1.58 | 2.31 | 3.04 | 3.77 | 4.51 | 5.24 |
|---|---|---|---|---|---|---|
| `f_2` | 0.007915 | 0.008226 | 0.008351 | 0.008383 | 0.008391 | 0.008405 |
| `s_2` | 0.059029 | 0.067017 | 0.072487 | 0.074552 | 0.075097 | 0.076322 |

UV tail fits `X(kappa_c) = X_inf - b kappa_c^{-p}` over `kappa_c >= 2.3` (three bases, N = 60/120, sig = 1.6/2.26):

* `f_2`: free `p = 2.3-2.8` -> **0.008426 - 0.008438**; forced `p = 2` -> 0.008451-0.008457; `p = 1` -> 0.008555.
* `s_2`: free `p = 1.14-1.39` -> 0.0810-0.0824; forced `p = 1` -> **0.0838-0.0842**; `p = 2` -> 0.0782.

The different exponents are expected: the discarded per-mode weight decays like `kappa^{-3}`, and the
Bures metric integrates it directly (`p = 2`) while the Kubo-Mori metric carries the extra modular-energy
factor `kappa` (`p = 1`).  Best values:

    f_2 = 0.00844 (2)      vs   1/(12 pi^2) = 0.0084434
    s_2 = 0.083  (2)       vs   1/12        = 0.0833333

i.e. **agreement at the 0.2% (f_2) and 1% (s_2) level: universality confirmed for c = 1.**

### Finite-s scan (`eps = 1e-12`, `N = 120`, `sig = 1.6`)

`Phi/zeta^2 = 0.00744, 0.00789, 0.00804` at `s = 0.4, 0.2, 0.1`, rising towards `f_2`.  Below `s ~ 0.05`
`Phi ~ 1e-6` and double precision loses the last digits (2-5% scatter); `D` is worse still — it is a
difference of two O(1) entropies and goes *negative* below `s ~ 0.1`.  That is why the second-order
coefficients above are computed **at** `s = 0` (exact metric formulas) rather than extrapolated in `s`.
A high-precision (flint/mpmath) finite-s scan would be needed to see the s-dependence of `D` directly.

## 5. c-linearity of the vacuum overlap (boson vs fermion, same `k~_s`)

Same circle diffeo `phi = k~_s` (`p1_bogoliubov.KMap`, extension `beta = 1`), two one-particle spaces:

* fermion (weight 1/2): `(W f)(x) = f(psi(x)) psi'(x)^{1/2}`, `V = P_- W P_+`,
  `-log|<Om, Gam_f Om>| = -(1/2) Tr log(1 - V^*V) = (1/2)E + O(s^3)`, `E = ||V||_2^2`;
* boson (weight 0): `(T f)(x) = f(psi(x))` on `H^{1/2}`; in the orthonormal Fourier basis
  `M_{nm} = sqrt(|k_n|/|k_m|) (1/2X) int e^{-i k_n x + i k_m psi(x)} dx`, `B = P_- M P_+`,
  `-log|<Om, Gam_b Om>| = (1/4) Tr log(1 + B^*B) = (1/4) Tr(B^*B) + O(s^3)`.

**Analytically**, with `phi = x + s g`: `W(p,q) = delta + (is/4 pi) (p+q) ghat(p-q)` and
`M(p,q) = delta + (is/2 pi) sqrt(|p/q|) q ghat(p-q)`, so

    E = (s^2/(48 pi^2)) int_0^inf k^3 |ghat|^2 dk  (= s^2 Q[g], reproducing p1_bogoliubov),
    Tr(B^*B) = (s^2/(24 pi^2)) int_0^inf k^3 |ghat|^2 dk = 2 E,

hence `-log|<Om, Gam_b Om>| = (1/4)Tr(B^*B) = (1/2)E = -log|<Om, Gam_f Om>| = (s^2/(96 pi^2)) int_0^inf k^3|ghat|^2 dk`,
i.e. **the two overlaps agree exactly at second order**, both equal to `(s^2/2)||T(g)Omega||^2` with the same
`c = 1` stress-tensor two-point function.

**Numerically** (`s = 0.1`, box `[-X,X)` with `|k| <= 20`): `Tr(B^*B)` is nearly box-independent
(`6.615e-4, 6.685e-4, 6.703e-4` for `X = 25, 50, 100`), while `E` has a `1/X` IR box error
(`2.473e-4, 2.887e-4, 3.112e-4` -> box-free quadrature value `E = 3.3617e-4`).  With the converged values,
`Tr(B^*B)/(2E) = 6.7182e-4/6.7234e-4 = 0.99923` (X = 100, |k| <= 60): the c-linearity holds to 0.08%.
