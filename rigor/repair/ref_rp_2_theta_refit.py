"""REF-RP-2 independent refit of theta families A and D (repair round 2026-11-19).
Run: ${PYTHON:-python3} rigor/repair/ref_rp_2_theta_refit.py > rigor/repair/ref_rp_2_theta_refit.out
Own parser of the raw F3 files, own fitting (scipy curve_fit Levenberg-Marquardt for h^p, numpy polyfit
for h and log(1/h)); shares no code with numerics/optimality_all/theta_three_fits.py.
TOLERANCES fixed before this run (by the referee brief): admissible iff max|resid| over the 3 finest
of the finest 5 rungs <= 1e-4 (primary) or 1e-3 (secondary). Agreement with the R3 .out: |dt| <= 1e-5.
Validation: synthetic 0.4 - 0.2 h^0.77 on family A's grid must give |t - 0.4| <= 1e-8 under h^p."""
import os, re, glob
import numpy as np
from scipy.optimize import curve_fit
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = os.path.join(R, "numerics", "optimality_all")
def kv(line): return dict(re.findall(r"(\w+)=([-0-9.]+)", line))
def load(files, tag, cond):
    seen = {}
    for f in files:
        for line in open(os.path.join(N, f)):
            if line.startswith(tag) and "theta=" in line:
                d = kv(line)
                if cond(d): seen[tuple(sorted((k, v) for k, v in d.items() if k != "cg"))] = d
    return list(seen.values())
A = load(["f3_t0_hladder.out", "f3_t0_hladder2.out"], "T0", lambda d: d["Y"] == "10" and d["Ymax"] == "10")
A = sorted((float(d["h"]), float(d["theta"])) for d in A)[::-1]
D = load(["f3_mimic.out", "f3_mimic_big.out"], "MIMIC",
         lambda d: d["a"] == "2.0" and d["Lg"] == "1.0" and d["capR"] == "1.0" and d["extra"] == "0")
D = sorted((1.0 / float(d["L"]), float(d["theta"])) for d in D)[::-1]
def hp(h, t, a, p): return t + a * h ** p
def fits(h, y):
    out = {}
    c = np.polyfit(h, y, 1); out["h"] = (c[1], y - np.polyval(c, h), c[:1])
    c = np.polyfit(np.log(1 / h), y, 1); out["log"] = (None, y - np.polyval(c, np.log(1 / h)), c[:1])
    best = None
    for p0 in (0.3, 0.6, 0.9, 1.2, 2.0):
        try:
            par, _ = curve_fit(hp, h, y, p0=(y[-1], -0.2, p0), method="lm", maxfev=20000, xtol=1e-15, ftol=1e-15)
        except RuntimeError:
            continue
        r = y - hp(h, *par)
        if best is None or (r ** 2).sum() < (best[1] ** 2).sum(): best = (par[0], r, par[1:])
    out["h^p"] = best
    return out
hv = np.array([a for a, _ in A]); par, _ = curve_fit(hp, hv, 0.4 - 0.2 * hv ** 0.77, p0=(0.39, -0.1, 0.5), method="lm",
                                                    xtol=1e-15, ftol=1e-15, maxfev=20000)
print(f"# validation h^p synthetic: t={par[0]:.12f} p={par[2]:.9f} {'PASS' if abs(par[0]-0.4)<=1e-8 else 'FAIL'}")
allv = []
for f in glob.glob(os.path.join(N, "f3*.out")):
    for line in open(f):
        m = re.search(r"\btheta=([0-9.]+)", line)
        if m: allv.append((float(m.group(1)), os.path.basename(f), line.split()[0], line.strip()[:60]))
allv.sort()
print(f"# finite-mesh theta values parsed from f3*.out: n={len(allv)}; largest three:")
for v in allv[-3:]: print("#   ", v)
for name, fam in (("A", A), ("D", D)):
    h = np.array([a for a, _ in fam])[-5:]; y = np.array([b for _, b in fam])[-5:]
    print(f"# family {name}: rungs used {list(zip(h.round(8).tolist(), y.tolist()))}")
    for m, (t, r, extra) in fits(h, y).items():
        r3 = np.abs(r[-3:]).max()
        ts = "none" if t is None else f"{t:.5f}"
        print(f"  {name} {m:4s} t_inf={ts:>8s} extra={np.round(extra, 4).tolist()} max|res|3={r3:.2e} "
              f"adm(1e-4)={r3 <= 1e-4} adm(1e-3)={r3 <= 1e-3}")
