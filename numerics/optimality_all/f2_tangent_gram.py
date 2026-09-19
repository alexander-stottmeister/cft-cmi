"""F2/T1 (efficient form): the tangent SDP with the quadratic form precomputed in the
variable space, so the canonical problem has n = 3|D|^2 columns instead of |I|^2.

Same problem as f2_tangent_sdp.py:
  min  g_Q( delta_c + [G,Q] + noise(N1,Y1) )  over G = iH anti-Herm on D, N1 >= 0, 0 <= Y1 <= N1.
Orthonormal real coordinates of a Hermitian A:  (A_aa)_a, (sqrt2 Re A_ab)_{a<b}, (sqrt2 Im A_ab)_{a<b}.
Usage:  f2_tangent_gram.py L1,L2,... [cap] [solver]
"""
import sys, time, numpy as np, cvxpy as cp
import f2_model as M


def herm_basis(n):
    B = []
    for a in range(n):
        E = np.zeros((n, n), complex); E[a, a] = 1.0; B.append(E)
    for a in range(n):
        for b in range(a+1, n):
            E = np.zeros((n, n), complex); E[a, b] = E[b, a] = 1/np.sqrt(2); B.append(E)
    for a in range(n):
        for b in range(a+1, n):
            E = np.zeros((n, n), complex); E[a, b] = 1j/np.sqrt(2); E[b, a] = -1j/np.sqrt(2); B.append(E)
    return B


def vec_h(A, n):
    """cvxpy expression -> the same orthonormal real coordinates."""
    d = np.arange(n); iu = np.triu_indices(n, 1)
    return cp.hstack([cp.real(A)[d, d], np.sqrt(2)*cp.real(A)[iu], np.sqrt(2)*cp.imag(A)[iu]])


def quadform(S, dtype=complex):
    """columns of the residual map: r(x) = sqrt(w) o U^H Delta(x) U ; returns (Gram, c, g0)."""
    nD, nI, U, sw = S['nD'], S['nI'], S['U'], np.sqrt(S['w'])
    B = herm_basis(nD); zero = np.zeros((nD, nD), complex)
    cols = []
    for role in ('H', 'N', 'Y'):
        for b in B:
            if role == 'H':  Dl = M.rot(S, 1j*b)
            elif role == 'N': Dl = M.noise(S, b, zero)
            else:             Dl = M.noise(S, zero, b)
            cols.append((sw*(U.conj().T@Dl@U)).ravel())
    Sm = np.array(cols, dtype=dtype).T                      # nI^2 x n
    r0 = (sw*(U.conj().T@S['dc']@U)).ravel().astype(dtype)
    G = 0.25*np.real(Sm.conj().T@Sm); G = 0.5*(G+G.T)
    c = 0.5*np.real(Sm.conj().T@r0)
    return G, c, 0.25*float(np.real(np.vdot(r0, r0)))


def factor(G, c, g0, tol=1e-14):
    s, V = np.linalg.eigh(G); keep = s > tol*s.max()
    sv = np.sqrt(s[keep]); Vk = V[:, keep]
    R = (Vk*sv).T                                           # k x n,  R^T R = G
    e = (Vk.T@c)/(2*sv)
    leak = np.linalg.norm(V[:, ~keep].T@c) if (~keep).any() else 0.0
    return R, e, g0 - float(e@e), leak, int(keep.sum()), s


def solve(S, G, c, g0, orbit_only=False, solver='CLARABEL', scale=1.0, sub=None):
    """sub: (k x nD) matrix of orthonormal columns -> N1,Y1 restricted to that subspace."""
    nD = S['nD']; n3 = 3*nD*nD; nn = nD*nD
    Gs = G.copy(); cs = scale*c; g0s = scale*scale*g0
    R, e, const, leak, k, sp = factor(Gs, cs, g0s)
    H = cp.Variable((nD, nD), hermitian=True); cons = []
    xs = [vec_h(H, nD)]
    if orbit_only:
        xs += [np.zeros(nn), np.zeros(nn)]
    elif sub is None:
        N1 = cp.Variable((nD, nD), hermitian=True); Y1 = cp.Variable((nD, nD), hermitian=True)
        cons = [N1 >> 0, Y1 >> 0, N1-Y1 >> 0]
        xs += [vec_h(N1, nD), vec_h(Y1, nD)]
    else:
        kk = sub.shape[1]
        Nr = cp.Variable((kk, kk), hermitian=True); Yr = cp.Variable((kk, kk), hermitian=True)
        cons = [Nr >> 0, Yr >> 0, Nr-Yr >> 0]
        N1 = sub@Nr@sub.conj().T; Y1 = sub@Yr@sub.conj().T
        xs += [vec_h(N1, nD), vec_h(Y1, nD)]
    x = cp.hstack(xs)
    pr = cp.Problem(cp.Minimize(cp.sum_squares(R@x + e)), cons)
    kw = dict(eps=1e-12, max_iters=200000) if solver == 'SCS' else {}
    pr.solve(solver=solver, **kw)
    val = pr.value + const
    out = dict(val=val, status=pr.status, H=H.value, leak=leak, rank=k, const=const)
    if not orbit_only:
        out['N1'] = N1.value if sub is None else sub@Nr.value@sub.conj().T
        out['Y1'] = Y1.value if sub is None else sub@Yr.value@sub.conj().T
    return out


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    caps = [float(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '1e10').split(',')]
    solver = sys.argv[3] if len(sys.argv) > 3 else 'CLARABEL'
    for L in Ls:
        for cap in caps:
            t0 = time.time(); S = M.build(L=L, cap=cap)
            th, xg, ds, g0c, it = M.theta_cg(S)
            G, c, g0 = quadform(S)
            R, e, const, leak, k, sp = factor(G, c, g0)
            print(f"L={L} nD={S['nD']} nI={S['nI']} cap={cap:.0e}: g0={g0:.8e} (CG {g0c:.8e}) "
                  f"theta={th:.6f} 1-theta={1-th:.6f} | Gram rank {k}/{3*S['nD']**2} "
                  f"cond={sp.max()/max(sp[sp>0].min(),1e-300):.2e} leak={leak:.2e} [{time.time()-t0:.0f}s]", flush=True)
            for tag, kwargs in (('orbit', dict(orbit_only=True)), ('FULL ', {})):
                t1 = time.time()
                try:
                    r = solve(S, G, c, g0, solver=solver, **kwargs)
                    ex = ''
                    if tag == 'FULL ':
                        N1, Y1 = r['N1'], r['Y1']
                        ex = (f" |N1|_F={np.linalg.norm(N1):.3e} trN1={np.trace(N1).real:.3e} "
                              f"|Y1|_F={np.linalg.norm(Y1):.3e} |Y1-N1|_F={np.linalg.norm(Y1-N1):.3e} "
                              f"eigN1 in [{np.linalg.eigvalsh(N1).min():.2e},{np.linalg.eigvalsh(N1).max():.2e}]")
                    print(f"   {tag}: g/g0 = {r['val']/g0:.10f}   dev from 1-theta = "
                          f"{r['val']/g0-(1-th):+.3e}  [{r['status']}] {time.time()-t1:.0f}s{ex}", flush=True)
                except Exception as ex0:
                    print(f"   {tag}: FAILED {type(ex0).__name__}: {ex0} {time.time()-t1:.0f}s", flush=True)
