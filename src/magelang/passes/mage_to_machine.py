
from collections.abc import Sequence, Iterable
from dataclasses import dataclass
from typing import assert_never
from warnings import warn

from magelang.graph import DGraph, toposort, graph_roots
from magelang.lang.mage.ast import POSINF
from magelang.machine import (
    FuncDef,
    Machine,
    Op,
    Build,
    Call,
    Catch,
    Commit,
    Dec,
    Dup,
    Fail,
    Jump,
    JumpNZ,
    JumpZ,
    Noop,
    Pop,
    Push,
    Ret,
    Sat,
    Seek,
    Tell,
)
from magelang.helpers import get_fields
from magelang.manager import declare_pass
from magelang.util import NameGenerator, todo, nonnull
from magelang import (
    MageRule,
    MageGrammar,
    MageModuleElement,
    MageExpr,
    MageLitExpr,
    MageHideExpr,
    MageLookaheadExpr,
    MageRefExpr,
    MageChoiceExpr,
    MageCharSetExpr,
    MageRepeatExpr,
    MageListExpr,
    MageSeqExpr,
    for_each_direct_child_expr,
    lookup_ref
)

NONE   = 0
PREFIX = 1
INFIX  = 2
SUFFIX = 3

@dataclass
class Pratt:
    name: str
    infix: Sequence[MageRule]
    prefix: Sequence[MageRule]
    suffix: Sequence[MageRule]
    atoms: Sequence[MageRule]

def split_pratt(grammar: MageGrammar) -> tuple[list[MageModuleElement], list[Pratt]]:

    # TODO require that all rules are inlined
    # TODO require that all SeqExpr are normalized
    # TODO require that 1-ary ChoiceExpr are elminated
    # TODO find the root variant rule through some clever mechanism

    def populate(g: DGraph[MageRule, None], expr: MageExpr, src: MageRule) -> None:
        if isinstance(expr, MageRefExpr):
            dst = lookup_ref(expr)
            if dst is None:
                return
            print(src.name, '->', dst.name)
            g.add_edge(src, dst, None)
            return
        for_each_direct_child_expr(expr, lambda child: populate(g, child, src))

    def get_roots(rules: Sequence[MageRule]) -> Iterable[MageRule]:
        print('--------------')
        g = DGraph[MageRule, None]()
        for rule in rules:
            if rule.expr is not None:
                populate(g, rule.expr, rule)
        for root in graph_roots(g):
            if root in rules:
                yield root

    g = DGraph[MageRule, None]()

    for rule in grammar.rules:
        if rule.expr is not None:
            populate(g, rule.expr, rule)

    sccs = list(toposort(g))

    rest = []
    pratts = []

    for scc in sccs:
        if len(scc) == 1: # optimisation
            rest.append(next(iter(scc)))
            continue
        infix  = []
        prefix = []
        suffix = []
        atoms = []
        candidates = []
        for rule in scc:
            if isinstance(rule.expr, MageChoiceExpr):
                candidates.append(rule)
            elif isinstance(rule.expr, MageSeqExpr) and len(rule.expr.elements) > 1:
                has_left = False
                has_right = False
                if isinstance(rule.expr.elements[0], MageRefExpr):
                    left = lookup_ref(rule.expr.elements[0])
                    has_left = left in scc
                if isinstance(rule.expr.elements[-1], MageRefExpr):
                    right = lookup_ref(rule.expr.elements[-1])
                    has_right = right in scc
                if has_left and has_right:
                    infix.append(rule)
                elif has_left:
                    suffix.append(rule)
                elif has_right:
                    prefix.append(rule)
                else:
                    atoms.append(rule)
        # We require at least two Pratt expressions. When less, there is no
        # need at all for a Pratt parser.
        if len(candidates) > 0 and len(infix) + len(prefix) + len(suffix) >= 2:
            roots = list(get_roots(candidates))
            print(roots)
            assert(len(roots) == 1)
            pratts.append(Pratt(nonnull(roots[0]).name, infix, prefix, suffix, atoms))
        else:
            rest.extend(scc)

    return rest, pratts

@declare_pass()
def mage_to_machine(grammar: MageGrammar) -> Machine:

    funcs = dict[str, FuncDef]()
    ops = list[Op]()

    generate_label_name = NameGenerator()
    generate_function_name = NameGenerator()

    elements, pratts = split_pratt(grammar)

    print(pratts)

    def compile_repeat(count: int, expr: MageExpr, hidden: bool) -> Iterable[Op]:
        if count == 0:
            return
        repeat_label_name = generate_label_name(prefix='repeat_main')
        yield Push(count)
        yield Noop(label=repeat_label_name)
        yield from compile_expr(expr, hidden)
        yield Dec()
        yield Dup()
        yield JumpNZ(target=repeat_label_name)
        yield Pop()

    def compile_expr(expr: MageExpr, hidden: bool = False) -> Iterable[Op]:
        if isinstance(expr, MageRefExpr):
            yield Call(expr.name)
            return
        if isinstance(expr, MageLitExpr):
            for ch in expr.text:
                yield Sat((ch, ch))
            return
        if isinstance(expr, MageCharSetExpr):
            for rng in expr.elements:
                if isinstance(rng, str):
                    l = rng
                    h = rng
                else:
                    l, h = rng
                yield Sat((l, h))
            return
        if isinstance(expr, MageChoiceExpr):
            n = len(expr.elements)
            success_label_name = generate_label_name('choice_success')
            label_names = list(generate_label_name(f'choice_{i}') for i in range(n+1))
            for i, element in enumerate(expr.elements):
                yield Catch(target=label_names[i+1], label=label_names[i])
                yield from compile_expr(element, hidden)
                yield Jump(target=success_label_name)
            yield Fail(label=label_names[n])
            yield Commit(label=success_label_name)
            return
        if isinstance(expr, MageLookaheadExpr):
            success_label_name = generate_label_name('lookahead_success')
            yield Tell()
            if expr.is_negated:
                yield Catch(success_label_name)
                yield from compile_expr(expr.expr, True)
                yield Commit()
                yield Fail()
            else:
                # FIXME
                yield from compile_expr(expr.expr, True)
            yield Seek(label=success_label_name)
            return
        if isinstance(expr, MageHideExpr):
            yield from compile_expr(expr.expr, True)
            return
        if isinstance(expr, MageSeqExpr):
            for element in expr.elements:
                yield from compile_expr(element, hidden)
            return
        if isinstance(expr, MageRepeatExpr):
            if expr.min > 0:
                yield from compile_repeat(expr.min, expr.expr, hidden)
            if expr.max == POSINF:
                repeat_label_name = generate_label_name(prefix='repeat_inf')
                done_label_name = generate_label_name(prefix='repeat_end')
                yield Catch(target=done_label_name)
                yield Noop(label=repeat_label_name)
                yield from compile_expr(expr.expr, hidden)
                yield Jump(target=repeat_label_name)
                yield Noop(label=done_label_name)
            else:
                yield from compile_repeat(expr.max - expr.min, expr.expr, hidden)
            return
        if isinstance(expr, MageListExpr):
            todo()
        assert_never(expr)

    for rule in elements:
        assert(isinstance(rule, MageRule))
        if rule.expr is not None:
            i = len(ops)
            field_names = list[str]()
            for expr, field in get_fields(rule.expr, grammar, include_hidden=True):
                if field is not None:
                    ops.append(Tell())
                    ops.extend(compile_expr(expr, field is None))
                    ops.append(Tell())
                    field_names.append(field.name)
                else:
                    ops.extend(compile_expr(expr, True))
            ops.append(Build(rule.name, field_names))
            ops.append(Ret())
            funcs[rule.name] = FuncDef(i, 0)

    for pratt in pratts:
        parse_expr_name = generate_function_name('expr')
        parse_atom_name = generate_function_name('atom')
        parse_prefix_name = generate_function_name('prefix_operator')
        parse_postfix_name = generate_function_name('postfix_operator')
        parse_infix_name = generate_function_name('infix_operator')
        i = len(ops)
        # parse_expr_bp accepts min_prec as single argument
        funcs[pratt.name] = FuncDef(i, 1)
        after_prefix_label_name = generate_label_name('parsed_prefix')
        ops.append(Call(name=parse_prefix_name))
        ops.append(JumpNZ(target=after_prefix_label_name))
        ops.append(Call(name=parse_atom_name))
        # parse_expr will be called with the precedence from parse_atom
        ops.append(Call(name=parse_expr_name))

        # Generate parse_postfix_operator
        success_label_name = generate_label_name('prefix_success')
        for rule in pratt.prefix:
            assert(isinstance(rule.expr, MageSeqExpr))
            ops.extend(compile_expr(rule.expr.elements[0]))
            ops.append(JumpZ(target=success_label_name))
        ops.append(Ret(label=success_label_name))

    return Machine(ops, funcs)
