# C7 Directions — advisory memo (council of 2026-11-19)

Actor C7 (track agent, advisory). KB read-only; nothing here is established unless it cites a card with its status.
All candidate statements below are UNREFEREED targets.

## 0. Sources read
AGENTS.md; rigor/council/COUNCIL_BRIEF.md; `kb -p cft_cmi summary`; `kb -p cft_cmi q --status open|conjectural|heuristic|active`;
`kb links --project cft_cmi`; cards shown in full: network-remainder-uniformity, network-upper-uniform-two-corners,
network-law-c-linear, multi-interval-networks, theta-modular-wiener-hopf, compression-not-optimal-exact-fidelity,
exact-fidelity-optimality-open, conj-s2, const-gkm-general-nets, sectors-o11, group-index-zero-large-s,
pushforward-blocks-equal-singular-values, dhat-quadrature-certification, certified-numerics, longo-xu-cmi,
longo-xu-cmi-general-c; `kb impact` for group-index-zero-large-s, pushforward-blocks-equal-singular-values,
certified-numerics. Documents (excerpts): rigor/network_second_order.tex l. 1030-1065; rigor/implementation_C11.tex
l. 805-850; rigor/exact_fidelity_upper_half.tex l. 839; open_problems_plan.tex sec:O11 (l. 304-306, 363, 377);
rigor/PHASE6_STATUS.md (open items); refs/LongoXu_1712.07283.pdf (pdftotext, Th. 4.2 and Remark 4.3).
Every "proved/numerical/conjectural" below is the card's status, not a judgement of this memo.

## 1. Candidate D1: uniform lower bound (U1) of network-remainder-uniformity
Cards: `network-remainder-uniformity` [open], `network-upper-uniform-two-corners` [proved, review passed REF-P6-4],
`network-law-free-fermion`, `corner-kernel-closed-form`, `vwz-protocol-ordering` [conjectural].

(i) First statement (lemma, M = 2, free fermion c = r). For every compact Z in (0,inf)^2 and eps > 0 there is s_eps > 0
such that for all 0 < s <= s_eps, (zeta_1, zeta_2) in Z and all y_1 < y_2:
Phi_tot(s) >= s^2 c [Ghat(0)(zeta_1^2 + zeta_2^2) + 2 zeta_1 zeta_2 Ghat(y_2 - y_1) - eps].
Combined with thm:T5 this closes M = 2 uniformity and, by the route already written in cor:vwz <1>3, upgrades
cor:vwz to lim Phi(2)/Phi(1) = 2 as a/b -> 0 (the 2 of `vwz-protocol-ordering`). A cheaper preliminary
computation: at fixed s in {0.05, 0.1, 0.2} evaluate Phi_tot(s; Delta)/s^2 - c Q(Delta) on Delta in [0, 10] with the
exact two-corner fidelities of numerics/networks/corner_kernel.py (block K4) and test whether the sup over Delta
decreases with s (tolerance to be fixed in the script before the run). This only informs; it cannot prove (U1).

(ii) Home: new lemma in rigor/network_second_order.tex sec:T5 (by its author) or a standalone
rigor/network_uniform_lower.tex; numerics in numerics/networks/ (new block K5 of corner_kernel.py or a sibling script).

(iii) Rests on: network-law-free-fermion (pointwise law), corner-kernel-closed-form (Ghat), corner-calculus,
thm-a-quadratic-law, network-upper-uniform-two-corners (the upper half, and its lem:onegroup with the MINOR range
restriction sigma ||[P_-,K]||_2 < 1 noted by REF-P6-4).

(iv) Obstacle, as recorded in the verdict box closing sec:T5 (rigor/network_second_order.tex l.1046-1059): the lower
bound of thm:T1 goes through a Legendre/variational step that compresses to a finite-rank P with no rate in s.
Uniformity in Delta needs (a) a spectral gap of P Q_I P away from 0 and 1 and (b) a bound on
||P(delta(s) - s D_tot)P|| uniform in Delta, for trial operators that are translated with the corners. As Delta -> inf
the two trial blocks separate and (a) is plausible from the decay Ghat(Delta) -> 0 (Cor. W3W4(i)); the hard regime is
Delta -> 0, where the two corners merge and the trial space degenerates (it becomes the single-corner problem with
zeta_1 + zeta_2, which is the content of `network-global-bound-coincident`). A proof will likely split Delta into
[0, Delta_0] (compactness plus continuity in Delta of the exact fidelity, which itself must be proved) and
[Delta_0, inf) (asymptotic decoupling).

(v) Payoff: closes the M = 2 half of the only open question of the Phase 6 law; turns cor:vwz into a limit (=2),
which is the cleanest comparison with Vardhan-Wei-Zou and the headline result a network paper 3 would want.

(vi) Difficulty: medium-high. Reason: the upper half needed only translation-invariant cross terms; the lower half
needs a quantitative (rate-carrying) version of a compression step that currently has none, and continuity of the
exact fidelity in Delta at s fixed is not on any card. The numerical test is low risk (script exists, exact kernels)
and is the right first step: if the sup over Delta does not decrease, (U1) is false as stated and the question is
answered negatively.

## 2. Candidate D2: Moebius implementer step for non-canonical orders
Cards: `network-law-c-linear` [proved; covers canonical-order products only], `c11-extension-implementer` [proved],
`implementer-hypotheses` [refereed], `thm-b-universality` [refereed], `multi-interval-networks` [open].

(i) First statement. Let (A, U, Omega) satisfy Theorem B's standing hypotheses, Psi the C^{1,1} single-corner map with
field g (Implementation_C11 thm:main) and h a Moebius transformation. Claim (M): for the unitary U_Psi of thm:main,
U(h) U_Psi U(h)^* implements h o Psi o h^{-1} on A(h I) in the sense of thm:main (equal, up to a phase and a factor in
A(hI)', to exp(i s T(h_* g)) where h_* g is the transported C^{1,1} field), i.e. Moebius covariance of T(f) for real
f with ||f||_{3/2} < inf. Writing h o Psi = (h Psi h^{-1}) o h, (M) gives U_{h o Psi} in T U(h) U_Psi A(I)', which is
exactly the missing step named in network-law-c-linear (rigor/implementation_C11.tex l. 824, paragraph (b)). Then
compute: the corner data of VWZ Protocol 3 in the canonical form and check that thm:T6 applies.

(ii) Home: a new section of rigor/implementation_C11.tex is excluded (council edits nothing; the author would add it);
better a standalone rigor/moebius_covariance_c11.tex, cited by a new corollary in rigor/network_second_order.tex
after thm:T6.

(iii) Rests on: c11-extension-implementer, implementer-hypotheses ((H1)-(H3) for all nets), thm-b-universality
(standing hypotheses S2, HD, BW, RS), corner-calculus (lem:frame, lem:canon: the state depends only on the corner
measure), network-law-c-linear.

(iv) Obstacle, concretely. For smooth f, U(h) T(f) U(h)^* = T(h_* f) + (Schwarzian term) holds on the finite-energy
core; for Moebius h the Schwarzian term vanishes. The extension to ||f||_{3/2} < inf must pass through the strong
resolvent limit used in Implementation_C11 (CW05 Prop. 4.5, Lemma 4.6: smooth support-preserving approximants
f_k -> f with e^{iT(f_k)} -> e^{iT(f)} strongly). Two things must be checked, each a step: (a) h_* f_k is again an
admissible approximating sequence for h_* f in the 3/2-norm (h is smooth on S^1, so composition and the
multiplier (h')^{-1} are bounded on H^{3/2}; needs a cited Sobolev-multiplier lemma with locator); (b) the field
h_* g of the conjugated map has its corner at h(p), possibly outside the line chart of I when h moves the point at
infinity; thm:main is stated for the standard geometry, so the transported geometry must be re-identified with it
via the frame lemma. The risk point is (b) for the protocols whose Moebius factor does not preserve I. An
alternative route that may avoid group-level statements: a left compression of I is the image of a right
compression under the reflection implemented by the modular conjugation J (Bisognano-Wichmann, hypothesis BW);
whether J-conjugation of thm:main's implementer is again of thm:main's form is a separate, also unchecked, step.

(v) Payoff: extends paper 2's network corollary from L->R chains to all VWZ protocols at general c (including the
c < 1 Virasoro nets); removes the integer-c restriction of paragraph (b). Modest for papers 1/2 (a remark today),
substantial for a paper 3 (one theorem covering every ordering).

(vi) Difficulty: medium. Reason: no new analysis beyond Implementation_C11's approximation scheme seems needed, but
two hypotheses (Sobolev multiplier stability of the approximants; geometry of the transported corner) must be
checked from the PDFs (CW05, CDIT), not from memory; risk that (b) needs the D^sigma group extension, which is open
for general c (CDIT Introduction, quoted at l. 828), in which case the step fails for a reason that is itself a
known open problem and the direction should be dropped.

## 3. Candidate D3: theta as a Wiener-Hopf constant
Cards: `theta-modular-wiener-hopf` [open, review passed REF-P5-4], `compression-not-optimal-exact-fidelity`
[numerical], `exact-fidelity-optimality-open` [numerical], `tangent-h1/h2/h3` [conjectural], `uhlmann-upper-half-proved`
[proved].

Observation that sets the priority. By card compression-not-optimal-exact-fidelity, E_rec <= (1 - theta_fr) f2 z^2
(1+o(1)) is proved, but the conclusion "the compression is beaten in exact fidelity" needs theta_fr > 0, and that is
NUMERICAL: theta_fr > 0 iff R_a != 0, and R_a != 0 is recorded only as "numerically >= 0.0143"
(rigor/exact_fidelity_upper_half.tex l. 839). So the cheapest high-value target is not the closed form but a
CERTIFIED POSITIVE LOWER BOUND on theta_fr.

(i) First statement (two stages).
Stage A (certify non-optimality): theta_fr >= theta_0 for an explicit theta_0 > 0 (target theta_0 = 0.01 from the
single direction G = R_a; stretch theta_0 = 0.3 from an explicit finite-rank trial G built from a coarse F3 optimiser),
computed in python-flint arb with the Fourier-space form g_Q([Q,X]) = (1/4) int int K(p,p') |X^(p,p')|^2 of Prop. 6.2
and every truncation of the (p,p') integral bounded analytically (K <= 1; tails of X^ from the explicit trial kernel).
Since theta_fr is a SUPREMUM over finite-rank G, any one admissible G gives a valid lower bound: the direction is right
for certification (direction ledger: trial G -> lower bound on theta_fr -> upper bound on kappa_opt = 1 - theta_fr).
Stage B (structure): an upper bound theta <= theta_1 < 1, i.e. a dual/coercivity bound
g_Q([Q, d + G]) >= (1 - theta_1) g_Q([Q, d]) for every bounded anti-self-adjoint G supported in D. This is the
"theta < 1 is NOT proved" item of the card and needs a Wiener-Hopf factorisation of the symbol K restricted to the
quadrant y, y' > 0.

(ii) Home: numerics/optimality_all/theta_certified.py (+ .out), and a short rigor/theta_certified_lower_bound.tex
stating the bound and its error budget; Stage B in rigor/exact_optimum_tangent_problem.tex (new section, author only).

(iii) Rests on: uhlmann-upper-half-proved, compression-not-optimal-exact-fidelity (Thm 7.3 and Rem 7.4(i),(ii)),
theta-modular-wiener-hopf (Lemma 6.1, Prop 6.2 kernel K), const-f2.

(iv) Obstacles. Stage A: the trial G must be admissible (finite rank, anti-self-adjoint, supported in D) in the frame
in which Thm 7.3 is stated; Prop 6.2's modular frame is equivalent only via the half-density push-forward, and the
transfer of an explicit finite-rank G between frames must be a written step. The integrand of g_Q involves
[Q, d + G] with d unbounded at y -> +inf (w(y) ~ -e^y), so the ratio's numerator and denominator must be computed
for the same regularisation and the regularisation must cancel analytically, not numerically (AGENTS.md §5 regulator
rule; F3 found a bulk h^0.77 convergence, so a naive mesh will not certify more than one digit). Stage B: K is not a
product kernel and depends on p+p' as well as p-p', so the scalar Wiener-Hopf method does not apply directly; a
genuinely two-variable (quarter-plane) problem, for which no general factorisation exists.

(v) Payoff: Stage A turns "the compression is not optimal in exact fidelity" from numerical into proved, which is the
main optimality claim of the programme and would go into paper 1 or paper 2 as a theorem instead of a remark. Stage B
is the theta < 1 statement; a closed form would be a paper-3 result but is the least likely.

(vi) Difficulty: Stage A low-medium (all formulas exist; the work is error control and the frame transfer; risk:
the analytic cancellation of the endpoint divergence). Stage B high (quarter-plane Wiener-Hopf with a non-separable
symbol; no route is written down anywhere in the KB). A closed form for theta: very high, and per AGENTS.md §3 no
candidate may be fitted (three candidates already excluded, card theta-modular-wiener-hopf).

## 4. Candidate D4: s2 = c/12 / Kubo-Mori gauge lemma
Cards: `conj-s2` [conjectural], `const-gkm-general-nets` [conjectural], `km-gauge-lemma-refuted` [refuted],
`km-exact-identity` [proved], `const-gb` [proved: one-particle g_KM = r/6 for the free fermion].

State of play (from the cards only). The gauge lemma by restriction to A(K) is refuted (inf over admissible gauges is
(11 + 5 sqrt5) c/12 = 11.09 x c/6, rigor/kubo_mori_gauge_lemma.tex eq:mainvalue). The bracket
0.034 c <= liminf s^-2 D <= limsup <= 0.924 c is conditional at both ends (Gaps RK1, RK2). c/12 is supported only
numerically (free fermion 0.0837(5), boson 0.083(2)); c/6 for g_KM of general nets exists only as an analytically
continued value (universality_normalization.tex l. 301-302, "used here formally").

(i) First statement: do the free fermion first, where no gauge question arises. Claim (S2-FF): for the r-component
free chiral fermion and the zero-collar recovery curve, lim_{s->0} s^-2 D(omega_I || omega_I o Ad U_s) = r/12, where
D is Araki's relative entropy on A(I). Route: for two quasi-free CAR states with symbols Q, Q' (0 < Q, Q' < 1 on the
one-particle space of I) Araki's relative entropy has a one-particle trace formula in Q, Q' (to be taken from a source
read from the PDF, with locator; not from memory); the restricted states depend only on the compressed symbols, so
the gauge freedom of U_s outside A(I) drops out. Expand to second order in s and identify the coefficient with half the
one-particle Kubo-Mori form of the compression direction, = (1/2)(r/6) by const-gb. This would make 0.0837(5) a
theorem for one model and turn conj-s2 into "proved for the free fermion, conjectural for general c".

(ii) Home: rigor/kubo_mori_free_fermion.tex; a numerical check of the second-order coefficient at small s against the
existing fermion numerics (the 0.0837(5) run behind conj-s2) is already available and must be cited, not redone.

(iii) Rests on: const-gb (g_KM = r/6), petz-zero-collar-channel (the recovered state is quasi-free with an explicit
symbol), quasi-free-fidelity-formula (the analogous fidelity formula, Note 5, as a template), km-exact-identity.

(iv) Obstacles. (a) The one-particle relative-entropy formula involves log Q and log(1-Q), which are unbounded on the
type III one-particle space (Q has spectrum accumulating at 0 and 1); the second-order expansion is an interchange
of a limit s->0 with a trace of an unbounded functional calculus and needs a dominating bound (a Hilbert-Schmidt bound
on the perturbation of the symbol in the norm weighted by the Kubo-Mori kernel; the HS bounds of uhlmann_upper_bound.tex
on P_-W_sP_+ are the natural input). (b) Whether the limit equals one half of the ONE-PARTICLE g_KM, or one half of the
second-quantised one, depends on the CAR doubling convention; the convention must be fixed against const-gb and the
cross-ratio-conventions card. (c) For general nets (the actual conj-s2), the refutation shows the restriction route
is closed; the card's next proposes a renormalised/collar route modulo the commutant orbit, for which no argument
exists in the repository. I rate general-c as a separate, much harder direction and recommend not starting it before
(S2-FF) is settled.

(v) Payoff: paper 2 currently states s2 = c/12 as a conjecture with a conditional bracket; (S2-FF) gives the first
proved value of s2 for any model, and the ratio s2/f2 = pi^2 (consistent on the lattice, card conj-s2) would become a
theorem for the free fermion. Moderate for paper 2, natural material for paper 1's relative-entropy section.

(vi) Difficulty: (S2-FF) medium (a one-particle relative-entropy formula for quasi-free CAR states is expected in the literature but NOT OBTAINED in this memo; refs/ must be searched first; the work is the trace-class interchange
and the convention). General-c s2 = c/12: high; the obvious route is refuted, and the Araki perturbation sources
(Gap RK2) are NOT OBTAINED per the card, so even the existing bracket is conditional.

## 5. Candidate D5: sectors-o11
Cards: `sectors-o11` [open; Statement "Deferred throughout Phases 1-3", next: "sector-dependent Markov defect for the free
fermion; write the half-page collar-Gaussianity lemma"]; cross-project links haag_s3:index-obstruction --informs-->
sectors-o11 and sector-defect-template (haag_s3:exact-hd-fails; quantities: Pimsner-Popa constant d^-2, JKL index d^2,
witness x0 = Rbar Rbar^*), both reviewed as "informs" (a research suggestion, not a consequence);
haag-duality-hypothesis link (thm-b-universality assumes Haag duality, which haag_s3:approx-hd-fails shows can fail
for charged lattice states). Note 8 sec:O11 (open_problems_plan.tex l. 304-306) rates O11 "low-med" difficulty.

(i) First statements, in increasing order.
(O11a, half page) Collar Gaussianity: for the r-component free fermion, a split inclusion with collar eps > 0 and a
quasi-free reference state that is a product across the split, the Petz map of the collar-regularised problem is a
quasi-free (Gaussian) channel, with an explicit one-particle map. Note 8 calls this elementary; it is still not written.
(O11b, first real sector statement) For the complex free fermion (r = 2 real components, c = 1) and the U(1) gauge
automorphism rho_alpha implemented by multiplication with e^{i alpha(x)}, alpha smooth, localised in a bounded K, with
alpha(+inf) - alpha(-inf) = 2 pi q, compute Phi_q(zeta) := -log F for the zero-collar recovery of the state
omega o rho_alpha restricted to A(I), and decide whether lim Phi_q/zeta^2 depends on q, on alpha, or on the position of
K relative to the corner. The states are quasi-free (rho_alpha is a Bogoliubov automorphism), so Note 5's fidelity
formula (card quasi-free-fidelity-formula) applies to the one-particle symbols.

(ii) Home: rigor/collar_gaussianity.tex (O11a); rigor/sector_markov_defect_free_fermion.tex and
numerics/sectors/u1_sector_defect.py (O11b).

(iii) Rests on: petz-zero-collar-channel, quasi-free-fidelity-formula, thm-a-quadratic-law (vacuum value as reference),
longo-xu-cmi (the CMI side, proved for the free fermion net, its finite-index subnets and extensions).

(iv) Obstacles. O11a: none mathematical; a bookkeeping item (Note 8 says O3 relies on it, so a gap sits under O3's
collar family as long as it is unwritten; C3's seat should confirm whether any proved card depends on the collar
family). O11b: (a) the U(1) automorphisms of the free fermion are inner on A(I) when K is inside I, so the
interesting case is K straddling an endpoint or the corner; the geometry must be chosen so that the state is not
unitarily equivalent to the vacuum on A(I) by a unitary of A(I) (otherwise Phi is trivially that of the vacuum
up to a recovery-channel conjugation, which itself needs a lemma); (b) the haag_s3 index lesson concerns sectors with
d > 1; U(1) sectors have d = 1, so O11b tests state dependence, not the index; a d > 1 sector needs a non-quasi-free
model (e.g. the Ising subnet of the real fermion, card longo-xu-cmi's finite-index subnets) and leaves the Gaussian
toolbox. (c) Theorem B assumes Haag duality in the vacuum sector; any extension to a sector representation must
re-check it there.

(v) Payoff: O11a removes an unwritten lemma under O3 (low effort, high hygiene value). O11b is a natural section for
a paper 3 ("state dependence of the Markov defect"); a d-dependent result (log d or d^-2 appearing in the defect) would
be a genuinely new link to the haag_s3 project, but nothing on any card supports it yet.

(vi) Difficulty: O11a low (a page of Lamport proof). O11b low-medium for U(1) (all tools exist; risk: a trivial
answer by inner equivalence, see (a)). d > 1 sectors: high (outside the quasi-free class; no fidelity formula on file).

## 6. Candidate D6: index zero at large s
Cards: `group-index-zero-large-s` [conjectural; "no document contains an argument"], `pushforward-blocks-equal-singular-values`
[heuristic]. `kb -p cft_cmi impact` on EITHER card lists four PROVED cards resting on it: rate-of-remainder (directly),
petz-not-optimal, network-global-bound-coincident, network-upper-uniform-two-corners (indirectly). This is the
"proved card resting on a conjectural/heuristic card" pattern of the council brief; whether each use lies outside the
proved range is C1's question. For directions it means: this is the item whose closure protects the most proved cards
per page of proof.

(i) First statements (two lemmas).
(L1, the push-forward case) For every admissible field chi (rate_of_remainder.tex Def. 2.1) and every real s,
P_- W~_s P_+ and P_+ W~_s P_- have the same singular values with multiplicities. Route already named on the card:
W~_s commutes with complex conjugation C (W_phi is a real operator, PA eq:pushforward) and C P_+ C = P_- (PA eq:hardy),
so P_+ W~_s P_- = C (P_- W~_s P_+) C with C antiunitary, and an antiunitary conjugation preserves singular values with
multiplicities. Each of the two facts must be a step with its locator in PA (the paper's PDF, not memory), and the
last implication a step of its own (|C X C| = C |X| C for antiunitary C).
(L2, the general group case) For U_s = e^{sK}, K^* = -K, [P_-, K] in S_2: ind(P_+ U_s P_+ |_{P_+H}) = 0 for every real s.
Route on the card: s -> U_s^* P_+ U_s - P_+ is S_2-continuous (rate_of_remainder.tex Lemma 6.1 <1>2), so the index
of the pair of projections (P_+, U_s^* P_+ U_s) is defined for all s and locally constant, hence equal to its value 0
at s = 0; and that pair index equals ind(P_+ U_s P_+) up to sign.

(ii) Home: a new correction item in rigor/rate_of_remainder.tex (the card's next: replacing the reasons at Thm 2.3
<1>4, l. 168-171, Lemma 6.1 <1>1/<1>4, l. 828-846, Prop. 6.2 <1>3, l. 871-874, Cor. 2.9 / C3, l. 1078-1079) and the
mirrored item in rigor/exact_fidelity_upper_half.tex (its C3, l. 1190-1193). Author only.

(iii) Rests on: nothing on the KB beyond rate-of-remainder's own Lemma 6.1 and the PA paper (Note 4's source).

(iv) Obstacles, concretely. L1: none beyond writing; the only risk is that W~_s is "real" in one convention of the
one-particle space (real vs complex fermion, r components) and the conjugation C must be the one under which P_+ and
P_- are exchanged in the SAME convention (cross-ratio-conventions card; PA Correction C1 is cited for exactly this).
L2: U_s is only strongly continuous (K unbounded), so the index of P_+ U_s P_+ cannot be followed by norm
continuity of s -> U_s; the argument must go through the pair index, whose invariance under S_2-continuous (indeed
norm-continuous with compact difference) deformation needs a cited theorem on the index of a pair of projections with
exact statement and locator (source to be obtained into refs/; NOT OBTAINED by this memo). Second step: the identity
between the pair index and ind(P_+ U_s P_+), including the sign, also from that source.

(v) Payoff: removes the conjectural/heuristic foundations under four proved cards, two of which (petz-not-optimal,
rate-of-remainder) are paper-1 statements. No new headline, but it is the cheapest way to make paper 1's remainder
section unconditional, and L2 also covers the product family W~_s e^{ish'} of Cor. 2.9.

(vi) Difficulty: L1 low (a page; argument complete on the card). L2 low-medium (a standard-looking Fredholm argument,
but the source must be obtained and its hypotheses checked one by one; risk only in the sign/identification step).

## 7. Candidate D7: certification of the D-hat quadrature
Cards: `dhat-quadrature-certification` [open], `certified-numerics` [numerical]. The certified 60-digit enclosures
(width 0.71% to 1.01%) refer to the COMPRESSED problem; two steps are uncertified: the 2-D quadrature that produces
the defect matrix D-hat (numerics/defect_matrix.py) and the box truncation at kappa_max. A cancellation defect in
defect_matrix.run (beta_I via L - x) is recorded (2.5e-8 of max|D| at (120, 45); NaN in a shifted frame at Lam = 120);
the card's next (1) is a user decision pending since 2026-10-05.

(i) First statements. (Q1, compute) Rerun the (Lam, kappa_max) = (120, 45) line value with the cancellation-free beta_I
of corner_kernel.py box_corner; success criterion fixed before the run: agreement with the recorded 0.0084111 to the
digits stable across the two finest resolutions. (Q2, certify) An arb enclosure of every entry of D-hat on the box
frame at (60, 30): the 2-D integrand evaluated in ball arithmetic with a rigorous quadrature error bound (e.g. a
Gauss-Legendre bound from an analytic continuation strip, whose width and sup bound are derived in the document),
replacing the floating-point D-hat in the existing certified pipeline. (Q3, prove) An analytic bound for the
box-cutoff tail beyond kappa_max; the card names the asymptotics 0.0641 zeta^2/kappa_max^2, which is a fit/asymptotic
and must be turned into an inequality with explicit constants.

(ii) Home: numerics/defect_matrix_arb.py (+ .out) and a new section of rigor/certified_numerics.tex (author only),
or a sibling rigor/certified_defect_matrix.tex.

(iii) Rests on: certified-numerics, tail-bound (the lower half Phi_W <= Phi^box), the existing exact-kernel paths
(numerics/fidelity_hp.py, numerics/line_so.py) as the second method for Q1.

(iv) Obstacles. Q2: the defect kernel has an integrable singularity on the diagonal and at the corner; a certified
2-D quadrature needs either subtraction of the singular part in closed form or a splitting with an analytic bound on
each piece; the integrand's analyticity strip must be established, not assumed. Q3: the tail is a sum over modes beyond
kappa_max whose individual size is known only asymptotically; a rigorous tail bound needs a monotonicity or
majorant argument for the box eigen-data. Independent of both: Q1 is a decision the user has left pending, not a
research obstacle.

(v) Payoff: completes the "certified numerics" claim of paper 1 (box values with rigorous error bars including the
quadrature); Theorem A itself is analytic (thm-a-quadratic-law, refereed) and does not need it, so the payoff is
reputational and for the tables, not for a theorem. Low for paper 2 and a paper 3.

(vi) Difficulty: Q1 trivial (minutes; script exists). Q2 medium (careful but routine interval quadrature; risk in the
singular parts). Q3 medium-high (needs analytic control of the box spectrum). Value per effort: Q1 high, Q2/Q3 low
unless a paper statement relies on the certified enclosure being complete (C6 should check paper 1's wording).

## 8. Candidate D8: Longo-Xu Remark 4.3 beyond free fermions (paper 3 on networks: assessed in section 9 as a packaging of D1, D2, D6)
Cards: `longo-xu-cmi-general-c` [conjectural], `longo-xu-cmi` [proved: free fermion A_r, its finite-index subnets and
the finite-index extensions]. Source read for this memo: refs/LongoXu_1712.07283.pdf (pdftotext). Verbatim, Remark 4.3:
"We conjecture that the above theorem is true for any rational conformal net, where r is replaced by the central
charge." "The above theorem" is Th. 4.2, whose hypothesis is "Assume that a subnet B subset A_r has finite index".
The mechanism of the finite-index case (same PDF, the paragraph before Th. 4.2): F_1 = F_{A_r} - F_B is
S(omega, omega o E) for the conditional expectation E, bounded by ln lambda^-2 through the Pimsner-Popa inequality
E(x) >= lambda^-2 x, and its limit ln lambda^-1 cancels in the combination that gives the CMI.

(i) First statement. The smallest step outside the proved class that the Longo-Xu mechanism does not cover is
INFINITE index inside A_r. Candidate: B = the U(1)-gauge fixed-point subnet of the complex fermion A_2 (c = 1).
Statement to decide: for adjacent intervals, I_B(A:C|B) = (1/6) log(1+z), i.e. the same as for A_2. Equivalent
formulation in Longo-Xu's notation: the combination of F_1(A, B) = F_{A_2} - F_B entering the CMI vanishes although
F_1 itself may be unbounded (no Pimsner-Popa constant). A first computable instance: the free-boson lattice/continuum
numerics behind card boson-check (c = 1), if their geometry allows the adjacent-interval CMI, give a numerical
test; this is a numerical datum only, never evidence for the general conjecture.

(ii) Home: rigor/longo_xu_infinite_index.tex; numerics/longo_xu/u1_cmi.py.

(iii) Rests on: longo-xu-cmi (the A_r value), cmi-markov-defect-interpretation, the Longo-Xu PDF.

(iv) Obstacle, concretely: the only argument on file (Pimsner-Popa) needs finite index; for a compact-group fixed
point subnet E exists (averaging over U(1)) but S(omega, omega o E) restricted to two-interval algebras need not be
bounded, and the cancellation in the CMI combination then needs a uniform control of S(omega, omega o E) as the gap
eps -> 0 that is not in the paper. For rational nets not embedded in any A_r (most of the c < 1 minimal models and
WZW nets beyond small level), no free-fermion handle exists at all, and the project's tools (quasi-free fidelity,
Theorem A/B) are second-order-in-z statements about recovery, whereas the CMI is (c/6) z at first order: Theorem B
(card thm-b-universality, f2 = c/(12 pi^2) for every net) does NOT imply Remark 4.3 and gives at best a consistency
check. A recovery-to-CMI inequality of Fawzi-Renner type in type III would relate them only as a one-sided bound of
the wrong order in z; no card holds such an inequality.

(v) Payoff: a proof for any rational net outside the free-fermion class would be a significant operator-algebra result
(a paper of its own), and would upgrade paper 1's Longo-Xu section from a scope remark (paper1 rem:LX-scope) to a
general statement. The infinite-index U(1) case alone would be a useful lemma but is not "rational" in Longo-Xu's
sense of the conjecture, so it does not decide Remark 4.3.

(vi) Difficulty: very high for the conjecture (an external open problem; the project's machinery has little leverage
on a first-order-in-z quantity). Medium-high for the U(1) fixed-point case. Recommendation: do not invest beyond a
literature check (refs/ search for later work on Remark 4.3, from PDFs only) and a scope sentence in the papers.

## 9. Ranking and justification
| rank | direction | first deliverable | difficulty | payoff |
|---|---|---|---|---|
| 1 | D6 index zero (L1 push-forward, L2 group) | correction item in rate_of_remainder.tex | low / low-medium | protects 4 proved cards (paper 1) |
| 2 | D3 Stage A: certified theta_fr >= theta_0 > 0 | numerics/optimality_all/theta_certified.py + short tex | low-medium | "compression beaten in exact fidelity" numerical -> proved |
| 3 | D1 (U1) uniform lower bound, M = 2 | numerical sup-over-Delta test (K4 script), then lemma in sec:T5 | test low; lemma medium-high | lim Phi(2)/Phi(1) = 2; headline of paper 3 |
| 4 | D4 (S2-FF) s2 = r/12 for the free fermion | rigor/kubo_mori_free_fermion.tex | medium | first proved s2 value; paper 2 |
| 5 | D2 Moebius covariance of the C^{1,1} implementer | rigor/moebius_covariance_c11.tex | medium | network law for all orders at general c |
| 6 | D7 Q1 rerun (decision), Q2/Q3 certification | rerun; defect_matrix_arb.py | trivial / medium / medium-high | tables of paper 1 only |
| 7 | D5 O11a collar lemma, O11b U(1) sectors | collar_gaussianity.tex; u1_sector_defect.py | low / low-medium | hygiene under O3; paper-3 section |
| 8 | D8 Longo-Xu Remark 4.3 beyond A_r | literature check from PDFs | very high | external open problem |

Justification. The ranking orders by (protection of claims already made) x (probability of success) / effort. D6
comes first because `kb impact` shows four PROVED cards, among them rate-of-remainder and petz-not-optimal (paper 1)
and both Phase 6 network theorems, resting on a conjectural and a heuristic card whose arguments are short and already
sketched on the cards; it is a repair of foundations, not new mathematics, and nothing else on the list is safe
while it is open. D3 Stage A is second for the same reason one level up: the programme's main optimality statement
is "numerical" only because theta_fr > 0 is numerical (R_a != 0 "numerically >= 0.0143"); one certified trial
direction suffices, the direction of the bound is the right one, and the frame and formulas exist. D1 is the most
valuable NEW result (it decides the VWZ limit), but its proof needs a rate in a compression step that currently has
none; its numerical test is cheap and should run first, because a negative outcome answers the question. D4 trades
the refuted general-c route for a model where the gauge problem does not arise; it is the realistic route to a
proved s2. D2 is well posed and probably within reach of Implementation_C11's approximation scheme, but its payoff
(Protocol 3 at general c) is narrower. D7 Q1 is a pending user decision, not research; Q2/Q3 certify tables no
theorem depends on (`kb impact certified-numerics`: 0). D5's collar lemma is half a page and should be written as
hygiene whenever convenient; the sector physics proper (d > 1) leaves the Gaussian toolbox. D8 is an external open
conjecture on which the project's second-order machinery has no first-order leverage.

Paper 3 on networks (assessed here, not as a separate direction). The Phase 6 cards (corner-calculus,
network-law-free-fermion, corner-kernel-closed-form, network-law-c-linear, network-upper-uniform-two-corners,
vwz-protocol-ordering [conjectural]) already carry the material of a paper. Prerequisites before drafting: (a) the
outcome of seat C5's second referee pass on these cards; (b) D6, since two network theorems rest on the index-zero
cards; (c) the D1 numerical test, which decides whether the paper can state lim Phi(2)/Phi(1) = 2 as a target or
must present (U1) as open. D2 is optional for paper 3 (it widens thm:T6 from canonical to all orders). Recommended:
draft paper 3 after (a)-(c), with D1's lemma and D2 as stated open problems if unproved.

## 10. NOT DONE
- No direction was worked on mathematically; every "first statement" is an UNREFEREED target.
- Sources named as needed but NOT OBTAINED here: a reference for the index of a pair of projections (D6 L2); a
  one-particle relative-entropy formula for quasi-free CAR states (D4); CW05/CDIT for the Sobolev-multiplier step
  (D2); later literature on Longo-Xu Remark 4.3 (D8). The Longo-Xu PDF was read (Th. 4.2, Remark 4.3).
- Not checked: whether the boson-check numerics can supply an adjacent-interval CMI (D8); whether any proved card
  depends on O3's collar family (D5 O11a; for seat C3); the lattice small-eta sweep of network-law-c-linear's next (3)
  was not assessed as a separate direction (it is a numerical counterpart of D1).
- The pdftotext extraction of the Longo-Xu PDF has no page numbers in this memo; page locators remain to be added.
