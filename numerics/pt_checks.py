import numpy as np
xs,ws=np.polynomial.legendre.leggauss(160)          # sigma nodes on [0,1]
sig=0.5*(xs+1); wsig=0.5*ws
xt,wt=np.polynomial.legendre.leggauss(48)
def gvec(t,z):                                       # g(t) = int_0^1 Ftilde(t s, t(1-s)) ds
    t=np.asarray(t,dtype=float)[:,None]
    B=np.sinh(t/2); A=np.sinh(t*sig/2)*np.sinh(t*(1-sig)/2)
    val=z*A/(B*(B+2*z*A))
    return (val*wsig).sum(1)
def g1vec(t):
    t=np.asarray(t,dtype=float)
    out=np.where(t==0,1/6.0,0.0); m=t!=0
    tt=t[m]; out[m]=(tt*np.cosh(tt/2)-2*np.sinh(tt/2))/(2*tt*np.sinh(tt/2)**2)
    return out
def osc(f,lam,T=90.0):                               # int_0^T f(t) cos(lam t) dt, period-by-period GL
    P=np.pi/lam; edges=np.arange(0,T+P,P); tot=0.0
    for a,b in zip(edges[:-1],edges[1:]):
        t=0.5*(b-a)*xt+0.5*(a+b); w=0.5*(b-a)*wt
        tot+=np.sum(w*f(t)*np.cos(lam*t))
    return tot
print("== A1:  hat g1(lam)=2 int_0^inf g1 cos(lam t)dt,  lam=kc/2pi ==")
A1=0
for kc in [6,8,12,18.4,25.3,32.2,40]:
    lam=kc/(2*np.pi); v=2*osc(g1vec,lam); r=abs(v)/((1+kc)*np.exp(-kc)); A1=max(A1,r)
    print("   kc=%5.1f  hat_g1=%12.5e  ratio=%9.4f"%(kc,v,r))
print("   -> A1 <= %.3f"%A1)
print("== Sigma(kc)=1/(2pi^2) int_0^inf g cos(lam t)dt   vs   z^2/(15 kc^2) ==")
for z in [0.0667,0.2,1.0]:
    for kc in [18.4,25.3,32.2]:
        lam=kc/(2*np.pi); S=osc(lambda t:gvec(t,z),lam)/(2*np.pi**2); lead=z*z/(15*kc*kc)
        print("   z=%6.4f kc=%5.1f Sigma=%12.5e lead=%12.5e ratio=%7.4f  rem*kc^3/z^2=%8.4f"%(
              z,kc,S,lead,S/lead,(S-lead)*kc**3/z**2))
