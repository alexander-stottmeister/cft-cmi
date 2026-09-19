"""Orchestrator check of S10's claim with the EXACT quasi-free root fidelity (Note 5 Thm 2.1) in high precision.
Model = S10's NS-circle model (s10_theta.setup conventions), grid L. States: Q1 = E_I P E_I (vacuum on I),
Q2 = E_I Wt^* P Wt E_I with Wt = exp(-s Dchi) exp(-eps G_*) (eps=0: compression; eps=eps_*: S10's rotated channel).
Everything after G_* (double, taken as a given anti-hermitian operator) is computed in mpmath at DPS digits:
exact P (geometric sum), expm by scaling-and-squaring Taylor, eigen-decompositions with mp.eighe."""
import sys, numpy as np, mpmath as mp, scipy.linalg as sla
sys.path.insert(0,'.')
from s10_theta import setup
L=int(sys.argv[1]) if len(sys.argv)>1 else 192; DPS=int(sys.argv[2]) if len(sys.argv)>2 else 60
SVALS=[float(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [0.002,0.005]
mp.mp.dps=DPS
S=setup(L=L,a=2.0,Lg=1.0); D=S['D']; u=S['u']; nu2=S['nu2']
# --- rebuild Dchi, I exactly as in s10_nonpert.py (double) ---
th=2*np.pi*np.arange(L)/L; thw=np.where(th>np.pi,th-2*np.pi,th)
n=np.fft.fftfreq(L,d=1.0/L); nu=n+0.5
F=np.fft.fft(np.eye(L),axis=0)/L; Fi=np.fft.ifft(np.eye(L),axis=0)*L
a1,a2=(0.30,0.42); xx=(np.abs(nu)/L-a1)/(a2-a1); s_=np.clip(1-xx,0,1); s_=s_*s_*(3-2*s_)
d=Fi@np.diag(1j*nu*s_)@F; d=0.5*(d-d.conj().T)
thD=2*np.arctan(1.0); thA=-2*np.arctan(2.0)
inD=(thw>0)&(thw<thD); inA=(thw>thA)&(thw<0); inI=inD|inA
chi=np.zeros(L); chi[inD]=np.cos(thw[inD])-1.0
t=thw.copy(); t[t<thA]+=2*np.pi; mm=~inI
chi[mm]=(np.cos(t[mm])-1.0)*np.exp(-3.0*(t[mm]-thD)**2)
X=np.diag(chi); Dc=0.5*(X@d+d@X); Dc=0.5*(Dc-Dc.conj().T)
I=np.where(inI)[0]
# --- G_* by CG (as S10) ---
def Aop(g):
    G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g; v,_=S['riesz'](G); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T); x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=np.real(np.vdot(r,r))
for k in range(70):
    Ap=Aop(p); pAp=np.real(np.vdot(p,Ap)); al=rs/pAp; x=x+al*p; r=r-al*Ap; rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
theta=np.real(np.vdot(b,x))/nu2
G=np.zeros((L,L),complex); G[np.ix_(D,D)]=x; G=0.5*(G-G.conj().T)
v,_=S['riesz'](G); eps_star=-np.real(np.vdot(u,v))/np.real(np.vdot(v,v))   # eps_*/s
print(f"L={L} dps={DPS} theta={theta:.5f} eps_*/s={eps_star:.4f} |u|^2={nu2:.6f}",flush=True)
# --- exact P in mp: P_jk = (1/L) sum_{nu>0} e^{i nu (th_j-th_k)}, nu = n+1/2, n=0..L/2-1 ---
def mpP():
    Pm=mp.matrix(L,L); nus=[mp.mpf(k)+mp.mpf(1)/2 for k in range(L//2)]
    for j in range(L):
        for k in range(L):
            dth=mp.mpf(2)*mp.pi*(j-k)/L
            Pm[j,k]=sum(mp.expj(nv*dth) for nv in nus)/L if j!=k else mp.mpf(L//2)/L
    return Pm
def to_mp(A):
    M=mp.matrix(A.shape[0],A.shape[1])
    for i in range(A.shape[0]):
        for j in range(A.shape[1]): M[i,j]=mp.mpc(A[i,j].real,A[i,j].imag)
    return M
def expm_mp(A):
    nrm=mp.mnorm(A,1); k=max(0,int(mp.ceil(mp.log(nrm,2))))+6; B=A/(2**k)
    E=mp.eye(A.rows); T=mp.eye(A.rows)
    for m in range(1,40):
        T=T*B/m; E=E+T
        if mp.mnorm(T,1)<mp.mpf(10)**(-DPS-5): break
    for _ in range(k): E=E*E
    return E
def sub(M,idx):
    S_=mp.matrix(len(idx),len(idx))
    for a_,i in enumerate(idx):
        for b_,j in enumerate(idx): S_[a_,b_]=M[i,j]
    return S_
def herm(M): return (M+M.H)/2
def neglogF(Q1,Q2,clip=None):
    """Note 5 Thm 2.1 in the STABLE form  F = det(1-Q1)^{1/2} det(1-Q2)^{1/2} prod_i (1+sigma_i(C)),
    C = G1^{1/2} G2^{1/2} = (1-Q1)^{-1/2} Q1^{1/2} Q2^{1/2} (1-Q2)^{-1/2}  (sigma_i^2 = eig(G1^{1/2} G2 G1^{1/2})).
    Only large singular values matter (1+sigma), so an SVD at working precision suffices; eigenvalues clipped
    to [clip, 1-clip] (default 10^-(DPS/2)) -> state perturbation ~ n*clip, negligible."""
    if clip is None: clip=mp.mpf(10)**(-(DPS//2))
    def prep(Q):
        E,Vv=mp.eighe(herm(Q)); E=[min(max(e,clip),1-clip) for e in E]; return E,Vv
    E1,V1=prep(Q1); E2,V2=prep(Q2)
    G1h=V1*mp.diag([mp.sqrt(e/(1-e)) for e in E1])*V1.H
    G2h=V2*mp.diag([mp.sqrt(e/(1-e)) for e in E2])*V2.H
    C=G1h*G2h; sig=mp.svd_c(C,compute_uv=False)
    val=-sum(mp.log(1-e) for e in E1)/2-sum(mp.log(1-e) for e in E2)/2-sum(mp.log(1+sg) for sg in sig)
    return val
def selftest():
    """brute-force many-body check on 3 random modes (Fock dim 8)."""
    import itertools
    rng=np.random.default_rng(0); n=3
    def rand_symbol():
        A=rng.standard_normal((n,n))+1j*rng.standard_normal((n,n)); H=(A+A.conj().T)/2
        w,V=np.linalg.eigh(H); q=1/(1+np.exp(-w)); return V@np.diag(q)@V.conj().T
    def rho_of(Q):
        w,V=np.linalg.eigh(Q); h=V@np.diag(np.log((1-w)/w))@V.conj().T
        # JW ops
        Z=np.diag([1.,-1.]); sm=np.array([[0.,1.],[0.,0.]]); I2=np.eye(2); cs=[]
        for k in range(n):
            mats=[Z]*k+[sm]+[I2]*(n-k-1); M=mats[0]
            for m_ in mats[1:]: M=np.kron(M,m_)
            cs.append(M)
        Hm=sum(h[i,j]*cs[i].conj().T@cs[j] for i in range(n) for j in range(n))
        r=sla.expm(-Hm); return r/np.trace(r)
    Qa,Qb=rand_symbol(),rand_symbol(); ra,rb=rho_of(Qa),rho_of(Qb)
    sa=sla.sqrtm(ra); Fbf=np.trace(sla.sqrtm(sa@rb@sa)).real
    val=neglogF(to_mp(Qa),to_mp(Qb),clip=mp.mpf(10)**(-30))
    print(f"selftest: brute force -logF = {-np.log(Fbf):.12f}   formula = {mp.nstr(val,12)}", flush=True)
selftest()
Pm=mpP(); Q1=sub(Pm,I); Dcm=to_mp(Dc); Gm=to_mp(G)
print("P projector check |P^2-P|:", mp.mnorm(Pm*Pm-Pm,1), flush=True)
for s in SVALS:
    Ws=expm_mp(-mp.mpf(s)*Dcm)
    res={}
    for label,eps in [("compression",0.0),("rotated",eps_star*s)]:
        Wt=Ws if eps==0 else Ws*expm_mp(-mp.mpf(eps)*Gm)
        Q2=sub(Wt.H*Pm*Wt,I)
        res[label]=neglogF(Q1,Q2)
        print(f"  s={s}: {label:12s} exact -logF = {mp.nstr(res[label],12)}   (g_Q-scale: 0.5 s^2|u|^2 = {0.5*s*s*nu2:.6e})",flush=True)
    print(f"  s={s}: RATIO rotated/compression = {mp.nstr(res['rotated']/res['compression'],8)}   (S10 prediction 1-theta = {1-theta:.4f})",flush=True)
