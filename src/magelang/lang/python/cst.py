from enum import IntEnum


from typing import Any, TypeGuard, TypeIs, TypedDict, Never, Unpack, Sequence, Callable, assert_never, no_type_check, cast


from magelang.runtime import BaseSyntax, Punctuated, ImmutablePunct, Span


class _PyBaseSyntax(BaseSyntax):

    pass


class _PyBaseNode(_PyBaseSyntax):

    pass


class _PyBaseToken(_PyBaseSyntax):

    def __init__(self, span: Span | None = None):
        super().__init__()
        self.span = span


class PyAmpersand(_PyBaseToken):

    pass


def is_py_ampersand(value: Any) -> TypeIs[PyAmpersand]:
    return isinstance(value, PyAmpersand)


class PyAndKeyword(_PyBaseToken):

    pass


def is_py_and_keyword(value: Any) -> TypeIs[PyAndKeyword]:
    return isinstance(value, PyAndKeyword)


class PyAsKeyword(_PyBaseToken):

    pass


def is_py_as_keyword(value: Any) -> TypeIs[PyAsKeyword]:
    return isinstance(value, PyAsKeyword)


class PyAsterisk(_PyBaseToken):

    pass


def is_py_asterisk(value: Any) -> TypeIs[PyAsterisk]:
    return isinstance(value, PyAsterisk)


class PyAsteriskAsterisk(_PyBaseToken):

    pass


def is_py_asterisk_asterisk(value: Any) -> TypeIs[PyAsteriskAsterisk]:
    return isinstance(value, PyAsteriskAsterisk)


class PyAsyncKeyword(_PyBaseToken):

    pass


def is_py_async_keyword(value: Any) -> TypeIs[PyAsyncKeyword]:
    return isinstance(value, PyAsyncKeyword)


class PyAtSign(_PyBaseToken):

    pass


def is_py_at_sign(value: Any) -> TypeIs[PyAtSign]:
    return isinstance(value, PyAtSign)


class PyBreakKeyword(_PyBaseToken):

    pass


def is_py_break_keyword(value: Any) -> TypeIs[PyBreakKeyword]:
    return isinstance(value, PyBreakKeyword)


class PyCaret(_PyBaseToken):

    pass


def is_py_caret(value: Any) -> TypeIs[PyCaret]:
    return isinstance(value, PyCaret)


class PyClassKeyword(_PyBaseToken):

    pass


def is_py_class_keyword(value: Any) -> TypeIs[PyClassKeyword]:
    return isinstance(value, PyClassKeyword)


class PyCloseBracket(_PyBaseToken):

    pass


def is_py_close_bracket(value: Any) -> TypeIs[PyCloseBracket]:
    return isinstance(value, PyCloseBracket)


class PyCloseParen(_PyBaseToken):

    pass


def is_py_close_paren(value: Any) -> TypeIs[PyCloseParen]:
    return isinstance(value, PyCloseParen)


class PyColon(_PyBaseToken):

    pass


def is_py_colon(value: Any) -> TypeIs[PyColon]:
    return isinstance(value, PyColon)


class PyComma(_PyBaseToken):

    pass


def is_py_comma(value: Any) -> TypeIs[PyComma]:
    return isinstance(value, PyComma)


class PyContinueKeyword(_PyBaseToken):

    pass


def is_py_continue_keyword(value: Any) -> TypeIs[PyContinueKeyword]:
    return isinstance(value, PyContinueKeyword)


class PyDefKeyword(_PyBaseToken):

    pass


def is_py_def_keyword(value: Any) -> TypeIs[PyDefKeyword]:
    return isinstance(value, PyDefKeyword)


class PyDelKeyword(_PyBaseToken):

    pass


def is_py_del_keyword(value: Any) -> TypeIs[PyDelKeyword]:
    return isinstance(value, PyDelKeyword)


class PyDot(_PyBaseToken):

    pass


def is_py_dot(value: Any) -> TypeIs[PyDot]:
    return isinstance(value, PyDot)


class PyDotDotDot(_PyBaseToken):

    pass


def is_py_dot_dot_dot(value: Any) -> TypeIs[PyDotDotDot]:
    return isinstance(value, PyDotDotDot)


class PyElifKeyword(_PyBaseToken):

    pass


def is_py_elif_keyword(value: Any) -> TypeIs[PyElifKeyword]:
    return isinstance(value, PyElifKeyword)


class PyElseKeyword(_PyBaseToken):

    pass


def is_py_else_keyword(value: Any) -> TypeIs[PyElseKeyword]:
    return isinstance(value, PyElseKeyword)


class PyEquals(_PyBaseToken):

    pass


def is_py_equals(value: Any) -> TypeIs[PyEquals]:
    return isinstance(value, PyEquals)


class PyEqualsEquals(_PyBaseToken):

    pass


def is_py_equals_equals(value: Any) -> TypeIs[PyEqualsEquals]:
    return isinstance(value, PyEqualsEquals)


class PyExceptKeyword(_PyBaseToken):

    pass


def is_py_except_keyword(value: Any) -> TypeIs[PyExceptKeyword]:
    return isinstance(value, PyExceptKeyword)


class PyExclamationMarkEquals(_PyBaseToken):

    pass


def is_py_exclamation_mark_equals(value: Any) -> TypeIs[PyExclamationMarkEquals]:
    return isinstance(value, PyExclamationMarkEquals)


class PyFinallyKeyword(_PyBaseToken):

    pass


def is_py_finally_keyword(value: Any) -> TypeIs[PyFinallyKeyword]:
    return isinstance(value, PyFinallyKeyword)


class PyFloat(_PyBaseToken):

    def __init__(self, value: float, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_py_float(value: Any) -> TypeIs[PyFloat]:
    return isinstance(value, PyFloat)


class PyForKeyword(_PyBaseToken):

    pass


def is_py_for_keyword(value: Any) -> TypeIs[PyForKeyword]:
    return isinstance(value, PyForKeyword)


class PyFromKeyword(_PyBaseToken):

    pass


def is_py_from_keyword(value: Any) -> TypeIs[PyFromKeyword]:
    return isinstance(value, PyFromKeyword)


class PyGlobalKeyword(_PyBaseToken):

    pass


def is_py_global_keyword(value: Any) -> TypeIs[PyGlobalKeyword]:
    return isinstance(value, PyGlobalKeyword)


class PyGreaterThan(_PyBaseToken):

    pass


def is_py_greater_than(value: Any) -> TypeIs[PyGreaterThan]:
    return isinstance(value, PyGreaterThan)


class PyGreaterThanEquals(_PyBaseToken):

    pass


def is_py_greater_than_equals(value: Any) -> TypeIs[PyGreaterThanEquals]:
    return isinstance(value, PyGreaterThanEquals)


class PyGreaterThanGreaterThan(_PyBaseToken):

    pass


def is_py_greater_than_greater_than(value: Any) -> TypeIs[PyGreaterThanGreaterThan]:
    return isinstance(value, PyGreaterThanGreaterThan)


class PyHyphen(_PyBaseToken):

    pass


def is_py_hyphen(value: Any) -> TypeIs[PyHyphen]:
    return isinstance(value, PyHyphen)


class PyIdent(_PyBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_py_ident(value: Any) -> TypeIs[PyIdent]:
    return isinstance(value, PyIdent)


class PyIfKeyword(_PyBaseToken):

    pass


def is_py_if_keyword(value: Any) -> TypeIs[PyIfKeyword]:
    return isinstance(value, PyIfKeyword)


class PyImportKeyword(_PyBaseToken):

    pass


def is_py_import_keyword(value: Any) -> TypeIs[PyImportKeyword]:
    return isinstance(value, PyImportKeyword)


class PyInKeyword(_PyBaseToken):

    pass


def is_py_in_keyword(value: Any) -> TypeIs[PyInKeyword]:
    return isinstance(value, PyInKeyword)


class PyInteger(_PyBaseToken):

    def __init__(self, value: int, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_py_integer(value: Any) -> TypeIs[PyInteger]:
    return isinstance(value, PyInteger)


class PyIsKeyword(_PyBaseToken):

    pass


def is_py_is_keyword(value: Any) -> TypeIs[PyIsKeyword]:
    return isinstance(value, PyIsKeyword)


class PyLambdaKeyword(_PyBaseToken):

    pass


def is_py_lambda_keyword(value: Any) -> TypeIs[PyLambdaKeyword]:
    return isinstance(value, PyLambdaKeyword)


class PyLessThan(_PyBaseToken):

    pass


def is_py_less_than(value: Any) -> TypeIs[PyLessThan]:
    return isinstance(value, PyLessThan)


class PyLessThanEquals(_PyBaseToken):

    pass


def is_py_less_than_equals(value: Any) -> TypeIs[PyLessThanEquals]:
    return isinstance(value, PyLessThanEquals)


class PyLessThanLessThan(_PyBaseToken):

    pass


def is_py_less_than_less_than(value: Any) -> TypeIs[PyLessThanLessThan]:
    return isinstance(value, PyLessThanLessThan)


class PyNonlocalKeyword(_PyBaseToken):

    pass


def is_py_nonlocal_keyword(value: Any) -> TypeIs[PyNonlocalKeyword]:
    return isinstance(value, PyNonlocalKeyword)


class PyNotKeyword(_PyBaseToken):

    pass


def is_py_not_keyword(value: Any) -> TypeIs[PyNotKeyword]:
    return isinstance(value, PyNotKeyword)


class PyOpenBracket(_PyBaseToken):

    pass


def is_py_open_bracket(value: Any) -> TypeIs[PyOpenBracket]:
    return isinstance(value, PyOpenBracket)


class PyOpenParen(_PyBaseToken):

    pass


def is_py_open_paren(value: Any) -> TypeIs[PyOpenParen]:
    return isinstance(value, PyOpenParen)


class PyOrKeyword(_PyBaseToken):

    pass


def is_py_or_keyword(value: Any) -> TypeIs[PyOrKeyword]:
    return isinstance(value, PyOrKeyword)


class PyPassKeyword(_PyBaseToken):

    pass


def is_py_pass_keyword(value: Any) -> TypeIs[PyPassKeyword]:
    return isinstance(value, PyPassKeyword)


class PyPercent(_PyBaseToken):

    pass


def is_py_percent(value: Any) -> TypeIs[PyPercent]:
    return isinstance(value, PyPercent)


class PyPlus(_PyBaseToken):

    pass


def is_py_plus(value: Any) -> TypeIs[PyPlus]:
    return isinstance(value, PyPlus)


class PyRArrow(_PyBaseToken):

    pass


def is_py_r_arrow(value: Any) -> TypeIs[PyRArrow]:
    return isinstance(value, PyRArrow)


class PyRaiseKeyword(_PyBaseToken):

    pass


def is_py_raise_keyword(value: Any) -> TypeIs[PyRaiseKeyword]:
    return isinstance(value, PyRaiseKeyword)


class PyReturnKeyword(_PyBaseToken):

    pass


def is_py_return_keyword(value: Any) -> TypeIs[PyReturnKeyword]:
    return isinstance(value, PyReturnKeyword)


class PySlash(_PyBaseToken):

    pass


def is_py_slash(value: Any) -> TypeIs[PySlash]:
    return isinstance(value, PySlash)


class PySlashSlash(_PyBaseToken):

    pass


def is_py_slash_slash(value: Any) -> TypeIs[PySlashSlash]:
    return isinstance(value, PySlashSlash)


class PyString(_PyBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_py_string(value: Any) -> TypeIs[PyString]:
    return isinstance(value, PyString)


class PyTilde(_PyBaseToken):

    pass


def is_py_tilde(value: Any) -> TypeIs[PyTilde]:
    return isinstance(value, PyTilde)


class PyTryKeyword(_PyBaseToken):

    pass


def is_py_try_keyword(value: Any) -> TypeIs[PyTryKeyword]:
    return isinstance(value, PyTryKeyword)


class PyTypeKeyword(_PyBaseToken):

    pass


def is_py_type_keyword(value: Any) -> TypeIs[PyTypeKeyword]:
    return isinstance(value, PyTypeKeyword)


class PyVerticalBar(_PyBaseToken):

    pass


def is_py_vertical_bar(value: Any) -> TypeIs[PyVerticalBar]:
    return isinstance(value, PyVerticalBar)


class PyWhileKeyword(_PyBaseToken):

    pass


def is_py_while_keyword(value: Any) -> TypeIs[PyWhileKeyword]:
    return isinstance(value, PyWhileKeyword)


class PyAbsolutePathDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | PyQualName | str'


class PyAbsolutePath(_PyBaseNode):

    _fields_ = ('name', )

    def __init__(self, name: 'PyIdent | PyQualName | str') -> None:
        self.name: PyQualName = _coerce_1(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyAbsolutePathDeriveKwargs]) -> 'PyAbsolutePath':
        name = _coerce_1(kwargs['name']) if 'name' in kwargs else self.name
        return PyAbsolutePath(name=name)

    @property
    def parent(self) -> 'PyAbsolutePathParent':
        assert(self._parent is not None)
        return cast(PyAbsolutePathParent, self._parent)


def is_py_absolute_path(value: Any) -> TypeIs[PyAbsolutePath]:
    return isinstance(value, PyAbsolutePath)


class PyAliasDeriveKwargs(TypedDict, total=False):

    path: 'PyPath'

    asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str'


class PyAlias(_PyBaseNode):

    _fields_ = ('path', 'asname')

    def __init__(self, path: 'PyPath', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> None:
        self.path: PyPath = _coerce_2(path)
        self.asname: tuple[PyAsKeyword, PyIdent] | None = _coerce_4(asname)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyAliasDeriveKwargs]) -> 'PyAlias':
        path = _coerce_2(kwargs['path']) if 'path' in kwargs else self.path
        asname = _coerce_4(kwargs['asname']) if 'asname' in kwargs else self.asname
        return PyAlias(path=path, asname=asname)

    @property
    def parent(self) -> 'PyAliasParent':
        assert(self._parent is not None)
        return cast(PyAliasParent, self._parent)


def is_py_alias(value: Any) -> TypeIs[PyAlias]:
    return isinstance(value, PyAlias)


class PyAssignStmtDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'

    value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None'


class PyAssignStmt(_PyBaseNode):

    _fields_ = ('pattern', 'annotation', 'value')

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = _coerce_5(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_8(annotation)
        self.value: tuple[PyEquals, PyExpr] | None = _coerce_10(value)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyAssignStmtDeriveKwargs]) -> 'PyAssignStmt':
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        annotation = _coerce_8(kwargs['annotation']) if 'annotation' in kwargs else self.annotation
        value = _coerce_10(kwargs['value']) if 'value' in kwargs else self.value
        return PyAssignStmt(pattern=pattern, annotation=annotation, value=value)

    @property
    def parent(self) -> 'PyAssignStmtParent':
        assert(self._parent is not None)
        return cast(PyAssignStmtParent, self._parent)


def is_py_assign_stmt(value: Any) -> TypeIs[PyAssignStmt]:
    return isinstance(value, PyAssignStmt)


class PyAttrExprDeriveKwargs(TypedDict, total=False):

    expr: 'PyExpr'

    dot: 'PyDot | None'

    name: 'PyIdent | str'


class PyAttrExpr(_PyBaseNode):

    _fields_ = ('expr', 'dot', 'name')

    def __init__(self, expr: 'PyExpr', name: 'PyIdent | str', *, dot: 'PyDot | None' = None) -> None:
        self.expr: PyExpr = _coerce_6(expr)
        self.dot: PyDot = _coerce_11(dot)
        self.name: PyIdent = _coerce_0(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyAttrExprDeriveKwargs]) -> 'PyAttrExpr':
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        dot = _coerce_11(kwargs['dot']) if 'dot' in kwargs else self.dot
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        return PyAttrExpr(expr=expr, dot=dot, name=name)

    @property
    def parent(self) -> 'PyAttrExprParent':
        assert(self._parent is not None)
        return cast(PyAttrExprParent, self._parent)


def is_py_attr_expr(value: Any) -> TypeIs[PyAttrExpr]:
    return isinstance(value, PyAttrExpr)


class PyAttrPatternDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    dot: 'PyDot | None'

    name: 'PyIdent | str'


class PyAttrPattern(_PyBaseNode):

    _fields_ = ('pattern', 'dot', 'name')

    def __init__(self, pattern: 'PyPattern', name: 'PyIdent | str', *, dot: 'PyDot | None' = None) -> None:
        self.pattern: PyPattern = _coerce_5(pattern)
        self.dot: PyDot = _coerce_11(dot)
        self.name: PyIdent = _coerce_0(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyAttrPatternDeriveKwargs]) -> 'PyAttrPattern':
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        dot = _coerce_11(kwargs['dot']) if 'dot' in kwargs else self.dot
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        return PyAttrPattern(pattern=pattern, dot=dot, name=name)

    @property
    def parent(self) -> 'PyAttrPatternParent':
        assert(self._parent is not None)
        return cast(PyAttrPatternParent, self._parent)


def is_py_attr_pattern(value: Any) -> TypeIs[PyAttrPattern]:
    return isinstance(value, PyAttrPattern)


class PyAugAssignStmtDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'

    op: 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyAugAssignStmt(_PyBaseNode):

    _fields_ = ('pattern', 'annotation', 'op', 'equals', 'expr')

    def __init__(self, pattern: 'PyPattern', op: 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar', expr: 'PyExpr', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, equals: 'PyEquals | None' = None) -> None:
        self.pattern: PyPattern = _coerce_5(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_8(annotation)
        self.op: PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar = _coerce_12(op)
        self.equals: PyEquals = _coerce_9(equals)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyAugAssignStmtDeriveKwargs]) -> 'PyAugAssignStmt':
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        annotation = _coerce_8(kwargs['annotation']) if 'annotation' in kwargs else self.annotation
        op = _coerce_12(kwargs['op']) if 'op' in kwargs else self.op
        equals = _coerce_9(kwargs['equals']) if 'equals' in kwargs else self.equals
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyAugAssignStmt(pattern=pattern, annotation=annotation, op=op, equals=equals, expr=expr)

    @property
    def parent(self) -> 'PyAugAssignStmtParent':
        assert(self._parent is not None)
        return cast(PyAugAssignStmtParent, self._parent)


def is_py_aug_assign_stmt(value: Any) -> TypeIs[PyAugAssignStmt]:
    return isinstance(value, PyAugAssignStmt)


class PyBreakStmtDeriveKwargs(TypedDict, total=False):

    break_keyword: 'PyBreakKeyword | None'


class PyBreakStmt(_PyBaseNode):

    _fields_ = ('break_keyword', )

    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None) -> None:
        self.break_keyword: PyBreakKeyword = _coerce_13(break_keyword)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyBreakStmtDeriveKwargs]) -> 'PyBreakStmt':
        break_keyword = _coerce_13(kwargs['break_keyword']) if 'break_keyword' in kwargs else self.break_keyword
        return PyBreakStmt(break_keyword=break_keyword)

    @property
    def parent(self) -> 'PyBreakStmtParent':
        assert(self._parent is not None)
        return cast(PyBreakStmtParent, self._parent)


def is_py_break_stmt(value: Any) -> TypeIs[PyBreakStmt]:
    return isinstance(value, PyBreakStmt)


class PyCallExprDeriveKwargs(TypedDict, total=False):

    operator: 'PyExpr'

    open_paren: 'PyOpenParen | None'

    args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | ImmutablePunct[PyArg, PyComma] | None'

    close_paren: 'PyCloseParen | None'


class PyCallExpr(_PyBaseNode):

    _fields_ = ('operator', 'open_paren', 'args', 'close_paren')

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, operator: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | ImmutablePunct[PyArg, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.operator: PyExpr = _coerce_6(operator)
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.args: Punctuated[PyArg, PyComma] = _coerce_17(args)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyCallExprDeriveKwargs]) -> 'PyCallExpr':
        operator = _coerce_6(kwargs['operator']) if 'operator' in kwargs else self.operator
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        args = _coerce_17(kwargs['args']) if 'args' in kwargs else self.args
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return PyCallExpr(operator=operator, open_paren=open_paren, args=args, close_paren=close_paren)

    @property
    def parent(self) -> 'PyCallExprParent':
        assert(self._parent is not None)
        return cast(PyCallExprParent, self._parent)


def is_py_call_expr(value: Any) -> TypeIs[PyCallExpr]:
    return isinstance(value, PyCallExpr)


class PyClassBaseArgDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'


class PyClassBaseArg(_PyBaseNode):

    _fields_ = ('name', )

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_0(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyClassBaseArgDeriveKwargs]) -> 'PyClassBaseArg':
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        return PyClassBaseArg(name=name)

    @property
    def parent(self) -> 'PyClassBaseArgParent':
        assert(self._parent is not None)
        return cast(PyClassBaseArgParent, self._parent)


def is_py_class_base_arg(value: Any) -> TypeIs[PyClassBaseArg]:
    return isinstance(value, PyClassBaseArg)


class PyClassDefDeriveKwargs(TypedDict, total=False):

    decorators: 'Sequence[PyDecorator | PyExpr] | None'

    class_keyword: 'PyClassKeyword | None'

    name: 'PyIdent | str'

    bases: 'tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyClassDef(_PyBaseNode):

    _fields_ = ('decorators', 'class_keyword', 'name', 'bases', 'colon', 'body')

    def count_decorators(self) -> int:
        return len(self.decorators)

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, class_keyword: 'PyClassKeyword | None' = None, bases: 'tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None' = None, colon: 'PyColon | None' = None) -> None:
        self.decorators: list[PyDecorator] = _coerce_20(decorators)
        self.class_keyword: PyClassKeyword = _coerce_21(class_keyword)
        self.name: PyIdent = _coerce_0(name)
        self.bases: tuple[PyOpenParen, Punctuated[PyBaseArg, PyComma], PyCloseParen] | None = _coerce_25(bases)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyClassDefDeriveKwargs]) -> 'PyClassDef':
        decorators = _coerce_20(kwargs['decorators']) if 'decorators' in kwargs else self.decorators
        class_keyword = _coerce_21(kwargs['class_keyword']) if 'class_keyword' in kwargs else self.class_keyword
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        bases = _coerce_25(kwargs['bases']) if 'bases' in kwargs else self.bases
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        return PyClassDef(decorators=decorators, class_keyword=class_keyword, name=name, bases=bases, colon=colon, body=body)

    @property
    def parent(self) -> 'PyClassDefParent':
        assert(self._parent is not None)
        return cast(PyClassDefParent, self._parent)


def is_py_class_def(value: Any) -> TypeIs[PyClassDef]:
    return isinstance(value, PyClassDef)


class PyComprehensionDeriveKwargs(TypedDict, total=False):

    async_keyword: 'PyAsyncKeyword | None'

    for_keyword: 'PyForKeyword | None'

    pattern: 'PyPattern'

    in_keyword: 'PyInKeyword | None'

    target: 'PyExpr'

    guards: 'Sequence[PyExpr | PyGuard] | None'


class PyComprehension(_PyBaseNode):

    _fields_ = ('async_keyword', 'for_keyword', 'pattern', 'in_keyword', 'target', 'guards')

    def count_guards(self) -> int:
        return len(self.guards)

    def __init__(self, pattern: 'PyPattern', target: 'PyExpr', *, async_keyword: 'PyAsyncKeyword | None' = None, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, guards: 'Sequence[PyExpr | PyGuard] | None' = None) -> None:
        self.async_keyword: PyAsyncKeyword | None = _coerce_28(async_keyword)
        self.for_keyword: PyForKeyword = _coerce_29(for_keyword)
        self.pattern: PyPattern = _coerce_5(pattern)
        self.in_keyword: PyInKeyword = _coerce_30(in_keyword)
        self.target: PyExpr = _coerce_6(target)
        self.guards: list[PyGuard] = _coerce_32(guards)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyComprehensionDeriveKwargs]) -> 'PyComprehension':
        async_keyword = _coerce_28(kwargs['async_keyword']) if 'async_keyword' in kwargs else self.async_keyword
        for_keyword = _coerce_29(kwargs['for_keyword']) if 'for_keyword' in kwargs else self.for_keyword
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        in_keyword = _coerce_30(kwargs['in_keyword']) if 'in_keyword' in kwargs else self.in_keyword
        target = _coerce_6(kwargs['target']) if 'target' in kwargs else self.target
        guards = _coerce_32(kwargs['guards']) if 'guards' in kwargs else self.guards
        return PyComprehension(async_keyword=async_keyword, for_keyword=for_keyword, pattern=pattern, in_keyword=in_keyword, target=target, guards=guards)

    @property
    def parent(self) -> 'PyComprehensionParent':
        assert(self._parent is not None)
        return cast(PyComprehensionParent, self._parent)


def is_py_comprehension(value: Any) -> TypeIs[PyComprehension]:
    return isinstance(value, PyComprehension)


class PyConstExprDeriveKwargs(TypedDict, total=False):

    literal: 'PyFloat | PyInteger | PyString | float | int | str'


class PyConstExpr(_PyBaseNode):

    _fields_ = ('literal', )

    def __init__(self, literal: 'PyFloat | PyInteger | PyString | float | int | str') -> None:
        self.literal: PyFloat | PyInteger | PyString = _coerce_33(literal)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyConstExprDeriveKwargs]) -> 'PyConstExpr':
        literal = _coerce_33(kwargs['literal']) if 'literal' in kwargs else self.literal
        return PyConstExpr(literal=literal)

    @property
    def parent(self) -> 'PyConstExprParent':
        assert(self._parent is not None)
        return cast(PyConstExprParent, self._parent)


def is_py_const_expr(value: Any) -> TypeIs[PyConstExpr]:
    return isinstance(value, PyConstExpr)


class PyContinueStmtDeriveKwargs(TypedDict, total=False):

    continue_keyword: 'PyContinueKeyword | None'


class PyContinueStmt(_PyBaseNode):

    _fields_ = ('continue_keyword', )

    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None) -> None:
        self.continue_keyword: PyContinueKeyword = _coerce_34(continue_keyword)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyContinueStmtDeriveKwargs]) -> 'PyContinueStmt':
        continue_keyword = _coerce_34(kwargs['continue_keyword']) if 'continue_keyword' in kwargs else self.continue_keyword
        return PyContinueStmt(continue_keyword=continue_keyword)

    @property
    def parent(self) -> 'PyContinueStmtParent':
        assert(self._parent is not None)
        return cast(PyContinueStmtParent, self._parent)


def is_py_continue_stmt(value: Any) -> TypeIs[PyContinueStmt]:
    return isinstance(value, PyContinueStmt)


class PyDecoratorDeriveKwargs(TypedDict, total=False):

    at_sign: 'PyAtSign | None'

    expr: 'PyExpr'


class PyDecorator(_PyBaseNode):

    _fields_ = ('at_sign', 'expr')

    def __init__(self, expr: 'PyExpr', *, at_sign: 'PyAtSign | None' = None) -> None:
        self.at_sign: PyAtSign = _coerce_35(at_sign)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyDecoratorDeriveKwargs]) -> 'PyDecorator':
        at_sign = _coerce_35(kwargs['at_sign']) if 'at_sign' in kwargs else self.at_sign
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyDecorator(at_sign=at_sign, expr=expr)

    @property
    def parent(self) -> 'PyDecoratorParent':
        assert(self._parent is not None)
        return cast(PyDecoratorParent, self._parent)


def is_py_decorator(value: Any) -> TypeIs[PyDecorator]:
    return isinstance(value, PyDecorator)


class PyDeleteStmtDeriveKwargs(TypedDict, total=False):

    del_keyword: 'PyDelKeyword | None'

    pattern: 'PyPattern'


class PyDeleteStmt(_PyBaseNode):

    _fields_ = ('del_keyword', 'pattern')

    def __init__(self, pattern: 'PyPattern', *, del_keyword: 'PyDelKeyword | None' = None) -> None:
        self.del_keyword: PyDelKeyword = _coerce_36(del_keyword)
        self.pattern: PyPattern = _coerce_5(pattern)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyDeleteStmtDeriveKwargs]) -> 'PyDeleteStmt':
        del_keyword = _coerce_36(kwargs['del_keyword']) if 'del_keyword' in kwargs else self.del_keyword
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        return PyDeleteStmt(del_keyword=del_keyword, pattern=pattern)

    @property
    def parent(self) -> 'PyDeleteStmtParent':
        assert(self._parent is not None)
        return cast(PyDeleteStmtParent, self._parent)


def is_py_delete_stmt(value: Any) -> TypeIs[PyDeleteStmt]:
    return isinstance(value, PyDeleteStmt)


class PyElifCaseDeriveKwargs(TypedDict, total=False):

    elif_keyword: 'PyElifKeyword | None'

    test: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyElifCase(_PyBaseNode):

    _fields_ = ('elif_keyword', 'test', 'colon', 'body')

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, elif_keyword: 'PyElifKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.elif_keyword: PyElifKeyword = _coerce_37(elif_keyword)
        self.test: PyExpr = _coerce_6(test)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyElifCaseDeriveKwargs]) -> 'PyElifCase':
        elif_keyword = _coerce_37(kwargs['elif_keyword']) if 'elif_keyword' in kwargs else self.elif_keyword
        test = _coerce_6(kwargs['test']) if 'test' in kwargs else self.test
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        return PyElifCase(elif_keyword=elif_keyword, test=test, colon=colon, body=body)

    @property
    def parent(self) -> 'PyElifCaseParent':
        assert(self._parent is not None)
        return cast(PyElifCaseParent, self._parent)


def is_py_elif_case(value: Any) -> TypeIs[PyElifCase]:
    return isinstance(value, PyElifCase)


class PyEllipsisExprDeriveKwargs(TypedDict, total=False):

    dot_dot_dot: 'PyDotDotDot | None'


class PyEllipsisExpr(_PyBaseNode):

    _fields_ = ('dot_dot_dot', )

    def __init__(self, *, dot_dot_dot: 'PyDotDotDot | None' = None) -> None:
        self.dot_dot_dot: PyDotDotDot = _coerce_38(dot_dot_dot)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyEllipsisExprDeriveKwargs]) -> 'PyEllipsisExpr':
        dot_dot_dot = _coerce_38(kwargs['dot_dot_dot']) if 'dot_dot_dot' in kwargs else self.dot_dot_dot
        return PyEllipsisExpr(dot_dot_dot=dot_dot_dot)

    @property
    def parent(self) -> 'PyEllipsisExprParent':
        assert(self._parent is not None)
        return cast(PyEllipsisExprParent, self._parent)


def is_py_ellipsis_expr(value: Any) -> TypeIs[PyEllipsisExpr]:
    return isinstance(value, PyEllipsisExpr)


class PyElseCaseDeriveKwargs(TypedDict, total=False):

    else_keyword: 'PyElseKeyword | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyElseCase(_PyBaseNode):

    _fields_ = ('else_keyword', 'colon', 'body')

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.else_keyword: PyElseKeyword = _coerce_39(else_keyword)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyElseCaseDeriveKwargs]) -> 'PyElseCase':
        else_keyword = _coerce_39(kwargs['else_keyword']) if 'else_keyword' in kwargs else self.else_keyword
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        return PyElseCase(else_keyword=else_keyword, colon=colon, body=body)

    @property
    def parent(self) -> 'PyElseCaseParent':
        assert(self._parent is not None)
        return cast(PyElseCaseParent, self._parent)


def is_py_else_case(value: Any) -> TypeIs[PyElseCase]:
    return isinstance(value, PyElseCase)


class PyExceptHandlerDeriveKwargs(TypedDict, total=False):

    except_keyword: 'PyExceptKeyword | None'

    expr: 'PyExpr'

    binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyExceptHandler(_PyBaseNode):

    _fields_ = ('except_keyword', 'expr', 'binder', 'colon', 'body')

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, except_keyword: 'PyExceptKeyword | None' = None, binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None, colon: 'PyColon | None' = None) -> None:
        self.except_keyword: PyExceptKeyword = _coerce_40(except_keyword)
        self.expr: PyExpr = _coerce_6(expr)
        self.binder: tuple[PyAsKeyword, PyIdent] | None = _coerce_4(binder)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyExceptHandlerDeriveKwargs]) -> 'PyExceptHandler':
        except_keyword = _coerce_40(kwargs['except_keyword']) if 'except_keyword' in kwargs else self.except_keyword
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        binder = _coerce_4(kwargs['binder']) if 'binder' in kwargs else self.binder
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        return PyExceptHandler(except_keyword=except_keyword, expr=expr, binder=binder, colon=colon, body=body)

    @property
    def parent(self) -> 'PyExceptHandlerParent':
        assert(self._parent is not None)
        return cast(PyExceptHandlerParent, self._parent)


def is_py_except_handler(value: Any) -> TypeIs[PyExceptHandler]:
    return isinstance(value, PyExceptHandler)


class PyExprSliceDeriveKwargs(TypedDict, total=False):

    lower: 'PyExpr | None'

    colon: 'PyColon | None'

    upper: 'PyExpr | None'

    step: 'PyExpr | tuple[PyColon | None, PyExpr] | None'


class PyExprSlice(_PyBaseNode):

    _fields_ = ('lower', 'colon', 'upper', 'step')

    def __init__(self, *, lower: 'PyExpr | None' = None, colon: 'PyColon | None' = None, upper: 'PyExpr | None' = None, step: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.lower: PyExpr | None = _coerce_41(lower)
        self.colon: PyColon = _coerce_7(colon)
        self.upper: PyExpr | None = _coerce_41(upper)
        self.step: tuple[PyColon, PyExpr] | None = _coerce_8(step)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyExprSliceDeriveKwargs]) -> 'PyExprSlice':
        lower = _coerce_41(kwargs['lower']) if 'lower' in kwargs else self.lower
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        upper = _coerce_41(kwargs['upper']) if 'upper' in kwargs else self.upper
        step = _coerce_8(kwargs['step']) if 'step' in kwargs else self.step
        return PyExprSlice(lower=lower, colon=colon, upper=upper, step=step)

    @property
    def parent(self) -> 'PyExprSliceParent':
        assert(self._parent is not None)
        return cast(PyExprSliceParent, self._parent)


def is_py_expr_slice(value: Any) -> TypeIs[PyExprSlice]:
    return isinstance(value, PyExprSlice)


class PyExprStmtDeriveKwargs(TypedDict, total=False):

    expr: 'PyExpr'


class PyExprStmt(_PyBaseNode):

    _fields_ = ('expr', )

    def __init__(self, expr: 'PyExpr') -> None:
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyExprStmtDeriveKwargs]) -> 'PyExprStmt':
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyExprStmt(expr=expr)

    @property
    def parent(self) -> 'PyExprStmtParent':
        assert(self._parent is not None)
        return cast(PyExprStmtParent, self._parent)


def is_py_expr_stmt(value: Any) -> TypeIs[PyExprStmt]:
    return isinstance(value, PyExprStmt)


class PyForStmtDeriveKwargs(TypedDict, total=False):

    for_keyword: 'PyForKeyword | None'

    pattern: 'PyPattern'

    in_keyword: 'PyInKeyword | None'

    expr: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'

    else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'


class PyForStmt(_PyBaseNode):

    _fields_ = ('for_keyword', 'pattern', 'in_keyword', 'expr', 'colon', 'body', 'else_clause')

    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.for_keyword: PyForKeyword = _coerce_29(for_keyword)
        self.pattern: PyPattern = _coerce_5(pattern)
        self.in_keyword: PyInKeyword = _coerce_30(in_keyword)
        self.expr: PyExpr = _coerce_6(expr)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = _coerce_42(else_clause)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyForStmtDeriveKwargs]) -> 'PyForStmt':
        for_keyword = _coerce_29(kwargs['for_keyword']) if 'for_keyword' in kwargs else self.for_keyword
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        in_keyword = _coerce_30(kwargs['in_keyword']) if 'in_keyword' in kwargs else self.in_keyword
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        else_clause = _coerce_42(kwargs['else_clause']) if 'else_clause' in kwargs else self.else_clause
        return PyForStmt(for_keyword=for_keyword, pattern=pattern, in_keyword=in_keyword, expr=expr, colon=colon, body=body, else_clause=else_clause)

    @property
    def parent(self) -> 'PyForStmtParent':
        assert(self._parent is not None)
        return cast(PyForStmtParent, self._parent)


def is_py_for_stmt(value: Any) -> TypeIs[PyForStmt]:
    return isinstance(value, PyForStmt)


class PyFromAliasDeriveKwargs(TypedDict, total=False):

    name: 'PyAsterisk | PyIdent | str'

    asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str'


class PyFromAlias(_PyBaseNode):

    _fields_ = ('name', 'asname')

    def __init__(self, name: 'PyAsterisk | PyIdent | str', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> None:
        self.name: PyAsterisk | PyIdent = _coerce_43(name)
        self.asname: tuple[PyAsKeyword, PyIdent] | None = _coerce_4(asname)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyFromAliasDeriveKwargs]) -> 'PyFromAlias':
        name = _coerce_43(kwargs['name']) if 'name' in kwargs else self.name
        asname = _coerce_4(kwargs['asname']) if 'asname' in kwargs else self.asname
        return PyFromAlias(name=name, asname=asname)

    @property
    def parent(self) -> 'PyFromAliasParent':
        assert(self._parent is not None)
        return cast(PyFromAliasParent, self._parent)


def is_py_from_alias(value: Any) -> TypeIs[PyFromAlias]:
    return isinstance(value, PyFromAlias)


class PyFuncDefDeriveKwargs(TypedDict, total=False):

    decorators: 'Sequence[PyDecorator | PyExpr] | None'

    async_keyword: 'PyAsyncKeyword | None'

    def_keyword: 'PyDefKeyword | None'

    name: 'PyIdent | str'

    open_paren: 'PyOpenParen | None'

    params: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | ImmutablePunct[PyParam, PyComma] | None'

    close_paren: 'PyCloseParen | None'

    return_type: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyFuncDef(_PyBaseNode):

    _fields_ = ('decorators', 'async_keyword', 'def_keyword', 'name', 'open_paren', 'params', 'close_paren', 'return_type', 'colon', 'body')

    def count_decorators(self) -> int:
        return len(self.decorators)

    def count_params(self) -> int:
        return len(self.params)

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, open_paren: 'PyOpenParen | None' = None, params: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | ImmutablePunct[PyParam, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None' = None, colon: 'PyColon | None' = None) -> None:
        self.decorators: list[PyDecorator] = _coerce_20(decorators)
        self.async_keyword: PyAsyncKeyword | None = _coerce_28(async_keyword)
        self.def_keyword: PyDefKeyword = _coerce_44(def_keyword)
        self.name: PyIdent = _coerce_0(name)
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.params: Punctuated[PyParam, PyComma] = _coerce_46(params)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)
        self.return_type: tuple[PyRArrow, PyExpr] | None = _coerce_48(return_type)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyFuncDefDeriveKwargs]) -> 'PyFuncDef':
        decorators = _coerce_20(kwargs['decorators']) if 'decorators' in kwargs else self.decorators
        async_keyword = _coerce_28(kwargs['async_keyword']) if 'async_keyword' in kwargs else self.async_keyword
        def_keyword = _coerce_44(kwargs['def_keyword']) if 'def_keyword' in kwargs else self.def_keyword
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        params = _coerce_46(kwargs['params']) if 'params' in kwargs else self.params
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return_type = _coerce_48(kwargs['return_type']) if 'return_type' in kwargs else self.return_type
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        return PyFuncDef(decorators=decorators, async_keyword=async_keyword, def_keyword=def_keyword, name=name, open_paren=open_paren, params=params, close_paren=close_paren, return_type=return_type, colon=colon, body=body)

    @property
    def parent(self) -> 'PyFuncDefParent':
        assert(self._parent is not None)
        return cast(PyFuncDefParent, self._parent)


def is_py_func_def(value: Any) -> TypeIs[PyFuncDef]:
    return isinstance(value, PyFuncDef)


class PyGeneratorExprDeriveKwargs(TypedDict, total=False):

    element: 'PyExpr'

    generators: 'Sequence[PyComprehension]'


class PyGeneratorExpr(_PyBaseNode):

    _fields_ = ('element', 'generators')

    def count_generators(self) -> int:
        return len(self.generators)

    def __init__(self, element: 'PyExpr', generators: 'Sequence[PyComprehension]') -> None:
        self.element: PyExpr = _coerce_6(element)
        self.generators: list[PyComprehension] = _coerce_50(generators)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyGeneratorExprDeriveKwargs]) -> 'PyGeneratorExpr':
        element = _coerce_6(kwargs['element']) if 'element' in kwargs else self.element
        generators = _coerce_50(kwargs['generators']) if 'generators' in kwargs else self.generators
        return PyGeneratorExpr(element=element, generators=generators)

    @property
    def parent(self) -> 'PyGeneratorExprParent':
        assert(self._parent is not None)
        return cast(PyGeneratorExprParent, self._parent)


def is_py_generator_expr(value: Any) -> TypeIs[PyGeneratorExpr]:
    return isinstance(value, PyGeneratorExpr)


class PyGlobalStmtDeriveKwargs(TypedDict, total=False):

    global_keyword: 'PyGlobalKeyword | None'

    names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | ImmutablePunct[PyIdent | str, PyComma]'


class PyGlobalStmt(_PyBaseNode):

    _fields_ = ('global_keyword', 'names')

    def count_names(self) -> int:
        return len(self.names)

    def __init__(self, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | ImmutablePunct[PyIdent | str, PyComma]', *, global_keyword: 'PyGlobalKeyword | None' = None) -> None:
        self.global_keyword: PyGlobalKeyword = _coerce_51(global_keyword)
        self.names: Punctuated[PyIdent, PyComma] = _coerce_52(names)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyGlobalStmtDeriveKwargs]) -> 'PyGlobalStmt':
        global_keyword = _coerce_51(kwargs['global_keyword']) if 'global_keyword' in kwargs else self.global_keyword
        names = _coerce_52(kwargs['names']) if 'names' in kwargs else self.names
        return PyGlobalStmt(global_keyword=global_keyword, names=names)

    @property
    def parent(self) -> 'PyGlobalStmtParent':
        assert(self._parent is not None)
        return cast(PyGlobalStmtParent, self._parent)


def is_py_global_stmt(value: Any) -> TypeIs[PyGlobalStmt]:
    return isinstance(value, PyGlobalStmt)


class PyGuardDeriveKwargs(TypedDict, total=False):

    if_keyword: 'PyIfKeyword | None'

    expr: 'PyExpr'


class PyGuard(_PyBaseNode):

    _fields_ = ('if_keyword', 'expr')

    def __init__(self, expr: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None) -> None:
        self.if_keyword: PyIfKeyword = _coerce_53(if_keyword)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyGuardDeriveKwargs]) -> 'PyGuard':
        if_keyword = _coerce_53(kwargs['if_keyword']) if 'if_keyword' in kwargs else self.if_keyword
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyGuard(if_keyword=if_keyword, expr=expr)

    @property
    def parent(self) -> 'PyGuardParent':
        assert(self._parent is not None)
        return cast(PyGuardParent, self._parent)


def is_py_guard(value: Any) -> TypeIs[PyGuard]:
    return isinstance(value, PyGuard)


class PyIfCaseDeriveKwargs(TypedDict, total=False):

    if_keyword: 'PyIfKeyword | None'

    test: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyIfCase(_PyBaseNode):

    _fields_ = ('if_keyword', 'test', 'colon', 'body')

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, if_keyword: 'PyIfKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.if_keyword: PyIfKeyword = _coerce_53(if_keyword)
        self.test: PyExpr = _coerce_6(test)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyIfCaseDeriveKwargs]) -> 'PyIfCase':
        if_keyword = _coerce_53(kwargs['if_keyword']) if 'if_keyword' in kwargs else self.if_keyword
        test = _coerce_6(kwargs['test']) if 'test' in kwargs else self.test
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        return PyIfCase(if_keyword=if_keyword, test=test, colon=colon, body=body)

    @property
    def parent(self) -> 'PyIfCaseParent':
        assert(self._parent is not None)
        return cast(PyIfCaseParent, self._parent)


def is_py_if_case(value: Any) -> TypeIs[PyIfCase]:
    return isinstance(value, PyIfCase)


class PyIfExprDeriveKwargs(TypedDict, total=False):

    then: 'PyExpr'

    if_keyword: 'PyIfKeyword | None'

    test: 'PyExpr'

    else_keyword: 'PyElseKeyword | None'

    alt: 'PyExpr'


class PyIfExpr(_PyBaseNode):

    _fields_ = ('then', 'if_keyword', 'test', 'else_keyword', 'alt')

    def __init__(self, then: 'PyExpr', test: 'PyExpr', alt: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None, else_keyword: 'PyElseKeyword | None' = None) -> None:
        self.then: PyExpr = _coerce_6(then)
        self.if_keyword: PyIfKeyword = _coerce_53(if_keyword)
        self.test: PyExpr = _coerce_6(test)
        self.else_keyword: PyElseKeyword = _coerce_39(else_keyword)
        self.alt: PyExpr = _coerce_6(alt)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyIfExprDeriveKwargs]) -> 'PyIfExpr':
        then = _coerce_6(kwargs['then']) if 'then' in kwargs else self.then
        if_keyword = _coerce_53(kwargs['if_keyword']) if 'if_keyword' in kwargs else self.if_keyword
        test = _coerce_6(kwargs['test']) if 'test' in kwargs else self.test
        else_keyword = _coerce_39(kwargs['else_keyword']) if 'else_keyword' in kwargs else self.else_keyword
        alt = _coerce_6(kwargs['alt']) if 'alt' in kwargs else self.alt
        return PyIfExpr(then=then, if_keyword=if_keyword, test=test, else_keyword=else_keyword, alt=alt)

    @property
    def parent(self) -> 'PyIfExprParent':
        assert(self._parent is not None)
        return cast(PyIfExprParent, self._parent)


def is_py_if_expr(value: Any) -> TypeIs[PyIfExpr]:
    return isinstance(value, PyIfExpr)


class PyIfStmtDeriveKwargs(TypedDict, total=False):

    first: 'PyIfCase'

    alternatives: 'Sequence[PyElifCase] | None'

    last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None'


class PyIfStmt(_PyBaseNode):

    _fields_ = ('first', 'alternatives', 'last')

    def count_alternatives(self) -> int:
        return len(self.alternatives)

    def __init__(self, first: 'PyIfCase', *, alternatives: 'Sequence[PyElifCase] | None' = None, last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None' = None) -> None:
        self.first: PyIfCase = _coerce_54(first)
        self.alternatives: list[PyElifCase] = _coerce_56(alternatives)
        self.last: PyElseCase | None = _coerce_57(last)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyIfStmtDeriveKwargs]) -> 'PyIfStmt':
        first = _coerce_54(kwargs['first']) if 'first' in kwargs else self.first
        alternatives = _coerce_56(kwargs['alternatives']) if 'alternatives' in kwargs else self.alternatives
        last = _coerce_57(kwargs['last']) if 'last' in kwargs else self.last
        return PyIfStmt(first=first, alternatives=alternatives, last=last)

    @property
    def parent(self) -> 'PyIfStmtParent':
        assert(self._parent is not None)
        return cast(PyIfStmtParent, self._parent)


def is_py_if_stmt(value: Any) -> TypeIs[PyIfStmt]:
    return isinstance(value, PyIfStmt)


class PyImportFromStmtDeriveKwargs(TypedDict, total=False):

    from_keyword: 'PyFromKeyword | None'

    path: 'PyPath'

    import_keyword: 'PyImportKeyword | None'

    aliases: 'Sequence[tuple[PyAsterisk | PyFromAlias | PyIdent | str, PyComma | None]] | Sequence[PyAsterisk | PyFromAlias | PyIdent | str] | ImmutablePunct[PyAsterisk | PyFromAlias | PyIdent | str, PyComma]'


class PyImportFromStmt(_PyBaseNode):

    _fields_ = ('from_keyword', 'path', 'import_keyword', 'aliases')

    def count_aliases(self) -> int:
        return len(self.aliases)

    def __init__(self, path: 'PyPath', aliases: 'Sequence[tuple[PyAsterisk | PyFromAlias | PyIdent | str, PyComma | None]] | Sequence[PyAsterisk | PyFromAlias | PyIdent | str] | ImmutablePunct[PyAsterisk | PyFromAlias | PyIdent | str, PyComma]', *, from_keyword: 'PyFromKeyword | None' = None, import_keyword: 'PyImportKeyword | None' = None) -> None:
        self.from_keyword: PyFromKeyword = _coerce_58(from_keyword)
        self.path: PyPath = _coerce_2(path)
        self.import_keyword: PyImportKeyword = _coerce_59(import_keyword)
        self.aliases: Punctuated[PyFromAlias, PyComma] = _coerce_61(aliases)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyImportFromStmtDeriveKwargs]) -> 'PyImportFromStmt':
        from_keyword = _coerce_58(kwargs['from_keyword']) if 'from_keyword' in kwargs else self.from_keyword
        path = _coerce_2(kwargs['path']) if 'path' in kwargs else self.path
        import_keyword = _coerce_59(kwargs['import_keyword']) if 'import_keyword' in kwargs else self.import_keyword
        aliases = _coerce_61(kwargs['aliases']) if 'aliases' in kwargs else self.aliases
        return PyImportFromStmt(from_keyword=from_keyword, path=path, import_keyword=import_keyword, aliases=aliases)

    @property
    def parent(self) -> 'PyImportFromStmtParent':
        assert(self._parent is not None)
        return cast(PyImportFromStmtParent, self._parent)


def is_py_import_from_stmt(value: Any) -> TypeIs[PyImportFromStmt]:
    return isinstance(value, PyImportFromStmt)


class PyImportStmtDeriveKwargs(TypedDict, total=False):

    import_keyword: 'PyImportKeyword | None'

    aliases: 'Sequence[tuple[PyAlias | PyPath, PyComma | None]] | Sequence[PyAlias | PyPath] | ImmutablePunct[PyAlias | PyPath, PyComma]'


class PyImportStmt(_PyBaseNode):

    _fields_ = ('import_keyword', 'aliases')

    def count_aliases(self) -> int:
        return len(self.aliases)

    def __init__(self, aliases: 'Sequence[tuple[PyAlias | PyPath, PyComma | None]] | Sequence[PyAlias | PyPath] | ImmutablePunct[PyAlias | PyPath, PyComma]', *, import_keyword: 'PyImportKeyword | None' = None) -> None:
        self.import_keyword: PyImportKeyword = _coerce_59(import_keyword)
        self.aliases: Punctuated[PyAlias, PyComma] = _coerce_63(aliases)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyImportStmtDeriveKwargs]) -> 'PyImportStmt':
        import_keyword = _coerce_59(kwargs['import_keyword']) if 'import_keyword' in kwargs else self.import_keyword
        aliases = _coerce_63(kwargs['aliases']) if 'aliases' in kwargs else self.aliases
        return PyImportStmt(import_keyword=import_keyword, aliases=aliases)

    @property
    def parent(self) -> 'PyImportStmtParent':
        assert(self._parent is not None)
        return cast(PyImportStmtParent, self._parent)


def is_py_import_stmt(value: Any) -> TypeIs[PyImportStmt]:
    return isinstance(value, PyImportStmt)


class PyInfixExprDeriveKwargs(TypedDict, total=False):

    left: 'PyExpr'

    op: 'PyInfixOp'

    right: 'PyExpr'


class PyInfixExpr(_PyBaseNode):

    _fields_ = ('left', 'op', 'right')

    def __init__(self, left: 'PyExpr', op: 'PyInfixOp', right: 'PyExpr') -> None:
        self.left: PyExpr = _coerce_6(left)
        self.op: PyInfixOp = _coerce_64(op)
        self.right: PyExpr = _coerce_6(right)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyInfixExprDeriveKwargs]) -> 'PyInfixExpr':
        left = _coerce_6(kwargs['left']) if 'left' in kwargs else self.left
        op = _coerce_64(kwargs['op']) if 'op' in kwargs else self.op
        right = _coerce_6(kwargs['right']) if 'right' in kwargs else self.right
        return PyInfixExpr(left=left, op=op, right=right)

    @property
    def parent(self) -> 'PyInfixExprParent':
        assert(self._parent is not None)
        return cast(PyInfixExprParent, self._parent)


def is_py_infix_expr(value: Any) -> TypeIs[PyInfixExpr]:
    return isinstance(value, PyInfixExpr)


class PyKeywordArgDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyKeywordArg(_PyBaseNode):

    _fields_ = ('name', 'equals', 'expr')

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        self.name: PyIdent = _coerce_0(name)
        self.equals: PyEquals = _coerce_9(equals)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyKeywordArgDeriveKwargs]) -> 'PyKeywordArg':
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        equals = _coerce_9(kwargs['equals']) if 'equals' in kwargs else self.equals
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyKeywordArg(name=name, equals=equals, expr=expr)

    @property
    def parent(self) -> 'PyKeywordArgParent':
        assert(self._parent is not None)
        return cast(PyKeywordArgParent, self._parent)


def is_py_keyword_arg(value: Any) -> TypeIs[PyKeywordArg]:
    return isinstance(value, PyKeywordArg)


class PyKeywordBaseArgDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyKeywordBaseArg(_PyBaseNode):

    _fields_ = ('name', 'equals', 'expr')

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        self.name: PyIdent = _coerce_0(name)
        self.equals: PyEquals = _coerce_9(equals)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyKeywordBaseArgDeriveKwargs]) -> 'PyKeywordBaseArg':
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        equals = _coerce_9(kwargs['equals']) if 'equals' in kwargs else self.equals
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyKeywordBaseArg(name=name, equals=equals, expr=expr)

    @property
    def parent(self) -> 'PyKeywordBaseArgParent':
        assert(self._parent is not None)
        return cast(PyKeywordBaseArgParent, self._parent)


def is_py_keyword_base_arg(value: Any) -> TypeIs[PyKeywordBaseArg]:
    return isinstance(value, PyKeywordBaseArg)


class PyKwSepParamDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'


class PyKwSepParam(_PyBaseNode):

    _fields_ = ('asterisk', )

    def __init__(self, *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_65(asterisk)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyKwSepParamDeriveKwargs]) -> 'PyKwSepParam':
        asterisk = _coerce_65(kwargs['asterisk']) if 'asterisk' in kwargs else self.asterisk
        return PyKwSepParam(asterisk=asterisk)

    @property
    def parent(self) -> 'PyKwSepParamParent':
        assert(self._parent is not None)
        return cast(PyKwSepParamParent, self._parent)


def is_py_kw_sep_param(value: Any) -> TypeIs[PyKwSepParam]:
    return isinstance(value, PyKwSepParam)


class PyLambdaExprDeriveKwargs(TypedDict, total=False):

    lambda_keyword: 'PyLambdaKeyword | None'

    params: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None'

    colon: 'PyColon | None'

    expr: 'PyExpr'


class PyLambdaExpr(_PyBaseNode):

    _fields_ = ('lambda_keyword', 'params', 'colon', 'expr')

    def count_params(self) -> int:
        return len(self.params)

    def __init__(self, expr: 'PyExpr', *, lambda_keyword: 'PyLambdaKeyword | None' = None, params: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None' = None, colon: 'PyColon | None' = None) -> None:
        self.lambda_keyword: PyLambdaKeyword = _coerce_66(lambda_keyword)
        self.params: Punctuated[PyPattern, PyComma] = _coerce_67(params)
        self.colon: PyColon = _coerce_7(colon)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyLambdaExprDeriveKwargs]) -> 'PyLambdaExpr':
        lambda_keyword = _coerce_66(kwargs['lambda_keyword']) if 'lambda_keyword' in kwargs else self.lambda_keyword
        params = _coerce_67(kwargs['params']) if 'params' in kwargs else self.params
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyLambdaExpr(lambda_keyword=lambda_keyword, params=params, colon=colon, expr=expr)

    @property
    def parent(self) -> 'PyLambdaExprParent':
        assert(self._parent is not None)
        return cast(PyLambdaExprParent, self._parent)


def is_py_lambda_expr(value: Any) -> TypeIs[PyLambdaExpr]:
    return isinstance(value, PyLambdaExpr)


class PyListExprDeriveKwargs(TypedDict, total=False):

    open_bracket: 'PyOpenBracket | None'

    elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None'

    close_bracket: 'PyCloseBracket | None'


class PyListExpr(_PyBaseNode):

    _fields_ = ('open_bracket', 'elements', 'close_bracket')

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.open_bracket: PyOpenBracket = _coerce_68(open_bracket)
        self.elements: Punctuated[PyExpr, PyComma] = _coerce_69(elements)
        self.close_bracket: PyCloseBracket = _coerce_70(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyListExprDeriveKwargs]) -> 'PyListExpr':
        open_bracket = _coerce_68(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        elements = _coerce_69(kwargs['elements']) if 'elements' in kwargs else self.elements
        close_bracket = _coerce_70(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return PyListExpr(open_bracket=open_bracket, elements=elements, close_bracket=close_bracket)

    @property
    def parent(self) -> 'PyListExprParent':
        assert(self._parent is not None)
        return cast(PyListExprParent, self._parent)


def is_py_list_expr(value: Any) -> TypeIs[PyListExpr]:
    return isinstance(value, PyListExpr)


class PyListPatternDeriveKwargs(TypedDict, total=False):

    open_bracket: 'PyOpenBracket | None'

    elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None'

    close_bracket: 'PyCloseBracket | None'


class PyListPattern(_PyBaseNode):

    _fields_ = ('open_bracket', 'elements', 'close_bracket')

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.open_bracket: PyOpenBracket = _coerce_68(open_bracket)
        self.elements: Punctuated[PyPattern, PyComma] = _coerce_67(elements)
        self.close_bracket: PyCloseBracket = _coerce_70(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyListPatternDeriveKwargs]) -> 'PyListPattern':
        open_bracket = _coerce_68(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        elements = _coerce_67(kwargs['elements']) if 'elements' in kwargs else self.elements
        close_bracket = _coerce_70(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return PyListPattern(open_bracket=open_bracket, elements=elements, close_bracket=close_bracket)

    @property
    def parent(self) -> 'PyListPatternParent':
        assert(self._parent is not None)
        return cast(PyListPatternParent, self._parent)


def is_py_list_pattern(value: Any) -> TypeIs[PyListPattern]:
    return isinstance(value, PyListPattern)


class PyModuleDeriveKwargs(TypedDict, total=False):

    stmts: 'Sequence[PyStmt] | None'


class PyModule(_PyBaseNode):

    _fields_ = ('stmts', )

    def count_stmts(self) -> int:
        return len(self.stmts)

    def __init__(self, *, stmts: 'Sequence[PyStmt] | None' = None) -> None:
        self.stmts: list[PyStmt] = _coerce_71(stmts)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyModuleDeriveKwargs]) -> 'PyModule':
        stmts = _coerce_71(kwargs['stmts']) if 'stmts' in kwargs else self.stmts
        return PyModule(stmts=stmts)

    @property
    def parent(self) -> 'PyModuleParent':
        raise AssertionError('trying to access the parent node of a top-level node')


def is_py_module(value: Any) -> TypeIs[PyModule]:
    return isinstance(value, PyModule)


class PyNamedExprDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'


class PyNamedExpr(_PyBaseNode):

    _fields_ = ('name', )

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_0(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyNamedExprDeriveKwargs]) -> 'PyNamedExpr':
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        return PyNamedExpr(name=name)

    @property
    def parent(self) -> 'PyNamedExprParent':
        assert(self._parent is not None)
        return cast(PyNamedExprParent, self._parent)


def is_py_named_expr(value: Any) -> TypeIs[PyNamedExpr]:
    return isinstance(value, PyNamedExpr)


class PyNamedParamDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'

    default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None'


class PyNamedParam(_PyBaseNode):

    _fields_ = ('pattern', 'annotation', 'default')

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = _coerce_5(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_8(annotation)
        self.default: tuple[PyEquals, PyExpr] | None = _coerce_10(default)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyNamedParamDeriveKwargs]) -> 'PyNamedParam':
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        annotation = _coerce_8(kwargs['annotation']) if 'annotation' in kwargs else self.annotation
        default = _coerce_10(kwargs['default']) if 'default' in kwargs else self.default
        return PyNamedParam(pattern=pattern, annotation=annotation, default=default)

    @property
    def parent(self) -> 'PyNamedParamParent':
        assert(self._parent is not None)
        return cast(PyNamedParamParent, self._parent)


def is_py_named_param(value: Any) -> TypeIs[PyNamedParam]:
    return isinstance(value, PyNamedParam)


class PyNamedPatternDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'


class PyNamedPattern(_PyBaseNode):

    _fields_ = ('name', )

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_0(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyNamedPatternDeriveKwargs]) -> 'PyNamedPattern':
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        return PyNamedPattern(name=name)

    @property
    def parent(self) -> 'PyNamedPatternParent':
        assert(self._parent is not None)
        return cast(PyNamedPatternParent, self._parent)


def is_py_named_pattern(value: Any) -> TypeIs[PyNamedPattern]:
    return isinstance(value, PyNamedPattern)


class PyNestExprDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    expr: 'PyExpr'

    close_paren: 'PyCloseParen | None'


class PyNestExpr(_PyBaseNode):

    _fields_ = ('open_paren', 'expr', 'close_paren')

    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.expr: PyExpr = _coerce_6(expr)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyNestExprDeriveKwargs]) -> 'PyNestExpr':
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return PyNestExpr(open_paren=open_paren, expr=expr, close_paren=close_paren)

    @property
    def parent(self) -> 'PyNestExprParent':
        assert(self._parent is not None)
        return cast(PyNestExprParent, self._parent)


def is_py_nest_expr(value: Any) -> TypeIs[PyNestExpr]:
    return isinstance(value, PyNestExpr)


class PyNonlocalStmtDeriveKwargs(TypedDict, total=False):

    nonlocal_keyword: 'PyNonlocalKeyword | None'

    names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | ImmutablePunct[PyIdent | str, PyComma]'


class PyNonlocalStmt(_PyBaseNode):

    _fields_ = ('nonlocal_keyword', 'names')

    def count_names(self) -> int:
        return len(self.names)

    def __init__(self, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | ImmutablePunct[PyIdent | str, PyComma]', *, nonlocal_keyword: 'PyNonlocalKeyword | None' = None) -> None:
        self.nonlocal_keyword: PyNonlocalKeyword = _coerce_72(nonlocal_keyword)
        self.names: Punctuated[PyIdent, PyComma] = _coerce_52(names)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyNonlocalStmtDeriveKwargs]) -> 'PyNonlocalStmt':
        nonlocal_keyword = _coerce_72(kwargs['nonlocal_keyword']) if 'nonlocal_keyword' in kwargs else self.nonlocal_keyword
        names = _coerce_52(kwargs['names']) if 'names' in kwargs else self.names
        return PyNonlocalStmt(nonlocal_keyword=nonlocal_keyword, names=names)

    @property
    def parent(self) -> 'PyNonlocalStmtParent':
        assert(self._parent is not None)
        return cast(PyNonlocalStmtParent, self._parent)


def is_py_nonlocal_stmt(value: Any) -> TypeIs[PyNonlocalStmt]:
    return isinstance(value, PyNonlocalStmt)


class PyPassStmtDeriveKwargs(TypedDict, total=False):

    pass_keyword: 'PyPassKeyword | None'


class PyPassStmt(_PyBaseNode):

    _fields_ = ('pass_keyword', )

    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None) -> None:
        self.pass_keyword: PyPassKeyword = _coerce_73(pass_keyword)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyPassStmtDeriveKwargs]) -> 'PyPassStmt':
        pass_keyword = _coerce_73(kwargs['pass_keyword']) if 'pass_keyword' in kwargs else self.pass_keyword
        return PyPassStmt(pass_keyword=pass_keyword)

    @property
    def parent(self) -> 'PyPassStmtParent':
        assert(self._parent is not None)
        return cast(PyPassStmtParent, self._parent)


def is_py_pass_stmt(value: Any) -> TypeIs[PyPassStmt]:
    return isinstance(value, PyPassStmt)


class PyPatternSliceDeriveKwargs(TypedDict, total=False):

    lower: 'PyPattern | None'

    colon: 'PyColon | None'

    upper: 'PyPattern | None'

    step: 'PyPattern | tuple[PyColon | None, PyPattern] | None'


class PyPatternSlice(_PyBaseNode):

    _fields_ = ('lower', 'colon', 'upper', 'step')

    def __init__(self, *, lower: 'PyPattern | None' = None, colon: 'PyColon | None' = None, upper: 'PyPattern | None' = None, step: 'PyPattern | tuple[PyColon | None, PyPattern] | None' = None) -> None:
        self.lower: PyPattern | None = _coerce_74(lower)
        self.colon: PyColon = _coerce_7(colon)
        self.upper: PyPattern | None = _coerce_74(upper)
        self.step: tuple[PyColon, PyPattern] | None = _coerce_75(step)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyPatternSliceDeriveKwargs]) -> 'PyPatternSlice':
        lower = _coerce_74(kwargs['lower']) if 'lower' in kwargs else self.lower
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        upper = _coerce_74(kwargs['upper']) if 'upper' in kwargs else self.upper
        step = _coerce_75(kwargs['step']) if 'step' in kwargs else self.step
        return PyPatternSlice(lower=lower, colon=colon, upper=upper, step=step)

    @property
    def parent(self) -> 'PyPatternSliceParent':
        assert(self._parent is not None)
        return cast(PyPatternSliceParent, self._parent)


def is_py_pattern_slice(value: Any) -> TypeIs[PyPatternSlice]:
    return isinstance(value, PyPatternSlice)


class PyPosSepParamDeriveKwargs(TypedDict, total=False):

    slash: 'PySlash | None'


class PyPosSepParam(_PyBaseNode):

    _fields_ = ('slash', )

    def __init__(self, *, slash: 'PySlash | None' = None) -> None:
        self.slash: PySlash = _coerce_76(slash)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyPosSepParamDeriveKwargs]) -> 'PyPosSepParam':
        slash = _coerce_76(kwargs['slash']) if 'slash' in kwargs else self.slash
        return PyPosSepParam(slash=slash)

    @property
    def parent(self) -> 'PyPosSepParamParent':
        assert(self._parent is not None)
        return cast(PyPosSepParamParent, self._parent)


def is_py_pos_sep_param(value: Any) -> TypeIs[PyPosSepParam]:
    return isinstance(value, PyPosSepParam)


class PyPrefixExprDeriveKwargs(TypedDict, total=False):

    prefix_op: 'PyPrefixOp'

    expr: 'PyExpr'


class PyPrefixExpr(_PyBaseNode):

    _fields_ = ('prefix_op', 'expr')

    def __init__(self, prefix_op: 'PyPrefixOp', expr: 'PyExpr') -> None:
        self.prefix_op: PyPrefixOp = _coerce_77(prefix_op)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyPrefixExprDeriveKwargs]) -> 'PyPrefixExpr':
        prefix_op = _coerce_77(kwargs['prefix_op']) if 'prefix_op' in kwargs else self.prefix_op
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyPrefixExpr(prefix_op=prefix_op, expr=expr)

    @property
    def parent(self) -> 'PyPrefixExprParent':
        assert(self._parent is not None)
        return cast(PyPrefixExprParent, self._parent)


def is_py_prefix_expr(value: Any) -> TypeIs[PyPrefixExpr]:
    return isinstance(value, PyPrefixExpr)


class PyQualNameDeriveKwargs(TypedDict, total=False):

    modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None'

    name: 'PyIdent | str'


class PyQualName(_PyBaseNode):

    _fields_ = ('modules', 'name')

    def count_modules(self) -> int:
        return len(self.modules)

    def __init__(self, name: 'PyIdent | str', *, modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None' = None) -> None:
        self.modules: list[tuple[PyIdent, PyDot]] = _coerce_79(modules)
        self.name: PyIdent = _coerce_0(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyQualNameDeriveKwargs]) -> 'PyQualName':
        modules = _coerce_79(kwargs['modules']) if 'modules' in kwargs else self.modules
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        return PyQualName(modules=modules, name=name)

    @property
    def parent(self) -> 'PyQualNameParent':
        assert(self._parent is not None)
        return cast(PyQualNameParent, self._parent)


def is_py_qual_name(value: Any) -> TypeIs[PyQualName]:
    return isinstance(value, PyQualName)


class PyRaiseStmtDeriveKwargs(TypedDict, total=False):

    raise_keyword: 'PyRaiseKeyword | None'

    expr: 'PyExpr'

    cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None'


class PyRaiseStmt(_PyBaseNode):

    _fields_ = ('raise_keyword', 'expr', 'cause')

    def __init__(self, expr: 'PyExpr', *, raise_keyword: 'PyRaiseKeyword | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None) -> None:
        self.raise_keyword: PyRaiseKeyword = _coerce_80(raise_keyword)
        self.expr: PyExpr = _coerce_6(expr)
        self.cause: tuple[PyFromKeyword, PyExpr] | None = _coerce_81(cause)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyRaiseStmtDeriveKwargs]) -> 'PyRaiseStmt':
        raise_keyword = _coerce_80(kwargs['raise_keyword']) if 'raise_keyword' in kwargs else self.raise_keyword
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        cause = _coerce_81(kwargs['cause']) if 'cause' in kwargs else self.cause
        return PyRaiseStmt(raise_keyword=raise_keyword, expr=expr, cause=cause)

    @property
    def parent(self) -> 'PyRaiseStmtParent':
        assert(self._parent is not None)
        return cast(PyRaiseStmtParent, self._parent)


def is_py_raise_stmt(value: Any) -> TypeIs[PyRaiseStmt]:
    return isinstance(value, PyRaiseStmt)


class PyRelativePathDeriveKwargs(TypedDict, total=False):

    dots: 'Sequence[PyDot] | int'

    name: 'PyIdent | PyQualName | None | str'


class PyRelativePath(_PyBaseNode):

    _fields_ = ('dots', 'name')

    def count_dots(self) -> int:
        return len(self.dots)

    def __init__(self, dots: 'Sequence[PyDot] | int', *, name: 'PyIdent | PyQualName | None | str' = None) -> None:
        self.dots: list[PyDot] = _coerce_83(dots)
        self.name: PyQualName | None = _coerce_84(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyRelativePathDeriveKwargs]) -> 'PyRelativePath':
        dots = _coerce_83(kwargs['dots']) if 'dots' in kwargs else self.dots
        name = _coerce_84(kwargs['name']) if 'name' in kwargs else self.name
        return PyRelativePath(dots=dots, name=name)

    @property
    def parent(self) -> 'PyRelativePathParent':
        assert(self._parent is not None)
        return cast(PyRelativePathParent, self._parent)


def is_py_relative_path(value: Any) -> TypeIs[PyRelativePath]:
    return isinstance(value, PyRelativePath)


class PyRestKeywordParamDeriveKwargs(TypedDict, total=False):

    asterisk_asterisk: 'PyAsteriskAsterisk | None'

    name: 'PyIdent | str'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'


class PyRestKeywordParam(_PyBaseNode):

    _fields_ = ('asterisk_asterisk', 'name', 'annotation')

    def __init__(self, name: 'PyIdent | str', *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.asterisk_asterisk: PyAsteriskAsterisk = _coerce_85(asterisk_asterisk)
        self.name: PyIdent = _coerce_0(name)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_8(annotation)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyRestKeywordParamDeriveKwargs]) -> 'PyRestKeywordParam':
        asterisk_asterisk = _coerce_85(kwargs['asterisk_asterisk']) if 'asterisk_asterisk' in kwargs else self.asterisk_asterisk
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        annotation = _coerce_8(kwargs['annotation']) if 'annotation' in kwargs else self.annotation
        return PyRestKeywordParam(asterisk_asterisk=asterisk_asterisk, name=name, annotation=annotation)

    @property
    def parent(self) -> 'PyRestKeywordParamParent':
        assert(self._parent is not None)
        return cast(PyRestKeywordParamParent, self._parent)


def is_py_rest_keyword_param(value: Any) -> TypeIs[PyRestKeywordParam]:
    return isinstance(value, PyRestKeywordParam)


class PyRestPosParamDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'

    name: 'PyIdent | str'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'


class PyRestPosParam(_PyBaseNode):

    _fields_ = ('asterisk', 'name', 'annotation')

    def __init__(self, name: 'PyIdent | str', *, asterisk: 'PyAsterisk | None' = None, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_65(asterisk)
        self.name: PyIdent = _coerce_0(name)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_8(annotation)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyRestPosParamDeriveKwargs]) -> 'PyRestPosParam':
        asterisk = _coerce_65(kwargs['asterisk']) if 'asterisk' in kwargs else self.asterisk
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        annotation = _coerce_8(kwargs['annotation']) if 'annotation' in kwargs else self.annotation
        return PyRestPosParam(asterisk=asterisk, name=name, annotation=annotation)

    @property
    def parent(self) -> 'PyRestPosParamParent':
        assert(self._parent is not None)
        return cast(PyRestPosParamParent, self._parent)


def is_py_rest_pos_param(value: Any) -> TypeIs[PyRestPosParam]:
    return isinstance(value, PyRestPosParam)


class PyRetStmtDeriveKwargs(TypedDict, total=False):

    return_keyword: 'PyReturnKeyword | None'

    expr: 'PyExpr | None'


class PyRetStmt(_PyBaseNode):

    _fields_ = ('return_keyword', 'expr')

    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> None:
        self.return_keyword: PyReturnKeyword = _coerce_86(return_keyword)
        self.expr: PyExpr | None = _coerce_41(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyRetStmtDeriveKwargs]) -> 'PyRetStmt':
        return_keyword = _coerce_86(kwargs['return_keyword']) if 'return_keyword' in kwargs else self.return_keyword
        expr = _coerce_41(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyRetStmt(return_keyword=return_keyword, expr=expr)

    @property
    def parent(self) -> 'PyRetStmtParent':
        assert(self._parent is not None)
        return cast(PyRetStmtParent, self._parent)


def is_py_ret_stmt(value: Any) -> TypeIs[PyRetStmt]:
    return isinstance(value, PyRetStmt)


class PyStarredExprDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'

    expr: 'PyExpr'


class PyStarredExpr(_PyBaseNode):

    _fields_ = ('asterisk', 'expr')

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_65(asterisk)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyStarredExprDeriveKwargs]) -> 'PyStarredExpr':
        asterisk = _coerce_65(kwargs['asterisk']) if 'asterisk' in kwargs else self.asterisk
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyStarredExpr(asterisk=asterisk, expr=expr)

    @property
    def parent(self) -> 'PyStarredExprParent':
        assert(self._parent is not None)
        return cast(PyStarredExprParent, self._parent)


def is_py_starred_expr(value: Any) -> TypeIs[PyStarredExpr]:
    return isinstance(value, PyStarredExpr)


class PyStarredPatternDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'

    pattern: 'PyPattern'


class PyStarredPattern(_PyBaseNode):

    _fields_ = ('asterisk', 'pattern')

    def __init__(self, pattern: 'PyPattern', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_65(asterisk)
        self.pattern: PyPattern = _coerce_5(pattern)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyStarredPatternDeriveKwargs]) -> 'PyStarredPattern':
        asterisk = _coerce_65(kwargs['asterisk']) if 'asterisk' in kwargs else self.asterisk
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        return PyStarredPattern(asterisk=asterisk, pattern=pattern)

    @property
    def parent(self) -> 'PyStarredPatternParent':
        assert(self._parent is not None)
        return cast(PyStarredPatternParent, self._parent)


def is_py_starred_pattern(value: Any) -> TypeIs[PyStarredPattern]:
    return isinstance(value, PyStarredPattern)


class PySubscriptExprDeriveKwargs(TypedDict, total=False):

    expr: 'PyExpr'

    open_bracket: 'PyOpenBracket | None'

    slices: 'Sequence[tuple[PyExpr | PyExprSlice, PyComma | None]] | Sequence[PyExpr | PyExprSlice] | ImmutablePunct[PyExpr | PyExprSlice, PyComma]'

    close_bracket: 'PyCloseBracket | None'


class PySubscriptExpr(_PyBaseNode):

    _fields_ = ('expr', 'open_bracket', 'slices', 'close_bracket')

    def count_slices(self) -> int:
        return len(self.slices)

    def __init__(self, expr: 'PyExpr', slices: 'Sequence[tuple[PyExpr | PyExprSlice, PyComma | None]] | Sequence[PyExpr | PyExprSlice] | ImmutablePunct[PyExpr | PyExprSlice, PyComma]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.expr: PyExpr = _coerce_6(expr)
        self.open_bracket: PyOpenBracket = _coerce_68(open_bracket)
        self.slices: Punctuated[PyExpr | PyExprSlice, PyComma] = _coerce_88(slices)
        self.close_bracket: PyCloseBracket = _coerce_70(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[PySubscriptExprDeriveKwargs]) -> 'PySubscriptExpr':
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        open_bracket = _coerce_68(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        slices = _coerce_88(kwargs['slices']) if 'slices' in kwargs else self.slices
        close_bracket = _coerce_70(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return PySubscriptExpr(expr=expr, open_bracket=open_bracket, slices=slices, close_bracket=close_bracket)

    @property
    def parent(self) -> 'PySubscriptExprParent':
        assert(self._parent is not None)
        return cast(PySubscriptExprParent, self._parent)


def is_py_subscript_expr(value: Any) -> TypeIs[PySubscriptExpr]:
    return isinstance(value, PySubscriptExpr)


class PySubscriptPatternDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    open_bracket: 'PyOpenBracket | None'

    slices: 'Sequence[tuple[PyPattern | PyPatternSlice, PyComma | None]] | Sequence[PyPattern | PyPatternSlice] | ImmutablePunct[PyPattern | PyPatternSlice, PyComma]'

    close_bracket: 'PyCloseBracket | None'


class PySubscriptPattern(_PyBaseNode):

    _fields_ = ('pattern', 'open_bracket', 'slices', 'close_bracket')

    def count_slices(self) -> int:
        return len(self.slices)

    def __init__(self, pattern: 'PyPattern', slices: 'Sequence[tuple[PyPattern | PyPatternSlice, PyComma | None]] | Sequence[PyPattern | PyPatternSlice] | ImmutablePunct[PyPattern | PyPatternSlice, PyComma]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.pattern: PyPattern = _coerce_5(pattern)
        self.open_bracket: PyOpenBracket = _coerce_68(open_bracket)
        self.slices: Punctuated[PyPattern | PyPatternSlice, PyComma] = _coerce_90(slices)
        self.close_bracket: PyCloseBracket = _coerce_70(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[PySubscriptPatternDeriveKwargs]) -> 'PySubscriptPattern':
        pattern = _coerce_5(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        open_bracket = _coerce_68(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        slices = _coerce_90(kwargs['slices']) if 'slices' in kwargs else self.slices
        close_bracket = _coerce_70(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return PySubscriptPattern(pattern=pattern, open_bracket=open_bracket, slices=slices, close_bracket=close_bracket)

    @property
    def parent(self) -> 'PySubscriptPatternParent':
        assert(self._parent is not None)
        return cast(PySubscriptPatternParent, self._parent)


def is_py_subscript_pattern(value: Any) -> TypeIs[PySubscriptPattern]:
    return isinstance(value, PySubscriptPattern)


class PyTryStmtDeriveKwargs(TypedDict, total=False):

    try_keyword: 'PyTryKeyword | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'

    handlers: 'Sequence[PyExceptHandler] | None'

    else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'

    finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'


class PyTryStmt(_PyBaseNode):

    _fields_ = ('try_keyword', 'colon', 'body', 'handlers', 'else_clause', 'finally_clause')

    def count_handlers(self) -> int:
        return len(self.handlers)

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, handlers: 'Sequence[PyExceptHandler] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None, finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.try_keyword: PyTryKeyword = _coerce_91(try_keyword)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)
        self.handlers: list[PyExceptHandler] = _coerce_93(handlers)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = _coerce_42(else_clause)
        self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None = _coerce_95(finally_clause)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyTryStmtDeriveKwargs]) -> 'PyTryStmt':
        try_keyword = _coerce_91(kwargs['try_keyword']) if 'try_keyword' in kwargs else self.try_keyword
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        handlers = _coerce_93(kwargs['handlers']) if 'handlers' in kwargs else self.handlers
        else_clause = _coerce_42(kwargs['else_clause']) if 'else_clause' in kwargs else self.else_clause
        finally_clause = _coerce_95(kwargs['finally_clause']) if 'finally_clause' in kwargs else self.finally_clause
        return PyTryStmt(try_keyword=try_keyword, colon=colon, body=body, handlers=handlers, else_clause=else_clause, finally_clause=finally_clause)

    @property
    def parent(self) -> 'PyTryStmtParent':
        assert(self._parent is not None)
        return cast(PyTryStmtParent, self._parent)


def is_py_try_stmt(value: Any) -> TypeIs[PyTryStmt]:
    return isinstance(value, PyTryStmt)


class PyTupleManyDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma]'

    close_paren: 'PyCloseParen | None'


class PyTupleMany(_PyBaseNode):

    _fields_ = ('open_paren', 'elements', 'close_paren')

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma]', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.elements: Punctuated[PyExpr, PyComma] = _coerce_96(elements)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyTupleManyDeriveKwargs]) -> 'PyTupleMany':
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        elements = _coerce_96(kwargs['elements']) if 'elements' in kwargs else self.elements
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return PyTupleMany(open_paren=open_paren, elements=elements, close_paren=close_paren)

    @property
    def parent(self) -> 'PyTupleManyParent':
        assert(self._parent is not None)
        return cast(PyTupleManyParent, self._parent)


def is_py_tuple_many(value: Any) -> TypeIs[PyTupleMany]:
    return isinstance(value, PyTupleMany)


class PyTupleOneDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    expr: 'PyExpr'

    comma: 'PyComma | None'

    close_paren: 'PyCloseParen | None'


class PyTupleOne(_PyBaseNode):

    _fields_ = ('open_paren', 'expr', 'comma', 'close_paren')

    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, comma: 'PyComma | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.expr: PyExpr = _coerce_6(expr)
        self.comma: PyComma = _coerce_97(comma)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyTupleOneDeriveKwargs]) -> 'PyTupleOne':
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        comma = _coerce_97(kwargs['comma']) if 'comma' in kwargs else self.comma
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return PyTupleOne(open_paren=open_paren, expr=expr, comma=comma, close_paren=close_paren)

    @property
    def parent(self) -> 'PyTupleOneParent':
        assert(self._parent is not None)
        return cast(PyTupleOneParent, self._parent)


def is_py_tuple_one(value: Any) -> TypeIs[PyTupleOne]:
    return isinstance(value, PyTupleOne)


class PyTuplePatternDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None'

    close_paren: 'PyCloseParen | None'


class PyTuplePattern(_PyBaseNode):

    _fields_ = ('open_paren', 'elements', 'close_paren')

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.elements: Punctuated[PyPattern, PyComma] = _coerce_67(elements)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyTuplePatternDeriveKwargs]) -> 'PyTuplePattern':
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        elements = _coerce_67(kwargs['elements']) if 'elements' in kwargs else self.elements
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return PyTuplePattern(open_paren=open_paren, elements=elements, close_paren=close_paren)

    @property
    def parent(self) -> 'PyTuplePatternParent':
        assert(self._parent is not None)
        return cast(PyTuplePatternParent, self._parent)


def is_py_tuple_pattern(value: Any) -> TypeIs[PyTuplePattern]:
    return isinstance(value, PyTuplePattern)


class PyTupleZeroDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    close_paren: 'PyCloseParen | None'


class PyTupleZero(_PyBaseNode):

    _fields_ = ('open_paren', 'close_paren')

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_14(open_paren)
        self.close_paren: PyCloseParen = _coerce_18(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyTupleZeroDeriveKwargs]) -> 'PyTupleZero':
        open_paren = _coerce_14(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        close_paren = _coerce_18(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return PyTupleZero(open_paren=open_paren, close_paren=close_paren)

    @property
    def parent(self) -> 'PyTupleZeroParent':
        assert(self._parent is not None)
        return cast(PyTupleZeroParent, self._parent)


def is_py_tuple_zero(value: Any) -> TypeIs[PyTupleZero]:
    return isinstance(value, PyTupleZero)


class PyTypeAliasStmtDeriveKwargs(TypedDict, total=False):

    type_keyword: 'PyTypeKeyword | None'

    name: 'PyIdent | str'

    type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyTypeAliasStmt(_PyBaseNode):

    _fields_ = ('type_keyword', 'name', 'type_params', 'equals', 'expr')

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, type_keyword: 'PyTypeKeyword | None' = None, type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None' = None, equals: 'PyEquals | None' = None) -> None:
        self.type_keyword: PyTypeKeyword = _coerce_98(type_keyword)
        self.name: PyIdent = _coerce_0(name)
        self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = _coerce_100(type_params)
        self.equals: PyEquals = _coerce_9(equals)
        self.expr: PyExpr = _coerce_6(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyTypeAliasStmtDeriveKwargs]) -> 'PyTypeAliasStmt':
        type_keyword = _coerce_98(kwargs['type_keyword']) if 'type_keyword' in kwargs else self.type_keyword
        name = _coerce_0(kwargs['name']) if 'name' in kwargs else self.name
        type_params = _coerce_100(kwargs['type_params']) if 'type_params' in kwargs else self.type_params
        equals = _coerce_9(kwargs['equals']) if 'equals' in kwargs else self.equals
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        return PyTypeAliasStmt(type_keyword=type_keyword, name=name, type_params=type_params, equals=equals, expr=expr)

    @property
    def parent(self) -> 'PyTypeAliasStmtParent':
        assert(self._parent is not None)
        return cast(PyTypeAliasStmtParent, self._parent)


def is_py_type_alias_stmt(value: Any) -> TypeIs[PyTypeAliasStmt]:
    return isinstance(value, PyTypeAliasStmt)


class PyWhileStmtDeriveKwargs(TypedDict, total=False):

    while_keyword: 'PyWhileKeyword | None'

    expr: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'

    else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'


class PyWhileStmt(_PyBaseNode):

    _fields_ = ('while_keyword', 'expr', 'colon', 'body', 'else_clause')

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, while_keyword: 'PyWhileKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.while_keyword: PyWhileKeyword = _coerce_101(while_keyword)
        self.expr: PyExpr = _coerce_6(expr)
        self.colon: PyColon = _coerce_7(colon)
        self.body: PyStmt | list[PyStmt] = _coerce_27(body)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None = _coerce_42(else_clause)

    @no_type_check
    def derive(self, **kwargs: Unpack[PyWhileStmtDeriveKwargs]) -> 'PyWhileStmt':
        while_keyword = _coerce_101(kwargs['while_keyword']) if 'while_keyword' in kwargs else self.while_keyword
        expr = _coerce_6(kwargs['expr']) if 'expr' in kwargs else self.expr
        colon = _coerce_7(kwargs['colon']) if 'colon' in kwargs else self.colon
        body = _coerce_27(kwargs['body']) if 'body' in kwargs else self.body
        else_clause = _coerce_42(kwargs['else_clause']) if 'else_clause' in kwargs else self.else_clause
        return PyWhileStmt(while_keyword=while_keyword, expr=expr, colon=colon, body=body, else_clause=else_clause)

    @property
    def parent(self) -> 'PyWhileStmtParent':
        assert(self._parent is not None)
        return cast(PyWhileStmtParent, self._parent)


def is_py_while_stmt(value: Any) -> TypeIs[PyWhileStmt]:
    return isinstance(value, PyWhileStmt)


type PyArg = PyKeywordArg | PyExpr


def is_py_arg(value: Any) -> TypeIs[PyArg]:
    return isinstance(value, PyKeywordArg) or is_py_expr(value)


type PyBaseArg = PyClassBaseArg | PyKeywordBaseArg


def is_py_base_arg(value: Any) -> TypeIs[PyBaseArg]:
    return isinstance(value, PyClassBaseArg) or isinstance(value, PyKeywordBaseArg)


type PyExpr = PyAttrExpr | PyCallExpr | PyConstExpr | PyEllipsisExpr | PyGeneratorExpr | PyIfExpr | PyInfixExpr | PyLambdaExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr


def is_py_expr(value: Any) -> TypeIs[PyExpr]:
    return isinstance(value, PyAttrExpr) or isinstance(value, PyCallExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyEllipsisExpr) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyIfExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyLambdaExpr) or isinstance(value, PyListExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PySubscriptExpr) or is_py_tuple_expr(value)


type PyInfixOp = PyPlus | PyHyphen | PyAsterisk | PySlash | PyAtSign | PySlashSlash | PyPercent | PyAsteriskAsterisk | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | tuple[PyIsKeyword, PyNotKeyword] | PyInKeyword | tuple[PyNotKeyword, PyInKeyword]


def is_py_infix_op(value: Any) -> TypeIs[PyInfixOp]:
    return isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyAsterisk) or isinstance(value, PySlash) or isinstance(value, PyAtSign) or isinstance(value, PySlashSlash) or isinstance(value, PyPercent) or isinstance(value, PyAsteriskAsterisk) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyVerticalBar) or isinstance(value, PyCaret) or isinstance(value, PyAmpersand) or isinstance(value, PyOrKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyEqualsEquals) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyLessThan) or isinstance(value, PyLessThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyIsKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyIsKeyword) and isinstance(value[1], PyNotKeyword)) or isinstance(value, PyInKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyNotKeyword) and isinstance(value[1], PyInKeyword))


type PyKeyword = PyIfKeyword | PyAsyncKeyword | PyForKeyword | PyInKeyword | PyIfKeyword | PyElseKeyword | PyLambdaKeyword | PyNotKeyword | PyOrKeyword | PyAndKeyword | PyIsKeyword | PyIsKeyword | PyNotKeyword | PyInKeyword | PyNotKeyword | PyInKeyword | PyAsKeyword | PyAsKeyword | PyImportKeyword | PyFromKeyword | PyImportKeyword | PyReturnKeyword | PyPassKeyword | PyGlobalKeyword | PyNonlocalKeyword | PyIfKeyword | PyElifKeyword | PyElseKeyword | PyDelKeyword | PyRaiseKeyword | PyFromKeyword | PyForKeyword | PyInKeyword | PyElseKeyword | PyWhileKeyword | PyElseKeyword | PyBreakKeyword | PyContinueKeyword | PyTypeKeyword | PyExceptKeyword | PyAsKeyword | PyTryKeyword | PyElseKeyword | PyFinallyKeyword | PyClassKeyword | PyAsyncKeyword | PyDefKeyword


def is_py_keyword(value: Any) -> TypeIs[PyKeyword]:
    return isinstance(value, PyIfKeyword) or isinstance(value, PyAsyncKeyword) or isinstance(value, PyForKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyIfKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyLambdaKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyOrKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyIsKeyword) or isinstance(value, PyIsKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyImportKeyword) or isinstance(value, PyFromKeyword) or isinstance(value, PyImportKeyword) or isinstance(value, PyReturnKeyword) or isinstance(value, PyPassKeyword) or isinstance(value, PyGlobalKeyword) or isinstance(value, PyNonlocalKeyword) or isinstance(value, PyIfKeyword) or isinstance(value, PyElifKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyDelKeyword) or isinstance(value, PyRaiseKeyword) or isinstance(value, PyFromKeyword) or isinstance(value, PyForKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyWhileKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyBreakKeyword) or isinstance(value, PyContinueKeyword) or isinstance(value, PyTypeKeyword) or isinstance(value, PyExceptKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyTryKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyFinallyKeyword) or isinstance(value, PyClassKeyword) or isinstance(value, PyAsyncKeyword) or isinstance(value, PyDefKeyword)


type PyNode = PyPatternSlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyExprSlice | PyEllipsisExpr | PyGuard | PyComprehension | PyGeneratorExpr | PyIfExpr | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleZero | PyTupleOne | PyTupleMany | PyKeywordArg | PyCallExpr | PyLambdaExpr | PyPrefixExpr | PyInfixExpr | PyQualName | PyAbsolutePath | PyRelativePath | PyAlias | PyFromAlias | PyImportStmt | PyImportFromStmt | PyRetStmt | PyExprStmt | PyAugAssignStmt | PyAssignStmt | PyPassStmt | PyGlobalStmt | PyNonlocalStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassBaseArg | PyKeywordBaseArg | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PyPosSepParam | PyKwSepParam | PyDecorator | PyFuncDef | PyModule


def is_py_node(value: Any) -> TypeIs[PyNode]:
    return isinstance(value, PyPatternSlice) or isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern) or isinstance(value, PyExprSlice) or isinstance(value, PyEllipsisExpr) or isinstance(value, PyGuard) or isinstance(value, PyComprehension) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyIfExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyAttrExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PyListExpr) or isinstance(value, PyTupleZero) or isinstance(value, PyTupleOne) or isinstance(value, PyTupleMany) or isinstance(value, PyKeywordArg) or isinstance(value, PyCallExpr) or isinstance(value, PyLambdaExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyQualName) or isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath) or isinstance(value, PyAlias) or isinstance(value, PyFromAlias) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyAugAssignStmt) or isinstance(value, PyAssignStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyGlobalStmt) or isinstance(value, PyNonlocalStmt) or isinstance(value, PyIfCase) or isinstance(value, PyElifCase) or isinstance(value, PyElseCase) or isinstance(value, PyIfStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyForStmt) or isinstance(value, PyWhileStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyContinueStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyExceptHandler) or isinstance(value, PyTryStmt) or isinstance(value, PyClassBaseArg) or isinstance(value, PyKeywordBaseArg) or isinstance(value, PyClassDef) or isinstance(value, PyNamedParam) or isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PyPosSepParam) or isinstance(value, PyKwSepParam) or isinstance(value, PyDecorator) or isinstance(value, PyFuncDef) or isinstance(value, PyModule)


type PyParam = PyRestPosParam | PyRestKeywordParam | PyPosSepParam | PyKwSepParam | PyNamedParam


def is_py_param(value: Any) -> TypeIs[PyParam]:
    return isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PyPosSepParam) or isinstance(value, PyKwSepParam) or isinstance(value, PyNamedParam)


type PyPath = PyAbsolutePath | PyRelativePath


def is_py_path(value: Any) -> TypeIs[PyPath]:
    return isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath)


type PyPattern = PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern


def is_py_pattern(value: Any) -> TypeIs[PyPattern]:
    return isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern)


type PyPrefixOp = PyNotKeyword | PyPlus | PyHyphen | PyTilde


def is_py_prefix_op(value: Any) -> TypeIs[PyPrefixOp]:
    return isinstance(value, PyNotKeyword) or isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyTilde)


type PyStmt = PyAssignStmt | PyAugAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyGlobalStmt | PyIfStmt | PyImportStmt | PyImportFromStmt | PyNonlocalStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt


def is_py_stmt(value: Any) -> TypeIs[PyStmt]:
    return isinstance(value, PyAssignStmt) or isinstance(value, PyAugAssignStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyClassDef) or isinstance(value, PyContinueStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyForStmt) or isinstance(value, PyFuncDef) or isinstance(value, PyGlobalStmt) or isinstance(value, PyIfStmt) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyNonlocalStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyTryStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyWhileStmt)


type PySyntax = PyToken | PyNode


def is_py_syntax(value: Any) -> TypeIs[PySyntax]:
    return is_py_token(value) or is_py_node(value)


type PyToken = str | str | str | str | PyIdent | PyFloat | PyInteger | PyString


def is_py_token(value: Any) -> TypeIs[PyToken]:
    return isinstance(value, str) or isinstance(value, str) or isinstance(value, str) or isinstance(value, str) or isinstance(value, PyIdent) or isinstance(value, PyFloat) or isinstance(value, PyInteger) or isinstance(value, PyString)


type PyTupleExpr = PyTupleZero | PyTupleOne | PyTupleMany


def is_py_tuple_expr(value: Any) -> TypeIs[PyTupleExpr]:
    return isinstance(value, PyTupleZero) or isinstance(value, PyTupleOne) or isinstance(value, PyTupleMany)


type PyAbsolutePathParent = PyAlias | PyImportFromStmt


type PyAliasParent = PyImportStmt


type PyAssignStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyAttrExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyAttrPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyLambdaExpr | PyListPattern | PyNamedParam | PyPatternSlice | PyStarredPattern | PySubscriptPattern | PyTuplePattern


type PyAugAssignStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyBreakStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyCallExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyClassBaseArgParent = PyClassDef


type PyClassDefParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyComprehensionParent = PyGeneratorExpr


type PyConstExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyContinueStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyDecoratorParent = PyClassDef | PyFuncDef


type PyDeleteStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyElifCaseParent = PyIfStmt


type PyEllipsisExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyElseCaseParent = PyIfStmt


type PyExceptHandlerParent = PyTryStmt


type PyExprSliceParent = PySubscriptExpr


type PyExprStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyForStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyFromAliasParent = PyImportFromStmt


type PyFuncDefParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyGeneratorExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyGlobalStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyGuardParent = PyComprehension


type PyIfCaseParent = PyIfStmt


type PyIfExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyIfStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyImportFromStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyImportStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyInfixExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyKeywordArgParent = PyCallExpr


type PyKeywordBaseArgParent = PyClassDef


type PyKwSepParamParent = PyFuncDef


type PyLambdaExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyListExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyListPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyLambdaExpr | PyListPattern | PyNamedParam | PyPatternSlice | PyStarredPattern | PySubscriptPattern | PyTuplePattern


type PyModuleParent = Never


type PyNamedExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyNamedParamParent = PyFuncDef


type PyNamedPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyLambdaExpr | PyListPattern | PyNamedParam | PyPatternSlice | PyStarredPattern | PySubscriptPattern | PyTuplePattern


type PyNestExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyNonlocalStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyPassStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyPatternSliceParent = PySubscriptPattern


type PyPosSepParamParent = PyFuncDef


type PyPrefixExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyQualNameParent = PyAbsolutePath | PyRelativePath


type PyRaiseStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyRelativePathParent = PyAlias | PyImportFromStmt


type PyRestKeywordParamParent = PyFuncDef


type PyRestPosParamParent = PyFuncDef


type PyRetStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyStarredExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyStarredPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyLambdaExpr | PyListPattern | PyNamedParam | PyPatternSlice | PyStarredPattern | PySubscriptPattern | PyTuplePattern


type PySubscriptExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PySubscriptPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyLambdaExpr | PyListPattern | PyNamedParam | PyPatternSlice | PyStarredPattern | PySubscriptPattern | PyTuplePattern


type PyTryStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyTupleManyParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyTupleOneParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyTuplePatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyLambdaExpr | PyListPattern | PyNamedParam | PyPatternSlice | PyStarredPattern | PySubscriptPattern | PyTuplePattern


type PyTupleZeroParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprSlice | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyLambdaExpr | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PyStarredExpr | PySubscriptExpr | PyTupleMany | PyTupleOne | PyTypeAliasStmt | PyWhileStmt


type PyTypeAliasStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyWhileStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


@no_type_check
def _coerce_0(value: 'PyIdent | str') -> 'PyIdent':
    if isinstance(value, str):
        return PyIdent(value)
    elif isinstance(value, PyIdent):
        return value
    else:
        raise ValueError('the coercion from PyIdent | str to PyIdent failed')


@no_type_check
def _coerce_1(value: 'PyIdent | PyQualName | str') -> 'PyQualName':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return PyQualName(_coerce_0(value))
    elif isinstance(value, PyQualName):
        return value
    else:
        raise ValueError('the coercion from PyIdent | PyQualName | str to PyQualName failed')


@no_type_check
def _coerce_2(value: 'PyPath') -> 'PyPath':
    return value


@no_type_check
def _coerce_3(value: 'PyAsKeyword | None') -> 'PyAsKeyword':
    if value is None:
        return PyAsKeyword()
    elif isinstance(value, PyAsKeyword):
        return value
    else:
        raise ValueError('the coercion from PyAsKeyword | None to PyAsKeyword failed')


@no_type_check
def _coerce_4(value: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str') -> 'tuple[PyAsKeyword, PyIdent] | None':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return (PyAsKeyword(), _coerce_0(value))
    elif isinstance(value, tuple):
        return (_coerce_3(value[0]), _coerce_0(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str to tuple[PyAsKeyword, PyIdent] | None failed')


@no_type_check
def _coerce_5(value: 'PyPattern') -> 'PyPattern':
    return value


@no_type_check
def _coerce_6(value: 'PyExpr') -> 'PyExpr':
    return value


@no_type_check
def _coerce_7(value: 'PyColon | None') -> 'PyColon':
    if value is None:
        return PyColon()
    elif isinstance(value, PyColon):
        return value
    else:
        raise ValueError('the coercion from PyColon | None to PyColon failed')


@no_type_check
def _coerce_8(value: 'PyExpr | tuple[PyColon | None, PyExpr] | None') -> 'tuple[PyColon, PyExpr] | None':
    if is_py_expr(value):
        return (PyColon(), _coerce_6(value))
    elif isinstance(value, tuple):
        return (_coerce_7(value[0]), _coerce_6(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyColon | None, PyExpr] | None to tuple[PyColon, PyExpr] | None failed')


@no_type_check
def _coerce_9(value: 'PyEquals | None') -> 'PyEquals':
    if value is None:
        return PyEquals()
    elif isinstance(value, PyEquals):
        return value
    else:
        raise ValueError('the coercion from PyEquals | None to PyEquals failed')


@no_type_check
def _coerce_10(value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None') -> 'tuple[PyEquals, PyExpr] | None':
    if is_py_expr(value):
        return (PyEquals(), _coerce_6(value))
    elif isinstance(value, tuple):
        return (_coerce_9(value[0]), _coerce_6(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyEquals | None, PyExpr] | None to tuple[PyEquals, PyExpr] | None failed')


@no_type_check
def _coerce_11(value: 'PyDot | None') -> 'PyDot':
    if value is None:
        return PyDot()
    elif isinstance(value, PyDot):
        return value
    else:
        raise ValueError('the coercion from PyDot | None to PyDot failed')


@no_type_check
def _coerce_12(value: 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar') -> 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar':
    if isinstance(value, PyAmpersand):
        return value
    elif isinstance(value, PyAsterisk):
        return value
    elif isinstance(value, PyAsteriskAsterisk):
        return value
    elif isinstance(value, PyAtSign):
        return value
    elif isinstance(value, PyCaret):
        return value
    elif isinstance(value, PyGreaterThanGreaterThan):
        return value
    elif isinstance(value, PyHyphen):
        return value
    elif isinstance(value, PyLessThanLessThan):
        return value
    elif isinstance(value, PyPercent):
        return value
    elif isinstance(value, PyPlus):
        return value
    elif isinstance(value, PySlash):
        return value
    elif isinstance(value, PySlashSlash):
        return value
    elif isinstance(value, PyVerticalBar):
        return value
    else:
        raise ValueError('the coercion from PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar to PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar failed')


@no_type_check
def _coerce_13(value: 'PyBreakKeyword | None') -> 'PyBreakKeyword':
    if value is None:
        return PyBreakKeyword()
    elif isinstance(value, PyBreakKeyword):
        return value
    else:
        raise ValueError('the coercion from PyBreakKeyword | None to PyBreakKeyword failed')


@no_type_check
def _coerce_14(value: 'PyOpenParen | None') -> 'PyOpenParen':
    if value is None:
        return PyOpenParen()
    elif isinstance(value, PyOpenParen):
        return value
    else:
        raise ValueError('the coercion from PyOpenParen | None to PyOpenParen failed')


@no_type_check
def _coerce_15(value: 'PyArg') -> 'PyArg':
    return value


@no_type_check
def _coerce_16(value: 'PyComma') -> 'PyComma':
    return value


@no_type_check
def _coerce_17(value: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | ImmutablePunct[PyArg, PyComma] | None') -> 'Punctuated[PyArg, PyComma]':
    if value is None:
        return Punctuated()
    elif isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        new_value = Punctuated()
        iterator = iter(value)
        try:
            first_element = next(iterator)
            while True:
                try:
                    second_element = next(iterator)
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        element_separator = first_element[1]
                        assert(element_separator is not None)
                    else:
                        element_value = first_element
                        element_separator = PyComma()
                    new_element_value = _coerce_15(element_value)
                    new_element_separator = _coerce_16(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_15(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | ImmutablePunct[PyArg, PyComma] | None to Punctuated[PyArg, PyComma] failed')


@no_type_check
def _coerce_18(value: 'PyCloseParen | None') -> 'PyCloseParen':
    if value is None:
        return PyCloseParen()
    elif isinstance(value, PyCloseParen):
        return value
    else:
        raise ValueError('the coercion from PyCloseParen | None to PyCloseParen failed')


@no_type_check
def _coerce_19(value: 'PyDecorator | PyExpr') -> 'PyDecorator':
    if is_py_expr(value):
        return PyDecorator(_coerce_6(value))
    elif isinstance(value, PyDecorator):
        return value
    else:
        raise ValueError('the coercion from PyDecorator | PyExpr to PyDecorator failed')


@no_type_check
def _coerce_20(value: 'Sequence[PyDecorator | PyExpr] | None') -> 'list[PyDecorator]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_19(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyDecorator | PyExpr] | None to list[PyDecorator] failed')


@no_type_check
def _coerce_21(value: 'PyClassKeyword | None') -> 'PyClassKeyword':
    if value is None:
        return PyClassKeyword()
    elif isinstance(value, PyClassKeyword):
        return value
    else:
        raise ValueError('the coercion from PyClassKeyword | None to PyClassKeyword failed')


@no_type_check
def _coerce_22(value: 'PyBaseArg') -> 'PyBaseArg':
    return value


@no_type_check
def _coerce_23(value: 'Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma]') -> 'Punctuated[PyBaseArg, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_22(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_22(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_24(value: 'Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None') -> 'Punctuated[PyBaseArg, PyComma]':
    if value is None:
        return Punctuated()
    elif isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        new_value = Punctuated()
        iterator = iter(value)
        try:
            first_element = next(iterator)
            while True:
                try:
                    second_element = next(iterator)
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        element_separator = first_element[1]
                        assert(element_separator is not None)
                    else:
                        element_value = first_element
                        element_separator = PyComma()
                    new_element_value = _coerce_22(element_value)
                    new_element_separator = _coerce_16(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_22(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None to Punctuated[PyBaseArg, PyComma] failed')


@no_type_check
def _coerce_25(value: 'tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None') -> 'tuple[PyOpenParen, Punctuated[PyBaseArg, PyComma], PyCloseParen] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (PyOpenParen(), _coerce_23(value), PyCloseParen())
    elif isinstance(value, tuple):
        return (_coerce_14(value[0]), _coerce_24(value[1]), _coerce_18(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | ImmutablePunct[PyBaseArg, PyComma] | None to tuple[PyOpenParen, Punctuated[PyBaseArg, PyComma], PyCloseParen] | None failed')


@no_type_check
def _coerce_26(value: 'PyStmt') -> 'PyStmt':
    return value


@no_type_check
def _coerce_27(value: 'PyStmt | Sequence[PyStmt]') -> 'PyStmt | list[PyStmt]':
    if is_py_stmt(value):
        return value
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_26(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from PyStmt | Sequence[PyStmt] to PyStmt | list[PyStmt] failed')


@no_type_check
def _coerce_28(value: 'PyAsyncKeyword | None') -> 'PyAsyncKeyword | None':
    if isinstance(value, PyAsyncKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyAsyncKeyword | None to PyAsyncKeyword | None failed')


@no_type_check
def _coerce_29(value: 'PyForKeyword | None') -> 'PyForKeyword':
    if value is None:
        return PyForKeyword()
    elif isinstance(value, PyForKeyword):
        return value
    else:
        raise ValueError('the coercion from PyForKeyword | None to PyForKeyword failed')


@no_type_check
def _coerce_30(value: 'PyInKeyword | None') -> 'PyInKeyword':
    if value is None:
        return PyInKeyword()
    elif isinstance(value, PyInKeyword):
        return value
    else:
        raise ValueError('the coercion from PyInKeyword | None to PyInKeyword failed')


@no_type_check
def _coerce_31(value: 'PyExpr | PyGuard') -> 'PyGuard':
    if is_py_expr(value):
        return PyGuard(_coerce_6(value))
    elif isinstance(value, PyGuard):
        return value
    else:
        raise ValueError('the coercion from PyExpr | PyGuard to PyGuard failed')


@no_type_check
def _coerce_32(value: 'Sequence[PyExpr | PyGuard] | None') -> 'list[PyGuard]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_31(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyExpr | PyGuard] | None to list[PyGuard] failed')


@no_type_check
def _coerce_33(value: 'PyFloat | PyInteger | PyString | float | int | str') -> 'PyFloat | PyInteger | PyString':
    if isinstance(value, float):
        return PyFloat(value)
    elif isinstance(value, PyFloat):
        return value
    elif isinstance(value, int):
        return PyInteger(value)
    elif isinstance(value, PyInteger):
        return value
    elif isinstance(value, str):
        return PyString(value)
    elif isinstance(value, PyString):
        return value
    else:
        raise ValueError('the coercion from PyFloat | PyInteger | PyString | float | int | str to PyFloat | PyInteger | PyString failed')


@no_type_check
def _coerce_34(value: 'PyContinueKeyword | None') -> 'PyContinueKeyword':
    if value is None:
        return PyContinueKeyword()
    elif isinstance(value, PyContinueKeyword):
        return value
    else:
        raise ValueError('the coercion from PyContinueKeyword | None to PyContinueKeyword failed')


@no_type_check
def _coerce_35(value: 'PyAtSign | None') -> 'PyAtSign':
    if value is None:
        return PyAtSign()
    elif isinstance(value, PyAtSign):
        return value
    else:
        raise ValueError('the coercion from PyAtSign | None to PyAtSign failed')


@no_type_check
def _coerce_36(value: 'PyDelKeyword | None') -> 'PyDelKeyword':
    if value is None:
        return PyDelKeyword()
    elif isinstance(value, PyDelKeyword):
        return value
    else:
        raise ValueError('the coercion from PyDelKeyword | None to PyDelKeyword failed')


@no_type_check
def _coerce_37(value: 'PyElifKeyword | None') -> 'PyElifKeyword':
    if value is None:
        return PyElifKeyword()
    elif isinstance(value, PyElifKeyword):
        return value
    else:
        raise ValueError('the coercion from PyElifKeyword | None to PyElifKeyword failed')


@no_type_check
def _coerce_38(value: 'PyDotDotDot | None') -> 'PyDotDotDot':
    if value is None:
        return PyDotDotDot()
    elif isinstance(value, PyDotDotDot):
        return value
    else:
        raise ValueError('the coercion from PyDotDotDot | None to PyDotDotDot failed')


@no_type_check
def _coerce_39(value: 'PyElseKeyword | None') -> 'PyElseKeyword':
    if value is None:
        return PyElseKeyword()
    elif isinstance(value, PyElseKeyword):
        return value
    else:
        raise ValueError('the coercion from PyElseKeyword | None to PyElseKeyword failed')


@no_type_check
def _coerce_40(value: 'PyExceptKeyword | None') -> 'PyExceptKeyword':
    if value is None:
        return PyExceptKeyword()
    elif isinstance(value, PyExceptKeyword):
        return value
    else:
        raise ValueError('the coercion from PyExceptKeyword | None to PyExceptKeyword failed')


@no_type_check
def _coerce_41(value: 'PyExpr | None') -> 'PyExpr | None':
    if is_py_expr(value):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | None to PyExpr | None failed')


@no_type_check
def _coerce_42(value: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None') -> 'tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None':
    if is_py_stmt(value) or isinstance(value, list):
        return (PyElseKeyword(), PyColon(), _coerce_27(value))
    elif isinstance(value, tuple):
        return (_coerce_39(value[0]), _coerce_7(value[1]), _coerce_27(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None to tuple[PyElseKeyword, PyColon, PyStmt | list[PyStmt]] | None failed')


@no_type_check
def _coerce_43(value: 'PyAsterisk | PyIdent | str') -> 'PyAsterisk | PyIdent':
    if isinstance(value, PyAsterisk):
        return value
    elif isinstance(value, str):
        return PyIdent(value)
    elif isinstance(value, PyIdent):
        return value
    else:
        raise ValueError('the coercion from PyAsterisk | PyIdent | str to PyAsterisk | PyIdent failed')


@no_type_check
def _coerce_44(value: 'PyDefKeyword | None') -> 'PyDefKeyword':
    if value is None:
        return PyDefKeyword()
    elif isinstance(value, PyDefKeyword):
        return value
    else:
        raise ValueError('the coercion from PyDefKeyword | None to PyDefKeyword failed')


@no_type_check
def _coerce_45(value: 'PyParam') -> 'PyParam':
    return value


@no_type_check
def _coerce_46(value: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | ImmutablePunct[PyParam, PyComma] | None') -> 'Punctuated[PyParam, PyComma]':
    if value is None:
        return Punctuated()
    elif isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        new_value = Punctuated()
        iterator = iter(value)
        try:
            first_element = next(iterator)
            while True:
                try:
                    second_element = next(iterator)
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        element_separator = first_element[1]
                        assert(element_separator is not None)
                    else:
                        element_value = first_element
                        element_separator = PyComma()
                    new_element_value = _coerce_45(element_value)
                    new_element_separator = _coerce_16(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_45(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | ImmutablePunct[PyParam, PyComma] | None to Punctuated[PyParam, PyComma] failed')


@no_type_check
def _coerce_47(value: 'PyRArrow | None') -> 'PyRArrow':
    if value is None:
        return PyRArrow()
    elif isinstance(value, PyRArrow):
        return value
    else:
        raise ValueError('the coercion from PyRArrow | None to PyRArrow failed')


@no_type_check
def _coerce_48(value: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None') -> 'tuple[PyRArrow, PyExpr] | None':
    if is_py_expr(value):
        return (PyRArrow(), _coerce_6(value))
    elif isinstance(value, tuple):
        return (_coerce_47(value[0]), _coerce_6(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyRArrow | None, PyExpr] | None to tuple[PyRArrow, PyExpr] | None failed')


@no_type_check
def _coerce_49(value: 'PyComprehension') -> 'PyComprehension':
    return value


@no_type_check
def _coerce_50(value: 'Sequence[PyComprehension]') -> 'list[PyComprehension]':
    new_elements = list()
    for value_element in value:
        new_elements.append(_coerce_49(value_element))
    return new_elements


@no_type_check
def _coerce_51(value: 'PyGlobalKeyword | None') -> 'PyGlobalKeyword':
    if value is None:
        return PyGlobalKeyword()
    elif isinstance(value, PyGlobalKeyword):
        return value
    else:
        raise ValueError('the coercion from PyGlobalKeyword | None to PyGlobalKeyword failed')


@no_type_check
def _coerce_52(value: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | ImmutablePunct[PyIdent | str, PyComma]') -> 'Punctuated[PyIdent, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_0(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_0(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_53(value: 'PyIfKeyword | None') -> 'PyIfKeyword':
    if value is None:
        return PyIfKeyword()
    elif isinstance(value, PyIfKeyword):
        return value
    else:
        raise ValueError('the coercion from PyIfKeyword | None to PyIfKeyword failed')


@no_type_check
def _coerce_54(value: 'PyIfCase') -> 'PyIfCase':
    return value


@no_type_check
def _coerce_55(value: 'PyElifCase') -> 'PyElifCase':
    return value


@no_type_check
def _coerce_56(value: 'Sequence[PyElifCase] | None') -> 'list[PyElifCase]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_55(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyElifCase] | None to list[PyElifCase] failed')


@no_type_check
def _coerce_57(value: 'PyElseCase | PyStmt | Sequence[PyStmt] | None') -> 'PyElseCase | None':
    if is_py_stmt(value) or isinstance(value, list):
        return PyElseCase(_coerce_27(value))
    elif isinstance(value, PyElseCase):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyElseCase | PyStmt | Sequence[PyStmt] | None to PyElseCase | None failed')


@no_type_check
def _coerce_58(value: 'PyFromKeyword | None') -> 'PyFromKeyword':
    if value is None:
        return PyFromKeyword()
    elif isinstance(value, PyFromKeyword):
        return value
    else:
        raise ValueError('the coercion from PyFromKeyword | None to PyFromKeyword failed')


@no_type_check
def _coerce_59(value: 'PyImportKeyword | None') -> 'PyImportKeyword':
    if value is None:
        return PyImportKeyword()
    elif isinstance(value, PyImportKeyword):
        return value
    else:
        raise ValueError('the coercion from PyImportKeyword | None to PyImportKeyword failed')


@no_type_check
def _coerce_60(value: 'PyAsterisk | PyFromAlias | PyIdent | str') -> 'PyFromAlias':
    if isinstance(value, PyAsterisk) or isinstance(value, PyIdent) or isinstance(value, str):
        return PyFromAlias(_coerce_43(value))
    elif isinstance(value, PyFromAlias):
        return value
    else:
        raise ValueError('the coercion from PyAsterisk | PyFromAlias | PyIdent | str to PyFromAlias failed')


@no_type_check
def _coerce_61(value: 'Sequence[tuple[PyAsterisk | PyFromAlias | PyIdent | str, PyComma | None]] | Sequence[PyAsterisk | PyFromAlias | PyIdent | str] | ImmutablePunct[PyAsterisk | PyFromAlias | PyIdent | str, PyComma]') -> 'Punctuated[PyFromAlias, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_60(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_60(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_62(value: 'PyAlias | PyPath') -> 'PyAlias':
    if is_py_path(value):
        return PyAlias(_coerce_2(value))
    elif isinstance(value, PyAlias):
        return value
    else:
        raise ValueError('the coercion from PyAlias | PyPath to PyAlias failed')


@no_type_check
def _coerce_63(value: 'Sequence[tuple[PyAlias | PyPath, PyComma | None]] | Sequence[PyAlias | PyPath] | ImmutablePunct[PyAlias | PyPath, PyComma]') -> 'Punctuated[PyAlias, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_62(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_62(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_64(value: 'PyInfixOp') -> 'PyInfixOp':
    return value


@no_type_check
def _coerce_65(value: 'PyAsterisk | None') -> 'PyAsterisk':
    if value is None:
        return PyAsterisk()
    elif isinstance(value, PyAsterisk):
        return value
    else:
        raise ValueError('the coercion from PyAsterisk | None to PyAsterisk failed')


@no_type_check
def _coerce_66(value: 'PyLambdaKeyword | None') -> 'PyLambdaKeyword':
    if value is None:
        return PyLambdaKeyword()
    elif isinstance(value, PyLambdaKeyword):
        return value
    else:
        raise ValueError('the coercion from PyLambdaKeyword | None to PyLambdaKeyword failed')


@no_type_check
def _coerce_67(value: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None') -> 'Punctuated[PyPattern, PyComma]':
    if value is None:
        return Punctuated()
    elif isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        new_value = Punctuated()
        iterator = iter(value)
        try:
            first_element = next(iterator)
            while True:
                try:
                    second_element = next(iterator)
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        element_separator = first_element[1]
                        assert(element_separator is not None)
                    else:
                        element_value = first_element
                        element_separator = PyComma()
                    new_element_value = _coerce_5(element_value)
                    new_element_separator = _coerce_16(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_5(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | ImmutablePunct[PyPattern, PyComma] | None to Punctuated[PyPattern, PyComma] failed')


@no_type_check
def _coerce_68(value: 'PyOpenBracket | None') -> 'PyOpenBracket':
    if value is None:
        return PyOpenBracket()
    elif isinstance(value, PyOpenBracket):
        return value
    else:
        raise ValueError('the coercion from PyOpenBracket | None to PyOpenBracket failed')


@no_type_check
def _coerce_69(value: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None') -> 'Punctuated[PyExpr, PyComma]':
    if value is None:
        return Punctuated()
    elif isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        new_value = Punctuated()
        iterator = iter(value)
        try:
            first_element = next(iterator)
            while True:
                try:
                    second_element = next(iterator)
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        element_separator = first_element[1]
                        assert(element_separator is not None)
                    else:
                        element_value = first_element
                        element_separator = PyComma()
                    new_element_value = _coerce_6(element_value)
                    new_element_separator = _coerce_16(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_6(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None to Punctuated[PyExpr, PyComma] failed')


@no_type_check
def _coerce_70(value: 'PyCloseBracket | None') -> 'PyCloseBracket':
    if value is None:
        return PyCloseBracket()
    elif isinstance(value, PyCloseBracket):
        return value
    else:
        raise ValueError('the coercion from PyCloseBracket | None to PyCloseBracket failed')


@no_type_check
def _coerce_71(value: 'Sequence[PyStmt] | None') -> 'list[PyStmt]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_26(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyStmt] | None to list[PyStmt] failed')


@no_type_check
def _coerce_72(value: 'PyNonlocalKeyword | None') -> 'PyNonlocalKeyword':
    if value is None:
        return PyNonlocalKeyword()
    elif isinstance(value, PyNonlocalKeyword):
        return value
    else:
        raise ValueError('the coercion from PyNonlocalKeyword | None to PyNonlocalKeyword failed')


@no_type_check
def _coerce_73(value: 'PyPassKeyword | None') -> 'PyPassKeyword':
    if value is None:
        return PyPassKeyword()
    elif isinstance(value, PyPassKeyword):
        return value
    else:
        raise ValueError('the coercion from PyPassKeyword | None to PyPassKeyword failed')


@no_type_check
def _coerce_74(value: 'PyPattern | None') -> 'PyPattern | None':
    if is_py_pattern(value):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyPattern | None to PyPattern | None failed')


@no_type_check
def _coerce_75(value: 'PyPattern | tuple[PyColon | None, PyPattern] | None') -> 'tuple[PyColon, PyPattern] | None':
    if is_py_pattern(value):
        return (PyColon(), _coerce_5(value))
    elif isinstance(value, tuple):
        return (_coerce_7(value[0]), _coerce_5(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyPattern | tuple[PyColon | None, PyPattern] | None to tuple[PyColon, PyPattern] | None failed')


@no_type_check
def _coerce_76(value: 'PySlash | None') -> 'PySlash':
    if value is None:
        return PySlash()
    elif isinstance(value, PySlash):
        return value
    else:
        raise ValueError('the coercion from PySlash | None to PySlash failed')


@no_type_check
def _coerce_77(value: 'PyPrefixOp') -> 'PyPrefixOp':
    return value


@no_type_check
def _coerce_78(value: 'PyIdent | tuple[PyIdent | str, PyDot | None] | str') -> 'tuple[PyIdent, PyDot]':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return (_coerce_0(value), PyDot())
    elif isinstance(value, tuple):
        return (_coerce_0(value[0]), _coerce_11(value[1]))
    else:
        raise ValueError('the coercion from PyIdent | tuple[PyIdent | str, PyDot | None] | str to tuple[PyIdent, PyDot] failed')


@no_type_check
def _coerce_79(value: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None') -> 'list[tuple[PyIdent, PyDot]]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_78(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None to list[tuple[PyIdent, PyDot]] failed')


@no_type_check
def _coerce_80(value: 'PyRaiseKeyword | None') -> 'PyRaiseKeyword':
    if value is None:
        return PyRaiseKeyword()
    elif isinstance(value, PyRaiseKeyword):
        return value
    else:
        raise ValueError('the coercion from PyRaiseKeyword | None to PyRaiseKeyword failed')


@no_type_check
def _coerce_81(value: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None') -> 'tuple[PyFromKeyword, PyExpr] | None':
    if is_py_expr(value):
        return (PyFromKeyword(), _coerce_6(value))
    elif isinstance(value, tuple):
        return (_coerce_58(value[0]), _coerce_6(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyFromKeyword | None, PyExpr] | None to tuple[PyFromKeyword, PyExpr] | None failed')


@no_type_check
def _coerce_82(value: 'PyDot') -> 'PyDot':
    return value


@no_type_check
def _coerce_83(value: 'Sequence[PyDot] | int') -> 'list[PyDot]':
    if isinstance(value, int):
        new_elements = list()
        for _ in range(0, value):
            new_elements.append(PyDot())
        return new_elements
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_82(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyDot] | int to list[PyDot] failed')


@no_type_check
def _coerce_84(value: 'PyIdent | PyQualName | None | str') -> 'PyQualName | None':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return PyQualName(_coerce_0(value))
    elif isinstance(value, PyQualName):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyIdent | PyQualName | None | str to PyQualName | None failed')


@no_type_check
def _coerce_85(value: 'PyAsteriskAsterisk | None') -> 'PyAsteriskAsterisk':
    if value is None:
        return PyAsteriskAsterisk()
    elif isinstance(value, PyAsteriskAsterisk):
        return value
    else:
        raise ValueError('the coercion from PyAsteriskAsterisk | None to PyAsteriskAsterisk failed')


@no_type_check
def _coerce_86(value: 'PyReturnKeyword | None') -> 'PyReturnKeyword':
    if value is None:
        return PyReturnKeyword()
    elif isinstance(value, PyReturnKeyword):
        return value
    else:
        raise ValueError('the coercion from PyReturnKeyword | None to PyReturnKeyword failed')


@no_type_check
def _coerce_87(value: 'PyExpr | PyExprSlice') -> 'PyExpr | PyExprSlice':
    if is_py_expr(value):
        return value
    elif isinstance(value, PyExprSlice):
        return value
    else:
        raise ValueError('the coercion from PyExpr | PyExprSlice to PyExpr | PyExprSlice failed')


@no_type_check
def _coerce_88(value: 'Sequence[tuple[PyExpr | PyExprSlice, PyComma | None]] | Sequence[PyExpr | PyExprSlice] | ImmutablePunct[PyExpr | PyExprSlice, PyComma]') -> 'Punctuated[PyExpr | PyExprSlice, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_87(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_87(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_89(value: 'PyPattern | PyPatternSlice') -> 'PyPattern | PyPatternSlice':
    if is_py_pattern(value):
        return value
    elif isinstance(value, PyPatternSlice):
        return value
    else:
        raise ValueError('the coercion from PyPattern | PyPatternSlice to PyPattern | PyPatternSlice failed')


@no_type_check
def _coerce_90(value: 'Sequence[tuple[PyPattern | PyPatternSlice, PyComma | None]] | Sequence[PyPattern | PyPatternSlice] | ImmutablePunct[PyPattern | PyPatternSlice, PyComma]') -> 'Punctuated[PyPattern | PyPatternSlice, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_89(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_89(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_91(value: 'PyTryKeyword | None') -> 'PyTryKeyword':
    if value is None:
        return PyTryKeyword()
    elif isinstance(value, PyTryKeyword):
        return value
    else:
        raise ValueError('the coercion from PyTryKeyword | None to PyTryKeyword failed')


@no_type_check
def _coerce_92(value: 'PyExceptHandler') -> 'PyExceptHandler':
    return value


@no_type_check
def _coerce_93(value: 'Sequence[PyExceptHandler] | None') -> 'list[PyExceptHandler]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_92(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyExceptHandler] | None to list[PyExceptHandler] failed')


@no_type_check
def _coerce_94(value: 'PyFinallyKeyword | None') -> 'PyFinallyKeyword':
    if value is None:
        return PyFinallyKeyword()
    elif isinstance(value, PyFinallyKeyword):
        return value
    else:
        raise ValueError('the coercion from PyFinallyKeyword | None to PyFinallyKeyword failed')


@no_type_check
def _coerce_95(value: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None') -> 'tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None':
    if is_py_stmt(value) or isinstance(value, list):
        return (PyFinallyKeyword(), PyColon(), _coerce_27(value))
    elif isinstance(value, tuple):
        return (_coerce_94(value[0]), _coerce_7(value[1]), _coerce_27(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None to tuple[PyFinallyKeyword, PyColon, PyStmt | list[PyStmt]] | None failed')


@no_type_check
def _coerce_96(value: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma]') -> 'Punctuated[PyExpr, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_6(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_6(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_97(value: 'PyComma | None') -> 'PyComma':
    if value is None:
        return PyComma()
    elif isinstance(value, PyComma):
        return value
    else:
        raise ValueError('the coercion from PyComma | None to PyComma failed')


@no_type_check
def _coerce_98(value: 'PyTypeKeyword | None') -> 'PyTypeKeyword':
    if value is None:
        return PyTypeKeyword()
    elif isinstance(value, PyTypeKeyword):
        return value
    else:
        raise ValueError('the coercion from PyTypeKeyword | None to PyTypeKeyword failed')


@no_type_check
def _coerce_99(value: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma]') -> 'Punctuated[PyExpr, PyComma]':
    new_value = Punctuated()
    iterator = iter(value)
    try:
        first_element = next(iterator)
        while True:
            try:
                second_element = next(iterator)
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    element_separator = first_element[1]
                    assert(element_separator is not None)
                else:
                    element_value = first_element
                    element_separator = PyComma()
                new_element_value = _coerce_6(element_value)
                new_element_separator = _coerce_16(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_6(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_100(value: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None') -> 'tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (PyOpenBracket(), _coerce_99(value), PyCloseBracket())
    elif isinstance(value, tuple):
        return (_coerce_68(value[0]), _coerce_69(value[1]), _coerce_70(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | ImmutablePunct[PyExpr, PyComma] | None to tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None failed')


@no_type_check
def _coerce_101(value: 'PyWhileKeyword | None') -> 'PyWhileKeyword':
    if value is None:
        return PyWhileKeyword()
    elif isinstance(value, PyWhileKeyword):
        return value
    else:
        raise ValueError('the coercion from PyWhileKeyword | None to PyWhileKeyword failed')


@no_type_check
def for_each_child_py_arg(node: PyArg, proc: Callable[[PyArg], None]) -> None:
    if isinstance(node, PyAssignStmt):
        if isinstance(node.annotation, tuple):
            if isinstance(node.annotation[1], PyAttrExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyCallExpr):
                proc(node.annotation[1].operator)
                for (element_0, separator_0) in node.annotation[1].args:
                    proc(element_0)
            elif isinstance(node.annotation[1], PyGeneratorExpr):
                proc(node.annotation[1].element)
                for element_1 in node.annotation[1].generators:
                    proc(element_1.target)
                    for element_2 in element_1.guards:
                        proc(element_2.expr)
            elif isinstance(node.annotation[1], PyIfExpr):
                proc(node.annotation[1].then)
                proc(node.annotation[1].test)
                proc(node.annotation[1].alt)
            elif isinstance(node.annotation[1], PyInfixExpr):
                proc(node.annotation[1].left)
                proc(node.annotation[1].right)
            elif isinstance(node.annotation[1], PyLambdaExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyListExpr):
                for (element_3, separator_1) in node.annotation[1].elements:
                    proc(element_3)
            elif isinstance(node.annotation[1], PyNestExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyPrefixExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyStarredExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PySubscriptExpr):
                proc(node.annotation[1].expr)
                for (element_4, separator_2) in node.annotation[1].slices:
                    if is_py_expr(element_4):
                        proc(element_4)
                    elif isinstance(element_4, PyExprSlice):
                        if is_py_expr(element_4.lower):
                            proc(element_4.lower)
                        if is_py_expr(element_4.upper):
                            proc(element_4.upper)
                        if isinstance(element_4.step, tuple):
                            proc(element_4.step[1])
            elif is_py_tuple_expr(node.annotation[1]):
                if isinstance(node.annotation[1], PyTupleOne):
                    proc(node.annotation[1].expr)
                elif isinstance(node.annotation[1], PyTupleMany):
                    for (element_5, separator_3) in node.annotation[1].elements:
                        proc(element_5)
        if isinstance(node.value, tuple):
            proc(node.value[1])
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PyAugAssignStmt):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element_6, separator_4) in node.args:
            proc(element_6)
        return
    if isinstance(node, PyClassDef):
        for element_7 in node.decorators:
            proc(element_7.expr)
        if isinstance(node.bases, tuple):
            for (element_8, separator_5) in node.bases[1]:
                if isinstance(element_8, PyKeywordBaseArg):
                    proc(element_8.expr)
        if is_py_stmt(node.body):
            if isinstance(node.body, PyAssignStmt):
                if isinstance(node.body.annotation, tuple):
                    proc(node.body.annotation[1])
                if isinstance(node.body.value, tuple):
                    proc(node.body.value[1])
            elif isinstance(node.body, PyAugAssignStmt):
                if isinstance(node.body.annotation, tuple):
                    proc(node.body.annotation[1])
                proc(node.body.expr)
            elif isinstance(node.body, PyClassDef):
                for element_9 in node.body.decorators:
                    proc(element_9)
                if isinstance(node.body.bases, tuple):
                    for (element_10, separator_6) in node.body.bases[1]:
                        proc(element_10)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_11 in node.body.body:
                        proc(element_11)
            elif isinstance(node.body, PyExprStmt):
                proc(node.body.expr)
            elif isinstance(node.body, PyForStmt):
                proc(node.body.expr)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_12 in node.body.body:
                        proc(element_12)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_13 in node.body.else_clause[2]:
                            proc(element_13)
            elif isinstance(node.body, PyFuncDef):
                for element_14 in node.body.decorators:
                    proc(element_14)
                for (element_15, separator_7) in node.body.params:
                    if isinstance(element_15, PyRestPosParam):
                        if isinstance(element_15.annotation, tuple):
                            proc(element_15.annotation[1])
                    elif isinstance(element_15, PyRestKeywordParam):
                        if isinstance(element_15.annotation, tuple):
                            proc(element_15.annotation[1])
                    elif isinstance(element_15, PyNamedParam):
                        if isinstance(element_15.annotation, tuple):
                            proc(element_15.annotation[1])
                        if isinstance(element_15.default, tuple):
                            proc(element_15.default[1])
                if isinstance(node.body.return_type, tuple):
                    proc(node.body.return_type[1])
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_16 in node.body.body:
                        proc(element_16)
            elif isinstance(node.body, PyIfStmt):
                proc(node.body.first.test)
                if is_py_stmt(node.body.first.body):
                    proc(node.body.first.body)
                elif isinstance(node.body.first.body, list):
                    for element_17 in node.body.first.body:
                        proc(element_17)
                for element_18 in node.body.alternatives:
                    proc(element_18.test)
                    if is_py_stmt(element_18.body):
                        proc(element_18.body)
                    elif isinstance(element_18.body, list):
                        for element_19 in element_18.body:
                            proc(element_19)
                if isinstance(node.body.last, PyElseCase):
                    if is_py_stmt(node.body.last.body):
                        proc(node.body.last.body)
                    elif isinstance(node.body.last.body, list):
                        for element_20 in node.body.last.body:
                            proc(element_20)
            elif isinstance(node.body, PyRaiseStmt):
                proc(node.body.expr)
                if isinstance(node.body.cause, tuple):
                    proc(node.body.cause[1])
            elif isinstance(node.body, PyRetStmt):
                if is_py_expr(node.body.expr):
                    proc(node.body.expr)
            elif isinstance(node.body, PyTryStmt):
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_21 in node.body.body:
                        proc(element_21)
                for element_22 in node.body.handlers:
                    proc(element_22.expr)
                    if is_py_stmt(element_22.body):
                        proc(element_22.body)
                    elif isinstance(element_22.body, list):
                        for element_23 in element_22.body:
                            proc(element_23)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_24 in node.body.else_clause[2]:
                            proc(element_24)
                if isinstance(node.body.finally_clause, tuple):
                    if is_py_stmt(node.body.finally_clause[2]):
                        proc(node.body.finally_clause[2])
                    elif isinstance(node.body.finally_clause[2], list):
                        for element_25 in node.body.finally_clause[2]:
                            proc(element_25)
            elif isinstance(node.body, PyTypeAliasStmt):
                if isinstance(node.body.type_params, tuple):
                    for (element_26, separator_8) in node.body.type_params[1]:
                        proc(element_26)
                proc(node.body.expr)
            elif isinstance(node.body, PyWhileStmt):
                proc(node.body.expr)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_27 in node.body.body:
                        proc(element_27)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_28 in node.body.else_clause[2]:
                            proc(element_28)
        elif isinstance(node.body, list):
            for element_29 in node.body:
                proc(element_29)
        return
    if isinstance(node, PyComprehension):
        proc(node.target)
        for element_30 in node.guards:
            proc(element_30)
        return
    if isinstance(node, PyDecorator):
        proc(node.expr)
        return
    if isinstance(node, PyElifCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_31 in node.body:
                proc(element_31)
        return
    if isinstance(node, PyElseCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_32 in node.body:
                proc(element_32)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_33 in node.body:
                proc(element_33)
        return
    if isinstance(node, PyExprSlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        if is_py_expr(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[1])
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyForStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_34 in node.body:
                proc(element_34)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_35 in node.else_clause[2]:
                    proc(element_35)
        return
    if isinstance(node, PyFuncDef):
        for element_36 in node.decorators:
            proc(element_36)
        for (element_37, separator_9) in node.params:
            proc(element_37)
        if isinstance(node.return_type, tuple):
            proc(node.return_type[1])
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_38 in node.body:
                proc(element_38)
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element_39 in node.generators:
            proc(element_39)
        return
    if isinstance(node, PyGuard):
        proc(node.expr)
        return
    if isinstance(node, PyIfCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_40 in node.body:
                proc(element_40)
        return
    if isinstance(node, PyIfExpr):
        proc(node.then)
        proc(node.test)
        proc(node.alt)
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element_41 in node.alternatives:
            proc(element_41)
        if isinstance(node.last, PyElseCase):
            proc(node.last)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyKeywordBaseArg):
        proc(node.expr)
        return
    if isinstance(node, PyLambdaExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element_42, separator_10) in node.elements:
            proc(element_42)
        return
    if isinstance(node, PyModule):
        for element_43 in node.stmts:
            proc(element_43)
        return
    if isinstance(node, PyNamedParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.default, tuple):
            proc(node.default[1])
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.expr)
        if isinstance(node.cause, tuple):
            proc(node.cause[1])
        return
    if isinstance(node, PyRestKeywordParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRestPosParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRetStmt):
        if is_py_expr(node.expr):
            proc(node.expr)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element_44, separator_11) in node.slices:
            if is_py_expr(element_44):
                proc(element_44)
            elif isinstance(element_44, PyExprSlice):
                proc(element_44)
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_45 in node.body:
                proc(element_45)
        for element_46 in node.handlers:
            proc(element_46)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_47 in node.else_clause[2]:
                    proc(element_47)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_48 in node.finally_clause[2]:
                    proc(element_48)
        return
    if isinstance(node, PyTupleMany):
        for (element_49, separator_12) in node.elements:
            proc(element_49)
        return
    if isinstance(node, PyTupleOne):
        proc(node.expr)
        return
    if isinstance(node, PyTypeAliasStmt):
        if isinstance(node.type_params, tuple):
            for (element_50, separator_13) in node.type_params[1]:
                proc(element_50)
        proc(node.expr)
        return
    if isinstance(node, PyWhileStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_51 in node.body:
                proc(element_51)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_52 in node.else_clause[2]:
                    proc(element_52)
        return


@no_type_check
def for_each_child_py_expr(node: PyExpr, proc: Callable[[PyExpr], None]) -> None:
    if isinstance(node, PyAssignStmt):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.value, tuple):
            proc(node.value[1])
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PyAugAssignStmt):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element_0, separator_0) in node.args:
            if isinstance(element_0, PyKeywordArg):
                proc(element_0.expr)
            elif is_py_expr(element_0):
                proc(element_0)
        return
    if isinstance(node, PyClassDef):
        for element_1 in node.decorators:
            proc(element_1.expr)
        if isinstance(node.bases, tuple):
            for (element_2, separator_1) in node.bases[1]:
                if isinstance(element_2, PyKeywordBaseArg):
                    proc(element_2.expr)
        if is_py_stmt(node.body):
            if isinstance(node.body, PyAssignStmt):
                if isinstance(node.body.annotation, tuple):
                    proc(node.body.annotation[1])
                if isinstance(node.body.value, tuple):
                    proc(node.body.value[1])
            elif isinstance(node.body, PyAugAssignStmt):
                if isinstance(node.body.annotation, tuple):
                    proc(node.body.annotation[1])
                proc(node.body.expr)
            elif isinstance(node.body, PyClassDef):
                for element_3 in node.body.decorators:
                    proc(element_3)
                if isinstance(node.body.bases, tuple):
                    for (element_4, separator_2) in node.body.bases[1]:
                        proc(element_4)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_5 in node.body.body:
                        proc(element_5)
            elif isinstance(node.body, PyExprStmt):
                proc(node.body.expr)
            elif isinstance(node.body, PyForStmt):
                proc(node.body.expr)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_6 in node.body.body:
                        proc(element_6)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_7 in node.body.else_clause[2]:
                            proc(element_7)
            elif isinstance(node.body, PyFuncDef):
                for element_8 in node.body.decorators:
                    proc(element_8)
                for (element_9, separator_3) in node.body.params:
                    if isinstance(element_9, PyRestPosParam):
                        if isinstance(element_9.annotation, tuple):
                            proc(element_9.annotation[1])
                    elif isinstance(element_9, PyRestKeywordParam):
                        if isinstance(element_9.annotation, tuple):
                            proc(element_9.annotation[1])
                    elif isinstance(element_9, PyNamedParam):
                        if isinstance(element_9.annotation, tuple):
                            proc(element_9.annotation[1])
                        if isinstance(element_9.default, tuple):
                            proc(element_9.default[1])
                if isinstance(node.body.return_type, tuple):
                    proc(node.body.return_type[1])
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_10 in node.body.body:
                        proc(element_10)
            elif isinstance(node.body, PyIfStmt):
                proc(node.body.first.test)
                if is_py_stmt(node.body.first.body):
                    proc(node.body.first.body)
                elif isinstance(node.body.first.body, list):
                    for element_11 in node.body.first.body:
                        proc(element_11)
                for element_12 in node.body.alternatives:
                    proc(element_12.test)
                    if is_py_stmt(element_12.body):
                        proc(element_12.body)
                    elif isinstance(element_12.body, list):
                        for element_13 in element_12.body:
                            proc(element_13)
                if isinstance(node.body.last, PyElseCase):
                    if is_py_stmt(node.body.last.body):
                        proc(node.body.last.body)
                    elif isinstance(node.body.last.body, list):
                        for element_14 in node.body.last.body:
                            proc(element_14)
            elif isinstance(node.body, PyRaiseStmt):
                proc(node.body.expr)
                if isinstance(node.body.cause, tuple):
                    proc(node.body.cause[1])
            elif isinstance(node.body, PyRetStmt):
                if is_py_expr(node.body.expr):
                    proc(node.body.expr)
            elif isinstance(node.body, PyTryStmt):
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_15 in node.body.body:
                        proc(element_15)
                for element_16 in node.body.handlers:
                    proc(element_16.expr)
                    if is_py_stmt(element_16.body):
                        proc(element_16.body)
                    elif isinstance(element_16.body, list):
                        for element_17 in element_16.body:
                            proc(element_17)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_18 in node.body.else_clause[2]:
                            proc(element_18)
                if isinstance(node.body.finally_clause, tuple):
                    if is_py_stmt(node.body.finally_clause[2]):
                        proc(node.body.finally_clause[2])
                    elif isinstance(node.body.finally_clause[2], list):
                        for element_19 in node.body.finally_clause[2]:
                            proc(element_19)
            elif isinstance(node.body, PyTypeAliasStmt):
                if isinstance(node.body.type_params, tuple):
                    for (element_20, separator_4) in node.body.type_params[1]:
                        proc(element_20)
                proc(node.body.expr)
            elif isinstance(node.body, PyWhileStmt):
                proc(node.body.expr)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_21 in node.body.body:
                        proc(element_21)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_22 in node.body.else_clause[2]:
                            proc(element_22)
        elif isinstance(node.body, list):
            for element_23 in node.body:
                proc(element_23)
        return
    if isinstance(node, PyComprehension):
        proc(node.target)
        for element_24 in node.guards:
            proc(element_24.expr)
        return
    if isinstance(node, PyDecorator):
        proc(node.expr)
        return
    if isinstance(node, PyElifCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_25 in node.body:
                proc(element_25)
        return
    if isinstance(node, PyElseCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_26 in node.body:
                proc(element_26)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_27 in node.body:
                proc(element_27)
        return
    if isinstance(node, PyExprSlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        if is_py_expr(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[1])
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyForStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_28 in node.body:
                proc(element_28)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_29 in node.else_clause[2]:
                    proc(element_29)
        return
    if isinstance(node, PyFuncDef):
        for element_30 in node.decorators:
            proc(element_30)
        for (element_31, separator_5) in node.params:
            proc(element_31)
        if isinstance(node.return_type, tuple):
            proc(node.return_type[1])
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_32 in node.body:
                proc(element_32)
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element_33 in node.generators:
            proc(element_33.target)
            for element_34 in element_33.guards:
                proc(element_34)
        return
    if isinstance(node, PyGuard):
        proc(node.expr)
        return
    if isinstance(node, PyIfCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_35 in node.body:
                proc(element_35)
        return
    if isinstance(node, PyIfExpr):
        proc(node.then)
        proc(node.test)
        proc(node.alt)
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element_36 in node.alternatives:
            proc(element_36)
        if isinstance(node.last, PyElseCase):
            proc(node.last)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyKeywordBaseArg):
        proc(node.expr)
        return
    if isinstance(node, PyLambdaExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element_37, separator_6) in node.elements:
            proc(element_37)
        return
    if isinstance(node, PyModule):
        for element_38 in node.stmts:
            proc(element_38)
        return
    if isinstance(node, PyNamedParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.default, tuple):
            proc(node.default[1])
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.expr)
        if isinstance(node.cause, tuple):
            proc(node.cause[1])
        return
    if isinstance(node, PyRestKeywordParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRestPosParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRetStmt):
        if is_py_expr(node.expr):
            proc(node.expr)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element_39, separator_7) in node.slices:
            if is_py_expr(element_39):
                proc(element_39)
            elif isinstance(element_39, PyExprSlice):
                if is_py_expr(element_39.lower):
                    proc(element_39.lower)
                if is_py_expr(element_39.upper):
                    proc(element_39.upper)
                if isinstance(element_39.step, tuple):
                    proc(element_39.step[1])
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_40 in node.body:
                proc(element_40)
        for element_41 in node.handlers:
            proc(element_41)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_42 in node.else_clause[2]:
                    proc(element_42)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_43 in node.finally_clause[2]:
                    proc(element_43)
        return
    if isinstance(node, PyTupleMany):
        for (element_44, separator_8) in node.elements:
            proc(element_44)
        return
    if isinstance(node, PyTupleOne):
        proc(node.expr)
        return
    if isinstance(node, PyTypeAliasStmt):
        if isinstance(node.type_params, tuple):
            for (element_45, separator_9) in node.type_params[1]:
                proc(element_45)
        proc(node.expr)
        return
    if isinstance(node, PyWhileStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_46 in node.body:
                proc(element_46)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_47 in node.else_clause[2]:
                    proc(element_47)
        return


@no_type_check
def for_each_child_py_pattern(node: PyPattern, proc: Callable[[PyPattern], None]) -> None:
    if isinstance(node, PyAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            if isinstance(node.annotation[1], PyAttrExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyCallExpr):
                proc(node.annotation[1].operator)
                for (element_0, separator_0) in node.annotation[1].args:
                    if isinstance(element_0, PyKeywordArg):
                        proc(element_0.expr)
                    elif is_py_expr(element_0):
                        proc(element_0)
            elif isinstance(node.annotation[1], PyGeneratorExpr):
                proc(node.annotation[1].element)
                for element_1 in node.annotation[1].generators:
                    proc(element_1.pattern)
                    proc(element_1.target)
                    for element_2 in element_1.guards:
                        proc(element_2.expr)
            elif isinstance(node.annotation[1], PyIfExpr):
                proc(node.annotation[1].then)
                proc(node.annotation[1].test)
                proc(node.annotation[1].alt)
            elif isinstance(node.annotation[1], PyInfixExpr):
                proc(node.annotation[1].left)
                proc(node.annotation[1].right)
            elif isinstance(node.annotation[1], PyLambdaExpr):
                for (element_3, separator_1) in node.annotation[1].params:
                    proc(element_3)
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyListExpr):
                for (element_4, separator_2) in node.annotation[1].elements:
                    proc(element_4)
            elif isinstance(node.annotation[1], PyNestExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyPrefixExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PyStarredExpr):
                proc(node.annotation[1].expr)
            elif isinstance(node.annotation[1], PySubscriptExpr):
                proc(node.annotation[1].expr)
                for (element_5, separator_3) in node.annotation[1].slices:
                    if is_py_expr(element_5):
                        proc(element_5)
                    elif isinstance(element_5, PyExprSlice):
                        if is_py_expr(element_5.lower):
                            proc(element_5.lower)
                        if is_py_expr(element_5.upper):
                            proc(element_5.upper)
                        if isinstance(element_5.step, tuple):
                            proc(element_5.step[1])
            elif is_py_tuple_expr(node.annotation[1]):
                if isinstance(node.annotation[1], PyTupleOne):
                    proc(node.annotation[1].expr)
                elif isinstance(node.annotation[1], PyTupleMany):
                    for (element_6, separator_4) in node.annotation[1].elements:
                        proc(element_6)
        if isinstance(node.value, tuple):
            proc(node.value[1])
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        return
    if isinstance(node, PyAugAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element_7, separator_5) in node.args:
            proc(element_7)
        return
    if isinstance(node, PyClassDef):
        for element_8 in node.decorators:
            proc(element_8.expr)
        if isinstance(node.bases, tuple):
            for (element_9, separator_6) in node.bases[1]:
                if isinstance(element_9, PyKeywordBaseArg):
                    proc(element_9.expr)
        if is_py_stmt(node.body):
            if isinstance(node.body, PyAssignStmt):
                proc(node.body.pattern)
                if isinstance(node.body.annotation, tuple):
                    proc(node.body.annotation[1])
                if isinstance(node.body.value, tuple):
                    proc(node.body.value[1])
            elif isinstance(node.body, PyAugAssignStmt):
                proc(node.body.pattern)
                if isinstance(node.body.annotation, tuple):
                    proc(node.body.annotation[1])
                proc(node.body.expr)
            elif isinstance(node.body, PyClassDef):
                for element_10 in node.body.decorators:
                    proc(element_10)
                if isinstance(node.body.bases, tuple):
                    for (element_11, separator_7) in node.body.bases[1]:
                        proc(element_11)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_12 in node.body.body:
                        proc(element_12)
            elif isinstance(node.body, PyDeleteStmt):
                proc(node.body.pattern)
            elif isinstance(node.body, PyExprStmt):
                proc(node.body.expr)
            elif isinstance(node.body, PyForStmt):
                proc(node.body.pattern)
                proc(node.body.expr)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_13 in node.body.body:
                        proc(element_13)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_14 in node.body.else_clause[2]:
                            proc(element_14)
            elif isinstance(node.body, PyFuncDef):
                for element_15 in node.body.decorators:
                    proc(element_15)
                for (element_16, separator_8) in node.body.params:
                    if isinstance(element_16, PyRestPosParam):
                        if isinstance(element_16.annotation, tuple):
                            proc(element_16.annotation[1])
                    elif isinstance(element_16, PyRestKeywordParam):
                        if isinstance(element_16.annotation, tuple):
                            proc(element_16.annotation[1])
                    elif isinstance(element_16, PyNamedParam):
                        proc(element_16.pattern)
                        if isinstance(element_16.annotation, tuple):
                            proc(element_16.annotation[1])
                        if isinstance(element_16.default, tuple):
                            proc(element_16.default[1])
                if isinstance(node.body.return_type, tuple):
                    proc(node.body.return_type[1])
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_17 in node.body.body:
                        proc(element_17)
            elif isinstance(node.body, PyIfStmt):
                proc(node.body.first.test)
                if is_py_stmt(node.body.first.body):
                    proc(node.body.first.body)
                elif isinstance(node.body.first.body, list):
                    for element_18 in node.body.first.body:
                        proc(element_18)
                for element_19 in node.body.alternatives:
                    proc(element_19.test)
                    if is_py_stmt(element_19.body):
                        proc(element_19.body)
                    elif isinstance(element_19.body, list):
                        for element_20 in element_19.body:
                            proc(element_20)
                if isinstance(node.body.last, PyElseCase):
                    if is_py_stmt(node.body.last.body):
                        proc(node.body.last.body)
                    elif isinstance(node.body.last.body, list):
                        for element_21 in node.body.last.body:
                            proc(element_21)
            elif isinstance(node.body, PyRaiseStmt):
                proc(node.body.expr)
                if isinstance(node.body.cause, tuple):
                    proc(node.body.cause[1])
            elif isinstance(node.body, PyRetStmt):
                if is_py_expr(node.body.expr):
                    proc(node.body.expr)
            elif isinstance(node.body, PyTryStmt):
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_22 in node.body.body:
                        proc(element_22)
                for element_23 in node.body.handlers:
                    proc(element_23.expr)
                    if is_py_stmt(element_23.body):
                        proc(element_23.body)
                    elif isinstance(element_23.body, list):
                        for element_24 in element_23.body:
                            proc(element_24)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_25 in node.body.else_clause[2]:
                            proc(element_25)
                if isinstance(node.body.finally_clause, tuple):
                    if is_py_stmt(node.body.finally_clause[2]):
                        proc(node.body.finally_clause[2])
                    elif isinstance(node.body.finally_clause[2], list):
                        for element_26 in node.body.finally_clause[2]:
                            proc(element_26)
            elif isinstance(node.body, PyTypeAliasStmt):
                if isinstance(node.body.type_params, tuple):
                    for (element_27, separator_9) in node.body.type_params[1]:
                        proc(element_27)
                proc(node.body.expr)
            elif isinstance(node.body, PyWhileStmt):
                proc(node.body.expr)
                if is_py_stmt(node.body.body):
                    proc(node.body.body)
                elif isinstance(node.body.body, list):
                    for element_28 in node.body.body:
                        proc(element_28)
                if isinstance(node.body.else_clause, tuple):
                    if is_py_stmt(node.body.else_clause[2]):
                        proc(node.body.else_clause[2])
                    elif isinstance(node.body.else_clause[2], list):
                        for element_29 in node.body.else_clause[2]:
                            proc(element_29)
        elif isinstance(node.body, list):
            for element_30 in node.body:
                proc(element_30)
        return
    if isinstance(node, PyComprehension):
        proc(node.pattern)
        proc(node.target)
        for element_31 in node.guards:
            proc(element_31)
        return
    if isinstance(node, PyDecorator):
        proc(node.expr)
        return
    if isinstance(node, PyDeleteStmt):
        proc(node.pattern)
        return
    if isinstance(node, PyElifCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_32 in node.body:
                proc(element_32)
        return
    if isinstance(node, PyElseCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_33 in node.body:
                proc(element_33)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_34 in node.body:
                proc(element_34)
        return
    if isinstance(node, PyExprSlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        if is_py_expr(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[1])
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyForStmt):
        proc(node.pattern)
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_35 in node.body:
                proc(element_35)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_36 in node.else_clause[2]:
                    proc(element_36)
        return
    if isinstance(node, PyFuncDef):
        for element_37 in node.decorators:
            proc(element_37)
        for (element_38, separator_10) in node.params:
            proc(element_38)
        if isinstance(node.return_type, tuple):
            proc(node.return_type[1])
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_39 in node.body:
                proc(element_39)
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element_40 in node.generators:
            proc(element_40)
        return
    if isinstance(node, PyGuard):
        proc(node.expr)
        return
    if isinstance(node, PyIfCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_41 in node.body:
                proc(element_41)
        return
    if isinstance(node, PyIfExpr):
        proc(node.then)
        proc(node.test)
        proc(node.alt)
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element_42 in node.alternatives:
            proc(element_42)
        if isinstance(node.last, PyElseCase):
            proc(node.last)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyKeywordBaseArg):
        proc(node.expr)
        return
    if isinstance(node, PyLambdaExpr):
        for (element_43, separator_11) in node.params:
            proc(element_43)
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element_44, separator_12) in node.elements:
            proc(element_44)
        return
    if isinstance(node, PyListPattern):
        for (element_45, separator_13) in node.elements:
            proc(element_45)
        return
    if isinstance(node, PyModule):
        for element_46 in node.stmts:
            proc(element_46)
        return
    if isinstance(node, PyNamedParam):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.default, tuple):
            proc(node.default[1])
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyPatternSlice):
        if is_py_pattern(node.lower):
            proc(node.lower)
        if is_py_pattern(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[1])
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.expr)
        if isinstance(node.cause, tuple):
            proc(node.cause[1])
        return
    if isinstance(node, PyRestKeywordParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRestPosParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRetStmt):
        if is_py_expr(node.expr):
            proc(node.expr)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyStarredPattern):
        proc(node.pattern)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element_47, separator_14) in node.slices:
            if is_py_expr(element_47):
                proc(element_47)
            elif isinstance(element_47, PyExprSlice):
                proc(element_47)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        for (element_48, separator_15) in node.slices:
            if is_py_pattern(element_48):
                proc(element_48)
            elif isinstance(element_48, PyPatternSlice):
                if is_py_pattern(element_48.lower):
                    proc(element_48.lower)
                if is_py_pattern(element_48.upper):
                    proc(element_48.upper)
                if isinstance(element_48.step, tuple):
                    proc(element_48.step[1])
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_49 in node.body:
                proc(element_49)
        for element_50 in node.handlers:
            proc(element_50)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_51 in node.else_clause[2]:
                    proc(element_51)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_52 in node.finally_clause[2]:
                    proc(element_52)
        return
    if isinstance(node, PyTupleMany):
        for (element_53, separator_16) in node.elements:
            proc(element_53)
        return
    if isinstance(node, PyTupleOne):
        proc(node.expr)
        return
    if isinstance(node, PyTuplePattern):
        for (element_54, separator_17) in node.elements:
            proc(element_54)
        return
    if isinstance(node, PyTypeAliasStmt):
        if isinstance(node.type_params, tuple):
            for (element_55, separator_18) in node.type_params[1]:
                proc(element_55)
        proc(node.expr)
        return
    if isinstance(node, PyWhileStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_56 in node.body:
                proc(element_56)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_57 in node.else_clause[2]:
                    proc(element_57)
        return


@no_type_check
def for_each_child_py_stmt(node: PyStmt, proc: Callable[[PyStmt], None]) -> None:
    if isinstance(node, PyClassDef):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_0 in node.body:
                proc(element_0)
        return
    if isinstance(node, PyElifCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_1 in node.body:
                proc(element_1)
        return
    if isinstance(node, PyElseCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)
        return
    if isinstance(node, PyExceptHandler):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_3 in node.body:
                proc(element_3)
        return
    if isinstance(node, PyForStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_4 in node.body:
                proc(element_4)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_5 in node.else_clause[2]:
                    proc(element_5)
        return
    if isinstance(node, PyFuncDef):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_6 in node.body:
                proc(element_6)
        return
    if isinstance(node, PyIfCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_7 in node.body:
                proc(element_7)
        return
    if isinstance(node, PyIfStmt):
        if is_py_stmt(node.first.body):
            proc(node.first.body)
        elif isinstance(node.first.body, list):
            for element_8 in node.first.body:
                proc(element_8)
        for element_9 in node.alternatives:
            if is_py_stmt(element_9.body):
                proc(element_9.body)
            elif isinstance(element_9.body, list):
                for element_10 in element_9.body:
                    proc(element_10)
        if isinstance(node.last, PyElseCase):
            if is_py_stmt(node.last.body):
                proc(node.last.body)
            elif isinstance(node.last.body, list):
                for element_11 in node.last.body:
                    proc(element_11)
        return
    if isinstance(node, PyModule):
        for element_12 in node.stmts:
            proc(element_12)
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_13 in node.body:
                proc(element_13)
        for element_14 in node.handlers:
            if is_py_stmt(element_14.body):
                proc(element_14.body)
            elif isinstance(element_14.body, list):
                for element_15 in element_14.body:
                    proc(element_15)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_16 in node.else_clause[2]:
                    proc(element_16)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_17 in node.finally_clause[2]:
                    proc(element_17)
        return
    if isinstance(node, PyWhileStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_18 in node.body:
                proc(element_18)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_19 in node.else_clause[2]:
                    proc(element_19)
        return


@no_type_check
def rewrite_each_py_arg(node: PyArg, proc: Callable[[PyArg], PyArg]) -> PyArg:
    if isinstance(node, PyKeywordArg):
        changed_1 = False
        if isinstance(node.expr, PyAttrExpr):
            changed_2 = False
            new_expr_1 = proc(node.expr.expr)
            assert(is_py_expr(new_expr_1))
            if new_expr_1 is not node.expr.expr:
                changed_2 = True
            if changed_2:
                new_expr = PyAttrExpr(expr=new_expr_1, dot=node.expr.dot, name=node.expr.name)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyCallExpr):
            changed_3 = False
            new_operator = proc(node.expr.operator)
            assert(is_py_expr(new_operator))
            if new_operator is not node.expr.operator:
                changed_3 = True
            new_args = Punctuated()
            for (element, separator) in node.expr.args.delimited:
                new_element = proc(element)
                assert(is_py_arg(new_element))
                if new_element is not element:
                    changed_3 = True
                new_separator = separator
                new_args.append(new_element, new_separator)
            new_last = proc(node.expr.args.last)
            assert(is_py_arg(new_last))
            if new_last is not node.expr.args.last:
                changed_3 = True
            new_args.append_final(new_last)
            if changed_3:
                new_expr = PyCallExpr(operator=new_operator, open_paren=node.expr.open_paren, args=new_args, close_paren=node.expr.close_paren)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyConstExpr):
            new_expr = node.expr
        elif isinstance(node.expr, PyEllipsisExpr):
            new_expr = node.expr
        elif isinstance(node.expr, PyGeneratorExpr):
            changed_6 = False
            new_element_1 = proc(node.expr.element)
            assert(is_py_expr(new_element_1))
            if new_element_1 is not node.expr.element:
                changed_6 = True
            new_generators = []
            for element_1 in node.expr.generators:
                changed_7 = False
                new_target = proc(element_1.target)
                assert(is_py_expr(new_target))
                if new_target is not element_1.target:
                    changed_7 = True
                new_guards = []
                for element_2 in element_1.guards:
                    changed_8 = False
                    new_expr_2 = proc(element_2.expr)
                    assert(is_py_expr(new_expr_2))
                    if new_expr_2 is not element_2.expr:
                        changed_8 = True
                    if changed_8:
                        new_element_3 = PyGuard(if_keyword=element_2.if_keyword, expr=new_expr_2)
                        changed_7 = True
                    else:
                        new_element_3 = element_2
                    new_elements_1.append(new_element_3)
                if changed_7:
                    new_element_2 = PyComprehension(async_keyword=element_1.async_keyword, for_keyword=element_1.for_keyword, pattern=element_1.pattern, in_keyword=element_1.in_keyword, target=new_target, guards=new_guards)
                    changed_6 = True
                else:
                    new_element_2 = element_1
                new_elements.append(new_element_2)
            if changed_6:
                new_expr = PyGeneratorExpr(element=new_element_1, generators=new_generators)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyIfExpr):
            changed_9 = False
            new_then = proc(node.expr.then)
            assert(is_py_expr(new_then))
            if new_then is not node.expr.then:
                changed_9 = True
            new_test = proc(node.expr.test)
            assert(is_py_expr(new_test))
            if new_test is not node.expr.test:
                changed_9 = True
            new_alt = proc(node.expr.alt)
            assert(is_py_expr(new_alt))
            if new_alt is not node.expr.alt:
                changed_9 = True
            if changed_9:
                new_expr = PyIfExpr(then=new_then, if_keyword=node.expr.if_keyword, test=new_test, else_keyword=node.expr.else_keyword, alt=new_alt)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyInfixExpr):
            changed_10 = False
            new_left = proc(node.expr.left)
            assert(is_py_expr(new_left))
            if new_left is not node.expr.left:
                changed_10 = True
            new_right = proc(node.expr.right)
            assert(is_py_expr(new_right))
            if new_right is not node.expr.right:
                changed_10 = True
            if changed_10:
                new_expr = PyInfixExpr(left=new_left, op=node.expr.op, right=new_right)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyLambdaExpr):
            changed_11 = False
            new_expr_3 = proc(node.expr.expr)
            assert(is_py_expr(new_expr_3))
            if new_expr_3 is not node.expr.expr:
                changed_11 = True
            if changed_11:
                new_expr = PyLambdaExpr(lambda_keyword=node.expr.lambda_keyword, params=node.expr.params, colon=node.expr.colon, expr=new_expr_3)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyListExpr):
            changed_12 = False
            new_elements_2 = Punctuated()
            for (element_3, separator_1) in node.expr.elements.delimited:
                new_element_4 = proc(element_3)
                assert(is_py_expr(new_element_4))
                if new_element_4 is not element_3:
                    changed_12 = True
                new_separator_1 = proc(separator_1)
                assert(isinstance(new_separator_1, PyComma))
                if new_separator_1 is not separator_1:
                    changed_12 = True
                new_elements_2.append(new_element_4, new_separator_1)
            new_last_1 = proc(node.expr.elements.last)
            assert(is_py_expr(new_last_1))
            if new_last_1 is not node.expr.elements.last:
                changed_12 = True
            new_elements_2.append_final(new_last_1)
            if changed_12:
                new_expr = PyListExpr(open_bracket=node.expr.open_bracket, elements=new_elements_2, close_bracket=node.expr.close_bracket)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyNamedExpr):
            new_expr = node.expr
        elif isinstance(node.expr, PyNestExpr):
            changed_14 = False
            new_expr_4 = proc(node.expr.expr)
            assert(is_py_expr(new_expr_4))
            if new_expr_4 is not node.expr.expr:
                changed_14 = True
            if changed_14:
                new_expr = PyNestExpr(open_paren=node.expr.open_paren, expr=new_expr_4, close_paren=node.expr.close_paren)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyPrefixExpr):
            changed_15 = False
            new_expr_5 = proc(node.expr.expr)
            assert(is_py_expr(new_expr_5))
            if new_expr_5 is not node.expr.expr:
                changed_15 = True
            if changed_15:
                new_expr = PyPrefixExpr(prefix_op=node.expr.prefix_op, expr=new_expr_5)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PyStarredExpr):
            changed_16 = False
            new_expr_6 = proc(node.expr.expr)
            assert(is_py_expr(new_expr_6))
            if new_expr_6 is not node.expr.expr:
                changed_16 = True
            if changed_16:
                new_expr = PyStarredExpr(asterisk=node.expr.asterisk, expr=new_expr_6)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, PySubscriptExpr):
            changed_17 = False
            new_expr_7 = proc(node.expr.expr)
            assert(is_py_expr(new_expr_7))
            if new_expr_7 is not node.expr.expr:
                changed_17 = True
            new_slices = Punctuated()
            for (element_4, separator_2) in node.expr.slices.delimited:
                if is_py_expr(element_4):
                    new_element_5 = proc(element_4)
                    assert(is_py_expr(new_element_5))
                    if new_element_5 is not element_4:
                        changed_17 = True
                elif isinstance(element_4, PyExprSlice):
                    changed_18 = False
                    if is_py_expr(element_4.lower):
                        new_lower = proc(element_4.lower)
                        assert(is_py_expr(new_lower))
                        if new_lower is not element_4.lower:
                            changed_18 = True
                    elif element_4.lower is None:
                        new_lower = element_4.lower
                    else:
                        assert_never(element_4.lower)
                    if is_py_expr(element_4.upper):
                        new_upper = proc(element_4.upper)
                        assert(is_py_expr(new_upper))
                        if new_upper is not element_4.upper:
                            changed_18 = True
                    elif element_4.upper is None:
                        new_upper = element_4.upper
                    else:
                        assert_never(element_4.upper)
                    if isinstance(element_4.step, tuple):
                        new_elements_3 = []
                        element_0 = element_4.step[0]
                        new_element_0 = element_0
                        new_elements_3.append(new_element_0)
                        element_1 = element_4.step[1]
                        new_element_1 = proc(element_1)
                        assert(is_py_expr(new_element_1))
                        if new_element_1 is not element_1:
                            changed_18 = True
                        new_elements_3.append(new_element_1)
                        new_step = tuple(new_elements_3) if changed_18 else element_4.step
                    elif element_4.step is None:
                        new_step = element_4.step
                    else:
                        assert_never(element_4.step)
                    if changed_18:
                        new_element_5 = PyExprSlice(lower=new_lower, colon=element_4.colon, upper=new_upper, step=new_step)
                        changed_17 = True
                    else:
                        new_element_5 = element_4
                else:
                    assert_never(element_4)
                new_separator_2 = proc(separator_2)
                assert(isinstance(new_separator_2, PyComma))
                if new_separator_2 is not separator_2:
                    changed_17 = True
                new_slices.append(new_element_5, new_separator_2)
            if is_py_expr(node.expr.slices.last):
                new_last_2 = proc(node.expr.slices.last)
                assert(is_py_expr(new_last_2))
                if new_last_2 is not node.expr.slices.last:
                    changed_17 = True
            elif isinstance(node.expr.slices.last, PyExprSlice):
                new_last_2 = proc(node.expr.slices.last)
                assert(isinstance(new_last_2, PyExprSlice))
                if new_last_2 is not node.expr.slices.last:
                    changed_17 = True
            else:
                assert_never(node.expr.slices.last)
            new_slices.append_final(new_last_2)
            if changed_17:
                new_expr = PySubscriptExpr(expr=new_expr_7, open_bracket=node.expr.open_bracket, slices=new_slices, close_bracket=node.expr.close_bracket)
                changed_1 = True
            else:
                new_expr = node.expr
        elif is_py_tuple_expr(node.expr):
            if isinstance(node.expr, PyTupleZero):
                new_expr = node.expr
            elif isinstance(node.expr, PyTupleOne):
                changed_20 = False
                new_expr_8 = proc(node.expr.expr)
                assert(is_py_expr(new_expr_8))
                if new_expr_8 is not node.expr.expr:
                    changed_20 = True
                if changed_20:
                    new_expr = PyTupleOne(open_paren=node.expr.open_paren, expr=new_expr_8, comma=node.expr.comma, close_paren=node.expr.close_paren)
                    changed_1 = True
                else:
                    new_expr = node.expr
            elif isinstance(node.expr, PyTupleMany):
                changed_21 = False
                new_elements_4 = Punctuated()
                for (element_5, separator_3) in node.expr.elements.delimited:
                    new_element_6 = proc(element_5)
                    assert(is_py_expr(new_element_6))
                    if new_element_6 is not element_5:
                        changed_21 = True
                    new_separator_3 = proc(separator_3)
                    assert(isinstance(new_separator_3, PyComma))
                    if new_separator_3 is not separator_3:
                        changed_21 = True
                    new_elements_4.append(new_element_6, new_separator_3)
                new_last_3 = proc(node.expr.elements.last)
                assert(is_py_expr(new_last_3))
                if new_last_3 is not node.expr.elements.last:
                    changed_21 = True
                new_elements_4.append_final(new_last_3)
                if changed_21:
                    new_expr = PyTupleMany(open_paren=node.expr.open_paren, elements=new_elements_4, close_paren=node.expr.close_paren)
                    changed_1 = True
                else:
                    new_expr = node.expr
            else:
                assert_never(node.expr)
        else:
            assert_never(node.expr)
        if changed_1:
            rewritten = PyKeywordArg(name=node.name, equals=node.equals, expr=new_expr)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_py_expr(node: PyExpr, proc: Callable[[PyExpr], PyExpr]) -> PyExpr:
    if isinstance(node, PyAttrExpr):
        changed_1 = False
        new_expr = proc(node.expr)
        assert(is_py_expr(new_expr))
        if new_expr is not node.expr:
            changed_1 = True
        if changed_1:
            rewritten = PyAttrExpr(expr=new_expr, dot=node.dot, name=node.name)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyCallExpr):
        changed_2 = False
        new_operator = proc(node.operator)
        assert(is_py_expr(new_operator))
        if new_operator is not node.operator:
            changed_2 = True
        new_args = Punctuated()
        for (element, separator) in node.args.delimited:
            if isinstance(element, PyKeywordArg):
                changed_3 = False
                new_expr_1 = proc(element.expr)
                assert(is_py_expr(new_expr_1))
                if new_expr_1 is not element.expr:
                    changed_3 = True
                if changed_3:
                    new_element = PyKeywordArg(name=element.name, equals=element.equals, expr=new_expr_1)
                    changed_2 = True
                else:
                    new_element = element
            elif is_py_expr(element):
                new_element = proc(element)
                assert(is_py_expr(new_element))
                if new_element is not element:
                    changed_2 = True
            else:
                assert_never(element)
            new_separator = separator
            new_args.append(new_element, new_separator)
        new_last = proc(node.args.last)
        assert(is_py_arg(new_last))
        if new_last is not node.args.last:
            changed_2 = True
        new_args.append_final(new_last)
        if changed_2:
            rewritten = PyCallExpr(operator=new_operator, open_paren=node.open_paren, args=new_args, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyConstExpr):
        rewritten = node
    elif isinstance(node, PyEllipsisExpr):
        rewritten = node
    elif isinstance(node, PyGeneratorExpr):
        changed_6 = False
        new_element_1 = proc(node.element)
        assert(is_py_expr(new_element_1))
        if new_element_1 is not node.element:
            changed_6 = True
        new_generators = []
        for element_1 in node.generators:
            changed_7 = False
            new_target = proc(element_1.target)
            assert(is_py_expr(new_target))
            if new_target is not element_1.target:
                changed_7 = True
            new_guards = []
            for element_2 in element_1.guards:
                changed_8 = False
                new_expr_2 = proc(element_2.expr)
                assert(is_py_expr(new_expr_2))
                if new_expr_2 is not element_2.expr:
                    changed_8 = True
                if changed_8:
                    new_element_3 = PyGuard(if_keyword=element_2.if_keyword, expr=new_expr_2)
                    changed_7 = True
                else:
                    new_element_3 = element_2
                new_elements_1.append(new_element_3)
            if changed_7:
                new_element_2 = PyComprehension(async_keyword=element_1.async_keyword, for_keyword=element_1.for_keyword, pattern=element_1.pattern, in_keyword=element_1.in_keyword, target=new_target, guards=new_guards)
                changed_6 = True
            else:
                new_element_2 = element_1
            new_elements.append(new_element_2)
        if changed_6:
            rewritten = PyGeneratorExpr(element=new_element_1, generators=new_generators)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyIfExpr):
        changed_9 = False
        new_then = proc(node.then)
        assert(is_py_expr(new_then))
        if new_then is not node.then:
            changed_9 = True
        new_test = proc(node.test)
        assert(is_py_expr(new_test))
        if new_test is not node.test:
            changed_9 = True
        new_alt = proc(node.alt)
        assert(is_py_expr(new_alt))
        if new_alt is not node.alt:
            changed_9 = True
        if changed_9:
            rewritten = PyIfExpr(then=new_then, if_keyword=node.if_keyword, test=new_test, else_keyword=node.else_keyword, alt=new_alt)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyInfixExpr):
        changed_10 = False
        new_left = proc(node.left)
        assert(is_py_expr(new_left))
        if new_left is not node.left:
            changed_10 = True
        new_right = proc(node.right)
        assert(is_py_expr(new_right))
        if new_right is not node.right:
            changed_10 = True
        if changed_10:
            rewritten = PyInfixExpr(left=new_left, op=node.op, right=new_right)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyLambdaExpr):
        changed_11 = False
        new_expr_3 = proc(node.expr)
        assert(is_py_expr(new_expr_3))
        if new_expr_3 is not node.expr:
            changed_11 = True
        if changed_11:
            rewritten = PyLambdaExpr(lambda_keyword=node.lambda_keyword, params=node.params, colon=node.colon, expr=new_expr_3)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyListExpr):
        changed_12 = False
        new_elements_2 = Punctuated()
        for (element_3, separator_1) in node.elements.delimited:
            new_element_4 = proc(element_3)
            assert(is_py_expr(new_element_4))
            if new_element_4 is not element_3:
                changed_12 = True
            new_separator_1 = proc(separator_1)
            assert(isinstance(new_separator_1, PyComma))
            if new_separator_1 is not separator_1:
                changed_12 = True
            new_elements_2.append(new_element_4, new_separator_1)
        new_last_1 = proc(node.elements.last)
        assert(is_py_expr(new_last_1))
        if new_last_1 is not node.elements.last:
            changed_12 = True
        new_elements_2.append_final(new_last_1)
        if changed_12:
            rewritten = PyListExpr(open_bracket=node.open_bracket, elements=new_elements_2, close_bracket=node.close_bracket)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyNamedExpr):
        rewritten = node
    elif isinstance(node, PyNestExpr):
        changed_14 = False
        new_expr_4 = proc(node.expr)
        assert(is_py_expr(new_expr_4))
        if new_expr_4 is not node.expr:
            changed_14 = True
        if changed_14:
            rewritten = PyNestExpr(open_paren=node.open_paren, expr=new_expr_4, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyPrefixExpr):
        changed_15 = False
        new_expr_5 = proc(node.expr)
        assert(is_py_expr(new_expr_5))
        if new_expr_5 is not node.expr:
            changed_15 = True
        if changed_15:
            rewritten = PyPrefixExpr(prefix_op=node.prefix_op, expr=new_expr_5)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyStarredExpr):
        changed_16 = False
        new_expr_6 = proc(node.expr)
        assert(is_py_expr(new_expr_6))
        if new_expr_6 is not node.expr:
            changed_16 = True
        if changed_16:
            rewritten = PyStarredExpr(asterisk=node.asterisk, expr=new_expr_6)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PySubscriptExpr):
        changed_17 = False
        new_expr_7 = proc(node.expr)
        assert(is_py_expr(new_expr_7))
        if new_expr_7 is not node.expr:
            changed_17 = True
        new_slices = Punctuated()
        for (element_4, separator_2) in node.slices.delimited:
            if is_py_expr(element_4):
                new_element_5 = proc(element_4)
                assert(is_py_expr(new_element_5))
                if new_element_5 is not element_4:
                    changed_17 = True
            elif isinstance(element_4, PyExprSlice):
                changed_18 = False
                if is_py_expr(element_4.lower):
                    new_lower = proc(element_4.lower)
                    assert(is_py_expr(new_lower))
                    if new_lower is not element_4.lower:
                        changed_18 = True
                elif element_4.lower is None:
                    new_lower = element_4.lower
                else:
                    assert_never(element_4.lower)
                if is_py_expr(element_4.upper):
                    new_upper = proc(element_4.upper)
                    assert(is_py_expr(new_upper))
                    if new_upper is not element_4.upper:
                        changed_18 = True
                elif element_4.upper is None:
                    new_upper = element_4.upper
                else:
                    assert_never(element_4.upper)
                if isinstance(element_4.step, tuple):
                    new_elements_3 = []
                    element_0 = element_4.step[0]
                    new_element_0 = element_0
                    new_elements_3.append(new_element_0)
                    element_1 = element_4.step[1]
                    new_element_1 = proc(element_1)
                    assert(is_py_expr(new_element_1))
                    if new_element_1 is not element_1:
                        changed_18 = True
                    new_elements_3.append(new_element_1)
                    new_step = tuple(new_elements_3) if changed_18 else element_4.step
                elif element_4.step is None:
                    new_step = element_4.step
                else:
                    assert_never(element_4.step)
                if changed_18:
                    new_element_5 = PyExprSlice(lower=new_lower, colon=element_4.colon, upper=new_upper, step=new_step)
                    changed_17 = True
                else:
                    new_element_5 = element_4
            else:
                assert_never(element_4)
            new_separator_2 = proc(separator_2)
            assert(isinstance(new_separator_2, PyComma))
            if new_separator_2 is not separator_2:
                changed_17 = True
            new_slices.append(new_element_5, new_separator_2)
        if is_py_expr(node.slices.last):
            new_last_2 = proc(node.slices.last)
            assert(is_py_expr(new_last_2))
            if new_last_2 is not node.slices.last:
                changed_17 = True
        elif isinstance(node.slices.last, PyExprSlice):
            new_last_2 = proc(node.slices.last)
            assert(isinstance(new_last_2, PyExprSlice))
            if new_last_2 is not node.slices.last:
                changed_17 = True
        else:
            assert_never(node.slices.last)
        new_slices.append_final(new_last_2)
        if changed_17:
            rewritten = PySubscriptExpr(expr=new_expr_7, open_bracket=node.open_bracket, slices=new_slices, close_bracket=node.close_bracket)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_py_pattern(node: PyPattern, proc: Callable[[PyPattern], PyPattern]) -> PyPattern:
    if isinstance(node, PyAttrPattern):
        changed_1 = False
        new_pattern = proc(node.pattern)
        assert(is_py_pattern(new_pattern))
        if new_pattern is not node.pattern:
            changed_1 = True
        if changed_1:
            rewritten = PyAttrPattern(pattern=new_pattern, dot=node.dot, name=node.name)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyListPattern):
        changed_2 = False
        new_elements = Punctuated()
        for (element, separator) in node.elements.delimited:
            new_element = proc(element)
            assert(is_py_pattern(new_element))
            if new_element is not element:
                changed_2 = True
            new_separator = separator
            new_elements.append(new_element, new_separator)
        new_last = proc(node.elements.last)
        assert(is_py_pattern(new_last))
        if new_last is not node.elements.last:
            changed_2 = True
        new_elements.append_final(new_last)
        if changed_2:
            rewritten = PyListPattern(open_bracket=node.open_bracket, elements=new_elements, close_bracket=node.close_bracket)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyNamedPattern):
        rewritten = node
    elif isinstance(node, PyStarredPattern):
        changed_4 = False
        new_pattern_1 = proc(node.pattern)
        assert(is_py_pattern(new_pattern_1))
        if new_pattern_1 is not node.pattern:
            changed_4 = True
        if changed_4:
            rewritten = PyStarredPattern(asterisk=node.asterisk, pattern=new_pattern_1)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PySubscriptPattern):
        changed_5 = False
        new_pattern_2 = proc(node.pattern)
        assert(is_py_pattern(new_pattern_2))
        if new_pattern_2 is not node.pattern:
            changed_5 = True
        new_slices = Punctuated()
        for (element_1, separator_1) in node.slices.delimited:
            if is_py_pattern(element_1):
                new_element_1 = proc(element_1)
                assert(is_py_pattern(new_element_1))
                if new_element_1 is not element_1:
                    changed_5 = True
            elif isinstance(element_1, PyPatternSlice):
                changed_6 = False
                if is_py_pattern(element_1.lower):
                    new_lower = proc(element_1.lower)
                    assert(is_py_pattern(new_lower))
                    if new_lower is not element_1.lower:
                        changed_6 = True
                elif element_1.lower is None:
                    new_lower = element_1.lower
                else:
                    assert_never(element_1.lower)
                if is_py_pattern(element_1.upper):
                    new_upper = proc(element_1.upper)
                    assert(is_py_pattern(new_upper))
                    if new_upper is not element_1.upper:
                        changed_6 = True
                elif element_1.upper is None:
                    new_upper = element_1.upper
                else:
                    assert_never(element_1.upper)
                if isinstance(element_1.step, tuple):
                    new_elements_1 = []
                    element_0 = element_1.step[0]
                    new_element_0 = element_0
                    new_elements_1.append(new_element_0)
                    element_1 = element_1.step[1]
                    new_element_1 = proc(element_1)
                    assert(is_py_pattern(new_element_1))
                    if new_element_1 is not element_1:
                        changed_6 = True
                    new_elements_1.append(new_element_1)
                    new_step = tuple(new_elements_1) if changed_6 else element_1.step
                elif element_1.step is None:
                    new_step = element_1.step
                else:
                    assert_never(element_1.step)
                if changed_6:
                    new_element_1 = PyPatternSlice(lower=new_lower, colon=element_1.colon, upper=new_upper, step=new_step)
                    changed_5 = True
                else:
                    new_element_1 = element_1
            else:
                assert_never(element_1)
            new_separator_1 = proc(separator_1)
            assert(isinstance(new_separator_1, PyComma))
            if new_separator_1 is not separator_1:
                changed_5 = True
            new_slices.append(new_element_1, new_separator_1)
        if is_py_pattern(node.slices.last):
            new_last_1 = proc(node.slices.last)
            assert(is_py_pattern(new_last_1))
            if new_last_1 is not node.slices.last:
                changed_5 = True
        elif isinstance(node.slices.last, PyPatternSlice):
            new_last_1 = proc(node.slices.last)
            assert(isinstance(new_last_1, PyPatternSlice))
            if new_last_1 is not node.slices.last:
                changed_5 = True
        else:
            assert_never(node.slices.last)
        new_slices.append_final(new_last_1)
        if changed_5:
            rewritten = PySubscriptPattern(pattern=new_pattern_2, open_bracket=node.open_bracket, slices=new_slices, close_bracket=node.close_bracket)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyTuplePattern):
        changed_7 = False
        new_elements_2 = Punctuated()
        for (element_2, separator_2) in node.elements.delimited:
            new_element_2 = proc(element_2)
            assert(is_py_pattern(new_element_2))
            if new_element_2 is not element_2:
                changed_7 = True
            new_separator_2 = proc(separator_2)
            assert(isinstance(new_separator_2, PyComma))
            if new_separator_2 is not separator_2:
                changed_7 = True
            new_elements_2.append(new_element_2, new_separator_2)
        new_last_2 = proc(node.elements.last)
        assert(is_py_pattern(new_last_2))
        if new_last_2 is not node.elements.last:
            changed_7 = True
        new_elements_2.append_final(new_last_2)
        if changed_7:
            rewritten = PyTuplePattern(open_paren=node.open_paren, elements=new_elements_2, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_py_stmt(node: PyStmt, proc: Callable[[PyStmt], PyStmt]) -> PyStmt:
    if isinstance(node, PyAssignStmt):
        rewritten = node
    elif isinstance(node, PyAugAssignStmt):
        rewritten = node
    elif isinstance(node, PyBreakStmt):
        rewritten = node
    elif isinstance(node, PyClassDef):
        changed_4 = False
        if is_py_stmt(node.body):
            new_body = proc(node.body)
            assert(is_py_stmt(new_body))
            if new_body is not node.body:
                changed_4 = True
        elif isinstance(node.body, list):
            new_body = []
            for element in node.body:
                new_element = proc(element)
                assert(is_py_stmt(new_element))
                if new_element is not element:
                    changed_4 = True
                new_elements.append(new_element)
        else:
            assert_never(node.body)
        if changed_4:
            rewritten = PyClassDef(decorators=node.decorators, class_keyword=node.class_keyword, name=node.name, bases=node.bases, colon=node.colon, body=new_body)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyContinueStmt):
        rewritten = node
    elif isinstance(node, PyDeleteStmt):
        rewritten = node
    elif isinstance(node, PyExprStmt):
        rewritten = node
    elif isinstance(node, PyForStmt):
        changed_8 = False
        if is_py_stmt(node.body):
            new_body_1 = proc(node.body)
            assert(is_py_stmt(new_body_1))
            if new_body_1 is not node.body:
                changed_8 = True
        elif isinstance(node.body, list):
            new_body_1 = []
            for element_1 in node.body:
                new_element_1 = proc(element_1)
                assert(is_py_stmt(new_element_1))
                if new_element_1 is not element_1:
                    changed_8 = True
                new_elements_1.append(new_element_1)
        else:
            assert_never(node.body)
        if isinstance(node.else_clause, tuple):
            new_elements_2 = []
            element_0 = node.else_clause[0]
            new_element_0 = element_0
            new_elements_2.append(new_element_0)
            element_1 = node.else_clause[1]
            new_element_1 = element_1
            new_elements_2.append(new_element_1)
            element_2 = node.else_clause[2]
            if is_py_stmt(element_2):
                new_element_2 = proc(element_2)
                assert(is_py_stmt(new_element_2))
                if new_element_2 is not element_2:
                    changed_8 = True
            elif isinstance(element_2, list):
                new_element_2 = []
                for element_2 in element_2:
                    new_element_2 = proc(element_2)
                    assert(is_py_stmt(new_element_2))
                    if new_element_2 is not element_2:
                        changed_8 = True
                    new_elements_3.append(new_element_2)
            else:
                assert_never(element_2)
            new_elements_2.append(new_element_2)
            new_else_clause = tuple(new_elements_2) if changed_8 else node.else_clause
        elif node.else_clause is None:
            new_else_clause = node.else_clause
        else:
            assert_never(node.else_clause)
        if changed_8:
            rewritten = PyForStmt(for_keyword=node.for_keyword, pattern=node.pattern, in_keyword=node.in_keyword, expr=node.expr, colon=node.colon, body=new_body_1, else_clause=new_else_clause)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyFuncDef):
        changed_9 = False
        if is_py_stmt(node.body):
            new_body_2 = proc(node.body)
            assert(is_py_stmt(new_body_2))
            if new_body_2 is not node.body:
                changed_9 = True
        elif isinstance(node.body, list):
            new_body_2 = []
            for element_3 in node.body:
                new_element_3 = proc(element_3)
                assert(is_py_stmt(new_element_3))
                if new_element_3 is not element_3:
                    changed_9 = True
                new_elements_4.append(new_element_3)
        else:
            assert_never(node.body)
        if changed_9:
            rewritten = PyFuncDef(decorators=node.decorators, async_keyword=node.async_keyword, def_keyword=node.def_keyword, name=node.name, open_paren=node.open_paren, params=node.params, close_paren=node.close_paren, return_type=node.return_type, colon=node.colon, body=new_body_2)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyGlobalStmt):
        rewritten = node
    elif isinstance(node, PyIfStmt):
        changed_11 = False
        changed_12 = False
        if is_py_stmt(node.first.body):
            new_body_3 = proc(node.first.body)
            assert(is_py_stmt(new_body_3))
            if new_body_3 is not node.first.body:
                changed_12 = True
        elif isinstance(node.first.body, list):
            new_body_3 = []
            for element_4 in node.first.body:
                new_element_4 = proc(element_4)
                assert(is_py_stmt(new_element_4))
                if new_element_4 is not element_4:
                    changed_12 = True
                new_elements_5.append(new_element_4)
        else:
            assert_never(node.first.body)
        if changed_12:
            new_first = PyIfCase(if_keyword=node.first.if_keyword, test=node.first.test, colon=node.first.colon, body=new_body_3)
            changed_11 = True
        else:
            new_first = node.first
        new_alternatives = []
        for element_5 in node.alternatives:
            changed_13 = False
            if is_py_stmt(element_5.body):
                new_body_4 = proc(element_5.body)
                assert(is_py_stmt(new_body_4))
                if new_body_4 is not element_5.body:
                    changed_13 = True
            elif isinstance(element_5.body, list):
                new_body_4 = []
                for element_6 in element_5.body:
                    new_element_6 = proc(element_6)
                    assert(is_py_stmt(new_element_6))
                    if new_element_6 is not element_6:
                        changed_13 = True
                    new_elements_7.append(new_element_6)
            else:
                assert_never(element_5.body)
            if changed_13:
                new_element_5 = PyElifCase(elif_keyword=element_5.elif_keyword, test=element_5.test, colon=element_5.colon, body=new_body_4)
                changed_11 = True
            else:
                new_element_5 = element_5
            new_elements_6.append(new_element_5)
        if isinstance(node.last, PyElseCase):
            changed_14 = False
            if is_py_stmt(node.last.body):
                new_body_5 = proc(node.last.body)
                assert(is_py_stmt(new_body_5))
                if new_body_5 is not node.last.body:
                    changed_14 = True
            elif isinstance(node.last.body, list):
                new_body_5 = []
                for element_7 in node.last.body:
                    new_element_7 = proc(element_7)
                    assert(is_py_stmt(new_element_7))
                    if new_element_7 is not element_7:
                        changed_14 = True
                    new_elements_8.append(new_element_7)
            else:
                assert_never(node.last.body)
            if changed_14:
                new_last = PyElseCase(else_keyword=node.last.else_keyword, colon=node.last.colon, body=new_body_5)
                changed_11 = True
            else:
                new_last = node.last
        elif node.last is None:
            new_last = node.last
        else:
            assert_never(node.last)
        if changed_11:
            rewritten = PyIfStmt(first=new_first, alternatives=new_alternatives, last=new_last)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyImportFromStmt):
        rewritten = node
    elif isinstance(node, PyImportStmt):
        rewritten = node
    elif isinstance(node, PyNonlocalStmt):
        rewritten = node
    elif isinstance(node, PyPassStmt):
        rewritten = node
    elif isinstance(node, PyRaiseStmt):
        rewritten = node
    elif isinstance(node, PyRetStmt):
        rewritten = node
    elif isinstance(node, PyTryStmt):
        changed_21 = False
        if is_py_stmt(node.body):
            new_body_6 = proc(node.body)
            assert(is_py_stmt(new_body_6))
            if new_body_6 is not node.body:
                changed_21 = True
        elif isinstance(node.body, list):
            new_body_6 = []
            for element_8 in node.body:
                new_element_8 = proc(element_8)
                assert(is_py_stmt(new_element_8))
                if new_element_8 is not element_8:
                    changed_21 = True
                new_elements_9.append(new_element_8)
        else:
            assert_never(node.body)
        new_handlers = []
        for element_9 in node.handlers:
            changed_22 = False
            if is_py_stmt(element_9.body):
                new_body_7 = proc(element_9.body)
                assert(is_py_stmt(new_body_7))
                if new_body_7 is not element_9.body:
                    changed_22 = True
            elif isinstance(element_9.body, list):
                new_body_7 = []
                for element_10 in element_9.body:
                    new_element_10 = proc(element_10)
                    assert(is_py_stmt(new_element_10))
                    if new_element_10 is not element_10:
                        changed_22 = True
                    new_elements_11.append(new_element_10)
            else:
                assert_never(element_9.body)
            if changed_22:
                new_element_9 = PyExceptHandler(except_keyword=element_9.except_keyword, expr=element_9.expr, binder=element_9.binder, colon=element_9.colon, body=new_body_7)
                changed_21 = True
            else:
                new_element_9 = element_9
            new_elements_10.append(new_element_9)
        if isinstance(node.else_clause, tuple):
            new_elements_12 = []
            element_0_1 = node.else_clause[0]
            new_element_0_1 = proc(element_0_1)
            assert(isinstance(new_element_0_1, PyElseKeyword))
            if new_element_0_1 is not element_0_1:
                changed_21 = True
            new_elements_12.append(new_element_0_1)
            element_1_1 = node.else_clause[1]
            new_element_1_1 = proc(element_1_1)
            assert(isinstance(new_element_1_1, PyColon))
            if new_element_1_1 is not element_1_1:
                changed_21 = True
            new_elements_12.append(new_element_1_1)
            element_2_1 = node.else_clause[2]
            if is_py_stmt(element_2_1):
                new_element_2_1 = proc(element_2_1)
                assert(is_py_stmt(new_element_2_1))
                if new_element_2_1 is not element_2_1:
                    changed_21 = True
            elif isinstance(element_2_1, list):
                new_element_2_1 = []
                for element_11 in element_2_1:
                    new_element_11 = proc(element_11)
                    assert(is_py_stmt(new_element_11))
                    if new_element_11 is not element_11:
                        changed_21 = True
                    new_elements_13.append(new_element_11)
            else:
                assert_never(element_2_1)
            new_elements_12.append(new_element_2_1)
            new_else_clause_1 = tuple(new_elements_12) if changed_21 else node.else_clause
        elif node.else_clause is None:
            new_else_clause_1 = node.else_clause
        else:
            assert_never(node.else_clause)
        if isinstance(node.finally_clause, tuple):
            new_elements_14 = []
            element_0_2 = node.finally_clause[0]
            new_element_0_2 = element_0_2
            new_elements_14.append(new_element_0_2)
            element_1_2 = node.finally_clause[1]
            new_element_1_2 = proc(element_1_2)
            assert(isinstance(new_element_1_2, PyColon))
            if new_element_1_2 is not element_1_2:
                changed_21 = True
            new_elements_14.append(new_element_1_2)
            element_2_2 = node.finally_clause[2]
            if is_py_stmt(element_2_2):
                new_element_2_2 = proc(element_2_2)
                assert(is_py_stmt(new_element_2_2))
                if new_element_2_2 is not element_2_2:
                    changed_21 = True
            elif isinstance(element_2_2, list):
                new_element_2_2 = []
                for element_12 in element_2_2:
                    new_element_12 = proc(element_12)
                    assert(is_py_stmt(new_element_12))
                    if new_element_12 is not element_12:
                        changed_21 = True
                    new_elements_15.append(new_element_12)
            else:
                assert_never(element_2_2)
            new_elements_14.append(new_element_2_2)
            new_finally_clause = tuple(new_elements_14) if changed_21 else node.finally_clause
        elif node.finally_clause is None:
            new_finally_clause = node.finally_clause
        else:
            assert_never(node.finally_clause)
        if changed_21:
            rewritten = PyTryStmt(try_keyword=node.try_keyword, colon=node.colon, body=new_body_6, handlers=new_handlers, else_clause=new_else_clause_1, finally_clause=new_finally_clause)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, PyTypeAliasStmt):
        rewritten = node
    elif isinstance(node, PyWhileStmt):
        changed_24 = False
        if is_py_stmt(node.body):
            new_body_8 = proc(node.body)
            assert(is_py_stmt(new_body_8))
            if new_body_8 is not node.body:
                changed_24 = True
        elif isinstance(node.body, list):
            new_body_8 = []
            for element_13 in node.body:
                new_element_13 = proc(element_13)
                assert(is_py_stmt(new_element_13))
                if new_element_13 is not element_13:
                    changed_24 = True
                new_elements_16.append(new_element_13)
        else:
            assert_never(node.body)
        if isinstance(node.else_clause, tuple):
            new_elements_17 = []
            element_0_3 = node.else_clause[0]
            new_element_0_3 = proc(element_0_3)
            assert(isinstance(new_element_0_3, PyElseKeyword))
            if new_element_0_3 is not element_0_3:
                changed_24 = True
            new_elements_17.append(new_element_0_3)
            element_1_3 = node.else_clause[1]
            new_element_1_3 = proc(element_1_3)
            assert(isinstance(new_element_1_3, PyColon))
            if new_element_1_3 is not element_1_3:
                changed_24 = True
            new_elements_17.append(new_element_1_3)
            element_2_3 = node.else_clause[2]
            if is_py_stmt(element_2_3):
                new_element_2_3 = proc(element_2_3)
                assert(is_py_stmt(new_element_2_3))
                if new_element_2_3 is not element_2_3:
                    changed_24 = True
            elif isinstance(element_2_3, list):
                new_element_2_3 = []
                for element_14 in element_2_3:
                    new_element_14 = proc(element_14)
                    assert(is_py_stmt(new_element_14))
                    if new_element_14 is not element_14:
                        changed_24 = True
                    new_elements_18.append(new_element_14)
            else:
                assert_never(element_2_3)
            new_elements_17.append(new_element_2_3)
            new_else_clause_2 = tuple(new_elements_17) if changed_24 else node.else_clause
        elif node.else_clause is None:
            new_else_clause_2 = node.else_clause
        else:
            assert_never(node.else_clause)
        if changed_24:
            rewritten = PyWhileStmt(while_keyword=node.while_keyword, expr=node.expr, colon=node.colon, body=new_body_8, else_clause=new_else_clause_2)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


