"""REF-P6-3: independent check of rigor/network_corner_calculus.tex, sections 3-9.

Everything here is EXACT rational arithmetic.  The composite point map of a protocol is
built as a genuine piecewise-Moebius object (list of (x_left, x_right, 2x2 matrix over Q)),
its breakpoints are computed by pushing the breakpoints of the outer maps back through the
inner ones, and the Schwarzian masses are read off as exact jumps of v = Phi''/Phi' = -2c/(cx+d).
Nothing is taken from the document: the maps, the corners and the sigma's are re-derived
from the conventions of rigor/phase6_brief.md.

Checks
  A. Schwarzian mass of a single parabolic compression: -2 sigma from EITHER side (Lem 4.3).
  B. Exact composite masses vs. Thm 5.2 (general rule) and vs. Thm 5.3 (under (H)),
     over random protocols in three classes:
       (i)  single-interval conditioning, starting block with >= 2 chain intervals;
       (ii) single-interval conditioning, starting block a SINGLE chain interval;
       (iii) arbitrary (union) conditioning regions.
     For each we also decide (H) directly from its definition.
  C. REF-P6-0's counterexample recomputed from scratch (exact).
  D. Prop 5.4(a): sufficiency (over (i)) and non-necessity (VWZ 1(B)).
  E. VWZ 1(B) = 1(A); Protocol 3 both orders; s' vs 2 lambda'; zeta_eff.
  F. Tables 1-3 of the document, every entry, re-enumerated independently.
Run: python3 rigor/ref_p6_3_calculus.py
"""
from fractions import Fraction as Q
from itertools import permutations
import random

FAILS = []
def ok(name, cond):
    print(("PASS  " if cond else "**FAIL** ") + name)
    if not cond:
        FAILS.append(name)

# ------------------------------------------------------------------ Moebius algebra
def mat_apply(M, x):
    a, b, c, d = M
    return (a * x + b) / (c * x + d)

def mat_inv_apply(M, y):
    a, b, c, d = M
    return (d * y - b) / (-c * y + a)

def mat_mul(M, N):                      # (M o N)
    a, b, c, d = M
    e, f, g, h = N
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)

def mat_deriv(M, x):
    a, b, c, d = M
    return (a * d - b * c) / (c * x + d) ** 2

def mat_v(M, x):                        # v = M''/M' = -2c/(cx+d)
    a, b, c, d = M
    return Q(-2) * c / (c * x + d)

ID = (Q(1), Q(0), Q(0), Q(1))

def R_mat(p, s):                        # x -> p + (x-p)/(1+s(x-p))
    return (1 + s * p, -s * p * p, s, 1 - s * p)

def L_mat(p, s):                        # x -> p + (x-p)/(1-s(x-p))
    return (1 - s * p, s * p * p, -s, 1 + s * p)

# A piecewise-Moebius map is [(lo, hi, M), ...] with lo < hi (Q or None for +-inf).
def pw_step(p, s, side, lo, hi):
    """the step map on (lo,hi): compression toward p from `side` ('R' or 'L').
    A degenerate piece (the corner sitting on the boundary of the domain) is dropped:
    the corner then carries no mass IN the domain (document Remark 7.4)."""
    if side == 'R':
        out = [(lo, p, ID), (p, hi, R_mat(p, s))]
    else:
        out = [(lo, p, L_mat(p, s)), (p, hi, ID)]
    return [(a, b, M) for a, b, M in out if a < b]

def pw_apply(F, x):
    for lo, hi, M in F:
        if (lo is None or x >= lo) and (hi is None or x <= hi):
            return mat_apply(M, x)
    raise ValueError("outside domain")

def pw_compose(Fout, Fin):
    """Fout o Fin as a piecewise-Moebius map on the domain of Fin."""
    out = []
    for lo, hi, N in Fin:
        # split (lo,hi) at the preimages under N of the breakpoints of Fout
        cuts = [lo]
        for lo2, hi2, _ in Fout:
            for q in (lo2, hi2):
                if q is None:
                    continue
                den = -N[2] * q + N[0]
                if den == 0:
                    continue
                x = mat_inv_apply(N, q)
                if lo < x < hi:
                    cuts.append(x)
        cuts.append(hi)
        cuts = sorted(set(cuts))
        for u, w in zip(cuts[:-1], cuts[1:]):
            if u >= w:
                continue
            mid = (u + w) / 2
            y = mat_apply(N, mid)
            M = None
            for lo2, hi2, M2 in Fout:
                if lo2 <= y <= hi2:
                    M = M2
                    break
            if M is None:
                raise ValueError("image leaves the domain of the outer map")
            out.append((u, w, mat_mul(M, N)))
    # merge equal neighbours
    merged = [out[0]]
    for piece in out[1:]:
        lo, hi, M = piece
        plo, phi, PM = merged[-1]
        if M == PM:
            merged[-1] = (plo, hi, M)
        else:
            merged.append(piece)
    return merged

def pw_masses(F):
    """exact Schwarzian masses {breakpoint: jump of v} of a piecewise-Moebius map."""
    m = {}
    for (lo1, hi1, M1), (lo2, hi2, M2) in zip(F[:-1], F[1:]):
        q = hi1
        j = mat_v(M2, q) - mat_v(M1, q)
        if j != 0:
            m[q] = m.get(q, Q(0)) + j
    return m

# ------------------------------------------------------------------ protocols
def sigma(lB, lnew, s=None):
    s = 2 * Q(lnew) / Q(lB) if s is None else s
    return s / (Q(lB) + Q(lnew))

class Protocol:
    """one-sided protocol on a chain of n intervals with lengths l[0..n-1]."""
    def __init__(self, lens, i0, j0):
        self.l = [Q(x) for x in lens]
        self.n = len(lens)
        self.p = [Q(0)]
        for x in self.l:
            self.p.append(self.p[-1] + x)      # p[k] = p_{k+1}
        self.lo, self.hi = i0, j0              # block = A_{lo}..A_{hi}, 1-based
        self.steps = []                        # (corner, sigma, side, Mlo, Mhi)

    def point(self, k):                        # p_k, 1-based
        return self.p[k - 1]

    def add(self, side, nB):
        """adjoin one interval on `side`, conditioning on nB chain intervals of the block."""
        if side == 'R':
            assert self.hi < self.n and 1 <= nB <= self.hi - self.lo + 1
            kB_lo, kB_hi = self.hi - nB + 1, self.hi           # A_B = A_{kB_lo}..A_{kB_hi}
            new = self.hi + 1
            corner = self.point(kB_lo)                          # far end of A_B
            lB = self.point(kB_hi + 1) - self.point(kB_lo)
            ln = self.l[new - 1]
            s = sigma(lB, ln)
            Mlo, Mhi = corner, self.point(new + 1)              # moving part
            self.steps.append((corner, s, 'R', Mlo, Mhi))
            self.hi = new
        else:
            assert self.lo > 1 and 1 <= nB <= self.hi - self.lo + 1
            kB_lo, kB_hi = self.lo, self.lo + nB - 1
            new = self.lo - 1
            corner = self.point(kB_hi + 1)
            lB = self.point(kB_hi + 1) - self.point(kB_lo)
            ln = self.l[new - 1]
            s = sigma(lB, ln)
            Mlo, Mhi = self.point(new), corner
            self.steps.append((corner, s, 'L', Mlo, Mhi))
            self.lo = new
        return self

    def block(self):
        return self.point(self.lo), self.point(self.hi + 1)

    def H(self):
        """hypothesis (H): no earlier corner in the INTERIOR of a later moving part."""
        for m in range(len(self.steps)):
            for mp in range(m + 1, len(self.steps)):
                pm = self.steps[m][0]
                _, _, _, lo, hi = self.steps[mp]
                if lo < pm < hi:
                    return False
        return True

    def composite(self):
        """Phi = k_1 o ... o k_N as an exact piecewise-Moebius map on the final block."""
        # domains: k_m maps J_m -> J_{m-1}.  Build J_m from the step record backwards.
        # reconstruct the block after each step
        blocks = []
        lo, hi = self.lo, self.hi                                # final block
        # undo the steps to get J_0 .. J_N
        los, his = [lo], [hi]
        for (corner, s, side, Mlo, Mhi) in reversed(self.steps):
            if side == 'R':
                hi -= 1
            else:
                lo += 1
            los.append(lo); his.append(hi)
        los.reverse(); his.reverse()                              # los[m],his[m] = J_m
        Phi = None
        for m, (corner, s, side, Mlo, Mhi) in enumerate(self.steps):
            dom = (self.point(los[m + 1]), self.point(his[m + 1] + 1))   # J_m
            km = pw_step(corner, s, side, dom[0], dom[1])
            Phi = km if Phi is None else pw_compose(Phi, km)
        return Phi

    def naive_measure(self):
        m = {}
        for (corner, s, side, Mlo, Mhi) in self.steps:
            m[corner] = m.get(corner, Q(0)) + s
        return {k: -2 * v for k, v in m.items()}

    def thm52_measure(self):
        """Thm 5.2: masses -2 sigma_m G_m'(x_m) at x_m = G_m^{-1}(p^(m)), G_m = k_{m+1}o..ok_N."""
        los, his = [self.lo], [self.hi]
        lo, hi = self.lo, self.hi
        for (corner, s, side, Mlo, Mhi) in reversed(self.steps):
            if side == 'R':
                hi -= 1
            else:
                lo += 1
            los.append(lo); his.append(hi)
        los.reverse(); his.reverse()
        N = len(self.steps)
        # G_m for m = 0..N (0-based: G_m = k_{m+1} o ... o k_N)
        Gs = [None] * (N + 1)
        Gs[N] = [(self.point(los[N]), self.point(his[N] + 1), ID)]
        for m in range(N - 1, -1, -1):
            dom = (self.point(los[m + 1]), self.point(his[m + 1] + 1))
            km = pw_step(*self.steps[m][0:3], dom[0], dom[1])
            Gs[m] = km if Gs[m + 1] is None else pw_compose(km, Gs[m + 1])
        out = {}
        JN = (self.point(self.lo), self.point(self.hi + 1))
        for m in range(N):
            corner, s = self.steps[m][0], self.steps[m][1]
            G = Gs[m + 1] if m + 1 <= N else None
            G = Gs[m + 1]
            # x_m with G(x_m) = corner, if corner is in the range of G
            xm = None
            for lo2, hi2, M in G:
                a, b = mat_apply(M, lo2), mat_apply(M, hi2)
                if a <= corner <= b:
                    xm = mat_inv_apply(M, corner)
                    dG = mat_deriv(M, xm)
                    break
            if xm is None:
                continue                      # corner swallowed
            if not (JN[0] <= xm <= JN[1]):
                continue
            out[xm] = out.get(xm, Q(0)) - 2 * s * dG
        return out

# ------------------------------------------------------------------ A. single corner
print("=== A. the mass of a single parabolic corner is -2 sigma from either side (Lem 4.3) ===")
badA = 0
for _ in range(2000):
    p = Q(random.randint(-30, 30), random.randint(1, 9))
    s = Q(random.randint(1, 40), random.randint(1, 20))
    for side, mk in (('R', R_mat), ('L', L_mat)):
        F = pw_step(p, s, side, p - 5, p + 5)
        m = pw_masses(F)
        if list(m.keys()) != [p] or m[p] != -2 * s:
            badA += 1
        # C^1: the two pieces agree in value and first derivative at p
        M1, M2 = F[0][2], F[1][2]
        if mat_apply(M1, p) != mat_apply(M2, p) or mat_deriv(M1, p) != mat_deriv(M2, p):
            badA += 1
ok("2000 random corners: C^1 at p and [v]_p = -2 sigma for R and for L (%d bad)" % badA, badA == 0)
print("   sign convention: kappa := -[v]_p/2 = +sigma > 0 for a compression toward p from EITHER side.")

# ------------------------------------------------------------------ B. random protocols
print("\n=== B. random protocols: exact masses vs Thm 5.2 / Thm 5.3, and (H) ===")
random.seed(20260916)
stat = {}
for cls in ('i_single_start2', 'ii_single_start1', 'iii_union'):
    n_ok52 = n_ok53 = n_H = n_tot = n_H_and_53 = n_notH_and_53 = 0
    for trial in range(400):
        n = random.randint(3, 6)
        lens = [Q(random.randint(1, 40), random.randint(1, 7)) for _ in range(n)]
        if cls == 'ii_single_start1':
            i0 = random.randint(1, n); j0 = i0
        else:
            i0 = random.randint(1, n - 1); j0 = i0 + 1
        P = Protocol(lens, i0, j0)
        while P.lo > 1 or P.hi < n:
            sides = (['L'] if P.lo > 1 else []) + (['R'] if P.hi < n else [])
            side = random.choice(sides)
            width = P.hi - P.lo + 1
            nB = 1 if cls != 'iii_union' else random.randint(1, width)
            P.add(side, nB)
        if not P.steps:
            continue
        n_tot += 1
        Phi = P.composite()
        JN = (P.point(P.lo), P.point(P.hi + 1))
        inside = lambda D: {k: v for k, v in D.items() if JN[0] < k < JN[1] and v != 0}
        exact = inside(pw_masses(Phi))
        pred52 = inside(P.thm52_measure())
        pred53 = inside(P.naive_measure())
        good52 = (set(exact) == set(pred52)) and all(exact[k] == pred52[k] for k in exact)
        good53 = (set(exact) == set(pred53)) and all(exact[k] == pred53[k] for k in exact)
        n_ok52 += good52
        n_ok53 += good53
        h = P.H()
        n_H += h
        if h:
            n_H_and_53 += good53
        else:
            n_notH_and_53 += good53
    stat[cls] = (n_tot, n_ok52, n_ok53, n_H, n_H_and_53, n_notH_and_53)
    print("   class %-16s  protocols %3d | Thm5.2 exact %3d | naive(Thm5.3) exact %3d | (H) holds %3d"
          % (cls, n_tot, n_ok52, n_ok53, n_H))

for cls in stat:
    n_tot, n_ok52, n_ok53, n_H, n_H_53, n_notH_53 = stat[cls]
    ok("  %-16s: Thm 5.2 (general rule) exact in every case" % cls, n_ok52 == n_tot)
    ok("  %-16s: under (H) the naive corner measure is exact in every case" % cls, n_H_53 == n_H)
ok("class (i)  single-interval conditioning + start >= 2 intervals  ==> (H) ALWAYS (Prop 5.4(a))",
   stat['i_single_start2'][3] == stat['i_single_start2'][0])
ok("class (ii) single-interval conditioning + SINGLE-interval start ==> (H) sometimes FAILS",
   stat['ii_single_start1'][3] < stat['ii_single_start1'][0])
ok("class (iii) union conditioning ==> (H) sometimes FAILS",
   stat['iii_union'][3] < stat['iii_union'][0])
ok("whenever (H) FAILS the naive corner measure is WRONG in at least one case",
   any(stat[c][0] - stat[c][3] > 0 and stat[c][5] < stat[c][0] - stat[c][3] for c in stat))
nfail = sum(stat[c][0] - stat[c][3] for c in stat)
nfail_naive_ok = sum(stat[c][5] for c in stat)
print("   (H) fails in %d of %d protocols; of those the naive measure still happens to be right in %d"
      % (nfail, sum(stat[c][0] for c in stat), nfail_naive_ok))

# ------------------------------------------------------------------ C. REF-P6-0 counterexample
print("\n=== C. REF-P6-0's counterexample, recomputed from scratch (exact) ===")
lens = [Q(13, 10), Q(21, 10), Q(9, 10), Q(17, 10)]
P = Protocol(lens, 2, 3)
P.add('R', 1)            # adjoin A_4 conditioning on A_3 (single)  -> corner p_3
P.add('L', 2)            # adjoin A_1 conditioning on A_2 u A_3     -> corner p_4
s1 = P.steps[0][1]; s2 = P.steps[1][1]
ok("sigma_1 = 2 l_4/(l_3(l_3+l_4)) = %.6f  (document 1.452991)" % float(s1),
   s1 == 2 * lens[3] / (lens[2] * (lens[2] + lens[3])) and abs(float(s1) - 1.452991) < 1e-6)
ok("sigma_2 = 2 l_1/((l_2+l_3)(l_1+l_2+l_3)) = %.6f  (document 0.201550)" % float(s2),
   s2 == 2 * lens[0] / ((lens[1] + lens[2]) * (lens[0] + lens[1] + lens[2]))
   and abs(float(s2) - 0.201550) < 1e-6)
ok("(H) fails: p_3 = %.1f is interior to M_2 = (%.1f, %.1f)"
   % (float(P.point(3)), float(P.steps[1][3]), float(P.steps[1][4])), not P.H())
ex = pw_masses(P.composite())
th = P.thm52_measure()
print("   exact masses of Phi : %s" % {float(k): float(v) for k, v in sorted(ex.items())})
print("   Thm 5.2 prediction  : %s" % {float(k): float(v) for k, v in sorted(th.items())})
x0 = [k for k in ex if k != P.point(4)][0]
ok("mass at x_0 = k_2^{-1}(p_3) = %.6f  (document 3.200568)" % float(x0),
   abs(float(x0) - 3.200568) < 1e-6)
k2 = pw_step(*P.steps[1][0:3], P.point(1), P.point(4))
dk2 = [mat_deriv(M, x0) for lo, hi, M in k2 if lo <= x0 <= hi][0]
ok("k_2'(x_0) = %.6f  (document 0.670114) and mass = -2 sigma_1 k_2'(x_0) = %.6f (document -1.947339)"
   % (float(dk2), float(ex[x0])), abs(float(dk2) - 0.670114) < 1e-6
   and ex[x0] == -2 * s1 * dk2 and abs(float(ex[x0]) + 1.947339) < 1e-6)
ok("NO mass at the junction p_3 (exact: %s)" % ex.get(P.point(3), Q(0)),
   P.point(3) not in ex)
ok("mass -2 sigma_2 at p_4 = %.6f" % float(ex[P.point(4)]), ex[P.point(4)] == -2 * s2)
tot = sum(ex.values()); naive = -2 * (s1 + s2)
ok("total mass %.6f is %.2f%% of the naive %.6f (document: 71%%)"
   % (float(tot), 100 * float(tot / naive), float(naive)),
   abs(100 * float(tot / naive) - 71.0) < 0.5)
# control of the document: the same geometry with A_B = A_2
P2 = Protocol(lens, 2, 3); P2.add('R', 1); P2.add('L', 1)
ex2 = pw_masses(P2.composite())
ok("control (A_B = A_2, single): both corners at p_3 and the masses ADD exactly (%s)"
   % {float(k): float(v) for k, v in ex2.items()},
   set(ex2) == {P2.point(3)} and ex2[P2.point(3)] == -2 * (P2.steps[0][1] + P2.steps[1][1]))

# ------------------------------------------------------------------ D. Example 5.6
print("\n=== D. Example 5.6 (swallowed corner) recomputed ===")
P = Protocol([1, 1, 1], 2, 2)
P.add('R', 1)            # A_3 on A_2, corner = far end p_2
P.add('L', 1)            # A_1 on A_2, corner = p_3
ok("both conditioning regions are single chain intervals, yet (H) FAILS", not P.H())
ok("sigma_1 = sigma_2 = 1", P.steps[0][1] == 1 and P.steps[1][1] == 1)
exS = pw_masses(P.composite())
ok("S(Phi) = -2 delta_{p_3} only (exact: %s); the first corner contributes NOTHING"
   % {float(k): float(v) for k, v in exS.items()},
   set(exS) == {P.point(3)} and exS[P.point(3)] == Q(-2))
k2 = pw_step(*P.steps[1][0:3], P.point(1), P.point(3))
img = (mat_apply(k2[0][2], P.point(1)), P.point(3))
ok("range of k_2 is (%s, %s), which does NOT contain p_2 = %s"
   % (img[0], img[1], P.point(2)), img[0] > P.point(2))

# ------------------------------------------------------------------ E. VWZ
print("\n=== E. VWZ protocols (exact) ===")
a, b, c, d = Q(3, 7), Q(5, 4), Q(9, 8), Q(2, 3)
ok("1(B) = 1(A): 2c/(b(b+c)) + 2d/((b+c)(b+c+d)) = 2(c+d)/(b(b+c+d))",
   sigma(b, c) + sigma(b + c, d) == sigma(b, c + d))
badid = 0
for _ in range(20000):
    rr = lambda: Q(random.randint(1, 60), random.randint(1, 17))
    bb, cc, dd = rr(), rr(), rr()
    if sigma(bb, cc) + sigma(bb + cc, dd) != sigma(bb, cc + dd):
        badid += 1
ok("  ... identically in 20000 random rational (b,c,d) (%d bad)" % badid, badid == 0)
P = [Q(0), a, a + b, a + b + c, a + b + c + d]
f1A = pw_step(P[1], sigma(b, c + d), 'R', P[0], P[4])
f1B = pw_compose(pw_step(P[1], sigma(b, c), 'R', P[0], P[3]),
                 pw_step(P[1], sigma(b + c, d), 'R', P[0], P[4]))
same = all(mat_apply(M, (lo + hi) / 2) == mat_apply(
    [MM for l2, h2, MM in f1A if l2 <= (lo + hi) / 2 <= h2][0], (lo + hi) / 2)
    for lo, hi, M in f1B)
ok("1(B) and 1(A) are the SAME point map, exactly (not merely modulo Moebius)", same)
s31, s32 = sigma(b, a), sigma(c, d)
ok("Protocol 3: sigma_1 = 2a/(b(a+b)) and sigma_2 = 2d/(c(c+d))",
   s31 == 2 * a / (b * (a + b)) and s32 == 2 * d / (c * (c + d)))
P3a = pw_compose(pw_step(P[2], s31, 'L', P[0], P[3]), pw_step(P[2], s32, 'R', P[0], P[4]))
P3b = pw_compose(pw_step(P[2], s32, 'R', P[1], P[4]), pw_step(P[2], s31, 'L', P[0], P[4]))
pts = [Q(i, 37) * P[4] for i in range(1, 37)]
ok("Protocol 3 in either order: LITERALLY the same point map (exact, 36 points)",
   all(pw_apply(P3a, x) == pw_apply(P3b, x) for x in pts))
m3 = pw_masses(P3a)
ok("S(Phi^(3)) = -2(sigma_1+sigma_2) delta_{p_3}",
   set(m3) == {P[2]} and m3[P[2]] == -2 * (s31 + s32))
sprime = (s31 + s32) * (c + d)
ok("s' = (sigma_1+sigma_2)(c+d) >= 2 lambda' = 2d/c  (s' = %s, 2d/c = %s)" % (sprime, 2 * d / c),
   sprime >= 2 * d / c)
bad2 = bad1 = 0
for _ in range(50000):
    rr = lambda: Q(random.randint(1, 80), random.randint(1, 23))
    aa, bb, cc, dd = rr(), rr(), rr(), rr()
    sp = (sigma(bb, aa) + sigma(cc, dd)) * (cc + dd)
    if sp < 2 * dd / cc:
        bad2 += 1
    if sp < dd / cc:
        bad1 += 1
ok("s' > 2 lambda' STRICTLY for all a,b,c,d > 0 (50000 rational cases, %d bad)" % bad2, bad2 == 0)
zeff = (s31 + s32) * (a + b) * (c + d) / (a + b + c + d)
bI = (P[2] - P[0]) * (P[4] - P[2]) / (P[4] - P[0])
ok("zeta_eff = (sigma_1+sigma_2) beta_I(p_3) = %s" % zeff, zeff == (s31 + s32) * bI)
# Moebius factor: pole location
pole = P[2] + 1 / s31
img_hi = mat_apply(R_mat(P[2], s31 + s32), P[4])
ok("the Moebius factor M has its pole at p_3 + 1/sigma_1 = %s, outside the image (max %s)"
   % (pole, img_hi), pole > img_hi)

# ------------------------------------------------------------------ F. Tables
print("\n=== F. Tables 1-3 of the document, re-enumerated independently ===")
def enumerate_pairs(lens):
    n = len(lens)
    res = {}
    for i in range(1, n):
        moves = ['L'] * (i - 1) + ['R'] * (n - i - 1)
        for order in sorted(set(permutations(moves))):
            P = Protocol(lens, i, i + 1)
            for mv in order:
                P.add(mv, 1)
            res[(i, ''.join(order))] = P
    return res

for n, lens, want in (
        (4, [1, 1, 1, 1], {1: {2: '0.75', 3: '1'}, 2: {3: '2'}, 3: {3: '1', 4: '0.75'}}),
        (5, [Q(1), Q(13, 10), Q(7, 10), Q(19, 10), Q(11, 10)],
         {1: {2: '0.4487', 3: '2.9614', 4: '0.5789'},
          2: {3: '3.9101', 4: '0.5789'},
          3: {3: '0.9487', 4: '3.3647'},
          4: {3: '0.9487', 4: '2.7857', 5: '0.2546'}})):
    res = enumerate_pairs([Q(x) for x in lens])
    classes = {}
    for (i, order), P in res.items():
        key = tuple(sorted(P.naive_measure().items()))
        classes.setdefault(key, []).append((i, order))
    ok("n=%d: %d protocols with a starting pair, %d distinct corner measures (claim n-1 = %d)"
       % (n, len(res), len(classes), n - 1), len(res) == 2 ** (n - 2) and len(classes) == n - 1)
    ok("n=%d: the corner measure depends only on the starting pair" % n,
       all(len(set(i for i, o in v)) == 1 for v in classes.values()))
    T = sum(Q(x) for x in lens)
    for i in range(1, n):
        P = [p for (ii, o), p in res.items() if ii == i][0]
        exact = pw_masses(P.composite())
        naive = {k: v for k, v in P.naive_measure().items()}
        ok("  n=%d start A_%dA_%d: exact S(Phi) = naive corner measure, and (H) holds"
           % (n, i, i + 1), exact == naive and P.H())
        zz = {}
        for k, v in sorted(naive.items()):
            kk = [j for j in range(1, n + 2) if P.point(j) == k][0]
            zz[kk] = (-v / 2) * (k - P.point(1)) * (P.point(n + 1) - k) / T
        got = {k: "%.4g" % float(v) for k, v in zz.items()}
        target = want[i]
        ok("  n=%d start A_%dA_%d: zeta^(I) = %s  (table: %s)" % (n, i, i + 1, got, target),
           all(abs(float(got[k]) - float(target[k])) <= 5e-4 * max(1, abs(float(target[k])))
               for k in target) and set(got) == set(target))

# Table 3 (union variants)
print("   Table 3 (union-conditioning variants, n=4):")
lens4 = [a, b, c, d]
cases = {
    "1(B)  P_{B->BC},P_{BC->BCD}": (2, 2, [('R', 1), ('R', 2)]),
    "2     P_{B->BC},P_{C->CD}":   (1, 2, [('R', 1), ('R', 1)]),
    "3     P_{B->AB},P_{C->CD}":   (2, 3, [('L', 1), ('R', 1)]),
    "--    P_{C->CD},P_{BC->ABC}": (2, 3, [('R', 1), ('L', 2)]),
}
P1A = Protocol([a, b, c + d], 1, 2)        # coarse chain A|B|CD: A_new = CD is a UNION,
P1A.add('R', 1)                            # so (C3) covers it only after coarsening
ex1A = pw_masses(P1A.composite())
ok("      1(A) P_{B->BCD}: one corner at p_2 with sigma = 2(c+d)/(b(b+c+d)), (H) holds",
   P1A.H() and set(ex1A) == {P1A.point(2)}
   and ex1A[P1A.point(2)] == -2 * (2 * (c + d) / (b * (b + c + d))))
print("      NOTE: 1(A) has A_new = CD, a UNION of two chain intervals; (C3) of the document")
print("            admits only a single chain interval as A_new, so 1(A) needs the coarse chain.")
for name, (i0, j0, moves) in cases.items():
    P = Protocol(lens4, i0, j0)
    for mv, nB in moves:
        P.add(mv, nB)
    exact = pw_masses(P.composite())
    naive = {k: v for k, v in P.naive_measure().items()}
    JN = (P.point(P.lo), P.point(P.hi + 1))
    naive = {k: v for k, v in naive.items() if JN[0] < k < JN[1]}
    corners = sorted(set(float(s[0]) for s in P.steps))
    print("      %-30s corners %s  (H)=%s  exact==naive: %s"
          % (name, corners, P.H(), exact == naive))
    ok("      %-30s (H) and the corner measure as claimed" % name,
       (P.H() and exact == naive) or (not P.H() and exact != naive))

print("\n%d FAILURES" % len(FAILS))
for f in FAILS:
    print("   FAIL: " + f)
