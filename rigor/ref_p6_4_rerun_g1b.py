#!/usr/bin/env python3
"""ref_p6_4_rerun_g1b.py -- referee REF-P6-4: rerun rigor/g1b_kernel.py UNCHANGED, but without letting it
overwrite the reviewed output file rigor/g1b_kernel.out (the script writes that file itself, l. 206).

Reproduce (repository root):
  ${PYTHON:-python3} rigor/ref_p6_4_rerun_g1b.py > rigor/ref_p6_4_g1b_kernel_rerun.out
then: diff rigor/g1b_kernel.out rigor/ref_p6_4_g1b_kernel_rerun_selfwrite.out
Every write-open of rigor/g1b_kernel.out is redirected to rigor/ref_p6_4_g1b_kernel_rerun_selfwrite.out;
nothing else in g1b_kernel.py is changed (it is executed from its own file by runpy)."""
import os, sys, runpy, builtins
_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TARGET = os.path.join(_ROOT, 'rigor', 'g1b_kernel.out')
REDIRECT = os.path.join(_ROOT, 'rigor', 'ref_p6_4_g1b_kernel_rerun_selfwrite.out')
_real_open = builtins.open
def _guarded_open(f, mode='r', *a, **k):
    if isinstance(f, (str, bytes, os.PathLike)) and os.path.abspath(os.fsdecode(f)) == TARGET \
            and any(c in mode for c in 'wax+'):
        f = REDIRECT
    return _real_open(f, mode, *a, **k)
builtins.open = _guarded_open
runpy.run_path(os.path.join(_ROOT, 'rigor', 'g1b_kernel.py'), run_name='__main__')
