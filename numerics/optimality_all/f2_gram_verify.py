"""F2: is the Gram-reduced tangent SDP (f2_tangent_gram.py) trustworthy?
It factors Ghat = R^T R after dropping eigenvalues below tol*max -- but Ghat has a
condition number ~1e19, so the dropped directions are NOT free.  Test: take the (H,N1,Y1)
the Gram SDP returns and evaluate the EXACT objective g_Q(delta_c + [iH,Q] + noise(N1,Y1)).
Usage:  f2_gram_verify.py L cap [tol1,tol2,...]
"""
import sys, time, numpy as np
import f2_model as M
import f2_tangent_gram as TG

L = int(sys.argv[1]) if len(sys.argv) > 1 else 64
cap = float(sys.argv[2]) if len(sys.argv) > 2 else 1e6
tols = [float(v) for v in (sys.argv[3] if len(sys.argv) > 3 else '1e-14,1e-10,1e-6').split(',')]

S = M.build(L=L, cap=cap); th, xg, ds, g0c, it = M.theta_cg(S)
G, c, g0 = TG.quadform(S)
print(f"L={L} cap={cap:.0e} nD={S['nD']}: g0={g0:.8e} theta={th:.6f} 1-theta={1-th:.8f}", flush=True)
for tol in tols:
    R, e, const, leak, k, sp = TG.factor(G, c, g0, tol=tol)
    t0 = time.time()
    try:
        r = TG.solve(S, G, c, g0, solver='CLARABEL')
    except Exception as ex:
        print(f"  tol={tol:.0e}: solver failed {type(ex).__name__}"); continue
    # exact re-evaluation
    d = S['dc'] + M.rot(S, 1j*r['H']) + M.noise(S, r['N1'], r['Y1'])
    gex = M.gQ(S, d)
    eN = np.linalg.eigvalsh(0.5*(r['N1']+r['N1'].conj().T))
    print(f"  tol={tol:.0e}: rank {k}/{3*S['nD']**2} leak={leak:.1e} | SDP says g/g0={r['val']/g0:.8f} "
          f"| EXACT g/g0={gex/g0:.8f} (1-theta={1-th:.8f})  feasible? eig(N1)_min={eN.min():.2e} "
          f"eig(Y1)_min={np.linalg.eigvalsh(0.5*(r['Y1']+r['Y1'].conj().T)).min():.2e} "
          f"eig(N1-Y1)_min={np.linalg.eigvalsh(0.5*((r['N1']-r['Y1'])+(r['N1']-r['Y1']).conj().T)).min():.2e} "
          f"[{r['status']}] {time.time()-t0:.0f}s", flush=True)
