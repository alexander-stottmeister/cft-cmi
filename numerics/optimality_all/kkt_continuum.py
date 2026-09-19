"""S11(b): continuum modular-frame discretisation of the quasi-free second-order programme,
SLD certificate t_c of the zero-collar compression defect, and the linear programme Delta(t_c).

Frame.  A=(-a,0), B=(0,b), C=(b,L), D=BC=(0,L), b=L/(1+s), zeta = a s/(a+L) (= the cross ratio
z of the geometry).  Modular coordinate of the interval AD=(-a,L):
  xi = log((x+a)/(L-x)),   x(xi) = (L e^xi - a)/(1+e^xi),   beta(x) = (x+a)(L-x)/(a+L) = dx/dxi.
In half-density form the vacuum symbol is the translation-invariant kernel (defect_matrix.py)
  qt(t) = delta(t)/2 - (i/4pi)/sinh(t/2),   Fourier symbol 1/(1+e^kappa), kappa = 2 pi k.
Zero-collar compression defect (Note 4 / defect_matrix.py), on A x D and its adjoint:
  Dt(xi,xi') = (i/2pi) sqrt(beta(x)beta(y)) R_s(-x, y),  x = x(xi) < 0 < y = x(xi'),
  R_s(u,v) = s u v /((u+v)(L(u+v) + s u v))      ['exact']   or  (s/L) u v/(u+v)^2  ['first'].

Discretisation.  GALERKIN in the piecewise-constant ("cell") basis of the modular coordinate:
uniform cells of width ~h on [xi0-LamA, xi1+LamC], with the two corners xi0 = log(a/L) and
xi1 = log((a+b)/(L-b)) EXACTLY on the grid.  Then h_A, h_B, h_C are exact coordinate subspaces
(unlike the box-Fourier frame of compression_box.py), so the feasible set F of S8 makes literal
sense.  Cell matrix elements of the vacuum kernel are CLOSED FORM: with
  F2(t) = -4( Li2(-e^{-t/2}) - Li2(e^{-t/2}) + pi^2/4 ) for t>0, F2 odd, F2'' = 1/sinh(t/2),
  int_{[al,be]} int_{[ga,de]} dxi dxi' / sinh((xi-xi')/2)
     = F2(be-ga) - F2(al-ga) - F2(be-de) + F2(al-de).
The defect cell integrals are done by tensor Gauss-Legendre, with a geometrically graded
sub-rule on the two cells touching the corner xi0 (the kernel is scale invariant there).
"""
import sys, os, numpy as np
from scipy.special import spence
HERE = os.path.dirname(os.path.abspath(__file__))

def Li2(y):
    return spence(1.0 - y)

def F2(t):
    at = np.abs(t); e = np.exp(-at / 2.0)
    v = -4.0 * (Li2(-e) - Li2(e) + np.pi ** 2 / 4.0)
    return np.sign(t) * v

def mesh(a, L, s, h, LamA, LamC, hB=None, hC=None):
    """Cell edges in xi; returns (edges, nA, nB, nC).  Piecewise uniform: width ~h on A,
    ~hB on B (default h), ~hC on C (default h).  The corners xi0, xi1 are exact grid points."""
    b = L / (1.0 + s); hB = h if hB is None else hB; hC = h if hC is None else hC
    xi0 = np.log(a / L); xi1 = np.log((a + b) / (L - b))
    nA = max(1, int(round(LamA / h))); nB = max(1, int(round((xi1 - xi0) / hB)))
    nC = max(1, int(round(LamC / hC)))
    eA = xi0 - LamA + np.arange(nA + 1) * (LamA / nA)
    eB = xi0 + np.arange(nB + 1) * ((xi1 - xi0) / nB)
    eC = xi1 + np.arange(nC + 1) * (LamC / nC)
    edges = np.concatenate([eA[:-1], eB[:-1], eC])
    return edges, nA, nB, nC, xi0, xi1, b

def Qmat(edges):
    al = edges[:-1]; be = edges[1:]; hh = be - al
    I = (F2(be[:, None] - al[None, :]) - F2(al[:, None] - al[None, :])
         - F2(be[:, None] - be[None, :]) + F2(al[:, None] - be[None, :]))
    Q = -1j / (4 * np.pi) * I / np.sqrt(np.outer(hh, hh))
    Q = Q + 0.5 * np.eye(len(hh))
    return 0.5 * (Q + Q.conj().T)

def _nodes(al, be, ng, graded_at=None, K=24, r=0.55):
    """GL nodes/weights on [al,be]; if graded_at is an endpoint, use geometric subdivision there."""
    xg, wg = np.polynomial.legendre.leggauss(ng)
    if graded_at is None:
        return (al + be) / 2 + (be - al) / 2 * xg, (be - al) / 2 * wg
    H = be - al; cuts = [0.0]
    d = H
    for _ in range(K):
        d *= r; cuts.append(H - d)
    cuts.append(H); cuts = np.array(sorted(set(cuts)))
    if graded_at == 'left':
        pts = al + cuts
    else:
        pts = be - cuts[::-1]
    lo, hi = pts[:-1], pts[1:]
    n = (lo + hi)[:, None] / 2 + (hi - lo)[:, None] / 2 * xg[None, :]
    w = (hi - lo)[:, None] / 2 * wg[None, :]
    return n.ravel(), w.ravel()

def defect(edges, nA, a, L, s, kind='exact', ng=10):
    """Dhat = Q - Qrec(compression), Hermitian, supported on the A-D blocks."""
    N = len(edges) - 1
    al, be = edges[:-1], edges[1:]; hh = be - al
    xof = lambda xi: (L * np.exp(xi) - a) / (1 + np.exp(xi))
    bet = lambda x: (x + a) * (L - x) / (a + L)
    if kind == 'exact':
        kern = lambda u, v: s * u * v / ((u + v) * (L * (u + v) + s * u * v))
    else:
        kern = lambda u, v: (s / L) * u * v / (u + v) ** 2
    # quadrature nodes per cell (graded on the cells touching the corner xi0 = edges[nA])
    nod, wei = [], []
    for m in range(N):
        g = 'right' if m == nA - 1 else ('left' if m == nA else None)
        n_, w_ = _nodes(al[m], be[m], ng, graded_at=g)
        nod.append(n_); wei.append(w_)
    J = np.zeros((nA, N - nA), dtype=complex)
    for m in range(nA):
        xm = xof(nod[m]); sm = np.sqrt(bet(xm)) * wei[m]
        for n in range(nA, N):
            yn = xof(nod[n]); sn = np.sqrt(bet(yn)) * wei[n]
            J[m, n - nA] = sm @ kern(-xm[:, None], yn[None, :]) @ sn
        J[m, :] /= np.sqrt(hh[m])
    J /= np.sqrt(hh[nA:])[None, :]
    D = np.zeros((N, N), dtype=complex)
    D[:nA, nA:] = 1j / (2 * np.pi) * J
    D = D + D.conj().T
    return D

def gQ_sld(Q, D):
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1 - 1e-16)
    w = 1.0 / (q[:, None] * (1 - q)[None, :] + q[None, :] * (1 - q)[:, None])
    dt = U.conj().T @ D @ U
    g = 0.25 * np.sum(w * np.abs(dt) ** 2)
    t = 0.5 * (U @ (w * dt) @ U.conj().T); t = 0.5 * (t + t.conj().T)
    V = np.trace(t @ Q @ t @ (np.eye(len(Q)) - Q)).real
    return float(g), t, float(V), q


# ---------------------------------------------------------------- SDP over F
def _cvx(Q, nA, nB):
    import cvxpy as cp
    N = len(Q); m = N - nA; LB = nB
    QAA = Q[:nA, :nA]; QAB = Q[:nA, nA:nA + nB]; QBB = Q[nA:nA + nB, nA:nA + nB]
    ev = np.linalg.eigvalsh(QBB); sh = max(0.0, 1e-13 - ev.min())
    sG = np.linalg.cholesky(QBB + sh * np.eye(LB))
    ev2 = np.linalg.eigvalsh(np.eye(LB) - QBB); sh2 = max(0.0, 1e-13 - ev2.min())
    sGD = np.linalg.cholesky(np.eye(LB) - QBB + sh2 * np.eye(LB))
    X = cp.Variable((m, LB), complex=True); Z = cp.Variable((m, m), hermitian=True)
    cons = [cp.bmat([[Z, X @ sG], [(X @ sG).H, np.eye(LB)]]) >> 0,
            cp.bmat([[np.eye(m) - Z, X @ sGD], [(X @ sGD).H, np.eye(LB)]]) >> 0]
    M = QAB @ X.H
    Qrec = cp.bmat([[cp.Constant(QAA), M], [M.H, Z]])
    return cp, X, Z, cons, Qrec

def linear_sdp(Q, t, nA, nB, solver='CLARABEL'):
    """Delta(t) = inf_{(X,Z) in F} Tr t (Q - Qrec(X,Z))."""
    cp, X, Z, cons, Qrec = _cvx(Q, nA, nB)
    pr = cp.Problem(cp.Minimize(cp.real(cp.trace(t @ (cp.Constant(Q) - Qrec)))), cons)
    pr.solve(solver=solver)
    return pr.value, X.value, Z.value, pr.status

def primal_sdp(Q, nA, nB, solver='CLARABEL'):
    """min_{(X,Z) in F} g_Q(Q - Qrec(X,Z)) with the TRUE quantum-Fisher weights."""
    cp, X, Z, cons, Qrec = _cvx(Q, nA, nB)
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1 - 1e-16)
    w = 1.0 / (q[:, None] * (1 - q)[None, :] + q[None, :] * (1 - q)[:, None])
    dt = cp.multiply(np.sqrt(w), U.conj().T @ (cp.Constant(Q) - Qrec) @ U)
    obj = 0.25 * (cp.sum_squares(cp.real(dt)) + cp.sum_squares(cp.imag(dt)))
    pr = cp.Problem(cp.Minimize(obj), cons)
    pr.solve(solver=solver)
    return pr.value, X.value, Z.value, pr.status

def build(a, L, s, h, LamA, LamC, kind, hB=None, hC=None):
    edges, nA, nB, nC, xi0, xi1, b = mesh(a, L, s, h, LamA, LamC, hB, hC)
    Q = Qmat(edges); D = defect(edges, nA, a, L, s, kind=kind)
    return edges, nA, nB, nC, Q, D

if __name__ == '__main__':
    a, L = 1.0, 2.0; f2 = 1.0 / (12 * np.pi ** 2)
    job = sys.argv[1] if len(sys.argv) > 1 else 'conv' 
    if job == 'conv':
      print("# convergence of g_Q(delta_c)/(f2 zeta^2) -> 1;  f2 = %.8f" % f2)
      print("# kind    s      h    Lam    N   nA  nB  nC  kappa_max   |D|_1/exact   g_Q/zeta^2   g_Q/(f2 zeta^2)")
      for kind in ['first', 'exact']:
        for s in [0.1]:
            for (h, Lam) in [(0.4,12),(0.3,12),(0.25,12),(0.2,12),(0.15,12),(0.125,12),(0.1,12),(0.25,16),(0.2,8)]:
                edges, nA, nB, nC, Q, D = build(a, L, s, h, Lam, Lam, kind)
                zeta = a * s / (a + L); q = np.linalg.eigvalsh(Q); km = np.log((1 - q[0]) / q[0])
                g, t, V, _ = gQ_sld(Q, D)
                d1 = np.abs(np.linalg.eigvalsh(D)).sum(); d1e = (1/(2*np.pi))*np.log(1 + a*s/(a+L))
                print(f"{kind:6s} {s:6.3f} {h:6.3f} {Lam:5.1f} {len(edges)-1:5d} {nA:4d} {nB:3d} {nC:3d} "
                      f"{km:9.3f}  {d1/d1e:.6f}  {g/zeta**2:.6f}  {g/zeta**2/f2:.5f}", flush=True)
      sys.exit(0)

    # ---------------- job 'sdp': self-consistent KKT test in the discretised continuum
    kind = sys.argv[2] if len(sys.argv) > 2 else 'first'
    h = float(sys.argv[3]); LamA = float(sys.argv[4]); LamC = float(sys.argv[5])
    sv = float(sys.argv[6]) if len(sys.argv) > 6 else 0.1
    edges, nA, nB, nC, Q, D = build(a, L, sv, h, LamA, LamC, kind)
    N = len(Q); zeta = a * sv / (a + L); ref = f2 * zeta ** 2
    g, t, V, q = gQ_sld(Q, D); km = np.log((1 - q[0]) / q[0])
    print(f"# kind={kind} s={sv} h={h} LamA={LamA} LamC={LamC} N={N} nA={nA} nB={nB} nC={nC} "
          f"kappa_max={km:.3f} zeta={zeta:.6f} f2 zeta^2={ref:.6e}", flush=True)
    print(f"# compression defect: g_Q(d_c)={g:.8e}  g_Q/(f2 zeta^2)={g/ref:.6f}  V(t_c)={V:.6e}  "
          f"Tr t_c d_c={np.trace(t@D).real:.6e}  ||t_c||_1={np.abs(np.linalg.eigvalsh(t)).sum():.4e}  "
          f"Legendre={np.trace(t@D).real**2/(8*V)/g:.10f}", flush=True)
    def qrec(X, Z):
        R = np.zeros((N, N), dtype=complex); R[:nA, :nA] = Q[:nA, :nA]
        M = Q[:nA, nA:nA + nB] @ X.conj().T
        R[:nA, nA:] = M; R[nA:, :nA] = M.conj().T; R[nA:, nA:] = Z
        return 0.5 * (R + R.conj().T)
    import time
    t0 = time.time(); Dl, Xl, Zl, stl = linear_sdp(Q, t, nA, nB)
    print(f"# LP at t_c: Delta(t_c)={Dl:.6e}  Delta/(2 g_Q(d_c))={Dl/(2*g):.6f}  "
          f"dual={max(Dl,0)**2/(8*V):.6e}  dual/(f2 zeta^2)={max(Dl,0)**2/(8*V)/ref:.6f}  [{stl}] "
          f"{time.time()-t0:.0f}s", flush=True)
    t0 = time.time(); gp, Xp, Zp, stp = primal_sdp(Q, nA, nB)
    Dp = Q - qrec(Xp, Zp); gp2, tp, Vp, _ = gQ_sld(Q, Dp)
    print(f"# PRIMAL: min_F g_Q = {gp:.8e} (recomputed {gp2:.8e})  min/(f2 zeta^2)={gp/ref:.6f}  "
          f"min/g_Q(d_c)={gp/g:.6f}  [{stp}] {time.time()-t0:.0f}s", flush=True)
    t0 = time.time(); Dlo, Xlo, Zlo, stlo = linear_sdp(Q, tp, nA, nB)
    print(f"# KKT at the primal optimum: Delta(t_opt)={Dlo:.8e}  2 g={2*gp2:.8e}  "
          f"gap={(2*gp2-Dlo)/(2*gp2):+.3e}  dual/min={max(Dlo,0)**2/(8*Vp)/gp2:.8f}  [{stlo}] "
          f"{time.time()-t0:.0f}s", flush=True)
    print(f"# structure: ||d_opt - d_c||_F/||d_c||_F={np.linalg.norm(Dp-D)/np.linalg.norm(D):.4f}  "
          f"||d_opt_DD||_F/||d_c||_F={np.linalg.norm(Dp[nA:,nA:])/np.linalg.norm(D):.4f}  "
          f"||d_c_DD||={np.linalg.norm(D[nA:,nA:]):.2e}  sv(X_opt) in "
          f"[{np.linalg.svd(Xp,compute_uv=False).min():.4f},{np.linalg.svd(Xp,compute_uv=False).max():.4f}]  "
          f"Tr(1-X X^*)={np.trace(np.eye(N-nA)-Xp@Xp.conj().T).real:.4f}", flush=True)
    np.savez(os.path.join(HERE, f'kkt_cont_{kind}_h{h}_A{LamA}_C{LamC}_s{sv}.npz'),
             Q=Q, D=D, t=t, Xp=Xp, Zp=Zp, g=g, gp=gp, V=V, Delta=Dl, Dlo=Dlo, Vp=Vp,
             nA=nA, nB=nB, nC=nC, ref=ref)
