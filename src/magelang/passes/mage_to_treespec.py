
from typing import Iterable
from magelang.helpers import get_field_name, infer_type, get_fields
from magelang.lang.mage.ast import *
from magelang.lang.treespec import *
from magelang.manager import declare_pass

@declare_pass()
def mage_to_treespec(
    grammar: MageGrammar,
    strong_enums: bool = False,
    include_hidden: bool = False
) -> Specs:

    field_counter = 0
    def generate_field_name() -> str:
        nonlocal field_counter
        name = f'field_{field_counter}'
        field_counter += 1
        return name

    def get_variant_name(expr: MageExpr, i: int) -> str:
        name = get_field_name(expr)
        return f'member_{i}'  if name is None else name

    def get_variants(expr: MageExpr) -> list[Variant]:
        out: list[Variant] = []
        def visit(expr: MageExpr) -> None:
            if isinstance(expr, MageChoiceExpr):
                for element in expr.elements:
                    visit(element)
                return
            if isinstance(expr, MageSeqExpr):
                names = []
                types = list()
                for element in expr.elements:
                    names.append(get_variant_name(element, len(out)))
                    types.append(infer_type(element, grammar))
                out.append(Variant('_'.join(names), TupleType(types)))
                return
            out.append(Variant(get_variant_name(expr, len(out)), infer_type(expr, grammar)))
        visit(expr)
        return out

    def get_field_members(expr: MageExpr) -> Iterable[Field]:
        for expr, field in get_fields(expr, grammar, include_hidden=include_hidden):
            if field is not None:
                yield field

    toplevel = []

    for rule in grammar.rules:
        if rule.is_extern or rule.is_fragment or rule.is_skip_def:
            continue
        # only Rule(is_extern=True) can have an empty expression
        assert(rule.expr is not None)
        if grammar.is_token_rule(rule):
            toplevel.append(TokenSpec(rule.name, rule.type_name, grammar.is_static_token_rule(rule) if rule.expr is not None else False))
            continue
        if grammar.is_variant_rule(rule):
            # if strong_enums:
            #     toplevel.append(VariantSpec(rule.name, list(get_variants(rule.expr))))
            # else:
            #     toplevel.append(TypeSpec(rule.name, UnionType(list(ty for _, ty in get_variants(rule.expr)))))
            toplevel.append(EnumSpec(rule.name, list(get_variants(rule.expr))))
            continue
        field_counter = 0
        assert(rule.expr is not None)
        members = list(get_field_members(rule.expr))
        toplevel.append(NodeSpec(rule.name, members))

    toplevel.sort(key=lambda spec: spec.name)

    return Specs(toplevel)
