#!/usr/bin/env python3

out = ''

count = 25

for i in range(0, count):
    out += f"_T{i} = TypeVar('_T{i}')\n"

out += '\n'

for i in range(1, count):
    out += '@overload\n'
    out += f"def pipeline("
    first = True
    for k in range(0, i):
        if first: first = False
        else: out += ', '
        out += f"p{k}: Pass[_T{k}, _T{k+1}]"
    out += f', /) -> Pass[_T0, _T{i}]: ...\n\n'

print(out)
