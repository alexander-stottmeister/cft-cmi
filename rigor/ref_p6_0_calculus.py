"""REF-P6-0 adversarial check of rigor/phase6_brief.md, Setting+W1..W4.
Exact rational arithmetic (fractions.Fraction) where possible, finite differences elsewhere.
No sympy on this machine; numpy + Fraction only.
Run:  python3 rigor/ref_p6_0_calculus.py
"""
from fractions import Fraction as F
import numpy as np

ok = lambda name, cond: print(("PASS " if cond else "**FAIL** ") + name)

# ---------------------------------------------------------------- maps
def Rpar(p, sig):
    """right-compression at p: identity for x<=p, parabolic toward p for x>p."""
    return lambda x: x if x <= p else p + (x - p) / (1 + sig * (x - p))

def Lpar(p, sig):
    """left-compression at p: identity for x>=p, parabolic toward p for x<p."""
    return lambda x: x if x >= p else p + (x - p) / (1 - sig * (x - p))

def compose(*fs):
    """compose(f1,f2,...) = f1 o f2 o ... (f1 = FIRST protocol step = outermost)."""
    def g(x):
        for f in reversed(fs):
            x = f(x)
        return x
    return g

def schw_jump(f, p, h=1e-4):
    """[f''/f'](p+) - [f''/f'](p-) by one-sided finite differences (f is C^1)."""
    def d2_over_d1(x0, side):
        s = 1.0 if side > 0 else -1.0
        xs = [x0 + s * k * h for k in (1, 2, 3, 4)]
        v = [f(x) for x in xs]
        # f'(x0+s h) ~ (v1-v0)/h etc.  Use 2nd/3rd order one-sided stencils on f.
        f1 = s * (-11 * f(x0) + 18 * v[0] - 9 * v[1] + 2 * v[2]) / (6 * h)
        f2 = (2 * f(x0) - 5 * v[0] + 4 * v[1] - 1 * v[2]) / (h * h)
        return f2 / f1
    return d2_over_d1(p, +1) - d2_over_d1(p, -1)

# ------------------------------------------------- (a) first-order field
print("\n=== (a) first-order field of h(x)=p+(x-p)/(1+sigma(x-p)) in the modular frame ===")
def beta_I(x, p1, pn):
    return (x - p1) * (pn - x) / (pn - p1)

rng = np.random.default_rng(0)
worst = 0.0
for _ in range(2000):
    p1 = rng.uniform(-5, 0); pn = p1 + rng.uniform(0.5, 10)
    p = rng.uniform(p1, pn); x = rng.uniform(p1, pn)
    sig = rng.uniform(0.01, 3.0)
    # field of the parabolic family, d/dsigma at sigma=0, in the y-coordinate
    eps = 1e-7
    hx = p + (x - p) / (1 + eps * (x - p))
    Vx = (hx - x) / eps                       # ~ -(x-p)^2
    Vy = Vx / beta_I(x, p1, pn)               # dy/dx = 1/beta_I
    y = np.log((x - p1) / (pn - x)); yp = np.log((p - p1) / (pn - p))
    pred = sig * beta_I(p, p1, pn) * (-4 * np.sinh((y - yp) / 2) ** 2) / sig  # per unit sigma
    worst = max(worst, abs(Vy - pred) / max(1e-12, abs(pred)))
ok("zeta*w(y-y_p) identity, zeta=sigma*beta_I(p), w(u)=-4 sinh^2(u/2)  (rel.err %.2e)" % worst,
   worst < 1e-5)

# Theorem A special case: I=(-a,L), p=0, sigma=s/L  =>  zeta = a s /(a+L)
a, L, s = F(7, 3), F(11, 5), F(4, 9)
zetaA = (s / L) * (a * L / (a + L))
ok("Theorem A zeta = a s/(a+L):  %s == %s" % (zetaA, a * s / (a + L)), zetaA == a * s / (a + L))

# ------------------------------------------------- (b) Schwarzian point masses
print("\n=== (b) Schwarzian of a C^1 piecewise-Moebius map ===")
sig1, sig2 = 0.37, 0.61
ok("right-compression jump = -2 sigma  (%.6f vs %.6f)" % (schw_jump(Rpar(0.0, sig1), 0.0), -2 * sig1),
   abs(schw_jump(Rpar(0.0, sig1), 0.0) + 2 * sig1) < 1e-4)
ok("left-compression  jump = -2 sigma  (%.6f vs %.6f)" % (schw_jump(Lpar(0.0, sig1), 0.0), -2 * sig1),
   abs(schw_jump(Lpar(0.0, sig1), 0.0) + 2 * sig1) < 1e-4)

# parameters add at a common point, same side
comp = compose(Rpar(0.0, sig1), Rpar(0.0, sig2))
xs = np.linspace(-2, 3, 41)
ok("R(s1) o R(s2) == R(s1+s2) exactly",
   max(abs(comp(x) - Rpar(0.0, sig1 + sig2)(x)) for x in xs) < 1e-13)

# opposite sides at a common point: = global Moebius o R(s1+s2)
comp = compose(Lpar(0.0, sig1), Rpar(0.0, sig2))
M = lambda u: u / (1 - sig1 * u)
ok("L(s1) o R(s2) == M_{-s1} o R(s1+s2) (global Moebius x single corner)",
   max(abs(comp(x) - M(Rpar(0.0, sig1 + sig2)(x))) for x in xs if x < 1 / sig1 - 0.3) < 1e-12)
ok("...and its Schwarzian jump = -2(s1+s2)  (%.6f)" % schw_jump(comp, 0.0),
   abs(schw_jump(comp, 0.0) + 2 * (sig1 + sig2)) < 1e-4)
comp2 = compose(Rpar(0.0, sig2), Lpar(0.0, sig1))   # other order (Protocol 3 'either order')
ok("R(s2) o L(s1) has the same Schwarzian jump (%.6f)" % schw_jump(comp2, 0.0),
   abs(schw_jump(comp2, 0.0) + 2 * (sig1 + sig2)) < 1e-4)

# ------------------------------------------------- VWZ protocols
print("\n=== (b) VWZ Protocols 1(A), 1(B), 2, 3 ===")
A, B, C, D = F(3, 7), F(5, 4), F(9, 8), F(2, 3)          # lengths a,b,c,d
p1 = F(0); p2 = A; p3 = A + B; p4 = A + B + C; p5 = A + B + C + D
T = p5 - p1
sig = lambda lB, lnew: 2 * lnew / (lB * (lB + lnew))      # ordinary Petz, s = 2 lambda

s1A = sig(B, C + D)                       # Protocol 1(A): P_{B->BCD}, corner p2
s1B_1 = sig(B, C)                         # Protocol 1(B) step 1: P_{B->BC},  corner p2
s1B_2 = sig(B + C, D)                     # Protocol 1(B) step 2: P_{BC->BCD}, corner p2
ok("1(B) identity 2c/(b(b+c)) + 2d/((b+c)(b+c+d)) = 2(c+d)/(b(b+c+d))  [%s]" % s1A,
   s1B_1 + s1B_2 == s1A)
f1A = Rpar(float(p2), float(s1A))
f1B = compose(Rpar(float(p2), float(s1B_1)), Rpar(float(p2), float(s1B_2)))
xs = np.linspace(float(p1) + 1e-9, float(p5) - 1e-9, 101)
err = max(abs(f1B(x) - f1A(x)) for x in xs)
ok("Protocol 1(B) point map == Protocol 1(A) point map LITERALLY (max|diff| = %.2e)" % err, err < 1e-14)

# Protocol 2: P_{B->BC} at p2, then P_{C->CD} at p3
s2_1, s2_2 = sig(B, C), sig(C, D)
f2 = compose(Rpar(float(p2), float(s2_1)), Rpar(float(p3), float(s2_2)))
ok("Protocol 2: two corners, jump at p2 = -2*%.6f (%.6f)" % (s2_1, schw_jump(f2, float(p2))),
   abs(schw_jump(f2, float(p2)) + 2 * float(s2_1)) < 1e-4)
ok("Protocol 2: jump at p3 = -2*%.6f (%.6f)" % (s2_2, schw_jump(f2, float(p3))),
   abs(schw_jump(f2, float(p3)) + 2 * float(s2_2)) < 1e-4)

# Protocol 3: P_{B->AB} (left-compression at p3), then P_{C->CD} (right at p3)
s3_1, s3_2 = sig(B, A), sig(C, D)
ok("sigma_1 = 2a/(b(a+b)) = %s" % s3_1, s3_1 == 2 * A / (B * (A + B)))
ok("sigma_2 = 2d/(c(c+d)) = %s" % s3_2, s3_2 == 2 * D / (C * (C + D)))
f3 = compose(Lpar(float(p3), float(s3_1)), Rpar(float(p3), float(s3_2)))
Mg = lambda u: float(p3) + (u - float(p3)) / (1 - float(s3_1) * (u - float(p3)))
single = Rpar(float(p3), float(s3_1 + s3_2))
err = max(abs(f3(x) - Mg(single(x))) for x in xs)
ok("Protocol 3 composite == (global Moebius) o R(sigma_1+sigma_2) at p3 (max|diff| %.2e)" % err, err < 1e-12)
err2 = max(abs(f3(x) - single(x)) for x in xs)
print("      (it is NOT literally equal to the single compression: max|diff| = %.4f)" % err2)
zeff = (s3_1 + s3_2) * (p3 - p1) * (p5 - p3) / T
ok("zeta_eff = (s1+s2)(a+b)(c+d)/(a+b+c+d) = %s" % zeff,
   zeff == (s3_1 + s3_2) * (A + B) * (C + D) / (A + B + C + D))

# ------------------------------------------------- (d) amplification
print("\n=== (d) amplification lemma ===")
bad = 0
for _ in range(20000):
    u = F(int(rng.integers(1, 50)), int(rng.integers(1, 20)))
    w = u + F(int(rng.integers(1, 50)), int(rng.integers(1, 20)))
    Tt = w + F(int(rng.integers(0, 50)), int(rng.integers(1, 20)))
    lhs = (Tt - u) * w / (Tt * (w - u))
    zp = u * (Tt - w) / (Tt * (w - u))     # cross ratio (p1,p,far,p_{n+1})
    ac = u * (Tt - w) / ((w - u) * Tt)     # z = a c/(b(a+b+c)) of the coarse triple
    if lhs != 1 + zp or zp != ac:
        bad += 1
ok("beta_I(p)/beta_Istep(p) = 1 + z', z' = cross ratio = ac/(b(a+b+c))  (%d/20000 bad)" % bad, bad == 0)

# ------------------------------------------------- (e) separation constraint
print("\n=== (e) L->R Petz chain: zeta_k^(I), e^{Delta_k}, separation inequality ===")
bad = 0; worstratio = 1e99
for _ in range(20000):
    n = int(rng.integers(4, 8))
    l = [F(int(rng.integers(1, 200)), int(rng.integers(1, 30))) for _ in range(n)]
    Ls = [sum(l[:k + 1]) for k in range(n)]
    Tt = Ls[-1]
    for k in range(2, n):                      # corner index k -> p_k, uses l_k,l_{k+1}
        lk, lk1 = l[k - 1], l[k]               # l_k, l_{k+1}
        Lkm1, Lk = Ls[k - 2], Ls[k - 1]        # L_{k-1}, L_k
        kap = 2 * lk1 / (lk * (lk + lk1))
        zeta = kap * Lkm1 * (Tt - Lkm1) / Tt
        r, uu, vv = lk1 / lk, lk / Lkm1, lk / (Tt - Lk)
        eD = (1 + uu) * (1 + vv)
        yk = Lkm1 / (Tt - Lkm1); yk1 = Lk / (Tt - Lk)
        if eD != yk1 / yk: bad += 1
        if zeta != 2 * r * (1 + vv) / ((1 + r) * (eD - 1)): bad += 1
        if (eD - 1) * zeta < 2 * r / (1 + r): bad += 1
        worstratio = min(worstratio, float((eD - 1) * zeta / (2 * r / (1 + r))))
ok("e^{Delta_k}=(1+u_k)(1+v_k), zeta_k^(I)=2r(1+v)/((1+r)(e^D-1)), (e^D-1)zeta>=2r/(1+r)  (%d bad)" % bad,
   bad == 0)
print("      min over 20000 random chains of (e^D-1)zeta / (2r/(1+r)) = %.6f  (>=1, =1+v_k)" % worstratio)

# how weak can two ADJACENT corners be at small separation?
print("      scan: smallest e^{Delta_k} compatible with zeta_k,zeta_{k+1} <= eps")
for eps in (0.3, 0.1, 0.03, 0.01):
    best = 1e99
    for _ in range(400000):
        l = np.exp(rng.uniform(-9, 9, 7))
        Ls = np.cumsum(l); Tt = Ls[-1]
        for k in range(2, 6):
            lk, lk1, lk2 = l[k - 1], l[k], l[k + 1]
            Lkm1, Lk, Lk1 = Ls[k - 2], Ls[k - 1], Ls[k]
            z1 = 2 * lk1 / (lk * (lk + lk1)) * Lkm1 * (Tt - Lkm1) / Tt
            z2 = 2 * lk2 / (lk1 * (lk1 + lk2)) * Lk * (Tt - Lk) / Tt
            if z1 <= eps and z2 <= eps:
                eD = (Lk / Lkm1) * ((Tt - Lkm1) / (Tt - Lk))
                best = min(best, eD)
    print("        eps=%.2f  min e^{Delta} = %.4g   (eps * min e^{Delta} = %.4g)" % (eps, best, eps * best))

# ------------------------------------------------- (f) the 1:2:4 numbers
print("\n=== (f) VWZ symmetric setup L_A=L_D=a, L_B=L_C=b ===")
for (aa, bb) in [(F(1, 10), F(1)), (F(1, 100), F(1)), (F(3), F(2))]:
    P1, P2, P3, P4, P5 = F(0), aa, aa + bb, aa + 2 * bb, 2 * aa + 2 * bb
    Tt = P5
    eta = aa / (aa + 2 * bb)
    bI = lambda x: (x - P1) * (P5 - x) / Tt
    z1 = sig(bb, bb + aa) * bI(P2)                     # Protocol 1(A): P_{B->BCD}
    z2a = sig(bb, bb) * bI(P2)                         # Protocol 2 corner at p2
    z2b = sig(bb, aa) * bI(P3)                         # Protocol 2 corner at p3
    z3 = (sig(bb, aa) + sig(bb, aa)) * bI(P3)          # Protocol 3 double corner
    D23 = (P3 / (P5 - P3)) / (P2 / (P5 - P2))
    print("  a=%s b=%s  eta=%s" % (aa, bb, eta))
    print("    single step zeta = %s   (a/b = %s)      -> %s" % (z1, aa / bb, z1 == aa / bb))
    print("    Prot2 zeta_2 = %s  (a(a+2b)/(2b(a+b)) = %s) -> %s"
          % (z2a, aa * (aa + 2 * bb) / (2 * bb * (aa + bb)), z2a == aa * (aa + 2 * bb) / (2 * bb * (aa + bb))))
    print("    Prot2 zeta_3 = %s  (a/b) -> %s" % (z2b, z2b == aa / bb))
    print("    Prot3 zeta_eff = %s  (2a/b) -> %s" % (z3, z3 == 2 * aa / bb))
    print("    e^{Delta_23} = %s  ((a+2b)/a = %s, = 1/eta) -> %s"
          % (D23, (aa + 2 * bb) / aa, D23 == (aa + 2 * bb) / aa))
    print("    zeta/eta:  1(A) %.4f   2:(%.4f,%.4f)   3: %.4f   [-> 2,2,2,4]"
          % (z1 / eta, z2a / eta, z2b / eta, z3 / eta))
    r1, r2, r3 = float(z1 ** 2), float(z2a ** 2 + z2b ** 2), float(z3 ** 2)
    print("    f2-sum ratios (cross term DROPPED): 1 : %.4f : %.4f" % (r2 / r1, r3 / r1))
    print("    with cross term 2 z2a z2b Ghat(D)/Ghat(0) = X:  ratio_2 = %.4f + %.4f*X"
          % (r2 / r1, float(2 * z2a * z2b) / r1))
