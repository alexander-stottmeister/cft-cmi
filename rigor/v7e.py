import numpy as np
from scipy.integrate import quad
import warnings; warnings.filterwarnings("ignore")
pi=np.pi
def lc(x):                       # log cosh, stable
    ax=np.abs(x); return ax+np.log1p(np.exp(-2*ax))-np.log(2.0)
def G(u,v):                      # stable integrand: iint G du dv = g_B (r=1)
    return np.tanh(u/2)**2/(1+np.exp(lc(v/2)-lc(u/2)))*v**2/(u**2*(u**2+4*pi**2)**2)
def innerv(u,v0,V=4000.):
    return quad(lambda v: G(u,v), v0, v0+V, limit=600, epsabs=1e-18, epsrel=1e-12)[0]
tot=4*quad(lambda u: innerv(u,0.0), 1e-12, 4000., limit=600, epsabs=1e-18, epsrel=1e-11)[0]
print(f"total iint G = {tot:.12f}   2/(3pi^2) = {2/(3*pi**2):.12f}")
print(" Lam    E(L)=g_B-g_B^(L)      2/(3L^2)      ratio   repaired piece  x L^4   step<1>5 LHS   1/(6L^2)")
for L in [10.,20.,40.,80.,160.,320.]:
    E=4*(quad(lambda u: innerv(u,max(0.,2*L-u)), 1e-12, 2*L, limit=600, epsabs=1e-20, epsrel=1e-10)[0]
        +quad(lambda u: innerv(u,0.0), 2*L, 2*L+4000., limit=600, epsabs=1e-20, epsrel=1e-10)[0])
    piece=4*quad(lambda u: innerv(u,L), 1e-12, L, limit=600, epsabs=1e-20, epsrel=1e-10)[0]
    lhs15=piece+4*quad(lambda u: innerv(u,L), L, L+4000., limit=600, epsabs=1e-20, epsrel=1e-10)[0]
    print(f"{L:6.0f}  {E:.6e}  {2/(3*L**2):.6e}  {E/(2/(3*L**2)):.4f}  {piece:.4e}  {piece*L**4:8.3f}   {lhs15:.4e}   {1/(6*L**2):.4e}")
