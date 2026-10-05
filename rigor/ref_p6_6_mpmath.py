#!/usr/bin/env python3
"""rigor/ref_p6_6_mpmath.py -- REF-P6-6 (2026-10-05): independent check of two-step VWZ protocols through the
mpmath path of numerics/lattice/petz_lattice.py (corr_infinite, block, gspec, embed_pow, hermitize, fid_relent;
mpmath eigsy/eighe, no flint, no code of lattice_chain.py), composed here step by step:
T <- X_s T X_s^dag, X_s = T_M^a T_B^-a (identity off M), T = 1 on sites not yet adjoined; a = (1 - i lam)/2
(VWZ (5.1)); log K <- log K - logdet(1+T_M) + logdet(1+T_B).  Compared with G2's flint values in
numerics/networks/vwz_C.raw (set e020, m = 3, n = 18 and m = 2, n = 12), tolerance 1e-10 (fixed in the brief).
Run (repository root): PYTHONDONTWRITEBYTECODE=1 $PYTHON rigor/ref_p6_6_mpmath.py > rigor/ref_p6_6_mpmath.out"""
import os, sys
_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(_ROOT, 'numerics', 'lattice'))
import mpmath as mp
import petz_lattice as PL

TOL = 1e-10
# VWZ Sec. 5 (refs/VWZ_2307.14434.pdf pp. 43-44), blocks A,B,C,D = 1..4; (start block, [(new, cond. block)])
PROTS = {'1B': ((1, 2), [((3, 3), (2, 2)), ((4, 4), (2, 3))]),   # P_{B->BC} then P_{BC->BCD}
         '2': ((1, 2), [((3, 3), (2, 2)), ((4, 4), (3, 3))]),    # P_{B->BC} then P_{C->CD}
         '3LR': ((2, 3), [((1, 1), (2, 2)), ((4, 4), (3, 3))])}  # start BC: P_{B->AB} then P_{C->CD}

def run(lengths, prot, lam=0):
    p = [0]
    for l in lengths: p.append(p[-1] + l)
    n = p[-1]
    C = PL.corr_infinite(n)
    a = (1 - 1j * mp.mpf(lam)) / 2
    (s0, s1), steps = PROTS[prot]
    lo, hi = p[s0 - 1], p[s1]
    V, t = PL.gspec(PL.block(C, lo, hi))
    T = PL.embed_pow(V, t, mp.mpf(1), n, lo)
    logK = -mp.fsum([mp.log(1 + x) for x in t])
    for (k1, k2), (b1, b2) in steps:
        nlo, nhi, blo, bhi = p[k1 - 1], p[k2], p[b1 - 1], p[b2]
        mlo, mhi = min(blo, nlo), max(bhi, nhi)
        VM, tM = PL.gspec(PL.block(C, mlo, mhi)); VB, tB = PL.gspec(PL.block(C, blo, bhi))
        Xs = PL.embed_pow(VM, tM, a, n, mlo) * PL.embed_pow(VB, tB, -a, n, blo)
        T = PL.hermitize(Xs * T * Xs.H)
        logK += -mp.fsum([mp.log(1 + x) for x in tM]) + mp.fsum([mp.log(1 + x) for x in tB])
    nrm = logK + mp.log(mp.re(mp.det(mp.eye(n) + T)))
    mF, D = PL.fid_relent(C, T)
    return mF, D, nrm

def g2(n, prot):
    for line in open(os.path.join(_ROOT, 'numerics', 'networks', 'vwz_C.raw')):
        d = dict(x.split('=', 1) for x in line.split()[1:])
        if line.startswith('DATA') and d['set'] == 'e020' and int(d['n']) == n and d['prot'] == prot:
            return float(d['mlogF']), float(d['D'])

if __name__ == '__main__':
    print('# REF-P6-6 mpmath path vs G2 flint (vwz_C.raw), tolerance %.0e on -log F and on D' % TOL)
    ok = True
    for L in ((2, 4, 4, 2), (3, 6, 6, 3)):
        for prot in ('1B', '2', '3LR'):
            res = {}
            for dps in (90, 130):
                mp.mp.dps = dps
                res[dps] = run(L, prot)
            (mF, D, nrm), (mF2, D2, _) = res[90], res[130]
            gF, gD = g2(sum(L), prot)
            good = abs(float(mF) - gF) <= TOL and abs(float(D) - gD) <= TOL
            ok &= good
            print('L=%s prot=%s n=%d mpmath(130 dps) -logF=%s D=%s | dps 90 vs 130: %.1e %.1e | nrm=%.1e | '
                  'G2 flint -logF=%.15e D=%.15e | diff %.1e %.1e %s' % (
                      L, prot, sum(L), mp.nstr(mF2, 20), mp.nstr(D2, 20), float(abs(mF - mF2)), float(abs(D - D2)),
                      float(abs(nrm)), gF, gD, float(mF2) - gF, float(D2) - gD, 'PASS' if good else 'FAIL'))
    print('# single step 1A = P_{B->BCD}(rho_AB) through petz_lattice.recovered_G (nA=a, nB=b, nC=b+a) + fid_relent')
    for L in ((2, 4, 4, 2), (3, 6, 6, 3)):
        mp.mp.dps = 130
        n = sum(L)
        T, logK = PL.recovered_G(L[0], L[1], L[2] + L[3], PL.corr_infinite(n), 0)
        mF, D = PL.fid_relent(PL.corr_infinite(n), T)
        gF, gD = g2(n, '1A')
        good = abs(float(mF) - gF) <= TOL and abs(float(D) - gD) <= TOL
        ok &= good
        print('L=%s prot=1A n=%d recovered_G: -logF=%s D=%s nrm=%.1e | G2 %.15e %.15e | diff %.1e %.1e %s' % (
            L, n, mp.nstr(mF, 20), mp.nstr(D, 20), float(abs(logK + mp.log(mp.re(mp.det(mp.eye(n) + T))))),
            gF, gD, float(mF) - gF, float(D) - gD, 'PASS' if good else 'FAIL'))
    print('RESULT: %s' % ('ALL PASS' if ok else 'FAILURES'))
