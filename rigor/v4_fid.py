"""v4 audit: independent finite-dimensional root-fidelity evaluation + the xi0-phase consistency test.

Independent formula used (Theorem 2.1, second form of the note):
    Fid = det(S1 S2 + C1 U C2)/det U,   S_i = Q_i^{1/2}, C_i = (1-Q_i)^{1/2},
    G1^{1/2} G2^{1/2} = U |G1^{1/2}G2^{1/2}| (polar).
This is algebraically independent of the code's route (which builds T = Wm Wm^H and
det(1+T^{1/2})).  Both are cross-checked against a brute-force Fock-space trace for n<=4.
All heavy linear algebra in mpmath at dps=40.
"""
import sys, numpy as np, mpmath as mp
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics")
from compression_box import Q_box

NUM = "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/"

# ---------- mpmath helpers ----------
def to_mp(A):
    n, m = A.shape; M = mp.matrix(n, m)
    for i in range(n):
        for j in range(m):
            z = A[i, j]
            M[i, j] = mp.mpc(float(np.real(z)), float(np.imag(z))) if np.iscomplexobj(A) else mp.mpf(float(z))
    return M

def herm_fun(M, f):
    """f applied to a Hermitian mp matrix via its eigen-decomposition."""
    E, V = mp.eighe(M); n = M.rows
    D = mp.matrix(n, n)
    for i in range(n): D[i, i] = f(E[i])
    return V*D*V.H, [E[i] for i in range(n)]

def logfid_route_A(Q1, Q2):
    """Code's route: -log Fid = -[1/2 sum log(1-q) + 1/2 sum log(1-qt) + sum log(1+sqrt(tau))]."""
    n = Q1.rows
    w1, V1 = mp.eighe(Q1); w2, V2 = mp.eighe(Q2)
    g1h = [mp.sqrt(w1[i]/(1-w1[i])) for i in range(n)]
    g2h = [mp.sqrt(w2[i]/(1-w2[i])) for i in range(n)]
    # X = G1^{1/2} G2^{1/2} ; T = X X^H ; need eig(T)
    G1h = V1*mp.diag(g1h)*V1.H
    G2h = V2*mp.diag(g2h)*V2.H
    X = G1h*G2h
    tau = mp.eighe(X*X.H, eigvals_only=True)
    s = mp.mpf(0)
    for i in range(n):
        s += mp.log(1-w1[i])/2 + mp.log(1-w2[i])/2 + mp.log(1+mp.sqrt(max(tau[i], mp.mpf(0))))
    return -s

def logfid_route_B(Q1, Q2):
    """Independent route: Fid = det(S1 S2 + C1 U C2)/det U with U from the polar decomposition."""
    n = Q1.rows
    S1, _ = herm_fun(Q1, mp.sqrt); S2, _ = herm_fun(Q2, mp.sqrt)
    I = mp.eye(n)
    C1, _ = herm_fun(I-Q1, mp.sqrt); C2, _ = herm_fun(I-Q2, mp.sqrt)
    G1h, _ = herm_fun(Q1, lambda q: mp.sqrt(q/(1-q)))
    G2h, _ = herm_fun(Q2, lambda q: mp.sqrt(q/(1-q)))
    X = G1h*G2h
    # polar X = U |X| : |X| = (X^H X)^{1/2}, U = X |X|^{-1}
    absX, _ = herm_fun(X.H*X, mp.sqrt)
    absXinv, _ = herm_fun(X.H*X, lambda t: 1/mp.sqrt(t))
    U = X*absXinv
    M = S1*S2 + C1*U*C2
    return -(mp.log(mp.det(M)) - mp.log(mp.det(U)))

def logfid_route_C(Q1, Q2):
    """Third route: Fid = det[(1-Q1)(1-Q2)]^{1/2} det[1 + (G1^{1/2} G2 G1^{1/2})^{1/2}]."""
    n = Q1.rows; I = mp.eye(n)
    G1h, _ = herm_fun(Q1, lambda q: mp.sqrt(q/(1-q)))
    G2, _ = herm_fun(Q2, lambda q: q/(1-q))
    T = G1h*G2*G1h
    Th, tt = herm_fun(T, mp.sqrt)
    _, w1 = herm_fun(Q1, lambda q: q); _, w2 = herm_fun(Q2, lambda q: q)
    s = mp.mpf(0)
    for i in range(n): s += mp.log(1-w1[i])/2 + mp.log(1-w2[i])/2
    s += mp.log(mp.det(I+Th))
    return -s

def relent_mp(Q1, Q2):
    n = Q1.rows; I = mp.eye(n)
    lQ1, _ = herm_fun(Q1, mp.log); l1Q1, _ = herm_fun(I-Q1, mp.log)
    lQ2, _ = herm_fun(Q2, mp.log); l1Q2, _ = herm_fun(I-Q2, mp.log)
    M = Q1*(lQ1-lQ2) + (I-Q1)*(l1Q1-l1Q2)
    return sum(M[i, i] for i in range(n)).real


# ---------- brute-force Fock check (small n) ----------
def brute_fock(Q1, Q2):
    import scipy.linalg as sla
    n = len(Q1); I2 = np.eye(2); Z = np.diag([1., -1.]); am = np.array([[0, 1], [0, 0]], dtype=complex)
    ops = []
    for j in range(n):
        mats = [Z]*j + [am] + [I2]*(n-j-1); M = mats[0]
        for m in mats[1:]: M = np.kron(M, m)
        ops.append(M)
    def rho(Q):
        G = Q @ np.linalg.inv(np.eye(n)-Q); K = sla.logm(G)
        H = sum(K[i, j]*ops[i].conj().T @ ops[j] for i in range(n) for j in range(n))
        return np.linalg.det(np.eye(n)-Q).real*sla.expm(H)
    r1, r2 = rho(Q1), rho(Q2); s1 = sla.sqrtm(r1)
    return np.trace(sla.sqrtm(s1 @ r2 @ s1)).real, np.trace(r1 @ (sla.logm(r1)-sla.logm(r2))).real


def subcompress(Q, D, eps, dps=40, Qmp=None):
    """Spectral sub-compression: P = eigenvectors of Q with eig in (eps,1-eps); return (ws, P^H(Q-D)P)."""
    mp.mp.dps = dps
    Qm = to_mp(Q) if Qmp is None else Qmp
    Dm = to_mp(D)
    Qt = Qm - Dm
    w, V = mp.eighe(Qm)
    keep = [i for i in range(Qm.rows) if eps < w[i] < 1-eps]
    n = len(keep); P = mp.matrix(Qm.rows, n)
    for c, i in enumerate(keep):
        for r in range(Qm.rows): P[r, c] = V[r, i]
    return [w[i] for i in keep], P.H*Qt*P, P.H*Qm*P


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "brute"):
        print("=== (1) the three fidelity routes vs brute-force Fock trace (n<=4) ===", flush=True)
        mp.mp.dps = 40
        rng = np.random.default_rng(7)
        for n in [1, 2, 3, 4]:
            def rq(n):
                B = rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n)); H = B+B.conj().T
                _, U = np.linalg.eigh(H); q = 1/(1+np.exp(rng.normal(size=n)*2))
                return U @ np.diag(q) @ U.conj().T
            Q1, Q2 = rq(n), rq(n)
            Fb, Sb = brute_fock(Q1, Q2)
            M1, M2 = to_mp(Q1), to_mp(Q2)
            a_, b_, c_ = logfid_route_A(M1, M2), logfid_route_B(M1, M2), logfid_route_C(M1, M2)
            Smp = relent_mp(M1, M2)
            print(f"  n={n}: -logF brute={-np.log(Fb):.14f}  A={float(a_.real):.14f}  "
                  f"B={float(b_.real):.14f}  C={float(c_.real):.14f} | S brute={Sb:.12f} mp={float(Smp):.12f}", flush=True)

    if mode in ("all", "phi"):
        print("\n=== (2) Phi(1/15) at eps=1e-8: reproduce and cross-check; xi0-phase test ===", flush=True)
        z = np.load(NUM+"Dhat_exact_s0.2_Lam60_k30_g12.npz", allow_pickle=True)
        Dph = z['Dhat']; kap = z['kappa']; Lam = float(z['Lam']); s = float(z['s'])
        a, L = float(z['a']), float(z['L']); zeta = a*s/(a+L)
        Q = Q_box(kap, Lam)
        U = np.exp(-1j*(kap/(2*np.pi))*np.log(a/L))
        Dno = (U.conj()[:, None]*Dph*U[None, :])          # remove the xi0 phase
        eps = 1e-8; kc = np.log((1-eps)/eps); tail = zeta**2/(15*kc**2)
        for label, Dm in [("code (Dhat WITH xi0 phase, Q_box without)", Dph),
                          ("consistent centred basis (both without xi0 phase)", Dno)]:
            ws, Qsub, Qsub_Q = subcompress(Q, Dm, eps)
            n = len(ws)
            A = logfid_route_A(mp.diag(ws), Qsub)
            B = logfid_route_B(mp.diag(ws), Qsub)
            print(f"  {label}:", flush=True)
            print(f"     n_sub={n}  kc={kc:.4f}  -logF_sub(route A)={float(A.real):.9e}  "
                  f"(route B)={float(B.real):.9e}  |A-B|={abs(float(A.real)-float(B.real)):.2e}", flush=True)
            print(f"     +tail={float(A.real)+tail:.9e}   /zeta^2={(float(A.real)+tail)/zeta**2:.7f}", flush=True)
        print(f"  note/table values: raw 3.432123e-05, corrected 3.519443e-05, tail={tail:.4e}", flush=True)
