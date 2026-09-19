import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""F3 T3: phi(Delta) = theta with the G class restricted to modular distance >= Delta from the
far endpoint of D (x=L), in BOTH frames.  Delta is a Moebius-invariant label, so the two
discretisations must agree at matched Delta wherever both resolve it.  phi(0)=theta."""
import sys, time, numpy as np
sys.path.insert(0,_os.path.join(_ROOT, 'numerics/optimality_all'))
import f3_gal as G, f3_circ as C
f2 = 1.0/(12*np.pi**2)

def gal_phi(a=1.0, L=2.0, s=0.1, h=0.06, Lam=8, Ds=(0.,0.25,0.5,1.,1.5,2.,3.,4.,6.,8.)):
    edges,nA,nB,nC,Q,Dc = G.setup(a,L,s,h,Lam,'first',uni=True)
    ctr = 0.5*(edges[:-1]+edges[1:])[nA:]; m = len(ctr); xmax = edges[-1]
    zeta = a*s/(a+L)
    for Dl in Ds:
        sel = np.where(ctr <= xmax-Dl)[0]
        if len(sel)<2: continue
        B = np.zeros((m,len(sel))); B[sel,np.arange(len(sel))]=1.0
        t0=time.time(); th,g0,k,_,_ = G.theta(Q,Dc,nA,B=(None if Dl==0 else B),iters=8000)
        print(f"GAL h={h} Lam={Lam} N={len(Q)} m={m} Delta={Dl:5.2f} r={len(sel)} theta={th:.5f} "
              f"gQ={g0/(f2*zeta**2):.4f} cg={k} {time.time()-t0:.0f}s",flush=True)

def circ_phi(L=512, a=2.0, Lg=1.0, uv=(0.30,0.42), taper='smooth', cap=1e10,
             Ds=(0.,0.25,0.5,1.,1.5,2.,3.,4.)):
    S = C.setup(L=L,a=a,Lg=Lg,cap=cap,uv=uv,taper=taper)
    thw = S['thw']; D = S['D']; x = np.tan(thw[D]/2.0)
    xi = np.log((x+a)/(Lg-x)); xmax = np.log((Lg+a)/(Lg-np.tan(np.pi/L)/1e-300*0+ (Lg-x.max())/2))
    xmax = xi.max()   # last grid point in D
    print(f"# CIRC L={L} a={a} Lg={Lg} |D|={len(D)} xi range [{xi.min():.3f},{xi.max():.3f}] "
          f"(xi0={np.log(a/Lg):.3f})",flush=True)
    for Dl in Ds:
        sel = np.where(xi <= xmax-Dl)[0]
        if len(sel)<2: continue
        B = np.zeros((len(D),len(sel))); B[sel,np.arange(len(sel))]=1.0
        t0=time.time(); th,k,_ = C.theta(S,B=(None if Dl==0 else B))
        print(f"CIRC L={L} taper={taper}{uv} Delta={Dl:5.2f} r={len(sel)} theta={th:.5f} "
              f"cg={k} {time.time()-t0:.0f}s",flush=True)

if __name__=='__main__':
    job = sys.argv[1] if len(sys.argv)>1 else 'gal'
    if job=='gal':
        for h in (0.12,0.06,0.03): gal_phi(h=h)
    elif job=='circ':
        for L in (256,384,512): circ_phi(L=L)
    elif job=='circ2':
        for L in (256,512): circ_phi(L=L,taper='none')
