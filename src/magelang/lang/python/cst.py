
from typing import TypeAlias, TypeGuard, Any

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

class Token:

    def __init__(self, span: Span | None = None) -> None:
        self.span = span

class Node:

    def __init__(self) -> None:
        pass

class PyCarriageReturnLineFeed(Token):
    pass


class PyLineFeed(Token):
    pass


class PySemicolon(Token):
    pass


class PyZero(Token):
    pass


class PyDot(Token):
    pass


class PyDoubleQuote(Token):
    pass


class PySingleQuote(Token):
    pass


class PyColon(Token):
    pass


class PyOpenBracket(Token):
    pass


class PyComma(Token):
    pass


class PyCloseBracket(Token):
    pass


class PyAsterisk(Token):
    pass


class PyOpenParen(Token):
    pass


class PyCloseParen(Token):
    pass


class PyEquals(Token):
    pass


class PyNotKeyword(Token):
    pass


class PyPlus(Token):
    pass


class PyHyphen(Token):
    pass


class PyTilde(Token):
    pass


class PySlash(Token):
    pass


class PySlashSlash(Token):
    pass


class PyPercenct(Token):
    pass


class PyLessThanLessThan(Token):
    pass


class PyGreaterThanGreaterThan(Token):
    pass


class PyVerticalBar(Token):
    pass


class PyCaret(Token):
    pass


class PyAmpersand(Token):
    pass


class PyAtSign(Token):
    pass


class PyOrKeyword(Token):
    pass


class PyAndKeyword(Token):
    pass


class PyEqualsEquals(Token):
    pass


class PyExclamationMarkEquals(Token):
    pass


class PyLessThan(Token):
    pass


class PyLessThanEquals(Token):
    pass


class PyGreaterThan(Token):
    pass


class PyGreaterThanEquals(Token):
    pass


class PyIsKeyword(Token):
    pass


class PyInKeyword(Token):
    pass


class PyReturnKeyword(Token):
    pass


class PyIfKeyword(Token):
    pass


class PyElifKeyword(Token):
    pass


class PyElseKeyword(Token):
    pass


class PyDelKeyword(Token):
    pass


class PyRaiseKeyword(Token):
    pass


class PyFormKeyword(Token):
    pass


class PyTypeKeyword(Token):
    pass


class PyClassKeyword(Token):
    pass


class PyAsteriskAsterisk(Token):
    pass


class PyAsyncKeyword(Token):
    pass


class PyDefKeyword(Token):
    pass


class PyHyphenGreaterThan(Token):
    pass


class PyIdent(Token):

    def __init__(self, value: (str | None)=None, span: (Span | None)=None):
        super().__init__(span=span)
        self.value = value


class PyInteger(Token):

    def __init__(self, value: (int | None)=None, span: (Span | None)=None):
        super().__init__(span=span)
        self.value = value


class PyFloat(Token):

    def __init__(self, value: (float | None)=None, span: (Span | None)=None):
        super().__init__(span=span)
        self.value = value


class PyString(Token):

    def __init__(self, value: (str | None)=None, span: (Span | None)=None):
        super().__init__(span=span)
        self.value = value


class PySlice(Node):

    def __init__(self, *, lower: 'PyExpr', colon: '(PyColon | None)'=None,
        upper: 'PyExpr') ->None:
        self.lower: PyExpr = lower
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon
        self.upper: PyExpr = upper


PyPattern: TypeAlias = (
    'PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern'
    )


def is_py_pattern(value: Any) ->TypeGuard[PyPattern]:
    return ((((isinstance(value, PyNamedPattern) or isinstance(value,
        PyAttrPattern)) or isinstance(value, PySubscriptPattern)) or
        isinstance(value, PyStarredPattern)) or isinstance(value,
        PyListPattern)) or isinstance(value, PyTuplePattern)


class PyNamedPattern(Node):

    def __init__(self, *, name: '(PyIdent | str)') ->None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name


class PyAttrPattern(Node):

    def __init__(self, *, pattern: 'PyPattern', dot: '(PyDot | None)'=None,
        name: '(PyIdent | str)') ->None:
        self.pattern: PyPattern = pattern
        if dot is None:
            self.dot: PyDot = PyDot()
        else:
            self.dot: PyDot = dot
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name


class PySubscriptPattern(Node):

    def __init__(self, *, pattern: 'PyPattern', open_bracket:
        '(PyOpenBracket | None)'=None, slices:
        '(None | list[PyPattern | PySlice | tuple[PyPattern | PySlice, PyComma | None]])'
        =None, close_bracket: '(PyCloseBracket | None)'=None) ->None:
        self.pattern: PyPattern = pattern
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket
        if slices is None:
            self.slices: list[tuple[PyPattern | PySlice, PyComma | None]
                ] = list()
        else:
            new_slices = list()
            for slices_element in slices:
                if is_py_pattern(slices_element) or isinstance(slices_element,
                    PySlice):
                    new_slices_element = slices_element, None
                else:
                    assert(isinstance(slices_element, tuple))
                    slices_element_0 = slices_element[0]
                    new_slices_element_0 = slices_element_0
                    slices_element_1 = slices_element[1]
                    if isinstance(slices_element_1, PyComma):
                        new_slices_element_1 = slices_element_1
                    elif slices_element_1 is None:
                        new_slices_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'slices' received an unrecognised value'"
                            )
                    new_slices_element = (new_slices_element_0,
                        new_slices_element_1)
                new_slices.append(new_slices_element)
            self.slices: list[tuple[PyPattern | PySlice, PyComma | None]
                ] = new_slices
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket


class PyStarredPattern(Node):

    def __init__(self, *, asterisk: '(PyAsterisk | None)'=None, expr: 'PyExpr'
        ) ->None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk
        self.expr: PyExpr = expr


class PyListPattern(Node):

    def __init__(self, *, open_bracket: '(PyOpenBracket | None)'=None,
        elements:
        '(None | list[PyPattern | tuple[PyPattern, PyComma | None]])'=None,
        close_bracket: '(PyCloseBracket | None)'=None) ->None:
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket
        if elements is None:
            self.elements: list[tuple[PyPattern, PyComma | None]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                if is_py_pattern(elements_element):
                    new_elements_element = elements_element, None
                else:
                    assert(isinstance(elements_element, tuple))
                    elements_element_0 = elements_element[0]
                    new_elements_element_0 = elements_element_0
                    elements_element_1 = elements_element[1]
                    if isinstance(elements_element_1, PyComma):
                        new_elements_element_1 = elements_element_1
                    elif elements_element_1 is None:
                        new_elements_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'elements' received an unrecognised value'"
                            )
                    new_elements_element = (new_elements_element_0,
                        new_elements_element_1)
                new_elements.append(new_elements_element)
            self.elements: list[tuple[PyPattern, PyComma | None]
                ] = new_elements
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket


class PyTuplePattern(Node):

    def __init__(self, *, open_paren: '(PyOpenParen | None)'=None, elements:
        '(None | list[PyPattern | tuple[PyPattern, PyComma | None]])'=None,
        close_paren: '(PyCloseParen | None)'=None) ->None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren
        if elements is None:
            self.elements: list[tuple[PyPattern, PyComma | None]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                if is_py_pattern(elements_element):
                    new_elements_element = elements_element, None
                else:
                    assert(isinstance(elements_element, tuple))
                    elements_element_0 = elements_element[0]
                    new_elements_element_0 = elements_element_0
                    elements_element_1 = elements_element[1]
                    if isinstance(elements_element_1, PyComma):
                        new_elements_element_1 = elements_element_1
                    elif elements_element_1 is None:
                        new_elements_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'elements' received an unrecognised value'"
                            )
                    new_elements_element = (new_elements_element_0,
                        new_elements_element_1)
                new_elements.append(new_elements_element)
            self.elements: list[tuple[PyPattern, PyComma | None]
                ] = new_elements
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren


PyExpr: TypeAlias = (
    'PyAttrExpr | PyCallExpr | PyConstExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr'
    )


def is_py_expr(value: Any) ->TypeGuard[PyExpr]:
    return (((((((((isinstance(value, PyAttrExpr) or isinstance(value,
        PyCallExpr)) or isinstance(value, PyConstExpr)) or isinstance(value,
        PyInfixExpr)) or isinstance(value, PyListExpr)) or isinstance(value,
        PyNamedExpr)) or isinstance(value, PyNestExpr)) or isinstance(value,
        PyPrefixExpr)) or isinstance(value, PyStarredExpr)) or isinstance(
        value, PySubscriptExpr)) or isinstance(value, PyTupleExpr)


class PyConstExpr(Node):

    def __init__(self, *, literal:
        '(PyString | str | (PyFloat | float) | (PyInteger | int))') ->None:
        if isinstance(literal, PyString) or isinstance(literal, str):
            if isinstance(literal, str):
                self.literal: PyString | PyFloat | PyInteger = PyString(literal
                    )
            else:
                self.literal: PyString | PyFloat | PyInteger = literal
        elif isinstance(literal, PyFloat) or isinstance(literal, float):
            if isinstance(literal, float):
                self.literal: PyString | PyFloat | PyInteger = PyFloat(literal)
            else:
                self.literal: PyString | PyFloat | PyInteger = literal
        elif isinstance(literal, PyInteger) or isinstance(literal, int):
            if isinstance(literal, int):
                self.literal: PyString | PyFloat | PyInteger = PyInteger(
                    literal)
            else:
                self.literal: PyString | PyFloat | PyInteger = literal
        else:
            raise ValueError(
                "the field 'literal' received an unrecognised value'")


class PyNestExpr(Node):

    def __init__(self, *, open_paren: '(PyOpenParen | None)'=None, expr:
        'PyExpr', close_paren: '(PyCloseParen | None)'=None) ->None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren
        self.expr: PyExpr = expr
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren


class PyNamedExpr(Node):

    def __init__(self, *, name: '(PyIdent | str)') ->None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name


class PyAttrExpr(Node):

    def __init__(self, *, expr: 'PyExpr', dot: '(PyDot | None)'=None, name:
        '(PyIdent | str)') ->None:
        self.expr: PyExpr = expr
        if dot is None:
            self.dot: PyDot = PyDot()
        else:
            self.dot: PyDot = dot
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name


class PySubscriptExpr(Node):

    def __init__(self, *, expr: 'PyExpr', open_bracket:
        '(PyOpenBracket | None)'=None, slices:
        '(None | list[PyExpr | PySlice | tuple[PyExpr | PySlice, PyComma | None]])'
        =None, close_bracket: '(PyCloseBracket | None)'=None) ->None:
        self.expr: PyExpr = expr
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket
        if slices is None:
            self.slices: list[tuple[PyExpr | PySlice, PyComma | None]] = list()
        else:
            new_slices = list()
            for slices_element in slices:
                if is_py_expr(slices_element) or isinstance(slices_element,
                    PySlice):
                    new_slices_element = slices_element, None
                else:
                    assert(isinstance(slices_element, tuple))
                    slices_element_0 = slices_element[0]
                    new_slices_element_0 = slices_element_0
                    slices_element_1 = slices_element[1]
                    if isinstance(slices_element_1, PyComma):
                        new_slices_element_1 = slices_element_1
                    elif slices_element_1 is None:
                        new_slices_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'slices' received an unrecognised value'"
                            )
                    new_slices_element = (new_slices_element_0,
                        new_slices_element_1)
                new_slices.append(new_slices_element)
            self.slices: list[tuple[PyExpr | PySlice, PyComma | None]
                ] = new_slices
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket


class PyStarredExpr(Node):

    def __init__(self, *, asterisk: '(PyAsterisk | None)'=None, expr: 'PyExpr'
        ) ->None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk
        self.expr: PyExpr = expr


class PyListExpr(Node):

    def __init__(self, *, open_bracket: '(PyOpenBracket | None)'=None,
        elements: '(None | list[PyExpr | tuple[PyExpr, PyComma | None]])'=
        None, close_bracket: '(PyCloseBracket | None)'=None) ->None:
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket
        if elements is None:
            self.elements: list[tuple[PyExpr, PyComma | None]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                if is_py_expr(elements_element):
                    new_elements_element = elements_element, None
                else:
                    assert(isinstance(elements_element, tuple))
                    elements_element_0 = elements_element[0]
                    new_elements_element_0 = elements_element_0
                    elements_element_1 = elements_element[1]
                    if isinstance(elements_element_1, PyComma):
                        new_elements_element_1 = elements_element_1
                    elif elements_element_1 is None:
                        new_elements_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'elements' received an unrecognised value'"
                            )
                    new_elements_element = (new_elements_element_0,
                        new_elements_element_1)
                new_elements.append(new_elements_element)
            self.elements: list[tuple[PyExpr, PyComma | None]] = new_elements
        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket


class PyTupleExpr(Node):

    def __init__(self, *, open_paren: '(PyOpenParen | None)'=None, elements:
        '(None | list[PyExpr | tuple[PyExpr, PyComma | None]])'=None,
        close_paren: '(PyCloseParen | None)'=None) ->None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren
        if elements is None:
            self.elements: list[tuple[PyExpr, PyComma | None]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                if is_py_expr(elements_element):
                    new_elements_element = elements_element, None
                else:
                    assert(isinstance(elements_element, tuple))
                    elements_element_0 = elements_element[0]
                    new_elements_element_0 = elements_element_0
                    elements_element_1 = elements_element[1]
                    if isinstance(elements_element_1, PyComma):
                        new_elements_element_1 = elements_element_1
                    elif elements_element_1 is None:
                        new_elements_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'elements' received an unrecognised value'"
                            )
                    new_elements_element = (new_elements_element_0,
                        new_elements_element_1)
                new_elements.append(new_elements_element)
            self.elements: list[tuple[PyExpr, PyComma | None]] = new_elements
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren


PyArg: TypeAlias = 'PyPosArg | PyKeywordArg'


def is_py_arg(value: Any) ->TypeGuard[PyArg]:
    return is_py_pos_arg(value) or isinstance(value, PyKeywordArg)


PyPosArg: TypeAlias = 'PyExpr'


def is_py_pos_arg(value: Any) ->TypeGuard[PyPosArg]:
    return is_py_expr(value)


class PyKeywordArg(Node):

    def __init__(self, *, name: '(PyIdent | str)', equals:
        '(PyEquals | None)'=None, expr: 'PyExpr') ->None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name
        if equals is None:
            self.equals: PyEquals = PyEquals()
        else:
            self.equals: PyEquals = equals
        self.expr: PyExpr = expr


class PyCallExpr(Node):

    def __init__(self, *, operator: 'PyExpr', open_paren:
        '(PyOpenParen | None)'=None, args:
        '(None | list[PyArg | tuple[PyArg, PyComma | None]])'=None,
        close_paren: '(PyCloseParen | None)'=None) ->None:
        self.operator: PyExpr = operator
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren
        if args is None:
            self.args: list[tuple[PyArg, PyComma | None]] = list()
        else:
            new_args = list()
            for args_element in args:
                if is_py_arg(args_element):
                    new_args_element = args_element, None
                else:
                    assert(isinstance(args_element, tuple))
                    args_element_0 = args_element[0]
                    new_args_element_0 = args_element_0
                    args_element_1 = args_element[1]
                    if isinstance(args_element_1, PyComma):
                        new_args_element_1 = args_element_1
                    elif args_element_1 is None:
                        new_args_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'args' received an unrecognised value'")
                    new_args_element = new_args_element_0, new_args_element_1
                new_args.append(new_args_element)
            self.args: list[tuple[PyArg, PyComma | None]] = new_args
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren


class PyPrefixOp(Token):

    def __init__(self, value: (str | None)=None, span: (Span | None)=None):
        super().__init__(span=span)
        self.value = value


class PyPrefixExpr(Node):

    def __init__(self, *, prefix_op: '(PyPrefixOp | str)', expr: 'PyExpr'
        ) ->None:
        if isinstance(prefix_op, str):
            self.prefix_op: PyPrefixOp = PyPrefixOp(prefix_op)
        else:
            self.prefix_op: PyPrefixOp = prefix_op
        self.expr: PyExpr = expr


class PyInfixOp(Token):

    def __init__(self, value: (str | None)=None, span: (Span | None)=None):
        super().__init__(span=span)
        self.value = value


class PyInfixExpr(Node):

    def __init__(self, *, left: 'PyExpr', infix_op: '(PyInfixOp | str)',
        right: 'PyExpr') ->None:
        self.left: PyExpr = left
        if isinstance(infix_op, str):
            self.infix_op: PyInfixOp = PyInfixOp(infix_op)
        else:
            self.infix_op: PyInfixOp = infix_op
        self.right: PyExpr = right


PyStmt: TypeAlias = (
    'PyRetStmt | PyExprStmt | PyAssignStmt | PyIfStmt | PyRaiseStmt | PyDeleteStmt | PyTypeAliasStmt'
    )


def is_py_stmt(value: Any) ->TypeGuard[PyStmt]:
    return (((((isinstance(value, PyRetStmt) or isinstance(value,
        PyExprStmt)) or isinstance(value, PyAssignStmt)) or isinstance(
        value, PyIfStmt)) or isinstance(value, PyRaiseStmt)) or isinstance(
        value, PyDeleteStmt)) or isinstance(value, PyTypeAliasStmt)


class PyRetStmt(Node):

    def __init__(self, *, return_keyword: '(PyReturnKeyword | None)'=None,
        expr: 'PyExpr') ->None:
        if return_keyword is None:
            self.return_keyword: PyReturnKeyword = PyReturnKeyword()
        else:
            self.return_keyword: PyReturnKeyword = return_keyword
        self.expr: PyExpr = expr


class PyExprStmt(Node):

    def __init__(self, *, expr: 'PyExpr') ->None:
        self.expr: PyExpr = expr


class PyAssignStmt(Node):

    def __init__(self, *, pattern: 'PyPattern', annotation:
        '(tuple[PyColon | None, PyExpr] | None)'=None, equals:
        '(PyEquals | None)'=None, expr: 'PyExpr') ->None:
        self.pattern: PyPattern = pattern
        if isinstance(annotation, tuple):
            assert(isinstance(annotation, tuple))
            annotation_0 = annotation[0]
            if annotation_0 is None:
                new_annotation_0 = PyColon()
            else:
                new_annotation_0 = annotation_0
            annotation_1 = annotation[1]
            new_annotation_1 = annotation_1
            self.annotation: tuple[PyColon, PyExpr] | None = (new_annotation_0,
                new_annotation_1)
        elif annotation is None:
            self.annotation: tuple[PyColon, PyExpr] | None = None
        else:
            raise ValueError(
                "the field 'annotation' received an unrecognised value'")
        if equals is None:
            self.equals: PyEquals = PyEquals()
        else:
            self.equals: PyEquals = equals
        self.expr: PyExpr = expr


class PyIfCase(Node):

    def __init__(self, *, if_keyword: '(PyIfKeyword | None)'=None, test:
        'PyExpr', colon: '(PyColon | None)'=None, body:
        '(PyStmt | (None | list[PyStmt]))'=None) ->None:
        if if_keyword is None:
            self.if_keyword: PyIfKeyword = PyIfKeyword()
        else:
            self.if_keyword: PyIfKeyword = if_keyword
        self.test: PyExpr = test
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None or isinstance(body, list):
            if body is None:
                self.body: PyStmt | list[PyStmt] = list()
            else:
                new_body = list()
                for body_element in body:
                    new_body_element = body_element
                    new_body.append(new_body_element)
                self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'"
                )


class PyElifCase(Node):

    def __init__(self, *, elif_keyword: '(PyElifKeyword | None)'=None, test:
        'PyExpr', colon: '(PyColon | None)'=None, body:
        '(PyStmt | (None | list[PyStmt]))'=None) ->None:
        if elif_keyword is None:
            self.elif_keyword: PyElifKeyword = PyElifKeyword()
        else:
            self.elif_keyword: PyElifKeyword = elif_keyword
        self.test: PyExpr = test
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None or isinstance(body, list):
            if body is None:
                self.body: PyStmt | list[PyStmt] = list()
            else:
                new_body = list()
                for body_element in body:
                    new_body_element = body_element
                    new_body.append(new_body_element)
                self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'"
                )


class PyElseCase(Node):

    def __init__(self, *, else_keyword: '(PyElseKeyword | None)'=None,
        colon: '(PyColon | None)'=None, body:
        '(PyStmt | (None | list[PyStmt]))'=None) ->None:
        if else_keyword is None:
            self.else_keyword: PyElseKeyword = PyElseKeyword()
        else:
            self.else_keyword: PyElseKeyword = else_keyword
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None or isinstance(body, list):
            if body is None:
                self.body: PyStmt | list[PyStmt] = list()
            else:
                new_body = list()
                for body_element in body:
                    new_body_element = body_element
                    new_body.append(new_body_element)
                self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'"
                )


class PyIfStmt(Node):

    def __init__(self, *, first: 'PyIfCase', alternatives:
        '(None | list[PyElifCase])'=None, last: '(PyElseCase | None)'=None
        ) ->None:
        self.first: PyIfCase = first
        if alternatives is None:
            self.alternatives: list[PyElifCase] = list()
        else:
            new_alternatives = list()
            for alternatives_element in alternatives:
                new_alternatives_element = alternatives_element
                new_alternatives.append(new_alternatives_element)
            self.alternatives: list[PyElifCase] = new_alternatives
        self.last: PyElseCase | None = last


class PyDeleteStmt(Node):

    def __init__(self, *, del_keyword: '(PyDelKeyword | None)'=None,
        pattern: 'PyPattern') ->None:
        if del_keyword is None:
            self.del_keyword: PyDelKeyword = PyDelKeyword()
        else:
            self.del_keyword: PyDelKeyword = del_keyword
        self.pattern: PyPattern = pattern


class PyRaiseStmt(Node):

    def __init__(self, *, raise_keyword: '(PyRaiseKeyword | None)'=None,
        expr: 'PyExpr', cause:
        '(tuple[PyFormKeyword | None, PyExpr] | None)'=None) ->None:
        if raise_keyword is None:
            self.raise_keyword: PyRaiseKeyword = PyRaiseKeyword()
        else:
            self.raise_keyword: PyRaiseKeyword = raise_keyword
        self.expr: PyExpr = expr
        if isinstance(cause, tuple):
            assert(isinstance(cause, tuple))
            cause_0 = cause[0]
            if cause_0 is None:
                new_cause_0 = PyFormKeyword()
            else:
                new_cause_0 = cause_0
            cause_1 = cause[1]
            new_cause_1 = cause_1
            self.cause: tuple[PyFormKeyword, PyExpr] | None = (new_cause_0,
                new_cause_1)
        elif cause is None:
            self.cause: tuple[PyFormKeyword, PyExpr] | None = None
        else:
            raise ValueError(
                "the field 'cause' received an unrecognised value'")


class PyTypeAliasStmt(Node):

    def __init__(self, *, type_keyword: '(PyTypeKeyword | None)'=None, name:
        '(PyIdent | str)', type_params:
        """(tuple[PyOpenBracket | None, None | list[PyExpr | tuple[PyExpr, PyComma |
    None]], PyCloseBracket | None] | None)"""
        =None, equals: '(PyEquals | None)'=None, expr: 'PyExpr') ->None:
        if type_keyword is None:
            self.type_keyword: PyTypeKeyword = PyTypeKeyword()
        else:
            self.type_keyword: PyTypeKeyword = type_keyword
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name
        if isinstance(type_params, tuple):
            assert(isinstance(type_params, tuple))
            type_params_0 = type_params[0]
            if type_params_0 is None:
                new_type_params_0 = PyOpenBracket()
            else:
                new_type_params_0 = type_params_0
            type_params_1 = type_params[1]
            if type_params_1 is None:
                new_type_params_1 = list()
            else:
                new_type_params_1 = list()
                for type_params_1_element in type_params_1:
                    if is_py_expr(type_params_1_element):
                        new_type_params_1_element = type_params_1_element, None
                    else:
                        assert(isinstance(type_params_1_element, tuple))
                        type_params_1_element_0 = type_params_1_element[0]
                        new_type_params_1_element_0 = type_params_1_element_0
                        type_params_1_element_1 = type_params_1_element[1]
                        if isinstance(type_params_1_element_1, PyComma):
                            new_type_params_1_element_1 = (
                                type_params_1_element_1)
                        elif type_params_1_element_1 is None:
                            new_type_params_1_element_1 = None
                        else:
                            raise ValueError(
                                "the field 'type_params' received an unrecognised value'"
                                )
                        new_type_params_1_element = (
                            new_type_params_1_element_0,
                            new_type_params_1_element_1)
                    new_type_params_1.append(new_type_params_1_element)
                new_type_params_1 = new_type_params_1
            type_params_2 = type_params[2]
            if type_params_2 is None:
                new_type_params_2 = PyCloseBracket()
            else:
                new_type_params_2 = type_params_2
            self.type_params: tuple[PyOpenBracket, list[tuple[PyExpr, 
                PyComma | None]], PyCloseBracket] | None = (new_type_params_0,
                new_type_params_1, new_type_params_2)
        elif type_params is None:
            self.type_params: tuple[PyOpenBracket, list[tuple[PyExpr, 
                PyComma | None]], PyCloseBracket] | None = None
        else:
            raise ValueError(
                "the field 'type_params' received an unrecognised value'")
        if equals is None:
            self.equals: PyEquals = PyEquals()
        else:
            self.equals: PyEquals = equals
        self.expr: PyExpr = expr


class PyClassDef(Node):

    def __init__(self, *, class_keyword: '(PyClassKeyword | None)'=None,
        name: '(PyIdent | str)', open_paren: '(PyOpenParen | None)'=None,
        expr: 'PyExpr', close_paren: '(PyCloseParen | None)'=None, colon:
        '(PyColon | None)'=None, body: '(PyStmt | (None | list[PyStmt]))'=None
        ) ->None:
        if class_keyword is None:
            self.class_keyword: PyClassKeyword = PyClassKeyword()
        else:
            self.class_keyword: PyClassKeyword = class_keyword
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren
        self.expr: PyExpr = expr
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None or isinstance(body, list):
            if body is None:
                self.body: PyStmt | list[PyStmt] = list()
            else:
                new_body = list()
                for body_element in body:
                    new_body_element = body_element
                    new_body.append(new_body_element)
                self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'"
                )


PyParam: TypeAlias = 'PyPosParam | PyRestPosParam | PyRestKeywordParam'


def is_py_param(value: Any) ->TypeGuard[PyParam]:
    return (isinstance(value, PyPosParam) or isinstance(value, PyRestPosParam)
        ) or isinstance(value, PyRestKeywordParam)


class PyPosParam(Node):

    def __init__(self, *, name: '(PyIdent | str)', annotation:
        '(tuple[PyColon | None, PyExpr] | None)'=None, default:
        '(tuple[PyEquals | None, PyExpr] | None)'=None) ->None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name
        if isinstance(annotation, tuple):
            assert(isinstance(annotation, tuple))
            annotation_0 = annotation[0]
            if annotation_0 is None:
                new_annotation_0 = PyColon()
            else:
                new_annotation_0 = annotation_0
            annotation_1 = annotation[1]
            new_annotation_1 = annotation_1
            self.annotation: tuple[PyColon, PyExpr] | None = (new_annotation_0,
                new_annotation_1)
        elif annotation is None:
            self.annotation: tuple[PyColon, PyExpr] | None = None
        else:
            raise ValueError(
                "the field 'annotation' received an unrecognised value'")
        if isinstance(default, tuple):
            assert(isinstance(default, tuple))
            default_0 = default[0]
            if default_0 is None:
                new_default_0 = PyEquals()
            else:
                new_default_0 = default_0
            default_1 = default[1]
            new_default_1 = default_1
            self.default: tuple[PyEquals, PyExpr] | None = (new_default_0,
                new_default_1)
        elif default is None:
            self.default: tuple[PyEquals, PyExpr] | None = None
        else:
            raise ValueError(
                "the field 'default' received an unrecognised value'")


class PyRestPosParam(Node):

    def __init__(self, *, asterisk: '(PyAsterisk | None)'=None, name:
        '(PyIdent | str)') ->None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name


class PyRestKeywordParam(Node):

    def __init__(self, *, asterisk_asterisk: '(PyAsteriskAsterisk | None)'=
        None, name: '(PyIdent | str)') ->None:
        if asterisk_asterisk is None:
            self.asterisk_asterisk: PyAsteriskAsterisk = PyAsteriskAsterisk()
        else:
            self.asterisk_asterisk: PyAsteriskAsterisk = asterisk_asterisk
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name


class PyFuncDef(Node):

    def __init__(self, *, async_keyword: '(PyAsyncKeyword | None)'=None,
        def_keyword: '(PyDefKeyword | None)'=None, name: '(PyIdent | str)',
        open_paren: '(PyOpenParen | None)'=None, params:
        '(None | list[PyParam | tuple[PyParam, PyComma | None]])'=None,
        close_paren: '(PyCloseParen | None)'=None, return_type:
        '(tuple[PyHyphenGreaterThan | None, PyExpr] | None)'=None, colon:
        '(PyColon | None)'=None, body: '(PyStmt | (None | list[PyStmt]))'=None
        ) ->None:
        if isinstance(async_keyword, PyAsyncKeyword):
            self.async_keyword: PyAsyncKeyword | None = async_keyword
        elif async_keyword is None:
            self.async_keyword: PyAsyncKeyword | None = None
        else:
            raise ValueError(
                "the field 'async_keyword' received an unrecognised value'")
        if def_keyword is None:
            self.def_keyword: PyDefKeyword = PyDefKeyword()
        else:
            self.def_keyword: PyDefKeyword = def_keyword
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren
        if params is None:
            self.params: list[tuple[PyParam, PyComma | None]] = list()
        else:
            new_params = list()
            for params_element in params:
                if is_py_param(params_element):
                    new_params_element = params_element, None
                else:
                    assert(isinstance(params_element, tuple))
                    params_element_0 = params_element[0]
                    new_params_element_0 = params_element_0
                    params_element_1 = params_element[1]
                    if isinstance(params_element_1, PyComma):
                        new_params_element_1 = params_element_1
                    elif params_element_1 is None:
                        new_params_element_1 = None
                    else:
                        raise ValueError(
                            "the field 'params' received an unrecognised value'"
                            )
                    new_params_element = (new_params_element_0,
                        new_params_element_1)
                new_params.append(new_params_element)
            self.params: list[tuple[PyParam, PyComma | None]] = new_params
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren
        if isinstance(return_type, tuple):
            assert(isinstance(return_type, tuple))
            return_type_0 = return_type[0]
            if return_type_0 is None:
                new_return_type_0 = PyHyphenGreaterThan()
            else:
                new_return_type_0 = return_type_0
            return_type_1 = return_type[1]
            new_return_type_1 = return_type_1
            self.return_type: tuple[PyHyphenGreaterThan, PyExpr] | None = (
                new_return_type_0, new_return_type_1)
        elif return_type is None:
            self.return_type: tuple[PyHyphenGreaterThan, PyExpr] | None = None
        else:
            raise ValueError(
                "the field 'return_type' received an unrecognised value'")
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon
        if is_py_stmt(body):
            self.body: PyStmt | list[PyStmt] = body
        elif body is None or isinstance(body, list):
            if body is None:
                self.body: PyStmt | list[PyStmt] = list()
            else:
                new_body = list()
                for body_element in body:
                    new_body_element = body_element
                    new_body.append(new_body_element)
                self.body: PyStmt | list[PyStmt] = new_body
        else:
            raise ValueError("the field 'body' received an unrecognised value'"
                )


