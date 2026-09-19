"""Run from cft_cmi/ after QA's and QB's post-referee repairs are confirmed: record the universality theorem in N7, N8 and paper 2."""
import datetime
log=open('rigor/errata_log.md','a'); log.write(f"\n## Additions {datetime.datetime.now():%Y-%m-%d %H:%M} — universality theorem established (QA, QB, QR1, QR2)\n")
def rep(p,old,new,why):
    s=open(p).read()
    if old in s: open(p,'w').write(s.replace(old,new,1)); log.write(f"- **{p}**: {why}\n"); print("ok  ",p[:26],why[:60])
    else: log.write(f"- **{p}**: ANCHOR NOT FOUND: {why}\n"); print("MISS",p[:26],why[:60])
N7='universality_normalization.tex'
rep(N7, r"\item \textbf{Theorem B (any diffeomorphism covariant net; the Bures statement now rests on the proved fidelity half of Lemma~\ref{lem:second-variation}, the Kubo--Mori statement remains conditional",
    r"\item \textbf{Theorem B (any diffeomorphism covariant net on \(S^1\); Bures statement now a theorem: \texttt{rigor/universality\_theorem\_B.tex} Thm~7.1 with hypotheses (H1)--(H3) proved for every such net in \texttt{rigor/implementation\_C11.tex} Thm~5.1, both refereed; the Kubo--Mori statement remains conditional",
    "Theorem B header: established")
rep(N7, r"Status: the fidelity (Bures) half is proved for every von Neumann algebra with cyclic separating vector (\texttt{rigor/lemma\_second\_variation.tex}); the Kubo--Mori half is proved only in finite dimensions.  For the free fermion both are bypassed.",
    r"Status: the fidelity (Bures) half is proved for every von Neumann algebra with cyclic separating vector (\texttt{rigor/lemma\_second\_variation.tex}), and Theorem~B itself is established for every diffeomorphism covariant net on \(S^1\) (\texttt{rigor/universality\_theorem\_B.tex}, \texttt{rigor/implementation\_C11.tex}, refereed): the implementer \(U_s=e^{isT(g_{\rm tot})}\) exists by the Carpi--Weiner energy bound because \(g_{\rm tot}\) is \(C^{1,1}\) with a single jump of the second derivative, and \(c\)-linearity of \(g_B\) follows because the stress-tensor subspace reduces \(\Delta\) and \(J\).  The Kubo--Mori half is proved for unitary orbits with generator affiliated with the algebra (\texttt{rigor/kubo\_mori\_second\_variation.tex}); for \(T(g_{\rm tot})\), which is not affiliated with \(\cA(I)\), a gauge lemma is still missing.  For the free fermion both are bypassed.",
    "S8 item 1: Theorem B established")
N8='open_problems_plan.tex'
rep(N8, r"\item \textbf{O3+O5: existence and identification at zero collar for general nets.}",
    r"\item \textbf{O3+O5: existence and identification at zero collar for general nets.}  \emph{Status 2026-09-08: closed in the reformulated form — Theorem~B holds for every diffeomorphism covariant net (\texttt{rigor/universality\_theorem\_B.tex}, \texttt{rigor/implementation\_C11.tex}, both refereed).}",
    "mainbox O3+O5 status")
P2='paper2/main.tex'
rep(P2, r"[To write. Claim: for every diffeomorphism covariant conformal net on the circle with central charge $c$ satisfying Haag duality, and for which the piecewise-M\"obius compression map of three adjacent intervals is implemented by unitaries $U_s$ with the differentiability properties (H1)--(H3), the zero-collar Petz recovery error obeys",
    r"[To write. Main theorem (proved, refereed, 2026-09-08): for every diffeomorphism covariant conformal net on the circle with central charge $c$ (separable vacuum Hilbert space, standard axioms), the piecewise-M\"obius compression map of three adjacent intervals is implemented by unitaries $U_s=e^{isT(g_{\rm tot})}$ (Carpi--Weiner energy bound; the first-order field is $C^{1,1}$ with one jump of the second derivative) and the zero-collar Petz recovery error obeys",
    "paper 2 abstract: theorem established")
log.close()
