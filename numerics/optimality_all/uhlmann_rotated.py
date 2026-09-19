"""Uhlmann upper bound for the compression and for S10's rotated channel in the spectral model:
recovered state = vector state of Gamma(Wt)^* Omega on A(I), so  F >= |<Omega, Gamma(Wt) Omega>| = det(1 - V^*V)^{1/2},
V = P^perp Wt P  (uhlmann_upper_bound.tex).  UB := -1/2 log det(1 - V^*V) = 1/2 ||V||_2^2 + ...  Double precision suffices
(Hilbert-Schmidt quantities).  Compare UB_c, UB_rot(eps*), their ratio, and UB_c / (1/2 s^2 |u|^2)."""
import sys, numpy as np, scipy.linalg as sla
sys.path.insert(0,'.')
from s10_theta import setup
def model(L):
    S=setup(L=L,a=2.0,Lg=1.0); P=S['P']; D=S['D']; u=S['u']; nu2=S['nu2']
    th=2*np.pi*np.arange(L)/L; thw=np.where(th>np.pi,th-2*np.pi,th); n=np.fft.fftfreq(L,d=1.0/L); nu=n+0.5
    F=np.fft.fft(np.eye(L),axis=0)/L; Fi=np.fft.ifft(np.eye(L),axis=0)*L
    a1,a2=(0.30,0.42); xx=(np.abs(nu)/L-a1)/(a2-a1); s_=np.clip(1-xx,0,1); s_=s_*s_*(3-2*s_)
    d=Fi@np.diag(1j*nu*s_)@F; d=0.5*(d-d.conj().T)
    thD=2*np.arctan(1.0); thA=-2*np.arctan(2.0); inD=(thw>0)&(thw<thD); inA=(thw>thA)&(thw<0); inI=inD|inA
    chi=np.zeros(L); chi[inD]=np.cos(thw[inD])-1.0; t=thw.copy(); t[t<thA]+=2*np.pi; mm=~inI
    chi[mm]=(np.cos(t[mm])-1.0)*np.exp(-3.0*(t[mm]-thD)**2)
    X=np.diag(chi); Dc=0.5*(X@d+d@X); Dc=0.5*(Dc-Dc.conj().T)
    def Aop(g):
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g; v,_=S['riesz'](G); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T); x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=np.real(np.vdot(r,r))
    for k in range(70):
        Ap=Aop(p); pAp=np.real(np.vdot(p,Ap)); al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
    theta=np.real(np.vdot(b,x))/nu2; G=np.zeros((L,L),complex); G[np.ix_(D,D)]=x; G=0.5*(G-G.conj().T)
    v,_=S['riesz'](G); eps_star=-np.real(np.vdot(u,v))/np.real(np.vdot(v,v))
    return P,Dc,G,theta,eps_star,nu2
def UB(P,Wt):
    Pp=np.eye(len(P))-P; V=Pp@Wt@P; sv=np.linalg.svd(V,compute_uv=False); sv=np.clip(sv,0,1-1e-16)
    return -0.5*np.sum(np.log1p(-sv**2)), 0.5*np.sum(sv**2)
for L in [96,160,256,384]:
    P,Dc,G,theta,es,nu2=model(L)
    for s in [0.005,0.002,0.001]:
        Ws=sla.expm(-s*Dc); ubc,hsc=UB(P,Ws); scale=0.5*s*s*nu2
        best=None
        for e in np.linspace(-2.5,0.5,61):
            ub,_=UB(P,Ws@sla.expm(-e*s*G))
            if best is None or ub<best[1]: best=(e,ub)
        ubr,_=UB(P,Ws@sla.expm(-es*s*G))
        print(f"L={L:3d} s={s:.3f} theta={theta:.4f} | UB_c={ubc:.4e} UB_c/(s^2|u|^2/2)={ubc/scale:.3f} | UB_rot(eps*)/UB_c={ubr/ubc:.4f} | best eps/s={best[0]:+.2f} UB_rot/UB_c={best[1]/ubc:.4f} | 1-theta={1-theta:.4f}",flush=True)
