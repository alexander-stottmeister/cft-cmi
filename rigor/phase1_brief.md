# Phase 1 brief (2026-09-08): a direct route to the sharp upper bound (O1)

Setting (Notes 4, 5, 7). Free chiral fermion (r complex components; take r=1), vacuum omega on M = CAR(L^2(I))'' with
I = ABC = (-a, L), A = (-a,0), D = BC = (0,L), touching point 0. Zero-collar recovery curve: omega_tilde_s = omega o beta_s,
beta_s(a(f)) = a(W_s f), W_s = push-forward of half-densities along the piecewise-Moebius map
    k_s(x) = x on (-a,0),   k_s(x) = h_s(x) = L x / (L + s x) on [0, L);   k_s in C^{1,1}(I), kink only at 0.
Cross-ratio variable zeta = a s/(a+L); Phi(zeta) = -log Fid(omega, omega_tilde). Known: liminf Phi/zeta^2 >= g_B/8 = 1/(12 pi^2)
(rigor/quadratic_limit.tex, unconditional); needed: limsup Phi/zeta^2 <= g_B/8.

Route (Uhlmann + Bogoliubov extension; no interchange of limits):
1. Extend k_s to a C^{1,1} diffeomorphism k~_s of R: identity on (-inf,-a], h_s on [0,L], and on [L, inf) any smooth
   increasing map onto [h_s(L), inf) matching h_s at L to first order and tending to the identity at infinity
   (displacement u_s(x) = x - k~_s(x) = s x^2/(L+sx) on D, = s phi(x) beyond L with phi(L)=L^2/(L+sL), phi decaying).
   Then W~_s (push-forward on L^2(R) half-densities) is unitary, and Gamma(W~_s) exists on Fock space iff
   V_s := P_- W~_s P_+ is Hilbert-Schmidt (Shale-Stinespring); for C^{1,1} maps this holds (kernel estimate:
   the kernel of P_- W_phi P_+ is (1/2 pi i)[ sqrt(phi'(x)phi'(y))/(phi(x)-phi(y)) - 1/(x-y) ] restricted appropriately).
2. Vector representative: Psi_s := Gamma(W~_s)^* Omega represents omega_tilde_s on M (check: Gamma(W~) a(f) Gamma(W~)^* = a(W~ f)).
   Uhlmann (Alberti-Uhlmann 2002 Thm 2(3)): Fid(omega, omega_tilde_s) = sup_{u' in U(M')} |<Omega, u' Psi_s>| >= |<Omega, Gamma(U) Omega>|
   for U = W~_s (1 (+) W') with any unitary W' on L^2(I') (Gamma(1 (+) W') lies in M').
3. Vacuum overlap of a Bogoliubov unitary (Berezin; Ruijsenaars J. Math. Phys. 18 (1977) 517): |<Omega, Gamma(U) Omega>| = |det(P_+ U P_+)| = det(1 - V^*V)^{1/2},
   V = P_- U P_+ Hilbert-Schmidt (one-mode check: rotation by theta gives overlap cos theta, V = sin theta). Hence
       Phi(zeta) <= -(1/2) log det(1 - V^*V) <= (1/2) ||V||_2^2 / (1 - ||V||^2).
4. Expansion: U_zeta = 1 + zeta K + O(zeta^2) with K = D_X + i h' (D_X the generator of the push-forward along the first-order
   field X = d k~_s/ds |_{s=0}, h' a one-particle generator on L^2(I')), so ||V_zeta||_2^2 = zeta^2 ||P_- K P_+||_2^2 + O(zeta^3),
   and limsup Phi/zeta^2 <= (1/2) ||P_- K P_+||_2^2 = (1/2) ||dGamma(K) Omega||^2 for EVERY admissible h'.
5. Sharpness: dGamma(D_X) Omega is (up to normalization) T(g) Omega with the universal g of Note 7 (g = -x^2/L on D, 0 on A);
   dGamma(i h') Omega ranges over the two-particle vectors B' Omega, B' in M'_sa quasi-free; by the three-way identity of
   rigor/lemma_second_variation.tex, g_B/4 = dist(T(g)Omega, closure M'_sa Omega)^2, and the modular data are second-quantized,
   so the distance is attained in the two-particle sector: inf_{h'} (1/2)||P_-(D_X + i h')P_+||_2^2 = (1/2)(g_B/4) = g_B/8.
   => limsup Phi/zeta^2 <= g_B/8. Combined with P2: lim Phi/zeta^2 = 1/(12 pi^2). Theorem A closed, no tail bound needed.
   (The tail bound O4 remains useful for certified numerics and for the rate.)
Numerical test (decisive, do first): E(s) := ||P_- W~_s P_+||_2^2 for the explicit family and a parametrized extension;
check E(s)/s^2 -> const, minimize over extensions, compare (1/2) E_min(zeta) with the tabulated Phi(zeta) (Note 5 Table 3:
Phi(1/15) = 3.517e-5, Phi(1/120) = 5.81e-7) -- the inequality Phi <= -(1/2) log det(1 - V^*V) must hold for every extension,
and the ratio must tend to 1 as zeta -> 0 for the optimal extension; the optimal (1/2)E/zeta^2 must tend to g_B/8 = 0.0084434.
Conventions: half-density push-forward (W f)(y) = f(k^{-1}(y)) (k^{-1})'(y)^{1/2}; P_+ = Hardy projection onto positive
frequencies of L^2(R) (vacuum symbol Q = P_+ compressed to I; the note's Fourier convention: P_+ projects on k<0 in its
convention -- check Note 4 Sec. 1 and use ONE convention consistently).

## Correction (2026-09-08, from numerics/p1_bogoliubov.out, agent PN)
- The extension of k_s must be a diffeomorphism of the CIRCLE S^1 = R u {inf} (asymptotically affine on R, moving the point at infinity),
  not a map tending to the identity at infinity: with identity-at-infinity extensions inf (1/2)E/zeta^2 = 0.0678 ~ 8 x g_B/8
  (exact constraint g~(pi) = g~'(pi) = 0 on the circle). Work in the Moebius-covariant circle chart.
- E = (1/2) ||W* P_- W - P_-||_2^2 (projection difference); validated on Moebius maps (E = 2e-27) and on x + eps e^{-x^2/2} (E = eps^2/(48 pi)).
- Q[g] = (1/(48 pi^2)) int_0^inf k^3 |g_hat(k)|^2 dk = (1/12) sum_{n>=2} (n^3 - n) |g~_n|^2 (circle modes).
- Results: E(s)/s^2 = 0.00183-0.00190 for s = 0.025 ... 0.8; bound Phi <= (1/2)E holds for every extension tested; optimal extension:
  (1/2)E/Phi = 1.0022, 1.0045, 1.0130, 1.0414, 1.1206, 1.2847 at zeta = 1/120, 1/60, 1/30, 1/15, 2/15, 4/15 (-> 1 from above).
  First order: 4.5 Q_min = 0.0084465 vs g_B/8 = 0.0084434 (0.04%); 9 Q_min = 0.0168930 vs g_B/4 = 0.0168869.
- The infimum over quasi-free h' is attained by GEOMETRIC h' (vector fields on I'): step 5 needs only vector-field extensions.
