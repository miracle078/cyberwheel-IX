#!/usr/bin/env python3
"""
Simple checker to find unbalanced \begin{...} / \end{...} in a LaTeX file.
Usage: python3 check_tex_envs.py <file>
If no file is given, it defaults to research_docs/cyberwheel_slides_final.tex
"""
import re, sys
from pathlib import Path

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
else:
    path = Path(__file__).parent.parent / 'research_docs' / 'cyberwheel_slides_final.tex'

if not path.exists():
    print('File not found:', path)
    sys.exit(1)

text = path.read_text(encoding='utf-8')
# remove comments
text_nocomment = re.sub(r"%.*", "", text)

begins = [(m.group(1), m.start()) for m in re.finditer(r"\\begin\{([^}]+)\}", text_nocomment)]
ends = [(m.group(1), m.start()) for m in re.finditer(r"\\end\{([^}]+)\}", text_nocomment)]

stack = []
idx_beg = 0
idx_end = 0

# naive stack-based matching
items = []
for m in re.finditer(r"(\\begin\{([^}]+)\})|(\\end\{([^}]+)\})", text_nocomment):
    if m.group(1):
        items.append(('begin', m.group(2), m.start()))
    else:
        items.append(('end', m.group(4), m.start()))

stack = []
unmatched = []
for typ, name, pos in items:
    lineno = text[:pos].count('\n') + 1
    if typ == 'begin':
        stack.append((name, lineno))
    else:
        if stack and stack[-1][0] == name:
            stack.pop()
        else:
            unmatched.append(('end', name, lineno))

print('Unclosed \begin{...} remaining on stack:')
for name, lineno in stack:
    print(f"  \\begin{{{name}}} at line {lineno}")

print('\nUnmatched \end{...}:')
for typ, name, lineno in unmatched:
    print(f"  \\end{{{name}}} at line {lineno}")
