import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""F2/T5: the ENDPOINT condition (e) of F1 Thm 4.4 (repaired), Prop 4.10 (prop:bdryfun),
in the rigid parameter-free modular Wiener-Hopf frame (f3_t0.py machinery, as in T4).

E(zeta) := 2 b(delta_*, A(zeta,0,0)) = -2 b(delta_*, [Q,zeta]) = (1/2) Tr(t_* A(zeta,0,0)),
t_* = U (w o delta~_*) U^H  (F1 normalisation, g_Q(delta_*) = (1/4) Tr(t_* delta_*)).
Model directions: zeta_0 = -S, S := E_D d/dy E_D  (junction y=0)  ->  E(zeta_0) = (1/2)Tr(t_*[Q,S]);
                  zeta_inf = -lambda D_w|_D, w = -4 sinh^2(y/2)  ->  A = lambda ddot,
                  E(zeta_inf) = 2 lambda (1-theta) g_Q(ddot)  (proved).

KEY STRUCTURAL FACT (found here).  For ANY matrix X supported on D, cyclicity of the trace of
finite matrices gives
      Tr(t_*[Q,X]) = 2 Tr( X . AntiHerm((t_* Q)_DD) ) ,
and the discrete stationarity of G_* over the FULL anti-Hermitian algebra on D forces
AntiHerm((t_* Q)_DD) = 0.  So in ANY finite Galerkin frame the trace formula for E is zero to
the CG residual, for every discretisation of S: the endpoint anomaly (a 0 x infinity in the
continuum) is invisible to it.  The computable form is F1's boundary form eq:Ebdry,
      E(zeta) = (1/2) Tr( (-2 sigma_zeta) M_* ),   sigma_{zeta_0}: <sigma g,g> = -(1/2)|g(0)|^2,
so -2 sigma_{zeta_0} = |delta_0><delta_0| and, in the orthonormal cell basis (first cell width h),
      E(zeta_0) = (1/2) M_*(0,0) = (1/2) (M_*)_{00} / h .
Usage:  f2_t5_endpoint.py [h1,h2,..] [Y] [Ymax]
"""
import sys, time, numpy as np
sys.path.insert(0, _os.path.join(_ROOT, 'numerics/optimality_all'))
import f2_t4_wh as T4


def diffops(m, h):
    """forward / backward / centred first-order d/dy on m uniform cells, truncated (E_D . E_D)."""
    Sf = (np.diag(-np.ones(m)) + np.diag(np.ones(m-1), 1))/h
    Sb = (np.diag(np.ones(m)) + np.diag(-np.ones(m-1), -1))/h
    return {'fwd': Sf, 'bwd': Sb, 'ctr': 0.5*(Sf+Sb)}


def Aop0(S, zeta):
    """F1 eq:Ablocks with N1 = Y1 = 0 (general zeta, NOT assumed anti-Hermitian):
    A_AD = -Q_AD zeta, A_DA = -zeta^* Q_DA, A_DD = -(zeta^* Q_DD + Q_DD zeta)."""
    nA, N, Q = S['nA'], S['N'], S['Q']
    A = np.zeros((N, N), complex)
    A[:nA, nA:] = -Q[:nA, nA:]@zeta
    A[nA:, :nA] = -zeta.conj().T@Q[nA:, :nA]
    A[nA:, nA:] = -(zeta.conj().T@Q[nA:, nA:] + Q[nA:, nA:]@zeta)
    return 0.5*(A + A.conj().T)


def Dw(m, h, yc):
    """discretised D_w|_D = (1/2)(w d/dy + d/dy w), w(y) = -4 sinh^2(y/2), centred, anti-Herm."""
    W = np.diag(-4.0*np.sinh(yc/2.0)**2)
    S = diffops(m, h)['ctr']
    A = 0.5*(W@S + S@W)
    return 0.5*(A - A.conj().T)


def run(h, Y=10.0, Ymax=10.0, ng=10, iters=20000, verbose=True):
    t0 = time.time(); S = T4.build(h, Y, Ymax, ng, iters)
    nA, N, t, Q, g0 = S['nA'], S['N'], S['t'], S['Q'], S['g0']
    m = N - nA; yc = S['ctr'][nA:]; hh = np.diff(S['e'])[nA:]
    tQ = (t@Q)[nA:, nA:]
    Ms = 0.5*(tQ + tQ.conj().T); Aa = 0.5*(tQ - tQ.conj().T)
    nM = np.abs(np.linalg.eigvalsh(Ms)).max()
    emb = lambda X: np.pad(X, ((nA, 0), (nA, 0)))
    Etr = lambda X: 0.5*np.real(np.trace(t@(Q@emb(X) - emb(X)@Q)))
    out = dict(h=h, Y=Y, Ymax=Ymax, N=N, m=m, theta=S['theta'], g0=g0,
               anti=np.linalg.norm(Aa)/nM, lmM=np.linalg.eigvalsh(Ms).min(), nM=nM)
    if verbose:
        print(f"h={h:.4f} Y={Y:g} Ymax={Ymax:g} N={N} m={m}: theta={S['theta']:.5f} "
              f"g_Q(ddot)={g0:.6e} g(d_*)/g0={S['gstar']/g0:.6f} | "
              f"||AntiHerm((t_*Q)_DD)||/||M_*||={out['anti']:.3e} lam_min(M_*)/||M_*||="
              f"{out['lmM']/nM:+.4e}", flush=True)
    # (i-a) convention check: E(zeta_inf)/g_Q(ddot) = 2(1-theta), computed from A = ddot
    Einf = 0.5*np.real(np.trace(t@S['Dc']))
    out['Einf'] = Einf/g0
    if verbose:
        print(f"   (i-a) E(zeta_inf)/g_Q(ddot) = (1/2)Tr(t_* ddot)/g_Q = {Einf/g0:.8f}   "
              f"exact 2(1-theta) = {2*(1-S['theta']):.8f}   rel.dev "
              f"{(Einf/g0)/(2*(1-S['theta']))-1:+.2e}", flush=True)
    # cyclicity identity and the blindness of the trace formula
    rng = np.random.default_rng(0); X = rng.normal(size=(m, m)) + 1j*rng.normal(size=(m, m))
    lhs = np.real(np.trace(t@(Q@emb(X) - emb(X)@Q))); rhs = 2*np.real(np.trace(X@Aa))
    out['cyc'] = abs(lhs-rhs)/max(abs(lhs), 1e-300)
    Es = {k: Etr(Sx)/g0 for k, Sx in diffops(m, h).items()}
    out.update({'Etr_'+k: v for k, v in Es.items()})
    EinfD = Etr(Dw(m, h, yc))/g0
    out['Einf_trace'] = EinfD
    if verbose:
        print(f"   cyclicity Tr(t_*[Q,X]) = 2Tr(X AntiHerm((t_*Q)_DD)): rel.dev {out['cyc']:.2e}", flush=True)
        print(f"   (trace formula) E(zeta_0)/g_Q(ddot) = " +
              "  ".join(f"{k}: {v:+.4e}" for k, v in Es.items()) +
              f"   | same formula for zeta_inf (discretised D_w): {EinfD:+.4e} "
              f"[true {2*(1-S['theta']):.5f}] -> BLIND", flush=True)
    # (e) the CORRECT discrete evaluation: F1 eq:Ablocks, and the absorption identity
    for k, Sx in diffops(m, h).items():
        zeta = -Sx                                 # zeta_0 = -S
        sig = 0.5*(zeta + zeta.conj().T)           # must be <= 0 for an isometry generator
        Ed = 0.5*np.real(np.trace(t@Aop0(S, zeta)))
        Ea = 0.5*np.real(np.trace((-2*sig)@Ms))
        es = np.linalg.eigvalsh(sig)
        out['Eblk_'+k] = Ed/g0; out['Eabs_'+k] = Ea/g0; out['sigmax_'+k] = es.max()
        if verbose:
            print(f"   (e) zeta_0 = -S[{k}]: E/g_Q(ddot) = {Ed/g0:+.6e} (eq:Ablocks) = {Ea/g0:+.6e} "
                  f"(absorption (1/2)Tr(-2sigma M_*))  rel.dev {abs(Ed-Ea)/max(abs(Ed),1e-300):.1e} | "
                  f"eig(sigma) in [{es.min():+.3e},{es.max():+.3e}] -> "
                  f"{'ADMISSIBLE (sigma<=0)' if es.max() <= 1e-10*max(abs(es).max(),1e-300) else 'NOT admissible'}",
                  flush=True)
    # (e) by the boundary form: E(zeta_0) = (1/2) (M_*)_00 / h ; and the far-end cell
    E0 = 0.5*np.real(Ms[0, 0])/hh[0]
    Efar = 0.5*np.real(Ms[-1, -1])/hh[-1]
    out['E0'] = E0/g0; out['Efar'] = Efar/g0
    dia = np.real(np.diag(Ms))/hh
    out['diag_first'] = dia[:4].tolist(); out['diag_last'] = dia[-4:].tolist()
    if verbose:
        print(f"   (e) BOUNDARY FORM  E(zeta_0)/g_Q(ddot) = (1/2)(M_*)_00/h /g_Q = {E0/g0:+.6e}"
              f"   [sign {'>= 0 OK' if E0 >= 0 else '< 0 VIOLATION'}]", flush=True)
        print(f"   (ii) M_* diagonal / cell width, first 4: "
              f"{[f'{v:+.4e}' for v in dia[:4]]}  last 4: {[f'{v:+.4e}' for v in dia[-4:]]}  "
              f"(far end -> zeta_inf, must be > 0)", flush=True)
        print(f"   [{time.time()-t0:.0f}s]", flush=True)
    return out


if __name__ == '__main__':
    hs = [float(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '0.24').split(',')]
    Y = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    Ymax = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
    res = [run(h, Y, Ymax) for h in hs]
    print("\n#   h      N   theta    E(z0)/g_Q (bdry form)  (M_*)_00/h   E(zinf)/g_Q (i-a)  2(1-theta)"
          "   Etr(z0) fwd/bwd/ctr   anti/||M||")
    for r in res:
        print(f"{r['h']:.4f} {r['N']:5d} {r['theta']:.5f} {r['E0']:+.6e} {2*r['E0']*r['g0']:+.4e} "
              f"{r['Einf']:.6f} {2*(1-r['theta']):.6f}  {r['Etr_fwd']:+.2e}/{r['Etr_bwd']:+.2e}/"
              f"{r['Etr_ctr']:+.2e}  {r['anti']:.2e}", flush=True)
