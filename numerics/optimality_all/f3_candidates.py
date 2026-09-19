"""F3 T4: the closed-form candidate test for theta = 0.384 +- 0.003 (F3_RESULTS.md Sec. 4).
Lists every candidate that was tested, with its value, and prints which lie in the window
[0.381, 0.387], together with the number expected inside by chance for that window width.
Reproduces F3_RESULTS.md Sec. 6.   Run:  $V/bin/python f3_candidates.py > f3_candidates.out"""
import numpy as np
PI, E, L2 = np.pi, np.e, np.log(2.0)
THETA, ERR = 0.384, 0.003
LO, HI = round(THETA-ERR, 3), round(THETA+ERR, 3)

CAND = [
 ("pi^2/8 - 1",        PI**2/8 - 1),
 ("1 - 2/e",           1 - 2/E),
 ("4/pi - 1",          4/PI - 1),
 ("1 - 1/(2 ln 2)",    1 - 1/(2*L2)),
 ("3 - e",             3 - E),
 ("3/pi^2",            3/PI**2),
 ("pi^2/6 - 4/3",      PI**2/6 - 4/3),
 ("(pi^2 - 6)/12",     (PI**2 - 6)/12),
 ("1/3",               1/3),
 ("1/2 - 1/(2 pi)",    0.5 - 1/(2*PI)),
 ("1 - pi/8 - 1/4",    1 - PI/8 - 0.25),
 ("1 - 2/pi",          1 - 2/PI),
 ("1/e",               1/E),
 ("3/8",               0.375),
 ("1 - pi^2/16",       1 - PI**2/16),
 ("2 ln 2 - 1",        2*L2 - 1),
 ("2/pi - 1/4",        2/PI - 0.25),
 ("7/18",              7/18),
 ("pi/8",              PI/8),
 ("(4 - pi)/(pi - 1)", (4 - PI)/(PI - 1)),
 ("pi^2/24",           PI**2/24),
 ("1/(2 ln 2) - 1/4",  1/(2*L2) - 0.25),
 ("(ln 2)^2",          L2**2),
 ("1 - 3/(2 pi)",      1 - 3/(2*PI)),
 ("ln 2/(2 - ln 2)",   L2/(2 - L2)),
 ("2 - 12/pi^2",       2 - 12/PI**2),
]

if __name__ == '__main__':
    v = np.array([x for _, x in CAND]); n = len(CAND)
    inside = [(k, x) for k, x in CAND if LO <= x <= HI]
    print(f"# F3 closed-form candidate test.  theta = {THETA} +- {ERR}  ->  window [{LO}, {HI}]"
          f" (width {HI-LO:.3f})")
    print(f"# {n} candidates tested; values span [{v.min():.4f}, {v.max():.4f}]"
          f" (range {v.max()-v.min():.4f})")
    print(f"# expected inside by chance if uniform over that range:"
          f" {n*(HI-LO)/(v.max()-v.min()):.2f};  found: {len(inside)}")
    print(f"#\n# {'verdict':9s} {'candidate':20s} {'value':>10s}  |value-theta|")
    for k, x in sorted(CAND, key=lambda t: t[1]):
        print(f"  {'INSIDE ' if LO <= x <= HI else 'excluded':9s} {k:20s} {x:10.6f}  {abs(x-THETA):.5f}")
    print(f"#\n# inside the window: " + ", ".join(f"{k} = {x:.6f}" for k, x in inside))
    print("# NO SELECTION IS MADE: with 26 candidates and a window of width "
          f"{HI-LO:.3f}, {len(inside)} hits against an expectation of "
          f"{n*(HI-LO)/(v.max()-v.min()):.2f} is not evidence, and the candidate list is not"
          " uniform (it clusters in 0.25-0.45).  A closed form must come from solving the"
          " Wiener-Hopf problem of exact_optimum_tangent_problem.tex eq:thetaWH, not from fitting.")
