import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""F3 smoke: reproduce one published number in each frame, and check CG convergence."""
import sys, time, numpy as np
HERE=_os.path.join(_ROOT, 'numerics/optimality_all')
sys.path.insert(0,HERE)
from kkt_continuum import build
from s10_theta import setup

def cg(Aop, b, ip, g0, iters, tag, ladder=(25,50,100,200,400,800,1600,3200,6400)):
    x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=ip(r,r); out=[]
    for k in range(iters):
        Ap=Aop(p); pAp=ip(p,Ap)
        if pAp<=1e-300: break
        al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=ip(r,r); p=r+(rs2/rs)*p; rs=rs2
        if (k+1) in ladder: out.append((k+1, 2*ip(b,x)/g0 if g0 else ip(b,x)))
        if np.sqrt(rs2)<1e-15*np.linalg.norm(b): break
    print(f"  {tag} ladder:", " ".join(f"{k}:{v:.5f}" for k,v in out), f"[stopped k={k+1}]", flush=True)
    return x, (2*ip(b,x)/g0 if g0 else ip(b,x))

# ---------- Galerkin, h=0.3, Lam=12, s=0.1, first  (published theta=0.299)
def gal(h=0.3, Lam=12, s=0.1, kind='first', a=1.0, L=2.0, iters=3000):
    t0=time.time(); edges,nA,nB,nC,Q,Dc = build(a,L,s,h,Lam,Lam,kind)
    N=len(Q); Didx=np.arange(nA,N); f2=1.0/(12*np.pi**2); zeta=a*s/(a+L)
    q,U=np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
    w=1.0/(q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None])
    Wop=lambda Y: U@(w*(U.conj().T@Y@U))@U.conj().T
    ip=lambda X,Y: np.real(np.vdot(X,Y)); g=lambda Y: 0.25*ip(Y,Wop(Y))
    def emb(G): Gf=np.zeros((N,N),complex); Gf[np.ix_(Didx,Didx)]=G; return Gf
    Phi=lambda G: Q@emb(G)-emb(G)@Q
    def PhiT(Y):
        C=Q@Y-Y@Q; R=C[np.ix_(Didx,Didx)]; return 0.5*(R-R.conj().T)
    Aop=lambda G: 0.5*PhiT(Wop(Phi(G)))
    beta=0.25*PhiT(Wop(Dc)); g0=g(Dc)
    print(f"GAL h={h} Lam={Lam} N={N} (nA,nB,nC)=({nA},{nB},{nC}) g/(f2 z^2)={g0/(f2*zeta**2):.4f}",flush=True)
    x,th=cg(Aop,beta,ip,g0,iters,"gal")
    print(f"  -> theta={th:.5f}  ({time.time()-t0:.0f}s)",flush=True)

# ---------- circle, L=256 (published theta=0.2895 at uv=(0.30,0.42)?)
def circ(L=256,a=2.0,Lg=1.0,uv=(0.30,0.42),cap=1e10,iters=3000):
    t0=time.time(); S=setup(L=L,a=a,Lg=Lg,alpha=3.0,cap=cap,uv=uv)
    D=S['D']; u=S['u']; nu2=S['nu2']
    def Aop(gg):
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=gg
        v,_=S['riesz'](G); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T)
    ip=lambda X,Y: np.real(np.vdot(X,Y))
    print(f"CIRC L={L} a={a} Lg={Lg} uv={uv} |D|={len(D)} |u|^2={nu2:.6f}",flush=True)
    x,th=cg(Aop,b,ip,None,iters,"circ")
    print(f"  -> theta={th/nu2:.5f}  ({time.time()-t0:.0f}s)",flush=True)

if __name__=='__main__':
    gal(); circ(L=256); circ(L=128)
