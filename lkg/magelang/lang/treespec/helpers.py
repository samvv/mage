
from functools import lru_cache
from typing import Generator, assert_never
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


def make_optional_type(ty: Type) -> Type:
    return UnionType([ ty, NoneType() ])


def is_optional_type(ty: Type) -> bool:
    if isinstance(ty, NoneType):
        return True
    if isinstance(ty, UnionType):
        for ty_2 in flatten_union_types(ty):
            if isinstance(ty_2, NoneType):
                return True
    return False


def unwrap_optional_type(ty: Type) -> Type:
    assert(isinstance(ty, UnionType))
    found = None
    for el_ty in ty.types:
        if not isinstance(el_ty, NoneType):
            assert(found is None)
            found = el_ty
    assert(found is not None)
    return found


def make_unit_type() -> Type:
    return TupleType(list())


def is_unit_type(ty: Type) -> bool:
    return isinstance(ty, TupleType) and len(ty.element_types) == 0


def is_static_type(ty: Type, specs: Specs) -> bool:
    visited = set[str]()
    def visit(ty: Type) -> bool:
        ty = resolve_type_references(ty, specs=specs)
        if isinstance(ty, ExternType):
            return False
        if isinstance(ty, NeverType):
            return False
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, UnionType):
            return all(visit(ty_2) for ty_2 in ty.types)
        if isinstance(ty, SpecType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = lookup_spec(specs, ty.name)
            assert(not isinstance(spec, TypeSpec))
            if spec is None:
                return False
            if isinstance(spec, ConstEnumSpec):
                return False
            if isinstance(spec, EnumSpec):
                return all(visit(member.ty) for member in spec.members)
            if isinstance(spec, NodeSpec):
                return all(visit(field.ty) for field in spec.fields)
            if isinstance(spec, TokenSpec):
                return spec.is_static
            assert_never(spec)
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
    if isinstance(ty, SpecType):
        return f'decl_{ty.name}'
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


def flatten_union_types(ty: Type) -> Generator[Type, None, None]:
    if isinstance(ty, UnionType):
        for ty in ty.types:
            yield from flatten_union_types(ty)
    else:
        yield ty


def spec_to_type(spec: Spec) -> Type:
    return SpecType(spec.name)


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

    if isinstance(a, SpecType) and isinstance(b, SpecType):
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
        if isinstance(ty, SpecType):
            spec = lookup_spec(specs, ty.name)
            if isinstance(spec, EnumSpec):
                types = list()
                assert(isinstance(spec, EnumSpec))
                for member in spec.members:
                    types.append(rewriter(member.ty))
                return UnionType(types)
        return rewrite_each_child_type(ty, rewriter)
    return rewriter(ty)

def resolve_type_references(ty: Type, *, specs: Specs) -> Type:
    if isinstance(ty, SpecType):
        spec = lookup_spec(specs, ty.name)
        if isinstance(spec, TypeSpec):
            return resolve_type_references(spec.ty, specs=specs)
    return ty

def is_type_assignable(left: Type, right: Type, *, specs: Specs) -> bool:
    """
    Check whether `right` is assignable to `left`, as in the Python expression `left = right`.
    """
    left = resolve_type_references(left, specs=specs)
    right = resolve_type_references(right, specs=specs)
    if isinstance(left, NeverType) or isinstance(right, NeverType):
        return False
    if isinstance(left, AnyType) or isinstance(right, AnyType):
        return True
    if isinstance(left, NoneType) and isinstance(right, NoneType):
        return True
    if isinstance(left, ExternType) and isinstance(right, ExternType):
        return left.name == right.name
    if isinstance(left, SpecType) and isinstance(right, SpecType):
        return left.name == right.name
    if isinstance(left, ListType) and isinstance(right, ListType):
        return is_type_assignable(left.element_type, right.element_type, specs=specs)
    if isinstance(left, PunctType) and isinstance(right, ListType):
        return is_type_assignable(left.element_type, right.element_type, specs=specs) \
           and is_type_assignable(left.element_type, right.element_type, specs=specs)
    if isinstance(right, UnionType):
        return all(is_type_assignable(left, ty, specs=specs) for ty in right.types)
    if isinstance(left, UnionType):
        return any(is_type_assignable(ty, right, specs=specs) for ty in left.types)
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


def contains_type(ty: Type, target: Type, *, specs: Specs) -> bool:
    """
    Check whether any part `ty` is assignable to `target`.
    """
    if is_type_assignable(target, ty, specs=specs):
        return True
    for ty_2 in expand_type(ty):
        if contains_type(ty_2, target, specs=specs):
            return True
    return False


def is_self_referential(name: str, *, specs: Specs, default: bool = False) -> bool:
    """
    Determine whether a declaration references itself eventually though one of its members.
    """

    visited = set[str]()

    main_type = SpecType(name)

    def check(ty: Type) -> bool:

        ty = resolve_type_references(ty, specs=specs)

        # If the type is assignable to our original type, that means we have
        # detected a cycle.
        if is_type_assignable(main_type, ty, specs=specs):
            return True

        return check_each_child(ty)

    def check_each_child(ty: Type) -> bool:

        if isinstance(ty, SpecType):

            # We encountered this type before. This means that there is a
            # cycle, but it's not the cycle we are interested in.
            if ty.name in visited:
                return False

            visited.add(ty.name)

            spec = lookup_spec(specs, ty.name)
            assert(not isinstance(spec, TypeSpec))
            if spec is None:
                return default
            if isinstance(spec, ConstEnumSpec) or isinstance(spec, TokenSpec):
                return False
            if isinstance(spec, NodeSpec):
                return any(check(field.ty) for field in spec.fields)
            if isinstance(spec, EnumSpec):
                return any(check(member.ty) for member in spec.members)
            assert_never(spec)

        for ty_2 in expand_type(ty):
            if check(ty_2):
                return True

        return False

    return check_each_child(main_type)


def normalize_type(ty: Type) -> Type:
    if isinstance(ty, UnionType):
        types = []
        for ty_2 in flatten_union_types(ty):
            if isinstance(ty_2, NeverType):
                continue
            if isinstance(ty_2, AnyType):
                return AnyType()
            types.append(normalize_type(ty_2))
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
    return rewrite_each_child_type(ty, normalize_type)


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

    for ty_2 in flatten_union_types(ty):

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
    return normalize_type(UnionType(types))
