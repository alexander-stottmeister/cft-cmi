# R4 report — Paper 1 repairs (repair round 2026-11-19, KB_ACTOR=R4, Opus)

## FILES
- rigor/repair/R4_patch.json — 47 patch items over 8 files of paper1/ (main, sec_intro, sec_2d_lattice, sec_fidelity,
  sec_quadratic, sec_numerics, sec_outlook, fidelity_tables). `python3 rigor/repair/check_patch.py rigor/repair/R4_patch.json`
  -> "47 items, 8 files, 0 problems".
- rigor/repair/R4_report.md — this file.
- Compile test: `check_patch.py ... --stage <scratchpad>/R4/stage` (plus numerics/fidelity_table_largezeta.tex copied to
  stage/numerics/ for the `\input{../numerics/...}`), pdflatex x3 on stage/paper1/main.tex: no `^!` line, no undefined
  reference/citation; 30 pages (unpatched paper: 29). Stage is in the scratchpad only; no _stage_ file in the project.

## KB
No card added or changed (brief §1). `kb -p cft_cmi lint`: 0 issues, 0 awaiting review (22 deps/locator warnings, pre-existing).

## FINDINGS
- Every C6 item A1-A14 confirmed at its file:line except as noted; no item rejected as "not confirmed".
- [MINOR] C4 F2 says the largest computed finite-mesh theta is 0.37635 (h = 0.015); numerics/optimality_all/F3_RESULTS.md
  (iii) table lists 0.37893 for family D (circle mesh, 1/L = 1/2048). Both are < 0.38, so C4's conclusion stands; the
  patch says "every computed finite-mesh value lies below 0.38".
- [MINOR] Card two-chirality-law (proved) covers only the massless Dirac fermion (r = 1 per chirality). C6 A1 suggested
  restricting prop:twobranch to F_r (r complex fermions); r > 1 is on no card, so the patch restricts to Dirac (c = cbar = 1).
- [MINOR] rem:norate / card rrr-bound-small-zeta are for ONE chiral component; the patched range is "r = 1 and
  0 <= zeta < pi sqrt 3"; for r > 1 the bound is on no card (Phi_r = r Phi_1 does not give -1/2 log(1 - 2 r f2 zeta^2)).
- [MINOR] D1 item 12: the paper's proof sketch of prop:monotone (semigroup law h_{s'} = h_{s'-s} o h_s) is NOT the argument
  of card phi-monotone-in-zeta (restriction to a subalgebra at fixed L, s, varying a). Patched to the card's argument.
- [MINOR] D1 item 10: the corrected value depends on the row used: Lambda=120/kmax=45 -> 0.08337, kmax=90 -> 0.08339,
  Lambda=240 -> 0.08325; the patch names the kmax=45 rows (those that also reproduce the caption's 0.0841).
- [MINOR, KB] card two-branch-law-lattice still says "22-5000"; the paper's "4 and 7600" is the referee's correction (A4).

## ITEM TABLE
| item | file:line | old claim | new claim | card [status] |
|---|---|---|---|---|
| C6 A1 | sec_2d_lattice:3-60, main:45-46, sec_intro:79 | two-branch law for every 2D CFT (Proposition) | Proposition for the massless Dirac fermion; general CFT = new rem:twobranch-general (conjecture, two missing inputs) | two-chirality-law [proved]; two-chirality-law-general-cft [conjectural] |
| C6 A2 | sec_2d_lattice:32,34; sec_intro:113-114 | + O(eta_V^3) | + o(eta_V^2), eta_V -> 0 at fixed lambda, not uniform | thm-a-quadratic-law [refereed]; two-chirality-minimum-at-lambda-zero (b) [conjectural, item (b) proved part] |
| C6 A2 add. | sec_2d_lattice:53-54 | 8 f2 = 2c/(3pi^2) "per chirality" | sum of both chiralities, 4 f2 each | const-f2 [proved] |
| C6 A3 | main:47-48 | Phi over three decades confirms quadratic law to 1e-4 | f2^num agrees to 1e-4 (heuristic tail corr.); Phi on 0.008-0.53 to 0.3-1% | const-f2 [proved; value numerical] |
| C6 A4 | sec_2d_lattice:111-113 | law exact in continuum, pure finite-size effect | "consistent with", extrapolation of a fit | two-branch-law-lattice [numerical] |
| C6 A5 | sec_intro:70-73; sec_quadratic:19-20 | D = (c/12) zeta^2 + o, "proved at QFI level"; def:gB normalises g_KM by D | conjecturally c/12; KM form value proved; def:gB: expansion of D open | conj-s2 [conjectural]; const-gb [proved] |
| C6 A6 | sec_quadratic:244; sec_fidelity:240; sec_outlook:56-57 | global bound, no range | r = 1, 0 <= zeta < pi sqrt 3 | rrr-bound-small-zeta [proved] |
| C6 A7 | sec_fidelity:238,241; sec_quadratic:244 | c3 = -0.99(1), c4 = +0.9(1) | c3 ~ -1, c4 ~ +0.9, unreproduced, no error bar | remainder-c3-c4-values [heuristic] |
| C6 A8a,b | sec_quadratic:36-40, 228-233 | eq:unconditional, h2 = 2 log2 f2 on no card | no paper change; two new cards proposed (below) | none (proposed) |
| C6 A9 / D1-9 | sec_fidelity:207-217 | Proposition, pointwise O(kappa^-5) | Remark "proof sketch only", integrated form RigorTB Thm 4.2 | tail-bound [proved, integrated form] |
| C6 A10 | sec_fidelity:256-261; sec_outlook:71-72 | "best member is the limit"; "optimal rotation" | infimum attained only in the limit (not a member); factor 4 at leading order | two-chirality-law [proved] |
| C6 A11 | KB only | tail-bound proved on numerical depends | card change proposed; paper already states the split | tail-bound [proved] |
| C6 A12 / C4 F1 | sec_outlook:72-74, 102 | "not optimal" / "not the minimiser" as fact; 0.384 cited to S10 | "Numerically, ..."; 0.384 cited to RigorAll, F3; S10's 0.300 = taper-suppressed | compression-not-second-order-minimiser, compression-not-optimal-exact-fidelity, theta-value [all numerical] |
| C4 F2 | sec_outlook:102 | theta_fr >= 0.38 (numerical) | + "extrapolation over finite meshes, every computed value < 0.38, not a rigorous bound" | compression-not-optimal-exact-fidelity [numerical] |
| C4 F3 / A12 | sec_outlook:102 | Petz at least 5.6 times worse | >= 4/0.62 ~ 6.4 at leading order in z, numerical input | compression-not-optimal-exact-fidelity [numerical] |
| C6 A13 | sec_outlook:4-5 | s2 = c/12 of prop:gBvalue | KM form value g_KM/2 = c/12; identification with s2 conjectural. "Two gaps"/O3 vs paper 2: deferred (needs a paper-2 bibitem and R2's (H1) form) | const-gb [proved]; conj-s2 [conjectural] |
| C6 A14 | main:110 | A. Wei | A. Y. Wei (refs/VWZ_2307.14434.pdf p.1) | — |
| D1-1 | main:42-43 | — | already applied | conj-s2 |
| D1-2 | sec_2d_lattice:114 | — | already applied (4-7600); card stale, see below | two-branch-law-lattice [numerical] |
| D1-3 | sec_2d_lattice:128-130; sec_numerics:158-159 | kappa_c = 18.4 lower bounds | kappa_c = 39.1/43.8 bounds of tab:largezeta (checked vs results_largezeta_certified.txt) | large-zeta-values [numerical] |
| D1-4 | sec_quadratic:11 | Omega(l) of lem:legendre | eq:Omega-ell of prop:oneparticle | const-gb [proved] |
| D1-5 | sec_quadratic:194 | -x^2 d/dx | -(x^2/L) d/dx | — |
| D1-6 | main:96-106, 83 | bibitems marked: already applied; inert \bibliographystyle | removed | — |
| D1-7 | sec_quadratic:223, 231 | named locators | Thm 6.3, Prop 6.5 (quadratic_limit.aux:53,59) | — |
| D1-8 | sec_fidelity:220-224 | Sigma constants without hypotheses | for 0 < zeta <= 1, kappa_c >= 8 (tail_bound.tex:61) | tail-bound [proved] |
| D1-10 | fidelity_tables:16 | 0.0833 | 0.0834 (rows Lambda=120, kmax=45) | conj-s2 (value numerical) |
| D1-11 | sec_intro:101 | brackets, rem:largezeta, lower bounds + extrapolation | tab:largezeta, rigorous lower bounds + uncertified extrapolation, 0.45-6.6% | large-zeta-values [numerical] |
| D1-12 | sec_fidelity:274-280 | proof only cited (semigroup sketch) | card's restriction argument written out, cites RigorCN5 Prop 8.1 | phi-monotone-in-zeta [proved] |
| D1-13 | sec_numerics:18-21 | diagnostics unattributed | attributed to Note 5 Sec. 6 (fidelity_recovered_quasifree.tex:441), uncertified | — |

## PROPOSED CARD CHANGES
1. two-branch-law-lattice, Statement: "a single-branch law is off by factors 22-5000" -> "a single-branch law is off by factors
   between 4 and 7.6e3 (growing with lambda and 1/eta_V; exactly 2 at lambda = 0), numerics/lattice/petz_lattice.out [2]/[6]".
   Reason: C6 A4 / referee_paper1.md 6.2; the paper already prints 4-7600.
2. NEW card (orchestrator, `kb add`): `phi-unconditional-linear-bound` [proved], "For the r-component free chiral fermion,
   for all zeta with tau(zeta) = (r/2pi) log(1+zeta) < 1, Phi(zeta) <= tau/(1-tau)", evidence doc:rigor/quadratic_limit.tex#thm:upper
   (l. 807-856), depends petz-zero-collar-channel (thm:tracenorm), quasi-free-fidelity-formula. Reason: C6 A8a, paper eq:unconditional.
3. NEW card: `hellinger-coefficient-h2` [proved], "the second-order coefficient of the Hellinger (Powers-Stormer) functional
   -log det(S_n S~_n + C_n C~_n) along the compression curve is h2 = r log2/(6 pi^2) = 2 log2 f2", evidence
   doc:rigor/quadratic_limit.tex#prop:h2 (l. 943). Reason: C6 A8b, paper rem:hellinger. (C6 recomputed the value: c6_constants.out.)
4. tail-bound: split (a) "conditional: if T < 1 and Y < 1 then ..." [proved] from (b) explicit constants and admissible region
   [numerical, depends tail-constants-numerical, phi-below-0085-zeta2-numerical]. Reason: C6 A11.
5. compression-not-optimal-exact-fidelity, Statement: "theta_fr >= 0.38 is as well supported numerically as theta = 0.384 +- 0.003"
   -> add "(an extrapolation in h^0.77 over finite meshes; every computed finite-mesh value is below 0.38, largest 0.37893,
   F3_RESULTS.md (iii))". Reason: C4 F2. Await R3's theta_three_fits.out before fixing the digits.
6. paper1-status: next "Apply the 13 proposed wording edits" -> done by R4_patch.json once applied (items 3-13 patched; 1, 2, 6 were applied).

## NUMBERS
- 0.08337 (D1-10): `python3 -c "print((32.2*0.074268-25.3*0.071785)/6.9)"` on the printed table entries of
  paper1/fidelity_tables.tex (rows Lambda=120, kmax=45); kmax=90 rows 0.08339, Lambda=240 rows 0.08325. Arithmetic on printed
  values, no new computation; tolerance not applicable.
- 4/0.62 = 6.45 (A12/C4 F3): arithmetic on card compression-not-optimal-exact-fidelity's numerical 1 - theta_fr <= 0.62.
- Large-zeta lower bounds (D1-3) read from numerics/results_largezeta_certified.txt (e.g. 4.3812425e-03 at zeta = 1.0667,
  kappa_c = 39.14) and numerics/fidelity_table_largezeta.tex; no new run.

## NOT DONE
- A8a/A8b, A11, A4 card: KB changes, not in R4's column (brief §1); proposed above.
- A13 first part (paper 1 says "Two gaps" and O3 "would test" although paper 2 / card boson-check exist): deferred; a
  cross-reference needs a paper-2 bibitem and the (H1) form R2 is restating. Paper 1 understates, does not overclaim.
- The F_r (r > 1) two-branch law and the r > 1 range of rem:norate: on no card, not stated.
- Mathematics of rigor documents not re-derived; patches are paper-vs-card.

## NEEDS ORCHESTRATOR
- Apply R4_patch.json (`check_patch.py rigor/repair/R4_patch.json --apply`), recompile paper1 (expected 30 pages), commit.
- Execute PROPOSED CARD CHANGES 1-6 (2-3 are new cards, needing `kb q` first and a referee pass).
- Coordinate with R3: if theta_three_fits.out changes 0.384 +- 0.003, the sec_outlook theta sentences (O4, l. 102) and
  the 4/0.62 factor need a follow-up patch.
- Coordinate with R1: if index_zero.tex is refereed, the range "r = 1, zeta < pi sqrt 3" in rem:norate, sec_fidelity:240 and
  O1 can be widened.
