"""C6 council check: independent quadrature of the closed-form constants quoted in paper 1
(sec_quadratic.tex eq:two-integrals, prop:gBvalue; rem:hellinger h2; thm:main f2 = 0.00844343 r; prop:twobranch
8 f2 = 2c/(3 pi^2); intro (c+cbar)/(3 pi^2)).  r = c = 1.  Tolerance fixed before the run: |quadrature - closed form|
<= 1e-25 (mpmath, 40 digits).  Run: ${PYTHON:-python3} rigor/council/c6_constants.py"""
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi
TOL = mp.mpf('1e-25')
def sym(f):  # integrand even in u; integrate over R, with the removable point u = 0 handled by splitting
    return 2 * mp.quad(f, [0, 1, 10, 100, mp.inf])
gB = (mp.mpf(2) / 3) * sym(lambda u: mp.tanh(u / 2) / (u * (u**2 + 4 * pi**2)))
gKM = (mp.mpf(1) / 3) * sym(lambda u: 1 / (u**2 + 4 * pi**2))
h2 = (mp.mpf(1) / 6) * sym(lambda u: mp.tanh(u / 4) / (u * (u**2 + 4 * pi**2)))
aux = mp.quad(lambda k: mp.tanh(pi * k) / (k * (k**2 + 1)), [0, 1, 10, mp.inf])
rows = [('g_B', gB, 2 / (3 * pi**2)), ('g_KM', gKM, mp.mpf(1) / 6), ('h2', h2, mp.log(2) / (6 * pi**2)),
        ('int tanh(pi k)/(k(k^2+1)) dk', aux, mp.mpf(2)), ('f2 = g_B/8', gB / 8, 1 / (12 * pi**2)),
        ('h2 / f2', h2 / (gB / 8), 2 * mp.log(2)), ('8 f2 (both chiralities, c = cbar = 1)', gB, 2 / (3 * pi**2))]
for name, q, cf in rows:
    print(f'{name:40s} quad = {mp.nstr(q, 20):>26s} closed = {mp.nstr(cf, 20):>26s} |diff| = {mp.nstr(abs(q - cf), 3):>8s} ok: {abs(q - cf) <= TOL}')
print('f2 to 8 digits:', mp.nstr(1 / (12 * pi**2), 8), '(paper: 0.00844343)')
print('4/0.616 =', mp.nstr(mp.mpf(4) / mp.mpf('0.616'), 4), '; 4/0.71 =', mp.nstr(mp.mpf(4) / mp.mpf('0.71'), 4), '(paper: "at least 5.6")')
