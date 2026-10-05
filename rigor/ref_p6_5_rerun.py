#!/usr/bin/env python3
"""ref_p6_5_rerun.py -- REF-P6-5: reruns of G3's numerics/networks/corner_kernel.py with ALL output redirected.

The reviewed script writes through its class Out into numerics/networks/<name> and np.savez into the same directory.
This wrapper imports it as a module and replaces (i) corner_kernel.Out by a writer into rigor/ref_p6_5_rerun_<job>.out and
(ii) numpy.savez by a writer into rigor/ref_p6_5_rerun_<job>_<basename>.npz, so no file under numerics/networks/ is touched.
Usage: $PYTHON rigor/ref_p6_5_rerun.py JOB, JOB in K0 (G3's K0), K1r (one K1 rung, h = 1/16, Y = 14, Ymax = 20, all Delta),
       K2r (G3's K2 restricted to the box (120,45)), K4v (G3's K4v), K1fit, K3 (G3's post-processing). Compare with numerics/networks/kernel_*.out by
       rigor/ref_p6_5_diff.py. Threads: OPENBLAS/OMP/MKL_NUM_THREADS = 2 (set before numpy is imported).
"""
import os, sys, time
for _v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '2'                                  # at most 2 cores (brief REF-P6-5 sec. 7)
sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))        # rigor/
_ROOT = os.path.abspath(os.path.join(_HERE, '..'))         # cft_cmi/
sys.path.insert(0, os.path.join(_ROOT, 'numerics', 'networks'))
import numpy as np
import corner_kernel as ck

JOB = sys.argv[1] if len(sys.argv) > 1 else 'K0'
_savez = np.savez
def _redirect_savez(path, *a, **k):
    tgt = os.path.join(_HERE, f'ref_p6_5_rerun_{JOB}_' + os.path.basename(str(path)))
    return _savez(tgt, *a, **k)
np.savez = _redirect_savez

class RefOut:
    """Same interface as corner_kernel.Out, but writes rigor/ref_p6_5_rerun_<JOB>.out (one file per job)."""
    _f = None
    def __init__(self, name, header):
        if RefOut._f is None:
            RefOut._f = open(os.path.join(_HERE, f'ref_p6_5_rerun_{JOB}.out'), 'w')
        self.f = RefOut._f
        self(f'# [{name} as written by corner_kernel.py, redirected by rigor/ref_p6_5_rerun.py {JOB}] '
             f'{time.strftime("%Y-%m-%d %H:%M")}')
        for l in header.strip().splitlines():
            self('# ' + l.strip())
    def __call__(self, *a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); self.f.write(s + '\n'); self.f.flush()
ck.Out = RefOut

if JOB == 'K0':
    ck.k0()
elif JOB == 'K1r':
    o = RefOut('kernel_t0.out (one rung)', 'K1 rung h = 1/16 of the dyadic ladder [A]: Y = 14, Ymax = 20, all Delta of DGRID')
    o('[A] dyadic ladder, Y = 14, Ymax = 20, all Delta (rung h = 0.0625 only)')
    ck.t0_ladder(o, (0.0625,), 14.0, 20.0, ck.DGRID)
elif JOB == 'K2r':
    ck.k2(boxes=((120, 45),))
elif JOB == 'K4v':
    ck.k4v()
elif JOB == 'K1fit':                                   # second pass: post-processing, reads G3's npz, writes only here
    ck.k1fit()
elif JOB == 'K3':
    ck.k3()
else:
    raise SystemExit(f'unknown job {JOB}')
