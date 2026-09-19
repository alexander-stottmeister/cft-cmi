"""v4 audit: fast double-precision diagnostics."""
import sys, numpy as np, glob, re
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics")
from compression_box import Q_box
from fidelity_flint import second_order
NUM = "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/"
a, L = 1.0, 2.0; xi0 = np.log(a/L)

print("=== (A) first-order defect matrix vs the closed form D1(k,k')=(q-q')(k+k')/[u(u^2+4pi^2)] ===")
print("    (rigor/kernel_identity.tex Thm; box prediction  Dhat_jl = Delta_kappa * zeta * D1(k_j,k_l))")
for fn in ["Dhat_first_s1.0_Lam60_k30_g12.npz", "Dhat_first_s1.0_Lam120_k45_g12.npz",
           "Dhat_first_s1.0_Lam240_k45_g12.npz"]:
    z = np.load(NUM+fn, allow_pickle=True); D = z['Dhat']; kap = z['kappa']; s = float(z['s'])
    Lam = float(z['Lam']); zeta = a*s/(a+L); dk = kap[1]-kap[0]
    q = 1/(1+np.exp(kap)); u = kap[:, None]-kap[None, :]; v = kap[:, None]+kap[None, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        D1 = np.where(np.abs(u) > 1e-12, (q[:, None]-q[None, :])*v/(u*(u**2+4*np.pi**2)),
                      -kap[:, None]*q[:, None]*(1-q[:, None])/(2*np.pi**2))
    pred = dk*zeta*D1
    m = np.abs(pred) > 1e-14
    rel = np.abs(np.abs(D)-np.abs(pred))[m]/np.abs(pred)[m]
    print(f"  {fn}: Lam={Lam} N={len(kap)} dkappa={dk:.4f}  max rel dev = {rel.max():.3e}, "
          f"median = {np.median(rel):.3e};  |D|max={np.abs(D).max():.3e}")
    for (i, j) in [(len(kap)//2, len(kap)//2), (len(kap)//2+3, len(kap)//2+9),
                   (len(kap)//2-7, len(kap)//2+4)]:
        print(f"     ({kap[i]:+7.3f},{kap[j]:+7.3f}): |Dhat|={abs(D[i,j]):.10e}  pred={abs(pred[i,j]):.10e}"
              f"  ratio={abs(D[i,j])/abs(pred[i,j]):.8f}")

print("\n=== (B) xi0-phase sensitivity of the second-order coefficient f2/s2 (uses eigvecs of Q_N) ===")
for fn in ["Dhat_first_s1.0_Lam60_k30_g12.npz", "Dhat_first_s1.0_Lam120_k45_g12.npz"]:
    z = np.load(NUM+fn, allow_pickle=True); D = z['Dhat']; kap = z['kappa']; Lam = float(z['Lam'])
    zeta = a*float(z['s'])/(a+L); Q = Q_box(kap, Lam)
    U = np.exp(-1j*(kap/(2*np.pi))*xi0); Dno = U.conj()[:, None]*D*U[None, :]
    f2p, s2p = second_order(Q, D); f2n, s2n = second_order(Q, Dno)
    print(f"  {fn}: f2(code, mixed basis)={f2p/zeta**2:.8f}  f2(consistent centred)={f2n/zeta**2:.8f}"
          f"   rel diff={abs(f2p-f2n)/abs(f2n):.3e}")
    print(f"      s2(code)={s2p/zeta**2:.6f}  s2(centred)={s2n/zeta**2:.6f}   rel diff={abs(s2p-s2n)/abs(s2n):.3e}")

print("\n=== (C) note S3.1 claims about eig(Q_N) and the 'trap' remark ===")
for (Lam, fn) in [(60.0, "Dhat_exact_s0.2_Lam60_k30_g12.npz"), (120.0, "Dhat_exact_s0.2_Lam120_k45_g12.npz")]:
    z = np.load(NUM+fn, allow_pickle=True); D = z['Dhat']; kap = z['kappa']
    Q = Q_box(kap, Lam); w = np.linalg.eigvalsh(Q); wt = np.linalg.eigvalsh(Q-D)
    print(f"  Lam={Lam} kappa_max={kap.max():.2f}: min eig Q_N = {w.min():.4e}, 1-max = {1-w.max():.4e}"
          f" | min eig Qt_N = {wt.min():.4e}, 1-max = {1-wt.max():.4e}   [note S3.1 claims '>~1e-4']")
    qd = np.diag(1/(1+np.exp(kap)))
    wtrap = np.linalg.eigvalsh(qd-D)
    print(f"     'trap' diag(qhat)-Dhat: min eig = {wtrap.min():.3e}  (note says ~ -1e-11 for kappa_max>~24)")

print("\n=== (D) t->0 endpoint term in the Q_box diagonal: effect on Phi (the note's '0.2% O(h)') ===")
import compression_box as cb
z = np.load(NUM+"Dhat_exact_s0.2_Lam60_k30_g12.npz", allow_pickle=True)
D = z['Dhat']; kap = z['kappa']; Lam = 60.0; zeta = 1/15.
def Q_box_noend(kappa, Lam, nt=400001):
    Q = Q_box(kappa, Lam).copy(); k = kappa/(2*np.pi)
    w0 = Lam/(2*(nt-1))
    Q[np.arange(len(k)), np.arange(len(k))] += (1/(2*np.pi*Lam))*w0*2*Lam*k
    return Q
for tag, QQ in [("with endpoint (code)", Q_box(kap, Lam)), ("without endpoint", Q_box_noend(kap, Lam))]:
    w1, V1 = np.linalg.eigh(QQ); w2, V2 = np.linalg.eigh(QQ-D)
    keep = (w1 > 1e-8) & (w1 < 1-1e-8)
    P = V1[:, keep]; ws = w1[keep]; Qs = P.conj().T @ (QQ-D) @ P
    e2, U2 = np.linalg.eigh(Qs)
    g1 = np.sqrt(ws/(1-ws)); g2 = np.sqrt(e2/(1-e2))
    Wm = g1[:, None]*U2*g2[None, :]
    tau = np.linalg.eigvalsh(Wm @ Wm.conj().T)
    lf = 0.5*np.sum(np.log(1-ws)) + 0.5*np.sum(np.log(1-e2)) + np.sum(np.log(1+np.sqrt(np.clip(tau, 0, None))))
    print(f"  {tag:24s}: n_sub={keep.sum()}  -logF_sub = {-lf:.8e}")

print("\n=== (E) kmax-extrapolation of line_so.txt with FREE exponents ===")
from scipy.optimize import curve_fit
rows = []
for l in open(NUM+"line_so.txt"):
    m = re.search(r'kmax=([\d.]+).*?f2_line=([\d.]+) s2_line=([\d.]+)', l)
    if m: rows.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
rows.sort(); K = np.array([r[0] for r in rows]); F = np.array([r[1] for r in rows]); S = np.array([r[2] for r in rows])
print("  data:", list(zip(K.round(2), F, S)))
for name, Y, guess in [("f2", F, (0.00844, 0.07, 2.0)), ("s2", S, (0.083, 0.3, 1.0))]:
    def mod(k, y, c, p): return y - c*k**(-p)
    po, pc = curve_fit(mod, K, Y, p0=guess, maxfev=200000)
    err = np.sqrt(np.diag(pc))
    print(f"  {name}: 3-param fit  {name}_inf={po[0]:.7f} +- {err[0]:.1e},  C={po[1]:.4f} +- {err[1]:.1e},"
          f"  p={po[2]:.4f} +- {err[2]:.2f}")
    for pfix in ([2.0] if name == "f2" else [1.0]):
        def mod2(k, y, c): return y - c*k**(-pfix)
        po2, pc2 = curve_fit(mod2, K, Y, p0=guess[:2], maxfev=200000)
        e2_ = np.sqrt(np.diag(pc2))
        res = Y-mod2(K, *po2)
        print(f"      p fixed = {pfix}: {name}_inf={po2[0]:.7f} +- {e2_[0]:.1e}, C={po2[1]:.4f};"
              f"  max resid = {np.abs(res).max():.2e}")
    # last-two-point Richardson with the note's exponents
    pn = 2.0 if name == "f2" else 1.0
    x = K**(-pn); yy = Y
    sl = (yy[-1]-yy[-2])/(x[-1]-x[-2]); print(f"      last-two Richardson (p={pn}): {yy[-1]-sl*x[-1]:.7f}")
print(f"  analytic targets (rigor/verify_normalization.py): f2 = 1/(12 pi^2) = {1/(12*np.pi**2):.9f},  s2 = 1/12 = {1/12:.9f}")
