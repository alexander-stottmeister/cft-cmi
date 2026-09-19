import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
"""Compare fidelity_hp.Q_box_mp (mp.quad) with compression_box.Q_box (trapezoid), and check the
1/kappa_c law for S against the full 91-mode compression."""
import sys, numpy as np, mpmath as mp
sys.path.insert(0, _os.path.join(_ROOT, "numerics"))
from compression_box import Q_box
from fidelity_hp import Q_box_mp
kap = np.load(_os.path.join(_ROOT, "numerics",
              "Dhat_exact_s0.2_Lam60_k30_g12.npz"), allow_pickle=True)['kappa']
Qd = Q_box(kap, 60.0)
Qm = Q_box_mp(kap, 60.0, 40)
N = len(kap); dif = max(abs(float(Qm[i, j])-Qd[i, j]) for i in range(N) for j in range(N))
print(f"max |Q_box_mp - Q_box(double)| = {dif:.3e}  (max|Q| = {np.abs(Qd).max():.3e})", flush=True)
w = mp.eighe(Qm, eigvals_only=True)
print(f"min eig (mp) = {float(min(w)):.6e}   1-max = {float(1-max(w)):.6e}", flush=True)
print(f"min eig (double) = {np.linalg.eigvalsh(Qd).min():.6e}", flush=True)
print(f"exp(-kappa_max) = {np.exp(-kap.max()):.3e}", flush=True)
print("\n1/kappa_c law for S, Lam=60 kmax=29.6:")
S1, S2 = 4.633291e-06, 4.922154e-06; k1, k2 = 18.4207, 25.3284
C = (S2-S1)/(1/k1-1/k2); Sinf = S2 + C/k2
print(f"  from kc=({k1:.3f},{k2:.3f}): C={C:.4e}  S_inf={Sinf:.5e}")
print(f"  predicted S at kc=29.61: {Sinf - C/29.61:.5e}")
print(f"  full 91-mode compression (results_final.txt, double precision): 5.020734e-06")
print(f"  -> agreement {abs((Sinf-C/29.61)/5.020734e-06-1)*100:.2f}%")
