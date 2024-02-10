
import re
from typing import Any, NewType, Tuple, Optional

from sweetener import Record

TokenType = NewType('TokenType', int)

class Token(Record):
    type: TokenType
    span: Tuple[int, int]
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

    def __init__(self, ch, offset):
        super().__init__("unexpected character encountered")
        self.ch = ch
        self.offset = offset

class Scanner:

    def __init__(self, text, text_offset=0, offset=0):
        self.text = text
        self._text_offset = text_offset
        self.offset = offset

    def _get_char(self):
        ch = self.text[self._text_offset] \
                if self._text_offset < len(self.text) \
                else EOF
        self._text_offset += 1
        self.offset += 1
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
            return Token(TT_EOF, (self.offset, self.offset))

        if c0 == '\'':
            start_offset = self.offset
            self._get_char()
            text = ''
            escaping = False
            while True:
                c1 = self._get_char()
                if escaping:
                    if c1 in ASCII_ESCAPE_CHARS:
                        text += ASCII_ESCAPE_CHARS[c1]
                    else:
                        raise ScanError(c1, self.offset-1)
                    escaping = False
                else:
                    if c1 == EOF:
                        raise ScanError(EOF, self.offset)
                    elif c1 == '\\':
                        escaping = True
                    elif c1 == '\'':
                        break
                    else:
                        text += c1
            end_offset = self.offset
            return Token(TT_STR, (start_offset, end_offset), text)

        if c0 in DELIMITERS:
            start_offset = self.offset
            self._get_char()
            end_offset = self.offset
            return Token(DELIMITERS[c0], (start_offset, end_offset))

        if is_operator_part(c0):
            start_offset = self.offset
            self._get_char()
            text = c0 + self._take_while(is_operator_part)
            end_offset = self.offset
            if text not in OPERATORS:
                raise ScanError(text, start_offset)
            return Token(OPERATORS[text], (start_offset, end_offset))

        if c0 == '[':
            start_offset = self.offset
            self._get_char()
            elements = []
            while True:
                c1 = self._get_char()
                if c1 == EOF:
                    raise ScanError(self.offset, c1)
                if c1 == ']':
                    break
                c2 = self._get_char()
                if c2 == EOF:
                    raise ScanError(self.offset, c2)
                if c2 == ']':
                    break
                if c2 == '-':
                    c3 = self._get_char()
                    if c3 == EOF:
                        raise ScanError(self.offset, c3)
                    if c3 == ']':
                        break
                    elements.append((c1, c3))
            end_offset = self.offset
            return Token(TT_CHARSET, (start_offset, end_offset), elements)

        if c0.isdigit():
            start_offset = self.offset
            self._get_char()
            digits = c0 + self._take_while(lambda ch: ch.isdigit())
            end_offset = self.offset
            return Token(TT_INT, (start_offset, end_offset), int(digits))

        if c0.isalpha():
            start_offset = self.offset
            self._get_char()
            text = c0 + self._take_while(lambda ch: ch.isalnum())
            end_offset = self.offset
            if text in KEYWORDS:
                return Token(KEYWORDS[text], (start_offset, end_offset), text)
            return Token(TT_IDENT, (start_offset, end_offset), text)


        raise ScanError(c0, self.offset)

