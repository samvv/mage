
from magelang.lang.mage.ast import *
from magelang.manager import declare_pass

@declare_pass()
def mage_reduce_list_expr(grammar: MageGrammar) -> MageGrammar:
    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageListExpr):
            if expr.min_count == 0:
                return MageChoiceExpr([
                    MageLitExpr(''),
                    MageSeqExpr([
                        expr.element,
                        MageRepeatExpr(
                            MageSeqExpr([
                                expr.separator,
                                expr.element,
                            ]),
                            0,
                            POSINF,
                        )
                    ])
                ])
            return MageSeqExpr([
                expr.element,
                MageRepeatExpr(
                    MageSeqExpr([
                        expr.separator,
                        expr.element,
                    ]),
                    expr.min_count-1,
                    POSINF,
                )
            ])
        return rewrite_each_child_expr(expr, rewrite_expr)
    return rewrite_each_expr(grammar, rewrite_expr)
