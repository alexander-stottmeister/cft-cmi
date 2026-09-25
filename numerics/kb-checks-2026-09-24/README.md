# numerics/kb-checks-2026-09-24/: the corrected tail constant A_3 (rigor/tail_bound.tex, Correction C10)

The referee REF-DOC-TAIL found that the value A_3 <= 0.036 of `rigor/tail_bound.tex` (thm:tau, §9(3)) does not follow
from its computation. That computation is `rigor/pt_tailconst.py`: A_3 is a supremum over 0 < zeta <= 1, the sampled
values decrease in zeta, and so the supremum is the limit zeta -> 0, which was never sampled. The fix author FIX-TAIL
checked this independently. The two scripts here are that check and the corrected tail check. Both were written on
2026-09-24; the scripts and outputs in numerics/kb-checks-2026-09-23/ are unchanged.

| script | checks | needs | runtime |
|---|---|---|---|
| `a3_refined.py` | zeta^-2 of the L1 norm of (g2)''' with the original functions of `rigor/pt_tailconst.py` at more zeta (0.03642 as zeta -> 0 on the script's grid); the zeta -> 0 limit in closed form on refined grids (0.03718 for t = 0.002..80, 0.03721 including t near 0); finite zeta on a refined grid, all below the limit. Result: A_3 = 0.0372, so A_3 <= 0.0374 and C_2 = 4 pi A_3 <= 0.47 (was 0.036 and 0.46). Not certified. | mpmath | about 4 min |
| `refb10_tail_sup_c2.py` | copy of `../kb-checks-2026-09-23/refb10_tail_sup.py` with 10 C_2 = 4.7 in place of 4.6 in T, plus a scan of the admissible grid of `tailcheck_ext.py` (kappa_c up to 200). The corrected chain of thm:main against eq:final has its supremum at the corner (11 e^-3.5, 10): 0.98405 (f = 0.0085) and 0.98467 (f = 0.008516); T kappa_c^2/zeta^2 = 1.7071 there. | standard library | about 20 s |

Run them from the repository root, `python3 numerics/kb-checks-2026-09-24/NAME.py`, and compare the printout with
`NAME.out`. The .out files here were produced with Python 3.9.6: the standard-library `/usr/bin/python3` for
`refb10_tail_sup_c2.py`, and a virtual environment with mpmath 1.4.1 for `a3_refined.py`.

The scripts in `../kb-checks-2026-09-23/` hard-code 4.6 (C_2 <= 0.46). Their ratios are for that constant.
