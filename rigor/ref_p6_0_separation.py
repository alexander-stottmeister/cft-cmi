"""REF-P6-0: how sharp is W3 ("admissible protocols cannot place two WEAK corners CLOSE to each
other at distinct points ... zeta_k, zeta_{k+1} <= eps forces e^{Delta_k} >~ 1/eps")?

L->R ordinary-Petz chain, brief conventions:
  kappa_k = 2 l_{k+1}/(l_k(l_k+l_{k+1})),  zeta_k = kappa_k L_{k-1}(T-L_{k-1})/T,
  y_k = log(L_{k-1}/(T-L_{k-1})),  e^{Delta_k} = (1+u_k)(1+v_k).
We minimise e^{Delta_k} over chains of n intervals subject to
  (A)  zeta_k, zeta_{k+1} <= eps            (the literal hypothesis of W3), and
  (B)  zeta_j <= eps for EVERY corner j     (what the second-order law actually needs).
Random log-uniform search + coordinate descent on log lengths.
"""
import numpy as np
rng = np.random.default_rng(7)

def data(l):
    l = np.asarray(l, float)
    n = len(l); Ls = np.cumsum(l); T = Ls[-1]
    ks = np.arange(2, n)                       # corner indices k = 2..n-1
    lk = l[ks - 1]; lk1 = l[ks]
    Lkm1 = Ls[ks - 2]
    kap = 2 * lk1 / (lk * (lk + lk1))
    zeta = kap * Lkm1 * (T - Lkm1) / T
    Lk = Ls[ks - 1]
    eD = (Lk / Lkm1) * ((T - Lkm1) / (T - Lk))  # e^{Delta_k}, k=2..n-1 (last one meaningless)
    return zeta, eD

def objective(logl, k, eps, allweak):
    l = np.exp(logl)
    zeta, eD = data(l)
    i = k - 2
    pen = 0.0
    idx = range(len(zeta)) if allweak else (i, i + 1)
    for j in idx:
        if j < len(zeta) and zeta[j] > eps:
            pen += 1e3 * np.log(zeta[j] / eps)
    return np.log(eD[i]) + pen

def minimise(n, k, eps, allweak, tries=300, iters=4000):
    best = (1e99, None)
    for _ in range(tries):
        x = rng.uniform(-8, 8, n)
        f = objective(x, k, eps, allweak)
        step = 1.5
        for it in range(iters):
            j = rng.integers(n)
            d = step * rng.normal()
            y = x.copy(); y[j] += d
            g = objective(y, k, eps, allweak)
            if g < f: x, f = y, g
            if it % 500 == 499: step *= 0.6
        if f < best[0]: best = (f, x)
    l = np.exp(best[1]); zeta, eD = data(l)
    return np.exp(best[0]), l / l.min(), zeta, eD[k - 2]

print("n = 6 intervals, corner pair (k, k+1) = (2, 3)\n")
print("  (A) only zeta_2, zeta_3 <= eps")
for eps in (0.3, 0.1, 0.03, 0.01, 0.003):
    v, l, zeta, eD = minimise(6, 2, eps, allweak=False, tries=60, iters=3000)
    print("    eps=%-7g min e^{Delta_2} = %-9.4g  Delta=%.3f  1/eps=%-8g  zetas=%s"
          % (eps, eD, np.log(eD), 1 / eps, np.array2string(zeta, precision=4)))
print("\n  (B) ALL corners weak: zeta_j <= eps for j = 2..5")
for eps in (0.3, 0.1, 0.03, 0.01, 0.003):
    v, l, zeta, eD = minimise(6, 2, eps, allweak=True, tries=60, iters=3000)
    print("    eps=%-7g min e^{Delta_2} = %-9.4g  Delta=%.3f  1/eps=%-8g  zetas=%s"
          % (eps, eD, np.log(eD), 1 / eps, np.array2string(zeta, precision=4)))

print("\n  (B) with n = 8, pair (3,4), all corners weak")
for eps in (0.1, 0.03, 0.01):
    v, l, zeta, eD = minimise(8, 3, eps, allweak=True, tries=60, iters=3000)
    print("    eps=%-7g min e^{Delta_3} = %-9.4g  Delta=%.3f  1/eps=%-8g  zetas=%s"
          % (eps, eD, np.log(eD), 1 / eps, np.array2string(zeta, precision=4)))

# exhibit one explicit chain for (A)
print("\nexplicit chain for (A), eps = 0.01:")
v, l, zeta, eD = minimise(6, 2, 0.01, allweak=False, tries=120, iters=6000)
print("   lengths (normalised) =", np.array2string(l, precision=4))
print("   zeta_k =", np.array2string(zeta, precision=5), "  e^{Delta_2} =", round(eD, 4))
