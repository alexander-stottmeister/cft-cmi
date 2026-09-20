# Referee report — public-site-plan (REF-SITE-1, 2026-09-21).  VERDICT: FAIL
## 1. Coverage claim — false (fatal)
`kb q`: proved 30, refereed 3, numerical 21 (+1 numerical finding in evidence/).  "33" is exactly 30+3, so it counts **no**
headline numerical, yet the table names eleven (large-zeta-values, certified-numerics, boson-check, theta-value,
all-channel-optimum-value, compression-not-second-order-minimiser, gap-law, thermal-shielding, rg-c-function,
two-branch-law-lattice, circle-model-taper-suppresses-theta).  Definition and count contradict; the set is >= 44.  All 41
named ids exist; circle-model-taper-suppresses-theta is an evidence-folder finding, not a claim, so not in the 21 either.
Nine of the 33 proved/refereed claims appear in **no** module row, only module 10's catch-all: second-variation-lemma,
sequential-recovery-bound-type-iii, quasi-free-fidelity-formula, w-hat-mellin-formula, all-channels-symbol-feasible,
tangent-problem-exact-parametrisation, single-observable-bound, kkt-noise-sign-criterion, ac-lower-bound-zero.  So "the
mapping is explicit so the coverage can be checked rather than asserted" does not hold.
## 2. Premises — true unless noted
Four PNGs exist, are public-tracked, both generating scripts survive (petz_lattice.py, petz_thermal_rg.py); `*.pdf`
gitignored (.gitignore:18); fidelity_tables.tex, fidelity_table_largezeta.tex, F3_RESULTS.md (h^0.77 l.142, taper Sec. 5),
numerics/boson/, paper1|paper2/app_conventions.tex, phase6_brief.md:13-45 all present with the data claimed; the two
non-building documents are named right (\lqed arity l.486; undefined \one l.364); C3 correct.  Slips: README is 80 lines,
not 77; the file is `numerics/results_hp2.txt`; module 2's "10^-3 to 20" exceeds the data (0.0083-17.07); F3's
"c-linearity" is Theorem B — every measured point (fermion, boson, lattice) is at c = 1; module 7's 2/eps is not attained
(exact min exceeds it by 2.2% at eps = 0.3, sharp only as eps -> 0).  sources.md cannot say "every external result relied
upon": REFERENCES.md's table has 36 rows, refs/ holds 47 PDFs, 14 absent, 4 bullet-only (restore.sh parses the table only).
## 3. Closed forms — cheap, and that is the problem for module 6
Longo-Xu, Moebius composition and the gamma-recursion are trivial in JS, so Thm 5.2 (unconditional, with the G_m'(x_m) factor
and corner swallowing) is no harder than the (H) form.  Yet the plan names neither (H) nor Thm 5.2.  (H) fails for single-interval starts (209/400) and union conditioning (199/400); in all 408 failures the naive
corner measure is wrong ("add D on C, then A on BC" displaces the mass off the junction, 71% of the naive total).
"two different protocols produce literally the same map" is literal only for VWZ 1(A)=1(B) and for orders within one
starting block; Protocol 3 equals the Theorem-A map only up to a global Moebius (literal difference 0.68).
## 4. Status honesty
One badge per module cannot serve module 4: six proved cards beside all-channel-optimum-value (numerical, conditional on
H1-H3; (a) fails in every finite run, (e) vacuous at zeta_0), and it omits kkt-noise-sign-criterion and
kkt-noise-criterion-numerics, the two cards carrying the conditionality.  Module 5's circle-model-taper-suppresses-theta has
never been refereed (REF-AUTHOR-1).  Needed: badges per displayed claim, a distinct `conditional` badge naming its hypotheses, unreviewed cards withheld or
badged `unreviewed`.  The README already says "conditional on three stated hypotheses" and "under a stated hypothesis", so
the plan is a regression; its outline also drops the README's "Status vocabulary" section, on which C5 depends.
## 5. Omissions and decisions
No CITATION.cff/DOI/archival plan though D2(b) calls Releases "cleanest for citation"; no .github/ and no workflow path
named; `plan_page/petz_program_plan.html` is public-tracked, frozen at "Status (10 Sep)", contradicts the new site, never
mentioned.  D2(c) contradicts the hosting choice: Pages serves docs/ from main, so CI-built `docs/pdf/` must be committed
and `*.pdf` blocks it without a second exception.  `make check` needs SOURCE_DATE_EPOCH and svg.hashsalt to be
reproducible; 3 MB holds only with a woff2-only KaTeX subset (full dist ~5.5 MB).  The four decisions are the right four but
incomplete: add D5, whether unreviewed and conditional cards may be published before a referee pass.
