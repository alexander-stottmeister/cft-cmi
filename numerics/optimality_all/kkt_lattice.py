"""S11(a): lattice KKT / strong-duality check for the quasi-free second-order programme
   min_{(X,Z) in F} g_w(Q - Qrec(X,Z))     on the (4,8,2) hopping chain (S8).

Conventions (opt_gaussian.py). Q_ij = sin(pi(i-j)/2)/(pi(i-j)); A=[0,LA), B=[LA,LA+LB),
C=[LA+LB,n), D=BC, m=dim h_D.  X: h_B -> h_D, Z=Z^* on h_D,
  F = { X Q_BB X^* <= Z <= 1 - X(1-Q_BB)X^* },  Qrec=[[Q_AA,Q_AB X^*],[X Q_BA,Z]].
  g_w(delta) = 1/4 sum_ik w_ik |delta~_ik|^2,  delta~ = U^* delta U,  Q = U diag(q) U^*,
  w_ik^true = 1/(q_i(1-q_k)+q_k(1-q_i)),  w^cap = min(w^true, 1+cosh kappa_c)  (S8's cap).
Legendre pair of g_w:  V_w(t) := sum_ik |t~_ik|^2/(2 w_ik);  for w = w^true this is exactly
  V(t) = Tr(t Q t (1-Q)),  the variance of dGamma(t) in the vacuum (Thm 4.1 of
  optimality_all_channels.tex).  For the CAPPED weights V_w != Tr(tQt(1-Q)); both are printed.
  SLD of delta: t = 1/2 U (w o delta~) U^*.  Then Tr t delta = 2 g_w, V_w(t) = g_w/2, so
  (Tr t delta)^2/(8 V_w(t)) = g_w(delta), and for every t, Delta(t)^2/(8 V_w(t)) <= min_F g_w.
KKT/strong duality test: at t = t_opt = SLD of the optimal defect the LINEAR programme
  Delta(t) = inf_F Tr t (Q - Qrec)   must be attained at the optimum itself, i.e.
  Delta(t_opt) = Tr t_opt delta_opt = 2 g_w(delta_opt), whence Delta^2/(8V_w) = min_F g_w.
"""
import sys, os, numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'optimality'))
import opt_gaussian as OG

def weights(Q, kappa_c=None):
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1 - 1e-16)
    w = 1.0 / (q[:, None] * (1 - q)[None, :] + q[None, :] * (1 - q)[:, None])
    if kappa_c is not None: w = np.minimum(w, 1.0 + np.cosh(kappa_c))
    return U, q, w

def g_w(delta, U, w):
    dt = U.conj().T @ delta @ U; return 0.25 * np.sum(w * np.abs(dt) ** 2)

def sld(delta, U, w):
    dt = U.conj().T @ delta @ U; t = 0.5 * (U @ (w * dt) @ U.conj().T)
    return 0.5 * (t + t.conj().T)

def V_w(t, U, w):
    tt = U.conj().T @ t @ U; return float(np.sum(np.abs(tt) ** 2 / (2 * w)))

def V_true(t, Q):
    return float(np.trace(t @ Q @ t @ (np.eye(len(Q)) - Q)).real)

class Geom:
    def __init__(self, LA, LB, LC):
        self.LA, self.LB, self.LC = LA, LB, LC
        n = LA + LB + LC; self.n, self.m = n, LB + LC
        Q = OG.corr_sine(n); self.Q = Q
        self.QAA, self.QAB = Q[:LA, :LA], Q[:LA, LA:LA + LB]
        self.QBB = Q[LA:LA + LB, LA:LA + LB]
        self.sG = np.linalg.cholesky(self.QBB + 1e-15 * np.eye(LB))
        self.sGD = np.linalg.cholesky(np.eye(LB) - self.QBB + 1e-15 * np.eye(LB))
    def qrec(self, X, Z):
        n, LA = self.n, self.LA
        R = np.zeros((n, n), dtype=complex); R[:LA, :LA] = self.QAA
        M = self.QAB @ X.conj().T; R[:LA, LA:] = M; R[LA:, :LA] = M.conj().T; R[LA:, LA:] = Z
        return 0.5 * (R + R.conj().T)
    def vars(self):
        X = cp.Variable((self.m, self.LB), complex=True)
        Z = cp.Variable((self.m, self.m), hermitian=True)
        cons = [cp.bmat([[Z, X @ self.sG], [(X @ self.sG).H, np.eye(self.LB)]]) >> 0,
                cp.bmat([[np.eye(self.m) - Z, X @ self.sGD], [(X @ self.sGD).H, np.eye(self.LB)]]) >> 0]
        return X, Z, cons
    def Qrec_expr(self, X, Z):
        LA = self.LA; M = self.QAB @ X.H
        return cp.bmat([[cp.Constant(self.QAA + 0j), M], [M.H, Z]])

def primal(G, U, w, solver='CLARABEL'):
    X, Z, cons = G.vars(); dt = U.conj().T @ (G.Q - G.Qrec_expr(X, Z)) @ U
    obj = 0.25 * cp.sum(cp.multiply(w, cp.square(cp.abs(dt))))
    pr = cp.Problem(cp.Minimize(obj), cons)
    try:
        pr.solve(solver=solver)
        if X.value is None: raise RuntimeError
    except Exception:
        pr.solve(solver='SCS', eps_abs=1e-11, eps_rel=1e-11, max_iters=400000)
    return pr.value, X.value, Z.value, pr.status

def linear(G, t, solver='CLARABEL'):
    """Delta(t) = inf_F Tr t (Q - Qrec)."""
    X, Z, cons = G.vars()
    obj = cp.real(cp.trace(t @ (cp.Constant(G.Q + 0j) - G.Qrec_expr(X, Z))))
    pr = cp.Problem(cp.Minimize(obj), cons)
    try:
        pr.solve(solver=solver)
        if X.value is None: raise RuntimeError
    except Exception:
        pr.solve(solver='SCS', eps_abs=1e-11, eps_rel=1e-11, max_iters=400000)
    return pr.value, X.value, Z.value, pr.status

def main():
    LA, LB, LC = 4, 8, 2
    G = Geom(LA, LB, LC); z = LA * LC / (LB * (LA + LB + LC)); f2 = 1 / (12 * np.pi ** 2)
    qe = np.linalg.eigvalsh(G.Q); kmax = np.log((1 - qe[0]) / qe[0])
    d = np.load(os.path.join(HERE, '..', 'optimality', 'best_4_8_2.npz'))
    print(f"# (LA,LB,LC)=({LA},{LB},{LC})  n={G.n}  z={z:.8f}  2 f2 z^2 = {2*f2*z**2:.6e}")
    print(f"# eig(Q) in [{qe[0]:.3e},{1-qe[-1]:.3e}] from 1 -> kappa_max = {kmax:.4f}; "
          f"w_true_max = {1/(2*qe[0]*(1-qe[0])):.4e}")
    print(f"# stored best_4_8_2.npz: exact -logF(best)={float(d['Fo']):.6e}, Petz={float(d['Fp']):.6e}, cap={float(d['cap'])}")
    Xs, Zs = d['X'], d['Z']
    hdr = ("kappa_c", "min_F g_w (SDP)", "g_w at S8 (X,Z)", "Delta(t_opt)", "2 g_w", "gap rel",
           "Dual/g_w [V_w]", "Dual/g_w [V_true]", "|Qr_lin-Qr_pri|_F", "status")
    print("# " + " | ".join(hdr))
    rows = []
    for kc in [4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, None]:
        U, q, w = weights(G.Q, kc)
        val, X, Z, st = primal(G, U, w)
        delta = G.Q - G.qrec(X, Z); gv = g_w(delta, U, w)
        gS8 = g_w(G.Q - G.qrec(Xs, Zs), U, w)
        t = sld(delta, U, w); Trtd = np.trace(t @ delta).real
        Vw, Vt = V_w(t, U, w), V_true(t, G.Q)
        Dl, Xl, Zl, stl = linear(G, t)
        dQ = np.linalg.norm(G.qrec(Xl, Zl) - G.qrec(X, Z))
        rows.append(dict(kc=(kmax if kc is None else kc), gmin=gv, gS8=gS8, Delta=Dl, twog=2 * gv,
                         gap=(2 * gv - Dl) / (2 * gv), rV=max(Dl, 0) ** 2 / (8 * Vw) / gv,
                         rT=max(Dl, 0) ** 2 / (8 * Vt) / gv, dQ=dQ, Vw=Vw, Vt=Vt, st=st + '/' + stl,
                         Trtd=Trtd, t1=np.abs(np.linalg.eigvalsh(t)).sum()))
        r = rows[-1]
        print(f"{r['kc']:7.3f} | {gv:.8e} | {gS8:.8e} | {Dl:.8e} | {2*gv:.8e} | {r['gap']:+.2e} | "
              f"{r['rV']:.8f} | {r['rT']:.8f} | {dQ:.2e} | {r['st']}", flush=True)
    np.savez(os.path.join(HERE, 'kkt_lattice_out.npz'), rows=np.array([[r[k] for k in
             ('kc','gmin','gS8','Delta','twog','gap','rV','rT','dQ','Vw','Vt','Trtd','t1')] for r in rows]),
             cols=np.array(['kc','gmin','gS8','Delta','twog','gap','rV','rT','dQ','Vw','Vt','Trtd','t1']))
    print("# columns: Dual = Delta(t_opt)^2/(8 V);  [V_w] uses the Legendre pair of the capped form,")
    print("#          [V_true] uses V(t)=Tr(tQt(1-Q)) (equal to V_w only for the uncapped weights).")

if __name__ == '__main__':
    main()
