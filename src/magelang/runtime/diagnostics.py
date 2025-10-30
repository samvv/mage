

from dataclasses import dataclass
from enum import IntEnum
import math
from typing import Protocol

from magelang.util import unreachable
from magelang.runtime.text import Span, TextFile

__all__ = [
    'Severity',
    'Diagnostic',
    'Diagnostics',
    'ConsoleDiagnostics',
]


def count_digits(n, base=10):
    return 1 if n == 0 or n == 1 else math.ceil(math.log(n+1, base))


class Severity(IntEnum):
    debug = 1
    info = 5
    warn = 6
    error = 7
    fatal = 10


@dataclass
class Diagnostic:
    severity: Severity
    message: str
    file: TextFile | None = None
    span: Span | None = None


ANSI_BOLD        = '\u001b[1m'
ANSI_FAINT       = '\u001b[2m'
ANSI_ITALIC      = '\u001b[3m'

ANSI_FG_BLACK   = '\u001b[30m'
ANSI_FG_RED     = '\u001b[31m'
ANSI_FG_GREEN   = '\u001b[32m'
ANSI_FG_YELLOW  = '\u001b[33m'
ANSI_FG_BLUE    = '\u001b[34m'
ANSI_FG_MAGENTA = '\u001b[35m'
ANSI_FG_CYAN    = '\u001b[36m'
ANSI_FG_WHITE   = '\u001b[37m'
ANSI_FG_RESET   = '\u001b[0m'

ANSI_BG_BLACK   = '\u001b[40m'
ANSI_BG_RED     = '\u001b[41m'
ANSI_BG_GREEN   = '\u001b[42m'
ANSI_BG_YELLOW  = '\u001b[43m'
ANSI_BG_BLUE    = '\u001b[44m'
ANSI_BG_MAGENTA = '\u001b[45m'
ANSI_BG_CYAN    = '\u001b[46m'
ANSI_BG_WHITE   = '\u001b[47m'

ANSI_RESET      = '\u001b[0m'


def print_excerpt(text: TextFile | str, span: Span, lines_pre=1, lines_post=1, gutter_width: int | None = None):

    if not isinstance(text, TextFile):
        text = TextFile(text)

    out = ''

    start_line = text.get_line(span.start)
    end_line = text.get_line(span.end)
    start_line_offset = text.get_offset(start_line)
    end_line_offset = text.get_offset(end_line+1)
    start_column = span.start - start_line_offset + 1
    end_column = span.end - text.get_offset(end_line) + 1
    pre_line = max(start_line-lines_pre, 1)
    pre_offset = text.get_offset(pre_line)
    post_offset = text.get_offset(end_line+lines_post+1)

    if gutter_width is None:
        gutter_width = max(2, count_digits(end_line+lines_post))

    # initial position in text
    line = pre_line
    column = 1
    offset = 0

    def print_guttered(start, end):
        nonlocal out, line
        for i in range(start, end):
            ch = text[i]
            if ch == '\n':
                out += '\n'
                line += 1
                print_gutter(line)
            else:
                out += ch

    def print_gutter(line=None):
        nonlocal out
        num_width = 0 if line is None else count_digits(line)
        out += ANSI_FG_BLACK + ANSI_BG_WHITE
        for _ in range(0, gutter_width - num_width):
            out += ' '
        if line is not None:
            out += str(line)
        out += ANSI_RESET + ' '

    def print_underline():
        nonlocal out
        k = start_column if line == start_line else 1
        l = end_column if line == end_line else column
        if l - k > 0:
            out += '\n'
            print_gutter()
            for _ in range(0, k-1):
                out += ' '
            out += ANSI_FG_RED
            for _ in range(k-1, l-1):
                out += '~'
            out += ANSI_RESET

    print_gutter(line)

    print_guttered(pre_offset, start_line_offset)

    for i in range(start_line_offset, end_line_offset):
        ch = text[i]
        if ch == '\n':
            print_underline()
            line += 1
            column = 1
            out += ch
            print_gutter(line)
        else:
            column += 1
            out += ch

    print_guttered(end_line_offset, post_offset)

    print(out)

class Diagnostics(Protocol):

    def add(self, diagnostic: Diagnostic) -> None: ...


class ConsoleDiagnostics(Diagnostics):

    def add(self, diagnostic: Diagnostic) -> None:
        if diagnostic.severity == Severity.debug:
            color = ANSI_FG_MAGENTA
            tag = 'debug'
        elif diagnostic.severity == Severity.info:
            color = ANSI_FG_YELLOW
            tag = 'info'
        elif diagnostic.severity == Severity.warn:
            color = ANSI_FAINT + ANSI_FG_RED
            tag = 'warning'
        elif diagnostic.severity == Severity.error:
            color = ANSI_FG_RED
            tag = 'error'
        elif diagnostic.severity == Severity.fatal:
            color = ANSI_FG_WHITE + ANSI_BG_RED
            tag = 'fatal'
        else:
            unreachable()
        print(ANSI_BOLD + color + tag + ANSI_RESET + ': ' + diagnostic.message)
        if diagnostic.file is not None and diagnostic.span is not None:
            print_excerpt(diagnostic.file, diagnostic.span)
