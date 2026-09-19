"""F2/T1d: scale-free cone problem with the residual map precomputed EXACTLY
(no Gram squaring, no rank cutoff):  columns of  x -> sqrt(w) o U^H Delta(x) U.

  q* = min { g_Q([G,Q] + noise(N1,Y1)) : Tr(N1 M_*) - Tr(Y1 t_DD) = -1, N1,Y1 >= 0, N1-Y1 >= 0 }
  gain = 1/(4 q*),   kappa_full = (1-theta) - gain/g0.
Usage:  f2_cone_fast.py L1,.. [cap1,..] [solver] [sub_k]
sub_k > 0 restricts N1,Y1 to the span of the sub_k lowest eigenvectors of M_* joined with
the sub_k leading left singular vectors of Q_DA (a lower bound on the gain, cheap at large L).
"""
import sys, time, numpy as np, cvxpy as cp
import f2_model as M
import f2_kkt_check as KC
from f2_tangent_gram import herm_basis, vec_h


def resid_cols(S, basis=None):
    """exact residual columns for the coordinates (H, N1, Y1); basis = subspace (nD x k)."""
    nD, U, sw = S['nD'], S['U'], np.sqrt(S['w'])
    Bh = herm_basis(nD); Bn = Bh if basis is None else [basis@b@basis.conj().T for b in herm_basis(basis.shape[1])]
    zero = np.zeros((nD, nD), complex); cols = []
    for b in Bh:
        cols.append((sw*(U.conj().T@M.rot(S, 1j*b)@U)).ravel())
    for b in Bn:
        cols.append((sw*(U.conj().T@M.noise(S, b, zero)@U)).ravel())
    for b in Bn:
        cols.append((sw*(U.conj().T@M.noise(S, zero, b)@U)).ravel())
    Sm = np.array(cols).T
    return np.vstack([Sm.real, Sm.imag])


def run(L, cap=1e10, solver='CLARABEL', sub_k=0, verbose=False):
    t0 = time.time(); S = M.build(L=L, cap=cap); K = KC.kkt(S); nD = S['nD']
    g0, gs, th = K['g0'], K['gstar'], K['theta']
    basis = None
    if sub_k:
        eM, VM = np.linalg.eigh(K['Ms']); uQ, sQ, _ = np.linalg.svd(S['QDA'])
        basis = np.linalg.qr(np.hstack([VM[:, :sub_k], uQ[:, :sub_k]]))[0]
    A = resid_cols(S, basis); kk = nD if basis is None else basis.shape[1]
    H = cp.Variable((nD, nD), hermitian=True)
    Nr = cp.Variable((kk, kk), hermitian=True); Yr = cp.Variable((kk, kk), hermitian=True)
    x = cp.hstack([vec_h(H, nD), vec_h(Nr, kk), vec_h(Yr, kk)])
    N1 = Nr if basis is None else basis@Nr@basis.conj().T
    Y1 = Yr if basis is None else basis@Yr@basis.conj().T
    lin = cp.real(cp.trace(N1@K['Ms'])) - cp.real(cp.trace(Y1@K['tDD']))
    cons = [Nr >> 0, Yr >> 0, Nr-Yr >> 0, lin == -1]
    pr = cp.Problem(cp.Minimize(0.25*cp.sum_squares(A@x)), cons)
    kw = dict(eps=1e-12, max_iters=500000) if solver == 'SCS' else {}
    pr.solve(solver=solver, verbose=verbose, **kw)
    N1v = Nr.value if basis is None else basis@Nr.value@basis.conj().T
    Y1v = Yr.value if basis is None else basis@Yr.value@basis.conj().T
    # exact re-evaluation from the returned matrices
    v = M.noise(S, N1v, Y1v) + M.rot(S, 1j*H.value)
    lv = np.real(np.trace(N1v@K['Ms'])) - np.real(np.trace(Y1v@K['tDD']))
    qq = M.gQ(S, v); gain = lv*lv/(4*qq); tstar = -lv/(2*qq)
    gnew = M.gQ(S, K['dstar'] + tstar*v)
    print(f"L={L} nD={nD} k={kk} cap={cap:.0e}: theta={th:.6f} 1-theta={1-th:.6f} | q*={pr.value:.6e} "
          f"[{pr.status}] recomputed q={qq:.6e}", flush=True)
    print(f"   gain/g0 = {gain/g0:.6e}   kappa_full = {(gs-gain)/g0:.8f}   "
          f"direct g_Q(d_*+t v)/g0 = {gnew/g0:.8f}  t*={tstar:.3e}", flush=True)
    print(f"   |N1|_F={np.linalg.norm(N1v):.3e} trN1={np.trace(N1v).real:.3e} |Y1|_F={np.linalg.norm(Y1v):.3e} "
          f"|N1-Y1|_F={np.linalg.norm(N1v-Y1v):.3e} rank(N1)~{int((np.linalg.eigvalsh(N1v) > 1e-8*max(np.linalg.norm(N1v),1e-300)).sum())} "
          f"rank(Y1)~{int((np.linalg.eigvalsh(Y1v) > 1e-8*max(np.linalg.norm(Y1v),1e-300)).sum())} "
          f"[{time.time()-t0:.0f}s]", flush=True)
    return dict(L=L, cap=cap, theta=th, g0=g0, gain=gain, kappa=(gs-gain)/g0, q=pr.value,
                N1=N1v, Y1=Y1v, H=H.value, status=pr.status, gnew=gnew/g0)


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    caps = [float(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '1e10').split(',')]
    solver = sys.argv[3] if len(sys.argv) > 3 else 'CLARABEL'
    sub_k = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    out = []
    for L in Ls:
        for cap in caps:
            try:
                out.append(run(L, cap=cap, solver=solver, sub_k=sub_k))
            except Exception as e:
                print(f"L={L} cap={cap:.0e}: FAILED {type(e).__name__}: {e}", flush=True)
            print('', flush=True)
    print("#   L    cap      1-theta     kappa_full      gap/g0")
    for r in out:
        print(f"{r['L']:5d} {r['cap']:.0e} {1-r['theta']:.6f} {r['kappa']:.6f} {r['gain']/r['g0']:.4e}", flush=True)
