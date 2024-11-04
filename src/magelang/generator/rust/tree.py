
from collections.abc import Iterable
from typing import TypeVar, assert_type
from magelang.lang.rust.cst import *
from magelang.logging import warn
from magelang.treespec import *
from magelang.util import get_common_suffix, to_camel_case, unreachable

def make_rust_ident(name: str) -> RustPath:
    return RustPath([ RustPathSegment(name) ])

T = TypeVar('T')

def to_type_name(name: str) -> str:
    return to_camel_case(name)

def external_type_to_rust_type_expr(name: str) -> RustTypeExpr:
    if name == 'String':
        return RustPathTypeExpr(make_rust_ident('String'))
    if name == 'Integer':
        return RustPathTypeExpr(make_rust_ident('i64'))
    unreachable()

def to_rust_type_expr(ty: Type) -> RustTypeExpr:
    assert(not isinstance(ty, AnyType)) # Any types are not supported by the Rust generator
    if is_optional(ty):
        return RustPathTypeExpr(RustPath([ RustPathSegment('Option', args=RustAngleBracketedGenericArguments(args=[
            to_rust_type_expr(get_optional_element(ty)),
        ]))]))
    if isinstance(ty, ExternType):
        return external_type_to_rust_type_expr(ty.name)
    if isinstance(ty, TokenType):
        return RustPathTypeExpr(make_rust_ident(to_type_name(ty.name)))
    if isinstance(ty, VariantType):
        return RustPathTypeExpr(make_rust_ident(to_type_name(ty.name)))
    if isinstance(ty, NodeType):
        return RustPathTypeExpr(make_rust_ident(to_type_name(ty.name)))
    if isinstance(ty, NeverType):
        return RustNeverTypeExpr()
    if isinstance(ty, TupleType):
        return RustTupleTypeExpr(elements=list(to_rust_type_expr(element) for element in ty.element_types))
    if isinstance(ty, ListType):
        return RustPathTypeExpr(RustPath([ RustPathSegment('Vec', args=RustAngleBracketedGenericArguments(args=[
            to_rust_type_expr(ty.element_type),
        ]))]))
    if isinstance(ty, PunctType):
        return RustPathTypeExpr(RustPath([ RustPathSegment('Punctuated', args=RustAngleBracketedGenericArguments(args=[
            to_rust_type_expr(ty.element_type),
            to_rust_type_expr(ty.separator_type),
        ]))]))
    assert_never(ty)

def generate_tree(
    specs: Specs,
    prefix = ''
) -> RustSourceFile:

    items = []

    def list_comma(elements: Iterable[T]) -> list[T | RustComma]:
        it = iter(elements)
        out = []
        try:
            out.append(next(it))
        except StopIteration:
            return []
        while True:
            try:
                el = next(it)
            except StopIteration:
                break
            out.append(RustComma())
            out.append(el)
        return out

    def make_derive(*names) -> RustMeta:
        return RustMetaParenthesized(
            path=make_rust_ident('derive'),
            tokens=list_comma(RustIdent(name) for name in names),
        )

    def drop(name: str, n: int) -> str:
        parts = name.split('_')
        return '_'.join(parts[:len(parts)-n])

    for spec in specs:
        if isinstance(spec, TokenSpec):
            fields = [
                RustField(
                    name='span',
                    type_expr=RustPathTypeExpr(make_rust_ident('Span')),
                ),
            ]
            if not spec.is_static:
                fields.append(
                    RustField(
                        name='value',
                        type_expr=external_type_to_rust_type_expr(spec.field_type),
                    )
                )
            items.append(RustStructItem(
                attrs=[ RustAttr(make_derive('Clone', 'Debug')) ],
                visibility=RustPublic(),
                name=to_type_name(spec.name),
                fields=fields
            ))

        if isinstance(spec, VariantSpec):
            k = len(get_common_suffix(list(name.split('_') for name, _ in spec.members)))
            items.append(RustEnumItem(
                attrs=[ RustAttr(make_derive('Clone', 'Debug')) ],
                visibility=RustPublic(),
                name=to_type_name(spec.name),
                variants=list(RustTupleVariant(to_type_name(drop(name, k)), types=[ to_rust_type_expr(ty) ]) for name, ty in spec.members),
            ))
            items.append(RustImplItem(
                trait=RustPath([ RustPathSegment('From', args=RustAngleBracketedGenericArguments(args=[ RustPathTypeExpr(make_rust_ident(to_type_name(spec.name))) ])) ]),
                type_expr=RustPathTypeExpr(make_rust_ident(spec.name))
            ))

    return RustSourceFile(items=items)
