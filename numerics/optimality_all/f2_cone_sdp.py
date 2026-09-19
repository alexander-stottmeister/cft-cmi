"""F2/T1c: the tangent problem in its scale-free form.

  gain = max_{v in cone, l(v)<0} l(v)^2/(4 g_red(v)) = 1/(4 q*),
  q* = min { g_Q([G,Q] + noise(N1,Y1)) : l(N1,Y1) = -1, N1 >= 0, Y1 >= 0, N1-Y1 >= 0 },
  l(N1,Y1) = Tr(N1 M_*) - Tr(Y1 t_DD),
  kappa_full = (1 - theta) - gain/g0.
This form has no large constant to cancel and the cone makes it well posed (the
unconstrained relaxation is not: see f2_gain.py).
Usage:  f2_cone_sdp.py L1,.. [cap1,..] [solver]
"""
import sys, time, numpy as np, cvxpy as cp
import f2_model as M
import f2_kkt_check as KC


def cone_sdp(S, K, solver='CLARABEL', gram=None, verbose=False):
    nD, nI, U, sw = S['nD'], S['nI'], S['U'], np.sqrt(S['w'])
    QDD, QDA = S['QDD'], S['QDA']
    H = cp.Variable((nD, nD), hermitian=True)
    N1 = cp.Variable((nD, nD), hermitian=True); Y1 = cp.Variable((nD, nD), hermitian=True)
    G = 1j*H
    DDD = (G@QDD - QDD@G) + 0.5*(N1@QDD + QDD@N1) - Y1
    DDA = G@QDA + 0.5*N1@QDA
    Delta = cp.bmat([[DDD, DDA], [DDA.H, np.zeros((nI-nD, nI-nD))]])
    dt = cp.multiply(sw, U.conj().T@Delta@U)
    obj = 0.25*(cp.sum_squares(cp.real(dt)) + cp.sum_squares(cp.imag(dt)))
    lin = cp.real(cp.trace(N1@K['Ms'])) - cp.real(cp.trace(Y1@K['tDD']))
    cons = [N1 >> 0, Y1 >> 0, N1-Y1 >> 0, lin == -1]
    pr = cp.Problem(cp.Minimize(obj), cons)
    kw = dict(eps=1e-11, max_iters=500000) if solver == 'SCS' else {}
    pr.solve(solver=solver, verbose=verbose, **kw)
    return pr.value, N1.value, Y1.value, H.value, pr.status


def run(L, cap=1e10, solver='CLARABEL'):
    t0 = time.time(); S = M.build(L=L, cap=cap); K = KC.kkt(S)
    g0, gs, th = K['g0'], K['gstar'], K['theta']
    eM = np.linalg.eigvalsh(K['Ms'])
    q, N1, Y1, H, st = cone_sdp(S, K, solver=solver)
    gain = 1.0/(4*q) if q > 0 else np.inf
    # exact re-evaluation of the achieved value from the returned matrices
    v = M.noise(S, N1, Y1) + M.rot(S, 1j*H)
    lv = np.real(np.trace(N1@K['Ms'])) - np.real(np.trace(Y1@K['tDD']))
    qq = M.gQ(S, v); tstar = -lv/(2*qq)              # optimal amplitude for this direction
    gain2 = lv*lv/(4*qq)
    dnew = K['dstar'] + tstar*v
    gnew = M.gQ(S, dnew)
    print(f"L={L} nD={nD_(S)} cap={cap:.0e}: theta={th:.6f} 1-theta={1-th:.6f} minEig(M)={eM.min():+.3e}", flush=True)
    print(f"   q*={q:.6e} [{st}]  gain/g0={gain/g0:.6e}  (recomputed {gain2/g0:.6e})  "
          f"kappa_full={(gs-gain2)/g0:.8f}  gap=(1-th)-kappa={gain2/g0:.3e}  [{time.time()-t0:.0f}s]", flush=True)
    print(f"   direct check: g_Q(delta_*+t v)/g0 = {gnew/g0:.8f}  t*={tstar:.3e}  "
          f"|N1|_F={np.linalg.norm(N1):.3e} trN1={np.trace(N1).real:.3e} |Y1|_F={np.linalg.norm(Y1):.3e} "
          f"|N1-Y1|_F={np.linalg.norm(N1-Y1):.3e} eigN1/|N1| in "
          f"[{np.linalg.eigvalsh(N1).min()/np.linalg.norm(N1):.2e},{np.linalg.eigvalsh(N1).max()/np.linalg.norm(N1):.2e}]",
          flush=True)
    return dict(L=L, cap=cap, theta=th, g0=g0, q=q, gain=gain2, kappa=(gs-gain2)/g0,
                N1=N1, Y1=Y1, H=H, status=st)


def nD_(S):
    return S['nD']


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    caps = [float(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '1e10').split(',')]
    solver = sys.argv[3] if len(sys.argv) > 3 else 'CLARABEL'
    out = []
    for L in Ls:
        for cap in caps:
            try:
                out.append(run(L, cap=cap, solver=solver))
            except Exception as e:
                print(f"L={L} cap={cap:.0e}: FAILED {type(e).__name__}: {e}", flush=True)
            print('', flush=True)
    print("#   L    cap     1-theta      kappa_full     gap")
    for r in out:
        print(f"{r['L']:5d} {r['cap']:.0e} {1-r['theta']:.6f} {r['kappa']:.6f} {r['gain']/r['g0']:.3e}", flush=True)
