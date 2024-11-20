
from magelang.lang.mage.ast import *

def mage_simplify(grammar: MageGrammar) -> MageGrammar:

    def make_fail() -> MageExpr:
        return MageChoiceExpr([])

    def make_empty(rules: list[MageRule] | None = None) -> MageExpr:
        return MageSeqExpr([], rules=rules)

    def is_fail(expr: MageExpr) -> bool:
        return isinstance(expr, MageChoiceExpr) and expr.elements == 0

    def is_empty(expr: MageExpr) -> bool:
        return isinstance(expr, MageSeqExpr) and expr.elements == 0

    def flatten_choice(elements: list[MageExpr]) -> Generator[MageExpr, None, None]:
        for expr in elements:
            if isinstance(expr, MageChoiceExpr):
                yield from flatten_choice(expr.elements)
            else:
                yield visit(expr)

    def flatten_seq(elements: list[MageExpr]) -> Generator[MageExpr, None, None]:
        for expr in elements:
            if isinstance(expr, MageSeqExpr):
                yield from flatten_seq(expr.elements)
            else:
                yield visit(expr)

    def flatten(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageChoiceExpr):
            return MageChoiceExpr(list(flatten_choice(expr.elements)))
        if isinstance(expr, MageSeqExpr):
            return MageSeqExpr(list(flatten_seq(expr.elements)))
        return expr

    def visit(expr: MageExpr) -> MageExpr:

        if isinstance(expr, MageLitExpr):
            if not expr.text:
                return make_empty(expr.rules)
            return expr

        if isinstance(expr, MageChoiceExpr):
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

        if isinstance(expr, MageSeqExpr):
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

        if isinstance(expr, MageCharSetExpr):

            if len(expr.elements) == 0:
                return expr

            normalized = list[tuple[str, str]]()
            for element in expr.elements:
                if isinstance(element, tuple):
                    low, high = element
                else:
                    low = element
                    high = element
                normalized.append((low, high))

            normalized.sort()

            new_elements = list[CharSetElement]()

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
                new_elements.append(prev_l if prev_l == max_h else (prev_l, max_h))
                prev_l = l
                prev_h = h
                max_h = max(h, max_h)
            new_elements.append(prev_l if prev_l == max_h else (prev_l, max_h))

            return expr.derive(elements=new_elements)

        if isinstance(expr, MageRefExpr):
            # We visit each rule so no need to lookup the rule in the grammar
            return expr

        if isinstance(expr, MageRepeatExpr):
            new_expr = visit(expr.expr)
            if is_empty(new_expr):
                return new_expr
            if is_fail(new_expr):
                return make_empty()
            if expr.max == 0:
                return make_empty()
            if expr.min == 1 and expr.max == 1:
                return expr
            return expr.derive(expr=new_expr)

        if isinstance(expr, MageHideExpr) or isinstance(expr, MageLookaheadExpr):
            return expr.derive(expr=visit(expr.expr))

        if isinstance(expr, MageListExpr):
            new_separator = visit(expr.separator)
            new_element = visit(expr.element)
            if is_empty(new_element):
                return new_element
            if is_fail(new_element):
                return make_empty()
            if is_fail(new_separator):
                if expr.min_count == 0:
                    return MageRepeatExpr(new_element, 0, 1)
                if expr.min_count == 1:
                    return new_element
                return new_separator
            if is_empty(new_separator):
                return MageRepeatExpr(new_element, expr.min_count, POSINF)
            return expr.derive(element=new_element, separator=new_separator)

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

    return MageGrammar(rules=new_rules)

