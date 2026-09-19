"""Exact optimum of -log F(omega, omega^beta) over ALL recovery channels beta: A(BC)->A(B)
(unital CP, optionally parity-covariant) on a tiny half-filled hopping chain, as ONE SDP:
  maximise  Re Tr X  s.t.  [[rho, X],[X^T, rho_rec(C)]] >= 0,  C >= 0 (Choi of E=beta_*),
            Tr_BC C = 1_B,  (parity covariance),  rho_rec = (id_A x E)(rho_AB).
Watrous' SDP for the root fidelity; the joint problem is convex because rho_rec is affine in C.
Fermions via Jordan-Wigner (A leftmost); even beta <-> parity-covariant qubit channel, and the
recovered fermionic state is then the recovered qubit state (see optimality_all_channels.tex)."""
import sys, numpy as np, cvxpy as cp
from scipy.linalg import expm, logm, sqrtm

def corr_sine(n):
    i = np.arange(n)[:, None]; j = np.arange(n)[None, :]; d = i - j
    with np.errstate(divide='ignore', invalid='ignore'):
        Q = np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * d))
    return Q

def jw_ops(n):
    I2 = np.eye(2); Z = np.diag([1., -1.]); sm = np.array([[0., 1.], [0., 0.]])  # sm = |0><1| annihilates
    cs = []
    for k in range(n):
        mats = [Z] * k + [sm] + [I2] * (n - k - 1)
        M = mats[0]
        for m in mats[1:]: M = np.kron(M, m)
        cs.append(M)
    return cs

def gaussian_rho(Q):
    n = Q.shape[0]; cs = jw_ops(n)
    w, V = np.linalg.eigh(Q); w = np.clip(w, 1e-14, 1 - 1e-14)
    h = V @ np.diag(np.log((1 - w) / w)) @ V.T
    H = sum(h[i, j] * cs[i].T @ cs[j] for i in range(n) for j in range(n))
    rho = expm(-H); return rho / np.trace(rho)

def ptrace(rho, dims, keep):
    n = len(dims); r = rho.reshape(dims + dims)
    idx = list(range(2 * n)); out = r
    for k in sorted([q for q in range(n) if q not in keep], reverse=True):
        out = np.trace(out, axis1=k, axis2=k + out.ndim // 2)
    d = int(np.prod([dims[q] for q in keep])); return out.reshape(d, d)

def parity(nq):
    P = np.array([1.]);  Z = np.diag([1., -1.])
    for _ in range(nq): P = np.kron(P, Z)
    return P

def solve(LA, LB, LC, parity_cov=True, solver='CLARABEL', verbose=False):
    n = LA + LB + LC; Q = corr_sine(n); rho = gaussian_rho(Q)
    dA, dB, dC = 2**LA, 2**LB, 2**LC; dBC = dB * dC
    rhoAB = ptrace(rho, [dA, dB, dC], [0, 1])
    # partial transpose on B of rho_AB
    rT = rhoAB.reshape(dA, dB, dA, dB).transpose(0, 3, 2, 1).reshape(dA * dB, dA * dB)
    C = cp.Variable((dB * dBC, dB * dBC), symmetric=True)           # Choi, order (B, BC)
    cons = [C >> 0]
    # Tr_BC C = 1_B
    cons.append(cp.partial_trace(C, [dB, dBC], axis=1) == np.eye(dB))
    if parity_cov:
        PP = np.kron(parity(LB), parity(LB + LC))
        cons.append(PP @ C @ PP == C)
    big = (np.kron(rT, np.eye(dBC))) @ cp.kron(np.eye(dA), C)     # (A,B,BC)
    rho_rec = cp.partial_trace(big, [dA, dB, dBC], axis=1)
    X = cp.Variable((dA * dBC, dA * dBC))
    M = cp.bmat([[rho, X], [X.T, rho_rec]])
    cons.append(M >> 0)
    prob = cp.Problem(cp.Maximize(cp.trace(X)), cons)
    prob.solve(solver=solver, verbose=verbose)
    F = prob.value
    return F, -np.log(F), rho, C.value, rho_rec.value

def petz_value(LA, LB, LC):
    n = LA + LB + LC; rho = gaussian_rho(corr_sine(n)); dA, dB, dC = 2**LA, 2**LB, 2**LC
    rAB = ptrace(rho, [dA, dB, dC], [0, 1]); rB = ptrace(rho, [dA, dB, dC], [1]); rBC = ptrace(rho, [dA, dB, dC], [1, 2])
    rBih = np.linalg.inv(sqrtm(rB)).real; rBCh = sqrtm(rBC).real
    K = rBCh @ np.kron(rBih, np.eye(dC)) 
    # Petz: E(sigma_B) = rBC^{1/2} (rB^{-1/2} sigma rB^{-1/2} x 1_C?) no: E(s)=rBC^{1/2}(rB^{-1/2} s rB^{-1/2} (x) 1_C) rBC^{1/2}
    rec = np.zeros((dA * dB * dC,) * 2)
    for i in range(dA):
        for j in range(dA):
            blk = rAB.reshape(dA, dB, dA, dB)[i, :, j, :]
            rec += np.kron(np.outer(np.eye(dA)[i], np.eye(dA)[j]), K @ np.kron(blk, np.eye(dC)) @ K.T)
    s1 = sqrtm(rho); F = np.trace(sqrtm(s1 @ rec @ s1)).real
    z = LA * LC / (LB * (LA + LB + LC))
    return -np.log(F), z

if __name__ == '__main__':
    LA, LB, LC = map(int, sys.argv[1:4]); pc = (sys.argv[4] != '0') if len(sys.argv) > 4 else True
    petz, z = petz_value(LA, LB, LC)
    F, nlF, rho, C, rr = solve(LA, LB, LC, parity_cov=pc)
    print(f"(LA,LB,LC)=({LA},{LB},{LC}) z={z:.5f} parity_cov={pc}  Petz -logF={petz:.6e}  OPT(all channels) -logF={nlF:.6e}  ratio opt/Petz={nlF/petz:.4f}  opt/z^2={nlF/z**2:.5f}  2f2={2/(12*np.pi**2):.5f} 8f2={8/(12*np.pi**2):.5f}")
