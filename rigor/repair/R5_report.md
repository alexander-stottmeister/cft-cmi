# R5 report — repair round 2026-11-19 — paper 2 (patch file rigor/repair/R5_patch.json over paper2/*.tex)

## FILES
- rigor/repair/R5_patch.json: 38 items over 10 paper2 files (main.tex, sec_intro, sec_setting, sec_universality,
  sec_implementation, sec_kubo_mori, sec_boson, sec_outlook, sec_second_variation, app_conventions); `check_patch.py` 0 problems.
- rigor/repair/R5_report.md (this file).
- Compile test: `check_patch.py rigor/repair/R5_patch.json --stage <scratchpad>/R5/stage`, pdflatex main.tex twice in
  stage/paper2: no `^!` line, no undefined reference/citation; 26 pages (25 before).

## KB
No card added or changed (none required for seat R5). `kb -p cft_cmi lint`: 0 issues, 0 awaiting review
(22 dependency/locator warnings, pre-existing).

## FINDINGS
- [BREAK, confirmed] C2 F3b: paper2 lem:ext proof applied eq:H1loc to the C^{1,1} map phi (U(phi) undefined). Patched:
  lem:ext restated for class E of RigorC Def. 2.1 and s >= 0, proof = C11 Thm 4.7 <1>7 (lem:loc(i) + thm:H1(iii) + Trotter).
- [GAP, confirmed, same defect, not listed by C6] paper2 prop:geom applied eq:H1loc to U(phi'_tau), phi'_tau the flow of a
  C^{1,1} h. Patched: hypothesis ||h||_{3/2} < infinity, membership in M' from lem:loc(i).
- [MINOR, confirmed, not listed] paper2 thm:H1(ii) said "for every s"; C11 l. 555 proves it for s >= 0. Patched.
- [BREAK (overclaim), confirmed] C2 F1: title/intro/outlook "Petz recovery". Patched to the geometric compression.
- [GAP, confirmed] C6 B1: bracket proved for D(omega_s||omega) (RK l. 601, 704), eq:s2 is D(omega||omega_s). Patched
  at all 5 occurrences (abstract, intro, two in sec_kubo_mori, app table).
- [GAP, confirmed] C6 B6 / C2 F2: Moebius reduction for general nets. Patched; also the boson section's a = 1, L = 2
  normal form (zeta = s/3) rests on the same uncarded reduction for the U(1) current net [MINOR, new].
- [MINOR, confirmed] C6 B2 (both mislabelled headers, s2 p-dependence), B3, B4, B5, B7 (DIT; also: CDIT's Outlook
  states the extension for "some h" only), B8, B9; D2 = P1, P3, P4, P5, P6 (P6 confirmed by hand: with
  e^{-ipx} the conjugate sits on g^, so the displayed <JJ> uses e^{+ipx}).
- No council item of my scope was found unconfirmed.

## ITEM TABLE
item | file:line | old claim | new claim | card [status] | disposition
C2 F1 | main.tex:19, :29; sec_intro.tex:7; sec_outlook.tex:2 | "Petz recovery error" | error of the geometric zero-collar compression; Petz identification free fermion only | petz-zero-collar-channel [proved], thm-b-universality [refereed] | patched (items 0-3)
C6 B9 + A7 + P10 | sec_outlook.tex:2, :14-19 | "the zero-collar Petz recovery"; asks Phi <= f2 z^2(1+Cz); c3 = -0.99(1) | compression = t -> infinity; proved Phi <= -1/2 log(1-2 f2 z^2) on [0, pi sqrt3); c3 "about -1, unreproduced" | rrr-bound-small-zeta [proved], rate-of-remainder [proved], remainder-c3-c4-values [heuristic] | patched (3, 4)
C6 B4 | sec_intro.tex:12 | c = 1/2 per Majorana component | r complex (Dirac) fermions, c = r | (paper1 convention) | patched (5)
C6 B1 | main.tex:41; sec_intro.tex:76; sec_kubo_mori.tex:127, :141; app_conventions.tex:77 | bracket on "D" | bracket on D(omega_s||omega), reversed order | conj-s2 [conjectural] | patched (6-10)
C2 F3/F3b | sec_setting.tex:116-119, :153-173 | lem:ext, any C^{1,1} extensions, all s, via U(phi) | class E, s >= 0, C11 <1>7 proof | implementer-hypotheses [refereed] | patched (11-13)
C2 F3 (thm:H1) | sec_implementation.tex:120 | (ii) for every s | (ii) for s >= 0 | implementer-hypotheses [refereed] | patched (14)
C2 F3 (prop:geom) | sec_universality.tex:71, :76, :85-88; sec_kubo_mori.tex:105 | U(phi'_tau) for C^{1,1} h | ||h||_{3/2} < inf, lem:loc(i) | thm-b-universality [refereed] | patched (15-18)
C6 B6 / C2 F2 | main.tex:32; sec_setting.tex:43-45; app_conventions.tex:51 | zeta = cross ratio, every net | half-line normal form; general reduction rests on rigor/moebius_reduction_general_nets.tex (under review) | mobius-reduction-cross-ratio [proved, free fermion] | patched (19-21)
C6 B2 | sec_boson.tex:77, :86, :92 | headers 3.04/3.77; "not fitted"; s2 1% | headers 3.41/4.14; fitted exponents; s2 depends on p | boson-check [numerical] | patched (22-24)
C6 B3 | main.tex:42; sec_intro.tex:87 | c-linearity "proved analytically" | "analytic second-order computation (not a refereed proof)" | boson-check [numerical] | patched (25-26)
C6 B5 | sec_universality.tex:318-322 | additivity because ||T(g)Omega||^2 adds | from thm:B and c = c1 + c2, A1 (x) A2 assumed in the class | thm-b-universality [refereed] | patched (27)
C6 B7 / P2 | sec_implementation.tex:218-222; sec_outlook.tex:37-39; main.tex:102 | DIT result as fact | via CDIT Outlook (PDF p. 24), DIT not obtained, unused | none | patched (28-31)
C6 B8 / P7 | sec_universality.tex:282-283 | "known in the models ..." | dropped; (BW1) named | thm-b-universality [refereed] | patched (32)
P1 | sec_setting.tex:28 | c-linearity uses locality | uses neither | thm-b-universality | patched (33)
P3 | sec_second_variation.tex:55 | \cite[S(B)]{RigorSV} | Prop. 5.2 | bures-three-faces | patched (34)
P4 | sec_kubo_mori.tex:141 | unnamed hypothesis | (V), RK Def. 4.3; (U_eps) fails, RK Prop. 4.1 | conj-s2 | patched (35)
P5 | sec_kubo_mori.tex:67 | \cite[S5]{RigorKM} | S5, Thm 5.9 with Thm 5.8 | km-exact-identity | patched (36)
P6 | sec_boson.tex:12 | Fourier convention unstated | e^{+ipx} in sec_boson, stated | boson-check | patched (37)
P8 | sec_universality.tex:294-308 | thm:B assumes (H1)-(H3) then declares itself unconditional | - | thm-b-universality | deferred: restructuring, author decision (referee_paper2 marked it so)
P9 | rigor/universality_theorem_B.tex | - | - | - | already repaired (l. 614), not paper2

## PROPOSED CARD CHANGES
- conj-s2, Statement: "bracket 0.034 c <= liminf s^-2 D <= limsup <= 0.924 c" -> "bracket for the REVERSED relative
  entropy, 0.034 c <= liminf s^-2 D(omega_s||omega) <= limsup s^-2 D(omega_s||omega) <= 0.924 c (kubo_mori_gauge_lemma.tex
  eq:final l. 601, eq:lowerb l. 704); the conjecture s2 = c/12 concerns D(omega||omega_s), and no argument converts one
  into the other at second order (U_s not in M)". Reason: C6 B1.
- boson-check, Statement: "c-linearity of the vacuum overlap proved analytically at second order" -> "computed analytically
  at second order (paper2/sec_boson.tex eq:clin; not refereed as a proof)"; append "s2 = 0.083(2) rests on the p = 1 tail
  law: free p gives 0.0810-0.0824, p = 2 gives 0.0782-0.0785 (boson_recovery.out l. 42, 56, 70)". Reason: C6 B2, B3.
- thm-b-universality, Statement: after "-log F = (s^2/8) g_B + o(s^2)" insert "in the half-line chart A = (-inf, 0), where
  zeta = s". Reason: C2 F2 [MINOR].
- paper2-status: note after the orchestrator applies R5_patch.json: "P1-P7, P10 applied (repair round 2026-11-19); P8
  deferred; 26 pp". Reason: C6 D2.

## NUMBERS
- 26 pages: `pdflatex main.tex` (twice) in the staged copy, log line "Output written on main.pdf (26 pages ...)".
- All numbers inserted into the paper are quoted from existing outputs, none newly computed: s2 fits 0.0810-0.0824
  (free p), 0.0838-0.0842 (p = 1) from numerics/boson/README.md:98; p = 2 values 0.0784621/0.0781738/0.0782506 from
  numerics/boson/boson_recovery.out:42, 56, 70; raw 0.0763220 at kappa_c = 5.24 (out:54); table values from out:48-52.

## NOT DONE
- P8 (restructuring thm:B) deferred, author decision.
- rigor/moebius_reduction_general_nets.tex is R2's deliverable; the paper sentences cite it as "under review" only.
- Not re-derived: the c-linearity computation eq:clin (only relabelled as a computation); the "0.2%" wording for f2 left as written.

## NEEDS ORCHESTRATOR
- Apply rigor/repair/R5_patch.json (`check_patch.py ... --apply`), recompile paper2, commit.
- B6: the patched sentences rest on rigor/moebius_reduction_general_nets.tex (R2, under review); if R2 ends conjectural,
  reword main.tex/sec_setting/app_conventions accordingly. The boson normal form a = 1, L = 2 also depends on it.
- Execute the PROPOSED CARD CHANGES (conj-s2, boson-check, thm-b-universality, paper2-status); coordinate with R2 on
  the (H1) form (paper2 keeps eq:H1loc for smooth phi only, CDIT axiom; no paper2 argument now applies it to a C^{1,1} map).
- Decide P8.
