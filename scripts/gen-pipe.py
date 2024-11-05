#!/usr/bin/env python3

out = ''

count = 25

for i in range(0, count):
    out += f"_T{i} = TypeVar('_T{i}')\n"

out += '\n'

for i in range(0, count):
    out += '@overload\n'
    out += f"def apply(ctx: Context, input: _T0"
    for k in range(0, i):
        out += f", f{k}: Pass[_T{k}, _T{k+1}]"
    out += f', /) -> _T{i}: ...\n\n'

print(out)
