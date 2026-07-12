from collections.abc import Sequence
from dataclasses import dataclass, field

from magelang.lang.mage.ast import *
from magelang.runtime.diagnostics import count_digits
from magelang.util import DynamicNode, NameGenerator, to_snake_case

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
    | Lt
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

    The topmost value on the stack will be consumed.
    """
    target: str | int
    label: str | None = None
    comment: str | None = None

@dataclass
class JumpNZ(OpBase):
    """
    Jump to a given named label or offset if the top of the stack is nonzero-valued.

    The topmost value on the stack will be consumed.
    """
    target: str | int
    label: str | None = None
    comment: str | None = None

@dataclass
class Lt(OpBase):
    """
    Determine if the first value on the stack is less than the second value.

    The first and second values on the stack will be consumed.

    When true, add 1 to the stack. When false, append 0.
    """
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
    """
    Do not perform anything.

    The program counter will simply be incremented to the next instruction.

    This instruction is useful for adding comments and labels.
    """
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
class FuncDef:
    arity: int
    ops: Sequence[Op]

@dataclass
class Machine:
    funcs: dict[str, FuncDef] = field(default_factory=dict)

    def dump(self) -> None:
        out = ''
        n = 0
        for func in self.funcs.values():
            n = max(n, count_digits(len(func.ops)))
        for name, func in self.funcs.items():
            out += f'def {name}:\n'
            for i, op in enumerate(func.ops):
                spacing = ' ' * (n - count_digits(i))
                if op.label is not None:
                    out += f'[{i}{spacing}] ' + op.label + ':\n'
                out += f'[{i}{spacing}]    ' + str(op)
                if op.comment:
                    out += ' # ' + op.comment
                out += '\n'
        print(out)


@dataclass
class Frame:
    func: FuncDef
    op_index: int = 0
    stack: list[Any] = field(default_factory=list)


class ParseError(RuntimeError):
    pass


class Execution:

    def __init__(
        self,
        machine: Machine,
        text: str,
        entrypoint: str = 'main',
        start_offset = 0,
        stack: list[Any] | None = None
    ) -> None:
        if stack is None:
            stack = []
        self.m = machine
        self.text = text
        self.offset = 0
        self.frames: list[Frame] = [ Frame(machine.funcs[entrypoint], start_offset, stack) ]
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

    def _check_post(self) -> None:
        assert(not self.handlers)
        if self.offset < len(self.text):
            raise ParseError()

    def execute(self) -> None:

        while True:

            op = self.frame.func.ops[self.frame.op_index]

            if isinstance(op, Sat):
                if self.offset >= len(self.text):
                    self.fail()
                    continue
                ch = self.text[self.offset]
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
                self._check_post()
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
                if not self.frames:
                    self._check_post()
                    break
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
                func = self.m.funcs[op.name]
                new_stack = list[Any]()
                for _ in range(func.arity):
                    new_stack.append(self.stack.pop())
                self.frames.append(Frame(func))
                # op_index is incremented when returning
            elif isinstance(op, Dup):
                self.stack.append(self.stack[-1])
                self.frame.op_index += 1
            elif isinstance(op, Lt):
                left = self.stack.pop()
                right = self.stack.pop()
                self.stack.append(left < right)
                self.frame.op_index += 1
            else:
                assert_never(op)


def execute_machine(
    machine: Machine,
    text: str,
    entrypoint = 'main',
    start = 0,
    stack: list[Any] | None = None
) -> None:
    e = Execution(machine, text, entrypoint, start, stack)
    e.execute()


def call_machine_function(m: Machine, name: str, text: str) -> Any:
    stack = []
    execute_machine(m, text, entrypoint=name, stack=stack)
    assert(len(stack) == 1)
    return stack[-1]


def link_machine(m: Machine) -> None:
    """
    Converts jumps to named labels of a machine to relative offsets.
    """
    labels = dict[str, int]()
    for func in m.funcs.values():
        i = 0
        for i, op in enumerate(func.ops):
            if op.label is not None:
                labels[op.label] = i
            else:
                i += 1
        for i, op in enumerate(func.ops):
            if isinstance(op, Jump) or isinstance(op, JumpZ) or isinstance(op, JumpNZ) or isinstance(op, Catch):
                op.target = labels[cast(str, op.target)] - i


class FuncBuilder:

    def __init__(self, name: str) -> None:
        self.name = name
        self.args = list[str]()
        self.ops = list[Op]()
        self._pending_labels = list[str]()
        self._label_generator = NameGenerator(hide_first=True)

    def arg(self, name: str) -> None:
        assert(name not in self.args)
        self.args.append(name)

    def generate_label(self, name: str) -> str:
        return self._label_generator(name)

    def label(self, name: str) -> None:
        self._pending_labels.append(name)

    def append(self, op: Op) -> None:
        for name in self._pending_labels:
            if op.label is None:
                op.label = name
            else:
                self.ops.append(Noop(label=name))
            self._pending_labels.clear()
        self.ops.append(op)

    def finish(self) -> FuncDef:
        assert(not self._pending_labels)
        return FuncDef(len(self.args), self.ops)
