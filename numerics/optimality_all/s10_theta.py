"""S10: the relative gain theta of the isometric orbit over the compression.
theta = <R_a, A^{-1} R_a> / |u|^2 ,  A(G) = antiherm(E_D v_G E_D),
v_G = Pi_N(P^perp G P) obtained from S_Q(l) = -E_I[P,G]E_I,  v = P^perp l P.
R_a = antiherm(E_D u E_D),  u the Riesz vector of the compression direction.
If theta > 0 the zero-collar compression is NOT the optimum: E^(2) <= (1-theta) f2 z^2."""
import numpy as np

def setup(L=512, a=2.0, Lg=1.0, alpha=3.0, cap=1e10, uv=(0.30,0.42)):
    th=2*np.pi*np.arange(L)/L; thw=np.where(th>np.pi,th-2*np.pi,th)
    n=np.fft.fftfreq(L,d=1.0/L); nu=n+0.5
    F=np.fft.fft(np.eye(L),axis=0)/L; Fi=np.fft.ifft(np.eye(L),axis=0)*L
    P=Fi@np.diag((nu>0).astype(float))@F; P=0.5*(P+P.conj().T); Pp=np.eye(L)-P
    a1,a2=uv; xx=(np.abs(nu)/L-a1)/(a2-a1); s_=np.clip(1-xx,0,1); s_=s_*s_*(3-2*s_)
    d=Fi@np.diag(1j*nu*s_)@F; d=0.5*(d-d.conj().T)
    thD=2*np.arctan(Lg); thA=-2*np.arctan(a)
    inD=(thw>0)&(thw<thD); inA=(thw>thA)&(thw<0); inI=inD|inA
    chi=np.zeros(L); chi[inD]=np.cos(thw[inD])-1.0
    t=thw.copy(); t[t<thA]+=2*np.pi; m=~inI
    chi[m]=(np.cos(t[m])-1.0)*np.exp(-alpha*(t[m]-thD)**2)
    X=np.diag(chi); Dc=0.5*(X@d+d@X); Dc=0.5*(Dc-Dc.conj().T)
    I=np.where(inI)[0]; D=np.where(inD)[0]
    iD=np.searchsorted(I,D)                       # position of D inside I
    Q=P[np.ix_(I,I)]; Q=0.5*(Q+Q.conj().T)
    q,U=np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
    den=q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None]
    w=np.minimum(1.0/den,cap)
    PI=P[np.ix_(I,I)]; PpI=Pp[np.ix_(I,I)]
    def riesz(Gfull):                              # G anti-herm supported in D (LxL)
        eta=( P@Gfull-Gfull@P )[np.ix_(I,I)]       # E_I[P,G]E_I  restricted
        l=U@(w*(U.conj().T@(-eta)@U))@U.conj().T
        Lf=np.zeros((L,L),complex); Lf[np.ix_(I,I)]=l
        v=Pp@Lf@P
        return v, -0.5*np.real(np.trace(l@eta))
    u,nu2=riesz(Dc)
    return dict(L=L,P=P,Pp=Pp,D=D,u=u,nu2=nu2,riesz=riesz)

def theta(S, iters=200):
    L=S['L']; D=S['D']; u=S['u']; nu2=S['nu2']
    def emb(g):
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g; return G
    def A(g):
        v,_=S['riesz'](emb(g)); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T)
    x=np.zeros_like(b); r=b.copy(); p=r.copy()
    rs=np.real(np.vdot(r,r)); hist=[]
    for k in range(iters):
        Ap=A(p); pAp=np.real(np.vdot(p,Ap))
        if pAp<=1e-30: break
        al=rs/pAp; x=x+al*p; r=r-al*Ap
        rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
        if k%20==19 or k==iters-1: hist.append((k+1,np.real(np.vdot(b,x))/nu2))
    return np.real(np.vdot(b,x))/nu2, hist, np.linalg.norm(b)**2/nu2

if __name__=="__main__":
    for (L,a,Lg) in [(256,2.0,1.0),(384,2.0,1.0),(512,2.0,1.0),(512,1.0,1.0),(512,4.0,1.0)]:
        S=setup(L=L,a=a,Lg=Lg)
        th,hist,lb=theta(S,iters=120)
        print(f"L={L} a={a} Lg={Lg}: |u|^2={S['nu2']:.6f} crude_lb={lb:.5f} theta={th:.5f}")
        print("   CG ladder:", " ".join(f"{k}:{val:.4f}" for k,val in hist[:8]))

def diagnostics(L=512,a=2.0,Lg=1.0,uv=(0.30,0.42),alpha=3.0,cap=1e10,iters=150):
    S=setup(L=L,a=a,Lg=Lg,alpha=alpha,cap=cap,uv=uv)
    D=S['D']; u=S['u']; nu2=S['nu2']
    def emb(g):
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g; return G
    def A(g):
        v,_=S['riesz'](emb(g)); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T)
    x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=np.real(np.vdot(r,r))
    for k in range(iters):
        Ap=A(p); pAp=np.real(np.vdot(p,Ap))
        if pAp<=1e-30: break
        al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
    th=np.real(np.vdot(b,x))/nu2
    # optimal G (up to scale) is x ; eps_* G_* :  eps=-b(dc,eta)/gQ(eta) with G=x
    v,_=S['riesz'](emb(x)); nv2=np.real(np.vdot(v,v))
    ip=np.real(np.vdot(u,v))
    eps=-ip/nv2                     # in units of s
    G=eps*x
    print(f"  uv={uv} L={L} cap={cap:.0e}: theta={th:.5f}  |u|^2={nu2:.6f}"
          f"  ||G_*||_op/s={np.linalg.norm(G,2):.3f}  ||G_*||_2/s={np.linalg.norm(G):.3f}"
          f"  cos^2={ip**2/(nu2*nv2):.5f}")
    return th

if __name__=="__main__":
    print("\n--- UV taper stability / diagnostics ---")
    for uv in [(0.20,0.32),(0.30,0.42),(0.38,0.48)]: diagnostics(uv=uv)
    for L in (256,384,512,640): diagnostics(L=L)
    for cap in (1e6,1e8,1e10,1e12): diagnostics(cap=cap)
