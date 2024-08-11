from typing import Any, TypeGuard, Never, Sequence


from magelang.runtime import Span, Punctuated, BaseNode as Node, BaseToken as Token


class PyIdent(Token):

    def __init__(self, value: str, span: Span | None = None): ...

    value: str 


class PyFloat(Token):

    def __init__(self, value: float, span: Span | None = None): ...

    value: float 


class PyInteger(Token):

    def __init__(self, value: int, span: Span | None = None): ...

    value: int 


class PyString(Token):

    def __init__(self, value: str, span: Span | None = None): ...

    value: str 


class PySlice(Node):

    lower: 'PyExpr | None' 

    colon: 'PyColon' 

    upper: 'PyExpr | None' 

    step: 'tuple[PyColon, PyExpr] | None' 

    def __init__(self, *, lower: 'PyExpr | None' = None, colon: 'PyColon | None' = None, upper: 'PyExpr | None' = None, step: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None): ...


type PyPattern = PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern


def is_py_pattern(value: Any) -> TypeGuard[PyPattern]: ...


class PyNamedPattern(Node):

    name: 'PyIdent' 

    def __init__(self, name: 'PyIdent | str'): ...


class PyAttrPattern(Node):

    pattern: 'PyPattern' 

    dot: 'PyDot' 

    name: 'PyIdent' 

    def __init__(self, pattern: 'PyPattern', name: 'PyIdent | str', *, dot: 'PyDot | None' = None): ...


class PySubscriptPattern(Node):

    pattern: 'PyPattern' 

    open_bracket: 'PyOpenBracket' 

    slices: 'Punctuated[PySlice | PyPattern, PyComma]' 

    close_bracket: 'PyCloseBracket' 

    def __init__(self, pattern: 'PyPattern', slices: 'Sequence[tuple[PySlice | PyPattern, PyComma | None]] | Sequence[PySlice | PyPattern] | Punctuated[PySlice | PyPattern, PyComma | None]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None): ...


class PyStarredPattern(Node):

    asterisk: 'PyAsterisk' 

    expr: 'PyExpr' 

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None): ...


class PyListPattern(Node):

    open_bracket: 'PyOpenBracket' 

    elements: 'Punctuated[PyPattern, PyComma]' 

    close_bracket: 'PyCloseBracket' 

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None): ...


class PyTuplePattern(Node):

    open_paren: 'PyOpenParen' 

    elements: 'Punctuated[PyPattern, PyComma]' 

    close_paren: 'PyCloseParen' 

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None): ...


type PyExpr = PyAttrExpr | PyCallExpr | PyConstExpr | PyEllipsisExpr | PyGeneratorExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr


def is_py_expr(value: Any) -> TypeGuard[PyExpr]: ...


class PyEllipsisExpr(Node):

    dot_dot_dot: 'PyDotDotDot' 

    def __init__(self, *, dot_dot_dot: 'PyDotDotDot | None' = None): ...


class PyGuard(Node):

    if_keyword: 'PyIfKeyword' 

    expr: 'PyExpr' 

    def __init__(self, expr: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None): ...


class PyComprehension(Node):

    async_keyword: 'PyAsyncKeyword | None' 

    for_keyword: 'PyForKeyword' 

    pattern: 'PyPattern' 

    in_keyword: 'PyInKeyword' 

    target: 'PyExpr' 

    guards: 'Sequence[PyGuard]' 

    def __init__(self, pattern: 'PyPattern', target: 'PyExpr', *, async_keyword: 'PyAsyncKeyword | None' = None, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, guards: 'Sequence[PyGuard | PyExpr] | None' = None): ...


class PyGeneratorExpr(Node):

    element: 'PyExpr' 

    generators: 'Sequence[PyComprehension]' 

    def __init__(self, element: 'PyExpr', generators: 'Sequence[PyComprehension]'): ...


class PyConstExpr(Node):

    literal: 'PyFloat | PyInteger | PyString' 

    def __init__(self, literal: 'PyFloat | PyInteger | PyString | float | int | str'): ...


class PyNestExpr(Node):

    open_paren: 'PyOpenParen' 

    expr: 'PyExpr' 

    close_paren: 'PyCloseParen' 

    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None): ...


class PyNamedExpr(Node):

    name: 'PyIdent' 

    def __init__(self, name: 'PyIdent | str'): ...


class PyAttrExpr(Node):

    expr: 'PyExpr' 

    dot: 'PyDot' 

    name: 'PyIdent' 

    def __init__(self, expr: 'PyExpr', name: 'PyIdent | str', *, dot: 'PyDot | None' = None): ...


class PySubscriptExpr(Node):

    expr: 'PyExpr' 

    open_bracket: 'PyOpenBracket' 

    slices: 'Punctuated[PySlice | PyExpr, PyComma]' 

    close_bracket: 'PyCloseBracket' 

    def __init__(self, expr: 'PyExpr', slices: 'Sequence[tuple[PySlice | PyExpr, PyComma | None]] | Sequence[PySlice | PyExpr] | Punctuated[PySlice | PyExpr, PyComma | None]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None): ...


class PyStarredExpr(Node):

    asterisk: 'PyAsterisk' 

    expr: 'PyExpr' 

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None): ...


class PyListExpr(Node):

    open_bracket: 'PyOpenBracket' 

    elements: 'Punctuated[PyExpr, PyComma]' 

    close_bracket: 'PyCloseBracket' 

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, close_bracket: 'PyCloseBracket | None' = None): ...


class PyTupleExpr(Node):

    open_paren: 'PyOpenParen' 

    elements: 'Punctuated[PyExpr, PyComma]' 

    close_paren: 'PyCloseParen' 

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None): ...


type PyArg = PyKeywordArg | PyExpr


def is_py_arg(value: Any) -> TypeGuard[PyArg]: ...


class PyKeywordArg(Node):

    name: 'PyIdent' 

    equals: 'PyEquals' 

    expr: 'PyExpr' 

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, equals: 'PyEquals | None' = None): ...


class PyCallExpr(Node):

    operator: 'PyExpr' 

    open_paren: 'PyOpenParen' 

    args: 'Punctuated[PyArg, PyComma]' 

    close_paren: 'PyCloseParen' 

    def __init__(self, operator: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None): ...


type PyPrefixOp = PyNotKeyword | PyPlus | PyHyphen | PyTilde


def is_py_prefix_op(value: Any) -> TypeGuard[PyPrefixOp]: ...


class PyPrefixExpr(Node):

    prefix_op: 'PyPrefixOp' 

    expr: 'PyExpr' 

    def __init__(self, prefix_op: 'PyPrefixOp', expr: 'PyExpr'): ...


type PyInfixOp = PyPlus | PyHyphen | PyAsterisk | PySlash | PySlashSlash | PyPercent | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyAtSign | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | tuple[PyIsKeyword, PyNotKeyword] | PyInKeyword | tuple[PyNotKeyword, PyInKeyword]


def is_py_infix_op(value: Any) -> TypeGuard[PyInfixOp]: ...


class PyInfixExpr(Node):

    left: 'PyExpr' 

    op: 'PyInfixOp' 

    right: 'PyExpr' 

    def __init__(self, left: 'PyExpr', op: 'PyInfixOp', right: 'PyExpr'): ...


class PyQualName(Node):

    modules: 'Sequence[tuple[PyIdent, PyDot]]' 

    name: 'PyIdent' 

    def __init__(self, name: 'PyIdent | str', *, modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None' = None): ...


class PyAbsolutePath(Node):

    name: 'PyQualName' 

    def __init__(self, name: 'PyQualName | PyIdent | str'): ...


class PyRelativePath(Node):

    dots: 'Sequence[PyDot]' 

    name: 'PyQualName | None' 

    def __init__(self, dots: 'Sequence[PyDot] | int', *, name: 'PyQualName | PyIdent | None | str' = None): ...


type PyPath = PyAbsolutePath | PyRelativePath


def is_py_path(value: Any) -> TypeGuard[PyPath]: ...


class PyAlias(Node):

    path: 'PyPath' 

    asname: 'tuple[PyAsKeyword, PyIdent] | None' 

    def __init__(self, path: 'PyPath', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None): ...


class PyFromAlias(Node):

    name: 'PyAsterisk | PyIdent' 

    asname: 'tuple[PyAsKeyword, PyIdent] | None' 

    def __init__(self, name: 'PyAsterisk | PyIdent | str', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None): ...


class PyImportStmt(Node):

    import_keyword: 'PyImportKeyword' 

    aliases: 'Punctuated[PyAlias, PyComma]' 

    def __init__(self, aliases: 'Sequence[PyAlias] | Sequence[tuple[PyAlias, PyComma | None]] | Punctuated[PyAlias, PyComma | None]', *, import_keyword: 'PyImportKeyword | None' = None): ...


class PyImportFromStmt(Node):

    from_keyword: 'PyFromKeyword' 

    path: 'PyPath' 

    import_keyword: 'PyImportKeyword' 

    aliases: 'Punctuated[PyFromAlias, PyComma]' 

    def __init__(self, path: 'PyPath', aliases: 'Sequence[PyFromAlias] | Sequence[tuple[PyFromAlias, PyComma | None]] | Punctuated[PyFromAlias, PyComma | None]', *, from_keyword: 'PyFromKeyword | None' = None, import_keyword: 'PyImportKeyword | None' = None): ...


type PyStmt = PyAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyIfStmt | PyImportStmt | PyImportFromStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt


def is_py_stmt(value: Any) -> TypeGuard[PyStmt]: ...


class PyRetStmt(Node):

    return_keyword: 'PyReturnKeyword' 

    expr: 'PyExpr | None' 

    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None): ...


class PyExprStmt(Node):

    expr: 'PyExpr' 

    def __init__(self, expr: 'PyExpr'): ...


class PyAssignStmt(Node):

    pattern: 'PyPattern' 

    annotation: 'tuple[PyColon, PyExpr] | None' 

    value: 'tuple[PyEquals, PyExpr] | None' 

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None): ...


class PyPassStmt(Node):

    pass_keyword: 'PyPassKeyword' 

    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None): ...


class PyIfCase(Node):

    if_keyword: 'PyIfKeyword' 

    test: 'PyExpr' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, if_keyword: 'PyIfKeyword | None' = None, colon: 'PyColon | None' = None): ...


class PyElifCase(Node):

    elif_keyword: 'PyElifKeyword' 

    test: 'PyExpr' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, elif_keyword: 'PyElifKeyword | None' = None, colon: 'PyColon | None' = None): ...


class PyElseCase(Node):

    else_keyword: 'PyElseKeyword' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None): ...


class PyIfStmt(Node):

    first: 'PyIfCase' 

    alternatives: 'Sequence[PyElifCase]' 

    last: 'PyElseCase | None' 

    def __init__(self, first: 'PyIfCase', *, alternatives: 'Sequence[PyElifCase] | None' = None, last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None' = None): ...


class PyDeleteStmt(Node):

    del_keyword: 'PyDelKeyword' 

    pattern: 'PyPattern' 

    def __init__(self, pattern: 'PyPattern', *, del_keyword: 'PyDelKeyword | None' = None): ...


class PyRaiseStmt(Node):

    raise_keyword: 'PyRaiseKeyword' 

    expr: 'PyExpr' 

    cause: 'tuple[PyFromKeyword, PyExpr] | None' 

    def __init__(self, expr: 'PyExpr', *, raise_keyword: 'PyRaiseKeyword | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None): ...


class PyForStmt(Node):

    for_keyword: 'PyForKeyword' 

    pattern: 'PyPattern' 

    in_keyword: 'PyInKeyword' 

    expr: 'PyExpr' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    else_clause: 'tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None' 

    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None): ...


class PyWhileStmt(Node):

    while_keyword: 'PyWhileKeyword' 

    expr: 'PyExpr' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    else_clause: 'tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None' 

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, while_keyword: 'PyWhileKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None): ...


class PyBreakStmt(Node):

    break_keyword: 'PyBreakKeyword' 

    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None): ...


class PyContinueStmt(Node):

    continue_keyword: 'PyContinueKeyword' 

    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None): ...


class PyTypeAliasStmt(Node):

    type_keyword: 'PyTypeKeyword' 

    name: 'PyIdent' 

    type_params: 'tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None' 

    equals: 'PyEquals' 

    expr: 'PyExpr' 

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, type_keyword: 'PyTypeKeyword | None' = None, type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma | None] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma | None] | None' = None, equals: 'PyEquals | None' = None): ...


class PyExceptHandler(Node):

    except_keyword: 'PyExceptKeyword' 

    expr: 'PyExpr' 

    binder: 'tuple[PyAsKeyword, PyIdent] | None' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, except_keyword: 'PyExceptKeyword | None' = None, binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None, colon: 'PyColon | None' = None): ...


class PyTryStmt(Node):

    try_keyword: 'PyTryKeyword' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    handlers: 'Sequence[PyExceptHandler]' 

    else_clause: 'tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None' 

    finally_clause: 'tuple[PyFinallyKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None' 

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, handlers: 'Sequence[PyExceptHandler] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None, finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None): ...


class PyClassDef(Node):

    decorators: 'Sequence[PyDecorator]' 

    class_keyword: 'PyClassKeyword' 

    name: 'PyIdent' 

    bases: 'tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, class_keyword: 'PyClassKeyword | None' = None, bases: 'tuple[PyOpenParen | None, Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma | None] | None, PyCloseParen | None] | Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma | None] | None' = None, colon: 'PyColon | None' = None): ...


type PyParam = PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam


def is_py_param(value: Any) -> TypeGuard[PyParam]: ...


class PyNamedParam(Node):

    pattern: 'PyPattern' 

    annotation: 'tuple[PyColon, PyExpr] | None' 

    default: 'tuple[PyEquals, PyExpr] | None' 

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None): ...


class PyRestPosParam(Node):

    asterisk: 'PyAsterisk' 

    name: 'PyIdent' 

    def __init__(self, name: 'PyIdent | str', *, asterisk: 'PyAsterisk | None' = None): ...


class PyRestKeywordParam(Node):

    asterisk_asterisk: 'PyAsteriskAsterisk' 

    name: 'PyIdent' 

    def __init__(self, name: 'PyIdent | str', *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None): ...


class PySepParam(Node):

    asterisk: 'PyAsterisk' 

    def __init__(self, *, asterisk: 'PyAsterisk | None' = None): ...


class PyDecorator(Node):

    at_sign: 'PyAtSign' 

    expr: 'PyExpr' 

    def __init__(self, expr: 'PyExpr', *, at_sign: 'PyAtSign | None' = None): ...


class PyFuncDef(Node):

    decorators: 'Sequence[PyDecorator]' 

    async_keyword: 'PyAsyncKeyword | None' 

    def_keyword: 'PyDefKeyword' 

    name: 'PyIdent' 

    open_paren: 'PyOpenParen' 

    params: 'Punctuated[PyParam, PyComma]' 

    close_paren: 'PyCloseParen' 

    return_type: 'tuple[PyRArrow, PyExpr] | None' 

    colon: 'PyColon' 

    body: 'PyStmt | Sequence[PyStmt]' 

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, open_paren: 'PyOpenParen | None' = None, params: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | Punctuated[PyParam, PyComma | None] | None' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None' = None, colon: 'PyColon | None' = None): ...


class PyModule(Node):

    stmts: 'Sequence[PyStmt]' 

    def __init__(self, *, stmts: 'Sequence[PyStmt] | None' = None): ...


class PyTilde(Token):

    def __init__(self, span: Span | None = None): ...


class PyVerticalBar(Token):

    def __init__(self, span: Span | None = None): ...


class PyWhileKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyTypeKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyTryKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyReturnKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyRaiseKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyPassKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyOrKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyNotKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyIsKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyInKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyImportKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyIfKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyFromKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyForKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyFinallyKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyExceptKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyElseKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyElifKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyDelKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyDefKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyContinueKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyClassKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyBreakKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyAsyncKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyAsKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyAndKeyword(Token):

    def __init__(self, span: Span | None = None): ...


class PyCaret(Token):

    def __init__(self, span: Span | None = None): ...


class PyCloseBracket(Token):

    def __init__(self, span: Span | None = None): ...


class PyOpenBracket(Token):

    def __init__(self, span: Span | None = None): ...


class PyAtSign(Token):

    def __init__(self, span: Span | None = None): ...


class PyGreaterThanGreaterThan(Token):

    def __init__(self, span: Span | None = None): ...


class PyGreaterThanEquals(Token):

    def __init__(self, span: Span | None = None): ...


class PyGreaterThan(Token):

    def __init__(self, span: Span | None = None): ...


class PyEqualsEquals(Token):

    def __init__(self, span: Span | None = None): ...


class PyEquals(Token):

    def __init__(self, span: Span | None = None): ...


class PyLessThanEquals(Token):

    def __init__(self, span: Span | None = None): ...


class PyLessThanLessThan(Token):

    def __init__(self, span: Span | None = None): ...


class PyLessThan(Token):

    def __init__(self, span: Span | None = None): ...


class PySemicolon(Token):

    def __init__(self, span: Span | None = None): ...


class PyColon(Token):

    def __init__(self, span: Span | None = None): ...


class PySlashSlash(Token):

    def __init__(self, span: Span | None = None): ...


class PySlash(Token):

    def __init__(self, span: Span | None = None): ...


class PyDotDotDot(Token):

    def __init__(self, span: Span | None = None): ...


class PyDot(Token):

    def __init__(self, span: Span | None = None): ...


class PyRArrow(Token):

    def __init__(self, span: Span | None = None): ...


class PyHyphen(Token):

    def __init__(self, span: Span | None = None): ...


class PyComma(Token):

    def __init__(self, span: Span | None = None): ...


class PyPlus(Token):

    def __init__(self, span: Span | None = None): ...


class PyAsteriskAsterisk(Token):

    def __init__(self, span: Span | None = None): ...


class PyAsterisk(Token):

    def __init__(self, span: Span | None = None): ...


class PyCloseParen(Token):

    def __init__(self, span: Span | None = None): ...


class PyOpenParen(Token):

    def __init__(self, span: Span | None = None): ...


class PyAmpersand(Token):

    def __init__(self, span: Span | None = None): ...


class PyPercent(Token):

    def __init__(self, span: Span | None = None): ...


class PyHashtag(Token):

    def __init__(self, span: Span | None = None): ...


class PyExclamationMarkEquals(Token):

    def __init__(self, span: Span | None = None): ...


class PyCarriageReturnLineFeed(Token):

    def __init__(self, span: Span | None = None): ...


class PyLineFeed(Token):

    def __init__(self, span: Span | None = None): ...


def is_py_syntax(value: Any) -> TypeGuard[PySyntax]: ...


def is_py_node(value: Any) -> TypeGuard[PyNode]: ...


def is_py_token(value: Any) -> TypeGuard[PyToken]: ...


type PySyntax = PyNode | PyToken


type PyToken = PyIdent | PyFloat | PyInteger | PyString | PyTilde | PyVerticalBar | PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyIsKeyword | PyInKeyword | PyImportKeyword | PyIfKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword | PyCaret | PyCloseBracket | PyOpenBracket | PyAtSign | PyGreaterThanGreaterThan | PyGreaterThanEquals | PyGreaterThan | PyEqualsEquals | PyEquals | PyLessThanEquals | PyLessThanLessThan | PyLessThan | PySemicolon | PyColon | PySlashSlash | PySlash | PyDotDotDot | PyDot | PyRArrow | PyHyphen | PyComma | PyPlus | PyAsteriskAsterisk | PyAsterisk | PyCloseParen | PyOpenParen | PyAmpersand | PyPercent | PyHashtag | PyExclamationMarkEquals | PyCarriageReturnLineFeed | PyLineFeed


type PyNode = PySlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyEllipsisExpr | PyGuard | PyComprehension | PyGeneratorExpr | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleExpr | PyKeywordArg | PyCallExpr | PyPrefixExpr | PyInfixExpr | PyQualName | PyAbsolutePath | PyRelativePath | PyAlias | PyFromAlias | PyImportStmt | PyImportFromStmt | PyRetStmt | PyExprStmt | PyAssignStmt | PyPassStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PySepParam | PyDecorator | PyFuncDef | PyModule


