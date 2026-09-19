# Referee report PP2 — paper2, "Universality of the Petz recovery error in conformal nets"

Referee PP2 (Phase 3, adversarial pass with concrete edits). Date 2026-09-09.
Draft: `paper2/main.tex`, `paper2/sec_*.tex`, `paper2/app_conventions.tex` (24 pp.).
Authoritative sources: `rigor/universality_theorem_B.tex` (Thm 7.1 + §9 QR1 corrections),
`rigor/implementation_C11.tex` (Thm 5.1 + §8 QR2 corrections), `rigor/referee_universality_theorem_B.tex`,
`rigor/referee_implementation_C11.tex`, `rigor/lemma_second_variation.tex`,
`rigor/kubo_mori_second_variation.tex` (QK), `rigor/kubo_mori_gauge_lemma.tex` (RK — gauge lemma REFUTED),
`rigor/uhlmann_upper_bound.tex`, `rigor/rate_of_remainder.tex`, `numerics/boson/README.md` +
`boson_recovery.out`, `rigor/phase2_brief.md`, `rigor/phase2b_brief.md`, `rigor/PHASE2_STATUS.md`,
`rigor/findings.tex`/`findings.pdf`, `rigor/errata_log.md`.

**Overall verdict.** After the 25 edits listed below the draft is consistent with the rigor documents in
their final (post-referee) form. Before the edits there was one *serious* class of defect — the Kubo–Mori
gauge lemma was presented as **open** and $s_2=c/12$ as a **conditional theorem**, in the abstract, the
introduction, §6 and the appendix table, although `kubo_mori_gauge_lemma.tex` (2026-09-09) **refutes** it —
plus two arithmetic slips (abstract "one quarter" for "one half"; an inverted normalisation factor) and one
number corrected during the audit that had reappeared ($c_3=-0.96$, corrected to $-0.99(1)$).
No proof-breaking issue in the mathematics as such was found.

## Statements

Every theorem, proposition and lemma was compared with its source in the source's final form.

| paper | source | verdict |
|---|---|---|
| `thm:B` (sec_universality:294) | `universality_theorem_B.tex` Thm 7.1 (`thm:B`) | **matches verbatim**: hypotheses (HD),(BW),(RS) + (H1),(H2)–(H2'),(H3); $\zeta=as/(a+L)|_{a=\infty}=s$; $g_B=2c/3\pi^2$; $f_2=g_B/8=c/12\pi^2$. The paper additionally upgrades it to *unconditional* by `thm:impl`; the source calls it "Conditional universality" only because (H1)–(H3) are hypotheses there. Legitimate. |
| `H1` + `eq:H1loc` (sec_setting:100) | QR1 **R2** | **matches**: $U(\mathrm{Diff}(K))\subseteq\cA(K)$, $\mathrm{Diff}(K)=\{\phi:\phi|_{K'}=\mathrm{id}\}$; the ill-posedness of the "$\operatorname{supp}\phi\subset K$" phrasing in `lem:ext` is reproduced (sec_setting:116–119, 172). |
| `H2` + clause **(H2')** (sec_setting:121) | QR1 **R1**, QR2 **R8** | **matches**: $T(g_{\rm tot})\Omega=\lim_nT(f_n)\Omega$ with $\|g_{\rm tot}-f_n\|_{H^{3/2}}\to0$, i.e. $a\in\HT$; supplied by the Carpi–Weiner bound (`lem:CW`, `lem:loc`(ii)); its role in `thm:linear` is spelled out (sec_setting:141–145). |
| `H3` (sec_setting:131) | source (S6) | **matches**; (H2)$\Rightarrow$(H3) recorded (sec_setting:144) = QR1 R4(c). |
| standing assumptions (sec_setting:2–29) | QR2 **R5**, (C4) | **matches**: separable $\Hil$, CDIT §4 axioms (1)–(10), (HD), (BW), (RS); the note that only locality (not (HD)) is used in the upper bound is correct, though `thm:linear` uses not even locality (see *proposed* P1). |
| `rem:graded` (sec_universality:208) | QR1 **R3** | **matches**: Haag duality **fails** for the Dirac net, twisted duality $\cF(I)'=Z\cF(I')Z^*$, $Z=(1+iV)/(1+i)$ (Foit); $J=Z\Theta$, $\Ad Z$ trivial on even operators, $Z\Omega=\Omega$. |
| `lem:phase` (sec_implementation:70) | QR2 **R1** | **matches**: Fewster–Hollands Prop. 5.1, eqs. (5.7)–(5.8), multiplier $e^{ic\widetilde B}$, CDIT Prop. 3.14, perfectness of $\mathrm{Diff}(I)$; both uses involve fields supported in a proper interval. |
| `prop:energy`(iii) (sec_implementation:196) | QR2 **R2** (`verdictbreak`) | **matches**: form threshold exactly $\beta=1$ (sup over $\psi_t=\Omega+t\|L_{-n}\Omega\|^{-1}L_{-n}\Omega$ $\sim(c/12)^{1/2}n$), $\beta=1$ from CW Lemma 4.1, route **closed** by the single logarithm $\|g_{\rm tot}'\|_1=\infty$. **The retracted "open window $\tfrac12\le\beta<1$" does not appear anywhere.** |
| `thm:H1`(ii) (sec_implementation:130) | QR2 **R7** | **matches**: Trotter split $(g_{\rm tot}-m)+m$, explicitly *not* $g_A+g_D$ (because $g_{\rm tot}(L)\ne0$); $e^{iaT(m)}=U(h_a)$ **exactly**, no "up to a phase". |
| sign $[L_0,T(g)]=+iT(g')$ (sec_implementation:197) | QR2 **R4** | **matches**. |
| `thm:reg` (sec_implementation:15) | `implementation_C11.tex` Thm 2.3 | **matches** (a)–(g) item by item, including $(in)^3\hat G_n\to J/2\pi$, $\|G'\|_{3/2}=2|J|\sqrt N/\pi+O(\log N)$, $T(G)\Omega\in D(L_0^{1/2})\setminus D(L_0)$ with $\frac{J^2}{4\pi^2}\log N$. Locator was wrong (Thm 3.1 → 2.3), fixed. |
| `thm:impl` (sec_implementation:166) | `implementation_C11.tex` Thm 5.1 | **matches**. The list of "exactly three external inputs" omitted **Haag duality**, which the source's (X3) names and which `thm:H1`(i) uses through $\cA(A_0)'=\cA(A_0')$ — fixed. |
| `thm:value` (sec_universality:220) | `universality_theorem_B.tex` §7.2 + `uhlmann_upper_bound.tex` Prop. "The infimum" | **matches**: $\gamma_0=2/3\pi^2$ obtained from $c$-linearity **plus the free fermion** ($\mathrm{dist}^2=1/6\pi^2$), *not* from an $x$-space evaluation. |
| `rem:mellin` (sec_universality:248) | `universality_theorem_B.tex` §7.3 `verdictgap` | **matches**, all three points (finite spectral measure; $\mu$ is not the spectral measure of $a$; the $\lambda$-form needs $A\in\cM$), including the disjoint-strip obstruction $\operatorname{Re}\sigma<1$ vs $\operatorname{Re}\sigma>3$ and the reason $g_{\rm tot}(L)\ne0$. |
| `thm:three`, `thm:alberti`, `thm:uhlmann`, `thm:secvar` (sec_second_variation) | `lemma_second_variation.tex` Lemma "Explicit real-orthogonal projection", Thm "Three faces", Thm "Upper bound", Thm "Lower bound", Thm "Type-III second variation" | **matches**, including the *direction* of the two citations (source "Upper bound" = $\liminf(1-F)/s^2\ge$, cited by `thm:alberti`; source "Lower bound" = $\limsup\le$, cited by `thm:uhlmann`) and $E'b=\Delta(1+\Delta)^{-1}b+(1+\Delta)^{-1}\Delta^{1/2}Jb$. |
| `thm:kmexact`, `thm:kmlower`, `thm:kmupper` (sec_kubo_mori) | QK Thm 3.3, Thm 4.1, Thm 5.8/5.9, Lemma 3.5 | **matches**, incl. the sum rule $\int(\lambda-1)d\nu_s=0$ and $\|h(\Delta)^{1/2}A\Omega\|^2=\tfrac12\gKM$. Locators §2→§6 and §8→§7 were wrong, fixed. |
| Kubo–Mori **gauge lemma** (sec_kubo_mori:83–92, 120–125; sec_intro:70–74; abstract) | RK `thm:gauge` (**refuted**) | **WAS WRONG**: stated as "(open)" with $s_2=c/12$ "conditional … once the gauge lemma is proved". RK proves $\inf_{K,\hat g}\gKM^{(K)}=(11+5\sqrt5)c/12=11.09\times c/6$. Fixed everywhere; $s_2=c/12$ now a **conjecture**, with the proved bracket. |
| `sec_boson` | `numerics/boson/README.md`, `boson_recovery.out` | **matches verbatim** (conventions, modular frame, validation, table, fits, values, $c$-linearity). |

## Numbers

Checked against the sources; "OK" means byte-for-byte agreement with the source value.

* $\langle\Omega,T(x)T(y)\Omega\rangle=\frac{c}{8\pi^2}(x-y-i0)^{-4}$ — OK (`eq:TT`, `eq:appTT`), BPZ field $2\pi T$ with $\frac c2(x-y)^{-4}$ — OK.
* $\|T(f)\Omega\|^2=\frac{c}{48\pi^2}\int_0^\infty p^3|\hat f|^2dp$ (line) and $\frac c{12}\sum_{n\ge2}n(n^2-1)|\hat G_n|^2$ (circle) — OK; the bridge $\int e^{-ipu}(u-i0)^{-4}du=\frac{2\pi}{3!}|p|^3\theta(-p)$ — OK.
* $\gamma_0=2/(3\pi^2)=0.0675$, $g_B=2c/(3\pi^2)$, $f_2=g_B/8=c/(12\pi^2)$, $1/(12\pi^2)=0.0084434$ — OK. Free-fermion $\mathrm{dist}^2=1/(6\pi^2)=0.016886863$ (`uhlmann_upper_bound.tex` Prop. "The infimum") — OK.
* Consistency of the variational constant: $\tfrac14 g_B=\frac{c}{48\pi}\inf\|G\|_{3/2}^2$ with $\|G\|_{3/2}^2=\int|p|^3|\hat G|^2\frac{dp}{2\pi}$ gives $\inf\|G\|^2_{3/2}=8/\pi=2.546479$ — OK (independently re-derived here). Rayleigh–Ritz $2.5678/2.5630/2.5579$ at $\ell=512/1024/2048$, 27 trial functions — OK; box-free $2.547971$, $0.06\%$ — OK (`findings.tex` entry QR1, `referee_universality_theorem_B.tex` §"A sharper, box-free check").
* Modular frame: $\widehat W(k)=\frac{c}{24\pi}\frac{k(k^2+1)}{e^{2\pi k}-1}$, $\tilde g(\xi)=-4\sinh^2\frac\xi2$, $\hat{\tilde g}(k)=-2i/(k(k^2+1))$, $g_B=\frac{c}{6\pi^2}\int_{\mathbb R}\frac{\tanh\pi k}{k(k^2+1)}dk=\frac{2c}{3\pi^2}$ — OK (source: $\int_0^\infty=2$, so $\int_{\mathbb R}=4$; $4c/6\pi^2=2c/3\pi^2$).
* **Jump of the second derivative — was wrong in the appendix.** Source: $\tilde k_s''(0^+)=-2s/L$ (line chart) and $J:=G''(0^+)-G''(0^-)=-1/L$ (circle representative). `sec_setting.tex:73` had it right ("$-2/L$ in the line chart, equivalently $-1/L$ for the circle representative"); `app_conventions.tex:58` said "a single jump $-1/L$ of $g_{\rm tot}''$", i.e. the circle value attached to the line-chart field, and the constants table attributed $J_{\rm jump}=-1/L$ to $g_{\rm tot}''$. Both fixed.
* Logarithmic divergence coefficient $\frac c{12}\cdot\frac{J^2}{4\pi^2}$; $\|G'\|_{3/2}$ partial sum $\frac{2|J|}{\pi}\sqrt N+O(\log N)$; $\|T(f)\Omega\|=(\frac c{12}n(n^2-1))^{1/2}$ for $f=2\cos n\theta$ (QR2 R3, factor 4) — all OK.
* $\|\Pi_-\mathfrak L_f\Pi_+\|^2_{\mathfrak S_2}=\frac1{48\pi^2}\int_0^\infty p^3|\hat f|^2dp$, numerically $1.5\cdot10^{-11}$ — OK (`phase2_brief.md` l. 99).
* Boson (all verbatim from `numerics/boson/README.md`): $\langle JJ\rangle$, $\Sigma(f,g)=\frac1{4\pi}\int fg'$, $V(f,g)$, $M(k)=\pi k\coth\pi k$, $\nu(k)=\coth\pi k$; $a=1,L=2,\zeta=s/3$; $\Lambda=2\sigma\sqrt{2N}$, $\kappa_{\max}=\sqrt{2N}/\sigma$, $\epsilon=10^{-14}\Rightarrow\kappa_c=5.24$; validation $2\cdot10^{-13}$–$6\cdot10^{-3}$, $\nu_{\rm med}=1.000000000$, $4\cdot10^{-15}$, $8\cdot10^{-8}$; the $\kappa_c$ table (0.007915…0.008405 / 0.059029…0.076322); free exponents $p=2.3$–$2.8$ and $1.14$–$1.39$; $f_2=0.00844(2)$, $s_2=0.083(2)$; finite-$s$ $0.00744/0.00789/0.00804$ — **all OK**.
* Boson $c$-linearity: $\mathcal E=\frac{s^2}{48\pi^2}\int_0^\infty k^3|\hat g|^2$, $\Tr(B^*B)=2\mathcal E$, overlap $\frac{s^2}{96\pi^2}\int_0^\infty k^3|\hat g|^2=\frac{s^2}2\|T(g)\Omega\|^2|_{c=1}$ — OK and internally consistent with `eq:normTg`; $6.7182/6.7234=0.99923$, $0.08\%$, $s=0.1$, $|k|\le60$, $X=100$ — OK. The intro copy of this formula had no integration limits (fixed).
* Kubo–Mori: $\gKM=\frac12\int\frac{I(u)du}{u(u^2+4\pi^2)^2}=\frac13\int\frac{du}{u^2+4\pi^2}=\frac16$ — OK (QK eq. (ff-result)). Gauge infimum $(11+5\sqrt5)c/12=1.848c=11.09\times c/6$ at $R_*=(3+\sqrt5)/2$ — OK; $\limsup\le(11+5\sqrt5)c/24=0.9242c$ — OK; $\liminf\ge\frac12g_B=c/(3\pi^2)=0.0338c$ — OK; free-fermion $s_2=0.0837(5)$ — OK (`numerics/boson/README.md` l. 5).
* **$c_3$ — a value corrected during the audit had reappeared.** `sec_outlook.tex:15` said $c_3\approx-0.96$; `rate_of_remainder.tex` eq. (16) boxes $c_3=-0.99\pm0.01$ and `referee_rate_of_remainder.tex` §5.2 states explicitly that "$c_3=-0.96$, $c_4=0$ (the brief's reading) is off by $1.9\cdot10^{-4}$" against the published table. Fixed to $c_3=-0.99(1)$.
* **Abstract arithmetic.** "The coefficient is one quarter of the squared Bures distance of $T(g_{\rm tot})\Omega$ to $\overline{\cM'_{\rm sa}\Omega}$" is wrong by a factor 2: $f_2=g_B/8=\tfrac12\mathrm{dist}^2$ (check at $c=1$: $\tfrac12\cdot\frac1{6\pi^2}=\frac1{12\pi^2}$). Fixed to "one half".
* **Inverted normalisation factor.** `sec_universality.tex:198`: with $V[f]=(48\pi^2/c)^{1/2}T(f)\Omega$ unitary, $V^{-1}a=(c/48\pi^2)^{1/2}[g_{\rm tot}]$, not $(48\pi^2/c)^{1/2}[g_{\rm tot}]$; the display that follows ($\tfrac14g_B=\frac{c}{48\pi^2}\cdot\tfrac12\|\cdots\|_\star^2$) already uses the correct factor, and reproduces $\inf\|G\|_\star^2=8$, i.e. $8/\pi$ in the $\frac{dp}{2\pi}$ normalisation. Fixed. **The same slip is present in the source**, `universality_theorem_B.tex` §5.2 step $\langle1\rangle2$ — reported for correction there.

## Forbidden content

All five prohibited items were searched for explicitly; none is present (after the edits).

1. **$\Delta^{1/2}$ fidelity formula** — absent. `grep` for `Delta^{1/2}`/`Delta^{-1/2}` in `paper2/` returns only the modular operators $S=J\Delta^{1/2}$, $F=J\Delta^{-1/2}$ and `eq:Eprime`, all legitimate.
2. **"the smooth extension legitimises the $x$-space Mellin evaluation"** — the paper says the opposite, in `rem:mellin`: "the modular-frame route is a *prescription*, not a proof, and the smooth extension does *not* legitimise it", followed by the three points of the source's `verdictgap`. Correct.
3. **Kosaki / Petz–Donald as an upper-bound route** — `rem:kosaki` records it as *refuted* ("those expressions are suprema … useless for a $\limsup$"); the Petz–Donald formula is used only for the *lower* bound in the closing paragraph. Correct.
4. **Old apparent exponents** — the retracted $2.04,2.04,1.96,1.31$ and the "exponents 2.0 and 1.0" of N5 do not occur; §7 quotes the measured $p=2.3$–$2.8$ / $1.14$–$1.39$ with the structural explanation. Correct.
5. **A gauge lemma stated as true** — it was not stated as *true*, but it was stated as **open**, and $s_2=c/12$ as a theorem *conditional on proving it*, in four places (abstract; `sec_intro.tex:70–74`; `sec_kubo_mori.tex:84` heading and `:121–124` Status box; `app_conventions.tex:73–76` table). Since RK **refutes** it, "conditional on a gauge lemma" asserted a false status: the condition can never be met, and the route is closed. This was the most serious defect and is now corrected everywhere; the closing paragraph of §6 (which already reported the refutation correctly) is now consistent with the rest of the paper.

## Consistency

* **Abstract vs. theorems.** Two mismatches, both fixed: the factor-2 slip ("one quarter") and the Kubo–Mori status ("conditional on a gauge lemma"). Everything else in the abstract is supported: the $C^{1,1}$ field with a single jump of $G''$ inside the Carpi–Weiner range (`thm:reg`(c),(f)), $-\log F=\frac{c}{12\pi^2}\zeta^2+o(\zeta^2)$ (`thm:B`), the $c$-linearity mechanism (`lem:reduce`, `thm:linear`), the value fixed by Paper 1 (`thm:value`), the boson numbers (§7).
* **Internal cross-references.** After recompilation: 0 LaTeX errors, 0 undefined references, 0 undefined citations, 24 pages. `\Cref` targets all resolve; the forward references from §2 to `thm:reg`, `thm:impl`, `lem:gauge`, `lem:ext`, `def:HT` are all correct.
* **External locators to the rigor documents.** Four were wrong and are fixed: `RigorC` Thm 3.1 → **Thm 2.3** (regularity), `RigorC` Thm 4.5 → **Thm 4.7** ((H1)); `RigorKM` §2 → **§6** (Kosaki), `RigorKM` §8 → **§7** (free-fermion $\gKM=1/6$). Verified against `implementation_C11.aux` and `kubo_mori_second_variation.aux`. Correct as they stood: `RigorKM` Thm 3.3, Lemma 3.5, §5; `RigorC` Lemma 4.2; the name-based locators into `RigorSV`, `RigorUB`; `CW` Thm 4.4 / Prop. 4.5 / Lemma 4.6 / Prop. 5.4 / Lemma 4.1; `CDIT` Prop. 2.2(3),(4),(5) / Prop. 3.14 / Prop. 4.1 / §4; `FH05` Prop. 5.1 eqs. (5.7)–(5.8); `AU02` p. 4 (1–4) and Thm 2(3); `Note5` Lemma 1.1; `BBP` Eq. (15).
* **Bibliography.** Nine of the twenty entries are internal program documents. `Note5`, `Note7`, `Paper1` and `RigorRK` were already marked; `RigorSV`, `RigorUB`, `RigorB`, `RigorC`, `RigorKM`, `RigorCol` were bare `\texttt{}` paths and are now prefixed "Internal rigor document" (edits E3–E8). Remaining cosmetic point: `\bibitem{AU02}` is keyed 02 (arXiv year) but dated 2000 (journal year) — harmless.
* **Logical structure.** The chain abstract → intro "what is unconditional and what is not" → `thm:B` → `thm:impl` is now sound: `thm:B` is stated under (H1)–(H3) and made unconditional by `thm:impl`, whose hypotheses are exactly the standing assumptions of §2.1. The two admitted gaps of the source that are *not* used by `thm:B` (the one-particle Reeh–Schlieder/BW density statement) are correctly confined to `rem:varform` and flagged there as a gap.
* **Graded case.** §4 uses the free fermion as the *input* of `thm:value`, not as a test of `thm:B` — matching QR1 R4(e) — and `rem:graded` supplies the twisted-duality justification. Consistent.
* **§6 vs. §7.** §6 now states $s_2=c/12$ as a conjecture; §7 correctly describes the boson number as "the only evidence for (6.1) beyond the free fermion". Consistent.

## Edits applied

25 edits, all applied to the draft; `pdflatex main.tex` run twice after each batch, 0 errors, 0 undefined references, 24 pages.

| # | file:line | old | new |
|---|---|---|---|
| E1 | `main.tex:33` | `The coefficient is one quarter of the squared Bures distance` | `… one half of the squared Bures distance` |
| E2 | `main.tex:37–41` | `and for which the value $s_{2}=c/12$ remains conditional on a gauge lemma;` | `but for which the value $s_{2}=c/12$ remains a \emph{conjecture}: the gauge lemma that would deliver it is refuted, and what is proved for a general net is the bracket $0.034\,c\le\liminf_{s\to0}s^{-2}D\le\limsup_{s\to0}s^{-2}D\le0.924\,c$;` |
| E3–E8 | `main.tex:98,100,102,104,106,107` | `\bibitem{RigorSV} \texttt{…}` (and RigorUB, RigorB, RigorC, RigorKM, RigorCol) | `\bibitem{RigorSV} Internal rigor document \texttt{…}` (idem) |
| E9 | `sec_intro.tex:72–74` | `the gauge lemma that would remove this discrepancy is open.  We therefore state $s_2=c/12$ \emph{conditionally} (\Cref{sec:km}) and are explicit about the missing step.` | `… is \emph{refuted}: its infimum over admissible gauges is $(11+5\sqrt5)c/12=11.09\times c/6$, not $c/6$.  We therefore state $s_2=c/12$ as a \emph{conjecture} (\Cref{sec:km}); what is proved there for a general net is the bracket $0.034\,c\le\liminf_{s\to0}s^{-2}D\le\limsup_{s\to0}s^{-2}D\le0.924\,c$.` |
| E10 | `sec_intro.tex:88` | `\frac{s^2}{96\pi^2}\int k^3|\hat g(k)|^2\,dk` | `\frac{s^2}{96\pi^2}\int_0^\infty k^3|\hat g(k)|^2\,dk` |
| E11 | `sec_universality.tex:198` | `Finally $V^{-1}a=(48\pi^{2}/c)^{1/2}[g_{\rm tot}]$` | `Finally $V^{-1}a=(c/48\pi^{2})^{1/2}[g_{\rm tot}]$` |
| E12 | `sec_implementation.tex:37` | `\cite[Thm.~3.1]{RigorC}` | `\cite[Thm.~2.3]{RigorC}` |
| E13 | `sec_implementation.tex:130` | `\cite[Thm.~4.5]{RigorC}` | `\cite[Thm.~4.7]{RigorC}` |
| E14 | `sec_implementation.tex:180–183` | `the net axioms including automatic additivity and semicontinuity and $U(\mathrm{Exp}f)=e^{iT(f)}$ mod phase for smooth $f$.` | `the net axioms, including automatic additivity and semicontinuity, Haag duality (used only in \Cref{thm:H1}(i), through $\cA(A_{0})'=\cA(A_{0}')$) and $U(\mathrm{Exp}f)=e^{iT(f)}$ mod phase for smooth $f$.` |
| E15 | `sec_kubo_mori.tex:81` | `Concretely, the missing statement is the following.` | `Concretely, the statement one would want is the following.  It is \emph{false}: see the final paragraph of this section, where its infimum is computed exactly and is larger than $c/6$ by a factor $11.09$.` |
| E16 | `sec_kubo_mori.tex:85` | `\textbf{Kubo--Mori gauge lemma (open).}` | `\textbf{Kubo--Mori gauge lemma (refuted).}` |
| E17 | `sec_kubo_mori.tex:113` | `We expect the same mechanism as in the Bures case to settle it: $\HT$ reduces the modular data of` | `Two of the three ingredients of the Bures mechanism do carry over, and are proved in \cite{RigorRK}; the third, the gauge lemma, does not.  Namely: $\HT$ reduces the modular data of` |
| E18 | `sec_kubo_mori.tex:119` | `\cite[\S8]{RigorKM}` | `\cite[\S7]{RigorKM}` |
| E19 | `sec_kubo_mori.tex:120` | `consistent with \eqref{eq:s2}.` | `consistent with \eqref{eq:s2} --- but this one-particle value is the analytic continuation of a divergent integral (final paragraph), so it does not by itself fix the constant for a general net.` |
| E20 | `sec_kubo_mori.tex:122–126` (Status box) | `$s_{2}=c/12$ is stated \emph{conditionally}: it follows from \Cref{thm:kmexact} and the above route once the Kubo--Mori gauge lemma is proved.  Unconditional at present are the exact identity \eqref{eq:kmexact}, the lower bound \eqref{eq:kmlower} for affiliated generators, and the numerical confirmation at $c=1$ of \Cref{sec:boson}.` | `$s_{2}=c/12$ is stated as a \emph{conjecture}, not as a conditional theorem: the route just described is \emph{closed}, the Kubo--Mori gauge lemma being false (final paragraph).  Unconditional at present are the exact identity \eqref{eq:kmexact}, the lower bound \eqref{eq:kmlower} for affiliated generators, the bracket $0.034\,c\le\liminf_{s\to0}s^{-2}D\le\limsup_{s\to0}s^{-2}D\le0.924\,c$ of the final paragraph, and the numerical confirmation at $c=1$ of \Cref{sec:boson}.` |
| E21 | `sec_kubo_mori.tex:133` | `is refuted \cite[\S2]{RigorKM}` | `is refuted \cite[\S6]{RigorKM}` |
| E22 | `sec_boson.tex:60` | `$\kappa_{c}=\log(2/\epsilon)/2\pi$` | `$\kappa_{c}=\log(2/\epsilon)/(2\pi)$` |
| E23 | `sec_outlook.tex:15` | `$c_{3}\approx-0.96$ per component` | `$c_{3}=-0.99(1)$ per component` |
| E24 | `app_conventions.tex:57–59` | `it is $C^{1,1}$ with a single jump $-1/L$ of $g_{\rm tot}''$ at the touching point.` | `it is $C^{1,1}$ with a single jump of its second derivative at the touching point, of size $-2/L$ in the line chart and $-1/L$ for the circle representative $G$ (\Cref{thm:reg}).` |
| E25 | `app_conventions.tex:78` and `:73–76` | `$J_{\rm jump}$ & $-1/L$ & \Cref{thm:reg}: jump of $g_{\rm tot}''$ …`; `$\gKM$ … \emph{(conditional)}`; `$s_{2}$ … \emph{(conditional)}` | `… jump of $G''$ at the touching point, $G$ the \emph{circle} representative; the line-chart field has $g_{\rm tot}''$ jumping by $-2/L$`; `\emph{(conjectural)} … an analytic continuation; the gauge lemma is refuted \cite{RigorRK}`; `\emph{(conjectural)} … proved bracket $0.034\,c\le\liminf\le\limsup\le0.924\,c$ \cite{RigorRK}` |

## Edits proposed (not applied — they touch wording or require an author decision)

* **P1** `sec_setting.tex:28`. "Only locality --- not (HD) --- is used in the upper bound and in the $c$-linearity theorem." `thm:linear` uses **neither** locality nor (HD) nor (RS) (QR1 R3; the theorem itself says so at `sec_universality.tex:185`). Suggested: "Only locality --- not (HD) --- is used in the upper bound, and the $c$-linearity theorem uses neither."
* **P2** `main.tex:77–78` (`\bibitem{DIT}`). The source records DIT19 as **NOT OBTAINED**, used only through CDIT's Outlook and Introduction. §5.4(b) cites `\cite{DIT}` "via the Outlook of `\cite{CDIT}`", which is honest, but the bibliography entry should carry the caveat, e.g. append "(consulted only through the Outlook of \cite{CDIT})".
* **P3** `sec_second_variation.tex:55`. `\cite[\S(B)]{RigorSV}` — there is no §(B) in `lemma_second_variation.tex`; "(B)" is a row of its status table. Suggested locator: `\cite[Prop. ``Identification of the two metrics in finite dimensions'']{RigorSV}`.
* **P4** `sec_kubo_mori.tex:141` (final paragraph). "the upper half under a uniform-integrability hypothesis on the negative part of $\log\Delta_K$ along the orbit" is a faithful paraphrase but not the hypothesis's name. RK labels it $(\mathrm V_\eps)$ *uniformly on the orbit* (Gap RK1), and proves $(\mathrm A_\eps)$ **fails** for every field compactly supported in $K$. Suggested: name $(\mathrm V_\eps)$ and add that modular analyticity is not available here.
* **P5** `sec_kubo_mori.tex:59–64` (`thm:kmupper`). The statement quoted is QK **Thm 5.9** (the second variation), while QK Thm 5.8 gives only the $\limsup$; the citation `\cite[\S5]{RigorKM}` is right but a theorem number would be sharper.
* **P6** `sec_boson.tex:14`. The boson section inherits the numerics' Fourier convention $\hat f(p)=\int fe^{+ipx}dx$, whereas `app_conventions.tex` fixes $\$\hat f(p)=\int fe^{-ipx}dx$. For real $f$ nothing quoted changes, but §7.1 should say which convention is in force, since the appendix claims every constant is traceable to it.
* **P7** `sec_universality.tex:282–283` (`rem:varform`). "it is known in the models where (H1)--(H3) were first verified" — I could not locate this claim in `universality_theorem_B.tex` (which admits `lem:RST` and (BW1) as GAPs without such a remark). Either cite the model computation or drop the clause. The companion gap (BW1), one-particle Bisognano--Wichmann, is not mentioned in the paper and could be added in the same sentence.
* **P8** `sec_universality.tex:294–308` (`thm:B`). The hypothesis list repeats (HD),(BW),(RS), which §2.1 already declares as standing facts; and the theorem assumes (H1)--(H3) and then declares itself unconditional in the same statement. Cleaner: state it unconditionally and put "(H1)--(H3), which hold by \Cref{thm:impl}" in the proof. Not applied because it is a restructuring.
* **P9** `rigor/universality_theorem_B.tex` §5.2, step $\langle1\rangle2$ (**source**, not the paper): `$V^{-1}a=(48\pi^2/c)^{1/2}[\gtot]$` has the factor inverted; it should be $(c/48\pi^2)^{1/2}$. Step $\langle1\rangle3$ already uses the correct factor, so nothing downstream changes. Flagged for the source's author.
* **P10** `sec_outlook.tex:14–19`. With $c_3=-0.99(1)$ the companion note also reports $c_4=+0.9(1)$ and that $c_3=-1$ lies inside the error bar; one sentence recording $c_4$ would make the "sharper law" quantitative.

## Summary of severity

* **Serious (fixed):** the Kubo--Mori gauge lemma presented as *open* and $s_2=c/12$ as a *conditional theorem* in the abstract, introduction, §6 heading, §6 Status box and the appendix table, contradicting `kubo_mori_gauge_lemma.tex` (refuted, factor $11.09$) and contradicting the paper's own closing paragraph of §6.
* **Moderate (fixed):** abstract factor 2 ("one quarter" vs "one half"); $c_3=-0.96$ (a value corrected during the audit) reappearing in §8; the jump $-1/L$ attributed to the line-chart field $g_{\rm tot}''$ in the appendix, contradicting §2.2.
* **Minor (fixed):** inverted factor in the $c$-linearity isometry; four wrong locators into the rigor documents; Haag duality missing from the list of external inputs of the implementation theorem; missing integration limits; unmarked internal bibliography entries; $\kappa_c$ parenthesisation.
* **No proof-breaking issue.** No forbidden formula or retracted claim survives in the draft.
