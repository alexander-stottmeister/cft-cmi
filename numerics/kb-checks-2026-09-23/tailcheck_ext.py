# AUTH-CFT-B, 2026-09-23. Extension of REF-DEP-CFT-B2's tailcheck.py (same folder); stdlib only.
# Target: rigor/tail_bound.tex, Cor. 5.2 (cor:rate, l. 502-529), claim eq:final
#   Phi - Phi_W <= 0.173 z^2/k + 0.88 z^2/k^2   (z = zeta, k = kappa_c)
# on the admissible region k >= 10 and k >= kdag(z) = 2 log(1/z) + 2 log(1+k) + 3.
# Inputs taken as given (they are the weak links, not checked here): Thm 4.2 (thm:tau) eq:taunu with
# A_1 <= 2.0, A_3 <= 0.036, i.e. T <= 2z^2/(3k^2) + 4.6 z^2/k^3 + (12 + 0.51 z (1+k)) e^{-k};
# Thm 5.1 (thm:main) eq:Psi: Phi - Phi_W <= Pd + y/(1-y), Pd <= T/(2(1-T)), y = 2 e^{2 Pd} sqrt(Phi Pd);
# and Phi <= f z^2.
import math

def T_exact(z, k):
    return 2*z*z/(3*k*k) + 4.6*z*z/k**3 + (12 + 0.51*z*(1+k))*math.exp(-k)

def chain(z, k, f, T):
    Pd = T/(2*(1-T))
    y = 2*math.exp(2*Pd)*math.sqrt(f*z*z*Pd)
    return Pd + y/(1-y)

def claim(z, k):
    return 0.173*z*z/k + 0.88*z*z/(k*k)

def admissible(z, k):
    return k >= 10 and k >= 2*math.log(1/z) + 2*math.log(1+k) + 3

zs = sorted(set([i/2000 for i in range(1, 2001)] + [10**(-e/10) for e in range(1, 81)]))  # (0,1] linear + 1e-8..1 log
ks = [10 + j*0.02 for j in range(0, 2001)] + [50 + j*0.25 for j in range(1, 601)]           # 10..50 fine, 50..200 coarse
res = {"T/(z^2/k^2)": (0, None), "step l.521: 0.51 z(1+k)e^-k/(z^2/k^2)": (0, None),
       "exact-T chain / claim, f=0.0085": (0, None), "exact-T chain / claim, f=0.008516": (0, None),
       "crude T=1.75z^2/k^2 chain / claim, f=0.0085": (0, None)}
n = 0
for z in zs:
    for k in ks:
        if not admissible(z, k):
            continue
        n += 1
        s = z*z/(k*k)
        vals = {"T/(z^2/k^2)": T_exact(z, k)/s,
                "step l.521: 0.51 z(1+k)e^-k/(z^2/k^2)": 0.51*z*(1+k)*math.exp(-k)/s,
                "exact-T chain / claim, f=0.0085": chain(z, k, 0.0085, T_exact(z, k))/claim(z, k),
                "exact-T chain / claim, f=0.008516": chain(z, k, 0.008516, T_exact(z, k))/claim(z, k),
                "crude T=1.75z^2/k^2 chain / claim, f=0.0085": chain(z, k, 0.0085, 1.75*s)/claim(z, k)}
        for key, v in vals.items():
            if v > res[key][0]:
                res[key] = (v, (z, round(k, 2)))
print("admissible grid points:", n, "(z in (0,1] linear step 5e-4 plus log grid 1e-8..1; k in [10,200])")
for key, (v, at) in res.items():
    print(f"max {key:45s} = {v:.4f} at (z, k) = {at}")
print("claimed in l.521: 0.51 z(1+k)e^-k <= 0.003 z^2/k^2, i.e. ratio <= 0.003")
print("f bound from rate_of_remainder prop:rrr: sup_(0,1] -(1/2)log(1-2 f2 z^2)/z^2 =",
      -0.5*math.log(1 - 2*z*z/(12*math.pi**2))/(z*z) if (z := 1.0) else None,
      "; 2 sqrt(0.875*0.008516) =", 2*math.sqrt(0.875*0.008516))
