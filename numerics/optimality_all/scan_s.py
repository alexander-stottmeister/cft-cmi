"""Scan: is the compression the minimiser of g_Q over F in the discretised continuum?
Region-dependent mesh widths; the compression D -> B is an infinite modular squeeze, so
dim V_B must be large compared with dim V_C for the discrete model to represent it."""
import sys, time, numpy as np, kkt_continuum as K
a, L = 1.0, 2.0; f2 = 1/(12*np.pi**2)
sv = float(sys.argv[1]); kind = sys.argv[2] if len(sys.argv)>2 else 'exact'
print(f"# s={sv} kind={kind}  zeta={a*sv/(a+L):.6f}  f2 zeta^2={f2*(a*sv/(a+L))**2:.6e}", flush=True)
print("# hA  hB  hC  LamA LamC |  N  nA nB nC |  g_Q(d_c)/(f2 z^2) | min_F g_Q/(f2 z^2) | min/g(d_c) | Delta(t_c)/(2g_c) | KKTgap | dual/min | Tr(1-XX*) | t", flush=True)
for (hA,hB,hC,LamA,LamC) in eval(sys.argv[3]):
    t0=time.time()
    edges,nA,nB,nC,Q,D = K.build(a,L,sv,hA,LamA,LamC,kind,hB=hB,hC=hC)
    N=len(Q); zeta=a*sv/(a+L); ref=f2*zeta**2
    g,t,V,q = K.gQ_sld(Q,D)
    Dc,_,_,_ = K.linear_sdp(Q,t,nA,nB)
    gp,Xp,Zp,stp = K.primal_sdp(Q,nA,nB)
    R=np.zeros((N,N),complex); R[:nA,:nA]=Q[:nA,:nA]; M=Q[:nA,nA:nA+nB]@Xp.conj().T
    R[:nA,nA:]=M; R[nA:,:nA]=M.conj().T; R[nA:,nA:]=Zp; R=0.5*(R+R.conj().T)
    gp2,tp,Vp,_ = K.gQ_sld(Q,Q-R)
    Dlo,_,_,stl = K.linear_sdp(Q,tp,nA,nB)
    print(f"{hA:5.3f} {hB:5.3f} {hC:5.3f} {LamA:4.1f} {LamC:4.1f} | {N:4d} {nA:3d} {nB:3d} {nC:3d} | "
          f"{g/ref:.6f} | {gp/ref:.6f} | {gp/g:.6f} | {Dc/(2*g):+.4f} | {(2*gp2-Dlo)/(2*gp2):+.2e} | "
          f"{max(Dlo,0)**2/(8*Vp)/gp2:.6f} | {np.trace(np.eye(N-nA)-Xp@Xp.conj().T).real:.3f} | "
          f"{time.time()-t0:.0f}s {stp}", flush=True)
