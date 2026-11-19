# Repair round of 2026-11-19 — status (brief: rigor/repair/REPAIR_BRIEF.md; source: rigor/council/)
Seats (track agents, Opus). Existing files are changed only through rigor/repair/<SEAT>_patch.json, applied by the
orchestrator with rigor/repair/check_patch.py --apply; referee pass (Opus) after application.
Launched 2026-11-19:
- R1 index zero + Theorem A patches      agent ab17a5277e1d69b9a  rigor/index_zero.tex, rigor/repair/R1_patch.json  [done: index_zero.tex 11 pp + check; 13 patch items applied by orchestrator; 6 shots rigor/shots/r1_BJL_*.png need pgit sync; R1 built a scratch venv with pymupdf (deviation)]
- R2 Theorem B (H1), Moebius reduction   agent a0c5a6c9f48a86cd4  rigor/moebius_reduction_general_nets.tex, R2_patch.json  [done: 17 items applied by orchestrator; new doc 14 pp; card moebius-reduction-general-nets added by R2; shot rigor/shots/R2_CDIT_axioms15.png needs pgit sync]
- R3 Note 5, optimality, networks, theta agent aac4ab49bdf761c48  R3_patch.json, numerics/optimality_all/theta_three_fits.py  [done: 58 items over 13 files, applied by orchestrator; theta three-fit check done; shots for 4 new citations missing (no pymupdf)]
- R4 paper 1                             agent a3da53d0ce9dca44f  R4_patch.json  [done: 47 items, compile-tested 30 pp; applied by orchestrator, paper1 compiles 0 errors]
- R5 paper 2                             agent acbd4253f8896ad18  R5_patch.json  [done: 38 items; applied by orchestrator, paper2 compiles 0 errors; title changed (user decision pending); P8 deferred]
Orchestrator, meanwhile: KB bookkeeping items of the council (C6 §C, C4 §3) once the seats report their PROPOSED CARD CHANGES.
Orchestrator 2026-11-19: card changes batch 1 executed (rigor/repair/card_changes_1.json via kbrepl.py, + notes/evidence):
quasi-free-fidelity-formula, large-zeta-values, theta-value, network-law-c-linear, network-second-order-law,
two-branch-law-lattice, conj-s2, thm-b-universality, compression-not-optimal-exact-fidelity, exact-fidelity-optimality-open,
boson-check, vwz-protocol-ordering, phi-derivative-nondecreasing, network-global-bound-coincident, paper1-status, paper2-status.
Not executed (with reason): tail-bound split and ac-lower-bound-zero (Statements already separate the proved implication from
the numerical inputs); kkt-noise-criterion-numerics (quoted sentence not in the Statement; check after R1/R2).
Pending: new cards phi-unconditional-linear-bound, hellinger-coefficient-h2 (C6 A8); R1, R2 results; referee pass.
Orchestrator: card batch 2 (card_changes_2.json): thm-b-universality ((C7) form of (H1)), implementer-hypotheses; notes on
thm-b-universality, mobius-reduction-cross-ratio; new cards phi-unconditional-linear-bound, hellinger-coefficient-h2 [proved].
kb lint: 0 issues, 21 awaiting review. Waiting for R1; then packet referee(s).
Referees (Opus; brief rigor/repair/REFEREE_BRIEF.md), launched 2026-11-19:
- REF-RP-1 Theorem B + Moebius reduction   agent ae43099e8f1e22943  rigor/repair/REF_RP_1_report.md  [done: implementer-hypotheses PASS; 3 FAIL with small repairs, executed by orchestrator (ORCH_patch_1.json, card_changes_4.json); re-review pending]
- REF-RP-2 notes, optimality, networks     agent a17ae1ffa71f51d8a  rigor/repair/REF_RP_2_report.md  [done: 5 PASS, 4 FAIL (card wording; repaired: card_changes_5.json, ORCH_patch_2.json), vwz-protocol-ordering no verdict (needs python-flint); re-review pending]
- REF-RP-3 papers + two new cards          agent aee2420fa2e421ee8  rigor/repair/REF_RP_3_report.md  [running]
- REF-RP-4 index zero: to launch after R1 reports.
- REF-RP-4 index zero   agent a7cceccd65ae53465  rigor/repair/REF_RP_4_report.md  [done: rate-of-remainder, const-f2 PASS; group-index-zero-large-s FAIL (stale text; PROMOTE recommended); author repairs sent to R1; checklist in the launch message:
  lem:cubic, thm:path, thm:sv, thm:group/lem:gen, applications, prop:ranges, check script, R1 patch, cards
  group-index-zero-large-s, rate-of-remainder, const-f2 (verdict), pushforward-blocks-equal-singular-values (report only)]
Orchestrator: card batch 3 (card_changes_3.json): const-f2 0.0675, rate-of-remainder range wording; note on group-index-zero-large-s.
All five repair seats done; all patches applied; every patched document compiles with a clean log.
R1 resumed 2026-11-19 (same agent ab17a5277e1d69b9a) for author repairs after REF-RP-4: (W) hypothesis, prop:ranges item 3, check script test (A), R1b_patch.json. REF-RP-3 still running.
REF-RP-3 done: paper2-status, conj-s2, boson-check, hellinger-coefficient-h2 PASS; paper1-status, two-branch-law-lattice,
phi-unconditional-linear-bound FAIL -> repaired by orchestrator (ORCH_patch_3.json, card_changes_6.json).
R1 round 2 done (index_zero.tex 12 pp; R1b_patch.json applied). group-index-zero-large-s and
pushforward-blocks-equal-singular-values (narrowed to (W)) promoted to proved by orchestrator, pending re-review.
Venv rebuilt without pymupdf: <scratchpad>/venv (numpy, scipy, mpmath, python-flint 0.9).
Re-review (one referee per card), launched 2026-11-19:
- REF-RR-A  agent a7842c0e96993aefd  rigor/repair/REF_RR_A_report.md  [running] group-index-zero-large-s,
  pushforward-blocks-equal-singular-values, rate-of-remainder, thm-b-universality, moebius-reduction-general-nets,
  mobius-reduction-cross-ratio, phi-unconditional-linear-bound
- REF-RR-B  agent aedfad547b22142d3  rigor/repair/REF_RR_B_report.md  [running] theta-value,
  compression-not-optimal-exact-fidelity, exact-fidelity-optimality-open, phi-derivative-nondecreasing,
  two-branch-law-lattice, paper1-status, paper2-status, vwz-protocol-ordering (first review)
Open follow-ups (not in this round): network_second_order.tex thm:T3 range can be widened (index_zero prop:ranges item 6);
condition (W) for general chi; paper2 cor:tensor wording; shots for four citations of seat R3; ./pgit sync for new shots.
Re-review results: REF-RR-A: moebius-reduction-general-nets, mobius-reduction-cross-ratio, phi-unconditional-linear-bound PASS;
group-index-zero-large-s, pushforward-blocks-equal-singular-values, rate-of-remainder, thm-b-universality FAIL (card text,
depends; mathematics stands). REF-RR-B: theta-value, compression-not-optimal-exact-fidelity, exact-fidelity-optimality-open,
phi-derivative-nondecreasing, paper2-status, vwz-protocol-ordering PASS; two-branch-law-lattice, paper1-status FAIL.
Repairs by orchestrator: ORCH_patch_4.json, ORCH_patch_5.json, card_changes_7.json, depends on the two index cards.
Third pass: REF-RR-C on the 7 pending cards (packet <scratchpad>/review_packet_3.md).
- REF-RR-C  agent a595e7fa03ec7986b  rigor/repair/REF_RR_C_report.md  [running] third pass, 7 cards
REF-RR-C: 5 PASS; two-branch-law-lattice, paper1-status FAIL -> repaired (ORCH_patch_6.json, card_changes_8.json); REF-RR-C resumed for the re-check of these two.
REF-RR-C re-check: two-branch-law-lattice, paper1-status PASS. kb lint: 0 issues, 0 awaiting review (cft_cmi). Round closed 2026-11-19.
Committed b972fdd (public), pgit sync done (private). kb sync REFUSED: lint issues in area_law (169) and zed (303): evidence paths missing on this machine; not caused by this session; --force needs the user.

## 2026-11-19 evening: user decisions
- "pull area_law and zed onto this machine first. Yes to the other decision points" (push; title kept; P8 applied).
- zed cloned from alexander-stottmeister/zed into the workspace root: kb lint 0 issues.
- area_law cloned from alexander-stottmeister/area-law (last remote commit 2026-10-24): 92 evidence paths still missing,
  all under area_law/peps/ and area_law/peps_approx.pdf (work of 2026-10-24 ... 11-07 on host Macmini, not on the remote).
  kb sync stays refused until that machine pushes area_law (or the user orders --force).
- Pushed: public a1b73a8, private d3e2358.
- P8: rigor/repair/ORCH_patch_7.json applied (thm:B unconditional, cor:tensor, 'under review' wordings); paper2 26 pp,
  universality_theorem_B 25 pp, logs clean. Referee REF-P8 agent ab65b02e7ca80cb8b, brief rigor/repair/REF_P8_BRIEF.md.
- REF-P8: FAIL (item 4, Moebius-reduction range in three places) -> rigor/repair/ORCH_patch_8.json -> re-review PASS. kb -p cft_cmi lint 0 issues, 0 awaiting.
