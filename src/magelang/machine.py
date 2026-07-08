from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from magelang.lang.treespec.ast import is_string_type
from magelang.helpers import get_fields
from magelang.lang.mage.ast import *
from magelang.util import DynamicNode, NameGenerator, todo

type Op = (
    Build
    | Call
    | Catch
    | Commit
    | Fail
    | Halt
    | Jump
    | Noop
    | Push
    | Ret
    | Sat
    | Seek
    | Tell
)

class OpBase:
    pass

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
class Sat(OpBase):
    """
    Check whether the character satisfies the given range.

    Advance the stream if the character matches, fail otherwise.
    """
    rng: tuple[str, str]
    add: bool
    """
    Whether to append the scanned character to the top of the stack.
    """
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
class Catch(OpBase):
    """
    Push a target label on the handler stack to handle failure.

    The machine will unwind the stack and jump to the given label on failure.
    """
    target: str | int
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

    def __str__(self) -> str:
        if self.label is None:
            return super().__str__()
        return f'{self.label}:'

@dataclass
class Machine:
    ops: list[Op]
    defs: dict[str, int]

    def dump(self) -> None:
        for op in self.ops:
            print(op)
        print('-------------')
        for name, offset in self.defs.items():
            print(f'def {name} = {offset}')

@dataclass
class Frame:
    op_index: int = 0
    stack: list[Any] = field(default_factory=list)
    # fields: dict[str, Any] = field(default_factory=dict)

class ParseError(RuntimeError):
    pass

def execute(m: Machine, text: str) -> Any:

    i = 0
    frames = list[Frame]()
    handlers = list[tuple[int, int]]()

    def fail():
        if not handlers:
            raise ParseError()
        i, target = handlers[-1]
        while len(frames) > i:
            frames.pop()
        handlers.pop()
        frames[-1].op_index = target

    frames.append(Frame())

    while True:

        frame = frames[-1]
        stack = frame.stack
        op = m.ops[frame.op_index]

        if isinstance(op, Sat):
            if i >= len(text):
                fail()
                continue
            ch = text[i]
            l, h = op.rng
            if l >= ch and h <= ch:
                print('accept', ch)
                i += 1
                if op.add:
                    stack[-1] += ch
            else:
                fail()
            frame.op_index += 1
        elif isinstance(op, Push):
            stack.append(op.value)
            frame.op_index += 1
        elif isinstance(op, Build):
            fields = dict[str, Any]()
            for name in reversed(op.field_names):
                fields[name] = stack.pop()
            stack.append(DynamicNode(op.name, fields))
            frame.op_index += 1
        elif isinstance(op, Halt):
            return stack[-1]
        elif isinstance(op, Fail):
            fail()
        elif isinstance(op, Commit):
            handlers.pop()
            frame.op_index += 1
        elif isinstance(op, Catch):
            assert(isinstance(op.target, int))
            handlers.append((len(frames), frame.op_index + op.target))
            frame.op_index += 1
        elif isinstance(op, Ret):
            value = stack[-1]
            frames.pop()
            if not frames: # FIXME remove me
                return value
            frames[-1].stack.append(value)
            frame.op_index += 1
        elif isinstance(op, Tell):
            stack.append(i)
            frame.op_index += 1
        elif isinstance(op, Seek):
            i = stack.pop()
            frame.op_index += 1
        elif isinstance(op, Jump):
            assert(isinstance(op.target, int))
            frame.op_index += op.target
        elif isinstance(op, Noop):
            frame.op_index += 1
        elif isinstance(op, Call):
            frames.append(Frame(m.defs[op.name]))
            # TODO what about the return value?
        else:
            assert_never(op)

    raise RuntimeError("end of instructions reached without return")


def link_machine(m: Machine) -> None:
    """
    Converts jumps to named labels of a machine to relative offsets.

    As a side-effect, this transformation removes Noop ops from the machine,
    since these were mainly used to store label offsets.
    """
    labels = dict[str, int]()
    i = 0
    while i < len(m.ops):
        op = m.ops[i]
        if op.label is not None:
            labels[op.label] = i
        if isinstance(op, Noop):
            del m.ops[i]
        else:
            i += 1
    for i, op in enumerate(m.ops):
        if isinstance(op, Jump) or isinstance(op, Catch):
            op.target = labels[cast(str, op.target)] - i


def mage_to_machine(grammar: MageGrammar) -> Machine:

    defs = {}
    ops = []

    generate_name = NameGenerator()

    def compile_expr(expr: MageExpr, hidden: bool = False) -> Iterable[Op]:
        if isinstance(expr, MageRefExpr):
            yield Call(expr.name)
            return
        if isinstance(expr, MageLitExpr):
            for ch in expr.text:
                yield Sat((ch, ch), False)
            return
        if isinstance(expr, MageCharSetExpr):
            for l, h in expr.elements:
                yield Sat((l, h), not hidden)
            return
        if isinstance(expr, MageChoiceExpr):
            names = list(generate_name(f'choice_{i}') for i in range(len(expr.elements)))
            for i, element in enumerate(expr.elements[:-1]):
                yield Catch(names[i+1], label=names[i])
                yield from compile_expr(element, hidden)
                yield Commit()
            yield from compile_expr(expr.elements[-1], hidden)
            return
        if isinstance(expr, MageLookaheadExpr):
            success_label = generate_name('look_success')
            yield Tell()
            if expr.is_negated:
                yield Catch(success_label)
                yield from compile_expr(expr.expr, True)
                yield Commit()
                yield Fail()
            else:
                yield from compile_expr(expr.expr, True)
            yield Seek(label=success_label)
            return
        if isinstance(expr, MageHideExpr):
            yield from compile_expr(expr.expr, hidden)
            return
        if isinstance(expr, MageSeqExpr):
            for element in expr.elements:
                yield from compile_expr(element, hidden)
            return
        if isinstance(expr, MageRepeatExpr):
            label_name = generate_name(prefix='repeat')
            done_label = generate_name(prefix='repeat_end')
            yield Catch(done_label)
            yield Noop(label=label_name)
            yield from compile_expr(expr.expr, hidden)
            yield Jump(label_name)
            yield Noop(label=done_label)
            return
        if isinstance(expr, MageListExpr):
            todo()
        assert_never(expr)

    for rule in grammar.rules:
        if rule.expr is not None:
            i = len(ops)
            field_names = list[str]()
            for expr, field in get_fields(rule.expr, grammar, include_hidden=True):
                if field is not None and is_string_type(field.ty):
                    # FIXME
                    ops.append(Push(''))
                ops.extend(compile_expr(expr, field is None))
                if field is not None:
                    field_names.append(field.name)
                    ops.append(Push(field.name, comment=f'field name'))
            ops.append(Build(rule.name, field_names))
            ops.append(Ret())
            defs[rule.name] = i

    return Machine(ops, defs)
