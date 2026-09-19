import numpy as np
rng=np.random.default_rng(7)
def rnd(n,lo=1e-9):
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); H=(A+A.conj().T)/2
    w,V=np.linalg.eigh(H); w=lo+(1-2*lo)*(w-w.min())/(w.max()-w.min())
    return (V*w)@V.conj().T
def fid(X,Y):
    w1,V1=np.linalg.eigh(X); w2,V2=np.linalg.eigh(Y)
    G1h=(V1*np.sqrt(w1/(1-w1)))@V1.conj().T; G2=(V2*(w2/(1-w2)))@V2.conj().T
    t=np.linalg.eigvalsh(G1h@G2@G1h)
    return 0.5*np.sum(np.log(1-w1))+0.5*np.sum(np.log(1-w2))+np.sum(np.log(1+np.sqrt(np.clip(t,0,None))))
def hf(A):
    w,V=np.linalg.eigh(A); w=np.clip(w,0,1); return (V*np.sqrt(w*(1-w)))@V.conj().T
def sqm(A,f):
    w,V=np.linalg.eigh(A); w=np.clip(w,0,1); return (V*f(w))@V.conj().T
print("== Lemma 3.2 (purification bound): -log F  <=  -1/2 log det(1-N*N)  <= |N|_2^2/(2(1-|N|_2^2)) ==")
bad=0
for trial in range(300):
    n=rng.integers(2,7); X=rnd(n); Y=rnd(n)
    N=sqm(X,np.sqrt)@sqm(1-np.eye(n)*0-Y+np.eye(n)*0,lambda w:np.sqrt(w)) if False else \
      sqm(X,np.sqrt)@sqm(np.eye(n)-Y,np.sqrt)-sqm(np.eye(n)-X,np.sqrt)@sqm(Y,np.sqrt)
    lhs=-fid(X,Y); mid=-0.5*np.log(np.linalg.det(np.eye(n)-N.conj().T@N)).real
    n2=np.linalg.norm(N,'fro')**2; rhs=n2/(2*(1-n2)) if n2<1 else np.inf
    if not (lhs<=mid+1e-12 and mid<=rhs+1e-12): bad+=1
    if trial<3: print("   n=%d  -logF=%.6e  purif=%.6e  HS=%.6e"%(n,lhs,mid,rhs))
print("   violations in 300 random trials:",bad)
print("== Lemma 2.2 (factorisation): F(rho,rho'')=F_W  with Q block diagonal ==")
for trial in range(3):
    n=8; m=5; w=np.sort(rng.uniform(1e-6,1-1e-6,n))[::-1]; Q=np.diag(w)
    Dl=rnd(n)*0.01; Dl=(Dl+Dl.conj().T)/2*0.05; Qt=Q-Dl
    ev=np.linalg.eigvalsh(Qt); assert ev.min()>0 and ev.max()<1, ev
    E=np.zeros(n,bool); E[:m]=True
    Qpp=np.zeros_like(Qt); Qpp[np.ix_(E,E)]=Qt[np.ix_(E,E)]; Qpp[np.ix_(~E,~E)]=Q[np.ix_(~E,~E)]
    lhs=-fid(Q,Qpp); rhs=-fid(Q[np.ix_(E,E)],Qt[np.ix_(E,E)])
    print("   -logF(rho,rho'')=%.12e   Phi_W=%.12e   rel.diff=%.2e"%(lhs,rhs,abs(lhs-rhs)/max(abs(rhs),1e-30)))
