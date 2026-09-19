import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""E2 (b),(c): the invisible components (1-Pi)M, (1-Pi)v and their distance to Ext;
the optimised Uhlmann bound UB(Z_I) = min_{Z_e} 1/2||P^perp(Z_I+Z_e)P||_F^2.

Since Ext is contained in N^perp (L1), Proj_Ext(Pi X) = 0, hence
  dist((1-Pi)X, Ext)^2 = ||X||^2 - ||Pi X||^2 - ||Proj_Ext X||^2 ,
  UB(X) = 1/2 dist(X, Ext)^2 = 1/2 (||Pi X||^2 + dist((1-Pi)X,Ext)^2).
The exterior-only block of D_chi lies in Ext, so using the full D_chi or D_chi with its
I^c-I^c block deleted gives the same UB; the strictly block-diagonal truncation
E_I D_chi E_I is reported separately.  Tikhonov mu bounds ||Z_e||_F.
"""
import sys, numpy as np
sys.path.insert(0, _os.path.join(_ROOT, 'numerics/optimality_all'))
import e2_common as E

def report(S, X, name, tag=""):
    n2 = np.real(np.vdot(X, X))
    pi2, leakN = E.normPi2(S, X)
    ext2, leakE, _, _ = E.normExt2(S, X)
    inv2 = n2-pi2                       # ||(1-Pi)X||^2
    d2 = n2-pi2-ext2                    # dist((1-Pi)X, Ext)^2
    print(f"  {name:<26s}{tag} ||X||^2={n2:.8e}  ||Pi X||^2={pi2:.8e}  ||(1-Pi)X||^2={inv2:.8e}")
    print(f"  {'':<26s}  ||Proj_Ext X||^2={ext2:.8e}  dist((1-Pi)X,Ext)^2={d2:.3e}"
          f"  rel dist={np.sqrt(max(d2,0)/inv2):.3e}   leak(N)={leakN:.1e} leak(Ext)={leakE:.1e}")
    return dict(n2=n2, pi2=pi2, inv2=inv2, ext2=ext2, d2=d2)

if __name__ == "__main__":
    MUS = [0.0, 1e-14, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2]
    for L in (128, 192, 256, 384):
        S = E.build(L=L); P, Pp = S['P'], S['Pp']
        theta, Gx, eps, nu2, u, M = E.Gstar(S, iters=90)
        Gs = eps*Gx                                     # G_* = eps_* x   (Z_rot = s(D_chi+G_*))
        v = Pp@Gs@P
        I = S['I']; Dtr = np.zeros_like(S['Dc']); Dtr[np.ix_(I, I)] = S['Dc'][np.ix_(I, I)]
        Mtr = Pp@Dtr@P
        print(f"=== L={L}  theta={theta:.5f}  eps_*={eps:+.5f}  |u|^2={nu2:.8e} "
              f" |I|={len(I)} |I^c|={len(S['Ic'])} ===")
        rM = report(S, M, "M = P^perp D_chi P")
        rv = report(S, v, "v = P^perp G_* P")
        rR = report(S, M+v, "M + v  (rotated)")
        rT = report(S, Mtr, "P^perp (E_I D_chi E_I) P")
        print(f"  CHECK ||Pi(M+v)||^2/|u|^2 = {rR['pi2']/nu2:.6f}   1-theta = {1-theta:.6f}")
        print(f"  UB_c/(1/2 s^2|u|^2)      = {(rM['pi2']+rM['d2'])/nu2:.8f}   (= 1 + d_c^2/|u|^2)")
        print(f"  UB_rot/UB_c              = {(rR['pi2']+rR['d2'])/(rM['pi2']+rM['d2']):.8f}"
              f"   UB_rot/(1/2 s^2|u|^2) = {(rR['pi2']+rR['d2'])/nu2:.8f}")
        print(f"  UB_c(truncated Z_I)/(1/2 s^2|u|^2) = {(rT['n2']-rT['ext2'])/nu2:.6f}")
        print("  Tikhonov trade-off (unit s):   mu        UB_c/(s^2|u|^2/2)   ||Z_e||_F/s"
              "      UB_rot/(s^2|u|^2/2)   ||Z_e||_F/s")
        for mu in MUS:
            _, _, redc, z2c = E.normExt2(S, M, mu=mu)
            _, _, redr, z2r = E.normExt2(S, M+v, mu=mu)
            print(f"      {mu:8.0e}   {(rM['n2']-redc)/nu2:>16.6f}   {np.sqrt(z2c):>12.4e}"
                  f"   {(rR['n2']-redr)/nu2:>16.6f}   {np.sqrt(z2r):>12.4e}")
        print(f"  s-independence: UB is exactly quadratic in s (UB(sX)=s^2 UB(X)); for "
              f"s=0.001,0.002,0.005 the ratios above are unchanged to machine precision.")
        for s in (0.001, 0.002, 0.005):
            print(f"      s={s:.3f}: UB_c={0.5*s*s*(rM['n2']-rM['ext2']):.6e}  "
                  f"1/2 s^2|u|^2={0.5*s*s*nu2:.6e}  ratio={(rM['n2']-rM['ext2'])/nu2:.8f}  "
                  f"UB_rot={0.5*s*s*(rR['n2']-rR['ext2']):.6e}  UB_rot/UB_c="
                  f"{(rR['n2']-rR['ext2'])/(rM['n2']-rM['ext2']):.8f}")
        print(flush=True)
