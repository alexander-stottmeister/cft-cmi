#!/usr/bin/env python3
"""Make absolute paths in the python scripts relative to the repository root.
Usage: fix_paths.py <repo-root> <absolute-prefix-to-remove>"""
import re, os, sys
root, PREFIX = sys.argv[1], sys.argv[2].rstrip('/')
os.chdir(root); nf = ns = 0
for dp, dn, fns in os.walk('.'):
    dn[:] = [d for d in dn if d not in ('__pycache__', '.git')]
    for fn in fns:
        if not fn.endswith('.py'): continue
        p = os.path.join(dp, fn); t = open(p).read()
        if PREFIX not in t: continue
        up = "".join([", '..'"] * os.path.relpath(p, '.').count(os.sep))
        def sub(m):
            q, rel = m.group(1), m.group(2).strip('/')
            return "_ROOT" if not rel else f"_os.path.join(_ROOT, {q}{rel}{q})"
        t, k = re.subn(r"(['\"])" + re.escape(PREFIX) + r"/?([^'\"]*)\1", sub, t)
        # merge implicit string continuations broken by the substitution
        t = re.sub(r"_os\.path\.join\(_ROOT, (['\"])([^'\"]*)\1\)(\s*)(f?['\"][^'\"]*['\"])",
                   lambda m: f"_os.path.join(_ROOT, {m.group(1)}{m.group(2)}{m.group(1)},{m.group(3)}{m.group(4)})", t)
        header = ("import os as _os\n_ROOT = _os.path.abspath(_os.path.join("
                  "_os.path.dirname(_os.path.abspath(__file__))" + up + "))\n")
        open(p, 'w').write(header + t); nf += 1; ns += k
print(f"fix_paths: {nf} files, {ns} absolute literals rewritten")
