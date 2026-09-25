"""PZ: windowed lower bounds for the continuum Phi(zeta)=(1/2)(-log F) at large zeta (zeta>=1); the kappa_c extrapolation (analyze_largezeta.py) is not certified.
Subcommands:
  qbox   Lam kmax dps      -- build box compression Q (mpmath) and its hp eigendecomposition; cache to .pkl
  fid    s Lam kmax eps dps-- sub-compressed Phi in the spectral window eps<w<1-eps (uses cached eig)
  fit                      -- tail fits in kappa_c and kappa_max, brackets, slopes, tables
Boxes: a=1, L=2, zeta = a*s/(a+L) = s/3.  N = 2*floor(kmax*Lam/(4 pi^2))+1.
"""
import numpy as np, mpmath as mp, sys, os, time, pickle
from flint import ctx, arb, acb, acb_mat
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
A_, L_ = 1.0, 2.0

def _quads(Lam, dps, Jmax):
    """diag_j, Ct_j for j = 0..Jmax at k_j = 2 pi j / Lam; cached on disk (reused by all kmax at this Lam).
    Uses diag(-k) = 1 - diag(k), Ct(-k) = Ct(k).  Panels: width 1 up to t=40, width 4 beyond (integrand ~ e^{-t/2})."""
    fn = os.path.join(HERE, f"quads_Lam{int(Lam)}_d{dps}.pkl")
    dg, ct = [], []
    if os.path.exists(fn):
        with open(fn, "rb") as f:
            dg, ct = pickle.load(f)
        if len(dg) > Jmax:
            return dg, ct
    mp.mp.dps = dps + 5; Lm = mp.mpf(Lam)
    e = list(range(0, min(41, int(Lam)+1))) + list(range(44, int(Lam)+1, 4))
    pts = sorted(set([mp.mpf(x) for x in e] + [Lm]))
    t0 = time.time()
    for j in range(len(dg), Jmax+1):
        kj = mp.mpf(2)*mp.pi*j/Lm
        dg.append(mp.mpf(1)/2 - mp.quad(lambda t, kj=kj: (Lm-t)*mp.sin(kj*t)/mp.sinh(t/2), pts)/(2*mp.pi*Lm))
        ct.append(mp.quad(lambda t, kj=kj: (mp.cos(kj*t)-1)/mp.sinh(t/2), pts))
        if j % 50 == 0:
            print(f"   [quad] Lam={Lam} j={j}/{Jmax} {time.time()-t0:.0f}s", flush=True)
    mp.mp.dps = dps
    with open(fn, "wb") as f:
        pickle.dump((dg, ct), f)
    return dg, ct

def _prec(dps):
    ctx.prec = int(dps*3.3219) + 40
    return ctx.prec

def Q_box_flint(Lam, kmax, dps):
    """Box compression Q of the vacuum symbol in the modular-mode basis, acb_mat, absolute-basis phase xi0=log(a/L).
    k_j = 2 pi j / Lam,  kappa_j = 2 pi k_j.  Same object as compression_box.Q_box / fidelity_hp.Q_box_mp."""
    _prec(dps)
    M = int(np.floor(kmax/(2*np.pi) * Lam/(2*np.pi))); N = 2*M+1
    dg, ct = _quads(Lam, dps, M)
    DG = [arb(mp.nstr(x, dps+5)) for x in dg]; CT = [arb(mp.nstr(x, dps+5)) for x in ct]
    twopi = 2*arb.pi(); Lm = arb(float(Lam)); xi0 = -arb(2).log()          # log(a/L) = log(1/2)
    ks = [twopi*j/Lm for j in range(-M, M+1)]
    ph = [acb(0, -(ks[i]*xi0)).exp() for i in range(N)]
    dia = [DG[abs(j)] if j >= 0 else 1-DG[abs(j)] for j in range(-M, M+1)]
    Ctl = [CT[abs(j)] for j in range(-M, M+1)]
    Q = acb_mat(N, N)
    for i in range(N):
        Q[i, i] = acb(dia[i])
        for j in range(i+1, N):
            v = (Ctl[j]-Ctl[i])*arb((-1)**(i-j))/(twopi*Lm*(ks[i]-ks[j]))
            z = acb(v)*ph[i]*ph[j].conjugate()
            Q[i, j] = z; Q[j, i] = z.conjugate()
    kap = np.array([float(2*np.pi*float(ks[i])) for i in range(N)])
    return Q, kap

def _colnorm(R, N, n):
    for c in range(n):
        s = arb(0)
        for r in range(N):
            z = R[r, c]; s += z.real**2 + z.imag**2
        s = s.sqrt()
        for r in range(N):
            R[r, c] = R[r, c]/s
    return R

def eigh_flint(Mx, n, dps, vecs=True):
    """Hermitian eigendecomposition at the ambient ctx.prec; returns (sorted arb eigenvalues, acb_mat of unit columns)."""
    if not vecs:
        E = Mx.eig(nonstop=True)
        return sorted([e.real.mid() for e in E], key=float), None
    E, R = Mx.eig(right=True, nonstop=True)
    R = R.mid(); w = [e.real.mid() for e in E]
    order = sorted(range(n), key=lambda i: float(w[i]))
    V = acb_mat(n, n)
    for c, i in enumerate(order):
        for r in range(n):
            V[r, c] = R[r, i]
    return [w[i] for i in order], _colnorm(V, n, n)

def eig_cache(Lam, kmax, dps):
    fn = os.path.join(HERE, f"qeig_Lam{int(Lam)}_k{int(kmax)}_d{dps}.pkl")
    if os.path.exists(fn):
        with open(fn, "rb") as f:
            kap, ws, Vs = pickle.load(f)
        _prec(dps); N = len(kap)
        V = acb_mat(N, N)
        for i in range(N):
            for j in range(N):
                V[i, j] = acb(arb(Vs[i][j][0]), arb(Vs[i][j][1]))
        return kap, [arb(x) for x in ws], V
    t0 = time.time(); print(f"[qbox] Lam={Lam} kmax={kmax} dps={dps}: building Q ...", flush=True)
    Q, kap = Q_box_flint(Lam, kmax, dps); N = len(kap); _prec(dps)
    print(f"[qbox]   N={N}, Q built {time.time()-t0:.0f}s; eig ...", flush=True)
    w, V = eigh_flint(Q, N, dps)
    print(f"[qbox]   done {time.time()-t0:.0f}s;  w in ({float(w[0]):.4e}, {float(w[-1]):.8f})", flush=True)
    with open(fn, "wb") as f:
        pickle.dump((kap, [x.str(40, radius=False) for x in w],
                     [[(V[i, j].real.str(40, radius=False), V[i, j].imag.str(40, radius=False))
                       for j in range(N)] for i in range(N)]), f)
    return kap, w, V

def get_D(s, Lam, kmax, ngl=12):
    fn = os.path.join(HERE, f"Dhat_exact_s{s}_Lam{int(Lam)}_k{int(kmax)}_g{ngl}.npz")
    if not os.path.exists(fn):
        import defect_matrix
        t0 = time.time(); print(f"[D] building {os.path.basename(fn)} ...", flush=True)
        defect_matrix.run(A_, L_, s, Lam, kmax, 'exact', ngl=ngl, out=fn[:-4])
        print(f"[D]   {time.time()-t0:.0f}s", flush=True)
    z = np.load(fn, allow_pickle=True)
    return z['Dhat'], z['kappa']

def fid(s, Lam, kmax, eps, dps=40):
    t0 = time.time(); kap, w, V = eig_cache(Lam, kmax, dps)
    Dh, kap2 = get_D(s, Lam, kmax); assert np.allclose(kap, kap2)
    N = len(kap); zeta = A_*s/(A_+L_)
    kcx = min(np.log((1-eps)/eps), float(kap.max()))
    dps_e = dps + int(np.ceil(2*kcx/np.log(10))) + 15; _prec(dps_e)   # dynamic range e^{2 kappa_c} in the sigma step
    keep = [i for i in range(N) if eps < float(w[i]) < 1-eps]; n = len(keep)
    P = acb_mat(N, n)
    for c, i in enumerate(keep):
        for r in range(N):
            P[r, c] = V[r, i]
    Df = acb_mat(N, N)
    for i in range(N):
        for j in range(N):
            Df[i, j] = acb(float(Dh[i, j].real), float(Dh[i, j].imag))
    S = P.conjugate().transpose()*(Df*P)
    Qs = acb_mat(n, n)
    for i in range(n):
        for j in range(n):
            Qs[i, j] = -S[i, j]
        Qs[i, i] = Qs[i, i] + acb(w[keep[i]])
    qt, U = eigh_flint(Qs, n, dps_e)
    ws = [w[i] for i in keep]
    ok = float(min(qt, key=float)) > 0 and float(max(qt, key=float)) < 1
    Wm = acb_mat(n, n)
    for l in range(n):
        g2 = (qt[l]/(1-qt[l])).sqrt()
        for i in range(n):
            Wm[i, l] = U[i, l]*acb((ws[i]/(1-ws[i])).sqrt()*g2)
    M = Wm*Wm.conjugate().transpose()        # tau = eig(M) = sigma^2; arb's eig fails here, mpmath eighe is exact
    mp.mp.dps = dps_e
    Mm = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            Mm[i, j] = mp.mpc(M[i, j].real.str(dps_e, radius=False), M[i, j].imag.str(dps_e, radius=False))
    tau = mp.eighe(Mm, eigvals_only=True)
    lf = mp.mpf(0)
    for i in range(n):
        lf += (mp.log(1-mp.mpf(ws[i].str(dps_e, radius=False)))/2 + mp.log(1-mp.mpf(qt[i].str(dps_e, radius=False)))/2
               + mp.log(1+mp.sqrt(max(tau[i], mp.mpf(0)))))
    Phi = -float(lf); kc = float(np.log((1-eps)/eps)); kc_eff = min(kc, float(kap.max()))
    line = (f"RES s={s} zeta={zeta:.5f} Lam={Lam:.0f} kmax={kmax:.0f} N={N} eps={eps:.0e} kc={kc:.2f} "
            f"kceff={kc_eff:.2f} nsub={n} dps={dps_e} t={time.time()-t0:.0f}s Phi={Phi:.7e} Phi/z2={Phi/zeta**2:.6f} "
            f"pos={ok} qtmin={float(min(qt, key=float)):.2e}")
    print(line, flush=True)
    with open(os.path.join(HERE, "largezeta_cert.raw"), "a") as f:
        f.write(line+"\n")
    return Phi

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "qbox":
        eig_cache(float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    elif cmd == "batch":
        Lam, kmax, dps = float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
        ss = [float(x) for x in sys.argv[5].split(",")]; es = [float(x) for x in sys.argv[6].split(",")]
        for s in ss:
            get_D(s, Lam, kmax)
        eig_cache(Lam, kmax, dps)
        for s in ss:
            for e in es:
                try:
                    fid(s, Lam, kmax, e, dps)
                except Exception as ex:
                    print(f"FAIL s={s} eps={e}: {type(ex).__name__} {ex}", flush=True)
