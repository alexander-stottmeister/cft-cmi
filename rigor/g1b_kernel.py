#!/usr/bin/env python3
"""g1b_kernel.py -- numerical check of Theorem T4 of rigor/network_second_order.tex (track G1b, Phase 6).

Reproduce (from the repository root):   ${PYTHON:-python3} rigor/g1b_kernel.py
It writes rigor/g1b_kernel.out next to itself (and echoes it).  Needs numpy, scipy, mpmath.

Quantities (c = 1, so Ghat = G):
  [T4a]  Ghat(D) = int_R rho(q) cos(qD) dq,   rho(q) = tanh(pi q) / (48 pi^2 q (1+q^2))
  [T4b]  Ghat(0) = 1/(12 pi^2) = f2
  [T4c]  dhat0(p,p') = (w(p)-w(p'))(p+p') / (2 pi (p-p')(1+(p-p')^2)),  w(p) = 1/(1+exp(-2 pi p))
  [T4cf] Ghat(D) = (1/12pi^2)[cosh(D/2) - sinh^2(D/2) log coth(|D|/4)]
               = (1/24pi^2) sum_{n>=0} exp(-a_n |D|)/(a_n (1-a_n^2)),  a_n = n + 1/2
  [T4d]  x(4-x^2)/(36 pi^2) <= Ghat <= x/(9 pi^2),  |Ghat - x/(9pi^2)| <= x^3/(36 pi^2),  x = exp(-|D|/2)
Methods (independent algorithms, no shared code beyond numpy/scipy/mpmath primitives):
  A : mpmath.quadosc on the 1-D q-integral (tanh-sinh + oscillatory tail extrapolation), at mp.dps = 20, 30, 40
  B : the 2-D integral (1/4) int int |D1(k,k')|^2/N(k,k') cos(u D/2pi) dk dk' with the KI closed form of D1,
      inner v-integral by scipy.integrate.quad (QUADPACK QAGS on [0,|u|+120]), outer u-integral by QUADPACK QAWO
      (weight='cos' on [0,1e5]; QAWF, i.e. the semi-infinite cosine rule, is used only in item V1d);
      B does NOT use the v-integral lemma (QL lem:V) nor rho(q)  [wording corrected after REF-P6-4]
  C : closed form (mpmath);  S : the series, summed by mpmath.nsum
  K : spot check of T4(c) against a direct 2-D quadrature of (2 pi)^-1 int int e^{ipy} ddot(y,y') e^{-ip'y'}
  L : first-order defect of a composite (Lemma lem:Dtot): the exact kernel (i/2pi) kappa_{Psi_s}(x,x'), kappa_phi =
      sqrt(phi'(x)phi'(y))/(phi(x)-phi(y)) - 1/(x-y) (PA lem:kernel), of Psi_s = R_{q1,s k1} o R_{q2,s k2} [o R_{q3,s k3}],
      differentiated in s at 0 by Richardson extrapolation (mpmath, 60 digits), in the y-frame with half-density factors,
      against sum_k zeta_k ddot(y - y_k, y' - y_k), zeta_k = kappa_k (1 - q_k), y_k = -log(1 - q_k)  [tolerance 1e-10 relative]
Tolerances, fixed before the run: A vs C and B vs C: 1e-8 relative to Ghat(0); C vs S: 1e-12; K: 1e-6 absolute.
Resolution statement: all quantities are continuum integrals; no operator is discretised and no regulator is used.
Truncations: B integrates v over [0, |u|+120] (neglected relative weight < 1e-21) and u over [0, 1e5] (neglected
|tail| <= (1e5)^-2/12 < 1e-11 in Ghat, from S(u) <= (2/3)u^-3, checked at the sample points of item B0);
K cuts y, y' at |y| <= 70 (kernel <= 2 e^{-35} beyond).  The q-integral of A has no cut-off (quadosc).
"""
import os, sys, math
import numpy as np
import mpmath as mp
from scipy import integrate
_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(_ROOT, 'rigor', 'g1b_kernel.out')
lines = []
def say(s=''):
    print(s, flush=True); lines.append(s)

F2 = 1.0/(12*math.pi**2)
DELTAS = [0.5, 1, 1.5, 2, 3, 4, 5, 6, 8]
TOL_Q, TOL_S, TOL_K = 1e-8, 1e-12, 1e-6

def G_closed(D):
    D = abs(mp.mpf(D))
    if D == 0: return 1/(12*mp.pi**2)
    return (mp.cosh(D/2) - mp.sinh(D/2)**2*mp.log(mp.coth(D/4)))/(12*mp.pi**2)
def G_series(D):
    D = abs(mp.mpf(D))
    return mp.nsum(lambda n: mp.exp(-(n+0.5)*D)/((n+0.5)*(1-(n+0.5)**2)), [0, mp.inf])/(24*mp.pi**2)
def rho(q):
    return mp.pi/(48*mp.pi**2) if q == 0 else mp.tanh(mp.pi*q)/(48*mp.pi**2*q*(1+q*q))
def G_A(D, dps):
    with mp.workdps(dps):
        if D == 0: return 2*mp.quad(rho, [0, 1, 10, mp.inf])
        return 2*mp.quadosc(lambda q: rho(q)*mp.cos(q*D), [0, mp.inf], omega=D)
# --- method B: 2-D integral with the KI closed form, inner v by QUADPACK QAGS, outer u by QUADPACK QAWO
def D1sqN(u, v):
    # |D1|^2/N = v^2 tanh(u/2) [sinh(u/2)/(cosh(v/2)+cosh(u/2))] / (u^2 (u^2+4pi^2)^2), from the KI closed form
    # D1 = -v sinh(u/2)/(u(u^2+4pi^2)(cosh(v/2)+cosh(u/2))) and N = cosh(u/2)/(cosh(v/2)+cosh(u/2)) (QL eq:NWuv);
    # the bracket is evaluated with exponents scaled by e^{-m}, m = max(|u|,|v|)/2 (no overflow)
    if abs(u) < 1e-7:
        return v*v/(64*math.pi**4*(1+math.cosh(v/2))) if abs(v) < 1400 else 0.0
    m = max(abs(u), abs(v))/2
    num = math.exp(u/2-m) - math.exp(-u/2-m)
    den = math.exp(v/2-m) + math.exp(-v/2-m) + math.exp(u/2-m) + math.exp(-u/2-m)
    return v*v*math.tanh(u/2)*(num/den)/(u*u*(u*u+4*math.pi**2)**2)
VPAD = 120.0     # beyond |v| = |u| + VPAD the integrand is < v^2 e^{-(|v|-|u|)/2}/(u^2(u^2+4pi^2)^2): weight < 1e-21
UCUT = 1.0e5     # outer cut: |int_UCUT^inf cos(.) S du| <= int_UCUT^inf (2/3) u^-3 du = UCUT^-2/3, i.e. < 1e-10 in Ghat
def S_v(u):
    a = abs(u); b = a + VPAD
    pts = [a] if a > 0 else None
    val, err = integrate.quad(lambda v: D1sqN(u, v), 0.0, b, points=pts, epsabs=0.0, epsrel=1e-12, limit=800)
    return 2*val          # integrand even in v
def G_B(D):
    # G = (1/4)(1/2) int du cos(uD/2pi) S(u) = (1/4) int_0^UCUT cos(uD/2pi) S(u) du  (+ tail < 1e-10, see UCUT)
    if D == 0:
        val, err = integrate.quad(S_v, 0, UCUT, points=[1, 10, 100, 1000, 10000], epsabs=1e-15, epsrel=1e-12, limit=2000)
    else:
        val, err = integrate.quad(S_v, 0, UCUT, weight='cos', wvar=D/(2*math.pi), epsabs=1e-15, epsrel=1e-12, limit=20000)
    return val/4
# --- K: direct transform of ddot
def Rt(y, yp):
    return -math.sinh(y/2)*math.sinh(yp/2)/math.sinh((y-yp)/2)**2
def dhat_direct(p, pp, Y=70.0):
    # (2pi)^-1 [ int_{y<0,y'>0} e^{ipy}(i/2pi)Rt(y,y')e^{-ip'y'} + int_{y>0,y'<0} e^{ipy}(-i/2pi)Rt(y',y)e^{-ip'y'} ],
    # Rt = R = -sinh(y/2)sinh(y'/2)/sinh^2((y-y')/2) as in KI eq:Rdef and f3_t0.kern
    def blk(sgn, re):
        def f(yp, y):
            if sgn > 0:   # y<0<y'
                ph = p*y - pp*yp; amp = Rt(y, yp)/(2*math.pi); c = 1j*amp     # ddot = (i/2pi) R, R = Rt (KI eq:Dt)
            else:         # y>0>y'
                ph = p*y - pp*yp; amp = Rt(yp, y)/(2*math.pi); c = -1j*amp    # conj((i/2pi) R(y',y))
            z = c*complex(math.cos(ph), math.sin(ph))
            return z.real if re else z.imag
        if sgn > 0: lim_y, lim_yp = (-Y, 0.0), (0.0, Y)
        else: lim_y, lim_yp = (0.0, Y), (-Y, 0.0)
        v, e = integrate.dblquad(f, lim_y[0], lim_y[1], lim_yp[0], lim_yp[1], epsabs=1e-11, epsrel=1e-10)
        return v
    tot = complex(blk(1, True) + blk(-1, True), blk(1, False) + blk(-1, False))
    return tot/(2*math.pi)
def w(p): return 1.0/(1.0+math.exp(-2*math.pi*p))
def dhat_formula(p, pp):
    if p == pp: return p/(2*math.cosh(math.pi*p)**2)
    return (w(p)-w(pp))*(p+pp)/(2*math.pi*(p-pp)*(1+(p-pp)**2))

def L_check(cfg, pts):
    """cfg: list of (q_k, zeta_k); returns max relative deviation over pts of the first-order composite kernel."""
    with mp.workdps(60):
        cs = [(mp.mpf(q), mp.mpf(z)/(1-mp.mpf(q))) for (q, z) in cfg]          # (q_k, kappa_k)
        def Psi(x, s):     # R_{q1} o R_{q2} o ... (innermost = last), returns (value, derivative)
            v, d = mp.mpf(x), mp.mpf(1)
            for (q, k) in reversed(cs):
                if v > q:
                    den = 1 + s*k*(v-q); d = d/den**2; v = q + (v-q)/den
            return v, d
        def kap(x, xp, s):
            (a, da), (b, db) = Psi(x, s), Psi(xp, s)
            return mp.sqrt(da*db)/(a-b) - 1/(mp.mpf(x)-mp.mpf(xp))
        def first(x, xp):  # Richardson: f(s) = kap/s = c1 + c2 s + c3 s^2 ...; eliminate c2, c3
            h = mp.mpf(10)**-12
            f = lambda t: kap(x, xp, t)/t
            f1, f2, f4 = f(h), f(h/2), f(h/4)
            return (8*f4 - 6*f2 + f1)/3
        worst = mp.mpf(0); rows = []
        for (y, yp) in pts:
            x, xp = 1-mp.exp(-mp.mpf(y)), 1-mp.exp(-mp.mpf(yp))
            comp = mp.sqrt((1-x)*(1-xp))*first(x, xp)          # y-kernel of the first-order defect, divided by i/2pi
            pred = mp.mpf(0)
            for (q, z) in cfg:
                yk = -mp.log(1-mp.mpf(q)); a, b = mp.mpf(y)-yk, mp.mpf(yp)-yk
                if a < 0 < b:   pred += z*Rt_mp(a, b)
                elif b < 0 < a: pred += -z*Rt_mp(b, a)                  # (i/2pi)R block and its adjoint: conj(i R) = -i R
            dev = abs(comp-pred)/max(abs(pred), mp.mpf(10)**-30); worst = max(worst, dev); rows.append((y, yp, comp, pred, dev))
        return worst, rows
def Rt_mp(y, yp):
    return -mp.sinh(y/2)*mp.sinh(yp/2)/mp.sinh((y-yp)/2)**2

if __name__ == '__main__':
    mp.mp.dps = 30
    say('# g1b_kernel.out -- produced by rigor/g1b_kernel.py (see its docstring for methods, tolerances, truncations)')
    say(f'# tolerances fixed before the run: TOL_Q={TOL_Q:g} (rel. to Ghat(0)), TOL_S={TOL_S:g}, TOL_K={TOL_K:g}')
    say('## V1 validation of the integrators on exactly known integrals (QL lem:U; Lemma lorentz)')
    with mp.workdps(30):
        I1 = mp.quad(lambda u: mp.tanh(u/2)/(u*(u*u+4*mp.pi**2)) if u != 0 else mp.mpf(1)/(8*mp.pi**2), [-mp.inf, 0, mp.inf])
        I2 = mp.quad(lambda u: mp.tanh(u/4)/(u*(u*u+4*mp.pi**2)) if u != 0 else mp.mpf(1)/(16*mp.pi**2), [-mp.inf, 0, mp.inf])
        L1 = mp.quadosc(lambda k: mp.cos(3*k)/(k*k+0.25), [-mp.inf, mp.inf], omega=3)
    say(f'V1a int tanh(u/2)/(u(u^2+4pi^2)) - 1/pi^2      = {mp.nstr(I1-1/mp.pi**2, 3)}')
    say(f'V1b int tanh(u/4)/(u(u^2+4pi^2)) - log2/pi^2   = {mp.nstr(I2-mp.log(2)/mp.pi**2, 3)}')
    say(f'V1c int cos(3k)/(k^2+1/4) - 2 pi e^(-3/2) (A)  = {mp.nstr(L1-2*mp.pi*mp.exp(-1.5), 3)}')
    Lq, _ = integrate.quad(lambda k: 2/(k*k+0.25), 0, np.inf, weight='cos', wvar=3.0)
    say(f'V1d same by QAWF (B)                          = {Lq-2*math.pi*math.exp(-1.5):.3e}')
    say('## V2 exact case Ghat(0)/f2 = 1 (T4(b))')
    a0 = {d: G_A(0, d) for d in (20, 30, 40)}
    b0 = G_B(0)
    say(f'V2 A: Ghat(0)/f2 - 1 at dps 20,30,40 = ' + ', '.join(mp.nstr(a0[d]*12*mp.pi**2-1, 3) for d in (20, 30, 40)))
    say(f'V2 B: Ghat(0)/f2 - 1                = {b0/F2-1:.3e}')
    say(f'V2 C,S: closed form/f2 - 1 = {mp.nstr(G_closed(0)*12*mp.pi**2-1,3)}, series/f2 - 1 = {mp.nstr(G_series(0)*12*mp.pi**2-1,3)}')
    say('## K kernel identity spot check: direct quadrature of the transform of ddot vs T4(c)')
    kmax = 0.0
    for (p, pp) in [(0.3, -0.2), (1.0, 0.5), (-0.7, 0.4), (0.25, 0.25), (0.1, 1.3)]:
        dd = dhat_direct(p, pp); df = dhat_formula(p, pp); dev = abs(dd-df); kmax = max(kmax, dev)
        say(f'K p={p:+.2f} p\'={pp:+.2f}  direct={dd.real:+.10f}{dd.imag:+.2e}i  formula={df:+.10f}  |dev|={dev:.2e}')
    say(f'K max |dev| = {kmax:.2e}  (tol {TOL_K:g}) -> {"PASS" if kmax < TOL_K else "FAIL"}')
    say('## L first-order defect of the composite = sum of translated single-corner defects (Lemma lem:Dtot)')
    cfgs = [[(0.0, 0.7), (1-math.exp(-1.2), 1.3)],
            [(-2.0, 0.4), (0.3, 1.1), (1-math.exp(-2.5), 0.9)]]
    pts = [(-1.0, 0.5), (0.5, -1.0), (0.4, 2.0), (-0.5, 3.0), (2.5, -0.3), (0.3, 0.9), (-3.0, -1.5), (1.0, 4.0)]
    lmax = mp.mpf(0)
    for cfg in cfgs:
        wst, rows = L_check(cfg, pts); lmax = max(lmax, wst)
        say(f'L corners (q,zeta) = {[(round(q,6), z) for (q, z) in cfg]}: max rel. dev = {mp.nstr(wst, 3)}')
        for (y, yp, c_, p_, d_) in rows:
            say(f'L   y={y:+.1f} y\'={yp:+.1f}  composite={mp.nstr(c_, 14):>22}  sum of translates={mp.nstr(p_, 14):>22}  rel={mp.nstr(d_, 2)}')
    say(f'L max relative deviation = {mp.nstr(lmax, 3)} (tol 1e-10; zero-blocks compared absolutely) -> {"PASS" if lmax < 1e-10 else "FAIL"}')
    say('## P1 production: Ghat(D)/Ghat(0) by A (dps 30, 40), B, C, S')
    say('#   D     A(dps40)              A40-A30     B-C        A40-C      S-C')
    g0 = G_closed(0); mAB = 0.0; mAC = 0.0; mBC = 0.0; mSC = 0.0; vals = {}
    for D in DELTAS:
        a30 = G_A(D, 30); a40 = G_A(D, 40); b = G_B(D); c = G_closed(D); s = G_series(D); vals[D] = c
        dA = float(abs(a40-a30)/g0); dB = float(abs(b-c)/g0); dC = float(abs(a40-c)/g0); dS = float(abs(s-c)/g0)
        mAB = max(mAB, float(abs(a40-b)/g0)); mAC = max(mAC, dC); mBC = max(mBC, dB); mSC = max(mSC, dS)
        say(f'{D:5.1f}  {mp.nstr(a40/g0, 15):>20}  {dA:9.1e}  {dB:9.1e}  {dC:9.1e}  {dS:9.1e}')
    say(f'P1 max|A-B|/Ghat(0) = {mAB:.2e}, max|A-C| = {mAC:.2e}, max|B-C| = {mBC:.2e}  (tol {TOL_Q:g}) -> '
        f'{"PASS" if max(mAB, mAC, mBC) < TOL_Q else "FAIL"};  max|S-C| = {mSC:.2e} (tol {TOL_S:g}) -> '
        f'{"PASS" if mSC < TOL_S else "FAIL"}')
    say('## D1 decay: T4(d) bounds and the rate')
    bad = 0
    for D in [0, 0.1] + DELTAS + [12, 16, 24]:
        x = mp.exp(-mp.mpf(D)/2); c = G_closed(D)
        lo = x*(4-x*x)/(36*mp.pi**2); hi = x/(9*mp.pi**2); err = abs(c - hi); eb = x**3/(36*mp.pi**2)
        ok = (lo <= c*(1+mp.mpf(10)**-25)) and (c <= hi*(1+mp.mpf(10)**-25)) and (err <= eb*(1+mp.mpf(10)**-25))
        bad += (not ok)
        say(f'D1 D={D:5.1f}  9pi^2 e^(D/2) Ghat = {mp.nstr(c*9*mp.pi**2/x, 12):>16}   '
            f'(|.-1| = {mp.nstr(abs(c*9*mp.pi**2/x-1),3)} <= x^2/4 = {mp.nstr(x*x/4,3)})  bounds {"ok" if ok else "VIOLATED"}')
    say(f'D1 bound violations: {bad}')
    Ds = np.array([4, 5, 6, 8], float); ys = np.array([float(mp.log(vals[d])) for d in (4, 5, 6, 8)])
    A = np.vstack([np.ones_like(Ds), -Ds]).T; coef, res, *_ = np.linalg.lstsq(A, ys, rcond=None)
    say(f'D2 least-squares fit log Ghat = log A - alpha D on D in {{4,5,6,8}}: alpha = {coef[1]:.6f}, '
        f'A*9pi^2 = {math.exp(coef[0])*9*math.pi**2:.6f};  T4(d): alpha = 1/2 exactly, A*9pi^2 -> 1, '
        f'fit bias from the e^(-3D/2) term predicted <= {max(math.exp(-d) for d in Ds)/4:.1e} in the log')
    say('## summary')
    say(f'SUMMARY Ghat(0)/f2 = 1 (A,B,C,S); two quadrature rules (A: mpmath quadosc; B: QUADPACK QAGS+QAWO) agree '
        f'with the closed form to max {max(mAC, mBC):.1e} relative to Ghat(0); kernel identity spot check max {kmax:.1e}')
    with open(OUT, 'w') as fh:
        fh.write('\n'.join(lines) + '\n')
