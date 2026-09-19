"""F2: stability of the KKT violation under the weight cap and the UV taper, with the
rank-one gain of the violating direction (this is the table in F2_RESULTS.md T2).
Usage:  f2_capscan.py [L] [cap1,cap2,...] [uv_a1,uv_a2,...]
"""
import sys, numpy as np
import f2_model as M
import f2_kkt_f1 as F1

L = int(sys.argv[1]) if len(sys.argv) > 1 else 128
caps = [float(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '1e4,1e6,1e8,1e10,1e12').split(',')]
uvs = [(float(v), float(v)+0.12) for v in (sys.argv[3] if len(sys.argv) > 3 else '0.30').split(',')]
print("#  L   cap    uv0   theta      lam_min(M)   lam_min/||M||   gQ(noise)/g0    gain/g0      loc(p)")
for uv in uvs:
    for cap in caps:
        S = M.build(L=L, cap=cap, uv=uv); O = F1.objects(S); nD = S['nD']; g0 = O['g0']
        e, V = np.linalg.eigh(O['Ms']); p = V[:, 0]
        nM = np.abs(e).max(); pp = np.outer(p, p.conj())
        tp = float(np.real(p.conj()@O['tau']@p)); y = 1.0 if tp > 0 else 0.0
        Delta = -0.5*(float(np.real(p.conj()@O['Ms']@p)) - y*tp)
        eta = M.noise(S, pp, y*pp); gq = M.gQ(S, eta)
        top = [round(float(i)/nD, 3) for i in np.argsort(-np.abs(p))[:3]]
        print(f"{L:5d} {cap:.0e} {uv[0]:.2f} {O['theta']:.5f} {e.min():+.4e} {e.min()/nM:+.4e} "
              f"{gq/g0:.3e} {Delta**2/gq/g0:.3e} {top}", flush=True)
