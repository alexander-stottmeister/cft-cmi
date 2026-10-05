#!/usr/bin/env python3
"""numerics/networks/lattice_chain.py -- Phase 6, track G2.

Sequential Gaussian (rotated) Petz chains on the half-filled infinite hopping chain
C_ij = sin(pi(i-j)/2)/(pi(i-j)), and the VWZ protocols 1(A), 1(B), 2, 3 (refs/VWZ_2307.14434.pdf Sec. 5).
Builds on numerics/lattice/petz_lattice.py (imported, never edited): corr_flint, _spec_T, _subm,
_pw, heig, bits_for, F2, PHI_TAB (= phi_cont's table).  The V0 reference (exact_hp) is independent of it.

One-sided step (rigor/network_corner_calculus.tex (C3)(i)): the VACUUM rotated Petz map of the inclusion
F(A_B) c F(A_B u A_new), P(x) = rho_M^a rho_B^-a x rho_B^-abar rho_M^abar, a = (1 - i lam)/2 (VWZ (5.1);
lam = 0 is the ordinary Petz map), applied to the state produced so far (tensored with 1 on A_new).
Gaussian form (Klich): rho = K exp(c^dag X c), T = e^X; T' = X_s (T_J (+) 1_new) X_s^dag with
X_s = 1 off M and T_M^a (T_B^-a (+) 1_new) on M; log K' = log K - logdet(1+T_M) + logdet(1+T_B).
Trace preservation of P gives the exact identity K' det(1+T') = 1 at every step (checked, 'nrm').
-log F and D(rho_I || rho~) by Note 5 Thm 3.2 exactly as petz_lattice.run_case.

Usage (from the repository root cft_cmi/; PYTHONDONTWRITEBYTECODE=1 recommended):
  $PYTHON numerics/networks/lattice_chain.py V0 > numerics/networks/validate.out     # validation (first)
  $PYTHON numerics/networks/lattice_chain.py sweep <VWZ_SETS keys>  > numerics/networks/vwz_<X>.raw
  $PYTHON numerics/networks/lattice_chain.py chains <CHAIN_SETS keys> > numerics/networks/chains_<X>.raw
  $PYTHON numerics/networks/lattice_chain.py {N1|...|N6} > numerics/networks/N<k>.out   # analyses of the raw files
  $PYTHON numerics/networks/lattice_chain.py PREC > numerics/networks/prec.out       # precision check
  $PYTHON numerics/networks/lattice_chain.py NRM > numerics/networks/nrm.out         # largest normalisation defects
The exact raw-file commands are listed in RAW_CMDS and in the header of every N<k>.out; summary in
numerics/networks/NETWORK_RESULTS.md.
"""
import math
import os
import sys
import time

_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
_NET = os.path.join(_ROOT, 'numerics', 'networks')
sys.path.insert(0, os.path.join(_ROOT, 'numerics', 'lattice'))
import petz_lattice as PL                     # noqa: E402  (imported, never edited)
from flint import acb, arb, acb_mat, ctx      # noqa: E402

HALF = None


def bounds(lengths):
    """Chain points in sites: p_1 = 0, p_{k+1} = p_k + l_k (returned 0-based list p[0..n])."""
    p = [0]
    for l in lengths:
        p.append(p[-1] + int(l))
    return p


def _embed(P, m, off):
    """m x m identity with the square block P at offset off."""
    M = acb_mat(m, m)
    for i in range(m):
        M[i, i] = acb(1)
    k = P.nrows()
    for a in range(k):
        for b in range(k):
            M[off + a, off + b] = P[a, b]
    return M


def _dag(V):
    return V.conjugate().transpose()


class Vac:
    """Vacuum of the infinite half-filled chain restricted to N consecutive sites; block spectra cached."""

    def __init__(self, N, bits):
        ctx.prec = bits
        self.N, self.bits = N, bits
        self.C = PL.corr_flint(N)
        self._spec, self._pow = {}, {}

    def spec(self, i0, i1):
        """(V, t, logdet(1+t), S): sites [i0, i1), t = eig(G), G = C/(1-C), S = von Neumann entropy."""
        k = (i0, i1)
        if k not in self._spec:
            V, t = PL._spec_T(PL._subm(self.C, i0, i1))
            ld = sum((1 + x).log() for x in t)
            S = -sum((x / (1 + x)) * (x / (1 + x)).log() + (1 / (1 + x)) * (1 / (1 + x)).log() for x in t)
            self._spec[k] = (V, t, ld, S)
        return self._spec[k]

    def pw(self, i0, i1, re, im=0.0):
        """G_block^alpha = V diag(t^alpha) V^dag, alpha = re + i im (re, im exact binary floats)."""
        k = (i0, i1, re, im)
        if k not in self._pow:
            V, t, _, _ = self.spec(i0, i1)
            self._pow[k] = PL._pw(V, t, acb(arb(re), arb(im)))
        return self._pow[k]


def logdet1p(T):
    m = T.nrows()
    return (T + _embed(acb_mat(0, 0), m, 0)).det().log().real


def run_protocol(vac, p, start, steps, lam=0.0):
    """start = (i, j): block A_i..A_j (1-based chain intervals); steps = [(k_new, (iB, jB)), ...]:
    adjoin A_k_new conditioning on the block A_iB..A_jB (must touch A_k_new).  Returns (T on the final
    block, (lo, hi) in sites, [|K det(1+T) - 1| per step as |log|])."""
    half = acb(arb(1) / 2)
    lo, hi = p[start[0] - 1], p[start[1]]
    T = vac.pw(lo, hi, 1.0)
    logK = -vac.spec(lo, hi)[2]
    nrm = [abs(float(logK + logdet1p(T)))]
    for (kn, (iB, jB)) in steps:
        k1, k2 = (kn, kn) if isinstance(kn, int) else kn
        nlo, nhi = p[k1 - 1], p[k2]
        blo, bhi = p[iB - 1], p[jB]
        if nlo == hi:
            assert blo >= lo and bhi == hi, 'A_B must end where A_new starts'
        elif nhi == lo:
            assert blo == lo and bhi <= hi, 'A_B must start where A_new ends'
        else:
            raise ValueError('A_new not adjacent to the block')
        mlo, mhi = min(blo, nlo), max(bhi, nhi)
        lo2, hi2 = min(lo, nlo), max(hi, nhi)
        m = hi2 - lo2
        XM = vac.pw(mlo, mhi, 0.5, -lam / 2) * _embed(vac.pw(blo, bhi, -0.5, lam / 2), mhi - mlo, blo - mlo)
        X = _embed(XM, m, mlo - lo2)
        T = X * _embed(T, m, lo - lo2) * _dag(X)
        T = (T + _dag(T)) * half
        logK = logK - vac.spec(mlo, mhi)[2] + vac.spec(blo, bhi)[2]
        lo, hi = lo2, hi2
        nrm.append(abs(float(logK + logdet1p(T))))
    return T, (lo, hi), nrm


def fid_relent(vac, T2):
    """-log F(rho_I, rho~) and D(rho_I || rho~) on all N sites (Note 5 Thm 3.2, as petz_lattice.run_case)."""
    N = vac.N
    V1, t1, ld1, S1 = vac.spec(0, N)
    G1h = vac.pw(0, N, 0.5)
    s2, V2 = PL.heig(T2)
    U = _dag(V2) * V2
    fid_relent.unitarity = max(abs(float((U[i, j] - (1 if i == j else 0)).abs_upper())) for i in range(N)
                               for j in range(N))   # D below assumes V2 unitary; reported in V0
    tau = [x.real for x in (G1h * T2 * G1h).eig(algorithm="approx")]
    mlogF = ld1 / 2 + sum((1 + x).log() for x in s2) / 2 - sum((1 + x.sqrt()).log() for x in tau)
    Y = _dag(V2) * vac.C * V2
    D = -S1 - sum(Y[l, l].real * (s2[l] / (1 + s2[l])).log() - (1 - Y[l, l].real) * (1 + s2[l]).log()
                  for l in range(N))
    return float(mlogF), float(D)


def cmi(vac, X, Y, Z):
    """I(X:Z|Y) = S(XY) + S(YZ) - S(Y) - S(XYZ) for consecutive site ranges X | Y | Z (vacuum)."""
    S = lambda a, b: vac.spec(a, b)[3]
    return float(S(X[0], Y[1]) + S(Y[0], Z[1]) - S(Y[0], Y[1]) - S(X[0], Z[1]))


# ---------------------------------------------------------------- exact 2^n check, high precision
# Independent of the Gaussian (Klich product) code: many-body matrices on the 2^n Fock space in the
# occupation basis (bit j = site j, Jordan-Wigner sign (-1)^{#occupied sites < j}), split into the particle-
# number sectors (every operator here conserves N), flint acb_mat at `bits`.  rho_blk^pw (x) 1 =
# K^pw exp(pw * sum_ab X_ab c_a^dag c_b), X = log(C/(1-C)), K = prod(1-w) (matrix exponential, no Gaussian
# composition rule).  -log F = -log sum_N Tr sqrt(r_N sigma_N r_N), r = rho_I^{1/2} = K^{1/2} exp(M/2);
# D = sum_N Tr rho_N (log K + M_N) - Tr rho_N log sigma_N (log sigma_N by eigendecomposition).
def _hop(s, a, b):
    """c_a^dag c_b |s> = sign |t> (t = None if zero); Jordan-Wigner order = site order."""
    if a == b:
        return (1, s) if (s >> a) & 1 else (0, None)
    if not (s >> b) & 1 or (s >> a) & 1:
        return (0, None)
    sg = bin(s & ((1 << b) - 1)).count('1')
    s2 = s ^ (1 << b)
    sg += bin(s2 & ((1 << a) - 1)).count('1')
    return (-1 if sg % 2 else 1), s2 ^ (1 << a)


def exact_hp(lengths, start, steps, lam=0.0, bits=400):
    ctx.prec = bits
    p = bounds(lengths)
    n = p[-1]
    pi = arb.pi()
    Cf = acb_mat(n, n)
    for i in range(n):
        for j in range(n):
            Cf[i, j] = acb(arb(1) / 2) if i == j else acb((pi * (i - j) / 2).sin() / (pi * (i - j)))
    sect = {}
    for st in range(1 << n):
        sect.setdefault(bin(st).count('1'), []).append(st)
    idx = {st: (N, k) for N, L in sect.items() for k, st in enumerate(L)}

    def mb(a0, a1):
        """(log K, {N: M_N}) of the vacuum block on sites [a0, a1)."""
        m = a1 - a0
        S = acb_mat(m, m)
        for i in range(m):
            for j in range(m):
                S[i, j] = Cf[a0 + i, a0 + j]
        ev, V = S.eig(right=True, algorithm='approx')
        w = [x.real for x in ev]
        X = V * acb_mat([[acb((w[k] / (1 - w[k])).log()) if k == l else acb(0) for l in range(m)]
                         for k in range(m)]) * _dag(V)
        out = {N: acb_mat(len(L), len(L)) for N, L in sect.items()}
        for st in range(1 << n):
            N, k = idx[st]
            for a in range(m):
                for b in range(m):
                    sg, t = _hop(st, a0 + a, a0 + b)
                    if sg:
                        out[N][idx[t][1], k] += sg * X[a, b]
        return sum((1 - x).log() for x in w), out

    cache = {}

    def rpow(a0, a1, z):
        if (a0, a1) not in cache:
            cache[(a0, a1)] = mb(a0, a1)
        lK, M = cache[(a0, a1)]
        return {N: (M[N] * z).exp() * (acb(lK) * z).exp() for N in M}

    a = acb(arb(1), arb(-lam)) / 2
    sig = rpow(p[start[0] - 1], p[start[1]], acb(1))
    for (kn, (iB, jB)) in steps:
        k1, k2 = (kn, kn) if isinstance(kn, int) else kn
        nlo, nhi, blo, bhi = p[k1 - 1], p[k2], p[iB - 1], p[jB]
        PM, PB = rpow(min(blo, nlo), max(bhi, nhi), a), rpow(blo, bhi, -a)
        for N in sig:
            Xs = PM[N] * PB[N]
            sig[N] = Xs * sig[N] * _dag(Xs)
    rh, r = rpow(0, n, acb(1)), rpow(0, n, acb(arb(1) / 2))
    lK, M = cache[(0, n)]
    F, D, tr = arb(0), arb(0), arb(0)
    for N in sig:
        sN = (sig[N] + _dag(sig[N])) * acb(arb(1) / 2)
        tr += sum(sN[k, k].real for k in range(sN.nrows()))
        F += sum(x.real.sqrt() for x in (r[N] * sN * r[N]).eig(algorithm='approx'))
        ev, V = sN.eig(right=True, algorithm='approx')
        m = sN.nrows()
        lS = V * acb_mat([[acb(ev[k].real.log()) if k == l else acb(0) for l in range(m)]
                          for k in range(m)]) * V.inv()     # V^-1, not V^dag: degenerate eigenspaces
        RL = rh[N] * (M[N] - lS)
        D += sum(RL[k, k].real for k in range(m)) + lK * sum(rh[N][k, k].real for k in range(m))
    return float(-F.log()), float(D), float(tr)


# ---------------------------------------------------------------- protocols (A,B,C,D = A_1..A_4)
PROT = {
    '1A': ((1, 2), [((3, 4), (2, 2))]),                 # P_{B->BCD} on rho_AB (coarse chain A|B|CD)
    '1B': ((1, 2), [(3, (2, 2)), (4, (2, 3))]),         # P_{B->BC}, then P_{BC->BCD} (union conditioning)
    '2': ((1, 2), [(3, (2, 2)), (4, (3, 3))]),          # P_{B->BC}, then P_{C->CD}
    '3LR': ((2, 3), [(1, (2, 2)), (4, (3, 3))]),        # start BC: P_{B->AB}, then P_{C->CD}
    '3RL': ((2, 3), [(4, (3, 3)), (1, (2, 2))]),        # the other order
    'RL': ((3, 4), [(2, (3, 3)), (1, (2, 2))]),         # mirror image of Protocol 2
    'U': ((2, 3), [(4, (3, 3)), (1, (2, 3))]),          # REF-P6-0: D on C, then A on the UNION BC
    'SW': ((2, 2), [(3, (2, 2)), (1, (2, 2))]),         # Ex. 5.6 (3 intervals): start A_2, A_3 on A_2, A_1 on A_2
    'S2': ((2, 3), [(1, (2, 2))]),                      # Ex. 5.6's second step alone: kept A_3, cond. A_2, new A_1
    'Ud': ((2, 3), [(4, (3, 3)), (1, (2, 4))]),         # REF-P6-0 variant: A_1 on the WHOLE block A_2A_3A_4
}


def lr_chain(n):
    """L->R Petz chain (def:LR): start A_1A_2, adjoin A_{k+1} on A_k, k = 2..n-1."""
    return ((1, 2), [(k + 1, (k, k)) for k in range(2, n)])


def gauss(lengths, name_or_prot, lam=0.0, extra_bits=200, vac=None):
    """-log F, D, max normalisation defect, unitarity defect for one protocol (Gaussian pipeline)."""
    p = bounds(lengths)
    N = p[-1]
    if vac is None or vac.N != N:
        vac = Vac(N, PL.bits_for(N) + extra_bits)
    start, steps = PROT[name_or_prot] if isinstance(name_or_prot, str) else name_or_prot
    T, (lo, hi), nrm = run_protocol(vac, p, start, steps, lam)
    assert (lo, hi) == (0, N), 'protocol not complete'
    mF, D = fid_relent(vac, T)
    return mF, D, max(nrm), fid_relent.unitarity, vac


def V0(out):
    """Validation: Gaussian sequential pipeline vs the independent 400-bit 2^n sector computation."""
    TOL_D, TOL_F = 1e-12, 1e-7          # fixed by rigor/phase6_g2_brief.md before the run
    cases = [((2, 2, 2, 2), nm, 0.0) for nm in ('1A', '1B', '2', '3LR', '3RL', 'RL', 'U')]
    cases += [((1, 3, 2, 2), nm, lam) for nm in ('2', '3LR', 'U') for lam in (0.0, 0.5, 1.0)]
    cases += [((2, 1, 3, 2), '1B', 1.0), ((2, 1, 3, 2), '1A', 1.0)]
    cases += [((3, 3, 3), 'SW', 0.0), ((2, 1, 2, 1, 2), lr_chain(5), 0.0), ((2, 2, 2, 2, 2), lr_chain(5), 0.0),
              ((3, 2, 2, 3), '2', 0.0), ((3, 2, 2, 3), '3LR', 0.0)]
    print('# V0: Gaussian sequential Petz pipeline (bits_for(n)+200) vs exact 2^n Fock-space computation in',
          '\n# particle-number sectors (flint, 400 bits; matrix exponentials, no Gaussian composition rule).',
          '\n# tolerances fixed before the run: |dD| <= %.0e, |d(-log F)| <= %.0e; normalisation |log K det(1+T)|'
          % (TOL_D, TOL_F), '\n# at every step <= 2^(-bits/2) (working precision 2^-bits); unit = max|V2^dag V2 - 1|.',
          file=out, flush=True)
    allok = True
    for (L, pr, lam) in cases:
        t0 = time.time()
        mF, D, nrm, un, vac = gauss(L, pr, lam)
        bits = vac.bits
        start, steps = PROT[pr] if isinstance(pr, str) else pr
        eF, eD, tr = exact_hp(list(L), start, steps, lam)
        ok = abs(mF - eF) <= TOL_F and abs(D - eD) <= TOL_D and nrm <= 2.0 ** (-bits / 2)
        allok &= ok
        print('V0 L=%s prot=%s lam=%.1f n=%d | gauss -logF=%.15e D=%.15e | exact %.15e %.15e Tr=%.15f |'
              ' dF=%.1e dD=%.1e nrm=%.1e unit=%.1e bits=%d %s %.0fs'
              % (L, pr if isinstance(pr, str) else 'LR%d' % len(L), lam, sum(L), mF, D, eF, eD, tr,
                 mF - eF, D - eD, nrm, un, bits, 'PASS' if ok else 'FAIL', time.time() - t0), file=out, flush=True)
    print('V0 RESULT: %s' % ('ALL PASS' if allok else 'FAILURES PRESENT'), file=out, flush=True)


# ---------------------------------------------------------------- continuum single-corner function Phi_A
# (i) paper 1 Table 3 col. A (petz_lattice.PHI_TAB, 0.0083 <= zeta <= 0.5333; petz_lattice.phi_cont);
# (ii) best estimates of numerics/results_largezeta_certified.txt sec. 4 (zeta = s/3, s = 3.2 ... 51.2; NOT
#      certified, rel. uncertainties 0.45% ... 6.6%).  Log-log linear interpolation as phi_cont.  Flags: 'tab'
#      inside (i); 'gap' in (0.5333, 1.0667) = interpolated across the gap between (i) and (ii); 'large' inside
#      (ii); 'extrap' outside both (power-law continuation of the last interval); 'f2' below 1/120 (f2 zeta^2).
LARGE = [(3.2 / 3, 4.41039e-03, 2.0e-05), (6.4 / 3, 1.07969e-02, 5.0e-05), (12.8 / 3, 2.24140e-02, 1.4e-04),
         (25.6 / 3, 3.97403e-02, 7.2e-04), (51.2 / 3, 6.41212e-02, 4.3e-03)]
TAB = [(z, v) for z, v in PL.PHI_TAB] + [(z, v) for z, v, _ in LARGE]
F2 = PL.F2


def phi_A(z):
    """(Phi_A(z) per chirality, flag)."""
    if z < 1.0 / 120:
        return F2 * z * z, 'f2'
    xs = [math.log(a) for a, _ in TAB]
    ys = [math.log(b) for _, b in TAB]
    x = math.log(z)
    flag = 'tab' if z <= PL.PHI_TAB[-1][0] * 1.0001 else ('gap' if z < LARGE[0][0] else 'large')
    if x >= xs[-1] or x < xs[0]:
        k = len(xs) - 2 if x >= xs[-1] else 0
        return math.exp(ys[k] + (ys[k + 1] - ys[k]) / (xs[k + 1] - xs[k]) * (x - xs[k])), 'extrap'
    for k in range(len(xs) - 1):
        if x <= xs[k + 1]:
            f = (x - xs[k]) / (xs[k + 1] - xs[k])
            return math.exp(ys[k] * (1 - f) + ys[k + 1] * f), flag


def S_closed(d):
    """Ghat(Delta)/Ghat(0) = cosh(D/2) - sinh^2(D/2) log coth(|D|/4) (card corner-kernel-closed-form, proved,
    rigor/network_second_order.tex thm:T4 (cf))."""
    d = abs(d)
    return math.cosh(d / 2) - math.sinh(d / 2) ** 2 * math.log(1 / math.tanh(d / 4))


def phi_Aq_spread(z):
    """Relative spread (max - min)/mean of the quadratic log-log interpolants over all 3-node stencils of
    consecutive table nodes whose span contains z (an estimate of the quadratic interpolation error)."""
    xs = [math.log(a) for a, _ in TAB]
    ys = [math.log(b) for _, b in TAB]
    x = math.log(z)
    vals = []
    for k in range(len(xs) - 2):
        if xs[k] <= x <= xs[k + 2]:
            X, Y = xs[k:k + 3], ys[k:k + 3]
            vals.append(math.exp(sum(Y[i] * math.prod((x - X[j]) / (X[i] - X[j]) for j in range(3) if j != i)
                                     for i in range(3))))
    return (max(vals) - min(vals)) / (sum(vals) / len(vals)) if len(vals) > 1 else float('nan')


def phi_Aq(z):
    """Quadratic (3-node Lagrange) log-log interpolation in the same table: |phi_Aq - phi_A| / phi_A is reported as
    the interpolation uncertainty of Phi_A (the linear interpolation lies below a concave log-log curve)."""
    xs = [math.log(a) for a, _ in TAB]
    ys = [math.log(b) for _, b in TAB]
    x = math.log(z)
    k = min(range(len(xs)), key=lambda i: abs(xs[i] - x))
    k = min(max(k - 1, 0), len(xs) - 3)
    X, Y = xs[k:k + 3], ys[k:k + 3]
    v = sum(Y[i] * math.prod((x - X[j]) / (X[i] - X[j]) for j in range(3) if j != i) for i in range(3))
    return math.exp(v)


# ---------------------------------------------------------------- convergence fits (AGENTS.md sec. 5)
TOL_FIT = 1e-4      # fixed before the production runs: admissible iff |residual| <= TOL_FIT at the 3 finest
NFIT = 4            # fits use the NFIT finest resolutions (all if fewer); fixed before the N1-N6 analyses


def _lsq(cols, ys):
    import numpy as np
    A = np.array(cols).T
    c, *_ = np.linalg.lstsq(A, np.array(ys), rcond=None)
    return c, A @ c - np.array(ys)


def fits(Ls, ys, tol=TOL_FIT):
    """Fits of y(L): '1/L' y = a + b/L; '1/L,1/L^2'; 'h^p' y = a + b L^-p (p free, scanned); 'logL' y = a + b
    log L (no limit).  Returns {name: (y_inf or None, max|res| at the 3 finest, admissible, dof, extra)}."""
    import numpy as np
    Ls, ys = list(map(float, Ls)), list(map(float, ys))
    order = sorted(range(len(Ls)), key=lambda i: Ls[i])[-NFIT:]      # the NFIT finest resolutions
    Ls, ys = [Ls[i] for i in order], [ys[i] for i in order]
    one = [1.0] * len(Ls)
    out = {}

    def rec(name, yinf, res, npar, extra=''):
        r3 = max(abs(x) for x in res[-3:])
        out[name] = (yinf, r3, r3 <= tol, len(Ls) - npar, extra)
    if len(Ls) >= 2:
        c, r = _lsq([one, [1 / L for L in Ls]], ys); rec('1/L', c[0], r, 2)
        c, r = _lsq([one, [math.log(L) for L in Ls]], ys); rec('logL', None, r, 2, 'b=%.3e' % c[1])
    if len(Ls) >= 3:
        c, r = _lsq([one, [1 / L for L in Ls], [1 / L ** 2 for L in Ls]], ys); rec('1/L,1/L^2', c[0], r, 3)
        best = None
        for p in np.linspace(0.2, 4.0, 381):
            c, r = _lsq([one, [L ** -p for L in Ls]], ys)
            if best is None or np.sum(r ** 2) < best[0]:
                best = (np.sum(r ** 2), p, c, r)
        rec('h^p', best[2][0], best[3], 3, 'p=%.2f' % best[1])
    return out


def fit_summary(Ls, ys, tol=TOL_FIT):
    """(estimate, spread over admissible extrapolating fits, text)."""
    fs = fits(Ls, ys, tol)
    txt = '; '.join('%s: %s res=%.1e %s dof=%d %s' % (k, ('%.6f' % v[0]) if v[0] is not None else '--', v[1],
                                                      'ADM' if v[2] else 'rej', v[3], v[4]) for k, v in fs.items())
    adm = [v[0] for k, v in fs.items() if v[2] and v[0] is not None]
    if not adm:
        return None, None, txt + '  => no admissible extrapolating fit'
    txt += '  [admissible: %s%s]' % (', '.join('%s (dof %d)' % (k, v[3]) for k, v in fs.items()
                                             if v[2] and v[0] is not None),
                                  '; ALL 0-dof' if all(v[3] == 0 for v in fs.values() if v[2] and v[0] is not None)
                                  else '')
    flag = '  [logL also admissible: divergence not excluded]' if fs.get('logL', (0, 0, False))[2] else ''
    if len(adm) == 1:      # a single admissible fit has no spread: use the distance to every extrapolating fit
        allx = [v[0] for v in fs.values() if v[0] is not None]
        return adm[0], max(abs(x - adm[0]) for x in allx), txt + flag + \
            '  [one admissible fit: uncertainty = max distance to all extrapolating fits]'
    return sum(adm) / len(adm), max(adm) - min(adm), txt + flag


# ---------------------------------------------------------------- VWZ symmetric setup sweep (raw data)
# L_A = L_D = a m, L_B = L_C = b m sites; eta = a/(a+2b) (VWZ (5.9)); resolutions m.  'e' sets: Protocols
# 1(A), 1(B), 2, 3 (3RL = 3LR and RL = mirror of 2 are identical on the lattice, V0) + the vacuum CMIs.
# 'm' sets: the single step 1(A) at a'/b' = 2a/b = zeta_eff of Protocol 3 at eta (lattice-internal Phi_A).
VWZ_SETS = {
    'e005': (2, 19, [1, 2, 3]), 'e010': (2, 9, [1, 2, 3, 4]), 'e015': (6, 17, [1, 2, 3]),
    'e020': (1, 2, [2, 3, 4, 6, 8, 10, 12]), 'e030': (6, 7, [1, 2, 3]), 'e040': (4, 3, [1, 2, 3, 4, 5]),
    'm010': (4, 9, [1, 2, 3]), 'm020': (1, 1, [3, 4, 6, 8, 12, 18]), 'm030': (12, 7, [1, 2, 3]),
    # extensions (more resolutions of the same geometry; merged with the set of the same name minus 'x')
    'm020x': (1, 1, [10, 14, 16, 20, 24]), 'e030x': (6, 7, [4]), 'm010x': (4, 9, [4]), 'm030x': (12, 7, [4]),
}


def sweep_vwz(keys, out):
    for key in keys:
        a0, b0, ms = VWZ_SETS[key]
        prots = ('1A', '1B', '2', '3LR') if key[0] == 'e' else ('1A',)
        for m in ms:
            a, b = a0 * m, b0 * m
            L = (a, b, b, a)
            vac = None
            for pr in prots:
                t0 = time.time()
                mF, D, nrm, un, vac = gauss(L, pr, 0.0, vac=vac)
                print('DATA set=%s eta=%.8f a=%d b=%d m=%d n=%d prot=%s mlogF=%.15e D=%.15e nrm=%.1e unit=%.1e '
                      'bits=%d t=%.0f' % (key, a / (a + 2.0 * b), a, b, m, 2 * (a + b), pr, mF, D, nrm, un, vac.bits,
                                          time.time() - t0), file=out, flush=True)
            if key[0] == 'e':
                A, B, C, Dd = (0, a), (a, a + b), (a + b, a + 2 * b), (a + 2 * b, 2 * a + 2 * b)
                I1 = cmi(vac, A, B, (C[0], Dd[1]))
                I2, I3, I4 = cmi(vac, A, B, C), cmi(vac, B, C, Dd), cmi(vac, A, (B[0], C[1]), Dd)
                I5 = cmi(vac, (A[0], B[1]), C, Dd)
                print('CMI set=%s eta=%.8f a=%d b=%d m=%d n=%d IA_CD_B=%.15e IA_C_B=%.15e IB_D_C=%.15e '
                      'IA_D_BC=%.15e IAB_D_C=%.15e' % (key, a / (a + 2.0 * b), a, b, m, 2 * (a + b), I1, I2, I3,
                                                        I4, I5), file=out, flush=True)


def load_raw(pattern):
    import glob
    rec = []
    for fn in sorted(glob.glob(os.path.join(_NET, pattern))):
        for line in open(fn):
            if line.startswith('DATA') or line.startswith('CMI'):
                d = dict(x.split('=', 1) for x in line.split()[1:])
                d['kind'] = line.split()[0]
                rec.append(d)
    return rec


# ---------------------------------------------------------------- corner data (Thm 5.2, general rule)
def _stepmap(p, sig, right):
    """R_{p,sig} (A_new to the right of p) or L_{p,sig}: (map, derivative)."""
    if right:
        return (lambda x: x if x <= p else p + (x - p) / (1 + sig * (x - p)),
                lambda x: 1.0 if x <= p else 1.0 / (1 + sig * (x - p)) ** 2)
    return (lambda x: x if x >= p else p + (x - p) / (1 - sig * (x - p)),
            lambda x: 1.0 if x >= p else 1.0 / (1 - sig * (x - p)) ** 2)


def corner_measure(lengths, prot, theta=1.0):
    """Corners of the composite point map Phi = k_1 o ... o k_N by Thm 5.2 (no hypothesis): list of
    (x_m, kappa_m = sigma_m G_m'(x_m), zeta^(I) = kappa beta_I(x), y_I(x)), coincident points merged;
    sigma_m = theta 2 l_new/(l_B (l_B + l_new)) (ordinary Petz: theta = 1); real (not site) lengths."""
    p = [0.0]
    for l in lengths:
        p.append(p[-1] + float(l))
    start, steps = PROT[prot] if isinstance(prot, str) else prot
    maps = []
    for (kn, (iB, jB)) in steps:
        k1, k2 = (kn, kn) if isinstance(kn, int) else kn
        nlo, nhi, blo, bhi = p[k1 - 1], p[k2], p[iB - 1], p[jB]
        lB, ln = bhi - blo, nhi - nlo
        sig = theta * 2 * ln / (lB * (lB + ln))
        right = nlo >= bhi
        pc = blo if right else bhi
        maps.append((pc, sig) + _stepmap(pc, sig, right))
    T = p[-1]
    out = {}
    for m, (pc, sig, _, _) in enumerate(maps):
        later = list(reversed(maps[m + 1:]))          # G_m = k_{m+1} o ... o k_N: apply k_N first

        def G(x):
            d = 1.0
            for (_, _, f, df) in later:
                d *= df(x)
                x = f(x)
            return x, d
        lo, hi = 1e-13 * T, (1 - 1e-13) * T
        if not (G(lo)[0] < pc < G(hi)[0]):
            continue                                   # swallowed: p^(m) not in the range of G_m
        a, b = lo, hi
        for _ in range(200):                           # G_m increasing: bisection for x_m = G_m^-1(p^(m))
            c = 0.5 * (a + b)
            a, b = (c, b) if G(c)[0] < pc else (a, c)
        x = 0.5 * (a + b)
        key = round(x, 9)
        out[key] = out.get(key, 0.0) + sig * G(x)[1]
    return [(x, k, k * x * (T - x) / T, math.log(x / (T - x))) for x, k in sorted(out.items())]


# ---------------------------------------------------------------- analyses of the VWZ sweep
def _table(key):
    """{m: {'n','a','b', prot: (mlogF, D), 'cmi': {...}}} for one VWZ set from numerics/networks/vwz_*.raw."""
    t = {}
    for d in load_raw('vwz_*.raw'):
        if d['set'].rstrip('x') != key:
            continue
        r = t.setdefault(int(d['m']), {'n': int(d['n']), 'a': int(d['a']), 'b': int(d['b'])})
        if d['kind'] == 'DATA':
            r[d['prot']] = (float(d['mlogF']), float(d['D']))
        else:
            r['cmi'] = {k: float(v) for k, v in d.items() if k.startswith('I')}
    return t


def stable(a, b):
    """Digits of a and b that agree (AGENTS.md sec. 5: digits stable across the two finest resolutions)."""
    sa, sb = '%.10f' % a, '%.10f' % b
    k = 0
    while k < len(sa) and k < len(sb) and sa[k] == sb[k]:
        k += 1
    st = sa[:k].rstrip('.')
    return st if any(ch.isdigit() and ch != '0' for ch in st) else 'none'


def _fitline(out, label, ns, ys):
    est, spr, txt = fit_summary(ns, ys)
    o = sorted(range(len(ns)), key=lambda i: ns[i])
    stab = stable(ys[o[-1]], ys[o[-2]]) if len(ns) >= 2 else '--'
    out.write('  %-34s n=%s\n    values: %s\n    stable digits (two finest): %s\n    fits: %s\n    => %s\n' % (
        label, ns, ' '.join('%.10f' % y for y in ys), stab, txt,
        'extrapolated %.6f +- %.1e (spread of admissible fits)' % (est, spr) if est is not None else 'none'))
    return est, spr


def N1(out):
    out.write('# N1: r_1 = Phi^(1B)/Phi^(1A) (ordinary Petz, Phi = -log F, two chiralities), VWZ symmetric setup\n'
              '# L_A = L_D = a m, L_B = L_C = b m sites, eta = a/(a+2b); prop:1B1A predicts r_1 = 1 for all sizes.\n'
              '# On the lattice 1(B) = 1(A) is an operator identity (rho_BC^-a rho_BC^a = 1 between the steps), so\n'
              '# r_1 - 1 measures only rounding; criterion (brief N1): extrapolated r_1 - 1 within the fit spread of 0.\n')
    for key in ('e010', 'e020', 'e030'):
        t = _table(key)
        ms = sorted(m for m in t if '1B' in t[m])
        if not ms:
            out.write('\n%s: PENDING (no data)\n' % key)
            continue
        ns = [t[m]['n'] for m in ms]
        r = [t[m]['1B'][0] / t[m]['1A'][0] for m in ms]
        rD = [t[m]['1B'][1] / t[m]['1A'][1] for m in ms]
        out.write('\n%s eta=%.4f (a,b)=(%d,%d)x m, m=%s, n=%s\n' % (key, t[ms[0]]['a'] / (t[ms[0]]['a'] + 2.0 *
                  t[ms[0]]['b']), t[ms[0]]['a'] // ms[0], t[ms[0]]['b'] // ms[0], ms, ns))
        out.write('  r_1 - 1 (-log F):  %s\n  r_D - 1 (rel. ent.): %s\n' % (' '.join('%.1e' % (x - 1) for x in r),
                  ' '.join('%.1e' % (x - 1) for x in rD)))
        _fitline(out, 'r_1', ns, r)


def N2(out):
    out.write('# N2: Protocol 3 vs Theorem A (thm:prot3): Phi^(3) = Phi_A(zeta_eff), zeta_eff = (sigma_1+sigma_2)\n'
              '# beta_I(p_3) = 2a/b here.  Lattice dictionary (numerics/lattice/README.md, card two-branch-law-lattice):\n'
              '# at lambda = 0 both chiralities carry the same corner measure, so -log F_lat -> 2 Phi_A (c = 1 per\n'
              '# chirality), single-step lattice/continuum ratio 1 - 0.15/L.  Q1 = Phi^(3)_lat/(2 Phi_A(zeta_eff)) with\n'
              '# Phi_A from the continuum tables (flag); Q2 = Phi^(3)_lat(eta)/Phi^(1A)_lat(matched) where the matched\n'
              '# single step has a\'/b\' = 2a/b (lattice-internal, no table): both extrapolated separately.\n')
    for key, mk in (('e010', 'm010'), ('e020', 'm020'), ('e030', 'm030')):
        t, tm = _table(key), _table(mk)
        ms = sorted(m for m in t if '3LR' in t[m])
        if not ms or not tm:
            out.write('\n%s: PENDING (no data)\n' % key)
            continue
        a0, b0 = t[ms[0]]['a'] // ms[0], t[ms[0]]['b'] // ms[0]
        cm = corner_measure((a0, b0, b0, a0), '3LR')
        ze = cm[0][2]
        pa, fl = phi_A(ze)
        out.write('\n%s eta=%.4f: corner measure %s, zeta_eff = %.6f (2a/b = %.6f), Phi_A = %.6e [%s]\n'
                  % (key, a0 / (a0 + 2.0 * b0), [(round(x, 4), round(k, 6)) for x, k, _, _ in cm], ze,
                     2.0 * a0 / b0, pa, fl))
        ns = [t[m]['n'] for m in ms]
        e_q1, s_q1 = _fitline(out, 'Q1 = Phi3/(2 Phi_A(zeta_eff))', ns, [t[m]['3LR'][0] / (2 * pa) for m in ms])
        pq = phi_Aq(ze)
        if e_q1 is not None:
            q1q, sq = e_q1 * pa / pq, s_q1 * pa / pq
            out.write('  Q1 with the quadratic log-log interpolation Phi_Aq = %.6e: %.6f +- %.1e (interp. diff %.2f%%; '
                      '3-node stencil spread %.2f%%); |Q1q - 1| = %.1f fit spreads, |Q1 - 1| = %.1f fit spreads\n'
                      % (pq, q1q, sq, 100 * (pq / pa - 1), 100 * phi_Aq_spread(ze), abs(q1q - 1) / sq,
                         abs(e_q1 - 1) / s_q1))
        e3, s3 = _fitline(out, 'Phi3(n)/Phi3(n_max)', ns, [t[m]['3LR'][0] / t[ms[-1]]['3LR'][0] for m in ms])
        mm = sorted(tm)
        nm = [tm[m]['n'] for m in mm]
        e1, s1 = _fitline(out, 'Phi1A_matched(n)/(.)(n_max)', nm, [tm[m]['1A'][0] / tm[mm[-1]]['1A'][0] for m in mm])
        qa = t[ms[-1]]['3LR'][0] / tm[mm[-1]]['1A'][0]
        qb = t[ms[-2]]['3LR'][0] / tm[mm[-2]]['1A'][0]
        out.write('  raw Q2 (finest / second-finest resolutions of each): %.6f / %.6f, stable digits %s\n'
                  % (qa, qb, stable(qa, qb)))
        if e3 is not None and e1 is not None:
            P3, P1 = e3 * t[ms[-1]]['3LR'][0], e1 * tm[mm[-1]]['1A'][0]
            out.write('  Q2 = Phi3_inf/Phi1A_matched_inf = %.6f +- %.1e  (Phi3_inf = %.6e, 2Phi_A^lat(zeta_eff) = %.6e,'
                      ' continuum-table 2 Phi_A = %.6e [%s])\n' % (P3 / P1, P3 / P1 * (s3 / e3 + s1 / e1), P3, P1,
                                                                 2 * pa, fl))


ESETS = ('e005', 'e010', 'e015', 'e020', 'e030', 'e040')


def N3(out):
    out.write('# N3: Phi^(1), Phi^(2), Phi^(3) (lattice -log F, ordinary Petz, two chiralities) and D, VWZ symmetric\n'
              '# setup.  Corner data (corner_measure = Thm 5.2): zeta_1 = a/b (1A), zeta_2 = a(a+2b)/(2b(a+b)) at p_2\n'
              '# and zeta_3 = a/b at p_3 (Protocol 2), Delta_23 = log(1/eta); zeta_eff = 2a/b (Protocol 3).\n'
              '# P31 = Phi_A(2a/b)/Phi_A(a/b) (unconditional prediction, continuum tables, flags); P21_2 =\n'
              '# (zeta_2^2+zeta_3^2)/zeta_1^2 (Ghat-free part, second order); P21_A = (Phi_A(z2)+Phi_A(z3))/Phi_A(z1)\n'
              '# (no cross term, all orders).  X = (R21 - P21_2)/(2 z2 z3/z1^2) estimates Ghat(Delta_23)/Ghat(0) ONLY if\n'
              '# all zeta <= 0.2; X_A = (R21 Phi_A(z1) - Phi_A(z2) - Phi_A(z3))/(2 f2 z2 z3) removes the single-corner\n'
              '# higher orders.  Sizes: see m, n; n > 72 rows go beyond the brief\'s 72-site range (labelled).\n')
    XS = []
    for key in ESETS:
        t = _table(key)
        ms = sorted(m for m in t if '3LR' in t[m] and '2' in t[m])
        if not ms:
            out.write('\n%s: PENDING (no data)\n' % key)
            continue
        a0, b0 = t[ms[0]]['a'] // ms[0], t[ms[0]]['b'] // ms[0]
        eta = a0 / (a0 + 2.0 * b0)
        c2 = corner_measure((a0, b0, b0, a0), '2')
        z1 = corner_measure((a0, b0, b0, a0), '1A')[0][2]
        (z2, y2), (z3, y3) = [(c[2], c[3]) for c in c2]
        z3e = corner_measure((a0, b0, b0, a0), '3LR')[0][2]
        (p1, f1), (p2, f2_), (p3, f3_), (pe, fe) = phi_A(z1), phi_A(z2), phi_A(z3), phi_A(z3e)
        P31, P21, P21A = pe / p1, (z2 ** 2 + z3 ** 2) / z1 ** 2, (p2 + p3) / p1
        cw = 2 * z2 * z3 / z1 ** 2
        out.write('\n%s eta=%.4f (a,b)=(%d,%d) x m: z1=%.6f z2=%.6f z3=%.6f Delta23=%.6f (log 1/eta=%.6f) '
                  'zeta_eff=%.6f\n  P31=%.6f [%s,%s]  P21_2=%.6f  P21_A=%.6f [%s]  2z2z3/z1^2=%.6f\n'
                  % (key, eta, a0, b0, z1, z2, z3, y3 - y2, math.log(1 / eta), z3e, P31, f1, fe, P21, P21A, f2_, cw))
        out.write('  %3s %4s %15s %15s %15s %10s %10s %10s %10s %s\n' % ('m', 'n', 'Phi1', 'Phi2', 'Phi3', 'R21',
                  'R31', 'D2/D1', 'D3/D1', 'f_i = Phi_i/eta^2'))
        for m in ms:
            r = t[m]
            P = [r[k][0] for k in ('1A', '2', '3LR')]
            Dd = [r[k][1] for k in ('1A', '2', '3LR')]
            out.write('  %3d %4d %15.9e %15.9e %15.9e %10.6f %10.6f %10.6f %10.6f %s%s\n' % (
                m, r['n'], P[0], P[1], P[2], P[1] / P[0], P[2] / P[0], Dd[1] / Dd[0], Dd[2] / Dd[0],
                ' '.join('%.5f' % (x / eta ** 2) for x in P), '  (n > 72)' if r['n'] > 72 else ''))
        ns = [t[m]['n'] for m in ms]
        e31, s31 = _fitline(out, 'R31 = Phi3/Phi1 (unnormalised)', ns, [t[m]['3LR'][0] / t[m]['1A'][0] for m in ms])
        e21, s21 = _fitline(out, 'R21 = Phi2/Phi1 (unnormalised)', ns, [t[m]['2'][0] / t[m]['1A'][0] for m in ms])
        for lab, k in (('R31', '3LR'), ('R21', '2')):     # the same ratios fitted normalised by the finest value
            rr = [t[m][k][0] / t[m]['1A'][0] for m in ms]
            en, sn, txt = fit_summary(ns, [x / rr[-1] for x in rr])
            out.write('  %s normalised fit (y/y(n_max), TOL relative): %s\n' % (
                lab, ('%.6f +- %.1e' % (en * rr[-1], sn * rr[-1])) if en is not None else 'no admissible fit'))
        _fitline(out, 'D2/D1', ns, [t[m]['2'][1] / t[m]['1A'][1] for m in ms])
        _fitline(out, 'D3/D1', ns, [t[m]['3LR'][1] / t[m]['1A'][1] for m in ms])
        if e31 is not None:
            P31q = phi_Aq(z3e) / phi_Aq(z1)
            out.write('  R31_inf/P31 = %.6f +- %.1e   (quadratic interpolation: P31q = %.6f, R31_inf/P31q = %.6f)\n'
                      % (e31 / P31, s31 / P31, P31q, e31 / P31q))
        if e21 is not None:
            weak = max(z1, z2, z3) <= 0.2
            X, XA = (e21 - P21) / cw, (e21 * p1 - p2 - p3) / (2 * F2 * z2 * z3)
            lab = ('lattice estimate of Ghat(%.4f)/Ghat(0)' % (y3 - y2)) if weak else \
                'lattice, second order not yet reached (max zeta = %.3f > 0.2)' % max(z1, z2, z3)
            out.write('  excess R21_inf - P21_2 = %.6f +- %.1e; X = %.5f +- %.1e, X_A = %.5f +- %.1e  [%s]\n'
                      % (e21 - P21, s21, X, s21 / cw, XA, s21 * p1 / (2 * F2 * z2 * z3), lab))
            mx = ms[-1]
            XS.append((eta, z1, y3 - y2, X, s21 / cw, (t[mx]['2'][0] / t[mx]['1A'][0] - P21) / cw))
    ordF = ordD = True
    nrows = 0
    for key in ESETS:
        for m, r in _table(key).items():
            if all(k in r for k in ('1A', '2', '3LR')):
                nrows += 1
                ordF &= r['1A'][0] < r['2'][0] < r['3LR'][0]
                ordD &= r['1A'][1] < r['2'][1] < r['3LR'][1]
    out.write('\nOrdering check over all %d (eta, n) rows: Phi1 < Phi2 < Phi3: %s;  D1 < D2 < D3: %s\n'
              % (nrows, ordF, ordD))
    # comparison with the PROVED closed form S(Delta) = Ghat(Delta)/Ghat(0) (card corner-kernel-closed-form; it
    # replaces the interpolated G3 box values used in the first version of this output: same X/S to 0.002)
    out.write('\nComparison with the closed form S(Delta) = Ghat(Delta)/Ghat(0) (card corner-kernel-closed-form):\n')
    rows = []
    for eta, z1, d, X, sX, Xraw in XS:
        sg = S_closed(d)
        rows.append((z1, X / sg))
        out.write('  eta=%.2f Delta23=%.4f S=%.5f X=%.5f +- %.1e (finest-n raw X = %.5f) X/S=%.4f +- %.4f; '
                  '(S - X)/spread = %.1f; (1-X/S)/zeta_1=%.3f\n' % (eta, d, sg, X, sX, Xraw, X / sg, sX / sg,
                                                                    (sg - X) / sX if sX > 0 else float('inf'),
                                                                    (1 - X / sg) / z1))
    small = sorted(rows)[:3]
    c, r = _lsq([[1.0] * 3, [z for z, _ in small]], [v for _, v in small])
    out.write('  linear fit X/S = A + B zeta_1 on the three smallest zeta_1: A = %.4f, B = %.4f, max|res| = %.1e\n'
              % (c[0], c[1], max(abs(x) for x in r)))


# ---------------------------------------------------------------- chain sweeps for N4, N5, N6
CHAIN_SETS = {   # name: (base lengths, resolutions m, protocols); 'LR' = def:LR chain (+ its single steps)
    'n4r2': ((8, 4, 2, 1), [1, 2, 3, 4, 6], ('LR',)), 'n5r2': ((16, 8, 4, 2, 1), [1, 2, 3], ('LR',)),
    'n6r2': ((32, 16, 8, 4, 2, 1), [1, 2], ('LR',)), 'n4r3': ((27, 9, 3, 1), [1, 2, 3], ('LR',)),
    'n5r3': ((81, 27, 9, 3, 1), [1], ('LR',)),
    'sw': ((1, 1, 1), [4, 6, 8, 12, 16, 24], ('SW', 'S2')),
    'ref': ((13, 21, 9, 17), [1, 2, 3], ('U', 'Ud', '3LR')),
    'eq3': ((1, 1, 1), [4, 6, 8, 10, 12], ('LR',)), 'eq4': ((1, 1, 1, 1), [4, 6, 8, 10, 12], ('LR',)),
    'eq5': ((1, 1, 1, 1, 1), [4, 6, 8, 10, 12], ('LR',)), 'eq6': ((1, 1, 1, 1, 1, 1), [4, 6, 8, 10, 12], ('LR',)),
    # extensions (merged with the set of the same name minus 'x')
    'n4r2x': ((8, 4, 2, 1), [8, 10, 12], ('LR',)), 'eq3x': ((1, 1, 1), [16, 20, 24], ('LR',)),
    'n6r2x': ((32, 16, 8, 4, 2, 1), [3], ('LR',)),
}


def sweep_chain(keys, out):
    for key in keys:
        base, ms, prots = CHAIN_SETS[key]
        nb = len(base)
        for m in ms:
            L = tuple(l * m for l in base)
            p = bounds(L)
            vac = None
            for pr in prots:
                t0 = time.time()
                prot = lr_chain(nb) if pr == 'LR' else pr
                mF, D, nrm, un, vac = gauss(L, prot, 0.0, vac=vac)
                print('CHAIN set=%s m=%d n=%d L=%s prot=%s mlogF=%.15e D=%.15e nrm=%.1e unit=%.1e bits=%d t=%.0f'
                      % (key, m, p[-1], ','.join(map(str, L)), pr, mF, D, nrm, un, vac.bits, time.time() - t0),
                      file=out, flush=True)
            if 'LR' in prots:
                for k in range(2, nb):           # step k adjoins A_{k+1} on A_k, kept A_1..A_{k-1}
                    I = cmi(vac, (0, p[k - 1]), (p[k - 1], p[k]), (p[k], p[k + 1]))
                    mF, D, nrm, un, _ = gauss(L[:k + 1], ((1, k), [(k + 1, (k, k))]), 0.0)
                    print('STEP set=%s m=%d n=%d k=%d mlogF=%.15e D=%.15e I=%.15e nrm=%.1e' % (key, m, p[-1], k, mF,
                          D, I, nrm), file=out, flush=True)


def _chains(key):
    """{m: {'n', prot: (mlogF, D), 'steps': {k: (mlogF, D, I)}}} from numerics/networks/chains_*.raw."""
    t = {}
    for fn in sorted(__import__('glob').glob(os.path.join(_NET, 'chains_*.raw'))):
        for line in open(fn):
            w = line.split()
            if not w or w[0] not in ('CHAIN', 'STEP'):
                continue
            d = dict(x.split('=', 1) for x in w[1:])
            if d['set'].rstrip('x') != key:
                continue
            r = t.setdefault(int(d['m']), {'n': int(d['n']), 'steps': {}})
            if w[0] == 'CHAIN':
                r[d['prot']] = (float(d['mlogF']), float(d['D']))
            else:
                r['steps'][int(d['k'])] = (float(d['mlogF']), float(d['D']), float(d['I']))
    return t


def _lr_data(base):
    """def:LR corner data: [(k, zeta^(I), zeta_step, y_k)], zeta_step in I_step = (p_1, p_{k+2})."""
    p = bounds(base) if all(float(l).is_integer() for l in base) else None
    cm = corner_measure(base, lr_chain(len(base)))
    out = []
    for k, (x, kap, z, y) in zip(range(2, len(base)), cm):
        f = p[k + 1]
        out.append((k, z, kap * x * (f - x) / f, y))
    return out


def chordal_check(out, keys):
    """Thm 12.6 (thm:w6chord, card sequential-recovery-bound-type-iii; no hypothesis, valid for finite-dimensional
    algebras): d_B(total) <= sum_k d_B(step k), d_B = sqrt(2 - 2F), each step with the TRUE state as input
    (= the lattice single steps).  Prints max d_B(tot)/sum_k d_B(k) over all chains and resolutions."""
    d = lambda P: math.sqrt(2 - 2 * math.exp(-P))
    worst, nrow, best = 0.0, 0, (9.0, '')
    for key in keys:
        t = _chains(key)
        for m, r in t.items():
            if 'LR' in r and len(r['steps']) == len(CHAIN_SETS[key][0]) - 2 and len(r['steps']) >= 2:
                q = d(r['LR'][0]) / sum(d(v[0]) for v in r['steps'].values())
                worst, nrow = max(worst, q), nrow + 1
                best = min(best, (q, '%s n=%d' % (key, r['n'])))
                out.write('  chordal %s n=%d: d_B(tot)/sum_k d_B(step) = %.6f\n' % (key, r['n'], q))
    out.write('Chordal bound (Thm 12.6) over %d multi-step (chain, n) rows: max d_B(tot)/sum d_B(step) = %.6f, '
              'min = %.6f (%s) (theorem: <= 1, a consistency check; one-step chains are equalities)\n'
              % (nrow, worst, best[0], best[1]))


def N4(out):
    out.write('# N4: L->R Petz chains (def:LR, lem:LRdata), geometric lengths l_{k+1}/l_k = r, ordinary Petz.\n'
              '# Phi_tot = lattice -log F (two chiralities); S2 = 2 f2 sum_k (zeta_k^(I))^2 (second order, no cross\n'
              '# terms); SA = 2 sum_k Phi_A(zeta_k^(I)) (all orders, no cross terms); Sstep = sum_k Phi_step (lattice\n'
              '# single steps = Theorem-A triples (A_1..A_{k-1}|A_k|A_{k+1})); Samp = 2 sum_k Phi_A(zeta_step,k) is\n'
              '# what Sstep tends to; lem:ampl: zeta^(I) = zeta_step (1 + z\'); W6 (Cor 12.7, second order):\n'
              '# Phi_tot <= 2 f2 (sum_k zeta_k^(I))^2 =: SW6; all-orders analogue SW6A = 2 (sum_k sqrt(Phi_A(zeta_k)))^2.\n')
    for key in ('n4r2', 'n5r2', 'n6r2', 'n4r3', 'n5r3'):
        t = _chains(key)
        ms = sorted(m for m in t if 'LR' in t[m] and len(t[m]['steps']) == len(CHAIN_SETS[key][0]) - 2)
        if not ms:
            out.write('\n%s: PENDING (no data)\n' % key)
            continue
        base = CHAIN_SETS[key][0]
        cd = _lr_data(base)
        zs, zst = [c[1] for c in cd], [c[2] for c in cd]
        S2, SA = 2 * F2 * sum(z * z for z in zs), 2 * sum(phi_A(z)[0] for z in zs)
        Samp, SW6 = 2 * sum(phi_A(z)[0] for z in zst), 2 * F2 * sum(zs) ** 2
        SW6A = 2 * sum(math.sqrt(phi_A(z)[0]) for z in zs) ** 2     # (sum_k sqrt(Phi_A(zeta_k)))^2, 2 chiralities
        out.write('\n%s lengths %s x m: zeta^(I) = %s, zeta_step = %s, 1+z\' = %s, Delta_k = %s; flags %s\n'
                  '  S2 = %.6e  SA = %.6e  Samp = %.6e  SW6 = %.6e  SW6A = %.6e\n' % (
                      key, base, ['%.4f' % z for z in zs], ['%.4f' % z for z in zst],
                      ['%.4f' % (a / b) for a, b in zip(zs, zst)],
                      ['%.4f' % (cd[i + 1][3] - cd[i][3]) for i in range(len(cd) - 1)],
                      sorted({phi_A(z)[1] for z in zs + zst}), S2, SA, Samp, SW6, SW6A))
        out.write('  %3s %4s %15s %15s %9s %9s %9s %9s %9s %9s\n' % ('m', 'n', 'Phi_tot', 'Sstep', 'tot/S2', 'tot/SA',
                  'tot/Sstp', 'Sstp/Samp', 'tot/SW6', 'tot/SW6A'))
        rows = []
        for m in ms:
            P = t[m]['LR'][0]
            Ss = sum(v[0] for v in t[m]['steps'].values())
            rows.append((t[m]['n'], P / S2, P / SA, P / Ss, Ss / Samp, P / SW6, P / SW6A))
            out.write('  %3d %4d %15.9e %15.9e %9.5f %9.5f %9.5f %9.5f %9.5f %9.5f\n' % ((m, t[m]['n'], P, Ss) +
                                                                                    rows[-1][1:]))
        if len(ms) >= 2:
            for j, lab in ((1, 'Phi_tot/S2'), (2, 'Phi_tot/SA'), (3, 'Phi_tot/Sstep'), (4, 'Sstep/Samp')):
                _fitline(out, lab, [r[0] for r in rows], [r[j] for r in rows])
        else:
            out.write('  one resolution only: no extrapolation\n')
    out.write('\n')
    chordal_check(out, ('n4r2', 'n5r2', 'n6r2', 'n4r3', 'n5r3', 'eq3', 'eq4', 'eq5', 'eq6'))


def N5(out):
    out.write('# N5: where (H) fails (thm:general).  (a) Ex. 5.6 (lengths (1,1,1) m, start A_2, A_3 on A_2, then A_1 on\n'
              '# A_2): Thm 5.2 swallows the first corner, prediction Phi_tot = Phi(second step alone) = 2 Phi_A(2/3).\n'
              '# (b) REF-P6-0 geometry (13,21,9,17) m = (1.3,2.1,0.9,1.7): U = start A_2A_3, A_4 on A_3, A_1 on the\n'
              '# UNION A_2A_3 (two corners: displaced mass at x_0 and p_4); Ud = A_1 on the WHOLE block A_2A_3A_4\n'
              '# (degenerate step = global Moebius map: ONE displaced corner, an exact single-corner prediction);\n'
              '# 3LR = control with A_B = A_2 (both corners at p_3, masses add).  Predictions: general rule (Thm\n'
              '# 5.2, corner_measure) vs the naive (H) rule (mass sigma_1 at p_3), each through the single-corner law\n'
              '# 2 Phi_A(zeta) per corner; for U the two-corner cross term (W2, Ghat unknown) is NOT included.\n')
    t = _chains('sw')
    ms = sorted(m for m in t if 'SW' in t[m] and 'S2' in t[m])
    if ms:
        pa, fl = phi_A(2.0 / 3)
        out.write('\n(a) Ex. 5.6: %s\n' % ', '.join('n=%d SW-S2=%.1e' % (t[m]['n'], t[m]['SW'][0] - t[m]['S2'][0])
                                                 for m in ms))
        e, sp = _fitline(out, 'SW/(2 Phi_A(2/3)) [%s]' % fl, [t[m]['n'] for m in ms],
                         [t[m]['SW'][0] / (2 * pa) for m in ms])
        if e is not None:
            out.write('    with the quadratic interpolation Phi_Aq(2/3) = %.6e: -> %.6f +- %.1e\n' % (
                phi_Aq(2.0 / 3), e * pa / phi_Aq(2.0 / 3), sp * pa / phi_Aq(2.0 / 3)))
    t = _chains('ref')
    ms = sorted(m for m in t if all(k in t[m] for k in ('U', 'Ud', '3LR')))
    if not ms:
        out.write('\n(b): PENDING (no data)\n')
        return
    base = CHAIN_SETS['ref'][0]
    T = float(sum(base))
    p3 = float(base[0] + base[1])
    sig1 = 2.0 * base[3] / (base[2] * (base[2] + base[3]))
    znaive = sig1 * p3 * (T - p3) / T
    cU, cUd, cC = corner_measure(base, 'U'), corner_measure(base, 'Ud'), corner_measure(base, '3LR')
    out.write('\n(b) corners (x/T, kappa T, zeta): U %s; Ud %s; 3LR %s; naive zeta at p_3 = %.6f\n' % (
        [(round(x / T, 6), round(k * T, 6), round(z, 6)) for x, k, z, _ in cU],
        [(round(x / T, 6), round(k * T, 6), round(z, 6)) for x, k, z, _ in cUd],
        [(round(x / T, 6), round(k * T, 6), round(z, 6)) for x, k, z, _ in cC], znaive))
    preds = {'U': (2 * sum(phi_A(c[2])[0] for c in cU), 2 * (phi_A(znaive)[0] + phi_A(cU[-1][2])[0])),
             'Ud': (2 * phi_A(cUd[0][2])[0], 2 * phi_A(znaive)[0]), '3LR': (2 * phi_A(cC[0][2])[0], None)}
    pq = {'U': 2 * sum(phi_Aq(c[2]) for c in cU), 'Ud': 2 * phi_Aq(cUd[0][2]), '3LR': 2 * phi_Aq(cC[0][2])}
    out.write('  Phi_A flags: %s\n' % {round(z, 4): phi_A(z)[1] for z in [c[2] for c in cU + cUd + cC] + [znaive]})
    out.write('  3-node stencil spread of the quadratic interpolation: %s; the large-zeta table itself is uncertain by\n'
              '  0.45%% (zeta = 1.07) and 0.46%% (2.13) (numerics/results_largezeta_certified.txt sec. 4)\n'
              % ', '.join('%.4f: %.2f%%' % (z, 100 * phi_Aq_spread(z)) for z in [c[2] for c in cU + cUd + cC] + [znaive]))
    ns = [t[m]['n'] for m in ms]
    for pr in ('Ud', 'U', '3LR'):
        g, nv = preds[pr]
        out.write('  %s: lattice %s; prediction general rule %.6e (quadratic interp. %.6e)%s\n' % (
            pr, ' '.join('%.9e' % t[m][pr][0] for m in ms), g, pq[pr], (', naive (H) rule %.6e' % nv) if nv else ''))
        e, sp = _fitline(out, '%s lattice/general' % pr, ns, [t[m][pr][0] / g for m in ms])
        if e is not None:
            out.write('    with the quadratic interpolation: lattice/general -> %.6f +- %.1e\n' % (e * g / pq[pr],
                                                                                              sp * g / pq[pr]))
        if nv:
            _fitline(out, '%s lattice/naive' % pr, ns, [t[m][pr][0] / nv for m in ms])
    yx = [c[3] for c in cU]
    out.write('  U: modular separation of its two corners Delta = %.6f (naive: %.6f); the missing cross term of U\n'
              '  is the excess over the no-cross-term single-corner sum (W2: 2 f2 zeta_a zeta_b Ghat(Delta)/Ghat(0) per\n'
              '  chirality at second order; zeta_a = %.3f is not small).\n' % (yx[1] - yx[0], yx[1] - math.log(
                  p3 / (T - p3)), cU[0][2]))


def N6(out):
    out.write('# N6 (a): VWZ CMI bounds, VWZ symmetric setup, lattice vacuum CMIs.  (5.3): max_lam F^(1) >= e^{-b1},\n'
              '# b1 = I(A:CD|B)/2; (5.4)/(5.5): max_lam F^(2),(3) >= e^{-b23}, b23 = (I(A:C|B)+I(B:D|C)+I(A:D|BC))/2;\n'
              '# (5.11): b23 = -(c/6) log((1-eta)/(1+eta)), c = 1.  Since -log max_lam F <= -log F^(lam=0), a ratio\n'
              '# Phi^(i)/b < 1 verifies the bound a fortiori.  Chain rule check: I(B:D|C) + I(A:D|BC) = I(AB:D|C).\n')
    out.write('%5s %3s %4s %12s %12s %12s %12s %9s %9s %9s %9s\n' % ('set', 'm', 'n', 'b1', 'b23', 'b23(5.11)',
              'b1_cont', 'Phi1/b1', 'Phi2/b23', 'Phi3/b23', 'chainrule'))
    for key in ESETS:
        t = _table(key)
        for m in sorted(t):
            r = t[m]
            if 'cmi' not in r or '3LR' not in r:
                continue
            c = r['cmi']
            eta = r['a'] / (r['a'] + 2.0 * r['b'])
            b1, b23 = c['IA_CD_B'] / 2, (c['IA_C_B'] + c['IB_D_C'] + c['IA_D_BC']) / 2
            out.write('%5s %3d %4d %12.6e %12.6e %12.6e %12.6e %9.5f %9.5f %9.5f %9.1e\n' % (
                key, m, r['n'], b1, b23, -math.log((1 - eta) / (1 + eta)) / 6, math.log(1 / (1 - eta)) / 6,
                r['1A'][0] / b1, r['2'][0] / b23, r['3LR'][0] / b23, c['IB_D_C'] + c['IA_D_BC'] - c['IAB_D_C']))
    out.write('\n# N6 (b): L->R chains: sum_k I_k, I_k = I(A_1..A_{k-1} : A_{k+1} | A_k) (lattice vacuum), the\n'
              '# continuum (1/3) log 1/(1-eta_k), and Phi_tot/(sum_k I_k / 2).\n'
              '# N6 (c): equal-block chains l = (1,...,1) m, n_blocks = 2..6 (n_blocks = 2: no step, Phi_tot = 0 exactly);\n'
              '# zeta_k^(I) = (k-1)(n-k+1)/n; SA = 2 sum_k Phi_A(zeta_k) (no cross terms).\n')
    out.write('\neq2 (n_blocks = 2): the L->R chain has no step (the starting block A_1A_2 is the whole chain), so\n'
              '  the recovered state is the vacuum and Phi_tot = D_tot = 0 exactly at every size.\n')
    for key in ('eq3', 'eq4', 'eq5', 'eq6', 'n4r2', 'n5r2', 'n6r2', 'n4r3', 'n5r3'):
        t = _chains(key)
        base = CHAIN_SETS[key][0]
        ms = sorted(m for m in t if 'LR' in t[m] and len(t[m]['steps']) == len(base) - 2)
        if not ms:
            out.write('\n%s: PENDING (no data)\n' % key)
            continue
        q = [0.0]
        for l in base:
            q.append(q[-1] + l)
        ec = [q[k - 1] * base[k] / ((q[k - 1] + base[k - 1]) * (base[k - 1] + base[k])) for k in range(2, len(base))]
        Ic = sum(math.log(1 / (1 - e)) / 3 for e in ec)
        zs = [c[1] for c in _lr_data(base)]
        SA = 2 * sum(phi_A(z)[0] for z in zs)
        SAq = 2 * sum(phi_Aq(z) for z in zs)
        ys = [c[3] for c in _lr_data(base)]
        out.write('\n%s lengths %s x m: zeta^(I) = %s; Delta_k = %s; continuum sum I_k = %.6f; SA = %.6e [%s]\n' % (
            key, base, ['%.4f' % z for z in zs], ['%.4f' % (ys[i + 1] - ys[i]) for i in range(len(ys) - 1)], Ic, SA,
            sorted({phi_A(z)[1] for z in zs})))
        rows = []
        for m in ms:
            P = t[m]['LR'][0]
            sI = sum(v[2] for v in t[m]['steps'].values())
            rows.append((t[m]['n'], P, sI, P / (sI / 2), P / SA))
            out.write('  m=%2d n=%3d Phi_tot=%.9e D_tot=%.9e sum I_k=%.9f Phi_tot/(sumI/2)=%.5f Phi_tot/SA=%.5f\n'
                      % (m, t[m]['n'], P, t[m]['LR'][1], sI, rows[-1][3], rows[-1][4]))
        if len(ms) >= 2 and key.startswith('eq'):
            e, sp = _fitline(out, 'Phi_tot(n)/Phi_tot(n_max)', [r[0] for r in rows], [r[1] / rows[-1][1] for r in rows])
            if e is not None:
                out.write('  => Phi_tot(n_blocks = %d) extrapolated = %.6e +- %.1e (per chirality %.6e); SA = %.6e, '
                          'SAq (quadratic interp.) = %.6e; Phi_tot_inf/SAq = %.4f\n' % (
                              len(base), e * rows[-1][1], sp * rows[-1][1], e * rows[-1][1] / 2, SA, SAq,
                              e * rows[-1][1] / SAq))
            _fitline(out, 'Phi_tot/SA', [r[0] for r in rows], [r[4] for r in rows])



RAW_CMDS = {   # how every raw file was produced (run from the repository root; PYTHONDONTWRITEBYTECODE=1 $PYTHON ...)
    'vwz_A.raw': 'lattice_chain.py sweep e015', 'vwz_B.raw': 'lattice_chain.py sweep e005,e010',
    'vwz_C.raw': 'lattice_chain.py sweep e020,e030,e040,m010,m020,m030',
    'vwz_G.raw': 'lattice_chain.py sweep m020x,e030x,m010x,m030x',
    'chains_D.raw': 'lattice_chain.py chains sw,eq3,eq4,eq5,eq6,n4r2', 'chains_E.raw': 'lattice_chain.py chains ref',
    'chains_F.raw': 'lattice_chain.py chains n5r2,n4r3,n6r2,n5r3', 'chains_H.raw': 'lattice_chain.py chains eq3x,n4r2x',
    'chains_I.raw': 'lattice_chain.py chains n6r2x',
}


def header(out, task):
    out.write('# %s -- numerics/networks/lattice_chain.py %s (run from the repository root cft_cmi/).\n' % (task, task))
    out.write('# Discretisation: the lattice model itself, computed exactly in Gaussian form (every one-particle mode of\n'
              '# every block kept; no truncation, no taper, flint ball arithmetic at bits_for(n)+200); the lattice\n'
              '# spacing is the only regulator, and its effect is the resolution dependence measured below (no\n'
              '# regulator-free discretisation exists for a lattice model; continuum statements are compared after\n'
              '# extrapolation in n).  Raw data (one line per run, with the normalisation defect nrm):\n')
    for fn, cmd in RAW_CMDS.items():
        out.write('#   numerics/networks/%-13s <- $PYTHON numerics/networks/%s\n' % (fn, cmd))
    out.write('# Fit rules: NFIT = %d finest resolutions, TOL_FIT = %.0e (fixed before the runs); see NETWORK_RESULTS.md.\n'
              % (NFIT, TOL_FIT))


def NRM(out):
    """Largest normalisation defect |log K det(1+T)| over every raw line of numerics/networks/*.raw."""
    import glob
    worst = []
    for fn in sorted(glob.glob(os.path.join(_NET, '*.raw'))):
        for line in open(fn):
            w = line.split()
            d = dict(x.split('=', 1) for x in w[1:] if '=' in x)
            if 'nrm' in d:
                worst.append((float(d['nrm']), os.path.basename(fn), ' '.join(w[1:4]), d.get('prot', d.get('k', ''))))
    worst.sort(reverse=True)
    out.write('# NRM: largest normalisation defects |log K det(1+T)| over all %d raw lines (bits_for(n)+200)\n'
              % len(worst))
    for v in worst[:5]:
        out.write('  %.1e  %s  %s  prot/k=%s\n' % v)


def PREC(out):
    """Precision check of production sizes: bits_for(n) + 200 (production) against bits_for(n) + 600."""
    out.write('# PREC: -log F and D at the production precision bits_for(n)+200 vs bits_for(n)+600\n')
    for L, pr in (((6, 57, 57, 6), '2'), ((18, 51, 51, 18), '3LR'), ((13, 21, 9, 17), 'U'),
                  ((26, 42, 18, 34), 'U'), ((32, 16, 8, 4, 2, 1), lr_chain(6))):
        r1 = gauss(L, pr, 0.0, extra_bits=200)
        r2 = gauss(L, pr, 0.0, extra_bits=600)
        out.write('PREC L=%s prot=%s n=%d bits=%d/%d -logF=%.15e/%.15e (diff %.1e) D=%.15e/%.15e (diff %.1e) '
                  'nrm=%.1e/%.1e\n' % (L, pr if isinstance(pr, str) else 'LR', sum(L), r1[4].bits, r2[4].bits,
                                        r1[0], r2[0], r1[0] - r2[0], r1[1], r2[1], r1[1] - r2[1], r1[2], r2[2]))
        out.flush()


if __name__ == '__main__':
    task = sys.argv[1] if len(sys.argv) > 1 else ''
    if task == 'V0':
        V0(sys.stdout)
    elif task in ('N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'PREC', 'NRM'):
        if task not in ('PREC', 'NRM'):
            header(sys.stdout, task)
        globals()[task](sys.stdout)
    elif task == 'chains':
        sweep_chain(sys.argv[2].split(','), sys.stdout)
    elif task == 'sweep':
        sweep_vwz(sys.argv[2].split(','), sys.stdout)
    else:
        print('PENDING: task %s not yet written' % task)
