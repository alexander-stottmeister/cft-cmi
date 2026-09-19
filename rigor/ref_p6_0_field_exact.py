"""REF-P6-0: EXACT (rational) check of the modular-frame first-order field identity of
rigor/phase6_brief.md "MODULAR FRAME of I".  The earlier float test lost precision when x -> p.

Claim: the sigma-derivative at sigma=0 of h(x) = p + (x-p)/(1+sigma(x-p)), pushed to the
modular coordinate y = log((x-p_1)/(p_{n+1}-x)), is  zeta * w(y-y_p) d/dy  with
w(u) = -4 sinh^2(u/2) and zeta = sigma * beta_I(p), beta_I(x) = (x-p_1)(p_{n+1}-x)/T.

Equivalent rational identity (X = (x-p_1)/(p_{n+1}-x), X_p likewise):
     -(x-p)^2 / beta_I(x)  ==  -beta_I(p) * (X/X_p - 2 + X_p/X).
"""
from fractions import Fraction as F
import random
random.seed(1)

def rat(lo, hi):
    return F(random.randint(lo, hi), random.randint(1, 12))

bad = 0
for _ in range(50000):
    p1 = rat(-40, 0)
    T = rat(1, 60)
    if T <= 0: continue
    pn = p1 + T
    p = p1 + T * F(random.randint(1, 99), 100)
    x = p1 + T * F(random.randint(1, 99), 100)
    if x == p: continue
    bI = lambda t: (t - p1) * (pn - t) / T
    X = (x - p1) / (pn - x); Xp = (p - p1) / (pn - p)
    lhs = -(x - p) ** 2 / bI(x)
    rhs = -bI(p) * (X / Xp - 2 + Xp / X)
    if lhs != rhs:
        bad += 1
print("exact rational identity  -(x-p)^2/beta_I(x) == -beta_I(p)(X/X_p - 2 + X_p/X):",
      "PASS (0 failures / 50000)" if bad == 0 else "**FAIL** %d failures" % bad)

# and -4 sinh^2(u/2) = -(e^u - 2 + e^{-u}) with e^u = X/X_p   (float sanity, away from u=0)
import numpy as np
w = lambda u: -4 * np.sinh(u / 2) ** 2
u = np.linspace(-6, 6, 25); u = u[np.abs(u) > 1e-6]
print("w(u) = -(e^u - 2 + e^{-u}) max err:", float(np.max(np.abs(w(u) + (np.exp(u) - 2 + np.exp(-u))))))

# Theorem A case, exact: I=(-a,L), p=0, sigma=s/L  =>  zeta = a s/(a+L)
bad = 0
for _ in range(5000):
    a = rat(1, 50); L = rat(1, 50); s = rat(1, 30)
    if a <= 0 or L <= 0: continue
    if (s / L) * (a * L / (a + L)) != a * s / (a + L): bad += 1
print("zeta = sigma*beta_I(0) = a s/(a+L) for I=(-a,L):",
      "PASS" if bad == 0 else "**FAIL** %d" % bad)

# the (-1)-density law sigma' = sigma/M'(p) used in the brief's derivation, checked on
# a random Moebius change of coordinate M (float).
rng = np.random.default_rng(3)
err = 0.0
for _ in range(200):
    A, B, Cc, Dd = rng.normal(size=4)
    if abs(A * Dd - B * Cc) < 1e-3: continue
    M = lambda t: (A * t + B) / (Cc * t + Dd)
    Mp = lambda t: (A * Dd - B * Cc) / (Cc * t + Dd) ** 2
    p = rng.uniform(-1, 1); sig = 1e-6
    h = lambda t: p + (t - p) / (1 + sig * (t - p))
    # conjugated map in the M-coordinate; its parabolic parameter read off at first order
    x = p + rng.uniform(0.1, 0.5)
    lhs = M(h(x)) - M(x)                       # ~ -sigma' (M(x)-M(p))^2
    sigp = -lhs / (M(x) - M(p)) ** 2
    err = max(err, abs(sigp - sig / Mp(p)) / (sig / abs(Mp(p))))
print("parabolic parameter is a (-1)-density, sigma' = sigma/M'(p):  max rel err %.2e" % err)
