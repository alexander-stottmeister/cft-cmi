"""QK (O2): numerical verification of the type-III Kubo-Mori second-variation identities.

Standard form in finite dimensions: H = HS(C^n), M = left multiplications, Om = rho^{1/2},
J X = X^*, Delta X = rho X rho^{-1}.  For A = A^* in M, u_s = e^{isA}, om_s = om o Ad u_s,
i.e. rho_s = u_s^* rho u_s.  Claims to check:

 (I1) D(rho||rho_s) = < w_s , h(Delta) w_s >,  w_s = (u_s - 1)Om,  h(x) = x - 1 - log x >= 0.
 (I2) int (lambda-1) d nu^{w_s} = 0 exactly (nu^{w_s} = spectral measure of w_s w.r.t. Delta).
 (I3) g_KM = -2 <AOm, log Delta AOm> = int (lambda-1) log lambda d mu = sum |drho_ij|^2 l(p_i,p_j).
 (I4) KMS symmetry int f(lambda) d mu = int f(1/lambda) lambda d mu.
 (I5) D(rho||rho_s)/s^2 -> g_KM/2.
 (I6) tail bound  int_{lambda<1/N} (-log lambda) d sigma_s <= (log N) N^{-eps} ||Delta^{-eps/2}w_s||^2/s^2
      and  s^{-2}||Delta^{-eps/2} w_s||^2 bounded (analyticity of A for sigma^om is automatic in fin dim).
"""
import numpy as np
from scipy.linalg import expm, logm

rng = np.random.default_rng(20260908)

def rand_state(n, spread=1.0):
    G = rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n))
    H = (G + G.conj().T)/2
    p, U = np.linalg.eigh(spread*H)
    p = np.exp(p); p = p/p.sum()
    return p, U

def rand_herm(n):
    G = rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n))
    return (G + G.conj().T)/2

def ell(p, q):
    with np.errstate(divide='ignore', invalid='ignore'):
        out = np.where(np.abs(p-q) > 1e-12, (np.log(p)-np.log(q))/(p-q), 1.0/np.where(p>0, p, 1))
    return out

def hfun(x):
    return x - 1.0 - np.log(x)

def relent(rho, sig):
    return np.real(np.trace(rho @ (logm(rho) - logm(sig))))

def report(name, a, b):
    d = abs(a-b)/max(1.0, abs(a))
    print(f"  {name:52s} {a: .12e}  {b: .12e}   rel {d:.2e}   {'OK' if d < 1e-8 else '**MISMATCH**'}")

for n, spread in [(3, 1.0), (5, 2.0), (7, 3.0)]:
    print(f"\n=== n = {n}, spread = {spread} ===")
    p, U = rand_state(n, spread)
    # work in the eigenbasis of rho: rho = diag(p)
    A = U.conj().T @ rand_herm(n) @ U          # A in the rho-eigenbasis
    rho = np.diag(p); rt = np.diag(np.sqrt(p))
    LAM = np.outer(p, 1.0/p)                    # Delta eigenvalue on |i><j|
    Om = rt
    a = A @ rt                                  # A Om
    mu = np.abs(a)**2                           # spectral weights of A Om
    # (I3)
    gKM_log   = -2.0*np.sum(mu*np.log(LAM))
    gKM_wt    = np.sum(mu*(LAM-1.0)*np.log(LAM))
    gKM_h     = 2.0*np.sum(mu*hfun(LAM))
    drho      = -1j*(A @ rho - rho @ A)
    gKM_fd    = np.sum(np.abs(drho)**2 * ell(p[:, None], p[None, :]))
    report("(I3) g_KM: -2<AOm,logD AOm>  vs  sum|drho|^2 l", gKM_log, gKM_fd)
    report("(I3) g_KM: int(lam-1)log lam dmu             ", gKM_wt, gKM_fd)
    report("(I3) g_KM: 2 int h dmu                       ", gKM_h,  gKM_fd)
    # (I4) KMS symmetry with f(x)=x^{-0.3}
    f = lambda x: x**(-0.3)
    report("(I4) int f dmu vs int f(1/lam) lam dmu       ",
           np.sum(mu*f(LAM)), np.sum(mu*f(1.0/LAM)*LAM))
    # (I1),(I2),(I5),(I6)
    print(f"  {'s':>10s} {'D(rho||rho_s)':>18s} {'<w,h(D)w>':>18s} {'int(lam-1)dnu':>15s} {'D/s^2':>14s}")
    for s in [0.3, 0.1, 0.03, 0.01, 0.003]:
        us = expm(1j*s*A)
        rho_s = us.conj().T @ rho @ us
        D = relent(rho, rho_s)
        w = (us - np.eye(n)) @ rt
        nu = np.abs(w)**2
        Dh = np.sum(nu*hfun(LAM))
        m1 = np.sum(nu*(LAM-1.0))
        print(f"  {s:10.4g} {D: .12e} {Dh: .12e} {m1: .3e} {D/s**2: .8e}")
    print(f"  {'':10s} {'':18s} {'':18s} {'g_KM/2 =':>15s} {gKM_fd/2: .8e}")
    # (I6) uniform bound on s^{-2}||Delta^{-eps/2}w_s||^2
    for eps in [0.25, 0.5]:
        vals = []
        for s in [0.3, 0.1, 0.03, 0.01]:
            us = expm(1j*s*A); w = (us - np.eye(n)) @ rt
            vals.append(np.sum(np.abs(w)**2 * LAM**(-eps))/s**2)
        print(f"  (I6) eps={eps}: s^-2||D^-eps/2 w_s||^2 = " +
              " ".join(f"{v:.4f}" for v in vals) +
              f"   limit ||D^-eps/2 AOm||^2 = {np.sum(mu*LAM**(-eps)):.4f}")

# ----------------------------------------------------------------------------
# (I7) Legendre form: g_KM = sup_K [2 phi(K) - Var^KM(K)], optimiser K Om = m(Delta)^{-1} eta.
# (I8) tail estimates of the upper-bound proof, on a deliberately "type-III-like" spectrum.
# (I9) free-fermion recovery curve: g_KM from the first-order kernel, target c/6 = 1/6.
# ----------------------------------------------------------------------------
print("\n=== (I7) Legendre form of g_KM ===")
for n, spread in [(4, 2.0), (6, 3.0)]:
    p, U = rand_state(n, spread)
    A = U.conj().T @ rand_herm(n) @ U
    rho = np.diag(p); rt = np.diag(np.sqrt(p)); LAM = np.outer(p, 1.0/p)
    a = A @ rt
    gKM = np.sum(np.abs(a)**2 * (LAM-1.0)*np.log(LAM))
    mlog = np.where(np.abs(LAM-1) > 1e-12, (LAM-1.0)/np.log(np.where(LAM>0,LAM,1)), 1.0)  # log mean
    eta = 1j*(LAM-1.0)*a                     # eta = i(Delta-1) a, entrywise
    Kvec = eta/mlog                          # m(Delta)^{-1} eta
    K = Kvec @ np.diag(1.0/np.sqrt(p))       # K Om = Kvec  =>  K = Kvec rho^{-1/2}
    phi = np.real(np.sum(np.conj(eta)*Kvec))            # phi(K) = <eta, K Om>
    varKM = np.real(np.sum(mlog*np.abs(Kvec)**2)) - np.real(np.trace(rho@K))**2
    report(f"  n={n}: 2phi(K)-Var^KM(K) vs g_KM", 2*phi-varKM, gKM)
    print(f"     K hermitian? max|K-K^*| = {np.max(np.abs(K-K.conj().T)):.2e}")

print("\n=== (I8) tail estimates, spectrum p_i ~ exp(-beta i) with beta = 4 (lambda up to e^{24}) ===")
n = 7; beta = 4.0
p = np.exp(-beta*np.arange(n)); p /= p.sum()
A = rand_herm(n); rho = np.diag(p); rt = np.diag(np.sqrt(p)); LAM = np.outer(p, 1.0/p)
a = A @ rt; mu = np.abs(a)**2
gKM = np.sum(mu*(LAM-1.0)*np.log(LAM))
print(f"  lambda range [{LAM.min():.3e}, {LAM.max():.3e}],  g_KM/2 = {gKM/2:.10e}")
for eps in [0.25, 0.5]:
    C2 = max(np.sum(np.abs((expm(1j*s*A)-np.eye(n))@rt)**2 * LAM**(-eps))/s**2
             for s in [0.1, 0.03, 0.01, 0.003])
    print(f"  eps={eps}: C^2 = sup_s s^-2||D^-eps/2 w_s||^2 = {C2:.4e}"
          f"   (||D^-eps/2 AOm||^2 = {np.sum(mu*LAM**(-eps)):.4e})")
    for N in [10.0, 100.0, 1000.0]:
        lhs = max(np.sum((np.abs((expm(1j*s*A)-np.eye(n))@rt)**2 * hfun(LAM))[LAM < 1/N])/s**2
                  for s in [0.1, 0.03, 0.01, 0.003])
        print(f"     N={N:7.0f}:  sup_s int_{{lam<1/N}} h dsigma_s = {lhs:.4e}"
              f"   <=  C^2 logN/N^eps = {C2*np.log(N)/N**eps:.4e}   "
              f"{'OK' if lhs <= C2*np.log(N)/N**eps*(1+1e-9) else '**VIOLATED**'}")
for s in [0.1, 0.03, 0.01, 0.003, 0.001]:
    w = (expm(1j*s*A)-np.eye(n)) @ rt
    D = relent(rho, expm(-1j*s*A) @ rho @ expm(1j*s*A))
    print(f"  s={s:8.4g}: D/s^2 = {D/s**2:.8e}   int(lam-1)dnu = {np.sum(np.abs(w)**2*(LAM-1)):.2e}")
print(f"  {'':8s}  g_KM/2 = {gKM/2:.8e}")

print("\n=== (I9) free fermion: g_KM from the first-order kernel (target c/6 = 1/6) ===")
# stable integrand:  |D1|^2 [ l(q,q') + l(1-q,1-q') ]  =  g^2 (q_{k'}-q_k)(k-k'),
#   g = (k+k')/[(k-k')((k-k')^2+4pi^2)],  because  log q - log(1-q) = -k.
def qf(k): return 1.0/(1.0+np.exp(k))
def integrand(k, kp):
    u = k-kp; s2 = k+kp
    g = np.where(np.abs(u) > 1e-9, s2/(u*(u**2+4*np.pi**2)), 0.0)
    val = g**2*(qf(kp)-qf(k))*u
    return np.where(np.abs(u) > 1e-9, val, 0.0)   # diagonal is a null set for GL nodes
for L in [50, 100, 200, 400]:
    t, wq = np.polynomial.legendre.leggauss(2000)
    k = L*t; wk = L*wq
    K1, K2 = np.meshgrid(k, k, indexing="ij")
    val = np.sum(np.outer(wk, wk)*integrand(K1, K2))
    print(f"  box |kappa|<={L:4d}, M=2000:  g_KM = {val:.8f}   1/6 = {1/6:.8f}   rel dev {abs(val-1/6)*6:.2e}")
# exact reduction:  g_KM = (1/2) int du I(u)/(u(u^2+4pi^2)^2),  I(u) = (2/3)u(u^2+4pi^2)
print(f"  exact reduction (1/3)*int du/(u^2+4pi^2) = {(1/3)*(1/(2*np.pi))*np.pi:.8f}")

# (I9b) exact (sigma,u) reduction:  with sigma=k+k', u=k-k',
#   int dsigma sigma^2 [q((sigma-u)/2)-q((sigma+u)/2)] = (2/3) u (u^2+4pi^2),
#   whence g_KM = (1/2) int du I(u)/(u(u^2+4pi^2)^2) = (1/3) int du/(u^2+4pi^2) = 1/6.
from scipy.integrate import quad
print("  (I9b) I(u) = int sigma^2 [q((sigma-u)/2)-q((sigma+u)/2)] dsigma  vs  (2/3)u(u^2+4pi^2):")
for u in [0.5, 1.0, 3.0, 10.0, 30.0]:
    I, err = quad(lambda x: x**2*(qf((x-u)/2)-qf((x+u)/2)), -np.inf, np.inf, limit=400)
    ex = (2.0/3.0)*u*(u**2+4*np.pi**2)
    print(f"     u={u:5.1f}:  I={I:.12e}   exact={ex:.12e}   rel {abs(I-ex)/ex:.2e}")
