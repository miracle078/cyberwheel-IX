#!/usr/bin/env python3
"""
Replace each tikzpicture environment in a LaTeX file with \includegraphics referencing
research_docs/figures/fig_<n>.svg. Writes output to research_docs/cyberwheel_slides_for_pptx.tex

Usage: python3 scripts/replace_tikz_with_images.py <input.tex>
"""
import sys
from pathlib import Path
import re

if len(sys.argv) < 2:
    print('Usage: replace_tikz_with_images.py <input.tex>')
    sys.exit(1)

src = Path(sys.argv[1])
if not src.exists():
    print('File not found:', src)
    sys.exit(1)

out = src.parent / 'cyberwheel_slides_for_pptx.tex'
text = src.read_text(encoding='utf-8')

pattern = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)

count = 0

def repl(m):
    global count
    count += 1
    return f"\\begin{{center}}\\includegraphics[width=0.95\\columnwidth]{{figures/fig_{count}.svg}}\\end{{center}}"

new = pattern.sub(repl, text)
out.write_text(new, encoding='utf-8')
print('Wrote', out, 'with', count, 'replacements')
