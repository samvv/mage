
from typing import TypeAlias, TypeGuard, Any, Callable

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

class _BaseToken:

    def __init__(self, span: Span | None = None) -> None:
        self.span = span

class _BaseNode:

    def __init__(self) -> None:
        pass

class PyCarriageReturnLineFeed(_BaseToken):
    pass


class PyLineFeed(_BaseToken):
    pass


class PySemicolon(_BaseToken):
    pass


class PyZero(_BaseToken):
    pass


class PyDot(_BaseToken):
    pass


class PyDoubleQuote(_BaseToken):
    pass


class PySingleQuote(_BaseToken):
    pass


class PyColon(_BaseToken):
    pass


class PyOpenBracket(_BaseToken):
    pass


class PyComma(_BaseToken):
    pass


class PyCloseBracket(_BaseToken):
    pass


class PyAsterisk(_BaseToken):
    pass


class PyOpenParen(_BaseToken):
    pass


class PyCloseParen(_BaseToken):
    pass


class PyEquals(_BaseToken):
    pass


class PyNotKeyword(_BaseToken):
    pass


class PyPlus(_BaseToken):
    pass


class PyHyphen(_BaseToken):
    pass


class PyTilde(_BaseToken):
    pass


class PySlash(_BaseToken):
    pass


class PySlashSlash(_BaseToken):
    pass


class PyPercenct(_BaseToken):
    pass


class PyLessThanLessThan(_BaseToken):
    pass


class PyGreaterThanGreaterThan(_BaseToken):
    pass


class PyVerticalBar(_BaseToken):
    pass


class PyCaret(_BaseToken):
    pass


class PyAmpersand(_BaseToken):
    pass


class PyAtSign(_BaseToken):
    pass


class PyOrKeyword(_BaseToken):
    pass


class PyAndKeyword(_BaseToken):
    pass


class PyEqualsEquals(_BaseToken):
    pass


class PyExclamationMarkEquals(_BaseToken):
    pass


class PyLessThan(_BaseToken):
    pass


class PyLessThanEquals(_BaseToken):
    pass


class PyGreaterThan(_BaseToken):
    pass


class PyGreaterThanEquals(_BaseToken):
    pass


class PyIsKeyword(_BaseToken):
    pass


class PyInKeyword(_BaseToken):
    pass


class PyReturnKeyword(_BaseToken):
    pass


class PyPassKeyword(_BaseToken):
    pass


class PyIfKeyword(_BaseToken):
    pass


class PyElifKeyword(_BaseToken):
    pass


class PyElseKeyword(_BaseToken):
    pass


class PyDelKeyword(_BaseToken):
    pass


class PyRaiseKeyword(_BaseToken):
    pass


class PyFormKeyword(_BaseToken):
    pass


class PyForKeyword(_BaseToken):
    pass


class PyWhileKeyword(_BaseToken):
    pass


class PyBreakKeyword(_BaseToken):
    pass


class PyContinueKeyword(_BaseToken):
    pass


class PyTypeKeyword(_BaseToken):
    pass


class PyExceptKeyword(_BaseToken):
    pass


class PyAsKeyword(_BaseToken):
    pass


class PyTryKeyword(_BaseToken):
    pass


class PyFinallyKeyword(_BaseToken):
    pass


class PyClassKeyword(_BaseToken):
    pass


class PyAsteriskAsterisk(_BaseToken):
    pass


class PyAsyncKeyword(_BaseToken):
    pass


class PyDefKeyword(_BaseToken):
    pass


class PyHyphenGreaterThan(_BaseToken):
    pass


class PyIdent(_BaseToken):
    def __init__(self, value: str | None = None, span: Span | None = None):
        super().__init__(span=span)
        self.value = value



class PyInteger(_BaseToken):
    def __init__(self, value: int | None = None, span: Span | None = None):
        super().__init__(span=span)
        self.value = value



class PyFloat(_BaseToken):
    def __init__(self, value: float | None = None, span: Span | None = None):
        super().__init__(span=span)
        self.value = value



class PyString(_BaseToken):
    def __init__(self, value: str | None = None, span: Span | None = None):
        super().__init__(span=span)
        self.value = value



class PySlice(_BaseNode):
    def __init__(self, *, lower: 'PyExpr', colon: 'PyColon | None' = None, upper: 'PyExpr') -> None:
        self.lower: PyExpr = lower
        if colon is None:
            self.colon: PyColon = PyColon()
        else:
            self.colon: PyColon = colon

        self.upper: PyExpr = upper



PyPattern: TypeAlias = 'PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern'

def is_py_pattern(value: Any) -> TypeGuard[PyPattern]:
    return isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern)


class PyNamedPattern(_BaseNode):
    def __init__(self, *, name: 'PyIdent | str') -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name




class PyAttrPattern(_BaseNode):
    def __init__(self, *, pattern: 'PyPattern', dot: 'PyDot | None' = None, name: 'PyIdent | str') -> None:
        self.pattern: PyPattern = pattern
        if dot is None:
            self.dot: PyDot = PyDot()
        else:
            self.dot: PyDot = dot

        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name




class PySubscriptPattern(_BaseNode):
    def __init__(self, *, pattern: 'PyPattern', open_bracket: 'PyOpenBracket | None' = None, slices: 'None | list[tuple[(PyPattern | PySlice, PyComma | None)]]' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.pattern: PyPattern = pattern
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket

        if slices is None:
            self.slices: list[tuple[(PyPattern | PySlice, PyComma | None)]] = list()
        else:
            new_slices = list()
            for slices_element in slices:
                assert(isinstance(slices_element, tuple))
                slices_element_0 = slices_element[0]
                new_slices_element_0 = slices_element_0
                slices_element_1 = slices_element[1]
                if isinstance(slices_element_1, PyComma):
                    new_slices_element_1 = slices_element_1
                elif slices_element_1 is None:
                    new_slices_element_1 = None
                else:
                    raise ValueError("the field 'slices' received an unrecognised value'")

                new_slices_element = (new_slices_element_0, new_slices_element_1)
                new_slices.append(new_slices_element)

            self.slices: list[tuple[(PyPattern | PySlice, PyComma | None)]] = new_slices

        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket




class PyStarredPattern(_BaseNode):
    def __init__(self, *, asterisk: 'PyAsterisk | None' = None, expr: 'PyExpr') -> None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk

        self.expr: PyExpr = expr



class PyListPattern(_BaseNode):
    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'None | list[tuple[(PyPattern, PyComma | None)]]' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket

        if elements is None:
            self.elements: list[tuple[(PyPattern, PyComma | None)]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                assert(isinstance(elements_element, tuple))
                elements_element_0 = elements_element[0]
                new_elements_element_0 = elements_element_0
                elements_element_1 = elements_element[1]
                if isinstance(elements_element_1, PyComma):
                    new_elements_element_1 = elements_element_1
                elif elements_element_1 is None:
                    new_elements_element_1 = None
                else:
                    raise ValueError("the field 'elements' received an unrecognised value'")

                new_elements_element = (new_elements_element_0, new_elements_element_1)
                new_elements.append(new_elements_element)

            self.elements: list[tuple[(PyPattern, PyComma | None)]] = new_elements

        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket




class PyTuplePattern(_BaseNode):
    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'None | list[tuple[(PyPattern, PyComma | None)]]' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren

        if elements is None:
            self.elements: list[tuple[(PyPattern, PyComma | None)]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                assert(isinstance(elements_element, tuple))
                elements_element_0 = elements_element[0]
                new_elements_element_0 = elements_element_0
                elements_element_1 = elements_element[1]
                if isinstance(elements_element_1, PyComma):
                    new_elements_element_1 = elements_element_1
                elif elements_element_1 is None:
                    new_elements_element_1 = None
                else:
                    raise ValueError("the field 'elements' received an unrecognised value'")

                new_elements_element = (new_elements_element_0, new_elements_element_1)
                new_elements.append(new_elements_element)

            self.elements: list[tuple[(PyPattern, PyComma | None)]] = new_elements

        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren




PyExpr: TypeAlias = 'PyAttrExpr | PyCallExpr | PyConstExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr'

def is_py_expr(value: Any) -> TypeGuard[PyExpr]:
    return isinstance(value, PyAttrExpr) or isinstance(value, PyCallExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyListExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyTupleExpr)


class PyConstExpr(_BaseNode):
    def __init__(self, *, literal: 'PyString | str | PyFloat | float | PyInteger | int') -> None:
        if isinstance(literal, PyString) or isinstance(literal, str):
            if isinstance(literal, str):
                self.literal: PyString | PyFloat | PyInteger = PyString(literal)
            else:
                self.literal: PyString | PyFloat | PyInteger = literal

        elif isinstance(literal, PyFloat) or isinstance(literal, float):
            if isinstance(literal, float):
                self.literal: PyString | PyFloat | PyInteger = PyFloat(literal)
            else:
                self.literal: PyString | PyFloat | PyInteger = literal

        elif isinstance(literal, PyInteger) or isinstance(literal, int):
            if isinstance(literal, int):
                self.literal: PyString | PyFloat | PyInteger = PyInteger(literal)
            else:
                self.literal: PyString | PyFloat | PyInteger = literal

        else:
            raise ValueError("the field 'literal' received an unrecognised value'")




class PyNestExpr(_BaseNode):
    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, expr: 'PyExpr', close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren

        self.expr: PyExpr = expr
        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren




class PyNamedExpr(_BaseNode):
    def __init__(self, *, name: 'PyIdent | str') -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name




class PyAttrExpr(_BaseNode):
    def __init__(self, *, expr: 'PyExpr', dot: 'PyDot | None' = None, name: 'PyIdent | str') -> None:
        self.expr: PyExpr = expr
        if dot is None:
            self.dot: PyDot = PyDot()
        else:
            self.dot: PyDot = dot

        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name




class PySubscriptExpr(_BaseNode):
    def __init__(self, *, expr: 'PyExpr', open_bracket: 'PyOpenBracket | None' = None, slices: 'None | list[tuple[(PyExpr | PySlice, PyComma | None)]]' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.expr: PyExpr = expr
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket

        if slices is None:
            self.slices: list[tuple[(PyExpr | PySlice, PyComma | None)]] = list()
        else:
            new_slices = list()
            for slices_element in slices:
                assert(isinstance(slices_element, tuple))
                slices_element_0 = slices_element[0]
                new_slices_element_0 = slices_element_0
                slices_element_1 = slices_element[1]
                if isinstance(slices_element_1, PyComma):
                    new_slices_element_1 = slices_element_1
                elif slices_element_1 is None:
                    new_slices_element_1 = None
                else:
                    raise ValueError("the field 'slices' received an unrecognised value'")

                new_slices_element = (new_slices_element_0, new_slices_element_1)
                new_slices.append(new_slices_element)

            self.slices: list[tuple[(PyExpr | PySlice, PyComma | None)]] = new_slices

        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket




class PyStarredExpr(_BaseNode):
    def __init__(self, *, asterisk: 'PyAsterisk | None' = None, expr: 'PyExpr') -> None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk

        self.expr: PyExpr = expr



class PyListExpr(_BaseNode):
    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'None | list[tuple[(PyExpr, PyComma | None)]]' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        if open_bracket is None:
            self.open_bracket: PyOpenBracket = PyOpenBracket()
        else:
            self.open_bracket: PyOpenBracket = open_bracket

        if elements is None:
            self.elements: list[tuple[(PyExpr, PyComma | None)]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                assert(isinstance(elements_element, tuple))
                elements_element_0 = elements_element[0]
                new_elements_element_0 = elements_element_0
                elements_element_1 = elements_element[1]
                if isinstance(elements_element_1, PyComma):
                    new_elements_element_1 = elements_element_1
                elif elements_element_1 is None:
                    new_elements_element_1 = None
                else:
                    raise ValueError("the field 'elements' received an unrecognised value'")

                new_elements_element = (new_elements_element_0, new_elements_element_1)
                new_elements.append(new_elements_element)

            self.elements: list[tuple[(PyExpr, PyComma | None)]] = new_elements

        if close_bracket is None:
            self.close_bracket: PyCloseBracket = PyCloseBracket()
        else:
            self.close_bracket: PyCloseBracket = close_bracket




class PyTupleExpr(_BaseNode):
    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'None | list[tuple[(PyExpr, PyComma | None)]]' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren

        if elements is None:
            self.elements: list[tuple[(PyExpr, PyComma | None)]] = list()
        else:
            new_elements = list()
            for elements_element in elements:
                assert(isinstance(elements_element, tuple))
                elements_element_0 = elements_element[0]
                new_elements_element_0 = elements_element_0
                elements_element_1 = elements_element[1]
                if isinstance(elements_element_1, PyComma):
                    new_elements_element_1 = elements_element_1
                elif elements_element_1 is None:
                    new_elements_element_1 = None
                else:
                    raise ValueError("the field 'elements' received an unrecognised value'")

                new_elements_element = (new_elements_element_0, new_elements_element_1)
                new_elements.append(new_elements_element)

            self.elements: list[tuple[(PyExpr, PyComma | None)]] = new_elements

        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren




PyArg: TypeAlias = 'PyPosArg | PyKeywordArg'

def is_py_arg(value: Any) -> TypeGuard[PyArg]:
    return is_py_pos_arg(value) or isinstance(value, PyKeywordArg)


PyPosArg: TypeAlias = 'PyExpr'

def is_py_pos_arg(value: Any) -> TypeGuard[PyPosArg]:
    return is_py_expr(value)


class PyKeywordArg(_BaseNode):
    def __init__(self, *, name: 'PyIdent | str', equals: 'PyEquals | None' = None, expr: 'PyExpr') -> None:
        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name

        if equals is None:
            self.equals: PyEquals = PyEquals()
        else:
            self.equals: PyEquals = equals

        self.expr: PyExpr = expr



class PyCallExpr(_BaseNode):
    def __init__(self, *, operator: 'PyExpr', open_paren: 'PyOpenParen | None' = None, args: 'None | list[tuple[(PyArg, PyComma | None)]]' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.operator: PyExpr = operator
        if open_paren is None:
            self.open_paren: PyOpenParen = PyOpenParen()
        else:
            self.open_paren: PyOpenParen = open_paren

        if args is None:
            self.args: list[tuple[(PyArg, PyComma | None)]] = list()
        else:
            new_args = list()
            for args_element in args:
                assert(isinstance(args_element, tuple))
                args_element_0 = args_element[0]
                new_args_element_0 = args_element_0
                args_element_1 = args_element[1]
                if isinstance(args_element_1, PyComma):
                    new_args_element_1 = args_element_1
                elif args_element_1 is None:
                    new_args_element_1 = None
                else:
                    raise ValueError("the field 'args' received an unrecognised value'")

                new_args_element = (new_args_element_0, new_args_element_1)
                new_args.append(new_args_element)

            self.args: list[tuple[(PyArg, PyComma | None)]] = new_args

        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren




class PyPrefixOp(_BaseToken):
    def __init__(self, value: str | None = None, span: Span | None = None):
        super().__init__(span=span)
        self.value = value



class PyPrefixExpr(_BaseNode):
    def __init__(self, *, prefix_op: 'PyPrefixOp | str', expr: 'PyExpr') -> None:
        if isinstance(prefix_op, str):
            self.prefix_op: PyPrefixOp = PyPrefixOp(prefix_op)
        else:
            self.prefix_op: PyPrefixOp = prefix_op

        self.expr: PyExpr = expr



class PyInfixOp(_BaseToken):
    def __init__(self, value: str | None = None, span: Span | None = None):
        super().__init__(span=span)
        self.value = value



class PyInfixExpr(_BaseNode):
    def __init__(self, *, left: 'PyExpr', op: 'PyInfixOp | str', right: 'PyExpr') -> None:
        self.left: PyExpr = left
        if isinstance(op, str):
            self.op: PyInfixOp = PyInfixOp(op)
        else:
            self.op: PyInfixOp = op

        self.right: PyExpr = right



PyStmt: TypeAlias = 'PyAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyIfStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt'

def is_py_stmt(value: Any) -> TypeGuard[PyStmt]:
    return isinstance(value, PyAssignStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyClassDef) or isinstance(value, PyContinueStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyForStmt) or isinstance(value, PyFuncDef) or isinstance(value, PyIfStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyTryStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyWhileStmt)


class PyRetStmt(_BaseNode):
    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> None:
        if return_keyword is None:
            self.return_keyword: PyReturnKeyword = PyReturnKeyword()
        else:
            self.return_keyword: PyReturnKeyword = return_keyword

        self.expr: PyExpr | None = expr



class PyExprStmt(_BaseNode):
    def __init__(self, *, expr: 'PyExpr') -> None:
        self.expr: PyExpr = expr



class PyAssignStmt(_BaseNode):
    def __init__(self, *, pattern: 'PyPattern', annotation: 'PyExpr | tuple[(PyColon | None, PyExpr)] | None' = None, equals: 'PyEquals | None' = None, expr: 'PyExpr') -> None:
        self.pattern: PyPattern = pattern
        if is_py_expr(annotation) or isinstance(annotation, tuple):
            if is_py_expr(annotation):
                self.annotation: tuple[(PyColon, PyExpr)] | None = (PyColon(), annotation)
            else:
                assert(isinstance(annotation, tuple))
                annotation_0 = annotation[0]
                if annotation_0 is None:
                    new_annotation_0 = PyColon()
                else:
                    new_annotation_0 = annotation_0

                annotation_1 = annotation[1]
                new_annotation_1 = annotation_1
                self.annotation: tuple[(PyColon, PyExpr)] | None = (new_annotation_0, new_annotation_1)

        elif annotation is None:
            self.annotation: tuple[(PyColon, PyExpr)] | None = None
        else:
            raise ValueError("the field 'annotation' received an unrecognised value'")

        if equals is None:
            self.equals: PyEquals = PyEquals()
        else:
            self.equals: PyEquals = equals

        self.expr: PyExpr = expr



class PyPassStmt(_BaseNode):
    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None) -> None:
        if pass_keyword is None:
            self.pass_keyword: PyPassKeyword = PyPassKeyword()
        else:
            self.pass_keyword: PyPassKeyword = pass_keyword




class PyIfCase(_BaseNode):
    def __init__(self, *, if_keyword: 'PyIfKeyword | None' = None, test: 'PyExpr', colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None) -> None:
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
            raise ValueError("the field 'body' received an unrecognised value'")




class PyElifCase(_BaseNode):
    def __init__(self, *, elif_keyword: 'PyElifKeyword | None' = None, test: 'PyExpr', colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None) -> None:
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
            raise ValueError("the field 'body' received an unrecognised value'")




class PyElseCase(_BaseNode):
    def __init__(self, *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None) -> None:
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
            raise ValueError("the field 'body' received an unrecognised value'")




class PyIfStmt(_BaseNode):
    def __init__(self, *, first: 'PyIfCase', alternatives: 'None | list[PyElifCase]' = None, last: 'PyElseCase | None' = None) -> None:
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



class PyDeleteStmt(_BaseNode):
    def __init__(self, *, del_keyword: 'PyDelKeyword | None' = None, pattern: 'PyPattern') -> None:
        if del_keyword is None:
            self.del_keyword: PyDelKeyword = PyDelKeyword()
        else:
            self.del_keyword: PyDelKeyword = del_keyword

        self.pattern: PyPattern = pattern



class PyRaiseStmt(_BaseNode):
    def __init__(self, *, raise_keyword: 'PyRaiseKeyword | None' = None, expr: 'PyExpr', cause: 'PyExpr | tuple[(PyFormKeyword | None, PyExpr)] | None' = None) -> None:
        if raise_keyword is None:
            self.raise_keyword: PyRaiseKeyword = PyRaiseKeyword()
        else:
            self.raise_keyword: PyRaiseKeyword = raise_keyword

        self.expr: PyExpr = expr
        if is_py_expr(cause) or isinstance(cause, tuple):
            if is_py_expr(cause):
                self.cause: tuple[(PyFormKeyword, PyExpr)] | None = (PyFormKeyword(), cause)
            else:
                assert(isinstance(cause, tuple))
                cause_0 = cause[0]
                if cause_0 is None:
                    new_cause_0 = PyFormKeyword()
                else:
                    new_cause_0 = cause_0

                cause_1 = cause[1]
                new_cause_1 = cause_1
                self.cause: tuple[(PyFormKeyword, PyExpr)] | None = (new_cause_0, new_cause_1)

        elif cause is None:
            self.cause: tuple[(PyFormKeyword, PyExpr)] | None = None
        else:
            raise ValueError("the field 'cause' received an unrecognised value'")




class PyForStmt(_BaseNode):
    def __init__(self, *, for_keyword: 'PyForKeyword | None' = None, pattern: 'PyPattern', in_keyword: 'PyInKeyword | None' = None, expr: 'PyExpr', colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None, else_clause: 'PyStmt | None | list[PyStmt] | tuple[(PyElseKeyword | None, PyColon | None, PyStmt | None | list[PyStmt])] | None' = None) -> None:
        if for_keyword is None:
            self.for_keyword: PyForKeyword = PyForKeyword()
        else:
            self.for_keyword: PyForKeyword = for_keyword

        self.pattern: PyPattern = pattern
        if in_keyword is None:
            self.in_keyword: PyInKeyword = PyInKeyword()
        else:
            self.in_keyword: PyInKeyword = in_keyword

        self.expr: PyExpr = expr
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
            raise ValueError("the field 'body' received an unrecognised value'")

        if is_py_stmt(else_clause) or else_clause is None or isinstance(else_clause, list) or isinstance(else_clause, tuple):
            if is_py_stmt(else_clause) or else_clause is None or isinstance(else_clause, list):
                if is_py_stmt(else_clause):
                    self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), else_clause)
                elif else_clause is None or isinstance(else_clause, list):
                    if else_clause is None:
                        self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), list())
                    else:
                        new_else_clause = list()
                        for else_clause_element in else_clause:
                            new_else_clause_element = else_clause_element
                            new_else_clause.append(new_else_clause_element)

                        self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), new_else_clause)

                else:
                    raise ValueError("the field 'else_clause' received an unrecognised value'")

            else:
                assert(isinstance(else_clause, tuple))
                else_clause_0 = else_clause[0]
                if else_clause_0 is None:
                    new_else_clause_0 = PyElseKeyword()
                else:
                    new_else_clause_0 = else_clause_0

                else_clause_1 = else_clause[1]
                if else_clause_1 is None:
                    new_else_clause_1 = PyColon()
                else:
                    new_else_clause_1 = else_clause_1

                else_clause_2 = else_clause[2]
                if is_py_stmt(else_clause_2):
                    new_else_clause_2 = else_clause_2
                elif else_clause_2 is None or isinstance(else_clause_2, list):
                    if else_clause_2 is None:
                        new_else_clause_2 = list()
                    else:
                        new_else_clause_2 = list()
                        for else_clause_2_element in else_clause_2:
                            new_else_clause_2_element = else_clause_2_element
                            new_else_clause_2.append(new_else_clause_2_element)

                        new_else_clause_2 = new_else_clause_2

                else:
                    raise ValueError("the field 'else_clause' received an unrecognised value'")

                self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (new_else_clause_0, new_else_clause_1, new_else_clause_2)

        elif else_clause is None:
            self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")




class PyWhileStmt(_BaseNode):
    def __init__(self, *, while_keyword: 'PyWhileKeyword | None' = None, expr: 'PyExpr', colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None, else_clause: 'PyStmt | None | list[PyStmt] | tuple[(PyElseKeyword | None, PyColon | None, PyStmt | None | list[PyStmt])] | None' = None) -> None:
        if while_keyword is None:
            self.while_keyword: PyWhileKeyword = PyWhileKeyword()
        else:
            self.while_keyword: PyWhileKeyword = while_keyword

        self.expr: PyExpr = expr
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
            raise ValueError("the field 'body' received an unrecognised value'")

        if is_py_stmt(else_clause) or else_clause is None or isinstance(else_clause, list) or isinstance(else_clause, tuple):
            if is_py_stmt(else_clause) or else_clause is None or isinstance(else_clause, list):
                if is_py_stmt(else_clause):
                    self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), else_clause)
                elif else_clause is None or isinstance(else_clause, list):
                    if else_clause is None:
                        self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), list())
                    else:
                        new_else_clause = list()
                        for else_clause_element in else_clause:
                            new_else_clause_element = else_clause_element
                            new_else_clause.append(new_else_clause_element)

                        self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), new_else_clause)

                else:
                    raise ValueError("the field 'else_clause' received an unrecognised value'")

            else:
                assert(isinstance(else_clause, tuple))
                else_clause_0 = else_clause[0]
                if else_clause_0 is None:
                    new_else_clause_0 = PyElseKeyword()
                else:
                    new_else_clause_0 = else_clause_0

                else_clause_1 = else_clause[1]
                if else_clause_1 is None:
                    new_else_clause_1 = PyColon()
                else:
                    new_else_clause_1 = else_clause_1

                else_clause_2 = else_clause[2]
                if is_py_stmt(else_clause_2):
                    new_else_clause_2 = else_clause_2
                elif else_clause_2 is None or isinstance(else_clause_2, list):
                    if else_clause_2 is None:
                        new_else_clause_2 = list()
                    else:
                        new_else_clause_2 = list()
                        for else_clause_2_element in else_clause_2:
                            new_else_clause_2_element = else_clause_2_element
                            new_else_clause_2.append(new_else_clause_2_element)

                        new_else_clause_2 = new_else_clause_2

                else:
                    raise ValueError("the field 'else_clause' received an unrecognised value'")

                self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (new_else_clause_0, new_else_clause_1, new_else_clause_2)

        elif else_clause is None:
            self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")




class PyBreakStmt(_BaseNode):
    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None) -> None:
        if break_keyword is None:
            self.break_keyword: PyBreakKeyword = PyBreakKeyword()
        else:
            self.break_keyword: PyBreakKeyword = break_keyword




class PyContinueStmt(_BaseNode):
    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None) -> None:
        if continue_keyword is None:
            self.continue_keyword: PyContinueKeyword = PyContinueKeyword()
        else:
            self.continue_keyword: PyContinueKeyword = continue_keyword




class PyTypeAliasStmt(_BaseNode):
    def __init__(self, *, type_keyword: 'PyTypeKeyword | None' = None, name: 'PyIdent | str', type_params: 'None | list[tuple[(PyExpr, PyComma | None)]] | tuple[(PyOpenBracket | None, None | list[tuple[(PyExpr, PyComma | None)]], PyCloseBracket | None)] | None' = None, equals: 'PyEquals | None' = None, expr: 'PyExpr') -> None:
        if type_keyword is None:
            self.type_keyword: PyTypeKeyword = PyTypeKeyword()
        else:
            self.type_keyword: PyTypeKeyword = type_keyword

        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name

        if type_params is None or isinstance(type_params, list) or isinstance(type_params, tuple):
            if type_params is None or isinstance(type_params, list):
                if type_params is None:
                    self.type_params: tuple[(PyOpenBracket, list[tuple[(PyExpr, PyComma | None)]], PyCloseBracket)] | None = (PyOpenBracket(), list(), PyCloseBracket())
                else:
                    new_type_params = list()
                    for type_params_element in type_params:
                        assert(isinstance(type_params_element, tuple))
                        type_params_element_0 = type_params_element[0]
                        new_type_params_element_0 = type_params_element_0
                        type_params_element_1 = type_params_element[1]
                        if isinstance(type_params_element_1, PyComma):
                            new_type_params_element_1 = type_params_element_1
                        elif type_params_element_1 is None:
                            new_type_params_element_1 = None
                        else:
                            raise ValueError("the field 'type_params' received an unrecognised value'")

                        new_type_params_element = (new_type_params_element_0, new_type_params_element_1)
                        new_type_params.append(new_type_params_element)

                    self.type_params: tuple[(PyOpenBracket, list[tuple[(PyExpr, PyComma | None)]], PyCloseBracket)] | None = (PyOpenBracket(), new_type_params, PyCloseBracket())

            else:
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
                        assert(isinstance(type_params_1_element, tuple))
                        type_params_1_element_0 = type_params_1_element[0]
                        new_type_params_1_element_0 = type_params_1_element_0
                        type_params_1_element_1 = type_params_1_element[1]
                        if isinstance(type_params_1_element_1, PyComma):
                            new_type_params_1_element_1 = type_params_1_element_1
                        elif type_params_1_element_1 is None:
                            new_type_params_1_element_1 = None
                        else:
                            raise ValueError("the field 'type_params' received an unrecognised value'")

                        new_type_params_1_element = (new_type_params_1_element_0, new_type_params_1_element_1)
                        new_type_params_1.append(new_type_params_1_element)

                    new_type_params_1 = new_type_params_1

                type_params_2 = type_params[2]
                if type_params_2 is None:
                    new_type_params_2 = PyCloseBracket()
                else:
                    new_type_params_2 = type_params_2

                self.type_params: tuple[(PyOpenBracket, list[tuple[(PyExpr, PyComma | None)]], PyCloseBracket)] | None = (new_type_params_0, new_type_params_1, new_type_params_2)

        elif type_params is None:
            self.type_params: tuple[(PyOpenBracket, list[tuple[(PyExpr, PyComma | None)]], PyCloseBracket)] | None = None
        else:
            raise ValueError("the field 'type_params' received an unrecognised value'")

        if equals is None:
            self.equals: PyEquals = PyEquals()
        else:
            self.equals: PyEquals = equals

        self.expr: PyExpr = expr



class PyExceptHandler(_BaseNode):
    def __init__(self, *, except_keyword: 'PyExceptKeyword | None' = None, expr: 'PyExpr', binder: 'PyIdent | str | tuple[(PyAsKeyword | None, PyIdent | str)] | None' = None, body: 'PyStmt | None | list[PyStmt]' = None) -> None:
        if except_keyword is None:
            self.except_keyword: PyExceptKeyword = PyExceptKeyword()
        else:
            self.except_keyword: PyExceptKeyword = except_keyword

        self.expr: PyExpr = expr
        if isinstance(binder, PyIdent) or isinstance(binder, str) or isinstance(binder, tuple):
            if isinstance(binder, PyIdent) or isinstance(binder, str):
                if isinstance(binder, str):
                    self.binder: tuple[(PyAsKeyword, PyIdent)] | None = (PyAsKeyword(), PyIdent(binder))
                else:
                    self.binder: tuple[(PyAsKeyword, PyIdent)] | None = (PyAsKeyword(), binder)

            else:
                assert(isinstance(binder, tuple))
                binder_0 = binder[0]
                if binder_0 is None:
                    new_binder_0 = PyAsKeyword()
                else:
                    new_binder_0 = binder_0

                binder_1 = binder[1]
                if isinstance(binder_1, str):
                    new_binder_1 = PyIdent(binder_1)
                else:
                    new_binder_1 = binder_1

                self.binder: tuple[(PyAsKeyword, PyIdent)] | None = (new_binder_0, new_binder_1)

        elif binder is None:
            self.binder: tuple[(PyAsKeyword, PyIdent)] | None = None
        else:
            raise ValueError("the field 'binder' received an unrecognised value'")

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
            raise ValueError("the field 'body' received an unrecognised value'")




class PyTryStmt(_BaseNode):
    def __init__(self, *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None, handlers: 'None | list[PyExceptHandler]' = None, else_clause: 'PyStmt | None | list[PyStmt] | tuple[(PyElseKeyword | None, PyColon | None, PyStmt | None | list[PyStmt])] | None' = None, finally_clause: 'PyStmt | None | list[PyStmt] | tuple[(PyFinallyKeyword | None, PyColon | None, PyStmt | None | list[PyStmt])] | None' = None) -> None:
        if try_keyword is None:
            self.try_keyword: PyTryKeyword = PyTryKeyword()
        else:
            self.try_keyword: PyTryKeyword = try_keyword

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
            raise ValueError("the field 'body' received an unrecognised value'")

        if handlers is None:
            self.handlers: list[PyExceptHandler] = list()
        else:
            new_handlers = list()
            for handlers_element in handlers:
                new_handlers_element = handlers_element
                new_handlers.append(new_handlers_element)

            self.handlers: list[PyExceptHandler] = new_handlers

        if is_py_stmt(else_clause) or else_clause is None or isinstance(else_clause, list) or isinstance(else_clause, tuple):
            if is_py_stmt(else_clause) or else_clause is None or isinstance(else_clause, list):
                if is_py_stmt(else_clause):
                    self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), else_clause)
                elif else_clause is None or isinstance(else_clause, list):
                    if else_clause is None:
                        self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), list())
                    else:
                        new_else_clause = list()
                        for else_clause_element in else_clause:
                            new_else_clause_element = else_clause_element
                            new_else_clause.append(new_else_clause_element)

                        self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyElseKeyword(), PyColon(), new_else_clause)

                else:
                    raise ValueError("the field 'else_clause' received an unrecognised value'")

            else:
                assert(isinstance(else_clause, tuple))
                else_clause_0 = else_clause[0]
                if else_clause_0 is None:
                    new_else_clause_0 = PyElseKeyword()
                else:
                    new_else_clause_0 = else_clause_0

                else_clause_1 = else_clause[1]
                if else_clause_1 is None:
                    new_else_clause_1 = PyColon()
                else:
                    new_else_clause_1 = else_clause_1

                else_clause_2 = else_clause[2]
                if is_py_stmt(else_clause_2):
                    new_else_clause_2 = else_clause_2
                elif else_clause_2 is None or isinstance(else_clause_2, list):
                    if else_clause_2 is None:
                        new_else_clause_2 = list()
                    else:
                        new_else_clause_2 = list()
                        for else_clause_2_element in else_clause_2:
                            new_else_clause_2_element = else_clause_2_element
                            new_else_clause_2.append(new_else_clause_2_element)

                        new_else_clause_2 = new_else_clause_2

                else:
                    raise ValueError("the field 'else_clause' received an unrecognised value'")

                self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = (new_else_clause_0, new_else_clause_1, new_else_clause_2)

        elif else_clause is None:
            self.else_clause: tuple[(PyElseKeyword, PyColon, PyStmt | list[PyStmt])] | None = None
        else:
            raise ValueError("the field 'else_clause' received an unrecognised value'")

        if is_py_stmt(finally_clause) or finally_clause is None or isinstance(finally_clause, list) or isinstance(finally_clause, tuple):
            if is_py_stmt(finally_clause) or finally_clause is None or isinstance(finally_clause, list):
                if is_py_stmt(finally_clause):
                    self.finally_clause: tuple[(PyFinallyKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyFinallyKeyword(), PyColon(), finally_clause)
                elif finally_clause is None or isinstance(finally_clause, list):
                    if finally_clause is None:
                        self.finally_clause: tuple[(PyFinallyKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyFinallyKeyword(), PyColon(), list())
                    else:
                        new_finally_clause = list()
                        for finally_clause_element in finally_clause:
                            new_finally_clause_element = finally_clause_element
                            new_finally_clause.append(new_finally_clause_element)

                        self.finally_clause: tuple[(PyFinallyKeyword, PyColon, PyStmt | list[PyStmt])] | None = (PyFinallyKeyword(), PyColon(), new_finally_clause)

                else:
                    raise ValueError("the field 'finally_clause' received an unrecognised value'")

            else:
                assert(isinstance(finally_clause, tuple))
                finally_clause_0 = finally_clause[0]
                if finally_clause_0 is None:
                    new_finally_clause_0 = PyFinallyKeyword()
                else:
                    new_finally_clause_0 = finally_clause_0

                finally_clause_1 = finally_clause[1]
                if finally_clause_1 is None:
                    new_finally_clause_1 = PyColon()
                else:
                    new_finally_clause_1 = finally_clause_1

                finally_clause_2 = finally_clause[2]
                if is_py_stmt(finally_clause_2):
                    new_finally_clause_2 = finally_clause_2
                elif finally_clause_2 is None or isinstance(finally_clause_2, list):
                    if finally_clause_2 is None:
                        new_finally_clause_2 = list()
                    else:
                        new_finally_clause_2 = list()
                        for finally_clause_2_element in finally_clause_2:
                            new_finally_clause_2_element = finally_clause_2_element
                            new_finally_clause_2.append(new_finally_clause_2_element)

                        new_finally_clause_2 = new_finally_clause_2

                else:
                    raise ValueError("the field 'finally_clause' received an unrecognised value'")

                self.finally_clause: tuple[(PyFinallyKeyword, PyColon, PyStmt | list[PyStmt])] | None = (new_finally_clause_0, new_finally_clause_1, new_finally_clause_2)

        elif finally_clause is None:
            self.finally_clause: tuple[(PyFinallyKeyword, PyColon, PyStmt | list[PyStmt])] | None = None
        else:
            raise ValueError("the field 'finally_clause' received an unrecognised value'")




class PyClassDef(_BaseNode):
    def __init__(self, *, class_keyword: 'PyClassKeyword | None' = None, name: 'PyIdent | str', bases: 'None | list[tuple[(PyIdent | str, PyComma | None)]] | tuple[(PyOpenParen | None, None | list[tuple[(PyIdent | str, PyComma | None)]], PyCloseParen | None)] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None) -> None:
        if class_keyword is None:
            self.class_keyword: PyClassKeyword = PyClassKeyword()
        else:
            self.class_keyword: PyClassKeyword = class_keyword

        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name

        if bases is None or isinstance(bases, list) or isinstance(bases, tuple):
            if bases is None or isinstance(bases, list):
                if bases is None:
                    self.bases: tuple[(PyOpenParen, list[tuple[(PyIdent, PyComma | None)]], PyCloseParen)] | None = (PyOpenParen(), list(), PyCloseParen())
                else:
                    new_bases = list()
                    for bases_element in bases:
                        assert(isinstance(bases_element, tuple))
                        bases_element_0 = bases_element[0]
                        if isinstance(bases_element_0, str):
                            new_bases_element_0 = PyIdent(bases_element_0)
                        else:
                            new_bases_element_0 = bases_element_0

                        bases_element_1 = bases_element[1]
                        if isinstance(bases_element_1, PyComma):
                            new_bases_element_1 = bases_element_1
                        elif bases_element_1 is None:
                            new_bases_element_1 = None
                        else:
                            raise ValueError("the field 'bases' received an unrecognised value'")

                        new_bases_element = (new_bases_element_0, new_bases_element_1)
                        new_bases.append(new_bases_element)

                    self.bases: tuple[(PyOpenParen, list[tuple[(PyIdent, PyComma | None)]], PyCloseParen)] | None = (PyOpenParen(), new_bases, PyCloseParen())

            else:
                assert(isinstance(bases, tuple))
                bases_0 = bases[0]
                if bases_0 is None:
                    new_bases_0 = PyOpenParen()
                else:
                    new_bases_0 = bases_0

                bases_1 = bases[1]
                if bases_1 is None:
                    new_bases_1 = list()
                else:
                    new_bases_1 = list()
                    for bases_1_element in bases_1:
                        assert(isinstance(bases_1_element, tuple))
                        bases_1_element_0 = bases_1_element[0]
                        if isinstance(bases_1_element_0, str):
                            new_bases_1_element_0 = PyIdent(bases_1_element_0)
                        else:
                            new_bases_1_element_0 = bases_1_element_0

                        bases_1_element_1 = bases_1_element[1]
                        if isinstance(bases_1_element_1, PyComma):
                            new_bases_1_element_1 = bases_1_element_1
                        elif bases_1_element_1 is None:
                            new_bases_1_element_1 = None
                        else:
                            raise ValueError("the field 'bases' received an unrecognised value'")

                        new_bases_1_element = (new_bases_1_element_0, new_bases_1_element_1)
                        new_bases_1.append(new_bases_1_element)

                    new_bases_1 = new_bases_1

                bases_2 = bases[2]
                if bases_2 is None:
                    new_bases_2 = PyCloseParen()
                else:
                    new_bases_2 = bases_2

                self.bases: tuple[(PyOpenParen, list[tuple[(PyIdent, PyComma | None)]], PyCloseParen)] | None = (new_bases_0, new_bases_1, new_bases_2)

        elif bases is None:
            self.bases: tuple[(PyOpenParen, list[tuple[(PyIdent, PyComma | None)]], PyCloseParen)] | None = None
        else:
            raise ValueError("the field 'bases' received an unrecognised value'")

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
            raise ValueError("the field 'body' received an unrecognised value'")




PyParam: TypeAlias = 'PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam'

def is_py_param(value: Any) -> TypeGuard[PyParam]:
    return isinstance(value, PyNamedParam) or isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PySepParam)


class PyNamedParam(_BaseNode):
    def __init__(self, *, pattern: 'PyPattern', annotation: 'PyExpr | tuple[(PyColon | None, PyExpr)] | None' = None, default: 'PyExpr | tuple[(PyEquals | None, PyExpr)] | None' = None) -> None:
        self.pattern: PyPattern = pattern
        if is_py_expr(annotation) or isinstance(annotation, tuple):
            if is_py_expr(annotation):
                self.annotation: tuple[(PyColon, PyExpr)] | None = (PyColon(), annotation)
            else:
                assert(isinstance(annotation, tuple))
                annotation_0 = annotation[0]
                if annotation_0 is None:
                    new_annotation_0 = PyColon()
                else:
                    new_annotation_0 = annotation_0

                annotation_1 = annotation[1]
                new_annotation_1 = annotation_1
                self.annotation: tuple[(PyColon, PyExpr)] | None = (new_annotation_0, new_annotation_1)

        elif annotation is None:
            self.annotation: tuple[(PyColon, PyExpr)] | None = None
        else:
            raise ValueError("the field 'annotation' received an unrecognised value'")

        if is_py_expr(default) or isinstance(default, tuple):
            if is_py_expr(default):
                self.default: tuple[(PyEquals, PyExpr)] | None = (PyEquals(), default)
            else:
                assert(isinstance(default, tuple))
                default_0 = default[0]
                if default_0 is None:
                    new_default_0 = PyEquals()
                else:
                    new_default_0 = default_0

                default_1 = default[1]
                new_default_1 = default_1
                self.default: tuple[(PyEquals, PyExpr)] | None = (new_default_0, new_default_1)

        elif default is None:
            self.default: tuple[(PyEquals, PyExpr)] | None = None
        else:
            raise ValueError("the field 'default' received an unrecognised value'")




class PyRestPosParam(_BaseNode):
    def __init__(self, *, asterisk: 'PyAsterisk | None' = None, name: 'PyIdent | str') -> None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk

        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name




class PyRestKeywordParam(_BaseNode):
    def __init__(self, *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None, name: 'PyIdent | str') -> None:
        if asterisk_asterisk is None:
            self.asterisk_asterisk: PyAsteriskAsterisk = PyAsteriskAsterisk()
        else:
            self.asterisk_asterisk: PyAsteriskAsterisk = asterisk_asterisk

        if isinstance(name, str):
            self.name: PyIdent = PyIdent(name)
        else:
            self.name: PyIdent = name




class PySepParam(_BaseNode):
    def __init__(self, *, asterisk: 'PyAsterisk | None' = None) -> None:
        if asterisk is None:
            self.asterisk: PyAsterisk = PyAsterisk()
        else:
            self.asterisk: PyAsterisk = asterisk




class PyFuncDef(_BaseNode):
    def __init__(self, *, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, name: 'PyIdent | str', open_paren: 'PyOpenParen | None' = None, params: 'None | list[tuple[(PyParam, PyComma | None)]]' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[(PyHyphenGreaterThan | None, PyExpr)] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | None | list[PyStmt]' = None) -> None:
        if isinstance(async_keyword, PyAsyncKeyword):
            self.async_keyword: PyAsyncKeyword | None = async_keyword
        elif async_keyword is None:
            self.async_keyword: PyAsyncKeyword | None = None
        else:
            raise ValueError("the field 'async_keyword' received an unrecognised value'")

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
            self.params: list[tuple[(PyParam, PyComma | None)]] = list()
        else:
            new_params = list()
            for params_element in params:
                assert(isinstance(params_element, tuple))
                params_element_0 = params_element[0]
                new_params_element_0 = params_element_0
                params_element_1 = params_element[1]
                if isinstance(params_element_1, PyComma):
                    new_params_element_1 = params_element_1
                elif params_element_1 is None:
                    new_params_element_1 = None
                else:
                    raise ValueError("the field 'params' received an unrecognised value'")

                new_params_element = (new_params_element_0, new_params_element_1)
                new_params.append(new_params_element)

            self.params: list[tuple[(PyParam, PyComma | None)]] = new_params

        if close_paren is None:
            self.close_paren: PyCloseParen = PyCloseParen()
        else:
            self.close_paren: PyCloseParen = close_paren

        if is_py_expr(return_type) or isinstance(return_type, tuple):
            if is_py_expr(return_type):
                self.return_type: tuple[(PyHyphenGreaterThan, PyExpr)] | None = (PyHyphenGreaterThan(), return_type)
            else:
                assert(isinstance(return_type, tuple))
                return_type_0 = return_type[0]
                if return_type_0 is None:
                    new_return_type_0 = PyHyphenGreaterThan()
                else:
                    new_return_type_0 = return_type_0

                return_type_1 = return_type[1]
                new_return_type_1 = return_type_1
                self.return_type: tuple[(PyHyphenGreaterThan, PyExpr)] | None = (new_return_type_0, new_return_type_1)

        elif return_type is None:
            self.return_type: tuple[(PyHyphenGreaterThan, PyExpr)] | None = None
        else:
            raise ValueError("the field 'return_type' received an unrecognised value'")

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
            raise ValueError("the field 'body' received an unrecognised value'")




class PyModule(_BaseNode):
    def __init__(self, *, stmts: 'None | list[PyStmt]' = None) -> None:
        if stmts is None:
            self.stmts: list[PyStmt] = list()
        else:
            new_stmts = list()
            for stmts_element in stmts:
                new_stmts_element = stmts_element
                new_stmts.append(new_stmts_element)

            self.stmts: list[PyStmt] = new_stmts




PyToken = PyCarriageReturnLineFeed | PyLineFeed | PySemicolon | PyZero | PyDot | PyDoubleQuote | PySingleQuote | PyColon | PyOpenBracket | PyComma | PyCloseBracket | PyAsterisk | PyOpenParen | PyCloseParen | PyEquals | PyNotKeyword | PyPlus | PyHyphen | PyTilde | PySlash | PySlashSlash | PyPercenct | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyAtSign | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | PyInKeyword | PyReturnKeyword | PyPassKeyword | PyIfKeyword | PyElifKeyword | PyElseKeyword | PyDelKeyword | PyRaiseKeyword | PyFormKeyword | PyForKeyword | PyWhileKeyword | PyBreakKeyword | PyContinueKeyword | PyTypeKeyword | PyExceptKeyword | PyAsKeyword | PyTryKeyword | PyFinallyKeyword | PyClassKeyword | PyAsteriskAsterisk | PyAsyncKeyword | PyDefKeyword | PyHyphenGreaterThan | PyIdent | PyInteger | PyFloat | PyString | PyPrefixOp | PyInfixOp

PyNode = PySlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleExpr | PyKeywordArg | PyCallExpr | PyPrefixExpr | PyInfixExpr | PyRetStmt | PyExprStmt | PyAssignStmt | PyPassStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam | PyFuncDef | PyModule

PySyntax = PyToken | PyNode

def is_py_token(value: Any) -> TypeGuard[PyToken]: return isinstance(value, _BaseToken)

def is_py_node(value: Any) -> TypeGuard[PyNode]: return isinstance(value, _BaseNode)

def is_py_syntax(value: Any): return is_py_node(value) or is_py_token(value)



def for_each_py_child(node: PySyntax, proc: Callable[[PySyntax],None]):
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
        for element_0 in node.slices:
            element_1 = element_0[0]
            if is_py_pattern(element_1):
                proc(element_1)
            elif isinstance(element_1, PySlice):
                proc(element_1)
            else:
                raise ValueError()

            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
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
        for element_0 in node.elements:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
            else:
                raise ValueError()


        proc(node.close_bracket)
        return

    if isinstance(node, PyTuplePattern):
        proc(node.open_paren)
        for element_0 in node.elements:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
            else:
                raise ValueError()


        proc(node.close_paren)
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
        for element_0 in node.slices:
            element_1 = element_0[0]
            if is_py_expr(element_1):
                proc(element_1)
            elif isinstance(element_1, PySlice):
                proc(element_1)
            else:
                raise ValueError()

            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
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
        for element_0 in node.elements:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
            else:
                raise ValueError()


        proc(node.close_bracket)
        return

    if isinstance(node, PyTupleExpr):
        proc(node.open_paren)
        for element_0 in node.elements:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
            else:
                raise ValueError()


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
        for element_0 in node.args:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
            else:
                raise ValueError()


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
            for element_2 in element_1:
                element_3 = element_2[0]
                proc(element_3)
                element_4 = element_2[1]
                if isinstance(element_4, PyComma):
                    proc(element_4)
                elif element_4 is None:
                    pass
                else:
                    raise ValueError()


            element_5 = node.type_params[2]
            proc(element_5)
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
            for element_2 in element_1:
                element_3 = element_2[0]
                proc(element_3)
                element_4 = element_2[1]
                if isinstance(element_4, PyComma):
                    proc(element_4)
                elif element_4 is None:
                    pass
                else:
                    raise ValueError()


            element_5 = node.bases[2]
            proc(element_5)
        elif node.bases is None:
            pass
        else:
            raise ValueError()

        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_6 in node.body:
                proc(element_6)

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
        for element_0 in node.params:
            element_1 = element_0[0]
            proc(element_1)
            element_2 = element_0[1]
            if isinstance(element_2, PyComma):
                proc(element_2)
            elif element_2 is None:
                pass
            else:
                raise ValueError()


        proc(node.close_paren)
        if isinstance(node.return_type, tuple):
            element_3 = node.return_type[0]
            proc(element_3)
            element_4 = node.return_type[1]
            proc(element_4)
        elif node.return_type is None:
            pass
        else:
            raise ValueError()

        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_5 in node.body:
                proc(element_5)

        else:
            raise ValueError()

        return

    if isinstance(node, PyModule):
        for element_0 in node.stmts:
            proc(element_0)

        return


