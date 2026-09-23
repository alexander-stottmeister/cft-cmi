# Moore-Penrose check of hypothesis (eq:Tcond) of Prop. prop:AC-zero (rigor/optimality_second_order.tex:408-418, verdict box :438-444).
# Written by referee REF-DEP-CFT-A1 (2026-09-23); copied unchanged below this header by AUTH-CFT-A (no paths to localise).
# Run: /usr/bin/python3 tcond_check.py > tcond_check.out   (needs numpy; /usr/bin/python3 has numpy 2.0.2 on this machine)
import numpy as np
def corr_sine(n):
    d = np.arange(n)[:,None]-np.arange(n)[None,:]
    Q = np.where(d==0, 0.5, np.sin(np.pi*d/2)/(np.pi*np.where(d==0,1,d)))
    return Q
for g in [(4,8,2),(4,12,2),(4,16,2)]:
    LA,LB,LC=g; n=sum(g); Q=corr_sine(n)
    a,b,c=slice(0,LA),slice(LA,LA+LB),slice(LA+LB,n)
    QAB,QAC,QBB,QCC=Q[a,b],Q[a,c],Q[b,b],Q[c,c]
    T=np.linalg.pinv(QAB)@QAC
    res=np.linalg.norm(QAB@T-QAC,2)
    m1=np.linalg.eigvalsh(QCC-T.T@QBB@T).min()
    m2=np.linalg.eigvalsh(np.eye(LC)-T.T@(np.eye(LB)-QBB)@T-QCC).min()
    print(g, 'res=%.2e'%res, '||T||=%.4f'%np.linalg.norm(T,2), 'margins %.4f %.4f'%(m1,m2))
