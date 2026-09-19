"""RC / certified numerics, step 1: ball-arithmetic enclosure of the box symbol Q_N.

Q_N[j,j] = 1/2 - (1/(2 pi Lam)) I_s(k_j),   I_s(k) = int_0^Lam (Lam-t) sin(k t)/sinh(t/2) dt
Q_N[j,l] = -((-1)^{j-l}/(2 pi Lam (k_j-k_l))) (C(k_j)-C(k_l)),  C(k) = int_0^Lam (cos(k t)-1)/sinh(t/2) dt
(compression_box.Q_box), then conjugated by diag(e^{-i k_j xi0}).

Only 2N one-dimensional integrals are needed.  Each is split as int_0^d + int_d^Lam:
  * [d,Lam]: python-flint acb.integral -> rigorous ball (arb's Petras algorithm with error bounds).
  * [0,d]:   sin(kt)/sinh(t/2) = 2k*sinc(kt)*[(t/2)/sinh(t/2)] = 2k(1+e), |e| <= (k d)^2/6 + d^2/24,
             (cos(kt)-1)/sinh(t/2) = -k^2 t (1+e'), |e'| <= (k d)^2/12 + d^2/24,
             giving explicit interval enclosures of the two small pieces.
Usage: python cert_qbox.py Lam kmax prec
"""
import sys, time, pickle
import numpy as np
from flint import acb, arb, ctx

def enclosures(Lam, kmax, prec=200, d=arb("1e-6")):
    ctx.prec = prec
    M = int(np.floor(kmax/(2*np.pi) * Lam/(2*np.pi)))
    js = np.arange(-M, M+1)
    kk = [arb(2)*arb.pi()*arb(int(j))/arb(Lam) for j in js]
    L = arb(Lam)
    Is, Cs = [], []
    for k in kk:
        ka = acb(k); Lc = acb(L)
        def fs(z, analytic):
            return (Lc-z)*(ka*z).sin()/(z/2).sinh()
        def fc(z, analytic):
            return ((ka*z).cos()-1)/(z/2).sinh()
        Ia = acb.integral(fs, acb(d), Lc).real
        Ca = acb.integral(fc, acb(d), Lc).real
        # small pieces on [0,d]
        e1 = (k*d)**2/6 + d**2/24
        base1 = 2*k*(L*d - d**2/2)                 # int_0^d 2k(Lam-t) dt
        Is.append(Ia + base1*arb(1, float(e1.upper())))
        e2 = (k*d)**2/12 + d**2/24
        base2 = -(k**2)*d**2/2                     # int_0^d -k^2 t dt
        Cs.append(Ca + base2*arb(1, float(e2.upper())))
    return js, kk, Is, Cs, L

def qmatrix(Lam, kmax, xi0, prec=200):
    js, kk, Is, Cs, L = enclosures(Lam, kmax, prec)
    N = len(js); twopiLam = 2*arb.pi()*L
    Q = [[acb(0) for _ in range(N)] for _ in range(N)]
    for a in range(N):
        Q[a][a] = acb(arb(1)/2 - Is[a]/twopiLam)
    for a in range(N):
        for b in range(N):
            if a == b: continue
            sgn = arb((-1)**int(js[a]-js[b]))
            Q[a][b] = acb(-sgn/(twopiLam*(kk[a]-kk[b]))*(Cs[a]-Cs[b]))
    ph = [acb(0, -k*arb(xi0)).exp() for k in kk]
    for a in range(N):
        for b in range(N):
            Q[a][b] = ph[a]*Q[a][b]*ph[b].conjugate()
    return js, kk, Q

if __name__ == "__main__":
    Lam = float(sys.argv[1]); kmax = float(sys.argv[2]); prec = int(sys.argv[3]) if len(sys.argv)>3 else 200
    a, Lint = 1.0, 1.0
    xi0 = np.log(a/Lint)
    t0 = time.time()
    js, kk, Q = qmatrix(Lam, kmax, xi0, prec)
    N = len(js)
    rad = max(float(abs(Q[i][j].real.rad())) + float(abs(Q[i][j].imag.rad())) for i in range(N) for j in range(N))
    print(f"Lam={Lam} kmax={kmax} N={N} prec={prec}  max entry radius = {rad:.3e}   ({time.time()-t0:.1f}s)")
    sys.path.insert(0, "..")
    from compression_box import Q_box
    kap = np.array([float(k)*2*np.pi for k in kk])
    Qf = Q_box(kap, Lam, xi0=xi0)
    dev = max(abs(complex(float(Q[i][j].real.mid()), float(Q[i][j].imag.mid())) - Qf[i,j]) for i in range(N) for j in range(N))
    inside = sum(1 for i in range(N) for j in range(N)
                 if Q[i][j].real.contains(arb(float(Qf[i,j].real))) and Q[i][j].imag.contains(arb(float(Qf[i,j].imag))))
    print(f"  max |Q_ball - Q_float| = {dev:.3e};  float entries inside ball: {inside}/{N*N}")
    with open(f"qball_Lam{int(Lam)}_k{int(kmax)}.pkl","wb") as f:
        pickle.dump({"js":js,"kap":kap,"mid":np.array([[complex(float(Q[i][j].real.mid()),float(Q[i][j].imag.mid())) for j in range(N)] for i in range(N)]),
                     "rad":np.array([[float(Q[i][j].real.rad())+float(Q[i][j].imag.rad()) for j in range(N)] for i in range(N)])}, f)
