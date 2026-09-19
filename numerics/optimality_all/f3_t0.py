import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""F3 T0: the parameter-free Wiener-Hopf problem of F1 Prop 6.2 (prop:thetaframe), discretised
directly in the modular frame of I.

I=(-inf,1), A=(-inf,0), D=(0,1);  y = -log(1-x):  A -> {y<0}, D -> {y>0}.
Q = (1+e^{-2 pi p})^{-1} is the Fourier multiplier; in the piecewise-constant CELL basis of y its
matrix elements are EXACT (kkt_continuum.Qmat, Lemma "closed form of the discretised vacuum
symbol"): Q_mn = 1/2 delta_mn - (i/4 pi sqrt(h_m h_n))[F2(b_m-a_n)-F2(a_m-a_n)-F2(b_m-b_n)+F2(a_m-b_n)].

The first-order defect delta-dot = [Q,d], d = D_w, w(y) = -4 sinh^2(y/2) 1_{y>0}, has the CLOSED
FORM (derived from S11's R_s^{(1)} = (s/L) u v/(u+v)^2 in the limit a -> infinity, L = 1;
x = 1-e^{-y}, half-density factor sqrt((1-x_1)(1-x_2)) = e^{-(y_1+y_2)/2}):

    ddot(y1,y2) = -(i/2pi) sinh(y1/2) sinh(y2/2) / sinh^2((y1-y2)/2) + h.c.,   y1<0<y2,

parameter-free, with no A-D block ambiguity.  Its tail is ~ e^{y1} e^{-y2/2} as y2 -> +inf, so the
moving endpoint x=1 (y=+inf) is NOT integrable away trivially: y_max convergence must be checked.
theta = 2<beta,A^{-1}beta>/g_Q(ddot) by the CG of f3_gal.theta (identical operator algebra)."""
import sys, time, numpy as np
sys.path.insert(0,_os.path.join(_ROOT, 'numerics/optimality_all'))
from kkt_continuum import Qmat, _nodes
import f3_gal as G
f2 = 1.0/(12*np.pi**2)

def kern(y1, y2):
    return -np.sinh(y1/2.0)*np.sinh(y2/2.0)/np.sinh((y1-y2)/2.0)**2

def ddot(edges, nA, ng=10):
    N = len(edges)-1; al, be = edges[:-1], edges[1:]; hh = be-al
    nod, wei = [], []
    for m in range(N):
        g = 'right' if m == nA-1 else ('left' if m == nA else None)
        n_, w_ = _nodes(al[m], be[m], ng, graded_at=g); nod.append(n_); wei.append(w_)
    J = np.zeros((nA, N-nA))
    for m in range(nA):
        for n in range(nA, N):
            J[m, n-nA] = wei[m] @ kern(nod[m][:,None], nod[n][None,:]) @ wei[n]
        J[m,:] /= np.sqrt(hh[m])
    J /= np.sqrt(hh[nA:])[None,:]
    D = np.zeros((N,N), dtype=complex); D[:nA, nA:] = 1j/(2*np.pi)*J
    return D + D.conj().T

def mesh(h, Y, Ymax, K=0, sg=0.5):
    """uniform width h; if K>0 the two cells touching the corner y=0 are replaced by K+1
    geometrically graded cells on each side (widths h*sg^k), i.e. hp-style corner refinement."""
    nA = max(1,int(round(Y/h))); nR = max(1,int(round(Ymax/h)))
    e = h*np.arange(-nA, nR+1)
    if K>0:
        g = h*sg**np.arange(1, K+1)
        e = np.concatenate([e[e<-1e-12], -g[::-1], [0.0], g, e[e>1e-12]])
        e = np.unique(np.round(e,14)); nA = int(np.sum(e<-1e-12))
    return e, nA

def run(h=0.12, Y=8.0, Ymax=8.0, ng=10, iters=20000, tag='', K=0, sg=0.5):
    t0=time.time(); e, nA = mesh(h,Y,Ymax,K,sg); Q = Qmat(e); D = ddot(e, nA, ng)
    th, g0, k, _, _ = G.theta(Q, D, nA, iters=iters)
    print(f"{tag}T0 h={h:.4f} Y={Y:g} Ymax={Ymax:g} K={K} sg={sg} N={len(Q)} nA={nA} g/f2={g0/f2:.5f} "
          f"theta={th:.5f} cg={k} {time.time()-t0:.0f}s", flush=True)
    return th, g0/f2

if __name__=='__main__':
    job = sys.argv[1] if len(sys.argv)>1 else 'smoke'
    if job=='smoke':
        for h in (0.4,0.2,0.1): run(h=h)
    elif job=='ymax':
        for Ymax in (2,4,6,8,10,12,16,20,30):
            run(h=0.12, Y=10.0, Ymax=Ymax)
    elif job=='Y':
        for Y in (2,4,6,8,10,14,20): run(h=0.12, Y=Y, Ymax=10.0)
    elif job=='hladder':
        for h in (0.32,0.16,0.08,0.04,0.02): run(h=h, Y=10.0, Ymax=10.0)
    elif job=='hladder2':
        for h in (0.24,0.12,0.06,0.03,0.015): run(h=h, Y=10.0, Ymax=10.0)
    elif job=='grade':
        for K in (0,2,4,6,8,12,16): run(h=0.12, Y=6.0, Ymax=12.0, K=K)
    elif job=='gradeh':
        for h in (0.24,0.12,0.06,0.03): run(h=h, Y=6.0, Ymax=20.0, K=12)
    elif job=='final':
        for h in (0.24,0.12,0.06,0.03,0.02): run(h=h, Y=6.0, Ymax=20.0)
    elif job=='final2':
        for h in (0.16,0.08,0.04,0.02): run(h=h, Y=6.0, Ymax=20.0)
    elif job=='ymax2':
        for Ymax in (20,24,30,40): run(h=0.12, Y=6.0, Ymax=Ymax)
        for Ymax in (12,16,20,24,30): run(h=0.06, Y=6.0, Ymax=Ymax)
    elif job=='ng':
        for ng in (6,10,16,24): run(h=0.12, Y=10.0, Ymax=10.0, ng=ng)
