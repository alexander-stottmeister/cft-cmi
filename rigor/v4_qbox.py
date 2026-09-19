import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
"""v4 audit: independent verification of the compressed vacuum symbol Q_box (compression_box.Q_box).

Independent route (Fourier / Plancherel), completely different from the code's t-integrals:
  Q_N[j,l] = <e_j, Q e_l> = (1/2pi) int dk qhat(k) conj(ehat_j(k)) ehat_l(k),
  e_j(xi)   = Lam^{-1/2} e^{i k_j xi} 1_[xi0-Lam/2, xi0+Lam/2],
  ehat_j(k) = int e^{-i k xi} e_j(xi) dxi = Lam^{-1/2} e^{i(k_j-k) xi0} 2 sin((k_j-k)Lam/2)/(k_j-k),
  qhat(k)   = 1/(1+e^{2 pi k}).
The xi0 phase is kept explicitly so the basis convention can be tested.
Quadrature in k: Gauss-Legendre panels of width (2pi/Lam)/2 (half an oscillation) over [-K,K]
plus an explicit asymptotic tail |k|>K.
"""
import sys, numpy as np
sys.path.insert(0, _os.path.join(_ROOT, "numerics"))
from compression_box import Q_box


def Qbox_fourier(kvals, Lam, xi0, K=60.0, ngl=24, panels_per_period=4):
    """Full matrix by the Plancherel route.  kvals = k_j (not kappa)."""
    per = 2*np.pi/Lam
    w_panel = per/panels_per_period
    ne = int(np.ceil(2*K/w_panel))
    edges = np.linspace(-K, K, ne+1)
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    kk = (((edges[1:]+edges[:-1])/2)[:, None] + ((edges[1:]-edges[:-1])/2)[:, None]*xg[None, :]).ravel()
    wk = (((edges[1:]-edges[:-1])/2)[:, None]*np.ones(ngl)[None, :]*wg[None, :]).ravel()
    qh = 1.0/(1.0+np.exp(np.clip(2*np.pi*kk, -700, 700)))
    d = kvals[:, None] - kk[None, :]                       # (N, nk)
    with np.errstate(divide='ignore', invalid='ignore'):
        sh = np.where(np.abs(d) > 1e-13, np.sin(d*Lam/2)/np.where(d == 0, 1, d), Lam/2)
    ph = np.exp(1j*np.outer(kvals, np.full(len(kk), 0.0)))  # placeholder, phases applied below
    # conj(ehat_j) ehat_l = (1/Lam) e^{-i(k_j-k)xi0} 2 sh_j * e^{i(k_l-k)xi0} 2 sh_l
    #                     = (4/Lam) sh_j sh_l e^{-i(k_j-k_l)xi0}
    A = sh*np.sqrt(np.abs(wk*qh))[None, :]*np.sign(1.0)
    # do it explicitly to keep the weights real-positive
    W = wk*qh
    M = (sh*W[None, :]) @ sh.T                              # real symmetric, (N,N)
    M = (4.0/Lam)*M/(2*np.pi)
    phase = np.exp(-1j*np.outer(kvals, np.ones(len(kvals)))*xi0
                   + 1j*np.outer(np.ones(len(kvals)), kvals)*xi0)
    return M*phase, M


if __name__ == "__main__":
    a, L, Lam = 1.0, 2.0, 60.0
    xi0 = float(np.log(a/L))
    kappa = np.load(_os.path.join(_ROOT, "numerics",
                    "Dhat_exact_s0.2_Lam60_k30_g12.npz"), allow_pickle=True)['kappa']
    N = len(kappa); mid = N//2; kv = kappa/(2*np.pi)
    Q = Q_box(kappa, Lam)
    print(f"N={N} Lam={Lam} xi0={xi0:.6f} Delta_kappa={kappa[1]-kappa[0]:.6f}", flush=True)

    Qf_ph, Qf_0 = Qbox_fourier(kv, Lam, xi0, K=60.0, ngl=24, panels_per_period=4)
    Qf_ph2, Qf_02 = Qbox_fourier(kv, Lam, xi0, K=90.0, ngl=32, panels_per_period=6)
    print(f"(0) Fourier route self-convergence: max|Q_f(K=60,g24,p4) - Q_f(K=90,g32,p6)| = "
          f"{np.abs(Qf_0-Qf_02).max():.3e}", flush=True)

    print("\n(a) code Q_box  vs  Fourier route WITHOUT the xi0 phase (centred basis e^{i k_j(xi-xi0)}):")
    print(f"    max|Q_code - Q_fourier(xi0=0)| = {np.abs(Q-Qf_02).max():.3e}   "
          f"(max|Q| = {np.abs(Q).max():.3e})")
    for (j, l) in [(mid, mid), (mid+5, mid+5), (mid+30, mid+30), (mid, mid+1), (mid+3, mid+7), (mid-20, mid+20)]:
        print(f"      ({j-mid:+4d},{l-mid:+4d}): code={Q[j,l]:+.14e}  fourier={Qf_02[j,l]:+.14e}  "
              f"diff={Q[j,l]-Qf_02[j,l]:+.2e}")

    print("\n(b) code Q_box  vs  Fourier route WITH the true xi0 = log(a/L) phase"
          " (the basis e_j = e^{i k_j xi}/sqrt(Lam) written in the note):")
    print(f"    max|Q_code - Q_fourier(xi0)| = {np.abs(Q-Qf_ph2).max():.3e}")
    for (j, l) in [(mid, mid+1), (mid+3, mid+7)]:
        print(f"      ({j-mid:+4d},{l-mid:+4d}): code={Q[j,l]:+.6e}   fourier={Qf_ph2[j,l]:+.6e}")

    print("\n(c) diagonal vs Lam->infty limit qhat and the claimed box-edge occupation 1/(pi Lam k_j):")
    for j in [mid, mid+5, mid+10, mid+20, mid+30, mid+45]:
        q = 1/(1+np.exp(kappa[j])); kj = kv[j]
        edge = 1/(np.pi*Lam*kj) if kj != 0 else np.inf
        print(f"    kappa={kappa[j]:7.3f}: Q_jj={Q[j,j]:.6e}  qhat={q:.3e}  Q_jj-qhat={Q[j,j]-q:+.3e}"
              f"  1/(pi Lam k_j)={edge:.3e}  ratio={(Q[j,j]-q)/edge if kj!=0 else float('nan'):.3f}")

    print("\n(d) trapezoid accuracy of Q_box (nt=400001 default):")
    for nt in [100001, 400001, 1600001]:
        Qn = Q_box(kappa, Lam, nt=nt)
        w = np.linalg.eigvalsh(Qn)
        print(f"    nt={nt:8d}: max|Q-Q(4e5)| = {np.abs(Qn-Q).max():.3e}   min eig = {w.min():.6e}"
              f"   1-max eig = {1-w.max():.6e}")
    print(f"    Q_box is real symmetric: max|Q-Q^T| = {np.abs(Q-Q.T).max():.2e}")

    print("\n(e) diagonal t->0 endpoint term: value of dropping it")
    def Q_diag_no_endpoint(kappa, Lam, nt=400001):
        k = kappa/(2*np.pi)
        t = np.linspace(0, Lam, nt); w = np.full(nt, Lam/(nt-1)); w[0] = w[-1] = Lam/(2*(nt-1))
        inv_sh = np.where(t > 0, 1/np.sinh(np.where(t > 0, t/2, 1)), 0.0)
        return np.array([0.5 - (1/(2*np.pi*Lam))*np.sum(w[1:]*(Lam-t[1:])*np.sin(kj*t[1:])*inv_sh[1:]) for kj in k])
    dnoend = Q_diag_no_endpoint(kappa, Lam)
    print(f"    max |diag(with endpoint) - diag(without)| = {np.abs(np.diag(Q)-dnoend).max():.3e}")
    print(f"    endpoint term w[0]*2*Lam*k_max/(2 pi Lam) = {(Lam/(2*(400001-1)))*2*Lam*kv[-1]/(2*np.pi*Lam):.3e}")
