#!/usr/bin/env python3

out = ''

count = 25

for i in range(1, count):
    out += '@overload\n'
    out += f"def pipeline["
    first = True
    for k in range(0, i+1):
        if first: first = False
        else: out += ', '
        out += f'T{k}'
    out += "]("
    first = True
    for k in range(0, i):
        if first: first = False
        else: out += ', '
        out += f"p{k}: Pass[T{k}, T{k+1}]"
    out += f', /) -> Pass[T0, T{i}]: ...\n\n'

print(out)
