#!/usr/bin/env python3
"""rigor/ref_p6_6_fitlib.py -- REF-P6-6 (2026-10-05): own parser of G2's raw files, own convergence fits and own
Phi_A interpolation, written without importing numerics/networks/lattice_chain.py.  Library for
rigor/ref_p6_6_n2n3.py and rigor/ref_p6_6_n4n6.py.  Fit rule (brief REF-P6-6 item 4, AGENTS.md sec. 5): the NFIT = 4
finest resolutions; y normalised by its value at the finest one; models A: a + b/L, B: a + b/L + c/L^2, C: a + b L^-p
(p free in [0.05, 6], profile least squares), Dlog: a + b log L (no limit); admissible iff max |residual| at the
three finest <= TOL = 1e-4; estimate = mean of admissible extrapolating fits, uncertainty = their spread; 0-dof fits
are flagged; 'stable' = digits common to the two finest resolutions."""
import glob, math, os
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
NET = os.path.join(ROOT, 'numerics', 'networks')
TOL, NFIT = 1e-4, 4

def parse(pattern):
    """list of dicts, one per line starting with DATA/CMI/CHAIN/STEP (values as strings)."""
    out = []
    for fn in sorted(glob.glob(os.path.join(NET, pattern))):
        for line in open(fn):
            w = line.split()
            if w and w[0] in ('DATA', 'CMI', 'CHAIN', 'STEP'):
                d = {k: v for k, v in (x.split('=', 1) for x in w[1:])}
                d['_kind'], d['_file'] = w[0], os.path.basename(fn)
                out.append(d)
    return out

def _ls(cols, y):
    A = np.array(cols, dtype=float).T
    c = np.linalg.lstsq(A, y, rcond=None)[0]
    return c, A @ c - y

def fit(Ls, ys):
    """{model: (y_inf, max|res| at 3 finest, admissible, dof, note)} on the NFIT finest, y normalised."""
    o = sorted(range(len(Ls)), key=lambda i: Ls[i])[-NFIT:]
    L = np.array([float(Ls[i]) for i in o]); y0 = float(ys[o[-1]])
    y = np.array([float(ys[i]) for i in o]) / y0
    one, res = np.ones_like(L), {}
    def put(name, yinf, r, npar, note=''):
        r3 = float(np.max(np.abs(r[-3:])))
        res[name] = (None if yinf is None else yinf * y0, r3, r3 <= TOL, len(L) - npar, note)
    if len(L) >= 2:
        c, r = _ls([one, 1 / L], y); put('A:1/L', c[0], r, 2)
        c, r = _ls([one, np.log(L)], y); put('Dlog', None, r, 2)
    if len(L) >= 3:
        c, r = _ls([one, 1 / L, 1 / L ** 2], y); put('B:1/L+1/L2', c[0], r, 3)
        ssr = lambda p: float(np.sum(_ls([one, L ** -p], y)[1] ** 2))
        grid = np.linspace(0.05, 6, 120); p0 = grid[int(np.argmin([ssr(p) for p in grid]))]
        m = minimize_scalar(ssr, bounds=(max(0.05, p0 - 0.05), min(6, p0 + 0.05)), method='bounded')
        c, r = _ls([one, L ** -m.x], y); put('C:h^p', c[0], r, 3, 'p=%.3f' % m.x)
    return res

def summary(Ls, ys):
    f = fit(Ls, ys)
    adm = [v[0] for v in f.values() if v[2] and v[0] is not None]
    est = (sum(adm) / len(adm), max(adm) - min(adm)) if adm else (None, None)
    o = sorted(range(len(Ls)), key=lambda i: Ls[i])
    return est, f, stable(ys[o[-1]], ys[o[-2]]) if len(Ls) > 1 else '--'

def stable(a, b):
    sa, sb = '%.10f' % a, '%.10f' % b
    k = 0
    while k < len(sa) and sa[k] == sb[k]: k += 1
    return sa[:k] if any(ch in '123456789' for ch in sa[:k]) else 'none'

def ftxt(f):
    return '; '.join('%s %s r=%.1e %s dof=%d %s' % (k, '%.6g' % v[0] if v[0] is not None else '--', v[1],
                     'ADM' if v[2] else 'rej', v[3], v[4]) for k, v in f.items())

# Phi_A per chirality: paper1/fidelity_tables.tex tab:scan col. A (l. 34-40) and
# numerics/fidelity_table_largezeta.tex 'best Phi' (zeta = s/3); values typed here from those files.
TAB = [(0.0083, 5.8155e-07), (0.0167, 2.3073e-06), (0.0333, 9.0814e-06), (0.0667, 3.5193e-05), (0.1333, 1.3243e-04),
       (0.2667, 4.7267e-04), (0.5333, 1.5458e-03), (3.2 / 3, 4.410e-03), (6.4 / 3, 1.0797e-02), (12.8 / 3, 2.241e-02),
       (25.6 / 3, 3.974e-02), (51.2 / 3, 6.41e-02)]
F2 = 1 / (12 * math.pi ** 2)

def interp(z, order, tab=TAB):
    """log-log Lagrange interpolation of degree `order` (1 or 2) on the nodes bracketing/nearest to z."""
    xs = [math.log(a) for a, _ in tab]; ys = [math.log(b) for _, b in tab]; x = math.log(z)
    if order == 1:
        k = max(0, min(len(xs) - 2, max(i for i in range(len(xs)) if xs[i] <= x) if x >= xs[0] else 0))
        idx = [k, k + 1]
    else:
        k = min(range(len(xs)), key=lambda i: abs(xs[i] - x)); k = min(max(k - 1, 0), len(xs) - 3)
        idx = [k, k + 1, k + 2]
    v = sum(ys[i] * math.prod((x - xs[j]) / (xs[i] - xs[j]) for j in idx if j != i) for i in idx)
    return math.exp(v)
