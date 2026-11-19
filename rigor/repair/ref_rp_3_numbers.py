"""REF-RP-3: independent recomputation of the numbers introduced by R4/R5 patches.
Run from the repository root:  ${PYTHON:-python3} rigor/repair/ref_rp_3_numbers.py > rigor/repair/ref_rp_3_numbers.out
Tolerances fixed before the run: TOL_ROUND = half a unit in the last quoted digit; TOL_FIT = 5e-5 absolute for fits."""
import os, re, math
import numpy as np
from scipy.optimize import curve_fit
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def chk(name, val, quoted, ulp):
    ok = abs(val - quoted) <= 0.5 * ulp + 1e-15
    print(f"{name:55s} computed {val:.7g}  quoted {quoted}  |diff| {abs(val-quoted):.2e}  tol {0.5*ulp:.1e}  {'OK' if ok else 'MISMATCH'}")
print("== validation: two-point 1/k extrapolation of an exact law X = 1 - 2/k must return 1")
k1, k2 = 10.0, 20.0; x1, x2 = 1 - 2/k1, 1 - 2/k2
print("   ", (k2*x2 - k1*x1)/(k2 - k1))
print("== (a) fidelity_tables s2: two-point 1/kappa_c extrapolations, kappa_c = log(1/eps)")
rows = {('1e-8',120,45):0.067167, ('1e-11',120,45):0.071785, ('1e-14',120,45):0.074268,
        ('1e-8',240,60):0.067289, ('1e-11',240,60):0.071703, ('1e-14',240,60):0.074177,
        ('1e-11',120,90):0.071731, ('1e-14',120,90):0.074229}
def ex(e1, e2, box):
    a, b = math.log(1/float(e1)), math.log(1/float(e2))
    return (b*rows[(e2,)+box] - a*rows[(e1,)+box])/(b - a)
chk("s2 from kappa 25.3,32.2 rows Lam=120,kmax=45", ex('1e-11','1e-14',(120,45)), 0.0834, 1e-4)
print("    (4 digits: %.5f; patch reason says 0.08337)" % ex('1e-11','1e-14',(120,45)))
chk("s2 from kappa 18.4,25.3 rows Lam=120,kmax=45", ex('1e-8','1e-11',(120,45)), 0.0841, 1e-4)
print("    Lam=240 rows 25.3,32.2: %.5f ; Lam=120,kmax=90: %.5f" % (ex('1e-11','1e-14',(240,60)), ex('1e-11','1e-14',(120,90))))
print("== (b) large-zeta lower bounds: largest kappa_c Phi_sub per zeta, box 120/45, results_largezeta_certified.txt")
best = {}
for line in open(os.path.join(ROOT, 'numerics/results_largezeta_certified.txt')):
    t = line.split()
    if len(t) == 8 and re.match(r'^\d+\.\d+$', t[0]) and t[1] == '120' and t[2] == '45':
        z, kc, ph = float(t[0]), float(t[5]), float(t[7])
        if z not in best or kc > best[z][0]: best[z] = (kc, ph)
for (z, (kc, ph)), (q, ulp) in zip(sorted(best.items()), [(4.381e-3,1e-6),(1.0672e-2,1e-6),(2.1872e-2,1e-6),(3.8259e-2,1e-6),(5.7395e-2,1e-6)]):
    chk(f"Phi_sub(zeta={z}) at kappa_c={kc}", ph, q, ulp)
print("== (c) Petz/best-channel factor")
print("    4/0.62 = %.4f ; 4/0.616 = %.4f ; 4/(0.616+0.003) = %.4f ; 4/(0.616-0.003) = %.4f" % (4/0.62, 4/0.616, 4/0.619, 4/0.613))
print("    4/(1-0.0143) = %.4f (only proved lower bound on theta_fr, per the card)" % (4/(1-0.0143)))
print("== (d) boson: tail fits X = Xinf - b k^-p over kappa_c >= 2.3, own code, rows from boson_recovery.out")
txt = open(os.path.join(ROOT, 'numerics/boson/boson_recovery.out')).read()
blocks = re.split(r' -- (N=\d+ sig=[\d.]+) \(Lam', txt.split('=== 3.')[1].split('=== 4.')[0])
res = {}
for lab, body in zip(blocks[1::2], blocks[2::2]):
    d = np.array([[float(x) for x in m] for m in re.findall(r'kappa_c=\s*([\d.]+)\s+f2=([\d.]+)\s+s2=([\d.]+)', body)])
    k = d[:, 0]; sel = k >= 2.3
    for j, nm in [(1, 'f2'), (2, 's2')]:
        y = d[sel, j]; kk = k[sel]
        pf, _ = curve_fit(lambda x, a, b, p: a - b*x**(-p), kk, y, p0=[y[-1], 0.05, 1.5], maxfev=20000)
        p1 = np.polyfit(1/kk, y, 1)[1]; p2 = np.polyfit(kk**-2.0, y, 1)[1]
        res[(lab, nm)] = (pf[0], pf[2], p1, p2)
        print(f"    {lab:14s} {nm}: free p={pf[2]:.2f} -> {pf[0]:.7f} | p=1 -> {p1:.7f} | p=2 -> {p2:.7f}")
for nm, idx, quoted in [('s2', 0, (0.0810, 0.0824)), ('s2', 2, (0.0838, 0.0842)), ('s2', 3, (0.0782, 0.0785)), ('f2', None, (0.008426, 0.008457))]:
    if idx is None: vals = [res[(l, 'f2')][i] for l in blocks[1::2] for i in (0, 3)]
    else: vals = [res[(l, nm)][idx] for l in blocks[1::2]]
    print(f"    {nm} fit#{idx}: range [{min(vals):.6f}, {max(vals):.6f}] quoted {quoted}")
print("== (e) abstract 0.3-1%: (error of correction) x (correction / Phi), kappa_c = 18.4, Phi(A) from tab:scan")
for z, phi, err in [(1/15, 3.5193e-05, 0.12), (1/120, 5.8155e-07, 0.56)]:
    corr = z**2/(15*math.log(1e8)**2)
    print(f"    zeta={z:.5f}: correction/Phi = {corr/phi:.4f}, x {err} = {err*corr/phi*100:.2f} %")
