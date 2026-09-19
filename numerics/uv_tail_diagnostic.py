"""UV-tail diagnostic: diagonal of the covariance defect D = Q_I - Qtilde_s in the
modular eigenbasis psi_kappa of the single-interval Hardy compression Q_I.
Geometry: A=(-a,0), D=BC=(0,L). Modular coordinate xi = log((x+a)/(L-x)),
beta(x) = dx/dxi = (x+a)(L-x)/(a+L), psi_kappa = beta^{-1/2} e^{i sigma kappa xi/2pi}/sqrt(2pi).
Kernel: D(x,y) = (i/2pi) R_s(-x,y) on A x D, R_s(u,v) = s u v /((u+v)(L(u+v)+s u v)).
Then -D(kappa,kappa) = (1/pi) Im J,  J = int_A int_D conj(psi) R psi.
Positivity of Qtilde requires -D(kappa,kappa) >= -q_kappa ~ -e^{-kappa}.
"""
import numpy as np, sys
a, L = 1.0, 2.0
xi0 = np.log(a/L)
def x_of(xi): e = np.exp(xi); return (L*e - a)/(1+e)
def beta(x): return (x+a)*(L-x)/(a+L)
def R(u, v, s): return s*u*v/((u+v)*(L*(u+v)+s*u*v))
def diag_defect(kappa, s, h=0.004, cut=38.0, sigma=+1.0):
    # xi grid on A: (xi0-cut, xi0], on D: [xi0, xi0+cut); trapezoid
    xa = np.arange(xi0-cut, xi0+1e-12, h); xd = np.arange(xi0, xi0+cut+1e-12, h)
    wa = np.full_like(xa, h); wa[0]=wa[-1]=h/2
    wd = np.full_like(xd, h); wd[0]=wd[-1]=h/2
    xA = x_of(xa); yD = x_of(xd)
    fa = np.sqrt(beta(xA))*wa; fd = np.sqrt(beta(yD))*wd
    # integrand: fa(xi) fd(xi') R(-x,y) e^{i sigma kappa (xi'-xi)/2pi}/(2pi)
    ph_a = np.exp(-1j*sigma*kappa*xa/(2*np.pi)); ph_d = np.exp(1j*sigma*kappa*xd/(2*np.pi))
    J = 0j
    chunk = 2000
    for i in range(0, len(xa), chunk):
        u = -xA[i:i+chunk][:,None]; v = yD[None,:]
        Rm = R(u, v, s)
        J += np.sum((fa[i:i+chunk]*ph_a[i:i+chunk])[:,None]*Rm*(fd*ph_d)[None,:])
    J /= 2*np.pi
    return (1/np.pi)*J.imag   # = Qtilde(kappa,kappa) - q_kappa
if __name__ == "__main__":
    s = float(sys.argv[1]) if len(sys.argv)>1 else 0.2
    print(f"# a={a} L={L} s={s}; columns: kappa, -D(kk) [h=0.004], -D(kk) [h=0.008], q_kappa")
    for kappa in [2,4,6,8,10,14,18,24,30,40,50,60]:
        d1 = diag_defect(kappa, s, h=0.004); d2 = diag_defect(kappa, s, h=0.008)
        print(f"{kappa:5.1f}  {d1: .6e}  {d2: .6e}  {1/(1+np.exp(kappa)):.3e}")
