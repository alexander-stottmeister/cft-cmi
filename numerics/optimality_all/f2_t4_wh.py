"""F2/T4: the F1 Thm 4.4 KKT criterion in the PARAMETER-FREE modular Wiener-Hopf frame
(F1 Prop 6.2, discretised by F3 in f3_t0.py), where Moebius rigidity is EXACT:
deltadot is exactly A-D off-diagonal (no DD/AA blocks at all), unlike the spectral circle
model of T2 (which violates rigidity at O(1/L) and weights the spurious blocks by w).

Frame: I = (-inf,1), y = -log(1-x), A = {y<0} (cells 0..nA-1), D = {y>0} (cells nA..N-1).
Q from kkt_continuum.Qmat (exact cell matrix elements), deltadot from f3_t0.ddot (closed form).
theta and the optimal rotation from f3_gal.theta (CG); with that routine's normalisation the
minimiser is G_* = -2x, delta_* = deltadot + [Q, G_*], g_Q(delta_*) = (1-theta) g_Q(deltadot).

F1 normalisation: t_* = U (w o delta~_*) U^H, g_Q(delta_*) = (1/4) Tr(t_* delta_*);
tau_* = E_D t_* E_D;  M_* = Herm((t_* Q)_DD) = Herm(t_DD Q_DD) + Herm(t_DA Q_AD).
CRITERION: orbit = global optimum of the tangent problem  <=>  M_* >= 0 and M_* - tau_* >= 0.
Usage:  f2_t4_wh.py h1,h2,.. [Y] [Ymax] [cap]
"""
import sys, time, numpy as np
sys.path.insert(0, '/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/optimality_all')
from kkt_continuum import Qmat
import f3_t0 as T0
import f3_gal as FG

f2 = 1.0/(12*np.pi**2)


def build(h, Y, Ymax, ng=10, iters=20000, cap=0.0):
    e, nA = T0.mesh(h, Y, Ymax)
    Q = Qmat(e); Dc = T0.ddot(e, nA, ng); N = len(Q)
    th, g0, k, _, x = FG.theta(Q, Dc, nA, iters=iters)
    Gs = -2.0*x                                   # f3_gal's CG returns x with G_* = -2x
    emb = np.zeros((N, N), complex); emb[nA:, nA:] = Gs
    dstar = Dc + (Q@emb - emb@Q); dstar = 0.5*(dstar + dstar.conj().T)
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1-1e-16)
    w = 1.0/(q[:, None]*(1-q)[None, :] + q[None, :]*(1-q)[:, None])
    if cap > 0:
        w = np.minimum(w, cap)
    gQ = lambda Z: 0.25*float(np.sum(w*np.abs(U.conj().T@Z@U)**2))
    t = U@(w*(U.conj().T@dstar@U))@U.conj().T; t = 0.5*(t + t.conj().T)
    ctr = 0.5*(e[:-1] + e[1:])
    return dict(e=e, ctr=ctr, nA=nA, N=N, Q=Q, Dc=Dc, dstar=dstar, U=U, q=q, w=w, t=t,
                theta=th, g0=g0, gstar=gQ(dstar), gQ=gQ, cg=k, h=h, Y=Y, Ymax=Ymax, cap=cap)


def noise(S, N1, Y1):
    nA, N, Q = S['nA'], S['N'], S['Q']
    QDD = Q[nA:, nA:]; QDA = Q[nA:, :nA]
    nz = np.zeros((N, N), complex)
    nz[nA:, nA:] = 0.5*(N1@QDD + QDD@N1) - Y1
    B = 0.5*N1@QDA
    nz[nA:, :nA] = B; nz[:nA, nA:] = B.conj().T
    return 0.5*(nz + nz.conj().T)


def run(h, Y=10.0, Ymax=10.0, ng=10, iters=20000, cap=0.0, fd=True, seed=0):
    t0 = time.time(); S = build(h, Y, Ymax, ng, iters, cap)
    nA, N, t, Q = S['nA'], S['N'], S['t'], S['Q']
    g0, gs = S['g0'], S['gstar']
    tQ = (t@Q)[nA:, nA:]
    Ms = 0.5*(tQ + tQ.conj().T); anti = 0.5*(tQ - tQ.conj().T)
    tau = t[nA:, nA:]; tau = 0.5*(tau + tau.conj().T)
    eM = np.linalg.eigvalsh(Ms); eMt = np.linalg.eigvalsh(Ms - tau); nM = np.abs(eM).max()
    sldid = 0.25*np.real(np.trace(t@S['dstar']))/gs
    kap = np.log((1-S['q'][0])/S['q'][0])
    print(f"h={h:.4f} Y={Y:g} Ymax={Ymax:g} N={N} nA={nA} cap={cap:.0e}: g/f2={g0/f2:.5f} "
          f"theta={S['theta']:.5f} g(d_*)/g0={gs/g0:.6f} (1-theta={1-S['theta']:.6f}) cg={S['cg']} "
          f"| SLD id={sldid:.10f} kappa_max={kap:.2f} max w={S['w'].max():.3e} "
          f"|dc_DD|={np.linalg.norm(S['Dc'][nA:, nA:]):.1e}", flush=True)
    print(f"   lam_min(M_*)     = {eM.min():+.6e} = {eM.min()/g0:+.4e} g0 = {eM.min()/nM:+.4e} ||M||"
          f"   lam_max(M_*)={eM.max():+.6e}", flush=True)
    print(f"   lam_min(M_*-tau) = {eMt.min():+.6e} = {eMt.min()/g0:+.4e} g0 = {eMt.min()/nM:+.4e} ||M||"
          f"   lam(tau) in [{np.linalg.eigvalsh(tau).min():+.3e},{np.linalg.eigvalsh(tau).max():+.3e}]", flush=True)
    print(f"   ||AntiHerm((t Q)_DD)||/||M_*|| = {np.linalg.norm(anti)/nM:.3e}   "
          f"CRITERION (M>=0 and M-tau>=0): {(eM.min() >= 0) and (eMt.min() >= 0)}", flush=True)
    if fd:                                        # F1's derivative formula, finite differences
        rng = np.random.default_rng(seed); m = N-nA
        A1 = rng.normal(size=(m, m)) + 1j*rng.normal(size=(m, m)); N1 = 0.5*(A1+A1.conj().T)
        B1 = rng.normal(size=(m, m)) + 1j*rng.normal(size=(m, m)); Y1 = 0.5*(B1+B1.conj().T)
        eta = noise(S, N1, Y1); ep = 1e-6*np.linalg.norm(S['dstar'])/max(np.linalg.norm(eta), 1e-300)
        num = (S['gQ'](S['dstar']+ep*eta) - S['gQ'](S['dstar']-ep*eta))/(2*ep)
        pred = 0.5*(np.real(np.trace(N1@Ms)) - np.real(np.trace(Y1@tau)))
        print(f"   FD check: d g_Q = {num:+.8e} predicted {pred:+.8e} rel {abs(num-pred)/abs(num):.2e}", flush=True)
    out = dict(h=h, Y=Y, Ymax=Ymax, N=N, theta=S['theta'], g0=g0, lmM=eM.min(), lmMt=eMt.min(),
               nM=nM, anti=np.linalg.norm(anti)/nM, sldid=sldid, gs=gs)
    for nm, A in (('M', Ms), ('M-tau', Ms-tau)):
        e_, V = np.linalg.eigh(A)
        if e_[0] >= 0:
            continue
        p = V[:, 0]; pp = np.outer(p, p.conj())
        tp = float(np.real(p.conj()@tau@p)); y = 1.0 if tp > 0 else 0.0
        Delta = -0.5*(float(np.real(p.conj()@Ms@p)) - y*tp)
        eta = noise(S, pp, y*pp); gq = S['gQ'](eta)
        yc = S['ctr'][nA:]; top = np.argsort(-np.abs(p))[:4]
        print(f"   violating p [{nm:5s}]: <p,Mp>={float(np.real(p.conj()@Ms@p)):+.4e} <p,tau p>={tp:+.4e} "
              f"y={y:.0f} Delta={Delta:+.4e} g_Q(eta)={gq:.4e} gain/g0={Delta**2/gq/g0:.4e} "
              f"| p lives at y = {[round(float(yc[i]),3) for i in top]} (|p| {[round(float(abs(p[i])),3) for i in top]})",
              flush=True)
        out['gain_'+nm] = Delta**2/gq/g0
    print(f"   [{time.time()-t0:.0f}s]", flush=True)
    return out


if __name__ == '__main__':
    hs = [float(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '0.24').split(',')]
    Y = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    Ymax = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
    cap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    res = [run(h, Y, Ymax, cap=cap) for h in hs]
    print("\n#   h      N   theta     lam_min(M)/g0  lam_min(M-tau)/g0  lam_min(M)/||M||  anti/||M||")
    for r in res:
        print(f"{r['h']:.4f} {r['N']:5d} {r['theta']:.5f} {r['lmM']/r['g0']:+.4e} {r['lmMt']/r['g0']:+.4e} "
              f"{r['lmM']/r['nM']:+.4e} {r['anti']:.2e}", flush=True)
