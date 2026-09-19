"""F3: extrapolation of theta(h) -> theta_infty.  Models: theta = t - c h^p (3-pt exact solve on
consecutive triples, and least squares on the tail); geometric per-octave ratio."""
import sys, numpy as np
from scipy.optimize import least_squares

def tri(hs, ts):
    """exact 3-point solve for (t,c,p) on each consecutive triple"""
    out=[]
    for i in range(len(hs)-2):
        h=np.array(hs[i:i+3]); y=np.array(ts[i:i+3])
        f=lambda p: (y[1]-y[0])*(h[1]**p-h[2]**p)-(y[2]-y[1])*(h[0]**p-h[1]**p)
        lo,hi=0.05,4.0
        if f(lo)*f(hi)>0: out.append((h[2],np.nan,np.nan)); continue
        for _ in range(200):
            mid=0.5*(lo+hi)
            if f(lo)*f(mid)<=0: hi=mid
            else: lo=mid
        p=0.5*(lo+hi); c=(y[1]-y[0])/(h[0]**p-h[1]**p); t=y[0]+c*h[0]**p
        out.append((h[2],p,t))
    return out

def lsq(hs, ts, p0=0.8):
    h=np.array(hs); y=np.array(ts)
    r=lambda v: v[0]-v[1]*h**v[2]-y
    s=least_squares(r,[y[-1]+0.02,0.2,p0])
    return s.x, np.sqrt(np.mean(s.fun**2))

if __name__=='__main__':
    sets = {
     'uniA (Lam12 uni) 0.32..0.04': ([0.32,0.24,0.16,0.12,0.08,0.06,0.04],
                                     [0.29797,0.31518,0.33357,0.34350,0.35423,0.36007,0.36644]),
     'hsweep (Lam12)  0.4..0.04' : ([0.4,0.3,0.25,0.2,0.15,0.125,0.1,0.08,0.07,0.06,0.05,0.04],
        [0.28578,0.29926,0.31418,0.32367,0.33620,0.34159,0.34843,0.35427,0.35708,0.35999,0.36326,0.36646]),
     'mimic (circle mesh) L=128..512': ([1/128.,1/256.,1/512.],[0.34058,0.35830,0.36904]),
    }
    for k,(hs,ts) in sets.items():
        print(f"--- {k}")
        for (h,p,t) in tri(hs,ts): print(f"    triple ending h={h:.4f}: p={p:.3f} theta_inf={t:.5f}")
        for n in (3,4,5,len(hs)):
            if n>len(hs): continue
            x,res = lsq(hs[-n:],ts[-n:])
            print(f"    lsq last {n}: theta_inf={x[0]:.5f} c={x[1]:.4f} p={x[2]:.3f} rms={res:.2e}")
