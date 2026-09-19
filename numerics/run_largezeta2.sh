#!/bin/bash
# Interpreter: set PYTHON to a python with numpy/scipy/mpmath/python-flint,
# e.g.  PYTHON=~/venvs/cft/bin/python ./run_largezeta2.sh   (default: python3)

# Large-zeta systematics: dependence on the window (eps) and on the box (Lambda, kappa_max) for s = 6.4 and 25.6.
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
for s in 6.4 25.6; do
  [ -f Dhat_exact_s${s}_Lam120_k45_g12.npz ] || $PY defect_matrix.py $s 120 45 exact 12 > /dev/null 2>&1
  $PY fidelity_flint.py "Dhat_exact_s${s}_Lam120_k45_g12.npz" 1e-8 2>/dev/null
  $PY fidelity_flint.py "Dhat_exact_s${s}_Lam120_k45_g12.npz" 1e-11 2>/dev/null
  $PY fidelity_hp.py Dhat_exact_s${s}_Lam60_k30_g12.npz 1e-11 40 2>/dev/null
  $PY fidelity_hp.py Dhat_exact_s${s}_Lam60_k30_g12.npz 1e-14 40 2>/dev/null
done
