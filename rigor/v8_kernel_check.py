#!/usr/bin/env python
"""V8 independent check of the kernel identity of rigor/kernel_identity.tex.

D^(1)(kappa,kappa') is computed from its DEFINING double integral, literally as
written in universality_normalization.tex eq. (D1-kernel) [= note's (10)]:

  Dtil(xi,xi') = -(i/2pi) sinh(xi/2) sinh(xi'/2) / sinh^2((xi-xi')/2)   for xi<0<xi'
               = conj( Dtil(xi',xi) )                                   for xi'<0<xi
               = 0                                                      otherwise
  psi_kappa(xi) = (1/2pi) e^{i kappa xi /2pi}
  D1(k,k') = int int dxi dxi'  conj(psi_k(xi)) Dtil(xi,xi') psi_k'(xi')

No use is made of P3's R, rho, J, series, or of p3_check.py.  Each block is
integrated in the "polar" chart t>0, x in (0,1) which removes the corner
(0,0) direction-dependence:  block1: (xi,xi')=(-t x, t(1-x));
block2: (xi,xi')=(t(1-x), -t x); Jacobian t in both cases.
"""
import mpmath as mp

mp.mp.dps = 25
PI = mp.pi
I = mp.mpc(0, 1)


def Dtil_AD(xi, xip):
    """note eq.(10) verbatim, valid for xi<0<xi'."""
    return -(I / (2 * PI)) * mp.sinh(xi / 2) * mp.sinh(xip / 2) / mp.sinh((xi - xip) / 2) ** 2


def integrand(t, x, kap, kapp, block):
    if block == 1:                      # xi<0<xi'
        xi, xip = -t * x, t * (1 - x)
        K = Dtil_AD(xi, xip)
    else:                               # xi'<0<xi : adjoint block
        xi, xip = t * (1 - x), -t * x
        K = mp.conj(Dtil_AD(xip, xi))
    phase = mp.e ** (I * (-kap * xi + kapp * xip) / (2 * PI))
    return t * phase * K / (2 * PI) ** 2


def D1_direct(kap, kapp):
    """Literal 2-D quadrature of the defining integral, polar chart."""
    tot = mp.mpc(0)
    for block in (1, 2):
        f = lambda t: mp.quad(lambda x: integrand(t, x, kap, kapp, block), [0, 1],
                              method='gauss-legendre', maxdegree=5)
        tot += mp.quad(f, [0, 2, 8, 25, 70, mp.inf], maxdegree=7)
    return tot


def q(k):
    return 1 / (1 + mp.e ** k)


def ghat(k):
    return -2 * I / (k * (k ** 2 + 1))


def gfrak(kap, kapp):
    return ghat((kap - kapp) / (2 * PI)) * (kap + kapp) / (4 * PI) / (2 * PI) ** 2


def rhs_factorized(kap, kapp):
    return I * (q(kap) - q(kapp)) * gfrak(kap, kapp)


def rhs_closed(kap, kapp):
    u, v = kap - kapp, kap + kapp
    return (q(kap) - q(kapp)) * v / (u * (u ** 2 + 4 * PI ** 2))


def rhs_third(kap, kapp):
    u, v = kap - kapp, kap + kapp
    return -v * mp.sinh(u / 2) / (u * (u ** 2 + 4 * PI ** 2) * (mp.cosh(v / 2) + mp.cosh(u / 2)))


def rhs_diag(kap):
    return -kap / (8 * PI ** 2 * mp.cosh(kap / 2) ** 2)



import random
random.seed(20260905)
PTS = [(mp.mpf(round(random.uniform(-6,6),4)), mp.mpf(round(random.uniform(-6,6),4))) for _ in range(5)]
print("V8 independent verification of the kernel identity, mp.dps =", mp.mp.dps)
print("D1 from the LITERAL defining double integral of Note 7 eq.(10) (polar chart, GL x tanh-sinh)")
print("="*104)
worst = mp.mpf(0); worstrel = mp.mpf(0)
for (a,b) in PTS:
    lhs = D1_direct(a,b); r1 = rhs_factorized(a,b); r2 = rhs_closed(a,b); r3 = rhs_third(a,b)
    e1=abs(lhs-r1); e2=abs(r1-r2); e3=abs(r2-r3); worst=max(worst,e1); worstrel=max(worstrel,e1/abs(r1))
    print(f"kappa={mp.nstr(a,6):>9s}  kappa'={mp.nstr(b,6):>9s}")
    print(f"   direct  = {mp.nstr(lhs,20)}")
    print(f"   i(q-q')g= {mp.nstr(r1,20)}")
    print(f"   |direct-factorized|={mp.nstr(e1,4)}  |Im direct|={mp.nstr(abs(mp.im(lhs)),4)}"
          f"  |fact-closed|={mp.nstr(e2,4)}  |closed-third|={mp.nstr(e3,4)}")
print("="*104)
for a in (mp.mpf('1.3'), mp.mpf('-2.7'), mp.mpf(0)):
    lhs = D1_direct(a,a); rd = rhs_diag(a); e=abs(lhs-rd); worst=max(worst,e)
    print(f"DIAGONAL kappa={mp.nstr(a,5):>7s}: direct={mp.nstr(lhs,20):>26s}  -k/(8pi^2cosh^2)="
          f"{mp.nstr(rd,20):>26s}  err={mp.nstr(e,4)}")
eps = mp.mpf('1e-5'); a = mp.mpf(2)
l = D1_direct(a,a-eps); print(f"NEAR-DIAG (2, 2-1e-5): direct={mp.nstr(l,18)}  closed={mp.nstr(rhs_closed(a,a-eps),18)}"
      f"  err={mp.nstr(abs(l-rhs_closed(a,a-eps)),4)}")
a=mp.mpf('1.7'); l=D1_direct(a,-a)
print(f"ANTIDIAG (1.7,-1.7) [v=0]: direct={mp.nstr(l,10)}  predicted 0")
print("="*104); print("WORST ABS ERROR:", mp.nstr(worst,6), "  WORST REL ERROR:", mp.nstr(worstrel,6))
