#!/usr/bin/env python3
"""ref_p6_5_second.py -- REF-P6-5b (second pass): checks of G3's repaired cards against the regenerated outputs.
Reads numerics/networks/kernel_t0_fits.out, kernel_decay.out (regenerated 2026-10-05), rigor/ref_p6_5_kernel.npz (my
independent continuum R, first pass). Card values transcribed from kb (2026-10-05). Writes rigor/ref_p6_5_second.out.
Usage: $PYTHON rigor/ref_p6_5_second.py (seconds)."""
import os, re
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__)); NET = os.path.join(_HERE, '..', 'numerics', 'networks')
out = open(os.path.join(_HERE, 'ref_p6_5_second.out'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
P('# ref_p6_5_second.out -- rigor/ref_p6_5_second.py (REF-P6-5b)')
Rt = dict(zip([0.5, 1, 1.5, 2, 3, 4, 5, 6, 8], np.load(os.path.join(_HERE, 'ref_p6_5_kernel.npz'))['R'][1:]))
def val(s):
    a, b = s[:-1].split('('); n = len(a.split('.')[1]); return float(a), int(b)*10.0**(-n)
cT = ['0.89844(41)', '0.74573(44)', '0.60090(46)', '0.47713(47)', '0.29468(46)', '0.17991(43)', '0.10939(40)', '0.06642(38)', '0.02445(34)']
cA = ['0.8984(5)', '0.7457(5)', '0.6008(6)', '0.4770(6)', '0.2946(6)', '0.1798(5)', '0.1093(5)', '0.06638(41)', '0.02443(36)']
txt = open(os.path.join(NET, 'kernel_t0_fits.out')).read()
est = re.findall(r'Delta = ([0-9.]+) R_h = G/G0:.*?-> estimate \+([0-9.]+) \+- ([0-9.]+) \(fit half-spread\) \+ 3e-04 \(calibrated overshoot\) = \+- ([0-9.]+)', txt, re.S)
P('(a) T0 card: Delta | estimate, fit spread, total (kernel_t0_fits.out) | card | total = spread + 3e-4? | true R (mine) inside? |T0 - true|/u')
for i, (d, c, u, t) in enumerate(est):
    d, c, u, t = float(d), float(c), float(u), float(t); cv, cu = val(cT[i]); tr = Rt[d]
    P(f'    {d:3.1f} | {c:.6f} {u:.6f} {t:.6f} | {cT[i]} | {"yes" if abs(t - u - 3e-4) < 2e-6 else "NO"} |'
      f' {"yes" if abs(cv - tr) <= cu else "NO"} | {abs(c - tr)/t:.2f} (card values: {abs(cv - tr)/cu:.2f})')
T = {}
for l in open(os.path.join(NET, 'kernel_decay.out')):
    m = re.match(r'\s*([0-9.]+)\s+\+([0-9.]+) \(([0-9.]+)\)\s+\+([0-9.]+) \(([0-9.]+)\).*?\s(\d+), (\d+)\s+\+([0-9.]+) \(([0-9.]+)\)\s*$', l)
    if m and float(m.group(1)) > 0:
        T[float(m.group(1))] = [float(m.group(k)) for k in range(2, 10)]
P('(b) two-frames card: Delta | my midpoint, u = |d|/2 + max u | out agreed | card | unrounded interval inside card interval? | frames, true R inside? | R/u T0')
x = sorted(T); ratios = []
for i, d in enumerate(x):
    rt, ut, sb, ub, q1, q2, av, au = T[d]; mid = 0.5*(rt + sb); un = 0.5*abs(rt - sb) + max(ut, ub); cv, cu = val(cA[i])
    ins = (mid - un >= cv - cu - 1e-12) and (mid + un <= cv + cu + 1e-12); fr = all(abs(v - cv) <= cu for v in (rt, sb, Rt[d]))
    ratios.append(rt/ut)
    P(f'    {d:3.1f} | {mid:.6f} {un:.2e} | {av:.6f} {au:.6f} | {cA[i]} | {"yes" if ins else "no (by %.1e)" % max(cv - cu - (mid - un), mid + un - cv - cu)} |'
      f' {"yes" if fr else "NO"} | {rt/ut:.0f}')
P(f'    min R_T0/u_T0 = {min(ratios):.1f}')
xs = np.array([d for d in x if 3 <= d <= 8]); al = []
for col in (0, 2):
    for sg in (0, 1, -1):
        y = np.log(np.array([T[d][col] + sg*T[d][col + 1] for d in xs]))
        al.append(np.linalg.lstsq(np.vstack([np.ones_like(xs), -xs]).T, y, rcond=None)[0][1])
        al.append(np.linalg.lstsq(np.vstack([np.ones_like(xs), np.log(xs), -xs]).T, y, rcond=None)[0][2])
P(f'(c) alpha over the 12 fits (my lstsq, regenerated R +- u): {0.5*(max(al) + min(al)):.4f} +- {0.5*(max(al) - min(al)):.4f}')
tail = [l.rstrip() for l in open(os.path.join(NET, 'kernel_t0_fits.out')) if not l.startswith('   ') and not l.startswith('#')]
P('(d) kernel_t0_fits.out block headers, last three: ' + ' || '.join(t[:60] for t in tail[-3:]))
kr = open(os.path.join(NET, 'KERNEL_RESULTS.md')).read()
P(f'(e) KERNEL_RESULTS.md: "no shared code" occurrences: {len(re.findall("no shared code", kr))}; lines: {sum(1 for _ in kr.splitlines())}')
out.close()
