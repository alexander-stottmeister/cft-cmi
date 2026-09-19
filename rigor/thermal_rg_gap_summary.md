# S9 (O9 + O10): thermal states, massive RG flow, gap geometries on the lattice

Numerics: `numerics/lattice/petz_thermal_rg.py`, output `petz_thermal_rg.out`,
raw data `thermal.raw`, `cfun.raw`, `masspetz.raw`, `gap.raw`, figures
`thermal_shield.png`, `cfun_flow.png`, `gap_decay.png`, method section appended
to `numerics/lattice/README.md`.  The Gaussian rotated-Petz pipeline of agent PL
(`petz_lattice.py`) is reused unchanged; only the reference state is new.

## 0. Conventions and validation

Complex free fermions on the chain `H = -sum (c_i^dag c_{i+1} + h.c.)` at half
filling; `eps_k = -2 cos k`, so the Fermi velocity is `v = 2` **sites per unit
lattice time**.  This conversion is the whole content of the "expected `2 pi`":
a lattice inverse temperature `beta` is the continuum `beta_len = v beta = 2 beta`,
the Dirac thermal correlation length `xi = beta_len/(2 pi)` is `beta/pi` sites,
and a staggered mass `m` (single-particle gap `2m`) is the continuum Dirac mass
`mu = m/v = m/2`, i.e. `xi = 2/m` sites.

Every new ingredient (thermal, massive with both site parities, gap geometry,
and the four-entropy CMI) was checked against exact `2^n` many-body density
matrices for `n <= 10` and `lambda = 0, 1/2, 1`: relative entropies to `1e-13`,
`-log F` to `3e-8` (`scipy.linalg.sqrtm`), entropies to `3e-14`, CMI to `7e-15`,
with the exact normalisation `K det(1+T~) = 1` holding to `1e-95..1e-250`.

## 1. Thermal: exponential shielding at rate 2 pi

With `L_A = L_C = L in {8,12,16}`, `L_B = b <= 40`, `beta in {4,8,16,32}`:

| beta | kappa_F (fit to `A e^{-kappa L_B/beta}`) | kappa_I |
|---|---|---|
| 4  | 5.863 | 3.129 |
| 8  | 6.237 | 3.159 |
| 16 | 6.293 | 3.150 |

against `kappa_I = pi = 3.14159` (the CMI decays on `xi = beta/pi` sites) and
`kappa_F = 2 pi = 6.28319` (`-log F` is quadratic in the cross ratio, hence
decays on `xi/2`).  Both are `L`-independent to four digits.  At `beta = 4`,
`xi = 1.27` sites and the lattice correction to `kappa_F` is already 7%.

Two further results, both new relative to Note 3:

* **The two-branch law survives finite temperature.**  Note 3 eq.
  (thermal-cmi) is equivalent to `I = (1/3) log 1/(1-eta_th)` with the thermal
  cross ratio `eta_th = sinh(pi a/bl) sinh(pi c/bl)/[sinh(pi(a+b)/bl)
  sinh(pi(b+c)/bl)]`, `bl = 2 beta` — the vacuum cross ratio of the images of
  the four endpoints under the exponential map.  Feeding this `eta_th` into the
  vacuum two-branch law of O7(a) reproduces the measured `-log F^(lambda)` to
  2% over five decades at `beta = 16`.  The KMS state therefore obeys the same
  recovery law as the vacuum with the conformally transported cross ratio;
  this is a sharp target for the operator-algebraic program of Note 3 Sec.
  "Thermal and KMS states".
* **First thermal correction.**  Expanding (thermal-cmi) gives
  `I_beta - I_vac = -pi^2 L_A L_C/(9 beta_len^2) = -pi^2 L_A L_C/(36 beta^2)`,
  quadratic in `1/beta` and *independent of `L_B`*.  Measured/predicted =
  0.300, 0.608, 0.855, 0.958 at `beta = 4, 8, 16, 32` (`L = 8`, `L_B = 1`),
  consistent with `1 - O(beta^-2)`; at fixed `beta = 32` the correction varies
  by only 3% between `L_B = 1` and `L_B = 4`, as predicted.

## 2. Massive flow: c_M vs c_E

Staggered mass; only even lengths are commensurate with the two-site cell and
entropies depend on the parity of the first site, so both parities are averaged
and all finite differences use even steps.  Primary definitions
`c_M(R) := 3R^2 I_{R-2}(2)/4` (a genuine lattice CMI, non-negative by SSA, with
the *known* fixed-point bias `c_M^(d) = c(1 + d^2/2R^2 + ...)`) and
`c_E(R) := 3R (S(R+2)-S(R-2))/4`.

* Normalisation: at `m = 0`, `R = 40`, `c_E = 1.00090` and `c_M = 1.00144`, both
  equal to `c = 1` up to the quoted `O(R^-2)` lattice bias.
* Along the flow `mu R: 0 -> inf` both fall monotonically from 1 to 0
  (`dc_E/dR < 0` and `dc_M/dR < 0` at every point of the collapse window), and
  `c_M >= c_E` everywhere, as the entropic c-theorem requires.
* `c_M/c_E -> 2 mu R = m R` in the IR: `(c_M/c_E)/(mR) = 1.196, 1.078, 1.020` at
  `R = 6, 10, 16` for `m = 0.4`.  This is the free-field prediction from
  `S(R) - S(inf) ~ A e^{-2 mu R}` and it means `c_M` is *not* an independent IR
  quantity: it is `c_E` times the RG time.
* **Regularisation caveat.**  A 2-3% overshoot `c_M > 1` appears at `R = 6, 8`;
  it does not collapse between `m = 0.05` and `m = 0.1` at fixed `mu R`
  (1.0286 vs 0.9835 at `mu R = 0.3`) and is therefore a lattice artefact of the
  smallest admissible `delta = 2`, not evidence against monotonicity.  For
  `mu R >= 0.4` the two masses agree to 1%.  Also lattice-specific: the
  even/odd length asymmetry of the staggered chain (the `delta = 1` CMI differs
  from the `delta = 2` one by a factor of two at `m = 0.4`), and the failure of
  the naive Richardson extrapolation in `delta` once `mu delta >~ 1`, where
  `I_{R-delta}(delta)` is exponential rather than polynomial in `delta`.

## 3. Recovery is only quadratic in the CMI at a conformal fixed point

The most consequential finding is negative, and it appears twice:

* **Massive flow, fixed geometry.**  `-log F^(0)/I(A:C|B)` rises from
  `0.02..0.05` at `m = 0` to `0.10..0.17` for `mu L_B >= 1.6` and stays there
  down to `I ~ 1e-19`; i.e. `-log F` becomes *linear* in the CMI and the vacuum
  two-branch law overestimates the fidelity by a factor that diverges like
  `1/eta`.
* **Gap geometry** `A(L) | G(L_G) | B(L) | C(L)` with `G` traced out.  For the
  massless Dirac field the two-interval entropies give exactly
  `I(A:C|B) = (1/3) log[(a+g+b)(g+b+c)/((g+b)(a+g+b+c))]`, i.e. the adjacent
  law with `L_B -> L_B + L_G` (all `log L_G` terms cancel), confirmed to 0.06%
  at `L_G = 96`; so `I ~ (1/3) L_A L_C/L_G^2`.  `-log F^(0)` decays with the
  *same* power `L_G^-2`, not `L_G^-4`, and `-log F^(0)/I` tends to an
  `L`-independent constant `kappa_g ~ 0.09` (0.0907, 0.0898, 0.0883 at
  `L_G = 96` for `L = 6, 8, 12`; extrapolated 0.093).

So the `eta^2` law of O7(a) is a fixed-point statement about *adjacent*
intervals: it survives a conformal change of state (thermal) but not a
relevant deformation (mass) and not a change of geometry (gap).  In both broken
cases the rotated Petz map saturates a *linear* fraction of the CMI.  Any
attempt to prove an `eta^2`-type recovery bound in general chiral CFT must
therefore use adjacency and conformal invariance, not just the CMI.
