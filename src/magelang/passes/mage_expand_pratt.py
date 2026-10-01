
from magelang.manager import declare_pass
from magelang.util import nonnull
from magelang.helpers import split_pratt
from magelang.lang.mage.ast import *


@declare_pass()
def mage_expand_pratt(grammar: MageGrammar) -> MageGrammar:
    """
    Splits multiple rules that may begin with the same expression into a primary rule and some variants.

    For example, the following rule:

    ```mage
    pub add_expr
      = expr '+' expr

    pub sub_expr
      = expr '-' expr

    pub expr
       = add_expr
       | lit_expr
       | ref_expr
       | sub_expr
    ```

    Would be converted into:

    ```mage
    @unwrap
    pub prim_expr
      = ref_expr
      | lit_expr

    pub add_expr
      = prim_expr '+' expr

    pub sub_expr
      = prim_expr '-' expr

    pub expr
      = add_expr
      | sub_expr
      | prim_expr
    ```
    """

    new_elements, pratts = split_pratt(grammar)

    for pratt in pratts:

        prim_rule_name = f'{pratt.name}_prim'
        wrap_rule_name = f'{pratt.name}_wrap'
        new_elements.extend(pratt.atoms)
        new_elements.append(MageRule(prim_rule_name, MageChoiceExpr(list(MageRefExpr(atom.name) for atom in pratt.atoms)), flags=PUBLIC))

        new_elements.append(MageRule(wrap_rule_name, MageSeqExpr([
            MageChoiceExpr(list(_get_prefix_operator(rule) for rule in pratt.prefix)),
            MageRefExpr(prim_rule_name),
            MageChoiceExpr(list(_get_suffix_operator(rule) for rule in pratt.suffix)),
        ]), flags=PUBLIC))

        next = wrap_rule_name

        for rule in pratt.infix:
            new_elements.append(substitute(rule, pratt.name, next))
            next = rule.name

        new_elements.append(MageRule(pratt.name, MageRefExpr(next), flags=PUBLIC))

    return grammar.derive(elements=new_elements)


def substitute(rule: MageRule, old: str, new: str) -> MageRule:
    assert(rule.expr is not None)
    return rule.derive(expr=substitute_expr(rule.expr, old, new))


def substitute_expr(expr: MageExpr, old: str, new: str) -> MageExpr:
    if isinstance(expr, MageRefExpr) and expr.name == old:
        return expr.derive(name=new)
    return rewrite_each_child_expr(expr, lambda child: substitute_expr(child, old, new))


def _get_prefix_operator(rule: MageRule) -> MageExpr:
    assert(rule.expr is not None)
    assert(isinstance(rule.expr, MageSeqExpr))
    return MageSeqExpr(rule.expr.elements[:-1])


def _get_suffix_operator(rule: MageRule) -> MageExpr:
    assert(rule.expr is not None)
    assert(isinstance(rule.expr, MageSeqExpr))
    return MageSeqExpr(rule.expr.elements[1:])

