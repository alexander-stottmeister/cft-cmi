"""theta_three_fits.py -- the three convergence fits of AGENTS.md Sec. 5 for theta = 0.384 +- 0.003
(numerics/optimality_all/F3_RESULTS.md Sec. 4), from the SAVED rung data only (no new sweep).
Repair round 2026-11-19, seat R3 (finding C4 F2(c): only an h^p closure was tried).

Run from anywhere:  ${PYTHON:-python3} numerics/optimality_all/theta_three_fits.py \
                       > numerics/optimality_all/theta_three_fits.out

Quantity: theta_h = the finite-mesh value printed as 'theta=' in the F3 output files (sup over a finite
cell class of cos^2(u, v_G), F3 Sec. 0-4).  No proved direction relates theta_h to the continuum theta
(C4 report Sec. 4 F2(a)); every number below is an extrapolation, not a bound.
Resolution: the mesh width h (T0 and Galerkin frames) or 1/L (family D, circle mesh), the only knob
(F3 Sec. 1(b)); the modular window (Y, Ymax, Lambda) is held fixed per family and is cut off; its
weight is F3's y_max law theta(Ymax) = theta_inf - c(h)/Ymax (|c/Ymax| <= 3.2e-3 at Ymax = 10, see the
'ycorr' column), applied exactly as in f3_close.py; fits are reported both raw and y_max-corrected.

Families (files of numerics/optimality_all/):
  A  T0 uniform, Y=Ymax=10           f3_t0_hladder.out, f3_t0_hladder2.out
  B  T0 uniform, Y=6, Ymax=20        f3_t0_final.out
  C  Galerkin a=1,L=2, Lam=12, uni=1 f3_gal_uni.out
  C' Galerkin a=1,L=2, Lam=8,  uni=1 f3_gal_lam.out, f3_gal_ladder8.out
  D  circle mesh (mimic), a=2, Lg=1  f3_mimic.out, f3_mimic_big.out   (variable h := 1/L)
y_max law from f3_t0_ymax.out, f3_t0_ymax2.out (rows with Ymax >= 10; the Y=6 row where both exist).

Models (variable h; extrapolation only in h):
  M1 '1/L' : theta = t + a h
  M2 'logL': theta = t + b log(1/h)        (no finite h -> 0 limit; t is NOT a limit)
  M3 'h^p' : theta = t + a h^p, p free (variable projection: grid in p, then bounded refinement)
Fit window: the finest NFIT = 5 rungs of each family (all rungs if fewer).
TOLERANCES, fixed before the run: F3 fixes no tolerance (F3_RESULTS.md contains none), so this script
fixes TOL = 1e-4 (primary; 20x the 5e-6 print rounding of theta, 30x below the quoted +-3e-3) and
reports TOL2 = 1e-3 as a looser secondary.  A fit is ADMISSIBLE iff max |residual| over the three finest
rungs <= TOL.  Uncertainty = spread of t over admissible M1/M3 fits (AGENTS.md Sec. 5).
Validation (exactly known case): synthetic theta = 0.4 - 0.2 h^0.77 and theta = 0.4 - 0.1 h on family
A's h grid must be recovered by M3 resp. M1 with |t - 0.4| <= 1e-8.
"""
import os, re, sys
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "numerics", "optimality_all")
TOL, TOL2, NFIT = 1e-4, 1e-3, 5
num = lambda key, s: float(re.search(key + r"=([-0-9.]+)", s).group(1))


def rows(files, pred):
    out = {}
    for f in files:
        for s in open(os.path.join(D, f)):
            if "theta=" in s and pred(s):
                out[s.split()[0] + repr(sorted((k, v) for k, v in re.findall(r"(\w+)=([-0-9.]+)", s)
                                               if k not in ("cg",)))] = s   # duplicate runs counted once
    return list(out.values())


def fam_T0(files, Y, Ym):
    r = rows(files, lambda s: s.startswith("T0") and num("Y", s) == Y and num("Ymax", s) == Ym)
    return sorted(((num("h", s), num("theta", s)) for s in r), reverse=True)


def fam_gal(files, lam):
    r = rows(files, lambda s: s.startswith("first") and num("Lam", s) == lam and "uni=1" in s)
    return sorted(((num("h", s), num("theta", s)) for s in r), reverse=True)


def fam_mimic():
    r = rows(["f3_mimic.out", "f3_mimic_big.out"], lambda s: s.startswith("MIMIC") and num("a", s) == 2.0
             and num("Lg", s) == 1.0 and num("capR", s) == 1.0 and num("extra", s) == 0)
    return sorted(((1.0 / num("L", s), num("theta", s)) for s in r), reverse=True)


def ymax_law():
    """c(h) of theta(Ymax) = t - c/Ymax at h = 0.12, 0.06 (Y=6 row preferred), c(h) = c06 (h/0.06)^pc."""
    r = rows(["f3_t0_ymax.out", "f3_t0_ymax2.out", "f3_t0_final.out"],
             lambda s: s.startswith("T0") and num("Ymax", s) >= 10 and num("h", s) in (0.12, 0.06))
    tab = {}
    for s in r:
        k = (num("h", s), num("Ymax", s))
        if k not in tab or num("Y", s) == 6:
            tab[k] = num("theta", s)
    c = {}
    for h in (0.12, 0.06):
        Y = np.array(sorted(y for (hh, y) in tab if hh == h)); T = np.array([tab[(h, y)] for y in Y])
        A = np.vstack([np.ones_like(Y), -1 / Y]).T
        sol = np.linalg.lstsq(A, T, rcond=None)[0]; c[h] = sol[1]
        print(f"#   y_max law h={h}: Ymax={Y.astype(int).tolist()} t={sol[0]:.5f} c={sol[1]:.4f} "
              f"max|resid|={np.abs(A @ sol - T).max():.1e}")
    pc = np.log(c[0.12] / c[0.06]) / np.log(2.0)
    print(f"#   c(h) = {c[0.06]:.4f} (h/0.06)^{pc:.3f}")
    return lambda h: c[0.06] * (np.asarray(h) / 0.06) ** pc


def fit(model, h, t):
    """least squares; returns (t_inf, extra parameters, residuals)."""
    if model == "1/L":
        A = np.vstack([np.ones_like(h), h]).T
    elif model == "logL":
        A = np.vstack([np.ones_like(h), np.log(1 / h)]).T
    else:
        def sse(p):
            A = np.vstack([np.ones_like(h), h ** p]).T
            return np.sum((A @ np.linalg.lstsq(A, t, rcond=None)[0] - t) ** 2)
        ps = np.linspace(0.05, 4.0, 791); k = int(np.argmin([sse(p) for p in ps]))
        p = minimize_scalar(sse, bounds=(ps[max(k - 1, 0)], ps[min(k + 1, len(ps) - 1)]), method="bounded",
                            options={"xatol": 1e-12}).x
        A = np.vstack([np.ones_like(h), h ** p]).T
        sol = np.linalg.lstsq(A, t, rcond=None)[0]
        return sol[0], (sol[1], p), A @ sol - t
    sol = np.linalg.lstsq(A, t, rcond=None)[0]
    return sol[0], (sol[1],), A @ sol - t


def validate(hgrid):
    print("# VALIDATION (exact synthetic cases on family A's h grid, tolerance 1e-8)")
    ok = True
    for model, f in (("h^p", lambda h: 0.4 - 0.2 * h ** 0.77), ("1/L", lambda h: 0.4 - 0.1 * h)):
        t0, par, res = fit(model, hgrid, f(hgrid))
        good = abs(t0 - 0.4) <= 1e-8 and np.abs(res).max() <= 1e-8
        ok &= good
        print(f"#   {model:4s}: t_inf={t0:.12f} params={np.round(par, 9).tolist()} "
              f"max|resid|={np.abs(res).max():.1e}  {'PASS' if good else 'FAIL'}")
    t0, par, res = fit("1/L", hgrid, 0.4 - 0.2 * hgrid ** 0.77)
    print(f"#   control: 1/L fit to the h^0.77 data, max|resid| = {np.abs(res).max():.1e} (must exceed TOL)")
    ok &= np.abs(res).max() > TOL
    print(f"# VALIDATION {'PASS' if ok else 'FAIL'}\n")
    return ok


def main():
    fams = {"A  T0 Y=Ymax=10": (fam_T0(["f3_t0_hladder.out", "f3_t0_hladder2.out"], 10, 10), 10.0),
            "B  T0 Y=6 Ymax=20": (fam_T0(["f3_t0_final.out"], 6, 20), 20.0),
            "C  Galerkin Lam=12": (fam_gal(["f3_gal_uni.out"], 12), 15.4),
            "C' Galerkin Lam=8": (fam_gal(["f3_gal_lam.out", "f3_gal_ladder8.out"], 8), 11.4),
            "D  mimic h=1/L": (fam_mimic(), None)}
    print(__doc__.split("Families")[0].strip().replace("\n", "\n# ").join(["# ", "\n"]))
    if not validate(np.array([h for h, _ in fams["A  T0 Y=Ymax=10"][0]])):
        sys.exit("validation failed")
    print("# y_max correction (f3_close.py law, recomputed from the saved y_max scans)")
    cof = ymax_law()
    print("\n# RUNG DATA (h, theta raw, ycorr = +c(h)/Ymax)")
    for name, (d, Ym) in fams.items():
        print(f"#   {name}: " + ", ".join(f"({h:.5g}, {t:.5f}, {0 if Ym is None else cof(h)/Ym:+.5f})"
                                       for h, t in d))
    print(f"\n# FITS: finest NFIT={NFIT} rungs; admissible iff max|resid| over 3 finest <= TOL={TOL:g} "
          f"(TOL2={TOL2:g} in brackets)")
    print(f"# {'family':20s} {'data':5s} {'model':5s} {'t_inf':>9s} {'params':>22s} {'max|res|3':>10s} "
          f"{'adm':>4s} {'adm2':>5s}")
    adm = {"raw": [], "ycorr": []}; adm2 = {"raw": [], "ycorr": []}
    for name, (d, Ym) in fams.items():
        for kind in ("raw", "ycorr"):
            if kind == "ycorr" and Ym is None:
                continue
            h = np.array([a for a, _ in d])[-NFIT:]
            t = np.array([b for _, b in d])[-NFIT:] + (0 if kind == "raw" else cof(h) / Ym)
            for model in ("1/L", "logL", "h^p"):
                t0, par, res = fit(model, h, t)
                r3 = np.abs(res[-3:]).max(); a1, a2 = r3 <= TOL, r3 <= TOL2
                if model != "logL":
                    if a1: adm[kind].append((name, model, t0))
                    if a2: adm2[kind].append((name, model, t0))
                tt = "(none)" if model == "logL" else f"{t0:.5f}"
                print(f"  {name:20s} {kind:5s} {model:5s} {tt:>9s} {str(np.round(par, 4).tolist()):>22s} "
                      f"{r3:10.1e} {'yes' if a1 else 'no':>4s} {'yes' if a2 else 'no':>5s}")
    print("\n# SUMMARY (t_inf of admissible convergent fits; logL has no limit and is reported separately)")
    for lab, A in (("TOL", adm), ("TOL2", adm2)):
        for kind in ("raw", "ycorr"):
            v = [x[2] for x in A[kind]]
            s = (f"min {min(v):.5f} max {max(v):.5f} spread {max(v)-min(v):.5f}" if v else "no admissible fit")
            ins = (all(0.381 <= x <= 0.387 for x in v) if v else False)
            print(f"  {lab:4s} {kind:5s}: n={len(v)} {s}; all inside [0.381, 0.387]: {ins}; "
                  f"{[(n.split()[0], m) for n, m, _ in A[kind]]}")


if __name__ == "__main__":
    main()
