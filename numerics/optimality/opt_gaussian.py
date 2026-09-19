"""S8/O8 -- second-order optimality of the Petz map among quasi-free recovery
channels, lattice free fermion (hopping chain at half filling).

Conventions.  Q_{ij} = <c_j^dag c_i> on n = LA+LB+LC consecutive sites, so a
number-conserving Bogoliubov map c -> U c sends Q -> U Q U^dag.  Blocks are
labelled A = [0,LA), B = [LA,LA+LB), C = [LA+LB,n); D := BC.

Gauge-invariant quasi-free channel N: S(B) -> S(BC) (Schroedinger picture; the
Heisenberg map beta: A(BC) -> A(B) is its adjoint):
    Q_out = X Q_in X^dag + Y,  X: H_B -> H_D,  Y = Y^dag,
CP  <=>  Y >= 0  and  X X^dag + Y <= 1.
Recovered symbol on I = ABC (channel applied to the B half of the vacuum AB
state, C initialised inside the channel):
    Qrec_AA = Q_AA,  Qrec_AD = Q_AB X^dag,  Qrec_DD = Z := X Q_BB X^dag + Y.
Change of variables (X,Z): the feasible set
    X Q_BB X^dag <= Z <= 1 - X (1-Q_BB) X^dag
is CONVEX (X -> X R X^dag is operator convex for R >= 0), and the second-order
error is a positive quadratic form in the defect, which is affine in (X,Z).
Hence the second-order optimisation is a convex programme.  Solved here by a
log-barrier + L-BFGS with analytic gradients.
"""
import numpy as np
from scipy.optimize import minimize


def corr_sine(n):
    """Q_ij = sin(pi(i-j)/2)/(pi(i-j)), half-filled hopping chain, real sym."""
    i = np.arange(n)
    d = i[:, None] - i[None, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        Q = np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * np.where(d == 0, 1, d)))
    return Q


def qfi_data(Q, kappa_c=None):
    """Eigenbasis of Q and the QFI weights w_ik = 1/(q_i(1-q_k)+q_k(1-q_i)).
    If kappa_c is given the weights are CAPPED at w_max = 1 + cosh(kappa_c)
    (their value on the diagonal kappa_i = kappa_k = kappa_c): no mode is
    discarded, the capped form still lower-bounds the true QFI form, is still a
    positive quadratic form (hence convex), but the minimiser can no longer
    dump defect into the ultraviolet for free."""
    q, U = np.linalg.eigh(Q)
    q = np.clip(q, 1e-300, 1 - 1e-16)
    kap = np.log((1 - q) / q)
    w = 1.0 / (q[:, None] * (1 - q)[None, :] + q[None, :] * (1 - q)[:, None])
    if kappa_c is not None:
        w = np.minimum(w, 1.0 + np.cosh(kappa_c))
    return U, q, w, kap


def qfi_form(delta, U, w):
    """(1/4) sum_ik w_ik |(U^dag delta U)_ik|^2  and its Hermitian gradient
    G with df = Re tr[G d(delta)]."""
    dt = U.conj().T @ delta @ U
    val = 0.25 * np.sum(w * np.abs(dt) ** 2)
    G = 0.5 * (U @ (w * dt) @ U.conj().T)
    return val, G


class Problem:
    def __init__(self, LA, LB, LC, kappa_c=None):
        self.LA, self.LB, self.LC = LA, LB, LC
        n = LA + LB + LC
        self.n, self.m = n, LB + LC          # m = dim H_D
        Q = corr_sine(n)
        self.Q = Q
        a, b = slice(0, LA), slice(LA, LA + LB)
        d = slice(LA, n)
        self.QAA, self.QAB, self.QAD = Q[a, a], Q[a, b], Q[a, d]
        self.QBB, self.QDD = Q[b, b], Q[d, d]
        self.U, self.q, self.w, self.kap = qfi_data(Q, kappa_c)
        self.q1, self.U1 = np.linalg.eigh(Q)
        self.mode = 'qfi'
        self.Rp = self.QBB                    # R_+ in  Z >= X R_+ X^dag
        self.Rm = np.eye(LB) - self.QBB       # R_- in  Z <= 1 - X R_- X^dag

    def defect(self, X, Z):
        n, LA = self.n, self.LA
        D = np.zeros((n, n), dtype=complex)
        dAD = self.QAD - self.QAB @ X.conj().T
        D[0:LA, LA:n] = dAD
        D[LA:n, 0:LA] = dAD.conj().T
        D[LA:n, LA:n] = self.QDD - Z
        return D

    def energy(self, X, Z):
        """Recovery error and gradients (dE/dX complex, dE/dZ Hermitian)."""
        if self.mode == 'exact':
            return exact_energy(self, X, Z)
        val, G = qfi_form(self.defect(X, Z), self.U, self.w)
        LA, n = self.LA, self.n
        gX = -2.0 * (G[LA:n, 0:LA] @ self.QAB)
        gZ = -G[LA:n, LA:n]
        return val, gX, gZ

    def slacks(self, X, Z):
        C1 = Z - X @ self.Rp @ X.conj().T
        C2 = np.eye(self.m) - X @ self.Rm @ X.conj().T - Z
        return 0.5 * (C1 + C1.conj().T), 0.5 * (C2 + C2.conj().T)


def _pack(X, Z):
    return np.concatenate([X.real.ravel(), X.imag.ravel(), Z.real.ravel(), Z.imag.ravel()])


def _unpack(v, m, k):
    nx = m * k
    X = v[:nx].reshape(m, k) + 1j * v[nx:2 * nx].reshape(m, k)
    Zr = v[2 * nx:2 * nx + m * m].reshape(m, m)
    Zi = v[2 * nx + m * m:].reshape(m, m)
    Z = 0.5 * (Zr + Zr.T) + 0.5j * (Zi - Zi.T)
    return X, Z


def _logdet_or_inf(M):
    try:
        L = np.linalg.cholesky(M)
    except np.linalg.LinAlgError:
        return None, None
    Li = np.linalg.inv(L)
    return 2.0 * np.sum(np.log(np.real(np.diag(L)))), Li.conj().T @ Li


def barrier_obj(v, P, mu):
    X, Z = _unpack(v, P.m, P.LB)
    C1, C2 = P.slacks(X, Z)
    l1, I1 = _logdet_or_inf(C1)
    l2, I2 = _logdet_or_inf(C2)
    if l1 is None or l2 is None:
        return 1e100, np.zeros_like(v)
    val, gX, gZ = P.energy(X, Z)
    f = val - mu * (l1 + l2)
    gX = gX + 2 * mu * (I1 @ X @ P.Rp + I2 @ X @ P.Rm)
    gZ = gZ + mu * (-I1 + I2)
    return f, np.concatenate([gX.real.ravel(), gX.imag.ravel(),
                              gZ.real.ravel(), gZ.imag.ravel()])


def fd_hessian(v, P, mu, f0, g0, h=1e-6):
    n = len(v)
    H = np.empty((n, n))
    for k in range(n):
        vp = v.copy(); vp[k] += h
        vm = v.copy(); vm[k] -= h
        fp, gp = barrier_obj(vp, P, mu)
        fm, gm = barrier_obj(vm, P, mu)
        okp, okm = fp < 1e99, fm < 1e99
        if okp and okm:
            H[:, k] = (gp - gm) / (2 * h)
        elif okp:
            H[:, k] = (gp - g0) / h
        elif okm:
            H[:, k] = (g0 - gm) / h
        else:
            H[:, k] = 0.0
            H[k, k] = 1.0
    return 0.5 * (H + H.T)


def newton_step(v, P, mu, H=None):
    f0, g0 = barrier_obj(v, P, mu)
    n = len(v)
    if H is None:
        H = fd_hessian(v, P, mu, f0, g0)
    ev = np.linalg.eigvalsh(H)
    lam = max(0.0, 1e-10 * max(1.0, ev.max()) - ev.min())
    dv = -np.linalg.solve(H + lam * np.eye(n), g0)
    if dv @ g0 > 0:
        dv = -g0 / max(1.0, np.linalg.norm(g0))
    t = 1.0
    for _ in range(60):
        vt = v + t * dv
        ft = barrier_obj(vt, P, mu)[0]
        if ft < 1e99 and ft <= f0 + 1e-4 * t * (g0 @ dv):
            return vt, ft, np.linalg.norm(g0), H
        t *= 0.5
    return v, f0, np.linalg.norm(g0), None


def solve(P, mus=None, X0=None, Z0=None, iters=30, verbose=False):
    if mus is None:
        mus = [1e-1 * 10 ** (-k) for k in range(10)]
    X = np.zeros((P.m, P.LB), dtype=complex) if X0 is None else X0.astype(complex)
    Z = (P.QDD + 0j) if Z0 is None else Z0.astype(complex)
    v = _pack(X, Z)
    for mu in mus:
        fprev, H = np.inf, None
        for it in range(iters):
            if it % 4 == 0:
                H = None
            v, f, gn, H = newton_step(v, P, mu, H)
            if abs(fprev - f) <= 1e-14 * max(1.0, abs(f)):
                break
            fprev = f
        if verbose:
            X, Z = _unpack(v, P.m, P.LB)
            print('   mu=%.0e  E=%.12e  it=%d  |g|=%.2e' % (mu, P.energy(X, Z)[0], it, gn))
    X, Z = _unpack(v, P.m, P.LB)
    return X, Z, P.energy(X, Z)[0]


def gradcheck(P, seed=0):
    rng = np.random.default_rng(seed)
    X = 0.05 * (rng.normal(size=(P.m, P.LB)) + 1j * rng.normal(size=(P.m, P.LB)))
    Z = 0.5 * np.eye(P.m) + 0.0j
    v = _pack(X, Z)
    f0, g0 = barrier_obj(v, P, 1e-3)
    err = 0.0
    for _ in range(25):
        k = rng.integers(len(v))
        h = 1e-6
        vp = v.copy(); vp[k] += h
        vm = v.copy(); vm[k] -= h
        num = (barrier_obj(vp, P, 1e-3)[0] - barrier_obj(vm, P, 1e-3)[0]) / (2 * h)
        err = max(err, abs(num - g0[k]) / max(1.0, abs(g0[k])))
    return err


# ---------------------------------------------------------------- exact -logF
def neglogF_grad(Q1, Q2, U1=None, q1=None):
    """-log Fid(omega_Q1, omega_Q2) (Note 5 Thm 2.1) and its gradient N with
    d(-log F) = Re tr[N dQ2].  Double precision; Q1, Q2 Hermitian, 0<Q<1."""
    if U1 is None:
        q1, U1 = np.linalg.eigh(Q1)
    t = q1 / (1 - q1)
    G1h = (U1 * np.sqrt(t)) @ U1.conj().T
    q2, U2 = np.linalg.eigh(Q2)
    q2c = np.clip(q2, 1e-300, 1 - 1e-16)
    s = q2c / (1 - q2c)
    G2 = (U2 * s) @ U2.conj().T
    T = G1h @ G2 @ G1h
    T = 0.5 * (T + T.conj().T)
    tau, V = np.linalg.eigh(T)
    tau = np.clip(tau, 0.0, None)
    st = np.sqrt(tau)
    val = 0.5 * np.sum(np.log1p(t)) + 0.5 * np.sum(np.log1p(s)) - np.sum(np.log1p(st))
    with np.errstate(divide='ignore'):
        d = np.where(st > 0, 1.0 / (2 * np.maximum(st, 1e-300) * (1 + st)), 0.0)
    M = (V * d) @ V.conj().T
    R = (U2 * (1.0 / (1 - q2c))) @ U2.conj().T          # (1-Q2)^{-1}
    N = 0.5 * R - R @ (G1h @ M @ G1h) @ R
    return val, 0.5 * (N + N.conj().T)


def exact_energy(P, X, Z):
    Qr = np.zeros((P.n, P.n), dtype=complex)
    Qr[:P.LA, :P.LA] = P.QAA
    Mad = P.QAB @ X.conj().T
    Qr[:P.LA, P.LA:] = Mad
    Qr[P.LA:, :P.LA] = Mad.conj().T
    Qr[P.LA:, P.LA:] = Z
    Qr = 0.5 * (Qr + Qr.conj().T)
    val, N = neglogF_grad(P.Q, Qr, P.U1, P.q1)
    gX = 2.0 * (N[P.LA:, :P.LA] @ P.QAB)
    gZ = N[P.LA:, P.LA:]
    return val, gX, gZ
