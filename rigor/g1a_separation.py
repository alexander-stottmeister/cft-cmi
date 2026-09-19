"""G1a: the modular form of the L->R Petz-chain corner data and the separation theorem
of rigor/network_corner_calculus.tex.

Claims checked (conventions rigor/phase6_brief.md):
  (i)   zeta_k^(I) = sinh(D_{k+1}/2) / (sinh(D_k/2) sinh((D_k+D_{k+1})/2)),  D_j = y_{j+1}-y_j
        the modular length of A_j, y_j = log((p_j-p_1)/(p_{n+1}-p_j));  D_n = +infinity.
  (ii)  1/zeta_k = sinh^2(D_k/2) coth(D_{k+1}/2) + (1/2) sinh(D_k)   (equivalent form).
  (iii) (e^{D_k}-1) zeta_k = 2 r_k (1+v_k)/(1+r_k) >= 2 r_k/(1+r_k)  (exact, REF-P6-0 (6)).
  (iv)  e^{D_k} <= 1 + 2/zeta_k, STRICT for k <= n-2 and an EQUALITY at k = n-1
        (repaired after REF-P6-3: the document's first version printed the strict form).
  (v)   SEPARATION THEOREM: if zeta_j <= eps < 2 for every corner j >= k, then
        e^{D_k} >= 2/eps; for the last corner e^{D_{n-1}} >= 1 + 2/eps.
        Sharpness: ref_p6_0_separation.out finds min e^{D} = 2/eps to 4 digits.
  (vi)  admissible case s_j >= lambda_j: zeta_j <= eps for all j => e^{D_k} >= 1/eps.
Run: python3 rigor/g1a_separation.py
"""
import numpy as np
ok = lambda name, c: print(("PASS  " if c else "**FAIL** ") + name)
rng = np.random.default_rng(11)

def chain(l):
    """corner data of the L->R ordinary-Petz chain with interval lengths l_1..l_n."""
    l = np.asarray(l, float); n = len(l); L = np.cumsum(l); T = L[-1]
    x = np.concatenate(([0.0], L)) / T                    # x_j = (p_j - p_1)/T, j=1..n+1
    y = np.log(x[1:-1] / (1 - x[1:-1]))                   # y_2..y_n
    z, D, r, v = [], [], [], []
    for k in range(2, n):                                 # corners k = 2..n-1 at p_k
        lk, lk1, Lkm1, Lk = l[k - 1], l[k], L[k - 2], L[k - 1]
        z.append(2 * lk1 / (lk * (lk + lk1)) * Lkm1 * (T - Lkm1) / T)
        D.append(y[k - 1] - y[k - 2])                     # Delta_k
        r.append(lk1 / lk); v.append(lk / (T - Lk))
    return np.array(z), np.array(D), np.array(r), np.array(v)

print("=== 1. the modular identities (i)-(iv) ===")
w1 = w2 = w3 = 0.0; bad4 = bad4s = bad4eq = 0
for _ in range(50000):
    n = int(rng.integers(4, 10)); l = np.exp(rng.uniform(-7, 7, n))
    z, D, r, v = chain(l)
    m = len(z)
    for i in range(m):
        D2 = D[i + 1] if i + 1 < m else np.inf
        if np.isfinite(D2):
            pred = np.sinh(D2 / 2) / (np.sinh(D[i] / 2) * np.sinh((D[i] + D2) / 2))
            inv = np.sinh(D[i] / 2) ** 2 / np.tanh(D2 / 2) + 0.5 * np.sinh(D[i])
        else:
            pred = np.exp(-D[i] / 2) / np.sinh(D[i] / 2)
            inv = np.sinh(D[i] / 2) ** 2 + 0.5 * np.sinh(D[i])
        w1 = max(w1, abs(pred / z[i] - 1)); w2 = max(w2, abs(1 / (inv * z[i]) - 1))
        w3 = max(w3, abs((np.exp(D[i]) - 1) * z[i] / (2 * r[i] * (1 + v[i]) / (1 + r[i])) - 1))
        # (iv): <= always; STRICT for i < m-1 (k <= n-2) whenever the gap is resolvable in
        # floating point (it is O(e^{-D_{k+1}}), so we only test D_{k+1} <= 20); exact equality
        # for i = m-1 (k = n-1).
        if np.exp(D[i]) > (1 + 2 / z[i]) * (1 + 1e-9): bad4 += 1
        if i < m - 1:
            gap = (1 + 2 / z[i]) - np.exp(D[i])          # measured gap
            pred = 2 * np.sinh(D[i] / 2) ** 2 * (1 / np.tanh(D[i + 1] / 2) - 1)
            if pred > 1e-6 * max(1.0, np.exp(D[i])):     # above the float noise floor
                if gap <= 0 or abs(gap / pred - 1) > 1e-4: bad4s += 1
        else:
            if abs(np.exp(D[i]) / (1 + 2 / z[i]) - 1) > 1e-9: bad4eq += 1
ok("(i)   zeta_k = sinh(D_{k+1}/2)/(sinh(D_k/2) sinh((D_k+D_{k+1})/2))   (max rel err %.1e)" % w1,
   w1 < 1e-8)
ok("(ii)  1/zeta_k = sinh^2(D_k/2) coth(D_{k+1}/2) + sinh(D_k)/2        (max rel err %.1e)" % w2,
   w2 < 1e-8)
ok("(iii) (e^{D_k}-1) zeta_k = 2 r_k(1+v_k)/(1+r_k)                     (max rel err %.1e)" % w3,
   w3 < 1e-8)
ok("(iv)  e^{D_k} <= 1 + 2/zeta_k for all k                            (%d violations)" % bad4,
   bad4 == 0)
ok("(iv)  ... with the exact gap (1+2/zeta_k) - e^{D_k} = 2 sinh^2(D_k/2)(coth(D_{k+1}/2)-1)\n      > 0 for k <= n-2, wherever it is above the float noise floor  (%d violations)" % bad4s,
   bad4s == 0)
ok("(iv') e^{D_{n-1}} = 1 + 2/zeta_{n-1} EXACTLY (equality at the last corner) (%d violations)"
   % bad4eq, bad4eq == 0)

print("\n=== 2. separation theorem: all corners weak => e^{D_k} >= 2/eps ===")
worst = np.inf; worst_last = np.inf; arg = None
for _ in range(400000):
    n = int(rng.integers(4, 9)); l = np.exp(rng.uniform(-9, 9, n))
    z, D, r, v = chain(l)
    if not np.all(np.isfinite(z)) or z.min() <= 0: continue
    for i in range(len(z)):
        eps = z[i:].max()                 # hypothesis uses the corners j >= k only
        if eps >= 2: continue
        val = np.exp(D[i]) * eps / 2.0
        if val < worst: worst, arg = val, (l.copy(), i, eps)
    if z[-1] < 2:                     # the last corner uses zeta_{n-1} only (Thm 11.1 <1>7)
        worst_last = min(worst_last, np.exp(D[-1]) / (1 + 2 / z[-1]))
ok("min over 400000 random chains of (eps/2) e^{D_k} = %.9f  (theorem: >= 1)" % worst,
   worst >= 1 - 1e-7)
ok("min over the same chains of e^{D_{n-1}}/(1+2/zeta_{n-1}) = %.9f  (theorem: >= 1, in fact = 1)"
   % worst_last, worst_last >= 1 - 1e-7)

# directed search with the all-weak constraint (as ref_p6_0_separation.py): minimise
# e^{D_2} subject to zeta_j <= eps for EVERY corner; the theorem says the min is >= 2/eps.
print("\n  constrained minimisation of e^{D_2} at fixed eps (theorem: >= 2/eps):")
def pen_obj(loglen, eps, k=0):
    z, D, _, _ = chain(np.exp(loglen))
    if len(z) <= k or not np.all(np.isfinite(z)) or z.min() <= 0: return 1e9
    p = sum(1e3 * np.log(zz / eps) for zz in z if zz > eps)
    return D[k] + p
for eps in (0.1, 0.01):
    best = 1e9
    for trial in range(40):
        x = rng.uniform(-8, 8, 6); f = pen_obj(x, eps); step = 1.5
        for it in range(4000):
            j = rng.integers(len(x)); y2 = x.copy(); y2[j] += step * rng.normal()
            g = pen_obj(y2, eps)
            if g < f: x, f = y2, g
            if it % 500 == 499: step *= 0.6
        best = min(best, f)
    print("    eps = %-6g  min e^{D_2} = %-10.5g   2/eps = %-8g   ratio = %.5f"
          % (eps, np.exp(best), 2 / eps, np.exp(best) * eps / 2))
# the optimal chain reported by REF-P6-0 (ref_p6_0_separation.out, n = 6, eps = 0.01)
lref = np.array([1.0, 198.363, 24084.4, 37011.8, 470.506, 2.36992])
zr, Dr, _, _ = chain(lref)
print("    REF-P6-0 optimum: zeta = %s, e^{D_2} = %.4f, (eps/2)e^{D_2} = %.6f"
      % (np.array2string(zr, precision=5), np.exp(Dr[0]), np.exp(Dr[0]) * zr.max() / 2))
ok("the constant 2 is attained only as eps -> 0 (REF-P6-0 optimum gives (eps/2) e^{D} = %.6f, >= 1)"
   % (np.exp(Dr[0]) * zr.max() / 2), 1 <= np.exp(Dr[0]) * zr.max() / 2 < 1.001)

print("\n=== 3. the induction constants of the proof ===")
# gamma_j := coth(D_j/2) - 1 = 2/(e^{D_j}-1);  the proof shows gamma_j <= eps + (eps/2) gamma_{j+1},
# hence gamma_j <= 2 eps/(2-eps) and e^{D_j} >= 1 + (4/eps)/(2+gamma*) = 2/eps.
bad = 0; wg = 0.0
for _ in range(200000):
    n = int(rng.integers(4, 9)); l = np.exp(rng.uniform(-8, 8, n))
    z, D, r, v = chain(l)
    if not np.all(np.isfinite(z)) or z.min() <= 0: continue
    g = 2 / (np.exp(D) - 1)
    eps = z.max()
    if eps >= 2: continue
    for i in range(len(z)):
        gnext = g[i + 1] if i + 1 < len(z) else 0.0
        if g[i] > (z[i] + 0.5 * z[i] * gnext) * (1 + 1e-8): bad += 1
        wg = max(wg, g[i] - (2 * eps / (2 - eps)))
ok("recursion gamma_j <= zeta_j + (zeta_j/2) gamma_{j+1}  (%d violations)" % bad, bad == 0)
ok("fixed point: gamma_j <= 2 eps/(2-eps)  (max excess %.2e)" % wg, wg <= 1e-9)

print("\n=== 4. general admissible case s_j >= lambda_j ===")
# sigma_j = s_j/(l_j+l_{j+1}) with s_j >= lambda_j = l_{j+1}/l_j: zeta_j >= zeta_j^Petz/2,
# so zeta_j <= eps for all j implies zeta_j^Petz <= 2 eps and e^{D_k} >= 1/eps.
worst = np.inf
for _ in range(200000):
    n = int(rng.integers(4, 9)); l = np.exp(rng.uniform(-8, 8, n))
    zP, D, r, v = chain(l)
    if not np.all(np.isfinite(zP)) or zP.min() <= 0: continue
    ratio = rng.uniform(0.5, 1.0, len(zP))       # s_j/(2 lambda_j) in [1/2, 1]
    z = zP * ratio
    for i in range(len(z)):
        eps = z[i:].max()
        if eps >= 1: continue
        worst = min(worst, np.exp(D[i]) * eps)
ok("min over 200000 admissible chains of eps e^{D_k} = %.6f  (theorem: >= 1)" % worst, worst >= 1)

print("\n=== 5. the EXACT constrained minimum of e^{D_k} (REF-P6-3's backward recursion) ===")
# With zeta_j = eps binding for every j >= k, Lemma 10.3 gives the quadratic
#   (c_{j+1}+1) E^2 - (4/eps + 2 c_{j+1}) E + (c_{j+1}-1) = 0,  c = 1 + gamma,  gamma_j = 2/(E-1),
# iterated downward from gamma_n = 0; the root at j = k is the exact minimum of e^{D_k}.
def exact_min(eps, m):
    g = 0.0                                   # gamma_n
    for _ in range(m):
        c = 1.0 + g
        a, b, c0 = c + 1.0, -(4.0 / eps + 2.0 * c), c - 1.0
        E = (-b + np.sqrt(b * b - 4 * a * c0)) / (2 * a)
        g = 2.0 / (E - 1.0)
    return E
print("   eps      m=1        m=2        m=3        m=10       2/eps      (eps/2)min")
for eps in (0.3, 0.1, 0.03, 0.01, 0.003):
    v = [exact_min(eps, m) for m in (1, 2, 3, 10)]
    print("  %-7g %-10.4f %-10.4f %-10.4f %-10.4f %-10.4f %.6f"
          % (eps, v[0], v[1], v[2], v[3], 2 / eps, v[3] * eps / 2))
ok("the exact minimum is >= 2/eps for every eps (Theorem 11.1 is never violated)",
   all(exact_min(e, 10) >= 2 / e for e in (0.3, 0.1, 0.03, 0.01, 0.003)))
ok("the constant 2 is sharp only as eps -> 0: (eps/2)min = %.4f at eps = 0.3, %.6f at eps = 0.003"
   % (exact_min(0.3, 10) * 0.15, exact_min(0.003, 10) * 0.0015),
   exact_min(0.3, 10) * 0.15 > 1.02 and exact_min(0.003, 10) * 0.0015 < 1.00001)
ok("REF-P6-0's eps = 0.3 entry 6.75 is BELOW the exact minimum %.4f (float artifact, not quoted)"
   % exact_min(0.3, 10), exact_min(0.3, 10) > 6.75)
