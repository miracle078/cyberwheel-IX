import sys, re
fname = sys.argv[1]
stack=[]
pat = re.compile(r'\\(begin|end)\{([^\}]+)\}')
with open(fname,'r',encoding='utf-8') as f:
    for i,l in enumerate(f,1):
        for m in pat.finditer(l):
            typ,env = m.group(1),m.group(2)
            if typ=='begin':
                stack.append((env,i))
            else: # end
                if stack and stack[-1][0]==env:
                    stack.pop()
                else:
                    print(f"Unmatched \\end{{{env}}} at line {i}")
if stack:
    print("Remaining unclosed begins (top is last):")
    for env,line in stack[::-1]:
        print(f"  \\begin{{{env}}} at line {line}")
else:
    print("All begin/end pairs appear balanced.")