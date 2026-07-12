from collections.abc import Iterable, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from os import wait

from magelang.graph import DGraph, graph_roots, toposort
from magelang.helpers import get_fields
from magelang.lang.mage.ast import *
from magelang.util import DynamicNode, NameGenerator, to_snake_case, todo

type Op = (
    Build
    | Call
    | Catch
    | Commit
    | Dec
    | Dup
    | Fail
    | Halt
    | Inc
    | Jump
    | JumpNZ
    | JumpZ
    | Noop
    | Pop
    | Push
    | Ret
    | Sat
    | Seek
    | Tell
)

class OpBase:

    def __str__(self) -> str:
        out = to_snake_case(self.__class__.__name__)
        for name in typing.get_type_hints(self.__class__).keys():
            if name != 'comment' and name != 'label':
                out += f' {getattr(self, name)}'
        return out

@dataclass
class Ret(OpBase):
    """
    Return the topmost value on the stack to the calling function.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Halt(OpBase):
    """
    Stop the machine from running.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Fail(OpBase):
    """
    Immediately execute the next failure handler on the handler stack.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Build(OpBase):
    """
    Build a node from the fields that are on the stack.
    """
    name: str
    field_names: Sequence[str]
    label: str | None = None
    comment: str | None = None

@dataclass
class Push(OpBase):
    """
    Push an arbitrary value on the stack.
    """
    value: Any
    label: str | None = None
    comment: str | None = None

@dataclass
class Pop(OpBase):
    """
    Pop the topmost value from the stack.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Sat(OpBase):
    """
    Check whether the character satisfies the given range.

    Advance the stream if the character matches, fail otherwise.
    """
    rng: tuple[str, str]
    label: str | None = None
    comment: str | None = None

@dataclass
class Jump(OpBase):
    """
    Jump to a given named label or offset.
    """
    target: str | int
    label: str | None = None
    comment: str | None = None

@dataclass
class JumpZ(OpBase):
    """
    Jump to a given named label or offset if the top of the stack is zero-valued.
    """
    target: str | int
    label: str | None = None
    comment: str | None = None

@dataclass
class JumpNZ(OpBase):
    """
    Jump to a given named label or offset if the top of the stack is nonzero-valued.
    """
    target: str | int
    label: str | None = None
    comment: str | None = None

@dataclass
class Catch(OpBase):
    """
    Push a target label on the handler stack to handle failure.

    The machine will unwind the stack and jump to the given label on failure.
    """
    target: str | int
    label: str | None = None
    comment: str | None = None

@dataclass
class Dup(OpBase):
    """
    Duplicate the topmost value on the stack.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Commit(OpBase):
    """
    Commit choice by cleaning up the last handler.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Tell(OpBase):
    """
    Store the stream position so that it may be rewound.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Seek(OpBase):
    """
    Rewind the stream to the position saved by Tell().
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Call(OpBase):
    """
    Call another function defined in this machine.
    """
    name: str
    label: str | None = None
    comment: str | None = None

@dataclass
class Noop(OpBase):
    label: str | None = None
    comment: str | None = None

@dataclass
class Inc(OpBase):
    """
    Increment the top of the stack by 1.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Dec(OpBase):
    """
    Decrement the top of the stack by 1.
    """
    label: str | None = None
    comment: str | None = None

@dataclass
class Machine:
    ops: list[Op]
    defs: dict[str, int] = field(default_factory=dict)

    def dump(self) -> None:
        out = ''
        for i, op in enumerate(self.ops):
            if op.label is not None:
                out += f'[{i}] ' + op.label + ':\n'
            out += f'[{i}]    ' + str(op)
            if op.comment:
                out += ' # ' + op.comment
            out += '\n'
        for name, offset in self.defs.items():
            out += f'def {name} = {offset}\n'
        print(out)

    def clone(self) -> Machine:
        return Machine(
            deepcopy(self.ops),
            deepcopy(self.defs),
        )


@dataclass
class Frame:
    op_index: int = 0
    stack: list[Any] = field(default_factory=list)


class ParseError(RuntimeError):
    pass


class Executor:

    def __init__(self, start = 0, stack: list[Any] | None = None) -> None:
        if stack is None:
            stack = []
        self.offset = 0
        self.frames: list[Frame] = [ Frame(start, stack) ]
        self.handlers = list[tuple[int, int]]()

    @property
    def frame(self) -> Frame:
        return self.frames[-1]

    @property
    def stack(self) -> list[Any]:
        return self.frame.stack

    def fail(self):
        if not self.handlers:
            raise ParseError()
        frame_offset, target = self.handlers[-1]
        while len(self.frames) > frame_offset:
            self.frames.pop()
        self.handlers.pop()
        self.frames[-1].op_index = target

    def execute(self, m: Machine, text: str) -> None:

        while True:

            op = m.ops[self.frame.op_index]

            if isinstance(op, Sat):
                if self.offset >= len(text):
                    self.fail()
                    continue
                ch = text[self.offset]
                l, h = op.rng
                if l >= ch and h <= ch:
                    self.offset += 1
                    self.frame.op_index += 1
                else:
                    self.fail()
            elif isinstance(op, Push):
                self.stack.append(op.value)
                self.frame.op_index += 1
            elif isinstance(op, Pop):
                self.stack.pop()
                self.frame.op_index += 1
            elif isinstance(op, Build):
                fields = list[tuple[str, Any]]()
                for name in reversed(op.field_names):
                    high = self.stack.pop()
                    low = self.stack.pop()
                    fields.append((name, (low, high)))
                fields.reverse()
                self.stack.append(DynamicNode(op.name, fields))
                self.frame.op_index += 1
            elif isinstance(op, Halt):
                assert(not self.handlers)
                if self.offset < len(text):
                    raise ParseError()
                break
            elif isinstance(op, Fail):
                self.fail()
            elif isinstance(op, Commit):
                self.handlers.pop()
                self.frame.op_index += 1
            elif isinstance(op, Catch):
                assert(isinstance(op.target, int))
                self.handlers.append((len(self.frames), self.frame.op_index + op.target))
                self.frame.op_index += 1
            elif isinstance(op, Ret):
                value = self.stack[-1]
                self.frames.pop()
                self.stack.append(value)
                self.frame.op_index += 1
            elif isinstance(op, Tell):
                self.stack.append(self.offset)
                self.frame.op_index += 1
            elif isinstance(op, Seek):
                self.offset = self.stack.pop()
                self.frame.op_index += 1
            elif isinstance(op, Jump):
                assert(isinstance(op.target, int))
                self.frame.op_index += op.target
            elif isinstance(op, JumpZ):
                assert(isinstance(op.target, int))
                if self.stack.pop() == 0:
                    self.frame.op_index += op.target
                else:
                    self.frame.op_index += 1
            elif isinstance(op, JumpNZ):
                assert(isinstance(op.target, int))
                if self.stack.pop() != 0:
                    self.frame.op_index += op.target
                else:
                    self.frame.op_index += 1
            elif isinstance(op, Noop):
                self.frame.op_index += 1
            elif isinstance(op, Inc):
                self.stack[-1] += 1
                self.frame.op_index += 1
            elif isinstance(op, Dec):
                self.stack[-1] -= 1
                self.frame.op_index += 1
            elif isinstance(op, Call):
                self.frames.append(Frame(m.defs[op.name]))
                # TODO what about the return value?
            elif isinstance(op, Dup):
                self.stack.append(self.stack[-1])
                self.frame.op_index += 1
            else:
                assert_never(op)


def execute_machine(m: Machine, text: str, start = 0, stack = None) -> None:
    e = Executor(start, stack)
    e.execute(m, text)


def call_machine_method(m: Machine, name: str, text: str) -> Any:
    m = m.clone()
    start = len(m.ops)
    m.ops.append(Call(name))
    m.ops.append(Halt())
    stack = []
    execute_machine(m, text, start=start, stack=stack)
    assert(len(stack) == 1)
    return stack[-1]


def link_machine(m: Machine) -> None:
    """
    Converts jumps to named labels of a machine to relative offsets.
    """
    labels = dict[str, int]()
    i = 0
    for i, op in enumerate(m.ops):
        if op.label is not None:
            labels[op.label] = i
        else:
            i += 1
    for i, op in enumerate(m.ops):
        if isinstance(op, Jump) or isinstance(op, JumpZ) or isinstance(op, JumpNZ) or isinstance(op, Catch):
            op.target = labels[cast(str, op.target)] - i

