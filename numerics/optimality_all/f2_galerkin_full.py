"""F2/T3: FULL primal SDP over F (all quasi-free channels, finite s, nonlinear) in the
modular Galerkin frame of kkt_continuum.py, next to the isometric-orbit value computed by
theta_galerkin.py's CG in the SAME code path.

a=1, L=2, Lambda=12, s=0.1, kind='first'.  Caveat (S11): in the Galerkin frame the Moebius
compression is NOT representable exactly, and delta_c is the 'first-order kernel'; so
min_F g_Q here need not be <= g_Q(delta_c).
Usage:  f2_galerkin_full.py h1,h2,...
"""
import sys, os, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kkt_continuum import build, gQ_sld, primal_sdp

a, L, f2 = 1.0, 2.0, 1.0/(12*np.pi**2)


def orbit_theta(Q, Dc, nA, N, iters=600):
    """theta_galerkin.py's CG, verbatim conventions."""
    Didx = np.arange(nA, N)
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1-1e-16)
    w = 1.0/(q[:, None]*(1-q)[None, :] + q[None, :]*(1-q)[:, None])
    Wop = lambda Y: U@(w*(U.conj().T@Y@U))@U.conj().T
    ip = lambda X, Y: float(np.real(np.vdot(X, Y)))
    g = lambda Y: 0.25*ip(Y, Wop(Y))
    def emb(G):
        Gf = np.zeros((N, N), complex); Gf[np.ix_(Didx, Didx)] = G; return Gf
    Phi = lambda G: Q@emb(G) - emb(G)@Q
    def PhiT(Y):
        C = Q@Y - Y@Q; R = C[np.ix_(Didx, Didx)]; return 0.5*(R - R.conj().T)
    Aop = lambda G: 0.5*PhiT(Wop(Phi(G)))
    beta = 0.25*PhiT(Wop(Dc)); g0 = g(Dc)
    x = np.zeros_like(beta); r = beta.copy(); p = r.copy(); rs = ip(r, r); nb = np.sqrt(rs)
    for k in range(iters):
        Ap = Aop(p); pAp = ip(p, Ap)
        if pAp <= 1e-300: break
        al = rs/pAp; x = x + al*p; r = r - al*Ap; rs2 = ip(r, r); p = r + (rs2/rs)*p; rs = rs2
        if np.sqrt(rs2) < 1e-14*nb: break
    theta = 2*ip(beta, x)/g0
    eta = Phi(x); bb = 0.25*ip(Wop(Dc), eta); eps = -bb/g(eta)
    return theta, g0, g(Dc + eps*eta), k+1


def run(h, Lam=12.0, s=0.1, kind='first', solver='CLARABEL'):
    t0 = time.time()
    edges, nA, nB, nC, Q, Dc = build(a, L, s, h, Lam, Lam, kind)
    N = len(Q); m = N - nA; zeta = a*s/(a+L); ref = f2*zeta**2
    th, g0, gorb, it = orbit_theta(Q, Dc, nA, N)
    print(f"h={h} N={N} (nA,nB,nC)=({nA},{nB},{nC}) g_Q(d_c)={g0:.8e} = {g0/ref:.4f} f2 z^2 | "
          f"theta={th:.5f} orbit (1-theta)={1-th:.5f} check g_orb/g0={gorb/g0:.5f} (CG {it})", flush=True)
    gp, X, Z, st = primal_sdp(Q, nA, nB, solver=solver)
    QBB = Q[nA:nA+nB, nA:nA+nB]
    XX = X@X.conj().T; Nl = np.eye(m) - XX; Zn = Z - X@QBB@X.conj().T
    eN = np.linalg.eigvalsh(0.5*(Nl+Nl.conj().T)); eZ = np.linalg.eigvalsh(0.5*(Zn+Zn.conj().T))
    print(f"   FULL F : min_F g_Q = {gp:.8e}  min_F/g_Q(d_c) = {gp/g0:.6f}  [orbit 1-theta = {1-th:.6f}]"
          f"  {st}  {time.time()-t0:.0f}s", flush=True)
    print(f"   structure: ||1-XX*||_F={np.linalg.norm(Nl):.4f} tr(1-XX*)={np.trace(Nl).real:.4f} "
          f"eig(1-XX*) in [{eN.min():+.3e},{eN.max():+.3e}] | ||Z-XQ_BBX*||_F={np.linalg.norm(Zn):.4e} "
          f"tr={np.trace(Zn).real:.4e} eig in [{eZ.min():+.3e},{eZ.max():+.3e}] | "
          f"sv(X) in [{np.linalg.svd(X, compute_uv=False).min():.4f},{np.linalg.svd(X, compute_uv=False).max():.4f}]",
          flush=True)
    np.savez(os.path.join(HERE, f'f2_galerkin_h{h}.npz'), h=h, N=N, nA=nA, nB=nB, nC=nC,
             theta=th, g0=g0, gp=gp, X=X, Z=Z, ref=ref)
    return dict(h=h, N=N, theta=th, g0=g0, gp=gp, ratio=gp/g0)


if __name__ == '__main__':
    hs = [float(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '0.4').split(',')]
    res = [run(h) for h in hs]
    print("\n#  h     N   1-theta(orbit)   min_F g_Q / g_Q(d_c)")
    for r in res:
        print(f"{r['h']:.3f} {r['N']:5d}   {1-r['theta']:.6f}      {r['ratio']:.6f}", flush=True)
