from typing import Any, TypeGuard, Never, Sequence, no_type_check


from magelang.runtime import BaseNode, BaseToken, Punctuated, Span


class _PyBaseNode(BaseNode):

    pass


class _PyBaseToken(BaseToken):

    pass


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


class PySlice(_PyBaseNode):

    def __init__(self, *, lower: 'PyExpr | None' = None, colon: 'PyColon | None' = None, upper: 'PyExpr | None' = None, step: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> None:
        self.lower: PyExpr | None = _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(lower)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.upper: PyExpr | None = _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(upper)
        self.step: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(step)

    @no_type_check
    def derive(self, lower: 'PyExpr | None' = None, colon: 'PyColon | None' = None, upper: 'PyExpr | None' = None, step: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None) -> 'PySlice':
        if lower is None:
            lower = self.lower
        if colon is None:
            colon = self.colon
        if upper is None:
            upper = self.upper
        if step is None:
            step = self.step
        return PySlice(lower=lower, colon=colon, upper=upper, step=step)

    def parent(self) -> 'PySliceParent':
        assert(self._parent is not None)
        return self._parent


class PyNamedPattern(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, name: 'PyIdent | None | str' = None) -> 'PyNamedPattern':
        if name is None:
            name = self.name
        return PyNamedPattern(name=name)

    def parent(self) -> 'PyNamedPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyAttrPattern(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', name: 'PyIdent | str', *, dot: 'PyDot | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.dot: PyDot = _coerce_union_2_token_dot_none_to_token_dot(dot)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, pattern: 'PyPattern | None' = None, dot: 'PyDot | None' = None, name: 'PyIdent | None | str' = None) -> 'PyAttrPattern':
        if pattern is None:
            pattern = self.pattern
        if dot is None:
            dot = self.dot
        if name is None:
            name = self.name
        return PyAttrPattern(pattern=pattern, dot=dot, name=name)

    def parent(self) -> 'PyAttrPatternParent':
        assert(self._parent is not None)
        return self._parent


class PySubscriptPattern(_PyBaseNode):

    def count_slices(self) -> int:
        return len(self.slices)

    def __init__(self, pattern: 'PyPattern', slices: 'Sequence[tuple[PySlice | PyPattern, PyComma | None]] | Sequence[PySlice | PyPattern] | Punctuated[PySlice | PyPattern, PyComma]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.slices: Punctuated[PySlice | PyPattern, PyComma] = _coerce_union_3_list_tuple_2_union_2_node_slice_variant_pattern_union_2_token_comma_none_required_list_union_2_node_slice_variant_pattern_required_punct_union_2_node_slice_variant_pattern_token_comma_required_to_punct_union_2_node_slice_variant_pattern_token_comma_required(slices)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, pattern: 'PyPattern | None' = None, open_bracket: 'PyOpenBracket | None' = None, slices: 'Sequence[tuple[PySlice | PyPattern, PyComma | None]] | Sequence[PySlice | PyPattern] | Punctuated[PySlice | PyPattern, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> 'PySubscriptPattern':
        if pattern is None:
            pattern = self.pattern
        if open_bracket is None:
            open_bracket = self.open_bracket
        if slices is None:
            slices = self.slices
        if close_bracket is None:
            close_bracket = self.close_bracket
        return PySubscriptPattern(pattern=pattern, open_bracket=open_bracket, slices=slices, close_bracket=close_bracket)

    def parent(self) -> 'PySubscriptPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyStarredPattern(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, asterisk: 'PyAsterisk | None' = None, expr: 'PyExpr | None' = None) -> 'PyStarredPattern':
        if asterisk is None:
            asterisk = self.asterisk
        if expr is None:
            expr = self.expr
        return PyStarredPattern(asterisk=asterisk, expr=expr)

    def parent(self) -> 'PyStarredPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyListPattern(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.elements: Punctuated[PyPattern, PyComma] = _coerce_union_4_list_variant_pattern_list_tuple_2_variant_pattern_union_2_token_comma_none_punct_variant_pattern_token_comma_none_to_punct_variant_pattern_token_comma(elements)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> 'PyListPattern':
        if open_bracket is None:
            open_bracket = self.open_bracket
        if elements is None:
            elements = self.elements
        if close_bracket is None:
            close_bracket = self.close_bracket
        return PyListPattern(open_bracket=open_bracket, elements=elements, close_bracket=close_bracket)

    def parent(self) -> 'PyListPatternParent':
        assert(self._parent is not None)
        return self._parent


class PyTuplePattern(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.elements: Punctuated[PyPattern, PyComma] = _coerce_union_4_list_variant_pattern_list_tuple_2_variant_pattern_union_2_token_comma_none_punct_variant_pattern_token_comma_none_to_punct_variant_pattern_token_comma(elements)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyPattern] | Sequence[tuple[PyPattern, PyComma | None]] | Punctuated[PyPattern, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> 'PyTuplePattern':
        if open_paren is None:
            open_paren = self.open_paren
        if elements is None:
            elements = self.elements
        if close_paren is None:
            close_paren = self.close_paren
        return PyTuplePattern(open_paren=open_paren, elements=elements, close_paren=close_paren)

    def parent(self) -> 'PyTuplePatternParent':
        assert(self._parent is not None)
        return self._parent


class PyEllipsisExpr(_PyBaseNode):

    def __init__(self, *, dot_dot_dot: 'PyDotDotDot | None' = None) -> None:
        self.dot_dot_dot: PyDotDotDot = _coerce_union_2_token_dot_dot_dot_none_to_token_dot_dot_dot(dot_dot_dot)

    @no_type_check
    def derive(self, dot_dot_dot: 'PyDotDotDot | None' = None) -> 'PyEllipsisExpr':
        if dot_dot_dot is None:
            dot_dot_dot = self.dot_dot_dot
        return PyEllipsisExpr(dot_dot_dot=dot_dot_dot)

    def parent(self) -> 'PyEllipsisExprParent':
        assert(self._parent is not None)
        return self._parent


class PyGuard(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, if_keyword: 'PyIfKeyword | None' = None) -> None:
        self.if_keyword: PyIfKeyword = _coerce_union_2_token_if_keyword_none_to_token_if_keyword(if_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, if_keyword: 'PyIfKeyword | None' = None, expr: 'PyExpr | None' = None) -> 'PyGuard':
        if if_keyword is None:
            if_keyword = self.if_keyword
        if expr is None:
            expr = self.expr
        return PyGuard(if_keyword=if_keyword, expr=expr)

    def parent(self) -> 'PyGuardParent':
        assert(self._parent is not None)
        return self._parent


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

    @no_type_check
    def derive(self, async_keyword: 'PyAsyncKeyword | None' = None, for_keyword: 'PyForKeyword | None' = None, pattern: 'PyPattern | None' = None, in_keyword: 'PyInKeyword | None' = None, target: 'PyExpr | None' = None, guards: 'Sequence[PyGuard | PyExpr] | None' = None) -> 'PyComprehension':
        if async_keyword is None:
            async_keyword = self.async_keyword
        if for_keyword is None:
            for_keyword = self.for_keyword
        if pattern is None:
            pattern = self.pattern
        if in_keyword is None:
            in_keyword = self.in_keyword
        if target is None:
            target = self.target
        if guards is None:
            guards = self.guards
        return PyComprehension(async_keyword=async_keyword, for_keyword=for_keyword, pattern=pattern, in_keyword=in_keyword, target=target, guards=guards)

    def parent(self) -> 'PyComprehensionParent':
        assert(self._parent is not None)
        return self._parent


class PyGeneratorExpr(_PyBaseNode):

    def count_generators(self) -> int:
        return len(self.generators)

    def __init__(self, element: 'PyExpr', generators: 'Sequence[PyComprehension]') -> None:
        self.element: PyExpr = _coerce_variant_expr_to_variant_expr(element)
        self.generators: Sequence[PyComprehension] = _coerce_list_node_comprehension_required_to_list_node_comprehension_required(generators)

    @no_type_check
    def derive(self, element: 'PyExpr | None' = None, generators: 'Sequence[PyComprehension] | None' = None) -> 'PyGeneratorExpr':
        if element is None:
            element = self.element
        if generators is None:
            generators = self.generators
        return PyGeneratorExpr(element=element, generators=generators)

    def parent(self) -> 'PyGeneratorExprParent':
        assert(self._parent is not None)
        return self._parent


class PyConstExpr(_PyBaseNode):

    def __init__(self, literal: 'PyFloat | PyInteger | PyString | float | int | str') -> None:
        self.literal: PyFloat | PyInteger | PyString = _coerce_union_6_token_float_token_integer_token_string_extern_float_extern_integer_extern_string_to_union_3_token_float_token_integer_token_string(literal)

    @no_type_check
    def derive(self, literal: 'PyFloat | PyInteger | PyString | None | float | int | str' = None) -> 'PyConstExpr':
        if literal is None:
            literal = self.literal
        return PyConstExpr(literal=literal)

    def parent(self) -> 'PyConstExprParent':
        assert(self._parent is not None)
        return self._parent


class PyNestExpr(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, open_paren: 'PyOpenParen | None' = None, expr: 'PyExpr | None' = None, close_paren: 'PyCloseParen | None' = None) -> 'PyNestExpr':
        if open_paren is None:
            open_paren = self.open_paren
        if expr is None:
            expr = self.expr
        if close_paren is None:
            close_paren = self.close_paren
        return PyNestExpr(open_paren=open_paren, expr=expr, close_paren=close_paren)

    def parent(self) -> 'PyNestExprParent':
        assert(self._parent is not None)
        return self._parent


class PyNamedExpr(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str') -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, name: 'PyIdent | None | str' = None) -> 'PyNamedExpr':
        if name is None:
            name = self.name
        return PyNamedExpr(name=name)

    def parent(self) -> 'PyNamedExprParent':
        assert(self._parent is not None)
        return self._parent


class PyAttrExpr(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', name: 'PyIdent | str', *, dot: 'PyDot | None' = None) -> None:
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.dot: PyDot = _coerce_union_2_token_dot_none_to_token_dot(dot)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, expr: 'PyExpr | None' = None, dot: 'PyDot | None' = None, name: 'PyIdent | None | str' = None) -> 'PyAttrExpr':
        if expr is None:
            expr = self.expr
        if dot is None:
            dot = self.dot
        if name is None:
            name = self.name
        return PyAttrExpr(expr=expr, dot=dot, name=name)

    def parent(self) -> 'PyAttrExprParent':
        assert(self._parent is not None)
        return self._parent


class PySubscriptExpr(_PyBaseNode):

    def count_slices(self) -> int:
        return len(self.slices)

    def __init__(self, expr: 'PyExpr', slices: 'Sequence[tuple[PySlice | PyExpr, PyComma | None]] | Sequence[PySlice | PyExpr] | Punctuated[PySlice | PyExpr, PyComma]', *, open_bracket: 'PyOpenBracket | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.slices: Punctuated[PySlice | PyExpr, PyComma] = _coerce_union_3_list_tuple_2_union_2_node_slice_variant_expr_union_2_token_comma_none_required_list_union_2_node_slice_variant_expr_required_punct_union_2_node_slice_variant_expr_token_comma_required_to_punct_union_2_node_slice_variant_expr_token_comma_required(slices)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, expr: 'PyExpr | None' = None, open_bracket: 'PyOpenBracket | None' = None, slices: 'Sequence[tuple[PySlice | PyExpr, PyComma | None]] | Sequence[PySlice | PyExpr] | Punctuated[PySlice | PyExpr, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> 'PySubscriptExpr':
        if expr is None:
            expr = self.expr
        if open_bracket is None:
            open_bracket = self.open_bracket
        if slices is None:
            slices = self.slices
        if close_bracket is None:
            close_bracket = self.close_bracket
        return PySubscriptExpr(expr=expr, open_bracket=open_bracket, slices=slices, close_bracket=close_bracket)

    def parent(self) -> 'PySubscriptExprParent':
        assert(self._parent is not None)
        return self._parent


class PyStarredExpr(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, asterisk: 'PyAsterisk | None' = None, expr: 'PyExpr | None' = None) -> 'PyStarredExpr':
        if asterisk is None:
            asterisk = self.asterisk
        if expr is None:
            expr = self.expr
        return PyStarredExpr(asterisk=asterisk, expr=expr)

    def parent(self) -> 'PyStarredExprParent':
        assert(self._parent is not None)
        return self._parent


class PyListExpr(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> None:
        self.open_bracket: PyOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.elements: Punctuated[PyExpr, PyComma] = _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(elements)
        self.close_bracket: PyCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, open_bracket: 'PyOpenBracket | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, close_bracket: 'PyCloseBracket | None' = None) -> 'PyListExpr':
        if open_bracket is None:
            open_bracket = self.open_bracket
        if elements is None:
            elements = self.elements
        if close_bracket is None:
            close_bracket = self.close_bracket
        return PyListExpr(open_bracket=open_bracket, elements=elements, close_bracket=close_bracket)

    def parent(self) -> 'PyListExprParent':
        assert(self._parent is not None)
        return self._parent


class PyTupleExpr(_PyBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.elements: Punctuated[PyExpr, PyComma] = _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(elements)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, open_paren: 'PyOpenParen | None' = None, elements: 'Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> 'PyTupleExpr':
        if open_paren is None:
            open_paren = self.open_paren
        if elements is None:
            elements = self.elements
        if close_paren is None:
            close_paren = self.close_paren
        return PyTupleExpr(open_paren=open_paren, elements=elements, close_paren=close_paren)

    def parent(self) -> 'PyTupleExprParent':
        assert(self._parent is not None)
        return self._parent


class PyKeywordArg(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, equals: 'PyEquals | None' = None) -> None:
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.equals: PyEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, name: 'PyIdent | None | str' = None, equals: 'PyEquals | None' = None, expr: 'PyExpr | None' = None) -> 'PyKeywordArg':
        if name is None:
            name = self.name
        if equals is None:
            equals = self.equals
        if expr is None:
            expr = self.expr
        return PyKeywordArg(name=name, equals=equals, expr=expr)

    def parent(self) -> 'PyKeywordArgParent':
        assert(self._parent is not None)
        return self._parent


class PyCallExpr(_PyBaseNode):

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, operator: 'PyExpr', *, open_paren: 'PyOpenParen | None' = None, args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> None:
        self.operator: PyExpr = _coerce_variant_expr_to_variant_expr(operator)
        self.open_paren: PyOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.args: Punctuated[PyArg, PyComma] = _coerce_union_4_list_variant_arg_list_tuple_2_variant_arg_union_2_token_comma_none_punct_variant_arg_token_comma_none_to_punct_variant_arg_token_comma(args)
        self.close_paren: PyCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, operator: 'PyExpr | None' = None, open_paren: 'PyOpenParen | None' = None, args: 'Sequence[PyArg] | Sequence[tuple[PyArg, PyComma | None]] | Punctuated[PyArg, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None) -> 'PyCallExpr':
        if operator is None:
            operator = self.operator
        if open_paren is None:
            open_paren = self.open_paren
        if args is None:
            args = self.args
        if close_paren is None:
            close_paren = self.close_paren
        return PyCallExpr(operator=operator, open_paren=open_paren, args=args, close_paren=close_paren)

    def parent(self) -> 'PyCallExprParent':
        assert(self._parent is not None)
        return self._parent


class PyPrefixExpr(_PyBaseNode):

    def __init__(self, prefix_op: 'PyPrefixOp', expr: 'PyExpr') -> None:
        self.prefix_op: PyPrefixOp = _coerce_variant_prefix_op_to_variant_prefix_op(prefix_op)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, prefix_op: 'PyPrefixOp | None' = None, expr: 'PyExpr | None' = None) -> 'PyPrefixExpr':
        if prefix_op is None:
            prefix_op = self.prefix_op
        if expr is None:
            expr = self.expr
        return PyPrefixExpr(prefix_op=prefix_op, expr=expr)

    def parent(self) -> 'PyPrefixExprParent':
        assert(self._parent is not None)
        return self._parent


class PyInfixExpr(_PyBaseNode):

    def __init__(self, left: 'PyExpr', op: 'PyInfixOp', right: 'PyExpr') -> None:
        self.left: PyExpr = _coerce_variant_expr_to_variant_expr(left)
        self.op: PyInfixOp = _coerce_variant_infix_op_to_variant_infix_op(op)
        self.right: PyExpr = _coerce_variant_expr_to_variant_expr(right)

    @no_type_check
    def derive(self, left: 'PyExpr | None' = None, op: 'PyInfixOp | None' = None, right: 'PyExpr | None' = None) -> 'PyInfixExpr':
        if left is None:
            left = self.left
        if op is None:
            op = self.op
        if right is None:
            right = self.right
        return PyInfixExpr(left=left, op=op, right=right)

    def parent(self) -> 'PyInfixExprParent':
        assert(self._parent is not None)
        return self._parent


class PyQualName(_PyBaseNode):

    def count_modules(self) -> int:
        return len(self.modules)

    def __init__(self, name: 'PyIdent | str', *, modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None' = None) -> None:
        self.modules: Sequence[tuple[PyIdent, PyDot]] = _coerce_union_2_list_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_dot_none_extern_string_none_to_list_tuple_2_token_ident_token_dot(modules)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, modules: 'Sequence[PyIdent | tuple[PyIdent | str, PyDot | None] | str] | None' = None, name: 'PyIdent | None | str' = None) -> 'PyQualName':
        if modules is None:
            modules = self.modules
        if name is None:
            name = self.name
        return PyQualName(modules=modules, name=name)

    def parent(self) -> 'PyQualNameParent':
        assert(self._parent is not None)
        return self._parent


class PyAbsolutePath(_PyBaseNode):

    def __init__(self, name: 'PyQualName | PyIdent | str') -> None:
        self.name: PyQualName = _coerce_union_3_node_qual_name_token_ident_extern_string_to_node_qual_name(name)

    @no_type_check
    def derive(self, name: 'PyQualName | PyIdent | None | str' = None) -> 'PyAbsolutePath':
        if name is None:
            name = self.name
        return PyAbsolutePath(name=name)

    def parent(self) -> 'PyAbsolutePathParent':
        assert(self._parent is not None)
        return self._parent


class PyRelativePath(_PyBaseNode):

    def count_dots(self) -> int:
        return len(self.dots)

    def __init__(self, dots: 'Sequence[PyDot] | int', *, name: 'PyQualName | PyIdent | None | str' = None) -> None:
        self.dots: Sequence[PyDot] = _coerce_union_2_list_token_dot_required_extern_integer_to_list_token_dot_required(dots)
        self.name: PyQualName | None = _coerce_union_4_node_qual_name_token_ident_none_extern_string_to_union_2_node_qual_name_none(name)

    @no_type_check
    def derive(self, dots: 'Sequence[PyDot] | None | int' = None, name: 'PyQualName | PyIdent | None | str' = None) -> 'PyRelativePath':
        if dots is None:
            dots = self.dots
        if name is None:
            name = self.name
        return PyRelativePath(dots=dots, name=name)

    def parent(self) -> 'PyRelativePathParent':
        assert(self._parent is not None)
        return self._parent


class PyAlias(_PyBaseNode):

    def __init__(self, path: 'PyPath', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> None:
        self.path: PyPath = _coerce_variant_path_to_variant_path(path)
        self.asname: tuple[PyAsKeyword, PyIdent] | None = _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(asname)

    @no_type_check
    def derive(self, path: 'PyPath | None' = None, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> 'PyAlias':
        if path is None:
            path = self.path
        if asname is None:
            asname = self.asname
        return PyAlias(path=path, asname=asname)

    def parent(self) -> 'PyAliasParent':
        assert(self._parent is not None)
        return self._parent


class PyFromAlias(_PyBaseNode):

    def __init__(self, name: 'PyAsterisk | PyIdent | str', *, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> None:
        self.name: PyAsterisk | PyIdent = _coerce_union_3_token_asterisk_token_ident_extern_string_to_union_2_token_asterisk_token_ident(name)
        self.asname: tuple[PyAsKeyword, PyIdent] | None = _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(asname)

    @no_type_check
    def derive(self, name: 'PyAsterisk | PyIdent | None | str' = None, asname: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None) -> 'PyFromAlias':
        if name is None:
            name = self.name
        if asname is None:
            asname = self.asname
        return PyFromAlias(name=name, asname=asname)

    def parent(self) -> 'PyFromAliasParent':
        assert(self._parent is not None)
        return self._parent


class PyImportStmt(_PyBaseNode):

    def count_aliases(self) -> int:
        return len(self.aliases)

    def __init__(self, aliases: 'Sequence[PyAlias] | Sequence[tuple[PyAlias, PyComma | None]] | Punctuated[PyAlias, PyComma]', *, import_keyword: 'PyImportKeyword | None' = None) -> None:
        self.import_keyword: PyImportKeyword = _coerce_union_2_token_import_keyword_none_to_token_import_keyword(import_keyword)
        self.aliases: Punctuated[PyAlias, PyComma] = _coerce_union_3_list_node_alias_required_list_tuple_2_node_alias_union_2_token_comma_none_required_punct_node_alias_token_comma_required_to_punct_node_alias_token_comma_required(aliases)

    @no_type_check
    def derive(self, import_keyword: 'PyImportKeyword | None' = None, aliases: 'Sequence[PyAlias] | Sequence[tuple[PyAlias, PyComma | None]] | Punctuated[PyAlias, PyComma] | None' = None) -> 'PyImportStmt':
        if import_keyword is None:
            import_keyword = self.import_keyword
        if aliases is None:
            aliases = self.aliases
        return PyImportStmt(import_keyword=import_keyword, aliases=aliases)

    def parent(self) -> 'PyImportStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyImportFromStmt(_PyBaseNode):

    def count_aliases(self) -> int:
        return len(self.aliases)

    def __init__(self, path: 'PyPath', aliases: 'Sequence[PyFromAlias] | Sequence[tuple[PyFromAlias, PyComma | None]] | Punctuated[PyFromAlias, PyComma]', *, from_keyword: 'PyFromKeyword | None' = None, import_keyword: 'PyImportKeyword | None' = None) -> None:
        self.from_keyword: PyFromKeyword = _coerce_union_2_token_from_keyword_none_to_token_from_keyword(from_keyword)
        self.path: PyPath = _coerce_variant_path_to_variant_path(path)
        self.import_keyword: PyImportKeyword = _coerce_union_2_token_import_keyword_none_to_token_import_keyword(import_keyword)
        self.aliases: Punctuated[PyFromAlias, PyComma] = _coerce_union_3_list_node_from_alias_required_list_tuple_2_node_from_alias_union_2_token_comma_none_required_punct_node_from_alias_token_comma_required_to_punct_node_from_alias_token_comma_required(aliases)

    @no_type_check
    def derive(self, from_keyword: 'PyFromKeyword | None' = None, path: 'PyPath | None' = None, import_keyword: 'PyImportKeyword | None' = None, aliases: 'Sequence[PyFromAlias] | Sequence[tuple[PyFromAlias, PyComma | None]] | Punctuated[PyFromAlias, PyComma] | None' = None) -> 'PyImportFromStmt':
        if from_keyword is None:
            from_keyword = self.from_keyword
        if path is None:
            path = self.path
        if import_keyword is None:
            import_keyword = self.import_keyword
        if aliases is None:
            aliases = self.aliases
        return PyImportFromStmt(from_keyword=from_keyword, path=path, import_keyword=import_keyword, aliases=aliases)

    def parent(self) -> 'PyImportFromStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyRetStmt(_PyBaseNode):

    def __init__(self, *, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> None:
        self.return_keyword: PyReturnKeyword = _coerce_union_2_token_return_keyword_none_to_token_return_keyword(return_keyword)
        self.expr: PyExpr | None = _coerce_union_2_variant_expr_none_to_union_2_variant_expr_none(expr)

    @no_type_check
    def derive(self, return_keyword: 'PyReturnKeyword | None' = None, expr: 'PyExpr | None' = None) -> 'PyRetStmt':
        if return_keyword is None:
            return_keyword = self.return_keyword
        if expr is None:
            expr = self.expr
        return PyRetStmt(return_keyword=return_keyword, expr=expr)

    def parent(self) -> 'PyRetStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyExprStmt(_PyBaseNode):

    def __init__(self, expr: 'PyExpr') -> None:
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, expr: 'PyExpr | None' = None) -> 'PyExprStmt':
        if expr is None:
            expr = self.expr
        return PyExprStmt(expr=expr)

    def parent(self) -> 'PyExprStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyAssignStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)
        self.value: tuple[PyEquals, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_equals_none_variant_expr_none_to_union_2_tuple_2_token_equals_variant_expr_none(value)

    @no_type_check
    def derive(self, pattern: 'PyPattern | None' = None, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, value: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> 'PyAssignStmt':
        if pattern is None:
            pattern = self.pattern
        if annotation is None:
            annotation = self.annotation
        if value is None:
            value = self.value
        return PyAssignStmt(pattern=pattern, annotation=annotation, value=value)

    def parent(self) -> 'PyAssignStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyPassStmt(_PyBaseNode):

    def __init__(self, *, pass_keyword: 'PyPassKeyword | None' = None) -> None:
        self.pass_keyword: PyPassKeyword = _coerce_union_2_token_pass_keyword_none_to_token_pass_keyword(pass_keyword)

    @no_type_check
    def derive(self, pass_keyword: 'PyPassKeyword | None' = None) -> 'PyPassStmt':
        if pass_keyword is None:
            pass_keyword = self.pass_keyword
        return PyPassStmt(pass_keyword=pass_keyword)

    def parent(self) -> 'PyPassStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyGlobalStmt(_PyBaseNode):

    def count_names(self) -> int:
        return len(self.names)

    def __init__(self, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]', *, global_keyword: 'PyGlobalKeyword | None' = None) -> None:
        self.global_keyword: PyGlobalKeyword = _coerce_union_2_token_global_keyword_none_to_token_global_keyword(global_keyword)
        self.names: Punctuated[PyIdent, PyComma] = _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_required_list_union_2_token_ident_extern_string_required_punct_union_2_token_ident_extern_string_token_comma_required_to_punct_token_ident_token_comma_required(names)

    @no_type_check
    def derive(self, global_keyword: 'PyGlobalKeyword | None' = None, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None' = None) -> 'PyGlobalStmt':
        if global_keyword is None:
            global_keyword = self.global_keyword
        if names is None:
            names = self.names
        return PyGlobalStmt(global_keyword=global_keyword, names=names)

    def parent(self) -> 'PyGlobalStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyNonlocalStmt(_PyBaseNode):

    def count_names(self) -> int:
        return len(self.names)

    def __init__(self, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]', *, nonlocal_keyword: 'PyNonlocalKeyword | None' = None) -> None:
        self.nonlocal_keyword: PyNonlocalKeyword = _coerce_union_2_token_nonlocal_keyword_none_to_token_nonlocal_keyword(nonlocal_keyword)
        self.names: Punctuated[PyIdent, PyComma] = _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_required_list_union_2_token_ident_extern_string_required_punct_union_2_token_ident_extern_string_token_comma_required_to_punct_token_ident_token_comma_required(names)

    @no_type_check
    def derive(self, nonlocal_keyword: 'PyNonlocalKeyword | None' = None, names: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None' = None) -> 'PyNonlocalStmt':
        if nonlocal_keyword is None:
            nonlocal_keyword = self.nonlocal_keyword
        if names is None:
            names = self.names
        return PyNonlocalStmt(nonlocal_keyword=nonlocal_keyword, names=names)

    def parent(self) -> 'PyNonlocalStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyIfCase(_PyBaseNode):

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, if_keyword: 'PyIfKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.if_keyword: PyIfKeyword = _coerce_union_2_token_if_keyword_none_to_token_if_keyword(if_keyword)
        self.test: PyExpr = _coerce_variant_expr_to_variant_expr(test)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)

    @no_type_check
    def derive(self, if_keyword: 'PyIfKeyword | None' = None, test: 'PyExpr | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None) -> 'PyIfCase':
        if if_keyword is None:
            if_keyword = self.if_keyword
        if test is None:
            test = self.test
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        return PyIfCase(if_keyword=if_keyword, test=test, colon=colon, body=body)

    def parent(self) -> 'PyIfCaseParent':
        assert(self._parent is not None)
        return self._parent


class PyElifCase(_PyBaseNode):

    def __init__(self, test: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, elif_keyword: 'PyElifKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.elif_keyword: PyElifKeyword = _coerce_union_2_token_elif_keyword_none_to_token_elif_keyword(elif_keyword)
        self.test: PyExpr = _coerce_variant_expr_to_variant_expr(test)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)

    @no_type_check
    def derive(self, elif_keyword: 'PyElifKeyword | None' = None, test: 'PyExpr | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None) -> 'PyElifCase':
        if elif_keyword is None:
            elif_keyword = self.elif_keyword
        if test is None:
            test = self.test
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        return PyElifCase(elif_keyword=elif_keyword, test=test, colon=colon, body=body)

    def parent(self) -> 'PyElifCaseParent':
        assert(self._parent is not None)
        return self._parent


class PyElseCase(_PyBaseNode):

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None) -> None:
        self.else_keyword: PyElseKeyword = _coerce_union_2_token_else_keyword_none_to_token_else_keyword(else_keyword)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)

    @no_type_check
    def derive(self, else_keyword: 'PyElseKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None) -> 'PyElseCase':
        if else_keyword is None:
            else_keyword = self.else_keyword
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        return PyElseCase(else_keyword=else_keyword, colon=colon, body=body)

    def parent(self) -> 'PyElseCaseParent':
        assert(self._parent is not None)
        return self._parent


class PyIfStmt(_PyBaseNode):

    def count_alternatives(self) -> int:
        return len(self.alternatives)

    def __init__(self, first: 'PyIfCase', *, alternatives: 'Sequence[PyElifCase] | None' = None, last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None' = None) -> None:
        self.first: PyIfCase = _coerce_node_if_case_to_node_if_case(first)
        self.alternatives: Sequence[PyElifCase] = _coerce_union_2_list_node_elif_case_none_to_list_node_elif_case(alternatives)
        self.last: PyElseCase | None = _coerce_union_4_node_else_case_variant_stmt_list_variant_stmt_none_to_union_2_node_else_case_none(last)

    @no_type_check
    def derive(self, first: 'PyIfCase | None' = None, alternatives: 'Sequence[PyElifCase] | None' = None, last: 'PyElseCase | PyStmt | Sequence[PyStmt] | None' = None) -> 'PyIfStmt':
        if first is None:
            first = self.first
        if alternatives is None:
            alternatives = self.alternatives
        if last is None:
            last = self.last
        return PyIfStmt(first=first, alternatives=alternatives, last=last)

    def parent(self) -> 'PyIfStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyDeleteStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', *, del_keyword: 'PyDelKeyword | None' = None) -> None:
        self.del_keyword: PyDelKeyword = _coerce_union_2_token_del_keyword_none_to_token_del_keyword(del_keyword)
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)

    @no_type_check
    def derive(self, del_keyword: 'PyDelKeyword | None' = None, pattern: 'PyPattern | None' = None) -> 'PyDeleteStmt':
        if del_keyword is None:
            del_keyword = self.del_keyword
        if pattern is None:
            pattern = self.pattern
        return PyDeleteStmt(del_keyword=del_keyword, pattern=pattern)

    def parent(self) -> 'PyDeleteStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyRaiseStmt(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, raise_keyword: 'PyRaiseKeyword | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None) -> None:
        self.raise_keyword: PyRaiseKeyword = _coerce_union_2_token_raise_keyword_none_to_token_raise_keyword(raise_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.cause: tuple[PyFromKeyword, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_from_keyword_none_variant_expr_none_to_union_2_tuple_2_token_from_keyword_variant_expr_none(cause)

    @no_type_check
    def derive(self, raise_keyword: 'PyRaiseKeyword | None' = None, expr: 'PyExpr | None' = None, cause: 'PyExpr | tuple[PyFromKeyword | None, PyExpr] | None' = None) -> 'PyRaiseStmt':
        if raise_keyword is None:
            raise_keyword = self.raise_keyword
        if expr is None:
            expr = self.expr
        if cause is None:
            cause = self.cause
        return PyRaiseStmt(raise_keyword=raise_keyword, expr=expr, cause=cause)

    def parent(self) -> 'PyRaiseStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyForStmt(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, for_keyword: 'PyForKeyword | None' = None, in_keyword: 'PyInKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.for_keyword: PyForKeyword = _coerce_union_2_token_for_keyword_none_to_token_for_keyword(for_keyword)
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.in_keyword: PyInKeyword = _coerce_union_2_token_in_keyword_none_to_token_in_keyword(in_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_list_variant_stmt_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_none(else_clause)

    @no_type_check
    def derive(self, for_keyword: 'PyForKeyword | None' = None, pattern: 'PyPattern | None' = None, in_keyword: 'PyInKeyword | None' = None, expr: 'PyExpr | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> 'PyForStmt':
        if for_keyword is None:
            for_keyword = self.for_keyword
        if pattern is None:
            pattern = self.pattern
        if in_keyword is None:
            in_keyword = self.in_keyword
        if expr is None:
            expr = self.expr
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        if else_clause is None:
            else_clause = self.else_clause
        return PyForStmt(for_keyword=for_keyword, pattern=pattern, in_keyword=in_keyword, expr=expr, colon=colon, body=body, else_clause=else_clause)

    def parent(self) -> 'PyForStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyWhileStmt(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, while_keyword: 'PyWhileKeyword | None' = None, colon: 'PyColon | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.while_keyword: PyWhileKeyword = _coerce_union_2_token_while_keyword_none_to_token_while_keyword(while_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_list_variant_stmt_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_none(else_clause)

    @no_type_check
    def derive(self, while_keyword: 'PyWhileKeyword | None' = None, expr: 'PyExpr | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> 'PyWhileStmt':
        if while_keyword is None:
            while_keyword = self.while_keyword
        if expr is None:
            expr = self.expr
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        if else_clause is None:
            else_clause = self.else_clause
        return PyWhileStmt(while_keyword=while_keyword, expr=expr, colon=colon, body=body, else_clause=else_clause)

    def parent(self) -> 'PyWhileStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyBreakStmt(_PyBaseNode):

    def __init__(self, *, break_keyword: 'PyBreakKeyword | None' = None) -> None:
        self.break_keyword: PyBreakKeyword = _coerce_union_2_token_break_keyword_none_to_token_break_keyword(break_keyword)

    @no_type_check
    def derive(self, break_keyword: 'PyBreakKeyword | None' = None) -> 'PyBreakStmt':
        if break_keyword is None:
            break_keyword = self.break_keyword
        return PyBreakStmt(break_keyword=break_keyword)

    def parent(self) -> 'PyBreakStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyContinueStmt(_PyBaseNode):

    def __init__(self, *, continue_keyword: 'PyContinueKeyword | None' = None) -> None:
        self.continue_keyword: PyContinueKeyword = _coerce_union_2_token_continue_keyword_none_to_token_continue_keyword(continue_keyword)

    @no_type_check
    def derive(self, continue_keyword: 'PyContinueKeyword | None' = None) -> 'PyContinueStmt':
        if continue_keyword is None:
            continue_keyword = self.continue_keyword
        return PyContinueStmt(continue_keyword=continue_keyword)

    def parent(self) -> 'PyContinueStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyTypeAliasStmt(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', expr: 'PyExpr', *, type_keyword: 'PyTypeKeyword | None' = None, type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, equals: 'PyEquals | None' = None) -> None:
        self.type_keyword: PyTypeKeyword = _coerce_union_2_token_type_keyword_none_to_token_type_keyword(type_keyword)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.type_params: tuple[PyOpenBracket, Punctuated[PyExpr, PyComma], PyCloseBracket] | None = _coerce_union_5_tuple_3_union_2_token_open_bracket_none_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_union_2_token_close_bracket_none_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_union_2_tuple_3_token_open_bracket_punct_variant_expr_token_comma_token_close_bracket_none(type_params)
        self.equals: PyEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, type_keyword: 'PyTypeKeyword | None' = None, name: 'PyIdent | None | str' = None, type_params: 'tuple[PyOpenBracket | None, Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None, PyCloseBracket | None] | Sequence[PyExpr] | Sequence[tuple[PyExpr, PyComma | None]] | Punctuated[PyExpr, PyComma] | None' = None, equals: 'PyEquals | None' = None, expr: 'PyExpr | None' = None) -> 'PyTypeAliasStmt':
        if type_keyword is None:
            type_keyword = self.type_keyword
        if name is None:
            name = self.name
        if type_params is None:
            type_params = self.type_params
        if equals is None:
            equals = self.equals
        if expr is None:
            expr = self.expr
        return PyTypeAliasStmt(type_keyword=type_keyword, name=name, type_params=type_params, equals=equals, expr=expr)

    def parent(self) -> 'PyTypeAliasStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyExceptHandler(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', body: 'PyStmt | Sequence[PyStmt]', *, except_keyword: 'PyExceptKeyword | None' = None, binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None, colon: 'PyColon | None' = None) -> None:
        self.except_keyword: PyExceptKeyword = _coerce_union_2_token_except_keyword_none_to_token_except_keyword(except_keyword)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.binder: tuple[PyAsKeyword, PyIdent] | None = _coerce_union_4_token_ident_tuple_2_union_2_token_as_keyword_none_union_2_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_as_keyword_token_ident_none(binder)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)

    @no_type_check
    def derive(self, except_keyword: 'PyExceptKeyword | None' = None, expr: 'PyExpr | None' = None, binder: 'PyIdent | tuple[PyAsKeyword | None, PyIdent | str] | None | str' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None) -> 'PyExceptHandler':
        if except_keyword is None:
            except_keyword = self.except_keyword
        if expr is None:
            expr = self.expr
        if binder is None:
            binder = self.binder
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        return PyExceptHandler(except_keyword=except_keyword, expr=expr, binder=binder, colon=colon, body=body)

    def parent(self) -> 'PyExceptHandlerParent':
        assert(self._parent is not None)
        return self._parent


class PyTryStmt(_PyBaseNode):

    def count_handlers(self) -> int:
        return len(self.handlers)

    def __init__(self, body: 'PyStmt | Sequence[PyStmt]', *, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, handlers: 'Sequence[PyExceptHandler] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None, finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> None:
        self.try_keyword: PyTryKeyword = _coerce_union_2_token_try_keyword_none_to_token_try_keyword(try_keyword)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)
        self.handlers: Sequence[PyExceptHandler] = _coerce_union_2_list_node_except_handler_none_to_list_node_except_handler(handlers)
        self.else_clause: tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_list_variant_stmt_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_none(else_clause)
        self.finally_clause: tuple[PyFinallyKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None = _coerce_union_4_variant_stmt_tuple_3_union_2_token_finally_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_list_variant_stmt_none_to_union_2_tuple_3_token_finally_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_none(finally_clause)

    @no_type_check
    def derive(self, try_keyword: 'PyTryKeyword | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None, handlers: 'Sequence[PyExceptHandler] | None' = None, else_clause: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None, finally_clause: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None' = None) -> 'PyTryStmt':
        if try_keyword is None:
            try_keyword = self.try_keyword
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        if handlers is None:
            handlers = self.handlers
        if else_clause is None:
            else_clause = self.else_clause
        if finally_clause is None:
            finally_clause = self.finally_clause
        return PyTryStmt(try_keyword=try_keyword, colon=colon, body=body, handlers=handlers, else_clause=else_clause, finally_clause=finally_clause)

    def parent(self) -> 'PyTryStmtParent':
        assert(self._parent is not None)
        return self._parent


class PyClassDef(_PyBaseNode):

    def count_decorators(self) -> int:
        return len(self.decorators)

    def __init__(self, name: 'PyIdent | str', body: 'PyStmt | Sequence[PyStmt]', *, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, class_keyword: 'PyClassKeyword | None' = None, bases: 'tuple[PyOpenParen | None, Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None, PyCloseParen | None] | Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None' = None, colon: 'PyColon | None' = None) -> None:
        self.decorators: Sequence[PyDecorator] = _coerce_union_2_list_union_2_node_decorator_variant_expr_none_to_list_node_decorator(decorators)
        self.class_keyword: PyClassKeyword = _coerce_union_2_token_class_keyword_none_to_token_class_keyword(class_keyword)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.bases: tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None = _coerce_union_5_tuple_3_union_2_token_open_paren_none_union_4_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_none_union_2_token_close_paren_none_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_none_to_union_2_tuple_3_token_open_paren_punct_token_ident_token_comma_token_close_paren_none(bases)
        self.colon: PyColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)

    @no_type_check
    def derive(self, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, class_keyword: 'PyClassKeyword | None' = None, name: 'PyIdent | None | str' = None, bases: 'tuple[PyOpenParen | None, Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None, PyCloseParen | None] | Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None) -> 'PyClassDef':
        if decorators is None:
            decorators = self.decorators
        if class_keyword is None:
            class_keyword = self.class_keyword
        if name is None:
            name = self.name
        if bases is None:
            bases = self.bases
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        return PyClassDef(decorators=decorators, class_keyword=class_keyword, name=name, bases=bases, colon=colon, body=body)

    def parent(self) -> 'PyClassDefParent':
        assert(self._parent is not None)
        return self._parent


class PyNamedParam(_PyBaseNode):

    def __init__(self, pattern: 'PyPattern', *, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> None:
        self.pattern: PyPattern = _coerce_variant_pattern_to_variant_pattern(pattern)
        self.annotation: tuple[PyColon, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_colon_none_variant_expr_none_to_union_2_tuple_2_token_colon_variant_expr_none(annotation)
        self.default: tuple[PyEquals, PyExpr] | None = _coerce_union_3_variant_expr_tuple_2_union_2_token_equals_none_variant_expr_none_to_union_2_tuple_2_token_equals_variant_expr_none(default)

    @no_type_check
    def derive(self, pattern: 'PyPattern | None' = None, annotation: 'PyExpr | tuple[PyColon | None, PyExpr] | None' = None, default: 'PyExpr | tuple[PyEquals | None, PyExpr] | None' = None) -> 'PyNamedParam':
        if pattern is None:
            pattern = self.pattern
        if annotation is None:
            annotation = self.annotation
        if default is None:
            default = self.default
        return PyNamedParam(pattern=pattern, annotation=annotation, default=default)

    def parent(self) -> 'PyNamedParamParent':
        assert(self._parent is not None)
        return self._parent


class PyRestPosParam(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, asterisk: 'PyAsterisk | None' = None, name: 'PyIdent | None | str' = None) -> 'PyRestPosParam':
        if asterisk is None:
            asterisk = self.asterisk
        if name is None:
            name = self.name
        return PyRestPosParam(asterisk=asterisk, name=name)

    def parent(self) -> 'PyRestPosParamParent':
        assert(self._parent is not None)
        return self._parent


class PyRestKeywordParam(_PyBaseNode):

    def __init__(self, name: 'PyIdent | str', *, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None) -> None:
        self.asterisk_asterisk: PyAsteriskAsterisk = _coerce_union_2_token_asterisk_asterisk_none_to_token_asterisk_asterisk(asterisk_asterisk)
        self.name: PyIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, asterisk_asterisk: 'PyAsteriskAsterisk | None' = None, name: 'PyIdent | None | str' = None) -> 'PyRestKeywordParam':
        if asterisk_asterisk is None:
            asterisk_asterisk = self.asterisk_asterisk
        if name is None:
            name = self.name
        return PyRestKeywordParam(asterisk_asterisk=asterisk_asterisk, name=name)

    def parent(self) -> 'PyRestKeywordParamParent':
        assert(self._parent is not None)
        return self._parent


class PyPosSepParam(_PyBaseNode):

    def __init__(self, *, slash: 'PySlash | None' = None) -> None:
        self.slash: PySlash = _coerce_union_2_token_slash_none_to_token_slash(slash)

    @no_type_check
    def derive(self, slash: 'PySlash | None' = None) -> 'PyPosSepParam':
        if slash is None:
            slash = self.slash
        return PyPosSepParam(slash=slash)

    def parent(self) -> 'PyPosSepParamParent':
        assert(self._parent is not None)
        return self._parent


class PyKwSepParam(_PyBaseNode):

    def __init__(self, *, asterisk: 'PyAsterisk | None' = None) -> None:
        self.asterisk: PyAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)

    @no_type_check
    def derive(self, asterisk: 'PyAsterisk | None' = None) -> 'PyKwSepParam':
        if asterisk is None:
            asterisk = self.asterisk
        return PyKwSepParam(asterisk=asterisk)

    def parent(self) -> 'PyKwSepParamParent':
        assert(self._parent is not None)
        return self._parent


class PyDecorator(_PyBaseNode):

    def __init__(self, expr: 'PyExpr', *, at_sign: 'PyAtSign | None' = None) -> None:
        self.at_sign: PyAtSign = _coerce_union_2_token_at_sign_none_to_token_at_sign(at_sign)
        self.expr: PyExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, at_sign: 'PyAtSign | None' = None, expr: 'PyExpr | None' = None) -> 'PyDecorator':
        if at_sign is None:
            at_sign = self.at_sign
        if expr is None:
            expr = self.expr
        return PyDecorator(at_sign=at_sign, expr=expr)

    def parent(self) -> 'PyDecoratorParent':
        assert(self._parent is not None)
        return self._parent


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
        self.body: PyStmt | Sequence[PyStmt] = _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(body)

    @no_type_check
    def derive(self, decorators: 'Sequence[PyDecorator | PyExpr] | None' = None, async_keyword: 'PyAsyncKeyword | None' = None, def_keyword: 'PyDefKeyword | None' = None, name: 'PyIdent | None | str' = None, open_paren: 'PyOpenParen | None' = None, params: 'Sequence[PyParam] | Sequence[tuple[PyParam, PyComma | None]] | Punctuated[PyParam, PyComma] | None' = None, close_paren: 'PyCloseParen | None' = None, return_type: 'PyExpr | tuple[PyRArrow | None, PyExpr] | None' = None, colon: 'PyColon | None' = None, body: 'PyStmt | Sequence[PyStmt] | None' = None) -> 'PyFuncDef':
        if decorators is None:
            decorators = self.decorators
        if async_keyword is None:
            async_keyword = self.async_keyword
        if def_keyword is None:
            def_keyword = self.def_keyword
        if name is None:
            name = self.name
        if open_paren is None:
            open_paren = self.open_paren
        if params is None:
            params = self.params
        if close_paren is None:
            close_paren = self.close_paren
        if return_type is None:
            return_type = self.return_type
        if colon is None:
            colon = self.colon
        if body is None:
            body = self.body
        return PyFuncDef(decorators=decorators, async_keyword=async_keyword, def_keyword=def_keyword, name=name, open_paren=open_paren, params=params, close_paren=close_paren, return_type=return_type, colon=colon, body=body)

    def parent(self) -> 'PyFuncDefParent':
        assert(self._parent is not None)
        return self._parent


class PyModule(_PyBaseNode):

    def count_stmts(self) -> int:
        return len(self.stmts)

    def __init__(self, *, stmts: 'Sequence[PyStmt] | None' = None) -> None:
        self.stmts: Sequence[PyStmt] = _coerce_union_2_list_variant_stmt_none_to_list_variant_stmt(stmts)

    @no_type_check
    def derive(self, stmts: 'Sequence[PyStmt] | None' = None) -> 'PyModule':
        if stmts is None:
            stmts = self.stmts
        return PyModule(stmts=stmts)

    def parent(self) -> 'PyModuleParent':
        raise AssertionError('trying to access the parent node of a top-level node')


type PyPattern = PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern


def is_py_pattern(value: Any) -> TypeGuard[PyPattern]:
    return isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern)


type PyExpr = PyAttrExpr | PyCallExpr | PyConstExpr | PyEllipsisExpr | PyGeneratorExpr | PyInfixExpr | PyListExpr | PyNamedExpr | PyNestExpr | PyPrefixExpr | PyStarredExpr | PySubscriptExpr | PyTupleExpr


def is_py_expr(value: Any) -> TypeGuard[PyExpr]:
    return isinstance(value, PyAttrExpr) or isinstance(value, PyCallExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyEllipsisExpr) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyListExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyTupleExpr)


type PyArg = PyKeywordArg | PyExpr


def is_py_arg(value: Any) -> TypeGuard[PyArg]:
    return isinstance(value, PyKeywordArg) or is_py_expr(value)


type PyPrefixOp = PyNotKeyword | PyPlus | PyHyphen | PyTilde


def is_py_prefix_op(value: Any) -> TypeGuard[PyPrefixOp]:
    return isinstance(value, PyNotKeyword) or isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyTilde)


type PyInfixOp = PyPlus | PyHyphen | PyAsterisk | PySlash | PySlashSlash | PyPercent | PyLessThanLessThan | PyGreaterThanGreaterThan | PyVerticalBar | PyCaret | PyAmpersand | PyAtSign | PyOrKeyword | PyAndKeyword | PyEqualsEquals | PyExclamationMarkEquals | PyLessThan | PyLessThanEquals | PyGreaterThan | PyGreaterThanEquals | PyIsKeyword | tuple[PyIsKeyword, PyNotKeyword] | PyInKeyword | tuple[PyNotKeyword, PyInKeyword]


def is_py_infix_op(value: Any) -> TypeGuard[PyInfixOp]:
    return isinstance(value, PyPlus) or isinstance(value, PyHyphen) or isinstance(value, PyAsterisk) or isinstance(value, PySlash) or isinstance(value, PySlashSlash) or isinstance(value, PyPercent) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyVerticalBar) or isinstance(value, PyCaret) or isinstance(value, PyAmpersand) or isinstance(value, PyAtSign) or isinstance(value, PyOrKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyEqualsEquals) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyLessThan) or isinstance(value, PyLessThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyIsKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyIsKeyword) and isinstance(value[1], PyNotKeyword)) or isinstance(value, PyInKeyword) or (isinstance(value, tuple) and isinstance(value[0], PyNotKeyword) and isinstance(value[1], PyInKeyword))


type PyPath = PyAbsolutePath | PyRelativePath


def is_py_path(value: Any) -> TypeGuard[PyPath]:
    return isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath)


type PyStmt = PyAssignStmt | PyBreakStmt | PyClassDef | PyContinueStmt | PyDeleteStmt | PyExprStmt | PyForStmt | PyFuncDef | PyGlobalStmt | PyIfStmt | PyImportStmt | PyImportFromStmt | PyNonlocalStmt | PyPassStmt | PyRaiseStmt | PyRetStmt | PyTryStmt | PyTypeAliasStmt | PyWhileStmt


def is_py_stmt(value: Any) -> TypeGuard[PyStmt]:
    return isinstance(value, PyAssignStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyClassDef) or isinstance(value, PyContinueStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyForStmt) or isinstance(value, PyFuncDef) or isinstance(value, PyGlobalStmt) or isinstance(value, PyIfStmt) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyNonlocalStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyTryStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyWhileStmt)


type PyParam = PyRestPosParam | PyRestKeywordParam | PyPosSepParam | PyKwSepParam | PyNamedParam


def is_py_param(value: Any) -> TypeGuard[PyParam]:
    return isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PyPosSepParam) or isinstance(value, PyKwSepParam) or isinstance(value, PyNamedParam)


type PyKeyword = PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyNonlocalKeyword | PyIsKeyword | PyInKeyword | PyImportKeyword | PyIfKeyword | PyGlobalKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword


def is_py_keyword(value: Any) -> TypeGuard[PyKeyword]:
    return isinstance(value, PyWhileKeyword) or isinstance(value, PyTypeKeyword) or isinstance(value, PyTryKeyword) or isinstance(value, PyReturnKeyword) or isinstance(value, PyRaiseKeyword) or isinstance(value, PyPassKeyword) or isinstance(value, PyOrKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyNonlocalKeyword) or isinstance(value, PyIsKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyImportKeyword) or isinstance(value, PyIfKeyword) or isinstance(value, PyGlobalKeyword) or isinstance(value, PyFromKeyword) or isinstance(value, PyForKeyword) or isinstance(value, PyFinallyKeyword) or isinstance(value, PyExceptKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyElifKeyword) or isinstance(value, PyDelKeyword) or isinstance(value, PyDefKeyword) or isinstance(value, PyContinueKeyword) or isinstance(value, PyClassKeyword) or isinstance(value, PyBreakKeyword) or isinstance(value, PyAsyncKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyAndKeyword)


type PyToken = PyIdent | PyFloat | PyInteger | PyString | PyTilde | PyVerticalBar | PyWhileKeyword | PyTypeKeyword | PyTryKeyword | PyReturnKeyword | PyRaiseKeyword | PyPassKeyword | PyOrKeyword | PyNotKeyword | PyNonlocalKeyword | PyIsKeyword | PyInKeyword | PyImportKeyword | PyIfKeyword | PyGlobalKeyword | PyFromKeyword | PyForKeyword | PyFinallyKeyword | PyExceptKeyword | PyElseKeyword | PyElifKeyword | PyDelKeyword | PyDefKeyword | PyContinueKeyword | PyClassKeyword | PyBreakKeyword | PyAsyncKeyword | PyAsKeyword | PyAndKeyword | PyCaret | PyCloseBracket | PyOpenBracket | PyAtSign | PyGreaterThanGreaterThan | PyGreaterThanEquals | PyGreaterThan | PyEqualsEquals | PyEquals | PyLessThanEquals | PyLessThanLessThan | PyLessThan | PySemicolon | PyColon | PySlashSlash | PySlash | PyDotDotDot | PyDot | PyRArrow | PyHyphen | PyComma | PyPlus | PyAsteriskAsterisk | PyAsterisk | PyCloseParen | PyOpenParen | PyAmpersand | PyPercent | PyHashtag | PyExclamationMarkEquals | PyCarriageReturnLineFeed | PyLineFeed


def is_py_token(value: Any) -> TypeGuard[PyToken]:
    return isinstance(value, PyIdent) or isinstance(value, PyFloat) or isinstance(value, PyInteger) or isinstance(value, PyString) or isinstance(value, PyTilde) or isinstance(value, PyVerticalBar) or isinstance(value, PyWhileKeyword) or isinstance(value, PyTypeKeyword) or isinstance(value, PyTryKeyword) or isinstance(value, PyReturnKeyword) or isinstance(value, PyRaiseKeyword) or isinstance(value, PyPassKeyword) or isinstance(value, PyOrKeyword) or isinstance(value, PyNotKeyword) or isinstance(value, PyNonlocalKeyword) or isinstance(value, PyIsKeyword) or isinstance(value, PyInKeyword) or isinstance(value, PyImportKeyword) or isinstance(value, PyIfKeyword) or isinstance(value, PyGlobalKeyword) or isinstance(value, PyFromKeyword) or isinstance(value, PyForKeyword) or isinstance(value, PyFinallyKeyword) or isinstance(value, PyExceptKeyword) or isinstance(value, PyElseKeyword) or isinstance(value, PyElifKeyword) or isinstance(value, PyDelKeyword) or isinstance(value, PyDefKeyword) or isinstance(value, PyContinueKeyword) or isinstance(value, PyClassKeyword) or isinstance(value, PyBreakKeyword) or isinstance(value, PyAsyncKeyword) or isinstance(value, PyAsKeyword) or isinstance(value, PyAndKeyword) or isinstance(value, PyCaret) or isinstance(value, PyCloseBracket) or isinstance(value, PyOpenBracket) or isinstance(value, PyAtSign) or isinstance(value, PyGreaterThanGreaterThan) or isinstance(value, PyGreaterThanEquals) or isinstance(value, PyGreaterThan) or isinstance(value, PyEqualsEquals) or isinstance(value, PyEquals) or isinstance(value, PyLessThanEquals) or isinstance(value, PyLessThanLessThan) or isinstance(value, PyLessThan) or isinstance(value, PySemicolon) or isinstance(value, PyColon) or isinstance(value, PySlashSlash) or isinstance(value, PySlash) or isinstance(value, PyDotDotDot) or isinstance(value, PyDot) or isinstance(value, PyRArrow) or isinstance(value, PyHyphen) or isinstance(value, PyComma) or isinstance(value, PyPlus) or isinstance(value, PyAsteriskAsterisk) or isinstance(value, PyAsterisk) or isinstance(value, PyCloseParen) or isinstance(value, PyOpenParen) or isinstance(value, PyAmpersand) or isinstance(value, PyPercent) or isinstance(value, PyHashtag) or isinstance(value, PyExclamationMarkEquals) or isinstance(value, PyCarriageReturnLineFeed) or isinstance(value, PyLineFeed)


type PyNode = PySlice | PyNamedPattern | PyAttrPattern | PySubscriptPattern | PyStarredPattern | PyListPattern | PyTuplePattern | PyEllipsisExpr | PyGuard | PyComprehension | PyGeneratorExpr | PyConstExpr | PyNestExpr | PyNamedExpr | PyAttrExpr | PySubscriptExpr | PyStarredExpr | PyListExpr | PyTupleExpr | PyKeywordArg | PyCallExpr | PyPrefixExpr | PyInfixExpr | PyQualName | PyAbsolutePath | PyRelativePath | PyAlias | PyFromAlias | PyImportStmt | PyImportFromStmt | PyRetStmt | PyExprStmt | PyAssignStmt | PyPassStmt | PyGlobalStmt | PyNonlocalStmt | PyIfCase | PyElifCase | PyElseCase | PyIfStmt | PyDeleteStmt | PyRaiseStmt | PyForStmt | PyWhileStmt | PyBreakStmt | PyContinueStmt | PyTypeAliasStmt | PyExceptHandler | PyTryStmt | PyClassDef | PyNamedParam | PyRestPosParam | PyRestKeywordParam | PyPosSepParam | PyKwSepParam | PyDecorator | PyFuncDef | PyModule


def is_py_node(value: Any) -> TypeGuard[PyNode]:
    return isinstance(value, PySlice) or isinstance(value, PyNamedPattern) or isinstance(value, PyAttrPattern) or isinstance(value, PySubscriptPattern) or isinstance(value, PyStarredPattern) or isinstance(value, PyListPattern) or isinstance(value, PyTuplePattern) or isinstance(value, PyEllipsisExpr) or isinstance(value, PyGuard) or isinstance(value, PyComprehension) or isinstance(value, PyGeneratorExpr) or isinstance(value, PyConstExpr) or isinstance(value, PyNestExpr) or isinstance(value, PyNamedExpr) or isinstance(value, PyAttrExpr) or isinstance(value, PySubscriptExpr) or isinstance(value, PyStarredExpr) or isinstance(value, PyListExpr) or isinstance(value, PyTupleExpr) or isinstance(value, PyKeywordArg) or isinstance(value, PyCallExpr) or isinstance(value, PyPrefixExpr) or isinstance(value, PyInfixExpr) or isinstance(value, PyQualName) or isinstance(value, PyAbsolutePath) or isinstance(value, PyRelativePath) or isinstance(value, PyAlias) or isinstance(value, PyFromAlias) or isinstance(value, PyImportStmt) or isinstance(value, PyImportFromStmt) or isinstance(value, PyRetStmt) or isinstance(value, PyExprStmt) or isinstance(value, PyAssignStmt) or isinstance(value, PyPassStmt) or isinstance(value, PyGlobalStmt) or isinstance(value, PyNonlocalStmt) or isinstance(value, PyIfCase) or isinstance(value, PyElifCase) or isinstance(value, PyElseCase) or isinstance(value, PyIfStmt) or isinstance(value, PyDeleteStmt) or isinstance(value, PyRaiseStmt) or isinstance(value, PyForStmt) or isinstance(value, PyWhileStmt) or isinstance(value, PyBreakStmt) or isinstance(value, PyContinueStmt) or isinstance(value, PyTypeAliasStmt) or isinstance(value, PyExceptHandler) or isinstance(value, PyTryStmt) or isinstance(value, PyClassDef) or isinstance(value, PyNamedParam) or isinstance(value, PyRestPosParam) or isinstance(value, PyRestKeywordParam) or isinstance(value, PyPosSepParam) or isinstance(value, PyKwSepParam) or isinstance(value, PyDecorator) or isinstance(value, PyFuncDef) or isinstance(value, PyModule)


type PySyntax = PyNode | PyToken


def is_py_syntax(value: Any) -> TypeGuard[PySyntax]:
    return is_py_node(value) or is_py_token(value)


type PySliceParent = PySubscriptExpr | PySubscriptPattern


type PyNamedPatternParent = PyAssignStmt | PyAttrPattern | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyAttrPatternParent = PyAssignStmt | PyAttrPattern | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PySubscriptPatternParent = PyAssignStmt | PyAttrPattern | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyStarredPatternParent = PyAssignStmt | PyAttrPattern | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyListPatternParent = PyAssignStmt | PyAttrPattern | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyTuplePatternParent = PyAssignStmt | PyAttrPattern | PyComprehension | PyDeleteStmt | PyForStmt | PyListPattern | PyNamedParam | PySubscriptPattern | PyTuplePattern


type PyEllipsisExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyGuardParent = PyComprehension


type PyComprehensionParent = PyGeneratorExpr


type PyGeneratorExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyConstExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyNestExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyNamedExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyAttrExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PySubscriptExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyStarredExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyListExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyTupleExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyKeywordArgParent = PyCallExpr


type PyCallExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyPrefixExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyInfixExprParent = PyAssignStmt | PyAttrExpr | PyCallExpr | PyComprehension | PyDecorator | PyElifCase | PyExceptHandler | PyExprStmt | PyForStmt | PyFuncDef | PyGeneratorExpr | PyGuard | PyIfCase | PyInfixExpr | PyKeywordArg | PyListExpr | PyNamedParam | PyNestExpr | PyPrefixExpr | PyRaiseStmt | PyRetStmt | PySlice | PyStarredExpr | PyStarredPattern | PySubscriptExpr | PyTupleExpr | PyTypeAliasStmt | PyWhileStmt


type PyQualNameParent = PyAbsolutePath | PyRelativePath


type PyAbsolutePathParent = PyAlias | PyImportFromStmt


type PyRelativePathParent = PyAlias | PyImportFromStmt


type PyAliasParent = PyImportStmt


type PyFromAliasParent = PyImportFromStmt


type PyImportStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyImportFromStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyRetStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


type PyExprStmtParent = PyClassDef | PyElifCase | PyElseCase | PyExceptHandler | PyForStmt | PyFuncDef | PyIfCase | PyModule | PyTryStmt | PyWhileStmt


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
def _coerce_node_alias_to_node_alias(value: 'PyAlias') -> 'PyAlias':
    return value


@no_type_check
def _coerce_union_3_list_node_alias_required_list_tuple_2_node_alias_union_2_token_comma_none_required_punct_node_alias_token_comma_required_to_punct_node_alias_token_comma_required(value: 'Sequence[PyAlias] | Sequence[tuple[PyAlias, PyComma | None]] | Punctuated[PyAlias, PyComma]') -> 'Punctuated[PyAlias, PyComma]':
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
                new_element_value = _coerce_node_alias_to_node_alias(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_node_alias_to_node_alias(element_value)
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
def _coerce_node_from_alias_to_node_from_alias(value: 'PyFromAlias') -> 'PyFromAlias':
    return value


@no_type_check
def _coerce_union_3_list_node_from_alias_required_list_tuple_2_node_from_alias_union_2_token_comma_none_required_punct_node_from_alias_token_comma_required_to_punct_node_from_alias_token_comma_required(value: 'Sequence[PyFromAlias] | Sequence[tuple[PyFromAlias, PyComma | None]] | Punctuated[PyFromAlias, PyComma]') -> 'Punctuated[PyFromAlias, PyComma]':
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
                new_element_value = _coerce_node_from_alias_to_node_from_alias(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_node_from_alias_to_node_from_alias(element_value)
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
def _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(value: 'PyStmt | Sequence[PyStmt]') -> 'PyStmt | Sequence[PyStmt]':
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
def _coerce_union_2_token_else_keyword_none_to_token_else_keyword(value: 'PyElseKeyword | None') -> 'PyElseKeyword':
    if value is None:
        return PyElseKeyword()
    elif isinstance(value, PyElseKeyword):
        return value
    else:
        raise ValueError('the coercion from PyElseKeyword | None to PyElseKeyword failed')


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
def _coerce_union_4_node_else_case_variant_stmt_list_variant_stmt_none_to_union_2_node_else_case_none(value: 'PyElseCase | PyStmt | Sequence[PyStmt] | None') -> 'PyElseCase | None':
    if is_py_stmt(value) or isinstance(value, list):
        return PyElseCase(_coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(value))
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
def _coerce_union_4_variant_stmt_tuple_3_union_2_token_else_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_list_variant_stmt_none_to_union_2_tuple_3_token_else_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_none(value: 'PyStmt | tuple[PyElseKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None') -> 'tuple[PyElseKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None':
    if is_py_stmt(value) or isinstance(value, list):
        return (PyElseKeyword(), PyColon(), _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_else_keyword_none_to_token_else_keyword(value[0]), _coerce_union_2_token_colon_none_to_token_colon(value[1]), _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(value[2]))
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
def _coerce_union_4_variant_stmt_tuple_3_union_2_token_finally_keyword_none_union_2_token_colon_none_union_2_variant_stmt_list_variant_stmt_list_variant_stmt_none_to_union_2_tuple_3_token_finally_keyword_token_colon_union_2_variant_stmt_list_variant_stmt_none(value: 'PyStmt | tuple[PyFinallyKeyword | None, PyColon | None, PyStmt | Sequence[PyStmt]] | Sequence[PyStmt] | None') -> 'tuple[PyFinallyKeyword, PyColon, PyStmt | Sequence[PyStmt]] | None':
    if is_py_stmt(value) or isinstance(value, list):
        return (PyFinallyKeyword(), PyColon(), _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_finally_keyword_none_to_token_finally_keyword(value[0]), _coerce_union_2_token_colon_none_to_token_colon(value[1]), _coerce_union_2_variant_stmt_list_variant_stmt_to_union_2_variant_stmt_list_variant_stmt(value[2]))
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
def _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_to_punct_token_ident_token_comma(value: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma]') -> 'Punctuated[PyIdent, PyComma]':
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
def _coerce_union_4_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_none_to_punct_token_ident_token_comma(value: 'Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None') -> 'Punctuated[PyIdent, PyComma]':
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
    else:
        raise ValueError('the coercion from Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None to Punctuated[PyIdent, PyComma] failed')


@no_type_check
def _coerce_union_5_tuple_3_union_2_token_open_paren_none_union_4_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_none_union_2_token_close_paren_none_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_none_to_union_2_tuple_3_token_open_paren_punct_token_ident_token_comma_token_close_paren_none(value: 'tuple[PyOpenParen | None, Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None, PyCloseParen | None] | Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None') -> 'tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (PyOpenParen(), _coerce_union_3_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_to_punct_token_ident_token_comma(value), PyCloseParen())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_open_paren_none_to_token_open_paren(value[0]), _coerce_union_4_list_tuple_2_union_2_token_ident_extern_string_union_2_token_comma_none_list_union_2_token_ident_extern_string_punct_union_2_token_ident_extern_string_token_comma_none_to_punct_token_ident_token_comma(value[1]), _coerce_union_2_token_close_paren_none_to_token_close_paren(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[PyOpenParen | None, Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None, PyCloseParen | None] | Sequence[tuple[PyIdent | str, PyComma | None]] | Sequence[PyIdent | str] | Punctuated[PyIdent | str, PyComma] | None to tuple[PyOpenParen, Punctuated[PyIdent, PyComma], PyCloseParen] | None failed')


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


