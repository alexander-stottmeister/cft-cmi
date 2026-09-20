# rigor/ index (auto-generated 2026-09-05)

Conventions: README_AGENTS.md. Preamble: rigor_preamble.tex. Screenshots: shots/. Errata log: errata_log.md. Build: build_all.sh.

| document | pages | content |
|---|---|---|
| audit_dependencies.tex | 31 | V6: dependency graph of all results, weakest links |
| check_note4.tex | 39 | V2: Lamport check of Note 4 (+ orchestrator correction of the Majorana claim) |
| check_note5_numerics.tex | 20 | V4: independent recomputation of the Note 5 numerics (basis-phase bug, tail correction accuracy) |
| check_note5_theory.tex | 36 | V3: Lamport check of Note 5 theory (exact first-order kernel, monotonicity proof) |
| check_notes_1_2.tex | 36 | V1: Lamport check of Notes 1 and 2 |
| cited_R1.tex | 31 | R1: LX, CH, BGL, Wiesbrock, Borchers with screenshots |
| cited_R2.tex | 32 | R2: FHSW, FH22, Araki, Petz, Ohya-Petz, VWZ with screenshots |
| cited_R3.tex | 26 | R3: Uhlmann/Alberti, Powers-Stormer, Araki-Yamagami, Petz variational formulas |
| cited_R4.tex | 38 | R4: Carpi-Weiner, CDIT, Fewster-Hollands, Nag-Sullivan, Takhtajan-Teo, Shen, VWZ numerics |
| cited_results_all.tex | 130 | Compendium of cited_R1-R4 (one document) |
| findings.tex | 28 | Consolidated findings by severity + status tables + errata (assembled from findings_entries.tex) |
| kernel_identity.tex | 15 | P3: analytic proof of the kernel identity; refereed correct by V8; orchestrator note + A&S/DLMF screenshots appended |
| lamport_example.tex | 1 | Template of the Lamport notation |
| lemma_second_variation.tex | 33 | P1: second-variation lemma — fidelity half PROVED for any vN algebra (three-way identity Thm 3.3); KM half open; 157 Lamport steps |
| quadratic_limit.tex | 27 | P2: quadratic limit — liminf Phi/zeta^2 >= g_B/8 proved unconditionally; upper bound 2log2·f_2 modulo one interchange; Phi <= tau/(1-tau) |
| referee_kernel_identity.tex | 12 | V8: referee report on kernel_identity.tex — correct, no gap; independent numerics (v8_kernel_check.py) |
| referee_quadratic_limit.tex | 19 | V7: referee report on quadratic_limit.tex — Thm 4.2 verified; Prop 7.1 step <1>5 false and repaired; scripts v7a-e.py |
| check_notes_6_7.tex | 25 | V5: Lamport check of Notes 6 and 7 — f2=c/(12π²), s2=c/12 confirmed; <TT> normalization proved independently; 2 local BREAKs fixed |
| collar_and_invariant_formula.tex | 8 | P4b: x-space Mellin route — W-hat exact from <TT> + dilation, g_B = 2c/(3π²) and g_KM = c/6 to 1e-11; diagnosis g(L)≠0; collar-limit status (p4_invariant.py/.out) |
| uhlmann_upper_bound.tex | 31 | PA (Phase 1): Uhlmann–Bogoliubov upper bound ⇒ lim Φ/ζ² = c/(12π²) (Thms 8.1-8.2); refereed by PR, repairs R1-R5; §10 proves (H2),(H3) for the fermion |
| referee_uhlmann_upper_bound.tex | 19 | PR: referee report on uhlmann_upper_bound.tex (in progress) |

Phase 1 (2026-09-08): brief in phase1_brief.md; numerics in ../numerics/p1_bogoliubov.py/.out (PN), ../numerics/lattice/ (PL), ../numerics/results_hp14.txt (Track C); paper skeleton in ../paper1/main.tex.
| tail_bound.tex | 17 | PT (Phase 1, O4): unconditional tail bound 0.173ζ²/κc + 0.88ζ²/κc², Prop 4.1 upgraded (Thm 4.2), certified brackets; log⁻² rate obstructed |
| universality_theorem_B.tex | 24 | QA (Phase 2): Theorem B (Thm 7.1) for all diffeo-covariant nets with (H1)-(H3)+(H2'); c-linearity via H_T; refereed by QR1, repairs applied (Sec. 9) |
| implementation_C11.tex | 26 | QB (Phase 2, O5): (H1)-(H3)+(H2') for ALL diffeo-covariant nets (Carpi-Weiner Thm 4.4 + Stone + Trotter; scalar phase via FH05 Prop 5.1); refereed by QR2, repairs applied (§8) |
| kubo_mori_second_variation.tex | 19 | QK (Phase 2, O2): exact identity for unitary orbits; lower bound unconditional, upper bound under modular analyticity; Kosaki route refuted; T(g_tot) case open |

Phase 2 (2026-09-08): brief in phase2_brief.md; bosonic check in ../numerics/boson/ (QN); paper 2 skeleton in ../paper2/main.tex.
| referee_implementation_C11.tex | 16 | QR2: referee report — Theorem 5.1 stands for all nets modulo the phase-lift repair; form-bound window empty (beta = 1 sharp) |
| referee_universality_theorem_B.tex | 15 | QR1: referee report — Theorem 7.1 stands; repairs (H2') a in H_T, (H1) locality clause, graded remark |
| kubo_mori_gauge_lemma.tex | 18 | RK (Phase 2b): gauge lemma REFUTED (inf = 11.09·c/6); exact non-sharp KM upper bound; local Sobolev form of KM; bracket [0.034c, 0.924c]; s_2 = c/12 general stays conjectural |
| rate_of_remainder.tex | 18 | RR (Phase 2b): global bound Phi <= -(1/2)log(1-2 f_2 zeta^2) UNCONDITIONAL (group extension, PA Prop 7.6), c_3 = -0.99(1), log^-2 claim refuted; refereed by RRr, repairs applied (§6.2-6.4) |
| certified_numerics.tex | 11 | RC (Phase 2b): weighted Sylvester bound, cross term removed; 60-digit enclosures of the box value 0.71-1.01%; a priori 1.20 Phi_W; refereed by RCr, repairs applied (Sec. 9) |

Phase 2b (2026-09-09): brief in phase2b_brief.md; paper 2 draft ../paper2/main.pdf (24 pp, RW, 2026-09-09).
| referee_certified_numerics.tex | 12 | RCr: referee report — theory OK, arithmetic of Phi_off not certified; quotable bracket 18-20% |
| referee_rate_of_remainder.tex | 15 | RRr: referee report — global bound and c_3 stand; f_2* = f_2 closable (Prop 3.1); Problem 7.2 verdict mis-scoped |
| optimality_second_order.tex | 14 | S8 (Phase 3, O8): quasi-free second-order problem is an exact SDP; optimum = geometric-compression value (Petz off by 4); A-C lower bound gives 0; Petz not optimal, compression unproved |
| optimality_all_channels.tex | ~13 | Orchestrator (Phase 3b): every recovery channel's recovered symbol is quasi-free feasible (Kadison–Schwarz + Tomita + BJL); exact single-observable fidelity bound; all-channel second-order optimum = quasi-free SDP value (Sion); §5: S10's exact KKT certificate + isometric-orbit refutation, exact-fidelity confirmation, independent Galerkin cross-check of θ. VERDICT: compression not the minimiser of the second-order functional (θ≥0.30); optimality in exact fidelity OPEN (upper half for the rotated channel), E_rec ∈ [D_z, f₂z²] |
| sdp_dual_certificate.tex | ~25 | S10 (Phase 3b): exact necessary-and-sufficient KKT certificate at the compression (unique multipliers, V_c unitary); Legendre reduction V(t)=‖P⊥tP‖²; Möbius rigidity δ_c,DD=0 ⇒ certificate ⇔ E_D u E_D = 0; θ = 0.300(5) numerically ⇒ compression∘e^{−εG*} beats compression by 1−θ; route 2 closed |
| sdp_certificate_numerics.tex | ~18 | S11 (Phase 3b): lattice strong duality/KKT verified (4,8,2); block-exact modular Galerkin discretisation (closed-form Q via Li₂, reproduces f₂ to 0.3%); certificate test at compression structurally inconclusive in finite models; exact windowed fidelity confirms S10's gain (ratio → 0.67) |

Phase 3 (2026-09-09): brief in phase3_brief.md; thermal/RG/gap numerics in ../numerics/lattice/petz_thermal_rg.py (S9, summary thermal_rg_gap_summary.md); paper referee reports referee_paper1.md (PP1), referee_paper2.md (PP2).

Phase 3b (2026-09-10): brief in phase3b_brief.md; all-channel numerics in ../numerics/optimality_all/ (SDP scans, S10/S11 scripts).
| exact_fidelity_upper_half.tex | 21 | E1 (Phase 4): exact-fidelity upper half for isometric quasi-free channels via arbitrary exterior extensions; THEOREM closure(Ext) = N^perp (generic position / twisted duality); E_rec <= (1 - theta_fr) f2 z^2 (1+o(1)), theta_fr > 0 iff E_D u E_D != 0; sandwich Cor 7.5; refereed (referee_exact_fidelity_upper_half.tex, stands with repairs Sec. 10) |
| referee_exact_fidelity_upper_half.tex | 14 | E1r: referee report — theorem stands; repairs R1–R10 applied |
| exterior_extension_numerics.tex | 10 | E2 (Phase 4): Ext = N^perp exactly at every L in the circle model; optimised Uhlmann bound = (1/2)s^2|u|^2 to 1e-7; UB_rot/UB_c = 1 - theta to 4 digits; exact finite-L fidelity is UV-polluted (not a verdict) |

Phase 4 (2026-09-15): brief in phase4_brief.md; status PHASE4_STATUS.md; numerics ../numerics/optimality_all/e0_*.py, e2_*.py.
Phase 5 (2026-09-15): brief in phase5_brief.md; status PHASE5_STATUS.md; tracks F1 (exact_optimum_tangent_problem.tex), F2/F3 numerics ../numerics/optimality_all/f2_*.py, f3_*.py.
| exact_optimum_tangent_problem.tex | 27 | F1 (Phase 5): exact chart of F ((X,Z) in F iff N = 1 - XX* >= 0, 0 <= Y = Z - X Q_BB X* <= N; X = (1-N)^{1/2} V, V co-isometry iff 1 not an eigenvalue of N); first-order defect with noise; tangent problem; KKT sign criterion at the isometric optimum (M_* = Herm((t_* Q)_DD) >= 0 and >= tau_* = (t_*)_DD, plus one-sided endpoint conditions after repair R10); S10 multiplier dictionary; theta as a geometry-free Wiener-Hopf constant in the modular frame (Prop 6.2); refereed (referee_exact_optimum_tangent_problem.tex): stands with repairs R1-R15, Thm 3.11(3) cone equality FAILS (inclusion only) |
| referee_exact_optimum_tangent_problem.tex | 16 | REF-P5-1: verdict table Sec. 11, repairs R1-R15 Sec. 12, undeclared assumptions Sec. 10; counterexample search for Thm 4.4 (a)<=>(c): none in 60 000 random triples; factor-2 in S10 (C4) adjudicated (see errata_log.md) |
| referee2_exact_optimum_tangent_problem.tex | 7 | REF-P5-3: repairs R1-R15 verified applied; new finding S1 — the reduction of the endpoint condition (e) to the two model boundary directions is proved only for vector fields (hypothesis H3 declared); repairs S1-S6; E(zeta_inf) = 2 lambda (1-theta) g_Q recomputed correct |
| referee3_exact_optimum_tangent_problem.tex | 4 | REF-P5-4: repairs S1-S6 verified; H3 usage sound; document accepted; residual D1-D3 on the H3 wording (equivalence clause, Thm 3.11(3) statement vs proof, ambient space of the decomposition forcing alpha = 0) |

| network_corner_calculus.tex | 42 | G1a (Phase 6, O10): corner calculus of sequential one-sided recovery — S(Phi) = -2 sum kappa_k delta_{p_k} under hypothesis (H) (Thm 5.3) and the unconditional displaced-mass rule (Thm 5.2, counterexamples 5.5/5.6, one correcting W1's wording); recovered state depends only on S(Phi) (Thm 6.3); single-corner universality (Cor 6.5); vacuum rigidity so exact recovery never occurs when the last step keeps a non-empty part (Thm 7.3); VWZ 1(B) = 1(A) literally, Protocol 3 = Phi_A(zeta_eff) with s' > 2 lambda' (Thm 8.5); holonomy = starting block, all protocols for n = 4, 5 with distinctness (Prop 9.1, Lem 9.2); amplification (Lem 10.1); modular identity for zeta_k and e^{Delta} <= 1 + 2/zeta (Lem 10.3); separation bound e^{Delta} >= 2/eps PROVED, sharp as eps -> 0 (Thm 11.1); type-III sequential bound W6 in the angle form under Uhlmann's standard-form hypothesis (Thm 12.5) and in the chordal form with no hypothesis (Thm 12.6), so the second-order bound is unconditional; twirled mixture (Prop 13.1); repairs after REF-P6-3 in Sec. 15; numerics g1a_calculus.py, g1a_separation.py |

Phase 6 (2026-09-16): brief in phase6_brief.md; status PHASE6_STATUS.md; tracks G1a (network_corner_calculus.tex), G1b (network_second_order.tex), G2/G3 numerics ../numerics/networks/.

Public presentation (2026-09-21): plan in public_site_plan.md — README with figures, interactive site on GitHub Pages, generated docs/ subfolder.
