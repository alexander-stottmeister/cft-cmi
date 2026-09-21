# Rigor audit of the cft_cmi notes — final report (state 2026-09-05, evening)

## What was done
- 7 notes (N1–N7) read in full by 6 verification agents (V1–V6, plus the x-space check P4b) writing Lamport-style step-by-step checks; 4 reference agents (R1–R4) downloaded every cited source (refs/, 39 PDFs) and cross-checked each cited statement with screenshots (rigor/shots/, ~135 images); 4 proof agents (P1–P4) attacked the open items of Note 7; 2 referees (V7, V8) checked the new proofs of P2 and P3. 19 Opus agent launches in total (18 distinct roles; P4 relaunched as P4b).
- All confirmed errata were applied to the LaTeX sources (67+ logged edits, rigor/errata_log.md) and every note recompiled.
- Numerics of Note 5 were independently recomputed (V4), a basis-phase bug was found and fixed, all tables regenerated from the corrected runs.

## Proof-breaking findings (all now resolved or labelled)
1. **2D two-chirality law** (R2, V3, R4): for a 2D CFT the two chiralities see opposite modular rotations, so −log F^(λ) = Φ(z(1+e^{−πλ})) + Φ(z(1+e^{πλ})), even in λ, optimum at λ = 0 (matches Vardhan–Wei–Zou). The claim that the geometric compression beats the Petz map is a single-chirality statement. Fixed in N5 Cor 5.1, N6, N7 Cor 6.1.
2. **False fidelity formula** (R3, P1): ⟨Ω, Δ^{1/2}Ω⟩ is the Wigner–Yanase quantity Tr(ρ^{1/2}σ^{1/2}), not the fidelity. Replaced by the Alberti–Uhlmann supremum formula; Jenčová's construction is finite-dimensional. Fixed in N6, N7.
3. **Zero-collar representative has ‖T(g)Ω‖ = ∞** (V6, P1): the ξ-frame spectral integrals of N7 need a finite-norm representative / form-domain lemma. Caveat added to N7; P1 shows the upper bound survives and reduces the lower bound to a uniform-convergence statement.
4. **Theorem A of N7 overclaimed** (V6): only the one-particle metrics were proved; the identification with lim Φ/ζ² was conditional. Now: liminf ≥ c/(12π²) proved unconditionally (P2, refereed by V7); upper bound within factor 2 log 2 modulo one interchange; sharp upper bound open.
5. **False numerical claims in N5 §3.1** (V4): eigenvalues do reach e^{−κmax}; sub-compression bounds not monotone; tail correction 12–56 % inaccurate at small ζ; Möbius "check" is an identity. Fixed.
6. **Basis-phase bug in the code** (V4): Q and D̂ were expressed in different bases (5e-5 relative effect). Fixed; all tables regenerated.
7. **Proof of Lemma 10.1 (N4)** (R3, V2): variational inequality had to be applied inside each M_n. Fixed.
8. **P2's Prop 7.1 step ⟨1⟩5** (V7): false bound (unrestricted u-integration); repaired, statement survives.
9. **Withdrawn claims**: V2's factor-2 Majorana claim (refuted from the LX text); no factor-2 error anywhere in the CMI coefficient.

## Verification of the universality derivation (V5)
- Notes 6 and 7 checked step by step (rigor/check_notes_6_7.pdf, 25 pp.): f₂ = c/(12π²) and s₂ = c/12 stand; ⟨TT⟩ = (c/8π²)(x−y−i0)⁻⁴ proved independently from [T(1),ψ] = −i∂ψ and positivity; both routes of Thm 5.2 agree integrand by integrand; the base integral is proved by a 2πi-rectangle.
- Two local errors fixed: the claim "both weights bounded by 1+λ" (false for Kubo–Mori) and the BPZ normalization c/32 in note 6 step 3 (inconsistent with step 4, would give f₂ = c/3). The modular translation sign is fixed to ξ ↦ ξ − 2πt (Bisognano–Wichmann + Haag duality), the KMS sign-fixing argument replaced, and the formal status of the ξ-frame computation stated (no admissible representative is affiliated with A(I)).

## New results produced during the audit
- Fidelity half of the type-III second-variation lemma proved for every von Neumann algebra (P1, Thm 3.3 three-way identity).
- Unconditional liminf Φ/ζ² ≥ r/(12π²); unconditional Φ ≤ τ/(1−τ); Hellinger coefficient h₂ = 2 log2 f₂; cutoff error 0.513 r Λ⁻² (P2 + V7).
- Kernel identity D⁽¹⁾ = i(q_κ − q_κ')𝔤 proved analytically with closed form via digamma functions (P3, refereed by V8; independent numerics to 1e-22).
- Exact first-order kernel and c₂ = −ζ²/30 (V3); monotonicity of Φ proved (V3).
- Corrected numerics: f₂ = 0.008444(1) vs c/(12π²) = 0.0084434; s₂ = 0.0837(5) vs c/12 = 0.08333.
- Independent x-space confirmation of the invariant formula and of W-hat(k) (P4b), see above.

## Still open (precisely)
- Kubo–Mori half of the second-variation lemma beyond finite dimensions.
- Sharp limsup Φ/ζ² ≤ g_B/8 (Hellinger route provably insufficient); cubic remainder; the stated O(log⁻²) rate.
- Zero-collar identification of the tangent functional with the spectral integral (uniform convergence of cut-off tangents).
- Note 5 Prop 4.1 tail (2/15)ζ²κ⁻³ is a sketch (exact kernel now available from V3; remainder not proved).
- P4b (x-space route, rigor/collar_and_invariant_formula.pdf): the Mellin transform in u = L−x diagonalizes the modular dilation; W-hat(k) follows exactly from <TT> and the geometric dilation (thermality at β = 2π is a consequence, not an input); g_B = 2c/(3π²) and g_KM = c/6 reassembled to 1e-11. Diagnosis of the formal ξ-frame step: the Mellin–Barnes strips are disjoint precisely because g(L) ≠ 0. Not proved: zero-collar identification of g_B(φ) with the spectral integral, exchange of the collar limit with the s→0 expansion, domain bookkeeping for the dilation of T. (The original P4 died four times without output.)

## Second pass (2026-09-07): every finding checked against the notes
All 93 findings were re-read against the current text of notes 1–7 and the repairs not yet carried into the notes were applied: the missing domain hypotheses of Lemma 3.1 and the simplified hypotheses of Lemma 3.2 in note 7, the status of all four remaining items of note 7 (fidelity half of Lemma 3.2 proved, lower bound of the quadratic limit proved, kernel identity proved and refereed, monotone collar convergence proved with the zero-collar identification open), the D×D vanishing in Lemma 5.1, the chiral-vs-2D coefficient in Cor. 6.1 and the two-branch qualification of Conjecture 2.1 in note 6; in note 4 the unitarity of the push-forward, the exact Powers–Størmer hypothesis, the automatic normality of the extension and the FHSW misprint; in note 5 the sketch status of the UV-tail proposition with the exact kernel referenced, the corrected trap remark and precise attributions of the fidelity formulas; in note 2 the support hypothesis, the reference state of the Petz map and the FHSW citation; in note 1 the definition of the subnet in the bound; in note 3 the modular-Hamiltonian normalization and the c-function convention. Not applied on purpose: stylistic remarks, and findings that concern the rigor documents themselves (these carry orchestrator notes instead).

## Build status
- All 18 standalone rigor documents compile (as of 5 September; the corpus is 46 today, 41 of them in the public repository) (build_all.sh, log build_all_2026-09-05.log); the two macro clashes found by the full rebuild (\cB etc. in audit_dependencies.tex, check_note4.tex) were fixed.

## Where to look
- rigor/findings.pdf — all findings by severity, status table of every result, errata summary.
- rigor/cited_results_all.pdf — every cited result with screenshot and usage cross-check (130 pp).
  Held in the private companion since 21 September; content available on request (THIRD-PARTY.md).
- rigor/check_*.pdf, rigor/audit_dependencies.pdf — Lamport step checks per note; rigor/kernel_identity.pdf, lemma_second_variation.pdf, quadratic_limit.pdf (+ referee_*.pdf) — new proofs and their referee reports.
- rigor/errata_log.md — every edit applied to the notes; numerics/README.md — result files.
