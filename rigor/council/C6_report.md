# C6 report — Papers and bookkeeping (REF-COUNCIL-C6, Opus)

Scope: paper1/*.tex, paper2/*.tex against the KB; `kb deps --check` warnings; proved cards with unrepaired referee items.

## 1. Verdict lines (one per paper theorem)
Verdict on each paper statement against its card (my scope is papers vs KB; the mathematics of the proofs is C1-C5's).
Paper 1:
- thm:LX (Longo-Xu CMI) — STANDS (card longo-xu-cmi, proved; scope remark rem:LX-scope correct).
- thm:tracenorm, thm:normal, lem:tensorization, lem:fidbelow — STAND as transcriptions of card petz-zero-collar-channel.
- lem:mobius, thm:fidfd, prop:relentfd, prop:secondorder, thm:detrep — STAND (cards mobius-reduction-cross-ratio,
  quasi-free-fidelity-formula, quasi-free-second-order-fidelity-expansion).
- prop:tail — STANDS WITH REPAIR: typeset as a Proposition, pointwise O(kappa^-5) on no card; relabel (A9).
- cor:collapse, prop:monotone — STAND WITH REPAIR (wording "best member", A10; monotonicity proof only internal, D1 item 12).
- thm:main (limit) — STANDS (thm-a-quadratic-law, refereed). eq:unconditional — STANDS WITH REPAIR: no card (A8a).
- thm:lower, thm:upper, prop:gBvalue — STAND (constants recomputed, c6_constants.out); rem:hellinger h2 — no card (A8b).
- rem:norate (i) global bound — FAILS as worded (no range; proved only on zeta < pi sqrt 3) (A6).
- prop:twobranch — FAILS as stated for a general 2D CFT (card conjectural); STANDS for F_r x F_r / Dirac (A1);
  its O(eta_V^3) remainder FAILS (only o(eta^2) proved) (A2).
- Abstract last sentence ("three decades ... 1e-4") — FAILS (A3). Intro D = (c/12) zeta^2 + o — FAILS (A5).
  Outlook O4 "not optimal" as fact — FAILS as worded (numerical) (A12).
Paper 2:
- thm:B, thm:linear, thm:value, thm:impl, thm:H1, thm:H23, thm:secvar, thm:three — STAND against cards (thm-b-universality,
  implementer-hypotheses refereed; second-variation-lemma, bures-three-faces proved); abstract's general-configuration
  reading — STANDS WITH REPAIR (Moebius reduction for general nets on no card, B6).
- thm:kmexact, thm:kmlower, thm:kmupper — STAND (km-exact-identity). s2 bracket — STANDS WITH REPAIR: it is for
  D(omega_s||omega), the conjecture and numerics for D(omega||omega_s) (B1).
- cor:tensor — STANDS WITH REPAIR (proof line, B5). eq:bosonvals — STANDS (numerical, checked, B2), eq:clin — numerical
  card carries a proved claim (B3).

## 2. Findings (most severe first)
No BREAK of a theorem's mathematics was found in my scope; the BREAKs are paper sentences stronger than their cards.
- [BREAK, paper] paper1/sec_2d_lattice.tex:4-39 + main.tex:43-46 — prop:twobranch stated for every 2D CFT; card
  two-chirality-law-general-cft is conjectural (Phi_c exists only for the free fermion) (A1).
- [BREAK, paper] paper1/sec_2d_lattice.tex:29-35, sec_intro.tex:113 — "+O(eta_V^3)": only o(eta^2) proved; lower
  remainder rate on no card (A2).
- [BREAK, paper] paper1/main.tex:47-48 — "numerics ... over three decades confirm the quadratic law to 1e-4": the 1e-4 is
  the f2 coefficient with a heuristic tail correction; Phi itself is known to 0.3-1% and is not quadratic for zeta >= 1 (A3).
- [BREAK, paper] paper1/sec_intro.tex:70-73 — D = (c/12) zeta^2 + o(zeta^2) asserted; card conj-s2 conjectural (A5).
- [BREAK, paper] paper1/sec_outlook.tex:72-74 — "It is not optimal among all normal recovery maps" as fact; theta > 0 is
  numerical (A12).
- [BREAK, paper, low impact] paper1/sec_quadratic.tex:243-247 — global remainder bound without range; proved on
  zeta < pi sqrt 3 only (A6).
- [GAP] paper2 abstract/intro/sec_kubo_mori + card conj-s2 — s2 bracket proved for D(omega_s||omega), not D(omega||omega_s) (B1).
- [GAP] c3 = -0.99(1), c4 = +0.9(1) quoted with error bars, no script in the project (A7).
- [GAP, KB] eq:unconditional and h2 = 2 log2 f2 have no card (A8); prop:tail pointwise (A9); Moebius reduction for
  general nets (B6); rate-of-remainder and tail-bound proved on heuristic/conjectural/numerical depends (A6, A11);
  4 assumes-chains missing (C1-C7).
- [MINOR] A4, A10, A11, A13, A14, B2-B5, B7-B9, C8 locators, D1-D2 unapplied wording edits.

## 3. Table: paper statement | card | status | ok?
| paper statement (file:line) | card | status | ok? |
|---|---|---|---|
| P1 thm:LX, CMI = (r/6) log(1+z) (sec_setting:77) | longo-xu-cmi | proved | ok |
| P1 thm:tracenorm ||Q-Q~||_1 = (r/2pi) log(1+zeta) (sec_petz:81) | petz-zero-collar-channel | proved | ok |
| P1 thm:normal, normal *-iso at zero collar (sec_petz:107) | petz-zero-collar-channel | proved | ok |
| P1 lem:mobius, Phi depends on zeta only (sec_fidelity:22) | mobius-reduction-cross-ratio | proved | ok |
| P1 thm:fidfd / prop:secondorder (sec_fidelity:58, 85) | quasi-free-fidelity-formula / quasi-free-second-order-fidelity-expansion | proved | ok |
| P1 prop:tail, pointwise kappa^-3 + O(kappa^-5) (sec_fidelity:207) | none (tail-bound covers the integrated tail) | — | NO (A9) |
| P1 eq:expansion-structure c3 = -0.99(1), c4 = 0.9(1) (sec_fidelity:236) | remainder-c3-c4-values | heuristic | wording ok, error bars not (A7) |
| P1 cor:collapse / prop:monotone (sec_fidelity:248, 271) | two-chirality-law / phi-monotone-in-zeta | proved | ok up to A10 |
| P1 thm:main limit = c/(12 pi^2) (sec_quadratic:23) | thm-a-quadratic-law, const-f2 | refereed / proved | ok |
| P1 thm:main eq:unconditional Phi <= tau/(1-tau) (sec_quadratic:36) | none | — | NO card (A8a) |
| P1 prop:gBvalue g_B = 2r/(3pi^2), g_KM = r/6 (sec_quadratic:100) | const-gb | proved | ok (recomputed) |
| P1 rem:hellinger h2 = 2 log2 f2 (sec_quadratic:228) | none | — | NO card (A8b), value recomputed ok |
| P1 rem:norate global bound, no range (sec_quadratic:244) | rrr-bound-small-zeta (zeta < pi sqrt3); rate-of-remainder | proved (range-limited) | NO (A6) |
| P1 intro D = (c/12) zeta^2 + o(zeta^2) (sec_intro:70) | conj-s2 | conjectural | NO (A5) |
| P1 Table 1 row D: "form proved; identification numerical" (sec_intro:99) | const-gb + conj-s2 | proved / conjectural | ok |
| P1 prop:twobranch for A_chiral x Abar_chiral (sec_2d:13) | two-chirality-law-general-cft | conjectural | NO (A1) |
| P1 prop:twobranch for Dirac / F_r | two-chirality-law | proved | ok |
| P1 eq:twobranch-small + O(eta^3) (sec_2d:29; intro:113) | thm-a-quadratic-law (o only) | refereed | NO (A2) |
| P1 minimum at lambda = 0 "proved only at leading order" (sec_2d:27) | two-chirality-minimum-at-lambda-zero | conjectural (b) | ok |
| P1 lattice exponents 1.986..1.151, ratio 1-0.15/L (sec_2d:97-115) | two-branch-law-lattice | numerical | ok; card stale on "22-5000" (A4) |
| P1 large-zeta values (sec_2d:125; tab:largezeta) | large-zeta-values | numerical | ok |
| P1 certified enclosures (sec_numerics:51) | certified-numerics | numerical | ok |
| P1 abstract "three decades ... 1e-4" (main:47) | const-f2 (f2^num), certified-numerics | numerical | NO (A3) |
| P1 f2^num = 0.008444(1), s2^num = 0.0837(5) (sec_numerics:83) | const-f2 / conj-s2 | proved / conjectural (numbers numerical) | ok |
| P1 O4 "not optimal among all normal recovery maps" (sec_outlook:72) | compression-not-second-order-minimiser, compression-not-optimal-exact-fidelity | numerical | NO (A12) |
| P1 outlook theta = 0.384 +- 0.003, theta_fr >= 0.38 numerical (sec_outlook:102) | theta-value | numerical | ok |
| P1 outlook all-channel = quasi-free SDP (sec_outlook:102) | all-channel-equals-quasi-free, all-channels-symbol-feasible | proved | ok |
| P1 outlook E_rec <= (1-theta_fr) f2 z^2 (sec_outlook:102) | compression-not-optimal-exact-fidelity / uhlmann-upper-half-proved | numerical / proved | ok |
| P2 thm:B f2 = c/(12 pi^2) every net (sec_universality:294) | thm-b-universality (+ implementer-hypotheses) | refereed | ok (normal form; B6) |
| P2 thm:impl / thm:H1 / thm:H23 (sec_implementation:115-166) | implementer-hypotheses, c11-extension-implementer | refereed / proved | ok |
| P2 thm:secvar / thm:three (sec_second_variation:26, 116) | second-variation-lemma, bures-three-faces | proved | ok |
| P2 thm:linear / thm:value (sec_universality:177, 220) | thm-b-universality, const-gb-general-nets | refereed / proved | ok |
| P2 thm:kmexact / kmlower / kmupper (sec_kubo_mori:19-64) | km-exact-identity | proved | ok |
| P2 gauge lemma refuted, inf = (11+5 sqrt5) c/12 (sec_kubo_mori:73-141) | km-gauge-lemma-refuted | refuted | ok (locator C) |
| P2 s2 bracket 0.034c..0.924c (abstract, intro:76) | conj-s2 | conjectural | order of D wrong (B1) |
| P2 boson f2 = 0.00844(2), s2 = 0.083(2) (sec_boson:87) | boson-check | numerical | ok (checked, B2) |
| P2 eq:clin c-linearity of the overlap "proved analytically" (sec_boson:118) | boson-check | numerical | status mismatch (B3) |
| P2 cor:tensor additivity (sec_universality:318) | none (follows from thm-b) | — | proof line (B5) |
| P2 stress-tensor normalisation <TT> = c/(8pi^2)(x-y-i0)^-4 (app_conventions) | stress-tensor-normalisation | proved | ok |

## 4. `kb -p cft_cmi deps --check` warnings: real or not
See §C below (8 dependency warnings: 7 real bookkeeping gaps, 1 honest-vacuous; 14 locator warnings: 3 real, 11 harmless; plus 2 proved->heuristic/numerical depends edges the checker misses).

## 5. Proved/refereed cards whose evidence document has an unrepaired referee item
See §D below (paper1: 9 of 13 proposed referee edits unapplied, none a BREAK; paper2: P1-P8, P10 unapplied, P9 repaired).

## 6. Abstract / introduction overclaims
Abstract/intro overclaims, paper 1: A1 (two-branch law for every 2D CFT), A3 (three decades / 1e-4), A5 (D expansion asserted), intro:113 O(eta^3) (A2). Paper 2: abstract bracket without argument order (B1); abstract "zeta the cross ratio" for general configurations (B6); abstract "analytic proof of the c-linearity of the vacuum overlap" sits on a numerical card (B3). Paper 2 abstract and intro are otherwise faithful to the cards (s2 a conjecture, gauge lemma refuted, bracket conditional).

## 7. NOT DONE
- Mathematics of the cited rigor documents not re-derived (C1-C5 scope); verdicts here are paper-vs-card and paper-vs-source-sentence.
- Per-document referee reports rigor/referee_*.tex not re-audited for unapplied items (only referee_paper1.md, referee_paper2.md).
- FHSW (eq:fhsw and the averaged form eq:zero-collar-bound) not checked against the PDF: C3's scope.
- paper1 app_proofs.tex, app_conventions.tex and fidelity_tables.tex only spot-checked (cross-ratio conversions verified:
  eta_V = 1 - eta, z = 1/eta - 1 = eta_V/(1-eta_V)); paper2 sec_setting.tex, app_conventions.tex not read in full.
- Did not compile the papers (no edits made; the §4 log check is the orchestrator's after repairs).
- Environment: the scratchpad venv lacks numpy and pymupdf (brief §7 says rebuilt); scripts ran on /usr/local/bin/python3
  (numpy 2.5.2, scipy 1.18.1, mpmath).

---
## A. Paper 1 — detailed findings (worked file-first; summarised in §§1-3 above)

A1. [BREAK, paper] paper1/sec_2d_lattice.tex:4-39 (prop:twobranch) and abstract main.tex:43-46, intro sec_intro.tex:79-85.
  Quoted: "Let A = A_chiral (x) Abar_chiral be a two-dimensional CFT with chiral halves of central charges c and cbar ...
  Then -log F^(lambda) = Phi_c(z(1+e^{-pi lambda})) + Phi_cbar(z(1+e^{pi lambda}))" — typeset as a Proposition with a proof.
  Card two-chirality-law-general-cft is CONJECTURAL; only the massless Dirac case is proved (card two-chirality-law).
  The tensor-product hypothesis of the paper settles the factorisation item (i) of the card, but NOT item (ii): a
  per-chirality function Phi_c and the collapse cor:collapse exist only for the free fermion (the proof, l. 46, cites
  cor:collapse, a free-fermion statement; for a general chiral net only f2 = c/(12 pi^2) is known, Theorem B).
  The abstract says "in a two-dimensional CFT ... the recovery error is a sum of two branches" with no qualifier.
  Repair: restrict prop:twobranch to A_chiral = F_r (r complex fermions per chirality; Dirac for r = 1), state the
  general-CFT version as a conjecture, and qualify the abstract/intro sentences accordingly.
  Inherited by: paper1 abstract, intro eq:twobranch-intro, rem. after prop:twobranch; KB unaffected (cards correct).

A2. [BREAK, paper] paper1/sec_2d_lattice.tex:29-35 (eq:twobranch-small) and sec_intro.tex:113-114.
  Quoted: "-log F^(lambda) = f2 eta_V^2 [2+4cosh(pi lambda)+2cosh(2 pi lambda)] + O(eta_V^3)" and
  "-log F^(0) = (c+cbar)/(3 pi^2) eta_V^2 + O(eta_V^3)". Theorem A (card thm-a-quadratic-law) gives only
  Phi = f2 zeta^2 + o(zeta^2). Card rate-of-remainder gives the ONE-SIDED bound Phi - f2 zeta^2 <= f2^2 zeta^4/(1-2 f2 zeta^2)
  (upper direction only); no card gives a lower bound Phi - f2 zeta^2 >= -C zeta^3 (c3 = -0.99(1) is card
  remainder-c3-c4-values, HEURISTIC, scripts not in the repository). Direction ledger: O(eta^3) needs BOTH directions for
  the exact Phi; only the upper one is proved. The proof (l. 50-53) says "Expanding with thm:main", which yields o(eta^2).
  Repair: replace O(eta_V^3) by o(eta_V^2) in both places (or "(1+o(1))"), as card two-chirality-minimum-at-lambda-zero (b)
  already writes it. Inherited by: paper1 intro l. 113-114, prop:twobranch; card const-f2 quotes 8 f2 eta^2 without a rate (ok).

A3. [BREAK, paper] paper1/main.tex:47-48 (abstract, last sentence).
  Quoted: "High-precision numerics for Phi over three decades of cross ratio confirm the quadratic law to 10^{-4} relative."
  The 10^{-4} figure is f2^num = 0.008444(1), 12 pi^2 f2^num = 1.0001(1) (sec_numerics.tex:82-86), a second-order
  coefficient extracted from the first-order kernel via prop:secondorder with the tail correction that sec_numerics.tex:37
  itself calls "heuristic" — it is not a statement about Phi over three decades. The Phi values carry "a realistic
  uncertainty of 0.3-1%" (sec_numerics.tex:46-47); for zeta >= 1 (the third decade) Phi is not quadratic at all
  (local log-slope 1.29 -> 0.69, rem:largezeta) and only brackets are quoted. Card const-f2 states "numerically
  0.008444(1) for c = 1" (numerical value of the coefficient), no card states a 1e-4 confirmation of Phi over three decades.
  Repair: "The second-order coefficient extracted numerically agrees with c/(12 pi^2) to 10^{-4} (heuristic tail
  correction), and Phi(zeta)/zeta^2 approaches it over 0.008 <= zeta <= 0.53 within 0.3-1%."

A4. [MINOR] paper1/sec_2d_lattice.tex:111-115 (L2): "the single-branch expression ... is off by factors between 4 and 7600";
  card two-branch-law-lattice says "off by factors 22-5000". The paper number is the referee's correction
  (rigor/referee_paper1.md §6 item 2, from petz_lattice.out); the CARD is stale and should be updated (KB fix). Also "i.e. the law
  is exact in the continuum limit and the deviation is a pure finite-size effect" states as fact an extrapolation of
  a fit 1-0.15/L at finitely many L (§5 of AGENTS.md: extrapolation is an estimate, not a result). Repair: "consistent with".

A5. [BREAK, paper] paper1/sec_intro.tex:70-73. Quoted: "The corresponding relative-entropy coefficient is
  D(omega||omega~_s) = (c_cft/12) zeta^2 + o(zeta^2); the Kubo--Mori half is proved here at the level of the quantum Fisher
  information and confirmed numerically". This asserts the expansion of D as a fact. Card conj-s2 is CONJECTURAL; the
  only bracket is 0.034 c <= liminf s^-2 D <= limsup <= 0.924 c, itself conditional at both ends (Gaps RK1, RK2).
  The paper's own rem:s2-status (sec_quadratic.tex:253-266) and Table 1 (sec_intro.tex:99) say it correctly
  ("numerically confirmed conjecture"). Also "proved at the level of the quantum Fisher information" is wrong in kind:
  what prop:gBvalue proves is the value of the Kubo-Mori FORM g_KM = r/6 (card const-gb), not a Fisher-information
  statement about D. Repair: "is conjecturally c/12: the Kubo-Mori quadratic form of the curve equals c/12 (proved) and
  D/zeta^2 follows it numerically to 0.5%".
  Same defect, milder: sec_quadratic.tex:19-20 (def:gB) DEFINES g_KM "normalized by D(omega||omega~_s) = (zeta^2/2) g_KM
  + o(zeta^2)", which presupposes the unproved expansion [MINOR; define g_KM as the form of eq:km].

A6. [BREAK, paper; low impact] paper1/sec_quadratic.tex:243-247 (rem:norate (i)) and sec_fidelity.tex:240.
  Quoted: "the exact identity of step (iii) gives ||V_s||_2^2 <= s^2 ||P_- D P_+||_2^2, hence the global bound
  Phi(zeta) <= -1/2 log(1 - 2 f2 zeta^2)" — no range is stated, so it is read on the whole natural range
  zeta < (2 f2)^{-1/2} = pi sqrt 6 = 7.70. The group bound needs equal singular values of the two off-diagonal blocks
  (index zero), proved only for |s| ||[P_-,K]||_2 < 1 (rate_of_remainder.tex Correction C3); card rrr-bound-small-zeta
  (proved) has the range zeta < (4 f2)^{-1/2} = pi sqrt 3 = 5.44; the rest rests on card group-index-zero-large-s
  (CONJECTURAL) and pushforward-blocks-equal-singular-values (HEURISTIC). Repair: add "for zeta < pi sqrt 3".
  The c3-sign and no-log^-2 consequences are small-zeta statements and survive.
  Bookkeeping corollary [GAP, KB]: card rate-of-remainder is status PROVED while depends lists a heuristic and a
  conjectural card; its Statement splits the ranges honestly, but by AGENTS.md §3 (weakest status) the unrestricted
  item (2) should be moved to its own conjectural card or the card restricted to the settled range (as rrr-bound does).

A7. [GAP, paper] paper1/sec_fidelity.tex:236 (eq:expansion-structure) and sec_quadratic.tex:246.
  Quoted: "c3 = -0.99(1), c4 = +0.9(1)". Card remainder-c3-c4-values is HEURISTIC with "scripts not in the repository";
  the paper itself says "not yet reproducible from the published scripts". A number with an error bar that no script
  in the project reproduces violates AGENTS.md §5 (every reported number from a script inside the project) and the
  paper's own Provenance standard ("numerical means a measurement with a stated error bar"). Repair: remove the error
  bars and say "a numerical estimate, about -1, unreproduced", or restore the script. Also eq:expansion-structure displays
  an integer-power expansion whose existence is unproved; the text calls it "the heuristic reason to expect", ok.

A8. [GAP, KB bookkeeping] paper1 statements with NO card:
  (a) sec_quadratic.tex:36-40, eq:unconditional, typeset as part of thm:main: "unconditionally for all zeta with
      tau(zeta) < 1, Phi(zeta) <= tau/(1-tau)". Source: rigor/quadratic_limit.tex:807-852 (thm:upper there). No card
      (kb q --text, grep 'tau' over claims: none). AGENTS.md §2: "A paper draft states a result only after its card exists."
  (b) sec_quadratic.tex:228-233, rem:hellinger: "h2 = r log2/(6 pi^2) = 2 log 2 f2" (quadratic_limit.tex:943 prop:h2).
      No card. Also "even the existence of the limit was open" before thm:upper — historical, fine.
  Not a defect in the mathematics as far as checked; a missing card.

A9. [GAP, paper] paper1/sec_fidelity.tex:207-217 (prop:tail) is typeset as a Proposition with "O(kappa^{-5})" pointwise;
  rem:tail-status (l. 219) says the argument in Note 5 "is a sketch" and that RigorTB proves only the INTEGRATED tail
  |Sigma(kappa_c) - zeta^2/(15 kappa_c^2)| <= C2 zeta^2 kappa_c^-3 + ... with C2 finite. The pointwise O(kappa^-5)
  statement is on no card. By the paper's own convention (Provenance: "Statements are labelled by status throughout")
  a Proposition reads as proved. Repair: relabel "Claim (sketch)" or restate as the integrated bound of RigorTB Thm 4.2.

A10. [MINOR] paper1/sec_fidelity.tex:256-261 (cor:collapse): "its best member is the limit t -> +infinity" — the
  limit is not a member (card two-chirality-law says so explicitly: "a limit point and not a member of the family");
  "worse than the optimal rotation by a factor 4" — no rotation attains it. Repair: "infimum over the family, attained
  only in the limit". sec_intro.tex:78 says it correctly ("worse than the limit t -> infinity").

A11. [MINOR] card tail-bound (KB): status PROVED while depends lists tail-constants-numerical and
  phi-below-0085-zeta2-numerical (both NUMERICAL). The card splits (a) proved shape / (b) explicit constants numerical,
  and the paper (rem:tail-status, sec_numerics.tex:51, main.tex RigorTB bibitem) states the split correctly. Also part
  (a)'s hypotheses T < 1, Y < 1 are verified on the admissible region only with the numerical inputs of (b).
  Repair (KB): split the card, or note that (a) is the conditional statement "if T < 1 and Y < 1".

A12. [BREAK, paper] paper1/sec_outlook.tex:72-74 (O4). Quoted: "It is *not* optimal among all normal recovery maps
  F_r(AB) -> F_r(ABC)". Stated as fact, emphasised. Cards: compression-not-second-order-minimiser (NUMERICAL: "theta > 0
  is numerical, not proved") and compression-not-optimal-exact-fidelity (NUMERICAL: theta_fr > 0 iff E_D u E_D != 0 is
  proved, but that E_D u E_D != 0 / theta_fr >= 0.38 is numerical). The paper's own later paragraph (l. 102: "theta_fr >= 0.38
  (numerical)") is correct; O4 is not. Repair: "is not optimal (numerical: theta = 0.384 +- 0.003)".
  Same item: "theta = 0.384 +- 0.003 numerically \cite{RigorS10,RigorF3}" — RigorS10 gives 0.300, a taper-suppressed lower
  bound, not 0.384 [MINOR citation]. l. 102 end: "the Petz map, at 4 f2 z^2, is at least 5.6 times worse than the best
  channel" — 5.6 = 4/0.71 is the pre-Phase-5 bracket (card paper1-status note of 2026-09-15: bracket 0.71 -> 0.616); with
  0.616 the factor is 4/0.616 = 6.49. "At least 5.6" stays true but is stale, and rests on numerical theta [MINOR].
  Direction ledger: Petz = 4 f2 z^2 (1+o(1)) per chirality (equality, Thm A, exact quantity); best channel
  <= 0.616 f2 z^2 (1+o(1)) (upper bound, exact fidelity, numerical input). The ratio direction Petz/best >= 6.49 holds
  asymptotically in z only.

A13. [MINOR, consistency between the papers] paper1/sec_outlook.tex:4-49 says the universality argument has "Two gaps
  ... from a theorem" and (O3) a bosonic check "would test" universality; paper 2 (thm:B, refereed card thm-b-universality)
  closes the Bures gap and card boson-check (numerical) exists. Paper 1 understates; it does not overclaim. Also
  sec_outlook.tex:4-5 attributes "s2 = c/12" to prop:gBvalue as a constant "obtained here" — it is the KM FORM value; see A5.

A14. [MINOR] paper1/main.tex bibitem VWZ: "S. Vardhan, A. Wei, Y. Zou"; paper2/main.tex:133: "S. Vardhan, Z. Wei, Y. Zou".
  The source PDF refs/VWZ_2307.14434.pdf p.1 reads "Shreya Vardhan, Annie Y. Wei, and Yijian Zou": paper 2 is wrong
  (Z.), paper 1 is right up to the middle initial.

---
## B. Paper 2 — detailed findings

B1. [GAP, paper2 + card conj-s2] Argument-order drift in the relative-entropy bracket.
  paper2 abstract (main.tex), sec_intro.tex:76 and sec_kubo_mori.tex:126-128, 141 quote
  "0.034 c <= liminf s^-2 D <= limsup s^-2 D <= 0.924 c" as the bracket for s2, where eq:s2 (sec_kubo_mori.tex:5) defines
  s2 through D(omega || omega_zeta) (vacuum FIRST), as does paper 1 (def:gB, rem:s2-status, Table 1) and the numerical
  fermion value 0.0837(5) (prop:relentfd with Q1 = vacuum symbol). The source of the bracket, rigor/kubo_mori_gauge_lemma.tex,
  proves both ends for the REVERSED order: cor:final eq:final l. 601 "limsup D_M(omega_s || omega)/s^2 <= 0.92418 c",
  and l. 704 "liminf D_M(omega_s || omega)/s^2 >= ...". In type III no argument in the documents converts
  D(omega_s||omega) into D(omega||omega_s) at second order (for an inner automorphism of M one could swap s -> -s,
  but U_s is not in M, which is the whole point of Gap QK2). So the bracket, even granting its hypotheses (V)/RK1 and
  RK2, brackets a different functional than the conjecture s2 = c/12 and the numerics. Statement not shown false
  (at second order in finite dimensions both orders give the Kubo-Mori form), hence GAP.
  Repair: write D(omega_s||omega) in the bracket everywhere (abstract, intro, sec_kubo_mori, card conj-s2), and either
  prove the order swap at second order or state that the bracket concerns the reversed relative entropy.
  Inherited by: card conj-s2 (statement "liminf s^-2 D" without order), paper 2 abstract and intro, card paper2-status.

B2. [MINOR, transcription] paper2/sec_boson.tex:76-83 (window table) and numerics/boson/README.md:92-93: the columns
  headed kappa_c = 3.04 and 3.77 carry the values of kappa_c = 3.41 and 4.14 of basis N=120, sigma=1.6
  (numerics/boson/boson_recovery.out:49, :51: f2 = 0.0083508, s2 = 0.0724870; f2 = 0.0083832, s2 = 0.0745522); the true
  values at 3.04 / 3.77 are 0.0083252 / 0.0083699 (f2) and 0.0711232 / 0.0736471 (s2) (out:48, :50). The mislabelled table
  is non-monotone in its increments and, refitted as printed, gives s2 = 0.0750-0.0839 depending on the fit (PART A of
  rigor/council/c6_boson_extrap.out). Repair: relabel the two headers.
  Independent check of eq:bosonvals (rigor/council/c6_boson_extrap.py, output .out beside it; tolerance fixed in the
  script before the run: quoted interval): on the three bases of boson_recovery.out, f2 fits (free p, p = 2, p = 2 on the
  3 finest, p = 2 + next order) give 0.008426-0.008457, all inside 0.00844(2) up to the edge (quoted +-2e-5, measured
  spread 3.1e-5): ok. s2: every fit with the Kubo-Mori tail exponent p = 1 (or free p = 1.14-1.39) gives 0.0810-0.0842,
  inside 0.083(2); fits with p = 2 give 0.0782-0.0799, outside. The quoted s2 therefore rests on the p = 1 tail law,
  which the paper derives heuristically ("the discarded per-mode weight decays like kappa^-3") — but also says "The
  different exponents are expected, not fitted" while the quoted values come from free-exponent fits. The raw value at
  the finest window is 0.0763 (8.4% below 1/12). "Agreement at the 1% level" for s2 is an extrapolation-dependent
  statement, single method [MINOR: state the p-dependence]. The script reproduces the free-p values 1.39 / 1.14 / 1.18
  and 0.08099 / 0.08240 / 0.08213 of boson_recovery.out:42, :56, :70 exactly (my 9-point kappa_c >= 2.3 window).

B3. [MINOR, KB] card boson-check is status NUMERICAL but its Statement contains "c-linearity of the vacuum overlap proved
  analytically at second order" (paper2/sec_boson.tex:101-127, eq:clin; also abstract and sec_intro.tex:87-88). A proved
  claim on a numerical card has no proof locator and was not refereed as a proof. Repair: own card (proved, doc:
  paper2/sec_boson.tex#eq:clin or its rigor source), or call it "computed" in the paper.

B4. [MINOR] paper2/sec_intro.tex:11-12: "In Paper 1 we computed the defect exactly for the chiral free fermion (c = 1/2
  per Majorana component)". Paper 1 treats r COMPLEX fermions, c = r (paper1 sec_intro.tex:27); no Majorana net appears
  there. Not wrong (complex = two Majorana), but the conventions of the two papers should agree (app_conventions).

B5. [MINOR] paper2/sec_universality.tex:318-322 (cor:tensor): the stated reason "||T(g_tot) Omega||^2 adds" does not prove
  additivity of g_B, which is a DISTANCE to cl (M1 (x) M2)'_sa Omega, not ||T(g)Omega||^2. The corollary follows at once
  from thm:linear + thm:value if A1 (x) A2 is in the class (g_B = (c1 + c2) gamma_0). Repair the one-line proof.

B6. [GAP, bookkeeping] paper2 abstract: "the recovery error obeys -log F = c/(12 pi^2) zeta^2 + o(zeta^2), zeta the cross
  ratio of the four endpoints", for every net and (implicitly) every adjacent configuration. thm:B is proved only in the
  half-line normal form A = (-inf, 0) (sec_universality.tex:296-300, "zeta = s in this normal form"). The reduction of a
  general configuration (a < inf) to the normal form for a general net is the Moebius reduction, whose card
  (mobius-reduction-cross-ratio) is stated "For the chiral free fermion". The free-fermion proof (paper1 lem:mobius) uses
  only Moebius covariance of the vacuum and of the construction, so it likely transfers — but no document or card states
  it for general nets. Repair: one lemma in paper 2 (or extend the card's scope after a referee pass).

B7. [MINOR, NOT OBTAINED source used as fact] paper2/sec_implementation.tex:218-222 ("(b) Fock representations with
  integer c. By \cite{DIT} (via the Outlook of \cite{CDIT}), U^(n,h) extends to D^sigma(S^1) for sigma > 2 ... This is
  strictly stronger than thm:impl for those models") and sec_outlook.tex:37-39 (networks: "the implementation half
  generalises directly", via DIT). DIT is NOT OBTAINED (rigor/referee_paper2.md P2, unapplied); the bibitem
  (paper2/main.tex:102) carries no caveat. Not used in thm:B. Repair: mark the bibitem and both sentences.

B8. [MINOR, unverified claim] paper2/sec_universality.tex:282-283 (rem:varform): "This is a gap ... it is known in the
  models where (H1)-(H3) were first verified" — referee_paper2.md P7 could not locate it; still present. Not used in thm:B.

B9. [MINOR, stale] paper2/sec_outlook.tex:2: "Thm B computes the error of *the* zero-collar Petz recovery" — thm:B is about
  the compression k_s (paper 1's s = lambda endpoint, not the ordinary Petz map s = 2 lambda); sec_outlook.tex:14-19 asks
  for an upper bound Phi <= f2 zeta^2 (1 + C zeta) although card rrr-bound-small-zeta already proves the stronger
  Phi <= -1/2 log(1 - 2 f2 zeta^2) on zeta < pi sqrt 3; and repeats c3 = -0.99(1) (A7 applies).

---
## C. `kb -p cft_cmi deps --check` (run 2026-11-19: 0 errors, 8 dependency + 14 locator warnings = 22)

Dependency warnings (8):
 C1-C3. kkt-noise-criterion-numerics (NUMERICAL, assumes H3 only) uses kkt-noise-sign-criterion (assumes H1, H2, H3) and
   tangent-problem-exact-parametrisation (assumes H1). REAL (bookkeeping, not mathematics): the card's interpretive
   statements ("orbit = global optimum iff (a) and (e)", "under H3, (e) follows ...") are Thm 4.4 of
   exact_optimum_tangent_problem.tex, which needs H1 and H2 as well; only the raw lambda_min / E(zeta) numbers are free
   of them. Repair: add assumes: tangent-h1-gq-differentiability, tangent-h2-minimiser-localisation.
 C4-C7. tangent-sdp-noise-directions (NUMERICAL, assumes nothing) uses the same two cards. REAL in the same sense: the
   SDP is "the fixed-geometry tangent problem", whose relation to the exact second-order problem is H1 (card
   tangent-problem-exact-parametrisation) and whose optimality reading is Thm 4.4 (H1-H3). The SOLID outputs (orbit-only
   value 1 - theta to 1.1e-7) do not need them. Repair: assumes H1 (and H2, H3 for any optimality reading).
 C8. sequential-recovery-angle-form-under-u (PROVED, assumes the REFUTED hypothesis-u-natural-cone-fidelity): NOT a defect
   — the card's title and Statement say "vacuous: (U) is refuted"; a proved implication with a false hypothesis is
   honest. Cosmetic: status superseded would stop the warning. No paper cites it (grep paper1/ paper2/: none).
Locator warnings (14): whole-file doc tokens. Harmless on lesson/decision/superseded/active cards (cross-ratio-conventions,
 fidelity-formula-correction, note3-collar-removal-programme x2, notes-errata, open-problems-plan-note8, paper1-status,
 paper2-status, rigor-pipeline, strategy-note-6: 10). REAL on three research claims, AGENTS.md §2 ("grep -n finds LOC"):
 compression-not-optimal-exact-fidelity (its third token doc:rigor/findings_entries.tex; the first two carry labels
 thm:main, cor:sandwich of exact_fidelity_upper_half.tex, so only the extra token is unlocated), conj-s2 and km-gauge-lemma-refuted (doc:rigor/kubo_mori_gauge_lemma.tex whole file; the REFUTED card
 must point at the disproof: sec. "The gauge problem, solved exactly", kubo_mori_gauge_lemma.tex:527-545). [MINOR x3]
Not caught by --check (found here): rate-of-remainder (PROVED) depends on group-index-zero-large-s (CONJECTURAL) and
 pushforward-blocks-equal-singular-values (HEURISTIC) — see A6; tail-bound (PROVED) depends on two NUMERICAL cards — A11.
 The checker evidently flags only `assumes` chains, not proved -> {conjectural, heuristic, numerical} `depends` edges;
 that is a tool gap worth a claude-team-knowledge card (orchestrator).

---
## D. Proved/refereed cards whose evidence document has an unrepaired referee item

D1. paper1-status (active; next: "Apply the 13 proposed wording edits of rigor/referee_paper1.md"). Status of the 13
  (rigor/referee_paper1.md §6, l. 212-279) against paper1/ today: APPLIED 1 (abstract KM wording, but see A5 for the
  intro), 2 (L2 factors 4-7600; the CARD two-branch-law-lattice still says "22-5000": stale card, not the paper — A4
  corrected accordingly), 6 (internal bibitems marked). NOT APPLIED: 3 (rem:largezeta quotes the weaker kappa_c = 18.4
  lower bounds, sec_2d_lattice.tex:128-130), 4 (def:gB cites lem:legendre for Omega(l), sec_quadratic.tex:11),
  5 ("-x^2 d/dx", sec_quadratic.tex:194), 7 (named locators 'Upper bound', 'Value of the Hellinger coefficient'),
  9 (prop:tail header cites only the sketch, = A9), 11 (tab:summary row zeta >~ 1, sec_intro.tex:101), 12 (prop:monotone
  proved only in RigorCN5, sec_fidelity.tex:271-281), 13 (quadrature diagnostics unattributed, sec_numerics.tex:19-21);
  8 partially. None of the unapplied items is a BREAK; 12 matters for publication (cor:collapse's monotonicity clause and
  prop:twobranch rest on a proof not in the paper).
D2. paper2-status: rigor/referee_paper2.md §"Edits proposed" P1-P8, P10 unapplied (P2 = B7, P7 = B8); P9 (inverted factor
  in universality_theorem_B.tex step <1>2, evidence of thm-b-universality) IS repaired (l. 614, "corrected 2026-09-09").
D3. thm-b-universality, implementer-hypotheses, thm-a-quadratic-law: no unrepaired item found in the referee reports
  read here (paper reports only; the per-document reports rigor/referee_*.tex are C1-C3's scope and were not re-audited).

A2 addendum [MINOR]: paper1/sec_2d_lattice.tex:53-54 "at lambda = 0 the bracket is 8 and 8 f2 = 2c/(3 pi^2) per chirality"
  — 8 f2 eta^2 is the sum of BOTH chiralities (2 x 4 f2); per chirality it is 4 f2 = c/(3 pi^2). The displayed
  (c + cbar)/(3 pi^2) is right; the phrase "per chirality" is wrong (card const-f2 says "with both chiralities ... 8 f2").

---
## E. Numbers recomputed by this seat
- Closed forms of paper 1 (g_B = 2/(3 pi^2), g_KM = 1/6, h2 = log2/(6 pi^2), int tanh(pi k)/(k(k^2+1)) = 2, f2 = 0.00844343,
  h2/f2 = 2 log 2): mpmath quadrature at 40 digits, max |diff| = 2.3e-41 < tol 1e-25. Command:
  `${PYTHON:-python3} rigor/council/c6_constants.py` -> rigor/council/c6_constants.out. Also 4/0.616 = 6.494, 4/0.71 = 5.634 (A12).
- Boson extrapolations (B2): `${PYTHON:-python3} rigor/council/c6_boson_extrap.py` -> rigor/council/c6_boson_extrap.out.
  f2 spread 0.008426-0.008457 over 4 fit families x 3 bases; s2 0.0810-0.0842 for p = 1 / free p, 0.0782-0.0799 for p = 2.
  Single method (the project's own boson_recovery.out data; refits, not a new boson computation).
