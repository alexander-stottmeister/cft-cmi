import numpy as np, scipy.linalg as sla, itertools
np.random.seed(7)
m=4
# build fermionic Fock space operators
dim=2**m
def annih(j):
    a=np.zeros((dim,dim))
    for s in range(dim):
        b=[(s>>k)&1 for k in range(m)]
        if b[j]==1:
            sgn=(-1)**sum(b[:j]); t=s & ~(1<<j)
            a[t,s]=sgn
    return a
A=[annih(j) for j in range(m)]
def rhoQ(Q):
    # gauge-invariant quasifree state with <a_i^† a_j> = Q_{ji}
    K=sla.logm(np.linalg.inv(Q)-np.eye(m))   # rho = exp(-dGamma(K))/Z ; Q=(1+e^K)^{-1}
    H=sum(K[i,j]*A[i].conj().T@A[j] for i in range(m) for j in range(m))
    R=sla.expm(-H); R=R/np.trace(R); return R
def checkQ(R):
    return np.array([[np.trace(R@A[i].conj().T@A[j]) for i in range(m)] for j in range(m)])
def rootfid(r,s):
    sr=sla.sqrtm(r); ss=sla.sqrtm(s); M=sr@ss
    return np.sum(sla.svdvals(M))
X=np.random.randn(m,m)+1j*np.random.randn(m,m); X=(X+X.conj().T)/2
Q1=sla.expm(X); Q1=Q1/ (np.linalg.eigvalsh(Q1).max()*1.7)   # spectrum in (0,1)
D=np.random.randn(m,m)+1j*np.random.randn(m,m); D=(D+D.conj().T)/2; D=D/np.linalg.norm(D)
R1=rhoQ(Q1); print("symbol check ||Q-Q||=",np.linalg.norm(checkQ(R1)-Q1))
q,U=np.linalg.eigh(Q1); Dd=U.conj().T@D@U
N=np.add.outer(q*0,0)+np.array([[q[i]*(1-q[k])+q[k]*(1-q[i]) for k in range(m)] for i in range(m)])
W=np.array([[ (np.sqrt(q[i]*(1-q[k]))+np.sqrt(q[k]*(1-q[i])))**2 for k in range(m)] for i in range(m)])
gB_1p=2*np.sum(np.abs(Dd)**2/N); print("one-particle gB=2 sum|D|^2/N =",gB_1p,"  gB/8=",gB_1p/8)
h2coef=0.5*np.sum(np.abs(Dd)**2/W); print("Hellinger coef (1/2)sum|D|^2/W =",h2coef)
# many-body SLD from Hubner
p,V=np.linalg.eigh(R1)
print("\n eps        -logF/eps^2      -logHell/eps^2")
for eps in [1e-2,3e-3,1e-3,3e-4]:
    Q2=Q1+eps*D; R2=rhoQ(Q2)
    F=rootfid(R1,R2); He=np.real(np.trace(sla.sqrtm(R1)@sla.sqrtm(R2)))
    print(f" {eps:8.1e}  {-np.log(F)/eps**2:15.8f}  {-np.log(He)/eps**2:15.8f}")
# many-body Hubner gB
eps=1e-6; Rp=rhoQ(Q1+eps*D); Rm=rhoQ(Q1-eps*D); dR=(Rp-Rm)/(2*eps)
dRe=V.conj().T@dR@V
gB_mb=2*np.sum(np.abs(dRe)**2/np.add.outer(p,p))
print("\n many-body Hubner gB =",gB_mb," vs one-particle 2sum|D|^2/N =",gB_1p," /8:",gB_mb/8)
# Legendre: sup over all self-adjoint X of 2Tr(dR X)-Tr(R X^2) == gB
Jinv_dR = np.zeros_like(dRe)
for i in range(dim):
    for j in range(dim):
        Jinv_dR[i,j]=2*dRe[i,j]/(p[i]+p[j])
L=V@Jinv_dR@V.conj().T
print(" Legendre value 2Tr(dR L)-Tr(R L^2) =",np.real(2*np.trace(dR@L)-np.trace(R1@L@L)))
# Hellinger closed form det(S1S2+C1C2)
eps=1e-2; Q2=Q1+eps*D
S1=sla.sqrtm(Q1);S2=sla.sqrtm(Q2);C1=sla.sqrtm(np.eye(m)-Q1);C2=sla.sqrtm(np.eye(m)-Q2)
Aop=S1@S2+C1@C2
print("\n det(S1S2+C1C2)=",np.real(np.linalg.det(Aop))," vs Tr sqrt(r1)sqrt(r2)=",np.real(np.trace(sla.sqrtm(R1)@sla.sqrtm(rhoQ(Q2)))))
Theta=(S1-S2)@(S1-S2)+(C1-C2)@(C1-C2)
print(" ||Re A - (1 - Theta/2)|| =",np.linalg.norm((Aop+Aop.conj().T)/2-(np.eye(m)-Theta/2)))
print(" det Re A =",np.real(np.linalg.det((Aop+Aop.conj().T)/2))," <= |det A| =",abs(np.linalg.det(Aop)))
print(" F >= Hell:", rootfid(R1,rhoQ(Q2)), ">=", np.real(np.linalg.det(Aop)))
# Note5 Thm2.1 determinant formula for root fidelity
G1=Q1@np.linalg.inv(np.eye(m)-Q1); G2=Q2@np.linalg.inv(np.eye(m)-Q2)
g1h=sla.sqrtm(G1)
Ffo=np.sqrt(np.real(np.linalg.det((np.eye(m)-Q1)@(np.eye(m)-Q2))))*np.real(np.linalg.det(np.eye(m)+sla.sqrtm(g1h@G2@g1h)))
print(" Note5 Thm2.1 formula F =",Ffo," vs direct rootfid =",rootfid(R1,rhoQ(Q2)))
