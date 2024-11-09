from typing import Any, TypeGuard, TypedDict, Never, Unpack, Sequence, no_type_check


from magelang.runtime import BaseSyntax, Punctuated, Span


class _PyBaseSyntax(BaseSyntax):

    pass


class _PyBaseNode(_PyBaseSyntax):

    pass


class _PyBaseToken(_PyBaseSyntax):

    def __init__(self, span: Span | None = None):
        self.span = span


class PyIdent(_PyBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyFloat(_PyBaseToken):

    def __init__(self, value: float, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyInteger(_PyBaseToken):

    def __init__(self, value: int, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyString(_PyBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class PyTilde(_PyBaseToken):

    pass


class PyVerticalBar(_PyBaseToken):

    pass


class PyWhileKeyword(_PyBaseToken):

    pass


class PyTypeKeyword(_PyBaseToken):

    pass


class PyTryKeyword(_PyBaseToken):

    pass


class PyReturnKeyword(_PyBaseToken):

    pass


class PyRaiseKeyword(_PyBaseToken):

    pass


class PyPassKeyword(_PyBaseToken):

    pass


class PyOrKeyword(_PyBaseToken):

    pass


class PyNotKeyword(_PyBaseToken):

    pass


class PyNonlocalKeyword(_PyBaseToken):

    pass


class PyIsKeyword(_PyBaseToken):

    pass


class PyInKeyword(_PyBaseToken):

    pass


class PyImportKeyword(_PyBaseToken):

    pass


class PyIfKeyword(_PyBaseToken):

    pass


class PyGlobalKeyword(_PyBaseToken):

    pass


class PyFromKeyword(_PyBaseToken):

    pass


class PyForKeyword(_PyBaseToken):

    pass


class PyFinallyKeyword(_PyBaseToken):

    pass


class PyExceptKeyword(_PyBaseToken):

    pass


class PyElseKeyword(_PyBaseToken):

    pass


class PyElifKeyword(_PyBaseToken):

    pass


class PyDelKeyword(_PyBaseToken):

    pass


class PyDefKeyword(_PyBaseToken):

    pass


class PyContinueKeyword(_PyBaseToken):

    pass


class PyClassKeyword(_PyBaseToken):

    pass


class PyBreakKeyword(_PyBaseToken):

    pass


class PyAsyncKeyword(_PyBaseToken):

    pass


class PyAsKeyword(_PyBaseToken):

    pass


class PyAndKeyword(_PyBaseToken):

    pass


class PyCaret(_PyBaseToken):

    pass


class PyCloseBracket(_PyBaseToken):

    pass


class PyOpenBracket(_PyBaseToken):

    pass


class PyAtSign(_PyBaseToken):

    pass


class PyGreaterThanGreaterThan(_PyBaseToken):

    pass


class PyGreaterThanEquals(_PyBaseToken):

    pass


class PyGreaterThan(_PyBaseToken):

    pass


class PyEqualsEquals(_PyBaseToken):

    pass


class PyEquals(_PyBaseToken):

    pass


class PyLessThanEquals(_PyBaseToken):

    pass


class PyLessThanLessThan(_PyBaseToken):

    pass


class PyLessThan(_PyBaseToken):

    pass


class PySemicolon(_PyBaseToken):

    pass


class PyColon(_PyBaseToken):

    pass


class PySlashSlash(_PyBaseToken):

    pass


class PySlash(_PyBaseToken):

    pass


class PyDotDotDot(_PyBaseToken):

    pass


class PyDot(_PyBaseToken):

    pass


class PyRArrow(_PyBaseToken):

    pass


class PyHyphen(_PyBaseToken):

    pass


class PyComma(_PyBaseToken):

    pass


class PyPlus(_PyBaseToken):

    pass


class PyAsteriskAsterisk(_PyBaseToken):

    pass


class PyAsterisk(_PyBaseToken):

    pass


class PyCloseParen(_PyBaseToken):

    pass


class PyOpenParen(_PyBaseToken):

    pass


class PyAmpersand(_PyBaseToken):

    pass


class PyPercent(_PyBaseToken):

    pass


class PyHashtag(_PyBaseToken):

    pass


class PyExclamationMarkEquals(_PyBaseToken):

    pass


class PyCarriageReturnLineFeed(_PyBaseToken):

    pass


class PyLineFeed(_PyBaseToken):

    pass


class PySliceDeriveKwargs(TypedDict, total=False):

    lower: 'PyExpr | None'

    colon: 'PyColon | None'

    upper: 'PyExpr | None'

    step: 'PyExpr | tuple[PyColon | None, PyExpr] | None'


class PySlice(_PyBaseNode):

    def __init__(self, *, lower: 'PyExpr | None' = None, colon: 'PyColon | None' = None, upper: 'PyExpr | None' = None, step: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.lower: PyExpr | None = _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(lower)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.upper: PyExpr | None = _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(upper)
        self.step: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(step)

    def derive(self, **kwargs: Unpack[PySliceDeriveKwargs]) -> 'PySlice':
        return PySlice(lower=lower, colon=colon, upper=upper, step=step)

    def parent(self) -> 'PySliceParent':
        assert(self._parent is not None)
        return self._parent


class PyNamedPatternDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'


class PyNamedPattern(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    def derive(self, **kwargs: Unpack[PyNamedPatternDeriveKwargs]) -> 'PyNamedPattern':
        return PyNamedPattern(name=name)

    def parent(self) -> 'PyNamedPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyAttrPatternDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    dot: 'PyDot | None'

    name: 'PyIdent | str'


class PyAttrPattern(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', name: 'PyIdent | str', *, dot: 'PyDot | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.dot: PyDot = _coerce_union_2_token_dot_none_to_token_dot(dot)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    def derive(self, **kwargs: Unpack[PyAttrPatternDeriveKwargs]) -> 'PyAttrPattern':
        return PyAttrPattern(pattern=pattern, dot=dot, name=name)

    def parent(self) -> 'PyAttrPatternParent':
        assert(self._parent is not None)
        return self._parent


class PySubscriptPatternDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    open_bracket: 'PyOpenBracket | None'

    slices: 'Sequence[tuple[PySlice | PyPattern, PyComma | None]] | Sequence[PySlice | PyPattern] | Punctuated[PySlice | PyPattern, PyComma]'

    close_bracket: 'PyCloseBracket | None'


class PySubscriptPattern(_PyBaseNode):

    def count_slices(self) -> int:
        return len(self.slices)

    def __init__(self, pattern: 'PyPattern', slices: 'Sequence[tuple[PySlice | PyPattern, PyComma | None]] | Sequence[PySlice | PyPattern] | Punctuated[PySlice | PyPattern, PyComma]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.slices: Punctuated[PySlice | PyPattern, PyComma] = _coerce_union_3_list_tuple_2_union_2_node_slice_variant_pattern_union_2_token_comma_none_required_list_union_2_node_slice_variant_pattern_required_punct_union_2_node_slice_variant_pattern_token_comma_required_to_punct_union_2_node_slice_variant_pattern_token_comma_required(slices)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    def derive(self, **kwargs: Unpack[PySubscriptPatternDeriveKwargs]) -> 'PySubscriptPattern':
        return PySubscriptPattern(pattern=pattern, open_bracket=open_bracket, slices=slices, close_bracket=close_bracket)

    def parent(self) -> 'PySubscriptPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyStarredPatternDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'

    expr: 'PyExpr'


class PyStarredPattern(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyStarredPatternDeriveKwargs]) -> 'PyStarredPattern':
        return PyStarredPattern(asterisk=asterisk, expr=expr)

    def parent(self) -> 'PyStarredPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyListPatternDeriveKwargs(TypedDict, total=False):

    open_bracket: 'PyOpenBracket | None'

    elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None'

    close_bracket: 'PyCloseBracket | None'


class PyListPattern(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.elements: Punctuated[PyPattern, PyComma] = _coerce_union_4_list_variant_pattern_list_tuple_2_variant_pattern_union_2_token_comma_none_punct_variant_pattern_token_comma_none_to_punct_variant_pattern_token_comma(elements)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    def derive(self, **kwargs: Unpack[PyListPatternDeriveKwargs]) -> 'PyListPattern':
        return PyListPattern(open_bracket=open_bracket, elements=elements, close_bracket=close_bracket)

    def parent(self) -> 'PyListPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyTuplePatternDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None'

    close_paren: 'PyCloseParen | None'


class PyTuplePattern(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.elements: Punctuated[PyPattern, PyComma] = _coerce_union_4_list_variant_pattern_list_tuple_2_variant_pattern_union_2_token_comma_none_punct_variant_pattern_token_comma_none_to_punct_variant_pattern_token_comma(elements)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    def derive(self, **kwargs: Unpack[PyTuplePatternDeriveKwargs]) -> 'PyTuplePattern':
        return PyTuplePattern(open_paren=open_paren, elements=elements, close_paren=close_paren)

    def parent(self) -> 'PyTuplePatternParent':
        assert(self._parent is not None)
        return self._parent


class PyEllipsisExprDeriveKwargs(TypedDict, total=False):

    dot_dot_dot: 'PyDotDotDot | None'


class PyEllipsisExpr(_PyBaseNode):

    def __init__(self, *, dot_dot_dot: 'PyDotDotDot | None' = None) -> None:
        self.dot_dot_dot: PyDotDotDot = _coerce_union_2_token_dot_dot_dot_none_to_token_dot_dot_dot(dot_dot_dot)

    def derive(self, **kwargs: Unpack[PyEllipsisExprDeriveKwargs]) -> 'PyEllipsisExpr':
        return PyEllipsisExpr(dot_dot_dot=dot_dot_dot)

    def parent(self) -> 'PyEllipsisExprParent':
        assert(self._parent is not None)
        return self._parent


class PyGuardDeriveKwargs(TypedDict, total=False):

    if_keyword: 'PyIfKeyword | None'

    expr: 'PyExpr'


class PyGuard(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None) -> None:
        self.if_keyword: PyIfKeyword = _coerce_union_2_token_if_keyword_none_to_token_if_keyword(if_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyGuardDeriveKwargs]) -> 'PyGuard':
        return PyGuard(if_keyword=if_keyword, expr=expr)

    def parent(self) -> 'PyGuardParent':
        assert(self._parent is not None)
        return self._parent


class PyComprehensionDeriveKwargs(TypedDict, total=False):

    async_keyword: 'PyAsyncKeyword | None'

    for_keyword: 'PyForKeyword | None'

    pattern: 'PyPattern'

    in_keyword: 'PyInKeyword | None'

    target: 'PyExpr'

    guards: 'Sequence[PyGuard | PyExpr] | None'


class PyComprehension(_PyBaseNode):

    def count_guards(self) -> int:
        return len(self.guards)

    def __init__(self, pattern: 'PyPattern', target: 'PyExpr', *, async_keyword: 'PyAsyncKeyword | None' = None, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, guards: 'Sequence[PyGuard | PyExpr] | None' = None) -> None:
        self.async_keyword: PyAsyncKeyword | None = _coerce_union_2_token_async_keyword_none_to_union_2_token_async_keyword_none(async_keyword)
        self.for_keyword: PyForKeyword = _coerce_union_2_token_for_keyword_none_to_token_for_keyword(for_keyword)
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.in_keyword: PyInKeyword = _coerce_union_2_token_in_keyword_none_to_token_in_keyword(in_keyword)
        self.target: PyExpr = _coerce_variant_expr_to_variant_expr(target)
        self.guards: Sequence[PyGuard] = _coerce_union_2_list_union_2_node_guard_variant_expr_none_to_list_node_guard(guards)

    def derive(self, **kwargs: Unpack[PyComprehensionDeriveKwargs]) -> 'PyComprehension':
        return PyComprehension(async_keyword=async_keyword, for_keyword=for_keyword, pattern=pattern, in_keyword=in_keyword, target=target, guards=guards)

    def parent(self) -> 'PyComprehensionParent':
        assert(self._parent is not None)
        return self._parent


class PyGeneratorExprDeriveKwargs(TypedDict, total=False):

    element: 'PyExpr'

    generators: 'Sequence[PyComprehension]'


class PyGeneratorExpr(_PyBaseNode):

    def count_generators(self) -> int:
        return len(self.generators)

    def __init__(self, element: 'PyExpr', generators: 'Sequence[PyComprehension]') -> None:
        self.element: PyExpr = _coerce_variant_expr_to_variant_expr(element)
        self.generators: Sequence[PyComprehension] = _coerce_list_node_comprehension_required_to_list_node_comprehension_required(generators)

    def derive(self, **kwargs: Unpack[PyGeneratorExprDeriveKwargs]) -> 'PyGeneratorExpr':
        return PyGeneratorExpr(element=element, generators=generators)

    def parent(self) -> 'PyGeneratorExprParent':
        assert(self._parent is not None)
        return self._parent


class PyIfExprDeriveKwargs(TypedDict, total=False):

    then: 'PyExpr'

    if_keyword: 'PyIfKeyword | None'

    test: 'PyExpr'

    else_keyword: 'PyElseKeyword | None'

    alt: 'PyExpr'


class PyIfExpr(_PyBaseNode):

    def __init__(self, then: 'PyExpr', test: 'PyExpr', alt: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None, else_keyword: 'PyElseKeyword | None' = None) -> None:
        self.then: PyExpr = _coerce_variant_expr_to_variant_expr(then)
        self.if_keyword: PyIfKeyword = _coerce_union_2_token_if_keyword_none_to_token_if_keyword(if_keyword)
        self.test: PyExpr = _coerce_variant_expr_to_variant_expr(test)
        self.else_keyword: PyElseKeyword = _coerce_union_2_token_else_keyword_none_to_token_else_keyword(else_keyword)
        self.alt: PyExpr = _coerce_variant_expr_to_variant_expr(alt)

    def derive(self, **kwargs: Unpack[PyIfExprDeriveKwargs]) -> 'PyIfExpr':
        return PyIfExpr(then=then, if_keyword=if_keyword, test=test, else_keyword=else_keyword, alt=alt)

    def parent(self) -> 'PyIfExprParent':
        assert(self._parent is not None)
        return self._parent


class PyConstExprDeriveKwargs(TypedDict, total=False):

    literal: 'PyFloat | PyInteger | PyString | float | int | str'


class PyConstExpr(_PyBaseNode):

    def __init__(self, literal: 'PyFloat | PyInteger | PyString | float | int | str') -> None:
        self.literal: PyFloat | PyInteger | PyString = _coerce_union_6_token_float_token_integer_token_string_extern_float_extern_integer_extern_string_to_union_3_token_float_token_integer_token_string(literal)

    def derive(self, **kwargs: Unpack[PyConstExprDeriveKwargs]) -> 'PyConstExpr':
        return PyConstExpr(literal=literal)

    def parent(self) -> 'PyConstExprParent':
        assert(self._parent is not None)
        return self._parent


class PyNestExprDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    expr: 'PyExpr'

    close_paren: 'PyCloseParen | None'


class PyNestExpr(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    def derive(self, **kwargs: Unpack[PyNestExprDeriveKwargs]) -> 'PyNestExpr':
        return PyNestExpr(open_paren=open_paren, expr=expr, close_paren=close_paren)

    def parent(self) -> 'PyNestExprParent':
        assert(self._parent is not None)
        return self._parent


class PyNamedExprDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'


class PyNamedExpr(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    def derive(self, **kwargs: Unpack[PyNamedExprDeriveKwargs]) -> 'PyNamedExpr':
        return PyNamedExpr(name=name)

    def parent(self) -> 'PyNamedExprParent':
        assert(self._parent is not None)
        return self._parent


class PyAttrExprDeriveKwargs(TypedDict, total=False):

    expr: 'PyExpr'

    dot: 'PyDot | None'

    name: 'PyIdent | str'


class PyAttrExpr(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', name: 'PyIdent | str', *, dot: 'PyDot | None' = None) -> None:
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.dot: PyDot = _coerce_union_2_token_dot_none_to_token_dot(dot)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    def derive(self, **kwargs: Unpack[PyAttrExprDeriveKwargs]) -> 'PyAttrExpr':
        return PyAttrExpr(expr=expr, dot=dot, name=name)

    def parent(self) -> 'PyAttrExprParent':
        assert(self._parent is not None)
        return self._parent


class PySubscriptExprDeriveKwargs(TypedDict, total=False):

    expr: 'PyExpr'

    open_bracket: 'PyOpenBracket | None'

    slices: 'Sequence[tuple[PySlice | PyExpr, PyComma | None]] | Sequence[PySlice | PyExpr] | Punctuated[PySlice | PyExpr, PyComma]'

    close_bracket: 'PyCloseBracket | None'


class PySubscriptExpr(_PyBaseNode):

    def count_slices(self) -> int:
        return len(self.slices)

    def __init__(self, expr: 'PyExpr', slices: 'Sequence[tuple[PySlice | PyExpr, PyComma | None]] | Sequence[PySlice | PyExpr] | Punctuated[PySlice | PyExpr, PyComma]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.slices: Punctuated[PySlice | PyExpr, PyComma] = _coerce_union_3_list_tuple_2_union_2_node_slice_variant_expr_union_2_token_comma_none_required_list_union_2_node_slice_variant_expr_required_punct_union_2_node_slice_variant_expr_token_comma_required_to_punct_union_2_node_slice_variant_expr_token_comma_required(slices)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    def derive(self, **kwargs: Unpack[PySubscriptExprDeriveKwargs]) -> 'PySubscriptExpr':
        return PySubscriptExpr(expr=expr, open_bracket=open_bracket, slices=slices, close_bracket=close_bracket)

    def parent(self) -> 'PySubscriptExprParent':
        assert(self._parent is not None)
        return self._parent


class PyStarredExprDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'

    expr: 'PyExpr'


class PyStarredExpr(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyStarredExprDeriveKwargs]) -> 'PyStarredExpr':
        return PyStarredExpr(asterisk=asterisk, expr=expr)

    def parent(self) -> 'PyStarredExprParent':
        assert(self._parent is not None)
        return self._parent


class PyListExprDeriveKwargs(TypedDict, total=False):

    open_bracket: 'PyOpenBracket | None'

    elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None'

    close_bracket: 'PyCloseBracket | None'


class PyListExpr(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.elements: Punctuated[PyExpr, PyComma] = _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(elements)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    def derive(self, **kwargs: Unpack[PyListExprDeriveKwargs]) -> 'PyListExpr':
        return PyListExpr(open_bracket=open_bracket, elements=elements, close_bracket=close_bracket)

    def parent(self) -> 'PyListExprParent':
        assert(self._parent is not None)
        return self._parent


class PyTupleExprDeriveKwargs(TypedDict, total=False):

    open_paren: 'PyOpenParen | None'

    elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None'

    close_paren: 'PyCloseParen | None'


class PyTupleExpr(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.elements: Punctuated[PyExpr, PyComma] = _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(elements)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    def derive(self, **kwargs: Unpack[PyTupleExprDeriveKwargs]) -> 'PyTupleExpr':
        return PyTupleExpr(open_paren=open_paren, elements=elements, close_paren=close_paren)

    def parent(self) -> 'PyTupleExprParent':
        assert(self._parent is not None)
        return self._parent


class PyKeywordArgDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyKeywordArg(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.equals: PyEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyKeywordArgDeriveKwargs]) -> 'PyKeywordArg':
        return PyKeywordArg(name=name, equals=equals, expr=expr)

    def parent(self) -> 'PyKeywordArgParent':
        assert(self._parent is not None)
        return self._parent


class PyCallExprDeriveKwargs(TypedDict, total=False):

    operator: 'PyExpr'

    open_paren: 'PyOpenParen | None'

    args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma] | None'

    close_paren: 'PyCloseParen | None'


class PyCallExpr(_PyBaseNode):

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, operator: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.operator: PyExpr = _coerce_variant_expr_to_variant_expr(operator)
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.args: Punctuated[PyArg, PyComma] = _coerce_union_4_list_variant_arg_list_tuple_2_variant_arg_union_2_token_comma_none_punct_variant_arg_token_comma_none_to_punct_variant_arg_token_comma(args)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    def derive(self, **kwargs: Unpack[PyCallExprDeriveKwargs]) -> 'PyCallExpr':
        return PyCallExpr(operator=operator, open_paren=open_paren, args=args, close_paren=close_paren)

    def parent(self) -> 'PyCallExprParent':
        assert(self._parent is not None)
        return self._parent


class PyPrefixExprDeriveKwargs(TypedDict, total=False):

    prefix_op: 'PyPrefixOp'

    expr: 'PyExpr'


class PyPrefixExpr(_PyBaseNode):

    def __init__(self, prefix_op: 'PyPrefixOp', expr: 'PyExpr') -> None:
        self.prefix_op: PyPrefixOp = _coerce_variant_prefix_op_to_variant_prefix_op(prefix_op)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyPrefixExprDeriveKwargs]) -> 'PyPrefixExpr':
        return PyPrefixExpr(prefix_op=prefix_op, expr=expr)

    def parent(self) -> 'PyPrefixExprParent':
        assert(self._parent is not None)
        return self._parent


class PyInfixExprDeriveKwargs(TypedDict, total=False):

    left: 'PyExpr'

    op: 'PyInfixOp'

    right: 'PyExpr'


class PyInfixExpr(_PyBaseNode):

    def __init__(self, left: 'PyExpr', op: 'PyInfixOp', right: 'PyExpr') -> None:
        self.left: PyExpr = _coerce_variant_expr_to_variant_expr(left)
        self.op: PyInfixOp = _coerce_variant_infix_op_to_variant_infix_op(op)
        self.right: PyExpr = _coerce_variant_expr_to_variant_expr(right)

    def derive(self, **kwargs: Unpack[PyInfixExprDeriveKwargs]) -> 'PyInfixExpr':
        return PyInfixExpr(left=left, op=op, right=right)

    def parent(self) -> 'PyInfixExprParent':
        assert(self._parent is not None)
        return self._parent


class PyQualNameDeriveKwargs(TypedDict, total=False):

    modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None'

    name: 'PyIdent | str'


class PyQualName(_PyBaseNode):

    def count_modules(self) -> int:
        return len(self.modules)

    def __init__(self, name: 'PyIdent | str', *, modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None' = None) -> None:
        self.modules: Sequence[tuple[PyIdent, PyDot]] = _coerce_union_2_list_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_dot_none_extern_string_none_to_list_tuple_2_token_ident_token_dot(modules)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    def derive(self, **kwargs: Unpack[PyQualNameDeriveKwargs]) -> 'PyQualName':
        return PyQualName(modules=modules, name=name)

    def parent(self) -> 'PyQualNameParent':
        assert(self._parent is not None)
        return self._parent


class PyAbsolutePathDeriveKwargs(TypedDict, total=False):

    name: 'PyQualName | PyIdent | str'


class PyAbsolutePath(_PyBaseNode):

    def __init__(self, name: 'PyQualName | PyIdent | str') -> None:
        self.name: PyQualName = _coerce_union_3_node_qual_name_token_ident_extern_string_to_node_qual_name(name)

    def derive(self, **kwargs: Unpack[PyAbsolutePathDeriveKwargs]) -> 'PyAbsolutePath':
        return PyAbsolutePath(name=name)

    def parent(self) -> 'PyAbsolutePathParent':
        assert(self._parent is not None)
        return self._parent


class PyRelativePathDeriveKwargs(TypedDict, total=False):

    dots: 'Sequence[PyDot] | int'

    name: 'PyQualName | PyIdent | None | str'


class PyRelativePath(_PyBaseNode):

    def count_dots(self) -> int:
        return len(self.dots)

    def __init__(self, dots: 'Sequence[PyDot] | int', *, name: 'PyQualName | PyIdent | None | str' = None) -> None:
        self.dots: Sequence[PyDot] = _coerce_union_2_list_token_dot_required_extern_integer_to_list_token_dot_required(dots)
        self.name: PyQualName | None = _coerce_union_4_node_qual_name_token_ident_none_extern_string_to_union_2_node_qual_name_none(name)

    def derive(self, **kwargs: Unpack[PyRelativePathDeriveKwargs]) -> 'PyRelativePath':
        return PyRelativePath(dots=dots, name=name)

    def parent(self) -> 'PyRelativePathParent':
        assert(self._parent is not None)
        return self._parent


class PyAliasDeriveKwargs(TypedDict, total=False):

    path: 'PyPath'

    asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str'


class PyAlias(_PyBaseNode):

    def __init__(self, path: 'PyPath', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> None:
        self.path: PyPath = _coerce_variant_path_to_variant_path(path)
        self.asname: tuple[PyAsKeyword, PyIdent] | None = _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(asname)

    def derive(self, **kwargs: Unpack[PyAliasDeriveKwargs]) -> 'PyAlias':
        return PyAlias(path=path, asname=asname)

    def parent(self) -> 'PyAliasParent':
        assert(self._parent is not None)
        return self._parent


class PyFromAliasDeriveKwargs(TypedDict, total=False):

    name: 'PyAsterisk | PyIdent | str'

    asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str'


class PyFromAlias(_PyBaseNode):

    def __init__(self, name: 'PyAsterisk | PyIdent | str', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> None:
        self.name: PyAsterisk | PyIdent = _coerce_union_3_token_asterisk_token_ident_extern_string_to_union_2_token_asterisk_token_ident(name)
        self.asname: tuple[PyAsKeyword, PyIdent] | None = _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(asname)

    def derive(self, **kwargs: Unpack[PyFromAliasDeriveKwargs]) -> 'PyFromAlias':
        return PyFromAlias(name=name, asname=asname)

    def parent(self) -> 'PyFromAliasParent':
        assert(self._parent is not None)
        return self._parent


class PyImportStmtDeriveKwargs(TypedDict, total=False):

    import_keyword: 'PyImportKeyword | None'

    aliases: 'Sequence[tuple[PyAlias | PyPath, PyComma | None]] | Sequence[PyAlias | PyPath] | Punctuated[PyAlias | PyPath, PyComma]'


class PyImportStmt(_PyBaseNode):

    def count_aliases(self) -> int:
        return len(self.aliases)

    def __init__(self, aliases: 'Sequence[tuple[PyAlias | PyPath, PyComma | None]] | Sequence[PyAlias | PyPath] | Punctuated[PyAlias | PyPath, PyComma]', *, import_keyword: 'PyImportKeyword | None' = None) -> None:
        self.import_keyword: PyImportKeyword = _coerce_union_2_token_import_keyword_none_to_token_import_keyword(import_keyword)
        self.aliases: Punctuated[PyAlias, PyComma] = _coerce_union_3_list_tuple_2_union_2_node_alias_variant_path_union_2_token_comma_none_required_list_union_2_node_alias_variant_path_required_punct_union_2_node_alias_variant_path_token_comma_required_to_punct_node_alias_token_comma_required(aliases)

    def derive(self, **kwargs: Unpack[PyImportStmtDeriveKwargs]) -> 'PyImportStmt':
        return PyImportStmt(import_keyword=import_keyword, aliases=aliases)

    def parent(self) -> 'PyImportStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyImportFromStmtDeriveKwargs(TypedDict, total=False):

    from_keyword: 'PyFromKeyword | None'

    path: 'PyPath'

    import_keyword: 'PyImportKeyword | None'

    aliases: 'Sequence[tuple[PyFromAlias | PyAsterisk | PyIdent | str, PyComma | None]] | Sequence[PyFromAlias | PyAsterisk | PyIdent | str] | Punctuated[PyFromAlias | PyAsterisk | PyIdent | str, PyComma]'


class PyImportFromStmt(_PyBaseNode):

    def count_aliases(self) -> int:
        return len(self.aliases)

    def __init__(self, path: 'PyPath', aliases: 'Sequence[tuple[PyFromAlias | PyAsterisk | PyIdent | str, PyComma | None]] | Sequence[PyFromAlias | PyAsterisk | PyIdent | str] | Punctuated[PyFromAlias | PyAsterisk | PyIdent | str, PyComma]', *, from_keyword: 'PyFromKeyword | None' = None, import_keyword: 'PyImportKeyword | None' = None) -> None:
        self.from_keyword: PyFromKeyword = _coerce_union_2_token_from_keyword_none_to_token_from_keyword(from_keyword)
        self.path: PyPath = _coerce_variant_path_to_variant_path(path)
        self.import_keyword: PyImportKeyword = _coerce_union_2_token_import_keyword_none_to_token_import_keyword(import_keyword)
        self.aliases: Punctuated[PyFromAlias, PyComma] = _coerce_union_3_list_tuple_2_union_4_node_from_alias_token_asterisk_token_ident_extern_string_union_2_token_comma_none_required_list_union_4_node_from_alias_token_asterisk_token_ident_extern_string_required_punct_union_4_node_from_alias_token_asterisk_token_ident_extern_string_token_comma_required_to_punct_node_from_alias_token_comma_required(aliases)

    def derive(self, **kwargs: Unpack[PyImportFromStmtDeriveKwargs]) -> 'PyImportFromStmt':
        return PyImportFromStmt(from_keyword=from_keyword, path=path, import_keyword=import_keyword, aliases=aliases)

    def parent(self) -> 'PyImportFromStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyRetStmtDeriveKwargs(TypedDict, total=False):

    return_keyword: 'PyReturnKeyword | None'

    expr: 'PyExpr | None'


class PyRetStmt(_PyBaseNode):

    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> None:
        self.return_keyword: PyReturnKeyword = _coerce_union_2_token_return_keyword_none_to_token_return_keyword(return_keyword)
        self.expr: PyExpr | None = _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(expr)

    def derive(self, **kwargs: Unpack[PyRetStmtDeriveKwargs]) -> 'PyRetStmt':
        return PyRetStmt(return_keyword=return_keyword, expr=expr)

    def parent(self) -> 'PyRetStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyExprStmtDeriveKwargs(TypedDict, total=False):

    expr: 'PyExpr'


class PyExprStmt(_PyBaseNode):

    def __init__(self, expr: 'PyExpr') -> None:
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyExprStmtDeriveKwargs]) -> 'PyExprStmt':
        return PyExprStmt(expr=expr)

    def parent(self) -> 'PyExprStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyAugAssignStmtDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'

    op: 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyAugAssignStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', op: 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar', expr: 'PyExpr', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, equals: 'PyEquals | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)
        self.op: PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar = _coerce_union_13_token_ampersand_token_asterisk_token_asterisk_asterisk_token_at_sign_token_caret_token_greater_than_greater_than_token_hyphen_token_less_than_less_than_token_percent_token_plus_token_slash_token_slash_slash_token_vertical_bar_to_union_13_token_ampersand_token_asterisk_token_asterisk_asterisk_token_at_sign_token_caret_token_greater_than_greater_than_token_hyphen_token_less_than_less_than_token_percent_token_plus_token_slash_token_slash_slash_token_vertical_bar(op)
        self.equals: PyEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyAugAssignStmtDeriveKwargs]) -> 'PyAugAssignStmt':
        return PyAugAssignStmt(pattern=pattern, annotation=annotation, op=op, equals=equals, expr=expr)

    def parent(self) -> 'PyAugAssignStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyAssignStmtDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'

    value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None'


class PyAssignStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)
        self.value: tuple[PyEquals, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_equals_none_variant_expr_none_to_union_2_tuple_2_token_equals_variant_expr_none(value)

    def derive(self, **kwargs: Unpack[PyAssignStmtDeriveKwargs]) -> 'PyAssignStmt':
        return PyAssignStmt(pattern=pattern, annotation=annotation, value=value)

    def parent(self) -> 'PyAssignStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyPassStmtDeriveKwargs(TypedDict, total=False):

    pass_keyword: 'PyPassKeyword | None'


class PyPassStmt(_PyBaseNode):

    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None) -> None:
        self.pass_keyword: PyPassKeyword = _coerce_union_2_token_pass_keyword_none_to_token_pass_keyword(pass_keyword)

    def derive(self, **kwargs: Unpack[PyPassStmtDeriveKwargs]) -> 'PyPassStmt':
        return PyPassStmt(pass_keyword=pass_keyword)

    def parent(self) -> 'PyPassStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyGlobalStmtDeriveKwargs(TypedDict, total=False):

    global_keyword: 'PyGlobalKeyword | None'

    names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]'


class PyGlobalStmt(_PyBaseNode):

    def count_names(self) -> int:
        return len(self.names)

    def __init__(self, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]', *, global_keyword: 'PyGlobalKeyword | None' = None) -> None:
        self.global_keyword: PyGlobalKeyword = _coerce_union_2_token_global_keyword_none_to_token_global_keyword(global_keyword)
        self.names: Punctuated[PyIdent, PyComma] = _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_required_list_union_2_token_ident_extern_string_required_punct_union_2_token_ident_extern_string_token_comma_required_to_punct_token_ident_token_comma_required(names)

    def derive(self, **kwargs: Unpack[PyGlobalStmtDeriveKwargs]) -> 'PyGlobalStmt':
        return PyGlobalStmt(global_keyword=global_keyword, names=names)

    def parent(self) -> 'PyGlobalStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyNonlocalStmtDeriveKwargs(TypedDict, total=False):

    nonlocal_keyword: 'PyNonlocalKeyword | None'

    names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]'


class PyNonlocalStmt(_PyBaseNode):

    def count_names(self) -> int:
        return len(self.names)

    def __init__(self, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]', *, nonlocal_keyword: 'PyNonlocalKeyword | None' = None) -> None:
        self.nonlocal_keyword: PyNonlocalKeyword = _coerce_union_2_token_nonlocal_keyword_none_to_token_nonlocal_keyword(nonlocal_keyword)
        self.names: Punctuated[PyIdent, PyComma] = _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_required_list_union_2_token_ident_extern_string_required_punct_union_2_token_ident_extern_string_token_comma_required_to_punct_token_ident_token_comma_required(names)

    def derive(self, **kwargs: Unpack[PyNonlocalStmtDeriveKwargs]) -> 'PyNonlocalStmt':
        return PyNonlocalStmt(nonlocal_keyword=nonlocal_keyword, names=names)

    def parent(self) -> 'PyNonlocalStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyIfCaseDeriveKwargs(TypedDict, total=False):

    if_keyword: 'PyIfKeyword | None'

    test: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyIfCase(_PyBaseNode):

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, if_keyword: 'PyIfKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.if_keyword: PyIfKeyword = _coerce_union_2_token_if_keyword_none_to_token_if_keyword(if_keyword)
        self.test: PyExpr = _coerce_variant_expr_to_variant_expr(test)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)

    def derive(self, **kwargs: Unpack[PyIfCaseDeriveKwargs]) -> 'PyIfCase':
        return PyIfCase(if_keyword=if_keyword, test=test, colon=colon, body=body)

    def parent(self) -> 'PyIfCaseParent':
        assert(self._parent is not None)
        return self._parent


class PyElifCaseDeriveKwargs(TypedDict, total=False):

    elif_keyword: 'PyElifKeyword | None'

    test: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyElifCase(_PyBaseNode):

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, elif_keyword: 'PyElifKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.elif_keyword: PyElifKeyword = _coerce_union_2_token_elif_keyword_none_to_token_elif_keyword(elif_keyword)
        self.test: PyExpr = _coerce_variant_expr_to_variant_expr(test)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)

    def derive(self, **kwargs: Unpack[PyElifCaseDeriveKwargs]) -> 'PyElifCase':
        return PyElifCase(elif_keyword=elif_keyword, test=test, colon=colon, body=body)

    def parent(self) -> 'PyElifCaseParent':
        assert(self._parent is not None)
        return self._parent


class PyElseCaseDeriveKwargs(TypedDict, total=False):

    else_keyword: 'PyElseKeyword | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyElseCase(_PyBaseNode):

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.else_keyword: PyElseKeyword = _coerce_union_2_token_else_keyword_none_to_token_else_keyword(else_keyword)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)

    def derive(self, **kwargs: Unpack[PyElseCaseDeriveKwargs]) -> 'PyElseCase':
        return PyElseCase(else_keyword=else_keyword, colon=colon, body=body)

    def parent(self) -> 'PyElseCaseParent':
        assert(self._parent is not None)
        return self._parent


class PyIfStmtDeriveKwargs(TypedDict, total=False):

    first: 'PyIfCase'

    alternatives: 'Sequence[PyElifCase] | None'

    last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None'


class PyIfStmt(_PyBaseNode):

    def count_alternatives(self) -> int:
        return len(self.alternatives)

    def __init__(self, first: 'PyIfCase', *, alternatives: 'Sequence[PyElifCase] | None' = None, last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None' = None) -> None:
        self.first: PyIfCase = _coerce_node_if_case_to_node_if_case(first)
        self.alternatives: Sequence[PyElifCase] = _coerce_union_2_list_node_elif_case_none_to_list_node_elif_case(alternatives)
        self.last: PyElseCase | None = _coerce_union_4_node_else_case_variant_stmt_list_variant_stmt_required_none_to_union_2_node_else_case_none(last)

    def derive(self, **kwargs: Unpack[PyIfStmtDeriveKwargs]) -> 'PyIfStmt':
        return PyIfStmt(first=first, alternatives=alternatives, last=last)

    def parent(self) -> 'PyIfStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyDeleteStmtDeriveKwargs(TypedDict, total=False):

    del_keyword: 'PyDelKeyword | None'

    pattern: 'PyPattern'


class PyDeleteStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', *, del_keyword: 'PyDelKeyword | None' = None) -> None:
        self.del_keyword: PyDelKeyword = _coerce_union_2_token_del_keyword_none_to_token_del_keyword(del_keyword)
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)

    def derive(self, **kwargs: Unpack[PyDeleteStmtDeriveKwargs]) -> 'PyDeleteStmt':
        return PyDeleteStmt(del_keyword=del_keyword, pattern=pattern)

    def parent(self) -> 'PyDeleteStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyRaiseStmtDeriveKwargs(TypedDict, total=False):

    raise_keyword: 'PyRaiseKeyword | None'

    expr: 'PyExpr'

    cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None'


class PyRaiseStmt(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, raise_keyword: 'PyRaiseKeyword | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None) -> None:
        self.raise_keyword: PyRaiseKeyword = _coerce_union_2_token_raise_keyword_none_to_token_raise_keyword(raise_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.cause: tuple[PyFromKeyword, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_from_keyword_none_variant_expr_none_to_union_2_tuple_2_token_from_keyword_variant_expr_none(cause)

    def derive(self, **kwargs: Unpack[PyRaiseStmtDeriveKwargs]) -> 'PyRaiseStmt':
        return PyRaiseStmt(raise_keyword=raise_keyword, expr=expr, cause=cause)

    def parent(self) -> 'PyRaiseStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyForStmtDeriveKwargs(TypedDict, total=False):

    for_keyword: 'PyForKeyword | None'

    pattern: 'PyPattern'

    in_keyword: 'PyInKeyword | None'

    expr: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'

    else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'


class PyForStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.for_keyword: PyForKeyword = _coerce_union_2_token_for_keyword_none_to_token_for_keyword(for_keyword)
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.in_keyword: PyInKeyword = _coerce_union_2_token_in_keyword_none_to_token_in_keyword(in_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_required_list_variant_stmt_required_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_required_none(else_clause)

    def derive(self, **kwargs: Unpack[PyForStmtDeriveKwargs]) -> 'PyForStmt':
        return PyForStmt(for_keyword=for_keyword, pattern=pattern, in_keyword=in_keyword, expr=expr, colon=colon, body=body, else_clause=else_clause)

    def parent(self) -> 'PyForStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyWhileStmtDeriveKwargs(TypedDict, total=False):

    while_keyword: 'PyWhileKeyword | None'

    expr: 'PyExpr'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'

    else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'


class PyWhileStmt(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, while_keyword: 'PyWhileKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.while_keyword: PyWhileKeyword = _coerce_union_2_token_while_keyword_none_to_token_while_keyword(while_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_required_list_variant_stmt_required_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_required_none(else_clause)

    def derive(self, **kwargs: Unpack[PyWhileStmtDeriveKwargs]) -> 'PyWhileStmt':
        return PyWhileStmt(while_keyword=while_keyword, expr=expr, colon=colon, body=body, else_clause=else_clause)

    def parent(self) -> 'PyWhileStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyBreakStmtDeriveKwargs(TypedDict, total=False):

    break_keyword: 'PyBreakKeyword | None'


class PyBreakStmt(_PyBaseNode):

    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None) -> None:
        self.break_keyword: PyBreakKeyword = _coerce_union_2_token_break_keyword_none_to_token_break_keyword(break_keyword)

    def derive(self, **kwargs: Unpack[PyBreakStmtDeriveKwargs]) -> 'PyBreakStmt':
        return PyBreakStmt(break_keyword=break_keyword)

    def parent(self) -> 'PyBreakStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyContinueStmtDeriveKwargs(TypedDict, total=False):

    continue_keyword: 'PyContinueKeyword | None'


class PyContinueStmt(_PyBaseNode):

    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None) -> None:
        self.continue_keyword: PyContinueKeyword = _coerce_union_2_token_continue_keyword_none_to_token_continue_keyword(continue_keyword)

    def derive(self, **kwargs: Unpack[PyContinueStmtDeriveKwargs]) -> 'PyContinueStmt':
        return PyContinueStmt(continue_keyword=continue_keyword)

    def parent(self) -> 'PyContinueStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyTypeAliasStmtDeriveKwargs(TypedDict, total=False):

    type_keyword: 'PyTypeKeyword | None'

    name: 'PyIdent | str'

    type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyTypeAliasStmt(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, type_keyword: 'PyTypeKeyword | None' = None, type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, equals: 'PyEquals | None' = None) -> None:
        self.type_keyword: PyTypeKeyword = _coerce_union_2_token_type_keyword_none_to_token_type_keyword(type_keyword)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = _coerce_union_5_tuple_3_union_2_token_open_bracket_none_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_union_2_token_close_bracket_none_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_union_2_tuple_3_token_open_bracket_punct_variant_expr_token_comma_token_close_bracket_none(type_params)
        self.equals: PyEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyTypeAliasStmtDeriveKwargs]) -> 'PyTypeAliasStmt':
        return PyTypeAliasStmt(type_keyword=type_keyword, name=name, type_params=type_params, equals=equals, expr=expr)

    def parent(self) -> 'PyTypeAliasStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyExceptHandlerDeriveKwargs(TypedDict, total=False):

    except_keyword: 'PyExceptKeyword | None'

    expr: 'PyExpr'

    binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyExceptHandler(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, except_keyword: 'PyExceptKeyword | None' = None, binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None, colon: 'PyColon | None' = None) -> None:
        self.except_keyword: PyExceptKeyword = _coerce_union_2_token_except_keyword_none_to_token_except_keyword(except_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.binder: tuple[PyAsKeyword, PyIdent] | None = _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(binder)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)

    def derive(self, **kwargs: Unpack[PyExceptHandlerDeriveKwargs]) -> 'PyExceptHandler':
        return PyExceptHandler(except_keyword=except_keyword, expr=expr, binder=binder, colon=colon, body=body)

    def parent(self) -> 'PyExceptHandlerParent':
        assert(self._parent is not None)
        return self._parent


class PyTryStmtDeriveKwargs(TypedDict, total=False):

    try_keyword: 'PyTryKeyword | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'

    handlers: 'Sequence[PyExceptHandler] | None'

    else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'

    finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None'


class PyTryStmt(_PyBaseNode):

    def count_handlers(self) -> int:
        return len(self.handlers)

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, handlers: 'Sequence[PyExceptHandler] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None, finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.try_keyword: PyTryKeyword = _coerce_union_2_token_try_keyword_none_to_token_try_keyword(try_keyword)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)
        self.handlers: Sequence[PyExceptHandler] = _coerce_union_2_list_node_except_handler_none_to_list_node_except_handler(handlers)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_required_list_variant_stmt_required_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_required_none(else_clause)
        self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_finally_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_required_list_variant_stmt_required_none_to_union_2_tuple_3_token_finally_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_required_none(finally_clause)

    def derive(self, **kwargs: Unpack[PyTryStmtDeriveKwargs]) -> 'PyTryStmt':
        return PyTryStmt(try_keyword=try_keyword, colon=colon, body=body, handlers=handlers, else_clause=else_clause, finally_clause=finally_clause)

    def parent(self) -> 'PyTryStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyClassBaseArgDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'


class PyClassBaseArg(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    def derive(self, **kwargs: Unpack[PyClassBaseArgDeriveKwargs]) -> 'PyClassBaseArg':
        return PyClassBaseArg(name=name)

    def parent(self) -> 'PyClassBaseArgParent':
        assert(self._parent is not None)
        return self._parent


class PyKeywordBaseArgDeriveKwargs(TypedDict, total=False):

    name: 'PyIdent | str'

    equals: 'PyEquals | None'

    expr: 'PyExpr'


class PyKeywordBaseArg(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.equals: PyEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyKeywordBaseArgDeriveKwargs]) -> 'PyKeywordBaseArg':
        return PyKeywordBaseArg(name=name, equals=equals, expr=expr)

    def parent(self) -> 'PyKeywordBaseArgParent':
        assert(self._parent is not None)
        return self._parent


class PyClassDefDeriveKwargs(TypedDict, total=False):

    decorators: 'Sequence[PyDecorator | PyExpr] | None'

    class_keyword: 'PyClassKeyword | None'

    name: 'PyIdent | str'

    bases: 'tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyClassDef(_PyBaseNode):

    def count_decorators(self) -> int:
        return len(self.decorators)

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, class_keyword: 'PyClassKeyword | None' = None, bases: 'tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None' = None, colon: 'PyColon | None' = None) -> None:
        self.decorators: Sequence[PyDecorator] = _coerce_union_2_list_union_2_node_decorator_variant_expr_none_to_list_node_decorator(decorators)
        self.class_keyword: PyClassKeyword = _coerce_union_2_token_class_keyword_none_to_token_class_keyword(class_keyword)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.bases: tuple[PyOpenParen, Punctuated[PyBaseArg, PyComma], PyCloseParen] | None = _coerce_union_5_tuple_3_union_2_token_open_paren_none_union_4_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_none_union_2_token_close_paren_none_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_none_to_union_2_tuple_3_token_open_paren_punct_variant_base_arg_token_comma_token_close_paren_none(bases)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)

    def derive(self, **kwargs: Unpack[PyClassDefDeriveKwargs]) -> 'PyClassDef':
        return PyClassDef(decorators=decorators, class_keyword=class_keyword, name=name, bases=bases, colon=colon, body=body)

    def parent(self) -> 'PyClassDefParent':
        assert(self._parent is not None)
        return self._parent


class PyNamedParamDeriveKwargs(TypedDict, total=False):

    pattern: 'PyPattern'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'

    default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None'


class PyNamedParam(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)
        self.default: tuple[PyEquals, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_equals_none_variant_expr_none_to_union_2_tuple_2_token_equals_variant_expr_none(default)

    def derive(self, **kwargs: Unpack[PyNamedParamDeriveKwargs]) -> 'PyNamedParam':
        return PyNamedParam(pattern=pattern, annotation=annotation, default=default)

    def parent(self) -> 'PyNamedParamParent':
        assert(self._parent is not None)
        return self._parent


class PyRestPosParamDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'

    name: 'PyIdent | str'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'


class PyRestPosParam(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', *, asterisk: 'PyAsterisk | None' = None, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)

    def derive(self, **kwargs: Unpack[PyRestPosParamDeriveKwargs]) -> 'PyRestPosParam':
        return PyRestPosParam(asterisk=asterisk, name=name, annotation=annotation)

    def parent(self) -> 'PyRestPosParamParent':
        assert(self._parent is not None)
        return self._parent


class PyRestKeywordParamDeriveKwargs(TypedDict, total=False):

    asterisk_asterisk: 'PyAsteriskAsterisk | None'

    name: 'PyIdent | str'

    annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None'


class PyRestKeywordParam(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.asterisk_asterisk: PyAsteriskAsterisk = _coerce_union_2_token_asterisk_asterisk_none_to_token_asterisk_asterisk(asterisk_asterisk)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)

    def derive(self, **kwargs: Unpack[PyRestKeywordParamDeriveKwargs]) -> 'PyRestKeywordParam':
        return PyRestKeywordParam(asterisk_asterisk=asterisk_asterisk, name=name, annotation=annotation)

    def parent(self) -> 'PyRestKeywordParamParent':
        assert(self._parent is not None)
        return self._parent


class PyPosSepParamDeriveKwargs(TypedDict, total=False):

    slash: 'PySlash | None'


class PyPosSepParam(_PyBaseNode):

    def __init__(self, *, slash: 'PySlash | None' = None) -> None:
        self.slash: PySlash = _coerce_union_2_token_slash_none_to_token_slash(slash)

    def derive(self, **kwargs: Unpack[PyPosSepParamDeriveKwargs]) -> 'PyPosSepParam':
        return PyPosSepParam(slash=slash)

    def parent(self) -> 'PyPosSepParamParent':
        assert(self._parent is not None)
        return self._parent


class PyKwSepParamDeriveKwargs(TypedDict, total=False):

    asterisk: 'PyAsterisk | None'


class PyKwSepParam(_PyBaseNode):

    def __init__(self, *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)

    def derive(self, **kwargs: Unpack[PyKwSepParamDeriveKwargs]) -> 'PyKwSepParam':
        return PyKwSepParam(asterisk=asterisk)

    def parent(self) -> 'PyKwSepParamParent':
        assert(self._parent is not None)
        return self._parent


class PyDecoratorDeriveKwargs(TypedDict, total=False):

    at_sign: 'PyAtSign | None'

    expr: 'PyExpr'


class PyDecorator(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, at_sign: 'PyAtSign | None' = None) -> None:
        self.at_sign: PyAtSign = _coerce_union_2_token_at_sign_none_to_token_at_sign(at_sign)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    def derive(self, **kwargs: Unpack[PyDecoratorDeriveKwargs]) -> 'PyDecorator':
        return PyDecorator(at_sign=at_sign, expr=expr)

    def parent(self) -> 'PyDecoratorParent':
        assert(self._parent is not None)
        return self._parent


class PyFuncDefDeriveKwargs(TypedDict, total=False):

    decorators: 'Sequence[PyDecorator | PyExpr] | None'

    async_keyword: 'PyAsyncKeyword | None'

    def_keyword: 'PyDefKeyword | None'

    name: 'PyIdent | str'

    open_paren: 'PyOpenParen | None'

    params: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | Punctuated[PyParam, PyComma] | None'

    close_paren: 'PyCloseParen | None'

    return_type: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None'

    colon: 'PyColon | None'

    body: 'PyStmt | Sequence[PyStmt]'


class PyFuncDef(_PyBaseNode):

    def count_decorators(self) -> int:
        return len(self.decorators)

    def count_params(self) -> int:
        return len(self.params)

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, open_paren: 'PyOpenParen | None' = None, params: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | Punctuated[PyParam, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None' = None, colon: 'PyColon | None' = None) -> None:
        self.decorators: Sequence[PyDecorator] = _coerce_union_2_list_union_2_node_decorator_variant_expr_none_to_list_node_decorator(decorators)
        self.async_keyword: PyAsyncKeyword | None = _coerce_union_2_token_async_keyword_none_to_union_2_token_async_keyword_none(async_keyword)
        self.def_keyword: PyDefKeyword = _coerce_union_2_token_def_keyword_none_to_token_def_keyword(def_keyword)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.params: Punctuated[PyParam, PyComma] = _coerce_union_4_list_variant_param_list_tuple_2_variant_param_union_2_token_comma_none_punct_variant_param_token_comma_none_to_punct_variant_param_token_comma(params)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)
        self.return_type: tuple[PyRArrow, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_r_arrow_none_variant_expr_none_to_union_2_tuple_2_token_r_arrow_variant_expr_none(return_type)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(body)

    def derive(self, **kwargs: Unpack[PyFuncDefDeriveKwargs]) -> 'PyFuncDef':
        return PyFuncDef(decorators=decorators, async_keyword=async_keyword, def_keyword=def_keyword, name=name, open_paren=open_paren, params=params, close_paren=close_paren, return_type=return_type, colon=colon, body=body)

    def parent(self) -> 'PyFuncDefParent':
        assert(self._parent is not None)
        return self._parent


class PyModuleDeriveKwargs(TypedDict, total=False):

    stmts: 'Sequence[PyStmt] | None'


class PyModule(_PyBaseNode):

    def count_stmts(self) -> int:
        return len(self.stmts)

    def __init__(self, *, stmts: 'Sequence[PyStmt] | None' = None) -> None:
        self.stmts: Sequence[PyStmt] = _coerce_union_2_list_variant_stmt_none_to_list_variant_stmt(stmts)

    def derive(self, **kwargs: Unpack[PyModuleDeriveKwargs]) -> 'PyModule':
        return PyModule(stmts=stmts)

    def parent(self) -> 'PyModuleParent':
        raise AssertionError('trying to access the parent node of a top-level node')


type PyPattern = PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern


def is_py_pattern(value: Any) -> TypeGuard[PyPattern]:
    return isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern)


type PyExpr = PyAttrExpr | PyCallExpr | PyConstExpr | PyEllipsisExpr | PyGeneratorExpr | PyIfExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr


def is_py_expr(value: Any) -> TypeGuard[PyExpr]:
    return isinstance(value, PyAttrExpr) or isinstance(value, PyCallExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyEllipsisExpr) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyIfExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyListExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyTupleExpr)


type PyArg = PyKeywordArg | PyExpr


def is_py_arg(value: Any) -> TypeGuard[PyArg]:
    return isinstance(value, PyKeywordArg) or is_py_expr(value)


type PyPrefixOp = PyNotKeyword | PyPlus | PyHyphen | PyTilde


def is_py_prefix_op(value: Any) -> TypeGuard[PyPrefixOp]:
    return isinstance(value, PyNotKeyword) or isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyTilde)


type PyInfixOp = PyPlus | PyHyphen | PyAsterisk | PySlash | PyAtSign | PySlashSlash | PyPercent | PyAsteriskAsterisk | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | tuple[PyIsKeyword, PyNotKeyword] | PyInKeyword | tuple[PyNotKeyword, PyInKeyword]


def is_py_infix_op(value: Any) -> TypeGuard[PyInfixOp]:
    return isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyAsterisk) or isinstance(value, PySlash) or isinstance(value, PyAtSign) or isinstance(value, PySlashSlash) or isinstance(value, PyPercent) or isinstance(value, PyAsteriskAsterisk) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyVerticalBar) or isinstance(value, PyCaret) or isinstance(value, PyAmpersand) or isinstance(value, PyOrKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyEqualsEquals) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyLessThan) or isinstance(value, PyLessThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyIsKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyIsKeyword) and isinstance(value[1], PyNotKeyword)) or isinstance(value, PyInKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyNotKeyword) and isinstance(value[1], PyInKeyword))


type PyPath = PyAbsolutePath | PyRelativePath


def is_py_path(value: Any) -> TypeGuard[PyPath]:
    return isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath)


type PyStmt = PyAssignStmt | PyAugAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyGlobalStmt | PyIfStmt | PyImportStmt | PyImportFromStmt | PyNonlocalStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt


def is_py_stmt(value: Any) -> TypeGuard[PyStmt]:
    return isinstance(value, PyAssignStmt) or isinstance(value, PyAugAssignStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyClassDef) or isinstance(value, PyContinueStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyForStmt) or isinstance(value, PyFuncDef) or isinstance(value, PyGlobalStmt) or isinstance(value, PyIfStmt) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyNonlocalStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyTryStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyWhileStmt)


type PyBaseArg = PyClassBaseArg | PyKeywordBaseArg


def is_py_base_arg(value: Any) -> TypeGuard[PyBaseArg]:
    return isinstance(value, PyClassBaseArg) or isinstance(value, PyKeywordBaseArg)


type PyParam = PyRestPosParam | PyRestKeywordParam | PyPosSepParam | PyKwSepParam | PyNamedParam


def is_py_param(value: Any) -> TypeGuard[PyParam]:
    return isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PyPosSepParam) or isinstance(value, PyKwSepParam) or isinstance(value, PyNamedParam)


type PyKeyword = PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyNonlocalKeyword | PyIsKeyword | PyInKeyword | PyImportKeyword | PyIfKeyword | PyGlobalKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword


def is_py_keyword(value: Any) -> TypeGuard[PyKeyword]:
    return isinstance(value, PyWhileKeyword) or isinstance(value, PyTypeKeyword) or isinstance(value, PyTryKeyword) or isinstance(value, PyReturnKeyword) or isinstance(value, PyRaiseKeyword) or isinstance(value, PyPassKeyword) or isinstance(value, PyOrKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyNonlocalKeyword) or isinstance(value, PyIsKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyImportKeyword) or isinstance(value, PyIfKeyword) or isinstance(value, PyGlobalKeyword) or isinstance(value, PyFromKeyword) or isinstance(value, PyForKeyword) or isinstance(value, PyFinallyKeyword) or isinstance(value, PyExceptKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyElifKeyword) or isinstance(value, PyDelKeyword) or isinstance(value, PyDefKeyword) or isinstance(value, PyContinueKeyword) or isinstance(value, PyClassKeyword) or isinstance(value, PyBreakKeyword) or isinstance(value, PyAsyncKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyAndKeyword)


type PyToken = str | str | PyIdent | PyFloat | PyInteger | PyString | PyTilde | PyVerticalBar | PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyNonlocalKeyword | PyIsKeyword | PyInKeyword | PyImportKeyword | PyIfKeyword | PyGlobalKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword | PyCaret | PyCloseBracket | PyOpenBracket | PyAtSign | PyGreaterThanGreaterThan | PyGreaterThanEquals | PyGreaterThan | PyEqualsEquals | PyEquals | PyLessThanEquals | PyLessThanLessThan | PyLessThan | PySemicolon | PyColon | PySlashSlash | PySlash | PyDotDotDot | PyDot | PyRArrow | PyHyphen | PyComma | PyPlus | PyAsteriskAsterisk | PyAsterisk | PyCloseParen | PyOpenParen | PyAmpersand | PyPercent | PyHashtag | PyExclamationMarkEquals | PyCarriageReturnLineFeed | PyLineFeed


def is_py_token(value: Any) -> TypeGuard[PyToken]:
    return isinstance(value, str) or isinstance(value, str) or isinstance(value, PyIdent) or isinstance(value, PyFloat) or isinstance(value, PyInteger) or isinstance(value, PyString) or isinstance(value, PyTilde) or isinstance(value, PyVerticalBar) or isinstance(value, PyWhileKeyword) or isinstance(value, PyTypeKeyword) or isinstance(value, PyTryKeyword) or isinstance(value, PyReturnKeyword) or isinstance(value, PyRaiseKeyword) or isinstance(value, PyPassKeyword) or isinstance(value, PyOrKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyNonlocalKeyword) or isinstance(value, PyIsKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyImportKeyword) or isinstance(value, PyIfKeyword) or isinstance(value, PyGlobalKeyword) or isinstance(value, PyFromKeyword) or isinstance(value, PyForKeyword) or isinstance(value, PyFinallyKeyword) or isinstance(value, PyExceptKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyElifKeyword) or isinstance(value, PyDelKeyword) or isinstance(value, PyDefKeyword) or isinstance(value, PyContinueKeyword) or isinstance(value, PyClassKeyword) or isinstance(value, PyBreakKeyword) or isinstance(value, PyAsyncKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyCaret) or isinstance(value, PyCloseBracket) or isinstance(value, PyOpenBracket) or isinstance(value, PyAtSign) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyEqualsEquals) or isinstance(value, PyEquals) or isinstance(value, PyLessThanEquals) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyLessThan) or isinstance(value, PySemicolon) or isinstance(value, PyColon) or isinstance(value, PySlashSlash) or isinstance(value, PySlash) or isinstance(value, PyDotDotDot) or isinstance(value, PyDot) or isinstance(value, PyRArrow) or isinstance(value, PyHyphen) or isinstance(value, PyComma) or isinstance(value, PyPlus) or isinstance(value, PyAsteriskAsterisk) or isinstance(value, PyAsterisk) or isinstance(value, PyCloseParen) or isinstance(value, PyOpenParen) or isinstance(value, PyAmpersand) or isinstance(value, PyPercent) or isinstance(value, PyHashtag) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyCarriageReturnLineFeed) or isinstance(value, PyLineFeed)


type PyNode = PySlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyEllipsisExpr | PyGuard | PyComprehension | PyGeneratorExpr | PyIfExpr | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleExpr | PyKeywordArg | PyCallExpr | PyPrefixExpr | PyInfixExpr | PyQualName | PyAbsolutePath | PyRelativePath | PyAlias | PyFromAlias | PyImportStmt | PyImportFromStmt | PyRetStmt | PyExprStmt | PyAugAssignStmt | PyAssignStmt | PyPassStmt | PyGlobalStmt | PyNonlocalStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassBaseArg | PyKeywordBaseArg | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PyPosSepParam | PyKwSepParam | PyDecorator | PyFuncDef | PyModule


def is_py_node(value: Any) -> TypeGuard[PyNode]:
    return isinstance(value, PySlice) or isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern) or isinstance(value, PyEllipsisExpr) or isinstance(value, PyGuard) or isinstance(value, PyComprehension) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyIfExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyAttrExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PyListExpr) or isinstance(value, PyTupleExpr) or isinstance(value, PyKeywordArg) or isinstance(value, PyCallExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyQualName) or isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath) or isinstance(value, PyAlias) or isinstance(value, PyFromAlias) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyAugAssignStmt) or isinstance(value, PyAssignStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyGlobalStmt) or isinstance(value, PyNonlocalStmt) or isinstance(value, PyIfCase) or isinstance(value, PyElifCase) or isinstance(value, PyElseCase) or isinstance(value, PyIfStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyForStmt) or isinstance(value, PyWhileStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyContinueStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyExceptHandler) or isinstance(value, PyTryStmt) or isinstance(value, PyClassBaseArg) or isinstance(value, PyKeywordBaseArg) or isinstance(value, PyClassDef) or isinstance(value, PyNamedParam) or isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PyPosSepParam) or isinstance(value, PyKwSepParam) or isinstance(value, PyDecorator) or isinstance(value, PyFuncDef) or isinstance(value, PyModule)


type PySyntax = PyNode | PyToken


def is_py_syntax(value: Any) -> TypeGuard[PySyntax]:
    return is_py_node(value) or is_py_token(value)


type PySliceParent = PySubscriptExpr | PySubscriptPattern


type PyNamedPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyAttrPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PySubscriptPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyStarredPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyListPatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyTuplePatternParent = PyAssignStmt | PyAttrPattern | PyAugAssignStmt | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyEllipsisExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyGuardParent = PyComprehension


type PyComprehensionParent = PyGeneratorExpr


type PyGeneratorExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyIfExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyConstExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyNestExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyNamedExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyAttrExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PySubscriptExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyStarredExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyListExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyTupleExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyKeywordArgParent = PyCallExpr


type PyCallExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyPrefixExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyInfixExprParent = PyAssignStmt | PyAttrExpr | PyAugAssignStmt | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyIfExpr | PyInfixExpr | PyKeywordArg | PyKeywordBaseArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRestKeywordParam | PyRestPosParam | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyQualNameParent = PyAbsolutePath | PyRelativePath


type PyAbsolutePathParent = PyAlias | PyImportFromStmt


type PyRelativePathParent = PyAlias | PyImportFromStmt


type PyAliasParent = PyImportStmt


type PyFromAliasParent = PyImportFromStmt


type PyImportStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyImportFromStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyRetStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyExprStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyAugAssignStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyAssignStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyPassStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyGlobalStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyNonlocalStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyIfCaseParent = PyIfStmt


type PyElifCaseParent = PyIfStmt


type PyElseCaseParent = PyIfStmt


type PyIfStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyDeleteStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyRaiseStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyForStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyWhileStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyBreakStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyContinueStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyTypeAliasStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyExceptHandlerParent = PyTryStmt


type PyTryStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyClassBaseArgParent = PyClassDef


type PyKeywordBaseArgParent = PyClassDef


type PyClassDefParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyNamedParamParent = PyFuncDef


type PyRestPosParamParent = PyFuncDef


type PyRestKeywordParamParent = PyFuncDef


type PyPosSepParamParent = PyFuncDef


type PyKwSepParamParent = PyFuncDef


type PyDecoratorParent = PyClassDef | PyFuncDef


type PyFuncDefParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyModuleParent = Never


@no_type_check
def _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(value: 'PyExpr | None') -> 'PyExpr | None':
    if is_py_expr(value):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | None to PyExpr | None failed')


@no_type_check
def _coerce_union_2_token_colon_none_to_token_colon(value: 'PyColon | None') -> 'PyColon':
    if value is None:
        return PyColon()
    elif isinstance(value, PyColon):
        return value
    else:
        raise ValueError('the coercion from PyColon | None to PyColon failed')


@no_type_check
def _coerce_variant_expr_to_variant_expr(value: 'PyExpr') -> 'PyExpr':
    return value


@no_type_check
def _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(value: 'PyExpr | tuple[PyColon | None, PyExpr] | None') -> 'tuple[PyColon, PyExpr] | None':
    if is_py_expr(value):
        return (PyColon(), _coerce_variant_expr_to_variant_expr(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_colon_none_to_token_colon(value[0]), _coerce_variant_expr_to_variant_expr(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyColon | None, PyExpr] | None to tuple[PyColon, PyExpr] | None failed')


@no_type_check
def _coerce_union_2_token_ident_extern_string_to_token_ident(value: 'PyIdent | str') -> 'PyIdent':
    if isinstance(value, str):
        return PyIdent(value)
    elif isinstance(value, PyIdent):
        return value
    else:
        raise ValueError('the coercion from PyIdent | str to PyIdent failed')


@no_type_check
def _coerce_variant_pattern_to_variant_pattern(value: 'PyPattern') -> 'PyPattern':
    return value


@no_type_check
def _coerce_union_2_token_dot_none_to_token_dot(value: 'PyDot | None') -> 'PyDot':
    if value is None:
        return PyDot()
    elif isinstance(value, PyDot):
        return value
    else:
        raise ValueError('the coercion from PyDot | None to PyDot failed')


@no_type_check
def _coerce_union_2_token_open_bracket_none_to_token_open_bracket(value: 'PyOpenBracket | None') -> 'PyOpenBracket':
    if value is None:
        return PyOpenBracket()
    elif isinstance(value, PyOpenBracket):
        return value
    else:
        raise ValueError('the coercion from PyOpenBracket | None to PyOpenBracket failed')


@no_type_check
def _coerce_union_2_node_slice_variant_pattern_to_union_2_node_slice_variant_pattern(value: 'PySlice | PyPattern') -> 'PySlice | PyPattern':
    if isinstance(value, PySlice):
        return value
    elif is_py_pattern(value):
        return value
    else:
        raise ValueError('the coercion from PySlice | PyPattern to PySlice | PyPattern failed')


@no_type_check
def _coerce_token_comma_to_token_comma(value: 'PyComma') -> 'PyComma':
    return value


@no_type_check
def _coerce_union_3_list_tuple_2_union_2_node_slice_variant_pattern_union_2_token_comma_none_required_list_union_2_node_slice_variant_pattern_required_punct_union_2_node_slice_variant_pattern_token_comma_required_to_punct_union_2_node_slice_variant_pattern_token_comma_required(value: 'Sequence[tuple[PySlice | PyPattern, PyComma | None]] | Sequence[PySlice | PyPattern] | Punctuated[PySlice | PyPattern, PyComma]') -> 'Punctuated[PySlice | PyPattern, PyComma]':
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
                new_element_value = _coerce_union_2_node_slice_variant_pattern_to_union_2_node_slice_variant_pattern(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_2_node_slice_variant_pattern_to_union_2_node_slice_variant_pattern(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_2_token_close_bracket_none_to_token_close_bracket(value: 'PyCloseBracket | None') -> 'PyCloseBracket':
    if value is None:
        return PyCloseBracket()
    elif isinstance(value, PyCloseBracket):
        return value
    else:
        raise ValueError('the coercion from PyCloseBracket | None to PyCloseBracket failed')


@no_type_check
def _coerce_union_2_token_asterisk_none_to_token_asterisk(value: 'PyAsterisk | None') -> 'PyAsterisk':
    if value is None:
        return PyAsterisk()
    elif isinstance(value, PyAsterisk):
        return value
    else:
        raise ValueError('the coercion from PyAsterisk | None to PyAsterisk failed')


@no_type_check
def _coerce_union_4_list_variant_pattern_list_tuple_2_variant_pattern_union_2_token_comma_none_punct_variant_pattern_token_comma_none_to_punct_variant_pattern_token_comma(value: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None') -> 'Punctuated[PyPattern, PyComma]':
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
                    new_element_value = _coerce_variant_pattern_to_variant_pattern(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_pattern_to_variant_pattern(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None to Punctuated[PyPattern, PyComma] failed')


@no_type_check
def _coerce_union_2_token_open_paren_none_to_token_open_paren(value: 'PyOpenParen | None') -> 'PyOpenParen':
    if value is None:
        return PyOpenParen()
    elif isinstance(value, PyOpenParen):
        return value
    else:
        raise ValueError('the coercion from PyOpenParen | None to PyOpenParen failed')


@no_type_check
def _coerce_union_2_token_close_paren_none_to_token_close_paren(value: 'PyCloseParen | None') -> 'PyCloseParen':
    if value is None:
        return PyCloseParen()
    elif isinstance(value, PyCloseParen):
        return value
    else:
        raise ValueError('the coercion from PyCloseParen | None to PyCloseParen failed')


@no_type_check
def _coerce_union_2_token_dot_dot_dot_none_to_token_dot_dot_dot(value: 'PyDotDotDot | None') -> 'PyDotDotDot':
    if value is None:
        return PyDotDotDot()
    elif isinstance(value, PyDotDotDot):
        return value
    else:
        raise ValueError('the coercion from PyDotDotDot | None to PyDotDotDot failed')


@no_type_check
def _coerce_union_2_token_if_keyword_none_to_token_if_keyword(value: 'PyIfKeyword | None') -> 'PyIfKeyword':
    if value is None:
        return PyIfKeyword()
    elif isinstance(value, PyIfKeyword):
        return value
    else:
        raise ValueError('the coercion from PyIfKeyword | None to PyIfKeyword failed')


@no_type_check
def _coerce_union_2_token_async_keyword_none_to_union_2_token_async_keyword_none(value: 'PyAsyncKeyword | None') -> 'PyAsyncKeyword | None':
    if isinstance(value, PyAsyncKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyAsyncKeyword | None to PyAsyncKeyword | None failed')


@no_type_check
def _coerce_union_2_token_for_keyword_none_to_token_for_keyword(value: 'PyForKeyword | None') -> 'PyForKeyword':
    if value is None:
        return PyForKeyword()
    elif isinstance(value, PyForKeyword):
        return value
    else:
        raise ValueError('the coercion from PyForKeyword | None to PyForKeyword failed')


@no_type_check
def _coerce_union_2_token_in_keyword_none_to_token_in_keyword(value: 'PyInKeyword | None') -> 'PyInKeyword':
    if value is None:
        return PyInKeyword()
    elif isinstance(value, PyInKeyword):
        return value
    else:
        raise ValueError('the coercion from PyInKeyword | None to PyInKeyword failed')


@no_type_check
def _coerce_union_2_node_guard_variant_expr_to_node_guard(value: 'PyGuard | PyExpr') -> 'PyGuard':
    if is_py_expr(value):
        return PyGuard(_coerce_variant_expr_to_variant_expr(value))
    elif isinstance(value, PyGuard):
        return value
    else:
        raise ValueError('the coercion from PyGuard | PyExpr to PyGuard failed')


@no_type_check
def _coerce_union_2_list_union_2_node_guard_variant_expr_none_to_list_node_guard(value: 'Sequence[PyGuard | PyExpr] | None') -> 'Sequence[PyGuard]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_2_node_guard_variant_expr_to_node_guard(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyGuard | PyExpr] | None to Sequence[PyGuard] failed')


@no_type_check
def _coerce_node_comprehension_to_node_comprehension(value: 'PyComprehension') -> 'PyComprehension':
    return value


@no_type_check
def _coerce_list_node_comprehension_required_to_list_node_comprehension_required(value: 'Sequence[PyComprehension]') -> 'Sequence[PyComprehension]':
    new_elements = list()
    for value_element in value:
        new_elements.append(_coerce_node_comprehension_to_node_comprehension(value_element))
    return new_elements


@no_type_check
def _coerce_union_2_token_else_keyword_none_to_token_else_keyword(value: 'PyElseKeyword | None') -> 'PyElseKeyword':
    if value is None:
        return PyElseKeyword()
    elif isinstance(value, PyElseKeyword):
        return value
    else:
        raise ValueError('the coercion from PyElseKeyword | None to PyElseKeyword failed')


@no_type_check
def _coerce_union_6_token_float_token_integer_token_string_extern_float_extern_integer_extern_string_to_union_3_token_float_token_integer_token_string(value: 'PyFloat | PyInteger | PyString | float | int | str') -> 'PyFloat | PyInteger | PyString':
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
def _coerce_union_2_node_slice_variant_expr_to_union_2_node_slice_variant_expr(value: 'PySlice | PyExpr') -> 'PySlice | PyExpr':
    if isinstance(value, PySlice):
        return value
    elif is_py_expr(value):
        return value
    else:
        raise ValueError('the coercion from PySlice | PyExpr to PySlice | PyExpr failed')


@no_type_check
def _coerce_union_3_list_tuple_2_union_2_node_slice_variant_expr_union_2_token_comma_none_required_list_union_2_node_slice_variant_expr_required_punct_union_2_node_slice_variant_expr_token_comma_required_to_punct_union_2_node_slice_variant_expr_token_comma_required(value: 'Sequence[tuple[PySlice | PyExpr, PyComma | None]] | Sequence[PySlice | PyExpr] | Punctuated[PySlice | PyExpr, PyComma]') -> 'Punctuated[PySlice | PyExpr, PyComma]':
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
                new_element_value = _coerce_union_2_node_slice_variant_expr_to_union_2_node_slice_variant_expr(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_2_node_slice_variant_expr_to_union_2_node_slice_variant_expr(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(value: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None') -> 'Punctuated[PyExpr, PyComma]':
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
                    new_element_value = _coerce_variant_expr_to_variant_expr(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_expr_to_variant_expr(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None to Punctuated[PyExpr, PyComma] failed')


@no_type_check
def _coerce_union_2_token_equals_none_to_token_equals(value: 'PyEquals | None') -> 'PyEquals':
    if value is None:
        return PyEquals()
    elif isinstance(value, PyEquals):
        return value
    else:
        raise ValueError('the coercion from PyEquals | None to PyEquals failed')


@no_type_check
def _coerce_variant_arg_to_variant_arg(value: 'PyArg') -> 'PyArg':
    return value


@no_type_check
def _coerce_union_4_list_variant_arg_list_tuple_2_variant_arg_union_2_token_comma_none_punct_variant_arg_token_comma_none_to_punct_variant_arg_token_comma(value: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma] | None') -> 'Punctuated[PyArg, PyComma]':
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
                    new_element_value = _coerce_variant_arg_to_variant_arg(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_arg_to_variant_arg(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma] | None to Punctuated[PyArg, PyComma] failed')


@no_type_check
def _coerce_variant_prefix_op_to_variant_prefix_op(value: 'PyPrefixOp') -> 'PyPrefixOp':
    return value


@no_type_check
def _coerce_variant_infix_op_to_variant_infix_op(value: 'PyInfixOp') -> 'PyInfixOp':
    return value


@no_type_check
def _coerce_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_dot_none_extern_string_to_tuple_2_token_ident_token_dot(value: 'PyIdent | tuple[PyIdent | str, PyDot | None] | str') -> 'tuple[PyIdent, PyDot]':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return (_coerce_union_2_token_ident_extern_string_to_token_ident(value), PyDot())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_ident_extern_string_to_token_ident(value[0]), _coerce_union_2_token_dot_none_to_token_dot(value[1]))
    else:
        raise ValueError('the coercion from PyIdent | tuple[PyIdent | str, PyDot | None] | str to tuple[PyIdent, PyDot] failed')


@no_type_check
def _coerce_union_2_list_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_dot_none_extern_string_none_to_list_tuple_2_token_ident_token_dot(value: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None') -> 'Sequence[tuple[PyIdent, PyDot]]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_dot_none_extern_string_to_tuple_2_token_ident_token_dot(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None to Sequence[tuple[PyIdent, PyDot]] failed')


@no_type_check
def _coerce_union_3_node_qual_name_token_ident_extern_string_to_node_qual_name(value: 'PyQualName | PyIdent | str') -> 'PyQualName':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return PyQualName(_coerce_union_2_token_ident_extern_string_to_token_ident(value))
    elif isinstance(value, PyQualName):
        return value
    else:
        raise ValueError('the coercion from PyQualName | PyIdent | str to PyQualName failed')


@no_type_check
def _coerce_token_dot_to_token_dot(value: 'PyDot') -> 'PyDot':
    return value


@no_type_check
def _coerce_union_2_list_token_dot_required_extern_integer_to_list_token_dot_required(value: 'Sequence[PyDot] | int') -> 'Sequence[PyDot]':
    if isinstance(value, int):
        new_elements = list()
        for _ in range(0, value):
            new_elements.append(PyDot())
        return new_elements
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_token_dot_to_token_dot(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyDot] | int to Sequence[PyDot] failed')


@no_type_check
def _coerce_union_4_node_qual_name_token_ident_none_extern_string_to_union_2_node_qual_name_none(value: 'PyQualName | PyIdent | None | str') -> 'PyQualName | None':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return PyQualName(_coerce_union_2_token_ident_extern_string_to_token_ident(value))
    elif isinstance(value, PyQualName):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyQualName | PyIdent | None | str to PyQualName | None failed')


@no_type_check
def _coerce_variant_path_to_variant_path(value: 'PyPath') -> 'PyPath':
    return value


@no_type_check
def _coerce_union_2_token_as_keyword_none_to_token_as_keyword(value: 'PyAsKeyword | None') -> 'PyAsKeyword':
    if value is None:
        return PyAsKeyword()
    elif isinstance(value, PyAsKeyword):
        return value
    else:
        raise ValueError('the coercion from PyAsKeyword | None to PyAsKeyword failed')


@no_type_check
def _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(value: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str') -> 'tuple[PyAsKeyword, PyIdent] | None':
    if isinstance(value, PyIdent) or isinstance(value, str):
        return (PyAsKeyword(), _coerce_union_2_token_ident_extern_string_to_token_ident(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_as_keyword_none_to_token_as_keyword(value[0]), _coerce_union_2_token_ident_extern_string_to_token_ident(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str to tuple[PyAsKeyword, PyIdent] | None failed')


@no_type_check
def _coerce_union_3_token_asterisk_token_ident_extern_string_to_union_2_token_asterisk_token_ident(value: 'PyAsterisk | PyIdent | str') -> 'PyAsterisk | PyIdent':
    if isinstance(value, PyAsterisk):
        return value
    elif isinstance(value, str):
        return PyIdent(value)
    elif isinstance(value, PyIdent):
        return value
    else:
        raise ValueError('the coercion from PyAsterisk | PyIdent | str to PyAsterisk | PyIdent failed')


@no_type_check
def _coerce_union_2_token_import_keyword_none_to_token_import_keyword(value: 'PyImportKeyword | None') -> 'PyImportKeyword':
    if value is None:
        return PyImportKeyword()
    elif isinstance(value, PyImportKeyword):
        return value
    else:
        raise ValueError('the coercion from PyImportKeyword | None to PyImportKeyword failed')


@no_type_check
def _coerce_union_2_node_alias_variant_path_to_node_alias(value: 'PyAlias | PyPath') -> 'PyAlias':
    if is_py_path(value):
        return PyAlias(_coerce_variant_path_to_variant_path(value))
    elif isinstance(value, PyAlias):
        return value
    else:
        raise ValueError('the coercion from PyAlias | PyPath to PyAlias failed')


@no_type_check
def _coerce_union_3_list_tuple_2_union_2_node_alias_variant_path_union_2_token_comma_none_required_list_union_2_node_alias_variant_path_required_punct_union_2_node_alias_variant_path_token_comma_required_to_punct_node_alias_token_comma_required(value: 'Sequence[tuple[PyAlias | PyPath, PyComma | None]] | Sequence[PyAlias | PyPath] | Punctuated[PyAlias | PyPath, PyComma]') -> 'Punctuated[PyAlias, PyComma]':
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
                new_element_value = _coerce_union_2_node_alias_variant_path_to_node_alias(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_2_node_alias_variant_path_to_node_alias(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_2_token_from_keyword_none_to_token_from_keyword(value: 'PyFromKeyword | None') -> 'PyFromKeyword':
    if value is None:
        return PyFromKeyword()
    elif isinstance(value, PyFromKeyword):
        return value
    else:
        raise ValueError('the coercion from PyFromKeyword | None to PyFromKeyword failed')


@no_type_check
def _coerce_union_4_node_from_alias_token_asterisk_token_ident_extern_string_to_node_from_alias(value: 'PyFromAlias | PyAsterisk | PyIdent | str') -> 'PyFromAlias':
    if isinstance(value, PyAsterisk) or isinstance(value, PyIdent) or isinstance(value, str):
        return PyFromAlias(_coerce_union_3_token_asterisk_token_ident_extern_string_to_union_2_token_asterisk_token_ident(value))
    elif isinstance(value, PyFromAlias):
        return value
    else:
        raise ValueError('the coercion from PyFromAlias | PyAsterisk | PyIdent | str to PyFromAlias failed')


@no_type_check
def _coerce_union_3_list_tuple_2_union_4_node_from_alias_token_asterisk_token_ident_extern_string_union_2_token_comma_none_required_list_union_4_node_from_alias_token_asterisk_token_ident_extern_string_required_punct_union_4_node_from_alias_token_asterisk_token_ident_extern_string_token_comma_required_to_punct_node_from_alias_token_comma_required(value: 'Sequence[tuple[PyFromAlias | PyAsterisk | PyIdent | str, PyComma | None]] | Sequence[PyFromAlias | PyAsterisk | PyIdent | str] | Punctuated[PyFromAlias | PyAsterisk | PyIdent | str, PyComma]') -> 'Punctuated[PyFromAlias, PyComma]':
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
                new_element_value = _coerce_union_4_node_from_alias_token_asterisk_token_ident_extern_string_to_node_from_alias(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_4_node_from_alias_token_asterisk_token_ident_extern_string_to_node_from_alias(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_2_token_return_keyword_none_to_token_return_keyword(value: 'PyReturnKeyword | None') -> 'PyReturnKeyword':
    if value is None:
        return PyReturnKeyword()
    elif isinstance(value, PyReturnKeyword):
        return value
    else:
        raise ValueError('the coercion from PyReturnKeyword | None to PyReturnKeyword failed')


@no_type_check
def _coerce_union_13_token_ampersand_token_asterisk_token_asterisk_asterisk_token_at_sign_token_caret_token_greater_than_greater_than_token_hyphen_token_less_than_less_than_token_percent_token_plus_token_slash_token_slash_slash_token_vertical_bar_to_union_13_token_ampersand_token_asterisk_token_asterisk_asterisk_token_at_sign_token_caret_token_greater_than_greater_than_token_hyphen_token_less_than_less_than_token_percent_token_plus_token_slash_token_slash_slash_token_vertical_bar(value: 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar') -> 'PyAmpersand | PyAsterisk | PyAsteriskAsterisk | PyAtSign | PyCaret | PyGreaterThanGreaterThan | PyHyphen | PyLessThanLessThan | PyPercent | PyPlus | PySlash | PySlashSlash | PyVerticalBar':
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
def _coerce_union_3_variant_expr_tuple_2_union_2_token_equals_none_variant_expr_none_to_union_2_tuple_2_token_equals_variant_expr_none(value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None') -> 'tuple[PyEquals, PyExpr] | None':
    if is_py_expr(value):
        return (PyEquals(), _coerce_variant_expr_to_variant_expr(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_equals_none_to_token_equals(value[0]), _coerce_variant_expr_to_variant_expr(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyEquals | None, PyExpr] | None to tuple[PyEquals, PyExpr] | None failed')


@no_type_check
def _coerce_union_2_token_pass_keyword_none_to_token_pass_keyword(value: 'PyPassKeyword | None') -> 'PyPassKeyword':
    if value is None:
        return PyPassKeyword()
    elif isinstance(value, PyPassKeyword):
        return value
    else:
        raise ValueError('the coercion from PyPassKeyword | None to PyPassKeyword failed')


@no_type_check
def _coerce_union_2_token_global_keyword_none_to_token_global_keyword(value: 'PyGlobalKeyword | None') -> 'PyGlobalKeyword':
    if value is None:
        return PyGlobalKeyword()
    elif isinstance(value, PyGlobalKeyword):
        return value
    else:
        raise ValueError('the coercion from PyGlobalKeyword | None to PyGlobalKeyword failed')


@no_type_check
def _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_required_list_union_2_token_ident_extern_string_required_punct_union_2_token_ident_extern_string_token_comma_required_to_punct_token_ident_token_comma_required(value: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]') -> 'Punctuated[PyIdent, PyComma]':
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
                new_element_value = _coerce_union_2_token_ident_extern_string_to_token_ident(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_2_token_ident_extern_string_to_token_ident(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_2_token_nonlocal_keyword_none_to_token_nonlocal_keyword(value: 'PyNonlocalKeyword | None') -> 'PyNonlocalKeyword':
    if value is None:
        return PyNonlocalKeyword()
    elif isinstance(value, PyNonlocalKeyword):
        return value
    else:
        raise ValueError('the coercion from PyNonlocalKeyword | None to PyNonlocalKeyword failed')


@no_type_check
def _coerce_variant_stmt_to_variant_stmt(value: 'PyStmt') -> 'PyStmt':
    return value


@no_type_check
def _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(value: 'PyStmt | Sequence[PyStmt]') -> 'PyStmt | Sequence[PyStmt]':
    if is_py_stmt(value):
        return value
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_variant_stmt_to_variant_stmt(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from PyStmt | Sequence[PyStmt] to PyStmt | Sequence[PyStmt] failed')


@no_type_check
def _coerce_union_2_token_elif_keyword_none_to_token_elif_keyword(value: 'PyElifKeyword | None') -> 'PyElifKeyword':
    if value is None:
        return PyElifKeyword()
    elif isinstance(value, PyElifKeyword):
        return value
    else:
        raise ValueError('the coercion from PyElifKeyword | None to PyElifKeyword failed')


@no_type_check
def _coerce_node_if_case_to_node_if_case(value: 'PyIfCase') -> 'PyIfCase':
    return value


@no_type_check
def _coerce_node_elif_case_to_node_elif_case(value: 'PyElifCase') -> 'PyElifCase':
    return value


@no_type_check
def _coerce_union_2_list_node_elif_case_none_to_list_node_elif_case(value: 'Sequence[PyElifCase] | None') -> 'Sequence[PyElifCase]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_node_elif_case_to_node_elif_case(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyElifCase] | None to Sequence[PyElifCase] failed')


@no_type_check
def _coerce_union_4_node_else_case_variant_stmt_list_variant_stmt_required_none_to_union_2_node_else_case_none(value: 'PyElseCase | PyStmt | Sequence[PyStmt] | None') -> 'PyElseCase | None':
    if is_py_stmt(value) or isinstance(value, list):
        return PyElseCase(_coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(value))
    elif isinstance(value, PyElseCase):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyElseCase | PyStmt | Sequence[PyStmt] | None to PyElseCase | None failed')


@no_type_check
def _coerce_union_2_token_del_keyword_none_to_token_del_keyword(value: 'PyDelKeyword | None') -> 'PyDelKeyword':
    if value is None:
        return PyDelKeyword()
    elif isinstance(value, PyDelKeyword):
        return value
    else:
        raise ValueError('the coercion from PyDelKeyword | None to PyDelKeyword failed')


@no_type_check
def _coerce_union_2_token_raise_keyword_none_to_token_raise_keyword(value: 'PyRaiseKeyword | None') -> 'PyRaiseKeyword':
    if value is None:
        return PyRaiseKeyword()
    elif isinstance(value, PyRaiseKeyword):
        return value
    else:
        raise ValueError('the coercion from PyRaiseKeyword | None to PyRaiseKeyword failed')


@no_type_check
def _coerce_union_3_variant_expr_tuple_2_union_2_token_from_keyword_none_variant_expr_none_to_union_2_tuple_2_token_from_keyword_variant_expr_none(value: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None') -> 'tuple[PyFromKeyword, PyExpr] | None':
    if is_py_expr(value):
        return (PyFromKeyword(), _coerce_variant_expr_to_variant_expr(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_from_keyword_none_to_token_from_keyword(value[0]), _coerce_variant_expr_to_variant_expr(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyFromKeyword | None, PyExpr] | None to tuple[PyFromKeyword, PyExpr] | None failed')


@no_type_check
def _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_required_list_variant_stmt_required_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_required_none(value: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None') -> 'tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None':
    if is_py_stmt(value) or isinstance(value, list):
        return (PyElseKeyword(), PyColon(), _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_else_keyword_none_to_token_else_keyword(value[0]), _coerce_union_2_token_colon_none_to_token_colon(value[1]), _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None to tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None failed')


@no_type_check
def _coerce_union_2_token_while_keyword_none_to_token_while_keyword(value: 'PyWhileKeyword | None') -> 'PyWhileKeyword':
    if value is None:
        return PyWhileKeyword()
    elif isinstance(value, PyWhileKeyword):
        return value
    else:
        raise ValueError('the coercion from PyWhileKeyword | None to PyWhileKeyword failed')


@no_type_check
def _coerce_union_2_token_break_keyword_none_to_token_break_keyword(value: 'PyBreakKeyword | None') -> 'PyBreakKeyword':
    if value is None:
        return PyBreakKeyword()
    elif isinstance(value, PyBreakKeyword):
        return value
    else:
        raise ValueError('the coercion from PyBreakKeyword | None to PyBreakKeyword failed')


@no_type_check
def _coerce_union_2_token_continue_keyword_none_to_token_continue_keyword(value: 'PyContinueKeyword | None') -> 'PyContinueKeyword':
    if value is None:
        return PyContinueKeyword()
    elif isinstance(value, PyContinueKeyword):
        return value
    else:
        raise ValueError('the coercion from PyContinueKeyword | None to PyContinueKeyword failed')


@no_type_check
def _coerce_union_2_token_type_keyword_none_to_token_type_keyword(value: 'PyTypeKeyword | None') -> 'PyTypeKeyword':
    if value is None:
        return PyTypeKeyword()
    elif isinstance(value, PyTypeKeyword):
        return value
    else:
        raise ValueError('the coercion from PyTypeKeyword | None to PyTypeKeyword failed')


@no_type_check
def _coerce_union_3_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_to_punct_variant_expr_token_comma(value: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma]') -> 'Punctuated[PyExpr, PyComma]':
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
                new_element_value = _coerce_variant_expr_to_variant_expr(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_variant_expr_to_variant_expr(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_5_tuple_3_union_2_token_open_bracket_none_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_union_2_token_close_bracket_none_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_union_2_tuple_3_token_open_bracket_punct_variant_expr_token_comma_token_close_bracket_none(value: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None') -> 'tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (PyOpenBracket(), _coerce_union_3_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_to_punct_variant_expr_token_comma(value), PyCloseBracket())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_open_bracket_none_to_token_open_bracket(value[0]), _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(value[1]), _coerce_union_2_token_close_bracket_none_to_token_close_bracket(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None to tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None failed')


@no_type_check
def _coerce_union_2_token_except_keyword_none_to_token_except_keyword(value: 'PyExceptKeyword | None') -> 'PyExceptKeyword':
    if value is None:
        return PyExceptKeyword()
    elif isinstance(value, PyExceptKeyword):
        return value
    else:
        raise ValueError('the coercion from PyExceptKeyword | None to PyExceptKeyword failed')


@no_type_check
def _coerce_union_2_token_try_keyword_none_to_token_try_keyword(value: 'PyTryKeyword | None') -> 'PyTryKeyword':
    if value is None:
        return PyTryKeyword()
    elif isinstance(value, PyTryKeyword):
        return value
    else:
        raise ValueError('the coercion from PyTryKeyword | None to PyTryKeyword failed')


@no_type_check
def _coerce_node_except_handler_to_node_except_handler(value: 'PyExceptHandler') -> 'PyExceptHandler':
    return value


@no_type_check
def _coerce_union_2_list_node_except_handler_none_to_list_node_except_handler(value: 'Sequence[PyExceptHandler] | None') -> 'Sequence[PyExceptHandler]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_node_except_handler_to_node_except_handler(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyExceptHandler] | None to Sequence[PyExceptHandler] failed')


@no_type_check
def _coerce_union_2_token_finally_keyword_none_to_token_finally_keyword(value: 'PyFinallyKeyword | None') -> 'PyFinallyKeyword':
    if value is None:
        return PyFinallyKeyword()
    elif isinstance(value, PyFinallyKeyword):
        return value
    else:
        raise ValueError('the coercion from PyFinallyKeyword | None to PyFinallyKeyword failed')


@no_type_check
def _coerce_union_4_variant_stmt_tuple_3_union_2_token_finally_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_required_list_variant_stmt_required_none_to_union_2_tuple_3_token_finally_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_required_none(value: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None') -> 'tuple[PyFinallyKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None':
    if is_py_stmt(value) or isinstance(value, list):
        return (PyFinallyKeyword(), PyColon(), _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_finally_keyword_none_to_token_finally_keyword(value[0]), _coerce_union_2_token_colon_none_to_token_colon(value[1]), _coerce_union_2_variant_stmt_list_variant_stmt_required_to_union_2_variant_stmt_list_variant_stmt_required(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None to tuple[PyFinallyKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None failed')


@no_type_check
def _coerce_union_2_node_decorator_variant_expr_to_node_decorator(value: 'PyDecorator | PyExpr') -> 'PyDecorator':
    if is_py_expr(value):
        return PyDecorator(_coerce_variant_expr_to_variant_expr(value))
    elif isinstance(value, PyDecorator):
        return value
    else:
        raise ValueError('the coercion from PyDecorator | PyExpr to PyDecorator failed')


@no_type_check
def _coerce_union_2_list_union_2_node_decorator_variant_expr_none_to_list_node_decorator(value: 'Sequence[PyDecorator | PyExpr] | None') -> 'Sequence[PyDecorator]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_2_node_decorator_variant_expr_to_node_decorator(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyDecorator | PyExpr] | None to Sequence[PyDecorator] failed')


@no_type_check
def _coerce_union_2_token_class_keyword_none_to_token_class_keyword(value: 'PyClassKeyword | None') -> 'PyClassKeyword':
    if value is None:
        return PyClassKeyword()
    elif isinstance(value, PyClassKeyword):
        return value
    else:
        raise ValueError('the coercion from PyClassKeyword | None to PyClassKeyword failed')


@no_type_check
def _coerce_variant_base_arg_to_variant_base_arg(value: 'PyBaseArg') -> 'PyBaseArg':
    return value


@no_type_check
def _coerce_union_3_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_to_punct_variant_base_arg_token_comma(value: 'Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma]') -> 'Punctuated[PyBaseArg, PyComma]':
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
                new_element_value = _coerce_variant_base_arg_to_variant_base_arg(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_variant_base_arg_to_variant_base_arg(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_4_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_none_to_punct_variant_base_arg_token_comma(value: 'Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None') -> 'Punctuated[PyBaseArg, PyComma]':
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
                    new_element_value = _coerce_variant_base_arg_to_variant_base_arg(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_base_arg_to_variant_base_arg(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None to Punctuated[PyBaseArg, PyComma] failed')


@no_type_check
def _coerce_union_5_tuple_3_union_2_token_open_paren_none_union_4_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_none_union_2_token_close_paren_none_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_none_to_union_2_tuple_3_token_open_paren_punct_variant_base_arg_token_comma_token_close_paren_none(value: 'tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None') -> 'tuple[PyOpenParen, Punctuated[PyBaseArg, PyComma], PyCloseParen] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (PyOpenParen(), _coerce_union_3_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_to_punct_variant_base_arg_token_comma(value), PyCloseParen())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_open_paren_none_to_token_open_paren(value[0]), _coerce_union_4_list_variant_base_arg_list_tuple_2_variant_base_arg_union_2_token_comma_none_punct_variant_base_arg_token_comma_none_to_punct_variant_base_arg_token_comma(value[1]), _coerce_union_2_token_close_paren_none_to_token_close_paren(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[PyOpenParen | None, Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None, PyCloseParen | None] | Sequence[PyBaseArg] | Sequence[tuple[PyBaseArg, PyComma | None]] | Punctuated[PyBaseArg, PyComma] | None to tuple[PyOpenParen, Punctuated[PyBaseArg, PyComma], PyCloseParen] | None failed')


@no_type_check
def _coerce_union_2_token_asterisk_asterisk_none_to_token_asterisk_asterisk(value: 'PyAsteriskAsterisk | None') -> 'PyAsteriskAsterisk':
    if value is None:
        return PyAsteriskAsterisk()
    elif isinstance(value, PyAsteriskAsterisk):
        return value
    else:
        raise ValueError('the coercion from PyAsteriskAsterisk | None to PyAsteriskAsterisk failed')


@no_type_check
def _coerce_union_2_token_slash_none_to_token_slash(value: 'PySlash | None') -> 'PySlash':
    if value is None:
        return PySlash()
    elif isinstance(value, PySlash):
        return value
    else:
        raise ValueError('the coercion from PySlash | None to PySlash failed')


@no_type_check
def _coerce_union_2_token_at_sign_none_to_token_at_sign(value: 'PyAtSign | None') -> 'PyAtSign':
    if value is None:
        return PyAtSign()
    elif isinstance(value, PyAtSign):
        return value
    else:
        raise ValueError('the coercion from PyAtSign | None to PyAtSign failed')


@no_type_check
def _coerce_union_2_token_def_keyword_none_to_token_def_keyword(value: 'PyDefKeyword | None') -> 'PyDefKeyword':
    if value is None:
        return PyDefKeyword()
    elif isinstance(value, PyDefKeyword):
        return value
    else:
        raise ValueError('the coercion from PyDefKeyword | None to PyDefKeyword failed')


@no_type_check
def _coerce_variant_param_to_variant_param(value: 'PyParam') -> 'PyParam':
    return value


@no_type_check
def _coerce_union_4_list_variant_param_list_tuple_2_variant_param_union_2_token_comma_none_punct_variant_param_token_comma_none_to_punct_variant_param_token_comma(value: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | Punctuated[PyParam, PyComma] | None') -> 'Punctuated[PyParam, PyComma]':
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
                    new_element_value = _coerce_variant_param_to_variant_param(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_param_to_variant_param(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | Punctuated[PyParam, PyComma] | None to Punctuated[PyParam, PyComma] failed')


@no_type_check
def _coerce_union_2_token_r_arrow_none_to_token_r_arrow(value: 'PyRArrow | None') -> 'PyRArrow':
    if value is None:
        return PyRArrow()
    elif isinstance(value, PyRArrow):
        return value
    else:
        raise ValueError('the coercion from PyRArrow | None to PyRArrow failed')


@no_type_check
def _coerce_union_3_variant_expr_tuple_2_union_2_token_r_arrow_none_variant_expr_none_to_union_2_tuple_2_token_r_arrow_variant_expr_none(value: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None') -> 'tuple[PyRArrow, PyExpr] | None':
    if is_py_expr(value):
        return (PyRArrow(), _coerce_variant_expr_to_variant_expr(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_r_arrow_none_to_token_r_arrow(value[0]), _coerce_variant_expr_to_variant_expr(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from PyExpr | tuple[PyRArrow | None, PyExpr] | None to tuple[PyRArrow, PyExpr] | None failed')


@no_type_check
def _coerce_union_2_list_variant_stmt_none_to_list_variant_stmt(value: 'Sequence[PyStmt] | None') -> 'Sequence[PyStmt]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_variant_stmt_to_variant_stmt(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[PyStmt] | None to Sequence[PyStmt] failed')


from typing import Callable, no_type_check


from .cst import *


def for_each_py_pattern(node: PyPattern, proc: Callable[[PyPattern], None]):
    if isinstance(node, PyNamedPattern):
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        for (element, separator) in node.slices.elements:
            if is_py_pattern(element):
                proc(element)
        if node.slices.last is not None:
            if is_py_pattern(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredPattern):
        return
    if isinstance(node, PyListPattern):
        for (element, separator) in node.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTuplePattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return


def for_each_py_expr(node: PyExpr, proc: Callable[[PyExpr], None]):
    if isinstance(node, PyEllipsisExpr):
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        return
    if isinstance(node, PyIfExpr):
        proc(node.then)
        proc(node.test)
        proc(node.alt)
        return
    if isinstance(node, PyConstExpr):
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyNamedExpr):
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                if is_py_expr(element.lower):
                    proc(element.lower)
                if is_py_expr(element.upper):
                    proc(element.upper)
                if isinstance(element.step, tuple):
                    proc(element.step[1])
            elif is_py_expr(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                if is_py_expr(node.slices.last.lower):
                    proc(node.slices.last.lower)
                if is_py_expr(node.slices.last.upper):
                    proc(node.slices.last.upper)
                if isinstance(node.slices.last.step, tuple):
                    proc(node.slices.last.step[1])
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTupleExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return


def for_each_py_arg(node: PyArg, proc: Callable[[PyArg], None]):
    if isinstance(node, PyEllipsisExpr):
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        return
    if isinstance(node, PyIfExpr):
        proc(node.then)
        proc(node.test)
        proc(node.alt)
        return
    if isinstance(node, PyConstExpr):
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyNamedExpr):
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                if is_py_expr(element.lower):
                    proc(element.lower)
                if is_py_expr(element.upper):
                    proc(element.upper)
                if isinstance(element.step, tuple):
                    proc(element.step[1])
            elif is_py_expr(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                if is_py_expr(node.slices.last.lower):
                    proc(node.slices.last.lower)
                if is_py_expr(node.slices.last.upper):
                    proc(node.slices.last.upper)
                if isinstance(node.slices.last.step, tuple):
                    proc(node.slices.last.step[1])
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTupleExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element, separator) in node.args.elements:
            proc(element)
        if node.args.last is not None:
            proc(node.args.last)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return


def for_each_py_stmt(node: PyStmt, proc: Callable[[PyStmt], None]):
    if isinstance(node, PyImportStmt):
        return
    if isinstance(node, PyImportFromStmt):
        return
    if isinstance(node, PyRetStmt):
        return
    if isinstance(node, PyExprStmt):
        return
    if isinstance(node, PyAugAssignStmt):
        return
    if isinstance(node, PyAssignStmt):
        return
    if isinstance(node, PyPassStmt):
        return
    if isinstance(node, PyGlobalStmt):
        return
    if isinstance(node, PyNonlocalStmt):
        return
    if isinstance(node, PyIfStmt):
        return
    if isinstance(node, PyDeleteStmt):
        return
    if isinstance(node, PyRaiseStmt):
        return
    if isinstance(node, PyForStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyWhileStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyBreakStmt):
        return
    if isinstance(node, PyContinueStmt):
        return
    if isinstance(node, PyTypeAliasStmt):
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_2 in node.finally_clause[2]:
                    proc(element_2)
        return
    if isinstance(node, PyClassDef):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyFuncDef):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return


def for_each_py_node(node: PyNode, proc: Callable[[PyNode], None]):
    if isinstance(node, PySlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        if is_py_expr(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[1])
        return
    if isinstance(node, PyNamedPattern):
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                proc(element)
            elif is_py_pattern(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                proc(node.slices.last)
            elif is_py_pattern(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredPattern):
        proc(node.expr)
        return
    if isinstance(node, PyListPattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTuplePattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyEllipsisExpr):
        return
    if isinstance(node, PyGuard):
        proc(node.expr)
        return
    if isinstance(node, PyComprehension):
        proc(node.pattern)
        proc(node.target)
        for element in node.guards:
            proc(element)
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element in node.generators:
            proc(element)
        return
    if isinstance(node, PyIfExpr):
        proc(node.then)
        proc(node.test)
        proc(node.alt)
        return
    if isinstance(node, PyConstExpr):
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyNamedExpr):
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                proc(element)
            elif is_py_expr(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                proc(node.slices.last)
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTupleExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element, separator) in node.args.elements:
            proc(element)
        if node.args.last is not None:
            proc(node.args.last)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return
    if isinstance(node, PyQualName):
        return
    if isinstance(node, PyAbsolutePath):
        proc(node.name)
        return
    if isinstance(node, PyRelativePath):
        if isinstance(node.name, PyQualName):
            proc(node.name)
        return
    if isinstance(node, PyAlias):
        proc(node.path)
        return
    if isinstance(node, PyFromAlias):
        return
    if isinstance(node, PyImportStmt):
        for (element, separator) in node.aliases.elements:
            proc(element)
        if node.aliases.last is not None:
            proc(node.aliases.last)
        return
    if isinstance(node, PyImportFromStmt):
        proc(node.path)
        for (element, separator) in node.aliases.elements:
            proc(element)
        if node.aliases.last is not None:
            proc(node.aliases.last)
        return
    if isinstance(node, PyRetStmt):
        if is_py_expr(node.expr):
            proc(node.expr)
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyAugAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        proc(node.expr)
        return
    if isinstance(node, PyAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.value, tuple):
            proc(node.value[1])
        return
    if isinstance(node, PyPassStmt):
        return
    if isinstance(node, PyGlobalStmt):
        return
    if isinstance(node, PyNonlocalStmt):
        return
    if isinstance(node, PyIfCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyElifCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyElseCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element in node.alternatives:
            proc(element)
        if isinstance(node.last, PyElseCase):
            proc(node.last)
        return
    if isinstance(node, PyDeleteStmt):
        proc(node.pattern)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.expr)
        if isinstance(node.cause, tuple):
            proc(node.cause[1])
        return
    if isinstance(node, PyForStmt):
        proc(node.pattern)
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyWhileStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyBreakStmt):
        return
    if isinstance(node, PyContinueStmt):
        return
    if isinstance(node, PyTypeAliasStmt):
        if isinstance(node.type_params, tuple):
            for (element, separator) in node.type_params[1].elements:
                proc(element)
            if node.type_params[1].last is not None:
                proc(node.type_params[1].last)
        proc(node.expr)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        for element_1 in node.handlers:
            proc(element_1)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_2 in node.else_clause[2]:
                    proc(element_2)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_3 in node.finally_clause[2]:
                    proc(element_3)
        return
    if isinstance(node, PyClassBaseArg):
        return
    if isinstance(node, PyKeywordBaseArg):
        proc(node.expr)
        return
    if isinstance(node, PyClassDef):
        for element in node.decorators:
            proc(element)
        if isinstance(node.bases, tuple):
            for (element_1, separator) in node.bases[1].elements:
                proc(element_1)
            if node.bases[1].last is not None:
                proc(node.bases[1].last)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)
        return
    if isinstance(node, PyNamedParam):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.default, tuple):
            proc(node.default[1])
        return
    if isinstance(node, PyRestPosParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyRestKeywordParam):
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        return
    if isinstance(node, PyPosSepParam):
        return
    if isinstance(node, PyKwSepParam):
        return
    if isinstance(node, PyDecorator):
        proc(node.expr)
        return
    if isinstance(node, PyFuncDef):
        for element in node.decorators:
            proc(element)
        for (element_1, separator) in node.params.elements:
            proc(element_1)
        if node.params.last is not None:
            proc(node.params.last)
        if isinstance(node.return_type, tuple):
            proc(node.return_type[1])
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)
        return
    if isinstance(node, PyModule):
        for element in node.stmts:
            proc(element)
        return


