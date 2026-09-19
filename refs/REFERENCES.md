# Master reference list (what our notes cite, where, and how to obtain it)

Download with `refs/getref.sh <arxiv-id> <Short>` (arXiv) or `refs/getref.sh <URL> <Short>`.
Notes: N1 adjacent_interval_cmi_longo_xu.tex, N2 cmi_as_quantum_markov_defect.tex, N3 cmi_cft_research_program.tex,
N4 continuum_petz_free_fermion.tex, N5 fidelity_recovered_quasifree.tex, N6 strategy_open_problems.tex, N7 universality_normalization.tex.

| Short | Reference | Source | Used in | Results used |
|---|---|---|---|---|
| LongoXu | Longo, Xu, Relative entropy in CFT, Adv. Math. 337 (2018) | arXiv:1712.07283 | N1,N2,N4,N5,N7 | Thm 3.18 (free-fermion MI), Thm 4.1 (generalized MI, positivity, finite-dim limit), Thm 4.2 (G-identity, singular limit), Rmk 4.3; mutual-information formula for two intervals; Hardy-projection realization of the vacuum |
| CasiniHuerta09 | Casini, Huerta, Reduced density matrix and internal dynamics for multicomponent regions, CQG 26 (2009) | arXiv:0903.5284 | N5,N7 | modular Hamiltonian / eigenfunctions of the interval Hardy compression; spectrum 1/(1+e^kappa); thermal form |
| BGL93 | Brunetti, Guido, Longo, Modular structure and duality in conformal QFT, CMP 156 (1993) | Project Euclid (open) https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-156/issue-1/ | N4,N7 | geometric modular group of interval algebras (Bisognano-Wichmann for conformal nets), modular conjugation geometric |
| Wiesbrock93 | Wiesbrock, Half-sided modular inclusions of von Neumann algebras, CMP 157 (1993) 83-92; and CMP 158 (1993) 537-543 (conformal QFT and hsm inclusions) | Project Euclid (open) | N4 | hsm inclusion <-> Borchers translations; interval algebras with a common endpoint are hsm |
| Borchers92 | Borchers, The CPT-theorem in two-dimensional theories of local observables, CMP 143 (1992) | Project Euclid (open) | N4,N7 | Borchers' commutation relations Delta^{it} U(s) Delta^{-it} = U(e^{-2 pi t} s), J U(s) J = U(-s) |
| FHSW20 | Faulkner, Hollands, Swingle, Wang, Approximate recovery and relative entropy I, CMP 389 (2022) | arXiv:2006.08002 | N2,N4,N5,N6,N7 | rotated Petz maps alpha_{sigma,t}; Sec 4.2 hsm inclusions (Petz map = Borchers translation, rotated = translation by 1+e^{-+2 pi t}); strengthened DPI with p(t)=pi/(cosh 2 pi t +1) (integrated form); standard-form Petz formula J_N V^* J_M x J_M V J_N |
| FH22 | Faulkner, Hollands, Approximate recoverability and relative entropy II, LMP 112 (2022) | arXiv:2010.05513 | N2 | 2-positive channels version |
| JRSWW | Junge, Renner, Sutter, Wilde, Winter, Universal recovery maps..., AHP 19 (2018) | arXiv:1509.07127 | N2 | universal recovery with the p(t) average |
| SFR | Sutter, Fawzi, Renner, Universal recovery map for approximate Markov chains, Proc R Soc A (2016) | arXiv:1504.07251 | N2 | |
| FR | Fawzi, Renner, Quantum CMI and approximate Markov chains, CMP 340 (2015) | arXiv:1410.0664 | N2 | |
| HJPW | Hayden, Jozsa, Petz, Winter, Structure of states which satisfy SSA with equality, CMP 246 (2004) | arXiv:quant-ph/0304007 | N2 | direct-sum decomposition of exact Markov states |
| Petz86 | Petz, Sufficient subalgebras and the relative entropy of states of a von Neumann algebra, CMP 105 (1986) | Project Euclid (open) | N2 | sufficiency <-> equality of relative entropies <-> Connes cocycle in N |
| Petz88 | Petz, Sufficiency of channels over von Neumann algebras, Quart. J. Math. 39 (1988) | paywalled (flag; use Petz86 + arXiv surveys) | N3 | |
| PowersStormer70 | Powers, Stormer, Free states of the CAR, CMP 16 (1970) | Project Euclid (open) | N4,N5 | quasi-equivalence criterion for gauge-invariant quasi-free states (S^{1/2}-T^{1/2} and (1-S)^{1/2}-(1-T)^{1/2} Hilbert-Schmidt); Powers-Stormer inequality ||S^{1/2}-T^{1/2}||_2^2 <= ||S-T||_1 |
| Araki71 | Araki, On quasifree states of CAR and Bogoliubov automorphisms, PRIMS 6 (1971) | EMS Press / PRIMS open access | N4 | quasi-equivalence of quasi-free states (self-dual formalism) |
| Araki76 | Araki, Relative entropy of states of von Neumann algebras (I), PRIMS 11 (1976) | EMS Press open | N5 | Araki relative entropy definition |
| Araki77 | Araki, Relative entropy for states of von Neumann algebras II, PRIMS 13 (1977) | EMS Press open | N5,N7 | monotone (martingale) convergence of relative entropy along increasing subalgebras (exact hypotheses!) |
| OhyaPetz | Ohya, Petz, Quantum Entropy and Its Use, Springer 1993/2004 | book (not downloadable): use Araki77 and Petz's arXiv surveys; flag | N5 | Cor 5.12 (relative entropy convergence) |
| Alberti83 | Alberti, A note on the transition probability over C*-algebras, LMP 7 (1983) | paywalled: find open restatement (e.g. arXiv papers on fidelity for vN algebras) | N4,N5 | F(phi,psi)^2 = inf_{x>0} phi(x) psi(x^{-1}) |
| Uhlmann76 | Uhlmann, The transition probability in the state space of a *-algebra, Rep. Math. Phys. 9 (1976) | paywalled: find open restatement | N5,N7 | Uhlmann fidelity, standard-form formula <Omega, Delta_{phi,omega}^{1/2} Omega> |
| ArakiRaggio82 | Araki, Raggio, A remark on transition probability, LMP 6 (1982) | paywalled (flag) | N7 | |
| Jencova02 | Jencova, Quantum information geometry and standard purification, JMP 43 (2002) | arXiv:math-ph/0107020 (check id) | N7 | monotone metrics on vN algebra state spaces |
| Petz96 | Petz, Monotone metrics on matrix spaces, LAA 244 (1996) | maybe not on arXiv (flag) | N7 | |
| DaleckiiKrein | Daleckii-Krein formula (derivative of matrix functions) | any open source, e.g. arXiv surveys | N5 | second-order expansion of Tr X log X |
| VWZ | Vardhan, Wei, Zou, Petz recovery from subsystems in CFT, JHEP 03 (2024) 016 | arXiv:2307.14434 (already in refs/VWZ_2307.14434.pdf) | N3,N5,N6,N7 | eqs (1.3),(1.8),(2.1),(2.13),(2.14),(3.15),(3.24); lambda statements; Fig 5 exponents; App A.5 |
| SwingleWang19 | Swingle, Wang, Recovery map for fermionic Gaussian channels, JMP 60 (2019) | arXiv:1811.04956 | N3,N6 | Gaussian Petz map formulas |
| CDIW21 | Carpi, Del Vecchio, Iovieno, Tanimoto (cited as CDIW in the notes; correct acronym CDIT), Positive energy representations of Sobolev diffeomorphism groups of the circle, AHP 22 (2021) | arXiv:1808.02384 | N6 | extension to D^s(S^1), which s? |
| TakhtajanTeo06 | Takhtajan, Teo, Weil-Petersson metric on the universal Teichmuller space, Mem. AMS 183 (2006) | arXiv:math/0312172 | N6 | WP class, Hilbert-Schmidt condition |
| NagSullivan95 | Nag, Sullivan, Teichmuller theory and the universal period mapping via quantum calculus and the H^{1/2} space, Osaka J. Math. 32 (1995) | Project Euclid (open) | N6 | Segal-Shale condition <-> H^{1/2} |
| Shen18 | Shen, Weil-Petersson Teichmuller space, Amer. J. Math. 140 (2018) | arXiv:1304.3197 | N6 | characterization log phi' in H^{1/2} |
| FewsterHollands05 | Fewster, Hollands, Quantum energy inequalities in 2D CFT, RMP 17 (2005) | arXiv:math-ph/0412028 | N6,N7 | energy bounds / smearing class for T(f) |
| KirillovYuriev87 | Kirillov, Yuriev, Kahler geometry of the infinite-dimensional homogeneous space Diff/Rot, Funct. Anal. Appl. 21 (1987) | paywalled (flag) | N6 | |
| CalabreseCardy04 | Calabrese, Cardy, Entanglement entropy and QFT, JSTAT (2004) | arXiv:hep-th/0405152 | N3 | thermal single-interval entropy |
| CasiniHuerta04 | Casini, Huerta, A finite entanglement entropy and the c-theorem, PLB 600 (2004) | arXiv:hep-th/0405111 | N3 | entropic c-function |
| CTT17 | Casini, Teste, Torroba, Modular Hamiltonians on the null plane and the Markov property, JPA 50 (2017) | arXiv:1703.10656 | N2,N3 | null Markov property |
| Camassa12 | Camassa, Longo, Tanimoto, Weiner, Thermal states in conformal QFT II, CMP 315 (2012) | arXiv:1109.2064 | N3 | |

- `OstrowskiTaussky_via_2001.00683.pdf` — L. Nasiri, S. Furuichi, On a reverse of the Tan–Xie inequality for sector matrices (arXiv:2001.00683); Lemma 3.1 states the Ostrowski–Taussky inequality det(Re A) ≤ |det A| for accretive A (used in rigor/quadratic_limit.tex Thm 6.4).

## Added 2026-09-10 (Phase 3b, optimality among all channels)
- `BJL_twisted_duality_math-ph-0204029.pdf` — Baumgärtel, Jurke, Lledó, "Twisted duality of the CAR-algebra", J. Math. Phys. 43 (2002) 4158; used: Lemma 3.5, Lemma 4.10 (graph of β), Prop. 5.3, Cor. 5.4 (Tomita operator restricts to n-particle spaces; S↾p = β), Prop. 3.4 (generic position ⇔ cyclic and separating). Screenshots rigor/shots/BJL_p{7,11,15,16,22}.png.
- `Sion1958_minimax.pdf` — M. Sion, "On general minimax theorems", Pacific J. Math. 8 (1958) 171–176 (msp.org copy). Screenshots rigor/shots/Sion1958_p{3,4}.png.
- `AlbertiUhlmann02_math-ph-0202038.pdf` (already present) — Thm 2(1): F = inf_{x>0} ½{ν(x)+ρ(x⁻¹)}; screenshot rigor/shots/alberti_uhlmann_thm2_p11.png.
