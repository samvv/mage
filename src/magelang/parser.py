
from collections import deque
from typing import cast

from .ast import *
from .scanner import *

class ParseError(RuntimeError):

    def __init__(self, actual: Token, expected: list[TokenType]) -> None:
        start_pos = actual.span[0]
        super().__init__(f"{start_pos.line}:{start_pos.column}: got an unexpected {token_type_descriptions[actual.type]}")
        self.actual = actual
        self.expected = expected

def is_prefix_operator(tt: TokenType) -> bool:
    return tt in [ TT_EXCL, TT_AMP, TT_SLASH ]

def is_suffix_operator(tt: TokenType) -> bool:
    return tt in [ TT_PLUS, TT_STAR, TT_QUEST ]

class Parser:

    def __init__(self, scanner: Scanner) -> None:
        self.scanner = scanner
        self._token_buffer = deque()

    def _get_token(self) -> Token:
        if self._token_buffer:
            return self._token_buffer.popleft()
        return self.scanner.scan()

    def _peek_token(self, offset=0) -> Token:
        while len(self._token_buffer) <= offset:
            self._token_buffer.append(self.scanner.scan())
        return self._token_buffer[offset]

    def _expect_token(self, expected: TokenType) -> Token:
        t0 = self._peek_token()
        if t0.type != expected:
            raise ParseError(t0, [ expected ])
        return self._get_token()

    def _parse_prim_expr(self) -> Expr:
        t1 = self._peek_token(1)
        label = None
        if t1.type == TT_COLON:
            label = self._expect_token(TT_IDENT)
            self._get_token()
        t2 = self._peek_token()
        if t2.type == TT_CHARSET:
            self._get_token()
            elements, ci = cast(tuple[list, bool], t2.value)
            expr = CharSetExpr(elements, ci)
        elif t2.type == TT_LPAREN:
            self._get_token()
            expr = self.parse_expr()
            self._expect_token(TT_RPAREN)
        elif t2.type == TT_IDENT:
            self._get_token()
            expr = RefExpr(t2.value)
        elif t2.type == TT_STR:
            self._get_token()
            expr = LitExpr(t2.value)
        else:
            raise ParseError(t2, [ TT_LBRACE, TT_LPAREN, TT_IDENT, TT_STR ])
        if label is not None:
            expr.label = label.value
        return expr

    def _parse_maybe_list_expr(self) -> Expr:
        element = self._parse_prim_expr()
        t0 = self._peek_token()
        if t0.type == TT_PERC:
            self._get_token()
            separator = self._parse_prim_expr()
            return ListExpr(element, separator)
        return element

    def _parse_expr_with_prefixes(self) -> Expr:
        tokens = []
        while True:
            t0 = self._peek_token()
            if not is_prefix_operator(t0.type):
                break
            self._get_token()
            tokens.append(t0.type)
        expr = self._parse_maybe_list_expr()
        for ty in reversed(tokens):
            if ty == TT_EXCL:
                expr = LookaheadExpr(expr, True)
            elif ty == TT_EXCL:
                expr = LookaheadExpr(expr, False)
            elif ty == TT_SLASH:
                expr = HideExpr(expr)
            else:
                raise RuntimeError(f'unexpected token type {token_type_descriptions[ty]}')
        return expr

    def _parse_expr_with_suffixes(self) -> Expr:
        t0 = self._peek_token(0)
        t1 = self._peek_token(1)
        label = None
        if t0.type == TT_IDENT and t1.type == TT_COLON:
            label = t0.value
            self._get_token()
            self._get_token()
        expr = self._parse_expr_with_prefixes()
        while True:
            t1 = self._peek_token()
            if not is_suffix_operator(t1.type):
                break
            if t1.type == TT_PLUS:
                self._get_token()
                expr = RepeatExpr(1, POSINF, expr)
            elif t1.type == TT_STAR:
                self._get_token()
                expr = RepeatExpr(0, POSINF, expr)
            elif t1.type == TT_QUEST:
                self._get_token()
                expr = RepeatExpr(0, 1, expr)
            else:
                raise ParseError(t1, [ TT_PLUS, TT_STAR ])
        expr.label = label
        return expr

    def _parse_expr_sequence(self) -> Expr:
        elements = [ self._parse_expr_with_suffixes() ]
        while True:
            t0 = self._peek_token(0)
            t1 = self._peek_token(1)
            if t0.type in [ TT_PUB, TT_EXTERN, TT_TOKEN ] or t1.type == TT_EQUAL or t0.type in [ TT_EOF, TT_VBAR, TT_RPAREN ]:
                break
            elements.append(self._parse_expr_with_suffixes())
        if len(elements) == 1:
            return elements[0]
        return SeqExpr(elements)

    def parse_expr(self) -> Expr:
        elements = [ self._parse_expr_sequence() ]
        while True:
            t0 = self._peek_token()
            if t0.type != TT_VBAR:
                break
            self._get_token()
            elements.append(self._parse_expr_sequence())
        if len(elements) == 1:
            return elements[0]
        return ChoiceExpr(elements)

    def parse_rule(self) -> Rule:
        decorators = []
        while True:
            t0 = self._peek_token()
            if t0.type != TT_AT:
                break
            self._get_token()
            name = self._expect_token(TT_IDENT).value
            decorators.append(Decorator(name))
        flags = 0
        t0 = self._get_token()
        if t0.type == TT_PUB:
            flags |= PUBLIC
            t0 = self._get_token()
        if t0.type == TT_EXTERN:
            flags |= EXTERN
            t0 = self._get_token()
        if t0.type == TT_TOKEN:
            flags |= FORCE_TOKEN
            t0 = self._get_token()
        if t0.type != TT_IDENT:
            raise ParseError(t0, [ TT_IDENT ])
        if flags & EXTERN:
            return Rule(decorators, flags, t0.value, None)
        self._expect_token(TT_EQUAL)
        expr = self.parse_expr()
        return Rule(decorators, flags, t0.value, expr)

    def parse_grammar(self) -> Grammar:
        elements = []
        while True:
            t0 = self._peek_token()
            if t0.type == TT_EOF:
                break
            elements.append(self.parse_rule())
        return Grammar(elements)
