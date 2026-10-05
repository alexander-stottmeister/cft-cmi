# Brief G3 — the corner kernel Ghat(Delta) in two independent frames (launched 2026-10-03)

## 1. Role
Track agent (numerics; not a referee). `KB_ACTOR=G3`, every kb command `-p cft_cmi`, model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it). Never run git or ./pgit.

## 2. Object
Read, in this order: rigor/phase6_brief.md ("Setting and conventions"; W2 and the track G3 paragraph),
numerics/optimality_all/f3_t0.py (T0 modular frame: mesh, Qmat from kkt_continuum.py, closed-form ddot, g_Q via
f3_gal.theta's g0), numerics/optimality_all/F3_RESULTS.md (h-ladder, order h^0.77, Ymax study, g_Q(ddot)/f2 = 0.990 at
h = 0.02), numerics/defect_matrix.py ('first' and 'exact' kernels in the box frame, graded mesh) and
numerics/compression_box.py (Q_box, fid_relent, qfi_c2; the f2 = c2/zeta^2 check in its __main__),
rigor/network_corner_calculus.tex lem:field, lem:density, thm:corner (strength zeta = kappa beta_I(p); two corners),
rigor/certified_numerics.tex (box ladders Lam 60/120, kappa_max 30/45/60, tail weight). Cards (`kb -p cft_cmi show ID`
after `kb -p cft_cmi summary`): phase6-plan, corner-correlation-kernel, network-second-order-law, const-f2,
theta-value (if present: `kb -p cft_cmi q --text theta`), certified-numerics, dhat-quadrature-certification;
common lessons discretisation-faithfulness and taper-dependence-of-first-order-constants (`kb -p common show ID`).
Status file: rigor/PHASE6_STATUS.md.

## 3. Deliverable: numerics/networks/corner_kernel.py, outputs beside it, numerics/networks/KERNEL_RESULTS.md
Quantity: R(Delta) := Ghat(Delta)/Ghat(0) with G(Delta) = g_Q(delta_0, delta_Delta), the real bilinear form of the
quadratic form g_Q(delta) = (1/4) sum_ij |delta_ij|^2/(w_i(1-w_j) + w_j(1-w_i)) (eigenbasis of Q), delta_Delta = the
y-translate by Delta of the first-order corner defect. Grid fixed now: Delta in {0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8}.
Tolerance fixed now: the two frames agree if |R_T0 - R_box| <= 1e-3 at each Delta (3 digits); else a diagnosis, not a
failure report: which modes each discretisation resolves, which it cuts off, and the weight of the cut-off modes.
K0 Validation FIRST: (a) T0 frame: g_Q(ddot)/f2 on the h-ladder 0.24, 0.12, 0.06, 0.03 (Y = 6, Ymax = 20) reproduces
   F3_RESULTS (0.990 at h = 0.02 is the published value; report yours); (b) the bilinear code at Delta = 0 equals g_Q
   to 1e-12; (c) box frame: 'first' kernel at one corner gives f2 = c2/zeta^2 at (Lam, kappa_max) = (60, 30) and
   (120, 45) as in compression_box.__main__ and certified_numerics. Save numerics/networks/kernel_validate.out.
K1 T0 frame: delta_Delta from ddot(y1 - Delta, y2 - Delta) on the same mesh (Y >= Delta + 6, Ymax >= Delta + 10);
   R(Delta) on the h-ladder 0.24, 0.12, 0.06, 0.03; fits 1/L, log L, h^p in h (measured p); extrapolate only in h;
   uncertainty = spread across admissible fits (residuals at the three finest h within 1e-4). Report also Ymax
   dependence at the largest Delta (two Ymax values).
K2 Box frame, independent: two 'first' kernels in one box, corner 1 at (a, L) and corner 2 at (a + p', L - p') with
   p' chosen so that the modular separation is Delta (beta_I and y of phase6_brief; write the formula for p'(Delta)
   and verify it numerically against lem:density), the same box (Lam, kappa_max) and graded mesh; the bilinear form in
   the eigenbasis of Q_box (polarise qfi_c2: (c2(D1 + D2) - c2(D1 - D2))/4 AND the direct bilinear sum; both must
   agree to 1e-10); ladders (Lam, kappa_max) in {(60,30), (120,45), (120,60)} as certified_numerics; report the box
   cut-off weight at each Delta.
K3 Decay and sign: fit R on Delta in [3, 8] to A e^{-alpha Delta} and A Delta^b e^{-alpha Delta}; report alpha with
   the spread; the sign of R(Delta) is established only where |R| exceeds its uncertainty (both frames).
K4 Finite zeta, two corners (box frame, 'exact' composite kernel sqrt(Phi'(x) Phi'(y)) Q(Phi(x), Phi(y)) - Q(x, y)
   for the composite Phi = k_1 o k_2 of two parabolic compressions, then compression_box.fid_relent): Phi_2(zeta,
   Delta) - Phi_A(zeta_1) - Phi_A(zeta_2) - 2 zeta_1 zeta_2 G(Delta) at zeta_1 = zeta_2 in {0.05, 0.1, 0.2}, Delta in
   {1, 2, 4}, and clustering Phi_2 -> Phi_A + Phi_A at Delta = 8; Phi_A from the single-corner 'exact' kernel on the
   same box (same code path, so discretisation errors cancel at first order; say so in the header).
Priority K0, K1, K2, K3, K4. Every output file header states resolution, resolved and cut-off modes, their weight.
G1b derives in parallel the continuum formula Ghat = cosine transform of a spectral density and a quadrature value
(rigor/g1b_kernel.out, if it appears before you finish): compare, but never fit to it or to any closed form.

## 4. Conventions: rigor/phase6_brief.md "Setting and conventions"; T0 frame I = (-inf, 1), y = -log(1-x), ddot as in
f3_t0.py; box frame xi = log((x+a)/(L-x)) as in defect_matrix.py; zeta = kappa beta_I(p); Ghat(0) = f2 = 1/(12 pi^2).
Write every frame conversion you use once in KERNEL_RESULTS.md and cite it.

## 5. Working results (UNREFEREED targets): W2 of phase6_brief.md and the Statements of corner-correlation-kernel and
network-second-order-law (positivity, decay rate, sign are OPEN; no value may be read off VWZ Fig. 25).

## 6. Output paths (the only files you may create): numerics/networks/corner_kernel.py, numerics/networks/kernel_*.out,
numerics/networks/*.npz, *.log, numerics/networks/KERNEL_RESULTS.md. Import f3_t0.py, kkt_continuum.py, f3_gal.py,
defect_matrix.py, compression_box.py via sys.path; never edit them.

## 7. Environment
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/venv
(ready: numpy, scipy, mpmath, python-flint, cvxpy, clarabel, scs, pymupdf, matplotlib). Scripts read `PYTHON` else
python3 and resolve paths from `_ROOT`. Over 2 min: `nohup $V/bin/python x.py > x.out 2>&1 < /dev/null & disown`,
output in numerics/networks/; otherwise Bash timeout <= 600000 ms. No `timeout` binary; absolute paths; cwd drifts.
G2 runs in parallel on this machine: at most 4 cores for your background jobs.

## 8. KB, rules, stop conditions, report
- `kb -p cft_cmi q --text ...` before every add. One `numerical` card per K when its output exists (`KB_ACTOR=G3
  kb -p cft_cmi add result ID --title ... --area lattice-thermal --status numerical --statement "<quantity, grid,
  resolutions, digits, both frames>" --evidence num:numerics/networks/corner_kernel.py,num:numerics/networks/<file>.out
  --tags phase6,kernel`). Report only digits stable across the two finest resolutions and on which both frames
  agree; a one-frame number is "single method". The cards of §2 belong to the orchestrator: `kb note` them; status
  changes go under NEEDS ORCHESTRATOR. `kb -p cft_cmi lint` before the final message.
- File first: corner_kernel.py skeleton and KERNEL_RESULTS.md with every K heading and PENDING within your first 3
  tool calls; appends <= 100 lines / 12,000 characters, run after each; chat <= 5 lines; reason only to the next call.
- Stop (write what you have, then report) on every §9 trigger, in particular: K0 fails; the two frames disagree beyond
  1e-3 after one diagnostic attempt (report the diagnosis); R(Delta) > 1 at some Delta in both frames (contradicts
  positive-definiteness: `kb note` corner-correlation-kernel with the evidence).
- Final message: §8 format (FILES, KB, FINDINGS, NUMBERS, NOT DONE, NEEDS ORCHESTRATOR), at most 400 words.
