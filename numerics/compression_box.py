"""Genuine compression onto box modes e_j = e^{i k_j xi}/sqrt(Lam) on [xi0-Lam/2, xi0+Lam/2], k_j = 2 pi j/Lam.
Exact compressed vacuum symbol (from the thermal kernel q~(t) = delta/2 - (i/4pi)/sinh(t/2)):
  Q_N[j,j] = 1/2 - (1/(2 pi Lam)) int_0^Lam (Lam - t) sin(k_j t)/sinh(t/2) dt
  Q_N[j,l] = -((-1)^{j-l}/(2 pi Lam (k_j-k_l))) int_0^Lam (cos(k_j t) - cos(k_l t))/sinh(t/2) dt   (j != l)
Then Qt_N = Q_N - Dhat (Dhat from defect_matrix.py, same box) and the finite-dimensional formulas give
rigorous upper bounds F_N >= F and lower bounds S_N <= S.  Double precision suffices (eigenvalues of Q_N
are bounded away from 0 and 1 by the box-edge occupation ~ 1/(pi Lam k)).
"""
import numpy as np, sys, glob
def Q_box(kappa, Lam, nt=400001, xi0=None):
    """Exact compression of the thermal kernel onto box modes; O(N) one-dimensional integrals.
    Off-diagonal uses cos(k_a t)-cos(k_b t) = [cos(k_a t)-1] - [cos(k_b t)-1].
    If xi0 is given, the result is expressed in the ABSOLUTE basis e^{i k_j xi} on the box centred at xi0
    (as used by defect_matrix.py): Q_abs = U Q_cent U^*, U = diag(e^{-i k_j xi0}).  [Fix of the basis
    mismatch found in the verification program (agent V4); relative effect on Phi ~ 5e-5.]"""
    k = kappa/(2*np.pi); N = len(k)
    t = np.linspace(0, Lam, nt); w = np.full(nt, Lam/(nt-1)); w[0]=w[-1]=Lam/(2*(nt-1))
    with np.errstate(divide='ignore', invalid='ignore'):
        inv_sh = np.where(t>0, 1/np.sinh(t/2), 0.0)
    diag = np.array([0.5 - (1/(2*np.pi*Lam))*(np.sum(w[1:]*(Lam-t[1:])*np.sin(kj*t[1:])*inv_sh[1:]) + w[0]*2*Lam*kj) for kj in k])   # t=0 limit = 2 Lam k
    Ct = np.array([np.sum(w*(np.cos(kj*t)-1.0)*inv_sh) for kj in k])          # convergent regularized integrals
    dk = k[:,None]-k[None,:]; sgn = (-1.0)**(np.arange(N)[:,None]-np.arange(N)[None,:])
    with np.errstate(divide='ignore', invalid='ignore'):
        Q = np.where(dk!=0, -sgn/(2*np.pi*Lam*dk)*(Ct[:,None]-Ct[None,:]), 0.0)
    Q[np.arange(N), np.arange(N)] = diag
    if xi0 is not None:
        ph = np.exp(-1j*k*xi0); Q = (ph[:,None]*Q*np.conj(ph)[None,:])
    return Q
def fid_relent(Q, Qt):
    N = len(Q); I = np.eye(N)
    w1, V1 = np.linalg.eigh(Q); w2, V2 = np.linalg.eigh(Qt)
    assert w1.min()>0 and w1.max()<1 and w2.min()>0 and w2.max()<1, (w1.min(), w1.max(), w2.min(), w2.max())
    G1h = V1 @ np.diag(np.sqrt(w1/(1-w1))) @ V1.conj().T
    G2  = V2 @ np.diag(w2/(1-w2)) @ V2.conj().T
    tau = np.linalg.eigvalsh(G1h @ G2 @ G1h)
    logF = 0.5*np.sum(np.log(1-w1)) + 0.5*np.sum(np.log(1-w2)) + np.sum(np.log(1+np.sqrt(np.clip(tau,0,None))))
    lQt = V2 @ np.diag(np.log(w2)) @ V2.conj().T; l1Qt = V2 @ np.diag(np.log(1-w2)) @ V2.conj().T
    lQ  = V1 @ np.diag(np.log(w1)) @ V1.conj().T; l1Q  = V1 @ np.diag(np.log(1-w1)) @ V1.conj().T
    S = np.trace(Q@(lQ-lQt) + (I-Q)@(l1Q-l1Qt)).real
    return -logF, S, (w1.min(), w1.max(), w2.min(), w2.max())
def qfi_c2(Q, D1):
    w, V = np.linalg.eigh(Q); Dm = V.conj().T @ D1 @ V
    Nw = w[:,None]*(1-w)[None,:] + w[None,:]*(1-w)[:,None]
    return 0.25*np.sum(np.abs(Dm)**2/Nw)
if __name__ == "__main__":
    files = sorted(glob.glob(sys.argv[1] if len(sys.argv)>1 else "Dhat_*.npz"))
    cache = {}
    for fn in files:
        z = np.load(fn, allow_pickle=True); Dhat=z['Dhat']; kap=z['kappa']; s=float(z['s']); a=float(z['a']); L=float(z['L']); Lam=float(z['Lam']); kind=str(z['kind'])
        key=(Lam, len(kap))
        if key not in cache: cache[key] = Q_box(kap, Lam, xi0=np.log(a/L))
        Q = cache[key]; zeta = a*s/(a+L)
        if kind == 'first':
            c2 = qfi_c2(Q, Dhat)   # for s=1: -log F ~ c2 * s^2 -> f2 := c2/zeta^2 (zeta at s=1)
            print(f"{fn}: N={len(kap)} Lam={Lam}  QFI:  c2/zeta^2 = f2 = {c2/zeta**2:.8f}   [eig(Q_N) in ({np.linalg.eigvalsh(Q).min():.2e},{np.linalg.eigvalsh(Q).max():.6f})]")
        else:
            mlogF, S, ev = fid_relent(Q, Q - Dhat); CMI = np.log(1+zeta/2)/6
            print(f"{fn}: N={len(kap)} Lam={Lam} zeta={zeta:.5f}  -logF={mlogF:.8e}  S={S:.8e}  -logF/zeta^2={mlogF/zeta**2:.6f}  S/zeta^2={S/zeta**2:.6f}  S/(-logF)={S/mlogF:.4f}  (-2logF)/CMI={2*mlogF/CMI:.5f}  eigQt=({ev[2]:.1e},{1-ev[3]:.1e})")
