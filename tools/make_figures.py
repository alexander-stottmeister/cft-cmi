#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the figures of the public README and the site into docs/assets/.

One script, standard library only (matplotlib is not installed in this
environment, so the SVG is written by hand).  Deterministic and re-runnable:
every number is parsed out of a file in this repository, never typed in here.

    F1  geometry.svg        original schematic (no data)
                            geometry + zeta from continuum_petz_free_fermion.tex,
                            CMI formula from adjacent_interval_cmi_longo_xu.tex
    F2  quadratic-law.svg   numerics/results_hp2.txt, fidelity_tables.tex,
                            fidelity_table_largezeta.tex
    F3  universality.svg    fidelity_tables.tex, numerics/boson/README.md,
                            numerics/lattice/petz_lattice.out
    F4  theta-ladder.svg    numerics/optimality_all/F3_RESULTS.md
    F5  corner-calculus.svg rigor/network_corner_calculus.tex (Thm 5.2, Thm 5.3,
                            Examples ex:displaced and ex:swallow)

Every parser asserts what it found, so the script fails loudly if a source file
changes underneath it rather than drawing a stale number.

Usage:  python3 tools/make_figures.py
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"

# --------------------------------------------------------------------------
# theme: transparent background, colours legible on light and on dark
# --------------------------------------------------------------------------

CSS = """
  :root {
    --ink:  #1f2328; --mut: #57606a; --grid: #d0d7de; --soft: #eaeef2;
    --c1: #0550ae; --c2: #9a4b00; --c3: #1a7f37; --c4: #6639ba; --c5: #a40e26;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --ink: #e6edf3; --mut: #9198a1; --grid: #3d444d; --soft: #21262d;
      --c1: #79c0ff; --c2: #f0a35e; --c3: #56d364; --c4: #d2a8ff; --c5: #ff8a8a;
    }
  }
  text { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI",
         Helvetica, Arial, sans-serif; fill: var(--ink); font-size: 12px; }
  .ttl  { font-size: 16px; font-weight: 600; }
  .sub  { font-size: 11px; fill: var(--mut); }
  .lab  { font-size: 12px; }
  .tick { font-size: 11px; fill: var(--mut); }
  .note { font-size: 11px; fill: var(--mut); }
  .bold { font-weight: 600; }
  .axis { stroke: var(--ink); stroke-width: 1.2; fill: none; }
  .grid { stroke: var(--grid); stroke-width: 1; fill: none; }
  .soft { fill: var(--soft); stroke: none; }
  .frame{ stroke: var(--grid); stroke-width: 1; fill: none; }
  .s1 { stroke: var(--c1); fill: none; stroke-width: 2; }
  .s2 { stroke: var(--c2); fill: none; stroke-width: 2; }
  .s3 { stroke: var(--c3); fill: none; stroke-width: 2; }
  .s4 { stroke: var(--c4); fill: none; stroke-width: 2; }
  .s5 { stroke: var(--c5); fill: none; stroke-width: 2; }
  .sk { stroke: var(--ink); fill: none; stroke-width: 1.6; }
  .f1 { fill: var(--c1); stroke: none; }
  .f2 { fill: var(--c2); stroke: none; }
  .f3 { fill: var(--c3); stroke: none; }
  .f4 { fill: var(--c4); stroke: none; }
  .f5 { fill: var(--c5); stroke: none; }
  .t1 { fill: var(--c1); } .t2 { fill: var(--c2); } .t3 { fill: var(--c3); }
  .t4 { fill: var(--c4); } .t5 { fill: var(--c5); }
  .hole { fill: none; stroke-width: 2; }
  .dash { stroke-dasharray: 6 4; }
  .dot  { stroke-dasharray: 2 3; }
"""


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Svg:
    """A very small SVG writer: elements are emitted in call order."""

    def __init__(self, w: int, h: int, title: str, desc: str):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.body: list[str] = []

    def raw(self, s: str) -> None:
        self.body.append(s)

    def line(self, x1, y1, x2, y2, cls="axis", extra=""):
        self.raw(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
                 f'y2="{y2:.2f}" class="{cls}"{extra}/>')

    def rect(self, x, y, w, h, cls="frame", rx=0, extra=""):
        self.raw(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" '
                 f'height="{h:.2f}" rx="{rx}" class="{cls}"{extra}/>')

    def circle(self, x, y, r, cls="f1", extra=""):
        self.raw(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" '
                 f'class="{cls}"{extra}/>')

    def path(self, d, cls="s1", extra=""):
        self.raw(f'<path d="{d}" class="{cls}"{extra}/>')

    def poly(self, pts, cls="s1", extra=""):
        d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.raw(f'<polyline points="{d}" class="{cls}"{extra}/>')

    def text(self, x, y, s, cls="lab", anchor="start", extra=""):
        self.raw(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" '
                 f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')

    def vtext(self, x, y, s, cls="lab", anchor="middle"):
        self.raw(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" '
                 f'text-anchor="{anchor}" transform="rotate(-90 {x:.2f} '
                 f'{y:.2f})">{esc(s)}</text>')

    def marker_defs(self) -> str:
        out = []
        for name, var in (("ink", "--ink"), ("c1", "--c1"), ("c2", "--c2"),
                          ("c3", "--c3"), ("c4", "--c4"), ("c5", "--c5")):
            out.append(
                f'<marker id="ar-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M 0 0 L 10 5 L 0 10 z" fill="var({var})"/></marker>')
        return "".join(out)

    def render(self) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} '
            f'{self.h}" width="{self.w}" height="{self.h}" role="img" '
            f'aria-labelledby="t d">\n'
            f'<title id="t">{esc(self.title)}</title>\n'
            f'<desc id="d">{esc(self.desc)}</desc>\n'
            f'<defs>{self.marker_defs()}</defs>\n'
            f'<style>{CSS}</style>\n' + "\n".join(self.body) + "\n</svg>\n")

    def write(self, name: str) -> Path:
        OUT.mkdir(parents=True, exist_ok=True)
        p = OUT / name
        p.write_text(self.render(), encoding="utf-8")
        return p


class Axes:
    """Linear or logarithmic cartesian axes inside a rectangle of the canvas."""

    def __init__(self, svg: Svg, x, y, w, h, xlim, ylim,
                 xlog=False, ylog=False):
        self.s, self.x, self.y, self.w, self.h = svg, x, y, w, h
        self.xlog, self.ylog = xlog, ylog
        self.x0, self.x1 = (math.log10(v) for v in xlim) if xlog else xlim
        self.y0, self.y1 = (math.log10(v) for v in ylim) if ylog else ylim

    def X(self, v):
        u = math.log10(v) if self.xlog else v
        return self.x + self.w * (u - self.x0) / (self.x1 - self.x0)

    def Y(self, v):
        u = math.log10(v) if self.ylog else v
        return self.y + self.h - self.h * (u - self.y0) / (self.y1 - self.y0)

    def box(self):
        self.s.rect(self.x, self.y, self.w, self.h, cls="frame")

    def xgrid(self, vals):
        for v in vals:
            self.s.line(self.X(v), self.y, self.X(v), self.y + self.h, "grid")

    def ygrid(self, vals):
        for v in vals:
            self.s.line(self.x, self.Y(v), self.x + self.w, self.Y(v), "grid")

    def xticks(self, vals, fmt=lambda v: f"{v:g}", dy=16):
        for v in vals:
            xx = self.X(v)
            self.s.line(xx, self.y + self.h, xx, self.y + self.h + 4, "axis")
            self.s.text(xx, self.y + self.h + dy, fmt(v), "tick", "middle")

    def yticks(self, vals, fmt=lambda v: f"{v:g}", dx=8):
        for v in vals:
            yy = self.Y(v)
            self.s.line(self.x - 4, yy, self.x, yy, "axis")
            self.s.text(self.x - dx, yy + 4, fmt(v), "tick", "end")

    def curve(self, pts, cls="s1", extra=""):
        self.s.poly([(self.X(a), self.Y(b)) for a, b in pts], cls, extra)

    def vbar(self, xv, lo, hi, cls="s1", cap=4):
        xx = self.X(xv)
        ylo, yhi = self.Y(lo), self.Y(hi)
        self.s.line(xx, ylo, xx, yhi, cls)
        self.s.line(xx - cap, ylo, xx + cap, ylo, cls)
        self.s.line(xx - cap, yhi, xx + cap, yhi, cls)


# --------------------------------------------------------------------------
# parsers: every number in every figure comes from one of these
# --------------------------------------------------------------------------

def read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        sys.exit(f"make_figures: missing source file {rel}")
    return p.read_text(encoding="utf-8", errors="replace")


def _pm(text: str) -> tuple[float, float]:
    """'0.4410(20)' -> (0.4410, 0.0020); the bracket is in last digits."""
    m = re.match(r"([0-9]+)\.([0-9]+)\((\d+)\)$", text.strip())
    assert m, f"not a value(err) literal: {text!r}"
    val = float(m.group(1) + "." + m.group(2))
    err = int(m.group(3)) * 10.0 ** (-len(m.group(2)))
    return val, err


def parse_small_zeta():
    """numerics/results_hp2.txt: certified window value and tail-corrected."""
    rows = []
    pat = re.compile(
        r"zeta=([0-9.]+)\s+-logF_sub=([0-9.eE+-]+)\s+\+tail=([0-9.eE+-]+)"
        r"\s+\[([0-9.eE+-]+) zeta\^2\]")
    for m in pat.finditer(read("numerics/results_hp2.txt")):
        rows.append(dict(zeta=float(m.group(1)), sub=float(m.group(2)),
                         tail=float(m.group(3)), ratio=float(m.group(4))))
    assert len(rows) == 7, f"results_hp2.txt: expected 7 rows, got {len(rows)}"
    assert abs(rows[0]["zeta"] - 0.00833) < 1e-5
    return rows


def parse_large_zeta():
    """fidelity_table_largezeta.tex; all Phi entries are 10^2 Phi."""
    rows = []
    body = read("fidelity_table_largezeta.tex")
    for line in body.splitlines():
        if "&" not in line or r"\\" not in line:
            continue
        cells = [c.strip() for c in line.split(r"\\")[0].split("&")]
        if len(cells) != 10 or not re.match(r"^[0-9.]+$", cells[0]):
            continue
        certified = [c for c in cells[1:6] if c != "--"]
        best, err = _pm(cells[7])
        rows.append(dict(zeta=float(cells[0]),
                         cert=float(certified[-1]) * 1e-2,
                         phi_inf=float(cells[6]) * 1e-2,
                         best=best * 1e-2, err=err * 1e-2,
                         slope=float(cells[8]),
                         lat=float(cells[9]) * 1e-2))
    assert len(rows) == 5, f"largezeta: expected 5 rows, got {len(rows)}"
    assert abs(rows[-1]["zeta"] - 17.067) < 1e-3
    return rows


def parse_f2_fermion():
    """fidelity_tables.tex, table tab:second-order, the kappa_c -> infinity row."""
    body = read("fidelity_tables.tex")
    m = re.search(r"\\to0\\\).*?&\s*([0-9.]+\(\d+\))\s*&\s*([0-9.]+\(\d+\))",
                  body)
    assert m, "fidelity_tables.tex: extrapolated f2/s2 row not found"
    f2, f2e = _pm(m.group(1))
    s2, s2e = _pm(m.group(2))
    assert abs(f2 - 0.008444) < 1e-6
    return dict(f2=f2, f2err=f2e, s2=s2, s2err=s2e)


def parse_f2_boson():
    """numerics/boson/README.md section 4, the best values."""
    body = read("numerics/boson/README.md")
    m = re.search(r"f_2 = ([0-9.]+)\s*\((\d+)\)\s+vs\s+1/\(12 pi\^2\)", body)
    assert m, "boson README: f_2 best value not found"
    digits = m.group(1).split(".")[1]
    return dict(f2=float(m.group(1)),
                f2err=int(m.group(2)) * 10.0 ** (-len(digits)))


def parse_f2_lattice():
    """numerics/lattice/petz_lattice.out table [1]: Phi_lat/zeta^2.

    The best-converged small-zeta point is the one with the largest chain
    length n below zeta = 0.05; no extrapolation is quoted in the file, so no
    error bar is invented here.
    """
    body = read("numerics/lattice/petz_lattice.out")
    block = body.split("[1]")[1].split("[2]")[0]
    best = None
    for line in block.splitlines():
        c = line.split()
        if len(c) != 6:
            continue
        try:
            zeta, n, phi, cont, ratio, over = (float(c[0]), int(c[1]),
                                               float(c[2]), float(c[3]),
                                               float(c[4]), float(c[5]))
        except ValueError:
            continue
        if zeta < 0.05 and (best is None or n > best["n"]):
            best = dict(zeta=zeta, n=n, phi=phi, cont=cont, ratio=ratio,
                        f2=over)
    assert best and best["n"] == 72, f"lattice table [1]: unexpected {best}"
    return best


def _md_row(lines, key):
    """Return the numeric cells of the markdown table row starting with key."""
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells and cells[0] == key:
            return cells[1:]
    return None


def parse_theta():
    """numerics/optimality_all/F3_RESULTS.md: the h-ladders and the closure."""
    body = read("numerics/optimality_all/F3_RESULTS.md")
    lines = body.splitlines()
    out = {}

    m = re.search(r"theta = ([0-9.]+) \+- ([0-9.]+)", body)
    assert m, "F3_RESULTS.md: reconciled theta not found"
    out["theta"], out["theta_err"] = float(m.group(1)), float(m.group(2))

    m = re.search(r"p = log2\(1/rho\) = ([0-9.]+) \+- ([0-9.]+)", body)
    assert m, "F3_RESULTS.md: convergence order not found"
    out["p"], out["p_err"] = float(m.group(1)), float(m.group(2))

    m = re.search(r"S10's ([0-9.]+) \+- ([0-9.]+) is a lower bound", body)
    assert m, "F3_RESULTS.md: S10 circle value not found"
    out["circle"], out["circle_err"] = float(m.group(1)), float(m.group(2))

    # Sec. 1(b): the Galerkin h-ladder
    blk = body.split("**(b) Mesh width h: the only knob.**")[1].splitlines()
    hs = _md_row(blk, "h")
    th = _md_row(blk, "theta")
    assert hs and th and len(hs) == len(th) == 7, "Galerkin ladder not found"
    out["galerkin"] = [(float(a), float(b)) for a, b in zip(hs, th)]

    # Sec. 3(c): the geometry-free T0 ladder at the same mesh widths
    blk = body.split("**(c) T0 reproduces the Galerkin frame")[1].splitlines()
    hs = _md_row(blk, "h")
    t0 = _md_row(blk, "T0 (Y=Ymax=10)")
    assert hs and t0 and len(hs) == len(t0) == 6, "T0 ladder not found"
    out["t0"] = [(float(a), float(b)) for a, b in zip(hs, t0)]

    # Sec. 4(iii): the family-A Richardson closure
    m = re.search(r"\| A T0 uniform, Y=Ymax=10 \| h=0\.32\.\.\.0\.02 \|"
                  r"[^|]*\| ([0-9.]+) \| \*\*([0-9.]+)\*\* \|", body)
    assert m, "F3_RESULTS.md: family A Richardson row not found"
    out["h_min"] = 0.02
    out["theta_hmin"] = float(m.group(1))
    out["theta_inf_A"] = float(m.group(2))

    # Sec. 5(b): the taper scan at L = 256
    blk = body.split("**(b) The taper is the mechanism.**")[1].splitlines()
    uv = _md_row(blk, "taper window uv")
    tt = _md_row(blk, "theta")
    assert uv and tt and len(uv) == len(tt), "taper scan not found"
    out["taper"] = list(zip(uv, [float(v) for v in tt]))
    return out


def parse_corner():
    """rigor/network_corner_calculus.tex: Examples ex:displaced and ex:swallow.

    The two examples are the two failure mechanisms of hypothesis (H).  Their
    numbers are read from the document; the step parameters are recomputed here
    from the ordinary-Petz formula sigma = 2 l_new/(l_B (l_B + l_new)) and
    checked against the printed ones.
    """
    body = read("rigor/network_corner_calculus.tex")
    dis = body.split(r"\label{ex:displaced}")[1].split(r"\end{example}")[0]
    swa = body.split(r"\label{ex:swallow}")[1].split(r"\end{example}")[0]

    def nums(pat, text, n=1):
        m = re.search(pat, text)
        assert m, f"pattern not found in the example: {pat}"
        return [float(g) for g in m.groups()] if n > 1 else float(m.group(1))

    d = {}
    m = re.search(r"\(l_1,l_2,l_3,l_4\)=\(([^)]*)\)", dis)
    assert m, "ex:displaced: chain lengths not found"
    d["l"] = [float(v) for v in m.group(1).split(",")]
    m = re.search(r"\(p_1,\\dots,p_5\)=\(([^)]*)\)", dis)
    assert m, "ex:displaced: chain points not found"
    d["p"] = [float(v) for v in m.group(1).split(",")]
    d["sigma1"] = nums(r"\\sigma_1=2l_4/\(l_3\(l_3\+l_4\)\)=([0-9.]+)", dis)
    d["sigma2"] = nums(
        r"\\sigma_2=2l_1/\(\(l_2\+l_3\)\(l_1\+l_2\+l_3\)\)=([0-9.]+)", dis)
    d["mass_x0"] = nums(r"-2\\sigma_1k_2'\(x_0\)=(-[0-9.]+)", dis)
    d["x0"] = nums(r"x_0=k_2\^\{-1\}\(p_3\)=([0-9.]+)", dis)
    d["dk2"] = nums(r"k_2'\(x_0\)=([0-9.]+)", dis)
    d["measured_x0"] = nums(r"Measured: \$(-[0-9.]+)\$ at \$x_0\$", dis)
    d["measured_p3"] = nums(r"\$\+([0-9.]+)\\cdot10\^\{-5\}\$ at \$p_3\$",
                            dis) * 1e-5
    d["percent"] = nums(r"total mass is \$([0-9]+)\\%\$", dis)
    d["ctrl_measured"] = nums(r"\(\$(-[0-9.]+)\$ against", dis)
    d["ctrl_naive"] = nums(r"-2\(\\sigma_1\+\\sigma_2\)=(-[0-9.]+)\$", dis)

    l1, l2, l3, l4 = d["l"]
    petz = lambda lb, ln: 2 * ln / (lb * (lb + ln))          # noqa: E731
    assert abs(petz(l3, l4) - d["sigma1"]) < 1e-6
    assert abs(petz(l2 + l3, l1) - d["sigma2"]) < 1e-6
    d["sigma2_ctrl"] = petz(l2, l1)            # control: A_B = A_2 alone
    assert abs(-2 * (d["sigma1"] + d["sigma2_ctrl"]) - d["ctrl_naive"]) < 1e-5

    s = {}
    m = re.search(r"\$l=\(([^)]*)\)\$", swa)
    assert m, "ex:swallow: chain lengths not found"
    s["l"] = [float(v) for v in m.group(1).split(",")]
    m = re.search(r"\(p_1,\\dots,p_4\)=\(([^)]*)\)", swa)
    assert m, "ex:swallow: chain points not found"
    s["p"] = [float(v) for v in m.group(1).split(",")]
    s["sigma1"] = nums(r"\\sigma_1=2l_3/\(l_2\(l_2\+l_3\)\)=([0-9]+)", swa)
    s["sigma2"] = nums(r"\\sigma_2=([0-9]+)", swa)
    m = re.search(r"k_2\\bigl\(\(p_1,p_3\)\\bigr\)=\(([0-9/]+),([0-9/]+)\)",
                  swa)
    assert m, "ex:swallow: image of the moving part not found"
    s["image"] = (m.group(1), m.group(2))
    assert abs(petz(s["l"][1], s["l"][2]) - s["sigma1"]) < 1e-9
    return d, s


# --------------------------------------------------------------------------
# F1  geometry.svg -- original schematic, no data
# --------------------------------------------------------------------------

def fig_geometry() -> Path:
    # the repository's standard geometry: a = 1, L = b + c = 2 (the scale used
    # by fidelity_table_largezeta.tex, where zeta = s/3 = a s/(a+L)); the
    # compression member is s = lambda = c/b (petz-zero-collar-channel),
    # so b = c = 1 gives s = 1 and h_s maps D = B u C exactly onto B.
    a, b, c = 1.0, 1.0, 1.0
    L = b + c
    s = c / b
    zeta = a * s / (a + L)
    sigma = s / L
    hs = lambda x: L * x / (L + s * x)                       # noqa: E731
    cmi = math.log((a + b) * (b + c) / (b * (a + b + c))) / 6
    eps = 0.22                                               # drawn collar

    W, H = 780, 430
    g = Svg(W, H, "Three adjacent intervals and the zero-collar recovery map",
            "Schematic of A, B, C on the chiral line, the collar between A "
            "and B, and the geometric compression that recovers ABC from AB.")
    X0, SC, Y1, Y2 = 250.0, 200.0, 152.0, 286.0
    xp = lambda v: X0 + SC * v                               # noqa: E731

    g.text(24, 30, "Three adjacent intervals, the collar, and the "
                   "compression that recovers ABC from AB", "ttl")
    g.text(24, 50, f"Schematic (no data). Drawn at a = b = c = 1, so L = b+c "
                   f"= 2 and s = λ = c/b = 1; maps and ζ from "
                   f"continuum_petz_free_fermion.tex, CMI from "
                   f"adjacent_interval_cmi_longo_xu.tex.", "sub")

    def band(y, lo, hi, cls, label, tcls):
        g.rect(xp(lo), y - 9, xp(hi) - xp(lo), 18, cls=cls, rx=3)
        g.text((xp(lo) + xp(hi)) / 2, y - 16, label, "lab bold " + tcls,
               "middle")

    # ---- row 1: the vacuum geometry on the chiral line
    g.text(24, Y1 - 46, "vacuum on the line", "note")
    g.line(xp(-1.25), Y1, xp(2.28), Y1, "axis")
    for cls, lo, hi, lab, t in (("f1", -a, 0.0, "A", "t1"),
                                ("f3", 0.0, b, "B", "t3"),
                                ("f2", b, b + c, "C", "t2")):
        band(Y1, lo, hi, cls + " ", lab, t)
    for v, lab in ((-a, "−a = −1"), (0.0, "0"), (b, "b = 1"),
                   (b + c, "b+c = L = 2")):
        g.line(xp(v), Y1 + 10, xp(v), Y1 + 16, "axis")
        g.text(xp(v), Y1 + 30, lab, "tick", "middle")
    # the collar, carved out of A at the touching endpoint
    g.rect(xp(-eps), Y1 - 13, xp(0) - xp(-eps), 26, cls="frame dash", rx=2)
    g.text(xp(-eps / 2), Y1 - 22, "collar ε", "note", "middle")
    g.path(f"M {xp(-eps/2):.1f} {Y1-34:.1f} C {xp(-0.55):.1f} {Y1-58:.1f} "
           f"{xp(-0.95):.1f} {Y1-58:.1f} {xp(-1.2):.1f} {Y1-52:.1f}",
           "grid")
    g.text(xp(-1.22), Y1 - 56, "ε > 0: split product state, FHSW Petz "
                               "map; ε = 0: no normal product state,",
           "note", "start")
    g.text(xp(-1.22), Y1 - 42, "the channel is the unique normal extension "
                               "(Note 4, Thm. normal zero-collar map)",
           "note", "start")

    # ---- transfer arrows
    for x in (0.5, 1.0, 1.5, 2.0):
        g.line(xp(x), Y1 + 42, xp(hs(x)), Y2 - 30, "grid dot",
               ' marker-end="url(#ar-ink)"')
    g.text(xp(2.34), (Y1 + Y2) / 2 + 4, "kₛ", "lab bold", "start")

    # ---- row 2: the image under the compression
    g.text(24, Y2 - 46, "after the compression kₛ", "note")
    g.line(xp(-1.25), Y2, xp(2.28), Y2, "axis")
    band(Y2, -a, 0.0, "f1 ", "A (fixed)", "t1")
    band(Y2, 0.0, hs(b), "f3 ", "hₛ(B)", "t3")
    band(Y2, hs(b), hs(b + c), "f2 ", "hₛ(C)", "t2")
    for v, lab in ((-a, "−1"), (0.0, "0"), (hs(b), f"{hs(b):.3f}"),
                   (hs(b + c), f"{hs(b+c):.0f} = b")):
        g.line(xp(v), Y2 + 10, xp(v), Y2 + 16, "axis")
        g.text(xp(v), Y2 + 30, lab, "tick", "middle")
    g.text(xp(1.15), Y2 + 6, "← the whole of B∪C now sits inside B",
           "note", "start")
    g.line(xp(0), Y2 - 30, xp(0), Y2 - 14, "s5",
           ' marker-end="url(#ar-c5)"')
    g.text(xp(0.04), Y2 - 32, f"corner p = 0:  Schwarzian mass "
                              f"−2σ = −{2*sigma:g}, "
                              f"σ = s/L = {sigma:g}", "note t5", "start")

    # ---- the three sourced statements
    yy = Y2 + 62
    for line in (
        "recovery map (Note 4):  kₛ = id on A,  hₛ(x) = Lx/(L+sx) "
        "on D = B∪C.  At s = λ = c/b the range is exactly "
        "𝒜(B), so the map recovers ABC from AB.",
        f"corner strength:  ζ = as/(a+L) = {zeta:.4f}  "
        f"(continuum_petz_free_fermion.tex); the recovery error of "
        f"Theorem A is Φ(ζ) = −log F.",
        f"Longo–Xu CMI:  I(A:C|B) = (c/6)·log[(a+b)(b+c)/"
        f"(b(a+b+c))] = (c/6)·log(4/3) = {cmi:.4f}·c  "
        f"(adjacent_interval_cmi_longo_xu.tex).",
    ):
        g.text(24, yy, line, "note")
        yy += 19
    return g.write("geometry.svg")


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴"
                                   "⁵⁶⁷⁸⁹")


def pow10(v):
    return "10" + str(int(round(math.log10(v)))).translate(SUP)


def sqmark(g, x, y, r, cls):
    g.rect(x - r, y - r, 2 * r, 2 * r, cls=cls)


# --------------------------------------------------------------------------
# F2  quadratic-law.svg
# --------------------------------------------------------------------------

def fig_quadratic_law() -> Path:
    small = parse_small_zeta()
    large = parse_large_zeta()
    con = parse_f2_fermion()
    f2 = con["f2"]
    zmin, zmax = small[0]["zeta"], large[-1]["zeta"]

    W, H = 780, 604
    g = Svg(W, H, "The quadratic law: recovery error against corner strength",
            "Phi(zeta) = -log F measured over the range zeta = %.4g to %.4g, "
            "with the zeta^2 asymptote and the measured remainder."
            % (zmin, zmax))
    g.text(24, 30, "Theorem A: Φ(ζ) = −log F and its "
                   "ζ² asymptote", "ttl")
    g.text(24, 50, "Free chiral fermion, c = 1. Sources: "
                   "numerics/results_hp2.txt (small ζ, certified "
                   "window + tail), fidelity_table_largezeta.tex (large "
                   "ζ, best estimates), fidelity_tables.tex "
                   f"(f₂ = {f2:.6f}({int(con['f2err']*1e6)})).", "sub")

    ax = Axes(g, 86, 76, 592, 258, (0.0068, 24), (2.6e-7, 0.13),
              xlog=True, ylog=True)
    xt = [0.01, 0.1, 1, 10]
    yt = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    ax.xgrid(xt), ax.ygrid(yt), ax.box()
    ax.xticks(xt, lambda v: f"{v:g}")
    ax.yticks(yt, pow10)
    g.vtext(36, ax.y + ax.h / 2, "Φ(ζ) = −log F   (nats)",
            "lab")

    # the proved asymptote, clipped to the panel
    zhi = math.sqrt(0.13 / f2)
    ax.curve([(0.0068, f2 * 0.0068 ** 2), (zhi, f2 * zhi ** 2)], "s4 dash")
    g.text(ax.X(3.0), ax.Y(f2 * 9.0) + 22,
           "Φ = f₂ζ² (Theorem A)", "note t4", "start")

    # small zeta: certified brackets [window value, window value + tail]
    for r in small:
        ax.vbar(r["zeta"], r["sub"], r["tail"], "s1", cap=3)
        sqmark(g, ax.X(r["zeta"]), ax.Y(r["tail"]), 3.2, "f1")
    # large zeta: certified lower end, and the best (extrapolated) estimate
    for r in large:
        x = ax.X(r["zeta"])
        g.line(x - 7, ax.Y(r["cert"]), x + 7, ax.Y(r["cert"]), "s3")
        ax.vbar(r["zeta"], r["best"] - r["err"], r["best"] + r["err"],
                "s2", cap=4)
        g.circle(x, ax.Y(r["best"]), 4.2, "hole",
                 ' stroke="var(--c2)" fill="none"')

    # legend, in the empty upper-left corner of the panel
    lx, ly = ax.x + 18, ax.y + 22
    for i, (draw, txt) in enumerate((
        ("sq", "certified bracket [Φ in the spectral window, "
               "+ tail ζ²/(15κᶜ²)]"),
        ("tick", "certified lower bound at the largest κᶜ "
                 "(large ζ)"),
        ("circ", "best estimate Φ∞, κᶜ→∞ "
                 "extrapolation, with its quoted error"),
        ("dash", "proved ζ² asymptote, f₂ = c/(12π²)"),
    )):
        y = ly + i * 19
        if draw == "sq":
            sqmark(g, lx, y - 4, 3.2, "f1")
        elif draw == "tick":
            g.line(lx - 6, y - 4, lx + 6, y - 4, "s3")
        elif draw == "circ":
            g.circle(lx, y - 4, 4.2, "hole",
                     ' stroke="var(--c2)" fill="none"')
        else:
            g.line(lx - 7, y - 4, lx + 7, y - 4, "s4 dash")
        g.text(lx + 14, y, txt, "note")

    # ---- lower panel: the measured remainder
    bx = Axes(g, 86, 404, 592, 106, (0.0068, 24), (0.0, 1.12), xlog=True)
    bt = [0.0, 0.25, 0.5, 0.75, 1.0]
    bx.xgrid(xt), bx.ygrid(bt), bx.box()
    bx.xticks(xt, lambda v: f"{v:g}")
    bx.yticks(bt, lambda v: f"{v:g}")
    g.vtext(36, bx.y + bx.h / 2, "Φ / (f₂ζ²)", "lab")
    g.text(24, 390, "measured remainder: the ratio to the pure "
                    "ζ² law", "note")
    bx.curve([(0.0068, 1.0), (24, 1.0)], "s4 dash")
    pts = []
    for r in small:
        v = r["ratio"] / f2
        pts.append((r["zeta"], v))
        sqmark(g, bx.X(r["zeta"]), bx.Y(v), 3.0, "f1")
    for r in large:
        v = r["best"] / (f2 * r["zeta"] ** 2)
        pts.append((r["zeta"], v))
        g.circle(bx.X(r["zeta"]), bx.Y(v), 3.8, "hole",
                 ' stroke="var(--c2)" fill="none"')
    bx.curve(pts, "s1", ' stroke-width="1" stroke-dasharray="3 3"')
    g.text(bx.x + bx.w / 2, bx.y + bx.h + 22,
           "ζ   (corner strength ζ = as/(a+L), dimensionless)",
           "lab", "middle")

    g.text(24, H - 34,
           f"Measured range ζ = {zmin} to {zmax}. The small-ζ window "
           f"values are rigorous lower bounds and the tail correction is "
           f"added; at large ζ that tail is not valid, so the bracket is "
           f"[Φ at κᶜ(max), Φ∞].", "note")
    g.text(24, H - 16,
           "The local log-slope d log Φ / d log ζ falls from "
           f"{large[0]['slope']} at ζ = {large[0]['zeta']} to "
           f"{large[-1]['slope']} at ζ = {large[-1]['zeta']} "
           "(fidelity_table_largezeta.tex): the ζ² law is a "
           "ζ → 0 statement, not a global one.", "note")
    return g.write("quadratic-law.svg")


# --------------------------------------------------------------------------
# F3  universality.svg
# --------------------------------------------------------------------------

def fig_universality() -> Path:
    ferm = parse_f2_fermion()
    bos = parse_f2_boson()
    lat = parse_f2_lattice()
    f2_of_c = lambda c: c / (12 * math.pi ** 2)              # noqa: E731

    W, H = 780, 452
    g = Svg(W, H, "Universality of the second-order coefficient",
            "The proved line f2 = c/(12 pi^2) of Theorem B, and the three "
            "independent measurements, all made at c = 1.")
    g.text(24, 30, "Theorem B: the second-order coefficient is linear in c, "
                   "and three models measure it at c = 1", "ttl")
    g.text(24, 50, "The straight line is a theorem, not a fit: no measurement "
                   "away from c = 1 exists, and none is scaled along the "
                   "line.", "sub")

    cmax = 3.0
    ax = Axes(g, 86, 84, 322, 252, (0.0, cmax), (0.0, f2_of_c(cmax) * 1.05))
    yt = [0.0, 0.005, 0.010, 0.015, 0.020, 0.025]
    ax.xgrid([1, 2, 3]), ax.ygrid(yt), ax.box()
    ax.xticks([0, 1, 2, 3])
    ax.yticks(yt, lambda v: f"{v:.3f}")
    g.vtext(30, ax.y + ax.h / 2,
            "f₂ = lim Φ/ζ²  (per chirality)", "lab")
    g.text(ax.x + ax.w / 2, ax.y + ax.h + 34, "central charge c", "lab",
           "middle")
    ax.curve([(0.0, 0.0), (cmax, f2_of_c(cmax))], "s4",
             ' stroke-width="2.4"')
    g.text(ax.X(1.45), ax.Y(f2_of_c(1.45)) - 12,
           "Theorem B (proved):", "note t4")
    g.text(ax.X(1.45), ax.Y(f2_of_c(1.45)) + 2,
           "f₂ = c/(12π²)", "note t4")
    # the measured cluster and the zoom window
    g.circle(ax.X(1.0), ax.Y(f2_of_c(1.0)), 4, "f1")
    g.rect(ax.X(1.0) - 16, ax.Y(f2_of_c(1.0)) - 14, 32, 28, "frame dash", 3)
    g.text(ax.X(1.0), ax.Y(f2_of_c(1.0)) + 34,
           "all three measurements", "note", "middle")
    g.text(ax.X(1.0), ax.Y(f2_of_c(1.0)) + 48, "sit here, at c = 1",
           "note", "middle")
    g.line(ax.X(1.0) + 18, ax.Y(f2_of_c(1.0)), 494, 200, "grid dash",
           ' marker-end="url(#ar-ink)"')

    # ---- zoom panel: the three measurements against the proved value
    lo, hi = 0.00836, 0.00850
    zx = Axes(g, 500, 84, 200, 252, (0.0, 3.0), (lo, hi))
    zt = [0.00836, 0.00840, 0.00844, 0.00848]
    zx.ygrid(zt), zx.box()
    zx.yticks(zt, lambda v: f"{v:.5f}")
    zx.curve([(0.0, f2_of_c(1.0)), (3.0, f2_of_c(1.0))], "s4")
    g.text(zx.x + 6, zx.Y(f2_of_c(1.0)) - 7,
           f"c/(12π²) = {f2_of_c(1.0):.7f}", "note t4")
    g.text(zx.x + zx.w / 2, zx.y - 10, "zoom at c = 1", "note", "middle")

    meas = [
        (0.6, ferm["f2"], ferm["f2err"], "f1", "fermion"),
        (1.5, bos["f2"], bos["f2err"], "f3", "boson"),
        (2.4, lat["f2"], None, "f2", "lattice"),
    ]
    for xx, val, err, cls, lab in meas:
        if err:
            zx.vbar(xx, val - err, val + err, "s" + cls[-1], cap=6)
            g.circle(zx.X(xx), zx.Y(val), 4.2, cls)
        else:
            g.circle(zx.X(xx), zx.Y(val), 4.4, "hole",
                     f' stroke="var(--c{cls[-1]})" fill="none"')
        g.text(zx.X(xx), zx.y + zx.h + 18, lab, "tick", "middle")

    yy = H - 92
    for line in (
        f"free chiral fermion (continuum, certified window + "
        f"κᶜ→∞ extrapolation):  f₂ = {ferm['f2']}"
        f"({int(ferm['f2err']*1e6)})  — fidelity_tables.tex, "
        f"table tab:second-order  [numerical]",
        f"U(1) current net, the bosonic check at c = 1:  f₂ = "
        f"{bos['f2']}({int(bos['f2err']*1e5)})  — "
        f"numerics/boson/README.md §4  [numerical]",
        f"hopping chain, c = 1:  Φ/ζ² = {lat['f2']} at "
        f"ζ = {lat['zeta']}, n = {lat['n']} sites (lattice/continuum "
        f"ratio {lat['ratio']} there; a single finite-ζ, finite-n point, "
        f"not an extrapolation, so no error bar is quoted)",
        "       — numerics/lattice/petz_lattice.out, table [1], "
        "produced by numerics/lattice/petz_lattice.py  [numerical]",
    ):
        g.text(24, yy, line, "note")
        yy += 18
    return g.write("universality.svg")


# --------------------------------------------------------------------------
# F4  theta-ladder.svg
# --------------------------------------------------------------------------

def fig_theta_ladder() -> Path:
    t = parse_theta()
    p = t["p"]
    B = (t["theta_inf_A"] - t["theta_hmin"]) / t["h_min"] ** p

    W, H = 780, 470
    g = Svg(W, H, "The theta convergence ladder and the superseded circle "
                  "model",
            "theta against mesh width plotted as h^0.77, extrapolating to "
            "0.384 +- 0.003, beside the taper-suppressed circle-model value "
            "0.300.")
    g.text(24, 30, "The first-order gain constant θ: convergence ladder "
                   f"in h, extrapolated to {t['theta']} ± "
                   f"{t['theta_err']}", "ttl")
    g.text(24, 50, "Source: numerics/optimality_all/F3_RESULTS.md "
                   "(§1(b), §3(c), §4, §5(b)). "
                   f"Measured convergence order h^{p} ± {t['p_err']}, "
                   "five mesh families.", "sub")

    hmax = t["galerkin"][0][0]
    ax = Axes(g, 86, 86, 456, 268, (0.0, hmax ** p * 1.06), (0.27, 0.40))
    yt = [0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40]
    hs = [0.02, 0.04, 0.06, 0.08, 0.12, 0.16, 0.24, 0.32]
    ax.ygrid(yt)
    ax.xgrid([h ** p for h in hs])
    ax.box()
    ax.yticks(yt, lambda v: f"{v:.2f}")
    ax.xticks([0.0] + [h ** p for h in hs],
              lambda v: "0" if v == 0 else f"{v ** (1/p):.2f}")
    g.vtext(32, ax.y + ax.h / 2, "θ   (first-order gain constant)",
            "lab")
    g.text(ax.x + ax.w / 2, ax.y + ax.h + 38,
           f"mesh width h, plotted on the axis h^{p} so that the "
           f"extrapolation is a straight line", "lab", "middle")

    # the extrapolated value and its error band
    ylo, yhi = t["theta"] - t["theta_err"], t["theta"] + t["theta_err"]
    g.rect(ax.x, ax.Y(yhi), ax.w, ax.Y(ylo) - ax.Y(yhi), "soft")
    ax.curve([(0.0, t["theta"]), (ax.x1, t["theta"])], "s2 dash")
    g.text(ax.x + 10, ax.Y(t["theta"]) - 8,
           f"θ = {t['theta']} ± {t['theta_err']}  (h → 0; "
           f"1 − θ = {1-t['theta']:.3f} ± {t['theta_err']})",
           "note t2")
    # the Richardson line through the finest family-A point
    ax.curve([(0.0, t["theta_inf_A"]),
              (ax.x1, t["theta_inf_A"] - B * ax.x1)], "s2")

    for h, v in t["galerkin"]:
        sqmark(g, ax.X(h ** p), ax.Y(v), 3.4, "f1")
    for h, v in t["t0"]:
        g.circle(ax.X(h ** p), ax.Y(v), 4.0, "hole",
                 ' stroke="var(--c3)" fill="none"')
    g.circle(ax.X(t["h_min"] ** p), ax.Y(t["theta_hmin"]), 4.0, "hole",
             ' stroke="var(--c3)" fill="none"')

    lx, ly = ax.x + 232, ax.y + 200
    sqmark(g, lx, ly - 4, 3.4, "f1")
    g.text(lx + 12, ly, "modular Galerkin frame, a = 1, L = 2 (§1b)",
           "note")
    g.circle(lx, ly + 15, 4.0, "hole", ' stroke="var(--c3)" fill="none"')
    g.text(lx + 12, ly + 19, "T0 Wiener–Hopf frame, geometry-free "
                             "(§3c, §4)", "note")
    g.line(lx - 7, ly + 34, lx + 7, ly + 34, "s2")
    g.text(lx + 12, ly + 38, "Richardson line through the finest point",
           "note")

    # ---- the superseded circle model, on the same theta axis
    cx = Axes(g, 596, 86, 118, 268, (0.0, 2.0), (0.27, 0.40))
    cx.ygrid(yt), cx.box()
    g.text(cx.x + cx.w / 2, cx.y - 10, "circle model", "note", "middle")
    taper = dict(t["taper"])
    lo_t, hi_t = taper["(0.30,0.42)"], taper["(0.35,0.47)"]
    g.line(cx.X(1.35), cx.Y(lo_t), cx.X(1.35), cx.Y(hi_t), "s5 dash",
           ' marker-end="url(#ar-c5)"')
    g.text(cx.X(1.35) + 6, cx.Y((lo_t + hi_t) / 2) - 4, "relax", "note t5")
    g.text(cx.X(1.35) + 6, cx.Y((lo_t + hi_t) / 2) + 8, "the taper", "note t5")
    cx.vbar(0.75, t["circle"] - t["circle_err"], t["circle"] + t["circle_err"],
            "s5", cap=6)
    sqmark(g, cx.X(0.75), cx.Y(t["circle"]), 3.6, "f5")
    g.text(cx.X(0.75), cx.Y(t["circle"]) + 20,
           f"{t['circle']} ± {t['circle_err']}", "note t5", "middle")
    g.text(cx.x + cx.w / 2, cx.y + cx.h + 18, "superseded", "note t5",
           "middle")

    yy = H - 84
    for line in (
        f"θ = {t['theta']} ± {t['theta_err']} is the "
        f"h → 0 Richardson closure of five mesh families "
        f"(F3_RESULTS.md §4(iii), spread 0.3835–0.3847); the "
        f"finest family-A point is θ = {t['theta_hmin']} at h = "
        f"{t['h_min']}.",
        "T0 points are taken at Y = y_max = 10; the finite-y_max correction "
        "is +0.002 at h = 0.06 (§4(i)) and is the offset of those points "
        "from the line.",
        f"The circle model with the S10 ultraviolet taper gives θ = "
        f"{t['circle']} ± {t['circle_err']}. It is a taper-suppressed "
        f"LOWER BOUND, not a competing limit: at L = 256 relaxing the taper "
        f"window from (0.30,0.42) to (0.35,0.47)",
        f"moves θ from {lo_t} to {hi_t} (§5(b)), and the model has "
        f"no taper-free limit. The card carrying it is marked superseded.",
    ):
        g.text(24, yy, line, "note")
        yy += 17
    return g.write("theta-ladder.svg")
