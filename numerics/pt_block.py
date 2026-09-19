import numpy as np, sys
sys.path.insert(0,'.'); from compression_box import Q_box
def hf(A):
    w,V=np.linalg.eigh(A); w=np.clip(w,0,1); return (V*np.sqrt(w*(1-w)))@V.conj().T
def sq(A,f):
    w,V=np.linalg.eigh(A); w=np.clip(w,0,1); return (V*f(w))@V.conj().T
for fn,Lam,kmax in [("Dhat_exact_s0.2_Lam60_k30_g12.npz",60,30),
                    ("Dhat_exact_s0.2_Lam120_k45_g12.npz",120,45)]:
    d=np.load(fn); D=d['Dhat']; kap=d['kappa'] if 'kappa' in d else None
    N=D.shape[0]; k=2*np.pi*np.arange(-(N//2),N//2+1)/Lam*1.0
    kappa=2*np.pi*np.arange(-(N//2),N//2+1)*(2*np.pi/Lam)   # placeholder, replaced below
    print("### %s  N=%d  keys=%s"%(fn,N,list(d.keys())))
    kk=d['kappa'] if 'kappa' in d else None
    Q=Q_box(kk,Lam,xi0=np.log(0.5)) if kk is not None else None
    if Q is None: print("   no kappa key"); continue
    Qt=Q-D
    w,V=np.linalg.eigh(Q); kapv=np.log((1-w)/w)
    Xf=V.conj().T@Qt@V                        # everything in the Q-eigenbasis (Q = diag(w))
    for kc in [18.4,25.3,32.2]:
        E=np.abs(kapv)<=kc; Ec=~E; Ep=kapv>kc; Em=kapv<-kc
        if Ec.sum()==0: print("   kc=%.1f : window = full box"%kc); continue
        X=Xf; Qd=np.diag(w)
        tp=np.real(np.trace(X[np.ix_(Ep,Ep)])); tm=np.real(np.trace(np.eye(Em.sum())-X[np.ix_(Em,Em)]))
        nup=w[Ep].sum(); num=(1-w[Em]).sum(); tau=tp+tm; nu=nup+num
        Y=np.zeros_like(X); Y[np.ix_(E,E)]=X[np.ix_(E,E)]; Y[np.ix_(Ec,Ec)]=np.diag(w[Ec])
        hX=hf(X); hY=hf(Y)
        N2=np.linalg.norm(X-Y,'fro')**2+np.linalg.norm(hX-hY,'fro')**2
        X12=np.linalg.norm(X[np.ix_(E,Ec)],'fro')**2
        hoff=np.linalg.norm(hX[np.ix_(Ec,E)],'fro')**2
        print("   kc=%4.1f n_out=%3d  tau+=%9.3e tau-=%9.3e nu=%9.3e | |N|_2^2=%9.3e  5tau+nu=%9.3e ratio=%6.4f"
              %(kc,Ec.sum(),tp,tm,nu,N2,5*tau+nu,N2/(5*tau+nu)))
        print("        |X12|_2^2=%9.3e  |E^perp h(X)E|_2^2=%9.3e   tau/2=%9.3e  Sigma_cont=%9.3e"
              %(X12,hoff,tau/2,(1.0/15)/15/kc**2*0+ (0.0666667**2)/(15*kc*kc)))
