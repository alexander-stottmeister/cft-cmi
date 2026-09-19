import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
"""v4 audit: (i) derivation check of the tail correction zeta^2/(15 kappa_c^2) and its validity;
(ii) the note's 'trap' remark; (iii) ratio tests for the kmax exponents."""
import sys, numpy as np, re
sys.path.insert(0, _os.path.join(_ROOT, "numerics"))
from compression_box import Q_box
NUM = _os.path.join(_ROOT, "numerics")
from scipy.integrate import quad

print("=== (F) tail correction: sum over discarded modes of the EXACT single-mode -log fidelity ===")
print("    single decoupled mode, vacuum occ q, recovered occ q+d:")
print("    -log[sqrt(q(q+d)) + sqrt((1-q)(1-q-d))]  vs the linearisation d/2")
for zeta in [1/15, 1/120, 8/15]:
    for eps in [1e-8, 1e-11]:
        kc = np.log((1-eps)/eps)
        d = lambda k: (2/15)*zeta**2/k**3
        q = lambda k: 1/(1+np.exp(k))
        def exact(k):
            qq = q(k); dd = d(k)
            if qq+dd >= 1: return 0.0
            return -np.log(np.sqrt(qq*(qq+dd)) + np.sqrt((1-qq)*(1-qq-dd)))
        Ie, _ = quad(exact, kc, kc+200, limit=400)
        Il = zeta**2/(30*kc**2)
        print(f"  zeta={zeta:.5f} eps={eps:.0e} kc={kc:.3f}: per side exact={Ie:.4e} linearised d/2={Il:.4e}"
              f"  ratio={Ie/Il:.4f}  |  both sides: applied={2*Il:.4e} vs 'exact-tail'={2*Ie:.4e}"
              f"  (diff = {2*(Il-Ie):.2e})")
print("   kappa_*(zeta) where (2/15)zeta^2 k^-3 = e^-k:")
for zeta in [1/15, 1/120, 8/15]:
    from scipy.optimize import brentq
    ks = brentq(lambda k: (2/15)*zeta**2/k**3 - np.exp(-k), 1.0, 60.0)
    print(f"      zeta={zeta:.5f}: kappa_* = {ks:.2f}   (kappa_c = 18.42 at eps=1e-8, 25.33 at eps=1e-11)")

print("\n=== (G) accuracy of the asymptotic tail density itself (measured/predicted from the box data) ===")
for fn, Lam in [("Dhat_exact_s0.2_Lam240_k60_g12.npz", 240.0), ("Dhat_exact_s0.2_Lam120_k90_g12.npz", 120.0)]:
    z = np.load(NUM+fn, allow_pickle=True); D = z['Dhat']; kap = z['kappa']; zeta = 1*0.2/3
    dkk = kap[1]-kap[0]; dens = -np.diag(D).real/dkk
    print(f"  {fn}:")
    for kk in [18.4, 20, 25, 30, 40, 50]:
        i = int(np.argmin(np.abs(kap-kk)))
        if kap[i] > kap.max()-1: continue
        pred = (2/15)*zeta**2/kap[i]**3
        print(f"     kappa={kap[i]:6.2f}: measured/asymptotic = {dens[i]/pred:.4f}")

print("\n=== (H) 'trap' remark: eigenvalues of diag(qhat) - Dhat ===")
import glob
for fn in sorted(glob.glob(NUM+"Dhat_exact_*.npz")):
    z = np.load(fn, allow_pickle=True); D = z['Dhat']; kap = z['kappa']
    qd = np.diag(1/(1+np.exp(kap)))
    w = np.linalg.eigvalsh(qd-D)
    print(f"  {fn.split('/')[-1]:42s} kmax={kap.max():5.1f}: min eig(diag(q)-D) = {w.min():+.3e}")

print("\n=== (I) ratio tests for the kmax exponents (note claims 2.0 and 1.0) ===")
rows = []
for l in open(NUM+"line_so.txt"):
    m = re.search(r'kmax=([\d.]+).*?f2_line=([\d.]+) s2_line=([\d.]+)', l)
    if m: rows.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
rows.sort(); K = np.array([r[0] for r in rows]); F = np.array([r[1] for r in rows]); S = np.array([r[2] for r in rows])
for nm, Y in [("f2", F), ("s2", S)]:
    print(f"  {nm}: successive increments and the implied local exponent")
    for i in range(len(K)-2):
        d1 = Y[i+1]-Y[i]; d2 = Y[i+2]-Y[i+1]
        # model Y = Yinf - C k^-p  =>  differences of k^-p
        from scipy.optimize import brentq
        try:
            p = brentq(lambda p: (K[i]**-p - K[i+1]**-p)/(K[i+1]**-p - K[i+2]**-p) - d1/d2, 0.05, 12.0)
        except Exception:
            p = float('nan')
        print(f"     kmax=({K[i]:.1f},{K[i+1]:.1f},{K[i+2]:.1f}): d1={d1:.3e} d2={d2:.3e}  local p = {p:.3f}")
