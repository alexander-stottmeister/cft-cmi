#!/usr/bin/env python3
"""rigor/ref_p6_6_n2n3.py -- REF-P6-6 (2026-10-05): N2 (Protocol 3 vs Theorem A) and N3 (VWZ ratios) re-fitted from
numerics/networks/vwz_*.raw with the own fits of rigor/ref_p6_6_fitlib.py; Phi_A interpolation tested on the
table nodes.  Run (repository root): PYTHONDONTWRITEBYTECODE=1 $PYTHON rigor/ref_p6_6_n2n3.py > rigor/ref_p6_6_n2n3.out"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import ref_p6_6_fitlib as FL

REC = FL.parse('vwz_*.raw')

def table(key):
    """{n: {prot: (mlogF, D), 'cmi': {...}, 'a','b'}} for a VWZ set (extensions 'x' merged)."""
    t = {}
    for d in REC:
        if d['set'].rstrip('x') != key: continue
        r = t.setdefault(int(d['n']), {'a': int(d['a']), 'b': int(d['b'])})
        if d['_kind'] == 'DATA': r[d['prot']] = (float(d['mlogF']), float(d['D']))
        else: r['cmi'] = {k: float(v) for k, v in d.items() if k.startswith('I')}
    return t

def line(lab, ns, ys):
    (e, s), f, st = FL.summary(ns, ys)
    print('  %-28s n=%s\n    values %s\n    stable(two finest) %s | %s\n    => %s' % (
        lab, ns, ' '.join('%.9f' % y for y in ys), st, FL.ftxt(f),
        'none admissible' if e is None else '%.6f +- %.1e' % (e, s)))
    return e, s

def interp_tests():
    print('# Phi_A table (per chirality): leave-one-out on interior nodes (rel. error of the prediction)')
    for k in range(1, len(FL.TAB) - 1):
        z, v = FL.TAB[k]
        sub = FL.TAB[:k] + FL.TAB[k + 1:]
        l1, l2 = FL.interp(z, 1, sub) / v - 1, FL.interp(z, 2, sub) / v - 1
        print('  node zeta=%.4f: linear %+.4f%%  quadratic %+.4f%%' % (z, 100 * l1, 100 * l2))
    print('# linear vs quadratic (full table) at the zeta values of N2/N3/N5: (quad/lin - 1)')
    for z in (0.10526, 0.2, 0.2105, 0.4444, 0.5, 2 / 3, 1.0, 1.2351, 1.3333, 1.454, 1.7143, 2.1407, 2.6667, 2.6772):
        print('  zeta=%.4f lin=%.6e quad=%.6e diff %+.3f%%' % (z, FL.interp(z, 1), FL.interp(z, 2),
                                                            100 * (FL.interp(z, 2) / FL.interp(z, 1) - 1)))

def stencils():
    print('# stencil variants at the N2 zeta values (per chirality Phi_A; rel. to the 3-node quadratic of interp)')
    T = FL.TAB
    for z in (4 / 9, 1.0, 12 / 7, 2 / 3, 1.235146, 2.677249, 1.453976):
        q = FL.interp(z, 2)
        k = max(i for i in range(len(T)) if T[i][0] <= z)
        for nodes in ((k - 1, k, k + 1), (k, k + 1, k + 2), (k - 1, k, k + 1, k + 2)):
            sub = [T[i] for i in nodes if 0 <= i < len(T)]
            xs = [math.log(a) for a, _ in sub]; ys = [math.log(b) for _, b in sub]; x = math.log(z)
            v = math.exp(sum(ys[i] * math.prod((x - xs[j]) / (xs[i] - xs[j]) for j in range(len(xs)) if j != i)
                             for i in range(len(xs))))
            print('  zeta=%.4f nodes %s: %.6e (%+.3f%% vs quad)' % (z, [round(T[i][0], 4) for i in nodes
                  if 0 <= i < len(T)], v, 100 * (v / q - 1)))

def N2():
    print('\n# N2: zeta_eff = (sigma1+sigma2) beta_I(p3), sigma = 2a/(b(a+b)) each, beta_I(p3) = (a+b)/2 (exact)')
    for key, mk in (('e010', 'm010'), ('e020', 'm020'), ('e030', 'm030')):
        t, tm = table(key), table(mk)
        ns = sorted(n for n in t if '3LR' in t[n]); nm = sorted(n for n in tm if '1A' in tm[n])
        m0 = min(ns) // (2 * (t[ns[0]]['a'] + t[ns[0]]['b']) // ns[0]) if False else None
        a, b = t[ns[0]]['a'], t[ns[0]]['b']; g = math.gcd(a, b); a0, b0 = a // g, b // g
        ze = Fr(4 * a0, b0 * (a0 + b0)) * Fr(a0 + b0, 2)
        am, bm = tm[nm[0]]['a'], tm[nm[0]]['b']; gm = math.gcd(am, bm)
        print('\n%s (a,b)=(%d,%d) eta=%s zeta_eff=%s=%.6f; matched %s (a\',b\')=(%d,%d): a\'/b\'=%s' % (
            key, a0, b0, Fr(a0, a0 + 2 * b0), ze, float(ze), mk, am // gm, bm // gm, Fr(am, bm)))
        e3, s3 = line('Phi3 (lattice -log F)', ns, [t[n]['3LR'][0] for n in ns])
        e1, s1 = line('Phi1A matched', nm, [tm[n]['1A'][0] for n in nm])
        pl, pq = 2 * FL.interp(float(ze), 1), 2 * FL.interp(float(ze), 2)
        print('  Q2 = %.5f +- %.1e (rel. spreads added) | Q1 lin = %.5f, Q1 quad = %.5f (+- %.1e fit) |'
              ' 2Phi_A lin %.6e quad %.6e' % (e3 / e1, e3 / e1 * (s3 / e3 + s1 / e1), e3 / pl, e3 / pq, s3 / pl, pl, pq))
        line('Q1 lin as ratio, own fit', ns, [t[n]['3LR'][0] / pl for n in ns])

def S_closed(D):
    """Ghat(D)/Ghat(0) = cosh(D/2) - sinh^2(D/2) log coth(D/4) (card corner-kernel-closed-form, thm:T4(cf), proved)."""
    return math.cosh(D / 2) - math.sinh(D / 2) ** 2 * math.log(1 / math.tanh(D / 4))

def N3():
    print('\n# N3: R31 = Phi3/Phi1A, R21 = Phi2/Phi1A (lattice -log F), exact corner data, X = (R21-P21)/(2 z2 z3/z1^2)')
    rows, ordF, ordD, XS = 0, True, True, []
    for key in ('e005', 'e010', 'e015', 'e020', 'e030', 'e040'):
        t = table(key)
        ns = sorted(n for n in t if all(k in t[n] for k in ('1A', '2', '3LR')))
        for n in ns:
            rows += 1
            ordF &= t[n]['1A'][0] < t[n]['2'][0] < t[n]['3LR'][0]; ordD &= t[n]['1A'][1] < t[n]['2'][1] < t[n]['3LR'][1]
        a, b = t[ns[0]]['a'], t[ns[0]]['b']; g = math.gcd(a, b); a, b = a // g, b // g
        eta = Fr(a, a + 2 * b); z1, z2, z3, ze = Fr(a, b), Fr(a * (a + 2 * b), 2 * b * (a + b)), Fr(a, b), Fr(2 * a, b)
        P21 = (z2 ** 2 + z3 ** 2) / z1 ** 2; cw = 2 * z2 * z3 / z1 ** 2; D23 = math.log(1 / eta)
        print('\n%s eta=%s n=%s z1=%.6f z2=%.6f zeff=%.6f Delta23=%.6f P21_2=%.6f 2z2z3/z1^2=%.6f' % (
            key, eta, ns, z1, z2, ze, D23, P21, cw))
        e31, s31 = line('R31', ns, [t[n]['3LR'][0] / t[n]['1A'][0] for n in ns])
        e21, s21 = line('R21', ns, [t[n]['2'][0] / t[n]['1A'][0] for n in ns])
        line('D2/D1', ns, [t[n]['2'][1] / t[n]['1A'][1] for n in ns])
        line('D3/D1', ns, [t[n]['3LR'][1] / t[n]['1A'][1] for n in ns])
        p = {o: [FL.interp(float(z), o) for z in (z1, z2, z3, ze)] for o in (1, 2)}
        P31l, P31q = p[1][3] / p[1][0], p[2][3] / p[2][0]
        X = (e21 - float(P21)) / float(cw); sX = s21 / float(cw)
        XA = {o: (e21 * p[o][0] - p[o][1] - p[o][2]) / (2 * FL.F2 * float(z2 * z3)) for o in (1, 2)}
        S = S_closed(D23)
        print('  P31 lin %.4f quad %.4f; R31/P31 lin %.4f quad %.4f (+- %.1e) | X = %.4f +- %.4f, X_A lin %.4f quad'
              ' %.4f | S_closed(Delta23) = %.5f, X/S = %.4f +- %.4f, (1-X/S)/z1 = %.3f, (X-S)/sX = %.1f' % (
                  P31l, P31q, e31 / P31l, e31 / P31q, s31 / P31l, X, sX, XA[1], XA[2], S, X / S, sX / S,
                  (1 - X / S) / float(z1), (X - S) / sX if sX else float('nan')))
        if key == 'e020':
            small = [n for n in ns if n <= 24]
            print('  VWZ sizes (L_A <= 4, L_B <= 8, n = %s): R21 = %s, R31 = %s' % (small, [
                round(t[n]['2'][0] / t[n]['1A'][0], 4) for n in small], [round(t[n]['3LR'][0] / t[n]['1A'][0], 4) for n in small]))
        XS.append((float(z1), X / S))
    print('\nOrdering over %d (eta, n) rows: Phi1 < Phi2 < Phi3: %s; D1 < D2 < D3: %s' % (rows, ordF, ordD))
    import numpy as np
    sm = sorted(XS)[:3]
    c = np.polyfit([z for z, _ in sm], [v for _, v in sm], 1)
    print('linear fit X/S = A + B zeta_1 on the 3 smallest zeta_1: A = %.4f, B = %.4f' % (c[1], c[0]))

if __name__ == '__main__':
    interp_tests()
    stencils()
    N2()
    N3()
