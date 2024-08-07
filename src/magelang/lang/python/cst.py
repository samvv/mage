
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

    def __init__(self, parent: Any = None) -> None:
        super().__init__()
        self._parent = parent

    def has_parent(self) -> bool:
        return self._parent is not None

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


class PyFloat(_BaseToken):

    def __init__(self, value: float, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyInteger(_BaseToken):

    def __init__(self, value: int, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyString(_BaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


type PySliceParent = PySubscriptExpr | PySubscriptPattern


class PySlice(_BaseNode):

    def __init__(self, *, lower: 'PyExpr | None' = None, colon: 'PyColon | None' = None, upper: 'PyExpr | None' = None, step: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        if is_py_expr(lower):
            lower_out = lower
        elif lower is None:
            lower_out = None
        else:
            raise ValueError("the field 'lower' received an unrecognised value'")
        self.lower: PyExpr | None = lower_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_expr(upper):
            upper_out = upper
        elif upper is None:
            upper_out = None
        else:
            raise ValueError("the field 'upper' received an unrecognised value'")
        self.upper: PyExpr | None = upper_out
        if is_py_expr(step):
            step_out = (PyColon(), step)
        elif isinstance(step, tuple):
            assert(isinstance(step, tuple))
            step_0 = step[0]
            if step_0 is None:
                new_step_0 = PyColon()
            elif isinstance(step_0, PyColon):
                new_step_0 = step_0
            else:
                raise ValueError("the field 'step' received an unrecognised value'")
            step_1 = step[1]
            new_step_1 = step_1
            step_out = (new_step_0, new_step_1)
        elif step is None:
            step_out = None
        else:
            raise ValueError("the field 'step' received an unrecognised value'")
        self.step: tuple[PyColon, PyExpr] | None = step_out

    def parent(self) -> PySliceParent:
        assert(self._parent is not None)
        return self._parent


type PyPattern = PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern


def is_py_pattern(value: Any) -> TypeGuard[PyPattern]:
    return isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern)


type PyNamedPatternParent = PyNamedParam | PyForStmt | PyTuplePattern | PyComprehension | PyDeleteStmt | PyListPattern | PySubscriptPattern | PyAttrPattern | PyAssignStmt


class PyNamedPattern(_BaseNode):

    def __init__(self, name: 'str | PyIdent') -> None:
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyNamedPatternParent:
        assert(self._parent is not None)
        return self._parent


type PyAttrPatternParent = PyNamedParam | PyForStmt | PyTuplePattern | PyComprehension | PyDeleteStmt | PyListPattern | PySubscriptPattern | PyAttrPattern | PyAssignStmt


class PyAttrPattern(_BaseNode):

    def __init__(self, pattern: 'PyPattern', name: 'str | PyIdent', *, dot: 'PyDot | None' = None) -> None:
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out
        if dot is None:
            dot_out = PyDot()
        elif isinstance(dot, PyDot):
            dot_out = dot
        else:
            raise ValueError("the field 'dot' received an unrecognised value'")
        self.dot: PyDot = dot_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyAttrPatternParent:
        assert(self._parent is not None)
        return self._parent


type PySubscriptPatternParent = PyNamedParam | PyForStmt | PyTuplePattern | PyComprehension | PyDeleteStmt | PyListPattern | PySubscriptPattern | PyAttrPattern | PyAssignStmt


class PySubscriptPattern(_BaseNode):

    def __init__(self, pattern: 'PyPattern', *, open_bracket: 'PyOpenBracket | None' = None, slices: 'list[PyPattern | PySlice | None] | list[tuple[PyPattern | PySlice | None, PyComma | None | None]] | Punctuated[PyPattern | PySlice | None, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out
        if open_bracket is None:
            open_bracket_out = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            open_bracket_out = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        self.open_bracket: PyOpenBracket = open_bracket_out
        if slices is None:
            slices_out = Punctuated()
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
                        elif slices_value is None:
                            new_slices_value = PySlice()
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
                        elif slices_value is None:
                            new_slices_value = PySlice()
                        elif isinstance(slices_value, PySlice):
                            new_slices_value = slices_value
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        new_slices.append(new_slices_value)
                        break
            except StopIteration:
                pass
            slices_out = new_slices
        else:
            raise ValueError("the field 'slices' received an unrecognised value'")
        self.slices: Punctuated[PyPattern | PySlice, PyComma] = slices_out
        if close_bracket is None:
            close_bracket_out = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            close_bracket_out = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")
        self.close_bracket: PyCloseBracket = close_bracket_out

    def parent(self) -> PySubscriptPatternParent:
        assert(self._parent is not None)
        return self._parent


type PyStarredPatternParent = PyNamedParam | PyForStmt | PyTuplePattern | PyComprehension | PyDeleteStmt | PyListPattern | PySubscriptPattern | PyAttrPattern | PyAssignStmt


class PyStarredPattern(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        if asterisk is None:
            asterisk_out = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            asterisk_out = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")
        self.asterisk: PyAsterisk = asterisk_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyStarredPatternParent:
        assert(self._parent is not None)
        return self._parent


type PyListPatternParent = PyNamedParam | PyForStmt | PyTuplePattern | PyComprehension | PyDeleteStmt | PyListPattern | PySubscriptPattern | PyAttrPattern | PyAssignStmt


class PyListPattern(_BaseNode):

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'list[PyPattern] | list[tuple[PyPattern, PyComma | None | None]] | Punctuated[PyPattern, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        if open_bracket is None:
            open_bracket_out = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            open_bracket_out = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        self.open_bracket: PyOpenBracket = open_bracket_out
        if elements is None:
            elements_out = Punctuated()
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
            elements_out = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        self.elements: Punctuated[PyPattern, PyComma] = elements_out
        if close_bracket is None:
            close_bracket_out = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            close_bracket_out = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")
        self.close_bracket: PyCloseBracket = close_bracket_out

    def parent(self) -> PyListPatternParent:
        assert(self._parent is not None)
        return self._parent


type PyTuplePatternParent = PyNamedParam | PyForStmt | PyTuplePattern | PyComprehension | PyDeleteStmt | PyListPattern | PySubscriptPattern | PyAttrPattern | PyAssignStmt


class PyTuplePattern(_BaseNode):

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'list[PyPattern] | list[tuple[PyPattern, PyComma | None | None]] | Punctuated[PyPattern, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            open_paren_out = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            open_paren_out = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        self.open_paren: PyOpenParen = open_paren_out
        if elements is None:
            elements_out = Punctuated()
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
            elements_out = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        self.elements: Punctuated[PyPattern, PyComma] = elements_out
        if close_paren is None:
            close_paren_out = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            close_paren_out = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")
        self.close_paren: PyCloseParen = close_paren_out

    def parent(self) -> PyTuplePatternParent:
        assert(self._parent is not None)
        return self._parent


type PyExpr = PyAttrExpr | PyCallExpr | PyConstExpr | PyGeneratorExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr


def is_py_expr(value: Any) -> TypeGuard[PyExpr]:
    return isinstance(value, PyAttrExpr) or isinstance(value, PyCallExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyListExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyTupleExpr)


type PyGuardParent = PyComprehension


class PyGuard(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None) -> None:
        if if_keyword is None:
            if_keyword_out = PyIfKeyword()
        elif isinstance(if_keyword, PyIfKeyword):
            if_keyword_out = if_keyword
        else:
            raise ValueError("the field 'if_keyword' received an unrecognised value'")
        self.if_keyword: PyIfKeyword = if_keyword_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyGuardParent:
        assert(self._parent is not None)
        return self._parent


type PyComprehensionParent = PyGeneratorExpr


class PyComprehension(_BaseNode):

    def __init__(self, pattern: 'PyPattern', target: 'PyExpr', *, async_keyword: 'PyAsyncKeyword | None' = None, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, guards: 'list[PyGuard] | None' = None) -> None:
        if isinstance(async_keyword, PyAsyncKeyword):
            async_keyword_out = async_keyword
        elif async_keyword is None:
            async_keyword_out = None
        else:
            raise ValueError("the field 'async_keyword' received an unrecognised value'")
        self.async_keyword: PyAsyncKeyword | None = async_keyword_out
        if for_keyword is None:
            for_keyword_out = PyForKeyword()
        elif isinstance(for_keyword, PyForKeyword):
            for_keyword_out = for_keyword
        else:
            raise ValueError("the field 'for_keyword' received an unrecognised value'")
        self.for_keyword: PyForKeyword = for_keyword_out
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out
        if in_keyword is None:
            in_keyword_out = PyInKeyword()
        elif isinstance(in_keyword, PyInKeyword):
            in_keyword_out = in_keyword
        else:
            raise ValueError("the field 'in_keyword' received an unrecognised value'")
        self.in_keyword: PyInKeyword = in_keyword_out
        target_out = target
        self.target: PyExpr = target_out
        if guards is None:
            guards_out = list()
        elif isinstance(guards, list):
            new_guards = list()
            for guards_element in guards:
                new_guards_element = guards_element
                new_guards.append(new_guards_element)
            guards_out = new_guards
        else:
            raise ValueError("the field 'guards' received an unrecognised value'")
        self.guards: list[PyGuard] = guards_out

    def parent(self) -> PyComprehensionParent:
        assert(self._parent is not None)
        return self._parent


type PyGeneratorExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyGeneratorExpr(_BaseNode):

    def __init__(self, element: 'PyExpr', *, generators: 'list[PyComprehension] | None' = None) -> None:
        element_out = element
        self.element: PyExpr = element_out
        if generators is None:
            generators_out = list()
        elif isinstance(generators, list):
            new_generators = list()
            for generators_element in generators:
                new_generators_element = generators_element
                new_generators.append(new_generators_element)
            generators_out = new_generators
        else:
            raise ValueError("the field 'generators' received an unrecognised value'")
        self.generators: list[PyComprehension] = generators_out

    def parent(self) -> PyGeneratorExprParent:
        assert(self._parent is not None)
        return self._parent


type PyConstExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyConstExpr(_BaseNode):

    def __init__(self, literal: 'str | PyString | float | PyFloat | int | PyInteger') -> None:
        if isinstance(literal, str):
            literal_out = PyString(literal)
        elif isinstance(literal, PyString):
            literal_out = literal
        elif isinstance(literal, float):
            literal_out = PyFloat(literal)
        elif isinstance(literal, PyFloat):
            literal_out = literal
        elif isinstance(literal, int):
            literal_out = PyInteger(literal)
        elif isinstance(literal, PyInteger):
            literal_out = literal
        else:
            raise ValueError("the field 'literal' received an unrecognised value'")
        self.literal: PyString | PyFloat | PyInteger = literal_out

    def parent(self) -> PyConstExprParent:
        assert(self._parent is not None)
        return self._parent


type PyNestExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyNestExpr(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            open_paren_out = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            open_paren_out = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        self.open_paren: PyOpenParen = open_paren_out
        expr_out = expr
        self.expr: PyExpr = expr_out
        if close_paren is None:
            close_paren_out = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            close_paren_out = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")
        self.close_paren: PyCloseParen = close_paren_out

    def parent(self) -> PyNestExprParent:
        assert(self._parent is not None)
        return self._parent


type PyNamedExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyNamedExpr(_BaseNode):

    def __init__(self, name: 'str | PyIdent') -> None:
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyNamedExprParent:
        assert(self._parent is not None)
        return self._parent


type PyAttrExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyAttrExpr(_BaseNode):

    def __init__(self, expr: 'PyExpr', name: 'str | PyIdent', *, dot: 'PyDot | None' = None) -> None:
        expr_out = expr
        self.expr: PyExpr = expr_out
        if dot is None:
            dot_out = PyDot()
        elif isinstance(dot, PyDot):
            dot_out = dot
        else:
            raise ValueError("the field 'dot' received an unrecognised value'")
        self.dot: PyDot = dot_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyAttrExprParent:
        assert(self._parent is not None)
        return self._parent


type PySubscriptExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PySubscriptExpr(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, open_bracket: 'PyOpenBracket | None' = None, slices: 'list[PyExpr | PySlice | None] | list[tuple[PyExpr | PySlice | None, PyComma | None | None]] | Punctuated[PyExpr | PySlice | None, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        expr_out = expr
        self.expr: PyExpr = expr_out
        if open_bracket is None:
            open_bracket_out = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            open_bracket_out = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        self.open_bracket: PyOpenBracket = open_bracket_out
        if slices is None:
            slices_out = Punctuated()
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
                        elif slices_value is None:
                            new_slices_value = PySlice()
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
                        elif slices_value is None:
                            new_slices_value = PySlice()
                        elif isinstance(slices_value, PySlice):
                            new_slices_value = slices_value
                        else:
                            raise ValueError("the field 'slices' received an unrecognised value'")
                        new_slices.append(new_slices_value)
                        break
            except StopIteration:
                pass
            slices_out = new_slices
        else:
            raise ValueError("the field 'slices' received an unrecognised value'")
        self.slices: Punctuated[PyExpr | PySlice, PyComma] = slices_out
        if close_bracket is None:
            close_bracket_out = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            close_bracket_out = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")
        self.close_bracket: PyCloseBracket = close_bracket_out

    def parent(self) -> PySubscriptExprParent:
        assert(self._parent is not None)
        return self._parent


type PyStarredExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyStarredExpr(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        if asterisk is None:
            asterisk_out = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            asterisk_out = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")
        self.asterisk: PyAsterisk = asterisk_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyStarredExprParent:
        assert(self._parent is not None)
        return self._parent


type PyListExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyListExpr(_BaseNode):

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        if open_bracket is None:
            open_bracket_out = PyOpenBracket()
        elif isinstance(open_bracket, PyOpenBracket):
            open_bracket_out = open_bracket
        else:
            raise ValueError("the field 'open_bracket' received an unrecognised value'")
        self.open_bracket: PyOpenBracket = open_bracket_out
        if elements is None:
            elements_out = Punctuated()
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
            elements_out = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        self.elements: Punctuated[PyExpr, PyComma] = elements_out
        if close_bracket is None:
            close_bracket_out = PyCloseBracket()
        elif isinstance(close_bracket, PyCloseBracket):
            close_bracket_out = close_bracket
        else:
            raise ValueError("the field 'close_bracket' received an unrecognised value'")
        self.close_bracket: PyCloseBracket = close_bracket_out

    def parent(self) -> PyListExprParent:
        assert(self._parent is not None)
        return self._parent


type PyTupleExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyTupleExpr(_BaseNode):

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            open_paren_out = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            open_paren_out = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        self.open_paren: PyOpenParen = open_paren_out
        if elements is None:
            elements_out = Punctuated()
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
            elements_out = new_elements
        else:
            raise ValueError("the field 'elements' received an unrecognised value'")
        self.elements: Punctuated[PyExpr, PyComma] = elements_out
        if close_paren is None:
            close_paren_out = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            close_paren_out = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")
        self.close_paren: PyCloseParen = close_paren_out

    def parent(self) -> PyTupleExprParent:
        assert(self._parent is not None)
        return self._parent


type PyArg = PyKeywordArg | PyExpr


def is_py_arg(value: Any) -> TypeGuard[PyArg]:
    return isinstance(value, PyKeywordArg) or is_py_expr(value)


type PyKeywordArgParent = PyCallExpr


class PyKeywordArg(_BaseNode):

    def __init__(self, name: 'str | PyIdent', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out
        if equals is None:
            equals_out = PyEquals()
        elif isinstance(equals, PyEquals):
            equals_out = equals
        else:
            raise ValueError("the field 'equals' received an unrecognised value'")
        self.equals: PyEquals = equals_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyKeywordArgParent:
        assert(self._parent is not None)
        return self._parent


type PyCallExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyCallExpr(_BaseNode):

    def __init__(self, operator: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, args: 'list[PyArg] | list[tuple[PyArg, PyComma | None | None]] | Punctuated[PyArg, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        operator_out = operator
        self.operator: PyExpr = operator_out
        if open_paren is None:
            open_paren_out = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            open_paren_out = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        self.open_paren: PyOpenParen = open_paren_out
        if args is None:
            args_out = Punctuated()
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
            args_out = new_args
        else:
            raise ValueError("the field 'args' received an unrecognised value'")
        self.args: Punctuated[PyArg, PyComma] = args_out
        if close_paren is None:
            close_paren_out = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            close_paren_out = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")
        self.close_paren: PyCloseParen = close_paren_out

    def parent(self) -> PyCallExprParent:
        assert(self._parent is not None)
        return self._parent


type PyPrefixOp = PyNotKeyword | PyPlus | PyHyphen | PyTilde


def is_py_prefix_op(value: Any) -> TypeGuard[PyPrefixOp]:
    return isinstance(value, PyNotKeyword) or isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyTilde)


type PyPrefixExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyPrefixExpr(_BaseNode):

    def __init__(self, prefix_op: 'PyPrefixOp', expr: 'PyExpr') -> None:
        prefix_op_out = prefix_op
        self.prefix_op: PyPrefixOp = prefix_op_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyPrefixExprParent:
        assert(self._parent is not None)
        return self._parent


type PyInfixOp = PyPlus | PyHyphen | PyAsterisk | PySlash | PySlashSlash | PyPercenct | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyAtSign | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | tuple[PyIsKeyword, PyNotKeyword] | PyInKeyword | tuple[PyNotKeyword, PyInKeyword]


def is_py_infix_op(value: Any) -> TypeGuard[PyInfixOp]:
    return isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyAsterisk) or isinstance(value, PySlash) or isinstance(value, PySlashSlash) or isinstance(value, PyPercenct) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyVerticalBar) or isinstance(value, PyCaret) or isinstance(value, PyAmpersand) or isinstance(value, PyAtSign) or isinstance(value, PyOrKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyEqualsEquals) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyLessThan) or isinstance(value, PyLessThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyIsKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyIsKeyword) and isinstance(value[1], PyNotKeyword)) or isinstance(value, PyInKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyNotKeyword) and isinstance(value[1], PyInKeyword))


type PyInfixExprParent = PySlice | PyComprehension | PyGeneratorExpr | PyGuard | PyAttrExpr | PyDecorator | PyIfCase | PyNamedParam | PyElifCase | PyAssignStmt | PyStarredPattern | PyExceptHandler | PySubscriptExpr | PyTypeAliasStmt | PyWhileStmt | PyFuncDef | PyExprStmt | PyListExpr | PyInfixExpr | PyKeywordArg | PyRetStmt | PyRaiseStmt | PyNestExpr | PyPrefixExpr | PyTupleExpr | PyForStmt | PyCallExpr | PyStarredExpr


class PyInfixExpr(_BaseNode):

    def __init__(self, left: 'PyExpr', op: 'PyInfixOp', right: 'PyExpr') -> None:
        left_out = left
        self.left: PyExpr = left_out
        op_out = op
        self.op: PyInfixOp = op_out
        right_out = right
        self.right: PyExpr = right_out

    def parent(self) -> PyInfixExprParent:
        assert(self._parent is not None)
        return self._parent


type PyQualNameParent = PyAbsolutePath | PyRelativePath


class PyQualName(_BaseNode):

    def __init__(self, name: 'str | PyIdent', *, modules: 'list[str | PyIdent | tuple[str | PyIdent, PyDot | None]] | None' = None) -> None:
        if modules is None:
            modules_out = list()
        elif isinstance(modules, list):
            new_modules = list()
            for modules_element in modules:
                if isinstance(modules_element, str):
                    new_modules_element = (PyIdent(modules_element), PyDot())
                elif isinstance(modules_element, PyIdent):
                    new_modules_element = (modules_element, PyDot())
                elif isinstance(modules_element, tuple):
                    assert(isinstance(modules_element, tuple))
                    modules_element_0 = modules_element[0]
                    if isinstance(modules_element_0, str):
                        new_modules_element_0 = PyIdent(modules_element_0)
                    elif isinstance(modules_element_0, PyIdent):
                        new_modules_element_0 = modules_element_0
                    else:
                        raise ValueError("the field 'modules' received an unrecognised value'")
                    modules_element_1 = modules_element[1]
                    if modules_element_1 is None:
                        new_modules_element_1 = PyDot()
                    elif isinstance(modules_element_1, PyDot):
                        new_modules_element_1 = modules_element_1
                    else:
                        raise ValueError("the field 'modules' received an unrecognised value'")
                    new_modules_element = (new_modules_element_0, new_modules_element_1)
                else:
                    raise ValueError("the field 'modules' received an unrecognised value'")
                new_modules.append(new_modules_element)
            modules_out = new_modules
        else:
            raise ValueError("the field 'modules' received an unrecognised value'")
        self.modules: list[tuple[PyIdent, PyDot]] = modules_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyQualNameParent:
        assert(self._parent is not None)
        return self._parent


type PyAbsolutePathParent = PyAlias | PyImportFromStmt


class PyAbsolutePath(_BaseNode):

    def __init__(self, name: 'PyQualName') -> None:
        name_out = name
        self.name: PyQualName = name_out

    def parent(self) -> PyAbsolutePathParent:
        assert(self._parent is not None)
        return self._parent


type PyRelativePathParent = PyAlias | PyImportFromStmt


class PyRelativePath(_BaseNode):

    def __init__(self, *, dots: 'list[PyDot | None] | None' = None, name: 'PyQualName | None' = None) -> None:
        if dots is None:
            dots_out = list()
        elif isinstance(dots, list):
            new_dots = list()
            for dots_element in dots:
                if dots_element is None:
                    new_dots_element = PyDot()
                elif isinstance(dots_element, PyDot):
                    new_dots_element = dots_element
                else:
                    raise ValueError("the field 'dots' received an unrecognised value'")
                new_dots.append(new_dots_element)
            dots_out = new_dots
        else:
            raise ValueError("the field 'dots' received an unrecognised value'")
        self.dots: list[PyDot] = dots_out
        if isinstance(name, PyQualName):
            name_out = name
        elif name is None:
            name_out = None
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyQualName | None = name_out

    def parent(self) -> PyRelativePathParent:
        assert(self._parent is not None)
        return self._parent


type PyPath = PyAbsolutePath | PyRelativePath


def is_py_path(value: Any) -> TypeGuard[PyPath]:
    return isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath)


type PyAliasParent = PyImportStmt | PyImportFromStmt


class PyAlias(_BaseNode):

    def __init__(self, path: 'PyPath', *, asname: 'str | PyIdent | tuple[PyAsKeyword | None, str | PyIdent] | None' = None) -> None:
        path_out = path
        self.path: PyPath = path_out
        if isinstance(asname, str):
            asname_out = (PyAsKeyword(), PyIdent(asname))
        elif isinstance(asname, PyIdent):
            asname_out = (PyAsKeyword(), asname)
        elif isinstance(asname, tuple):
            assert(isinstance(asname, tuple))
            asname_0 = asname[0]
            if asname_0 is None:
                new_asname_0 = PyAsKeyword()
            elif isinstance(asname_0, PyAsKeyword):
                new_asname_0 = asname_0
            else:
                raise ValueError("the field 'asname' received an unrecognised value'")
            asname_1 = asname[1]
            if isinstance(asname_1, str):
                new_asname_1 = PyIdent(asname_1)
            elif isinstance(asname_1, PyIdent):
                new_asname_1 = asname_1
            else:
                raise ValueError("the field 'asname' received an unrecognised value'")
            asname_out = (new_asname_0, new_asname_1)
        elif asname is None:
            asname_out = None
        else:
            raise ValueError("the field 'asname' received an unrecognised value'")
        self.asname: tuple[PyAsKeyword, PyIdent] | None = asname_out

    def parent(self) -> PyAliasParent:
        assert(self._parent is not None)
        return self._parent


type PyImportStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyImportStmt(_BaseNode):

    def __init__(self, *, import_keyword: 'PyImportKeyword | None' = None, aliases: 'list[PyAlias] | list[tuple[PyAlias, PyComma | None | None]] | Punctuated[PyAlias, PyComma | None] | None' = None) -> None:
        if import_keyword is None:
            import_keyword_out = PyImportKeyword()
        elif isinstance(import_keyword, PyImportKeyword):
            import_keyword_out = import_keyword
        else:
            raise ValueError("the field 'import_keyword' received an unrecognised value'")
        self.import_keyword: PyImportKeyword = import_keyword_out
        if aliases is None:
            aliases_out = Punctuated()
        elif isinstance(aliases, list) or isinstance(aliases, list) or isinstance(aliases, Punctuated):
            new_aliases = Punctuated()
            aliases_iter = iter(aliases)
            try:
                first_aliases_element = next(aliases_iter)
                while True:
                    try:
                        second_aliases_element = next(aliases_iter)
                        if isinstance(first_aliases_element, tuple):
                            aliases_value = first_aliases_element[0]
                            aliases_separator = first_aliases_element[1]
                        else:
                            aliases_value = first_aliases_element
                            aliases_separator = None
                        new_aliases_value = aliases_value
                        if aliases_separator is None:
                            new_aliases_separator = PyComma()
                        elif isinstance(aliases_separator, PyComma):
                            new_aliases_separator = aliases_separator
                        else:
                            raise ValueError("the field 'aliases' received an unrecognised value'")
                        new_aliases.append(new_aliases_value, new_aliases_separator)
                        first_aliases_element = second_aliases_element
                    except StopIteration:
                        if isinstance(first_aliases_element, tuple):
                            aliases_value = first_aliases_element[0]
                            assert(first_aliases_element[1] is None)
                        else:
                            aliases_value = first_aliases_element
                        new_aliases_value = aliases_value
                        new_aliases.append(new_aliases_value)
                        break
            except StopIteration:
                pass
            aliases_out = new_aliases
        else:
            raise ValueError("the field 'aliases' received an unrecognised value'")
        self.aliases: Punctuated[PyAlias, PyComma] = aliases_out

    def parent(self) -> PyImportStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyImportFromStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyImportFromStmt(_BaseNode):

    def __init__(self, path: 'PyPath', *, from_keyword: 'PyFromKeyword | None' = None, import_keyword: 'PyImportKeyword | None' = None, aliases: 'list[PyAlias] | list[tuple[PyAlias, PyComma | None | None]] | Punctuated[PyAlias, PyComma | None] | None' = None) -> None:
        if from_keyword is None:
            from_keyword_out = PyFromKeyword()
        elif isinstance(from_keyword, PyFromKeyword):
            from_keyword_out = from_keyword
        else:
            raise ValueError("the field 'from_keyword' received an unrecognised value'")
        self.from_keyword: PyFromKeyword = from_keyword_out
        path_out = path
        self.path: PyPath = path_out
        if import_keyword is None:
            import_keyword_out = PyImportKeyword()
        elif isinstance(import_keyword, PyImportKeyword):
            import_keyword_out = import_keyword
        else:
            raise ValueError("the field 'import_keyword' received an unrecognised value'")
        self.import_keyword: PyImportKeyword = import_keyword_out
        if aliases is None:
            aliases_out = Punctuated()
        elif isinstance(aliases, list) or isinstance(aliases, list) or isinstance(aliases, Punctuated):
            new_aliases = Punctuated()
            aliases_iter = iter(aliases)
            try:
                first_aliases_element = next(aliases_iter)
                while True:
                    try:
                        second_aliases_element = next(aliases_iter)
                        if isinstance(first_aliases_element, tuple):
                            aliases_value = first_aliases_element[0]
                            aliases_separator = first_aliases_element[1]
                        else:
                            aliases_value = first_aliases_element
                            aliases_separator = None
                        new_aliases_value = aliases_value
                        if aliases_separator is None:
                            new_aliases_separator = PyComma()
                        elif isinstance(aliases_separator, PyComma):
                            new_aliases_separator = aliases_separator
                        else:
                            raise ValueError("the field 'aliases' received an unrecognised value'")
                        new_aliases.append(new_aliases_value, new_aliases_separator)
                        first_aliases_element = second_aliases_element
                    except StopIteration:
                        if isinstance(first_aliases_element, tuple):
                            aliases_value = first_aliases_element[0]
                            assert(first_aliases_element[1] is None)
                        else:
                            aliases_value = first_aliases_element
                        new_aliases_value = aliases_value
                        new_aliases.append(new_aliases_value)
                        break
            except StopIteration:
                pass
            aliases_out = new_aliases
        else:
            raise ValueError("the field 'aliases' received an unrecognised value'")
        self.aliases: Punctuated[PyAlias, PyComma] = aliases_out

    def parent(self) -> PyImportFromStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyStmt = PyAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyIfStmt | PyImportStmt | PyImportFromStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt


def is_py_stmt(value: Any) -> TypeGuard[PyStmt]:
    return isinstance(value, PyAssignStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyClassDef) or isinstance(value, PyContinueStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyForStmt) or isinstance(value, PyFuncDef) or isinstance(value, PyIfStmt) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyTryStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyWhileStmt)


type PyRetStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyRetStmt(_BaseNode):

    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> None:
        if return_keyword is None:
            return_keyword_out = PyReturnKeyword()
        elif isinstance(return_keyword, PyReturnKeyword):
            return_keyword_out = return_keyword
        else:
            raise ValueError("the field 'return_keyword' received an unrecognised value'")
        self.return_keyword: PyReturnKeyword = return_keyword_out
        if is_py_expr(expr):
            expr_out = expr
        elif expr is None:
            expr_out = None
        else:
            raise ValueError("the field 'expr' received an unrecognised value'")
        self.expr: PyExpr | None = expr_out

    def parent(self) -> PyRetStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyExprStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyExprStmt(_BaseNode):

    def __init__(self, expr: 'PyExpr') -> None:
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyExprStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyAssignStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyAssignStmt(_BaseNode):

    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, equals: 'PyEquals | None' = None) -> None:
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out
        if is_py_expr(annotation):
            annotation_out = (PyColon(), annotation)
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
            annotation_out = (new_annotation_0, new_annotation_1)
        elif annotation is None:
            annotation_out = None
        else:
            raise ValueError("the field 'annotation' received an unrecognised value'")
        self.annotation: tuple[PyColon, PyExpr] | None = annotation_out
        if equals is None:
            equals_out = PyEquals()
        elif isinstance(equals, PyEquals):
            equals_out = equals
        else:
            raise ValueError("the field 'equals' received an unrecognised value'")
        self.equals: PyEquals = equals_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyAssignStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyPassStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyPassStmt(_BaseNode):

    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None) -> None:
        if pass_keyword is None:
            pass_keyword_out = PyPassKeyword()
        elif isinstance(pass_keyword, PyPassKeyword):
            pass_keyword_out = pass_keyword
        else:
            raise ValueError("the field 'pass_keyword' received an unrecognised value'")
        self.pass_keyword: PyPassKeyword = pass_keyword_out

    def parent(self) -> PyPassStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyIfCaseParent = PyIfStmt


class PyIfCase(_BaseNode):

    def __init__(self, test: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if if_keyword is None:
            if_keyword_out = PyIfKeyword()
        elif isinstance(if_keyword, PyIfKeyword):
            if_keyword_out = if_keyword
        else:
            raise ValueError("the field 'if_keyword' received an unrecognised value'")
        self.if_keyword: PyIfKeyword = if_keyword_out
        test_out = test
        self.test: PyExpr = test_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out

    def parent(self) -> PyIfCaseParent:
        assert(self._parent is not None)
        return self._parent


type PyElifCaseParent = PyIfStmt


class PyElifCase(_BaseNode):

    def __init__(self, test: 'PyExpr', *, elif_keyword: 'PyElifKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if elif_keyword is None:
            elif_keyword_out = PyElifKeyword()
        elif isinstance(elif_keyword, PyElifKeyword):
            elif_keyword_out = elif_keyword
        else:
            raise ValueError("the field 'elif_keyword' received an unrecognised value'")
        self.elif_keyword: PyElifKeyword = elif_keyword_out
        test_out = test
        self.test: PyExpr = test_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out

    def parent(self) -> PyElifCaseParent:
        assert(self._parent is not None)
        return self._parent


type PyElseCaseParent = PyIfStmt


class PyElseCase(_BaseNode):

    def __init__(self, *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if else_keyword is None:
            else_keyword_out = PyElseKeyword()
        elif isinstance(else_keyword, PyElseKeyword):
            else_keyword_out = else_keyword
        else:
            raise ValueError("the field 'else_keyword' received an unrecognised value'")
        self.else_keyword: PyElseKeyword = else_keyword_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out

    def parent(self) -> PyElseCaseParent:
        assert(self._parent is not None)
        return self._parent


type PyIfStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyIfStmt(_BaseNode):

    def __init__(self, first: 'PyIfCase', *, alternatives: 'list[PyElifCase] | None' = None, last: 'PyElseCase | None' = None) -> None:
        first_out = first
        self.first: PyIfCase = first_out
        if alternatives is None:
            alternatives_out = list()
        elif isinstance(alternatives, list):
            new_alternatives = list()
            for alternatives_element in alternatives:
                new_alternatives_element = alternatives_element
                new_alternatives.append(new_alternatives_element)
            alternatives_out = new_alternatives
        else:
            raise ValueError("the field 'alternatives' received an unrecognised value'")
        self.alternatives: list[PyElifCase] = alternatives_out
        if isinstance(last, PyElseCase):
            last_out = last
        elif last is None:
            last_out = None
        else:
            raise ValueError("the field 'last' received an unrecognised value'")
        self.last: PyElseCase | None = last_out

    def parent(self) -> PyIfStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyDeleteStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyDeleteStmt(_BaseNode):

    def __init__(self, pattern: 'PyPattern', *, del_keyword: 'PyDelKeyword | None' = None) -> None:
        if del_keyword is None:
            del_keyword_out = PyDelKeyword()
        elif isinstance(del_keyword, PyDelKeyword):
            del_keyword_out = del_keyword
        else:
            raise ValueError("the field 'del_keyword' received an unrecognised value'")
        self.del_keyword: PyDelKeyword = del_keyword_out
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out

    def parent(self) -> PyDeleteStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyRaiseStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyRaiseStmt(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, raise_keyword: 'PyRaiseKeyword | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None) -> None:
        if raise_keyword is None:
            raise_keyword_out = PyRaiseKeyword()
        elif isinstance(raise_keyword, PyRaiseKeyword):
            raise_keyword_out = raise_keyword
        else:
            raise ValueError("the field 'raise_keyword' received an unrecognised value'")
        self.raise_keyword: PyRaiseKeyword = raise_keyword_out
        expr_out = expr
        self.expr: PyExpr = expr_out
        if is_py_expr(cause):
            cause_out = (PyFromKeyword(), cause)
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
            cause_out = (new_cause_0, new_cause_1)
        elif cause is None:
            cause_out = None
        else:
            raise ValueError("the field 'cause' received an unrecognised value'")
        self.cause: tuple[PyFromKeyword, PyExpr] | None = cause_out

    def parent(self) -> PyRaiseStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyForStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyForStmt(_BaseNode):

    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', *, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None, else_clause: 'PyStmt | list[PyStmt] | tuple[PyElseKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None) -> None:
        if for_keyword is None:
            for_keyword_out = PyForKeyword()
        elif isinstance(for_keyword, PyForKeyword):
            for_keyword_out = for_keyword
        else:
            raise ValueError("the field 'for_keyword' received an unrecognised value'")
        self.for_keyword: PyForKeyword = for_keyword_out
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out
        if in_keyword is None:
            in_keyword_out = PyInKeyword()
        elif isinstance(in_keyword, PyInKeyword):
            in_keyword_out = in_keyword
        else:
            raise ValueError("the field 'in_keyword' received an unrecognised value'")
        self.in_keyword: PyInKeyword = in_keyword_out
        expr_out = expr
        self.expr: PyExpr = expr_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out
        if is_py_stmt(else_clause):
            else_clause_out = (PyElseKeyword(), PyColon(), else_clause)
        elif isinstance(else_clause, list):
            new_else_clause = list()
            for else_clause_element in else_clause:
                new_else_clause_element = else_clause_element
                new_else_clause.append(new_else_clause_element)
            else_clause_out = (PyElseKeyword(), PyColon(), new_else_clause)
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
            else_clause_out = (new_else_clause_0, new_else_clause_1, new_else_clause_2)
        elif else_clause is None:
            else_clause_out = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = else_clause_out

    def parent(self) -> PyForStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyWhileStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyWhileStmt(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, while_keyword: 'PyWhileKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None, else_clause: 'PyStmt | list[PyStmt] | tuple[PyElseKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None) -> None:
        if while_keyword is None:
            while_keyword_out = PyWhileKeyword()
        elif isinstance(while_keyword, PyWhileKeyword):
            while_keyword_out = while_keyword
        else:
            raise ValueError("the field 'while_keyword' received an unrecognised value'")
        self.while_keyword: PyWhileKeyword = while_keyword_out
        expr_out = expr
        self.expr: PyExpr = expr_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out
        if is_py_stmt(else_clause):
            else_clause_out = (PyElseKeyword(), PyColon(), else_clause)
        elif isinstance(else_clause, list):
            new_else_clause = list()
            for else_clause_element in else_clause:
                new_else_clause_element = else_clause_element
                new_else_clause.append(new_else_clause_element)
            else_clause_out = (PyElseKeyword(), PyColon(), new_else_clause)
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
            else_clause_out = (new_else_clause_0, new_else_clause_1, new_else_clause_2)
        elif else_clause is None:
            else_clause_out = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = else_clause_out

    def parent(self) -> PyWhileStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyBreakStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyBreakStmt(_BaseNode):

    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None) -> None:
        if break_keyword is None:
            break_keyword_out = PyBreakKeyword()
        elif isinstance(break_keyword, PyBreakKeyword):
            break_keyword_out = break_keyword
        else:
            raise ValueError("the field 'break_keyword' received an unrecognised value'")
        self.break_keyword: PyBreakKeyword = break_keyword_out

    def parent(self) -> PyBreakStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyContinueStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyContinueStmt(_BaseNode):

    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None) -> None:
        if continue_keyword is None:
            continue_keyword_out = PyContinueKeyword()
        elif isinstance(continue_keyword, PyContinueKeyword):
            continue_keyword_out = continue_keyword
        else:
            raise ValueError("the field 'continue_keyword' received an unrecognised value'")
        self.continue_keyword: PyContinueKeyword = continue_keyword_out

    def parent(self) -> PyContinueStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyTypeAliasStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyTypeAliasStmt(_BaseNode):

    def __init__(self, name: 'str | PyIdent', expr: 'PyExpr', *, type_keyword: 'PyTypeKeyword | None' = None, type_params: 'list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | tuple[PyOpenBracket | None, list[PyExpr] | list[tuple[PyExpr, PyComma | None | None]] | Punctuated[PyExpr, PyComma | None] | None, PyCloseBracket | None] | None' = None, equals: 'PyEquals | None' = None) -> None:
        if type_keyword is None:
            type_keyword_out = PyTypeKeyword()
        elif isinstance(type_keyword, PyTypeKeyword):
            type_keyword_out = type_keyword
        else:
            raise ValueError("the field 'type_keyword' received an unrecognised value'")
        self.type_keyword: PyTypeKeyword = type_keyword_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out
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
            type_params_out = (PyOpenBracket(), new_type_params, PyCloseBracket())
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
            type_params_out = (new_type_params_0, new_type_params_1, new_type_params_2)
        elif type_params is None:
            type_params_out = None
        else:
            raise ValueError("the field 'type_params' received an unrecognised value'")
        self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = type_params_out
        if equals is None:
            equals_out = PyEquals()
        elif isinstance(equals, PyEquals):
            equals_out = equals
        else:
            raise ValueError("the field 'equals' received an unrecognised value'")
        self.equals: PyEquals = equals_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyTypeAliasStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyExceptHandlerParent = PyTryStmt


class PyExceptHandler(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, except_keyword: 'PyExceptKeyword | None' = None, binder: 'str | PyIdent | tuple[PyAsKeyword | None, str | PyIdent] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if except_keyword is None:
            except_keyword_out = PyExceptKeyword()
        elif isinstance(except_keyword, PyExceptKeyword):
            except_keyword_out = except_keyword
        else:
            raise ValueError("the field 'except_keyword' received an unrecognised value'")
        self.except_keyword: PyExceptKeyword = except_keyword_out
        expr_out = expr
        self.expr: PyExpr = expr_out
        if isinstance(binder, str):
            binder_out = (PyAsKeyword(), PyIdent(binder))
        elif isinstance(binder, PyIdent):
            binder_out = (PyAsKeyword(), binder)
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
            binder_out = (new_binder_0, new_binder_1)
        elif binder is None:
            binder_out = None
        else:
            raise ValueError("the field 'binder' received an unrecognised value'")
        self.binder: tuple[PyAsKeyword, PyIdent] | None = binder_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out

    def parent(self) -> PyExceptHandlerParent:
        assert(self._parent is not None)
        return self._parent


type PyTryStmtParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyTryStmt(_BaseNode):

    def __init__(self, *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None, handlers: 'list[PyExceptHandler] | None' = None, else_clause: 'PyStmt | list[PyStmt] | tuple[PyElseKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None, finally_clause: 'PyStmt | list[PyStmt] | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | list[PyStmt] | None] | None' = None) -> None:
        if try_keyword is None:
            try_keyword_out = PyTryKeyword()
        elif isinstance(try_keyword, PyTryKeyword):
            try_keyword_out = try_keyword
        else:
            raise ValueError("the field 'try_keyword' received an unrecognised value'")
        self.try_keyword: PyTryKeyword = try_keyword_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out
        if handlers is None:
            handlers_out = list()
        elif isinstance(handlers, list):
            new_handlers = list()
            for handlers_element in handlers:
                new_handlers_element = handlers_element
                new_handlers.append(new_handlers_element)
            handlers_out = new_handlers
        else:
            raise ValueError("the field 'handlers' received an unrecognised value'")
        self.handlers: list[PyExceptHandler] = handlers_out
        if is_py_stmt(else_clause):
            else_clause_out = (PyElseKeyword(), PyColon(), else_clause)
        elif isinstance(else_clause, list):
            new_else_clause = list()
            for else_clause_element in else_clause:
                new_else_clause_element = else_clause_element
                new_else_clause.append(new_else_clause_element)
            else_clause_out = (PyElseKeyword(), PyColon(), new_else_clause)
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
            else_clause_out = (new_else_clause_0, new_else_clause_1, new_else_clause_2)
        elif else_clause is None:
            else_clause_out = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = else_clause_out
        if is_py_stmt(finally_clause):
            finally_clause_out = (PyFinallyKeyword(), PyColon(), finally_clause)
        elif isinstance(finally_clause, list):
            new_finally_clause = list()
            for finally_clause_element in finally_clause:
                new_finally_clause_element = finally_clause_element
                new_finally_clause.append(new_finally_clause_element)
            finally_clause_out = (PyFinallyKeyword(), PyColon(), new_finally_clause)
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
            finally_clause_out = (new_finally_clause_0, new_finally_clause_1, new_finally_clause_2)
        elif finally_clause is None:
            finally_clause_out = None
        else:
            raise ValueError("the field 'finally_clause' received an unrecognised value'")
        self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None = finally_clause_out

    def parent(self) -> PyTryStmtParent:
        assert(self._parent is not None)
        return self._parent


type PyClassDefParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyClassDef(_BaseNode):

    def __init__(self, name: 'str | PyIdent', *, class_keyword: 'PyClassKeyword | None' = None, bases: 'list[str | PyIdent] | list[tuple[str | PyIdent, PyComma | None | None]] | Punctuated[str | PyIdent, PyComma | None] | tuple[PyOpenParen | None, list[str | PyIdent] | list[tuple[str | PyIdent, PyComma | None | None]] | Punctuated[str | PyIdent, PyComma | None] | None, PyCloseParen | None] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if class_keyword is None:
            class_keyword_out = PyClassKeyword()
        elif isinstance(class_keyword, PyClassKeyword):
            class_keyword_out = class_keyword
        else:
            raise ValueError("the field 'class_keyword' received an unrecognised value'")
        self.class_keyword: PyClassKeyword = class_keyword_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out
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
            bases_out = (PyOpenParen(), new_bases, PyCloseParen())
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
            bases_out = (new_bases_0, new_bases_1, new_bases_2)
        elif bases is None:
            bases_out = None
        else:
            raise ValueError("the field 'bases' received an unrecognised value'")
        self.bases: tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None = bases_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out

    def parent(self) -> PyClassDefParent:
        assert(self._parent is not None)
        return self._parent


type PyParam = PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam


def is_py_param(value: Any) -> TypeGuard[PyParam]:
    return isinstance(value, PyNamedParam) or isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PySepParam)


type PyNamedParamParent = PyFuncDef


class PyNamedParam(_BaseNode):

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        pattern_out = pattern
        self.pattern: PyPattern = pattern_out
        if is_py_expr(annotation):
            annotation_out = (PyColon(), annotation)
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
            annotation_out = (new_annotation_0, new_annotation_1)
        elif annotation is None:
            annotation_out = None
        else:
            raise ValueError("the field 'annotation' received an unrecognised value'")
        self.annotation: tuple[PyColon, PyExpr] | None = annotation_out
        if is_py_expr(default):
            default_out = (PyEquals(), default)
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
            default_out = (new_default_0, new_default_1)
        elif default is None:
            default_out = None
        else:
            raise ValueError("the field 'default' received an unrecognised value'")
        self.default: tuple[PyEquals, PyExpr] | None = default_out

    def parent(self) -> PyNamedParamParent:
        assert(self._parent is not None)
        return self._parent


type PyRestPosParamParent = PyFuncDef


class PyRestPosParam(_BaseNode):

    def __init__(self, name: 'str | PyIdent', *, asterisk: 'PyAsterisk | None' = None) -> None:
        if asterisk is None:
            asterisk_out = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            asterisk_out = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")
        self.asterisk: PyAsterisk = asterisk_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyRestPosParamParent:
        assert(self._parent is not None)
        return self._parent


type PyRestKeywordParamParent = PyFuncDef


class PyRestKeywordParam(_BaseNode):

    def __init__(self, name: 'str | PyIdent', *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None) -> None:
        if asterisk_asterisk is None:
            asterisk_asterisk_out = PyAsteriskAsterisk()
        elif isinstance(asterisk_asterisk, PyAsteriskAsterisk):
            asterisk_asterisk_out = asterisk_asterisk
        else:
            raise ValueError("the field 'asterisk_asterisk' received an unrecognised value'")
        self.asterisk_asterisk: PyAsteriskAsterisk = asterisk_asterisk_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out

    def parent(self) -> PyRestKeywordParamParent:
        assert(self._parent is not None)
        return self._parent


type PySepParamParent = PyFuncDef


class PySepParam(_BaseNode):

    def __init__(self, *, asterisk: 'PyAsterisk | None' = None) -> None:
        if asterisk is None:
            asterisk_out = PyAsterisk()
        elif isinstance(asterisk, PyAsterisk):
            asterisk_out = asterisk
        else:
            raise ValueError("the field 'asterisk' received an unrecognised value'")
        self.asterisk: PyAsterisk = asterisk_out

    def parent(self) -> PySepParamParent:
        assert(self._parent is not None)
        return self._parent


type PyDecoratorParent = PyFuncDef


class PyDecorator(_BaseNode):

    def __init__(self, expr: 'PyExpr', *, at_sign: 'PyAtSign | None' = None) -> None:
        if at_sign is None:
            at_sign_out = PyAtSign()
        elif isinstance(at_sign, PyAtSign):
            at_sign_out = at_sign
        else:
            raise ValueError("the field 'at_sign' received an unrecognised value'")
        self.at_sign: PyAtSign = at_sign_out
        expr_out = expr
        self.expr: PyExpr = expr_out

    def parent(self) -> PyDecoratorParent:
        assert(self._parent is not None)
        return self._parent


type PyFuncDefParent = PyTryStmt | PyModule | PyFuncDef | PyWhileStmt | PyForStmt | PyIfCase | PyClassDef | PyElifCase | PyElseCase | PyExceptHandler


class PyFuncDef(_BaseNode):

    def __init__(self, name: 'str | PyIdent', *, decorators: 'list[PyDecorator] | None' = None, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, open_paren: 'PyOpenParen | None' = None, params: 'list[PyParam] | list[tuple[PyParam, PyComma | None | None]] | Punctuated[PyParam, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[PyHyphenGreaterThan | None, PyExpr] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | list[PyStmt] | None' = None) -> None:
        if decorators is None:
            decorators_out = list()
        elif isinstance(decorators, list):
            new_decorators = list()
            for decorators_element in decorators:
                new_decorators_element = decorators_element
                new_decorators.append(new_decorators_element)
            decorators_out = new_decorators
        else:
            raise ValueError("the field 'decorators' received an unrecognised value'")
        self.decorators: list[PyDecorator] = decorators_out
        if isinstance(async_keyword, PyAsyncKeyword):
            async_keyword_out = async_keyword
        elif async_keyword is None:
            async_keyword_out = None
        else:
            raise ValueError("the field 'async_keyword' received an unrecognised value'")
        self.async_keyword: PyAsyncKeyword | None = async_keyword_out
        if def_keyword is None:
            def_keyword_out = PyDefKeyword()
        elif isinstance(def_keyword, PyDefKeyword):
            def_keyword_out = def_keyword
        else:
            raise ValueError("the field 'def_keyword' received an unrecognised value'")
        self.def_keyword: PyDefKeyword = def_keyword_out
        if isinstance(name, str):
            name_out = PyIdent(name)
        elif isinstance(name, PyIdent):
            name_out = name
        else:
            raise ValueError("the field 'name' received an unrecognised value'")
        self.name: PyIdent = name_out
        if open_paren is None:
            open_paren_out = PyOpenParen()
        elif isinstance(open_paren, PyOpenParen):
            open_paren_out = open_paren
        else:
            raise ValueError("the field 'open_paren' received an unrecognised value'")
        self.open_paren: PyOpenParen = open_paren_out
        if params is None:
            params_out = Punctuated()
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
            params_out = new_params
        else:
            raise ValueError("the field 'params' received an unrecognised value'")
        self.params: Punctuated[PyParam, PyComma] = params_out
        if close_paren is None:
            close_paren_out = PyCloseParen()
        elif isinstance(close_paren, PyCloseParen):
            close_paren_out = close_paren
        else:
            raise ValueError("the field 'close_paren' received an unrecognised value'")
        self.close_paren: PyCloseParen = close_paren_out
        if is_py_expr(return_type):
            return_type_out = (PyHyphenGreaterThan(), return_type)
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
            return_type_out = (new_return_type_0, new_return_type_1)
        elif return_type is None:
            return_type_out = None
        else:
            raise ValueError("the field 'return_type' received an unrecognised value'")
        self.return_type: tuple[PyHyphenGreaterThan, PyExpr] | None = return_type_out
        if colon is None:
            colon_out = PyColon()
        elif isinstance(colon, PyColon):
            colon_out = colon
        else:
            raise ValueError("the field 'colon' received an unrecognised value'")
        self.colon: PyColon = colon_out
        if is_py_stmt(body):
            body_out = body
        elif body is None:
            body_out = list()
        elif isinstance(body, list):
            new_body = list()
            for body_element in body:
                new_body_element = body_element
                new_body.append(new_body_element)
            body_out = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'")
        self.body: PyStmt | list[PyStmt] = body_out

    def parent(self) -> PyFuncDefParent:
        assert(self._parent is not None)
        return self._parent


type PyModuleParent = Never


class PyModule(_BaseNode):

    def __init__(self, *, stmts: 'list[PyStmt] | None' = None) -> None:
        if stmts is None:
            stmts_out = list()
        elif isinstance(stmts, list):
            new_stmts = list()
            for stmts_element in stmts:
                new_stmts_element = stmts_element
                new_stmts.append(new_stmts_element)
            stmts_out = new_stmts
        else:
            raise ValueError("the field 'stmts' received an unrecognised value'")
        self.stmts: list[PyStmt] = stmts_out

    def parent(self) -> PyModuleParent:
        raise AssertionError('trying to access the parent node of a top-level node')


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


class PyImportKeyword(_BaseToken):

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


PyToken = PyIdent | PyFloat | PyInteger | PyString | PyTilde | PyVerticalBar | PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyIsKeyword | PyInKeyword | PyImportKeyword | PyIfKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword | PyCaret | PyCloseBracket | PyOpenBracket | PyAtSign | PyGreaterThanGreaterThan | PyGreaterThanEquals | PyGreaterThan | PyEqualsEquals | PyEquals | PyLessThanEquals | PyLessThanLessThan | PyLessThan | PySemicolon | PyColon | PySlashSlash | PySlash | PyDot | PyHyphenGreaterThan | PyHyphen | PyComma | PyPlus | PyAsteriskAsterisk | PyAsterisk | PyCloseParen | PyOpenParen | PyAmpersand | PyPercenct | PyHashtag | PyExclamationMarkEquals | PyCarriageReturnLineFeed | PyLineFeed


PyNode = PySlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyGuard | PyComprehension | PyGeneratorExpr | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleExpr | PyKeywordArg | PyCallExpr | PyPrefixExpr | PyInfixExpr | PyQualName | PyAbsolutePath | PyRelativePath | PyAlias | PyImportStmt | PyImportFromStmt | PyRetStmt | PyExprStmt | PyAssignStmt | PyPassStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam | PyDecorator | PyFuncDef | PyModule


PySyntax = PyToken | PyNode




def for_each_py_child(node: PySyntax, proc: Callable[[PySyntax], None]):
    if is_py_token(node): return
    if isinstance(node, PySlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        elif node.lower is None:
            pass
        else:
            raise ValueError()
        proc(node.colon)
        if is_py_expr(node.upper):
            proc(node.upper)
        elif node.upper is None:
            pass
        else:
            raise ValueError()
        if isinstance(node.step, tuple):
            element_0 = node.step[0]
            proc(element_0)
            element_1 = node.step[1]
            proc(element_1)
        elif node.step is None:
            pass
        else:
            raise ValueError()
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
    if isinstance(node, PyQualName):
        for element_0 in node.modules:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            proc(element_2)
        proc(node.name)
        return
    if isinstance(node, PyAbsolutePath):
        proc(node.name)
        return
    if isinstance(node, PyRelativePath):
        for element_0 in node.dots:
            proc(element_0)
        if isinstance(node.name, PyQualName):
            proc(node.name)
        elif node.name is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyAlias):
        proc(node.path)
        if isinstance(node.asname, tuple):
            element_0 = node.asname[0]
            proc(element_0)
            element_1 = node.asname[1]
            proc(element_1)
        elif node.asname is None:
            pass
        else:
            raise ValueError()
        return
    if isinstance(node, PyImportStmt):
        proc(node.import_keyword)
        for (element_0, separator_0) in node.aliases:
            proc(element_0)
        return
    if isinstance(node, PyImportFromStmt):
        proc(node.from_keyword)
        proc(node.path)
        proc(node.import_keyword)
        for (element_0, separator_0) in node.aliases:
            proc(element_0)
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
    if isinstance(node, PyDecorator):
        proc(node.at_sign)
        proc(node.expr)
        return
    if isinstance(node, PyFuncDef):
        for element_0 in node.decorators:
            proc(element_0)
        if isinstance(node.async_keyword, PyAsyncKeyword):
            proc(node.async_keyword)
        elif node.async_keyword is None:
            pass
        else:
            raise ValueError()
        proc(node.def_keyword)
        proc(node.name)
        proc(node.open_paren)
        for (element_1, separator_0) in node.params:
            proc(element_1)
        proc(node.close_paren)
        if isinstance(node.return_type, tuple):
            element_2 = node.return_type[0]
            proc(element_2)
            element_3 = node.return_type[1]
            proc(element_3)
        elif node.return_type is None:
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
    if isinstance(node, PyModule):
        for element_0 in node.stmts:
            proc(element_0)
        return
