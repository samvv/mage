

from magelang.ast import Grammar, RefExpr, Expr
def check_undefined(grammar: Grammar) -> Grammar:
    def traverse(expr: Expr) -> None:
        if isinstance(expr, RefExpr):
            if not any(rule.name == expr.name for rule in grammar.rules):
                raise ValueError(f"Undefined rule referenced: {expr.name}")
        elif hasattr(expr, 'expr'):
            traverse(expr.expr)
        elif hasattr(expr, 'alternatives'):
            for alternative in expr.alternatives:
                traverse(alternative)

    for rule in grammar.rules:  
        traverse(rule.expr)
    
    return grammar
