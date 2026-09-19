"""Continuum-type relaxation on the lattice: xi_b = sum_j X_bj c_j Omega over ALL 2n modes of the purified chain,
with the QUASI-FREE modular operator Delta_B = Gamma(M), M = e^{h_B} (+) e^{-h_B'} (h = log((1-Q)/Q) blockwise),
which is the vacuum modular operator's action on the one-excitation space.  Constraints
  Z >= X G X^T (G = P = <c_j O, c_k O>),  1 - Z >= X GD X^T (GD_jk = <c_j O, Gamma(M) c_k O>),  Q_rec_AD = P_A,all X^T.
Compare min of the capped SLD form with the Gaussian-set minimum (X supported on B)."""
import sys, numpy as np, cvxpy as cp, all_channels_sdp as S
from scipy.linalg import expm, logm
LA,LB,LC=map(int,sys.argv[1:4]); KC=float(sys.argv[4]) if len(sys.argv)>4 else 8.0
n=LA+LB+LC; Q=S.corr_sine(n); w,U=np.linalg.eigh(Q); q=np.clip(w,1e-14,1-1e-14)
R=U@np.diag(np.sqrt(q*(1-q)))@U.T; P=np.block([[Q,R],[R,np.eye(n)-Q]])
cs=S.jw_ops(2*n); rhoP=S.gaussian_rho(P); wp,Vp=np.linalg.eigh(rhoP); Om=Vp[:,-1]
B=list(range(LA,LA+LB)); Bc=[j for j in range(2*n) if j not in B]
def hlog(Qs):
    ws,Us=np.linalg.eigh(Qs); ws=np.clip(ws,1e-13,1-1e-13); return Us@np.diag(np.log((1-ws)/ws))@Us.T
logM=np.zeros((2*n,2*n)); logM[np.ix_(B,B)]=hlog(P[np.ix_(B,B)]); logM[np.ix_(Bc,Bc)]=-hlog(P[np.ix_(Bc,Bc)])
K=sum(logM[j,k]*cs[j].T@cs[k] for j in range(2*n) for k in range(2*n)); GM=expm(K)
print("Gamma(M) Omega == Omega ?", np.linalg.norm(GM@Om-Om), " (try also sign flip below)")
xis=[c@Om for c in cs]
GD=np.array([[np.vdot(a,GM@b) for b in xis] for a in xis]).real; G=np.array([[np.vdot(a,b) for b in xis] for a in xis]).real
QBB=Q[np.ix_(B,B)]; print("GD_BB - (1-Q_BB):",np.abs(GD[np.ix_(B,B)]-(np.eye(LB)-QBB)).max(), " G==P:",np.abs(G-P).max())
wik=1.0/(q[:,None]*(1-q[None,:])+q[None,:]*(1-q[:,None])); wik=np.minimum(wik,1+np.cosh(KC))
def solve(cols,G_,GD_):
    m=LB+LC; k=len(cols); X=cp.Variable((m,k)); Z=cp.Variable((m,m),symmetric=True); CA=P[:LA,:][:,cols]
    Qrec=cp.bmat([[Q[:LA,:LA], CA@X.T],[X@CA.T, Z]]); delta=U.T@(Q-Qrec)@U
    obj=0.25*cp.sum(cp.multiply(wik,cp.square(delta)))
    sG=np.linalg.cholesky(G_+1e-12*np.eye(k)); sGD=np.linalg.cholesky(GD_+1e-12*np.eye(k))
    cons=[cp.bmat([[Z, X@sG],[sG.T@X.T, np.eye(k)]])>>0, cp.bmat([[np.eye(m)-Z, X@sGD],[sGD.T@X.T, np.eye(k)]])>>0]
    pr=cp.Problem(cp.Minimize(obj),cons)
    try: pr.solve(solver='CLARABEL')
    except Exception: pr.solve(solver='SCS',eps_abs=1e-9,eps_rel=1e-9,max_iters=200000)
    return pr.value,pr.status,X.value
gF,sF,_=solve(B,G[np.ix_(B,B)],GD[np.ix_(B,B)]); gR,sR,XR=solve(list(range(2*n)),G,GD)
print(f"({LA},{LB},{LC}) kc={KC}: Gaussian-set min g_Q = {gF:.6e} [{sF}] | all-mode relaxed min = {gR:.6e} [{sR}] | weight of X outside B: {np.linalg.norm(XR[:,Bc]):.3e} vs inside {np.linalg.norm(XR[:,B]):.3e}")
