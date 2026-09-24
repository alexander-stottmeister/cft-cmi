# F2 (Phase 5, track F2 — numerics): non-isometric directions in the tangent problem

Question: do non-isometric quasi-free recoveries (loss of isometry `N1 >= 0`, noise
`0 <= Y1 <= N1`) lower the second-order recovery error below the isometric-orbit value
`(1 - theta) g_Q(delta_c)` in the S10 spectral circle model, and what does the KKT sign
criterion (F1 Thm 4.4) say?

All of T1/T2 is done in the fixed-geometry **first-order (tangent)** problem, which the
circle model resolves exactly.  Scripts (all in `numerics/optimality_all/`, prefix `f2_`):

| file | what |
|---|---|
| `f2_model.py` | circle-model builder + conventions (S10-identical), `g_Q`, SLD, `rot`, `noise`, `theta_cg` |
| `f2_kkt_check.py` | T2 in the brief's normalisation (SLD of `kkt_continuum.gQ_sld`) |
| `f2_kkt_f1.py` | T2 in **F1 Thm 4.4** normalisation — the table below |
| `f2_tangent_sdp.py` | T1, direct cvxpy form (works, slow) |
| `f2_tangent_gram.py` | T1, Gram-reduced form (fast, but the Gram squares a 1e19 condition number — see caveat) |
| `f2_gain.py` | the exact gain functional; unconstrained relaxation (shown to be ill-posed) |
| `f2_cone_fast.py` | T1 in scale-free cone form, residual map precomputed exactly |
| `f2_sub_gain.py` | T1 restricted to k-dim noise subspaces, rotation eliminated exactly (lower bounds on the gain) |
| `f2_galerkin_full.py` | T3, full primal SDP over F in the modular Galerkin frame |
| `f2_capscan.py` | T2 weight-cap / UV-taper stability scan |
| `f2_gram_verify.py` | demonstration that the Gram rank cutoff fakes a 5% gain |
| **`f2_t4_wh.py`** | **T4 (the test of (a)): condition (a) in F3's parameter-free modular Wiener-Hopf frame** |
| **`f2_t5_endpoint.py`** | **T5 (the test of (e)): the endpoint condition (e) in the same frame** |
| `f2_gram_cond.py` (one-liner, see T1) | measured Gram condition numbers -> `f2_gram_cond.out` |

Environment: `V=/private/tmp/.../scratchpad/venv`; `$V/bin/python f2_*.py ...`.

## 0. Conventions (reproduced before anything else)

`f2_model.build` is `s10_theta.setup` verbatim: NS circle, `L` sites, `P = 1_{nu>0}`,
smoothstep UV taper `uv=(0.30,0.42)`, `alpha=3`, `a=2`, `Lg=1`, weight cap `1e10`
(`w = min(1/den, cap)`), `I = D u A` with **D first** in the index order.
`g_Q(delta) = (1/4) sum w_ik |delta~_ik|^2` (`optimality_second_order.tex` l.333).

First-order defect (`delta = Q - Q_rec`, in units of `s`), signs fixed by
`V = (1 - sG) e^{s D_chi}`, `X X* = 1 - s N1`, `Z = V Q_BB V* - (s/2){N1, V Q_BB V*} + s Y1`:

    delta_c   = E_I [P, D_chi] E_I                 (compression; this is S10's "u" as a defect)
    delta_rot = E_I [G, P] E_I = [G, Q]            (G = iH anti-Herm., supported on D)
    noise_DD  = (1/2){N1, Q_DD} - Y1 ,  noise_DA = (1/2) N1 Q_DA ,  noise_AA = 0.

Checks that fix the conventions (`$V/bin/python f2_tangent_sdp.py 64`):

* `theta` by CG: **0.28958 at L=256** vs S10's published 0.2895
  (`sdp_dual_certificate.tex` Sec. 7(c)); 0.29118 (L=128), 0.30121 (L=96), 0.35095 (L=64).
* orbit-only SDP (`N1 = Y1 = 0` forced) reproduces `(1-theta) g_Q(delta_c)` to
  **1.1e-07 relative** at L=64 — so the SDP path and the CG path agree.
* SLD identity: with F1's normalisation `t_* = U (w o delta~_*) U^H` one has
  `g_Q(delta_*) = (1/4) Tr(t_* delta_*)` to **1e-10**; this `t_*` is exactly **twice**
  the SLD of `kkt_continuum.gQ_sld` (and of the brief's S10 (C4) convention).  All the
  criterion quantities are homogeneous of degree 1 in `t_*`, so the verdict is unaffected.
* Derivative formula (F1): `d/ds g_Q(delta_* + s A(0,N1,Y1)) = (1/2)[Tr(N1 M_*) - Tr(Y1 tau_*)]`
  verified by central finite differences along random Hermitian `N1, Y1`: relative error
  **1e-9 ... 1e-8** at every L (`f2_kkt_check.py`, "FD check" lines).
* Stationarity along rotations, `AntiHerm((t_* Q)_DD) = 0` (F1 Prop 4.3):
  `||AntiHerm((t_*Q)_DD)|| / ||M_*|| = 3.3e-08, 3.8e-07, 9.0e-07, 2.2e-06, 2.5e-07`
  at L = 64, 96, 128, 192, 256.
* Homogeneity `delta_c -> 2 delta_c` scales the tangent optimum by 4 (see T1).

### Convention discrepancy found (reported to F1)

The circle model does **not** have `delta_c` purely A-D off-diagonal: Moebius rigidity
(`delta_c,DD = 0`, `delta_c,AA = 0`, exact in the continuum and exact in the Galerkin frame,
where `|dc_DD|/|dc| = 0.0e+00`) is violated at **O(1/L)** on the lattice, because the tapered
spectral derivative `d` in `D_chi = (1/2)(chi d + d chi)` is not local:

| L | 64 | 96 | 128 | 192 | 256 |
|---|---|---|---|---|---|
| `|dc_DD|/|dc|` | 0.3455 | 0.2138 | 0.1528 | 0.1009 | 0.0747 |
| `|dc_AA|/|dc|` | 0.0484 | 0.0324 | 0.0238 | 0.0162 | 0.0121 |

Both decay like `1/L` (rigidity is restored in the continuum limit), but they are the
dominant source of uncertainty in everything below, because `g_Q` weights those blocks with
`w` up to the cap: taken separately the blocks of `delta_c` have `g_Q` of order
`1e5 x g_Q(delta_c)` (L=256: DD 4.3e4, AA 4.2e4, DA 9.6e4 in units of `g_Q(delta_c)`), i.e.
`g_Q(delta_c)` is a cancellation of five orders of magnitude.

## T2. The KKT criterion (F1 Thm 4.4) — **it FAILS at every L**

`$V/bin/python f2_kkt_f1.py 64,96,128,192,256 1e10` -> `f2_kkt_f1_L.out`
(brief-normalisation version: `f2_kkt_check.py 64,96,128,192,256` -> `f2_kkt.out`).

Objects (F1 normalisation, `t_* = U (w o delta~_*) U^H`):
`tau_* = E_D t_* E_D`, `M_* = Herm((t_* Q)_DD) = Herm(t_DD Q_DD) + Herm(t_DA Q_AD)`.
Criterion: orbit = global optimum of the tangent problem **iff** `M_* >= 0` and `M_* - tau_* >= 0` (condition (a)) **and** the endpoint condition (e) of T5 (F1 Thm 4.4 as amended: (a) alone is necessary, not sufficient; see Correction C6).

| L | nD | theta | `lam_min(M_*)` | `/g_Q(dc)` | `/||M_*||` | `lam_min(M_*-tau_*)` | `/g_Q(dc)` | verdict |
|---|---|---|---|---|---|---|---|---|
| 64 | 15 | 0.350955 | -3.1079e-01 | -83.90 | -0.2057 | -3.1079e-01 | -83.91 | FAIL |
| 96 | 23 | 0.301210 | -7.6969e-03 | -2.167 | -0.00754 | -7.7030e-03 | -2.169 | FAIL |
| 128 | 31 | 0.291179 | -3.4771e-02 | -9.450 | -0.03519 | -3.4762e-02 | -9.448 | FAIL |
| 192 | 47 | 0.288861 | -6.3068e-02 | -17.35 | -0.05788 | -6.3060e-02 | -17.34 | FAIL |
| 256 | 63 | 0.289582 | -5.8636e-02 | -15.88 | -0.04983 | -5.8637e-02 | -15.88 | FAIL |

`lam_max(M_*) = 1.511, 1.021, 0.988, 1.090, 1.177` and `lam_max(tau_*) = -lam_min(tau_*)`
= 1.510, 1.019, 0.985, 1.086, 1.173 at the same L: `M_*` and `tau_*` have nearly equal
spectra, and `M_* - tau_*` is nearly zero on the violating directions (the two criteria
fail on *different* eigenvectors with the same localisation and opposite `<p,tau_* p>`: the `M_*` minimiser has `<p,M_* p> ~ +<p,tau_* p>`, e.g. -0.3108 and -0.3097 at L=64, and the `M_* - tau_*` minimiser has `<p,tau_* p> = +0.3097` and `<p,M_* p> ~ 0`, `f2_kkt_f1_L.out` l.5-6; see Correction C1).

**The verdict is stable in L (it always fails) but the SIZE of the violation is not**: it is
a pure ultraviolet effect.  Weight-cap and UV-taper scan at L=128, **all numbers in F1's
normalisation** (`t_* = U (w o delta~_*) U^H`; the half-SLD convention of
`kkt_continuum.gQ_sld` halves `lam_min` and quarters the gain), from
`f2_capscan_L128.out` (`$V/bin/python f2_capscan.py 128 1e4,1e6,1e8,1e10,1e12 0.30,0.20`):

| cap | 1e4 | 1e6 | 1e8 | 1e10 | 1e12 |
|---|---|---|---|---|---|
| theta (`uv=0.30`) | 0.29117 | 0.29119 | 0.29116 | 0.29118 | 0.29119 |
| `lam_min(M_*)` | -3.211e-03 | -3.134e-03 | -7.887e-03 | -3.477e-02 | -1.050e-01 |
| `lam_min/||M_*||` | -0.01220 | -0.00672 | -0.01048 | -0.03519 | -0.07529 |
| `g_Q(noise(pp*,0))/g_Q(dc)` | 1.305e+03 | 9.315e+04 | 6.671e+09 | 6.319e+11 | 5.475e+13 |
| rank-1 gain `/g_Q(dc)` | 1.463e-04 | 1.948e-06 | 1.722e-10 | 3.534e-11 | 3.718e-12 |
| same rows, taper `uv=0.20`: `lam_min/||M_*||` | -0.01253 | -0.00701 | -0.00880 | -0.02582 | -0.02869 |
| ... gain `/g_Q(dc)` | 5.808e-04 | 8.072e-06 | 1.458e-10 | 2.274e-11 | 6.444e-13 |

i.e. as the ultraviolet is resolved (cap up), the violation of the criterion grows but the
*curvature* of the violating direction grows much faster, so the achievable gain collapses.
theta itself is cap-stable to 4 digits at both tapers (0.29116-0.29119 and 0.26146-0.26150; see Correction C4),
while the taper shifts theta by 10%: the criterion verdict (FAIL) is taper-independent, its
size is not.

**Violating direction and its gain** (F1 Cor 4.5; `p` = eigenvector of `lam_min`,
`y = 1` if `<p,tau_* p> > 0` else `0`, `Delta = -(1/2)[<p,M_*p> - y<p,tau_*p>]`,
`gain = Delta^2/g_Q(eta)`, `gain_red = Delta^2/g_red(eta)` with the rotation re-optimised):

| L | `Delta` | `g_Q(eta)` | `g_red(eta)` | `gain/g_Q(dc)` | `gain_red/g_Q(dc)` | where `p` lives (top-3 `|p|`, fraction of D) |
|---|---|---|---|---|---|---|
| 64 | 1.554e-01 | 1.033e+09 | 1.033e+09 | 6.31e-09 | 6.31e-09 | 0.07, 0.00, 0.13 |
| 96 | 3.848e-03 | 2.318e+09 | 2.317e+09 | 1.80e-12 | 1.80e-12 | 0.65, 0.70, 0.61 |
| 128 | 1.739e-02 | 2.325e+09 | 2.324e+09 | 3.53e-11 | 3.53e-11 | 0.77, 0.81, 0.74 |
| 192 | 3.153e-02 | 2.214e+09 | 2.213e+09 | 1.24e-10 | 1.24e-10 | 0.87, 0.89, 0.85 |
| 256 | 2.932e-02 | 2.134e+09 | 2.134e+09 | 1.09e-10 | 1.09e-10 | 0.89, 0.91, 0.91 (from M-tau) |

Note `g_red ~ g_Q` to 5e-4: the isometric rotations cannot absorb these directions at all.
Both choices of `p` (from `M_*` and from `M_* - tau_*`) give the same gain to 3 digits.

### T2 is ARTEFACT-SUSPECT — do not use it to decide Q1

Two independent signatures say the T2 violation is not physical: (i) it is not cap-stable
(it *grows* with the cap while `theta` does not), and the achievable gain *collapses* as the
cap grows; (ii) the circle model violates Moebius rigidity at O(1/L) and `g_Q` weights the
spurious `DD`/`AA` blocks of `delta_c` by `w` up to the cap, so `t_*` — and hence `M_*`,
`tau_*` — is contaminated exactly where the weights are largest.  T4 below repeats the test
in a frame where rigidity is exact; that is the frame to believe.

## T1. The tangent SDP in the circle model — orbit-only solid, full optimum not resolvable

`f2_tangent_sdp.py` (direct), `f2_tangent_gram.py` (Gram), `f2_cone_fast.py` (scale-free
cone form), `f2_sub_gain.py` (k-dim noise subspaces, rotation eliminated by CG).

What is solid:

* **orbit-only** optimum (`N1 = Y1 = 0` forced) reproduces `(1-theta) g_Q(delta_c)` to
  **1.1e-07 relative** (L=64, cap 1e10) and **4.0e-07** (L=64, cap 1e6) — not "exactly";
  this validates the SDP formulation against the S10 CG, and it is a statement about the
  **orbit-only** problem, not about the full tangent optimum;
* **homogeneity**: `delta_c -> 2 delta_c` scales the orbit-only optimum by exactly
  4.00000000 in both the direct and the Gram form (L=64, cap 1e6);
* **rank-one gains** along the KKT-violating directions (exact, solver-free, T2 table):
  `1e-12 ... 6e-9` of `g_Q(delta_c)` at L = 64..256, cap 1e10;
* **subspace lower bounds** (`f2_sub_gain_fixed.out`, after the bug fix below), which are
  valid lower bounds on the gain because the returned `(N1,Y1)` is checked for cone
  feasibility and `l` and `g_red` are recomputed exactly outside the solver:

| L | subspace | solver status | cone feasibility `min eig/||N1||` | `l` | `g_red` | gain `/g_Q(dc)` | `kappa_full <=` |
|---|---|---|---|---|---|---|---|
| 64 | `eigM` k=4 | infeasible_inaccurate | — | — | — | (no point) | — |
| 64 | `eigMtau` k=4 | optimal | -2.4e-12 | -1.0000 | 2.3742e+08 | 2.843e-07 | 0.64904512 |
| 64 | `svdQDA` k=4 | optimal_inaccurate | -4.4e-14 | -1.0000 | 7.3331e+09 | 9.204e-09 | 0.64904540 |
| 64 | `mix` k=8 | optimal_inaccurate | **-3.4e-17** | -1.0000 | 3.2049e+05 | **2.106e-04** | **0.64883481** |
| 64 | `rand` k=4 | infeasible_inaccurate | — | — | — | (no point) | — |
| 128 | `eigM` k=4 | infeasible_inaccurate | — | — | — | (no point) | — |
| 128 | `eigMtau` k=4 | optimal_inaccurate | -7.8e-16 | -1.0000 | 1.2164e+11 | 5.586e-10 | 0.70882131 |
| 128 | `svdQDA` k=4 | infeasible | — | — | — | (no point) | — |
| 128 | `mix` k=8 | infeasible_inaccurate (SCS) | — | — | — | (no point) | — |
| 128 | `rand` k=4 | infeasible | — | — | — | (no point) | — |

(`1-theta = 0.64904541` at L=64 and `0.70882131` at L=128.)

**Correction to an earlier reading of this run.**  The first version of `f2_sub_gain.py`
crashed with `ValueError: matmul: Input operand 1 does not have enough dimensions` whenever
the solver returned no point (`Nr.value is None`), and that crash was misreported here as
"every subspace solve failed" / a conditioning failure.  It was a plain code defect (an
unguarded `basis @ Nr.value`).  Fixed: the status is now caught, SCS is tried as a fallback,
and the cone feasibility of the returned point is measured.  The corrected picture is the
table above: most subspaces return a point; the genuine failures are reported as
`infeasible(_inaccurate)` statuses, not as crashes.

**On the k=8 number.**  The solver returned it as `optimal_inaccurate` with its own objective
`q* = 6.970e+05`, which differs from the exactly recomputed `g_red = 3.205e+05` by 2.17x —
the returned point is *better* than the solver thought.  What is quoted above does not use
the solver's objective at all: the point is cone-feasible to `-3.4e-17` (machine precision),
`l` is recomputed as `-1.0000` and `g_red` by an independent CG, so
`gain = l^2/(4 g_red) = 2.106e-04 g_Q(delta_c)` is a valid lower bound (a non-converged CG
would only make `g_red` larger, i.e. the bound weaker).

What is NOT resolved: the **full** tangent optimum `kappa_full` in the circle model.  The
quadratic form of the tangent problem is numerically singular there — measured Gram
condition numbers (`f2_gram_cond.out`): `2.50e+18` (L=64, cap 1e4), `2.65e+19` (L=64, cap
1e6), `2.37e+22` (L=64, cap 1e10), `2.51e+26` (L=96, cap 1e10), with the smallest positive
eigenvalue at the double-precision floor.  This is a direct consequence of the rigidity
violation (the blocks of `delta_c` carry `g_Q` of order `1e5 x g_Q(delta_c)`).  Consequences:

* CLARABEL fails (`SolverError`) on the direct form at L=64 for caps 1e4 and 1e10, and on the
  scale-free cone form for all caps; SCS does not converge in 1e5 iterations;
* the Gram-reduced form appears to succeed but its answer is a rank-cutoff artefact: with the
  default cutoff it drops 161/675 directions and reports `kappa_full = 0.5990` against
  `1-theta = 0.6490` at L=64 (0.59897 at cap 1e6) — a spurious 5% gain from treating
  small-curvature directions as free;
* the *unconstrained* relaxation (arbitrary Hermitian `N1, Y1`) is genuinely ill-posed: CG on
  `Ghat x = l` does not converge and the gain estimate grows with the iteration count
  (`f2_gain.py`: 8.7e-4 -> 6.8e-3 of `g0` between iterations 75 and 200 at L=64).  The cone
  constraints are essential; the correct scale-free formulation is
  `q* = min{ g_Q([G,Q]+noise(v)) : l(v) = -1, v in cone }`, `gain = 1/(4q*)`.

So this section reports bounds, not a value: `kappa_full <= 1 - theta - 2.1e-04` at L=64 and
`<= 1 - theta - 5.6e-10` at L=128, in a frame whose criterion verdict T4 shows to be
artefact-dominated.  No claim about `kappa_opt` is made here; that is T4/T5's business.

## T3. Full primal SDP over F in the modular Galerkin frame — not usable for Q1

`$V/bin/python f2_galerkin_full.py 0.4,0.3` -> `f2_galerkin_a.out` (h=0.4: 9425 s;
h=0.3: 24923 s).  At `a=1, L=2, Lambda=12, s=0.1, kind='first'`:

| h | N | (nA,nB,nC) | `g_Q(delta_c)/(f2 z^2)` | theta | `1-theta` | `min_F g_Q` | `min_F/g_Q(delta_c)` | `tr(1-XX*)` | `sv(X)` |
|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 69 | (30,9,30) | 0.8687 | 0.28578 | 0.71422 | 6.8546e-05 | **8.411034** | 35.16 of m=39 | [0.0061, 0.9999] |
| 0.3 | 91 | (40,11,40) | 0.8956 | 0.29926 | 0.70074 | 5.9870e-05 | **7.125692** | 46.71 of m=51 | [0.0002, 0.9999] |

Both rungs are a factor **7-8 ABOVE** the compression defect, not below the orbit value, and
the optimal `X` is a strong contraction (`||1-XX*||_F = 5.872` and `6.780`), nothing like a
co-isometry.  **Caveat on what is being compared** (referee's point, adopted): `min_F g_Q` is
an exact finite-`s` minimum over the discretised `F`, whereas `theta`/`1-theta` and
`g_Q(delta_c)` on the same rung are *first-order* (tangent) reference numbers computed by
`orbit_theta()`; the two are not values of one and the same programme, so the ratio must not
be read as "the orbit beaten/not beaten by that factor".

What the rungs do show is the S11 representability obstruction
(`rigor/sdp_certificate_numerics.tex` l.484-497): in a finite Galerkin cell frame the Moebius
compression is not representable (its `V` maps cells to non-cells), so the discretised `F`
does not contain the compression point at all.  The two rungs move with `h` in the right
direction (8.411 -> 7.126 from `h=0.4` to `h=0.3` at fixed `Lambda` and collar), but **two
points are a trend, not a verdict**: `kc_h04.out`/`kc_h05.out` (8.2635 and 10.0467) are *not*
comparable rungs of the same ladder — they differ in `LamC` (6, 4 vs 12), `n_B` (9, 7 vs 9,11)
and `n_C` (15, 8 vs 30,40) — and S11 identifies `n_B/n_C` and the collar `s`, not `h` alone,
as the knobs (`kc_h04.out`'s `Delta/(2 g_Q) = -10.325` is S11's `n_B < n_C` corner).  No
extrapolated "factor still to be closed" is claimed here.  T3 therefore cannot decide Q1; the
tangent problem (T1/T2/T4/T5) is the right place; T4/T5 answer it only as far as the numerics can: condition (a) as an extrapolation, condition (e) under H3 (see the Verdict on Q1 and Correction C5).

## T4 (the test of (a)). The criterion in the parameter-free modular Wiener-Hopf frame

Frame: F1 Prop 6.2 as discretised by F3 in `f3_t0.py` — `I = (-inf,1)`, `y = -log(1-x)`,
`A = {y<0}`, `D = {y>0}`, `Q` exact in the piecewise-constant cell basis
(`kkt_continuum.Qmat`), and the first-order compression defect in closed form
`ddot(y1,y2) = -(i/2pi) sinh(y1/2) sinh(y2/2)/sinh^2((y1-y2)/2) + h.c.` for `y1<0<y2`.
**Moebius rigidity is exact here**: `||ddot_DD|| = 0.0` identically (no spurious blocks),
and the weights need **no cap** — `kappa_max = 5.4 ... 7.7` and `max w = 1.1e2 ... 1.1e3`
for `h = 0.24 ... 0.06`, so `den` is never near-singular and `q` is clipped only formally
to `[1e-300, 1-1e-16]` (F3's convention).  `theta` and the optimal rotation come from
`f3_gal.theta` (CG); with that routine's normalisation `G_* = -2x`, and
`g_Q(deltadot + [Q,G_*])/g_Q(deltadot) = 1 - theta` is verified to 6 digits at every point.

Reproduce: `$V/bin/python f2_t4_wh.py 0.24 10 10` (smoke), `f2_t4_wh.py 0.12,0.06 10 10`
-> `f2_t4_hladder.out`, `f2_t4_wh.py 0.03 10 10` -> `f2_t4_h003.out`; the cutoff scans are in
`f2_t4_ymax12.out` (see the commands at the end).  Checks at every point:
`theta` reproduces F3's ladder exactly (0.31367, 0.34236, 0.35934 at h = 0.24, 0.12, 0.06,
Y = Ymax = 10); SLD identity `(1/4)Tr(t_* delta_*)/g_Q(delta_*) = 1.0000000000`;
`||AntiHerm((t_*Q)_DD)||/||M_*|| = 2.8e-09, 8.5e-08, 1.5e-07` (F1 Prop 4.3); F1's derivative
formula by finite differences, relative error 3.94e-10, 1.08e-08, 7.56e-09 at h = 0.24, 0.12, 0.06 and 2.63e-08 at h = 0.03, i.e. `<= 3e-8` (FD lines of `f2_t4_h024.out`, `f2_t4_hladder.out`, `f2_t4_h003.out`; see Correction C4).

### (a) h-ladder at fixed window `Y = Ymax = 10`

| h | N | theta | `lam_min(M_*)` | `/g_Q(ddot)` | `/||M_*||` | `lam_min(M_*-tau_*)/g_Q(ddot)` | rank-1 gain `/g_Q(ddot)` | `p` lives at `y` |
|---|---|---|---|---|---|---|---|---|
| 0.24 | 84 | 0.31367 | -5.432e-04 | -7.013e-02 | -4.076e-03 | -7.013e-02 | 3.85e-04 | 5.2 - 5.9 |
| 0.12 | 166 | 0.34236 | -3.045e-04 | -3.757e-02 | -1.859e-03 | -3.757e-02 | 1.23e-04 | 4.9 - 5.3 |
| 0.06 | 334 | 0.35934 | -1.610e-04 | -1.942e-02 | -8.228e-04 | -1.942e-02 | 3.51e-05 | 4.2 - 4.4 |
| 0.03 | 666 | 0.36945 | -8.387e-05 | -1.001e-02 | -3.667e-04 | -1.001e-02 | 9.69e-06 | 1.85 - 1.94 |

The violation **shrinks like `h^1.15`** (ratios 2.19, 2.26, 2.24 per halving) and the rank-one
gain like `h^1.85` (ratios 3.13, 3.50, 3.62): both extrapolate to **0** as `h -> 0`.
(`theta` = 0.31367, 0.34236, 0.35934, 0.36945 reproduces F3's ladder at all four `h`.)
`lam_min(M_*)` and `lam_min(M_*-tau_*)` coincide to 5 digits at every point, but on different
eigenvectors with the same localisation and modulus profile and opposite `<p,tau_*p>` (at h = 0.24: `<p,M_*p> = -5.4316e-04`, `<p,tau_*p> = -3.3086e-03` for the `M_*` minimiser, `+2.7654e-03`, `+3.3086e-03` for the `M_*-tau_*` minimiser; `f2_t4_h024.out` l.6-7), as in T2 (see Correction C1).

### (b) It is the `y`-truncation: `Ymax` scans (the A-side cutoff `Y` is irrelevant)

`h = 0.12`, `Y = 6`:

| Ymax | 6 | 8 | 10 | 14 | 20 | 30 |
|---|---|---|---|---|---|---|
| theta | 0.33984 | 0.34153 | 0.34235 | 0.34328 | 0.34395 | 0.34447 |
| `lam_min(M_*)/||M_*||` | -3.014e-03 | -2.286e-03 | -1.865e-03 | -1.339e-03 | -9.459e-04 | -6.360e-04 |
| x `Ymax` | -0.0181 | -0.0183 | -0.0186 | -0.0187 | -0.0189 | -0.0191 |
| rank-1 gain `/g_Q(ddot)` | 3.325e-04 | 1.874e-04 | 1.230e-04 | 6.236e-05 | 3.080e-05 | 1.380e-05 |
| x `Ymax^2` | 0.01197 | 0.01199 | 0.01230 | 0.01222 | 0.01232 | 0.01242 |
| `p` lives at `y ~` | 3.1 | 4.2 | 5.2 | 7.4 | 12.0 | 11.2 |

`h = 0.24`, `Y = 10`, same pattern: `lam_min/||M_*|| = -6.562e-03, -5.095e-03, -4.076e-03,
-3.003e-03, -2.125e-03` for `Ymax = 6,8,10,14,20` (times `Ymax`: -0.0394 ... -0.0425), gain
`1.049e-03, 6.150e-04, 3.846e-04, 2.042e-04, 1.007e-04` (times `Ymax^2`: 0.0378 ... 0.0403),
`p` at `y ~ 3.4, 4.4, 5.6, 7.5, 10.8`.
A-side cutoff: `Y = 6, 10, 14` at `h=0.24, Ymax=10` give
`lam_min(M_*)/||M_*|| = -4.0904e-03, -4.0756e-03, -4.0751e-03` — **independent of `Y` to 0.4%**.

So the violating direction is not a feature of the problem: at fixed `h` it is a delocalised
mode sitting at `y ~ (0.37-0.6) Ymax` (0.37 at `Ymax = 30`, where it sits inward of its `Ymax = 20` location; see Correction C4), i.e. it **tracks the artificial outer end of the `y`
window** (the moving endpoint `x = 1`, which `f3_t0.py` already flags as the delicate limit).
(At fixed `Ymax = 10` the mode moves inward as `h` falls -- `y ~ 5.5, 5.1, 4.3, 1.9` for
`h = 0.24, 0.12, 0.06, 0.03` -- while its eigenvalue keeps shrinking.)  The two scalings are
clean:


    lam_min(M_*)/||M_*||  ~  -c(h)/Ymax  ,   rank-1 gain/g_Q(ddot)  ~  c'(h)/Ymax^2 ,
    c(0.24) = 0.041, c(0.12) = 0.0187 ;  c'(0.24) = 0.039, c'(0.12) = 0.0123   (both ~ h^1.1..h^1.7)

both vanishing in the physical double limit `h -> 0`, `Ymax -> +inf`.

### Verdict on Q1 (as far as numerics can say)

In the frame where Moebius rigidity is exact and the weights need no cap, the F1 Thm 4.4
criterion `M_* >= 0`, `M_* - tau_* >= 0` is violated **only** by an amount that goes to zero
in the continuum/untruncated limit, in two independent directions of parameter space, with
clean power laws and with the violating eigenvector pinned to the truncation window.  The
numerics therefore say, **as an extrapolation** (every finite run prints `CRITERION (M>=0 and M-tau>=0): False`): the violation of condition (a) goes to `0^-` in the double limit `h -> 0`, `Ymax -> inf`, so (a) can hold only in the limit, marginally, not strictly (see Correction C5);
condition (e) is treated separately in T5 below (vacuous at `zeta_0`; under hypothesis H3 it follows from `E(zeta_inf) >= 0` alone).
The numerics are thus consistent with the isometric orbit carrying the global optimum of the tangent problem, with `kappa_opt = 1 - theta`; they do NOT show that the optimal `N_1`,
`Y_1` are zero (F1 Thm 4.4(d) gives a global minimiser, not uniqueness, and `lam_min -> 0^-` is exactly the marginal case).  Non-isometric quasi-free recoveries do
NOT lower the second-order recovery error by any O(1) amount: every measured rank-one gain is `<= 1.05e-3 g_Q(ddot)` and falls like `h^1.85/Ymax^2`.  The T2 (circle-model) "failure" of the criterion
and the T1 subspace gains are artefacts of a frame that breaks rigidity at O(1/L) and then
amplifies the broken blocks by weights up to the cap.

## T5 (the test of (e)). The endpoint condition of the repaired criterion — vacuous at `zeta_0`; under H3 it holds (see Correction C6)

F1 Thm 4.4 condition (e) / Prop 4.10: the boundary-moving isometry generators are not
reducible to noise, and (e) reduces on the model cone to the single scalar
`E(zeta_0) >= 0` at the junction `y = 0` (for the moving-endpoint direction `zeta_inf`, `E(zeta_inf) = 2 lambda (1-theta) g_Q(ddot) >= 0` is
proved, while `E(zeta_inf) > 0` is equivalent to `theta < 1`, which is numerical, not proved; see Correction C3).  Frame: the same rigid parameter-free Wiener-Hopf frame as T4
(`f2_t5_endpoint.py`, importing `f2_t4_wh.build`; run saved as `f2_t5_endpoint.out`).

**Normalisation used: F1's.**  `t_* = U (w o delta~_*) U^H`, `g_Q(delta_*) = (1/4)Tr(t_* delta_*)`
(verified 1.0000000000 at every point), and
`E(zeta) = 2 b(delta_*, A(zeta,0,0)) = (1/2) Tr(t_* A(zeta,0,0))` — the factor of Sec. 5 item 5.

### A correction to the recipe (please read, F1)

The recipe says `E(zeta) = 2b(delta_*, A(zeta,0,0)) = -2 b(delta_*,[Q,zeta]) = (1/2)Tr(t_*[Q,S])`.
The middle equality is **not** a matrix identity for an endpoint-moving `zeta`: by
eq:Ablocks, `A(zeta,0,0)_{DA} = -zeta^* Q_{DA}` and
`A(zeta,0,0)_{DD} = -(zeta^* Q_{DD} + Q_{DD} zeta)`, which equals `-[Q,zeta]` **only when
`zeta^* = -zeta`**.  For a general `zeta = G + sigma` (`G` anti-Hermitian, `sigma = Herm(zeta)`)
one gets exactly the absorption identity `A(zeta,0,0) = A(G, -2 sigma, 0)`.  Numerically this
matters completely, because the naive commutator expression is *identically blind*: for any
matrix `X` supported on `D`, cyclicity of the trace of finite matrices gives

    Tr(t_*[Q,X]) = 2 Tr( X . AntiHerm((t_* Q)_DD) )          (verified to 4e-10 .. 1e-7)

and discrete stationarity of `G_*` over the full anti-Hermitian algebra on `D` forces
`AntiHerm((t_*Q)_DD) = 0`.  So `(1/2)Tr(t_*[Q,S])` returns only the stationarity (CG) residual contracted with `S` and carries no information about `E` (see Correction C7); for `zeta_0` it is small here — `+6.9e-09,
+3.6e-07, +2.3e-06, -1.9e-05` at `h = 0.24, 0.12, 0.06, 0.03`, the **same number for the
forward, backward and centred `S`** (indeed `AntiHerm(S_fwd) = AntiHerm(S_bwd) = S_ctr`
identically on a uniform mesh).  Proof that this is blindness and not a small true value:
the same expression applied to `zeta_inf` (with the discretised `D_w|_D`), whose value is
*known* to be `2(1-theta) g_Q(ddot) = 1.26 ... 1.37 g_Q(ddot)`, returns `-9.1e-06, +1.9e-04, -9.9e-03, +7.4e-02` at `h = 0.24, 0.12, 0.06, 0.03` and `-0.116, -63, -1.57e+06` at `Ymax = 14, 20, 30` (`h = 0.12`, `Y = 6`): not merely small noise but `O(1)`, and worse as `h` decreases or `Ymax` grows (see Correction C7).
The correct object is `A(zeta,0,0)` from eq:Ablocks, equivalently `(1/2)Tr((-2 sigma) M_*)`;
the two agree to `2e-10 ... 7.5e-8` in all runs below (see Correction C4).

### The three difference schemes are three different directions (not three discretisations)

On the uniform D-mesh, `zeta_0 = -S` with `S = E_D d/dy E_D` truncated at both ends:

| scheme | `sigma = Herm(zeta_0)` | meaning | `E(zeta_0)/g_Q(ddot)` at h=0.24 |
|---|---|---|---|
| backward (`(U-I)/h`, the exact one-cell shift) | `eig in [-8.32, -1.1e-02]`, `<= 0` | **admissible** isometry generator | **+34.122** |
| centred | `sigma = 0` exactly | anti-Hermitian: lies in `L-bar`, no endpoint motion | `+6.9e-09` (= 0) |
| forward | `eig in [+1.1e-02, +8.32]`, `>= 0` | decompression, points out of `D` | `-34.122` (inadmissible) |

This is exactly the theory: `E = 0` on `L-bar` (Prop 4.10(1)), `E` odd under `zeta -> -zeta`,
and only the upwind/backward difference is the shift semigroup `(U_a g)(y) = g(y-a)`.  So the
"scheme-independence" that a bulk quantity would need does not apply here; what must be
(and is) reproduced is the sign pattern above.

### What the admissible number contains

For the backward (upwind) scheme, `-2 sigma = (1/h)(2I - U - L) >= 0` acts on cell
coefficients as the quadratic form

    <g, (-2 sigma) g>  =  |g(0)|^2  +  h * int_0^Ymax |g'|^2  +  |g(Ymax)|^2 ,

i.e. exactly F1's continuum boundary form `|delta_0><delta_0|` at the junction, **plus** the
`O(h)` numerical viscosity of upwinding, **plus** a second boundary term at the artificial
far end (the truncated shift is only a partial isometry: it loses the last cell).  Hence

    E(zeta_0)^{discrete} = (1/2)[ M_*(0,0) + h Tr((-Laplacian) M_*) + M_*(Ymax,Ymax) ] ,

and the piece that represents the continuum `E(zeta_0)` of eq:econd (it does not converge to it: it diverges as `h -> 0`, see below and Correction C6) is the **corner term**
`(1/2) M_*(0,0) = (1/2)(M_*)_00/h`.  All three pieces are positive at every `h`, `Y`, `Ymax`.

### T5 results (`f2_t5_endpoint.out`)

**h-ladder at `Y = Ymax = 10`** (`E` in units of `g_Q(ddot)`; `bwd` = the admissible shift).
The `bwd` column is the TOTAL discrete value (scheme-dependent, `~h^-0.97`, dominated by the
`O(h)` upwind viscosity); the **corner** column is the scheme-invariant piece that represents the continuum boundary
form; it diverges as `h -> 0`, so it is not a margin: (e) is vacuous at `zeta_0` (see Correction C6):

| h | N | theta | `E(zeta_0)` bwd | `E` ctr | `E` fwd (inadm.) | corner `(1/2)(M_*)_00/h` | `E(zeta_inf)` = `(1/2)Tr(t_* ddot)` | `2(1-theta)` | naive `(1/2)Tr(t_*[Q,S])` |
|---|---|---|---|---|---|---|---|---|---|
| 0.24 | 84 | 0.31367 | **+34.122** | +6.9e-09 | -34.122 | **+10.304** | 1.37265519 | 1.37265519 | +6.9e-09 |
| 0.12 | 166 | 0.34236 | **+66.873** | +3.6e-07 | -66.873 | **+16.096** | 1.31527744 | 1.31527744 | +3.6e-07 |
| 0.06 | 334 | 0.35934 | **+131.298** | +2.3e-06 | -131.298 | **+24.672** | 1.28132522 | 1.28132522 | +2.3e-06 |
| 0.03 | 666 | 0.36945 | **+257.998** | -1.9e-05 | -257.998 | **+37.210** | 1.26109117 | 1.26109117 | -1.9e-05 |

`eq:Ablocks` and the absorption form `(1/2)Tr((-2 sigma)M_*)` agree to `2e-10 ... 7.5e-8` (`7.5e-8` at h = 0.03; see Correction C4)
at every rung.  Cross-check (i) is exact to machine precision at all four `h`
(`rel.dev 2e-16 ... 1e-15`), which validates the `b(.,.)`, the SLD normalisation and the
factor `1/2`.  Cross-check (iii): `||AntiHerm((t_*Q)_DD)||/||M_*|| = 2.8e-09, 8.5e-08,
1.5e-07, 3.5e-07`.  Cross-check (iv) (referee R14), the rank-one gain from T4:
`3.85e-04, 1.23e-04, 3.51e-05, 9.69e-06` of `g_Q(ddot)` on the same ladder (`~ h^1.85 -> 0`).

**Saturation.**  The *total* `E(zeta_0)` grows like `1/h` (ratios 1.960, 1.963, 1.965) — that
is the `O(h)` upwind viscosity term `h Tr((-Lap) M_*)`, which is a discretisation artefact
(a legitimate PSD `N_1` direction, hence positive, but scheme-dependent).  The **corner**
term, which represents the continuum `E(zeta_0)`, grows like `h^{-0.6}` (ratios 1.562, 1.533, 1.508):
it does **not** saturate in `h`; it diverges, consistent with a divergence of the kernel
diagonal `M_*(y,y)` as `y -> 0+` (the near-corner diagonals `(M_*)_jj/h_j` at `h=0.06` are
`+0.409, +0.333, +0.286, +0.252` for `y = 0.03 ... 0.21`).  In the continuum therefore
`|delta_0><delta_0|` is not in the form domain of `M_*` and `E(zeta_0) = +infinity`: shifting
the junction end of `D` inward destroys the recovery at first order with infinite slope.

**Cutoff controls (`h = 0.12`)** — both quantities **saturate in `Ymax`** and are
**independent of `Y`**:

| Ymax (Y=6) | 6 | 10 | 14 | 20 | 30 |
|---|---|---|---|---|---|
| `E(zeta_0)` bwd | +66.899 | +67.066 | +67.231 | +67.356 | +67.453 |
| corner | +16.461 | +16.145 | +16.035 | +15.955 | +15.893 |

`Y = 6, 10, 14` at `Ymax = 10`: `E(zeta_0)` bwd `= +67.066, +66.873, +66.869`; corner
`= +16.145, +16.096, +16.096`.

**Cross-check (ii), the cell form.**  The first-cell diagonal of `M_*` normalised by the cell
width is `+0.160, +0.261, +0.409, +0.623` at `h = 0.24 ... 0.03` (positive: same sign as
`E(zeta_0)`), and the last-cell diagonal is `+3.2e-03, +3.9e-03, +4.4e-03` at
`h = 0.24, 0.12, 0.06` (positive: same sign as `E(zeta_inf) = 2 lambda (1-theta) g_Q(ddot)`, which is proved `>= 0` and is `> 0` here because `theta < 1` numerically; see Correction C3).

### Verdict on (e)

**Numerically, at every finite discretisation, `E(zeta_0) > 0` and `E(zeta_inf) > 0` on the two model
boundary directions of F1 Prop 4.10(3): the regularised junction value is `+10.3, +16.1, +24.7,
+37.2` times `g_Q(ddot)` at `h = 0.24 ... 0.03` — the CORNER row `(1/2)(M_*)_00/h`, which is
the scheme-invariant piece; the tabulated total (`+34 ... +258`, `~h^-0.97`) is dominated by
the `O(h)` upwind-viscosity term of the difference scheme.  The corner row diverges (`~h^-0.60`), so `A(zeta_0,0,0)` is not in F and `E(zeta_0) = +infinity` in the sense of eq:Efun, a convention: (e) is vacuous at `zeta_0`, not satisfied with a margin (see Correction C6).
No sign change at any `h = 0.24 ... 0.03`, `Ymax = 6 ... 30`, `Y = 6 ... 14`.**  Condition (e)
for the WHOLE admissible cone holds under hypothesis H3 (F1 hyp:H3, read in F: every admissible `A(zeta,0,0)` in F is, modulo the b-closure of the linear class, a non-negative combination of `A(zeta_0,0,0)` and `A(zeta_inf,0,0)`):
since `A(zeta_0,0,0)` is not in F (numerically, by the divergent corner row), H3 forces its coefficient to vanish and (e) follows from the proved `E(zeta_inf) >= 0` alone (F1 rem:H3space).
H3 is a hypothesis these numerics do not test.  The sign of `E(zeta_0)` is NOT structurally forced in this
frame: at finite `h` the absorption identity holds and `-2 sigma_{zeta_0} >= 0` is a legitimate `N_1` direction, but
`E(zeta_0) = (1/2)Tr((-2 sigma) M_*) >= 0` would follow from `M_* >= 0`, i.e. from condition (a), which fails in every run, and `-2 sigma` has full rank; in the continuum the identity is not available (F1 prop:bdryfun(5)).  The positive sign is a numerical fact.
Together with T4: **numerically (a) in the limit (`lam_min -> 0^-`); `E(zeta_0) > 0` and
`E(zeta_inf) > 0`; (e) for the whole cone under H3** — under which the numerics are consistent with the
isometric orbit carrying the tangent optimum and `kappa_opt = 1 - theta` (a global minimiser, not uniqueness; see Correction C5).
Reproduce: `$V/bin/python f2_t5_endpoint.py 0.24 10 10` (smoke) and the driver in
`f2_t5_endpoint.out`'s header (h-ladder + `Ymax`/`Y` scans).

## Exact commands to reproduce

```
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team/2a3c5aab-2bd9-408c-811f-f4144c2149e4/scratchpad/venv
cd /Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/optimality_all

# conventions / theta / orbit-only SDP / homogeneity          (f2_tangent_sdp.py 64 prints all four)
$V/bin/python f2_tangent_sdp.py 64
# T2, F1 form, L ladder                                        -> f2_kkt_f1_L.out
$V/bin/python f2_kkt_f1.py 64,96,128,192,256 1e10
# T2, brief's SLD normalisation + FD checks                    -> f2_kkt.out
$V/bin/python f2_kkt_check.py 64,96,128,192,256
# T2 cap / UV-taper stability                                  -> f2_capscan_L128.out
$V/bin/python f2_capscan.py 128 1e4,1e6,1e8,1e10,1e12 0.30,0.20
# T4 h=0.24 rung (the smoke row, as a file)                     -> f2_t4_h024.out
$V/bin/python f2_t4_wh.py 0.24 10 10
# T1 subspace lower bounds (bug-fixed version)                 -> f2_sub_gain_fixed.out
$V/bin/python f2_sub_gain.py 64,128 1e10 4
# T1 Gram condition numbers                                    -> f2_gram_cond.out
$V/bin/python -c "import numpy as np, f2_model as M, f2_tangent_gram as TG
for (L,cap) in [(64,1e4),(64,1e6),(64,1e10),(96,1e10)]:
    S=M.build(L=L,cap=cap); G,c,g0=TG.quadform(S); s_=np.linalg.eigvalsh(G); pos=s_[s_>0]
    print(L,cap,G.shape[0],s_.max(),pos.min(),s_.max()/pos.min())" 
# T1 Gram-cutoff artefact demonstration
$V/bin/python f2_gram_verify.py 64 1e6 1e-14,1e-10,1e-6
# T1 ill-posedness of the unconstrained relaxation
$V/bin/python f2_gain.py 64 1e10,1e4 200
# T3 Galerkin full F                                           -> f2_galerkin_a.out
$V/bin/python f2_galerkin_full.py 0.4,0.3
# T4 (the test of (a)): modular Wiener-Hopf frame
$V/bin/python f2_t4_wh.py 0.24 10 10                           # smoke, theta=0.31367
$V/bin/python f2_t4_wh.py 0.12,0.06 10 10                      -> f2_t4_hladder.out
$V/bin/python f2_t4_wh.py 0.03 10 10                           -> f2_t4_h003.out (N=666)
$V/bin/python -c "import f2_t4_wh as T
for Ym in (6.,8.,10.,14.,20.,30.): T.run(0.12, Y=6.0, Ymax=Ym, fd=False)"   -> f2_t4_ymax12.out
$V/bin/python -c "import f2_t4_wh as T
for (Y,Ym) in [(10,6),(10,8),(10,14),(10,20),(6,10),(14,10),(6,20)]: T.run(0.24, Y=float(Y), Ymax=float(Ym), fd=False)"
# T5 (the test of (e)): endpoint condition                      -> f2_t5_endpoint.out
$V/bin/python f2_t5_endpoint.py 0.24 10 10                     # smoke
$V/bin/python -c "import f2_t5_endpoint as T5
r=[T5.run(h) for h in (0.24,0.12,0.06,0.03)]
r2=[T5.run(0.12, Y=6.0, Ymax=Ym) for Ym in (6.,10.,14.,20.,30.)]
r3=[T5.run(0.12, Y=Yv, Ymax=10.0) for Yv in (6.,10.,14.)]"
```

Caveat on timings: all runs above were made while the machine carried a load average of
~500 (other tracks), so wall-clock times in the `.out` files are not indicative.

## Corrections of 2026-09-24

These corrections were made on 2026-09-24 from the project's knowledge base, cards
`kkt-noise-criterion-numerics` (for which this file is the main evidence) and
`kkt-noise-sign-criterion`. Each corrected line above was replaced by exactly one line, so the
line numbers of the text above this section are unchanged. Every corrected number was checked
against the `.out` file it summarises.

**C1. Same eigenvector (lines 100 and 285-286).**
*Said:* the two criteria `M_* >= 0` and `M_* - tau_* >= 0` "fail on the *same* eigenvector, with
`<p,M_* p> ~ -<p,tau_* p>`" (T2, circle model), and in T4 "the same eigenvector, with
`<p,M_*p> ~ -<p,tau_*p>`), exactly as in T2".
*Says now:* the two minimisers are different eigenvectors with the same localisation (and, in T4,
the same modulus profile) and opposite `<p,tau_* p>`.
*Why:* `f2_t4_wh.py` and `f2_kkt_f1.py` diagonalise `M_*` and `M_* - tau_*` separately and print
both vectors. T4, h = 0.24 (`f2_t4_h024.out` l.6-7): the `M_*` minimiser has
`<p,M_*p> = -5.4316e-04`, `<p,tau_*p> = -3.3086e-03`; the `M_* - tau_*` minimiser has
`+2.7654e-03`, `+3.3086e-03`; both live at `y = 5.16, 5.4, 5.88, 5.64` with the same `|p|`. The
other rungs (`f2_t4_hladder.out` l.6-7, 14-15; `f2_t4_h003.out` l.6-7) are alike. Neither vector
satisfies `<p,M_*p> ~ -<p,tau_*p>`. T2, L = 64 (`f2_kkt_f1_L.out` l.5-6): the `M_*` minimiser has
`<p,M_*p> = -0.3108 ~ +<p,tau_*p> = -0.3097`, so line 99 ("`M_* - tau_*` is nearly zero
on the violating directions") holds for the `M_*` minimiser, `<p,(M_* - tau_*)p> = -1.1e-03`; the `M_* - tau_*` minimiser has `<p,tau_*p> = +0.3097` and
`<p,M_*p> = -1.1e-03`. The old wording contradicted line 99. Knowledge-base card
`kkt-noise-criterion-numerics`, document error recorded on 2026-09-23 (after referee
REF-DEP-CFT-A4).

**C2. T5 table, row h = 0.03 (line 413).**
*Said:* `E(zeta_inf)/g_Q(ddot) = 2(1-theta) = 1.26109076`. *Says now:* `1.26109117` in both columns.
*Why:* `f2_t5_endpoint.out` l.33 prints `E(zeta_inf)/g_Q(ddot) = ... = 1.26109117   exact
2(1-theta) = 1.26109117`; its summary row l.47 prints `1.261091` for both, which agrees. The old
value was a transcription error of relative size 3e-7. Card `kkt-noise-criterion-numerics`,
document error recorded on 2026-09-23.

**C3. Sign of `E(zeta_inf)` (lines 339-340 and 446).**
*Said:* "the moving-endpoint direction `zeta_inf` is proved positive", and "the proved
`E(zeta_inf) > 0`". *Says now:* `E(zeta_inf) = 2 lambda (1-theta) g_Q(ddot) >= 0` is proved;
`E(zeta_inf) > 0` is equivalent to `theta < 1`, which holds numerically here
(`theta_h = 0.31367 ... 0.36945`; the knowledge base gives `1 - theta = 0.616 +- 0.003`) but is
not proved. *Why:* card `kkt-noise-sign-criterion`, Statement (iii): "E(zeta_inf) = 2 lambda
(1-theta) g_Q(ddelta) is proved, hence E(zeta_inf) >= 0; E(zeta_inf) > 0 is equivalent to
theta < 1, which is NOT proved". The check `E(zeta_inf) = 2(1-theta_h) g_Q(ddot)` itself is exact
to `2e-16 ... 1e-15` (`f2_t5_endpoint.out` l.3, 13, 23, 33).

**C4. Numbers that the card's referees corrected and this file repeated.**
- Line 120. *Said:* `theta` is cap-stable "to 5 digits". *Now:* "to 4 digits". *Why:*
  `f2_capscan_L128.out` l.2-6 and l.7-11 give 0.29116-0.29119 and 0.26146-0.26150 (REF-DEP-CFT-A6).
- Line 271. *Said:* FD check of F1's derivative formula, "relative error 4e-09". *Now:* 3.94e-10,
  1.08e-08, 7.56e-09 at h = 0.24, 0.12, 0.06 and 2.63e-08 at h = 0.03, i.e. `<= 3e-8`. *Why:* the FD
  lines `f2_t4_h024.out` l.5, `f2_t4_hladder.out` l.5 and l.13, `f2_t4_h003.out` l.5
  (REF-P5-KB1, REF-P5-3, REF-DEP-CFT-A2).
- Line 309. *Said:* the violating mode sits at `y ~ (0.4-0.6) Ymax`. *Now:* `(0.37-0.6) Ymax`.
  *Why:* `f2_t4_ymax12.out`: at `Ymax = 30` it lives at `y = 11.1-11.5` (0.37 `Ymax`), inward of its
  `Ymax = 20` location `y = 11.8-12.3`; the table in line 299 already shows `11.2` at `Ymax = 30`
  (REF-opus-kbgate2, REF-DEP-CFT-A6).
- Lines 368 and 415. *Said:* `eq:Ablocks` and the absorption form agree to `2e-10 ... 2e-8`.
  *Now:* `2e-10 ... 7.5e-8`. *Why:* the relative deviations printed in `f2_t5_endpoint.out` are
  2.0e-10, 5.4e-09, 1.8e-08, 7.5e-08 on the h-ladder (l.7, 17, 27, 37) and up to 6.5e-08 in the
  `Ymax` scan (l.95); the card states `<= 7.5e-8` (REF-DEP-CFT-A5).

**C5. What the numerics say about Q1 (lines 327-331 and 462-463).**
*Said:* "`M_* >= 0` and `M_* - tau_* >= 0` hold for the exact problem", condition (e) "holds", "the
isometric orbit IS the global optimum of the tangent problem, the optimal `N_1`, `Y_1` are ZERO,
and `kappa_opt = 1 - theta` exactly", "Non-isometric quasi-free recoveries do NOT lower the
second-order recovery error"; and "under which the numerics say the isometric orbit carries the
tangent optimum". *Says now:* (a) is an extrapolation: every finite run prints
`CRITERION (M>=0 and M-tau>=0): False` (`f2_t4_h024.out` l.4, `f2_t4_hladder.out` l.4 and l.12,
`f2_t4_h003.out` l.4, every block of `f2_t4_ymax12.out`), and the violation goes to `0^-` in the
double limit, a marginal, not a strict, sign. The numerics are consistent with the isometric orbit
carrying the tangent optimum and `kappa_opt = 1 - theta`, but do not show that the optimal `N_1`,
`Y_1` vanish: F1 Thm 4.4(d) gives a global minimiser, not uniqueness, and the marginal case is
exactly where uniqueness is not delivered. They exclude any O(1) gain: every measured rank-one
gain is `<= 1.05e-3 g_Q(ddot)` (the largest, 1.049e-3 at h = 0.24, `Ymax = 6`, is line 303 of this
file and is in no saved output; in the runs with output files it is `<= 3.85e-4`,
`f2_t4_h024.out` l.6) and falls like `h^1.85/Ymax^2`. *Why:* card `kkt-noise-criterion-numerics`,
Statement ("READ THE SIGN CLAIM AS AN EXTRAPOLATION", "WHAT MAY AND MAY NOT BE CONCLUDED"), after
the referee failure of 2026-09-15 (REF-opus-kbgate2, points (1) and (2)).

**C6. The reading of condition (e) (lines 87, 335, 398, 405-406, 425, 450-460).**
*Said:* the criterion is "orbit = global optimum **iff** `M_* >= 0` and `M_* - tau_* >= 0`" (line
87); T5 "HOLDS" (line 335); the corner term "converges to" and "is" the continuum `E(zeta_0)` and
"is the margin to quote" (lines 398, 405-406, 425); "(e) is verified for the two model boundary
directions ..., with a continuum margin of +10.3, +16.1, +24.7, +37.2"; (e) for the whole cone
"follows from these two numbers" under a model-cone reduction "that modulo `L-bar` the cone is
generated by `zeta_0` and `zeta_inf`"; and "The sign is structurally forced in this frame ...
follows from `M_* >= 0`, i.e. from condition (a)" (lines 450-460).
*Says now:* F1 Thm 4.4 as amended needs (a) **and** (e); (a) alone is necessary, not sufficient.
The corner row represents the continuum `E(zeta_0)` and diverges (`~h^-0.60`), so
`A(zeta_0,0,0)` is not in F and `E(zeta_0) = +infinity` in the sense of eq:Efun, a convention:
(e) is vacuous at `zeta_0`, not satisfied with a margin; the positive finite-h values are the
regularised junction values. H3 is stated as in F1 (hyp:H3, read in F): every admissible
`A(zeta,0,0)` in F is, modulo the b-closure of the linear class, a non-negative combination of
`A(zeta_0,0,0)` and `A(zeta_inf,0,0)`. Under H3 the `zeta_0` coefficient vanishes and (e) follows
from the proved `E(zeta_inf) >= 0` alone (F1 rem:H3space). The sign of `E(zeta_0)` is a numerical
fact, not a forced one: at finite h the absorption identity holds, but `M_* >= 0` fails in every
run and `-2 sigma` has full rank (`eig(sigma) in [-8.322, -1.112e-02]` at h = 0.24,
`f2_t5_endpoint.out` l.7); in the continuum the identity is not available (F1 prop:bdryfun(5)).
*Why:* card `kkt-noise-criterion-numerics`, Statement (lead; "(e) ENDPOINT CONDITION"; "VERDICT ON
(e), QUALIFIED"), after the referee failures REF-DEP-CFT-A4 (point 4) and REF-DEP-CFT-A5
(points (i)-(iv) and the H3 remark); card `kkt-noise-sign-criterion`, Statement (ii)-(iii).

**C7. What the commutator form returns (lines 361 and 366).**
*Said:* "`(1/2)Tr(t_*[Q,S])` returns the CG residual — `+6.6e-09`, ..." and, for `zeta_inf`, "returns
`-8.3e-06 ... -9.9e-03`". *Says now:* the commutator form returns only the stationarity (CG)
residual contracted with the direction and carries no information about `E`. For the `zeta_0`
matrices `S` it is small here: `+6.9e-09, +3.6e-07, +2.3e-06, -1.9e-05` on the h-ladder, the same
for all three schemes. For `zeta_inf`, whose true value is `2(1-theta_h) g_Q(ddot) = 1.26 ... 1.37
g_Q(ddot)`, it returns `-9.1e-06, +1.9e-04, -9.9e-03, +7.4e-02` at h = 0.24, 0.12, 0.06, 0.03 and
`-0.116, -63, -1.57e+06` at `Ymax = 14, 20, 30` (h = 0.12, `Y = 6`): not merely small noise but
`O(1)`, and worse as h decreases or `Ymax` grows. *Why:* the `(trace formula)` lines of
`f2_t5_endpoint.out` (l.5, 15, 25, 35 on the h-ladder; l.73, 83, 93 in the `Ymax` scan) print
these numbers; `+6.6e-09` and `-8.3e-06` occur in no output (the first is `+6.8792e-09`, l.5,
as the T5 table already shows). Card `kkt-noise-sign-criterion`, Statement (NUMERICAL part: "the
commutator form returns, even for zeta_inf, -9.1e-6, +1.9e-4, -9.9e-3, +7.4e-2 ... and -63, -1.6e6
on other rungs of the scan (O(1), no information on the true 2 lambda (1-theta) g_Q(ddelta)"); its
referee notes list the old reading, "returns only the CG residual (-8e-6 ... -1e-2) even for
zeta_inf", as stale. F1 (`rigor/exact_optimum_tangent_problem.tex`), Prop 4.10(2') and Sec. 5 item 5,
says the same ("not merely solver noise but O(1) and worse on the finer scans").
The docstring of `f2_t5_endpoint.py` (l.16-17, "zero to the CG residual, for every
discretisation of S") carries the old reading; it is a script and is not changed here.

**C8. Labels and details (after the referee REF-DOC-SMALL; lines 24, 25, 250, 252, 335, 422, 496,
504, and C1, C6, C7 above).**
*Said:* T4 and T5 were labelled "decisive" / "DECISIVE" (lines 24, 25, 252, 335, 496, 504), and
line 250 said that the tangent problem "answers" Q1. *Says now:* "the test of (a)" and "the test
of (e)"; line 250 says that T4/T5 answer Q1 only as far as the numerics can: (a) as an
extrapolation, (e) under H3. *Why:* the Verdict on Q1 (C5) and the reading of (e) (C6); a test
whose outcome is an extrapolation, or holds under a hypothesis the numerics do not test, does not
decide the question. Also: line 422, ratios of the total `E(zeta_0)` "1.960, 1.963, 1.966" ->
"1.965" for the last (`+257.9981/+131.2980 = 1.96498`, `f2_t5_endpoint.out` l.44-47); line 366,
the scan values are at `h = 0.12`, `Y = 6`; line 460 reads "would follow from `M_* >= 0`"
instead of "would follow only from" (C6); C1 now says that line 99 holds for the `M_*`
minimiser.

**Checked without change.** The corner value at `Ymax = 20` in the cutoff table, `+15.955`, is
right: `f2_t5_endpoint.out` l.87 and l.137 print `1.595497e+01`. (The value 15.96 was a rounding
in the knowledge-base card, not in this file.) All other entries of the T5 tables agree with
`f2_t5_endpoint.out`. The h = 0.24 numbers in lines 301-306 (the `Ymax` scan at `Y = 10` and the
A-side triple) are in no saved output file, except the `Ymax = Y = 10` values in
`f2_t4_h024.out`. They are left as they are.
