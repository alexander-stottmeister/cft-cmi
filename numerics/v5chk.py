import mpmath as mp
mp.mp.dps=25
pi=mp.pi
# (1) free complex fermion <TT>: T=(i/2)(psi^dag psi' - psi^dag' psi), A(u)=1/(2 pi i u)
# <TT>_c = (1/2)[(A')^2 - A A''] ; A=a/u -> = -a^2/(2u^4), a=1/(2 pi i)
a=1/(2j*pi); print("(1) <TT> coeff  -a^2/2 =",mp.nstr(-a**2/2,15)," vs c/(8pi^2)=",mp.nstr(1/(8*pi**2),15))
# check by numeric differentiation of A at complex u
u=mp.mpf('1.3')-mp.mpf('0.001')*1j
A=lambda z: a/z
h=mp.mpf('1e-8')
Ap=(A(u+h)-A(u-h))/(2*h); App=(A(u+h)-2*A(u)+A(u-h))/h**2
print("    numeric (1/2)[(A')^2-A A''] =",mp.nstr((Ap**2-A(u)*App)/2,12)," vs (1/(8pi^2))u^-4 =",mp.nstr(1/(8*pi**2)/u**4,12))
# (2) Fourier of (u-i0)^-4
for p in [mp.mpf('-1.7'),mp.mpf('0.9')]:
    I=mp.quad(lambda t: mp.e**(-1j*p*t)/(t-1e-6j)**4,[-mp.inf,-1,0,1,mp.inf])
    print(f"(2) p={float(p):+.2f} FT[(u-i0)^-4]={mp.nstr(I,8)}  (2pi/6)|p|^3 theta(-p)={mp.nstr((2*pi/6)*abs(p)**3 if p<0 else 0,8)}")
# (3) What
C=1/(128*pi**2)
for k in [mp.mpf('-1.3'),mp.mpf('0.25'),mp.mpf('1.0')]:
    I4=mp.quad(lambda v: mp.cos(k*v)/mp.cosh(v/2)**4,[-mp.inf,0,mp.inf])
    lhs=C*mp.e**(-pi*k)*I4; rhs=k*(k**2+1)/(24*pi*(mp.e**(2*pi*k)-1))
    print(f"(3) k={float(k):+.2f}: shifted {mp.nstr(lhs,14)}  formula {mp.nstr(rhs,14)}")
print("    What(0)=c/(48 pi^2)=",mp.nstr(1/(48*pi**2),12)," lim:",mp.nstr(mp.limit(lambda k: k*(k**2+1)/(24*pi*(mp.e**(2*pi*k)-1)),0),12))
# (4) key integral and base integral, V(u)
print("(4) int_0^inf tanh(pi k)/(k(k^2+1)) =",mp.nstr(mp.quad(lambda k: mp.tanh(pi*k)/(k*(k**2+1)),[0,1,5,mp.inf]),15))
for A_ in [mp.mpf('0.5'),mp.mpf('2.0')]:
    print(f"    a={float(A_)}: int w^2/(cosh w+cosh a)={mp.nstr(mp.quad(lambda w: w**2/(mp.cosh(w)+mp.cosh(A_)),[-mp.inf,0,mp.inf]),14)} vs {mp.nstr(2*A_*(A_**2+pi**2)/(3*mp.sinh(A_)),14)}")
for U in [mp.mpf('0.7'),mp.mpf('3.0')]:
    print(f"    V({float(U)})={mp.nstr(mp.quad(lambda v: v**2/(mp.cosh(v/2)+mp.cosh(U/2)),[-mp.inf,0,mp.inf]),14)} vs {mp.nstr(2*U*(U**2+4*pi**2)/(3*mp.sinh(U/2)),14)}")
# (5) Thm 5.2 assembly
IB=mp.quad(lambda U: mp.tanh(U/2)/(U*(U**2+4*pi**2)),[-mp.inf,-1,0,1,mp.inf])
print("(5) int_R tanh(u/2)/(u(u^2+4pi^2)) =",mp.nstr(IB,15)," 1/pi^2 =",mp.nstr(1/pi**2,15),"  gB=(2/3)I=",mp.nstr(2*IB/3,15)," 2/(3pi^2)=",mp.nstr(2/(3*pi**2),15))
IK=mp.quad(lambda U: 1/(U**2+4*pi**2),[-mp.inf,0,mp.inf]); print("    int_R du/(u^2+4pi^2)=",mp.nstr(IK,15),"(1/2)  gKM=(1/3)I=",mp.nstr(IK/3,15)," 1/6=",mp.nstr(mp.mpf(1)/6,15))
# (6) weight w_KM(lam)=(lam-1)log lam  vs 1+lam
for lam in [mp.mpf('7.389'),mp.mpf('100')]:
    print(f"(6) lam={float(lam)}: (lam-1)log lam={mp.nstr((lam-1)*mp.log(lam),8)}  1+lam={mp.nstr(1+lam,8)}")
