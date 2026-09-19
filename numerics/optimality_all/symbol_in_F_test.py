"""Lattice test of Theorem 3.5 (optimality_all_channels.tex): is the recovered symbol of a channel in the
quasi-free feasible set F?  Feasibility SDP: find X (m x LB) with Q_rec_DA = X Q_BA, X Q_BB X^T <= Z <= 1 - X(1-Q_BB)X^T.
Tested for (a) the all-channel optimum, (b) the Petz map, (c) random parity-covariant channels (random Choi)."""
import sys, numpy as np, cvxpy as cp, all_channels_sdp as S
LA,LB,LC=map(int,sys.argv[1:4]); n=LA+LB+LC; Q=S.corr_sine(n); rho=S.gaussian_rho(Q); cs=S.jw_ops(n)
dA,dB,dC=2**LA,2**LB,2**LC; dBC=dB*dC; m=LB+LC
rhoAB=S.ptrace(rho,[dA,dB,dC],[0,1]); rT=rhoAB.reshape(dA,dB,dA,dB).transpose(0,3,2,1).reshape(dA*dB,dA*dB)
def rec_from_choi(C):
    big=np.kron(rT,np.eye(dBC))@np.kron(np.eye(dA),C); return S.ptrace(big,[dA,dB,dBC],[0,2])
def symbol(rr): return np.array([[np.trace(rr@cs[i].T@cs[j]).real for j in range(n)] for i in range(n)])
QBB=Q[LA:LA+LB,LA:LA+LB]; QBA=Q[LA:LA+LB,:LA]
def in_F(Qr, tol=1e-7):
    Z=Qr[LA:,LA:]; X=cp.Variable((m,LB)); s=cp.Variable()
    sG=np.linalg.cholesky(QBB+1e-13*np.eye(LB)); sR=np.linalg.cholesky(np.eye(LB)-QBB+1e-13*np.eye(LB))
    cons=[X@QBA==Qr[LA:,:LA], cp.bmat([[Z+s*np.eye(m), X@sG],[sG.T@X.T, np.eye(LB)]])>>0,
          cp.bmat([[np.eye(m)-Z+s*np.eye(m), X@sR],[sR.T@X.T, np.eye(LB)]])>>0]
    pr=cp.Problem(cp.Minimize(s),cons); pr.solve(solver='CLARABEL'); return pr.value  # <= tol  <=> feasible
F,nlF,rho_,C,rr=S.solve(LA,LB,LC,parity_cov=True,solver='CLARABEL')
print(f"({LA},{LB},{LC}) all-channel optimum: min slack needed s* = {in_F(symbol(rr)):+.3e}  (<=0 means symbol in F)")
# Petz via Gaussian data
import gaussian_opt_tiny as G
Xp,Yp=G.petz_XY(LA,LB,LC); Zp=Xp@QBB@Xp.T+Yp; Qp=G.qrec(Q,Xp,Zp,LA,LB); print(f"Petz symbol: s* = {in_F(Qp):+.3e}")
rng=np.random.default_rng(1); PP=np.kron(S.parity(LB),S.parity(LB+LC))
for trial in range(6):
    # random CPTP Schrodinger channel B -> BC via random Kraus / Choi: C = sum_k vec(K_k)vec(K_k)^T normalised to Tr_BC C = 1
    K=rng.standard_normal((dB*dBC,dB*dBC)); C0=K@K.T; C0=(C0+PP@C0@PP)/2
    # normalise partial trace: C = (1 x T^{-1/2})^T-type fix:  Tr_BC C0 = M (dB x dB) -> C = (M^{-1/2} x 1) C0 (M^{-1/2} x 1)
    M=np.einsum('ikjk->ij',C0.reshape(dB,dBC,dB,dBC)); w,U=np.linalg.eigh(M); Mih=U@np.diag(w**-0.5)@U.T
    C=np.kron(Mih,np.eye(dBC))@C0@np.kron(Mih,np.eye(dBC))
    assert np.abs(np.einsum('ikjk->ij',C.reshape(dB,dBC,dB,dBC))-np.eye(dB)).max()<1e-10
    rr_=rec_from_choi(C); Qr=symbol(rr_)
    # Gaussianity measure of the recovered state
    Gs=S.gaussian_rho(np.clip(Qr,-1,1)) if True else None
    print(f"random channel {trial}: s* = {in_F(Qr):+.3e}   trace distance to Gaussian(same symbol) = {np.abs(np.linalg.eigvalsh(rr_-Gs)).sum():.3f}")

# extreme points: random parity-covariant ISOMETRIC channels E(rho) = W rho W^T, W: H_B -> H_BC
for trial in range(6):
    Pb=np.diag(S.parity(LB)); Pbc=np.diag(S.parity(LB+LC))
    W=np.zeros((dBC,dB))
    for par in [1,-1]:
        rows=np.where(Pbc==par)[0]; cols=np.where(Pb==par)[0]
        A=rng.standard_normal((len(rows),len(cols))); Uq,_=np.linalg.qr(A); W[np.ix_(rows,cols)]=Uq[:,:len(cols)]
    assert np.abs(W.T@W-np.eye(dB)).max()<1e-12
    C=np.zeros((dB*dBC,dB*dBC))
    for i in range(dB):
        for j in range(dB):
            C+=np.kron(np.outer(np.eye(dB)[i],np.eye(dB)[j]), np.outer(W[:,i],W[:,j]))
    rr_=rec_from_choi(C); Qr=symbol(rr_); Gs=S.gaussian_rho(np.clip(Qr,1e-12,1-1e-12))
    print(f"random isometric channel {trial}: s* = {in_F(Qr):+.3e}   trace dist to Gaussian(same symbol) = {np.abs(np.linalg.eigvalsh(rr_-Gs)).sum():.3f}   -logF = {G.neglogF(rho,rr_):.4f}")
