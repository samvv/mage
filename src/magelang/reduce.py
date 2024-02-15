
from sweetener import warn
from .ast import *

FAIL = 1
EMPTY = 2

def transform(grammar: Grammar) -> Grammar:

    def make_fail() -> Expr:
        return ChoiceExpr([])

    def make_empty(rules: list[Rule] | None = None) -> Expr:
        return SeqExpr([], rules=rules)

    def is_fail(expr: Expr) -> bool:
        return isinstance(expr, ChoiceExpr) and expr.elements == 0

    def is_empty(expr: Expr) -> bool:
        return isinstance(expr, SeqExpr) and expr.elements == 0

    def flatten_choice(elements: list[Expr]) -> Generator[Expr, None, None]:
        for expr in elements:
            if isinstance(expr, ChoiceExpr):
                yield from flatten_choice(expr.elements)
            else:
                yield visit(expr)

    def flatten_seq(elements: list[Expr]) -> Generator[Expr, None, None]:
        for expr in elements:
            if isinstance(expr, SeqExpr):
                yield from flatten_seq(expr.elements)
            else:
                yield visit(expr)

    def flatten(expr: Expr) -> Expr:
        if isinstance(expr, ChoiceExpr):
            return ChoiceExpr(flatten_choice(expr.elements))
        if isinstance(expr, SeqExpr):
            return SeqExpr(flatten_seq(expr.elements))
        return expr

    def visit(expr: Expr) -> Expr:
        if isinstance(expr, LitExpr):
            if not expr.text:
                return make_empty(expr.rules)
            return expr
        if isinstance(expr, ChoiceExpr):
            new_elements = []
            has_empty = False
            empty_rules = []
            for new_element in flatten_choice(expr.elements):
                if is_fail(new_element):
                    continue
                if is_empty(new_element):
                    empty_rules.extend(new_element.rules)
                    has_empty = True
                    continue
                new_elements.append(new_element)
            if has_empty:
                new_elements.append(make_empty(empty_rules))
            if not new_elements:
                return make_fail()
            if len(new_elements) == 1:
                new_elements[0].rules.extend(expr.rules)
                return new_elements[0]
            return ChoiceExpr(new_elements, rules=expr.rules)
        if isinstance(expr, SeqExpr):
            new_elements = []
            has_fail = False
            for new_element in flatten_seq(expr.elements):
                if is_empty(new_element):
                    continue
                if is_fail(new_element):
                    has_fail = True
                    continue
                new_elements.append(new_element)
            if has_fail:
                new_elements.append(make_fail())
            if not new_elements:
                return make_empty()
            if len(new_elements) == 1:
                new_elements[0].rules.extend(expr.rules)
                return new_elements[0]
            return SeqExpr(new_elements, rules=expr.rules)
        if isinstance(expr, CharSetExpr):
            # TODO remove overlapping ranges
            return expr
        if isinstance(expr, RepeatExpr):
            return RepeatExpr(expr.min, expr.max, expr.expr, rules=expr.rules)
        if isinstance(expr, RefExpr):
            return expr
        raise RuntimeError(f'unexpected node {expr}')

    new_rules = []
    for rule in grammar.rules:
        # FIXME not sure why this call to flatten is necessary for good output
        new_expr = flatten(visit(rule.expr))
        if new_expr == FAIL:
            continue
        if new_expr == EMPTY:
            new_expr = LitExpr('')
        new_rules.append(Rule(rule.flags, rule.name, new_expr))

    return Grammar(rules=new_rules)

