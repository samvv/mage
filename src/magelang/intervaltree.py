
from collections.abc import Iterable, Iterator, MutableSet
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar, cast

Self = TypeVar('Self', bound='PointLike')

class PointLike(Protocol):
    def __lt__(self: Self, value: 'Self', /) -> bool: ...
    def __gt__(self: Self, value: 'Self', /) -> bool: ...
    def __le__(self: Self, value: 'Self', /) -> bool: ...
    def __ge__(self: Self, value: 'Self', /) -> bool: ...

Point = TypeVar('Point', bound=PointLike)
Data = TypeVar('Data', default=None)

@dataclass(frozen=True)
class Interval(Generic[Point, Data]):
    start: Point
    stop: Point
    data: Data | None = None

@dataclass
class Node(Generic[Point, Data]):
    interval: Interval[Point, Data]
    balance: int = 0
    left: 'Node[Point, Data] | None' = None
    right: 'Node[Point, Data] | None' = None
    parent: 'Node[Point, Data] | None' = None

    @property
    def value(self) -> Point:
        return self.interval.stop

_T = TypeVar('_T')

def nonnull(value: _T | None) -> _T:
    assert(value is not None)
    return value

class IntervalTree(MutableSet[Interval[Point, Data]]):

    def __init__(self, values: Iterable[Interval[Point, Data]] | None = None) -> None:
        super().__init__()
        self.root: Node[Point, Data] | None = None
        self._count = 0
        if values is not None:
            for value in values:
                self.add(value)

    def _rotate_left(self, node: Node[Point, Data]) -> Node[Point, Data]:
        right = nonnull(node.right)
        if right.balance == 0:
            node.balance = +1
            right.balance = -1
        else:
            node.balance = 0
            right.balance = 0
        new_node = right
        if node == self.root:
            self.root = new_node
        else:
            parent = nonnull(node.parent)
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node
        new_node.parent = node.parent
        node.right = right.left
        if right.left is not None:
            right.left.parent = node
        right.left = node
        return right

    def _rotate_right(self, node: Node[Point, Data]) -> Node[Point, Data]:
        left = nonnull(node.left)
        if left.balance == 0:
            node.balance = -1
            left.balance = +1
        else:
            left.balance = 0
            node.balance = 0
        new_node = left
        if node == self.root:
            self.root = new_node
        else:
            parent = nonnull(node.parent)
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node
        new_node.parent = node.parent
        node.parent = left
        node.left = left.right
        if left.right is not None:
            left.right.parent = node
        left.right = node
        return left

    def _rotate_right_then_left(self, x: Node[Point, Data]) -> Node[Point, Data]:
        z = nonnull(x.right)
        y = nonnull(z.left)
        t2 = y.left
        t3 = y.right
        z.left = t3
        if t3 is not None:
            t3.parent = z
        y.right = z
        z.parent = y
        x.right = t2
        if t2 is not None:
            t2.parent = x
        if x == self.root:
            self.root = y
        else:
            parent = nonnull(x.parent)
            if x == parent.left:
                parent.left = y
            else:
                parent.right = y
        y.left = x
        y.parent = x.parent
        x.parent = y
        if y.balance == 0:
            x.balance = 0
            z.balance = 0
        elif y.balance > 0:
            x.balance = -1
            z.balance = 0
        else:
            x.balance = 0
            z.balance = +1
        y.balance = 0
        return y

    def _rotate_left_then_right(self, x: Node[Point, Data]) -> Node[Point, Data]:
        z = nonnull(x.left)
        y = nonnull(z.right)
        t2 = y.left
        t3 = y.right
        z.right = t2
        if t2 is not None:
            t2.parent = z
        y.left = z
        z.parent = y
        x.left = t3
        if t3 is not None:
            t3.parent = x
        if x == self.root:
            self.root = y
        else:
            parent = nonnull(x.parent)
            if x == parent.left:
                parent.left = y
            else:
                parent.right = y
        y.right = x
        y.parent = x.parent
        x.parent = y
        if y.balance == 0:
            x.balance = 0
            z.balance = 0
        elif y.balance < 0:
            x.balance = +1
            z.balance = 0
        else:
            x.balance = 0
            z.balance = -1
        y.balance = 0
        return y

    def get_add_hint(self, value: Interval[Point, Data]) -> Any:
        key = value.stop
        node = self.root
        while node is not None:
            if node.left is not None and key < node.value:
                node = node.left
            elif node.right is not None and key > node.value:
                node = node.right
            else:
                break
        return node

    def __iter__(self) -> Iterator[Interval[Point, Data]]:
        if self.root is None:
            return
        stack = [ self.root ]
        while stack:
            node = stack.pop()
            yield node.interval
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)

    def add(self, value: Interval[Point, Data], hint: Any = None) -> tuple[bool, Any]: # type: ignore
        parent = cast(Node[Point, Data], hint) if hint is not None else self.get_add_hint(value)
        if parent is None:
            self.root = Node(value)
            self._count += 1
            return True, self.root
        node = Node(value)
        if value.stop < parent.value:
            parent.left = node
        else:
            parent.right = node
        node.parent = parent
        self._count += 1
        return True, node

    def addi(self, start: Point, stop: Point, data: Data | None = None):
        self.add(Interval(start, stop, data))

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, Interval):
            return False
        key = value.stop
        node = self.root
        while node is not None:
            if node.value < key:
                node = node.left
            elif node.value > key:
                node = node.right
            else:
                break
        return node is not None and node.interval == value

    def __len__(self) -> int:
        return self._count

    def discard(self, value: Interval[Point, Data]) -> None:
        raise NotImplementedError()
