"""REF-RP-3: sign check of <J(f)J(g)> = (1/4pi^2) int_0^inf p conj(fhat) ghat dp, fhat(p) = int f e^{+ipx} dx,
given <J(x)J(y)> = -(1/4pi^2)(x-y-i0)^{-2}.  Tolerance fixed before the run: relative 1e-6.
Run: ${PYTHON:-python3} rigor/repair/ref_rp_3_fourier.py > rigor/repair/ref_rp_3_fourier.out"""
import numpy as np
from scipy.integrate import quad, dblquad
eps = 0.05                                   # regulator (x-y-i eps); the identity holds for each eps>0 with e^{-eps p}
f = lambda x: np.exp(-(x-0.3)**2)            # real test functions with known transforms
g = lambda x: (x+0.2)*np.exp(-(x+0.2)**2/2)
# position space: -(1/4pi^2) int int f(x) g(y) (x-y-i eps)^{-2}
def kern(y, x, part):
    v = -f(x)*g(y)/(x-y-1j*eps)**2/(4*np.pi**2); return v.real if part == 0 else v.imag
L = 9
pos = complex(*[dblquad(kern, -L, L, -L, L, args=(k,), epsabs=1e-12, epsrel=1e-10)[0] for k in (0, 1)])
def hat(h, p, sgn):
    re = quad(lambda x: h(x)*np.cos(p*x), -L, L, epsabs=1e-13)[0]; im = quad(lambda x: h(x)*np.sin(p*x), -L, L, epsabs=1e-13)[0]
    return re + 1j*sgn*im
def mom(sgn, conj_on):
    def integrand(p, part):
        fh, gh = hat(f, p, sgn), hat(g, p, sgn)
        v = (np.conj(fh)*gh if conj_on == 'f' else fh*np.conj(gh))*p*np.exp(-eps*p)/(4*np.pi**2)
        return v.real if part == 0 else v.imag
    return complex(*[quad(integrand, 0, 40, args=(k,), limit=400, epsabs=1e-13)[0] for k in (0, 1)])
print("validation: int_0^inf p e^{-ipu-eps p} dp vs -1/(u-i eps)^2 at u=0.7:",
      complex(quad(lambda p: p*np.cos(0.7*p)*np.exp(-eps*p), 0, 2000, limit=4000)[0], -quad(lambda p: p*np.sin(0.7*p)*np.exp(-eps*p), 0, 2000, limit=4000)[0]), -1/(0.7-1j*eps)**2)
print("position space              :", pos)
for sgn, name in [(+1, 'e^{+ipx}'), (-1, 'e^{-ipx}')]:
    for c in ('f', 'g'):
        m = mom(sgn, c); print(f"fhat={name}, conj on {c}hat : {m}   rel.dev {abs(m-pos)/abs(pos):.2e}  {'MATCH' if abs(m-pos)/abs(pos)<1e-6 else ''}")
