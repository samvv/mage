from pprint import pprint
from magelang.logging import warn
from typing import assert_never, Any
from dataclasses import dataclass, field
from collections.abc import Callable, Iterable, Sequence

# TODO Make the only Event be a CharEvent, together with StartEvent and FinishEvent
#      That way we don't need tokens

type SyntaxKind = str

WHITESPACE  = 'whitespace'
PLUS        = 'plus'
MINUS       = 'minus'
MULT        = 'mult'
DIV         = 'div'
QUEST       = 'quest'
EXCL        = 'excl'
COLON       = 'colon'
LBRACKET    = 'lbracket'
RBRACKET    = 'rbracket'
IDENT       = 'ident'
END_OF_FILE = 'end_of_file'
LPAREN      = 'lparen'
RPAREN      = 'rparen'
DOT         = 'dot'
INTEGER     = 'integer'
EQUALS      = 'equals'

REF_EXPR     = 'ref_expr'
INT_EXPR     = 'int_expr'
NEST_EXPR    = 'nest_expr'
ASSIGN_EXPR  = 'assign_expr'
COMPOSE_EXPR = 'access_expr'
ADD_EXPR     = 'add_expr'
SUB_EXPR     = 'sub_expr'
DIV_EXPR     = 'div_expr'
SUB_EXPR     = 'sub_expr'
TERN_EXPR    = 'try_expr'
MUL_EXPR     = 'mul_expr'
FAC_EXPR     = 'fac_expr'
INDEX_EXPR   = 'index_expr'
POS_EXPR     = 'pos_expr'
NEG_EXPR     = 'neg_expr'

@dataclass(frozen=True)
class Token:
    kind: SyntaxKind
    len: int
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
        p0 = self._text_offset
        while True:
            c0 = self.peek()
            if c0 != ' ':
                break
            self.get()
        p1 = self._text_offset
        if p1 > p0:
            return Token(WHITESPACE, p1 - p0)
        c0 = self.get()
        if c0 == EOF:
            return Token(END_OF_FILE, 0)
        tt = tts.get(c0)
        if tt is not None:
            return Token(tt, 1)
        if c0.isalpha():
            name = c0
            while True:
                c1 = self.peek()
                if not c1.isalpha():
                    break
                self.get()
                name += c1
            return Token(IDENT, len(name), name)
        if c0.isdigit():
            value = int(c0)
            n = 1
            while True:
                c1 = self.peek()
                if not c1.isdigit():
                    break
                self.get()
                n += 1
                value = value * 10 + int(c1)
            return Token(INTEGER, n, value)
        raise RuntimeError()

def is_trivia(kind: SyntaxKind) -> bool:
    return kind == WHITESPACE

@dataclass(frozen=True)
class LexResult:
    kinds: Sequence[SyntaxKind]
    lens: Sequence[int]
    text: str

def tokenize(text: str) -> LexResult:
    kinds = []
    lens =  []
    scanner = Scanner(text)
    while True:
        token = scanner.scan()
        kinds.append(token.kind)
        lens.append(token.len)
        if token.kind == END_OF_FILE:
            break
    return LexResult(kinds, lens, text)

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

TOMBSTONE = '@tombstone'

class ParseError(RuntimeError):
    pass

type Event = StartEvent | FinishEvent | TokenEvent | ErrorEvent

@dataclass
class StartEvent:
    kind: list[SyntaxKind]
    forward_parent: int | None = None

@dataclass
class TokenEvent:
    kind: SyntaxKind

@dataclass
class FinishEvent:
    pass

@dataclass
class ErrorEvent:
    message: str

class CompletedMarker:

    def __init__(self, start_pos: int, end_pos: int, kind: SyntaxKind) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.kind = kind

class Marker:

    def __init__(self, pos: int) -> None:
        self.pos = pos

    def complete(self, p: 'Parser', kind: SyntaxKind) -> CompletedMarker:
        event = p.events[self.pos]
        assert(isinstance(event, StartEvent))
        event.kind.append(kind)
        p.events.append(FinishEvent())
        end_pos = len(p.events)
        return CompletedMarker(self.pos, end_pos, kind)

    def abandon(self, p: 'Parser') -> None:
        if self.pos == len(p.events)-1:
            event = p.events.pop()
            assert(isinstance(event, StartEvent))
            assert(event.kind == TOMBSTONE)
            assert(event.forward_parent is None)

class Parser:

    def __init__(self, kinds: Sequence[SyntaxKind], offset = 0) -> None:
        self._kinds = list(kind for kind in kinds if not is_trivia(kind))
        self._offset = offset
        self.events = list[Event]()

    def tell(self) -> int:
        return self._offset

    def seek(self, offset: int) -> None:
        self._offset = offset

    def nth_at(self, n: int, kind: SyntaxKind) -> bool:
        return self._kinds[self._offset + n] == kind

    def at(self, kind: SyntaxKind) -> bool:
        return self.nth_at(0, kind)

    def eat(self, kind: SyntaxKind) -> bool:
        if not self.at(kind):
            return False
        self.do_bump(kind)
        return True

    def bump(self, kind: SyntaxKind) -> None:
        assert(self.eat(kind))

    def bump_any(self) -> None:
        kind = self.current()
        if kind == END_OF_FILE:
            return
        self.do_bump(kind)

    def do_bump(self, kind: SyntaxKind) -> None:
        self._offset += 1
        self.events.append(TokenEvent(kind))

    def current(self) -> SyntaxKind:
        return self._kinds[self._offset] if self._offset < len(self._kinds) else END_OF_FILE

    def expect(self, tt: SyntaxKind) -> None:
        if not self.eat(tt):
            raise ParseError()

    def start(self) -> Marker:
        pos = len(self.events)
        self.events.append(StartEvent([]))
        return Marker(pos)

    def error(self, message) -> None:
        self.events.append(ErrorEvent(message))


@dataclass
class DynamicNode:
    kind: SyntaxKind
    children: list[Any] = field(default_factory=list)

@dataclass
class DynamicToken:
    kind: SyntaxKind
    text: str

class TreeBuilder:

    def __init__(self, res: LexResult) -> None:
        self.root = None
        self.text = res.text
        self.lens = res.lens
        self.kinds = res.kinds
        self.text_pos = 0
        self.token_pos = 0
        self._stack = list[DynamicNode]()

    def enter_node(self, kind: SyntaxKind) -> None:
        node = DynamicNode(kind)
        self._stack.append(node)

    def leave_node(self) -> None:
        node = self._stack.pop()
        if self._stack:
            self._stack[-1].children.append(node)
        else:
            self.root = node

    def token(self, kind: SyntaxKind) -> None:
        while is_trivia(self.kinds[self.token_pos]):
            self.text_pos += self.lens[self.token_pos]
            self.token_pos += 1
        n = self.lens[self.token_pos]
        p1 = self.text_pos
        p2 = p1 + n
        self._stack[-1].children.append(DynamicToken(kind, self.text[p1:p2]))
        self.text_pos += n
        self.token_pos += 1

    def error(self, message: str) -> None:
        raise ParseError(f'{self.text_pos}: {message}')

def parse_atom(p: Parser) -> CompletedMarker:
    m = p.start()
    if p.eat(IDENT):
        return m.complete(p, REF_EXPR)
    if p.eat(INTEGER):
        return m.complete(p, INT_EXPR)
    elif p.eat(LPAREN):
        parse_expr(p)
        p.expect(RPAREN)
        return m.complete(p, NEST_EXPR)
    else:
        raise ParseError()

def peek_prefix_operator(p: Parser) -> tuple[SyntaxKind, int] | None:
    if p.at(PLUS):
        return POS_EXPR, 9
    if p.at(MINUS):
        return NEG_EXPR, 9

def peek_postfix_operator(p: Parser) -> tuple[SyntaxKind, int] | None:
    if p.at(EXCL):
        return FAC_EXPR, 11
    if p.at(LBRACKET):
        return INDEX_EXPR, 11

def peek_infix_operator(p: Parser) -> tuple[SyntaxKind, int, int] | None:
    if p.at(EQUALS):
        return ASSIGN_EXPR, 2, 1
    if p.at(PLUS):
        return ADD_EXPR, 5, 6
    if p.at(MINUS):
        return SUB_EXPR, 5, 6
    if p.at(QUEST):
        return TERN_EXPR, 4, 3
    if p.at(MULT):
        return MUL_EXPR, 7, 8
    if p.at(DIV):
        return DIV_EXPR, 7, 8
    if p.at(DOT):
        return COMPOSE_EXPR, 14, 13

def parse_prefix_operator(p: Parser) -> tuple[SyntaxKind, int] | None:
    if p.eat(PLUS):
        return
    if p.eat(MINUS):
        return
    p.error("expected prefix operator")

def parse_postfix_operator(p: Parser) -> tuple[SyntaxKind, int] | None:
    if p.eat(EXCL):
        return
    if p.eat(LBRACKET):
        print("HEEERR")
        parse_expr(p)
        p.expect(RBRACKET)
        return
    p.error("expected postfix operator")

def parse_infix_operator(p: Parser) -> tuple[SyntaxKind, int, int] | None:
    if p.eat(EQUALS):
        return
    if p.eat(PLUS):
        return
    if p.eat(MINUS):
        return
    if p.eat(QUEST):
        parse_expr(p)
        p.expect(COLON)
        return
    if p.eat(MULT):
        return
    if p.eat(DIV):
        return
    if p.eat(DOT):
        return
    p.error("invalid infix operator")

def parse_expr_bp(p: Parser, min_bp: int) -> CompletedMarker:

    m = p.start()

    m_prefix = p.start()
    res = peek_prefix_operator(p)
    if res is None:
        lhs = parse_atom(p)
        m_prefix.abandon(p)
    else:
        prefix_kind, r_bp = res
        parse_prefix_operator(p)
        parse_expr_bp(p, r_bp)
        lhs = m_prefix.complete(p, prefix_kind)

    while True:

        if p.at(END_OF_FILE):
            break

        res = peek_postfix_operator(p)
        if res is not None:
            postfix_kind, l_bp = res
            if l_bp < min_bp:
                break
            parse_postfix_operator(p)
            lhs = m.complete(p, postfix_kind)
            continue

        res = peek_infix_operator(p)
        if res is not None:
            infix_kind, l_bp, r_bp = res
            if l_bp < min_bp:
                break
            parse_infix_operator(p)
            parse_expr_bp(p, r_bp)
            lhs = m.complete(p, infix_kind)
            continue

        # No valid operator was parsed
        break

    return lhs

def parse_expr(p: Parser) -> CompletedMarker:
    return parse_expr_bp(p, 0)

def process(events: list[Event], lexed: LexResult) -> DynamicNode | None:
    res = TreeBuilder(lexed)
    for i, event in enumerate(events):
        if isinstance(event, StartEvent):
            forward_parents = list[SyntaxKind]()
            forward_parents.extend(event.kind)
            idx = i
            fp = event.forward_parent
            while fp is not None:
                idx += fp
                event_2 = events[idx]
                assert(isinstance(event_2, StartEvent))
                forward_parents.extend(event_2.kind)
                fp = event_2.forward_parent
                events[idx] = StartEvent([])
            for kind in reversed(forward_parents):
                if kind != TOMBSTONE:
                    res.enter_node(kind)
        elif isinstance(event, FinishEvent):
            res.leave_node()
        elif isinstance(event, TokenEvent):
            res.token(event.kind)
        elif isinstance(event, ErrorEvent):
            res.error(event.message)
        else:
            assert_never(event)
    return res.root

infix_ops = {
    ADD_EXPR: '+',
    MUL_EXPR: '*',
    DIV_EXPR: '/',
    SUB_EXPR: '-',
    TERN_EXPR: '?',
    ASSIGN_EXPR: '=',
    COMPOSE_EXPR: '.',
}

prefix_ops = {
    POS_EXPR: '+',
    NEG_EXPR: '-',
}

postfix_ops = {
    FAC_EXPR: '!',
    INDEX_EXPR: 'index'
}

def syntax_to_sexp(value: Any) -> Expr:
    if isinstance(value, DynamicNode):
        if value.kind == NEST_EXPR:
            return syntax_to_sexp(value.children[1])
        if value.kind == INDEX_EXPR:
            return slist(Atom('index'), syntax_to_sexp(value.children[0]), syntax_to_sexp(value.children[2]))
        if value.kind == TERN_EXPR:
            return slist(Atom('?'), syntax_to_sexp(value.children[0]), syntax_to_sexp(value.children[2]), syntax_to_sexp(value.children[4]))
        if value.kind in [ REF_EXPR, INT_EXPR ]:
            return syntax_to_sexp(value.children[0])
        if value.kind in prefix_ops:
            return slist(Atom(prefix_ops[value.kind]), syntax_to_sexp(value.children[1]))
        if value.kind in postfix_ops:
            return slist(Atom(postfix_ops[value.kind]), syntax_to_sexp(value.children[0]))
        if value.kind in infix_ops:
            return slist(Atom(infix_ops[value.kind]), syntax_to_sexp(value.children[0]), syntax_to_sexp(value.children[2]))
        raise RuntimeError(value)
    if isinstance(value, DynamicToken):
        return Atom(value.text)
    raise RuntimeError(value)

def parse_to_sexp(text: str) -> str:
    lexed = tokenize(text)
    p = Parser(lexed.kinds)
    parse_expr(p)
    # pprint(p.events)
    root = process(p.events, lexed)
    return str(syntax_to_sexp(root))

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

if __name__ == '__main__':
    print(parse_to_sexp('a + b * c * d + e'))

