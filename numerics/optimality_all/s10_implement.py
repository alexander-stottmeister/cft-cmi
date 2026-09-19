"""S10: is the optimal rotation implementable?  Check ||P^perp G P||_2 (Shale-Stinespring)
for (i) the CG optimiser G_*, (ii) the single direction G = R_a, and the single-direction
gain cos^2(u, v_{R_a}), as functions of L."""
import numpy as np, sys
sys.path.insert(0,'/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/optimality_all')
from s10_theta import setup
for L in (256,384,512):
    S=setup(L=L,a=2.0,Lg=1.0); D=S['D']; u=S['u']; nu2=S['nu2']; P=S['P']; Pp=S['Pp']
    def emb(g):
        G=np.zeros((L,L),complex); G[np.ix_(D,D)]=g; return G
    def Aop(g):
        v,_=S['riesz'](emb(g)); R=v[np.ix_(D,D)]; return 0.5*(R-R.conj().T)
    R=u[np.ix_(D,D)]; b=0.5*(R-R.conj().T)
    # single direction G = R_a
    v1,_=S['riesz'](emb(b)); nv1=np.real(np.vdot(v1,v1)); ip1=np.real(np.vdot(u,v1))
    c1=ip1**2/(nu2*nv1)
    hs_b=np.linalg.norm(Pp@emb(b)@P)/np.linalg.norm(b)
    x=np.zeros_like(b); r=b.copy(); p=r.copy(); rs=np.real(np.vdot(r,r))
    for k in range(70):
        Ap=Aop(p); pAp=np.real(np.vdot(p,Ap)); al=rs/pAp
        x=x+al*p; r=r-al*Ap; rs2=np.real(np.vdot(r,r)); p=r+(rs2/rs)*p; rs=rs2
    th=np.real(np.vdot(b,x))/nu2
    vx,_=S['riesz'](emb(x)); nvx=np.real(np.vdot(vx,vx)); ipx=np.real(np.vdot(u,vx))
    eps=-ipx/nvx; Gs=eps*x
    hs_G=np.linalg.norm(Pp@emb(Gs)@P); op_G=np.linalg.norm(Gs,2)
    print(f"L={L}: theta={th:.5f}  cos^2(G=R_a)={c1:.5f}   "
          f"|P^perp eps*G_* P|_2/s={hs_G:.4f}  |eps*G_*|_op/s={op_G:.4f}  "
          f"|P^perp R_a P|_2/|R_a|_2={hs_b:.4f}", flush=True)
