"""F2/T2: KKT sign criterion for the tangent problem at the isometric-orbit optimum.

delta_* = delta_c + [G_*,Q] (S10's CG optimum), t_* = SLD of delta_*, normalised as in
kkt_continuum.gQ_sld:  t = (1/2) U (w o delta~) U^H, so that  g_Q(delta) = (1/2) Tr(t delta)
and  d/d eps g_Q(delta_* + eps eta) = Tr(t_* eta)  (checked by finite differences below).
[The Phase-5 brief writes g_Q = (1/4) Tr(t delta); that is the same t times 2.  All sign
conditions are invariant under t -> c t, c > 0.]

Coefficient of the noise directions in Tr(t_* noise):
  Tr(t_* noise(N1,Y1)) = Tr(N1 M_*) - Tr(Y1 t_DD),
  M_* = (1/2)(t_DD Q_DD + Q_DD t_DD) + (1/2)(t_DA Q_AD + Q_DA t_AD).
NECESSARY for global optimality of the orbit:  M_* >= 0  and  M_* - t_DD >= 0.
SUFFICIENT:  M_* >= (t_DD)_+ .
Usage:  f2_kkt_check.py [L1,L2,...] [cap]
"""
import sys, time, numpy as np
import f2_model as M


def kkt(S):
    nD = S['nD']
    th, x, dstar, g0, it = M.theta_cg(S)
    t = M.sld(S, dstar)
    gs = M.gQ(S, dstar)
    idn = 0.5*np.real(np.trace(t@dstar))/gs           # = 1 for this normalisation
    tDD = t[:nD, :nD]; tDA = t[:nD, nD:]
    QDD, QDA = S['QDD'], S['QDA']
    Ms = 0.5*(tDD@QDD + QDD@tDD) + 0.5*(tDA@QDA.conj().T + QDA@tDA.conj().T)
    Ms = 0.5*(Ms + Ms.conj().T); tDD = 0.5*(tDD + tDD.conj().T)
    return dict(theta=th, g0=g0, gstar=gs, dstar=dstar, t=t, Ms=Ms, tDD=tDD, sldid=idn, its=it)


def fd_check(S, K, nrep=3, eps=1e-6, seed=0):
    """finite differences: d/deps g_Q(delta_* + eps noise(N1,Y1)) =?= Tr(N1 M) - Tr(Y1 tDD)."""
    rng = np.random.default_rng(seed); nD = S['nD']; out = []
    for r in range(nrep):
        A = rng.normal(size=(nD, nD)) + 1j*rng.normal(size=(nD, nD)); N1 = 0.5*(A+A.conj().T)
        B = rng.normal(size=(nD, nD)) + 1j*rng.normal(size=(nD, nD)); Y1 = 0.5*(B+B.conj().T)
        eta = M.noise(S, N1, Y1)
        gp = M.gQ(S, K['dstar'] + eps*eta); gm = M.gQ(S, K['dstar'] - eps*eta)
        num = (gp-gm)/(2*eps)
        pred = np.real(np.trace(N1@K['Ms'])) - np.real(np.trace(Y1@K['tDD']))
        # also the rotation directions must have zero derivative at the orbit optimum
        C = rng.normal(size=(nD, nD)) + 1j*rng.normal(size=(nD, nD)); H = 0.5*(C+C.conj().T)
        er = M.rot(S, 1j*H)
        drot = (M.gQ(S, K['dstar']+eps*er) - M.gQ(S, K['dstar']-eps*er))/(2*eps)
        out.append((num, pred, abs(num-pred)/max(abs(num), 1e-300), drot/max(abs(num), 1e-300)))
    return out


def pos(A):
    e, V = np.linalg.eigh(0.5*(A+A.conj().T)); e = np.maximum(e, 0.0)
    return (V*e)@V.conj().T


def run(L, cap=1e10, seed=0):
    t0 = time.time(); S = M.build(L=L, cap=cap); K = kkt(S)
    eM = np.linalg.eigvalsh(K['Ms']); eMt = np.linalg.eigvalsh(K['Ms']-K['tDD'])
    et = np.linalg.eigvalsh(K['tDD']); eMp = np.linalg.eigvalsh(K['Ms']-pos(K['tDD']))
    sc = max(abs(eM).max(), abs(et).max())
    print(f"L={L} nD={S['nD']} nI={S['nI']} cap={cap:.0e}: theta={K['theta']:.6f}  "
          f"g_Q(d_*)={K['gstar']:.6e}  SLD identity (1/2)Tr(t d)/g = {K['sldid']:.10f}", flush=True)
    for nm, e in (('M_*', eM), ('M_* - t_DD', eMt), ('t_DD', et), ('M_* - (t_DD)_+', eMp)):
        print(f"    eig({nm:14s}) min={e.min():+.6e}  max={e.max():+.6e}  min/scale={e.min()/sc:+.3e}",
              flush=True)
    nec = (eM.min() >= -1e-12*sc) and (eMt.min() >= -1e-12*sc)
    suf = eMp.min() >= -1e-12*sc
    print(f"    scale={sc:.3e}  NECESSARY (M>=0 and M-t_DD>=0): {nec}   SUFFICIENT (M>=(t_DD)_+): {suf}",
          flush=True)
    for (num, pred, rel, drot) in fd_check(S, K, seed=seed):
        print(f"    FD check: d g_Q = {num:+.8e}  predicted {pred:+.8e}  rel.err {rel:.2e}  "
              f"|d_rot|/|d| {abs(drot):.2e}", flush=True)
    print(f"    [{time.time()-t0:.1f}s]", flush=True)
    return dict(L=L, S=S, K=K, eM=eM, eMt=eMt, et=et, eMp=eMp, nec=nec, suf=suf, scale=sc)


if __name__ == '__main__':
    Ls = [int(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '64').split(',')]
    cap = float(sys.argv[2]) if len(sys.argv) > 2 else 1e10
    res = {}
    for L in Ls:
        res[L] = run(L, cap=cap)
        print('', flush=True)
    print('# summary  L | min eig M_* | min eig (M_*-t_DD) | min eig t_DD | min eig (M_*-(t_DD)_+) | nec | suf')
    for L, r in res.items():
        print(f"{L:5d} {r['eM'].min():+.4e} {r['eMt'].min():+.4e} {r['et'].min():+.4e} "
              f"{r['eMp'].min():+.4e}  {r['nec']}  {r['suf']}", flush=True)
    np.savez('f2_kkt_%s_%.0e.npz' % ('_'.join(map(str, Ls)), cap),
             **{f'{k}_{L}': r[k] for L, r in res.items() for k in ('eM', 'eMt', 'et', 'eMp')},
             **{f'Ms_{L}': r['K']['Ms'] for L, r in res.items()},
             **{f'tDD_{L}': r['K']['tDD'] for L, r in res.items()})
