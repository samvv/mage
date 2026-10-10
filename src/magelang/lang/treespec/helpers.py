from warnings import deprecated
from collections.abc import Iterable
from functools import lru_cache
from typing import Generator, assert_never, Union

from magelang.util import to_snake_case, todo
from .ast import *
from magelang.lang.mage.constants import string_rule_type


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
    found = []
    for el_ty in ty.types:
        if not isinstance(el_ty, NoneType):
            found.append(el_ty)
    if len(found) == 0:
        return NeverType()
    if len(found) == 1:
        return found[0]
    return UnionType(found)


def make_unit_type() -> Type:
    return TupleType(list())


def is_unit_type(ty: Type) -> bool:
    return isinstance(ty, TupleType) and len(ty.element_types) == 0


def is_static_type(ty: Type, specs: Specs) -> bool:
    visited = set[str]()
    def visit(ty: Type) -> bool:
        ty = expand_type(ty, specs=specs)
        if isinstance(ty, ExternType):
            return False
        if isinstance(ty, NeverType):
            return False
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, UnionType):
            if len(ty.types) >= 2:
                return False
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
        # FIXME what about a SpecType named 'foo_decl'?
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


@deprecated('This function is an anti-patern and should not be used.')
def expand_type(ty: Type, *, specs: Specs) -> Type:
    """
    Expand some special forms of a Type such as EnumSpec and TypeSpec.

    Using this function may simplify the implementation of some other functions.

    This function will return the never type when infinite recursion is detected.
    """
    cycle = False
    visited = set[Type]()
    def visit(ty: Type) -> Iterable[Type]:
        nonlocal cycle
        if ty in visited: # cycle detected
            cycle = True
            return
        visited.add(ty)
        if isinstance(ty, SpecType):
            spec = lookup_spec(specs, ty.name)
            if isinstance(spec, TypeSpec):
                yield from visit(spec.ty)
                return
            elif isinstance(spec, EnumSpec):
                for var in spec.members:
                    yield from visit(var.ty)
                return
        yield ty
    types = list(visit(ty))
    if cycle:
        # expanding a cyclic type leads to infinity
        # we prevent this by making the type invalid
        return NeverType()
    if len(types) == 1:
        return types[0]
    return UnionType(types)


@lru_cache
def are_types_equal(left: Type, right: Type, *, specs: Specs) -> bool:
    """
    Check whether the two given types are syntactically equivalent.
    """
    def visit(left: Type, right: Type) -> bool:
        if isinstance(left, NeverType) or isinstance(right, NeverType):
            return True
        if isinstance(left, AnyType) or isinstance(right, AnyType):
            return True
        if isinstance(left, NoneType) and isinstance(right, NoneType):
            return True
        if isinstance(left, ExternType) and isinstance(right, ExternType):
            return left.name == right.name
        if isinstance(left, SpecType) and isinstance(right, SpecType):
            return left.name == right.name
        if isinstance(left, ListType) and isinstance(right, ListType):
            return visit(left.element_type, right.element_type)
        if isinstance(left, PunctType) and isinstance(right, ListType):
            return visit(left.element_type, right.element_type) \
               and visit(left.element_type, right.element_type)
        if isinstance(left, TupleType) and isinstance(right, TupleType):
            if len(left.element_types) != len(right.element_types):
                return False
            for a, b in zip(left.element_types, right.element_types):
                if not visit(a, b):
                    return False
            return True
        if isinstance(left, UnionType) and isinstance(right, UnionType):
            if len(left.types) != len(right.types):
                return False
            left.types.sort()
            right.types.sort()
            for l, r in zip(left.types, right.types):
                if not visit(l, r):
                    return False
            return True
        return False
    return visit(left, right)


@lru_cache
def is_type_assignable(left: Type, right: Type, *, specs: Specs) -> bool:
    """
    Check whether `right` is assignable to `left`, as in the Python expression `left = right`.
    """
    visited_left = set[str]()
    visited_right = set[str]()
    def visit(left: Type, right: Type) -> bool:
        left = resolve_type_aliases(left, specs=specs)
        right = resolve_type_aliases(right, specs=specs)
        if isinstance(left, NeverType) or isinstance(right, NeverType):
            return False
        if isinstance(left, AnyType) or isinstance(right, AnyType):
            return True
        if isinstance(left, NoneType) and isinstance(right, NoneType):
            return True
        if isinstance(left, ExternType) and isinstance(right, ExternType):
            return left.name == right.name
        if isinstance(left, SpecType) and isinstance(right, SpecType):
            if left.name == right.name:
                return True
            if left.name in visited_left or right.name in visited_right: # cycle detected
                return False # infinite types are never assignable
            visited_left.add(left.name)
            visited_right.add(right.name)
            left_spec = lookup_spec(specs, left.name)
            right_spec = lookup_spec(specs, right.name)
            has_enum = False
            if isinstance(left_spec, EnumSpec):
                left = UnionType(list(var.ty for var in left_spec.members))
                has_enum = True
            if isinstance(right_spec, EnumSpec):
                right = UnionType(list(var.ty for var in right_spec.members))
                has_enum = True
            if has_enum:
                return visit(left, right)
            return False
        if isinstance(left, TupleType) and isinstance(right, TupleType):
            if len(left.element_types) != len(right.element_types):
                return False
            for a, b in zip(left.element_types, right.element_types):
                if not visit(a, b):
                    return False
            return True
        if isinstance(left, ListType) and isinstance(right, ListType):
            return visit(left.element_type, right.element_type)
        if isinstance(left, PunctType) and isinstance(right, ListType):
            return visit(left.element_type, right.element_type) \
               and visit(left.element_type, right.element_type)
        if isinstance(left, UnionType) or isinstance(right, UnionType):
            left_els = list(left.types if isinstance(left, UnionType) else [ left ])
            right_els = list(right.types if isinstance(right, UnionType) else [ right ])
            for r in right_els:
                found = False
                for l in left_els:
                    if visit(l, r):
                        found = True
                        break
                if not found:
                    return False
            return True
        return False
    return visit(left, right)


def resolve_type_aliases(ty: Type, *, specs: Specs) -> Type:
    while isinstance(ty, SpecType):
        spec = lookup_spec(specs, ty.name)
        if not isinstance(spec, TypeSpec):
            break
        ty = spec.ty
    return ty


def get_child_types(ty: Type, *, specs: Specs) -> Iterable[Type]:
    """
    Get the all the types that are structurally direct children of the given type.

    This method will also expand types holding an EnumSpec, TypeSpec and a
    NodeSpec. In the first case, the types of the individual variants will be
    further inspected. In the second case the types of the node's fields will
    be returned.
    """
    visited = set[Type]()
    def visit(ty: Type) -> Iterable[Type]:
        # FIXME this will make types unique
        if ty in visited: # cycle detected
            return
        visited.add(ty)
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
        elif isinstance(ty, SpecType):
            spec = lookup_spec(specs, ty.name)
            if isinstance(spec, EnumSpec):
                for variant in spec.members:
                    yield from visit(variant.ty)
            elif isinstance(spec, NodeSpec):
                for field in spec.fields:
                    yield field.ty
            elif isinstance(spec, TypeSpec):
                yield from visit(spec.ty)
    return visit(ty)

@lru_cache
def contains_type(ty: Type, needle: Type, *, specs: Specs) -> bool:
    """
    Check whether any part of `ty` is assignable to `target`.
    """
    visited = set[Type]()
    def visit(ty: Type) -> bool:
        if ty in visited: # cycle or duplicate detected
            return False
        visited.add(ty)
        # We check whether needle is assignable to ty and not the reverse
        # because ty may contain types other than needle. A narrower union type
        # may be assigned to a wider union type, but not the reverse.
        if is_type_assignable(ty, needle, specs=specs):
            return True
        for child in get_child_types(ty, specs=specs):
            if visit(child):
                return True
        return False
    return visit(ty)


@lru_cache
def is_recursive(ty: Type, *, specs: Specs) -> bool:
    """
    Determine whether a declaration references itself eventually though one of its members.

    This is also known in functional programming literature as a recursive datatype.
    """
    for child in get_child_types(ty, specs=specs):
        if contains_type(child, ty, specs=specs):
            return True
    return False


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
    if isinstance(ty, ListType) and isinstance(ty.element_type, ExternType) and ty.element_type.name == string_rule_type:
        return ty.element_type
    return rewrite_each_child_type(ty, normalize_type)


def merge_similar_types(ty: Type) -> Type:
    """
    Merges the elements of similarly structured types to a single type.

    For example, the type `List[int] | List[str]` becomes `List[int | str]`.

    Note that this is semantically incorrect, but some (mostly dynamic)
    programming languages can use this to write less intensive checks for a
    value of this type.
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
    # must call `simplify_type`.
    return normalize_type(UnionType(types))
