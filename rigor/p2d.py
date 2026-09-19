import numpy as np, itertools, scipy.linalg as sla
rng=np.random.default_rng(7)
n=4
def rand_herm(n):
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); return (A+A.conj().T)/2
def qf_rho(Q):
    # many-body density matrix in occupation basis
    w,U=np.linalg.eigh(Q); dim=2**n
    # build via one-particle: rho = det(1-Q) Gamma(G) ; in the eigenbasis of Q it is diagonal
    idx=list(itertools.product([0,1],repeat=n))
    p=np.array([np.prod([w[j] if o[j] else 1-w[j] for j in range(n)]) for o in idx])
    # transform to fixed basis: build Gamma(U) on Fock space
    return p, w, U, idx
def Gamma(X, idx):
    # matrix of Gamma(X) = sum_k X^{wedge k} in occupation basis given by idx
    dim=len(idx); M=np.zeros((dim,dim),dtype=complex)
    for a,oa in enumerate(idx):
        ia=[j for j in range(len(oa)) if oa[j]]
        for b,ob in enumerate(idx):
            ib=[j for j in range(len(ob)) if ob[j]]
            if len(ia)!=len(ib): continue
            if len(ia)==0: M[a,b]=1.0; continue
            M[a,b]=np.linalg.det(X[np.ix_(ia,ib)])
    return M
idx=list(itertools.product([0,1],repeat=n))
def rho_of_Q(Q):
    G=Q@np.linalg.inv(np.eye(n)-Q)
    return np.linalg.det(np.eye(n)-Q)*Gamma(G,idx)
def sqrtm_pos(A):
    w,U=np.linalg.eigh((A+A.conj().T)/2); return U@np.diag(np.sqrt(np.maximum(w,0)))@U.conj().T
# random Q1 in (0,1), D hermitian traceless
H=rand_herm(n); w,U=np.linalg.eigh(H); q=1/(1+np.exp(2*w)); Q1=U@np.diag(q)@U.conj().T
D=rand_herm(n); D=D-np.trace(D)/n*np.eye(n)
def Fmb(Q1,Q2):
    r1=rho_of_Q(Q1); r2=rho_of_Q(Q2); s1=sqrtm_pos(r1)
    M=s1@r2@s1; return np.sum(np.sqrt(np.maximum(np.linalg.eigvalsh((M+M.conj().T)/2),0)))
def Hell(Q1,Q2):
    return np.real(np.trace(sqrtm_pos(rho_of_Q(Q1))@sqrtm_pos(rho_of_Q(Q2))))
def detform(Q1,Q2):
    S1=sqrtm_pos(Q1);S2=sqrtm_pos(Q2);C1=sqrtm_pos(np.eye(n)-Q1);C2=sqrtm_pos(np.eye(n)-Q2)
    return np.linalg.det(S1@S2+C1@C2)
eps=1e-3; Q2=Q1+eps*D
print("Hellinger Tr(sqrt rho sqrt sigma) =",Hell(Q1,Q2)," det(S1S2+C1C2)=",np.real(detform(Q1,Q2)))
print("F >= Hell ?",Fmb(Q1,Q2),">=",Hell(Q1,Q2), Fmb(Q1,Q2)>=Hell(Q1,Q2)-1e-14)
# second order coefficients
qv,V=np.linalg.eigh(Q1); Dm=V.conj().T@D@V
N=np.add.outer(qv*(1-qv[:,None]*0),0)  # placeholder
Nm=np.outer(qv,1-qv)+np.outer(1-qv,qv)
Wm=(np.sqrt(np.outer(qv,1-qv))+np.sqrt(np.outer(1-qv,qv)))**2
gB=2*np.sum(np.abs(Dm)**2/Nm); Ps2=0.5*np.sum(np.abs(Dm)**2/Wm)
for eps in [1e-2,3e-3,1e-3]:
    Q2=Q1+eps*D
    print(f" eps={eps:8.1e}  -logF/eps^2={-np.log(Fmb(Q1,Q2))/eps**2:.8f} (gB/8={gB/8:.8f})   -logHell/eps^2={-np.log(Hell(Q1,Q2))/eps**2:.8f} (Psi2={Ps2:.8f})")
# Ostrowski-Taussky check
S1=sqrtm_pos(Q1);C1=sqrtm_pos(np.eye(n)-Q1)
eps=0.05; Q2=Q1+eps*D; S2=sqrtm_pos(Q2);C2=sqrtm_pos(np.eye(n)-Q2)
A=S1@S2+C1@C2; ReA=(A+A.conj().T)/2; Th=(S1-S2)@(S1-S2)+(C1-C2)@(C1-C2)
print("ReA - (1-Theta/2) max:",np.max(np.abs(ReA-(np.eye(n)-Th/2))))
print("det ReA =",np.linalg.det(ReA)," |det A| =",abs(np.linalg.det(A))," OT ok:",np.linalg.det(ReA)<=abs(np.linalg.det(A))+1e-14)
# variational one-particle formula
best=-1e9
for _ in range(4000):
    l=rand_herm(n)*rng.normal()*3
    val=2*np.real(np.trace(D@l))-np.real(np.trace(Q1@l@(np.eye(n)-Q1)@l))
    best=max(best,val)
lstar=V@(2*Dm/Nm)@V.conj().T
val=2*np.real(np.trace(D@lstar))-np.real(np.trace(Q1@lstar@(np.eye(n)-Q1)@lstar))
print("variational: sup(random)=",best," at l*=",val," 2sum|D|^2/N=",gB)

print("\n-- recheck ReA=1-Theta/2 with admissible eps --")
for eps in [0.05,0.02,0.005]:
    Q2=Q1+eps*D; ev=np.linalg.eigvalsh(Q2)
    S2=sqrtm_pos(Q2);C2=sqrtm_pos(np.eye(n)-Q2)
    A=S1@S2+C1@C2; ReA=(A+A.conj().T)/2; Th=(S1-S2)@(S1-S2)+(C1-C2)@(C1-C2)
    print(f" eps={eps}: min/max eig Q2 = {ev.min():.4f},{ev.max():.4f}  ||ReA-(1-Th/2)||={np.max(np.abs(ReA-(np.eye(n)-Th/2))):.2e}  detReA={np.real(np.linalg.det(ReA)):.8f} |detA|={abs(np.linalg.det(A)):.8f}")
