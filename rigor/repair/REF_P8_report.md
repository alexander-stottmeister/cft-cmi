# REF-P8 report — Theorem B stated unconditionally in paper 2 (2026-11-19)
Referee REF-P8 (Opus), adversarial. Object: card paper2-status; patch rigor/repair/ORCH_patch_7.json.

## 1. thm:B hypotheses vs ss:standing + thm:impl; strength vs cards
STANDS. thm:B (paper2/sec_universality.tex:295-308) assumes a net as in ss:standing (axioms (1)-(10) of CDIT, separable, c>0, standing facts (HD),(BW),(RS); sec_setting.tex:2-29) and U_s = e^{is closure T(g_tot)}. thm:impl (sec_implementation.tex:166-173) has exactly these hypotheses ("satisfying the axioms of ss:standing", c>0, separable) and the same U_s (def:Us, l.112). thm:H1 (iii) and thm:H23 hold "for every s", so (H1)-(H3),(H2') hold for both signs of s, which the two-sided o(s^2) of eq:B needs. Proof chain: prop:lower uses (H1),(H3),(RS); prop:upper (H1),(H2),(RS); thm:linear (BW),(H2'); thm:value a fact about the fermion net (rem:graded), not a hypothesis on the net. All available.
Against the cards: thm-b-universality (refereed; (H1)-(H3) assumed, two-sided expansion, same g_B) composed with implementer-hypotheses (refereed; "(H1)-(H3) hold for all diffeomorphism-covariant nets", (H1) in (C7) form) gives exactly the new statement; the eq:H1loc clause of (H1) concerns smooth phi only and is the CDIT axiom plus (HD) (sec_setting.tex:118-121). No sign or range restriction of s and no extension independence is claimed (the latter, s>=0 only, is lem:ext, which thm:B does not use, sec_setting.tex:189). Not stronger than the cards.
MINOR (pre-existing, not in the patch): eq:chi defines g_tot at L=1 (sec_setting.tex:62) while thm:B keeps a general L; app_conventions.tex:58 gives the L-form -x^2/L. Harmless by dilation covariance, but the U_s of thm:B for L != 1 is not literally the one of def:ktilde.
## 2. "No hypothesis beyond those of ss:standing is made"
STANDS. Every input of the proof (sec_universality.tex:310-317) is either in ss:standing or a theorem proved from it (thm:impl, thm:linear, thm:value, prop:lower/upper). The sentence is true of the proof chain. The old self-contradiction (assume (H1)-(H3), then call itself unconditional; referee_paper2.md P8) is gone; the old texts of patch items 1-3 are absent from the file.
## 3. cor:tensor proof completeness
STANDS. With U = U1 (x) U2 and vacuum Omega1 (x) Omega2 named, thm:B applies to each of A1, A2, A, giving f2 = c_i/(12 pi^2) and c(A)/(12 pi^2). c(A) = c1 + c2 follows from T = T1 (x) 1 + 1 (x) T2 (generator of a tensor product of one-parameter groups, Reed-Simon VIII.33 type) and eq:TT: the cross terms of the two-point function vanish because each vacuum one-point function is 0 (sec_universality.tex:10-12). MINOR: these two one-line steps (scalar normalisation of T on the product, cross terms vanish) are left to the reader; no repair required.
## 4. Moebius-reduction wordings vs card moebius-reduction-general-nets; "reviewed internally"
FAILS (one of four). Card moebius-reduction-general-nets: (a) state equality for every real s; (b) s>=0 for every extension of class E, every real s for one explicit extension; (c) fidelity; "Not covered: s<0 for a general extension, implementers other than C11's, relative entropy". Review line: passed 2026-11-19 by REF-RR-A (after a card-only FAIL by REF-RP-1, document STANDS). "reviewed internally on 2026-11-19" is accurate in all four places.
- sec_setting.tex:46: range stated exactly as on the card. OK.
- rigor/universality_theorem_B.tex:93: "proved, review passed 2026-11-19; implementers of implementation_C11.tex, s>=0 for every extension of class E". OK (weaker than the card, which is allowed).
- main.tex:34-35 (abstract): "the reduction ... for a general net rests on an internal document, reviewed internally". No range; the formula itself is stated in the normal form only. MINOR: add the range.
- app_conventions.tex:51-52: "for the free fermion all recovery quantities depend on (a,L,s) only through the cross ratio (for a general net, the U(1) current net of sec:boson included, the reduction rests on [doc], reviewed internally on 2026-11-19)". Read with its parenthesis this asserts, for a general net and the U(1) net, that ALL recovery quantities (relative entropy included) depend only on zeta, for all s. The card covers the recovered state and the fidelity only, s>=0 for a general extension, and excludes relative entropy explicitly. Stronger than the card: FAIL. sec_boson.tex:29 and :89-100 compare the U(1) net's s2 (relative entropy) at a=1, L=2, zeta=s/3 with 1/12; that conversion of s2 is exactly what the card does not cover (relevant for the repair).
- The orchestrator note of 2026-11-19 20:59 on paper2-status says the proved range was written into "sec_setting.tex, app_conventions.tex, main.tex abstract"; only sec_setting.tex carries it.
## 5. Remaining places calling Theorem B conditional
STANDS. grep of sec_intro.tex, main.tex, sec_outlook.tex, sec_boson.tex, sec_kubo_mori.tex, app_*.tex, sec_implementation.tex for (H1)/hypothes/condition/assum/thm:B: no place calls Theorem B conditional or (H1)-(H3) its assumptions. sec_intro.tex:28-33 (informal statement, "standard axioms"), :67-68 ("unconditional ... standing assumptions"), :93 ("the hypotheses (H1)-(H3)", naming only), sec_setting.tex:97-100 ("verified for every ... net"), sec_universality.tex:43 (the propositions are conditional, correctly), sec_implementation.tex:226-230 consistent. The card's next item "sec_intro.tex:21 standing hypotheses wording": l.21 now reads "holds for every diffeomorphism covariant conformal net on S^1", consistent.
## 6. Build and card Statement against facts
STANDS. Copy of paper2/ in scratchpad REF-P8/paper2, pdflatex x3 (no bibtex: thebibliography inline): 26 pages, log has no line matching ^! or (Reference|Citation).*undefined. rigor/universality_theorem_B.tex built with -output-directory into REF-P8/rigorB: 25 pp, log clean. Card Statement: 26 pp correct; title 'Universality of the zero-collar compression error in conformal nets' = main.tex:19; P8 applied (this patch), P9 concerns the source only (referee_paper2.md:122), so "P1-P8, P10 applied" is consistent; Theorem B sentence accurate.
## Numerical recomputation
No number in a theorem statement changed; no recomputation required.
## Verdict
paper2-status: FAIL (item 4). Repair: paper2/app_conventions.tex:51-52, restrict the general-net parenthesis to the card's range ("for a general net the recovered state and the fidelity, not the relative entropy, reduce to zeta for s>=0 and every extension of class E, and for both signs for one explicit extension; rigor/moebius_reduction_general_nets.tex, reviewed internally on 2026-11-19"); state the same range in main.tex:34-35; for the U(1) net's s2 at zeta=s/3 (sec_boson.tex:29) either cite a model-specific reduction or say the conversion is not covered. Items 1-3, 5, 6 STAND; P8 itself (thm:B) is correct.

## Re-review (2026-11-19, rigor/repair/ORCH_patch_8.json)
(a) Wordings against card moebius-reduction-general-nets (state and fidelity; s>=0 for every extension of class E;
both signs for one explicit extension; relative entropy not covered):
- app_conventions.tex:51-55: "proved only for the recovered state and its fidelity, for s>=0 and every admissible
  extension ... and for both signs for one explicit extension ...; for relative entropies of a general net no such
  reduction is proved". Exactly the card's range. OK.
- main.tex:35 (abstract): "proves it for the recovered state and its fidelity when s>=0". Weaker than the card
  (omits the one-extension both-sign case), nothing false. OK.
- sec_boson.tex:29-31: fidelity and s>=0 via the Moebius reduction of ss:geom; for the relative entropy "no reduction
  is proved for this net, and zeta=s/3 there only labels this one configuration". Not stronger than the card. OK.
(b) Orchestrator note of 21:04:09 on paper2-status: describes the three replacements correctly and corrects the
  20:59 note (range previously only in sec_setting.tex). Accurate.
(c) Build: fresh copy in scratchpad REF-P8/paper2b, pdflatex x3: 26 pages, no line matching ^! or
  (Reference|Citation).*undefined.
Re-review verdict: paper2-status PASS. Item 4 now STANDS; items 1-3, 5, 6 unchanged (STAND).
