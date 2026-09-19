"""Run from cft_cmi/ after referee RRr confirms rigor/rate_of_remainder.tex: replace the log^-2 remainder claim of Note 5 Cor. 4.2 by the
integer-power expansion, update Note 7 Sec. 8 item 2 and paper 1 (sec_fidelity / sec_quadratic) accordingly."""
import re, datetime
log=open('rigor/errata_log.md','a'); log.write(f"\n## Errata applied {datetime.datetime.now():%Y-%m-%d %H:%M} — rate of the remainder (RR, RRr)\n")
def rep(p,old,new,why,regex=False):
    s=open(p).read()
    if regex:
        m=re.search(old,s,re.DOTALL)
        if m: s=s[:m.start()]+new+s[m.end():]; open(p,'w').write(s); log.write(f"- **{p}**: {why}\n"); print("ok  ",p[:26],why[:60]); return
    elif old in s: open(p,'w').write(s.replace(old,new,1)); log.write(f"- **{p}**: {why}\n"); print("ok  ",p[:26],why[:60]); return
    log.write(f"- **{p}**: ANCHOR NOT FOUND: {why}\n"); print("MISS",p[:26],why[:60])
N5='fidelity_recovered_quasifree.tex'
# Replace the body of Cor 4.2 from "The fourth-order coefficient is infinite." up to the end of the sentence containing "twice but not four times differentiable"
rep(N5, r"The fourth-order coefficient is infinite\.  Indeed the modes.*?at \\\(s=0\\\)\.",
    r"\emph{Corrected statement (2026-09-09, \texttt{rigor/rate\_of\_remainder.tex}, refereed).}  The expansion proceeds in integer powers, \(-\log\Fid(\zeta)=f_2\zeta^2\,[1+c_3\zeta+c_4\zeta^2+O(\zeta^3)]\) with \(c_3=-0.99(1)\) and \(c_4=+0.9(1)\) per fermion component; the remainder after the quadratic term is negative and of order \(\zeta^3\).  An earlier version of this corollary claimed a \(\log^{-2}(1/\zeta)\) correction from the saturated ultraviolet modes above \(\kappa_*(\zeta)\); that term double-counted a contribution already contained in \(\frac{\zeta^2}8\,(g_B-g_B^{(\kappa_*)})\), and it is refuted by the global bound \(-\log\Fid\le-\frac12\log(1-2f_2\zeta^2)=f_2\zeta^2(1+f_2\zeta^2+O(\zeta^4))\), obtained from the Uhlmann--Bogoliubov construction with the flow extension (for which \(\|V_s\|_2^2\le s^2\|P_-DP_+\|_2^2\) exactly and \(\det(1-V_s^*V_s)\) is even in \(s\)), which admits no cubic term, together with the numerically established \(c_3<0\).",
    "Cor 4.2: log^-2 claim replaced by the integer-power expansion", regex=True)
rep(N5, r"the stated \(\log^{-2}\) rate of the remainder remains open.", r"the remainder is \(c_3f_2\zeta^3+O(\zeta^4)\) with \(c_3=-0.99(1)\) (\texttt{rigor/rate\_of\_remainder.tex}); the \(\log^{-2}\) rate stated in an earlier version was wrong.", "Cor 4.2 label: rate")
N7='universality_normalization.tex'
rep(N7, r"the rate of the remainder remains open, and \texttt{rigor/tail\_bound.tex} shows that the \(\log^{-2}\) rate cannot be obtained from a window-tail bound combined with a cubic estimate)",
    r"the remainder is \(O(\zeta^3)\) with a negative cubic coefficient \(c_3=-0.99(1)\), and the \(\log^{-2}\) rate claimed earlier is refuted by the global bound \(\Phi\le-\frac12\log(1-2f_2\zeta^2)\) of \texttt{rigor/rate\_of\_remainder.tex})", "S8 item 2: rate corrected")
rep(N7, r"No interchange of limits and no tail estimate are needed; the remainder is \(o(\zeta^2)\) without a rate.", r"No interchange of limits and no tail estimate are needed; with the flow extension the bound is global, \(\Phi\le-\frac12\log(1-2f_2\zeta^2)\), and the remainder of the quadratic law is \(c_3f_2\zeta^3+O(\zeta^4)\), \(c_3=-0.99(1)\) (\texttt{rigor/rate\_of\_remainder.tex}).", "Thm A paragraph: rate")
log.close()

# ---- paper 1 ----
log=open('rigor/errata_log.md','a')
rep('paper1/sec_fidelity.tex', r" \Phi(\zeta)=f_2\zeta^2\bigl[1+O(\log^{-2}(1/\zeta))\bigr]:", r" \Phi(\zeta)=f_2\zeta^2\bigl[1+c_3\zeta+c_4\zeta^2+O(\zeta^3)\bigr],\qquad c_3=-0.99(1),\ c_4=+0.9(1):", "paper 1: expansion structure corrected")
rep('paper1/sec_fidelity.tex', r"a finite quadratic coefficient, but a remainder that is not a power of $\zeta$, so"+"\n"+r"that $s\mapsto\widetilde\omega_s$ is twice but not four times Bures differentiable"+"\n"+r"at $s=0$.  The quadratic coefficient itself is proved unconditionally in"+"\n"+r"\cref{sec:quadratic}; the $\log^{-2}$ rate remains open.",
    r"an expansion in integer powers with a negative cubic coefficient (a $\log^{-2}(1/\zeta)$ correction from the saturated ultraviolet modes, claimed in an earlier version, double-counted a contribution already contained in $\tfrac{\zeta^2}{8}(g_B-g_B^{(\kappa_*)})$ and is excluded by the global bound $\Phi\le-\tfrac12\log(1-2f_2\zeta^2)$ of \cref{sec:quadratic}).  The quadratic coefficient itself is proved unconditionally in"+"\n"+r"\cref{sec:quadratic}; the cubic coefficient is established numerically \cite{RigorRR}.", "paper 1: remainder paragraph")
rep('paper1/sec_quadratic.tex', r"(i) No rate: the expansion in step (iii) carries a qualitative $o(\zeta^2)$, so"+"\n"+r"$\Phi(\zeta)=f_2\zeta^2+o(\zeta^2)$ is all that follows.  A certified"+"\n"+r"$O(\zeta^3)$ or $O(\zeta^2\log^{-2}(1/\zeta))$ remainder still needs the tail"+"\n"+r"analysis behind \cref{prop:tail}.",
    r"(i) Rate: with the extension chosen as the flow of a fixed field, $s\mapsto\widetilde W_s$ is a one-parameter group and the exact identity of step (iii) gives $\|V_s\|_2^2\le s^2\|P_-DP_+\|_2^2$, hence the global bound $\Phi(\zeta)\le-\tfrac12\log(1-2f_2\zeta^2)=f_2\zeta^2(1+f_2\zeta^2+O(\zeta^4))$ with no cubic term \cite{RigorRR}; the lower bound of step (i) carries only $o(\zeta^2)$, so the sign and size of the cubic term, $c_3=-0.99(1)$, rest on numerics.", "paper 1: remark norate")
s=open('paper1/main.tex').read()
if 'RigorRR' not in s:
    s=s.replace(r"\bibitem{Ruij77}", r"\bibitem{RigorRR} Internal rigor document \texttt{rigor/rate\_of\_remainder.tex}: global Uhlmann bound and the cubic coefficient (2026-09-09)."+"\n"+r"\bibitem{Ruij77}",1); open('paper1/main.tex','w').write(s); print("bibitem RigorRR added")
log.close()
