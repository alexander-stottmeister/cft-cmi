import numpy as np, scipy.linalg as sla, mpmath as mp, sys, time
sys.path.insert(0,'.')
from defect_matrix import run
from fidelity_mp import fidelity_relent
for kmax, dps in [(15,30),(20,30),(24,30),(30,30),(30,60)]:
    Dhat, kap = run(1.0, 2.0, 0.2, 40.0, float(kmax), 'exact', h=0.008)
    q = 1/(1+np.exp(kap)); N=len(kap); I=np.eye(N); Q=np.diag(q); Qt=Q-Dhat
    t0=time.time(); mF, S = fidelity_relent(Dhat, kap, dps=dps); t1=time.time()-t0
    if kmax <= 20:
        C1=np.diag(np.sqrt(1-q)); C2=sla.sqrtm(I-Qt); G1h=np.diag(np.sqrt(q/(1-q))); G2=Qt@np.linalg.inv(I-Qt); T=G1h@G2@G1h
        Fnp=(np.linalg.det(C1)*np.linalg.det(C2)*np.linalg.det(I+sla.sqrtm(T))).real; ref=f"numpy -logF={-np.log(Fnp):.6e}"
    else: ref=""
    print(f"kmax={kmax} N={N} dps={dps} ({t1:.0f}s): mp -logF={mp.nstr(mF,8)} S={mp.nstr(S,8)} {ref}", flush=True)
