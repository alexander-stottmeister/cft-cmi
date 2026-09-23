# Extra geometries for the Moore-Penrose (eq:Tcond) check (AUTH-CFT-A, 2026-09-23): same code as tcond_check.py, geometry list replaced.
# Records that T = Q_AB^+ Q_AC violates (eq:Tcond) at (6,12,3) and (8,16,4); cited for that limitation by the
# results ac-intertwiner-exists-hopping-chain and ac-lower-bound-zero (README.md in this folder).
# Run: /usr/bin/python3 tcond_check_extra.py > tcond_check_extra.out
import numpy as np
def corr_sine(n):
    d = np.arange(n)[:,None]-np.arange(n)[None,:]
    Q = np.where(d==0, 0.5, np.sin(np.pi*d/2)/(np.pi*np.where(d==0,1,d)))
    return Q
for g in [(6,12,3),(8,16,4)]:
    LA,LB,LC=g; n=sum(g); Q=corr_sine(n)
    a,b,c=slice(0,LA),slice(LA,LA+LB),slice(LA+LB,n)
    QAB,QAC,QBB,QCC=Q[a,b],Q[a,c],Q[b,b],Q[c,c]
    T=np.linalg.pinv(QAB)@QAC
    res=np.linalg.norm(QAB@T-QAC,2)
    m1=np.linalg.eigvalsh(QCC-T.T@QBB@T).min()
    m2=np.linalg.eigvalsh(np.eye(LC)-T.T@(np.eye(LB)-QBB)@T-QCC).min()
    print(g, 'res=%.2e'%res, '||T||=%.4f'%np.linalg.norm(T,2), 'margins %.4f %.4f'%(m1,m2))
