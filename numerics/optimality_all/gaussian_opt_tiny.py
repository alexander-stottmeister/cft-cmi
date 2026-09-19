"""Optimum over gauge-invariant QUASI-FREE recovery channels on tiny chains, evaluated with the
EXACT -log F of the full 2^n-dimensional Gaussian density matrices (no second-order approximation).
Recovered symbol (rigor/optimality_second_order.tex, Lemma rec-symbol):
    Q_rec = [[Q_AA, Q_AB X^T],[X Q_BA, Z]],  feasible iff  X Q_BB X^T <= Z <= 1 - X (1-Q_BB) X^T.
Parametrisation: Z = X Q_BB X^T + W W^T (first constraint automatic), second by a barrier."""
import sys, numpy as np
from scipy.optimize import minimize
from scipy.linalg import sqrtm
import all_channels_sdp as S

def neglogF(rho, sig):
    s = sqrtm(rho); M = s @ sig @ s; M = (M + M.T) / 2
    w = np.linalg.eigvalsh(M); w = np.clip(w, 0, None)
    return -np.log(np.sqrt(w).sum())

def setup(LA, LB, LC):
    n = LA + LB + LC; Q = S.corr_sine(n); rho = S.gaussian_rho(Q)
    return n, Q, rho

def qrec(Q, X, Z, LA, LB):
    n = Q.shape[0]; QAA = Q[:LA, :LA]; QAB = Q[:LA, LA:LA + LB]
    top = np.hstack([QAA, QAB @ X.T]); bot = np.hstack([X @ QAB.T, Z])
    return np.vstack([top, bot])


def petz_XY(LA, LB, LC):
    """(X,Y) of the Gaussian Petz channel E(s)=rBC^{1/2}(rB^{-1/2} s rB^{-1/2} x 1_C) rBC^{1/2} from
    E^+(c_k^+ c_l) = sum_ab X_ka X_lb c_a^+ c_b + Y_kl 1  (exact for Gaussian channels)."""
    n = LA + LB + LC; rho = S.gaussian_rho(S.corr_sine(n)); dA, dB, dC = 2**LA, 2**LB, 2**LC
    rB = S.ptrace(rho, [dA, dB, dC], [1]); rBC = S.ptrace(rho, [dA, dB, dC], [1, 2])
    K = sqrtm(rBC).real @ np.kron(np.linalg.inv(sqrtm(rB)).real, np.eye(dC))
    cB = S.jw_ops(LB); cD = S.jw_ops(LB + LC); m = LB + LC
    basis = [cB[a].T @ cB[b] for a in range(LB) for b in range(LB)] + [np.eye(dB)]
    Bm = np.array([b.ravel() for b in basis]).T
    M = np.zeros((m, m, LB, LB)); Y = np.zeros((m, m)); res = 0.0
    for k in range(m):
        for l in range(m):
            O = cD[k].T @ cD[l]; Od = (K.T @ O @ K).reshape(dB, dC, dB, dC); Od = np.einsum('icjc->ij', Od)
            coef, r, *_ = np.linalg.lstsq(Bm, Od.ravel(), rcond=None)
            res = max(res, np.abs(Bm @ coef - Od.ravel()).max())
            M[k, l] = coef[:-1].reshape(LB, LB); Y[k, l] = coef[-1]
    # M[k,l,a,b] = X_ka X_lb ; recover X from the (k,a) x (l,b) rank-one matrix
    R = M.transpose(0, 2, 1, 3).reshape(m * LB, m * LB); w, V = np.linalg.eigh((R + R.T) / 2)
    X = (np.sqrt(w[-1]) * V[:, -1]).reshape(m, LB)
    print('petz_XY: fit residual', res, 'rank-one residual', np.abs(np.outer(X.ravel(), X.ravel()) - R).max(), flush=True)
    return X, Y

def run(LA, LB, LC, nstarts=6, seed=0):
    n, Q, rho = setup(LA, LB, LC); m = LB + LC; k = LB
    QBB = Q[LA:LA + LB, LA:LA + LB]; Rm = np.eye(k) - QBB
    def unpack(v):
        X = v[:m * k].reshape(m, k); W = v[m * k:].reshape(m, m); return X, W
    def obj(v):
        X, W = unpack(v); Z = X @ QBB @ X.T + W @ W.T
        slack = np.eye(m) - X @ Rm @ X.T - Z
        lam = np.linalg.eigvalsh((slack + slack.T) / 2).min()
        if lam < -1e-12: return 10.0 + 1e3 * lam**2
        Qr = qrec(Q, X, Z, LA, LB)
        w = np.linalg.eigvalsh(Qr)
        if w.min() < 1e-13 or w.max() > 1 - 1e-13: return 10.0
        return neglogF(rho, S.gaussian_rho(Qr))
    rng = np.random.default_rng(seed); best = (np.inf, None)
    # start at the Petz point: extract (X,Y) of the Gaussian Petz channel from its Heisenberg action on c_k^+ c_l
    Xp, Yp = petz_XY(LA, LB, LC); Zp = Xp @ QBB @ Xp.T + Yp
    wY, VY = np.linalg.eigh((Yp + Yp.T) / 2); Wp = VY @ np.diag(np.sqrt(np.clip(wY, 0, None)))
    print('Petz point: minY', wY.min(), 'min slack', np.linalg.eigvalsh(np.eye(m) - Xp @ Rm @ Xp.T - Zp).min(), flush=True)
    starts = [np.concatenate([Xp.ravel(), Wp.ravel()])]
    print('objective at Petz point', obj(starts[0]), flush=True)
    for _ in range(nstarts - 1):
        starts.append(starts[0] + 0.02 * rng.standard_normal(starts[0].size))
    for v0 in starts:
        r = minimize(obj, v0, method='Nelder-Mead', options=dict(maxiter=40000, maxfev=40000, xatol=1e-10, fatol=1e-14))
        r = minimize(obj, r.x, method='BFGS', options=dict(gtol=1e-11, maxiter=5000))
        if r.fun < best[0]: best = (r.fun, r.x)
    return best[0], obj(starts[0])

if __name__ == '__main__':
    LA, LB, LC = map(int, sys.argv[1:4])
    petz, z = S.petz_value(LA, LB, LC)
    g, prod = run(LA, LB, LC)
    print(f"({LA},{LB},{LC}) z={z:.4f}  Petz={petz:.8e}  Gaussian-opt={g:.8e}  (product start {prod:.4e})  gauss/Petz={g/petz:.5f}")
