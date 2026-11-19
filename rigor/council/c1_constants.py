"""Council seat C1: independent recomputation of the constants of the Theorem-A cards.
Tolerance fixed before the run: TOL = 1e-10 (absolute) for closed forms; card values are compared at the
number of digits the card prints (half a unit in the last printed digit).
Run from the cft_cmi root: ${PYTHON:-python3} rigor/council/c1_constants.py > rigor/council/c1_constants.out
No discretisation, no regulator: every quantity is a closed form or a 1-d root of an analytic function (mpmath, 30 digits)."""
from mpmath import mp, mpf, pi, sqrt, log, findroot
mp.dps = 30
TOL = mpf('1e-10')
f2 = 1/(12*pi**2)
rows = []
def chk(name, val, card, half_ulp):
    ok = abs(val - mpf(card)) <= mpf(half_ulp)
    rows.append((name, val, card, ok)); print(f"{name:55s} {mp.nstr(val,12):>16s}  card {card:>10s}  {'OK' if ok else 'MISMATCH'}")
# validation (exactly known case): -(1/2)log(1-x) series at tiny x equals x/2 + x^2/4 to 1e-20
x = mpf('1e-8'); assert abs(-log(1-x)/2 - (x/2 + x**2/4)) < mpf('1e-23'); print("validation series OK")
chk("f2 = 1/(12 pi^2)", f2, "0.0084434", "5e-8")
chk("g_B/8 with g_B = 2/(3 pi^2)", (2/(3*pi**2))/8, "0.0084434", "5e-8")
chk("(4 f2)^(-1/2) = pi sqrt3", (4*f2)**-0.5, "5.44", "5e-3")
chk("(2 f2)^(-1/2) = pi sqrt6", (2*f2)**-0.5, "7.70", "5e-3")
g = lambda z: -log(1-2*f2*z**2)/2 - mpf('0.0085')*z**2
zc = findroot(g, mpf('0.88'))
chk("crossover -1/2 log(1-2 f2 z^2) = 0.0085 z^2", zc, "0.88681", "5e-6")
chk("ratio -1/2 log(1-2 f2)/1 at zeta=1", -log(1-2*f2)/2, "0.0085155", "5e-8")
chk("2 sqrt(0.875*0.008516)", 2*sqrt(mpf('0.875')*mpf('0.008516')), "0.1726", "5e-5")
chk("0.0085*0.8868^2", mpf('0.0085')*mpf('0.8868')**2, "6.68e-3", "5e-6")
chk("C2 = 4 pi A3 at A3=0.0374", 4*pi*mpf('0.0374'), "0.47", "5e-3")
chk("VWZ: 8 f2", 8*f2, "0.0676", "5e-5")
chk("VWZ: 2 f2", 2*f2, "0.0169", "5e-5")
# monotonicity of the ratio r(z) = -1/2 log(1-2f2 z^2)/z^2 on (0,1]: r = sum_k (2f2)^k z^(2k-2)/(2k), all terms >= 0
print("ratio increasing on (0,1]: power series with nonnegative coefficients -> yes (analytic, no sampling)")
print("ALL OK" if all(r[3] for r in rows) else "SOME MISMATCH")
