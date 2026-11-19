"""C4 check N1 (independent of numerics/kb-checks-2026-09-23/tcond_check.py): the A-C intertwining
conditions (Tcond) of rigor/optimality_second_order.tex prop:AC-zero on the half-filled infinite hopping
chain, Q_ij = sin(pi(i-j)/2)/(pi(i-j)), Q_ii = 1/2, for consecutive blocks A|B|C of sizes (LA,LB,LC).
T = pinv(Q_AB) Q_AC.  Conditions: Q_AB T = Q_AC; T*T <= 1; T* Q_BB T <= Q_CC <= 1 - T*(1-Q_BB)T.
Tolerance fixed before the run: residual <= 1e-10; a condition holds if its min eigenvalue margin >= -1e-12.
Run: ${PYTHON:-python3} rigor/council/c4_tcond.py > rigor/council/c4_tcond.out"""
import numpy as np
def Qchain(n):
    d = np.subtract.outer(np.arange(n), np.arange(n)).astype(float)
    with np.errstate(divide='ignore', invalid='ignore'):
        Q = np.sin(np.pi*d/2)/(np.pi*d)
    Q[d == 0] = 0.5
    return Q
print("validation: spectrum of Q on 40 sites lies in [0,1]:", end=" ")
ev = np.linalg.eigvalsh(Qchain(40)); print(f"min {ev.min():.3e} max {ev.max():.6f}")
for LA, LB, LC in [(4,8,2),(4,12,2),(4,16,2),(6,12,3),(8,16,4)]:
    n = LA+LB+LC; Q = Qchain(n)
    A = np.arange(LA); B = np.arange(LA, LA+LB); C = np.arange(LA+LB, n)
    QAB, QAC, QBB, QCC = Q[np.ix_(A,B)], Q[np.ix_(A,C)], Q[np.ix_(B,B)], Q[np.ix_(C,C)]
    T = np.linalg.pinv(QAB) @ QAC
    res = np.abs(QAB @ T - QAC).max()
    m1 = np.linalg.eigvalsh(np.eye(LC) - T.T @ T).min()
    m2 = np.linalg.eigvalsh(QCC - T.T @ QBB @ T).min()
    m3 = np.linalg.eigvalsh(np.eye(LC) - T.T @ (np.eye(LB)-QBB) @ T - QCC).min()
    ok = res <= 1e-10 and min(m1,m2,m3) >= -1e-12
    print(f"(LA,LB,LC)=({LA},{LB},{LC}) residual {res:.1e} ||T|| {np.linalg.norm(T,2):.4f} "
          f"margins 1-T*T {m1:.4f} Qcc-T*QbbT {m2:.4f} 1-T*(1-Qbb)T-Qcc {m3:.4f} Tcond {'HOLDS' if ok else 'FAILS'}")
