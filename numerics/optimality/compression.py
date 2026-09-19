"""The lattice image of the continuum zero-collar geometric compression.

Continuum (Note 4): gamma_s = Ad U(h_s) with h_s(x) = x/(1+s x/L) mapping
D = (0,L) onto (0, L/(1+s)); the admissible endpoint is s = lambda = c/b, i.e.
h maps D onto B.  One-particle map V: L^2(D) -> L^2(B),
(V f)(y) = sqrt(g'(y)) f(g(y)),  g = h^{-1}(y) = y/(1 - lambda y/L).
Discretised in the site (piecewise-constant) basis; X* := V, X := V*, Y := 0."""
import numpy as np
from scipy.integrate import quad
from opt_gaussian import corr_sine
from petz_ref import petz_symbol, neglogF
from run_opt import assemble, zval


def comp_matrix(LB, LC):
    L = LB + LC
    lam = LC / LB
    h = lambda x: x / (1 + lam * x / L)
    gp = lambda y: 1.0 / (1 - lam * y / L) ** 2          # g'(y)
    V = np.zeros((LB, L))
    for k in range(LB):
        for j in range(L):
            lo, hi = max(k, h(j)), min(k + 1, h(j + 1))
            if hi > lo:
                V[k, j] = quad(lambda y: np.sqrt(gp(y)), lo, hi, limit=200)[0]
    return V                                              # = X^*  (LB x L)


class _P:
    pass


def run(LA, LB, LC):
    n = LA + LB + LC
    Q = corr_sine(n)
    Vc = comp_matrix(LB, LC)
    sv = np.linalg.svd(Vc, compute_uv=False)
    X = (Vc / max(1.0, sv.max())).T                       # X: h_B -> h_D, ||X||<=1
    QBB = Q[LA:LA + LB, LA:LA + LB]
    Z = X @ QBB @ X.T                                     # Y = 0
    P = _P(); P.n, P.LA = n, LA
    P.QAA, P.QAB = Q[:LA, :LA], Q[:LA, LA:LA + LB]
    Qr = np.real(assemble(P, X + 0j, Z + 0j))
    Qp = petz_symbol(Q, LA, LB, LC, dps=90)
    z = zval(LA, LB, LC)
    Fc, Fp = float(neglogF(Q, Qr, dps=90)), float(neglogF(Q, Qp, dps=90))
    f2 = 1.0 / (12 * np.pi ** 2)
    print('(%d,%d,%d) z=%.5f | sv(V) in [%.4f,%.4f] | compression=%.6e  Petz=%.6e'
          '  ratio=%.4f | comp/(2f2 z^2)=%.4f  Petz/(8f2 z^2)=%.4f'
          % (LA, LB, LC, z, sv.min(), sv.max(), Fc, Fp, Fc / Fp,
             Fc / (2 * f2 * z ** 2), Fp / (8 * f2 * z ** 2)), flush=True)
    return Fc, Fp


if __name__ == '__main__':
    for g in [(4, 8, 2), (4, 12, 2), (6, 12, 3), (4, 16, 2), (8, 16, 4), (12, 24, 6)]:
        run(*g)
