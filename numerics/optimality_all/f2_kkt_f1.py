"""F2/T2 (F1 Thm 4.4 form): the necessary AND sufficient criterion for the isometric orbit
to be the global optimum of the tangent problem.

F1 normalisation: t_* is the SLD with  g_Q(delta_*) = (1/4) Tr(t_* delta_*), i.e. exactly
TWICE the SLD of kkt_continuum.gQ_sld (t_F1 = U (w o delta~) U^H).  Then
   d/ds g_Q(delta_* + s A(0,N1,Y1))|_0 = (1/2)[Tr(N1 M_*) - Tr(Y1 tau_*)],
   tau_* = E_D t_* E_D,  M_* = Herm((t_* Q)_DD) = Herm(t_DD Q_DD) + Herm(t_DA Q_AD).
CRITERION: orbit = global optimum  <=>  M_* >= 0  and  M_* - tau_* >= 0.
Consistency (F1 Prop 4.3): AntiHerm((t_* Q)_DD) = 0 at the orbit optimum.
Cor 4.5 gain for a violating p: Delta = -(1/2)[<p,M p> - y<p,tau p>] (y = 1 if <p,tau p> > 0
else 0); gain = Delta^2 / g_Q(A(0,pp*,y pp*)), and with the rotation re-optimised,
gain_red = Delta^2 / g_red, g_red = min_G g_Q(A(0,pp*,y pp*) + [G,Q]).
Usage:  f2_kkt_f1.py L1,.. [cap1,..] [uv_a1]
"""
import sys, time, numpy as np
import f2_model as M


def objects(S, iters=400):
    th, x, dstar, g0, it = M.theta_cg(S)
    nD = S['nD']
    t = 2.0*M.sld(S, dstar)                       # F1 normalisation
    idn = 0.25*np.real(np.trace(t@dstar))/M.gQ(S, dstar)
    tQ = (t@S['Q'])[:nD, :nD]
    Ms = 0.5*(tQ + tQ.conj().T); Aa = 0.5*(tQ - tQ.conj().T)
    tau = 0.5*(t[:nD, :nD] + t[:nD, :nD].conj().T)
    return dict(theta=th, g0=g0, dstar=dstar, t=t, Ms=Ms, tau=tau, anti=Aa, sldid=idn, its=it)


def gred(S, eta, iters=400, tol=1e-14):
    """min_G g_Q(eta + [G,Q]) by CG (same operator A as theta_cg)."""
    iD = S['iD']; U, w = S['U'], S['w']
    W = lambda Y: U@(w*(U.conj().T@Y@U))@U.conj().T
    def PhiT(Y):
        C = Y@S['Q'] - S['Q']@Y; R = C[np.ix_(iD, iD)]; return 0.5*(R - R.conj().T)
    Aop = lambda G: 0.5*PhiT(W(M.rot(S, G)))
    ip = lambda A, B: float(np.real(np.vdot(A, B)))
    beta = -0.5*PhiT(W(eta)); g0 = M.gQ(S, eta)
    xx = np.zeros_like(beta); r = beta.copy(); p = r.copy(); rs = ip(r, r); nb = np.sqrt(max(rs, 1e-300))
    for k in range(iters):
        Ap = Aop(p); pAp = ip(p, Ap)
        if pAp <= 1e-300: break
        al = rs/pAp; xx = xx + al*p; r = r - al*Ap
        rs2 = ip(r, r); p = r + (rs2/rs)*p; rs = rs2
        if np.sqrt(rs2) < tol*nb: break
    return g0 - 0.5*ip(beta, xx), xx


def run(L, cap=1e10, uv=(0.30, 0.42), full=True):
    t0 = time.time(); S = M.build(L=L, cap=cap, uv=uv); O = objects(S); nD = S['nD']
    g0 = O['g0']; eM = np.linalg.eigvalsh(O['Ms']); eMt = np.linalg.eigvalsh(O['Ms']-O['tau'])
    et = np.linalg.eigvalsh(O['tau']); nM = np.abs(eM).max()
    dcDD = np.linalg.norm(S['dc'][:nD, :nD])/np.linalg.norm(S['dc'])
    dcAA = np.linalg.norm(S['dc'][nD:, nD:])/np.linalg.norm(S['dc'])
    print(f"L={L} nD={nD} cap={cap:.0e} uv={uv}: theta={O['theta']:.6f} g0={g0:.6e} "
          f"SLD id (1/4)Tr(t d)/g={O['sldid']:.10f} | |dc_DD|/|dc|={dcDD:.4f} |dc_AA|/|dc|={dcAA:.4f} "
          f"| ||AntiHerm(tQ)_DD||/||M||={np.linalg.norm(O['anti'])/nM:.3e}", flush=True)
    print(f"   lam_min(M_*)     = {eM.min():+.6e} = {eM.min()/g0:+.4e} g0 = {eM.min()/nM:+.4e} ||M||"
          f"   lam_max={eM.max():+.6e}", flush=True)
    print(f"   lam_min(M_*-tau) = {eMt.min():+.6e} = {eMt.min()/g0:+.4e} g0 = {eMt.min()/nM:+.4e} ||M||"
          f"   lam_min(tau)={et.min():+.3e} lam_max(tau)={et.max():+.3e}", flush=True)
    ok = (eM.min() >= 0) and (eMt.min() >= 0)
    print(f"   CRITERION (M>=0 and M-tau>=0): {ok}", flush=True)
    if full:
        for nm, A in (('M', O['Ms']), ('M-tau', O['Ms']-O['tau'])):
            e, V = np.linalg.eigh(A); p = V[:, 0]
            if e[0] >= 0: continue
            pp = np.outer(p, p.conj()); tp = float(np.real(p.conj()@O['tau']@p))
            y = 1.0 if tp > 0 else 0.0
            Delta = -0.5*(float(np.real(p.conj()@O['Ms']@p)) - y*tp)
            eta = M.noise(S, pp, y*pp)
            gq = M.gQ(S, eta); gr, _ = gred(S, eta)
            print(f"   violating p from {nm:5s}: <p,Mp>={float(np.real(p.conj()@O['Ms']@p)):+.4e} "
                  f"<p,tau p>={tp:+.4e} y={y:.0f} Delta={Delta:+.4e} | g_Q(eta)={gq:.4e} "
                  f"g_red(eta)={gr:.4e} | gain/g0={Delta**2/gq/g0:.4e} gain_red/g0={Delta**2/gr/g0:.4e} "
                  f"| loc(p): top-3 |p| at D-frac {[round(float(i)/nD,3) for i in np.argsort(-np.abs(p))[:3]]}",
                  flush=True)
    print(f"   [{time.time()-t0:.0f}s]", flush=True)
    return dict(L=L, cap=cap, uv=uv, theta=O['theta'], g0=g0, lmM=eM.min(), lmMt=eMt.min(),
                nM=nM, ok=ok, anti=np.linalg.norm(O['anti'])/nM, dcDD=dcDD, dcAA=dcAA)


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    caps = [float(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '1e10').split(',')]
    uvs = [(float(v), float(v)+0.12) for v in (sys.argv[3] if len(sys.argv) > 3 else '0.30').split(',')]
    res = []
    for L in Ls:
        for cap in caps:
            for uv in uvs:
                res.append(run(L, cap=cap, uv=uv)); print('', flush=True)
    print("#    L     cap      uv0    theta     lam_min(M)/g0  lam_min(M-tau)/g0  lam_min(M)/||M||  |dc_DD|/|dc|")
    for r in res:
        print(f"{r['L']:6d} {r['cap']:.0e} {r['uv'][0]:.2f} {r['theta']:.6f} {r['lmM']/r['g0']:+.4e} "
              f"{r['lmMt']/r['g0']:+.4e} {r['lmM']/r['nM']:+.4e} {r['dcDD']:.4f}", flush=True)
