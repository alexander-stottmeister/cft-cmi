"""S9 (O9+O10): thermal states, massive RG flow, gap geometries on the lattice.

Extends numerics/lattice/petz_lattice.py (agent PL) from the vacuum hopping
chain to three new settings:

 (1) THERMAL   H = -sum_i (c_i^dag c_{i+1} + h.c.), half filling, inverse
     temperature beta:  C_ij(beta) = (1/2pi) int_{-pi}^{pi} dk e^{ik(i-j)}
     / (1 + e^{beta eps_k}),  eps_k = -2 cos k.
 (2) MASSIVE   staggered potential (-1)^i m c_i^dag c_i (single-particle gap
     2m), ground state; Markov c-function c_M and entropic c_E = 3 R S'(R).
 (3) GAP       regions A, G, B, C adjacent; recovery of rho_ABC from rho_AB by
     a channel on B, with G traced out.

Everything Gaussian; the rotated Petz map is composed exactly as in PL,
    T~ = [1_A (+) T_BC^a][1_AC (+) T_B^{-a}][T_AB (+) 1_C]
         [1_AC (+) T_B^{-abar}][1_A (+) T_BC^abar],  a = (1 - i lambda)/2,
with T = G = C/(1-C).  Linear algebra in python-flint ball arithmetic.
"""
import sys, math, cmath, time
import numpy as np
from flint import acb, arb, acb_mat, ctx
import petz_lattice as PL          # same directory: reuse the validated backend
from petz_lattice import _subm, _spec_T, _pw, _embed, _dag, heig, bits_for, F2

# ------------------------------------------------------------------ kernels
# All correlation matrices are real symmetric; they are built from periodic
# integrals (1/2pi) int_{-pi}^{pi} dq e^{iqr} f(q) with f analytic in a strip
# |Im q| < a, so the N-point trapezoidal rule converges like e^{-aN} and we
# choose N from the requested number of bits.  a = pi/(2 beta) (thermal, poles
# of the Fermi function at cos k = -i pi(2j+1)/(2beta)) and a = 2 asinh(m/2)
# (massive, branch points of E(q) = sqrt(m^2 + 4 cos^2(q/2)) at q = pi -+ ia).

def _npoints(a, bits, extra=30):
    return max(64, 4 * int(((bits + extra) * math.log(2) / a) / 4 + 1))


def kern_thermal(nmax, beta, bits):
    """h[d] = (1/2pi) int dk cos(k d)/(1 + e^{beta eps_k}), eps_k = -2 cos k,
    d = 0..nmax, in arb ball arithmetic (trapezoidal rule, N points)."""
    ctx.prec = bits
    N = _npoints(math.pi / (2.0 * beta), bits)
    h = [arb(0) for _ in range(nmax + 1)]
    twopi_N = arb.pi() * 2 / N
    bb = arb(beta)
    for mi in range(N):
        k = twopi_N * mi
        ck = k.cos()
        f = 1 / (1 + (-2 * bb * ck).exp())     # 1/(1+e^{beta eps_k})
        t0, t1 = arb(1), ck                    # cos(0k), cos(1k)
        h[0] += f
        for d in range(1, nmax + 1):
            h[d] += f * t1
            t0, t1 = t1, 2 * ck * t1 - t0
    return [x / N for x in h]


_KC = {}


def _kern(kind, nmax, par, bits):
    """Cached kernel: computed once per (kind, par, bits) up to NMAX_K sites."""
    key = (kind, par, bits)
    if key not in _KC or len(_KC[key]) < nmax + 2:
        N = max(nmax + 1, NMAX_K)
        _KC[key] = (kern_thermal if kind == "th" else kern_mass)(N, par, bits)
    return _KC[key]


NMAX_K = 80


def corr_thermal(n, beta, bits):
    """C_ij(beta) on n consecutive sites of the hopping chain (acb_mat)."""
    h = _kern("th", n - 1, beta, bits)
    M = acb_mat(n, n)
    for i in range(n):
        for j in range(n):
            M[i, j] = acb(h[abs(i - j)])
    return M


def kern_mass(rmax, m, bits):
    """h[r] = (1/2pi) int dq cos(q r)/(2 E(q)), E = sqrt(m^2+4cos^2(q/2)),
    r = -1..rmax (h[-1]=h[1]); returns a dict r -> arb."""
    ctx.prec = bits
    a = 2 * math.asinh(m / 2.0)
    N = _npoints(a, bits)
    mm = arb(m)
    h = [arb(0) for _ in range(rmax + 2)]
    twopi_N = arb.pi() * 2 / N
    for mi in range(N):
        q = twopi_N * mi
        cq = q.cos()
        E = (mm * mm + 2 + 2 * cq).sqrt()      # 4cos^2(q/2) = 2+2cos q
        f = 1 / (2 * E)
        t0, t1 = arb(1), cq
        h[0] += f
        for r in range(1, rmax + 2):
            h[r] += f * t1
            t0, t1 = t1, 2 * cq * t1 - t0
    return [x / N for x in h]


def corr_mass(n, m, bits, off=0):
    """Staggered chain (-1)^i m c_i^dag c_i, ground state, n consecutive sites
    starting at site `off` (parity matters).  C_{i,j} = f_{ab}(r), r = j//2-i//2
    with sublattice a = i%2 (a=0: potential +m).  f_AA(r) = d_{r0}/2 - m h(r),
    f_BB = d_{r0}/2 + m h(r), f_AB(r) = h(r)+h(r+1), f_BA(r) = h(r)+h(r-1)."""
    ctx.prec = bits
    if m == 0:
        return PL.corr_flint(n)
    rmax = n // 2 + 2
    h = _kern("m", rmax, m, bits)
    hh = lambda r: h[abs(r)]
    M = acb_mat(n, n)
    for i in range(n):
        gi, ai = (i + off) // 2, (i + off) % 2
        for j in range(n):
            gj, bj = (j + off) // 2, (j + off) % 2
            r = gj - gi
            if ai == bj:
                v = (arb(1) / 2 if r == 0 else arb(0)) + (arb(m) * hh(r)) * (1 if ai else -1)
            else:
                v = hh(r) + (hh(r + 1) if ai == 0 else hh(r - 1))
            M[i, j] = acb(v)
    return M


def sub_idx(C, idx):
    """Sub-correlation-matrix on a list of site indices (= partial trace)."""
    m = len(idx)
    S = acb_mat(m, m)
    for a in range(m):
        for b in range(m):
            S[a, b] = C[idx[a], idx[b]]
    return S


def vn_entropy(Cblk):
    """S = -sum [w log w + (1-w) log(1-w)] from a correlation block."""
    w, _ = heig(Cblk)
    s = arb(0)
    for x in w:
        y = x.real if hasattr(x, "real") else x
        s -= y * y.log() + (1 - y) * (1 - y).log()
    return s


def cmi(C, nA, nB, nC):
    """I(A:C|B) = S(AB)+S(BC)-S(B)-S(ABC) for the Gaussian state with
    correlation matrix C on the ordered blocks A,B,C."""
    n = nA + nB + nC
    return float(vn_entropy(_subm(C, 0, nA + nB)) + vn_entropy(_subm(C, nA, n))
                 - vn_entropy(_subm(C, nA, nA + nB)) - vn_entropy(_subm(C, 0, n)))


def run_C(C, nA, nB, nC, lams, bits, verbose=False):
    """PL.run_case for an arbitrary Gaussian reference state given by C.
    Returns {lam: (-log F, D(rho||rho~), |log normalisation defect|)}."""
    n = nA + nB + nC
    assert C.nrows() == n
    ctx.prec = bits
    t0 = time.time()
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
        tau = [x if float(x) > 0 else arb(0) for x in tau]
        mlogF = (sum((1 + x).log() for x in t1) / 2 + sum((1 + x).log() for x in s2) / 2
                 - sum((1 + x.sqrt()).log() for x in tau))
        norm = logK + sum((1 + x).log() for x in s2)
        Y = _dag(V2) * C * V2
        D = S1 - sum(Y[l, l].real * (s2[l] / (1 + s2[l])).log()
                     - (1 - Y[l, l].real) * (1 + s2[l]).log() for l in range(n))
        out[lam] = (float(mlogF), float(D), abs(float(norm)))
    if verbose:
        print("#   run_C (%d,%d,%d) bits=%d %.1fs" % (nA, nB, nC, bits, time.time() - t0),
              flush=True)
    return out


def exact_C(Cnp, nA, nB, nC, lam):
    """Ground truth from the 2^n many-body matrices for an arbitrary Gaussian C."""
    import scipy.linalg as sla
    n = nA + nB + nC
    c = PL._jw(n)
    al = (1 - 1j * lam) / 2
    g = lambda blk, off, p: PL._gexp(c, blk, off, p, n)
    rt = (g(Cnp[nA:, nA:], nA, al) @ g(Cnp[nA:nA + nB, nA:nA + nB], nA, -al)
          @ g(Cnp[:nA + nB, :nA + nB], 0, 1.0)
          @ g(Cnp[nA:nA + nB, nA:nA + nB], nA, -al.conjugate())
          @ g(Cnp[nA:, nA:], nA, al.conjugate()))
    rho = g(Cnp, 0, 1.0)
    sr = sla.sqrtm(rho)
    F = np.trace(sla.sqrtm(sr @ rt @ sr)).real
    D = np.trace(rho @ (sla.logm(rho) - sla.logm(rt))).real
    ev = np.linalg.eigvalsh(rho)
    S = float(-sum(x * math.log(x) for x in ev if x > 1e-300))
    return -math.log(F), D, np.trace(rt).real, S


def to_np(C):
    n = C.nrows()
    return np.array([[complex(C[i, j]) for j in range(n)] for i in range(n)])


def gap_C(LA, LG, LB, LC, bits, kind="vac", par=None):
    """Correlation matrix of the ABC-reduced state for the geometry
    A (LA) | G (LG) | B (LB) | C (LC): build C on all LA+LG+LB+LC sites and
    delete the G rows/columns (exactly the partial trace for Gaussian states)."""
    ntot = LA + LG + LB + LC
    Cf = {"vac": lambda: PL.corr_flint(ntot),
          "th": lambda: corr_thermal(ntot, par, bits),
          "m": lambda: corr_mass(ntot, par, bits)}[kind]()
    idx = list(range(LA)) + list(range(LA + LG, ntot))
    return sub_idx(Cf, idx)


def validate():
    """Every new ingredient against the exact 2^n many-body density matrices."""
    print("=" * 92)
    print("VALIDATION of the new ingredients against exact 2^n density matrices (n <= 10)")
    print("  columns: -logF (Gaussian | exact) , D (Gaussian | exact), Tr rho~, S(ABC) gauss|exact")
    print("=" * 92)
    cases = [("thermal beta=6", (3, 2, 3), lambda b: corr_thermal(8, 6.0, b), [0.0, 0.5]),
             ("thermal beta=2", (2, 3, 4), lambda b: corr_thermal(9, 2.0, b), [0.0, 1.0]),
             ("mass m=0.4", (3, 2, 3), lambda b: corr_mass(8, 0.4, b), [0.0, 0.5]),
             ("mass m=1.0 odd", (3, 3, 3), lambda b: corr_mass(9, 1.0, b, off=1), [0.0]),
             ("gap LG=2 vac", (3, 2, 3), lambda b: gap_C(3, 2, 2, 3, b), [0.0, 1.0]),
             ("gap LG=3 th b=6", (2, 3, 3), lambda b: gap_C(2, 3, 3, 3, b, "th", 6.0), [0.0])]
    ok = True
    for name, (nA, nB, nC), mk, lams in cases:
        n = nA + nB + nC
        bits = bits_for(n)
        C = mk(bits)
        g = run_C(C, nA, nB, nC, lams, bits)
        Snp = to_np(C)
        Sg = float(vn_entropy(C))
        for lam in lams:
            e = exact_C(Snp.real, nA, nB, nC, lam)
            df, dd, ds = abs(g[lam][0] - e[0]), abs(g[lam][1] - e[1]), abs(Sg - e[3])
            ok &= (df < 2e-7 and dd < 1e-9 and ds < 1e-9 and g[lam][2] < 1e-20)
            print("%-16s (%d,%d,%d) lam=%.1f  -logF %.10f | %.10f  D %.10f | %.10f"
                  "  Tr=%.14f  dS=%.2e  norm=%.1e"
                  % (name, nA, nB, nC, lam, g[lam][0], e[0], g[lam][1], e[1], e[2], ds,
                     g[lam][2]))
    # CMI from the four Gaussian entropies vs exact 2^n entropies (thermal, n=9)
    bits = bits_for(9)
    C = corr_thermal(9, 4.0, bits)
    nA, nB, nC = 3, 3, 3
    ex = [exact_C(to_np(_subm(C, *r)).real, len(range(*r)), 0, 0, 0.0)[3]
          for r in ((0, 6), (3, 9), (3, 6), (0, 9))]
    exc = ex[0] + ex[1] - ex[2] - ex[3]
    gc = cmi(C, nA, nB, nC)
    ok &= abs(gc - exc) < 1e-9
    print("CMI thermal beta=4 (3,3,3):  gaussian %.12f  exact-2^n %.12f  diff %.2e"
          % (gc, exc, abs(gc - exc)))
    print("VALIDATION", "PASSED" if ok else "FAILED")
    return ok


# ================================================================ (1) THERMAL
# Continuum dictionary.  The half-filled hopping chain has eps_k = -2 cos k, so
# the Fermi velocity is v = |d eps/dk|_{k=pi/2} = 2 SITES per unit of lattice
# time; a lattice inverse temperature beta corresponds to the length-unit
# inverse temperature beta_len = v beta = 2 beta of the continuum Dirac fermion
# (c = 1).  Hence the thermal correlation length is xi = beta_len/(2 pi) =
# beta/pi sites, and Note 3 eq. (thermal-asymp) predicts
#     I(A:C|B) ~ (c/3)(1-e^{-2 pi a/beta_len})(1-e^{-2 pi c/beta_len}) e^{-2 pi b/beta_len}
#              = ...  e^{- pi L_B/beta}            (kappa_CMI = pi),
# and, since -log F = 2 Phi(z) ~ 2 f_2 z^2 with z ~ eta ~ 3 CMI/c at small eta,
#     -log F ~ e^{-2 pi L_B/beta}                  (kappa_F = 2 pi = 6.28319).
KAPPA_F, KAPPA_I = 2 * math.pi, math.pi
LAMS = [0.0, 0.5, 1.0]


def cmi_cont_thermal(a, b, c, beta, v=2.0):
    """(c=1) Note 3 eq. (thermal-cmi) with beta_len = v beta."""
    s = lambda x: math.sinh(math.pi * x / (v * beta)) if beta < 1e30 else x
    return (1.0 / 3) * math.log(s(a + b) * s(b + c) / (s(b) * s(a + b + c)))


def thermal_scan(Ls=(8, 12, 16), betas=(4.0, 8.0, 16.0, 32.0),
                 bs=(1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40), nmax=72,
                 out=sys.stdout):
    rows = []
    for L in Ls:
        for beta in list(betas) + [INF]:
            for b in bs:
                n = 2 * L + b
                if n > nmax:
                    continue
                bits = bits_for(n)
                C = PL.corr_flint(n) if beta == INF else corr_thermal(n, beta, bits)
                r = run_C(C, L, b, L, LAMS, bits)
                I = cmi(C, L, b, L)
                rows.append((L, beta, b, I) + tuple(r[l][0] for l in LAMS)
                            + (r[0.0][1], r[0.0][2]))
                print("RAW %2d %8.1f %3d %.16e %.16e %.16e %.16e %.16e %.3e"
                      % rows[-1], file=out, flush=True)
    return rows


INF = float("inf")


def thermal_report(rows, out=sys.stdout):
    P = lambda *a: print(*a, file=out)
    P("=" * 100)
    P("(1) THERMAL hopping chain, half filling.  L_A = L_C = L, L_B = b, v = 2, "
      "beta_len = 2 beta, xi = beta/pi")
    P("=" * 100)
    vac = {(r[0], r[2]): r for r in rows if r[1] == INF}
    for L in sorted({r[0] for r in rows}):
        for beta in sorted({r[1] for r in rows if r[0] == L}):
            sel = sorted([r for r in rows if r[0] == L and r[1] == beta], key=lambda r: r[2])
            if not sel:
                continue
            P("\n L_A=L_C=%d  beta=%s" % (L, beta))
            P("   b/beta       -logF^(0)   /vacuum             CMI       CMI_cont"
              "   kap_F   kap_I  kap_Ic  ratio 2br")
            prev = None
            for r in sel:
                L_, beta_, b, I, f0, f5, f1, D, nrm = r
                v0 = vac.get((L, b))
                kf = ki = kic = float("nan")
                Ic = cmi_cont_thermal(L, b, L, beta)
                if prev is not None and beta != INF:
                    db = (b - prev[2]) / beta
                    kf = -math.log(f0 / prev[4]) / db
                    ki = -math.log(I / prev[3]) / db
                    kic = -math.log(Ic / cmi_cont_thermal(L, prev[2], L, beta)) / db
                et = eta_thermal(L, b, L, beta)
                z = et / (1 - et)
                P("  %6.2f  %14.7e  %7.4f  %14.7e %14.7e %7.4f %7.4f %7.4f  %12.4f"
                  % (b / beta, f0, f0 / v0[4] if v0 else float("nan"), I, Ic, kf, ki, kic,
                     f0 / (2 * PL.phi_cont(2 * z))))
                prev = r


def eta_thermal(a, b, c, beta, v=2.0):
    """Thermal cross ratio: 1-eta = sinh(b)sinh(a+b+c)/(sinh(a+b)sinh(b+c)) gives
    eta = sinh(pi a/bl) sinh(pi c/bl)/(sinh(pi(a+b)/bl) sinh(pi(b+c)/bl)), bl = v beta."""
    if beta == INF:
        return a * c / float((a + b) * (b + c))
    s = lambda x: math.sinh(math.pi * x / (v * beta))
    return s(a) * s(c) / (s(a + b) * s(b + c))


def _lsq_exp(xs, ys):
    """least squares log y = log A - kappa x; returns (kappa, A)."""
    n = len(xs)
    ly = [math.log(y) for y in ys]
    mx, my = sum(xs) / n, sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ly))
    k = -sxy / sxx
    return k, math.exp(my + k * mx)


def thermal_fit(rows, out=sys.stdout, xmin=2.0):
    P = lambda *a: print(*a, file=out)
    P("\n" + "=" * 100)
    P("(1a) SHIELDED REGIME  L_B >> beta:  fit -log F^(0) = A exp(-kappa_F L_B/beta) and")
    P("     I(A:C|B) = A' exp(-kappa_I L_B/beta) over L_B/beta >= %.1f." % xmin)
    P("     Continuum expectation: xi = v beta/(2 pi) = beta/pi sites (v = 2), so")
    P("     kappa_I = pi = %.5f and, if -log F ~ eta^2, kappa_F = 2 pi = %.5f."
      % (KAPPA_I, KAPPA_F))
    P("  L  beta   #pts   kappa_F     A_F      kappa_I     A_I    kappa_F/kappa_I  "
      "kappa_I(cont)")
    for L in sorted({r[0] for r in rows}):
        for beta in sorted({r[1] for r in rows if r[0] == L and r[1] != INF}):
            sel = [r for r in rows if r[0] == L and r[1] == beta and r[2] / beta >= xmin]
            if len(sel) < 3:
                continue
            xs = [r[2] / beta for r in sel]
            kf, Af = _lsq_exp(xs, [r[4] for r in sel])
            ki, Ai = _lsq_exp(xs, [r[3] for r in sel])
            kc, _ = _lsq_exp(xs, [cmi_cont_thermal(L, r[2], L, beta) for r in sel])
            P("  %2d %5.1f  %4d  %8.4f %10.3e  %8.4f %10.3e   %8.4f   %8.4f"
              % (L, beta, len(sel), kf, Af, ki, Ai, kf / ki, kc))
    P("\n(1b) SMALL L_B/beta:  the O(1/beta^2) thermal correction.  Note 3 eq. (thermal-cmi)")
    P("     expanded to first order gives  I_beta - I_vac = -pi^2 L_A L_C/(9 beta_len^2)")
    P("     = -pi^2 L_A L_C/(36 beta^2), independent of L_B; the table gives the measured")
    P("     ratio (I_beta - I_vac)/(-pi^2 L_A L_C/(36 beta^2)) and the same for -log F.")
    P("   L   b   beta   I_beta-I_vac   ratio to O(beta^-2)   dF=(-logF)_b-(-logF)_vac"
      "   dF/(-logF)_vac * beta^2")
    vac = {(r[0], r[2]): r for r in rows if r[1] == INF}
    for L in sorted({r[0] for r in rows}):
        for b in sorted({r[2] for r in rows if r[0] == L}):
            for beta in sorted({r[1] for r in rows if r[0] == L and r[1] != INF}):
                sel = [r for r in rows if r[0] == L and r[1] == beta and r[2] == b]
                v0 = vac.get((L, b))
                if not sel or not v0 or b > beta:
                    continue
                r = sel[0]
                pred = -math.pi ** 2 * L * L / (36.0 * beta ** 2)
                P("  %2d %3d %5.1f  %13.6e   %10.5f   %13.6e   %12.5f"
                  % (L, b, beta, r[3] - v0[3], (r[3] - v0[3]) / pred, r[4] - v0[4],
                     (r[4] - v0[4]) / v0[4] * beta ** 2))


def save(rows, fn):
    with open(fn, "w") as f:
        for r in rows:
            print(" ".join(repr(x) for x in r), file=f)


def load(fn):
    return [tuple(float(x) for x in l.split()) for l in open(fn) if l.strip()]


# ============================================================ (2) MASSIVE / RG
# Staggered potential (-1)^i m c_i^dag c_i: bands +-E(q), E = sqrt(m^2+4cos^2(q/2)),
# single-particle gap 2m.  Near q = pi, E = sqrt(m^2 + v^2 k^2) with v = 2 and k
# the momentum per SITE, so the continuum Dirac mass in inverse-length units is
# mu = m/v = m/2 and the correlation length is xi = 1/mu = 2/m sites.  The
# dimensionless RG variable is mu R = m R/2.
#
# Lattice regularisation.  The staggered chain has a two-site unit cell, so an
# interval is commensurate only if its length is even, and entropies depend on
# the parity of the first site.  We therefore (i) average over the two starting
# parities and (ii) use only EVEN interval lengths and even delta.  With
#   I_b(d) = 2S(b+d) - S(b) - S(b+2d) = -d^2 S''(b+d) + O(d^4),
# the centred assignment R = b + d gives c_M^(d)(R) = 3R^2 I_{R-d}(d)/d^2
#   = c_M(R) + O(d^2/R^2)   [at a fixed point c_M^(d) = -(3R^2/d^2)log(1-d^2/R^2)],
# so (4 c_M^(2) - c_M^(4))/3 removes the leading lattice bias.  Likewise
#   c_E(R) = 3R (S(R+2)-S(R-2))/4 = 3R S'(R) + O(1/R^2).

def S_int(R, m, bits, par):
    """von Neumann entropy of R consecutive sites starting on parity `par`.
    Kept as an arb: the second differences below are exponentially small in mR
    and would be destroyed by rounding S to double precision."""
    return vn_entropy(corr_mass(R, m, bits, off=par))


def cfun_scan(ms=(0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6), Rmax=40, bits=None,
              out=sys.stdout):
    bits = bits or bits_for(Rmax + 10)
    rows = []
    for m in ms:
        S = {}
        for R in range(2, Rmax + 11, 2):
            S[R] = sum(S_int(R, m, bits, p) for p in (0, 1)) / 2
        cm = lambda R, d: 3 * R * R * (2 * S[R] - S[R - d] - S[R + d]) / (d * d)
        for R in range(6, Rmax + 1, 2):
            cE = float(3 * R * (S[R + 2] - S[R - 2]) / 4)
            c2, c4 = float(cm(R, 2)), float(cm(R, 4))
            rows.append((m, R, cE, c2, c4, (4 * c2 - c4) / 3.0))
            print("RAWC %.4f %3d %.16e %.16e %.16e %.16e" % rows[-1], file=out, flush=True)
    return rows


def cfun_report(rows, out=sys.stdout):
    P = lambda *a: print(*a, file=out)
    P("=" * 100)
    P("(2) MASSIVE FLOW: entropic c_E(R) = 3 R S'(R) and Markov c_M(R) = -3R^2 S''(R)")
    P("    (Note 3, eqs. (cM), (cE)); staggered mass m, mu = m/2, xi = 2/m sites,")
    P("    RG variable mu R = m R/2.  PRIMARY DEFINITION c_M := c_M^(2) = 3R^2 I_{R-2}(2)/4,")
    P("    a genuine lattice CMI (>= 0 by SSA).  At a fixed point c_M^(d) =")
    P("    -(3R^2/d^2)log(1-d^2/R^2) = c(1 + d^2/2R^2 + ...), so c_M^(2) carries a known")
    P("    +2/R^2 bias; the Richardson column (4c_M^(2)-c_M^(4))/3 removes it in the UV")
    P("    but is INVALID once mu d >~ 1 (there I_{R-d}(d) is exponential in d, not")
    P("    polynomial) - it even goes negative in the deep IR and is shown for reference.")
    P("=" * 100)
    for m in sorted({r[0] for r in rows}):
        sel = sorted([r for r in rows if r[0] == m], key=lambda r: r[1])
        P("\n  m = %.4f    xi = %s sites" % (m, "inf" if m == 0 else "%.1f" % (2.0 / m)))
        P("     R     mu R        c_E        c_M=c_M^(2)   c_M^(4)     c_M^(Rich)   "
          "c_M/c_E   (c_M/c_E)/(mR)   dc_E     dc_M")
        for k, r in enumerate(sel):
            _, R, cE, c2, c4, cR = r
            cM = c2
            dE = (sel[k + 1][2] - sel[k - 1][2]) / 4 if 0 < k < len(sel) - 1 else float("nan")
            dM = (sel[k + 1][3] - sel[k - 1][3]) / 4 if 0 < k < len(sel) - 1 else float("nan")
            P("  %4d %8.3f  %11.4e  %11.4e  %11.4e  %11.4e  %9.4f  %9.4f  %9.2e %9.2e"
              % (R, m * R / 2, cE, cM, c4, cR, cM / cE if cE else float("nan"),
                 (cM / cE) / (m * R) if m * cE else float("nan"), dE, dM))


def eta_of_cmi(I):
    """cross ratio implied by the c=1 adjacent-interval law I = (1/3)log 1/(1-eta)."""
    return -math.expm1(-3.0 * I)


def two_branch(I, lam=0.0):
    """vacuum two-branch prediction -logF = Phi(z(1+e^{-pi lam})) + Phi(z(1+e^{pi lam}))
    evaluated at the cross ratio implied by the measured CMI."""
    e = eta_of_cmi(I)
    z = e / (1 - e)
    return PL.phi_cont(z * (1 + math.exp(-math.pi * lam))) + \
        PL.phi_cont(z * (1 + math.exp(math.pi * lam)))


def mass_petz_scan(L=8, bs=(8, 16), ms=(0.0, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2),
                   out=sys.stdout):
    """-log F and I(A:C|B) at fixed geometry as functions of m L_B."""
    rows = []
    for b in bs:
        n = 2 * L + b
        bits = bits_for(n)
        for m in ms:
            bm = bits + int(300 * m)      # near-product states need extra head-room
            C = corr_mass(n, m, bm)
            r = run_C(C, L, b, L, LAMS, bm)
            I = cmi(C, L, b, L)
            rows.append((L, b, m, I) + tuple(r[l][0] for l in LAMS) + (r[0.0][1], r[0.0][2]))
            print("RAWM %2d %3d %.5f %.16e %.16e %.16e %.16e %.16e %.3e" % rows[-1],
                  file=out, flush=True)
    return rows


def mass_petz_report(rows, out=sys.stdout):
    P = lambda *a: print(*a, file=out)
    P("=" * 100)
    P("(2b) MASSIVE FLOW at fixed geometry L_A=L_C=%d: -log F and I(A:C|B) vs m L_B"
      % rows[0][0])
    P("     mu L_B = m L_B/2 is the continuum RG variable; 'ratio 2br' tests whether the")
    P("     vacuum two-branch law still holds at the cross ratio implied by the CMI.")
    P("=" * 100)
    for b in sorted({r[1] for r in rows}):
        P("\n  L_B = %d" % b)
        P("      m     mu L_B      I(A:C|B)     -logF^(0)    -logF^(1/2)   -logF^(1)"
          "     D(rho||rho~)  ratio 2br(0) ratio 2br(1)  -logF/I")
        for r in sorted([x for x in rows if x[1] == b], key=lambda x: x[2]):
            L, b_, m, I, f0, f5, f1, D, nrm = r
            P("  %7.4f %8.3f  %13.6e %13.6e %13.6e %13.6e %13.6e %10.2f %10.2f %8.4f"
              % (m, m * b / 2, I, f0, f5, f1, D, f0 / (two_branch(I, 0.0) or float("nan")),
                 f1 / (two_branch(I, 1.0) or float("nan")), f0 / I))


# ================================================================== (3) GAP
def gap_scan(L=8, LGs=(0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96),
             nmax=140, out=sys.stdout):
    """A (L) | G (L_G) | B (L) | C (L), G traced out, channel on B."""
    rows = []
    for g in LGs:
        if 3 * L + g > nmax:
            continue
        bits = bits_for(min(3 * L + g, 5 * L))
        C = gap_C(L, g, L, L, bits)
        r = run_C(C, L, L, L, LAMS, bits)
        I = cmi(C, L, L, L)
        rows.append((L, g, I) + tuple(r[l][0] for l in LAMS) + (r[0.0][1], r[0.0][2]))
        print("RAWG %2d %3d %.16e %.16e %.16e %.16e %.16e %.3e" % rows[-1],
              file=out, flush=True)
    return rows


def gap_report(rows, out=sys.stdout):
    P = lambda *a: print(*a, file=out)
    P("=" * 100)
    P("(3) GAP GEOMETRY  A(L) | G(L_G) | B(L) | C(L), G traced out, Petz channel on B.")
    P("    Massless Dirac (c=1): the two-interval entropies give exactly")
    P("      I(A:C|B) = (1/3) log[(a+g+b)(g+b+c)/((g+b)(a+g+b+c))],")
    P("    i.e. the adjacent-interval law with L_B -> L_B + L_G, and the cross ratio")
    P("      eta_g = a c/[(a+g+b)(g+b+c)]  ->  a c/L_G^2,  so I ~ L_G^-2, -logF ~ L_G^-4.")
    P("=" * 100)
    P("   L_G     eta_g      I(A:C|B)      I_cont     I/I_cont    -logF^(0)"
      "     -logF^(1)   ratio 2br   p_I    p_F   -logF/I   norm")
    sel = sorted(rows, key=lambda r: r[1])
    for k, r in enumerate(sel):
        L, g, I, f0, f5, f1, D, nrm = r
        Ic = cmi_cont_thermal(L, L + g, L, INF)
        et = L * L / float((2 * L + g) * (2 * L + g))
        pI = pF = float("nan")
        if 0 < k < len(sel) - 1 and sel[k - 1][1] > 0:
            dl = math.log(sel[k + 1][1] / sel[k - 1][1])
            pI = -math.log(sel[k + 1][2] / sel[k - 1][2]) / dl
            pF = -math.log(sel[k + 1][3] / sel[k - 1][3]) / dl
        P("  %4d  %9.6f  %12.6e %12.6e %9.5f  %12.6e %12.6e %9.3f %6.3f %6.3f"
          "  %8.5f %8.1e"
          % (g, et, I, Ic, I / Ic, f0, f1, f0 / (two_branch(I, 0.0) or float("nan")),
             pI, pF, f0 / I, nrm))


def plots():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # (1) thermal shielding
    rows = load("thermal.raw")
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for L, mk in ((8, "o"), (12, "s"), (16, "^")):
        for beta, col in ((4.0, "C3"), (8.0, "C1"), (16.0, "C0"), (32.0, "C2"),
                          (INF, "k")):
            sel = sorted([r for r in rows if r[0] == L and r[1] == beta], key=lambda r: r[2])
            if not sel:
                continue
            x = [r[2] / (beta if beta != INF else 1.0) for r in sel]
            ax[0].semilogy(x, [r[4] for r in sel], mk + "-", color=col, ms=3, lw=.8,
                           alpha=.8, label=("L=%d beta=%s" % (L, beta)) if L == 8 else None)
            ax[1].loglog([r[3] for r in sel], [r[4] for r in sel], mk, color=col, ms=3)
    xs = [x / 4.0 for x in range(8, 45)]
    ax[0].semilogy(xs, [3e-2 * math.exp(-KAPPA_F * x) for x in xs], "k--", lw=1,
                   label=r"$e^{-2\pi L_B/\beta}$")
    ax[0].set_xlabel(r"$L_B/\beta$  (black: vacuum, $x=L_B$)")
    ax[0].set_ylabel(r"$-\log F^{(0)}$")
    ax[0].set_ylim(1e-30, 1)
    ax[0].legend(fontsize=5.5, ncol=2)
    ax[0].set_title("thermal shielding of the Petz recovery")
    ii = [10 ** (-14 + 0.5 * k) for k in range(30)]
    ax[1].loglog(ii, [8 * F2 * (eta_of_cmi(i) / (1 - eta_of_cmi(i))) ** 2 for i in ii],
                 "k--", lw=1, label=r"$8f_2\eta^2$ (two-branch)")
    ax[1].set_xlabel(r"$I(A:C|B)$")
    ax[1].set_ylabel(r"$-\log F^{(0)}$")
    ax[1].legend(fontsize=7)
    ax[1].set_title("two-branch law at finite temperature")
    fig.tight_layout()
    fig.savefig("thermal_shield.png", dpi=140)
    # (2) c-functions
    rows = load("cfun.raw")
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for m in sorted({r[0] for r in rows}):
        sel = sorted([r for r in rows if r[0] == m and r[3] > 0], key=lambda r: r[1])
        if m == 0:
            ax[0].plot([r[1] for r in sel], [r[2] for r in sel], "k:", lw=1)
            continue
        x = [m * r[1] / 2 for r in sel]
        p = ax[0].plot(x, [r[2] for r in sel], "-", lw=1, label="$c_E$, m=%.2f" % m)
        ax[0].plot(x, [r[3] for r in sel], "--", lw=1, color=p[0].get_color(),
                   label="$c_M$, m=%.2f" % m)
        ax[1].plot([m * r[1] for r in sel], [r[3] / r[2] for r in sel], "o-", ms=2, lw=.8,
                   label="m=%.2f" % m)
    ax[0].set_xlabel(r"$\mu R = mR/2$"); ax[0].set_ylabel("c-function")
    ax[0].set_xlim(0, 6); ax[0].set_ylim(0, 1.2); ax[0].legend(fontsize=6, ncol=2)
    ax[0].set_title(r"$c_E=3RS'$ (solid), $c_M=-3R^2S''$ (dashed)")
    ax[1].plot([0, 12], [0, 12], "k--", lw=1, label=r"$c_M/c_E = mR = 2\mu R$")
    ax[1].set_xlabel("$mR$"); ax[1].set_ylabel("$c_M/c_E$")
    ax[1].set_xlim(0, 12); ax[1].set_ylim(0, 12); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig("cfun_flow.png", dpi=140)
    # (3) gap
    rows = load("gap.raw")
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    for L, col in ((6, "C0"), (8, "C1"), (12, "C2")):
        sel = sorted([r for r in rows if r[0] == L and r[1] > 0], key=lambda r: r[1])
        if not sel:
            continue
        ax.loglog([r[1] for r in sel], [r[2] for r in sel], "o-", color=col, ms=3, lw=.8,
                  label="$I(A:C|B)$, L=%d" % L)
        ax.loglog([r[1] for r in sel], [r[3] for r in sel], "s--", color=col, ms=3, lw=.8,
                  label="$-\\log F^{(0)}$, L=%d" % L)
    g = [4 * 1.3 ** k for k in range(12)]
    ax.loglog(g, [3.0 / x ** 2 for x in g], "k:", lw=1, label=r"$\propto L_G^{-2}$")
    ax.set_xlabel("$L_G$"); ax.set_ylabel("")
    ax.legend(fontsize=6); ax.set_title("gap geometry: both decay as $L_G^{-2}$")
    fig.tight_layout(); fig.savefig("gap_decay.png", dpi=140)
    print("wrote thermal_shield.png cfun_flow.png gap_decay.png")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if cmd == "validate":
        validate()
    elif cmd == "thermal":
        rows = thermal_scan(out=open("thermal.log", "w"))
        save(rows, "thermal.raw")
        thermal_report(rows)
        thermal_fit(rows)
    elif cmd == "thermal_report":
        rows = load("thermal.raw")
        thermal_report(rows)
        thermal_fit(rows)
    elif cmd == "mass":
        rows = cfun_scan(out=open("cfun.log", "w"))
        save(rows, "cfun.raw")
        cfun_report(rows)
        rows = mass_petz_scan(out=open("masspetz.log", "w"))
        save(rows, "masspetz.raw")
        mass_petz_report(rows)
    elif cmd == "masspetz":
        rows = mass_petz_scan(out=open("masspetz.log", "w"))
        save(rows, "masspetz.raw")
        cfun_report(load("cfun.raw"))
        mass_petz_report(rows)
    elif cmd == "gap":
        rows = []
        for L in (6, 8, 12):
            rows += gap_scan(L=L, out=open("gap%d.log" % L, "w"))
        save(rows, "gap.raw")
        for L in (6, 8, 12):
            gap_report([r for r in rows if r[0] == L])
    elif cmd == "plot":
        plots()
    elif cmd == "report":
        thermal_report(load("thermal.raw")); thermal_fit(load("thermal.raw"))
        cfun_report(load("cfun.raw"))
        mass_petz_report(load("masspetz.raw"))
        for L in (6, 8, 12):
            g = [r for r in load("gap.raw") if r[0] == L]
            if g:
                gap_report(g)
