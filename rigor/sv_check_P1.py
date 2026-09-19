import numpy as np, scipy.linalg as sla
rng=np.random.default_rng(7)
n=4
def rand_herm(N):
    X=rng.normal(size=(N,N))+1j*rng.normal(size=(N,N)); return (X+X.conj().T)/2
# rho faithful
h=rand_herm(n); rho=sla.expm(h); rho/=np.trace(rho).real
p,U=np.linalg.eigh(rho); rho=U@np.diag(p)@U.conj().T
# standard form: H = HS(C^n) with <X,Y>=Tr(X^* Y); M = left mult; M' = right mult; Omega=rho^{1/2}
rh=sla.sqrtm(rho); Om=rh
N=n*n
def vec(X): return X.reshape(-1)
def unvec(v): return v.reshape(n,n)
# big self-adjoint operator A on H (N x N complex matrix acting on vec)
Abig=rand_herm(N)
a=unvec(Abig@vec(Om))          # AOmega as a matrix
# ---- curve
def state(s):
    xi=unvec(sla.expm(-1j*s*Abig)@vec(Om))
    return xi@xi.conj().T       # rho_s  since <xi, X xi> = Tr(xi^* X xi)=Tr(X xi xi^*)
def fid(r,s):
    A_=sla.sqrtm(r); T=A_@s@A_
    w=np.linalg.eigvalsh((T+T.conj().T)/2); w=np.clip(w,0,None)
    return np.sum(np.sqrt(w)).real
# ---- drho and finite-dim g_B, g_KM
eps=1e-6
drho=(state(eps)-state(-eps))/(2*eps)
print("Tr drho",np.trace(drho).real, "herm err",np.abs(drho-drho.conj().T).max())
pw,V=np.linalg.eigh(rho); D=V.conj().T@drho@V
gB=2*sum(abs(D[i,j])**2/(pw[i]+pw[j]) for i in range(n) for j in range(n))
def ell(x,y): return 1/x if abs(x-y)<1e-12 else (np.log(x)-np.log(y))/(x-y)
gKM=sum(abs(D[i,j])**2*ell(pw[i],pw[j]) for i in range(n) for j in range(n))
print("g_B(SLD sum) =",gB, "  g_KM =",gKM)
# ---- eta and modular formulas
def Delta(X): return rho@X@np.linalg.inv(rho)
def J(X): return X.conj().T
Sstar=lambda X: rh@ (X.conj().T) @ np.linalg.inv(rh)   # Delta^{1/2} J
eta=1j*(Sstar(a)-a)
# eta should satisfy phi(X)=Tr(drho X)=<eta,X Om>
X0=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
print("eta check", abs(np.trace(drho@X0)-np.trace(eta.conj().T@(X0@Om))))
# g_B = 2 <eta,(1+Delta)^{-1} eta>
Dmat=np.zeros((N,N),dtype=complex)
for k in range(N):
    E=np.zeros(N); E[k]=1; Dmat[:,k]=vec(Delta(unvec(E)))
inv1pD=np.linalg.inv(np.eye(N)+Dmat)
gB2=2*np.vdot(vec(eta),inv1pD@vec(eta)).real
print("g_B (2<eta,(1+D)^-1 eta>) =",gB2)
# g_B = 2||(1-J)(1+Delta)^{-1/2} a||^2
s1pD=sla.sqrtm(np.eye(N)+Dmat); inv_s=np.linalg.inv(s1pD)
chi=unvec(inv_s@vec(a)); w1=chi-J(chi)
gB3=2*np.vdot(vec(w1),vec(w1)).real
print("g_B (2||(1-J)(1+D)^-1/2 a||^2) =",gB3)
# ---- variational: distance to M'_sa Omega  (M'_sa Om = {rho^{1/2} Y, Y=Y^*})
R=rh@a+a.conj().T@rh
Y=np.array([[R[i,j]/(pw[i]+pw[j]) for j in range(n)] for i in range(n)])  # in eigenbasis!
Rb=V.conj().T@R@V; Yb=np.array([[Rb[i,j]/(pw[i]+pw[j]) for j in range(n)] for i in range(n)])
Yv=V@Yb@V.conj().T
G=np.linalg.norm(a-rh@Yv,'fro')**2
print("4*dist(a, M'_sa Om)^2 =",4*G)
# brute-force minimisation check
from scipy.optimize import minimize
def par2herm(x):
    Yr=np.zeros((n,n),dtype=complex); k=0
    for i in range(n): Yr[i,i]=x[k]; k+=1
    for i in range(n):
        for j in range(i+1,n): Yr[i,j]=x[k]+1j*x[k+1]; Yr[j,i]=x[k]-1j*x[k+1]; k+=2
    return Yr
f=lambda x: np.linalg.norm(a-rh@par2herm(x),'fro')**2
res=minimize(f,np.zeros(n*n),method='BFGS',tol=1e-14)
print("4*dist^2 (numerical min) =",4*res.fun)
# ---- variational Alberti: sup_K [phi(K) - Var(K)]
def obj(x):
    K=par2herm(x); phi=np.trace(drho@K).real
    var=np.trace(rho@K@K).real-np.trace(rho@K).real**2
    return -(phi-var)
res2=minimize(obj,np.zeros(n*n),method='BFGS',tol=1e-14)
print("4*sup_K[phi(K)-Var(K)] =",-4*res2.fun)

print("\n--- expansions ---")
def relent(r,s):
    lr=V@np.diag(np.log(np.linalg.eigvalsh(r)))@V.conj().T
    w1,U1=np.linalg.eigh(r); w2,U2=np.linalg.eigh(s)
    return (np.trace(r@(U1@np.diag(np.log(w1))@U1.conj().T - U2@np.diag(np.log(w2))@U2.conj().T))).real
for s in [1e-1,3e-2,1e-2,3e-3]:
    rs=state(s); Fv=fid(rho,rs); mlF=-np.log(Fv); De=relent(rho,rs)
    print(f"s={s:8.1e}  -logF/s^2={mlF/s**2:.6f} (g_B/8={gB/8:.6f})   D/s^2={De/s**2:.6f} (g_KM/2={gKM/2:.6f})")
# Alberti inf formula check: F^2 = inf_x Tr(rho x) Tr(rho_s x^{-1})
print("\n--- Alberti inf and unitary sup, s=0.05 ---")
s=0.05; rs=state(s); Fv=fid(rho,rs)
def albobj(x):
    K=par2herm(x); X=sla.expm(K)
    return np.trace(rho@X).real*np.trace(rs@np.linalg.inv(X)).real
r3=minimize(albobj,np.zeros(n*n),method='Nelder-Mead',options={'maxiter':60000,'maxfev':60000,'xatol':1e-12,'fatol':1e-14})
print("F =",Fv,"  sqrt(inf_x rho(x)rho_s(x^-1)) =",np.sqrt(r3.fun))
# sup over unitaries in M' of |<Om, u' xi_s>|
xis=unvec(sla.expm(-1j*s*Abig)@vec(Om))     # xi_s
def supobj(x):
    u=sla.expm(1j*par2herm(x))       # acts on the RIGHT: (u' X)= X u
    return -abs(np.trace(Om.conj().T@(xis@u)))
r4=minimize(supobj,np.zeros(n*n),method='BFGS',tol=1e-14)
print("F =",Fv,"  sup_{u' in U(M')} |<Om,u' xi_s>| =",-r4.fun)
