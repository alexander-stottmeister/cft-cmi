"""Is the all-channel optimal recovered state Gaussian? Compare rho_rec with the Gaussian state of the same symbol."""
import sys, numpy as np, all_channels_sdp as S
from gaussian_opt_tiny import neglogF
LA,LB,LC=map(int,sys.argv[1:4]); n=LA+LB+LC
F,nlF,rho,C,rr=S.solve(LA,LB,LC,parity_cov=True,solver='CLARABEL')
rr=(rr+rr.T)/2; cs=S.jw_ops(n)
Qr=np.array([[np.trace(rr@cs[i].T@cs[j]).real for j in range(n)] for i in range(n)])
Q=S.corr_sine(n)
print("opt -logF",nlF," trace rr",np.trace(rr)," min eig rr",np.linalg.eigvalsh(rr).min())
print("symbol defect |Q_rec-Q| max:",np.abs(Qr-Q).max()," blocks: AA",np.abs(Qr-Q)[:LA,:LA].max()," AD",np.abs(Qr-Q)[:LA,LA:].max()," DD",np.abs(Qr-Q)[LA:,LA:].max())
G=S.gaussian_rho(Qr)
print("||rr - Gauss(Q_rec)||_1 =",np.abs(np.linalg.eigvalsh(rr-G)).sum(),"   -logF(rho,Gauss(Q_rec)) =",neglogF(rho,G))
N=sum(c.T@c for c in cs); print("[rr,N] norm",np.abs(rr@N-N@rr).max())
# pairing <c_i c_j> (should vanish for gauge-covariant)
print("max |<c_i c_j>|",max(abs(np.trace(rr@cs[i]@cs[j])) for i in range(n) for j in range(n)))
# Wick test: 4-point <c_i^+ c_j^+ c_k c_l> vs Gaussian value
i,j,k,l=0,1,1,0
four=np.trace(rr@cs[i].T@cs[j].T@cs[k]@cs[l]).real; wick=Qr[i,l]*Qr[j,k]-Qr[i,k]*Qr[j,l]
print("4-pt",four," Wick",wick," diff",four-wick)
np.savez(f"allch_{LA}_{LB}_{LC}.npz",C=C,rr=rr,rho=rho,F=F)
