
from collections import deque
from typing import cast

from .ast import *
from .scanner import *

class ParseError(RuntimeError):

    def __init__(self, actual: Token, expected: list[TokenType]) -> None:
        start_pos = actual.span[0]
        super().__init__(f"{start_pos.line}:{start_pos.column}: got {token_type_descriptions[actual.type]} but expected something else")
        self.actual = actual
        self.expected = expected

_tt_ident = [ TT_IDENT, TT_TOKEN ]

def _is_prefix_operator(tt: TokenType) -> bool:
    return tt in [ TT_EXCL, TT_AMP, TT_SLASH ]

def _is_ident(token: Token) -> bool:
    return token.type in _tt_ident

class Parser:

    def __init__(self, scanner: Scanner, file: TextFile) -> None:
        self.scanner = scanner
        self.file = file
        self._token_buffer = deque()

    def _get_token_with_comment(self) -> Token:
        if self._token_buffer:
            return self._token_buffer.popleft()
        return self.scanner.scan()

    def _peek_token_with_comment(self, offset=0) -> Token:
        while len(self._token_buffer) <= offset:
            self._token_buffer.append(self.scanner.scan())
        return self._token_buffer[offset]

    def _peek_token(self, offset = 0) -> Token:
        i = 0
        k = 0
        while True:
            t0 = self._peek_token_with_comment(i + k)
            if t0.type == TT_COMMENT:
                i += 1
            elif k == offset:
                return t0
            else:
                k += 1

    def _get_token(self) -> Token:
        while True:
            t0 = self._get_token_with_comment()
            if t0.type != TT_COMMENT:
                return t0

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
        label = None
        decorators = []
        while True:
            t0 = self._peek_token()
            if t0.type != TT_AT:
                break
            self._get_token()
            name = self._expect_token(TT_IDENT)
            args = []
            t2 = self._peek_token()
            if t2.type == TT_LBRACE:
                self._get_token()
                t3 = self._peek_token()
                if t3.type != TT_RBRACE:
                    while True:
                        t3 = self._get_token()
                        if t3.type not in [ TT_IDENT, TT_INT ]:
                            raise ParseError(t3, [ TT_IDENT, TT_INT ])
                        args.append(t3.value)
                        t4 = self._get_token()
                        if t4.type == TT_COMMA:
                            self._get_token()
                        elif t4.type == TT_RBRACE:
                            break
                        else:
                            raise ParseError(t4, [ TT_COMMA, TT_RBRACE ])
                        args.append(t3.value)
            decorators.append(Decorator(cast(str, name.value), args))
        t1 = self._peek_token(1)
        if t1.type == TT_COLON:
            label = self._get_ident()
            self._get_token()
        t0 = self._peek_token()
        if t0.type == TT_TILDE or t0.type == TT_CHARSET:
            invert = False
            while t0.type == TT_TILDE:
                self._get_token()
                invert = not invert
                t0 = self._peek_token()
            self._get_token()
            elements, ci = cast(tuple[list, bool], t0.value)
            expr = MageCharSetExpr(elements=elements, ci=ci, invert=invert)
        elif t0.type == TT_LPAREN:
            self._get_token()
            expr = self.parse_expr()
            self._expect_token(TT_RPAREN)
        elif _is_ident(t0):
            name = token_to_string(t0)
            module_path = []
            self._get_token()
            while True:
                t3 = self._peek_token(0)
                t4 = self._peek_token(1)
                if t3.type != TT_DOT or t4.type != TT_IDENT:
                    break
                self._get_token()
                self._get_token()
                module_path.append(name)
                name = token_to_string(t4)
            expr = MageRefExpr(name=name, module_path=module_path)
        elif t0.type == TT_STR:
            self._get_token()
            assert(isinstance(t0.value, str))
            expr = MageLitExpr(text=t0.value)
        else:
            raise ParseError(t0, [ TT_LBRACE, TT_LPAREN, TT_IDENT, TT_STR ])
        if label is not None:
            expr.label = label.value
        expr.decorators.extend(decorators)
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

    def _lookahead_is_module_element(self) -> bool:
        i = 0
        while True:
            t0 = self._peek_token(i)
            if t0.type != TT_AT:
                break
            i += 2
            t1 = self._peek_token(i)
            if t1 == TT_LBRACE:
                while True:
                    i += 1
                    t2 = self._peek_token()
                    if t2.type == TT_RBRACE:
                        i += 1
                        break
        t0 = self._peek_token(i)
        t1 = self._peek_token(i+1)
        t2 = self._peek_token(i+2)
        return t0.type in [ TT_PUB, TT_EXTERN ] \
               or t1.type == TT_EQUAL \
               or t0.type == TT_TOKEN and t2.type == TT_EQUAL

    def _parse_expr_sequence(self) -> MageExpr:
        elements = [ self._parse_expr_with_suffixes() ]
        while True:
            t0 = self._peek_token(0)
            if self._lookahead_is_module_element() or t0.type in [ TT_EOF, TT_VBAR, TT_RPAREN, TT_RBRACE ]:
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

    def _parse_comment(self) -> str | None:
        i = 0
        comment = None
        while True:
            t0 = self._peek_token_with_comment(i)
            if t0.type != TT_COMMENT:
                token = t0
                break
            comment = t0
            i += 1
        if comment is None:
            return None
        return comment.value if comment.span[1].line == token.span[0].line-1 else None

    def parse_rule(self) -> MageRule:
        comment = self._parse_comment()
        decorators = []
        while True:
            t1 = self._peek_token()
            if t1.type != TT_AT:
                break
            self._get_token()
            name = token_to_string(self._get_ident())
            decorators.append(Decorator(name=name))
        flags = 0
        t1 = self._get_token()
        if t1.type == TT_PUB:
            flags |= PUBLIC
            t1 = self._get_token()
        if t1.type == TT_EXTERN:
            flags |= EXTERN
            t1 = self._get_token()
        if t1.type == TT_TOKEN:
            flags |= FORCE_TOKEN
            t1 = self._get_token()
        if not _is_ident(t1):
            raise ParseError(t1, [ TT_IDENT ])
        assert(isinstance(t1.value, str))
        t3 = self._peek_token()
        type_name = string_rule_type
        if t3.type == TT_RARROW:
            self._get_token()
            type_name = token_to_string(self._get_ident())
        if flags & EXTERN:
            return MageRule(name=t1.value, expr=None, comment=comment, decorators=decorators, flags=flags, type_name=type_name)
        self._expect_token(TT_EQUAL)
        expr = self.parse_expr()
        return MageRule(name=t1.value, expr=expr, comment=comment, decorators=decorators, flags=flags, type_name=type_name)

    def _peek_token_after_modifiers(self) -> Token:
        i = 0
        while True:
            t0 = self._peek_token(i)
            if t0.type not in [ TT_PUB, TT_EXTERN ]:
                return t0
            i += 1

    def parse_module(self) -> MageModule:
        t0 = self._peek_token()
        flags = 0
        if t0.type == TT_PUB:
            self._get_token()
            flags |= PUBLIC
        self._expect_token(TT_MOD)
        name = cast(str, self._expect_token(TT_IDENT).value)
        self._expect_token(TT_LBRACE)
        elements = self._parse_elements()
        self._expect_token(TT_RBRACE)
        return MageModule(name=name, elements=elements)

    def parse_element(self) -> MageModuleElement:
        t0 = self._peek_token_after_modifiers()
        if t0.type == TT_MOD:
            return self.parse_module()
        else:
            return self.parse_rule()

    def _parse_elements(self) -> list[MageModuleElement]:
        elements = []
        while True:
            t0 = self._peek_token()
            if t0.type == TT_EOF or t0.type == TT_RBRACE:
                break
            elements.append(self.parse_element())
        return elements

    def parse_grammar(self) -> MageGrammar:
        return MageGrammar(self._parse_elements(), self.file)

