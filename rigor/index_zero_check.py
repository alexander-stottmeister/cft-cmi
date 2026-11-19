#!/usr/bin/env python3
"""index_zero_check.py -- numerical instance for rigor/index_zero.tex (author R1, 2026-11-19).

Run:  ${PYTHON:-python3} rigor/index_zero_check.py > rigor/index_zero_check.out
Setting: H = l^2(Z), P+ = projection onto span{e_n : n >= 0}, P- = 1 - P+.
(0) Validation: uniform hopping h e_n = e_{n+1} + e_{n-1}: <e_m, e^{ish} e_n> = i^{m-n} J_{m-n}(2s) (exact).
(A) Instance (round 2, after REF-RP-4): K = i H, H = nearest-neighbour hopping with bond strengths 1.0 (n>=0),
    0.8 (the bond (-1,0)), 0.6 (n<=-2), next-nearest-neighbour hopping H[n,n+2] = 0.4i = conj(H[n+2,n]) for all n
    (a flux through every triangle: H is not real, U_s is not symmetric, so B = C^T does NOT hold; printed), and
    potential 0.5 (n>=0), -0.3 (n<0).  [P-,K] has rank <= 6, ||[P-,K]||_2 = sqrt(2(0.8^2+0.4^2+0.4^2)) = 1.3856;
    old range |s| < 0.7217.  What this test can and cannot do: U_s is computed as the finite unitary
    U_N = expm(i s H_N); the blocks of a finite unitary always have equal singular values, and the inner read-out
    differs from the infinite-volume blocks only by the printed truncation bound.  So (A) checks the instance up to
    truncation; it cannot detect a failure of the theorem.  The infinite-dimensional content is the index, which a
    finite unitary window cannot carry; (B) is the discriminating read-out.
(B) Negative control: U_s = multiplication by e^{is theta}, theta in (-pi,pi), in the Fourier basis:
    <e_m,U_s e_n> = sinc(s-(m-n)).  K = i theta: [P-,K] is not HS.  s = 1: the bilateral shift, index -1,
    B has singular value 1 once, C = 0.  s = 1/2: ||C||_2^2 on a window of size M grows like log M (not HS).
Discretisation: model A is computed on the window [-N, N) (exact truncated Hamiltonian, U_N = expm(i s H_N));
the blocks are read on the inner window rows/cols |n| < M.  Truncation bounds (range-2 hopping, ||H|| <= 3.3,
x = 3.3|s|): entry error of U_N vs U inside the inner window <= 2 sum_{k>=N-M} x^k/k! (a path must leave the
window and return); a dropped block entry with |m-n| = d >= M is <= sum_{k>=ceil(d/2)} x^k/k!, and at most d
dropped entries have |m-n| = d, which bounds the HS norm of the dropped part (printed).  Singular values move by
at most the HS norm of the perturbation (Mirsky); the inner-window entry error contributes <= 2M times its bound.
Tolerance (fixed before the run): TOL = 1e-10 on max_k |sigma_k(B) - sigma_k(C)| (model A) and on the
validation (0).
"""
import os, sys, math
import numpy as np
from scipy.linalg import expm, svdvals
from scipy.special import jv

TOL = 1e-10
N, M = 450, 150
S_A = [0.5, 1.5, 3.0, 4.0, -3.5]

def idx(n):            # site n in [-N, N) -> matrix index
    return n + N

def hop_uniform():
    H = np.zeros((2 * N, 2 * N))
    for n in range(-N, N - 1):
        H[idx(n), idx(n + 1)] = H[idx(n + 1), idx(n)] = 1.0
    return H

HNORM = 2 * 1.0 + 2 * 0.4 + 0.5          # Gershgorin bound on ||H_A||

def hop_A():
    H = np.zeros((2 * N, 2 * N), dtype=complex)
    for n in range(-N, N - 1):
        t = 1.0 if n >= 0 else (0.8 if n == -1 else 0.6)
        H[idx(n), idx(n + 1)] = H[idx(n + 1), idx(n)] = t
    for n in range(-N, N - 2):
        H[idx(n), idx(n + 2)] = 0.4j
        H[idx(n + 2), idx(n)] = -0.4j
    for n in range(-N, N):
        H[idx(n), idx(n)] = 0.5 if n >= 0 else -0.3
    return H

def tail(x, k0):       # sum_{k>=k0} x^k/k!, computed in logs
    tot, k = 0.0, k0
    while True:
        term = math.exp(k * math.log(x) - math.lgamma(k + 1)) if x > 0 else 0.0
        tot += term
        if term < 1e-300 or k > k0 + 2000:
            return tot
        k += 1

def blocks(U):
    rows_m = [idx(n) for n in range(-M, 0)]      # P- side, n < 0
    rows_p = [idx(n) for n in range(0, M)]       # P+ side, n >= 0
    C = U[np.ix_(rows_m, rows_p)]                # P- U P+
    B = U[np.ix_(rows_p, rows_m)]                # P+ U P-
    return B, C

def main():
    print("# index_zero_check.py output; TOL =", TOL, "; window N =", N, ", inner M =", M)
    # (0) validation
    H0 = hop_uniform()
    s = 2.7
    U = expm(1j * s * H0)
    err = 0.0
    for m in range(-60, 60):
        for n in range(-60, 60):
            exact = (1j) ** ((m - n) % 4) * jv(m - n, 2 * s)
            err = max(err, abs(U[idx(m), idx(n)] - exact))
    print("(0) validation, uniform hopping, s = 2.7: max |U_mn - i^(m-n) J_(m-n)(2s)| over |m|,|n|<60 = %.3e  %s"
          % (err, "PASS" if err < TOL else "FAIL"))
    # (A) positive instance
    HA = hop_A()
    hs_comm = math.sqrt(2 * (0.8 ** 2 + 0.4 ** 2 + 0.4 ** 2))
    assert np.allclose(HA, HA.conj().T)
    print("(A) ||[P-,K]||_2 = %.6f ; old range |s| < %.6f" % (hs_comm, 1 / hs_comm))
    allpass = True
    for s in S_A:
        U = expm(1j * s * HA)
        B, C = blocks(U)
        sB = np.sort(svdvals(B))[::-1]
        sC = np.sort(svdvals(C))[::-1]
        d = np.max(np.abs(sB - sC))
        nB2, nC2 = np.sum(sB ** 2), np.sum(sC ** 2)
        x = HNORM * abs(s)
        e1 = 2 * tail(x, N - M)            # range-2 hopping: >= (N-M) hops to reach the window edge and back
        e2 = math.sqrt(sum(d * tail(x, (d + 1) // 2) ** 2 for d in range(M, M + 4000)))  # HS of dropped part
        asym = np.max(np.abs(B - C.T))
        ok = d < TOL
        allpass &= ok
        print("(A) s = %5.2f |s|*||[P-,K]||_2 = %6.3f  ||G_s||_2^2 = ||B||_2^2+||C||_2^2 = %.12f"
              % (s, abs(s) * hs_comm, nB2 + nC2))
        print("    top sv B: %s" % np.array2string(sB[:4], precision=12))
        print("    top sv C: %s" % np.array2string(sC[:4], precision=12))
        print("    max_k |sv_k(B) - sv_k(C)| = %.3e  %s ; ||B||_2^2-||C||_2^2 = %.3e ; trunc bounds: entry %.1e, HS of dropped part %.1e"
              % (d, "PASS" if ok else "FAIL", nB2 - nC2, e1, e2))
        print("    max |B - C^T| = %.3f (transposition symmetry absent)" % asym)
    print("(A) all s:", "PASS" if allpass else "FAIL", "(instance check up to truncation; non-discriminating, see header)")
    # (B) negative control
    def Umult(s, MM):
        k = np.subtract.outer(np.arange(-MM, MM), np.arange(-MM, MM))
        return np.sinc(s - k)          # numpy sinc(x) = sin(pi x)/(pi x)
    for s in [1.0, 2.0, 0.5]:
        for MM in ([200] if s in (1.0, 2.0) else [100, 200, 400, 800]):
            U = Umult(s, MM)
            C = U[:MM, MM:]            # rows n<0, cols n>=0
            B = U[MM:, :MM]
            sB = np.sort(svdvals(B))[::-1]; sC = np.sort(svdvals(C))[::-1]
            print("(B) s = %.1f M = %4d: top sv B %s ; top sv C %s ; ||B||_2^2 = %.6f ; ||C||_2^2 = %.6f"
                  % (s, MM, np.array2string(sB[:3], precision=6), np.array2string(sC[:3], precision=6),
                     np.sum(sB ** 2), np.sum(sC ** 2)))
    for s in (1.0, 2.0):
        U = Umult(s, 200)
        print("(B) at s = %.0f: #{sv(B) > 1 - 1e-12} = %d, #{sv(C) > 1 - 1e-12} = %d  (index of P+U P+ = %d)"
              % (s, int(np.sum(svdvals(U[200:, :200]) > 1 - 1e-12)), int(np.sum(svdvals(U[:200, 200:]) > 1 - 1e-12)),
                 -int(s)))

if __name__ == "__main__":
    main()
