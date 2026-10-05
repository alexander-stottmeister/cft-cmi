#!/usr/bin/env python3
"""REF-P6-7: independent recomputation of the numbers quoted on the Phase 6 summary cards
(corner-correlation-kernel, network-second-order-law, vwz-protocol-ordering, phase6-plan).

Run from the repository root:  ${PYTHON:-python3} rigor/ref_p6_7_checks.py > rigor/ref_p6_7_checks.out
Tolerances fixed before the run: TOL_KERNEL = 6e-8 (cards print 7 decimals, rounding 5e-8 + margin);
TOL_SERIES = 1e-25 (closed form vs series, mpmath 40 digits); TOL_QUAD = 1e-12 (Fourier integral).
Methods: (i) the boxed closed form, (ii) the exponential series of thm:T4(cf), (iii) direct mpmath
quadrature of int rho(q) cos(q D) dq with rho(q) = tanh(pi q)/(48 pi^2 q (1+q^2)) -- no shared code
with rigor/g1b_kernel.py.  Validation first: Ghat(0) = 1/(12 pi^2) (thm:T4(b), exact) by (ii) and (iii).
"""
import os
import mpmath as mp

mp.mp.dps = 40
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TOL_KERNEL, TOL_SERIES, TOL_QUAD = 6e-8, mp.mpf('1e-25'), 1e-12
G0 = 1 / (12 * mp.pi**2)

def closed(D):
    D = abs(mp.mpf(D))
    return G0 * (mp.cosh(D/2) - mp.sinh(D/2)**2 * mp.log(mp.coth(D/4)))

def series(D):
    D = abs(mp.mpf(D))
    f = lambda n: mp.e**(-(n+mp.mpf(1)/2)*D) / ((n+mp.mpf(1)/2)*(1-(n+mp.mpf(1)/2)**2))
    return mp.nsum(f, [0, mp.inf]) / (24 * mp.pi**2)

def rho(q):
    return mp.mpf(1)/(48*mp.pi) if q == 0 else mp.tanh(mp.pi*q)/(48*mp.pi**2*q*(1+q**2))

def quad(D):
    D = mp.mpf(D)
    if D == 0:
        return 2*mp.quad(rho, [0, 1, 10, mp.inf])
    return 2*mp.quadosc(lambda q: rho(q)*mp.cos(q*D), [0, mp.inf], omega=D)

print("== A. validation: Ghat(0) = 1/(12 pi^2) exactly (thm:T4(b))")
s0, q0 = series(0), quad(0)
print("  series/G0 - 1 = %.2e   quad/G0 - 1 = %.2e   -> %s" % (s0/G0-1, q0/G0-1,
      "PASS" if abs(s0/G0-1) < TOL_SERIES and abs(q0/G0-1) < TOL_QUAD else "FAIL"))

print("== B. the nine values Ghat(D)/Ghat(0) quoted on corner-correlation-kernel")
card = {0.5: 0.8983866, 1: 0.7456151, 1.5: 0.6007454, 2: 0.4769603, 3: 0.2945231,
        4: 0.1797843, 5: 0.1092990, 6: 0.0663498, 8: 0.0244192}
worst = 0
for D, v in card.items():
    c, s, q = closed(D)/G0, series(D)/G0, quad(D)/G0
    x = mp.e**(-mp.mpf(D)/2)
    lo, hi = x*(4-x**2)/3, 4*x/3          # thm:T4(d) divided by Ghat(0)
    worst = max(worst, abs(c - v))
    print("  D=%-4s closed %.10f  |cl-ser| %.1e  |cl-quad| %.1e  card %.7f  |diff| %.1e  bounds %s"
          % (D, c, abs(c-s), abs(c-q), v, abs(c-v), "ok" if lo <= c <= hi else "VIOLATED"))
print("  max |closed - card| = %.2e  (tol %.0e) -> %s" % (worst, TOL_KERNEL, "PASS" if worst < TOL_KERNEL else "FAIL"))

print("== C. VWZ symmetric setup (b = 1, a = 2 eta/(1-eta)); zeta's of cor:vwz step <1>1")
for eta in [0.05, 0.1, 0.15, 0.2, 0.3, 0.4]:
    eta = mp.mpf(eta); a = 2*eta/(1-eta); b = 1
    z1, z2, z3, zeff = a/b, a*(a+2*b)/(2*b*(a+b)), a/b, 2*a/b
    S = closed(mp.log(1/eta))/G0
    print("  eta=%.2f z1=%.4f z2=%.4f z3=%.4f zeff=%.4f  S(log 1/eta)=%.5f  in [%.5f, %.5f]  Ghat-free part %.3f"
          % (eta, z1, z2, z3, zeff, S, mp.sqrt(eta)*(4-eta)/3, 4*mp.sqrt(eta)/3, (z2**2+z3**2)/z1**2))
X, S20 = mp.mpf('0.28140'), closed(mp.log(20))/G0
for u in ['0.0045', '0.0044', '0.005']:
    print("  eta=0.05: (S - X)/u with X = 0.28140, u = %s : %.2f" % (u, (S20-X)/mp.mpf(u)))
print("  8 f2/c = 8/(12 pi^2) = %.5f ;  pi*sqrt(3) = %.5f" % (8*G0, mp.pi*mp.sqrt(3)))

print("== D. numerics/networks/N4.out: extrapolated Phi_tot/Sstep per chain")
lines = open(os.path.join(ROOT, 'numerics', 'networks', 'N4.out')).read().splitlines()
vals = []
for i, l in enumerate(lines):
    if l.strip().startswith('Phi_tot/Sstep'):
        for m in lines[i+1:i+8]:
            if '=> extrapolated' in m:
                vals.append(float(m.split()[2])); break
print("  values:", ", ".join("%.4f" % v for v in vals), " -> range %.4f ... %.4f" % (min(vals), max(vals)))
