# REF-README-1 — `readme-and-figures`: pass 1 **FAIL**, pass 2 (REF-README-1b) **FAIL** (2026-09-21)

**Pass 2.** D1-D5, D9, D10 repaired and verified: badge now `numerical` with the θ > 0 reason; the `proved`
sentence ends at "convex tangent programme" and attainment sits in the conditional paragraph, matching
`exact_optimum_tangent_problem.tex` §Conditional(4); CHECKLIST link gone; §10/§13 corrected; Prop. 9.1 /
Lem. 9.2 confirmed in the `.aux`, (H) stated with the two-interval start, and the 1:4 (unconditional) /
1:2 (needs the network law) split matches card `vwz-protocol-ordering`; 1012 lines, 0 unreachable, figures
byte-identical on re-run. **Three remain.** (D8b) (V)→upper and Araki→lower are the right ends, but Gap RK2
says the Araki sources were **NOT OBTAINED** and (ii) is "carried as a hypothesis" — the README instead
picks "taken from an obtainable source", the wrong one of its own four dispositions. (D6b) `0.969`–`0.990`
matches no window of table [2] (η ≤ 0.02 → 0.9686-0.9953; η ≤ 0.05 → 0.9489-0.9967) and no η range is
stated, though the column falls to 0.41 at large η. (D7b) README F4 still badges the S10 value
`superseded`, which no card carries (`docs/status.md` lists 2, neither this); the SVG sentence is now
broken English, "the model has no taper-free limit, and superseded by the reconciliation"; orphan comment
at `make_figures.py:846`.

| README | claim | source | verdict |
|---|---|---|---|
| 20,128 | θ = 0.384 ± 0.003, 1−θ = 0.616 ± 0.003 | F3_RESULTS.md §4 l.13,15,163 | OK |
| 20,127 | optimum value, `numerical` + H1,H2,H3 | card `all-channel-optimum-value` | OK |
| 64-65 | f₂ = 0.008444(1), s₂ = 0.0837(5) | fidelity_tables.tex `tab:second-order` last row | OK |
| 66 | range ζ = 0.0083 … 17.067 | results_hp2.txt says **0.00833**; F2 itself says 0.00833 | minor |
| 77-79 | [0.05739, 0.06412], 0.0641(43); slope 1.29→0.69 | fidelity_table_largezeta.tex (10²Φ) | OK |
| 102 | boson 0.00844(2), 0.083(2) vs 0.0084434, 0.0833333 | numerics/boson/README.md §4 l.104-105 | OK |
| 104-105 | 0.008454 at ζ=0.03175, n=72, ratio 1.0316 | petz_lattice.out table [1] l.15 | OK |
| 110 | "What **is proved** is the bracket 0.0338c … 0.924c" | kubo_mori l.811 proved **under (V)** ((V) *open*), l.816 proved **modulo** Araki | **D8** |
| 121-125 | "`proved`. compression is **not** the minimiser" | card is **`numerical`** ("theta > 0 is numerical, not proved") | **D1** |
| 121-125 | "`proved` … optimum attained on the isometric orbit" | exact_optimum §Conditional(4): "under H3 … modulo H1,H2,H3, and (a),(e) on meshes" | **D2** |
| 142-146 | 0.3835-0.3847, 0.37442 @ h=0.02, 0.28958→0.36178 | F3_RESULTS.md §4(iii), §5(b) | OK |
| 143 | S10 value badged `superseded` | no card is `superseded`; `docs/status.md` l.17 lists 2, neither this | **D7** |
| 173-178 | −3.634274/−3.634266, x₀=3.200568, k₂′=0.670114, 71%, −2δ(p₃) | network_corner_calculus.tex l.762-767, 771-786 | OK |
| 187-194 | 2ⁿ⁻² protocols → n−1 classes; the two conjectures | true (`prop:startblock`) but **no file cited**; holonomy needs \|J₀\|≥2 | **D9** |
| 203-206 | 1.986,1.912,1.635,1.151 vs 2.00,1.90,1.70,1.20; 0.1525,0.1444,0.1357 | petz_lattice.out [3] l.287-291, [8] l.579-581 | OK |
| 205 | "reproduces −log F to ratio **1.0000** (table [2])" | 1.0000 only at λ=0, where Φ_lat ≡ ½(−log F⁰) makes it definitional; λ=0.5/1/1.5 give 0.969-0.990 | **D6** |
| 215-222 | κ_F 5.863/6.237/6.293, κ_I 3.129/3.159/3.150, gap law, 1.0006, κ_g≈0.09 | numerics/lattice/README.md §1, §3 | OK |
| 315 | "every document still compiles" | contradicts l.309 and §13 | **D4** |
| 367 | "both PDFs on disk date from 8 September" | `rigor/referee_implementation_C11.pdf` does not exist | **D5** |
| 368 | link `CHECKLIST.md` | `.gitignore:40 /CHECKLIST.md`; untracked ⇒ dead in a clone | **D3** |

**D10** `tools/make_figures.py`: 114 of 1127 lines unreachable (656-690, 778-819, 924-960), duplicated tails after a `return`; the dead copies carry divergent caption text, so a repair could silently miss.
