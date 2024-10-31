
from collections.abc import Generator, Iterable
from typing import TypeVar
from magelang.lang.rust.cst import *
from magelang.treespec import Specs, TokenSpec
from magelang.util import to_camel_case, unreachable

def to_type_name(name: str) -> str:
    return to_camel_case(name)

def make_rust_ident(name: str) -> RustPath:
    return RustPath([ RustPathSegment(name) ])

T = TypeVar('T')

def external_type_to_rust_type_expr(name: str) -> RustTypeExpr:
    if name == 'String':
        return RustPathTypeExpr(make_rust_ident('String'))
    unreachable()

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
                pub_keyword=RustPubKeyword(),
                name=to_type_name(spec.name),
                fields=fields
            ))

    return RustSourceFile(items=items)
