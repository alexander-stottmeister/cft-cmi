import numpy as np
from scipy.integrate import solve_ivp, quad, dblquad
# chi = x^2 beta(x-1), beta smooth 1 on (-inf,0], 0 on [1,inf)
def beta(t):
    t=np.atleast_1d(np.asarray(t,float)); out=np.zeros_like(t)
    m=(t<=0); out[m]=1.0
    m=(t>0)&(t<1); u=t[m]
    # smooth step: 1 - S(u), S = 6u^5-15u^4+10u^3  (C^2)
    out[m]=1-(6*u**5-15*u**4+10*u**3)
    return out
def dbeta(t):
    t=np.atleast_1d(np.asarray(t,float)); out=np.zeros_like(t)
    m=(t>0)&(t<1); u=t[m]; out[m]=-(30*u**4-60*u**3+30*u**2)
    return out
def chi(x):
    x=np.atleast_1d(np.asarray(x,float)); out=np.zeros_like(x)
    m=x>0; out[m]=x[m]**2*beta(x[m]-1); return out
def chip(x):
    x=np.atleast_1d(np.asarray(x,float)); out=np.zeros_like(x)
    m=x>0; out[m]=2*x[m]*beta(x[m]-1)+x[m]**2*dbeta(x[m]-1); return out
# flow of -chi d/dx together with derivative
def flow(s, xs):
    def rhs(t,y):
        n=len(xs); x=y[:n]; d=y[n:]
        return np.concatenate([-chi(x), -chip(x)*d])
    y0=np.concatenate([np.asarray(xs,float), np.ones(len(xs))])
    sol=solve_ivp(rhs,[0,s],y0,rtol=1e-12,atol=1e-14,dense_output=True)
    return sol
def kappa(phi_x,phi_y,dphi_x,dphi_y,x,y):
    return np.sqrt(dphi_x*dphi_y)/(phi_x-phi_y) - 1.0/(x-y)
def kappa1(x,y):
    return (1.0/(x-y))*((chi(x)-chi(y))/(x-y) - 0.5*(chip(x)+chip(y)))
# TEST 1: exact integral representation  kappa_{k_s}(x,y) = int_0^s sqrt(k'k') kappa1(k(x),k(y)) dsig
print("TEST 1: integral representation of the defect kernel")
pts=[(-0.7,0.5),(0.3,0.9),(0.2,1.6),(-2.0,1.9),(0.05,0.06),(1.2,3.0),(-5.0,0.8)]
for s in [0.05,0.3,1.0]:
    err=0.0
    for (x,y) in pts:
        sol=flow(s,[x,y])
        Y=sol.sol(s); lhs=kappa(Y[0],Y[1],Y[2],Y[3],x,y)
        def integrand(sig):
            Z=sol.sol(sig)
            return float(np.sqrt(Z[2]*Z[3])*kappa1(np.array([Z[0]]),np.array([Z[1]]))[0])
        rhs=quad(integrand,0,s,limit=200,epsabs=1e-12,epsrel=1e-12)[0]
        err=max(err,abs(lhs-rhs))
    print(f"  s={s:<5} max |lhs-rhs| over {len(pts)} point pairs = {err:.3e}")
# TEST 2: kappa1(-u,v) = uv/(u+v)^2 for u>0, 0<v<1
print("TEST 2: kappa^(1)(-u,v) vs uv/(u+v)^2   (Note 4 cross-check, sign included)")
e=0.0
for u in [0.1,0.5,1.0,3.0,10.0]:
    for v in [0.05,0.3,0.7,0.99]:
        e=max(e,abs(kappa1(np.array([-u]),np.array([v]))[0]-u*v/(u+v)**2))
print(f"  max error = {e:.3e}")
# TEST 3: the A x D block integral   (1/(8 pi^2)) * 2 * int int u^2v^2/(u+v)^4 = 1/(24 pi^2)
val=dblquad(lambda u,v: (u*v/(u+v)**2)**2, 0,1, 0, np.inf, epsabs=1e-12)[0]
print(f"TEST 3: 2*int_A int_D (kappa1)^2 = {2*val:.10f}  (exact 1/3 = {1/3:.10f});")
print(f"        (1/(8pi^2))*that = {2*val/(8*np.pi**2):.10f}, 1/(24 pi^2) = {1/(24*np.pi**2):.10f},"
      f" g_B/4 = {1/(6*np.pi**2):.10f}, ratio = {(2*val/(8*np.pi**2))/(1/(6*np.pi**2)):.6f}")
# TEST 4: Q[chi] for PA's Definition 2.1 field  = (1/(8 pi^2)) int int kappa1^2
f=lambda y,x: kappa1(np.array([x]),np.array([y]))[0]**2
tot=0.0
# support: kappa1 vanishes unless x or y in [0,2]
tot+=dblquad(f,-60,62,-60,62,epsabs=1e-10)[0]
print(f"TEST 4: Q[chi_PA] = (1/(8pi^2)) * {tot:.6f} = {tot/(8*np.pi**2):.6f}   (PA reports 0.1926;"
      f" g_B/4 = {1/(6*np.pi**2):.6f})")
