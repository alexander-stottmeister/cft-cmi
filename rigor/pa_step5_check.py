import numpy as np
rng=np.random.default_rng(7)
def hermbasis(m):
    B=[]
    for i in range(m):
        E=np.zeros((m,m),complex); E[i,i]=1; B.append(E)
    for i in range(m):
        for j in range(i+1,m):
            E=np.zeros((m,m),complex); E[i,j]=1; E[j,i]=1; B.append(E)
            E=np.zeros((m,m),complex); E[i,j]=1j; E[j,i]=-1j; B.append(E)
    return B
def realvec(X):  # complex matrix -> real vector
    return np.concatenate([X.real.ravel(),X.imag.ravel()])
def test(n,k,m,seed):
    rng=np.random.default_rng(seed)
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); A=A+A.conj().T
    w,U=np.linalg.eigh(A); Pp=U[:,:k]@U[:,:k].conj().T; Pm=np.eye(n)-Pp
    EI=np.diag([1.0]*m+[0.0]*(n-m)); EIp=np.eye(n)-EI
    L=[]; K=[]
    for h in hermbasis(m):
        hh=np.zeros((n,n),complex); hh[:m,:m]=h
        L.append(realvec(Pm@hh@Pp))
    for h in hermbasis(n-m):
        hh=np.zeros((n,n),complex); hh[m:,m:]=h
        K.append(realvec(1j*(Pm@hh@Pp)))   # i*K
    L=np.array(L).T; K=np.array(K).T
    rL=np.linalg.matrix_rank(L,tol=1e-9); rK=np.linalg.matrix_rank(K,tol=1e-9)
    # ambient real dimension of Pm X Pp block
    amb=2*k*(n-k)
    # check orthogonality and completeness
    G=L.T@K; orth=np.abs(G).max()
    M=np.concatenate([L,K],axis=1); rM=np.linalg.matrix_rank(M,tol=1e-9)
    # random target in the block, check Pythagoras
    X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); X=Pm@X@Pp; v=realvec(X)
    def proj(B,v):
        Q,_=np.linalg.qr(B); Q=Q[:,:np.linalg.matrix_rank(B,tol=1e-9)]
        return Q@(Q.T@v)
    pL=proj(L,v); pK=proj(K,v)
    lhs=pL@pL+pK@pK; rhs=v@v
    return dict(n=n,k=k,m=m,ambient=amb,dimL=rL,dimK=rK,sum=rL+rK,rankLK=rM,
                max_inner=orth,pyth_lhs=lhs,pyth_rhs=rhs,rel=abs(lhs-rhs)/rhs)
for (n,k,m) in [(4,2,2),(5,2,2),(6,3,3),(6,2,3),(7,3,2),(8,4,3)]:
    r=test(n,k,m,10*n+k+m)
    print(f"n={r['n']} k={r['k']} m={r['m']} ambient={r['ambient']} dimL={r['dimL']} dimK={r['dimK']} sum={r['sum']} rank(L|K)={r['rankLK']} max<L,K>={r['max_inner']:.2e} Pyth rel.err={r['rel']:.3e}")
