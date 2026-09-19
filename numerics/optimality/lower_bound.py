"""Lower bound on E_opt from the restriction to A(A) v A(C).

Monotonicity of the root fidelity under the conditional expectation onto
A(A) v A(C) gives  -log F(omega, omega^beta) >= -log F(omega_AC, sigma) with
sigma = omega_AB o (id (x) beta|_{A(C)}), i.e. sigma is obtained from the vacuum
AB state by a channel B -> C.  For quasi-free beta the AC symbol is
    [[Q_AA, Q_AB T], [T* Q_BA, Zc]],   T*T <= 1,  T* Q_BB T <= Zc <= 1-T*(1-Q_BB)T,
a convex feasible set (Thm. 3.1 applied to the pair (T,Zc)).  We minimise the
exact -log F of the AC pair over it: a rigorous lower bound for E_opt over
quasi-free channels (and, after gauge twirling, a lower bound for the
gauge-covariant *quasi-free* class only -- see the note in the tex)."""
import sys
import numpy as np
from scipy.optimize import minimize
from opt_gaussian import corr_sine, neglogF_grad, qfi_form
from petz_ref import neglogF


class ACProblem:
    def __init__(self, LA, LB, LC):
        n = LA + LB + LC
        Q = corr_sine(n)
        self.LA, self.LB, self.LC, self.n, self.Q = LA, LB, LC, n, Q
        a, b, c = slice(0, LA), slice(LA, LA + LB), slice(LA + LB, n)
        self.QAA, self.QAB, self.QAC = Q[a, a], Q[a, b], Q[a, c]
        self.QBB, self.QCC = Q[b, b], Q[c, c]
        self.Qac = np.block([[self.QAA, self.QAC], [self.QAC.T, self.QCC]])
        self.q1, self.U1 = np.linalg.eigh(self.Qac)
        self.Rp, self.Rm = self.QBB, np.eye(LB) - self.QBB

    def sym(self, T, Zc):
        M = self.QAB @ T
        return np.block([[self.QAA + 0j, M], [M.conj().T, Zc]])

    def slacks(self, T, Zc):
        C0 = np.eye(self.LC) - T.conj().T @ T
        C1 = Zc - T.conj().T @ self.Rp @ T
        C2 = np.eye(self.LC) - T.conj().T @ self.Rm @ T - Zc
        return C0, 0.5 * (C1 + C1.conj().T), 0.5 * (C2 + C2.conj().T)

    def obj(self, v, mu):
        LB, LC = self.LB, self.LC
        nt = LB * LC
        T = v[:nt].reshape(LB, LC) + 1j * v[nt:2 * nt].reshape(LB, LC)
        Zr = v[2 * nt:2 * nt + LC * LC].reshape(LC, LC)
        Zi = v[2 * nt + LC * LC:].reshape(LC, LC)
        Zc = 0.5 * (Zr + Zr.T) + 0.5j * (Zi - Zi.T)
        Cs = self.slacks(T, Zc)
        pen = 0.0
        for C in Cs:
            e = np.linalg.eigvalsh(C)
            if e.min() <= 0:
                return 1e100
            pen += np.sum(np.log(e))
        val = neglogF_grad(self.Qac, self.sym(T, Zc), self.U1, self.q1)[0]
        return val - mu * pen

    def solve(self, mus=(1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8)):
        LB, LC = self.LB, self.LC
        v = np.zeros(2 * LB * LC + 2 * LC * LC)
        v[2 * LB * LC:2 * LB * LC + LC * LC] = self.QCC.ravel()
        for mu in mus:
            r = minimize(self.obj, v, args=(mu,), method='Nelder-Mead' if False else 'Powell',
                         options=dict(maxiter=100000, maxfev=200000, xtol=1e-12, ftol=1e-14))
            v = r.x
        nt = LB * LC
        T = v[:nt].reshape(LB, LC) + 1j * v[nt:2 * nt].reshape(LB, LC)
        Zr = v[2 * nt:2 * nt + LC * LC].reshape(LC, LC)
        Zi = v[2 * nt + LC * LC:].reshape(LC, LC)
        Zc = 0.5 * (Zr + Zr.T) + 0.5j * (Zi - Zi.T)
        return T, Zc, float(neglogF(self.Qac, np.real(self.sym(T, Zc)), dps=80))


if __name__ == '__main__':
    for g in [(4, 8, 2), (4, 12, 2), (6, 12, 3), (4, 16, 2)]:
        P = ACProblem(*g)
        T, Zc, val = P.solve()
        z = g[0] * g[2] / (g[1] * sum(g))
        prod = float(neglogF(P.Qac, np.real(np.block(
            [[P.QAA, 0 * P.QAC], [0 * P.QAC.T, P.QCC]])), dps=80))
        print('%s z=%.5f  E_AC(lower bnd)=%.4e  E_AC/z^2=%.5f  ||T||=%.4f | '
              '-logF(vac_AC || product)=%.4e' % (str(g), z, val, val / z**2,
                                                 np.linalg.norm(T, 2), prod), flush=True)
