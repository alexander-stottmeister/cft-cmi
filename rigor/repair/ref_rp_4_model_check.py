"""REF-RP-4: is index_zero_check.py (A) discriminating?  TOL = 1e-10 (fixed before the run).
(i) transposition: H_A real symmetric => U_s = expm(i s H) symmetric => B = P+UP- = (P-UP+)^T = C^T, so equal
    singular values follow for every s with no index argument.  Measure max|B - C^T|.
(ii) finite-window unitaries: a unitary window always has equal block singular values (finite dimension);
    demonstrate with the CIRCULAR shift on [-M, M) (a unitary window of the index -1 bilateral shift).
(iii) a model without (i): complex next-nearest-neighbour hopping i*t2 (flux, not gauge-removable), same cut
    structure as (A); compare sv(B), sv(C), and max|B - C^T|; Tr G^3 on the inner window.
"""
import numpy as np, sys, os
from scipy.linalg import expm, svdvals
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import index_zero_check as izc
TOL = 1e-10
N, M = izc.N, izc.M
HA = izc.hop_A()
for s in [3.0, 4.0]:
    U = expm(1j * s * HA); B, C = izc.blocks(U)
    print(f"(i) model A s={s}: max|U - U^T| = {np.max(abs(U - U.T)):.2e};  max|B - C^T| = {np.max(abs(B - C.T)):.2e}")
Mw = 50
Sc = np.roll(np.eye(2 * Mw), 1, axis=0)           # circular shift e_n -> e_{n+1}, unitary on the window
Bw = Sc[Mw:, :Mw]; Cw = Sc[:Mw, Mw:]
print("(ii) circular shift window: sv(B) top", np.sort(svdvals(Bw))[::-1][:2], " sv(C) top", np.sort(svdvals(Cw))[::-1][:2])
def hop_flux(t2=0.4):
    H = HA.astype(complex).copy()
    for n in range(-N, N - 2):
        a = 0.7 if n < -1 else 1.0
        H[izc.idx(n), izc.idx(n + 2)] = 1j * t2 * a
        H[izc.idx(n + 2), izc.idx(n)] = -1j * t2 * a
    return H
HF = hop_flux()
comm = np.zeros_like(HF); Pm = np.diag([1.0 if n < 0 else 0.0 for n in range(-N, N)])
comm = Pm @ HF - HF @ Pm
hs = np.linalg.norm(comm[np.ix_(range(N - 5, N + 5), range(N - 5, N + 5))])
print(f"(iii) flux model: ||[P-,K]||_2 = {hs:.6f}, old range |s| < {1 / hs:.4f}")
for s in [2.0, 4.0, -3.5]:
    U = expm(1j * s * HF); B, C = izc.blocks(U)
    sB = np.sort(svdvals(B))[::-1]; sC = np.sort(svdvals(C))[::-1]
    rows = [izc.idx(n) for n in range(-M, M)]; Uw = U[np.ix_(rows, rows)]
    P = np.diag([1.0 if n >= 0 else 0.0 for n in range(-M, M)])
    G = P - Uw.conj().T @ P @ Uw
    Gi = G[M - 60:M + 60, M - 60:M + 60]          # inner part, away from the read-out edge
    t3 = np.trace(Gi @ Gi @ Gi).real
    d = np.max(abs(sB - sC))
    print(f"(iii) s={s:5.2f} |s|*||[P-,K]||_2={abs(s)*hs:6.3f}  max|B - C^T| = {np.max(abs(B - C.T)):.3e} (not small: no transposition symmetry)"
          f"  max|sv(B)-sv(C)| = {d:.2e} {'PASS' if d < TOL else 'FAIL'}  top sv {np.round(sB[:3], 10)}  Tr G_inner^3 = {t3:+.2e}")
