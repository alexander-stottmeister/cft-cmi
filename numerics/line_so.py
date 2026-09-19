import numpy as np, sys, glob
def ell(p,q):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.abs(p-q)>1e-14*np.maximum(p,q), (np.log(p)-np.log(q))/(p-q), 1/p)
for fn in sys.argv[1:]:
    z=np.load(fn,allow_pickle=True); D=z['Dhat']; kap=z['kappa']; a=float(z['a']); L=float(z['L']); s=float(z['s']); zeta=a*s/(a+L)
    q=1/(1+np.exp(kap)); omq=1/(1+np.exp(-kap)); A=np.abs(D)**2
    Nw=q[:,None]*omq[None,:]+q[None,:]*omq[:,None]; f2=0.25*np.sum(A/Nw)/zeta**2
    P=q[:,None]*np.ones(len(q))[None,:]; Pm=omq[:,None]*np.ones(len(q))[None,:]
    s2=0.5*np.sum(A*(ell(P,P.T)+ell(Pm,Pm.T)))/zeta**2
    print(f"{fn}: kmax={kap.max():.2f} N={len(kap)} f2_line={f2:.7f} s2_line={s2:.6f} s2/f2={s2/f2:.4f}")
