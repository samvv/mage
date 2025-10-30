
from magelang.lang.mage.ast import MageGrammar, MageRefExpr, MageExpr, MageRule, for_each_direct_child_expr, for_each_rule, lookup_ref
from magelang.manager import declare_pass
from magelang.runtime.diagnostics import Diagnostic, Diagnostics, Severity

@declare_pass()
def mage_check_undefined(
    grammar: MageGrammar,
    diagnostics: Diagnostics
) -> MageGrammar:

    def visit_expr(expr: MageExpr) -> None:
        if isinstance(expr, MageRefExpr):
            if lookup_ref(expr) is None:
                diagnostics.add(Diagnostic(Severity.error, f"'{expr.name}' is not a known rule at this scope", grammar.file, expr.span))
            return
        for_each_direct_child_expr(expr, visit_expr)

    def visit_rule(rule: MageRule) -> None:
        if rule.expr is not None:
            visit_expr(rule.expr)

    for_each_rule(grammar, visit_rule)

    return grammar
