# Phase 4 brief — is the geometric compression beaten in EXACT fidelity? (2026-09-15)

## State (kb -p cft_cmi show exact-fidelity-optimality-open)
Per chirality, E_rec := inf over recovery channels of -log F(omega, omega^beta) satisfies
  D_z (1-o(1)) <= E_rec <= f2 z^2 (1+o(1)),      D_z = min_F g_Q <= (1 - theta) f2 z^2,  theta >= 0.30 (numerical).
The lower half (-log F >= g_Q(defect)(1-o(1)) for EVERY channel) is proved (rigor/optimality_all_channels.tex Prop 2.4).
MISSING: the UPPER half for the rotated channel  beta_eps = Ad Gamma(W_s e^{-eps G_*})|_{A(D)}  (S10, rigor/sdp_dual_certificate.tex Lemma 6.1):
      -log F(omega, omega^{beta_eps}) <= g_Q(delta(eps)) (1+o(1)).                                               (UH)
If (UH) holds then E_rec <= (1-theta) f2 z^2 (1+o(1)) and the compression is NOT optimal in exact fidelity.

## The route (Uhlmann), stated correctly
Let W_I be the one-particle unitary of L^2(I) realising the channel (identity on L^2(A), L^2(D) -> L^2(B) onto), I = A u D.
For ANY unitary W~ of L^2(R) with W~|_{L^2(I)} = W_I (hence W~ preserves L^2(I^c) as well) such that Gamma(W~) exists
(Shale-Stinespring: P^perp W~ P Hilbert-Schmidt), the recovered state on A(I) is the vector state of Gamma(W~)^* Omega, so
      F >= |<Omega, Gamma(W~) Omega>| = det(1 - V^*V)^{1/2},   V := P^perp W~ P                    (rigor/uhlmann_upper_bound.tex).
KEY POINT (new): the admissible exterior parts W~|_{L^2(I^c)} are ALL unitaries of L^2(I^c) (not only flows of exterior vector
fields as in P1's extension class). Writing W~ = exp(Z) to first order with Z anti-self-adjoint and block-diagonal, Z = Z_I (+) Z_e,
      -1/2 log det(1-V^*V) = 1/2 ||P^perp (Z_I + Z_e) P||_2^2 + O(||V||_2^4).
## Two lemmas that are already true (verify and write them up)
(L1) Exterior directions are invisible: for anti-self-adjoint Z_e = E_{I^c} Z_e E_{I^c},  E_I [P, Z_e] E_I = 0 (E_I Z_e = Z_e E_I = 0),
     hence Re <P^perp Z_e P, P^perp l P>_2 = 1/2 Tr( l (P^perp Z_e P + P Z_e^* P^perp) ) = -1/2 Tr(l E_I[P,Z_e]E_I) = 0
     for every self-adjoint l = E_I l E_I. So  Ext := closure{P^perp Z_e P}  is contained in  N^perp,  where
     N := closure{P^perp l P : l = l^* = E_I l E_I} is S10's visible space (Riesz vectors of first-order defects) and
     N^perp = {A = P^perp X P : E_I(A + A^*)E_I = 0} = the invisible directions.
(L2) Legendre: g_Q(E_I[P,Z_I]E_I) = 1/2 ||Pi P^perp Z_I P||_2^2 with Pi the (real) orthogonal projection onto N (S10 Lemma 4.1/Prop 4.3).
Consequently  inf over exterior extensions of the Uhlmann bound = 1/2 dist(P^perp Z_I P, Ext)^2  and
      (UH) at leading order  <=>  the invisible component (1 - Pi) P^perp Z_I P lies in Ext,   for Z_I = s D_chi|_I + eps G_*.
For the compression alone (eps = 0) this is P1's three-way identity (inf over extensions = ||Pi M||^2 = g_B/4), proved even with
the SMALLER class of flow extensions (rigor/uhlmann_upper_bound.tex Sec. 5, eq. (5.6)).
## The question to settle
(Q) Is  Ext = N^perp  (exterior directions are dense in the invisible space)?  If yes, (UH) holds for EVERY isometric channel
    Ad Gamma(W_I) (any W_I preserving L^2(A) and mapping L^2(D) onto L^2(B)), not just the rotated one, and the second-order
    recovery problem over the isometric orbit is exactly the g_Q problem. If no, compute dist((1-Pi)P^perp G_* P, Ext) itself.
Dimension count (finite model, half filling, |I| = m of n sites): dim N^perp = 2k(n-k) - m^2 <= (n-m)^2 = dim of exterior
anti-Hermitian matrices, with equality iff m = n/2 -- consistent with (Q), not a proof.
## Second-order control
The bound must hold beyond first order: use a one-parameter group. Either W~ = exp(t Z_total) at t = 1 with Z_total = Z_I + Z_e
anti-self-adjoint and [P, Z_total] Hilbert-Schmidt (then the exact identity of rigor/rate_of_remainder.tex, ||P^perp e^{tZ} P||_2^2
<= t^2 ||P^perp Z P||_2^2, gives -1/2 log det(1-V^*V) <= 1/2 ||P^perp Z_total P||^2 (1 + O(||.||^2)) exactly), or the product
W_s e^{-eps G_*} with Z_I := log(W_s e^{-eps G_*}) on L^2(I) (spectral calculus; W_s e^{-eps G_*} preserves L^2(I)).
## Tracks
E1 (analytic, Opus): rigor/exact_fidelity_upper_half.tex (Lamport style): (L1), (L2), the reduction, then attack (Q) -- e.g. via
   the characterisation N^perp = {P^perp X P: E_I(P^perp X P + P X^* P^perp) E_I = 0} and the block structure of P (Hardy
   projection on the line/circle: P has an explicit kernel; the maps X -> P^perp X P and the compressions E_I, E_{I^c});
   Hilbert-space arguments (annihilator of Ext inside N^perp = ?). If (Q) resists, prove the weaker statement for the specific
   direction v = P^perp G_* P, or find the obstruction. Deliver theorem + verdict boxes; cite documents by label.
E2 (numerical, Opus): in S10's spectral NS-circle model (numerics/optimality_all/s10_theta.py setup; exact P, exterior arcs
   present) compute: (a) N^perp and Ext as subspaces of the real Hilbert space S_2(PH, P^perp H); check dim Ext vs dim N^perp
   and the distance of (1-Pi)P^perp G_* P and of (1-Pi)M to Ext, as functions of the grid L (convergence!); (b) the optimised
   Uhlmann bound UB(Z_I) = min over exterior anti-Hermitian Z_e of 1/2 ||P^perp(Z_I + Z_e)P||^2 for Z_I = s D_chi + eps G_*
   (a linear least-squares problem, CG), for eps = 0 and eps = eps_*: report UB_c/(1/2 s^2 |u|^2) (should -> 1 if (Q) holds,
   replacing the 4.3 of numerics/optimality_all/uhlmann_rotated.py whose Gaussian-taper extension was far from optimal) and
   UB_rot/UB_c (should -> 1 - theta = 0.70); (c) the exact -1/2 log det(1 - V^*V) with the optimised extension at small s
   (second-order check). Scripts numerics/optimality_all/e2_*.py with .out files; document rigor/exterior_extension_numerics.tex.
Rules: KB cards for every result (kb -p cft_cmi add ...; KB_ACTOR=E1/E2), Opus referees afterwards (never Fable), small file
appends, compile after each append, think only to the next tool call, never run git.
