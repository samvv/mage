
import re
from typing import Any, NewType, Tuple, Optional

from sweetener import Record, warn

TokenType = NewType('TokenType', int)

class TextPos(Record):
    offset: int = 0
    line: int = 1
    column: int = 1

class Token(Record):
    type: TokenType
    span: Tuple[TextPos, TextPos]
    value: Optional[Any] = None

TT_EOF      = TokenType(1)
TT_IDENT    = TokenType(2)
TT_EQUAL    = TokenType(3)
TT_PUB      = TokenType(4)
TT_TOKEN    = TokenType(5)
TT_INT      = TokenType(6)
TT_LPAREN   = TokenType(7)
TT_RPAREN   = TokenType(8)
TT_LBRACE   = TokenType(9)
TT_RBRACE   = TokenType(10)
TT_LBRACKET = TokenType(11)
TT_RBRACKET = TokenType(12)
TT_COMMA    = TokenType(13)
TT_SEMI     = TokenType(14)
TT_STR      = TokenType(15)
TT_STAR     = TokenType(16)
TT_PLUS     = TokenType(17)
TT_AMP      = TokenType(18)
TT_EXCL     = TokenType(19)
TT_PERC     = TokenType(20)
TT_VBAR     = TokenType(21)
TT_CHARSET  = TokenType(22)
TT_COLON    = TokenType(23)

EOF = '\uFFFF'

def is_space(ch):
    return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'

OPERATOR_REGEX = re.compile('[+*%&!]')
def is_operator_part(ch):
    return OPERATOR_REGEX.match(ch)

DELIMITERS = {
    '(': TT_LPAREN,
    ')': TT_RPAREN,
    #'[': TT_LBRACKET,
    #']': TT_RBRACKET,
    '{': TT_LBRACE,
    '}': TT_RBRACE,
    ',': TT_COMMA,
    ';': TT_SEMI,
    '=': TT_EQUAL,
    '|': TT_VBAR,
    ':': TT_COLON,
    }

OPERATORS = {
    '+': TT_PLUS,
    '*': TT_STAR,
    '%': TT_PERC,
    '&': TT_AMP,
    '!': TT_EXCL,
    }

KEYWORDS = {
    'pub': TT_PUB,
    'token': TT_TOKEN,
    }

ASCII_ESCAPE_CHARS = {
    '\'': '\'',
    '\\': '\\',
    'a': '\a',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
    '0': '\0',
    }

class ScanError(RuntimeError):

    def __init__(self, ch: str, position: TextPos) -> None:
        super().__init__(f"{position.line}:{position.column}: unexpected character encountered")
        self.ch = ch
        self.position = position

class Scanner:

    def __init__(self, text: str, text_offset=0, init_pos: TextPos | None = None) -> None:
        if init_pos is None:
            init_pos = TextPos()
        self.text = text
        self._text_offset = text_offset
        self.curr_pos = init_pos

    def _get_char(self):
        if self._text_offset >= len(self.text):
            return EOF
        ch = self.text[self._text_offset] 
        self._text_offset += 1
        self.curr_pos.offset += 1
        if ch == '\n':
            self.curr_pos.line += 1
            self.curr_pos.column = 1
        else:
            self.curr_pos.column += 1
        return ch

    def _peek_char(self, offset=1):
        real_offset = self._text_offset + offset - 1
        return self.text[real_offset] \
                if real_offset < len(self.text) \
                else EOF

    def _take_while(self, pred):
        text = ''
        while True:
            c1 = self._peek_char()
            if not pred(c1):
                break
            self._get_char()
            text += c1
        return text

    def scan(self):

        c0 = self._peek_char()

        while True:
            if c0 == '#':
                self._get_char()
                while True:
                    c1 = self._get_char()
                    if c1 == '\n' or c1 == EOF:
                        break
                c0 = self._peek_char()
                continue
            if not is_space(c0):
                break
            self._get_char()
            c0 = self._peek_char()

        if c0 == EOF:
            return Token(TT_EOF, (self.curr_pos.clone(), self.curr_pos.clone()))

        if c0 == '\'':
            start_pos = self.curr_pos.clone()
            self._get_char()
            text = ''
            escaping = False
            while True:
                pos1 = self.curr_pos.clone()
                c1 = self._get_char()
                if escaping:
                    if c1 in ASCII_ESCAPE_CHARS:
                        text += ASCII_ESCAPE_CHARS[c1]
                    else:
                        raise ScanError(c1, pos1)
                    escaping = False
                else:
                    if c1 == EOF:
                        raise ScanError(EOF, pos1);
                    elif c1 == '\\':
                        escaping = True
                    elif c1 == '\'':
                        break
                    else:
                        text += c1
            end_pos = self.curr_pos.clone()
            return Token(TT_STR, (start_pos, end_pos), text)

        if c0 in DELIMITERS:
            start_pos = self.curr_pos.clone()
            self._get_char()
            end_pos = self.curr_pos.clone()
            return Token(DELIMITERS[c0], (start_pos, end_pos))

        if is_operator_part(c0):
            start_pos = self.curr_pos.clone()
            self._get_char()
            text = c0 + self._take_while(is_operator_part)
            end_pos = self.curr_pos.clone()
            if text not in OPERATORS:
                raise ScanError(text, start_pos)
            return Token(OPERATORS[text], (start_pos, end_pos))

        if c0 == '[':
            start_pos = self.curr_pos.clone()
            self._get_char()
            elements = []
            while True:
                c1 = self._get_char()
                if c1 == EOF:
                    raise ScanError(c1, self.curr_pos.clone())
                if c1 == ']':
                    break
                c2 = self._get_char()
                if c2 == EOF:
                    raise ScanError(c2, self.curr_pos.clone())
                if c2 == ']':
                    break
                if c2 == '-':
                    c3 = self._get_char()
                    if c3 == EOF:
                        raise ScanError(c3, self.curr_pos.clone())
                    if c3 == ']':
                        break
                    elements.append((c1, c3))
            end_pos = self.curr_pos.clone()
            return Token(TT_CHARSET, (start_pos, end_pos), elements)

        if c0.isdigit():
            start_pos = self.curr_pos.clone()
            self._get_char()
            digits = c0 + self._take_while(lambda ch: ch.isdigit())
            end_pos = self.curr_pos.clone()
            return Token(TT_INT, (start_pos, end_pos), int(digits))

        if c0.isalpha() or c0 == '_':
            start_pos = self.curr_pos.clone()
            self._get_char()
            text = c0 + self._take_while(lambda ch: ch.isalnum() or ch == '_')
            end_pos = self.curr_pos.clone()
            if text in KEYWORDS:
                return Token(KEYWORDS[text], (start_pos, end_pos), text)
            return Token(TT_IDENT, (start_pos, end_pos), text)

        raise ScanError(c0, self.curr_pos.clone())
