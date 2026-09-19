r"""Combine the standalone cited_R*.tex documents into one compendium cited_results_all.tex.
Packages/theorem environments of the parts go (deduplicated) into the preamble; macro definitions are re-issued
inside the body right before each \part (as \providecommand{}{}+\renewcommand), so each part keeps its own macros."""
import re, glob
def split_defs(text):
    r"""yield (kind, name, rest) for \newcommand/\renewcommand/\providecommand/\DeclareMathOperator occurrences"""
    i=0; out=[]
    pat=re.compile(r'\\(newcommand|renewcommand|providecommand|DeclareMathOperator)\*?\s*\{?(\\[A-Za-z]+)\}?')
    while True:
        m=pat.search(text,i)
        if not m: break
        j=m.end(); args=''
        while j<len(text) and text[j]=='[':
            k=text.index(']',j); args+=text[j:k+1]; j=k+1
        # brace-matched body
        assert text[j]=='{', text[j:j+40]
        depth=0; k=j
        while True:
            if text[k]=='{': depth+=1
            elif text[k]=='}':
                depth-=1
                if depth==0: break
            k+=1
        out.append((m.group(1), m.group(2), args, text[j:k+1])); i=k+1
    return out
parts=[]; pre=[]
for fn in sorted(glob.glob('cited_R*.tex')):
    s=open(fn).read()
    head=s[:s.index(r'\begin{document}')]
    k=head.find(r'\input{rigor_preamble}')
    extra=head[k+len(r'\input{rigor_preamble}'):] if k>=0 else ''
    local=[]
    for kind,name,args,body in split_defs(extra):
        if kind=='DeclareMathOperator': local.append(f"\\providecommand{{{name}}}{{}}\\renewcommand{{{name}}}{{\\operatorname{body}}}")
        else: local.append(f"\\providecommand{{{name}}}{{}}\\renewcommand{{{name}}}{args}{body}")
    for line in extra.splitlines():
        t=line.strip()
        if t.startswith((r'\usepackage', r'\newtheorem', r'\theoremstyle', r'\graphicspath')) and 'cleveref' not in t and t not in pre: pre.append(t)
    body=s[s.index(r'\begin{document}')+len(r'\begin{document}'):s.rindex(r'\end{document}')]
    body=re.sub(r'\\maketitle','',body); body=re.sub(r'\\tableofcontents','',body)
    parts.append(f"\\part{{{fn.replace('.tex','').replace('_',' ')}}}\n"+"\n".join(local)+"\n"+body)
out=r"""\documentclass[11pt]{article}\input{rigor_preamble}
"""+"\n".join(pre)+r"""
\usepackage[capitalise,nameinlink]{cleveref}
\title{Compendium of cited results with screenshots and usage cross-checks}\author{}\date{}
\begin{document}\maketitle\tableofcontents\clearpage
"""+"\n\\clearpage\n".join(parts)+"\n\\end{document}\n"
open('cited_results_all.tex','w').write(out); print("written cited_results_all.tex with", len(parts), "parts;", len(pre), "preamble lines")
