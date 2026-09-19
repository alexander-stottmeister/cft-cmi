#!/usr/bin/env python3
r"""Replace \includegraphics{shots/...} and the local \shot macros by the canonical
graceful \shot/\shotc of rigor_preamble.tex.  Usage: convert_shots.py <rigor-dir>"""
import re, sys, glob, os
MACRO = r"""
% --- excerpts of cited sources ----------------------------------------------------
% The page images in rigor/shots/ are excerpts of third-party publications and are NOT
% redistributed with the public release.  \shot is an exact drop-in for \includegraphics
% that degrades to a framed note when shots/ is absent, so every document still compiles
% from a clone without them; \shotc is the centred variant.  The precise locator of each
% excerpt is always stated in the accompanying cited-result box.
\newcommand{\shotmissing}[2]{\fbox{\parbox{\dimexpr#1-2\fboxsep-2\fboxrule\relax}{\small%
\textbf{Screenshot not included.}\ \texttt{\detokenize{#2}} is an image of a third-party
publication, omitted from the public release; see the locator in the cited-result box.}}}
\newcommand{\shot}[2][\textwidth]{%
  \IfFileExists{shots/#2}{\includegraphics[width=#1]{shots/#2}}{\shotmissing{#1}{#2}}}
\newcommand{\shotc}[2][\textwidth]{\begin{center}\shot[#1]{#2}\end{center}}
"""
root = sys.argv[1]; os.chdir(root)
s = open('rigor_preamble.tex').read()
if '\\shot' not in s:
    open('rigor_preamble.tex', 'w').write(s.rstrip('\n') + '\n' + MACRO)
defn   = re.compile(r'^.*?(?:\\providecommand\{\\shot\}\{\})?\\(?:re)?newcommand\{\\shot\}\[2\]\{.*$', re.M)
legacy = re.compile(r'\\shot\{([^{}]+\.(?:png|jpg))\}\{([0-9.]+)\}')
rawopt = re.compile(r'\\includegraphics\[width=([^\]]+)\]\{shots/([^{}]+)\}')
rawbar = re.compile(r'\\includegraphics\{shots/([^{}]+)\}')
f_, d_, l_, r_ = 0, 0, 0, 0
for f in sorted(glob.glob('*.tex')):
    if f == 'rigor_preamble.tex': continue
    t = o = open(f).read()
    t, nd = defn.subn(lambda m: '% [local \\shot definition removed: canonical macro in rigor_preamble.tex]', t)
    t, nl = legacy.subn(lambda m: '\\shotc[' + m.group(2) + '\\textwidth]{' + m.group(1) + '}', t)
    t, nr = rawopt.subn(lambda m: '\\shot[' + m.group(1) + ']{' + m.group(2) + '}', t)
    t, nb = rawbar.subn(lambda m: '\\shot{' + m.group(1) + '}', t)
    if t != o:
        open(f, 'w').write(t); f_ += 1; d_ += nd; l_ += nl; r_ += nr + nb
print(f"convert_shots: {f_} files, {d_} local definitions removed, {l_+r_} image calls converted")
