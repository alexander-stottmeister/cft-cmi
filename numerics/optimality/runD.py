import sys
from run_exact import study
for g in [(4, 12, 2), (4, 16, 2), (6, 16, 3)]:
    study(*g, caps=(12.0, 16.0, 20.0, 26.0))
