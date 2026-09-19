"""High-precision variant: Q_N computed in mpmath (so extreme eigenvalues ~1e-12 are accurate), allowing the
spectral sub-compression down to eps ~ 1e-12 (kappa_c ~ 27.6) and a smaller analytic tail correction.
Usage: python fidelity_hp.py file.npz eps [dps]"""
import numpy as np, mpmath as mp, sys, time
def Q_box_mp(kappa, Lam, dps, xi0=None):
    mp.mp.dps = dps; k = [mp.mpf(float(x))/(2*mp.pi) for x in kappa]; N = len(k); Lm = mp.mpf(Lam)
    pts = [mp.mpf(i) for i in range(0, int(Lam)+1)] + [Lm]
    pts = sorted(set(pts))
    diag = [mp.mpf(1)/2 - mp.quad(lambda t, kj=kj: (Lm-t)*mp.sin(kj*t)/mp.sinh(t/2), pts)/(2*mp.pi*Lm) for kj in k]
    Ct = [mp.quad(lambda t, kj=kj: (mp.cos(kj*t)-1)/mp.sinh(t/2), pts) for kj in k]
    Q = mp.matrix(N, N)
    for i in range(N):
        Q[i,i] = diag[i]
        for j in range(i+1, N):
            Q[i,j] = -((-1)**(i-j))/(2*mp.pi*Lm*(k[i]-k[j]))*(Ct[i]-Ct[j]); Q[j,i] = Q[i,j]
    if xi0 is not None:   # absolute-basis phases e^{-i k_j xi0} (basis of defect_matrix.py); fix from agent V4
        for i in range(N):
            for j in range(N):
                Q[i,j] = Q[i,j]*mp.e**(-1j*(k[i]-k[j])*mp.mpf(xi0))
    return Q
def run(fn, eps, dps=40):
    z = np.load(fn, allow_pickle=True); Dhat=z['Dhat']; kap=z['kappa']; s=float(z['s']); a=float(z['a']); L=float(z['L']); Lam=float(z['Lam'])
    zeta = a*s/(a+L); N = len(kap); t0=time.time()
    Q = Q_box_mp(kap, Lam, dps, xi0=np.log(a/L))
    D = mp.matrix(N, N)
    for i in range(N):
        for j in range(N): D[i,j] = mp.mpc(Dhat[i,j].real, Dhat[i,j].imag)
    Qt = Q - D
    w, V = mp.eighe(Q)                                    # Q = V diag(w) V^H, w real
    keep = [i for i in range(N) if eps < w[i] < 1-eps]; n = len(keep)
    P = mp.matrix(N, n)
    for c, i in enumerate(keep):
        for r in range(N): P[r,c] = V[r,i]
    Qs = P.H*Qt*P                                        # sub-compressed recovered symbol (Hermitian)
    ws = [w[i] for i in keep]
    E, U = mp.eighe(Qs); qt = [E[i] for i in range(n)]
    assert min(qt) > 0 and max(qt) < 1, (float(min(qt)), float(max(qt)))
    Wm = mp.matrix(n, n)
    for l in range(n):
        g2h = mp.sqrt(qt[l]/(1-qt[l]))
        for i in range(n): Wm[i,l] = mp.sqrt(ws[i]/(1-ws[i]))*U[i,l]*g2h
    tau = mp.eighe(Wm*Wm.H, eigvals_only=True)
    logF = mp.mpf(0)
    for i in range(n): logF += mp.log(1-ws[i])/2 + mp.log(1-qt[i])/2 + mp.log(1+mp.sqrt(max(tau[i], mp.mpf(0))))
    Ssub = mp.mpf(0)
    for i in range(n):
        Ssub += ws[i]*mp.log(ws[i]) + (1-ws[i])*mp.log(1-ws[i])
        for l in range(n):
            wt = abs(U[i,l])**2; Ssub -= wt*(ws[i]*mp.log(qt[l]) + (1-ws[i])*mp.log(1-qt[l]))
    Ssub = float(Ssub)
    mlogF = float(-logF); kc = np.log((1-eps)/eps); tail = zeta**2/(15*kc**2)
    print(f"{fn}: N={N} n_sub={n} kc={kc:.1f} dps={dps} ({time.time()-t0:.0f}s) zeta={zeta:.5f} -logF_sub={mlogF:.6e} +tail={mlogF+tail:.6e} [{(mlogF+tail)/zeta**2:.6f} zeta^2]  S_sub={Ssub:.6e} +tail={Ssub+2*tail:.6e} [{(Ssub+2*tail)/zeta**2:.6f} zeta^2]  qt in ({float(min(qt)):.1e},{1-float(max(qt)):.1e})", flush=True)
if __name__ == "__main__":
    run(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv)>3 else 40)
