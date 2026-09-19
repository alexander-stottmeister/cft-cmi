"""S11: EXACT root fidelity test of S10's refutation claim.

S10 (rigor/sdp_dual_certificate.tex Secs 6,7,9) finds, in the spectral NS-circle model, that
composing the zero-collar compression W_s = exp(-s Dchi) with a Bogoliubov rotation
exp(-eps G_*) supported in D lowers the SLD form g_Q by 1 - theta, theta = 0.295 (L=512),
the non-perturbative check giving the ratio 0.705 at eps/s = -1 (s10_nonpert.out).
That evidence is at the level of the (capped) quadratic form g_Q.  Here we compute the EXACT
  -log F(omega, omega^beta),  omega, omega^beta quasi-free with symbols Q = P|_I and
  Q^rec = (Wt^* P Wt)|_I,   Wt = W_s exp(-eps G_*),
by Note 5 Thm 2.1 (the quasi-free root-fidelity formula), in high precision.

Numerical method (as in numerics/fidelity_flint.py): Q = P|_I has eigenvalues exponentially
close to 0 and 1, so -log F is a huge cancellation in double precision.  We SUB-COMPRESS onto
the spectral subspace S(kc) = span{ eigenvectors of Q with |kappa| = |log((1-q)/q)| <= kc };
this is a compression, hence -log F_sub <= -log F (data processing), and -log F_sub increases
to -log F as kc -> infinity.  Both channels are compressed with the SAME S(kc), so the ratio is
computed between comparable quantities; convergence in kc is reported.
Sub-block dimensions are ~10-60, so mpmath at dps=60 is fast and safe.
"""
import sys, os, time, numpy as np, scipy.linalg as sla, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from s10_theta import setup

def model(L=512, a=2.0, Lg=1.0, alpha=3.0, uv=(0.30, 0.42)):
    """Rebuild S10's ingredients: P, Dchi, index set I, and the CG-optimal generator G_*."""
    th = 2*np.pi*np.arange(L)/L; thw = np.where(th > np.pi, th - 2*np.pi, th)
    n = np.fft.fftfreq(L, d=1.0/L); nu = n + 0.5
    F = np.fft.fft(np.eye(L), axis=0)/L; Fi = np.fft.ifft(np.eye(L), axis=0)*L
    P = Fi @ np.diag((nu > 0).astype(float)) @ F; P = 0.5*(P + P.conj().T)
    a1, a2 = uv; xx = (np.abs(nu)/L - a1)/(a2 - a1); s_ = np.clip(1 - xx, 0, 1); s_ = s_*s_*(3 - 2*s_)
    d = Fi @ np.diag(1j*nu*s_) @ F; d = 0.5*(d - d.conj().T)
    thD = 2*np.arctan(Lg); thA = -2*np.arctan(a)
    inD = (thw > 0) & (thw < thD); inA = (thw > thA) & (thw < 0); inI = inD | inA
    chi = np.zeros(L); chi[inD] = np.cos(thw[inD]) - 1.0
    t = thw.copy(); t[t < thA] += 2*np.pi; m = ~inI
    chi[m] = (np.cos(t[m]) - 1.0)*np.exp(-alpha*(t[m] - thD)**2)
    X = np.diag(chi); Dc = 0.5*(X @ d + d @ X); Dc = 0.5*(Dc - Dc.conj().T)
    I = np.where(inI)[0]; D = np.where(inD)[0]
    S = setup(L=L, a=a, Lg=Lg, alpha=alpha, uv=uv)
    u = S['u']; nu2 = S['nu2']
    def Aop(g):
        G = np.zeros((L, L), complex); G[np.ix_(D, D)] = g
        v, _ = S['riesz'](G); R = v[np.ix_(D, D)]; return 0.5*(R - R.conj().T)
    R = u[np.ix_(D, D)]; b = 0.5*(R - R.conj().T)
    x = np.zeros_like(b); r = b.copy(); p = r.copy(); rs = np.real(np.vdot(r, r))
    for k in range(80):
        Ap = Aop(p); pAp = np.real(np.vdot(p, Ap))
        if pAp <= 1e-30: break
        al = rs/pAp; x = x + al*p; r = r - al*Ap
        rs2 = np.real(np.vdot(r, r)); p = r + (rs2/rs)*p; rs = rs2
    theta = np.real(np.vdot(b, x))/nu2
    G = np.zeros((L, L), complex); G[np.ix_(D, D)] = x; G = 0.5*(G - G.conj().T)
    return dict(L=L, P=P, Dc=Dc, I=I, D=D, G=G, theta=theta, nu2=nu2)

def neglogF_sub(Q1, Q2, kc, dps=60):
    """-log F on the spectral window |kappa|<=kc of Q1 (a compression: a LOWER bound)."""
    q, U = np.linalg.eigh(Q1)
    qc = np.clip(q, 1e-300, 1 - 1e-16); kap = np.log((1 - qc)/qc)
    sel = np.abs(kap) <= kc
    V = U[:, sel]; w = q[sel]; n = len(w)
    if n == 0: return 0.0, 0
    Qt = V.conj().T @ Q2 @ V; Qt = 0.5*(Qt + Qt.conj().T)
    mp.mp.dps = dps
    M = mp.matrix(n, n)
    for i in range(n):
        for j in range(n): M[i, j] = mp.mpc(float(Qt[i, j].real), float(Qt[i, j].imag))
    E, Vm = mp.eighe(M)
    tiny = mp.mpf(10)**(-dps+10)
    qt = [min(max(mp.mpf(E[i].real if hasattr(E[i],'real') else E[i]), tiny), 1-tiny) for i in range(n)]
    g1h = [mp.sqrt(mp.mpf(float(x))/mp.mpf(float(1 - x))) for x in w]
    Wm = mp.matrix(n, n)
    for l in range(n):
        g2h = mp.sqrt(qt[l]/(1 - qt[l]))
        for i in range(n): Wm[i, l] = g1h[i]*Vm[i, l]*g2h
    tau = mp.eighe(Wm*Wm.H, eigvals_only=True)
    logF = mp.mpf(0)
    for i in range(n):
        logF += mp.log(mp.mpf(float(1 - w[i])))/2 + mp.log(1 - qt[i])/2 \
                + mp.log(1 + mp.sqrt(max(tau[i], mp.mpf(0))))
    return float(-logF), n

def gQ(Q1, Q2, cap=None):
    q, U = np.linalg.eigh(Q1); q = np.clip(q, 1e-300, 1 - 1e-16)
    w = 1.0/(q[:, None]*(1 - q)[None, :] + q[None, :]*(1 - q)[:, None])
    if cap is not None: w = np.minimum(w, cap)
    dt = U.conj().T @ (Q1 - Q2) @ U
    return float(0.25*np.sum(w*np.abs(dt)**2))

if __name__ == '__main__':
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 192
    kcs = [float(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '10,15,20,25,30').split(',')]
    slist = [float(x) for x in (sys.argv[3] if len(sys.argv) > 3 else '0.05,0.02,0.01,0.005').split(',')]
    t0 = time.time(); M = model(L=L); P = M['P']; I = M['I']; Dc = M['Dc']; G = M['G']
    Q1 = P[np.ix_(I, I)]; Q1 = 0.5*(Q1 + Q1.conj().T)
    print(f"# S11 exact-fidelity test of S10's claim.  L={L} |I|={len(I)} theta(CG)={M['theta']:.5f} "
          f"|u|^2={M['nu2']:.6f}  ({time.time()-t0:.0f}s)", flush=True)
    print(f"# window kc -> modes: " + " ".join(
        f"{kc:g}:{neglogF_sub(Q1,Q1,kc)[1]}" for kc in kcs), flush=True)
    def Qrec(s, e):
        W = sla.expm(-s*Dc) @ sla.expm(-e*G)
        R = (W.conj().T @ P @ W)[np.ix_(I, I)]; return 0.5*(R + R.conj().T)
    eg = np.concatenate([np.linspace(-2.0, 0.5, 11), np.linspace(-1.3, -0.7, 7)])
    eg = np.unique(np.round(eg, 6))
    for s in slist:
        Q0 = Qrec(s, 0.0)
        g0c = gQ(Q1, Q0, cap=1e4); g0u = gQ(Q1, Q0, cap=None)
        F0 = {kc: neglogF_sub(Q1, Q0, kc)[0] for kc in kcs}
        # eps scan on the capped form (S10's criterion) and on the exact fidelity
        rows = []
        for r in eg:
            Qe = Qrec(s, r*s)
            rows.append((r, gQ(Q1, Qe, cap=1e4), gQ(Q1, Qe, cap=None),
                         {kc: neglogF_sub(Q1, Qe, kc)[0] for kc in kcs}))
        rc = min(rows, key=lambda z: z[1]); ru = min(rows, key=lambda z: z[2])
        kcm = max(kcs); rf = min(rows, key=lambda z: z[3][kcm])
        print(f"# s={s:g}: g_Q^cap(compr)={g0c:.6e}  g_Q^unc(compr)={g0u:.6e}  "
              f"-logF(compr): " + " ".join(f"kc{kc:g}={F0[kc]:.6e}" for kc in kcs), flush=True)
        print(f"#   best eps/s on g_Q^cap: {rc[0]:+.3f} ratio={rc[1]/g0c:.4f} | "
              f"on g_Q^unc: {ru[0]:+.3f} ratio={ru[2]/g0u:.4f} | "
              f"on -logF(kc={kcm:g}): {rf[0]:+.3f} ratio={rf[3][kcm]/F0[kcm]:.4f}", flush=True)
        print(f"#   AT eps/s=-1 : ratios  g_Q^cap={[r for r in rows if r[0]==-1.0][0][1]/g0c:.4f}  "
              f"g_Q^unc={[r for r in rows if r[0]==-1.0][0][2]/g0u:.4f}  " +
              " ".join(f"-logF(kc{kc:g})={[r for r in rows if r[0]==-1.0][0][3][kc]/F0[kc]:.4f}"
                       for kc in kcs), flush=True)
        print("#   eps/s   g_Q^cap/g0     g_Q^unc/g0    " +
              "  ".join(f"-logF(kc{kc:g})/F0" for kc in kcs), flush=True)
        for r in rows:
            print(f"   {r[0]:+7.3f}  {r[1]/g0c:11.6f}  {r[2]/g0u:11.6f}   " +
                  "  ".join(f"{r[3][kc]/F0[kc]:11.6f}" for kc in kcs), flush=True)
