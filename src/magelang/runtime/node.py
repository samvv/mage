
from magelang.runtime.text import Span

__all__ = [
    'BaseSyntax',
    'BaseNode',
    'BaseToken',
]

class BaseSyntax:

    def __init__(self) -> None:
        self._parent = None

    def has_parent(self) -> bool:
        return self._parent is not None


class BaseNode(BaseSyntax):
    pass


class BaseToken(BaseSyntax):

    def __init__(self, span: Span | None = None) -> None:
        super().__init__()
        self.span = span

