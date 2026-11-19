"""Council seat C1: independent recomputation of g_B = 2/(3 pi^2) (r = 1), the constant of Theorem A.
(a) 1-d integral of quadratic_limit.tex prop:gB: J = int tanh(u/2)/(u(u^2+4pi^2)) du, claimed (2/3) J = 2/(3pi^2).
(b) 2-d Fisher integral 2 iint |D1(k,k')|^2/N(k,k') dk dk' with the closed form of kernel_identity.tex (abstract):
    D1 = (q_k - q_k')(k+k')/[(k-k')((k-k')^2+4pi^2)], q_k = 1/(1+e^k), N = q_k(1-q_k')+q_k'(1-q_k).
(c) |D1(k,k')| at sample points by DIRECT quadrature of the modular-frame kernel of quadratic_limit.tex def:D1,
    Dt(x,x') = -(i/2pi) sinh(x/2) sinh(x'/2)/sinh^2((x-x')/2) for x<0<x', adjoint kernel on the other block,
    modes psi_k(x) = e^{i k x/2pi}/(2pi): independent of the kernel identity (no digamma, no contour).
Tolerances fixed before the run: (a),(b) relative 1e-8; (c) relative 2e-4 (truncated 2-d oscillatory quadrature).
Run from the cft_cmi root: ${PYTHON:-python3} rigor/council/c1_gB.py > rigor/council/c1_gB.out"""
import numpy as np
from mpmath import mp, mpf, quad, tanh, pi, inf
from scipy import integrate
mp.dps = 25
target = 2/(3*pi**2)
# validation (exactly known case): int_0^inf tanh(u/2)/u * 0 ... use int_R 1/(u^2+4pi^2) du = 1/2
v = quad(lambda u: 1/(u**2+4*pi**2), [-inf, 0, inf]); print("validation int 1/(u^2+4pi^2) =", v, "exact 0.5, dev", abs(v-mpf(1)/2))
J = 2*quad(lambda u: tanh(u/2)/(u*(u**2+4*pi**2)), [0, 1, 10, 100, inf])
print("(a) J =", J, " 1/pi^2 =", 1/pi**2, " rel dev", abs(J*pi**2-1), "PASS" if abs(J*pi**2-1) < 1e-8 else "FAIL")
q = lambda k: 1/(1+np.exp(k))
def D1(k, kp):
    u = k-kp
    if abs(u) < 1e-7:  # limit u->0: (q_k-q_k')/u -> q'(k) = -q(1-q)
        return -q(k)*(1-q(k))*(k+kp)/(4*np.pi**2)
    return (q(k)-q(kp))*(k+kp)/(u*(u**2+4*np.pi**2))
# (b) in mpmath (u = k-k', v = k+k', dk dk' = du dv/2; eq:NWuv of quadratic_limit.tex; even in u and v).
# History: a scipy box [0,120]^2 missed 6.9e-4 (u-tail decays like u^-3), scipy nested quad to inf gave 6.6e-7
# (quadrature accuracy); the mpmath nested quadrature below is the reported route.
from mpmath import cosh, sinh
def inner(u):
    f = lambda v: tanh(u/2)*sinh(u/2)/(cosh(v/2)+cosh(u/2)) * v**2/(u**2*(u**2+4*pi**2)**2)
    return quad(f, [0, u/2+1, u+20, inf])
gB2 = 2*4*mpf('0.5')*quad(inner, [0, 1, 5, 20, 100, 1000, inf]); rel = abs(gB2/target-1)
print(f"(b) 2 iint D1^2/N = {mp.nstr(gB2,18)}  target 2/(3pi^2) = {mp.nstr(target,18)}  rel dev {mp.nstr(rel,3)}", "PASS" if rel < 1e-8 else "FAIL")
def D1_direct(k, kp, X=70.0):
    # A x D block: x<0<x'; matrix element <psi_k, Dt psi_k'> = (2pi)^-2 iint e^{-ikx/2pi} Dt(x,x') e^{ik'x'/2pi}
    K = lambda x, xp: np.sinh(x/2)*np.sinh(xp/2)/np.sinh((x-xp)/2)**2
    def blk(k, kp, part):
        f = lambda xp, x: K(x, xp)*(np.cos if part == 'c' else np.sin)((kp*xp-k*x)/(2*np.pi))
        return integrate.dblquad(f, -X, 0, lambda x: 0, lambda x: X, epsabs=1e-12, epsrel=1e-10)[0]
    # block 1 (x<0<x'): -(i/2pi) K e^{i(k'x'-kx)/2pi}
    c1, s1 = blk(k, kp, 'c'), blk(k, kp, 's')
    b1 = -1j/(2*np.pi)*(c1+1j*s1)
    # block 2 (x'<0<x): conj of Dt(x',x) -> +(i/2pi) K(x',x); swap names: integrate over x'<0<x
    c2, s2 = blk(kp, k, 'c'), blk(kp, k, 's')   # gives iint_{x'<0<x} K(x',x) e^{i(k x - k' x')/2pi}
    b2 = 1j/(2*np.pi)*(c2-1j*s2)   # exponent -i(k x - k' x')/2pi with x>0>x'
    return (b1+b2)/(2*np.pi)**2
for (k, kp) in [(1.0, -2.0), (3.0, 0.5), (-4.0, 2.0)]:
    d = D1_direct(k, kp); c = D1(k, kp); rel = abs(abs(d)/abs(c)-1)
    print(f"(c) k={k:+.1f} k'={kp:+.1f}: |direct| = {abs(d):.8e}  |closed| = {abs(c):.8e}  phase(direct) = {np.angle(d):+.4f}  rel dev {rel:.1e}", "PASS" if rel < 2e-4 else "FAIL")
