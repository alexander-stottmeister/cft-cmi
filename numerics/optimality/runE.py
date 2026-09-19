from run_exact import study
import sys
fam = {'A2': [(8, 16, 4)], 'D2': [(6, 12, 3), (4, 16, 2)], 'E': [(6, 16, 3), (5, 10, 2)]}[sys.argv[1]]
for g in fam:
    study(*g, caps=(6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0))
