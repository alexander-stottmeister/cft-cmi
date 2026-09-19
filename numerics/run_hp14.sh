#!/bin/bash
# Interpreter: set PYTHON to a python with numpy/scipy/mpmath/python-flint,
# e.g.  PYTHON=~/venvs/cft/bin/python ./run_hp14.sh   (default: python3)

# Track C (O4): exact windowed evaluation at eps=1e-14 (kappa_c = 32.2) with Q in 40-digit arithmetic; then eps=1e-11 for the same files.
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
for f in Dhat_exact_s0.2_Lam60_k30_g12.npz Dhat_exact_s0.025_Lam60_k30_g12.npz Dhat_exact_s0.05_Lam60_k30_g12.npz Dhat_exact_s0.1_Lam60_k30_g12.npz Dhat_exact_s0.4_Lam60_k30_g12.npz; do
  $PY fidelity_hp.py $f 1e-14 40 2>/dev/null
done
for f in Dhat_exact_s0.2_Lam120_k45_g12.npz Dhat_exact_s0.025_Lam120_k45_g12.npz; do
  $PY fidelity_hp.py $f 1e-14 40 2>/dev/null
done
