"""F3 T2: circle-model theta (s10_theta conventions, copied so the original is untouched):
taper window uv on the spectral derivative, weight cap, L, geometry, restricted G classes."""
import sys, time, numpy as np
f2 = 1.0/(12*np.pi**2)

def setup(L=512, a=2.0, Lg=1.0, alpha=3.0, cap=1e10, uv=(0.30,0.42), taper='smooth'):
    th=2*np.pi*np.arange(L)/L; thw=np.where(th>np.pi,th-2*np.pi,th)
    n=np.fft.fftfreq(L,d=1.0/L); nu=n+0.5
    F=np.fft.fft(np.eye(L),axis=0)/L; Fi=np.fft.ifft(np.eye(L),axis=0)*L
    P=Fi@np.diag((nu>0).astype(float))@F; P=0.5*(P+P.conj().T); Pp=np.eye(L)-P
    a1,a2=uv
    if taper=='none': s_=np.ones(L)
    elif taper=='gauss': s_=np.exp(-((np.abs(nu)/L)/a1)**2*np.log(2.0))
    else:
        xx=(np.abs(nu)/L-a1)/(a2-a1); s_=np.clip(1-xx,0,1); s_=s_*s_*(3-2*s_)
    d=Fi@np.diag(1j*nu*s_)@F; d=0.5*(d-d.conj().T)
    thD=2*np.arctan(Lg); thA=-2*np.arctan(a)
    inD=(thw>0)&(thw<thD); inA=(thw>thA)&(thw<0); inI=inD|inA
    chi=np.zeros(L); chi[inD]=np.cos(thw[inD])-1.0
    t=thw.copy(); t[t<thA]+=2*np.pi; m=~inI
    chi[m]=(np.cos(t[m])-1.0)*np.exp(-alpha*(t[m]-thD)**2)
    X=np.diag(chi); Dc=0.5*(X@d+d@X); Dc=0.5*(Dc-Dc.conj().T)
    I=np.where(inI)[0]; D=np.where(inD)[0]
    Q=P[np.ix_(I,I)]; Q=0.5*(Q+Q.conj().T)
    q,U=np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
    den=q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None]
    w=np.minimum(1.0/den,cap)
    def riesz(Gfull):
        eta=(P@Gfull-Gfull@P)[np.ix_(I,I)]
        l=U@(w*(U.conj().T@(-eta)@U))@U.conj().T
        Lf=np.zeros((L,L),complex); Lf[np.ix_(I,I)]=l
        return Pp@Lf@P, -0.5*np.real(np.trace(l@eta))
    u,nu2=riesz(Dc)
    return dict(L=L,P=P,Pp=Pp,D=D,I=I,u=u,nu2=nu2,riesz=riesz,thw=thw,q=q,inD=inD)

def theta(S, B=None, iters=4000, tag=''):
    """B: |D| x r orthonormal columns restricting the G class (None = full)."""
    L=S['L']; D=S['D']; u=S['u']; nu2=S['nu2']
    def Aop(gg):
        g2 = gg if B is None else B@gg@B.conj().T
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g2
        v,_=S['riesz'](G); R=v[np.ix_(D,D)]
        if B is not None: R = B.conj().T@R@B
        return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]
    if B is not None: R = B.conj().T@R@B
    b=0.5*(R-R.conj().T)
    ip=lambda X,Y: np.real(np.vdot(X,Y))
    x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=ip(r,r); nb=np.linalg.norm(b); prev=None; stall=0
    for k in range(iters):
        Ap=Aop(p); pAp=ip(p,Ap)
        if pAp<=1e-300: break
        al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=ip(r,r); p=r+(rs2/rs)*p; rs=rs2
        if (k+1)%25==0:
            cur=ip(b,x)/nu2
            if prev is not None and abs(cur-prev)<1e-7*max(cur,1e-30): stall+=1
            else: stall=0
            prev=cur
            if stall>=2: break
        if np.sqrt(rs2)<1e-14*nb: break
    return ip(b,x)/nu2, k+1, x

def run(L=512,a=2.0,Lg=1.0,uv=(0.30,0.42),cap=1e10,taper='smooth',alpha=3.0,tag=''):
    t0=time.time(); S=setup(L=L,a=a,Lg=Lg,alpha=alpha,cap=cap,uv=uv,taper=taper)
    th,k,x=theta(S)
    print(f"{tag}L={L} a={a} Lg={Lg} taper={taper}{uv if taper=='smooth' else ''} cap={cap:.0e} "
          f"alpha={alpha} |D|={len(S['D'])} |u|^2={S['nu2']:.6f} theta={th:.5f} cg={k} {time.time()-t0:.0f}s",flush=True)
    return th, S['nu2']

if __name__=='__main__':
    job=sys.argv[1] if len(sys.argv)>1 else 'check'
    if job=='check':
        run(L=256); run(L=128)
    elif job=='Lsweep':
        for L in (128,192,256,320,384,448,512,640,768): run(L=L)
    elif job=='taper':
        for L in (256,384,512):
            for uv in [(0.20,0.32),(0.30,0.42),(0.35,0.47),(0.42,0.49),(0.46,0.499)]: run(L=L,uv=uv)
            run(L=L,taper='none'); run(L=L,taper='none',cap=1e6)
    elif job=='caps':
        for cap in (1e4,1e6,1e8,1e12): run(L=512,cap=cap)
        for al in (1.5,6.0): run(L=512,alpha=al)
    elif job=='geom':
        for (a,Lg) in [(1.0,2.0),(1.0,1.0),(2.0,1.0),(4.0,1.0),(1.0,4.0)]: run(L=512,a=a,Lg=Lg)
