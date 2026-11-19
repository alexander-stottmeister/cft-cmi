"""C6 council check: robustness of the bosonic extrapolations f2 = 0.00844(2), s2 = 0.083(2)
(paper2/sec_boson.tex eq:bosonvals) from the ONE printed window table (paper2/sec_boson.tex:76-83).
Tolerance fixed before the run: the quoted value is 'robust' if every fit below lands inside the quoted
interval (f2 in [0.00842, 0.00846], s2 in [0.081, 0.085]).  Data are the printed table (one basis only;
the paper used three bases, N = 60, 120, sigma = 1.6, 2.26, not printed), so this is a consistency check of the
printed numbers, not a recomputation of the boson model.  Run: ${PYTHON:-python3} rigor/council/c6_boson_extrap.py"""
import numpy as np
from scipy.optimize import curve_fit
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Part A: the printed table, columns labelled as in the paper (kappa_c headers 3.04, 3.77 are suspect)
PRINTED = (np.array([1.58, 2.31, 3.04, 3.77, 4.51, 5.24]),
           np.array([0.007915, 0.008226, 0.008351, 0.008383, 0.008391, 0.008405]),
           np.array([0.059029, 0.067017, 0.072487, 0.074552, 0.075097, 0.076322]))
# Part B: the three bases of numerics/boson/boson_recovery.out, section 3 (all 11 windows each)
txt = open(os.path.join(ROOT, 'numerics/boson/boson_recovery.out')).read().split('=== 3.')[1]
BLOCKS = []
for blk in txt.split(' -- ')[1:4]:
    head = blk.splitlines()[0]
    rows = re.findall(r'kappa_c=\s*([\d.]+)\s+f2=([\d.]+)\s+s2=([\d.]+)', blk)
    a = np.array(rows, dtype=float)
    BLOCKS.append((head.strip(), a[:, 0], a[:, 1], a[:, 2]))
TOL = {'f2': (0.00842, 0.00846), 's2': (0.081, 0.085)}
def free(k, X, b, p): return X - b * k**(-p)
def fixp(p):
    return lambda k, X, b: X - b * k**(-p)
def two(p):
    return lambda k, X, b, d: X - b * k**(-p) - d * k**(-p - 1)
def analyse(kc, f2, s2):
    sel = kc >= 2.3
    for name, y, pexp in     (('f2', f2, 2.0), ('s2', s2, 1.0)):
        print(f'--- {name}: raw value at kappa_c = 5.24: {y[-1]:.6f}; quoted interval {TOL[name]}')
        rows = []
        try:
            P, _ = curve_fit(free, kc[sel], y[sel], p0=[y[-1], 0.01, pexp], maxfev=20000)
            rows.append(('free p (5 pts)', P[0], 'p=%.3f' % P[2], np.max(np.abs(free(kc[sel], *P) - y[sel]))))
        except Exception as e:
            rows.append(('free p', float('nan'), str(e), float('nan')))
        for p in (pexp, pexp + 0.5, pexp + 1.0):
            P, _ = curve_fit(fixp(p), kc[sel], y[sel], p0=[y[-1], 0.01])
            rows.append((f'fixed p={p}', P[0], '', np.max(np.abs(fixp(p)(kc[sel], *P) - y[sel]))))
            P, _ = curve_fit(fixp(p), kc[-3:], y[-3:], p0=[y[-1], 0.01])
            rows.append((f'fixed p={p}, 3 finest', P[0], '', np.max(np.abs(fixp(p)(kc[-3:], *P) - y[-3:]))))
        P, _ = curve_fit(two(pexp), kc[sel], y[sel], p0=[y[-1], 0.01, 0.0])
        rows.append((f'p={pexp} + next order', P[0], '', np.max(np.abs(two(pexp)(kc[sel], *P) - y[sel]))))
        lo, hi = TOL[name]
        for lab, X, extra, res in rows:
            print(f'{lab:28s} X_inf = {X:.6f} {extra:10s} max resid = {res:.2e}  inside quoted: {lo <= X <= hi}')
print('===== PART A: printed table (paper2/sec_boson.tex:76-83)')
analyse(*PRINTED)
for head, kc, f2, s2 in BLOCKS:
    print('===== PART B: boson_recovery.out basis', head)
    analyse(kc, f2, s2)
