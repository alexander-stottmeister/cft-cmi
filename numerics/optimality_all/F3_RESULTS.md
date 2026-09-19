# F3 (Phase 5): reconciliation of the first-order gain constant theta

theta := sup_G cos^2(u, v_G)   (S10 eq:theta), u = visible compression defect,
v_G = E_I[G,P]E_I projected, G anti-self-adjoint supported in D.

**Verdict (short).**  The two published numbers do **not** have different limits.  The modular
Galerkin frame is right and the S10 spectral-circle number is a **taper-suppressed lower bound**:
the ultraviolet smoothstep taper that S10 puts on the spectral derivative (to kill the periodic
grid's second Fermi point) removes exactly the modes that carry ~20% of theta.  Running the
*same* modular-Galerkin functional on the *circle model's own mesh* (no taper, exact continuum
defect kernel) reproduces the Galerkin values, not the circle ones.  The reconciled value is

        theta = 0.384 +- 0.003      (h -> 0, measured order h^0.77, five mesh families)

so 1 - theta = 0.616 +- 0.003.  S10's 0.300 +- 0.005 is a lower bound, and the Galerkin table of
`optimality_all_channels.tex` Sec. 5.2 (0.286 ... 0.336, "at least 0.30, plausibly 0.34-0.40")
confirmed and sharpened.

All scripts have prefix `f3_` in `numerics/optimality_all/`; the original scripts were not edited.
Environment: `$V/bin/python` with V as in the Phase-5 brief.

## 0. Reproduction of the published numbers (f3_smoke.py, f3_smoke.out)

| frame | published | reproduced | CG converged? |
|---|---|---|---|
| Galerkin `theta_galerkin.py` h=0.3, Lam=12, s=0.1, first | 0.299 | 0.29926 | yes, flat from k=200 (ran to 843) |
| circle `s10_diag.py` L=256, uv=(0.30,0.42), cap=1e10 | 0.2895 | 0.28958 | yes, flat from k=50 |
| circle L=128 | - | 0.29118 | yes |

Both published numbers are *converged* sups over their respective finite-dimensional G classes;
the discrepancy is **not** a CG-convergence artefact.  `f3_gal.py` reimplements the Galerkin
operator in the Q-eigenbasis (A(G) = 1/4 antiherm(Uh^dag [K o (Uh G Uh^dag)] Uh),
K_ij = (q_i-q_j)^2 w_ij) and reproduces the whole published table to 5 digits (0.28578, 0.29926,
0.31418, 0.32367, 0.33620 at h=0.4...0.15, plus gQ/(f2 zeta^2) = 0.86867...0.94934).

## 1. What theta is sensitive to (Galerkin frame, a=1, L=2, s=0.1, kernel 'first')

Meshes: `uni=1` = cells of width exactly h everywhere with the corner xi0 = log(a/L) exactly on
the grid (the B|C boundary is numerically irrelevant: delta_c couples A to D=BC and G lives on all
of D).  This removes the h_B jitter of `kkt_continuum.mesh` and gives a clean h-ladder.

**(a) Modular cutoff Lambda: irrelevant.** (f3_gal_lamsmall.out, f3_gal_lam.out)

| Lambda | 3 | 4 | 5 | 6 | 8 | 12 |
|---|---|---|---|---|---|---|
| theta (h=0.12) | 0.33974 | 0.34098 | 0.34168 | 0.34218 | 0.34277 | 0.34350 |
| theta (h=0.06) | 0.35757 | 0.35842 | 0.35889 | 0.35919 | 0.35960 | 0.36007 |

Truncating the modular window at Lambda is a *Moebius-equivalent geometry* (it moves the outer
endpoints of I), so theta is Lambda-independent to ~0.002 already at Lambda=3, and to 0.0005 from
Lambda=8 on.  (f3_mimic.py deep: pushing the right modular window from xi=5.8 to xi=261 moves
theta by +0.001.)  **Lambda is not the knob.**

**(b) Mesh width h: the only knob.**  (f3_gal_uni.out, f3_gal_hsweep.out)

| h | 0.32 | 0.24 | 0.16 | 0.12 | 0.08 | 0.06 | 0.04 |
|---|---|---|---|---|---|---|---|
| theta | 0.29797 | 0.31518 | 0.33357 | 0.34350 | 0.35423 | 0.36007 | 0.36644 |
| gQ/(f2 zeta^2) | 0.89097 | 0.91753 | 0.94562 | 0.96010 | 0.97465 | 0.98178 | 0.98878 |

(gQ -> 1 linearly in h, deficit ~ 0.33 h, as required by Theorem A.)

**(c) Kernel and geometry.**  'exact' vs 'first' kernel at h=0.1: 0.34635 vs 0.34843 (0.6%).
Geometry independence: see Sec. 4.

## 2. Where theta lives: phi(Delta) (f3_phi_gal.out, f3_class_win.out)

phi(Delta) := theta with G restricted to modular distance >= Delta from the far endpoint of D
(x = L, the common endpoint of D and I).  Delta is a Moebius-invariant label; phi(0) = theta.

| Delta | 0 | 0.25 | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 4.0 | 6.0 | 8.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| h=0.12 | 0.34277 | 0.26541 | 0.25825 | 0.24995 | 0.24352 | 0.23599 | 0.22331 | 0.20856 | 0.16507 | 0.09709 |
| h=0.06 | 0.35960 | 0.27653 | 0.27002 | 0.26112 | 0.25476 | 0.24867 | - | - | 0.17563 | 0.10837 |

Two facts: (i) ~23% of theta comes from G supported in the *last* modular unit at the endpoint of
D -- this is S10 Sec. 10's "G_* lives in the ultraviolet", now quantified; (ii) that endpoint
piece is already saturated at coarse h (f3_ep_K.out: subdividing the last cell geometrically down
to width 3e-5 moves theta by +0.0003), so the h-dependence of theta is a **bulk** effect, spread
over the whole modular window, not an endpoint-resolution effect.

## 3. T0: the parameter-free Wiener-Hopf frame (F1 Prop. 6.2, `prop:thetaframe`)

`f3_t0.py`.  I = (-inf,1), A = (-inf,0), D = (0,1), y = -log(1-x).  Q is the Fourier multiplier
(1+e^{-2 pi p})^{-1}; in the piecewise-constant **cell** basis of y its matrix elements are exact
(`kkt_continuum.Qmat`).  For the defect I use the closed form obtained by sending a -> infinity,
L = 1 in S11's first-order kernel R_s^(1) = (s/L) u v/(u+v)^2 with x = 1-e^{-y}
(half-density factor sqrt((1-x_1)(1-x_2)) = e^{-(y_1+y_2)/2}):

**delta-dot(y1,y2) = -(i/2 pi) sinh(y1/2) sinh(y2/2) / sinh^2((y1-y2)/2) + h.c.,   y1 < 0 < y2**

(parameter-free; consistent with w(y) = -4 sinh^2(y/2), since sinh(y/2) = sgn(y) sqrt(-w/4)).
Tail: ~ e^{y1} e^{-y2/2} as y2 -> +infinity.  Normalisation check: g_Q(delta-dot)/f2 -> 1.

**(a) A-side cutoff Y and quadrature: exactly converged.**  (f3_t0_Y.out, f3_t0_ng.out)
theta = 0.33998, 0.34215, 0.34235, 0.34236, 0.34236, 0.34236, 0.34236 for Y = 2,4,6,8,10,14,20
(h=0.12, Ymax=10) -- flat from Y=6 to 5 digits.  Gauss-Legendre order ng = 6,10,16,24: identical
to 5 digits.  So the only two knobs are h and **y_max**.

**(b) y_max (the moving endpoint x=1) converges.**  (f3_t0_ymax.out, f3_t0_ymax2.out)

| y_max | 2 | 4 | 6 | 8 | 10 | 12 | 16 |
|---|---|---|---|---|---|---|---|
| theta (h=0.12) | 0.31783 | 0.33519 | 0.33985 | 0.34154 | 0.34236 | 0.34291 | 0.34357 |
| g/f2 | 0.70597 | 0.91898 | 0.95443 | 0.95925 | 0.95989 | 0.95999 | 0.96000 |

The denominator g_Q(delta-dot) saturates at y_max >= 12; theta keeps creeping with increments
per unit y_max of 8.7e-3, 2.3e-3, 8.5e-4, 4.1e-4, 2.8e-4, 1.65e-4 -- i.e. an approximately
geometric tail, extrapolating to theta(y_max=inf) - theta(y_max=16) ~ +7e-4 at h=0.12.
**y_max converges**; it is worth about +0.002 relative to y_max=10 and is the smaller of the two
systematics.  (Independently: in the (a,L)=(1,2) Galerkin frame the same statement is
Lambda-independence, Sec. 1(a), because truncating the modular window is a Moebius-equivalent
geometry; and f3_mimic deep pushes the window to y = 261 for +0.001.)

**(c) T0 reproduces the Galerkin frame at matched h** (different geometry a=inf,L=1 vs a=1,L=2;
Moebius covariance):

| h | 0.32 | 0.24 | 0.16 | 0.12 | 0.08 | 0.06 |
|---|---|---|---|---|---|---|
| T0 (Y=Ymax=10) | 0.29622 | 0.31367 | 0.33225 | 0.34236 | 0.35334 | 0.35934 |
| Galerkin (a=1,L=2,Lam=12) | 0.29797 | 0.31518 | 0.33357 | 0.34350 | 0.35423 | 0.36007 |

agreeing to ~0.001 (the residual is the y_max/Lambda systematic of (b)).  **The Galerkin number
is therefore confirmed by an independent, geometry-free discretisation.**

## 4. The Richardson closure (f3_close.py)

**(i) The y_max systematic obeys theta(y_max) = theta_inf - c(h)/y_max** (least squares on 1/y_max,
max residual 1.5e-5 over y_max = 10...40):

| h | theta_inf | c |
|---|---|---|
| 0.12 | 0.34552 | 0.0315 |
| 0.06 | 0.36140 | 0.0208 |

c(h) ~ h^0.60.  Every ladder below is corrected by +c(h)/y_max.  The correction is validated by the
fact that it maps the y_max=10 and the y_max=20 T0 ladders onto each other to 1e-4
(e.g. h=0.06: 0.35934+0.00208 = 0.36142 vs 0.36036+0.00104 = 0.36140).

**(ii) Measured convergence order.**  Successive increments on octave ladders have ratio
rho = 0.577...0.592 per family (A: 0.581-0.591, B: 0.581, 0.591, C: 0.577, 0.588, C': 0.592,
D: 0.570-0.606; i.e. **p = log2(1/rho) = 0.77 +- 0.02**, *not* 1 and not 2), stable over four
octaves from h = 0.32 down to h = 0.015 in every family.  The order is fractional because the
defect kernel is homogeneous of degree 0 at the corner y=0; corner-graded meshes confirm this
(f3_t0.py grade: at h=0.12 geometric corner refinement with K levels gives theta = 0.34290,
0.35288, 0.35701, 0.35858, 0.35914, 0.35946, 0.35956 for K = 0,2,4,6,8,12,16 -- **saturating**, and
equal to the uniform mesh at h ~ 0.058).

**(iii) Extrapolation** theta_inf = theta(h_min) + Delta * rho/(1-rho):

| family | ladder | rho | theta(h_min) | theta_inf |
|---|---|---|---|---|
| A T0 uniform, Y=Ymax=10 | h=0.32...0.02 | 0.581, 0.590, 0.590 | 0.37442 | **0.38436** |
| A T0 uniform, Y=Ymax=10 | h=0.24...0.015 | 0.588, 0.591, 0.587 | 0.37635 | **0.38421** |
| B T0 uniform, Y=6, Ymax=20 | h=0.24...0.03 | 0.581, 0.591 | 0.37078 | **0.38431** |
| C Galerkin (a=1,L=2), Lam=12 | h=0.32...0.04 | 0.577, 0.588 | 0.36750 | **0.38415** |
| C' Galerkin (a=1,L=2), Lam=8 | h=0.12...0.03 | 0.592 | 0.37082 | **0.38444** |
| D mimic (circle mesh, a=2,Lg=1) | 1/L=1/128...1/2048 | 0.606, 0.587, 0.570 | 0.37893 | 0.38369 (+~0.001 window) |

Spread over families and fit windows: 0.3835-0.3847.  Sensitivity to the assumed tail ratio:
rho in [0.55, 0.62] moves family A(0.015) over [0.3831, 0.3854].  Hence

> **theta = 0.384 +- 0.003**

T0 (geometry-free Wiener-Hopf frame, a = infinity) and the Galerkin frame (a=1, L=2) agree to
3e-4 after the y_max/Lambda correction -- well inside the error bar.

**(iv) Geometry independence** (Moebius covariance; f3_gal_misc.out, f3_mimic_geom.out, T0 itself):

| frame | (a,L) | theta |
|---|---|---|
| Galerkin h=0.1, Lam=12 | (1,2) | 0.34843 |
| Galerkin h=0.1, Lam=12 | (2,1) | 0.34894 |
| Galerkin h=0.1, Lam=12 | (1,4) | 0.34854 |
| Galerkin h=0.1, Lam=12, s=0.3 | (1,2) | 0.34863 |
| T0 (h=0.1, Y=Ymax=8) | (inf,1) | 0.34695 |

Spread 5.1e-4 over the four Galerkin rows (same code, same h, same Lambda) and 2.0e-3 over the
whole table including the T0 (inf,1) row -- the extra spread is the frame change (T0 uses
Y=Ymax=8, worth about -1.5e-3 by the y_max law of (i)), not the geometry.  theta is geometry- and
s-independent, as Moebius covariance requires.  Kernel 'exact' vs 'first' at h=0.1: 0.34635 vs 0.34843 (0.6%, an O(s) effect at s=0.1;
irrelevant for the first-order constant).

## 5. Why S10's circle number is different: the ultraviolet taper

**(a) The circle model does not converge.**  (f3_circ_L.out, fast solver f3_circ2.py, validated
against `s10_diag.py`)  With S10's taper uv=(0.30,0.42), a=2, Lg=1, cap=1e10:

| L | 128 | 192 | 256 | 320 | 384 | 512 | 640 | 768 | 896 | 1024 |
|---|---|---|---|---|---|---|---|---|---|---|
| theta | 0.29118 | 0.28886 | 0.28958 | 0.29114 | 0.29251 | 0.29511 | 0.29723 | 0.29898 | 0.30046 | 0.30173 |
| xi_max of D | 4.12 | 4.52 | 4.81 | 5.03 | 5.21 | 5.50 | 5.72 | 5.91 | 6.06 | 6.19 |

theta is *not* a function of 1/L: it is non-monotone below L=256 and then rises linearly in
**log L** (= the modular window reached, d theta/d log L = 0.0096 per unit, flat from L=384 to
1024).  S10's Richardson in 1/L over L=256,384,512 uses the wrong variable; the model would need
xi_max ~ 14.7, i.e. L ~ 5e6, to reach 0.384.

**(b) The taper is the mechanism.**  (f3_circ_taper2.out, L=256)

| taper window uv | (0.20,0.32) | (0.30,0.42) | (0.35,0.47) | (0.42,0.49) | (0.46,0.499) | none | none, cap 1e6 |
|---|---|---|---|---|---|---|---|
| theta | 0.27762 | 0.28958 | 0.36178 | 0.72688 | 0.54681 | 0.17175 | 0.17176 |
| \|u\|^2 | 0.007385 | 0.007387 | 0.007733 | 0.027306 | 0.626909 | 0.014889 | 0.014888 |

theta rises monotonically as the taper is relaxed until the periodic grid's **second Fermi point**
(nu ~ +-L/2) takes over and destroys \|u\|^2 (x3.7, x85, x2).  There is **no taper-free limit** in
this model: the untapered lattice is not a chiral fermion in the ultraviolet.  The window
(0.35,0.47), which S10 discards as "contaminated" (\|u\|^2 4.7% off), already gives 0.362 -- the
correct order of magnitude.  The cap is irrelevant (1e6 vs 1e10: 5 digits).

**(c) Direct proof that it is the taper and not the mesh.**  (f3_mimic.py)  Run the *modular
Galerkin* functional (exact vacuum symbol in closed form, exact continuum defect kernel, no taper,
no cap) on the **circle model's own mesh** -- cell edges at the xi-midpoints of the grid points
theta_j = 2 pi j/L mapped through xi = log((x+a)/(Lg-x)), x = tan(theta_j/2):

| L | 128 | 256 | 512 | 1024 | 2048 |
|---|---|---|---|---|---|
| theta (circle mesh, no taper) | 0.34058 | 0.35830 | 0.36904 | 0.37534 | 0.37893 |
| theta (circle model, S10 taper) | 0.29118 | 0.28958 | 0.29511 | - | - |

Same mesh, same geometry, same |D|: 0.379 vs 0.295.  **The mesh is not the problem; the taper is.**
(The circle mesh is in fact an efficient mesh -- it extrapolates to 0.3837+0.001, family D above.)

**Conclusion.** S10 Sec. 7(c)'s theta = 0.300 +- 0.005 is a **taper-suppressed lower bound**, not
an estimate of theta: the smoothstep taper on the spectral derivative removes precisely the
ultraviolet modes near the moving endpoint that carry ~20% of theta (cf. phi(Delta), Sec. 2).  All
qualitative conclusions drawn from it (theta > 0, condition (S) fails, the compression is not the
second-order minimiser, E^(2) <= (1-theta) f2 z^2) are unaffected and in fact strengthened:
1 - theta = 0.616 +- 0.003 instead of 0.70.

## 6. Closed-form candidates (T4)

Window from Sec. 4: theta in [0.381, 0.387] (width 0.006).  **26** candidates were tested
(`f3_candidates.py`, output `f3_candidates.out`); 3 fall inside:

| candidate | value | verdict |
|---|---|---|
| 3/pi^2 | 0.303964 | **excluded** |
| (pi^2-6)/12 | 0.322467 | **excluded** |
| 1/3 | 0.333333 | **excluded** |
| 1-2/pi | 0.363380 | **excluded** |
| 1/e | 0.367879 | **excluded** |
| 3/8 | 0.375000 | **excluded** |
| 1 - pi^2/16 | 0.383150 | inside |
| 2 ln 2 - 1 | 0.386294 | inside |
| 2/pi - 1/4 | 0.386620 | inside |
| 7/18 | 0.388889 | excluded (marginal) |
| pi/8 | 0.392699 | **excluded** |
| 2 - 12/pi^2 | 0.784146 | **excluded** |

(also excluded: pi^2/8-1, 1-2/e, 4/pi-1, 1-1/(2 ln2), 3-e, pi^2/6-4/3, 1/2-1/(2pi),
1-pi/8-1/4, (4-pi)/(pi-1), pi^2/24, 1/(2 ln2)-1/4, (ln 2)^2, 1-3/(2pi), ln2/(2-ln2)).

**No selection is made.**  With 26 candidates spread over [0.2337,0.7841] (range 0.5504) and a
window of width 0.006, 0.28 hits are expected by chance and 3 were found; the candidate list is moreover not uniform (it
clusters in 0.25-0.45).  The central value 0.3842 is 0.0011 above 1-pi^2/16 and 0.0021 below
2 ln 2 - 1; neither is favoured.  A closed form must come from solving the Wiener-Hopf problem
\eqref{eq:thetaWH}, not from fitting.

## 7. Reproduce

```
V=<venv>;  cd numerics/optimality_all
$V/bin/python f3_smoke.py                 # reproduces theta_galerkin.py 0.299 and s10_diag.py 0.2895
$V/bin/python f3_t0.py smoke              # T0 Wiener-Hopf frame, h=0.4,0.2,0.1
$V/bin/python f3_t0.py Y ; ... ymax ; ... ymax2 ; ... ng    # Y, y_max, quadrature convergence
$V/bin/python f3_t0.py hladder ; ... hladder2 ; ... final   # the h-ladders (hours at h<=0.02)
$V/bin/python f3_t0.py grade              # corner-graded mesh (saturates in K)
$V/bin/python f3_gal.py uni ; ... ladder8 ; ... lamsmall ; ... misc
$V/bin/python f3_phi.py gal               # phi(Delta)
$V/bin/python f3_mimic.py main ; ... big ; ... deep ; ... geom
$V/bin/python f3_circ2.py Lsweep ; ... taper      # circle model (fast solver)
$V/bin/python f3_close.py                 # the y_max law, the measured order, the Richardson closure (Sec. 4)
$V/bin/python f3_candidates.py > f3_candidates.out   # the 26-candidate closed-form test (Sec. 6)
```
Long runs: `nohup $V/bin/python f3_x.py job > f3_x_job.out 2>&1 < /dev/null & disown`.
