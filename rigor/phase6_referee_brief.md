# Phase 6 referee brief (referees run on Claude Opus; never Fable unless the user explicitly requires it)

Object under review (REF-P6-3, 2026-09-16): track G1a's document rigor/network_corner_calculus.tex (38 pp, Lamport) with its
scripts rigor/g1a_calculus.py/.out (33 checks) and rigor/g1a_separation.py/.out (10 checks), and the eight pending KB cards
(kb -p cft_cmi review --all --packet ...): corner-calculus [proved], frame-strength-amplification, vacuum-rigidity-exact-recovery,
corner-separation-constraint, sequential-recovery-bound-type-iii, protocol-corner-data-n4-n5 [all proved], and the notes on
network-second-order-law and phase6-plan. Plan and conventions: rigor/phase6_brief.md; earlier plan referee: rigor/referee_phase6_plan.md.

Adversarial stance; the burden of proof is on the document. Write rigor/referee_network_corner_calculus.tex (Lamport, one verdict
per theorem: STANDS / STANDS WITH REPAIR / FAILS, with the exact step and the counter-argument), then the card verdicts.
Checklist:
 1. Hypothesis (H) and its variants: the document corrects the brief ("single-interval conditioning implies (H)" is false when the
    starting block is one interval, Ex. 5.6, the earlier corner is swallowed). Is the corrected condition (single-interval
    conditioning AND a starting block of >= 2 chain intervals) sufficient for (H)? Necessary? Test with random protocols.
 2. Thm 5.2 (unconditional rule S(Phi) = -2 sum sigma_m G_m'(x_m) delta_{x_m}) and Thm 5.3 (under (H)): every composition step,
    the pullback of a delta, the derivative-1 claim at fixed corners, the abelian parabolic subgroup. Recompute REF-P6-0's
    counterexample from Thm 5.2 independently.
 3. Lem 3.3/3.4: the exact first-order field and the (-1)-density law -- algebra, and the sign conventions (compression toward p
    from either side has the same sign of [h''/h']).
 4. Lem 4.2-4.5 (Schwarzian of C^1 piecewise-Moebius maps, no square term, composition rule, same Schwarzian => differ by a
    Moebius map): domains, regularity assumed, distributional identities.
 5. Thm 6.3 (composite normal; the state depends only on S(Phi)): is the per-step use of Note 4 Thm 7.1 legitimate for a step
    applied to a NON-vacuum input state (the previously recovered state)? The Heisenberg composite is state-independent, but check
    that the maps compose in the right order and land in the right algebras; the one-particle identity W_{k1} W_{k2} = W_{k1 o k2}.
 6. Thm 7.3 (rigidity: exact recovery iff Phi is Moebius; never for a non-empty protocol): the two-point-function argument
    (Phi'(x)Phi'(y))^{1/2}/(Phi(x)-Phi(y)) = 1/(x-y) => Phi Moebius; is the pulled-back symbol really E_I V^* Q V E_I with the
    off-diagonal blocks as claimed; does 'never' need the parabolic parameters strictly positive (s >= lambda > 0)?
 7. Thm 8.5 (Protocol 3 = Phi_A(zeta_eff), s' >= 2 lambda'): recompute sigma_1, sigma_2, s', lambda'; is s' >= 2 lambda' (the
    document's claim) or only >= lambda'? Both orders literally the same map: verify numerically.
 8. Prop 9.1 / Tables 1-3 (the corner measure depends only on the starting block; 2^{n-2} protocols -> n-1 classes for n = 4, 5):
    enumerate independently with a script; check the table entries.
 9. Lem 10.1 (amplification), Lem 10.3 (NEW identity zeta_k = sinh(D_{k+1}/2)/(sinh(D_k/2) sinh((D_k+D_{k+1})/2)) with the
    modular lengths D_k) and the consequence e^{Delta_k} < 1 + 2/zeta_k: derive independently.
10. Thm 11.1 (all-weak separation e^{Delta_k} >= 2/eps via the recursion gamma_j <= zeta_j (1 + gamma_{j+1}/2), fixed point
    2 eps/(2 - eps)): every inequality direction; the boundary terms (last corner); sharpness claim vs the numerical minimum
    (ref_p6_0_separation.out: 20.05, 66.68, 200.0, 666.7); the 1/eps version for admissible s_k >= lambda_k.
11. Thm 12.5 / Cor 12.6 (Bures-angle sequential bound under Hypothesis (U)): refs/Uhlmann76.pdf and refs/AlbertiUhlmann02 ARE on
    disk -- can (U) be discharged with an exact locator (then it is a repair, not a failure)? Check monotonicity of the fidelity
    under normal UCP maps for normal states on von Neumann algebras (FHSW20 or Alberti-Uhlmann) with locators; the triangle
    inequality of the Bures angle for normal states.
12. Prop 13.1 (twirled composite is a mixture; Phi^tw <= average): direction of the concavity inequality.
13. Cited results: every citedbox has (i) exact statement, (ii) locator, (iii) screenshot in rigor/shots/, (iv) use, (v) verdict.
14. Scripts: rerun rigor/g1a_calculus.py and rigor/g1a_separation.py; do they test what the text claims?
15. Cards: statement vs document (theorem numbers, hypotheses, constants), weakest supported status, evidence pointers resolve,
    contradictions with existing cards (corner-calculus vs the brief's W1; network-second-order-law's 'bound NOT proved' clause
    vs Thm 11.1). Use kb -p cft_cmi verdict ID pass|fail --note "..." with KB_ACTOR=REF-P6-3. Never edit the documents under
    review; never edit existing referee notes on cards.
Output: verdict per theorem; list of required repairs [BREAK|GAP|MINOR] with exact locators; card verdicts; <= 450 words back.
