"""Verification of Prop. 2.2 (complete positivity of gauge-invariant quasi-free
channels) on small mode numbers, against an explicit Fock-space dilation.

dim h_B = 1 (the input mode), dim h_D = 2 (output modes), dim h_E = 2.
Everything is built as explicit 2^n x 2^n matrices with Jordan-Wigner."""
import numpy as np

rng = np.random.default_rng(7)


def jw(n):
    """Annihilation operators c_0..c_{n-1} on (C^2)^{(x)n}, Jordan-Wigner."""
    a = np.array([[0., 1.], [0., 0.]])
    z = np.array([[1., 0.], [0., -1.]])
    i2 = np.eye(2)
    ops = []
    for k in range(n):
        m = np.array([[1.]])
        for j in range(n):
            m = np.kron(m, z if j < k else (a if j == k else i2))
        ops.append(m)
    return ops


def gaussian_rho(Q):
    """Density matrix of the gauge-invariant quasi-free state with symbol
    Q_ij = <c_j^dag c_i>  (so rho = det(1-Q) Gamma(Q/(1-Q)))."""
    n = Q.shape[0]
    c = jw(n)
    q, U = np.linalg.eigh(Q)
    d = [sum(np.conj(U[j, k]) * c[j] for j in range(n)) for k in range(n)]
    rho = np.eye(2 ** n, dtype=complex)
    for k in range(n):
        nk = d[k].conj().T @ d[k]
        rho = rho @ ((1 - q[k]) * np.eye(2 ** n) + (2 * q[k] - 1) * nk)
    return rho


def symbol(rho, n):
    c = jw(n)
    return np.array([[np.trace(rho @ (c[j].conj().T @ c[i])) for j in range(n)]
                     for i in range(n)])


def bogoliubov(W, n):
    """Unitary Gamma(W) on Fock space for a number-conserving W (n modes)."""
    from scipy.linalg import logm, expm
    L = logm(W)
    c = jw(n)
    K = sum(L[i, j] * (c[i].conj().T @ c[j]) for i in range(n) for j in range(n))
    return expm(K)


def run(trials=4):
    worst = 0.0
    for _ in range(trials):
        kB, kD = 1, 2
        X = rng.normal(size=(kD, kB)) + 1j * rng.normal(size=(kD, kB))
        X = 0.7 * X / np.linalg.norm(X, 2)
        P = np.eye(kD) - X @ X.conj().T
        ev, ew = np.linalg.eigh(P)
        Psq = (ew * np.sqrt(np.clip(ev, 0, None))) @ ew.conj().T
        M = rng.normal(size=(kD, kD)) + 1j * rng.normal(size=(kD, kD))
        QE = M @ M.conj().T
        QE = QE / (1.3 * np.linalg.eigvalsh(QE).max())        # 0 <= Q_E <= 1
        Y = Psq @ QE @ Psq                                     # 0 <= Y <= P
        assert np.linalg.eigvalsh(Y).min() > -1e-12
        assert np.linalg.eigvalsh(np.eye(kD) - X @ X.conj().T - Y).min() > -1e-12
        V = np.hstack([X, Psq])                       # kD x (kB+kD) coisometry
        # complete V to a unitary W on kB+kD = 3 modes
        ns = np.linalg.svd(V)[2][kD:]                 # orthonormal complement rows
        W = np.vstack([V, ns])
        assert np.allclose(W @ W.conj().T, np.eye(kB + kD), atol=1e-10)
        # global system: A (1 mode) + B (1 mode) + E (2 modes) = 4 modes
        QAB = np.array([[0.5, 0.3], [0.3, 0.45]])     # a vacuum-like AB symbol
        Qglob = np.zeros((4, 4), dtype=complex)
        Qglob[:2, :2] = QAB
        Qglob[2:, 2:] = QE
        rho = gaussian_rho(Qglob)
        Wg = np.eye(4, dtype=complex)
        Wg[1:, 1:] = W                                # acts on B (+) E
        rho2 = bogoliubov(Wg, 4) @ rho @ bogoliubov(Wg, 4).conj().T
        Qout = symbol(rho2, 4)
        pred = np.zeros((3, 3), dtype=complex)        # A (+) D  (D = modes 1,2)
        pred[0, 0] = QAB[0, 0]
        pred[0, 1:] = QAB[0, 1] * X.conj().T
        pred[1:, 0] = pred[0, 1:].conj()
        pred[1:, 1:] = X @ QAB[1:, 1:] @ X.conj().T + Y
        got = Qout[np.ix_([0, 1, 2], [0, 1, 2])]
        worst = max(worst, np.abs(got - pred).max())
    return worst


if __name__ == '__main__':
    print('max |Q_out(dilation) - (X Q X* + Y)| over trials =', run())
