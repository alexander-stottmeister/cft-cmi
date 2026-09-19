"""Numerical verification of every ingredient of the c/12 derivation (r = c = 1 chiral fermion)."""
import mpmath as mp
mp.mp.dps = 20
pi = mp.pi
print("== (1) thermal weight-2 spectral density: W(u) = C/sinh^4((u-i0)/2), C = c/(128 pi^2), c=1")
C = 1/(128*pi**2)
def What_formula(k): return k*(k**2+1)/(24*pi*(mp.e**(2*pi*k)-1))
def What_direct(k, eps=mp.mpf('0.3')):
    # shift contour to Im u = -eps... use exact contour shift by -i*pi: W-hat = C e^{-pi k} int dv e^{-ikv}/cosh^4(v/2)
    I4 = mp.quad(lambda v: mp.cos(k*v)/mp.cosh(v/2)**4, [-mp.inf, mp.inf])   # even integrand -> cos
    return C*mp.e**(-pi*k)*I4
for k in [mp.mpf('-1.3'), mp.mpf('-0.4'), mp.mpf('0.25'), mp.mpf('1.0')]:
    print(f"  k={float(k):+.2f}: contour-shift value {mp.nstr(What_direct(k),12)}   formula (c/24pi) k(k^2+1)/(e^{{2pi k}}-1) = {mp.nstr(What_formula(k),12)}")
print("  |Gamma(2+ik)|^2 check at k=0.7:", mp.nstr(abs(mp.gamma(2+0.7j))**2,12), " vs pi k(1+k^2)/sinh(pi k) =", mp.nstr(pi*0.7*(1+0.49)/mp.sinh(pi*0.7),12))
print("== (2) auxiliary integral int w^2/(cosh w + cosh u) dw = 2u(u^2+pi^2)/(3 sinh u)")
for u in [mp.mpf('0.5'), mp.mpf('2.0'), mp.mpf('5.0')]:
    lhs = mp.quad(lambda w: w**2/(mp.cosh(w)+mp.cosh(u)), [-mp.inf, mp.inf]); rhs = 2*u*(u**2+pi**2)/(3*mp.sinh(u))
    print(f"  u={float(u)}: {mp.nstr(lhs,12)}  vs  {mp.nstr(rhs,12)}")
print("== (3) the Bures and KM integrals")
IB = mp.quad(lambda k: mp.tanh(pi*k)/(k*(k**2+1)), [0, 1, 5, mp.inf]); print("  int_0^inf tanh(pi k)/(k(k^2+1)) dk =", mp.nstr(IB,15), " (claim: 2)")
gB = (1/(6*pi**2))*2*IB; print("  g_B = (c/6pi^2)*2*I =", mp.nstr(gB,15), "  2c/(3pi^2) =", mp.nstr(2/(3*pi**2),15), "  f2 = g_B/8 =", mp.nstr(gB/8,15), " 1/(12pi^2) =", mp.nstr(1/(12*pi**2),15))
gKM = (1/(6*pi))*mp.quad(lambda k: 1/(k**2+1), [-mp.inf, mp.inf]); print("  g_KM =", mp.nstr(gKM,15), " c/6 =", mp.nstr(mp.mpf(1)/6,15), "  s2 = g_KM/2 =", mp.nstr(gKM/2,15))
print("== (4) kernel identity: modular matrix elements of the exact first-order defect vs (q-q') * regularized generator")
def Dkernel(xi, xip):   # first-order defect kernel in the half-line modular frame, block xi<0<xi'  (times i/2pi omitted: real part R)
    return -mp.sinh(xi/2)*mp.sinh(xip/2)/mp.sinh((xi-xip)/2)**2
def D1_kernel_FT(kap, kapp):
    # D(kappa,kappa') = (1/(2pi)^2) [ (i/2pi) J - conj((i/2pi) J(kapp,kap)) ]  with J = int int e^{-i kap xi/2pi} R e^{i kapp xi'/2pi}
    def J(k1, k2):
        f = lambda xi: mp.quad(lambda xip: Dkernel(xi, xip)*mp.e**(1j*k2*xip/(2*pi)), [0, 5, 15, 60])*mp.e**(-1j*k1*xi/(2*pi))
        return mp.quad(f, [-60, -15, -5, 0])
    Jab = J(kap, kapp); Jba = J(kapp, kap)
    return ((1j/(2*pi))*Jab + mp.conj((1j/(2*pi))*Jba))/(2*pi)**2      # block + adjoint block
def gt_hat(k): return -2j/(k*(k**2+1))
def h_closed(kap, kapp):
    k = (kap-kapp)/(2*pi); return gt_hat(k)*(kap+kapp)/(4*pi)/(2*pi)**2
def q(kap): return 1/(1+mp.e**kap)
mp.mp.dps = 12
for (kap,kapp) in [(1.0,3.0),(2.5,-1.0),(4.0,4.5),(-3.0,0.7)]:
    kap, kapp = mp.mpf(kap), mp.mpf(kapp)
    num = D1_kernel_FT(kap, kapp); cf = (q(kap)-q(kapp))*h_closed(kap, kapp)
    print(f"  (k,k')=({float(kap)},{float(kapp)}): |D_kernel|={mp.nstr(abs(num),8)}  |(q-q')h_reg|={mp.nstr(abs(cf),8)}   ratio={mp.nstr(abs(num)/abs(cf),8)}  phase ratio={mp.nstr(num/cf,6)}")
