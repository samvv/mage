
from typing import TypeGuard, Iterable, Iterator, TypeAlias, TypeGuard, Any, Callable, TypeVar, Never

class TextPos:

    def __init__(self, offset: int, line: int, column: int) -> None:
        self.offset = offset
        self.line = line
        self.column = column

class Span:

    def __init__(self, start_offset: int, end_offset: int) -> None:
        self.start_offset = start_offset
        self.end_offset = end_offset

    def __len__(self) -> int:
        return self.end_offset - self.start_offset

class _BaseSyntax:
    pass

class _BaseToken(_BaseSyntax):

    def __init__(self, span: Span | None = None) -> None:
        super().__init__()
        self.span = span

class _BaseNode(_BaseSyntax):

    def __init__(self) -> None:
        super().__init__()
        pass

def is_py_token(value: Any) -> TypeGuard['PyToken']:
    return isinstance(value, _BaseToken)

def is_py_node(value: Any) -> TypeGuard['PyNode']:
    return isinstance(value, _BaseNode)

def is_py_syntax(value: Any) -> TypeGuard['PySyntax']:
    return isinstance(value, _BaseSyntax)

_T = TypeVar('_T')
_P = TypeVar('_P')

class Punctuated[_T, _P]:

    def __init__(self, elements: Iterable[tuple[_T, _P | None]] | None = None) -> None:
        self.elements = []
        self.last = None
        if elements is not None:
          for element, sep  in elements:
              self.append(element, sep)

    def append(self, element: _T, separator: _P | None = None) -> None:
        if separator is None:
            assert(self.last is None)
            self.last = element
        else:
            self.elements.append((element, separator))

    def __iter__(self) -> Iterator[tuple[_T, _P | None]]:
        for item in self.elements:
            yield item
        if self.last is not None:
            yield self.last, None

class PyIdent(_BaseToken):
    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyInteger(_BaseToken):
    def __init__(self, value: int, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyFloat(_BaseToken):
    def __init__(self, value: float, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyString(_BaseToken):
    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PySlice(_BaseNode):
    def __init__(self, lower: 'PyExpr', upper: 'PyExpr', *, colon: 'PyColon | None' = None) -> None:
        self.lower: PyExpr = lower
        self.upper: PyExpr = upper
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")


PyPattern: TypeAlias = 'PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern'


def is_py_pattern(value: Any) -> TypeGuard[PyPattern]:
    return isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern)


class PyNamedPattern(_BaseNode):
    def __init__(self, name: 'str | PyIdent') -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")


class PyAttrPattern(_BaseNode):
    def __init__(self, pattern: 'PyPattern', name: 'str | PyIdent', *, dot: 'PyDot | None' = None) -> None:
        self.pattern: PyPattern = pattern
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        if dot is None:
            self.dot: PyDot = PyDot()
        elif isinstance(dot, PyDot):
            self.dot: PyDot = dot
        else:
            raise ValueError("the field 'dot' received an unrecognised value'")


class PySubscriptPattern(_BaseNode):
    def __init__(self, pattern: 'PyPattern', *, open_bracket: 'PyOpenBracket | None' = None, slices: 'list[PyPattern | PySlice] | list[tuple[PyPattern | PySlice, PyComma | None | None]] | Punctuated[PyPattern | PySlice, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.pattern: PyPattern = pattern
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            self.open_bracket: PyOpenBracket = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        if slices is None:
            self.slices: Punctuated[PyPattern | PySlice, PyComma] = Punctuated()
        elif isinstance(slices, list) or isinstance(slices, list) or isinstance(slices, Punctuated):
            new_slices = Punctuated()
            slices_iter = iter(slices)
            try:
                first_slices_element = next(slices_iter)
                while True:
                    try:
                        second_slices_element = next(slices_iter)
                        if isinstance(first_slices_element, tuple):
                            slices_value = first_slices_element[0]
                            slices_separator = first_slices_element[1]
                        else:
                            slices_value = first_slices_element
                            slices_separator = None
                        if is_py_pattern(slices_value):
                            new_slices_value = slices_value
                        elif isinstance(slices_value, PySlice):
                            new_slices_value = slices_value
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        if slices_separator is None:
                            new_slices_separator = PyComma()
                        elif isinstance(slices_separator, PyComma):
                            new_slices_separator = slices_separator
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        new_slices.append(new_slices_value, new_slices_separator)
                        first_slices_element = second_slices_element
                    except StopIteration:
                        if isinstance(first_slices_element, tuple):
                            slices_value = first_slices_element[0]
                            assert(first_slices_element[1] is None)
                        else:
                            slices_value = first_slices_element
                        if is_py_pattern(slices_value):
                            new_slices_value = slices_value
                        elif isinstance(slices_value, PySlice):
                            new_slices_value = slices_value
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        new_slices.append(new_slices_value)
                        break

            except StopIteration:
                pass
            self.slices: Punctuated[PyPattern | PySlice, PyComma] = new_slices
        else:
            raise ValueError("the field 'slices' received an unrecognised value'")
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            self.close_bracket: PyCloseBracket = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")


class PyStarredPattern(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.expr: PyExpr = expr
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            self.asterisk: PyAsterisk = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")


class PyListPattern(_BaseNode):
    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'list[PyPattern] | list[tuple[PyPattern, PyComma | None | None]] | Punctuated[PyPattern, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            self.open_bracket: PyOpenBracket = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        if elements is None:
            self.elements: Punctuated[PyPattern, PyComma] = Punctuated()
        elif isinstance(elements, list) or isinstance(elements, list) or isinstance(elements, Punctuated):
            new_elements = Punctuated()
            elements_iter = iter(elements)
            try:
                first_elements_element = next(elements_iter)
                while True:
                    try:
                        second_elements_element = next(elements_iter)
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            elements_separator = first_elements_element[1]
                        else:
                            elements_value = first_elements_element
                            elements_separator = None
                        new_elements_value = elements_value
                        if elements_separator is None:
                            new_elements_separator = PyComma()
                        elif isinstance(elements_separator, PyComma):
                            new_elements_separator = elements_separator
                        else:
                            raise ValueError("the field 'elements' received an unrecognised value'")
                        new_elements.append(new_elements_value, new_elements_separator)
                        first_elements_element = second_elements_element
                    except StopIteration:
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            assert(first_elements_element[1] is None)
                        else:
                            elements_value = first_elements_element
                        new_elements_value = elements_value
                        new_elements.append(new_elements_value)
                        break

            except StopIteration:
                pass
            self.elements: Punctuated[PyPattern, PyComma] = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            self.close_bracket: PyCloseBracket = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")


class PyTuplePattern(_BaseNode):
    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'list[PyPattern] | list[tuple[PyPattern, PyComma | None | None]] | Punctuated[PyPattern, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            self.open_paren: PyOpenParen = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        if elements is None:
            self.elements: Punctuated[PyPattern, PyComma] = Punctuated()
        elif isinstance(elements, list) or isinstance(elements, list) or isinstance(elements, Punctuated):
            new_elements = Punctuated()
            elements_iter = iter(elements)
            try:
                first_elements_element = next(elements_iter)
                while True:
                    try:
                        second_elements_element = next(elements_iter)
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            elements_separator = first_elements_element[1]
                        else:
                            elements_value = first_elements_element
                            elements_separator = None
                        new_elements_value = elements_value
                        if elements_separator is None:
                            new_elements_separator = PyComma()
                        elif isinstance(elements_separator, PyComma):
                            new_elements_separator = elements_separator
                        else:
                            raise ValueError("the field 'elements' received an unrecognised value'")
                        new_elements.append(new_elements_value, new_elements_separator)
                        first_elements_element = second_elements_element
                    except StopIteration:
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            assert(first_elements_element[1] is None)
                        else:
                            elements_value = first_elements_element
                        new_elements_value = elements_value
                        new_elements.append(new_elements_value)
                        break

            except StopIteration:
                pass
            self.elements: Punctuated[PyPattern, PyComma] = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            self.close_paren: PyCloseParen = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")


PyExpr: TypeAlias = 'PyAttrExpr | PyCallExpr | PyConstExpr | PyGeneratorExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr'


def is_py_expr(value: Any) -> TypeGuard[PyExpr]:
    return isinstance(value, PyAttrExpr) or isinstance(value, PyCallExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyListExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyTupleExpr)


class PyGuard(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None) -> None:
        self.expr: PyExpr = expr
        if if_keyword is None:
            self.if_keyword: PyIfKeyword = PyIfKeyword()
        elif isinstance(if_keyword, PyIfKeyword):
            self.if_keyword: PyIfKeyword = if_keyword
        else:
            raise ValueError("the field 'if_keyword' received an unrecognised value'")


class PyComprehension(_BaseNode):
    def __init__(self, pattern: 'PyPattern', target: 'PyExpr', *, async_keyword: 'PyAsyncKeyword | None' = None, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, guards: 'list[PyGuard] | None' = None) -> None:
        self.pattern: PyPattern = pattern
        self.target: PyExpr = target
        if isinstance(async_keyword, PyAsyncKeyword):
            self.async_keyword: PyAsyncKeyword | None = async_keyword
        elif async_keyword is None:
            self.async_keyword: PyAsyncKeyword | None = None
        else:
            raise ValueError("the field 'async_keyword' received an unrecognised value'")
        if for_keyword is None:
            self.for_keyword: PyForKeyword = PyForKeyword()
        elif isinstance(for_keyword, PyForKeyword):
            self.for_keyword: PyForKeyword = for_keyword
        else:
            raise ValueError("the field 'for_keyword' received an unrecognised value'")
        if in_keyword is None:
            self.in_keyword: PyInKeyword = PyInKeyword()
        elif isinstance(in_keyword, PyInKeyword):
            self.in_keyword: PyInKeyword = in_keyword
        else:
            raise ValueError("the field 'in_keyword' received an unrecognised value'")
        if guards is None:
            self.guards: list[PyGuard] = list()
        elif isinstance(guards, list):
            new_guards = list()
            for guards_element in guards:
                new_guards_element = guards_element
                new_guards.append(new_guards_element)

            self.guards: list[PyGuard] = new_guards
        else:
            raise ValueError("the field 'guards' received an unrecognised value'")


class PyGeneratorExpr(_BaseNode):
    def __init__(self, element: 'PyExpr', *, generators: 'list[PyComprehension] | None' = None) -> None:
        self.element: PyExpr = element
        if generators is None:
            self.generators: list[PyComprehension] = list()
        elif isinstance(generators, list):
            new_generators = list()
            for generators_element in generators:
                new_generators_element = generators_element
                new_generators.append(new_generators_element)

            self.generators: list[PyComprehension] = new_generators
        else:
            raise ValueError("the field 'generators' received an unrecognised value'")


class PyConstExpr(_BaseNode):
    def __init__(self, literal: 'str | PyString | float | PyFloat | int | PyInteger') -> None:
        if isinstance(literal, str):
            self.literal: PyString | PyFloat | PyInteger = PyString(literal)
        elif isinstance(literal, PyString):
            self.literal: PyString | PyFloat | PyInteger = literal
        elif isinstance(literal, float):
            self.literal: PyString | PyFloat | PyInteger = PyFloat(literal)
        elif isinstance(literal, PyFloat):
            self.literal: PyString | PyFloat | PyInteger = literal
        elif isinstance(literal, int):
            self.literal: PyString | PyFloat | PyInteger = PyInteger(literal)
        elif isinstance(literal, PyInteger):
            self.literal: PyString | PyFloat | PyInteger = literal
        else:
            raise ValueError("the field 'literal' received an unrecognised value'")


class PyNestExpr(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.expr: PyExpr = expr
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            self.open_paren: PyOpenParen = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            self.close_paren: PyCloseParen = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")


class PyNamedExpr(_BaseNode):
    def __init__(self, name: 'str | PyIdent') -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")


class PyAttrExpr(_BaseNode):
    def __init__(self, expr: 'PyExpr', name: 'str | PyIdent', *, dot: 'PyDot | None' = None) -> None:
        self.expr: PyExpr = expr
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        if dot is None:
            self.dot: PyDot = PyDot()
        elif isinstance(dot, PyDot):
            self.dot: PyDot = dot
        else:
            raise ValueError("the field 'dot' received an unrecognised value'")


class PySubscriptExpr(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, open_bracket: 'PyOpenBracket | None' = None, slices: 'list[PyExpr | PySlice] | list[tuple[PyExpr | PySlice, PyComma | None | None]] | Punctuated[PyExpr | PySlice, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.expr: PyExpr = expr
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            self.open_bracket: PyOpenBracket = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        if slices is None:
            self.slices: Punctuated[PyExpr | PySlice, PyComma] = Punctuated()
        elif isinstance(slices, list) or isinstance(slices, list) or isinstance(slices, Punctuated):
            new_slices = Punctuated()
            slices_iter = iter(slices)
            try:
                first_slices_element = next(slices_iter)
                while True:
                    try:
                        second_slices_element = next(slices_iter)
                        if isinstance(first_slices_element, tuple):
                            slices_value = first_slices_element[0]
                            slices_separator = first_slices_element[1]
                        else:
                            slices_value = first_slices_element
                            slices_separator = None
                        if is_py_expr(slices_value):
                            new_slices_value = slices_value
                        elif isinstance(slices_value, PySlice):
                            new_slices_value = slices_value
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        if slices_separator is None:
                            new_slices_separator = PyComma()
                        elif isinstance(slices_separator, PyComma):
                            new_slices_separator = slices_separator
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        new_slices.append(new_slices_value, new_slices_separator)
                        first_slices_element = second_slices_element
                    except StopIteration:
                        if isinstance(first_slices_element, tuple):
                            slices_value = first_slices_element[0]
                            assert(first_slices_element[1] is None)
                        else:
                            slices_value = first_slices_element
                        if is_py_expr(slices_value):
                            new_slices_value = slices_value
                        elif isinstance(slices_value, PySlice):
                            new_slices_value = slices_value
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        new_slices.append(new_slices_value)
                        break

            except StopIteration:
                pass
            self.slices: Punctuated[PyExpr | PySlice, PyComma] = new_slices
        else:
            raise ValueError("the field 'slices' received an unrecognised value'")
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            self.close_bracket: PyCloseBracket = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")


class PyStarredExpr(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.expr: PyExpr = expr
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            self.asterisk: PyAsterisk = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")


class PyListExpr(_BaseNode):
    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            self.open_bracket: PyOpenBracket = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        if elements is None:
            self.elements: Punctuated[PyExpr, PyComma] = Punctuated()
        elif isinstance(elements, list) or isinstance(elements, list) or isinstance(elements, Punctuated):
            new_elements = Punctuated()
            elements_iter = iter(elements)
            try:
                first_elements_element = next(elements_iter)
                while True:
                    try:
                        second_elements_element = next(elements_iter)
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            elements_separator = first_elements_element[1]
                        else:
                            elements_value = first_elements_element
                            elements_separator = None
                        new_elements_value = elements_value
                        if elements_separator is None:
                            new_elements_separator = PyComma()
                        elif isinstance(elements_separator, PyComma):
                            new_elements_separator = elements_separator
                        else:
                            raise ValueError("the field 'elements' received an unrecognised value'")
                        new_elements.append(new_elements_value, new_elements_separator)
                        first_elements_element = second_elements_element
                    except StopIteration:
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            assert(first_elements_element[1] is None)
                        else:
                            elements_value = first_elements_element
                        new_elements_value = elements_value
                        new_elements.append(new_elements_value)
                        break

            except StopIteration:
                pass
            self.elements: Punctuated[PyExpr, PyComma] = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            self.close_bracket: PyCloseBracket = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")


class PyTupleExpr(_BaseNode):
    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            self.open_paren: PyOpenParen = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        if elements is None:
            self.elements: Punctuated[PyExpr, PyComma] = Punctuated()
        elif isinstance(elements, list) or isinstance(elements, list) or isinstance(elements, Punctuated):
            new_elements = Punctuated()
            elements_iter = iter(elements)
            try:
                first_elements_element = next(elements_iter)
                while True:
                    try:
                        second_elements_element = next(elements_iter)
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            elements_separator = first_elements_element[1]
                        else:
                            elements_value = first_elements_element
                            elements_separator = None
                        new_elements_value = elements_value
                        if elements_separator is None:
                            new_elements_separator = PyComma()
                        elif isinstance(elements_separator, PyComma):
                            new_elements_separator = elements_separator
                        else:
                            raise ValueError("the field 'elements' received an unrecognised value'")
                        new_elements.append(new_elements_value, new_elements_separator)
                        first_elements_element = second_elements_element
                    except StopIteration:
                        if isinstance(first_elements_element, tuple):
                            elements_value = first_elements_element[0]
                            assert(first_elements_element[1] is None)
                        else:
                            elements_value = first_elements_element
                        new_elements_value = elements_value
                        new_elements.append(new_elements_value)
                        break

            except StopIteration:
                pass
            self.elements: Punctuated[PyExpr, PyComma] = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            self.close_paren: PyCloseParen = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")


PyArg: TypeAlias = 'PyKeywordArg | PyExpr'


def is_py_arg(value: Any) -> TypeGuard[PyArg]:
    return isinstance(value, PyKeywordArg) or is_py_expr(value)


class PyKeywordArg(_BaseNode):
    def __init__(self, name: 'str | PyIdent', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.expr: PyExpr = expr
        if equals is None:
            self.equals: PyEquals = PyEquals()
        elif isinstance(equals, PyEquals):
            self.equals: PyEquals = equals
        else:
            raise ValueError("the field 'equals' received an unrecognised value'")


class PyCallExpr(_BaseNode):
    def __init__(self, operator: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, args: 'list[PyArg] | list[tuple[PyArg, PyComma | None | None]] | Punctuated[PyArg, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.operator: PyExpr = operator
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            self.open_paren: PyOpenParen = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        if args is None:
            self.args: Punctuated[PyArg, PyComma] = Punctuated()
        elif isinstance(args, list) or isinstance(args, list) or isinstance(args, Punctuated):
            new_args = Punctuated()
            args_iter = iter(args)
            try:
                first_args_element = next(args_iter)
                while True:
                    try:
                        second_args_element = next(args_iter)
                        if isinstance(first_args_element, tuple):
                            args_value = first_args_element[0]
                            args_separator = first_args_element[1]
                        else:
                            args_value = first_args_element
                            args_separator = None
                        new_args_value = args_value
                        if args_separator is None:
                            new_args_separator = PyComma()
                        elif isinstance(args_separator, PyComma):
                            new_args_separator = args_separator
                        else:
                            raise ValueError("the field 'args' received an unrecognised value'")
                        new_args.append(new_args_value, new_args_separator)
                        first_args_element = second_args_element
                    except StopIteration:
                        if isinstance(first_args_element, tuple):
                            args_value = first_args_element[0]
                            assert(first_args_element[1] is None)
                        else:
                            args_value = first_args_element
                        new_args_value = args_value
                        new_args.append(new_args_value)
                        break

            except StopIteration:
                pass
            self.args: Punctuated[PyArg, PyComma] = new_args
        else:
            raise ValueError("the field 'args' received an unrecognised value'")
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            self.close_paren: PyCloseParen = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")


PyPrefixOp: TypeAlias = 'PyNotKeyword | PyPlus | PyHyphen | PyTilde'


def is_py_prefix_op(value: Any) -> TypeGuard[PyPrefixOp]:
    return isinstance(value, PyNotKeyword) or isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyTilde)


class PyPrefixExpr(_BaseNode):
    def __init__(self, prefix_op: 'PyPrefixOp', expr: 'PyExpr') -> None:
        self.prefix_op: PyPrefixOp = prefix_op
        self.expr: PyExpr = expr


PyInfixOp: TypeAlias = 'PyPlus | PyHyphen | PyAsterisk | PySlash | PySlashSlash | PyPercenct | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyAtSign | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | tuple[PyIsKeyword, PyNotKeyword] | PyInKeyword | tuple[PyNotKeyword, PyInKeyword]'


def is_py_infix_op(value: Any) -> TypeGuard[PyInfixOp]:
    return isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyAsterisk) or isinstance(value, PySlash) or isinstance(value, PySlashSlash) or isinstance(value, PyPercenct) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyVerticalBar) or isinstance(value, PyCaret) or isinstance(value, PyAmpersand) or isinstance(value, PyAtSign) or isinstance(value, PyOrKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyEqualsEquals) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyLessThan) or isinstance(value, PyLessThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyIsKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyIsKeyword) and isinstance(value[1], PyNotKeyword)) or isinstance(value, PyInKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyNotKeyword) and isinstance(value[1], PyInKeyword))


class PyInfixExpr(_BaseNode):
    def __init__(self, left: 'PyExpr', op: 'PyInfixOp', right: 'PyExpr') -> None:
        self.left: PyExpr = left
        self.op: PyInfixOp = op
        self.right: PyExpr = right


PyStmt: TypeAlias = 'PyAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyIfStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt'


def is_py_stmt(value: Any) -> TypeGuard[PyStmt]:
    return isinstance(value, PyAssignStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyClassDef) or isinstance(value, PyContinueStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyForStmt) or isinstance(value, PyFuncDef) or isinstance(value, PyIfStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyTryStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyWhileStmt)


class PyRetStmt(_BaseNode):
    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> None:
        if return_keyword is None:
            self.return_keyword: PyReturnKeyword = PyReturnKeyword()
        elif isinstance(return_keyword, PyReturnKeyword):
            self.return_keyword: PyReturnKeyword = return_keyword
        else:
            raise ValueError("the field 'return_keyword' received an unrecognised value'")
        if is_py_expr(expr):
            self.expr: PyExpr | None = expr
        elif expr is None:
            self.expr: PyExpr | None = None
        else:
            raise ValueError("the field 'expr' received an unrecognised value'")


class PyExprStmt(_BaseNode):
    def __init__(self, expr: 'PyExpr') -> None:
        self.expr: PyExpr = expr


class PyAssignStmt(_BaseNode):
    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, equals: 'PyEquals | None' = None) -> None:
        self.pattern: PyPattern = pattern
        self.expr: PyExpr = expr
        if is_py_expr(annotation):
            self.annotation: tuple[PyColon, PyExpr] | None = (PyColon(), annotation)
        elif isinstance(annotation, tuple):
            assert(isinstance(annotation, tuple))
            annotation_0 = annotation[0]
            if annotation_0 is None:
                new_annotation_0 = PyColon()
            elif isinstance(annotation_0, PyColon):
                new_annotation_0 = annotation_0
            else:
                raise ValueError("the field 'annotation' received an unrecognised value'")
            annotation_1 = annotation[1]
            new_annotation_1 = annotation_1
            self.annotation: tuple[PyColon, PyExpr] | None = (new_annotation_0, new_annotation_1)
        elif annotation is None:
            self.annotation: tuple[PyColon, PyExpr] | None = None
        else:
            raise ValueError("the field 'annotation' received an unrecognised value'")
        if equals is None:
            self.equals: PyEquals = PyEquals()
        elif isinstance(equals, PyEquals):
            self.equals: PyEquals = equals
        else:
            raise ValueError("the field 'equals' received an unrecognised value'")


class PyPassStmt(_BaseNode):
    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None) -> None:
        if pass_keyword is None:
            self.pass_keyword: PyPassKeyword = PyPassKeyword()
        elif isinstance(pass_keyword, PyPassKeyword):
            self.pass_keyword: PyPassKeyword = pass_keyword
        else:
            raise ValueError("the field 'pass_keyword' received an unrecognised value'")


class PyIfCase(_BaseNode):
    def __init__(self, test: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        self.test: PyExpr = test
        if if_keyword is None:
            self.if_keyword: PyIfKeyword = PyIfKeyword()
        elif isinstance(if_keyword, PyIfKeyword):
            self.if_keyword: PyIfKeyword = if_keyword
        else:
            raise ValueError("the field 'if_keyword' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")


class PyElifCase(_BaseNode):
    def __init__(self, test: 'PyExpr', *, elif_keyword: 'PyElifKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        self.test: PyExpr = test
        if elif_keyword is None:
            self.elif_keyword: PyElifKeyword = PyElifKeyword()
        elif isinstance(elif_keyword, PyElifKeyword):
            self.elif_keyword: PyElifKeyword = elif_keyword
        else:
            raise ValueError("the field 'elif_keyword' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")


class PyElseCase(_BaseNode):
    def __init__(self, *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if else_keyword is None:
            self.else_keyword: PyElseKeyword = PyElseKeyword()
        elif isinstance(else_keyword, PyElseKeyword):
            self.else_keyword: PyElseKeyword = else_keyword
        else:
            raise ValueError("the field 'else_keyword' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")


class PyIfStmt(_BaseNode):
    def __init__(self, first: 'PyIfCase', *, alternatives: 'list[PyElifCase] | None' = None, last: 'PyElseCase | None' = None) -> None:
        self.first: PyIfCase = first
        if alternatives is None:
            self.alternatives: list[PyElifCase] = list()
        elif isinstance(alternatives, list):
            new_alternatives = list()
            for alternatives_element in alternatives:
                new_alternatives_element = alternatives_element
                new_alternatives.append(new_alternatives_element)

            self.alternatives: list[PyElifCase] = new_alternatives
        else:
            raise ValueError("the field 'alternatives' received an unrecognised value'")
        if isinstance(last, PyElseCase):
            self.last: PyElseCase | None = last
        elif last is None:
            self.last: PyElseCase | None = None
        else:
            raise ValueError("the field 'last' received an unrecognised value'")


class PyDeleteStmt(_BaseNode):
    def __init__(self, pattern: 'PyPattern', *, del_keyword: 'PyDelKeyword | None' = None) -> None:
        self.pattern: PyPattern = pattern
        if del_keyword is None:
            self.del_keyword: PyDelKeyword = PyDelKeyword()
        elif isinstance(del_keyword, PyDelKeyword):
            self.del_keyword: PyDelKeyword = del_keyword
        else:
            raise ValueError("the field 'del_keyword' received an unrecognised value'")


class PyRaiseStmt(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, raise_keyword: 'PyRaiseKeyword | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None) -> None:
        self.expr: PyExpr = expr
        if raise_keyword is None:
            self.raise_keyword: PyRaiseKeyword = PyRaiseKeyword()
        elif isinstance(raise_keyword, PyRaiseKeyword):
            self.raise_keyword: PyRaiseKeyword = raise_keyword
        else:
            raise ValueError("the field 'raise_keyword' received an unrecognised value'")
        if is_py_expr(cause):
            self.cause: tuple[PyFromKeyword, PyExpr] | None = (PyFromKeyword(), cause)
        elif isinstance(cause, tuple):
            assert(isinstance(cause, tuple))
            cause_0 = cause[0]
            if cause_0 is None:
                new_cause_0 = PyFromKeyword()
            elif isinstance(cause_0, PyFromKeyword):
                new_cause_0 = cause_0
            else:
                raise ValueError("the field 'cause' received an unrecognised value'")
            cause_1 = cause[1]
            new_cause_1 = cause_1
            self.cause: tuple[PyFromKeyword, PyExpr] | None = (new_cause_0, new_cause_1)
        elif cause is None:
            self.cause: tuple[PyFromKeyword, PyExpr] | None = None
        else:
            raise ValueError("the field 'cause' received an unrecognised value'")


class PyForStmt(_BaseNode):
    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', *, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None, else_clause: 'PyStmt | list[PyStmt] | tuple[PyElseKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None) -> None:
        self.pattern: PyPattern = pattern
        self.expr: PyExpr = expr
        if for_keyword is None:
            self.for_keyword: PyForKeyword = PyForKeyword()
        elif isinstance(for_keyword, PyForKeyword):
            self.for_keyword: PyForKeyword = for_keyword
        else:
            raise ValueError("the field 'for_keyword' received an unrecognised value'")
        if in_keyword is None:
            self.in_keyword: PyInKeyword = PyInKeyword()
        elif isinstance(in_keyword, PyInKeyword):
            self.in_keyword: PyInKeyword = in_keyword
        else:
            raise ValueError("the field 'in_keyword' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        if is_py_stmt(else_clause):
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyElseKeyword(), PyColon(), else_clause)
        elif isinstance(else_clause, list):
            new_else_clause = list()
            for else_clause_element in else_clause:
                new_else_clause_element = else_clause_element
                new_else_clause.append(new_else_clause_element)

            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyElseKeyword(), PyColon(), new_else_clause)
        elif isinstance(else_clause, tuple):
            assert(isinstance(else_clause, tuple))
            else_clause_0 = else_clause[0]
            if else_clause_0 is None:
                new_else_clause_0 = PyElseKeyword()
            elif isinstance(else_clause_0, PyElseKeyword):
                new_else_clause_0 = else_clause_0
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            else_clause_1 = else_clause[1]
            if else_clause_1 is None:
                new_else_clause_1 = PyColon()
            elif isinstance(else_clause_1, PyColon):
                new_else_clause_1 = else_clause_1
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            else_clause_2 = else_clause[2]
            if is_py_stmt(else_clause_2):
                new_else_clause_2 = else_clause_2
            elif else_clause_2 is None:
                new_else_clause_2 = list()
            elif isinstance(else_clause_2, list):
                new_else_clause_2 = list()
                for else_clause_2_element in else_clause_2:
                    new_else_clause_2_element = else_clause_2_element
                    new_else_clause_2.append(new_else_clause_2_element)

                new_else_clause_2 = new_else_clause_2
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (new_else_clause_0, new_else_clause_1, new_else_clause_2)
        elif else_clause is None:
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")


class PyWhileStmt(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, while_keyword: 'PyWhileKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None, else_clause: 'PyStmt | list[PyStmt] | tuple[PyElseKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None) -> None:
        self.expr: PyExpr = expr
        if while_keyword is None:
            self.while_keyword: PyWhileKeyword = PyWhileKeyword()
        elif isinstance(while_keyword, PyWhileKeyword):
            self.while_keyword: PyWhileKeyword = while_keyword
        else:
            raise ValueError("the field 'while_keyword' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        if is_py_stmt(else_clause):
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyElseKeyword(), PyColon(), else_clause)
        elif isinstance(else_clause, list):
            new_else_clause = list()
            for else_clause_element in else_clause:
                new_else_clause_element = else_clause_element
                new_else_clause.append(new_else_clause_element)

            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyElseKeyword(), PyColon(), new_else_clause)
        elif isinstance(else_clause, tuple):
            assert(isinstance(else_clause, tuple))
            else_clause_0 = else_clause[0]
            if else_clause_0 is None:
                new_else_clause_0 = PyElseKeyword()
            elif isinstance(else_clause_0, PyElseKeyword):
                new_else_clause_0 = else_clause_0
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            else_clause_1 = else_clause[1]
            if else_clause_1 is None:
                new_else_clause_1 = PyColon()
            elif isinstance(else_clause_1, PyColon):
                new_else_clause_1 = else_clause_1
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            else_clause_2 = else_clause[2]
            if is_py_stmt(else_clause_2):
                new_else_clause_2 = else_clause_2
            elif else_clause_2 is None:
                new_else_clause_2 = list()
            elif isinstance(else_clause_2, list):
                new_else_clause_2 = list()
                for else_clause_2_element in else_clause_2:
                    new_else_clause_2_element = else_clause_2_element
                    new_else_clause_2.append(new_else_clause_2_element)

                new_else_clause_2 = new_else_clause_2
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (new_else_clause_0, new_else_clause_1, new_else_clause_2)
        elif else_clause is None:
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")


class PyBreakStmt(_BaseNode):
    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None) -> None:
        if break_keyword is None:
            self.break_keyword: PyBreakKeyword = PyBreakKeyword()
        elif isinstance(break_keyword, PyBreakKeyword):
            self.break_keyword: PyBreakKeyword = break_keyword
        else:
            raise ValueError("the field 'break_keyword' received an unrecognised value'")


class PyContinueStmt(_BaseNode):
    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None) -> None:
        if continue_keyword is None:
            self.continue_keyword: PyContinueKeyword = PyContinueKeyword()
        elif isinstance(continue_keyword, PyContinueKeyword):
            self.continue_keyword: PyContinueKeyword = continue_keyword
        else:
            raise ValueError("the field 'continue_keyword' received an unrecognised value'")


class PyTypeAliasStmt(_BaseNode):
    def __init__(self, name: 'str | PyIdent', expr: 'PyExpr', *, type_keyword: 'PyTypeKeyword | None' = None, type_params: 'list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | tuple[PyOpenBracket | None, list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | None, PyCloseBracket | None] | None' = None, equals: 'PyEquals | None' = None) -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.expr: PyExpr = expr
        if type_keyword is None:
            self.type_keyword: PyTypeKeyword = PyTypeKeyword()
        elif isinstance(type_keyword, PyTypeKeyword):
            self.type_keyword: PyTypeKeyword = type_keyword
        else:
            raise ValueError("the field 'type_keyword' received an unrecognised value'")
        if isinstance(type_params, list) or isinstance(type_params, list) or isinstance(type_params, Punctuated):
            new_type_params = Punctuated()
            type_params_iter = iter(type_params)
            try:
                first_type_params_element = next(type_params_iter)
                while True:
                    try:
                        second_type_params_element = next(type_params_iter)
                        if isinstance(first_type_params_element, tuple):
                            type_params_value = first_type_params_element[0]
                            type_params_separator = first_type_params_element[1]
                        else:
                            type_params_value = first_type_params_element
                            type_params_separator = None
                        new_type_params_value = type_params_value
                        if type_params_separator is None:
                            new_type_params_separator = PyComma()
                        elif isinstance(type_params_separator, PyComma):
                            new_type_params_separator = type_params_separator
                        else:
                            raise ValueError("the field 'type_params' received an unrecognised value'")
                        new_type_params.append(new_type_params_value, new_type_params_separator)
                        first_type_params_element = second_type_params_element
                    except StopIteration:
                        if isinstance(first_type_params_element, tuple):
                            type_params_value = first_type_params_element[0]
                            assert(first_type_params_element[1] is None)
                        else:
                            type_params_value = first_type_params_element
                        new_type_params_value = type_params_value
                        new_type_params.append(new_type_params_value)
                        break

            except StopIteration:
                pass
            self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = (PyOpenBracket(), new_type_params, PyCloseBracket())
        elif isinstance(type_params, tuple):
            assert(isinstance(type_params, tuple))
            type_params_0 = type_params[0]
            if type_params_0 is None:
                new_type_params_0 = PyOpenBracket()
            elif isinstance(type_params_0, PyOpenBracket):
                new_type_params_0 = type_params_0
            else:
                raise ValueError("the field 'type_params' received an unrecognised value'")
            type_params_1 = type_params[1]
            if type_params_1 is None:
                new_type_params_1 = Punctuated()
            elif isinstance(type_params_1, list) or isinstance(type_params_1, list) or isinstance(type_params_1, Punctuated):
                new_type_params_1 = Punctuated()
                type_params_1_iter = iter(type_params_1)
                try:
                    first_type_params_1_element = next(type_params_1_iter)
                    while True:
                        try:
                            second_type_params_1_element = next(type_params_1_iter)
                            if isinstance(first_type_params_1_element, tuple):
                                type_params_1_value = first_type_params_1_element[0]
                                type_params_1_separator = first_type_params_1_element[1]
                            else:
                                type_params_1_value = first_type_params_1_element
                                type_params_1_separator = None
                            new_type_params_1_value = type_params_1_value
                            if type_params_1_separator is None:
                                new_type_params_1_separator = PyComma()
                            elif isinstance(type_params_1_separator, PyComma):
                                new_type_params_1_separator = type_params_1_separator
                            else:
                                raise ValueError("the field 'type_params' received an unrecognised value'")
                            new_type_params_1.append(new_type_params_1_value, new_type_params_1_separator)
                            first_type_params_1_element = second_type_params_1_element
                        except StopIteration:
                            if isinstance(first_type_params_1_element, tuple):
                                type_params_1_value = first_type_params_1_element[0]
                                assert(first_type_params_1_element[1] is None)
                            else:
                                type_params_1_value = first_type_params_1_element
                            new_type_params_1_value = type_params_1_value
                            new_type_params_1.append(new_type_params_1_value)
                            break

                except StopIteration:
                    pass
                new_type_params_1 = new_type_params_1
            else:
                raise ValueError("the field 'type_params' received an unrecognised value'")
            type_params_2 = type_params[2]
            if type_params_2 is None:
                new_type_params_2 = PyCloseBracket()
            elif isinstance(type_params_2, PyCloseBracket):
                new_type_params_2 = type_params_2
            else:
                raise ValueError("the field 'type_params' received an unrecognised value'")
            self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = (new_type_params_0, new_type_params_1, new_type_params_2)
        elif type_params is None:
            self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = None
        else:
            raise ValueError("the field 'type_params' received an unrecognised value'")
        if equals is None:
            self.equals: PyEquals = PyEquals()
        elif isinstance(equals, PyEquals):
            self.equals: PyEquals = equals
        else:
            raise ValueError("the field 'equals' received an unrecognised value'")


class PyExceptHandler(_BaseNode):
    def __init__(self, expr: 'PyExpr', *, except_keyword: 'PyExceptKeyword | None' = None, binder: 'str | PyIdent | tuple[PyAsKeyword | None, str | PyIdent] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        self.expr: PyExpr = expr
        if except_keyword is None:
            self.except_keyword: PyExceptKeyword = PyExceptKeyword()
        elif isinstance(except_keyword, PyExceptKeyword):
            self.except_keyword: PyExceptKeyword = except_keyword
        else:
            raise ValueError("the field 'except_keyword' received an unrecognised value'")
        if isinstance(binder, str):
            self.binder: tuple[PyAsKeyword, PyIdent] | None = (PyAsKeyword(), PyIdent(binder))
        elif isinstance(binder, PyIdent):
            self.binder: tuple[PyAsKeyword, PyIdent] | None = (PyAsKeyword(), binder)
        elif isinstance(binder, tuple):
            assert(isinstance(binder, tuple))
            binder_0 = binder[0]
            if binder_0 is None:
                new_binder_0 = PyAsKeyword()
            elif isinstance(binder_0, PyAsKeyword):
                new_binder_0 = binder_0
            else:
                raise ValueError("the field 'binder' received an unrecognised value'")
            binder_1 = binder[1]
            if isinstance(binder_1, str):
                new_binder_1 = PyIdent(binder_1)
            elif isinstance(binder_1, PyIdent):
                new_binder_1 = binder_1
            else:
                raise ValueError("the field 'binder' received an unrecognised value'")
            self.binder: tuple[PyAsKeyword, PyIdent] | None = (new_binder_0, new_binder_1)
        elif binder is None:
            self.binder: tuple[PyAsKeyword, PyIdent] | None = None
        else:
            raise ValueError("the field 'binder' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")


class PyTryStmt(_BaseNode):
    def __init__(self, *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None, handlers: 'list[PyExceptHandler] | None' = None, else_clause: 'PyStmt | list[PyStmt] | tuple[PyElseKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None, finally_clause: 'PyStmt | list[PyStmt] | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None) -> None:
        if try_keyword is None:
            self.try_keyword: PyTryKeyword = PyTryKeyword()
        elif isinstance(try_keyword, PyTryKeyword):
            self.try_keyword: PyTryKeyword = try_keyword
        else:
            raise ValueError("the field 'try_keyword' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        if handlers is None:
            self.handlers: list[PyExceptHandler] = list()
        elif isinstance(handlers, list):
            new_handlers = list()
            for handlers_element in handlers:
                new_handlers_element = handlers_element
                new_handlers.append(new_handlers_element)

            self.handlers: list[PyExceptHandler] = new_handlers
        else:
            raise ValueError("the field 'handlers' received an unrecognised value'")
        if is_py_stmt(else_clause):
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyElseKeyword(), PyColon(), else_clause)
        elif isinstance(else_clause, list):
            new_else_clause = list()
            for else_clause_element in else_clause:
                new_else_clause_element = else_clause_element
                new_else_clause.append(new_else_clause_element)

            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyElseKeyword(), PyColon(), new_else_clause)
        elif isinstance(else_clause, tuple):
            assert(isinstance(else_clause, tuple))
            else_clause_0 = else_clause[0]
            if else_clause_0 is None:
                new_else_clause_0 = PyElseKeyword()
            elif isinstance(else_clause_0, PyElseKeyword):
                new_else_clause_0 = else_clause_0
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            else_clause_1 = else_clause[1]
            if else_clause_1 is None:
                new_else_clause_1 = PyColon()
            elif isinstance(else_clause_1, PyColon):
                new_else_clause_1 = else_clause_1
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            else_clause_2 = else_clause[2]
            if is_py_stmt(else_clause_2):
                new_else_clause_2 = else_clause_2
            elif else_clause_2 is None:
                new_else_clause_2 = list()
            elif isinstance(else_clause_2, list):
                new_else_clause_2 = list()
                for else_clause_2_element in else_clause_2:
                    new_else_clause_2_element = else_clause_2_element
                    new_else_clause_2.append(new_else_clause_2_element)

                new_else_clause_2 = new_else_clause_2
            else:
                raise ValueError("the field 'else_clause' received an unrecognised value'")
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = (new_else_clause_0, new_else_clause_1, new_else_clause_2)
        elif else_clause is None:
            self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")
        if is_py_stmt(finally_clause):
            self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyFinallyKeyword(), PyColon(), finally_clause)
        elif isinstance(finally_clause, list):
            new_finally_clause = list()
            for finally_clause_element in finally_clause:
                new_finally_clause_element = finally_clause_element
                new_finally_clause.append(new_finally_clause_element)

            self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None = (PyFinallyKeyword(), PyColon(), new_finally_clause)
        elif isinstance(finally_clause, tuple):
            assert(isinstance(finally_clause, tuple))
            finally_clause_0 = finally_clause[0]
            if finally_clause_0 is None:
                new_finally_clause_0 = PyFinallyKeyword()
            elif isinstance(finally_clause_0, PyFinallyKeyword):
                new_finally_clause_0 = finally_clause_0
            else:
                raise ValueError("the field 'finally_clause' received an unrecognised value'")
            finally_clause_1 = finally_clause[1]
            if finally_clause_1 is None:
                new_finally_clause_1 = PyColon()
            elif isinstance(finally_clause_1, PyColon):
                new_finally_clause_1 = finally_clause_1
            else:
                raise ValueError("the field 'finally_clause' received an unrecognised value'")
            finally_clause_2 = finally_clause[2]
            if is_py_stmt(finally_clause_2):
                new_finally_clause_2 = finally_clause_2
            elif finally_clause_2 is None:
                new_finally_clause_2 = list()
            elif isinstance(finally_clause_2, list):
                new_finally_clause_2 = list()
                for finally_clause_2_element in finally_clause_2:
                    new_finally_clause_2_element = finally_clause_2_element
                    new_finally_clause_2.append(new_finally_clause_2_element)

                new_finally_clause_2 = new_finally_clause_2
            else:
                raise ValueError("the field 'finally_clause' received an unrecognised value'")
            self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None = (new_finally_clause_0, new_finally_clause_1, new_finally_clause_2)
        elif finally_clause is None:
            self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None = None
        else:
            raise ValueError("the field 'finally_clause' received an unrecognised value'")


class PyClassDef(_BaseNode):
    def __init__(self, name: 'str | PyIdent', *, class_keyword: 'PyClassKeyword | None' = None, bases: 'list[str | PyIdent] | list[tuple[str | PyIdent, PyComma | None | None]] | Punctuated[str | PyIdent, PyComma | None] | tuple[PyOpenParen | None, list[str | PyIdent] | list[tuple[str | PyIdent, PyComma | None | None]] | Punctuated[str | PyIdent, PyComma | None] | None, PyCloseParen | None] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        if class_keyword is None:
            self.class_keyword: PyClassKeyword = PyClassKeyword()
        elif isinstance(class_keyword, PyClassKeyword):
            self.class_keyword: PyClassKeyword = class_keyword
        else:
            raise ValueError("the field 'class_keyword' received an unrecognised value'")
        if isinstance(bases, list) or isinstance(bases, list) or isinstance(bases, Punctuated):
            new_bases = Punctuated()
            bases_iter = iter(bases)
            try:
                first_bases_element = next(bases_iter)
                while True:
                    try:
                        second_bases_element = next(bases_iter)
                        if isinstance(first_bases_element, tuple):
                            bases_value = first_bases_element[0]
                            bases_separator = first_bases_element[1]
                        else:
                            bases_value = first_bases_element
                            bases_separator = None
                        if isinstance(bases_value, str):
                            new_bases_value = PyIdent(bases_value)
                        elif isinstance(bases_value, PyIdent):
                            new_bases_value = bases_value
                        else:
                            raise ValueError("the field 'bases' received an unrecognised value'")
                        if bases_separator is None:
                            new_bases_separator = PyComma()
                        elif isinstance(bases_separator, PyComma):
                            new_bases_separator = bases_separator
                        else:
                            raise ValueError("the field 'bases' received an unrecognised value'")
                        new_bases.append(new_bases_value, new_bases_separator)
                        first_bases_element = second_bases_element
                    except StopIteration:
                        if isinstance(first_bases_element, tuple):
                            bases_value = first_bases_element[0]
                            assert(first_bases_element[1] is None)
                        else:
                            bases_value = first_bases_element
                        if isinstance(bases_value, str):
                            new_bases_value = PyIdent(bases_value)
                        elif isinstance(bases_value, PyIdent):
                            new_bases_value = bases_value
                        else:
                            raise ValueError("the field 'bases' received an unrecognised value'")
                        new_bases.append(new_bases_value)
                        break

            except StopIteration:
                pass
            self.bases: tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None = (PyOpenParen(), new_bases, PyCloseParen())
        elif isinstance(bases, tuple):
            assert(isinstance(bases, tuple))
            bases_0 = bases[0]
            if bases_0 is None:
                new_bases_0 = PyOpenParen()
            elif isinstance(bases_0, PyOpenParen):
                new_bases_0 = bases_0
            else:
                raise ValueError("the field 'bases' received an unrecognised value'")
            bases_1 = bases[1]
            if bases_1 is None:
                new_bases_1 = Punctuated()
            elif isinstance(bases_1, list) or isinstance(bases_1, list) or isinstance(bases_1, Punctuated):
                new_bases_1 = Punctuated()
                bases_1_iter = iter(bases_1)
                try:
                    first_bases_1_element = next(bases_1_iter)
                    while True:
                        try:
                            second_bases_1_element = next(bases_1_iter)
                            if isinstance(first_bases_1_element, tuple):
                                bases_1_value = first_bases_1_element[0]
                                bases_1_separator = first_bases_1_element[1]
                            else:
                                bases_1_value = first_bases_1_element
                                bases_1_separator = None
                            if isinstance(bases_1_value, str):
                                new_bases_1_value = PyIdent(bases_1_value)
                            elif isinstance(bases_1_value, PyIdent):
                                new_bases_1_value = bases_1_value
                            else:
                                raise ValueError("the field 'bases' received an unrecognised value'")
                            if bases_1_separator is None:
                                new_bases_1_separator = PyComma()
                            elif isinstance(bases_1_separator, PyComma):
                                new_bases_1_separator = bases_1_separator
                            else:
                                raise ValueError("the field 'bases' received an unrecognised value'")
                            new_bases_1.append(new_bases_1_value, new_bases_1_separator)
                            first_bases_1_element = second_bases_1_element
                        except StopIteration:
                            if isinstance(first_bases_1_element, tuple):
                                bases_1_value = first_bases_1_element[0]
                                assert(first_bases_1_element[1] is None)
                            else:
                                bases_1_value = first_bases_1_element
                            if isinstance(bases_1_value, str):
                                new_bases_1_value = PyIdent(bases_1_value)
                            elif isinstance(bases_1_value, PyIdent):
                                new_bases_1_value = bases_1_value
                            else:
                                raise ValueError("the field 'bases' received an unrecognised value'")
                            new_bases_1.append(new_bases_1_value)
                            break

                except StopIteration:
                    pass
                new_bases_1 = new_bases_1
            else:
                raise ValueError("the field 'bases' received an unrecognised value'")
            bases_2 = bases[2]
            if bases_2 is None:
                new_bases_2 = PyCloseParen()
            elif isinstance(bases_2, PyCloseParen):
                new_bases_2 = bases_2
            else:
                raise ValueError("the field 'bases' received an unrecognised value'")
            self.bases: tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None = (new_bases_0, new_bases_1, new_bases_2)
        elif bases is None:
            self.bases: tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None = None
        else:
            raise ValueError("the field 'bases' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")


PyParam: TypeAlias = 'PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam'


def is_py_param(value: Any) -> TypeGuard[PyParam]:
    return isinstance(value, PyNamedParam) or isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PySepParam)


class PyNamedParam(_BaseNode):
    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = pattern
        if is_py_expr(annotation):
            self.annotation: tuple[PyColon, PyExpr] | None = (PyColon(), annotation)
        elif isinstance(annotation, tuple):
            assert(isinstance(annotation, tuple))
            annotation_0 = annotation[0]
            if annotation_0 is None:
                new_annotation_0 = PyColon()
            elif isinstance(annotation_0, PyColon):
                new_annotation_0 = annotation_0
            else:
                raise ValueError("the field 'annotation' received an unrecognised value'")
            annotation_1 = annotation[1]
            new_annotation_1 = annotation_1
            self.annotation: tuple[PyColon, PyExpr] | None = (new_annotation_0, new_annotation_1)
        elif annotation is None:
            self.annotation: tuple[PyColon, PyExpr] | None = None
        else:
            raise ValueError("the field 'annotation' received an unrecognised value'")
        if is_py_expr(default):
            self.default: tuple[PyEquals, PyExpr] | None = (PyEquals(), default)
        elif isinstance(default, tuple):
            assert(isinstance(default, tuple))
            default_0 = default[0]
            if default_0 is None:
                new_default_0 = PyEquals()
            elif isinstance(default_0, PyEquals):
                new_default_0 = default_0
            else:
                raise ValueError("the field 'default' received an unrecognised value'")
            default_1 = default[1]
            new_default_1 = default_1
            self.default: tuple[PyEquals, PyExpr] | None = (new_default_0, new_default_1)
        elif default is None:
            self.default: tuple[PyEquals, PyExpr] | None = None
        else:
            raise ValueError("the field 'default' received an unrecognised value'")


class PyRestPosParam(_BaseNode):
    def __init__(self, name: 'str | PyIdent', *, asterisk: 'PyAsterisk | None' = None) -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            self.asterisk: PyAsterisk = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")


class PyRestKeywordParam(_BaseNode):
    def __init__(self, name: 'str | PyIdent', *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None) -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        if asterisk_asterisk is None:
            self.asterisk_asterisk: PyAsteriskAsterisk = PyAsteriskAsterisk()
        elif isinstance(asterisk_asterisk, PyAsteriskAsterisk):
            self.asterisk_asterisk: PyAsteriskAsterisk = asterisk_asterisk
        else:
            raise ValueError("the field 'asterisk_asterisk' received an unrecognised value'")


class PySepParam(_BaseNode):
    def __init__(self, *, asterisk: 'PyAsterisk | None' = None) -> None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            self.asterisk: PyAsterisk = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")


class PyFuncDef(_BaseNode):
    def __init__(self, name: 'str | PyIdent', *, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, open_paren: 'PyOpenParen | None' = None, params: 'list[PyParam] | list[tuple[PyParam, PyComma | None | None]] | Punctuated[PyParam, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[PyHyphenGreaterThan | None, PyExpr] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        elif isinstance(name, PyIdent):
            self.name: PyIdent = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        if isinstance(async_keyword, PyAsyncKeyword):
            self.async_keyword: PyAsyncKeyword | None = async_keyword
        elif async_keyword is None:
            self.async_keyword: PyAsyncKeyword | None = None
        else:
            raise ValueError("the field 'async_keyword' received an unrecognised value'")
        if def_keyword is None:
            self.def_keyword: PyDefKeyword = PyDefKeyword()
        elif isinstance(def_keyword, PyDefKeyword):
            self.def_keyword: PyDefKeyword = def_keyword
        else:
            raise ValueError("the field 'def_keyword' received an unrecognised value'")
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            self.open_paren: PyOpenParen = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        if params is None:
            self.params: Punctuated[PyParam, PyComma] = Punctuated()
        elif isinstance(params, list) or isinstance(params, list) or isinstance(params, Punctuated):
            new_params = Punctuated()
            params_iter = iter(params)
            try:
                first_params_element = next(params_iter)
                while True:
                    try:
                        second_params_element = next(params_iter)
                        if isinstance(first_params_element, tuple):
                            params_value = first_params_element[0]
                            params_separator = first_params_element[1]
                        else:
                            params_value = first_params_element
                            params_separator = None
                        new_params_value = params_value
                        if params_separator is None:
                            new_params_separator = PyComma()
                        elif isinstance(params_separator, PyComma):
                            new_params_separator = params_separator
                        else:
                            raise ValueError("the field 'params' received an unrecognised value'")
                        new_params.append(new_params_value, new_params_separator)
                        first_params_element = second_params_element
                    except StopIteration:
                        if isinstance(first_params_element, tuple):
                            params_value = first_params_element[0]
                            assert(first_params_element[1] is None)
                        else:
                            params_value = first_params_element
                        new_params_value = params_value
                        new_params.append(new_params_value)
                        break

            except StopIteration:
                pass
            self.params: Punctuated[PyParam, PyComma] = new_params
        else:
            raise ValueError("the field 'params' received an unrecognised value'")
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            self.close_paren: PyCloseParen = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")
        if is_py_expr(return_type):
            self.return_type: tuple[PyHyphenGreaterThan, PyExpr] | None = (PyHyphenGreaterThan(), return_type)
        elif isinstance(return_type, tuple):
            assert(isinstance(return_type, tuple))
            return_type_0 = return_type[0]
            if return_type_0 is None:
                new_return_type_0 = PyHyphenGreaterThan()
            elif isinstance(return_type_0, PyHyphenGreaterThan):
                new_return_type_0 = return_type_0
            else:
                raise ValueError("the field 'return_type' received an unrecognised value'")
            return_type_1 = return_type[1]
            new_return_type_1 = return_type_1
            self.return_type: tuple[PyHyphenGreaterThan, PyExpr] | None = (new_return_type_0, new_return_type_1)
        elif return_type is None:
            self.return_type: tuple[PyHyphenGreaterThan, PyExpr] | None = None
        else:
            raise ValueError("the field 'return_type' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        elif isinstance(colon, PyColon):
            self.colon: PyColon = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None:
            self.body: PyStmt | list[PyStmt] = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)

            self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")


class PyModule(_BaseNode):
    def __init__(self, *, stmts: 'list[PyStmt] | None' = None) -> None:
        if stmts is None:
            self.stmts: list[PyStmt] = list()
        elif isinstance(stmts, list):
            new_stmts = list()
            for stmts_element in stmts:
                new_stmts_element = stmts_element
                new_stmts.append(new_stmts_element)

            self.stmts: list[PyStmt] = new_stmts
        else:
            raise ValueError("the field 'stmts' received an unrecognised value'")


class PyTilde(_BaseToken):
    pass


class PyVerticalBar(_BaseToken):
    pass


class PyWhileKeyword(_BaseToken):
    pass


class PyTypeKeyword(_BaseToken):
    pass


class PyTryKeyword(_BaseToken):
    pass


class PyReturnKeyword(_BaseToken):
    pass


class PyRaiseKeyword(_BaseToken):
    pass


class PyPassKeyword(_BaseToken):
    pass


class PyOrKeyword(_BaseToken):
    pass


class PyNotKeyword(_BaseToken):
    pass


class PyIsKeyword(_BaseToken):
    pass


class PyInKeyword(_BaseToken):
    pass


class PyIfKeyword(_BaseToken):
    pass


class PyFromKeyword(_BaseToken):
    pass


class PyForKeyword(_BaseToken):
    pass


class PyFinallyKeyword(_BaseToken):
    pass


class PyExceptKeyword(_BaseToken):
    pass


class PyElseKeyword(_BaseToken):
    pass


class PyElifKeyword(_BaseToken):
    pass


class PyDelKeyword(_BaseToken):
    pass


class PyDefKeyword(_BaseToken):
    pass


class PyContinueKeyword(_BaseToken):
    pass


class PyClassKeyword(_BaseToken):
    pass


class PyBreakKeyword(_BaseToken):
    pass


class PyAsyncKeyword(_BaseToken):
    pass


class PyAsKeyword(_BaseToken):
    pass


class PyAndKeyword(_BaseToken):
    pass


class PyCaret(_BaseToken):
    pass


class PyCloseBracket(_BaseToken):
    pass


class PyOpenBracket(_BaseToken):
    pass


class PyAtSign(_BaseToken):
    pass


class PyGreaterThanGreaterThan(_BaseToken):
    pass


class PyGreaterThanEquals(_BaseToken):
    pass


class PyGreaterThan(_BaseToken):
    pass


class PyEqualsEquals(_BaseToken):
    pass


class PyEquals(_BaseToken):
    pass


class PyLessThanEquals(_BaseToken):
    pass


class PyLessThanLessThan(_BaseToken):
    pass


class PyLessThan(_BaseToken):
    pass


class PySemicolon(_BaseToken):
    pass


class PyColon(_BaseToken):
    pass


class PySlashSlash(_BaseToken):
    pass


class PySlash(_BaseToken):
    pass


class PyDot(_BaseToken):
    pass


class PyHyphenGreaterThan(_BaseToken):
    pass


class PyHyphen(_BaseToken):
    pass


class PyComma(_BaseToken):
    pass


class PyPlus(_BaseToken):
    pass


class PyAsteriskAsterisk(_BaseToken):
    pass


class PyAsterisk(_BaseToken):
    pass


class PyCloseParen(_BaseToken):
    pass


class PyOpenParen(_BaseToken):
    pass


class PyAmpersand(_BaseToken):
    pass


class PyPercenct(_BaseToken):
    pass


class PyHashtag(_BaseToken):
    pass


class PyExclamationMarkEquals(_BaseToken):
    pass


class PyCarriageReturnLineFeed(_BaseToken):
    pass


class PyLineFeed(_BaseToken):
    pass


PyToken = PyIdent | PyInteger | PyFloat | PyString | PyTilde | PyVerticalBar | PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyIsKeyword | PyInKeyword | PyIfKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword | PyCaret | PyCloseBracket | PyOpenBracket | PyAtSign | PyGreaterThanGreaterThan | PyGreaterThanEquals | PyGreaterThan | PyEqualsEquals | PyEquals | PyLessThanEquals | PyLessThanLessThan | PyLessThan | PySemicolon | PyColon | PySlashSlash | PySlash | PyDot | PyHyphenGreaterThan | PyHyphen | PyComma | PyPlus | PyAsteriskAsterisk | PyAsterisk | PyCloseParen | PyOpenParen | PyAmpersand | PyPercenct | PyHashtag | PyExclamationMarkEquals | PyCarriageReturnLineFeed | PyLineFeed


PyNode = PySlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyGuard | PyComprehension | PyGeneratorExpr | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleExpr | PyKeywordArg | PyCallExpr | PyPrefixExpr | PyInfixExpr | PyRetStmt | PyExprStmt | PyAssignStmt | PyPassStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam | PyFuncDef | PyModule


PySyntax = PyToken | PyNode




def for_each_py_child(node: PySyntax, proc: Callable[[PySyntax], None]):
    if is_py_token(node): return
    if isinstance(node, PySlice):
        proc(node.lower)
        proc(node.colon)
        proc(node.upper)
        return
    if isinstance(node, PyNamedPattern):
        proc(node.name)
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        proc(node.dot)
        proc(node.name)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        proc(node.open_bracket)
        for (element_0, separator_0) in node.slices:
            if is_py_pattern(element_0):
                proc(element_0)
            elif isinstance(element_0, PySlice):
                proc(element_0)
            else:
                raise ValueError()

        proc(node.close_bracket)
        return
    if isinstance(node, PyStarredPattern):
        proc(node.asterisk)
        proc(node.expr)
        return
    if isinstance(node, PyListPattern):
        proc(node.open_bracket)
        for (element_0, separator_0) in node.elements:
            proc(element_0)

        proc(node.close_bracket)
        return
    if isinstance(node, PyTuplePattern):
        proc(node.open_paren)
        for (element_0, separator_0) in node.elements:
            proc(element_0)

        proc(node.close_paren)
        return
    if isinstance(node, PyGuard):
        proc(node.if_keyword)
        proc(node.expr)
        return
    if isinstance(node, PyComprehension):
        if isinstance(node.async_keyword, PyAsyncKeyword):
            proc(node.async_keyword)
        elif node.async_keyword is None:
            pass
        else:
            raise ValueError()
        proc(node.for_keyword)
        proc(node.pattern)
        proc(node.in_keyword)
        proc(node.target)
        for element_0 in node.guards:
            proc(element_0)

        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element_0 in node.generators:
            proc(element_0)

        return
    if isinstance(node, PyConstExpr):
        if isinstance(node.literal, PyString):
            proc(node.literal)
        elif isinstance(node.literal, PyFloat):
            proc(node.literal)
        elif isinstance(node.literal, PyInteger):
            proc(node.literal)
        else:
            raise ValueError()
        return
    if isinstance(node, PyNestExpr):
        proc(node.open_paren)
        proc(node.expr)
        proc(node.close_paren)
        return
    if isinstance(node, PyNamedExpr):
        proc(node.name)
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        proc(node.dot)
        proc(node.name)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        proc(node.open_bracket)
        for (element_0, separator_0) in node.slices:
            if is_py_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, PySlice):
                proc(element_0)
            else:
                raise ValueError()

        proc(node.close_bracket)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.asterisk)
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        proc(node.open_bracket)
        for (element_0, separator_0) in node.elements:
            proc(element_0)

        proc(node.close_bracket)
        return
    if isinstance(node, PyTupleExpr):
        proc(node.open_paren)
        for (element_0, separator_0) in node.elements:
            proc(element_0)

        proc(node.close_paren)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.name)
        proc(node.equals)
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        proc(node.open_paren)
        for (element_0, separator_0) in node.args:
            proc(element_0)

        proc(node.close_paren)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.prefix_op)
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.op)
        proc(node.right)
        return
    if isinstance(node, PyRetStmt):
        proc(node.return_keyword)
        if is_py_expr(node.expr):
            proc(node.expr)
        elif node.expr is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            element_0 = node.annotation[0]
            proc(element_0)
            element_1 = node.annotation[1]
            proc(element_1)
        elif node.annotation is None:
            pass
        else:
            raise ValueError()
        proc(node.equals)
        proc(node.expr)
        return
    if isinstance(node, PyPassStmt):
        proc(node.pass_keyword)
        return
    if isinstance(node, PyIfCase):
        proc(node.if_keyword)
        proc(node.test)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)

        else:
            raise ValueError()
        return
    if isinstance(node, PyElifCase):
        proc(node.elif_keyword)
        proc(node.test)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)

        else:
            raise ValueError()
        return
    if isinstance(node, PyElseCase):
        proc(node.else_keyword)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)

        else:
            raise ValueError()
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element_0 in node.alternatives:
            proc(element_0)

        if isinstance(node.last, PyElseCase):
            proc(node.last)
        elif node.last is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyDeleteStmt):
        proc(node.del_keyword)
        proc(node.pattern)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.raise_keyword)
        proc(node.expr)
        if isinstance(node.cause, tuple):
            element_0 = node.cause[0]
            proc(element_0)
            element_1 = node.cause[1]
            proc(element_1)
        elif node.cause is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyForStmt):
        proc(node.for_keyword)
        proc(node.pattern)
        proc(node.in_keyword)
        proc(node.expr)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)

        else:
            raise ValueError()
        if isinstance(node.else_clause, tuple):
            element_1 = node.else_clause[0]
            proc(element_1)
            element_2 = node.else_clause[1]
            proc(element_2)
            element_3 = node.else_clause[2]
            if is_py_stmt(element_3):
                proc(element_3)
            elif isinstance(element_3, list):
                for element_4 in element_3:
                    proc(element_4)

            else:
                raise ValueError()
        elif node.else_clause is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyWhileStmt):
        proc(node.while_keyword)
        proc(node.expr)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)

        else:
            raise ValueError()
        if isinstance(node.else_clause, tuple):
            element_1 = node.else_clause[0]
            proc(element_1)
            element_2 = node.else_clause[1]
            proc(element_2)
            element_3 = node.else_clause[2]
            if is_py_stmt(element_3):
                proc(element_3)
            elif isinstance(element_3, list):
                for element_4 in element_3:
                    proc(element_4)

            else:
                raise ValueError()
        elif node.else_clause is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyBreakStmt):
        proc(node.break_keyword)
        return
    if isinstance(node, PyContinueStmt):
        proc(node.continue_keyword)
        return
    if isinstance(node, PyTypeAliasStmt):
        proc(node.type_keyword)
        proc(node.name)
        if isinstance(node.type_params, tuple):
            element_0 = node.type_params[0]
            proc(element_0)
            element_1 = node.type_params[1]
            for (element_2, separator_0) in element_1:
                proc(element_2)

            element_3 = node.type_params[2]
            proc(element_3)
        elif node.type_params is None:
            pass
        else:
            raise ValueError()
        proc(node.equals)
        proc(node.expr)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.except_keyword)
        proc(node.expr)
        if isinstance(node.binder, tuple):
            element_0 = node.binder[0]
            proc(element_0)
            element_1 = node.binder[1]
            proc(element_1)
        elif node.binder is None:
            pass
        else:
            raise ValueError()
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)

        else:
            raise ValueError()
        return
    if isinstance(node, PyTryStmt):
        proc(node.try_keyword)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)

        else:
            raise ValueError()
        for element_1 in node.handlers:
            proc(element_1)

        if isinstance(node.else_clause, tuple):
            element_2 = node.else_clause[0]
            proc(element_2)
            element_3 = node.else_clause[1]
            proc(element_3)
            element_4 = node.else_clause[2]
            if is_py_stmt(element_4):
                proc(element_4)
            elif isinstance(element_4, list):
                for element_5 in element_4:
                    proc(element_5)

            else:
                raise ValueError()
        elif node.else_clause is None:
            pass
        else:
            raise ValueError()
        if isinstance(node.finally_clause, tuple):
            element_6 = node.finally_clause[0]
            proc(element_6)
            element_7 = node.finally_clause[1]
            proc(element_7)
            element_8 = node.finally_clause[2]
            if is_py_stmt(element_8):
                proc(element_8)
            elif isinstance(element_8, list):
                for element_9 in element_8:
                    proc(element_9)

            else:
                raise ValueError()
        elif node.finally_clause is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyClassDef):
        proc(node.class_keyword)
        proc(node.name)
        if isinstance(node.bases, tuple):
            element_0 = node.bases[0]
            proc(element_0)
            element_1 = node.bases[1]
            for (element_2, separator_0) in element_1:
                proc(element_2)

            element_3 = node.bases[2]
            proc(element_3)
        elif node.bases is None:
            pass
        else:
            raise ValueError()
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_4 in node.body:
                proc(element_4)

        else:
            raise ValueError()
        return
    if isinstance(node, PyNamedParam):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            element_0 = node.annotation[0]
            proc(element_0)
            element_1 = node.annotation[1]
            proc(element_1)
        elif node.annotation is None:
            pass
        else:
            raise ValueError()
        if isinstance(node.default, tuple):
            element_2 = node.default[0]
            proc(element_2)
            element_3 = node.default[1]
            proc(element_3)
        elif node.default is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyRestPosParam):
        proc(node.asterisk)
        proc(node.name)
        return
    if isinstance(node, PyRestKeywordParam):
        proc(node.asterisk_asterisk)
        proc(node.name)
        return
    if isinstance(node, PySepParam):
        proc(node.asterisk)
        return
    if isinstance(node, PyFuncDef):
        if isinstance(node.async_keyword, PyAsyncKeyword):
            proc(node.async_keyword)
        elif node.async_keyword is None:
            pass
        else:
            raise ValueError()
        proc(node.def_keyword)
        proc(node.name)
        proc(node.open_paren)
        for (element_0, separator_0) in node.params:
            proc(element_0)

        proc(node.close_paren)
        if isinstance(node.return_type, tuple):
            element_1 = node.return_type[0]
            proc(element_1)
            element_2 = node.return_type[1]
            proc(element_2)
        elif node.return_type is None:
            pass
        else:
            raise ValueError()
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_3 in node.body:
                proc(element_3)

        else:
            raise ValueError()
        return
    if isinstance(node, PyModule):
        for element_0 in node.stmts:
            proc(element_0)

        return

