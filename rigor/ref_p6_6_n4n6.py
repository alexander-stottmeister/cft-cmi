#!/usr/bin/env python3
"""rigor/ref_p6_6_n4n6.py -- REF-P6-6 (2026-10-05): N4 (L->R chains), N5 (where (H) fails), N6 (VWZ bounds,
equal-block chains) recomputed from numerics/networks/chains_*.raw and vwz_*.raw with the own parser, fits,
Phi_A interpolation (rigor/ref_p6_6_fitlib.py) and exact corner data (rigor/ref_p6_6_corners.py).
Run (repository root): PYTHONDONTWRITEBYTECODE=1 $PYTHON rigor/ref_p6_6_n4n6.py > rigor/ref_p6_6_n4n6.out"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import ref_p6_6_fitlib as FL
import ref_p6_6_corners as CO

CH = FL.parse('chains_*.raw')

def chains(key):
    """{n: {'L': lengths, prot: (mlogF, D), 'steps': {k: (mlogF, D, I)}}} for one chain set (x merged)."""
    t = {}
    for d in CH:
        if d['set'].rstrip('x') != key: continue
        r = t.setdefault(int(d['n']), {'steps': {}})
        if d['_kind'] == 'CHAIN':
            r[d['prot']] = (float(d['mlogF']), float(d['D'])); r['L'] = tuple(int(x) for x in d['L'].split(','))
        else: r['steps'][int(d['k'])] = (float(d['mlogF']), float(d['D']), float(d['I']))
    return t

def fl(lab, ns, ys):
    (e, s), f, st = FL.summary(ns, ys)
    print('  %-16s n=%s values %s stable %s\n      %s\n      => %s' % (lab, ns, ' '.join('%.6f' % y for y in ys), st,
          FL.ftxt(f), 'none admissible' if e is None else '%.7g +- %.2g' % (e, s)))
    return e, s

dB = lambda P: math.sqrt(2 - 2 * math.exp(-P))      # Bures distance, root fidelity F = e^{-Phi}

def lr_data(base):
    n = len(base)
    cs = CO.corners(base, (1, 2), [(k + 1, (k, k)) for k in range(2, n)])[0]
    p = [0]
    for l in base: p.append(p[-1] + l)
    zI = [float(c[3]) for c in cs]
    zs = [float(c[1] * c[0] * (p[k + 1] - c[0]) / p[k + 1]) for k, c in zip(range(2, n), cs)]
    return zI, zs, [c[4] for c in cs]

def N4():
    print('# N4: L->R chains; Phi_tot, Sstep = sum_k Phi_step (lattice single steps), SA = 2 sum Phi_A(zeta^(I)),'
          '\n#     Samp = 2 sum Phi_A(zeta_step), S2 = 2 f2 sum zeta^2, SW6 = 2 f2 (sum zeta)^2; linear interpolation')
    worst, rows = [], 0
    for key, base in (('n4r2', (8, 4, 2, 1)), ('n5r2', (16, 8, 4, 2, 1)), ('n6r2', (32, 16, 8, 4, 2, 1)),
                      ('n4r3', (27, 9, 3, 1)), ('n5r3', (81, 27, 9, 3, 1))):
        t = chains(key)
        ns = sorted(n for n in t if 'LR' in t[n] and len(t[n]['steps']) == len(base) - 2)
        zI, zs, ys = lr_data(base)
        SA, Samp = 2 * sum(FL.interp(z, 1) for z in zI), 2 * sum(FL.interp(z, 1) for z in zs)
        S2, SW6 = 2 * FL.F2 * sum(z * z for z in zI), 2 * FL.F2 * sum(zI) ** 2
        print('\n%s %s: zeta^(I)=%s zeta_step=%s SA/Samp=%.4f n=%s' % (key, base, ['%.4f' % z for z in zI],
              ['%.4f' % z for z in zs], SA / Samp, ns))
        P = {n: t[n]['LR'][0] for n in ns}; Ss = {n: sum(v[0] for v in t[n]['steps'].values()) for n in ns}
        for lab, f in (('tot/Sstep', lambda n: P[n] / Ss[n]), ('tot/SA', lambda n: P[n] / SA),
                       ('tot/S2', lambda n: P[n] / S2), ('Sstep/Samp', lambda n: Ss[n] / Samp)):
            if len(ns) > 1: fl(lab, ns, [f(n) for n in ns])
            else: print('  %-16s n=%s value %.5f (one resolution, not extrapolated)' % (lab, ns, f(ns[0])))
        print('  tot/SW6 per n: %s' % ' '.join('%d:%.4f' % (n, P[n] / SW6) for n in ns))
    for key in ('n4r2', 'n5r2', 'n6r2', 'n4r3', 'n5r3', 'eq3', 'eq4', 'eq5', 'eq6'):
        for n, r in sorted(chains(key).items()):
            if 'LR' in r and len(r['steps']) >= 2 and len(r['steps']) == len(r['L']) - 2:
                q = dB(r['LR'][0]) / sum(dB(v[0]) for v in r['steps'].values()); worst.append(q); rows += 1
    print('\nchordal (thm:w6chord): d_B(tot)/sum_k d_B(step k) over %d multi-step rows: min %.4f max %.4f' % (
        rows, min(worst), max(worst)))

def N5():
    print('# N5 (a) Ex. 5.6 (1,1,1)m: SW - S2 and SW/(2 Phi_A(2/3)); (b) REF-P6-0 (13,21,9,17)m: U, Ud, 3LR')
    t = chains('sw'); ns = sorted(n for n in t if 'SW' in t[n] and 'S2' in t[n])
    print('  SW - S2 (-log F): %s; (D): %s' % (' '.join('%d:%.1e' % (n, t[n]['SW'][0] - t[n]['S2'][0]) for n in ns),
          ' '.join('%d:%.1e' % (n, t[n]['SW'][1] - t[n]['S2'][1]) for n in ns)))
    for o in (1, 2):
        fl('SW/2PhiA(2/3) %s' % ('lin' if o == 1 else 'quad'), ns, [t[n]['SW'][0] / (2 * FL.interp(2 / 3, o)) for n in ns])
    G = (Fr(13, 10), Fr(21, 10), Fr(9, 10), Fr(17, 10))
    cU = CO.corners(G, *CO.PROT['U'])[0]; cUd = CO.corners(G, *CO.PROT['Ud'])[0]; c3 = CO.corners(G, *CO.PROT['3LR'])[0]
    s1 = 2 * G[3] / (G[2] * (G[2] + G[3])); p3 = G[0] + G[1]; T = sum(G); zn = float(s1 * p3 * (T - p3) / T)
    zU, zUd, z3 = [float(c[3]) for c in cU], float(cUd[0][3]), float(c3[0][3])
    print('  exact: U zeta = %s at x/T = %s; Ud zeta = %.6f at x/T = %.6f; 3LR zeta = %.6f; naive %.6f' % (
        ['%.6f' % z for z in zU], ['%.6f' % float(c[0] / T) for c in cU], zUd, float(cUd[0][0] / T), z3, zn))
    t = chains('ref'); ns = sorted(n for n in t if all(k in t[n] for k in ('U', 'Ud', '3LR')))
    for o in (1, 2):
        P = lambda z: 2 * FL.interp(z, o)
        lab = 'lin' if o == 1 else 'quad'
        fl('Ud/general ' + lab, ns, [t[n]['Ud'][0] / P(zUd) for n in ns])
        fl('Ud/naive ' + lab, ns, [t[n]['Ud'][0] / P(zn) for n in ns])
        fl('3LR/pred ' + lab, ns, [t[n]['3LR'][0] / P(z3) for n in ns])
        fl('U/general ' + lab, ns, [t[n]['U'][0] / (P(zU[0]) + P(zU[1])) for n in ns])
        fl('U/naive ' + lab, ns, [t[n]['U'][0] / (P(zn) + P(zU[1])) for n in ns])

def N6():
    print('# N6 (a) VWZ (5.3)-(5.5): ratios -log F^(i)(lam=0) / b, b1 = I(A:CD|B)/2, b23 = (I(A:C|B)+I(B:D|C)+I(A:D|BC))/2')
    V = FL.parse('vwz_*.raw'); worst, fin = 0.0, {}
    for key in ('e005', 'e010', 'e015', 'e020', 'e030', 'e040'):
        t = {}
        for d in V:
            if d['set'].rstrip('x') != key: continue
            r = t.setdefault(int(d['n']), {'a': int(d['a']), 'b': int(d['b'])})
            if d['_kind'] == 'DATA': r[d['prot']] = float(d['mlogF'])
            else: r['cmi'] = {k: float(v) for k, v in d.items() if k.startswith('I')}
        for n in sorted(t):
            r = t[n]
            if 'cmi' not in r or '3LR' not in r: continue
            c = r['cmi']; eta = r['a'] / (r['a'] + 2 * r['b'])
            b1, b23 = c['IA_CD_B'] / 2, (c['IA_C_B'] + c['IB_D_C'] + c['IA_D_BC']) / 2
            q = (r['1A'] / b1, r['2'] / b23, r['3LR'] / b23); worst = max(worst, max(q))
            fin[key] = (n, q, b23 + math.log((1 - eta) / (1 + eta)) / 6, b1 - math.log(1 / (1 - eta)) / 6,
                        c['IB_D_C'] + c['IA_D_BC'] - c['IAB_D_C'])
    for key, (n, q, d511, d1, ch) in fin.items():
        print('  %s finest n=%d: Phi1/b1=%.4f Phi2/b23=%.4f Phi3/b23=%.4f  b23-(5.11)=%.1e b1-(1/6)log(1/(1-eta))=%.1e'
              ' chain rule %.1e' % (key, n, q[0], q[1], q[2], d511, d1, ch))
    print('  largest ratio over all (eta, n): %.4f (margin %.2f)' % (worst, 1 / worst))
    print('# N6 (b), (c): L->R chains, Phi_tot/(sum_k I_k/2) at the finest n; equal blocks Phi_tot extrapolated')
    for key in ('eq3', 'eq4', 'eq5', 'eq6', 'n4r2', 'n5r2', 'n6r2', 'n4r3', 'n5r3'):
        t = chains(key); ns = sorted(n for n in t if 'LR' in t[n] and len(t[n]['steps']) == len(t[n]['L']) - 2)
        r = t[ns[-1]]; sI = sum(v[2] for v in r['steps'].values())
        print('  %s n=%d: Phi_tot/(sum I_k/2) = %.4f (margin %.1f)' % (key, ns[-1], r['LR'][0] / (sI / 2), sI / 2 / r['LR'][0]))
        if key.startswith('eq'):
            nb = len(r['L']); zs = [(k - 1) * (nb - k + 1) / nb for k in range(2, nb)]
            e, sp = fl('Phi_tot', ns, [t[n]['LR'][0] for n in ns])
            print('      zeta^(I) = %s; Phi_tot/(2 sum Phi_A) lin %.4f quad %.4f' % (['%.4f' % z for z in zs],
                  e / (2 * sum(FL.interp(z, 1) for z in zs)), e / (2 * sum(FL.interp(z, 2) for z in zs))))

if __name__ == '__main__':
    for task in sys.argv[1:] or ['N4']:
        globals()[task]()
