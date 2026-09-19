import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
import numpy as np, sys
sys.path.insert(0,_os.path.join(_ROOT, 'numerics/optimality_all'))
from s10_theta import setup

def diag(L=512,a=2.0,Lg=1.0,uv=(0.30,0.42),alpha=3.0,cap=1e10,iters=70):
    S=setup(L=L,a=a,Lg=Lg,alpha=alpha,cap=cap,uv=uv)
    D=S['D']; u=S['u']; nu2=S['nu2']
    def A(g):
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g
        v,_=S['riesz'](G); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T)
    x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=np.real(np.vdot(r,r))
    for k in range(iters):
        Ap=A(p); pAp=np.real(np.vdot(p,Ap))
        if pAp<=1e-30: break
        al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
    th=np.real(np.vdot(b,x))/nu2
    G=np.zeros((L,L),complex); G[np.ix_(D,D)]=x
    v,_=S['riesz'](G); nv2=np.real(np.vdot(v,v)); ip=np.real(np.vdot(u,v))
    eps=-ip/nv2; Gs=eps*x
    print(f" L={L} a={a} uv={uv} cap={cap:.0e}: theta={th:.5f} |u|^2={nu2:.6f} "
          f"|eps G|_op/s={np.linalg.norm(Gs,2):.3f} |eps G|_2/s={np.linalg.norm(Gs):.3f}", flush=True)
    return th
if __name__=="__main__":
    for uv in [(0.20,0.32),(0.30,0.42),(0.38,0.48)]: diag(uv=uv)
    for cap in (1e6,1e12): diag(cap=cap)
    for L in (640,): diag(L=L)
