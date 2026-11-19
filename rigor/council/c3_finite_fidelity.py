"""C3 council check of Note 5 thm:finite-fidelity (fidelity_recovered_quasifree.tex:225-243) and of the monotonicity
claim of thm:det-rep (l. 294-312) on nested compressions. Independent code: many-body density matrices built by
Jordan-Wigner from rho_Q = exp(-sum h_ij a_i^* a_j)/Z with h = log((1-Q)/Q) (no Fock functor used), root fidelity
Tr|sqrt(rho1) sqrt(rho2)| via eigendecompositions in mpmath (dps 40).
Tolerances fixed before the run: |F_formula - F_bruteforce| < 1e-25 (n = 3, 4 modes); along nested compressions
P_1 H < P_2 H < ... of a 5-mode pair, F_k must be nonincreasing up to 1e-25.
Run: ${PYTHON:-python3} rigor/council/c3_finite_fidelity.py > rigor/council/c3_finite_fidelity.out
"""
import mpmath as mp, random
mp.mp.dps = 40
random.seed(7)

def rand_symbol(n):
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            A[i, j] = mp.mpc(random.gauss(0, 1), random.gauss(0, 1))
    H = (A + A.H) / 2
    E, U = mp.eighe(H)
    return U * mp.diag([1 / (1 + mp.e ** (2 * e)) for e in E]) * U.H   # 0 < Q < 1

def mfun(X, f):
    E, U = mp.eighe((X + X.H) / 2)
    return U * mp.diag([f(e) for e in E]) * U.H

def formula(Q1, Q2):
    n = Q1.rows; I = mp.eye(n)
    G1 = Q1 * mp.inverse(I - Q1); G2 = Q2 * mp.inverse(I - Q2)
    G1h = mfun(G1, mp.sqrt)
    T = mfun(G1h * G2 * G1h, mp.sqrt)
    return mp.re(mp.sqrt(mp.det(I - Q1) * mp.det(I - Q2)) * mp.det(I + T))

def annihilators(n):
    dim = 2 ** n; ops = []
    for k in range(n):
        a = mp.zeros(dim, dim)
        for st in range(dim):
            if st >> k & 1:
                sign = (-1) ** bin(st & ((1 << k) - 1)).count('1')
                a[st ^ (1 << k), st] = sign
        ops.append(a)
    return ops

def rho(Q, ops):
    n = Q.rows; h = mfun(Q, lambda q: mp.log((1 - q) / q))
    Hm = mp.zeros(2 ** n, 2 ** n)
    for i in range(n):
        for j in range(n):
            Hm += h[i, j] * ops[i].H * ops[j]
    r = mfun(Hm, lambda e: mp.e ** (-e)); return r / sum(r[i, i] for i in range(r.rows))

def brute(Q1, Q2):
    ops = annihilators(Q1.rows)
    # convention check: omega_Q(a^*(f) a(g)) = <g, Q f>  <=>  Tr rho a_i^* a_j = Q_ji
    r1, r2 = rho(Q1, ops), rho(Q2, ops)
    s1 = mfun(r1, lambda e: mp.sqrt(max(e, 0)))
    X = s1 * r2 * s1
    return sum(mp.sqrt(max(e, 0)) for e in mp.eighe((X + X.H) / 2)[0]), r1, ops

for n in (3, 4):
    Q1, Q2 = rand_symbol(n), rand_symbol(n)
    fb, r1, ops = brute(Q1, Q2); ff = formula(Q1, Q2)
    corr = max(abs(mp.fsum(r1[k, l] * (ops[i].H * ops[j])[l, k] for k in range(2**n) for l in range(2**n)) - Q1[j, i])
               for i in range(n) for j in range(n))
    print(f"n={n}: F_formula={mp.nstr(ff, 30)} F_brute={mp.nstr(fb, 30)} |diff|={mp.nstr(abs(ff-fb), 3)} "
          f"symbol-convention residual={mp.nstr(corr, 3)}", "PASS" if abs(ff - fb) < 1e-25 else "FAIL")

n = 5; Q1, Q2 = rand_symbol(n), rand_symbol(n)
prev, ok = mp.mpf(2), True
for k in range(1, n + 1):
    Fk = formula(Q1[:k, :k], Q2[:k, :k]); ok &= Fk <= prev + mp.mpf('1e-25'); prev = Fk
    print(f"nested compression k={k}: F_k={mp.nstr(Fk, 25)}  -logF_k={mp.nstr(-mp.log(Fk), 20)}")
print("monotone nonincreasing:", "PASS" if ok else "FAIL")
