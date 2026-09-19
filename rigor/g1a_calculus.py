"""G1a: numerical verification of every closed-form identity of
rigor/network_corner_calculus.tex (corner calculus, VWZ protocols, protocol tables).

Conventions: rigor/phase6_brief.md.  Points p_1<...<p_{n+1}, A_k=(p_k,p_{k+1}),
step map = parabolic compression toward the corner, sigma = s/(l_B+l_new),
ordinary Petz s = 2 lambda = 2 l_new/l_B; composite Phi = k_1 o k_2 o ... (first
step OUTERMOST).  Run: python3 rigor/g1a_calculus.py
"""
from fractions import Fraction as F
from itertools import permutations
import numpy as np

ok = lambda name, c: print(("PASS  " if c else "**FAIL** ") + name)

# ---------------------------------------------------------------- maps
def Rpar(p, s):  return lambda x: x if x <= p else p + (x - p) / (1 + s * (x - p))
def Lpar(p, s):  return lambda x: x if x >= p else p + (x - p) / (1 - s * (x - p))
def comp(*fs):
    def g(x):
        for f in reversed(fs): x = f(x)
        return x
    return g

def dd_over_d(f, x0, side, h=1e-5):
    s = 1.0 if side > 0 else -1.0
    v = [f(x0 + s * k * h) for k in (1, 2, 3)]
    f1 = s * (-11 * f(x0) + 18 * v[0] - 9 * v[1] + 2 * v[2]) / (6 * h)
    f2 = (2 * f(x0) - 5 * v[0] + 4 * v[1] - 1 * v[2]) / (h * h)
    return f2 / f1
def jump(f, p): return dd_over_d(f, p, +1) - dd_over_d(f, p, -1)
def sig(lB, ln, s=None):            # sigma = s/(l_B+l_new); default ordinary Petz
    s = 2 * ln / lB if s is None else s
    return s / (lB + ln)

print("=== 1. parabolic group laws (Lemma: composition at a common point) ===")
s1, s2 = 0.37, 0.61
xs = np.linspace(-2.0, 3.0, 61)
ok("R(s1) o R(s2) = R(s1+s2)  [same side]",
   max(abs(comp(Rpar(0, s1), Rpar(0, s2))(x) - Rpar(0, s1 + s2)(x)) for x in xs) < 1e-13)
ok("L(s1) o L(s2) = L(s1+s2)  [same side]",
   max(abs(comp(Lpar(0, s1), Lpar(0, s2))(x) - Lpar(0, s1 + s2)(x)) for x in xs) < 1e-13)
Mg = lambda u: u / (1 - s1 * u)                      # global Moebius, parabolic at 0
ok("L(s1) o R(s2) = M o R(s1+s2)  [opposite sides, M global Moebius]",
   max(abs(comp(Lpar(0, s1), Rpar(0, s2))(x) - Mg(Rpar(0, s1 + s2)(x)))
       for x in xs if x < 1 / s1 - 0.3) < 1e-12)
ok("jump of [Phi''/Phi'] at 0 for L(s1) o R(s2) equals -2(s1+s2) (%.6f)"
   % jump(comp(Lpar(0, s1), Rpar(0, s2)), 0.0),
   abs(jump(comp(Lpar(0, s1), Rpar(0, s2)), 0.0) + 2 * (s1 + s2)) < 1e-4)
ok("jump of [Phi''/Phi'] at 0 for R(s2) o L(s1) equals -2(s1+s2) (%.6f)"
   % jump(comp(Rpar(0, s2), Lpar(0, s1)), 0.0),
   abs(jump(comp(Rpar(0, s2), Lpar(0, s1)), 0.0) + 2 * (s1 + s2)) < 1e-4)

print("\n=== 2. general transformation rule S(f o g) = S(g) + (g')^2 S(f) o g ===")
# REF-P6-0 counterexample, reproduced: (l1..l4)=(1.3,2.1,0.9,1.7), start A_2A_3,
# step 1 = A_4 on A_3 (corner p_3), step 2 = A_1 on A_2A_3 (corner p_4).
l = [1.3, 2.1, 0.9, 1.7]
p = [0.0] + list(np.cumsum(l))                      # p[0]=p_1 ... p[4]=p_5
sA, sB = sig(l[2], l[3]), sig(l[1] + l[2], l[0])
k1, k2 = Rpar(p[2], sA), Lpar(p[3], sB)
Phi = comp(k1, k2)
lo, hi = p[0], p[3]
for _ in range(200):
    m = 0.5 * (lo + hi)
    lo, hi = (m, hi) if k2(m) < p[2] else (lo, m)
x0 = 0.5 * (lo + hi); k2p = (k2(x0 + 1e-6) - k2(x0 - 1e-6)) / 2e-6
ok("displaced mass at k_2^{-1}(p_3)=%.6f is -2 sigma_1 k_2'(x_0) (k_2'=%.6f)" % (x0, k2p),
   abs(jump(Phi, x0) + 2 * sA * k2p) < 1e-4)
ok("no mass at the junction p_3 (jump = %.2e)" % jump(Phi, p[2]), abs(jump(Phi, p[2])) < 1e-3)
ok("mass -2 sigma_2 at p_4", abs(jump(Phi, p[3]) + 2 * sB) < 1e-4)

print("\n=== 3. Hypothesis H: single-interval conditioning is NOT sufficient ===")
# start from the SINGLE interval A_2 (chain A_1 A_2 A_3): step 1 = A_3 on A_2 (corner p_2,
# the far end), step 2 = A_1 on A_2 (corner p_3).  Both A_B are single chain intervals,
# yet the earlier corner p_2 is interior to the later moving part A_1 u A_2 = (p_1,p_3).
l3 = [1.0, 1.0, 1.0]; q = [0.0, 1.0, 2.0, 3.0]
t1 = sig(l3[1], l3[2]); t2 = sig(l3[1], l3[0])          # sigma_1 = sigma_2 = 1
k2b = Lpar(q[2], t2); Pc = comp(Rpar(q[1], t1), k2b)
print("   image of the later step: k_2((p_1,p_3)) = (%.6f, %.6f); the earlier corner p_2 = %.1f"
      % (k2b(q[0]), q[2], q[1]))
ok("the earlier corner p_2 is NOT in the range of k_2 (it is swallowed)", k2b(q[0]) > q[1])
print("   jump of Phi at p_2 = %+.2e (claim -2 sigma_1 = %+.6f)" % (jump(Pc, q[1]), -2 * t1))
ok("total Schwarzian mass is -2 sigma_2 = %+.4f, NOT -2(sigma_1+sigma_2) = %+.4f"
   % (-2 * t2, -2 * (t1 + t2)), abs(jump(Pc, q[2]) + 2 * t2) < 1e-4 and abs(jump(Pc, q[1])) < 1e-3)
ok("Phi = (global Moebius) o k_2 : the first step leaves the state unchanged",
   max(abs(Pc(x) - (q[1] + (k2b(x) - q[1]) / (1 + t1 * (k2b(x) - q[1]))))
       for x in np.linspace(1e-9, 3 - 1e-9, 101)) < 1e-13)
print("   (starting block with >= 2 intervals + single-interval conditioning => H, see 5.)")

print("\n=== 4. VWZ protocols (a,b,c,d = lengths of A,B,C,D) ===")
a, b, c, d = F(3, 7), F(5, 4), F(9, 8), F(2, 3)
P1, P2, P3, P4, P5 = F(0), a, a + b, a + b + c, a + b + c + d
ok("1(B)=1(A) identity 2c/(b(b+c)) + 2d/((b+c)(b+c+d)) = 2(c+d)/(b(b+c+d))",
   sig(b, c) + sig(b + c, d) == sig(b, c + d))
for t in (0.0, 0.3, 1.7):                        # rotated maps, common t: s_t = lam(1+e^{-2pi t})
    f = (1 + np.exp(-2 * np.pi * t)) / 2
    lhs = float(sig(b, c)) * f + float(sig(b + c, d)) * f
    ok("  ... also for the rotated maps at common t = %.1f" % t,
       abs(lhs - float(sig(b, c + d)) * f) < 1e-15)
f1A = Rpar(float(P2), float(sig(b, c + d)))
f1B = comp(Rpar(float(P2), float(sig(b, c))), Rpar(float(P2), float(sig(b + c, d))))
xs = np.linspace(float(P1) + 1e-9, float(P5) - 1e-9, 201)
ok("1(B) and 1(A) are LITERALLY the same point map (max|diff| = %.1e)"
   % max(abs(f1B(x) - f1A(x)) for x in xs), max(abs(f1B(x) - f1A(x)) for x in xs) < 1e-14)
s31, s32 = sig(b, a), sig(c, d)                   # Protocol 3: A on B, D on C, corner p_3
ok("Protocol 3: sigma_1 = 2a/(b(a+b)), sigma_2 = 2d/(c(c+d))",
   s31 == 2 * a / (b * (a + b)) and s32 == 2 * d / (c * (c + d)))
f3 = comp(Lpar(float(P3), float(s31)), Rpar(float(P3), float(s32)))
f3r = comp(Rpar(float(P3), float(s32)), Lpar(float(P3), float(s31)))
single = Rpar(float(P3), float(s31 + s32))
Mob = lambda u: float(P3) + (u - float(P3)) / (1 - float(s31) * (u - float(P3)))
ok("Protocol 3 = (global Moebius) o R(sigma_1+sigma_2) at p_3",
   max(abs(f3(x) - Mob(single(x))) for x in xs) < 1e-12)
ok("Protocol 3 in the other order has the same Schwarzian mass (%.6f)" % jump(f3r, float(P3)),
   abs(jump(f3r, float(P3)) + 2 * float(s31 + s32)) < 1e-4)
ok("Protocol 3: the two orders give LITERALLY the same point map (L and R at p commute)",
   max(abs(f3(x) - f3r(x)) for x in xs) < 1e-14)
zeff = (s31 + s32) * (P3 - P1) * (P5 - P3) / (P5 - P1)
ok("zeta_eff = (sigma_1+sigma_2)(a+b)(c+d)/(a+b+c+d) = %s" % zeff,
   zeff == (s31 + s32) * (a + b) * (c + d) / (a + b + c + d))
sprime = (s31 + s32) * (c + d)
ok("effective Theorem-A parameter s' = (sigma_1+sigma_2)(c+d) = %s >= lambda' = d/c = %s"
   % (sprime, d / c), sprime >= d / c)
bad = 0
for _ in range(20000):                            # s' >= 2 lambda' exactly, for all sizes
    r = lambda: F(int(np.random.randint(1, 60)), int(np.random.randint(1, 17)))
    aa, bb, cc, dd = r(), r(), r(), r()
    if (2 * aa / (bb * (aa + bb)) + 2 * dd / (cc * (cc + dd))) * (cc + dd) < 2 * dd / cc: bad += 1
ok("s' >= 2 lambda' (over-compressed) in 20000 random rational configurations (%d bad)" % bad,
   bad == 0)

print("\n=== 5. protocol tables n = 4, 5 (single-interval conditioning) ===")
def protocols(n, lens):
    """all one-sided protocols: start from an adjacent pair, add one interval at a time
    on either side, conditioning on the adjacent chain interval.  Returns
    {(start, order-string): {corner index k: kappa_k}}."""
    P = [0.0] + list(np.cumsum(lens))
    out = {}
    for i in range(1, n):                          # start block = A_i A_{i+1}
        left, right = i, i + 1                     # block = A_left..A_right
        moves = ['L'] * (left - 1) + ['R'] * (n - right)
        for order in sorted(set(permutations(moves))):
            lo, hi, corners = left, right, {}
            for mv in order:
                if mv == 'R':
                    kB, kN = hi, hi + 1; k = kB     # corner p_kB (inner end of A_hi)
                    s = sig(lens[kB - 1], lens[kN - 1]); hi += 1
                else:
                    kB, kN = lo, lo - 1; k = kB + 1  # corner p_{kB+1}
                    s = sig(lens[kB - 1], lens[kN - 1]); lo -= 1
                corners[k] = corners.get(k, 0.0) + s
            out[(i, ''.join(order))] = corners
    return out, P

for n in (4, 5):
    lens = [1.0] * n if n == 4 else [1.0, 1.3, 0.7, 1.9, 1.1]
    tab, P = protocols(n, lens)
    T = P[-1]
    print("  n = %d, lengths %s" % (n, lens))
    seen = {}
    for (i, order), cor in sorted(tab.items()):
        key = tuple(sorted((k, round(v, 12)) for k, v in cor.items()))
        seen.setdefault(key, []).append((i, order))
        zz = {k: v * (P[k - 1] - P[0]) * (T - P[k - 1]) / T for k, v in sorted(cor.items())}
        print("    start A_%d A_%d  order %-4s  kappa = %s   zeta^(I) = %s"
              % (i, i + 1, order, {k: round(v, 5) for k, v in sorted(cor.items())},
                 {k: round(v, 5) for k, v in zz.items()}))
    ok("  n=%d: %d protocols fall into %d classes = %d starting pairs (order-independent)"
       % (n, len(tab), len(seen), n - 1), len(seen) == n - 1)
    # verify the composite Schwarzian numerically for one representative of each class
    for key, members in seen.items():
        i, order = members[0]
        lo, hi, maps = i, i + 1, []
        for mv in order:
            if mv == 'R':
                maps.append(Rpar(P[hi - 1], sig(lens[hi - 1], lens[hi]))); hi += 1
            else:
                maps.append(Lpar(P[lo], sig(lens[lo - 1], lens[lo - 2]))); lo -= 1
        Phi = comp(*maps)
        good = all(abs(jump(Phi, P[k - 1]) + 2 * v) < 3e-3 * max(1.0, 2 * v)
                   for k, v in dict(key).items())
        ok("    S(Phi) = -2 sum kappa_k delta_{p_k} for start A_%d A_%d order %s" % (i, i + 1, order),
           good)

print("\n=== 6. amplification (Lemma) ===")
bad = 0
for _ in range(20000):
    rr = lambda lo, hi: F(int(np.random.randint(lo, hi)), int(np.random.randint(1, 20)))
    u = rr(1, 50); w = u + rr(1, 50); Tt = w + rr(0, 50)
    if (Tt - u) * w / (Tt * (w - u)) != 1 + u * (Tt - w) / (Tt * (w - u)): bad += 1
    if u * (Tt - w) / (Tt * (w - u)) != u * (Tt - w) / ((w - u) * Tt): bad += 1
ok("beta_I(p)/beta_{I_step}(p) = 1 + z', z' = ac/(b(a+b+c))  (%d/20000 bad)" % bad, bad == 0)
