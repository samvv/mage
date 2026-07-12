
from collections.abc import Sequence, Iterable
from dataclasses import dataclass
from typing import assert_never

from magelang.graph import DGraph, toposort, graph_roots
from magelang.lang.mage.ast import POSINF
from magelang.machine import (
    FuncBuilder,
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
    Lt,
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
from magelang.util import NameGenerator, todo, nonnull, unreachable
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

EOF = '\uFFFF'

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
            g.add_edge(src, dst, None)
            return
        for_each_direct_child_expr(expr, lambda child: populate(g, child, src))

    def get_roots(rules: Sequence[MageRule]) -> Iterable[MageRule]:
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
                    unreachable()
        # TODO add the atoms, wich will be in another SCC
        # We require at least two Pratt expressions. When less, there is no
        # need at all for a Pratt parser.
        if len(candidates) > 0 and len(infix) + len(prefix) + len(suffix) >= 2:
            roots = list(get_roots(candidates))
            assert(len(roots) == 1)
            pratts.append(Pratt(nonnull(roots[0]).name, infix, prefix, suffix, atoms))
        else:
            rest.extend(scc)

    return rest, pratts

@declare_pass()
def mage_to_machine(grammar: MageGrammar) -> Machine:

    funcs = dict[str, FuncDef]()

    generate_label_name = NameGenerator()
    generate_function_name = NameGenerator(hide_first=True)

    elements, pratts = split_pratt(grammar)

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
            ops = list[Op]()
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
            funcs[rule.name] = FuncDef(0, ops)

    for pratt in pratts:

        parse_with_bp = generate_function_name(f'{pratt.name}_with_bp')
        parse_atom = generate_function_name(f'{pratt.name}_atom')
        parse_prefix = generate_function_name(f'{pratt.name}_prefix_operator')
        parse_postfix = generate_function_name(f'{pratt.name}_postfix_operator')
        parse_infix = generate_function_name(f'{pratt.name}_infix_operator')

        # Generate parse_expr_bp
        expr_bp = FuncBuilder(parse_with_bp)

        expr_bp.arg('min_prec')

        fail_parse_prefix = expr_bp.generate_label('fail_parse_prefix')
        fail_parse_postfix = expr_bp.generate_label('fail_parse_postfix')
        loop_start = expr_bp.generate_label('loop_start')
        loop_fail = expr_bp.generate_label('loop_fail')

        expr_bp.append(Catch(target=fail_parse_prefix))
        # parse_prefix will push a binding power on the stack if successful
        expr_bp.append(Call(name=parse_prefix))
        expr_bp.append(Commit())
        # parse_expr will be called with the precedence from parse_prefix_name
        expr_bp.append(Call(name=parse_with_bp))
        expr_bp.append(Jump(target=loop_start))

        # Alternative branch where parsing the prefix failed
        expr_bp.label(fail_parse_prefix)
        expr_bp.append(Call(name=parse_atom))

        # Start of the main loop
        expr_bp.label(loop_start)
        expr_bp.append(Tell())

        # Special case for EOF
        expr_bp.append(Catch(target=loop_fail))
        expr_bp.append(Sat((EOF, EOF)))
        expr_bp.append(Commit())

        # Attempt to parse a postfix expression
        expr_bp.append(Catch(target=fail_parse_postfix))
        expr_bp.append(Call(name=parse_postfix))
        expr_bp.append(Commit())
        expr_bp.append(Lt())
        expr_bp.append(JumpNZ(target=loop_fail))
        # TODO assign LHS as a combination of operator + expr
        expr_bp.append(Jump(target=loop_start))

        # Attempt to parse an infix expression
        expr_bp.label(fail_parse_postfix)
        expr_bp.append(Catch(target=loop_start))
        expr_bp.append(Call(name=parse_infix))
        expr_bp.append(Lt())
        expr_bp.append(JumpNZ(target=loop_fail))
        expr_bp.append(Call(name=parse_with_bp)) # should be called with r_bp from parse_infix
        # TODO assign LHS as a combination of expr + operator + expr
        expr_bp.append(Jump(target=loop_start))

        # We only get here if neither a prefix nor a postfix expression was parsed
        expr_bp.label(loop_fail)
        expr_bp.append(Seek())

        funcs[parse_with_bp] = expr_bp.finish()

        # Generate parse_prefix_operator
        prefix_ops = list[Op]()
        for rule in pratt.prefix:
            assert(isinstance(rule.expr, MageSeqExpr))
            failure = generate_label_name('failure')
            prefix_ops.append(Catch(target=failure))
            prefix_ops.extend(compile_expr(rule.expr.elements[0]))
            prefix_ops.append(Ret())
            prefix_ops.append(Noop(label=failure))
        prefix_ops.append(Push(None))
        prefix_ops.append(Ret())
        funcs[parse_prefix] = FuncDef(0, prefix_ops)

        # Generate parse_postfix_operator
        postfix_ops = list[Op]()
        for rule in pratt.prefix:
            assert(isinstance(rule.expr, MageSeqExpr))
            failure = generate_label_name('failure')
            postfix_ops.append(Catch(target=failure))
            postfix_ops.extend(compile_expr(rule.expr.elements[0]))
            postfix_ops.append(Ret())
            postfix_ops.append(Noop(label=failure))
        postfix_ops.append(Push(None))
        postfix_ops.append(Ret())
        funcs[parse_postfix] = FuncDef(0, postfix_ops)

        funcs[pratt.name] = FuncDef(0, [
            Push(0),
            Call(name=parse_with_bp),
            Ret(),
        ])

    return Machine(funcs)
