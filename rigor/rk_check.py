"""RK (Phase 2b) numerical checks for rigor/kubo_mori_gauge_lemma.tex.

(C1) frame consistency: ||T(f)Om||^2 in the line chart  vs  in the modular frame of K.
(C2) the Kubo-Mori cancellation: spectral form  vs  local Sobolev form (c/12)(||f~''||^2+||f~'||^2).
(C3) the gauge infimum: Phi_*(R)=2R^2(2R-1)/(R-1)^2 (tail solved by Rayleigh-Ritz) and
     min_R Phi_* = 11+5 sqrt5 at R=(3+sqrt5)/2;  Note 7's renormalised value is Phi=2.
(C4) monotonicity of the relative entropy under restriction, finite dimensions.
Run: <venv>/bin/python rk_check.py
"""
import numpy as np
from scipy.linalg import logm, expm

C = 1.0  # central charge; every quantity below is exactly linear in c

# ---------------------------------------------------------------- helpers
def What(k, c=C):
    """W^(k) = (c/24pi) k(k^2+1)/(e^{2pi k}-1), the frame two-point weight (Note 7, Lem 4.1)."""
    k = np.asarray(k, dtype=float)
    out = np.empty_like(k)
    small = np.abs(k) < 1e-7
    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
        big = ~small
        out[big] = (c/(24*np.pi))*k[big]*(k[big]**2+1)/np.expm1(2*np.pi*k[big])
    # k/expm1(2 pi k) -> 1/(2pi) * (1 - pi k + ...)
    out[small] = (c/(24*np.pi))*(1+k[small]**2)*(1-np.pi*k[small])/(2*np.pi)
    out[~np.isfinite(out)] = 0.0
    return out

def bump(t, a, b):
    """C^infty bump supported exactly on [a,b]."""
    t = np.asarray(t, dtype=float)
    u = (t-a)/(b-a)
    out = np.zeros_like(u)
    m = (u > 0) & (u < 1)
    out[m] = np.exp(-1.0/(u[m]*(1-u[m])))
    return out

def ft(vals, dz):
    """f^(k)=int f(z)e^{-ikz}dz on a uniform grid; returns (k, fhat) with |fhat| only meaningful."""
    N = vals.size
    k = 2*np.pi*np.fft.fftfreq(N, d=dz)
    return k, dz*np.fft.fft(vals)

# ---------------------------------------------------------------- (C1),(C2)
def c1_c2(R=1.0, xi_a=0.2, xi_b=1.2, N=1 << 20, span=(-2.0, 6.0)):
    xi = np.linspace(span[0], span[1], N, endpoint=False)
    dxi = xi[1]-xi[0]
    ft_ = bump(xi, xi_a, xi_b)                      # the frame field  f~(xi)
    x = R*(1-np.exp(-xi))                           # inverse frame map
    f = (R-x)*ft_                                   # the field f(x) = beta_K(x) f~(xi)
    # ---- frame side
    k, fth = ft(ft_, dxi)
    dk = k[1]-k[0] if k[1] > 0 else 2*np.pi/(N*dxi)
    nrm_frame = np.sum(What(k)*np.abs(fth)**2)*dk/(2*np.pi)
    gkm_spec = (C/(24*np.pi))*np.sum(k**2*(k**2+1)*np.abs(fth)**2)*dk
    # W^(k) m(e^{2pi k}) = (c/24pi)(k^2+1)/(2pi) exactly (the KMS denominator cancels)
    var_spec = (C/(96*np.pi**3))*np.sum((k**2+1)*np.abs(fth)**2)*dk
    # ---- line-chart side: resample f on a uniform x-grid
    xa, xb = R*(1-np.exp(-xi_a)), R*(1-np.exp(-xi_b))
    Nx = 1 << 20
    xg = np.linspace(xa-1.0, xb+1.0, Nx, endpoint=False)
    dx = xg[1]-xg[0]
    xig = -np.log(np.maximum(R-xg, 1e-300)/R)
    fg = np.where((xg > xa) & (xg < xb), (R-xg)*bump(xig, xi_a, xi_b), 0.0)
    p, fh = ft(fg, dx)
    pos = p > 0
    nrm_line = (C/(48*np.pi**2))*np.sum(p[pos]**3*np.abs(fh[pos])**2)*(2*np.pi/(Nx*dx))
    # ---- local Sobolev form, finite differences in xi
    d1 = np.gradient(ft_, dxi); d2 = np.gradient(d1, dxi)
    gkm_loc = (C/12)*np.sum(d1**2+d2**2)*dxi
    var_loc = (C/(48*np.pi**2))*np.sum(d1**2+ft_**2)*dxi
    return dict(nrm_frame=nrm_frame, nrm_line=nrm_line, gkm_spec=gkm_spec, gkm_loc=gkm_loc,
                var_spec=var_spec, var_loc=var_loc)

# ---------------------------------------------------------------- (C3)
def tail_min(alpha, beta, xi1, L=60.0, n=3000):
    """min int(u''^2+u'^2) over [xi1,xi1+L], u(xi1)=alpha, u'(xi1)=beta, u=u'=0 at the end (FD + normal eqs)."""
    import scipy.sparse as sp, scipy.sparse.linalg as spl
    h = L/n
    m = n-1                                    # unknowns u_1..u_{n-1};  u_0=alpha, u_n=0, ghost u_{-1}=u_1-2h*beta
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    def add(j, coef):
        # contribution of node j to the current residual row
        if j <= -1:
            rows.append(r); cols.append(0); vals.append(coef); rhs[-1] -= coef*(-2*h*beta)
        elif j == 0:
            rhs[-1] -= coef*alpha
        elif j <= m:
            rows.append(r); cols.append(j-1); vals.append(coef)
        # j == n : u_n = 0
    for j in range(0, n):
        rhs.append(0.0)
        w = np.sqrt(h)/h**2
        add(j+1, w); add(j, -2*w); add(j-1, w)
        r += 1
        rhs.append(0.0)
        w = np.sqrt(h)/(2*h)
        add(j+1, w); add(j-1, -w)
        r += 1
    A = sp.coo_matrix((vals, (rows, cols)), shape=(r, m)).tocsr()
    b = np.array(rhs)
    M = (A.T@A).tocsc(); v = A.T@b
    u = spl.spsolve(M, v)
    return float(np.sum((A@u-b)**2))

def c3():
    out = {}
    Rs = [1.5, 2.0, 2.618033988749895, 3.0, 5.0]
    for R in Rs:
        xi1 = np.log(R/(R-1))
        fixed = 2*R**2*np.sinh(2*xi1)
        alpha, beta = -2*R*(np.cosh(xi1)-1), -2*R*np.sinh(xi1)
        num = tail_min(alpha, beta, xi1)
        out[R] = (fixed+beta**2, 2*R**2*(2*R-1)/(R-1)**2, fixed+num)
    return out

# ---------------------------------------------------------------- (C4)
def c4(seed=20260909, d1=2, d2=2, s_list=(0.2, 0.05, 0.01)):
    rng = np.random.default_rng(seed); d = d1*d2
    def rand_rho():
        X = rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)); r = X@X.conj().T
        return r/np.trace(r).real
    def herm():
        X = rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)); return (X+X.conj().T)/2
    def ptrace(r):
        return np.trace(r.reshape(d1, d2, d1, d2), axis1=1, axis2=3)
    def rel(a, b):
        return np.trace(a@(logm(a)-logm(b))).real
    rho, A = rand_rho(), herm()
    res = []
    for s in s_list:
        u = expm(1j*s*A); rs = u.conj().T@rho@u
        res.append((s, rel(rs, rho), rel(ptrace(rs), ptrace(rho))))
    return res

if __name__ == "__main__":
    print("== (C1),(C2)  frame vs line chart, R=1 ==")
    r = c1_c2()
    print(f"  ||T(f)Om||^2  frame = {r['nrm_frame']:.10f}   line = {r['nrm_line']:.10f}"
          f"   rel.diff = {abs(r['nrm_frame']-r['nrm_line'])/r['nrm_line']:.3e}")
    print(f"  g_KM^(K)      spec  = {r['gkm_spec']:.10f}   local= {r['gkm_loc']:.10f}"
          f"   rel.diff = {abs(r['gkm_spec']-r['gkm_loc'])/r['gkm_loc']:.3e}")
    print(f"  Var^KM        spec  = {r['var_spec']:.10f}   local= {r['var_loc']:.10f}"
          f"   rel.diff = {abs(r['var_spec']-r['var_loc'])/r['var_loc']:.3e}")
    print("== (C3)  gauge infimum:  R -> (closed form, formula, quadrature+Rayleigh-Ritz) ==")
    for R, (cf, fo, rr) in c3().items():
        print(f"  R={R:8.5f}   closed={cf:12.6f}  2R^2(2R-1)/(R-1)^2={fo:12.6f}   FD-min={rr:12.6f}")
    print(f"  11+5sqrt5 = {11+5*np.sqrt(5):.6f}   at R*=(3+sqrt5)/2 = {(3+np.sqrt(5))/2:.6f}")
    print(f"  Note 7 renormalised value Phi_ren = 2  ->  g_KM = c/6 = {1/6:.6f}"
          f";  honest inf = {(11+5*np.sqrt(5))/12:.6f} c  (ratio {(11+5*np.sqrt(5))/2:.4f})")
    print("== (C4)  monotonicity D_M <= D_N, finite dimensions ==")
    for s, dN, dM in c4():
        print(f"  s={s:6.3f}   D_N={dN:.8f}   D_M={dM:.8f}   D_M<=D_N: {dM<=dN+1e-12}"
              f"   D_N/s^2={dN/s**2:.6f}  D_M/s^2={dM/s**2:.6f}")
