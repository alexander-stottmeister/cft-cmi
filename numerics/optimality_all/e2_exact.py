import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""E2 (d): beyond first order.  With the optimised exterior generator Z_e (Tikhonov
parameter mu) form the unitary W~ and evaluate the EXACT Uhlmann exponent
   UH(W~) := -1/2 log det(1 - V^*V),   V = P^perp W~ P,
via the singular values of V and log1p.  Three constructions, all first-order equal:
  sum : W~ = exp(Z_pre + Z_e)
  prod: W~ = exp(Z_pre) exp(Z_e)
  Ws  : W~ = W_s exp(-s eps_* G_*) exp(Z_e)   [W_s = exp(-s D_chi); = prod for eps=0]
Z_pre = -s D_chi (compression) or -s(D_chi + eps_* G_*) (rotated); the free block is
E_{I^c} Z E_{I^c}, because a unitary extension of W~|_{L^2(I)} fixes the whole column
Z E_I to first order and leaves exactly E_c Z E_c free.
Compare with UB (first order) and with 1/2 s^2 |u|^2 (1-theta).
"""
import sys, numpy as np, scipy.linalg as sla
sys.path.insert(0, _os.path.join(_ROOT, 'numerics/optimality_all'))
import e2_common as E

def UH(P, Pp, Wt):
    V = Pp@Wt@P; sv = np.linalg.svd(V, compute_uv=False); sv = np.clip(sv, 0.0, 1-1e-15)
    return -0.5*np.sum(np.log1p(-sv**2)), 0.5*np.sum(sv**2)

if __name__ == "__main__":
    MUS = (1e-4, 1e-6, 1e-8, 1e-10)
    for L in (128, 192, 256, 384):
        S = E.build(L=L); P, Pp, Dc = S['P'], S['Pp'], S['Dc']
        theta, Gx, eps, nu2, u, M = E.Gstar(S, iters=90)
        Gs = eps*Gx; v = Pp@Gs@P
        print(f"=== L={L}  theta={theta:.5f}  |u|^2={nu2:.8e}  1-theta={1-theta:.5f} ===", flush=True)
        for s in (0.001, 0.002, 0.005):
            base = 0.5*s*s*nu2
            print(f"  s={s:.3f}   1/2 s^2|u|^2 = {base:.8e}   (1-theta)*that = {base*(1-theta):.8e}")
            for lab, Zpre, X in (("compr", -s*Dc, -s*M), ("rot", -s*(Dc+Gs), -s*(M+v))):
                for mu in MUS:
                    Ze = E.Zext(S, X, mu=mu)
                    ub = 0.5*np.real(np.vdot(X+Pp@Ze@P, X+Pp@Ze@P))
                    Wsum = sla.expm(Zpre+Ze); Wpro = sla.expm(Zpre)@sla.expm(Ze)
                    e1, h1 = UH(P, Pp, Wsum); e2, h2 = UH(P, Pp, Wpro)
                    extra = ""
                    if lab == "rot":
                        Wws = sla.expm(-s*Dc)@sla.expm(-s*eps*Gx)@sla.expm(Ze)
                        e3, _ = UH(P, Pp, Wws); extra = f" Ws-prod={e3:.6e} ({e3/base:.5f})"
                    print(f"    {lab:5s} mu={mu:.0e} |Ze|_F={np.linalg.norm(Ze):.3e}"
                          f" |Ze|_op={np.linalg.norm(Ze,2):.3e} | UB={ub:.6e} ({ub/base:.5f})"
                          f" | exact sum={e1:.6e} ({e1/base:.5f}) prod={e2:.6e} ({e2/base:.5f})"
                          + extra, flush=True)
