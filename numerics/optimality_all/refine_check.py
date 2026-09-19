"""Is the discrete minimiser really better than the compression, or is it an artefact?

The Galerkin space V_N is nested under cell splitting, and (i) F_N embeds isometrically into
F_{N'} for N' a refinement (and into the CONTINUUM F), (ii) g_{Q_N}(P delta P) <= g_Q(delta)
increases to the continuum value (V_{Q_N}(t) = Tr(t Q t (1-Q)) exactly for t supported on V_N,
so g_{Q_N} is the same Legendre sup over a smaller set of test operators).
Hence: solve the primal in a coarse model, embed the minimiser into successive refinements and
watch g_{Q_{N'}} climb.  If it climbs past f2 zeta^2 the coarse 'winner' is a truncation artefact.
The compression defect is carried along as the control."""
import sys, time, numpy as np, kkt_continuum as K
a, L = 1.0, 2.0; f2 = 1/(12*np.pi**2)
sv = float(sys.argv[1]); kind = sys.argv[2]
hA, hB, hC, LamA, LamC = [float(x) for x in sys.argv[3:8]]
rs = [int(x) for x in sys.argv[8].split(',')]
e0, nA, nB, nC, xi0, xi1, b = K.mesh(a, L, sv, hA, LamA, LamC, hB, hC)
Q0 = K.Qmat(e0); D0 = K.defect(e0, nA, a, L, sv, kind=kind)
zeta = a*sv/(a+L); ref = f2*zeta**2
g0, t0_, V0, _ = K.gQ_sld(Q0, D0)
t0 = time.time(); gp, Xp, Zp, stp = K.primal_sdp(Q0, nA, nB)
print(f"# s={sv} kind={kind} coarse mesh ({hA},{hB},{hC}) Lam=({LamA},{LamC}) N={len(Q0)} "
      f"(nA,nB,nC)=({nA},{nB},{nC})  zeta={zeta:.5f} f2 zeta^2={ref:.6e}", flush=True)
print(f"# coarse: g_Q(d_c)/ref={g0/ref:.6f}   min_F g_Q/ref={gp/ref:.6f}   min/g(d_c)={gp/g0:.6f} "
      f"[{stp}] {time.time()-t0:.0f}s", flush=True)
print("#  r   N'     g_{Q_N'}(delta_c)/ref    g_{Q_N'}(delta_opt embedded)/ref    ratio opt/comp", flush=True)
for r in rs:
    ed = np.concatenate([np.linspace(e0[i], e0[i+1], r+1)[:-1] for i in range(len(e0)-1)] + [[e0[-1]]])
    nA2, nB2, nC2 = nA*r, nB*r, nC*r; N2 = len(ed)-1
    Q2 = K.Qmat(ed); D2 = K.defect(ed, nA2, a, L, sv, kind=kind)
    E = np.zeros((N2, len(e0)-1))
    for m in range(len(e0)-1): E[r*m:r*m+r, m] = 1/np.sqrt(r)
    EB = E[nA2:nA2+nB2, nA:nA+nB]; ED = E[nA2:, nA:]
    X2 = ED @ Xp @ EB.conj().T; Z2 = ED @ Zp @ ED.conj().T
    R = np.zeros((N2, N2), complex); R[:nA2,:nA2] = Q2[:nA2,:nA2]
    M = Q2[:nA2, nA2:nA2+nB2] @ X2.conj().T
    R[:nA2, nA2:] = M; R[nA2:, :nA2] = M.conj().T; R[nA2:, nA2:] = Z2; R = 0.5*(R+R.conj().T)
    gc = K.gQ_sld(Q2, D2)[0]; go = K.gQ_sld(Q2, Q2-R)[0]
    print(f"{r:4d} {N2:5d}   {gc/ref:.6f}   {go/ref:.6f}   {go/gc:.6f}", flush=True)
