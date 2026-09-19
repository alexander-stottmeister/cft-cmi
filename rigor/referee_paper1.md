# Referee report PP1 — paper1/main.tex ("Exact recovery error of the vacuum in chiral CFT: the free fermion")

Referee: PP1 (adversarial pass, 2026-09-09). Sources of truth: rigor/quadratic_limit.tex,
rigor/uhlmann_upper_bound.tex (Sec. 8-11), rigor/rate_of_remainder.tex (Sec. 6.2-6.4),
rigor/tail_bound.tex, rigor/certified_numerics.tex (Sec. 9), rigor/kernel_identity.tex,
rigor/findings.pdf, rigor/errata_log.md, numerics/README.md, fidelity_tables.tex,
fidelity_table_largezeta.tex, numerics/lattice/README.md, numerics/p1_bogoliubov.out.

Sections: 1 statement-by-statement verdicts; 2 numbers; 3 forbidden content;
4 internal consistency; 5 edits applied; 6 edits proposed.

(report body appended below as the pass proceeds)

## 1. Statement-by-statement verdicts

Legend: OK = statement, hypotheses, constants and normalisation agree with the source's final
(post-referee) form; LOCATOR = statement correct, citation locator wrong; WEAK = paper is weaker
than the source (acceptable); STRONG = paper claims more than the source (must be fixed).

| # | paper | source (final form) | verdict |
|---|---|---|---|
| 1 | Thm 2.1 `thm:LX` (Longo--Xu CMI $=\frac r6\log\frac{(a+b)(b+c)}{b(a+b+c)}=\frac r6\log(1+z)$) | Note 1; LX Thm 4.1(5),(6), Thm 4.2; scope restricted to $\mathcal A_r$/finite index + strong additivity, Rem. 4.3 conjecture explicitly *not* used | OK (scope remark `rem:LX-scope` is correctly conservative) |
| 2 | Thm 3.2 `thm:tracenorm`, $\lVert R_s\rVert_1=\frac12\log(1+\frac{as}{a+L})$, $\lVert Q_I-\widetilde Q_s\rVert_1=\frac r{2\pi}\log(1+\zeta)$ | Note 4 **Theorem 6.2** "Exact endpoint trace norm" (paper cites Thm 6.4) | LOCATOR (content OK, incl. the factor $1/2\pi$, multiplicity 2, $r$ copies) |
| 3 | Def 3.3 `def:zeta` $\zeta=as/(a+L)$, $\zeta_{\rm Petz}=2z$, $\zeta_t=z(1+e^{-2\pi t})$ | Note 4 §8, Note 5 Cor. 5.1 | OK |
| 4 | Thm 3.4 `thm:normal` (normal $*$-iso $\overline\beta_s$ onto $\mathcal F_r(J_s)\subset\mathcal F_r(AB)$, $s\ge\lambda$) | Note 4 **Theorem 7.1** | OK (locator correct) |
| 5 | Lemma 3.6 `lem:tensorization` | Note 4 **Lemma 3.1** (paper cites Lemma 4.1) | LOCATOR |
| 6 | Lemma 3.7 `lem:fidbelow` (continuity from below of $F$) | Note 4 **Lemma 10.1** | OK |
| 7 | Lemma 4.1 `lem:mobius` (Möbius reduction, $1+\zeta$ = cross ratio) | Note 5 **Lemma 1.1** (paper cites Lemma 2.1) | LOCATOR |
| 8 | Thm 4.2 `thm:fidfd` (quasi-free root fidelity, $\det[(1-Q_1)(1-Q_2)]^{1/2}\det[1+(G_1^{1/2}G_2G_1^{1/2})^{1/2}]$) | Note 5 **Theorem 2.1** (paper cites Thm 3.2) | LOCATOR. Note the *correct* determinant form is used; the refuted $\Delta^{1/2}$ formula does not appear anywhere |
| 9 | Prop 4.3 `prop:relentfd` | Note 5 **Prop 2.2** (paper: 3.3) | LOCATOR |
| 10 | Prop 4.4 `prop:secondorder` ($\frac{\eps^2}4\sum|D_{ik}|^2/N$, $\frac{\eps^2}2\sum|D_{ik}|^2[\ell+\ell]$) | Note 5 **Prop 2.3** (paper: 3.4) | LOCATOR; the factors $\frac14,\frac12$ and the weight $1/N=1+\cosh\frac{\kappa+\kappa'}2/\cosh\frac{\kappa-\kappa'}2$ agree |
| 11 | Thm 4.5 `thm:detrep` (determinant representation; monotone sequences) | Note 5 **Theorem 3.1** (paper: 4.1); martingale locator Araki 1977 Thm 3.9(2)+3.8(2)($\gamma$) | LOCATOR only. Martingale locator is the corrected one — "Ohya--Petz Cor. 5.12" is absent |
| 12 | Prop 4.7 `prop:tail` (UV tail $\frac2{15}\zeta^2\kappa^{-3}$) | Note 5 **Prop 4.1** (paper: 5.2) | LOCATOR; status remark `rem:tail-status` correctly marks it a sketch and states it is *not used* in Sec. 5 |
| 13 | `rem:tail-status` constants: $\lvert\Sigma-\zeta^2/(15\kappa_c^2)\rvert\le0.46\zeta^2\kappa_c^{-3}+0.051\zeta(1+\kappa_c)e^{-\kappa_c}$; $0\le\Phi-\Phi_W\le0.173\zeta^2/\kappa_c+0.88\zeta^2/\kappa_c^2$ for $\kappa_c\ge\max\{10,2\log\frac1\zeta+2\log(1+\kappa_c)+3\}$ | `tail_bound.tex` Thm (main) l. 504--514 and summary l. 804--814: identical constants and identical hypothesis | OK (exact match) |
| 14 | Cor 4.9 `cor:collapse` ($\zeta_t=z(1+e^{-2\pi t})$, best member $t\to+\infty$, factor 4) | Note 5 **Cor 5.1** (paper: 6.1) | LOCATOR |
| 15 | Prop 4.10 `prop:monotone` ($\Phi$ nondecreasing) | `check_note5_theory.tex` | OK (cited as a verification document, not as a theorem of this paper) |
| 16 | Def 5.1 `def:gB` ($g_B=\sup\Omega(\ell)=2r\iint|D^{(1)}|^2/N$) | `quadratic_limit.tex` **Def. 4.1** + **Prop. 5.1**; $D^{(1)}:=\partial_\zeta\delta_\zeta\rvert_{\zeta=0}$ (**Def. 2.3**) | **NORMALISATION ERROR** in the paper: it defines $D^{(1)}=\partial_s\delta_s\rvert_{s=0}$ and normalises by $s$, while $g_B/8=\lim\Phi/\zeta^2$ requires the $\zeta$-derivative ($\zeta=as/(a+L)$, e.g. $\zeta=s/3$ in the numerics). Fixed, see §5 |
| 17 | Thm 5.2 `thm:main` ($\lim\Phi/\zeta^2=g_B/8=r/(12\pi^2)=0.00844343r$; $\Phi\le\tau/(1-\tau)$ for $\tau<1$) | `quadratic_limit.tex` Thm 4.2 + Thm 6.3; `uhlmann_upper_bound.tex` Thm 8.1/8.2 | OK, incl. the constant to 9 digits |
| 18 | Lemma 5.3 `lem:legendre` | `quadratic_limit.tex` **Lemma 3.1** (paper: Lemma 3.2) | LOCATOR |
| 19 | Prop 5.4 `prop:oneparticle` | `quadratic_limit.tex` **Prop. 3.3** | OK |
| 20 | Thm 5.5 `thm:lower` | `quadratic_limit.tex` **Thm 4.2** | OK |
| 21 | Prop 5.6 `prop:gBvalue` ($g_B=2r/(3\pi^2)$, $g_{\rm KM}=r/6$, $f_2=g_B/8=r/12\pi^2$, $s_2=g_{\rm KM}/2=r/12$) | `quadratic_limit.tex` Prop. 5.1; Note 7 Thm A | OK; the $u$- and $v$-integrals and $\int_0^\infty\frac{\tanh\pi k}{k(k^2+1)}dk=2$ agree with Lemmas 5.2/5.3 |
| 22 | Lemma 5.7 `lem:vector` | `uhlmann_upper_bound.tex` **Prop. 3.1** | OK |
| 23 | Thm 5.8 `thm:det` (vacuum overlap $=\det(1-V^*V)^{1/2}$) | `uhlmann_upper_bound.tex` **Thm 4.1**, cf. Dereziński Thm 31(3) | OK |
| 24 | Thm 5.9 `thm:upper` ($\limsup\le g_B/8$) | `uhlmann_upper_bound.tex` **Thm 8.1** ("Sharp upper bound"; 8.2 = "Theorem A closed") | OK; but the proof sketch says the referee repairs are in "§10" — they are in **§11** (§10 is (H2)/(H3)). Fixed |
| 25 | `rem:hellinger` ($h_2=\frac{r\log2}{6\pi^2}=2\log2\,f_2$, bracket $[1,1.3863]f_2$) | `quadratic_limit.tex` Prop. 6.5 ($h_2=r\log2/(6\pi^2)$, $h_2/(g_B/8)=2\log2$) | OK |
| 26 | `rem:norate` (global bound $\Phi\le-\frac12\log(1-2f_2\zeta^2)$, no cubic term; $c_3=-0.99(1)$ numerical) | `rate_of_remainder.tex` Thm (global) + RRr Prop. 3.1 (hypothesis removed) + §6.2--6.4 | OK (this is the post-referee form) |
| 27 | `rem:s2-status` ($s_2=r/12$ as a Kubo--Mori *quadratic-form* statement; identification numerical) | Note 7 §; `lemma_second_variation.tex` (KM half open beyond finite dim.); RK (gauge lemma refuted 2026-09-09) | OK — correctly weaker than Note 7's Theorem A blurb, which still claims the $s_2$ identification. The KM weight remark ($4(\lambda-1)/\log\lambda$ not bounded by $1+\lambda$) is verbatim the source's |
| 28 | Prop 6.1 `prop:twobranch` (two-chirality law; $2+4\cosh\pi\lambda+2\cosh2\pi\lambda$; $-\log F^{(0)}=\frac{c+\bar c}{3\pi^2}\eta_{\rm V}^2$; $D=\frac{c+\bar c}3\eta_{\rm V}^2$) | Note 5 Cor. 5.1 + VWZ translation paragraph | OK; algebra re-checked ($(1+e^{-\pi\lambda})^2+(1+e^{\pi\lambda})^2$, bracket $=8$ at $\lambda=0$, $8f_2=2c/3\pi^2$) |
| 29 | Appendix A.1/A.2/A.3/A.4 | Note 5 Prop 2.3; Note 4 §6; Note 5 §4; `kernel_identity.tex` | OK; A.3 repeats the "sketch" status and A.4 states the analytic-continuation caveat |

## 2. Numbers

Verified against `numerics/results_A2.txt` (A), `results_L120_2.txt` (B), `results_hp2.txt` (C),
`results_final2.txt`, `results_first_window.txt`, `results_largezeta*.txt`,
`numerics/p1_bogoliubov.out`, `numerics/lattice/petz_lattice.out`, `numerics/README.md`,
`fidelity_tables.tex`, `numerics/fidelity_table_largezeta.tex`.

**Correct (spot-checked digit by digit).**
* `tab:convergence` (9 rows): all $\Phi_{\rm sub}$ and $\Phi_{\rm sub}+$tail values reproduce
  `results_final2.txt` to the last printed digit (e.g. 60/30: 3.431959e-5 / 3.519279e-5;
  240/60: 3.429988e-5 / 3.517308e-5). Spread $\pm0.058\%$ → the quoted $\pm0.06\%$ and
  $\Phi(1/15)=3.517(3)\times10^{-5}$ are right. Caption tail $\zeta^2/(15\kappa_c^2)=8.73\times10^{-7}$
  checks with $\kappa_c=\log10^{8}=18.42$.
* `tab:second-order`: all 27 entries reproduce `results_first_window.txt` exactly; the $10^{-16}$ rows
  are correctly omitted ("double-precision floor", as in `numerics/README.md`).
* `tab:scan`: columns A/B/C reproduce the three result files exactly; $\Phi/\zeta^2$(C) and the
  last column ($-2\log F/I$) agree. $S_\infty$ is the $1/\kappa_c$ extrapolation of the **raw**
  $S_{\rm sub}$ (not the tail-corrected value) — I reproduced 5.6944e-6 at $\zeta=0.0083$ from
  4.632232e-6/4.921910e-6, so the column is right and the caption's description is right.
* `f_2^{\rm num}=0.008444(1)`, `s_2^{\rm num}=0.0837(5)`, `12\pi^2f_2=1.0001(1)`, `12s_2=1.004(6)`:
  all consistent with the last table row.
* Bogoliubov table in §7.4: the six rows are `p1_bogoliubov.out` §(3) verbatim
  ($E$, $\frac12E/\zeta^2$, $\Phi$, $\frac12E/\Phi=1.00216\ldots1.28470$). The optimisation numbers
  $4.5Q_{\min}=0.0084653,\dots,0.0084494$ at $M=30,\dots,200$, Richardson $4.5Q_\infty=0.0084465$,
  agreement $0.04\%$, cubic-Hermite $0.011174$ ($32\%$ weaker), restricted class $0.0678$ (factor
  $8.0$): all verbatim from §(4) of the same file.
* Lattice: exponents $1.986,1.912,1.635,1.151$ (window $\eta_{\rm V}\le0.1$) and
  $2.051,1.715,1.125,0.678$ (window $0.05$--$0.5$) are columns 1 and 3 of `[3]` in
  `petz_lattice.out`; the VWZ comparison values $2.0,1.9,1.7,1.2$ are its "VWZ fit" column.
  Finite-size drift $4.872,4.599,4.530,4.476,4.451,4.438,4.429$ ($\times10^{-3}$) at
  $n=12,\dots,72$ matches `[5]`. $\Phi_{\rm lat}(1.986)=1.004\times10^{-2}$,
  $\Phi_{\rm lat}(11.52)=5.61\times10^{-2}$ match `[1]`. Validation ($n=8,9,10$;
  $\lambda=0,0.5,1,1.5$; $K\det(1+\widetilde T)=1$), precision recipe
  ($3\kappa_{\max}/\log2+250$ bits, $\kappa_{\max}\approx1.8n$, $n\le72$) match `lattice/README.md`.
* Certified statements in §7.2: $Q_N$ enclosed to $5.6\times10^{-18}$ per entry
  (`certified_numerics.tex` §5, $5.62\times10^{-18}$ at $(60,30)$); a priori
  $\Phi_W\le\Phi^{\rm box}\le1.20\,\Phi_W$ (§RCr, widths 17.8--19.9 %); weighted Sylvester identity
  with the explicit warning that the unweighted quadratic square-root bound is **false**
  (`certified_numerics.tex`, Prop. "the unweighted bound is false", §2); enclosure widths $0.71\%$ at $\zeta=1/120$ to $1.01\%$ at
  $\zeta=8/15$; "not certified: the two-dimensional quadrature of $\widehat D$ and the box cutoff".
  All four match the source, including the honest scope.
* Tail-bound constants $0.173$, $0.88$, $0.46$, $0.051$ and the hypothesis
  $\kappa_c\ge\max\{10,2\log\frac1\zeta+2\log(1+\kappa_c)+3\}$: exact match with `tail_bound.tex`.
* §7.3 large-$\zeta$ text (brackets $0.45\%$ / $1.8\%$ / $6.6\%$, local slope $1.29\to0.69$,
  lattice slopes $1.41,1.18,0.98,0.87,0.68$, lattice/continuum ratio $1.01\to1.28$, $p$ drifting
  $2.5\to1.2$, $\kappa_c$ up to $43.8$): matches `fidelity_table_largezeta.tex` and
  `numerics/README.md` (PZ section).
* Intro ratio range $1.7\times10^{-3}$ at $\zeta=0.008$ to $7.8\times10^{-2}$ at $\zeta=0.53$: matches
  `tab:scan`. $-\log F^{(0)}=\frac{c+\bar c}{3\pi^2}\eta_{\rm V}^2$: re-derived, correct.
  Lattice amplitude check `[7]` of `petz_lattice.out` ($0.07220$ vs $8f_2=0.06755$) supports it.

**Wrong or stale numbers (all listed again in §5/§6).**
1. **`sec_numerics.tex` l. 87**: `$s_2^{\rm num}/f_2^{\rm num}=9.877(60)$`. From the paper's own
   $0.0837(5)/0.008444(1)$ the ratio is $9.912(60)$, not $9.877$ (9.877 corresponds to $s_2=0.0834$).
   Against $\pi^2=9.8696$ the deviation is $0.4\%$, not $0.08\%$. **Fixed.**
2. **`sec_2d_lattice.tex` `rem:largezeta`**: the brackets $\Phi(2.13)\in[1.06,1.10]\times10^{-2}$
   ($4\%$), $\Phi(8.53)\in[3.7,4.05]\times10^{-2}$ ($10\%$) and the "extrapolated local log-slope
   $\approx0.93$" are the **superseded** pre-certification numbers of `numerics/README.md`
   (2026-09-08, results_largezeta2). The paper's own `tab:largezeta` gives $1.0797(50)$ and
   $3.974(72)$ ($\times10^{-2}$), i.e. $0.5\%$ and $1.8\%$, and local slopes $1.29\to0.69$;
   §7.3 quotes the new numbers. Direct contradiction inside the paper. **Fixed.**
3. **`sec_2d_lattice.tex` (L2)**: "$0.961$ at $L=4$" — `[8]` of `petz_lattice.out` gives $0.96186$,
   i.e. $0.962$. **Fixed.**
4. **abstract**: "over four decades of cross ratio" — the tabulated range is
   $\zeta=0.0083\ldots17.07$, i.e. $3.3$ decades. **Fixed** ("three decades").
5. **`sec_2d_lattice.tex` (L2)**: "off by factors between $22$ and $5000$" — over the in-range points
   of `[2]`/`[6]` the single-branch ratio runs from $\approx4$ ($\lambda=0.5$, $\eta_{\rm V}=0.79$)
   to $7573.7$ ($\lambda=1.5$, $\eta_{\rm V}=0.00444$); at $\lambda=0$ it is exactly 2. Proposed
   only (the intended data subset is ambiguous), see §6.
6. **`sec_numerics.tex` l. 57**: the box law is quoted as $g_B-g_B^{(\Lambda)}=0.513r/\Lambda^2$ but
   then used as $0.0641\zeta^2/\kappa_{\max}^2$. In `quadratic_limit.tex` Prop. 7.1 the cutoff
   $\Lambda$ **is** the modular-energy cutoff (the paper's $\kappa_{\max}$), not the box length in
   $\xi$ (the paper's $\Lambda$). As printed the sentence is self-contradictory. **Fixed** (notation).
7. `fidelity_tables.tex` caption of `tab:second-order`: "$0.0833$ from $25.3,32.2$" — the two-point
   $1/\kappa_c$ extrapolation gives $0.08337$, i.e. $0.0834$. Cosmetic; proposed only.

## 3. Forbidden content

| item | status in `paper1/` |
|---|---|
| old apparent exponents $2.04/2.04/1.96/1.31$ | **absent**. `sec_2d_lattice.tex` quotes the lattice values $1.986/1.912/1.635/1.151$ and, as the comparison, VWZ's own $2.0/1.9/1.7/1.2$ — i.e. the "VWZ fit" column of `petz_lattice.out`, not the withdrawn "Note 5" column |
| single-branch 2D law | **absent as a claim**; it appears only in (L2) and in the remark after Prop. 6.1 as the law that *fails* ("a single-branch fit is badly wrong") |
| $\Delta^{1/2}$ fidelity formula | **absent**; Thm 4.2 uses the corrected $\det[(1-Q_1)(1-Q_2)]^{1/2}\det[1+(G_1^{1/2}G_2G_1^{1/2})^{1/2}]$ and the equivalent $\det(S_1S_2+C_1UC_2)/\det U$ |
| $\log^{-2}$ remainder as a claim | **PRESENT, forbidden occurrence** in `sec_outlook.tex` (O1): "The heuristic (5.x) predicts $\Theta(\zeta^2\log^{-2}(1/\zeta))$ … a genuine $O(\zeta^3)$ remainder is *excluded* … the fourth-order Bures derivative is infinite." This is exactly the claim refuted by `rate_of_remainder.tex` (Cor. "Sign of the cubic coefficient") and already retracted in `sec_fidelity.tex`. The 2026-09-09 errata patched `sec_fidelity.tex` and `sec_quadratic.tex` but **not** `sec_outlook.tex`. **Fixed** (§5) |
| "ten times $\Phi$" | **absent**; the text says "the relative entropy stays close to $\pi^2$ times $\Phi$" (checked: $S_\infty/\Phi=9.79$ at $\zeta=0.0083$ vs $\pi^2=9.8696$) |
| tail correction claimed certified | **absent**; §7.2 says "*This correction is heuristic*", lists the raw values as the only rigorous lower bounds, and the certified bullet explicitly excludes the $\widehat D$ quadrature and the box cutoff |
| "Ohya--Petz Cor. 5.12" as the martingale locator | **absent**; `sec_fidelity.tex` cites Araki 1977, Thm. 3.9(2) with Thm. 3.8(2)($\gamma$), the corrected locator |

## 4. Internal consistency

1. **Hardy-projection convention.** Stated once in §2.1 ($\widehat f(k)=\int fe^{-ikx}$, $P_+=\mathbf 1_{\{k<0\}}$,
   kernel (2.1)) and repeated in App. B with the explicit warning that `uhlmann_upper_bound.tex` and
   `p1_bogoliubov.py` use the opposite labelling after $x\to-x$. Consistent; no third convention appears.
2. **$c$ = interval length vs $c_{\rm cft}$.** Handled by App. B and the sentence in §2.2. But §6 (Prop. 6.1)
   silently switches $c,\bar c$ to central charges *and* uses $L_A,L_B,L_C$; App. B says exactly this. OK.
3. **$s$ vs $\zeta$ normalisation (serious).** §5 opens with $D^{(1)}=\partial_s\delta_s|_{s=0}$ and
   Def. 5.1 normalises "$-\log F=\frac{s^2}8g_B$", while Thm. 5.2 asserts $\lim\Phi/\zeta^2=g_B/8$ and
   App. B says "the parameter being $\zeta$". Since $\zeta=as/(a+L)$ (e.g. $s/3$ in all numerics), the
   two cannot both hold; the source (`quadratic_limit.tex` Def. 2.3) defines
   $D^{(1)}=\partial_\zeta\delta_\zeta|_{\zeta=0}$. Fixed in three places.
4. **Large-$\zeta$ numbers.** `rem:largezeta` (§6) contradicted §7.3 and `tab:largezeta` (item 2 of §2);
   (O6) in §8 repeated the stale "$4$--$10\%$ … log-slope $\approx0.93$". Both fixed.
5. **(O1) vs `sec_fidelity`/`rem:norate`.** Direct contradiction (§3 above): §4.4 says the expansion is
   in integer powers with $c_3=-0.99(1)$ and that the $\log^{-2}$ term is excluded by the global bound,
   while (O1) predicted it. Fixed.
6. **Abstract vs theorems.** (i) "The corresponding relative-entropy coefficient is $c/12$" is stated
   flatly; Prop. 5.6 + Rem. 5.12 prove it only as a statement about the Kubo--Mori *quadratic form*, the
   identification with $\lim\mathcal D/\zeta^2$ being numerical. The introduction and `tab:summary` are
   careful; the abstract is not. Proposed wording in §6 (not applied: authorial).
   (ii) "four decades of cross ratio" — fixed to three.
   (iii) Everything else in the abstract (Borchers semigroup, zero-collar $*$-isomorphism from the exact
   trace-norm identity + Powers--Størmer--Araki, no global diffeomorphism, single cross ratio, two-branch
   law, 72 sites, $10^{-4}$) is supported by Thms 3.2/3.4, 5.2, Prop. 6.1 and §7.
7. **Cross-references.** All `\cref` targets resolve (compilation gives no undefined references; see §5).
   `\cref{rem:largezeta}` in `tab:summary` and (O6), `\cref{rem:s2-status}`, `\cref{app:secondorder}`,
   `\cref{tab:largezeta}` all exist. `\cref{sec:box}` is defined twice-over (label `sec:box` in
   `sec_fidelity.tex` §4.4 and a subsection of the same name in §7.1) — only one carries the label, no clash.
8. **Duplicated statements.** Rem. 4.11 (`rem:twirled`) repeats verbatim the last two sentences of Note 5
   Cor. 5.1 and partially duplicates the discussion after (3.19); harmless. The $p(t)$ density is defined
   twice ((3.20) and Rem. 4.11) with the same normalisation. The Hankel/Frullani computation appears both
   as a proof sketch in §3.1 and in App. A.2 — deliberate, and the two agree.
9. **Bibliography.** `Note1, Note2, Note4, Note5, Note7, RigorQL, RigorUB, RigorKI, RigorCN5, RigorCN5N,
   RigorSV` are placeholder items that give only a file name; only `RigorTB`, `RigorRR`, `RigorCN` are
   flagged "Internal rigor document". `Note3` and `Note6` are cited nowhere and are absent (consistent).
   `\bibliographystyle{plain}` is inert next to a manual `thebibliography`. Recommendation in §6.
10. **Unused/mismatched citations.** `[Bhatia]` is used once (X.1.1) and correctly; `[Petz88]`, `[FR]`,
    `[Uhl11]`, `[PS70]`, `[ArakiCAR]`, `[BGL]`, `[Wiesbrock]`, `[Ruij77]`, `[CH]`, `[Derez]`, `[AU02]`,
    `[Araki77]` all appear with locators. No citation is dangling.

## 5. Edits applied (23 edits, all in `paper1/`; `pdflatex` twice, 0 errors, 0 undefined
references/citations, 27 pages)

Line numbers are those of the edited files.

| # | file:line | old | new | why |
|---|---|---|---|---|
| 1 | `main.tex`:50 | `over four\ndecades of cross ratio` | `over three decades` | tabulated range $\zeta=0.0083\ldots17.07$ = 3.3 decades |
| 2 | `sec_petz.tex`:81 | `\cite[Thm.~6.4]{Note4}` | `\cite[Thm.~6.2]{Note4}` | Note 4's "Exact endpoint trace norm" is Thm 6.2 |
| 3 | `sec_petz.tex`:156 | `\cite[Lemma~4.1]{Note4}` | `\cite[Lemma~3.1]{Note4}` | Note 4's "Tensorization" is Lemma 3.1 |
| 4 | `sec_fidelity.tex`:22 | `\cite[Lemma~2.1]{Note5}` | `\cite[Lemma~1.1]{Note5}` | Note 5 numbering |
| 5 | `sec_fidelity.tex`:58 | `\cite[Thm.~3.2]{Note5}` | `\cite[Thm.~2.1]{Note5}` | " |
| 6 | `sec_fidelity.tex`:80 | `\cite[Prop.~3.3]{Note5}` | `\cite[Prop.~2.2]{Note5}` | " |
| 7 | `sec_fidelity.tex`:85 | `\cite[Prop.~3.4]{Note5}` | `\cite[Prop.~2.3]{Note5}` | " |
| 8 | `sec_fidelity.tex`:119 | `\cite[Thm.~4.1]{Note5}` | `\cite[Thm.~3.1]{Note5}` | " |
| 9 | `sec_fidelity.tex`:207 | `\cite[Prop.~5.2]{Note5}` | `\cite[Prop.~4.1]{Note5}` | " |
| 10 | `sec_fidelity.tex`:248 | `\cite[Cor.~6.1]{Note5}` | `\cite[Cor.~5.1]{Note5}` | " |
| 11 | `sec_quadratic.tex`:5 | `$D^{(1)}=\partial_s\delta_s|_{s=0}$` | `$D^{(1)}=\partial_\zeta\delta_\zeta|_{\zeta=0}$` | `quadratic_limit.tex` Def. 2.3; the $s$-derivative would rescale $g_B$ by $((a+L)/a)^2$ and contradict Thm 5.2 |
| 12 | `sec_quadratic.tex`:18 | `$-\log\Fid=\frac{s^2}8g_B+o(s^2)$` | `$\frac{\zeta^2}8g_B+o(\zeta^2)$` | same normalisation; App. B already says "the parameter being $\zeta$" |
| 13 | `sec_quadratic.tex`:20 | `$D(\omega\Vert\omega_s)=\frac{s^2}2g_{\rm KM}+o(s^2)$` | `$D(\omega\Vert\widetilde\omega_s)=\frac{\zeta^2}2g_{\rm KM}+o(\zeta^2)$` | same; also $\omega_s$ was undefined ($\widetilde\omega_s$ is meant) |
| 14 | `sec_quadratic.tex`:46 | `\cite[Lemma~3.2]{RigorQL}` | `\cite[Lemma~3.1]{RigorQL}` | "Legendre form of the SLD information" is Lemma 3.1 |
| 15 | `sec_quadratic.tex`:211 | `the repairs are listed in its \S10` | `\S11` | §10 is (H2)/(H3); the referee repairs are §11 |
| 16 | `app_conventions.tex`:79 | `$-\log\Fid=\frac{s^2}8g_B$ and $D=\frac{s^2}2g_{\rm KM}$` | $\zeta$ in place of $s$ | same normalisation fix |
| 17 | `sec_numerics.tex`:57 | `$g_B-g_B^{(\Lambda)}=0.513\,r/\Lambda^2$` | `$g_B-g_B^{(\kappa_{\max})}=0.513\,r/\kappa_{\max}^2$` | in `quadratic_limit.tex` Prop. 7.1 the cutoff is the modular-energy cutoff, i.e. the paper's $\kappa_{\max}$, not the box length $\Lambda$; as printed the sentence contradicted its own conclusion $0.0641\zeta^2/\kappa_{\max}^2$ |
| 18 | `sec_numerics.tex`:87 | `$s_2^{\rm num}/f_2^{\rm num}=9.877(60)$` | `$9.912(60)$` | $0.0837(5)/0.008444(1)=9.912(59)$ |
| 19 | `sec_numerics.tex`:156--157 | `The large-$\zeta$ brackets of \cref{rem:largezeta} come from results_largezeta.txt and results_largezeta2.txt` | `The large-$\zeta$ values of \cref{tab:largezeta} come from run_largezeta_cert.py and results_largezeta_certified.txt (results_largezeta{,2}.txt for the $\Phi_{\rm sub}$ lower bounds of \cref{rem:largezeta})` | the table is produced by the certified pipeline (PZ, 2026-09-08) |
| 20 | `sec_2d_lattice.tex`:113 | `($0.961$ at $L=4$)` | `($0.962$ at $L=4$)` | `petz_lattice.out` `[8]`: 0.96186 |
| 21 | `sec_2d_lattice.tex`:129--134 | `two-point extrapolations … give the brackets $\Phi(2.13)\in[1.06,1.10]\times10^{-2}$ ($4\%$) and $\Phi(8.53)\in[3.7,4.05]\times10^{-2}$ ($10\%$), with an extrapolated local log-slope $\approx0.93$ … i.e. inside the continuum brackets.` | `the certified extrapolations of \cref{tab:largezeta} give $\Phi(2.13)=1.0797(50)\times10^{-2}$ ($0.5\%$) and $\Phi(8.53)=3.974(72)\times10^{-2}$ ($1.8\%$), with a local log-slope falling from $1.29$ at $\zeta\approx1$ to $0.69$ at $\zeta\approx17$ … i.e. above the continuum best estimates by $1\%$ and $14\%$ respectively, the finite-size drift of (L3).` | the old brackets and slope are the superseded pre-certification numbers and contradicted §7.3 and `tab:largezeta`; with the tighter brackets the lattice values are no longer "inside" them (ratios 1.01 and 1.14, cf. the $\Phi_{\rm lat}$ column) |
| 22 | `sec_outlook.tex`:54--59 (O1) | `The heuristic … predicts $\Theta(\zeta^2\log^{-2}(1/\zeta))$ … Note that a genuine $O(\zeta^3)$ remainder is excluded by the same heuristic: the fourth-order Bures derivative is infinite.` | `The expansion … proceeds in integer powers, so what is missing is a two-sided $O(\zeta^3)$ remainder. The upper half is available: the global bound of \cref{rem:norate} gives $\Phi-f_2\zeta^2\le f_2^2\zeta^4/(1-2f_2\zeta^2)$, whence $c_3\le0$ once the limit defining $c_3$ exists \cite{RigorRR}. A matching lower bound needs a cubic remainder uniform in the modular cutoff. (The formal fourth-order Taylor coefficient of the quadratic quantum-Fisher functional diverges, but that is not the expansion of $\Phi$, whose quartic coefficient is finite, $c_4f_2\approx+0.0076$.)` | **forbidden content**: the $\log^{-2}$ rate is refuted (`rate_of_remainder.tex`, Cor. "Sign of the cubic coefficient"; errata 2026-09-09) and was already retracted in `sec_fidelity.tex`; the "$O(\zeta^3)$ excluded" claim is the opposite of what RR proves. Wording follows RR §7.4 |
| 23 | `sec_outlook.tex`:81--83 (O6) | `brackets of $4$--$10\%$ and an extrapolated local log-slope $\approx0.93$` | `brackets of $0.45$--$6.6\%$ (\cref{tab:largezeta}) and a local log-slope falling from $1.29$ to $0.69$` | same stale numbers as #21 |

## 6. Edits proposed but not applied

Ordered by importance. Line numbers refer to the files *after* the edits of §5.

1. **Abstract, `main.tex`:42--43 (statement stronger than its source).**
   old: `The corresponding relative-entropy coefficient is $c/12$.`
   new: `The corresponding relative-entropy coefficient is $c/12$ as a statement about the
   Kubo--Mori quadratic form; its identification with the relative entropy itself is so far only
   numerical.`
   Reason: Prop. 5.6 proves $g_{\rm KM}=r/6$; Rem. 5.12 states explicitly that
   $\lim\mathcal D/\zeta^2=s_2$ has no analogue of Thm 5.9 (the Kubo--Mori half of the
   second-variation lemma is open beyond finite dimensions, and the gauge lemma was refuted on
   2026-09-09, `errata_log.md`, RK). The introduction and `tab:summary` are correctly hedged; the
   abstract is not. Not applied because the wording is authorial.
2. **`sec_2d_lattice.tex`:114 (L2).** old: `off by factors between $22$ and $5000$`.
   Over the in-range points of `petz_lattice.out` `[2]`/`[6]` the single-branch/lattice ratio runs
   from $\approx4$ ($\lambda=0.5$, $\eta_{\rm V}=0.79$, $L=24$) to $7573.7$ ($\lambda=1.5$,
   $\eta_{\rm V}=0.00444$), and is exactly $2$ at $\lambda=0$. Suggested:
   `off by factors between $4$ and $7.6\times10^3$, growing with $\lambda$ and with $1/\eta_{\rm V}$`.
   Not applied: the intended data subset ($\lambda\ge0.5$? small $\eta_{\rm V}$ only?) is ambiguous.
3. **`sec_2d_lattice.tex`:128--130 (`rem:largezeta`).** The quoted rigorous lower bounds
   $\Phi_{\rm sub}=4.230\times10^{-3},\ldots,4.779\times10^{-2}$ are the $\Lambda=60$,
   $\kappa_c=18.4$ values of `results_largezeta.txt`; the paper's own `tab:largezeta` contains
   strictly better certified lower bounds ($\kappa_c=39.1$/$43.8$: $4.381\times10^{-3}$, $1.0672
   \times10^{-2}$, $2.1872\times10^{-2}$, $3.8259\times10^{-2}$, $5.7395\times10^{-2}$).
   Suggested: quote the last columns of `tab:largezeta`, or add "($\kappa_c=18.4$; the best
   certified lower bounds are the last columns of \cref{tab:largezeta})".
4. **`sec_quadratic.tex`:11--12 (`def:gB`).** `where $\Omega(\ell)$ is the Legendre functional of
   \cref{lem:legendre}` → `of \cref{prop:oneparticle}`: $\Omega(\ell)$ is defined in
   \eqref{eq:Omega-ell} (Prop. 5.4), not in Lemma 5.3, and this matches
   `quadratic_limit.tex` Def. 4.1.
5. **`sec_quadratic.tex`:194--195.** `the flow of $-x^2\,d/dx$ on $D$ in the $q$-coordinate` →
   `$-(x^2/L)\,d/dx$`, as in App. B ("generator $-x^2/L\cdot\partial_x$"), in `uhlmann_upper_bound.tex`
   and in `p1_bogoliubov.out` §(4). The parenthesis that follows already gives $-x^2/L$.
6. **Bibliography, `main.tex`:96--106.** `Note1, Note2, Note4, Note5, Note7, RigorQL, RigorUB,
   RigorKI, RigorCN5, RigorCN5N, RigorSV` are placeholders that give only a `.tex` file name.
   Suggested: mark each the way `RigorTB`/`RigorRR`/`RigorCN` are, e.g. append
   `(unpublished internal note; to be replaced by the published version)`; a referee cannot check
   any of the theorem locators otherwise. Also delete the inert `\bibliographystyle{plain}`
   (`main.tex`:83) next to the manual `thebibliography`.
7. **Numeric locators for the two "named" citations.**
   `sec_quadratic.tex`:223 `\cite[Thm.~``Upper bound'']{RigorQL}` → `\cite[Thm.~6.3]{RigorQL}`;
   `sec_quadratic.tex`:231 `\cite[Prop.~``Value of the Hellinger coefficient'']{RigorQL}` →
   `\cite[Prop.~6.5]{RigorQL}`.
8. **`sec_fidelity.tex`:220--224 (`rem:tail-status`).** The $\Sigma$-estimate constants $0.46$ and
   $0.051$ hold in `tail_bound.tex` under `$0<\zeta\le1$ and $\kappa_c\ge8$`; the paper states them
   without hypotheses (the full-tail bound's hypothesis *is* stated). Suggested: add
   "for $0<\zeta\le1$, $\kappa_c\ge8$".
9. **`sec_fidelity.tex`:207 (Prop. 4.7).** The header cites Note 5 only, while `rem:tail-status`
   says the Note 5 argument is a sketch and the complete proof is `RigorTB`. Suggested header:
   `{\cite[Prop.~4.1]{Note5}}, complete proof in {\cite{RigorTB}}`.
10. **`fidelity_tables.tex`:16 (caption of `tab:second-order`).** `0.0833 from 25.3,32.2` →
    `0.0834`: the two-point $1/\kappa_c$ extrapolation of $0.071785,0.074268$ gives $0.08337$.
    (The quoted mean $s_2^{\rm num}=0.0837(5)$ is unaffected.)
11. **`sec_intro.tex`:101 (`tab:summary`).** Row `$\Phi(\zeta)$, $\zeta\gtrsim1$` points at
    `\cref{rem:largezeta}` and says "lower bounds plus extrapolation only"; with the certified
    table it should point at `\cref{tab:largezeta}` and read "certified lower bounds plus
    extrapolation, $0.45$--$6.6\%$".
12. **Referee remark, no edit.** Prop. 4.10 (monotonicity of $\Phi$) is used in Cor. 4.9 and in the
    proof of Prop. 6.1, but its only proof is in the internal verification document `RigorCN5`.
    For publication either include the two-line semigroup argument or mark the corollary's
    monotonicity clause as relying on it.
13. **Referee remark, no edit.** §7.1's claim "16 nodes change the matrix by $3\times10^{-11}$
    relative" and "omitting [the exact $t\to0$ diagonal limit] produces an $O(h)$ error of $0.2\%$"
    are quadrature diagnostics that I could not locate verbatim in `certified_numerics.tex` §7
    (which certifies $Q_N$, not $\widehat D$); §7.2 already declares the $\widehat D$ quadrature
    uncertified, so the two numbers should be attributed to the run that produced them.

## 7. Overall verdict

After the 23 edits of §5 the draft is consistent with the rigor documents in their final,
post-referee form. No theorem, proposition or lemma of `paper1/` claims more than its source; the
only two overstatements found were (i) the $\log^{-2}$ rate in (O1), which was a live claim
refuted by `rate_of_remainder.tex` and is now removed, and (ii) the abstract's unqualified
"relative-entropy coefficient is $c/12$", left for the authors (§6.1). The two genuine technical
defects were the $s$- versus $\zeta$-normalisation of $D^{(1)}$/$g_B$ (which, taken literally,
falsifies Thm 5.2 for any configuration with $a\ne a+L$) and the stale large-$\zeta$ brackets,
which contradicted the paper's own §7.3 and `tab:largezeta`. Nine citation locators into Notes 4/5
and one into `quadratic_limit.tex` were off (Note 5's numbering shifted by one section at some
point); these are now correct against the compiled PDFs of the notes. Every number in the three
continuum tables, the large-$\zeta$ table, the Bogoliubov table and the lattice findings
reproduces its source file to the printed digits, with the six exceptions listed in §2.
Nothing corrected during the audit (old apparent exponents, single-branch 2D law, $\Delta^{1/2}$
fidelity formula, "ten times $\Phi$", Ohya--Petz martingale locator, certified tail correction)
has reappeared.
