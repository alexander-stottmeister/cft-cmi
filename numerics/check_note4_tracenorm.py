"""Independent numerical check of Note-4 Thm 6.3: ||R_s||_1 = (1/2) log(1 + a s/(a+L)).
R_s : L^2(0,L) -> L^2(0,a),  R_s(u,v) = s u v /[(u+v)(L(u+v)+s u v)].
Nystrom discretisation on a geometrically graded composite Gauss-Legendre mesh
(the kernel is continuous but non-smooth at the corner u=v=0)."""
import numpy as np

def graded_nodes(T, npanel=14, ng=20, sigma=0.25):
    """composite Gauss-Legendre nodes/weights on (0,T), panels graded towards 0."""
    xg, wg = np.polynomial.legendre.leggauss(ng)
    edges = [T*sigma**k for k in range(npanel)][::-1]
    edges = [0.0] + edges          # 0 < T*sigma^(n-1) < ... < T
    X, W = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m, h = 0.5*(lo+hi), 0.5*(hi-lo)
        X.append(m + h*xg); W.append(h*wg)
    return np.concatenate(X), np.concatenate(W)

def R_kernel(u, v, s, L):
    U, V = np.meshgrid(u, v, indexing='ij')
    return s*U*V/((U+V)*(L*(U+V)+s*U*V))

def H_kernel(x, y, alpha, beta):
    X, Y = np.meshgrid(x, y, indexing='ij')
    return 1.0/(X+Y+beta) - 1.0/(X+Y+beta+alpha)

def trace_norm_R(a, L, s, npanel=14, ng=20, sigma=0.25):
    u, wu = graded_nodes(a, npanel, ng, sigma)
    v, wv = graded_nodes(L, npanel, ng, sigma)
    M = np.sqrt(wu)[:, None]*R_kernel(u, v, s, L)*np.sqrt(wv)[None, :]
    sv = np.linalg.svd(M, compute_uv=False)
    return sv.sum(), np.sqrt((sv**2).sum()), sv

def eig_H(a, L, s, Tmax=None, npanel=22, ng=20, sigma=0.35):
    alpha, beta = s/L, 1.0/a + 1.0/L
    # H lives on (0,infty); map x = beta*t/(1-t) (t in (0,1)) -> exact for decaying kernels
    xg, wg = np.polynomial.legendre.leggauss(400)
    t = 0.5*(xg+1); wt = 0.5*wg
    x = beta*t/(1-t); jac = beta/(1-t)**2
    w = wt*jac
    M = np.sqrt(w)[:, None]*H_kernel(x, x, alpha, beta)*np.sqrt(w)[None, :]
    ev = np.linalg.eigvalsh(M)
    return ev, alpha, beta

print("="*72)
for (a, b, c) in [(1.0, 1.0, 1.0), (0.7, 2.3, 0.4), (5.0, 0.3, 11.0)]:
    L = b+c
    for s, tag in [(2*c/b, "s_P=2c/b"), (0.5, "s=0.5"), (7.0, "s=7")]:
        exact = 0.5*np.log1p(a*s/(a+L))
        n1, n2, sv = trace_norm_R(a, L, s)
        ev, al, be = eig_H(a, L, s)
        trH = ev[ev > 0].sum(); minev = ev.min()
        print(f"a={a} b={b} c={c} L={L} {tag}: s={s:.6f}")
        print(f"   exact  (1/2)log(1+as/(a+L)) = {exact:.12f}")
        print(f"   sum sing.val. of R_s (disc.) = {n1:.12f}   rel.err = {abs(n1-exact)/exact:.3e}")
        print(f"   Tr H_(alpha,beta)  (disc.)   = {trH:.12f}   rel.err = {abs(trH-exact)/exact:.3e}")
        print(f"   min eig H = {minev:.3e} (positivity),  ||R||_2 = {n2:.9f}, ||H||_2 = {np.sqrt((ev**2).sum()):.9f}")
    print("-"*72)
