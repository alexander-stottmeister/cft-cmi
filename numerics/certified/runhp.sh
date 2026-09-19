#!/bin/zsh
PY=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team/2a3c5aab-2bd9-408c-811f-f4144c2149e4/scratchpad/venv/bin/python
for e in 1e-11 1e-08; do
for s in 0.025 0.05 0.1 0.2 0.4 0.8 1.6; do
  $PY cert_tail_hp.py ../Dhat_exact_s${s}_Lam60_k30_g12.npz qball_Lam60_k30.pkl $e 60
done; done
