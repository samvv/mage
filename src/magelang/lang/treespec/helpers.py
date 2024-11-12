
from functools import lru_cache
from typing import Generator
from magelang.util import to_snake_case
from .ast import *

@lru_cache
def _get_spec_mapping(specs: Specs) -> dict[str, Spec]:
    out = {}
    for spec in specs.elements:
        out[spec.name] = spec
    return out

def lookup_spec(specs: Specs, name: str) -> Spec | None:
    return _get_spec_mapping(specs).get(name)

def make_optional(ty: Type) -> Type:
    return UnionType([ ty, NoneType() ])

def is_optional(ty: Type) -> bool:
    if isinstance(ty, NoneType):
        return True
    if isinstance(ty, UnionType):
        for ty_2 in flatten_union(ty):
            if isinstance(ty_2, NoneType):
                return True
    return False

def get_optional_element(ty: Type) -> Type:
    assert(isinstance(ty, UnionType))
    found = None
    for el_ty in ty.types:
        if not isinstance(el_ty, NoneType):
            assert(found is None)
            found = el_ty
    assert(found is not None)
    return found

def make_unit() -> Type:
    return TupleType(list())

def is_unit_type(ty: Type) -> bool:
    return isinstance(ty, TupleType) and len(ty.element_types) == 0

def is_static_type(ty: Type, specs: Specs) -> bool:
    visited = set[str]()
    def visit(ty: Type) -> bool:
        if isinstance(ty, ExternType):
            return False
        if isinstance(ty, NeverType):
            return False
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, UnionType):
            return all(visit(ty_2) for ty_2 in ty.types)
        if isinstance(ty, VariantType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, VariantSpec))
            return all(visit(ty_2) for _, ty_2 in spec.members)
        if isinstance(ty, NodeType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, NodeSpec))
            return all(visit(field.ty) for field in spec.fields)
        if isinstance(ty, TokenType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, TokenSpec))
            return spec.is_static
        if isinstance(ty, TupleType):
            return all(visit(ty_2) for ty_2 in ty.element_types)
        if isinstance(ty, ListType):
            # This assumes that repetitions of a fixed size have been eliminated.
            return False
        if isinstance(ty, PunctType):
            return False
        if isinstance(ty, AnyType):
            return False
        assert_never(ty)
    return visit(ty)

def mangle_type(ty: Type) -> str:
    if isinstance(ty, NodeType):
        return f'node_{ty.name}'
    if isinstance(ty, VariantType):
        return f'variant_{ty.name}'
    if isinstance(ty, TokenType):
        return f'token_{ty.name}'
    if isinstance(ty, TupleType):
        out = f'tuple_{len(ty.element_types)}'
        for ty in ty.element_types:
            out += '_' + mangle_type(ty)
        return out
    if isinstance(ty, ListType):
        out = f'list_{mangle_type(ty.element_type)}'
        if ty.required:
            out += '_required'
        return out
    if isinstance(ty, ExternType):
        return f'extern_{to_snake_case(ty.name)}'
    if isinstance(ty, NeverType):
        return 'never'
    if isinstance(ty, NoneType):
        return 'none'
    if isinstance(ty, UnionType):
        out = f'union_{len(ty.types)}'
        for ty in ty.types:
            out += '_' + mangle_type(ty)
        return out
    if isinstance(ty, PunctType):
        out = f'punct_{mangle_type(ty.element_type)}_{mangle_type(ty.separator_type)}'
        if ty.required:
            out += '_required'
        return out
    if isinstance(ty, AnyType):
        return 'any'
    assert_never(ty)


def flatten_union(ty: Type) -> Generator[Type, None, None]:
    if isinstance(ty, UnionType):
        for ty in ty.types:
            yield from flatten_union(ty)
    else:
        yield ty

def spec_to_type(spec: Spec) -> Type:
    if isinstance(spec, TokenSpec):
        return TokenType(spec.name)
    if isinstance(spec, NodeSpec):
        return NodeType(spec.name)
    if isinstance(spec, VariantSpec):
        return VariantType(spec.name)
    assert_never(spec)

def do_types_shallow_overlap(a: Type, b: Type) -> bool:
    """
    Determine whether two types have roughly the same structure.

    In Python, you could view this as whether the check `type(a) == type(b)`
    will always hold.
    """

    if isinstance(a, NeverType) or isinstance(b, NeverType):
        return False

    if isinstance(a, AnyType) or isinstance(b, AnyType):
        return True

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

def expand_variant_types(ty: Type, *, specs: Specs) -> Type:
    def rewriter(ty: Type) -> Type:
        if isinstance(ty, VariantType):
            types = list()
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, VariantSpec))
            for _, ty_2 in spec.members:
                types.append(rewriter(ty_2))
            return UnionType(types)
        return rewrite_each_child_type(ty, rewriter)
    return rewriter(ty)

def simplify_type(ty: Type) -> Type:
    if isinstance(ty, NoneType) \
        or isinstance(ty, NeverType) \
        or isinstance(ty, NodeType) \
        or isinstance(ty, ExternType) \
        or isinstance(ty, AnyType) \
        or isinstance(ty, VariantType) \
        or isinstance(ty, TokenType):
        return ty
    if isinstance(ty, ListType):
        return ty.derive(element_type=simplify_type(ty.element_type))
    if isinstance(ty, TupleType):
        return ty.derive(element_types=list(simplify_type(ty) for ty in ty.element_types))
    if isinstance(ty, PunctType):
        return ty.derive(
            element_type=simplify_type(ty.element_type),
            separator_type=simplify_type(ty.separator_type),
        )
    if isinstance(ty, UnionType):
        types = []
        for ty_2 in flatten_union(ty):
            if isinstance(ty_2, NeverType):
                continue
            if isinstance(ty_2, AnyType):
                return AnyType()
            types.append(simplify_type(ty_2))
        if len(types) == 0:
            return NeverType()
        types.sort()
        iterator = iter(types)
        prev = next(iterator)
        dedup_types: list[Type] = list([ prev ])
        while True:
            try:
                curr = next(iterator)
            except StopIteration:
                break
            if prev == curr:
                continue
            dedup_types.append(curr)
            prev = curr
        if len(dedup_types) == 1:
            return dedup_types[0]
        return ty.derive(types=dedup_types)
    assert_never(ty)

def is_type_assignable(left: Type, right: Type, *, specs: Specs) -> bool:
    if isinstance(left, NeverType) or isinstance(right, NeverType):
        return False
    if isinstance(left, AnyType) or isinstance(right, AnyType):
        return True
    if isinstance(left, NoneType) and isinstance(right, NoneType):
        return True
    if isinstance(left, ExternType) and isinstance(right, ExternType):
        return left.name == right.name
    if isinstance(left, NodeType) and isinstance(right, NodeType):
        return left.name == right.name
    if isinstance(left, TokenType) and isinstance(right, TokenType):
        return left.name == right.name
    if isinstance(left, VariantType):
        spec = lookup_spec(specs, left.name)
        assert(isinstance(spec, VariantSpec))
        return all(is_type_assignable(ty, right, specs=specs) for _, ty in spec.members)
    if isinstance(right, VariantType):
        spec = lookup_spec(specs, right.name)
        assert(isinstance(spec, VariantSpec))
        return any(is_type_assignable(left, ty, specs=specs) for _, ty in spec.members)
    if isinstance(left, ListType) and isinstance(right, ListType):
        return is_type_assignable(left.element_type, right.element_type, specs=specs)
    if isinstance(left, PunctType) and isinstance(right, ListType):
        return is_type_assignable(left.element_type, right.element_type, specs=specs) \
           and is_type_assignable(left.element_type, right.element_type, specs=specs)
    if isinstance(left, UnionType):
        return all(is_type_assignable(ty, right, specs=specs) for ty in left.types)
    if isinstance(right, UnionType):
        return any(is_type_assignable(left, ty, specs=specs) for ty in right.types)
    if isinstance(left, TupleType) and isinstance(right, TupleType):
        if len(left.element_types) != len(right.element_types):
            return False
        for a, b in zip(left.element_types, right.element_types):
            if not is_type_assignable(a, b, specs=specs):
                return False
        return True
    return False


def expand_type(ty: Type):
    if isinstance(ty, ListType):
        yield ty.element_type
    elif isinstance(ty, PunctType):
        yield ty.element_type
        yield ty.separator_type
    elif isinstance(ty, TupleType):
        for element_type in ty.element_types:
            yield element_type
    elif isinstance(ty, UnionType):
        for ty_2 in ty.types:
            yield ty_2

def contains_type(ty: Type, target_type: Type, *, specs: Specs) -> bool:
    if is_type_assignable(ty, target_type, specs=specs):
        return True
    for ty_2 in expand_type(ty):
        if contains_type(ty_2, target_type, specs=specs):
            return True
    return False

def is_cyclic(name: str, *, specs: Specs) -> bool:
    """
    Determine whether a type references itself eventually.
    """

    visited = set[str]()

    spec = lookup_spec(specs, name)
    spec_type = expand_variant_types(spec_to_type(spec), specs=specs)

    def check(ty: Type, first = False) -> bool:

        # If the type is assignable to our original type, that means we have
        # detected a cycle.
        if not first and is_type_assignable(ty, spec_type, specs=specs):
            return True

        if isinstance(ty, NodeType):

            # We encountered this type before. This means that there is a
            # cycle, but it's not the cycle we are interested in.
            if ty.name in visited:
                return False

            visited.add(ty.name)

            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, NodeSpec))

            return any(check(expand_variant_types(field.ty, specs=specs)) for field in spec.fields)

        for ty_2 in expand_type(ty):
            if check(ty_2, first):
                return True

        return False

    return check(spec_type, first=True)

def merge_similar_types(ty: Type) -> Type:
    """
    Merges the elements of similarly structured types to a single type.

    For example, the type `List[int] | List[str]` becomes `List[int | str]`.

    Note that this is semantically incorrect, but some (mostly dynamic)
    programming languages can use this to write less intensive checks for a
    value that has this type.
    """

    # The resulting types that will be part of the output union type
    types = list[Type]()

    # Any types that should be inside of a `List[...]` type
    list_element_types = list[Type]()

    # `True` if all lists in the original type are required, `False` otherwise
    list_required = True

    # Any type that should go inside a `PunctType.element_type`
    punct_value_types = list[Type]()

    # Any type that should go inside a `PunctType.separator_type`
    punct_sep_types = list[Type]()

    # `True` if all punctuated types in the original type are required, `False`
    # otherwise
    punct_required = True

    # Holds tuples sorted by length, where each entry in the hash table
    # corresponds to another table that stores all possible elements for that
    # index.
    tuples_by_len = dict[int, list[list[Type]]]()\

    for ty_2 in flatten_union(ty):

        if isinstance(ty_2, TupleType):
            n = len(ty_2.element_types)
            if n not in tuples_by_len:
                new = list()
                for _ in range(0, n):
                    new.append(list())
                tuples_by_len[n] = new
            else:
                new = tuples_by_len[n]
            for i, ty_3 in enumerate(ty_2.element_types):
                new[i].append(merge_similar_types(ty_3))

        if isinstance(ty_2, ListType):
            list_element_types.append(merge_similar_types(ty_2.element_type))
            if not ty_2.required:
                list_required = False

        elif isinstance(ty_2, PunctType):
            punct_value_types.append(merge_similar_types(ty_2.element_type))
            punct_sep_types.append(merge_similar_types(ty_2.separator_type))
            if not ty_2.required:
                punct_required = False

        else:
            # If we got here, the type is not structural. In that case, we just
            # leave it as-is.
            types.append(ty_2)

    # Gather all list elements under a single `List[...]`, if any
    if list_element_types:
        types.append(ListType(UnionType(list_element_types), list_required))

    # Gather all punctuated types under a single `Punct[..., ....]`, if any
    if punct_value_types or punct_sep_types:
        assert(punct_value_types)
        assert(punct_sep_types)
        types.append(PunctType(UnionType(punct_value_types), UnionType(punct_sep_types), punct_required))

    # Gather all tuples, by traversing the hash table and freezing the elements that are stored together
    for tuple_elements in tuples_by_len.values():
        new_tuple_elements = list[Type]()
        for elements_at_index in tuple_elements:
            new_tuple_elements.append(UnionType(elements_at_index))
        types.append(TupleType(new_tuple_elements))

    # Some elements might be duplicated by the previous procedure, therefore we
    # call `simplify_type`.
    return simplify_type(UnionType(types))
