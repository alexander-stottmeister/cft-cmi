# Referee report REF-P6-0 — Phase 6 plan and targets (2026-09-16)

Packet: rigor/review_packet_P6_0.md (6 pending cards). Evidence read: rigor/phase6_brief.md (unrefereed),
paper1/sec_petz.tex (Def. zeta, Thm normal), paper1/sec_setting.tex (z, eta), continuum_petz_free_fermion.tex
(eq. h-s, k-s, J-s), numerics/optimality_all/f3_t0.py + f3_t0_final.out, refs/VWZ_2307.14434.pdf Sec. 5.
Scripts (+.out): rigor/ref_p6_0_{calculus,field_exact,w1_counterexample,separation}.py.
## Verdicts
| card | verdict |
|---|---|
| corner-calculus | **FAIL** — universal quantifier false (union conditioning region); "equals" -> "up to a global Moebius map" |
| network-second-order-law | **FAIL** — separation constraint needs ALL corners weak; sharp constant measured (2/eps) |
| vwz-protocol-ordering | **FAIL** — 1:2:4 hides the unproved Ghat(Delta)->0; VWZ quote incomplete |
| corner-correlation-kernel | PASS (notes) |
| phase6-plan | PASS (notes) |
| multi-interval-networks | PASS (notes) |
## Checks that PASSED (exact unless stated)
1. **First-order field is EXACT.** Rational identity `-(x-p)^2/beta_I(x) == -beta_I(p)(X/X_p - 2 + X_p/X)`,
   `X=(x-p_1)/(p_{n+1}-x)`, 50 000 random rational configurations, 0 failures; plus `-4 sinh^2(u/2) = -(e^u-2+e^{-u})`.
   So the field is exactly `zeta w(y-y_p) d/dy`, `zeta = sigma beta_I(p)`; for `I=(-a,L), p=0, sigma=s/L` this is
   `zeta = a s/(a+L)` (Def. zeta). The `(-1)`-density law `sigma' = sigma/M'(p)` checks to 3e-6 (float).
   [ref_p6_0_calculus.py's first line reports a spurious 6.7e-3 "FAIL" — pure cancellation at `x -> p`; superseded.]
2. **Schwarzian.** jump `[h''/h'](p) = -2 sigma` for a compression toward `p` from EITHER side (same sign), so
   `kappa = sigma > 0`; composition `S(f o g) = S(g) + (g')^2 S(f) o g` used correctly. The pullback of a delta
   carries a factor `H'(x_0)`, `= 1` iff the inner map fixes the corner with derivative 1 — see F1.
3. **Same-point addition.** `R(s1) o R(s2) = R(s1+s2)` exactly; `L(s1) o R(s2) = M_{-s1} o R(s1+s2)` and
   `R(s2) o L(s1) = M_{s2} M_{-(s1+s2)} o R(s1+s2)` (max |diff| 9e-16), both with jump `-2(s1+s2)`; the Moebius factor
   is pole-free on the image (pole at `1/sigma_1 >` max image). Protocol 3 in either order -> same state.
4. **VWZ 1(B) = 1(A).** `2c/(b(b+c)) + 2d/((b+c)(b+c+d)) = 2(c+d)/(b(b+c+d))` identically, and the two point maps are
   LITERALLY equal (max |diff| 2e-16), not merely modulo Moebius. Faithful to VWZ ("...gives rise to exactly the same
   final state on ABCD"). Protocol 3: both corners at `p_3`, `sigma_1 = 2a/(b(a+b))`, `sigma_2 = 2d/(c(c+d))`,
   `zeta_eff = (sigma_1+sigma_2)(a+b)(c+d)/(a+b+c+d)`. Protocol 2: corners at `p_2, p_3` as claimed.
5. **Amplification.** `beta_I(p)/beta_{I_step}(p) = (T-u)v/(T(v-u)) = 1 + u(T-v)/(T(v-u)) = 1 + z'`; `z'` IS the cross
   ratio of `(p_1,p,far,p_{n+1})` AND equals `z = ac/(b(a+b+c))` of the coarse triple (20 000 rational cases, 0 bad);
   `>= 1`, `= 1` iff last step.
6. **L->R chain.** `e^{Delta_k}=(1+u_k)(1+v_k)` and `zeta_k^(I) = 2r_k(1+v_k)/((1+r_k)(e^{Delta_k}-1))` re-derived from
   `kappa_k = 2 l_{k+1}/(l_k(l_k+l_{k+1}))`, `zeta_k^(I) = kappa_k L_{k-1}(T-L_{k-1})/T` (20 000 random chains, 0 bad);
   hence `(e^{Delta_k}-1) zeta_k^(I) = 2 r_k(1+v_k)/(1+r_k) >= 2 r_k/(1+r_k)`, equality iff `v_k = 0`.
7. **VWZ symmetric setup.** `eta = a/(a+2b)` IS VWZ (5.9) at `L_A=L_D, L_B=L_C`. Exact: single step `zeta = a/b`;
   Protocol 2 `zeta_2^(I) = a(a+2b)/(2b(a+b))`, `zeta_3^(I) = a/b`; Protocol 3 `zeta_eff = 2a/b`;
   `e^{Delta_23} = (a+2b)/a = 1/eta`. All -> `2eta, 2eta, 2eta, 4eta`.
8. **Consistency.** `Ghat(0) = 1/(12 pi^2)` is supported by f3_t0.py's own output `g/f2 = 0.91158 ... 0.99019` at
   `h = 0.24 ... 0.02` (f3_t0_final.out); the quoted kernel matches the f3_t0.py docstring verbatim. The law
   reproduces Theorem A for one corner, coherent addition for coincident corners, and is compatible with W6 since
   `|Ghat(D)| <= Ghat(0)` for a positive-definite kernel. All `related:` ids exist; no duplicate card.
## Defects
**F1 (corner-calculus).** "For ANY sequential one-sided protocol ... `kappa_k` = sum of the sigma's of all steps whose
corner is the junction `p_k`" is FALSE when a step's conditioning region `A_B` is a UNION of chain intervals — exactly
what VWZ 1(B) does (`P_{BC->BCD}`, `l_B = b+c`), which the card itself invokes. Counterexample
(ref_p6_0_w1_counterexample.out) `(l_1..l_4) = (1.3,2.1,0.9,1.7)`, start `A_2A_3`: step 1 adds `A_4` on `A_3`
(corner `p_3`, `sigma_1 = 1.452991`), step 2 adds `A_1` on `A_2A_3` (corner `p_4`, `sigma_2 = 0.201550`; image of `p_1`
= 1.996 >= `p_2` = 1.3, admissible). `Phi = k_1 o k_2` has jump `+5.4e-5` at `p_3` (NO mass) and mass `-1.947332` at
`x_0 = k_2^{-1}(p_3) = 3.200568`, `= -2 sigma_1 k_2'(x_0)`, `k_2'(x_0) = 0.670114`; total mass 71% of the claimed
`-2(sigma_1+sigma_2)`. Cause: `p_3` is interior to step 2's moving part `A_1 u A_2 u A_3`. Control with `A_B = A_2`
(single interval): both corners at `p_3`, masses add (`-3.634266` vs `-3.634274`).
REPAIR — after "For any sequential one-sided zero-collar protocol on adjacent intervals" insert "**in which every
step's conditioning region A_B is a single interval of the chain (equivalently: no earlier corner lies in the interior
of the moving part A_B u A_new — this covers VWZ 1(B), where the two corners coincide at p_2)**". With that
hypothesis the point-order argument is airtight: a junction is never interior to `A_B u A_new`, so every later step is
either the identity near an earlier corner or fixes it with derivative 1, which is what makes `H'(x_0) = 1`.
F1b (same card): "Protocol 3 ... equals the over-compressed Theorem-A map" — the POINT maps agree only up to
post-composition with a global Moebius map (literal difference up to 0.68). Write "equals, up to post-composition
with a global Moebius map, ...; hence `Phi^(3) = Phi_A(zeta_eff)` as a fidelity".

**F2 (network-second-order-law).** "admissible protocols cannot have two weak corners close at distinct points (for
the L->R chain `(e^{Delta_k}-1) zeta_k^(I) >= 2 r_k/(1+r_k)`)": the inequality is right, the sentence is not. With only
the PAIR weak the separation stays O(1) (ref_p6_0_separation.out): `zeta_2 = zeta_3 = 0.1` at `e^{Delta_2} = 1.56`
(`Delta = 0.44`) and `zeta_2 = zeta_3 = 0.01` at `e^{Delta_2} = 3.5-4.0` (`Delta ~ 1.3`), against the asserted
`1/eps = 100`; the escape buys it with a large `zeta` elsewhere. With `zeta_j <= eps` for EVERY corner the claim is
true and sharp: `min e^{Delta_k} = 2/eps` (6.75, 20.05, 66.68, 200.0, 666.7 at eps = 0.3, 0.1, 0.03, 0.01, 0.003; the
optimum saturates all `zeta_j = eps`, e.g. n=6, eps=0.01, lengths `1 : 198.4 : 2.41e4 : 3.70e4 : 470.5 : 2.37`).
REPAIR — "admissible protocols **all of whose corners are weak (zeta_j <= eps for every j)** cannot have two of them
close: `(e^{Delta_k}-1) zeta_k^(I) = 2 r_k(1+v_k)/(1+r_k) >= 2 r_k/(1+r_k)`, and `zeta_j <= eps` for all `j` forces
`e^{Delta_k} >= 2/eps` (numerically sharp, REF-P6-0 2026-09-16); with only the pair weak the separation can stay O(1)."
Also: the `o(|zeta|^2)` is stated at fixed corner positions but applied (vwz card) with `Delta -> inf` as
`zeta -> 0` — uniformity in `Delta` must be claimed; and "positive-definite" does not imply `Ghat >= 0` pointwise.

**F3 (vwz-protocol-ordering).** (a) "Hence ... -> 1 : 2 : 4" hides two dependences. 1:4 is unconditional (Theorem A:
`Phi^(1) = Phi_A(a/b)`, `Phi^(3) = Phi_A(2a/b)` exactly). 1:2 needs (i) `Ghat(Delta)/Ghat(0) -> 0` as
`Delta_23 = log(1/eta) -> inf`, explicitly OPEN on the sibling card corner-correlation-kernel (decay rate, even the
sign, open), and (ii) the conjectural network law with a remainder UNIFORM in the separation, since `eta -> 0` sends
`zeta -> 0` and `Delta -> inf` at once. Exactly
`ratio_2 = (zeta_2^2+zeta_3^2)/zeta_1^2 + (2 zeta_2 zeta_3/zeta_1^2) Ghat(log 1/eta)/Ghat(0) -> 2 + 2X`.
REPAIR — "`-log F^(1) : -log F^(3) -> 1 : 4` unconditionally (Theorem A); and, CONDITIONAL on the second-order network
law with a remainder uniform in the corner separation and on `Ghat(Delta) -> 0` as `Delta -> inf` (both open,
corner-correlation-kernel), `-log F^(2) -> 2 x -log F^(1)`, i.e. 1 : 2 : 4."
(b) VWZ quote incomplete. (5.10)-(5.11) read "`- log F^(2) ~ - log F^(3) ∝ f' c eta^2`" **"with f' < f, confirming
that the sequential recovery is less effective than the single-step case"**. The card drops "f' < f", which as written
contradicts its own `f^(2) = 2f, f^(3) = 4f` (and contradicts VWZ's own prose — their inequality and their sentence
point opposite ways). Quote it and say which half the calculus contradicts.
(c) "their single-step coefficient is already 4x the exact one (const-f2)" is convention-sensitive: VWZ's
`lambda = 0` IS the ordinary Petz, which by Def. zeta has `zeta = 2z`, so OUR prediction for THEIR quantity is
`8 f2 = 8c/(12 pi^2) = 0.0675 c eta^2` — precisely the "0.0676 c eta^2" const-f2 attributes to VWZ, and within 4% of
VWZ (2.13) "`- log F^(lambda=0) = f2 c eta^2`, `f2 ~ 0.070`". The factor 4 is exactly `(2z)^2/z^2`, i.e. the ordinary
Petz against the `s = lambda` compression. Justify or drop (this also touches const-f2).
(d) "three distinct corner measures for four intervals" is incomplete: `{p_2}` (1(A)) and `{2 x p_2}` (1(B), same
measure by the identity) also occur, and union conditioning regions give corners that are not junctions (F1).
(e) "VWZ Fig. 25 (<= 8 sites per interval)": I found no "sites" anywhere in VWZ; Sec. 2.2 uses spin chains of length
`L` (c = 0.5, 0.7, 1), App. A.5 the correlation-matrix method (~5L digits for 2L fermions). Give the locator or drop it.
## Notes on the passing cards
- **corner-correlation-kernel**: kernel, frame, `Ghat(0)`, and the spectral-density argument (`rho(-q) = rho(q)` by
  hermiticity, `G = FT(rho >= 0)` hence even and positive-definite) all check out; the no-fitting rule is faithful to
  theta-value. Say that `Ghat = g_Q(delta_0, delta_Delta)/c` is the REAL polarisation and that off the diagonal it
  presupposes W2 (only `Delta = 0` is Theorem A); "agreement to 3 digits" is optimistic (T0 converges at `h^0.77`,
  `g/f2 = 0.990` only at `h = 0.02`, 12 500 s). Code referenced exists (defect_matrix.py 'first';
  compression_box.py:41 `qfi_c2`).
- **phase6-plan**: status `active` correct, both doc tokens resolve, tracks match rigor/PHASE6_STATUS.md, "prediction
  1:2:4" honestly labelled, `zeta = kappa beta_I(p)` with `w(y) = -4 sinh^2(y/2) 1_{y>0}` exact. But the first
  sentence asserts W1 as established while the brief marks W1 "UNREFEREED — a target"; add "(W1, unrefereed target of
  G1a)" and carry F1's hypothesis.
- **multi-interval-networks**: "Not started" is accurate (PHASE6_STATUS.md: all four tracks [not started]), `next`
  concrete, all five `related` ids exist. Its 2026-09-16 note calls W1 a "Key structural fact" — same over-strong
  wording as F1.
## Not checked
No lattice/Petz numerics (G2/G3 do not exist yet); `Ghat(Delta)` for `Delta > 0` was not computed, so positivity, the
decay law and the 1:2:4 cross term are untested. Normality was checked only structurally (per-step Note 4 Thm 7.1 +
`W_{k_1} W_{k_2} = W_{k_1 o k_2}`): note that `Phi` itself is not the zero-collar map of a single inclusion, so Thm 7.1
does not apply to it directly, and in a factorisation `g o R` the image of `R` need not lie in the recovery block
(only `g o R`'s does) — harmless for the state but worth saying. "Exact recovery never occurs" further needs
"corner measure != 0 => Phi > 0", which is Theorem A for one corner and part of W2 for several.

## Second pass (REF-P6-1, 2026-09-16)
Packet rigor/review_packet_P6_1.md; new script rigor/ref_p6_1_fig25.py (+.out). PASS corner-calculus,
network-second-order-law, phase6-plan, multi-interval-networks. FAIL vwz-protocol-ordering.
- **corner-calculus**: F1's hypothesis and F1b's "up to post-composition with a global Moebius map" are in, with the
  counterexample and the `corner measure != 0 => Phi > 0` caveat. Residual (my own pass-0 wording, one word): the two
  conditions are NOT equivalent — "A_B a single chain interval" implies "no earlier corner interior to A_B u A_new",
  not conversely, and VWZ 1(B) fails the first, satisfies the second: the hypothesis excludes its own example. Write "(or, more generally, such that no earlier corner lies in the interior of a later
  step's moving part A_B u A_new — the weaker condition is the one the proof uses; VWZ 1(B) conditions on the union BC,
  so it fails the first and satisfies the second, its two corners coinciding at p_2)". Same fix in W1 and phase6-plan.
- **network-second-order-law**: all-weak hypothesis, the 2/eps constant, my numbers (20.05, 66.68, 200.0, 666.7 at
  eps = 0.1, 0.03, 0.01, 0.003), `O(eps^2 Ghat(log 2/eps))`, the uniform-remainder sentence and the "positive-definite
  does not imply Ghat >= 0" clause are correct and correctly attributed. Residual (wording): a minimisation bounds the
  minimum from ABOVE, so "forces e^{Delta_k} >= 2/eps (numerically sharp)" should read "the numerical minimum over
  L->R chains is 2/eps to 4 digits (ref_p6_0_separation.out); the bound is not proved". `Ghat(Delta_k) <=
  Ghat(log 2/eps)` also needs Ghat monotone there.
- **vwz-protocol-ordering** FAIL, one new sentence: "Fig. 25 is a rough measurement of Ghat at Delta <~ 2 (suggesting
  Ghat(Delta)/Ghat(0) ~ 1 there)". (i) Backwards: `Delta_23 = log(1/eta)`, so the axis `eta^2 <= 0.4` bounds Delta_23
  from BELOW (`>= 0.459`); `Delta_23 <~ 2.3` means `eta >= 0.1`, a claim about the smallest plotted point, not the
  axis. (ii) There `zeta_1 = a/b = 2eta/(1-eta) >= 0.22` is not small, so the second-order law — the only bridge to
  Ghat — does not apply. (iii) Impossible anyway: at second order `Phi^(2) < Phi^(3)` STRICTLY for every eta>0
  (`zeta_2+zeta_3 < 2 zeta_1 = zeta_eff`), and `Phi^(2) = Phi^(3)` needs `X = Ghat(Delta_23)/Ghat(0) = 2.14, 1.92,
  1.74, 1.57, 1.38, 1.20, 1.10` at `eta = 0.632 ... 0.05`, all > 1, excluded by positive-definiteness
  (ref_p6_1_fig25.out). REPAIR: "Fig. 25 cannot be read as a measurement of Ghat: in the eta range it probes the
  corner strengths are O(1), and Phi^(2) = Phi^(3) would need Ghat(Delta_23)/Ghat(0) > 1, which positive-definiteness
  forbids; VWZ's own statement is self-contradictory (f' < f against 'less effective'), so no value or sign of Ghat may
  be extracted — G3 must measure it directly." Same in brief W4 (l. 100, 103-105) and phase6-plan's G3 clause.
  All else is correctly repaired (1:4 / conditional 1:2 split, the full quote with "f' < f", removal of "4x" and
  "<= 8 sites", the 0.070 c vs 8 f2 = 0.0675 c sentence, the corner-measure list). Cosmetic: "middle-out worst if
  Ghat >= 0" needs no hypothesis; "1:4 UNCONDITIONALLY" is unconditional in Ghat, not in corner-calculus (open).
- **phase6-plan / multi-interval-networks**: both wording items applied, the new dated note is additive, no earlier note touched; phase6-plan's `next:` still promises REF-P6-1 "after the documents exist" — bump to REF-P6-2.

## Third pass (REF-P6-2, 2026-09-16)
Packet rigor/review_packet_P6_2.md. PASS all four (vwz-protocol-ordering, corner-calculus, network-second-order-law, phase6-plan); every REF-P6-1 residual is repaired verbatim and correctly.
- corner-calculus / phase6-plan: "or, more generally, ... the first implies the second, not conversely: VWZ 1(B)
  conditions on the union BC, so it fails the first and satisfies the second" — the logic is now right and 1(B) is
  inside the hypothesis. phase6-plan's `next:` is bumped to REF-P6-2.
- network-second-order-law: "the numerical minimum ... is 2/eps to 4 digits ...; the bound e^{Delta_k} >= 2/eps is NOT
  proved (a minimisation bounds the minimum only from above; target of G1a)" and the remainder rewritten
  `O(eps^2 sup_{Delta >= log(2/eps)} |Ghat(Delta)|)`, so no monotonicity is used. Residual (cosmetic): that "Hence ...
  at strict second order" still leans on the unproved separation bound — add "and given the separation bound" beside
  "given the uniform remainder".
- vwz-protocol-ordering: the Fig.-25 sentence is my repair text, numerically faithful (axis gives `Delta_23 >= 0.46`;
  `zeta_1 >= 0.22` for `eta >= 0.1`; `Ghat/Ghat(0) = 1.1 ... 2.1 > 1`, cf. ref_p6_1_fig25.out 1.10 ... 2.14). The new
  Cauchy-Schwarz sentence is CORRECT: `|Ghat| <= Ghat(0)` gives `Phi^(2) <= f2 (zeta_2+zeta_3)^2`, and
  `zeta_1 - zeta_2 = (a/b) a/(2(a+b)) > 0` for all a,b > 0 (exact, 200000 rational cases, 0 failures), so
  `Phi^(2) < f2 (2 zeta_1)^2 = Phi^(3)` with no sign hypothesis. `1:4` is now correctly "given the corner calculus".
