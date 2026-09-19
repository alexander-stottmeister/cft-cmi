"""Unit tests: (1) quasi-free fidelity/relative-entropy formulas vs brute-force Fock space (n<=4 modes);
(2) mp pipeline vs numpy double precision on a small mode set."""
import numpy as np, itertools, scipy.linalg as sla
rng = np.random.default_rng(1)
def fock_ops(n):
    # Jordan-Wigner annihilation operators on 2^n dim
    I2 = np.eye(2); Z = np.diag([1.,-1.]); am = np.array([[0,1],[0,0]],dtype=complex)  # |0>=(1,0) empty, a|1>=|0>
    ops = []
    for j in range(n):
        mats = [Z]*j + [am] + [I2]*(n-j-1)
        M = mats[0]
        for m in mats[1:]: M = np.kron(M, m)
        ops.append(M)
    return ops
def rho_of_Q(Q, ops):
    n = len(ops); G = Q @ np.linalg.inv(np.eye(n)-Q); K = sla.logm(G)   # rho = det(1-Q) exp(a^* K a)
    H = sum(K[i,j]*ops[i].conj().T @ ops[j] for i in range(n) for j in range(n))
    rho = np.linalg.det(np.eye(n)-Q).real * sla.expm(H)
    return rho
def rand_Q(n):
    B = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n)); Hm = B + B.conj().T
    w, U = np.linalg.eigh(Hm); q = 1/(1+np.exp(rng.normal(size=n)*2))
    return U @ np.diag(q) @ U.conj().T
def F_formula(Q1, Q2):
    n = len(Q1); C1 = sla.sqrtm(np.eye(n)-Q1); C2 = sla.sqrtm(np.eye(n)-Q2)
    G1 = Q1 @ np.linalg.inv(np.eye(n)-Q1); G2 = Q2 @ np.linalg.inv(np.eye(n)-Q2)
    G1h = sla.sqrtm(G1); T = G1h @ G2 @ G1h
    return (np.linalg.det(C1)*np.linalg.det(C2)*np.linalg.det(np.eye(n)+sla.sqrtm(T))).real
def S_formula(Q1, Q2):
    n=len(Q1); I=np.eye(n)
    return np.trace(Q1@(sla.logm(Q1)-sla.logm(Q2)) + (I-Q1)@(sla.logm(I-Q1)-sla.logm(I-Q2))).real
for n in [1,2,3,4]:
    ops = fock_ops(n); Q1, Q2 = rand_Q(n), rand_Q(n)
    r1, r2 = rho_of_Q(Q1, ops), rho_of_Q(Q2, ops)
    # sanity: two-point function
    chk = max(abs(np.trace(r1 @ ops[i].conj().T @ ops[j]) - Q1[j,i]) for i in range(n) for j in range(n))  # <a_i^* a_j> = <e_j, Q e_i>
    s1 = sla.sqrtm(r1); M = s1 @ r2 @ s1; Fb = np.trace(sla.sqrtm(M)).real
    Sb = np.trace(r1 @ (sla.logm(r1) - sla.logm(r2))).real
    print(f"n={n}: Tr rho={np.trace(r1).real:.6f} 2pt-chk={chk:.1e} | F brute={Fb:.10f} formula={F_formula(Q1,Q2):.10f} | S brute={Sb:.10f} formula={S_formula(Q1,Q2):.10f}")
