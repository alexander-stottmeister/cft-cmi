"""REF-RP-4: independent test of index_zero.tex lem:cubic (ind X_U = Tr(G_U^3) = m(1) - m(-1)) and thm:sv.
Tolerance fixed before the run: TOL = 1e-10.
(a) finite dimension, random unitary U on C^n, P of rank k: ind X = 0 always, so Tr(G^3) must vanish.
(b) l^2(Z), P = proj on n >= 0, U = multiplication by u(theta) in the Fourier basis (U_{nm} = uhat(n-m)):
    u = exp(i a sin theta)        (winding 0, G HS with infinitely many eigenvalues, index 0)
    u = e^{i theta} exp(i a sin)  (winding 1, X = Toeplitz T_u, index -1)
    uhat(n) = J_n(a) (Jacobi-Anger), resp. J_{n-1}(a).  Truncation honest: G is computed on the window |j|,|k| <= N0
    with the inner sum over n >= 0 cut at |n| <= N0 + M (Bessel tail < 1e-30 for M = 60, a <= 3);
    the discarded HS weight ||G||_2^2 - ||G_W||_2^2 uses the exact ||G||_2^2 = sum_n |n| |uhat(n)|^2
    (Hankel HS norms), and |tau(G) - tau(G_W)| <= 3 ||G||_2^2 * sqrt(discarded)  (lem:cubic (c), A' = Pi G Pi).
(c) exact shift U e_n = e_{n+1}: G = -|e_{-1}><e_{-1}|, Tr G^3 = -1, ind X = -1.
"""
import numpy as np
from scipy.special import jv
TOL = 1e-10
rng = np.random.default_rng(4)
print("TOL =", TOL)
# (a)
for n, k in [(6, 2), (11, 5), (40, 17)]:
    Z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    U, _ = np.linalg.qr(Z)
    P = np.diag([1.0] * k + [0.0] * (n - k))
    G = P - U.conj().T @ P @ U
    t3 = np.trace(G @ G @ G).real
    B = P @ U @ (np.eye(n) - P); C = (np.eye(n) - P) @ U @ P
    sB = np.sort(np.linalg.svd(B, compute_uv=False)); sC = np.sort(np.linalg.svd(C, compute_uv=False))
    print(f"(a) n={n} k={k}: Tr G^3 = {t3:+.3e}  |.|<TOL: {abs(t3) < TOL};  max|sv(B)-sv(C)| = {np.max(abs(sB - sC)):.2e}")
# (b)
def window_G(uhat, N0, M):
    idx = np.arange(-N0, N0 + 1)
    ns = np.arange(0, N0 + M + 1)
    Ublk = uhat(ns[:, None] - idx[None, :])          # rows n >= 0, cols j in window
    QW = Ublk.conj().T @ Ublk
    PW = np.diag((idx >= 0).astype(float))
    return PW - QW, idx
for name, wind, uh in [("exp(i a sin)", 0, None), ("z exp(i a sin)", 1, None)]:
    for a in [0.7, 3.0]:
        shift = wind
        uhat = lambda m, a=a, shift=shift: jv(m - shift, a)
        N0, M = 60, 60
        G, idx = window_G(uhat, N0, M)
        m = np.arange(-400, 401)
        hs_exact = np.sum(np.abs(m) * np.abs(jv(m - shift, a)) ** 2)
        hs_win = np.sum(np.abs(G) ** 2)
        disc = max(hs_exact - hs_win, 0.0)
        t3 = np.trace(G @ G @ G).real
        ev = np.linalg.eigvalsh((G + G.conj().T) / 2)
        m1 = np.sum(np.abs(ev - 1) < 1e-8); mm1 = np.sum(np.abs(ev + 1) < 1e-8)
        bound = 3 * hs_exact * np.sqrt(disc)
        # blocks restricted to the window: B = P U P_-, C = P_- U P  (U_{nm} = uhat(n-m))
        U = uhat(idx[:, None] - idx[None, :])
        Pp = idx >= 0
        sB = np.sort(np.linalg.svd(U[np.ix_(Pp, ~Pp)], compute_uv=False))[::-1][:8]
        sC = np.sort(np.linalg.svd(U[np.ix_(~Pp, Pp)], compute_uv=False))[::-1][:8]
        print(f"(b) u={name} a={a}: Tr G_W^3 = {t3:+.14f}  expected {-wind:+d}  dev {abs(t3 + wind):.2e} "
              f"< TOL: {abs(t3 + wind) < TOL}; m(1)-m(-1) = {m1 - mm1}; ||G||_2^2 exact {hs_exact:.12f} "
              f"window {hs_win:.12f} discarded {disc:.1e} trunc.bound {bound:.1e}")
        print("    top sv B:", np.round(sB[:4], 12), " top sv C:", np.round(sC[:4], 12))
# (c)
N = 30; idx = np.arange(-N, N + 1)
S = np.zeros((2 * N + 1, 2 * N + 1)); S[1:, :-1] = np.eye(2 * N)  # e_n -> e_{n+1}, window interior exact
P = np.diag((idx >= 0).astype(float))
G = P - S.T @ P @ S
inner = slice(1, 2 * N)  # drop window edges where truncated S is not unitary
Gi = G[inner, inner]
print("(c) shift: nonzero entries of G (interior):", [(int(idx[1 + i]), Gi[i, i]) for i in range(Gi.shape[0]) if abs(Gi[i, i]) > 0],
      " Tr G^3 =", np.trace(Gi @ Gi @ Gi), " off-diag max", np.max(np.abs(Gi - np.diag(np.diag(Gi)))))
