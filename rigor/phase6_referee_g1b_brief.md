# Referee brief REF-P6-4 — rigor/network_second_order.tex and the six G1b cards (2026-10-03)

## 1. Role
Referee. `KB_ACTOR=REF-P6-4`, every kb command `-p cft_cmi`, model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it). Never git, never ./pgit, never
edit a reviewed document, script or card text (§1: only `kb verdict`, `kb note`, and `kb set ID evidence=` for a wrong
locator). Stance: adversarial; the burden of proof is on the document and the cards. Nothing is accepted from memory:
every cited result is checked in the PDF under refs/ (or marked NOT OBTAINED).

## 2. Object
Document under review: rigor/network_second_order.tex (27 pp, author G1b; brief rigor/phase6_g1b_brief.md). Its
numerical check: rigor/g1b_kernel.py, rigor/g1b_kernel.out. Context (read as needed, not under review):
rigor/phase6_brief.md (conventions; W2, W4, W5), rigor/network_corner_calculus.tex (G1a, refereed: lem:field,
thm:general, thm:corner, thm:state, lem:ampl, thm:sep), rigor/quadratic_limit.tex (thm:lower), rigor/uhlmann_upper_bound.tex
(thm:main-upper, thm:three-faces), rigor/rate_of_remainder.tex (thm:global, Def. 2.1), rigor/universality_theorem_B.tex
(thm:linear, thm:B), rigor/implementation_C11.tex, numerics/optimality_all/f3_t0.py (ddot, g_Q).
Cards under review (`kb -p cft_cmi show ID`, after `kb -p cft_cmi summary`; read each card's Notes first):
network-law-free-fermion, corner-kernel-closed-form, network-global-bound-coincident, network-upper-uniform-two-corners,
network-law-c-linear [all proved], network-remainder-uniformity [open]. NOT under verdict (G3 is still writing on them;
report on the accuracy of G1b's notes only): network-second-order-law, corner-correlation-kernel, vwz-protocol-ordering.
Status file: rigor/PHASE6_STATUS.md.

## 3. Deliverable: rigor/referee_network_second_order.tex (Lamport verdict document, `\input{rigor_preamble}`)
Per theorem one verdict: STANDS / STANDS WITH REPAIR / FAILS, with the step and the counter-argument; quote the
objected sentence or equation. Checklist (every item gets a line, every inequality its direction):
 1. lem:frame, lem:canon: the frame reduction and the canonical composite Psi_s; its corner measure equals s sum kappa_k
    delta_{q_k} and (by G1a thm:corner/thm:state) it carries the recovered state of every (H)-protocol: is the
    hypothesis (H) stated and used; is "right compressions in canonical order" the same object as the protocols?
 2. lem:implementer: normality, implementation, telescoping; every hypothesis of Note 4 Thm 7.1 / G1a thm:state checked.
 3. lem:Dtot: the first-order defect of the composite = sum of translated single-corner defects; sign and the frame of
    the translation (y_k, not -y_k); recompute item L of g1b_kernel.out independently.
 4. lem:polar, lem:taylor: is first-order differentiability of the compressed symbol enough where quadratic_limit
    thm:lower assumed more (analyticity)? Identify the exact hypothesis of thm:lower and check it.
 5. thm:T1 (lower bound, direction >=): data processing + Legendre form; linearity in the defect; the compression P.
 6. lem:prodexp, prop:inf, thm:T2 (upper bound, direction <=): Uhlmann with the product of one C^{1,1} flow per corner;
    the infimum over commutant generators equals the SLD form with the SUMMED generator; every hypothesis of
    uhlmann_upper_bound thm:main-upper / thm:three-faces checked for the multi-corner field.
 7. cor:law: both halves give the law at FIXED configuration only; is any uniformity claimed anywhere by accident?
 8. lem:nogroup: Psi_s o Psi_t != Psi_{s+t} for M >= 2 (recompute the Schwarzian mass -2 t kappa_2 exactly, e.g. with
    sympy or exact rationals).
 9. thm:T3 (global bound, direction <=; constant Z^2 = (sum zeta_k)^2): the per-corner Dyson-cocycle groups, the move
    into the commutant, the Hilbert-Schmidt triangle inequality; the claim that it is weaker than the network form
    because 0 < Ghat(Delta) < Ghat(0) for Delta != 0, and equal when all corners coincide.
10. thm:T4(a): rho(q) = tanh(pi q)/(48 pi^2 q (1+q^2)) from the brief's rho(q) = (1/4) int dp |dhat_0|^2/W: redo the p
    integral independently (at least numerically at 5 values of q, tolerance 1e-10). (b) Ghat(0) = 1/(12 pi^2) exactly.
    (c) dhat_0(p,p') = (w(p)-w(p'))(p+p')/(2 pi (p-p')(1+(p-p')^2)): direct 2-D Fourier integral of ddot at 5 points
    with YOUR OWN code; the Fourier sign convention used, and whether it is the one of f3_t0.py. (cf) the closed form
    (1/12 pi^2)[cosh(Delta/2) - sinh^2(Delta/2) log coth(|Delta|/4)] and the series: check each step of the
    Mittag-Leffler / partial-fraction / Fourier-pair derivation (lem:lorentz), and the value at 9 Delta's against an
    independent quadrature of int rho(q) cos(q Delta) dq. (d) both bounds x(4-x^2)/(36 pi^2) <= Ghat <= x/(9 pi^2),
    x = e^{-|Delta|/2}, on a grid Delta in [0.01, 20], and the sharpness claim. (e) Ghat > 0, strictly decreasing,
    C^1 not C^2 at 0 (check the second derivative's log singularity).
11. cor:W3W4: what exactly is inferred for W3 and W4; nothing beyond the proved theorems.
12. lem:onegroup, thm:T5 (uniform upper bound, M = 2, direction <=; "for every compact Z and eps there is s_eps"):
    is the cross term really controlled uniformly in y_2 - y_1 -> infinity (the far corner acts near the moving
    endpoint)? Where does the proof use M = 2?
13. cor:vwz: 1 <= liminf <= limsup Phi(2)/Phi(1) <= 2; the lower bound by restriction to F(p_2, p_5) with zeta =
    2a/(a+2b) (recompute the strengths zeta_1 = a/b, zeta_2, zeta_3 and e^{Delta_23} = 1/eta from G1a lem:LRdata; data
    processing direction); the upper bound needs Ghat(log 1/eta) -> 0 (item 10(d)).
14. thm:T6 (c-linearity under Theorem B's hypotheses): (H1)-(H2') for the product, prop:H3/prop:H2 of Theorem B, the
    H_T reduction with a_tot; the restriction to canonical-order right compressions is stated in the theorem, and the
    card says "under implementer-hypotheses" (depends) -- is the status word the weakest the evidence supports?
15. The open card network-remainder-uniformity: are (U1), (U2) the exact obstructions the document's verdict box
    states; is `next` a named lemma or a named computation?
16. Cards: every Statement against the theorem it cites (quantifiers, ranges, constants, "at fixed configuration");
    every evidence locator resolves (`grep -n` the label); every `depends` card says what the Statement needs; the six
    findings_entries.tex entries G1b appended (plain LaTeX, accurate); the G1b notes on the three orchestrator cards.
Numbers to recompute independently (your own scripts rigor/ref_p6_4_*.py with outputs rigor/ref_p6_4_*.out; no code
shared with g1b_kernel.py beyond numpy/scipy/mpmath): Ghat(0)/f2; Ghat/Ghat(0) at Delta = 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8
(closed form vs your quadrature of rho; tolerance 1e-8); the five dhat_0 spot values; the lem:Dtot identity; the
Schwarzian mass of lem:nogroup. Also rerun `PYTHON=$V/bin/python $V/bin/python rigor/g1b_kernel.py >
rigor/ref_p6_4_g1b_kernel_rerun.out` (never onto rigor/g1b_kernel.out) and diff.

## 4. Conventions: rigor/phase6_brief.md "Setting and conventions"; T0 frame I = (-inf,1), y = -log(1-x); Fourier
convention as the document defines it (check it is used consistently and matches f3_t0.py where it imports ddot).

## 5. Working results: W2, W4, W5 of rigor/phase6_brief.md are UNREFEREED targets; the document's theorems are claims
under your review; G1a's theorems (refereed, cards proved) may be used with their locators.

## 6. Output paths (the only files you may create): rigor/referee_network_second_order.tex and its pdflatex
by-products; rigor/ref_p6_4_*.py, rigor/ref_p6_4_*.out; rigor/shots/ref_p6_4_*.png via rigor/snap.py if you need an
excerpt (list them under NEEDS ORCHESTRATOR).

## 7. Environment
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/venv
(numpy, scipy, mpmath, python-flint, sympy is NOT installed: use exact rationals/mpmath). Scripts read `PYTHON` else
python3, paths from `_ROOT`. Over 2 min: nohup ... & disown, output in rigor/; else Bash timeout <= 600000 ms. No
`timeout` binary; absolute paths; cwd drifts. G2 and G3 run in parallel: at most 2 cores.

## 8. Verdicts, rules, report
- Per card: `KB_ACTOR=REF-P6-4 kb -p cft_cmi verdict ID pass` (STANDS) or `... verdict ID fail --note "<repair,
  locator>"` (STANDS WITH REPAIR or FAILS). A competing verdict goes in a new note, never by flipping another referee's
  line. Never edit a referee note. For a wrong locator only: `kb set ID evidence=...`.
- File first: the report skeleton (one section per checklist item, PENDING) within your first 3 tool calls; appends
  <= 100 lines / 12,000 characters, compile after each (pdflatex twice from rigor/; the log must end with no `^!` and no
  undefined reference; report the page count). Chat <= 5 lines; reason only to the next tool call.
- Stop and report on every §9 trigger (a source NOT OBTAINED; a hypothesis you cannot check).
- Final message: at most 400 words; one line per card and per theorem, failures first, each with reason and locator;
  then `kb -p cft_cmi lint` counts; NEEDS ORCHESTRATOR (shots, files).
