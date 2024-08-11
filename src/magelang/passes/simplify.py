
from ..ast import *

def simplify(grammar: Grammar) -> Grammar:

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
            return ChoiceExpr(list(flatten_choice(expr.elements)))
        if isinstance(expr, SeqExpr):
            return SeqExpr(list(flatten_seq(expr.elements)))
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
            return expr.derive(elements=new_elements)
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
            return expr.derive(elements=new_elements)

        if isinstance(expr, CharSetExpr):

            assert(len(expr.elements) > 0)

            normalized = []
            for element in expr.elements:
                if isinstance(element, tuple):
                    low, high = element
                else:
                    low = element
                    high = element
                normalized.append((ord(low), ord(high)))

            normalized.sort()

            new_elements = []

            # The list is now strongly sorted on the first key. Go from left to
            # right over the list, incrementing max_h each time the interval
            # stretches. When it doesn't stretch, put wherever we started
            # combined with the maximum value we encountered in the output.
            prev_l, prev_h = normalized[0]
            max_h = prev_h
            for l, h in normalized[1:]:
                if l <= prev_h:
                    prev_h = h
                    continue
                new_elements.append((prev_l, max_h))
                prev_l = l
                prev_h = h
                max_h = max(h, max_h)

            return expr.derive(elements=new_elements)

        if isinstance(expr, RefExpr):
            # We visit each rule so no need to lookup the rule in the grammar
            return expr
        if isinstance(expr, RepeatExpr) or isinstance(expr, HideExpr) or isinstance(expr, LookaheadExpr):
            return expr.derive(expr=visit(expr.expr))
        if isinstance(expr, ListExpr):
            return expr.derive(element=visit(expr.element))
        assert_never(expr)

    new_rules = []
    for rule in grammar.rules:
        if rule.is_extern:
            new_rules.append(rule)
            continue
        assert(rule.expr is not None)
        # FIXME not sure why this call to flatten is necessary for good output
        new_expr = flatten(visit(rule.expr))
        new_rules.append(rule.derive(expr=new_expr))

    return Grammar(rules=new_rules)

