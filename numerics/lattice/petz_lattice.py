"""O7(a): lattice test of the two-branch rotated-Petz law (agent PL).

Model: complex free-fermion hopping chain at half filling, infinite chain,
C_ij = <c_i^dag c_j> = sin(pi(i-j)/2)/(pi(i-j)) (exact).

Rotated Petz map, Vardhan-Wei-Zou arXiv:2307.14434 eq. (2.9) (Sec. 2.2,
"twirled Petz map"), reproduced in Note 5 (fidelity_recovered_quasifree.tex,
eq. after Cor. 5.1):
    P^(lambda)_{B->BC}(x) = rho_BC^{1/2-i l/2} rho_B^{-1/2+i l/2} x
                            rho_B^{-1/2-i l/2} rho_BC^{1/2+i l/2},
    rho~_ABC = (id_A (x) P^(lambda)_{B->BC})(rho_AB (x) 1_C).

Gaussian implementation.  Every factor is a number-conserving fermionic
Gaussian operator K exp(sum_ij c_i^dag X_ij c_j); with T := e^X the product
rule is T_1 T_2 (Klich), Tr = K det(1+T), and the state's correlation matrix
is C = T(1+T)^{-1}, i.e. T = G = C/(1-C).  Hence with alpha=(1-i lambda)/2,
    T~ = [1_A (+) T_BC^alpha] [1_AC (+) T_B^{-alpha}] [T_AB (+) 1_C]
         [1_AC (+) T_B^{-abar}] [1_A (+) T_BC^abar],
which is Hermitian positive definite, G~ = T~, Q~ = T~(1+T~)^{-1}, and the
normalisation K det(1+T~) = 1 is an exact check of the composition.
(VWZ's own correlation-matrix route is their App. A.5, Majorana form, citing
Ref. [50] eqs. (44), (51); they report needing ~5L digits, which is why they
stopped at L_A,L_B <= 8.  We use mpmath at adaptive precision instead.)

Fidelity / relative entropy: Note 5 Thm 3.2 (finite-dimensional quasi-free
determinant representation),
    Fid = det[(1-Q1)(1-Q2)]^{1/2} det[1+(G1^{1/2} G2 G1^{1/2})^{1/2}],
    D   = Tr[Q1(log Q1 - log Q2) + (1-Q1)(log(1-Q1)-log(1-Q2))].
In terms of t_i = eig(G1), s_i = eig(G2), tau_i = eig(G1^{1/2}G2 G1^{1/2}):
    -log F = 1/2 sum log(1+t) + 1/2 sum log(1+s) - sum log(1+sqrt(tau)).
"""
import sys, time, math
import mpmath as mp


def corr_infinite(n):
    """C_ij = sin(pi(i-j)/2)/(pi(i-j)) on n consecutive sites (exact)."""
    C = mp.matrix(n, n)
    half = mp.mpf(1) / 2
    for i in range(n):
        C[i, i] = half
        for j in range(i + 1, n):
            d = j - i
            if d % 2 == 0:
                v = mp.mpf(0)
            else:
                v = mp.mpf((-1) ** ((d - 1) // 2)) / (mp.pi * d)
            C[i, j] = v
            C[j, i] = v
    return C


def block(C, i0, i1):
    m = i1 - i0
    B = mp.matrix(m, m)
    for a in range(m):
        for b in range(m):
            B[a, b] = C[i0 + a, i0 + b]
    return B


def gspec(Csub):
    """Eigen-decomposition of a real-symmetric correlation block.
    Returns (V, t) with Csub = V diag(w) V^T and t = w/(1-w) = eig(G)."""
    E, V = mp.eigsy(Csub)
    m = Csub.rows
    t = [E[k] / (1 - E[k]) for k in range(m)]
    return V, t


def embed_pow(V, t, alpha, n, off):
    """n x n identity with V diag(t^alpha) V^H placed at offset off."""
    m = V.rows
    M = mp.eye(n)
    p = [mp.power(t[k], alpha) for k in range(m)]
    for a in range(m):
        for b in range(m):
            s = mp.mpc(0)
            for k in range(m):
                s += V[a, k] * p[k] * mp.conj(V[b, k])
            M[off + a, off + b] = s
    return M


def hermitize(M):
    n = M.rows
    H = mp.matrix(n, n)
    for a in range(n):
        H[a, a] = mp.re(M[a, a])
        for b in range(a + 1, n):
            v = (M[a, b] + mp.conj(M[b, a])) / 2
            H[a, b] = v
            H[b, a] = mp.conj(v)
    return H


def recovered_G(nA, nB, nC, C, lam):
    """T~ = G of the rotated-Petz-recovered state on ABC, plus the log of the
    normalisation K det(1+T~) (must be 0)."""
    n = nA + nB + nC
    al = (1 - 1j * mp.mpf(lam)) / 2
    ab = mp.conj(al)
    Vab, tab = gspec(block(C, 0, nA + nB))
    Vb, tb = gspec(block(C, nA, nA + nB))
    Vbc, tbc = gspec(block(C, nA, n))
    Xbc_a = embed_pow(Vbc, tbc, al, n, nA)
    Xbc_b = embed_pow(Vbc, tbc, ab, n, nA)
    Xb_a = embed_pow(Vb, tb, -al, n, nA)
    Xb_b = embed_pow(Vb, tb, -ab, n, nA)
    Xab = embed_pow(Vab, tab, mp.mpf(1), n, 0)
    T = hermitize(Xbc_a * (Xb_a * (Xab * (Xb_b * Xbc_b))))
    logK = (-sum(mp.log(1 + x) for x in tbc) + sum(mp.log(1 + x) for x in tb)
            - sum(mp.log(1 + x) for x in tab))
    return T, logK


def fid_relent(C1, T2):
    """-log Fid and D(rho1||rho2) from Q1 = C1 (real symmetric) and G2 = T2."""
    n = C1.rows
    E1, V1 = mp.eigsy(C1)
    w1 = [E1[k] for k in range(n)]
    t1 = [w / (1 - w) for w in w1]
    E2, V2 = mp.eighe(T2)
    s2 = [E2[k] for k in range(n)]
    # M = G1^{1/2} G2 G1^{1/2}
    r1 = [mp.sqrt(x) for x in t1]
    A = mp.matrix(n, n)              # A = G1^{1/2} V2 diag(sqrt(s2))
    for a in range(n):
        for l in range(n):
            s = mp.mpc(0)
            for k in range(n):
                s += V1[a, k] * r1[k] * mp.fsum([V1[b, k] * V2[b, l] for b in range(n)])
            A[a, l] = s * mp.sqrt(s2[l])
    tau = mp.eighe(A * A.H, eigvals_only=True)
    mlogF = (mp.fsum([mp.log(1 + x) for x in t1]) / 2
             + mp.fsum([mp.log(1 + x) for x in s2]) / 2
             - mp.fsum([mp.log(1 + mp.sqrt(abs(tau[k]))) for k in range(n)]))
    # relative entropy: Tr[Q1 log Q1 + (1-Q1)log(1-Q1)] - Tr[Q1 log Q2 + (1-Q1)log(1-Q2)]
    S1 = mp.fsum([w * mp.log(w) + (1 - w) * mp.log(1 - w) for w in w1])
    lq2 = [mp.log(x / (1 + x)) for x in s2]
    l1q2 = [-mp.log(1 + x) for x in s2]
    cross = mp.mpf(0)
    for l in range(n):
        # <l| Q1 |l> in the V2 basis
        u = [mp.fsum([mp.conj(V2[b, l]) * V1[b, k] for b in range(n)]) for k in range(n)]
        q1ll = mp.fsum([w1[k] * abs(u[k]) ** 2 for k in range(n)])
        cross += q1ll * lq2[l] + (1 - q1ll) * l1q2[l]
    return mlogF, S1 - cross


# ---------------------------------------------------------------- exact 2^n check
def _jw(n):
    import numpy as np
    I2 = np.eye(2); Z = np.diag([1.0, -1.0]); cm = np.array([[0.0, 1.0], [0.0, 0.0]])
    ops = []
    for j in range(n):
        M = np.array([[1.0]])
        for k in range(n):
            M = np.kron(M, Z if k < j else (cm if k == j else I2))
        ops.append(M.astype(complex))
    return ops


def _quad(c, X, off):
    """sum_ab X_ab c_{off+a}^dag c_{off+b} as a 2^n matrix."""
    import numpy as np
    m = X.shape[0]
    M = np.zeros_like(c[0])
    for a in range(m):
        for b in range(m):
            if X[a, b] != 0:
                M += X[a, b] * (c[off + a].conj().T @ c[off + b])
    return M


def _gexp(c, Cblk, off, power, n):
    """(rho_blk)^power (x) 1 as a 2^n matrix, from the block correlation matrix."""
    import numpy as np
    w, V = np.linalg.eigh(Cblk)
    X = V @ np.diag(np.log(w / (1 - w))) @ V.conj().T
    pref = power * np.sum(np.log(1 - w))
    M = _quad(c, X, off)
    e, U = np.linalg.eigh(M)
    return np.exp(pref) * (U @ np.diag(np.exp(power * e)) @ U.conj().T)


def exact_check(nA, nB, nC, lam, dps=30):
    """Ground truth from the 2^n many-body matrices (double precision)."""
    import numpy as np, scipy.linalg as sla
    mp.mp.dps = dps
    n = nA + nB + nC
    Cm = corr_infinite(n)
    Cn = np.array([[float(Cm[i, j]) for j in range(n)] for i in range(n)])
    c = _jw(n)
    al = (1 - 1j * lam) / 2
    rAB = _gexp(c, Cn[:nA + nB, :nA + nB], 0, 1.0, n)
    rB_a = _gexp(c, Cn[nA:nA + nB, nA:nA + nB], nA, -al, n)
    rB_b = _gexp(c, Cn[nA:nA + nB, nA:nA + nB], nA, -al.conjugate(), n)
    rBC_a = _gexp(c, Cn[nA:, nA:], nA, al, n)
    rBC_b = _gexp(c, Cn[nA:, nA:], nA, al.conjugate(), n)
    rt = rBC_a @ rB_a @ rAB @ rB_b @ rBC_b
    rho = _gexp(c, Cn, 0, 1.0, n)
    sr = sla.sqrtm(rho)
    F = np.trace(sla.sqrtm(sr @ rt @ sr)).real
    ev = np.linalg.eigvalsh(rho)
    lr = sla.logm(rho); lrt = sla.logm(rt)
    D = np.trace(rho @ (lr - lrt)).real
    return -math.log(F), D, np.trace(rt).real


# ---------------------------------------------------------------- flint backend
from flint import acb, arb, acb_mat, ctx


def corr_flint(n):
    pi = arb.pi()
    M = acb_mat(n, n)
    for i in range(n):
        M[i, i] = acb(arb(1) / 2)
        for j in range(i + 1, n):
            d = j - i
            v = acb(0) if d % 2 == 0 else acb(arb((-1) ** ((d - 1) // 2)) / (pi * d))
            M[i, j] = v
            M[j, i] = v
    return M


def _subm(M, i0, i1):
    m = i1 - i0
    S = acb_mat(m, m)
    for a in range(m):
        for b in range(m):
            S[a, b] = M[i0 + a, i0 + b]
    return S


def _dag(V):
    return V.conjugate().transpose()


def heig(M):
    """Hermitian eigen-decomposition (approx algorithm, eigenvectors unitary)."""
    ev, V = M.eig(right=True, algorithm="approx")
    return [x.real for x in ev], V


def _spec_T(Cblk):
    """(V, t) with Cblk = V diag(w) V^H, t = w/(1-w) = eig(G)."""
    w, V = heig(Cblk)
    return V, [x / (1 - x) for x in w]


def _pw(V, t, alpha):
    """V diag(t^alpha) V^H."""
    m = V.nrows()
    D = acb_mat(m, m)
    for k in range(m):
        D[k, k] = (acb(t[k]).log() * alpha).exp()
    return V * D * _dag(V)


def _embed(P, n, off):
    M = acb_mat(n, n)
    for i in range(n):
        M[i, i] = acb(1)
    m = P.nrows()
    for a in range(m):
        for b in range(m):
            M[off + a, off + b] = P[a, b]
    return M


def kappa_max(n, bits=None):
    if bits:
        ctx.prec = bits
    w, _ = heig(corr_flint(n))
    return max(abs(float((x / (1 - x)).log())) for x in w)


def bits_for(n, safety=250):
    """3 kappa_max / log 2 bits (two factors of the condition number of G) + margin."""
    return int(3.0 * (1.8 * n + 4) / math.log(2)) + safety


def run_case(nA, nB, nC, lams, bits=None, verbose=True):
    """Returns {lam: (-log F, D, |normalisation defect|)} for one geometry."""
    n = nA + nB + nC
    ctx.prec = bits or bits_for(n)
    t0 = time.time()
    C = corr_flint(n)
    Vab, tab = _spec_T(_subm(C, 0, nA + nB))
    Vb, tb = _spec_T(_subm(C, nA, nA + nB))
    Vbc, tbc = _spec_T(_subm(C, nA, n))
    V1, t1 = _spec_T(C)
    G1h = _pw(V1, t1, acb(arb(1) / 2))
    Xab = _embed(_pw(Vab, tab, acb(1)), n, 0)
    logK = (-sum((1 + x).log() for x in tbc) + sum((1 + x).log() for x in tb)
            - sum((1 + x).log() for x in tab))
    S1 = sum((x / (1 + x)) * (x / (1 + x)).log() + (1 / (1 + x)) * (1 / (1 + x)).log()
             for x in t1)
    half = acb(arb(1) / 2)
    out = {}
    for lam in lams:
        al = acb(arb(1), arb(-lam)) / 2
        ab = al.conjugate()
        T = (_embed(_pw(Vbc, tbc, al), n, nA) * _embed(_pw(Vb, tb, -al), n, nA) * Xab
             * _embed(_pw(Vb, tb, -ab), n, nA) * _embed(_pw(Vbc, tbc, ab), n, nA))
        T = (T + _dag(T)) * half
        s2, V2 = heig(T)
        tau = [x.real for x in (G1h * T * G1h).eig(algorithm="approx")]
        mlogF = (sum((1 + x).log() for x in t1) / 2 + sum((1 + x).log() for x in s2) / 2
                 - sum((1 + x.sqrt()).log() for x in tau))
        norm = logK + sum((1 + x).log() for x in s2)
        Y = _dag(V2) * C * V2
        D = S1 - sum(Y[l, l].real * (s2[l] / (1 + s2[l])).log()
                     - (1 - Y[l, l].real) * (1 + s2[l]).log() for l in range(n))
        out[lam] = (float(mlogF), float(D), abs(float(norm)))
    if verbose:
        print("# (%d,%d,%d) n=%d bits=%d  %.1fs" % (nA, nB, nC, n, ctx.prec, time.time() - t0),
              flush=True)
    return out


# ---------------------------------------------------------------- continuum Phi
F2 = 1.0 / (12 * math.pi ** 2)          # f_2 = c/(12 pi^2) per chiral component (Note 7)
# fidelity_tables.tex, Table "tab:scan", column Phi (A): Lam=60, kappa_max=30, eps=1e-8
PHI_TAB = [(0.0083, 5.8155e-07), (0.0167, 2.3073e-06), (0.0333, 9.0814e-06),
           (0.0667, 3.5193e-05), (0.1333, 1.3243e-04), (0.2667, 4.7267e-04),
           (0.5333, 1.5458e-03)]


def phi_cont(z):
    """Continuum single-chirality Phi(zeta): f2 zeta^2 below 1/120, log-log
    interpolation of Table 3 column A inside, power-law continuation above
    (slope of the last tabulated interval; EXTRAPOLATED, flagged in the output)."""
    if z <= 0:
        return 0.0
    if z < 1.0 / 120:
        return F2 * z * z
    xs = [math.log(a) for a, _ in PHI_TAB]
    ys = [math.log(b) for _, b in PHI_TAB]
    x = math.log(z)
    if x >= xs[-1]:
        s = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        return math.exp(ys[-1] + s * (x - xs[-1]))
    for k in range(len(xs) - 1):
        if x <= xs[k + 1]:
            f = (x - xs[k]) / (xs[k + 1] - xs[k])
            return math.exp(ys[k] * (1 - f) + ys[k + 1] * f)
    raise RuntimeError


def eta_of(LA, LB, LC):
    return LA * LC / float((LA + LB) * (LB + LC))


GEOMS = []          # (L, b) with L_A = L_C = L, L_B = b, n = 2L+b <= NMAX
NMAX = 72
for L in (4, 6, 8, 12, 16, 20, 24):
    for b in (1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 42, 49, 56):
        if 2 * L + b <= NMAX:
            GEOMS.append((L, b))
LAMS = (0.0, 0.5, 1.0, 1.5)


def sweep(geoms=None, lams=LAMS, out=sys.stdout):
    for (L, b) in (geoms or GEOMS):
        r = run_case(L, b, L, lams, verbose=False)
        e = eta_of(L, b, L)
        for lam in lams:
            mF, D, nd = r[lam]
            print("DATA L=%d b=%d n=%d eta=%.8f lam=%.2f mlogF=%.12e D=%.12e nrm=%.1e"
                  % (L, b, 2 * L + b, e, lam, mF, D, nd), file=out, flush=True)


# ---------------------------------------------------------------- analysis
def load(fn="sweep.raw"):
    rec = []
    for line in open(fn):
        if not line.startswith("DATA"):
            continue
        d = dict(p.split("=") for p in line.split()[1:])
        rec.append(dict(L=int(d["L"]), b=int(d["b"]), n=int(d["n"]), eta=float(d["eta"]),
                        lam=float(d["lam"]), mF=float(d["mlogF"]), D=float(d["D"])))
    return rec


def best(rec, lam):
    """largest n at each eta, sorted by eta"""
    h = {}
    for r in rec:
        if r["lam"] != lam:
            continue
        k = round(r["eta"], 10)
        if k not in h or r["n"] > h[k]["n"]:
            h[k] = r
    return sorted(h.values(), key=lambda r: r["eta"])


def phi_lat_factory(rec):
    """Phi_lat(zeta) := (1/2)(-log F^(0)) at zeta = 2 eta/(1-eta), log-log PCHIP."""
    from scipy.interpolate import PchipInterpolator
    pts = [(2 * r["eta"] / (1 - r["eta"]), 0.5 * r["mF"]) for r in best(rec, 0.0)]
    xs = [math.log(z) for z, _ in pts]
    ys = [math.log(p) for _, p in pts]
    f = PchipInterpolator(xs, ys)
    zlo, zhi = math.exp(xs[0]), math.exp(xs[-1])
    slo = (ys[1] - ys[0]) / (xs[1] - xs[0])
    shi = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])

    def phi(z):
        if z <= 0:
            return 0.0
        if z < zlo:
            return math.exp(ys[0] + slo * (math.log(z) - math.log(zlo)))
        if z > zhi:
            return math.exp(ys[-1] + shi * (math.log(z) - math.log(zhi)))
        return math.exp(float(f(math.log(z))))
    return phi, zlo, zhi


def local_exp(rows, key="mF"):
    out = {}
    for i, r in enumerate(rows):
        if i == 0 or i == len(rows) - 1:
            continue
        a, b_ = rows[i - 1], rows[i + 1]
        out[round(r["eta"], 10)] = (math.log(b_[key]) - math.log(a[key])) / \
                                   (math.log(b_["eta"]) - math.log(a["eta"]))
    return out


def fit_exp(rows, lo, hi, key="mF"):
    xs = [math.log(r["eta"]) for r in rows if lo <= r["eta"] <= hi]
    ys = [math.log(r[key]) for r in rows if lo <= r["eta"] <= hi]
    m = len(xs)
    if m < 2:
        return float("nan")
    mx, my = sum(xs) / m, sum(ys) / m
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def report(fn="sweep.raw"):
    rec = load(fn)
    phiL, zlo, zhi = phi_lat_factory(rec)
    print("=" * 100)
    print("O7(a) LATTICE TEST OF THE TWO-BRANCH ROTATED-PETZ LAW  (complex hopping chain, c=cbar=1)")
    print("geometries: L_A=L_C=L, L_B=b, n=2L+b<=%d;  eta_V=L^2/(L+b)^2;  z=eta/(1-eta)" % NMAX)
    print("=" * 100)
    b0 = best(rec, 0.0)
    print("\n[1] Phi_lat(zeta) := (1/2)(-log F^(0)) at zeta=2z  vs continuum Table 3 col A"
          "   (f2=%.7f)" % F2)
    print("%9s %5s %14s %14s %8s %11s" % ("zeta", "n", "Phi_lat", "Phi_cont", "ratio", "Phi_lat/z^2"))
    for r in b0:
        z = 2 * r["eta"] / (1 - r["eta"])
        pl = 0.5 * r["mF"]
        pc = phi_cont(z) if z <= PHI_TAB[-1][0] * 1.0001 else float("nan")
        print("%9.5f %5d %14.6e %14.6e %8.4f %11.6f"
              % (z, r["n"], pl, pc, pl / pc if pc == pc else float("nan"), pl / z ** 2))
    print("\n[2] two-branch law  -log F^(lam) = Phi(z(1+e^{-pi lam})) + Phi(z(1+e^{pi lam}))")
    print("    columns: lattice | 2-branch with Phi_lat | 2-branch with continuum Phi |"
          " single-branch Phi(z(1+e^{-pi lam})) [the wrong law]")
    for lam in LAMS:
        rows = best(rec, lam)
        le = local_exp(rows)
        print("\n  lambda = %.1f" % lam)
        print("  %8s %5s %14s %14s %7s %14s %7s %13s %7s %7s"
              % ("eta_V", "n", "-logF(lat)", "2br(Phi_lat)", "ratio", "2br(Phi_cont)",
                 "ratio", "1br", "ratio", "p_loc"))
        for r in rows:
            z = r["eta"] / (1 - r["eta"])
            zm, zp = z * (1 + math.exp(-math.pi * lam)), z * (1 + math.exp(math.pi * lam))
            p2l = phiL(zm) + phiL(zp)
            p2c = phi_cont(zm) + phi_cont(zp)
            p1 = phiL(zm)
            flag = "*" if zp > zhi else " "
            print("  %8.5f %5d %14.6e %14.6e %7.4f %14.6e %7.4f %13.6e %7.4f %7.3f%s"
                  % (r["eta"], r["n"], r["mF"], p2l, r["mF"] / p2l, p2c, r["mF"] / p2c,
                     p1, r["mF"] / p1, le.get(round(r["eta"], 10), float("nan")), flag))
    print("\n  (* : the large branch zeta_+ exceeds the range zeta<=%.2f of Phi_lat -> extrapolated)"
          % zhi)
    print("\n[3] apparent exponents p of -log F^(lam) ~ eta^p (least squares in log-log)")
    print("  %6s %10s %10s %10s | %10s %10s" % ("lambda", "eta<=0.1", "0.02-0.2", "0.05-0.5",
                                                "VWZ fit", "Note 5"))
    vwz = {0.0: 2.0, 0.5: 1.9, 1.0: 1.7, 1.5: 1.2}
    n5 = {0.0: 2.04, 0.5: 2.04, 1.0: 1.96, 1.5: 1.31}
    for lam in LAMS:
        rows = best(rec, lam)
        pr = [dict(eta=r["eta"],
                   mF=phi_cont(r["eta"] / (1 - r["eta"]) * (1 + math.exp(-math.pi * lam)))
                       + phi_cont(r["eta"] / (1 - r["eta"]) * (1 + math.exp(math.pi * lam))))
              for r in rows]
        print("  %6.1f %10.3f %10.3f %10.3f | %10.2f %10.2f   [2br(Phi_cont): %.3f %.3f %.3f]"
              % (lam, fit_exp(rows, 0.0, 0.1), fit_exp(rows, 0.02, 0.2),
                 fit_exp(rows, 0.05, 0.5), vwz[lam], n5[lam],
                 fit_exp(pr, 0.0, 0.1), fit_exp(pr, 0.02, 0.2), fit_exp(pr, 0.05, 0.5)))
    print("\n[4] relative entropy D(rho_ABC || rho~_ABC): value, D/eta^2, local exponent")
    for lam in (0.0, 1.0):
        rows = best(rec, lam)
        le = local_exp(rows, "D")
        print("  lambda=%.1f  %10s %5s %14s %10s %8s" % (lam, "eta_V", "n", "D", "D/eta^2", "p_loc"))
        for r in rows:
            print("            %10.5f %5d %14.6e %10.5f %8.3f"
                  % (r["eta"], r["n"], r["D"], r["D"] / r["eta"] ** 2,
                     le.get(round(r["eta"], 10), float("nan"))))
    print("\n[5] finite-size drift at fixed eta_V (same L/b ratio, growing n), lambda=0")
    fam = {}
    for r in rec:
        if r["lam"] == 0.0:
            fam.setdefault(round(r["eta"], 8), []).append(r)
    for e in sorted(fam):
        rs = sorted(fam[e], key=lambda r: r["n"])
        if len(rs) >= 3:
            print("  eta=%.5f : " % e + "  ".join("n=%d:%.6e" % (r["n"], r["mF"]) for r in rs))


# Okabe-Ito, fixed order (colour-blind safe); identity is also carried by marker+label.
COLS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]
MRK = ["o", "s", "^", "D"]


def plot(fn="sweep.raw", png="collapse.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    rec = load(fn)
    phiL, zlo, zhi = phi_lat_factory(rec)
    plt.rcParams.update({"font.size": 10, "axes.labelsize": 11})
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.6))
    A = ax[0]
    for i, lam in enumerate(LAMS):
        rows = [r for r in best(rec, lam) if r["eta"] <= 0.55]
        e = np.array([r["eta"] for r in rows]); y = np.array([r["mF"] for r in rows])
        A.plot(e, y, MRK[i], ms=4.5, mfc="none", mew=1.2, color=COLS[i],
               label=r"$\lambda=%.1f$" % lam)
        eg = np.geomspace(e.min(), e.max(), 200)
        z = eg / (1 - eg)
        A.plot(eg, [phiL(x * (1 + math.exp(-math.pi * lam))) +
                    phiL(x * (1 + math.exp(math.pi * lam))) for x in z],
               "-", lw=1.6, color=COLS[i])
        A.plot(eg, [phiL(x * (1 + math.exp(-math.pi * lam))) for x in z],
               "--", lw=1.0, color=COLS[i], alpha=0.65)
    A.set_xscale("log"); A.set_yscale("log")
    A.set_xlabel(r"$\eta_V = L_AL_C/[(L_A+L_B)(L_B+L_C)]$")
    A.set_ylabel(r"$-\log F^{(\lambda)}$")
    A.set_title(r"lattice (markers) vs two-branch law $\Phi(z(1{+}e^{-\pi\lambda}))+\Phi(z(1{+}e^{\pi\lambda}))$"
                "\n(solid; exact at $\\lambda=0$ by construction of $\\Phi_{\\rm lat}$) and single branch (dashed)",
                fontsize=9)
    A.grid(True, which="both", lw=0.3, color="0.85")
    A.legend(frameon=False, fontsize=9, loc="lower right")
    B = ax[1]
    b0 = best(rec, 0.0)
    zz = np.array([2 * r["eta"] / (1 - r["eta"]) for r in b0])
    pl = np.array([0.5 * r["mF"] for r in b0])
    B.plot(zz, pl / zz ** 2, "o", ms=4.5, mfc="none", mew=1.2, color=COLS[0],
           label=r"lattice $\Phi_{\rm lat}/\zeta^2$")
    zt = np.array([a for a, _ in PHI_TAB]); pt = np.array([b for _, b in PHI_TAB])
    B.plot(zt, pt / zt ** 2, "s", ms=6, color=COLS[1], label=r"continuum $\Phi/\zeta^2$ (Table 3A)")
    B.axhline(F2, color="0.35", lw=1.0, ls=":")
    B.text(zz.min() * 1.15, F2 * 0.80, r"$f_2=1/(12\pi^2)$", fontsize=9, color="0.35")
    B.set_xscale("log"); B.set_yscale("log")
    B.set_xlabel(r"$\zeta$"); B.set_ylabel(r"$\Phi(\zeta)/\zeta^2$")
    B.set_title(r"single-chirality function extracted from $\lambda=0$", fontsize=9.5)
    B.grid(True, which="both", lw=0.3, color="0.85")
    B.legend(frameon=False, fontsize=9, loc="lower left")
    for a in ax:
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(png, dpi=170)
    print("wrote", png)


def report_family(fn="sweep.raw"):
    """Cleanest test: within ONE family L_A=L_C=L (same lattice UV cutoff at the two
    touching points) extract Phi_lat^{(L)} from lambda=0 and predict lambda>0."""
    rec = load(fn)
    Ls = sorted({r["L"] for r in rec})
    print("\n[6] fixed-L two-branch test (Phi_lat^{(L)} from lambda=0 of the SAME family)")
    for L in Ls:
        sub = [r for r in rec if r["L"] == L]
        if len({r["eta"] for r in sub}) < 5:
            continue
        phiL, zlo, zhi = phi_lat_factory(sub)
        print("\n  L_A=L_C=%d   (Phi_lat valid for %.4f <= zeta <= %.3f)" % (L, zlo, zhi))
        print("  %6s %8s %5s %13s %13s %8s %12s %8s"
              % ("lam", "eta_V", "n", "-logF(lat)", "2branch", "ratio", "1branch", "ratio"))
        for lam in LAMS:
            if lam == 0.0:
                continue
            devs = []
            for r in sorted([x for x in sub if x["lam"] == lam], key=lambda r: r["eta"]):
                z = r["eta"] / (1 - r["eta"])
                zm, zp = z * (1 + math.exp(-math.pi * lam)), z * (1 + math.exp(math.pi * lam))
                if zp > zhi or zm < zlo:
                    continue
                p2, p1 = phiL(zm) + phiL(zp), phiL(zm)
                devs.append(abs(r["mF"] / p2 - 1))
                print("  %6.1f %8.5f %5d %13.6e %13.6e %8.4f %12.4e %8.2f"
                      % (lam, r["eta"], r["n"], r["mF"], p2, r["mF"] / p2, p1, r["mF"] / p1))
            if devs:
                print("  %6.1f  -> max |ratio-1| = %.3f  over %d in-range points"
                      % (lam, max(devs), len(devs)))


def report_quad(fn="sweep.raw"):
    """Small-eta prediction  -log F^(lam) = f2 eta^2 [2 + 4 cosh(pi lam) + 2 cosh(2 pi lam)]
    (Note 5, paragraph after Cor. 5.1) and the 1/L drift of the fixed-L two-branch ratio."""
    rec = load(fn)
    print("\n[7] small-eta amplitude  A(lam) = (-log F)/eta^2  vs  f2[2+4cosh(pi l)+2cosh(2pi l)]")
    print("  %6s %12s %12s %8s   (largest-n point below eta=0.02, then eta->0 Richardson)"
          % ("lambda", "A(lattice)", "A(theory)", "ratio"))
    for lam in LAMS:
        rows = [r for r in best(rec, lam) if r["eta"] < 0.02]
        if not rows:
            continue
        r = min(rows, key=lambda r: r["eta"])
        th = F2 * (2 + 4 * math.cosh(math.pi * lam) + 2 * math.cosh(2 * math.pi * lam))
        a = r["mF"] / r["eta"] ** 2
        print("  %6.1f %12.5f %12.5f %8.4f   (eta=%.5f, n=%d)" % (lam, a, th, a / th,
                                                                  r["eta"], r["n"]))
    print("\n[8] 1/L drift of the fixed-L two-branch ratio (lambda=0.5, mean over eta<=0.05)")
    print("  %4s %10s %10s" % ("L", "ratio", "L(1-ratio)"))
    for L in sorted({r["L"] for r in rec}):
        sub = [r for r in rec if r["L"] == L]
        if len({r["eta"] for r in sub}) < 5:
            continue
        phiL, zlo, zhi = phi_lat_factory(sub)
        v = []
        for r in sub:
            if r["lam"] != 0.5 or r["eta"] > 0.05:
                continue
            z = r["eta"] / (1 - r["eta"])
            zm, zp = z * (1 + math.exp(-math.pi / 2)), z * (1 + math.exp(math.pi / 2))
            if zlo <= zm and zp <= zhi:
                v.append(r["mF"] / (phiL(zm) + phiL(zp)))
        if v:
            m = sum(v) / len(v)
            print("  %4d %10.5f %10.4f" % (L, m, L * (1 - m)))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sweep":
        sweep()
    elif len(sys.argv) > 1 and sys.argv[1] == "report":
        report()
        report_family()
        report_quad()
    elif len(sys.argv) > 1 and sys.argv[1] == "plot":
        plot()
    elif len(sys.argv) > 1 and sys.argv[1] == "validate":
        for g, lam in (((3, 2, 3), 0.0), ((3, 2, 3), 1.0), ((2, 3, 4), 0.5), ((4, 3, 3), 1.5)):
            gg = run_case(*g, [lam], verbose=False)[lam]
            ex = exact_check(*g, lam)
            print("VALIDATE %s lam=%.1f  gauss -logF=%.12f D=%.12f | exact %.12f %.12f "
                  "| Tr rho~=%.14f" % (g, lam, gg[0], gg[1], ex[0], ex[1], ex[2]))
