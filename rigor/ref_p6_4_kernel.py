#!/usr/bin/env python3
"""ref_p6_4_kernel.py -- referee REF-P6-4: independent recomputation of the numbers of Thm T4 of
rigor/network_second_order.tex.  No code shared with rigor/g1b_kernel.py (not imported, not copied); only
numpy and mpmath primitives.  Reproduce (repository root):
    ${PYTHON:-python3} rigor/ref_p6_4_kernel.py > rigor/ref_p6_4_kernel.out
Conventions (document (C3)): w(p) = 1/(1+e^{-2 pi p}); p-kernel dhat(p,p') = (2pi)^-1 int int e^{ipy} D(y,y') e^{-ip'y'};
D(y,y') = -(i/2pi) sinh(y/2) sinh(y'/2)/sinh^2((y-y')/2) for y<0<y', its hermitian conjugate for y'<0<y, 0 else.
Methods (all mine):
  QG : Ghat(D) = (1/24pi^2) int_0^inf R(q) cos(qD) dq, R = tanh(pi q)/(q(1+q^2)): composite Gauss-Legendre on [0,Q]
       (panels 0.25, 30 nodes) + EXACT tail beyond Q (tanh = 1 there to 1e-100): -Ci(QD) - Re of E1-terms; Q = 20, 40, 80.
  CF : closed form (mpmath, 50 digits);  SR : the series summed term by term to n = N with N set by e^{-a_N D} < 1e-45.
  RP : rho(q) = (1/4) int dp |dhat(p,p-q)|^2/W(p,p-q) by mpmath tanh-sinh (dhat from T4(c), W = w(1-w')+w'(1-w)).
  DF : dhat(p,p') by direct 2-D quadrature of the definition: (t,u) coordinates on each quadrant (y=-tu, y'=t(1-u)
       resp. y=tu, y'=-t(1-u)), composite Gauss-Legendre (t in [0,100], panels 1; u in 14 graded panels), n = 16 and 24.
Tolerances (fixed here, before the run): QG vs CF 1e-8 relative to Ghat(0) (brief); SR vs CF 1e-12; RP vs rho 1e-10
relative; DF vs T4(c) 1e-9 absolute; validation integrals 1e-12.  No operator is discretised and no regulator is used."""
import os, sys
import numpy as np
import mpmath as mp
mp.mp.dps = 50
PI = np.pi
TOL_Q, TOL_S, TOL_R, TOL_K, TOL_V = 1e-8, 1e-12, 1e-10, 1e-9, 1e-12
GL30 = np.polynomial.legendre.leggauss(30)

def panels_GL(f, a, b, h, nodes=GL30):
    x, w = nodes; edges = np.arange(a, b + 0.5 * h, h)
    tot = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        xx = 0.5 * (hi + lo) + 0.5 * (hi - lo) * x
        tot += 0.5 * (hi - lo) * np.dot(w, f(xx))
    return tot

def tail_exact(Q, D):
    """int_Q^inf cos(qD)/(q(1+q^2)) dq for D > 0, via 1/(q(1+q^2)) = 1/q - (1/2)[1/(q-i)+1/(q+i)] and
    int_Q^inf e^{iqD}/(q-c) dq = e^{icD} E1(-iD(Q-c)) (contour rotated in the fourth quadrant)."""
    Q, D = mp.mpf(Q), mp.mpf(D)
    t1 = -mp.ci(Q * D)
    t2 = 0
    for c in (mp.mpc(0, 1), mp.mpc(0, -1)):
        t2 += mp.exp(1j * c * D) * mp.e1(-1j * D * (Q - c))
    return float(t1 - mp.re(t2) / 2)

def R(q):
    return np.tanh(PI * q) / (q * (1 + q * q))

def Ghat_QG(D, Q):
    main = panels_GL(lambda q: R(q) * np.cos(q * D), 0.0, Q, 0.25)
    tail = 0.5 * float(mp.log(1 + 1 / mp.mpf(Q) ** 2)) if D == 0 else tail_exact(Q, D)
    return (main + tail) / (24 * PI ** 2)

def Ghat_CF(D):
    D = mp.mpf(abs(D))
    if D == 0:
        return 1 / (12 * mp.pi ** 2)
    return (mp.cosh(D / 2) - mp.sinh(D / 2) ** 2 * mp.log(mp.coth(D / 4))) / (12 * mp.pi ** 2)

def Ghat_SR(D):
    D = mp.mpf(abs(D)); s = mp.mpf(0); n = 0
    while True:
        a = n + mp.mpf(1) / 2; term = mp.exp(-a * D) / (a * (1 - a * a)); s += term; n += 1
        if D > 0 and mp.exp(-a * D) < mp.mpf(10) ** -45 and n > 5: break
        if D == 0 and n > 200000: break
    return s / (24 * mp.pi ** 2), n

def w(p):
    return 1 / (1 + mp.exp(-2 * mp.pi * p))

def dhat_T4c(p, pp):
    p, pp = mp.mpf(p), mp.mpf(pp)
    if p == pp:
        return mp.diff(w, p) * p / mp.pi
    return (w(p) - w(pp)) * (p + pp) / (2 * mp.pi * (p - pp) * (1 + (p - pp) ** 2))

def W(p, pp):
    return w(p) * (1 - w(pp)) + w(pp) * (1 - w(p))

def rho_RP(q):
    f = lambda p: abs(dhat_T4c(p, p - q)) ** 2 / W(p, p - q)
    # |p| <= 45 + |q|: the integrand is O(p^2 e^{-2 pi |p|}) < 1e-115 beyond (dropped); 160 digits so that 1 - w(p)
    # (down to 1e-123) is resolved by the literal formula of T4(c)
    with mp.workdps(160):
        pts = [-45 - abs(q), -20, -6, -2, q / 2 - 0.5, q / 2, q / 2 + 0.5, 2 + q, 6 + q, 20 + q, 45 + abs(q)]
        val = mp.quad(f, sorted(set(pts), key=lambda z: float(z))) / 4
    return +val

def rho_formula(q):
    q = mp.mpf(q)
    return mp.tanh(mp.pi * q) / (48 * mp.pi ** 2 * q * (1 + q * q))

def Dker(y, yp):
    """eq. (ddot) of the document, literally: y<0<y' block and its hermitian conjugate."""
    k = np.sinh(y / 2) * np.sinh(yp / 2) / np.sinh((y - yp) / 2) ** 2
    out = np.zeros(np.broadcast(y, yp).shape, dtype=complex)
    out = np.where((y < 0) & (yp > 0), -1j / (2 * PI) * k, out)
    out = np.where((yp < 0) & (y > 0), np.conj(-1j / (2 * PI) * k), out)  # conj(D(y',y)) = conj of same k
    return out

def dhat_DF(p, pp, n):
    x, wts = np.polynomial.legendre.leggauss(n)
    ue = np.array([0, 1e-3, 3e-3, 1e-2, 3e-2, .1, .3, .5, .7, .9, .97, .99, .997, .999, 1.0])
    uu = np.concatenate([0.5 * (b + a) + 0.5 * (b - a) * x for a, b in zip(ue[:-1], ue[1:])])
    wu = np.concatenate([0.5 * (b - a) * wts for a, b in zip(ue[:-1], ue[1:])])
    te = np.arange(0.0, 100.0 + 1e-9, 1.0)
    tt = np.concatenate([0.5 * (b + a) + 0.5 * (b - a) * x for a, b in zip(te[:-1], te[1:])])
    wt = np.concatenate([0.5 * (b - a) * wts for a, b in zip(te[:-1], te[1:])])
    T, U = np.meshgrid(tt, uu, indexing='ij'); WW = np.outer(wt, wu) * T   # Jacobian t
    tot = 0j
    for sgn in (+1, -1):          # sgn=+1: quadrant y<0<y' (y=-tu, y'=t(1-u)); sgn=-1: y'<0<y (y=tu, y'=-t(1-u))
        y, yp = -sgn * T * U, sgn * T * (1 - U)
        tot += np.sum(WW * Dker(y, yp) * np.exp(1j * (p * y - pp * yp)))
    return tot / (2 * PI)

def tail_lorentz(Q, D):
    """int_Q^inf cos(qD)/(1+q^2) dq = Re (1/2i)[e^{-D} E1(-iD(Q-i)) - e^{D} E1(-iD(Q+i))]  (D > 0)."""
    Q, D, i = mp.mpf(Q), mp.mpf(D), mp.mpc(0, 1)
    return float(mp.re((mp.exp(-D) * mp.e1(-i * D * (Q - i)) - mp.exp(D) * mp.e1(-i * D * (Q + i))) / (2 * i)))

if __name__ == '__main__':
    print('# ref_p6_4_kernel.out -- referee REF-P6-4, produced by rigor/ref_p6_4_kernel.py (methods, tolerances: docstring)')
    print('## V validation on exactly known integrals (tol %.0e)' % TOL_V)
    worst = 0.0
    for D in (0.5, 3.0):          # int_0^inf cos(qD)/(1+q^2) = (pi/2) e^{-D}: GL on [0,40] + exact E1 tail
        main = panels_GL(lambda q: np.cos(q * D) / (1 + q * q), 0, 40, 0.25)
        dev = main + tail_lorentz(40, D) - PI / 2 * np.exp(-D); worst = max(worst, abs(dev))
        print('V1 D=%.1f  int_0^inf cos(qD)/(1+q^2) dq - (pi/2)e^-D = %+.2e' % (D, dev))
    for Q in (20, 40, 80):
        dev = 24 * PI ** 2 * Ghat_QG(0.0, Q) - 2; worst = max(worst, abs(dev))
        print('V2 Q=%d  int_0^inf R(q) dq - 2 = %+.2e   (i.e. Ghat(0) = 1/(12 pi^2) = f2/c)' % (Q, dev))
    for p in (0.3, 1.1):
        val = float(mp.quad(lambda z: mp.sin(p * z) / mp.sinh(z / 2), [0, 1, 10, mp.inf]))
        dev = val - PI * np.tanh(PI * p); worst = max(worst, abs(dev))
        print('V3 Fourier convention: int_0^inf sin(pz)/sinh(z/2) dz - pi tanh(pi p), p=%.1f: %+.2e' % (p, dev))
    print('V max |dev| = %.2e -> %s' % (worst, 'PASS' if worst < TOL_V else 'FAIL'))
    print('## P Ghat(D)/Ghat(0): QG (Q = 20, 40, 80) vs closed form CF vs series SR (tol QG %.0e rel. Ghat(0); SR %.0e)' % (TOL_Q, TOL_S))
    G0 = Ghat_CF(0); wq = ws = wQ = 0.0
    print('#  D      CF/G0                 QG40/G0 - CF/G0   QG80-QG20 (/G0)   SR/G0 - CF/G0   (N terms)')
    for D in (0.5, 1, 1.5, 2, 3, 4, 5, 6, 8):
        cf = Ghat_CF(D); q20, q40, q80 = (Ghat_QG(float(D), Q) for Q in (20, 40, 80)); sr, N = Ghat_SR(D)
        d1 = (q40 - float(cf)) / float(G0); d2 = (q80 - q20) / float(G0); d3 = float((sr - cf) / G0)
        wq = max(wq, abs(d1), abs((q20 - float(cf)) / float(G0)), abs((q80 - float(cf)) / float(G0))); ws = max(ws, abs(d3))
        print('  %-5s  %.15f   %+.2e         %+.2e         %+.2e       %d' % (D, float(cf / G0), d1, d2, d3, N))
    print('P max|QG - CF|/G0 = %.2e (tol %.0e) -> %s;  max|SR - CF|/G0 = %.2e (tol %.0e) -> %s' % (
        wq, TOL_Q, 'PASS' if wq < TOL_Q else 'FAIL', ws, TOL_S, 'PASS' if ws < TOL_S else 'FAIL'))
    print('## R rho(q) from the p-integral (1/4) int |dhat0(p,p-q)|^2/W(p,p-q) dp vs tanh(pi q)/(48 pi^2 q (1+q^2)) (tol %.0e rel.)' % TOL_R)
    wr = 0.0
    for q in (0.1, 0.5, 1.0, 2.0, 5.0):
        a, b = rho_RP(q), rho_formula(q); rel = float(abs(a / b - 1)); wr = max(wr, rel)
        print('R q=%.1f  p-integral = %.15e  formula = %.15e  rel.dev = %.1e' % (q, float(a), float(b), rel))
    print('R max rel.dev = %.2e -> %s' % (wr, 'PASS' if wr < TOL_R else 'FAIL'))
    print('## K dhat0(p,p\') by direct 2-D quadrature of (2pi)^-1 int int e^{ipy} D(y,y\') e^{-ip\'y\'} vs T4(c) (tol %.0e abs.)' % TOL_K)
    wk = 0.0
    for p, pp in ((0.4, -0.1), (1.2, 0.3), (-0.9, 0.6), (0.35, 0.35), (2.0, -1.5), (0.05, 0.8)):
        d16, d24 = dhat_DF(p, pp, 16), dhat_DF(p, pp, 24); f = float(dhat_T4c(p, pp)); dev = abs(d24 - f); wk = max(wk, dev)
        print("K p=%+.2f p'=%+.2f  direct(n=24) = %+.12f %+.1ei  |n24-n16| = %.1e  T4(c) = %+.12f  |dev| = %.1e  -T4(c) dev = %.1e"
              % (p, pp, d24.real, d24.imag, abs(d24 - d16), f, dev, abs(d24 + f)))
    print('K max |dev| = %.2e -> %s' % (wk, 'PASS' if wk < TOL_K else 'FAIL'))
    print('## B bounds of T4(d) on the grid D = 0.01, 0.02, ..., 20 (2000 points), closed form at 50 digits')
    viol = 0; mlo = mhi = mab = mp.inf; prev = Ghat_CF(0); nonmono = 0; nonpos = 0
    for k in range(1, 2001):
        D = mp.mpf(k) / 100; g = Ghat_CF(D); x = mp.exp(-D / 2); pi2 = mp.pi ** 2
        lo, hi, ab = g - x * (4 - x * x) / (36 * pi2), x / (9 * pi2) - g, x ** 3 / (36 * pi2) - abs(g - x / (9 * pi2))
        viol += (lo < 0) + (hi < 0) + (ab < 0); mlo, mhi, mab = min(mlo, lo / g), min(mhi, hi / g), min(mab, ab / g)
        nonmono += (g >= prev); nonpos += (g <= 0); prev = g
    print('B violations = %d; min relative margins (lower, upper, |G - x/9pi^2| <= x^3/36pi^2) = %.3e, %.3e, %.3e' % (viol, float(mlo), float(mhi), float(mab)))
    print('B sharpness: 9 pi^2 e^{D/2} Ghat(D) - 1 at D = 10, 20, 40: %s' % ', '.join('%.3e' % float(9 * mp.pi ** 2 * mp.exp(mp.mpf(D) / 2) * Ghat_CF(D) - 1) for D in (10, 20, 40)))
    print('## E sign, monotonicity, regularity at 0')
    print('E grid: Ghat <= 0 at %d points; Ghat(D_{k+1}) >= Ghat(D_k) at %d points (of 2000)' % (nonpos, nonmono))
    c0 = mp.log(10) / (24 * mp.pi ** 2); prevd2 = None
    for k in range(1, 7):
        D = mp.mpf(10) ** -k; d1 = mp.diff(Ghat_CF, D, 1); d2 = mp.diff(Ghat_CF, D, 2)
        inc = '' if prevd2 is None else '   G\'\'(D) - G\'\'(10D) = %+.6e (log-singularity prediction -ln10/(24pi^2) = %+.6e)' % (float(d2 - prevd2), float(-c0))
        print("E D=1e-%d  G'(D) = %+.3e  G''(D) = %+.6e%s" % (k, float(d1), float(d2), inc)); prevd2 = d2
