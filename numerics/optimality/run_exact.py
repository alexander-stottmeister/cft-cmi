"""Scan: capped-QFI convex optimisation -> candidate Gaussian channel ->
EXACT high-precision -log F as the arbiter.  The channel is a certificate:
however it was found, its exact recovery error is compared with the Petz map's."""
import sys, time
import numpy as np
from opt_gaussian import corr_sine, Problem, qfi_form, solve
from petz_ref import petz_symbol, neglogF
from run_opt import assemble, zval

CAPS = (3.0, 5.0, 8.0, 12.0)


def study(LA, LB, LC, caps=CAPS, dps=90):
    n = LA + LB + LC
    Q = corr_sine(n)
    Qp = petz_symbol(Q, LA, LB, LC, dps=dps)
    Fp = float(neglogF(Q, Qp, dps=dps))
    z = zval(LA, LB, LC)
    best = (np.inf, None, None, None)
    X0 = Z0 = None
    for kc in caps:
        t0 = time.time()
        P = Problem(LA, LB, LC, kappa_c=kc)
        X, Z, E = solve(P, X0=X0, Z0=Z0)
        X0, Z0 = X, Z
        Qr = np.real(assemble(P, X, Z))
        Fo = float(neglogF(Q, Qr, dps=dps))
        print('  (%d,%d,%d) z=%.5f cap=%4.1f  capQFI=%.6e  exact=%.8e  r=%.4f  %.0fs'
              % (LA, LB, LC, z, kc, E, Fo, Fo / Fp, time.time() - t0), flush=True)
        if Fo < best[0]:
            best = (Fo, kc, X.copy(), Z.copy())
    print('  (%d,%d,%d) n=%d z=%.5f | Petz=%.8e (Petz/z^2=%.5f) | BEST=%.8e cap=%.1f'
          '  ratio=%.4f  opt/z^2=%.5f' % (LA, LB, LC, n, z, Fp, Fp / z**2, best[0],
                                          best[1], best[0] / Fp, best[0] / z**2), flush=True)
    np.savez('best_%d_%d_%d.npz' % (LA, LB, LC), X=best[2], Z=best[3], Q=Q, Qp=Qp,
             Fp=Fp, Fo=best[0], z=z, cap=best[1])
    return dict(z=z, Fp=Fp, Fo=best[0], ratio=best[0] / Fp)


if __name__ == '__main__':
    which = sys.argv[1]
    fam = {'A': [(4, 8, 2), (6, 12, 3), (8, 16, 4)],
           'B': [(4, 12, 2), (4, 16, 2), (6, 18, 3)],
           'C': [(10, 20, 5), (8, 24, 4)]}[which]
    for g in fam:
        study(*g)
