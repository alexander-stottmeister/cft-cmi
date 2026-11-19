#!/usr/bin/env python3
"""Council seat C2: independent checks of the Theorem-B constant chain (c = 1 throughout).

Run from the repository root:  ${PYTHON:-python3} rigor/council/c2_gB_check.py > rigor/council/c2_gB_check.out

(V)  Validation on an exactly known case: f(x) = exp(-x^2) on the line,
     ||T(f)Omega||^2 = (1/48 pi^2) int_0^inf p^3 |f^(p)|^2 dp = 1/(24 pi)  (closed form, f^ = sqrt(pi) e^{-p^2/4}),
     against the circle normalisation of implementation_C11.tex thm:reg(f): (1/12) sum_{n>=2} n(n^2-1)|G_n|^2,
     G(theta) = 2 f(tan(theta/2))/(1+tan^2(theta/2)).  Tolerance (fixed before the run): rel. 1e-9.
(A)  ||T(g_tot)Omega||^2 for the field of universality_theorem_B.tex eq:chi (L = 1), by two algorithms:
     (A1) direct Gauss-Legendre Fourier quadrature on the line + analytic p^-3 tail;
     (A2) FFT on the circle (C11 normalisation) + analytic n^-3 tail.  Tolerance: rel. 1e-6.
     Direction ledger: dist(a, H_M')^2 <= ||a||^2, so ||a||^2 >= gB/4 = 1/(6 pi^2) is NECESSARY for gB = 2/(3pi^2).
(B)  Rayleigh-Ritz upper bounds U_N >= inf_h ||T(g_tot + h)Omega||^2 over h supported in I' = (1, inf)
     (theta in (pi/2, pi)), basis h_j = w(theta) T_j(t), w = (theta-pi/2)^2 (pi-theta)^2, T_j Chebyshev.
     Rigorous inequality (UB Prop. H2 / lem:gauge(1)): inf_h >= gB/4.  Hence U_N < (1 - 1e-6)/(6 pi^2) for any N
     would REFUTE gB = 2c/(3 pi^2); U_N >= 1/(6pi^2) is consistent only (it proves nothing).
Modes: circle Fourier modes 2 <= n <= NMAX resolved; n > NMAX added by the analytic tail |G_n| ~ |J|/(2 pi n^3).
"""
import numpy as np
from scipy.special import roots_legendre

PI = np.pi
TARGET = 1.0 / (6 * PI**2)          # gB/4 at c = 1 claimed by thm:value
M = 2**18                            # FFT grid on the circle
NMAX = M // 16                       # modes kept from the FFT


def beta(y):
    y = np.asarray(y, float)
    out = np.where(y <= 0, 1.0, 0.0)
    m = (y > 0) & (y < 1)
    psi = lambda t: np.exp(-1.0 / t)
    ym = y[m]
    out[m] = psi(1 - ym) / (psi(1 - ym) + psi(ym))
    return out


def g_tot(x):
    x = np.asarray(x, float)
    return np.where(x > 0, -(x**2) * beta(x - 1.0), 0.0)


def circle_coeffs(fline):
    th = -PI + 2 * PI * np.arange(M) / M
    with np.errstate(over='ignore', invalid='ignore'):
        x = np.tan(th / 2)
        G = 2 * fline(x) / (1 + x**2)
    G[~np.isfinite(G)] = 0.0
    c = np.fft.fft(G) / M * np.exp(1j * np.arange(M) * PI)  # shift theta origin to -pi
    return c[:NMAX + 1]


def circle_norm2(c, tailJ=0.0):
    n = np.arange(len(c))
    w = n * (n**2 - 1.0) / 12.0
    s = np.sum(w[2:] * np.abs(c[2:])**2)
    tail = (tailJ**2 / (4 * PI**2)) / 12.0 * (1.0 / (2 * NMAX**2))  # sum_{n>NMAX} n^3 * J^2/(4pi^2 n^6) / 12
    return s + tail


def line_norm2_gtot(P=4000.0, npts=6000):
    xg, wg = roots_legendre(npts)
    xs, ws = [], []
    for a, b in ((0.0, 1.0), (1.0, 2.0)):
        xs.append(0.5 * (b - a) * xg + 0.5 * (a + b)); ws.append(0.5 * (b - a) * wg)
    xs = np.concatenate(xs); ws = np.concatenate(ws); gv = g_tot(xs)
    p, wp = roots_legendre(20000)
    p = 0.5 * P * (p + 1); wp = 0.5 * P * wp
    gh = np.array([np.sum(ws * gv * np.exp(-1j * pk * xs)) for pk in p])
    core = np.sum(wp * p**3 * np.abs(gh)**2)
    tail = 4.0 * 0.5 / P**2              # |g^| ~ |jump g''| / p^3 = 2/p^3  ->  int_P^inf p^3 4/p^6
    return (core + tail) / (48 * PI**2)


def main():
    print("# c2_gB_check.py  (c = 1; circle grid M = %d, modes n <= %d resolved, tail analytic)" % (M, NMAX))
    exact = 1.0 / (24 * PI)
    cv = circle_norm2(circle_coeffs(lambda x: np.exp(-x**2)))
    print("(V) exp(-x^2): circle %.15f  exact 1/(24pi) %.15f  rel.dev %.2e  tol 1e-9  %s"
          % (cv, exact, abs(cv / exact - 1), "PASS" if abs(cv / exact - 1) < 1e-9 else "FAIL"))
    cg = circle_coeffs(g_tot)
    a2 = circle_norm2(cg, tailJ=1.0)
    a1 = line_norm2_gtot()
    print("(A1) line quadrature ||T(g_tot)Om||^2 = %.10f" % a1)
    print("(A2) circle FFT      ||T(g_tot)Om||^2 = %.10f   rel.dev %.2e  tol 1e-6  %s"
          % (a2, abs(a1 / a2 - 1), "PASS" if abs(a1 / a2 - 1) < 1e-6 else "FAIL"))
    print("     ratio ||a||^2 / (gB/4 claimed = 1/(6pi^2) = %.10f) = %.6f  (must be >= 1)" % (TARGET, a2 / TARGET))
    th = -PI + 2 * PI * np.arange(M) / M
    tt = (th - 0.75 * PI) / (0.25 * PI)
    inside = (th > PI / 2) & (th < PI)
    wgt = np.where(inside, (th - PI / 2)**2 * (PI - th)**2, 0.0)
    shift = np.exp(1j * np.arange(M) * PI)
    n = np.arange(NMAX + 1); wn = np.where(n >= 2, n * (n**2 - 1.0) / 12.0, 0.0)
    print("(B) Rayleigh-Ritz upper bounds U_N on inf_h ||T(g_tot+h)Om||^2 ; claimed limit 1/(6pi^2) = %.10f" % TARGET)
    for N in (16, 32, 48, 64, 96, 128):
        H = []
        for j in range(N):
            Tj = np.cos(j * np.arccos(np.clip(tt, -1, 1)))
            H.append((np.fft.fft(wgt * Tj) / M * shift)[:NMAX + 1])
        H = np.array(H)
        sw = np.sqrt(wn)
        A = np.concatenate([(sw * H.real).T, (sw * H.imag).T])
        y = -np.concatenate([sw * cg.real, sw * cg.imag])
        coef, _, rk, sv = np.linalg.lstsq(A, y, rcond=1e-13)
        ev = sv**2
        tot = cg + coef @ H
        UN = circle_norm2(tot, tailJ=1.0)
        flag = "REFUTES" if UN < TARGET * (1 - 1e-6) else "consistent"
        print("    N = %2d  U_N = %.10f  U_N/target = %.6f  cond = %.1e  %s"
              % (N, UN, UN / TARGET, ev.max() / ev.min(), flag))


if __name__ == "__main__":
    main()
