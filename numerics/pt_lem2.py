import numpy as np
rng=np.random.default_rng(7)
def rnd(n,lo=1e-9):
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); H=(A+A.conj().T)/2
    w,V=np.linalg.eigh(H); w=lo+(1-2*lo)*(w-w.min())/(w.max()-w.min()); return (V*w)@V.conj().T
def fid(X,Y):
    w1,V1=np.linalg.eigh(X); w2,V2=np.linalg.eigh(Y)
    G1h=(V1*np.sqrt(w1/(1-w1)))@V1.conj().T; G2=(V2*(w2/(1-w2)))@V2.conj().T
    t=np.linalg.eigvalsh(G1h@G2@G1h)
    return 0.5*np.sum(np.log(1-w1))+0.5*np.sum(np.log(1-w2))+np.sum(np.log(1+np.sqrt(np.clip(t,0,None))))
def sqm(A,f):
    w,V=np.linalg.eigh(A); w=np.clip(w,0,1); return (V*f(w))@V.conj().T
worst=0; bad=0
for trial in range(2000):
    n=int(rng.integers(2,7)); X=rnd(n); Y=rnd(n); I=np.eye(n)
    N=sqm(X,np.sqrt)@sqm(I-Y,np.sqrt)-sqm(I-X,np.sqrt)@sqm(Y,np.sqrt)
    sv=np.clip(np.linalg.svd(N,compute_uv=False),0,1-1e-16)
    mid=-np.sum(np.log1p(-sv**2))/2; lhs=-fid(X,Y)
    d=lhs-mid
    if d>1e-11: bad+=1; worst=max(worst,d/max(mid,1e-12))
print("violations (lhs>mid):",bad,"/2000   worst relative excess:",worst)
# small-perturbation regime (the one used in the note)
bad2=0; rat=[]
for trial in range(2000):
    n=int(rng.integers(2,8)); X=rnd(n,1e-6); Dl=rnd(n)*0; A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    P=(A+A.conj().T)/2*1e-4; Y=X+P
    ev=np.linalg.eigvalsh(Y)
    if ev.min()<=1e-12 or ev.max()>=1-1e-12: continue
    I=np.eye(n); N=sqm(X,np.sqrt)@sqm(I-Y,np.sqrt)-sqm(I-X,np.sqrt)@sqm(Y,np.sqrt)
    sv=np.linalg.svd(N,compute_uv=False); mid=-np.sum(np.log1p(-sv**2))/2; lhs=-fid(X,Y)
    if lhs>mid*(1+1e-8)+1e-15: bad2+=1
    rat.append(lhs/mid)
print("perturbative regime: violations",bad2,"of",len(rat),"  min/max ratio -logF/purif = %.4f %.4f"%(min(rat),max(rat)))
