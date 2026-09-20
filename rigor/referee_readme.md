# REF-README-1 — `readme-and-figures`: **FAIL** (2026-09-21)

`make figures` reproduces all five SVGs byte-identically to HEAD. No SVG holds an absolute path or a CSS
variable; both themes are literal hex under `@media (prefers-color-scheme: dark)`. Provenance is byte-identical
to `paper1/main.tex` §Provenance. 50 relative links resolve; the only external URL is the release; no `*.pdf`
link. F2 distinguishes certified brackets from best estimates; F3 draws Theorem B as a proved line with all
three points at c = 1; F5 shows `ex:displaced` **and** `ex:swallow` and marks the junction form under (H).
2/ε and the angle form do not appear, so neither is overstated. The three unsourceable items were replaced
honestly (raw lattice point, no error bar; "factors 22-5000" dropped; tally → `docs/status.md`).

| README | claim | source | verdict |
|---|---|---|---|
| 20,128 | θ = 0.384 ± 0.003, 1−θ = 0.616 ± 0.003 | F3_RESULTS.md §4 l.13,15,163 | OK |
| 20,127 | optimum value, `numerical` + H1,H2,H3 | card `all-channel-optimum-value` | OK |
| 56 | f₂ = c/(12π²) = 0.0084434·c | quadratic_limit.tex l.497,1156 | OK |
| 61 | 0.173 ζ²/κ_c + 0.88 ζ²/κ_c², κ_c ≥ max{10,…} | tail_bound.tex l.804-805 (§5 ⇒ Thm 5.1) | OK |
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
| 151-152 | 26 candidates, 3 inside [0.381,0.387], 0.28 by chance | F3_RESULTS.md §6 l.234,255-256 | OK |
| 173-178 | −3.634274/−3.634266, x₀=3.200568, k₂′=0.670114, 71%, −2δ(p₃) | network_corner_calculus.tex l.762-767, 771-786 | OK |
| 187-194 | 2ⁿ⁻² protocols → n−1 classes; the two conjectures | true (`prop:startblock`) but **no file cited**; holonomy needs \|J₀\|≥2 | **D9** |
| 203-206 | 1.986,1.912,1.635,1.151 vs 2.00,1.90,1.70,1.20; 0.1525,0.1444,0.1357 | petz_lattice.out [3] l.287-291, [8] l.579-581 | OK |
| 205 | "reproduces −log F to ratio **1.0000** (table [2])" | 1.0000 only at λ=0, where Φ_lat ≡ ½(−log F⁰) makes it definitional; λ=0.5/1/1.5 give 0.969-0.990 | **D6** |
| 215-222 | κ_F 5.863/6.237/6.293, κ_I 3.129/3.159/3.150, gap law, 1.0006, κ_g≈0.09 | numerics/lattice/README.md §1, §3 | OK |
| 232-233 | c_E=1.00090, c_M=1.00144; (c_M/c_E)/(mR)=1.02 @ m=0.4,R=16 | numerics/lattice/README.md §2 l.106,112 | OK |
| 243,300,357-361 | 5 open, 30 errata sections, 178/221/36/20/16 | docs/open.md, errata_log.md, THIRD-PARTY.md | OK |
| 315 | "every document still compiles" | contradicts l.309 and §13 | **D4** |
| 367 | "both PDFs on disk date from 8 September" | `rigor/referee_implementation_C11.pdf` does not exist | **D5** |
| 368 | link `CHECKLIST.md` | `.gitignore:40 /CHECKLIST.md`; untracked ⇒ dead in a clone | **D3** |
| 373-374 | C11 l.486 `\lstep{1}{4}{\lqed}`; referee l.364 `\one`, undefined | both confirmed | OK |

**D10** `tools/make_figures.py`: 114 of 1127 lines unreachable (656-690, 778-819, 924-960), duplicated tails after a `return`; the dead copies carry divergent caption text, so a repair could silently miss.
