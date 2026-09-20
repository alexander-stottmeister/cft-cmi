<!-- Assembled once by tools/build_docs.py from paper1/app_conventions.tex,
     paper2/app_conventions.tex and the conventions block of rigor/phase6_brief.md.
     Change the next line to `hand-edited: yes` after a human pass and the
     generator will leave this file alone. -->
<!-- hand-edited: no -->

# The objects, and what they mean

The objects the results are about: the compression map, the stress tensor normalisation, fidelity and relative entropy, the one-sided recovery step and the Schwarzian corner data. As with the symbol table, this is a first assembly awaiting a human pass.

Assembled from [`paper1/app_conventions.tex`](../paper1/app_conventions.tex), [`paper2/app_conventions.tex`](../paper2/app_conventions.tex), [`rigor/phase6_brief.md`](../rigor/phase6_brief.md). Mathematics is reproduced as LaTeX; a renderer that supports it will typeset it, and the sources above are authoritative.

## From `paper1/app_conventions.tex`

### Preamble

Every constant quoted in this paper depends on the following choices, which are
fixed once and used everywhere.

### Half-density push-forward

For an increasing $C^{1,1}$ diffeomorphism $\varphi$,
$$
 (W_\varphi f)(y)=f\bigl(\varphi^{-1}(y)\bigr)
 \bigl((\varphi^{-1})'(y)\bigr)^{1/2}
 =\frac{f(\varphi^{-1}(y))}{\sqrt{\varphi'(\varphi^{-1}(y))}} ,
$$
which is unitary on $L^2(\mathbb R)$ and isometric between the corresponding
interval subspaces.  We write $u(x)=x-\varphi(x)$ for the displacement, so
$\varphi'=1-u'$.  The recovery flow inside $D$ is
$\varphi=h_s$ of (eq:hs), with generator $-x^2/L\cdot\partial_x$, i.e.\
$u_s(x)=sx^2/(L+sx)$ on $[0,L]$; the total first-order field is
$g_{\rm tot}=0$ on $(-a,0)$, $g_{\rm tot}(x)=-x^2/L$ on $(0,L)$, and free on
$I'=(-\infty,-a]\cup[L,\infty)$.

### Stress tensor

The generator normalization is
$$
 \langle T(x)T(y)\rangle=\frac{c_{\rm cft}}{8\pi^2} (x-y-i0)^{-4},
$$
i.e. $T$ is normalized so that its smeared version generates the M\"obius flow
with unit coefficient.  This is the convention in which the two quadratic forms of
the recovery curve come out as
$$
 \boxed{
 g_B=\frac{2c_{\rm cft}}{3\pi^2},\qquad
 g_{\mathrm{KM}}=\frac{c_{\rm cft}}6,\qquad
 f_2=\frac{g_B}8=\frac{c_{\rm cft}}{12\pi^2},\qquad
 s_2=\frac{g_{\mathrm{KM}}}2=\frac{c_{\rm cft}}{12},\qquad
 \frac{s_2}{f_2}=\pi^2 . }
$$
The metric normalizations behind the factors $\frac18$ and $\frac12$ are those of
(def:gB):
$-\logF=\frac{\zeta^2}8g_B+o(\zeta^2)$ and $D=\frac{\zeta^2}2g_{\mathrm{KM}}+o(\zeta^2)$ per
unit of the deformation parameter, the parameter being $\zeta$.

## From `paper2/app_conventions.tex`

### Preamble

The value of $f_{2}$ is normalisation dependent, so we collect the conventions in one place and make every
constant in the paper traceable to them.

### Stress tensor

The generator normalisation used throughout is
$$
 \langle\Omega,T(x)T(y)\Omega\rangle=\frac{c}{8\pi^{2}} \frac{1}{(x-y-i0)^{4}},
 \qquad U(\mathrm{Exp}(tf\partial_{x}))=e^{itT(f)}  \text{(up to phase)} .
$$
The BPZ-normalised field is $2\pi T$, with $\langle(2\pi T)(x)(2\pi T)(y)\rangle=\frac{c}{2}(x-y)^{-4}$.
Equivalent forms of (eq:appTT), used at various points:
$$
 \|T(f)\Omega\|^{2}=\frac{c}{48\pi^{2}}\int_{0}^{\infty}p^{3}|\hat f(p)|^{2}dp
 \quad\text{(line)},\qquad
 \|T(G)\Omega\|^{2}=\frac{c}{12}\sum_{n\ge2}n(n^{2}-1)|\hat G_{n}|^{2}
 \quad\text{(circle)} .
$$
The first follows from (eq:appTT) and
$\int e^{-ipu}(u-i0)^{-4}du=\frac{2\pi}{3!}|p|^{3}\theta(-p)$; the second from
$\langle L_{-n}\Omega,L_{-n}\Omega\rangle=\frac{c}{12}n(n^{2}-1)$.  In the modular frame the thermal
spectral density is $\widehat W(k)=\frac{c}{24\pi}\frac{k(k^{2}+1)}{e^{2\pi k}-1}$; see (rem:mellin)
for the status of the computation that uses it.

### The compression map and the cross ratio

For the general configuration $A=(-a,0)$,
$D=(0,L)$, the zero-collar compression is
$$
 k_{s}|_{A}=\mathrm{id},\qquad k_{s}(x)=h_{s}(x)=\frac{Lx}{L+sx}  (x\in D),
$$
and all recovery quantities depend on $(a,L,s)$ only through the cross ratio
$$
 \zeta=\frac{a s}{a+L}.
$$
Two normal forms are used.  The half-line normal form $a=\infty$ gives $\zeta=s$ and is the one in which
(sec:univ,sec:impl) are written; the bosonic computation of (sec:boson) uses $a=1$, $L=2$, i.e.\
$\zeta=s/3$.  The first-order field of the extended map $\tilde k_{s}$ is $g_{\rm tot}$ of (eq:chi):
$g_{\rm tot}=0$ on $A$, $g_{\rm tot}(x)=-x^{2}/L$ on $D$, smooth and compactly supported beyond $L$; it is
$C^{1,1}$ with a single jump of its second derivative at the touching point, of size $-2/L$ in the line
chart and $-1/L$ for the circle representative $G$ ((thm:reg)).  In the rotated Petz family
of (FHSW) the parameter enters as $\zeta_{t}=z(1+e^{-2\pi t})$, $t=0$ being the ordinary Petz map.

### Fidelity and relative entropy

$F$ is the root fidelity, $F=\operatorname{Tr}|\rho^{1/2}\sigma^{1/2}|$
in finite dimensions, equal to $\sqrt{P_{\mathcal{M}}}$ with $P_{\mathcal{M}}$ the Uhlmann transition probability
(AU02); $\Phi(\zeta)=-\logF(\omega,\omega_{\zeta})$.  Relative entropy is Araki's
$D(\omega\Vert\omega_{\xi})=-\langle\Omega,\log\Delta_{\xi,\Omega}\Omega\rangle$ (Araki), and the
Kubo--Mori metric is its second variation, $D=\frac{s^{2}}{2}g_{\mathrm{KM}}+o(s^{2})$, so that $s_{2}=g_{\mathrm{KM}}/2$ with
$\Phi$ and $D$ both expressed in $\zeta$.

## From `rigor/phase6_brief.md`

### Chain geometry

Points p_1 \< ... \< p_{n+1}; A_k = (p_k, p_{k+1}), l_k = p_{k+1} - p_k, L_k = p_{k+1} - p_1 = l_1 + ... + l_k, T = L_n, I = (p_1, p_{n+1}). c = central charge per chirality; f2 = c/(12 pi^2) (const-f2). The hopping chain has two chiralities: dictionary in numerics/lattice/README.md.

### ONE-SIDED STEP

block J (a union of consecutive A's, hence an interval), conditioning interval A_B = the interval of J adjacent to the new interval A_new, corner point p = the INNER end of A_B (its junction with the rest of J; for J = A_B alone, the end of A_B away from A_new). The zero-collar (rotated or ordinary) Petz map of the half-sided modular inclusion F(A_B) subset F(A_B u A_new) is the parabolic Moebius compression fixing p that pushes A_B u A_new toward p: in an affine coordinate, h(x) = p + (x-p)/(1 + sigma (x-p)) for A_new to the right of p (sigma > 0), the mirror image for A_new to the left; sigma = s/(l_B + l_new), s in \[lambda, 2 lambda\], lambda = l_new/l_B; s = 2 lambda is the ordinary Petz map (VWZ's lambda = 0), s_t = lambda (1 + e^{-2 pi t}) the rotated maps (paper1/sec_petz.tex Def. zeta; Note 4 Thm 7.1). The step acts as the identity on J \\ A_B. Compression strength of the corner: kappa := -\[h''/h'\](p)/2 = sigma > 0 for a compression toward p from EITHER side (both give the same sign of the jump).

### STEP FRAME vs CHAIN FRAME (amplification)

the same corner has zeta_step = kappa beta_{I_step}(p) in the interval I_step = (kept block) u A_B u A_new of its own Theorem-A triple, and zeta^(I) = kappa beta_I(p) in the frame of the whole chain; zeta^(I)/zeta_step = beta_I(p)/beta_{I_step}(p) = 1 + z', z' = cross ratio of (p_1, p, far end of I_step, p_{n+1}) = the Markov variable z = a c/(b (a+b+c)) of the coarse triple (kept block | A_B u A_new | rest of the chain). >= 1, = 1 for the last step.

### Chain geometry

L->R PETZ CHAIN (start with A_1 A_2, add A_3, ..., A_n; ordinary Petz): corner k at p_k, k = 2..n-1, kappa_k = 2 l_{k+1}/(l_k (l_k + l_{k+1})), zeta_k^(I) = kappa_k L_{k-1} (T - L_{k-1})/T, y_k = log(L_{k-1}/(T - L_{k-1})). With r_k = l_{k+1}/l_k, u_k = l_k/L_{k-1}, v_k = l_k/(T - L_k): e^{Delta_k} = e^{y_{k+1} - y_k} = (1+u_k)(1+v_k) and zeta_k^(I) = 2 r_k (1+v_k)/((1+r_k)(e^{Delta_k} - 1)).

### SCHWARZIAN of a C^1 piecewise-Moebius map

S(Phi) = sum_k \[Phi''/Phi'\](p_k) delta_{p_k} (no square term: h' is continuous); parabolic corner: \[h''/h'\](p) = -2 kappa. Composition: S(Phi_1 o Phi_2) = S(Phi_2) + (Phi_2')^2 S(Phi_1) o Phi_2.

### Fidelity conventions

Phi := -log F on F(I) (paper 1); Note 5 Thm 2.1 (symbols) / Thm 3.2 (finite matrices); g_Q(delta) = (1/4) sum |delta_ij|^2/(w_i(1-w_j)+w_j(1-w_i)) in the eigenbasis of Q (f3_gal.theta: g0), Phi \~ g_Q(delta).

---

[Documentation map](index.md) · [All claims by area](status.md)
