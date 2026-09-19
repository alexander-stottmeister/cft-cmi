"""Gaussian (rotated) Petz recovered symbol on the hopping chain, and the exact
quasi-free root fidelity, in mpmath at high precision.

Petz channel B -> BC with reference rho_BC (Vardhan-Wei-Zou eq. (2.9), lambda=0):
   T~ = [1_A (+) G_BC^{1/2}][1 (+)_B G_B^{-1/2}][G_AB (+) 1_C][1 (+)_B G_B^{-1/2}]
        [1_A (+) G_BC^{1/2}],      G_S = Q_S (1-Q_S)^{-1},   Q~ = T~ (1+T~)^{-1}.
Note 5 Thm 2.1:  -log F = 1/2 sum log(1+t) + 1/2 sum log(1+s) - sum log(1+sqrt(tau)),
   t = eig G1, s = eig G2, tau = eig(G1^{1/2} G2 G1^{1/2}).
"""
import numpy as np
import mpmath as mp


def _mpm(A):
    M = mp.matrix(A.shape[0], A.shape[1])
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            M[i, j] = mp.mpf(float(A[i, j]))
    return M


def _np(M):
    return np.array([[complex(M[i, j]) for j in range(M.cols)] for i in range(M.rows)])


def _fun_sym(Msub, f):
    E, V = mp.eigsy(Msub)
    m = Msub.rows
    D = mp.diag([f(E[k]) for k in range(m)])
    return V * D * V.T


def _sq(x):
    """sqrt guarded against round-off making a true zero slightly negative."""
    return mp.sqrt(x) if x > 0 else mp.mpf(0)


def _embed(n, off, Msub):
    M = mp.eye(n)
    m = Msub.rows
    for a in range(m):
        for b in range(m):
            M[off + a, off + b] = Msub[a, b]
    return M


def petz_symbol(Qnp, LA, LB, LC, dps=60):
    """Recovered symbol of the ordinary Petz map (lambda = 0), float output."""
    mp.mp.dps = dps
    n = LA + LB + LC
    Q = _mpm(Qnp)
    def sub(i0, i1):
        m = i1 - i0
        S = mp.matrix(m, m)
        for a in range(m):
            for b in range(m):
                S[a, b] = Q[i0 + a, i0 + b]
        return S
    g = lambda x: x / (1 - x)
    GAB = _fun_sym(sub(0, LA + LB), g)
    GBC = _fun_sym(sub(LA, n), g)
    GB = sub(LA, LA + LB)
    GBh = _fun_sym(GB, lambda x: _sq((1 - x) / x))     # G_B^{-1/2}
    GBCh = _fun_sym(GBC, lambda x: _sq(x))             # G_BC^{1/2}
    L = _embed(n, LA, GBCh) * _embed(n, LA, GBh)
    T = L * _embed(n, 0, GAB) * L.T
    T = (T + T.T) / 2
    Qt = T * (mp.eye(n) + T) ** -1
    return np.real(_np((Qt + Qt.T) / 2))


def _prep(Q, eps):
    """Eigen-data of a symbol with eigenvalues clipped to [eps, 1-eps].  The SAME
    eps is used for both states, so the log-determinant cancellations in the
    fidelity formula are preserved; eps is far below the resolution of the
    double-precision symbols that are fed in."""
    E, V = mp.eigsy(Q)
    e = [min(max(E[k], eps), 1 - eps) for k in range(Q.rows)]
    return e, V


def neglogF(Q1np, Q2np, dps=80, eps=None):
    """Exact -log(root fidelity) between two gauge-invariant quasi-free states."""
    mp.mp.dps = dps
    if eps is None:
        eps = mp.mpf(10) ** (-25)
    Q1, Q2 = _mpm(np.real(Q1np)), _mpm(np.real(Q2np))
    e1, V1 = _prep(Q1, eps)
    e2, V2 = _prep(Q2, eps)
    n = Q1.rows
    t = [e1[k] / (1 - e1[k]) for k in range(n)]
    s = [e2[k] / (1 - e2[k]) for k in range(n)]
    G1h = V1 * mp.diag([mp.sqrt(x) for x in t]) * V1.T
    G2 = V2 * mp.diag(s) * V2.T
    M = G1h * G2 * G1h
    tau = mp.eigsy((M + M.T) / 2, eigvals_only=True)
    val = mp.mpf(0)
    for k in range(n):
        val += mp.log(1 + t[k]) / 2 + mp.log(1 + s[k]) / 2 - mp.log(1 + _sq(tau[k]))
    return val
