"""v4 audit: independent recomputation of the defect matrix Dhat, and the xi0-phase consistency test.

Independent quadrature: double-exponential (tanh-sinh) in the variable p = |xi-xi0| after the
substitution p = exp(sigma), sigma in (-inf, log(Lam/2)], with scipy's fixed-order Gauss-Legendre on a
DIFFERENT panel structure (width 0.37 in sigma over the whole range, no split at p=0.2).
"""
import sys, numpy as np
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics")
import defect_matrix as dm

a, L = 1.0, 2.0

def run_v4(a, L, s, Lam, kmax_kappa, kind, ngl=20, width=0.37, pmin=1e-14, xi0_phase=True):
    xi0 = np.log(a/L)
    x_of = lambda xi: (L*np.exp(xi) - a)/(1+np.exp(xi))
    beta = lambda x: (x+a)*(L-x)/(a+L)
    if kind == 'exact':
        kern = lambda u, v: s*u*v/((u+v)*(L*(u+v)+s*u*v))
    else:
        kern = lambda u, v: (s/L)*u*v/(u+v)**2
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    lo, hi = np.log(pmin), np.log(Lam/2)
    ne = int(np.ceil((hi-lo)/width))
    edges = np.linspace(lo, hi, ne+1)
    sig = ((edges[1:]+edges[:-1])/2)[:, None] + ((edges[1:]-edges[:-1])/2)[:, None]*xg[None, :]
    ws = ((edges[1:]-edges[:-1])/2)[:, None]*wg[None, :]
    p = np.exp(sig).ravel(); w = (ws*np.exp(sig)).ravel()
    xA = x_of(xi0 - p); yD = x_of(xi0 + p)
    sa = np.sqrt(beta(xA))*w; sd = np.sqrt(beta(yD))*w
    M = int(np.floor(kmax_kappa/(2*np.pi) * Lam/(2*np.pi)))
    j = np.arange(-M, M+1); k = 2*np.pi*j/Lam
    off = xi0 if xi0_phase else 0.0
    EA = np.exp(-1j*np.outer(k, off - p)); ED = np.exp(1j*np.outer(k, off + p))
    n = len(p); J = np.zeros((len(k), len(k)), dtype=complex); chunk = 1200
    for i0 in range(0, n, chunk):
        u = -xA[i0:i0+chunk][:, None]; v = yD[None, :]
        Rm = kern(u, v)*sa[i0:i0+chunk][:, None]*sd[None, :]
        J += EA[:, i0:i0+chunk] @ (Rm @ ED.T)
    J /= Lam
    Dhat = (1j/(2*np.pi))*J
    return Dhat + Dhat.conj().T, 2*np.pi*k

if __name__ == "__main__":
    s, Lam, kmax = 0.2, 60.0, 30.0
    zeta = a*s/(a+L)
    ref = np.load("/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/"
                  f"Dhat_exact_s{s}_Lam{int(Lam)}_k{int(kmax)}_g12.npz", allow_pickle=True)
    D0 = ref['Dhat']; kap = ref['kappa']
    print(f"== stored file: N={len(kap)} dkappa={kap[1]-kap[0]:.6f} zeta={zeta:.6f}")
    D1, kap1 = dm.run(a, L, s, Lam, kmax, 'exact', ngl=12)
    D2, _ = dm.run(a, L, s, Lam, kmax, 'exact', ngl=16)
    D3, _ = run_v4(a, L, s, Lam, kmax, 'exact', ngl=20, width=0.37)
    D4, _ = run_v4(a, L, s, Lam, kmax, 'exact', ngl=24, width=0.21, pmin=1e-16)
    mx = np.abs(D1).max()
    print(f"reproduce stored .npz with defect_matrix.run(ngl=12): max|diff| = {np.abs(D1-D0).max():.3e}")
    print(f"GL12 vs GL16 (same panels)  : max abs {np.abs(D1-D2).max():.3e}  relative to max|D| = {np.abs(D1-D2).max()/mx:.3e}")
    print(f"GL12 vs v4 (GL20, w=0.37)   : max abs {np.abs(D1-D3).max():.3e}  relative = {np.abs(D1-D3).max()/mx:.3e}")
    print(f"v4(GL20,.37) vs v4(GL24,.21): max abs {np.abs(D3-D4).max():.3e}  relative = {np.abs(D3-D4).max()/mx:.3e}")
    print(f"Hermiticity max|D-D^H| = {np.abs(D1-D1.conj().T).max():.2e}")
    print(f"Tr D = {np.trace(D1).real:+.3e} (exact: 0 by the block-off-diagonal structure)")
    ev = np.linalg.eigvalsh(D1)
    print(f"||D||_1 (box-compressed) = {np.abs(ev).sum():.8e}  continuum (1/2pi)log(1+zeta) = "
          f"{np.log(1+zeta)/(2*np.pi):.8e}  ratio = {np.abs(ev).sum()/(np.log(1+zeta)/(2*np.pi)):.5f}")
    print(f"   spectrum symmetric?  sum(ev) = {ev.sum():+.2e}; max ev {ev.max():.3e}, min ev {ev.min():.3e}")

    print("\n== UV tail of the diagonal:  -D_jj/Delta_kappa  vs  (2/15) zeta^2 kappa^-3")
    dk = kap[1]-kap[0]; d = -np.diag(D1).real/dk
    for kk in [8, 12, 16, 20, 24, 28]:
        i = int(np.argmin(np.abs(kap-kk)))
        pred = (2/15)*zeta**2/kap[i]**3
        print(f"   kappa={kap[i]:6.3f}: density={d[i]:.5e}  pred={pred:.5e}  ratio={d[i]/pred:.4f}"
              f"   q_kappa={1/(1+np.exp(kap[i])):.2e}")

    print("\n== xi0-phase consistency test (basis e_j = e^{i k_j xi}/sqrt(Lam) vs centred e^{i k_j(xi-xi0)})")
    Dnp, _ = run_v4(a, L, s, Lam, kmax, 'exact', ngl=20, width=0.37, xi0_phase=False)
    U = np.exp(-1j*(kap/(2*np.pi))*np.log(a/L))
    print(f"   check D(with xi0) = U D(no xi0) U^*:  max|diff| = "
          f"{np.abs(D3 - (U[:,None]*Dnp*U.conj()[None,:])).max():.3e}  (max|D| = {mx:.3e})")
    np.save("/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/rigor/v4_D_nophase.npy", Dnp)
    np.save("/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/rigor/v4_D_phase.npy", D3)
