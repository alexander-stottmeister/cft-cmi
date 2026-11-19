"""REF-RP-2: independent refit of the window tail law Phi_sub(kc) = Phi_inf - b kc^-p from the raw rows of
numerics/results_largezeta_certified.txt (section 1), and the arithmetic of card phi-derivative-nondecreasing.
Run: ${PYTHON:-python3} rigor/repair/ref_rp_2_largezeta_refit.py > rigor/repair/ref_rp_2_largezeta_refit.out
Tolerance fixed before the run: |Phi_inf(mine) - card value| <= the card's quoted uncertainty; arithmetic to 1e-3 rel.
Method: scipy least_squares (TRF) on (Phi_inf, b, p) -- not the file's pipeline. The Phi_sub values themselves
are NOT recomputed (needs the flint/D-hat pipeline; not available: no python-flint)."""
import os, re
import numpy as np
from scipy.optimize import least_squares
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = []
sec = 0
for line in open(os.path.join(R, "numerics", "results_largezeta_certified.txt")):
    if line.startswith("## "): sec = int(line[3])
    elif sec == 1 and re.match(r"\s+\d", line):
        z, lam, km, N, eps, kc, ns, ph = line.split(); rows.append((float(z), int(lam), int(km), float(kc), float(ph)))
card = {1.0667: (4.410e-3, 0.020e-3, 120, 45), 2.1333: (1.0797e-2, 0.0050e-2, 120, 45), 4.2667: (2.241e-2, 0.014e-2, 120, 45),
        8.5333: (3.974e-2, 0.072e-2, 120, 45), 17.0667: (6.41e-2, 0.43e-2, 120, 45)}
res = {}
for z, (cv, cu, lam, km) in card.items():
    d = sorted((kc, ph) for (zz, l, k, kc, ph) in rows if zz == z and l == lam and k == km)
    kc = np.array([a for a, _ in d]); ph = np.array([b for _, b in d])
    f = lambda q: (q[0] - q[1] * kc ** (-q[2]) - ph) / ph[-1]
    sol = least_squares(f, x0=(ph[-1] * 1.02, ph[-1], 2.0), method="trf", xtol=1e-15, ftol=1e-15, gtol=1e-15)
    pinf, b, p = sol.x; res[z] = pinf
    print(f"zeta={z:8.4f} box={lam}/{km} n={len(kc)} kc_max={kc[-1]:.2f} Phi_sub(max)={ph[-1]:.6e} -> Phi_inf={pinf:.6e} "
          f"p={p:.3f} maxres={np.abs(sol.fun).max():.1e}; card {cv:.4e}+-{cu:.1e}: {'OK' if abs(pinf-cv)<=cu else 'MISMATCH'}")
print("# phi-derivative-nondecreasing arithmetic")
for z in (4.2667, 8.5333, 17.0667):
    print(f"  Phi/zeta at {z}: card value {card[z][0]/z:.3e}; my refit {res[z]/z:.3e}")
lb = max(ph for (zz, l, k, kc, ph) in rows if zz == 4.2667)
print(f"  max Phi_sub(4.2667) = {lb:.4e}; convexity => Phi(8.5333) >= 2*that = {2*lb:.4e}")
print("  largest extrapolated estimate at 8.5333 in the file's sec. 2 table: read by hand, 4.30574e-2 (Phi_inf(p=1), 180/45)")
print(f"  log bound check: (1/6) log(1+zeta/2) at 17.0667 = {np.log(1+17.0667/2)/6:.4e} >= card 6.41e-2")
