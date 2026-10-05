# Referee report REF-P6-7: Phase 6 knowledge-base cards (review of 2026-10-05)

Referee: REF-P6-7 (Opus). Packet: scratchpad/kb_review_packet.md (8 cards).
Stance: adversarial; the burden of proof is on the card.

## 0. Method and environment
- Read AGENTS.md, kb/REVIEW_BRIEF.md, the packet; `kb show` and `kb history` of every card live (all eight still
  `review: pending`, no verdict or note by another referee after the orchestrator's edits of 2026-10-05 21:34-21:36;
  the last content event on network-second-order-law is G2's note of 21:38:54, which is in the packet).
- Every cited card checked live: all 31 ids named by the six cft_cmi cards exist and show `review: passed`
  (REF-P6-3/3b/4/4b/5/5b/6/6b, REF-DEP-*, REF-CARD-*); `kb -p cft_cmi deps --check` gives no warning for any packet card.
- Every `doc:` label grepped: thm:T1-T6, cor:law, cor:W3W4, cor:vwz, lem:nogroup, sec:T4, sec:T5
  (rigor/network_second_order.tex); thm:corner, thm:state, thm:sep, thm:prot3, prop:prot2, prop:1B1A, def:LR, lem:LRdata
  (rigor/network_corner_calculus.tex): each exactly once. PDFs: network_corner_calculus 42 pp, network_second_order 29 pp
  (pymupdf page count; network_second_order.log has no `^!` or undefined-reference line).
- Script rigor/ref_p6_7_checks.py -> rigor/ref_p6_7_checks.out (tolerances fixed in the docstring before the run):
  (A) validation Ghat(0) = 1/(12 pi^2) by series and by direct Fourier quadrature: PASS;
  (B) the nine kernel values by three methods sharing no code with g1b_kernel.py (boxed closed form, exponential series of
      T4(cf), mpmath quadosc of int rho(q) cos(q Delta) dq): mutual agreement < 1e-38; card values within 4.7e-8 of the
      closed form (rounding of the printed 7 decimals; tol 6e-8): PASS; T4(d) bounds hold at all nine points;
  (C) VWZ strengths, S(log 1/eta), the cor:W3W4(i) bracket, (S - X)/u for X = 0.28140 and u = 0.0045 / 0.0044 / 0.005
      = 3.05 / 3.12 / 2.75; 8 f2/c = 0.06755;
  (D) extrapolated Phi_tot/Sstep of every chain in numerics/networks/N4.out: 1.4828, 1.8171, 2.0699, 1.4610.
- Reruns (output into my files, never onto reviewed outputs): `PYTHONDONTWRITEBYTECODE=1 $PYTHON
  numerics/networks/lattice_chain.py N3 > rigor/ref_p6_7_N3.out` and `... N4 > rigor/ref_p6_7_N4.out`: both
  byte-identical to numerics/networks/N3.out and N4.out (cmp).
- VWZ text from refs/VWZ_2307.14434.pdf (pymupdf, page 48 of the PDF = journal p. 47): (5.10), the sentence after it,
  and (5.11) read verbatim (quoted in section 3).
- Transcripts ($CLAUDE_CONFIG_DIR/projects/<slug>/<session>/subagents/*.jsonl) read for the two common notes only.
- Venv: scratchpad/venv (numpy, scipy, mpmath, python-flint, pymupdf). Temporary files: scratchpad/REF-P6-7/.

## 1. cft_cmi:dhat-quadrature-certification
Verdict: **FAIL** (one unsupported and literally false sentence; How to verify does not reach the new finding).

Checked and correct (every number traced):
- 7.0e-12 at (60,30) and 2.5e-8 at (120,45) of max|D|: numerics/networks/kernel_validate.out:26-27, line (d');
  reproduced by REF-P6-5 (rigor/referee_corner_kernel.tex item 9, verdict box "Item 9 ... reproduce").
- NaN in a shifted frame at Lam = 120: REF-P6-5 item 9 (G3 named no output for it; the card cites the report, fine).
- 0.0084112 -> 0.0084111: numerics/line_so.txt:4 (`f2_line=0.0084112`); kernel_box.out:46 `[line] G/f2 = +0.99617060`
  in the (120,45) block, and 0.99617060/(12 pi^2) = 0.0084111; REF-P6-5 item 9 ("only 0.0084112 moves (to 0.0084111)").
- qfi_c2 = inf from kappa_max = 45 on: kernel_validate.out block (c) (120,45) `inf ... FAIL`; REF-P6-5 found inf also at
  (60,45), (120,60).
- fid_relent noise: numerics/results_batch3.txt:1-7 give -log F = -6.54, 0.134, 3.06, -8.50, -9.36, -8.46, -0.893
  (range -9.36 ... +3.06, either sign); numerics/results_A2.txt:1 `-logF_sub=5.679016e-07` = 5.7e-7.
- next (2): the cutoff term is PT's 0.0641 zeta^2 kappa_max,eff^-2 (rigor/certified_numerics.tex:519, 792).
- Status `open`, type `question`: weakest; `next` names files and the expected value.

Defects:
1. [GAP, the fail] "every published number of the project came from the windowed method, not from fid_relent". No
   locator, no refereed card or document says it, and as written it is false: the card's own published line value
   0.0084112 (numerics/line_so.txt:4) comes from line_so.py's line-symbol QFI, not from a windowed fidelity; the
   certified enclosures come from interval arithmetic (certified-numerics), the lattice numbers from the flint Gaussian
   pipeline. REF-P6-5 explicitly did NOT recompute the exact-kernel windowed values at Lam = 120 (referee_corner_kernel.tex
   item 9, "NOT checked: ... results_L120.txt, results_final2.txt, results_largezeta2.txt"). What is supported:
   numerics/networks/KERNEL_RESULTS.md:159-161 (fid_relent unusable; the Theorem A pipeline's method is
   numerics/fidelity_hp.py). REPAIR: "the published box-frame fidelities (numerics/results_A2.txt, ...) come from the
   windowed 30-digit method of numerics/fidelity_hp.py (KERNEL_RESULTS.md:159-161), not from fid_relent", or delete.
2. [GAP] How to verify ("rigor/certified_numerics.tex, verdict boxes") does not re-establish the FINDING the Statement
   now carries. Add: numerics/networks/kernel_validate.out:16-20 (block c) and :26-27 (line d'), kernel_box.out:46,
   numerics/line_so.txt:4, numerics/results_batch3.txt:1-7, numerics/results_A2.txt:1, rigor/referee_corner_kernel.tex
   item 9.
3. [MINOR] next (2): write kappa_max,eff (certified_numerics.tex:519), not kappa_max.

## 2. cft_cmi:multi-interval-networks
Verdict: **FAIL** (the card now asserts some fifteen results and its How to verify is "n/a"; one mis-citation; one
wrong locator in `next`).

Checked and correct: every id in the Statement and `related` exists and has passed review (section 0); corner-calculus
(H) and the general rule, Schwarzian-only dependence, the closed form of Ghat with positivity and rate 1/2, the separation
constraint, the chordal type-III bound (sequential-recovery-bound-type-iii: chordal form, no Hypothesis (U)), the
Protocol 3 identity, the lattice items (189 sites = the 6-block r = 1/2 chain, lattice-lr-chains-cross-terms), and the
OPEN list (U1 for M >= 2, U2 for M >= 3, non-canonical orders, network-form global bound with lem:nogroup, small eta,
sectors-o11) agree with the cited cards. Status `open`, type `question` right; `next` concrete.

Defects:
1. [GAP, the fail] How to verify reads "n/a". REF-P6-0 accepted that only because the card then "claims nothing"
   ("Not started"); the 2026-10-05 Statement asserts PROVED, refereed and NUMERICAL results. AGENTS.md section 2
   requires a command or file:label that re-establishes the claim. REPAIR: e.g. "kb -p cft_cmi show corner-calculus
   vacuum-rigidity-exact-recovery protocol-corner-data-n4-n5 network-law-free-fermion network-law-c-linear
   corner-kernel-closed-form corner-separation-constraint sequential-recovery-bound-type-iii
   network-upper-uniform-two-corners lattice-vwz-protocol-ratios lattice-lr-chains-cross-terms network-remainder-uniformity;
   status rigor/PHASE6_STATUS.md".
2. [MINOR, mis-citation] "strengths add at a common junction, frame-strength-amplification": that card states the
   amplification zeta^(I) = zeta_step (1 + z') and nothing about addition; addition at a common junction is the corner
   calculus (R(s1) o R(s2) = R(s1 + s2); thm:prot3 for Protocol 3; cor:law "coincident corners add their strengths").
3. [MINOR] "1 <= Phi(2)/Phi(1) <= 2 in the limit (vwz-protocol-ordering)" sits in the PROVED list but cites the
   conjectural card under review; the proved source is cor:vwz / network-upper-uniform-two-corners, and what is proved is
   1 <= liminf <= limsup <= 2 (the existence of the limit is the open question). Same for "Phi(1):Phi(3) =
   Phi_A(a/b):Phi_A(2a/b) exactly": source thm:prot3 (free fermion).
4. [MINOR, wrong locator] next (2) "rigor/implementation_C11.tex Sec. 8(b)": Sec. 8 of that document is "Corrections
   after the referee report (QR2)" (items (R1), (R2), ..., no item (b)); the integer-c group-level statement and the quote "for
   piecewise-Moebius maps with several touching points, which Theorem [main] does not give" are Sec. 5, paragraph (b)
   (implementation_C11.toc; tex line 824-828, p. 22). The same wrong "C11 S8(b)" is in rigor/network_second_order.tex:1152
   and on the refereed card network-law-c-linear (not in this packet: for the orchestrator).
5. [MINOR] "exact recovery never occurs": vacuum-rigidity-exact-recovery (c) restricts to protocols whose last step keeps
   a non-empty part (degenerate exception: a step conditioning on the entire block); its title is unqualified, so this
   is consistent with the card's title, not with its Statement.
6. [MINOR] "PROVED and refereed": the cited cards carry status `proved` (passed review); `refereed` is a stronger KB
   status word (AGENTS.md section 3). Say "proved, passed review".

## 3. cft_cmi:vwz-protocol-ordering
Verdict: **FAIL** (the VWZ comparison now says the opposite of what the evidence shows about VWZ's own prose).

Checked and correct: corner data zeta_1 = a/b, zeta_2 = a(a+2b)/(2b(a+b)), zeta_3 = a/b, e^{Delta_23} = 1/eta,
zeta_eff = 2a/b (cor:vwz <1>1; rigor/ref_p6_4_composite.out block W, exact; my eta-table in ref_p6_7_checks.out C);
the bracket 1 <= liminf <= limsup <= 2 as a/b -> 0 is cor:vwz verbatim (REF-P6-4: "thm:T5, cor:vwz ... stands"), with
the upper half from thm:T5 + cor:W3W4(i) (Ghat(log 1/eta)/Ghat(0) in [sqrt(eta)(4-eta)/3, 4 sqrt(eta)/3], so ~ (4/3)
Ghat(0) eta^{1/2}) and the lower half by restriction to F(p_2,p_5) (network-upper-uniform-two-corners); the second-order
ratio formula and "middle-out worst" (zeta_2 < zeta_1, |Ghat| <= Ghat(0)); the CONJECTURAL clause (U1 for M = 2) and
the status `conjectural` with a concrete `next`; the lattice numbers against lattice-vwz-protocol-ratios and N3.out
(rerun byte-identical): within 0.7 % (3.66(3) vs 3.634-3.647 ... 2.316 vs 2.322-2.325), R21 = 2.2118 ... 2.499 ->
"2.21-2.50", 26 rows = 3+4+3+7+4+5 resolutions; 8 f2 = 0.06755 c; Fig. 25 sentence; corner-measure list.

Defects:
1. [BREAK, the fail] "Phi1 < Phi2 < Phi3 in all 26 (eta, n) rows, so VWZ (5.10)-(5.11) with f-prime < f ('sequential
   recovery less effective than the single step') is contradicted". VWZ p. 47 (PDF p. 48), verbatim: "-log F(2) ~
   -log F(3) prop. f' c eta^2. (5.10) with f' < f, confirming that the sequential recovery is less effective than the
   single-step case." Phi1 < Phi2 < Phi3 means the sequential protocols have the LARGER error, i.e. sequential recovery
   IS less effective: the lattice and the calculus CONFIRM VWZ's prose and contradict only "f' < f". The two halves of
   VWZ's sentence point opposite ways -- the point REF-P6-0 (defect 2) and REF-P6-1 required the card to state, and the
   REF-P6-2-passed version did. The parenthesis now glosses f' < f by the prose and declares the prose contradicted.
   REPAIR: "... so VWZ's 'f' < f' after (5.10) is contradicted on the lattice and by the calculus (f'_3 = 4 f exactly),
   while their accompanying words 'the sequential recovery is less effective than the single-step case' agree with
   Phi1 < Phi2 < Phi3: VWZ's sentence is self-contradictory".
2. [MINOR, wrong locator] "(5.10)-(5.11)": (5.11) is "1/2 (I(A:C|B) + I(B:D|C) + I(A:D|BC)) = -(c/6) log((1-eta)/(1+eta))
   ~ (c/3) eta", the CMI comparison, which nothing here contradicts. Cite (5.10) and the sentence after it.
3. [MINOR, number] "0.281(5), 3.1 fit spreads below the closed-form 0.29514": N3.out:223 gives X = 0.28140 +- 4.5e-3
   and "(S - X)/spread = 3.0"; lattice-vwz-protocol-ratios: "3.0 fit spreads (3.1 with REF-P6-6's spread 0.0044)". With
   the printed (5) the distance is 2.75 spreads (ref_p6_7_checks.out C). Quote 3.0, or 3.1 together with 0.0044.
4. [MINOR, quantifier] The PROVED parts hold for the free chiral fermion F_r (cor:vwz is stated "on F_r(ABCD)"; Phi_A is
   Theorem A's free-fermion function; Protocol 3 is not covered at general c, network-law-c-linear). VWZ's Sec. 5 is
   itself "the free fermion CFT" (p. 47), so say "free chiral fermion" in the setup sentence.
5. [MINOR] "at eta = 0.05 (all zeta <= 0.21)": zeta_eff = 2a/b = 0.2105 (rounding only).

## 4. cft_cmi:corner-correlation-kernel
Verdict: **FAIL** (status `proved` with no `depends`: the one missing edge in the KB).

Checked and correct:
- (a)-(e) and (cf) are thm:T4 verbatim (rigor/network_second_order.tex:749-771), including "C^1 but not C^2 at 0",
  which G1b moved into T4(e) after REF-P6-4's MINOR; the definition of Ghat (real polarisation, T0 frame, y-translate of
  ddot) matches corner-kernel-closed-form.
- The nine values 0.8983866 ... 0.0244192: recomputed by three independent methods (ref_p6_7_checks.out B), all within
  rounding of the printed digits; T4(d) bounds hold at the nine points. "three methods agree to 2.3e-14":
  g1b_kernel.out:50, :69 (quadosc, QUADPACK, closed form, series). "recomputed independently to 7e-16":
  referee_network_second_order.tex:29. "4e-10" (status note): ref_p6_5_kernel.out:38-46, max |mine - g1b| = 4.3e-10.
- Two frames (corner-kernel-two-frames, REF-P6-5b): agreement 1.6e-4, closed form inside every agreed interval,
  alpha = 0.504 +- 0.009, sign margin >= 72: as on that card.
- Consequences: cor:W3W4(ii) assumes e^Delta >= 2/eps, and the card writes "with the separation constraint e^{Delta} >=
  2/eps", so the O(eps^{5/2}) is correctly conditioned.
- Status `proved` is the weakest that fits the answered question (thm:T4, passed review); numerical items are labelled.

Defects:
1. [GAP, the fail] No `depends` line. `kb -p cft_cmi deps --check`: "50/51 proved/refereed claims declare depends";
   a loop over kb/projects/cft_cmi/claims shows corner-correlation-kernel is the one without. Its proved content IS
   thm:T4 = card corner-kernel-closed-form (Lamport BY). REVIEW_BRIEF item 6: a missing edge is a failure. REPAIR:
   `depends: corner-kernel-closed-form` (it carries const-gb and const-f2 below it).
2. [MINOR, number] "uncertainties 5e-4 ... 4e-4": corner-kernel-two-frames gives (5), (5), (6), (6), (6), (5), (5),
   (41), (36) in units of the last digit, i.e. 3.6e-4 ... 6e-4.
3. [MINOR, number] "0.281(5), 3.1 fit spreads below 0.29514": as section 3 item 3 (3.0 with the author's spread 4.5e-3).
4. [MINOR, verifiability] "python3 numerics/networks/corner_kernel.py K3 reproduces numerics/networks/kernel_decay.out":
   K3 opens kernel_decay.out for writing itself (corner_kernel.py:40, :488), so the command as written overwrites the
   file it is to be compared with; say "copy kernel_decay.out aside first" (same wording on corner-kernel-two-frames).

## 5. cft_cmi:network-second-order-law
Verdict: **FAIL** (a misquoted range; a cor:W3W4 consequence stated more generally than proved, without its proviso).

Checked and correct: the fixed-configuration law against network-law-free-fermion and cor:law (free fermion c = r,
canonical composite of the scaled corner measure, (H), o(s^2) at fixed (M, zeta, y), REF-P6-4: T1, T2, cor:law stand);
Ghat(0) = 1/(12 pi^2), 0 < Ghat < Ghat(0) off 0, (4/3) Ghat(0) e^{-|Delta|/2} (T4(d),(e)); thm:T6 scope against
network-law-c-linear (canonical order, all L->R chains, VWZ 1(A) and 2; Protocol 3 open at general c); the REMAINDER
paragraph against network-upper-uniform-two-corners and network-remainder-uniformity (U1, U2); lem:nogroup; thm:sep;
rem/zeta^3 = -0.0244, -0.0136, -0.00455, -0.00058 at zeta = 0.05 (two-corner-remainder-finite-zeta); 2.21-2.50;
0.281(5) vs 0.2951; depends of the main claim (corner-calculus, network-law-free-fermion, corner-kernel-closed-form,
network-law-c-linear, implementer-hypotheses) and all tokens resolve; g1b_kernel.out block L exists (max rel. dev.
3.7e-18). Status `proved` fits the fixed-configuration law.

Defects:
1. [BREAK, number; the fail] "lattice-lr-chains-cross-terms: Phi_tot/sum Phi_step = 1.48-2.07 for geometric chains with
   zeta = 0.49-1.04". The card and numerics/networks/N4.out:49, :76, :103, :130 give 1.4828, 1.8171, 2.0699, 1.4610
   (rerun byte-identical, ref_p6_7_N4.out; ref_p6_7_checks.out D), plus 1.750 not extrapolated: the range is
   1.46-2.07. The excluded value 1.46(1) belongs to the r = 1/3, 4-block chain, whose zeta^(I) = 0.4875 is precisely the
   lower end "0.49" of the quoted zeta range (N4.out:110).
2. [GAP; the fail] "with the decay of Ghat the cross term of all-weak protocols is O(eps^2 sup Ghat) = O(eps^{5/2})
   (cor:W3W4): ... distinct weak junctions are additive in zeta^2 up to that order". cor:W3W4(ii)
   (rigor/network_second_order.tex:935-938) says "the cross terms of an all-weak L->R chain are O(eps^{5/2}) in the
   second-order law --- again at fixed configuration; as a statement about protocols with eps -> 0 it needs sec:T5".
   The card (a) widens L->R chains to "all-weak protocols" although e^{Delta} >= 2/eps (thm:sep) is proved for L->R
   chains only, and (b) drops the proviso, which REF-P6-3 required to stay ("the 'given the uniform remainder' proviso
   stays, it is genuinely open") and which the REF-P6-3b-passed version carried. REPAIR: "for all-weak L->R chains the
   cross terms of the second-order law are O(eps^{5/2}) at fixed configuration (cor:W3W4(ii)); as eps -> 0 this needs
   the uniform remainder (open)".
3. [MINOR] thm:T3 range: the card gives only s max_k zeta_k < pi sqrt3; network-global-bound-coincident also requires
   2 s^2 Z^2/(12 pi^2) < 1, which is not implied for M >= 2 (Z <= M zeta_max gives only < M^2/2).
4. [MINOR, inherited] Normalisation of the conjectured network form -(1/2) log(1 - 2 sum zeta_j zeta_k G), G = c Ghat:
   at coincidence it equals the proved -(c/2) log(1 - 2 s^2 Z^2/(12 pi^2)) only for c = 1; for c = r = 2 and
   s^2 Z^2/(12 pi^2) = 0.1 they are 0.2554 and 0.2231, so "weaker than the network form ... and equal to it when all
   corners coincide" fails literally for c >= 2 (and the form is not additive over components). Same wording on the
   refereed network-global-bound-coincident and rigor/phase6_brief.md:84; natural form -(c/2) log(1 - 2 s^2 sum
   zeta_j zeta_k Ghat(y_j - y_k)). For the orchestrator.
5. [MINOR] The PROVED clauses thm:T3, thm:T5, thm:sep enter only as ev: tokens; if the card's status covers them, add
   network-global-bound-coincident, network-upper-uniform-two-corners, corner-separation-constraint to `depends`.
6. [MINOR] "exact two-corner fidelities on the box (60, 30) give the cubic coefficient of the remainder": add "of the
   windowed box problem (O(zeta^3) there automatically); the continuum remainder's order is not tested", as
   two-corner-remainder-finite-zeta and G3's 2026-10-05 note on this card say.

## 6. cft_cmi:phase6-plan
Verdict: **FAIL** (the Statement contradicts itself and the status file on the G2 review state).

Checked and correct: both doc tokens resolve (rigor/phase6_brief.md, rigor/PHASE6_STATUS.md); G1a 42 pp and G1b 29 pp
(pymupdf); the G1a/G1b/G3 card lists and statuses (all passed review, section 0); "agreeing to 1.6e-4", "decay 0.504 +-
0.009" (corner-kernel-two-frames); "189 sites" (6-block r = 1/2 chain); "23/23 validation" (PHASE6_STATUS.md:120 "all
23 passed"; REF-P6-6's note on lattice-vwz-1b-equals-1a "V0 rerun byte-identical (23/23)"); "Protocol 3 vs single step
1.000 +- 0.003" (lattice-protocol3-equals-theorem-a: Q2 = 1.000(2), 1.001(3), 1.000(2)); "within 0.7 percent",
"2.21-2.50", "against VWZ (5.10)" (correct: only (5.10)'s f' < f is contradicted); zeta >= 2r/(1+r)^2
(referee_lattice_chain.tex:309-311); lem:nogroup; Fig. 25; `next` concrete; status `active` right for a decision card.

Defects:
1. [BREAK, state; the fail] "All four tracks are done and refereed" and, in the same Statement, "G2
   (numerics/networks/lattice_chain.py; REF-P6-6, repairs in progress)". PHASE6_STATUS.md:14 reads "repairs applied by
   G2 2026-10-05; REF-P6-6b PASS 2026-10-05: all six G2 cards pass", and every G2 card shows `review: passed 2026-10-05
   by REF-P6-6b` (REF-P6-6 for lattice-vwz-1b-equals-1a). The clause was written at 21:35:19, eleven minutes before
   REF-P6-6b's verdicts (21:46); it is now false and contradicts the first sentence. REPAIR: "REF-P6-6/6b".
2. [MINOR] "1 <= Phi(2)/Phi(1) <= 2 for VWZ in the limit": what is proved is 1 <= liminf <= limsup <= 2 (cor:vwz).
3. [MINOR] "the coincident-constant global bound under s max zeta_k < pi sqrt3": plus 2 s^2 Z^2/(12 pi^2) < 1 (section 5
   item 3).
4. [MINOR] "the brief's weak-corner premise": the premise is in G2's brief (rigor/phase6_g2_brief.md:38), not in
   rigor/phase6_brief.md, which this card cites as its evidence.
5. [MINOR] "the cubic remainder coefficient from exact two-corner fidelities": of the windowed (60,30) box problem
   (section 5 item 6).

## 7. common:agent-resumption (newest note)
Verdict: **PASS**. Statement and How to verify unchanged since REF-AGENTSMD-1's pass; locators still resolve
(kb/projects/cft_cmi/import/legacy-memory-log.md:76 P4 -> P4b, :138 RK/RRr/RCr resumed via SendMessage;
kb/kbcore/store.py def note calls mark_pending). The 2026-10-05 note against the record:
- PHASE6_STATUS.md:124-131: all three referees died of the session limit on 2026-10-03; REF-P6-4 had its report and six
  verdicts (18:33) and lost only its final message; REF-P6-5 and REF-P6-6 had skeletons and scripts; resumed 2026-10-05
  by SendMessage.
- Details beyond the status file, checked in the subagent transcripts: each of agents a7c520af4dcb14eb6,
  ac52db970d7bc5900, a92b34b7e298ece88 ends its 2026-10-03 activity with "You've hit your session limit . resets 7pm
  (Europe/Berlin)", `"error":"rate_limit"`, `"apiErrorStatus":429`, at 18:33:58, 18:34:06, 18:34:58 CEST (so "within
  15 minutes" holds; in fact within one minute); the resume messages of 2026-10-05 restate the chunk rules ("Chunk rules,
  restated: append at most 100 lines / 12,000 characters ...").
- MINOR (not on the card): PHASE6_STATUS.md:124 "~18:34-18:50" and the resume message to REF-P6-6 ("about 18:50")
  disagree with the transcript (18:34:06) for REF-P6-6.

## 8. common:scratchpad-venv-fragility (newest note)
Verdict: **PASS**. The card was imported 2026-09-14 and has no earlier review event, so I checked it whole.
- Statement against its How to verify: the memory file
  $CLAUDE_CONFIG_DIR/projects/-Users-alex-Documents-Uni-Hannover-claude-team/memory/team-config-dir.md, addendum
  "Venv fragility (2026-09-10)", says the scratchpad venv was deleted at a session restart with the path unchanged, gives
  the same rebuild line and package list, nohup ... < /dev/null & disown, and "results must be written to files under
  the project, never the scratchpad". "keep artifact sources in the project" is a recommendation not in that addendum
  (MINOR; it is an instruction, not a claim of fact).
- The 2026-10-05 note: PHASE6_STATUS.md:151-153 ("another agent's fill.py overwrote its own in the shared scratchpad
  (rule from now on: agents use <scratchpad>/<actor>/)"); REF-P6-5's final message in its transcript ("Another agent's
  fill.py overwrote mine in the shared scratchpad. Nothing was damaged; agents should get their own subdirectories").
  "briefs state it": every agent message sent after the event states the rule (G3 19:17 UTC <scratchpad>/G3/, REF-P6-5b
  19:25, G2 19:31, REF-P6-6b 19:42, REF-P6-7 19:48).
- MINOR: "(REF-P6-5 report)" points at REF-P6-5's final message; the report file rigor/referee_corner_kernel.tex does
  not mention fill.py (it mentions only the stray .err file, line 467-468). A later note may cite PHASE6_STATUS.md:151-153.

## 9. Verdicts recorded and lint counts
Recorded 2026-10-05 22:10-22:11 as REF-P6-7 (`kb history` shows the actor on all eight):
- FAIL: dhat-quadrature-certification, multi-interval-networks, vwz-protocol-ordering, corner-correlation-kernel,
  network-second-order-law, phase6-plan (notes carry the repair text of sections 1-6).
- PASS: common:agent-resumption, common:scratchpad-venv-fragility.

`kb lint --all` after the verdicts: cft_cmi 0 issues, 6 awaiting review (the six FAILED cards, "repairs not yet
absorbed"), 22 dependency/locator warnings (none on a packet card); claude-team-knowledge 0/0; dmax_mbz 0/0 (6 warnings);
haag_s3 0/0 (1); common 0/0 (1); links 0/0.

For the orchestrator, outside this packet (MINOR, no verdict of mine): (i) "C11 S8(b)" in
rigor/network_second_order.tex:1152 and on network-law-c-linear should be "C11 S5(b)" (rigor/implementation_C11.tex
paragraph (b), lines 824-828, p. 22); (ii) the c-normalisation of the conjectured network form on
network-global-bound-coincident and rigor/phase6_brief.md:84 (section 5 item 4); (iii) PHASE6_STATUS.md:124 "~18:34-18:50"
vs the transcripts (all three limits hit 18:33:58-18:34:58); (iv) corner-kernel-two-frames' How to verify has the same
overwrite issue as section 4 item 4. Files of this pass: rigor/referee_phase6_cards.md, rigor/ref_p6_7_checks.py,
rigor/ref_p6_7_checks.out, rigor/ref_p6_7_N3.out, rigor/ref_p6_7_N4.out (all untracked; commit is the orchestrator's).

## Second pass (REF-P6-7b)
Requested 2026-10-05 after the orchestrator's edits of 22:14:23-22:14:39 (`set` events only; no note by any other
agent after my first-pass verdicts). Eight cft_cmi cards, judged against the first-pass notes above.

### 2.1 vwz-protocol-ordering
**PASS.** Defect 1 repaired in the right sense: "Phi1 < Phi2 < Phi3 ...: sequential recovery IS less effective than
the single step, as VWZ's prose after (5.10) says, while their inequality f-prime < f ... is contradicted ... their
sentence contradicts itself" (VWZ p. 47). Defect 2: "(5.11) is the conditional-mutual-information formula and is not
in question". MINOR 3: "3.0 fit spreads ... (N3.out:223; 3.1 with REF-P6-6's own spread 0.0044)". MINOR 4: the free
chiral fermion is named; the lattice is the half-filled hopping chain = free Dirac fermion, c = 1, two chiralities
(as on lattice-protocol3-equals-theorem-a). The added "the corner data of G1a are pure geometry and hold for every net
whose zero-collar map is the geometric compression" is a conditional statement about point maps, which is what G1a
proves. Nothing new and wrong; status `conjectural` and `next` unchanged and right.

### 2.2 network-second-order-law
**PASS.** "1.46-2.07" (N4.out); the cor:W3W4 sentence now reads "all-weak L->R Petz chains ... O(eps^{5/2}) at fixed
configuration (cor:W3W4; as eps -> 0 together with the configuration this needs the uniformity of sec:T5, which is
open)", matching rigor/network_second_order.tex:935-938; thm:T3 with both conditions; the network form written
-(c/2) log(1 - 2 s^2 sum zeta_j zeta_k Ghat), which at coincidence is exactly the thm:T3 bound and is additive over
components, so "weaker ... and equal to it when all corners coincide" now holds for every c. Residual MINORs (not
grounds for failure, first-pass items 5-6): depends still lists only the law's inputs (the thm:T3/T5/sep clauses enter
as ev: tokens), and "the cubic coefficient of the remainder" is still not marked as that of the windowed box problem.

### 2.3 corner-correlation-kernel
**PASS.** depends = corner-kernel-closed-form (`kb deps --check`: now 51/51 proved/refereed claims declare depends);
uncertainties "3.6e-4 to 6e-4"; "3.0 fit spreads (N3.out:223)". Residual MINOR: How to verify still runs
corner_kernel.py K3, which rewrites kernel_decay.out itself.

### 2.4 dhat-quadrature-certification
**PASS.** The false sentence is replaced by two sourced facts: the windowed method reproduces results_A2.txt:1 (and
:3) -- numerics/networks/kernel_k4_validate.out:6-7, rel. diff 3.8e-8, 3.4e-8 -- and the (120,45) line value
0.0084112 is line_so.py's line-symbol QFI (line_so.txt:4); neither from fid_relent. How to verify now reaches the
finding. Residual MINORs: (a) it attributes the shifted-frame NaN to kernel_validate.out line (d'), but that file has
no such NaN (its only nan, line 24, is f2_box of the unresolved Q_box); the NaN is in rigor/ref_p6_5_checks_9.out:16-17,
which the field also cites. (b) Newly noticed, also in the first-pass text: numerics/README.md:15 lists line_so.txt
(and results_hp.txt) as "OLD (basis-phase bug, 5e-5 relative effect on Phi) | superseded, kept for the audit
rigor/check_note5_numerics.tex"; "published line value" is the value quoted in that audit (check_note5_numerics.tex:677).
(c) kappa_max,eff in next (2).

### 2.5 multi-interval-networks
**PASS** (recorded after the five named cards under review passed, so that the new How to verify's "every one has
review: passed" is true). How to verify now names the cards, both documents, the four referee reports and the status
file; "strengths add at a common junction" credited to corner-calculus and "zeta_step (1 + z')" to
frame-strength-amplification; next (2) cites rigor/implementation_C11.tex Sec. 5 paragraph (b), l. 824 (checked:
lines 824-830). Residual MINORs (first-pass items 3, 5, 6): "1 <= Phi(2)/Phi(1) <= 2 in the limit" still cites the
vwz card rather than cor:vwz and does not say liminf/limsup; "exact recovery never occurs" without the last-step
qualifier; "PROVED and refereed".

### 2.6 phase6-plan
**PASS.** The G2 clause now reads "REF-P6-6/6b, all six cards pass", consistent with "All four tracks are done and
refereed" and with PHASE6_STATUS.md:14. Residual MINORs (first-pass items 2-5) unchanged.

### 2.7 network-law-c-linear (re-opened)
**PASS.** Only the locator changed: "Implementation_C11 Sec. 5, paragraph (b) (rigor/implementation_C11.tex l. 824;
the locator Sec. 8(b) of 2026-10-03 was wrong, REF-P6-7) has it only for integer-c Fock representations". C11:824-830
says exactly that (group-level extension for all positive integers n; "It does not extend to general c"). The document
was corrected too (network_second_order.tex:1152 "C11 S5(b)", dated line :1254; 29 pp, log clean). For the
orchestrator (MINOR, document only): network_second_order.tex:1137 cites "C11 S8(a)" for (BW) and (H2)-(H2') of the
fermion; C11 Sec. 8 has items (R1), ..., no (a) -- presumably Sec. 5 paragraph (a) or item (R8).

### 2.8 network-global-bound-coincident (re-opened)
**PASS.** The comparison is now with the c-normalised form -(c/2) log(1 - 2 s^2 sum zeta_j zeta_k Ghat), with the
remark that the brief's -(1/2) log(1 - 2 sum zeta zeta G) agrees only for c = 1; at coincidence it equals (1), and
since sum zeta_j zeta_k Ghat(y_j - y_k) <= Ghat(0) Z^2 with x -> -log(1 - x) increasing, (1) is the weaker bound,
equality iff all corners coincide. "implies only the upper half" holds (-(c/2) log(1 - 2x) = c x + O(x^2)). The brief
(rigor/phase6_brief.md:84-85) carries the same correction. Range, lem:nogroup and depends unchanged and right.

### 2.9 Verdicts and lint
Recorded 2026-10-05 as REF-P6-7b, all PASS: vwz-protocol-ordering, network-second-order-law, corner-correlation-kernel,
network-law-c-linear, network-global-bound-coincident, dhat-quadrature-certification, phase6-plan, then
multi-interval-networks last, after confirming that all 20 cards its Statement names show `review: passed`.
`kb lint --all`: cft_cmi 0 issues, 0 awaiting review (22 dependency/locator warnings, none on these cards; `deps
--check` now 51/51 proved/refereed claims declare depends); claude-team-knowledge, dmax_mbz, haag_s3, common, links:
0 issues, 0 awaiting review.

Out-of-KB fixes checked: rigor/network_second_order.tex:1152 "C11 S5(b)" with the dated line :1254, PDF 29 pp, log
without `^!` or undefined references; rigor/phase6_brief.md:84-85 c-normalised; rigor/PHASE6_STATUS.md:124
"18:33:58-18:34:58".

For the orchestrator (outside the packet, no verdict of mine):
(i) network_second_order.tex:1137 "C11 S8(a)" (section 2.7).
(ii) two-corner-remainder-finite-zeta says the eps = 1e-11 window "misses numerics/results_hp.txt:1 by 8.8e-6 relative
(cause not identified)". numerics/README.md:15 lists results_hp.txt as OLD (basis-phase bug, superseded); the current
file results_hp2.txt:1 has -logF_sub = 5.744386e-07, and kernel_k4_validate.out:8 has 5.744385648e-07: agreement
within the 7 printed digits (difference 3.5e-14, i.e. 6e-8 relative). The mismatch looks like the superseded
reference file, not the window method; I did not rerun K4v against results_hp2.txt.

