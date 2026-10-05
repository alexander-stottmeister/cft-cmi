#!/usr/bin/env python3
"""ref_p6_4_composite.py -- referee REF-P6-4: independent checks of lem:Dtot, lem:nogroup and the VWZ corner data of
cor:vwz in rigor/network_second_order.tex.  No code shared with rigor/g1b_kernel.py; mpmath and fractions only.
Reproduce (repository root):  ${PYTHON:-python3} rigor/ref_p6_4_composite.py > rigor/ref_p6_4_composite.out
L : the exact kernel of delta(s) = Q_I - V*P_+V for Psi_s = R_{q1,s k1} o ... o R_{qM,s kM}, derived here from PA eq.
    (hardy) P_+(x,y) = delta/2 - (i/2pi) pv 1/(x-y):  delta(s)(x,x') = (i/2pi)[sqrt(Psi'(x)Psi'(x'))/(Psi(x)-Psi(x'))
    - 1/(x-x')]; y-frame x = 1-e^{-y} with half-density factor e^{-(y+y')/2}; d/ds at s=0 by the COMPLEX-STEP rule
    f'(0) = Im f(ih)/h + O(h^2) (h = 1e-25, 60 digits; g1b used Richardson instead), against
    sum_k zeta_k D(y-y_k, y'-y_k), D = eq.(ddot), zeta_k = kappa_k (1-q_k), y_k = -log(1-q_k); and, as a control,
    against the wrong frame sum_k zeta_k D(y+y_k, y'+y_k).  Tolerance 1e-12 relative (zero entries: 1e-30 absolute).
N : lem:nogroup, exact rational arithmetic: masses [Phi''/Phi'] of Phi = Psi_s o Psi_t at its breakpoints, M = 2.
W : VWZ corner data (G1a prop:1B1A, prop:prot2 with c = b, d = a, theta_t = 1), exact rationals."""
import mpmath as mp
from fractions import Fraction as F
mp.mp.dps = 60

def Rpiece(z, q, sig):            # Moebius piece of R_{q,sig} and its derivative (valid for complex sig)
    den = 1 + sig * (z - q)
    return q + (z - q) / den, 1 / den ** 2

def Psi(x, qs, ks, s):
    """Psi_s(x) and Psi_s'(x); piece of R_{q_k} chosen by x > q_k (exact for every small s, see the report)."""
    z, d = mp.mpf(x), mp.mpf(1)
    for q, k in reversed(list(zip(qs, ks))):
        if x > q:
            z, dz = Rpiece(z, q, s * k); d = d * dz
    return z, d

def kappa_y(y, yp, qs, ks, s):     # e^{-(y+y')/2} kappa_Psi(x,x'), real for real s
    x, xp = 1 - mp.exp(-y), 1 - mp.exp(-yp)
    (z, d), (zp, dp) = Psi(x, qs, ks, s), Psi(xp, qs, ks, s)
    return mp.exp(-(y + yp) / 2) * (mp.sqrt(d) * mp.sqrt(dp) / (z - zp) - 1 / (x - xp))

def Dker(y, yp):                   # eq. (ddot)
    k = mp.sinh(y / 2) * mp.sinh(yp / 2) / mp.sinh((y - yp) / 2) ** 2
    if y < 0 < yp: return -1j / (2 * mp.pi) * k
    if yp < 0 < y: return 1j / (2 * mp.pi) * k
    return mp.mpc(0)

if __name__ == '__main__':
    print('# ref_p6_4_composite.out -- referee REF-P6-4, produced by rigor/ref_p6_4_composite.py (see docstring)')
    print('## L first-order defect of the composite vs sum of translated single-corner defects (lem:Dtot)')
    h = mp.mpf(10) ** -25; worst = 0; worst_wrong = 0
    configs = [((-0.5, 0.4), (0.9, 1.7)), ((-1.5, 0.2, 0.75), (0.3, 1.2, 2.5))]
    pts = [(-1.2, 0.1), (0.1, -1.2), (-0.3, 2.5), (1.0, 3.0), (-2.0, -0.8), (0.6, 1.2), (-0.9, 0.0), (2.0, -2.0)]
    for qs, ks in configs:
        ys = [-mp.log(1 - mp.mpf(q)) for q in qs]; zs = [mp.mpf(k) * (1 - mp.mpf(q)) for q, k in zip(qs, ks)]
        print('L corners q = %s, kappa = %s -> y_k = %s, zeta_k = %s' % (qs, ks, [mp.nstr(v, 8) for v in ys], [mp.nstr(v, 8) for v in zs]))
        for y, yp in pts:
            y, yp = mp.mpf(y), mp.mpf(yp)
            first = 1j / (2 * mp.pi) * mp.im(kappa_y(y, yp, qs, ks, mp.mpc(0, h))) / h
            pred = sum(z * Dker(y - yk, yp - yk) for z, yk in zip(zs, ys))
            wrong = sum(z * Dker(y + yk, yp + yk) for z, yk in zip(zs, ys))
            dev = abs(first - pred) / abs(pred) if abs(pred) > 0 else abs(first)
            worst = max(worst, dev if abs(pred) > 0 else (0 if abs(first) < 1e-30 else 1))
            if abs(pred) > 0: worst_wrong = max(worst_wrong, abs(first - wrong) / abs(pred))
            print("L   y=%+.2f y'=%+.2f  d/ds delta(s) = %s   sum_k zeta_k D(y-y_k,.) = %s   rel.dev = %.1e   wrong frame |dev| = %.2e"
                  % (y, yp, mp.nstr(first, 14), mp.nstr(pred, 14), dev, float(abs(first - wrong))))
    print('L max rel.dev = %.2e (tol 1e-12) -> %s;  wrong frame (y + y_k): max rel.dev = %.2e (must FAIL)' % (worst, 'PASS' if worst < 1e-12 else 'FAIL', worst_wrong))
    print('## N lem:nogroup: Schwarzian masses of Psi_s o Psi_t vs Psi_{s+t}, M = 2, exact rationals')
    def chain_jets(x0, maps, side):
        """(value, Phi', Phi'') of the composition maps[0] o ... o maps[-1] at x0 from the left (side=-1) or right (+1);
        each map (q, sig) is R_{q,sig}: identity for x <= q, Moebius piece for x > q; one-sided piece choice at q."""
        z, d1, d2 = x0, F(1), F(0)
        for q, sig in reversed(maps):
            right = z > q or (z == q and side > 0)
            if right:
                den = 1 + sig * (z - q); m1, m2 = 1 / den ** 2, -2 * sig / den ** 3; z = q + (z - q) / den
            else:
                m1, m2 = F(1), F(0)
            d1, d2 = m1 * d1, m2 * d1 ** 2 + m1 * d2          # chain rule (f o g)'' = f''(g) g'^2 + f'(g) g''
        return z, d1, d2
    q1, q2, k1, k2, s, t = F(-1, 2), F(1, 3), F(3, 2), F(5, 4), F(2, 7), F(3, 5)
    Ps = lambda u: [(q1, u * k1), (q2, u * k2)]
    comp, plain = Ps(s) + Ps(t), Ps(s + t)                  # Psi_s o Psi_t = R1(s) o R2(s) o R1(t) o R2(t)
    def mass(maps, x0):
        _, a1, a2 = chain_jets(x0, maps, -1); _, b1, b2 = chain_jets(x0, maps, +1); return b2 / b1 - a2 / a1
    # breakpoints of the composite: q1, q2, and x* = Psi_t^{-1}(q2) if q2 lies in Psi_t(q2, 1)
    def Psi_t_inv(yv):                                      # invert R1(t) o R2(t) on (q2, 1) exactly
        u = q1 + (yv - q1) / (1 - t * k1 * (yv - q1)); return q2 + (u - q2) / (1 - t * k2 * (u - q2))
    xs = Psi_t_inv(q2); top = chain_jets(F(1), Ps(t), -1)[0]
    print('N q1=%s q2=%s kappa=(%s,%s) s=%s t=%s;  Psi_t(q2) = %s (in (q1,q2)),  Psi_t(1) = %s' % (q1, q2, k1, k2, s, t, chain_jets(q2, Ps(t), +1)[0], top))
    for x0 in [q1, q2] + ([xs] if q2 < top else []):
        print('N   at x = %-10s mass of Sch(Psi_s o Psi_t) = %-12s mass of Sch(Psi_(s+t)) = %s' % (x0, mass(comp, x0), mass(plain, x0)))
    print('N   predicted at q2: -2 t kappa_2 = %s  vs  -2 (s+t) kappa_2 = %s;  match: %s' % (-2 * t * k2, -2 * (s + t) * k2, mass(comp, q2) == -2 * t * k2))
    print('## W VWZ corner data (G1a prop:1B1A, prop:prot2, c = b, d = a, theta_t = 1), exact')
    for a, b in ((F(1), F(1)), (F(1), F(3)), (F(2), F(7)), (F(1), F(100))):
        T = 2 * a + 2 * b; beta = lambda x, lo, hi: (x - lo) * (hi - x) / (hi - lo)
        p2, p3, p5 = a, a + b, T
        s1A, s2, s3 = 2 * (a + b) / (b * (a + 2 * b)), 2 * b / (b * (2 * b)), 2 * a / (b * (b + a))
        z1, z2, z3 = s1A * beta(p2, 0, T), s2 * beta(p2, 0, T), s3 * beta(p3, 0, T)
        eD = (p3 / (T - p3)) / (p2 / (T - p2)); eta = a / (a + 2 * b); zJ = s3 * beta(p3, p2, p5)
        r, u, v = F(1), b / a, b / (a + b)                     # brief's L->R chain formula at corner p2
        z2chain = 2 * r * (1 + v) / ((1 + r) * ((1 + u) * (1 + v) - 1))
        ok = (z1 == a / b and z2 == a * (a + 2 * b) / (2 * b * (a + b)) and z3 == a / b and eD == 1 / eta
              and zJ == 2 * a / (a + 2 * b) and z2chain == z2 and z2 / (a / b) == (a / b + 2) / (2 * (a / b + 1)))
        print('W a=%s b=%s: zeta_1=%s zeta_2=%s zeta_3=%s e^D23=%s 1/eta=%s zeta_3^(J)=%s chain-formula zeta_2=%s -> %s'
              % (a, b, z1, z2, z3, eD, 1 / eta, zJ, z2chain, 'all as in cor:vwz' if ok else 'MISMATCH'))
