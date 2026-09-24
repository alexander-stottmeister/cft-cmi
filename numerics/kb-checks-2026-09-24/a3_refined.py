# FIX-TAIL, 2026-09-24. Check of A_3 = sup_{0<zeta<=1} zeta^-2 ||(g2)'''||_{L1(0,inf)} of rigor/tail_bound.tex
# (thm:tau, l.326; value claimed at l.749-751 from rigor/pt_tailconst.py: A_3 <= 0.036 "monotone decreasing in zeta").
# Needs mpmath (like rigor/pt_tailconst.py). Runtime about 4 minutes.
# (1) The ORIGINAL functions of rigor/pt_tailconst.py (g_ge2 by mp.quad, 4-point third difference with h=1e-3,
#     trapezoid of |g2'''| on the script's grid t = 0.05..40) at more zeta: the values rise as zeta -> 0, so the
#     supremum is the limit zeta -> 0, which the script does not sample.
# (2) That limit in closed form: g_ge2(t,z)/z^2 -> g0(t) = -2 B^-3 int_0^1 A^2 ds with A = sinh(ts/2) sinh(t(1-s)/2),
#     B = sinh(t/2), and int_0^1 A^2 ds = (1 + cosh(t)/2 - (3/2) sinh(t)/t)/4, so
#     g0(t) = -(1 + cosh(t)/2 - 1.5 sinh(t)/t) / (2 sinh(t/2)^3) = -t/30 + O(t^3).
#     ||g0'''||_1 on the script's grid and on refined grids.
# (3) Finite zeta on a refined grid (original g_ge2): all values stay below the zeta -> 0 limit.
import mpmath as mp
mp.mp.dps = 30

def g_ge2(t, z):                       # verbatim from rigor/pt_tailconst.py
    if t == 0: return mp.mpf(0)
    B = mp.sinh(t/2)
    f = lambda s: (lambda A: -2*z**2*A**2/(B**2*(B+2*z*A)))(mp.sinh(t*s/2)*mp.sinh(t*(1-s)/2))
    return mp.quad(f, [0, mp.mpf(1)/2, 1])

def g0(t):
    t = mp.mpf(t)
    return -(1 + mp.cosh(t)/2 - mp.mpf(3)/2*mp.sinh(t)/t)/(2*mp.sinh(t/2)**3)

def d3(F, t, h): return (F(t+2*h) - 2*F(t+h) + 2*F(t-h) - F(t-2*h))/(2*h**3)

def trap_abs(F, ts, h):
    tot = mp.mpf(0); prev = None
    for t in ts:
        v = abs(d3(F, t, h))
        if prev is not None: tot += (v + prev[1])/2*(t - prev[0])
        prev = (t, v)
    return tot

def script_grid():                     # the t-grid of rigor/pt_tailconst.py
    return [mp.mpf(x)/20 for x in range(1, 20)] + [1 + mp.mpf(x)/4 for x in range(0, 40)] + [11 + mp.mpf(x) for x in range(0, 30)]

def uniform(a, b, n):
    a = mp.mpf(a); b = mp.mpf(b); return [a + (b - a)*i/n for i in range(n + 1)]

print("(0) closed form against the original integrand: g_ge2(t,1e-8)/1e-16 vs g0(t)")
for t in ('0.3', '2', '10'):
    t = mp.mpf(t)
    print("    t=%-4s %s  %s" % (mp.nstr(t, 3), mp.nstr(g_ge2(t, mp.mpf('1e-8'))/mp.mpf('1e-16'), 10), mp.nstr(g0(t), 10)))
print("    g0(1e-6)/1e-6 = %s  (-1/30 = %s)" % (mp.nstr(g0(mp.mpf('1e-6'))/mp.mpf('1e-6'), 8), mp.nstr(-mp.mpf(1)/30, 8)))

print("(1) original functions and grid of rigor/pt_tailconst.py, h=1e-3")
for z in ('1e-4', '1e-3', '0.01', '0.05', '0.2', '0.5', '1.0'):
    zz = mp.mpf(z)
    print("    z=%-5s zeta^-2 ||g2'''||_1 = %s" % (z, mp.nstr(trap_abs(lambda t: g_ge2(t, zz), script_grid(), mp.mpf('1e-3'))/zz**2, 6)), flush=True)
print("    zeta->0 limit (g0) on the same grid: %s" % mp.nstr(trap_abs(g0, script_grid(), mp.mpf('1e-3')), 6))

print("(2) zeta->0 limit ||g0'''||_1 on refined grids, h=1e-4")
for (a, b, n) in (('0.002', 80, 20000), ('0.002', 80, 40000), ('0.0005', 120, 40000)):
    print("    t=%s..%s, %d intervals: %s" % (a, b, n, mp.nstr(trap_abs(g0, uniform(a, b, n), mp.mpf('1e-4')), 7)), flush=True)
print("    |g0'''| near t=0: %s at t=0.0005, so (0,0.0005) adds about %s" % (
      mp.nstr(abs(d3(g0, mp.mpf('0.0005'), mp.mpf('1e-4'))), 6), mp.nstr(mp.mpf('0.0005')*abs(d3(g0, mp.mpf('0.0005'), mp.mpf('1e-4'))), 3)))

print("(3) finite zeta, original g_ge2, refined grid t=0.002..80 with 1000 intervals, h=1e-4")
ts = uniform('0.002', 80, 1000)
print("    zeta->0 limit (g0) on this grid: %s" % mp.nstr(trap_abs(g0, ts, mp.mpf('1e-4')), 7))
for z in ('0.01', '0.05', '0.2', '1.0'):
    zz = mp.mpf(z)
    print("    z=%-5s zeta^-2 ||g2'''||_1 = %s" % (z, mp.nstr(trap_abs(lambda t: g_ge2(t, zz), ts, mp.mpf('1e-4'))/zz**2, 7)), flush=True)
print("A_3 = zeta->0 limit = 0.03721 (t from 0), so A_3 <= 0.0374 and C_2 = 4 pi A_3 <= 0.47; not certified")
