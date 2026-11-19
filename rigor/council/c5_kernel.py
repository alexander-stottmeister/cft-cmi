"""C5 council: independent check of thm:T4 (corner kernel Ghat) and of cor:vwz corner data.
Run (repository root):  ${PYTHON:-python3} rigor/council/c5_kernel.py > rigor/council/c5_kernel.out
Written from the formulas of network_second_order.tex (C3)-(C7), (eq:KI) and thm:T4 only; shares no code
with rigor/g1b_kernel.py. c = r = 1 throughout.
Tolerances (fixed before the run):
 V0 (validation, exact known case): int rho = 1/(12 pi^2), rel tol 1e-12.
 K1 Fourier integral of rho vs closed form vs series, |diff|/Ghat(0) < 1e-10.
 K2 S(u) = int |D1|^2/N dv from the KI kernel (2D route, scipy quad) vs (2/3) tanh(u/2)/(u(u^2+4pi^2)), rel 1e-7.
 K3 decay bounds of thm:T4(d), checked with 30-digit mpmath values, must hold exactly (no tolerance).
 K4 card values Ghat/Ghat(0) at Delta = 0.5,1,2,4,8, abs tol 6e-8 (card gives 7 decimals).
 K5 cor:vwz corner data, exact rational arithmetic, must be identities.
Modes: K2 integrates v over [-150,150]; the integrand is O(v^2 e^{-|v|/2}) beyond, cut-off weight < 1e-28 with scipy quad (integrand decays like e^{-|v|/2}); no cutoff."""
import mpmath as mp
from fractions import Fraction as Fr
import random, math
from scipy import integrate
mp.mp.dps = 30
pi = mp.pi
rho = lambda q: mp.tanh(pi*q)/(48*pi**2*q*(1+q**2)) if q != 0 else 1/(48*pi)
G0 = 1/(12*pi**2)
def G_fourier(D):
    if D == 0:
        return 2*mp.quad(rho, [0, 1, 10, mp.inf])
    return 2*mp.quadosc(lambda q: rho(q)*mp.cos(q*D), [0, mp.inf], omega=D)
def G_closed(D):
    D = abs(mp.mpf(D))
    return (mp.cosh(D/2) - mp.sinh(D/2)**2*mp.log(mp.coth(D/4)))/(12*pi**2)
def G_series(D):
    D = abs(mp.mpf(D))
    return mp.nsum(lambda n: mp.exp(-(n+0.5)*D)/((n+0.5)*(1-(n+0.5)**2)), [0, mp.inf])/(24*pi**2)
ok = True
v0 = G_fourier(0)
r = abs(v0/G0-1); print(f"V0 int rho = {mp.nstr(v0,20)}  1/(12pi^2) = {mp.nstr(G0,20)}  rel {mp.nstr(r,3)}  {'PASS' if r<1e-12 else 'FAIL'}"); ok &= r<1e-12
print("K1 Delta | Fourier | closed | series | max|diff|/G0")
for D in [0.1, 0.5, 1, 2, 4, 8, 12]:
    a, b, c = G_fourier(mp.mpf(D)), G_closed(D), G_series(D)
    d = max(abs(a-b), abs(a-c), abs(b-c))/G0
    print(f"   {D:5} {mp.nstr(a,16)} {mp.nstr(b,16)} {mp.nstr(c,16)} {mp.nstr(d,3)} {'PASS' if d<1e-10 else 'FAIL'}"); ok &= d<1e-10
# K2: from the KI kernel, in floats
def S_num(u):
    def f(v):
        k, kp = (v+u)/2, (v-u)/2
        q = lambda x: 1/(1+math.exp(x))          # q_kappa; 1-q_kappa computed as q(-kappa) (no cancellation)
        qk, qkp, pk, pkp = q(k), q(kp), q(-k), q(-kp)
        D1 = (qk-qkp)*v/(u*(u*u+4*math.pi**2))   # eq:KI as printed
        N = qk*pkp+qkp*pk
        return D1*D1/N
    return integrate.quad(f, -150, 150, points=[0], limit=400, epsabs=0, epsrel=1e-12)[0]
print("K2 u | S numerical (KI kernel) | (2/3)tanh(u/2)/(u(u^2+4pi^2)) | rel")
for u in [0.3, 1.0, 2.5, 6.0, 15.0]:
    a = S_num(u); b = 2/3*math.tanh(u/2)/(u*(u*u+4*math.pi**2)); rr = abs(a/b-1)
    print(f"   {u:5} {a:.15e} {b:.15e} {rr:.2e} {'PASS' if rr<1e-7 else 'FAIL'}"); ok &= rr<1e-7
print("K3 Delta | lower x(4-x^2)/36pi^2 <= G <= x/9pi^2 | |G-x/9pi^2| <= x^3/36pi^2")
prev = G0
for i in range(1, 81):
    D = mp.mpf(i)/8; x = mp.exp(-D/2); g = G_closed(D)
    c1 = x*(4-x**2)/(36*pi**2) <= g <= x/(9*pi**2); c2 = abs(g-x/(9*pi**2)) <= x**3/(36*pi**2); c3 = g < prev and g > 0
    prev = g; ok &= bool(c1 and c2 and c3)
    if i % 16 == 0 or not (c1 and c2 and c3): print(f"   {mp.nstr(D,4)} {c1} {c2} decreasing&positive {c3}")
print("K4 card ratios")
for D, card in [(0.5,0.8983866),(1,0.7456151),(2,0.4769603),(4,0.1797843),(8,0.0244192)]:
    v = G_closed(D)/G0; d = abs(v-card)
    print(f"   {D} {mp.nstr(v,10)} card {card} |diff| {mp.nstr(d,2)} {'PASS' if d<6e-8 else 'FAIL'}"); ok &= d<6e-8
print("K5 cor:vwz corner data (exact rationals, 200 random (a,b))")
random.seed(5); good = True
for _ in range(200):
    a, b = Fr(random.randint(1,97), random.randint(1,13)), Fr(random.randint(1,97), random.randint(1,13))
    p = [0, a, a+b, a+2*b, 2*a+2*b]; L = p[4]
    beta = lambda x, l, r_: (x-l)*(r_-x)/(r_-l)
    lam1A = (a+b)/b; s1A = 2*lam1A/(b+b+a); z1 = s1A*beta(p[1],0,L)            # 1(A): kept AB, cond B, add CD
    s2 = 2*Fr(1)/(2*b); s3 = 2*(a/b)/(b+a)                                   # Protocol 2 steps (ordinary Petz s = 2 lambda)
    z2, z3 = s2*beta(p[1],0,L), s3*beta(p[2],0,L)
    yratio = (p[2]/(L-p[2]))/(p[1]/(L-p[1]))                                 # e^{y3-y2}
    zJ = s3*beta(p[2],p[1],L)
    good &= (z1 == a/b and z2 == a*(a+2*b)/(2*b*(a+b)) and z3 == a/b and yratio == (a+2*b)/a and zJ == 2*a/(a+2*b))
print(f"   all identities hold: {good}"); ok &= good
print("OVERALL", "PASS" if ok else "FAIL")
