
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

_tt_ident = [ TT_IDENT, TT_TOKEN ]

def _is_prefix_operator(tt: TokenType) -> bool:
    return tt in [ TT_EXCL, TT_AMP, TT_SLASH ]

def _is_ident(token: Token) -> bool:
    return token.type in _tt_ident

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

    def _get_ident(self) -> Token:
        token = self._peek_token();
        if not _is_ident(token):
            raise ParseError(token, _tt_ident)
        return self._get_token()

    def _parse_prim_expr(self) -> MageExpr:
        t1 = self._peek_token(1)
        label = None
        if t1.type == TT_COLON:
            label = self._get_ident()
            self._get_token()
        t2 = self._peek_token()
        if t2.type == TT_TILDE or t2.type == TT_CHARSET:
            invert = False
            while t2.type == TT_TILDE:
                self._get_token()
                invert = not invert
                t2 = self._peek_token()
            self._get_token()
            elements, ci = cast(tuple[list, bool], t2.value)
            expr = MageCharSetExpr(elements=elements, ci=ci, invert=invert)
        elif t2.type == TT_LPAREN:
            self._get_token()
            expr = self.parse_expr()
            self._expect_token(TT_RPAREN)
        elif _is_ident(t2):
            self._get_token()
            expr = MageRefExpr(name=token_to_string(t2))
        elif t2.type == TT_STR:
            self._get_token()
            assert(isinstance(t2.value, str))
            expr = MageLitExpr(text=t2.value)
        else:
            raise ParseError(t2, [ TT_LBRACE, TT_LPAREN, TT_IDENT, TT_STR ])
        if label is not None:
            expr.label = label.value
        return expr

    def _parse_maybe_list_expr(self) -> MageExpr:
        element = self._parse_prim_expr()
        t0 = self._peek_token()
        if t0.type == TT_PERC:
            self._get_token()
            count = 0
            while True:
                t1 = self._peek_token()
                if t1.type != TT_PERC:
                    break
                self._get_token()
                count += 1
            separator = self._parse_prim_expr()
            return MageListExpr(element=element, separator=separator, min_count=count)
        return element

    def _parse_expr_with_prefixes(self) -> MageExpr:
        tokens = []
        while True:
            t0 = self._peek_token()
            if not _is_prefix_operator(t0.type):
                break
            self._get_token()
            tokens.append(t0.type)
        expr = self._parse_maybe_list_expr()
        for ty in reversed(tokens):
            if ty == TT_EXCL:
                expr = MageLookaheadExpr(expr=expr, is_negated=True)
            elif ty == TT_EXCL:
                expr = MageLookaheadExpr(expr=expr, is_negated=False)
            elif ty == TT_SLASH:
                expr = MageHideExpr(expr=expr)
            else:
                raise RuntimeError(f'unexpected token type {token_type_descriptions[ty]}')
        return expr

    def _parse_expr_with_suffixes(self) -> MageExpr:
        t0 = self._peek_token(0)
        t1 = self._peek_token(1)
        label = None
        if _is_ident(t0) and t1.type == TT_COLON:
            label = t0.value
            self._get_token()
            self._get_token()
        expr = self._parse_expr_with_prefixes()
        while True:
            t1 = self._peek_token()
            if t1.type == TT_PLUS:
                self._get_token()
                expr = MageRepeatExpr(min=1, max=POSINF, expr=expr)
            elif t1.type == TT_STAR:
                self._get_token()
                expr = MageRepeatExpr(min=0, max=POSINF, expr=expr)
            elif t1.type == TT_QUEST:
                self._get_token()
                expr = MageRepeatExpr(min=0, max=1, expr=expr)
            elif t1.type == TT_LBRACE:
                self._get_token()
                min = cast(int, self._expect_token(TT_INT).value)
                t2 = self._peek_token()
                max = min
                if t2.type == TT_COMMA:
                    max = POSINF
                    self._get_token()
                    t3 = self._peek_token()
                    if t3.type == TT_INT:
                        self._get_token()
                        max = cast(int, t3.value)
                self._expect_token(TT_RBRACE)
                expr = MageRepeatExpr(min=min, max=max, expr=expr)
            else:
                break
        expr.label = label
        return expr

    def _lookahead_is_rule(self) -> bool:
            t0 = self._peek_token(0)
            t1 = self._peek_token(1)
            t2 = self._peek_token(2)
            return t0.type in [ TT_PUB, TT_EXTERN, TT_AT ] \
                   or t1.type == TT_EQUAL \
                   or t0.type == TT_TOKEN and t2.type == TT_EQUAL

    def _parse_expr_sequence(self) -> MageExpr:
        elements = [ self._parse_expr_with_suffixes() ]
        while True:
            t0 = self._peek_token(0)
            if self._lookahead_is_rule() or t0.type in [ TT_EOF, TT_VBAR, TT_RPAREN ]:
                break
            elements.append(self._parse_expr_with_suffixes())
        if len(elements) == 1:
            return elements[0]
        return MageSeqExpr(elements=elements)

    def parse_expr(self) -> MageExpr:
        elements = [ self._parse_expr_sequence() ]
        while True:
            t0 = self._peek_token()
            if t0.type != TT_VBAR:
                break
            self._get_token()
            elements.append(self._parse_expr_sequence())
        if len(elements) == 1:
            return elements[0]
        return MageChoiceExpr(elements=elements)

    def parse_rule(self) -> MageRule:
        comment = self.scanner.take_comment()
        decorators = []
        while True:
            t0 = self._peek_token()
            if t0.type != TT_AT:
                break
            self._get_token()
            name = token_to_string(self._get_ident())
            decorators.append(Decorator(name=name))
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
        if not _is_ident(t0):
            raise ParseError(t0, [ TT_IDENT ])
        assert(isinstance(t0.value, str))
        t3 = self._peek_token()
        type_name = string_rule_type
        if t3.type == TT_RARROW:
            self._get_token()
            type_name = token_to_string(self._get_ident())
        if flags & EXTERN:
            return MageRule(name=t0.value, expr=None, comment=comment, decorators=decorators, flags=flags, type_name=type_name)
        self._expect_token(TT_EQUAL)
        expr = self.parse_expr()
        return MageRule(name=t0.value, expr=expr, comment=comment, decorators=decorators, flags=flags, type_name=type_name)

    def parse_grammar(self) -> MageGrammar:
        elements = []
        while True:
            t0 = self._peek_token()
            if t0.type == TT_EOF:
                break
            elements.append(self.parse_rule())
        return MageGrammar(elements)

