# Referee brief REF-P6-5 — G3's kernel numerics and its five cards (2026-10-03)

## 1. Role
Referee. `KB_ACTOR=REF-P6-5`, every kb command `-p cft_cmi`, model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it). Never git, never ./pgit, never
edit a reviewed script, output or card text (§1: only `kb verdict`, `kb note`, `kb set ID evidence=` for a wrong
locator). Stance: adversarial; the burden of proof is on the scripts, the outputs and the cards. A rerun of a reviewed
script writes ONLY into your own files (rigor/ref_p6_5_*), never onto numerics/networks/kernel_*.

## 2. Object
Under review: numerics/networks/corner_kernel.py, numerics/networks/KERNEL_RESULTS.md and the outputs
kernel_validate.out, kernel_t0.out, kernel_t0b.out, kernel_t0_fits.out, kernel_box.out, kernel_boxb.out,
kernel_box_fits.out, kernel_decay.out, kernel_k4.out, kernel_k4b.out, kernel_k4_validate.out (+ .npz, .log) by track
G3 (brief rigor/phase6_g3_brief.md). Cards under verdict (`kb -p cft_cmi show ID` after `kb -p cft_cmi summary`; read
the Notes first): corner-kernel-pipeline-validation, corner-kernel-t0-frame, corner-kernel-box-frame,
corner-kernel-two-frames, two-corner-remainder-finite-zeta [all numerical]. Report only (no verdict) on the accuracy of
G3's notes on corner-correlation-kernel, network-second-order-law (two notes, the second withdraws an extrapolation of
the first), dhat-quadrature-certification, corner-kernel-closed-form. Context (not under review): rigor/phase6_brief.md
"Setting and conventions" and W2; numerics/optimality_all/f3_t0.py, kkt_continuum.py, f3_gal.py; numerics/defect_matrix.py,
numerics/compression_box.py, numerics/fidelity_hp.py, numerics/line_so.py; rigor/network_corner_calculus.tex lem:field,
lem:density; rigor/g1b_kernel.out (G1b's closed form Ghat(Delta) = (1/12 pi^2)[cosh(Delta/2) - sinh^2(Delta/2) log
coth(|Delta|/4)], itself under review by REF-P6-4: use it as an independent COMPARISON, not as truth); common lessons
discretisation-faithfulness, taper-dependence-of-first-order-constants (`kb -p common show ID`).
Status file: rigor/PHASE6_STATUS.md (section "G3 result" lists G3's deviations from its brief).

## 3. Deliverable: rigor/referee_corner_kernel.tex (verdict document, `\input{rigor_preamble}`) + rigor/ref_p6_5_*.py/.out
Checklist (every item one verdict line; every number of a card Statement recomputed or reproduced):
 1. Definitions: R(Delta) = G(Delta)/G(0), G = real bilinear form of g_Q (1/4 sum Re(conj(D1_ij) D2_ij)/(w_i(1-w_j)
    + w_j(1-w_i)) in Q's eigenbasis); the translate delta_Delta(y1,y2) = ddot(y1 - Delta, y2 - Delta): is the sign of
    the shift the one that moves the corner to y = +Delta (lem:field, frame y = -log(1-x))? Does the box corner 2 at
    p'(Delta) = a L (e^Delta - 1)/(L + a e^Delta) have y_I(p') - y_I(0) = Delta and strength zeta' = zeta (recompute
    exactly from lem:density and beta_I; the card says so)?
 2. K0 reproductions: f3_t0_final.out values; results_batch3.txt:8 (0.00836978 at (60,30)); line_so.txt:4 (0.0084112 at
    (120,45)); the bilinear code at Delta = 0 vs f3_gal.theta g0 (2.1e-16); corner_kernel.box_corner vs defect_matrix.run
    (3.5e-16). Open the cited files and lines yourself.
 3. T0 frame (corner-kernel-t0-frame): re-fit the saved rung values of kernel_t0.out / kernel_t0b.out with YOUR OWN fit
    code (lin in h and h^p on the 4 finest and the 4 next rungs; residual criterion 1e-4); do the quoted estimates and
    half-spreads follow? Local exponents 0.61, 0.78, 0.94, 1.07 at Delta = 1? Ymax 20 -> 24 effect 2.3e-7? The
    diagonal test G0/f2 -> 1.00028 and what it says about the frame's bias.
 4. Box frame (corner-kernel-box-frame): the eigenvalue-window regulator above kappa_max = 30 (eps = 1e-13, 1e-12, 1e-11,
    effect <= 2e-9; equal to the unregulated value to 7.5e-11 where it exists; equal to line_so.py weights to 8.5e-6 /
    1.7e-7): §5 regulator rule -- is the comparison with a regulator-free computation on the SAME mesh reported, and is
    the card's wording exact? Envelope of kappa_max = 75 ... 120 as uncertainty (no admissible fit: oscillating
    convergence): is "uncertainty = envelope" disclosed? Lam 60 vs 120 effect 9.6e-5; diagonal cut-off weight.
 5. Two frames (corner-kernel-two-frames): recompute |R_T0 - S_box| at each Delta from the two single-frame cards'
    numbers; the midpoint/uncertainty arithmetic; "independent" (§5: different algorithm, no shared code beyond
    numpy/scipy/mpmath -- G3 declares corner_kernel.sld/bil shared at definition level: is that admissible, and is it
    disclosed?); the sign claim R/u >= 600; the decay fit alpha = 0.502 +- 0.004 (re-fit kernel_decay.out yourself).
 6. INDEPENDENT recomputation of R(Delta) at the 9 grid points with your own code and a different algorithm: the
    double integral G(Delta) = (1/4) int int |dhat_0(p,p')|^2 cos((p-p') Delta) / W(p,p') dp dp' with dhat_0 the 2-D
    Fourier transform of ddot computed numerically by you (or the brief's rho(q) formulation), W(p,p') = w(p)(1-w(p')) +
    w(p')(1-w(p)), w(p) = (1+e^{-2 pi p})^{-1}; state your quadrature tolerance (1e-7) and compare with G3's agreed values
    and with rigor/g1b_kernel.out. Report the three-way deviations.
 7. K4 (two-corner-remainder-finite-zeta): the exact composite kernel of Phi = k1 o k2 (box_composite) reduces to the
    single-corner exact kernel when one sigma = 0 (5.2e-13); the window method (fidelity_hp.py) reproduces results_A2.txt;
    the rem/zeta^3 table and the "<= 20 % over zeta" claim from kernel_k4.out/kernel_k4b.out; eps-dependence 2.2e-5;
    is "O(zeta^3)" the right wording for 3 values of zeta on one box ("on this box and at these Delta")?
 8. G3's deviations from its brief (status-file section "G3 result"): h-ladder 1/4 ... 1/128 instead of 0.24 ... 0.03;
    the regulator; fid_relent replaced by the windowed method -- each justified, each disclosed on the cards?
 9. G3's MINOR code findings: reproduce the defect_matrix.py cancellation (beta_I via L - x; 2.5e-8 of max|D| at
    (120,45); NaN in shifted frames) and compression_box.qfi_c2 = inf at kappa_max >= 45, fid_relent -log F < 0 at
    (60,30) for exact kernels. Do they affect any published number beyond the 0.0084112 -> 0.0084111 shift?
10. Cards: every Statement against the outputs (quantities, grid, resolutions, digits stable across the two finest
    resolutions, "single frame"/"both frames" labels); every evidence locator resolves; `depends`/`related` accurate;
    the notes on the four non-verdict cards accurate (report only).
Reruns: `PYTHON=$V/bin/python $V/bin/python numerics/networks/corner_kernel.py <job>` for at least K0 and one K1 rung and
one K2 box, output redirected to rigor/ref_p6_5_rerun_<job>.out; diff against G3's outputs; do not rerun jobs the
.log files show took over 20 minutes -- say so.

## 4. Conventions: rigor/phase6_brief.md "Setting and conventions"; frames as in corner_kernel.py's header and
KERNEL_RESULTS.md "Conventions and frame conversions" (check each conversion written there).

## 5. Working results: W2 of rigor/phase6_brief.md and the Statements of corner-correlation-kernel and
network-second-order-law are UNREFEREED; G1b's closed form is under review by REF-P6-4.

## 6. Output paths (the only files you may create): rigor/referee_corner_kernel.tex and its pdflatex by-products;
rigor/ref_p6_5_*.py, rigor/ref_p6_5_*.out, rigor/ref_p6_5_*.npz.

## 7. Environment
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/venv
(numpy, scipy, mpmath, python-flint; no sympy). Scripts read `PYTHON` else python3, paths from `_ROOT`. Over 2 min:
nohup ... & disown, output in rigor/; else Bash timeout <= 600000 ms. No `timeout` binary; absolute paths; cwd drifts.
G2 and REF-P6-4 run in parallel: at most 2 cores.

## 8. Verdicts, rules, report
- Per card: `KB_ACTOR=REF-P6-5 kb -p cft_cmi verdict ID pass` (STANDS) or `... verdict ID fail --note "<repair,
  locator>"` (STANDS WITH REPAIR or FAILS). Competing verdicts as a new note; never edit a referee note.
- File first: report skeleton (one section per checklist item, PENDING) within your first 3 tool calls; appends <= 100
  lines / 12,000 characters, compile after each (pdflatex twice from rigor/; log without `^!` or undefined references;
  report the page count). Chat <= 5 lines; reason only to the next tool call.
- Stop and report on every §9 trigger.
- Final message: at most 400 words; one line per card and per checklist item, failures first, each with reason and
  locator; the three-way deviation table of item 6; `kb -p cft_cmi lint` counts; NEEDS ORCHESTRATOR.
