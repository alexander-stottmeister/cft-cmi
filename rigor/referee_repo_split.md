# Referee report — `repo-split-public-private` (REF-INFRA-1, 2026-09-20)

Verdict: **pass** — every number reproduces, the public clone builds, sets are disjoint.

## Claimed vs measured

| Claim | Claimed | Measured |
|---|---|---|
| public files / size | 405 / 5.9 MB | 405 / 5,888,415 B = 5.89 MB |
| private files / size | 228 / 47.7 MB | 228 / 47,750,584 B = 47.75 MB (truncated) |
| overlap public ∩ private | 0 | 0 |
| tracked by neither / size | 331 / 196 MB | 331 (+1, my packet) / 196,019,119 B |
| excerpts / source PDFs | 178 / 47 | 178 / 47 |
| result captures | 97 | 97 tracked `.out` |
| call sites / documents | 255 / 19 | 255 / 19 |
| python scripts / literals | 24 / 37 | 24 / 37 (diff of f9ffae4) |
| refs listed / fetchable / library | 36 / 20 / 16 | 36 / 20 / 16 |
| network_corner_calculus | 42 pp with images | 42 pp, 10 images, 0 placeholders |
| remotes | none | none in either repo |

## Tests

1. **Layout.** Both git dirs present; private has `core.bare=false`, `core.worktree` =
   project root. `./pgit check` → overlap 0, shots 178/178.
2. **Coverage.** The 331 untracked files are 96 `.npz`, 77 `.log`, 55 `.pdf`, 31 `.out`,
   31 `.aux`, 26 `.toc`, 10 `.pkl`, 6 review packets. Every untracked `.pdf` has a
   tracked `.tex` source (0 orphans); all `.npz`/`.pkl` are under `numerics/`.
   **No `.tex`, `.py`, `.sh` or `.bib` falls through** — the design property holds.
3. **With excerpts.** `quadratic_limit` → 27 pp, 8 embedded images, 0 placeholders.
4. **Public clone** (`git archive HEAD | tar -x`; 405 files, no `shots/`, no PDFs):
   compiles → 26 pp, 0 images, 8 placeholders for 8 call sites, exact 1:1 degradation.
   All 19 converted documents: **17 build**; the 2 failures fail *identically in the
   local tree with excerpts present*, so the conversion breaks nothing.
5. **`pgit sync`.** A dummy under `rigor/shots/` was invisible to both `git status -uall`
   and `./pgit status -uall`; `./pgit check` said "on disk 179, tracked 178". Dummy
   deleted, both trees clean.
6. **Python.** `grep -rl '/Users/alex' --include='*.py'` empty; all 148 `.py` compile (no
   `__pycache__` left). `_ROOT` resolves to the project root from depth 1 and 2, cwd-independently.
7. **Release safety.** LICENSE (MIT code / CC BY 4.0 docs), LICENSE-CODE, LICENSE-DOCS,
   THIRD-PARTY.md, refs/restore.sh present, public-tracked, and saying what the card says.
   `git ls-files | grep -E 'shots/|\.pdf$'` empty. **Public history: 413 distinct paths
   ever, 0 matching `shots/` or `.pdf`; largest blob 0.30 MB** — a later push is safe.
   THIRD-PARTY.md's "221 citedbox" also reproduces exactly.

## Defects (none fatal)

- **`next` understates.** It names one non-building document; CHECKLIST.md item 2 says
  *two*. The second fails from a different cause: `referee_implementation_C11` dies at
  l.364 on an undefined `\one`, not the `\lqed` arity. Both pre-existing — the release
  commit's diff for that file is shot conversion only (0 other changed lines).
- **CHECKLIST.md item 4 is off.** It claims thirteen `.out`/`.txt` carry the absolute
  path; measured 12 (10 `.out`, 2 `.txt`), and 14 tracked files once `F2_RESULTS.md` and
  `results_hp14_L120.err` are counted. 31 literal occurrences remain.
- **A second path class is missed entirely.** 10 public-tracked files — 4 `.sh`
  (`numerics/run_hp14.sh`, `run_largezeta.sh`, `run_largezeta2.sh`, `certified/runhp.sh`)
  plus `rigor/README_AGENTS.md` — hardcode a scratchpad venv interpreter that **no longer
  exists**; the portability work covered `.py` only.
- Omitted risks are covered in evidence docs (`git clean -xfd` and the second-machine
  two-clone recipe are in PRIVATE.md, repeated in README_AGENTS.md 4-5). `./pgit check`
  *reports* a shots mismatch but still exits 0, so it is not usable as a CI gate.
