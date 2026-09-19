"""S10 (Phase 3b): the obstruction (S).
u = Pi_N M is the g_Q-Riesz vector of the compression direction; it solves
  S_Q(l) = -(1/2) ddelta ,  u = P^perp l P,   S_Q(l)=Q l (1-Q)+(1-Q) l Q ,
  ddelta = E_I [P,Dchi] E_I,  Q = E_I P E_I.
Test: is E_D u E_D self-adjoint?  theta >= |antiherm(E_D u E_D)|^2/|u|^2 is a lower
bound on the relative gain of the isometric orbit over the compression."""
import numpy as np

def model(n, nA, nD, taper=4.0, cap=1e12):
    hop = -(np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1))
    w,V = np.linalg.eigh(hop); P = V[:,w<0]@V[:,w<0].conj().T
    Pp = np.eye(n)-P
    A=np.arange(nA); D=np.arange(nA,nA+nD); I=np.arange(nA+nD)
    x=(np.arange(n)-nA+0.5)/nD
    chi=np.zeros(n); chi[D]=-x[D]**2
    out=np.arange(nA+nD,n)
    chi[out]=-x[out]**2*np.exp(-taper*(x[out]-1.0))     # C^inf continuation of -x^2
    h=1.0/nD
    grad=(np.diag(np.ones(n-1),1)-np.diag(np.ones(n-1),-1))/(2*h)
    Dchi=0.5*(np.diag(chi)@grad+grad@np.diag(chi))
    EI=np.zeros((n,n)); EI[I,I]=1
    ddelta=EI@(P@Dchi-Dchi@P)@EI                        # E_I [P,Dchi] E_I
    ddelta=ddelta[np.ix_(I,I)]                          # as operator on h_I
    Q=P[np.ix_(I,I)]
    q,U=np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
    dt=U.conj().T@(-0.5*ddelta)@U
    denom=q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None]
    wt=np.minimum(1.0/denom,cap)
    l=U@(wt*dt)@U.conj().T                              # l_* on h_I
    L=np.zeros((n,n),complex); L[np.ix_(I,I)]=l
    u=Pp@L@P
    R=u[np.ix_(D,D)]
    Ra=0.5*(R-R.conj().T)
    nu=np.linalg.norm(u); nR=np.linalg.norm(R); nRa=np.linalg.norm(Ra)
    return dict(nu=nu,nR=nR,nRa=nRa,ratio=nRa/nR,theta_lb=(nRa/nu)**2,
                gQ=-0.25*np.real(np.trace(l@ddelta)))

if __name__=="__main__":
    print("n  nA nD taper cap      |u|      |E_DuE_D| antiherm/|R| theta_lb   gQ(=|u|^2/2)")
    for (n,nA,nD) in [(96,32,16),(120,40,20),(160,56,24)]:
        for taper in (2.0,4.0,8.0):
            for cap in (1e4,1e6,1e8,1e10):
                r=model(n,nA,nD,taper,cap)
                print(f"{n:3d} {nA:2d} {nD:2d} {taper:4.1f} {cap:7.0e} {r['nu']:9.4f} {r['nR']:9.4f}"
                      f"  {r['ratio']:9.5f} {r['theta_lb']:9.5f} {r['gQ']:10.4f}")
            print()
