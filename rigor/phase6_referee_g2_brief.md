# Referee brief REF-P6-6 — G2's lattice chains and its six cards (2026-10-03)

## 1. Role
Referee. `KB_ACTOR=REF-P6-6`, every kb command `-p cft_cmi`, model Opus. Workspace root
/Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root); project root
/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths below relative to it). Never git, never ./pgit, never
edit a reviewed script, output or card text (§1: only `kb verdict`, `kb note`, `kb set ID evidence=` for a wrong
locator). Stance: adversarial; the burden of proof is on the scripts, outputs and cards. Reruns write ONLY into your
own files rigor/ref_p6_6_*, never onto numerics/networks/*.

## 2. Object
Under review: numerics/networks/lattice_chain.py, numerics/networks/NETWORK_RESULTS.md, outputs validate.out,
prec.out, N1.out ... N6.out, raw data vwz_{A,B,C,G}.raw, chains_{D,E,F,H,I}.raw (track G2, brief rigor/phase6_g2_brief.md).
Cards under verdict (`kb -p cft_cmi show ID` after `kb -p cft_cmi summary`; read the Notes first): lattice-vwz-1b-equals-1a,
lattice-protocol3-equals-theorem-a, lattice-vwz-protocol-ratios, lattice-lr-chains-cross-terms,
lattice-general-rule-where-h-fails, lattice-vwz-bounds-equal-block-chains [all numerical]; and the two G1a cards that
G2's notes re-opened, corner-calculus and frame-strength-amplification [proved]: verdict on whether the Statement is
still true and the G2 note accurate. Report only (no verdict) on G2's notes on vwz-protocol-ordering and
network-second-order-law. Context (not under review): rigor/phase6_brief.md ("Setting and conventions", W1, W4);
numerics/lattice/petz_lattice.py and README.md (dictionary: two chiralities, -log F_lat -> 2 Phi_cont; `recovered_G`,
`fid_relent` are an independent mpmath path); rigor/network_corner_calculus.tex (thm:general, thm:corner, ex:swallow,
prop:1B1A, prop:prot2, thm:prot3, lem:ampl, lem:LRdata, thm:w6chord, cor:w6-second); refs/VWZ_2307.14434.pdf Sec. 5
((5.3)-(5.5), (5.9)-(5.11), p. 44 note; the PDF, never memory); paper1/sec_numerics.tex table l. 116 and petz_lattice
`PHI_TAB`/`phi_cont`; G3's agreed kernel values on card corner-kernel-two-frames (under review by REF-P6-5).
Status file: rigor/PHASE6_STATUS.md (section "G2 result" lists G2's deviations from its brief).

## 3. Deliverable: rigor/referee_lattice_chain.tex (verdict document, `\input{rigor_preamble}`) + rigor/ref_p6_6_*.py/.out
Checklist (one verdict line each; every number of a card Statement recomputed or reproduced):
 1. Model and dictionary: the code applies, at each step, the Gaussian Petz map of the step's own inclusion to the state
    produced so far (Gaussian composition rule of petz_lattice.py); VWZ lambda = 0 = our s = 2 lambda_geom; two
    chiralities (-log F_lat -> 2 Phi_cont); eta = VWZ (5.9). Read lattice_chain.py's protocol definitions against VWZ
    Sec. 5 (which block conditions on which, in which order) for 1(A), 1(B), 2, 3.
 2. V0 (validate.out): 23 cases, exact 2^n in particle-number sectors, the fixed tolerances; rerun `validate` into
    rigor/ref_p6_6_validate.out and diff. Independent check: one two-step protocol at n <= 20 through petz_lattice's
    mpmath path (`recovered_G`, `fid_relent`) in your own script vs G2's flint value (tolerance 1e-10).
 3. N1: the claimed operator identity (rho_BC^{-a} rho_BC^{a} = 1 between the two steps of 1(B)): derive it from the
    Petz-map formula in petz_lattice.py's docstring; does the card say correctly that this validates the union-
    conditioning pipeline and does NOT test the continuum prop:1B1A?
 4. N2: zeta_eff = (sigma_1 + sigma_2) beta_I(p_3) = 2a/b (recompute exactly from phase6_brief W1(ii)); the matched
    single step a'/b' = 2a/b; Q2 = 1.0001(21), 1.0006(29), 0.9999(19): re-fit from the .raw data with your own fit code
    (fits 1/L + 1/L^2 and h^p; admissibility 1e-4 on the 4 finest); Q1 against paper 1's tables: check the interpolation
    claim (linear log-log underestimates Phi_A by 0.65-1.8 % between nodes; quadratic removes the deviation) on the
    table nodes yourself; is the card's wording about Q1 the weakest the evidence supports?
 5. N3: exact corner data zeta_1 = a/b, zeta_2 = a(a+2b)/(2b(a+b)), zeta_3 = a/b, e^{Delta_23} = 1/eta (G1a prop:prot2 /
    lem:LRdata; recompute); R31 vs Phi_A(2a/b)/Phi_A(a/b) "within 0.7 %" (your interpolation of the tables); R21 values
    and the Ghat-free part (zeta_2^2 + zeta_3^2)/zeta_1^2; the estimator X = (R21 - P21)/(2 zeta_2 zeta_3/zeta_1^2) and
    its labels ("lattice estimate of Ghat(3.00)/Ghat(0)" only at eta = 0.05, "second order not yet reached" elsewhere);
    X = 0.281(5) vs G3's 0.2951: is the 3-sigma deficit disclosed and correctly attributed (not explained away)? The
    statement "Phi1 < Phi2 < Phi3 in all 26 rows" and the direction of VWZ (5.10) f' < f from the PDF.
 6. N4: the brief's "weak corners" premise is false for geometric chains (zeta = 0.49-1.04 by lem:LRdata: recompute);
    the card must not present N4 as a test of the second-order law; Phi_tot / sum Phi_step ratios re-fitted from
    chains_*.raw; "chordal bound Thm 12.6 holds, max ratio 0.8695": identify the exact inequality (thm:w6chord in Bures
    DISTANCE, direction) and recompute the ratio from the saved values; the amplification factors 1 + z' = 1.06-1.19.
 7. N5: (a) Ex. 5.6: the degenerate first step P_{A2 -> A2A3}(rho_{A2}) = rho_{A2A3} is exact (Petz map recovers the
    state it is built from): verify from the formula; "exactly on the lattice" vs "0 in double precision" wording.
    (b) REF-P6-0 geometry (1.3, 2.1, 0.9, 1.7), degenerate second step: recompute the displaced corner from Thm 5.2
    with your own exact code: strength zeta = 1.2351 at x/T = 0.4300, and the naive value 2.1407 at p_3; lattice/
    prediction 1.0012(4) vs 0.4988(2) re-fitted from the .raw data.
 8. N6: the direction of VWZ (5.3)-(5.5) (lower bounds on -log F in terms of CMIs? read the PDF) and the a fortiori
    argument -log max_lambda F <= -log F^(0); b23 vs (5.11): -(1/6) log((1-eta)/(1+eta)); chain rule 1e-16; equal-block
    Phi_tot values reproduced from N6.out; are any of these "results" or only bounds checks (card wording)?
 9. Fits and digits (§5): three resolutions minimum; 0-dof fits flagged; digits stable across the two finest
    resolutions; uncertainty = spread of admissible fits; where only one resolution exists, "not extrapolated".
10. Deviations from the brief and process (status-file section "G2 result"): sizes up to 189 (orchestrator accepted);
    production sweeps started before V0 was complete (all 23 passed); N4 premise; N5(b) variant; one read-only `git
    status` (rule §1) -- each disclosed where it matters?
11. Cards: every Statement against the outputs (quantities, ranges, resolutions, digits, "lattice"/"continuum" labels);
    every evidence locator resolves; `depends`/`related` accurate; the G2 notes on corner-calculus and
    frame-strength-amplification (verdict on those two cards), on vwz-protocol-ordering and network-second-order-law
    (report only).
Reruns: `PYTHONDONTWRITEBYTECODE=1 PYTHON=$V/bin/python $V/bin/python numerics/networks/lattice_chain.py <task>` for
validate, N1 and N5 (reading the saved .raw where the task only post-processes), output redirected to
rigor/ref_p6_6_rerun_<task>.out; do not repeat sweeps that need more than 20 minutes -- time one small run and say so.

## 4. Conventions: rigor/phase6_brief.md "Setting and conventions"; numerics/lattice/README.md; NETWORK_RESULTS.md
"Conventions and conversions" (check each conversion written there).

## 5. Working results: W2, W4 of rigor/phase6_brief.md and the Statements of vwz-protocol-ordering,
network-second-order-law are UNREFEREED; G1a's theorems (refereed) are citable with locators.

## 6. Output paths (the only files you may create): rigor/referee_lattice_chain.tex and its pdflatex by-products;
rigor/ref_p6_6_*.py, rigor/ref_p6_6_*.out.

## 7. Environment
V=/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/venv
(numpy, scipy, mpmath, python-flint; no sympy). Scripts read `PYTHON` else python3, paths from `_ROOT`. Over 2 min:
nohup ... & disown, output in rigor/; else Bash timeout <= 600000 ms. No `timeout` binary; absolute paths; cwd drifts.
REF-P6-4 and REF-P6-5 run in parallel: at most 2 cores.

## 8. Verdicts, rules, report
- Per card: `KB_ACTOR=REF-P6-6 kb -p cft_cmi verdict ID pass` (STANDS) or `... verdict ID fail --note "<repair,
  locator>"` (STANDS WITH REPAIR or FAILS). Competing verdicts as a new note; never edit a referee note.
- File first: report skeleton (one section per checklist item, PENDING) within your first 3 tool calls; appends <= 100
  lines / 12,000 characters, compile after each (pdflatex twice from rigor/; log without `^!` or undefined references;
  report the page count). Chat <= 5 lines; reason only to the next tool call.
- Stop and report on every §9 trigger (VWZ PDF not openable; a hypothesis you cannot check).
- Final message: at most 400 words; one line per card and per checklist item, failures first, each with reason and
  locator; `kb -p cft_cmi lint` counts; NEEDS ORCHESTRATOR.
