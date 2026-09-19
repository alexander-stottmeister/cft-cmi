"""F2/T1e: lower bound on the tangent gain by restricting N1, Y1 to a k-dimensional
subspace of D, with the rotation G eliminated EXACTLY (CG) rather than carried as a variable.

For each basis direction eta_j of the noise space (N1,Y1 in the subspace) compute
eta_j^perp = eta_j + [G_j,Q] with G_j the g_Q-optimal rotation; then
   g_red(x) = x^T B x,  B_ij = (1/4) Re <eta_i^perp, W eta_j^perp>,
and the gain is  1/(4 q*),  q* = min{ x^T B x : l.x = -1, N1>=0, Y1>=0, N1-Y1>=0 }.
Any subspace gives a valid LOWER bound on the true gain (upper bound on kappa_full).
Usage:  f2_sub_gain.py L1,.. [cap] [k]
"""
import sys, time, numpy as np, cvxpy as cp
import f2_model as M
import f2_kkt_f1 as F1
from f2_tangent_gram import herm_basis, vec_h


def sub_gain(S, O, basis, tag='', solver='CLARABEL'):
    nD = S['nD']; k = basis.shape[1]; U, w = S['U'], S['w']
    W = lambda Y: U@(w*(U.conj().T@Y@U))@U.conj().T
    Bh = herm_basis(k); zero = np.zeros((nD, nD), complex)
    etas = []
    for b in Bh:
        etas.append(M.noise(S, basis@b@basis.conj().T, zero))
    for b in Bh:
        etas.append(M.noise(S, zero, basis@b@basis.conj().T))
    perp = []
    for e in etas:
        _, G = F1.gred(S, e)
        perp.append(e + M.rot(S, G))
    n = len(perp); B = np.zeros((n, n))
    We = [W(p) for p in perp]
    for i in range(n):
        for j in range(i, n):
            B[i, j] = B[j, i] = 0.25*float(np.real(np.vdot(perp[i], We[j])))
    # linear functional l (kkt normalisation: dg = Tr(N1 M_kkt) - Tr(Y1 tau_kkt))
    Mk, tk = 0.5*O['Ms'], 0.5*O['tau']
    lN = np.array([float(np.real(np.trace((basis@b@basis.conj().T)@Mk))) for b in Bh])
    lY = np.array([-float(np.real(np.trace((basis@b@basis.conj().T)@tk))) for b in Bh])
    ell = np.concatenate([lN, lY])
    Nr = cp.Variable((k, k), hermitian=True); Yr = cp.Variable((k, k), hermitian=True)
    x = cp.hstack([vec_h(Nr, k), vec_h(Yr, k)])
    s, V = np.linalg.eigh(B); s = np.maximum(s, 0.0); R = (V*np.sqrt(s)).T
    pr = cp.Problem(cp.Minimize(cp.sum_squares(R@x)),
                    [Nr >> 0, Yr >> 0, Nr-Yr >> 0, cp.sum(cp.multiply(ell, x)) == -1])
    try:
        pr.solve(solver=solver)
    except Exception as e:
        print(f"   sub[{tag}] k={k}: solver raised {type(e).__name__} ({solver}); retrying SCS", flush=True)
    if Nr.value is None or Yr.value is None:
        try:
            pr.solve(solver='SCS', eps=1e-10, max_iters=200000)
        except Exception as e:
            print(f"   sub[{tag}] k={k}: SCS also raised {type(e).__name__}", flush=True)
    if Nr.value is None or Yr.value is None:                 # no point returned: report, do not crash
        print(f"   sub[{tag}] k={k}: NO SOLUTION POINT  status={pr.status}  obj={pr.value}", flush=True)
        return 0.0, None, None
    # exact re-evaluation
    N1 = basis@Nr.value@basis.conj().T; Y1 = basis@Yr.value@basis.conj().T
    eta = M.noise(S, N1, Y1); gr, G = F1.gred(S, eta)
    lv = float(np.real(np.trace(N1@Mk))) - float(np.real(np.trace(Y1@tk)))
    gain = lv*lv/(4*gr)
    eN = np.linalg.eigvalsh(0.5*(N1+N1.conj().T)); eY = np.linalg.eigvalsh(0.5*(Y1+Y1.conj().T))
    eD = np.linalg.eigvalsh(0.5*((N1-Y1)+(N1-Y1).conj().T)); sc = max(np.linalg.norm(N1), 1e-300)
    feas = min(eN.min(), eY.min(), eD.min())/sc              # cone feasibility of the returned point
    print(f"   sub[{tag}] k={k}: cone feasibility min eig/||N1|| = {feas:+.2e} "
          f"(N1 {eN.min()/sc:+.1e}, Y1 {eY.min()/sc:+.1e}, N1-Y1 {eD.min()/sc:+.1e})", flush=True)
    print(f"   sub[{tag}] k={k}: q*={pr.value:.6e} [{pr.status}]  recomputed g_red={gr:.6e} l={lv:+.4e} "
          f"-> gain/g0 = {gain/O['g0']:.6e}  kappa <= {(1-O['theta']) - gain/O['g0']:.8f}", flush=True)
    return gain, N1, Y1


def run(L, cap=1e10, k=4, seed=0):
    t0 = time.time(); S = M.build(L=L, cap=cap); O = F1.objects(S); nD = S['nD']
    eM, VM = np.linalg.eigh(O['Ms']); eMt, VMt = np.linalg.eigh(O['Ms']-O['tau'])
    uQ, sQ, _ = np.linalg.svd(S['QDA'])
    rng = np.random.default_rng(seed)
    print(f"L={L} nD={nD} cap={cap:.0e}: theta={O['theta']:.6f} 1-theta={1-O['theta']:.6f} "
          f"g0={O['g0']:.6e} lam_min(M)={eM.min():+.3e} lam_min(M-tau)={eMt.min():+.3e}", flush=True)
    best = 0.0
    for tag, bas in (('eigM', VM[:, :k]), ('eigMtau', VMt[:, :k]),
                     ('svdQDA', uQ[:, :k]),
                     ('mix', np.linalg.qr(np.hstack([VM[:, :k], uQ[:, :k]]))[0]),
                     ('rand', np.linalg.qr(rng.normal(size=(nD, k))+1j*rng.normal(size=(nD, k)))[0])):
        try:
            g, _, _ = sub_gain(S, O, np.ascontiguousarray(bas), tag=tag)
            best = max(best, g)
        except Exception as e:
            print(f"   sub[{tag}]: FAILED {type(e).__name__}: {e}", flush=True)
    print(f"   BEST gain/g0 = {best/O['g0']:.6e}  =>  kappa_full <= {(1-O['theta'])-best/O['g0']:.8f} "
          f"(1-theta = {1-O['theta']:.8f})  [{time.time()-t0:.0f}s]", flush=True)
    return dict(L=L, cap=cap, theta=O['theta'], g0=O['g0'], gain=best)


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    cap = float(sys.argv[2]) if len(sys.argv) > 2 else 1e10
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    out = [run(L, cap=cap, k=k) for L in Ls]
    print("\n#    L     1-theta    max gain/g0    kappa_full <=")
    for r in out:
        print(f"{r['L']:6d} {1-r['theta']:.6f} {r['gain']/r['g0']:.4e} {1-r['theta']-r['gain']/r['g0']:.8f}",
              flush=True)
