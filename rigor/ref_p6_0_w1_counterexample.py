"""REF-P6-0: counterexample to W1 as literally stated ("for ANY sequential one-sided protocol
S(Phi) = -2 sum_k kappa_k delta_{p_k}, kappa_k = sum of the sigma's of all steps whose corner is p_k").

The point-order argument needs every LATER step to be the identity near an EARLIER corner (or to
fix it with derivative 1).  That holds whenever every conditioning region A_B is a SINGLE interval
of the chain (a junction can then never be interior to the moving part A_B u A_new).  It FAILS as
soon as A_B is a UNION of chain intervals -- which is exactly what VWZ Protocol 1(B) does
(P_{BC->BCD}: A_B = BC).

Counterexample (4 intervals A_1 A_2 A_3 A_4, points p_1..p_5), ordinary Petz s = 2 lambda:
  start from A_2 A_3;
  step 1: add A_4 conditioning on A_3          -> corner p_3, right-compression, sigma_1
  step 2: add A_1 conditioning on A_2 A_3      -> corner p_4, LEFT-compression, sigma_2
Composite Phi = k_1 o k_2 (earlier step outermost).  Step 2 is NOT the identity near p_3: p_3 is
interior to its moving part A_1 u A_2 u A_3.  The corner of step 1 is therefore DISPLACED to
k_2^{-1}(p_3) and its mass is multiplied by k_2'(k_2^{-1}(p_3)) != 1.
"""
import numpy as np

def Rpar(p, s): return lambda x: x if x <= p else p + (x - p) / (1 + s * (x - p))
def Lpar(p, s): return lambda x: x if x >= p else p + (x - p) / (1 - s * (x - p))
def comp(f, g): return lambda x: f(g(x))

def dd_over_d(f, x0, side, h=1e-5):
    s = 1.0 if side > 0 else -1.0
    v = [f(x0 + s * k * h) for k in (1, 2, 3)]
    f1 = s * (-11 * f(x0) + 18 * v[0] - 9 * v[1] + 2 * v[2]) / (6 * h)
    f2 = (2 * f(x0) - 5 * v[0] + 4 * v[1] - 1 * v[2]) / (h * h)
    return f2 / f1
def jump(f, p): return dd_over_d(f, p, +1) - dd_over_d(f, p, -1)

l1, l2, l3, l4 = 1.3, 2.1, 0.9, 1.7
p1 = 0.0; p2 = l1; p3 = l1 + l2; p4 = l1 + l2 + l3; p5 = l1 + l2 + l3 + l4
sig = lambda lB, ln: 2 * ln / (lB * (lB + ln))

s1 = sig(l3, l4)            # step 1: A_B = A_3 (len l3), A_new = A_4 (len l4), corner p_3
s2 = sig(l2 + l3, l1)       # step 2: A_B = A_2 A_3 (len l2+l3), A_new = A_1, corner p_4
k1 = Rpar(p3, s1)
k2 = Lpar(p4, s2)
Phi = comp(k1, k2)          # earlier step outermost

# image check: step 2 must land inside A_2 A_3 (admissibility of the zero-collar map)
print("step-2 image of p_1 = %.6f  (must be >= p_2 = %.6f): %s" % (k2(p1), p2, k2(p1) >= p2))
print("sigma_1 = %.6f   sigma_2 = %.6f" % (s1, s2))

x0 = None                                   # k_2^{-1}(p_3)
lo, hi = p1, p4
for _ in range(200):
    m = 0.5 * (lo + hi)
    if k2(m) < p3: lo = m
    else: hi = m
x0 = 0.5 * (lo + hi)
k2p = (k2(x0 + 1e-6) - k2(x0 - 1e-6)) / 2e-6
print("\nclaimed corner set (junctions): p_3 = %.6f, p_4 = %.6f" % (p3, p4))
print("actual   corner at  k_2^{-1}(p_3) = %.6f   (NOT a junction; p_3 = %.6f)" % (x0, p3))
print("k_2'(x_0) = %.6f" % k2p)
print("\njumps of Phi'' / Phi' :")
for name, q in (("p_3 (claimed, sigma_1)", p3), ("x_0 = k_2^{-1}(p_3)", x0), ("p_4 (sigma_2)", p4)):
    print("   at %-24s : %+.6f      (claim -2 sigma: %+.6f / %+.6f)"
          % (name, jump(Phi, q), -2 * s1, -2 * s2))
print("\npredicted displaced mass -2 sigma_1 k_2'(x_0) = %+.6f" % (-2 * s1 * k2p))
print("measured                                        %+.6f" % jump(Phi, x0))
print("mass at the junction p_3                        %+.6f  (claim %+.6f)" % (jump(Phi, p3), -2 * s1))
tot_claim = -2 * (s1 + s2)
tot_true = jump(Phi, x0) + jump(Phi, p4)
print("\ntotal Schwarzian mass: claimed %+.6f, actual %+.6f  (ratio %.4f)"
      % (tot_claim, tot_true, tot_true / tot_claim))

# control: the same two steps with A_B = A_2 only (a single chain interval) -> corner p_3 for
# BOTH steps, masses add, claim holds.
s2b = sig(l2, l1)
Phi_b = comp(Rpar(p3, s1), Lpar(p3, s2b))
print("\ncontrol (A_B = A_2, a single interval): both corners at p_3;")
print("   jump = %+.6f, claim -2(sigma_1+sigma_2) = %+.6f" % (jump(Phi_b, p3), -2 * (s1 + s2b)))
