
import re
from textwrap import dedent
from typing import Any, NewType

from magelang.runtime.text import Span, TextFile

TokenType = NewType('TokenType', int)

class TextPos:

    def __init__(self, offset = 0, line = 1, column = 1) -> None:
        self.offset = offset
        self.line = line
        self.column = column

    def clone(self) -> 'TextPos':
        return TextPos(self.offset, self.line, self.column)

class Token:

    def __init__(self, ty: TokenType, span: Span, value: Any | None = None) -> None:
        self.type = ty
        self.span = span
        self.value = value

def _is_hex_digit(ch: str) -> bool:
    return ch in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C' 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f' ]

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
TT_EXTERN   = TokenType(24)
TT_SLASH    = TokenType(25)
TT_QUEST    = TokenType(26)
TT_AT       = TokenType(27)
TT_TILDE    = TokenType(28)
TT_RARROW   = TokenType(29)
TT_COMMENT  = TokenType(30)
TT_MOD      = TokenType(31)
TT_DOT      = TokenType(32)

EOF = '\uFFFF'

def is_space(ch):
    return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'

_operator_regex = re.compile(r'[<>~+\-*%&!?\\]')
def is_operator_part(ch) -> bool:
    return _operator_regex.match(ch) is not None

_simple_tokens = {
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
    '@': TT_AT,
    '.': TT_DOT,
    }

_operator_to_token_type = {
    '+': TT_PLUS,
    '*': TT_STAR,
    '%': TT_PERC,
    '&': TT_AMP,
    '!': TT_EXCL,
    '?': TT_QUEST,
    '\\': TT_SLASH,
    '~': TT_TILDE,
    '->': TT_RARROW,
    }

_keyword_to_token_type = {
    'pub': TT_PUB,
    'token': TT_TOKEN,
    'extern': TT_EXTERN,
    'mod': TT_MOD,
    }

_ascii_escape_chars = {
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

token_type_descriptions = {
    TT_EOF: "end-of-file",
    TT_IDENT: "an identifier",
    TT_EQUAL: "'='",
    TT_PUB: "'pub'",
    TT_TOKEN: "'token'",
    TT_INT: "an integer",
    TT_LPAREN: "'('",
    TT_RPAREN: "')'",
    TT_LBRACE: "'{'",
    TT_RBRACE: "'}'",
    TT_LBRACKET: "'['",
    TT_RBRACKET: "']'",
    TT_COMMA: "','",
    TT_SEMI: "';'",
    TT_STR: "a piece of quoted text",
    TT_STAR: "'*'",
    TT_PLUS: "'+'",
    TT_AMP: "'&'",
    TT_EXCL: "'!'",
    TT_PERC: "'%'",
    TT_VBAR: "'|'",
    TT_CHARSET: "a character range (like [a-z])",
    TT_COLON: "':'",
    TT_EXTERN: "'extern'",
    TT_SLASH: "'$'",
    TT_QUEST: "'?'",
    TT_AT: "'@'",
    TT_TILDE: "'~'",
    TT_RARROW: "'->'",
    TT_MOD: "'mod'",
    TT_DOT: '.',
    }

def token_to_string(token: Token) -> str:
    if token.type == TT_IDENT:
        assert(isinstance(token.value, str))
        return token.value
    if token.type  == TT_TOKEN:
        return 'token'
    raise NotImplementedError()

class ScanError(RuntimeError):

    def __init__(self, file: TextFile, ch: str, offset: int, message: str | None = None) -> None:
        start_line = file.get_line(offset)
        start_column = file.get_column(offset)
        full_message = f"{file.filename}:{start_line}:{start_column}: "
        if message is not None:
            full_message += message
        elif ch == EOF:
            full_message += "unexpected end-of-file reached"
        else:
            full_message += f"unexpected character {repr(ch)} encountered"
        super().__init__(full_message)
        self.file = file
        self.ch = ch
        self.offset = offset

class Scanner:

    def __init__(self, file_or_text: str | TextFile, text_offset=0, init_pos: TextPos | None = None) -> None:
        if init_pos is None:
            init_pos = TextPos()
        if isinstance(file_or_text, str):
            file_or_text = TextFile(file_or_text)
        self.file = file_or_text
        self.text = file_or_text.text
        self._text_offset = text_offset
        self._last_comment_line = 0
        self.curr_pos = init_pos
        self._comment = ''

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

    def _peek_char(self, offset=0):
        real_offset = self._text_offset + offset
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

    def _scan_hex_digit(self) -> int:
        ch = self._get_char()
        if not _is_hex_digit(ch):
            raise ScanError(self.file, ch, self._text_offset)
        return int(ch, 16)

    def _scan_escapable_char(self) -> str:
        c0 = self._get_char()
        if c0 == '\\':
            c1 = self._get_char()
            if c1 == 'x':
                d0 = self._scan_hex_digit()
                d1 = self._scan_hex_digit()
                return chr(d0 * 16 + d1)
            elif c1 == 'u':
                d0 = self._scan_hex_digit()
                d1 = self._scan_hex_digit()
                d2 = self._scan_hex_digit()
                d3 = self._scan_hex_digit()
                return chr(d0 * 16 * 16 * 16 + d1 * 16 * 16 + d2 * 16 + d3)
            elif c1 in _ascii_escape_chars:
                return _ascii_escape_chars[c1]
            else:
                return c1
        else:
            return c0

    def scan(self) -> Token:

        doc_comment = ''
        doc_comment_start_pos = None
        doc_comment_end_pos = None

        def reset_doc_comment():
            nonlocal doc_comment, doc_comment_start_pos, doc_comment_end_pos
            doc_comment = ''
            doc_comment_start_pos = None
            doc_comment_end_pos = None

        while True:
            c0 = self._peek_char(0)
            c1 = self._peek_char(1)
            if c0 == '#' and c1 == '#':
                # If the next doc line is not underneath the previous one
                if doc_comment_end_pos is not None and doc_comment_end_pos.line != self.curr_pos.line-1:
                    reset_doc_comment()
                # If this is the start of a new doc comment
                if doc_comment_start_pos is None:
                    doc_comment_start_pos = self.curr_pos.clone()
                # Get the '##'
                self._get_char()
                self._get_char()
                # Get the rest of the line
                while True:
                    c1 = self._peek_char()
                    if c1 == '\n' or c1 == EOF:
                        doc_comment_end_pos = self.curr_pos.clone()
                        self._get_char()
                        break
                    self._get_char()
                    doc_comment += c1
                doc_comment += '\n'
                continue
            if c0 == '#':
                reset_doc_comment()
                self._get_char()
                while True:
                    c2 = self._get_char()
                    if c2 == '\n' or c2 == EOF:
                        break
                continue
            if is_space(c0):
                reset_doc_comment()
                self._get_char()
                continue
            break

        if doc_comment:
            assert(doc_comment_start_pos is not None)
            assert(doc_comment_end_pos is not None)
            return Token(TT_COMMENT, Span(doc_comment_start_pos.offset, doc_comment_end_pos.offset), dedent(doc_comment))

        if c0 == EOF:
            return Token(TT_EOF, Span(self._text_offset, self._text_offset))

        if c0 == '\'':
            start_offset = self._text_offset
            self._get_char()
            text = ''
            escaping = False
            while True:
                offset1 = self._text_offset
                c1 = self._get_char()
                if escaping:
                    if c1 in _ascii_escape_chars:
                        text += _ascii_escape_chars[c1]
                    else:
                        raise ScanError(self.file, c1, offset1)
                    escaping = False
                else:
                    if c1 == EOF:
                        raise ScanError(self.file, EOF, offset1);
                    elif c1 == '\\':
                        escaping = True
                    elif c1 == '\'':
                        break
                    else:
                        text += c1
            end_offset = self._text_offset
            return Token(TT_STR, Span(start_offset, end_offset), text)

        if c0 in _simple_tokens:
            start_offset = self._text_offset
            self._get_char()
            end_offset = self._text_offset
            return Token(_simple_tokens[c0], Span(start_offset, end_offset))

        if c0 == '%':
            start_offset = self._text_offset
            self._get_char()
            end_offset = self._text_offset
            return Token(TT_PERC, Span(start_offset, end_offset))

        if is_operator_part(c0):
            start_offset = self._text_offset
            self._get_char()
            text = c0 + self._take_while(is_operator_part)
            end_offset = self._text_offset
            if text not in _operator_to_token_type:
                raise ScanError(self.file, text, start_offset)
            return Token(_operator_to_token_type[text], Span(start_offset, end_offset))

        if c0 == '[':
            start_offset = self._text_offset
            self._get_char()
            elements = []
            while True:
                if self._peek_char() == ']':
                    self._get_char()
                    break
                c1 = self._scan_escapable_char()
                if c1 == EOF:
                    raise ScanError(self.file, c1, self._text_offset)
                if self._peek_char() == '-':
                    self._get_char()
                    c2 = self._scan_escapable_char()
                    if c2 == EOF:
                        raise ScanError(self.file, c2, self._text_offset)
                    elements.append((c1, c2))
                else:
                    elements.append(c1)
            ci = False
            c4 = self._peek_char()
            if c4 == 'i':
                self._get_char()
                ci = True
            end_offset = self._text_offset
            return Token(TT_CHARSET, Span(start_offset, end_offset), (elements, ci))

        if c0.isdigit():
            start_offset = self._text_offset
            self._get_char()
            digits = c0 + self._take_while(lambda ch: ch.isdigit())
            end_offset = self._text_offset
            return Token(TT_INT, Span(start_offset, end_offset), int(digits))

        if c0.isalpha() or c0 == '_':
            start_offset = self._text_offset
            self._get_char()
            text = c0 + self._take_while(lambda ch: ch.isalnum() or ch == '_')
            end_offset = self._text_offset
            if text in _keyword_to_token_type:
                return Token(_keyword_to_token_type[text], Span(start_offset, end_offset), None)
            return Token(TT_IDENT, Span(start_offset, end_offset), text)

        raise ScanError(self.file, c0, self._text_offset)
