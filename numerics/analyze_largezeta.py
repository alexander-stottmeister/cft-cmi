"""PZ: analysis of largezeta_cert.raw -> results_largezeta_certified.txt + fidelity_table_largezeta.tex."""
import numpy as np, re, os, sys
from scipy.optimize import curve_fit
HERE = os.path.dirname(os.path.abspath(__file__))

def load(fn="largezeta_cert.raw"):
    rec = []
    for ln in open(os.path.join(HERE, fn)):
        if not ln.startswith("RES"): continue
        d = dict(kv.split("=", 1) for kv in ln.split()[1:] if "=" in kv)
        if d["Phi"] == "nan": continue
        r = dict(s=float(d["s"]), zeta=float(d["zeta"]), Lam=float(d["Lam"]), kmax=float(d["kmax"]),
                 eps=float(d["eps"]), kc=float(d["kceff"]), n=int(d["nsub"]), N=int(d["N"]), Phi=float(d["Phi"]))
        if not any(abs(q["zeta"]-r["zeta"]) < 1e-9 and q["Lam"] == r["Lam"] and q["kmax"] == r["kmax"]
                   and q["eps"] == r["eps"] for q in rec):
            rec.append(r)
    return rec

def fits(kc, Phi):
    """Phi_inf from (a) p free, (b) p=1, (c) p=2 fits of Phi(kc)=Phi_inf - b kc^-p."""
    kc = np.asarray(kc, float); Phi = np.asarray(Phi, float); out = {}
    for tag, p0 in (("p1", 1.0), ("p2", 2.0)):
        A = np.vstack([np.ones_like(kc), -kc**(-p0)]).T
        c, *_ = np.linalg.lstsq(A, Phi, rcond=None); out[tag] = (c[0], c[1], p0)
    if len(kc) >= 3:
        try:
            f = lambda x, Pi, b, p: Pi - b*x**(-p)
            popt, _ = curve_fit(f, kc, Phi, p0=[Phi.max()*1.05, 1.0, 1.5], maxfev=40000)
            out["free"] = tuple(popt)
        except Exception:
            pass
    if len(kc) >= 2:                       # two-point Richardson on the two largest windows
        i, j = np.argsort(kc)[-2:]
        for p0 in (1.0, 2.0):
            r = (kc[i]/kc[j])**p0
            out[f"rich{int(p0)}"] = ((Phi[j] - r*Phi[i])/(1-r), None, p0)
    return out

LAT = [(0.66667,2.214528e-03),(0.84706,3.189856e-03),(0.89286,3.455263e-03),(0.96970,3.910136e-03),
       (1.12500,4.801267e-03),(1.21905,5.396293e-03),(1.28205,5.757578e-03),(1.60000,7.681831e-03),
       (1.98621,1.003693e-02),(2.08333,1.065870e-02),(2.24561,1.171773e-02),(2.57143,1.352931e-02),
       (2.89855,1.550203e-02),(3.55556,1.909594e-02),(4.54545,2.465830e-02),(4.87619,2.731354e-02),
       (5.53846,2.929953e-02),(6.20155,3.334059e-02),(7.52941,3.872806e-02),(9.52381,4.973731e-02),
       (11.52000,5.613913e-02),(15.51515,7.839737e-02),(19.51220,8.767256e-02),(23.51020,9.552423e-02)]

def lat_interp(z):
    x = np.log([a for a, _ in LAT]); y = np.log([b for _, b in LAT])
    return float(np.exp(np.interp(np.log(z), x, y)))

def lat_slope(z):
    x = np.log([a for a, _ in LAT]); y = np.log([b for _, b in LAT])
    h = 0.25
    return float((np.interp(np.log(z)+h, x, y) - np.interp(np.log(z)-h, x, y))/(2*h))

def report():
    rec = load(); zs = sorted(set(r["zeta"] for r in rec))
    out = ["# PZ (2026-09-08): continuum Phi(zeta) = -log F(rho_ABC, rho~_ABC) for zeta >= 1: rigorous lower bounds Phi_sub, extrapolated estimates Phi_inf (not certified; label corrected 2026-09-24).",
           "# a=1, L=2, zeta = s/3.  Phi_sub = spectral-window (eps < w < 1-eps) sub-compression = rigorous LOWER bound.",
           "# kappa_c = log((1-eps)/eps) (clipped to kappa_max).  Pipeline run_largezeta_cert.py, cross-checked",
           "# against fidelity_hp.py/fidelity_flint.py to 7 digits at (Lam,kmax)=(60,30) and (120,45).", "",
           "## 1. raw sub-compressed values", "  zeta      Lam kmax    N   eps      kappa_c  n_sub   Phi_sub"]
    for z in zs:
        for r in sorted([r for r in rec if r["zeta"] == z], key=lambda r: (r["Lam"], r["kmax"], r["kc"])):
            out.append(f"  {z:8.4f}  {r['Lam']:.0f} {r['kmax']:4.0f} {r['N']:5d}  {r['eps']:.0e}  {r['kc']:6.2f} {r['n']:6d}   {r['Phi']:.7e}")
    out += ["", "## 2. window (UV) tail law at fixed zeta:  Phi_sub(kappa_c) = Phi_inf - b kappa_c^{-p}",
            "  zeta    box        p_free   Phi_inf(free)  Phi_inf(p=1)  Phi_inf(p=2)  Rich(p=1)   Rich(p=2)   Phi_sub(max kc)"]
    best = {}
    for z in zs:
        for (Lam, kmax) in sorted(set((r["Lam"], r["kmax"]) for r in rec if r["zeta"] == z)):
            g = sorted([r for r in rec if r["zeta"] == z and r["Lam"] == Lam and r["kmax"] == kmax], key=lambda r: r["kc"])
            if len(g) < 2: continue
            kc = [r["kc"] for r in g]; ph = [r["Phi"] for r in g]; f = fits(kc, ph)
            pf = f.get("free", (np.nan, np.nan, np.nan))
            out.append(f"  {z:6.3f}  {Lam:.0f}/{kmax:.0f}   {pf[2]:7.3f}  {pf[0]:.5e}   {f['p1'][0]:.5e}  {f['p2'][0]:.5e}  "
                       f"{f['rich1'][0]:.5e} {f['rich2'][0]:.5e} {ph[-1]:.5e}  (kc={kc[-1]:.1f})")
            if (Lam, kmax) == (120.0, 45.0):
                best[z] = (g, f)
    out += ["", "## 3. box dependence at fixed (zeta, kappa_c)  [Lam/kmax -> Phi_sub]"]
    for z in zs:
        for kc0 in sorted(set(round(r["kc"], 1) for r in rec if r["zeta"] == z)):
            g = [r for r in rec if r["zeta"] == z and abs(r["kc"]-kc0) < 0.05]
            if len(g) < 2: continue
            out.append(f"  zeta={z:7.3f} kappa_c={kc0:5.2f}: " + "  ".join(f"{r['Lam']:.0f}/{r['kmax']:.0f}={r['Phi']:.6e}" for r in
                                                                          sorted(g, key=lambda r: (r["Lam"], r["kmax"]))) +
                       f"   spread={max(r['Phi'] for r in g)/min(r['Phi'] for r in g)-1:.2e}")
    return out, best, zs

def vu(v, u):
    """value(uncertainty) with the uncertainty as two digits in the last places shown."""
    d = max(0, int(np.ceil(-np.log10(u))) + 1)
    return f"{v:.{d}f}({round(u*10**d):d})"

def certify():
    out, best, zs = report()
    out += ["", "## 4. brackets  [Phi_sub(largest window), Phi_inf]  (lower end rigorous; upper end extrapolated, not a bound)  and best estimate",
            "  zeta     lower=Phi_sub(kc_max)   Phi_inf estimates (free,p1,p2,R1,R2)                      best +- unc      rel"]
    cen = {}
    for z in zs:
        if z not in best: continue
        g, f = best[z]; lo = g[-1]["Phi"]
        pfree = f["free"][0] if "free" in f else float("nan")
        kc = [r["kc"] for r in g]; ph = [r["Phi"] for r in g]
        pe = f["free"][2] if "free" in f else 2.0
        i, j = -2, -1; t = (kc[i]/kc[j])**pe; rich = (ph[j] - t*ph[i])/(1-t)
        alts = [x for x in (rich, f["p2"][0], f["rich2"][0]) if np.isfinite(x)]
        best_v = pfree if np.isfinite(pfree) else rich
        unc = max([abs(a-best_v) for a in alts] + [0.25*(best_v-lo)])
        cen[z] = (lo, best_v, best_v, unc, pe)
        out.append(f"  {z:7.3f}  {lo:.6e}   " + " ".join(f"{f[k][0]:.5e}" if k in f else "     -     "
                   for k in ("free", "p1", "p2", "rich1", "rich2")) +
                   f"  p={pe:.2f} Rich={rich:.5e}   {best_v:.5e} +- {unc:.1e}  {unc/best_v*100:5.2f}%")
    out += ["", "## 5. local log-slope d log Phi / d log zeta  and lattice comparison",
            "  zeta     Phi_best      slope_cont   Phi_lat(interp)  slope_lat   Phi_lat/Phi_best"]
    zl = sorted(cen); lg = [np.log(cen[z][2]) for z in zl]; lz = [np.log(z) for z in zl]
    for i, z in enumerate(zl):
        if 0 < i < len(zl)-1: sl = (lg[i+1]-lg[i-1])/(lz[i+1]-lz[i-1])
        elif i == 0: sl = (lg[1]-lg[0])/(lz[1]-lz[0])
        else: sl = (lg[-1]-lg[-2])/(lz[-1]-lz[-2])
        pl = lat_interp(z) if 0.667 <= z <= 23.5 else float("nan")
        out.append(f"  {z:7.3f}  {cen[z][2]:.5e}   {sl:8.3f}   {pl:.5e}      {lat_slope(z):6.3f}     {pl/cen[z][2]:.4f}")
    open(os.path.join(HERE, "results_largezeta_certified.txt"), "w").write("\n".join(out)+"\n")
    # ---- LaTeX table -------------------------------------------------------
    kcs = sorted(set(round(r["kc"], 1) for r in load() if r["Lam"] == 120 and r["kmax"] == 45))
    L = [r"\begin{table}[ht]\centering\small",
         r"\caption{Continuum \(\Phi(\zeta)=-\log\Fid(\rho_{ABC},\tilde\rho_{ABC})\) at large cross ratio: rigorous lower bounds and uncertified extrapolated estimates "
         r"(\(a=1\), \(L=2\), \(\zeta=s/3\); box \(\Lambda=120\), \(\kappa_{\max}=45\)). \(\Phi^{\rm sub}\) in the spectral "
         r"window \(\eps<w<1-\eps\), \(\kappa_c=\log(1/\eps)\), is a rigorous lower bound; the small-\(\zeta\) tail "
         r"\(\zeta^2/(15\kappa_c^2)\) is NOT valid here. \(\Phi_\infty\) is the \(\kappa_c\to\infty\) extrapolation "
         r"\(\Phi^{\rm sub}=\Phi_\infty-b\,\kappa_c^{-p}\) (\(p\) free), an estimate and not a bound; the bracket is "
         r"\([\Phi^{\rm sub}(\kappa_c^{\max}),\Phi_\infty]\). Last columns: local log-slope and the lattice value "
         r"(O7a, \(c=1\) hopping chain) interpolated at the same \(\zeta\).}\label{tab:largezeta}",
         r"\begin{tabular}{r" + "r"*len(kcs) + r" r r r r}\toprule",
         r"\(\zeta\) & " + " & ".join(rf"\(\kappa_c{{=}}{k:.1f}\)" for k in kcs) +
         r" & \(\Phi_\infty\) & best \(\Phi\) & \(d\log\Phi/d\log\zeta\) & \(\Phi_{\rm lat}\) \\\midrule"]
    for i, z in enumerate(zl):
        g = {round(r["kc"], 1): r["Phi"] for r in load() if r["zeta"] == z and r["Lam"] == 120 and r["kmax"] == 45}
        sl = (lg[min(i+1, len(zl)-1)]-lg[max(i-1, 0)])/(lz[min(i+1, len(zl)-1)]-lz[max(i-1, 0)])
        pl = lat_interp(z) if 0.667 <= z <= 23.5 else float("nan")
        L.append(f"{z:.3f} & " + " & ".join((f"{g[k]*1e2:.4f}" if k in g else "--") for k in kcs) +
                 f" & {cen[z][1]*1e2:.4f} & {vu(cen[z][2]*1e2, cen[z][3]*1e2)} & {sl:.2f} & {pl*1e2:.4f}" + r" \\")
    L += [r"\bottomrule\end{tabular}", r"\\[2pt]\footnotesize All \(\Phi\) entries are \(10^{2}\,\Phi\).", r"\end{table}"]
    open(os.path.join(HERE, "fidelity_table_largezeta.tex"), "w").write("\n".join(L)+"\n")
    print("\n".join(out))

if __name__ == "__main__":
    certify()
