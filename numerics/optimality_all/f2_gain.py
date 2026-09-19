"""F2/T1b: the exact gain of the noise directions over the isometric orbit.

At the orbit optimum delta_* the objective splits EXACTLY (stationarity in G kills the
cross term with the rotations):
   g_Q(delta_* + [G,Q] + noise(v)) = g_* + l(v) + g_Q([G,Q] + noise(v)),  v = (N1,Y1),
   l(v) = Tr(N1 M_*) - Tr(Y1 t_DD)      (= the KKT linear functional).
Hence   min over the cone  =  g_* - max_{v in cone, l(v)<0} l(v)^2 / (4 g_red(v)),
   g_red(v) = min_G g_Q([G,Q] + noise(v)),
and the maximal gain equals  g_* cos^2( delta_*, achievable noise direction ) -- a theta-like
quantity, NOT the smallest eigenvalue of M_*.

Dropping the cone gives the unconstrained upper bound  gain_unc = (1/4) l^T Ghat^+ l,
computed by CG on Ghat x = l in the orthonormal coordinates of (H, N1, Y1).  Ghat is the
Gram of the map x -> Delta(x) = [iH,Q] + noise(N1,Y1) in the g_Q metric.
Usage:  f2_gain.py L1,L2,... [cap]
"""
import sys, time, numpy as np
import f2_model as M
import f2_kkt_check as KC


def coords(Z):
    n = Z.shape[0]; d = np.arange(n); iu = np.triu_indices(n, 1)
    return np.concatenate([Z[d, d].real, np.sqrt(2)*Z[iu].real, np.sqrt(2)*Z[iu].imag])


def uncoords(x, n):
    d = np.arange(n); iu = np.triu_indices(n, 1); k = n*(n-1)//2
    Z = np.zeros((n, n), complex); Z[d, d] = x[:n]
    Z[iu] = (x[n:n+k] + 1j*x[n+k:n+2*k])/np.sqrt(2)
    return Z + Z.conj().T - np.diag(np.diag(Z).real)


def ops(S):
    nD, nI, Q, U, w = S['nD'], S['nI'], S['Q'], S['U'], S['w']
    QDD, QDA = S['QDD'], S['QDA']
    Wop = lambda Y: U@(w*(U.conj().T@Y@U))@U.conj().T

    def delta(x):
        H = uncoords(x[:nD*nD], nD); N1 = uncoords(x[nD*nD:2*nD*nD], nD)
        Y1 = uncoords(x[2*nD*nD:], nD)
        return M.rot(S, 1j*H) + M.noise(S, N1, Y1)

    def adj(Y):
        Yd = Y[:nD, :nD]; Yda = Y[:nD, nD:]
        ar = 1j*(Q@Y - Y@Q)[:nD, :nD]; ar = 0.5*(ar + ar.conj().T)
        an = 0.5*(QDD@Yd + Yd@QDD) + Yda@QDA.conj().T; an = 0.5*(an + an.conj().T)
        return np.concatenate([coords(ar), coords(an), coords(-Yd)])

    Gop = lambda x: 0.25*adj(Wop(delta(x)))
    return delta, adj, Wop, Gop


def run(L, cap=1e10, iters=400, seed=0):
    t0 = time.time(); S = M.build(L=L, cap=cap); K = KC.kkt(S); nD = S['nD']
    delta, adj, Wop, Gop = ops(S)
    g0, gs, th = K['g0'], K['gstar'], K['theta']
    ell = adj(K['t'])                                   # (0, M_*, -t_DD) in coordinates
    print(f"L={L} nD={nD} cap={cap:.0e}: g0={g0:.6e} theta={th:.6f} g_*=(1-th)g0={gs:.6e}  "
          f"|l_H|={np.linalg.norm(ell[:nD*nD]):.2e} (0 by stationarity) "
          f"|l_N|={np.linalg.norm(ell[nD*nD:2*nD*nD]):.3e} |l_Y|={np.linalg.norm(ell[2*nD*nD:]):.3e}", flush=True)
    # consistency: Ghat and l reproduce g_Q exactly on a random direction
    rng = np.random.default_rng(seed); xr = rng.normal(size=3*nD*nD)
    q1 = float(xr@Gop(xr)); q2 = M.gQ(S, delta(xr))
    lin = float(ell@xr); lin2 = (M.gQ(S, K['dstar']+1e-6*delta(xr))-M.gQ(S, K['dstar']-1e-6*delta(xr)))/2e-6
    print(f"    check: x.Gx/g_Q = {q1/q2:.10f}   l.x/(d g_Q) = {lin/lin2:.10f}", flush=True)
    # CG on Ghat x = l  (min-norm solution; gain = (1/4) l.x)
    x = np.zeros_like(ell); r = ell.copy(); p = r.copy(); rs = r@r; nb = np.sqrt(rs); lad = []
    for k in range(iters):
        Ap = Gop(p); pAp = float(p@Ap)
        if pAp <= 0: break
        al = rs/pAp; x = x + al*p; r = r - al*Ap; rs2 = float(r@r); p = r + (rs2/rs)*p; rs = rs2
        if (k+1) % 25 == 0 or k == iters-1:
            lad.append((k+1, 0.25*float(ell@x)/g0, np.sqrt(rs2)/nb))
    gain = 0.25*float(ell@x)
    print("    CG ladder (it, gain_unc/g0, |res|):  " +
          "  ".join(f"{a}:{b:.4e}/{c:.1e}" for a, b, c in lad[-6:]), flush=True)
    print(f"    gain_unc/g0 = {gain/g0:.6e}   (1-theta) = {1-th:.6f}  =>  kappa_lower = "
          f"{(gs-gain)/g0:.6f}   [{time.time()-t0:.0f}s]", flush=True)
    return dict(L=L, cap=cap, theta=th, g0=g0, gain=gain, lad=lad, S=S, K=K, ell=ell, x=x)


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    caps = [float(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '1e10').split(',')]
    it = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    for L in Ls:
        for cap in caps:
            run(L, cap=cap, iters=it)
            print('', flush=True)
