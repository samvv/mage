
from typing import Iterator, assert_never
from sweetener import Record

from magelang.eval import accepts
from magelang.util import nonnull

from .ast import *

class Type(Record):
    pass

class ExternType(Type):
    """
    A type that is directly representing the Foo part in a `pub foo -> Foo = bar` 
    """
    name: str

class NodeType(Type):
    """
    Matches a leaf node in the AST/CST.
    """
    name: str

class TokenType(Type):
    """
    Matches a token type in the CST.
    """
    name: str

class VariantType(Type):
    """
    Matches a union of different nodes in the AST/CST.
    """
    name: str

class NeverType(Type):
    """
    Represents a type that never matches. Mostly useful to close off a union type when generating types.
    """
    pass

class TupleType(Type):
    """
    A type that allows values to contain a specific sequence of types.
    """
    element_types: list[Type]

class ListType(Type):
    """
    A type that allows multiple values of the same underlying type.
    """
    element_type: Type

class PunctType(Type):
    """
    A type that is like a list but where values are seperated by another type.
    """
    element_type: Type
    separator_type: Type

class UnionType(Type):
    """
    A type where any of the member types are valid.
    """
    types: list[Type]

class NoneType(Type):
    """
    A type that indicates that the value is empty.

    This type is usually created in conjunction with a union type.
    """
    pass

class Field(Record):
    """
    Not a type, but represents exactly one field of a data structure/CST node. 
    """
    name: str
    ty: Type

class SpecBase(Record):
    pass

class TokenSpec(SpecBase):
    name: str
    field_type: str
    is_static: bool

class NodeSpec(SpecBase):
    name: str
    members: list[Field]

class VariantSpec(SpecBase):
    name: str
    members: list[tuple[str, Type]]

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

    def get_nodes(self) -> Iterator[NodeSpec]:
        for spec in self:
            if isinstance(spec, NodeSpec):
                yield spec

    def __iter__(self) -> Iterator[Spec]:
        return iter(self.mapping.values())

def make_optional(ty: Type) -> Type:
    return UnionType([ ty, NoneType() ])

def is_optional(ty: Type) -> bool:
    # if isinstance(ty, NoneType):
    #     return True
    if isinstance(ty, UnionType):
        for ty_2 in flatten_union(ty):
            if isinstance(ty_2, NoneType):
                return True
    return False

def make_unit() -> Type:
    return TupleType([])

def is_unit(ty: Type) -> bool:
    return isinstance(ty, TupleType) and len(ty.element_types) == 0

def infer_type(grammar: Grammar, expr: Expr) -> Type:

    if isinstance(expr, HideExpr):
        return make_unit()

    if isinstance(expr, ListExpr):
        element_field = infer_type(grammar, expr.element)
        separator_field = infer_type(grammar, expr.separator)
        return PunctType(element_field, separator_field)

    if isinstance(expr, RefExpr):
        rule = grammar.lookup(expr.name)
        if rule.is_extern:
            return ExternType(rule.type_name) #TokenType(rule.name) if rule.is_token else NodeType(rule.name)
        if not rule.is_public:
            return infer_type(grammar, nonnull(rule.expr))
        if grammar.is_token_rule(rule):
            return TokenType(rule.name) 
        if grammar.is_variant(rule):
            return VariantType(rule.name)
        return NodeType(rule.name)

    if isinstance(expr, LitExpr) or isinstance(expr, CharSetExpr):
        assert(False) # literals should already have been eliminated

    if isinstance(expr, RepeatExpr):
        element_type = infer_type(grammar, expr.expr)
        if expr.max == 0:
            return make_unit()
        elif expr.min == 0 and expr.max == 1:
            ty = make_optional(element_type)
        elif expr.min == 1 and expr.max == 1:
            ty = element_type
        else:
            ty = ListType(element_type)
        return ty

    if isinstance(expr, SeqExpr):
        types = []
        for element in expr.elements:
            ty = infer_type(grammar, element)
            if is_unit(ty):
                continue
            types.append(ty)
        if len(types) == 1:
            return types[0]
        return TupleType(types)

    if isinstance(expr, LookaheadExpr):
        return make_unit()

    if isinstance(expr, ChoiceExpr):
        return UnionType(list(infer_type(grammar, element) for element in expr.elements))

    assert_never(expr)

def flatten_union(ty: Type) -> Generator[Type, None, None]:
    if isinstance(ty, UnionType):
        for ty in ty.types:
            yield from flatten_union(ty)
    else:
        yield ty

def do_types_shallow_overlap(a: Type, b: Type) -> bool:
    """
    Determine whether two types have roughly the same structure.

    In Python, you could view this as whether the check `type(a) == type(b)`
    will always hold.
    """

    if isinstance(a, NeverType) or isinstance(b, NeverType):
        return False

    if isinstance(a, UnionType):
        return any(do_types_shallow_overlap(element_type, b) for element_type in a.types)

    if isinstance(b, UnionType):
        return do_types_shallow_overlap(b, a)

    if isinstance(a, ExternType) and isinstance(b, ExternType):
        return a.name == b.name

    if isinstance(a, NodeType) and isinstance(b, NodeType):
        return a.name == b.name

    if isinstance(a, VariantType) and isinstance(b, VariantType):
        return a.name == b.name

    if isinstance(a, TokenType) and isinstance(b, TokenType):
        return a.name == b.name

    if isinstance(a, ListType) and isinstance(b, ListType):
        return True

    if isinstance(a, PunctType) and isinstance(b, PunctType):
        return True

    if isinstance(a, NoneType) and isinstance(b, NoneType):
        return True

    if isinstance(a, TupleType) and isinstance(b, TupleType):
        return True

    return False

def simplify_type(ty: Type) -> Type:
    if isinstance(ty, UnionType):
        types = []
        has_none = False
        for ty in flatten_union(ty):
            if isinstance(ty, NeverType):
                continue
            if  isinstance(ty, NoneType):
                has_none = True
                continue
            types.append(ty)
        if has_none:
            types.append(NoneType())
        if len(types) == 0:
            return NeverType()
        if len(types) == 1:
            return types[0]
        return UnionType(types)
    else:
        return ty

def grammar_to_specs(grammar: Grammar) -> Specs:

    field_counter = 0
    def generate_field_name() -> str:
        nonlocal field_counter
        name = f'field_{field_counter}'
        field_counter += 1
        return name

    def get_member_name(expr: Expr) -> str:
        if expr.label is not None:
            return expr.label
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            assert(rule.is_public)
            return expr.name
        raise NotImplementedError()

    def get_variant_members(expr: Expr) -> Generator[tuple[str, Type], None, None]:
        if isinstance(expr, ChoiceExpr):
            for element in expr.elements:
                yield from get_variant_members(element)
            return
        if isinstance(expr, SeqExpr):
            names = []
            types = []
            for element in expr.elements:
                names.append(get_member_name(element))
                types.append(infer_type(grammar, element))
            yield '_'.join(names), TupleType(types)
            return
        yield get_member_name(expr), infer_type(grammar, expr)

    def plural(name: str) -> str:
        return name if name.endswith('s') else f'{name}s'

    def get_field_name(expr: Expr) -> str:
        if expr.label is not None:
            return expr.label
        if isinstance(expr, RefExpr):
            return expr.name
        if isinstance(expr, RepeatExpr):
            element_label = get_field_name(expr.expr)
            if element_label is not None:
                if expr.max > 1:
                    return plural(element_label)
                return element_label
            return generate_field_name()
        if isinstance(expr, ListExpr) or isinstance(expr, CharSetExpr) or isinstance(expr, ChoiceExpr):
            return generate_field_name()
        raise RuntimeError(f'unexpected {expr}')

    def get_node_members(expr: Expr) -> Generator[Field, None, None]:

        if isinstance(expr, HideExpr) or isinstance(expr, LookaheadExpr):
            return

        if isinstance(expr, SeqExpr):
            for element in expr.elements:
                yield from get_node_members(element)
            return

        if isinstance(expr, LitExpr) or isinstance(expr, CharSetExpr):
            assert(False) # literals should already have been eliminated

        field_name = get_field_name(expr)
        field_type = simplify_type(infer_type(grammar, expr))
        expr.field_name = field_name
        expr.field_type = field_type
        yield Field(field_name, field_type)

    def rename_duplicate_members(members: list[Field]) -> list[Field]:
        taken = dict[str, int]()
        out = []
        for field in members:
            count = taken.get(field.name, 0)
            taken[field.name] = count + 1
            if count > 0:
                field.name = f'{field.name}_{count+1}'
        return out

    specs = Specs()

    for rule in grammar.rules:
        if rule.is_extern or grammar.is_fragment(rule) or rule.is_skip:
            continue
        # only Rule(is_extern=True) can have an empty expression
        assert(rule.expr is not None)
        if grammar.is_token_rule(rule):
            specs.add(TokenSpec(rule.name, rule.type_name, grammar.is_static_token(rule.expr) if rule.expr is not None else False))
            continue
        if grammar.is_variant(rule):
            specs.add(VariantSpec(rule.name, list(get_variant_members(rule.expr))))
            continue
        field_counter = 0
        assert(rule.expr is not None)
        members = list(get_node_members(rule.expr))
        rename_duplicate_members(members)
        specs.add(NodeSpec(rule.name, members))

    kw_rules = []

    def visit(expr: Expr, rule: Rule) -> None:
        if isinstance(expr, LitExpr):
            match = False
            for rule in kw_rules:
                assert(rule.expr is not None)
                if accepts(rule.expr, expr.text, grammar):
                    match = True
            if match:
                specs.add(TokenSpec(rule.name, unit_rule_name, True))

    for rule in grammar.rules:
        if rule.expr is not None:
            for_each_expr(rule.expr, lambda expr: visit(expr, rule))

    return specs

