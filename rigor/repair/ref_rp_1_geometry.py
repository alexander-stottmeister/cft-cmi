"""REF-RP-1: independent exact check of lem:geom of rigor/moebius_reduction_general_nets.tex.
Exact rational arithmetic (fractions.Fraction); tolerance 0 (exact equality) for rational identities;
Schwarzian of circle Moebius maps in mpmath at 50 digits, tolerance 1e-40 fixed before the run.
Run: ${PYTHON:-python3} rigor/repair/ref_rp_1_geometry.py > rigor/repair/ref_rp_1_geometry.out"""
from fractions import Fraction as Fr
import random, mpmath
random.seed(20261119)
def R(): return Fr(random.randint(1, 997), random.randint(1, 97))
nfail = 0; N = 2000
for _ in range(N):
    a, L, s, y = R(), R(), R(), R() * random.choice([1, -1])
    kap = a / (a + L)
    g = lambda x: (a + L) * x / (L * (x + a))
    gp = lambda x: a * (a + L) / (L * (x + a) ** 2)
    ginv = lambda y: a * L * y / (a + L - L * y)
    h = lambda x, t: L * x / (L + t * x)          # flow of m = -x^2/L
    hh = lambda y, t: y / (1 + t * y)             # flow of mhat = -y^2
    m = lambda x: -x * x / L
    ok = (g(0) == 0 and g(L) == 1 and ginv(g(L / 3)) == L / 3)
    if y * L != a + L:   # y not the image of infinity
        x = ginv(y)
        ok &= (g(x) == y)
        ok &= (gp(x) * m(x) == kap * (-y * y))                    # (3): g_* m = kappa mhat
        if L + s * x != 0 and 1 + kap * s * y != 0:
            ok &= (g(h(x, s)) == hh(y, kap * s))                  # (5): g h_s g^-1 = hhat_{kappa s}
    # flows solve the ODE: d/dt h = m(h), d/dt hh = -hh^2 (exact derivative of rational fn)
    x0 = R(); t = R()
    ok &= (-L * x0 * x0 / (L + t * x0) ** 2 == m(h(x0, t)))
    # cross ratio and z
    lA, lB, lC = a, L / (1 + s), L * s / (1 + s)
    z = lA * lC / (lB * (lA + lB + lC))
    x1, x2, x3, x4 = -a, Fr(0), L / (1 + s), L
    cr = (x3 - x1) * (x4 - x2) / ((x3 - x2) * (x4 - x1))
    etaV = lA * lC / ((lA + lB) * (lB + lC))
    ok &= (z == a * s / (a + L) == kap * s) and (cr == 1 + z) and (z == etaV / (1 - etaV))
    # image of B = h_s(D) right endpoint: h_s(L) = L/(1+s)
    ok &= (h(L, s) == L / (1 + s)) and (g(L / (1 + s)) == 1 / (1 + kap * s))
    nfail += (not ok)
print("rational identities (3),(5), flows, cross ratio, z = kappa s, eta_V: %d samples, %d failures (exact)" % (N, nfail))
mpmath.mp.dps = 50; worst = 0
for _ in range(200):
    q = mpmath.mpc(random.uniform(-3, 3), random.uniform(-3, 3)); p = mpmath.sqrt(1 + abs(q) ** 2) * mpmath.expjpi(random.random())
    gam = lambda z: (p * z + q) / (mpmath.conj(q) * z + mpmath.conj(p))
    z0 = mpmath.expjpi(2 * random.random())
    d1, d2, d3 = (mpmath.diff(gam, z0, k) for k in (1, 2, 3))
    S = d3 / d1 - mpmath.mpf(3) / 2 * (d2 / d1) ** 2
    worst = max(worst, abs(S))
print("max |Schwarzian| of circle Moebius maps (200 samples, 50 digits):", mpmath.nstr(worst, 3), "tol 1e-40:", worst < mpmath.mpf('1e-40'))
print("g_B/8 =? c/(12 pi^2): (2/(3 pi^2))/8 - 1/(12 pi^2) =", (Fr(2, 3) / 8 - Fr(1, 12)), "(in units of c/pi^2, exact)")
