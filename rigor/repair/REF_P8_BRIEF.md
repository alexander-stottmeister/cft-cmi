# Referee brief REF-P8 — Theorem B stated unconditionally in paper 2 (2026-11-19)
## 1. Role
Referee, adversarial (burden of proof on the documents). `KB_ACTOR=REF-P8`, every kb command `-p cft_cmi`, model Opus.
Workspace root /Users/alex/Documents/Uni/Hannover/claude-team (AGENTS.md there binds you; kb = kb/bin/kb at that root);
project root /Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi (paths relative to it). Never git, never ./pgit,
never spawn agents, never edit a reviewed document or card text (only `kb verdict`, `kb note`).
## 2. Object
Card paper2-status (`kb -p cft_cmi summary`, then `kb -p cft_cmi show paper2-status`; read the Notes first; also
`show thm-b-universality implementer-hypotheses moebius-reduction-general-nets`). Patch under review:
rigor/repair/ORCH_patch_7.json (8 exact replacements; old/new texts) applied to paper2/sec_universality.tex (thm:B,
its proof, cor:tensor), paper2/sec_setting.tex l. 46, paper2/app_conventions.tex l. 52, paper2/main.tex l. 35,
rigor/universality_theorem_B.tex l. 93; note that three "refereed internally" strings were afterwards changed to
"reviewed internally" and the rigor one to "card moebius-reduction-general-nets, proved, review passed 2026-11-19".
Context: paper2/sec_setting.tex (ss:standing, H1-H3), paper2/sec_implementation.tex (thm:impl), rigor/referee_paper2.md
item P8, rigor/repair/REF_RP_3_report.md item on cor:tensor. Status file: rigor/repair/REPAIR_STATUS.md.
## 3. Deliverable: rigor/repair/REF_P8_report.md. Checklist, one verdict line each
1. thm:B as now stated: is every hypothesis its proof uses (lower bound prop:lower, upper bound prop:upper, thm:linear,
   thm:value, (BW), (RS), (HD), (H2')) available from ss:standing plus thm:impl with exactly the hypotheses thm:impl
   states (c > 0, separable, axioms)? Is the U_s of the statement the U_s for which thm:impl proves (H1)-(H3)? Is the
   statement now stronger than card thm-b-universality / implementer-hypotheses (e.g. sign and range of s, "every net",
   the form of (H1))? A paper sentence stronger than its card is a FAIL.
2. "No hypothesis beyond those of ss:standing is made": true of the proof chain?
3. cor:tensor: with U = U1 (x) U2 and vacuum Omega1 (x) Omega2 named, is the proof complete?
4. The four Moebius-reduction wordings: do they say no more than card moebius-reduction-general-nets (s >= 0 for every
   extension of the class; both signs for one explicit extension)? Is "reviewed internally" accurate against the card's
   review line?
5. Other places of paper 2 that still call Theorem B conditional or (H1)-(H3) assumptions of it (grep sec_intro.tex,
   main.tex abstract, sec_outlook.tex, sec_boson.tex): list inconsistencies.
6. Build: pdflatex/bibtex in a COPY of paper2 under your scratch directory (never in place): log without `^!` or
   undefined references, 26 pp. Card Statement against the facts (page count, P1-P8, P10 applied, title).
No number of a theorem statement changed, so no numerical recomputation is required; say so in the report.
## 4. Conventions: paper2/app_conventions.tex; card cross-ratio-conventions.
## 5. Working results: none; every card status is a claim under scrutiny.
## 6. Output paths: rigor/repair/REF_P8_report.md; scratch only under
/private/tmp/claude-501/-Users-alex-Documents-Uni-Hannover-claude-team-cft-cmi/7fe3011d-d839-46fb-b674-8eebe07d7cea/scratchpad/REF-P8/
## 7. Environment: pdflatex/bibtex on PATH; no `timeout` binary; absolute paths; Bash timeout <= 600000 ms.
## 8. Verdict, rules, report
`KB_ACTOR=REF-P8 kb -p cft_cmi verdict paper2-status pass` or `... verdict paper2-status fail --note "<repair, locator>"`.
File first: report skeleton with the six items PENDING within your first 3 tool calls; appends <= 100 lines; chat <= 5
lines; reason only to the next tool call. Stop on every AGENTS.md §9 trigger. Final message <= 300 words: one line per
item, failures first with locator; `kb -p cft_cmi lint` counts; NEEDS ORCHESTRATOR.
