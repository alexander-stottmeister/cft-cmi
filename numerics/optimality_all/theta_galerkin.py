"""Orchestrator cross-check of S10's theta in S11's block-exact modular Galerkin model (kkt_continuum.py):
first-order defect on the isometric orbit  delta(eps) = delta_c + eps*[Q, G]  (G anti-Hermitian on V_D; E_I[P,G]E_I=[Q,G]
because G is supported in D subset I), SLD form g_Q on I with TRUE weights (no cap needed: kappa_max ~ 5-7).
theta = sup_G  b(delta_c,eta_G)^2 / (g(delta_c) g(eta_G)) = 2 <beta, A^{-1} beta> / g(delta_c),  via CG."""
import sys, numpy as np
sys.path.insert(0, '.')
from kkt_continuum import build
a, L = 1.0, 2.0; f2 = 1.0/(12*np.pi**2)
def run(h, Lam, s, kind, iters=400):
    edges, nA, nB, nC, Q, Dc = build(a, L, s, h, Lam, Lam, kind)
    N = len(Q); m = nB + nC; Didx = np.arange(nA, N); zeta = a*s/(a+L)
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1-1e-16)
    w = 1.0/(q[:, None]*(1-q)[None, :] + q[None, :]*(1-q)[:, None])
    Wop = lambda Y: U @ (w * (U.conj().T @ Y @ U)) @ U.conj().T
    ip = lambda X, Y: np.real(np.vdot(X, Y))
    g = lambda Y: 0.25*ip(Y, Wop(Y))
    def emb(G): Gf = np.zeros((N, N), complex); Gf[np.ix_(Didx, Didx)] = G; return Gf
    Phi = lambda G: Q @ emb(G) - emb(G) @ Q
    def PhiT(Y): C = Q @ Y - Y @ Q; R = C[np.ix_(Didx, Didx)]; return 0.5*(R - R.conj().T)
    Aop = lambda G: 0.5*PhiT(Wop(Phi(G)))          # f(G)=g(Phi G)= 1/2 <G, A G>
    beta = 0.25*PhiT(Wop(Dc))                       # lin(G)=b(delta_c,Phi G)=<beta,G>
    g0 = g(Dc)
    # CG
    x = np.zeros_like(beta); r = beta.copy(); p = r.copy(); rs = ip(r, r); hist = []
    for k in range(iters):
        Ap = Aop(p); pAp = ip(p, Ap)
        if pAp <= 1e-300: break
        al = rs/pAp; x = x + al*p; r = r - al*Ap; rs2 = ip(r, r); p = r + (rs2/rs)*p; rs = rs2
        if (k+1) % 50 == 0: hist.append((k+1, 2*ip(beta, x)/g0))
        if np.sqrt(rs2) < 1e-14*np.linalg.norm(beta): break
    theta = 2*ip(beta, x)/g0
    # direct verification with the optimal G: min over eps of g(delta_c + eps Phi(x))
    eta = Phi(x); bb = 0.25*ip(Wop(Dc), eta); ge = g(eta); eps = -bb/ge
    gmin = g(Dc + eps*eta); crude = 2*ip(beta, beta)/ip(beta, Aop(beta))/g0
    # DD block of delta_c (Moebius rigidity check)
    dd = np.linalg.norm(Dc[np.ix_(Didx, Didx)])/np.linalg.norm(Dc)
    print(f"{kind:5s} h={h:.3f} Lam={Lam} s={s} N={N} (nA,nB,nC)=({nA},{nB},{nC}) kappa_max={np.log((1-q[0])/q[0]):.2f} "
          f"g(dc)/(f2 zeta^2)={g0/(f2*zeta**2):.4f} |dc_DD|/|dc|={dd:.1e} | theta(CG)={theta:.4f} crude={crude:.4f} "
          f"check min_eps g/g0={gmin/g0:.4f} (1-theta={1-theta:.4f}) eps*={eps:.3f} iters={k+1}", flush=True)
    return theta
if __name__ == '__main__':
    kind = sys.argv[1] if len(sys.argv) > 1 else 'first'
    for (h, Lam, s) in [(0.4, 12, 0.1), (0.3, 12, 0.1), (0.25, 12, 0.1), (0.2, 12, 0.1), (0.15, 12, 0.1), (0.2, 12, 0.02), (0.2, 12, 0.5)]:
        run(h, Lam, s, kind)
