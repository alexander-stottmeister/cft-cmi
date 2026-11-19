"""REF-RP-2: independent brute-force check of card quasi-free-fidelity-formula (finite-dimensional h).
Run: ${PYTHON:-python3} rigor/repair/ref_rp_2_qf_fidelity.py > rigor/repair/ref_rp_2_qf_fidelity.out
Jordan-Wigner Fock space of n modes, rho = exp(-a^* H a)/Z with <a_i^* a_j> = Q_{ji}, Q = (e^{H^T}+1)^{-1};
root fidelity F = Tr |sqrt(rho1) sqrt(rho2)| (singular values) vs the card's two forms. Tolerance fixed before
the run: |difference of -log F| <= 1e-10. Also: block-diagonal symbols factorise (R3 item 16)."""
import numpy as np
from scipy.linalg import expm, logm, svdvals, eigh
rng = np.random.default_rng(20261119)
def ops(n):
    I2, Z = np.eye(2), np.diag([1., -1.]); a = np.array([[0., 1.], [0., 0.]])
    out = []
    for k in range(n):
        m = np.array([[1.]])
        for j in range(n): m = np.kron(m, Z if j < k else (a if j == k else I2))
        out.append(m)
    return out
def state(Q, A):
    H = logm((np.eye(len(Q)) - Q) @ np.linalg.inv(Q))               # matrix log; Q = (e^{H}+1)^{-1} up to the convention fixed by the symbol check
    K = sum(H[i, j] * A[i].conj().T @ A[j] for i in range(len(A)) for j in range(len(A)))
    r = expm(-K); return r / np.trace(r)
def psd(M): w, V = eigh((M + M.conj().T) / 2); return V @ np.diag(np.sqrt(np.clip(w, 0, None))) @ V.conj().T
def randQ(n):
    X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); U = np.linalg.qr(X)[0]
    return U @ np.diag(rng.uniform(0.05, 0.95, n)) @ U.conj().T
def form1(Q1, Q2):
    G1 = Q1 @ np.linalg.inv(np.eye(len(Q1)) - Q1); G2 = Q2 @ np.linalg.inv(np.eye(len(Q2)) - Q2)
    t = np.linalg.eigvalsh(G1); s = np.linalg.eigvalsh(G2); g = psd(G1)
    tau = np.linalg.eigvalsh(g @ G2 @ g)
    return 0.5 * np.log1p(t).sum() + 0.5 * np.log1p(s).sum() - np.log1p(np.sqrt(np.clip(tau, 0, None))).sum()
def form2(Q1, Q2):
    I = np.eye(len(Q1)); C = np.linalg.inv(psd(I - Q1)) @ psd(Q1) @ psd(Q2) @ np.linalg.inv(psd(I - Q2))
    F = np.sqrt(np.linalg.det(I - Q1).real * np.linalg.det(I - Q2).real) * np.prod(1 + svdvals(C))
    return -np.log(F)
worst = 0
for n in (1, 2, 3, 4):
    A = ops(n)
    for trial in range(3):
        Q1, Q2 = randQ(n), randQ(n)
        r1, r2 = state(Q1, A), state(Q2, A)
        chk = max(abs(np.trace(r1 @ A[i].conj().T @ A[j]) - Q1[j, i]) for i in range(n) for j in range(n))
        bf = -np.log(svdvals(psd(r1) @ psd(r2)).sum())
        d1, d2 = abs(bf - form1(Q1, Q2)), abs(bf - form2(Q1, Q2)); worst = max(worst, d1, d2)
        print(f"n={n} trial={trial} symbol check {chk:.1e}  brute -logF={bf:.12f}  |f1-bf|={d1:.1e} |f2-bf|={d2:.1e}")
print(f"worst {worst:.1e} {'PASS' if worst <= 1e-10 else 'FAIL'} (tol 1e-10)")
A = ops(4); Qa, Qb, Qc, Qd = randQ(2), randQ(2), randQ(2), randQ(2)
blk = lambda X, Y: np.block([[X, np.zeros((2, 2))], [np.zeros((2, 2)), Y]])
full = form1(blk(Qa, Qb), blk(Qc, Qd)); prod = form1(Qa, Qc) + form1(Qb, Qd)
print(f"block-diagonal factorisation (item 16): -logF full {full:.12f} = sum of halves {prod:.12f}, diff {abs(full-prod):.1e}")
