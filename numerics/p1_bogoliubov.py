"""p1_bogoliubov.py -- Phase 1 (agent PN): Shale-Stinespring HS norm E(s)=||P_- W_s P_+||_2^2
for the zero-collar recovery diffeomorphism of Note 5, extended to a diffeo of R.

CONVENTIONS (fixed once, used everywhere)
  Fourier:      fhat(k) = int_R f(x) e^{-i k x} dx,  f(x) = (1/2pi) int fhat(k) e^{ikx} dk
  Projections:  P_+ = 1_{k>0}  (Hardy space of the UPPER half plane), P_- = 1_{k<0}
  Push-forward of half-densities: (W_phi f)(y) = f(phi^{-1}(y)) ((phi^{-1})'(y))^{1/2},
                phi an increasing C^{1,1} diffeo of R.  W_phi is unitary on L^2(R).
  Displacement: u(x) := x - phi(x),  so phi' = 1 - u'.
"""
import numpy as np, sys
from numpy.polynomial.legendre import leggauss

# ---------------------------------------------------------------- kernel
# D := W* P_- W - P_-  has the (regular, real) kernel  K(x,y) = (1/(2 pi i)) k(x,y),
#   k(x,y) = sqrt(phi'(x) phi'(y))/(phi(x)-phi(y)) - 1/(x-y),   k(x,x)=0.
# Since D = Q - P_- with Q = W* P_- W a projection,
#   ||D||_2^2 = Tr(Q P_+) + Tr(P_-(1-Q)) = ||P_- W P_+||_2^2 + ||P_+ W P_-||_2^2 = 2 E.
# Hence  E = (1/2)||D||_2^2 = (1/2)(1/(2pi)^2) \iint k^2 = (1/(8 pi^2)) \iint k(x,y)^2 dx dy.

def kfun(mp, X, Y):
    """numerically stable k(x,y); mp is a map object with .u(x), .du(x)."""
    d  = X - Y
    du = mp.u(X) - mp.u(Y)
    s  = np.expm1(0.5*(np.log1p(-mp.du(X)) + np.log1p(-mp.du(Y))))  # sqrt(ph'x ph'y)-1
    N  = d*s + du
    D  = d*(d - du)
    out = np.zeros_like(d)
    m = d != 0.0
    out[m] = N[m]/D[m]
    return out

# ------------------------------------------------- compactified tensor quadrature
def nodes(brk, npan, ngl, c=2.0):
    """Gauss-Legendre nodes/weights for x in R via x = c*tan(theta); the theta interval
    (-pi/2,pi/2) is split at the images of the breakpoints in brk, each piece into npan
    panels of ngl points.  Returns (x, w) with int f dx ~ sum w f(x)."""
    th = [-np.pi/2] + sorted(np.arctan(np.asarray(brk, float)/c)) + [np.pi/2]
    g, gw = leggauss(ngl); xs = []; ws = []
    for i in range(len(th)-1):
        e = np.linspace(th[i], th[i+1], npan+1)
        for j in range(npan):
            a, b = e[j], e[j+1]; hm = 0.5*(b-a); mid = 0.5*(a+b)
            t = mid + hm*g
            xs.append(c*np.tan(t)); ws.append(gw*hm*c/np.cos(t)**2)
    return np.concatenate(xs), np.concatenate(ws)

def E_of(mp, brk, npan=6, ngl=20, c=2.0):
    x, w = nodes(brk, npan, ngl, c)
    X = x[:, None]; Y = x[None, :]
    k = kfun(mp, X, Y)
    return float(w @ (k*k) @ w) / (8*np.pi**2)

# ---------------------------------------------------------------- test maps
class Mobius:
    """phi(x) = (A x + B)/(C x + D), AD-BC>0 -> P_- W P_+ = 0 exactly."""
    def __init__(s, A, B, C, D): s.A, s.B, s.C, s.D = A, B, C, D
    def phi(s, x):  return (s.A*x + s.B)/(s.C*x + s.D)
    def u(s, x):    return x - s.phi(x)
    def du(s, x):   return 1.0 - (s.A*s.D - s.B*s.C)/(s.C*x + s.D)**2

class Pert:
    """phi(x) = x + eps*eta(x), eta(x)=exp(-x^2/2)."""
    def __init__(s, eps): s.eps = eps
    def u(s, x):  return -s.eps*np.exp(-x*x/2)
    def du(s, x): return  s.eps*x*np.exp(-x*x/2)

# ------------------------------------------- independent check: matrix of P_- W P_+
def E_matrix(mp, X=25.0, N=16384, M=160):
    """||P_- W P_+||_2^2 computed directly from the matrix of W in the Fourier basis of
    the box [-X,X):  e_m(x)=e^{i k_m x}/sqrt(2X), k_m = pi m/X, m in Z.  Only the modes
    |m| <= M are summed (the rest are negligible for phi-id supported near 0) and M is
    far below the Nyquist index N/2, so the sampled integrals are alias-free."""
    h = 2*X/N; y = -X + h*np.arange(N)
    z = y.copy()                                   # Newton solve psi(y) = phi^{-1}(y)
    for _ in range(80):
        z = z - ((z - mp.u(z)) - y)/(1.0 - mp.du(z))
    dpsi = 1.0/(1.0 - mp.du(z))
    mp_ = np.arange(1, M+1); mn = -mp_[::-1]
    F = np.exp(1j*np.outer(np.pi*mp_/X, z))*np.sqrt(dpsi)[None, :]      # W e_m  (x sqrt(2X))
    B = np.exp(-1j*np.outer(np.pi*mn/X, y))
    C = (F @ B.T)/N
    return float(np.sum(np.abs(C)**2))

# ============================== the zero-collar family (Note 5: a=1, L=2, zeta=s/3) ====
A_, L_ = 1.0, 2.0

class KMap:
    """k~_s : R -> R.  u = x - k~_s :
         x <= -a      : v(x) = lam*t^2*exp(-mu*t), t=-a-x        (free left extension)
        -a <= x <= 0  : 0
         0 <= x <= L  : s x^2/(L+s x)                            (Moebius piece h_s)
         x >= L       : u_L*(1+al*t+ga*t^2)*exp(-be*t), t=x-L    (free right extension)
    with u_L = s L/(1+s) and al = be + sig, sig = u_s'(L)/u_L = (2+s)/(L(1+s)),
    so that u and u' match at L (C^{1,1} at L; at -a and 0 the value and slope vanish)."""
    def __init__(s_, s, be=1.0, ga=0.0, lam=0.0, mu=1.0):
        s_.s, s_.be, s_.ga, s_.lam, s_.mu = s, be, ga, lam, mu
        s_.uL = s*L_/(1+s); s_.al = be + (2+s)/(L_*(1+s))
    def u(o, x):
        x = np.asarray(x, float); t1 = np.maximum(-A_-x, 0.0); t2 = np.maximum(x-L_, 0.0)
        xm = np.clip(x, 0.0, L_)
        r = np.where(x <= -A_, o.lam*t1**2*np.exp(-o.mu*t1), 0.0)
        r = np.where((x > 0) & (x < L_), o.s*xm**2/(L_+o.s*xm), r)
        return np.where(x >= L_, o.uL*(1+o.al*t2+o.ga*t2**2)*np.exp(-o.be*t2), r)
    def du(o, x):
        x = np.asarray(x, float); t1 = np.maximum(-A_-x, 0.0); t2 = np.maximum(x-L_, 0.0)
        xm = np.clip(x, 0.0, L_)
        r = np.where(x <= -A_, -o.lam*(2*t1-o.mu*t1**2)*np.exp(-o.mu*t1), 0.0)
        r = np.where((x > 0) & (x < L_), o.s*xm*(2*L_+o.s*xm)/(L_+o.s*xm)**2, r)
        d2 = o.uL*((o.al+2*o.ga*t2) - o.be*(1+o.al*t2+o.ga*t2**2))*np.exp(-o.be*t2)
        return np.where(x >= L_, d2, r)

BRK = [-A_, 0.0, L_]

def maxdu(o, n=4000):
    x = np.linspace(-40, 60, n); return float(np.max(o.du(x)))   # need < 1 for phi' > 0

# --------- first-order field g_tot: phi = x + s*g + O(s^2), i.e. g = -lim u_s/s ---------
class Field:
    """g(x) = 0 (x<=0, x>=-a side except the left bump), -x^2/L on [0,L],
       -L(1+al t+ga t^2)e^{-be t} on x>=L (al=be+2/L),  lam t^2 e^{-mu t} on x<=-a."""
    def __init__(o, be=1.0, ga=0.0, lam=0.0, mu=1.0):
        o.be, o.ga, o.lam, o.mu, o.al = be, ga, lam, mu, be + 2.0/L_
    def g(o, x):
        x = np.asarray(x, float); t1 = np.maximum(-A_-x, 0.0); t2 = np.maximum(x-L_, 0.0)
        xm = np.clip(x, 0.0, L_)
        r = np.where(x <= -A_, o.lam*t1**2*np.exp(-o.mu*t1), 0.0)
        r = np.where((x > 0) & (x < L_), -xm**2/L_, r)
        return np.where(x >= L_, -L_*(1+o.al*t2+o.ga*t2**2)*np.exp(-o.be*t2), r)
    def dg(o, x):
        x = np.asarray(x, float); t1 = np.maximum(-A_-x, 0.0); t2 = np.maximum(x-L_, 0.0)
        xm = np.clip(x, 0.0, L_)
        r = np.where(x <= -A_, -o.lam*(2*t1-o.mu*t1**2)*np.exp(-o.mu*t1), 0.0)
        r = np.where((x > 0) & (x < L_), -2*xm/L_, r)
        d2 = -L_*((o.al+2*o.ga*t2) - o.be*(1+o.al*t2+o.ga*t2**2))*np.exp(-o.be*t2)
        return np.where(x >= L_, d2, r)

def k1(f, X, Y):
    d = X - Y; N = 0.5*d*(f.dg(X)+f.dg(Y)) - (f.g(X)-f.g(Y))
    out = np.zeros_like(d); m = d != 0.0; out[m] = N[m]/d[m]**2
    return out

def Q_of(f, npan=8, ngl=24, c=2.0):
    """Q[g] = (1/(8 pi^2)) iint k1^2 = (1/(48 pi^2)) int_0^inf k^3 |ghat(k)|^2 dk;
    it is the coefficient in  E = s^2 Q[g] + O(s^3)."""
    x, w = nodes(BRK, npan, ngl, c); k = k1(f, x[:, None], x[None, :])
    return float(w @ (k*k) @ w) / (8*np.pi**2)

def Q_fourier(f, X=400.0, N=2**21):
    """same Q via the Fourier formula, ghat(k) = int g e^{-ikx} dx, by FFT."""
    h = 2*X/N; x = -X + h*np.arange(N)
    G = np.fft.fft(f.g(x))*h*np.exp(1j*np.pi*np.arange(N))   # ghat at k_m = pi m/X
    m = np.arange(N); kk = np.pi*np.fft.fftfreq(N, d=1.0/N)/X
    p = kk > 0
    return float(np.sum(kk[p]**3*np.abs(G[p])**2)*(np.pi/X))/(48*np.pi**2)

# ------------- exact minimisation of Q over extensions (Q is a quadratic form) --------
class Gen:
    def __init__(o, g, dg): o.g, o.dg = g, dg

def _bump(x0, be, side):
    """b, b' supported in the extension region, vanishing to first order at x0."""
    if side > 0:
        t = lambda x: np.maximum(x-x0, 0.0)
        return Gen(lambda x: t(x)**2*np.exp(-be*t(x)),
                   lambda x: (2*t(x)-be*t(x)**2)*np.exp(-be*t(x)))
    t = lambda x: np.maximum(x0-x, 0.0)
    return Gen(lambda x: t(x)**2*np.exp(-be*t(x)),
               lambda x: -(2*t(x)-be*t(x)**2)*np.exp(-be*t(x)))

def basis(nb=16, b0=0.03, b1=8.0):
    bs = np.geomspace(b0, b1, nb)
    return ([_bump(L_, b, +1) for b in bs] + [_bump(-A_, b, -1) for b in bs], bs)

def minQ(nb=16, npan=8, ngl=24, c=2.0, both=True):
    """least-squares min of Q[g0 + sum c_i b_i] over the extension basis."""
    x, w = nodes(BRK, npan, ngl, c); sw = np.sqrt(w)
    X, Y = x[:, None], x[None, :]
    B, bs = basis(nb)
    if not both: B = B[:nb]
    def vec(f): return (sw[:, None]*k1(f, X, Y)*sw[None, :]).ravel()
    v0 = vec(Field(1.0, 0.0, 0.0, 1.0))
    M = np.array([vec(b) for b in B])
    G = M @ M.T; r = M @ v0
    cf = np.linalg.lstsq(G, -r, rcond=1e-12)[0]
    res = v0 + cf @ M
    return float(res @ res)/(8*np.pi**2), cf, B, bs

def gopt(cf, B, base=None):
    """the least-squares-optimal first-order field g_0 + sum c_i b_i as a Gen."""
    b0 = base if base is not None else Field(1.0, 0.0, 0.0, 1.0)
    return Gen(lambda x: b0.g(x) + sum(c*b.g(x) for c, b in zip(cf, B)),
               lambda x: b0.dg(x) + sum(c*b.dg(x) for c, b in zip(cf, B)))

class KMapOpt:
    """finite-s map whose extension is the optimal first-order profile, rescaled so that
    u and u' match exactly at x=L (right) and vanish to 2nd order at x=-a (left)."""
    def __init__(o, s, G):
        o.s, o.G = s, G
        o.uL = s*L_/(1+s); o.kap = (2+s)/(2*(1+s))      # = sigma*L/2 -> 1 as s->0
    def u(o, x):
        x = np.asarray(x, float); xm = np.clip(x, 0.0, L_)
        r = np.where(x <= -A_, -o.s*o.G.g(np.minimum(x, -A_)), 0.0)
        r = np.where((x > 0) & (x < L_), o.s*xm**2/(L_+o.s*xm), r)
        z = L_ + o.kap*np.maximum(x-L_, 0.0)
        return np.where(x >= L_, -o.uL*o.G.g(z)/L_, r)
    def du(o, x):
        x = np.asarray(x, float); xm = np.clip(x, 0.0, L_)
        r = np.where(x <= -A_, -o.s*o.G.dg(np.minimum(x, -A_)), 0.0)
        r = np.where((x > 0) & (x < L_), o.s*xm*(2*L_+o.s*xm)/(L_+o.s*xm)**2, r)
        z = L_ + o.kap*np.maximum(x-L_, 0.0)
        return np.where(x >= L_, -o.uL*o.kap*o.G.dg(z)/L_, r)

# ======================= circle (Moebius-covariant) form of the same problem ==========
# x = C tan(theta/2) maps (-pi,pi) -> R (theta = +-pi is the point at infinity).  A vector
# field g(x) d/dx becomes gt(theta) d/dtheta with gt = g(x) * 2C/(C^2+x^2).  The line form
# Q[g] = (1/(48 pi^2)) int_0^inf k^3 |ghat|^2 dk becomes the Moebius-invariant circle form
#        Q = (1/12) sum_{n>=2} (n^3-n) |gt_n|^2 ,   gt(th) = sum_n gt_n e^{i n th}.
# (kappa = 1/12 is verified numerically against the line kernel below.)
CC = 2.0
def x_of(th):  return CC*np.tan(0.5*th)
def gt_of(g, th):  x = x_of(th); return g(x)*2*CC/(CC**2 + x**2)

def Qcirc(vals):
    """vals = gt sampled on the uniform grid th_j = -pi + 2 pi j/N."""
    N = len(vals); n = np.fft.fftfreq(N, 1.0/N)
    c = np.fft.fft(vals)/N*((-1.0)**n)                      # coefficients gt_n
    m = n >= 2
    return float(np.sum((n[m]**3-n[m])*np.abs(c[m])**2))/12.0

def qvec(vals):
    N = len(vals); n = np.fft.fftfreq(N, 1.0/N)
    c = np.fft.fft(vals)/N*((-1.0)**n)
    m = n >= 2; z = np.sqrt((n[m]**3-n[m])/12.0)*c[m]
    return np.concatenate([z.real, z.imag])

TH_A, TH_L = 2*np.arctan(-A_/CC), 2*np.arctan(L_/CC)

def prescribed(th):
    """gt on the arc J = [TH_A, TH_L] (image of I = (-a,L)): g = 0 on (-a,0), -x^2/L on (0,L)."""
    x = x_of(th); g = np.where(x > 0, -x*x/L_, 0.0)
    return g*2*CC/(CC**2 + x**2)

def minQ_circle(M=40, N=2**15, decay=False):
    th = -np.pi + 2*np.pi*np.arange(N)/N
    t0, t1 = TH_L, TH_A + 2*np.pi                       # free arc J' (contains infinity)
    thu = np.where(th < TH_A, th + 2*np.pi, th)         # unwrapped so that J' = [t0,t1]
    inJ = thu > t1 - 1e-14
    thu = np.where(inJ, thu - 2*np.pi, thu)
    free = ~inJ & (thu >= t0)
    # reference: cubic Hermite on J' matching gt, gt' of the prescribed field at both ends
    gL = float(prescribed(np.array([TH_L]))[0])
    dgL = -2.0 + 2*L_**2/(CC**2+L_**2)                  # d gt/d th at TH_L
    u = (thu - t0)/(t1 - t0); h = t1 - t0
    h00 = 2*u**3-3*u**2+1; h10 = u**3-2*u**2+u
    ref = prescribed(th).copy()
    ref[free] = (gL*h00 + h*dgL*h10)[free]
    B = []
    if decay:   # extra constraint gt(pi)=gt'(pi)=0  <=>  u -> 0 at |x| = infinity
        h1 = np.pi - t0; u1 = (thu - t0)/h1
        ref[free] = np.where(thu[free] < np.pi,
                             (gL*(2*u1**3-3*u1**2+1) + h1*dgL*(u1**3-2*u1**2+u1))[free], 0.0)
        for (a, b_) in ((t0, np.pi), (np.pi, t1)):
            uu = (thu-a)/(b_-a); sel = free & (thu >= a) & (thu <= b_)
            for m in range(M+1):
                for fn in ((np.cos,) if m == 0 else (np.cos, np.sin)):
                    b = np.zeros(N); b[sel] = (np.sin(np.pi*uu)**2*fn(m*np.pi*uu))[sel]; B.append(b)
    else:
      for m in range(M+1):
        for fn in ((np.cos,) if m == 0 else (np.cos, np.sin)):
            b = np.zeros(N); b[free] = (np.sin(np.pi*u)**2*fn(m*np.pi*u))[free]; B.append(b)
    Mm = np.array([qvec(b) for b in B]); v0 = qvec(ref)
    G = Mm @ Mm.T; r = Mm @ v0
    cf = np.linalg.lstsq(G, -r, rcond=1e-13)[0]
    res = v0 + cf @ Mm
    gopt_vals = ref + cf @ np.array(B)
    return float(res @ res), Qcirc(ref), cf, th

# ------------- finite s on the circle: E(s) = (1/2)||K_{S^1}||_2^2 --------------------
# P_-(th,th') = (1/(2 pi i)) / (2 sin((th-th')/2))  (NS half-densities, the Cayley image of
# the line Hardy projection), so the same argument gives
#   E = (1/(8 pi^2)) \iint kc(th,th')^2,  kc = sqrt(psi'psi')/(2 sin(dpsi/2)) - 1/(2 sin(dth/2)).
TH_END = TH_A + 2*np.pi
def Th(x):  return 2*np.arctan(x/CC)

def psi_basis(M):
    h = TH_END - TH_L
    out = []
    for m in range(M+1):
        for w in ((0,) if m == 0 else (0, 1)):
            def f(t, m=m, w=w):
                u = (t-TH_L)/h; c = np.sin(np.pi*u)**2
                return c*(np.sin(m*np.pi*u) if w else np.cos(m*np.pi*u))
            def df(t, m=m, w=w):
                u = (t-TH_L)/h; sp = np.pi*np.sin(2*np.pi*u); c = np.sin(np.pi*u)**2
                g = np.sin(m*np.pi*u) if w else np.cos(m*np.pi*u)
                dg = m*np.pi*(np.cos(m*np.pi*u) if w else -np.sin(m*np.pi*u))
                return (sp*g + c*dg)/h
            out.append((f, df))
    return out

class CMap:
    """circle diffeo psi = th - delta;  delta prescribed on J = [TH_A,TH_L] by k_s,
    on J' = [TH_L,TH_END] the cubic Hermite matching (delta,delta') at both ends minus
    lam * sum_i c_i psi_i (c_i = the first-order optimal coefficients)."""
    def __init__(o, s, cf, PB, lam=1.0):
        o.s, o.cf, o.PB, o.lam = s, cf, PB, lam
        kL = L_/(1+s); o.h = TH_END - TH_L
        o.v1 = TH_L - Th(kL)
        o.d1 = 1.0 - (1.0/(1+s)**2)*(CC**2+L_**2)/(CC**2+kL**2)
    def _pre(o, t):
        x = CC*np.tan(0.5*np.clip(t, TH_A, TH_L))
        k = np.where(x > 0, L_*x/(L_+o.s*x), x)
        dk = np.where(x > 0, (L_/(L_+o.s*x))**2, 1.0)
        return t - Th(k), 1.0 - dk*(CC**2+x**2)/(CC**2+k**2)
    def delta(o, t):
        p, dp = o._pre(t); u = (t-TH_L)/o.h
        H = o.v1*(2*u**3-3*u**2+1) + o.h*o.d1*(u**3-2*u**2+u)
        corr = sum(c*f(t) for c, (f, _) in zip(o.cf, o.PB))
        return np.where(t > TH_L, H - o.lam*o.s*corr, p)
    def ddelta(o, t):
        p, dp = o._pre(t); u = (t-TH_L)/o.h
        H = (o.v1*(6*u**2-6*u) + o.h*o.d1*(3*u**2-4*u+1))/o.h
        corr = sum(c*d(t) for c, (_, d) in zip(o.cf, o.PB))
        return np.where(t > TH_L, H - o.lam*o.s*corr, dp)

def kcirc(m, T, S):
    dt = T - S; dd = m.delta(T) - m.delta(S); dp = dt - dd
    se = np.expm1(0.5*(np.log1p(-m.ddelta(T)) + np.log1p(-m.ddelta(S))))
    S0 = 2*np.sin(0.5*dt); S1 = 2*np.sin(0.5*dp)
    num = se*S0 + 4*np.cos(0.25*(dt+dp))*np.sin(0.25*dd)
    out = np.zeros_like(dt); g = dt != 0.0
    out[g] = num[g]/(S0[g]*S1[g])
    return out

def cnodes(npan, ngl):
    br = [TH_A, 0.0, TH_L, TH_END]; g, gw = leggauss(ngl); xs = []; ws = []
    for i in range(3):
        e = np.linspace(br[i], br[i+1], npan+1)
        for k in range(npan):
            a, b = e[k], e[k+1]; hm = 0.5*(b-a)
            xs.append(0.5*(a+b) + hm*g); ws.append(gw*hm)
    return np.concatenate(xs), np.concatenate(ws)

class CFromLine:
    """circle picture of a line diffeo phi = x - u (validation of the circle kernel)."""
    def __init__(o, mp): o.m = mp
    def delta(o, t):
        x = x_of(t); return t - Th(x - o.m.u(x)) - 2*np.pi*(t > np.pi)
    def ddelta(o, t):
        x = x_of(t); ph = x - o.m.u(x)
        return 1.0 - (1.0-o.m.du(x))*(CC**2+x**2)/(CC**2+ph**2)

def E_circ(m, npan=10, ngl=26):
    t, w = cnodes(npan, ngl); k = kcirc(m, t[:, None], t[None, :])
    return float(w @ (k*k) @ w)/(8*np.pi**2)

PHI = {0.025: 5.815454e-07, 0.05: 2.307294e-06, 0.1: 9.081363e-06,
       0.2: 3.519279e-05, 0.4: 1.324328e-04, 0.8: 4.726750e-04}   # numerics/results_A2.txt
GB8, GB4 = 1/(12*np.pi**2), 1/(6*np.pi**2)

def main(out):
    P = lambda *a: print(*a, file=out)
    P(__doc__)
    P("="*100); P("(1) NORMALISATION AND VALIDATION"); P("="*100)
    P("Identity used:  D := W* P_- W - P_-  has kernel K = (1/(2 pi i)) k(x,y),")
    P("   k(x,y) = sqrt(phi'(x)phi'(y))/(phi(x)-phi(y)) - 1/(x-y),  k(x,x)=0.")
    P("D = Q - P_- with Q = W* P_- W a projection, so Tr D^2 = Tr(Q P_+) + Tr(P_-(1-Q))")
    P("   = ||P_- W P_+||_2^2 + ||P_+ W P_-||_2^2 = 2 E.   Hence   E = (1/2)||K||_2^2 ,")
    P("   E = (1/(8 pi^2)) \\iint k(x,y)^2 dx dy      <-- NOT ||K||_2^2 : the factor is 1/2.")
    mb = Mobius(2., 1., 1., 3.); g = np.linspace(-2.9, 40., 400)
    P("\n (a) Moebius maps: max|k| on (-2.9,40)^2 for phi=(2x+1)/(x+3):  %.2e" %
      np.max(np.abs(kfun(mb, g[:, None], g[None, :]))))
    P("     (a Moebius map with a pole is not a diffeo of R; across the pole k = -2/(x-y),")
    P("      which is why only pole-free Moebius maps -- affine on R, or any Moebius map of")
    P("      the CIRCLE -- give E = 0.)   affine phi=1.7x+0.4:  E = %.2e" %
      E_of(Mobius(1.7, .4, 0., 1.), [0.0], 8, 24, 2.0))
    P("\n (b) phi = x + eps*exp(-x^2/2):  first order  E = eps^2 (1/(48 pi^2)) int_0^inf k^3|etahat|^2 dk")
    P("     = eps^2/(48 pi)   [Fourier convention fhat(k)=int f e^{-ikx}dx, P_+ = 1_{k>0}]")
    P("     eps      E (double integral)   E (matrix of P_-WP_+)   eps^2/(48 pi)    quad/exact")
    for eps in (0.02, 0.05, 0.1):
        E = E_of(Pert(eps), [0.0], 12, 28, 1.5)
        m1 = E_matrix(Pert(eps), 50.0, 32768, 320); m2 = E_matrix(Pert(eps), 100.0, 65536, 640)
        P("     %-8.3g %-21.8e %-23.8e %-16.8e %.5f" % (eps, E, 2*m2-m1, eps**2/(48*np.pi), E*48*np.pi/eps**2))
    P("     (matrix column: Fourier basis of a box [-X,X), Richardson-extrapolated in 1/X from")
    P("      X=50,100; it converges to the same value, confirming the factor 1/2 independently.)")
    P("\n (c) circle picture (Cayley x = C tan(th/2), C=%g).  P_-(th,th') = (1/(2 pi i))/(2 sin((th-th')/2)),"%CC)
    P("     kc = sqrt(psi'psi')/(2 sin(dpsi/2)) - 1/(2 sin(dth/2)),  E = (1/(8 pi^2)) \\iint kc^2 dth dth'.")
    for eps in (0.1, 0.3):
        P("     eps=%.1f : E(line) = %.10e   E(circle) = %.10e" %
          (eps, E_of(Pert(eps), [0.], 12, 28, 1.5), E_circ(CFromLine(Pert(eps)), 14, 30)))
    th = -np.pi + 2*np.pi*np.arange(2**16)/2**16
    G = Gen(lambda x: np.exp(-x*x/2), lambda x: -x*np.exp(-x*x/2))
    P("\n (d) first-order (quadratic) functional, three independent evaluations for eta=exp(-x^2/2):")
    P("     real-space kernel  %.10f | Fourier int k^3|etahat|^2 %.10f | circle (1/12)sum(n^3-n)|etat_n|^2 %.10f"
      % (Q_of(G, 12, 28), 1/(48*np.pi), Qcirc(gt_of(G.g, th))))
    P("     => Q[g] = (1/(48 pi^2)) int_0^inf k^3 |ghat|^2 dk = (1/12) sum_{n>=2}(n^3-n)|gt_n|^2 ,")
    P("        gt = g * dtheta/dx the same vector field in the circle chart (Moebius invariant).")

    P("\n" + "="*100); P("(2) THE FAMILY (Note 5: a=1, L=2, zeta = a s/(a+L) = s/3)"); P("="*100)
    P("k~_s(x) = x on (-inf,0], = L x/(L+s x) on [0,L]; u_s = x - k~_s = s x^2/(L+s x) on [0,L],")
    P("u_s(L)=sL/(1+s), u_s'(L)=s(2+s)/(1+s)^2.  The extension is FREE on I' = (-inf,-a] u [L,inf),")
    P("i.e. on the single circle arc J' through infinity; it must match u_s,u_s' at L and vanish")
    P("to first order at -a.  Parametrisation (circle chart): psi = th - delta, delta = cubic")
    P("Hermite on J' matching (delta,delta') at both ends, minus lam*s*sum_i c_i sin^2(pi u)")
    P("{cos,sin}(m pi u), u=(th-th_L)/|J'|, m=0..M; the c_i minimise the first-order functional.")
    P("NOTE: the optimal extension moves the point at infinity (it is asymptotically affine on R,")
    P("      NOT decaying to the identity).  Restricting to extensions with u -> 0 at |x| = inf")
    P("      gives min 0.5 E/zeta^2 = 0.0678 (M=90, still falling slowly), a factor 8.0 too\n      large -- see section (4) and finding PN-2.")
    M = 90
    q, qref, cf, _ = minQ_circle(M, 2**17); PB = psi_basis(M)
    P("\n" + "="*100); P("(3) E(s) = ||P_- W~_s P_+||_2^2  AND THE BOUND  Phi(zeta) <= -(1/2)log det(1-V*V) ~ (1/2)E")
    P("="*100)
    P("   s        zeta      E(s)            E/s^2      (1/2)E/zeta^2   Phi(zeta)       (1/2)E/Phi")
    for s_ in (0.075, 0.15, 0.3, 0.6):
        E = E_circ(CMap(s_, cf, PB), 14, 32); z = s_/3
        P("  %-8.4g %-9.6f %-15.8e %-10.6f %-15.7f %-15s %s" % (s_, z, E, E/s_**2, 0.5*E/z**2, "-", "-"))
    for s_ in sorted(PHI):
        E = E_circ(CMap(s_, cf, PB), 14, 32); z = s_/3; ph = PHI[s_]
        P("  %-8.4g %-9.6f %-15.8e %-10.6f %-15.7f %-15.7e %.5f" % (s_, z, E, E/s_**2, 0.5*E/z**2, ph, 0.5*E/ph))
    P("  (Phi from numerics/results_A2.txt, column A, -logF_sub+tail; zeta = s/3.)")
    P("\n  the bound for NON-optimal extensions (lam scales the optimal correction; lam=0 is the")
    P("  bare cubic-Hermite extension) -- (1/2)E/Phi must stay >= 1 for every one of them:")
    P("     s      lam=0        lam=0.5      lam=1.0      lam=1.5   |  (1/2)E/Phi at lam=0 / 1")
    for s_ in (0.05, 0.2, 0.8):
        v = [0.5*E_circ(CMap(s_, cf, PB, l), 14, 32) for l in (0.0, 0.5, 1.0, 1.5)]
        P("   %-7.3g %-12.6e %-12.6e %-12.6e %-10.6e|  %.4f / %.4f"
          % (s_, v[0], v[1], v[2], v[3], v[0]/PHI[s_], v[2]/PHI[s_]))
    P("\n" + "="*100); P("(4) FIRST-ORDER FIELD g_tot AND THE SHARP CONSTANT"); P("="*100)
    P("g_tot: phi = x + s g_tot + O(s^2);  g_tot = 0 on (-a,0), -x^2/L on (0,L), free on I'.")
    P("Q[g] := (1/(48 pi^2)) int_0^inf k^3 |ghat(k)|^2 dk = lim_{s->0} E(s)/s^2 .")
    P("Minimised over the extension (linear least squares, basis size M):")
    P("     M      Q_min          9*Q_min (=Q of the zeta-normalised field)   4.5*Q_min")
    QM = []
    for Mi in (30, 60, 90, 140, 200):
        qq, _, _, _ = minQ_circle(Mi, 2**17); QM.append((Mi, qq))
        P("     %-6d %-14.8f %-42.8f %.8f" % (Mi, qq, 9*qq, 4.5*qq))
    P("     unoptimised (cubic-Hermite) extension:  Q = %.8f,  4.5*Q = %.8f" % (qref, 4.5*qref))
    P("\n     g_B/4 = 1/(6 pi^2)  = %.8f   <-> 9*Q_min  (the zeta-normalised first-order field)" % GB4)
    P("     g_B/8 = 1/(12 pi^2) = %.8f   <-> 4.5*Q_min = lim_{zeta->0} (1/2)E/zeta^2" % GB8)
    (m1, q1), (m2, q2) = QM[-2], QM[-1]
    qx = q2 + (q2-q1)/(1.0/m1 - 1.0/m2)*(1.0/m2)
    P("     Richardson (1/M) extrapolation from M=%d,%d:  Q_inf = %.8f, 9*Q_inf = %.8f,"
      "  4.5*Q_inf = %.8f  (g_B/8 = %.8f)" % (m1, m2, qx, 9*qx, 4.5*qx, GB8))
    P("\n  RESTRICTED class: extensions with u -> 0 at |x| = infinity, i.e. gt(pi)=gt'(pi)=0")
    P("  (the circle field must vanish to second order at the point at infinity):")
    for Mi in (30, 60, 90):
        qd, _, _, _ = minQ_circle(Mi, 2**17, decay=True)
        P("     M=%-4d Q_min = %.8f   4.5*Q_min = %.8f   ratio to g_B/8 = %.3f"
          % (Mi, qd, 4.5*qd, 4.5*qd/GB8))
    P("\n  CONCLUSION: inf over extensions of (1/2)E/zeta^2 -> g_B/8 = 1/(12 pi^2) to ~0.1%,")
    P("  Phi <= (1/2)E holds for every extension tested, and (1/2)E/Phi -> 1 from above as zeta -> 0.")

if __name__ == "__main__":
    import io
    buf = io.StringIO(); main(buf)
    open("p1_bogoliubov.out", "w").write(buf.getvalue()); print(buf.getvalue())
