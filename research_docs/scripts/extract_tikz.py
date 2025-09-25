#!/usr/bin/env python3
"""
Extract all tikzpicture environments from a Beamer LaTeX file and write standalone .tex files
into research_docs/figures/fig_<n>.tex for compilation.

Usage: python3 scripts/extract_tikz.py ../cyberwheel_slides_final.tex
"""
import sys, os, re
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: extract_tikz.py <path-to-tex>")
    sys.exit(1)

src = Path(sys.argv[1])
if not src.exists():
    print("File not found:", src)
    sys.exit(1)

outdir = src.parent / 'figures'
outdir.mkdir(exist_ok=True)

text = src.read_text(encoding='utf-8')
# naive regex to extract tikzpicture blocks (multiline)
pattern = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)
blocks = pattern.findall(text)

print(f"Found {len(blocks)} tikzpicture blocks")

preamble = r'''% standalone wrapper for a tikz picture
\documentclass[tikz,border=2pt]{standalone}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows,positioning,shadows,patterns,arrows.meta,calc}
\begin{document}
'''

for i, blk in enumerate(blocks, start=1):
    fname = outdir / f'fig_{i}.tex'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(preamble + '\n' + blk + '\n\\end{document}\n')
    print('Wrote', fname)

print('Done. Compile these with pdflatex or tectonic in the figures folder.')
