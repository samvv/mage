#!/usr/bin/env python3

out = ''

count = 25

for i in range(0, count):
    out += f"_T{i} = TypeVar('_T{i}')\n"

out += '\n'

for i in range(0, count):
    out += '@overload\n'
    out += f"def pipe(arg0: _T0"
    for k in range(0, i):
        out += f", f{k}: Callable[[_T{k}], _T{k+1}]"
    out += f', /) -> _T{i}: ...\n\n'

out += f"""
def pipe(arg0, fs):
    result = arg0
    for f in fs:
        result = f(result)
    return result
"""

print(out)
