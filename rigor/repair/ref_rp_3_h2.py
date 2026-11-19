"""REF-RP-3: independent quadrature of h2 = (r/2) iint |D1(k,k')|^2 / W(k,k') dk dk' (r = 1), with
D1 = (q_k - q_k') v / (u (u^2 + 4 pi^2))  (kernel_identity.tex thm:main, middle member), u = k - k', v = k + k',
q_k = 1/(1+e^k), W = (sqrt(q_k(1-q_k')) + sqrt(q_k'(1-q_k)))^2 (quadratic_limit.tex eq:NW) -- built from q directly,
NOT from the (u,v) identities eq:NWuv or Lemma V used by the document.  Tolerance fixed before the run: 1e-10 relative.
Run: ${PYTHON:-python3} rigor/repair/ref_rp_3_h2.py > rigor/repair/ref_rp_3_h2.out"""
import mpmath as mp
from scipy.integrate import quad
from scipy.special import expit
import numpy as np
mp.mp.dps = 30
TOL = 1e-10
q = lambda k: expit(-k)          # 1/(1+e^k), overflow-safe, float64
def integrand(u, v):          # dk dk' = (1/2) du dv
    k, kp = (v+u)/2, (v-u)/2
    qk, qkp = q(k), q(kp)
    W = (np.sqrt(qk*expit(kp)) + np.sqrt(qkp*expit(k)))**2
    if u == 0 or not (qk > 0 or qkp > 0) or (qk == qkp): return 0.0
    D1 = (qk - qkp)*v/(u*(u**2 + 4*np.pi**2))
    return D1**2/W/2 if W > 1e-300 else 0.0
# validation: the same code with W -> N reproduces g_B/8 = 1/(12 pi^2) via g_B = 2 iint |D1|^2/N (const-gb, r = 1)
def integrandN(u, v):
    k, kp = (v+u)/2, (v-u)/2
    qk, qkp = q(k), q(kp)
    N = qk*expit(kp) + qkp*expit(k)
    if u == 0 or not (qk > 0 or qkp > 0) or (qk == qkp): return 0.0
    D1 = (qk - qkp)*v/(u*(u**2 + 4*np.pi**2))
    return D1**2/N/2 if N > 1e-300 else 0.0
def dbl(f):   # integrand even in u and v: 4 x quadrant; inner v-range follows the ridge |v| ~ u (support ~ v < u + O(1))
    def inner(u):
        pts = [0, 0.5*u, u, u + 10, u + 40, u + 120]
        return sum(quad(lambda v: f(u, v), a, b, epsabs=0, epsrel=1e-13, limit=200)[0] for a, b in zip(pts[:-1], pts[1:])) \
            + quad(lambda v: f(u, v), u + 120, np.inf, epsabs=0, epsrel=1e-12, limit=200)[0]
    us = [1e-12, 0.5, 2, 2*np.pi, 20, 60, 200, 1000, 5000]
    tot = sum(quad(inner, a, b, epsabs=0, epsrel=1e-12, limit=200)[0] for a, b in zip(us[:-1], us[1:]))
    tail = quad(inner, us[-1], np.inf, epsabs=0, epsrel=1e-8, limit=200)[0]
    return 4*(tot + tail)
gB8 = 2*dbl(integrandN)/8
print("validation g_B/8 =", repr(gB8), " exact 1/(12 pi^2) =", mp.nstr(1/(12*mp.pi**2), 15),
      " rel.dev", '%.2e' % abs(gB8*12*np.pi**2 - 1))
h2 = dbl(integrand)/2          # h2 = (r/2) iint |D1|^2/W
ex = mp.log(2)/(6*mp.pi**2)
print("h2 (2D quadrature)        =", repr(h2))
print("r log2/(6 pi^2), r = 1    =", mp.nstr(ex, 15), " rel.dev", "%.2e" % abs(h2/float(ex) - 1), "OK" if abs(h2/float(ex)-1) < TOL else "FAIL")
I1 = 2*mp.quad(lambda u: mp.tanh(u/4)/(u*(u**2+4*mp.pi**2)), [0, 1, 2*mp.pi, 50, mp.inf])
print("(1/6) int tanh(u/4)/(u(u^2+4pi^2)) du =", mp.nstr(I1/6, 15), " rel.dev", mp.nstr(abs(I1/6/ex - 1), 3))
print("h2 / f2 =", repr(h2*12*np.pi**2), " 2 log 2 =", mp.nstr(2*mp.log(2), 12))
