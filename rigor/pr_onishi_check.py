#!/usr/bin/env python3
"""
pr_onishi_check.py -- numerical verification of the fermionic vacuum-overlap
("Onishi"/Pfaffian-type) formula

        |<Omega, Gamma(U) Omega>| = det(1 - V^* V)^{1/2},   V = P_- U P_+,

in an explicit finite-dimensional (2^n) fermionic Fock space with Jordan-Wigner
matrices.  Conventions are those of the document under review:

        omega( a^*(f) a(g) ) = <g, P_+ f>        (so P_+ modes are OCCUPIED)

Tests performed
  T0  CAR algebra / Jordan-Wigner sanity
  T1  Omega has the prescribed two-point function <Om, c_i^* c_j Om> = (P_+)_{ji}
  T2  Gamma(U) built two independent ways (exp dGamma(log U)  vs  minors/Lambda^k U)
  T3  main identity, >=200 Haar unitaries, several (n,p); also |det(P_+ U P_+)|
  T4  phase question: is the modulus essential?
  T5  one-mode-pair rotation table (n=2, p=1)
  T6  in which sense is Gamma(U) number-non-conserving?  (bare N vs Omega-relative N)
  T7  genuine pairing (number-non-conserving w.r.t. the BARE vacuum) Bogoliubov
      transformations: does the naive formula survive?  what is the fix?
  T8  the inequality  -(1/2) log det(1-V^*V) <= (1/2) ||V||_2^2 / (1 - ||V||^2)
"""

import numpy as np
import scipy.linalg as sla
from itertools import combinations

rng = np.random.default_rng(20260908)
np.set_printoptions(precision=12, suppress=False, linewidth=140)

# ----------------------------------------------------------------- Jordan-Wigner
def jw(n):
    """Return list of annihilation operators c_1..c_n as 2^n x 2^n complex matrices.
    Mode 1 = most significant tensor factor.  |0> basis = (1,0), |1> = (0,1)."""
    I2 = np.eye(2, dtype=complex)
    Z = np.diag([1.0, -1.0]).astype(complex)
    a = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)   # a|1> = |0>
    cs = []
    for j in range(n):
        ops = [Z] * j + [a] + [I2] * (n - j - 1)
        M = ops[0]
        for O in ops[1:]:
            M = np.kron(M, O)
        cs.append(M)
    return cs

def anticomm(X, Y):
    return X @ Y + Y @ X

def check_car(n):
    cs = jw(n)
    d = 2 ** n
    err = 0.0
    for i in range(n):
        for j in range(n):
            err = max(err, np.abs(anticomm(cs[i], cs[j])).max())
            err = max(err, np.abs(anticomm(cs[i], cs[j].conj().T)
                                  - (1.0 if i == j else 0.0) * np.eye(d)).max())
    return err

# ------------------------------------------------------- Fock basis / states
def basis_index(occ, n):
    """computational-basis index of the occupation set `occ` (mode 1 = MSB)."""
    idx = 0
    for j in range(n):
        if j in occ:
            idx |= 1 << (n - 1 - j)
    return idx

def filled_sea(n, p):
    """Omega = c_1^* ... c_p^* |bare vac>, built by applying the JW operators."""
    cs = jw(n)
    v = np.zeros(2 ** n, dtype=complex)
    v[0] = 1.0                                   # bare vacuum = |00...0>
    for j in range(p - 1, -1, -1):               # c_1^* (c_2^* ( ... ))
        v = cs[j].conj().T @ v
    return v

def dGamma(A, cs):
    """dGamma(A) = sum_{ij} A_ij c_i^* c_j."""
    n = len(cs)
    d = cs[0].shape[0]
    out = np.zeros((d, d), dtype=complex)
    for i in range(n):
        for j in range(n):
            if A[i, j] != 0:
                out += A[i, j] * (cs[i].conj().T @ cs[j])
    return out

def Gamma_exp(U, cs):
    """Gamma(U) = exp(dGamma(log U));  Gamma(U) c^*(f) Gamma(U)^* = c^*(Uf)."""
    L = sla.logm(U)
    return sla.expm(dGamma(L, cs))

def Gamma_minors(U):
    """Gamma(U) = direct sum of Lambda^k U, in the JW computational basis.
    <S|Gamma(U)|T> = det(U[S,T]) for ordered subsets S,T of equal size."""
    n = U.shape[0]
    d = 2 ** n
    G = np.zeros((d, d), dtype=complex)
    subsets = {}
    for k in range(n + 1):
        subsets[k] = list(combinations(range(n), k))
    for k in range(n + 1):
        for S in subsets[k]:
            iS = basis_index(S, n)
            for T in subsets[k]:
                iT = basis_index(T, n)
                if k == 0:
                    G[iS, iT] = 1.0
                else:
                    G[iS, iT] = np.linalg.det(U[np.ix_(list(S), list(T))])
    return G

def haar(n):
    X = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    Q, R = np.linalg.qr(X)
    return Q * (np.diag(R) / np.abs(np.diag(R)))

def anti_herm(n):
    X = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    return X - X.conj().T

banner = lambda s: print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

# ================================================================= T0
banner("T0  CAR / Jordan-Wigner sanity")
for n in (2, 3, 4, 5):
    print(f"  n={n}:  max |CAR violation| = {check_car(n):.3e}")

# ================================================================= T1
banner("T1  Omega two-point function:  <Om, c_i^* c_j Om> =? (P_+)_{ji}")
for (n, p) in [(3, 1), (3, 2), (4, 2), (4, 1), (4, 3), (5, 2), (5, 3)]:
    cs = jw(n)
    Om = filled_sea(n, p)
    Pp = np.diag([1.0] * p + [0.0] * (n - p)).astype(complex)
    G2 = np.array([[Om.conj() @ (cs[i].conj().T @ cs[j]) @ Om for j in range(n)]
                   for i in range(n)])
    print(f"  n={n} p={p}:  ||<c_i^* c_j> - (P_+)^T||_max = "
          f"{np.abs(G2 - Pp.T).max():.3e}   (norm |Om| = {np.linalg.norm(Om):.12f})")
print("  => Omega is the FILLED SEA of the first p modes, as required by")
print("     omega(a^*(f)a(g)) = <g,P_+ f>.")

# ================================================================= T2
banner("T2  Gamma(U): exp(dGamma(log U))  vs  direct sum of Lambda^k U")
for n in (2, 3, 4):
    cs = jw(n)
    e = 0.0
    for _ in range(8):
        U = haar(n)
        G1, G2 = Gamma_exp(U, cs), Gamma_minors(U)
        e = max(e, np.abs(G1 - G2).max())
        # covariance property Gamma c^*(f) Gamma^* = c^*(Uf) for f = e_j
        for j in range(n):
            lhs = G2 @ cs[j].conj().T @ G2.conj().T
            rhs = sum(U[k, j] * cs[k].conj().T for k in range(n))
            e = max(e, np.abs(lhs - rhs).max())
        e = max(e, abs(G2[0, 0] - 1.0))          # Gamma|bare vac> = |bare vac>
    print(f"  n={n}:  max |Gamma_exp - Gamma_minors| and covariance error = {e:.3e}")

# ================================================================= T3 / T4
banner("T3/T4  main identity over Haar-random U  (N = 300 each)")
print(f"{'n':>2} {'p':>2} {'N':>4} | {'max| |ovl| - det(1-V*V)^1/2 |':>30}"
      f" | {'max| |ovl| - |det P+UP+| |':>27} | {'max| ovl - det P+UP+ |':>23}")
cases = [(3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 2), (5, 3), (5, 4)]
phase_spread = []
for (n, p) in cases:
    cs = jw(n)
    Om = filled_sea(n, p)
    e1 = e2 = e3 = 0.0
    for _ in range(300):
        U = haar(n)
        G = Gamma_minors(U)
        ovl = Om.conj() @ (G @ Om)
        A = U[:p, :p]                      # P_+ U P_+ on P_+H
        V = U[p:, :p]                      # P_- U P_+ : P_+H -> P_-H
        rhs = np.sqrt(max(np.real(np.linalg.det(np.eye(p) - V.conj().T @ V)), 0.0))
        e1 = max(e1, abs(abs(ovl) - rhs))
        e2 = max(e2, abs(abs(ovl) - abs(np.linalg.det(A))))
        e3 = max(e3, abs(ovl - np.linalg.det(A)))
        if abs(ovl) > 1e-8:
            phase_spread.append(np.angle(ovl))
    print(f"{n:>2} {p:>2} {300:>4} | {e1:>30.3e} | {e2:>27.3e} | {e3:>23.3e}")
ph = np.array(phase_spread)
print(f"\n  phases arg<Om,Gamma(U)Om> over all samples: min={ph.min():+.4f}, "
      f"max={ph.max():+.4f}, |mean e^{{i arg}}|={abs(np.exp(1j*ph).mean()):.4f}")
print("  => <Om,Gamma(U)Om> = det(P_+ U P_+) EXACTLY (phase included);")
print("     the modulus is essential only in the comparison with")
print("     det(1-V^*V)^{1/2}, which is >= 0 by construction.")

# ================================================================= T5
banner("T5  one-mode-pair check: n=2, p=1, U = [[cos t, -sin t],[sin t, cos t]]")
n, p = 2, 1
cs = jw(n); Om = filled_sea(n, p)
print(f"{'t':>6} {'<Om,Gam Om>':>22} {'cos t':>14} {'V=P-UP+':>12} {'sin t':>12}"
      f" {'det(1-V*V)^1/2':>16}")
for t in np.arange(0.0, 1.5001, 0.1):
    U = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]], dtype=complex)
    G = Gamma_minors(U)
    ovl = Om.conj() @ (G @ Om)
    V = U[p:, :p]
    rhs = np.sqrt(np.real(np.linalg.det(np.eye(p) - V.conj().T @ V)))
    print(f"{t:6.1f} {ovl.real:+.12f} {np.cos(t):14.9f} {V[0,0].real:12.9f}"
          f" {np.sin(t):12.9f} {rhs:16.12f}")

# ================================================================= T6
banner("T6  WHICH Bogoliubov class is this?  bare-N vs Omega-relative-N")
n, p = 4, 2
cs = jw(n); Om = filled_sea(n, p)
Pp = np.diag([1.0]*p + [0.0]*(n-p)).astype(complex); Pm = np.eye(n) - Pp
N   = dGamma(np.eye(n, dtype=complex), cs)                       # bare number
Nt  = dGamma(Pm, cs) + (p*np.eye(2**n) - dGamma(Pp, cs))         # part-hole number
print(f"  Nt Omega = 0 ?  ||Nt Om|| = {np.linalg.norm(Nt @ Om):.3e}")
for _ in range(3):
    U = haar(n); G = Gamma_minors(U)
    w = G @ Om
    ev, P_ev = np.linalg.eigh(Nt)
    occ = {}
    for k in range(2**n):
        key = int(round(ev[k]))
        occ[key] = occ.get(key, 0.0) + abs(P_ev[:, k].conj() @ w) ** 2
    print(f"   ||[Gamma,N]||   = {np.abs(G@N - N@G).max():.3e}   "
          f"||[Gamma,Nt]|| = {np.abs(G@Nt - Nt@G).max():.3e}   "
          f"Gamma(U)Om spread over Nt-sectors: "
          + ", ".join(f"{k}:{v:.3f}" for k, v in sorted(occ.items()) if v > 1e-10))
print("  => Gamma(U) is gauge-invariant (commutes with bare N) but is a GENUINE")
print("     particle-number-NON-conserving Bogoliubov transformation relative to")
print("     Omega: it does not commute with the particle-hole number Nt and maps")
print("     Omega into a superposition of several particle-hole sectors.")

# ================================================================= T7
banner("T7  genuine PAIRING Bogoliubov transformations (bare-N violating)")

def nambu_of(G, cs):
    """Extract 2n x 2n Nambu matrix Ucal from Gamma B(F) Gamma^* = B(Ucal F),
    B(u,v) = sum u_j c_j^* + sum v_j c_j.  Uses tr(c_k X)/2^{n-1} = coeff of c_k^*."""
    n = len(cs); d = 2 ** n
    Ucal = np.zeros((2 * n, 2 * n), dtype=complex)
    ops = [c.conj().T for c in cs] + list(cs)          # B(e_j) for j=1..2n
    for j, Bj in enumerate(ops):
        X = G @ Bj @ G.conj().T
        for k in range(n):
            Ucal[k, j]     = np.trace(cs[k] @ X) / (d // 2)          # coeff of c_k^*
            Ucal[n + k, j] = np.trace(cs[k].conj().T @ X) / (d // 2)  # coeff of c_k
    return Ucal

def selfdual_P(Pp):
    n = Pp.shape[0]
    Pm = np.eye(n) - Pp
    return sla.block_diag(Pm, Pp.conj())

def sd_overlap_pred(Ucal, P):
    Q = np.eye(P.shape[0]) - P
    V = Q @ Ucal @ P
    val = np.real(np.linalg.det(np.eye(P.shape[0]) - V.conj().T @ V))
    return max(val, 0.0) ** 0.25, V

# 7a: validate the self-dual (1/4-power) formula on the gauge-invariant case
n, p = 4, 2
cs = jw(n); Om = filled_sea(n, p)
Pp = np.diag([1.0]*p + [0.0]*(n-p)).astype(complex)
Psd = selfdual_P(Pp)
e = 0.0
for _ in range(60):
    U = haar(n); G = Gamma_minors(U)
    ovl = abs(Om.conj() @ (G @ Om))
    Uc = nambu_of(G, cs)
    e = max(e, abs(ovl - sd_overlap_pred(Uc, Psd)[0]))
print(f"  7a gauge-invariant case, self-dual det(1-V^*V)^(1/4):  max err = {e:.3e}")

# 7b: honest pairing generator  K = sum A c^*c + 1/2 sum (B c^*c^* - h.c.)
def pairing_gamma(n, cs, scale=1.0):
    A = anti_herm(n) * scale
    Braw = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    B = (Braw - Braw.T) * scale
    d = 2 ** n
    K = dGamma(A, cs)
    Xp = np.zeros((d, d), dtype=complex)
    for i in range(n):
        for j in range(n):
            Xp += B[i, j] * (cs[i].conj().T @ cs[j].conj().T)
    K = K + 0.5 * (Xp - Xp.conj().T)
    return sla.expm(K), A, B

for (n, p) in [(4, 2), (4, 1), (5, 2), (3, 1)]:
    cs = jw(n); Om = filled_sea(n, p)
    Pp = np.diag([1.0]*p + [0.0]*(n-p)).astype(complex)
    Psd = selfdual_P(Pp)
    e_sd = e_cov = 0.0; naive_err = []; ovls = []
    for _ in range(60):
        G, A, B = pairing_gamma(n, cs, scale=0.55)
        e_cov = max(e_cov, np.abs(G @ G.conj().T - np.eye(2**n)).max())
        ovl = abs(Om.conj() @ (G @ Om)); ovls.append(ovl)
        Uc = nambu_of(G, cs)
        # validate the extracted Nambu matrix
        e_cov = max(e_cov, np.abs(Uc @ Uc.conj().T - np.eye(2*n)).max())
        pred, _ = sd_overlap_pred(Uc, Psd)
        e_sd = max(e_sd, abs(ovl - pred))
        # NAIVE formula: pretend the c^*c^* block is absent, use the uu-block
        Unaive = Uc[:n, :n]
        Vn = Unaive[p:, :p]
        pr = np.real(np.linalg.det(np.eye(p) - Vn.conj().T @ Vn))
        naive_err.append(abs(ovl - (max(pr, 0.0) ** 0.5)))
    print(f"  7b n={n} p={p}: unitarity err {e_cov:.2e} | self-dual (1/4) max err"
          f" {e_sd:.3e} | NAIVE det(1-V*V)^(1/2) err: median "
          f"{np.median(naive_err):.3e} max {np.max(naive_err):.3e} "
          f"(|ovl| range {min(ovls):.3f}-{max(ovls):.3f})")
print("  => with genuine pairing the naive P_-UP_+ formula FAILS by O(1);")
print("     the correct statement is the self-dual/Nambu one, det(1-V^*V)^{1/4}")
print("     with V = (1-P)Ucal P on K = H (+) Hbar, which reduces to the")
print("     stated formula in the gauge-invariant case.")

# ================================================================= T8
banner("T8  inequality  -(1/2) log det(1-V^*V) <= (1/2)||V||_2^2/(1-||V||^2)")
print(f"{'n':>2} {'p':>2} {'eps':>7} {'max ||V||':>10} {'min slack (RHS-LHS)':>22}"
      f" {'max LHS':>12} {'holds':>7}")
for (n, p) in [(4, 2), (5, 2), (3, 1)]:
    cs = jw(n); Om = filled_sea(n, p)
    for eps in (1.0, 0.5, 0.2, 0.05, 0.01):
        slack = []; nv = []; lhs_all = []; ok = True
        for _ in range(200):
            U = sla.expm(eps * anti_herm(n))
            G = Gamma_minors(U)
            ovl = abs(Om.conj() @ (G @ Om))
            V = U[p:, :p]
            if ovl < 1e-14:
                continue
            lhs = -np.log(ovl)
            s = np.linalg.svd(V, compute_uv=False)
            op = s.max() if s.size else 0.0
            if op >= 1 - 1e-12:
                continue
            rhs = 0.5 * (np.sum(s ** 2)) / (1 - op ** 2)
            # cross-check: -log|ovl| == -(1/2) log det(1-V^*V)
            chk = -0.5 * np.log(max(np.real(np.linalg.det(
                np.eye(p) - V.conj().T @ V)), 1e-300))
            assert abs(lhs - chk) < 1e-9, (lhs, chk)
            slack.append(rhs - lhs); nv.append(op); lhs_all.append(lhs)
            ok = ok and (rhs - lhs > -1e-12)
        print(f"{n:>2} {p:>2} {eps:>7.3g} {max(nv):>10.4f} {min(slack):>22.3e}"
              f" {max(lhs_all):>12.3e} {str(ok):>7}")
print("  (LHS == -(1/2)log det(1-V^*V) asserted to 1e-9 at every sample.)")
print("\nDONE.")
