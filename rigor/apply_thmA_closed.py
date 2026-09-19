"""Apply the 'Theorem A closed' status to the notes once PA's repairs after the referee report are confirmed. Run from cft_cmi/."""
import datetime
log=open('rigor/errata_log.md','a'); log.write(f"\n## Errata applied {datetime.datetime.now():%Y-%m-%d %H:%M} — Theorem A closed (PA + PR, Phase 1)\n")
def rep(p,old,new,why):
    s=open(p).read()
    if old in s: open(p,'w').write(s.replace(old,new,1)); log.write(f"- **{p}**: {why}\n"); print("ok  ",p[:24],why[:60])
    else: log.write(f"- **{p}**: ANCHOR NOT FOUND: {why}\n"); print("MISS",p[:24],why[:60])
N7='universality_normalization.tex'
rep(N7, r"is proved as a lower bound, \(\liminf_{\zeta\to0}\Phi/\zeta^2\ge r/(12\pi^2)\), without any interchange of limits (\texttt{rigor/quadratic\_limit.tex}, Thm~4.2); the matching upper bound is proved with the constant \(2\log2\cdot r/(12\pi^2)\) modulo one interchange of a supremum with the limit, and the sharp upper bound is open (ibid.\ Lemma~6.7, Problem~6.8).  Numerically the limit is confirmed to \(10^{-3}\).",
    r"is now a theorem: \(\liminf_{\zeta\to0}\Phi/\zeta^2\ge r/(12\pi^2)\) by data processing and the Legendre form of the SLD metric (\texttt{rigor/quadratic\_limit.tex}, Thm~4.2), and \(\limsup_{\zeta\to0}\Phi/\zeta^2\le r/(12\pi^2)\) by Uhlmann's inequality applied to the vector representative \(\Gamma(\widetilde W_s)^*\Omega\) obtained from a Bogoliubov extension of the compression map to a diffeomorphism, whose vacuum overlap is \(\det(1-V^*V)^{1/2}\) with \(V=P_-\widetilde W_sP_+\), and whose second-order expansion, minimized over the extension, is exactly \(\tfrac18g_B\) by the three-way identity (\texttt{rigor/uhlmann\_upper\_bound.tex}, refereed in \texttt{rigor/referee\_uhlmann\_upper\_bound.tex}).  No interchange of limits and no tail estimate are needed; the remainder is \(o(\zeta^2)\) without a rate.  Numerically the limit is confirmed to \(10^{-3}\), and the Uhlmann bound itself exceeds \(\Phi\) by \(0.2\%\) at \(\zeta=1/120\).",
    "Theorem A: limit proved (PA, PR)")
rep(N7, r"(Note~5, Corollary~4.2; status: \(\liminf\Phi/\zeta^2\ge g_B/8\) proved unconditionally and \(\limsup\le2\log2\cdot g_B/8\) modulo one interchange in \texttt{rigor/quadratic\_limit.tex}, the sharp upper bound open)",
    r"(Note~5, Corollary~4.2; status: done, \(\lim\Phi/\zeta^2=g_B/8\) proved by \texttt{rigor/quadratic\_limit.tex} Thm~4.2 together with \texttt{rigor/uhlmann\_upper\_bound.tex}; only the rate of the remainder remains open)",
    "S8 item 2: done")
N5='fidelity_recovered_quasifree.tex'
rep(N5, r"\texttt{rigor/quadratic\_limit.tex} proves unconditionally \(\liminf_{\zeta\to0}\Phi/\zeta^2\ge g_B/8\) and \(\Phi(\zeta)\le\tau/(1-\tau)\) with \(\tau=\frac r{2\pi}\log(1+\zeta)\), and \(\limsup\Phi/\zeta^2\le2\log2\cdot g_B/8\) modulo one interchange of limits; the sharp upper bound and the stated rate remain open there (Problems~6.8, 7.2).",
    r"\texttt{rigor/quadratic\_limit.tex} proves unconditionally \(\liminf_{\zeta\to0}\Phi/\zeta^2\ge g_B/8\) and \(\Phi(\zeta)\le\tau/(1-\tau)\) with \(\tau=\frac r{2\pi}\log(1+\zeta)\), and \texttt{rigor/uhlmann\_upper\_bound.tex} proves \(\limsup\Phi/\zeta^2\le g_B/8\) through Uhlmann's inequality with a Bogoliubov extension of the compression map; hence \(\lim_{\zeta\to0}\Phi/\zeta^2=g_B/8\) is a theorem, while the stated \(\log^{-2}\) rate of the remainder remains open.",
    "Cor 4.2: limit proved")
N8='open_problems_plan.tex'
rep(N8, r"\textbf{Definition of done.} A Lamport proof of the tail bound and of the sharp limit, refereed; the certified error bar of the tabulated \(\Phi\) values replaces the heuristic \(0.3\)--\(1\%\).",
    r"\textbf{Definition of done.} A Lamport proof of the tail bound and of the sharp limit, refereed; the certified error bar of the tabulated \(\Phi\) values replaces the heuristic \(0.3\)--\(1\%\).  \emph{Status (2026-09-08): the sharp limit is proved by a different route, Uhlmann's inequality with a Bogoliubov extension of the compression map (\texttt{rigor/uhlmann\_upper\_bound.tex}, refereed), which needs no tail bound and no interchange; the tail bound is now only needed for the rate and for certified numerics.}",
    "O1 status")
log.close()
