# Phase 4 status — exact-fidelity optimality (started 2026-09-15)

Question (kb card exact-fidelity-optimality-open): is the zero-collar geometric compression beaten in EXACT fidelity, i.e. does the
upper half -log F <= g_Q(delta)(1+o(1)) hold for the rotated channel W_s e^{-eps G_*}?

Reformulation (rigor/phase4_brief.md): the Uhlmann purification may use ANY unitary on the exterior of I = ABC (not only exterior
flows). Prescribing the channel fixes the column Z E_I of the generator; the free block is E_{I^c} Z E_{I^c}. Exterior directions
P^perp Z_e P are invisible (E_I[P, Z_e]E_I = 0), so the optimised Uhlmann bound equals the second-order functional iff the invisible
part of the channel's direction lies in the closure of the exterior directions Ext.

Results:
- Orchestrator (e0_finite_density.py): on finite hopping chains Ext = N^perp exactly (dim N = |I|^2). Reduction of the density
  question to a two-projection statement (H P-off-diagonal Hermitian, E_I H E_I = 0, E_{I^c}(1-2P)H E_{I^c} = 0 => H = 0).
- E2 (rigor/exterior_extension_numerics.tex, numerics/optimality_all/e2_*.py): in the spectral circle model Ext = N^perp exactly at
  every L; dist((1-Pi)M, Ext) = 0 to 55-70 digits; optimised UB_c/(1/2 s^2|u|^2) = 1.0000000 (the 4.3 of the fixed taper was an
  artefact); UB_rot/UB_c = 1 - theta to 5 digits; exact Fredholm determinant agrees at second order; ||Z_e||/s ~ 3 bounded in L.
- E1 (rigor/exact_fidelity_upper_half.tex, 17 pp): THEOREM closure(Ext) = N^perp (two proofs: compressed reflection Gamma' is a
  contraction without eigenvalues +-1 so the invisible remainder vanishes; twisted duality). Consequences: (UH) for every isometric
  quasi-free channel; E_rec <= (1 - theta_fr) f2 z^2 (1+o(1)); theta_fr > 0 iff E_D u E_D not self-adjoint (proved); theta_fr >= 0.30
  numerical. Referee (rigor/referee_exact_fidelity_upper_half.tex): STANDS WITH REPAIRS R1-R10, no proof-breaking issue; repairs
  being applied by E1.
Consequences applied: paper1/sec_outlook.tex optimality passages rewritten (bibitems RigorAll, RigorS10, RigorE1, RigorE2); Note 5
remark after Cor. 5.1; plan page O8 status; kb card exact-fidelity-optimality-open -> numerical (answered).
Open after Phase 4: exact value of the all-channel optimum (non-isometric channels; bracket [D_z, 0.71 f2 z^2]); analytic proof
of theta > 0; the Kubo-Mori coefficient (Phase 2b); D-hat quadrature certification; O10 networks; O11 sectors.
