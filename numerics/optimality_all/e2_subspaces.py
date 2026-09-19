import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))
"""E2 (a): dimensions of N, N^perp, Ext in S_2(PH,P^perp H); is Ext = N^perp?
Two independent computations:
 (A) brute force at small L: explicit real bases, ranks by SVD (relative tolerance),
     principal angles between Ext and N^perp, and the check Ext subset N^perp (L1).
 (B) the analytic Gram diagonalisation (e2_common): the map l -> P^perp l P is
     multiplication by den_ij in the Q-eigenbasis, Z -> P^perp Z P by denc_ij in the
     Qc-eigenbasis, so the singular-value spectra are sqrt(den_ij/2), sqrt(denc_ij/2)
     and the ranks are the counts of nonzero den / denc.
Predicted exactly:  dim N = m^2 - 2 z^2,  z = m - L/2,  dim N^perp = (L-m)^2 = dim Ext.
"""
import sys, numpy as np
sys.path.insert(0, _os.path.join(_ROOT, 'numerics/optimality_all'))
import e2_common as E

def bases(S):
    L = S['L']; P = S['P']; Pp = S['Pp']; I = S['I']; Ic = S['Ic']
    w, Vv = np.linalg.eigh(P); k = int(round(w.sum()))
    Vp = Vv[:, -k:]; Vm = Vv[:, :L-k]                     # ran P, ran P^perp
    def coord(X):                                          # A = P^perp X P -> real vector
        C = Vm.conj().T@X@Vp
        return np.concatenate([C.real.ravel(), C.imag.ravel()])
    BN = []
    for i, ii in enumerate(I):
        for j, jj in enumerate(I):
            if jj < ii: continue
            l = np.zeros((L, L), complex)
            if ii == jj: l[ii, ii] = 1.0; BN.append(coord(l))
            else:
                l[ii, jj] = 1.0; l[jj, ii] = 1.0; BN.append(coord(l))
                l = np.zeros((L, L), complex); l[ii, jj] = 1j; l[jj, ii] = -1j; BN.append(coord(l))
    BE = []
    for i, ii in enumerate(Ic):
        for j, jj in enumerate(Ic):
            if jj < ii: continue
            Z = np.zeros((L, L), complex)
            if ii == jj: Z[ii, ii] = 1j; BE.append(coord(Z))
            else:
                Z[ii, jj] = 1.0; Z[jj, ii] = -1.0; BE.append(coord(Z))
                Z = np.zeros((L, L), complex); Z[ii, jj] = 1j; Z[jj, ii] = 1j; BE.append(coord(Z))
    return np.array(BN).T, np.array(BE).T, 2*(L-k)*k

def rank_sv(Amat, rtol=1e-10):
    sv = np.linalg.svd(Amat, compute_uv=False)
    return int((sv > rtol*sv[0]).sum()), sv

if __name__ == "__main__":
    print("=== (B) analytic Gram diagonalisation (all L); ranks at relative tolerance ===")
    print("gains of  l -> P^perp l P  are sqrt(den_ij/2), of  Z -> P^perp Z P  are sqrt(denc_ij/2);")
    print("max gain = 1/sqrt(2) = 0.7071.  rank(tau) := #{gains > tau * maxgain}.")
    TOLS = (1e-6, 1e-8, 1e-10, 1e-12)
    for L in (96, 128, 192, 256, 384):
        S = E.build(L=L); m = len(S['I']); mc = len(S['Ic']); k = L//2; z = m-k
        den, dc = S['den'], S['denc']; dS2 = 2*k*(L-k)
        gN = np.sqrt(den/2).ravel(); gE = np.sqrt(dc/2).ravel(); gmax = 1/np.sqrt(2)
        print(f"L={L:>4} m={m:>4} |Ic|={mc:>4} k={k:>4} dim S2={dS2:>6} | EXACT prediction: "
              f"dim N = m^2-2z^2 = {m*m-2*z*z}, dim N^perp = dim S2 - dim N = {dS2-(m*m-2*z*z)}"
              f" = (L-m)^2 = {mc*mc} = dim Ext (max possible)")
        for tau in TOLS:
            rN = int((gN > tau*gmax).sum()); rE = int((gE > tau*gmax).sum())
            print(f"      tau={tau:.0e}:  rank N={rN:>6}  dim N^perp={dS2-rN:>6}  rank Ext={rE:>6}"
                  f"   (rank Ext)-(dim N^perp) = {rE-(dS2-rN):>6}")
        qs = np.quantile(np.log10(gE[gE > 0]), [0, .05, .25, .5, .75, 1.0])
        qn = np.quantile(np.log10(gN[gN > 0]), [0, .05, .25, .5, .75, 1.0])
        print("      log10 gain quantiles  Ext: " + " ".join(f"{x:6.2f}" for x in qs)
              + "   |  N: " + " ".join(f"{x:6.2f}" for x in qn))
    print()
    print("=== (A) brute force: explicit bases, SVD ranks, principal angles ===")
    for L in (32, 48, 64):
        S = E.build(L=L); BN, BE, dS2 = bases(S)
        rN, svN = rank_sv(BN); rE, svE = rank_sv(BE)
        QN, _ = np.linalg.qr(BN[:, :]); QN = QN[:, :rN]
        # orthonormal basis of N (economical): use SVD
        UN = np.linalg.svd(BN, full_matrices=False)[0][:, :rN]
        UE = np.linalg.svd(BE, full_matrices=False)[0][:, :rE]
        # N^perp basis: complement of UN inside R^dS2
        Full = np.eye(dS2)-UN@UN.T
        UP = np.linalg.svd(Full, full_matrices=False)[0][:, :dS2-rN]
        cang = np.linalg.svd(UE.T@UP, compute_uv=False)        # cosines of principal angles
        over = np.linalg.svd(UE.T@UN, compute_uv=False)        # should be ~0 (L1)
        m = len(S['I']); mc = len(S['Ic']); k = L//2; z = m-k
        print(f"L={L:3d} m={m:3d} mc={mc:3d} dimS2={dS2:5d} | rank N={rN:5d} (pred {m*m-2*z*z:5d})"
              f"  rank Ext={rE:5d} (pred {mc*mc:5d})  dim N^perp={dS2-rN:5d}")
        print(f"      Ext vs N^perp: cos(angle) min={cang.min():.10f} max={cang.max():.10f}"
              f"   |  Ext vs N overlap max={over.max():.3e}   [Ext=N^perp iff all cos=1]")
        print(f"      basis sv of Ext: max={svE[0]:.4e} min(kept)={svE[rE-1]:.4e}"
              f" first dropped={svE[rE] if rE < len(svE) else float('nan'):.4e}")
