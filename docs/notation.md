<!-- Assembled once by tools/build_docs.py from paper1/app_conventions.tex,
     paper2/app_conventions.tex and the conventions block of rigor/phase6_brief.md.
     Change the next line to `hand-edited: yes` after a human pass and the
     generator will leave this file alone. -->
<!-- hand-edited: no -->

# Symbols and conventions

Every constant quoted in this project depends on the choices collected here. This page is a first assembly from the conventions of the two papers and of the Phase 6 brief; it is meant to be read once by a human and corrected, after which the marker line at the top stops the generator from touching it again.

Assembled from [`paper1/app_conventions.tex`](../paper1/app_conventions.tex), [`paper2/app_conventions.tex`](../paper2/app_conventions.tex), [`rigor/phase6_brief.md`](../rigor/phase6_brief.md). Mathematics is reproduced as LaTeX; a renderer that supports it will typeset it, and the sources above are authoritative.

## From `paper1/app_conventions.tex`

### Fourier transform and the Hardy projection

$$

 \widehat f(k)=\int_{\mathbb R}f(x)e^{-ikx} dx,
 \qquad
 f(x)=\frac1{2\pi}\int_{\mathbb R}\widehat f(k)e^{ikx} dk .

$$

With this convention the positive-energy subspace for the light-ray coordinate
used here is $\{k<0\}$, so $P_+=\mathbf1_{\{k<0\}}$ and $P_-=1-P_+$; the
distributional kernel of $P_+$ is (eq:hardy).  (In
(RigorUB) and in the Bogoliubov numerics the opposite labelling
$P_+=\mathbf1_{\{k>0\}}$ is used for the same object after $x\to-x$; the
Hilbert--Schmidt norms and determinants quoted are unaffected.)

### Modular frame

For the interval $I=(-a,L)$,

$$

 \xi(x)=\log\frac{x+a}{L-x},
 \qquad
 \beta(x)=\frac{dx}{d\xi}=\frac{(x+a)(L-x)}{a+L},
 \qquad
 \beta_0=\beta(0)=\frac{aL}{a+L},

$$

and the modular modes are (eq:modes), normalized by
$\int_{\mathbb R}d\kappa |\psi_\kappa\rangle\langle\psi_\kappa|=1$ on $L^2(I)$,
with $Q\psi_\kappa=q_\kappa\psi_\kappa$, $q_\kappa=(1+e^\kappa)^{-1}$; thus
$\kappa$ is the one-particle modular Hamiltonian $K=\log\frac{1-Q}Q$, and
$\kappa\to+\infty$ labels the nearly empty modes.  Modular translation is
$\xi\mapsto\xi-2\pi t$, corresponding to the KMS asymmetry
$\widehat W(-k)=e^{2\pi k}\widehat W(k)$ of the thermal spectral density at
inverse temperature $2\pi$.  A symbol $X$ with bounded kernel on $I\times I$ has
modular kernel

$$

 X(\kappa,\kappa')
 =\frac1{(2\pi)^2}\iint d\xi d\xi'
 e^{-i\kappa\xi/2\pi} \widetilde X(\xi,\xi') e^{i\kappa'\xi'/2\pi},
 \qquad
 \widetilde X(\xi,\xi')=\sqrt{\beta(x)\beta(y)} X(x,y),

$$

and $\operatorname{Tr} X=\int d\kappa X(\kappa,\kappa)$ when $X$ is trace class.

### Cross-ratio variables

Four variables occur, all M\"obius invariants of the same configuration:

$$

 \eta=\frac{b(a+b+c)}{(a+b)(b+c)},\quad
 z=\frac1\eta-1=\frac{ac}{b(a+b+c)},\quad
 \eta_{\rm V}=1-\eta=\frac z{1+z},\quad
 \zeta=\frac{as}{a+L} .

$$

$\eta$ is the cross ratio of Note 1, in which the Longo--Xu conditional mutual
information is $-\frac r6\log\eta$; $\eta_{\rm V}$ is the cross ratio of
(VWZ), the complement of $\eta$; $\zeta$ is the recovery variable, with
$1+\zeta$ the cross ratio of $J_s$ inside $I$.  For the ordinary Petz map
$\zeta=2z$, for the rotated map $\zeta_t=z(1+e^{-2\pi t})$, and for the pure
geometric compression $\zeta=z$.

### Central charge versus interval length

The letter $c$ denotes the length of the third interval $C$ throughout
(sec:setting to sec:petz); where the central charge appears it is written
$c_{\rm cft}$, and $c_{\rm cft}=r$ for the net of $r$ complex chiral fermions.  In
(prop:twobranch) the pair $(c,\bar c)$ denotes the two central charges of a
two-dimensional CFT, the interval lengths being written $L_A,L_B,L_C$ there.

## From `paper2/app_conventions.tex`

### Fourier transform

$\hat f(p)=\int_{\mathbb R}f(x)e^{-ipx}dx$ on the line;
$\hat f_{n}=\frac{1}{2\pi}\int_{-\pi}^{\pi}f(\theta)e^{-in\theta}d\theta$ on the circle.  Sobolev norms:
$\|f\|_{\beta}=\sum_{n}|\hat f_{n}|(1+|n|^{\beta})$ (the Carpi--Weiner norm), and
$\|G\|_{3/2}^{2}=\int_{\mathbb R}|p|^{3}|\hat G(p)|^{2}\frac{dp}{2\pi}$ for the homogeneous
$\dot H^{3/2}$ (Weil--Petersson) norm on the line.

### Inner products, modular objects

$\langle\cdot,\cdot\rangle$ is conjugate linear in the first
variable.  $S=J\Delta^{1/2}$, $F=S^{*}=J\Delta^{-1/2}$, $J\Omega=\Omega$, $\Delta\Omega=\Omega$,
$J\mathcal{M} J=\mathcal{M}'$.  In the line chart with $I=(-\infty,L)$ and $u=L-x$, (BW) says that $\Delta^{it}$ is the
dilation $u\mapsto e^{2\pi t}u$ and $J$ implements $u\mapsto-u$, i.e. $x\mapsto 2L-x$.

### Hardy projections

For the free fermion the one-particle space is $L^{2}(\mathbb R)$ and
$\Pi_{\pm}$ are the spectral projections of the momentum $-i\partial_{x}$ onto $\pm(0,\infty)$; we use
*$\Pi_{+*=$ positive momenta}, so that $\Pi_{+}L^{2}$ is the Hardy space of the upper half plane and
the vacuum is the Fock state of $\Pi_{+}$.  The opposite convention ($\Pi_{+}=$ negative momenta) is also
common; it replaces $V=\Pi_{-}W\Pi_{+}$ by $\Pi_{+}W\Pi_{-}$, which has the same Hilbert--Schmidt norm, so
none of the quoted numbers changes.  With $\mathfrak L_{f}=f\partial_{x}+\frac12f'$ one has
$T(f)= : d\Gamma(-i\mathfrak L_{f}) :$ and $T(f)\Omega\cong\Pi_{-}(-i\mathfrak L_{f})\Pi_{+}$, and
$\|\Pi_{-}\mathfrak L_{f}\Pi_{+}\|_{\mathfrak S_{2}}^{2}=\frac{1}{48\pi^{2}}\int_{0}^{\infty}
p^{3}|\hat f(p)|^{2}dp$, i.e. (eq:appnorm) at $c=1$ (checked numerically to $1.5\cdot10^{-11}$).

### The constants, and where they come from

| llp{0.44\textwidth}@{}} Constant | Value | Source |
|---|---|---|
| $\gamma_{0}$ | $2/(3\pi^{2})=0.0675$ | (thm:value): $c$-linearity ((thm:linear)) plus the free-fermion distance $\frac{1}{6\pi^{2}}$ of Paper 1 (Paper1,RigorUB) |
| $g_B$ | $c \gamma_{0}=2c/(3\pi^{2})$ | (thm:value); independently reproduced by the modular-frame computation of Note 7 (Note7) (a confirmation, not a proof: (rem:mellin)) |
| $f_{2}$ | $g_B/8=c/(12\pi^{2})$ | (thm:B); at $c=1$, $0.0084434$ |
| $\inf\\|G\\|_{3/2}^{2}$ | $8/\pi=2.546479$ | (rem:varform), equivalent to $g_B$ at $c=1$; Rayleigh--Ritz value $2.547971$ ($0.06\%$) |
| $g_{\mathrm{KM}}$ | $c/6$ *(conjectural)* | (sec:km); free-fermion reduction $g_{\mathrm{KM}}=1/6$ (RigorKM), an analytic continuation; the gauge lemma is refuted (RigorRK) |
| $s_{2}$ | $g_{\mathrm{KM}}/2=c/12$ *(conjectural)* | (sec:km); proved bracket $0.034 c\le\liminf\le\limsup\le0.924 c$ (RigorRK); bosonic check $0.083(2)$ ((sec:boson)) |
| $J_{\rm jump}$ | $-1/L$ | (thm:reg): jump of $G''$ at the touching point, $G$ the *circle* representative; the line-chart field has $g_{\rm tot}''$ jumping by $-2/L$ |
| $\\|T(g_{\rm tot})\Omega\\|^{2}$ | $\frac{c}{12}\\|g_{\rm tot}\\|_{\dot H^{3/2}}^{2}$ | (thm:reg)(f); finite, whereas $\\|L_{0}T(g_{\rm tot})\Omega\\|^{2}$ diverges logarithmically with coefficient $\frac{c}{12}\frac{J_{\rm jump}^{2}}{4\pi^{2}}$ |

## From `rigor/phase6_brief.md`

### MODULAR FRAME of I

y = log((x-p_1)/(p_{n+1}-x)), beta_I(x) = dx/dy = (x-p_1)(p_{n+1}-x)/T. The first-order field of a corner (p, kappa) is EXACTLY zeta w(y - y_p) d/dy with w(u) = -4 sinh^2(u/2) 1_{u>0} (Phase 5 F1 Prop 6.2, f3_t0.py) and zeta = kappa beta_I(p).  \[Derivation: in the (0,inf)-frame X = e^y, -sigma'(X-X_p)^2 d/dX = -sigma' X_p (X/X_p - 2 + X_p/X) d/dy = sigma' X_p w(y-y_p) d/dy, and sigma' X_p = sigma beta_I(p) by the (-1)-density law sigma' = sigma/M'(p) of parabolic parameters under a Moebius change of coordinate M. Theorem A's zeta = a s/(a+L) is the case p = 0, I = (-a, L): beta_I(0) = aL/(a+L), sigma = s/L.\]

---

[Documentation map](index.md) · [All claims by area](status.md)
