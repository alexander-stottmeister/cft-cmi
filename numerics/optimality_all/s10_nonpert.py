import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""S10: non-perturbative check. Build W_s = exp(-s Dchi) (exactly unitary), the exact
defect delta(eps) = E_I(P - Wt^* P Wt)E_I with Wt = W_s exp(-eps G_*), and evaluate the
exact quadratic form g_Q(delta) = (1/4) sum w_ik |delta~_ik|^2 (capped weights).
Compare min_eps g_Q vs g_Q at eps=0 and vs the predicted (1-theta)."""
import numpy as np, sys, scipy.linalg as sla
sys.path.insert(0,_os.path.join(_ROOT, 'numerics/optimality_all'))
from s10_theta import setup

L=512; S=setup(L=L,a=2.0,Lg=1.0)
P=S['P']; D=S['D']; u=S['u']; nu2=S['nu2']
# recompute Dchi and I from setup ingredients
import s10_theta as m
th=2*np.pi*np.arange(L)/L; thw=np.where(th>np.pi,th-2*np.pi,th)
n=np.fft.fftfreq(L,d=1.0/L); nu=n+0.5
F=np.fft.fft(np.eye(L),axis=0)/L; Fi=np.fft.ifft(np.eye(L),axis=0)*L
a1,a2=(0.30,0.42); xx=(np.abs(nu)/L-a1)/(a2-a1); s_=np.clip(1-xx,0,1); s_=s_*s_*(3-2*s_)
d=Fi@np.diag(1j*nu*s_)@F; d=0.5*(d-d.conj().T)
thD=2*np.arctan(1.0); thA=-2*np.arctan(2.0)
inD=(thw>0)&(thw<thD); inA=(thw>thA)&(thw<0); inI=inD|inA
chi=np.zeros(L); chi[inD]=np.cos(thw[inD])-1.0
t=thw.copy(); t[t<thA]+=2*np.pi; mm=~inI
chi[mm]=(np.cos(t[mm])-1.0)*np.exp(-3.0*(t[mm]-thD)**2)
X=np.diag(chi); Dc=0.5*(X@d+d@X); Dc=0.5*(Dc-Dc.conj().T)
I=np.where(inI)[0]
Q=P[np.ix_(I,I)]; Q=0.5*(Q+Q.conj().T)
q,U=np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
den=q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None]
CAP=float(sys.argv[1]) if len(sys.argv)>1 else 1e4; W=np.minimum(1.0/den,CAP)
def gQ(delta):
    dt=U.conj().T@delta@U
    return 0.25*np.sum(W*np.abs(dt)**2)
def defect(Wt):
    Pr=Wt.conj().T@P@Wt
    return (P-Pr)[np.ix_(I,I)]
# optimal G_* from CG
def Aop(g):
    G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g
    v,_=S['riesz'](G); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T)
x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=np.real(np.vdot(r,r))
for k in range(70):
    Ap=Aop(p); pAp=np.real(np.vdot(p,Ap)); al=rs/pAp
    x=x+al*p; r=r-al*Ap; rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
theta=np.real(np.vdot(b,x))/nu2
G=np.zeros((L,L),complex); G[np.ix_(D,D)]=x; G=0.5*(G-G.conj().T)
print(f"theta(CG) = {theta:.5f}   |u|^2={nu2:.6f}")
for s in (0.001,0.002,0.005):
    Ws=sla.expm(-s*Dc)
    g0=gQ(defect(Ws)); pred=0.5*s*s*nu2
    best=(0.0,g0)
    for e in np.linspace(-4.0*s,1.0*s,81):
        ge=gQ(defect(Ws@sla.expm(-e*G)))
        if ge<best[1]: best=(e,ge)
    print(f" s={s:5.3f}  gQ(compression)={g0:.6e} (pred {pred:.6e}, ratio {g0/pred:.4f})"
          f"  min_eps gQ={best[1]:.6e} at eps/s={best[0]/s:+.3f}   ratio={best[1]/g0:.4f}"
          f"   (predicted 1-theta={1-theta:.4f})")
