import numpy as np, scipy.linalg as sla, mpmath as mp, sys
sys.path.insert(0,'.')
from defect_matrix import run
from fidelity_mp import fidelity_relent
Dhat, kap = run(1.0, 2.0, 0.5, 30.0, 8.0, 'exact', h=0.01)
q = 1/(1+np.exp(kap)); N=len(kap); I=np.eye(N)
Q = np.diag(q); Qt = Q - Dhat
w = np.linalg.eigvalsh(Qt); print("N=",N," qt range:", w.min(), w.max(), " q range:", q.min(), q.max())
C1 = np.diag(np.sqrt(1-q)); C2 = sla.sqrtm(I-Qt); G1h = np.diag(np.sqrt(q/(1-q))); G2 = Qt @ np.linalg.inv(I-Qt)
T = G1h @ G2 @ G1h
F_np = (np.linalg.det(C1)*np.linalg.det(C2)*np.linalg.det(I+sla.sqrtm(T))).real
S_np = np.trace(Q@(sla.logm(Q)-sla.logm(Qt)) + (I-Q)@(sla.logm(I-Q)-sla.logm(I-Qt))).real
mlogF_mp, S_mp = fidelity_relent(Dhat, kap, dps=30)
print("numpy: -logF =", -np.log(F_np), " S =", S_np)
print("mp   : -logF =", mp.nstr(mlogF_mp, 12), " S =", mp.nstr(S_mp, 12))
