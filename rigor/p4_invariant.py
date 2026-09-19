#!/usr/bin/env python
"""P4b: x-space (Mellin-in-u) check of the invariant formula of Note 7.

Geometry: A=(-inf,0), D=(0,L), I=(-inf,L).  Put u = L-x > 0 on I.
Modular dilation about L:  u -> e^{2 pi t} u   (xi = -log(u/L) -> xi - 2 pi t).
Reflection J: x -> 2L-x, i.e. u -> -u.

Weight-2 densities: Ttilde(xi) = beta^2 T(x), beta = dx/dxi = L-x = u.
<T(x)T(y)> = (c/8 pi^2) (x-y-i0)^{-4} and x-y = u'-u, so the x-space kernel is
   K(u,u') = u^2 u'^2 (c/8 pi^2) (u'-u-i0)^{-4}.
NOTHING below uses the xi-frame thermal form (c/128 pi^2) sinh^{-4}(u/2).
All computations are done with L=1 (everything is homogeneous of degree 0).
"""
import mpmath as mp
mp.mp.dps = 30
PI = mp.pi

# ---------------------------------------------------------------- part 0
# Mellin transform  M[F](s) = int_0^inf u^{s-1} F(u) du   evaluated at s = i k
# equals the xi-Fourier transform  int e^{-i k xi} F du/u ... (see doc).
def mellin_ray(F, s, phi=mp.mpf('0.6')):
    """int_0^inf u^{s-1} F(u) du along the ray u = t e^{i phi} (t: 0->inf).
    Valid when F is analytic off the real axis singularities that the ray
    passes above, and the arcs at 0 and infinity vanish."""
    e = mp.e**(1j*phi)
    f = lambda t: (t*e)**(s-1) * F(t*e) * e
    return mp.quad(f, [0, 1, mp.inf])

# ---------------------------------------------------------------- part 1
# Whatx(k) := int_0^inf u^{1+ik} (u-1+i0)^{-4} du * c/(8 pi^2)   [c=1]
# because  (1-u-i0)^{-4} = (u-1+i0)^{-4}  (even integer power).
def What_xspace(k):
    s = 2 + 1j*k                      # u^{s-1} = u^{1+ik}
    K = lambda u: (u - 1)**(-4)       # ray with Im u > 0 realises the +i0
    return mellin_ray(K, s) / (8*PI**2)

def What_note(k):
    k = mp.mpf(k) if not isinstance(k, mp.mpf) else k
    return k*(k**2+1) / (mp.e**(2*PI*k) - 1) / (24*PI)

print("="*74)
print("(1) x-space Mellin transform of  (c/8pi^2)(u'-u-i0)^{-4}  vs  What(k)")
print("    What(k) = (c/24pi) k(k^2+1)/(e^{2pi k}-1)      [c = 1]")
print("="*74)
print(f"{'k':>7} {'Mellin (x-space), Re':>26} {'Im':>12} {'note What(k)':>22} {'rel.err':>10}")
for k in [mp.mpf('-1.7'), mp.mpf('-0.5'), mp.mpf('0.3'), mp.mpf('1.0'), mp.mpf('2.5')]:
    a = What_xspace(k); b = What_note(k)
    rel = abs(a-b)/abs(b)
    print(f"{float(k):7.2f} {mp.nstr(a.real,14):>26} {mp.nstr(a.imag,3):>12} "
          f"{mp.nstr(b,14):>22} {float(rel):10.2e}")

# KMS asymmetry, checked on the x-space Mellin transform itself
print()
print("    KMS asymmetry  What(-k) = e^{2 pi k} What(k), from x-space only:")
for k in [mp.mpf('0.3'), mp.mpf('1.0'), mp.mpf('2.5')]:
    lhs = What_xspace(-k); rhs = mp.e**(2*PI*k)*What_xspace(k)
    print(f"      k={float(k):4.1f}  What(-k)={mp.nstr(lhs.real,12):>18}  "
          f"e^(2pik)What(k)={mp.nstr(rhs.real,12):>18}  rel={float(abs(lhs-rhs)/abs(lhs)):.2e}")

# Dilation is diagonalised by the Mellin transform: check numerically on a
# test density.  (delta_t F)(u) := F(e^{-2 pi t} u);  M[delta_t F](s)
# = e^{2 pi t s} M[F](s), a pure PHASE at s = i k.  This is the statement
# that log(u) -conjugated dilations are translations, diagonalised by Fourier.
print()
print("    Mellin diagonalises the dilation:  M[F(e^{-2pi t}.)](ik)/M[F](ik) "
      "= e^{2 pi i k t}?")
Ftest = lambda u: u**2/(1+u)**5          # decays, Mellin strip contains Re s=0
for (k, t) in [(mp.mpf('0.7'), mp.mpf('0.31')), (mp.mpf('-1.3'), mp.mpf('0.5'))]:
    s = 1j*k
    num = mp.quad(lambda u: u**(s-1)*Ftest(u*mp.e**(-2*PI*t)), [0, 1, mp.inf])
    den = mp.quad(lambda u: u**(s-1)*Ftest(u), [0, 1, mp.inf])
    pred = mp.e**(2j*PI*k*t)
    print(f"      k={float(k):5.2f} t={float(t):4.2f}  ratio={mp.nstr(num/den,10)}"
          f"   e^(2pi i k t)={mp.nstr(pred,10)}   err={float(abs(num/den-pred)):.2e}")

# ---------------------------------------------------------------- part 2
# g in x-space.  On D, g(x) = f(x) = -x^2/L; with L=1 and u=1-x,
#   g(x) = -(1-u)^2 ,  gtilde = g/beta = -(1-u)^2/u   for 0<u<1 (xi>0), 0 else.
# ghat(k) = int_0^inf u^{ik} gtilde(u) du/u = -int_0^1 u^{ik-2}(1-u)^2 du,
# which DIVERGES at u=0 (gtilde ~ -1/u): the Mellin strip is Re s > 1 and we
# need s = ik.  Regularise with u^{eps} (convergent for eps>1) and continue.
def ghat_eps_quad(k, eps):
    s = 1j*k - 1 + eps                        # u^{s-1} = u^{ik-2+eps}
    return -mp.quad(lambda u: u**(s-1)*(1-u)**2, [0, 1])

def ghat_xspace(k, nodes=(mp.mpf('1.5'), mp.mpf('2'), mp.mpf('2.5'), mp.mpf('3'))):
    """1/ghat_eps is a CUBIC polynomial in eps, so Lagrange-interpolate the
    four quadrature values of 1/ghat_eps and evaluate the cubic at eps=0."""
    ys = [1/ghat_eps_quad(k, e) for e in nodes]
    tot = mp.mpc(0)
    for i, e in enumerate(nodes):                     # Lagrange at eps = 0
        L = mp.mpf(1)
        for j, e2 in enumerate(nodes):
            if i != j: L *= (0 - e2)/(e - e2)
        tot += ys[i]*L
    return 1/tot

def ghat_note(k):
    return -2j/(k*(k**2+1))

print()
print("="*74)
print("(2) x-space ghat by eps-continuation of the Mellin integral, vs -2i/(k(k^2+1))")
print("="*74)
print(f"{'k':>7} {'x-space ghat':>34} {'note ghat':>26} {'rel.err':>10}")
for k in [mp.mpf('-1.7'), mp.mpf('-0.5'), mp.mpf('0.3'), mp.mpf('1.0'), mp.mpf('2.5')]:
    a = ghat_xspace(k); b = ghat_note(k)
    print(f"{float(k):7.2f} {mp.nstr(a,12):>34} {mp.nstr(b,12):>26} "
          f"{float(abs(a-b)/abs(b)):10.2e}")

# ---------------------------------------------------------------- part 3
# The two metrics, from the x-space What and ghat ONLY.
#   g_B  = (1/pi)  int_R dk What |ghat|^2 w_B ,   w_B  = (e^{2pi k}-1)^2/(e^{2pi k}+1)
#   g_KM = (1/2pi) int_R dk What |ghat|^2 w_KM,   w_KM = (e^{2pi k}-1) * 2 pi k
# Both integrands are even; we integrate over k<0, where What is O(|k|^3) and
# the weights are O(1)/O(|k|) -- no catastrophic e^{2pi k} cancellation.
import time
mp.mp.dps = 22
# For k<0 both x-space Mellin transforms have STABLE representations, obtained
# by contour rotation, with no cancellation (see doc, Prop. 1.4):
#   What: rotate the ray BELOW the pole u=1 and add -2 pi i Res_{u=1}
#         = -(pi/3) k(k^2+1);  the remaining ray integral is O(e^{-|k phi|}).
#   ghat: put u = e^{-y} and rotate y = i r; then e^{r k} damps (k<0).
def What_xspace_neg(k):
    phi = mp.mpf('-0.6'); e = mp.e**(1j*phi); s = 2 + 1j*k
    ray = mp.quad(lambda t: (t*e)**(s-1)*(t*e-1)**(-4)*e, [0, 1, mp.inf])
    return (ray - (PI/3)*k*(k**2+1))/(8*PI**2)

def ghat_eps_rot(k, eps):
    return -1j*mp.quad(lambda r: mp.e**(r*k)*mp.e**(1j*r*(1-eps))
                       *(1-mp.e**(-1j*r))**2, [0, 2, 10, 60, mp.inf])

def ghat_xspace_neg(k, nodes=(mp.mpf('1.5'), mp.mpf(2), mp.mpf('2.5'), mp.mpf(3))):
    ys = [1/ghat_eps_rot(k, e) for e in nodes]; tot = mp.mpc(0)
    for i, e in enumerate(nodes):
        L = mp.mpf(1)
        for j, e2 in enumerate(nodes):
            if i != j: L *= (0 - e2)/(e - e2)
        tot += ys[i]*L
    return 1/tot

w_B  = lambda k: (mp.e**(2*PI*k)-1)**2/(mp.e**(2*PI*k)+1)
w_KM = lambda k: (mp.e**(2*PI*k)-1)*2*PI*k
_n = [0]
def ghat_neg(k):
    """rotated form for |k|>3 (fast); direct u-integral of part 2 otherwise
    (the e^{rk} damping of the rotated form is too slow near k=0)."""
    return ghat_xspace_neg(k) if abs(k) > 3 else ghat_xspace(k)

def core(k):
    _n[0] += 1
    return (What_xspace_neg(k) * abs(ghat_neg(k))**2).real

def gl(f, a, b, n=28):
    import numpy as np
    x, w = np.polynomial.legendre.leggauss(n)
    h, m = (b-a)/2, (a+b)/2
    return h*sum(mp.mpf(float(wi))*f(m + h*mp.mpf(float(xi))) for xi, wi in zip(x, w))

def tail(f, c, n=32):        # int_{-inf}^{c} f dk  via k = c/t, t in (0,1]
    return gl(lambda t: f(c/t)*(-c)/t**2, mp.mpf(0), mp.mpf(1), n)

t0 = time.time()
fB  = lambda k: core(k)*w_B(k)
fKM = lambda k: core(k)*w_KM(k)
IB  = (gl(fB, mp.mpf(-8), mp.mpf(-2), 22) + gl(fB, mp.mpf(-2), mp.mpf(0), 22)
       + tail(fB, mp.mpf(-8), 32))
IKM = (gl(fKM, mp.mpf(-8), mp.mpf(-2), 22) + gl(fKM, mp.mpf(-2), mp.mpf(0), 22)
       + tail(fKM, mp.mpf(-8), 32))
gB, gKM = 2*IB/PI, IKM/PI
print()
print("="*74)
print("(3) metrics assembled from the x-space ingredients (c = 1)")
print("="*74)
print(f"    g_B  (x-space) = {mp.nstr(gB,12):>18}   2c/(3 pi^2) = "
      f"{mp.nstr(2/(3*PI**2),12):>18}   rel = {float(abs(gB-2/(3*PI**2))*3*PI**2/2):.2e}")
print(f"    g_KM (x-space) = {mp.nstr(gKM,12):>18}   c/6         = "
      f"{mp.nstr(mp.mpf(1)/6,12):>18}   rel = {float(abs(gKM-mp.mpf(1)/6)*6):.2e}")
print(f"    f_2 = g_B/8    = {mp.nstr(gB/8,12):>18}   c/(12 pi^2) = "
      f"{mp.nstr(1/(12*PI**2),12):>18}")
print(f"    s_2 = g_KM/2   = {mp.nstr(gKM/2,12):>18}   c/12        = "
      f"{mp.nstr(mp.mpf(1)/12,12):>18}")
print(f"    s_2/f_2        = {mp.nstr((gKM/2)/(gB/8),12):>18}   pi^2 = {mp.nstr(PI**2,12)}")
print(f"    [{_n[0]} integrand evaluations, {time.time()-t0:.1f} s]")
