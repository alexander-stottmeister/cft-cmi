#!/usr/bin/env python3
"""ref_p6_5_kernel.py -- REF-P6-5 item 6: INDEPENDENT continuum recomputation of R(Delta) = G(Delta)/G(0) (own code; no
cells, no box, no window, no eigen-decomposition, no regulator; nothing from corner_kernel.py or rigor/g1b_kernel.py).
G(Delta) = (1/4) int int dhat(p,p')^2 cos((p-p')Delta)/W(p,p') dp dp',  W = w(p)(1-w(p')) + w(p')(1-w(p)),
w(p) = 1/(1+e^{-2 pi p}), so 1/W = 1 + cosh(2 pi P)/cosh(pi q), P = (p+p')/2, q = p-p' (exact algebra, report sec. 7).
dhat = 2-D Fourier transform (1/2pi) int int e^{-ipy} D(y,y') e^{ip'y'} of the T0 kernel D = ddot (+h.c.); with u = -y,
v = y', s = u+v, d = u-v the d-integral is elementary (report sec. 7, steps <1>1-<1>4) and leaves
  dhat(p,p') = -(p+p')(S(p) - S(p'))/(4 pi^2 (1+q^2) q),  dhat(p,p) = -p S'(p)/(2 pi^2),
  S(a) = int_0^inf sin(a s)/sinh(s/2) ds  (COMPUTED NUMERICALLY: trapezoid on s = (i+1/2)k, even integrand).
check  : dhat against a brute-force 2-D Gauss-Legendre quadrature of ddot itself (no reduction) at 5 points;
         S(a) against scipy.integrate.quad (QAWF) at 6 points.
sum    : trapezoid in p on the lattice hZ (both p and p' on it), |P| <= |q|/2 + XC; q-sum h Z, |q| <= QM; tail beyond QM
         from q^3 rho(q) = c3 + c5/q^2 fitted on [QM/2, QM] (a tail model in the convergence variable, not a closed form).
Validation (exactly known case): G(0) = f2 = 1/(12 pi^2) (Theorem A). Tolerance fixed before the run: 1e-7 (brief).
Usage: $PYTHON rigor/ref_p6_5_kernel.py   (a few minutes; writes rigor/ref_p6_5_kernel.out and .npz)."""
import os, sys, time
for _v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '2'
import numpy as np
from scipy.integrate import quad
_HERE = os.path.dirname(os.path.abspath(__file__)); F2 = 1/(12*np.pi**2); TOL = 1e-7; XC = 5.0
DG = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0])
out = open(os.path.join(_HERE, 'ref_p6_5_kernel.out'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.write(s + '\n'); out.flush()

def S_table(amax, h, kfac=1.0, smax=80.0):
    """S(jh), S'(jh) for j = 0..ceil(amax/h): trapezoid on s_i = (i+1/2)k, k = kfac*2pi/(amax+10), s < smax."""
    k = kfac*2*np.pi/(amax + 10.0); s = (np.arange(int(smax/k)) + 0.5)*k; f = 1/np.sinh(s/2)
    a = h*np.arange(int(np.ceil(amax/h)) + 1); Sv = np.empty_like(a); Sd = np.empty_like(a)
    for i0 in range(0, len(a), 400):
        A = np.outer(a[i0:i0 + 400], s); Sv[i0:i0 + 400] = k*(np.sin(A) @ f); Sd[i0:i0 + 400] = k*(np.cos(A) @ (s*f))
    return a, Sv, Sd

def dhat_lat(j, jp, h, Sv, Sd):
    """dhat at p = j h, p' = jp h from the S table (S odd, S' even)."""
    p, pp = j*h, jp*h; S = lambda i: np.sign(i)*Sv[np.abs(i)]
    with np.errstate(invalid='ignore', divide='ignore'):
        d = -(p + pp)*(S(j) - S(jp))/(4*np.pi**2*(1 + (p - pp)**2)*(p - pp))
    return np.where(j == jp, -p*Sd[np.abs(j)]/(2*np.pi**2), d)

def rho_lat(h, QM, Sv, Sd):
    """rho(m h), m = 0..M: (h/4) sum_p dhat^2/W over p in hZ, |P| <= |q|/2 + XC."""
    M = int(round(QM/h)); rho = np.zeros(M + 1)
    for m in range(M + 1):
        j = np.arange(int(np.ceil(-XC/h)), int(np.floor((m*h + XC)/h)) + 1); jp = j - m; q = m*h; Pv = 0.5*(j + jp)*h
        iw = 1 + np.exp(2*np.pi*np.abs(Pv) - np.pi*q)*(1 + np.exp(-4*np.pi*np.abs(Pv)))/(1 + np.exp(-2*np.pi*q))
        rho[m] = 0.25*h*np.sum(dhat_lat(j, jp, h, Sv, Sd)**2*iw)
    return h*np.arange(M + 1), rho

def G_of(qs, rho, h, Dl):
    """G(Delta) = h[rho(0) + 2 sum rho(q) cos(q Delta)] + tail from q^3 rho = c3 + c5/q^2 on [QM/2, QM]."""
    QM = qs[-1]; sel = qs >= QM/2; c = np.linalg.lstsq(np.vstack([np.ones(sel.sum()), qs[sel]**-2]).T, qs[sel]**3*rho[sel], rcond=None)[0]
    Qt = QM + h/2; G = []; T = []
    for D in Dl:
        body = h*(rho[0] + 2*np.sum(rho[1:]*np.cos(qs[1:]*D)))
        if D == 0:
            t = 2*(c[0]/(2*Qt**2) + c[1]/(4*Qt**4))
        else:
            t = 2*quad(lambda x: c[0]/x**3 + c[1]/x**5, Qt, np.inf, weight='cos', wvar=D, limlst=200)[0]
        G.append(body + t); T.append(t)
    return np.array(G), np.array(T), c

def S_quad(a):
    """S(a) by QUADPACK, independent of the trapezoid: int_0^1 sin(as)(1/sinh(s/2) - 2/s) ds (QAWO) + 2 Si(a) + QAWF on [1, inf)."""
    from scipy.special import sici
    g = lambda s: (1/np.sinh(s/2) - 2/s) if s > 1e-4 else -s/12 + 7*s**3/2880
    return (quad(g, 0, 1, weight='sin', wvar=a, limit=500)[0] + 2*sici(a)[0]
            + quad(lambda s: 1/np.sinh(s/2), 1, np.inf, weight='sin', wvar=a, limlst=200)[0])

def Sd_quad(a):
    f = lambda s: s/np.sinh(s/2) if s > 1e-8 else 2.0
    return quad(f, 0, np.inf, weight='cos', wvar=a, limlst=200)[0] if a > 0 else quad(f, 0, 200, limit=500)[0]

def brute_dhat(p, pp, U=80.0, ngl=20):
    """dhat = -(1/2pi^2) Im int_0^U int_0^U e^{i(pu + p'v)} k(u,v) du dv by product Gauss-Legendre on panels graded
    geometrically at 0 (2^-40 ... 1) and of width 0.5 on [1, U]; k = sinh(u/2)sinh(v/2)/sinh^2((u+v)/2) written as
    e^{-(u+v)/2}(1-e^{-u})(1-e^{-v})/(1-e^{-(u+v)})^2. No use of S, of the reduction, or of any closed form."""
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    cuts = np.concatenate([[0.0], 2.0**np.arange(-40, 1), np.arange(1.5, U + 1e-9, 0.5)]); lo, hi = cuts[:-1], cuts[1:]
    x = (((lo + hi)/2)[:, None] + ((hi - lo)/2)[:, None]*xg[None, :]).ravel(); w = (((hi - lo)/2)[:, None]*wg[None, :]).ravel()
    em = -np.expm1(-x); X = x[:, None] + x[None, :]
    K = np.exp(-X/2)*em[:, None]*em[None, :]/np.expm1(-X)**2
    Kc = (w*np.exp(1j*p*x)) @ K @ (w*np.exp(1j*pp*x))          # K(p,p') = int int e^{i(pu+p'v)} k du dv
    return -Kc.imag/(2*np.pi**2), len(x)                         # dhat = -(1/2pi^2) Im K

if __name__ == '__main__':
    t0 = time.time()
    P('# ref_p6_5_kernel.out -- rigor/ref_p6_5_kernel.py (REF-P6-5, item 6); ' + time.strftime('%Y-%m-%d %H:%M'))
    P('# Quantity: R(Delta) = G(Delta)/G(0) and S(Delta) = G(Delta)/f2, continuum (infinite line, modular frame of the T0 kernel).')
    P('# Resolved: all (p, p\') with |q| <= QM on the lattice hZ^2 (trapezoid, error ~ G(2 pi/h - Delta) + e^{-pi/h}); cut off:')
    P('# |q| > QM (replaced by the tail model, printed), |P| > |q|/2 + 5 (weight < e^{-10 pi}). Tolerance 1e-7 (fixed before the run).')
    tabs = {}
    for h in (0.1, 0.05):
        tabs[h] = S_table(1010.0, h); P(f'S table h = {h}: {len(tabs[h][0])} values, {time.time() - t0:.0f}s')
    a, Sv, Sd = tabs[0.1]; _, Sv2, Sd2 = S_table(1010.0, 0.1, kfac=0.5, smax=90.0)
    P(f'(i) trapezoid self-check (k -> k/2, smax 80 -> 90): max|dS| = {np.abs(Sv - Sv2).max():.1e}, max|dS\'| = {np.abs(Sd - Sd2).max():.1e}')
    for j in (1, 7, 32, 175, 2503, 10000):
        sq, dq = S_quad(a[j]), Sd_quad(a[j])
        P(f'    a = {a[j]:7.1f}: S trap {Sv[j]:.15f}  QUADPACK {sq:.15f}  |diff| {abs(Sv[j] - sq):.1e};  S\' trap {Sd[j]:+.3e}'
          f' QUADPACK {dq:+.3e} |diff| {abs(Sd[j] - dq):.1e};  diagnostic |S - pi tanh(pi a)| = {abs(Sv[j] - np.pi*np.tanh(np.pi*a[j])):.1e}')
    for (j, jp) in ((3, -7), (11, 4), (-20, 15), (5, 5), (25, -25), (0, 9)):
        b, n = brute_dhat(j*0.1, jp*0.1); m = float(dhat_lat(np.array([j]), np.array([jp]), 0.1, Sv, Sd)[0])
        P(f'(ii) dhat({j*0.1:+.1f},{jp*0.1:+.1f}): reduced {m:+.15e}  brute 2-D ({n} nodes/dim) {b:+.15e}  |diff| {abs(m - b):.1e}')
    res = {}
    for (h, QM) in ((0.1, 500.0), (0.1, 1000.0), (0.05, 1000.0)):
        qs, rho = rho_lat(h, QM, tabs[h][1], tabs[h][2]); G, T, c = G_of(qs, rho, h, DG); res[(h, QM)] = G
        P(f'(iii) h = {h}, QM = {QM:.0f}: tail model q^3 rho -> c3 = {c[0]:.8f} (c5 = {c[1]:+.5f}; diagnostic 1/(48 pi^2) = '
          f'{1/(48*np.pi**2):.8f}); G(0)/f2 - 1 = {G[0]/F2 - 1:+.2e} (tail {T[0]/F2:.2e} of f2)  {time.time() - t0:.0f}s')
        P('      Delta: ' + ' '.join(f'{d:4.1f}' for d in DG[1:]))
        P('      R    : ' + ' '.join(f'{x:.9f}' for x in G[1:]/G[0]))
        P('      G/f2 : ' + ' '.join(f'{x:.9f}' for x in G[1:]/F2))
        P('      tail : ' + ' '.join(f'{x/F2:+.0e}' for x in T[1:]))
    A, B, C = res[(0.1, 500.0)], res[(0.1, 1000.0)], res[(0.05, 1000.0)]
    P(f'(iv) max|dR| QM 500 -> 1000: {np.abs(A/A[0] - B/B[0]).max():.1e};  h 0.1 -> 0.05: {np.abs(B/B[0] - C/C[0]).max():.1e};'
      f'  max|R - G/f2| at the finest: {np.abs(C/C[0] - C/F2)[1:].max():.1e}  (tolerance 1e-7)')
    import re
    g1b = {float(m.group(1)): float(m.group(2)) for m in (re.match(r'\s+([0-9.]+)\s+([0-9.]+)\s+\S+\s+\S+\s+\S+\s+\S+\s*$', l)
           for l in open(os.path.join(_HERE, 'g1b_kernel.out'))) if m}
    T3 = {}
    for l in open(os.path.join(_HERE, '..', 'numerics', 'networks', 'kernel_decay.out')):
        m = re.match(r'\s*([0-9.]+)\s+\+([0-9.]+) \(([0-9.]+)\)\s+\+([0-9.]+) \(([0-9.]+)\)', l)
        if m and float(m.group(1)) > 0:
            T3[float(m.group(1))] = [float(m.group(k)) for k in range(2, 6)]
    AG = [(0.8984, 3e-4), (0.7457, 2e-4), (0.6008, 3e-4), (0.4770, 3e-4), (0.2946, 3e-4), (0.1798, 2e-4), (0.1093, 2e-4),
          (0.06638, 1.1e-4), (0.02443, 6e-5)]                      # card corner-kernel-two-frames, transcribed
    CT = [(0.89844, 11e-5), (0.74573, 14e-5), (0.60090, 16e-5), (0.47713, 16e-5), (0.29468, 15e-5), (0.17991, 13e-5),
          (0.10939, 10e-5), (0.066415, 74e-6), (0.024448, 37e-6)]  # card corner-kernel-t0-frame, transcribed
    CB = [(0.89835, 19e-5), (0.745633, 47e-6), (0.600737, 21e-6), (0.476965, 19e-6), (0.294525, 10e-6), (0.1797849, 55e-7),
          (0.1092993, 23e-7), (0.0663499, 5e-7), (0.0244192, 3e-7)]  # card corner-kernel-box-frame, transcribed
    P('(v) three-way table, R_mine = h 0.05, QM 1000 (full precision); g1b = rigor/g1b_kernel.out P1 A(dps40) (refereed);')
    P('    Delta  R_mine            mine-g1b   agreed(G3)-mine [inside?]  R_T0(card)-mine [inside?]  S_box(card)-mine [inside?]')
    Rm = C/C[0]
    for i, d in enumerate(DG[1:]):
        r = Rm[i + 1]; (av, au) = AG[i]; (rt, ut), (sb, ub) = CT[i], CB[i]
        P(f'    {d:4.1f}  {r:.12f}  {r - g1b[d]:+.1e}   {av - r:+.1e} [{"yes" if abs(av - r) <= au else "NO"}]'
          f'          {rt - r:+.1e} [{"yes" if abs(rt - r) <= ut else "NO"}]      {sb - r:+.1e} [{"yes" if abs(sb - r) <= ub else "NO"}]')
    np.savez(os.path.join(_HERE, 'ref_p6_5_kernel.npz'), D=DG, R=C/C[0], S=C/F2, R_h01=B/B[0], R_Q500=A/A[0])
    P(f'saved rigor/ref_p6_5_kernel.npz  total {time.time() - t0:.0f}s')
