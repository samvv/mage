
from pathlib import Path
from magelang.lang.mage.ast import *
from magelang.manager import declare_pass

here = Path(__file__).parent.parent.parent.parent.resolve()

words = []

def random_word() -> str:
    if not words:
        with open(here / 'wordlist.10000') as f:
            for line in f:
                words.append(line.strip())
    import random
    return random.choice(words)

@declare_pass()
def mage_distill(grammar: MageGrammar) -> MageGrammar:
    """
    Distill a grammar to its essential parts to make it easier to debug by a human.

    May be used in conjunction with `mage_unhide` and `mage_simplify`.

    During the distillation, some essential features of the grammar may be
    lost, which may cause a bug to disappear. In that case you might need different tools.
    """

    next_character = 97
    mapping = dict[str, str]()

    for rule in grammar.rules:
        # TODO blacklist rule names already taken
        mapping[rule.name] = random_word()

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        nonlocal next_character
        if isinstance(expr, MageLitExpr):
            ch = chr(next_character)
            next_character += 1
            return expr.derive(text=ch)
        if isinstance(expr, MageCharSetExpr):
            ch = chr(next_character)
            next_character += 1
            return MageLitExpr(text=ch)
        if isinstance(expr, MageRefExpr):
            return expr.derive(name=mapping[expr.name])
        return rewrite_each_child_expr(expr, rewrite_expr)

    def rewrite_rule(rule: MageRule) -> MageRule:
        new_name = mapping[rule.name]
        if rule.expr is None:
            return rule.derive(name=new_name)
        return rule.derive(name=new_name, expr=rewrite_expr(rule.expr))

    return rewrite_each_rule(grammar, rewrite_rule)
