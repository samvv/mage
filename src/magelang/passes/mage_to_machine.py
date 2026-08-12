
from collections.abc import Sequence, Iterable
from dataclasses import dataclass, field
from typing import assert_never

from magelang.graph import DGraph, graph_reachable, toposort, graph_roots
from magelang.lang.mage.ast import ASSOC_RIGHT, MAGE_REPEAT_INFINITY
from magelang.lang.treespec.helpers import is_unit_type
from magelang.machine import (
    BuildToken,
    BuildTuple,
    Dump,
    Flip,
    FuncBuilder,
    Get,
    Machine,
    MachineBuilder,
    Build,
    Call,
    Catch,
    Commit,
    Dec,
    Dup,
    Fail,
    Jump,
    JumpNZ,
    Lt,
    Pop,
    Push,
    Ret,
    Sat,
    Seek,
    Set,
    Tell,
)
from magelang.helpers import get_fields, infer_type, lit_to_name, split_pratt
from magelang.manager import declare_pass
from magelang.util import NameGenerator, nonnull, unreachable
from magelang import (
    MageRule,
    MageGrammar,
    MageGrammarElement,
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

@declare_pass()
def mage_to_machine(grammar: MageGrammar) -> Machine:

    builder = MachineBuilder()

    generate_label_name = NameGenerator(hide_first=False)
    generate_function_name = NameGenerator(hide_first=True)

    elements, pratts = split_pratt(grammar)

    def compile_repeat(builder: FuncBuilder, count: int, expr: MageExpr, hidden: bool, in_token: bool, generate_token_name) -> None:
        if count == 0:
            return
        repeat_label_name = generate_label_name(prefix='repeat_main')
        builder.append(Push(count))
        builder.label(repeat_label_name)
        compile_expr(builder, expr, hidden, in_token, generate_token_name)
        builder.append(Dec())
        builder.append(Dup())
        builder.append(JumpNZ(target=repeat_label_name))
        builder.append(Pop())

    def compile_expr(builder: FuncBuilder, expr: MageExpr, hidden: bool = False, in_token: bool = False, generate_token_name: NameGenerator | None = None) -> None:

        if generate_token_name is None:
            generate_token_name = NameGenerator()

        if isinstance(expr, MageRefExpr):
            builder.append(Call(expr.name))
            return

        if isinstance(expr, MageLitExpr):
            if not hidden:
                builder.append(Tell())
            for ch in expr.text:
                builder.append(Sat((ch, ch)))
            if not hidden:
                builder.append(Tell())
                name = expr.label
                if name is None:
                    _is_keyword, name = lit_to_name(expr.text, grammar=grammar)
                builder.append(BuildToken(name))
            return

        if isinstance(expr, MageCharSetExpr):
            if not hidden:
                builder.append(Tell())
            success = generate_label_name('charset_success')
            for rng in expr.elements:
                if isinstance(rng, str):
                    l = rng
                    h = rng
                else:
                    l, h = rng
                next = generate_label_name('charset_next')
                builder.append(Catch(target=next))
                builder.append(Sat((l, h)))
                builder.append(Jump(target=success))
                builder.label(next)
            builder.append(Fail(f"doesn't satisfy {expr.label or ' | '.join(repr(el) for el in expr.elements)}"))
            builder.label(success)
            builder.append(Commit())
            if not hidden:
                builder.append(Tell())
                builder.append(BuildToken(expr.label or generate_token_name()))
            return

        if isinstance(expr, MageChoiceExpr):
            n = len(expr.elements)
            success_label_name = generate_label_name('choice_success')
            label_names = list(generate_label_name(f'choice_{i}') for i in range(n+1))
            for i, element in enumerate(expr.elements):
                builder.label(label_names[i])
                builder.append(Catch(target=label_names[i+1]))
                compile_expr(builder, element, hidden, in_token, generate_token_name)
                builder.append(Jump(target=success_label_name))
            builder.label(label_names[n])
            builder.append(Fail())
            builder.label(success_label_name)
            builder.append(Commit())
            return

        if isinstance(expr, MageLookaheadExpr):
            failure_label_name = generate_label_name('lookahead_failed')
            finish_label_name = generate_label_name('lookahead_end')
            if expr.is_negated:
                builder.append(Tell())
                builder.append(Catch(target=failure_label_name))
                compile_expr(builder, expr.expr, True, in_token, generate_token_name)
                builder.append(Commit())
                builder.append(Seek())
                builder.append(Fail())
                builder.label(failure_label_name)
                builder.append(Seek())
            else:
                builder.append(Tell())
                builder.append(Catch(target=failure_label_name))
                compile_expr(builder, expr.expr, True, in_token, generate_token_name)
                builder.append(Commit())
                builder.append(Seek())
                builder.append(Jump(target=finish_label_name))
                builder.label(failure_label_name)
                builder.append(Seek())
                builder.append(Fail())
                builder.label(finish_label_name)
            return

        if isinstance(expr, MageHideExpr):
            compile_expr(builder, expr.expr, True, in_token, generate_token_name)
            return

        if isinstance(expr, MageSeqExpr):
            ty = infer_type(expr, grammar=grammar)
            for el in expr.elements:
                compile_expr(builder, el, hidden, in_token, generate_token_name)
            if not hidden and not is_unit_type(ty):
                builder.append(BuildTuple(sum(0 if is_unit_type(infer_type(child, grammar=grammar)) else 1 for child in expr.elements)))
            return

        if isinstance(expr, MageRepeatExpr):
            if expr.min > 0:
                compile_repeat(builder, expr.min, expr.expr, hidden, in_token, generate_token_name)
            if expr.max == MAGE_REPEAT_INFINITY:
                repeat_label_name = generate_label_name(prefix='repeat_inf')
                done_label_name = generate_label_name(prefix='repeat_end')
                builder.append(Catch(target=done_label_name))
                builder.label(repeat_label_name)
                compile_expr(builder, expr.expr, hidden, in_token, generate_token_name)
                builder.append(Jump(target=repeat_label_name))
                builder.label(done_label_name)
            else:
                compile_repeat(builder, expr.max - expr.min, expr.expr, hidden, in_token, generate_token_name)
            return

        if isinstance(expr, MageListExpr):
            first_fail = generate_label_name('list_first_fail')
            finish_label_name = generate_label_name('finish')
            min_loop_start = generate_label_name('min_loop_start')
            loop_start = generate_label_name('loop_start')
            builder.append(Catch(target=first_fail))
            compile_expr(builder, expr.element, hidden, in_token, generate_token_name)
            builder.append(Commit())
            if expr.min_count > 0:
                builder.append(Push(expr.min_count))
                builder.append(Set('i'))
                builder.label(min_loop_start)
                builder.append(Catch(target=finish_label_name))
                compile_expr(builder, expr.separator, hidden, in_token, generate_token_name)
                builder.append(Commit())
                compile_expr(builder, expr.element, hidden, in_token, generate_token_name)
                builder.append(Get('i'))
                builder.append(Dec())
                builder.append(JumpNZ(target=min_loop_start))
            builder.label(loop_start)
            builder.append(Catch(target=finish_label_name))
            compile_expr(builder, expr.separator, hidden, in_token, generate_token_name)
            builder.append(Commit())
            compile_expr(builder, expr.element, hidden, in_token, generate_token_name)
            builder.append(Jump(target=loop_start))
            builder.label(first_fail)
            if expr.min_count > 0:
                builder.append(Fail())
            builder.label(finish_label_name)
            return

        assert_never(expr)

    for rule in elements:
        if not isinstance(rule, MageRule) or rule.expr is None:
            continue
        generate_field = NameGenerator('field', hide_first=False)
        func = builder.func(rule.name)
        func.retval('node_or_token')
        field_names = list[str]()
        if rule.is_lex:
            func.append(Tell())
            compile_expr(func, rule.expr, in_token=True, generate_token_name=generate_field)
            func.append(Tell())
            func.append(BuildToken(rule.name))
        else:
            for expr, field in get_fields(rule.expr, grammar, include_hidden=True):
                if field is not None:
                    compile_expr(func, expr, False, generate_token_name=generate_field)
                    field_names.append(field.name)
                else:
                    compile_expr(func, expr, True, generate_token_name=generate_field)
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

        expr_bp.append(Set('min_prec')) # store the first argument in a local

        expr_bp.append(Catch(target=fail_parse_prefix))
        # parse_prefix will push a binding power on the stack if successful
        expr_bp.append(Call(name=parse_prefix_name))
        expr_bp.append(Commit())
        # parse_expr will be called with the precedence from parse_prefix_name
        expr_bp.append(Call(name=parse_with_bp_name))
        expr_bp.append(Build(f'{pratt.name}_prefix', ['expr']))
        expr_bp.append(Set('lhs'))
        expr_bp.append(Jump(target=loop_start))

        # Alternative branch where parsing the prefix failed
        expr_bp.label(fail_parse_prefix)
        expr_bp.append(Call(name=parse_atom_name))
        expr_bp.append(Set('lhs'))

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
        expr_bp.append(Call(name=parse_postfix_name)) # returns kind, l_bp in that order
        expr_bp.append(Commit())
        expr_bp.append(Flip())
        expr_bp.append(Set('kind'))
        expr_bp.append(Get('min_prec')) # load min_prec
        expr_bp.append(Flip()) # we don't have Gt
        expr_bp.append(Dump())
        expr_bp.append(Lt()) # l_bp < min_prec
        expr_bp.append(JumpNZ(target=loop_end))
        expr_bp.append(Get('lhs'))
        expr_bp.append(Build(f'{pratt.name}_postfix', ['expr']))
        expr_bp.append(Set('lhs'))
        expr_bp.append(Jump(target=loop_start))

        # Attempt to parse an infix expression
        expr_bp.label(start_parse_infix)
        expr_bp.append(Catch(target=loop_end))
        expr_bp.append(Call(name=parse_infix_name)) # returns kind, l_bp, r_bp in that order
        expr_bp.append(Commit())
        expr_bp.append(Set('r_bp'))
        expr_bp.append(Flip())
        expr_bp.append(Set('kind'))
        expr_bp.append(Get('min_prec'))
        expr_bp.append(Flip()) # we don't have Gt
        expr_bp.append(Lt()) # l_bp < min_prec
        expr_bp.append(JumpNZ(target=loop_end))
        expr_bp.append(Get('r_bp'))
        expr_bp.append(Call(name=parse_with_bp_name)) # should be called with r_bp from parse_infix
        expr_bp.append(Get('lhs'))
        # expr_bp.append(Flip())
        expr_bp.append(Build(f'{pratt.name}_infix', ['lhs', 'rhs']))
        expr_bp.append(Set('lhs'))
        expr_bp.append(Jump(target=loop_start))

        # We only get here if neither an infix nor a postfix expression was parsed
        expr_bp.label(loop_end)
        expr_bp.append(Seek())
        expr_bp.append(Get('lhs'))
        expr_bp.append(Ret())

        expr_bp.finish()

        # Generate parse_atom
        atom = builder.func(parse_atom_name)
        atom.retval('node')
        compile_expr(atom, MageChoiceExpr(list(MageRefExpr(rule.name) for rule in pratt.atoms)))
        atom.append(Ret())
        atom.finish()

        # Generate parse_prefix_operator
        prefix = builder.func(parse_prefix_name)
        prefix.retval('op')
        prefix.retval('precedence')
        prefix.retval('kind')
        for rule in pratt.prefix:
            assert(isinstance(rule.expr, MageSeqExpr))
            assert(len(rule.expr.elements) == 2)
            next_op = prefix.generate_label('failure')
            op = rule.expr.elements[0]
            prefix.append(Catch(target=next_op))
            compile_expr(prefix, op)
            prefix.append(Commit())
            prefix.append(Push(nonnull(op.precedence)[0]))
            prefix.append(Push(rule.name))
            prefix.append(Ret())
            prefix.label(next_op)
        prefix.append(Fail('expected a prefix operator'))
        prefix.finish()

        # Generate parse_postfix_operator
        postfix = builder.func(parse_postfix_name)
        prefix.retval('op')
        postfix.retval('precedence')
        postfix.retval('kind')
        for rule in pratt.suffix:
            assert(isinstance(rule.expr, MageSeqExpr))
            assert(len(rule.expr.elements) == 2)
            next_op = generate_label_name('failure')
            op = rule.expr.elements[1]
            postfix.append(Catch(target=next_op))
            compile_expr(postfix, op)
            postfix.append(Commit())
            postfix.append(Push(nonnull(op.precedence)[0]))
            postfix.append(Push(rule.name))
            postfix.append(Ret())
            postfix.label(next_op)
        postfix.append(Fail('expected a postfix operator'))
        postfix.finish()

        # Generate parse_infix_operator
        infix = builder.func(parse_infix_name)
        infix.retval('op')
        infix.retval('r_bp')
        infix.retval('l_bp')
        infix.retval('kind')
        for rule in pratt.infix:
            assert(isinstance(rule.expr, MageSeqExpr))
            assert(len(rule.expr.elements) == 3)
            next_op = generate_label_name('failure')
            infix.append(Catch(target=next_op))
            op = rule.expr.elements[1]
            compile_expr(infix, op)
            infix.append(Commit())
            prec, assoc = nonnull(op.precedence)
            infix.append(Push(prec+1 if assoc == ASSOC_RIGHT else prec))
            infix.append(Push(prec))
            infix.append(Push(rule.name))
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
