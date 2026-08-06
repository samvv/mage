
from dataclasses import dataclass
from collections.abc import Callable, Iterable, Sequence

PLUS        = 0
MINUS       = 1
MULT        = 2
DIV         = 3
QUEST       = 4
EXCL        = 5
COLON       = 6
LBRACKET    = 7
RBRACKET    = 8
IDENT       = 9
END_OF_FILE = 10
LPAREN      = 11
RPAREN      = 12
DOT         = 13
INTEGER     = 14
EQUALS      = 15

type TokenType = int

@dataclass(frozen=True)
class Token:
    type: TokenType
    value: int | str | None = None

tts = {
    '+': PLUS,
    '-': MINUS,
    '.': DOT,
    '*': MULT,
    '/': DIV,
    '?': QUEST,
    '!': EXCL,
    ':': COLON,
    '=': EQUALS,
    '[': LBRACKET,
    ']': RBRACKET,
    '(': LPAREN,
    ')': RPAREN,
}

EOF = '\uFFFF'

class Scanner:

    def __init__(self, text: str) -> None:
        self._text = text
        self._text_offset = 0

    def get(self) -> str:
        if self._text_offset == len(self._text):
            return EOF
        ch = self._text[self._text_offset]
        self._text_offset += 1
        return ch

    def peek(self) -> str:
        return self._text[self._text_offset] if self._text_offset < len(self._text) else EOF

    def scan(self) -> Token:
        while True:
            c0 = self.peek()
            if c0 != ' ':
                break
            self.get()
        c0 = self.get()
        if c0 == EOF:
            return Token(END_OF_FILE)
        tt = tts.get(c0)
        if tt is not None:
            return Token(tt)
        if c0.isalpha():
            name = c0
            while True:
                c1 = self.peek()
                if not c1.isalpha():
                    break
                self.get()
                name += c1
            return Token(IDENT, name)
        if c0.isdigit():
            value = int(c0)
            while True:
                c1 = self.peek()
                if not c1.isdigit():
                    break
                self.get()
                value = value * 10 + int(c1)
            return Token(INTEGER, value)
        raise RuntimeError()

def tokenize(text: str) -> Iterable[Token]:
    scanner = Scanner(text)
    while True:
        token = scanner.scan()
        if token.type == END_OF_FILE:
            break
        yield token

@dataclass(frozen=True)
class Atom:
    value: str

    def __str__(self) -> str:
        return self.value

type Expr = Atom | Cons

@dataclass(frozen=True)
class Cons:
    head: Expr
    tail: Expr

    def __str__(self) -> str:
        out = '('
        out += str(self.head)
        el = self.tail
        while el is not nil:
            if isinstance(el, Cons):
                out += ' ' + str(el.head)
                el = el.tail
            elif isinstance(el, Atom):
                out += ' . ' + str(el)
                break
        out += ')'
        return out

def slist(*els: Expr) -> Expr:
    out = nil
    for el in reversed(els):
        out = Cons(el, out)
    return out

nil = Atom('\'()')

class ParseError(RuntimeError):
    pass

class Parser:

    def __init__(self, tokens: Sequence[Token], offset = 0) -> None:
        self._tokens = tokens
        self._offset = offset

    def tell(self) -> int:
        return self._offset

    def seek(self, offset: int) -> None:
        self._offset = offset

    def get(self) -> Token:
        if self._offset == len(self._tokens):
            return Token(END_OF_FILE)
        token = self._tokens[self._offset]
        self._offset += 1
        return token

    def peek(self) -> Token:
        return self._tokens[self._offset] if self._offset < len(self._tokens) else Token(END_OF_FILE)

    def expect(self, tt: TokenType) -> None:
        if self.get().type != tt:
            raise ParseError()

def parse_atom(p: Parser) -> Expr:
    t0 = p.get()
    if t0.type in [ IDENT, INTEGER ]:
        return Atom(str(t0.value))
    elif t0.type == LPAREN:
        e = parse_expr(p)
        p.expect(RPAREN)
        return e
    else:
        raise ParseError()

def parse_prefix_operator(p: Parser) -> tuple[Callable[[Expr], Expr], int] | None:
    t0 = p.peek()
    if t0.type == PLUS:
        p.get()
        return lambda rhs: slist(Atom('+'), rhs), 9
    if t0.type == MINUS:
        p.get()
        return lambda rhs: slist(Atom('-'), rhs), 9

def parse_postfix_operator(p: Parser) -> tuple[Callable[[Expr], Expr], int] | None:
    t0 = p.peek()
    if t0.type == EXCL:
        p.get()
        return lambda lhs: Cons(Atom('!'), Cons(lhs, nil)), 11
    if t0.type == LBRACKET:
        p.get()
        rhs = parse_expr(p)
        p.expect(RBRACKET)
        return lambda lhs: Cons(Atom('index'), Cons(lhs, Cons(rhs, nil))), 11

def parse_infix_operator(p: Parser) -> tuple[Callable[[Expr, Expr], Expr], int, int] | None:
    t0 = p.peek()
    if t0.type == EQUALS:
        p.get()
        return lambda lhs, rhs: slist(Atom('='), lhs, rhs), 2, 1
    if t0.type == PLUS:
        p.get()
        return lambda lhs, rhs: slist(Atom('+'), lhs, rhs), 5, 6
    if t0.type == MINUS:
        p.get()
        return lambda lhs, rhs: slist(Atom('-'), lhs, rhs), 5, 6
    if t0.type == QUEST:
        p.get()
        mhs = parse_expr(p)
        p.expect(COLON)
        return lambda lhs, rhs: slist(Atom('?'), lhs, mhs, rhs), 4, 3
    if t0.type == MULT:
        p.get()
        return lambda lhs, rhs: slist(Atom('*'), lhs, rhs), 7, 8
    if t0.type == DIV:
        p.get()
        return lambda lhs, rhs: slist(Atom('/'), lhs, rhs), 7, 8
    if t0.type == DOT:
        p.get()
        return lambda lhs, rhs: slist(Atom('.'), lhs, rhs), 14, 13

def parse_expr_bp(p: Parser, min_bp: int) -> Expr:

    res = parse_prefix_operator(p)
    if res is None:
        lhs = parse_atom(p)
    else:
        build, r_bp = res
        rhs = parse_expr_bp(p, r_bp)
        lhs = build(rhs)

    while True:

        if p.peek().type == END_OF_FILE:
            break

        before_op = p.tell()

        res = parse_postfix_operator(p)
        if res is not None:
            build, l_bp = res
            if l_bp < min_bp:
                # Could be a GOTO to below when compiling
                p.seek(before_op)
                break
            lhs = build(lhs)
            continue

        res = parse_infix_operator(p)
        if res is not None:
            build, l_bp, r_bp = res
            if l_bp < min_bp:
                # Could be a GOTO to below when compiling
                p.seek(before_op)
                break
            rhs = parse_expr_bp(p, r_bp)
            lhs = build(lhs, rhs)
            continue

        # No valid operator was parsed
        p.seek(before_op)
        break

    return lhs

def parse_expr(p: Parser) -> Expr:
    return parse_expr_bp(p, 0)

def parse_to_sexp(text: str) -> str:
    return str(parse_expr(Parser(list(tokenize(text)))))

def test_parse_atom():
    assert(parse_to_sexp('1') == '1')

def test_parse_basic_infix_prec():
    assert(parse_to_sexp('1 + 2 * 3') == '(+ 1 (* 2 3))')

def test_parse_infix_prec_2():
    assert(parse_to_sexp('a + b * c * d + e') == '(+ (+ a (* (* b c) d)) e)')

def test_parse_infix_prec_3():
    assert(parse_to_sexp('1 + 2 + f . g . h * 3 * 4') == '(+ (+ 1 2) (* (* (. f (. g h)) 3) 4))')

def test_parse_infix_dot_rassoc():
    assert(parse_to_sexp('f . g . h') == '(. f (. g h))')

def test_parse_prefix_with_lower_infix():
    assert(parse_to_sexp('--1 * 2') == '(* (- (- 1)) 2)')

def test_parse_prefix_with_higher_infix():
    assert(parse_to_sexp('--f . g') == '(- (- (. f g)))')

def test_parse_prefix_postfix_prec():
    assert(parse_to_sexp('-9!') == "(- (! 9))")

def test_parse_postfix_with_higher_infix():
    assert(parse_to_sexp('f . g !') == '(! (. f g))')

def test_parse_nested():
    assert(parse_to_sexp('(((0)))') == '0')

def test_parse_array_access():
    assert(parse_to_sexp('x[0][1]') == '(index (index x 0) 1)')

def test_parse_ternary():
    assert(parse_to_sexp('a ? b : c ? d : e') == '(? a b (? c d e))')

def test_parse_ternary_with_assignment():
    assert(parse_to_sexp('a = 0 ? b : c = d') == '(= a (= (? 0 b c) d))')
