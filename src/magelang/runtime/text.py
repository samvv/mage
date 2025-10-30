
__all__ = [
    'TextFile',
    'Span',
]


class TextFile:

    def __init__(self, text, filename="#<anonymous>"):
        self.filename = filename
        self.text = text
        self.lines = list()

    def __iter__(self):
        return iter(self.text)

    def __getitem__(self, key):
        return self.text[key]

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text

    def count_lines_until_offset(self, end_offset):
        end_offset = min(end_offset, len(self.text)-1)
        line = 1 if not self.lines else len(self.lines)+1
        offset = 0 if line == 1 else self.lines[line-2]
        while offset <= end_offset:
            ch = self.text[offset]
            offset += 1
            if ch == '\n':
                self.lines.append(offset)
                line += 1

    def count_lines_until_line(self, end_line):
        line = 1 if not self.lines else len(self.lines)+1
        offset = 0 if line == 1 else self.lines[line-2]
        while line <= end_line and offset < len(self.text):
            ch = self.text[offset]
            offset += 1
            if ch == '\n':
                self.lines.append(offset)
                line += 1

    def get_offset(self, line):
        if line <= 1:
            return 0
        self.count_lines_until_line(line)
        line = min(line, len(self.lines)+1)
        return self.lines[line-2]

    def get_column(self, offset):
        return offset - self.get_offset(self.get_line(offset))

    def get_line(self, offset):
        if offset == 0:
            return 1
        if offset >= len(self.text):
            raise RuntimeError(f'offset out of text bounds')
        self.count_lines_until_offset(offset)
        for i, line_start_offset in enumerate(self.lines):
            if line_start_offset > offset:
                return i+1
        return len(self.lines)+1

    def count_lines(self):
        self.count_lines_until_offset(len(self.text)-1)
        return len(self.lines)+1


class TextPos:

    def __init__(self, offset: int, line: int, column: int) -> None:
        self.offset = offset
        self.line = line
        self.column = column


class Span(tuple[int, int]):

    @property
    def start_offset(self) -> int:
        return self[0]

    @property
    def end_offset(self) -> int:
        return self[1]

    def __len__(self) -> int:
        return self.end_offset - self.start_offset


