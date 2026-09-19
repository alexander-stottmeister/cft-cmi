"""F3 T2: circle model, FAST theta operator (all matmuls restricted to the I-block; the
original s10_theta riesz does full LxL products).  Validated against f3_circ (L=256: 0.28958)."""
import sys, time, numpy as np
import f3_circ as C

def prep(S, a, Lg):
    L=S['L']; I=S['I']; D=S['D']; P=S['P']; Pp=S['Pp']
    iD = np.searchsorted(I, D)                  # position of D inside I
    PID = P[np.ix_(I,D)]; PDI = P[np.ix_(D,I)]; PpDI = Pp[np.ix_(D,I)]
    q,U = np.linalg.eigh(S['Q_I']) if 'Q_I' in S else (None,None)
    x = np.tan(S['thw'][D]/2.0); xi = np.log((x+a)/(Lg-x))
    return dict(I=I,D=D,iD=iD,PID=PID,PDI=PDI,PpDI=PpDI,xi=xi)

def setup2(L=512,a=2.0,Lg=1.0,alpha=3.0,cap=1e10,uv=(0.30,0.42),taper='smooth'):
    S = C.setup(L=L,a=a,Lg=Lg,alpha=alpha,cap=cap,uv=uv,taper=taper)
    P=S['P']; Pp=S['Pp']; I=S['I']; D=S['D']; nI=len(I); nD=len(D)
    iD = np.searchsorted(I,D)
    Q = P[np.ix_(I,I)]; Q=0.5*(Q+Q.conj().T)
    q,U = np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
    den = q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None]
    w = np.minimum(1.0/den, cap)
    PID = P[np.ix_(I,D)]; PDI = P[np.ix_(D,I)]
    PpDI = Pp[np.ix_(D,I)]; PID2 = P[np.ix_(I,D)]
    def riesz_DD(G):                 # G: nD x nD anti-herm -> R = (Pp l P)[D,D], l from eta
        eta = PID @ G                              # (nI x nD)
        E = np.zeros((nI,nI),complex); E[:,iD] = eta; E[iD,:] -= (G @ PDI)
        l = U@(w*(U.conj().T@(-E)@U))@U.conj().T
        return PpDI @ l @ PID2
    x = np.tan(S['thw'][D]/2.0); xi = np.log((x+a)/(Lg-x))
    return dict(S=S,riesz_DD=riesz_DD,D=D,I=I,u=S['u'],nu2=S['nu2'],xi=xi,q=q,U=U,w=w,iD=iD)

def theta2(T, B=None, iters=20000):
    u=T['u']; D=T['D']
    R=u[np.ix_(D,D)]
    def Aop(gg):
        g2 = gg if B is None else B@gg@B.conj().T
        Rr = T['riesz_DD'](g2)
        if B is not None: Rr = B.conj().T@Rr@B
        return 0.5*(Rr-Rr.conj().T)
    b = 0.5*(R-R.conj().T)
    if B is not None: b = 0.5*(B.conj().T@R@B - (B.conj().T@R@B).conj().T)
    ip=lambda X,Y: np.real(np.vdot(X,Y))
    x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=ip(r,r); nb=np.linalg.norm(b); prev=None; stall=0
    for k in range(iters):
        Ap=Aop(p); pAp=ip(p,Ap)
        if pAp<=1e-300: break
        al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=ip(r,r); p=r+(rs2/rs)*p; rs=rs2
        if (k+1)%50==0:
            cur=ip(b,x)/T['nu2']
            if prev is not None and abs(cur-prev)<1e-8*max(cur,1e-30): stall+=1
            else: stall=0
            prev=cur
            if stall>=2: break
        if np.sqrt(rs2)<1e-14*nb: break
    return ip(b,x)/T['nu2'], k+1, x

def run(L=512,a=2.0,Lg=1.0,uv=(0.30,0.42),cap=1e10,taper='smooth',alpha=3.0,Ds=None):
    t0=time.time(); T=setup2(L=L,a=a,Lg=Lg,cap=cap,uv=uv,taper=taper,alpha=alpha)
    th,k,_=theta2(T)
    print(f"L={L} a={a} Lg={Lg} taper={taper}{uv if taper=='smooth' else ''} cap={cap:.0e} al={alpha} "
          f"|D|={len(T['D'])} xi=[{T['xi'].min():.2f},{T['xi'].max():.2f}] |u|^2={T['nu2']:.6f} "
          f"theta={th:.5f} cg={k} {time.time()-t0:.0f}s",flush=True)
    if Ds is not None:
        xi=T['xi']; xm=xi.max(); nD=len(T['D'])
        for Dl in Ds:
            sel=np.where(xi<=xm-Dl)[0]
            if len(sel)<2: continue
            B=np.zeros((nD,len(sel))); B[sel,np.arange(len(sel))]=1.0
            th2,k2,_=theta2(T,B=B)
            print(f"   Delta={Dl:5.2f} r={len(sel)} theta={th2:.5f} cg={k2}",flush=True)
    return th
if __name__=='__main__':
    job=sys.argv[1] if len(sys.argv)>1 else 'check'
    if job=='check': run(L=256); run(L=512)
    elif job=='Lsweep':
        for L in (128,192,256,320,384,512,640,768,896,1024): run(L=L)
    elif job=='taper':
        for L in (256,512,768):
            for uv in [(0.20,0.32),(0.30,0.42),(0.35,0.47),(0.42,0.49),(0.46,0.499)]: run(L=L,uv=uv)
            run(L=L,taper='none'); run(L=L,taper='none',cap=1e6)
    elif job=='phi':
        for L in (256,512,768): run(L=L,Ds=(0.25,0.5,1.,1.5,2.,3.,4.))
    elif job=='geom':
        for (a,Lg) in [(1.0,2.0),(1.0,1.0),(2.0,1.0),(4.0,1.0),(1.0,4.0),(2.0,0.5)]: run(L=512,a=a,Lg=Lg)
