"""Driver: minimise the second-order (QFI) recovery error over gauge-invariant
quasi-free channels and compare with the Petz map, on the hopping chain."""
import sys, time
import numpy as np
from opt_gaussian import corr_sine, Problem, qfi_form, solve
from petz_ref import petz_symbol, neglogF


def assemble(P, X, Z):
    n, LA = P.n, P.LA
    Qr = np.zeros((n, n), dtype=complex)
    Qr[:LA, :LA] = P.QAA
    M = P.QAB @ X.conj().T
    Qr[:LA, LA:] = M
    Qr[LA:, :LA] = M.conj().T
    Qr[LA:, LA:] = Z
    return 0.5 * (Qr + Qr.conj().T)


def zval(LA, LB, LC):
    return LA * LC / (LB * (LA + LB + LC))


def run(LA, LB, LC, kappa_c, exact=True, verbose=False):
    t0 = time.time()
    n = LA + LB + LC
    Q = corr_sine(n)
    Qp = petz_symbol(Q, LA, LB, LC)
    P = Problem(LA, LB, LC, kappa_c=kappa_c)
    Ep = qfi_form(Q - Qp, P.U, P.w)[0]
    X, Z, Eo = solve(P, verbose=verbose)
    Qr = assemble(P, X, Z)
    out = dict(LA=LA, LB=LB, LC=LC, z=zval(LA, LB, LC), kc=kappa_c,
               E_petz=Ep, E_opt=Eo, ratio=Eo / Ep, t=time.time() - t0,
               minev=min(np.linalg.eigvalsh(Qr).min(), 0.0),
               X=X, Z=Z, Qr=Qr, Qp=Qp, Q=Q)
    if exact:
        out['F_petz'] = float(neglogF(Q, Qp))
        out['F_opt'] = float(neglogF(Q, np.real(Qr)))
    return out


if __name__ == '__main__':
    job = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    if job == 'scan':
        cases = [((4, 6, 3), 10.0), ((4, 8, 3), 10.0), ((4, 12, 3), 10.0),
                 ((3, 6, 3), 10.0), ((3, 9, 3), 10.0), ((3, 12, 3), 10.0),
                 ((4, 6, 3), 8.0), ((4, 6, 3), 12.0), ((4, 6, 3), 14.0),
                 ((3, 9, 3), 8.0), ((3, 9, 3), 12.0),
                 ((2, 6, 2), 10.0), ((2, 10, 2), 10.0), ((5, 10, 4), 10.0),
                 ((4, 16, 3), 10.0)]
    else:
        cases = [((4, 20, 3), 10.0), ((6, 12, 4), 10.0), ((4, 12, 3), 12.0)]
    for g, kc in cases:
        r = run(*g, kappa_c=kc)
        print('LA,LB,LC=%-11s z=%.5f kc=%4.1f | E_petz=%.6e E_opt=%.6e ratio=%.4f'
              % (str(g), r['z'], kc, r['E_petz'], r['E_opt'], r['ratio']), flush=True)
        print('    exact -logF: Petz=%.6e opt=%.6e ratio=%.4f | E_petz/z^2=%.5f E_opt/z^2=%.5f | minev=%.1e %.0fs'
              % (r['F_petz'], r['F_opt'], r['F_opt'] / r['F_petz'],
                 r['E_petz'] / r['z']**2, r['E_opt'] / r['z']**2, r['minev'], r['t']), flush=True)
        np.savez('sol_%d_%d_%d_kc%g.npz' % (g[0], g[1], g[2], kc),
                 X=r['X'], Z=r['Z'], Qr=r['Qr'], Qp=r['Qp'], Q=r['Q'])
