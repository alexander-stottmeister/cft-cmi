#!/usr/bin/env python
"""p3_check.py -- numerical verification of every intermediate closed form in
   rigor/kernel_identity.tex  (analytic proof of Lemma 5.1(ii) of universality_normalization.tex).

Conventions are taken from universality_normalization.tex, eqs. (D1-kernel), (ghat),
and from numerics/verify_normalization.py (function D1_kernel_FT):

    psi_kappa(xi) = e^{i kappa xi /2pi}/(2pi)
    Dtilde^{(1)}(xi,xi') = (i/2pi) R(xi,xi'),  R = -sinh(xi/2) sinh(xi'/2)/sinh^2((xi-xi')/2)   on xi<0<xi'
                         = adjoint on xi'<0<xi,  0 on the diagonal blocks
    J(kappa,kappa') = int_{-inf}^0 dxi int_0^inf dxi' e^{-i kappa xi/2pi} R(xi,xi') e^{i kappa' xi'/2pi}
    D1(kappa,kappa') = (1/(2pi)^2) [ (i/2pi) J(kappa,kappa') + conj( (i/2pi) J(kappa',kappa) ) ]

Target:  D1(kappa,kappa') = i (q_k - q_k') gfrak(kappa,kappa'),
         gfrak = (1/(2pi)^2) ghat((kappa-kappa')/2pi) (kappa+kappa')/(4pi),  ghat(k) = -2i/(k(k^2+1)),
         q_kappa = 1/(1+e^kappa).

Run:  python p3_check.py           (includes the slow literal 2-D quadrature)
      python p3_check.py --fast    (skips it)
"""
import sys
import mpmath as mp

mp.mp.dps = 30
pi = mp.pi
half = mp.mpf(1) / 2
FAST = "--fast" in sys.argv
TOL = mp.mpf(10) ** (-24)          # all high-precision checks must beat this
FAILURES = []


def report(tag, err, tol=TOL, extra=""):
    ok = abs(err) <= tol
    if not ok:
        FAILURES.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag:<58s} err = {mp.nstr(abs(err), 3):>10s}  {extra}")


# --------------------------------------------------------------------------------------
# basic objects
# --------------------------------------------------------------------------------------
def Rker(xi, xip):
    """R(xi,xi') on the block xi<0<xi';  Dtilde^{(1)} = (i/2pi) R."""
    return -mp.sinh(xi / 2) * mp.sinh(xip / 2) / mp.sinh((xi - xip) / 2) ** 2


def rho(a, b):
    """rho(a,b) = R(-a,b),  a,b>0."""
    return mp.sinh(a / 2) * mp.sinh(b / 2) / mp.sinh((a + b) / 2) ** 2


def q(kap):
    return 1 / (1 + mp.e ** kap)


def ghat(k):
    return -2j / (k * (k ** 2 + 1))


def gfrak(kap, kapp):
    return ghat((kap - kapp) / (2 * pi)) * (kap + kapp) / (4 * pi) / (2 * pi) ** 2


def rhs_identity(kap, kapp):
    """i (q-q') gfrak; at kappa=kappa' the removable singularity is resolved by the limit."""
    if kap == kapp:
        return -kap / (8 * pi ** 2 * mp.cosh(kap / 2) ** 2)
    return 1j * (q(kap) - q(kapp)) * gfrak(kap, kapp)


# --------------------------------------------------------------------------------------
# the four representations of J
# --------------------------------------------------------------------------------------
def J_2d_xi(kap, kapp, maxdeg=5):
    """Literal definition: double quadrature over xi<0<xi' (slow, ~11-13 digits)."""
    def inner(xi):
        f = lambda xip: Rker(xi, xip) * mp.e ** (1j * kapp * xip / (2 * pi))
        return mp.quad(f, [0, 1, 5, 20, 60], maxdegree=maxdeg) * mp.e ** (-1j * kap * xi / (2 * pi))
    return mp.quad(inner, [-60, -20, -5, -1, 0], maxdegree=maxdeg)


def J_1d(al, be):
    """Exact reduction (s,d)=( (a+b)/2,(a-b)/2 ) with the d-integral done in closed form."""
    k = al - be
    sg = al + be
    if k == 0:
        br = lambda s: 2 * mp.cosh(s) * s - 2 * mp.sinh(s)
    else:
        br = lambda s: (2 * mp.cosh(s) * mp.sin(k * s) / k
                        - 2 * (mp.cos(k * s) * mp.sinh(s) + k * mp.sin(k * s) * mp.cosh(s)) / (1 + k ** 2))
    return mp.quad(lambda s: mp.e ** (1j * sg * s) * br(s) / mp.sinh(s) ** 2, [0, 1, 3, 10, 30, 80])


def Efun(n, x):
    """E_n(x) = int_0^inf e^{i x a} e^{-n a} sinh(a/2) da."""
    return half / ((n - 1j * x) ** 2 - mp.mpf(1) / 4)


def J_series(al, be):
    return 4 * mp.nsum(lambda n: n * Efun(n, al) * Efun(n, be), [1, mp.inf])


def J_closed(al, be):
    k = al - be
    sg = al + be
    if k == 0:
        return 2 + 2j * al * mp.polygamma(1, half - 1j * al)
    return (-sg / (k * (k ** 2 + 1)) * (mp.digamma(half - 1j * al) - mp.digamma(half - 1j * be))
            + 2 / (k ** 2 + 1))


def D1_from_J(kap, kapp, Jfun=J_1d):
    """D1 = (1/(2pi)^2)[(i/2pi)J(k,k') + conj((i/2pi)J(k',k))] = -Im J /(pi (2pi)^2)  (J symmetric)."""
    al, be = kap / (2 * pi), kapp / (2 * pi)
    Jab, Jba = Jfun(al, be), Jfun(be, al)
    return ((1j / (2 * pi)) * Jab + mp.conj((1j / (2 * pi)) * Jba)) / (2 * pi) ** 2


PTS = [(1, 3), (2.5, -1), (4, 4.5), (-3, 0.7), (6, -5), (0.4, -0.4), (0.05, 0.03)]
DIAG = [1, 2.5, -3, 0]

print(__doc__.split("Run:")[0])
print("=" * 100)

# --------------------------------------------------------------------------------------
print("C1  <1>2a  substitution a=-xi, b=xi':  R(-a,b) = sinh(a/2)sinh(b/2)/sinh^2((a+b)/2) > 0")
for (a, b) in [(0.3, 1.7), (2.0, 0.1), (5.0, 4.0), (0.01, 0.02)]:
    a, b = mp.mpf(a), mp.mpf(b)
    report(f"R(-{float(a)},{float(b)}) = rho({float(a)},{float(b)})", Rker(-a, b) - rho(a, b),
           extra=f"value {mp.nstr(rho(a,b),10)} (>0)")

# --------------------------------------------------------------------------------------
print("C2  <1>2b  rho = (cosh s - cosh d)/(2 sinh^2 s),  s=(a+b)/2, d=(a-b)/2")
for (a, b) in [(0.3, 1.7), (2.0, 0.1), (0.01, 0.02), (7.0, 3.0)]:
    a, b = mp.mpf(a), mp.mpf(b)
    s, d = (a + b) / 2, (a - b) / 2
    report(f"rho({float(a)},{float(b)})", rho(a, b) - (mp.cosh(s) - mp.cosh(d)) / (2 * mp.sinh(s) ** 2))

print("C3  <1>2c  bound 0 <= rho(a,b) <= 1/(4 cosh^2((a+b)/4)) <= min(1/4, e^{-(a+b)/2})")
worst = mp.mpf(0)
for i in range(1, 40):
    for j in range(1, 40):
        a, b = mp.mpf(i) / 7, mp.mpf(j) / 5
        v = rho(a, b)
        B = 1 / (4 * mp.cosh((a + b) / 4) ** 2)
        worst = max(worst, v - B)
        if v < 0 or v - B > TOL or B - min(mp.mpf(1) / 4, mp.e ** (-(a + b) / 2)) > TOL:
            FAILURES.append("C3")
print(f"  [{'PASS' if 'C3' not in FAILURES else 'FAIL'}] 1521 grid points, max(rho - bound) = "
      f"{mp.nstr(worst,3)} (<=0 up to rounding; equality holds on a=b)")
Ibound = mp.quad(lambda t: t / (4 * mp.cosh(t / 4) ** 2), [0, 4, 20, mp.inf])
report("int_0^inf t dt/(4 cosh^2(t/4)) = 4 log 2", Ibound - 4 * mp.log(2),
       extra=f"= {mp.nstr(Ibound,15)}")
report("J(0,0) = iint rho = 2  (< 4 log 2 = 2.7726)", J_1d(mp.mpf(0), mp.mpf(0)) - 2)

# --------------------------------------------------------------------------------------
print("C4  <1>3a  1/sinh^2(s) = 4 sum_{n>=1} n e^{-2ns}")
for s in [mp.mpf('0.2'), mp.mpf('1.0'), mp.mpf('3.0')]:
    ser = 4 * mp.nsum(lambda n: n * mp.e ** (-2 * n * s), [1, mp.inf])
    report(f"s={float(s)}", ser - 1 / mp.sinh(s) ** 2)

print("C5  <1>3b  E_n(x) = int_0^inf e^{ixa-na} sinh(a/2) da = (1/2)/((n-ix)^2-1/4)")
for n in [1, 2, 5, 12]:
    for x in [mp.mpf('0.37'), mp.mpf('-1.1')]:
        num = mp.quad(lambda a: mp.e ** (1j * x * a - n * a) * mp.sinh(a / 2), [0, 5, 30, 120])
        report(f"n={n}, x={float(x)}", num - Efun(n, x))

# --------------------------------------------------------------------------------------
print("C6  <1>2d/<1>4a  exact (s,d) reduction of the double integral to a 1-D integral")
print("      inner integral  int_{-s}^{s} e^{ikd}(cosh s - cosh d) dd = 2cosh(s) sin(ks)/k")
print("                                       - 2(cos(ks) sinh s + k sin(ks) cosh s)/(1+k^2)")
for s in [mp.mpf('0.4'), mp.mpf('2.3')]:
    for k in [mp.mpf('0.31'), mp.mpf('-0.77')]:
        num = mp.quad(lambda d: mp.e ** (1j * k * d) * (mp.cosh(s) - mp.cosh(d)), [-s, 0, s])
        cf = (2 * mp.cosh(s) * mp.sin(k * s) / k
              - 2 * (mp.cos(k * s) * mp.sinh(s) + k * mp.sin(k * s) * mp.cosh(s)) / (1 + k ** 2))
        report(f"s={float(s)}, k={float(k)}", num - cf)

# --------------------------------------------------------------------------------------
print("C7  <1>4b  partial fractions of n/prod_j (n-c_j),  c = {p+-1/2, r+-1/2}, p=i alpha, r=i beta")
for (kap, kapp) in [(1, 3), (2.5, -1), (-3, 0.7)]:
    al, be = mp.mpf(kap) / (2 * pi), mp.mpf(kapp) / (2 * pi)
    p, r = 1j * al, 1j * be
    delta = p - r
    c = [p + half, p - half, r + half, r - half]
    rr = [c[j] / mp.fprod([c[j] - c[k] for k in range(4) if k != j]) for j in range(4)]
    Lam = (p + r) / (delta * (delta ** 2 - 1))
    report(f"({kap},{kapp}) sum_j r_j = 0", sum(rr))
    report(f"({kap},{kapp}) r_1+r_2 = -Lambda", rr[0] + rr[1] + Lam)
    report(f"({kap},{kapp}) r_3+r_4 = +Lambda", rr[2] + rr[3] - Lam)
    report(f"({kap},{kapp}) r_2/(1/2-p) = 1/(delta(delta-1))", rr[1] / (half - p) - 1 / (delta * (delta - 1)))
    report(f"({kap},{kapp}) r_4/(1/2-r) = 1/(delta(delta+1))", rr[3] / (half - r) - 1 / (delta * (delta + 1)))
    for n in [mp.mpf(1), mp.mpf(7)]:
        report(f"({kap},{kapp}) Heaviside expansion at n={int(n)}",
               n / mp.fprod([n - cj for cj in c]) - sum(rr[j] / (n - c[j]) for j in range(4)))

print("C8  <1>4c  sum_{n>=1} [1/(n-c) - 1/n] = -gamma - psi(1-c)")
for cc in [mp.mpf('0.3') + 0.4j, half + 0.9j, -half - 1.7j]:
    report(f"c={mp.nstr(cc,6)}", mp.nsum(lambda n: 1 / (n - cc) - 1 / n, [1, mp.inf])
           + mp.euler + mp.digamma(1 - cc))

# --------------------------------------------------------------------------------------
print("C9  <1>4d  J = -sigma/(k(k^2+1)) [psi(1/2-i alpha) - psi(1/2-i beta)] + 2/(k^2+1)")
print("           checked against the 1-D integral and against the series 4 sum n E_n E_n")
for (kap, kapp) in PTS:
    al, be = mp.mpf(kap) / (2 * pi), mp.mpf(kapp) / (2 * pi)
    Ji, Js, Jc = J_1d(al, be), J_series(al, be), J_closed(al, be)
    report(f"({kap},{kapp}) series = integral", Js - Ji, extra=f"J = {mp.nstr(Ji,14)}")
    report(f"({kap},{kapp}) closed form = integral", Jc - Ji)
    report(f"({kap},{kapp}) J symmetric in alpha<->beta", J_1d(be, al) - Ji)
for kap in DIAG:
    al = mp.mpf(kap) / (2 * pi)
    report(f"diagonal kappa={kap}: J = 2 + 2 i alpha psi'(1/2-i alpha)",
           J_closed(al, al) - J_1d(al, al), extra=f"J = {mp.nstr(J_1d(al,al),14)}")
    report(f"diagonal kappa={kap}: series = integral", J_series(al, al) - J_1d(al, al))

# --------------------------------------------------------------------------------------
print("C10 <1>5  Im psi(1/2-i x) = -(pi/2) tanh(pi x)   and   Re psi'(1/2-i x) = pi^2/(2 cosh^2(pi x))")
for x in [mp.mpf('0.4'), mp.mpf('-1.3'), mp.mpf(0)]:
    report(f"x={float(x)}", mp.im(mp.digamma(half - 1j * x)) + pi / 2 * mp.tanh(pi * x))
    report(f"x={float(x)} (derivative)",
           mp.re(mp.polygamma(1, half - 1j * x)) - pi ** 2 / (2 * mp.cosh(pi * x) ** 2))

print("C11 <1>5  Im J = -pi sigma (q_kappa - q_kappa')/(k(k^2+1)),  sigma=(kappa+kappa')/2pi, k=(kappa-kappa')/2pi")
for (kap, kapp) in PTS:
    kap, kapp = mp.mpf(kap), mp.mpf(kapp)
    if kap == kapp:
        continue
    al, be = kap / (2 * pi), kapp / (2 * pi)
    k, sg = al - be, al + be
    report(f"({float(kap)},{float(kapp)})",
           mp.im(J_1d(al, be)) + pi * sg * (q(kap) - q(kapp)) / (k * (k ** 2 + 1)))

# --------------------------------------------------------------------------------------
print("C12 <1>6  THE IDENTITY   D1(kappa,kappa') = i (q_kappa - q_kappa') gfrak(kappa,kappa')")
print("          and the explicit form  D1 = (q-q')(kappa+kappa')/[(kappa-kappa')((kappa-kappa')^2+4pi^2)]")
print("                                    = -v sinh(u/2)/[u(u^2+4pi^2)(cosh(v/2)+cosh(u/2))],  u=k-k', v=k+k'")
for (kap, kapp) in PTS:
    kap, kapp = mp.mpf(kap), mp.mpf(kapp)
    lhs = D1_from_J(kap, kapp)
    rhs = rhs_identity(kap, kapp)
    report(f"({float(kap)},{float(kapp)}) LHS = RHS", lhs - rhs, extra=f"D1 = {mp.nstr(mp.re(lhs),16)}")
    report(f"({float(kap)},{float(kapp)}) LHS real", mp.im(lhs))
    if kap != kapp:
        u, v = kap - kapp, kap + kapp
        expl = (q(kap) - q(kapp)) * v / (u * (u ** 2 + 4 * pi ** 2))
        expl2 = -v * mp.sinh(u / 2) / (u * (u ** 2 + 4 * pi ** 2) * (mp.cosh(v / 2) + mp.cosh(u / 2)))
        report(f"({float(kap)},{float(kapp)}) explicit rational form", lhs - expl)
        report(f"({float(kap)},{float(kapp)}) hyperbolic form", lhs - expl2)

print("C13 <1>7  diagonal: D1(kappa,kappa) = -kappa/(8 pi^2 cosh^2(kappa/2)) = -kappa q(1-q)/(2 pi^2)")
for kap in DIAG:
    kap = mp.mpf(kap)
    lhs = D1_from_J(kap, kap)
    cf = -kap / (8 * pi ** 2 * mp.cosh(kap / 2) ** 2)
    report(f"kappa={float(kap)}", lhs - cf, extra=f"D1 = {mp.nstr(mp.re(lhs),16)}")
    report(f"kappa={float(kap)} (= -kappa q(1-q)/2pi^2)", lhs + kap * q(kap) * (1 - q(kap)) / (2 * pi ** 2))
    # continuity of the right-hand side across the diagonal
    for h in [mp.mpf('1e-3'), mp.mpf('1e-5')]:
        report(f"kappa={float(kap)} RHS continuity, h={mp.nstr(h,2)}",
               rhs_identity(kap + h, kap - h) - cf, tol=mp.mpf(10) * h ** 2 + mp.mpf('1e-20'))

# --------------------------------------------------------------------------------------
if not FAST:
    print("C14 <1>1  literal 2-D quadrature in (xi,xi') of the definition (slow; ~11-13 digits)")
    for (kap, kapp) in [(1, 3), (2.5, -1)]:
        kap, kapp = mp.mpf(kap), mp.mpf(kapp)
        lhs = D1_from_J(kap, kapp, Jfun=lambda a, b: J_2d_xi(a * 2 * pi, b * 2 * pi))
        rhs = rhs_identity(kap, kapp)
        rel = abs(lhs - rhs) / abs(rhs)
        print(f"  [{'PASS' if rel < mp.mpf('1e-10') else 'FAIL'}] ({float(kap)},{float(kapp)}) "
              f"2-D quadrature vs identity: rel err = {mp.nstr(rel,3)}   D1 = {mp.nstr(mp.re(lhs),14)}")
        if rel >= mp.mpf('1e-10'):
            FAILURES.append("C14")
else:
    print("C14 skipped (--fast)")

print("=" * 100)
print("ALL CHECKS PASSED" if not FAILURES else f"FAILURES: {sorted(set(FAILURES))}")
