# O7(a): lattice test of the two-branch rotated-Petz law

`petz_lattice.py` — complex free-fermion hopping chain at half filling (infinite chain,
`C_ij = sin(pi(i-j)/2)/(pi(i-j))`, exact), three adjacent blocks `A,B,C` with
`L_A = L_C = L`, `L_B = b`, `eta_V = L_A L_C/[(L_A+L_B)(L_B+L_C)]`.

## What it computes
The rotated ("twirled") Petz map of Vardhan–Wei–Zou, arXiv:2307.14434, Sec. 2.2,
`P^(l)_{B->BC}(x) = rho_BC^{1/2-il/2} rho_B^{-1/2+il/2} x rho_B^{-1/2-il/2} rho_BC^{1/2+il/2}`,
`rho~_ABC = (id_A ⊗ P^(l))(rho_AB ⊗ 1_C)` (their eq. for `rho~_ABC`, p. 8; correlation-matrix
route sketched in their App. A.5, Majorana form),
and then `-log F(rho_ABC, rho~_ABC)` and `D(rho_ABC || rho~_ABC)`.

**Gaussian implementation.** Every factor is a number-conserving fermionic Gaussian operator
`K exp(sum c_i^dag X_ij c_j)`; with `T = e^X` the composition rule is `T_1 T_2` (Klich),
`Tr = K det(1+T)` and `C = T(1+T)^{-1}`, i.e. `T = G = C/(1-C)`. Hence, with `a=(1-il)/2`,

    T~ = [1_A ⊕ T_BC^a][1_AC ⊕ T_B^{-a}][T_AB ⊕ 1_C][1_AC ⊕ T_B^{-abar}][1_A ⊕ T_BC^abar],

which is Hermitian positive definite, `G~ = T~`, `Q~ = T~(1+T~)^{-1}`. Fidelity and relative
entropy from Note 5, Thm 3.2 (finite-dimensional quasi-free determinant representation).

**Precision.** All linear algebra in `python-flint` (`acb_mat`, ball arithmetic) at
`3 kappa_max/log 2 + 250` bits, `kappa_max ≈ 1.8 n` (measured). This is the eigenvalue-floor
problem that limited VWZ to `L_A, L_B <= 8`; here `n = L_A+L_B+L_C <= 72`.

## Validation
`python petz_lattice.py validate` compares the Gaussian pipeline with the exact `2^n`
many-body density matrices (Jordan–Wigner, `scipy`, `n = 8, 9, 10`) at
`lambda = 0, 0.5, 1, 1.5`: relative entropies agree to 1e-15, `-log F` to the accuracy of
`scipy.linalg.sqrtm` (~1e-8 absolute). Independently, the exact normalisation identity
`K det(1+T~) = 1` holds to the working precision (~1e-100 .. 1e-250) at every point,
and the whole flint pipeline reproduces an independent `mpmath` implementation
(`recovered_G`/`fid_relent`) to all digits.

## Usage
    python petz_lattice.py validate            # Gaussian vs exact 2^n
    python petz_lattice.py sweep > sweep.raw   # ~100 geometries x 4 lambda
    python petz_lattice.py report > petz_lattice.out
    python petz_lattice.py plot                # collapse.png

## Files
* `petz_lattice.py` — everything (model, Gaussian Petz map, exact check, sweep, analysis, plot)
* `sweep.raw` — one line per (geometry, lambda)
* `petz_lattice.out` — the tables
* `collapse.png` — log–log collapse plot

---

# S9 (O9+O10): thermal states, massive RG flow, gap geometries

`petz_thermal_rg.py` — same Gaussian rotated-Petz pipeline as `petz_lattice.py`
(it imports it), but for three new families of Gaussian reference states.  All
correlation matrices are built as periodic integrals evaluated with the
trapezoidal rule in `arb` ball arithmetic; the integrands are analytic in a
strip of half width `a`, so the `N`-point rule converges like `e^{-aN}` and `N`
is chosen from the requested number of bits (`a = pi/(2 beta)` thermal,
`a = 2 asinh(m/2)` massive).

**Continuum dictionary (used everywhere).**  `eps_k = -2 cos k` gives the Fermi
velocity `v = |d eps/dk|_{k=pi/2} = 2` sites per unit lattice time.  Hence a
lattice inverse temperature `beta` is the continuum `beta_len = v beta = 2 beta`
and the thermal correlation length is `xi = beta_len/(2 pi) = beta/pi` **sites**;
a staggered mass `m` (gap `2m`) is the continuum Dirac mass `mu = m/v = m/2`,
i.e. `xi = 2/m` sites, and the RG variable is `mu R = m R/2`.

## Validation (`python petz_thermal_rg.py validate`)
Every new ingredient against exact `2^n` many-body density matrices, `n <= 10`:
thermal (`beta = 2, 6`), massive (`m = 0.4, 1.0`, both site parities), gap
(`L_G = 2, 3`, vacuum and thermal), `lambda = 0, 0.5, 1`.  Relative entropies
agree to `1e-13`, `-log F` to `3e-8` (the accuracy of `scipy.linalg.sqrtm`),
`S(ABC)` to `3e-14`, the CMI from four Gaussian entropies to `7e-15`, and the
exact normalisation `K det(1+T~) = 1` holds to `1e-95 .. 1e-250` at every point.
The thermal kernel was additionally checked against `mpmath.quad` (18 digits).

## (1) Thermal, `python petz_thermal_rg.py thermal`
`L_A = L_C = L in {8,12,16}`, `L_B = b <= 40`, `beta in {4,8,16,32}` and the
vacuum, `n = 2L+b <= 72`, `lambda = 0, 1/2, 1`.
* **Shielding.**  `-log F^(0) = A e^{-kappa_F L_B/beta}` and
  `I(A:C|B) = A' e^{-kappa_I L_B/beta}` with `kappa_I -> pi` and
  `kappa_F -> 2 pi` (independent of `L`): `kappa_F = 5.863 (beta=4),
  6.237 (beta=8), 6.293 (beta=16)` vs `2 pi = 6.28319`, and
  `kappa_I = 3.129, 3.159, 3.150` vs `pi = 3.14159`.  `2 pi` is
  `2 x (2 pi/v) = 2/xi` in sites: the CMI decays on the thermal correlation
  length `xi = beta/pi`, and `-log F` on half of it because it is quadratic in
  the cross ratio.  At `beta = 4` (`xi = 1.27` sites) the lattice correction is
  already 7%.
* **Two-branch law survives.**  With the thermal cross ratio
  `eta_th = sinh(pi a/bl) sinh(pi c/bl)/[sinh(pi(a+b)/bl) sinh(pi(b+c)/bl)]`,
  `bl = 2 beta` (this is the vacuum cross ratio of the exponential map, and
  `I = (1/3) log 1/(1-eta_th)` exactly), the vacuum law
  `-log F = Phi(z(1+e^{-pi lam})) + Phi(z(1+e^{pi lam}))`, `z = eta/(1-eta)`,
  reproduces the thermal data to 2% over five decades at `beta = 16`.
* **First thermal correction.**  Expanding Note 3 eq. (thermal-cmi) gives
  `I_beta - I_vac = -pi^2 L_A L_C/(9 beta_len^2) = -pi^2 L_A L_C/(36 beta^2)`,
  independent of `L_B`; measured ratio to this prediction 0.300, 0.608, 0.855,
  0.958 at `beta = 4, 8, 16, 32` (`L = 8`, `b = 1`), i.e. `1 - O(beta^-2)`.

## (2) Massive / RG, `python petz_thermal_rg.py mass` (and `masspetz`)
Staggered potential `(-1)^i m c_i^dag c_i`.  Only even interval lengths are
commensurate with the two-site cell and entropies depend on the parity of the
first site, so both parities are averaged and all differences use even steps.
`c_M := c_M^(2)(R) = 3R^2 I_{R-2}(2)/4` (a genuine lattice CMI, `>= 0` by SSA);
at a fixed point `c_M^(d) = -(3R^2/d^2) log(1-d^2/R^2) = c(1+d^2/2R^2+...)`, so
this carries a known `+2/R^2` bias; `c_E(R) = 3R (S(R+2)-S(R-2))/4`.
* Normalisation at `m = 0`, `R = 40`: `c_E = 1.00090`, `c_M = 1.00144` (`= c = 1`).
* Both are **monotone decreasing** in `R` for every `m > 0` in the collapse
  window, and `c_M >= c_E` everywhere (the entropic c-theorem inequality of
  Note 3).  The 2-3% overshoot `c_M > 1` visible at `R = 6, 8` does **not**
  collapse between `m = 0.05` and `m = 0.1` at fixed `mu R` and is a lattice
  (finite `delta/R`) artefact; for `mu R >= 0.4` the two masses agree to 1%.
* `c_M/c_E -> m R = 2 mu R` in the IR (measured `(c_M/c_E)/(mR) = 1.02` at
  `m = 0.4, R = 16`), the free-field prediction from `S-S(inf) ~ e^{-2 mu R}`.
* At fixed geometry the vacuum two-branch law **fails** along the flow: the
  ratio `-log F^(0)/2Phi(2z(I))` grows without bound, because `-log F^(0)`
  becomes *linear* in the CMI, `-log F^(0)/I = 0.10 .. 0.17` for `mu L_B >= 1.6`
  (vs `0.02 .. 0.05` at `m = 0`).
* Near-product states need head-room: `bits = bits_for(n) + 300 m`.

## (3) Gap, `python petz_thermal_rg.py gap`
`A(L) | G(L_G) | B(L) | C(L)`, `G` traced out, Petz channel on `B`,
`L in {6,8,12}`, `L_G <= 96`.
* For the massless Dirac field the two-interval entropies give exactly
  `I(A:C|B) = (1/3) log[(a+g+b)(g+b+c)/((g+b)(a+g+b+c))]`: the adjacent law with
  `L_B -> L_B + L_G` (`log L_G` terms cancel).  Confirmed: `I/I_cont = 1.0006`
  at `L_G = 96, L = 12`.  Hence `I ~ (1/3) L_A L_C/L_G^2`.
* `-log F^(0)` decays with the **same** power `L_G^-2` (local exponents 1.49 vs
  1.40 at `L_G = 64`, both approaching 2), so `-log F^(0)/I` tends to an
  `L`-independent constant `kappa_g ~ 0.09` (0.0907, 0.0898, 0.0883 at
  `L_G = 96` for `L = 6, 8, 12`; `1/L_G` extrapolation gives `0.093`).  The
  two-branch law fails by a factor `~ 1/eta` (44 at `L_G = 96`).

## Files
* `petz_thermal_rg.py` — model kernels, generic Gaussian Petz runner, exact
  `2^n` validation, the three scans, reports, plots
* `petz_thermal_rg.out` — validation + all tables; `thermal.raw`, `cfun.raw`,
  `masspetz.raw`, `gap.raw` — one line per data point; `*.log` — run logs
* `thermal_shield.png`, `cfun_flow.png`, `gap_decay.png`
