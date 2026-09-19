"""Errata for N5 (fidelity_recovered_quasifree.tex), N6 (strategy_open_problems.tex), N7 (universality_normalization.tex).
Run from cft_cmi/ AFTER agents V5, P1, P2, P4 have finished.  Each edit is anchor-based; failures are reported, not silently skipped."""
import re, datetime, sys
log=open('rigor/errata_log.md','a'); log.write(f"\n## Errata applied {datetime.datetime.now():%Y-%m-%d %H:%M} — N5, N6, N7\n")
def edit(path, pairs, regex=False):
    s=open(path).read(); n=0
    for old,new,why in pairs:
        if regex:
            m=re.search(old, s, re.DOTALL)
            if m: s=s[:m.start()]+new+s[m.end():]; n+=1; log.write(f"- **{path}**: {why}\n")
            else: log.write(f"- **{path}**: ANCHOR NOT FOUND: {why}\n"); print("NOT FOUND:", path, why[:70])
        else:
            if old in s: s=s.replace(old,new,1); n+=1; log.write(f"- **{path}**: {why}\n")
            else: log.write(f"- **{path}**: ANCHOR NOT FOUND: {why}\n"); print("NOT FOUND:", path, why[:70])
    open(path,'w').write(s); print(path, n, "edits")
N5='fidelity_recovered_quasifree.tex'; N6='strategy_open_problems.tex'; N7='universality_normalization.tex'
TWO_BRANCH=(r"For a two-dimensional CFT the Bisognano--Wichmann boost dilates the two light-ray coordinates oppositely, so the rotated Petz map with parameter \(t\) acts as \(t\) on one chirality and as \(-t\) on the other: with \(z=\eta_{\mathrm V}/(1-\eta_{\mathrm V})\), "
 r"\[ -\log F^{(\lambda)}(\eta_{\mathrm V})=\Phi_{c}\bigl(z(1+e^{-\pi\lambda})\bigr)+\Phi_{\bar c}\bigl(z(1+e^{\pi\lambda})\bigr), \] "
 r"which is even in \(\lambda\) with its minimum at \(\lambda=0\); at small \(\eta_{\mathrm V}\) and \(c=\bar c\) it equals \(\frac{c}{12\pi^2}\eta_{\mathrm V}^2\,[2+4\cosh\pi\lambda+2\cosh2\pi\lambda]\).  This is consistent with the observation of \cite{VardhanWeiZou} that the fidelity is maximal at \(\lambda=0\) (and with the exact symmetry \(F^{(\lambda)}=F^{(-\lambda)}\) of real lattice states), and it reproduces their exponents \(p\approx2.0,1.9,1.7,1.2\) at \(\lambda=0,0.5,1,1.5\) as \(2.04,2.04,1.96,1.31\).  The collapse onto a single function of one variable is a statement about a single chirality.")
if __name__=="__main__":
    pass  # edits are appended below by the orchestrator once anchors are verified
