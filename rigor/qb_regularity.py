#!/usr/bin/env python
"""QB / O5: regularity of the first-order field g_tot of the C^{1,1} piecewise-Moebius map.

Circle coordinate theta in (-pi,pi], real line coordinate x = tan(theta/2).
A vector field g(x) d/dx equals G(theta) d/dtheta with G(theta) = 2 g(x) cos^2(theta/2).

g_tot: 0 for x <= 0 ; -x^2/L for 0 <= x <= L ; -x^2/L * chi((x-L)/(M-L)) for x >= L (chi smooth, 1->0);
0 for x >= M and across the point at infinity.  Only non-smooth point: x = 0 (jump of g'').

Checks: (1) |G_n| ~ |J|/(2 pi |n|^3) with J = G''(0+)-G''(0-) = -1/L;
        (2) ||G||_{3/2} = sum |G_n|(1+|n|^{3/2}) finite  (Carpi-Weiner class S^{3/2});
        (3) ||G'||_{3/2} divergent, partial sums ~ const * sqrt(N);
        (4) ||T(g)Om||^2 = (c/12) sum n(n^2-1)|G_n|^2 finite (homogeneous H^{3/2} = Weil-Petersson);
        (5) <L_0> of T(g)Om finite, <L_0^2> logarithmically divergent;
        (6) H^s(S^1) norm finite iff s < 5/2.
"""
import numpy as np

L, M = 1.0, 3.0

def chi(t):                      # smooth 1 -> 0 on [0,1]
    t = np.clip(t, 0.0, 1.0)
    a = np.zeros_like(t); b = np.zeros_like(t)
    m = t > 0;  a[m] = np.exp(-1.0/t[m])
    m = t < 1;  b[m] = np.exp(-1.0/(1.0-t[m]))
    return b/(a+b)

def g_of_x(x):
    out = np.zeros_like(x)
    m = (x > 0) & (x <= L);           out[m] = -x[m]**2/L
    m = (x > L) & (x < M);            out[m] = -x[m]**2/L*chi((x[m]-L)/(M-L))
    return out

def G_of_theta(th):
    c2 = np.cos(th/2.0)**2
    x = np.tan(th/2.0)
    x = np.where(np.abs(np.cos(th/2.0)) < 1e-14, np.inf, x)   # point at infinity
    out = np.zeros_like(th)
    fin = np.isfinite(x)
    out[fin] = 2.0*g_of_x(x[fin])*c2[fin]
    return out

N = 1 << 22
th = -np.pi + 2*np.pi*np.arange(N)/N
G = G_of_theta(th)
# Fourier coefficients  G_n = (1/2pi) int G e^{-i n th} dth   (trapezoid = FFT on the uniform grid)
n = np.arange(N); n = np.where(n > N//2, n-N, n)
# G_n = (1/2pi) int G e^{-i n th} dth ~= (1/N) sum_j G_j e^{-i n th_j},  th_j = -pi + 2 pi j/N,
# and e^{-i n th_j} = (-1)^n e^{-2 pi i n j/N}, so G_n = (-1)^n fft(G)[n]/N.
Gn = ((-1.0)**n)*np.fft.fft(G)/N
absG = np.abs(Gn)

J = -1.0/L
print("== (1) decay:  n^3 |G_n|  vs  |J|/(2pi) = %.6f" % (abs(J)/(2*np.pi)))
for k in [8, 32, 128, 512, 2048, 8192, 32768]:
    print("   n=%7d   n^3|G_n| = %.6f" % (k, k**3*absG[k]))

w32 = 1.0 + np.abs(n)**1.5
def partial(weights, cut):
    m = (np.abs(n) <= cut)
    return float(np.sum(weights[m]))
print("== (2) ||G||_{3/2} partial sums (should converge)")
for k in [64, 256, 1024, 4096, 16384, 65536, 262144]:
    print("   N=%7d   %.8f" % (k, partial(absG*w32, k)))
print("== (3) ||G'||_{3/2} partial sums (|G'_n| = |n||G_n|), should grow like sqrt(N)")
for k in [64, 256, 1024, 4096, 16384, 65536, 262144]:
    s = partial(np.abs(n)*absG*w32, k)
    print("   N=%7d   %.6f   ratio to sqrt(N) = %.6f" % (k, s, s/np.sqrt(k)))
nn = np.abs(n).astype(float)
wp = nn*(nn**2-1.0)*absG**2                     # (12/c)*||T(g)Om||^2 summand
print("== (4) sum n(n^2-1)|G_n|^2  = (12/c)||T(g)Om||^2  (homogeneous H^{3/2}); converges")
for k in [64, 1024, 16384, 262144]:
    print("   N=%7d   %.8f" % (k, partial(wp, k)))
print("== (5) energy moments of T(g)Om:  sum n^p * n(n^2-1)|G_n|^2 ")
for p, tag in [(1, "<L_0>   (finite)"), (2, "<L_0^2> (log divergent)")]:
    row = [partial(nn**p*wp, k) for k in [1024, 16384, 262144, 1048576]]
    print("   p=%d  %s  " % (p, tag), "  ".join("%.6f" % v for v in row))
print("== (6) H^s norms  sum (1+n^2)^s |G_n|^2 ")
for s in [2.0, 2.4, 2.5, 2.6]:
    row = [partial((1.0+nn**2)**s*absG**2, k) for k in [1024, 16384, 262144, 1048576]]
    print("   s=%.2f " % s, "  ".join("%.6f" % v for v in row))
