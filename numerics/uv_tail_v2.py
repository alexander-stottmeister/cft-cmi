"""UV tail of the recovered symbol in the modular eigenbasis, v2.
Normalization: psi_kappa = beta^{-1/2} e^{i sigma kappa xi/2pi}/(2pi), so int dkappa |psi><psi| = 1.
Then  Qt(k,k) - q_k = -D(k,k) = (1/pi) Im J,  J = (2pi)^{-2} int int sqrt(beta beta') K(-x,y) e^{i sigma k (xi'-xi)/2pi}.
Kernel options: 'exact' K=R_s ; 'first' K = (s/L) u v/(u+v)^2 (O(s) part).
Mesh: geometric toward the corner (|xi-xi0| from 1e-10 to 0.2, ratio 1+dg), uniform h beyond, trapezoid.
Prediction (exact kernel): (2/15) s^2 beta0^2 / L^2 / kappa^3.
"""
import numpy as np, sys
a, L = 1.0, 2.0
xi0 = np.log(a/L); beta0 = a*L/(a+L)
def x_of(xi): e = np.exp(xi); return (L*e - a)/(1+e)
def beta(x): return (x+a)*(L-x)/(a+L)
def kern(u, v, s, kind):
    if kind == 'exact': return s*u*v/((u+v)*(L*(u+v)+s*u*v))
    return (s/L)*u*v/(u+v)**2
def mesh(h, cut, dg):
    g = 1e-10*(1+dg)**np.arange(0, int(np.log(0.2/1e-10)/np.log(1+dg))+1)   # geometric part up to ~0.2
    g = g[g < 0.2]
    p = np.concatenate((g, np.arange(0.2, cut, h)))                             # distances from corner (corner point itself omitted: kernel bounded)
    w = np.zeros_like(p); w[1:] += np.diff(p)/2; w[:-1] += np.diff(p)/2            # trapezoid weights
    return p, w
def diag_defect(kappa, s, kind, h=0.004, cut=38.0, dg=0.02, sigma=+1.0):
    p, w = mesh(h, cut, dg)
    xA = x_of(xi0 - p); yD = x_of(xi0 + p)               # A side: xi = xi0 - p ; D side: xi' = xi0 + p
    fa = np.sqrt(beta(xA))*w*np.exp(1j*sigma*kappa*p/(2*np.pi))   # e^{-i sigma k xi/2pi} ~ e^{+i sigma k p/2pi} (xi0 phase cancels)
    fd = np.sqrt(beta(yD))*w*np.exp(1j*sigma*kappa*p/(2*np.pi))   # e^{+i sigma k xi'/2pi}
    J = 0j; chunk = 1500
    for i in range(0, len(p), chunk):
        u = -xA[i:i+chunk][:,None]; v = yD[None,:]
        J += np.sum(fa[i:i+chunk][:,None]*kern(u, v, s, kind)*fd[None,:])
    J /= (2*np.pi)**2
    return J.imag/np.pi
if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv)>1 else 'exact'; s = float(sys.argv[2]) if len(sys.argv)>2 else 0.2
    pred = (2/15)*s**2*beta0**2/L**2
    print(f"# kind={kind} a={a} L={L} s={s}; cols: kappa | -D(kk) h=.004 | h=.008 | pred (2/15)s^2 b0^2/L^2/k^3 | q_k")
    for kappa in [4,8,12,16,20,30,40,60,80,120]:
        d1 = diag_defect(kappa, s, kind, h=0.004); d2 = diag_defect(kappa, s, kind, h=0.008)
        print(f"{kappa:6.1f} {d1: .5e} {d2: .5e} {pred/kappa**3: .5e} {1/(1+np.exp(kappa)):.2e}")
