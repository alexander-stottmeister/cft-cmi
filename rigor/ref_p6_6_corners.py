#!/usr/bin/env python3
"""rigor/ref_p6_6_corners.py -- REF-P6-6 (2026-10-03): exact corner data in rational arithmetic, written
independently of numerics/networks/lattice_chain.py (no import of it).  Conventions: rigor/phase6_brief.md
'Setting and conventions': step = (new block, conditioning block A_B); corner p = end of A_B away from A_new;
ordinary Petz sigma = 2 l_new/(l_B (l_B + l_new)); h(x) = p + (x-p)/(1 + e sigma (x-p)) on the side e(x-p) > 0
of A_new (e = +1 right, -1 left), identity on the other side; Phi = k_1 o ... o k_N (k_N applied first).
Masses are read off as EXACT jumps of Phi''/Phi' (S(Phi) = sum_x [Phi''/Phi'](x) delta_x, kappa = -jump/2),
not from the formula of Thm 5.2; the formula sigma_m G_m'(x_m) is evaluated separately and compared.
Run: PYTHONDONTWRITEBYTECODE=1 $PYTHON rigor/ref_p6_6_corners.py > rigor/ref_p6_6_corners.out"""
from fractions import Fraction as Fr
import math

def steps_of(lengths, start, steps):
    p = [Fr(0)]
    for l in lengths: p.append(p[-1] + Fr(l))
    lo, hi, out = p[start[0] - 1], p[start[1]], []
    for (kn, (iB, jB)) in steps:
        k1, k2 = (kn, kn) if isinstance(kn, int) else kn
        nlo, nhi, blo, bhi = p[k1 - 1], p[k2], p[iB - 1], p[jB]
        assert (nlo == hi and bhi == hi and blo >= lo) or (nhi == lo and blo == lo and bhi <= hi)
        e = 1 if nlo == hi else -1
        lB, ln = bhi - blo, nhi - nlo
        out.append((blo if e == 1 else bhi, 2 * ln / (lB * (lB + ln)), e))
        lo, hi = min(lo, nlo), max(hi, nhi)
    assert (lo, hi) == (p[0], p[-1])
    return p, out

def jet(maps, x, side):
    """(Phi, Phi', Phi'') at x from the side `side` (+1 right limit, -1 left limit); maps applied last-first."""
    v, d1, d2 = x, Fr(1), Fr(0)
    for (p, s, e) in reversed(maps):
        u = v - p
        if e * u > 0 or (u == 0 and e * side > 0):
            D = 1 + e * s * u
            h1, h2 = 1 / D ** 2, -2 * e * s / D ** 3
            v, d1, d2 = p + u / D, h1 * d1, h2 * d1 ** 2 + h1 * d2
    return v, d1, d2

def inv(maps, y):
    """G^-1(y) for G = maps[0] o ... o maps[-1]; None if y is outside the range."""
    for (p, s, e) in maps:
        u = y - p
        if e * u > 0:
            if 1 - e * s * u <= 0: return None
            y = p + u / (1 - e * s * u)
    return y

def corners(lengths, start, steps):
    """[(x, kappa_jump, kappa_thm52, zeta^(I), y_I)] and the C^1 defect; swallowed corners reported."""
    p, maps = steps_of(lengths, start, steps)
    T, res, sw = p[-1], [], []
    for m, (pc, s, e) in enumerate(maps):
        later = maps[m + 1:]
        x = inv(later, pc)
        if x is None or not (0 < x < T):
            sw.append(m + 1); continue
        g1 = jet(later, x, +1)[1]                     # G_m'(x_m) (G_m is C^1)
        res.append([x, s * g1])
    pts = {}
    for x, k in res: pts[x] = pts.get(x, 0) + k
    out, c1 = [], 0
    for x, k52 in sorted(pts.items()):
        (_, a1, a2), (_, b1, b2) = jet(maps, x, -1), jet(maps, x, +1)
        c1 = max(c1, abs(a1 - b1))
        kj = -(b2 / b1 - a2 / a1) / 2
        out.append((x, kj, k52, kj * x * (T - x) / T, math.log(x / (T - x))))
    return out, sw, c1, T

PROT = {'1A': ((1, 2), [((3, 4), (2, 2))]), '1B': ((1, 2), [(3, (2, 2)), (4, (2, 3))]),
        '2': ((1, 2), [(3, (2, 2)), (4, (3, 3))]), '3LR': ((2, 3), [(1, (2, 2)), (4, (3, 3))]),
        '3RL': ((2, 3), [(4, (3, 3)), (1, (2, 2))]), 'U': ((2, 3), [(4, (3, 3)), (1, (2, 3))]),
        'Ud': ((2, 3), [(4, (3, 3)), (1, (2, 4))]), 'SW': ((2, 2), [(3, (2, 2)), (1, (2, 2))]),
        'S2': ((2, 3), [(1, (2, 2))])}
lr = lambda n: ((1, 2), [(k + 1, (k, k)) for k in range(2, n)])

def show(tag, L, pr):
    st, sp = PROT[pr] if isinstance(pr, str) else pr
    cs, sw, c1, T = corners(L, st, sp)
    print('%-12s L=%s swallowed=%s C1-defect=%s' % (tag, [str(Fr(l)) for l in L], sw, c1))
    for x, kj, k52, z, y in cs:
        print('   x=%s (x/T=%.6f) kappa_jump=%.9f kappa_thm52=%.9f equal=%s zeta=%.9f y=%.6f' % (
            x, float(x / T), float(kj), float(k52), kj == k52, float(z), y))
    return cs

if __name__ == '__main__':
    print('# REF-P6-6 exact corner data (Fractions); kappa from exact jumps of Phi\'\'/Phi\' vs Thm 5.2 formula')
    print('\n## 1. VWZ symmetric setup (a,b,b,a): closed forms zeta1=a/b, zeta2=a(a+2b)/(2b(a+b)), zeta3=a/b,')
    print('##    e^Delta23 = 1/eta, zeta_eff = 2a/b; eta = a/(a+2b) (VWZ (5.9) with L_A=L_D=a, L_B=L_C=b)')
    for (a, b) in ((2, 19), (2, 9), (6, 17), (1, 2), (6, 7), (4, 3), (4, 9), (1, 1), (12, 7)):
        L, eta = (a, b, b, a), Fr(a, a + 2 * b)
        assert eta == Fr(a * (b + a), (a + b) * (b + b + a))          # (5.9) literally
        c1 = show('1A a,b=%d,%d' % (a, b), L, '1A'); c1b = show('1B', L, '1B')
        c2 = show('2', L, '2'); c3 = show('3LR', L, '3LR'); c3r = show('3RL', L, '3RL')
        p1 = steps_of(L, *PROT['1A'])[1]; p1b = steps_of(L, *PROT['1B'])[1]
        same = all(jet(p1, Fr(k, 7) * 2 * (a + b), 1)[0] == jet(p1b, Fr(k, 7) * 2 * (a + b), 1)[0] for k in range(1, 7))
        z1, z2, z3, ze = c1[0][3], c2[0][3], c2[1][3], c3[0][3]
        ok = (z1 == Fr(a, b) and z2 == Fr(a * (a + 2 * b), 2 * b * (a + b)) and z3 == Fr(a, b) and ze == Fr(2 * a, b)
              and c3r == c3 and [c[:4] for c in c1b] == [c[:4] for c in c1]
              and abs(c2[1][4] - c2[0][4] - math.log(1 / eta)) < 1e-14)
        print('  eta=%s=%.4f: zeta1=%s zeta2=%s zeta3=%s zeta_eff=%s Delta23=%.6f log(1/eta)=%.6f; P21_2=%.6f '
              '2z2z3/z1^2=%.6f; 1B=1A as point maps at 6 points: %s; ALL CLOSED FORMS EXACT: %s' % (
                  eta, float(eta), z1, z2, z3, ze, c2[1][4] - c2[0][4], math.log(1 / eta),
                  float((z2 ** 2 + z3 ** 2) / z1 ** 2), float(2 * z2 * z3 / z1 ** 2), same, ok))
    print('\n## 2. REF-P6-0 geometry (1.3, 2.1, 0.9, 1.7) and Ex. 5.6')
    G = (Fr(13, 10), Fr(21, 10), Fr(9, 10), Fr(17, 10))
    cU, cUd, c3 = show('U', G, 'U'), show('Ud', G, 'Ud'), show('3LR', G, '3LR')
    s1 = Fr(2) * G[3] / (G[2] * (G[2] + G[3])); p3 = G[0] + G[1]; T = sum(G)
    print('  sigma_1 = %.6f; naive (H) zeta at p_3 = sigma_1 beta_I(p_3) = %.6f; U modular separation %.6f' % (
        float(s1), float(s1 * p3 * (T - p3) / T), cU[1][4] - cU[0][4]))
    show('SW (1,1,1)', (1, 1, 1), 'SW'); show('S2 (1,1,1)', (1, 1, 1), 'S2')
    print('\n## 3. L->R chains (def:LR): zeta^(I), zeta_step (frame (p_1, p_{k+2})), 1+z\', lem:ampl and lem:LRdata')
    for base in ((8, 4, 2, 1), (16, 8, 4, 2, 1), (32, 16, 8, 4, 2, 1), (27, 9, 3, 1), (81, 27, 9, 3, 1),
                 (1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1)):
        cs = show('LR%d' % len(base), base, lr(len(base)))
        p = steps_of(base, *lr(len(base)))[0]; T = p[-1]; n = len(base)
        zs, zst, amp, zp, chk = [], [], [], [], True
        for k, (x, kj, _, z, y) in zip(range(2, n), cs):
            f = p[k + 1]; zstep = kj * x * (f - x) / f
            aa, bb, cc = x - p[0], f - x, T - f
            zpr = aa * cc / (bb * (aa + bb + cc))
            chk &= (z / zstep == 1 + zpr) and x == p[k - 1] and kj == Fr(2 * base[k], base[k - 1] * (base[k - 1] + base[k]))
            Lk1 = p[k - 1]; uk, vk, rk = Fr(base[k - 1]) / Lk1, Fr(base[k - 1]) / (T - p[k]), Fr(base[k], base[k - 1])
            chk &= (z * ((1 + uk) * (1 + vk) - 1) == 2 * rk * (1 + vk) / (1 + rk))        # eq:LR1
            zs.append(float(z)); zst.append(float(zstep)); amp.append(float(1 + zpr))
        ys = [c[4] for c in cs]
        print('  zeta^(I)=%s zeta_step=%s 1+z\'=%s Delta_k=%s; lem:ampl, eq:LR1, kappa_k exact: %s' % (
            ['%.4f' % z for z in zs], ['%.4f' % z for z in zst], ['%.4f' % v for v in amp],
            ['%.4f' % (ys[i + 1] - ys[i]) for i in range(len(ys) - 1)], chk))
