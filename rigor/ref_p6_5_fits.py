#!/usr/bin/env python3
"""ref_p6_5_fits.py -- REF-P6-5 items 3 and 5: my own re-fits of G3's saved rung values (own code, not corner_kernel.hfits).
Reads numerics/networks/kernel_t0.npz, kernel_t0b.npz (T0 rungs), kernel_t0.out (8-decimal print, cross-check),
kernel_decay.out (two-frame table), rigor/g1b_kernel.out (P1, comparison only). Writes rigor/ref_p6_5_fits.out.
Item 3: fits v0 + c h ('lin'), v0 + c h^p ('pow', p in [0.1, 4], nonlinear least squares from 9 starts, scipy),
v0 + c log h ('log', no finite limit) on the 4 finest rungs ('4f') and the 4 next ('4c'); admissible iff max|res| at the
3 finest rungs <= 1e-4 (tolerance of the brief, fixed before the run). Item 5: two-frame arithmetic, sign ratio, decay fits.
Usage: $PYTHON rigor/ref_p6_5_fits.py   (seconds)."""
import os, re, sys
import numpy as np
from scipy.optimize import least_squares
_HERE = os.path.dirname(os.path.abspath(__file__)); _ROOT = os.path.abspath(os.path.join(_HERE, '..'))
NET = os.path.join(_ROOT, 'numerics', 'networks'); F2 = 1/(12*np.pi**2); TOL = 1e-4
out = open(os.path.join(_HERE, 'ref_p6_5_fits.out'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
P('# ref_p6_5_fits.out -- written by rigor/ref_p6_5_fits.py (REF-P6-5); tolerance for admissibility 1e-4 (brief)')

def fit(h, v, model):
    """least squares fit of v(h); returns (v0, p, residual function)"""
    if model == 'lin':
        M = np.vstack([np.ones_like(h), h]).T; c = np.linalg.lstsq(M, v, rcond=None)[0]
        return c[0], 1.0, (lambda x: c[0] + c[1]*x)
    if model == 'log':
        M = np.vstack([np.ones_like(h), np.log(h)]).T; c = np.linalg.lstsq(M, v, rcond=None)[0]
        return np.nan, 0.0, (lambda x: c[0] + c[1]*np.log(x))
    best = None
    for p0 in np.linspace(0.3, 3.0, 9):
        r = least_squares(lambda t: t[0] + t[1]*h**t[2] - v, x0=[v[-1], v[0] - v[-1], p0],
                          bounds=([-np.inf, -np.inf, 0.1], [np.inf, np.inf, 4.0]), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if best is None or r.cost < best.cost:
            best = r
    t = best.x
    return t[0], t[2], (lambda x: t[0] + t[1]*x**t[2])

def fits(hs, v):
    res = []
    for win, sl in (('4f', slice(-4, None)), ('4c', slice(-5, -1))):
        for m in ('lin', 'pow', 'log'):
            v0, p, f = fit(hs[sl], v[sl], m); r3 = np.abs(f(hs[-3:]) - v[-3:]).max()
            res.append((f'{m}-{win}', v0, p, r3, r3 <= TOL))
    return res

def est(res):
    L = [r[1] for r in res if r[4] and np.isfinite(r[1])]
    return (0.5*(max(L) + min(L)), 0.5*(max(L) - min(L))) if L else (np.nan, np.nan)

# ------------------------------------------------------------------ item 3: T0 ladder
z = np.load(os.path.join(NET, 'kernel_t0.npz')); zb = np.load(os.path.join(NET, 'kernel_t0b.npz'))
hs = np.append(z['hA'], zb['h'][-1]); D = z['DA']
G = np.vstack([z['GA'], zb['G'][-1]]); G0 = np.append(z['G0A'], zb['G'][-1][0])
txt = open(os.path.join(NET, 'kernel_t0.out')).read()                 # cross-check npz against the printed values
pr = [float(x) for x in re.findall(r'R_h = G/G0 = \+([0-9.]+)', txt.split('[B]')[0])]
P(f'npz vs kernel_t0.out print (block [A], 50 values): max|diff| = {np.abs(np.array(pr) - (z["GA"]/z["G0A"][:, None]).ravel()).max():.1e}')
P(f'h-ladder: {" ".join(f"{x:.7f}" for x in hs)}; ordering coarse -> fine')
ref = {}
for iD, d in enumerate(D):
    for lab, v in (('R=G/G0', G[:, iD]/G0), ('S=G/f2', G[:, iD]/F2)):
        if d == 0 and lab[0] == 'R':
            continue
        dv = np.diff(v); ploc = np.log(dv[:-1]/dv[1:])/np.log(2)
        r = fits(hs, v); c, u = est(r); ref[(d, lab[0])] = (c, u, v[-1], abs(v[-1] - v[-2]))
        P(f'Delta={d:3.1f} {lab}: finest two {v[-2]:.8f} {v[-1]:.8f} (|diff| {abs(v[-1]-v[-2]):.2e}); p_loc ' +
          ' '.join(f'{x:.3f}' for x in ploc))
        P('    ' + '; '.join(f'{n} {v0:+.7f} p={p:.3f} r3={r3:.1e}{"*" if a else ""}' for n, v0, p, r3, a in r))
        P(f'    -> mine {c:.6f} +- {u:.6f}   (admissible incl. log: {", ".join(n for n, _, _, _, a in r if a)})')
P('Ymax 20 -> 24 at Delta = 8 (R_h), per h: ' + ' '.join(f'{(z["GC"][i, 1]/z["G0C"][i] - z["GA"][i, -1]/z["G0A"][i]):+.2e}'
                                                     for i in range(len(z['hC']))))
hb = z['hB']; vb = z['GB'][:, 2]/z['G0B']; rb = fits(hb, vb)
P("brief's ladder Delta = 6 (4 rungs): " + '; '.join(f'{n} {v0:+.7f} r3={r3:.1e}{"*" if a else ""}' for n, v0, p, r3, a in rb[:3]))

# ------------------------------------------------------------------ item 5: two-frame arithmetic, sign, decay
T = {}
for l in open(os.path.join(NET, 'kernel_decay.out')):
    m = re.match(r'\s*([0-9.]+)\s+\+([0-9.]+) \(([0-9.]+)\)\s+\+([0-9.]+) \(([0-9.]+)\)', l)
    if m and float(m.group(1)) > 0:
        T[float(m.group(1))] = [float(m.group(k)) for k in range(2, 6)]
g1b = {}
for l in open(os.path.join(_HERE, 'g1b_kernel.out')):
    m = re.match(r'\s+([0-9.]+)\s+([0-9.]+)\s+[0-9.e+-]+\s+[0-9.e+-]+\s+[0-9.e+-]+\s+[0-9.e+-]+\s*$', l)
    if m:
        g1b[float(m.group(1))] = float(m.group(2))
# card values, transcribed from kb (corner-kernel-t0-frame, corner-kernel-box-frame, corner-kernel-two-frames)
cT = ['0.89844(11)', '0.74573(14)', '0.60090(16)', '0.47713(16)', '0.29468(15)', '0.17991(13)', '0.10939(10)', '0.066415(74)', '0.024448(37)']
cB = ['0.89835(19)', '0.745633(47)', '0.600737(21)', '0.476965(19)', '0.294525(10)', '0.1797849(55)', '0.1092993(23)', '0.0663499(5)', '0.0244192(3)']
cA = ['0.8984(3)', '0.7457(2)', '0.6008(3)', '0.4770(3)', '0.2946(3)', '0.1798(2)', '0.1093(2)', '0.06638(11)', '0.02443(6)']
def val(s):
    a, b = s[:-1].split('('); n = len(a.split('.')[1]); return float(a), int(b)*10.0**(-n)
P('item 5: Delta | R_T0 card vs out | S_box card vs out | |R_T0-S_box| | my midpoint, |d|/2+max u | card agreed | both inside?'
  ' | R/u T0, box | T0-g1b, box-g1b, agreed-g1b')
Dl = sorted(T); ratios = []
for i, d in enumerate(Dl):
    rt, ut, sb, ub = T[d]; (rT, uT), (sB, uB), (aV, aU) = val(cT[i]), val(cB[i]), val(cA[i])
    mid = 0.5*(rT + sB); unc = 0.5*abs(rT - sB) + max(uT, uB); inside = abs(rT - aV) <= aU and abs(sB - aV) <= aU
    ratios += [rT/uT, sB/uB]
    P(f'{d:3.1f} | {rT:.6f} {rt:.6f} | {sB:.7f} {sb:.7f} | {abs(rT - sB):.2e} | {mid:.6f} {unc:.2e} | {cA[i]} ({aV - mid:+.1e}) |'
      f' {"yes" if inside else "NO"} | {rT/uT:.0f} {sB/uB:.0f} | {rT - g1b[d]:+.1e} {sB - g1b[d]:+.1e} {aV - g1b[d]:+.1e}'
      f' (u_T0 {uT:.1e}, ratio {abs(rT - g1b[d])/uT:.2f})')
P(f'min R/u over both frames and the grid: {min(ratios):.0f}')
x = np.array([d for d in Dl if 3 <= d <= 8]); alphas = []
for lab, col in (('R_T0', 0), ('S_box', 2)):
    for sg in (0, 1, -1):
        y = np.log(np.array([T[d][col] + sg*T[d][col + 1] for d in x]))
        c1 = np.linalg.lstsq(np.vstack([np.ones_like(x), -x]).T, y, rcond=None)[0]
        c2 = np.linalg.lstsq(np.vstack([np.ones_like(x), np.log(x), -x]).T, y, rcond=None)[0]
        r1 = np.abs(y - (c1[0] - c1[1]*x)).max(); r2 = np.abs(y - (c2[0] + c2[1]*np.log(x) - c2[2]*x)).max()
        alphas += [c1[1], c2[2]]
        P(f'  decay {lab} {["R", "R+u", "R-u"][sg]}: exp: alpha={c1[1]:.4f} A={np.exp(c1[0]):.4f} res={r1:.1e};'
          f' D^b exp: alpha={c2[2]:.4f} b={c2[1]:+.3f} res={r2:.1e}')
    y = np.log(np.array([T[d][col] for d in x])); P(f'  local rates {lab}: ' + ' '.join(f'{v:.4f}' for v in -np.diff(y)/np.diff(x)))
yg = np.log(np.array([g1b[d] for d in x])); P('  local rates g1b (comparison): ' + ' '.join(f'{v:.4f}' for v in -np.diff(yg)/np.diff(x)))
P(f'alpha over all 12 fits: {0.5*(max(alphas) + min(alphas)):.4f} +- {0.5*(max(alphas) - min(alphas)):.4f}')
out.close()
