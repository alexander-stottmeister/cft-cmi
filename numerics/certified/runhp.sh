#!/bin/zsh
# Interpreter: set PYTHON to a python with numpy/scipy/mpmath/python-flint,
# e.g.  PYTHON=~/venvs/cft/bin/python ./runhp.sh   (default: python3)

PY="${PYTHON:-python3}"
for e in 1e-11 1e-08; do
for s in 0.025 0.05 0.1 0.2 0.4 0.8 1.6; do
  $PY cert_tail_hp.py ../Dhat_exact_s${s}_Lam60_k30_g12.npz qball_Lam60_k30.pkl $e 60
done; done
