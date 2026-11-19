"""C3 council check: independent Nystrom recomputation of Note 4 thm:trace-norm,
||R_s||_1 = (1/2) log(1+zeta), zeta = a s/(a+L), R_s(u,v) = s u v/((u+v)(L(u+v)+s u v)) on L^2(0,a) -> L^2(0,L)
(continuum_petz_free_fermion.tex eq:defect-recall / thm:trace-norm, scalar kernel without i/(2 pi)).
Method: log-graded Gauss-Legendre nodes, u = a e^{-x}, x in [0, X]; trace norm = sum of singular values of the
weighted matrix. Discretisation resolves the kernel for u, v >= a e^{-X}, L e^{-X}; the cut-off corner square has
Hilbert-Schmidt weight <= (s/L) * a e^{-X} * L e^{-X} / 4-type bound (kernel <= s/(4L)), printed below.
Tolerance fixed before the run: |sum sigma - (1/2)log(1+zeta)| / ((1/2)log(1+zeta)) < 1e-6 at the finest resolution,
and the two finest resolutions agree to 1e-7 relative.
Validation (exactly known case): rank-one kernel k(u,v) = e^{-u} e^{-v} on (0,a)x(0,L): ||k||_1 = ||e^{-u}||_2 ||e^{-v}||_2.
Run: ${PYTHON:-python3} rigor/council/c3_trace_norm.py > rigor/council/c3_trace_norm.out
"""
import numpy as np

def nodes(a, n, X):
    x, w = np.polynomial.legendre.leggauss(n)
    x = 0.5 * X * (x + 1.0); w = 0.5 * X * w
    u = a * np.exp(-x)               # du = u dx
    return u, w * u

def tracenorm(kernel, a, L, n, X):
    u, wu = nodes(a, n, X); v, wv = nodes(L, n, X)
    M = np.sqrt(wu)[:, None] * kernel(u[:, None], v[None, :]) * np.sqrt(wv)[None, :]
    return np.linalg.svd(M, compute_uv=False).sum()

# validation
a, L = 1.3, 0.7
exact = np.sqrt((1 - np.exp(-2 * a)) / 2) * np.sqrt((1 - np.exp(-2 * L)) / 2)
for n in (100, 200):
    t = tracenorm(lambda u, v: np.exp(-u) * np.exp(-v), a, L, n, 40.0)
    print(f"VALIDATION rank-one n={n}: nystrom={t:.15f} exact={exact:.15f} rel.dev={abs(t-exact)/exact:.2e}")

for (a, L, s) in [(1.0, 1.0, 1.0), (2.0, 0.7, 3.1), (0.3, 5.0, 0.5), (1.0, 3.0, 20.0)]:
    zeta = a * s / (a + L); target = 0.5 * np.log1p(zeta)
    R = lambda u, v: s * u * v / ((u + v) * (L * (u + v) + s * u * v))
    res = []
    for (n, X) in [(200, 40.0), (400, 50.0), (800, 60.0)]:
        res.append(tracenorm(R, a, L, n, X))
        print(f"a={a} L={L} s={s} zeta={zeta:.6f} n={n} X={X}: ||R||_1={res[-1]:.12f} target={target:.12f} "
              f"rel.dev={abs(res[-1]-target)/target:.2e} cutoff-HS<= {s/(4*L)*np.sqrt(a*L)*np.exp(-X):.1e}")
    ok = abs(res[-1] - target) / target < 1e-6 and abs(res[-1] - res[-2]) / target < 1e-7
    print("  PASS" if ok else "  FAIL", f"(finest two differ by {abs(res[-1]-res[-2])/target:.2e} rel.)")
