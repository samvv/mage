
from collections.abc import Sequence, Iterable
from dataclasses import dataclass, field
from typing import assert_never

from magelang.graph import DGraph, graph_reachable, toposort, graph_roots
from magelang.lang.mage.ast import ASSOC_LEFT, ASSOC_RIGHT, MAGE_REPEAT_INFINITY
from magelang.machine import (
    BuildToken,
    Dump,
    Flip,
    Load,
    Machine,
    MachineBuilder,
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
    infix: list[MageRule]
    prefix: list[MageRule]
    suffix: list[MageRule]
    atoms: list[MageRule] = field(default_factory=list)

    def all(self) -> Iterable[MageRule]:
        yield from self.infix
        yield from self.prefix
        yield from self.suffix

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

    rest   = list[MageModuleElement]()
    pratts = list[Pratt]()

    for scc in sccs:
        if len(scc) == 1: # optimisation
            rest.append(next(iter(scc)))
            continue
        infix      = list[MageRule]()
        prefix     = list[MageRule]()
        suffix     = list[MageRule]()
        candidates = list[MageRule]()
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
        # We require at least two Pratt expressions. When less, there is no
        # need at all for a Pratt parser.
        if len(candidates) > 0 and len(infix) + len(prefix) + len(suffix) >= 2:
            roots = list(get_roots(candidates))
            assert(len(roots) == 1)
            pratts.append(Pratt(nonnull(roots[0]).name, infix, prefix, suffix))
        else:
            rest.extend(scc)

    for rule in rest:
        if isinstance(rule, MageRule) and rule.is_parse:
            for pratt in pratts:
                for pratt_rule in pratt.all():
                    if graph_reachable(g, pratt_rule, rule):
                        pratt.atoms.append(rule)
                        break

    return rest, pratts


@declare_pass()
def mage_to_machine(grammar: MageGrammar) -> Machine:

    builder = MachineBuilder()

    generate_label_name = NameGenerator()
    generate_function_name = NameGenerator(hide_first=True)

    elements, pratts = split_pratt(grammar)

    def compile_repeat(count: int, expr: MageExpr, hidden: bool, in_token: bool) -> Iterable[Op]:
        if count == 0:
            return
        repeat_label_name = generate_label_name(prefix='repeat_main')
        yield Push(count)
        yield Noop(label=repeat_label_name)
        yield from compile_expr(expr, hidden, in_token)
        yield Dec()
        yield Dup()
        yield JumpNZ(target=repeat_label_name)
        yield Pop()

    def compile_expr(expr: MageExpr, hidden: bool = False, in_token: bool = False) -> Iterable[Op]:
        if isinstance(expr, MageRefExpr):
            yield Call(expr.name)
            return
        if isinstance(expr, MageLitExpr):
            for ch in expr.text:
                yield Sat((ch, ch))
            return
        if isinstance(expr, MageCharSetExpr):
            success = generate_label_name('charset_success')
            for rng in expr.elements:
                if isinstance(rng, str):
                    l = rng
                    h = rng
                else:
                    l, h = rng
                next = generate_label_name('charset_next')
                yield Catch(target=next)
                yield Sat((l, h))
                yield Jump(target=success)
                yield Noop(label=next)
            yield Fail(f"doesn't satisfy {' | '.join(repr(el) for el in expr.elements)}")
            yield Commit(label=success)
            return
        if isinstance(expr, MageChoiceExpr):
            n = len(expr.elements)
            success_label_name = generate_label_name('choice_success')
            label_names = list(generate_label_name(f'choice_{i}') for i in range(n+1))
            for i, element in enumerate(expr.elements):
                yield Catch(target=label_names[i+1], label=label_names[i])
                yield from compile_expr(element, hidden, in_token)
                yield Jump(target=success_label_name)
            yield Fail(label=label_names[n])
            yield Commit(label=success_label_name)
            return
        if isinstance(expr, MageLookaheadExpr):
            success_label_name = generate_label_name('lookahead_success')
            yield Tell()
            if expr.is_negated:
                yield Catch(success_label_name)
                yield from compile_expr(expr.expr, True, in_token)
                yield Commit()
                yield Fail()
            else:
                # FIXME
                yield from compile_expr(expr.expr, True, in_token)
            yield Seek(label=success_label_name)
            return
        if isinstance(expr, MageHideExpr):
            yield from compile_expr(expr.expr, True, in_token)
            return
        if isinstance(expr, MageSeqExpr):
            for element in expr.elements:
                yield from compile_expr(element, hidden, in_token)
            return
        if isinstance(expr, MageRepeatExpr):
            if expr.min > 0:
                yield from compile_repeat(expr.min, expr.expr, hidden, in_token)
            if expr.max == MAGE_REPEAT_INFINITY:
                repeat_label_name = generate_label_name(prefix='repeat_inf')
                done_label_name = generate_label_name(prefix='repeat_end')
                yield Catch(target=done_label_name)
                yield Noop(label=repeat_label_name)
                yield from compile_expr(expr.expr, hidden, in_token)
                yield Jump(target=repeat_label_name)
                yield Noop(label=done_label_name)
            else:
                yield from compile_repeat(expr.max - expr.min, expr.expr, hidden, in_token)
            return
        if isinstance(expr, MageListExpr):
            todo()
        assert_never(expr)

    for rule in elements:
        if not isinstance(rule, MageRule) or rule.expr is None:
            continue
        func = builder.func(rule.name)
        func.retval('node_or_token')
        field_names = list[str]()
        if rule.is_lex:
            func.append(Tell())
            func.extend(compile_expr(rule.expr, in_token=True))
            func.append(Tell())
            func.append(BuildToken(rule.name))
        else:
            for expr, field in get_fields(rule.expr, grammar, include_hidden=True):
                if field is not None:
                    func.extend(compile_expr(expr, False))
                    field_names.append(field.name)
                else:
                    func.extend(compile_expr(expr, True))
            func.append(Build(rule.name, field_names))
        func.append(Ret())
        func.finish()

    for pratt in pratts:

        parse_with_bp_name = generate_function_name(f'{pratt.name}_with_bp')
        parse_atom_name = generate_function_name(f'{pratt.name}_atom')
        parse_prefix_name = generate_function_name(f'{pratt.name}_prefix_operator')
        parse_postfix_name = generate_function_name(f'{pratt.name}_postfix_operator')
        parse_infix_name = generate_function_name(f'{pratt.name}_infix_operator')

        # Generate parse_expr_bp
        expr_bp = builder.func(parse_with_bp_name)

        expr_bp.arg('min_prec')
        expr_bp.retval('node')

        fail_parse_prefix = expr_bp.generate_label('fail_parse_prefix')
        loop_start = expr_bp.generate_label('loop_start')
        start_parse_postfix = expr_bp.generate_label('start_parse_postfix')
        start_parse_infix = expr_bp.generate_label('start_parse_infix')
        loop_end = expr_bp.generate_label('loop_end')

        expr_bp.append(Catch(target=fail_parse_prefix))
        # parse_prefix will push a binding power on the stack if successful
        expr_bp.append(Call(name=parse_prefix_name))
        expr_bp.append(Commit())
        # parse_expr will be called with the precedence from parse_prefix_name
        expr_bp.append(Call(name=parse_with_bp_name))
        expr_bp.append(Jump(target=loop_start))

        # Alternative branch where parsing the prefix failed
        expr_bp.label(fail_parse_prefix)
        expr_bp.append(Call(name=parse_atom_name))

        # Start of the main loop
        expr_bp.label(loop_start)
        expr_bp.append(Tell())

        # Special case for EOF
        expr_bp.append(Catch(target=start_parse_postfix))
        expr_bp.append(Sat((EOF, EOF)))
        expr_bp.append(Commit())
        expr_bp.append(Jump(target=loop_end))

        # Attempt to parse a postfix expression
        expr_bp.label(start_parse_postfix)
        expr_bp.append(Catch(target=start_parse_infix))
        expr_bp.append(Call(name=parse_postfix_name))
        expr_bp.append(Commit())
        expr_bp.append(Dup()) # copy the parse_postfix result
        expr_bp.append(Load(3)) # load min_prec
        expr_bp.append(Flip()) # prepare for Lt
        expr_bp.append(Lt())
        expr_bp.append(Dump())
        expr_bp.append(JumpNZ(target=loop_end))
        # TODO assign LHS as a combination of operator + expr
        expr_bp.append(Jump(target=loop_start))

        # Attempt to parse an infix expression
        expr_bp.label(start_parse_infix)
        expr_bp.append(Dump())
        expr_bp.append(Catch(target=loop_end))
        expr_bp.append(Call(name=parse_infix_name))
        expr_bp.append(Commit())
        expr_bp.append(Load(3)) # load min_prec
        expr_bp.append(Dup()) # copy the parse_infix precedence result
        expr_bp.append(Flip()) # prepare for Lt
        expr_bp.append(Lt())
        expr_bp.append(JumpNZ(target=loop_end))
        expr_bp.append(Call(name=parse_with_bp_name)) # should be called with r_bp from parse_infix
        # TODO assign LHS as a combination of expr + operator + expr
        expr_bp.append(Load(2)) # load lhs
        expr_bp.append(Flip())
        expr_bp.append(Build(pratt.name, ['lhs', 'rhs']))
        expr_bp.append(Jump(target=loop_start))

        # We only get here if neither a prefix nor a postfix expression was parsed
        expr_bp.label(loop_end)
        # expr_bp.append(Flip())
        expr_bp.append(Seek())
        expr_bp.append(Ret())

        expr_bp.finish()

        # Generate parse_atom
        atom = builder.func(parse_atom_name)
        atom.retval('node')
        atom.extend(compile_expr(MageChoiceExpr(list(MageRefExpr(rule.name) for rule in pratt.atoms))))
        atom.append(Ret())
        atom.finish()

        # Generate parse_prefix_operator
        prefix = builder.func(parse_prefix_name)
        prefix.retval('precedence')
        for rule in pratt.prefix:
            assert(isinstance(rule.expr, MageSeqExpr))
            assert(len(rule.expr.elements) == 2)
            next_op = prefix.generate_label('failure')
            op = rule.expr.elements[0]
            prefix.append(Catch(target=next_op))
            prefix.extend(compile_expr(op))
            prefix.append(Commit())
            prefix.append(Push(nonnull(op.precedence)[0]))
            prefix.append(Ret())
            prefix.label(next_op)
        prefix.append(Fail('expected a prefix operator'))
        prefix.finish()

        # Generate parse_postfix_operator
        postfix = builder.func(parse_postfix_name)
        postfix.retval('precedence')
        for rule in pratt.suffix:
            assert(isinstance(rule.expr, MageSeqExpr))
            assert(len(rule.expr.elements) == 2)
            next_op = generate_label_name('failure')
            op = rule.expr.elements[1]
            postfix.append(Catch(target=next_op))
            postfix.extend(compile_expr(op))
            postfix.append(Commit())
            postfix.append(Push(nonnull(op.precedence)[0]))
            postfix.append(Ret())
            postfix.label(next_op)
        postfix.append(Fail('expected a postfix operator'))
        postfix.finish()

        # Generate parse_infix_operator
        infix = builder.func(parse_infix_name)
        infix.retval('precedence')
        for rule in pratt.infix:
            assert(isinstance(rule.expr, MageSeqExpr))
            assert(len(rule.expr.elements) == 3)
            next_op = generate_label_name('failure')
            infix.append(Catch(target=next_op))
            op = rule.expr.elements[1]
            infix.extend(compile_expr(op))
            infix.append(Commit())
            prec, assoc = nonnull(op.precedence)
            infix.append(Push(prec if assoc == ASSOC_LEFT else prec+1))
            infix.append(Push(prec))
            infix.append(Ret())
            infix.label(next_op)
        infix.append(Fail('expected an infix operator'))
        infix.finish()

        main = builder.func(pratt.name)
        main.retval('node')
        main.append(Push(0))
        main.append(Call(name=parse_with_bp_name))
        main.append(Ret())
        main.finish()

    return builder.finish()
