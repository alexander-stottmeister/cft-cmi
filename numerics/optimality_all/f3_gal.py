import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""F3 T1: Galerkin theta, fast operator, graded meshes, Lambda sweep, restricted classes.
Aop(G) = 1/4 * antiherm( Uh^dag [K o (Uh G Uh^dag)] Uh ),  K_ij=(q_i-q_j)^2 w_ij,  Uh = U^dag E_D.
Checked against theta_galerkin.py (h=0.3 -> 0.29926)."""
import sys, os, time, numpy as np
HERE=_os.path.join(_ROOT, 'numerics/optimality_all')
sys.path.insert(0,HERE); sys.path.insert(0,os.getcwd())
from kkt_continuum import Qmat, defect
f2 = 1.0/(12*np.pi**2)

def mesh_g(a, L, s, nA, LamA, nC, LamC, nB, r=1.0):
    """Cells uniform in xi if r=1; r>1 grades geometrically FINER towards the corners
    xi0 (A and B sides) and xi1 (B and C sides). Corners exactly on the grid."""
    b = L/(1.0+s); xi0 = np.log(a/L); xi1 = np.log((a+b)/(L-b))
    def geo(n, span, rr, rev):          # n widths summing to span, ratio rr, finest first
        w = rr**np.arange(n); w = w*span/w.sum()
        return w[::-1] if rev else w
    wA = geo(nA, LamA, r, True)                      # widths left->right, finest at xi0
    wC = geo(nC, LamC, r, False)                     # finest at xi1
    sB = xi1-xi0
    if r == 1.0:
        wB = np.full(nB, sB/nB)
    else:
        nB1 = nB//2; nB2 = nB-nB1
        wB = np.concatenate([geo(nB1, sB/2, r, False), geo(nB2, sB/2, r, True)])
    edges = np.concatenate([[xi0-LamA], xi0-LamA+np.cumsum(wA), xi0+np.cumsum(wB), xi1+np.cumsum(wC)])
    return edges, nA, nB, nC

def mesh_u(a, L, s, h, Lam):
    """FULLY uniform cells of width exactly h, xi0 exactly on the grid (the B|C boundary is
    numerically irrelevant: delta_c couples A to D=BC and G lives on all of D)."""
    b = L/(1.0+s); xi0=np.log(a/L); xi1=np.log((a+b)/(L-b))
    nA = max(1,int(round(Lam/h))); nR = max(1,int(round((xi1-xi0+Lam)/h)))
    edges = xi0 + h*np.arange(-nA, nR+1)
    nB = int(round((xi1-xi0)/h)); nC = nR-nB
    return edges, nA, nB, nC

def setup(a, L, s, h, Lam, kind='first', r=1.0, hB=None, ng=10, uni=False):
    if uni:
        edges,nA,nB,nC = mesh_u(a,L,s,h,Lam)
        return edges,nA,nB,nC,Qmat(edges),defect(edges,nA,a,L,s,kind=kind,ng=ng)
    b = L/(1.0+s); xi0=np.log(a/L); xi1=np.log((a+b)/(L-b)); hB = h if hB is None else hB
    nA = max(1,int(round(Lam/h))); nC = nA; nB = max(1,int(round((xi1-xi0)/hB)))
    edges,nA,nB,nC = mesh_g(a,L,s,nA,Lam,nC,Lam,nB,r)
    Q = Qmat(edges); Dc = defect(edges, nA, a, L, s, kind=kind, ng=ng)
    return edges,nA,nB,nC,Q,Dc

def theta(Q, Dc, nA, B=None, iters=8000, tol=1e-13, ladder=()):
    """theta = 2<beta,A^{-1}beta>/g0 by CG; B (m x r, orthonormal cols) restricts the G class."""
    N=len(Q); m=N-nA
    q,U = np.linalg.eigh(Q); q=np.clip(q,1e-300,1-1e-16)
    w = 1.0/(q[:,None]*(1-q)[None,:]+q[None,:]*(1-q)[:,None])
    K = (q[:,None]-q[None,:])**2 * w
    Uh = U.conj().T[:,nA:]                      # N x m
    if B is not None: Uh = Uh @ B
    Dh = U.conj().T @ Dc @ U
    g0 = 0.25*np.sum(w*np.abs(Dh)**2)
    ip = lambda X,Y: np.real(np.vdot(X,Y))
    def Aop(G):
        M = Uh @ G @ Uh.conj().T
        R = Uh.conj().T @ (K*M) @ Uh
        return 0.25*(R-R.conj().T)
    R0 = Uh.conj().T @ ((q[:,None]-q[None,:])*w*Dh) @ Uh
    beta = 0.125*(R0-R0.conj().T)
    x=np.zeros_like(beta); rr=beta.copy(); p=rr.copy(); rs=ip(rr,rr); nb=np.linalg.norm(beta); hist=[]
    for k in range(iters):
        Ap=Aop(p); pAp=ip(p,Ap)
        if pAp<=1e-300: break
        al=rs/pAp; x=x+al*p; rr=rr-al*Ap; rs2=ip(rr,rr); p=rr+(rs2/rs)*p; rs=rs2
        if (k+1) in ladder: hist.append((k+1,2*ip(beta,x)/g0))
        if (k+1) % 50 == 0:                      # stop when the theta estimate stagnates
            cur = 2*ip(beta,x)/g0
            if 'prev' in dir() and abs(cur-prev) < 1e-9*max(cur,1e-30): stall += 1
            else: stall = 0
            prev = cur
            if stall >= 2: break
        if np.sqrt(rs2)<tol*nb: break
    return 2*ip(beta,x)/g0, g0, k+1, hist, x

def run(a,L,s,h,Lam,kind='first',r=1.0,hB=None,ng=10,iters=8000,tag='',uni=False):
    t0=time.time(); edges,nA,nB,nC,Q,Dc = setup(a,L,s,h,Lam,kind,r,hB,ng,uni)
    zeta=a*s/(a+L); th,g0,k,hist,x = theta(Q,Dc,nA,iters=iters,ladder=(100,400,1000))
    print(f"{tag}{kind:5s} a={a} L={L} h={h:.4f} Lam={Lam:g} r={r:g} N={len(Q)} "
          f"(nA,nB,nC)=({nA},{nB},{nC}) gQ/(f2 z^2)={g0/(f2*zeta**2):.5f} theta={th:.5f} "
          f"uni={int(uni)} cg={k} lad={['%.5f'%v for _,v in hist]} {time.time()-t0:.0f}s", flush=True)
    return th, g0/(f2*zeta**2)

if __name__=='__main__':
    job = sys.argv[1] if len(sys.argv)>1 else 'check'
    a,L,s = 1.0,2.0,0.1
    if job=='check':
        for h in (0.3,0.2): run(a,L,s,h,12)
    elif job=='hsweep':
        for h in (0.4,0.3,0.25,0.2,0.15,0.125,0.1,0.08,0.07,0.06,0.05,0.04): run(a,L,s,h,12)
    elif job=='lamsweep':
        for Lam in (6,8,12,16,20,24):
            for h in (0.2,0.15,0.1): run(a,L,s,h,Lam)
    elif job=='grade':
        for r in (1.0,1.05,1.1): 
            for h in (0.2,0.1): run(a,L,s,h,12,r=r)
    elif job=='uni':
        for h in (0.32,0.16,0.08,0.04,0.24,0.12,0.06,0.03): run(a,L,s,h,12,uni=True)
    elif job=='uni2':
        for h in (0.2,0.1,0.05,0.025): run(a,L,s,h,12,uni=True)
    elif job=='lamfine':
        for Lam in (8,12,16,20,24,30):
            for h in (0.12,0.06): run(a,L,s,h,Lam,uni=True)
    elif job=='lamsmall':
        for Lam in (3,4,5,6,8,12):
            for h in (0.12,0.06): run(a,L,s,h,Lam,uni=True)
    elif job=='ladder5':
        for h in (0.24,0.12,0.06,0.03,0.02,0.015,0.01): run(a,L,s,h,5,uni=True)
    elif job=='ladder8':
        for h in (0.04,0.03,0.02): run(a,L,s,h,8,uni=True)
    elif job=='misc':
        run(a,L,s,0.1,12,kind='exact'); run(a,L,s,0.1,12,ng=16)
        run(2.0,1.0,s,0.1,12); run(1.0,4.0,s,0.1,12); run(a,L,0.3,0.1,12)
