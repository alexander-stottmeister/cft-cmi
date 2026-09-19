import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""F3 T1/T3: the h-dependence of theta is an ENDPOINT effect (phi(Delta) jumps at Delta=0).
Resolve it cheaply: uniform mesh of width h, but the LAST cell (at xi_max, i.e. x -> L, the
common endpoint of D and I) is subdivided geometrically, K levels with ratio r.  Smallest cell
h*r^K.  Optionally the same at the left end of the window (x -> -a, inside A, no G there)."""
import sys, time, numpy as np
sys.path.insert(0,_os.path.join(_ROOT, 'numerics/optimality_all'))
from kkt_continuum import Qmat, defect
import f3_gal as G
f2 = 1.0/(12*np.pi**2)

def mesh_ep(a, L, s, h, Lam, K=0, r=0.5, Kl=0):
    b = L/(1.0+s); xi0=np.log(a/L); xi1=np.log((a+b)/(L-b))
    nA = max(1,int(round(Lam/h))); nR = max(1,int(round((xi1-xi0+Lam)/h)))
    e = xi0 + h*np.arange(-nA, nR+1)
    if K>0:                      # refine the last cell towards e[-1]
        lo, hi = e[-2], e[-1]
        add = hi - (hi-lo)*r**np.arange(1,K+1)
        e = np.concatenate([e[:-1], add, [hi]])
    if Kl>0:                     # refine the first cell towards e[0]
        lo, hi = e[0], e[1]; nA += Kl
        add = lo + (hi-lo)*r**np.arange(K if False else Kl,0,-1)
        e = np.concatenate([[lo], add, e[1:]])
    return e, nA

def run(a=1.0, L=2.0, s=0.1, h=0.12, Lam=8, K=0, r=0.5, Kl=0, kind='first', ng=10):
    t0=time.time(); e, nA = mesh_ep(a,L,s,h,Lam,K,r,Kl)
    Q = Qmat(e); Dc = defect(e, nA, a, L, s, kind=kind, ng=ng)
    zeta=a*s/(a+L); q=np.linalg.eigvalsh(Q)
    th,g0,k,_,x = G.theta(Q,Dc,nA,iters=8000)
    hmin = np.diff(e).min()
    print(f"h={h} Lam={Lam} K={K} r={r} Kl={Kl} N={len(Q)} hmin={hmin:.2e} "
          f"kmax={np.log((1-q[0])/max(q[0],1e-300)):.2f} gQ/(f2z^2)={g0/(f2*zeta**2):.5f} "
          f"theta={th:.5f} cg={k} {time.time()-t0:.0f}s", flush=True)
    return th

if __name__=='__main__':
    job=sys.argv[1] if len(sys.argv)>1 else 'K'
    if job=='K':
        for h in (0.12,0.06):
            for K in (0,2,4,6,8,10,12): run(h=h,K=K)
    elif job=='Kl':
        for K in (0,6,10): run(h=0.12,K=K,Kl=K)
    elif job=='r':
        for r in (0.3,0.5,0.7): run(h=0.12,K=8,r=r)
    elif job=='fine':
        for h in (0.24,0.12,0.06,0.03): run(h=h,K=10)
