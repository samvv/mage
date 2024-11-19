from typing import assert_never


from .cst import *


def rust_emit_token(token):
    if isinstance(token, RustIdent):
        return str(token.value)
    if isinstance(token, RustInteger):
        return str(token.value)
    if isinstance(token, RustFloat):
        return str(token.value)
    if isinstance(token, RustString):
        return str(token.value)
    if isinstance(token, RustChar):
        return str(token.value)
    if isinstance(token, RustCloseBrace):
        return '}'
    if isinstance(token, RustOpenBrace):
        return '{'
    if isinstance(token, RustWhereKeyword):
        return 'where'
    if isinstance(token, RustUseKeyword):
        return 'use'
    if isinstance(token, RustUnsafeKeyword):
        return 'unsafe'
    if isinstance(token, RustTrueKeyword):
        return 'true'
    if isinstance(token, RustStructKeyword):
        return 'struct'
    if isinstance(token, RustSelfKeyword):
        return 'self'
    if isinstance(token, RustReturnKeyword):
        return 'return'
    if isinstance(token, RustRefKeyword):
        return 'ref'
    if isinstance(token, RustPubKeyword):
        return 'pub'
    if isinstance(token, RustMutKeyword):
        return 'mut'
    if isinstance(token, RustInKeyword):
        return 'in'
    if isinstance(token, RustImplKeyword):
        return 'impl'
    if isinstance(token, RustForKeyword):
        return 'for'
    if isinstance(token, RustFnKeyword):
        return 'fn'
    if isinstance(token, RustFalseKeyword):
        return 'false'
    if isinstance(token, RustExternKeyword):
        return 'extern'
    if isinstance(token, RustEnumKeyword):
        return 'enum'
    if isinstance(token, RustDefaultKeyword):
        return 'default'
    if isinstance(token, RustConstKeyword):
        return 'const'
    if isinstance(token, RustAsyncKeyword):
        return 'async'
    if isinstance(token, RustAsKeyword):
        return 'as'
    if isinstance(token, RustCloseBracket):
        return ']'
    if isinstance(token, RustOpenBracket):
        return '['
    if isinstance(token, RustAtSign):
        return '@'
    if isinstance(token, RustQuestionMark):
        return '?'
    if isinstance(token, RustGreaterThan):
        return '>'
    if isinstance(token, RustEquals):
        return '='
    if isinstance(token, RustLessThan):
        return '<'
    if isinstance(token, RustSemicolon):
        return ';'
    if isinstance(token, RustColonColon):
        return '::'
    if isinstance(token, RustColon):
        return ':'
    if isinstance(token, RustDotDotDot):
        return '...'
    if isinstance(token, RustRArrow):
        return '->'
    if isinstance(token, RustComma):
        return ','
    if isinstance(token, RustPlus):
        return '+'
    if isinstance(token, RustAsterisk):
        return '*'
    if isinstance(token, RustCloseParen):
        return ')'
    if isinstance(token, RustOpenParen):
        return '('
    if isinstance(token, RustSingleQuote):
        return "'"
    if isinstance(token, RustAmpersand):
        return '&'
    if isinstance(token, RustPercent):
        return '%'
    if isinstance(token, RustHashtag):
        return '#'
    if isinstance(token, RustExclamationMark):
        return '!'
    assert_never(token)


def rust_emit(node):
    out = ''
    def visit(node):
        nonlocal out
        if isinstance(node, RustPublic):
            out += rust_emit_token(node.pub_keyword)
            out += ' '
            if node.restrict is not None:
                out += rust_emit_token(node.restrict[0])
                out += ' '
                if node.restrict[1] is not None:
                    out += rust_emit_token(node.restrict[1])
                visit(node.restrict[2])
                out += rust_emit_token(node.restrict[3])
            return
        if isinstance(node, RustTypeInit):
            out += rust_emit_token(node.equals)
            visit(node.type_expr)
            return
        if isinstance(node, RustTypeParam):
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.colon)
            out += ' '
            visit(node.type_param_bound)
            out += rust_emit_token(node.percent)
            out += rust_emit_token(node.plus)
            out += ' '
            if node.default is not None:
                visit(node.default)
            return
        if isinstance(node, RustConstParam):
            out += rust_emit_token(node.const_keyword)
            out += ' '
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.colon)
            out += ' '
            visit(node.type_expr)
            if node.default is not None:
                visit(node.default)
            return
        if isinstance(node, RustTraitBoundModifier):
            out += rust_emit_token(node.question_mark)
            return
        if isinstance(node, RustBoundLifetimes):
            out += rust_emit_token(node.for_keyword)
            out += rust_emit_token(node.less_than)
            for (element, separator) in node.lifetimes:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.lifetimes.last is not None:
                visit(node.lifetimes.last)
            out += rust_emit_token(node.greater_than)
            return
        if isinstance(node, RustTraitBound):
            if node.modifier is not None:
                visit(node.modifier)
            if node.bound_lifetimes is not None:
                visit(node.bound_lifetimes)
            visit(node.path)
            return
        if isinstance(node, RustLifetime):
            out += rust_emit_token(node.single_quote)
            out += rust_emit_token(node.name)
            return
        if isinstance(node, RustAssocType):
            out += rust_emit_token(node.name)
            out += ' '
            if node.generics is not None:
                visit(node.generics)
            out += rust_emit_token(node.equals)
            visit(node.type_expr)
            return
        if isinstance(node, RustAssocConst):
            out += rust_emit_token(node.name)
            out += ' '
            if node.generics is not None:
                visit(node.generics)
            out += rust_emit_token(node.equals)
            out += ' '
            visit(node.expr)
            return
        if isinstance(node, RustConstraint):
            out += rust_emit_token(node.name)
            visit(node.generics)
            out += rust_emit_token(node.colon)
            out += ' '
            for (element, separator) in node.bounds:
                visit(element)
                out += rust_emit_token(separator)
            if node.bounds.last is not None:
                visit(node.bounds.last)
            return
        if isinstance(node, RustTurbofish):
            out += rust_emit_token(node.colon_colon)
            out += rust_emit_token(node.less_than)
            out += ' '
            for (element, separator) in node.args:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.args.last is not None:
                visit(node.args.last)
            out += rust_emit_token(node.greater_than)
            return
        if isinstance(node, RustAngleBracketedGenericArguments):
            out += rust_emit_token(node.less_than)
            out += ' '
            for (element, separator) in node.args:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.args.last is not None:
                visit(node.args.last)
            out += rust_emit_token(node.greater_than)
            return
        if isinstance(node, RustParenthesizedGenericArguments):
            out += rust_emit_token(node.open_paren)
            out += ' '
            for (element, separator) in node.params:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.params.last is not None:
                visit(node.params.last)
            out += rust_emit_token(node.close_paren)
            out += rust_emit_token(node.r_arrow)
            visit(node.result)
            return
        if isinstance(node, RustPathSegment):
            out += rust_emit_token(node.name)
            out += ' '
            if node.args is not None:
                visit(node.args)
            return
        if isinstance(node, RustPath):
            if node.leading_colon_colon is not None:
                out += rust_emit_token(node.leading_colon_colon)
                out += ' '
            for (element, separator) in node.segments:
                visit(element)
                out += rust_emit_token(separator)
            if node.segments.last is not None:
                visit(node.segments.last)
            return
        if isinstance(node, RustQself):
            out += rust_emit_token(node.less_than)
            out += ' '
            visit(node.type_expr)
            out += rust_emit_token(node.as_keyword)
            out += ' '
            visit(node.path)
            out += rust_emit_token(node.greater_than)
            return
        if isinstance(node, RustPathTypeExpr):
            if node.qself is not None:
                visit(node.qself)
            visit(node.path)
            return
        if isinstance(node, RustArrayTypeExpr):
            out += rust_emit_token(node.open_bracket)
            out += ' '
            visit(node.type_expr)
            out += rust_emit_token(node.semicolon)
            out += ' '
            visit(node.expr)
            out += rust_emit_token(node.close_bracket)
            return
        if isinstance(node, RustNeverTypeExpr):
            out += rust_emit_token(node.exclamation_mark)
            return
        if isinstance(node, RustTupleTypeExpr):
            out += rust_emit_token(node.open_paren)
            out += ' '
            for (element, separator) in node.elements:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.elements.last is not None:
                visit(node.elements.last)
            out += rust_emit_token(node.close_paren)
            return
        if isinstance(node, RustNamedPattern):
            for element in node.attrs:
                visit(element)
            if node.ref_keyword is not None:
                out += rust_emit_token(node.ref_keyword)
                out += ' '
            if node.mut_keyword is not None:
                out += rust_emit_token(node.mut_keyword)
                out += ' '
            out += rust_emit_token(node.name)
            out += ' '
            if node.sub is not None:
                out += rust_emit_token(node.sub[0])
                out += ' '
                visit(node.sub[1])
            return
        if isinstance(node, RustPattern):
            visit(node.named_pattern)
            return
        if isinstance(node, RustPathExpr):
            for element in node.attrs:
                visit(element)
            if node.qself is not None:
                visit(node.qself)
            visit(node.path)
            return
        if isinstance(node, RustLitExpr):
            if isinstance(node.literal, RustString):
                out += rust_emit_token(node.literal)
            elif isinstance(node.literal, RustChar):
                out += rust_emit_token(node.literal)
            elif isinstance(node.literal, RustFloat):
                out += rust_emit_token(node.literal)
            elif isinstance(node.literal, RustTrueKeyword) or isinstance(node.literal, RustFalseKeyword):
                if isinstance(node.literal, RustTrueKeyword):
                    out += rust_emit_token(node.literal)
                elif isinstance(node.literal, RustFalseKeyword):
                    out += rust_emit_token(node.literal)
            return
        if isinstance(node, RustInit):
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.equals)
            out += ' '
            visit(node.value)
            return
        if isinstance(node, RustStructExpr):
            visit(node.path)
            out += rust_emit_token(node.open_brace)
            out += ' '
            for (element, separator) in node.field_:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.field_.last is not None:
                visit(node.field_.last)
            if node.comma is not None:
                out += rust_emit_token(node.comma)
                out += ' '
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustCallExpr):
            visit(node.operator)
            out += rust_emit_token(node.open_paren)
            out += ' '
            for (element, separator) in node.args:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.args.last is not None:
                visit(node.args.last)
            out += rust_emit_token(node.close_paren)
            return
        if isinstance(node, RustRetExpr):
            out += rust_emit_token(node.return_keyword)
            out += ' '
            visit(node.expr)
            return
        if isinstance(node, RustBlockExpr):
            out += rust_emit_token(node.open_brace)
            out += ' '
            visit(node.item)
            out += rust_emit_token(node.semicolon)
            out += ' '
            visit(node.last)
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustAbi):
            out += rust_emit_token(node.extern_keyword)
            out += rust_emit_token(node.name)
            return
        if isinstance(node, RustVariadicArg):
            for element in node.attrs:
                visit(element)
            visit(node.pattern)
            if node.dot_dot_dot is not None:
                out += rust_emit_token(node.dot_dot_dot)
                out += ' '
            if node.comma is not None:
                out += rust_emit_token(node.comma)
            return
        if isinstance(node, RustSelfArg):
            for element in node.attrs:
                visit(element)
            if node.reference is not None:
                out += rust_emit_token(node.reference[0])
                out += ' '
                visit(node.reference[1])
            if node.mut_keyword is not None:
                out += rust_emit_token(node.mut_keyword)
                out += ' '
            out += rust_emit_token(node.self_keyword)
            out += rust_emit_token(node.colon)
            out += ' '
            visit(node.type_expr)
            return
        if isinstance(node, RustTypedArg):
            for element in node.attrs:
                visit(element)
            visit(node.pattern)
            out += rust_emit_token(node.colon)
            out += ' '
            visit(node.type_expr)
            return
        if isinstance(node, RustLifetimePredicate):
            visit(node.lifetime)
            out += rust_emit_token(node.colon)
            for (element, separator) in node.bounds:
                visit(element)
                out += rust_emit_token(separator)
            if node.bounds.last is not None:
                visit(node.bounds.last)
            return
        if isinstance(node, RustTypePredicate):
            visit(node.bound_lifetimes)
            visit(node.type_expr)
            out += rust_emit_token(node.colon)
            out += ' '
            for (element, separator) in node.bounds:
                visit(element)
                out += rust_emit_token(separator)
            if node.bounds.last is not None:
                visit(node.bounds.last)
            return
        if isinstance(node, RustGenerics):
            if node.params is not None:
                out += rust_emit_token(node.params[0])
                out += ' '
                for (element, separator) in node.params[1]:
                    visit(element)
                    out += rust_emit_token(separator)
                if node.params[1].last is not None:
                    visit(node.params[1].last)
                out += rust_emit_token(node.params[2])
            if node.where_clause is not None:
                out += rust_emit_token(node.where_clause[0])
                out += ' '
                for (element, separator) in node.where_clause[1]:
                    visit(element)
                    out += rust_emit_token(separator)
                if node.where_clause[1].last is not None:
                    visit(node.where_clause[1].last)
            return
        if isinstance(node, RustSignature):
            if node.const_keyword is not None:
                out += rust_emit_token(node.const_keyword)
                out += ' '
            if node.async_keyword is not None:
                out += rust_emit_token(node.async_keyword)
                out += ' '
            if node.unsafe_keyword is not None:
                out += rust_emit_token(node.unsafe_keyword)
                out += ' '
            if node.abi is not None:
                visit(node.abi)
            out += rust_emit_token(node.fn_keyword)
            out += ' '
            out += rust_emit_token(node.name)
            out += ' '
            visit(node.generics)
            out += rust_emit_token(node.open_paren)
            out += ' '
            for (element, separator) in node.inputs:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.inputs.last is not None:
                visit(node.inputs.last)
            out += rust_emit_token(node.close_paren)
            out += ' '
            if node.output is not None:
                out += rust_emit_token(node.output[0])
                out += ' '
                visit(node.output[1])
            return
        if isinstance(node, RustField):
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.colon)
            out += ' '
            visit(node.type_expr)
            return
        if isinstance(node, RustStructVariant):
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.open_brace)
            out += ' '
            for (element, separator) in node.fields:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.fields.last is not None:
                visit(node.fields.last)
            if node.comma is not None:
                out += rust_emit_token(node.comma)
                out += ' '
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustTupleVariant):
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.open_paren)
            out += ' '
            for (element, separator) in node.types:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.types.last is not None:
                visit(node.types.last)
            out += rust_emit_token(node.close_paren)
            return
        if isinstance(node, RustEmptyVariant):
            out += rust_emit_token(node.name)
            out += ' '
            if node.init is not None:
                visit(node.init)
            return
        if isinstance(node, RustEnumItem):
            for element in node.attrs:
                visit(element)
            if node.visibility is not None:
                visit(node.visibility)
            out += rust_emit_token(node.enum_keyword)
            out += ' '
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.open_brace)
            out += ' '
            for (element, separator) in node.variants:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.variants.last is not None:
                visit(node.variants.last)
            if node.comma is not None:
                out += rust_emit_token(node.comma)
                out += ' '
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustMetaPath):
            visit(node.path)
            return
        if isinstance(node, RustMetaBraced):
            visit(node.path)
            out += rust_emit_token(node.open_brace)
            out += ' '
            for element in node.tokens:
                out += rust_emit_token(element)
                visit(element)
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustMetaParenthesized):
            visit(node.path)
            out += rust_emit_token(node.open_paren)
            out += ' '
            for element in node.tokens:
                out += rust_emit_token(element)
                visit(element)
            out += rust_emit_token(node.close_paren)
            return
        if isinstance(node, RustMetaBracketed):
            visit(node.path)
            out += rust_emit_token(node.open_bracket)
            out += ' '
            for element in node.tokens:
                out += rust_emit_token(element)
                visit(element)
            out += rust_emit_token(node.close_bracket)
            return
        if isinstance(node, RustMetaNameValue):
            visit(node.path)
            out += rust_emit_token(node.equals)
            out += ' '
            visit(node.expr)
            return
        if isinstance(node, RustAttr):
            out += rust_emit_token(node.hashtag)
            out += ' '
            if node.exclamation_mark is not None:
                out += rust_emit_token(node.exclamation_mark)
                out += ' '
            out += rust_emit_token(node.open_bracket)
            out += ' '
            visit(node.meta)
            out += rust_emit_token(node.close_bracket)
            return
        if isinstance(node, RustStructItem):
            for element in node.attrs:
                visit(element)
            if node.visibility is not None:
                visit(node.visibility)
            out += rust_emit_token(node.struct_keyword)
            out += ' '
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.open_brace)
            out += ' '
            for (element, separator) in node.fields:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.fields.last is not None:
                visit(node.fields.last)
            if node.comma is not None:
                out += rust_emit_token(node.comma)
                out += ' '
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustExprItem):
            visit(node.expr)
            return
        if isinstance(node, RustUsePath):
            out += rust_emit_token(node.name)
            out += rust_emit_token(node.colon_colon)
            out += ' '
            visit(node.tree)
            return
        if isinstance(node, RustUseName):
            out += rust_emit_token(node.name)
            return
        if isinstance(node, RustUseRename):
            out += rust_emit_token(node.name)
            out += ' '
            out += rust_emit_token(node.as_keyword)
            out += ' '
            out += rust_emit_token(node.rename)
            return
        if isinstance(node, RustUseGlob):
            out += rust_emit_token(node.asterisk)
            return
        if isinstance(node, RustUseGroup):
            out += rust_emit_token(node.open_brace)
            out += ' '
            for (element, separator) in node.items:
                visit(element)
                out += rust_emit_token(separator)
                out += ' '
            if node.items.last is not None:
                visit(node.items.last)
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustUseItem):
            for element in node.attrs:
                visit(element)
            if node.visibility is not None:
                visit(node.visibility)
            out += rust_emit_token(node.use_keyword)
            out += ' '
            if node.colon_colon is not None:
                out += rust_emit_token(node.colon_colon)
                out += ' '
            for element in node.path:
                out += rust_emit_token(element[0])
                out += ' '
                out += rust_emit_token(element[1])
            out += rust_emit_token(node.semicolon)
            return
        if isinstance(node, RustFnImplElement):
            for element in node.attrs:
                visit(element)
            if node.visibility is not None:
                visit(node.visibility)
            if node.default_keyword is not None:
                out += rust_emit_token(node.default_keyword)
                out += ' '
            visit(node.signature)
            out += rust_emit_token(node.open_brace)
            out += ' '
            visit(node.item)
            out += rust_emit_token(node.semicolon)
            out += ' '
            visit(node.last)
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustImplElement):
            visit(node.fn_impl_element)
            return
        if isinstance(node, RustImplItem):
            for element in node.attrs:
                visit(element)
            if node.default_keyword is not None:
                out += rust_emit_token(node.default_keyword)
                out += ' '
            if node.unsafe_keyword is not None:
                out += rust_emit_token(node.unsafe_keyword)
                out += ' '
            out += rust_emit_token(node.impl_keyword)
            out += ' '
            visit(node.generics)
            if node.trait is not None:
                if node.trait[0] is not None:
                    out += rust_emit_token(node.trait[0])
                    out += ' '
                visit(node.trait[1])
                out += rust_emit_token(node.trait[2])
            visit(node.type_expr)
            out += rust_emit_token(node.open_brace)
            out += ' '
            for element in node.impl_elements:
                visit(element)
            out += rust_emit_token(node.close_brace)
            return
        if isinstance(node, RustSourceFile):
            for element in node.items:
                visit(element)
            return
    visit(node)
    return out


