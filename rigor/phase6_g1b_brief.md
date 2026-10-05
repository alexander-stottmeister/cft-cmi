# Brief G1b — second-order network law and the corner kernel Ghat (launched 2026-10-03)

## 1. Role
Track agent (author, not referee). `KB_ACTOR=G1b`, every kb command `-p cft_cmi`, model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (all paths below are relative to it). Never run git or ./pgit.

## 2. Object
Read, in this order: rigor/phase6_brief.md (conventions "Setting and conventions", results W2, W4, W5; W1, W3, W6 are
now PROVED in G1a's document), rigor/README_AGENTS.md (Lamport macros, \shot, citedbox), rigor/network_corner_calculus.tex
(G1a, 42 pp; cite its results by label: lem:field (exact first-order field zeta w(y - y_p) d/dy), lem:density,
thm:general, thm:corner, def:H, thm:state, cor:phiA, lem:ampl, thm:sep, thm:w6chord, cor:w6-second),
rigor/quadratic_limit.tex (thm:lower: data processing + Legendre form, linear in the defect; thm:upper),
rigor/uhlmann_upper_bound.tex (thm:main-upper, thm:three-faces, thm:det), rigor/rate_of_remainder.tex (thm:exactquad,
thm:global, Def. 2.1 admissible fields), rigor/universality_theorem_B.tex (thm:linear, thm:B),
rigor/implementation_C11.tex ((H1)-(H3) for fields with second-derivative jumps), numerics/optimality_all/f3_t0.py
(closed-form first-order kernel ddot and the quadratic form g_Q; F3_RESULTS.md Sec. 0 for g_Q(ddot)/f2 -> 1).
Cards (`kb -p cft_cmi show ID`, after `kb -p cft_cmi summary`): phase6-plan, network-second-order-law,
corner-correlation-kernel, vwz-protocol-ordering, corner-calculus, frame-strength-amplification,
corner-separation-constraint, sequential-recovery-bound-type-iii, thm-a-quadratic-law, const-f2, thm-b-universality,
implementer-hypotheses, bures-three-faces, second-variation-lemma. Status file: rigor/PHASE6_STATUS.md.

## 3. Deliverable: rigor/network_second_order.tex (Lamport; `\documentclass[11pt]{article}\input{rigor_preamble}`)
Setting: corners (p_k, kappa_k), k = 1..m, in the modular frame of I with positions y_k and strengths zeta_k =
kappa_k beta_I(p_k); the composite Phi under (H) (thm:corner), scaled family kappa_k -> s kappa_k, Phi_tot(s) :=
-log F(omega, omega o beta_{Phi_s}) on F(I) (free chiral fermion, c = 1, then the c-linear statement).
T1 (lower bound). liminf_{s->0} Phi_tot(s)/s^2 >= sum_{j,k} zeta_j zeta_k G(y_j - y_k), G(Delta) := g_Q(delta_0,
   delta_Delta) (bilinear form of the Bures/SLD quadratic form on first-order defects; delta_Delta = y-translate of ddot).
   Route: the first-order defect of the composite is sum_k zeta_k delta_{y_k} (lem:field per corner + composition);
   quadratic_limit thm:lower is linear in the defect. Every hypothesis of thm:lower checked in a step.
T2 (upper bound). limsup <= the same. Route: Uhlmann + C^{1,1} flow extension (uhlmann_upper_bound Sec. 1,
   rate_of_remainder) for a field with finitely many second-derivative jumps; the identity inf_ext = SLD form =
   4 dist(., commutant)^2 (thm:three-faces). If T2 needs a hypothesis you cannot discharge, state the theorem under it.
T3 (global bound). Phi_tot <= -(1/2) log(1 - 2 sum_{j,k} zeta_j zeta_k G(y_j - y_k)) when the group-extension argument
   of rate_of_remainder thm:global extends; otherwise the proved relation ("implies", "equivalent", "unknown").
T4 (kernel). With Q the Fourier multiplier w(p) = (1 + e^{-2 pi p})^{-1} in y (f3_t0.py docstring) and dhat_0(p,p') the
   Fourier transform of ddot: (a) G(Delta) = int dq rho(q) cos(q Delta), rho(q) = (1/4) int dp |dhat_0(p, p-q)|^2 /
   W(p, p-q), W(p,p') = w(p)(1-w(p')) + w(p')(1-w(p)); hence Ghat := G/c is even and positive-definite; (b) Ghat(0) =
   1/(12 pi^2) = f2 (must reproduce const-f2 exactly, else stop: §9); (c) dhat_0 in closed form if it exists (derive;
   Gamma/digamma-type integrals are expected), else as an explicit one-dimensional integral; (d) a PROVED decay bound
   Ghat(Delta) = O(e^{-alpha Delta}) with explicit alpha, and the sharp rate if you can prove it; (e) the sign of Ghat
   for Delta > 0: prove Ghat >= 0, or exhibit a Delta with Ghat < 0 by a certified evaluation, or state open with the
   obstruction. NO closed-form candidate may be chosen by matching numbers (§3); "agrees to N digits, no derivation".
T5 (uniformity). Is the o(s^2) remainder of T1/T2 uniform in the separations Delta_jk? Prove a bound with explicit
   dependence on (zeta, Delta), or state exactly what fails; vwz-protocol-ordering depends on it.
T6 (W5). c-linearity of Ghat by the H_T argument (universality_theorem_B thm:linear) and (H1)-(H3) for fields with
   finitely many second-derivative jumps (implementation_C11): theorem for every diffeomorphism-covariant net under the
   standing hypotheses of Theorem B, or the exact obstruction.
Numerical check (§4, §5): rigor/g1b_kernel.py + rigor/g1b_kernel.out (mpmath/scipy quadrature of your T4 formulas):
   Ghat(0)/f2 = 1 to 1e-8 (validation, exact case), then Ghat(Delta)/Ghat(0) at Delta = 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8
   with a stated quadrature tolerance (1e-8), two quadrature rules agreeing (state max deviation), and the decay fit
   compared with T4(d). These values are the continuum reference that G3 (two discretisations) is compared against.
Success criterion: T1, T2, T4(a)(b) proved with every leaf justified; the document compiles (pdflatex twice from
rigor/; log has no line matching `^!` or `(Reference|Citation).*undefined`; report the page count); every theorem
with a computable instance has its instance in g1b_kernel.out.

## 4. Conventions
Exactly rigor/phase6_brief.md "Setting and conventions" and cross-ratio-conventions; T0 frame I = (-inf, 1), y =
-log(1-x), ddot(y1,y2) = -(i/2 pi) sinh(y1/2) sinh(y2/2)/sinh^2((y1-y2)/2) (y1 < 0 < y2) + h.c.; g_Q as in f3_gal.theta
(g0). Fourier sign convention: write it once (Def.) and cite it. Any other convention: write the conversion out.

## 5. Working results (UNREFEREED targets, never assumptions): W2, W4, W5 of rigor/phase6_brief.md and the Statements
of network-second-order-law, corner-correlation-kernel, vwz-protocol-ordering. PROVED and citable with locator:
corner-calculus, frame-strength-amplification, corner-separation-constraint, sequential-recovery-bound-type-iii,
thm-a-quadratic-law, const-f2, thm-b-universality (under implementer-hypotheses).

## 6. Output paths (the only files you may create)
rigor/network_second_order.tex and its pdflatex by-products; rigor/g1b_*.py, rigor/g1b_*.out; rigor/shots/g1b_*.png via
rigor/snap.py; refs/ via refs/getref.sh; plain-LaTeX entries appended to rigor/findings_entries.tex (README_AGENTS rule).
Never edit rigor/network_corner_calculus.tex or any other existing document or script.

## 7. Environment
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/venv
(ready: numpy, scipy, mpmath, python-flint, cvxpy, clarabel, scs, pymupdf, matplotlib). Scripts: `PYTHON` else
python3, paths from `_ROOT`, outputs beside the script. Over 2 min: `nohup $V/bin/python x.py > x.out 2>&1 < /dev/null
& disown`; otherwise set the Bash timeout (<= 600000 ms). No `timeout` binary; absolute paths; cwd drifts.

## 8. KB, rules, stop conditions, report
- `kb -p cft_cmi q --text ...` before every add. Add a card for each theorem when proved (`KB_ACTOR=G1b kb -p cft_cmi
  add theorem ID --title ... --area lattice-thermal --status proved --statement ... --evidence doc:rigor/
  network_second_order.tex#LABEL,num:rigor/g1b_kernel.py --depends ... --tags phase6`), weakest status the evidence
  supports; `next` on open/conjectural cards. The cards of §2 belong to the orchestrator: `kb note` them with your
  evidence and put every status change on them under NEEDS ORCHESTRATOR. `kb -p cft_cmi lint` before the final message.
- File first: skeleton with every section heading and PENDING markers within your first 3 tool calls; appends of at
  most 100 lines / 12,000 characters, compile after each; chat at most 5 lines; reason only to the next tool call.
- Stop (write what you have, then report) on every §9 trigger, in particular: T4(b) fails to give f2; a hypothesis of
  thm:lower, thm:main-upper or thm:linear fails for the multi-corner field; a source is NOT OBTAINED.
- Final message: §8 format (FILES, KB, FINDINGS, NUMBERS, NOT DONE, NEEDS ORCHESTRATOR), at most 400 words. List
  snap.py and getref.sh files under NEEDS ORCHESTRATOR (./pgit sync).
