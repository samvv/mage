
from collections import deque

from .ast import *
from .scanner import *

class ParseError(RuntimeError):

    def __init__(self, actual, expected):
        super().__init__(f"got an unexpected token")
        self.actual = actual
        self.expected = expected

def is_operator(tt):
    return tt in [ TT_PLUS, TT_STAR, TT_AMP, TT_EXCL, TT_PERC ]

class Parser:

    def __init__(self, scanner: Scanner) -> None:
        self.scanner = scanner
        self._token_buffer = deque()

    def _get_token(self) -> Token:
        if self._token_buffer:
            return self._token_buffer.popleft()
        return self.scanner.scan()

    def _peek_token(self, offset=1) -> Token:
        while len(self._token_buffer) < offset:
            self._token_buffer.append(self.scanner.scan())
        return self._token_buffer[offset-1]

    def _expect_token(self, expected: TokenType) -> Token:
        t0 = self._peek_token()
        if t0.type != expected:
            raise ParseError(t0, expected)
        return self._get_token()

    def _parse_prim_expr(self) -> Expr:
        t0 = self._peek_token()
        if t0.type == TT_CHARSET:
            self._get_token()
            return CharSetExpr(t0.value)
        elif t0.type == TT_LPAREN:
            self._get_token()
            e = self.parse_expr()
            self._expect_token(TT_RPAREN)
            return e
        elif t0.type == TT_IDENT:
            self._get_token()
            return RefExpr(t0.value)
        elif t0.type == TT_STR:
            self._get_token()
            return LitExpr(t0.value)
        else:
            raise ParseError(t0, [ TT_LBRACE, TT_LPAREN, TT_IDENT, TT_STR ])

    def _parse_expr_with_suffixes(self) -> Expr:
        e = self._parse_prim_expr()
        while True:
            t1 = self._peek_token()
            if not is_operator(t1.type):
                break
            if t1.type == TT_PLUS:
                self._get_token()
                e = RepeatExpr(1, POSINF, e)
            elif t1.type == TT_STAR:
                self._get_token()
                e = RepeatExpr(0, POSINF, e)
            else:
                raise ParseError(t1, [ TT_PLUS, TT_STAR ])
        return e

    def _parse_expr_sequence(self) -> Expr:
        elements = [ self._parse_expr_with_suffixes() ]
        while True:
            t0 = self._peek_token(1)
            t1 = self._peek_token(2)
            if t0.type == TT_PUB or t1.type == TT_EQUAL or t0.type == TT_EOF or t0.type == TT_VBAR:
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
        is_public = False
        is_token = False
        t0 = self._get_token()
        if t0.type == TT_PUB:
            is_public = True
            t0 = self._get_token()
        if t0.type == TT_TOKEN:
            is_token = True
            t0 = self._get_token()
        if t0.type != TT_IDENT:
            raise ParseError(t0, [ TT_IDENT ])
        self._expect_token(TT_EQUAL)
        e = self.parse_expr()
        #self._expect_token(TT_SEMI)
        return Rule(is_public, is_token, t0.value, e)

    def parse_grammar(self) -> Grammar:
        elements = []
        while True:
            t0 = self._peek_token()
            if t0.type == TT_EOF:
                break
            elements.append(self.parse_rule())
        return Grammar(elements)
