#!/usr/bin/env python3
"""ref_p6_5_checks.py -- REF-P6-5 checks for items 4, 7, 9 (own code; G3's modules are imported read-only where named).
Usage: $PYTHON rigor/ref_p6_5_checks.py ITEM, ITEM in 4 (regulator/line/box numbers from G3's kernel_box*.npz at full
precision), 7 (composite kernel vs a direct Moebius composition), 9 (G3's MINOR code findings). Writes
rigor/ref_p6_5_checks_<ITEM>.out."""
import os, sys
for _v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '2'
sys.dont_write_bytecode = True
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__)); _ROOT = os.path.abspath(os.path.join(_HERE, '..'))
NET = os.path.join(_ROOT, 'numerics', 'networks'); F2 = 1/(12*np.pi**2)
ITEM = sys.argv[1] if len(sys.argv) > 1 else '4'
out = open(os.path.join(_HERE, f'ref_p6_5_checks_{ITEM}.out'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.write(s + '\n'); out.flush()
P(f'# ref_p6_5_checks_{ITEM}.out -- written by rigor/ref_p6_5_checks.py {ITEM} (REF-P6-5)')

if ITEM == '4':
    za = np.load(os.path.join(NET, 'kernel_box.npz')); zb = np.load(os.path.join(NET, 'kernel_boxb.npz')); zz = float(za['zeta'])**2
    eps = list(za['eps']); P('eps =', eps, '; D =', list(za['D']))
    for z, keys in ((za, ('60_30', '120_30', '120_45', '120_60')), (zb, ('120_75', '120_90', '120_105', '120_120'))):
        for k in keys:
            gw, gl, gb = z[k + '_gw'], z[k + '_gl'], z[k + '_gb']; Rw = gw/gw[:, :1]; Rl = gl/gl[0]; Rb = gb/gb[0]
            Sw = gw/zz/F2
            line = (f'({k}): eps-spread R {np.ptp(Rw, axis=0).max():.1e}, G/f2 {np.ptp(Sw, axis=0).max():.1e};'
                    f' max|R_win(1e-12) - R_line| {np.abs(Rw[1] - Rl).max():.1e}')
            if np.all(np.isfinite(gb)):
                line += ('; max|R_win - R_box| per eps ' + ', '.join(f'{e:.0e}: {np.abs(Rw[i] - Rb).max():.1e}' for i, e in enumerate(eps)))
                line += (f'; max|R_win - R_box| over eps {np.abs(Rw - Rb).max():.1e}, max|G_win - G_box|/G_box(0) '
                         f'{np.abs(gw - gb).max()/gb[0]:.1e}; max|R_line - R_box| {np.abs(Rl - Rb).max():.1e}')
            P(line + f'; 1 - G0/f2 (win) {1 - Sw[1, 0]:.4e}, x kmax^2 = {(1 - Sw[1, 0])*float(z[k + "_kmax"])**2:.3f}')
    S = np.array([zb[k + '_gw'][1]/zz/F2 for k in ('120_75', '120_90', '120_105', '120_120')]).T
    P('S = G/f2 (eps 1e-12) at kappa_max = 75, 90, 105, 120; envelope = max|S(k) - S(120)|, k = 75..105; |S(105) - S(120)|:')
    for i, d in enumerate(za['D']):
        P(f'   Delta {d:3.1f}: ' + ' '.join(f'{x:.9f}' for x in S[i]) + f'  env {np.abs(S[i, :3] - S[i, 3]).max():.1e}'
          f'  two finest {abs(S[i, 2] - S[i, 3]):.1e}')

if ITEM == '7':
    import re, mpmath as mp
    mp.mp.dps = 40; rng = np.random.default_rng(7)
    # (1) K13 of corner_kernel.box_composite against a direct Moebius composition (my code): Phi = id on P1, m1 on P2,
    #     m1 o m2 on P3, m1(z) = z/(1 + s1 z), m2(y) = pp + (y - pp)/(1 + s2 (y - pp)); K = sqrt(m'(y))/(x - m(y)) - 1/(x - y).
    worst = mp.mpf(0)
    for _ in range(400):
        a, L = mp.mpf(1), mp.mpf(2); pp = mp.mpf(rng.uniform(0.05, 1.95)); s1, s2 = mp.mpf(rng.uniform(0, 3)), mp.mpf(rng.uniform(0, 3))
        x = -mp.mpf(rng.uniform(1e-3, 0.999)); y = pp + (L - pp)*mp.mpf(rng.uniform(1e-3, 0.999))
        m = lambda t: (lambda z: z/(1 + s1*z))(pp + (t - pp)/(1 + s2*(t - pp)))
        Kd = mp.sqrt(mp.diff(m, y))/(x - m(y)) - 1/(x - y)
        U, Y = -x, y; V = Y - pp; Nn = s2*(pp + U)*V + s1*U*(Y + s2*pp*V); Kg = Nn/(((U + Y) + Nn)*(U + Y))
        worst = max(worst, abs(Kg/Kd - 1))
    P(f'(1) K13 formula of box_composite vs direct composition m1 o m2 (400 random points, 40 digits): max rel. dev. {float(worst):.1e}')
    # (2) G3's reduction check, recomputed with G3's functions (read-only): sigma2 = 0 and sigma1 = 0
    sys.path.insert(0, NET); import corner_kernel as ck
    a, L = 1.0, 2.0; xi0 = np.log(a/L); sg = 0.1*(a + L)/(a*L); pp = ck.p_of_Delta(a, L, 2.0)
    Dc, _ = ck.box_composite(a, L, sg, 0.0, pp, 60, 30, xi0); De, _ = ck.box_corner(a, L, sg*L, 60, 30, xi0, kind='exact')
    s2 = 0.1*(a + L)/((a + pp)*(L - pp)); Dc2, _ = ck.box_composite(a, L, 0.0, s2, pp, 60, 30, xi0)
    De2, _ = ck.box_corner(a + pp, L - pp, s2*(L - pp), 60, 30, xi0, kind='exact')
    P(f'(2) box_composite(sigma2=0) vs box_corner exact: {np.abs(Dc - De).max()/np.abs(De).max():.1e}; (sigma1=0) at p\'(2): '
      f'{np.abs(Dc2 - De2).max()/np.abs(De2).max():.1e}')
    # (3) the rem/zeta^3 table from G3's outputs
    rows = {}
    for f, e in (('kernel_k4.out', 1e-8), ('kernel_k4b.out', 1e-11)):
        for l in open(os.path.join(NET, f)):
            m = re.search(r'Delta = ([0-9.]+) zeta = ([0-9.]+): Phi_2 = (\S+) Phi_A1 = (\S+) Phi_A2 = (\S+) 2zeta\^2 G = (\S+) rem = (\S+)', l)
            if m:
                rows[(e, float(m.group(1)), float(m.group(2)))] = [float(m.group(k)) for k in range(3, 8)]
    for D in (1.0, 2.0, 4.0, 8.0):
        rz = {e: [rows[(e, D, z)][4]/z**3 for z in (0.05, 0.1, 0.2)] for e in (1e-8, 1e-11)}
        r2 = [rows[(1e-11, D, z)][4]/rows[(1e-11, D, z)][3] for z in (0.05, 0.1, 0.2)]
        v = rz[1e-11]; var = (max(map(abs, v)) - min(map(abs, v)))
        P(f'(3) Delta {D:3.1f}: rem/zeta^3 (1e-11) ' + ' '.join(f'{x:+.6f}' for x in v) + f'; variation {var/max(map(abs, v)):.3f} of max,'
          f' {var/min(map(abs, v)):.3f} of min; |eps 1e-8 - 1e-11| max {max(abs(p - q) for p, q in zip(rz[1e-8], v)):.1e};'
          f' rem/(2z^2G) ' + ' '.join(f'{x:+.4f}' for x in r2) + ' -> /zeta ' + ' '.join(f'{x/z:+.2f}' for x, z in zip(r2, (0.05, 0.1, 0.2))))
    p2, a1, a2 = rows[(1e-11, 8.0, 0.05)][:3]; P(f'(3) clustering Delta 8, zeta 0.05: (Phi_2 - Phi_A1 - Phi_A2)/(Phi_A1 + Phi_A2) = {(p2 - a1 - a2)/(a1 + a2):.5f}')

if ITEM == '9':
    sys.path.insert(0, NET); sys.path.insert(0, os.path.join(_ROOT, 'numerics'))
    import corner_kernel as ck, defect_matrix as dm, compression_box as cb
    a, L = 1.0, 2.0; xi0 = np.log(a/L); r = a/L; z0 = a/(a + L)
    P('(a) beta_I at t = xi - xi0: defect_matrix route (x+a)(L-x)/(a+L) vs cancellation-free a(1+r)e^t/(1+re^t)^2 (my formula):')
    for t in (-60, -45, -37, -30, -20, 20, 30, 37, 45, 60):
        xi = xi0 + t; x = (L*np.exp(xi) - a)/(1 + np.exp(xi)); bn = (x + a)*(L - x)/(a + L); bs = a*(1 + r)*np.exp(t)/(1 + r*np.exp(t))**2
        P(f'    t = {t:+4d}: beta naive {bn:.6e}  stable {bs:.6e}  rel. err {abs(bn - bs)/bs:.1e}')
    for (Lam, km) in ((60, 30), (120, 45)):
        D1, _ = dm.run(a, L, 1.0, Lam, km, 'first', ngl=12); D3, _ = ck.box_corner(a, L, 1.0, Lam, km, xi0)
        P(f'    D level ({Lam},{km}): max|run - stable|/max|D| = {np.abs(D1 - D3).max()/np.abs(D1).max():.1e}')
    P('(b) shifted frame (a\', L\') = (a + p\', L - p\') with the defect_matrix formulas (box_corner stable=False), Lam = 120, kmax = 45:')
    for D in (0.5, 2.0, 8.0):
        pp = ck.p_of_Delta(a, L, D); a2, L2 = a + pp, L - pp
        with np.errstate(all='ignore'):
            Dn, _ = ck.box_corner(a2, L2, z0*(a + L)/a2, 120, 45, xi0, stable=False)
        P(f'    Delta = {D}: NaN entries {int(np.isnan(Dn).sum())} of {Dn.size}')
    P('(c) compression_box.qfi_c2 of the first kernel (stable) where Q_box eigenvalues reach machine precision:')
    for (Lam, km) in ((60, 30), (60, 45), (120, 45), (120, 60)):
        D3, kap = ck.box_corner(a, L, 1.0, Lam, km, xi0); Q = cb.Q_box(kap, Lam, xi0=xi0); w = np.linalg.eigvalsh(Q)
        with np.errstate(all='ignore'):
            c2 = cb.qfi_c2(Q, D3)
        P(f'    ({Lam},{km}): N = {len(kap)}, min eig {w.min():+.2e}, 1 - max eig {1 - w.max():+.2e}, qfi_c2/zeta^2 = {c2/z0**2}')
    D, kap = dm.run(a, L, 0.025, 60, 30, 'exact', ngl=12); Q = cb.Q_box(kap, 60, xi0=xi0)
    m = cb.fid_relent(Q, Q - D)[0]
    P(f'(d) fid_relent, exact kernel s = 0.025, (60,30): -log F = {m:+.6e} (results_batch3.txt:1: -6.54030981e+00; windowed 30-digit'
      f' value 5.679e-07, results_A2.txt:1)')
    P('(e) published values built on defect_matrix.run at Lam = 120, recomputed with the cancellation-free kernel:')
    for km, ref in ((37, 0.0083956), (41, 0.0084045), (45, 0.0084112)):
        D1, kap = dm.run(a, L, 1.0, 120, km, 'first', ngl=12); D3, _ = ck.box_corner(a, L, 1.0, 120, km, xi0); Nl = ck.line_sld(kap)
        f1, f3 = ck.bil(Nl, D1, D1)/z0**2, ck.bil(Nl, D3, D3)/z0**2
        P(f'    line_so.txt (120,{km}) f2_line: published {ref}; defect_matrix.run {f1:.9f}; cancellation-free {f3:.9f} (shift {f3 - f1:+.1e})')
    D1, kap = dm.run(a, L, 1.0, 120, 45, 'first', ngl=12); D3, _ = ck.box_corner(a, L, 1.0, 120, 45, xi0)
    w, U, Nw = ck.sld(cb.Q_box(kap, 120, xi0=xi0)); k = (w > 1e-8) & (w < 1 - 1e-8); Nk = Nw[np.ix_(k, k)]
    fs = [ck.bil(Nk, (U.conj().T @ X @ U)[np.ix_(k, k)], (U.conj().T @ X @ U)[np.ix_(k, k)])/z0**2 for X in (D1, D3)]
    P(f'    results_first_window.txt:1 (120,45), eps 1e-8, f2_sub: published 0.0082392; defect_matrix.run {fs[0]:.9f}; cancellation-free'
      f' {fs[1]:.9f} (shift {fs[1] - fs[0]:+.1e}); {int(k.sum())} modes kept')
out.close()
