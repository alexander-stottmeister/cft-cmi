#!/bin/bash
# Interpreter: set PYTHON to a python with numpy/scipy/mpmath/python-flint,
# e.g.  PYTHON=~/venvs/cft/bin/python ./run_largezeta.sh   (default: python3)

# Large-zeta continuum values of Phi (Note 6 P3 / lattice comparison): s = 3.2 ... 51.2 at Lambda=60, kappa_max=30, eps=1e-8.
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
for s in 3.2 6.4 12.8 25.6 51.2; do
  [ -f Dhat_exact_s${s}_Lam60_k30_g12.npz ] || $PY defect_matrix.py $s 60 30 exact 12 2>&1 | tail -1
done
for s in 3.2 6.4 12.8 25.6 51.2; do
  $PY fidelity_flint.py "Dhat_exact_s${s}_Lam60_k30_g12.npz" 1e-8 2>/dev/null
done
