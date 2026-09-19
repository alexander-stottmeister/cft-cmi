"""F2/T1: the fixed-geometry TANGENT problem in the S10 spectral circle model.

  min over  G = iH anti-Hermitian on D,  N1 >= 0 on D,  0 <= Y1 <= N1   of
  g_Q( delta_c + [G,Q] + noise(N1,Y1) ),
  noise_DD = (1/2){N1,Q_DD} - Y1,  noise_DA = (1/2) N1 Q_DA,  noise_AA = 0.

Orbit-only (N1 = Y1 = 0) must reproduce S10's (1 - theta) g_Q(delta_c).
Usage:  f2_tangent_sdp.py [L1,L2,...] [cap] [solver]
"""
import sys, time, numpy as np, cvxpy as cp
import f2_model as M


def solve(S, orbit_only=False, solver='CLARABEL', scale=1.0, rank1=None, eps=0.0):
    nD, nI = S['nD'], S['nI']
    QDD, QDA, U, sw = S['QDD'], S['QDA'], S['U'], np.sqrt(S['w'])
    dc = scale*S['dc']
    dDD, dDA, dAA = dc[:nD, :nD], dc[:nD, nD:], dc[nD:, nD:]
    H = cp.Variable((nD, nD), hermitian=True); G = 1j*H
    DDD = dDD + (G@QDD - QDD@G); DDA = dDA + G@QDA; cons = []
    if not orbit_only:
        if rank1 is None:
            N1 = cp.Variable((nD, nD), hermitian=True); Y1 = cp.Variable((nD, nD), hermitian=True)
            cons = [N1 >> 0, Y1 >> 0, N1 - Y1 >> 0]
        else:                                   # N1 = n pp*, Y1 = y pp*  (0 <= y <= n)
            p = rank1.reshape(-1, 1); pp = p@p.conj().T
            nv = cp.Variable(nonneg=True); yv = cp.Variable(nonneg=True)
            N1 = nv*pp; Y1 = yv*pp; cons = [nv - yv >= 0]
        DDD = DDD + 0.5*(N1@QDD + QDD@N1) - Y1
        DDA = DDA + 0.5*N1@QDA
    Delta = cp.bmat([[DDD, DDA], [DDA.H, cp.Constant(dAA)]])
    dt = cp.multiply(sw, U.conj().T@Delta@U)
    obj = 0.25*(cp.sum_squares(cp.real(dt)) + cp.sum_squares(cp.imag(dt)))
    pr = cp.Problem(cp.Minimize(obj), cons)
    kw = dict(verbose=False)
    if solver == 'SCS':
        kw.update(eps=1e-9, max_iters=100000)
    pr.solve(solver=solver, **kw)
    out = dict(val=pr.value, status=pr.status, H=H.value)
    if not orbit_only:
        out['N1'] = N1.value if rank1 is None else nv.value*(rank1.reshape(-1, 1)@rank1.reshape(1, -1).conj())
        out['Y1'] = Y1.value if rank1 is None else yv.value*(rank1.reshape(-1, 1)@rank1.reshape(1, -1).conj())
        if rank1 is not None:
            out['n'] = nv.value; out['y'] = yv.value
    return out


def report(S, L, solver='CLARABEL'):
    th, x, dstar, g0, it = M.theta_cg(S)
    print(f"L={L}  nI={S['nI']} nD={S['nD']} nA={S['nA']}  cap={S['cap']:.0e}  "
          f"g_Q(dc)={g0:.8e}  theta_CG={th:.6f}  1-theta={1-th:.6f}  (CG {it} its)", flush=True)
    t0 = time.time(); ro = solve(S, orbit_only=True, solver=solver)
    print(f"  orbit-only SDP : g/g0 = {ro['val']/g0:.6f}   [1-theta = {1-th:.6f}, "
          f"rel.dev = {(ro['val']/g0-(1-th))/(1-th):+.2e}]  {ro['status']}  {time.time()-t0:.1f}s", flush=True)
    t0 = time.time(); rf = solve(S, orbit_only=False, solver=solver)
    kap = rf['val']/g0
    N1, Y1 = rf['N1'], rf['Y1']
    eN = np.linalg.eigvalsh(0.5*(N1+N1.conj().T)); eY = np.linalg.eigvalsh(0.5*(Y1+Y1.conj().T))
    print(f"  FULL SDP       : kappa_full = {kap:.6f}   gap (1-theta)-kappa_full = "
          f"{(1-th)-kap:+.3e}  {rf['status']}  {time.time()-t0:.1f}s", flush=True)
    print(f"    ||N1||_F={np.linalg.norm(N1):.3e} tr N1={np.trace(N1).real:.3e} "
          f"eig(N1) in [{eN.min():.2e},{eN.max():.2e}] | ||Y1||_F={np.linalg.norm(Y1):.3e} "
          f"tr Y1={np.trace(Y1).real:.3e} eig(Y1) in [{eY.min():.2e},{eY.max():.2e}] | "
          f"||Y1-N1||_F={np.linalg.norm(Y1-N1):.3e}", flush=True)
    # homogeneity: dc -> 2 dc must scale the optimum by 4
    r2 = solve(S, orbit_only=False, solver=solver, scale=2.0)
    print(f"    homogeneity: g(2 dc)/g(dc) = {r2['val']/rf['val']:.6f}  (exact 4)", flush=True)
    return dict(L=L, theta=th, g0=g0, orbit=ro['val'], full=rf['val'], kappa=kap,
                N1=N1, Y1=Y1, H=rf['H'])


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    cap = float(sys.argv[2]) if len(sys.argv) > 2 else 1e10
    solver = sys.argv[3] if len(sys.argv) > 3 else 'CLARABEL'
    out = {}
    for L in Ls:
        t0 = time.time(); S = M.build(L=L, cap=cap)
        r = report(S, L, solver=solver)
        out[L] = r
        print(f"  [total {time.time()-t0:.1f}s]\n", flush=True)
    np.savez('f2_tangent_%s_%.0e.npz' % ('_'.join(map(str, Ls)), cap),
             **{f'{k}_{L}': v for L, r in out.items() for k, v in r.items() if k != 'L'})
