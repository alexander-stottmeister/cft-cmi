import mpmath as mp
mp.mp.dps=40
def rnd(n,seed):
    mp.mp.dps=40; import random; random.seed(seed)
    A=mp.matrix(n,n)
    for i in range(n):
        for j in range(n): A[i,j]=mp.mpf(random.uniform(-1,1))+1j*mp.mpf(random.uniform(-1,1))
    H=(A+A.transpose_conj())/2
    E,V=mp.eighe(H); E=[mp.re(e) for e in E]; lo=mp.mpf("0.02")
    mn,mx=min(E),max(E); w=[lo+(1-2*lo)*(e-mn)/(mx-mn) for e in E]
    D=mp.diag(w); return V*D*V.transpose_conj()
def fn(A,f):
    E,V=mp.eighe((A+A.transpose_conj())/2); return V*mp.diag([f(mp.re(e)) for e in E])*V.transpose_conj()
def F_exact(X,Y):
    n=X.rows; I=mp.eye(n)
    G1h=fn(X,lambda w: mp.sqrt(w/(1-w))); G2=fn(Y,lambda w: w/(1-w))
    T=G1h*G2*G1h; E,V=mp.eighe((T+T.transpose_conj())/2)
    return mp.re(mp.sqrt(mp.det(I-X)*mp.det(I-Y)))*mp.fprod([1+mp.sqrt(max(mp.re(e),mp.mpf(0))) for e in E])
def F_purif(X,Y):
    n=X.rows; I=mp.eye(n)
    M=fn(X,mp.sqrt)*fn(Y,mp.sqrt)+fn(I-X,mp.sqrt)*fn(I-Y,mp.sqrt)
    return abs(mp.det(M))
worst=mp.mpf(1)
for seed in range(40):
    n=3; X=rnd(n,seed); Y=rnd(n,1000+seed)
    a=F_exact(X,Y); b=F_purif(X,Y)
    if seed<5: print("  seed=%2d  F_exact=%s  F_purif=%s  ratio=%s"%(seed,mp.nstr(a,12),mp.nstr(b,12),mp.nstr(b/a,10)))
    worst=max(worst,b/a)
print("max  F_purif/F_exact over 40 random 3x3 pairs =",mp.nstr(worst,12))
# near-diagonal perturbative regime
worst=mp.mpf(0)
for seed in range(30):
    n=4; X=rnd(n,seed); P=rnd(n,500+seed); P=(P-mp.eye(n)*mp.mpf('0.5'))*mp.mpf('1e-3')
    Y=X+(P+P.transpose_conj())/2
    a=F_exact(X,Y); b=F_purif(X,Y)
    worst=max(worst,(-mp.log(a))/(-mp.log(b)))
print("max Phi_exact / Phi_purif in perturbative regime (must be <=1):",mp.nstr(worst,10))
