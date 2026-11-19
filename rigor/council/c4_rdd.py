"""C4 check N2 (own code; shares nothing with numerics/optimality_all beyond numpy/scipy): in the
parameter-free modular Wiener-Hopf frame (I = (-inf,1), y = -log(1-x), A = {y<0}, D = {y>0}; F3_RESULTS.md Sec. 3)
compute the ratio rho = ||E_D u E_D||_2^2 / ||u||_2^2 of S10 cor:maximal eq:thetalb (S10: 0.0143 in the tapered circle
model), where u = P^perp l P and S_Q(l) = Q l (1-Q) + (1-Q) l Q = -ddot (S10 cor:maximal <1>1).  Since l = E_I l E_I and
D in I:  E_D u E_D = E_D (1-Q) l Q E_D  and  ||u||^2 = Tr(l (1-Q) l Q)  (all within I).  Both are invariant under
Q -> 1-Q and under complex conjugation, so the sign conventions of Q and of i in ddot do not matter.
Q = Fourier multiplier (1+e^{-2 pi p})^{-1}: kernel (1/2) delta(y) + i/(4 pi sinh(y/2)) (PV), in the orthonormal
piecewise-constant cell basis of a uniform mesh with y = 0 on a cell edge, window [-Y, Ymax].
ddot(y1,y2) = -(i/2pi) sinh(y1/2) sinh(y2/2)/sinh^2((y1-y2)/2) for y1<0<y2, plus h.c. (F3 Sec. 3 closed form).
Validation (tolerance fixed before the run): g_Q(ddot)/f2 = (1/4) sum |ddot_ij|^2/(q_i+q_j-2q_iq_j) / f2 must match
F3's T0 value 0.95989 (h = 0.12, Y = Ymax = 10, F3_RESULTS.md Sec. 3(b)) within 1e-3; also (1/2)||u||^2 = g_Q.
Criterion: rho counts as nonzero if rho > 1e-3 at every h and changes by < 20% between the two finest h.
Run: ${PYTHON:-python3} rigor/council/c4_rdd.py > rigor/council/c4_rdd.out"""
import numpy as np
from scipy.integrate import quad
f2 = 1/(12*np.pi**2)
xg, wg = np.polynomial.legendre.leggauss(10)
def Fint(x):  # F(x) = int_0^x 2 log tanh(t/4) dt, F'' = 1/sinh(x/2)
    return quad(lambda t: 2*np.log(np.tanh(t/4)), 0, x, limit=200, epsabs=1e-14, epsrel=1e-13)[0]
def cellint_offdiag(m, h):  # int_0^h int_0^h ds dt 1/sinh((m h + s - t)/2), m >= 1
    if m == 1:
        return Fint(2*h) - 2*Fint(h)
    s = (xg+1)*h/2; w = wg*h/2
    S, Tt = np.meshgrid(s, s, indexing='ij')
    return float(np.sum(np.outer(w, w)/np.sinh((m*h + S - Tt)/2)))
def ddot_kernel(y1, y2):  # y1 < 0 < y2
    return np.sinh(y1/2)*np.sinh(y2/2)/np.sinh((y1-y2)/2)**2
def run(h, Y, Ymax, ng=8):
    nA, nD = int(round(Y/h)), int(round(Ymax/h)); N = nA+nD
    edges = h*np.arange(-nA, nD+1)
    I = np.array([0.0]+[cellint_offdiag(m, h) for m in range(1, N)])
    idx = np.subtract.outer(np.arange(N), np.arange(N))
    Q = 1j/(4*np.pi*h)*np.sign(idx)*I[np.abs(idx)] + 0.5*np.eye(N)
    xs, ws = np.polynomial.legendre.leggauss(ng)
    pts = (edges[:-1,None] + (xs[None,:]+1)*h/2); wts = np.tile(ws*h/2, (N,1))
    dd = np.zeros((N, N), complex)
    for i in range(nA):
        for j in range(nA, N):
            K = ddot_kernel(pts[i][:,None], pts[j][None,:])
            dd[i, j] = -1j/(2*np.pi)*np.sum(np.outer(wts[i], wts[j])*K)/h
    dd = dd + dd.conj().T
    q, V = np.linalg.eigh(Q)
    dt = V.conj().T @ dd @ V
    W = q[:,None] + q[None,:] - 2*np.outer(q, q)
    gQ = 0.25*np.sum(np.abs(dt)**2/W)
    l = V @ (-dt/W) @ V.conj().T
    one = np.eye(N)
    u2 = np.real(np.trace(l @ (one-Q) @ l @ Q))
    R = ((one-Q) @ l @ Q)[nA:, nA:]
    rho = np.sum(np.abs(R)**2)/u2
    herm = np.linalg.norm(R + R.conj().T)/np.linalg.norm(R)
    return dict(h=h, N=N, qmin=q.min(), qmax=q.max(), g=gQ/f2, half_u2_over_g=0.5*u2/gQ, rho=rho, herm=herm)
print("columns: h, N, spec(Q) range, g_Q(ddot)/f2, (1/2)||u||^2/g_Q, rho=||E_D u E_D||^2/||u||^2, ||R+R*||/||R||")
for h in [0.24, 0.12, 0.06, 0.03]:
    r = run(h, 10.0, 10.0)
    print(f"h={r['h']:.2f} N={r['N']} q in [{r['qmin']:.2e},{1-r['qmax']:.2e} from 1] g/f2={r['g']:.5f} "
          f"half_u2/g={r['half_u2_over_g']:.10f} rho={r['rho']:.5f} herm={r['herm']:.1e}", flush=True)
print("window scan at h = 0.06 (Y, Ymax):")
for Y, Ym in [(6.0, 10.0), (10.0, 16.0), (10.0, 20.0)]:
    r = run(0.06, Y, Ym)
    print(f"Y={Y} Ymax={Ym} g/f2={r['g']:.5f} rho={r['rho']:.5f} herm={r['herm']:.1e}", flush=True)
