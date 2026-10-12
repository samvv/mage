from enum import IntEnum


from typing import Any, TypeGuard, TypeIs, TypedDict, Never, Unpack, Sequence, Callable, assert_never, no_type_check, cast


from magelang.runtime import BaseSyntax, Punctuated, ImmutablePunct, Span


class _RustBaseSyntax(BaseSyntax):

    pass


class _RustBaseNode(_RustBaseSyntax):

    pass


class _RustBaseToken(_RustBaseSyntax):

    def __init__(self, span: Span | None = None):
        super().__init__()
        self.span = span


class RustAmpersand(_RustBaseToken):

    pass


def is_rust_ampersand(value: Any) -> TypeIs[RustAmpersand]:
    return isinstance(value, RustAmpersand)


class RustAsKeyword(_RustBaseToken):

    pass


def is_rust_as_keyword(value: Any) -> TypeIs[RustAsKeyword]:
    return isinstance(value, RustAsKeyword)


class RustAsterisk(_RustBaseToken):

    pass


def is_rust_asterisk(value: Any) -> TypeIs[RustAsterisk]:
    return isinstance(value, RustAsterisk)


class RustAsyncKeyword(_RustBaseToken):

    pass


def is_rust_async_keyword(value: Any) -> TypeIs[RustAsyncKeyword]:
    return isinstance(value, RustAsyncKeyword)


class RustAtSign(_RustBaseToken):

    pass


def is_rust_at_sign(value: Any) -> TypeIs[RustAtSign]:
    return isinstance(value, RustAtSign)


class RustChar(_RustBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_rust_char(value: Any) -> TypeIs[RustChar]:
    return isinstance(value, RustChar)


class RustCloseBrace(_RustBaseToken):

    pass


def is_rust_close_brace(value: Any) -> TypeIs[RustCloseBrace]:
    return isinstance(value, RustCloseBrace)


class RustCloseBracket(_RustBaseToken):

    pass


def is_rust_close_bracket(value: Any) -> TypeIs[RustCloseBracket]:
    return isinstance(value, RustCloseBracket)


class RustCloseParen(_RustBaseToken):

    pass


def is_rust_close_paren(value: Any) -> TypeIs[RustCloseParen]:
    return isinstance(value, RustCloseParen)


class RustColon(_RustBaseToken):

    pass


def is_rust_colon(value: Any) -> TypeIs[RustColon]:
    return isinstance(value, RustColon)


class RustColonColon(_RustBaseToken):

    pass


def is_rust_colon_colon(value: Any) -> TypeIs[RustColonColon]:
    return isinstance(value, RustColonColon)


class RustComma(_RustBaseToken):

    pass


def is_rust_comma(value: Any) -> TypeIs[RustComma]:
    return isinstance(value, RustComma)


class RustConstKeyword(_RustBaseToken):

    pass


def is_rust_const_keyword(value: Any) -> TypeIs[RustConstKeyword]:
    return isinstance(value, RustConstKeyword)


class RustDefaultKeyword(_RustBaseToken):

    pass


def is_rust_default_keyword(value: Any) -> TypeIs[RustDefaultKeyword]:
    return isinstance(value, RustDefaultKeyword)


class RustDotDotDot(_RustBaseToken):

    pass


def is_rust_dot_dot_dot(value: Any) -> TypeIs[RustDotDotDot]:
    return isinstance(value, RustDotDotDot)


class RustEnumKeyword(_RustBaseToken):

    pass


def is_rust_enum_keyword(value: Any) -> TypeIs[RustEnumKeyword]:
    return isinstance(value, RustEnumKeyword)


class RustEquals(_RustBaseToken):

    pass


def is_rust_equals(value: Any) -> TypeIs[RustEquals]:
    return isinstance(value, RustEquals)


class RustExclamationMark(_RustBaseToken):

    pass


def is_rust_exclamation_mark(value: Any) -> TypeIs[RustExclamationMark]:
    return isinstance(value, RustExclamationMark)


class RustExternKeyword(_RustBaseToken):

    pass


def is_rust_extern_keyword(value: Any) -> TypeIs[RustExternKeyword]:
    return isinstance(value, RustExternKeyword)


class RustFalseKeyword(_RustBaseToken):

    pass


def is_rust_false_keyword(value: Any) -> TypeIs[RustFalseKeyword]:
    return isinstance(value, RustFalseKeyword)


class RustFloat(_RustBaseToken):

    def __init__(self, value: float, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_rust_float(value: Any) -> TypeIs[RustFloat]:
    return isinstance(value, RustFloat)


class RustFnKeyword(_RustBaseToken):

    pass


def is_rust_fn_keyword(value: Any) -> TypeIs[RustFnKeyword]:
    return isinstance(value, RustFnKeyword)


class RustForKeyword(_RustBaseToken):

    pass


def is_rust_for_keyword(value: Any) -> TypeIs[RustForKeyword]:
    return isinstance(value, RustForKeyword)


class RustGreaterThan(_RustBaseToken):

    pass


def is_rust_greater_than(value: Any) -> TypeIs[RustGreaterThan]:
    return isinstance(value, RustGreaterThan)


class RustHashtag(_RustBaseToken):

    pass


def is_rust_hashtag(value: Any) -> TypeIs[RustHashtag]:
    return isinstance(value, RustHashtag)


class RustIdent(_RustBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_rust_ident(value: Any) -> TypeIs[RustIdent]:
    return isinstance(value, RustIdent)


class RustImplKeyword(_RustBaseToken):

    pass


def is_rust_impl_keyword(value: Any) -> TypeIs[RustImplKeyword]:
    return isinstance(value, RustImplKeyword)


class RustInKeyword(_RustBaseToken):

    pass


def is_rust_in_keyword(value: Any) -> TypeIs[RustInKeyword]:
    return isinstance(value, RustInKeyword)


class RustInteger(_RustBaseToken):

    def __init__(self, value: int, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_rust_integer(value: Any) -> TypeIs[RustInteger]:
    return isinstance(value, RustInteger)


class RustLessThan(_RustBaseToken):

    pass


def is_rust_less_than(value: Any) -> TypeIs[RustLessThan]:
    return isinstance(value, RustLessThan)


class RustMutKeyword(_RustBaseToken):

    pass


def is_rust_mut_keyword(value: Any) -> TypeIs[RustMutKeyword]:
    return isinstance(value, RustMutKeyword)


class RustOpenBrace(_RustBaseToken):

    pass


def is_rust_open_brace(value: Any) -> TypeIs[RustOpenBrace]:
    return isinstance(value, RustOpenBrace)


class RustOpenBracket(_RustBaseToken):

    pass


def is_rust_open_bracket(value: Any) -> TypeIs[RustOpenBracket]:
    return isinstance(value, RustOpenBracket)


class RustOpenParen(_RustBaseToken):

    pass


def is_rust_open_paren(value: Any) -> TypeIs[RustOpenParen]:
    return isinstance(value, RustOpenParen)


class RustPercent(_RustBaseToken):

    pass


def is_rust_percent(value: Any) -> TypeIs[RustPercent]:
    return isinstance(value, RustPercent)


class RustPlus(_RustBaseToken):

    pass


def is_rust_plus(value: Any) -> TypeIs[RustPlus]:
    return isinstance(value, RustPlus)


class RustPubKeyword(_RustBaseToken):

    pass


def is_rust_pub_keyword(value: Any) -> TypeIs[RustPubKeyword]:
    return isinstance(value, RustPubKeyword)


class RustQuestionMark(_RustBaseToken):

    pass


def is_rust_question_mark(value: Any) -> TypeIs[RustQuestionMark]:
    return isinstance(value, RustQuestionMark)


class RustRArrow(_RustBaseToken):

    pass


def is_rust_r_arrow(value: Any) -> TypeIs[RustRArrow]:
    return isinstance(value, RustRArrow)


class RustRefKeyword(_RustBaseToken):

    pass


def is_rust_ref_keyword(value: Any) -> TypeIs[RustRefKeyword]:
    return isinstance(value, RustRefKeyword)


class RustReturnKeyword(_RustBaseToken):

    pass


def is_rust_return_keyword(value: Any) -> TypeIs[RustReturnKeyword]:
    return isinstance(value, RustReturnKeyword)


class RustSelfKeyword(_RustBaseToken):

    pass


def is_rust_self_keyword(value: Any) -> TypeIs[RustSelfKeyword]:
    return isinstance(value, RustSelfKeyword)


class RustSemicolon(_RustBaseToken):

    pass


def is_rust_semicolon(value: Any) -> TypeIs[RustSemicolon]:
    return isinstance(value, RustSemicolon)


class RustSingleQuote(_RustBaseToken):

    pass


def is_rust_single_quote(value: Any) -> TypeIs[RustSingleQuote]:
    return isinstance(value, RustSingleQuote)


class RustString(_RustBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


def is_rust_string(value: Any) -> TypeIs[RustString]:
    return isinstance(value, RustString)


class RustStructKeyword(_RustBaseToken):

    pass


def is_rust_struct_keyword(value: Any) -> TypeIs[RustStructKeyword]:
    return isinstance(value, RustStructKeyword)


class RustTrueKeyword(_RustBaseToken):

    pass


def is_rust_true_keyword(value: Any) -> TypeIs[RustTrueKeyword]:
    return isinstance(value, RustTrueKeyword)


class RustUnsafeKeyword(_RustBaseToken):

    pass


def is_rust_unsafe_keyword(value: Any) -> TypeIs[RustUnsafeKeyword]:
    return isinstance(value, RustUnsafeKeyword)


class RustUseKeyword(_RustBaseToken):

    pass


def is_rust_use_keyword(value: Any) -> TypeIs[RustUseKeyword]:
    return isinstance(value, RustUseKeyword)


class RustWhereKeyword(_RustBaseToken):

    pass


def is_rust_where_keyword(value: Any) -> TypeIs[RustWhereKeyword]:
    return isinstance(value, RustWhereKeyword)


class RustAbiDeriveKwargs(TypedDict, total=False):

    extern_keyword: 'RustExternKeyword | None'

    name: 'RustString | str'


class RustAbi(_RustBaseNode):

    _fields_ = ('extern_keyword', 'name')

    def __init__(self, name: 'RustString | str', *, extern_keyword: 'RustExternKeyword | None' = None) -> None:
        self.extern_keyword: RustExternKeyword = _coerce_0(extern_keyword)
        self.name: RustString = _coerce_1(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustAbiDeriveKwargs]) -> 'RustAbi':
        extern_keyword = _coerce_0(kwargs['extern_keyword']) if 'extern_keyword' in kwargs else self.extern_keyword
        name = _coerce_1(kwargs['name']) if 'name' in kwargs else self.name
        return RustAbi(extern_keyword=extern_keyword, name=name)

    @property
    def parent(self) -> 'RustAbiParent':
        assert(self._parent is not None)
        return cast(RustAbiParent, self._parent)


def is_rust_abi(value: Any) -> TypeIs[RustAbi]:
    return isinstance(value, RustAbi)


class RustAngleBracketedGenericArgumentsDeriveKwargs(TypedDict, total=False):

    less_than: 'RustLessThan | None'

    args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | ImmutablePunct[RustGenericArgument, RustComma] | None'

    greater_than: 'RustGreaterThan | None'


class RustAngleBracketedGenericArguments(_RustBaseNode):

    _fields_ = ('less_than', 'args', 'greater_than')

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, *, less_than: 'RustLessThan | None' = None, args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | ImmutablePunct[RustGenericArgument, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.less_than: RustLessThan = _coerce_2(less_than)
        self.args: Punctuated[RustGenericArgument, RustComma] = _coerce_5(args)
        self.greater_than: RustGreaterThan = _coerce_6(greater_than)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustAngleBracketedGenericArgumentsDeriveKwargs]) -> 'RustAngleBracketedGenericArguments':
        less_than = _coerce_2(kwargs['less_than']) if 'less_than' in kwargs else self.less_than
        args = _coerce_5(kwargs['args']) if 'args' in kwargs else self.args
        greater_than = _coerce_6(kwargs['greater_than']) if 'greater_than' in kwargs else self.greater_than
        return RustAngleBracketedGenericArguments(less_than=less_than, args=args, greater_than=greater_than)

    @property
    def parent(self) -> 'RustAngleBracketedGenericArgumentsParent':
        assert(self._parent is not None)
        return cast(RustAngleBracketedGenericArgumentsParent, self._parent)


def is_rust_angle_bracketed_generic_arguments(value: Any) -> TypeIs[RustAngleBracketedGenericArguments]:
    return isinstance(value, RustAngleBracketedGenericArguments)


class RustArrayTypeExprDeriveKwargs(TypedDict, total=False):

    open_bracket: 'RustOpenBracket | None'

    type_expr: 'RustTypeExpr'

    semicolon: 'RustSemicolon | None'

    expr: 'RustExpr'

    close_bracket: 'RustCloseBracket | None'


class RustArrayTypeExpr(_RustBaseNode):

    _fields_ = ('open_bracket', 'type_expr', 'semicolon', 'expr', 'close_bracket')

    def __init__(self, type_expr: 'RustTypeExpr', expr: 'RustExpr', *, open_bracket: 'RustOpenBracket | None' = None, semicolon: 'RustSemicolon | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.open_bracket: RustOpenBracket = _coerce_7(open_bracket)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)
        self.semicolon: RustSemicolon = _coerce_9(semicolon)
        self.expr: RustExpr = _coerce_10(expr)
        self.close_bracket: RustCloseBracket = _coerce_11(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustArrayTypeExprDeriveKwargs]) -> 'RustArrayTypeExpr':
        open_bracket = _coerce_7(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        semicolon = _coerce_9(kwargs['semicolon']) if 'semicolon' in kwargs else self.semicolon
        expr = _coerce_10(kwargs['expr']) if 'expr' in kwargs else self.expr
        close_bracket = _coerce_11(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return RustArrayTypeExpr(open_bracket=open_bracket, type_expr=type_expr, semicolon=semicolon, expr=expr, close_bracket=close_bracket)

    @property
    def parent(self) -> 'RustArrayTypeExprParent':
        assert(self._parent is not None)
        return cast(RustArrayTypeExprParent, self._parent)


def is_rust_array_type_expr(value: Any) -> TypeIs[RustArrayTypeExpr]:
    return isinstance(value, RustArrayTypeExpr)


class RustAssocConstDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    generics: 'RustAngleBracketedGenericArguments | None'

    equals: 'RustEquals | None'

    expr: 'RustExpr'


class RustAssocConst(_RustBaseNode):

    _fields_ = ('name', 'generics', 'equals', 'expr')

    def __init__(self, name: 'RustIdent | str', expr: 'RustExpr', *, generics: 'RustAngleBracketedGenericArguments | None' = None, equals: 'RustEquals | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.generics: RustAngleBracketedGenericArguments | None = _coerce_13(generics)
        self.equals: RustEquals = _coerce_14(equals)
        self.expr: RustExpr = _coerce_10(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustAssocConstDeriveKwargs]) -> 'RustAssocConst':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        generics = _coerce_13(kwargs['generics']) if 'generics' in kwargs else self.generics
        equals = _coerce_14(kwargs['equals']) if 'equals' in kwargs else self.equals
        expr = _coerce_10(kwargs['expr']) if 'expr' in kwargs else self.expr
        return RustAssocConst(name=name, generics=generics, equals=equals, expr=expr)

    @property
    def parent(self) -> 'RustAssocConstParent':
        assert(self._parent is not None)
        return cast(RustAssocConstParent, self._parent)


def is_rust_assoc_const(value: Any) -> TypeIs[RustAssocConst]:
    return isinstance(value, RustAssocConst)


class RustAssocTypeDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    generics: 'RustAngleBracketedGenericArguments | None'

    equals: 'RustEquals | None'

    type_expr: 'RustTypeExpr'


class RustAssocType(_RustBaseNode):

    _fields_ = ('name', 'generics', 'equals', 'type_expr')

    def __init__(self, name: 'RustIdent | str', type_expr: 'RustTypeExpr', *, generics: 'RustAngleBracketedGenericArguments | None' = None, equals: 'RustEquals | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.generics: RustAngleBracketedGenericArguments | None = _coerce_13(generics)
        self.equals: RustEquals = _coerce_14(equals)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustAssocTypeDeriveKwargs]) -> 'RustAssocType':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        generics = _coerce_13(kwargs['generics']) if 'generics' in kwargs else self.generics
        equals = _coerce_14(kwargs['equals']) if 'equals' in kwargs else self.equals
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        return RustAssocType(name=name, generics=generics, equals=equals, type_expr=type_expr)

    @property
    def parent(self) -> 'RustAssocTypeParent':
        assert(self._parent is not None)
        return cast(RustAssocTypeParent, self._parent)


def is_rust_assoc_type(value: Any) -> TypeIs[RustAssocType]:
    return isinstance(value, RustAssocType)


class RustAttrDeriveKwargs(TypedDict, total=False):

    hashtag: 'RustHashtag | None'

    exclamation_mark: 'RustExclamationMark | None'

    open_bracket: 'RustOpenBracket | None'

    meta: 'RustMeta'

    close_bracket: 'RustCloseBracket | None'


class RustAttr(_RustBaseNode):

    _fields_ = ('hashtag', 'exclamation_mark', 'open_bracket', 'meta', 'close_bracket')

    def __init__(self, meta: 'RustMeta', *, hashtag: 'RustHashtag | None' = None, exclamation_mark: 'RustExclamationMark | None' = None, open_bracket: 'RustOpenBracket | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.hashtag: RustHashtag = _coerce_15(hashtag)
        self.exclamation_mark: RustExclamationMark | None = _coerce_16(exclamation_mark)
        self.open_bracket: RustOpenBracket = _coerce_7(open_bracket)
        self.meta: RustMeta = _coerce_17(meta)
        self.close_bracket: RustCloseBracket = _coerce_11(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustAttrDeriveKwargs]) -> 'RustAttr':
        hashtag = _coerce_15(kwargs['hashtag']) if 'hashtag' in kwargs else self.hashtag
        exclamation_mark = _coerce_16(kwargs['exclamation_mark']) if 'exclamation_mark' in kwargs else self.exclamation_mark
        open_bracket = _coerce_7(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        meta = _coerce_17(kwargs['meta']) if 'meta' in kwargs else self.meta
        close_bracket = _coerce_11(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return RustAttr(hashtag=hashtag, exclamation_mark=exclamation_mark, open_bracket=open_bracket, meta=meta, close_bracket=close_bracket)

    @property
    def parent(self) -> 'RustAttrParent':
        assert(self._parent is not None)
        return cast(RustAttrParent, self._parent)


def is_rust_attr(value: Any) -> TypeIs[RustAttr]:
    return isinstance(value, RustAttr)


class RustBlockExprDeriveKwargs(TypedDict, total=False):

    open_brace: 'RustOpenBrace | None'

    item: 'RustItem'

    semicolon: 'RustSemicolon | None'

    last: 'RustExpr'

    close_brace: 'RustCloseBrace | None'


class RustBlockExpr(_RustBaseNode):

    _fields_ = ('open_brace', 'item', 'semicolon', 'last', 'close_brace')

    def __init__(self, item: 'RustItem', last: 'RustExpr', *, open_brace: 'RustOpenBrace | None' = None, semicolon: 'RustSemicolon | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.item: RustItem = _coerce_19(item)
        self.semicolon: RustSemicolon = _coerce_9(semicolon)
        self.last: RustExpr = _coerce_10(last)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustBlockExprDeriveKwargs]) -> 'RustBlockExpr':
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        item = _coerce_19(kwargs['item']) if 'item' in kwargs else self.item
        semicolon = _coerce_9(kwargs['semicolon']) if 'semicolon' in kwargs else self.semicolon
        last = _coerce_10(kwargs['last']) if 'last' in kwargs else self.last
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustBlockExpr(open_brace=open_brace, item=item, semicolon=semicolon, last=last, close_brace=close_brace)

    @property
    def parent(self) -> 'RustBlockExprParent':
        assert(self._parent is not None)
        return cast(RustBlockExprParent, self._parent)


def is_rust_block_expr(value: Any) -> TypeIs[RustBlockExpr]:
    return isinstance(value, RustBlockExpr)


class RustBoundLifetimesDeriveKwargs(TypedDict, total=False):

    for_keyword: 'RustForKeyword | None'

    less_than: 'RustLessThan | None'

    lifetimes: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None'

    greater_than: 'RustGreaterThan | None'


class RustBoundLifetimes(_RustBaseNode):

    _fields_ = ('for_keyword', 'less_than', 'lifetimes', 'greater_than')

    def count_lifetimes(self) -> int:
        return len(self.lifetimes)

    def __init__(self, *, for_keyword: 'RustForKeyword | None' = None, less_than: 'RustLessThan | None' = None, lifetimes: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.for_keyword: RustForKeyword = _coerce_21(for_keyword)
        self.less_than: RustLessThan = _coerce_2(less_than)
        self.lifetimes: Punctuated[RustGenericParam, RustComma] = _coerce_23(lifetimes)
        self.greater_than: RustGreaterThan = _coerce_6(greater_than)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustBoundLifetimesDeriveKwargs]) -> 'RustBoundLifetimes':
        for_keyword = _coerce_21(kwargs['for_keyword']) if 'for_keyword' in kwargs else self.for_keyword
        less_than = _coerce_2(kwargs['less_than']) if 'less_than' in kwargs else self.less_than
        lifetimes = _coerce_23(kwargs['lifetimes']) if 'lifetimes' in kwargs else self.lifetimes
        greater_than = _coerce_6(kwargs['greater_than']) if 'greater_than' in kwargs else self.greater_than
        return RustBoundLifetimes(for_keyword=for_keyword, less_than=less_than, lifetimes=lifetimes, greater_than=greater_than)

    @property
    def parent(self) -> 'RustBoundLifetimesParent':
        assert(self._parent is not None)
        return cast(RustBoundLifetimesParent, self._parent)


def is_rust_bound_lifetimes(value: Any) -> TypeIs[RustBoundLifetimes]:
    return isinstance(value, RustBoundLifetimes)


class RustCallExprDeriveKwargs(TypedDict, total=False):

    operator: 'RustExpr'

    open_paren: 'RustOpenParen | None'

    args: 'Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | ImmutablePunct[RustExpr, RustComma] | None'

    close_paren: 'RustCloseParen | None'


class RustCallExpr(_RustBaseNode):

    _fields_ = ('operator', 'open_paren', 'args', 'close_paren')

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, operator: 'RustExpr', *, open_paren: 'RustOpenParen | None' = None, args: 'Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | ImmutablePunct[RustExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.operator: RustExpr = _coerce_10(operator)
        self.open_paren: RustOpenParen = _coerce_24(open_paren)
        self.args: Punctuated[RustExpr, RustComma] = _coerce_25(args)
        self.close_paren: RustCloseParen = _coerce_26(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustCallExprDeriveKwargs]) -> 'RustCallExpr':
        operator = _coerce_10(kwargs['operator']) if 'operator' in kwargs else self.operator
        open_paren = _coerce_24(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        args = _coerce_25(kwargs['args']) if 'args' in kwargs else self.args
        close_paren = _coerce_26(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return RustCallExpr(operator=operator, open_paren=open_paren, args=args, close_paren=close_paren)

    @property
    def parent(self) -> 'RustCallExprParent':
        assert(self._parent is not None)
        return cast(RustCallExprParent, self._parent)


def is_rust_call_expr(value: Any) -> TypeIs[RustCallExpr]:
    return isinstance(value, RustCallExpr)


class RustConstParamDeriveKwargs(TypedDict, total=False):

    const_keyword: 'RustConstKeyword | None'

    name: 'RustIdent | str'

    colon: 'RustColon | None'

    type_expr: 'RustTypeExpr'

    default: 'RustInit | None'


class RustConstParam(_RustBaseNode):

    _fields_ = ('const_keyword', 'name', 'colon', 'type_expr', 'default')

    def __init__(self, name: 'RustIdent | str', type_expr: 'RustTypeExpr', *, const_keyword: 'RustConstKeyword | None' = None, colon: 'RustColon | None' = None, default: 'RustInit | None' = None) -> None:
        self.const_keyword: RustConstKeyword = _coerce_27(const_keyword)
        self.name: RustIdent = _coerce_12(name)
        self.colon: RustColon = _coerce_28(colon)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)
        self.default: RustInit | None = _coerce_29(default)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustConstParamDeriveKwargs]) -> 'RustConstParam':
        const_keyword = _coerce_27(kwargs['const_keyword']) if 'const_keyword' in kwargs else self.const_keyword
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        default = _coerce_29(kwargs['default']) if 'default' in kwargs else self.default
        return RustConstParam(const_keyword=const_keyword, name=name, colon=colon, type_expr=type_expr, default=default)

    @property
    def parent(self) -> 'RustConstParamParent':
        assert(self._parent is not None)
        return cast(RustConstParamParent, self._parent)


def is_rust_const_param(value: Any) -> TypeIs[RustConstParam]:
    return isinstance(value, RustConstParam)


class RustConstraintDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    generics: 'RustAngleBracketedGenericArguments | None'

    colon: 'RustColon | None'

    bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus] | None'


class RustConstraint(_RustBaseNode):

    _fields_ = ('name', 'generics', 'colon', 'bounds')

    def count_bounds(self) -> int:
        return len(self.bounds)

    def __init__(self, name: 'RustIdent | str', *, generics: 'RustAngleBracketedGenericArguments | None' = None, colon: 'RustColon | None' = None, bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus] | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.generics: RustAngleBracketedGenericArguments = _coerce_30(generics)
        self.colon: RustColon = _coerce_28(colon)
        self.bounds: Punctuated[RustTypeParamBound, RustPlus] = _coerce_33(bounds)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustConstraintDeriveKwargs]) -> 'RustConstraint':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        generics = _coerce_30(kwargs['generics']) if 'generics' in kwargs else self.generics
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        bounds = _coerce_33(kwargs['bounds']) if 'bounds' in kwargs else self.bounds
        return RustConstraint(name=name, generics=generics, colon=colon, bounds=bounds)

    @property
    def parent(self) -> 'RustConstraintParent':
        assert(self._parent is not None)
        return cast(RustConstraintParent, self._parent)


def is_rust_constraint(value: Any) -> TypeIs[RustConstraint]:
    return isinstance(value, RustConstraint)


class RustEmptyVariantDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    init: 'RustInit | None'


class RustEmptyVariant(_RustBaseNode):

    _fields_ = ('name', 'init')

    def __init__(self, name: 'RustIdent | str', *, init: 'RustInit | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.init: RustInit | None = _coerce_29(init)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustEmptyVariantDeriveKwargs]) -> 'RustEmptyVariant':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        init = _coerce_29(kwargs['init']) if 'init' in kwargs else self.init
        return RustEmptyVariant(name=name, init=init)

    @property
    def parent(self) -> 'RustEmptyVariantParent':
        assert(self._parent is not None)
        return cast(RustEmptyVariantParent, self._parent)


def is_rust_empty_variant(value: Any) -> TypeIs[RustEmptyVariant]:
    return isinstance(value, RustEmptyVariant)


class RustEnumItemDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    visibility: 'RustPublic | None'

    enum_keyword: 'RustEnumKeyword | None'

    name: 'RustIdent | str'

    open_brace: 'RustOpenBrace | None'

    variants: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | ImmutablePunct[RustVariant, RustComma] | None'

    comma: 'RustComma | None'

    close_brace: 'RustCloseBrace | None'


class RustEnumItem(_RustBaseNode):

    _fields_ = ('attrs', 'visibility', 'enum_keyword', 'name', 'open_brace', 'variants', 'comma', 'close_brace')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_variants(self) -> int:
        return len(self.variants)

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, enum_keyword: 'RustEnumKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, variants: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | ImmutablePunct[RustVariant, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.visibility: RustPublic | None = _coerce_36(visibility)
        self.enum_keyword: RustEnumKeyword = _coerce_37(enum_keyword)
        self.name: RustIdent = _coerce_12(name)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.variants: Punctuated[RustVariant, RustComma] = _coerce_39(variants)
        self.comma: RustComma | None = _coerce_40(comma)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustEnumItemDeriveKwargs]) -> 'RustEnumItem':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        visibility = _coerce_36(kwargs['visibility']) if 'visibility' in kwargs else self.visibility
        enum_keyword = _coerce_37(kwargs['enum_keyword']) if 'enum_keyword' in kwargs else self.enum_keyword
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        variants = _coerce_39(kwargs['variants']) if 'variants' in kwargs else self.variants
        comma = _coerce_40(kwargs['comma']) if 'comma' in kwargs else self.comma
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustEnumItem(attrs=attrs, visibility=visibility, enum_keyword=enum_keyword, name=name, open_brace=open_brace, variants=variants, comma=comma, close_brace=close_brace)

    @property
    def parent(self) -> 'RustEnumItemParent':
        assert(self._parent is not None)
        return cast(RustEnumItemParent, self._parent)


def is_rust_enum_item(value: Any) -> TypeIs[RustEnumItem]:
    return isinstance(value, RustEnumItem)


class RustExprItemDeriveKwargs(TypedDict, total=False):

    expr: 'RustExpr'


class RustExprItem(_RustBaseNode):

    _fields_ = ('expr', )

    def __init__(self, expr: 'RustExpr') -> None:
        self.expr: RustExpr = _coerce_10(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustExprItemDeriveKwargs]) -> 'RustExprItem':
        expr = _coerce_10(kwargs['expr']) if 'expr' in kwargs else self.expr
        return RustExprItem(expr=expr)

    @property
    def parent(self) -> 'RustExprItemParent':
        assert(self._parent is not None)
        return cast(RustExprItemParent, self._parent)


def is_rust_expr_item(value: Any) -> TypeIs[RustExprItem]:
    return isinstance(value, RustExprItem)


class RustFieldDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    colon: 'RustColon | None'

    type_expr: 'RustTypeExpr'


class RustField(_RustBaseNode):

    _fields_ = ('name', 'colon', 'type_expr')

    def __init__(self, name: 'RustIdent | str', type_expr: 'RustTypeExpr', *, colon: 'RustColon | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.colon: RustColon = _coerce_28(colon)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustFieldDeriveKwargs]) -> 'RustField':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        return RustField(name=name, colon=colon, type_expr=type_expr)

    @property
    def parent(self) -> 'RustFieldParent':
        assert(self._parent is not None)
        return cast(RustFieldParent, self._parent)


def is_rust_field(value: Any) -> TypeIs[RustField]:
    return isinstance(value, RustField)


class RustFnImplElementDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    visibility: 'RustPublic | None'

    default_keyword: 'RustDefaultKeyword | None'

    signature: 'RustSignature'

    open_brace: 'RustOpenBrace | None'

    item: 'RustItem'

    semicolon: 'RustSemicolon | None'

    last: 'RustExpr'

    close_brace: 'RustCloseBrace | None'


class RustFnImplElement(_RustBaseNode):

    _fields_ = ('attrs', 'visibility', 'default_keyword', 'signature', 'open_brace', 'item', 'semicolon', 'last', 'close_brace')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, signature: 'RustSignature', item: 'RustItem', last: 'RustExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, default_keyword: 'RustDefaultKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, semicolon: 'RustSemicolon | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.visibility: RustPublic | None = _coerce_36(visibility)
        self.default_keyword: RustDefaultKeyword | None = _coerce_41(default_keyword)
        self.signature: RustSignature = _coerce_42(signature)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.item: RustItem = _coerce_19(item)
        self.semicolon: RustSemicolon = _coerce_9(semicolon)
        self.last: RustExpr = _coerce_10(last)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustFnImplElementDeriveKwargs]) -> 'RustFnImplElement':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        visibility = _coerce_36(kwargs['visibility']) if 'visibility' in kwargs else self.visibility
        default_keyword = _coerce_41(kwargs['default_keyword']) if 'default_keyword' in kwargs else self.default_keyword
        signature = _coerce_42(kwargs['signature']) if 'signature' in kwargs else self.signature
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        item = _coerce_19(kwargs['item']) if 'item' in kwargs else self.item
        semicolon = _coerce_9(kwargs['semicolon']) if 'semicolon' in kwargs else self.semicolon
        last = _coerce_10(kwargs['last']) if 'last' in kwargs else self.last
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustFnImplElement(attrs=attrs, visibility=visibility, default_keyword=default_keyword, signature=signature, open_brace=open_brace, item=item, semicolon=semicolon, last=last, close_brace=close_brace)

    @property
    def parent(self) -> 'RustFnImplElementParent':
        assert(self._parent is not None)
        return cast(RustFnImplElementParent, self._parent)


def is_rust_fn_impl_element(value: Any) -> TypeIs[RustFnImplElement]:
    return isinstance(value, RustFnImplElement)


class RustGenericsDeriveKwargs(TypedDict, total=False):

    params: 'tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None'

    where_clause: 'tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma] | None'


class RustGenerics(_RustBaseNode):

    _fields_ = ('params', 'where_clause')

    def __init__(self, *, params: 'tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None' = None, where_clause: 'tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma] | None' = None) -> None:
        self.params: tuple[RustLessThan, Punctuated[RustGenericParam, RustComma], RustGreaterThan] | None = _coerce_44(params)
        self.where_clause: tuple[RustWhereKeyword, Punctuated[RustWherePredicate, RustComma]] | None = _coerce_48(where_clause)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustGenericsDeriveKwargs]) -> 'RustGenerics':
        params = _coerce_44(kwargs['params']) if 'params' in kwargs else self.params
        where_clause = _coerce_48(kwargs['where_clause']) if 'where_clause' in kwargs else self.where_clause
        return RustGenerics(params=params, where_clause=where_clause)

    @property
    def parent(self) -> 'RustGenericsParent':
        assert(self._parent is not None)
        return cast(RustGenericsParent, self._parent)


def is_rust_generics(value: Any) -> TypeIs[RustGenerics]:
    return isinstance(value, RustGenerics)


class RustImplElementDeriveKwargs(TypedDict, total=False):

    fn_impl_element: 'RustFnImplElement'


class RustImplElement(_RustBaseNode):

    _fields_ = ('fn_impl_element', )

    def __init__(self, fn_impl_element: 'RustFnImplElement') -> None:
        self.fn_impl_element: RustFnImplElement = _coerce_49(fn_impl_element)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustImplElementDeriveKwargs]) -> 'RustImplElement':
        fn_impl_element = _coerce_49(kwargs['fn_impl_element']) if 'fn_impl_element' in kwargs else self.fn_impl_element
        return RustImplElement(fn_impl_element=fn_impl_element)

    @property
    def parent(self) -> 'RustImplElementParent':
        assert(self._parent is not None)
        return cast(RustImplElementParent, self._parent)


def is_rust_impl_element(value: Any) -> TypeIs[RustImplElement]:
    return isinstance(value, RustImplElement)


class RustImplItemDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    default_keyword: 'RustDefaultKeyword | None'

    unsafe_keyword: 'RustUnsafeKeyword | None'

    impl_keyword: 'RustImplKeyword | None'

    generics: 'RustGenerics | None'

    trait: 'RustPath | tuple[RustExclamationMark | None, RustPath, RustForKeyword | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None'

    type_expr: 'RustTypeExpr'

    open_brace: 'RustOpenBrace | None'

    impl_elements: 'Sequence[RustFnImplElement | RustImplElement] | None'

    close_brace: 'RustCloseBrace | None'


class RustImplItem(_RustBaseNode):

    _fields_ = ('attrs', 'default_keyword', 'unsafe_keyword', 'impl_keyword', 'generics', 'trait', 'type_expr', 'open_brace', 'impl_elements', 'close_brace')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_impl_elements(self) -> int:
        return len(self.impl_elements)

    def __init__(self, type_expr: 'RustTypeExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, default_keyword: 'RustDefaultKeyword | None' = None, unsafe_keyword: 'RustUnsafeKeyword | None' = None, impl_keyword: 'RustImplKeyword | None' = None, generics: 'RustGenerics | None' = None, trait: 'RustPath | tuple[RustExclamationMark | None, RustPath, RustForKeyword | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None' = None, open_brace: 'RustOpenBrace | None' = None, impl_elements: 'Sequence[RustFnImplElement | RustImplElement] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.default_keyword: RustDefaultKeyword | None = _coerce_41(default_keyword)
        self.unsafe_keyword: RustUnsafeKeyword | None = _coerce_50(unsafe_keyword)
        self.impl_keyword: RustImplKeyword = _coerce_51(impl_keyword)
        self.generics: RustGenerics = _coerce_52(generics)
        self.trait: tuple[RustExclamationMark | None, RustPath, RustForKeyword] | None = _coerce_58(trait)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.impl_elements: list[RustImplElement] = _coerce_60(impl_elements)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustImplItemDeriveKwargs]) -> 'RustImplItem':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        default_keyword = _coerce_41(kwargs['default_keyword']) if 'default_keyword' in kwargs else self.default_keyword
        unsafe_keyword = _coerce_50(kwargs['unsafe_keyword']) if 'unsafe_keyword' in kwargs else self.unsafe_keyword
        impl_keyword = _coerce_51(kwargs['impl_keyword']) if 'impl_keyword' in kwargs else self.impl_keyword
        generics = _coerce_52(kwargs['generics']) if 'generics' in kwargs else self.generics
        trait = _coerce_58(kwargs['trait']) if 'trait' in kwargs else self.trait
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        impl_elements = _coerce_60(kwargs['impl_elements']) if 'impl_elements' in kwargs else self.impl_elements
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustImplItem(attrs=attrs, default_keyword=default_keyword, unsafe_keyword=unsafe_keyword, impl_keyword=impl_keyword, generics=generics, trait=trait, type_expr=type_expr, open_brace=open_brace, impl_elements=impl_elements, close_brace=close_brace)

    @property
    def parent(self) -> 'RustImplItemParent':
        assert(self._parent is not None)
        return cast(RustImplItemParent, self._parent)


def is_rust_impl_item(value: Any) -> TypeIs[RustImplItem]:
    return isinstance(value, RustImplItem)


class RustInitDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    equals: 'RustEquals | None'

    value: 'RustExpr'


class RustInit(_RustBaseNode):

    _fields_ = ('name', 'equals', 'value')

    def __init__(self, name: 'RustIdent | str', value: 'RustExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.equals: RustEquals = _coerce_14(equals)
        self.value: RustExpr = _coerce_10(value)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustInitDeriveKwargs]) -> 'RustInit':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        equals = _coerce_14(kwargs['equals']) if 'equals' in kwargs else self.equals
        value = _coerce_10(kwargs['value']) if 'value' in kwargs else self.value
        return RustInit(name=name, equals=equals, value=value)

    @property
    def parent(self) -> 'RustInitParent':
        assert(self._parent is not None)
        return cast(RustInitParent, self._parent)


def is_rust_init(value: Any) -> TypeIs[RustInit]:
    return isinstance(value, RustInit)


class RustLifetimeDeriveKwargs(TypedDict, total=False):

    single_quote: 'RustSingleQuote | None'

    name: 'RustIdent | str'


class RustLifetime(_RustBaseNode):

    _fields_ = ('single_quote', 'name')

    def __init__(self, name: 'RustIdent | str', *, single_quote: 'RustSingleQuote | None' = None) -> None:
        self.single_quote: RustSingleQuote = _coerce_61(single_quote)
        self.name: RustIdent = _coerce_12(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustLifetimeDeriveKwargs]) -> 'RustLifetime':
        single_quote = _coerce_61(kwargs['single_quote']) if 'single_quote' in kwargs else self.single_quote
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        return RustLifetime(single_quote=single_quote, name=name)

    @property
    def parent(self) -> 'RustLifetimeParent':
        assert(self._parent is not None)
        return cast(RustLifetimeParent, self._parent)


def is_rust_lifetime(value: Any) -> TypeIs[RustLifetime]:
    return isinstance(value, RustLifetime)


class RustLifetimePredicateDeriveKwargs(TypedDict, total=False):

    lifetime: 'RustIdent | RustLifetime | str'

    colon: 'RustColon | None'

    bounds: 'Sequence[tuple[RustIdent | RustLifetime | str, RustPlus | None]] | Sequence[RustIdent | RustLifetime | str] | ImmutablePunct[RustIdent | RustLifetime | str, RustPlus]'


class RustLifetimePredicate(_RustBaseNode):

    _fields_ = ('lifetime', 'colon', 'bounds')

    def count_bounds(self) -> int:
        return len(self.bounds)

    def __init__(self, lifetime: 'RustIdent | RustLifetime | str', bounds: 'Sequence[tuple[RustIdent | RustLifetime | str, RustPlus | None]] | Sequence[RustIdent | RustLifetime | str] | ImmutablePunct[RustIdent | RustLifetime | str, RustPlus]', *, colon: 'RustColon | None' = None) -> None:
        self.lifetime: RustLifetime = _coerce_62(lifetime)
        self.colon: RustColon = _coerce_28(colon)
        self.bounds: Punctuated[RustLifetime, RustPlus] = _coerce_63(bounds)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustLifetimePredicateDeriveKwargs]) -> 'RustLifetimePredicate':
        lifetime = _coerce_62(kwargs['lifetime']) if 'lifetime' in kwargs else self.lifetime
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        bounds = _coerce_63(kwargs['bounds']) if 'bounds' in kwargs else self.bounds
        return RustLifetimePredicate(lifetime=lifetime, colon=colon, bounds=bounds)

    @property
    def parent(self) -> 'RustLifetimePredicateParent':
        assert(self._parent is not None)
        return cast(RustLifetimePredicateParent, self._parent)


def is_rust_lifetime_predicate(value: Any) -> TypeIs[RustLifetimePredicate]:
    return isinstance(value, RustLifetimePredicate)


class RustLitExprDeriveKwargs(TypedDict, total=False):

    literal: 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | float | str'


class RustLitExpr(_RustBaseNode):

    _fields_ = ('literal', )

    def __init__(self, literal: 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | float | str') -> None:
        self.literal: RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword = _coerce_64(literal)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustLitExprDeriveKwargs]) -> 'RustLitExpr':
        literal = _coerce_64(kwargs['literal']) if 'literal' in kwargs else self.literal
        return RustLitExpr(literal=literal)

    @property
    def parent(self) -> 'RustLitExprParent':
        assert(self._parent is not None)
        return cast(RustLitExprParent, self._parent)


def is_rust_lit_expr(value: Any) -> TypeIs[RustLitExpr]:
    return isinstance(value, RustLitExpr)


class RustMetaBracedDeriveKwargs(TypedDict, total=False):

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'

    open_brace: 'RustOpenBrace | None'

    tokens: 'Sequence[RustToken] | None'

    close_brace: 'RustCloseBrace | None'


class RustMetaBraced(_RustBaseNode):

    _fields_ = ('path', 'open_brace', 'tokens', 'close_brace')

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, open_brace: 'RustOpenBrace | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.path: RustPath = _coerce_56(path)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.tokens: list[RustToken] = _coerce_66(tokens)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustMetaBracedDeriveKwargs]) -> 'RustMetaBraced':
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        tokens = _coerce_66(kwargs['tokens']) if 'tokens' in kwargs else self.tokens
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustMetaBraced(path=path, open_brace=open_brace, tokens=tokens, close_brace=close_brace)

    @property
    def parent(self) -> 'RustMetaBracedParent':
        assert(self._parent is not None)
        return cast(RustMetaBracedParent, self._parent)


def is_rust_meta_braced(value: Any) -> TypeIs[RustMetaBraced]:
    return isinstance(value, RustMetaBraced)


class RustMetaBracketedDeriveKwargs(TypedDict, total=False):

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'

    open_bracket: 'RustOpenBracket | None'

    tokens: 'Sequence[RustToken] | None'

    close_bracket: 'RustCloseBracket | None'


class RustMetaBracketed(_RustBaseNode):

    _fields_ = ('path', 'open_bracket', 'tokens', 'close_bracket')

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, open_bracket: 'RustOpenBracket | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.path: RustPath = _coerce_56(path)
        self.open_bracket: RustOpenBracket = _coerce_7(open_bracket)
        self.tokens: list[RustToken] = _coerce_66(tokens)
        self.close_bracket: RustCloseBracket = _coerce_11(close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustMetaBracketedDeriveKwargs]) -> 'RustMetaBracketed':
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        open_bracket = _coerce_7(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        tokens = _coerce_66(kwargs['tokens']) if 'tokens' in kwargs else self.tokens
        close_bracket = _coerce_11(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        return RustMetaBracketed(path=path, open_bracket=open_bracket, tokens=tokens, close_bracket=close_bracket)

    @property
    def parent(self) -> 'RustMetaBracketedParent':
        assert(self._parent is not None)
        return cast(RustMetaBracketedParent, self._parent)


def is_rust_meta_bracketed(value: Any) -> TypeIs[RustMetaBracketed]:
    return isinstance(value, RustMetaBracketed)


class RustMetaNameValueDeriveKwargs(TypedDict, total=False):

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'

    equals: 'RustEquals | None'

    expr: 'RustExpr'


class RustMetaNameValue(_RustBaseNode):

    _fields_ = ('path', 'equals', 'expr')

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', expr: 'RustExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.path: RustPath = _coerce_56(path)
        self.equals: RustEquals = _coerce_14(equals)
        self.expr: RustExpr = _coerce_10(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustMetaNameValueDeriveKwargs]) -> 'RustMetaNameValue':
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        equals = _coerce_14(kwargs['equals']) if 'equals' in kwargs else self.equals
        expr = _coerce_10(kwargs['expr']) if 'expr' in kwargs else self.expr
        return RustMetaNameValue(path=path, equals=equals, expr=expr)

    @property
    def parent(self) -> 'RustMetaNameValueParent':
        assert(self._parent is not None)
        return cast(RustMetaNameValueParent, self._parent)


def is_rust_meta_name_value(value: Any) -> TypeIs[RustMetaNameValue]:
    return isinstance(value, RustMetaNameValue)


class RustMetaParenthesizedDeriveKwargs(TypedDict, total=False):

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'

    open_paren: 'RustOpenParen | None'

    tokens: 'Sequence[RustToken] | None'

    close_paren: 'RustCloseParen | None'


class RustMetaParenthesized(_RustBaseNode):

    _fields_ = ('path', 'open_paren', 'tokens', 'close_paren')

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, open_paren: 'RustOpenParen | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.path: RustPath = _coerce_56(path)
        self.open_paren: RustOpenParen = _coerce_24(open_paren)
        self.tokens: list[RustToken] = _coerce_66(tokens)
        self.close_paren: RustCloseParen = _coerce_26(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustMetaParenthesizedDeriveKwargs]) -> 'RustMetaParenthesized':
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        open_paren = _coerce_24(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        tokens = _coerce_66(kwargs['tokens']) if 'tokens' in kwargs else self.tokens
        close_paren = _coerce_26(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return RustMetaParenthesized(path=path, open_paren=open_paren, tokens=tokens, close_paren=close_paren)

    @property
    def parent(self) -> 'RustMetaParenthesizedParent':
        assert(self._parent is not None)
        return cast(RustMetaParenthesizedParent, self._parent)


def is_rust_meta_parenthesized(value: Any) -> TypeIs[RustMetaParenthesized]:
    return isinstance(value, RustMetaParenthesized)


class RustMetaPathDeriveKwargs(TypedDict, total=False):

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'


class RustMetaPath(_RustBaseNode):

    _fields_ = ('path', )

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]') -> None:
        self.path: RustPath = _coerce_56(path)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustMetaPathDeriveKwargs]) -> 'RustMetaPath':
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        return RustMetaPath(path=path)

    @property
    def parent(self) -> 'RustMetaPathParent':
        assert(self._parent is not None)
        return cast(RustMetaPathParent, self._parent)


def is_rust_meta_path(value: Any) -> TypeIs[RustMetaPath]:
    return isinstance(value, RustMetaPath)


class RustNamedPatternDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    ref_keyword: 'RustRefKeyword | None'

    mut_keyword: 'RustMutKeyword | None'

    name: 'RustIdent | str'

    sub: 'RustIdent | RustNamedPattern | RustPattern | tuple[RustAtSign | None, RustPattern] | None | str'


class RustNamedPattern(_RustBaseNode):

    _fields_ = ('attrs', 'ref_keyword', 'mut_keyword', 'name', 'sub')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, ref_keyword: 'RustRefKeyword | None' = None, mut_keyword: 'RustMutKeyword | None' = None, sub: 'RustIdent | RustNamedPattern | RustPattern | tuple[RustAtSign | None, RustPattern] | None | str' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.ref_keyword: RustRefKeyword | None = _coerce_67(ref_keyword)
        self.mut_keyword: RustMutKeyword | None = _coerce_68(mut_keyword)
        self.name: RustIdent = _coerce_12(name)
        self.sub: tuple[RustAtSign, RustPattern] | None = _coerce_73(sub)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustNamedPatternDeriveKwargs]) -> 'RustNamedPattern':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        ref_keyword = _coerce_67(kwargs['ref_keyword']) if 'ref_keyword' in kwargs else self.ref_keyword
        mut_keyword = _coerce_68(kwargs['mut_keyword']) if 'mut_keyword' in kwargs else self.mut_keyword
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        sub = _coerce_73(kwargs['sub']) if 'sub' in kwargs else self.sub
        return RustNamedPattern(attrs=attrs, ref_keyword=ref_keyword, mut_keyword=mut_keyword, name=name, sub=sub)

    @property
    def parent(self) -> 'RustNamedPatternParent':
        assert(self._parent is not None)
        return cast(RustNamedPatternParent, self._parent)


def is_rust_named_pattern(value: Any) -> TypeIs[RustNamedPattern]:
    return isinstance(value, RustNamedPattern)


class RustNeverTypeExprDeriveKwargs(TypedDict, total=False):

    exclamation_mark: 'RustExclamationMark | None'


class RustNeverTypeExpr(_RustBaseNode):

    _fields_ = ('exclamation_mark', )

    def __init__(self, *, exclamation_mark: 'RustExclamationMark | None' = None) -> None:
        self.exclamation_mark: RustExclamationMark = _coerce_74(exclamation_mark)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustNeverTypeExprDeriveKwargs]) -> 'RustNeverTypeExpr':
        exclamation_mark = _coerce_74(kwargs['exclamation_mark']) if 'exclamation_mark' in kwargs else self.exclamation_mark
        return RustNeverTypeExpr(exclamation_mark=exclamation_mark)

    @property
    def parent(self) -> 'RustNeverTypeExprParent':
        assert(self._parent is not None)
        return cast(RustNeverTypeExprParent, self._parent)


def is_rust_never_type_expr(value: Any) -> TypeIs[RustNeverTypeExpr]:
    return isinstance(value, RustNeverTypeExpr)


class RustParenthesizedGenericArgumentsDeriveKwargs(TypedDict, total=False):

    open_paren: 'RustOpenParen | None'

    params: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None'

    close_paren: 'RustCloseParen | None'

    r_arrow: 'RustRArrow | None'

    result: 'RustTypeExpr'


class RustParenthesizedGenericArguments(_RustBaseNode):

    _fields_ = ('open_paren', 'params', 'close_paren', 'r_arrow', 'result')

    def count_params(self) -> int:
        return len(self.params)

    def __init__(self, result: 'RustTypeExpr', *, open_paren: 'RustOpenParen | None' = None, params: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None, r_arrow: 'RustRArrow | None' = None) -> None:
        self.open_paren: RustOpenParen = _coerce_24(open_paren)
        self.params: Punctuated[RustTypeExpr, RustComma] = _coerce_75(params)
        self.close_paren: RustCloseParen = _coerce_26(close_paren)
        self.r_arrow: RustRArrow = _coerce_76(r_arrow)
        self.result: RustTypeExpr = _coerce_8(result)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustParenthesizedGenericArgumentsDeriveKwargs]) -> 'RustParenthesizedGenericArguments':
        open_paren = _coerce_24(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        params = _coerce_75(kwargs['params']) if 'params' in kwargs else self.params
        close_paren = _coerce_26(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        r_arrow = _coerce_76(kwargs['r_arrow']) if 'r_arrow' in kwargs else self.r_arrow
        result = _coerce_8(kwargs['result']) if 'result' in kwargs else self.result
        return RustParenthesizedGenericArguments(open_paren=open_paren, params=params, close_paren=close_paren, r_arrow=r_arrow, result=result)

    @property
    def parent(self) -> 'RustParenthesizedGenericArgumentsParent':
        assert(self._parent is not None)
        return cast(RustParenthesizedGenericArgumentsParent, self._parent)


def is_rust_parenthesized_generic_arguments(value: Any) -> TypeIs[RustParenthesizedGenericArguments]:
    return isinstance(value, RustParenthesizedGenericArguments)


class RustPathDeriveKwargs(TypedDict, total=False):

    leading_colon_colon: 'RustColonColon | None'

    segments: 'Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'


class RustPath(_RustBaseNode):

    _fields_ = ('leading_colon_colon', 'segments')

    def count_segments(self) -> int:
        return len(self.segments)

    def __init__(self, segments: 'Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, leading_colon_colon: 'RustColonColon | None' = None) -> None:
        self.leading_colon_colon: RustColonColon | None = _coerce_77(leading_colon_colon)
        self.segments: Punctuated[RustPathSegment, RustColonColon] = _coerce_55(segments)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustPathDeriveKwargs]) -> 'RustPath':
        leading_colon_colon = _coerce_77(kwargs['leading_colon_colon']) if 'leading_colon_colon' in kwargs else self.leading_colon_colon
        segments = _coerce_55(kwargs['segments']) if 'segments' in kwargs else self.segments
        return RustPath(leading_colon_colon=leading_colon_colon, segments=segments)

    @property
    def parent(self) -> 'RustPathParent':
        assert(self._parent is not None)
        return cast(RustPathParent, self._parent)


def is_rust_path(value: Any) -> TypeIs[RustPath]:
    return isinstance(value, RustPath)


class RustPathExprDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    qself: 'RustQself | None'

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'


class RustPathExpr(_RustBaseNode):

    _fields_ = ('attrs', 'qself', 'path')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, qself: 'RustQself | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.qself: RustQself | None = _coerce_78(qself)
        self.path: RustPath = _coerce_56(path)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustPathExprDeriveKwargs]) -> 'RustPathExpr':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        qself = _coerce_78(kwargs['qself']) if 'qself' in kwargs else self.qself
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        return RustPathExpr(attrs=attrs, qself=qself, path=path)

    @property
    def parent(self) -> 'RustPathExprParent':
        assert(self._parent is not None)
        return cast(RustPathExprParent, self._parent)


def is_rust_path_expr(value: Any) -> TypeIs[RustPathExpr]:
    return isinstance(value, RustPathExpr)


class RustPathSegmentDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    args: 'RustPathArguments | None'


class RustPathSegment(_RustBaseNode):

    _fields_ = ('name', 'args')

    def __init__(self, name: 'RustIdent | str', *, args: 'RustPathArguments | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.args: RustPathArguments | None = _coerce_79(args)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustPathSegmentDeriveKwargs]) -> 'RustPathSegment':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        args = _coerce_79(kwargs['args']) if 'args' in kwargs else self.args
        return RustPathSegment(name=name, args=args)

    @property
    def parent(self) -> 'RustPathSegmentParent':
        assert(self._parent is not None)
        return cast(RustPathSegmentParent, self._parent)


def is_rust_path_segment(value: Any) -> TypeIs[RustPathSegment]:
    return isinstance(value, RustPathSegment)


class RustPathTypeExprDeriveKwargs(TypedDict, total=False):

    qself: 'RustQself | None'

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'


class RustPathTypeExpr(_RustBaseNode):

    _fields_ = ('qself', 'path')

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, qself: 'RustQself | None' = None) -> None:
        self.qself: RustQself | None = _coerce_78(qself)
        self.path: RustPath = _coerce_56(path)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustPathTypeExprDeriveKwargs]) -> 'RustPathTypeExpr':
        qself = _coerce_78(kwargs['qself']) if 'qself' in kwargs else self.qself
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        return RustPathTypeExpr(qself=qself, path=path)

    @property
    def parent(self) -> 'RustPathTypeExprParent':
        assert(self._parent is not None)
        return cast(RustPathTypeExprParent, self._parent)


def is_rust_path_type_expr(value: Any) -> TypeIs[RustPathTypeExpr]:
    return isinstance(value, RustPathTypeExpr)


class RustPatternDeriveKwargs(TypedDict, total=False):

    named_pattern: 'RustIdent | RustNamedPattern | str'


class RustPattern(_RustBaseNode):

    _fields_ = ('named_pattern', )

    def __init__(self, named_pattern: 'RustIdent | RustNamedPattern | str') -> None:
        self.named_pattern: RustNamedPattern = _coerce_69(named_pattern)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustPatternDeriveKwargs]) -> 'RustPattern':
        named_pattern = _coerce_69(kwargs['named_pattern']) if 'named_pattern' in kwargs else self.named_pattern
        return RustPattern(named_pattern=named_pattern)

    @property
    def parent(self) -> 'RustPatternParent':
        assert(self._parent is not None)
        return cast(RustPatternParent, self._parent)


def is_rust_pattern(value: Any) -> TypeIs[RustPattern]:
    return isinstance(value, RustPattern)


class RustPublicDeriveKwargs(TypedDict, total=False):

    pub_keyword: 'RustPubKeyword | None'

    restrict: 'RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath, RustCloseParen | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None'


class RustPublic(_RustBaseNode):

    _fields_ = ('pub_keyword', 'restrict')

    def __init__(self, *, pub_keyword: 'RustPubKeyword | None' = None, restrict: 'RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath, RustCloseParen | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None' = None) -> None:
        self.pub_keyword: RustPubKeyword = _coerce_80(pub_keyword)
        self.restrict: tuple[RustOpenParen, RustInKeyword | None, RustPath, RustCloseParen] | None = _coerce_82(restrict)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustPublicDeriveKwargs]) -> 'RustPublic':
        pub_keyword = _coerce_80(kwargs['pub_keyword']) if 'pub_keyword' in kwargs else self.pub_keyword
        restrict = _coerce_82(kwargs['restrict']) if 'restrict' in kwargs else self.restrict
        return RustPublic(pub_keyword=pub_keyword, restrict=restrict)

    @property
    def parent(self) -> 'RustPublicParent':
        assert(self._parent is not None)
        return cast(RustPublicParent, self._parent)


def is_rust_public(value: Any) -> TypeIs[RustPublic]:
    return isinstance(value, RustPublic)


class RustQselfDeriveKwargs(TypedDict, total=False):

    less_than: 'RustLessThan | None'

    type_expr: 'RustTypeExpr'

    as_keyword: 'RustAsKeyword | None'

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'

    greater_than: 'RustGreaterThan | None'


class RustQself(_RustBaseNode):

    _fields_ = ('less_than', 'type_expr', 'as_keyword', 'path', 'greater_than')

    def __init__(self, type_expr: 'RustTypeExpr', path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, less_than: 'RustLessThan | None' = None, as_keyword: 'RustAsKeyword | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.less_than: RustLessThan = _coerce_2(less_than)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)
        self.as_keyword: RustAsKeyword = _coerce_83(as_keyword)
        self.path: RustPath = _coerce_56(path)
        self.greater_than: RustGreaterThan = _coerce_6(greater_than)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustQselfDeriveKwargs]) -> 'RustQself':
        less_than = _coerce_2(kwargs['less_than']) if 'less_than' in kwargs else self.less_than
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        as_keyword = _coerce_83(kwargs['as_keyword']) if 'as_keyword' in kwargs else self.as_keyword
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        greater_than = _coerce_6(kwargs['greater_than']) if 'greater_than' in kwargs else self.greater_than
        return RustQself(less_than=less_than, type_expr=type_expr, as_keyword=as_keyword, path=path, greater_than=greater_than)

    @property
    def parent(self) -> 'RustQselfParent':
        assert(self._parent is not None)
        return cast(RustQselfParent, self._parent)


def is_rust_qself(value: Any) -> TypeIs[RustQself]:
    return isinstance(value, RustQself)


class RustRetExprDeriveKwargs(TypedDict, total=False):

    return_keyword: 'RustReturnKeyword | None'

    expr: 'RustExpr'


class RustRetExpr(_RustBaseNode):

    _fields_ = ('return_keyword', 'expr')

    def __init__(self, expr: 'RustExpr', *, return_keyword: 'RustReturnKeyword | None' = None) -> None:
        self.return_keyword: RustReturnKeyword = _coerce_84(return_keyword)
        self.expr: RustExpr = _coerce_10(expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustRetExprDeriveKwargs]) -> 'RustRetExpr':
        return_keyword = _coerce_84(kwargs['return_keyword']) if 'return_keyword' in kwargs else self.return_keyword
        expr = _coerce_10(kwargs['expr']) if 'expr' in kwargs else self.expr
        return RustRetExpr(return_keyword=return_keyword, expr=expr)

    @property
    def parent(self) -> 'RustRetExprParent':
        assert(self._parent is not None)
        return cast(RustRetExprParent, self._parent)


def is_rust_ret_expr(value: Any) -> TypeIs[RustRetExpr]:
    return isinstance(value, RustRetExpr)


class RustSelfArgDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    reference: 'RustIdent | RustLifetime | tuple[RustAmpersand | None, RustLifetime] | None | str'

    mut_keyword: 'RustMutKeyword | None'

    self_keyword: 'RustSelfKeyword | None'

    colon: 'RustColon | None'

    type_expr: 'RustTypeExpr'


class RustSelfArg(_RustBaseNode):

    _fields_ = ('attrs', 'reference', 'mut_keyword', 'self_keyword', 'colon', 'type_expr')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, type_expr: 'RustTypeExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, reference: 'RustIdent | RustLifetime | tuple[RustAmpersand | None, RustLifetime] | None | str' = None, mut_keyword: 'RustMutKeyword | None' = None, self_keyword: 'RustSelfKeyword | None' = None, colon: 'RustColon | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.reference: tuple[RustAmpersand, RustLifetime] | None = _coerce_87(reference)
        self.mut_keyword: RustMutKeyword | None = _coerce_68(mut_keyword)
        self.self_keyword: RustSelfKeyword = _coerce_88(self_keyword)
        self.colon: RustColon = _coerce_28(colon)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustSelfArgDeriveKwargs]) -> 'RustSelfArg':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        reference = _coerce_87(kwargs['reference']) if 'reference' in kwargs else self.reference
        mut_keyword = _coerce_68(kwargs['mut_keyword']) if 'mut_keyword' in kwargs else self.mut_keyword
        self_keyword = _coerce_88(kwargs['self_keyword']) if 'self_keyword' in kwargs else self.self_keyword
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        return RustSelfArg(attrs=attrs, reference=reference, mut_keyword=mut_keyword, self_keyword=self_keyword, colon=colon, type_expr=type_expr)

    @property
    def parent(self) -> 'RustSelfArgParent':
        assert(self._parent is not None)
        return cast(RustSelfArgParent, self._parent)


def is_rust_self_arg(value: Any) -> TypeIs[RustSelfArg]:
    return isinstance(value, RustSelfArg)


class RustSignatureDeriveKwargs(TypedDict, total=False):

    const_keyword: 'RustConstKeyword | None'

    async_keyword: 'RustAsyncKeyword | None'

    unsafe_keyword: 'RustUnsafeKeyword | None'

    abi: 'RustAbi | RustString | None | str'

    fn_keyword: 'RustFnKeyword | None'

    name: 'RustIdent | str'

    generics: 'RustGenerics | None'

    open_paren: 'RustOpenParen | None'

    inputs: 'Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | ImmutablePunct[RustArg, RustComma] | None'

    close_paren: 'RustCloseParen | None'

    output: 'RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None'


class RustSignature(_RustBaseNode):

    _fields_ = ('const_keyword', 'async_keyword', 'unsafe_keyword', 'abi', 'fn_keyword', 'name', 'generics', 'open_paren', 'inputs', 'close_paren', 'output')

    def count_inputs(self) -> int:
        return len(self.inputs)

    def __init__(self, name: 'RustIdent | str', *, const_keyword: 'RustConstKeyword | None' = None, async_keyword: 'RustAsyncKeyword | None' = None, unsafe_keyword: 'RustUnsafeKeyword | None' = None, abi: 'RustAbi | RustString | None | str' = None, fn_keyword: 'RustFnKeyword | None' = None, generics: 'RustGenerics | None' = None, open_paren: 'RustOpenParen | None' = None, inputs: 'Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | ImmutablePunct[RustArg, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None, output: 'RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None' = None) -> None:
        self.const_keyword: RustConstKeyword | None = _coerce_89(const_keyword)
        self.async_keyword: RustAsyncKeyword | None = _coerce_90(async_keyword)
        self.unsafe_keyword: RustUnsafeKeyword | None = _coerce_50(unsafe_keyword)
        self.abi: RustAbi | None = _coerce_91(abi)
        self.fn_keyword: RustFnKeyword = _coerce_92(fn_keyword)
        self.name: RustIdent = _coerce_12(name)
        self.generics: RustGenerics = _coerce_52(generics)
        self.open_paren: RustOpenParen = _coerce_24(open_paren)
        self.inputs: Punctuated[RustArg, RustComma] = _coerce_94(inputs)
        self.close_paren: RustCloseParen = _coerce_26(close_paren)
        self.output: tuple[RustRArrow, RustTypeExpr] | None = _coerce_95(output)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustSignatureDeriveKwargs]) -> 'RustSignature':
        const_keyword = _coerce_89(kwargs['const_keyword']) if 'const_keyword' in kwargs else self.const_keyword
        async_keyword = _coerce_90(kwargs['async_keyword']) if 'async_keyword' in kwargs else self.async_keyword
        unsafe_keyword = _coerce_50(kwargs['unsafe_keyword']) if 'unsafe_keyword' in kwargs else self.unsafe_keyword
        abi = _coerce_91(kwargs['abi']) if 'abi' in kwargs else self.abi
        fn_keyword = _coerce_92(kwargs['fn_keyword']) if 'fn_keyword' in kwargs else self.fn_keyword
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        generics = _coerce_52(kwargs['generics']) if 'generics' in kwargs else self.generics
        open_paren = _coerce_24(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        inputs = _coerce_94(kwargs['inputs']) if 'inputs' in kwargs else self.inputs
        close_paren = _coerce_26(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        output = _coerce_95(kwargs['output']) if 'output' in kwargs else self.output
        return RustSignature(const_keyword=const_keyword, async_keyword=async_keyword, unsafe_keyword=unsafe_keyword, abi=abi, fn_keyword=fn_keyword, name=name, generics=generics, open_paren=open_paren, inputs=inputs, close_paren=close_paren, output=output)

    @property
    def parent(self) -> 'RustSignatureParent':
        assert(self._parent is not None)
        return cast(RustSignatureParent, self._parent)


def is_rust_signature(value: Any) -> TypeIs[RustSignature]:
    return isinstance(value, RustSignature)


class RustSourceFileDeriveKwargs(TypedDict, total=False):

    items: 'Sequence[RustToplevel] | None'


class RustSourceFile(_RustBaseNode):

    _fields_ = ('items', )

    def count_items(self) -> int:
        return len(self.items)

    def __init__(self, *, items: 'Sequence[RustToplevel] | None' = None) -> None:
        self.items: list[RustToplevel] = _coerce_97(items)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustSourceFileDeriveKwargs]) -> 'RustSourceFile':
        items = _coerce_97(kwargs['items']) if 'items' in kwargs else self.items
        return RustSourceFile(items=items)

    @property
    def parent(self) -> 'RustSourceFileParent':
        raise AssertionError('trying to access the parent node of a top-level node')


def is_rust_source_file(value: Any) -> TypeIs[RustSourceFile]:
    return isinstance(value, RustSourceFile)


class RustStructExprDeriveKwargs(TypedDict, total=False):

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'

    open_brace: 'RustOpenBrace | None'

    inits: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | ImmutablePunct[RustInit, RustComma] | None'

    comma: 'RustComma | None'

    close_brace: 'RustCloseBrace | None'


class RustStructExpr(_RustBaseNode):

    _fields_ = ('path', 'open_brace', 'inits', 'comma', 'close_brace')

    def count_inits(self) -> int:
        return len(self.inits)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, open_brace: 'RustOpenBrace | None' = None, inits: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | ImmutablePunct[RustInit, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.path: RustPath = _coerce_56(path)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.inits: Punctuated[RustInit, RustComma] = _coerce_99(inits)
        self.comma: RustComma | None = _coerce_40(comma)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustStructExprDeriveKwargs]) -> 'RustStructExpr':
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        inits = _coerce_99(kwargs['inits']) if 'inits' in kwargs else self.inits
        comma = _coerce_40(kwargs['comma']) if 'comma' in kwargs else self.comma
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustStructExpr(path=path, open_brace=open_brace, inits=inits, comma=comma, close_brace=close_brace)

    @property
    def parent(self) -> 'RustStructExprParent':
        assert(self._parent is not None)
        return cast(RustStructExprParent, self._parent)


def is_rust_struct_expr(value: Any) -> TypeIs[RustStructExpr]:
    return isinstance(value, RustStructExpr)


class RustStructItemDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    visibility: 'RustPublic | None'

    struct_keyword: 'RustStructKeyword | None'

    name: 'RustIdent | str'

    open_brace: 'RustOpenBrace | None'

    fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | ImmutablePunct[RustField, RustComma] | None'

    comma: 'RustComma | None'

    close_brace: 'RustCloseBrace | None'


class RustStructItem(_RustBaseNode):

    _fields_ = ('attrs', 'visibility', 'struct_keyword', 'name', 'open_brace', 'fields', 'comma', 'close_brace')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_fields(self) -> int:
        return len(self.fields)

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, struct_keyword: 'RustStructKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | ImmutablePunct[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.visibility: RustPublic | None = _coerce_36(visibility)
        self.struct_keyword: RustStructKeyword = _coerce_100(struct_keyword)
        self.name: RustIdent = _coerce_12(name)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.fields: Punctuated[RustField, RustComma] = _coerce_102(fields)
        self.comma: RustComma | None = _coerce_40(comma)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustStructItemDeriveKwargs]) -> 'RustStructItem':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        visibility = _coerce_36(kwargs['visibility']) if 'visibility' in kwargs else self.visibility
        struct_keyword = _coerce_100(kwargs['struct_keyword']) if 'struct_keyword' in kwargs else self.struct_keyword
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        fields = _coerce_102(kwargs['fields']) if 'fields' in kwargs else self.fields
        comma = _coerce_40(kwargs['comma']) if 'comma' in kwargs else self.comma
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustStructItem(attrs=attrs, visibility=visibility, struct_keyword=struct_keyword, name=name, open_brace=open_brace, fields=fields, comma=comma, close_brace=close_brace)

    @property
    def parent(self) -> 'RustStructItemParent':
        assert(self._parent is not None)
        return cast(RustStructItemParent, self._parent)


def is_rust_struct_item(value: Any) -> TypeIs[RustStructItem]:
    return isinstance(value, RustStructItem)


class RustStructVariantDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    open_brace: 'RustOpenBrace | None'

    fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | ImmutablePunct[RustField, RustComma] | None'

    comma: 'RustComma | None'

    close_brace: 'RustCloseBrace | None'


class RustStructVariant(_RustBaseNode):

    _fields_ = ('name', 'open_brace', 'fields', 'comma', 'close_brace')

    def count_fields(self) -> int:
        return len(self.fields)

    def __init__(self, name: 'RustIdent | str', *, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | ImmutablePunct[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.fields: Punctuated[RustField, RustComma] = _coerce_102(fields)
        self.comma: RustComma | None = _coerce_40(comma)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustStructVariantDeriveKwargs]) -> 'RustStructVariant':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        fields = _coerce_102(kwargs['fields']) if 'fields' in kwargs else self.fields
        comma = _coerce_40(kwargs['comma']) if 'comma' in kwargs else self.comma
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustStructVariant(name=name, open_brace=open_brace, fields=fields, comma=comma, close_brace=close_brace)

    @property
    def parent(self) -> 'RustStructVariantParent':
        assert(self._parent is not None)
        return cast(RustStructVariantParent, self._parent)


def is_rust_struct_variant(value: Any) -> TypeIs[RustStructVariant]:
    return isinstance(value, RustStructVariant)


class RustTraitBoundDeriveKwargs(TypedDict, total=False):

    modifier: 'RustTraitBoundModifier | None'

    bound_lifetimes: 'RustBoundLifetimes | None'

    path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]'


class RustTraitBound(_RustBaseNode):

    _fields_ = ('modifier', 'bound_lifetimes', 'path')

    def __init__(self, path: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]', *, modifier: 'RustTraitBoundModifier | None' = None, bound_lifetimes: 'RustBoundLifetimes | None' = None) -> None:
        self.modifier: RustTraitBoundModifier | None = _coerce_103(modifier)
        self.bound_lifetimes: RustBoundLifetimes | None = _coerce_104(bound_lifetimes)
        self.path: RustPath = _coerce_56(path)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTraitBoundDeriveKwargs]) -> 'RustTraitBound':
        modifier = _coerce_103(kwargs['modifier']) if 'modifier' in kwargs else self.modifier
        bound_lifetimes = _coerce_104(kwargs['bound_lifetimes']) if 'bound_lifetimes' in kwargs else self.bound_lifetimes
        path = _coerce_56(kwargs['path']) if 'path' in kwargs else self.path
        return RustTraitBound(modifier=modifier, bound_lifetimes=bound_lifetimes, path=path)

    @property
    def parent(self) -> 'RustTraitBoundParent':
        assert(self._parent is not None)
        return cast(RustTraitBoundParent, self._parent)


def is_rust_trait_bound(value: Any) -> TypeIs[RustTraitBound]:
    return isinstance(value, RustTraitBound)


class RustTraitBoundModifierDeriveKwargs(TypedDict, total=False):

    question_mark: 'RustQuestionMark | None'


class RustTraitBoundModifier(_RustBaseNode):

    _fields_ = ('question_mark', )

    def __init__(self, *, question_mark: 'RustQuestionMark | None' = None) -> None:
        self.question_mark: RustQuestionMark = _coerce_105(question_mark)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTraitBoundModifierDeriveKwargs]) -> 'RustTraitBoundModifier':
        question_mark = _coerce_105(kwargs['question_mark']) if 'question_mark' in kwargs else self.question_mark
        return RustTraitBoundModifier(question_mark=question_mark)

    @property
    def parent(self) -> 'RustTraitBoundModifierParent':
        assert(self._parent is not None)
        return cast(RustTraitBoundModifierParent, self._parent)


def is_rust_trait_bound_modifier(value: Any) -> TypeIs[RustTraitBoundModifier]:
    return isinstance(value, RustTraitBoundModifier)


class RustTupleTypeExprDeriveKwargs(TypedDict, total=False):

    open_paren: 'RustOpenParen | None'

    elements: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None'

    close_paren: 'RustCloseParen | None'


class RustTupleTypeExpr(_RustBaseNode):

    _fields_ = ('open_paren', 'elements', 'close_paren')

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'RustOpenParen | None' = None, elements: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.open_paren: RustOpenParen = _coerce_24(open_paren)
        self.elements: Punctuated[RustTypeExpr, RustComma] = _coerce_75(elements)
        self.close_paren: RustCloseParen = _coerce_26(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTupleTypeExprDeriveKwargs]) -> 'RustTupleTypeExpr':
        open_paren = _coerce_24(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        elements = _coerce_75(kwargs['elements']) if 'elements' in kwargs else self.elements
        close_paren = _coerce_26(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return RustTupleTypeExpr(open_paren=open_paren, elements=elements, close_paren=close_paren)

    @property
    def parent(self) -> 'RustTupleTypeExprParent':
        assert(self._parent is not None)
        return cast(RustTupleTypeExprParent, self._parent)


def is_rust_tuple_type_expr(value: Any) -> TypeIs[RustTupleTypeExpr]:
    return isinstance(value, RustTupleTypeExpr)


class RustTupleVariantDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    open_paren: 'RustOpenParen | None'

    types: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None'

    close_paren: 'RustCloseParen | None'


class RustTupleVariant(_RustBaseNode):

    _fields_ = ('name', 'open_paren', 'types', 'close_paren')

    def count_types(self) -> int:
        return len(self.types)

    def __init__(self, name: 'RustIdent | str', *, open_paren: 'RustOpenParen | None' = None, types: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.open_paren: RustOpenParen = _coerce_24(open_paren)
        self.types: Punctuated[RustTypeExpr, RustComma] = _coerce_75(types)
        self.close_paren: RustCloseParen = _coerce_26(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTupleVariantDeriveKwargs]) -> 'RustTupleVariant':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        open_paren = _coerce_24(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        types = _coerce_75(kwargs['types']) if 'types' in kwargs else self.types
        close_paren = _coerce_26(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return RustTupleVariant(name=name, open_paren=open_paren, types=types, close_paren=close_paren)

    @property
    def parent(self) -> 'RustTupleVariantParent':
        assert(self._parent is not None)
        return cast(RustTupleVariantParent, self._parent)


def is_rust_tuple_variant(value: Any) -> TypeIs[RustTupleVariant]:
    return isinstance(value, RustTupleVariant)


class RustTurbofishDeriveKwargs(TypedDict, total=False):

    colon_colon: 'RustColonColon | None'

    less_than: 'RustLessThan | None'

    args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | ImmutablePunct[RustGenericArgument, RustComma] | None'

    greater_than: 'RustGreaterThan | None'


class RustTurbofish(_RustBaseNode):

    _fields_ = ('colon_colon', 'less_than', 'args', 'greater_than')

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, *, colon_colon: 'RustColonColon | None' = None, less_than: 'RustLessThan | None' = None, args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | ImmutablePunct[RustGenericArgument, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.colon_colon: RustColonColon = _coerce_106(colon_colon)
        self.less_than: RustLessThan = _coerce_2(less_than)
        self.args: Punctuated[RustGenericArgument, RustComma] = _coerce_5(args)
        self.greater_than: RustGreaterThan = _coerce_6(greater_than)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTurbofishDeriveKwargs]) -> 'RustTurbofish':
        colon_colon = _coerce_106(kwargs['colon_colon']) if 'colon_colon' in kwargs else self.colon_colon
        less_than = _coerce_2(kwargs['less_than']) if 'less_than' in kwargs else self.less_than
        args = _coerce_5(kwargs['args']) if 'args' in kwargs else self.args
        greater_than = _coerce_6(kwargs['greater_than']) if 'greater_than' in kwargs else self.greater_than
        return RustTurbofish(colon_colon=colon_colon, less_than=less_than, args=args, greater_than=greater_than)

    @property
    def parent(self) -> 'RustTurbofishParent':
        assert(self._parent is not None)
        return cast(RustTurbofishParent, self._parent)


def is_rust_turbofish(value: Any) -> TypeIs[RustTurbofish]:
    return isinstance(value, RustTurbofish)


class RustTypeInitDeriveKwargs(TypedDict, total=False):

    equals: 'RustEquals | None'

    type_expr: 'RustTypeExpr'


class RustTypeInit(_RustBaseNode):

    _fields_ = ('equals', 'type_expr')

    def __init__(self, type_expr: 'RustTypeExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.equals: RustEquals = _coerce_14(equals)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTypeInitDeriveKwargs]) -> 'RustTypeInit':
        equals = _coerce_14(kwargs['equals']) if 'equals' in kwargs else self.equals
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        return RustTypeInit(equals=equals, type_expr=type_expr)

    @property
    def parent(self) -> 'RustTypeInitParent':
        assert(self._parent is not None)
        return cast(RustTypeInitParent, self._parent)


def is_rust_type_init(value: Any) -> TypeIs[RustTypeInit]:
    return isinstance(value, RustTypeInit)


class RustTypeParamDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    colon: 'RustColon | None'

    type_param_bound: 'RustTypeParamBound'

    percent: 'RustPercent | None'

    plus: 'RustPlus | None'

    default: 'RustTypeExpr | RustTypeInit | None'


class RustTypeParam(_RustBaseNode):

    _fields_ = ('name', 'colon', 'type_param_bound', 'percent', 'plus', 'default')

    def __init__(self, name: 'RustIdent | str', type_param_bound: 'RustTypeParamBound', *, colon: 'RustColon | None' = None, percent: 'RustPercent | None' = None, plus: 'RustPlus | None' = None, default: 'RustTypeExpr | RustTypeInit | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.colon: RustColon = _coerce_28(colon)
        self.type_param_bound: RustTypeParamBound = _coerce_31(type_param_bound)
        self.percent: RustPercent = _coerce_107(percent)
        self.plus: RustPlus = _coerce_108(plus)
        self.default: RustTypeInit | None = _coerce_109(default)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTypeParamDeriveKwargs]) -> 'RustTypeParam':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        type_param_bound = _coerce_31(kwargs['type_param_bound']) if 'type_param_bound' in kwargs else self.type_param_bound
        percent = _coerce_107(kwargs['percent']) if 'percent' in kwargs else self.percent
        plus = _coerce_108(kwargs['plus']) if 'plus' in kwargs else self.plus
        default = _coerce_109(kwargs['default']) if 'default' in kwargs else self.default
        return RustTypeParam(name=name, colon=colon, type_param_bound=type_param_bound, percent=percent, plus=plus, default=default)

    @property
    def parent(self) -> 'RustTypeParamParent':
        assert(self._parent is not None)
        return cast(RustTypeParamParent, self._parent)


def is_rust_type_param(value: Any) -> TypeIs[RustTypeParam]:
    return isinstance(value, RustTypeParam)


class RustTypePredicateDeriveKwargs(TypedDict, total=False):

    bound_lifetimes: 'RustBoundLifetimes | None'

    type_expr: 'RustTypeExpr'

    colon: 'RustColon | None'

    bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus]'


class RustTypePredicate(_RustBaseNode):

    _fields_ = ('bound_lifetimes', 'type_expr', 'colon', 'bounds')

    def count_bounds(self) -> int:
        return len(self.bounds)

    def __init__(self, type_expr: 'RustTypeExpr', bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus]', *, bound_lifetimes: 'RustBoundLifetimes | None' = None, colon: 'RustColon | None' = None) -> None:
        self.bound_lifetimes: RustBoundLifetimes = _coerce_110(bound_lifetimes)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)
        self.colon: RustColon = _coerce_28(colon)
        self.bounds: Punctuated[RustTypeParamBound, RustPlus] = _coerce_111(bounds)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTypePredicateDeriveKwargs]) -> 'RustTypePredicate':
        bound_lifetimes = _coerce_110(kwargs['bound_lifetimes']) if 'bound_lifetimes' in kwargs else self.bound_lifetimes
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        bounds = _coerce_111(kwargs['bounds']) if 'bounds' in kwargs else self.bounds
        return RustTypePredicate(bound_lifetimes=bound_lifetimes, type_expr=type_expr, colon=colon, bounds=bounds)

    @property
    def parent(self) -> 'RustTypePredicateParent':
        assert(self._parent is not None)
        return cast(RustTypePredicateParent, self._parent)


def is_rust_type_predicate(value: Any) -> TypeIs[RustTypePredicate]:
    return isinstance(value, RustTypePredicate)


class RustTypedArgDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    pattern: 'RustIdent | RustNamedPattern | RustPattern | str'

    colon: 'RustColon | None'

    type_expr: 'RustTypeExpr'


class RustTypedArg(_RustBaseNode):

    _fields_ = ('attrs', 'pattern', 'colon', 'type_expr')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, pattern: 'RustIdent | RustNamedPattern | RustPattern | str', type_expr: 'RustTypeExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, colon: 'RustColon | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.pattern: RustPattern = _coerce_70(pattern)
        self.colon: RustColon = _coerce_28(colon)
        self.type_expr: RustTypeExpr = _coerce_8(type_expr)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustTypedArgDeriveKwargs]) -> 'RustTypedArg':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        pattern = _coerce_70(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        colon = _coerce_28(kwargs['colon']) if 'colon' in kwargs else self.colon
        type_expr = _coerce_8(kwargs['type_expr']) if 'type_expr' in kwargs else self.type_expr
        return RustTypedArg(attrs=attrs, pattern=pattern, colon=colon, type_expr=type_expr)

    @property
    def parent(self) -> 'RustTypedArgParent':
        assert(self._parent is not None)
        return cast(RustTypedArgParent, self._parent)


def is_rust_typed_arg(value: Any) -> TypeIs[RustTypedArg]:
    return isinstance(value, RustTypedArg)


class RustUseGlobDeriveKwargs(TypedDict, total=False):

    asterisk: 'RustAsterisk | None'


class RustUseGlob(_RustBaseNode):

    _fields_ = ('asterisk', )

    def __init__(self, *, asterisk: 'RustAsterisk | None' = None) -> None:
        self.asterisk: RustAsterisk = _coerce_112(asterisk)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustUseGlobDeriveKwargs]) -> 'RustUseGlob':
        asterisk = _coerce_112(kwargs['asterisk']) if 'asterisk' in kwargs else self.asterisk
        return RustUseGlob(asterisk=asterisk)

    @property
    def parent(self) -> 'RustUseGlobParent':
        assert(self._parent is not None)
        return cast(RustUseGlobParent, self._parent)


def is_rust_use_glob(value: Any) -> TypeIs[RustUseGlob]:
    return isinstance(value, RustUseGlob)


class RustUseGroupDeriveKwargs(TypedDict, total=False):

    open_brace: 'RustOpenBrace | None'

    items: 'Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | ImmutablePunct[RustUseTree, RustComma] | None'

    close_brace: 'RustCloseBrace | None'


class RustUseGroup(_RustBaseNode):

    _fields_ = ('open_brace', 'items', 'close_brace')

    def count_items(self) -> int:
        return len(self.items)

    def __init__(self, *, open_brace: 'RustOpenBrace | None' = None, items: 'Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | ImmutablePunct[RustUseTree, RustComma] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.open_brace: RustOpenBrace = _coerce_18(open_brace)
        self.items: Punctuated[RustUseTree, RustComma] = _coerce_114(items)
        self.close_brace: RustCloseBrace = _coerce_20(close_brace)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustUseGroupDeriveKwargs]) -> 'RustUseGroup':
        open_brace = _coerce_18(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        items = _coerce_114(kwargs['items']) if 'items' in kwargs else self.items
        close_brace = _coerce_20(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        return RustUseGroup(open_brace=open_brace, items=items, close_brace=close_brace)

    @property
    def parent(self) -> 'RustUseGroupParent':
        assert(self._parent is not None)
        return cast(RustUseGroupParent, self._parent)


def is_rust_use_group(value: Any) -> TypeIs[RustUseGroup]:
    return isinstance(value, RustUseGroup)


class RustUseItemDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    visibility: 'RustPublic | None'

    use_keyword: 'RustUseKeyword | None'

    colon_colon: 'RustColonColon | None'

    path: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None'

    semicolon: 'RustSemicolon | None'


class RustUseItem(_RustBaseNode):

    _fields_ = ('attrs', 'visibility', 'use_keyword', 'colon_colon', 'path', 'semicolon')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_path(self) -> int:
        return len(self.path)

    def __init__(self, *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, use_keyword: 'RustUseKeyword | None' = None, colon_colon: 'RustColonColon | None' = None, path: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None' = None, semicolon: 'RustSemicolon | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.visibility: RustPublic | None = _coerce_36(visibility)
        self.use_keyword: RustUseKeyword = _coerce_115(use_keyword)
        self.colon_colon: RustColonColon | None = _coerce_77(colon_colon)
        self.path: list[tuple[RustIdent, RustColonColon]] = _coerce_117(path)
        self.semicolon: RustSemicolon = _coerce_9(semicolon)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustUseItemDeriveKwargs]) -> 'RustUseItem':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        visibility = _coerce_36(kwargs['visibility']) if 'visibility' in kwargs else self.visibility
        use_keyword = _coerce_115(kwargs['use_keyword']) if 'use_keyword' in kwargs else self.use_keyword
        colon_colon = _coerce_77(kwargs['colon_colon']) if 'colon_colon' in kwargs else self.colon_colon
        path = _coerce_117(kwargs['path']) if 'path' in kwargs else self.path
        semicolon = _coerce_9(kwargs['semicolon']) if 'semicolon' in kwargs else self.semicolon
        return RustUseItem(attrs=attrs, visibility=visibility, use_keyword=use_keyword, colon_colon=colon_colon, path=path, semicolon=semicolon)

    @property
    def parent(self) -> 'RustUseItemParent':
        assert(self._parent is not None)
        return cast(RustUseItemParent, self._parent)


def is_rust_use_item(value: Any) -> TypeIs[RustUseItem]:
    return isinstance(value, RustUseItem)


class RustUseNameDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'


class RustUseName(_RustBaseNode):

    _fields_ = ('name', )

    def __init__(self, name: 'RustIdent | str') -> None:
        self.name: RustIdent = _coerce_12(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustUseNameDeriveKwargs]) -> 'RustUseName':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        return RustUseName(name=name)

    @property
    def parent(self) -> 'RustUseNameParent':
        assert(self._parent is not None)
        return cast(RustUseNameParent, self._parent)


def is_rust_use_name(value: Any) -> TypeIs[RustUseName]:
    return isinstance(value, RustUseName)


class RustUsePathDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    colon_colon: 'RustColonColon | None'

    tree: 'RustUseTree'


class RustUsePath(_RustBaseNode):

    _fields_ = ('name', 'colon_colon', 'tree')

    def __init__(self, name: 'RustIdent | str', tree: 'RustUseTree', *, colon_colon: 'RustColonColon | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.colon_colon: RustColonColon = _coerce_106(colon_colon)
        self.tree: RustUseTree = _coerce_113(tree)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustUsePathDeriveKwargs]) -> 'RustUsePath':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        colon_colon = _coerce_106(kwargs['colon_colon']) if 'colon_colon' in kwargs else self.colon_colon
        tree = _coerce_113(kwargs['tree']) if 'tree' in kwargs else self.tree
        return RustUsePath(name=name, colon_colon=colon_colon, tree=tree)

    @property
    def parent(self) -> 'RustUsePathParent':
        assert(self._parent is not None)
        return cast(RustUsePathParent, self._parent)


def is_rust_use_path(value: Any) -> TypeIs[RustUsePath]:
    return isinstance(value, RustUsePath)


class RustUseRenameDeriveKwargs(TypedDict, total=False):

    name: 'RustIdent | str'

    as_keyword: 'RustAsKeyword | None'

    rename: 'RustIdent | str'


class RustUseRename(_RustBaseNode):

    _fields_ = ('name', 'as_keyword', 'rename')

    def __init__(self, name: 'RustIdent | str', rename: 'RustIdent | str', *, as_keyword: 'RustAsKeyword | None' = None) -> None:
        self.name: RustIdent = _coerce_12(name)
        self.as_keyword: RustAsKeyword = _coerce_83(as_keyword)
        self.rename: RustIdent = _coerce_12(rename)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustUseRenameDeriveKwargs]) -> 'RustUseRename':
        name = _coerce_12(kwargs['name']) if 'name' in kwargs else self.name
        as_keyword = _coerce_83(kwargs['as_keyword']) if 'as_keyword' in kwargs else self.as_keyword
        rename = _coerce_12(kwargs['rename']) if 'rename' in kwargs else self.rename
        return RustUseRename(name=name, as_keyword=as_keyword, rename=rename)

    @property
    def parent(self) -> 'RustUseRenameParent':
        assert(self._parent is not None)
        return cast(RustUseRenameParent, self._parent)


def is_rust_use_rename(value: Any) -> TypeIs[RustUseRename]:
    return isinstance(value, RustUseRename)


class RustVariadicArgDeriveKwargs(TypedDict, total=False):

    attrs: 'Sequence[RustAttr | RustMeta] | None'

    pattern: 'RustIdent | RustNamedPattern | RustPattern | str'

    dot_dot_dot: 'RustDotDotDot | None'

    comma: 'RustComma | None'


class RustVariadicArg(_RustBaseNode):

    _fields_ = ('attrs', 'pattern', 'dot_dot_dot', 'comma')

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, pattern: 'RustIdent | RustNamedPattern | RustPattern | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, dot_dot_dot: 'RustDotDotDot | None' = None, comma: 'RustComma | None' = None) -> None:
        self.attrs: list[RustAttr] = _coerce_35(attrs)
        self.pattern: RustPattern = _coerce_70(pattern)
        self.dot_dot_dot: RustDotDotDot | None = _coerce_118(dot_dot_dot)
        self.comma: RustComma | None = _coerce_40(comma)

    @no_type_check
    def derive(self, **kwargs: Unpack[RustVariadicArgDeriveKwargs]) -> 'RustVariadicArg':
        attrs = _coerce_35(kwargs['attrs']) if 'attrs' in kwargs else self.attrs
        pattern = _coerce_70(kwargs['pattern']) if 'pattern' in kwargs else self.pattern
        dot_dot_dot = _coerce_118(kwargs['dot_dot_dot']) if 'dot_dot_dot' in kwargs else self.dot_dot_dot
        comma = _coerce_40(kwargs['comma']) if 'comma' in kwargs else self.comma
        return RustVariadicArg(attrs=attrs, pattern=pattern, dot_dot_dot=dot_dot_dot, comma=comma)

    @property
    def parent(self) -> 'RustVariadicArgParent':
        assert(self._parent is not None)
        return cast(RustVariadicArgParent, self._parent)


def is_rust_variadic_arg(value: Any) -> TypeIs[RustVariadicArg]:
    return isinstance(value, RustVariadicArg)


type RustArg = RustSelfArg | RustTypedArg | RustVariadicArg


def is_rust_arg(value: Any) -> TypeIs[RustArg]:
    return isinstance(value, RustSelfArg) or isinstance(value, RustTypedArg) or isinstance(value, RustVariadicArg)


type RustExpr = RustLitExpr | RustPathExpr | RustCallExpr | RustStructExpr | RustBlockExpr | RustRetExpr


def is_rust_expr(value: Any) -> TypeIs[RustExpr]:
    return isinstance(value, RustLitExpr) or isinstance(value, RustPathExpr) or isinstance(value, RustCallExpr) or isinstance(value, RustStructExpr) or isinstance(value, RustBlockExpr) or isinstance(value, RustRetExpr)


type RustGenericArgument = RustLifetime | RustTypeExpr | RustExpr | RustAssocType | RustAssocConst | RustConstraint


def is_rust_generic_argument(value: Any) -> TypeIs[RustGenericArgument]:
    return isinstance(value, RustLifetime) or is_rust_type_expr(value) or is_rust_expr(value) or isinstance(value, RustAssocType) or isinstance(value, RustAssocConst) or isinstance(value, RustConstraint)


type RustGenericParam = RustLifetime | RustTypeParam | RustConstParam


def is_rust_generic_param(value: Any) -> TypeIs[RustGenericParam]:
    return isinstance(value, RustLifetime) or isinstance(value, RustTypeParam) or isinstance(value, RustConstParam)


type RustItem = RustEnumItem | RustStructItem | RustUseItem | RustExprItem


def is_rust_item(value: Any) -> TypeIs[RustItem]:
    return isinstance(value, RustEnumItem) or isinstance(value, RustStructItem) or isinstance(value, RustUseItem) or isinstance(value, RustExprItem)


type RustKeyword = RustPubKeyword | RustInKeyword | RustConstKeyword | RustForKeyword | RustAsKeyword | RustRefKeyword | RustMutKeyword | RustTrueKeyword | RustFalseKeyword | RustReturnKeyword | RustExternKeyword | RustMutKeyword | RustSelfKeyword | RustWhereKeyword | RustConstKeyword | RustAsyncKeyword | RustUnsafeKeyword | RustFnKeyword | RustEnumKeyword | RustStructKeyword | RustAsKeyword | RustUseKeyword | RustDefaultKeyword | RustDefaultKeyword | RustUnsafeKeyword | RustImplKeyword | RustForKeyword


def is_rust_keyword(value: Any) -> TypeIs[RustKeyword]:
    return isinstance(value, RustPubKeyword) or isinstance(value, RustInKeyword) or isinstance(value, RustConstKeyword) or isinstance(value, RustForKeyword) or isinstance(value, RustAsKeyword) or isinstance(value, RustRefKeyword) or isinstance(value, RustMutKeyword) or isinstance(value, RustTrueKeyword) or isinstance(value, RustFalseKeyword) or isinstance(value, RustReturnKeyword) or isinstance(value, RustExternKeyword) or isinstance(value, RustMutKeyword) or isinstance(value, RustSelfKeyword) or isinstance(value, RustWhereKeyword) or isinstance(value, RustConstKeyword) or isinstance(value, RustAsyncKeyword) or isinstance(value, RustUnsafeKeyword) or isinstance(value, RustFnKeyword) or isinstance(value, RustEnumKeyword) or isinstance(value, RustStructKeyword) or isinstance(value, RustAsKeyword) or isinstance(value, RustUseKeyword) or isinstance(value, RustDefaultKeyword) or isinstance(value, RustDefaultKeyword) or isinstance(value, RustUnsafeKeyword) or isinstance(value, RustImplKeyword) or isinstance(value, RustForKeyword)


type RustMeta = RustMetaPath | RustMetaParenthesized | RustMetaBracketed | RustMetaBraced | RustMetaNameValue


def is_rust_meta(value: Any) -> TypeIs[RustMeta]:
    return isinstance(value, RustMetaPath) or isinstance(value, RustMetaParenthesized) or isinstance(value, RustMetaBracketed) or isinstance(value, RustMetaBraced) or isinstance(value, RustMetaNameValue)


type RustNode = RustPublic | RustTypeInit | RustTypeParam | RustConstParam | RustTraitBoundModifier | RustBoundLifetimes | RustTraitBound | RustLifetime | RustAssocType | RustAssocConst | RustConstraint | RustTurbofish | RustAngleBracketedGenericArguments | RustParenthesizedGenericArguments | RustPathSegment | RustPath | RustQself | RustPathTypeExpr | RustArrayTypeExpr | RustNeverTypeExpr | RustTupleTypeExpr | RustNamedPattern | RustPattern | RustPathExpr | RustLitExpr | RustInit | RustStructExpr | RustCallExpr | RustRetExpr | RustBlockExpr | RustAbi | RustVariadicArg | RustSelfArg | RustTypedArg | RustLifetimePredicate | RustTypePredicate | RustGenerics | RustSignature | RustField | RustStructVariant | RustTupleVariant | RustEmptyVariant | RustEnumItem | RustMetaPath | RustMetaBraced | RustMetaParenthesized | RustMetaBracketed | RustMetaNameValue | RustAttr | RustStructItem | RustExprItem | RustUsePath | RustUseName | RustUseRename | RustUseGlob | RustUseGroup | RustUseItem | RustFnImplElement | RustImplElement | RustImplItem | RustSourceFile


def is_rust_node(value: Any) -> TypeIs[RustNode]:
    return isinstance(value, RustPublic) or isinstance(value, RustTypeInit) or isinstance(value, RustTypeParam) or isinstance(value, RustConstParam) or isinstance(value, RustTraitBoundModifier) or isinstance(value, RustBoundLifetimes) or isinstance(value, RustTraitBound) or isinstance(value, RustLifetime) or isinstance(value, RustAssocType) or isinstance(value, RustAssocConst) or isinstance(value, RustConstraint) or isinstance(value, RustTurbofish) or isinstance(value, RustAngleBracketedGenericArguments) or isinstance(value, RustParenthesizedGenericArguments) or isinstance(value, RustPathSegment) or isinstance(value, RustPath) or isinstance(value, RustQself) or isinstance(value, RustPathTypeExpr) or isinstance(value, RustArrayTypeExpr) or isinstance(value, RustNeverTypeExpr) or isinstance(value, RustTupleTypeExpr) or isinstance(value, RustNamedPattern) or isinstance(value, RustPattern) or isinstance(value, RustPathExpr) or isinstance(value, RustLitExpr) or isinstance(value, RustInit) or isinstance(value, RustStructExpr) or isinstance(value, RustCallExpr) or isinstance(value, RustRetExpr) or isinstance(value, RustBlockExpr) or isinstance(value, RustAbi) or isinstance(value, RustVariadicArg) or isinstance(value, RustSelfArg) or isinstance(value, RustTypedArg) or isinstance(value, RustLifetimePredicate) or isinstance(value, RustTypePredicate) or isinstance(value, RustGenerics) or isinstance(value, RustSignature) or isinstance(value, RustField) or isinstance(value, RustStructVariant) or isinstance(value, RustTupleVariant) or isinstance(value, RustEmptyVariant) or isinstance(value, RustEnumItem) or isinstance(value, RustMetaPath) or isinstance(value, RustMetaBraced) or isinstance(value, RustMetaParenthesized) or isinstance(value, RustMetaBracketed) or isinstance(value, RustMetaNameValue) or isinstance(value, RustAttr) or isinstance(value, RustStructItem) or isinstance(value, RustExprItem) or isinstance(value, RustUsePath) or isinstance(value, RustUseName) or isinstance(value, RustUseRename) or isinstance(value, RustUseGlob) or isinstance(value, RustUseGroup) or isinstance(value, RustUseItem) or isinstance(value, RustFnImplElement) or isinstance(value, RustImplElement) or isinstance(value, RustImplItem) or isinstance(value, RustSourceFile)


type RustPathArguments = RustTurbofish | RustAngleBracketedGenericArguments | RustParenthesizedGenericArguments


def is_rust_path_arguments(value: Any) -> TypeIs[RustPathArguments]:
    return isinstance(value, RustTurbofish) or isinstance(value, RustAngleBracketedGenericArguments) or isinstance(value, RustParenthesizedGenericArguments)


type RustSyntax = RustToken | RustNode


def is_rust_syntax(value: Any) -> TypeIs[RustSyntax]:
    return is_rust_token(value) or is_rust_node(value)


type RustToken = RustIdent | RustInteger | RustFloat | RustString | RustChar


def is_rust_token(value: Any) -> TypeIs[RustToken]:
    return isinstance(value, RustIdent) or isinstance(value, RustInteger) or isinstance(value, RustFloat) or isinstance(value, RustString) or isinstance(value, RustChar)


type RustToplevel = RustEnumItem | RustStructItem | RustUseItem | RustImplItem


def is_rust_toplevel(value: Any) -> TypeIs[RustToplevel]:
    return isinstance(value, RustEnumItem) or isinstance(value, RustStructItem) or isinstance(value, RustUseItem) or isinstance(value, RustImplItem)


type RustTypeExpr = RustPathTypeExpr | RustArrayTypeExpr | RustNeverTypeExpr | RustTupleTypeExpr


def is_rust_type_expr(value: Any) -> TypeIs[RustTypeExpr]:
    return isinstance(value, RustPathTypeExpr) or isinstance(value, RustArrayTypeExpr) or isinstance(value, RustNeverTypeExpr) or isinstance(value, RustTupleTypeExpr)


type RustTypeParamBound = RustTraitBound | RustLifetime


def is_rust_type_param_bound(value: Any) -> TypeIs[RustTypeParamBound]:
    return isinstance(value, RustTraitBound) or isinstance(value, RustLifetime)


type RustUseTree = RustUsePath | RustUseRename | RustUseName | RustUseGlob | RustUseGroup


def is_rust_use_tree(value: Any) -> TypeIs[RustUseTree]:
    return isinstance(value, RustUsePath) or isinstance(value, RustUseRename) or isinstance(value, RustUseName) or isinstance(value, RustUseGlob) or isinstance(value, RustUseGroup)


type RustVariant = RustStructVariant | RustTupleVariant | RustEmptyVariant


def is_rust_variant(value: Any) -> TypeIs[RustVariant]:
    return isinstance(value, RustStructVariant) or isinstance(value, RustTupleVariant) or isinstance(value, RustEmptyVariant)


type RustWherePredicate = RustLifetimePredicate | RustTypePredicate


def is_rust_where_predicate(value: Any) -> TypeIs[RustWherePredicate]:
    return isinstance(value, RustLifetimePredicate) or isinstance(value, RustTypePredicate)


type RustAbiParent = RustSignature


type RustAngleBracketedGenericArgumentsParent = RustAssocConst | RustAssocType | RustConstraint | RustPathSegment


type RustArrayTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustAssocConstParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustAssocTypeParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustAttrParent = RustEnumItem | RustFnImplElement | RustImplItem | RustNamedPattern | RustPathExpr | RustSelfArg | RustStructItem | RustTypedArg | RustUseItem | RustVariadicArg


type RustBlockExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustBoundLifetimesParent = RustTraitBound | RustTypePredicate


type RustCallExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustConstParamParent = RustBoundLifetimes | RustGenerics


type RustConstraintParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustEmptyVariantParent = RustEnumItem


type RustEnumItemParent = RustBlockExpr | RustFnImplElement | RustSourceFile


type RustExprItemParent = RustBlockExpr | RustFnImplElement


type RustFieldParent = RustStructItem | RustStructVariant


type RustFnImplElementParent = RustImplElement


type RustGenericsParent = RustImplItem | RustSignature


type RustImplElementParent = RustImplItem


type RustImplItemParent = RustSourceFile


type RustInitParent = RustConstParam | RustEmptyVariant | RustStructExpr


type RustLifetimeParent = RustAngleBracketedGenericArguments | RustBoundLifetimes | RustConstraint | RustGenerics | RustLifetimePredicate | RustSelfArg | RustTurbofish | RustTypeParam | RustTypePredicate


type RustLifetimePredicateParent = RustGenerics


type RustLitExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustMetaBracedParent = RustAttr


type RustMetaBracketedParent = RustAttr


type RustMetaNameValueParent = RustAttr


type RustMetaParenthesizedParent = RustAttr


type RustMetaPathParent = RustAttr


type RustNamedPatternParent = RustPattern


type RustNeverTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustParenthesizedGenericArgumentsParent = RustPathSegment


type RustPathParent = RustImplItem | RustMetaBraced | RustMetaBracketed | RustMetaNameValue | RustMetaParenthesized | RustMetaPath | RustPathExpr | RustPathTypeExpr | RustPublic | RustQself | RustStructExpr | RustTraitBound


type RustPathExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustPathSegmentParent = RustPath


type RustPathTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustPatternParent = RustNamedPattern | RustTypedArg | RustVariadicArg


type RustPublicParent = RustEnumItem | RustFnImplElement | RustStructItem | RustUseItem


type RustQselfParent = RustPathExpr | RustPathTypeExpr


type RustRetExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustSelfArgParent = RustSignature


type RustSignatureParent = RustFnImplElement


type RustSourceFileParent = Never


type RustStructExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustStructItemParent = RustBlockExpr | RustFnImplElement | RustSourceFile


type RustStructVariantParent = RustEnumItem


type RustTraitBoundParent = RustConstraint | RustTypeParam | RustTypePredicate


type RustTraitBoundModifierParent = RustTraitBound


type RustTupleTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustTupleVariantParent = RustEnumItem


type RustTurbofishParent = RustPathSegment


type RustTypeInitParent = RustTypeParam


type RustTypeParamParent = RustBoundLifetimes | RustGenerics


type RustTypePredicateParent = RustGenerics


type RustTypedArgParent = RustSignature


type RustUseGlobParent = RustUseGroup | RustUsePath


type RustUseGroupParent = RustUseGroup | RustUsePath


type RustUseItemParent = RustBlockExpr | RustFnImplElement | RustSourceFile


type RustUseNameParent = RustUseGroup | RustUsePath


type RustUsePathParent = RustUseGroup | RustUsePath


type RustUseRenameParent = RustUseGroup | RustUsePath


type RustVariadicArgParent = RustSignature


@no_type_check
def _coerce_0(value: 'RustExternKeyword | None') -> 'RustExternKeyword':
    if value is None:
        return RustExternKeyword()
    elif isinstance(value, RustExternKeyword):
        return value
    else:
        raise ValueError('the coercion from RustExternKeyword | None to RustExternKeyword failed')


@no_type_check
def _coerce_1(value: 'RustString | str') -> 'RustString':
    if isinstance(value, str):
        return RustString(value)
    elif isinstance(value, RustString):
        return value
    else:
        raise ValueError('the coercion from RustString | str to RustString failed')


@no_type_check
def _coerce_2(value: 'RustLessThan | None') -> 'RustLessThan':
    if value is None:
        return RustLessThan()
    elif isinstance(value, RustLessThan):
        return value
    else:
        raise ValueError('the coercion from RustLessThan | None to RustLessThan failed')


@no_type_check
def _coerce_3(value: 'RustGenericArgument') -> 'RustGenericArgument':
    return value


@no_type_check
def _coerce_4(value: 'RustComma') -> 'RustComma':
    return value


@no_type_check
def _coerce_5(value: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | ImmutablePunct[RustGenericArgument, RustComma] | None') -> 'Punctuated[RustGenericArgument, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_3(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_3(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | ImmutablePunct[RustGenericArgument, RustComma] | None to Punctuated[RustGenericArgument, RustComma] failed')


@no_type_check
def _coerce_6(value: 'RustGreaterThan | None') -> 'RustGreaterThan':
    if value is None:
        return RustGreaterThan()
    elif isinstance(value, RustGreaterThan):
        return value
    else:
        raise ValueError('the coercion from RustGreaterThan | None to RustGreaterThan failed')


@no_type_check
def _coerce_7(value: 'RustOpenBracket | None') -> 'RustOpenBracket':
    if value is None:
        return RustOpenBracket()
    elif isinstance(value, RustOpenBracket):
        return value
    else:
        raise ValueError('the coercion from RustOpenBracket | None to RustOpenBracket failed')


@no_type_check
def _coerce_8(value: 'RustTypeExpr') -> 'RustTypeExpr':
    return value


@no_type_check
def _coerce_9(value: 'RustSemicolon | None') -> 'RustSemicolon':
    if value is None:
        return RustSemicolon()
    elif isinstance(value, RustSemicolon):
        return value
    else:
        raise ValueError('the coercion from RustSemicolon | None to RustSemicolon failed')


@no_type_check
def _coerce_10(value: 'RustExpr') -> 'RustExpr':
    return value


@no_type_check
def _coerce_11(value: 'RustCloseBracket | None') -> 'RustCloseBracket':
    if value is None:
        return RustCloseBracket()
    elif isinstance(value, RustCloseBracket):
        return value
    else:
        raise ValueError('the coercion from RustCloseBracket | None to RustCloseBracket failed')


@no_type_check
def _coerce_12(value: 'RustIdent | str') -> 'RustIdent':
    if isinstance(value, str):
        return RustIdent(value)
    elif isinstance(value, RustIdent):
        return value
    else:
        raise ValueError('the coercion from RustIdent | str to RustIdent failed')


@no_type_check
def _coerce_13(value: 'RustAngleBracketedGenericArguments | None') -> 'RustAngleBracketedGenericArguments | None':
    if isinstance(value, RustAngleBracketedGenericArguments):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustAngleBracketedGenericArguments | None to RustAngleBracketedGenericArguments | None failed')


@no_type_check
def _coerce_14(value: 'RustEquals | None') -> 'RustEquals':
    if value is None:
        return RustEquals()
    elif isinstance(value, RustEquals):
        return value
    else:
        raise ValueError('the coercion from RustEquals | None to RustEquals failed')


@no_type_check
def _coerce_15(value: 'RustHashtag | None') -> 'RustHashtag':
    if value is None:
        return RustHashtag()
    elif isinstance(value, RustHashtag):
        return value
    else:
        raise ValueError('the coercion from RustHashtag | None to RustHashtag failed')


@no_type_check
def _coerce_16(value: 'RustExclamationMark | None') -> 'RustExclamationMark | None':
    if isinstance(value, RustExclamationMark):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustExclamationMark | None to RustExclamationMark | None failed')


@no_type_check
def _coerce_17(value: 'RustMeta') -> 'RustMeta':
    return value


@no_type_check
def _coerce_18(value: 'RustOpenBrace | None') -> 'RustOpenBrace':
    if value is None:
        return RustOpenBrace()
    elif isinstance(value, RustOpenBrace):
        return value
    else:
        raise ValueError('the coercion from RustOpenBrace | None to RustOpenBrace failed')


@no_type_check
def _coerce_19(value: 'RustItem') -> 'RustItem':
    return value


@no_type_check
def _coerce_20(value: 'RustCloseBrace | None') -> 'RustCloseBrace':
    if value is None:
        return RustCloseBrace()
    elif isinstance(value, RustCloseBrace):
        return value
    else:
        raise ValueError('the coercion from RustCloseBrace | None to RustCloseBrace failed')


@no_type_check
def _coerce_21(value: 'RustForKeyword | None') -> 'RustForKeyword':
    if value is None:
        return RustForKeyword()
    elif isinstance(value, RustForKeyword):
        return value
    else:
        raise ValueError('the coercion from RustForKeyword | None to RustForKeyword failed')


@no_type_check
def _coerce_22(value: 'RustGenericParam') -> 'RustGenericParam':
    return value


@no_type_check
def _coerce_23(value: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None') -> 'Punctuated[RustGenericParam, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_22(element_value)
                    new_element_separator = _coerce_4(element_separator)
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
        raise ValueError('the coercion from Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None to Punctuated[RustGenericParam, RustComma] failed')


@no_type_check
def _coerce_24(value: 'RustOpenParen | None') -> 'RustOpenParen':
    if value is None:
        return RustOpenParen()
    elif isinstance(value, RustOpenParen):
        return value
    else:
        raise ValueError('the coercion from RustOpenParen | None to RustOpenParen failed')


@no_type_check
def _coerce_25(value: 'Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | ImmutablePunct[RustExpr, RustComma] | None') -> 'Punctuated[RustExpr, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_10(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_10(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | ImmutablePunct[RustExpr, RustComma] | None to Punctuated[RustExpr, RustComma] failed')


@no_type_check
def _coerce_26(value: 'RustCloseParen | None') -> 'RustCloseParen':
    if value is None:
        return RustCloseParen()
    elif isinstance(value, RustCloseParen):
        return value
    else:
        raise ValueError('the coercion from RustCloseParen | None to RustCloseParen failed')


@no_type_check
def _coerce_27(value: 'RustConstKeyword | None') -> 'RustConstKeyword':
    if value is None:
        return RustConstKeyword()
    elif isinstance(value, RustConstKeyword):
        return value
    else:
        raise ValueError('the coercion from RustConstKeyword | None to RustConstKeyword failed')


@no_type_check
def _coerce_28(value: 'RustColon | None') -> 'RustColon':
    if value is None:
        return RustColon()
    elif isinstance(value, RustColon):
        return value
    else:
        raise ValueError('the coercion from RustColon | None to RustColon failed')


@no_type_check
def _coerce_29(value: 'RustInit | None') -> 'RustInit | None':
    if isinstance(value, RustInit):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustInit | None to RustInit | None failed')


@no_type_check
def _coerce_30(value: 'RustAngleBracketedGenericArguments | None') -> 'RustAngleBracketedGenericArguments':
    if value is None:
        return RustAngleBracketedGenericArguments()
    elif value is None:
        return RustAngleBracketedGenericArguments()
    elif isinstance(value, RustAngleBracketedGenericArguments):
        return value
    else:
        raise ValueError('the coercion from RustAngleBracketedGenericArguments | None to RustAngleBracketedGenericArguments failed')


@no_type_check
def _coerce_31(value: 'RustTypeParamBound') -> 'RustTypeParamBound':
    return value


@no_type_check
def _coerce_32(value: 'RustPlus') -> 'RustPlus':
    return value


@no_type_check
def _coerce_33(value: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus] | None') -> 'Punctuated[RustTypeParamBound, RustPlus]':
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
                        element_separator = RustPlus()
                    new_element_value = _coerce_31(element_value)
                    new_element_separator = _coerce_32(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_31(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus] | None to Punctuated[RustTypeParamBound, RustPlus] failed')


@no_type_check
def _coerce_34(value: 'RustAttr | RustMeta') -> 'RustAttr':
    if is_rust_meta(value):
        return RustAttr(_coerce_17(value))
    elif isinstance(value, RustAttr):
        return value
    else:
        raise ValueError('the coercion from RustAttr | RustMeta to RustAttr failed')


@no_type_check
def _coerce_35(value: 'Sequence[RustAttr | RustMeta] | None') -> 'list[RustAttr]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_34(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustAttr | RustMeta] | None to list[RustAttr] failed')


@no_type_check
def _coerce_36(value: 'RustPublic | None') -> 'RustPublic | None':
    if isinstance(value, RustPublic):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPublic | None to RustPublic | None failed')


@no_type_check
def _coerce_37(value: 'RustEnumKeyword | None') -> 'RustEnumKeyword':
    if value is None:
        return RustEnumKeyword()
    elif isinstance(value, RustEnumKeyword):
        return value
    else:
        raise ValueError('the coercion from RustEnumKeyword | None to RustEnumKeyword failed')


@no_type_check
def _coerce_38(value: 'RustVariant') -> 'RustVariant':
    return value


@no_type_check
def _coerce_39(value: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | ImmutablePunct[RustVariant, RustComma] | None') -> 'Punctuated[RustVariant, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_38(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_38(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | ImmutablePunct[RustVariant, RustComma] | None to Punctuated[RustVariant, RustComma] failed')


@no_type_check
def _coerce_40(value: 'RustComma | None') -> 'RustComma | None':
    if isinstance(value, RustComma):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustComma | None to RustComma | None failed')


@no_type_check
def _coerce_41(value: 'RustDefaultKeyword | None') -> 'RustDefaultKeyword | None':
    if isinstance(value, RustDefaultKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustDefaultKeyword | None to RustDefaultKeyword | None failed')


@no_type_check
def _coerce_42(value: 'RustSignature') -> 'RustSignature':
    return value


@no_type_check
def _coerce_43(value: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma]') -> 'Punctuated[RustGenericParam, RustComma]':
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
                    element_separator = RustComma()
                new_element_value = _coerce_22(element_value)
                new_element_separator = _coerce_4(element_separator)
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
def _coerce_44(value: 'tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None') -> 'tuple[RustLessThan, Punctuated[RustGenericParam, RustComma], RustGreaterThan] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (RustLessThan(), _coerce_43(value), RustGreaterThan())
    elif isinstance(value, tuple):
        return (_coerce_2(value[0]), _coerce_23(value[1]), _coerce_6(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | ImmutablePunct[RustGenericParam, RustComma] | None to tuple[RustLessThan, Punctuated[RustGenericParam, RustComma], RustGreaterThan] | None failed')


@no_type_check
def _coerce_45(value: 'RustWherePredicate') -> 'RustWherePredicate':
    return value


@no_type_check
def _coerce_46(value: 'Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma]') -> 'Punctuated[RustWherePredicate, RustComma]':
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
                    element_separator = RustComma()
                new_element_value = _coerce_45(element_value)
                new_element_separator = _coerce_4(element_separator)
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


@no_type_check
def _coerce_47(value: 'RustWhereKeyword | None') -> 'RustWhereKeyword':
    if value is None:
        return RustWhereKeyword()
    elif isinstance(value, RustWhereKeyword):
        return value
    else:
        raise ValueError('the coercion from RustWhereKeyword | None to RustWhereKeyword failed')


@no_type_check
def _coerce_48(value: 'tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma] | None') -> 'tuple[RustWhereKeyword, Punctuated[RustWherePredicate, RustComma]] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (RustWhereKeyword(), _coerce_46(value))
    elif isinstance(value, tuple):
        return (_coerce_47(value[0]), _coerce_46(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | ImmutablePunct[RustWherePredicate, RustComma] | None to tuple[RustWhereKeyword, Punctuated[RustWherePredicate, RustComma]] | None failed')


@no_type_check
def _coerce_49(value: 'RustFnImplElement') -> 'RustFnImplElement':
    return value


@no_type_check
def _coerce_50(value: 'RustUnsafeKeyword | None') -> 'RustUnsafeKeyword | None':
    if isinstance(value, RustUnsafeKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustUnsafeKeyword | None to RustUnsafeKeyword | None failed')


@no_type_check
def _coerce_51(value: 'RustImplKeyword | None') -> 'RustImplKeyword':
    if value is None:
        return RustImplKeyword()
    elif isinstance(value, RustImplKeyword):
        return value
    else:
        raise ValueError('the coercion from RustImplKeyword | None to RustImplKeyword failed')


@no_type_check
def _coerce_52(value: 'RustGenerics | None') -> 'RustGenerics':
    if value is None:
        return RustGenerics()
    elif isinstance(value, RustGenerics):
        return value
    else:
        raise ValueError('the coercion from RustGenerics | None to RustGenerics failed')


@no_type_check
def _coerce_53(value: 'RustIdent | RustPathSegment | str') -> 'RustPathSegment':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return RustPathSegment(_coerce_12(value))
    elif isinstance(value, RustPathSegment):
        return value
    else:
        raise ValueError('the coercion from RustIdent | RustPathSegment | str to RustPathSegment failed')


@no_type_check
def _coerce_54(value: 'RustColonColon') -> 'RustColonColon':
    return value


@no_type_check
def _coerce_55(value: 'Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]') -> 'Punctuated[RustPathSegment, RustColonColon]':
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
                    element_separator = RustColonColon()
                new_element_value = _coerce_53(element_value)
                new_element_separator = _coerce_54(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_53(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_56(value: 'RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon]') -> 'RustPath':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return RustPath(_coerce_55(value))
    elif isinstance(value, RustPath):
        return value
    else:
        raise ValueError('the coercion from RustPath | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] to RustPath failed')


@no_type_check
def _coerce_57(value: 'RustPath') -> 'RustPath':
    return value


@no_type_check
def _coerce_58(value: 'RustPath | tuple[RustExclamationMark | None, RustPath, RustForKeyword | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None') -> 'tuple[RustExclamationMark | None, RustPath, RustForKeyword] | None':
    if isinstance(value, RustPath) or isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (None, _coerce_56(value), RustForKeyword())
    elif isinstance(value, tuple):
        return (_coerce_16(value[0]), _coerce_57(value[1]), _coerce_21(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPath | tuple[RustExclamationMark | None, RustPath, RustForKeyword | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None to tuple[RustExclamationMark | None, RustPath, RustForKeyword] | None failed')


@no_type_check
def _coerce_59(value: 'RustFnImplElement | RustImplElement') -> 'RustImplElement':
    if isinstance(value, RustFnImplElement):
        return RustImplElement(_coerce_49(value))
    elif isinstance(value, RustImplElement):
        return value
    else:
        raise ValueError('the coercion from RustFnImplElement | RustImplElement to RustImplElement failed')


@no_type_check
def _coerce_60(value: 'Sequence[RustFnImplElement | RustImplElement] | None') -> 'list[RustImplElement]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_59(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustFnImplElement | RustImplElement] | None to list[RustImplElement] failed')


@no_type_check
def _coerce_61(value: 'RustSingleQuote | None') -> 'RustSingleQuote':
    if value is None:
        return RustSingleQuote()
    elif isinstance(value, RustSingleQuote):
        return value
    else:
        raise ValueError('the coercion from RustSingleQuote | None to RustSingleQuote failed')


@no_type_check
def _coerce_62(value: 'RustIdent | RustLifetime | str') -> 'RustLifetime':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return RustLifetime(_coerce_12(value))
    elif isinstance(value, RustLifetime):
        return value
    else:
        raise ValueError('the coercion from RustIdent | RustLifetime | str to RustLifetime failed')


@no_type_check
def _coerce_63(value: 'Sequence[tuple[RustIdent | RustLifetime | str, RustPlus | None]] | Sequence[RustIdent | RustLifetime | str] | ImmutablePunct[RustIdent | RustLifetime | str, RustPlus]') -> 'Punctuated[RustLifetime, RustPlus]':
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
                    element_separator = RustPlus()
                new_element_value = _coerce_62(element_value)
                new_element_separator = _coerce_32(element_separator)
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
def _coerce_64(value: 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | float | str') -> 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword':
    if isinstance(value, RustChar):
        return value
    elif isinstance(value, RustFalseKeyword):
        return value
    elif isinstance(value, float):
        return RustFloat(value)
    elif isinstance(value, RustFloat):
        return value
    elif isinstance(value, str):
        return RustString(value)
    elif isinstance(value, RustString):
        return value
    elif isinstance(value, RustTrueKeyword):
        return value
    else:
        raise ValueError('the coercion from RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | float | str to RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword failed')


@no_type_check
def _coerce_65(value: 'RustToken') -> 'RustToken':
    return value


@no_type_check
def _coerce_66(value: 'Sequence[RustToken] | None') -> 'list[RustToken]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_65(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustToken] | None to list[RustToken] failed')


@no_type_check
def _coerce_67(value: 'RustRefKeyword | None') -> 'RustRefKeyword | None':
    if isinstance(value, RustRefKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustRefKeyword | None to RustRefKeyword | None failed')


@no_type_check
def _coerce_68(value: 'RustMutKeyword | None') -> 'RustMutKeyword | None':
    if isinstance(value, RustMutKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustMutKeyword | None to RustMutKeyword | None failed')


@no_type_check
def _coerce_69(value: 'RustIdent | RustNamedPattern | str') -> 'RustNamedPattern':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return RustNamedPattern(_coerce_12(value))
    elif isinstance(value, RustNamedPattern):
        return value
    else:
        raise ValueError('the coercion from RustIdent | RustNamedPattern | str to RustNamedPattern failed')


@no_type_check
def _coerce_70(value: 'RustIdent | RustNamedPattern | RustPattern | str') -> 'RustPattern':
    if isinstance(value, RustIdent) or isinstance(value, RustNamedPattern) or isinstance(value, str):
        return RustPattern(_coerce_69(value))
    elif isinstance(value, RustPattern):
        return value
    else:
        raise ValueError('the coercion from RustIdent | RustNamedPattern | RustPattern | str to RustPattern failed')


@no_type_check
def _coerce_71(value: 'RustAtSign | None') -> 'RustAtSign':
    if value is None:
        return RustAtSign()
    elif isinstance(value, RustAtSign):
        return value
    else:
        raise ValueError('the coercion from RustAtSign | None to RustAtSign failed')


@no_type_check
def _coerce_72(value: 'RustPattern') -> 'RustPattern':
    return value


@no_type_check
def _coerce_73(value: 'RustIdent | RustNamedPattern | RustPattern | tuple[RustAtSign | None, RustPattern] | None | str') -> 'tuple[RustAtSign, RustPattern] | None':
    if isinstance(value, RustIdent) or isinstance(value, RustNamedPattern) or isinstance(value, RustPattern) or isinstance(value, str):
        return (RustAtSign(), _coerce_70(value))
    elif isinstance(value, tuple):
        return (_coerce_71(value[0]), _coerce_72(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustIdent | RustNamedPattern | RustPattern | tuple[RustAtSign | None, RustPattern] | None | str to tuple[RustAtSign, RustPattern] | None failed')


@no_type_check
def _coerce_74(value: 'RustExclamationMark | None') -> 'RustExclamationMark':
    if value is None:
        return RustExclamationMark()
    elif isinstance(value, RustExclamationMark):
        return value
    else:
        raise ValueError('the coercion from RustExclamationMark | None to RustExclamationMark failed')


@no_type_check
def _coerce_75(value: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None') -> 'Punctuated[RustTypeExpr, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_8(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_8(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | ImmutablePunct[RustTypeExpr, RustComma] | None to Punctuated[RustTypeExpr, RustComma] failed')


@no_type_check
def _coerce_76(value: 'RustRArrow | None') -> 'RustRArrow':
    if value is None:
        return RustRArrow()
    elif isinstance(value, RustRArrow):
        return value
    else:
        raise ValueError('the coercion from RustRArrow | None to RustRArrow failed')


@no_type_check
def _coerce_77(value: 'RustColonColon | None') -> 'RustColonColon | None':
    if isinstance(value, RustColonColon):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustColonColon | None to RustColonColon | None failed')


@no_type_check
def _coerce_78(value: 'RustQself | None') -> 'RustQself | None':
    if isinstance(value, RustQself):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustQself | None to RustQself | None failed')


@no_type_check
def _coerce_79(value: 'RustPathArguments | None') -> 'RustPathArguments | None':
    if is_rust_path_arguments(value):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPathArguments | None to RustPathArguments | None failed')


@no_type_check
def _coerce_80(value: 'RustPubKeyword | None') -> 'RustPubKeyword':
    if value is None:
        return RustPubKeyword()
    elif isinstance(value, RustPubKeyword):
        return value
    else:
        raise ValueError('the coercion from RustPubKeyword | None to RustPubKeyword failed')


@no_type_check
def _coerce_81(value: 'RustInKeyword | None') -> 'RustInKeyword | None':
    if isinstance(value, RustInKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustInKeyword | None to RustInKeyword | None failed')


@no_type_check
def _coerce_82(value: 'RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath, RustCloseParen | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None') -> 'tuple[RustOpenParen, RustInKeyword | None, RustPath, RustCloseParen] | None':
    if isinstance(value, RustPath) or isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (RustOpenParen(), None, _coerce_56(value), RustCloseParen())
    elif isinstance(value, tuple):
        return (_coerce_24(value[0]), _coerce_81(value[1]), _coerce_57(value[2]), _coerce_26(value[3]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath, RustCloseParen | None] | Sequence[tuple[RustIdent | RustPathSegment | str, RustColonColon | None]] | Sequence[RustIdent | RustPathSegment | str] | ImmutablePunct[RustIdent | RustPathSegment | str, RustColonColon] | None to tuple[RustOpenParen, RustInKeyword | None, RustPath, RustCloseParen] | None failed')


@no_type_check
def _coerce_83(value: 'RustAsKeyword | None') -> 'RustAsKeyword':
    if value is None:
        return RustAsKeyword()
    elif isinstance(value, RustAsKeyword):
        return value
    else:
        raise ValueError('the coercion from RustAsKeyword | None to RustAsKeyword failed')


@no_type_check
def _coerce_84(value: 'RustReturnKeyword | None') -> 'RustReturnKeyword':
    if value is None:
        return RustReturnKeyword()
    elif isinstance(value, RustReturnKeyword):
        return value
    else:
        raise ValueError('the coercion from RustReturnKeyword | None to RustReturnKeyword failed')


@no_type_check
def _coerce_85(value: 'RustAmpersand | None') -> 'RustAmpersand':
    if value is None:
        return RustAmpersand()
    elif isinstance(value, RustAmpersand):
        return value
    else:
        raise ValueError('the coercion from RustAmpersand | None to RustAmpersand failed')


@no_type_check
def _coerce_86(value: 'RustLifetime') -> 'RustLifetime':
    return value


@no_type_check
def _coerce_87(value: 'RustIdent | RustLifetime | tuple[RustAmpersand | None, RustLifetime] | None | str') -> 'tuple[RustAmpersand, RustLifetime] | None':
    if isinstance(value, RustIdent) or isinstance(value, RustLifetime) or isinstance(value, str):
        return (RustAmpersand(), _coerce_62(value))
    elif isinstance(value, tuple):
        return (_coerce_85(value[0]), _coerce_86(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustIdent | RustLifetime | tuple[RustAmpersand | None, RustLifetime] | None | str to tuple[RustAmpersand, RustLifetime] | None failed')


@no_type_check
def _coerce_88(value: 'RustSelfKeyword | None') -> 'RustSelfKeyword':
    if value is None:
        return RustSelfKeyword()
    elif isinstance(value, RustSelfKeyword):
        return value
    else:
        raise ValueError('the coercion from RustSelfKeyword | None to RustSelfKeyword failed')


@no_type_check
def _coerce_89(value: 'RustConstKeyword | None') -> 'RustConstKeyword | None':
    if isinstance(value, RustConstKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustConstKeyword | None to RustConstKeyword | None failed')


@no_type_check
def _coerce_90(value: 'RustAsyncKeyword | None') -> 'RustAsyncKeyword | None':
    if isinstance(value, RustAsyncKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustAsyncKeyword | None to RustAsyncKeyword | None failed')


@no_type_check
def _coerce_91(value: 'RustAbi | RustString | None | str') -> 'RustAbi | None':
    if isinstance(value, RustString) or isinstance(value, str):
        return RustAbi(_coerce_1(value))
    elif isinstance(value, RustAbi):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustAbi | RustString | None | str to RustAbi | None failed')


@no_type_check
def _coerce_92(value: 'RustFnKeyword | None') -> 'RustFnKeyword':
    if value is None:
        return RustFnKeyword()
    elif isinstance(value, RustFnKeyword):
        return value
    else:
        raise ValueError('the coercion from RustFnKeyword | None to RustFnKeyword failed')


@no_type_check
def _coerce_93(value: 'RustArg') -> 'RustArg':
    return value


@no_type_check
def _coerce_94(value: 'Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | ImmutablePunct[RustArg, RustComma] | None') -> 'Punctuated[RustArg, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_93(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_93(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | ImmutablePunct[RustArg, RustComma] | None to Punctuated[RustArg, RustComma] failed')


@no_type_check
def _coerce_95(value: 'RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None') -> 'tuple[RustRArrow, RustTypeExpr] | None':
    if is_rust_type_expr(value):
        return (RustRArrow(), _coerce_8(value))
    elif isinstance(value, tuple):
        return (_coerce_76(value[0]), _coerce_8(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None to tuple[RustRArrow, RustTypeExpr] | None failed')


@no_type_check
def _coerce_96(value: 'RustToplevel') -> 'RustToplevel':
    return value


@no_type_check
def _coerce_97(value: 'Sequence[RustToplevel] | None') -> 'list[RustToplevel]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_96(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustToplevel] | None to list[RustToplevel] failed')


@no_type_check
def _coerce_98(value: 'RustInit') -> 'RustInit':
    return value


@no_type_check
def _coerce_99(value: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | ImmutablePunct[RustInit, RustComma] | None') -> 'Punctuated[RustInit, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_98(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_98(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | ImmutablePunct[RustInit, RustComma] | None to Punctuated[RustInit, RustComma] failed')


@no_type_check
def _coerce_100(value: 'RustStructKeyword | None') -> 'RustStructKeyword':
    if value is None:
        return RustStructKeyword()
    elif isinstance(value, RustStructKeyword):
        return value
    else:
        raise ValueError('the coercion from RustStructKeyword | None to RustStructKeyword failed')


@no_type_check
def _coerce_101(value: 'RustField') -> 'RustField':
    return value


@no_type_check
def _coerce_102(value: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | ImmutablePunct[RustField, RustComma] | None') -> 'Punctuated[RustField, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_101(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_101(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | ImmutablePunct[RustField, RustComma] | None to Punctuated[RustField, RustComma] failed')


@no_type_check
def _coerce_103(value: 'RustTraitBoundModifier | None') -> 'RustTraitBoundModifier | None':
    if isinstance(value, RustTraitBoundModifier):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustTraitBoundModifier | None to RustTraitBoundModifier | None failed')


@no_type_check
def _coerce_104(value: 'RustBoundLifetimes | None') -> 'RustBoundLifetimes | None':
    if isinstance(value, RustBoundLifetimes):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustBoundLifetimes | None to RustBoundLifetimes | None failed')


@no_type_check
def _coerce_105(value: 'RustQuestionMark | None') -> 'RustQuestionMark':
    if value is None:
        return RustQuestionMark()
    elif isinstance(value, RustQuestionMark):
        return value
    else:
        raise ValueError('the coercion from RustQuestionMark | None to RustQuestionMark failed')


@no_type_check
def _coerce_106(value: 'RustColonColon | None') -> 'RustColonColon':
    if value is None:
        return RustColonColon()
    elif isinstance(value, RustColonColon):
        return value
    else:
        raise ValueError('the coercion from RustColonColon | None to RustColonColon failed')


@no_type_check
def _coerce_107(value: 'RustPercent | None') -> 'RustPercent':
    if value is None:
        return RustPercent()
    elif isinstance(value, RustPercent):
        return value
    else:
        raise ValueError('the coercion from RustPercent | None to RustPercent failed')


@no_type_check
def _coerce_108(value: 'RustPlus | None') -> 'RustPlus':
    if value is None:
        return RustPlus()
    elif isinstance(value, RustPlus):
        return value
    else:
        raise ValueError('the coercion from RustPlus | None to RustPlus failed')


@no_type_check
def _coerce_109(value: 'RustTypeExpr | RustTypeInit | None') -> 'RustTypeInit | None':
    if is_rust_type_expr(value):
        return RustTypeInit(_coerce_8(value))
    elif isinstance(value, RustTypeInit):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustTypeExpr | RustTypeInit | None to RustTypeInit | None failed')


@no_type_check
def _coerce_110(value: 'RustBoundLifetimes | None') -> 'RustBoundLifetimes':
    if value is None:
        return RustBoundLifetimes()
    elif value is None:
        return RustBoundLifetimes()
    elif isinstance(value, RustBoundLifetimes):
        return value
    else:
        raise ValueError('the coercion from RustBoundLifetimes | None to RustBoundLifetimes failed')


@no_type_check
def _coerce_111(value: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | ImmutablePunct[RustTypeParamBound, RustPlus]') -> 'Punctuated[RustTypeParamBound, RustPlus]':
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
                    element_separator = RustPlus()
                new_element_value = _coerce_31(element_value)
                new_element_separator = _coerce_32(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_31(element_value)
                new_value.append_final(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_112(value: 'RustAsterisk | None') -> 'RustAsterisk':
    if value is None:
        return RustAsterisk()
    elif isinstance(value, RustAsterisk):
        return value
    else:
        raise ValueError('the coercion from RustAsterisk | None to RustAsterisk failed')


@no_type_check
def _coerce_113(value: 'RustUseTree') -> 'RustUseTree':
    return value


@no_type_check
def _coerce_114(value: 'Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | ImmutablePunct[RustUseTree, RustComma] | None') -> 'Punctuated[RustUseTree, RustComma]':
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
                        element_separator = RustComma()
                    new_element_value = _coerce_113(element_value)
                    new_element_separator = _coerce_4(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_113(element_value)
                    new_value.append_final(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | ImmutablePunct[RustUseTree, RustComma] | None to Punctuated[RustUseTree, RustComma] failed')


@no_type_check
def _coerce_115(value: 'RustUseKeyword | None') -> 'RustUseKeyword':
    if value is None:
        return RustUseKeyword()
    elif isinstance(value, RustUseKeyword):
        return value
    else:
        raise ValueError('the coercion from RustUseKeyword | None to RustUseKeyword failed')


@no_type_check
def _coerce_116(value: 'RustIdent | tuple[RustIdent | str, RustColonColon | None] | str') -> 'tuple[RustIdent, RustColonColon]':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return (_coerce_12(value), RustColonColon())
    elif isinstance(value, tuple):
        return (_coerce_12(value[0]), _coerce_106(value[1]))
    else:
        raise ValueError('the coercion from RustIdent | tuple[RustIdent | str, RustColonColon | None] | str to tuple[RustIdent, RustColonColon] failed')


@no_type_check
def _coerce_117(value: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None') -> 'list[tuple[RustIdent, RustColonColon]]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_116(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None to list[tuple[RustIdent, RustColonColon]] failed')


@no_type_check
def _coerce_118(value: 'RustDotDotDot | None') -> 'RustDotDotDot | None':
    if isinstance(value, RustDotDotDot):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustDotDotDot | None to RustDotDotDot | None failed')


@no_type_check
def for_each_child_rust_expr(node: RustExpr, proc: Callable[[RustExpr], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    for (element_2, separator_2) in element_1.args.args:
                                        proc(element_2)
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    for (element_3, separator_3) in element_1.args.args:
                                        proc(element_3)
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    for (element_4, separator_4) in element_1.args.params:
                                        proc(element_4)
                                    proc(element_1.args.result)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    proc(element_0.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_5, separator_5) in element_0.elements:
                        proc(element_5)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_6, separator_6) in element_0.bounds:
                    if isinstance(element_6, RustTraitBound):
                        if isinstance(element_6.bound_lifetimes, RustBoundLifetimes):
                            for (element_7, separator_7) in element_6.bound_lifetimes.lifetimes:
                                if isinstance(element_7, RustLifetime):
                                    proc(element_7)
                                elif isinstance(element_7, RustTypeParam):
                                    proc(element_7.type_param_bound)
                                    if isinstance(element_7.default, RustTypeInit):
                                        proc(element_7.default.type_expr)
                                elif isinstance(element_7, RustConstParam):
                                    proc(element_7.type_expr)
                                    if isinstance(element_7.default, RustInit):
                                        proc(element_7.default.value)
                        proc(element_6.path)
                    elif isinstance(element_6, RustLifetime):
                        proc(element_6)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        if isinstance(node.meta, RustMetaPath):
            proc(node.meta.path)
        elif isinstance(node.meta, RustMetaParenthesized):
            proc(node.meta.path)
        elif isinstance(node.meta, RustMetaBracketed):
            proc(node.meta.path)
        elif isinstance(node.meta, RustMetaBraced):
            proc(node.meta.path)
        elif isinstance(node.meta, RustMetaNameValue):
            proc(node.meta.path)
            proc(node.meta.expr)
        return
    if isinstance(node, RustBlockExpr):
        if isinstance(node.item, RustEnumItem):
            for element_8 in node.item.attrs:
                proc(element_8.meta)
            if isinstance(node.item.visibility, RustPublic):
                if isinstance(node.item.visibility.restrict, tuple):
                    proc(node.item.visibility.restrict[2])
            for (element_9, separator_8) in node.item.variants:
                if isinstance(element_9, RustStructVariant):
                    for (element_10, separator_9) in element_9.fields:
                        proc(element_10.type_expr)
                elif isinstance(element_9, RustTupleVariant):
                    for (element_11, separator_10) in element_9.types:
                        proc(element_11)
                elif isinstance(element_9, RustEmptyVariant):
                    if isinstance(element_9.init, RustInit):
                        proc(element_9.init)
        elif isinstance(node.item, RustStructItem):
            for element_12 in node.item.attrs:
                proc(element_12)
            if isinstance(node.item.visibility, RustPublic):
                proc(node.item.visibility)
            for (element_13, separator_11) in node.item.fields:
                proc(element_13)
        elif isinstance(node.item, RustUseItem):
            for element_14 in node.item.attrs:
                proc(element_14)
            if isinstance(node.item.visibility, RustPublic):
                proc(node.item.visibility)
        elif isinstance(node.item, RustExprItem):
            proc(node.item.expr)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_15, separator_12) in node.lifetimes:
            proc(element_15)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_16, separator_13) in node.args:
            proc(element_16)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_17, separator_14) in node.bounds:
            proc(element_17)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_18 in node.attrs:
            proc(element_18)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_19, separator_15) in node.variants:
            proc(element_19)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_20 in node.attrs:
            proc(element_20)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_21, separator_16) in node.signature.generics.params[1]:
                proc(element_21)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_22, separator_17) in node.signature.generics.where_clause[1]:
                if isinstance(element_22, RustTypePredicate):
                    proc(element_22.bound_lifetimes)
                    proc(element_22.type_expr)
                    for (element_23, separator_18) in element_22.bounds:
                        proc(element_23)
        for (element_24, separator_19) in node.signature.inputs:
            if isinstance(element_24, RustSelfArg):
                for element_25 in element_24.attrs:
                    proc(element_25)
                proc(element_24.type_expr)
            elif isinstance(element_24, RustTypedArg):
                for element_26 in element_24.attrs:
                    proc(element_26)
                for element_27 in element_24.pattern.named_pattern.attrs:
                    proc(element_27)
                if isinstance(element_24.pattern.named_pattern.sub, tuple):
                    proc(element_24.pattern.named_pattern.sub[1])
                proc(element_24.type_expr)
            elif isinstance(element_24, RustVariadicArg):
                for element_28 in element_24.attrs:
                    proc(element_28)
                proc(element_24.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_29, separator_20) in node.params[1]:
                proc(element_29)
        if isinstance(node.where_clause, tuple):
            for (element_30, separator_21) in node.where_clause[1]:
                proc(element_30)
        return
    if isinstance(node, RustImplElement):
        for element_31 in node.fn_impl_element.attrs:
            proc(element_31)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_32 in node.attrs:
            proc(element_32)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_33 in node.impl_elements:
            proc(element_33.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_34 in node.attrs:
            proc(element_34)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_35, separator_22) in node.params:
            proc(element_35)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_36, separator_23) in node.segments:
            proc(element_36)
        return
    if isinstance(node, RustPathExpr):
        for element_37 in node.attrs:
            proc(element_37)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_38 in node.attrs:
            proc(element_38)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_39, separator_24) in node.inputs:
            proc(element_39)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_40 in node.items:
            if isinstance(element_40, RustEnumItem):
                proc(element_40)
            elif isinstance(element_40, RustStructItem):
                proc(element_40)
            elif isinstance(element_40, RustUseItem):
                proc(element_40)
            elif isinstance(element_40, RustImplItem):
                for element_41 in element_40.attrs:
                    proc(element_41)
                proc(element_40.generics)
                if isinstance(element_40.trait, tuple):
                    proc(element_40.trait[1])
                proc(element_40.type_expr)
                for element_42 in element_40.impl_elements:
                    proc(element_42)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_43, separator_25) in node.inits:
            proc(element_43)
        return
    if isinstance(node, RustStructItem):
        for element_44 in node.attrs:
            proc(element_44)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_45, separator_26) in node.fields:
            proc(element_45)
        return
    if isinstance(node, RustStructVariant):
        for (element_46, separator_27) in node.fields:
            proc(element_46)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_47, separator_28) in node.elements:
            proc(element_47)
        return
    if isinstance(node, RustTupleVariant):
        for (element_48, separator_29) in node.types:
            proc(element_48)
        return
    if isinstance(node, RustTurbofish):
        for (element_49, separator_30) in node.args:
            proc(element_49)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_50, separator_31) in node.bounds:
            proc(element_50)
        return
    if isinstance(node, RustTypedArg):
        for element_51 in node.attrs:
            proc(element_51)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_52 in node.attrs:
            proc(element_52)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_53 in node.attrs:
            proc(element_53)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_generic_argument(node: RustGenericArgument, proc: Callable[[RustGenericArgument], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            proc(element_0)
        return
    if isinstance(node, RustArrayTypeExpr):
        if isinstance(node.type_expr, RustPathTypeExpr):
            if isinstance(node.type_expr.qself, RustQself):
                proc(node.type_expr.qself.type_expr)
                for (element_1, separator_1) in node.type_expr.qself.path.segments:
                    if is_rust_path_arguments(element_1.args):
                        if isinstance(element_1.args, RustTurbofish):
                            for (element_2, separator_2) in element_1.args.args:
                                proc(element_2)
                        elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                            for (element_3, separator_3) in element_1.args.args:
                                proc(element_3)
                        elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                            for (element_4, separator_4) in element_1.args.params:
                                proc(element_4)
                            proc(element_1.args.result)
            proc(node.type_expr.path)
        elif isinstance(node.type_expr, RustArrayTypeExpr):
            proc(node.type_expr.type_expr)
            if isinstance(node.type_expr.expr, RustPathExpr):
                for element_5 in node.type_expr.expr.attrs:
                    if isinstance(element_5.meta, RustMetaPath):
                        proc(element_5.meta.path)
                    elif isinstance(element_5.meta, RustMetaParenthesized):
                        proc(element_5.meta.path)
                    elif isinstance(element_5.meta, RustMetaBracketed):
                        proc(element_5.meta.path)
                    elif isinstance(element_5.meta, RustMetaBraced):
                        proc(element_5.meta.path)
                    elif isinstance(element_5.meta, RustMetaNameValue):
                        proc(element_5.meta.path)
                        proc(element_5.meta.expr)
                if isinstance(node.type_expr.expr.qself, RustQself):
                    proc(node.type_expr.expr.qself)
                proc(node.type_expr.expr.path)
            elif isinstance(node.type_expr.expr, RustCallExpr):
                proc(node.type_expr.expr.operator)
                for (element_6, separator_5) in node.type_expr.expr.args:
                    proc(element_6)
            elif isinstance(node.type_expr.expr, RustStructExpr):
                proc(node.type_expr.expr.path)
                for (element_7, separator_6) in node.type_expr.expr.inits:
                    proc(element_7.value)
            elif isinstance(node.type_expr.expr, RustBlockExpr):
                if isinstance(node.type_expr.expr.item, RustEnumItem):
                    for element_8 in node.type_expr.expr.item.attrs:
                        proc(element_8)
                    if isinstance(node.type_expr.expr.item.visibility, RustPublic):
                        if isinstance(node.type_expr.expr.item.visibility.restrict, tuple):
                            proc(node.type_expr.expr.item.visibility.restrict[2])
                    for (element_9, separator_7) in node.type_expr.expr.item.variants:
                        if isinstance(element_9, RustStructVariant):
                            for (element_10, separator_8) in element_9.fields:
                                proc(element_10.type_expr)
                        elif isinstance(element_9, RustTupleVariant):
                            for (element_11, separator_9) in element_9.types:
                                proc(element_11)
                        elif isinstance(element_9, RustEmptyVariant):
                            if isinstance(element_9.init, RustInit):
                                proc(element_9.init)
                elif isinstance(node.type_expr.expr.item, RustStructItem):
                    for element_12 in node.type_expr.expr.item.attrs:
                        proc(element_12)
                    if isinstance(node.type_expr.expr.item.visibility, RustPublic):
                        proc(node.type_expr.expr.item.visibility)
                    for (element_13, separator_10) in node.type_expr.expr.item.fields:
                        proc(element_13)
                elif isinstance(node.type_expr.expr.item, RustUseItem):
                    for element_14 in node.type_expr.expr.item.attrs:
                        proc(element_14)
                    if isinstance(node.type_expr.expr.item.visibility, RustPublic):
                        proc(node.type_expr.expr.item.visibility)
                elif isinstance(node.type_expr.expr.item, RustExprItem):
                    proc(node.type_expr.expr.item.expr)
                proc(node.type_expr.expr.last)
            elif isinstance(node.type_expr.expr, RustRetExpr):
                proc(node.type_expr.expr.expr)
        elif isinstance(node.type_expr, RustTupleTypeExpr):
            for (element_15, separator_11) in node.type_expr.elements:
                proc(element_15)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_16, separator_12) in node.lifetimes:
            if isinstance(element_16, RustLifetime):
                proc(element_16)
            elif isinstance(element_16, RustTypeParam):
                if isinstance(element_16.type_param_bound, RustTraitBound):
                    if isinstance(element_16.type_param_bound.bound_lifetimes, RustBoundLifetimes):
                        for (element_17, separator_13) in element_16.type_param_bound.bound_lifetimes.lifetimes:
                            proc(element_17)
                    proc(element_16.type_param_bound.path)
                elif isinstance(element_16.type_param_bound, RustLifetime):
                    proc(element_16.type_param_bound)
                if isinstance(element_16.default, RustTypeInit):
                    proc(element_16.default.type_expr)
            elif isinstance(element_16, RustConstParam):
                proc(element_16.type_expr)
                if isinstance(element_16.default, RustInit):
                    proc(element_16.default)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_18, separator_14) in node.args:
            proc(element_18)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_19, separator_15) in node.bounds:
            proc(element_19)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_20 in node.attrs:
            proc(element_20)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_21, separator_16) in node.variants:
            proc(element_21)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_22 in node.attrs:
            proc(element_22)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_23, separator_17) in node.signature.generics.params[1]:
                proc(element_23)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_24, separator_18) in node.signature.generics.where_clause[1]:
                if isinstance(element_24, RustTypePredicate):
                    proc(element_24.bound_lifetimes)
                    proc(element_24.type_expr)
                    for (element_25, separator_19) in element_24.bounds:
                        proc(element_25)
        for (element_26, separator_20) in node.signature.inputs:
            if isinstance(element_26, RustSelfArg):
                for element_27 in element_26.attrs:
                    proc(element_27)
                proc(element_26.type_expr)
            elif isinstance(element_26, RustTypedArg):
                for element_28 in element_26.attrs:
                    proc(element_28)
                for element_29 in element_26.pattern.named_pattern.attrs:
                    proc(element_29)
                if isinstance(element_26.pattern.named_pattern.sub, tuple):
                    proc(element_26.pattern.named_pattern.sub[1])
                proc(element_26.type_expr)
            elif isinstance(element_26, RustVariadicArg):
                for element_30 in element_26.attrs:
                    proc(element_30)
                proc(element_26.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_31, separator_21) in node.params[1]:
                proc(element_31)
        if isinstance(node.where_clause, tuple):
            for (element_32, separator_22) in node.where_clause[1]:
                proc(element_32)
        return
    if isinstance(node, RustImplElement):
        for element_33 in node.fn_impl_element.attrs:
            proc(element_33)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_34 in node.attrs:
            proc(element_34)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_35 in node.impl_elements:
            proc(element_35.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_36 in node.attrs:
            proc(element_36)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_37, separator_23) in node.params:
            proc(element_37)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_38, separator_24) in node.segments:
            proc(element_38)
        return
    if isinstance(node, RustPathExpr):
        for element_39 in node.attrs:
            proc(element_39)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_40 in node.attrs:
            proc(element_40)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_41, separator_25) in node.inputs:
            proc(element_41)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_42 in node.items:
            if isinstance(element_42, RustEnumItem):
                proc(element_42)
            elif isinstance(element_42, RustStructItem):
                proc(element_42)
            elif isinstance(element_42, RustUseItem):
                proc(element_42)
            elif isinstance(element_42, RustImplItem):
                for element_43 in element_42.attrs:
                    proc(element_43)
                proc(element_42.generics)
                if isinstance(element_42.trait, tuple):
                    proc(element_42.trait[1])
                proc(element_42.type_expr)
                for element_44 in element_42.impl_elements:
                    proc(element_44)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_45, separator_26) in node.inits:
            proc(element_45)
        return
    if isinstance(node, RustStructItem):
        for element_46 in node.attrs:
            proc(element_46)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_47, separator_27) in node.fields:
            proc(element_47)
        return
    if isinstance(node, RustStructVariant):
        for (element_48, separator_28) in node.fields:
            proc(element_48)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_49, separator_29) in node.elements:
            proc(element_49)
        return
    if isinstance(node, RustTupleVariant):
        for (element_50, separator_30) in node.types:
            proc(element_50)
        return
    if isinstance(node, RustTurbofish):
        for (element_51, separator_31) in node.args:
            proc(element_51)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_52, separator_32) in node.bounds:
            proc(element_52)
        return
    if isinstance(node, RustTypedArg):
        for element_53 in node.attrs:
            proc(element_53)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_54 in node.attrs:
            proc(element_54)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_55 in node.attrs:
            proc(element_55)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_generic_param(node: RustGenericParam, proc: Callable[[RustGenericParam], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if isinstance(element_0, RustLifetime):
                proc(element_0)
            elif is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    for (element_2, separator_2) in element_1.args.args:
                                        proc(element_2)
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    for (element_3, separator_3) in element_1.args.args:
                                        proc(element_3)
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    for (element_4, separator_4) in element_1.args.params:
                                        proc(element_4)
                                    proc(element_1.args.result)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    if isinstance(element_0.expr, RustPathExpr):
                        for element_5 in element_0.expr.attrs:
                            if isinstance(element_5.meta, RustMetaPath):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaParenthesized):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBracketed):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBraced):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaNameValue):
                                proc(element_5.meta.path)
                                proc(element_5.meta.expr)
                        if isinstance(element_0.expr.qself, RustQself):
                            proc(element_0.expr.qself)
                        proc(element_0.expr.path)
                    elif isinstance(element_0.expr, RustCallExpr):
                        proc(element_0.expr.operator)
                        for (element_6, separator_5) in element_0.expr.args:
                            proc(element_6)
                    elif isinstance(element_0.expr, RustStructExpr):
                        proc(element_0.expr.path)
                        for (element_7, separator_6) in element_0.expr.inits:
                            proc(element_7.value)
                    elif isinstance(element_0.expr, RustBlockExpr):
                        if isinstance(element_0.expr.item, RustEnumItem):
                            for element_8 in element_0.expr.item.attrs:
                                proc(element_8)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                if isinstance(element_0.expr.item.visibility.restrict, tuple):
                                    proc(element_0.expr.item.visibility.restrict[2])
                            for (element_9, separator_7) in element_0.expr.item.variants:
                                if isinstance(element_9, RustStructVariant):
                                    for (element_10, separator_8) in element_9.fields:
                                        proc(element_10.type_expr)
                                elif isinstance(element_9, RustTupleVariant):
                                    for (element_11, separator_9) in element_9.types:
                                        proc(element_11)
                                elif isinstance(element_9, RustEmptyVariant):
                                    if isinstance(element_9.init, RustInit):
                                        proc(element_9.init)
                        elif isinstance(element_0.expr.item, RustStructItem):
                            for element_12 in element_0.expr.item.attrs:
                                proc(element_12)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                            for (element_13, separator_10) in element_0.expr.item.fields:
                                proc(element_13)
                        elif isinstance(element_0.expr.item, RustUseItem):
                            for element_14 in element_0.expr.item.attrs:
                                proc(element_14)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                        elif isinstance(element_0.expr.item, RustExprItem):
                            proc(element_0.expr.item.expr)
                        proc(element_0.expr.last)
                    elif isinstance(element_0.expr, RustRetExpr):
                        proc(element_0.expr.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_15, separator_11) in element_0.elements:
                        proc(element_15)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_16, separator_12) in element_0.bounds:
                    if isinstance(element_16, RustTraitBound):
                        if isinstance(element_16.bound_lifetimes, RustBoundLifetimes):
                            for (element_17, separator_13) in element_16.bound_lifetimes.lifetimes:
                                proc(element_17)
                        proc(element_16.path)
                    elif isinstance(element_16, RustLifetime):
                        proc(element_16)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_18, separator_14) in node.lifetimes:
            proc(element_18)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_19, separator_15) in node.args:
            proc(element_19)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_20, separator_16) in node.bounds:
            proc(element_20)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_21 in node.attrs:
            proc(element_21)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_22, separator_17) in node.variants:
            proc(element_22)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_23 in node.attrs:
            proc(element_23)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_24, separator_18) in node.signature.generics.params[1]:
                proc(element_24)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_25, separator_19) in node.signature.generics.where_clause[1]:
                if isinstance(element_25, RustTypePredicate):
                    proc(element_25.bound_lifetimes)
                    proc(element_25.type_expr)
                    for (element_26, separator_20) in element_25.bounds:
                        proc(element_26)
        for (element_27, separator_21) in node.signature.inputs:
            if isinstance(element_27, RustSelfArg):
                for element_28 in element_27.attrs:
                    proc(element_28)
                proc(element_27.type_expr)
            elif isinstance(element_27, RustTypedArg):
                for element_29 in element_27.attrs:
                    proc(element_29)
                for element_30 in element_27.pattern.named_pattern.attrs:
                    proc(element_30)
                if isinstance(element_27.pattern.named_pattern.sub, tuple):
                    proc(element_27.pattern.named_pattern.sub[1])
                proc(element_27.type_expr)
            elif isinstance(element_27, RustVariadicArg):
                for element_31 in element_27.attrs:
                    proc(element_31)
                proc(element_27.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_32, separator_22) in node.params[1]:
                proc(element_32)
        if isinstance(node.where_clause, tuple):
            for (element_33, separator_23) in node.where_clause[1]:
                proc(element_33)
        return
    if isinstance(node, RustImplElement):
        for element_34 in node.fn_impl_element.attrs:
            proc(element_34)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_35 in node.attrs:
            proc(element_35)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_36 in node.impl_elements:
            proc(element_36.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_37 in node.attrs:
            proc(element_37)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_38, separator_24) in node.params:
            proc(element_38)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_39, separator_25) in node.segments:
            proc(element_39)
        return
    if isinstance(node, RustPathExpr):
        for element_40 in node.attrs:
            proc(element_40)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_41 in node.attrs:
            proc(element_41)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_42, separator_26) in node.inputs:
            proc(element_42)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_43 in node.items:
            if isinstance(element_43, RustEnumItem):
                proc(element_43)
            elif isinstance(element_43, RustStructItem):
                proc(element_43)
            elif isinstance(element_43, RustUseItem):
                proc(element_43)
            elif isinstance(element_43, RustImplItem):
                for element_44 in element_43.attrs:
                    proc(element_44)
                proc(element_43.generics)
                if isinstance(element_43.trait, tuple):
                    proc(element_43.trait[1])
                proc(element_43.type_expr)
                for element_45 in element_43.impl_elements:
                    proc(element_45)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_46, separator_27) in node.inits:
            proc(element_46)
        return
    if isinstance(node, RustStructItem):
        for element_47 in node.attrs:
            proc(element_47)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_48, separator_28) in node.fields:
            proc(element_48)
        return
    if isinstance(node, RustStructVariant):
        for (element_49, separator_29) in node.fields:
            proc(element_49)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_50, separator_30) in node.elements:
            proc(element_50)
        return
    if isinstance(node, RustTupleVariant):
        for (element_51, separator_31) in node.types:
            proc(element_51)
        return
    if isinstance(node, RustTurbofish):
        for (element_52, separator_32) in node.args:
            proc(element_52)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default.type_expr)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_53, separator_33) in node.bounds:
            proc(element_53)
        return
    if isinstance(node, RustTypedArg):
        for element_54 in node.attrs:
            proc(element_54)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_55 in node.attrs:
            proc(element_55)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_56 in node.attrs:
            proc(element_56)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_item(node: RustItem, proc: Callable[[RustItem], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    for (element_2, separator_2) in element_1.args.args:
                                        proc(element_2)
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    for (element_3, separator_3) in element_1.args.args:
                                        proc(element_3)
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    for (element_4, separator_4) in element_1.args.params:
                                        proc(element_4)
                                    proc(element_1.args.result)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    if isinstance(element_0.expr, RustPathExpr):
                        for element_5 in element_0.expr.attrs:
                            if isinstance(element_5.meta, RustMetaPath):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaParenthesized):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBracketed):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBraced):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaNameValue):
                                proc(element_5.meta.path)
                                proc(element_5.meta.expr)
                        if isinstance(element_0.expr.qself, RustQself):
                            proc(element_0.expr.qself)
                        proc(element_0.expr.path)
                    elif isinstance(element_0.expr, RustCallExpr):
                        proc(element_0.expr.operator)
                        for (element_6, separator_5) in element_0.expr.args:
                            proc(element_6)
                    elif isinstance(element_0.expr, RustStructExpr):
                        proc(element_0.expr.path)
                        for (element_7, separator_6) in element_0.expr.inits:
                            proc(element_7.value)
                    elif isinstance(element_0.expr, RustBlockExpr):
                        proc(element_0.expr.item)
                        proc(element_0.expr.last)
                    elif isinstance(element_0.expr, RustRetExpr):
                        proc(element_0.expr.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_8, separator_7) in element_0.elements:
                        proc(element_8)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_9, separator_8) in element_0.bounds:
                    if isinstance(element_9, RustTraitBound):
                        if isinstance(element_9.bound_lifetimes, RustBoundLifetimes):
                            for (element_10, separator_9) in element_9.bound_lifetimes.lifetimes:
                                if isinstance(element_10, RustLifetime):
                                    proc(element_10)
                                elif isinstance(element_10, RustTypeParam):
                                    proc(element_10.type_param_bound)
                                    if isinstance(element_10.default, RustTypeInit):
                                        proc(element_10.default.type_expr)
                                elif isinstance(element_10, RustConstParam):
                                    proc(element_10.type_expr)
                                    if isinstance(element_10.default, RustInit):
                                        proc(element_10.default)
                        proc(element_9.path)
                    elif isinstance(element_9, RustLifetime):
                        proc(element_9)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_11, separator_10) in node.lifetimes:
            proc(element_11)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_12, separator_11) in node.args:
            proc(element_12)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_13, separator_12) in node.bounds:
            proc(element_13)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_14 in node.attrs:
            proc(element_14)
        if isinstance(node.visibility, RustPublic):
            if isinstance(node.visibility.restrict, tuple):
                proc(node.visibility.restrict[2])
        for (element_15, separator_13) in node.variants:
            if isinstance(element_15, RustStructVariant):
                for (element_16, separator_14) in element_15.fields:
                    proc(element_16.type_expr)
            elif isinstance(element_15, RustTupleVariant):
                for (element_17, separator_15) in element_15.types:
                    proc(element_17)
            elif isinstance(element_15, RustEmptyVariant):
                if isinstance(element_15.init, RustInit):
                    proc(element_15.init)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_18 in node.attrs:
            proc(element_18)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_19, separator_16) in node.signature.generics.params[1]:
                proc(element_19)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_20, separator_17) in node.signature.generics.where_clause[1]:
                if isinstance(element_20, RustTypePredicate):
                    proc(element_20.bound_lifetimes)
                    proc(element_20.type_expr)
                    for (element_21, separator_18) in element_20.bounds:
                        proc(element_21)
        for (element_22, separator_19) in node.signature.inputs:
            if isinstance(element_22, RustSelfArg):
                for element_23 in element_22.attrs:
                    proc(element_23)
                proc(element_22.type_expr)
            elif isinstance(element_22, RustTypedArg):
                for element_24 in element_22.attrs:
                    proc(element_24)
                for element_25 in element_22.pattern.named_pattern.attrs:
                    proc(element_25)
                if isinstance(element_22.pattern.named_pattern.sub, tuple):
                    proc(element_22.pattern.named_pattern.sub[1])
                proc(element_22.type_expr)
            elif isinstance(element_22, RustVariadicArg):
                for element_26 in element_22.attrs:
                    proc(element_26)
                proc(element_22.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_27, separator_20) in node.params[1]:
                proc(element_27)
        if isinstance(node.where_clause, tuple):
            for (element_28, separator_21) in node.where_clause[1]:
                proc(element_28)
        return
    if isinstance(node, RustImplElement):
        for element_29 in node.fn_impl_element.attrs:
            proc(element_29)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_30 in node.attrs:
            proc(element_30)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_31 in node.impl_elements:
            proc(element_31.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_32 in node.attrs:
            proc(element_32)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_33, separator_22) in node.params:
            proc(element_33)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_34, separator_23) in node.segments:
            proc(element_34)
        return
    if isinstance(node, RustPathExpr):
        for element_35 in node.attrs:
            proc(element_35)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_36 in node.attrs:
            proc(element_36)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_37, separator_24) in node.inputs:
            proc(element_37)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_38 in node.items:
            if isinstance(element_38, RustEnumItem):
                proc(element_38)
            elif isinstance(element_38, RustStructItem):
                proc(element_38)
            elif isinstance(element_38, RustUseItem):
                proc(element_38)
            elif isinstance(element_38, RustImplItem):
                for element_39 in element_38.attrs:
                    proc(element_39)
                proc(element_38.generics)
                if isinstance(element_38.trait, tuple):
                    proc(element_38.trait[1])
                proc(element_38.type_expr)
                for element_40 in element_38.impl_elements:
                    proc(element_40)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_41, separator_25) in node.inits:
            proc(element_41)
        return
    if isinstance(node, RustStructItem):
        for element_42 in node.attrs:
            proc(element_42)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_43, separator_26) in node.fields:
            proc(element_43)
        return
    if isinstance(node, RustStructVariant):
        for (element_44, separator_27) in node.fields:
            proc(element_44)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_45, separator_28) in node.elements:
            proc(element_45)
        return
    if isinstance(node, RustTupleVariant):
        for (element_46, separator_29) in node.types:
            proc(element_46)
        return
    if isinstance(node, RustTurbofish):
        for (element_47, separator_30) in node.args:
            proc(element_47)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_48, separator_31) in node.bounds:
            proc(element_48)
        return
    if isinstance(node, RustTypedArg):
        for element_49 in node.attrs:
            proc(element_49)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_50 in node.attrs:
            proc(element_50)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_51 in node.attrs:
            proc(element_51)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_meta(node: RustMeta, proc: Callable[[RustMeta], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    for (element_2, separator_2) in element_1.args.args:
                                        proc(element_2)
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    for (element_3, separator_3) in element_1.args.args:
                                        proc(element_3)
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    for (element_4, separator_4) in element_1.args.params:
                                        proc(element_4)
                                    proc(element_1.args.result)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    if isinstance(element_0.expr, RustPathExpr):
                        for element_5 in element_0.expr.attrs:
                            proc(element_5.meta)
                        if isinstance(element_0.expr.qself, RustQself):
                            proc(element_0.expr.qself)
                        proc(element_0.expr.path)
                    elif isinstance(element_0.expr, RustCallExpr):
                        proc(element_0.expr.operator)
                        for (element_6, separator_5) in element_0.expr.args:
                            proc(element_6)
                    elif isinstance(element_0.expr, RustStructExpr):
                        proc(element_0.expr.path)
                        for (element_7, separator_6) in element_0.expr.inits:
                            proc(element_7.value)
                    elif isinstance(element_0.expr, RustBlockExpr):
                        if isinstance(element_0.expr.item, RustEnumItem):
                            for element_8 in element_0.expr.item.attrs:
                                proc(element_8)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                if isinstance(element_0.expr.item.visibility.restrict, tuple):
                                    proc(element_0.expr.item.visibility.restrict[2])
                            for (element_9, separator_7) in element_0.expr.item.variants:
                                if isinstance(element_9, RustStructVariant):
                                    for (element_10, separator_8) in element_9.fields:
                                        proc(element_10.type_expr)
                                elif isinstance(element_9, RustTupleVariant):
                                    for (element_11, separator_9) in element_9.types:
                                        proc(element_11)
                                elif isinstance(element_9, RustEmptyVariant):
                                    if isinstance(element_9.init, RustInit):
                                        proc(element_9.init)
                        elif isinstance(element_0.expr.item, RustStructItem):
                            for element_12 in element_0.expr.item.attrs:
                                proc(element_12)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                            for (element_13, separator_10) in element_0.expr.item.fields:
                                proc(element_13)
                        elif isinstance(element_0.expr.item, RustUseItem):
                            for element_14 in element_0.expr.item.attrs:
                                proc(element_14)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                        elif isinstance(element_0.expr.item, RustExprItem):
                            proc(element_0.expr.item.expr)
                        proc(element_0.expr.last)
                    elif isinstance(element_0.expr, RustRetExpr):
                        proc(element_0.expr.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_15, separator_11) in element_0.elements:
                        proc(element_15)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_16, separator_12) in element_0.bounds:
                    if isinstance(element_16, RustTraitBound):
                        if isinstance(element_16.bound_lifetimes, RustBoundLifetimes):
                            for (element_17, separator_13) in element_16.bound_lifetimes.lifetimes:
                                if isinstance(element_17, RustLifetime):
                                    proc(element_17)
                                elif isinstance(element_17, RustTypeParam):
                                    proc(element_17.type_param_bound)
                                    if isinstance(element_17.default, RustTypeInit):
                                        proc(element_17.default.type_expr)
                                elif isinstance(element_17, RustConstParam):
                                    proc(element_17.type_expr)
                                    if isinstance(element_17.default, RustInit):
                                        proc(element_17.default)
                        proc(element_16.path)
                    elif isinstance(element_16, RustLifetime):
                        proc(element_16)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_18, separator_14) in node.lifetimes:
            proc(element_18)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_19, separator_15) in node.args:
            proc(element_19)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_20, separator_16) in node.bounds:
            proc(element_20)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_21 in node.attrs:
            proc(element_21)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_22, separator_17) in node.variants:
            proc(element_22)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_23 in node.attrs:
            proc(element_23)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_24, separator_18) in node.signature.generics.params[1]:
                proc(element_24)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_25, separator_19) in node.signature.generics.where_clause[1]:
                if isinstance(element_25, RustTypePredicate):
                    proc(element_25.bound_lifetimes)
                    proc(element_25.type_expr)
                    for (element_26, separator_20) in element_25.bounds:
                        proc(element_26)
        for (element_27, separator_21) in node.signature.inputs:
            if isinstance(element_27, RustSelfArg):
                for element_28 in element_27.attrs:
                    proc(element_28)
                proc(element_27.type_expr)
            elif isinstance(element_27, RustTypedArg):
                for element_29 in element_27.attrs:
                    proc(element_29)
                for element_30 in element_27.pattern.named_pattern.attrs:
                    proc(element_30)
                if isinstance(element_27.pattern.named_pattern.sub, tuple):
                    proc(element_27.pattern.named_pattern.sub[1])
                proc(element_27.type_expr)
            elif isinstance(element_27, RustVariadicArg):
                for element_31 in element_27.attrs:
                    proc(element_31)
                proc(element_27.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_32, separator_22) in node.params[1]:
                proc(element_32)
        if isinstance(node.where_clause, tuple):
            for (element_33, separator_23) in node.where_clause[1]:
                proc(element_33)
        return
    if isinstance(node, RustImplElement):
        for element_34 in node.fn_impl_element.attrs:
            proc(element_34)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_35 in node.attrs:
            proc(element_35)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_36 in node.impl_elements:
            proc(element_36.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_37 in node.attrs:
            proc(element_37)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_38, separator_24) in node.params:
            proc(element_38)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_39, separator_25) in node.segments:
            proc(element_39)
        return
    if isinstance(node, RustPathExpr):
        for element_40 in node.attrs:
            proc(element_40)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_41 in node.attrs:
            proc(element_41)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_42, separator_26) in node.inputs:
            proc(element_42)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_43 in node.items:
            if isinstance(element_43, RustEnumItem):
                proc(element_43)
            elif isinstance(element_43, RustStructItem):
                proc(element_43)
            elif isinstance(element_43, RustUseItem):
                proc(element_43)
            elif isinstance(element_43, RustImplItem):
                for element_44 in element_43.attrs:
                    proc(element_44)
                proc(element_43.generics)
                if isinstance(element_43.trait, tuple):
                    proc(element_43.trait[1])
                proc(element_43.type_expr)
                for element_45 in element_43.impl_elements:
                    proc(element_45)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_46, separator_27) in node.inits:
            proc(element_46)
        return
    if isinstance(node, RustStructItem):
        for element_47 in node.attrs:
            proc(element_47)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_48, separator_28) in node.fields:
            proc(element_48)
        return
    if isinstance(node, RustStructVariant):
        for (element_49, separator_29) in node.fields:
            proc(element_49)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_50, separator_30) in node.elements:
            proc(element_50)
        return
    if isinstance(node, RustTupleVariant):
        for (element_51, separator_31) in node.types:
            proc(element_51)
        return
    if isinstance(node, RustTurbofish):
        for (element_52, separator_32) in node.args:
            proc(element_52)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_53, separator_33) in node.bounds:
            proc(element_53)
        return
    if isinstance(node, RustTypedArg):
        for element_54 in node.attrs:
            proc(element_54)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_55 in node.attrs:
            proc(element_55)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_56 in node.attrs:
            proc(element_56)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_path_arguments(node: RustPathArguments, proc: Callable[[RustPathArguments], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                proc(element_1.args)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    if isinstance(element_0.expr, RustPathExpr):
                        for element_2 in element_0.expr.attrs:
                            if isinstance(element_2.meta, RustMetaPath):
                                proc(element_2.meta.path)
                            elif isinstance(element_2.meta, RustMetaParenthesized):
                                proc(element_2.meta.path)
                            elif isinstance(element_2.meta, RustMetaBracketed):
                                proc(element_2.meta.path)
                            elif isinstance(element_2.meta, RustMetaBraced):
                                proc(element_2.meta.path)
                            elif isinstance(element_2.meta, RustMetaNameValue):
                                proc(element_2.meta.path)
                                proc(element_2.meta.expr)
                        if isinstance(element_0.expr.qself, RustQself):
                            proc(element_0.expr.qself)
                        proc(element_0.expr.path)
                    elif isinstance(element_0.expr, RustCallExpr):
                        proc(element_0.expr.operator)
                        for (element_3, separator_2) in element_0.expr.args:
                            proc(element_3)
                    elif isinstance(element_0.expr, RustStructExpr):
                        proc(element_0.expr.path)
                        for (element_4, separator_3) in element_0.expr.inits:
                            proc(element_4.value)
                    elif isinstance(element_0.expr, RustBlockExpr):
                        if isinstance(element_0.expr.item, RustEnumItem):
                            for element_5 in element_0.expr.item.attrs:
                                proc(element_5)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                if isinstance(element_0.expr.item.visibility.restrict, tuple):
                                    proc(element_0.expr.item.visibility.restrict[2])
                            for (element_6, separator_4) in element_0.expr.item.variants:
                                if isinstance(element_6, RustStructVariant):
                                    for (element_7, separator_5) in element_6.fields:
                                        proc(element_7.type_expr)
                                elif isinstance(element_6, RustTupleVariant):
                                    for (element_8, separator_6) in element_6.types:
                                        proc(element_8)
                                elif isinstance(element_6, RustEmptyVariant):
                                    if isinstance(element_6.init, RustInit):
                                        proc(element_6.init)
                        elif isinstance(element_0.expr.item, RustStructItem):
                            for element_9 in element_0.expr.item.attrs:
                                proc(element_9)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                            for (element_10, separator_7) in element_0.expr.item.fields:
                                proc(element_10)
                        elif isinstance(element_0.expr.item, RustUseItem):
                            for element_11 in element_0.expr.item.attrs:
                                proc(element_11)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                        elif isinstance(element_0.expr.item, RustExprItem):
                            proc(element_0.expr.item.expr)
                        proc(element_0.expr.last)
                    elif isinstance(element_0.expr, RustRetExpr):
                        proc(element_0.expr.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_12, separator_8) in element_0.elements:
                        proc(element_12)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_13, separator_9) in element_0.bounds:
                    if isinstance(element_13, RustTraitBound):
                        if isinstance(element_13.bound_lifetimes, RustBoundLifetimes):
                            for (element_14, separator_10) in element_13.bound_lifetimes.lifetimes:
                                if isinstance(element_14, RustLifetime):
                                    proc(element_14)
                                elif isinstance(element_14, RustTypeParam):
                                    proc(element_14.type_param_bound)
                                    if isinstance(element_14.default, RustTypeInit):
                                        proc(element_14.default.type_expr)
                                elif isinstance(element_14, RustConstParam):
                                    proc(element_14.type_expr)
                                    if isinstance(element_14.default, RustInit):
                                        proc(element_14.default)
                        proc(element_13.path)
                    elif isinstance(element_13, RustLifetime):
                        proc(element_13)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_15, separator_11) in node.lifetimes:
            proc(element_15)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_16, separator_12) in node.args:
            proc(element_16)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_17, separator_13) in node.bounds:
            proc(element_17)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_18 in node.attrs:
            proc(element_18)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_19, separator_14) in node.variants:
            proc(element_19)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_20 in node.attrs:
            proc(element_20)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_21, separator_15) in node.signature.generics.params[1]:
                proc(element_21)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_22, separator_16) in node.signature.generics.where_clause[1]:
                if isinstance(element_22, RustTypePredicate):
                    proc(element_22.bound_lifetimes)
                    proc(element_22.type_expr)
                    for (element_23, separator_17) in element_22.bounds:
                        proc(element_23)
        for (element_24, separator_18) in node.signature.inputs:
            if isinstance(element_24, RustSelfArg):
                for element_25 in element_24.attrs:
                    proc(element_25)
                proc(element_24.type_expr)
            elif isinstance(element_24, RustTypedArg):
                for element_26 in element_24.attrs:
                    proc(element_26)
                for element_27 in element_24.pattern.named_pattern.attrs:
                    proc(element_27)
                if isinstance(element_24.pattern.named_pattern.sub, tuple):
                    proc(element_24.pattern.named_pattern.sub[1])
                proc(element_24.type_expr)
            elif isinstance(element_24, RustVariadicArg):
                for element_28 in element_24.attrs:
                    proc(element_28)
                proc(element_24.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_29, separator_19) in node.params[1]:
                proc(element_29)
        if isinstance(node.where_clause, tuple):
            for (element_30, separator_20) in node.where_clause[1]:
                proc(element_30)
        return
    if isinstance(node, RustImplElement):
        for element_31 in node.fn_impl_element.attrs:
            proc(element_31)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_32 in node.attrs:
            proc(element_32)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_33 in node.impl_elements:
            proc(element_33.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_34 in node.attrs:
            proc(element_34)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_35, separator_21) in node.params:
            proc(element_35)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_36, separator_22) in node.segments:
            proc(element_36)
        return
    if isinstance(node, RustPathExpr):
        for element_37 in node.attrs:
            proc(element_37)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_38 in node.attrs:
            proc(element_38)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_39, separator_23) in node.inputs:
            proc(element_39)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_40 in node.items:
            if isinstance(element_40, RustEnumItem):
                proc(element_40)
            elif isinstance(element_40, RustStructItem):
                proc(element_40)
            elif isinstance(element_40, RustUseItem):
                proc(element_40)
            elif isinstance(element_40, RustImplItem):
                for element_41 in element_40.attrs:
                    proc(element_41)
                proc(element_40.generics)
                if isinstance(element_40.trait, tuple):
                    proc(element_40.trait[1])
                proc(element_40.type_expr)
                for element_42 in element_40.impl_elements:
                    proc(element_42)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_43, separator_24) in node.inits:
            proc(element_43)
        return
    if isinstance(node, RustStructItem):
        for element_44 in node.attrs:
            proc(element_44)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_45, separator_25) in node.fields:
            proc(element_45)
        return
    if isinstance(node, RustStructVariant):
        for (element_46, separator_26) in node.fields:
            proc(element_46)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_47, separator_27) in node.elements:
            proc(element_47)
        return
    if isinstance(node, RustTupleVariant):
        for (element_48, separator_28) in node.types:
            proc(element_48)
        return
    if isinstance(node, RustTurbofish):
        for (element_49, separator_29) in node.args:
            proc(element_49)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_50, separator_30) in node.bounds:
            proc(element_50)
        return
    if isinstance(node, RustTypedArg):
        for element_51 in node.attrs:
            proc(element_51)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_52 in node.attrs:
            proc(element_52)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_53 in node.attrs:
            proc(element_53)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_type_expr(node: RustTypeExpr, proc: Callable[[RustTypeExpr], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if is_rust_type_expr(element_0):
                proc(element_0)
            elif is_rust_expr(element_0):
                if isinstance(element_0, RustPathExpr):
                    for element_1 in element_0.attrs:
                        if isinstance(element_1.meta, RustMetaPath):
                            for (element_2, separator_1) in element_1.meta.path.segments:
                                if is_rust_path_arguments(element_2.args):
                                    if isinstance(element_2.args, RustTurbofish):
                                        for (element_3, separator_2) in element_2.args.args:
                                            proc(element_3)
                                    elif isinstance(element_2.args, RustAngleBracketedGenericArguments):
                                        for (element_4, separator_3) in element_2.args.args:
                                            proc(element_4)
                                    elif isinstance(element_2.args, RustParenthesizedGenericArguments):
                                        for (element_5, separator_4) in element_2.args.params:
                                            proc(element_5)
                                        proc(element_2.args.result)
                        elif isinstance(element_1.meta, RustMetaParenthesized):
                            proc(element_1.meta.path)
                        elif isinstance(element_1.meta, RustMetaBracketed):
                            proc(element_1.meta.path)
                        elif isinstance(element_1.meta, RustMetaBraced):
                            proc(element_1.meta.path)
                        elif isinstance(element_1.meta, RustMetaNameValue):
                            proc(element_1.meta.path)
                            proc(element_1.meta.expr)
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        proc(element_0.qself.path)
                    proc(element_0.path)
                elif isinstance(element_0, RustCallExpr):
                    proc(element_0.operator)
                    for (element_6, separator_5) in element_0.args:
                        proc(element_6)
                elif isinstance(element_0, RustStructExpr):
                    proc(element_0.path)
                    for (element_7, separator_6) in element_0.inits:
                        proc(element_7.value)
                elif isinstance(element_0, RustBlockExpr):
                    if isinstance(element_0.item, RustEnumItem):
                        for element_8 in element_0.item.attrs:
                            proc(element_8)
                        if isinstance(element_0.item.visibility, RustPublic):
                            if isinstance(element_0.item.visibility.restrict, tuple):
                                proc(element_0.item.visibility.restrict[2])
                        for (element_9, separator_7) in element_0.item.variants:
                            if isinstance(element_9, RustStructVariant):
                                for (element_10, separator_8) in element_9.fields:
                                    proc(element_10.type_expr)
                            elif isinstance(element_9, RustTupleVariant):
                                for (element_11, separator_9) in element_9.types:
                                    proc(element_11)
                            elif isinstance(element_9, RustEmptyVariant):
                                if isinstance(element_9.init, RustInit):
                                    proc(element_9.init)
                    elif isinstance(element_0.item, RustStructItem):
                        for element_12 in element_0.item.attrs:
                            proc(element_12)
                        if isinstance(element_0.item.visibility, RustPublic):
                            proc(element_0.item.visibility)
                        for (element_13, separator_10) in element_0.item.fields:
                            proc(element_13)
                    elif isinstance(element_0.item, RustUseItem):
                        for element_14 in element_0.item.attrs:
                            proc(element_14)
                        if isinstance(element_0.item.visibility, RustPublic):
                            proc(element_0.item.visibility)
                    elif isinstance(element_0.item, RustExprItem):
                        proc(element_0.item.expr)
                    proc(element_0.last)
                elif isinstance(element_0, RustRetExpr):
                    proc(element_0.expr)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_15, separator_11) in element_0.bounds:
                    if isinstance(element_15, RustTraitBound):
                        if isinstance(element_15.bound_lifetimes, RustBoundLifetimes):
                            for (element_16, separator_12) in element_15.bound_lifetimes.lifetimes:
                                if isinstance(element_16, RustLifetime):
                                    proc(element_16)
                                elif isinstance(element_16, RustTypeParam):
                                    proc(element_16.type_param_bound)
                                    if isinstance(element_16.default, RustTypeInit):
                                        proc(element_16.default.type_expr)
                                elif isinstance(element_16, RustConstParam):
                                    proc(element_16.type_expr)
                                    if isinstance(element_16.default, RustInit):
                                        proc(element_16.default)
                        proc(element_15.path)
                    elif isinstance(element_15, RustLifetime):
                        proc(element_15)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_17, separator_13) in node.lifetimes:
            proc(element_17)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_18, separator_14) in node.args:
            proc(element_18)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_19, separator_15) in node.bounds:
            proc(element_19)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_20 in node.attrs:
            proc(element_20)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_21, separator_16) in node.variants:
            proc(element_21)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_22 in node.attrs:
            proc(element_22)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_23, separator_17) in node.signature.generics.params[1]:
                proc(element_23)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_24, separator_18) in node.signature.generics.where_clause[1]:
                if isinstance(element_24, RustTypePredicate):
                    proc(element_24.bound_lifetimes)
                    proc(element_24.type_expr)
                    for (element_25, separator_19) in element_24.bounds:
                        proc(element_25)
        for (element_26, separator_20) in node.signature.inputs:
            if isinstance(element_26, RustSelfArg):
                for element_27 in element_26.attrs:
                    proc(element_27)
                proc(element_26.type_expr)
            elif isinstance(element_26, RustTypedArg):
                for element_28 in element_26.attrs:
                    proc(element_28)
                for element_29 in element_26.pattern.named_pattern.attrs:
                    proc(element_29)
                if isinstance(element_26.pattern.named_pattern.sub, tuple):
                    proc(element_26.pattern.named_pattern.sub[1])
                proc(element_26.type_expr)
            elif isinstance(element_26, RustVariadicArg):
                for element_30 in element_26.attrs:
                    proc(element_30)
                proc(element_26.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_31, separator_21) in node.params[1]:
                proc(element_31)
        if isinstance(node.where_clause, tuple):
            for (element_32, separator_22) in node.where_clause[1]:
                proc(element_32)
        return
    if isinstance(node, RustImplElement):
        for element_33 in node.fn_impl_element.attrs:
            proc(element_33)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_34 in node.attrs:
            proc(element_34)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_35 in node.impl_elements:
            proc(element_35.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_36 in node.attrs:
            proc(element_36)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_37, separator_23) in node.params:
            proc(element_37)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_38, separator_24) in node.segments:
            proc(element_38)
        return
    if isinstance(node, RustPathExpr):
        for element_39 in node.attrs:
            proc(element_39)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_40 in node.attrs:
            proc(element_40)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_41, separator_25) in node.inputs:
            proc(element_41)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_42 in node.items:
            if isinstance(element_42, RustEnumItem):
                proc(element_42)
            elif isinstance(element_42, RustStructItem):
                proc(element_42)
            elif isinstance(element_42, RustUseItem):
                proc(element_42)
            elif isinstance(element_42, RustImplItem):
                for element_43 in element_42.attrs:
                    proc(element_43)
                proc(element_42.generics)
                if isinstance(element_42.trait, tuple):
                    proc(element_42.trait[1])
                proc(element_42.type_expr)
                for element_44 in element_42.impl_elements:
                    proc(element_44)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_45, separator_26) in node.inits:
            proc(element_45)
        return
    if isinstance(node, RustStructItem):
        for element_46 in node.attrs:
            proc(element_46)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_47, separator_27) in node.fields:
            proc(element_47)
        return
    if isinstance(node, RustStructVariant):
        for (element_48, separator_28) in node.fields:
            proc(element_48)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_49, separator_29) in node.elements:
            proc(element_49)
        return
    if isinstance(node, RustTupleVariant):
        for (element_50, separator_30) in node.types:
            proc(element_50)
        return
    if isinstance(node, RustTurbofish):
        for (element_51, separator_31) in node.args:
            proc(element_51)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_52, separator_32) in node.bounds:
            proc(element_52)
        return
    if isinstance(node, RustTypedArg):
        for element_53 in node.attrs:
            proc(element_53)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_54 in node.attrs:
            proc(element_54)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_55 in node.attrs:
            proc(element_55)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_type_param_bound(node: RustTypeParamBound, proc: Callable[[RustTypeParamBound], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if isinstance(element_0, RustLifetime):
                proc(element_0)
            elif is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    for (element_2, separator_2) in element_1.args.args:
                                        proc(element_2)
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    for (element_3, separator_3) in element_1.args.args:
                                        proc(element_3)
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    for (element_4, separator_4) in element_1.args.params:
                                        proc(element_4)
                                    proc(element_1.args.result)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    if isinstance(element_0.expr, RustPathExpr):
                        for element_5 in element_0.expr.attrs:
                            if isinstance(element_5.meta, RustMetaPath):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaParenthesized):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBracketed):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBraced):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaNameValue):
                                proc(element_5.meta.path)
                                proc(element_5.meta.expr)
                        if isinstance(element_0.expr.qself, RustQself):
                            proc(element_0.expr.qself)
                        proc(element_0.expr.path)
                    elif isinstance(element_0.expr, RustCallExpr):
                        proc(element_0.expr.operator)
                        for (element_6, separator_5) in element_0.expr.args:
                            proc(element_6)
                    elif isinstance(element_0.expr, RustStructExpr):
                        proc(element_0.expr.path)
                        for (element_7, separator_6) in element_0.expr.inits:
                            proc(element_7.value)
                    elif isinstance(element_0.expr, RustBlockExpr):
                        if isinstance(element_0.expr.item, RustEnumItem):
                            for element_8 in element_0.expr.item.attrs:
                                proc(element_8)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                if isinstance(element_0.expr.item.visibility.restrict, tuple):
                                    proc(element_0.expr.item.visibility.restrict[2])
                            for (element_9, separator_7) in element_0.expr.item.variants:
                                if isinstance(element_9, RustStructVariant):
                                    for (element_10, separator_8) in element_9.fields:
                                        proc(element_10.type_expr)
                                elif isinstance(element_9, RustTupleVariant):
                                    for (element_11, separator_9) in element_9.types:
                                        proc(element_11)
                                elif isinstance(element_9, RustEmptyVariant):
                                    if isinstance(element_9.init, RustInit):
                                        proc(element_9.init)
                        elif isinstance(element_0.expr.item, RustStructItem):
                            for element_12 in element_0.expr.item.attrs:
                                proc(element_12)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                            for (element_13, separator_10) in element_0.expr.item.fields:
                                proc(element_13)
                        elif isinstance(element_0.expr.item, RustUseItem):
                            for element_14 in element_0.expr.item.attrs:
                                proc(element_14)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                        elif isinstance(element_0.expr.item, RustExprItem):
                            proc(element_0.expr.item.expr)
                        proc(element_0.expr.last)
                    elif isinstance(element_0.expr, RustRetExpr):
                        proc(element_0.expr.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_15, separator_11) in element_0.elements:
                        proc(element_15)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_16, separator_12) in element_0.bounds:
                    proc(element_16)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_17, separator_13) in node.lifetimes:
            if isinstance(element_17, RustLifetime):
                proc(element_17)
            elif isinstance(element_17, RustTypeParam):
                proc(element_17.type_param_bound)
                if isinstance(element_17.default, RustTypeInit):
                    proc(element_17.default.type_expr)
            elif isinstance(element_17, RustConstParam):
                proc(element_17.type_expr)
                if isinstance(element_17.default, RustInit):
                    proc(element_17.default)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_18, separator_14) in node.args:
            proc(element_18)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_19, separator_15) in node.bounds:
            proc(element_19)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_20 in node.attrs:
            proc(element_20)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_21, separator_16) in node.variants:
            proc(element_21)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_22 in node.attrs:
            proc(element_22)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_23, separator_17) in node.signature.generics.params[1]:
                proc(element_23)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_24, separator_18) in node.signature.generics.where_clause[1]:
                if isinstance(element_24, RustTypePredicate):
                    for (element_25, separator_19) in element_24.bound_lifetimes.lifetimes:
                        proc(element_25)
                    proc(element_24.type_expr)
                    for (element_26, separator_20) in element_24.bounds:
                        proc(element_26)
        for (element_27, separator_21) in node.signature.inputs:
            if isinstance(element_27, RustSelfArg):
                for element_28 in element_27.attrs:
                    proc(element_28)
                proc(element_27.type_expr)
            elif isinstance(element_27, RustTypedArg):
                for element_29 in element_27.attrs:
                    proc(element_29)
                for element_30 in element_27.pattern.named_pattern.attrs:
                    proc(element_30)
                if isinstance(element_27.pattern.named_pattern.sub, tuple):
                    proc(element_27.pattern.named_pattern.sub[1])
                proc(element_27.type_expr)
            elif isinstance(element_27, RustVariadicArg):
                for element_31 in element_27.attrs:
                    proc(element_31)
                proc(element_27.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_32, separator_22) in node.params[1]:
                proc(element_32)
        if isinstance(node.where_clause, tuple):
            for (element_33, separator_23) in node.where_clause[1]:
                proc(element_33)
        return
    if isinstance(node, RustImplElement):
        for element_34 in node.fn_impl_element.attrs:
            proc(element_34)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_35 in node.attrs:
            proc(element_35)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_36 in node.impl_elements:
            proc(element_36.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_37 in node.attrs:
            proc(element_37)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_38, separator_24) in node.params:
            proc(element_38)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_39, separator_25) in node.segments:
            proc(element_39)
        return
    if isinstance(node, RustPathExpr):
        for element_40 in node.attrs:
            proc(element_40)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_41 in node.attrs:
            proc(element_41)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_42, separator_26) in node.inputs:
            proc(element_42)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_43 in node.items:
            if isinstance(element_43, RustEnumItem):
                proc(element_43)
            elif isinstance(element_43, RustStructItem):
                proc(element_43)
            elif isinstance(element_43, RustUseItem):
                proc(element_43)
            elif isinstance(element_43, RustImplItem):
                for element_44 in element_43.attrs:
                    proc(element_44)
                proc(element_43.generics)
                if isinstance(element_43.trait, tuple):
                    proc(element_43.trait[1])
                proc(element_43.type_expr)
                for element_45 in element_43.impl_elements:
                    proc(element_45)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_46, separator_27) in node.inits:
            proc(element_46)
        return
    if isinstance(node, RustStructItem):
        for element_47 in node.attrs:
            proc(element_47)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_48, separator_28) in node.fields:
            proc(element_48)
        return
    if isinstance(node, RustStructVariant):
        for (element_49, separator_29) in node.fields:
            proc(element_49)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_50, separator_30) in node.elements:
            proc(element_50)
        return
    if isinstance(node, RustTupleVariant):
        for (element_51, separator_31) in node.types:
            proc(element_51)
        return
    if isinstance(node, RustTurbofish):
        for (element_52, separator_32) in node.args:
            proc(element_52)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_53, separator_33) in node.bounds:
            proc(element_53)
        return
    if isinstance(node, RustTypedArg):
        for element_54 in node.attrs:
            proc(element_54)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_55 in node.attrs:
            proc(element_55)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_56 in node.attrs:
            proc(element_56)
        proc(node.pattern)
        return


@no_type_check
def for_each_child_rust_use_tree(node: RustUseTree, proc: Callable[[RustUseTree], None]) -> None:
    if isinstance(node, RustUseGroup):
        for (element_0, separator_0) in node.items:
            proc(element_0)
        return
    if isinstance(node, RustUsePath):
        proc(node.tree)
        return


@no_type_check
def for_each_child_rust_variant(node: RustVariant, proc: Callable[[RustVariant], None]) -> None:
    if isinstance(node, RustAngleBracketedGenericArguments):
        for (element_0, separator_0) in node.args:
            if is_rust_type_expr(element_0):
                if isinstance(element_0, RustPathTypeExpr):
                    if isinstance(element_0.qself, RustQself):
                        proc(element_0.qself.type_expr)
                        for (element_1, separator_1) in element_0.qself.path.segments:
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    for (element_2, separator_2) in element_1.args.args:
                                        proc(element_2)
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    for (element_3, separator_3) in element_1.args.args:
                                        proc(element_3)
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    for (element_4, separator_4) in element_1.args.params:
                                        proc(element_4)
                                    proc(element_1.args.result)
                    proc(element_0.path)
                elif isinstance(element_0, RustArrayTypeExpr):
                    proc(element_0.type_expr)
                    if isinstance(element_0.expr, RustPathExpr):
                        for element_5 in element_0.expr.attrs:
                            if isinstance(element_5.meta, RustMetaPath):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaParenthesized):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBracketed):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaBraced):
                                proc(element_5.meta.path)
                            elif isinstance(element_5.meta, RustMetaNameValue):
                                proc(element_5.meta.path)
                                proc(element_5.meta.expr)
                        if isinstance(element_0.expr.qself, RustQself):
                            proc(element_0.expr.qself)
                        proc(element_0.expr.path)
                    elif isinstance(element_0.expr, RustCallExpr):
                        proc(element_0.expr.operator)
                        for (element_6, separator_5) in element_0.expr.args:
                            proc(element_6)
                    elif isinstance(element_0.expr, RustStructExpr):
                        proc(element_0.expr.path)
                        for (element_7, separator_6) in element_0.expr.inits:
                            proc(element_7.value)
                    elif isinstance(element_0.expr, RustBlockExpr):
                        if isinstance(element_0.expr.item, RustEnumItem):
                            for element_8 in element_0.expr.item.attrs:
                                proc(element_8)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                if isinstance(element_0.expr.item.visibility.restrict, tuple):
                                    proc(element_0.expr.item.visibility.restrict[2])
                            for (element_9, separator_7) in element_0.expr.item.variants:
                                proc(element_9)
                        elif isinstance(element_0.expr.item, RustStructItem):
                            for element_10 in element_0.expr.item.attrs:
                                proc(element_10)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                            for (element_11, separator_8) in element_0.expr.item.fields:
                                proc(element_11.type_expr)
                        elif isinstance(element_0.expr.item, RustUseItem):
                            for element_12 in element_0.expr.item.attrs:
                                proc(element_12)
                            if isinstance(element_0.expr.item.visibility, RustPublic):
                                proc(element_0.expr.item.visibility)
                        elif isinstance(element_0.expr.item, RustExprItem):
                            proc(element_0.expr.item.expr)
                        proc(element_0.expr.last)
                    elif isinstance(element_0.expr, RustRetExpr):
                        proc(element_0.expr.expr)
                elif isinstance(element_0, RustTupleTypeExpr):
                    for (element_13, separator_9) in element_0.elements:
                        proc(element_13)
            elif is_rust_expr(element_0):
                proc(element_0)
            elif isinstance(element_0, RustAssocType):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.type_expr)
            elif isinstance(element_0, RustAssocConst):
                if isinstance(element_0.generics, RustAngleBracketedGenericArguments):
                    proc(element_0.generics)
                proc(element_0.expr)
            elif isinstance(element_0, RustConstraint):
                proc(element_0.generics)
                for (element_14, separator_10) in element_0.bounds:
                    if isinstance(element_14, RustTraitBound):
                        if isinstance(element_14.bound_lifetimes, RustBoundLifetimes):
                            for (element_15, separator_11) in element_14.bound_lifetimes.lifetimes:
                                if isinstance(element_15, RustLifetime):
                                    proc(element_15)
                                elif isinstance(element_15, RustTypeParam):
                                    proc(element_15.type_param_bound)
                                    if isinstance(element_15.default, RustTypeInit):
                                        proc(element_15.default.type_expr)
                                elif isinstance(element_15, RustConstParam):
                                    proc(element_15.type_expr)
                                    if isinstance(element_15.default, RustInit):
                                        proc(element_15.default)
                        proc(element_14.path)
                    elif isinstance(element_14, RustLifetime):
                        proc(element_14)
        return
    if isinstance(node, RustArrayTypeExpr):
        proc(node.type_expr)
        proc(node.expr)
        return
    if isinstance(node, RustAssocConst):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.expr)
        return
    if isinstance(node, RustAssocType):
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            proc(node.generics)
        proc(node.type_expr)
        return
    if isinstance(node, RustAttr):
        proc(node.meta)
        return
    if isinstance(node, RustBlockExpr):
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustBoundLifetimes):
        for (element_16, separator_12) in node.lifetimes:
            proc(element_16)
        return
    if isinstance(node, RustCallExpr):
        proc(node.operator)
        for (element_17, separator_13) in node.args:
            proc(element_17)
        return
    if isinstance(node, RustConstParam):
        proc(node.type_expr)
        if isinstance(node.default, RustInit):
            proc(node.default)
        return
    if isinstance(node, RustConstraint):
        proc(node.generics)
        for (element_18, separator_14) in node.bounds:
            proc(element_18)
        return
    if isinstance(node, RustEmptyVariant):
        if isinstance(node.init, RustInit):
            proc(node.init)
        return
    if isinstance(node, RustEnumItem):
        for element_19 in node.attrs:
            proc(element_19)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_20, separator_15) in node.variants:
            proc(element_20)
        return
    if isinstance(node, RustExprItem):
        proc(node.expr)
        return
    if isinstance(node, RustField):
        proc(node.type_expr)
        return
    if isinstance(node, RustFnImplElement):
        for element_21 in node.attrs:
            proc(element_21)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        if isinstance(node.signature.generics.params, tuple):
            for (element_22, separator_16) in node.signature.generics.params[1]:
                proc(element_22)
        if isinstance(node.signature.generics.where_clause, tuple):
            for (element_23, separator_17) in node.signature.generics.where_clause[1]:
                if isinstance(element_23, RustTypePredicate):
                    proc(element_23.bound_lifetimes)
                    proc(element_23.type_expr)
                    for (element_24, separator_18) in element_23.bounds:
                        proc(element_24)
        for (element_25, separator_19) in node.signature.inputs:
            if isinstance(element_25, RustSelfArg):
                for element_26 in element_25.attrs:
                    proc(element_26)
                proc(element_25.type_expr)
            elif isinstance(element_25, RustTypedArg):
                for element_27 in element_25.attrs:
                    proc(element_27)
                for element_28 in element_25.pattern.named_pattern.attrs:
                    proc(element_28)
                if isinstance(element_25.pattern.named_pattern.sub, tuple):
                    proc(element_25.pattern.named_pattern.sub[1])
                proc(element_25.type_expr)
            elif isinstance(element_25, RustVariadicArg):
                for element_29 in element_25.attrs:
                    proc(element_29)
                proc(element_25.pattern)
        if isinstance(node.signature.output, tuple):
            proc(node.signature.output[1])
        proc(node.item)
        proc(node.last)
        return
    if isinstance(node, RustGenerics):
        if isinstance(node.params, tuple):
            for (element_30, separator_20) in node.params[1]:
                proc(element_30)
        if isinstance(node.where_clause, tuple):
            for (element_31, separator_21) in node.where_clause[1]:
                proc(element_31)
        return
    if isinstance(node, RustImplElement):
        for element_32 in node.fn_impl_element.attrs:
            proc(element_32)
        if isinstance(node.fn_impl_element.visibility, RustPublic):
            proc(node.fn_impl_element.visibility)
        proc(node.fn_impl_element.signature)
        proc(node.fn_impl_element.item)
        proc(node.fn_impl_element.last)
        return
    if isinstance(node, RustImplItem):
        for element_33 in node.attrs:
            proc(element_33)
        proc(node.generics)
        if isinstance(node.trait, tuple):
            proc(node.trait[1])
        proc(node.type_expr)
        for element_34 in node.impl_elements:
            proc(element_34.fn_impl_element)
        return
    if isinstance(node, RustInit):
        proc(node.value)
        return
    if isinstance(node, RustMetaBraced):
        proc(node.path)
        return
    if isinstance(node, RustMetaBracketed):
        proc(node.path)
        return
    if isinstance(node, RustMetaNameValue):
        proc(node.path)
        proc(node.expr)
        return
    if isinstance(node, RustMetaParenthesized):
        proc(node.path)
        return
    if isinstance(node, RustMetaPath):
        proc(node.path)
        return
    if isinstance(node, RustNamedPattern):
        for element_35 in node.attrs:
            proc(element_35)
        if isinstance(node.sub, tuple):
            proc(node.sub[1])
        return
    if isinstance(node, RustParenthesizedGenericArguments):
        for (element_36, separator_22) in node.params:
            proc(element_36)
        proc(node.result)
        return
    if isinstance(node, RustPath):
        for (element_37, separator_23) in node.segments:
            proc(element_37)
        return
    if isinstance(node, RustPathExpr):
        for element_38 in node.attrs:
            proc(element_38)
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPathSegment):
        if is_rust_path_arguments(node.args):
            proc(node.args)
        return
    if isinstance(node, RustPathTypeExpr):
        if isinstance(node.qself, RustQself):
            proc(node.qself)
        proc(node.path)
        return
    if isinstance(node, RustPattern):
        proc(node.named_pattern)
        return
    if isinstance(node, RustPublic):
        if isinstance(node.restrict, tuple):
            proc(node.restrict[2])
        return
    if isinstance(node, RustQself):
        proc(node.type_expr)
        proc(node.path)
        return
    if isinstance(node, RustRetExpr):
        proc(node.expr)
        return
    if isinstance(node, RustSelfArg):
        for element_39 in node.attrs:
            proc(element_39)
        proc(node.type_expr)
        return
    if isinstance(node, RustSignature):
        proc(node.generics)
        for (element_40, separator_24) in node.inputs:
            proc(element_40)
        if isinstance(node.output, tuple):
            proc(node.output[1])
        return
    if isinstance(node, RustSourceFile):
        for element_41 in node.items:
            if isinstance(element_41, RustEnumItem):
                proc(element_41)
            elif isinstance(element_41, RustStructItem):
                proc(element_41)
            elif isinstance(element_41, RustUseItem):
                proc(element_41)
            elif isinstance(element_41, RustImplItem):
                for element_42 in element_41.attrs:
                    proc(element_42)
                proc(element_41.generics)
                if isinstance(element_41.trait, tuple):
                    proc(element_41.trait[1])
                proc(element_41.type_expr)
                for element_43 in element_41.impl_elements:
                    proc(element_43)
        return
    if isinstance(node, RustStructExpr):
        proc(node.path)
        for (element_44, separator_25) in node.inits:
            proc(element_44)
        return
    if isinstance(node, RustStructItem):
        for element_45 in node.attrs:
            proc(element_45)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        for (element_46, separator_26) in node.fields:
            proc(element_46)
        return
    if isinstance(node, RustStructVariant):
        for (element_47, separator_27) in node.fields:
            proc(element_47)
        return
    if isinstance(node, RustTraitBound):
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            proc(node.bound_lifetimes)
        proc(node.path)
        return
    if isinstance(node, RustTupleTypeExpr):
        for (element_48, separator_28) in node.elements:
            proc(element_48)
        return
    if isinstance(node, RustTupleVariant):
        for (element_49, separator_29) in node.types:
            proc(element_49)
        return
    if isinstance(node, RustTurbofish):
        for (element_50, separator_30) in node.args:
            proc(element_50)
        return
    if isinstance(node, RustTypeInit):
        proc(node.type_expr)
        return
    if isinstance(node, RustTypeParam):
        proc(node.type_param_bound)
        if isinstance(node.default, RustTypeInit):
            proc(node.default)
        return
    if isinstance(node, RustTypePredicate):
        proc(node.bound_lifetimes)
        proc(node.type_expr)
        for (element_51, separator_31) in node.bounds:
            proc(element_51)
        return
    if isinstance(node, RustTypedArg):
        for element_52 in node.attrs:
            proc(element_52)
        proc(node.pattern)
        proc(node.type_expr)
        return
    if isinstance(node, RustUseItem):
        for element_53 in node.attrs:
            proc(element_53)
        if isinstance(node.visibility, RustPublic):
            proc(node.visibility)
        return
    if isinstance(node, RustVariadicArg):
        for element_54 in node.attrs:
            proc(element_54)
        proc(node.pattern)
        return


@no_type_check
def rewrite_each_rust_expr(node: RustExpr, proc: Callable[[RustExpr], RustExpr]) -> RustExpr:
    if isinstance(node, RustBlockExpr):
        changed_1 = False
        if isinstance(node.item, RustEnumItem):
            changed_2 = False
            new_attrs = []
            for element in node.item.attrs:
                changed_3 = False
                if isinstance(element.meta, RustMetaPath):
                    changed_4 = False
                    changed_5 = False
                    new_segments = Punctuated()
                    for (element_1, separator) in element.meta.path.segments.delimited:
                        changed_6 = False
                        if is_rust_path_arguments(element_1.args):
                            if isinstance(element_1.args, RustTurbofish):
                                changed_7 = False
                                new_args_1 = Punctuated()
                                for (element_2, separator_1) in element_1.args.args.delimited:
                                    if isinstance(element_2, RustLifetime):
                                        new_element_2 = element_2
                                    elif is_rust_type_expr(element_2):
                                        if isinstance(element_2, RustPathTypeExpr):
                                            changed_9 = False
                                            if isinstance(element_2.qself, RustQself):
                                                changed_10 = False
                                                new_type_expr = proc(element_2.qself.type_expr)
                                                assert(is_rust_type_expr(new_type_expr))
                                                if new_type_expr is not element_2.qself.type_expr:
                                                    changed_10 = True
                                                new_path_1 = proc(element_2.qself.path)
                                                assert(isinstance(new_path_1, RustPath))
                                                if new_path_1 is not element_2.qself.path:
                                                    changed_10 = True
                                                if changed_10:
                                                    new_qself = RustQself(less_than=element_2.qself.less_than, type_expr=new_type_expr, as_keyword=element_2.qself.as_keyword, path=new_path_1, greater_than=element_2.qself.greater_than)
                                                    changed_9 = True
                                                else:
                                                    new_qself = element_2.qself
                                            elif element_2.qself is None:
                                                new_qself = element_2.qself
                                            else:
                                                assert_never(element_2.qself)
                                            new_path_2 = proc(element_2.path)
                                            assert(isinstance(new_path_2, RustPath))
                                            if new_path_2 is not element_2.path:
                                                changed_9 = True
                                            if changed_9:
                                                new_element_2 = RustPathTypeExpr(qself=new_qself, path=new_path_2)
                                                changed_7 = True
                                            else:
                                                new_element_2 = element_2
                                        elif isinstance(element_2, RustArrayTypeExpr):
                                            changed_11 = False
                                            new_type_expr_1 = proc(element_2.type_expr)
                                            assert(is_rust_type_expr(new_type_expr_1))
                                            if new_type_expr_1 is not element_2.type_expr:
                                                changed_11 = True
                                            new_expr = proc(element_2.expr)
                                            assert(is_rust_expr(new_expr))
                                            if new_expr is not element_2.expr:
                                                changed_11 = True
                                            if changed_11:
                                                new_element_2 = RustArrayTypeExpr(open_bracket=element_2.open_bracket, type_expr=new_type_expr_1, semicolon=element_2.semicolon, expr=new_expr, close_bracket=element_2.close_bracket)
                                                changed_7 = True
                                            else:
                                                new_element_2 = element_2
                                        elif isinstance(element_2, RustNeverTypeExpr):
                                            new_element_2 = element_2
                                        elif isinstance(element_2, RustTupleTypeExpr):
                                            changed_13 = False
                                            new_elements_1 = Punctuated()
                                            for (element_3, separator_2) in element_2.elements.delimited:
                                                new_element_3 = proc(element_3)
                                                assert(is_rust_type_expr(new_element_3))
                                                if new_element_3 is not element_3:
                                                    changed_13 = True
                                                new_separator_2 = separator_2
                                                new_elements_1.append(new_element_3, new_separator_2)
                                            new_last_2 = proc(element_2.elements.last)
                                            assert(is_rust_type_expr(new_last_2))
                                            if new_last_2 is not element_2.elements.last:
                                                changed_13 = True
                                            new_elements_1.append_final(new_last_2)
                                            if changed_13:
                                                new_element_2 = RustTupleTypeExpr(open_paren=element_2.open_paren, elements=new_elements_1, close_paren=element_2.close_paren)
                                                changed_7 = True
                                            else:
                                                new_element_2 = element_2
                                        else:
                                            assert_never(element_2)
                                    elif is_rust_expr(element_2):
                                        new_element_2 = proc(element_2)
                                        assert(is_rust_expr(new_element_2))
                                        if new_element_2 is not element_2:
                                            changed_7 = True
                                    elif isinstance(element_2, RustAssocType):
                                        changed_14 = False
                                        if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                            changed_15 = False
                                            new_args_2 = Punctuated()
                                            for (element_4, separator_3) in element_2.generics.args.delimited:
                                                new_element_4 = proc(element_4)
                                                assert(is_rust_generic_argument(new_element_4))
                                                if new_element_4 is not element_4:
                                                    changed_15 = True
                                                new_separator_3 = proc(separator_3)
                                                assert(isinstance(new_separator_3, RustComma))
                                                if new_separator_3 is not separator_3:
                                                    changed_15 = True
                                                new_args_2.append(new_element_4, new_separator_3)
                                            new_last_3 = proc(element_2.generics.args.last)
                                            assert(is_rust_generic_argument(new_last_3))
                                            if new_last_3 is not element_2.generics.args.last:
                                                changed_15 = True
                                            new_args_2.append_final(new_last_3)
                                            if changed_15:
                                                new_generics = RustAngleBracketedGenericArguments(less_than=element_2.generics.less_than, args=new_args_2, greater_than=element_2.generics.greater_than)
                                                changed_14 = True
                                            else:
                                                new_generics = element_2.generics
                                        elif element_2.generics is None:
                                            new_generics = element_2.generics
                                        else:
                                            assert_never(element_2.generics)
                                        new_type_expr_2 = proc(element_2.type_expr)
                                        assert(is_rust_type_expr(new_type_expr_2))
                                        if new_type_expr_2 is not element_2.type_expr:
                                            changed_14 = True
                                        if changed_14:
                                            new_element_2 = RustAssocType(name=element_2.name, generics=new_generics, equals=element_2.equals, type_expr=new_type_expr_2)
                                            changed_7 = True
                                        else:
                                            new_element_2 = element_2
                                    elif isinstance(element_2, RustAssocConst):
                                        changed_16 = False
                                        if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                            new_generics_1 = proc(element_2.generics)
                                            assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                            if new_generics_1 is not element_2.generics:
                                                changed_16 = True
                                        elif element_2.generics is None:
                                            new_generics_1 = element_2.generics
                                        else:
                                            assert_never(element_2.generics)
                                        new_expr_1 = proc(element_2.expr)
                                        assert(is_rust_expr(new_expr_1))
                                        if new_expr_1 is not element_2.expr:
                                            changed_16 = True
                                        if changed_16:
                                            new_element_2 = RustAssocConst(name=element_2.name, generics=new_generics_1, equals=element_2.equals, expr=new_expr_1)
                                            changed_7 = True
                                        else:
                                            new_element_2 = element_2
                                    elif isinstance(element_2, RustConstraint):
                                        changed_17 = False
                                        new_generics_2 = proc(element_2.generics)
                                        assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                                        if new_generics_2 is not element_2.generics:
                                            changed_17 = True
                                        new_bounds = Punctuated()
                                        for (element_5, separator_4) in element_2.bounds.delimited:
                                            if isinstance(element_5, RustTraitBound):
                                                changed_18 = False
                                                if isinstance(element_5.bound_lifetimes, RustBoundLifetimes):
                                                    changed_19 = False
                                                    new_lifetimes = Punctuated()
                                                    for (element_6, separator_5) in element_5.bound_lifetimes.lifetimes.delimited:
                                                        if isinstance(element_6, RustLifetime):
                                                            new_element_6 = proc(element_6)
                                                            assert(isinstance(new_element_6, RustLifetime))
                                                            if new_element_6 is not element_6:
                                                                changed_19 = True
                                                        elif isinstance(element_6, RustTypeParam):
                                                            changed_20 = False
                                                            new_type_param_bound = proc(element_6.type_param_bound)
                                                            assert(is_rust_type_param_bound(new_type_param_bound))
                                                            if new_type_param_bound is not element_6.type_param_bound:
                                                                changed_20 = True
                                                            if isinstance(element_6.default, RustTypeInit):
                                                                changed_21 = False
                                                                new_type_expr_3 = proc(element_6.default.type_expr)
                                                                assert(is_rust_type_expr(new_type_expr_3))
                                                                if new_type_expr_3 is not element_6.default.type_expr:
                                                                    changed_21 = True
                                                                if changed_21:
                                                                    new_default = RustTypeInit(equals=element_6.default.equals, type_expr=new_type_expr_3)
                                                                    changed_20 = True
                                                                else:
                                                                    new_default = element_6.default
                                                            elif element_6.default is None:
                                                                new_default = element_6.default
                                                            else:
                                                                assert_never(element_6.default)
                                                            if changed_20:
                                                                new_element_6 = RustTypeParam(name=element_6.name, colon=element_6.colon, type_param_bound=new_type_param_bound, percent=element_6.percent, plus=element_6.plus, default=new_default)
                                                                changed_19 = True
                                                            else:
                                                                new_element_6 = element_6
                                                        elif isinstance(element_6, RustConstParam):
                                                            changed_22 = False
                                                            new_type_expr_4 = proc(element_6.type_expr)
                                                            assert(is_rust_type_expr(new_type_expr_4))
                                                            if new_type_expr_4 is not element_6.type_expr:
                                                                changed_22 = True
                                                            if isinstance(element_6.default, RustInit):
                                                                changed_23 = False
                                                                new_value = proc(element_6.default.value)
                                                                assert(is_rust_expr(new_value))
                                                                if new_value is not element_6.default.value:
                                                                    changed_23 = True
                                                                if changed_23:
                                                                    new_default_1 = RustInit(name=element_6.default.name, equals=element_6.default.equals, value=new_value)
                                                                    changed_22 = True
                                                                else:
                                                                    new_default_1 = element_6.default
                                                            elif element_6.default is None:
                                                                new_default_1 = element_6.default
                                                            else:
                                                                assert_never(element_6.default)
                                                            if changed_22:
                                                                new_element_6 = RustConstParam(const_keyword=element_6.const_keyword, name=element_6.name, colon=element_6.colon, type_expr=new_type_expr_4, default=new_default_1)
                                                                changed_19 = True
                                                            else:
                                                                new_element_6 = element_6
                                                        else:
                                                            assert_never(element_6)
                                                        new_separator_5 = proc(separator_5)
                                                        assert(isinstance(new_separator_5, RustComma))
                                                        if new_separator_5 is not separator_5:
                                                            changed_19 = True
                                                        new_lifetimes.append(new_element_6, new_separator_5)
                                                    new_last_5 = proc(element_5.bound_lifetimes.lifetimes.last)
                                                    assert(is_rust_generic_param(new_last_5))
                                                    if new_last_5 is not element_5.bound_lifetimes.lifetimes.last:
                                                        changed_19 = True
                                                    new_lifetimes.append_final(new_last_5)
                                                    if changed_19:
                                                        new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_5.bound_lifetimes.for_keyword, less_than=element_5.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_5.bound_lifetimes.greater_than)
                                                        changed_18 = True
                                                    else:
                                                        new_bound_lifetimes = element_5.bound_lifetimes
                                                elif element_5.bound_lifetimes is None:
                                                    new_bound_lifetimes = element_5.bound_lifetimes
                                                else:
                                                    assert_never(element_5.bound_lifetimes)
                                                new_path_3 = proc(element_5.path)
                                                assert(isinstance(new_path_3, RustPath))
                                                if new_path_3 is not element_5.path:
                                                    changed_18 = True
                                                if changed_18:
                                                    new_element_5 = RustTraitBound(modifier=element_5.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_3)
                                                    changed_17 = True
                                                else:
                                                    new_element_5 = element_5
                                            elif isinstance(element_5, RustLifetime):
                                                new_element_5 = proc(element_5)
                                                assert(isinstance(new_element_5, RustLifetime))
                                                if new_element_5 is not element_5:
                                                    changed_17 = True
                                            else:
                                                assert_never(element_5)
                                            new_separator_4 = separator_4
                                            new_bounds.append(new_element_5, new_separator_4)
                                        new_last_4 = proc(element_2.bounds.last)
                                        assert(is_rust_type_param_bound(new_last_4))
                                        if new_last_4 is not element_2.bounds.last:
                                            changed_17 = True
                                        new_bounds.append_final(new_last_4)
                                        if changed_17:
                                            new_element_2 = RustConstraint(name=element_2.name, generics=new_generics_2, colon=element_2.colon, bounds=new_bounds)
                                            changed_7 = True
                                        else:
                                            new_element_2 = element_2
                                    else:
                                        assert_never(element_2)
                                    new_separator_1 = proc(separator_1)
                                    assert(isinstance(new_separator_1, RustComma))
                                    if new_separator_1 is not separator_1:
                                        changed_7 = True
                                    new_args_1.append(new_element_2, new_separator_1)
                                new_last_1 = proc(element_1.args.args.last)
                                assert(is_rust_generic_argument(new_last_1))
                                if new_last_1 is not element_1.args.args.last:
                                    changed_7 = True
                                new_args_1.append_final(new_last_1)
                                if changed_7:
                                    new_args = RustTurbofish(colon_colon=element_1.args.colon_colon, less_than=element_1.args.less_than, args=new_args_1, greater_than=element_1.args.greater_than)
                                    changed_6 = True
                                else:
                                    new_args = element_1.args
                            elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                new_args = proc(element_1.args)
                                assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                                if new_args is not element_1.args:
                                    changed_6 = True
                            elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                changed_24 = False
                                new_params = Punctuated()
                                for (element_7, separator_6) in element_1.args.params.delimited:
                                    new_element_7 = proc(element_7)
                                    assert(is_rust_type_expr(new_element_7))
                                    if new_element_7 is not element_7:
                                        changed_24 = True
                                    new_separator_6 = proc(separator_6)
                                    assert(isinstance(new_separator_6, RustComma))
                                    if new_separator_6 is not separator_6:
                                        changed_24 = True
                                    new_params.append(new_element_7, new_separator_6)
                                new_last_6 = proc(element_1.args.params.last)
                                assert(is_rust_type_expr(new_last_6))
                                if new_last_6 is not element_1.args.params.last:
                                    changed_24 = True
                                new_params.append_final(new_last_6)
                                new_result = proc(element_1.args.result)
                                assert(is_rust_type_expr(new_result))
                                if new_result is not element_1.args.result:
                                    changed_24 = True
                                if changed_24:
                                    new_args = RustParenthesizedGenericArguments(open_paren=element_1.args.open_paren, params=new_params, close_paren=element_1.args.close_paren, r_arrow=element_1.args.r_arrow, result=new_result)
                                    changed_6 = True
                                else:
                                    new_args = element_1.args
                            else:
                                assert_never(element_1.args)
                        elif element_1.args is None:
                            new_args = element_1.args
                        else:
                            assert_never(element_1.args)
                        if changed_6:
                            new_element_1 = RustPathSegment(name=element_1.name, args=new_args)
                            changed_5 = True
                        else:
                            new_element_1 = element_1
                        new_separator = separator
                        new_segments.append(new_element_1, new_separator)
                    new_last = proc(element.meta.path.segments.last)
                    assert(isinstance(new_last, RustPathSegment))
                    if new_last is not element.meta.path.segments.last:
                        changed_5 = True
                    new_segments.append_final(new_last)
                    if changed_5:
                        new_path = RustPath(leading_colon_colon=element.meta.path.leading_colon_colon, segments=new_segments)
                        changed_4 = True
                    else:
                        new_path = element.meta.path
                    if changed_4:
                        new_meta = RustMetaPath(path=new_path)
                        changed_3 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaParenthesized):
                    changed_25 = False
                    new_path_4 = proc(element.meta.path)
                    assert(isinstance(new_path_4, RustPath))
                    if new_path_4 is not element.meta.path:
                        changed_25 = True
                    if changed_25:
                        new_meta = RustMetaParenthesized(path=new_path_4, open_paren=element.meta.open_paren, tokens=element.meta.tokens, close_paren=element.meta.close_paren)
                        changed_3 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaBracketed):
                    changed_26 = False
                    new_path_5 = proc(element.meta.path)
                    assert(isinstance(new_path_5, RustPath))
                    if new_path_5 is not element.meta.path:
                        changed_26 = True
                    if changed_26:
                        new_meta = RustMetaBracketed(path=new_path_5, open_bracket=element.meta.open_bracket, tokens=element.meta.tokens, close_bracket=element.meta.close_bracket)
                        changed_3 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaBraced):
                    changed_27 = False
                    new_path_6 = proc(element.meta.path)
                    assert(isinstance(new_path_6, RustPath))
                    if new_path_6 is not element.meta.path:
                        changed_27 = True
                    if changed_27:
                        new_meta = RustMetaBraced(path=new_path_6, open_brace=element.meta.open_brace, tokens=element.meta.tokens, close_brace=element.meta.close_brace)
                        changed_3 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaNameValue):
                    changed_28 = False
                    new_path_7 = proc(element.meta.path)
                    assert(isinstance(new_path_7, RustPath))
                    if new_path_7 is not element.meta.path:
                        changed_28 = True
                    new_expr_2 = proc(element.meta.expr)
                    assert(is_rust_expr(new_expr_2))
                    if new_expr_2 is not element.meta.expr:
                        changed_28 = True
                    if changed_28:
                        new_meta = RustMetaNameValue(path=new_path_7, equals=element.meta.equals, expr=new_expr_2)
                        changed_3 = True
                    else:
                        new_meta = element.meta
                else:
                    assert_never(element.meta)
                if changed_3:
                    new_element = RustAttr(hashtag=element.hashtag, exclamation_mark=element.exclamation_mark, open_bracket=element.open_bracket, meta=new_meta, close_bracket=element.close_bracket)
                    changed_2 = True
                else:
                    new_element = element
                new_elements.append(new_element)
            if isinstance(node.item.visibility, RustPublic):
                changed_29 = False
                if isinstance(node.item.visibility.restrict, tuple):
                    new_elements_2 = []
                    element_0 = node.item.visibility.restrict[0]
                    new_element_0 = element_0
                    new_elements_2.append(new_element_0)
                    element_1 = node.item.visibility.restrict[1]
                    if isinstance(element_1, RustInKeyword):
                        new_element_1 = element_1
                    elif element_1 is None:
                        new_element_1 = element_1
                    else:
                        assert_never(element_1)
                    new_elements_2.append(new_element_1)
                    element_2 = node.item.visibility.restrict[2]
                    new_element_2 = proc(element_2)
                    assert(isinstance(new_element_2, RustPath))
                    if new_element_2 is not element_2:
                        changed_29 = True
                    new_elements_2.append(new_element_2)
                    element_3 = node.item.visibility.restrict[3]
                    new_element_3 = element_3
                    new_elements_2.append(new_element_3)
                    new_restrict = tuple(new_elements_2) if changed_29 else node.item.visibility.restrict
                elif node.item.visibility.restrict is None:
                    new_restrict = node.item.visibility.restrict
                else:
                    assert_never(node.item.visibility.restrict)
                if changed_29:
                    new_visibility = RustPublic(pub_keyword=node.item.visibility.pub_keyword, restrict=new_restrict)
                    changed_2 = True
                else:
                    new_visibility = node.item.visibility
            elif node.item.visibility is None:
                new_visibility = node.item.visibility
            else:
                assert_never(node.item.visibility)
            new_variants = Punctuated()
            for (element_8, separator_7) in node.item.variants.delimited:
                if isinstance(element_8, RustStructVariant):
                    changed_30 = False
                    new_fields = Punctuated()
                    for (element_9, separator_8) in element_8.fields.delimited:
                        changed_31 = False
                        new_type_expr_5 = proc(element_9.type_expr)
                        assert(is_rust_type_expr(new_type_expr_5))
                        if new_type_expr_5 is not element_9.type_expr:
                            changed_31 = True
                        if changed_31:
                            new_element_9 = RustField(name=element_9.name, colon=element_9.colon, type_expr=new_type_expr_5)
                            changed_30 = True
                        else:
                            new_element_9 = element_9
                        new_separator_8 = proc(separator_8)
                        assert(isinstance(new_separator_8, RustComma))
                        if new_separator_8 is not separator_8:
                            changed_30 = True
                        new_fields.append(new_element_9, new_separator_8)
                    new_last_8 = proc(element_8.fields.last)
                    assert(isinstance(new_last_8, RustField))
                    if new_last_8 is not element_8.fields.last:
                        changed_30 = True
                    new_fields.append_final(new_last_8)
                    if changed_30:
                        new_element_8 = RustStructVariant(name=element_8.name, open_brace=element_8.open_brace, fields=new_fields, comma=element_8.comma, close_brace=element_8.close_brace)
                        changed_2 = True
                    else:
                        new_element_8 = element_8
                elif isinstance(element_8, RustTupleVariant):
                    changed_32 = False
                    new_types = Punctuated()
                    for (element_10, separator_9) in element_8.types.delimited:
                        new_element_10 = proc(element_10)
                        assert(is_rust_type_expr(new_element_10))
                        if new_element_10 is not element_10:
                            changed_32 = True
                        new_separator_9 = proc(separator_9)
                        assert(isinstance(new_separator_9, RustComma))
                        if new_separator_9 is not separator_9:
                            changed_32 = True
                        new_types.append(new_element_10, new_separator_9)
                    new_last_9 = proc(element_8.types.last)
                    assert(is_rust_type_expr(new_last_9))
                    if new_last_9 is not element_8.types.last:
                        changed_32 = True
                    new_types.append_final(new_last_9)
                    if changed_32:
                        new_element_8 = RustTupleVariant(name=element_8.name, open_paren=element_8.open_paren, types=new_types, close_paren=element_8.close_paren)
                        changed_2 = True
                    else:
                        new_element_8 = element_8
                elif isinstance(element_8, RustEmptyVariant):
                    changed_33 = False
                    if isinstance(element_8.init, RustInit):
                        new_init = proc(element_8.init)
                        assert(isinstance(new_init, RustInit))
                        if new_init is not element_8.init:
                            changed_33 = True
                    elif element_8.init is None:
                        new_init = element_8.init
                    else:
                        assert_never(element_8.init)
                    if changed_33:
                        new_element_8 = RustEmptyVariant(name=element_8.name, init=new_init)
                        changed_2 = True
                    else:
                        new_element_8 = element_8
                else:
                    assert_never(element_8)
                new_separator_7 = proc(separator_7)
                assert(isinstance(new_separator_7, RustComma))
                if new_separator_7 is not separator_7:
                    changed_2 = True
                new_variants.append(new_element_8, new_separator_7)
            new_last_7 = proc(node.item.variants.last)
            assert(is_rust_variant(new_last_7))
            if new_last_7 is not node.item.variants.last:
                changed_2 = True
            new_variants.append_final(new_last_7)
            if changed_2:
                new_item = RustEnumItem(attrs=new_attrs, visibility=new_visibility, enum_keyword=node.item.enum_keyword, name=node.item.name, open_brace=node.item.open_brace, variants=new_variants, comma=node.item.comma, close_brace=node.item.close_brace)
                changed_1 = True
            else:
                new_item = node.item
        elif isinstance(node.item, RustStructItem):
            changed_34 = False
            new_attrs_1 = []
            for element_11 in node.item.attrs:
                new_element_11 = proc(element_11)
                assert(isinstance(new_element_11, RustAttr))
                if new_element_11 is not element_11:
                    changed_34 = True
                new_elements_3.append(new_element_11)
            if isinstance(node.item.visibility, RustPublic):
                new_visibility_1 = proc(node.item.visibility)
                assert(isinstance(new_visibility_1, RustPublic))
                if new_visibility_1 is not node.item.visibility:
                    changed_34 = True
            elif node.item.visibility is None:
                new_visibility_1 = node.item.visibility
            else:
                assert_never(node.item.visibility)
            new_fields_1 = Punctuated()
            for (element_12, separator_10) in node.item.fields.delimited:
                new_element_12 = proc(element_12)
                assert(isinstance(new_element_12, RustField))
                if new_element_12 is not element_12:
                    changed_34 = True
                new_separator_10 = proc(separator_10)
                assert(isinstance(new_separator_10, RustComma))
                if new_separator_10 is not separator_10:
                    changed_34 = True
                new_fields_1.append(new_element_12, new_separator_10)
            new_last_10 = proc(node.item.fields.last)
            assert(isinstance(new_last_10, RustField))
            if new_last_10 is not node.item.fields.last:
                changed_34 = True
            new_fields_1.append_final(new_last_10)
            if changed_34:
                new_item = RustStructItem(attrs=new_attrs_1, visibility=new_visibility_1, struct_keyword=node.item.struct_keyword, name=node.item.name, open_brace=node.item.open_brace, fields=new_fields_1, comma=node.item.comma, close_brace=node.item.close_brace)
                changed_1 = True
            else:
                new_item = node.item
        elif isinstance(node.item, RustUseItem):
            changed_35 = False
            new_attrs_2 = []
            for element_13 in node.item.attrs:
                new_element_13 = proc(element_13)
                assert(isinstance(new_element_13, RustAttr))
                if new_element_13 is not element_13:
                    changed_35 = True
                new_elements_4.append(new_element_13)
            if isinstance(node.item.visibility, RustPublic):
                new_visibility_2 = proc(node.item.visibility)
                assert(isinstance(new_visibility_2, RustPublic))
                if new_visibility_2 is not node.item.visibility:
                    changed_35 = True
            elif node.item.visibility is None:
                new_visibility_2 = node.item.visibility
            else:
                assert_never(node.item.visibility)
            if changed_35:
                new_item = RustUseItem(attrs=new_attrs_2, visibility=new_visibility_2, use_keyword=node.item.use_keyword, colon_colon=node.item.colon_colon, path=node.item.path, semicolon=node.item.semicolon)
                changed_1 = True
            else:
                new_item = node.item
        elif isinstance(node.item, RustExprItem):
            changed_36 = False
            new_expr_3 = proc(node.item.expr)
            assert(is_rust_expr(new_expr_3))
            if new_expr_3 is not node.item.expr:
                changed_36 = True
            if changed_36:
                new_item = RustExprItem(expr=new_expr_3)
                changed_1 = True
            else:
                new_item = node.item
        else:
            assert_never(node.item)
        new_last_11 = proc(node.last)
        assert(is_rust_expr(new_last_11))
        if new_last_11 is not node.last:
            changed_1 = True
        if changed_1:
            rewritten = RustBlockExpr(open_brace=node.open_brace, item=new_item, semicolon=node.semicolon, last=new_last_11, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustCallExpr):
        changed_37 = False
        new_operator = proc(node.operator)
        assert(is_rust_expr(new_operator))
        if new_operator is not node.operator:
            changed_37 = True
        new_args_3 = Punctuated()
        for (element_14, separator_11) in node.args.delimited:
            new_element_14 = proc(element_14)
            assert(is_rust_expr(new_element_14))
            if new_element_14 is not element_14:
                changed_37 = True
            new_separator_11 = proc(separator_11)
            assert(isinstance(new_separator_11, RustComma))
            if new_separator_11 is not separator_11:
                changed_37 = True
            new_args_3.append(new_element_14, new_separator_11)
        new_last_12 = proc(node.args.last)
        assert(is_rust_expr(new_last_12))
        if new_last_12 is not node.args.last:
            changed_37 = True
        new_args_3.append_final(new_last_12)
        if changed_37:
            rewritten = RustCallExpr(operator=new_operator, open_paren=node.open_paren, args=new_args_3, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustLitExpr):
        rewritten = node
    elif isinstance(node, RustPathExpr):
        changed_39 = False
        new_attrs_3 = []
        for element_15 in node.attrs:
            new_element_15 = proc(element_15)
            assert(isinstance(new_element_15, RustAttr))
            if new_element_15 is not element_15:
                changed_39 = True
            new_elements_5.append(new_element_15)
        if isinstance(node.qself, RustQself):
            new_qself_1 = proc(node.qself)
            assert(isinstance(new_qself_1, RustQself))
            if new_qself_1 is not node.qself:
                changed_39 = True
        elif node.qself is None:
            new_qself_1 = node.qself
        else:
            assert_never(node.qself)
        new_path_8 = proc(node.path)
        assert(isinstance(new_path_8, RustPath))
        if new_path_8 is not node.path:
            changed_39 = True
        if changed_39:
            rewritten = RustPathExpr(attrs=new_attrs_3, qself=new_qself_1, path=new_path_8)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustRetExpr):
        changed_40 = False
        new_expr_4 = proc(node.expr)
        assert(is_rust_expr(new_expr_4))
        if new_expr_4 is not node.expr:
            changed_40 = True
        if changed_40:
            rewritten = RustRetExpr(return_keyword=node.return_keyword, expr=new_expr_4)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustStructExpr):
        changed_41 = False
        new_path_9 = proc(node.path)
        assert(isinstance(new_path_9, RustPath))
        if new_path_9 is not node.path:
            changed_41 = True
        new_inits = Punctuated()
        for (element_16, separator_12) in node.inits.delimited:
            new_element_16 = proc(element_16)
            assert(isinstance(new_element_16, RustInit))
            if new_element_16 is not element_16:
                changed_41 = True
            new_separator_12 = proc(separator_12)
            assert(isinstance(new_separator_12, RustComma))
            if new_separator_12 is not separator_12:
                changed_41 = True
            new_inits.append(new_element_16, new_separator_12)
        new_last_13 = proc(node.inits.last)
        assert(isinstance(new_last_13, RustInit))
        if new_last_13 is not node.inits.last:
            changed_41 = True
        new_inits.append_final(new_last_13)
        if changed_41:
            rewritten = RustStructExpr(path=new_path_9, open_brace=node.open_brace, inits=new_inits, comma=node.comma, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_generic_argument(node: RustGenericArgument, proc: Callable[[RustGenericArgument], RustGenericArgument]) -> RustGenericArgument:
    if isinstance(node, RustAssocConst):
        changed_1 = False
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            changed_2 = False
            new_args = Punctuated()
            for (element, separator) in node.generics.args.delimited:
                new_element = proc(element)
                assert(is_rust_generic_argument(new_element))
                if new_element is not element:
                    changed_2 = True
                new_separator = separator
                new_args.append(new_element, new_separator)
            new_last = proc(node.generics.args.last)
            assert(is_rust_generic_argument(new_last))
            if new_last is not node.generics.args.last:
                changed_2 = True
            new_args.append_final(new_last)
            if changed_2:
                new_generics = RustAngleBracketedGenericArguments(less_than=node.generics.less_than, args=new_args, greater_than=node.generics.greater_than)
                changed_1 = True
            else:
                new_generics = node.generics
        elif node.generics is None:
            new_generics = node.generics
        else:
            assert_never(node.generics)
        if isinstance(node.expr, RustLitExpr):
            new_expr = node.expr
        elif isinstance(node.expr, RustPathExpr):
            changed_4 = False
            new_attrs = []
            for element_1 in node.expr.attrs:
                changed_5 = False
                if isinstance(element_1.meta, RustMetaPath):
                    changed_6 = False
                    changed_7 = False
                    new_segments = Punctuated()
                    for (element_2, separator_1) in element_1.meta.path.segments.delimited:
                        changed_8 = False
                        if is_rust_path_arguments(element_2.args):
                            if isinstance(element_2.args, RustTurbofish):
                                changed_9 = False
                                new_args_2 = Punctuated()
                                for (element_3, separator_2) in element_2.args.args.delimited:
                                    new_element_3 = proc(element_3)
                                    assert(is_rust_generic_argument(new_element_3))
                                    if new_element_3 is not element_3:
                                        changed_9 = True
                                    new_separator_2 = proc(separator_2)
                                    assert(isinstance(new_separator_2, RustComma))
                                    if new_separator_2 is not separator_2:
                                        changed_9 = True
                                    new_args_2.append(new_element_3, new_separator_2)
                                new_last_2 = proc(element_2.args.args.last)
                                assert(is_rust_generic_argument(new_last_2))
                                if new_last_2 is not element_2.args.args.last:
                                    changed_9 = True
                                new_args_2.append_final(new_last_2)
                                if changed_9:
                                    new_args_1 = RustTurbofish(colon_colon=element_2.args.colon_colon, less_than=element_2.args.less_than, args=new_args_2, greater_than=element_2.args.greater_than)
                                    changed_8 = True
                                else:
                                    new_args_1 = element_2.args
                            elif isinstance(element_2.args, RustAngleBracketedGenericArguments):
                                new_args_1 = proc(element_2.args)
                                assert(isinstance(new_args_1, RustAngleBracketedGenericArguments))
                                if new_args_1 is not element_2.args:
                                    changed_8 = True
                            elif isinstance(element_2.args, RustParenthesizedGenericArguments):
                                changed_10 = False
                                new_params = Punctuated()
                                for (element_4, separator_3) in element_2.args.params.delimited:
                                    if isinstance(element_4, RustPathTypeExpr):
                                        changed_11 = False
                                        if isinstance(element_4.qself, RustQself):
                                            changed_12 = False
                                            new_type_expr = proc(element_4.qself.type_expr)
                                            assert(is_rust_type_expr(new_type_expr))
                                            if new_type_expr is not element_4.qself.type_expr:
                                                changed_12 = True
                                            new_path_1 = proc(element_4.qself.path)
                                            assert(isinstance(new_path_1, RustPath))
                                            if new_path_1 is not element_4.qself.path:
                                                changed_12 = True
                                            if changed_12:
                                                new_qself = RustQself(less_than=element_4.qself.less_than, type_expr=new_type_expr, as_keyword=element_4.qself.as_keyword, path=new_path_1, greater_than=element_4.qself.greater_than)
                                                changed_11 = True
                                            else:
                                                new_qself = element_4.qself
                                        elif element_4.qself is None:
                                            new_qself = element_4.qself
                                        else:
                                            assert_never(element_4.qself)
                                        new_path_2 = proc(element_4.path)
                                        assert(isinstance(new_path_2, RustPath))
                                        if new_path_2 is not element_4.path:
                                            changed_11 = True
                                        if changed_11:
                                            new_element_4 = RustPathTypeExpr(qself=new_qself, path=new_path_2)
                                            changed_10 = True
                                        else:
                                            new_element_4 = element_4
                                    elif isinstance(element_4, RustArrayTypeExpr):
                                        changed_13 = False
                                        new_type_expr_1 = proc(element_4.type_expr)
                                        assert(is_rust_type_expr(new_type_expr_1))
                                        if new_type_expr_1 is not element_4.type_expr:
                                            changed_13 = True
                                        new_expr_1 = proc(element_4.expr)
                                        assert(is_rust_expr(new_expr_1))
                                        if new_expr_1 is not element_4.expr:
                                            changed_13 = True
                                        if changed_13:
                                            new_element_4 = RustArrayTypeExpr(open_bracket=element_4.open_bracket, type_expr=new_type_expr_1, semicolon=element_4.semicolon, expr=new_expr_1, close_bracket=element_4.close_bracket)
                                            changed_10 = True
                                        else:
                                            new_element_4 = element_4
                                    elif isinstance(element_4, RustNeverTypeExpr):
                                        new_element_4 = element_4
                                    elif isinstance(element_4, RustTupleTypeExpr):
                                        changed_15 = False
                                        new_elements_1 = Punctuated()
                                        for (element_5, separator_4) in element_4.elements.delimited:
                                            new_element_5 = proc(element_5)
                                            assert(is_rust_type_expr(new_element_5))
                                            if new_element_5 is not element_5:
                                                changed_15 = True
                                            new_separator_4 = proc(separator_4)
                                            assert(isinstance(new_separator_4, RustComma))
                                            if new_separator_4 is not separator_4:
                                                changed_15 = True
                                            new_elements_1.append(new_element_5, new_separator_4)
                                        new_last_4 = proc(element_4.elements.last)
                                        assert(is_rust_type_expr(new_last_4))
                                        if new_last_4 is not element_4.elements.last:
                                            changed_15 = True
                                        new_elements_1.append_final(new_last_4)
                                        if changed_15:
                                            new_element_4 = RustTupleTypeExpr(open_paren=element_4.open_paren, elements=new_elements_1, close_paren=element_4.close_paren)
                                            changed_10 = True
                                        else:
                                            new_element_4 = element_4
                                    else:
                                        assert_never(element_4)
                                    new_separator_3 = proc(separator_3)
                                    assert(isinstance(new_separator_3, RustComma))
                                    if new_separator_3 is not separator_3:
                                        changed_10 = True
                                    new_params.append(new_element_4, new_separator_3)
                                new_last_3 = proc(element_2.args.params.last)
                                assert(is_rust_type_expr(new_last_3))
                                if new_last_3 is not element_2.args.params.last:
                                    changed_10 = True
                                new_params.append_final(new_last_3)
                                new_result = proc(element_2.args.result)
                                assert(is_rust_type_expr(new_result))
                                if new_result is not element_2.args.result:
                                    changed_10 = True
                                if changed_10:
                                    new_args_1 = RustParenthesizedGenericArguments(open_paren=element_2.args.open_paren, params=new_params, close_paren=element_2.args.close_paren, r_arrow=element_2.args.r_arrow, result=new_result)
                                    changed_8 = True
                                else:
                                    new_args_1 = element_2.args
                            else:
                                assert_never(element_2.args)
                        elif element_2.args is None:
                            new_args_1 = element_2.args
                        else:
                            assert_never(element_2.args)
                        if changed_8:
                            new_element_2 = RustPathSegment(name=element_2.name, args=new_args_1)
                            changed_7 = True
                        else:
                            new_element_2 = element_2
                        new_separator_1 = separator_1
                        new_segments.append(new_element_2, new_separator_1)
                    new_last_1 = proc(element_1.meta.path.segments.last)
                    assert(isinstance(new_last_1, RustPathSegment))
                    if new_last_1 is not element_1.meta.path.segments.last:
                        changed_7 = True
                    new_segments.append_final(new_last_1)
                    if changed_7:
                        new_path = RustPath(leading_colon_colon=element_1.meta.path.leading_colon_colon, segments=new_segments)
                        changed_6 = True
                    else:
                        new_path = element_1.meta.path
                    if changed_6:
                        new_meta = RustMetaPath(path=new_path)
                        changed_5 = True
                    else:
                        new_meta = element_1.meta
                elif isinstance(element_1.meta, RustMetaParenthesized):
                    changed_16 = False
                    new_path_3 = proc(element_1.meta.path)
                    assert(isinstance(new_path_3, RustPath))
                    if new_path_3 is not element_1.meta.path:
                        changed_16 = True
                    if changed_16:
                        new_meta = RustMetaParenthesized(path=new_path_3, open_paren=element_1.meta.open_paren, tokens=element_1.meta.tokens, close_paren=element_1.meta.close_paren)
                        changed_5 = True
                    else:
                        new_meta = element_1.meta
                elif isinstance(element_1.meta, RustMetaBracketed):
                    changed_17 = False
                    new_path_4 = proc(element_1.meta.path)
                    assert(isinstance(new_path_4, RustPath))
                    if new_path_4 is not element_1.meta.path:
                        changed_17 = True
                    if changed_17:
                        new_meta = RustMetaBracketed(path=new_path_4, open_bracket=element_1.meta.open_bracket, tokens=element_1.meta.tokens, close_bracket=element_1.meta.close_bracket)
                        changed_5 = True
                    else:
                        new_meta = element_1.meta
                elif isinstance(element_1.meta, RustMetaBraced):
                    changed_18 = False
                    new_path_5 = proc(element_1.meta.path)
                    assert(isinstance(new_path_5, RustPath))
                    if new_path_5 is not element_1.meta.path:
                        changed_18 = True
                    if changed_18:
                        new_meta = RustMetaBraced(path=new_path_5, open_brace=element_1.meta.open_brace, tokens=element_1.meta.tokens, close_brace=element_1.meta.close_brace)
                        changed_5 = True
                    else:
                        new_meta = element_1.meta
                elif isinstance(element_1.meta, RustMetaNameValue):
                    changed_19 = False
                    new_path_6 = proc(element_1.meta.path)
                    assert(isinstance(new_path_6, RustPath))
                    if new_path_6 is not element_1.meta.path:
                        changed_19 = True
                    new_expr_2 = proc(element_1.meta.expr)
                    assert(is_rust_expr(new_expr_2))
                    if new_expr_2 is not element_1.meta.expr:
                        changed_19 = True
                    if changed_19:
                        new_meta = RustMetaNameValue(path=new_path_6, equals=element_1.meta.equals, expr=new_expr_2)
                        changed_5 = True
                    else:
                        new_meta = element_1.meta
                else:
                    assert_never(element_1.meta)
                if changed_5:
                    new_element_1 = RustAttr(hashtag=element_1.hashtag, exclamation_mark=element_1.exclamation_mark, open_bracket=element_1.open_bracket, meta=new_meta, close_bracket=element_1.close_bracket)
                    changed_4 = True
                else:
                    new_element_1 = element_1
                new_elements.append(new_element_1)
            if isinstance(node.expr.qself, RustQself):
                new_qself_1 = proc(node.expr.qself)
                assert(isinstance(new_qself_1, RustQself))
                if new_qself_1 is not node.expr.qself:
                    changed_4 = True
            elif node.expr.qself is None:
                new_qself_1 = node.expr.qself
            else:
                assert_never(node.expr.qself)
            new_path_7 = proc(node.expr.path)
            assert(isinstance(new_path_7, RustPath))
            if new_path_7 is not node.expr.path:
                changed_4 = True
            if changed_4:
                new_expr = RustPathExpr(attrs=new_attrs, qself=new_qself_1, path=new_path_7)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustCallExpr):
            changed_20 = False
            new_operator = proc(node.expr.operator)
            assert(is_rust_expr(new_operator))
            if new_operator is not node.expr.operator:
                changed_20 = True
            new_args_3 = Punctuated()
            for (element_6, separator_5) in node.expr.args.delimited:
                new_element_6 = proc(element_6)
                assert(is_rust_expr(new_element_6))
                if new_element_6 is not element_6:
                    changed_20 = True
                new_separator_5 = proc(separator_5)
                assert(isinstance(new_separator_5, RustComma))
                if new_separator_5 is not separator_5:
                    changed_20 = True
                new_args_3.append(new_element_6, new_separator_5)
            new_last_5 = proc(node.expr.args.last)
            assert(is_rust_expr(new_last_5))
            if new_last_5 is not node.expr.args.last:
                changed_20 = True
            new_args_3.append_final(new_last_5)
            if changed_20:
                new_expr = RustCallExpr(operator=new_operator, open_paren=node.expr.open_paren, args=new_args_3, close_paren=node.expr.close_paren)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustStructExpr):
            changed_21 = False
            new_path_8 = proc(node.expr.path)
            assert(isinstance(new_path_8, RustPath))
            if new_path_8 is not node.expr.path:
                changed_21 = True
            new_inits = Punctuated()
            for (element_7, separator_6) in node.expr.inits.delimited:
                changed_22 = False
                new_value = proc(element_7.value)
                assert(is_rust_expr(new_value))
                if new_value is not element_7.value:
                    changed_22 = True
                if changed_22:
                    new_element_7 = RustInit(name=element_7.name, equals=element_7.equals, value=new_value)
                    changed_21 = True
                else:
                    new_element_7 = element_7
                new_separator_6 = proc(separator_6)
                assert(isinstance(new_separator_6, RustComma))
                if new_separator_6 is not separator_6:
                    changed_21 = True
                new_inits.append(new_element_7, new_separator_6)
            new_last_6 = proc(node.expr.inits.last)
            assert(isinstance(new_last_6, RustInit))
            if new_last_6 is not node.expr.inits.last:
                changed_21 = True
            new_inits.append_final(new_last_6)
            if changed_21:
                new_expr = RustStructExpr(path=new_path_8, open_brace=node.expr.open_brace, inits=new_inits, comma=node.expr.comma, close_brace=node.expr.close_brace)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustBlockExpr):
            changed_23 = False
            if isinstance(node.expr.item, RustEnumItem):
                changed_24 = False
                new_attrs_1 = []
                for element_8 in node.expr.item.attrs:
                    new_element_8 = proc(element_8)
                    assert(isinstance(new_element_8, RustAttr))
                    if new_element_8 is not element_8:
                        changed_24 = True
                    new_elements_2.append(new_element_8)
                if isinstance(node.expr.item.visibility, RustPublic):
                    changed_25 = False
                    if isinstance(node.expr.item.visibility.restrict, tuple):
                        new_elements_3 = []
                        element_0 = node.expr.item.visibility.restrict[0]
                        new_element_0 = element_0
                        new_elements_3.append(new_element_0)
                        element_1 = node.expr.item.visibility.restrict[1]
                        if isinstance(element_1, RustInKeyword):
                            new_element_1 = element_1
                        elif element_1 is None:
                            new_element_1 = element_1
                        else:
                            assert_never(element_1)
                        new_elements_3.append(new_element_1)
                        element_2 = node.expr.item.visibility.restrict[2]
                        new_element_2 = proc(element_2)
                        assert(isinstance(new_element_2, RustPath))
                        if new_element_2 is not element_2:
                            changed_25 = True
                        new_elements_3.append(new_element_2)
                        element_3 = node.expr.item.visibility.restrict[3]
                        new_element_3 = element_3
                        new_elements_3.append(new_element_3)
                        new_restrict = tuple(new_elements_3) if changed_25 else node.expr.item.visibility.restrict
                    elif node.expr.item.visibility.restrict is None:
                        new_restrict = node.expr.item.visibility.restrict
                    else:
                        assert_never(node.expr.item.visibility.restrict)
                    if changed_25:
                        new_visibility = RustPublic(pub_keyword=node.expr.item.visibility.pub_keyword, restrict=new_restrict)
                        changed_24 = True
                    else:
                        new_visibility = node.expr.item.visibility
                elif node.expr.item.visibility is None:
                    new_visibility = node.expr.item.visibility
                else:
                    assert_never(node.expr.item.visibility)
                new_variants = Punctuated()
                for (element_9, separator_7) in node.expr.item.variants.delimited:
                    if isinstance(element_9, RustStructVariant):
                        changed_26 = False
                        new_fields = Punctuated()
                        for (element_10, separator_8) in element_9.fields.delimited:
                            changed_27 = False
                            new_type_expr_2 = proc(element_10.type_expr)
                            assert(is_rust_type_expr(new_type_expr_2))
                            if new_type_expr_2 is not element_10.type_expr:
                                changed_27 = True
                            if changed_27:
                                new_element_10 = RustField(name=element_10.name, colon=element_10.colon, type_expr=new_type_expr_2)
                                changed_26 = True
                            else:
                                new_element_10 = element_10
                            new_separator_8 = proc(separator_8)
                            assert(isinstance(new_separator_8, RustComma))
                            if new_separator_8 is not separator_8:
                                changed_26 = True
                            new_fields.append(new_element_10, new_separator_8)
                        new_last_8 = proc(element_9.fields.last)
                        assert(isinstance(new_last_8, RustField))
                        if new_last_8 is not element_9.fields.last:
                            changed_26 = True
                        new_fields.append_final(new_last_8)
                        if changed_26:
                            new_element_9 = RustStructVariant(name=element_9.name, open_brace=element_9.open_brace, fields=new_fields, comma=element_9.comma, close_brace=element_9.close_brace)
                            changed_24 = True
                        else:
                            new_element_9 = element_9
                    elif isinstance(element_9, RustTupleVariant):
                        changed_28 = False
                        new_types = Punctuated()
                        for (element_11, separator_9) in element_9.types.delimited:
                            new_element_11 = proc(element_11)
                            assert(is_rust_type_expr(new_element_11))
                            if new_element_11 is not element_11:
                                changed_28 = True
                            new_separator_9 = proc(separator_9)
                            assert(isinstance(new_separator_9, RustComma))
                            if new_separator_9 is not separator_9:
                                changed_28 = True
                            new_types.append(new_element_11, new_separator_9)
                        new_last_9 = proc(element_9.types.last)
                        assert(is_rust_type_expr(new_last_9))
                        if new_last_9 is not element_9.types.last:
                            changed_28 = True
                        new_types.append_final(new_last_9)
                        if changed_28:
                            new_element_9 = RustTupleVariant(name=element_9.name, open_paren=element_9.open_paren, types=new_types, close_paren=element_9.close_paren)
                            changed_24 = True
                        else:
                            new_element_9 = element_9
                    elif isinstance(element_9, RustEmptyVariant):
                        changed_29 = False
                        if isinstance(element_9.init, RustInit):
                            new_init = proc(element_9.init)
                            assert(isinstance(new_init, RustInit))
                            if new_init is not element_9.init:
                                changed_29 = True
                        elif element_9.init is None:
                            new_init = element_9.init
                        else:
                            assert_never(element_9.init)
                        if changed_29:
                            new_element_9 = RustEmptyVariant(name=element_9.name, init=new_init)
                            changed_24 = True
                        else:
                            new_element_9 = element_9
                    else:
                        assert_never(element_9)
                    new_separator_7 = proc(separator_7)
                    assert(isinstance(new_separator_7, RustComma))
                    if new_separator_7 is not separator_7:
                        changed_24 = True
                    new_variants.append(new_element_9, new_separator_7)
                new_last_7 = proc(node.expr.item.variants.last)
                assert(is_rust_variant(new_last_7))
                if new_last_7 is not node.expr.item.variants.last:
                    changed_24 = True
                new_variants.append_final(new_last_7)
                if changed_24:
                    new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=node.expr.item.enum_keyword, name=node.expr.item.name, open_brace=node.expr.item.open_brace, variants=new_variants, comma=node.expr.item.comma, close_brace=node.expr.item.close_brace)
                    changed_23 = True
                else:
                    new_item = node.expr.item
            elif isinstance(node.expr.item, RustStructItem):
                changed_30 = False
                new_attrs_2 = []
                for element_12 in node.expr.item.attrs:
                    new_element_12 = proc(element_12)
                    assert(isinstance(new_element_12, RustAttr))
                    if new_element_12 is not element_12:
                        changed_30 = True
                    new_elements_4.append(new_element_12)
                if isinstance(node.expr.item.visibility, RustPublic):
                    new_visibility_1 = proc(node.expr.item.visibility)
                    assert(isinstance(new_visibility_1, RustPublic))
                    if new_visibility_1 is not node.expr.item.visibility:
                        changed_30 = True
                elif node.expr.item.visibility is None:
                    new_visibility_1 = node.expr.item.visibility
                else:
                    assert_never(node.expr.item.visibility)
                new_fields_1 = Punctuated()
                for (element_13, separator_10) in node.expr.item.fields.delimited:
                    new_element_13 = proc(element_13)
                    assert(isinstance(new_element_13, RustField))
                    if new_element_13 is not element_13:
                        changed_30 = True
                    new_separator_10 = proc(separator_10)
                    assert(isinstance(new_separator_10, RustComma))
                    if new_separator_10 is not separator_10:
                        changed_30 = True
                    new_fields_1.append(new_element_13, new_separator_10)
                new_last_10 = proc(node.expr.item.fields.last)
                assert(isinstance(new_last_10, RustField))
                if new_last_10 is not node.expr.item.fields.last:
                    changed_30 = True
                new_fields_1.append_final(new_last_10)
                if changed_30:
                    new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=node.expr.item.struct_keyword, name=node.expr.item.name, open_brace=node.expr.item.open_brace, fields=new_fields_1, comma=node.expr.item.comma, close_brace=node.expr.item.close_brace)
                    changed_23 = True
                else:
                    new_item = node.expr.item
            elif isinstance(node.expr.item, RustUseItem):
                changed_31 = False
                new_attrs_3 = []
                for element_14 in node.expr.item.attrs:
                    new_element_14 = proc(element_14)
                    assert(isinstance(new_element_14, RustAttr))
                    if new_element_14 is not element_14:
                        changed_31 = True
                    new_elements_5.append(new_element_14)
                if isinstance(node.expr.item.visibility, RustPublic):
                    new_visibility_2 = proc(node.expr.item.visibility)
                    assert(isinstance(new_visibility_2, RustPublic))
                    if new_visibility_2 is not node.expr.item.visibility:
                        changed_31 = True
                elif node.expr.item.visibility is None:
                    new_visibility_2 = node.expr.item.visibility
                else:
                    assert_never(node.expr.item.visibility)
                if changed_31:
                    new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=node.expr.item.use_keyword, colon_colon=node.expr.item.colon_colon, path=node.expr.item.path, semicolon=node.expr.item.semicolon)
                    changed_23 = True
                else:
                    new_item = node.expr.item
            elif isinstance(node.expr.item, RustExprItem):
                changed_32 = False
                new_expr_3 = proc(node.expr.item.expr)
                assert(is_rust_expr(new_expr_3))
                if new_expr_3 is not node.expr.item.expr:
                    changed_32 = True
                if changed_32:
                    new_item = RustExprItem(expr=new_expr_3)
                    changed_23 = True
                else:
                    new_item = node.expr.item
            else:
                assert_never(node.expr.item)
            new_last_11 = proc(node.expr.last)
            assert(is_rust_expr(new_last_11))
            if new_last_11 is not node.expr.last:
                changed_23 = True
            if changed_23:
                new_expr = RustBlockExpr(open_brace=node.expr.open_brace, item=new_item, semicolon=node.expr.semicolon, last=new_last_11, close_brace=node.expr.close_brace)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustRetExpr):
            changed_33 = False
            new_expr_4 = proc(node.expr.expr)
            assert(is_rust_expr(new_expr_4))
            if new_expr_4 is not node.expr.expr:
                changed_33 = True
            if changed_33:
                new_expr = RustRetExpr(return_keyword=node.expr.return_keyword, expr=new_expr_4)
                changed_1 = True
            else:
                new_expr = node.expr
        else:
            assert_never(node.expr)
        if changed_1:
            rewritten = RustAssocConst(name=node.name, generics=new_generics, equals=node.equals, expr=new_expr)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustAssocType):
        changed_34 = False
        if isinstance(node.generics, RustAngleBracketedGenericArguments):
            new_generics_1 = proc(node.generics)
            assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
            if new_generics_1 is not node.generics:
                changed_34 = True
        elif node.generics is None:
            new_generics_1 = node.generics
        else:
            assert_never(node.generics)
        new_type_expr_3 = proc(node.type_expr)
        assert(is_rust_type_expr(new_type_expr_3))
        if new_type_expr_3 is not node.type_expr:
            changed_34 = True
        if changed_34:
            rewritten = RustAssocType(name=node.name, generics=new_generics_1, equals=node.equals, type_expr=new_type_expr_3)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustConstraint):
        changed_35 = False
        new_generics_2 = proc(node.generics)
        assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
        if new_generics_2 is not node.generics:
            changed_35 = True
        new_bounds = Punctuated()
        for (element_15, separator_11) in node.bounds.delimited:
            if isinstance(element_15, RustTraitBound):
                changed_36 = False
                if isinstance(element_15.bound_lifetimes, RustBoundLifetimes):
                    changed_37 = False
                    new_lifetimes = Punctuated()
                    for (element_16, separator_12) in element_15.bound_lifetimes.lifetimes.delimited:
                        if isinstance(element_16, RustLifetime):
                            new_element_16 = proc(element_16)
                            assert(isinstance(new_element_16, RustLifetime))
                            if new_element_16 is not element_16:
                                changed_37 = True
                        elif isinstance(element_16, RustTypeParam):
                            changed_38 = False
                            new_type_param_bound = proc(element_16.type_param_bound)
                            assert(is_rust_type_param_bound(new_type_param_bound))
                            if new_type_param_bound is not element_16.type_param_bound:
                                changed_38 = True
                            if isinstance(element_16.default, RustTypeInit):
                                changed_39 = False
                                new_type_expr_4 = proc(element_16.default.type_expr)
                                assert(is_rust_type_expr(new_type_expr_4))
                                if new_type_expr_4 is not element_16.default.type_expr:
                                    changed_39 = True
                                if changed_39:
                                    new_default = RustTypeInit(equals=element_16.default.equals, type_expr=new_type_expr_4)
                                    changed_38 = True
                                else:
                                    new_default = element_16.default
                            elif element_16.default is None:
                                new_default = element_16.default
                            else:
                                assert_never(element_16.default)
                            if changed_38:
                                new_element_16 = RustTypeParam(name=element_16.name, colon=element_16.colon, type_param_bound=new_type_param_bound, percent=element_16.percent, plus=element_16.plus, default=new_default)
                                changed_37 = True
                            else:
                                new_element_16 = element_16
                        elif isinstance(element_16, RustConstParam):
                            changed_40 = False
                            new_type_expr_5 = proc(element_16.type_expr)
                            assert(is_rust_type_expr(new_type_expr_5))
                            if new_type_expr_5 is not element_16.type_expr:
                                changed_40 = True
                            if isinstance(element_16.default, RustInit):
                                new_default_1 = proc(element_16.default)
                                assert(isinstance(new_default_1, RustInit))
                                if new_default_1 is not element_16.default:
                                    changed_40 = True
                            elif element_16.default is None:
                                new_default_1 = element_16.default
                            else:
                                assert_never(element_16.default)
                            if changed_40:
                                new_element_16 = RustConstParam(const_keyword=element_16.const_keyword, name=element_16.name, colon=element_16.colon, type_expr=new_type_expr_5, default=new_default_1)
                                changed_37 = True
                            else:
                                new_element_16 = element_16
                        else:
                            assert_never(element_16)
                        new_separator_12 = proc(separator_12)
                        assert(isinstance(new_separator_12, RustComma))
                        if new_separator_12 is not separator_12:
                            changed_37 = True
                        new_lifetimes.append(new_element_16, new_separator_12)
                    new_last_13 = proc(element_15.bound_lifetimes.lifetimes.last)
                    assert(is_rust_generic_param(new_last_13))
                    if new_last_13 is not element_15.bound_lifetimes.lifetimes.last:
                        changed_37 = True
                    new_lifetimes.append_final(new_last_13)
                    if changed_37:
                        new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_15.bound_lifetimes.for_keyword, less_than=element_15.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_15.bound_lifetimes.greater_than)
                        changed_36 = True
                    else:
                        new_bound_lifetimes = element_15.bound_lifetimes
                elif element_15.bound_lifetimes is None:
                    new_bound_lifetimes = element_15.bound_lifetimes
                else:
                    assert_never(element_15.bound_lifetimes)
                new_path_9 = proc(element_15.path)
                assert(isinstance(new_path_9, RustPath))
                if new_path_9 is not element_15.path:
                    changed_36 = True
                if changed_36:
                    new_element_15 = RustTraitBound(modifier=element_15.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_9)
                    changed_35 = True
                else:
                    new_element_15 = element_15
            elif isinstance(element_15, RustLifetime):
                new_element_15 = proc(element_15)
                assert(isinstance(new_element_15, RustLifetime))
                if new_element_15 is not element_15:
                    changed_35 = True
            else:
                assert_never(element_15)
            new_separator_11 = separator_11
            new_bounds.append(new_element_15, new_separator_11)
        new_last_12 = proc(node.bounds.last)
        assert(is_rust_type_param_bound(new_last_12))
        if new_last_12 is not node.bounds.last:
            changed_35 = True
        new_bounds.append_final(new_last_12)
        if changed_35:
            rewritten = RustConstraint(name=node.name, generics=new_generics_2, colon=node.colon, bounds=new_bounds)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustLifetime):
        rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_generic_param(node: RustGenericParam, proc: Callable[[RustGenericParam], RustGenericParam]) -> RustGenericParam:
    if isinstance(node, RustConstParam):
        changed_1 = False
        if isinstance(node.type_expr, RustPathTypeExpr):
            changed_2 = False
            if isinstance(node.type_expr.qself, RustQself):
                changed_3 = False
                new_type_expr_1 = proc(node.type_expr.qself.type_expr)
                assert(is_rust_type_expr(new_type_expr_1))
                if new_type_expr_1 is not node.type_expr.qself.type_expr:
                    changed_3 = True
                changed_4 = False
                new_segments = Punctuated()
                for (element, separator) in node.type_expr.qself.path.segments.delimited:
                    changed_5 = False
                    if is_rust_path_arguments(element.args):
                        if isinstance(element.args, RustTurbofish):
                            changed_6 = False
                            new_args_1 = Punctuated()
                            for (element_1, separator_1) in element.args.args.delimited:
                                if isinstance(element_1, RustLifetime):
                                    new_element_1 = proc(element_1)
                                    assert(isinstance(new_element_1, RustLifetime))
                                    if new_element_1 is not element_1:
                                        changed_6 = True
                                elif is_rust_type_expr(element_1):
                                    new_element_1 = proc(element_1)
                                    assert(is_rust_type_expr(new_element_1))
                                    if new_element_1 is not element_1:
                                        changed_6 = True
                                elif is_rust_expr(element_1):
                                    if isinstance(element_1, RustLitExpr):
                                        new_element_1 = element_1
                                    elif isinstance(element_1, RustPathExpr):
                                        changed_8 = False
                                        new_attrs = []
                                        for element_2 in element_1.attrs:
                                            changed_9 = False
                                            if isinstance(element_2.meta, RustMetaPath):
                                                changed_10 = False
                                                new_path_1 = proc(element_2.meta.path)
                                                assert(isinstance(new_path_1, RustPath))
                                                if new_path_1 is not element_2.meta.path:
                                                    changed_10 = True
                                                if changed_10:
                                                    new_meta = RustMetaPath(path=new_path_1)
                                                    changed_9 = True
                                                else:
                                                    new_meta = element_2.meta
                                            elif isinstance(element_2.meta, RustMetaParenthesized):
                                                changed_11 = False
                                                new_path_2 = proc(element_2.meta.path)
                                                assert(isinstance(new_path_2, RustPath))
                                                if new_path_2 is not element_2.meta.path:
                                                    changed_11 = True
                                                if changed_11:
                                                    new_meta = RustMetaParenthesized(path=new_path_2, open_paren=element_2.meta.open_paren, tokens=element_2.meta.tokens, close_paren=element_2.meta.close_paren)
                                                    changed_9 = True
                                                else:
                                                    new_meta = element_2.meta
                                            elif isinstance(element_2.meta, RustMetaBracketed):
                                                changed_12 = False
                                                new_path_3 = proc(element_2.meta.path)
                                                assert(isinstance(new_path_3, RustPath))
                                                if new_path_3 is not element_2.meta.path:
                                                    changed_12 = True
                                                if changed_12:
                                                    new_meta = RustMetaBracketed(path=new_path_3, open_bracket=element_2.meta.open_bracket, tokens=element_2.meta.tokens, close_bracket=element_2.meta.close_bracket)
                                                    changed_9 = True
                                                else:
                                                    new_meta = element_2.meta
                                            elif isinstance(element_2.meta, RustMetaBraced):
                                                changed_13 = False
                                                new_path_4 = proc(element_2.meta.path)
                                                assert(isinstance(new_path_4, RustPath))
                                                if new_path_4 is not element_2.meta.path:
                                                    changed_13 = True
                                                if changed_13:
                                                    new_meta = RustMetaBraced(path=new_path_4, open_brace=element_2.meta.open_brace, tokens=element_2.meta.tokens, close_brace=element_2.meta.close_brace)
                                                    changed_9 = True
                                                else:
                                                    new_meta = element_2.meta
                                            elif isinstance(element_2.meta, RustMetaNameValue):
                                                changed_14 = False
                                                new_path_5 = proc(element_2.meta.path)
                                                assert(isinstance(new_path_5, RustPath))
                                                if new_path_5 is not element_2.meta.path:
                                                    changed_14 = True
                                                new_expr = proc(element_2.meta.expr)
                                                assert(is_rust_expr(new_expr))
                                                if new_expr is not element_2.meta.expr:
                                                    changed_14 = True
                                                if changed_14:
                                                    new_meta = RustMetaNameValue(path=new_path_5, equals=element_2.meta.equals, expr=new_expr)
                                                    changed_9 = True
                                                else:
                                                    new_meta = element_2.meta
                                            else:
                                                assert_never(element_2.meta)
                                            if changed_9:
                                                new_element_2 = RustAttr(hashtag=element_2.hashtag, exclamation_mark=element_2.exclamation_mark, open_bracket=element_2.open_bracket, meta=new_meta, close_bracket=element_2.close_bracket)
                                                changed_8 = True
                                            else:
                                                new_element_2 = element_2
                                            new_elements.append(new_element_2)
                                        if isinstance(element_1.qself, RustQself):
                                            new_qself_1 = proc(element_1.qself)
                                            assert(isinstance(new_qself_1, RustQself))
                                            if new_qself_1 is not element_1.qself:
                                                changed_8 = True
                                        elif element_1.qself is None:
                                            new_qself_1 = element_1.qself
                                        else:
                                            assert_never(element_1.qself)
                                        new_path_6 = proc(element_1.path)
                                        assert(isinstance(new_path_6, RustPath))
                                        if new_path_6 is not element_1.path:
                                            changed_8 = True
                                        if changed_8:
                                            new_element_1 = RustPathExpr(attrs=new_attrs, qself=new_qself_1, path=new_path_6)
                                            changed_6 = True
                                        else:
                                            new_element_1 = element_1
                                    elif isinstance(element_1, RustCallExpr):
                                        changed_15 = False
                                        new_operator = proc(element_1.operator)
                                        assert(is_rust_expr(new_operator))
                                        if new_operator is not element_1.operator:
                                            changed_15 = True
                                        new_args_2 = Punctuated()
                                        for (element_3, separator_2) in element_1.args.delimited:
                                            new_element_3 = proc(element_3)
                                            assert(is_rust_expr(new_element_3))
                                            if new_element_3 is not element_3:
                                                changed_15 = True
                                            new_separator_2 = separator_2
                                            new_args_2.append(new_element_3, new_separator_2)
                                        new_last_2 = proc(element_1.args.last)
                                        assert(is_rust_expr(new_last_2))
                                        if new_last_2 is not element_1.args.last:
                                            changed_15 = True
                                        new_args_2.append_final(new_last_2)
                                        if changed_15:
                                            new_element_1 = RustCallExpr(operator=new_operator, open_paren=element_1.open_paren, args=new_args_2, close_paren=element_1.close_paren)
                                            changed_6 = True
                                        else:
                                            new_element_1 = element_1
                                    elif isinstance(element_1, RustStructExpr):
                                        changed_16 = False
                                        new_path_7 = proc(element_1.path)
                                        assert(isinstance(new_path_7, RustPath))
                                        if new_path_7 is not element_1.path:
                                            changed_16 = True
                                        new_inits = Punctuated()
                                        for (element_4, separator_3) in element_1.inits.delimited:
                                            changed_17 = False
                                            new_value = proc(element_4.value)
                                            assert(is_rust_expr(new_value))
                                            if new_value is not element_4.value:
                                                changed_17 = True
                                            if changed_17:
                                                new_element_4 = RustInit(name=element_4.name, equals=element_4.equals, value=new_value)
                                                changed_16 = True
                                            else:
                                                new_element_4 = element_4
                                            new_separator_3 = proc(separator_3)
                                            assert(isinstance(new_separator_3, RustComma))
                                            if new_separator_3 is not separator_3:
                                                changed_16 = True
                                            new_inits.append(new_element_4, new_separator_3)
                                        new_last_3 = proc(element_1.inits.last)
                                        assert(isinstance(new_last_3, RustInit))
                                        if new_last_3 is not element_1.inits.last:
                                            changed_16 = True
                                        new_inits.append_final(new_last_3)
                                        if changed_16:
                                            new_element_1 = RustStructExpr(path=new_path_7, open_brace=element_1.open_brace, inits=new_inits, comma=element_1.comma, close_brace=element_1.close_brace)
                                            changed_6 = True
                                        else:
                                            new_element_1 = element_1
                                    elif isinstance(element_1, RustBlockExpr):
                                        changed_18 = False
                                        if isinstance(element_1.item, RustEnumItem):
                                            changed_19 = False
                                            new_attrs_1 = []
                                            for element_5 in element_1.item.attrs:
                                                new_element_5 = proc(element_5)
                                                assert(isinstance(new_element_5, RustAttr))
                                                if new_element_5 is not element_5:
                                                    changed_19 = True
                                                new_elements_1.append(new_element_5)
                                            if isinstance(element_1.item.visibility, RustPublic):
                                                changed_20 = False
                                                if isinstance(element_1.item.visibility.restrict, tuple):
                                                    new_elements_2 = []
                                                    element_0 = element_1.item.visibility.restrict[0]
                                                    new_element_0 = element_0
                                                    new_elements_2.append(new_element_0)
                                                    element_1 = element_1.item.visibility.restrict[1]
                                                    if isinstance(element_1, RustInKeyword):
                                                        new_element_1 = element_1
                                                    elif element_1 is None:
                                                        new_element_1 = element_1
                                                    else:
                                                        assert_never(element_1)
                                                    new_elements_2.append(new_element_1)
                                                    element_2 = element_1.item.visibility.restrict[2]
                                                    new_element_2 = proc(element_2)
                                                    assert(isinstance(new_element_2, RustPath))
                                                    if new_element_2 is not element_2:
                                                        changed_20 = True
                                                    new_elements_2.append(new_element_2)
                                                    element_3 = element_1.item.visibility.restrict[3]
                                                    new_element_3 = element_3
                                                    new_elements_2.append(new_element_3)
                                                    new_restrict = tuple(new_elements_2) if changed_20 else element_1.item.visibility.restrict
                                                elif element_1.item.visibility.restrict is None:
                                                    new_restrict = element_1.item.visibility.restrict
                                                else:
                                                    assert_never(element_1.item.visibility.restrict)
                                                if changed_20:
                                                    new_visibility = RustPublic(pub_keyword=element_1.item.visibility.pub_keyword, restrict=new_restrict)
                                                    changed_19 = True
                                                else:
                                                    new_visibility = element_1.item.visibility
                                            elif element_1.item.visibility is None:
                                                new_visibility = element_1.item.visibility
                                            else:
                                                assert_never(element_1.item.visibility)
                                            new_variants = Punctuated()
                                            for (element_6, separator_4) in element_1.item.variants.delimited:
                                                if isinstance(element_6, RustStructVariant):
                                                    changed_21 = False
                                                    new_fields = Punctuated()
                                                    for (element_7, separator_5) in element_6.fields.delimited:
                                                        changed_22 = False
                                                        new_type_expr_2 = proc(element_7.type_expr)
                                                        assert(is_rust_type_expr(new_type_expr_2))
                                                        if new_type_expr_2 is not element_7.type_expr:
                                                            changed_22 = True
                                                        if changed_22:
                                                            new_element_7 = RustField(name=element_7.name, colon=element_7.colon, type_expr=new_type_expr_2)
                                                            changed_21 = True
                                                        else:
                                                            new_element_7 = element_7
                                                        new_separator_5 = proc(separator_5)
                                                        assert(isinstance(new_separator_5, RustComma))
                                                        if new_separator_5 is not separator_5:
                                                            changed_21 = True
                                                        new_fields.append(new_element_7, new_separator_5)
                                                    new_last_5 = proc(element_6.fields.last)
                                                    assert(isinstance(new_last_5, RustField))
                                                    if new_last_5 is not element_6.fields.last:
                                                        changed_21 = True
                                                    new_fields.append_final(new_last_5)
                                                    if changed_21:
                                                        new_element_6 = RustStructVariant(name=element_6.name, open_brace=element_6.open_brace, fields=new_fields, comma=element_6.comma, close_brace=element_6.close_brace)
                                                        changed_19 = True
                                                    else:
                                                        new_element_6 = element_6
                                                elif isinstance(element_6, RustTupleVariant):
                                                    changed_23 = False
                                                    new_types = Punctuated()
                                                    for (element_8, separator_6) in element_6.types.delimited:
                                                        new_element_8 = proc(element_8)
                                                        assert(is_rust_type_expr(new_element_8))
                                                        if new_element_8 is not element_8:
                                                            changed_23 = True
                                                        new_separator_6 = proc(separator_6)
                                                        assert(isinstance(new_separator_6, RustComma))
                                                        if new_separator_6 is not separator_6:
                                                            changed_23 = True
                                                        new_types.append(new_element_8, new_separator_6)
                                                    new_last_6 = proc(element_6.types.last)
                                                    assert(is_rust_type_expr(new_last_6))
                                                    if new_last_6 is not element_6.types.last:
                                                        changed_23 = True
                                                    new_types.append_final(new_last_6)
                                                    if changed_23:
                                                        new_element_6 = RustTupleVariant(name=element_6.name, open_paren=element_6.open_paren, types=new_types, close_paren=element_6.close_paren)
                                                        changed_19 = True
                                                    else:
                                                        new_element_6 = element_6
                                                elif isinstance(element_6, RustEmptyVariant):
                                                    changed_24 = False
                                                    if isinstance(element_6.init, RustInit):
                                                        new_init = proc(element_6.init)
                                                        assert(isinstance(new_init, RustInit))
                                                        if new_init is not element_6.init:
                                                            changed_24 = True
                                                    elif element_6.init is None:
                                                        new_init = element_6.init
                                                    else:
                                                        assert_never(element_6.init)
                                                    if changed_24:
                                                        new_element_6 = RustEmptyVariant(name=element_6.name, init=new_init)
                                                        changed_19 = True
                                                    else:
                                                        new_element_6 = element_6
                                                else:
                                                    assert_never(element_6)
                                                new_separator_4 = proc(separator_4)
                                                assert(isinstance(new_separator_4, RustComma))
                                                if new_separator_4 is not separator_4:
                                                    changed_19 = True
                                                new_variants.append(new_element_6, new_separator_4)
                                            new_last_4 = proc(element_1.item.variants.last)
                                            assert(is_rust_variant(new_last_4))
                                            if new_last_4 is not element_1.item.variants.last:
                                                changed_19 = True
                                            new_variants.append_final(new_last_4)
                                            if changed_19:
                                                new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=element_1.item.enum_keyword, name=element_1.item.name, open_brace=element_1.item.open_brace, variants=new_variants, comma=element_1.item.comma, close_brace=element_1.item.close_brace)
                                                changed_18 = True
                                            else:
                                                new_item = element_1.item
                                        elif isinstance(element_1.item, RustStructItem):
                                            changed_25 = False
                                            new_attrs_2 = []
                                            for element_9 in element_1.item.attrs:
                                                new_element_9 = proc(element_9)
                                                assert(isinstance(new_element_9, RustAttr))
                                                if new_element_9 is not element_9:
                                                    changed_25 = True
                                                new_elements_3.append(new_element_9)
                                            if isinstance(element_1.item.visibility, RustPublic):
                                                new_visibility_1 = proc(element_1.item.visibility)
                                                assert(isinstance(new_visibility_1, RustPublic))
                                                if new_visibility_1 is not element_1.item.visibility:
                                                    changed_25 = True
                                            elif element_1.item.visibility is None:
                                                new_visibility_1 = element_1.item.visibility
                                            else:
                                                assert_never(element_1.item.visibility)
                                            new_fields_1 = Punctuated()
                                            for (element_10, separator_7) in element_1.item.fields.delimited:
                                                new_element_10 = proc(element_10)
                                                assert(isinstance(new_element_10, RustField))
                                                if new_element_10 is not element_10:
                                                    changed_25 = True
                                                new_separator_7 = proc(separator_7)
                                                assert(isinstance(new_separator_7, RustComma))
                                                if new_separator_7 is not separator_7:
                                                    changed_25 = True
                                                new_fields_1.append(new_element_10, new_separator_7)
                                            new_last_7 = proc(element_1.item.fields.last)
                                            assert(isinstance(new_last_7, RustField))
                                            if new_last_7 is not element_1.item.fields.last:
                                                changed_25 = True
                                            new_fields_1.append_final(new_last_7)
                                            if changed_25:
                                                new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=element_1.item.struct_keyword, name=element_1.item.name, open_brace=element_1.item.open_brace, fields=new_fields_1, comma=element_1.item.comma, close_brace=element_1.item.close_brace)
                                                changed_18 = True
                                            else:
                                                new_item = element_1.item
                                        elif isinstance(element_1.item, RustUseItem):
                                            changed_26 = False
                                            new_attrs_3 = []
                                            for element_11 in element_1.item.attrs:
                                                new_element_11 = proc(element_11)
                                                assert(isinstance(new_element_11, RustAttr))
                                                if new_element_11 is not element_11:
                                                    changed_26 = True
                                                new_elements_4.append(new_element_11)
                                            if isinstance(element_1.item.visibility, RustPublic):
                                                new_visibility_2 = proc(element_1.item.visibility)
                                                assert(isinstance(new_visibility_2, RustPublic))
                                                if new_visibility_2 is not element_1.item.visibility:
                                                    changed_26 = True
                                            elif element_1.item.visibility is None:
                                                new_visibility_2 = element_1.item.visibility
                                            else:
                                                assert_never(element_1.item.visibility)
                                            if changed_26:
                                                new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=element_1.item.use_keyword, colon_colon=element_1.item.colon_colon, path=element_1.item.path, semicolon=element_1.item.semicolon)
                                                changed_18 = True
                                            else:
                                                new_item = element_1.item
                                        elif isinstance(element_1.item, RustExprItem):
                                            changed_27 = False
                                            new_expr_1 = proc(element_1.item.expr)
                                            assert(is_rust_expr(new_expr_1))
                                            if new_expr_1 is not element_1.item.expr:
                                                changed_27 = True
                                            if changed_27:
                                                new_item = RustExprItem(expr=new_expr_1)
                                                changed_18 = True
                                            else:
                                                new_item = element_1.item
                                        else:
                                            assert_never(element_1.item)
                                        new_last_8 = proc(element_1.last)
                                        assert(is_rust_expr(new_last_8))
                                        if new_last_8 is not element_1.last:
                                            changed_18 = True
                                        if changed_18:
                                            new_element_1 = RustBlockExpr(open_brace=element_1.open_brace, item=new_item, semicolon=element_1.semicolon, last=new_last_8, close_brace=element_1.close_brace)
                                            changed_6 = True
                                        else:
                                            new_element_1 = element_1
                                    elif isinstance(element_1, RustRetExpr):
                                        changed_28 = False
                                        new_expr_2 = proc(element_1.expr)
                                        assert(is_rust_expr(new_expr_2))
                                        if new_expr_2 is not element_1.expr:
                                            changed_28 = True
                                        if changed_28:
                                            new_element_1 = RustRetExpr(return_keyword=element_1.return_keyword, expr=new_expr_2)
                                            changed_6 = True
                                        else:
                                            new_element_1 = element_1
                                    else:
                                        assert_never(element_1)
                                elif isinstance(element_1, RustAssocType):
                                    changed_29 = False
                                    if isinstance(element_1.generics, RustAngleBracketedGenericArguments):
                                        changed_30 = False
                                        new_args_3 = Punctuated()
                                        for (element_12, separator_8) in element_1.generics.args.delimited:
                                            new_element_12 = proc(element_12)
                                            assert(is_rust_generic_argument(new_element_12))
                                            if new_element_12 is not element_12:
                                                changed_30 = True
                                            new_separator_8 = proc(separator_8)
                                            assert(isinstance(new_separator_8, RustComma))
                                            if new_separator_8 is not separator_8:
                                                changed_30 = True
                                            new_args_3.append(new_element_12, new_separator_8)
                                        new_last_9 = proc(element_1.generics.args.last)
                                        assert(is_rust_generic_argument(new_last_9))
                                        if new_last_9 is not element_1.generics.args.last:
                                            changed_30 = True
                                        new_args_3.append_final(new_last_9)
                                        if changed_30:
                                            new_generics = RustAngleBracketedGenericArguments(less_than=element_1.generics.less_than, args=new_args_3, greater_than=element_1.generics.greater_than)
                                            changed_29 = True
                                        else:
                                            new_generics = element_1.generics
                                    elif element_1.generics is None:
                                        new_generics = element_1.generics
                                    else:
                                        assert_never(element_1.generics)
                                    new_type_expr_3 = proc(element_1.type_expr)
                                    assert(is_rust_type_expr(new_type_expr_3))
                                    if new_type_expr_3 is not element_1.type_expr:
                                        changed_29 = True
                                    if changed_29:
                                        new_element_1 = RustAssocType(name=element_1.name, generics=new_generics, equals=element_1.equals, type_expr=new_type_expr_3)
                                        changed_6 = True
                                    else:
                                        new_element_1 = element_1
                                elif isinstance(element_1, RustAssocConst):
                                    changed_31 = False
                                    if isinstance(element_1.generics, RustAngleBracketedGenericArguments):
                                        new_generics_1 = proc(element_1.generics)
                                        assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                        if new_generics_1 is not element_1.generics:
                                            changed_31 = True
                                    elif element_1.generics is None:
                                        new_generics_1 = element_1.generics
                                    else:
                                        assert_never(element_1.generics)
                                    new_expr_3 = proc(element_1.expr)
                                    assert(is_rust_expr(new_expr_3))
                                    if new_expr_3 is not element_1.expr:
                                        changed_31 = True
                                    if changed_31:
                                        new_element_1 = RustAssocConst(name=element_1.name, generics=new_generics_1, equals=element_1.equals, expr=new_expr_3)
                                        changed_6 = True
                                    else:
                                        new_element_1 = element_1
                                elif isinstance(element_1, RustConstraint):
                                    changed_32 = False
                                    new_generics_2 = proc(element_1.generics)
                                    assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                                    if new_generics_2 is not element_1.generics:
                                        changed_32 = True
                                    new_bounds = Punctuated()
                                    for (element_13, separator_9) in element_1.bounds.delimited:
                                        if isinstance(element_13, RustTraitBound):
                                            changed_33 = False
                                            if isinstance(element_13.bound_lifetimes, RustBoundLifetimes):
                                                changed_34 = False
                                                new_lifetimes = Punctuated()
                                                for (element_14, separator_10) in element_13.bound_lifetimes.lifetimes.delimited:
                                                    new_element_14 = proc(element_14)
                                                    assert(is_rust_generic_param(new_element_14))
                                                    if new_element_14 is not element_14:
                                                        changed_34 = True
                                                    new_separator_10 = proc(separator_10)
                                                    assert(isinstance(new_separator_10, RustComma))
                                                    if new_separator_10 is not separator_10:
                                                        changed_34 = True
                                                    new_lifetimes.append(new_element_14, new_separator_10)
                                                new_last_11 = proc(element_13.bound_lifetimes.lifetimes.last)
                                                assert(is_rust_generic_param(new_last_11))
                                                if new_last_11 is not element_13.bound_lifetimes.lifetimes.last:
                                                    changed_34 = True
                                                new_lifetimes.append_final(new_last_11)
                                                if changed_34:
                                                    new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_13.bound_lifetimes.for_keyword, less_than=element_13.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_13.bound_lifetimes.greater_than)
                                                    changed_33 = True
                                                else:
                                                    new_bound_lifetimes = element_13.bound_lifetimes
                                            elif element_13.bound_lifetimes is None:
                                                new_bound_lifetimes = element_13.bound_lifetimes
                                            else:
                                                assert_never(element_13.bound_lifetimes)
                                            new_path_8 = proc(element_13.path)
                                            assert(isinstance(new_path_8, RustPath))
                                            if new_path_8 is not element_13.path:
                                                changed_33 = True
                                            if changed_33:
                                                new_element_13 = RustTraitBound(modifier=element_13.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_8)
                                                changed_32 = True
                                            else:
                                                new_element_13 = element_13
                                        elif isinstance(element_13, RustLifetime):
                                            new_element_13 = proc(element_13)
                                            assert(isinstance(new_element_13, RustLifetime))
                                            if new_element_13 is not element_13:
                                                changed_32 = True
                                        else:
                                            assert_never(element_13)
                                        new_separator_9 = separator_9
                                        new_bounds.append(new_element_13, new_separator_9)
                                    new_last_10 = proc(element_1.bounds.last)
                                    assert(is_rust_type_param_bound(new_last_10))
                                    if new_last_10 is not element_1.bounds.last:
                                        changed_32 = True
                                    new_bounds.append_final(new_last_10)
                                    if changed_32:
                                        new_element_1 = RustConstraint(name=element_1.name, generics=new_generics_2, colon=element_1.colon, bounds=new_bounds)
                                        changed_6 = True
                                    else:
                                        new_element_1 = element_1
                                else:
                                    assert_never(element_1)
                                new_separator_1 = proc(separator_1)
                                assert(isinstance(new_separator_1, RustComma))
                                if new_separator_1 is not separator_1:
                                    changed_6 = True
                                new_args_1.append(new_element_1, new_separator_1)
                            new_last_1 = proc(element.args.args.last)
                            assert(is_rust_generic_argument(new_last_1))
                            if new_last_1 is not element.args.args.last:
                                changed_6 = True
                            new_args_1.append_final(new_last_1)
                            if changed_6:
                                new_args = RustTurbofish(colon_colon=element.args.colon_colon, less_than=element.args.less_than, args=new_args_1, greater_than=element.args.greater_than)
                                changed_5 = True
                            else:
                                new_args = element.args
                        elif isinstance(element.args, RustAngleBracketedGenericArguments):
                            new_args = proc(element.args)
                            assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                            if new_args is not element.args:
                                changed_5 = True
                        elif isinstance(element.args, RustParenthesizedGenericArguments):
                            changed_35 = False
                            new_params = Punctuated()
                            for (element_15, separator_11) in element.args.params.delimited:
                                new_element_15 = proc(element_15)
                                assert(is_rust_type_expr(new_element_15))
                                if new_element_15 is not element_15:
                                    changed_35 = True
                                new_separator_11 = proc(separator_11)
                                assert(isinstance(new_separator_11, RustComma))
                                if new_separator_11 is not separator_11:
                                    changed_35 = True
                                new_params.append(new_element_15, new_separator_11)
                            new_last_12 = proc(element.args.params.last)
                            assert(is_rust_type_expr(new_last_12))
                            if new_last_12 is not element.args.params.last:
                                changed_35 = True
                            new_params.append_final(new_last_12)
                            new_result = proc(element.args.result)
                            assert(is_rust_type_expr(new_result))
                            if new_result is not element.args.result:
                                changed_35 = True
                            if changed_35:
                                new_args = RustParenthesizedGenericArguments(open_paren=element.args.open_paren, params=new_params, close_paren=element.args.close_paren, r_arrow=element.args.r_arrow, result=new_result)
                                changed_5 = True
                            else:
                                new_args = element.args
                        else:
                            assert_never(element.args)
                    elif element.args is None:
                        new_args = element.args
                    else:
                        assert_never(element.args)
                    if changed_5:
                        new_element = RustPathSegment(name=element.name, args=new_args)
                        changed_4 = True
                    else:
                        new_element = element
                    new_separator = separator
                    new_segments.append(new_element, new_separator)
                new_last = proc(node.type_expr.qself.path.segments.last)
                assert(isinstance(new_last, RustPathSegment))
                if new_last is not node.type_expr.qself.path.segments.last:
                    changed_4 = True
                new_segments.append_final(new_last)
                if changed_4:
                    new_path = RustPath(leading_colon_colon=node.type_expr.qself.path.leading_colon_colon, segments=new_segments)
                    changed_3 = True
                else:
                    new_path = node.type_expr.qself.path
                if changed_3:
                    new_qself = RustQself(less_than=node.type_expr.qself.less_than, type_expr=new_type_expr_1, as_keyword=node.type_expr.qself.as_keyword, path=new_path, greater_than=node.type_expr.qself.greater_than)
                    changed_2 = True
                else:
                    new_qself = node.type_expr.qself
            elif node.type_expr.qself is None:
                new_qself = node.type_expr.qself
            else:
                assert_never(node.type_expr.qself)
            new_path_9 = proc(node.type_expr.path)
            assert(isinstance(new_path_9, RustPath))
            if new_path_9 is not node.type_expr.path:
                changed_2 = True
            if changed_2:
                new_type_expr = RustPathTypeExpr(qself=new_qself, path=new_path_9)
                changed_1 = True
            else:
                new_type_expr = node.type_expr
        elif isinstance(node.type_expr, RustArrayTypeExpr):
            changed_36 = False
            new_type_expr_4 = proc(node.type_expr.type_expr)
            assert(is_rust_type_expr(new_type_expr_4))
            if new_type_expr_4 is not node.type_expr.type_expr:
                changed_36 = True
            new_expr_4 = proc(node.type_expr.expr)
            assert(is_rust_expr(new_expr_4))
            if new_expr_4 is not node.type_expr.expr:
                changed_36 = True
            if changed_36:
                new_type_expr = RustArrayTypeExpr(open_bracket=node.type_expr.open_bracket, type_expr=new_type_expr_4, semicolon=node.type_expr.semicolon, expr=new_expr_4, close_bracket=node.type_expr.close_bracket)
                changed_1 = True
            else:
                new_type_expr = node.type_expr
        elif isinstance(node.type_expr, RustNeverTypeExpr):
            new_type_expr = node.type_expr
        elif isinstance(node.type_expr, RustTupleTypeExpr):
            changed_38 = False
            new_elements_5 = Punctuated()
            for (element_16, separator_12) in node.type_expr.elements.delimited:
                new_element_16 = proc(element_16)
                assert(is_rust_type_expr(new_element_16))
                if new_element_16 is not element_16:
                    changed_38 = True
                new_separator_12 = proc(separator_12)
                assert(isinstance(new_separator_12, RustComma))
                if new_separator_12 is not separator_12:
                    changed_38 = True
                new_elements_5.append(new_element_16, new_separator_12)
            new_last_13 = proc(node.type_expr.elements.last)
            assert(is_rust_type_expr(new_last_13))
            if new_last_13 is not node.type_expr.elements.last:
                changed_38 = True
            new_elements_5.append_final(new_last_13)
            if changed_38:
                new_type_expr = RustTupleTypeExpr(open_paren=node.type_expr.open_paren, elements=new_elements_5, close_paren=node.type_expr.close_paren)
                changed_1 = True
            else:
                new_type_expr = node.type_expr
        else:
            assert_never(node.type_expr)
        if isinstance(node.default, RustInit):
            new_default = proc(node.default)
            assert(isinstance(new_default, RustInit))
            if new_default is not node.default:
                changed_1 = True
        elif node.default is None:
            new_default = node.default
        else:
            assert_never(node.default)
        if changed_1:
            rewritten = RustConstParam(const_keyword=node.const_keyword, name=node.name, colon=node.colon, type_expr=new_type_expr, default=new_default)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustLifetime):
        rewritten = node
    elif isinstance(node, RustTypeParam):
        changed_40 = False
        new_type_param_bound = proc(node.type_param_bound)
        assert(is_rust_type_param_bound(new_type_param_bound))
        if new_type_param_bound is not node.type_param_bound:
            changed_40 = True
        if isinstance(node.default, RustTypeInit):
            changed_41 = False
            new_type_expr_5 = proc(node.default.type_expr)
            assert(is_rust_type_expr(new_type_expr_5))
            if new_type_expr_5 is not node.default.type_expr:
                changed_41 = True
            if changed_41:
                new_default_1 = RustTypeInit(equals=node.default.equals, type_expr=new_type_expr_5)
                changed_40 = True
            else:
                new_default_1 = node.default
        elif node.default is None:
            new_default_1 = node.default
        else:
            assert_never(node.default)
        if changed_40:
            rewritten = RustTypeParam(name=node.name, colon=node.colon, type_param_bound=new_type_param_bound, percent=node.percent, plus=node.plus, default=new_default_1)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_item(node: RustItem, proc: Callable[[RustItem], RustItem]) -> RustItem:
    if isinstance(node, RustEnumItem):
        changed_1 = False
        new_attrs = []
        for element in node.attrs:
            changed_2 = False
            if isinstance(element.meta, RustMetaPath):
                changed_3 = False
                changed_4 = False
                new_segments = Punctuated()
                for (element_1, separator) in element.meta.path.segments.delimited:
                    changed_5 = False
                    if is_rust_path_arguments(element_1.args):
                        if isinstance(element_1.args, RustTurbofish):
                            changed_6 = False
                            new_args_1 = Punctuated()
                            for (element_2, separator_1) in element_1.args.args.delimited:
                                if isinstance(element_2, RustLifetime):
                                    new_element_2 = element_2
                                elif is_rust_type_expr(element_2):
                                    if isinstance(element_2, RustPathTypeExpr):
                                        changed_8 = False
                                        if isinstance(element_2.qself, RustQself):
                                            changed_9 = False
                                            new_type_expr = proc(element_2.qself.type_expr)
                                            assert(is_rust_type_expr(new_type_expr))
                                            if new_type_expr is not element_2.qself.type_expr:
                                                changed_9 = True
                                            new_path_1 = proc(element_2.qself.path)
                                            assert(isinstance(new_path_1, RustPath))
                                            if new_path_1 is not element_2.qself.path:
                                                changed_9 = True
                                            if changed_9:
                                                new_qself = RustQself(less_than=element_2.qself.less_than, type_expr=new_type_expr, as_keyword=element_2.qself.as_keyword, path=new_path_1, greater_than=element_2.qself.greater_than)
                                                changed_8 = True
                                            else:
                                                new_qself = element_2.qself
                                        elif element_2.qself is None:
                                            new_qself = element_2.qself
                                        else:
                                            assert_never(element_2.qself)
                                        new_path_2 = proc(element_2.path)
                                        assert(isinstance(new_path_2, RustPath))
                                        if new_path_2 is not element_2.path:
                                            changed_8 = True
                                        if changed_8:
                                            new_element_2 = RustPathTypeExpr(qself=new_qself, path=new_path_2)
                                            changed_6 = True
                                        else:
                                            new_element_2 = element_2
                                    elif isinstance(element_2, RustArrayTypeExpr):
                                        changed_10 = False
                                        new_type_expr_1 = proc(element_2.type_expr)
                                        assert(is_rust_type_expr(new_type_expr_1))
                                        if new_type_expr_1 is not element_2.type_expr:
                                            changed_10 = True
                                        if isinstance(element_2.expr, RustLitExpr):
                                            new_expr = element_2.expr
                                        elif isinstance(element_2.expr, RustPathExpr):
                                            changed_12 = False
                                            new_attrs_1 = []
                                            for element_3 in element_2.expr.attrs:
                                                new_element_3 = proc(element_3)
                                                assert(isinstance(new_element_3, RustAttr))
                                                if new_element_3 is not element_3:
                                                    changed_12 = True
                                                new_elements_1.append(new_element_3)
                                            if isinstance(element_2.expr.qself, RustQself):
                                                new_qself_1 = proc(element_2.expr.qself)
                                                assert(isinstance(new_qself_1, RustQself))
                                                if new_qself_1 is not element_2.expr.qself:
                                                    changed_12 = True
                                            elif element_2.expr.qself is None:
                                                new_qself_1 = element_2.expr.qself
                                            else:
                                                assert_never(element_2.expr.qself)
                                            new_path_3 = proc(element_2.expr.path)
                                            assert(isinstance(new_path_3, RustPath))
                                            if new_path_3 is not element_2.expr.path:
                                                changed_12 = True
                                            if changed_12:
                                                new_expr = RustPathExpr(attrs=new_attrs_1, qself=new_qself_1, path=new_path_3)
                                                changed_10 = True
                                            else:
                                                new_expr = element_2.expr
                                        elif isinstance(element_2.expr, RustCallExpr):
                                            changed_13 = False
                                            new_operator = proc(element_2.expr.operator)
                                            assert(is_rust_expr(new_operator))
                                            if new_operator is not element_2.expr.operator:
                                                changed_13 = True
                                            new_args_2 = Punctuated()
                                            for (element_4, separator_2) in element_2.expr.args.delimited:
                                                new_element_4 = proc(element_4)
                                                assert(is_rust_expr(new_element_4))
                                                if new_element_4 is not element_4:
                                                    changed_13 = True
                                                new_separator_2 = separator_2
                                                new_args_2.append(new_element_4, new_separator_2)
                                            new_last_2 = proc(element_2.expr.args.last)
                                            assert(is_rust_expr(new_last_2))
                                            if new_last_2 is not element_2.expr.args.last:
                                                changed_13 = True
                                            new_args_2.append_final(new_last_2)
                                            if changed_13:
                                                new_expr = RustCallExpr(operator=new_operator, open_paren=element_2.expr.open_paren, args=new_args_2, close_paren=element_2.expr.close_paren)
                                                changed_10 = True
                                            else:
                                                new_expr = element_2.expr
                                        elif isinstance(element_2.expr, RustStructExpr):
                                            changed_14 = False
                                            new_path_4 = proc(element_2.expr.path)
                                            assert(isinstance(new_path_4, RustPath))
                                            if new_path_4 is not element_2.expr.path:
                                                changed_14 = True
                                            new_inits = Punctuated()
                                            for (element_5, separator_3) in element_2.expr.inits.delimited:
                                                changed_15 = False
                                                new_value = proc(element_5.value)
                                                assert(is_rust_expr(new_value))
                                                if new_value is not element_5.value:
                                                    changed_15 = True
                                                if changed_15:
                                                    new_element_5 = RustInit(name=element_5.name, equals=element_5.equals, value=new_value)
                                                    changed_14 = True
                                                else:
                                                    new_element_5 = element_5
                                                new_separator_3 = proc(separator_3)
                                                assert(isinstance(new_separator_3, RustComma))
                                                if new_separator_3 is not separator_3:
                                                    changed_14 = True
                                                new_inits.append(new_element_5, new_separator_3)
                                            new_last_3 = proc(element_2.expr.inits.last)
                                            assert(isinstance(new_last_3, RustInit))
                                            if new_last_3 is not element_2.expr.inits.last:
                                                changed_14 = True
                                            new_inits.append_final(new_last_3)
                                            if changed_14:
                                                new_expr = RustStructExpr(path=new_path_4, open_brace=element_2.expr.open_brace, inits=new_inits, comma=element_2.expr.comma, close_brace=element_2.expr.close_brace)
                                                changed_10 = True
                                            else:
                                                new_expr = element_2.expr
                                        elif isinstance(element_2.expr, RustBlockExpr):
                                            changed_16 = False
                                            new_item = proc(element_2.expr.item)
                                            assert(is_rust_item(new_item))
                                            if new_item is not element_2.expr.item:
                                                changed_16 = True
                                            new_last_4 = proc(element_2.expr.last)
                                            assert(is_rust_expr(new_last_4))
                                            if new_last_4 is not element_2.expr.last:
                                                changed_16 = True
                                            if changed_16:
                                                new_expr = RustBlockExpr(open_brace=element_2.expr.open_brace, item=new_item, semicolon=element_2.expr.semicolon, last=new_last_4, close_brace=element_2.expr.close_brace)
                                                changed_10 = True
                                            else:
                                                new_expr = element_2.expr
                                        elif isinstance(element_2.expr, RustRetExpr):
                                            changed_17 = False
                                            new_expr_1 = proc(element_2.expr.expr)
                                            assert(is_rust_expr(new_expr_1))
                                            if new_expr_1 is not element_2.expr.expr:
                                                changed_17 = True
                                            if changed_17:
                                                new_expr = RustRetExpr(return_keyword=element_2.expr.return_keyword, expr=new_expr_1)
                                                changed_10 = True
                                            else:
                                                new_expr = element_2.expr
                                        else:
                                            assert_never(element_2.expr)
                                        if changed_10:
                                            new_element_2 = RustArrayTypeExpr(open_bracket=element_2.open_bracket, type_expr=new_type_expr_1, semicolon=element_2.semicolon, expr=new_expr, close_bracket=element_2.close_bracket)
                                            changed_6 = True
                                        else:
                                            new_element_2 = element_2
                                    elif isinstance(element_2, RustNeverTypeExpr):
                                        new_element_2 = element_2
                                    elif isinstance(element_2, RustTupleTypeExpr):
                                        changed_19 = False
                                        new_elements_2 = Punctuated()
                                        for (element_6, separator_4) in element_2.elements.delimited:
                                            new_element_6 = proc(element_6)
                                            assert(is_rust_type_expr(new_element_6))
                                            if new_element_6 is not element_6:
                                                changed_19 = True
                                            new_separator_4 = proc(separator_4)
                                            assert(isinstance(new_separator_4, RustComma))
                                            if new_separator_4 is not separator_4:
                                                changed_19 = True
                                            new_elements_2.append(new_element_6, new_separator_4)
                                        new_last_5 = proc(element_2.elements.last)
                                        assert(is_rust_type_expr(new_last_5))
                                        if new_last_5 is not element_2.elements.last:
                                            changed_19 = True
                                        new_elements_2.append_final(new_last_5)
                                        if changed_19:
                                            new_element_2 = RustTupleTypeExpr(open_paren=element_2.open_paren, elements=new_elements_2, close_paren=element_2.close_paren)
                                            changed_6 = True
                                        else:
                                            new_element_2 = element_2
                                    else:
                                        assert_never(element_2)
                                elif is_rust_expr(element_2):
                                    new_element_2 = proc(element_2)
                                    assert(is_rust_expr(new_element_2))
                                    if new_element_2 is not element_2:
                                        changed_6 = True
                                elif isinstance(element_2, RustAssocType):
                                    changed_20 = False
                                    if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                        changed_21 = False
                                        new_args_3 = Punctuated()
                                        for (element_7, separator_5) in element_2.generics.args.delimited:
                                            new_element_7 = proc(element_7)
                                            assert(is_rust_generic_argument(new_element_7))
                                            if new_element_7 is not element_7:
                                                changed_21 = True
                                            new_separator_5 = proc(separator_5)
                                            assert(isinstance(new_separator_5, RustComma))
                                            if new_separator_5 is not separator_5:
                                                changed_21 = True
                                            new_args_3.append(new_element_7, new_separator_5)
                                        new_last_6 = proc(element_2.generics.args.last)
                                        assert(is_rust_generic_argument(new_last_6))
                                        if new_last_6 is not element_2.generics.args.last:
                                            changed_21 = True
                                        new_args_3.append_final(new_last_6)
                                        if changed_21:
                                            new_generics = RustAngleBracketedGenericArguments(less_than=element_2.generics.less_than, args=new_args_3, greater_than=element_2.generics.greater_than)
                                            changed_20 = True
                                        else:
                                            new_generics = element_2.generics
                                    elif element_2.generics is None:
                                        new_generics = element_2.generics
                                    else:
                                        assert_never(element_2.generics)
                                    new_type_expr_2 = proc(element_2.type_expr)
                                    assert(is_rust_type_expr(new_type_expr_2))
                                    if new_type_expr_2 is not element_2.type_expr:
                                        changed_20 = True
                                    if changed_20:
                                        new_element_2 = RustAssocType(name=element_2.name, generics=new_generics, equals=element_2.equals, type_expr=new_type_expr_2)
                                        changed_6 = True
                                    else:
                                        new_element_2 = element_2
                                elif isinstance(element_2, RustAssocConst):
                                    changed_22 = False
                                    if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                        new_generics_1 = proc(element_2.generics)
                                        assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                        if new_generics_1 is not element_2.generics:
                                            changed_22 = True
                                    elif element_2.generics is None:
                                        new_generics_1 = element_2.generics
                                    else:
                                        assert_never(element_2.generics)
                                    new_expr_2 = proc(element_2.expr)
                                    assert(is_rust_expr(new_expr_2))
                                    if new_expr_2 is not element_2.expr:
                                        changed_22 = True
                                    if changed_22:
                                        new_element_2 = RustAssocConst(name=element_2.name, generics=new_generics_1, equals=element_2.equals, expr=new_expr_2)
                                        changed_6 = True
                                    else:
                                        new_element_2 = element_2
                                elif isinstance(element_2, RustConstraint):
                                    changed_23 = False
                                    new_generics_2 = proc(element_2.generics)
                                    assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                                    if new_generics_2 is not element_2.generics:
                                        changed_23 = True
                                    new_bounds = Punctuated()
                                    for (element_8, separator_6) in element_2.bounds.delimited:
                                        if isinstance(element_8, RustTraitBound):
                                            changed_24 = False
                                            if isinstance(element_8.bound_lifetimes, RustBoundLifetimes):
                                                changed_25 = False
                                                new_lifetimes = Punctuated()
                                                for (element_9, separator_7) in element_8.bound_lifetimes.lifetimes.delimited:
                                                    if isinstance(element_9, RustLifetime):
                                                        new_element_9 = proc(element_9)
                                                        assert(isinstance(new_element_9, RustLifetime))
                                                        if new_element_9 is not element_9:
                                                            changed_25 = True
                                                    elif isinstance(element_9, RustTypeParam):
                                                        changed_26 = False
                                                        new_type_param_bound = proc(element_9.type_param_bound)
                                                        assert(is_rust_type_param_bound(new_type_param_bound))
                                                        if new_type_param_bound is not element_9.type_param_bound:
                                                            changed_26 = True
                                                        if isinstance(element_9.default, RustTypeInit):
                                                            changed_27 = False
                                                            new_type_expr_3 = proc(element_9.default.type_expr)
                                                            assert(is_rust_type_expr(new_type_expr_3))
                                                            if new_type_expr_3 is not element_9.default.type_expr:
                                                                changed_27 = True
                                                            if changed_27:
                                                                new_default = RustTypeInit(equals=element_9.default.equals, type_expr=new_type_expr_3)
                                                                changed_26 = True
                                                            else:
                                                                new_default = element_9.default
                                                        elif element_9.default is None:
                                                            new_default = element_9.default
                                                        else:
                                                            assert_never(element_9.default)
                                                        if changed_26:
                                                            new_element_9 = RustTypeParam(name=element_9.name, colon=element_9.colon, type_param_bound=new_type_param_bound, percent=element_9.percent, plus=element_9.plus, default=new_default)
                                                            changed_25 = True
                                                        else:
                                                            new_element_9 = element_9
                                                    elif isinstance(element_9, RustConstParam):
                                                        changed_28 = False
                                                        new_type_expr_4 = proc(element_9.type_expr)
                                                        assert(is_rust_type_expr(new_type_expr_4))
                                                        if new_type_expr_4 is not element_9.type_expr:
                                                            changed_28 = True
                                                        if isinstance(element_9.default, RustInit):
                                                            new_default_1 = proc(element_9.default)
                                                            assert(isinstance(new_default_1, RustInit))
                                                            if new_default_1 is not element_9.default:
                                                                changed_28 = True
                                                        elif element_9.default is None:
                                                            new_default_1 = element_9.default
                                                        else:
                                                            assert_never(element_9.default)
                                                        if changed_28:
                                                            new_element_9 = RustConstParam(const_keyword=element_9.const_keyword, name=element_9.name, colon=element_9.colon, type_expr=new_type_expr_4, default=new_default_1)
                                                            changed_25 = True
                                                        else:
                                                            new_element_9 = element_9
                                                    else:
                                                        assert_never(element_9)
                                                    new_separator_7 = proc(separator_7)
                                                    assert(isinstance(new_separator_7, RustComma))
                                                    if new_separator_7 is not separator_7:
                                                        changed_25 = True
                                                    new_lifetimes.append(new_element_9, new_separator_7)
                                                new_last_8 = proc(element_8.bound_lifetimes.lifetimes.last)
                                                assert(is_rust_generic_param(new_last_8))
                                                if new_last_8 is not element_8.bound_lifetimes.lifetimes.last:
                                                    changed_25 = True
                                                new_lifetimes.append_final(new_last_8)
                                                if changed_25:
                                                    new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_8.bound_lifetimes.for_keyword, less_than=element_8.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_8.bound_lifetimes.greater_than)
                                                    changed_24 = True
                                                else:
                                                    new_bound_lifetimes = element_8.bound_lifetimes
                                            elif element_8.bound_lifetimes is None:
                                                new_bound_lifetimes = element_8.bound_lifetimes
                                            else:
                                                assert_never(element_8.bound_lifetimes)
                                            new_path_5 = proc(element_8.path)
                                            assert(isinstance(new_path_5, RustPath))
                                            if new_path_5 is not element_8.path:
                                                changed_24 = True
                                            if changed_24:
                                                new_element_8 = RustTraitBound(modifier=element_8.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_5)
                                                changed_23 = True
                                            else:
                                                new_element_8 = element_8
                                        elif isinstance(element_8, RustLifetime):
                                            new_element_8 = proc(element_8)
                                            assert(isinstance(new_element_8, RustLifetime))
                                            if new_element_8 is not element_8:
                                                changed_23 = True
                                        else:
                                            assert_never(element_8)
                                        new_separator_6 = separator_6
                                        new_bounds.append(new_element_8, new_separator_6)
                                    new_last_7 = proc(element_2.bounds.last)
                                    assert(is_rust_type_param_bound(new_last_7))
                                    if new_last_7 is not element_2.bounds.last:
                                        changed_23 = True
                                    new_bounds.append_final(new_last_7)
                                    if changed_23:
                                        new_element_2 = RustConstraint(name=element_2.name, generics=new_generics_2, colon=element_2.colon, bounds=new_bounds)
                                        changed_6 = True
                                    else:
                                        new_element_2 = element_2
                                else:
                                    assert_never(element_2)
                                new_separator_1 = proc(separator_1)
                                assert(isinstance(new_separator_1, RustComma))
                                if new_separator_1 is not separator_1:
                                    changed_6 = True
                                new_args_1.append(new_element_2, new_separator_1)
                            new_last_1 = proc(element_1.args.args.last)
                            assert(is_rust_generic_argument(new_last_1))
                            if new_last_1 is not element_1.args.args.last:
                                changed_6 = True
                            new_args_1.append_final(new_last_1)
                            if changed_6:
                                new_args = RustTurbofish(colon_colon=element_1.args.colon_colon, less_than=element_1.args.less_than, args=new_args_1, greater_than=element_1.args.greater_than)
                                changed_5 = True
                            else:
                                new_args = element_1.args
                        elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                            new_args = proc(element_1.args)
                            assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                            if new_args is not element_1.args:
                                changed_5 = True
                        elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                            changed_29 = False
                            new_params = Punctuated()
                            for (element_10, separator_8) in element_1.args.params.delimited:
                                new_element_10 = proc(element_10)
                                assert(is_rust_type_expr(new_element_10))
                                if new_element_10 is not element_10:
                                    changed_29 = True
                                new_separator_8 = proc(separator_8)
                                assert(isinstance(new_separator_8, RustComma))
                                if new_separator_8 is not separator_8:
                                    changed_29 = True
                                new_params.append(new_element_10, new_separator_8)
                            new_last_9 = proc(element_1.args.params.last)
                            assert(is_rust_type_expr(new_last_9))
                            if new_last_9 is not element_1.args.params.last:
                                changed_29 = True
                            new_params.append_final(new_last_9)
                            new_result = proc(element_1.args.result)
                            assert(is_rust_type_expr(new_result))
                            if new_result is not element_1.args.result:
                                changed_29 = True
                            if changed_29:
                                new_args = RustParenthesizedGenericArguments(open_paren=element_1.args.open_paren, params=new_params, close_paren=element_1.args.close_paren, r_arrow=element_1.args.r_arrow, result=new_result)
                                changed_5 = True
                            else:
                                new_args = element_1.args
                        else:
                            assert_never(element_1.args)
                    elif element_1.args is None:
                        new_args = element_1.args
                    else:
                        assert_never(element_1.args)
                    if changed_5:
                        new_element_1 = RustPathSegment(name=element_1.name, args=new_args)
                        changed_4 = True
                    else:
                        new_element_1 = element_1
                    new_separator = separator
                    new_segments.append(new_element_1, new_separator)
                new_last = proc(element.meta.path.segments.last)
                assert(isinstance(new_last, RustPathSegment))
                if new_last is not element.meta.path.segments.last:
                    changed_4 = True
                new_segments.append_final(new_last)
                if changed_4:
                    new_path = RustPath(leading_colon_colon=element.meta.path.leading_colon_colon, segments=new_segments)
                    changed_3 = True
                else:
                    new_path = element.meta.path
                if changed_3:
                    new_meta = RustMetaPath(path=new_path)
                    changed_2 = True
                else:
                    new_meta = element.meta
            elif isinstance(element.meta, RustMetaParenthesized):
                changed_30 = False
                new_path_6 = proc(element.meta.path)
                assert(isinstance(new_path_6, RustPath))
                if new_path_6 is not element.meta.path:
                    changed_30 = True
                if changed_30:
                    new_meta = RustMetaParenthesized(path=new_path_6, open_paren=element.meta.open_paren, tokens=element.meta.tokens, close_paren=element.meta.close_paren)
                    changed_2 = True
                else:
                    new_meta = element.meta
            elif isinstance(element.meta, RustMetaBracketed):
                changed_31 = False
                new_path_7 = proc(element.meta.path)
                assert(isinstance(new_path_7, RustPath))
                if new_path_7 is not element.meta.path:
                    changed_31 = True
                if changed_31:
                    new_meta = RustMetaBracketed(path=new_path_7, open_bracket=element.meta.open_bracket, tokens=element.meta.tokens, close_bracket=element.meta.close_bracket)
                    changed_2 = True
                else:
                    new_meta = element.meta
            elif isinstance(element.meta, RustMetaBraced):
                changed_32 = False
                new_path_8 = proc(element.meta.path)
                assert(isinstance(new_path_8, RustPath))
                if new_path_8 is not element.meta.path:
                    changed_32 = True
                if changed_32:
                    new_meta = RustMetaBraced(path=new_path_8, open_brace=element.meta.open_brace, tokens=element.meta.tokens, close_brace=element.meta.close_brace)
                    changed_2 = True
                else:
                    new_meta = element.meta
            elif isinstance(element.meta, RustMetaNameValue):
                changed_33 = False
                new_path_9 = proc(element.meta.path)
                assert(isinstance(new_path_9, RustPath))
                if new_path_9 is not element.meta.path:
                    changed_33 = True
                new_expr_3 = proc(element.meta.expr)
                assert(is_rust_expr(new_expr_3))
                if new_expr_3 is not element.meta.expr:
                    changed_33 = True
                if changed_33:
                    new_meta = RustMetaNameValue(path=new_path_9, equals=element.meta.equals, expr=new_expr_3)
                    changed_2 = True
                else:
                    new_meta = element.meta
            else:
                assert_never(element.meta)
            if changed_2:
                new_element = RustAttr(hashtag=element.hashtag, exclamation_mark=element.exclamation_mark, open_bracket=element.open_bracket, meta=new_meta, close_bracket=element.close_bracket)
                changed_1 = True
            else:
                new_element = element
            new_elements.append(new_element)
        if isinstance(node.visibility, RustPublic):
            changed_34 = False
            if isinstance(node.visibility.restrict, tuple):
                new_elements_3 = []
                element_0 = node.visibility.restrict[0]
                new_element_0 = element_0
                new_elements_3.append(new_element_0)
                element_1 = node.visibility.restrict[1]
                if isinstance(element_1, RustInKeyword):
                    new_element_1 = element_1
                elif element_1 is None:
                    new_element_1 = element_1
                else:
                    assert_never(element_1)
                new_elements_3.append(new_element_1)
                element_2 = node.visibility.restrict[2]
                new_element_2 = proc(element_2)
                assert(isinstance(new_element_2, RustPath))
                if new_element_2 is not element_2:
                    changed_34 = True
                new_elements_3.append(new_element_2)
                element_3 = node.visibility.restrict[3]
                new_element_3 = element_3
                new_elements_3.append(new_element_3)
                new_restrict = tuple(new_elements_3) if changed_34 else node.visibility.restrict
            elif node.visibility.restrict is None:
                new_restrict = node.visibility.restrict
            else:
                assert_never(node.visibility.restrict)
            if changed_34:
                new_visibility = RustPublic(pub_keyword=node.visibility.pub_keyword, restrict=new_restrict)
                changed_1 = True
            else:
                new_visibility = node.visibility
        elif node.visibility is None:
            new_visibility = node.visibility
        else:
            assert_never(node.visibility)
        new_variants = Punctuated()
        for (element_11, separator_9) in node.variants.delimited:
            if isinstance(element_11, RustStructVariant):
                changed_35 = False
                new_fields = Punctuated()
                for (element_12, separator_10) in element_11.fields.delimited:
                    changed_36 = False
                    new_type_expr_5 = proc(element_12.type_expr)
                    assert(is_rust_type_expr(new_type_expr_5))
                    if new_type_expr_5 is not element_12.type_expr:
                        changed_36 = True
                    if changed_36:
                        new_element_12 = RustField(name=element_12.name, colon=element_12.colon, type_expr=new_type_expr_5)
                        changed_35 = True
                    else:
                        new_element_12 = element_12
                    new_separator_10 = proc(separator_10)
                    assert(isinstance(new_separator_10, RustComma))
                    if new_separator_10 is not separator_10:
                        changed_35 = True
                    new_fields.append(new_element_12, new_separator_10)
                new_last_11 = proc(element_11.fields.last)
                assert(isinstance(new_last_11, RustField))
                if new_last_11 is not element_11.fields.last:
                    changed_35 = True
                new_fields.append_final(new_last_11)
                if changed_35:
                    new_element_11 = RustStructVariant(name=element_11.name, open_brace=element_11.open_brace, fields=new_fields, comma=element_11.comma, close_brace=element_11.close_brace)
                    changed_1 = True
                else:
                    new_element_11 = element_11
            elif isinstance(element_11, RustTupleVariant):
                changed_37 = False
                new_types = Punctuated()
                for (element_13, separator_11) in element_11.types.delimited:
                    new_element_13 = proc(element_13)
                    assert(is_rust_type_expr(new_element_13))
                    if new_element_13 is not element_13:
                        changed_37 = True
                    new_separator_11 = proc(separator_11)
                    assert(isinstance(new_separator_11, RustComma))
                    if new_separator_11 is not separator_11:
                        changed_37 = True
                    new_types.append(new_element_13, new_separator_11)
                new_last_12 = proc(element_11.types.last)
                assert(is_rust_type_expr(new_last_12))
                if new_last_12 is not element_11.types.last:
                    changed_37 = True
                new_types.append_final(new_last_12)
                if changed_37:
                    new_element_11 = RustTupleVariant(name=element_11.name, open_paren=element_11.open_paren, types=new_types, close_paren=element_11.close_paren)
                    changed_1 = True
                else:
                    new_element_11 = element_11
            elif isinstance(element_11, RustEmptyVariant):
                changed_38 = False
                if isinstance(element_11.init, RustInit):
                    new_init = proc(element_11.init)
                    assert(isinstance(new_init, RustInit))
                    if new_init is not element_11.init:
                        changed_38 = True
                elif element_11.init is None:
                    new_init = element_11.init
                else:
                    assert_never(element_11.init)
                if changed_38:
                    new_element_11 = RustEmptyVariant(name=element_11.name, init=new_init)
                    changed_1 = True
                else:
                    new_element_11 = element_11
            else:
                assert_never(element_11)
            new_separator_9 = proc(separator_9)
            assert(isinstance(new_separator_9, RustComma))
            if new_separator_9 is not separator_9:
                changed_1 = True
            new_variants.append(new_element_11, new_separator_9)
        new_last_10 = proc(node.variants.last)
        assert(is_rust_variant(new_last_10))
        if new_last_10 is not node.variants.last:
            changed_1 = True
        new_variants.append_final(new_last_10)
        if changed_1:
            rewritten = RustEnumItem(attrs=new_attrs, visibility=new_visibility, enum_keyword=node.enum_keyword, name=node.name, open_brace=node.open_brace, variants=new_variants, comma=node.comma, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustExprItem):
        changed_39 = False
        new_expr_4 = proc(node.expr)
        assert(is_rust_expr(new_expr_4))
        if new_expr_4 is not node.expr:
            changed_39 = True
        if changed_39:
            rewritten = RustExprItem(expr=new_expr_4)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustStructItem):
        changed_40 = False
        new_attrs_2 = []
        for element_14 in node.attrs:
            new_element_14 = proc(element_14)
            assert(isinstance(new_element_14, RustAttr))
            if new_element_14 is not element_14:
                changed_40 = True
            new_elements_4.append(new_element_14)
        if isinstance(node.visibility, RustPublic):
            new_visibility_1 = proc(node.visibility)
            assert(isinstance(new_visibility_1, RustPublic))
            if new_visibility_1 is not node.visibility:
                changed_40 = True
        elif node.visibility is None:
            new_visibility_1 = node.visibility
        else:
            assert_never(node.visibility)
        new_fields_1 = Punctuated()
        for (element_15, separator_12) in node.fields.delimited:
            new_element_15 = proc(element_15)
            assert(isinstance(new_element_15, RustField))
            if new_element_15 is not element_15:
                changed_40 = True
            new_separator_12 = proc(separator_12)
            assert(isinstance(new_separator_12, RustComma))
            if new_separator_12 is not separator_12:
                changed_40 = True
            new_fields_1.append(new_element_15, new_separator_12)
        new_last_13 = proc(node.fields.last)
        assert(isinstance(new_last_13, RustField))
        if new_last_13 is not node.fields.last:
            changed_40 = True
        new_fields_1.append_final(new_last_13)
        if changed_40:
            rewritten = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=node.struct_keyword, name=node.name, open_brace=node.open_brace, fields=new_fields_1, comma=node.comma, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustUseItem):
        changed_41 = False
        new_attrs_3 = []
        for element_16 in node.attrs:
            new_element_16 = proc(element_16)
            assert(isinstance(new_element_16, RustAttr))
            if new_element_16 is not element_16:
                changed_41 = True
            new_elements_5.append(new_element_16)
        if isinstance(node.visibility, RustPublic):
            new_visibility_2 = proc(node.visibility)
            assert(isinstance(new_visibility_2, RustPublic))
            if new_visibility_2 is not node.visibility:
                changed_41 = True
        elif node.visibility is None:
            new_visibility_2 = node.visibility
        else:
            assert_never(node.visibility)
        if changed_41:
            rewritten = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=node.use_keyword, colon_colon=node.colon_colon, path=node.path, semicolon=node.semicolon)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_meta(node: RustMeta, proc: Callable[[RustMeta], RustMeta]) -> RustMeta:
    if isinstance(node, RustMetaBraced):
        changed_1 = False
        changed_2 = False
        new_segments = Punctuated()
        for (element, separator) in node.path.segments.delimited:
            changed_3 = False
            if is_rust_path_arguments(element.args):
                if isinstance(element.args, RustTurbofish):
                    changed_4 = False
                    new_args_1 = Punctuated()
                    for (element_1, separator_1) in element.args.args.delimited:
                        if isinstance(element_1, RustLifetime):
                            new_element_1 = element_1
                        elif is_rust_type_expr(element_1):
                            if isinstance(element_1, RustPathTypeExpr):
                                changed_6 = False
                                if isinstance(element_1.qself, RustQself):
                                    changed_7 = False
                                    new_type_expr = proc(element_1.qself.type_expr)
                                    assert(is_rust_type_expr(new_type_expr))
                                    if new_type_expr is not element_1.qself.type_expr:
                                        changed_7 = True
                                    new_path_1 = proc(element_1.qself.path)
                                    assert(isinstance(new_path_1, RustPath))
                                    if new_path_1 is not element_1.qself.path:
                                        changed_7 = True
                                    if changed_7:
                                        new_qself = RustQself(less_than=element_1.qself.less_than, type_expr=new_type_expr, as_keyword=element_1.qself.as_keyword, path=new_path_1, greater_than=element_1.qself.greater_than)
                                        changed_6 = True
                                    else:
                                        new_qself = element_1.qself
                                elif element_1.qself is None:
                                    new_qself = element_1.qself
                                else:
                                    assert_never(element_1.qself)
                                new_path_2 = proc(element_1.path)
                                assert(isinstance(new_path_2, RustPath))
                                if new_path_2 is not element_1.path:
                                    changed_6 = True
                                if changed_6:
                                    new_element_1 = RustPathTypeExpr(qself=new_qself, path=new_path_2)
                                    changed_4 = True
                                else:
                                    new_element_1 = element_1
                            elif isinstance(element_1, RustArrayTypeExpr):
                                changed_8 = False
                                new_type_expr_1 = proc(element_1.type_expr)
                                assert(is_rust_type_expr(new_type_expr_1))
                                if new_type_expr_1 is not element_1.type_expr:
                                    changed_8 = True
                                if isinstance(element_1.expr, RustLitExpr):
                                    new_expr = element_1.expr
                                elif isinstance(element_1.expr, RustPathExpr):
                                    changed_10 = False
                                    new_attrs = []
                                    for element_2 in element_1.expr.attrs:
                                        changed_11 = False
                                        new_meta = proc(element_2.meta)
                                        assert(is_rust_meta(new_meta))
                                        if new_meta is not element_2.meta:
                                            changed_11 = True
                                        if changed_11:
                                            new_element_2 = RustAttr(hashtag=element_2.hashtag, exclamation_mark=element_2.exclamation_mark, open_bracket=element_2.open_bracket, meta=new_meta, close_bracket=element_2.close_bracket)
                                            changed_10 = True
                                        else:
                                            new_element_2 = element_2
                                        new_elements.append(new_element_2)
                                    if isinstance(element_1.expr.qself, RustQself):
                                        new_qself_1 = proc(element_1.expr.qself)
                                        assert(isinstance(new_qself_1, RustQself))
                                        if new_qself_1 is not element_1.expr.qself:
                                            changed_10 = True
                                    elif element_1.expr.qself is None:
                                        new_qself_1 = element_1.expr.qself
                                    else:
                                        assert_never(element_1.expr.qself)
                                    new_path_3 = proc(element_1.expr.path)
                                    assert(isinstance(new_path_3, RustPath))
                                    if new_path_3 is not element_1.expr.path:
                                        changed_10 = True
                                    if changed_10:
                                        new_expr = RustPathExpr(attrs=new_attrs, qself=new_qself_1, path=new_path_3)
                                        changed_8 = True
                                    else:
                                        new_expr = element_1.expr
                                elif isinstance(element_1.expr, RustCallExpr):
                                    changed_12 = False
                                    new_operator = proc(element_1.expr.operator)
                                    assert(is_rust_expr(new_operator))
                                    if new_operator is not element_1.expr.operator:
                                        changed_12 = True
                                    new_args_2 = Punctuated()
                                    for (element_3, separator_2) in element_1.expr.args.delimited:
                                        new_element_3 = proc(element_3)
                                        assert(is_rust_expr(new_element_3))
                                        if new_element_3 is not element_3:
                                            changed_12 = True
                                        new_separator_2 = separator_2
                                        new_args_2.append(new_element_3, new_separator_2)
                                    new_last_2 = proc(element_1.expr.args.last)
                                    assert(is_rust_expr(new_last_2))
                                    if new_last_2 is not element_1.expr.args.last:
                                        changed_12 = True
                                    new_args_2.append_final(new_last_2)
                                    if changed_12:
                                        new_expr = RustCallExpr(operator=new_operator, open_paren=element_1.expr.open_paren, args=new_args_2, close_paren=element_1.expr.close_paren)
                                        changed_8 = True
                                    else:
                                        new_expr = element_1.expr
                                elif isinstance(element_1.expr, RustStructExpr):
                                    changed_13 = False
                                    new_path_4 = proc(element_1.expr.path)
                                    assert(isinstance(new_path_4, RustPath))
                                    if new_path_4 is not element_1.expr.path:
                                        changed_13 = True
                                    new_inits = Punctuated()
                                    for (element_4, separator_3) in element_1.expr.inits.delimited:
                                        changed_14 = False
                                        new_value = proc(element_4.value)
                                        assert(is_rust_expr(new_value))
                                        if new_value is not element_4.value:
                                            changed_14 = True
                                        if changed_14:
                                            new_element_4 = RustInit(name=element_4.name, equals=element_4.equals, value=new_value)
                                            changed_13 = True
                                        else:
                                            new_element_4 = element_4
                                        new_separator_3 = proc(separator_3)
                                        assert(isinstance(new_separator_3, RustComma))
                                        if new_separator_3 is not separator_3:
                                            changed_13 = True
                                        new_inits.append(new_element_4, new_separator_3)
                                    new_last_3 = proc(element_1.expr.inits.last)
                                    assert(isinstance(new_last_3, RustInit))
                                    if new_last_3 is not element_1.expr.inits.last:
                                        changed_13 = True
                                    new_inits.append_final(new_last_3)
                                    if changed_13:
                                        new_expr = RustStructExpr(path=new_path_4, open_brace=element_1.expr.open_brace, inits=new_inits, comma=element_1.expr.comma, close_brace=element_1.expr.close_brace)
                                        changed_8 = True
                                    else:
                                        new_expr = element_1.expr
                                elif isinstance(element_1.expr, RustBlockExpr):
                                    changed_15 = False
                                    if isinstance(element_1.expr.item, RustEnumItem):
                                        changed_16 = False
                                        new_attrs_1 = []
                                        for element_5 in element_1.expr.item.attrs:
                                            new_element_5 = proc(element_5)
                                            assert(isinstance(new_element_5, RustAttr))
                                            if new_element_5 is not element_5:
                                                changed_16 = True
                                            new_elements_1.append(new_element_5)
                                        if isinstance(element_1.expr.item.visibility, RustPublic):
                                            changed_17 = False
                                            if isinstance(element_1.expr.item.visibility.restrict, tuple):
                                                new_elements_2 = []
                                                element_0 = element_1.expr.item.visibility.restrict[0]
                                                new_element_0 = element_0
                                                new_elements_2.append(new_element_0)
                                                element_1 = element_1.expr.item.visibility.restrict[1]
                                                if isinstance(element_1, RustInKeyword):
                                                    new_element_1 = element_1
                                                elif element_1 is None:
                                                    new_element_1 = element_1
                                                else:
                                                    assert_never(element_1)
                                                new_elements_2.append(new_element_1)
                                                element_2 = element_1.expr.item.visibility.restrict[2]
                                                new_element_2 = proc(element_2)
                                                assert(isinstance(new_element_2, RustPath))
                                                if new_element_2 is not element_2:
                                                    changed_17 = True
                                                new_elements_2.append(new_element_2)
                                                element_3 = element_1.expr.item.visibility.restrict[3]
                                                new_element_3 = element_3
                                                new_elements_2.append(new_element_3)
                                                new_restrict = tuple(new_elements_2) if changed_17 else element_1.expr.item.visibility.restrict
                                            elif element_1.expr.item.visibility.restrict is None:
                                                new_restrict = element_1.expr.item.visibility.restrict
                                            else:
                                                assert_never(element_1.expr.item.visibility.restrict)
                                            if changed_17:
                                                new_visibility = RustPublic(pub_keyword=element_1.expr.item.visibility.pub_keyword, restrict=new_restrict)
                                                changed_16 = True
                                            else:
                                                new_visibility = element_1.expr.item.visibility
                                        elif element_1.expr.item.visibility is None:
                                            new_visibility = element_1.expr.item.visibility
                                        else:
                                            assert_never(element_1.expr.item.visibility)
                                        new_variants = Punctuated()
                                        for (element_6, separator_4) in element_1.expr.item.variants.delimited:
                                            if isinstance(element_6, RustStructVariant):
                                                changed_18 = False
                                                new_fields = Punctuated()
                                                for (element_7, separator_5) in element_6.fields.delimited:
                                                    changed_19 = False
                                                    new_type_expr_2 = proc(element_7.type_expr)
                                                    assert(is_rust_type_expr(new_type_expr_2))
                                                    if new_type_expr_2 is not element_7.type_expr:
                                                        changed_19 = True
                                                    if changed_19:
                                                        new_element_7 = RustField(name=element_7.name, colon=element_7.colon, type_expr=new_type_expr_2)
                                                        changed_18 = True
                                                    else:
                                                        new_element_7 = element_7
                                                    new_separator_5 = proc(separator_5)
                                                    assert(isinstance(new_separator_5, RustComma))
                                                    if new_separator_5 is not separator_5:
                                                        changed_18 = True
                                                    new_fields.append(new_element_7, new_separator_5)
                                                new_last_5 = proc(element_6.fields.last)
                                                assert(isinstance(new_last_5, RustField))
                                                if new_last_5 is not element_6.fields.last:
                                                    changed_18 = True
                                                new_fields.append_final(new_last_5)
                                                if changed_18:
                                                    new_element_6 = RustStructVariant(name=element_6.name, open_brace=element_6.open_brace, fields=new_fields, comma=element_6.comma, close_brace=element_6.close_brace)
                                                    changed_16 = True
                                                else:
                                                    new_element_6 = element_6
                                            elif isinstance(element_6, RustTupleVariant):
                                                changed_20 = False
                                                new_types = Punctuated()
                                                for (element_8, separator_6) in element_6.types.delimited:
                                                    new_element_8 = proc(element_8)
                                                    assert(is_rust_type_expr(new_element_8))
                                                    if new_element_8 is not element_8:
                                                        changed_20 = True
                                                    new_separator_6 = proc(separator_6)
                                                    assert(isinstance(new_separator_6, RustComma))
                                                    if new_separator_6 is not separator_6:
                                                        changed_20 = True
                                                    new_types.append(new_element_8, new_separator_6)
                                                new_last_6 = proc(element_6.types.last)
                                                assert(is_rust_type_expr(new_last_6))
                                                if new_last_6 is not element_6.types.last:
                                                    changed_20 = True
                                                new_types.append_final(new_last_6)
                                                if changed_20:
                                                    new_element_6 = RustTupleVariant(name=element_6.name, open_paren=element_6.open_paren, types=new_types, close_paren=element_6.close_paren)
                                                    changed_16 = True
                                                else:
                                                    new_element_6 = element_6
                                            elif isinstance(element_6, RustEmptyVariant):
                                                changed_21 = False
                                                if isinstance(element_6.init, RustInit):
                                                    new_init = proc(element_6.init)
                                                    assert(isinstance(new_init, RustInit))
                                                    if new_init is not element_6.init:
                                                        changed_21 = True
                                                elif element_6.init is None:
                                                    new_init = element_6.init
                                                else:
                                                    assert_never(element_6.init)
                                                if changed_21:
                                                    new_element_6 = RustEmptyVariant(name=element_6.name, init=new_init)
                                                    changed_16 = True
                                                else:
                                                    new_element_6 = element_6
                                            else:
                                                assert_never(element_6)
                                            new_separator_4 = proc(separator_4)
                                            assert(isinstance(new_separator_4, RustComma))
                                            if new_separator_4 is not separator_4:
                                                changed_16 = True
                                            new_variants.append(new_element_6, new_separator_4)
                                        new_last_4 = proc(element_1.expr.item.variants.last)
                                        assert(is_rust_variant(new_last_4))
                                        if new_last_4 is not element_1.expr.item.variants.last:
                                            changed_16 = True
                                        new_variants.append_final(new_last_4)
                                        if changed_16:
                                            new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=element_1.expr.item.enum_keyword, name=element_1.expr.item.name, open_brace=element_1.expr.item.open_brace, variants=new_variants, comma=element_1.expr.item.comma, close_brace=element_1.expr.item.close_brace)
                                            changed_15 = True
                                        else:
                                            new_item = element_1.expr.item
                                    elif isinstance(element_1.expr.item, RustStructItem):
                                        changed_22 = False
                                        new_attrs_2 = []
                                        for element_9 in element_1.expr.item.attrs:
                                            new_element_9 = proc(element_9)
                                            assert(isinstance(new_element_9, RustAttr))
                                            if new_element_9 is not element_9:
                                                changed_22 = True
                                            new_elements_3.append(new_element_9)
                                        if isinstance(element_1.expr.item.visibility, RustPublic):
                                            new_visibility_1 = proc(element_1.expr.item.visibility)
                                            assert(isinstance(new_visibility_1, RustPublic))
                                            if new_visibility_1 is not element_1.expr.item.visibility:
                                                changed_22 = True
                                        elif element_1.expr.item.visibility is None:
                                            new_visibility_1 = element_1.expr.item.visibility
                                        else:
                                            assert_never(element_1.expr.item.visibility)
                                        new_fields_1 = Punctuated()
                                        for (element_10, separator_7) in element_1.expr.item.fields.delimited:
                                            new_element_10 = proc(element_10)
                                            assert(isinstance(new_element_10, RustField))
                                            if new_element_10 is not element_10:
                                                changed_22 = True
                                            new_separator_7 = proc(separator_7)
                                            assert(isinstance(new_separator_7, RustComma))
                                            if new_separator_7 is not separator_7:
                                                changed_22 = True
                                            new_fields_1.append(new_element_10, new_separator_7)
                                        new_last_7 = proc(element_1.expr.item.fields.last)
                                        assert(isinstance(new_last_7, RustField))
                                        if new_last_7 is not element_1.expr.item.fields.last:
                                            changed_22 = True
                                        new_fields_1.append_final(new_last_7)
                                        if changed_22:
                                            new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=element_1.expr.item.struct_keyword, name=element_1.expr.item.name, open_brace=element_1.expr.item.open_brace, fields=new_fields_1, comma=element_1.expr.item.comma, close_brace=element_1.expr.item.close_brace)
                                            changed_15 = True
                                        else:
                                            new_item = element_1.expr.item
                                    elif isinstance(element_1.expr.item, RustUseItem):
                                        changed_23 = False
                                        new_attrs_3 = []
                                        for element_11 in element_1.expr.item.attrs:
                                            new_element_11 = proc(element_11)
                                            assert(isinstance(new_element_11, RustAttr))
                                            if new_element_11 is not element_11:
                                                changed_23 = True
                                            new_elements_4.append(new_element_11)
                                        if isinstance(element_1.expr.item.visibility, RustPublic):
                                            new_visibility_2 = proc(element_1.expr.item.visibility)
                                            assert(isinstance(new_visibility_2, RustPublic))
                                            if new_visibility_2 is not element_1.expr.item.visibility:
                                                changed_23 = True
                                        elif element_1.expr.item.visibility is None:
                                            new_visibility_2 = element_1.expr.item.visibility
                                        else:
                                            assert_never(element_1.expr.item.visibility)
                                        if changed_23:
                                            new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=element_1.expr.item.use_keyword, colon_colon=element_1.expr.item.colon_colon, path=element_1.expr.item.path, semicolon=element_1.expr.item.semicolon)
                                            changed_15 = True
                                        else:
                                            new_item = element_1.expr.item
                                    elif isinstance(element_1.expr.item, RustExprItem):
                                        changed_24 = False
                                        new_expr_1 = proc(element_1.expr.item.expr)
                                        assert(is_rust_expr(new_expr_1))
                                        if new_expr_1 is not element_1.expr.item.expr:
                                            changed_24 = True
                                        if changed_24:
                                            new_item = RustExprItem(expr=new_expr_1)
                                            changed_15 = True
                                        else:
                                            new_item = element_1.expr.item
                                    else:
                                        assert_never(element_1.expr.item)
                                    new_last_8 = proc(element_1.expr.last)
                                    assert(is_rust_expr(new_last_8))
                                    if new_last_8 is not element_1.expr.last:
                                        changed_15 = True
                                    if changed_15:
                                        new_expr = RustBlockExpr(open_brace=element_1.expr.open_brace, item=new_item, semicolon=element_1.expr.semicolon, last=new_last_8, close_brace=element_1.expr.close_brace)
                                        changed_8 = True
                                    else:
                                        new_expr = element_1.expr
                                elif isinstance(element_1.expr, RustRetExpr):
                                    changed_25 = False
                                    new_expr_2 = proc(element_1.expr.expr)
                                    assert(is_rust_expr(new_expr_2))
                                    if new_expr_2 is not element_1.expr.expr:
                                        changed_25 = True
                                    if changed_25:
                                        new_expr = RustRetExpr(return_keyword=element_1.expr.return_keyword, expr=new_expr_2)
                                        changed_8 = True
                                    else:
                                        new_expr = element_1.expr
                                else:
                                    assert_never(element_1.expr)
                                if changed_8:
                                    new_element_1 = RustArrayTypeExpr(open_bracket=element_1.open_bracket, type_expr=new_type_expr_1, semicolon=element_1.semicolon, expr=new_expr, close_bracket=element_1.close_bracket)
                                    changed_4 = True
                                else:
                                    new_element_1 = element_1
                            elif isinstance(element_1, RustNeverTypeExpr):
                                new_element_1 = element_1
                            elif isinstance(element_1, RustTupleTypeExpr):
                                changed_27 = False
                                new_elements_5 = Punctuated()
                                for (element_12, separator_8) in element_1.elements.delimited:
                                    new_element_12 = proc(element_12)
                                    assert(is_rust_type_expr(new_element_12))
                                    if new_element_12 is not element_12:
                                        changed_27 = True
                                    new_separator_8 = proc(separator_8)
                                    assert(isinstance(new_separator_8, RustComma))
                                    if new_separator_8 is not separator_8:
                                        changed_27 = True
                                    new_elements_5.append(new_element_12, new_separator_8)
                                new_last_9 = proc(element_1.elements.last)
                                assert(is_rust_type_expr(new_last_9))
                                if new_last_9 is not element_1.elements.last:
                                    changed_27 = True
                                new_elements_5.append_final(new_last_9)
                                if changed_27:
                                    new_element_1 = RustTupleTypeExpr(open_paren=element_1.open_paren, elements=new_elements_5, close_paren=element_1.close_paren)
                                    changed_4 = True
                                else:
                                    new_element_1 = element_1
                            else:
                                assert_never(element_1)
                        elif is_rust_expr(element_1):
                            new_element_1 = proc(element_1)
                            assert(is_rust_expr(new_element_1))
                            if new_element_1 is not element_1:
                                changed_4 = True
                        elif isinstance(element_1, RustAssocType):
                            changed_28 = False
                            if isinstance(element_1.generics, RustAngleBracketedGenericArguments):
                                changed_29 = False
                                new_args_3 = Punctuated()
                                for (element_13, separator_9) in element_1.generics.args.delimited:
                                    new_element_13 = proc(element_13)
                                    assert(is_rust_generic_argument(new_element_13))
                                    if new_element_13 is not element_13:
                                        changed_29 = True
                                    new_separator_9 = proc(separator_9)
                                    assert(isinstance(new_separator_9, RustComma))
                                    if new_separator_9 is not separator_9:
                                        changed_29 = True
                                    new_args_3.append(new_element_13, new_separator_9)
                                new_last_10 = proc(element_1.generics.args.last)
                                assert(is_rust_generic_argument(new_last_10))
                                if new_last_10 is not element_1.generics.args.last:
                                    changed_29 = True
                                new_args_3.append_final(new_last_10)
                                if changed_29:
                                    new_generics = RustAngleBracketedGenericArguments(less_than=element_1.generics.less_than, args=new_args_3, greater_than=element_1.generics.greater_than)
                                    changed_28 = True
                                else:
                                    new_generics = element_1.generics
                            elif element_1.generics is None:
                                new_generics = element_1.generics
                            else:
                                assert_never(element_1.generics)
                            new_type_expr_3 = proc(element_1.type_expr)
                            assert(is_rust_type_expr(new_type_expr_3))
                            if new_type_expr_3 is not element_1.type_expr:
                                changed_28 = True
                            if changed_28:
                                new_element_1 = RustAssocType(name=element_1.name, generics=new_generics, equals=element_1.equals, type_expr=new_type_expr_3)
                                changed_4 = True
                            else:
                                new_element_1 = element_1
                        elif isinstance(element_1, RustAssocConst):
                            changed_30 = False
                            if isinstance(element_1.generics, RustAngleBracketedGenericArguments):
                                new_generics_1 = proc(element_1.generics)
                                assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                if new_generics_1 is not element_1.generics:
                                    changed_30 = True
                            elif element_1.generics is None:
                                new_generics_1 = element_1.generics
                            else:
                                assert_never(element_1.generics)
                            new_expr_3 = proc(element_1.expr)
                            assert(is_rust_expr(new_expr_3))
                            if new_expr_3 is not element_1.expr:
                                changed_30 = True
                            if changed_30:
                                new_element_1 = RustAssocConst(name=element_1.name, generics=new_generics_1, equals=element_1.equals, expr=new_expr_3)
                                changed_4 = True
                            else:
                                new_element_1 = element_1
                        elif isinstance(element_1, RustConstraint):
                            changed_31 = False
                            new_generics_2 = proc(element_1.generics)
                            assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                            if new_generics_2 is not element_1.generics:
                                changed_31 = True
                            new_bounds = Punctuated()
                            for (element_14, separator_10) in element_1.bounds.delimited:
                                if isinstance(element_14, RustTraitBound):
                                    changed_32 = False
                                    if isinstance(element_14.bound_lifetimes, RustBoundLifetimes):
                                        changed_33 = False
                                        new_lifetimes = Punctuated()
                                        for (element_15, separator_11) in element_14.bound_lifetimes.lifetimes.delimited:
                                            if isinstance(element_15, RustLifetime):
                                                new_element_15 = proc(element_15)
                                                assert(isinstance(new_element_15, RustLifetime))
                                                if new_element_15 is not element_15:
                                                    changed_33 = True
                                            elif isinstance(element_15, RustTypeParam):
                                                changed_34 = False
                                                new_type_param_bound = proc(element_15.type_param_bound)
                                                assert(is_rust_type_param_bound(new_type_param_bound))
                                                if new_type_param_bound is not element_15.type_param_bound:
                                                    changed_34 = True
                                                if isinstance(element_15.default, RustTypeInit):
                                                    changed_35 = False
                                                    new_type_expr_4 = proc(element_15.default.type_expr)
                                                    assert(is_rust_type_expr(new_type_expr_4))
                                                    if new_type_expr_4 is not element_15.default.type_expr:
                                                        changed_35 = True
                                                    if changed_35:
                                                        new_default = RustTypeInit(equals=element_15.default.equals, type_expr=new_type_expr_4)
                                                        changed_34 = True
                                                    else:
                                                        new_default = element_15.default
                                                elif element_15.default is None:
                                                    new_default = element_15.default
                                                else:
                                                    assert_never(element_15.default)
                                                if changed_34:
                                                    new_element_15 = RustTypeParam(name=element_15.name, colon=element_15.colon, type_param_bound=new_type_param_bound, percent=element_15.percent, plus=element_15.plus, default=new_default)
                                                    changed_33 = True
                                                else:
                                                    new_element_15 = element_15
                                            elif isinstance(element_15, RustConstParam):
                                                changed_36 = False
                                                new_type_expr_5 = proc(element_15.type_expr)
                                                assert(is_rust_type_expr(new_type_expr_5))
                                                if new_type_expr_5 is not element_15.type_expr:
                                                    changed_36 = True
                                                if isinstance(element_15.default, RustInit):
                                                    new_default_1 = proc(element_15.default)
                                                    assert(isinstance(new_default_1, RustInit))
                                                    if new_default_1 is not element_15.default:
                                                        changed_36 = True
                                                elif element_15.default is None:
                                                    new_default_1 = element_15.default
                                                else:
                                                    assert_never(element_15.default)
                                                if changed_36:
                                                    new_element_15 = RustConstParam(const_keyword=element_15.const_keyword, name=element_15.name, colon=element_15.colon, type_expr=new_type_expr_5, default=new_default_1)
                                                    changed_33 = True
                                                else:
                                                    new_element_15 = element_15
                                            else:
                                                assert_never(element_15)
                                            new_separator_11 = proc(separator_11)
                                            assert(isinstance(new_separator_11, RustComma))
                                            if new_separator_11 is not separator_11:
                                                changed_33 = True
                                            new_lifetimes.append(new_element_15, new_separator_11)
                                        new_last_12 = proc(element_14.bound_lifetimes.lifetimes.last)
                                        assert(is_rust_generic_param(new_last_12))
                                        if new_last_12 is not element_14.bound_lifetimes.lifetimes.last:
                                            changed_33 = True
                                        new_lifetimes.append_final(new_last_12)
                                        if changed_33:
                                            new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_14.bound_lifetimes.for_keyword, less_than=element_14.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_14.bound_lifetimes.greater_than)
                                            changed_32 = True
                                        else:
                                            new_bound_lifetimes = element_14.bound_lifetimes
                                    elif element_14.bound_lifetimes is None:
                                        new_bound_lifetimes = element_14.bound_lifetimes
                                    else:
                                        assert_never(element_14.bound_lifetimes)
                                    new_path_5 = proc(element_14.path)
                                    assert(isinstance(new_path_5, RustPath))
                                    if new_path_5 is not element_14.path:
                                        changed_32 = True
                                    if changed_32:
                                        new_element_14 = RustTraitBound(modifier=element_14.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_5)
                                        changed_31 = True
                                    else:
                                        new_element_14 = element_14
                                elif isinstance(element_14, RustLifetime):
                                    new_element_14 = proc(element_14)
                                    assert(isinstance(new_element_14, RustLifetime))
                                    if new_element_14 is not element_14:
                                        changed_31 = True
                                else:
                                    assert_never(element_14)
                                new_separator_10 = separator_10
                                new_bounds.append(new_element_14, new_separator_10)
                            new_last_11 = proc(element_1.bounds.last)
                            assert(is_rust_type_param_bound(new_last_11))
                            if new_last_11 is not element_1.bounds.last:
                                changed_31 = True
                            new_bounds.append_final(new_last_11)
                            if changed_31:
                                new_element_1 = RustConstraint(name=element_1.name, generics=new_generics_2, colon=element_1.colon, bounds=new_bounds)
                                changed_4 = True
                            else:
                                new_element_1 = element_1
                        else:
                            assert_never(element_1)
                        new_separator_1 = proc(separator_1)
                        assert(isinstance(new_separator_1, RustComma))
                        if new_separator_1 is not separator_1:
                            changed_4 = True
                        new_args_1.append(new_element_1, new_separator_1)
                    new_last_1 = proc(element.args.args.last)
                    assert(is_rust_generic_argument(new_last_1))
                    if new_last_1 is not element.args.args.last:
                        changed_4 = True
                    new_args_1.append_final(new_last_1)
                    if changed_4:
                        new_args = RustTurbofish(colon_colon=element.args.colon_colon, less_than=element.args.less_than, args=new_args_1, greater_than=element.args.greater_than)
                        changed_3 = True
                    else:
                        new_args = element.args
                elif isinstance(element.args, RustAngleBracketedGenericArguments):
                    new_args = proc(element.args)
                    assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                    if new_args is not element.args:
                        changed_3 = True
                elif isinstance(element.args, RustParenthesizedGenericArguments):
                    changed_37 = False
                    new_params = Punctuated()
                    for (element_16, separator_12) in element.args.params.delimited:
                        new_element_16 = proc(element_16)
                        assert(is_rust_type_expr(new_element_16))
                        if new_element_16 is not element_16:
                            changed_37 = True
                        new_separator_12 = proc(separator_12)
                        assert(isinstance(new_separator_12, RustComma))
                        if new_separator_12 is not separator_12:
                            changed_37 = True
                        new_params.append(new_element_16, new_separator_12)
                    new_last_13 = proc(element.args.params.last)
                    assert(is_rust_type_expr(new_last_13))
                    if new_last_13 is not element.args.params.last:
                        changed_37 = True
                    new_params.append_final(new_last_13)
                    new_result = proc(element.args.result)
                    assert(is_rust_type_expr(new_result))
                    if new_result is not element.args.result:
                        changed_37 = True
                    if changed_37:
                        new_args = RustParenthesizedGenericArguments(open_paren=element.args.open_paren, params=new_params, close_paren=element.args.close_paren, r_arrow=element.args.r_arrow, result=new_result)
                        changed_3 = True
                    else:
                        new_args = element.args
                else:
                    assert_never(element.args)
            elif element.args is None:
                new_args = element.args
            else:
                assert_never(element.args)
            if changed_3:
                new_element = RustPathSegment(name=element.name, args=new_args)
                changed_2 = True
            else:
                new_element = element
            new_separator = separator
            new_segments.append(new_element, new_separator)
        new_last = proc(node.path.segments.last)
        assert(isinstance(new_last, RustPathSegment))
        if new_last is not node.path.segments.last:
            changed_2 = True
        new_segments.append_final(new_last)
        if changed_2:
            new_path = RustPath(leading_colon_colon=node.path.leading_colon_colon, segments=new_segments)
            changed_1 = True
        else:
            new_path = node.path
        if changed_1:
            rewritten = RustMetaBraced(path=new_path, open_brace=node.open_brace, tokens=node.tokens, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustMetaBracketed):
        changed_38 = False
        new_path_6 = proc(node.path)
        assert(isinstance(new_path_6, RustPath))
        if new_path_6 is not node.path:
            changed_38 = True
        if changed_38:
            rewritten = RustMetaBracketed(path=new_path_6, open_bracket=node.open_bracket, tokens=node.tokens, close_bracket=node.close_bracket)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustMetaNameValue):
        changed_39 = False
        new_path_7 = proc(node.path)
        assert(isinstance(new_path_7, RustPath))
        if new_path_7 is not node.path:
            changed_39 = True
        new_expr_4 = proc(node.expr)
        assert(is_rust_expr(new_expr_4))
        if new_expr_4 is not node.expr:
            changed_39 = True
        if changed_39:
            rewritten = RustMetaNameValue(path=new_path_7, equals=node.equals, expr=new_expr_4)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustMetaParenthesized):
        changed_40 = False
        new_path_8 = proc(node.path)
        assert(isinstance(new_path_8, RustPath))
        if new_path_8 is not node.path:
            changed_40 = True
        if changed_40:
            rewritten = RustMetaParenthesized(path=new_path_8, open_paren=node.open_paren, tokens=node.tokens, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustMetaPath):
        changed_41 = False
        new_path_9 = proc(node.path)
        assert(isinstance(new_path_9, RustPath))
        if new_path_9 is not node.path:
            changed_41 = True
        if changed_41:
            rewritten = RustMetaPath(path=new_path_9)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_path_arguments(node: RustPathArguments, proc: Callable[[RustPathArguments], RustPathArguments]) -> RustPathArguments:
    if isinstance(node, RustAngleBracketedGenericArguments):
        changed_1 = False
        new_args = Punctuated()
        for (element, separator) in node.args.delimited:
            if isinstance(element, RustLifetime):
                new_element = element
            elif is_rust_type_expr(element):
                if isinstance(element, RustPathTypeExpr):
                    changed_3 = False
                    if isinstance(element.qself, RustQself):
                        changed_4 = False
                        new_type_expr = proc(element.qself.type_expr)
                        assert(is_rust_type_expr(new_type_expr))
                        if new_type_expr is not element.qself.type_expr:
                            changed_4 = True
                        changed_5 = False
                        new_segments = Punctuated()
                        for (element_1, separator_1) in element.qself.path.segments.delimited:
                            changed_6 = False
                            if is_rust_path_arguments(element_1.args):
                                new_args_1 = proc(element_1.args)
                                assert(is_rust_path_arguments(new_args_1))
                                if new_args_1 is not element_1.args:
                                    changed_6 = True
                            elif element_1.args is None:
                                new_args_1 = element_1.args
                            else:
                                assert_never(element_1.args)
                            if changed_6:
                                new_element_1 = RustPathSegment(name=element_1.name, args=new_args_1)
                                changed_5 = True
                            else:
                                new_element_1 = element_1
                            new_separator_1 = separator_1
                            new_segments.append(new_element_1, new_separator_1)
                        new_last_1 = proc(element.qself.path.segments.last)
                        assert(isinstance(new_last_1, RustPathSegment))
                        if new_last_1 is not element.qself.path.segments.last:
                            changed_5 = True
                        new_segments.append_final(new_last_1)
                        if changed_5:
                            new_path = RustPath(leading_colon_colon=element.qself.path.leading_colon_colon, segments=new_segments)
                            changed_4 = True
                        else:
                            new_path = element.qself.path
                        if changed_4:
                            new_qself = RustQself(less_than=element.qself.less_than, type_expr=new_type_expr, as_keyword=element.qself.as_keyword, path=new_path, greater_than=element.qself.greater_than)
                            changed_3 = True
                        else:
                            new_qself = element.qself
                    elif element.qself is None:
                        new_qself = element.qself
                    else:
                        assert_never(element.qself)
                    new_path_1 = proc(element.path)
                    assert(isinstance(new_path_1, RustPath))
                    if new_path_1 is not element.path:
                        changed_3 = True
                    if changed_3:
                        new_element = RustPathTypeExpr(qself=new_qself, path=new_path_1)
                        changed_1 = True
                    else:
                        new_element = element
                elif isinstance(element, RustArrayTypeExpr):
                    changed_7 = False
                    new_type_expr_1 = proc(element.type_expr)
                    assert(is_rust_type_expr(new_type_expr_1))
                    if new_type_expr_1 is not element.type_expr:
                        changed_7 = True
                    if isinstance(element.expr, RustLitExpr):
                        new_expr = element.expr
                    elif isinstance(element.expr, RustPathExpr):
                        changed_9 = False
                        new_attrs = []
                        for element_2 in element.expr.attrs:
                            changed_10 = False
                            if isinstance(element_2.meta, RustMetaPath):
                                changed_11 = False
                                new_path_2 = proc(element_2.meta.path)
                                assert(isinstance(new_path_2, RustPath))
                                if new_path_2 is not element_2.meta.path:
                                    changed_11 = True
                                if changed_11:
                                    new_meta = RustMetaPath(path=new_path_2)
                                    changed_10 = True
                                else:
                                    new_meta = element_2.meta
                            elif isinstance(element_2.meta, RustMetaParenthesized):
                                changed_12 = False
                                new_path_3 = proc(element_2.meta.path)
                                assert(isinstance(new_path_3, RustPath))
                                if new_path_3 is not element_2.meta.path:
                                    changed_12 = True
                                if changed_12:
                                    new_meta = RustMetaParenthesized(path=new_path_3, open_paren=element_2.meta.open_paren, tokens=element_2.meta.tokens, close_paren=element_2.meta.close_paren)
                                    changed_10 = True
                                else:
                                    new_meta = element_2.meta
                            elif isinstance(element_2.meta, RustMetaBracketed):
                                changed_13 = False
                                new_path_4 = proc(element_2.meta.path)
                                assert(isinstance(new_path_4, RustPath))
                                if new_path_4 is not element_2.meta.path:
                                    changed_13 = True
                                if changed_13:
                                    new_meta = RustMetaBracketed(path=new_path_4, open_bracket=element_2.meta.open_bracket, tokens=element_2.meta.tokens, close_bracket=element_2.meta.close_bracket)
                                    changed_10 = True
                                else:
                                    new_meta = element_2.meta
                            elif isinstance(element_2.meta, RustMetaBraced):
                                changed_14 = False
                                new_path_5 = proc(element_2.meta.path)
                                assert(isinstance(new_path_5, RustPath))
                                if new_path_5 is not element_2.meta.path:
                                    changed_14 = True
                                if changed_14:
                                    new_meta = RustMetaBraced(path=new_path_5, open_brace=element_2.meta.open_brace, tokens=element_2.meta.tokens, close_brace=element_2.meta.close_brace)
                                    changed_10 = True
                                else:
                                    new_meta = element_2.meta
                            elif isinstance(element_2.meta, RustMetaNameValue):
                                changed_15 = False
                                new_path_6 = proc(element_2.meta.path)
                                assert(isinstance(new_path_6, RustPath))
                                if new_path_6 is not element_2.meta.path:
                                    changed_15 = True
                                new_expr_1 = proc(element_2.meta.expr)
                                assert(is_rust_expr(new_expr_1))
                                if new_expr_1 is not element_2.meta.expr:
                                    changed_15 = True
                                if changed_15:
                                    new_meta = RustMetaNameValue(path=new_path_6, equals=element_2.meta.equals, expr=new_expr_1)
                                    changed_10 = True
                                else:
                                    new_meta = element_2.meta
                            else:
                                assert_never(element_2.meta)
                            if changed_10:
                                new_element_2 = RustAttr(hashtag=element_2.hashtag, exclamation_mark=element_2.exclamation_mark, open_bracket=element_2.open_bracket, meta=new_meta, close_bracket=element_2.close_bracket)
                                changed_9 = True
                            else:
                                new_element_2 = element_2
                            new_elements.append(new_element_2)
                        if isinstance(element.expr.qself, RustQself):
                            new_qself_1 = proc(element.expr.qself)
                            assert(isinstance(new_qself_1, RustQself))
                            if new_qself_1 is not element.expr.qself:
                                changed_9 = True
                        elif element.expr.qself is None:
                            new_qself_1 = element.expr.qself
                        else:
                            assert_never(element.expr.qself)
                        new_path_7 = proc(element.expr.path)
                        assert(isinstance(new_path_7, RustPath))
                        if new_path_7 is not element.expr.path:
                            changed_9 = True
                        if changed_9:
                            new_expr = RustPathExpr(attrs=new_attrs, qself=new_qself_1, path=new_path_7)
                            changed_7 = True
                        else:
                            new_expr = element.expr
                    elif isinstance(element.expr, RustCallExpr):
                        changed_16 = False
                        new_operator = proc(element.expr.operator)
                        assert(is_rust_expr(new_operator))
                        if new_operator is not element.expr.operator:
                            changed_16 = True
                        new_args_2 = Punctuated()
                        for (element_3, separator_2) in element.expr.args.delimited:
                            new_element_3 = proc(element_3)
                            assert(is_rust_expr(new_element_3))
                            if new_element_3 is not element_3:
                                changed_16 = True
                            new_separator_2 = separator_2
                            new_args_2.append(new_element_3, new_separator_2)
                        new_last_2 = proc(element.expr.args.last)
                        assert(is_rust_expr(new_last_2))
                        if new_last_2 is not element.expr.args.last:
                            changed_16 = True
                        new_args_2.append_final(new_last_2)
                        if changed_16:
                            new_expr = RustCallExpr(operator=new_operator, open_paren=element.expr.open_paren, args=new_args_2, close_paren=element.expr.close_paren)
                            changed_7 = True
                        else:
                            new_expr = element.expr
                    elif isinstance(element.expr, RustStructExpr):
                        changed_17 = False
                        new_path_8 = proc(element.expr.path)
                        assert(isinstance(new_path_8, RustPath))
                        if new_path_8 is not element.expr.path:
                            changed_17 = True
                        new_inits = Punctuated()
                        for (element_4, separator_3) in element.expr.inits.delimited:
                            changed_18 = False
                            new_value = proc(element_4.value)
                            assert(is_rust_expr(new_value))
                            if new_value is not element_4.value:
                                changed_18 = True
                            if changed_18:
                                new_element_4 = RustInit(name=element_4.name, equals=element_4.equals, value=new_value)
                                changed_17 = True
                            else:
                                new_element_4 = element_4
                            new_separator_3 = proc(separator_3)
                            assert(isinstance(new_separator_3, RustComma))
                            if new_separator_3 is not separator_3:
                                changed_17 = True
                            new_inits.append(new_element_4, new_separator_3)
                        new_last_3 = proc(element.expr.inits.last)
                        assert(isinstance(new_last_3, RustInit))
                        if new_last_3 is not element.expr.inits.last:
                            changed_17 = True
                        new_inits.append_final(new_last_3)
                        if changed_17:
                            new_expr = RustStructExpr(path=new_path_8, open_brace=element.expr.open_brace, inits=new_inits, comma=element.expr.comma, close_brace=element.expr.close_brace)
                            changed_7 = True
                        else:
                            new_expr = element.expr
                    elif isinstance(element.expr, RustBlockExpr):
                        changed_19 = False
                        if isinstance(element.expr.item, RustEnumItem):
                            changed_20 = False
                            new_attrs_1 = []
                            for element_5 in element.expr.item.attrs:
                                new_element_5 = proc(element_5)
                                assert(isinstance(new_element_5, RustAttr))
                                if new_element_5 is not element_5:
                                    changed_20 = True
                                new_elements_1.append(new_element_5)
                            if isinstance(element.expr.item.visibility, RustPublic):
                                changed_21 = False
                                if isinstance(element.expr.item.visibility.restrict, tuple):
                                    new_elements_2 = []
                                    element_0 = element.expr.item.visibility.restrict[0]
                                    new_element_0 = element_0
                                    new_elements_2.append(new_element_0)
                                    element_1 = element.expr.item.visibility.restrict[1]
                                    if isinstance(element_1, RustInKeyword):
                                        new_element_1 = element_1
                                    elif element_1 is None:
                                        new_element_1 = element_1
                                    else:
                                        assert_never(element_1)
                                    new_elements_2.append(new_element_1)
                                    element_2 = element.expr.item.visibility.restrict[2]
                                    new_element_2 = proc(element_2)
                                    assert(isinstance(new_element_2, RustPath))
                                    if new_element_2 is not element_2:
                                        changed_21 = True
                                    new_elements_2.append(new_element_2)
                                    element_3 = element.expr.item.visibility.restrict[3]
                                    new_element_3 = element_3
                                    new_elements_2.append(new_element_3)
                                    new_restrict = tuple(new_elements_2) if changed_21 else element.expr.item.visibility.restrict
                                elif element.expr.item.visibility.restrict is None:
                                    new_restrict = element.expr.item.visibility.restrict
                                else:
                                    assert_never(element.expr.item.visibility.restrict)
                                if changed_21:
                                    new_visibility = RustPublic(pub_keyword=element.expr.item.visibility.pub_keyword, restrict=new_restrict)
                                    changed_20 = True
                                else:
                                    new_visibility = element.expr.item.visibility
                            elif element.expr.item.visibility is None:
                                new_visibility = element.expr.item.visibility
                            else:
                                assert_never(element.expr.item.visibility)
                            new_variants = Punctuated()
                            for (element_6, separator_4) in element.expr.item.variants.delimited:
                                if isinstance(element_6, RustStructVariant):
                                    changed_22 = False
                                    new_fields = Punctuated()
                                    for (element_7, separator_5) in element_6.fields.delimited:
                                        changed_23 = False
                                        new_type_expr_2 = proc(element_7.type_expr)
                                        assert(is_rust_type_expr(new_type_expr_2))
                                        if new_type_expr_2 is not element_7.type_expr:
                                            changed_23 = True
                                        if changed_23:
                                            new_element_7 = RustField(name=element_7.name, colon=element_7.colon, type_expr=new_type_expr_2)
                                            changed_22 = True
                                        else:
                                            new_element_7 = element_7
                                        new_separator_5 = proc(separator_5)
                                        assert(isinstance(new_separator_5, RustComma))
                                        if new_separator_5 is not separator_5:
                                            changed_22 = True
                                        new_fields.append(new_element_7, new_separator_5)
                                    new_last_5 = proc(element_6.fields.last)
                                    assert(isinstance(new_last_5, RustField))
                                    if new_last_5 is not element_6.fields.last:
                                        changed_22 = True
                                    new_fields.append_final(new_last_5)
                                    if changed_22:
                                        new_element_6 = RustStructVariant(name=element_6.name, open_brace=element_6.open_brace, fields=new_fields, comma=element_6.comma, close_brace=element_6.close_brace)
                                        changed_20 = True
                                    else:
                                        new_element_6 = element_6
                                elif isinstance(element_6, RustTupleVariant):
                                    changed_24 = False
                                    new_types = Punctuated()
                                    for (element_8, separator_6) in element_6.types.delimited:
                                        new_element_8 = proc(element_8)
                                        assert(is_rust_type_expr(new_element_8))
                                        if new_element_8 is not element_8:
                                            changed_24 = True
                                        new_separator_6 = proc(separator_6)
                                        assert(isinstance(new_separator_6, RustComma))
                                        if new_separator_6 is not separator_6:
                                            changed_24 = True
                                        new_types.append(new_element_8, new_separator_6)
                                    new_last_6 = proc(element_6.types.last)
                                    assert(is_rust_type_expr(new_last_6))
                                    if new_last_6 is not element_6.types.last:
                                        changed_24 = True
                                    new_types.append_final(new_last_6)
                                    if changed_24:
                                        new_element_6 = RustTupleVariant(name=element_6.name, open_paren=element_6.open_paren, types=new_types, close_paren=element_6.close_paren)
                                        changed_20 = True
                                    else:
                                        new_element_6 = element_6
                                elif isinstance(element_6, RustEmptyVariant):
                                    changed_25 = False
                                    if isinstance(element_6.init, RustInit):
                                        new_init = proc(element_6.init)
                                        assert(isinstance(new_init, RustInit))
                                        if new_init is not element_6.init:
                                            changed_25 = True
                                    elif element_6.init is None:
                                        new_init = element_6.init
                                    else:
                                        assert_never(element_6.init)
                                    if changed_25:
                                        new_element_6 = RustEmptyVariant(name=element_6.name, init=new_init)
                                        changed_20 = True
                                    else:
                                        new_element_6 = element_6
                                else:
                                    assert_never(element_6)
                                new_separator_4 = proc(separator_4)
                                assert(isinstance(new_separator_4, RustComma))
                                if new_separator_4 is not separator_4:
                                    changed_20 = True
                                new_variants.append(new_element_6, new_separator_4)
                            new_last_4 = proc(element.expr.item.variants.last)
                            assert(is_rust_variant(new_last_4))
                            if new_last_4 is not element.expr.item.variants.last:
                                changed_20 = True
                            new_variants.append_final(new_last_4)
                            if changed_20:
                                new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=element.expr.item.enum_keyword, name=element.expr.item.name, open_brace=element.expr.item.open_brace, variants=new_variants, comma=element.expr.item.comma, close_brace=element.expr.item.close_brace)
                                changed_19 = True
                            else:
                                new_item = element.expr.item
                        elif isinstance(element.expr.item, RustStructItem):
                            changed_26 = False
                            new_attrs_2 = []
                            for element_9 in element.expr.item.attrs:
                                new_element_9 = proc(element_9)
                                assert(isinstance(new_element_9, RustAttr))
                                if new_element_9 is not element_9:
                                    changed_26 = True
                                new_elements_3.append(new_element_9)
                            if isinstance(element.expr.item.visibility, RustPublic):
                                new_visibility_1 = proc(element.expr.item.visibility)
                                assert(isinstance(new_visibility_1, RustPublic))
                                if new_visibility_1 is not element.expr.item.visibility:
                                    changed_26 = True
                            elif element.expr.item.visibility is None:
                                new_visibility_1 = element.expr.item.visibility
                            else:
                                assert_never(element.expr.item.visibility)
                            new_fields_1 = Punctuated()
                            for (element_10, separator_7) in element.expr.item.fields.delimited:
                                new_element_10 = proc(element_10)
                                assert(isinstance(new_element_10, RustField))
                                if new_element_10 is not element_10:
                                    changed_26 = True
                                new_separator_7 = proc(separator_7)
                                assert(isinstance(new_separator_7, RustComma))
                                if new_separator_7 is not separator_7:
                                    changed_26 = True
                                new_fields_1.append(new_element_10, new_separator_7)
                            new_last_7 = proc(element.expr.item.fields.last)
                            assert(isinstance(new_last_7, RustField))
                            if new_last_7 is not element.expr.item.fields.last:
                                changed_26 = True
                            new_fields_1.append_final(new_last_7)
                            if changed_26:
                                new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=element.expr.item.struct_keyword, name=element.expr.item.name, open_brace=element.expr.item.open_brace, fields=new_fields_1, comma=element.expr.item.comma, close_brace=element.expr.item.close_brace)
                                changed_19 = True
                            else:
                                new_item = element.expr.item
                        elif isinstance(element.expr.item, RustUseItem):
                            changed_27 = False
                            new_attrs_3 = []
                            for element_11 in element.expr.item.attrs:
                                new_element_11 = proc(element_11)
                                assert(isinstance(new_element_11, RustAttr))
                                if new_element_11 is not element_11:
                                    changed_27 = True
                                new_elements_4.append(new_element_11)
                            if isinstance(element.expr.item.visibility, RustPublic):
                                new_visibility_2 = proc(element.expr.item.visibility)
                                assert(isinstance(new_visibility_2, RustPublic))
                                if new_visibility_2 is not element.expr.item.visibility:
                                    changed_27 = True
                            elif element.expr.item.visibility is None:
                                new_visibility_2 = element.expr.item.visibility
                            else:
                                assert_never(element.expr.item.visibility)
                            if changed_27:
                                new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=element.expr.item.use_keyword, colon_colon=element.expr.item.colon_colon, path=element.expr.item.path, semicolon=element.expr.item.semicolon)
                                changed_19 = True
                            else:
                                new_item = element.expr.item
                        elif isinstance(element.expr.item, RustExprItem):
                            changed_28 = False
                            new_expr_2 = proc(element.expr.item.expr)
                            assert(is_rust_expr(new_expr_2))
                            if new_expr_2 is not element.expr.item.expr:
                                changed_28 = True
                            if changed_28:
                                new_item = RustExprItem(expr=new_expr_2)
                                changed_19 = True
                            else:
                                new_item = element.expr.item
                        else:
                            assert_never(element.expr.item)
                        new_last_8 = proc(element.expr.last)
                        assert(is_rust_expr(new_last_8))
                        if new_last_8 is not element.expr.last:
                            changed_19 = True
                        if changed_19:
                            new_expr = RustBlockExpr(open_brace=element.expr.open_brace, item=new_item, semicolon=element.expr.semicolon, last=new_last_8, close_brace=element.expr.close_brace)
                            changed_7 = True
                        else:
                            new_expr = element.expr
                    elif isinstance(element.expr, RustRetExpr):
                        changed_29 = False
                        new_expr_3 = proc(element.expr.expr)
                        assert(is_rust_expr(new_expr_3))
                        if new_expr_3 is not element.expr.expr:
                            changed_29 = True
                        if changed_29:
                            new_expr = RustRetExpr(return_keyword=element.expr.return_keyword, expr=new_expr_3)
                            changed_7 = True
                        else:
                            new_expr = element.expr
                    else:
                        assert_never(element.expr)
                    if changed_7:
                        new_element = RustArrayTypeExpr(open_bracket=element.open_bracket, type_expr=new_type_expr_1, semicolon=element.semicolon, expr=new_expr, close_bracket=element.close_bracket)
                        changed_1 = True
                    else:
                        new_element = element
                elif isinstance(element, RustNeverTypeExpr):
                    new_element = element
                elif isinstance(element, RustTupleTypeExpr):
                    changed_31 = False
                    new_elements_5 = Punctuated()
                    for (element_12, separator_8) in element.elements.delimited:
                        new_element_12 = proc(element_12)
                        assert(is_rust_type_expr(new_element_12))
                        if new_element_12 is not element_12:
                            changed_31 = True
                        new_separator_8 = proc(separator_8)
                        assert(isinstance(new_separator_8, RustComma))
                        if new_separator_8 is not separator_8:
                            changed_31 = True
                        new_elements_5.append(new_element_12, new_separator_8)
                    new_last_9 = proc(element.elements.last)
                    assert(is_rust_type_expr(new_last_9))
                    if new_last_9 is not element.elements.last:
                        changed_31 = True
                    new_elements_5.append_final(new_last_9)
                    if changed_31:
                        new_element = RustTupleTypeExpr(open_paren=element.open_paren, elements=new_elements_5, close_paren=element.close_paren)
                        changed_1 = True
                    else:
                        new_element = element
                else:
                    assert_never(element)
            elif is_rust_expr(element):
                new_element = proc(element)
                assert(is_rust_expr(new_element))
                if new_element is not element:
                    changed_1 = True
            elif isinstance(element, RustAssocType):
                changed_32 = False
                if isinstance(element.generics, RustAngleBracketedGenericArguments):
                    new_generics = proc(element.generics)
                    assert(isinstance(new_generics, RustAngleBracketedGenericArguments))
                    if new_generics is not element.generics:
                        changed_32 = True
                elif element.generics is None:
                    new_generics = element.generics
                else:
                    assert_never(element.generics)
                new_type_expr_3 = proc(element.type_expr)
                assert(is_rust_type_expr(new_type_expr_3))
                if new_type_expr_3 is not element.type_expr:
                    changed_32 = True
                if changed_32:
                    new_element = RustAssocType(name=element.name, generics=new_generics, equals=element.equals, type_expr=new_type_expr_3)
                    changed_1 = True
                else:
                    new_element = element
            elif isinstance(element, RustAssocConst):
                changed_33 = False
                if isinstance(element.generics, RustAngleBracketedGenericArguments):
                    new_generics_1 = proc(element.generics)
                    assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                    if new_generics_1 is not element.generics:
                        changed_33 = True
                elif element.generics is None:
                    new_generics_1 = element.generics
                else:
                    assert_never(element.generics)
                new_expr_4 = proc(element.expr)
                assert(is_rust_expr(new_expr_4))
                if new_expr_4 is not element.expr:
                    changed_33 = True
                if changed_33:
                    new_element = RustAssocConst(name=element.name, generics=new_generics_1, equals=element.equals, expr=new_expr_4)
                    changed_1 = True
                else:
                    new_element = element
            elif isinstance(element, RustConstraint):
                changed_34 = False
                new_generics_2 = proc(element.generics)
                assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                if new_generics_2 is not element.generics:
                    changed_34 = True
                new_bounds = Punctuated()
                for (element_13, separator_9) in element.bounds.delimited:
                    if isinstance(element_13, RustTraitBound):
                        changed_35 = False
                        if isinstance(element_13.bound_lifetimes, RustBoundLifetimes):
                            changed_36 = False
                            new_lifetimes = Punctuated()
                            for (element_14, separator_10) in element_13.bound_lifetimes.lifetimes.delimited:
                                if isinstance(element_14, RustLifetime):
                                    new_element_14 = proc(element_14)
                                    assert(isinstance(new_element_14, RustLifetime))
                                    if new_element_14 is not element_14:
                                        changed_36 = True
                                elif isinstance(element_14, RustTypeParam):
                                    changed_37 = False
                                    new_type_param_bound = proc(element_14.type_param_bound)
                                    assert(is_rust_type_param_bound(new_type_param_bound))
                                    if new_type_param_bound is not element_14.type_param_bound:
                                        changed_37 = True
                                    if isinstance(element_14.default, RustTypeInit):
                                        changed_38 = False
                                        new_type_expr_4 = proc(element_14.default.type_expr)
                                        assert(is_rust_type_expr(new_type_expr_4))
                                        if new_type_expr_4 is not element_14.default.type_expr:
                                            changed_38 = True
                                        if changed_38:
                                            new_default = RustTypeInit(equals=element_14.default.equals, type_expr=new_type_expr_4)
                                            changed_37 = True
                                        else:
                                            new_default = element_14.default
                                    elif element_14.default is None:
                                        new_default = element_14.default
                                    else:
                                        assert_never(element_14.default)
                                    if changed_37:
                                        new_element_14 = RustTypeParam(name=element_14.name, colon=element_14.colon, type_param_bound=new_type_param_bound, percent=element_14.percent, plus=element_14.plus, default=new_default)
                                        changed_36 = True
                                    else:
                                        new_element_14 = element_14
                                elif isinstance(element_14, RustConstParam):
                                    changed_39 = False
                                    new_type_expr_5 = proc(element_14.type_expr)
                                    assert(is_rust_type_expr(new_type_expr_5))
                                    if new_type_expr_5 is not element_14.type_expr:
                                        changed_39 = True
                                    if isinstance(element_14.default, RustInit):
                                        new_default_1 = proc(element_14.default)
                                        assert(isinstance(new_default_1, RustInit))
                                        if new_default_1 is not element_14.default:
                                            changed_39 = True
                                    elif element_14.default is None:
                                        new_default_1 = element_14.default
                                    else:
                                        assert_never(element_14.default)
                                    if changed_39:
                                        new_element_14 = RustConstParam(const_keyword=element_14.const_keyword, name=element_14.name, colon=element_14.colon, type_expr=new_type_expr_5, default=new_default_1)
                                        changed_36 = True
                                    else:
                                        new_element_14 = element_14
                                else:
                                    assert_never(element_14)
                                new_separator_10 = proc(separator_10)
                                assert(isinstance(new_separator_10, RustComma))
                                if new_separator_10 is not separator_10:
                                    changed_36 = True
                                new_lifetimes.append(new_element_14, new_separator_10)
                            new_last_11 = proc(element_13.bound_lifetimes.lifetimes.last)
                            assert(is_rust_generic_param(new_last_11))
                            if new_last_11 is not element_13.bound_lifetimes.lifetimes.last:
                                changed_36 = True
                            new_lifetimes.append_final(new_last_11)
                            if changed_36:
                                new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_13.bound_lifetimes.for_keyword, less_than=element_13.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_13.bound_lifetimes.greater_than)
                                changed_35 = True
                            else:
                                new_bound_lifetimes = element_13.bound_lifetimes
                        elif element_13.bound_lifetimes is None:
                            new_bound_lifetimes = element_13.bound_lifetimes
                        else:
                            assert_never(element_13.bound_lifetimes)
                        new_path_9 = proc(element_13.path)
                        assert(isinstance(new_path_9, RustPath))
                        if new_path_9 is not element_13.path:
                            changed_35 = True
                        if changed_35:
                            new_element_13 = RustTraitBound(modifier=element_13.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_9)
                            changed_34 = True
                        else:
                            new_element_13 = element_13
                    elif isinstance(element_13, RustLifetime):
                        new_element_13 = proc(element_13)
                        assert(isinstance(new_element_13, RustLifetime))
                        if new_element_13 is not element_13:
                            changed_34 = True
                    else:
                        assert_never(element_13)
                    new_separator_9 = separator_9
                    new_bounds.append(new_element_13, new_separator_9)
                new_last_10 = proc(element.bounds.last)
                assert(is_rust_type_param_bound(new_last_10))
                if new_last_10 is not element.bounds.last:
                    changed_34 = True
                new_bounds.append_final(new_last_10)
                if changed_34:
                    new_element = RustConstraint(name=element.name, generics=new_generics_2, colon=element.colon, bounds=new_bounds)
                    changed_1 = True
                else:
                    new_element = element
            else:
                assert_never(element)
            new_separator = proc(separator)
            assert(isinstance(new_separator, RustComma))
            if new_separator is not separator:
                changed_1 = True
            new_args.append(new_element, new_separator)
        new_last = proc(node.args.last)
        assert(is_rust_generic_argument(new_last))
        if new_last is not node.args.last:
            changed_1 = True
        new_args.append_final(new_last)
        if changed_1:
            rewritten = RustAngleBracketedGenericArguments(less_than=node.less_than, args=new_args, greater_than=node.greater_than)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustParenthesizedGenericArguments):
        changed_40 = False
        new_params = Punctuated()
        for (element_15, separator_11) in node.params.delimited:
            new_element_15 = proc(element_15)
            assert(is_rust_type_expr(new_element_15))
            if new_element_15 is not element_15:
                changed_40 = True
            new_separator_11 = proc(separator_11)
            assert(isinstance(new_separator_11, RustComma))
            if new_separator_11 is not separator_11:
                changed_40 = True
            new_params.append(new_element_15, new_separator_11)
        new_last_12 = proc(node.params.last)
        assert(is_rust_type_expr(new_last_12))
        if new_last_12 is not node.params.last:
            changed_40 = True
        new_params.append_final(new_last_12)
        new_result = proc(node.result)
        assert(is_rust_type_expr(new_result))
        if new_result is not node.result:
            changed_40 = True
        if changed_40:
            rewritten = RustParenthesizedGenericArguments(open_paren=node.open_paren, params=new_params, close_paren=node.close_paren, r_arrow=node.r_arrow, result=new_result)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustTurbofish):
        changed_41 = False
        new_args_3 = Punctuated()
        for (element_16, separator_12) in node.args.delimited:
            new_element_16 = proc(element_16)
            assert(is_rust_generic_argument(new_element_16))
            if new_element_16 is not element_16:
                changed_41 = True
            new_separator_12 = proc(separator_12)
            assert(isinstance(new_separator_12, RustComma))
            if new_separator_12 is not separator_12:
                changed_41 = True
            new_args_3.append(new_element_16, new_separator_12)
        new_last_13 = proc(node.args.last)
        assert(is_rust_generic_argument(new_last_13))
        if new_last_13 is not node.args.last:
            changed_41 = True
        new_args_3.append_final(new_last_13)
        if changed_41:
            rewritten = RustTurbofish(colon_colon=node.colon_colon, less_than=node.less_than, args=new_args_3, greater_than=node.greater_than)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_type_expr(node: RustTypeExpr, proc: Callable[[RustTypeExpr], RustTypeExpr]) -> RustTypeExpr:
    if isinstance(node, RustArrayTypeExpr):
        changed_1 = False
        new_type_expr = proc(node.type_expr)
        assert(is_rust_type_expr(new_type_expr))
        if new_type_expr is not node.type_expr:
            changed_1 = True
        if isinstance(node.expr, RustLitExpr):
            new_expr = node.expr
        elif isinstance(node.expr, RustPathExpr):
            changed_3 = False
            new_attrs = []
            for element in node.expr.attrs:
                changed_4 = False
                if isinstance(element.meta, RustMetaPath):
                    changed_5 = False
                    changed_6 = False
                    new_segments = Punctuated()
                    for (element_1, separator) in element.meta.path.segments.delimited:
                        changed_7 = False
                        if is_rust_path_arguments(element_1.args):
                            if isinstance(element_1.args, RustTurbofish):
                                changed_8 = False
                                new_args_1 = Punctuated()
                                for (element_2, separator_1) in element_1.args.args.delimited:
                                    if isinstance(element_2, RustLifetime):
                                        new_element_2 = element_2
                                    elif is_rust_type_expr(element_2):
                                        new_element_2 = proc(element_2)
                                        assert(is_rust_type_expr(new_element_2))
                                        if new_element_2 is not element_2:
                                            changed_8 = True
                                    elif is_rust_expr(element_2):
                                        new_element_2 = proc(element_2)
                                        assert(is_rust_expr(new_element_2))
                                        if new_element_2 is not element_2:
                                            changed_8 = True
                                    elif isinstance(element_2, RustAssocType):
                                        changed_10 = False
                                        if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                            changed_11 = False
                                            new_args_2 = Punctuated()
                                            for (element_3, separator_2) in element_2.generics.args.delimited:
                                                new_element_3 = proc(element_3)
                                                assert(is_rust_generic_argument(new_element_3))
                                                if new_element_3 is not element_3:
                                                    changed_11 = True
                                                new_separator_2 = separator_2
                                                new_args_2.append(new_element_3, new_separator_2)
                                            new_last_2 = proc(element_2.generics.args.last)
                                            assert(is_rust_generic_argument(new_last_2))
                                            if new_last_2 is not element_2.generics.args.last:
                                                changed_11 = True
                                            new_args_2.append_final(new_last_2)
                                            if changed_11:
                                                new_generics = RustAngleBracketedGenericArguments(less_than=element_2.generics.less_than, args=new_args_2, greater_than=element_2.generics.greater_than)
                                                changed_10 = True
                                            else:
                                                new_generics = element_2.generics
                                        elif element_2.generics is None:
                                            new_generics = element_2.generics
                                        else:
                                            assert_never(element_2.generics)
                                        new_type_expr_1 = proc(element_2.type_expr)
                                        assert(is_rust_type_expr(new_type_expr_1))
                                        if new_type_expr_1 is not element_2.type_expr:
                                            changed_10 = True
                                        if changed_10:
                                            new_element_2 = RustAssocType(name=element_2.name, generics=new_generics, equals=element_2.equals, type_expr=new_type_expr_1)
                                            changed_8 = True
                                        else:
                                            new_element_2 = element_2
                                    elif isinstance(element_2, RustAssocConst):
                                        changed_12 = False
                                        if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                            new_generics_1 = proc(element_2.generics)
                                            assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                            if new_generics_1 is not element_2.generics:
                                                changed_12 = True
                                        elif element_2.generics is None:
                                            new_generics_1 = element_2.generics
                                        else:
                                            assert_never(element_2.generics)
                                        new_expr_1 = proc(element_2.expr)
                                        assert(is_rust_expr(new_expr_1))
                                        if new_expr_1 is not element_2.expr:
                                            changed_12 = True
                                        if changed_12:
                                            new_element_2 = RustAssocConst(name=element_2.name, generics=new_generics_1, equals=element_2.equals, expr=new_expr_1)
                                            changed_8 = True
                                        else:
                                            new_element_2 = element_2
                                    elif isinstance(element_2, RustConstraint):
                                        changed_13 = False
                                        new_generics_2 = proc(element_2.generics)
                                        assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                                        if new_generics_2 is not element_2.generics:
                                            changed_13 = True
                                        new_bounds = Punctuated()
                                        for (element_4, separator_3) in element_2.bounds.delimited:
                                            if isinstance(element_4, RustTraitBound):
                                                changed_14 = False
                                                if isinstance(element_4.bound_lifetimes, RustBoundLifetimes):
                                                    changed_15 = False
                                                    new_lifetimes = Punctuated()
                                                    for (element_5, separator_4) in element_4.bound_lifetimes.lifetimes.delimited:
                                                        if isinstance(element_5, RustLifetime):
                                                            new_element_5 = proc(element_5)
                                                            assert(isinstance(new_element_5, RustLifetime))
                                                            if new_element_5 is not element_5:
                                                                changed_15 = True
                                                        elif isinstance(element_5, RustTypeParam):
                                                            changed_16 = False
                                                            new_type_param_bound = proc(element_5.type_param_bound)
                                                            assert(is_rust_type_param_bound(new_type_param_bound))
                                                            if new_type_param_bound is not element_5.type_param_bound:
                                                                changed_16 = True
                                                            if isinstance(element_5.default, RustTypeInit):
                                                                changed_17 = False
                                                                new_type_expr_2 = proc(element_5.default.type_expr)
                                                                assert(is_rust_type_expr(new_type_expr_2))
                                                                if new_type_expr_2 is not element_5.default.type_expr:
                                                                    changed_17 = True
                                                                if changed_17:
                                                                    new_default = RustTypeInit(equals=element_5.default.equals, type_expr=new_type_expr_2)
                                                                    changed_16 = True
                                                                else:
                                                                    new_default = element_5.default
                                                            elif element_5.default is None:
                                                                new_default = element_5.default
                                                            else:
                                                                assert_never(element_5.default)
                                                            if changed_16:
                                                                new_element_5 = RustTypeParam(name=element_5.name, colon=element_5.colon, type_param_bound=new_type_param_bound, percent=element_5.percent, plus=element_5.plus, default=new_default)
                                                                changed_15 = True
                                                            else:
                                                                new_element_5 = element_5
                                                        elif isinstance(element_5, RustConstParam):
                                                            changed_18 = False
                                                            new_type_expr_3 = proc(element_5.type_expr)
                                                            assert(is_rust_type_expr(new_type_expr_3))
                                                            if new_type_expr_3 is not element_5.type_expr:
                                                                changed_18 = True
                                                            if isinstance(element_5.default, RustInit):
                                                                changed_19 = False
                                                                new_value = proc(element_5.default.value)
                                                                assert(is_rust_expr(new_value))
                                                                if new_value is not element_5.default.value:
                                                                    changed_19 = True
                                                                if changed_19:
                                                                    new_default_1 = RustInit(name=element_5.default.name, equals=element_5.default.equals, value=new_value)
                                                                    changed_18 = True
                                                                else:
                                                                    new_default_1 = element_5.default
                                                            elif element_5.default is None:
                                                                new_default_1 = element_5.default
                                                            else:
                                                                assert_never(element_5.default)
                                                            if changed_18:
                                                                new_element_5 = RustConstParam(const_keyword=element_5.const_keyword, name=element_5.name, colon=element_5.colon, type_expr=new_type_expr_3, default=new_default_1)
                                                                changed_15 = True
                                                            else:
                                                                new_element_5 = element_5
                                                        else:
                                                            assert_never(element_5)
                                                        new_separator_4 = proc(separator_4)
                                                        assert(isinstance(new_separator_4, RustComma))
                                                        if new_separator_4 is not separator_4:
                                                            changed_15 = True
                                                        new_lifetimes.append(new_element_5, new_separator_4)
                                                    new_last_4 = proc(element_4.bound_lifetimes.lifetimes.last)
                                                    assert(is_rust_generic_param(new_last_4))
                                                    if new_last_4 is not element_4.bound_lifetimes.lifetimes.last:
                                                        changed_15 = True
                                                    new_lifetimes.append_final(new_last_4)
                                                    if changed_15:
                                                        new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_4.bound_lifetimes.for_keyword, less_than=element_4.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_4.bound_lifetimes.greater_than)
                                                        changed_14 = True
                                                    else:
                                                        new_bound_lifetimes = element_4.bound_lifetimes
                                                elif element_4.bound_lifetimes is None:
                                                    new_bound_lifetimes = element_4.bound_lifetimes
                                                else:
                                                    assert_never(element_4.bound_lifetimes)
                                                new_path_1 = proc(element_4.path)
                                                assert(isinstance(new_path_1, RustPath))
                                                if new_path_1 is not element_4.path:
                                                    changed_14 = True
                                                if changed_14:
                                                    new_element_4 = RustTraitBound(modifier=element_4.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_1)
                                                    changed_13 = True
                                                else:
                                                    new_element_4 = element_4
                                            elif isinstance(element_4, RustLifetime):
                                                new_element_4 = proc(element_4)
                                                assert(isinstance(new_element_4, RustLifetime))
                                                if new_element_4 is not element_4:
                                                    changed_13 = True
                                            else:
                                                assert_never(element_4)
                                            new_separator_3 = separator_3
                                            new_bounds.append(new_element_4, new_separator_3)
                                        new_last_3 = proc(element_2.bounds.last)
                                        assert(is_rust_type_param_bound(new_last_3))
                                        if new_last_3 is not element_2.bounds.last:
                                            changed_13 = True
                                        new_bounds.append_final(new_last_3)
                                        if changed_13:
                                            new_element_2 = RustConstraint(name=element_2.name, generics=new_generics_2, colon=element_2.colon, bounds=new_bounds)
                                            changed_8 = True
                                        else:
                                            new_element_2 = element_2
                                    else:
                                        assert_never(element_2)
                                    new_separator_1 = proc(separator_1)
                                    assert(isinstance(new_separator_1, RustComma))
                                    if new_separator_1 is not separator_1:
                                        changed_8 = True
                                    new_args_1.append(new_element_2, new_separator_1)
                                new_last_1 = proc(element_1.args.args.last)
                                assert(is_rust_generic_argument(new_last_1))
                                if new_last_1 is not element_1.args.args.last:
                                    changed_8 = True
                                new_args_1.append_final(new_last_1)
                                if changed_8:
                                    new_args = RustTurbofish(colon_colon=element_1.args.colon_colon, less_than=element_1.args.less_than, args=new_args_1, greater_than=element_1.args.greater_than)
                                    changed_7 = True
                                else:
                                    new_args = element_1.args
                            elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                new_args = proc(element_1.args)
                                assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                                if new_args is not element_1.args:
                                    changed_7 = True
                            elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                changed_20 = False
                                new_params = Punctuated()
                                for (element_6, separator_5) in element_1.args.params.delimited:
                                    new_element_6 = proc(element_6)
                                    assert(is_rust_type_expr(new_element_6))
                                    if new_element_6 is not element_6:
                                        changed_20 = True
                                    new_separator_5 = proc(separator_5)
                                    assert(isinstance(new_separator_5, RustComma))
                                    if new_separator_5 is not separator_5:
                                        changed_20 = True
                                    new_params.append(new_element_6, new_separator_5)
                                new_last_5 = proc(element_1.args.params.last)
                                assert(is_rust_type_expr(new_last_5))
                                if new_last_5 is not element_1.args.params.last:
                                    changed_20 = True
                                new_params.append_final(new_last_5)
                                new_result = proc(element_1.args.result)
                                assert(is_rust_type_expr(new_result))
                                if new_result is not element_1.args.result:
                                    changed_20 = True
                                if changed_20:
                                    new_args = RustParenthesizedGenericArguments(open_paren=element_1.args.open_paren, params=new_params, close_paren=element_1.args.close_paren, r_arrow=element_1.args.r_arrow, result=new_result)
                                    changed_7 = True
                                else:
                                    new_args = element_1.args
                            else:
                                assert_never(element_1.args)
                        elif element_1.args is None:
                            new_args = element_1.args
                        else:
                            assert_never(element_1.args)
                        if changed_7:
                            new_element_1 = RustPathSegment(name=element_1.name, args=new_args)
                            changed_6 = True
                        else:
                            new_element_1 = element_1
                        new_separator = separator
                        new_segments.append(new_element_1, new_separator)
                    new_last = proc(element.meta.path.segments.last)
                    assert(isinstance(new_last, RustPathSegment))
                    if new_last is not element.meta.path.segments.last:
                        changed_6 = True
                    new_segments.append_final(new_last)
                    if changed_6:
                        new_path = RustPath(leading_colon_colon=element.meta.path.leading_colon_colon, segments=new_segments)
                        changed_5 = True
                    else:
                        new_path = element.meta.path
                    if changed_5:
                        new_meta = RustMetaPath(path=new_path)
                        changed_4 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaParenthesized):
                    changed_21 = False
                    new_path_2 = proc(element.meta.path)
                    assert(isinstance(new_path_2, RustPath))
                    if new_path_2 is not element.meta.path:
                        changed_21 = True
                    if changed_21:
                        new_meta = RustMetaParenthesized(path=new_path_2, open_paren=element.meta.open_paren, tokens=element.meta.tokens, close_paren=element.meta.close_paren)
                        changed_4 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaBracketed):
                    changed_22 = False
                    new_path_3 = proc(element.meta.path)
                    assert(isinstance(new_path_3, RustPath))
                    if new_path_3 is not element.meta.path:
                        changed_22 = True
                    if changed_22:
                        new_meta = RustMetaBracketed(path=new_path_3, open_bracket=element.meta.open_bracket, tokens=element.meta.tokens, close_bracket=element.meta.close_bracket)
                        changed_4 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaBraced):
                    changed_23 = False
                    new_path_4 = proc(element.meta.path)
                    assert(isinstance(new_path_4, RustPath))
                    if new_path_4 is not element.meta.path:
                        changed_23 = True
                    if changed_23:
                        new_meta = RustMetaBraced(path=new_path_4, open_brace=element.meta.open_brace, tokens=element.meta.tokens, close_brace=element.meta.close_brace)
                        changed_4 = True
                    else:
                        new_meta = element.meta
                elif isinstance(element.meta, RustMetaNameValue):
                    changed_24 = False
                    new_path_5 = proc(element.meta.path)
                    assert(isinstance(new_path_5, RustPath))
                    if new_path_5 is not element.meta.path:
                        changed_24 = True
                    new_expr_2 = proc(element.meta.expr)
                    assert(is_rust_expr(new_expr_2))
                    if new_expr_2 is not element.meta.expr:
                        changed_24 = True
                    if changed_24:
                        new_meta = RustMetaNameValue(path=new_path_5, equals=element.meta.equals, expr=new_expr_2)
                        changed_4 = True
                    else:
                        new_meta = element.meta
                else:
                    assert_never(element.meta)
                if changed_4:
                    new_element = RustAttr(hashtag=element.hashtag, exclamation_mark=element.exclamation_mark, open_bracket=element.open_bracket, meta=new_meta, close_bracket=element.close_bracket)
                    changed_3 = True
                else:
                    new_element = element
                new_elements.append(new_element)
            if isinstance(node.expr.qself, RustQself):
                changed_25 = False
                new_type_expr_4 = proc(node.expr.qself.type_expr)
                assert(is_rust_type_expr(new_type_expr_4))
                if new_type_expr_4 is not node.expr.qself.type_expr:
                    changed_25 = True
                new_path_6 = proc(node.expr.qself.path)
                assert(isinstance(new_path_6, RustPath))
                if new_path_6 is not node.expr.qself.path:
                    changed_25 = True
                if changed_25:
                    new_qself = RustQself(less_than=node.expr.qself.less_than, type_expr=new_type_expr_4, as_keyword=node.expr.qself.as_keyword, path=new_path_6, greater_than=node.expr.qself.greater_than)
                    changed_3 = True
                else:
                    new_qself = node.expr.qself
            elif node.expr.qself is None:
                new_qself = node.expr.qself
            else:
                assert_never(node.expr.qself)
            new_path_7 = proc(node.expr.path)
            assert(isinstance(new_path_7, RustPath))
            if new_path_7 is not node.expr.path:
                changed_3 = True
            if changed_3:
                new_expr = RustPathExpr(attrs=new_attrs, qself=new_qself, path=new_path_7)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustCallExpr):
            changed_26 = False
            new_operator = proc(node.expr.operator)
            assert(is_rust_expr(new_operator))
            if new_operator is not node.expr.operator:
                changed_26 = True
            new_args_3 = Punctuated()
            for (element_7, separator_6) in node.expr.args.delimited:
                new_element_7 = proc(element_7)
                assert(is_rust_expr(new_element_7))
                if new_element_7 is not element_7:
                    changed_26 = True
                new_separator_6 = proc(separator_6)
                assert(isinstance(new_separator_6, RustComma))
                if new_separator_6 is not separator_6:
                    changed_26 = True
                new_args_3.append(new_element_7, new_separator_6)
            new_last_6 = proc(node.expr.args.last)
            assert(is_rust_expr(new_last_6))
            if new_last_6 is not node.expr.args.last:
                changed_26 = True
            new_args_3.append_final(new_last_6)
            if changed_26:
                new_expr = RustCallExpr(operator=new_operator, open_paren=node.expr.open_paren, args=new_args_3, close_paren=node.expr.close_paren)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustStructExpr):
            changed_27 = False
            new_path_8 = proc(node.expr.path)
            assert(isinstance(new_path_8, RustPath))
            if new_path_8 is not node.expr.path:
                changed_27 = True
            new_inits = Punctuated()
            for (element_8, separator_7) in node.expr.inits.delimited:
                new_element_8 = proc(element_8)
                assert(isinstance(new_element_8, RustInit))
                if new_element_8 is not element_8:
                    changed_27 = True
                new_separator_7 = proc(separator_7)
                assert(isinstance(new_separator_7, RustComma))
                if new_separator_7 is not separator_7:
                    changed_27 = True
                new_inits.append(new_element_8, new_separator_7)
            new_last_7 = proc(node.expr.inits.last)
            assert(isinstance(new_last_7, RustInit))
            if new_last_7 is not node.expr.inits.last:
                changed_27 = True
            new_inits.append_final(new_last_7)
            if changed_27:
                new_expr = RustStructExpr(path=new_path_8, open_brace=node.expr.open_brace, inits=new_inits, comma=node.expr.comma, close_brace=node.expr.close_brace)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustBlockExpr):
            changed_28 = False
            if isinstance(node.expr.item, RustEnumItem):
                changed_29 = False
                new_attrs_1 = []
                for element_9 in node.expr.item.attrs:
                    new_element_9 = proc(element_9)
                    assert(isinstance(new_element_9, RustAttr))
                    if new_element_9 is not element_9:
                        changed_29 = True
                    new_elements_1.append(new_element_9)
                if isinstance(node.expr.item.visibility, RustPublic):
                    changed_30 = False
                    if isinstance(node.expr.item.visibility.restrict, tuple):
                        new_elements_2 = []
                        element_0 = node.expr.item.visibility.restrict[0]
                        new_element_0 = element_0
                        new_elements_2.append(new_element_0)
                        element_1 = node.expr.item.visibility.restrict[1]
                        if isinstance(element_1, RustInKeyword):
                            new_element_1 = element_1
                        elif element_1 is None:
                            new_element_1 = element_1
                        else:
                            assert_never(element_1)
                        new_elements_2.append(new_element_1)
                        element_2 = node.expr.item.visibility.restrict[2]
                        new_element_2 = proc(element_2)
                        assert(isinstance(new_element_2, RustPath))
                        if new_element_2 is not element_2:
                            changed_30 = True
                        new_elements_2.append(new_element_2)
                        element_3 = node.expr.item.visibility.restrict[3]
                        new_element_3 = element_3
                        new_elements_2.append(new_element_3)
                        new_restrict = tuple(new_elements_2) if changed_30 else node.expr.item.visibility.restrict
                    elif node.expr.item.visibility.restrict is None:
                        new_restrict = node.expr.item.visibility.restrict
                    else:
                        assert_never(node.expr.item.visibility.restrict)
                    if changed_30:
                        new_visibility = RustPublic(pub_keyword=node.expr.item.visibility.pub_keyword, restrict=new_restrict)
                        changed_29 = True
                    else:
                        new_visibility = node.expr.item.visibility
                elif node.expr.item.visibility is None:
                    new_visibility = node.expr.item.visibility
                else:
                    assert_never(node.expr.item.visibility)
                new_variants = Punctuated()
                for (element_10, separator_8) in node.expr.item.variants.delimited:
                    if isinstance(element_10, RustStructVariant):
                        changed_31 = False
                        new_fields = Punctuated()
                        for (element_11, separator_9) in element_10.fields.delimited:
                            changed_32 = False
                            new_type_expr_5 = proc(element_11.type_expr)
                            assert(is_rust_type_expr(new_type_expr_5))
                            if new_type_expr_5 is not element_11.type_expr:
                                changed_32 = True
                            if changed_32:
                                new_element_11 = RustField(name=element_11.name, colon=element_11.colon, type_expr=new_type_expr_5)
                                changed_31 = True
                            else:
                                new_element_11 = element_11
                            new_separator_9 = proc(separator_9)
                            assert(isinstance(new_separator_9, RustComma))
                            if new_separator_9 is not separator_9:
                                changed_31 = True
                            new_fields.append(new_element_11, new_separator_9)
                        new_last_9 = proc(element_10.fields.last)
                        assert(isinstance(new_last_9, RustField))
                        if new_last_9 is not element_10.fields.last:
                            changed_31 = True
                        new_fields.append_final(new_last_9)
                        if changed_31:
                            new_element_10 = RustStructVariant(name=element_10.name, open_brace=element_10.open_brace, fields=new_fields, comma=element_10.comma, close_brace=element_10.close_brace)
                            changed_29 = True
                        else:
                            new_element_10 = element_10
                    elif isinstance(element_10, RustTupleVariant):
                        changed_33 = False
                        new_types = Punctuated()
                        for (element_12, separator_10) in element_10.types.delimited:
                            new_element_12 = proc(element_12)
                            assert(is_rust_type_expr(new_element_12))
                            if new_element_12 is not element_12:
                                changed_33 = True
                            new_separator_10 = proc(separator_10)
                            assert(isinstance(new_separator_10, RustComma))
                            if new_separator_10 is not separator_10:
                                changed_33 = True
                            new_types.append(new_element_12, new_separator_10)
                        new_last_10 = proc(element_10.types.last)
                        assert(is_rust_type_expr(new_last_10))
                        if new_last_10 is not element_10.types.last:
                            changed_33 = True
                        new_types.append_final(new_last_10)
                        if changed_33:
                            new_element_10 = RustTupleVariant(name=element_10.name, open_paren=element_10.open_paren, types=new_types, close_paren=element_10.close_paren)
                            changed_29 = True
                        else:
                            new_element_10 = element_10
                    elif isinstance(element_10, RustEmptyVariant):
                        changed_34 = False
                        if isinstance(element_10.init, RustInit):
                            new_init = proc(element_10.init)
                            assert(isinstance(new_init, RustInit))
                            if new_init is not element_10.init:
                                changed_34 = True
                        elif element_10.init is None:
                            new_init = element_10.init
                        else:
                            assert_never(element_10.init)
                        if changed_34:
                            new_element_10 = RustEmptyVariant(name=element_10.name, init=new_init)
                            changed_29 = True
                        else:
                            new_element_10 = element_10
                    else:
                        assert_never(element_10)
                    new_separator_8 = proc(separator_8)
                    assert(isinstance(new_separator_8, RustComma))
                    if new_separator_8 is not separator_8:
                        changed_29 = True
                    new_variants.append(new_element_10, new_separator_8)
                new_last_8 = proc(node.expr.item.variants.last)
                assert(is_rust_variant(new_last_8))
                if new_last_8 is not node.expr.item.variants.last:
                    changed_29 = True
                new_variants.append_final(new_last_8)
                if changed_29:
                    new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=node.expr.item.enum_keyword, name=node.expr.item.name, open_brace=node.expr.item.open_brace, variants=new_variants, comma=node.expr.item.comma, close_brace=node.expr.item.close_brace)
                    changed_28 = True
                else:
                    new_item = node.expr.item
            elif isinstance(node.expr.item, RustStructItem):
                changed_35 = False
                new_attrs_2 = []
                for element_13 in node.expr.item.attrs:
                    new_element_13 = proc(element_13)
                    assert(isinstance(new_element_13, RustAttr))
                    if new_element_13 is not element_13:
                        changed_35 = True
                    new_elements_3.append(new_element_13)
                if isinstance(node.expr.item.visibility, RustPublic):
                    new_visibility_1 = proc(node.expr.item.visibility)
                    assert(isinstance(new_visibility_1, RustPublic))
                    if new_visibility_1 is not node.expr.item.visibility:
                        changed_35 = True
                elif node.expr.item.visibility is None:
                    new_visibility_1 = node.expr.item.visibility
                else:
                    assert_never(node.expr.item.visibility)
                new_fields_1 = Punctuated()
                for (element_14, separator_11) in node.expr.item.fields.delimited:
                    new_element_14 = proc(element_14)
                    assert(isinstance(new_element_14, RustField))
                    if new_element_14 is not element_14:
                        changed_35 = True
                    new_separator_11 = proc(separator_11)
                    assert(isinstance(new_separator_11, RustComma))
                    if new_separator_11 is not separator_11:
                        changed_35 = True
                    new_fields_1.append(new_element_14, new_separator_11)
                new_last_11 = proc(node.expr.item.fields.last)
                assert(isinstance(new_last_11, RustField))
                if new_last_11 is not node.expr.item.fields.last:
                    changed_35 = True
                new_fields_1.append_final(new_last_11)
                if changed_35:
                    new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=node.expr.item.struct_keyword, name=node.expr.item.name, open_brace=node.expr.item.open_brace, fields=new_fields_1, comma=node.expr.item.comma, close_brace=node.expr.item.close_brace)
                    changed_28 = True
                else:
                    new_item = node.expr.item
            elif isinstance(node.expr.item, RustUseItem):
                changed_36 = False
                new_attrs_3 = []
                for element_15 in node.expr.item.attrs:
                    new_element_15 = proc(element_15)
                    assert(isinstance(new_element_15, RustAttr))
                    if new_element_15 is not element_15:
                        changed_36 = True
                    new_elements_4.append(new_element_15)
                if isinstance(node.expr.item.visibility, RustPublic):
                    new_visibility_2 = proc(node.expr.item.visibility)
                    assert(isinstance(new_visibility_2, RustPublic))
                    if new_visibility_2 is not node.expr.item.visibility:
                        changed_36 = True
                elif node.expr.item.visibility is None:
                    new_visibility_2 = node.expr.item.visibility
                else:
                    assert_never(node.expr.item.visibility)
                if changed_36:
                    new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=node.expr.item.use_keyword, colon_colon=node.expr.item.colon_colon, path=node.expr.item.path, semicolon=node.expr.item.semicolon)
                    changed_28 = True
                else:
                    new_item = node.expr.item
            elif isinstance(node.expr.item, RustExprItem):
                changed_37 = False
                new_expr_3 = proc(node.expr.item.expr)
                assert(is_rust_expr(new_expr_3))
                if new_expr_3 is not node.expr.item.expr:
                    changed_37 = True
                if changed_37:
                    new_item = RustExprItem(expr=new_expr_3)
                    changed_28 = True
                else:
                    new_item = node.expr.item
            else:
                assert_never(node.expr.item)
            new_last_12 = proc(node.expr.last)
            assert(is_rust_expr(new_last_12))
            if new_last_12 is not node.expr.last:
                changed_28 = True
            if changed_28:
                new_expr = RustBlockExpr(open_brace=node.expr.open_brace, item=new_item, semicolon=node.expr.semicolon, last=new_last_12, close_brace=node.expr.close_brace)
                changed_1 = True
            else:
                new_expr = node.expr
        elif isinstance(node.expr, RustRetExpr):
            changed_38 = False
            new_expr_4 = proc(node.expr.expr)
            assert(is_rust_expr(new_expr_4))
            if new_expr_4 is not node.expr.expr:
                changed_38 = True
            if changed_38:
                new_expr = RustRetExpr(return_keyword=node.expr.return_keyword, expr=new_expr_4)
                changed_1 = True
            else:
                new_expr = node.expr
        else:
            assert_never(node.expr)
        if changed_1:
            rewritten = RustArrayTypeExpr(open_bracket=node.open_bracket, type_expr=new_type_expr, semicolon=node.semicolon, expr=new_expr, close_bracket=node.close_bracket)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustNeverTypeExpr):
        rewritten = node
    elif isinstance(node, RustPathTypeExpr):
        changed_40 = False
        if isinstance(node.qself, RustQself):
            new_qself_1 = proc(node.qself)
            assert(isinstance(new_qself_1, RustQself))
            if new_qself_1 is not node.qself:
                changed_40 = True
        elif node.qself is None:
            new_qself_1 = node.qself
        else:
            assert_never(node.qself)
        new_path_9 = proc(node.path)
        assert(isinstance(new_path_9, RustPath))
        if new_path_9 is not node.path:
            changed_40 = True
        if changed_40:
            rewritten = RustPathTypeExpr(qself=new_qself_1, path=new_path_9)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustTupleTypeExpr):
        changed_41 = False
        new_elements_5 = Punctuated()
        for (element_16, separator_12) in node.elements.delimited:
            new_element_16 = proc(element_16)
            assert(is_rust_type_expr(new_element_16))
            if new_element_16 is not element_16:
                changed_41 = True
            new_separator_12 = proc(separator_12)
            assert(isinstance(new_separator_12, RustComma))
            if new_separator_12 is not separator_12:
                changed_41 = True
            new_elements_5.append(new_element_16, new_separator_12)
        new_last_13 = proc(node.elements.last)
        assert(is_rust_type_expr(new_last_13))
        if new_last_13 is not node.elements.last:
            changed_41 = True
        new_elements_5.append_final(new_last_13)
        if changed_41:
            rewritten = RustTupleTypeExpr(open_paren=node.open_paren, elements=new_elements_5, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_type_param_bound(node: RustTypeParamBound, proc: Callable[[RustTypeParamBound], RustTypeParamBound]) -> RustTypeParamBound:
    if isinstance(node, RustLifetime):
        rewritten = node
    elif isinstance(node, RustTraitBound):
        changed_2 = False
        if isinstance(node.bound_lifetimes, RustBoundLifetimes):
            changed_3 = False
            new_lifetimes = Punctuated()
            for (element, separator) in node.bound_lifetimes.lifetimes.delimited:
                if isinstance(element, RustLifetime):
                    new_element = proc(element)
                    assert(isinstance(new_element, RustLifetime))
                    if new_element is not element:
                        changed_3 = True
                elif isinstance(element, RustTypeParam):
                    changed_4 = False
                    new_type_param_bound = proc(element.type_param_bound)
                    assert(is_rust_type_param_bound(new_type_param_bound))
                    if new_type_param_bound is not element.type_param_bound:
                        changed_4 = True
                    if isinstance(element.default, RustTypeInit):
                        changed_5 = False
                        if isinstance(element.default.type_expr, RustPathTypeExpr):
                            changed_6 = False
                            if isinstance(element.default.type_expr.qself, RustQself):
                                changed_7 = False
                                new_type_expr_1 = proc(element.default.type_expr.qself.type_expr)
                                assert(is_rust_type_expr(new_type_expr_1))
                                if new_type_expr_1 is not element.default.type_expr.qself.type_expr:
                                    changed_7 = True
                                changed_8 = False
                                new_segments = Punctuated()
                                for (element_1, separator_1) in element.default.type_expr.qself.path.segments.delimited:
                                    changed_9 = False
                                    if is_rust_path_arguments(element_1.args):
                                        if isinstance(element_1.args, RustTurbofish):
                                            changed_10 = False
                                            new_args_1 = Punctuated()
                                            for (element_2, separator_2) in element_1.args.args.delimited:
                                                if isinstance(element_2, RustLifetime):
                                                    new_element_2 = proc(element_2)
                                                    assert(isinstance(new_element_2, RustLifetime))
                                                    if new_element_2 is not element_2:
                                                        changed_10 = True
                                                elif is_rust_type_expr(element_2):
                                                    new_element_2 = proc(element_2)
                                                    assert(is_rust_type_expr(new_element_2))
                                                    if new_element_2 is not element_2:
                                                        changed_10 = True
                                                elif is_rust_expr(element_2):
                                                    if isinstance(element_2, RustLitExpr):
                                                        new_element_2 = element_2
                                                    elif isinstance(element_2, RustPathExpr):
                                                        changed_12 = False
                                                        new_attrs = []
                                                        for element_3 in element_2.attrs:
                                                            changed_13 = False
                                                            if isinstance(element_3.meta, RustMetaPath):
                                                                changed_14 = False
                                                                new_path_1 = proc(element_3.meta.path)
                                                                assert(isinstance(new_path_1, RustPath))
                                                                if new_path_1 is not element_3.meta.path:
                                                                    changed_14 = True
                                                                if changed_14:
                                                                    new_meta = RustMetaPath(path=new_path_1)
                                                                    changed_13 = True
                                                                else:
                                                                    new_meta = element_3.meta
                                                            elif isinstance(element_3.meta, RustMetaParenthesized):
                                                                changed_15 = False
                                                                new_path_2 = proc(element_3.meta.path)
                                                                assert(isinstance(new_path_2, RustPath))
                                                                if new_path_2 is not element_3.meta.path:
                                                                    changed_15 = True
                                                                if changed_15:
                                                                    new_meta = RustMetaParenthesized(path=new_path_2, open_paren=element_3.meta.open_paren, tokens=element_3.meta.tokens, close_paren=element_3.meta.close_paren)
                                                                    changed_13 = True
                                                                else:
                                                                    new_meta = element_3.meta
                                                            elif isinstance(element_3.meta, RustMetaBracketed):
                                                                changed_16 = False
                                                                new_path_3 = proc(element_3.meta.path)
                                                                assert(isinstance(new_path_3, RustPath))
                                                                if new_path_3 is not element_3.meta.path:
                                                                    changed_16 = True
                                                                if changed_16:
                                                                    new_meta = RustMetaBracketed(path=new_path_3, open_bracket=element_3.meta.open_bracket, tokens=element_3.meta.tokens, close_bracket=element_3.meta.close_bracket)
                                                                    changed_13 = True
                                                                else:
                                                                    new_meta = element_3.meta
                                                            elif isinstance(element_3.meta, RustMetaBraced):
                                                                changed_17 = False
                                                                new_path_4 = proc(element_3.meta.path)
                                                                assert(isinstance(new_path_4, RustPath))
                                                                if new_path_4 is not element_3.meta.path:
                                                                    changed_17 = True
                                                                if changed_17:
                                                                    new_meta = RustMetaBraced(path=new_path_4, open_brace=element_3.meta.open_brace, tokens=element_3.meta.tokens, close_brace=element_3.meta.close_brace)
                                                                    changed_13 = True
                                                                else:
                                                                    new_meta = element_3.meta
                                                            elif isinstance(element_3.meta, RustMetaNameValue):
                                                                changed_18 = False
                                                                new_path_5 = proc(element_3.meta.path)
                                                                assert(isinstance(new_path_5, RustPath))
                                                                if new_path_5 is not element_3.meta.path:
                                                                    changed_18 = True
                                                                new_expr = proc(element_3.meta.expr)
                                                                assert(is_rust_expr(new_expr))
                                                                if new_expr is not element_3.meta.expr:
                                                                    changed_18 = True
                                                                if changed_18:
                                                                    new_meta = RustMetaNameValue(path=new_path_5, equals=element_3.meta.equals, expr=new_expr)
                                                                    changed_13 = True
                                                                else:
                                                                    new_meta = element_3.meta
                                                            else:
                                                                assert_never(element_3.meta)
                                                            if changed_13:
                                                                new_element_3 = RustAttr(hashtag=element_3.hashtag, exclamation_mark=element_3.exclamation_mark, open_bracket=element_3.open_bracket, meta=new_meta, close_bracket=element_3.close_bracket)
                                                                changed_12 = True
                                                            else:
                                                                new_element_3 = element_3
                                                            new_elements.append(new_element_3)
                                                        if isinstance(element_2.qself, RustQself):
                                                            new_qself_1 = proc(element_2.qself)
                                                            assert(isinstance(new_qself_1, RustQself))
                                                            if new_qself_1 is not element_2.qself:
                                                                changed_12 = True
                                                        elif element_2.qself is None:
                                                            new_qself_1 = element_2.qself
                                                        else:
                                                            assert_never(element_2.qself)
                                                        new_path_6 = proc(element_2.path)
                                                        assert(isinstance(new_path_6, RustPath))
                                                        if new_path_6 is not element_2.path:
                                                            changed_12 = True
                                                        if changed_12:
                                                            new_element_2 = RustPathExpr(attrs=new_attrs, qself=new_qself_1, path=new_path_6)
                                                            changed_10 = True
                                                        else:
                                                            new_element_2 = element_2
                                                    elif isinstance(element_2, RustCallExpr):
                                                        changed_19 = False
                                                        new_operator = proc(element_2.operator)
                                                        assert(is_rust_expr(new_operator))
                                                        if new_operator is not element_2.operator:
                                                            changed_19 = True
                                                        new_args_2 = Punctuated()
                                                        for (element_4, separator_3) in element_2.args.delimited:
                                                            new_element_4 = proc(element_4)
                                                            assert(is_rust_expr(new_element_4))
                                                            if new_element_4 is not element_4:
                                                                changed_19 = True
                                                            new_separator_3 = separator_3
                                                            new_args_2.append(new_element_4, new_separator_3)
                                                        new_last_3 = proc(element_2.args.last)
                                                        assert(is_rust_expr(new_last_3))
                                                        if new_last_3 is not element_2.args.last:
                                                            changed_19 = True
                                                        new_args_2.append_final(new_last_3)
                                                        if changed_19:
                                                            new_element_2 = RustCallExpr(operator=new_operator, open_paren=element_2.open_paren, args=new_args_2, close_paren=element_2.close_paren)
                                                            changed_10 = True
                                                        else:
                                                            new_element_2 = element_2
                                                    elif isinstance(element_2, RustStructExpr):
                                                        changed_20 = False
                                                        new_path_7 = proc(element_2.path)
                                                        assert(isinstance(new_path_7, RustPath))
                                                        if new_path_7 is not element_2.path:
                                                            changed_20 = True
                                                        new_inits = Punctuated()
                                                        for (element_5, separator_4) in element_2.inits.delimited:
                                                            changed_21 = False
                                                            new_value = proc(element_5.value)
                                                            assert(is_rust_expr(new_value))
                                                            if new_value is not element_5.value:
                                                                changed_21 = True
                                                            if changed_21:
                                                                new_element_5 = RustInit(name=element_5.name, equals=element_5.equals, value=new_value)
                                                                changed_20 = True
                                                            else:
                                                                new_element_5 = element_5
                                                            new_separator_4 = proc(separator_4)
                                                            assert(isinstance(new_separator_4, RustComma))
                                                            if new_separator_4 is not separator_4:
                                                                changed_20 = True
                                                            new_inits.append(new_element_5, new_separator_4)
                                                        new_last_4 = proc(element_2.inits.last)
                                                        assert(isinstance(new_last_4, RustInit))
                                                        if new_last_4 is not element_2.inits.last:
                                                            changed_20 = True
                                                        new_inits.append_final(new_last_4)
                                                        if changed_20:
                                                            new_element_2 = RustStructExpr(path=new_path_7, open_brace=element_2.open_brace, inits=new_inits, comma=element_2.comma, close_brace=element_2.close_brace)
                                                            changed_10 = True
                                                        else:
                                                            new_element_2 = element_2
                                                    elif isinstance(element_2, RustBlockExpr):
                                                        changed_22 = False
                                                        if isinstance(element_2.item, RustEnumItem):
                                                            changed_23 = False
                                                            new_attrs_1 = []
                                                            for element_6 in element_2.item.attrs:
                                                                new_element_6 = proc(element_6)
                                                                assert(isinstance(new_element_6, RustAttr))
                                                                if new_element_6 is not element_6:
                                                                    changed_23 = True
                                                                new_elements_1.append(new_element_6)
                                                            if isinstance(element_2.item.visibility, RustPublic):
                                                                changed_24 = False
                                                                if isinstance(element_2.item.visibility.restrict, tuple):
                                                                    new_elements_2 = []
                                                                    element_0 = element_2.item.visibility.restrict[0]
                                                                    new_element_0 = element_0
                                                                    new_elements_2.append(new_element_0)
                                                                    element_1 = element_2.item.visibility.restrict[1]
                                                                    if isinstance(element_1, RustInKeyword):
                                                                        new_element_1 = element_1
                                                                    elif element_1 is None:
                                                                        new_element_1 = element_1
                                                                    else:
                                                                        assert_never(element_1)
                                                                    new_elements_2.append(new_element_1)
                                                                    element_2 = element_2.item.visibility.restrict[2]
                                                                    new_element_2 = proc(element_2)
                                                                    assert(isinstance(new_element_2, RustPath))
                                                                    if new_element_2 is not element_2:
                                                                        changed_24 = True
                                                                    new_elements_2.append(new_element_2)
                                                                    element_3 = element_2.item.visibility.restrict[3]
                                                                    new_element_3 = element_3
                                                                    new_elements_2.append(new_element_3)
                                                                    new_restrict = tuple(new_elements_2) if changed_24 else element_2.item.visibility.restrict
                                                                elif element_2.item.visibility.restrict is None:
                                                                    new_restrict = element_2.item.visibility.restrict
                                                                else:
                                                                    assert_never(element_2.item.visibility.restrict)
                                                                if changed_24:
                                                                    new_visibility = RustPublic(pub_keyword=element_2.item.visibility.pub_keyword, restrict=new_restrict)
                                                                    changed_23 = True
                                                                else:
                                                                    new_visibility = element_2.item.visibility
                                                            elif element_2.item.visibility is None:
                                                                new_visibility = element_2.item.visibility
                                                            else:
                                                                assert_never(element_2.item.visibility)
                                                            new_variants = Punctuated()
                                                            for (element_7, separator_5) in element_2.item.variants.delimited:
                                                                if isinstance(element_7, RustStructVariant):
                                                                    changed_25 = False
                                                                    new_fields = Punctuated()
                                                                    for (element_8, separator_6) in element_7.fields.delimited:
                                                                        changed_26 = False
                                                                        new_type_expr_2 = proc(element_8.type_expr)
                                                                        assert(is_rust_type_expr(new_type_expr_2))
                                                                        if new_type_expr_2 is not element_8.type_expr:
                                                                            changed_26 = True
                                                                        if changed_26:
                                                                            new_element_8 = RustField(name=element_8.name, colon=element_8.colon, type_expr=new_type_expr_2)
                                                                            changed_25 = True
                                                                        else:
                                                                            new_element_8 = element_8
                                                                        new_separator_6 = proc(separator_6)
                                                                        assert(isinstance(new_separator_6, RustComma))
                                                                        if new_separator_6 is not separator_6:
                                                                            changed_25 = True
                                                                        new_fields.append(new_element_8, new_separator_6)
                                                                    new_last_6 = proc(element_7.fields.last)
                                                                    assert(isinstance(new_last_6, RustField))
                                                                    if new_last_6 is not element_7.fields.last:
                                                                        changed_25 = True
                                                                    new_fields.append_final(new_last_6)
                                                                    if changed_25:
                                                                        new_element_7 = RustStructVariant(name=element_7.name, open_brace=element_7.open_brace, fields=new_fields, comma=element_7.comma, close_brace=element_7.close_brace)
                                                                        changed_23 = True
                                                                    else:
                                                                        new_element_7 = element_7
                                                                elif isinstance(element_7, RustTupleVariant):
                                                                    changed_27 = False
                                                                    new_types = Punctuated()
                                                                    for (element_9, separator_7) in element_7.types.delimited:
                                                                        new_element_9 = proc(element_9)
                                                                        assert(is_rust_type_expr(new_element_9))
                                                                        if new_element_9 is not element_9:
                                                                            changed_27 = True
                                                                        new_separator_7 = proc(separator_7)
                                                                        assert(isinstance(new_separator_7, RustComma))
                                                                        if new_separator_7 is not separator_7:
                                                                            changed_27 = True
                                                                        new_types.append(new_element_9, new_separator_7)
                                                                    new_last_7 = proc(element_7.types.last)
                                                                    assert(is_rust_type_expr(new_last_7))
                                                                    if new_last_7 is not element_7.types.last:
                                                                        changed_27 = True
                                                                    new_types.append_final(new_last_7)
                                                                    if changed_27:
                                                                        new_element_7 = RustTupleVariant(name=element_7.name, open_paren=element_7.open_paren, types=new_types, close_paren=element_7.close_paren)
                                                                        changed_23 = True
                                                                    else:
                                                                        new_element_7 = element_7
                                                                elif isinstance(element_7, RustEmptyVariant):
                                                                    changed_28 = False
                                                                    if isinstance(element_7.init, RustInit):
                                                                        new_init = proc(element_7.init)
                                                                        assert(isinstance(new_init, RustInit))
                                                                        if new_init is not element_7.init:
                                                                            changed_28 = True
                                                                    elif element_7.init is None:
                                                                        new_init = element_7.init
                                                                    else:
                                                                        assert_never(element_7.init)
                                                                    if changed_28:
                                                                        new_element_7 = RustEmptyVariant(name=element_7.name, init=new_init)
                                                                        changed_23 = True
                                                                    else:
                                                                        new_element_7 = element_7
                                                                else:
                                                                    assert_never(element_7)
                                                                new_separator_5 = proc(separator_5)
                                                                assert(isinstance(new_separator_5, RustComma))
                                                                if new_separator_5 is not separator_5:
                                                                    changed_23 = True
                                                                new_variants.append(new_element_7, new_separator_5)
                                                            new_last_5 = proc(element_2.item.variants.last)
                                                            assert(is_rust_variant(new_last_5))
                                                            if new_last_5 is not element_2.item.variants.last:
                                                                changed_23 = True
                                                            new_variants.append_final(new_last_5)
                                                            if changed_23:
                                                                new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=element_2.item.enum_keyword, name=element_2.item.name, open_brace=element_2.item.open_brace, variants=new_variants, comma=element_2.item.comma, close_brace=element_2.item.close_brace)
                                                                changed_22 = True
                                                            else:
                                                                new_item = element_2.item
                                                        elif isinstance(element_2.item, RustStructItem):
                                                            changed_29 = False
                                                            new_attrs_2 = []
                                                            for element_10 in element_2.item.attrs:
                                                                new_element_10 = proc(element_10)
                                                                assert(isinstance(new_element_10, RustAttr))
                                                                if new_element_10 is not element_10:
                                                                    changed_29 = True
                                                                new_elements_3.append(new_element_10)
                                                            if isinstance(element_2.item.visibility, RustPublic):
                                                                new_visibility_1 = proc(element_2.item.visibility)
                                                                assert(isinstance(new_visibility_1, RustPublic))
                                                                if new_visibility_1 is not element_2.item.visibility:
                                                                    changed_29 = True
                                                            elif element_2.item.visibility is None:
                                                                new_visibility_1 = element_2.item.visibility
                                                            else:
                                                                assert_never(element_2.item.visibility)
                                                            new_fields_1 = Punctuated()
                                                            for (element_11, separator_8) in element_2.item.fields.delimited:
                                                                new_element_11 = proc(element_11)
                                                                assert(isinstance(new_element_11, RustField))
                                                                if new_element_11 is not element_11:
                                                                    changed_29 = True
                                                                new_separator_8 = proc(separator_8)
                                                                assert(isinstance(new_separator_8, RustComma))
                                                                if new_separator_8 is not separator_8:
                                                                    changed_29 = True
                                                                new_fields_1.append(new_element_11, new_separator_8)
                                                            new_last_8 = proc(element_2.item.fields.last)
                                                            assert(isinstance(new_last_8, RustField))
                                                            if new_last_8 is not element_2.item.fields.last:
                                                                changed_29 = True
                                                            new_fields_1.append_final(new_last_8)
                                                            if changed_29:
                                                                new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=element_2.item.struct_keyword, name=element_2.item.name, open_brace=element_2.item.open_brace, fields=new_fields_1, comma=element_2.item.comma, close_brace=element_2.item.close_brace)
                                                                changed_22 = True
                                                            else:
                                                                new_item = element_2.item
                                                        elif isinstance(element_2.item, RustUseItem):
                                                            changed_30 = False
                                                            new_attrs_3 = []
                                                            for element_12 in element_2.item.attrs:
                                                                new_element_12 = proc(element_12)
                                                                assert(isinstance(new_element_12, RustAttr))
                                                                if new_element_12 is not element_12:
                                                                    changed_30 = True
                                                                new_elements_4.append(new_element_12)
                                                            if isinstance(element_2.item.visibility, RustPublic):
                                                                new_visibility_2 = proc(element_2.item.visibility)
                                                                assert(isinstance(new_visibility_2, RustPublic))
                                                                if new_visibility_2 is not element_2.item.visibility:
                                                                    changed_30 = True
                                                            elif element_2.item.visibility is None:
                                                                new_visibility_2 = element_2.item.visibility
                                                            else:
                                                                assert_never(element_2.item.visibility)
                                                            if changed_30:
                                                                new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=element_2.item.use_keyword, colon_colon=element_2.item.colon_colon, path=element_2.item.path, semicolon=element_2.item.semicolon)
                                                                changed_22 = True
                                                            else:
                                                                new_item = element_2.item
                                                        elif isinstance(element_2.item, RustExprItem):
                                                            changed_31 = False
                                                            new_expr_1 = proc(element_2.item.expr)
                                                            assert(is_rust_expr(new_expr_1))
                                                            if new_expr_1 is not element_2.item.expr:
                                                                changed_31 = True
                                                            if changed_31:
                                                                new_item = RustExprItem(expr=new_expr_1)
                                                                changed_22 = True
                                                            else:
                                                                new_item = element_2.item
                                                        else:
                                                            assert_never(element_2.item)
                                                        new_last_9 = proc(element_2.last)
                                                        assert(is_rust_expr(new_last_9))
                                                        if new_last_9 is not element_2.last:
                                                            changed_22 = True
                                                        if changed_22:
                                                            new_element_2 = RustBlockExpr(open_brace=element_2.open_brace, item=new_item, semicolon=element_2.semicolon, last=new_last_9, close_brace=element_2.close_brace)
                                                            changed_10 = True
                                                        else:
                                                            new_element_2 = element_2
                                                    elif isinstance(element_2, RustRetExpr):
                                                        changed_32 = False
                                                        new_expr_2 = proc(element_2.expr)
                                                        assert(is_rust_expr(new_expr_2))
                                                        if new_expr_2 is not element_2.expr:
                                                            changed_32 = True
                                                        if changed_32:
                                                            new_element_2 = RustRetExpr(return_keyword=element_2.return_keyword, expr=new_expr_2)
                                                            changed_10 = True
                                                        else:
                                                            new_element_2 = element_2
                                                    else:
                                                        assert_never(element_2)
                                                elif isinstance(element_2, RustAssocType):
                                                    changed_33 = False
                                                    if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                                        changed_34 = False
                                                        new_args_3 = Punctuated()
                                                        for (element_13, separator_9) in element_2.generics.args.delimited:
                                                            new_element_13 = proc(element_13)
                                                            assert(is_rust_generic_argument(new_element_13))
                                                            if new_element_13 is not element_13:
                                                                changed_34 = True
                                                            new_separator_9 = proc(separator_9)
                                                            assert(isinstance(new_separator_9, RustComma))
                                                            if new_separator_9 is not separator_9:
                                                                changed_34 = True
                                                            new_args_3.append(new_element_13, new_separator_9)
                                                        new_last_10 = proc(element_2.generics.args.last)
                                                        assert(is_rust_generic_argument(new_last_10))
                                                        if new_last_10 is not element_2.generics.args.last:
                                                            changed_34 = True
                                                        new_args_3.append_final(new_last_10)
                                                        if changed_34:
                                                            new_generics = RustAngleBracketedGenericArguments(less_than=element_2.generics.less_than, args=new_args_3, greater_than=element_2.generics.greater_than)
                                                            changed_33 = True
                                                        else:
                                                            new_generics = element_2.generics
                                                    elif element_2.generics is None:
                                                        new_generics = element_2.generics
                                                    else:
                                                        assert_never(element_2.generics)
                                                    new_type_expr_3 = proc(element_2.type_expr)
                                                    assert(is_rust_type_expr(new_type_expr_3))
                                                    if new_type_expr_3 is not element_2.type_expr:
                                                        changed_33 = True
                                                    if changed_33:
                                                        new_element_2 = RustAssocType(name=element_2.name, generics=new_generics, equals=element_2.equals, type_expr=new_type_expr_3)
                                                        changed_10 = True
                                                    else:
                                                        new_element_2 = element_2
                                                elif isinstance(element_2, RustAssocConst):
                                                    changed_35 = False
                                                    if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                                        new_generics_1 = proc(element_2.generics)
                                                        assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                                        if new_generics_1 is not element_2.generics:
                                                            changed_35 = True
                                                    elif element_2.generics is None:
                                                        new_generics_1 = element_2.generics
                                                    else:
                                                        assert_never(element_2.generics)
                                                    new_expr_3 = proc(element_2.expr)
                                                    assert(is_rust_expr(new_expr_3))
                                                    if new_expr_3 is not element_2.expr:
                                                        changed_35 = True
                                                    if changed_35:
                                                        new_element_2 = RustAssocConst(name=element_2.name, generics=new_generics_1, equals=element_2.equals, expr=new_expr_3)
                                                        changed_10 = True
                                                    else:
                                                        new_element_2 = element_2
                                                elif isinstance(element_2, RustConstraint):
                                                    changed_36 = False
                                                    new_generics_2 = proc(element_2.generics)
                                                    assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                                                    if new_generics_2 is not element_2.generics:
                                                        changed_36 = True
                                                    new_bounds = Punctuated()
                                                    for (element_14, separator_10) in element_2.bounds.delimited:
                                                        new_element_14 = proc(element_14)
                                                        assert(is_rust_type_param_bound(new_element_14))
                                                        if new_element_14 is not element_14:
                                                            changed_36 = True
                                                        new_separator_10 = separator_10
                                                        new_bounds.append(new_element_14, new_separator_10)
                                                    new_last_11 = proc(element_2.bounds.last)
                                                    assert(is_rust_type_param_bound(new_last_11))
                                                    if new_last_11 is not element_2.bounds.last:
                                                        changed_36 = True
                                                    new_bounds.append_final(new_last_11)
                                                    if changed_36:
                                                        new_element_2 = RustConstraint(name=element_2.name, generics=new_generics_2, colon=element_2.colon, bounds=new_bounds)
                                                        changed_10 = True
                                                    else:
                                                        new_element_2 = element_2
                                                else:
                                                    assert_never(element_2)
                                                new_separator_2 = proc(separator_2)
                                                assert(isinstance(new_separator_2, RustComma))
                                                if new_separator_2 is not separator_2:
                                                    changed_10 = True
                                                new_args_1.append(new_element_2, new_separator_2)
                                            new_last_2 = proc(element_1.args.args.last)
                                            assert(is_rust_generic_argument(new_last_2))
                                            if new_last_2 is not element_1.args.args.last:
                                                changed_10 = True
                                            new_args_1.append_final(new_last_2)
                                            if changed_10:
                                                new_args = RustTurbofish(colon_colon=element_1.args.colon_colon, less_than=element_1.args.less_than, args=new_args_1, greater_than=element_1.args.greater_than)
                                                changed_9 = True
                                            else:
                                                new_args = element_1.args
                                        elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                            new_args = proc(element_1.args)
                                            assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                                            if new_args is not element_1.args:
                                                changed_9 = True
                                        elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                            changed_37 = False
                                            new_params = Punctuated()
                                            for (element_15, separator_11) in element_1.args.params.delimited:
                                                new_element_15 = proc(element_15)
                                                assert(is_rust_type_expr(new_element_15))
                                                if new_element_15 is not element_15:
                                                    changed_37 = True
                                                new_separator_11 = proc(separator_11)
                                                assert(isinstance(new_separator_11, RustComma))
                                                if new_separator_11 is not separator_11:
                                                    changed_37 = True
                                                new_params.append(new_element_15, new_separator_11)
                                            new_last_12 = proc(element_1.args.params.last)
                                            assert(is_rust_type_expr(new_last_12))
                                            if new_last_12 is not element_1.args.params.last:
                                                changed_37 = True
                                            new_params.append_final(new_last_12)
                                            new_result = proc(element_1.args.result)
                                            assert(is_rust_type_expr(new_result))
                                            if new_result is not element_1.args.result:
                                                changed_37 = True
                                            if changed_37:
                                                new_args = RustParenthesizedGenericArguments(open_paren=element_1.args.open_paren, params=new_params, close_paren=element_1.args.close_paren, r_arrow=element_1.args.r_arrow, result=new_result)
                                                changed_9 = True
                                            else:
                                                new_args = element_1.args
                                        else:
                                            assert_never(element_1.args)
                                    elif element_1.args is None:
                                        new_args = element_1.args
                                    else:
                                        assert_never(element_1.args)
                                    if changed_9:
                                        new_element_1 = RustPathSegment(name=element_1.name, args=new_args)
                                        changed_8 = True
                                    else:
                                        new_element_1 = element_1
                                    new_separator_1 = separator_1
                                    new_segments.append(new_element_1, new_separator_1)
                                new_last_1 = proc(element.default.type_expr.qself.path.segments.last)
                                assert(isinstance(new_last_1, RustPathSegment))
                                if new_last_1 is not element.default.type_expr.qself.path.segments.last:
                                    changed_8 = True
                                new_segments.append_final(new_last_1)
                                if changed_8:
                                    new_path = RustPath(leading_colon_colon=element.default.type_expr.qself.path.leading_colon_colon, segments=new_segments)
                                    changed_7 = True
                                else:
                                    new_path = element.default.type_expr.qself.path
                                if changed_7:
                                    new_qself = RustQself(less_than=element.default.type_expr.qself.less_than, type_expr=new_type_expr_1, as_keyword=element.default.type_expr.qself.as_keyword, path=new_path, greater_than=element.default.type_expr.qself.greater_than)
                                    changed_6 = True
                                else:
                                    new_qself = element.default.type_expr.qself
                            elif element.default.type_expr.qself is None:
                                new_qself = element.default.type_expr.qself
                            else:
                                assert_never(element.default.type_expr.qself)
                            new_path_8 = proc(element.default.type_expr.path)
                            assert(isinstance(new_path_8, RustPath))
                            if new_path_8 is not element.default.type_expr.path:
                                changed_6 = True
                            if changed_6:
                                new_type_expr = RustPathTypeExpr(qself=new_qself, path=new_path_8)
                                changed_5 = True
                            else:
                                new_type_expr = element.default.type_expr
                        elif isinstance(element.default.type_expr, RustArrayTypeExpr):
                            changed_38 = False
                            new_type_expr_4 = proc(element.default.type_expr.type_expr)
                            assert(is_rust_type_expr(new_type_expr_4))
                            if new_type_expr_4 is not element.default.type_expr.type_expr:
                                changed_38 = True
                            new_expr_4 = proc(element.default.type_expr.expr)
                            assert(is_rust_expr(new_expr_4))
                            if new_expr_4 is not element.default.type_expr.expr:
                                changed_38 = True
                            if changed_38:
                                new_type_expr = RustArrayTypeExpr(open_bracket=element.default.type_expr.open_bracket, type_expr=new_type_expr_4, semicolon=element.default.type_expr.semicolon, expr=new_expr_4, close_bracket=element.default.type_expr.close_bracket)
                                changed_5 = True
                            else:
                                new_type_expr = element.default.type_expr
                        elif isinstance(element.default.type_expr, RustNeverTypeExpr):
                            new_type_expr = element.default.type_expr
                        elif isinstance(element.default.type_expr, RustTupleTypeExpr):
                            changed_40 = False
                            new_elements_5 = Punctuated()
                            for (element_16, separator_12) in element.default.type_expr.elements.delimited:
                                new_element_16 = proc(element_16)
                                assert(is_rust_type_expr(new_element_16))
                                if new_element_16 is not element_16:
                                    changed_40 = True
                                new_separator_12 = proc(separator_12)
                                assert(isinstance(new_separator_12, RustComma))
                                if new_separator_12 is not separator_12:
                                    changed_40 = True
                                new_elements_5.append(new_element_16, new_separator_12)
                            new_last_13 = proc(element.default.type_expr.elements.last)
                            assert(is_rust_type_expr(new_last_13))
                            if new_last_13 is not element.default.type_expr.elements.last:
                                changed_40 = True
                            new_elements_5.append_final(new_last_13)
                            if changed_40:
                                new_type_expr = RustTupleTypeExpr(open_paren=element.default.type_expr.open_paren, elements=new_elements_5, close_paren=element.default.type_expr.close_paren)
                                changed_5 = True
                            else:
                                new_type_expr = element.default.type_expr
                        else:
                            assert_never(element.default.type_expr)
                        if changed_5:
                            new_default = RustTypeInit(equals=element.default.equals, type_expr=new_type_expr)
                            changed_4 = True
                        else:
                            new_default = element.default
                    elif element.default is None:
                        new_default = element.default
                    else:
                        assert_never(element.default)
                    if changed_4:
                        new_element = RustTypeParam(name=element.name, colon=element.colon, type_param_bound=new_type_param_bound, percent=element.percent, plus=element.plus, default=new_default)
                        changed_3 = True
                    else:
                        new_element = element
                elif isinstance(element, RustConstParam):
                    changed_41 = False
                    new_type_expr_5 = proc(element.type_expr)
                    assert(is_rust_type_expr(new_type_expr_5))
                    if new_type_expr_5 is not element.type_expr:
                        changed_41 = True
                    if isinstance(element.default, RustInit):
                        new_default_1 = proc(element.default)
                        assert(isinstance(new_default_1, RustInit))
                        if new_default_1 is not element.default:
                            changed_41 = True
                    elif element.default is None:
                        new_default_1 = element.default
                    else:
                        assert_never(element.default)
                    if changed_41:
                        new_element = RustConstParam(const_keyword=element.const_keyword, name=element.name, colon=element.colon, type_expr=new_type_expr_5, default=new_default_1)
                        changed_3 = True
                    else:
                        new_element = element
                else:
                    assert_never(element)
                new_separator = proc(separator)
                assert(isinstance(new_separator, RustComma))
                if new_separator is not separator:
                    changed_3 = True
                new_lifetimes.append(new_element, new_separator)
            new_last = proc(node.bound_lifetimes.lifetimes.last)
            assert(is_rust_generic_param(new_last))
            if new_last is not node.bound_lifetimes.lifetimes.last:
                changed_3 = True
            new_lifetimes.append_final(new_last)
            if changed_3:
                new_bound_lifetimes = RustBoundLifetimes(for_keyword=node.bound_lifetimes.for_keyword, less_than=node.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=node.bound_lifetimes.greater_than)
                changed_2 = True
            else:
                new_bound_lifetimes = node.bound_lifetimes
        elif node.bound_lifetimes is None:
            new_bound_lifetimes = node.bound_lifetimes
        else:
            assert_never(node.bound_lifetimes)
        new_path_9 = proc(node.path)
        assert(isinstance(new_path_9, RustPath))
        if new_path_9 is not node.path:
            changed_2 = True
        if changed_2:
            rewritten = RustTraitBound(modifier=node.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_9)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_use_tree(node: RustUseTree, proc: Callable[[RustUseTree], RustUseTree]) -> RustUseTree:
    if isinstance(node, RustUseGlob):
        rewritten = node
    elif isinstance(node, RustUseGroup):
        changed_2 = False
        new_items = Punctuated()
        for (element, separator) in node.items.delimited:
            new_element = proc(element)
            assert(is_rust_use_tree(new_element))
            if new_element is not element:
                changed_2 = True
            new_separator = separator
            new_items.append(new_element, new_separator)
        new_last = proc(node.items.last)
        assert(is_rust_use_tree(new_last))
        if new_last is not node.items.last:
            changed_2 = True
        new_items.append_final(new_last)
        if changed_2:
            rewritten = RustUseGroup(open_brace=node.open_brace, items=new_items, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustUseName):
        rewritten = node
    elif isinstance(node, RustUsePath):
        changed_4 = False
        new_tree = proc(node.tree)
        assert(is_rust_use_tree(new_tree))
        if new_tree is not node.tree:
            changed_4 = True
        if changed_4:
            rewritten = RustUsePath(name=node.name, colon_colon=node.colon_colon, tree=new_tree)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustUseRename):
        rewritten = node
    else:
        assert_never(node)
    return rewritten


@no_type_check
def rewrite_each_rust_variant(node: RustVariant, proc: Callable[[RustVariant], RustVariant]) -> RustVariant:
    if isinstance(node, RustEmptyVariant):
        changed_1 = False
        if isinstance(node.init, RustInit):
            changed_2 = False
            if isinstance(node.init.value, RustLitExpr):
                new_value = node.init.value
            elif isinstance(node.init.value, RustPathExpr):
                changed_4 = False
                new_attrs = []
                for element in node.init.value.attrs:
                    changed_5 = False
                    if isinstance(element.meta, RustMetaPath):
                        changed_6 = False
                        changed_7 = False
                        new_segments = Punctuated()
                        for (element_1, separator) in element.meta.path.segments.delimited:
                            changed_8 = False
                            if is_rust_path_arguments(element_1.args):
                                if isinstance(element_1.args, RustTurbofish):
                                    changed_9 = False
                                    new_args_1 = Punctuated()
                                    for (element_2, separator_1) in element_1.args.args.delimited:
                                        if isinstance(element_2, RustLifetime):
                                            new_element_2 = element_2
                                        elif is_rust_type_expr(element_2):
                                            if isinstance(element_2, RustPathTypeExpr):
                                                changed_11 = False
                                                if isinstance(element_2.qself, RustQself):
                                                    changed_12 = False
                                                    new_type_expr = proc(element_2.qself.type_expr)
                                                    assert(is_rust_type_expr(new_type_expr))
                                                    if new_type_expr is not element_2.qself.type_expr:
                                                        changed_12 = True
                                                    new_path_1 = proc(element_2.qself.path)
                                                    assert(isinstance(new_path_1, RustPath))
                                                    if new_path_1 is not element_2.qself.path:
                                                        changed_12 = True
                                                    if changed_12:
                                                        new_qself = RustQself(less_than=element_2.qself.less_than, type_expr=new_type_expr, as_keyword=element_2.qself.as_keyword, path=new_path_1, greater_than=element_2.qself.greater_than)
                                                        changed_11 = True
                                                    else:
                                                        new_qself = element_2.qself
                                                elif element_2.qself is None:
                                                    new_qself = element_2.qself
                                                else:
                                                    assert_never(element_2.qself)
                                                new_path_2 = proc(element_2.path)
                                                assert(isinstance(new_path_2, RustPath))
                                                if new_path_2 is not element_2.path:
                                                    changed_11 = True
                                                if changed_11:
                                                    new_element_2 = RustPathTypeExpr(qself=new_qself, path=new_path_2)
                                                    changed_9 = True
                                                else:
                                                    new_element_2 = element_2
                                            elif isinstance(element_2, RustArrayTypeExpr):
                                                changed_13 = False
                                                new_type_expr_1 = proc(element_2.type_expr)
                                                assert(is_rust_type_expr(new_type_expr_1))
                                                if new_type_expr_1 is not element_2.type_expr:
                                                    changed_13 = True
                                                new_expr = proc(element_2.expr)
                                                assert(is_rust_expr(new_expr))
                                                if new_expr is not element_2.expr:
                                                    changed_13 = True
                                                if changed_13:
                                                    new_element_2 = RustArrayTypeExpr(open_bracket=element_2.open_bracket, type_expr=new_type_expr_1, semicolon=element_2.semicolon, expr=new_expr, close_bracket=element_2.close_bracket)
                                                    changed_9 = True
                                                else:
                                                    new_element_2 = element_2
                                            elif isinstance(element_2, RustNeverTypeExpr):
                                                new_element_2 = element_2
                                            elif isinstance(element_2, RustTupleTypeExpr):
                                                changed_15 = False
                                                new_elements_1 = Punctuated()
                                                for (element_3, separator_2) in element_2.elements.delimited:
                                                    new_element_3 = proc(element_3)
                                                    assert(is_rust_type_expr(new_element_3))
                                                    if new_element_3 is not element_3:
                                                        changed_15 = True
                                                    new_separator_2 = separator_2
                                                    new_elements_1.append(new_element_3, new_separator_2)
                                                new_last_2 = proc(element_2.elements.last)
                                                assert(is_rust_type_expr(new_last_2))
                                                if new_last_2 is not element_2.elements.last:
                                                    changed_15 = True
                                                new_elements_1.append_final(new_last_2)
                                                if changed_15:
                                                    new_element_2 = RustTupleTypeExpr(open_paren=element_2.open_paren, elements=new_elements_1, close_paren=element_2.close_paren)
                                                    changed_9 = True
                                                else:
                                                    new_element_2 = element_2
                                            else:
                                                assert_never(element_2)
                                        elif is_rust_expr(element_2):
                                            new_element_2 = proc(element_2)
                                            assert(is_rust_expr(new_element_2))
                                            if new_element_2 is not element_2:
                                                changed_9 = True
                                        elif isinstance(element_2, RustAssocType):
                                            changed_16 = False
                                            if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                                changed_17 = False
                                                new_args_2 = Punctuated()
                                                for (element_4, separator_3) in element_2.generics.args.delimited:
                                                    new_element_4 = proc(element_4)
                                                    assert(is_rust_generic_argument(new_element_4))
                                                    if new_element_4 is not element_4:
                                                        changed_17 = True
                                                    new_separator_3 = proc(separator_3)
                                                    assert(isinstance(new_separator_3, RustComma))
                                                    if new_separator_3 is not separator_3:
                                                        changed_17 = True
                                                    new_args_2.append(new_element_4, new_separator_3)
                                                new_last_3 = proc(element_2.generics.args.last)
                                                assert(is_rust_generic_argument(new_last_3))
                                                if new_last_3 is not element_2.generics.args.last:
                                                    changed_17 = True
                                                new_args_2.append_final(new_last_3)
                                                if changed_17:
                                                    new_generics = RustAngleBracketedGenericArguments(less_than=element_2.generics.less_than, args=new_args_2, greater_than=element_2.generics.greater_than)
                                                    changed_16 = True
                                                else:
                                                    new_generics = element_2.generics
                                            elif element_2.generics is None:
                                                new_generics = element_2.generics
                                            else:
                                                assert_never(element_2.generics)
                                            new_type_expr_2 = proc(element_2.type_expr)
                                            assert(is_rust_type_expr(new_type_expr_2))
                                            if new_type_expr_2 is not element_2.type_expr:
                                                changed_16 = True
                                            if changed_16:
                                                new_element_2 = RustAssocType(name=element_2.name, generics=new_generics, equals=element_2.equals, type_expr=new_type_expr_2)
                                                changed_9 = True
                                            else:
                                                new_element_2 = element_2
                                        elif isinstance(element_2, RustAssocConst):
                                            changed_18 = False
                                            if isinstance(element_2.generics, RustAngleBracketedGenericArguments):
                                                new_generics_1 = proc(element_2.generics)
                                                assert(isinstance(new_generics_1, RustAngleBracketedGenericArguments))
                                                if new_generics_1 is not element_2.generics:
                                                    changed_18 = True
                                            elif element_2.generics is None:
                                                new_generics_1 = element_2.generics
                                            else:
                                                assert_never(element_2.generics)
                                            new_expr_1 = proc(element_2.expr)
                                            assert(is_rust_expr(new_expr_1))
                                            if new_expr_1 is not element_2.expr:
                                                changed_18 = True
                                            if changed_18:
                                                new_element_2 = RustAssocConst(name=element_2.name, generics=new_generics_1, equals=element_2.equals, expr=new_expr_1)
                                                changed_9 = True
                                            else:
                                                new_element_2 = element_2
                                        elif isinstance(element_2, RustConstraint):
                                            changed_19 = False
                                            new_generics_2 = proc(element_2.generics)
                                            assert(isinstance(new_generics_2, RustAngleBracketedGenericArguments))
                                            if new_generics_2 is not element_2.generics:
                                                changed_19 = True
                                            new_bounds = Punctuated()
                                            for (element_5, separator_4) in element_2.bounds.delimited:
                                                if isinstance(element_5, RustTraitBound):
                                                    changed_20 = False
                                                    if isinstance(element_5.bound_lifetimes, RustBoundLifetimes):
                                                        changed_21 = False
                                                        new_lifetimes = Punctuated()
                                                        for (element_6, separator_5) in element_5.bound_lifetimes.lifetimes.delimited:
                                                            if isinstance(element_6, RustLifetime):
                                                                new_element_6 = proc(element_6)
                                                                assert(isinstance(new_element_6, RustLifetime))
                                                                if new_element_6 is not element_6:
                                                                    changed_21 = True
                                                            elif isinstance(element_6, RustTypeParam):
                                                                changed_22 = False
                                                                new_type_param_bound = proc(element_6.type_param_bound)
                                                                assert(is_rust_type_param_bound(new_type_param_bound))
                                                                if new_type_param_bound is not element_6.type_param_bound:
                                                                    changed_22 = True
                                                                if isinstance(element_6.default, RustTypeInit):
                                                                    changed_23 = False
                                                                    new_type_expr_3 = proc(element_6.default.type_expr)
                                                                    assert(is_rust_type_expr(new_type_expr_3))
                                                                    if new_type_expr_3 is not element_6.default.type_expr:
                                                                        changed_23 = True
                                                                    if changed_23:
                                                                        new_default = RustTypeInit(equals=element_6.default.equals, type_expr=new_type_expr_3)
                                                                        changed_22 = True
                                                                    else:
                                                                        new_default = element_6.default
                                                                elif element_6.default is None:
                                                                    new_default = element_6.default
                                                                else:
                                                                    assert_never(element_6.default)
                                                                if changed_22:
                                                                    new_element_6 = RustTypeParam(name=element_6.name, colon=element_6.colon, type_param_bound=new_type_param_bound, percent=element_6.percent, plus=element_6.plus, default=new_default)
                                                                    changed_21 = True
                                                                else:
                                                                    new_element_6 = element_6
                                                            elif isinstance(element_6, RustConstParam):
                                                                changed_24 = False
                                                                new_type_expr_4 = proc(element_6.type_expr)
                                                                assert(is_rust_type_expr(new_type_expr_4))
                                                                if new_type_expr_4 is not element_6.type_expr:
                                                                    changed_24 = True
                                                                if isinstance(element_6.default, RustInit):
                                                                    new_default_1 = proc(element_6.default)
                                                                    assert(isinstance(new_default_1, RustInit))
                                                                    if new_default_1 is not element_6.default:
                                                                        changed_24 = True
                                                                elif element_6.default is None:
                                                                    new_default_1 = element_6.default
                                                                else:
                                                                    assert_never(element_6.default)
                                                                if changed_24:
                                                                    new_element_6 = RustConstParam(const_keyword=element_6.const_keyword, name=element_6.name, colon=element_6.colon, type_expr=new_type_expr_4, default=new_default_1)
                                                                    changed_21 = True
                                                                else:
                                                                    new_element_6 = element_6
                                                            else:
                                                                assert_never(element_6)
                                                            new_separator_5 = proc(separator_5)
                                                            assert(isinstance(new_separator_5, RustComma))
                                                            if new_separator_5 is not separator_5:
                                                                changed_21 = True
                                                            new_lifetimes.append(new_element_6, new_separator_5)
                                                        new_last_5 = proc(element_5.bound_lifetimes.lifetimes.last)
                                                        assert(is_rust_generic_param(new_last_5))
                                                        if new_last_5 is not element_5.bound_lifetimes.lifetimes.last:
                                                            changed_21 = True
                                                        new_lifetimes.append_final(new_last_5)
                                                        if changed_21:
                                                            new_bound_lifetimes = RustBoundLifetimes(for_keyword=element_5.bound_lifetimes.for_keyword, less_than=element_5.bound_lifetimes.less_than, lifetimes=new_lifetimes, greater_than=element_5.bound_lifetimes.greater_than)
                                                            changed_20 = True
                                                        else:
                                                            new_bound_lifetimes = element_5.bound_lifetimes
                                                    elif element_5.bound_lifetimes is None:
                                                        new_bound_lifetimes = element_5.bound_lifetimes
                                                    else:
                                                        assert_never(element_5.bound_lifetimes)
                                                    new_path_3 = proc(element_5.path)
                                                    assert(isinstance(new_path_3, RustPath))
                                                    if new_path_3 is not element_5.path:
                                                        changed_20 = True
                                                    if changed_20:
                                                        new_element_5 = RustTraitBound(modifier=element_5.modifier, bound_lifetimes=new_bound_lifetimes, path=new_path_3)
                                                        changed_19 = True
                                                    else:
                                                        new_element_5 = element_5
                                                elif isinstance(element_5, RustLifetime):
                                                    new_element_5 = proc(element_5)
                                                    assert(isinstance(new_element_5, RustLifetime))
                                                    if new_element_5 is not element_5:
                                                        changed_19 = True
                                                else:
                                                    assert_never(element_5)
                                                new_separator_4 = separator_4
                                                new_bounds.append(new_element_5, new_separator_4)
                                            new_last_4 = proc(element_2.bounds.last)
                                            assert(is_rust_type_param_bound(new_last_4))
                                            if new_last_4 is not element_2.bounds.last:
                                                changed_19 = True
                                            new_bounds.append_final(new_last_4)
                                            if changed_19:
                                                new_element_2 = RustConstraint(name=element_2.name, generics=new_generics_2, colon=element_2.colon, bounds=new_bounds)
                                                changed_9 = True
                                            else:
                                                new_element_2 = element_2
                                        else:
                                            assert_never(element_2)
                                        new_separator_1 = proc(separator_1)
                                        assert(isinstance(new_separator_1, RustComma))
                                        if new_separator_1 is not separator_1:
                                            changed_9 = True
                                        new_args_1.append(new_element_2, new_separator_1)
                                    new_last_1 = proc(element_1.args.args.last)
                                    assert(is_rust_generic_argument(new_last_1))
                                    if new_last_1 is not element_1.args.args.last:
                                        changed_9 = True
                                    new_args_1.append_final(new_last_1)
                                    if changed_9:
                                        new_args = RustTurbofish(colon_colon=element_1.args.colon_colon, less_than=element_1.args.less_than, args=new_args_1, greater_than=element_1.args.greater_than)
                                        changed_8 = True
                                    else:
                                        new_args = element_1.args
                                elif isinstance(element_1.args, RustAngleBracketedGenericArguments):
                                    new_args = proc(element_1.args)
                                    assert(isinstance(new_args, RustAngleBracketedGenericArguments))
                                    if new_args is not element_1.args:
                                        changed_8 = True
                                elif isinstance(element_1.args, RustParenthesizedGenericArguments):
                                    changed_25 = False
                                    new_params = Punctuated()
                                    for (element_7, separator_6) in element_1.args.params.delimited:
                                        new_element_7 = proc(element_7)
                                        assert(is_rust_type_expr(new_element_7))
                                        if new_element_7 is not element_7:
                                            changed_25 = True
                                        new_separator_6 = proc(separator_6)
                                        assert(isinstance(new_separator_6, RustComma))
                                        if new_separator_6 is not separator_6:
                                            changed_25 = True
                                        new_params.append(new_element_7, new_separator_6)
                                    new_last_6 = proc(element_1.args.params.last)
                                    assert(is_rust_type_expr(new_last_6))
                                    if new_last_6 is not element_1.args.params.last:
                                        changed_25 = True
                                    new_params.append_final(new_last_6)
                                    new_result = proc(element_1.args.result)
                                    assert(is_rust_type_expr(new_result))
                                    if new_result is not element_1.args.result:
                                        changed_25 = True
                                    if changed_25:
                                        new_args = RustParenthesizedGenericArguments(open_paren=element_1.args.open_paren, params=new_params, close_paren=element_1.args.close_paren, r_arrow=element_1.args.r_arrow, result=new_result)
                                        changed_8 = True
                                    else:
                                        new_args = element_1.args
                                else:
                                    assert_never(element_1.args)
                            elif element_1.args is None:
                                new_args = element_1.args
                            else:
                                assert_never(element_1.args)
                            if changed_8:
                                new_element_1 = RustPathSegment(name=element_1.name, args=new_args)
                                changed_7 = True
                            else:
                                new_element_1 = element_1
                            new_separator = separator
                            new_segments.append(new_element_1, new_separator)
                        new_last = proc(element.meta.path.segments.last)
                        assert(isinstance(new_last, RustPathSegment))
                        if new_last is not element.meta.path.segments.last:
                            changed_7 = True
                        new_segments.append_final(new_last)
                        if changed_7:
                            new_path = RustPath(leading_colon_colon=element.meta.path.leading_colon_colon, segments=new_segments)
                            changed_6 = True
                        else:
                            new_path = element.meta.path
                        if changed_6:
                            new_meta = RustMetaPath(path=new_path)
                            changed_5 = True
                        else:
                            new_meta = element.meta
                    elif isinstance(element.meta, RustMetaParenthesized):
                        changed_26 = False
                        new_path_4 = proc(element.meta.path)
                        assert(isinstance(new_path_4, RustPath))
                        if new_path_4 is not element.meta.path:
                            changed_26 = True
                        if changed_26:
                            new_meta = RustMetaParenthesized(path=new_path_4, open_paren=element.meta.open_paren, tokens=element.meta.tokens, close_paren=element.meta.close_paren)
                            changed_5 = True
                        else:
                            new_meta = element.meta
                    elif isinstance(element.meta, RustMetaBracketed):
                        changed_27 = False
                        new_path_5 = proc(element.meta.path)
                        assert(isinstance(new_path_5, RustPath))
                        if new_path_5 is not element.meta.path:
                            changed_27 = True
                        if changed_27:
                            new_meta = RustMetaBracketed(path=new_path_5, open_bracket=element.meta.open_bracket, tokens=element.meta.tokens, close_bracket=element.meta.close_bracket)
                            changed_5 = True
                        else:
                            new_meta = element.meta
                    elif isinstance(element.meta, RustMetaBraced):
                        changed_28 = False
                        new_path_6 = proc(element.meta.path)
                        assert(isinstance(new_path_6, RustPath))
                        if new_path_6 is not element.meta.path:
                            changed_28 = True
                        if changed_28:
                            new_meta = RustMetaBraced(path=new_path_6, open_brace=element.meta.open_brace, tokens=element.meta.tokens, close_brace=element.meta.close_brace)
                            changed_5 = True
                        else:
                            new_meta = element.meta
                    elif isinstance(element.meta, RustMetaNameValue):
                        changed_29 = False
                        new_path_7 = proc(element.meta.path)
                        assert(isinstance(new_path_7, RustPath))
                        if new_path_7 is not element.meta.path:
                            changed_29 = True
                        new_expr_2 = proc(element.meta.expr)
                        assert(is_rust_expr(new_expr_2))
                        if new_expr_2 is not element.meta.expr:
                            changed_29 = True
                        if changed_29:
                            new_meta = RustMetaNameValue(path=new_path_7, equals=element.meta.equals, expr=new_expr_2)
                            changed_5 = True
                        else:
                            new_meta = element.meta
                    else:
                        assert_never(element.meta)
                    if changed_5:
                        new_element = RustAttr(hashtag=element.hashtag, exclamation_mark=element.exclamation_mark, open_bracket=element.open_bracket, meta=new_meta, close_bracket=element.close_bracket)
                        changed_4 = True
                    else:
                        new_element = element
                    new_elements.append(new_element)
                if isinstance(node.init.value.qself, RustQself):
                    new_qself_1 = proc(node.init.value.qself)
                    assert(isinstance(new_qself_1, RustQself))
                    if new_qself_1 is not node.init.value.qself:
                        changed_4 = True
                elif node.init.value.qself is None:
                    new_qself_1 = node.init.value.qself
                else:
                    assert_never(node.init.value.qself)
                new_path_8 = proc(node.init.value.path)
                assert(isinstance(new_path_8, RustPath))
                if new_path_8 is not node.init.value.path:
                    changed_4 = True
                if changed_4:
                    new_value = RustPathExpr(attrs=new_attrs, qself=new_qself_1, path=new_path_8)
                    changed_2 = True
                else:
                    new_value = node.init.value
            elif isinstance(node.init.value, RustCallExpr):
                changed_30 = False
                new_operator = proc(node.init.value.operator)
                assert(is_rust_expr(new_operator))
                if new_operator is not node.init.value.operator:
                    changed_30 = True
                new_args_3 = Punctuated()
                for (element_8, separator_7) in node.init.value.args.delimited:
                    new_element_8 = proc(element_8)
                    assert(is_rust_expr(new_element_8))
                    if new_element_8 is not element_8:
                        changed_30 = True
                    new_separator_7 = proc(separator_7)
                    assert(isinstance(new_separator_7, RustComma))
                    if new_separator_7 is not separator_7:
                        changed_30 = True
                    new_args_3.append(new_element_8, new_separator_7)
                new_last_7 = proc(node.init.value.args.last)
                assert(is_rust_expr(new_last_7))
                if new_last_7 is not node.init.value.args.last:
                    changed_30 = True
                new_args_3.append_final(new_last_7)
                if changed_30:
                    new_value = RustCallExpr(operator=new_operator, open_paren=node.init.value.open_paren, args=new_args_3, close_paren=node.init.value.close_paren)
                    changed_2 = True
                else:
                    new_value = node.init.value
            elif isinstance(node.init.value, RustStructExpr):
                changed_31 = False
                new_path_9 = proc(node.init.value.path)
                assert(isinstance(new_path_9, RustPath))
                if new_path_9 is not node.init.value.path:
                    changed_31 = True
                new_inits = Punctuated()
                for (element_9, separator_8) in node.init.value.inits.delimited:
                    new_element_9 = proc(element_9)
                    assert(isinstance(new_element_9, RustInit))
                    if new_element_9 is not element_9:
                        changed_31 = True
                    new_separator_8 = proc(separator_8)
                    assert(isinstance(new_separator_8, RustComma))
                    if new_separator_8 is not separator_8:
                        changed_31 = True
                    new_inits.append(new_element_9, new_separator_8)
                new_last_8 = proc(node.init.value.inits.last)
                assert(isinstance(new_last_8, RustInit))
                if new_last_8 is not node.init.value.inits.last:
                    changed_31 = True
                new_inits.append_final(new_last_8)
                if changed_31:
                    new_value = RustStructExpr(path=new_path_9, open_brace=node.init.value.open_brace, inits=new_inits, comma=node.init.value.comma, close_brace=node.init.value.close_brace)
                    changed_2 = True
                else:
                    new_value = node.init.value
            elif isinstance(node.init.value, RustBlockExpr):
                changed_32 = False
                if isinstance(node.init.value.item, RustEnumItem):
                    changed_33 = False
                    new_attrs_1 = []
                    for element_10 in node.init.value.item.attrs:
                        new_element_10 = proc(element_10)
                        assert(isinstance(new_element_10, RustAttr))
                        if new_element_10 is not element_10:
                            changed_33 = True
                        new_elements_2.append(new_element_10)
                    if isinstance(node.init.value.item.visibility, RustPublic):
                        changed_34 = False
                        if isinstance(node.init.value.item.visibility.restrict, tuple):
                            new_elements_3 = []
                            element_0 = node.init.value.item.visibility.restrict[0]
                            new_element_0 = element_0
                            new_elements_3.append(new_element_0)
                            element_1 = node.init.value.item.visibility.restrict[1]
                            if isinstance(element_1, RustInKeyword):
                                new_element_1 = element_1
                            elif element_1 is None:
                                new_element_1 = element_1
                            else:
                                assert_never(element_1)
                            new_elements_3.append(new_element_1)
                            element_2 = node.init.value.item.visibility.restrict[2]
                            new_element_2 = proc(element_2)
                            assert(isinstance(new_element_2, RustPath))
                            if new_element_2 is not element_2:
                                changed_34 = True
                            new_elements_3.append(new_element_2)
                            element_3 = node.init.value.item.visibility.restrict[3]
                            new_element_3 = element_3
                            new_elements_3.append(new_element_3)
                            new_restrict = tuple(new_elements_3) if changed_34 else node.init.value.item.visibility.restrict
                        elif node.init.value.item.visibility.restrict is None:
                            new_restrict = node.init.value.item.visibility.restrict
                        else:
                            assert_never(node.init.value.item.visibility.restrict)
                        if changed_34:
                            new_visibility = RustPublic(pub_keyword=node.init.value.item.visibility.pub_keyword, restrict=new_restrict)
                            changed_33 = True
                        else:
                            new_visibility = node.init.value.item.visibility
                    elif node.init.value.item.visibility is None:
                        new_visibility = node.init.value.item.visibility
                    else:
                        assert_never(node.init.value.item.visibility)
                    new_variants = Punctuated()
                    for (element_11, separator_9) in node.init.value.item.variants.delimited:
                        new_element_11 = proc(element_11)
                        assert(is_rust_variant(new_element_11))
                        if new_element_11 is not element_11:
                            changed_33 = True
                        new_separator_9 = proc(separator_9)
                        assert(isinstance(new_separator_9, RustComma))
                        if new_separator_9 is not separator_9:
                            changed_33 = True
                        new_variants.append(new_element_11, new_separator_9)
                    new_last_9 = proc(node.init.value.item.variants.last)
                    assert(is_rust_variant(new_last_9))
                    if new_last_9 is not node.init.value.item.variants.last:
                        changed_33 = True
                    new_variants.append_final(new_last_9)
                    if changed_33:
                        new_item = RustEnumItem(attrs=new_attrs_1, visibility=new_visibility, enum_keyword=node.init.value.item.enum_keyword, name=node.init.value.item.name, open_brace=node.init.value.item.open_brace, variants=new_variants, comma=node.init.value.item.comma, close_brace=node.init.value.item.close_brace)
                        changed_32 = True
                    else:
                        new_item = node.init.value.item
                elif isinstance(node.init.value.item, RustStructItem):
                    changed_35 = False
                    new_attrs_2 = []
                    for element_12 in node.init.value.item.attrs:
                        new_element_12 = proc(element_12)
                        assert(isinstance(new_element_12, RustAttr))
                        if new_element_12 is not element_12:
                            changed_35 = True
                        new_elements_4.append(new_element_12)
                    if isinstance(node.init.value.item.visibility, RustPublic):
                        new_visibility_1 = proc(node.init.value.item.visibility)
                        assert(isinstance(new_visibility_1, RustPublic))
                        if new_visibility_1 is not node.init.value.item.visibility:
                            changed_35 = True
                    elif node.init.value.item.visibility is None:
                        new_visibility_1 = node.init.value.item.visibility
                    else:
                        assert_never(node.init.value.item.visibility)
                    new_fields = Punctuated()
                    for (element_13, separator_10) in node.init.value.item.fields.delimited:
                        changed_36 = False
                        new_type_expr_5 = proc(element_13.type_expr)
                        assert(is_rust_type_expr(new_type_expr_5))
                        if new_type_expr_5 is not element_13.type_expr:
                            changed_36 = True
                        if changed_36:
                            new_element_13 = RustField(name=element_13.name, colon=element_13.colon, type_expr=new_type_expr_5)
                            changed_35 = True
                        else:
                            new_element_13 = element_13
                        new_separator_10 = proc(separator_10)
                        assert(isinstance(new_separator_10, RustComma))
                        if new_separator_10 is not separator_10:
                            changed_35 = True
                        new_fields.append(new_element_13, new_separator_10)
                    new_last_10 = proc(node.init.value.item.fields.last)
                    assert(isinstance(new_last_10, RustField))
                    if new_last_10 is not node.init.value.item.fields.last:
                        changed_35 = True
                    new_fields.append_final(new_last_10)
                    if changed_35:
                        new_item = RustStructItem(attrs=new_attrs_2, visibility=new_visibility_1, struct_keyword=node.init.value.item.struct_keyword, name=node.init.value.item.name, open_brace=node.init.value.item.open_brace, fields=new_fields, comma=node.init.value.item.comma, close_brace=node.init.value.item.close_brace)
                        changed_32 = True
                    else:
                        new_item = node.init.value.item
                elif isinstance(node.init.value.item, RustUseItem):
                    changed_37 = False
                    new_attrs_3 = []
                    for element_14 in node.init.value.item.attrs:
                        new_element_14 = proc(element_14)
                        assert(isinstance(new_element_14, RustAttr))
                        if new_element_14 is not element_14:
                            changed_37 = True
                        new_elements_5.append(new_element_14)
                    if isinstance(node.init.value.item.visibility, RustPublic):
                        new_visibility_2 = proc(node.init.value.item.visibility)
                        assert(isinstance(new_visibility_2, RustPublic))
                        if new_visibility_2 is not node.init.value.item.visibility:
                            changed_37 = True
                    elif node.init.value.item.visibility is None:
                        new_visibility_2 = node.init.value.item.visibility
                    else:
                        assert_never(node.init.value.item.visibility)
                    if changed_37:
                        new_item = RustUseItem(attrs=new_attrs_3, visibility=new_visibility_2, use_keyword=node.init.value.item.use_keyword, colon_colon=node.init.value.item.colon_colon, path=node.init.value.item.path, semicolon=node.init.value.item.semicolon)
                        changed_32 = True
                    else:
                        new_item = node.init.value.item
                elif isinstance(node.init.value.item, RustExprItem):
                    changed_38 = False
                    new_expr_3 = proc(node.init.value.item.expr)
                    assert(is_rust_expr(new_expr_3))
                    if new_expr_3 is not node.init.value.item.expr:
                        changed_38 = True
                    if changed_38:
                        new_item = RustExprItem(expr=new_expr_3)
                        changed_32 = True
                    else:
                        new_item = node.init.value.item
                else:
                    assert_never(node.init.value.item)
                new_last_11 = proc(node.init.value.last)
                assert(is_rust_expr(new_last_11))
                if new_last_11 is not node.init.value.last:
                    changed_32 = True
                if changed_32:
                    new_value = RustBlockExpr(open_brace=node.init.value.open_brace, item=new_item, semicolon=node.init.value.semicolon, last=new_last_11, close_brace=node.init.value.close_brace)
                    changed_2 = True
                else:
                    new_value = node.init.value
            elif isinstance(node.init.value, RustRetExpr):
                changed_39 = False
                new_expr_4 = proc(node.init.value.expr)
                assert(is_rust_expr(new_expr_4))
                if new_expr_4 is not node.init.value.expr:
                    changed_39 = True
                if changed_39:
                    new_value = RustRetExpr(return_keyword=node.init.value.return_keyword, expr=new_expr_4)
                    changed_2 = True
                else:
                    new_value = node.init.value
            else:
                assert_never(node.init.value)
            if changed_2:
                new_init = RustInit(name=node.init.name, equals=node.init.equals, value=new_value)
                changed_1 = True
            else:
                new_init = node.init
        elif node.init is None:
            new_init = node.init
        else:
            assert_never(node.init)
        if changed_1:
            rewritten = RustEmptyVariant(name=node.name, init=new_init)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustStructVariant):
        changed_40 = False
        new_fields_1 = Punctuated()
        for (element_15, separator_11) in node.fields.delimited:
            new_element_15 = proc(element_15)
            assert(isinstance(new_element_15, RustField))
            if new_element_15 is not element_15:
                changed_40 = True
            new_separator_11 = proc(separator_11)
            assert(isinstance(new_separator_11, RustComma))
            if new_separator_11 is not separator_11:
                changed_40 = True
            new_fields_1.append(new_element_15, new_separator_11)
        new_last_12 = proc(node.fields.last)
        assert(isinstance(new_last_12, RustField))
        if new_last_12 is not node.fields.last:
            changed_40 = True
        new_fields_1.append_final(new_last_12)
        if changed_40:
            rewritten = RustStructVariant(name=node.name, open_brace=node.open_brace, fields=new_fields_1, comma=node.comma, close_brace=node.close_brace)
            changed = True
        else:
            rewritten = node
    elif isinstance(node, RustTupleVariant):
        changed_41 = False
        new_types = Punctuated()
        for (element_16, separator_12) in node.types.delimited:
            new_element_16 = proc(element_16)
            assert(is_rust_type_expr(new_element_16))
            if new_element_16 is not element_16:
                changed_41 = True
            new_separator_12 = proc(separator_12)
            assert(isinstance(new_separator_12, RustComma))
            if new_separator_12 is not separator_12:
                changed_41 = True
            new_types.append(new_element_16, new_separator_12)
        new_last_13 = proc(node.types.last)
        assert(is_rust_type_expr(new_last_13))
        if new_last_13 is not node.types.last:
            changed_41 = True
        new_types.append_final(new_last_13)
        if changed_41:
            rewritten = RustTupleVariant(name=node.name, open_paren=node.open_paren, types=new_types, close_paren=node.close_paren)
            changed = True
        else:
            rewritten = node
    else:
        assert_never(node)
    return rewritten


