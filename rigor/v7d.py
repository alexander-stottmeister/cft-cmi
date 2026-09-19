import numpy as np
from scipy.integrate import quad
pi=np.pi
def pref(u):  # sinh^2(u/2)/(cosh(u/2) u^2 (u^2+4pi^2)^2), even
    return np.sinh(u/2)**2/(np.cosh(u/2)*u**2*(u**2+4*pi**2)**2)
def Vfull(u): return 2*u*(u**2+4*pi**2)/(3*np.sinh(u/2))
def tail_v(u,V0):
    if V0<=0: return Vfull(u)
    f=lambda v: v**2/(np.cosh(v/2)+np.cosh(u/2))
    r,_=quad(f,V0,V0+400,limit=400); return 2*r
print(" Lam    exact E(L)=2iint_{Bc}|D|^2/N    2/(3L^2)     ratio    piece{|v|>L,|u|<=L}   *L^4    step<1>5 LHS   1/(6L^2)")
for L in [10.,20.,40.,80.,160.]:
    I1,_=quad(lambda u: pref(u)*tail_v(u,2*L-u),1e-9,2*L,limit=400)
    I2,_=quad(lambda u: pref(u)*Vfull(u),2*L,2*L+2000,limit=400)
    tot=2*0.5*2*(I1+I2)   # factor 2 for u<0, 1/2 Jacobian, outer 2 of g_B
    J,_=quad(lambda u: pref(u)*tail_v(u,L),1e-9,L,limit=400)
    piece=2*0.5*2*J
    K1,_=quad(lambda u: pref(u)*tail_v(u,L),1e-9,L,limit=400)
    K2,_=quad(lambda u: pref(u)*tail_v(u,L),L,L+3000,limit=400)
    lhs=2*0.5*2*(K1+K2)
    print(f"{L:6.0f}  {tot:.6e}  {2/(3*L**2):.6e}  {tot/(2/(3*L**2)):.4f}  {piece:.4e}  {piece*L**4:.4f}   {lhs:.4e}   {1/(6*L**2):.4e}")
