"""F3: Richardson closure.  (1) y_max systematic: theta(Ymax) = theta_inf - c/Ymax (fitted).
(2) measured convergence order from log-log of successive increments on octave ladders.
(3) Richardson extrapolation h->0 per family."""
import numpy as np
np.set_printoptions(precision=5, suppress=True)

# ---- (1) y_max law, from f3_t0_ymax.out / f3_t0_ymax2.out (Y=6 or 10 -> identical, Y converged)
ym = {0.12: [(10,0.34236),(12,0.34291),(16,0.34357),(20,0.34395),(24,0.34421),(30,0.34447),(40,0.34473)],
      0.06: [(12,0.35967),(16,0.36011),(20,0.36036),(24,0.36054),(30,0.36071)]}
cfit={}
print("# (1) y_max law  theta(Ymax) = t - c/Ymax   (least squares on 1/Ymax)")
for h,d in ym.items():
    Y=np.array([a for a,_ in d],float); T=np.array([b for _,b in d])
    A=np.vstack([np.ones_like(Y),-1/Y]).T; sol,res,_,_=np.linalg.lstsq(A,T,rcond=None)
    pred=A@sol; cfit[h]=sol[1]
    print(f"  h={h}: theta_inf={sol[0]:.5f} c={sol[1]:.4f}  max|resid|={np.abs(pred-T).max():.1e}")
p_c = np.log(cfit[0.12]/cfit[0.06])/np.log(2.0)
print(f"  c(h) ~ h^{p_c:.3f}  (c=0.031 at h=0.12, 0.021 at h=0.06) -> correction +c(h)/Ymax")
cof = lambda h: cfit[0.06]*(h/0.06)**p_c

fam = {
 'A  T0 uniform Y=Ymax=10': (10.0,[(0.32,0.29622),(0.24,0.31367),(0.16,0.33225),(0.12,0.34236),
    (0.08,0.35334),(0.06,0.35934),(0.04,0.36588),(0.03,0.36945),(0.02,0.37334),(0.015,0.37544)]),
 'B  T0 uniform Y=6 Ymax=20': (20.0,[(0.24,0.31581),(0.12,0.34395),(0.06,0.36036),(0.03,0.37009),(0.02,0.37380)]),
 'C  Galerkin a=1,L=2 Lam=12': (15.4,[(0.32,0.29797),(0.24,0.31518),(0.16,0.33357),(0.12,0.34350),
    (0.08,0.35423),(0.06,0.36007),(0.04,0.36644)]),
 "C' Galerkin a=1,L=2 Lam=8": (11.4,[(0.12,0.34277),(0.06,0.35960),(0.04,0.36608),(0.03,0.36962),(0.02,0.37346)]),
}
print("\n# (2)+(3) octave ladders: ratio rho of successive increments, order p=log2(1/rho),")
print("#         Richardson theta_inf = theta(h_min) + Delta*rho/(1-rho); y_max-corrected")
for name,(Ymax,d) in fam.items():
    hs=np.array([a for a,_ in d]); ts=np.array([b for _,b in d])+cof(np.array([a for a,_ in d]))/Ymax
    for start in range(2):
        sub=[(h,t) for h,t in zip(hs,ts) if abs(np.log2(h/hs[start])-round(np.log2(h/hs[start])))<1e-6]
        if len(sub)<3: continue
        H=np.array([a for a,_ in sub]); T=np.array([b for _,b in sub])
        dd=np.diff(T); rho=dd[1:]/dd[:-1]; p=np.log2(1.0/rho)
        r=rho[-1]; tinf=T[-1]+dd[-1]*r/(1-r)
        print(f"  {name:28s} h={H[0]:.3f}->{H[-1]:.4f}: rho={np.round(rho,3)} p={np.round(p,3)} "
              f"theta(h_min)={T[-1]:.5f} -> theta_inf={tinf:.5f}")
# mimic family: variable = 1/L
print()
Lm=np.array([128,256,512,1024,2048.]); Tm=np.array([0.34058,0.35830,0.36904,0.37534,0.37893])
Tm = Tm + cof(13.0/ (0.5*Lm*0+1)*0 + 6.0/Lm*0 + 1.0)*0   # (window correction added separately)
dd=np.diff(Tm); rho=dd[1:]/dd[:-1]
print(f"  D  mimic (circle mesh, a=2,Lg=1) 1/L: rho={np.round(rho,3)} p={np.round(np.log2(1/rho),3)} "
      f"theta(L=2048)={Tm[-1]:.5f} -> theta_inf={Tm[-1]+dd[-1]*rho[-1]/(1-rho[-1]):.5f} (+~0.001 window)")
