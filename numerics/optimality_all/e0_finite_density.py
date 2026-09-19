"""Orchestrator check of question (Q) of rigor/phase4_brief.md on half-filled hopping chains:
real Hilbert space S_2(PH, P^perp H) with inner product Re Tr(A^*B); N = span{P^perp l P : l Hermitian on I};
Ext = span{P^perp Z P : Z anti-Hermitian on I^c}.  Result: Ext = N^perp EXACTLY for every chain tested, with dim N = |I|^2.
Algebra behind it: B = P^perp X P is orthogonal to N iff E_I (B+B^*) E_I = 0, and orthogonal to Ext iff E_{I^c}(B - B^*)E_{I^c} = 0;
with H := B + B^* (Hermitian, P-off-diagonal) one has B - B^* = S H, S := 1 - 2P, so (Q) <=> [E_I H E_I = 0 and E_{I^c} S H E_{I^c} = 0 => H = 0]
for P-off-diagonal Hermitian H -- a two-projection (Halmos) statement about the pair (P, E_I)."""
import numpy as np
def corr(n):
    i=np.arange(n)[:,None]; j=np.arange(n)[None,:]; d=i-j
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(d==0,0.5,np.sin(np.pi*d/2)/(np.pi*d))
def herm_basis(idx, n, anti=False):
    B=[]
    for a in idx:
        for b in idx:
            if a<b:
                E=np.zeros((n,n),complex); E[a,b]=1; E[b,a]=1; B.append(1j*E if anti else E)
                E=np.zeros((n,n),complex); E[a,b]=1j; E[b,a]=-1j; B.append(1j*E if anti else E)
            elif a==b:
                E=np.zeros((n,n),complex); E[a,a]=1; B.append(1j*E if anti else E)
    return B
def realvec(A): return np.concatenate([A.real.ravel(), A.imag.ravel()])
if __name__ == "__main__":
    for n, I in [(8, range(2,6)), (10, range(3,7)), (10, range(2,7)), (12, range(3,9)), (12, range(4,7)), (12, range(1,6)), (14, range(2,9)), (16, range(5,11))]:
        Q=corr(n); w,U=np.linalg.eigh(Q); P=U[:,w>0.5]@U[:,w>0.5].conj().T; Pp=np.eye(n)-P
        I=list(I); Ic=[k for k in range(n) if k not in I]
        Nv=np.array([realvec(Pp@l@P) for l in herm_basis(I,n)]).T
        Ev=np.array([realvec(Pp@z@P) for z in herm_basis(Ic,n,anti=True)]).T
        k=int(round(np.trace(P).real)); full=2*k*(n-k)
        rN=np.linalg.matrix_rank(Nv,1e-9); rE=np.linalg.matrix_rank(Ev,1e-9); rNE=np.linalg.matrix_rank(np.hstack([Nv,Ev]),1e-9)
        print(f"n={n:2d} |I|={len(I):2d} k={k}: dim S2={full:3d} dim N={rN:3d} dim N^perp={full-rN:3d} dim Ext={rE:3d} rank(N+Ext)={rNE:3d} max|<N,Ext>|={np.abs(Nv.T@Ev).max():.1e} => Ext = N^perp: {rE==full-rN and rNE==full}")
