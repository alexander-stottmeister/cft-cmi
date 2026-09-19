"""2-positivity (Kadison-Schwarz) + Tomita relaxation of the all-channel recovered-symbol set, exact on a tiny chain.
For an even UCP beta: A(D)->A(B), put xi_b := beta(c_b) Omega in A(B)Omega (odd part), b in D.  Then
   Q_rec_AD[i,b] = <c_i Omega, xi_b>,  Z := Q_rec_DD >= Gram(xi),  1 - Z >= Gram(S xi),  S = Tomita operator of A(B),
i.e. 1 - Z >= [<xi_a, Delta_B xi_b>].  Minimise the (capped) SLD form g_Q(Q-Q_rec) over (xi, Z): a relaxation of the
all-channel problem.  Compare with (i) the same form over the Gaussian set F, (ii) the all-channel SDP optimum's symbol."""
import sys, itertools, numpy as np, cvxpy as cp, all_channels_sdp as S
LA,LB,LC=map(int,sys.argv[1:4]); KC=float(sys.argv[4]) if len(sys.argv)>4 else 8.0
n=LA+LB+LC; Q=S.corr_sine(n); w,U=np.linalg.eigh(Q); q=np.clip(w,1e-14,1-1e-14)
R=U@np.diag(np.sqrt(q*(1-q)))@U.T; P=np.block([[Q,R],[R,np.eye(n)-Q]])      # pure symbol on 2n modes
cs=S.jw_ops(2*n); rhoP=S.gaussian_rho(P); wp,Vp=np.linalg.eigh(rhoP); Om=Vp[:,-1]
# fermionic algebra A(B): span of all products of c_j, c_j^+ (j in B); odd part
ops=[cs[j] for j in range(LA,LA+LB)]+[cs[j].T for j in range(LA,LA+LB)]
basis=[np.eye(2**(2*n))]
for r in range(1,2*LB+1):
    for comb in itertools.combinations(range(2*LB),r):
        M=np.eye(2**(2*n))
        for k in comb: M=M@ops[k]
        basis.append(M)
Par=S.parity(2*n)
odd=[M for M in basis if np.allclose(Par@M@Par,-M)]
V=np.array([M@Om for M in odd]).T                     # columns span A(B)Omega_odd
Vq,_=np.linalg.qr(V); r=np.linalg.matrix_rank(V,tol=1e-9); Vq=Vq[:,:r]
Sv=np.array([M.T@Om for M in odd]).T                  # S(M Omega) = M^+ Omega  (M real)
# Tomita S on the odd subspace in the basis Vq: S Vq = Vq Ssub  (solve least squares)
coef=np.linalg.lstsq(V,Vq,rcond=None)[0]              # Vq = V coef
SVq=Sv@coef; Ssub=Vq.T@SVq; print("S maps odd A(B)Om into itself?",np.abs(Vq@Ssub-SVq).max(),"dim",r)
GD_full=(SVq.T@SVq)                                   # <S v_a, S v_b> = <v_a, Delta v_b>
G_full=np.eye(r)
vA=np.array([cs[i]@Om for i in range(LA)]).T          # c_i Omega, i in A
CA=vA.T@Vq                                            # <c_i Om, v_k>
wik=1.0/(q[:,None]*(1-q[None,:])+q[None,:]*(1-q[:,None])); wik=np.minimum(wik,1+np.cosh(KC))
def solve(CA_, G_, GD_):
    m=LB+LC; k=G_.shape[0]; X=cp.Variable((m,k)); Z=cp.Variable((m,m),symmetric=True)
    Qrec=cp.bmat([[Q[:LA,:LA], CA_@X.T],[X@CA_.T, Z]]); delta=U.T@(Q-Qrec)@U
    obj=0.25*cp.sum(cp.multiply(wik,cp.square(delta)))
    sG=np.linalg.cholesky(G_+1e-12*np.eye(k)); sGD=np.linalg.cholesky(GD_+1e-12*np.eye(k))
    cons=[cp.bmat([[Z, X@sG],[sG.T@X.T, np.eye(k)]])>>0, cp.bmat([[np.eye(m)-Z, X@sGD],[sGD.T@X.T, np.eye(k)]])>>0]
    pr=cp.Problem(cp.Minimize(obj),cons)
    try: pr.solve(solver='CLARABEL')
    except Exception: pr.solve(solver='SCS',eps_abs=1e-9,eps_rel=1e-9,max_iters=100000)
    return pr.value, pr.status, Qrec.value
QBB=Q[LA:LA+LB,LA:LA+LB]
gF,stF,QrF=solve(Q[:LA,LA:LA+LB], QBB, np.eye(LB)-QBB)          # Gaussian set F (xi_b = sum_j X_bj c_j Om, j in B)
gR,stR,QrR=solve(CA, G_full, GD_full)                           # relaxed set
def gQ(Qr): d=U.T@(Q-Qr)@U; return 0.25*np.sum(wik*d*d)
F,nlF,rho,C,rr=S.solve(LA,LB,LC,parity_cov=True,solver='CLARABEL'); csn=S.jw_ops(n)
Qopt=np.array([[np.trace(rr@csn[i].T@csn[j]).real for j in range(n)] for i in range(n)])
petz,z=S.petz_value(LA,LB,LC)
print(f"({LA},{LB},{LC}) kc={KC}: min g_Q over F = {gF:.6e} [{stF}] | over relaxed set = {gR:.6e} [{stR}] | g_Q at all-channel optimum symbol = {gQ(Qopt):.6e} | exact all-channel opt -logF = {nlF:.6e} | Petz = {petz:.6e}")
