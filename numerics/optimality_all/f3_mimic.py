"""F3 T3 decisive test: run the MODULAR GALERKIN machinery on the CIRCLE model's mesh.
Circle grid theta_j = 2 pi j / L  ->  x_j = tan(theta_j/2)  ->  xi_j = log((x_j+a)/(Lg-x_j)).
Cell edges = xi-midpoints; the outermost cell is capped at modular distance 'cap' beyond the last
point (the circle grid's last cell really reaches xi=+infty).  If theta on this mesh reproduces
the circle value (~0.29) while the uniform-in-xi mesh of comparable size gives ~0.36, the whole
discrepancy is the MESH: the circle grid resolves the modular neighbourhood of the endpoint of D
only to depth ~log(#points)."""
import sys, time, numpy as np
sys.path.insert(0,'/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/optimality_all')
from kkt_continuum import Qmat, defect
import f3_gal as G
f2 = 1.0/(12*np.pi**2)

def circ_edges(L, a, Lg, capR=1.0, capL=1.0):
    th = 2*np.pi*np.arange(L)/L; thw = np.where(th>np.pi, th-2*np.pi, th)
    thD = 2*np.arctan(Lg); thA = -2*np.arctan(a)
    inD = (thw>0)&(thw<thD); inA=(thw>thA)&(thw<0)
    thI = np.sort(thw[inA|inD]); x = np.tan(thI/2.0)
    xi = np.log((x+a)/(Lg-x))
    mid = 0.5*(xi[1:]+xi[:-1])
    edges = np.concatenate([[xi[0]-capL],mid,[xi[-1]+capR]])
    nA = int(np.sum(thI<0))
    return edges, nA, xi

def run(L=256, a=2.0, Lg=1.0, s=0.1, capR=1.0, capL=1.0, kind='first', extra=0, rr=2.0):
    """extra>0: append 'extra' extra geometrically refined cells beyond the circle mesh at the
    right end (modular depth capR*rr^k), i.e. artificially deepen the endpoint resolution."""
    t0=time.time(); edges,nA,xi = circ_edges(L,a,Lg,capR,capL)
    if extra>0:
        add = edges[-1] + capR*(rr**np.arange(1,extra+1)-1)
        edges = np.concatenate([edges,add])
    Q = Qmat(edges); Dc = defect(edges, nA, a, Lg, s, kind=kind)
    zeta=a*s/(a+Lg); th,g0,k,_,_ = G.theta(Q,Dc,nA,iters=20000)
    print(f"MIMIC L={L} a={a} Lg={Lg} capR={capR} extra={extra} N={len(Q)} nA={nA} "
          f"xi=[{edges[0]:.2f},{edges[-1]:.2f}] gQ/(f2z^2)={g0/(f2*zeta**2):.5f} theta={th:.5f} "
          f"cg={k} {time.time()-t0:.0f}s",flush=True)
    return th

if __name__=='__main__':
    job=sys.argv[1] if len(sys.argv)>1 else 'main'
    if job=='main':
        for L in (128,256,512,1024): run(L=L)
    elif job=='cap':
        for c in (0.3,0.7,1.0,2.0): run(L=256,capR=c)
    elif job=='deep':
        for e in (0,2,4,8,16,32): run(L=256,extra=e)
    elif job=='big':
        for L in (1024,2048): run(L=L)
    elif job=='geom':
        for (a,Lg) in [(2.0,1.0),(1.0,2.0),(1.0,1.0)]: run(L=256,a=a,Lg=Lg)
