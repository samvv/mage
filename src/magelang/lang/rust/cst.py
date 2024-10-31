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


class RustUseKeyword(_RustBaseToken):

    pass


class RustTrueKeyword(_RustBaseToken):

    pass


class RustStructKeyword(_RustBaseToken):

    pass


class RustReturnKeyword(_RustBaseToken):

    pass


class RustPubKeyword(_RustBaseToken):

    pass


class RustForKeyword(_RustBaseToken):

    pass


class RustFalseKeyword(_RustBaseToken):

    pass


class RustEnumKeyword(_RustBaseToken):

    pass


class RustConstKeyword(_RustBaseToken):

    pass


class RustAsKeyword(_RustBaseToken):

    pass


class RustCloseBracket(_RustBaseToken):

    pass


class RustOpenBracket(_RustBaseToken):

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


class RustPercent(_RustBaseToken):

    pass


class RustHashtag(_RustBaseToken):

    pass


class RustExclamationMark(_RustBaseToken):

    pass


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

    def __init__(self, path: 'RustPath', *, modifier: 'RustTraitBoundModifier | None' = None, bound_lifetimes: 'RustBoundLifetimes | None' = None) -> None:
        self.modifier: RustTraitBoundModifier | None = _coerce_union_2_node_trait_bound_modifier_none_to_union_2_node_trait_bound_modifier_none(modifier)
        self.bound_lifetimes: RustBoundLifetimes | None = _coerce_union_2_node_bound_lifetimes_none_to_union_2_node_bound_lifetimes_none(bound_lifetimes)
        self.path: RustPath = _coerce_node_path_to_node_path(path)

    @no_type_check
    def derive(self, modifier: 'RustTraitBoundModifier | None' = None, bound_lifetimes: 'RustBoundLifetimes | None' = None, path: 'RustPath | None' = None) -> 'RustTraitBound':
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

    def __init__(self, segments: 'Sequence[RustPathSegment] | Sequence[tuple[RustPathSegment, RustColonColon | None]] | Punctuated[RustPathSegment, RustColonColon]', *, leading_colon_colon: 'RustColonColon | None' = None) -> None:
        self.leading_colon_colon: RustColonColon | None = _coerce_union_2_token_colon_colon_none_to_union_2_token_colon_colon_none(leading_colon_colon)
        self.segments: Punctuated[RustPathSegment, RustColonColon] = _coerce_union_3_list_node_path_segment_required_list_tuple_2_node_path_segment_union_2_token_colon_colon_none_required_punct_node_path_segment_token_colon_colon_required_to_punct_node_path_segment_token_colon_colon_required(segments)

    @no_type_check
    def derive(self, leading_colon_colon: 'RustColonColon | None' = None, segments: 'Sequence[RustPathSegment] | Sequence[tuple[RustPathSegment, RustColonColon | None]] | Punctuated[RustPathSegment, RustColonColon] | None' = None) -> 'RustPath':
        if leading_colon_colon is None:
            leading_colon_colon = self.leading_colon_colon
        if segments is None:
            segments = self.segments
        return RustPath(leading_colon_colon=leading_colon_colon, segments=segments)

    def parent(self) -> 'RustPathParent':
        assert(self._parent is not None)
        return self._parent


class RustQself(_RustBaseNode):

    def __init__(self, type_expr: 'RustTypeExpr', path: 'RustPath', *, less_than: 'RustLessThan | None' = None, as_keyword: 'RustAsKeyword | None' = None, greater_than: 'RustGreaterThan | None' = None) -> None:
        self.less_than: RustLessThan = _coerce_union_2_token_less_than_none_to_token_less_than(less_than)
        self.type_expr: RustTypeExpr = _coerce_variant_type_expr_to_variant_type_expr(type_expr)
        self.as_keyword: RustAsKeyword = _coerce_union_2_token_as_keyword_none_to_token_as_keyword(as_keyword)
        self.path: RustPath = _coerce_node_path_to_node_path(path)
        self.greater_than: RustGreaterThan = _coerce_union_2_token_greater_than_none_to_token_greater_than(greater_than)

    @no_type_check
    def derive(self, less_than: 'RustLessThan | None' = None, type_expr: 'RustTypeExpr | None' = None, as_keyword: 'RustAsKeyword | None' = None, path: 'RustPath | None' = None, greater_than: 'RustGreaterThan | None' = None) -> 'RustQself':
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

    def __init__(self, path: 'RustPath', *, qself: 'RustQself | None' = None) -> None:
        self.qself: RustQself | None = _coerce_union_2_node_qself_none_to_union_2_node_qself_none(qself)
        self.path: RustPath = _coerce_node_path_to_node_path(path)

    @no_type_check
    def derive(self, qself: 'RustQself | None' = None, path: 'RustPath | None' = None) -> 'RustPathTypeExpr':
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


class RustPathExpr(_RustBaseNode):

    def count_attrs(self) -> int:
        return len(self.attrs)

    def __init__(self, path: 'RustPath', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, qself: 'RustQself | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.qself: RustQself | None = _coerce_union_2_node_qself_none_to_union_2_node_qself_none(qself)
        self.path: RustPath = _coerce_node_path_to_node_path(path)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, qself: 'RustQself | None' = None, path: 'RustPath | None' = None) -> 'RustPathExpr':
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

    def __init__(self, path: 'RustPath', *, open_brace: 'RustOpenBrace | None' = None, field_: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | Punctuated[RustInit, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.path: RustPath = _coerce_node_path_to_node_path(path)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.field_: Punctuated[RustInit, RustComma] = _coerce_union_4_list_node_init_list_tuple_2_node_init_union_2_token_comma_none_punct_node_init_token_comma_none_to_punct_node_init_token_comma(field_)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, path: 'RustPath | None' = None, open_brace: 'RustOpenBrace | None' = None, field_: 'Sequence[RustInit] | Sequence[tuple[RustInit, RustComma | None]] | Punctuated[RustInit, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustStructExpr':
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

    def count_variants(self) -> int:
        return len(self.variants)

    def __init__(self, name: 'RustIdent | str', *, pub_keyword: 'RustPubKeyword | None' = None, enum_keyword: 'RustEnumKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, variants: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | Punctuated[RustVariant, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.pub_keyword: RustPubKeyword | None = _coerce_union_2_token_pub_keyword_none_to_union_2_token_pub_keyword_none(pub_keyword)
        self.enum_keyword: RustEnumKeyword = _coerce_union_2_token_enum_keyword_none_to_token_enum_keyword(enum_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.variants: Punctuated[RustVariant, RustComma] = _coerce_union_4_list_variant_variant_list_tuple_2_variant_variant_union_2_token_comma_none_punct_variant_variant_token_comma_none_to_punct_variant_variant_token_comma(variants)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, pub_keyword: 'RustPubKeyword | None' = None, enum_keyword: 'RustEnumKeyword | None' = None, name: 'RustIdent | None | str' = None, open_brace: 'RustOpenBrace | None' = None, variants: 'Sequence[RustVariant] | Sequence[tuple[RustVariant, RustComma | None]] | Punctuated[RustVariant, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustEnumItem':
        if pub_keyword is None:
            pub_keyword = self.pub_keyword
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
        return RustEnumItem(pub_keyword=pub_keyword, enum_keyword=enum_keyword, name=name, open_brace=open_brace, variants=variants, comma=comma, close_brace=close_brace)

    def parent(self) -> 'RustEnumItemParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaPath(_RustBaseNode):

    def __init__(self, path: 'RustPath') -> None:
        self.path: RustPath = _coerce_node_path_to_node_path(path)

    @no_type_check
    def derive(self, path: 'RustPath | None' = None) -> 'RustMetaPath':
        if path is None:
            path = self.path
        return RustMetaPath(path=path)

    def parent(self) -> 'RustMetaPathParent':
        assert(self._parent is not None)
        return self._parent


class RustMetaBraced(_RustBaseNode):

    def count_tokens(self) -> int:
        return len(self.tokens)

    def __init__(self, path: 'RustPath', *, open_brace: 'RustOpenBrace | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.path: RustPath = _coerce_node_path_to_node_path(path)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.tokens: Sequence[RustToken] = _coerce_union_2_list_variant_token_none_to_list_variant_token(tokens)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, path: 'RustPath | None' = None, open_brace: 'RustOpenBrace | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustMetaBraced':
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

    def __init__(self, path: 'RustPath', *, open_paren: 'RustOpenParen | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_paren: 'RustCloseParen | None' = None) -> None:
        self.path: RustPath = _coerce_node_path_to_node_path(path)
        self.open_paren: RustOpenParen = _coerce_union_2_token_open_paren_none_to_token_open_paren(open_paren)
        self.tokens: Sequence[RustToken] = _coerce_union_2_list_variant_token_none_to_list_variant_token(tokens)
        self.close_paren: RustCloseParen = _coerce_union_2_token_close_paren_none_to_token_close_paren(close_paren)

    @no_type_check
    def derive(self, path: 'RustPath | None' = None, open_paren: 'RustOpenParen | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_paren: 'RustCloseParen | None' = None) -> 'RustMetaParenthesized':
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

    def __init__(self, path: 'RustPath', *, open_bracket: 'RustOpenBracket | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> None:
        self.path: RustPath = _coerce_node_path_to_node_path(path)
        self.open_bracket: RustOpenBracket = _coerce_union_2_token_open_bracket_none_to_token_open_bracket(open_bracket)
        self.tokens: Sequence[RustToken] = _coerce_union_2_list_variant_token_none_to_list_variant_token(tokens)
        self.close_bracket: RustCloseBracket = _coerce_union_2_token_close_bracket_none_to_token_close_bracket(close_bracket)

    @no_type_check
    def derive(self, path: 'RustPath | None' = None, open_bracket: 'RustOpenBracket | None' = None, tokens: 'Sequence[RustToken] | None' = None, close_bracket: 'RustCloseBracket | None' = None) -> 'RustMetaBracketed':
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

    def __init__(self, path: 'RustPath', expr: 'RustExpr', *, equals: 'RustEquals | None' = None) -> None:
        self.path: RustPath = _coerce_node_path_to_node_path(path)
        self.equals: RustEquals = _coerce_union_2_token_equals_none_to_token_equals(equals)
        self.expr: RustExpr = _coerce_variant_expr_to_variant_expr(expr)

    @no_type_check
    def derive(self, path: 'RustPath | None' = None, equals: 'RustEquals | None' = None, expr: 'RustExpr | None' = None) -> 'RustMetaNameValue':
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
        self.exclamation_mark: RustExclamationMark = _coerce_union_2_token_exclamation_mark_none_to_token_exclamation_mark(exclamation_mark)
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

    def __init__(self, name: 'RustIdent | str', *, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, pub_keyword: 'RustPubKeyword | None' = None, struct_keyword: 'RustStructKeyword | None' = None, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> None:
        self.attrs: Sequence[RustAttr] = _coerce_union_2_list_union_2_node_attr_variant_meta_none_to_list_node_attr(attrs)
        self.pub_keyword: RustPubKeyword | None = _coerce_union_2_token_pub_keyword_none_to_union_2_token_pub_keyword_none(pub_keyword)
        self.struct_keyword: RustStructKeyword = _coerce_union_2_token_struct_keyword_none_to_token_struct_keyword(struct_keyword)
        self.name: RustIdent = _coerce_union_2_token_ident_extern_string_to_token_ident(name)
        self.open_brace: RustOpenBrace = _coerce_union_2_token_open_brace_none_to_token_open_brace(open_brace)
        self.fields: Punctuated[RustField, RustComma] = _coerce_union_4_list_node_field_list_tuple_2_node_field_union_2_token_comma_none_punct_node_field_token_comma_none_to_punct_node_field_token_comma(fields)
        self.comma: RustComma | None = _coerce_union_2_token_comma_none_to_union_2_token_comma_none(comma)
        self.close_brace: RustCloseBrace = _coerce_union_2_token_close_brace_none_to_token_close_brace(close_brace)

    @no_type_check
    def derive(self, attrs: 'Sequence[RustAttr | RustMeta] | None' = None, pub_keyword: 'RustPubKeyword | None' = None, struct_keyword: 'RustStructKeyword | None' = None, name: 'RustIdent | None | str' = None, open_brace: 'RustOpenBrace | None' = None, fields: 'Sequence[RustField] | Sequence[tuple[RustField, RustComma | None]] | Punctuated[RustField, RustComma] | None' = None, comma: 'RustComma | None' = None, close_brace: 'RustCloseBrace | None' = None) -> 'RustStructItem':
        if attrs is None:
            attrs = self.attrs
        if pub_keyword is None:
            pub_keyword = self.pub_keyword
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
        return RustStructItem(attrs=attrs, pub_keyword=pub_keyword, struct_keyword=struct_keyword, name=name, open_brace=open_brace, fields=fields, comma=comma, close_brace=close_brace)

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

    def count_path(self) -> int:
        return len(self.path)

    def __init__(self, *, use_keyword: 'RustUseKeyword | None' = None, colon_colon: 'RustColonColon | None' = None, path: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None' = None, semicolon: 'RustSemicolon | None' = None) -> None:
        self.use_keyword: RustUseKeyword = _coerce_union_2_token_use_keyword_none_to_token_use_keyword(use_keyword)
        self.colon_colon: RustColonColon | None = _coerce_union_2_token_colon_colon_none_to_union_2_token_colon_colon_none(colon_colon)
        self.path: Sequence[tuple[RustIdent, RustColonColon]] = _coerce_union_2_list_union_3_token_ident_tuple_2_union_2_token_ident_extern_string_union_2_token_colon_colon_none_extern_string_none_to_list_tuple_2_token_ident_token_colon_colon(path)
        self.semicolon: RustSemicolon = _coerce_union_2_token_semicolon_none_to_token_semicolon(semicolon)

    @no_type_check
    def derive(self, use_keyword: 'RustUseKeyword | None' = None, colon_colon: 'RustColonColon | None' = None, path: 'Sequence[RustIdent | tuple[RustIdent | str, RustColonColon | None] | str] | None' = None, semicolon: 'RustSemicolon | None' = None) -> 'RustUseItem':
        if use_keyword is None:
            use_keyword = self.use_keyword
        if colon_colon is None:
            colon_colon = self.colon_colon
        if path is None:
            path = self.path
        if semicolon is None:
            semicolon = self.semicolon
        return RustUseItem(use_keyword=use_keyword, colon_colon=colon_colon, path=path, semicolon=semicolon)

    def parent(self) -> 'RustUseItemParent':
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


type RustTypeExpr = RustPathTypeExpr | RustArrayTypeExpr


def is_rust_type_expr(value: Any) -> TypeGuard[RustTypeExpr]:
    return isinstance(value, RustPathTypeExpr) or isinstance(value, RustArrayTypeExpr)


type RustExpr = RustLitExpr | RustPathExpr | RustCallExpr | RustStructExpr | RustBlockExpr | RustRetExpr


def is_rust_expr(value: Any) -> TypeGuard[RustExpr]:
    return isinstance(value, RustLitExpr) or isinstance(value, RustPathExpr) or isinstance(value, RustCallExpr) or isinstance(value, RustStructExpr) or isinstance(value, RustBlockExpr) or isinstance(value, RustRetExpr)


type RustVariant = RustStructVariant | RustTupleVariant | RustEmptyVariant


def is_rust_variant(value: Any) -> TypeGuard[RustVariant]:
    return isinstance(value, RustStructVariant) or isinstance(value, RustTupleVariant) or isinstance(value, RustEmptyVariant)


type RustMeta = RustMetaPath | RustMetaParenthesized | RustMetaBracketed | RustMetaBraced | RustMetaNameValue


def is_rust_meta(value: Any) -> TypeGuard[RustMeta]:
    return isinstance(value, RustMetaPath) or isinstance(value, RustMetaParenthesized) or isinstance(value, RustMetaBracketed) or isinstance(value, RustMetaBraced) or isinstance(value, RustMetaNameValue)


type RustUseTree = RustUsePath | RustUseName | RustUseRename | RustUseGlob | RustUseGroup


def is_rust_use_tree(value: Any) -> TypeGuard[RustUseTree]:
    return isinstance(value, RustUsePath) or isinstance(value, RustUseName) or isinstance(value, RustUseRename) or isinstance(value, RustUseGlob) or isinstance(value, RustUseGroup)


type RustItem = RustEnumItem | RustStructItem | RustUseItem | RustExprItem


def is_rust_item(value: Any) -> TypeGuard[RustItem]:
    return isinstance(value, RustEnumItem) or isinstance(value, RustStructItem) or isinstance(value, RustUseItem) or isinstance(value, RustExprItem)


type RustToplevel = RustEnumItem | RustStructItem | RustUseItem


def is_rust_toplevel(value: Any) -> TypeGuard[RustToplevel]:
    return isinstance(value, RustEnumItem) or isinstance(value, RustStructItem) or isinstance(value, RustUseItem)


type RustKeyword = RustUseKeyword | RustTrueKeyword | RustStructKeyword | RustReturnKeyword | RustPubKeyword | RustForKeyword | RustFalseKeyword | RustEnumKeyword | RustConstKeyword | RustAsKeyword


def is_rust_keyword(value: Any) -> TypeGuard[RustKeyword]:
    return isinstance(value, RustUseKeyword) or isinstance(value, RustTrueKeyword) or isinstance(value, RustStructKeyword) or isinstance(value, RustReturnKeyword) or isinstance(value, RustPubKeyword) or isinstance(value, RustForKeyword) or isinstance(value, RustFalseKeyword) or isinstance(value, RustEnumKeyword) or isinstance(value, RustConstKeyword) or isinstance(value, RustAsKeyword)


type RustToken = RustIdent | RustInteger | RustFloat | RustString | RustChar | RustCloseBrace | RustOpenBrace | RustUseKeyword | RustTrueKeyword | RustStructKeyword | RustReturnKeyword | RustPubKeyword | RustForKeyword | RustFalseKeyword | RustEnumKeyword | RustConstKeyword | RustAsKeyword | RustCloseBracket | RustOpenBracket | RustQuestionMark | RustGreaterThan | RustEquals | RustLessThan | RustSemicolon | RustColonColon | RustColon | RustRArrow | RustComma | RustPlus | RustAsterisk | RustCloseParen | RustOpenParen | RustSingleQuote | RustPercent | RustHashtag | RustExclamationMark


def is_rust_token(value: Any) -> TypeGuard[RustToken]:
    return isinstance(value, RustIdent) or isinstance(value, RustInteger) or isinstance(value, RustFloat) or isinstance(value, RustString) or isinstance(value, RustChar) or isinstance(value, RustCloseBrace) or isinstance(value, RustOpenBrace) or isinstance(value, RustUseKeyword) or isinstance(value, RustTrueKeyword) or isinstance(value, RustStructKeyword) or isinstance(value, RustReturnKeyword) or isinstance(value, RustPubKeyword) or isinstance(value, RustForKeyword) or isinstance(value, RustFalseKeyword) or isinstance(value, RustEnumKeyword) or isinstance(value, RustConstKeyword) or isinstance(value, RustAsKeyword) or isinstance(value, RustCloseBracket) or isinstance(value, RustOpenBracket) or isinstance(value, RustQuestionMark) or isinstance(value, RustGreaterThan) or isinstance(value, RustEquals) or isinstance(value, RustLessThan) or isinstance(value, RustSemicolon) or isinstance(value, RustColonColon) or isinstance(value, RustColon) or isinstance(value, RustRArrow) or isinstance(value, RustComma) or isinstance(value, RustPlus) or isinstance(value, RustAsterisk) or isinstance(value, RustCloseParen) or isinstance(value, RustOpenParen) or isinstance(value, RustSingleQuote) or isinstance(value, RustPercent) or isinstance(value, RustHashtag) or isinstance(value, RustExclamationMark)


type RustNode = RustTypeInit | RustTypeParam | RustConstParam | RustTraitBoundModifier | RustBoundLifetimes | RustTraitBound | RustLifetime | RustAssocType | RustAssocConst | RustConstraint | RustTurbofish | RustAngleBracketedGenericArguments | RustParenthesizedGenericArguments | RustPathSegment | RustPath | RustQself | RustPathTypeExpr | RustArrayTypeExpr | RustPathExpr | RustLitExpr | RustInit | RustStructExpr | RustCallExpr | RustRetExpr | RustBlockExpr | RustField | RustStructVariant | RustTupleVariant | RustEmptyVariant | RustEnumItem | RustMetaPath | RustMetaBraced | RustMetaParenthesized | RustMetaBracketed | RustMetaNameValue | RustAttr | RustStructItem | RustExprItem | RustUsePath | RustUseName | RustUseRename | RustUseGlob | RustUseGroup | RustUseItem | RustSourceFile


def is_rust_node(value: Any) -> TypeGuard[RustNode]:
    return isinstance(value, RustTypeInit) or isinstance(value, RustTypeParam) or isinstance(value, RustConstParam) or isinstance(value, RustTraitBoundModifier) or isinstance(value, RustBoundLifetimes) or isinstance(value, RustTraitBound) or isinstance(value, RustLifetime) or isinstance(value, RustAssocType) or isinstance(value, RustAssocConst) or isinstance(value, RustConstraint) or isinstance(value, RustTurbofish) or isinstance(value, RustAngleBracketedGenericArguments) or isinstance(value, RustParenthesizedGenericArguments) or isinstance(value, RustPathSegment) or isinstance(value, RustPath) or isinstance(value, RustQself) or isinstance(value, RustPathTypeExpr) or isinstance(value, RustArrayTypeExpr) or isinstance(value, RustPathExpr) or isinstance(value, RustLitExpr) or isinstance(value, RustInit) or isinstance(value, RustStructExpr) or isinstance(value, RustCallExpr) or isinstance(value, RustRetExpr) or isinstance(value, RustBlockExpr) or isinstance(value, RustField) or isinstance(value, RustStructVariant) or isinstance(value, RustTupleVariant) or isinstance(value, RustEmptyVariant) or isinstance(value, RustEnumItem) or isinstance(value, RustMetaPath) or isinstance(value, RustMetaBraced) or isinstance(value, RustMetaParenthesized) or isinstance(value, RustMetaBracketed) or isinstance(value, RustMetaNameValue) or isinstance(value, RustAttr) or isinstance(value, RustStructItem) or isinstance(value, RustExprItem) or isinstance(value, RustUsePath) or isinstance(value, RustUseName) or isinstance(value, RustUseRename) or isinstance(value, RustUseGlob) or isinstance(value, RustUseGroup) or isinstance(value, RustUseItem) or isinstance(value, RustSourceFile)


type RustSyntax = RustNode | RustToken


def is_rust_syntax(value: Any) -> TypeGuard[RustSyntax]:
    return is_rust_node(value) or is_rust_token(value)


type RustTypeInitParent = RustTypeParam


type RustTypeParamParent = RustBoundLifetimes


type RustConstParamParent = RustBoundLifetimes


type RustTraitBoundModifierParent = RustTraitBound


type RustBoundLifetimesParent = RustTraitBound


type RustTraitBoundParent = RustConstraint | RustTypeParam


type RustLifetimeParent = RustAngleBracketedGenericArguments | RustBoundLifetimes | RustConstraint | RustTurbofish | RustTypeParam


type RustAssocTypeParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustAssocConstParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustConstraintParent = RustAngleBracketedGenericArguments | RustTurbofish


type RustTurbofishParent = RustPathSegment


type RustAngleBracketedGenericArgumentsParent = RustAssocConst | RustAssocType | RustConstraint | RustPathSegment


type RustParenthesizedGenericArgumentsParent = RustPathSegment


type RustPathSegmentParent = RustPath


type RustPathParent = RustMetaBraced | RustMetaBracketed | RustMetaNameValue | RustMetaParenthesized | RustMetaPath | RustPathExpr | RustPathTypeExpr | RustQself | RustStructExpr | RustTraitBound


type RustQselfParent = RustPathExpr | RustPathTypeExpr


type RustPathTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustParenthesizedGenericArguments | RustQself | RustTupleVariant | RustTurbofish | RustTypeInit


type RustArrayTypeExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocType | RustConstParam | RustField | RustParenthesizedGenericArguments | RustQself | RustTupleVariant | RustTurbofish | RustTypeInit


type RustPathExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustLitExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustInitParent = RustConstParam | RustEmptyVariant | RustStructExpr


type RustStructExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustCallExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustRetExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustBlockExprParent = RustAngleBracketedGenericArguments | RustArrayTypeExpr | RustAssocConst | RustBlockExpr | RustCallExpr | RustExprItem | RustInit | RustMetaNameValue | RustRetExpr | RustTurbofish


type RustFieldParent = RustStructItem | RustStructVariant


type RustStructVariantParent = RustEnumItem


type RustTupleVariantParent = RustEnumItem


type RustEmptyVariantParent = RustEnumItem


type RustEnumItemParent = RustBlockExpr | RustSourceFile


type RustMetaPathParent = RustAttr


type RustMetaBracedParent = RustAttr


type RustMetaParenthesizedParent = RustAttr


type RustMetaBracketedParent = RustAttr


type RustMetaNameValueParent = RustAttr


type RustAttrParent = RustPathExpr | RustStructItem


type RustStructItemParent = RustBlockExpr | RustSourceFile


type RustExprItemParent = RustBlockExpr


type RustUsePathParent = RustUseGroup | RustUsePath


type RustUseNameParent = RustUseGroup | RustUsePath


type RustUseRenameParent = RustUseGroup | RustUsePath


type RustUseGlobParent = RustUseGroup | RustUsePath


type RustUseGroupParent = RustUseGroup | RustUsePath


type RustUseItemParent = RustBlockExpr | RustSourceFile


type RustSourceFileParent = Never


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
def _coerce_union_2_token_ident_extern_string_to_token_ident(value: 'RustIdent | str') -> 'RustIdent':
    if isinstance(value, str):
        return RustIdent(value)
    elif isinstance(value, RustIdent):
        return value
    else:
        raise ValueError('the coercion from RustIdent | str to RustIdent failed')


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
def _coerce_node_path_to_node_path(value: 'RustPath') -> 'RustPath':
    return value


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
def _coerce_union_2_token_open_paren_none_to_token_open_paren(value: 'RustOpenParen | None') -> 'RustOpenParen':
    if value is None:
        return RustOpenParen()
    elif isinstance(value, RustOpenParen):
        return value
    else:
        raise ValueError('the coercion from RustOpenParen | None to RustOpenParen failed')


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
def _coerce_union_2_token_close_paren_none_to_token_close_paren(value: 'RustCloseParen | None') -> 'RustCloseParen':
    if value is None:
        return RustCloseParen()
    elif isinstance(value, RustCloseParen):
        return value
    else:
        raise ValueError('the coercion from RustCloseParen | None to RustCloseParen failed')


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
def _coerce_node_path_segment_to_node_path_segment(value: 'RustPathSegment') -> 'RustPathSegment':
    return value


@no_type_check
def _coerce_token_colon_colon_to_token_colon_colon(value: 'RustColonColon') -> 'RustColonColon':
    return value


@no_type_check
def _coerce_union_3_list_node_path_segment_required_list_tuple_2_node_path_segment_union_2_token_colon_colon_none_required_punct_node_path_segment_token_colon_colon_required_to_punct_node_path_segment_token_colon_colon_required(value: 'Sequence[RustPathSegment] | Sequence[tuple[RustPathSegment, RustColonColon | None]] | Punctuated[RustPathSegment, RustColonColon]') -> 'Punctuated[RustPathSegment, RustColonColon]':
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
                new_element_value = _coerce_node_path_segment_to_node_path_segment(element_value)
                new_element_separator = _coerce_token_colon_colon_to_token_colon_colon(element_separator)
                new_value.append(new_element_value, new_element_separator)
                first_element = second_element
            except StopIteration:
                if isinstance(first_element, tuple):
                    element_value = first_element[0]
                    assert(first_element[1] is None)
                else:
                    element_value = first_element
                new_element_value = _coerce_node_path_segment_to_node_path_segment(element_value)
                new_value.append(new_element_value)
                break
    except StopIteration:
        pass
    return new_value


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
def _coerce_union_2_token_pub_keyword_none_to_union_2_token_pub_keyword_none(value: 'RustPubKeyword | None') -> 'RustPubKeyword | None':
    if isinstance(value, RustPubKeyword):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from RustPubKeyword | None to RustPubKeyword | None failed')


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
def _coerce_union_2_token_exclamation_mark_none_to_token_exclamation_mark(value: 'RustExclamationMark | None') -> 'RustExclamationMark':
    if value is None:
        return RustExclamationMark()
    elif isinstance(value, RustExclamationMark):
        return value
    else:
        raise ValueError('the coercion from RustExclamationMark | None to RustExclamationMark failed')


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


