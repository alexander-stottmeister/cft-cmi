# Brief G2 — lattice sequential Petz chains and the VWZ protocols (launched 2026-10-03)

## 1. Role
Track agent (numerics; not a referee). `KB_ACTOR=G2`, every kb command `-p cft_cmi`, model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it). Never run git or ./pgit.

## 2. Object
Read, in this order: rigor/phase6_brief.md ("Setting and conventions"; W1/W3/W6 are PROVED by G1a, W2/W4 are
UNREFEREED targets; track G2 paragraph), numerics/lattice/README.md (hopping-chain dictionary: two chiralities, eta_V,
lattice/continuum ratio) and numerics/lattice/petz_lattice.py (Gaussian rotated Petz map, flint ball arithmetic,
`validate`, `recovered_G`, `fid_relent`, `exact_check`, `phi_cont`/`PHI_TAB` = continuum Phi_A table),
rigor/network_corner_calculus.tex Sec. 5, 8, 9 (thm:general, thm:corner, ex:swallow, prop:1B1A, prop:prot2, thm:prot3,
prop:startblock, tab:n4), refs/VWZ_2307.14434.pdf Sec. 5 (Protocols 1(A), 1(B), 2, 3; eqs. (5.3)-(5.5), (5.9)-(5.11),
Fig. 24-25; the PDF is the source, never memory), paper1/sec_numerics.tex (table l. 116: Phi(zeta)).
Cards (`kb -p cft_cmi show ID` after `kb -p cft_cmi summary`): phase6-plan, corner-calculus, vwz-protocol-ordering,
network-second-order-law, frame-strength-amplification, protocol-corner-data-n4-n5, vacuum-rigidity-exact-recovery,
two-branch-law-lattice, large-zeta-values, const-f2. Status file: rigor/PHASE6_STATUS.md.

## 3. Deliverable: numerics/networks/lattice_chain.py, outputs beside it, numerics/networks/NETWORK_RESULTS.md
Model: half-filled infinite hopping chain, C_ij = sin(pi(i-j)/2)/(pi(i-j)); blocks A_1..A_n of l_k sites; a one-sided
step = the Gaussian (rotated) Petz map of petz_lattice.py applied to the state produced so far, conditioning on the
sub-block the protocol names (single interval or union). Every reported number: script + saved output + exact command.
V0 Validation FIRST (tolerances fixed here): two-step protocols on n <= 10 sites against exact 2^n density matrices
   (Jordan-Wigner, as `validate`): |Delta D| <= 1e-12 (relative entropy), |Delta(-log F)| <= 1e-7; the identity
   K det(1+T~) = 1 at every step to working precision. Save numerics/networks/validate.out. No production run before.
N1 VWZ 1(B) = 1(A) (prop:1B1A, continuum identity): symmetric setup L_A = L_D = a, L_B = L_C = b sites; r_1 :=
   Phi^(1B)/Phi^(1A) at three resolutions (scale (a, b) by 1, 2, 3 at fixed eta = a/(a+2b)); fit 1/L, log L, h^p;
   criterion: the extrapolated r_1 - 1 is within the fit spread of 0 (report the spread). Run eta in {0.1, 0.2, 0.3}.
N2 Protocol 3 vs Theorem A (thm:prot3): Phi^(3)_lat / Phi_A(zeta_eff), zeta_eff = (sigma_1 + sigma_2) beta_I(p_3)
   (phase6_brief W1(ii); Phi_A from `phi_cont`, flagged if extrapolated; mind the two-chirality dictionary and the
   lattice/continuum ratio of two-branch-law-lattice); three resolutions, same fits, report the extrapolated ratio.
N3 The 1:2:4 question (vwz-protocol-ordering): Phi^(1), Phi^(2), Phi^(3) for eta in {0.05, 0.1, 0.15, 0.2, 0.3, 0.4},
   total sites up to 72 (flint bits as petz_lattice.bits_for); report Phi^(3)/Phi^(1) against Phi_A(2a/b)/Phi_A(a/b)
   (unconditional prediction) and Phi^(2)/Phi^(1) against (zeta_2^2 + zeta_3^2)/zeta_1^2 (the Ghat-free part); the
   measured excess, divided by 2 zeta_2 zeta_3/zeta_1^2, is a lattice estimate of Ghat(log 1/eta)/Ghat(0) ONLY where all
   zeta <= 0.2; label it "lattice, second order not yet reached" otherwise. Relative entropy alongside -log F.
N4 L->R Petz chains (def:LR, lem:LRdata) of 4, 5, 6 blocks with weak corners (geometric lengths l_{k+1}/l_k = r in
   {1/2, 1/3}): Phi_tot vs f2 sum_k (zeta_k^(I))^2 (second-order prediction without cross terms) vs sum_k Phi_step
   (amplification, lem:ampl); report the ratios at three resolutions.
N5 Where (H) fails (thm:general): Ex. 5.6 geometry (chain (1,1,1) scaled, start A_2, add A_3 on A_2, then A_1 on A_2):
   prediction Phi_tot = Phi(second step alone); and the REF-P6-0 geometry (lengths (1.3, 2.1, 0.9, 1.7), start A_2A_3,
   add A_4 on A_3, then A_1 on the UNION A_2A_3): prediction from the displaced mass -2 sigma_1 k_2'(x_0) delta_{x_0}
   plus the undisplaced corner, through the single-corner law. Criterion: ratio lattice/prediction -> 1 in 1/L.
N6 VWZ CMI bounds (5.3)-(5.5) and sum_k I_k along the chain; equal-block chains Phi_tot(n_blocks) for n = 2..6.
Priority N1, N2, N3, then N4, N5, N6. Each N gets its own output file and a NETWORK_RESULTS.md section with the exact
command, the resolutions, the fits and the digits stable across the two finest resolutions (§5).

## 4. Conventions: rigor/phase6_brief.md "Setting and conventions" (s = 2 lambda_geom is the ordinary Petz map = VWZ
lambda = 0; rotated maps s_t); numerics/lattice/README.md for the lattice dictionary; Phi = -log F; "eta" is VWZ (5.9)
unless written eta_V. Write every conversion you use in NETWORK_RESULTS.md once.

## 5. Working results (UNREFEREED targets): W2, W4 of phase6_brief.md; Statements of vwz-protocol-ordering and
network-second-order-law. PROVED continuum statements you test: corner-calculus, frame-strength-amplification,
protocol-corner-data-n4-n5, vacuum-rigidity-exact-recovery (all rigor/network_corner_calculus.tex, refereed).

## 6. Output paths (the only files you may create): numerics/networks/lattice_chain.py, numerics/networks/*.out,
*.raw, *.npz, *.log, numerics/networks/NETWORK_RESULTS.md. Import petz_lattice.py (sys.path), never edit it.

## 7. Environment
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/venv
(ready: numpy, scipy, mpmath, python-flint, cvxpy, clarabel, scs, pymupdf, matplotlib). Scripts read `PYTHON` else
python3 and resolve paths from `_ROOT` (repository root). Over 2 min: `nohup $V/bin/python x.py > x.out 2>&1 <
/dev/null & disown`, output in numerics/networks/; otherwise Bash timeout <= 600000 ms. No `timeout` binary; absolute
paths; cwd drifts between calls. G3 runs in parallel on this machine: at most 4 cores for your background jobs.

## 8. KB, rules, stop conditions, report
- `kb -p cft_cmi q --text ...` before every add. One `numerical` card per N when its output exists (`KB_ACTOR=G2
  kb -p cft_cmi add result ID --title ... --area lattice-thermal --status numerical --statement "<quantity, range,
  resolutions, digits>" --evidence num:numerics/networks/lattice_chain.py,num:numerics/networks/<file>.out --tags
  phase6,lattice`). Weakest status the evidence supports; estimates with uncertainty = spread across admissible fits.
  The cards of §2 belong to the orchestrator: `kb note` them; status changes go under NEEDS ORCHESTRATOR.
  `kb -p cft_cmi lint` before the final message.
- File first: lattice_chain.py skeleton and NETWORK_RESULTS.md with every N heading and PENDING within your first 3
  tool calls; appends <= 100 lines / 12,000 characters, run after each; chat <= 5 lines; reason only to the next call.
- Stop (write what you have, then report) on every §9 trigger, in particular: V0 fails; a proved continuum statement
  (N1, N2, N5) is contradicted beyond the fit spread after one diagnostic (then `kb note` the card, never its status);
  a working result of §5 is false (report the counterexample; do not redesign).
- Final message: §8 format (FILES, KB, FINDINGS, NUMBERS, NOT DONE, NEEDS ORCHESTRATOR), at most 400 words.
