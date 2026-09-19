"""REF-P6-3: independent check of rigor/network_corner_calculus.tex, sections 10-13.

  (a) Lemma 10.3 re-derived from scratch (exact rational --> hyperbolic form), including the
      BOUNDARY case k = n-1, where Delta_n = +infinity and (29) holds with EQUALITY, not with
      the strict "<" printed in the document.
  (b) Theorem 11.1: the recursion, the fixed point, the bound e^{Delta_k} >= 2/eps, and how
      sharp the constant 2 really is (a dedicated minimiser as a function of eps and of the
      chain length).
  (c) Corollary 11.2 (admissible s_j), and the claim that the hypothesis cannot be weakened
      to the pair {k,k+1}.
  (d) Corollary 12.6: the two asymptotic expansions, and the chordal (Bures-DISTANCE)
      variant of Theorem 12.5, which needs no Hypothesis (U).
  (e) Proposition 13.1 / Box [G5]: the normalisation of the FHSW weight p(t).
Run: python3 rigor/ref_p6_3_separation.py
"""
import math
import random
from fractions import Fraction as Q

FAILS = []
def ok(name, cond):
    print(("PASS  " if cond else "**FAIL** ") + name)
    if not cond:
        FAILS.append(name)

# ---------------------------------------------------------------- L->R chain data
def chain(l):
    """exact kappa_k, zeta_k and Delta_k for the L->R ordinary-Petz chain, k = 2..n-1."""
    l = [Q(x) for x in l]
    n = len(l)
    L = []
    acc = Q(0)
    for x in l:
        acc += x
        L.append(acc)                       # L[k-1] = L_k
    T = L[-1]
    z, D = [], []
    for k in range(2, n):                   # corner at p_k
        lk, lk1 = l[k - 1], l[k]
        Lkm1 = L[k - 2]                     # L_{k-1}
        kap = 2 * lk1 / (lk * (lk + lk1))
        z.append(kap * Lkm1 * (T - Lkm1) / T)
        # Delta_k = y_{k+1} - y_k, y_j = log( (p_j-p_1)/(p_{n+1}-p_j) ) = log(L_{j-1}/(T-L_{j-1}))
        yk = Q(L[k - 2], 1) / (T - L[k - 2])
        yk1 = Q(L[k - 1], 1) / (T - L[k - 1])
        D.append(yk1 / yk)                  # e^{Delta_k}, EXACT rational
    return z, D                             # D holds e^{Delta_k}

print("=== (a) Lemma 10.3, re-derived; the boundary case k = n-1 ===")
random.seed(3)
w1 = w2 = 0.0
bad_strict = 0
eqs_last = 0
tested_last = 0
for _ in range(20000):
    n = random.randint(4, 9)
    l = [Q(random.randint(1, 10 ** 4), random.randint(1, 97)) for _ in range(n)]
    z, E = chain(l)                          # E[i] = e^{Delta_{i+2}}
    m = len(z)
    D = [math.log(float(e)) for e in E]
    for i in range(m):
        D2 = D[i + 1] if i + 1 < m else math.inf
        if math.isfinite(D2):
            pred = math.sinh(D2 / 2) / (math.sinh(D[i] / 2) * math.sinh((D[i] + D2) / 2))
            inv = math.sinh(D[i] / 2) ** 2 / math.tanh(D2 / 2) + 0.5 * math.sinh(D[i])
        else:
            pred = 2.0 / (math.exp(D[i]) - 1.0)       # the k = n-1 convention coth(inf)=1
            inv = (math.exp(D[i]) - 1.0) / 2.0
        w1 = max(w1, abs(pred / float(z[i]) - 1))
        w2 = max(w2, abs(1 / (inv * float(z[i])) - 1))
    # (29) e^{Delta_k} < 1 + 2/zeta_k : EXACT rational test, and the last corner separately
    for i in range(m):
        lhs, rhs = E[i], 1 + 2 / z[i]
        if i < m - 1:
            if not lhs < rhs:
                bad_strict += 1
        else:
            tested_last += 1
            if lhs == rhs:
                eqs_last += 1
ok("Lem 10.3 first form  zeta_k = sinh(D_{k+1}/2)/(sinh(D_k/2)sinh((D_k+D_{k+1})/2))  "
   "(max rel err %.1e)" % w1, w1 < 1e-9)
ok("Lem 10.3 second form 1/zeta_k = sinh^2(D_k/2)coth(D_{k+1}/2)+sinh(D_k)/2  (max rel err %.1e)"
   % w2, w2 < 1e-9)
ok("(29) e^{Delta_k} < 1 + 2/zeta_k is STRICT for k <= n-2 (%d violations in 20000 chains)"
   % bad_strict, bad_strict == 0)
ok("but for k = n-1 (29) holds with EXACT EQUALITY in %d of %d chains -- the document prints "
   "the strict '<' for 2 <= k <= n-1" % (eqs_last, tested_last), eqs_last == tested_last)
print("   => Lemma 10.3 eq. (29) must read  e^{Delta_k} <= 1 + 2/zeta_k, with equality iff k = n-1")
print("      (the document itself uses the equality at k = n-1 in Thm 11.1 step <1>7).")
print("   g1a_separation.py check (iv) uses the slack (1+1e-8), so it does not test the strict form.")

def chain_f(l):
    """float version: zeta_k and e^{Delta_k}."""
    n = len(l); L = []; acc = 0.0
    for x in l:
        acc += x; L.append(acc)
    T = L[-1]; z = []; E = []
    for k in range(2, n):
        lk, lk1, Lkm1, Lk = l[k - 1], l[k], L[k - 2], L[k - 1]
        if T - Lk <= 0 or Lkm1 <= 0 or T - Lkm1 <= 0:
            return [], []                      # underflow: reject this trial
        z.append(2 * lk1 / (lk * (lk + lk1)) * Lkm1 * (T - Lkm1) / T)
        E.append((Lk / (T - Lk)) * ((T - Lkm1) / Lkm1))
    return z, E

print("\n=== (b) Theorem 11.1: recursion, fixed point, bound, sharpness (EXACT rationals) ===")
badrec = badfix = badsep = badlast = 0
eq_last_rec = 0
worst = Q(10 ** 9)
for _ in range(60000):
    n = random.randint(4, 9)
    l = [Q(random.randint(1, 10 ** 5), random.randint(1, 233)) for _ in range(n)]
    z, E = chain(l)                              # EXACT
    g = [2 / (e - 1) for e in E]                 # gamma_j, exact
    for i in range(len(z)):
        gnext = g[i + 1] if i + 1 < len(z) else Q(0)
        if g[i] > z[i] * (1 + gnext / 2):
            badrec += 1
        if i == len(z) - 1 and g[i] == z[i]:
            eq_last_rec += 1
        eps = max(z[i:])
        if eps >= 2:
            continue
        if g[i] > 2 * eps / (2 - eps):
            badfix += 1
        if E[i] < 2 / eps:
            badsep += 1
        worst = min(worst, E[i] * eps / 2)
    epsl = z[-1]
    if epsl < 2 and E[-1] < 1 + 2 / epsl:
        badlast += 1
worst = float(worst)
ok("recursion  gamma_j <= zeta_j (1 + gamma_{j+1}/2)   (%d violations)" % badrec, badrec == 0)
ok("fixed point gamma_j <= 2 eps/(2-eps)               (%d violations)" % badfix, badfix == 0)
ok("separation e^{Delta_k} >= 2/eps                    (%d violations, min (eps/2)e^{Delta} = %.9f)"
   % (badsep, worst), badsep == 0)
ok("last corner e^{Delta_{n-1}} >= 1 + 2/eps_{n-1}     (%d violations)" % badlast, badlast == 0)
ok("the recursion is an EQUALITY at the last corner (gamma_{n-1} = zeta_{n-1}) in %d/60000 chains"
   % eq_last_rec, eq_last_rec == 60000)

# How sharp is the constant 2?  Lemma 10.3 makes (Delta_2,...,Delta_{n-1}) FREE positive reals
# (given any y_2<...<y_n put x_j = e^{y_j}/(1+e^{y_j}), l_k = T(x_{k+1}-x_k)), so the exact
# minimum of e^{Delta_k} subject to zeta_j <= eps for all j >= k is a backward recursion:
#   4/zeta_j = c_{j+1}(E-2+1/E) + E - 1/E,  c = coth(Delta_{j+1}/2) = 1+gamma_{j+1},  E = e^{Delta_j};
# put zeta_j = eps (the binding constraint) and solve (c+1)E^2 - (4/eps+2c)E + (c-1) = 0.
# gamma_j increases with gamma_{j+1}, so iterating upward from gamma_n = 0 maximises gamma_k,
# i.e. minimises e^{Delta_k}.  Theorem 11.1 drops the term (c-1)/E, which is exactly the gap.
def Emin(eps, ncorners):
    g = 0.0
    E = float('inf')
    for _ in range(ncorners):
        c = 1.0 + g
        A, B, C = c + 1.0, -(4.0 / eps + 2.0 * c), c - 1.0
        E = (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
        g = 2.0 / (E - 1.0)
    return E

print("   EXACT minimum of e^{Delta_k} over all-weak chains (m = number of corners j >= k):")
print("     eps      m=1        m=2        m=3        m=10       m->inf      2/eps      ratio")
rows = []
for eps in (0.3, 0.1, 0.03, 0.01, 0.003):
    vals = [Emin(eps, m) for m in (1, 2, 3, 10, 400)]
    rows.append((eps, vals[-1]))
    print("    %6g  " % eps + "  ".join("%9.4f" % v for v in vals)
          + "  %9.4f  %.6f" % (2 / eps, vals[-1] * eps / 2))
ok("the exact minimum is >= 2/eps for every eps (Theorem 11.1 holds, and is never violated)",
   all(v * e / 2 >= 1 for e, v in rows))
ok("the constant 2 is sharp only ASYMPTOTICALLY: (eps/2) min e^{Delta} = %.4f at eps=0.3 and "
   "%.6f at eps=0.003" % (rows[0][1] * 0.3 / 2, rows[-1][1] * 0.003 / 2),
   rows[0][1] * 0.3 / 2 > 1.02 and abs(rows[-1][1] * 0.003 / 2 - 1) < 1e-5)
ok("the exact minima reproduce REF-P6-0's 20.05, 66.68, 200.0, 666.7 at eps=0.1,0.03,0.01,0.003",
   all(abs(Emin(e, 400) - t) < 5e-3 * t
       for e, t in ((0.1, 20.05), (0.03, 66.68), (0.01, 200.0), (0.003, 666.7))))
ok("but REF-P6-0's eps=0.3 entry 6.75, quoted verbatim in the document's verdict box, is BELOW "
   "the exact minimum %.4f and is therefore not attainable" % Emin(0.3, 400), Emin(0.3, 400) > 6.75)
print("   CAUTION: a naive float minimisation over the LENGTHS drives l_2/l_1 ~ 1e-15 and loses")
print("   all precision in T - L_k; it then reports e^{Delta_2} = 6.40 at eps = 0.3, i.e. BELOW")
print("   the theorem.  The exact recomputation of that point gives e^{Delta_2} = 6.979, zeta_2 =")
print("   0.29922: no violation.  Optimise in the modular variables (Lemma 10.3), not in lengths.")

print("\n=== (c) Corollary 11.2 and the pair-only hypothesis ===")
worstadm = math.inf
for _ in range(200000):
    n = random.randint(4, 9)
    l = [math.exp(random.uniform(-8, 8)) for _ in range(n)]
    zP, E = chain_f(l)
    if not zP or min(zP) <= 0 or not all(math.isfinite(t) for t in E):
        continue
    z = [t * random.uniform(0.5, 1.0) for t in zP]      # s_j/(2 lambda_j) in [1/2,1]
    for i in range(len(z)):
        eps = max(z[i:])
        if eps >= 1:
            continue
        worstadm = min(worstadm, E[i] * eps)
ok("Cor 11.2: eps e^{Delta_k} >= 1 for admissible s_j (min = %.6f)" % worstadm, worstadm >= 1)
# pair-only
bestpair = math.inf
for _ in range(400000):
    n = random.randint(4, 8)
    l = [math.exp(random.uniform(-7, 7)) for _ in range(n)]
    z, E = chain_f(l)
    if len(z) < 2 or min(z) <= 0 or not all(math.isfinite(t) for t in E):
        continue
    for i in range(len(z) - 1):
        if max(z[i], z[i + 1]) <= 0.01:
            bestpair = min(bestpair, E[i])
ok("with only the PAIR weak (zeta_k,zeta_{k+1} <= 0.01) the separation stays O(1): "
   "min e^{Delta_k} found = %.3f  <<  2/eps = 200" % bestpair, bestpair < 20)

print("\n=== (d) Corollary 12.6 asymptotics, and the chordal variant that avoids (U) ===")
def excess(scale, chordal):
    """max over random Phi-vectors with Phi_k <= scale of (bound / (sum sqrt(Phi_k))^2) - 1."""
    w = 0.0
    for k in range(1, 8):
        for _ in range(20000):
            P = [scale * 10 ** random.uniform(-4, 0) for _ in range(k)]
            if chordal:
                dtot = sum(math.sqrt(2 - 2 * math.exp(-t)) for t in P)
                if dtot ** 2 >= 2:
                    continue
                tot = -math.log(1 - dtot ** 2 / 2)
            else:
                A = [math.acos(math.exp(-t)) for t in P]
                if sum(A) >= math.pi / 2:
                    continue
                tot = -math.log(math.cos(sum(A)))
            pred = (sum(math.sqrt(t) for t in P)) ** 2
            w = max(w, tot / pred - 1)
    return w
eA = [excess(s0, False) for s0 in (1e-2, 1e-4, 1e-6)]
eC = [excess(s0, True) for s0 in (1e-2, 1e-4, 1e-6)]
print("   max relative excess of the exact bound over (sum sqrt(Phi_k))^2, Phi_k <= 1e-2/1e-4/1e-6:")
print("     angle route  (34): %.2e  %.2e  %.2e" % tuple(eA))
print("     chordal route    : %.2e  %.2e  %.2e" % tuple(eC))
ok("(35) Phi_tot <= (sum sqrt(Phi_k))^2 (1+o(1)): the excess vanishes as Phi -> 0 "
   "(angle route, Cor 12.6 as written)", eA[0] > eA[1] > eA[2] and eA[2] < 1e-5)
ok("chordal route (Bures DISTANCE triangle inequality, Alberti-Uhlmann 2002 Prop. 1(1) p.3, "
   "no Hypothesis (U)) gives the SAME second-order bound", eC[0] > eC[1] > eC[2] and eC[2] < 1e-5)

print("\n=== (e) Box [G5] / Prop 13.1: the normalisation of the FHSW weight ===")
def integrate(f, a=-40.0, b=40.0, n=400001):
    h = (b - a) / (n - 1)
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n - 1):
        s += f(a + i * h)
    return s * h
doc = integrate(lambda t: (math.pi / 2) / (math.cosh(2 * math.pi * t) + 1))
fhsw = integrate(lambda t: math.pi / (math.cosh(2 * math.pi * t) + 1))
print("   document Box [G5]:  int (pi/2)(cosh 2 pi t + 1)^{-1} dt = %.10f" % doc)
print("   FHSW eq. (26)    :  int  pi   (cosh 2 pi t + 1)^{-1} dt = %.10f" % fhsw)
ok("FHSW's p(t) = pi/(cosh 2 pi t + 1) is the probability density (integral 1)",
   abs(fhsw - 1) < 1e-9)
ok("the document's dmu(t) = (pi/2)(cosh 2 pi t + 1)^{-1} dt has TOTAL MASS 1/2, so it is NOT a "
   "probability measure (Prop 13.1 step <1>1 asserts that it is)", abs(doc - 0.5) < 1e-9)

print("\n%d FAILURES" % len(FAILS))
for f in FAILS:
    print("   FAIL: " + f)
