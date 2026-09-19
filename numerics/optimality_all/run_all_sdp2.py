import time, numpy as np, all_channels_sdp as S
for g in [(1,3,2),(2,3,2),(3,3,2)]:
    petz,z=S.petz_value(*g); t=time.time()
    try:
        F,nlF,rho,C,rr=S.solve(*g,parity_cov=True,solver='CLARABEL')
        np.savez(f"allch_{g[0]}_{g[1]}_{g[2]}.npz",C=C,rr=rr,rho=rho,F=F)
        print(f"{g} z={z:.4f} Petz={petz:.6e} OPT={nlF:.6e} opt/Petz={nlF/petz:.5f} opt/z^2={nlF/z**2:.5f} t={time.time()-t:.0f}s",flush=True)
    except Exception as e: print(g,"failed",e,flush=True)
