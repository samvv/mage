from typing import Any, TypeGuard, Never, Sequence, no_type_check


from magelang.runtime import BaseNode, BaseToken, Punctuated, Span


class _RustBaseNode(BaseNode):

    pass


class _RustBaseToken(BaseToken):

    pass


class RustIdent(_RustBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class RustInteger(_RustBaseToken):

    def __init__(self, value: int, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class RustFloat(_RustBaseToken):

    def __init__(self, value: float, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class RustString(_RustBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class RustChar(_RustBaseToken):

    def __init__(self, value: str, span: Span | None = None):
        super().__init__(span=span)
        self.value = value


class RustCloseBrace(_RustBaseToken):

    pass


class RustOpenBrace(_RustBaseToken):

    pass


class RustWhereKeyword(_RustBaseToken):

    pass


class RustUseKeyword(_RustBaseToken):

    pass


class RustUnsafeKeyword(_RustBaseToken):

    pass


class RustTrueKeyword(_RustBaseToken):

    pass


class RustStructKeyword(_RustBaseToken):

    pass


class RustSelfKeyword(_RustBaseToken):

    pass


class RustReturnKeyword(_RustBaseToken):

    pass


class RustRefKeyword(_RustBaseToken):

    pass


class RustPubKeyword(_RustBaseToken):

    pass


class RustMutKeyword(_RustBaseToken):

    pass


class RustInKeyword(_RustBaseToken):

    pass


class RustImplKeyword(_RustBaseToken):

    pass


class RustForKeyword(_RustBaseToken):

    pass


class RustFnKeyword(_RustBaseToken):

    pass


class RustFalseKeyword(_RustBaseToken):

    pass


class RustExternKeyword(_RustBaseToken):

    pass


class RustEnumKeyword(_RustBaseToken):

    pass


class RustDefaultKeyword(_RustBaseToken):

    pass


class RustConstKeyword(_RustBaseToken):

    pass


class RustAsyncKeyword(_RustBaseToken):

    pass


class RustAsKeyword(_RustBaseToken):

    pass


class RustCloseBracket(_RustBaseToken):

    pass


class RustOpenBracket(_RustBaseToken):

    pass


class RustAtSign(_RustBaseToken):

    pass


class RustQuestionMark(_RustBaseToken):

    pass


class RustGreaterThan(_RustBaseToken):

    pass


class RustEquals(_RustBaseToken):

    pass


class RustLessThan(_RustBaseToken):

    pass


class RustSemicolon(_RustBaseToken):

    pass


class RustColonColon(_RustBaseToken):

    pass


class RustColon(_RustBaseToken):

    pass


class RustDotDotDot(_RustBaseToken):

    pass


class RustRArrow(_RustBaseToken):

    pass


class RustComma(_RustBaseToken):

    pass


class RustPlus(_RustBaseToken):

    pass


class RustAsterisk(_RustBaseToken):

    pass


class RustCloseParen(_RustBaseToken):

    pass


class RustOpenParen(_RustBaseToken):

    pass


class RustSingleQuote(_RustBaseToken):

    pass


class RustAmpersand(_RustBaseToken):

    pass


class RustPercent(_RustBaseToken):

    pass


class RustHashtag(_RustBaseToken):

    pass


class RustExclamationMark(_RustBaseToken):

    pass


class RustPublic(_RustBaseNode):

    def __init__(self, *, pub_keyword: 'RustPubKeyword | None' = None, restrict: 'RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustCloseParen | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> None:
        self.pub_keyword: RustPubKeyword = _coerce_union_2_token_pub_keyword_none_to_token_pub_keyword(pub_keyword)
        self.restrict: tuple[RustOpenParen, RustInKeyword | None, RustPath, RustCloseParen] | None = _coerce_union_6_node_path_tuple_4_union_2_token_open_paren_none_union_2_token_in_keyword_none_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_union_2_token_close_paren_none_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_none_to_union_2_tuple_4_token_open_paren_union_2_token_in_keyword_none_node_path_token_close_paren_none(restrict)

    @no_type_check
    def derive(self, pub_keyword: 'RustPubKeyword | None' = None, restrict: 'RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustCloseParen | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> 'RustPublic':
        if pub_keyword is None:
            pub_keyword = self.pub_keyword
        if restrict is None:
            restrict = self.restrict
        return RustPublic(pub_keyword=pub_keyword, restrict=restrict)

    def parent(self) -> 'RustPublicParent':
        assert(self._parent is not None)
        return self._parent


class RustTypeInit(_RustBaseNode):

    def __init__(self, type_expr: 'RustTypeExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.equals: RustEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)

    @no_type_check
    def derive(self, equals: 'RustEquals | None' = None, type_expr: 'RustTypeExpr | None' = None) -> 'RustTypeInit':
        if equals is None:
            equals = self.equals
        if type_expr is None:
            type_expr = self.type_expr
        return RustTypeInit(equals=equals, type_expr=type_expr)

    def parent(self) -> 'RustTypeInitParent':
        assert(self._parent is not None)
        return self._parent


class RustTypeParam(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', type_param_bound: 'RustTypeParamBound', *, colon: 'RustColon | None' = None, percent: 'RustPercent | None' = None, plus: 'RustPlus | None' = None, default: 'RustTypeInit | RustTypeExpr | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.type_param_bound: RustTypeParamBound = _coerce_variant_type_param_bound_to_variant_type_param_bound(type_param_bound)
        self.percent: RustPercent = _coerce_union_2_token_percent_none_to_token_percent(percent)
        self.plus: RustPlus = _coerce_union_2_token_plus_none_to_token_plus(plus)
        self.default: RustTypeInit | None = _coerce_union_3_node_type_init_variant_type_expr_none_to_union_2_node_type_init_none(default)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, colon: 'RustColon | None' = None, type_param_bound: 'RustTypeParamBound | None' = None, percent: 'RustPercent | None' = None, plus: 'RustPlus | None' = None, default: 'RustTypeInit | RustTypeExpr | None' = None) -> 'RustTypeParam':
        if name is None:
            name = self.name
        if colon is None:
            colon = self.colon
        if type_param_bound is None:
            type_param_bound = self.type_param_bound
        if percent is None:
            percent = self.percent
        if plus is None:
            plus = self.plus
        if default is None:
            default = self.default
        return RustTypeParam(name=name, colon=colon, type_param_bound=type_param_bound, percent=percent, plus=plus, default=default)

    def parent(self) -> 'RustTypeParamParent':
        assert(self._parent is not None)
        return self._parent


class RustConstParam(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', type_expr: 'RustTypeExpr', *, const_keyword: 'RustConstKeyword | None' = None, colon: 'RustColon | None' = None, default: 'RustInit | None' = None) -> None:
        self.const_keyword: RustConstKeyword = _coerce_union_2_token_const_keyword_none_to_token_const_keyword(const_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)
        self.default: RustInit | None = _coerce_union_2_node_init_none_to_union_2_node_init_none(default)

    @no_type_check
    def derive(self, const_keyword: 'RustConstKeyword | None' = None, name: 'RustIdent | None | str' = None, colon: 'RustColon | None' = None, type_expr: 'RustTypeExpr | None' = None, default: 'RustInit | None' = None) -> 'RustConstParam':
        if const_keyword is None:
            const_keyword = self.const_keyword
        if name is None:
            name = self.name
        if colon is None:
            colon = self.colon
        if type_expr is None:
            type_expr = self.type_expr
        if default is None:
            default = self.default
        return RustConstParam(const_keyword=const_keyword, name=name, colon=colon, type_expr=type_expr, default=default)

    def parent(self) -> 'RustConstParamParent':
        assert(self._parent is not None)
        return self._parent


class RustTraitBoundModifier(_RustBaseNode):

    def __init__(self, *, question_mark: 'RustQuestionMark | None' = None) -> None:
        self.question_mark: RustQuestionMark = _coerce_union_2_token_question_mark_none_to_token_question_mark(question_mark)

    @no_type_check
    def derive(self, question_mark: 'RustQuestionMark | None' = None) -> 'RustTraitBoundModifier':
        if question_mark is None:
            question_mark = self.question_mark
        return RustTraitBoundModifier(question_mark=question_mark)

    def parent(self) -> 'RustTraitBoundModifierParent':
        assert(self._parent is not None)
        return self._parent


class RustBoundLifetimes(_RustBaseNode):

    def count_lifetimes(self) -> int:
        return len(self.lifetimes)

    def __init__(self, *, for_keyword: 'RustForKeyword | None' = None, less_than: 'RustLessThan | None' = None, lifetimes: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.for_keyword: RustForKeyword = _coerce_union_2_token_for_keyword_none_to_token_for_keyword(for_keyword)
        self.less_than: RustLessThan = _coerce_union_2_token_less_than_none_to_token_less_than(less_than)
        self.lifetimes: Punctuated[RustGenericParam, RustComma] = _coerce_union_4_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_to_punct_variant_generic_param_token_comma(lifetimes)
        self.greater_than: RustGreaterThan = _coerce_union_2_token_greater_than_none_to_token_greater_than(greater_than)

    @no_type_check
    def derive(self, for_keyword: 'RustForKeyword | None' = None, less_than: 'RustLessThan | None' = None, lifetimes: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> 'RustBoundLifetimes':
        if for_keyword is None:
            for_keyword = self.for_keyword
        if less_than is None:
            less_than = self.less_than
        if lifetimes is None:
            lifetimes = self.lifetimes
        if greater_than is None:
            greater_than = self.greater_than
        return RustBoundLifetimes(for_keyword=for_keyword, less_than=less_than, lifetimes=lifetimes, greater_than=greater_than)

    def parent(self) -> 'RustBoundLifetimesParent':
        assert(self._parent is not None)
        return self._parent


class RustTraitBound(_RustBaseNode):

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, modifier: 'RustTraitBoundModifier | None' = None, bound_lifetimes: 'RustBoundLifetimes | None' = None) -> None:
        self.modifier: RustTraitBoundModifier | None = _coerce_union_2_node_trait_bound_modifier_none_to_union_2_node_trait_bound_modifier_none(modifier)
        self.bound_lifetimes: RustBoundLifetimes | None = _coerce_union_2_node_bound_lifetimes_none_to_union_2_node_bound_lifetimes_none(bound_lifetimes)
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)

    @no_type_check
    def derive(self, modifier: 'RustTraitBoundModifier | None' = None, bound_lifetimes: 'RustBoundLifetimes | None' = None, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> 'RustTraitBound':
        if modifier is None:
            modifier = self.modifier
        if bound_lifetimes is None:
            bound_lifetimes = self.bound_lifetimes
        if path is None:
            path = self.path
        return RustTraitBound(modifier=modifier, bound_lifetimes=bound_lifetimes, path=path)

    def parent(self) -> 'RustTraitBoundParent':
        assert(self._parent is not None)
        return self._parent


class RustLifetime(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', *, single_quote: 'RustSingleQuote | None' = None) -> None:
        self.single_quote: RustSingleQuote = _coerce_union_2_token_single_quote_none_to_token_single_quote(single_quote)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, single_quote: 'RustSingleQuote | None' = None, name: 'RustIdent | None | str' = None) -> 'RustLifetime':
        if single_quote is None:
            single_quote = self.single_quote
        if name is None:
            name = self.name
        return RustLifetime(single_quote=single_quote, name=name)

    def parent(self) -> 'RustLifetimeParent':
        assert(self._parent is not None)
        return self._parent


class RustAssocType(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', type_expr: 'RustTypeExpr', *, generics: 'RustAngleBracketedGenericArguments | None' = None, equals: 'RustEquals | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.generics: RustAngleBracketedGenericArguments | None = _coerce_union_2_node_angle_bracketed_generic_arguments_none_to_union_2_node_angle_bracketed_generic_arguments_none(generics)
        self.equals: RustEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, generics: 'RustAngleBracketedGenericArguments | None' = None, equals: 'RustEquals | None' = None, type_expr: 'RustTypeExpr | None' = None) -> 'RustAssocType':
        if name is None:
            name = self.name
        if generics is None:
            generics = self.generics
        if equals is None:
            equals = self.equals
        if type_expr is None:
            type_expr = self.type_expr
        return RustAssocType(name=name, generics=generics, equals=equals, type_expr=type_expr)

    def parent(self) -> 'RustAssocTypeParent':
        assert(self._parent is not None)
        return self._parent


class RustAssocConst(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', expr: 'RustExpr', *, generics: 'RustAngleBracketedGenericArguments | None' = None, equals: 'RustEquals | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.generics: RustAngleBracketedGenericArguments | None = _coerce_union_2_node_angle_bracketed_generic_arguments_none_to_union_2_node_angle_bracketed_generic_arguments_none(generics)
        self.equals: RustEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: RustExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, generics: 'RustAngleBracketedGenericArguments | None' = None, equals: 'RustEquals | None' = None, expr: 'RustExpr | None' = None) -> 'RustAssocConst':
        if name is None:
            name = self.name
        if generics is None:
            generics = self.generics
        if equals is None:
            equals = self.equals
        if expr is None:
            expr = self.expr
        return RustAssocConst(name=name, generics=generics, equals=equals, expr=expr)

    def parent(self) -> 'RustAssocConstParent':
        assert(self._parent is not None)
        return self._parent


class RustConstraint(_RustBaseNode):

    def count_bounds(self) -> int:
        return len(self.bounds)

    def __init__(self, name: 'RustIdent | str', *, generics: 'RustAngleBracketedGenericArguments | None' = None, colon: 'RustColon | None' = None, bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus] | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.generics: RustAngleBracketedGenericArguments = _coerce_union_2_node_angle_bracketed_generic_arguments_none_to_node_angle_bracketed_generic_arguments(generics)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.bounds: Punctuated[RustTypeParamBound, RustPlus] = _coerce_union_4_list_variant_type_param_bound_list_tuple_2_variant_type_param_bound_union_2_token_plus_none_punct_variant_type_param_bound_token_plus_none_to_punct_variant_type_param_bound_token_plus(bounds)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, generics: 'RustAngleBracketedGenericArguments | None' = None, colon: 'RustColon | None' = None, bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus] | None' = None) -> 'RustConstraint':
        if name is None:
            name = self.name
        if generics is None:
            generics = self.generics
        if colon is None:
            colon = self.colon
        if bounds is None:
            bounds = self.bounds
        return RustConstraint(name=name, generics=generics, colon=colon, bounds=bounds)

    def parent(self) -> 'RustConstraintParent':
        assert(self._parent is not None)
        return self._parent


class RustTurbofish(_RustBaseNode):

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, *, colon_colon: 'RustColonColon | None' = None, less_than: 'RustLessThan | None' = None, args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | Punctuated[RustGenericArgument, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.colon_colon: RustColonColon = _coerce_union_2_token_colon_colon_none_to_token_colon_colon(colon_colon)
        self.less_than: RustLessThan = _coerce_union_2_token_less_than_none_to_token_less_than(less_than)
        self.args: Punctuated[RustGenericArgument, RustComma] = _coerce_union_4_list_variant_generic_argument_list_tuple_2_variant_generic_argument_union_2_token_comma_none_punct_variant_generic_argument_token_comma_none_to_punct_variant_generic_argument_token_comma(args)
        self.greater_than: RustGreaterThan = _coerce_union_2_token_greater_than_none_to_token_greater_than(greater_than)

    @no_type_check
    def derive(self, colon_colon: 'RustColonColon | None' = None, less_than: 'RustLessThan | None' = None, args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | Punctuated[RustGenericArgument, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> 'RustTurbofish':
        if colon_colon is None:
            colon_colon = self.colon_colon
        if less_than is None:
            less_than = self.less_than
        if args is None:
            args = self.args
        if greater_than is None:
            greater_than = self.greater_than
        return RustTurbofish(colon_colon=colon_colon, less_than=less_than, args=args, greater_than=greater_than)

    def parent(self) -> 'RustTurbofishParent':
        assert(self._parent is not None)
        return self._parent


class RustAngleBracketedGenericArguments(_RustBaseNode):

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, *, less_than: 'RustLessThan | None' = None, args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | Punctuated[RustGenericArgument, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.less_than: RustLessThan = _coerce_union_2_token_less_than_none_to_token_less_than(less_than)
        self.args: Punctuated[RustGenericArgument, RustComma] = _coerce_union_4_list_variant_generic_argument_list_tuple_2_variant_generic_argument_union_2_token_comma_none_punct_variant_generic_argument_token_comma_none_to_punct_variant_generic_argument_token_comma(args)
        self.greater_than: RustGreaterThan = _coerce_union_2_token_greater_than_none_to_token_greater_than(greater_than)

    @no_type_check
    def derive(self, less_than: 'RustLessThan | None' = None, args: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | Punctuated[RustGenericArgument, RustComma] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> 'RustAngleBracketedGenericArguments':
        if less_than is None:
            less_than = self.less_than
        if args is None:
            args = self.args
        if greater_than is None:
            greater_than = self.greater_than
        return RustAngleBracketedGenericArguments(less_than=less_than, args=args, greater_than=greater_than)

    def parent(self) -> 'RustAngleBracketedGenericArgumentsParent':
        assert(self._parent is not None)
        return self._parent


class RustParenthesizedGenericArguments(_RustBaseNode):

    def count_params(self) -> int:
        return len(self.params)

    def __init__(self, result: 'RustTypeExpr', *, open_paren: 'RustOpenParen | None' = None, params: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None, r_arrow: 'RustRArrow | None' = None) -> None:
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.params: Punctuated[RustTypeExpr, RustComma] = _coerce_union_4_list_variant_type_expr_list_tuple_2_variant_type_expr_union_2_token_comma_none_punct_variant_type_expr_token_comma_none_to_punct_variant_type_expr_token_comma(params)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)
        self.r_arrow: RustRArrow = _coerce_union_2_token_r_arrow_none_to_token_r_arrow(r_arrow)
        self.result: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(result)

    @no_type_check
    def derive(self, open_paren: 'RustOpenParen | None' = None, params: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None, r_arrow: 'RustRArrow | None' = None, result: 'RustTypeExpr | None' = None) -> 'RustParenthesizedGenericArguments':
        if open_paren is None:
            open_paren = self.open_paren
        if params is None:
            params = self.params
        if close_paren is None:
            close_paren = self.close_paren
        if r_arrow is None:
            r_arrow = self.r_arrow
        if result is None:
            result = self.result
        return RustParenthesizedGenericArguments(open_paren=open_paren, params=params, close_paren=close_paren, r_arrow=r_arrow, result=result)

    def parent(self) -> 'RustParenthesizedGenericArgumentsParent':
        assert(self._parent is not None)
        return self._parent


class RustPathSegment(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', *, args: 'RustPathArguments | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.args: RustPathArguments | None = _coerce_union_2_variant_path_arguments_none_to_union_2_variant_path_arguments_none(args)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, args: 'RustPathArguments | None' = None) -> 'RustPathSegment':
        if name is None:
            name = self.name
        if args is None:
            args = self.args
        return RustPathSegment(name=name, args=args)

    def parent(self) -> 'RustPathSegmentParent':
        assert(self._parent is not None)
        return self._parent


class RustPath(_RustBaseNode):

    def count_segments(self) -> int:
        return len(self.segments)

    def __init__(self, segments: 'Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, leading_colon_colon: 'RustColonColon | None' = None) -> None:
        self.leading_colon_colon: RustColonColon | None = _coerce_union_2_token_colon_colon_none_to_union_2_token_colon_colon_none(leading_colon_colon)
        self.segments: Punctuated[RustPathSegment, RustColonColon] = _coerce_union_3_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_punct_node_path_segment_token_colon_colon_required(segments)

    @no_type_check
    def derive(self, leading_colon_colon: 'RustColonColon | None' = None, segments: 'Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> 'RustPath':
        if leading_colon_colon is None:
            leading_colon_colon = self.leading_colon_colon
        if segments is None:
            segments = self.segments
        return RustPath(leading_colon_colon=leading_colon_colon, segments=segments)

    def parent(self) -> 'RustPathParent':
        assert(self._parent is not None)
        return self._parent


class RustQself(_RustBaseNode):

    def __init__(self, type_expr: 'RustTypeExpr', path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, less_than: 'RustLessThan | None' = None, as_keyword: 'RustAsKeyword | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.less_than: RustLessThan = _coerce_union_2_token_less_than_none_to_token_less_than(less_than)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)
        self.as_keyword: RustAsKeyword = _coerce_union_2_token_as_keyword_none_to_token_as_keyword(as_keyword)
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)
        self.greater_than: RustGreaterThan = _coerce_union_2_token_greater_than_none_to_token_greater_than(greater_than)

    @no_type_check
    def derive(self, less_than: 'RustLessThan | None' = None, type_expr: 'RustTypeExpr | None' = None, as_keyword: 'RustAsKeyword | None' = None, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, greater_than: 'RustGreaterThan | None' = None) -> 'RustQself':
        if less_than is None:
            less_than = self.less_than
        if type_expr is None:
            type_expr = self.type_expr
        if as_keyword is None:
            as_keyword = self.as_keyword
        if path is None:
            path = self.path
        if greater_than is None:
            greater_than = self.greater_than
        return RustQself(less_than=less_than, type_expr=type_expr, as_keyword=as_keyword, path=path, greater_than=greater_than)

    def parent(self) -> 'RustQselfParent':
        assert(self._parent is not None)
        return self._parent


class RustPathTypeExpr(_RustBaseNode):

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, qself: 'RustQself | None' = None) -> None:
        self.qself: RustQself | None = _coerce_union_2_node_qself_none_to_union_2_node_qself_none(qself)
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)

    @no_type_check
    def derive(self, qself: 'RustQself | None' = None, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> 'RustPathTypeExpr':
        if qself is None:
            qself = self.qself
        if path is None:
            path = self.path
        return RustPathTypeExpr(qself=qself, path=path)

    def parent(self) -> 'RustPathTypeExprParent':
        assert(self._parent is not None)
        return self._parent


class RustArrayTypeExpr(_RustBaseNode):

    def __init__(self, type_expr: 'RustTypeExpr', expr: 'RustExpr', *, open_bracket: 'RustOpenBracket | None' = None, semicolon: 'RustSemicolon | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.open_bracket: RustOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)
        self.semicolon: RustSemicolon = _coerce_union_2_token_semicolon_none_to_token_semicolon(semicolon)
        self.expr: RustExpr = _coerce_variant_expr_to_variant_expr(expr)
        self.close_bracket: RustCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, open_bracket: 'RustOpenBracket | None' = None, type_expr: 'RustTypeExpr | None' = None, semicolon: 'RustSemicolon | None' = None, expr: 'RustExpr | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> 'RustArrayTypeExpr':
        if open_bracket is None:
            open_bracket = self.open_bracket
        if type_expr is None:
            type_expr = self.type_expr
        if semicolon is None:
            semicolon = self.semicolon
        if expr is None:
            expr = self.expr
        if close_bracket is None:
            close_bracket = self.close_bracket
        return RustArrayTypeExpr(open_bracket=open_bracket, type_expr=type_expr, semicolon=semicolon, expr=expr, close_bracket=close_bracket)

    def parent(self) -> 'RustArrayTypeExprParent':
        assert(self._parent is not None)
        return self._parent


class RustNeverTypeExpr(_RustBaseNode):

    def __init__(self, *, exclamation_mark: 'RustExclamationMark | None' = None) -> None:
        self.exclamation_mark: RustExclamationMark = _coerce_union_2_token_exclamation_mark_none_to_token_exclamation_mark(exclamation_mark)

    @no_type_check
    def derive(self, exclamation_mark: 'RustExclamationMark | None' = None) -> 'RustNeverTypeExpr':
        if exclamation_mark is None:
            exclamation_mark = self.exclamation_mark
        return RustNeverTypeExpr(exclamation_mark=exclamation_mark)

    def parent(self) -> 'RustNeverTypeExprParent':
        assert(self._parent is not None)
        return self._parent


class RustTupleTypeExpr(_RustBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, open_paren: 'RustOpenParen | None' = None, elements: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.elements: Punctuated[RustTypeExpr, RustComma] = _coerce_union_4_list_variant_type_expr_list_tuple_2_variant_type_expr_union_2_token_comma_none_punct_variant_type_expr_token_comma_none_to_punct_variant_type_expr_token_comma(elements)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, open_paren: 'RustOpenParen | None' = None, elements: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> 'RustTupleTypeExpr':
        if open_paren is None:
            open_paren = self.open_paren
        if elements is None:
            elements = self.elements
        if close_paren is None:
            close_paren = self.close_paren
        return RustTupleTypeExpr(open_paren=open_paren, elements=elements, close_paren=close_paren)

    def parent(self) -> 'RustTupleTypeExprParent':
        assert(self._parent is not None)
        return self._parent


class RustNamedPattern(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, ref_keyword: 'RustRefKeyword | None' = None, mut_keyword: 'RustMutKeyword | None' = None, sub: 'RustNamedPattern | RustPattern | RustIdent | tuple[RustAtSign | None, RustNamedPattern | RustPattern | RustIdent | str] | None | str' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.ref_keyword: RustRefKeyword | None = _coerce_union_2_token_ref_keyword_none_to_union_2_token_ref_keyword_none(ref_keyword)
        self.mut_keyword: RustMutKeyword | None = _coerce_union_2_token_mut_keyword_none_to_union_2_token_mut_keyword_none(mut_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.sub: tuple[RustAtSign, RustPattern] | None = _coerce_union_6_node_named_pattern_node_pattern_token_ident_tuple_2_union_2_token_at_sign_none_union_4_node_named_pattern_node_pattern_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_at_sign_node_pattern_none(sub)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, ref_keyword: 'RustRefKeyword | None' = None, mut_keyword: 'RustMutKeyword | None' = None, name: 'RustIdent | None | str' = None, sub: 'RustNamedPattern | RustPattern | RustIdent | tuple[RustAtSign | None, RustNamedPattern | RustPattern | RustIdent | str] | None | str' = None) -> 'RustNamedPattern':
        if attrs is None:
            attrs = self.attrs
        if ref_keyword is None:
            ref_keyword = self.ref_keyword
        if mut_keyword is None:
            mut_keyword = self.mut_keyword
        if name is None:
            name = self.name
        if sub is None:
            sub = self.sub
        return RustNamedPattern(attrs=attrs, ref_keyword=ref_keyword, mut_keyword=mut_keyword, name=name, sub=sub)

    def parent(self) -> 'RustNamedPatternParent':
        assert(self._parent is not None)
        return self._parent


class RustPattern(_RustBaseNode):

    def __init__(self, named_pattern: 'RustNamedPattern | RustIdent | str') -> None:
        self.named_pattern: RustNamedPattern = _coerce_union_3_node_named_pattern_token_ident_extern_string_to_node_named_pattern(named_pattern)

    @no_type_check
    def derive(self, named_pattern: 'RustNamedPattern | RustIdent | None | str' = None) -> 'RustPattern':
        if named_pattern is None:
            named_pattern = self.named_pattern
        return RustPattern(named_pattern=named_pattern)

    def parent(self) -> 'RustPatternParent':
        assert(self._parent is not None)
        return self._parent


class RustPathExpr(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, qself: 'RustQself | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.qself: RustQself | None = _coerce_union_2_node_qself_none_to_union_2_node_qself_none(qself)
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, qself: 'RustQself | None' = None, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> 'RustPathExpr':
        if attrs is None:
            attrs = self.attrs
        if qself is None:
            qself = self.qself
        if path is None:
            path = self.path
        return RustPathExpr(attrs=attrs, qself=qself, path=path)

    def parent(self) -> 'RustPathExprParent':
        assert(self._parent is not None)
        return self._parent


class RustLitExpr(_RustBaseNode):

    def __init__(self, literal: 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | float | str') -> None:
        self.literal: RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword = _coerce_union_7_token_char_token_false_keyword_token_float_token_string_token_true_keyword_extern_float_extern_string_to_union_5_token_char_token_false_keyword_token_float_token_string_token_true_keyword(literal)

    @no_type_check
    def derive(self, literal: 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | None | float | str' = None) -> 'RustLitExpr':
        if literal is None:
            literal = self.literal
        return RustLitExpr(literal=literal)

    def parent(self) -> 'RustLitExprParent':
        assert(self._parent is not None)
        return self._parent


class RustInit(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', value: 'RustExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.equals: RustEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.value: RustExpr = _coerce_variant_expr_to_variant_expr(value)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, equals: 'RustEquals | None' = None, value: 'RustExpr | None' = None) -> 'RustInit':
        if name is None:
            name = self.name
        if equals is None:
            equals = self.equals
        if value is None:
            value = self.value
        return RustInit(name=name, equals=equals, value=value)

    def parent(self) -> 'RustInitParent':
        assert(self._parent is not None)
        return self._parent


class RustStructExpr(_RustBaseNode):

    def count_field_(self) -> int:
        return len(self.field_)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, open_brace: 'RustOpenBrace | None' = None, field_: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | Punctuated[RustInit, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.field_: Punctuated[RustInit, RustComma] = _coerce_union_4_list_node_init_list_tuple_2_node_init_union_2_token_comma_none_punct_node_init_token_comma_none_to_punct_node_init_token_comma(field_)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, open_brace: 'RustOpenBrace | None' = None, field_: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | Punctuated[RustInit, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustStructExpr':
        if path is None:
            path = self.path
        if open_brace is None:
            open_brace = self.open_brace
        if field_ is None:
            field_ = self.field_
        if comma is None:
            comma = self.comma
        if close_brace is None:
            close_brace = self.close_brace
        return RustStructExpr(path=path, open_brace=open_brace, field_=field_, comma=comma, close_brace=close_brace)

    def parent(self) -> 'RustStructExprParent':
        assert(self._parent is not None)
        return self._parent


class RustCallExpr(_RustBaseNode):

    def count_args(self) -> int:
        return len(self.args)

    def __init__(self, operator: 'RustExpr', *, open_paren: 'RustOpenParen | None' = None, args: 'Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | Punctuated[RustExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.operator: RustExpr = _coerce_variant_expr_to_variant_expr(operator)
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.args: Punctuated[RustExpr, RustComma] = _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(args)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, operator: 'RustExpr | None' = None, open_paren: 'RustOpenParen | None' = None, args: 'Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | Punctuated[RustExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> 'RustCallExpr':
        if operator is None:
            operator = self.operator
        if open_paren is None:
            open_paren = self.open_paren
        if args is None:
            args = self.args
        if close_paren is None:
            close_paren = self.close_paren
        return RustCallExpr(operator=operator, open_paren=open_paren, args=args, close_paren=close_paren)

    def parent(self) -> 'RustCallExprParent':
        assert(self._parent is not None)
        return self._parent


class RustRetExpr(_RustBaseNode):

    def __init__(self, expr: 'RustExpr', *, return_keyword: 'RustReturnKeyword | None' = None) -> None:
        self.return_keyword: RustReturnKeyword = _coerce_union_2_token_return_keyword_none_to_token_return_keyword(return_keyword)
        self.expr: RustExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, return_keyword: 'RustReturnKeyword | None' = None, expr: 'RustExpr | None' = None) -> 'RustRetExpr':
        if return_keyword is None:
            return_keyword = self.return_keyword
        if expr is None:
            expr = self.expr
        return RustRetExpr(return_keyword=return_keyword, expr=expr)

    def parent(self) -> 'RustRetExprParent':
        assert(self._parent is not None)
        return self._parent


class RustBlockExpr(_RustBaseNode):

    def __init__(self, item: 'RustItem', last: 'RustExpr', *, open_brace: 'RustOpenBrace | None' = None, semicolon: 'RustSemicolon | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.item: RustItem = _coerce_variant_item_to_variant_item(item)
        self.semicolon: RustSemicolon = _coerce_union_2_token_semicolon_none_to_token_semicolon(semicolon)
        self.last: RustExpr = _coerce_variant_expr_to_variant_expr(last)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, open_brace: 'RustOpenBrace | None' = None, item: 'RustItem | None' = None, semicolon: 'RustSemicolon | None' = None, last: 'RustExpr | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustBlockExpr':
        if open_brace is None:
            open_brace = self.open_brace
        if item is None:
            item = self.item
        if semicolon is None:
            semicolon = self.semicolon
        if last is None:
            last = self.last
        if close_brace is None:
            close_brace = self.close_brace
        return RustBlockExpr(open_brace=open_brace, item=item, semicolon=semicolon, last=last, close_brace=close_brace)

    def parent(self) -> 'RustBlockExprParent':
        assert(self._parent is not None)
        return self._parent


class RustAbi(_RustBaseNode):

    def __init__(self, name: 'RustString | str', *, extern_keyword: 'RustExternKeyword | None' = None) -> None:
        self.extern_keyword: RustExternKeyword = _coerce_union_2_token_extern_keyword_none_to_token_extern_keyword(extern_keyword)
        self.name: RustString = _coerce_union_2_token_string_extern_string_to_token_string(name)

    @no_type_check
    def derive(self, extern_keyword: 'RustExternKeyword | None' = None, name: 'RustString | None | str' = None) -> 'RustAbi':
        if extern_keyword is None:
            extern_keyword = self.extern_keyword
        if name is None:
            name = self.name
        return RustAbi(extern_keyword=extern_keyword, name=name)

    def parent(self) -> 'RustAbiParent':
        assert(self._parent is not None)
        return self._parent


class RustVariadicArg(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, pattern: 'RustNamedPattern | RustPattern | RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, dot_dot_dot: 'RustDotDotDot | None' = None, comma: 'RustComma | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.pattern: RustPattern = _coerce_union_4_node_named_pattern_node_pattern_token_ident_extern_string_to_node_pattern(pattern)
        self.dot_dot_dot: RustDotDotDot | None = _coerce_union_2_token_dot_dot_dot_none_to_union_2_token_dot_dot_dot_none(dot_dot_dot)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, pattern: 'RustNamedPattern | RustPattern | RustIdent | None | str' = None, dot_dot_dot: 'RustDotDotDot | None' = None, comma: 'RustComma | None' = None) -> 'RustVariadicArg':
        if attrs is None:
            attrs = self.attrs
        if pattern is None:
            pattern = self.pattern
        if dot_dot_dot is None:
            dot_dot_dot = self.dot_dot_dot
        if comma is None:
            comma = self.comma
        return RustVariadicArg(attrs=attrs, pattern=pattern, dot_dot_dot=dot_dot_dot, comma=comma)

    def parent(self) -> 'RustVariadicArgParent':
        assert(self._parent is not None)
        return self._parent


class RustSelfArg(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, type_expr: 'RustTypeExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, reference: 'RustLifetime | RustIdent | tuple[RustAmpersand | None, RustLifetime | RustIdent | str] | None | str' = None, mut_keyword: 'RustMutKeyword | None' = None, self_keyword: 'RustSelfKeyword | None' = None, colon: 'RustColon | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.reference: tuple[RustAmpersand, RustLifetime] | None = _coerce_union_5_node_lifetime_token_ident_tuple_2_union_2_token_ampersand_none_union_3_node_lifetime_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_ampersand_node_lifetime_none(reference)
        self.mut_keyword: RustMutKeyword | None = _coerce_union_2_token_mut_keyword_none_to_union_2_token_mut_keyword_none(mut_keyword)
        self.self_keyword: RustSelfKeyword = _coerce_union_2_token_self_keyword_none_to_token_self_keyword(self_keyword)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, reference: 'RustLifetime | RustIdent | tuple[RustAmpersand | None, RustLifetime | RustIdent | str] | None | str' = None, mut_keyword: 'RustMutKeyword | None' = None, self_keyword: 'RustSelfKeyword | None' = None, colon: 'RustColon | None' = None, type_expr: 'RustTypeExpr | None' = None) -> 'RustSelfArg':
        if attrs is None:
            attrs = self.attrs
        if reference is None:
            reference = self.reference
        if mut_keyword is None:
            mut_keyword = self.mut_keyword
        if self_keyword is None:
            self_keyword = self.self_keyword
        if colon is None:
            colon = self.colon
        if type_expr is None:
            type_expr = self.type_expr
        return RustSelfArg(attrs=attrs, reference=reference, mut_keyword=mut_keyword, self_keyword=self_keyword, colon=colon, type_expr=type_expr)

    def parent(self) -> 'RustSelfArgParent':
        assert(self._parent is not None)
        return self._parent


class RustTypedArg(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, pattern: 'RustNamedPattern | RustPattern | RustIdent | str', type_expr: 'RustTypeExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, colon: 'RustColon | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.pattern: RustPattern = _coerce_union_4_node_named_pattern_node_pattern_token_ident_extern_string_to_node_pattern(pattern)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, pattern: 'RustNamedPattern | RustPattern | RustIdent | None | str' = None, colon: 'RustColon | None' = None, type_expr: 'RustTypeExpr | None' = None) -> 'RustTypedArg':
        if attrs is None:
            attrs = self.attrs
        if pattern is None:
            pattern = self.pattern
        if colon is None:
            colon = self.colon
        if type_expr is None:
            type_expr = self.type_expr
        return RustTypedArg(attrs=attrs, pattern=pattern, colon=colon, type_expr=type_expr)

    def parent(self) -> 'RustTypedArgParent':
        assert(self._parent is not None)
        return self._parent


class RustLifetimePredicate(_RustBaseNode):

    def count_bounds(self) -> int:
        return len(self.bounds)

    def __init__(self, lifetime: 'RustLifetime | RustIdent | str', bounds: 'Sequence[tuple[RustLifetime | RustIdent | str, RustPlus | None]] | Sequence[RustLifetime | RustIdent | str] | Punctuated[RustLifetime | RustIdent | str, RustPlus]', *, colon: 'RustColon | None' = None) -> None:
        self.lifetime: RustLifetime = _coerce_union_3_node_lifetime_token_ident_extern_string_to_node_lifetime(lifetime)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.bounds: Punctuated[RustLifetime, RustPlus] = _coerce_union_3_list_tuple_2_union_3_node_lifetime_token_ident_extern_string_union_2_token_plus_none_required_list_union_3_node_lifetime_token_ident_extern_string_required_punct_union_3_node_lifetime_token_ident_extern_string_token_plus_required_to_punct_node_lifetime_token_plus_required(bounds)

    @no_type_check
    def derive(self, lifetime: 'RustLifetime | RustIdent | None | str' = None, colon: 'RustColon | None' = None, bounds: 'Sequence[tuple[RustLifetime | RustIdent | str, RustPlus | None]] | Sequence[RustLifetime | RustIdent | str] | Punctuated[RustLifetime | RustIdent | str, RustPlus] | None' = None) -> 'RustLifetimePredicate':
        if lifetime is None:
            lifetime = self.lifetime
        if colon is None:
            colon = self.colon
        if bounds is None:
            bounds = self.bounds
        return RustLifetimePredicate(lifetime=lifetime, colon=colon, bounds=bounds)

    def parent(self) -> 'RustLifetimePredicateParent':
        assert(self._parent is not None)
        return self._parent


class RustTypePredicate(_RustBaseNode):

    def count_bounds(self) -> int:
        return len(self.bounds)

    def __init__(self, type_expr: 'RustTypeExpr', bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus]', *, bound_lifetimes: 'RustBoundLifetimes | None' = None, colon: 'RustColon | None' = None) -> None:
        self.bound_lifetimes: RustBoundLifetimes = _coerce_union_2_node_bound_lifetimes_none_to_node_bound_lifetimes(bound_lifetimes)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.bounds: Punctuated[RustTypeParamBound, RustPlus] = _coerce_union_3_list_variant_type_param_bound_required_list_tuple_2_variant_type_param_bound_union_2_token_plus_none_required_punct_variant_type_param_bound_token_plus_required_to_punct_variant_type_param_bound_token_plus_required(bounds)

    @no_type_check
    def derive(self, bound_lifetimes: 'RustBoundLifetimes | None' = None, type_expr: 'RustTypeExpr | None' = None, colon: 'RustColon | None' = None, bounds: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus] | None' = None) -> 'RustTypePredicate':
        if bound_lifetimes is None:
            bound_lifetimes = self.bound_lifetimes
        if type_expr is None:
            type_expr = self.type_expr
        if colon is None:
            colon = self.colon
        if bounds is None:
            bounds = self.bounds
        return RustTypePredicate(bound_lifetimes=bound_lifetimes, type_expr=type_expr, colon=colon, bounds=bounds)

    def parent(self) -> 'RustTypePredicateParent':
        assert(self._parent is not None)
        return self._parent


class RustGenerics(_RustBaseNode):

    def __init__(self, *, params: 'tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None' = None, where_clause: 'tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma] | None' = None) -> None:
        self.params: tuple[RustLessThan, Punctuated[RustGenericParam, RustComma], RustGreaterThan] | None = _coerce_union_5_tuple_3_union_2_token_less_than_none_union_4_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_union_2_token_greater_than_none_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_to_union_2_tuple_3_token_less_than_punct_variant_generic_param_token_comma_token_greater_than_none(params)
        self.where_clause: tuple[RustWhereKeyword, Punctuated[RustWherePredicate, RustComma]] | None = _coerce_union_5_tuple_2_union_2_token_where_keyword_none_union_3_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_none_to_union_2_tuple_2_token_where_keyword_punct_variant_where_predicate_token_comma_required_none(where_clause)

    @no_type_check
    def derive(self, params: 'tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None' = None, where_clause: 'tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma] | None' = None) -> 'RustGenerics':
        if params is None:
            params = self.params
        if where_clause is None:
            where_clause = self.where_clause
        return RustGenerics(params=params, where_clause=where_clause)

    def parent(self) -> 'RustGenericsParent':
        assert(self._parent is not None)
        return self._parent


class RustSignature(_RustBaseNode):

    def count_inputs(self) -> int:
        return len(self.inputs)

    def __init__(self, name: 'RustIdent | str', *, const_keyword: 'RustConstKeyword | None' = None, async_keyword: 'RustAsyncKeyword | None' = None, unsafe_keyword: 'RustUnsafeKeyword | None' = None, abi: 'RustAbi | RustString | None | str' = None, fn_keyword: 'RustFnKeyword | None' = None, generics: 'RustGenerics | None' = None, open_paren: 'RustOpenParen | None' = None, inputs: 'Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | Punctuated[RustArg, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None, output: 'RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None' = None) -> None:
        self.const_keyword: RustConstKeyword | None = _coerce_union_2_token_const_keyword_none_to_union_2_token_const_keyword_none(const_keyword)
        self.async_keyword: RustAsyncKeyword | None = _coerce_union_2_token_async_keyword_none_to_union_2_token_async_keyword_none(async_keyword)
        self.unsafe_keyword: RustUnsafeKeyword | None = _coerce_union_2_token_unsafe_keyword_none_to_union_2_token_unsafe_keyword_none(unsafe_keyword)
        self.abi: RustAbi | None = _coerce_union_4_node_abi_token_string_none_extern_string_to_union_2_node_abi_none(abi)
        self.fn_keyword: RustFnKeyword = _coerce_union_2_token_fn_keyword_none_to_token_fn_keyword(fn_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.generics: RustGenerics = _coerce_union_2_node_generics_none_to_node_generics(generics)
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.inputs: Punctuated[RustArg, RustComma] = _coerce_union_4_list_variant_arg_list_tuple_2_variant_arg_union_2_token_comma_none_punct_variant_arg_token_comma_none_to_punct_variant_arg_token_comma(inputs)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)
        self.output: tuple[RustRArrow, RustTypeExpr] | None = _coerce_union_3_variant_type_expr_tuple_2_union_2_token_r_arrow_none_variant_type_expr_none_to_union_2_tuple_2_token_r_arrow_variant_type_expr_none(output)

    @no_type_check
    def derive(self, const_keyword: 'RustConstKeyword | None' = None, async_keyword: 'RustAsyncKeyword | None' = None, unsafe_keyword: 'RustUnsafeKeyword | None' = None, abi: 'RustAbi | RustString | None | str' = None, fn_keyword: 'RustFnKeyword | None' = None, name: 'RustIdent | None | str' = None, generics: 'RustGenerics | None' = None, open_paren: 'RustOpenParen | None' = None, inputs: 'Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | Punctuated[RustArg, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None, output: 'RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None' = None) -> 'RustSignature':
        if const_keyword is None:
            const_keyword = self.const_keyword
        if async_keyword is None:
            async_keyword = self.async_keyword
        if unsafe_keyword is None:
            unsafe_keyword = self.unsafe_keyword
        if abi is None:
            abi = self.abi
        if fn_keyword is None:
            fn_keyword = self.fn_keyword
        if name is None:
            name = self.name
        if generics is None:
            generics = self.generics
        if open_paren is None:
            open_paren = self.open_paren
        if inputs is None:
            inputs = self.inputs
        if close_paren is None:
            close_paren = self.close_paren
        if output is None:
            output = self.output
        return RustSignature(const_keyword=const_keyword, async_keyword=async_keyword, unsafe_keyword=unsafe_keyword, abi=abi, fn_keyword=fn_keyword, name=name, generics=generics, open_paren=open_paren, inputs=inputs, close_paren=close_paren, output=output)

    def parent(self) -> 'RustSignatureParent':
        assert(self._parent is not None)
        return self._parent


class RustField(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', type_expr: 'RustTypeExpr', *, colon: 'RustColon | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.colon: RustColon = _coerce_union_2_token_colon_none_to_token_colon(colon)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, colon: 'RustColon | None' = None, type_expr: 'RustTypeExpr | None' = None) -> 'RustField':
        if name is None:
            name = self.name
        if colon is None:
            colon = self.colon
        if type_expr is None:
            type_expr = self.type_expr
        return RustField(name=name, colon=colon, type_expr=type_expr)

    def parent(self) -> 'RustFieldParent':
        assert(self._parent is not None)
        return self._parent


class RustStructVariant(_RustBaseNode):

    def count_fields(self) -> int:
        return len(self.fields)

    def __init__(self, name: 'RustIdent | str', *, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.fields: Punctuated[RustField, RustComma] = _coerce_union_4_list_node_field_list_tuple_2_node_field_union_2_token_comma_none_punct_node_field_token_comma_none_to_punct_node_field_token_comma(fields)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustStructVariant':
        if name is None:
            name = self.name
        if open_brace is None:
            open_brace = self.open_brace
        if fields is None:
            fields = self.fields
        if comma is None:
            comma = self.comma
        if close_brace is None:
            close_brace = self.close_brace
        return RustStructVariant(name=name, open_brace=open_brace, fields=fields, comma=comma, close_brace=close_brace)

    def parent(self) -> 'RustStructVariantParent':
        assert(self._parent is not None)
        return self._parent


class RustTupleVariant(_RustBaseNode):

    def count_types(self) -> int:
        return len(self.types)

    def __init__(self, name: 'RustIdent | str', *, open_paren: 'RustOpenParen | None' = None, types: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.types: Punctuated[RustTypeExpr, RustComma] = _coerce_union_4_list_variant_type_expr_list_tuple_2_variant_type_expr_union_2_token_comma_none_punct_variant_type_expr_token_comma_none_to_punct_variant_type_expr_token_comma(types)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, open_paren: 'RustOpenParen | None' = None, types: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None' = None, close_paren: 'RustCloseParen | None' = None) -> 'RustTupleVariant':
        if name is None:
            name = self.name
        if open_paren is None:
            open_paren = self.open_paren
        if types is None:
            types = self.types
        if close_paren is None:
            close_paren = self.close_paren
        return RustTupleVariant(name=name, open_paren=open_paren, types=types, close_paren=close_paren)

    def parent(self) -> 'RustTupleVariantParent':
        assert(self._parent is not None)
        return self._parent


class RustEmptyVariant(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', *, init: 'RustInit | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.init: RustInit | None = _coerce_union_2_node_init_none_to_union_2_node_init_none(init)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, init: 'RustInit | None' = None) -> 'RustEmptyVariant':
        if name is None:
            name = self.name
        if init is None:
            init = self.init
        return RustEmptyVariant(name=name, init=init)

    def parent(self) -> 'RustEmptyVariantParent':
        assert(self._parent is not None)
        return self._parent


class RustEnumItem(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_variants(self) -> int:
        return len(self.variants)

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, enum_keyword: 'RustEnumKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, variants: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | Punctuated[RustVariant, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.visibility: RustPublic | None = _coerce_union_2_node_public_none_to_union_2_node_public_none(visibility)
        self.enum_keyword: RustEnumKeyword = _coerce_union_2_token_enum_keyword_none_to_token_enum_keyword(enum_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.variants: Punctuated[RustVariant, RustComma] = _coerce_union_4_list_variant_variant_list_tuple_2_variant_variant_union_2_token_comma_none_punct_variant_variant_token_comma_none_to_punct_variant_variant_token_comma(variants)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, enum_keyword: 'RustEnumKeyword | None' = None, name: 'RustIdent | None | str' = None, open_brace: 'RustOpenBrace | None' = None, variants: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | Punctuated[RustVariant, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustEnumItem':
        if attrs is None:
            attrs = self.attrs
        if visibility is None:
            visibility = self.visibility
        if enum_keyword is None:
            enum_keyword = self.enum_keyword
        if name is None:
            name = self.name
        if open_brace is None:
            open_brace = self.open_brace
        if variants is None:
            variants = self.variants
        if comma is None:
            comma = self.comma
        if close_brace is None:
            close_brace = self.close_brace
        return RustEnumItem(attrs=attrs, visibility=visibility, enum_keyword=enum_keyword, name=name, open_brace=open_brace, variants=variants, comma=comma, close_brace=close_brace)

    def parent(self) -> 'RustEnumItemParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaPath(_RustBaseNode):

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]') -> None:
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)

    @no_type_check
    def derive(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None) -> 'RustMetaPath':
        if path is None:
            path = self.path
        return RustMetaPath(path=path)

    def parent(self) -> 'RustMetaPathParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaBraced(_RustBaseNode):

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, open_brace: 'RustOpenBrace | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.tokens: Sequence[RustToken] = _coerce_union_2_list_variant_token_none_to_list_variant_token(tokens)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, open_brace: 'RustOpenBrace | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustMetaBraced':
        if path is None:
            path = self.path
        if open_brace is None:
            open_brace = self.open_brace
        if tokens is None:
            tokens = self.tokens
        if close_brace is None:
            close_brace = self.close_brace
        return RustMetaBraced(path=path, open_brace=open_brace, tokens=tokens, close_brace=close_brace)

    def parent(self) -> 'RustMetaBracedParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaParenthesized(_RustBaseNode):

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, open_paren: 'RustOpenParen | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.tokens: Sequence[RustToken] = _coerce_union_2_list_variant_token_none_to_list_variant_token(tokens)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, open_paren: 'RustOpenParen | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_paren: 'RustCloseParen | None' = None) -> 'RustMetaParenthesized':
        if path is None:
            path = self.path
        if open_paren is None:
            open_paren = self.open_paren
        if tokens is None:
            tokens = self.tokens
        if close_paren is None:
            close_paren = self.close_paren
        return RustMetaParenthesized(path=path, open_paren=open_paren, tokens=tokens, close_paren=close_paren)

    def parent(self) -> 'RustMetaParenthesizedParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaBracketed(_RustBaseNode):

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', *, open_bracket: 'RustOpenBracket | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)
        self.open_bracket: RustOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.tokens: Sequence[RustToken] = _coerce_union_2_list_variant_token_none_to_list_variant_token(tokens)
        self.close_bracket: RustCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, open_bracket: 'RustOpenBracket | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> 'RustMetaBracketed':
        if path is None:
            path = self.path
        if open_bracket is None:
            open_bracket = self.open_bracket
        if tokens is None:
            tokens = self.tokens
        if close_bracket is None:
            close_bracket = self.close_bracket
        return RustMetaBracketed(path=path, open_bracket=open_bracket, tokens=tokens, close_bracket=close_bracket)

    def parent(self) -> 'RustMetaBracketedParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaNameValue(_RustBaseNode):

    def __init__(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]', expr: 'RustExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.path: RustPath = _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(path)
        self.equals: RustEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: RustExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, path: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, equals: 'RustEquals | None' = None, expr: 'RustExpr | None' = None) -> 'RustMetaNameValue':
        if path is None:
            path = self.path
        if equals is None:
            equals = self.equals
        if expr is None:
            expr = self.expr
        return RustMetaNameValue(path=path, equals=equals, expr=expr)

    def parent(self) -> 'RustMetaNameValueParent':
        assert(self._parent is not None)
        return self._parent


class RustAttr(_RustBaseNode):

    def __init__(self, meta: 'RustMeta', *, hashtag: 'RustHashtag | None' = None, exclamation_mark: 'RustExclamationMark | None' = None, open_bracket: 'RustOpenBracket | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.hashtag: RustHashtag = _coerce_union_2_token_hashtag_none_to_token_hashtag(hashtag)
        self.exclamation_mark: RustExclamationMark | None = _coerce_union_2_token_exclamation_mark_none_to_union_2_token_exclamation_mark_none(exclamation_mark)
        self.open_bracket: RustOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.meta: RustMeta = _coerce_variant_meta_to_variant_meta(meta)
        self.close_bracket: RustCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, hashtag: 'RustHashtag | None' = None, exclamation_mark: 'RustExclamationMark | None' = None, open_bracket: 'RustOpenBracket | None' = None, meta: 'RustMeta | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> 'RustAttr':
        if hashtag is None:
            hashtag = self.hashtag
        if exclamation_mark is None:
            exclamation_mark = self.exclamation_mark
        if open_bracket is None:
            open_bracket = self.open_bracket
        if meta is None:
            meta = self.meta
        if close_bracket is None:
            close_bracket = self.close_bracket
        return RustAttr(hashtag=hashtag, exclamation_mark=exclamation_mark, open_bracket=open_bracket, meta=meta, close_bracket=close_bracket)

    def parent(self) -> 'RustAttrParent':
        assert(self._parent is not None)
        return self._parent


class RustStructItem(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_fields(self) -> int:
        return len(self.fields)

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, struct_keyword: 'RustStructKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.visibility: RustPublic | None = _coerce_union_2_node_public_none_to_union_2_node_public_none(visibility)
        self.struct_keyword: RustStructKeyword = _coerce_union_2_token_struct_keyword_none_to_token_struct_keyword(struct_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.fields: Punctuated[RustField, RustComma] = _coerce_union_4_list_node_field_list_tuple_2_node_field_union_2_token_comma_none_punct_node_field_token_comma_none_to_punct_node_field_token_comma(fields)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, struct_keyword: 'RustStructKeyword | None' = None, name: 'RustIdent | None | str' = None, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustStructItem':
        if attrs is None:
            attrs = self.attrs
        if visibility is None:
            visibility = self.visibility
        if struct_keyword is None:
            struct_keyword = self.struct_keyword
        if name is None:
            name = self.name
        if open_brace is None:
            open_brace = self.open_brace
        if fields is None:
            fields = self.fields
        if comma is None:
            comma = self.comma
        if close_brace is None:
            close_brace = self.close_brace
        return RustStructItem(attrs=attrs, visibility=visibility, struct_keyword=struct_keyword, name=name, open_brace=open_brace, fields=fields, comma=comma, close_brace=close_brace)

    def parent(self) -> 'RustStructItemParent':
        assert(self._parent is not None)
        return self._parent


class RustExprItem(_RustBaseNode):

    def __init__(self, expr: 'RustExpr') -> None:
        self.expr: RustExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, expr: 'RustExpr | None' = None) -> 'RustExprItem':
        if expr is None:
            expr = self.expr
        return RustExprItem(expr=expr)

    def parent(self) -> 'RustExprItemParent':
        assert(self._parent is not None)
        return self._parent


class RustUsePath(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', tree: 'RustUseTree', *, colon_colon: 'RustColonColon | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.colon_colon: RustColonColon = _coerce_union_2_token_colon_colon_none_to_token_colon_colon(colon_colon)
        self.tree: RustUseTree = _coerce_variant_use_tree_to_variant_use_tree(tree)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, colon_colon: 'RustColonColon | None' = None, tree: 'RustUseTree | None' = None) -> 'RustUsePath':
        if name is None:
            name = self.name
        if colon_colon is None:
            colon_colon = self.colon_colon
        if tree is None:
            tree = self.tree
        return RustUsePath(name=name, colon_colon=colon_colon, tree=tree)

    def parent(self) -> 'RustUsePathParent':
        assert(self._parent is not None)
        return self._parent


class RustUseName(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str') -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None) -> 'RustUseName':
        if name is None:
            name = self.name
        return RustUseName(name=name)

    def parent(self) -> 'RustUseNameParent':
        assert(self._parent is not None)
        return self._parent


class RustUseRename(_RustBaseNode):

    def __init__(self, name: 'RustIdent | str', rename: 'RustIdent | str', *, as_keyword: 'RustAsKeyword | None' = None) -> None:
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.as_keyword: RustAsKeyword = _coerce_union_2_token_as_keyword_none_to_token_as_keyword(as_keyword)
        self.rename: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(rename)

    @no_type_check
    def derive(self, name: 'RustIdent | None | str' = None, as_keyword: 'RustAsKeyword | None' = None, rename: 'RustIdent | None | str' = None) -> 'RustUseRename':
        if name is None:
            name = self.name
        if as_keyword is None:
            as_keyword = self.as_keyword
        if rename is None:
            rename = self.rename
        return RustUseRename(name=name, as_keyword=as_keyword, rename=rename)

    def parent(self) -> 'RustUseRenameParent':
        assert(self._parent is not None)
        return self._parent


class RustUseGlob(_RustBaseNode):

    def __init__(self, *, asterisk: 'RustAsterisk | None' = None) -> None:
        self.asterisk: RustAsterisk = _coerce_union_2_token_asterisk_none_to_token_asterisk(asterisk)

    @no_type_check
    def derive(self, asterisk: 'RustAsterisk | None' = None) -> 'RustUseGlob':
        if asterisk is None:
            asterisk = self.asterisk
        return RustUseGlob(asterisk=asterisk)

    def parent(self) -> 'RustUseGlobParent':
        assert(self._parent is not None)
        return self._parent


class RustUseGroup(_RustBaseNode):

    def count_items(self) -> int:
        return len(self.items)

    def __init__(self, *, open_brace: 'RustOpenBrace | None' = None, items: 'Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | Punctuated[RustUseTree, RustComma] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.items: Punctuated[RustUseTree, RustComma] = _coerce_union_4_list_variant_use_tree_list_tuple_2_variant_use_tree_union_2_token_comma_none_punct_variant_use_tree_token_comma_none_to_punct_variant_use_tree_token_comma(items)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, open_brace: 'RustOpenBrace | None' = None, items: 'Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | Punctuated[RustUseTree, RustComma] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustUseGroup':
        if open_brace is None:
            open_brace = self.open_brace
        if items is None:
            items = self.items
        if close_brace is None:
            close_brace = self.close_brace
        return RustUseGroup(open_brace=open_brace, items=items, close_brace=close_brace)

    def parent(self) -> 'RustUseGroupParent':
        assert(self._parent is not None)
        return self._parent


class RustUseItem(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_path(self) -> int:
        return len(self.path)

    def __init__(self, *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, use_keyword: 'RustUseKeyword | None' = None, colon_colon: 'RustColonColon | None' = None, path: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None' = None, semicolon: 'RustSemicolon | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.visibility: RustPublic | None = _coerce_union_2_node_public_none_to_union_2_node_public_none(visibility)
        self.use_keyword: RustUseKeyword = _coerce_union_2_token_use_keyword_none_to_token_use_keyword(use_keyword)
        self.colon_colon: RustColonColon | None = _coerce_union_2_token_colon_colon_none_to_union_2_token_colon_colon_none(colon_colon)
        self.path: Sequence[tuple[RustIdent, RustColonColon]] = _coerce_union_2_list_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_colon_colon_none_extern_string_none_to_list_tuple_2_token_ident_token_colon_colon(path)
        self.semicolon: RustSemicolon = _coerce_union_2_token_semicolon_none_to_token_semicolon(semicolon)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, use_keyword: 'RustUseKeyword | None' = None, colon_colon: 'RustColonColon | None' = None, path: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None' = None, semicolon: 'RustSemicolon | None' = None) -> 'RustUseItem':
        if attrs is None:
            attrs = self.attrs
        if visibility is None:
            visibility = self.visibility
        if use_keyword is None:
            use_keyword = self.use_keyword
        if colon_colon is None:
            colon_colon = self.colon_colon
        if path is None:
            path = self.path
        if semicolon is None:
            semicolon = self.semicolon
        return RustUseItem(attrs=attrs, visibility=visibility, use_keyword=use_keyword, colon_colon=colon_colon, path=path, semicolon=semicolon)

    def parent(self) -> 'RustUseItemParent':
        assert(self._parent is not None)
        return self._parent


class RustFnImplElement(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, signature: 'RustSignature', item: 'RustItem', last: 'RustExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, default_keyword: 'RustDefaultKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, semicolon: 'RustSemicolon | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.visibility: RustPublic | None = _coerce_union_2_node_public_none_to_union_2_node_public_none(visibility)
        self.default_keyword: RustDefaultKeyword | None = _coerce_union_2_token_default_keyword_none_to_union_2_token_default_keyword_none(default_keyword)
        self.signature: RustSignature = _coerce_node_signature_to_node_signature(signature)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.item: RustItem = _coerce_variant_item_to_variant_item(item)
        self.semicolon: RustSemicolon = _coerce_union_2_token_semicolon_none_to_token_semicolon(semicolon)
        self.last: RustExpr = _coerce_variant_expr_to_variant_expr(last)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, visibility: 'RustPublic | None' = None, default_keyword: 'RustDefaultKeyword | None' = None, signature: 'RustSignature | None' = None, open_brace: 'RustOpenBrace | None' = None, item: 'RustItem | None' = None, semicolon: 'RustSemicolon | None' = None, last: 'RustExpr | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustFnImplElement':
        if attrs is None:
            attrs = self.attrs
        if visibility is None:
            visibility = self.visibility
        if default_keyword is None:
            default_keyword = self.default_keyword
        if signature is None:
            signature = self.signature
        if open_brace is None:
            open_brace = self.open_brace
        if item is None:
            item = self.item
        if semicolon is None:
            semicolon = self.semicolon
        if last is None:
            last = self.last
        if close_brace is None:
            close_brace = self.close_brace
        return RustFnImplElement(attrs=attrs, visibility=visibility, default_keyword=default_keyword, signature=signature, open_brace=open_brace, item=item, semicolon=semicolon, last=last, close_brace=close_brace)

    def parent(self) -> 'RustFnImplElementParent':
        assert(self._parent is not None)
        return self._parent


class RustImplElement(_RustBaseNode):

    def __init__(self, fn_impl_element: 'RustFnImplElement') -> None:
        self.fn_impl_element: RustFnImplElement = _coerce_node_fn_impl_element_to_node_fn_impl_element(fn_impl_element)

    @no_type_check
    def derive(self, fn_impl_element: 'RustFnImplElement | None' = None) -> 'RustImplElement':
        if fn_impl_element is None:
            fn_impl_element = self.fn_impl_element
        return RustImplElement(fn_impl_element=fn_impl_element)

    def parent(self) -> 'RustImplElementParent':
        assert(self._parent is not None)
        return self._parent


class RustImplItem(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def count_impl_elements(self) -> int:
        return len(self.impl_elements)

    def __init__(self, type_expr: 'RustTypeExpr', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, default_keyword: 'RustDefaultKeyword | None' = None, unsafe_keyword: 'RustUnsafeKeyword | None' = None, impl_keyword: 'RustImplKeyword | None' = None, generics: 'RustGenerics | None' = None, trait: 'RustPath | tuple[RustExclamationMark | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustForKeyword | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, open_brace: 'RustOpenBrace | None' = None, impl_elements: 'Sequence[RustFnImplElement | RustImplElement] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.default_keyword: RustDefaultKeyword | None = _coerce_union_2_token_default_keyword_none_to_union_2_token_default_keyword_none(default_keyword)
        self.unsafe_keyword: RustUnsafeKeyword | None = _coerce_union_2_token_unsafe_keyword_none_to_union_2_token_unsafe_keyword_none(unsafe_keyword)
        self.impl_keyword: RustImplKeyword = _coerce_union_2_token_impl_keyword_none_to_token_impl_keyword(impl_keyword)
        self.generics: RustGenerics = _coerce_union_2_node_generics_none_to_node_generics(generics)
        self.trait: tuple[RustExclamationMark | None, RustPath, RustForKeyword] | None = _coerce_union_6_node_path_tuple_3_union_2_token_exclamation_mark_none_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_union_2_token_for_keyword_none_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_none_to_union_2_tuple_3_union_2_token_exclamation_mark_none_node_path_token_for_keyword_none(trait)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.impl_elements: Sequence[RustImplElement] = _coerce_union_2_list_union_2_node_fn_impl_element_node_impl_element_none_to_list_node_impl_element(impl_elements)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, default_keyword: 'RustDefaultKeyword | None' = None, unsafe_keyword: 'RustUnsafeKeyword | None' = None, impl_keyword: 'RustImplKeyword | None' = None, generics: 'RustGenerics | None' = None, trait: 'RustPath | tuple[RustExclamationMark | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustForKeyword | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None' = None, type_expr: 'RustTypeExpr | None' = None, open_brace: 'RustOpenBrace | None' = None, impl_elements: 'Sequence[RustFnImplElement | RustImplElement] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustImplItem':
        if attrs is None:
            attrs = self.attrs
        if default_keyword is None:
            default_keyword = self.default_keyword
        if unsafe_keyword is None:
            unsafe_keyword = self.unsafe_keyword
        if impl_keyword is None:
            impl_keyword = self.impl_keyword
        if generics is None:
            generics = self.generics
        if trait is None:
            trait = self.trait
        if type_expr is None:
            type_expr = self.type_expr
        if open_brace is None:
            open_brace = self.open_brace
        if impl_elements is None:
            impl_elements = self.impl_elements
        if close_brace is None:
            close_brace = self.close_brace
        return RustImplItem(attrs=attrs, default_keyword=default_keyword, unsafe_keyword=unsafe_keyword, impl_keyword=impl_keyword, generics=generics, trait=trait, type_expr=type_expr, open_brace=open_brace, impl_elements=impl_elements, close_brace=close_brace)

    def parent(self) -> 'RustImplItemParent':
        assert(self._parent is not None)
        return self._parent


class RustSourceFile(_RustBaseNode):

    def count_items(self) -> int:
        return len(self.items)

    def __init__(self, *, items: 'Sequence[RustToplevel] | None' = None) -> None:
        self.items: Sequence[RustToplevel] = _coerce_union_2_list_variant_toplevel_none_to_list_variant_toplevel(items)

    @no_type_check
    def derive(self, items: 'Sequence[RustToplevel] | None' = None) -> 'RustSourceFile':
        if items is None:
            items = self.items
        return RustSourceFile(items=items)

    def parent(self) -> 'RustSourceFileParent':
        raise AssertionError('trying to access the parent node of a top-level node')


type RustGenericParam = RustLifetime | RustTypeParam | RustConstParam


def is_rust_generic_param(value: Any) -> TypeGuard[RustGenericParam]:
    return isinstance(value, RustLifetime) or isinstance(value, RustTypeParam) or isinstance(value, RustConstParam)


type RustTypeParamBound = RustTraitBound | RustLifetime


def is_rust_type_param_bound(value: Any) -> TypeGuard[RustTypeParamBound]:
    return isinstance(value, RustTraitBound) or isinstance(value, RustLifetime)


type RustGenericArgument = RustLifetime | RustTypeExpr | RustExpr | RustAssocType | RustAssocConst | RustConstraint


def is_rust_generic_argument(value: Any) -> TypeGuard[RustGenericArgument]:
    return isinstance(value, RustLifetime) or is_rust_type_expr(value) or is_rust_expr(value) or isinstance(value, RustAssocType) or isinstance(value, RustAssocConst) or isinstance(value, RustConstraint)


type RustPathArguments = RustTurbofish | RustAngleBracketedGenericArguments | RustParenthesizedGenericArguments


def is_rust_path_arguments(value: Any) -> TypeGuard[RustPathArguments]:
    return isinstance(value, RustTurbofish) or isinstance(value, RustAngleBracketedGenericArguments) or isinstance(value, RustParenthesizedGenericArguments)


type RustTypeExpr = RustPathTypeExpr | RustArrayTypeExpr | RustNeverTypeExpr | RustTupleTypeExpr


def is_rust_type_expr(value: Any) -> TypeGuard[RustTypeExpr]:
    return isinstance(value, RustPathTypeExpr) or isinstance(value, RustArrayTypeExpr) or isinstance(value, RustNeverTypeExpr) or isinstance(value, RustTupleTypeExpr)


type RustExpr = RustLitExpr | RustPathExpr | RustCallExpr | RustStructExpr | RustBlockExpr | RustRetExpr


def is_rust_expr(value: Any) -> TypeGuard[RustExpr]:
    return isinstance(value, RustLitExpr) or isinstance(value, RustPathExpr) or isinstance(value, RustCallExpr) or isinstance(value, RustStructExpr) or isinstance(value, RustBlockExpr) or isinstance(value, RustRetExpr)


type RustArg = RustSelfArg | RustTypedArg | RustVariadicArg


def is_rust_arg(value: Any) -> TypeGuard[RustArg]:
    return isinstance(value, RustSelfArg) or isinstance(value, RustTypedArg) or isinstance(value, RustVariadicArg)


type RustWherePredicate = RustLifetimePredicate | RustTypePredicate


def is_rust_where_predicate(value: Any) -> TypeGuard[RustWherePredicate]:
    return isinstance(value, RustLifetimePredicate) or isinstance(value, RustTypePredicate)


type RustVariant = RustStructVariant | RustTupleVariant | RustEmptyVariant


def is_rust_variant(value: Any) -> TypeGuard[RustVariant]:
    return isinstance(value, RustStructVariant) or isinstance(value, RustTupleVariant) or isinstance(value, RustEmptyVariant)


type RustMeta = RustMetaPath | RustMetaParenthesized | RustMetaBracketed | RustMetaBraced | RustMetaNameValue


def is_rust_meta(value: Any) -> TypeGuard[RustMeta]:
    return isinstance(value, RustMetaPath) or isinstance(value, RustMetaParenthesized) or isinstance(value, RustMetaBracketed) or isinstance(value, RustMetaBraced) or isinstance(value, RustMetaNameValue)


type RustUseTree = RustUsePath | RustUseRename | RustUseName | RustUseGlob | RustUseGroup


def is_rust_use_tree(value: Any) -> TypeGuard[RustUseTree]:
    return isinstance(value, RustUsePath) or isinstance(value, RustUseRename) or isinstance(value, RustUseName) or isinstance(value, RustUseGlob) or isinstance(value, RustUseGroup)


type RustItem = RustEnumItem | RustStructItem | RustUseItem | RustExprItem


def is_rust_item(value: Any) -> TypeGuard[RustItem]:
    return isinstance(value, RustEnumItem) or isinstance(value, RustStructItem) or isinstance(value, RustUseItem) or isinstance(value, RustExprItem)


type RustToplevel = RustEnumItem | RustStructItem | RustUseItem | RustImplItem


def is_rust_toplevel(value: Any) -> TypeGuard[RustToplevel]:
    return isinstance(value, RustEnumItem) or isinstance(value, RustStructItem) or isinstance(value, RustUseItem) or isinstance(value, RustImplItem)


type RustKeyword = RustWhereKeyword | RustUseKeyword | RustUnsafeKeyword | RustTrueKeyword | RustStructKeyword | RustSelfKeyword | RustReturnKeyword | RustRefKeyword | RustPubKeyword | RustMutKeyword | RustInKeyword | RustImplKeyword | RustForKeyword | RustFnKeyword | RustFalseKeyword | RustExternKeyword | RustEnumKeyword | RustDefaultKeyword | RustConstKeyword | RustAsyncKeyword | RustAsKeyword


def is_rust_keyword(value: Any) -> TypeGuard[RustKeyword]:
    return isinstance(value, RustWhereKeyword) or isinstance(value, RustUseKeyword) or isinstance(value, RustUnsafeKeyword) or isinstance(value, RustTrueKeyword) or isinstance(value, RustStructKeyword) or isinstance(value, RustSelfKeyword) or isinstance(value, RustReturnKeyword) or isinstance(value, RustRefKeyword) or isinstance(value, RustPubKeyword) or isinstance(value, RustMutKeyword) or isinstance(value, RustInKeyword) or isinstance(value, RustImplKeyword) or isinstance(value, RustForKeyword) or isinstance(value, RustFnKeyword) or isinstance(value, RustFalseKeyword) or isinstance(value, RustExternKeyword) or isinstance(value, RustEnumKeyword) or isinstance(value, RustDefaultKeyword) or isinstance(value, RustConstKeyword) or isinstance(value, RustAsyncKeyword) or isinstance(value, RustAsKeyword)


type RustToken = RustIdent | RustInteger | RustFloat | RustString | RustChar | RustCloseBrace | RustOpenBrace | RustWhereKeyword | RustUseKeyword | RustUnsafeKeyword | RustTrueKeyword | RustStructKeyword | RustSelfKeyword | RustReturnKeyword | RustRefKeyword | RustPubKeyword | RustMutKeyword | RustInKeyword | RustImplKeyword | RustForKeyword | RustFnKeyword | RustFalseKeyword | RustExternKeyword | RustEnumKeyword | RustDefaultKeyword | RustConstKeyword | RustAsyncKeyword | RustAsKeyword | RustCloseBracket | RustOpenBracket | RustAtSign | RustQuestionMark | RustGreaterThan | RustEquals | RustLessThan | RustSemicolon | RustColonColon | RustColon | RustDotDotDot | RustRArrow | RustComma | RustPlus | RustAsterisk | RustCloseParen | RustOpenParen | RustSingleQuote | RustAmpersand | RustPercent | RustHashtag | RustExclamationMark


def is_rust_token(value: Any) -> TypeGuard[RustToken]:
    return isinstance(value, RustIdent) or isinstance(value, RustInteger) or isinstance(value, RustFloat) or isinstance(value, RustString) or isinstance(value, RustChar) or isinstance(value, RustCloseBrace) or isinstance(value, RustOpenBrace) or isinstance(value, RustWhereKeyword) or isinstance(value, RustUseKeyword) or isinstance(value, RustUnsafeKeyword) or isinstance(value, RustTrueKeyword) or isinstance(value, RustStructKeyword) or isinstance(value, RustSelfKeyword) or isinstance(value, RustReturnKeyword) or isinstance(value, RustRefKeyword) or isinstance(value, RustPubKeyword) or isinstance(value, RustMutKeyword) or isinstance(value, RustInKeyword) or isinstance(value, RustImplKeyword) or isinstance(value, RustForKeyword) or isinstance(value, RustFnKeyword) or isinstance(value, RustFalseKeyword) or isinstance(value, RustExternKeyword) or isinstance(value, RustEnumKeyword) or isinstance(value, RustDefaultKeyword) or isinstance(value, RustConstKeyword) or isinstance(value, RustAsyncKeyword) or isinstance(value, RustAsKeyword) or isinstance(value, RustCloseBracket) or isinstance(value, RustOpenBracket) or isinstance(value, RustAtSign) or isinstance(value, RustQuestionMark) or isinstance(value, RustGreaterThan) or isinstance(value, RustEquals) or isinstance(value, RustLessThan) or isinstance(value, RustSemicolon) or isinstance(value, RustColonColon) or isinstance(value, RustColon) or isinstance(value, RustDotDotDot) or isinstance(value, RustRArrow) or isinstance(value, RustComma) or isinstance(value, RustPlus) or isinstance(value, RustAsterisk) or isinstance(value, RustCloseParen) or isinstance(value, RustOpenParen) or isinstance(value, RustSingleQuote) or isinstance(value, RustAmpersand) or isinstance(value, RustPercent) or isinstance(value, RustHashtag) or isinstance(value, RustExclamationMark)


type RustNode = RustPublic | RustTypeInit | RustTypeParam | RustConstParam | RustTraitBoundModifier | RustBoundLifetimes | RustTraitBound | RustLifetime | RustAssocType | RustAssocConst | RustConstraint | RustTurbofish | RustAngleBracketedGenericArguments | RustParenthesizedGenericArguments | RustPathSegment | RustPath | RustQself | RustPathTypeExpr | RustArrayTypeExpr | RustNeverTypeExpr | RustTupleTypeExpr | RustNamedPattern | RustPattern | RustPathExpr | RustLitExpr | RustInit | RustStructExpr | RustCallExpr | RustRetExpr | RustBlockExpr | RustAbi | RustVariadicArg | RustSelfArg | RustTypedArg | RustLifetimePredicate | RustTypePredicate | RustGenerics | RustSignature | RustField | RustStructVariant | RustTupleVariant | RustEmptyVariant | RustEnumItem | RustMetaPath | RustMetaBraced | RustMetaParenthesized | RustMetaBracketed | RustMetaNameValue | RustAttr | RustStructItem | RustExprItem | RustUsePath | RustUseName | RustUseRename | RustUseGlob | RustUseGroup | RustUseItem | RustFnImplElement | RustImplElement | RustImplItem | RustSourceFile


def is_rust_node(value: Any) -> TypeGuard[RustNode]:
    return isinstance(value, RustPublic) or isinstance(value, RustTypeInit) or isinstance(value, RustTypeParam) or isinstance(value, RustConstParam) or isinstance(value, RustTraitBoundModifier) or isinstance(value, RustBoundLifetimes) or isinstance(value, RustTraitBound) or isinstance(value, RustLifetime) or isinstance(value, RustAssocType) or isinstance(value, RustAssocConst) or isinstance(value, RustConstraint) or isinstance(value, RustTurbofish) or isinstance(value, RustAngleBracketedGenericArguments) or isinstance(value, RustParenthesizedGenericArguments) or isinstance(value, RustPathSegment) or isinstance(value, RustPath) or isinstance(value, RustQself) or isinstance(value, RustPathTypeExpr) or isinstance(value, RustArrayTypeExpr) or isinstance(value, RustNeverTypeExpr) or isinstance(value, RustTupleTypeExpr) or isinstance(value, RustNamedPattern) or isinstance(value, RustPattern) or isinstance(value, RustPathExpr) or isinstance(value, RustLitExpr) or isinstance(value, RustInit) or isinstance(value, RustStructExpr) or isinstance(value, RustCallExpr) or isinstance(value, RustRetExpr) or isinstance(value, RustBlockExpr) or isinstance(value, RustAbi) or isinstance(value, RustVariadicArg) or isinstance(value, RustSelfArg) or isinstance(value, RustTypedArg) or isinstance(value, RustLifetimePredicate) or isinstance(value, RustTypePredicate) or isinstance(value, RustGenerics) or isinstance(value, RustSignature) or isinstance(value, RustField) or isinstance(value, RustStructVariant) or isinstance(value, RustTupleVariant) or isinstance(value, RustEmptyVariant) or isinstance(value, RustEnumItem) or isinstance(value, RustMetaPath) or isinstance(value, RustMetaBraced) or isinstance(value, RustMetaParenthesized) or isinstance(value, RustMetaBracketed) or isinstance(value, RustMetaNameValue) or isinstance(value, RustAttr) or isinstance(value, RustStructItem) or isinstance(value, RustExprItem) or isinstance(value, RustUsePath) or isinstance(value, RustUseName) or isinstance(value, RustUseRename) or isinstance(value, RustUseGlob) or isinstance(value, RustUseGroup) or isinstance(value, RustUseItem) or isinstance(value, RustFnImplElement) or isinstance(value, RustImplElement) or isinstance(value, RustImplItem) or isinstance(value, RustSourceFile)


type RustSyntax = RustNode | RustToken


def is_rust_syntax(value: Any) -> TypeGuard[RustSyntax]:
    return is_rust_node(value) or is_rust_token(value)


type RustPublicParent = RustEnumItem | RustFnImplElement | RustStructItem | RustUseItem


type RustTypeInitParent = RustTypeParam


type RustTypeParamParent = RustBoundLifetimes | RustGenerics


type RustConstParamParent = RustBoundLifetimes | RustGenerics


type RustTraitBoundModifierParent = RustTraitBound


type RustBoundLifetimesParent = RustTraitBound | RustTypePredicate


type RustTraitBoundParent = RustConstraint | RustTypeParam | RustTypePredicate


type RustLifetimeParent = RustAngleBracketedGenericArguments | RustBoundLifetimes | RustConstraint | RustGenerics | RustLifetimePredicate | RustSelfArg | RustTurbofish | RustTypeParam | RustTypePredicate


type RustAssocTypeParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustAssocConstParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustConstraintParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustTurbofishParent = RustPathSegment


type RustAngleBracketedGenericArgumentsParent = RustAssocConst | RustAssocType | RustConstraint | RustPathSegment


type RustParenthesizedGenericArgumentsParent = RustPathSegment


type RustPathSegmentParent = RustPath


type RustPathParent = RustImplItem | RustMetaBraced | RustMetaBracketed | RustMetaNameValue | RustMetaParenthesized | RustMetaPath | RustPathExpr | RustPathTypeExpr | RustPublic | RustQself | RustStructExpr | RustTraitBound


type RustQselfParent = RustPathExpr | RustPathTypeExpr


type RustPathTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustArrayTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustNeverTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustTupleTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustImplItem | RustParenthesizedGenericArguments | RustQself | RustSelfArg | RustSignature | RustTupleTypeExpr | RustTupleVariant | RustTurbofish | RustTypeInit | RustTypePredicate | RustTypedArg


type RustNamedPatternParent = RustPattern


type RustPatternParent = RustNamedPattern | RustTypedArg | RustVariadicArg


type RustPathExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustLitExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustInitParent = RustConstParam | RustEmptyVariant | RustStructExpr


type RustStructExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustCallExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustRetExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustBlockExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustFnImplElement | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustAbiParent = RustSignature


type RustVariadicArgParent = RustSignature


type RustSelfArgParent = RustSignature


type RustTypedArgParent = RustSignature


type RustLifetimePredicateParent = RustGenerics


type RustTypePredicateParent = RustGenerics


type RustGenericsParent = RustImplItem | RustSignature


type RustSignatureParent = RustFnImplElement


type RustFieldParent = RustStructItem | RustStructVariant


type RustStructVariantParent = RustEnumItem


type RustTupleVariantParent = RustEnumItem


type RustEmptyVariantParent = RustEnumItem


type RustEnumItemParent = RustBlockExpr | RustFnImplElement | RustSourceFile


type RustMetaPathParent = RustAttr


type RustMetaBracedParent = RustAttr


type RustMetaParenthesizedParent = RustAttr


type RustMetaBracketedParent = RustAttr


type RustMetaNameValueParent = RustAttr


type RustAttrParent = RustEnumItem | RustFnImplElement | RustImplItem | RustNamedPattern | RustPathExpr | RustSelfArg | RustStructItem | RustTypedArg | RustUseItem | RustVariadicArg


type RustStructItemParent = RustBlockExpr | RustFnImplElement | RustSourceFile


type RustExprItemParent = RustBlockExpr | RustFnImplElement


type RustUsePathParent = RustUseGroup | RustUsePath


type RustUseNameParent = RustUseGroup | RustUsePath


type RustUseRenameParent = RustUseGroup | RustUsePath


type RustUseGlobParent = RustUseGroup | RustUsePath


type RustUseGroupParent = RustUseGroup | RustUsePath


type RustUseItemParent = RustBlockExpr | RustFnImplElement | RustSourceFile


type RustFnImplElementParent = RustImplElement


type RustImplElementParent = RustImplItem


type RustImplItemParent = RustSourceFile


type RustSourceFileParent = Never


@no_type_check
def _coerce_union_2_token_pub_keyword_none_to_token_pub_keyword(value: 'RustPubKeyword | None') -> 'RustPubKeyword':
    if value is None:
        return RustPubKeyword()
    elif isinstance(value, RustPubKeyword):
        return value
    else:
        raise ValueError('the coercion from RustPubKeyword | None to RustPubKeyword failed')


@no_type_check
def _coerce_union_2_token_ident_extern_string_to_token_ident(value: 'RustIdent | str') -> 'RustIdent':
    if isinstance(value, str):
        return RustIdent(value)
    elif isinstance(value, RustIdent):
        return value
    else:
        raise ValueError('the coercion from RustIdent | str to RustIdent failed')


@no_type_check
def _coerce_union_3_node_path_segment_token_ident_extern_string_to_node_path_segment(value: 'RustPathSegment | RustIdent | str') -> 'RustPathSegment':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return RustPathSegment(_coerce_union_2_token_ident_extern_string_to_token_ident(value))
    elif isinstance(value, RustPathSegment):
        return value
    else:
        raise ValueError('the coercion from RustPathSegment | RustIdent | str to RustPathSegment failed')


@no_type_check
def _coerce_token_colon_colon_to_token_colon_colon(value: 'RustColonColon') -> 'RustColonColon':
    return value


@no_type_check
def _coerce_union_3_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_punct_node_path_segment_token_colon_colon_required(value: 'Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]') -> 'Punctuated[RustPathSegment, RustColonColon]':
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
                new_element_value = _coerce_union_3_node_path_segment_token_ident_extern_string_to_node_path_segment(element_value)
                new_element_separator = _coerce_token_colon_colon_to_token_colon_colon(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_3_node_path_segment_token_ident_extern_string_to_node_path_segment(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(value: 'RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon]') -> 'RustPath':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return RustPath(_coerce_union_3_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_punct_node_path_segment_token_colon_colon_required(value))
    elif isinstance(value, RustPath):
        return value
    else:
        raise ValueError('the coercion from RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] to RustPath failed')


@no_type_check
def _coerce_union_2_token_open_paren_none_to_token_open_paren(value: 'RustOpenParen | None') -> 'RustOpenParen':
    if value is None:
        return RustOpenParen()
    elif isinstance(value, RustOpenParen):
        return value
    else:
        raise ValueError('the coercion from RustOpenParen | None to RustOpenParen failed')


@no_type_check
def _coerce_union_2_token_in_keyword_none_to_union_2_token_in_keyword_none(value: 'RustInKeyword | None') -> 'RustInKeyword | None':
    if isinstance(value, RustInKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustInKeyword | None to RustInKeyword | None failed')


@no_type_check
def _coerce_union_2_token_close_paren_none_to_token_close_paren(value: 'RustCloseParen | None') -> 'RustCloseParen':
    if value is None:
        return RustCloseParen()
    elif isinstance(value, RustCloseParen):
        return value
    else:
        raise ValueError('the coercion from RustCloseParen | None to RustCloseParen failed')


@no_type_check
def _coerce_union_6_node_path_tuple_4_union_2_token_open_paren_none_union_2_token_in_keyword_none_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_union_2_token_close_paren_none_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_none_to_union_2_tuple_4_token_open_paren_union_2_token_in_keyword_none_node_path_token_close_paren_none(value: 'RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustCloseParen | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None') -> 'tuple[RustOpenParen, RustInKeyword | None, RustPath, RustCloseParen] | None':
    if isinstance(value, RustPath) or isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (RustOpenParen(), None, _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(value), RustCloseParen())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_open_paren_none_to_token_open_paren(value[0]), _coerce_union_2_token_in_keyword_none_to_union_2_token_in_keyword_none(value[1]), _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(value[2]), _coerce_union_2_token_close_paren_none_to_token_close_paren(value[3]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPath | tuple[RustOpenParen | None, RustInKeyword | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustCloseParen | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None to tuple[RustOpenParen, RustInKeyword | None, RustPath, RustCloseParen] | None failed')


@no_type_check
def _coerce_union_2_token_equals_none_to_token_equals(value: 'RustEquals | None') -> 'RustEquals':
    if value is None:
        return RustEquals()
    elif isinstance(value, RustEquals):
        return value
    else:
        raise ValueError('the coercion from RustEquals | None to RustEquals failed')


@no_type_check
def _coerce_variant_type_expr_to_variant_type_expr(value: 'RustTypeExpr') -> 'RustTypeExpr':
    return value


@no_type_check
def _coerce_union_2_token_colon_none_to_token_colon(value: 'RustColon | None') -> 'RustColon':
    if value is None:
        return RustColon()
    elif isinstance(value, RustColon):
        return value
    else:
        raise ValueError('the coercion from RustColon | None to RustColon failed')


@no_type_check
def _coerce_variant_type_param_bound_to_variant_type_param_bound(value: 'RustTypeParamBound') -> 'RustTypeParamBound':
    return value


@no_type_check
def _coerce_union_2_token_percent_none_to_token_percent(value: 'RustPercent | None') -> 'RustPercent':
    if value is None:
        return RustPercent()
    elif isinstance(value, RustPercent):
        return value
    else:
        raise ValueError('the coercion from RustPercent | None to RustPercent failed')


@no_type_check
def _coerce_union_2_token_plus_none_to_token_plus(value: 'RustPlus | None') -> 'RustPlus':
    if value is None:
        return RustPlus()
    elif isinstance(value, RustPlus):
        return value
    else:
        raise ValueError('the coercion from RustPlus | None to RustPlus failed')


@no_type_check
def _coerce_union_3_node_type_init_variant_type_expr_none_to_union_2_node_type_init_none(value: 'RustTypeInit | RustTypeExpr | None') -> 'RustTypeInit | None':
    if is_rust_type_expr(value):
        return RustTypeInit(_coerce_variant_type_expr_to_variant_type_expr(value))
    elif isinstance(value, RustTypeInit):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustTypeInit | RustTypeExpr | None to RustTypeInit | None failed')


@no_type_check
def _coerce_union_2_token_const_keyword_none_to_token_const_keyword(value: 'RustConstKeyword | None') -> 'RustConstKeyword':
    if value is None:
        return RustConstKeyword()
    elif isinstance(value, RustConstKeyword):
        return value
    else:
        raise ValueError('the coercion from RustConstKeyword | None to RustConstKeyword failed')


@no_type_check
def _coerce_union_2_node_init_none_to_union_2_node_init_none(value: 'RustInit | None') -> 'RustInit | None':
    if isinstance(value, RustInit):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustInit | None to RustInit | None failed')


@no_type_check
def _coerce_union_2_token_question_mark_none_to_token_question_mark(value: 'RustQuestionMark | None') -> 'RustQuestionMark':
    if value is None:
        return RustQuestionMark()
    elif isinstance(value, RustQuestionMark):
        return value
    else:
        raise ValueError('the coercion from RustQuestionMark | None to RustQuestionMark failed')


@no_type_check
def _coerce_union_2_token_for_keyword_none_to_token_for_keyword(value: 'RustForKeyword | None') -> 'RustForKeyword':
    if value is None:
        return RustForKeyword()
    elif isinstance(value, RustForKeyword):
        return value
    else:
        raise ValueError('the coercion from RustForKeyword | None to RustForKeyword failed')


@no_type_check
def _coerce_union_2_token_less_than_none_to_token_less_than(value: 'RustLessThan | None') -> 'RustLessThan':
    if value is None:
        return RustLessThan()
    elif isinstance(value, RustLessThan):
        return value
    else:
        raise ValueError('the coercion from RustLessThan | None to RustLessThan failed')


@no_type_check
def _coerce_variant_generic_param_to_variant_generic_param(value: 'RustGenericParam') -> 'RustGenericParam':
    return value


@no_type_check
def _coerce_token_comma_to_token_comma(value: 'RustComma') -> 'RustComma':
    return value


@no_type_check
def _coerce_union_4_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_to_punct_variant_generic_param_token_comma(value: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None') -> 'Punctuated[RustGenericParam, RustComma]':
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
                    new_element_value = _coerce_variant_generic_param_to_variant_generic_param(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_generic_param_to_variant_generic_param(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None to Punctuated[RustGenericParam, RustComma] failed')


@no_type_check
def _coerce_union_2_token_greater_than_none_to_token_greater_than(value: 'RustGreaterThan | None') -> 'RustGreaterThan':
    if value is None:
        return RustGreaterThan()
    elif isinstance(value, RustGreaterThan):
        return value
    else:
        raise ValueError('the coercion from RustGreaterThan | None to RustGreaterThan failed')


@no_type_check
def _coerce_union_2_node_trait_bound_modifier_none_to_union_2_node_trait_bound_modifier_none(value: 'RustTraitBoundModifier | None') -> 'RustTraitBoundModifier | None':
    if isinstance(value, RustTraitBoundModifier):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustTraitBoundModifier | None to RustTraitBoundModifier | None failed')


@no_type_check
def _coerce_union_2_node_bound_lifetimes_none_to_union_2_node_bound_lifetimes_none(value: 'RustBoundLifetimes | None') -> 'RustBoundLifetimes | None':
    if isinstance(value, RustBoundLifetimes):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustBoundLifetimes | None to RustBoundLifetimes | None failed')


@no_type_check
def _coerce_union_2_token_single_quote_none_to_token_single_quote(value: 'RustSingleQuote | None') -> 'RustSingleQuote':
    if value is None:
        return RustSingleQuote()
    elif isinstance(value, RustSingleQuote):
        return value
    else:
        raise ValueError('the coercion from RustSingleQuote | None to RustSingleQuote failed')


@no_type_check
def _coerce_union_2_node_angle_bracketed_generic_arguments_none_to_union_2_node_angle_bracketed_generic_arguments_none(value: 'RustAngleBracketedGenericArguments | None') -> 'RustAngleBracketedGenericArguments | None':
    if isinstance(value, RustAngleBracketedGenericArguments):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustAngleBracketedGenericArguments | None to RustAngleBracketedGenericArguments | None failed')


@no_type_check
def _coerce_variant_expr_to_variant_expr(value: 'RustExpr') -> 'RustExpr':
    return value


@no_type_check
def _coerce_union_2_node_angle_bracketed_generic_arguments_none_to_node_angle_bracketed_generic_arguments(value: 'RustAngleBracketedGenericArguments | None') -> 'RustAngleBracketedGenericArguments':
    if value is None:
        return RustAngleBracketedGenericArguments()
    elif value is None:
        return RustAngleBracketedGenericArguments()
    elif isinstance(value, RustAngleBracketedGenericArguments):
        return value
    else:
        raise ValueError('the coercion from RustAngleBracketedGenericArguments | None to RustAngleBracketedGenericArguments failed')


@no_type_check
def _coerce_token_plus_to_token_plus(value: 'RustPlus') -> 'RustPlus':
    return value


@no_type_check
def _coerce_union_4_list_variant_type_param_bound_list_tuple_2_variant_type_param_bound_union_2_token_plus_none_punct_variant_type_param_bound_token_plus_none_to_punct_variant_type_param_bound_token_plus(value: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus] | None') -> 'Punctuated[RustTypeParamBound, RustPlus]':
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
                    new_element_value = _coerce_variant_type_param_bound_to_variant_type_param_bound(element_value)
                    new_element_separator = _coerce_token_plus_to_token_plus(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_type_param_bound_to_variant_type_param_bound(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus] | None to Punctuated[RustTypeParamBound, RustPlus] failed')


@no_type_check
def _coerce_union_2_token_colon_colon_none_to_token_colon_colon(value: 'RustColonColon | None') -> 'RustColonColon':
    if value is None:
        return RustColonColon()
    elif isinstance(value, RustColonColon):
        return value
    else:
        raise ValueError('the coercion from RustColonColon | None to RustColonColon failed')


@no_type_check
def _coerce_variant_generic_argument_to_variant_generic_argument(value: 'RustGenericArgument') -> 'RustGenericArgument':
    return value


@no_type_check
def _coerce_union_4_list_variant_generic_argument_list_tuple_2_variant_generic_argument_union_2_token_comma_none_punct_variant_generic_argument_token_comma_none_to_punct_variant_generic_argument_token_comma(value: 'Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | Punctuated[RustGenericArgument, RustComma] | None') -> 'Punctuated[RustGenericArgument, RustComma]':
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
                    new_element_value = _coerce_variant_generic_argument_to_variant_generic_argument(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_generic_argument_to_variant_generic_argument(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustGenericArgument] | Sequence[tuple[RustGenericArgument, RustComma | None]] | Punctuated[RustGenericArgument, RustComma] | None to Punctuated[RustGenericArgument, RustComma] failed')


@no_type_check
def _coerce_union_4_list_variant_type_expr_list_tuple_2_variant_type_expr_union_2_token_comma_none_punct_variant_type_expr_token_comma_none_to_punct_variant_type_expr_token_comma(value: 'Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None') -> 'Punctuated[RustTypeExpr, RustComma]':
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
                    new_element_value = _coerce_variant_type_expr_to_variant_type_expr(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_type_expr_to_variant_type_expr(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustTypeExpr] | Sequence[tuple[RustTypeExpr, RustComma | None]] | Punctuated[RustTypeExpr, RustComma] | None to Punctuated[RustTypeExpr, RustComma] failed')


@no_type_check
def _coerce_union_2_token_r_arrow_none_to_token_r_arrow(value: 'RustRArrow | None') -> 'RustRArrow':
    if value is None:
        return RustRArrow()
    elif isinstance(value, RustRArrow):
        return value
    else:
        raise ValueError('the coercion from RustRArrow | None to RustRArrow failed')


@no_type_check
def _coerce_union_2_variant_path_arguments_none_to_union_2_variant_path_arguments_none(value: 'RustPathArguments | None') -> 'RustPathArguments | None':
    if is_rust_path_arguments(value):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPathArguments | None to RustPathArguments | None failed')


@no_type_check
def _coerce_union_2_token_colon_colon_none_to_union_2_token_colon_colon_none(value: 'RustColonColon | None') -> 'RustColonColon | None':
    if isinstance(value, RustColonColon):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustColonColon | None to RustColonColon | None failed')


@no_type_check
def _coerce_union_2_token_as_keyword_none_to_token_as_keyword(value: 'RustAsKeyword | None') -> 'RustAsKeyword':
    if value is None:
        return RustAsKeyword()
    elif isinstance(value, RustAsKeyword):
        return value
    else:
        raise ValueError('the coercion from RustAsKeyword | None to RustAsKeyword failed')


@no_type_check
def _coerce_union_2_node_qself_none_to_union_2_node_qself_none(value: 'RustQself | None') -> 'RustQself | None':
    if isinstance(value, RustQself):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustQself | None to RustQself | None failed')


@no_type_check
def _coerce_union_2_token_open_bracket_none_to_token_open_bracket(value: 'RustOpenBracket | None') -> 'RustOpenBracket':
    if value is None:
        return RustOpenBracket()
    elif isinstance(value, RustOpenBracket):
        return value
    else:
        raise ValueError('the coercion from RustOpenBracket | None to RustOpenBracket failed')


@no_type_check
def _coerce_union_2_token_semicolon_none_to_token_semicolon(value: 'RustSemicolon | None') -> 'RustSemicolon':
    if value is None:
        return RustSemicolon()
    elif isinstance(value, RustSemicolon):
        return value
    else:
        raise ValueError('the coercion from RustSemicolon | None to RustSemicolon failed')


@no_type_check
def _coerce_union_2_token_close_bracket_none_to_token_close_bracket(value: 'RustCloseBracket | None') -> 'RustCloseBracket':
    if value is None:
        return RustCloseBracket()
    elif isinstance(value, RustCloseBracket):
        return value
    else:
        raise ValueError('the coercion from RustCloseBracket | None to RustCloseBracket failed')


@no_type_check
def _coerce_union_2_token_exclamation_mark_none_to_token_exclamation_mark(value: 'RustExclamationMark | None') -> 'RustExclamationMark':
    if value is None:
        return RustExclamationMark()
    elif isinstance(value, RustExclamationMark):
        return value
    else:
        raise ValueError('the coercion from RustExclamationMark | None to RustExclamationMark failed')


@no_type_check
def _coerce_variant_meta_to_variant_meta(value: 'RustMeta') -> 'RustMeta':
    return value


@no_type_check
def _coerce_union_2_node_attr_variant_meta_to_node_attr(value: 'RustAttr | RustMeta') -> 'RustAttr':
    if is_rust_meta(value):
        return RustAttr(_coerce_variant_meta_to_variant_meta(value))
    elif isinstance(value, RustAttr):
        return value
    else:
        raise ValueError('the coercion from RustAttr | RustMeta to RustAttr failed')


@no_type_check
def _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(value: 'Sequence[RustAttr | RustMeta] | None') -> 'Sequence[RustAttr]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_2_node_attr_variant_meta_to_node_attr(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustAttr | RustMeta] | None to Sequence[RustAttr] failed')


@no_type_check
def _coerce_union_2_token_ref_keyword_none_to_union_2_token_ref_keyword_none(value: 'RustRefKeyword | None') -> 'RustRefKeyword | None':
    if isinstance(value, RustRefKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustRefKeyword | None to RustRefKeyword | None failed')


@no_type_check
def _coerce_union_2_token_mut_keyword_none_to_union_2_token_mut_keyword_none(value: 'RustMutKeyword | None') -> 'RustMutKeyword | None':
    if isinstance(value, RustMutKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustMutKeyword | None to RustMutKeyword | None failed')


@no_type_check
def _coerce_union_3_node_named_pattern_token_ident_extern_string_to_node_named_pattern(value: 'RustNamedPattern | RustIdent | str') -> 'RustNamedPattern':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return RustNamedPattern(_coerce_union_2_token_ident_extern_string_to_token_ident(value))
    elif isinstance(value, RustNamedPattern):
        return value
    else:
        raise ValueError('the coercion from RustNamedPattern | RustIdent | str to RustNamedPattern failed')


@no_type_check
def _coerce_union_4_node_named_pattern_node_pattern_token_ident_extern_string_to_node_pattern(value: 'RustNamedPattern | RustPattern | RustIdent | str') -> 'RustPattern':
    if isinstance(value, RustNamedPattern) or isinstance(value, RustIdent) or isinstance(value, str):
        return RustPattern(_coerce_union_3_node_named_pattern_token_ident_extern_string_to_node_named_pattern(value))
    elif isinstance(value, RustPattern):
        return value
    else:
        raise ValueError('the coercion from RustNamedPattern | RustPattern | RustIdent | str to RustPattern failed')


@no_type_check
def _coerce_union_2_token_at_sign_none_to_token_at_sign(value: 'RustAtSign | None') -> 'RustAtSign':
    if value is None:
        return RustAtSign()
    elif isinstance(value, RustAtSign):
        return value
    else:
        raise ValueError('the coercion from RustAtSign | None to RustAtSign failed')


@no_type_check
def _coerce_union_6_node_named_pattern_node_pattern_token_ident_tuple_2_union_2_token_at_sign_none_union_4_node_named_pattern_node_pattern_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_at_sign_node_pattern_none(value: 'RustNamedPattern | RustPattern | RustIdent | tuple[RustAtSign | None, RustNamedPattern | RustPattern | RustIdent | str] | None | str') -> 'tuple[RustAtSign, RustPattern] | None':
    if isinstance(value, RustNamedPattern) or isinstance(value, RustPattern) or isinstance(value, RustIdent) or isinstance(value, str):
        return (RustAtSign(), _coerce_union_4_node_named_pattern_node_pattern_token_ident_extern_string_to_node_pattern(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_at_sign_none_to_token_at_sign(value[0]), _coerce_union_4_node_named_pattern_node_pattern_token_ident_extern_string_to_node_pattern(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustNamedPattern | RustPattern | RustIdent | tuple[RustAtSign | None, RustNamedPattern | RustPattern | RustIdent | str] | None | str to tuple[RustAtSign, RustPattern] | None failed')


@no_type_check
def _coerce_union_7_token_char_token_false_keyword_token_float_token_string_token_true_keyword_extern_float_extern_string_to_union_5_token_char_token_false_keyword_token_float_token_string_token_true_keyword(value: 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword | float | str') -> 'RustChar | RustFalseKeyword | RustFloat | RustString | RustTrueKeyword':
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
def _coerce_union_2_token_open_brace_none_to_token_open_brace(value: 'RustOpenBrace | None') -> 'RustOpenBrace':
    if value is None:
        return RustOpenBrace()
    elif isinstance(value, RustOpenBrace):
        return value
    else:
        raise ValueError('the coercion from RustOpenBrace | None to RustOpenBrace failed')


@no_type_check
def _coerce_node_init_to_node_init(value: 'RustInit') -> 'RustInit':
    return value


@no_type_check
def _coerce_union_4_list_node_init_list_tuple_2_node_init_union_2_token_comma_none_punct_node_init_token_comma_none_to_punct_node_init_token_comma(value: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | Punctuated[RustInit, RustComma] | None') -> 'Punctuated[RustInit, RustComma]':
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
                    new_element_value = _coerce_node_init_to_node_init(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_node_init_to_node_init(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | Punctuated[RustInit, RustComma] | None to Punctuated[RustInit, RustComma] failed')


@no_type_check
def _coerce_union_2_token_comma_none_to_union_2_token_comma_none(value: 'RustComma | None') -> 'RustComma | None':
    if isinstance(value, RustComma):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustComma | None to RustComma | None failed')


@no_type_check
def _coerce_union_2_token_close_brace_none_to_token_close_brace(value: 'RustCloseBrace | None') -> 'RustCloseBrace':
    if value is None:
        return RustCloseBrace()
    elif isinstance(value, RustCloseBrace):
        return value
    else:
        raise ValueError('the coercion from RustCloseBrace | None to RustCloseBrace failed')


@no_type_check
def _coerce_union_4_list_variant_expr_list_tuple_2_variant_expr_union_2_token_comma_none_punct_variant_expr_token_comma_none_to_punct_variant_expr_token_comma(value: 'Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | Punctuated[RustExpr, RustComma] | None') -> 'Punctuated[RustExpr, RustComma]':
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
        raise ValueError('the coercion from Sequence[RustExpr] | Sequence[tuple[RustExpr, RustComma | None]] | Punctuated[RustExpr, RustComma] | None to Punctuated[RustExpr, RustComma] failed')


@no_type_check
def _coerce_union_2_token_return_keyword_none_to_token_return_keyword(value: 'RustReturnKeyword | None') -> 'RustReturnKeyword':
    if value is None:
        return RustReturnKeyword()
    elif isinstance(value, RustReturnKeyword):
        return value
    else:
        raise ValueError('the coercion from RustReturnKeyword | None to RustReturnKeyword failed')


@no_type_check
def _coerce_variant_item_to_variant_item(value: 'RustItem') -> 'RustItem':
    return value


@no_type_check
def _coerce_union_2_token_extern_keyword_none_to_token_extern_keyword(value: 'RustExternKeyword | None') -> 'RustExternKeyword':
    if value is None:
        return RustExternKeyword()
    elif isinstance(value, RustExternKeyword):
        return value
    else:
        raise ValueError('the coercion from RustExternKeyword | None to RustExternKeyword failed')


@no_type_check
def _coerce_union_2_token_string_extern_string_to_token_string(value: 'RustString | str') -> 'RustString':
    if isinstance(value, str):
        return RustString(value)
    elif isinstance(value, RustString):
        return value
    else:
        raise ValueError('the coercion from RustString | str to RustString failed')


@no_type_check
def _coerce_union_2_token_dot_dot_dot_none_to_union_2_token_dot_dot_dot_none(value: 'RustDotDotDot | None') -> 'RustDotDotDot | None':
    if isinstance(value, RustDotDotDot):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustDotDotDot | None to RustDotDotDot | None failed')


@no_type_check
def _coerce_union_3_node_lifetime_token_ident_extern_string_to_node_lifetime(value: 'RustLifetime | RustIdent | str') -> 'RustLifetime':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return RustLifetime(_coerce_union_2_token_ident_extern_string_to_token_ident(value))
    elif isinstance(value, RustLifetime):
        return value
    else:
        raise ValueError('the coercion from RustLifetime | RustIdent | str to RustLifetime failed')


@no_type_check
def _coerce_union_2_token_ampersand_none_to_token_ampersand(value: 'RustAmpersand | None') -> 'RustAmpersand':
    if value is None:
        return RustAmpersand()
    elif isinstance(value, RustAmpersand):
        return value
    else:
        raise ValueError('the coercion from RustAmpersand | None to RustAmpersand failed')


@no_type_check
def _coerce_union_5_node_lifetime_token_ident_tuple_2_union_2_token_ampersand_none_union_3_node_lifetime_token_ident_extern_string_none_extern_string_to_union_2_tuple_2_token_ampersand_node_lifetime_none(value: 'RustLifetime | RustIdent | tuple[RustAmpersand | None, RustLifetime | RustIdent | str] | None | str') -> 'tuple[RustAmpersand, RustLifetime] | None':
    if isinstance(value, RustLifetime) or isinstance(value, RustIdent) or isinstance(value, str):
        return (RustAmpersand(), _coerce_union_3_node_lifetime_token_ident_extern_string_to_node_lifetime(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_ampersand_none_to_token_ampersand(value[0]), _coerce_union_3_node_lifetime_token_ident_extern_string_to_node_lifetime(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustLifetime | RustIdent | tuple[RustAmpersand | None, RustLifetime | RustIdent | str] | None | str to tuple[RustAmpersand, RustLifetime] | None failed')


@no_type_check
def _coerce_union_2_token_self_keyword_none_to_token_self_keyword(value: 'RustSelfKeyword | None') -> 'RustSelfKeyword':
    if value is None:
        return RustSelfKeyword()
    elif isinstance(value, RustSelfKeyword):
        return value
    else:
        raise ValueError('the coercion from RustSelfKeyword | None to RustSelfKeyword failed')


@no_type_check
def _coerce_union_3_list_tuple_2_union_3_node_lifetime_token_ident_extern_string_union_2_token_plus_none_required_list_union_3_node_lifetime_token_ident_extern_string_required_punct_union_3_node_lifetime_token_ident_extern_string_token_plus_required_to_punct_node_lifetime_token_plus_required(value: 'Sequence[tuple[RustLifetime | RustIdent | str, RustPlus | None]] | Sequence[RustLifetime | RustIdent | str] | Punctuated[RustLifetime | RustIdent | str, RustPlus]') -> 'Punctuated[RustLifetime, RustPlus]':
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
                new_element_value = _coerce_union_3_node_lifetime_token_ident_extern_string_to_node_lifetime(element_value)
                new_element_separator = _coerce_token_plus_to_token_plus(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_union_3_node_lifetime_token_ident_extern_string_to_node_lifetime(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_2_node_bound_lifetimes_none_to_node_bound_lifetimes(value: 'RustBoundLifetimes | None') -> 'RustBoundLifetimes':
    if value is None:
        return RustBoundLifetimes()
    elif value is None:
        return RustBoundLifetimes()
    elif isinstance(value, RustBoundLifetimes):
        return value
    else:
        raise ValueError('the coercion from RustBoundLifetimes | None to RustBoundLifetimes failed')


@no_type_check
def _coerce_union_3_list_variant_type_param_bound_required_list_tuple_2_variant_type_param_bound_union_2_token_plus_none_required_punct_variant_type_param_bound_token_plus_required_to_punct_variant_type_param_bound_token_plus_required(value: 'Sequence[RustTypeParamBound] | Sequence[tuple[RustTypeParamBound, RustPlus | None]] | Punctuated[RustTypeParamBound, RustPlus]') -> 'Punctuated[RustTypeParamBound, RustPlus]':
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
                new_element_value = _coerce_variant_type_param_bound_to_variant_type_param_bound(element_value)
                new_element_separator = _coerce_token_plus_to_token_plus(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_variant_type_param_bound_to_variant_type_param_bound(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_3_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_to_punct_variant_generic_param_token_comma(value: 'Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma]') -> 'Punctuated[RustGenericParam, RustComma]':
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
                new_element_value = _coerce_variant_generic_param_to_variant_generic_param(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_variant_generic_param_to_variant_generic_param(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_5_tuple_3_union_2_token_less_than_none_union_4_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_union_2_token_greater_than_none_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_to_union_2_tuple_3_token_less_than_punct_variant_generic_param_token_comma_token_greater_than_none(value: 'tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None') -> 'tuple[RustLessThan, Punctuated[RustGenericParam, RustComma], RustGreaterThan] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (RustLessThan(), _coerce_union_3_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_to_punct_variant_generic_param_token_comma(value), RustGreaterThan())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_less_than_none_to_token_less_than(value[0]), _coerce_union_4_list_variant_generic_param_list_tuple_2_variant_generic_param_union_2_token_comma_none_punct_variant_generic_param_token_comma_none_to_punct_variant_generic_param_token_comma(value[1]), _coerce_union_2_token_greater_than_none_to_token_greater_than(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[RustLessThan | None, Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None, RustGreaterThan | None] | Sequence[RustGenericParam] | Sequence[tuple[RustGenericParam, RustComma | None]] | Punctuated[RustGenericParam, RustComma] | None to tuple[RustLessThan, Punctuated[RustGenericParam, RustComma], RustGreaterThan] | None failed')


@no_type_check
def _coerce_variant_where_predicate_to_variant_where_predicate(value: 'RustWherePredicate') -> 'RustWherePredicate':
    return value


@no_type_check
def _coerce_union_3_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_to_punct_variant_where_predicate_token_comma_required(value: 'Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma]') -> 'Punctuated[RustWherePredicate, RustComma]':
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
                new_element_value = _coerce_variant_where_predicate_to_variant_where_predicate(element_value)
                new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_variant_where_predicate_to_variant_where_predicate(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


@no_type_check
def _coerce_union_2_token_where_keyword_none_to_token_where_keyword(value: 'RustWhereKeyword | None') -> 'RustWhereKeyword':
    if value is None:
        return RustWhereKeyword()
    elif isinstance(value, RustWhereKeyword):
        return value
    else:
        raise ValueError('the coercion from RustWhereKeyword | None to RustWhereKeyword failed')


@no_type_check
def _coerce_union_5_tuple_2_union_2_token_where_keyword_none_union_3_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_none_to_union_2_tuple_2_token_where_keyword_punct_variant_where_predicate_token_comma_required_none(value: 'tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma] | None') -> 'tuple[RustWhereKeyword, Punctuated[RustWherePredicate, RustComma]] | None':
    if isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (RustWhereKeyword(), _coerce_union_3_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_to_punct_variant_where_predicate_token_comma_required(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_where_keyword_none_to_token_where_keyword(value[0]), _coerce_union_3_list_variant_where_predicate_required_list_tuple_2_variant_where_predicate_union_2_token_comma_none_required_punct_variant_where_predicate_token_comma_required_to_punct_variant_where_predicate_token_comma_required(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from tuple[RustWhereKeyword | None, Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma]] | Sequence[RustWherePredicate] | Sequence[tuple[RustWherePredicate, RustComma | None]] | Punctuated[RustWherePredicate, RustComma] | None to tuple[RustWhereKeyword, Punctuated[RustWherePredicate, RustComma]] | None failed')


@no_type_check
def _coerce_union_2_token_const_keyword_none_to_union_2_token_const_keyword_none(value: 'RustConstKeyword | None') -> 'RustConstKeyword | None':
    if isinstance(value, RustConstKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustConstKeyword | None to RustConstKeyword | None failed')


@no_type_check
def _coerce_union_2_token_async_keyword_none_to_union_2_token_async_keyword_none(value: 'RustAsyncKeyword | None') -> 'RustAsyncKeyword | None':
    if isinstance(value, RustAsyncKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustAsyncKeyword | None to RustAsyncKeyword | None failed')


@no_type_check
def _coerce_union_2_token_unsafe_keyword_none_to_union_2_token_unsafe_keyword_none(value: 'RustUnsafeKeyword | None') -> 'RustUnsafeKeyword | None':
    if isinstance(value, RustUnsafeKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustUnsafeKeyword | None to RustUnsafeKeyword | None failed')


@no_type_check
def _coerce_union_4_node_abi_token_string_none_extern_string_to_union_2_node_abi_none(value: 'RustAbi | RustString | None | str') -> 'RustAbi | None':
    if isinstance(value, RustString) or isinstance(value, str):
        return RustAbi(_coerce_union_2_token_string_extern_string_to_token_string(value))
    elif isinstance(value, RustAbi):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustAbi | RustString | None | str to RustAbi | None failed')


@no_type_check
def _coerce_union_2_token_fn_keyword_none_to_token_fn_keyword(value: 'RustFnKeyword | None') -> 'RustFnKeyword':
    if value is None:
        return RustFnKeyword()
    elif isinstance(value, RustFnKeyword):
        return value
    else:
        raise ValueError('the coercion from RustFnKeyword | None to RustFnKeyword failed')


@no_type_check
def _coerce_union_2_node_generics_none_to_node_generics(value: 'RustGenerics | None') -> 'RustGenerics':
    if value is None:
        return RustGenerics()
    elif isinstance(value, RustGenerics):
        return value
    else:
        raise ValueError('the coercion from RustGenerics | None to RustGenerics failed')


@no_type_check
def _coerce_variant_arg_to_variant_arg(value: 'RustArg') -> 'RustArg':
    return value


@no_type_check
def _coerce_union_4_list_variant_arg_list_tuple_2_variant_arg_union_2_token_comma_none_punct_variant_arg_token_comma_none_to_punct_variant_arg_token_comma(value: 'Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | Punctuated[RustArg, RustComma] | None') -> 'Punctuated[RustArg, RustComma]':
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
        raise ValueError('the coercion from Sequence[RustArg] | Sequence[tuple[RustArg, RustComma | None]] | Punctuated[RustArg, RustComma] | None to Punctuated[RustArg, RustComma] failed')


@no_type_check
def _coerce_union_3_variant_type_expr_tuple_2_union_2_token_r_arrow_none_variant_type_expr_none_to_union_2_tuple_2_token_r_arrow_variant_type_expr_none(value: 'RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None') -> 'tuple[RustRArrow, RustTypeExpr] | None':
    if is_rust_type_expr(value):
        return (RustRArrow(), _coerce_variant_type_expr_to_variant_type_expr(value))
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_r_arrow_none_to_token_r_arrow(value[0]), _coerce_variant_type_expr_to_variant_type_expr(value[1]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustTypeExpr | tuple[RustRArrow | None, RustTypeExpr] | None to tuple[RustRArrow, RustTypeExpr] | None failed')


@no_type_check
def _coerce_node_field_to_node_field(value: 'RustField') -> 'RustField':
    return value


@no_type_check
def _coerce_union_4_list_node_field_list_tuple_2_node_field_union_2_token_comma_none_punct_node_field_token_comma_none_to_punct_node_field_token_comma(value: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None') -> 'Punctuated[RustField, RustComma]':
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
                    new_element_value = _coerce_node_field_to_node_field(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_node_field_to_node_field(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None to Punctuated[RustField, RustComma] failed')


@no_type_check
def _coerce_union_2_node_public_none_to_union_2_node_public_none(value: 'RustPublic | None') -> 'RustPublic | None':
    if isinstance(value, RustPublic):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPublic | None to RustPublic | None failed')


@no_type_check
def _coerce_union_2_token_enum_keyword_none_to_token_enum_keyword(value: 'RustEnumKeyword | None') -> 'RustEnumKeyword':
    if value is None:
        return RustEnumKeyword()
    elif isinstance(value, RustEnumKeyword):
        return value
    else:
        raise ValueError('the coercion from RustEnumKeyword | None to RustEnumKeyword failed')


@no_type_check
def _coerce_variant_variant_to_variant_variant(value: 'RustVariant') -> 'RustVariant':
    return value


@no_type_check
def _coerce_union_4_list_variant_variant_list_tuple_2_variant_variant_union_2_token_comma_none_punct_variant_variant_token_comma_none_to_punct_variant_variant_token_comma(value: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | Punctuated[RustVariant, RustComma] | None') -> 'Punctuated[RustVariant, RustComma]':
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
                    new_element_value = _coerce_variant_variant_to_variant_variant(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_variant_to_variant_variant(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | Punctuated[RustVariant, RustComma] | None to Punctuated[RustVariant, RustComma] failed')


@no_type_check
def _coerce_variant_token_to_variant_token(value: 'RustToken') -> 'RustToken':
    return value


@no_type_check
def _coerce_union_2_list_variant_token_none_to_list_variant_token(value: 'Sequence[RustToken] | None') -> 'Sequence[RustToken]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_variant_token_to_variant_token(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustToken] | None to Sequence[RustToken] failed')


@no_type_check
def _coerce_union_2_token_hashtag_none_to_token_hashtag(value: 'RustHashtag | None') -> 'RustHashtag':
    if value is None:
        return RustHashtag()
    elif isinstance(value, RustHashtag):
        return value
    else:
        raise ValueError('the coercion from RustHashtag | None to RustHashtag failed')


@no_type_check
def _coerce_union_2_token_exclamation_mark_none_to_union_2_token_exclamation_mark_none(value: 'RustExclamationMark | None') -> 'RustExclamationMark | None':
    if isinstance(value, RustExclamationMark):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustExclamationMark | None to RustExclamationMark | None failed')


@no_type_check
def _coerce_union_2_token_struct_keyword_none_to_token_struct_keyword(value: 'RustStructKeyword | None') -> 'RustStructKeyword':
    if value is None:
        return RustStructKeyword()
    elif isinstance(value, RustStructKeyword):
        return value
    else:
        raise ValueError('the coercion from RustStructKeyword | None to RustStructKeyword failed')


@no_type_check
def _coerce_variant_use_tree_to_variant_use_tree(value: 'RustUseTree') -> 'RustUseTree':
    return value


@no_type_check
def _coerce_union_2_token_asterisk_none_to_token_asterisk(value: 'RustAsterisk | None') -> 'RustAsterisk':
    if value is None:
        return RustAsterisk()
    elif isinstance(value, RustAsterisk):
        return value
    else:
        raise ValueError('the coercion from RustAsterisk | None to RustAsterisk failed')


@no_type_check
def _coerce_union_4_list_variant_use_tree_list_tuple_2_variant_use_tree_union_2_token_comma_none_punct_variant_use_tree_token_comma_none_to_punct_variant_use_tree_token_comma(value: 'Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | Punctuated[RustUseTree, RustComma] | None') -> 'Punctuated[RustUseTree, RustComma]':
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
                    new_element_value = _coerce_variant_use_tree_to_variant_use_tree(element_value)
                    new_element_separator = _coerce_token_comma_to_token_comma(element_separator)
                    new_value.append(new_element_value, new_element_separator)
                    first_element = second_element
                except StopIteration:
                    if isinstance(first_element, tuple):
                        element_value = first_element[0]
                        assert(first_element[1] is None)
                    else:
                        element_value = first_element
                    new_element_value = _coerce_variant_use_tree_to_variant_use_tree(element_value)
                    new_value.append(new_element_value)
                    break
        except StopIteration:
            pass
        return new_value
    else:
        raise ValueError('the coercion from Sequence[RustUseTree] | Sequence[tuple[RustUseTree, RustComma | None]] | Punctuated[RustUseTree, RustComma] | None to Punctuated[RustUseTree, RustComma] failed')


@no_type_check
def _coerce_union_2_token_use_keyword_none_to_token_use_keyword(value: 'RustUseKeyword | None') -> 'RustUseKeyword':
    if value is None:
        return RustUseKeyword()
    elif isinstance(value, RustUseKeyword):
        return value
    else:
        raise ValueError('the coercion from RustUseKeyword | None to RustUseKeyword failed')


@no_type_check
def _coerce_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_colon_colon_none_extern_string_to_tuple_2_token_ident_token_colon_colon(value: 'RustIdent | tuple[RustIdent | str, RustColonColon | None] | str') -> 'tuple[RustIdent, RustColonColon]':
    if isinstance(value, RustIdent) or isinstance(value, str):
        return (_coerce_union_2_token_ident_extern_string_to_token_ident(value), RustColonColon())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_ident_extern_string_to_token_ident(value[0]), _coerce_union_2_token_colon_colon_none_to_token_colon_colon(value[1]))
    else:
        raise ValueError('the coercion from RustIdent | tuple[RustIdent | str, RustColonColon | None] | str to tuple[RustIdent, RustColonColon] failed')


@no_type_check
def _coerce_union_2_list_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_colon_colon_none_extern_string_none_to_list_tuple_2_token_ident_token_colon_colon(value: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None') -> 'Sequence[tuple[RustIdent, RustColonColon]]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_colon_colon_none_extern_string_to_tuple_2_token_ident_token_colon_colon(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None to Sequence[tuple[RustIdent, RustColonColon]] failed')


@no_type_check
def _coerce_union_2_token_default_keyword_none_to_union_2_token_default_keyword_none(value: 'RustDefaultKeyword | None') -> 'RustDefaultKeyword | None':
    if isinstance(value, RustDefaultKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustDefaultKeyword | None to RustDefaultKeyword | None failed')


@no_type_check
def _coerce_node_signature_to_node_signature(value: 'RustSignature') -> 'RustSignature':
    return value


@no_type_check
def _coerce_node_fn_impl_element_to_node_fn_impl_element(value: 'RustFnImplElement') -> 'RustFnImplElement':
    return value


@no_type_check
def _coerce_union_2_token_impl_keyword_none_to_token_impl_keyword(value: 'RustImplKeyword | None') -> 'RustImplKeyword':
    if value is None:
        return RustImplKeyword()
    elif isinstance(value, RustImplKeyword):
        return value
    else:
        raise ValueError('the coercion from RustImplKeyword | None to RustImplKeyword failed')


@no_type_check
def _coerce_union_6_node_path_tuple_3_union_2_token_exclamation_mark_none_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_union_2_token_for_keyword_none_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_none_to_union_2_tuple_3_union_2_token_exclamation_mark_none_node_path_token_for_keyword_none(value: 'RustPath | tuple[RustExclamationMark | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustForKeyword | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None') -> 'tuple[RustExclamationMark | None, RustPath, RustForKeyword] | None':
    if isinstance(value, RustPath) or isinstance(value, list) or isinstance(value, list) or isinstance(value, Punctuated):
        return (None, _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(value), RustForKeyword())
    elif isinstance(value, tuple):
        return (_coerce_union_2_token_exclamation_mark_none_to_union_2_token_exclamation_mark_none(value[0]), _coerce_union_4_node_path_list_tuple_2_union_3_node_path_segment_token_ident_extern_string_union_2_token_colon_colon_none_required_list_union_3_node_path_segment_token_ident_extern_string_required_punct_union_3_node_path_segment_token_ident_extern_string_token_colon_colon_required_to_node_path(value[1]), _coerce_union_2_token_for_keyword_none_to_token_for_keyword(value[2]))
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPath | tuple[RustExclamationMark | None, RustPath | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon], RustForKeyword | None] | Sequence[tuple[RustPathSegment | RustIdent | str, RustColonColon | None]] | Sequence[RustPathSegment | RustIdent | str] | Punctuated[RustPathSegment | RustIdent | str, RustColonColon] | None to tuple[RustExclamationMark | None, RustPath, RustForKeyword] | None failed')


@no_type_check
def _coerce_union_2_node_fn_impl_element_node_impl_element_to_node_impl_element(value: 'RustFnImplElement | RustImplElement') -> 'RustImplElement':
    if isinstance(value, RustFnImplElement):
        return RustImplElement(_coerce_node_fn_impl_element_to_node_fn_impl_element(value))
    elif isinstance(value, RustImplElement):
        return value
    else:
        raise ValueError('the coercion from RustFnImplElement | RustImplElement to RustImplElement failed')


@no_type_check
def _coerce_union_2_list_union_2_node_fn_impl_element_node_impl_element_none_to_list_node_impl_element(value: 'Sequence[RustFnImplElement | RustImplElement] | None') -> 'Sequence[RustImplElement]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_2_node_fn_impl_element_node_impl_element_to_node_impl_element(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustFnImplElement | RustImplElement] | None to Sequence[RustImplElement] failed')


@no_type_check
def _coerce_variant_toplevel_to_variant_toplevel(value: 'RustToplevel') -> 'RustToplevel':
    return value


@no_type_check
def _coerce_union_2_list_variant_toplevel_none_to_list_variant_toplevel(value: 'Sequence[RustToplevel] | None') -> 'Sequence[RustToplevel]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_variant_toplevel_to_variant_toplevel(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[RustToplevel] | None to Sequence[RustToplevel] failed')


