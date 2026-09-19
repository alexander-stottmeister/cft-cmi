import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import sys, numpy as np, re
sys.path.insert(0, _os.path.join(_ROOT, "numerics"))
from compression_box import Q_box
NUM = _os.path.join(_ROOT, "numerics")

print("=== (J) the Moebius check (a,L,s)=(2,1,0.1) vs (1,2,0.2) ===")
z1 = np.load(NUM+"Dhat_exact_s0.2_Lam60_k30_g12.npz", allow_pickle=True)
z2 = np.load(NUM+"Dhat_mobius_a2L1_s0.1_Lam60_k30_g12.npz", allow_pickle=True)
D1, D2 = z1['Dhat'], z2['Dhat']
print(f"  a,L,s = ({float(z1['a'])},{float(z1['L'])},{float(z1['s'])}) vs ({float(z2['a'])},{float(z2['L'])},{float(z2['s'])});"
      f"  zeta = {float(z1['a'])*float(z1['s'])/(float(z1['a'])+float(z1['L'])):.6f} both")
print(f"  max|D1 - D2|      = {np.abs(D1-D2).max():.3e}      (max|D| = {np.abs(D1).max():.3e})")
print(f"  max|D1 - conj(D2)|= {np.abs(D1-D2.conj()).max():.3e}")
print(f"  max||D1|-|D2||    = {np.abs(np.abs(D1)-np.abs(D2)).max():.3e}")
print("  -> the two configurations give (up to conjugation) the SAME matrix, so the Moebius test")
print("     verifies the coordinate code but is an identity, not an independent numerical check.")

print("\n=== (K) recomputation of one 'line' value: f2, s2 at Lam=120, kmax=44.74 ===")
def ell(p, q):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.abs(p-q) > 1e-14*np.maximum(p, q), (np.log(p)-np.log(q))/(p-q), 1/p)
for fn in ["Dhat_first_s1.0_Lam120_k45_g12.npz"]:
    z = np.load(NUM+fn, allow_pickle=True); D = z['Dhat']; kap = z['kappa']
    zeta = 1*1.0/3; A = np.abs(D)**2
    q = 1/(1+np.exp(kap)); omq = 1/(1+np.exp(-kap))
    Nw = q[:, None]*omq[None, :] + q[None, :]*omq[:, None]
    f2 = 0.25*np.sum(A/Nw)/zeta**2
    P = q[:, None]*np.ones(len(q))[None, :]; Pm = omq[:, None]*np.ones(len(q))[None, :]
    s2 = 0.5*np.sum(A*(ell(P, P.T)+ell(Pm, Pm.T)))/zeta**2
    print(f"  reproduce line_so.py:  f2={f2:.7f}  s2={s2:.6f}   (line_so.txt: 0.0084112 / 0.076821)")
    # independent: closed-form |D1|^2 from kernel_identity, same box weights
    dk = kap[1]-kap[0]; u = kap[:, None]-kap[None, :]; v = kap[:, None]+kap[None, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        Dc = np.where(np.abs(u) > 1e-12, (q[:, None]-q[None, :])*v/(u*(u**2+4*np.pi**2)),
                      -kap[:, None]*q[:, None]*(1-q[:, None])/(2*np.pi**2))
    Ac = (dk*zeta*Dc)**2
    f2c = 0.25*np.sum(Ac/Nw)/zeta**2; s2c = 0.5*np.sum(Ac*(ell(P, P.T)+ell(Pm, Pm.T)))/zeta**2
    print(f"  from the CLOSED FORM D1 (kernel_identity.tex) with the same box grid: f2={f2c:.7f}  s2={s2c:.6f}")
    # Riemann-sum convergence to the continuum integrals
    print(f"  (this is the Delta_kappa^2 Riemann sum of  (1/4)int int |D1|^2/N  over |kappa|<={kap.max():.2f})")

print("\n=== (L) where the sub-compression actually cuts (vs kappa_c = log((1-eps)/eps)) ===")
for fn, Lam in [("Dhat_exact_s0.2_Lam60_k30_g12.npz", 60.0), ("Dhat_exact_s0.2_Lam120_k45_g12.npz", 120.0)]:
    z = np.load(NUM+fn, allow_pickle=True); kap = z['kappa']; Q = Q_box(kap, Lam)
    w = np.sort(np.linalg.eigvalsh(Q))
    for eps in [1e-8, 1e-11]:
        keep = (w > eps) & (w < 1-eps); n = keep.sum()
        wk = w[keep]
        kap_eff = np.log((1-wk.min())/wk.min())
        print(f"  {fn.split('/')[-1][:34]:34s} eps={eps:.0e}: n_sub={n} (N={len(w)})  smallest kept eig={wk.min():.3e}"
              f"  -> effective |kappa|_cut={kap_eff:.2f}   nominal kappa_c={np.log((1-eps)/eps):.2f}")

print("\n=== (M) make_tables.py provenance: which result file feeds which column ===")
def parse(fn):
    out = []
    for l in open(NUM+fn):
        if not l.startswith(('exact_', 'mobius_', 'Dhat_exact')): continue
        tag = l.split(':')[0].replace('Dhat_', '').replace('_g12.npz', '')
        kc = float(re.search(r'kc=([\d.]+)', l).group(1))
        z = float(re.search(r'zeta=([\d.e+-]+)', l).group(1))
        cor = float(re.search(r'-logF_sub=[-\d.e+]+ \+tail=([\d.e+-]+)', l).group(1))
        mS = re.search(r'S(?:_sub)?=(nan|[\d.e+-]+)(?: \+tail=(nan|[\d.e+-]+))?', l)
        out.append((tag, z, kc, cor, float(mS.group(1))))
    return out
for f in ['results_A.txt', 'results_L120.txt', 'results_hp.txt', 'results_final.txt']:
    p = parse(f)
    print(f"  {f}: {len(p)} rows; kc set = {sorted(set(r[2] for r in p))}; "
          f"tags = {sorted(set(r[0].rsplit('_s',1)[0]+'|'+r[0].split('_',2)[2] for r in p))[:3]} ...")
    nn = [r for r in p if not np.isfinite(r[4])]
    if nn: print(f"     !! {len(nn)} rows with S = nan: {[r[0] for r in nn]}")
