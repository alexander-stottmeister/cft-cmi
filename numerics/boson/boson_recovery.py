"""Chiral free boson (U(1) current net, c=1): Petz-recovery defect Phi=-log F and
relative entropy D for the geometric compression k_s, in the modular frame.

CONVENTIONS (fixed once, used everywhere).
Current J, weight 1, vacuum 2-pt fn  <J(x)J(y)> = -1/(4 pi^2 (x-y-i0)^2)
 (=> Sugawara T = (1/2):JJ: has <T T> = (1/(8 pi^2))(x-y-i0)^{-4}, i.e. c = 1).
Smeared J(f) = int f J dx with real f in C_c^inf.  Then
 <J(f)J(g)> = (1/(4 pi^2)) int_0^inf p conj(fhat(p)) ghat(p) dp,   fhat(p)=int e^{ipx}f dx,
 [J(f),J(g)] = (i/(2 pi)) int f g' dx.
Gaussian/quadrature convention (Banchi-Braunstein-Pirandola, Weedbrook): [x_j,x_k]=2i Om_jk,
 V_jk = (1/2)<{x_j,x_k}>, vacuum V = Id, symplectic eigenvalues nu >= 1.  With x = J(b_j):
 Om(f,g) = (1/(4 pi)) int f g' dx,   V(f,g) = Re <J(f)J(g)> = (1/(8 pi^2)) int |p| conj(fhat) ghat dp
         = (1/(8 pi^2)) int int (f(x)-f(y))(g(x)-g(y))/(x-y)^2 dx dy   [Moebius invariant].
Test functions are weight 0 (f |-> f o k^{-1}), equivalently the current is pushed forward
 with weight 1: U_s J(f) U_s^* = J(f o k_s^{-1}).  Recovered state on A(I):
 V_s(f,g) := V(f o k_s, g o k_s),  Om unchanged (Om is diffeo invariant).

MODULAR FRAME.  I = (-a,L); y = (x+a)/(L-x) maps I -> (0,inf); t = log y.  Then
 Om(f,g) = (1/(4 pi)) int_R f dg/dt dt      (diffeo invariant)
 V(f,g) = (1/(8 pi^3)) int_R M(k) conj(fhat(k)) ghat(k) dk,   M(k) = pi k coth(pi k),
 i.e. symplectic-eigenvalue density nu(k) = M(k)/(pi|k|) = coth(pi k) = 1 + 2/(e^{2 pi|k|}-1):
 the Bose factor of the modular (boost) Hamiltonian at temperature 1/(2 pi).
 [Derivation: V = (1/(8 pi^2))[ int_{IxI}(Df)(Dg)/(x-y)^2 + 2 int_I f g (int_{I^c} dy/(x-y)^2) ];
  the first term -> kernel 1/(4 sinh^2((t-t')/2)) with symbol pi k coth(pi k) - 1, the collar
  term -> 2 int f g dt, symbol +1.]
"""
import numpy as np, scipy.linalg as sla, sys

# ---------- Fock-space reference implementation (validation only) ----------
def fock_ops(nmodes, ncut):
    """q_j, p_j on (C^ncut)^{otimes nmodes} with [q,p]=2i:  q=a+a^dag, p=-i(a-a^dag)."""
    a1 = np.diag(np.sqrt(np.arange(1, ncut)), 1)
    ops = []
    for j in range(nmodes):
        mats = [np.eye(ncut)] * nmodes
        mats[j] = a1
        A = mats[0]
        for m in mats[1:]:
            A = np.kron(A, m)
        ops.append((A + A.conj().T, -1j * (A - A.conj().T)))
    return [o for pair in ops for o in pair]      # order q1,p1,q2,p2,...

def gaussian_rho(W, nmodes, ncut):
    """rho propto exp(-(1/2) sum_jk W_jk (x_j x_k + x_k x_j)/2), W symmetric > 0."""
    X = fock_ops(nmodes, ncut)
    H = np.zeros_like(X[0], dtype=complex)
    for j in range(2 * nmodes):
        for k in range(2 * nmodes):
            H += 0.25 * W[j, k] * (X[j] @ X[k] + X[k] @ X[j])
    ev, U = np.linalg.eigh(H)
    ev = ev - ev.min()
    r = U @ np.diag(np.exp(-ev)) @ U.conj().T
    return r / np.trace(r).real

def cov_from_rho(rho, nmodes, ncut):
    X = fock_ops(nmodes, ncut)
    n = 2 * nmodes
    V = np.zeros((n, n))
    for j in range(n):
        for k in range(n):
            V[j, k] = 0.5 * np.trace(rho @ (X[j] @ X[k] + X[k] @ X[j])).real
    return V

def fid_exact(r1, r2):
    s1 = sla.sqrtm(r1)
    M = sla.sqrtm(s1 @ r2 @ s1)
    return np.trace(M).real

def relent_exact(r1, r2):
    e1, U1 = np.linalg.eigh(r1); e2, U2 = np.linalg.eigh(r2)
    e1 = np.clip(e1, 1e-300, None); e2 = np.clip(e2, 1e-300, None)
    l2 = U2 @ np.diag(np.log(e2)) @ U2.conj().T
    return (np.sum(e1 * np.log(e1)) - np.trace(r1 @ l2).real)

# ---------- finite-dimensional Gaussian formulas (convention: vacuum V = Id, nu >= 1) ----
def Omega_std(n):
    O = np.zeros((2 * n, 2 * n))
    for j in range(n):
        O[2 * j, 2 * j + 1] = 1.0; O[2 * j + 1, 2 * j] = -1.0
    return O

def sympl_eig(V, Om):
    """symplectic eigenvalues nu_k >= 1 of V (vacuum-normalised) w.r.t. Om."""
    ev = np.sort(np.abs(np.linalg.eigvals(V @ (1j * Om)).real))
    return ev[1::2]          # the 2n eigenvalues are +-nu_k: each nu_k occurs twice

def _fun_W(V, Om, fun):
    """f(W) with W = V iOm (eigenvalues +-nu_k), returned as the matrix 2 iOm f(W)."""
    W = V @ (1j * Om)
    lam, S = np.linalg.eig(W)
    Fm = S @ np.diag(fun(lam)) @ np.linalg.inv(S)
    return (2j * Om @ Fm)

def gibbs(V, Om):
    """G with rho = exp(-(1/2) Q^T G Q)/Z, Q the BBP quadratures (V_BBP = V/2)."""
    G = _fun_W(V, Om, lambda l: 0.5 * np.log((l + 1) / (l - 1)))   # arccoth
    return 0.5 * (G + G.T).real

def gfun(nu):
    x = np.clip((nu - 1) / 2, 0, None); y = (nu + 1) / 2
    return y * np.log(y) - np.where(x > 0, x * np.log(np.maximum(x, 1e-300)), 0.0)

def entropy(V, Om):
    return float(np.sum(gfun(sympl_eig(V, Om))))

def relent(V1, V2, Om):
    """D(rho_1 || rho_2) for zero-mean Gaussians."""
    G2 = gibbs(V2, Om)
    return float(entropy(V2, Om) - entropy(V1, Om) + 0.25 * np.trace(G2 @ (V1 - V2)))

def fidelity(V1, V2, Om):
    """Banchi-Braunstein-Pirandola arXiv:1507.01941 Eqs. (11),(12),(15); zero mean."""
    W1 = V1 @ (1j * Om); W2 = V2 @ (1j * Om)
    Wa = -np.linalg.solve(W1 + W2, np.eye(len(W1)) + W2 @ W1)
    w = np.linalg.eigvals(Wa).real
    w = np.sort(w)[len(w) // 2:]
    w = np.maximum(w, 1.0)
    Ft = np.prod(np.sqrt(w + np.sqrt(w * w - 1)))
    return float(Ft / np.linalg.det(0.5 * (V1 + V2)) ** 0.25)

def logfid(V1, V2, Om):
    """-log F, computed additively (avoids catastrophic cancellation for F -> 1)."""
    W1 = V1 @ (1j * Om); W2 = V2 @ (1j * Om)
    Wa = -np.linalg.solve(W1 + W2, np.eye(len(W1)) + W2 @ W1)
    w = np.linalg.eigvals(Wa).real
    w = np.sort(w)[len(w) // 2:]
    w = np.maximum(w, 1.0)
    sl, ld = np.linalg.slogdet(0.5 * (V1 + V2))
    return float(0.25 * ld - 0.5 * np.sum(np.log(w + np.sqrt(w * w - 1))))

# ---------------------------- validation against Fock space ---------------------------
def _rand_V(n, rng, T=0.8, a=0.35):
    Om = Omega_std(n)
    A = rng.normal(size=(2 * n, 2 * n)) * a
    S = sla.expm(Om @ (A + A.T) / 2)                       # symplectic
    nu = 1 + T * rng.random(n)
    D = np.diag(np.repeat(nu, 2))
    return S @ D @ S.T, Om

def validate(nmodes=1, ncut=26, ntest=3, seed=1, T=0.8, a=0.35):
    rng = np.random.default_rng(seed); out = []
    for _ in range(ntest):
        V1, Om = _rand_V(nmodes, rng, T, a); V2, _ = _rand_V(nmodes, rng, T, a)
        r1 = gaussian_rho(gibbs(V1, Om) / 2, nmodes, ncut)   # /2: G is for BBP quadratures
        r2 = gaussian_rho(gibbs(V2, Om) / 2, nmodes, ncut)
        c1 = cov_from_rho(r1, nmodes, ncut)
        out.append((np.abs(c1 - V1).max(), abs(fid_exact(r1, r2) - fidelity(V1, V2, Om)),
                    abs(relent_exact(r1, r2) - relent(V1, V2, Om))))
    return np.array(out)

if __name__ == "__main__" and "validate" in sys.argv:
    for nm, nc, T, a in ((1, 60, 0.8, 0.35), (2, 26, 0.5, 0.18), (3, 12, 0.35, 0.12)):
        e = validate(nm, nc, 3, T=T, a=a)
        print(f"modes={nm} ncut={nc}: max|dV|={e[:,0].max():.2e} "
              f"max|dF|={e[:,1].max():.2e} max|dD|={e[:,2].max():.2e}", flush=True)

# ======================= modular frame of I = (-a, L), a = 1, L = 2 ====================
A_, L_ = 1.0, 2.0
T0 = np.log(A_ / L_)                       # modular coordinate of the kink x = 0
tau     = lambda x: np.log((x + A_) / (L_ - x))
tau_inv = lambda t: (L_ * np.exp(t) - A_) / (1.0 + np.exp(t))
hinv    = lambda y, s: L_ * y / (L_ - s * y)          # h_s^{-1} on D = (0,L)
beta    = lambda v, s: tau(hinv(tau_inv(v), s))       # h_s^{-1} in the modular frame

def herm(nmax, u):
    """phi_n(u) = H_n(u) e^{-u^2/2}/(pi^{1/4} sqrt(2^n n!)), n = 0..nmax-1; shape (nmax,|u|)."""
    P = np.empty((nmax, len(u)))
    P[0] = np.pi ** -0.25 * np.exp(-u * u / 2)
    if nmax > 1: P[1] = np.sqrt(2.0) * u * P[0]
    for n in range(1, nmax - 1):
        P[n + 1] = np.sqrt(2.0 / (n + 1)) * u * P[n] - np.sqrt(n / (n + 1.0)) * P[n - 1]
    return P

def gl(a, b, npan, ngl, grade=None):
    """Gauss-Legendre nodes/weights on [a,b]; grade='left'/'right' = geometric refinement."""
    g, gw = np.polynomial.legendre.leggauss(ngl)
    if grade is None:  e = np.linspace(a, b, npan + 1)
    elif grade == 'right':  e = b - (b - a) * np.geomspace(1.0, 1e-9, npan + 1); e[-1] = b
    else:  e = a + (b - a) * np.geomspace(1.0, 1e-9, npan + 1)[::-1]; e[-1] = b
    x = []; w = []
    for j in range(npan):
        hm = 0.5 * (e[j + 1] - e[j]); mid = 0.5 * (e[j] + e[j + 1])
        x.append(mid + hm * g); w.append(gw * hm)
    return np.concatenate(x), np.concatenate(w)

class Basis:
    """Hermite modes psi_n(t) = sig^{-1/2} phi_n((t-tc)/sig), n = 0..N-1, in the modular frame.
    Effective box  Lam = 2 sig sqrt(2N),  UV cutoff  kap_max = sqrt(2N)/sig."""
    def __init__(o, N, sig, tc=T0, npan=28, ngl=24):
        o.N, o.sig, o.tc = N, sig, tc
        o.Lam, o.kmax = 2 * sig * np.sqrt(2 * N), np.sqrt(2 * N) / sig
        # ---- Omega (exact): Om_mn = (1/(4 pi sig)) [sqrt(n/2) d_{m,n-1} - sqrt((n+1)/2) d_{m,n+1}]
        o.Om = np.zeros((N, N))
        for n in range(N):
            if n >= 1: o.Om[n - 1, n] += np.sqrt(n / 2.0) / (4 * np.pi * o.sig)
            if n + 1 < N: o.Om[n + 1, n] -= np.sqrt((n + 1) / 2.0) / (4 * np.pi * o.sig)
        # ---- V (exact symbol M(k) = pi k coth(pi k)):  V_mn = (1/(4 pi^2)) i^{n-m} int M(u/sig) ph_m ph_n
        U = np.sqrt(2 * N + 2) + 8.0
        uu, wu = gl(-U, U, npan, ngl)
        Ph = herm(N, uu)
        o._Ph, o._uu, o._wu = Ph, uu, wu
        ph = lambda x: np.where(np.abs(x) < 1e-12, 1.0 + (np.pi * x) ** 2 / 3, np.pi * x / np.tanh(np.pi * x))
        o.V = o._sym(ph(uu / sig) * wu, Ph)
        o.Vflat = o._sym(np.pi * np.abs(uu / sig) * wu, Ph)     # symbol pi|k| : must be pure
    def _sym(o, wgt, Ph):
        M = (Ph * wgt) @ Ph.T / (4 * np.pi ** 2)
        n = np.arange(o.N); ph = np.real(1j ** (n[None, :] - n[:, None]))
        return M * ph
    def dV(o, s, npan=26, ngl=24, R=None):
        """DeltaV = V_s - V, V_s(f,g) = V(f o k_s^{-1}, g o k_s^{-1}); exact localisation:
        DeltaV(f,g) = -(1/(4 pi^2)) int_A du int_D dv [f(u) Gg(v) + g(u) Gf(v)]/(4 sinh^2((u-v)/2)),
        Gf(v) = f(beta_s(v)) - f(v)   (A = (-inf,T0), D = (T0,inf) in the modular frame)."""
        R = R or (o.sig * np.sqrt(2 * o.N + 2) + 8.0)
        tmax = np.log((L_ / (1 + s) + A_) / (L_ - L_ / (1 + s)))   # tau(L/(1+s)); beta undefined above
        uu, wu = gl(o.tc - R, T0, npan, ngl, grade='right')
        v1, w1 = gl(T0, tmax, npan, ngl, grade='left')             # push-forward region
        v2, w2 = gl(tmax, o.tc + R, max(npan // 2, 6), ngl)        # beyond k_s(I): only -psi
        vv = np.concatenate([v1, v2]); wv = np.concatenate([w1, w2])
        Pu = herm(o.N, (uu - o.tc) / o.sig) / np.sqrt(o.sig)
        Pv = herm(o.N, (vv - o.tc) / o.sig) / np.sqrt(o.sig)
        Pb = np.zeros_like(Pv)
        Pb[:, :len(v1)] = herm(o.N, (beta(v1, s) - o.tc) / o.sig) / np.sqrt(o.sig)
        K = 1.0 / (4 * np.sinh((uu[:, None] - vv[None, :]) / 2) ** 2)
        C = (Pu * wu) @ K @ ((Pb - Pv) * wv).T
        return -(C + C.T) / (4 * np.pi ** 2)      # position-space form: NO i^{n-m} phase

# ------------- change to a standard symplectic basis (Om -> Om_std = +-1 blocks) -------
def to_standard(Om, *Vs):
    """A with A^T Om A = Omega_std; returns (Om_std, A^T V A for each V).
    Needed because V and Om are BILINEAR FORMS: only Om^{-1}V is basis independent, and
    the BBP/Williamson formulas below are written for the standard symplectic basis."""
    T, Z = sla.schur(Om, output='real')
    n = len(Om) // 2
    cols = []
    for j in range(n):
        b = T[2 * j, 2 * j + 1]
        c1, c2 = (Z[:, 2 * j], Z[:, 2 * j + 1]) if b > 0 else (Z[:, 2 * j + 1], Z[:, 2 * j])
        s = 1.0 / np.sqrt(abs(b)); cols += [c1 * s, c2 * s]
    A = np.array(cols).T
    return Omega_std(n), [A.T @ V @ A for V in Vs]

def relent_exact2(W1, W2, nmodes, ncut):
    """D(rho1||rho2) from the exact Fock-space quadratic Hamiltonians (numerically stable)."""
    X = fock_ops(nmodes, ncut); D = []
    for W in (W1, W2):
        H = np.zeros_like(X[0], dtype=complex)
        for j in range(2 * nmodes):
            for k in range(2 * nmodes):
                H += 0.25 * W[j, k] * (X[j] @ X[k] + X[k] @ X[j])
        ev, U = np.linalg.eigh(H); ev = ev - ev.min()
        p = np.exp(-ev); Z = p.sum(); D.append((ev, U, np.log(Z), p / Z))
    (e1, U1, lZ1, p1), (e2, U2, lZ2, p2) = D
    r1 = U1 @ np.diag(p1) @ U1.conj().T
    S1 = -float(np.sum(p1 * np.log(np.maximum(p1, 1e-300))))
    H2 = U2 @ np.diag(e2) @ U2.conj().T
    return -S1 + float(np.trace(r1 @ H2).real) + lZ2

def williamson(V, Om):
    """A with A^T Om A = Om_std and A^T V A = diag(nu_1,nu_1,nu_2,nu_2,...)."""
    ev, U = np.linalg.eigh(V)
    Ri = U @ np.diag(ev ** -0.5) @ U.T
    M = Ri @ Om @ Ri
    T, Q = sla.schur(M, output='real')
    n = len(V) // 2; cols = []; nu = np.empty(n)
    for j in range(n):
        b = T[2 * j, 2 * j + 1]
        c1, c2 = (Q[:, 2 * j], Q[:, 2 * j + 1]) if b > 0 else (Q[:, 2 * j + 1], Q[:, 2 * j])
        nu[j] = 1.0 / abs(b); s = np.sqrt(nu[j]); cols += [c1 * s, c2 * s]
    o = np.argsort(-nu)                                  # IR (large nu) first
    A = Ri @ np.array(cols).T
    perm = np.concatenate([[2 * j, 2 * j + 1] for j in o])
    return nu[o], A[:, perm]

def run(N, sig, s, eps=1e-11, tc=T0, npan=26, ngl=24, b=None):
    """Phi = -log F(omega, omega_s) and D(omega_s||omega) on the mode-compressed algebra."""
    b = b or Basis(N, sig, tc)
    Os, (V0, Vs0) = to_standard(b.Om, b.V, b.V + b.dV(s, npan, ngl))
    nu, A = williamson(V0, Os)
    keep = nu - 1.0 > eps
    idx = np.concatenate([[2 * j, 2 * j + 1] for j in np.where(keep)[0]]).astype(int)
    Aw = A[:, idx]; Ow = Omega_std(len(idx) // 2)
    nk = nu[keep]
    V1 = np.diag(np.repeat(nk, 2))          # exact by construction (Williamson basis)
    V2 = Aw.T @ Vs0 @ Aw
    # D(omega_s || omega) with the EXACT Gibbs matrix of the vacuum block, G1 = 2 arccoth(nu):
    G1 = np.diag(np.repeat(2 * np.arctanh(1.0 / nk), 2))
    D = float(np.sum(gfun(nk)) - np.sum(gfun(sympl_eig(V2, Ow)))
              + 0.25 * np.trace(G1 @ (V2 - V1)))
    return dict(n=int(keep.sum()), numax=nu.max(), nucut=nk.min(),
                Phi=logfid(V1, V2, Ow), D=D, b=b)

# =========================== exact second-order (s -> 0) coefficients ==================
def dVp(o, npan=40, ngl=32, R=None):
    """E' = d(DeltaV)/ds at s=0.  Gf'(v) = psi'(v) gam(v), gam = tau'(y) y^2/L, y = tau^{-1}(v)."""
    R = R or (o.sig * np.sqrt(2 * o.N + 2) + 8.0)
    uu, wu = gl(o.tc - R, T0, npan, ngl, grade='right')
    vv, wv = gl(T0, o.tc + R, npan, ngl, grade='left')
    e = np.exp(vv); gam = (L_ * e - A_) ** 2 / (L_ * (L_ + A_) * e)   # = tau'(y) y^2/L, stable
    Pu = herm(o.N, (uu - o.tc) / o.sig) / np.sqrt(o.sig)
    Pv = herm(o.N, (vv - o.tc) / o.sig) / np.sqrt(o.sig)
    dP = np.empty_like(Pv); z = (vv - o.tc) / o.sig
    for n in range(o.N):                                    # phi_n' = sqrt(n/2)phi_{n-1}-sqrt((n+1)/2)phi_{n+1}
        a = np.sqrt(n / 2.0) * Pv[n - 1] if n >= 1 else 0.0
        b = np.sqrt((n + 1) / 2.0) * (herm(n + 2, z)[n + 1] / np.sqrt(o.sig))
        dP[n] = (a - b) / o.sig
    K = 1.0 / (4 * np.sinh((uu[:, None] - vv[None, :]) / 2) ** 2)
    C = (Pu * wu) @ K @ ((dP * gam) * wv).T
    return -(C + C.T) / (4 * np.pi ** 2)

def _Wbasis(nu):
    """U (unitary) and w with W = V iOm = U diag(w) U^dag for V = diag(nu)x I_2, Om standard."""
    n = len(nu); U = np.zeros((2 * n, 2 * n), complex); w = np.empty(2 * n)
    for k in range(n):
        U[2 * k:2 * k + 2, 2 * k:2 * k + 2] = np.array([[1, 1], [-1j, 1j]]) / np.sqrt(2)
        w[2 * k], w[2 * k + 1] = nu[k], -nu[k]
    return U, w

def second_order(N, sig, eps=1e-12, tc=T0, npan=40, ngl=32, b=None):
    """Phi = Phi2 s^2 + O(s^3), D = D2 s^2 + O(s^3);  f2 = 9 Phi2, s2 = 9 D2 (zeta = s/3)."""
    b = b or Basis(N, sig, tc)
    Os, (V0, Ep0) = to_standard(b.Om, b.V, dVp(b, npan, ngl))
    nu, A = williamson(V0, Os)
    keep = nu - 1.0 > eps
    idx = np.concatenate([[2 * j, 2 * j + 1] for j in np.where(keep)[0]]).astype(int)
    Aw = A[:, idx]; nk = nu[keep]; m = len(nk)
    E = Aw.T @ Ep0 @ Aw; Om = Omega_std(m)
    U, w = _Wbasis(nk)
    dW = U.conj().T @ (E @ (1j * Om)) @ U
    P = np.outer(w, w) - 1.0
    ok = np.abs(P) > 1e-13
    Phi2 = float(np.sum(np.where(ok, dW * dW.T / np.where(ok, P, 1.0), 0.0)).real) / 16.0
    ac = lambda x: 0.5 * np.log((x + 1) / (x - 1))       # arccoth, |x| > 1, both signs
    dd = w[:, None] - w[None, :]
    Dl = np.where(np.abs(dd) > 1e-12, (ac(w)[:, None] - ac(w)[None, :]) / np.where(np.abs(dd) > 1e-12, dd, 1.0),
                  1.0 / (1.0 - w[:, None] ** 2))
    dG = 2j * Om @ (U @ (dW * Dl) @ U.conj().T)
    D2 = -0.125 * float(np.trace(dG @ E).real)
    return dict(n=m, Phi2=Phi2, D2=D2, f2=9 * Phi2, s2=9 * D2, b=b)

# ================= (3) c-linearity of the vacuum overlap: boson vs fermion =============
# One-particle spaces for the SAME circle diffeo phi = k~_s (p1_bogoliubov.KMapOpt):
#   fermion (weight 1/2): (W f)(x) = f(psi(x)) psi'(x)^{1/2},  psi = phi^{-1};  V = P_- W P_+,
#     -log|<Om,Gamma_f Om>| = -(1/2) Tr log(1 - V^*V) = (1/2) E + O(s^3),  E = ||V||_2^2.
#   boson  (weight 0)   : (T f)(x) = f(psi(x)) on the H^{1/2} space; in the ORTHONORMAL Fourier
#     basis e_k/sqrt|k| the matrix is M_{nm} = sqrt(|k_n|/|k_m|) (1/2X) int e^{-i k_n x + i k_m psi(x)} dx,
#     B = P_- M P_+,  -log|<Om,Gamma_b Om>| = (1/4) Tr log(1 + B^*B) = (1/4)Tr(B^*B) + O(s^3).
# Analytic first order (phi = x + s g):  M(p,q) = delta + (i s/2pi) sqrt(|p/q|) q ghat(p-q),
#   Tr(B^*B) = (s^2/(24 pi^2)) int_0^inf k^3 |ghat|^2 dk  =  2 E,  hence both -log|overlap| equal
#   (s^2/(96 pi^2)) int_0^inf k^3 |ghat(k)|^2 dk = (s^2/2)||T(g)Omega||^2 with the same c = 1.
def overlap_blocks(mp, X=25.0, Ngr=16384, Mmax=160):
    h = 2 * X / Ngr; y = -X + h * np.arange(Ngr)
    z = y.copy()
    for _ in range(80):
        z = z - ((z - mp.u(z)) - y) / (1.0 - mp.du(z))     # z = psi(y) = phi^{-1}(y)
    dpsi = 1.0 / (1.0 - mp.du(z))
    kp = np.pi * np.arange(1, Mmax + 1) / X; kn = -kp[::-1]
    En = np.exp(-1j * np.outer(kn, y))                     # (Mmax, Ngr)
    sq = np.sqrt(dpsi); Wf = np.empty((Mmax, Mmax), complex); Cb = np.empty_like(Wf)
    for i in range(0, Mmax, 64):                           # chunked: <e_n, . e_m>
        Ep = np.exp(1j * np.outer(kp[i:i + 64], z))
        Wf[i:i + 64] = (Ep * sq[None, :]) @ En.T / Ngr     # fermion (weight 1/2)
        Cb[i:i + 64] = Ep @ En.T / Ngr                     # boson   (weight 0)
    Mb = Cb * np.sqrt(np.abs(kn)[None, :] / kp[:, None])   #   ... x sqrt(|k_n|/|k_m|)
    return Wf.T, Mb.T                                      # rows: n<0, cols: m>0

def overlap_compare(svals=(0.4, 0.2, 0.1, 0.05, 0.025), nb=16, X=25.0, Ngr=16384, Mmax=160):
    import p1_bogoliubov as P1
    _, cf, Bs, _ = P1.minQ(nb)
    G = P1.gopt(cf, Bs); out = []
    for s in svals:
        mp = P1.KMapOpt(s, G)
        V, Bm = overlap_blocks(mp, X, Ngr, Mmax)
        E = float(np.sum(np.abs(V) ** 2)); TB = float(np.sum(np.abs(Bm) ** 2))
        sv = np.linalg.svd(V, compute_uv=False); sb = np.linalg.svd(Bm, compute_uv=False)
        lf = -0.5 * float(np.sum(np.log1p(-np.minimum(sv, 1 - 1e-14) ** 2)))
        lb = 0.25 * float(np.sum(np.log1p(sb ** 2)))
        out.append((s, E, TB, TB / (2 * E), lf, lb, lb / lf))
    return out

# ======================================= driver =======================================
def main():
    from scipy.optimize import curve_fit
    print("=== 0. validation of the finite-dimensional Gaussian formulas vs exact Fock space ===")
    rng = np.random.default_rng(7)
    for nm, nc, T, a in ((1, 60, 0.8, 0.35), (2, 22, 0.5, 0.18), (3, 10, 0.35, 0.12)):
        V1, Om = _rand_V(nm, rng, T, a); V2, _ = _rand_V(nm, rng, T, a)
        r1 = gaussian_rho(gibbs(V1, Om) / 2, nm, nc); r2 = gaussian_rho(gibbs(V2, Om) / 2, nm, nc)
        print(f" modes={nm} ncut={nc}: max|V_Fock-V|={np.abs(cov_from_rho(r1,nm,nc)-V1).max():.2e}"
              f"  |F_Fock-F_BBP|={abs(fid_exact(r1,r2)-fidelity(V1,V2,Om)):.2e}"
              f"  |D_Fock-D_Gauss|={abs(relent_exact2(gibbs(V1,Om)/2,gibbs(V2,Om)/2,nm,nc)-relent(V1,V2,Om)):.2e}",
              flush=True)
    print("\n=== 1. modular frame: purity of the flat symbol pi|k| (must give nu = 1) ===")
    for N, sg in ((60, 1.6), (120, 1.6)):
        b = Basis(N, sg); Os, (Vf,) = to_standard(b.Om, b.Vflat)
        nf = sympl_eig(Vf, Os)
        print(f" N={N} sig={sg}: nu_flat in [{nf.min():.9f},{nf.max():.4f}], median {np.median(nf):.9f}")
    print("\n=== 2. finite-s scan  (a=1, L=2, zeta=s/3), eps = 1e-12 window ===")
    print("   s      zeta      n    Phi=-log F     Phi/zeta^2    D(w_s||w)      D/zeta^2")
    for N, sg in ((60, 1.6), (120, 1.6)):
        b = Basis(N, sg)
        print(f" -- N={N} sig={sg} Lam={b.Lam:.1f} kmax={b.kmax:.2f}")
        for s in (0.4, 0.2, 0.1, 0.05, 0.025):
            r = run(N, sg, s, eps=1e-12, b=b); z = s / 3
            print(f" {s:6.4f} {z:8.5f} {r['n']:4d} {r['Phi']:.6e}  {r['Phi']/z**2:.6f}  "
                  f"{r['D']:.6e}  {r['D']/z**2:.6f}", flush=True)
    print("\n=== 3. exact second-order coefficients f2 = 9 lim Phi/s^2, s2 = 9 lim D/s^2 ===")
    print("  window eps -> kappa_c = log(2/eps)/(2 pi);  target 1/(12 pi^2)=0.00844343, 1/12=0.08333333")
    res = {}
    for N, sg in ((60, 1.6), (120, 1.6), (120, 2.26)):
        b = Basis(N, sg); K = []; F = []; S = []
        for k in range(4, 15):
            e = 10.0 ** -k; r = second_order(N, sg, e, b=b)
            K.append(np.log(2 / e) / (2 * np.pi)); F.append(r['f2']); S.append(r['s2'])
        K, F, S = np.array(K), np.array(F), np.array(S)
        print(f" -- N={N} sig={sg} (Lam={b.Lam:.1f}, kmax={b.kmax:.2f})")
        for kc, f2, s2 in zip(K, F, S):
            print(f"    kappa_c={kc:5.2f}   f2={f2:.7f}   s2={s2:.7f}")
        for nm, Y in (("f2", F), ("s2", S)):
            fp, _ = curve_fit(lambda k, A, c, p: A - c * k ** -p, K[2:], Y[2:],
                              p0=[Y[-1] * 1.05, 0.01, 2.0], maxfev=60000)
            a2, _ = curve_fit(lambda k, A, c: A - c / k ** 2, K[2:], Y[2:], p0=[Y[-1], .01])
            a1, _ = curve_fit(lambda k, A, c: A - c / k, K[2:], Y[2:], p0=[Y[-1], .01])
            print(f"    {nm} tail fits: free p={fp[2]:.2f} -> {fp[0]:.7f} | p=2 -> {a2[0]:.7f} | p=1 -> {a1[0]:.7f}")
            res[(N, sg, nm)] = (fp[0], a2[0], a1[0])
    print("\n=== 4. c-linearity of the vacuum overlap (same diffeo k~_s, extension beta=1) ===")
    import p1_bogoliubov as P1
    Qg = P1.Q_of(P1.Field(1.0, 0.0, 0.0, 1.0))
    print(f"  Q[g] = (1/(48 pi^2)) int_0^inf k^3 |ghat|^2 dk = {Qg:.8f}")
    print("  box: X=100, 2^15 grid, |k|<=20.1.  E_box underestimates E (IR, ~1/X); E_quad is box free.")
    print("    s      s^2 Q       E_quad        E_box       Tr(B*B)_box   Tr(B*B)/(2E_quad)  -logF_f  -logF_b")
    for s in (0.4, 0.2, 0.1, 0.05, 0.025):
        mp = P1.KMap(s, be=1.0)
        V, Bm = overlap_blocks(mp, 100.0, 1 << 15, 640)
        E = float(np.sum(np.abs(V) ** 2)); TB = float(np.sum(np.abs(Bm) ** 2))
        Eq = P1.E_of(mp, P1.BRK)
        sv = np.linalg.svd(V, compute_uv=False); sb = np.linalg.svd(Bm, compute_uv=False)
        lf = -0.5 * float(np.sum(np.log1p(-np.minimum(sv, 1 - 1e-14) ** 2)))
        lb = 0.25 * float(np.sum(np.log1p(sb ** 2)))
        print(f" {s:6.4f} {s*s*Qg:.5e} {Eq:.5e} {E:.5e} {TB:.5e}   {TB/(2*Eq):.6f}   "
              f"{lf:.5e} {lb:.5e}", flush=True)

if __name__ == "__main__" and "run" in sys.argv:
    main()
