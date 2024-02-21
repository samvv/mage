
from collections.abc import Iterator
import json
from pathlib import Path
from sweetener import Record

from .ast import *

class Type(Record):
    pass

class AnyTokenType(Type):
    pass

class AnyNodeType(Type):
    pass

class NodeType(Type):
    name: str

class TokenType(Type):
    name: str

class TupleType(Type):
    element_types: list[Type]

class ListType(Type):
    element_type: Type

class UnionType(Type):
    types: list[Type]

class NoneType(Type):
    pass

class Field(Record):
    name: str
    ty: Type

class SpecBase(Record):
    pass

class TokenSpec(SpecBase):
    name: str
    field_type: str | None
    is_static: bool

class NodeSpec(SpecBase):
    name: str
    members: list[Field]

class VariantSpec(SpecBase):
    name: str
    members: list[str]

builtin_types = {
    'String',
    'Integer',
}

Spec = TokenSpec | NodeSpec | VariantSpec

class Specs:

    def __init__(self) -> None:
        self.mapping = dict[str, Spec]()

    def is_static(self, name: str) -> bool:
        spec = self.mapping.get(name)
        assert(isinstance(spec, TokenSpec))
        return spec.is_static

    def add(self, spec: Spec) -> None:
        assert(spec.name not in self.mapping)
        self.mapping[spec.name] = spec

    def lookup(self, name: str) -> Spec:
        spec = self.mapping.get(name)
        if spec is None:
            raise RuntimeError(f"could not find a CST specification for '{name}'")
        return spec

    def __iter__(self) -> Iterator[Spec]:
        return iter(self.mapping.values())

def flatten_union(ty: Type) -> Generator[Type, None, None]:
    if isinstance(ty, UnionType):
        for element in ty.types:
            yield from flatten_union(element)
    else:
        yield ty

def grammar_to_specs(grammar: Grammar) -> Specs:

    with open(Path(__file__).parent / 'names.json', 'r') as f:
        names = json.load(f)

    field_counter = 0
    def generate_field_name() -> str:
        nonlocal field_counter
        name = f'field_{field_counter}'
        field_counter += 1
        return name

    token_counter = 0
    def generate_token_name() -> str:
        nonlocal token_counter
        name = f'token_{token_counter}'
        token_counter += 1
        return name

    literal_to_name = dict()

    def make_optional(ty: Type) -> Type:
        return UnionType([ ty, NoneType() ])

    def str_to_name(text: str) -> str | None:
        if text[0].isalpha() and all(ch.isalnum() for ch in text[1:]):
            return f'{text}_keyword'
        elif len(text) <= 4:
            return '_'.join(names[ch] for ch in text)

    def is_variant(rule: Rule) -> bool:
        def visit(expr: Expr) -> bool:
            if isinstance(expr, RefExpr):
                rule = grammar.lookup(expr.name)
                if grammar.is_parse_rule(rule):
                    return True
                # FIXME What to do with Rule(is_extern=True, is_public=False) ?
                assert(rule.expr is not None)
                return visit(rule.expr)
            if isinstance(expr, ChoiceExpr):
                for element in expr.elements:
                    if not visit(element):
                        return False
                return True
            return False
        if rule.is_extern:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(rule.expr is not None)
        return visit(rule.expr)

    def get_variant_members(expr: Expr) -> Generator[str, None, None]:
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            if rule.is_public:
                yield rule.name
                return
            # FIXME What to do with Rule(is_extern=True, is_public=False) ?
            if rule.expr is not None:
                yield from get_variant_members(rule.expr)
            return
        if isinstance(expr, ChoiceExpr):
            for element in expr.elements:
                yield from get_variant_members(element)
            return
        assert(False)

    def get_node_members(expr: Expr, toplevel: bool) -> Generator[Field, None, None]:
        if isinstance(expr, HideExpr):
            return
        if isinstance(expr, ListExpr):
            element_fields = list(get_node_members(expr.element, False))
            separator_fields = list(get_node_members(expr.separator, False))
            if not element_fields and not separator_fields:
                return
            assert(len(element_fields) == 1)
            assert(len(separator_fields) == 1)
            label = expr.label
            if label is None:
                label = generate_field_name()
            yield Field(label, ListType(TupleType([ element_fields[0].ty, make_optional(separator_fields[0].ty) ])))
            return
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            label = rule.name if expr.label is None else expr.label
            if rule.is_extern:
                yield Field(label, TokenType(rule.name) if rule.is_token else NodeType(rule.name))
                return
            if not rule.is_public:
                assert(rule.expr is not None)
                yield from get_node_members(rule.expr, toplevel)
                return
            # TODO yield TokenType if rule is a token rule
            yield Field(label, NodeType(expr.name))
            return
        if isinstance(expr, LitExpr):
            label = expr.label
            if label is None:
                label = str_to_name(expr.text)
                if label is None:
                    label = generate_field_name()
            yield Field(label, TokenType(literal_to_name[expr.text]))
            return
        if isinstance(expr, RepeatExpr):
            fields = list(get_node_members(expr.expr, False))
            assert(len(fields) == 1)
            field = fields[0]
            label = expr.label
            if label is None:
                label = field.name
                if label is None:
                    label = generate_field_name()
            if expr.max == 0:
                return
            elif expr.min == 0 and expr.max == 1:
                ty = make_optional(field.ty)
            elif expr.min == 1 and expr.max == 1:
                ty = field.ty
            else:
                ty = ListType(field.ty)
            yield Field(label, ty)
            return
        if isinstance(expr, CharSetExpr):
            label = expr.label if expr.label is not None else generate_field_name()
            yield Field(label, AnyTokenType())
            return
        if isinstance(expr, SeqExpr):
            if toplevel:
                for element in expr.elements:
                    yield from get_node_members(element, True)
            else:
                label = expr.label if expr.label is not None else generate_field_name()
                types = []
                for element in expr.elements:
                    for field in get_node_members(element, False):
                        types.append(field.ty)
                if not types:
                    return
                yield Field(label, TupleType(types) if len(types) > 1 else types[0])
            return
        if isinstance(expr, LookaheadExpr):
            return
        if isinstance(expr, ChoiceExpr):
            label = expr.label if expr.label is not None else generate_field_name()
            fields = list(field for element in expr.elements for field in get_node_members(element, False))
            if len(fields) == 1:
                yield fields[0]
                return
            yield Field(label, UnionType(list(field.ty for field in fields)))
            return
        raise RuntimeError(f'unexpected {expr}')

    def is_static(expr: Expr):
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            if rule.is_extern:
                return False
            assert(rule.expr is not None)
            return is_static(rule.expr)
        if isinstance(expr, LitExpr):
            return True
        if isinstance(expr, CharSetExpr):
            # FIXME should I check whether the range contains only one char?
            return False
        if isinstance(expr, SeqExpr):
            return all(is_static(element) for element in expr.elements)
        if isinstance(expr, ChoiceExpr):
            # FIXME should I check whether the choices are actually different?
            return False
        if isinstance(expr, RepeatExpr):
            if expr.min != expr.max:
                return False
            return is_static(expr.expr)
        if isinstance(expr, LookaheadExpr):
            # Lookahead has no effect on what (non-)static characters are generated
            return True
        raise RuntimeError(f'unexpected {expr}')

    specs = Specs()

    def collect_literals(expr: Expr):
        if isinstance(expr, LitExpr):
            name = str_to_name(expr.text)
            if name is None:
                name = generate_token_name()
            if expr.text not in literal_to_name:
                specs.add(TokenSpec(name, string_kind, True))
                literal_to_name[expr.text] = name
            return
        for_each_expr(expr, collect_literals)

    for rule in grammar.rules:
        if rule.expr is not None:
            collect_literals(rule.expr)

    for rule in grammar.rules:
        if rule.is_extern or grammar.is_fragment(rule) or rule.has_decorator('skip'):
            continue
        # only Rule(is_extern=True) can have an empty expression
        assert(rule.expr is not None)
        if grammar.is_token_rule(rule):
            specs.add(TokenSpec(rule.name, rule.type_name, is_static(rule.expr) if rule.expr is not None else False))
            continue
        if is_variant(rule):
            specs.add(VariantSpec(rule.name, list(get_variant_members(rule.expr))))
            continue
        field_counter = 0
        assert(rule.expr is not None)
        members = list(get_node_members(rule.expr, True))
        specs.add(NodeSpec(rule.name, members))

    return specs

