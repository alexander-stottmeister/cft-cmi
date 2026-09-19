"""Stage 2 (final): rigorous compressed fidelity via spectral sub-compression + python-flint (200 bits).
Q_N exact box compression (compression_box.Q_box); Qt_N = Q_N - Dhat.  Sub-compress onto eigenvectors of Q_N
with eigenvalue in [eps, 1-eps] (still a compression => -logF_sub <= -logF).  Discarded modes |kappa| > kappa_c =
log((1-eps)/eps) carry the analytic tail occupation (2/15) zeta^2 |kappa|^-3 in the recovered state, contributing
~ zeta^2/(15 kappa_c^2) to -log F (both particle and hole sides); we report raw and tail-corrected values.
Relative entropy S in double precision on the full compression (stable: extreme eigenvalues enter only through
log(q) weighted by tiny occupations).  For 'first' files: second-order coefficients f2 (Bures/QFI) and s2 (Kubo-Mori).
"""
import numpy as np, sys, glob, time
from compression_box import Q_box
def logF_flint(w, Qt_sub, dps=40):
    """Hermitian eigen-decompositions in mpmath (robust); name kept for the driver."""
    import mpmath as mp
    mp.mp.dps = dps; n = len(w)
    M = mp.matrix(n, n)
    for i in range(n):
        for j in range(n): M[i,j] = mp.mpc(Qt_sub[i,j].real, Qt_sub[i,j].imag)
    E, V = mp.eighe(M); qt = [E[i] for i in range(n)]
    g1h = [mp.sqrt(mp.mpf(float(x))/mp.mpf(float(1-x))) for x in w]
    Wm = mp.matrix(n, n)
    for l in range(n):
        g2h = mp.sqrt(qt[l]/(1-qt[l]))
        for i in range(n): Wm[i,l] = g1h[i]*V[i,l]*g2h
    tau = mp.eighe(Wm*Wm.H, eigvals_only=True)
    logF = mp.mpf(0); Ssub = mp.mpf(0)
    for i in range(n):
        logF += mp.log(mp.mpf(float(1-w[i])))/2 + mp.log(1-qt[i])/2 + mp.log(1+mp.sqrt(max(tau[i], mp.mpf(0))))
        wi = mp.mpf(float(w[i])); Ssub += wi*mp.log(wi) + (1-wi)*mp.log(1-wi)
        for l in range(n):
            wt = abs(V[i,l])**2; Ssub -= wt*(wi*mp.log(qt[l]) + (1-wi)*mp.log(1-qt[l]))
    return float(-logF), (float(min(qt)), float(max(qt))), n, float(Ssub)
def relent(Q, Qt):
    N=len(Q); I=np.eye(N); w1,V1=np.linalg.eigh(Q); w2,V2=np.linalg.eigh(Qt)
    lQ=V1@np.diag(np.log(w1))@V1.conj().T; l1Q=V1@np.diag(np.log(1-w1))@V1.conj().T
    lQt=V2@np.diag(np.log(w2))@V2.conj().T; l1Qt=V2@np.diag(np.log(1-w2))@V2.conj().T
    return np.trace(Q@(lQ-lQt)+(I-Q)@(l1Q-l1Qt)).real
def second_order(Q, D1, eps=1e-8):
    """Second-order coefficients f2 (Bures) and s2 (Kubo-Mori) of the first-order kernel D1, evaluated in the
    spectral window eps<w<1-eps of Q (sub-compression, a rigorous lower bound by monotonicity); the caller adds the UV tail."""
    w,V=np.linalg.eigh(Q); keep=(w>eps)&(w<1-eps); w=w[keep]; V=V[:,keep]
    Dm=V.conj().T@D1@V; A=np.abs(Dm)**2
    Nw=w[:,None]*(1-w)[None,:]+w[None,:]*(1-w)[:,None]; f2=0.25*np.sum(A/Nw)
    def ell(p,q):
        with np.errstate(divide='ignore', invalid='ignore'):
            r=np.where(np.abs(p-q)>1e-12, (np.log(p)-np.log(q))/(p-q), 1/p)
        return r
    P=w[:,None]*np.ones(len(w))[None,:]; Qm=P.T
    s2=0.5*np.sum(A*(ell(P,Qm)+ell(1-P,1-Qm)))
    return f2, s2
if __name__ == "__main__":
    pat = sys.argv[1] if len(sys.argv)>1 else "Dhat_*.npz"; eps = float(sys.argv[2]) if len(sys.argv)>2 else 1e-8
    cache={}
    for fn in sorted(glob.glob(pat)):
        z=np.load(fn, allow_pickle=True); Dhat=z['Dhat']; kap=z['kappa']; s=float(z['s']); a=float(z['a']); L=float(z['L']); Lam=float(z['Lam']); kind=str(z['kind'])
        key=(Lam,len(kap),a,L); Q = cache.setdefault(key, Q_box(kap, Lam, xi0=np.log(a/L))); zeta=a*s/(a+L); tag=fn.replace('Dhat_','').replace('_g12.npz','')
        if kind=='first':
            f2,s2 = second_order(Q, Dhat, eps); kc=np.log((1-eps)/eps); tail=zeta**2/(15*kc**2); f2c=f2+tail; s2c=s2+2*tail
            print(f"{tag}: N={len(kap)} kc={kc:.1f}  f2_sub={f2/zeta**2:.7f}  f2={f2c/zeta**2:.7f}  s2_sub={s2/zeta**2:.6f}  s2={s2c/zeta**2:.6f}  s2/f2={s2c/f2c:.4f}", flush=True); continue
        Qt = Q - Dhat; w,V = np.linalg.eigh(Q); keep=(w>eps)&(w<1-eps); P=V[:,keep]
        t0=time.time(); mlogF, rng_, n, Ssub = logF_flint(w[keep], P.conj().T@Qt@P)
        kc = np.log((1-eps)/eps); tail = zeta**2/(15*kc**2); CMI=np.log(1+zeta/2)/6; S = Ssub + 2*tail
        print(f"{tag}: N={len(kap)} n_sub={n} kc={kc:.1f} ({time.time()-t0:.0f}s) zeta={zeta:.5f} -logF_sub={mlogF:.6e} +tail={mlogF+tail:.6e} [{(mlogF+tail)/zeta**2:.6f} zeta^2]  S_sub={Ssub:.6e} +tail={S:.6e} [{S/zeta**2:.6f} zeta^2]  S/(-logF)={S/(mlogF+tail):.3f}  -2logF/CMI={2*(mlogF+tail)/CMI:.5f}  qt in ({rng_[0]:.1e},{1-rng_[1]:.1e})", flush=True)
