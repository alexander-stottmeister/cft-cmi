"""Stage 2: root fidelity and relative entropy of two quasi-free states from the finite formulas,
in high precision (mpmath), on the circle modes.  Input: npz from defect_matrix.py.
  Q  = diag(q_j),  q_j = 1/(1+e^{kappa_j});  Qt = Q - Dhat.
  Fid = prod sqrt(1-q_j) * prod sqrt(1-qt_l) * prod (1+sqrt(tau_m)),  tau = eig(G1^{1/2} G2 G1^{1/2}),
  S(Q||Qt) = sum q_j log q_j + (1-q_j)log(1-q_j) - Tr[Q log Qt] - Tr[(1-Q) log(1-Qt)].
Also the QFI-based second-order coefficient  c2 := (1/4) sum |Dhat_jl|^2 / N_jl  (so -log F ~ c2 at this s).
"""
import numpy as np, mpmath as mp, sys, time
def load(fn):
    z = np.load(fn, allow_pickle=True); return z['Dhat'], z['kappa'], float(z['s']), float(z['a']), float(z['L'])
def fidelity_relent(Dhat, kappa, dps=40):
    mp.mp.dps = dps; N = len(kappa)
    q = [1/(1+mp.e**mp.mpf(k)) for k in kappa]; omq = [1/(1+mp.e**(-mp.mpf(k))) for k in kappa]   # q, 1-q without cancellation
    Qt = mp.matrix(N, N)
    for j in range(N):
        for l in range(N):
            Qt[j,l] = mp.mpc(Dhat[j,l].real, Dhat[j,l].imag)*(-1)
        Qt[j,j] += q[j]
    E, V = mp.eighe(Qt)                                   # Qt = V diag(E) V^H
    qt = [E[l] for l in range(N)]
    assert min(qt) > 0 and max(qt) < 1, (min(qt), max(qt))
    # G2 = V diag(qt/(1-qt)) V^H ; T = G1^{1/2} G2 G1^{1/2}, G1^{1/2} = diag(e^{-kappa/2})
    g1h = [mp.e**(-mp.mpf(k)/2) for k in kappa]
    Wm = mp.matrix(N, N)                                   # Wm = diag(g1h) V diag(sqrt(g2))  => T = Wm Wm^H
    for j in range(N):
        for l in range(N):
            Wm[j,l] = g1h[j]*V[j,l]*mp.sqrt(qt[l]/(1-qt[l]))
    T = Wm*Wm.H
    tau = mp.eighe(T, eigvals_only=True)
    logF = mp.mpf(0)
    for j in range(N): logF += mp.log(omq[j])/2 + mp.log(1-qt[j])/2 + mp.log(1+mp.sqrt(tau[j]))
    # relative entropy
    S = mp.mpf(0)
    for j in range(N):
        S += q[j]*mp.log(q[j]) + omq[j]*mp.log(omq[j])
        for l in range(N):
            w = abs(V[j,l])**2
            S -= w*(q[j]*mp.log(qt[l]) + omq[j]*mp.log(1-qt[l]))
    return -logF, S
def qfi_c2(Dhat, kappa):
    q = 1/(1+np.exp(kappa)); omq = 1/(1+np.exp(-kappa))
    Nw = q[:,None]*omq[None,:] + q[None,:]*omq[:,None]
    return 0.25*np.sum(np.abs(Dhat)**2/Nw)
if __name__ == "__main__":
    fn = sys.argv[1]; dps = int(sys.argv[2]) if len(sys.argv)>2 else 40
    Dhat, kappa, s, a, L = load(fn); zeta = a*s/(a+L); z = zeta/2
    t0 = time.time(); mlogF, S = fidelity_relent(Dhat, kappa, dps); c2 = qfi_c2(Dhat, kappa)
    CMI = mp.log(1+z)/6   # r = 1
    print(f"{fn}: N={len(kappa)} dps={dps} time={time.time()-t0:.0f}s")
    print(f"  zeta={zeta:.6f}  -logF={mp.nstr(mlogF,10)}  S(w||wt)={mp.nstr(S,10)}  c2(QFI at this D)={c2:.6e}")
    print(f"  -logF/zeta^2={mp.nstr(mlogF/zeta**2,8)}  S/zeta^2={mp.nstr(S/zeta**2,8)}  S/(-logF)={mp.nstr(S/mlogF,6)}  (-2logF)/CMI={mp.nstr(2*mlogF/CMI,6)}  CMI/2={mp.nstr(CMI/2,6)}")
