"""Stage 1 of the fidelity computation: defect matrix in the modular-mode basis.
Modular coordinate xi = log((x+a)/(L-x)); in half-density form the vacuum symbol is the
translation-invariant kernel q~(t) = delta(t)/2 - (i/4pi)/sinh(t/2), t = xi - xi', with Fourier
symbol q(k) = 1/(1+e^{2 pi k}), kappa = 2 pi k.  We put the xi-line on a circle of length Lam
(modes e_j = e^{i k_j xi}/sqrt(Lam), k_j = 2 pi j/Lam) and compute
   Dhat[j,l] = <e_j, D e_l> = (1/Lam) int int e^{-i k_j xi} Dt(xi,xi') e^{i k_l xi'} dxi dxi',
   Dt(xi,xi') = sqrt(beta beta') * D(x,y),  D = (i/2pi) R_s(-x,y) on A x D and adjoint on D x A.
Kernel 'exact' or 'first' (O(s) part).  Output: .npz with Dhat, kgrid, params.
Graded mesh in p=|xi-xi0| near the corner, uniform beyond; trapezoid weights.
"""
import numpy as np, sys, time
def run(a, L, s, Lam, kmax_kappa, kind, ngl=12, out=None):
    xi0 = np.log(a/L)
    def x_of(xi): e = np.exp(xi); return (L*e - a)/(1+e)
    def beta(x): return (x+a)*(L-x)/(a+L)
    def kern(u, v):
        if kind == 'exact': return s*u*v/((u+v)*(L*(u+v)+s*u*v))
        return (s/L)*u*v/(u+v)**2
    # Gauss-Legendre product mesh in p = |xi - xi0|:
    #   corner region p in [1e-12, 0.2]: GL panels in sigma = log p (kernel is a smooth sech^2 of log-ratios there),
    #   outer region p in [0.2, Lam/2]: GL panels in p of width 0.25.
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    def panels(lo, hi, width):
        edges = np.linspace(lo, hi, int(np.ceil((hi-lo)/width))+1)
        nodes = ((edges[1:]+edges[:-1])/2)[:,None] + ((edges[1:]-edges[:-1])/2)[:,None]*xg[None,:]
        wts = ((edges[1:]-edges[:-1])/2)[:,None]*wg[None,:]
        return nodes.ravel(), wts.ravel()
    sig, wsig = panels(np.log(1e-12), np.log(0.2), 0.5)
    p1, w1 = np.exp(sig), wsig*np.exp(sig)                     # dp = p dsigma
    p2, w2 = panels(0.2, Lam/2, 0.25)
    p = np.concatenate((p1, p2)); w = np.concatenate((w1, w2))
    xA = x_of(xi0 - p); yD = x_of(xi0 + p)                 # A side xi=xi0-p, D side xi'=xi0+p
    sa = np.sqrt(beta(xA))*w; sd = np.sqrt(beta(yD))*w
    M = int(np.floor(kmax_kappa/(2*np.pi) * Lam/(2*np.pi)))  # k_j = 2 pi j/Lam, kappa_max = 2 pi k_max
    j = np.arange(-M, M+1); k = 2*np.pi*j/Lam
    # phases: e^{-i k xi} on A side (xi = xi0 - p) and e^{+i k xi'} on D side (xi' = xi0 + p)
    EA = np.exp(-1j*np.outer(k, xi0 - p))     # (N, n)
    ED = np.exp( 1j*np.outer(k, xi0 + p))     # (N, n)
    # J[j,l] = sum_{p,p'} EA[j,p] sa[p] R(u,v) sd[p'] ED[l,p']   (block A x D of (2pi/i) * D)
    n = len(p); J = np.zeros((len(k), len(k)), dtype=complex); chunk = 1200
    for i0 in range(0, n, chunk):
        u = -xA[i0:i0+chunk][:, None]; v = yD[None, :]
        Rm = kern(u, v) * sa[i0:i0+chunk][:, None] * sd[None, :]     # (c, n)
        G = Rm @ ED.T                                                   # (c, N)
        J += EA[:, i0:i0+chunk] @ G                                     # (N, N)
    J /= Lam
    # D = (i/2pi)[block A x D] + adjoint: Dhat = (i/2pi) J + ((i/2pi) J)^dagger
    Dhat = (1j/(2*np.pi))*J; Dhat = Dhat + Dhat.conj().T
    kap = 2*np.pi*k
    if out: np.savez(out, Dhat=Dhat, kappa=kap, a=a, L=L, s=s, Lam=Lam, kind=kind, ngl=ngl)
    return Dhat, kap
if __name__ == "__main__":
    a, L = 1.0, 2.0
    s = float(sys.argv[1]); Lam = float(sys.argv[2]); kmax = float(sys.argv[3]); kind = sys.argv[4]
    t0 = time.time()
    ngl = int(sys.argv[5]) if len(sys.argv)>5 else 12
    Dhat, kap = run(a, L, s, Lam, kmax, kind, ngl=ngl, out=f"Dhat_{kind}_s{s}_Lam{int(Lam)}_k{int(kmax)}_g{ngl}.npz")
    q = 1/(1+np.exp(kap))
    print(f"kind={kind} s={s} Lam={Lam} kappa_max={kmax}: N={len(kap)} modes, dkappa={kap[1]-kap[0]:.3f}, time {time.time()-t0:.1f}s")
    print(f"  ||Dhat||_1 (trace norm, discretized) = {np.abs(np.linalg.eigvalsh(Dhat)).sum():.6e}   exact continuum: {(1/(2*np.pi))*np.log(1+a*s/(a+L)):.6e}")
    print(f"  Tr Dhat = {np.trace(Dhat).real:.2e} (should be 0);  max |Dhat| = {np.abs(Dhat).max():.3e}")
    d = np.diag(Dhat).real
    for kk in [5,10,15,20,25]:
        i = np.argmin(np.abs(kap-kk)); print(f"  kappa={kap[i]:6.2f}: -Dhat_diag/dkappa = {-d[i]/(kap[1]-kap[0]): .4e}  q={q[i]:.2e}")
