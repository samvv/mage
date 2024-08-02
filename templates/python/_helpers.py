
from __future__ import annotations

# TODO Generate a union type with all nodes/tokens

from functools import _lru_cache_wrapper
from typing import Iterable, Iterator, Sequence, assert_never, TypeVar, cast

import templaty
from sweetener import is_iterator, warn
from magelang.repr import *
from magelang.util import NameGenerator
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit

ctx = templaty.load_context()

grammar = cast(Grammar, ctx['grammar'])
prefix = cast(str, ctx['prefix'])

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def namespace(name: str) -> str:
    return prefix + name if prefix else name

def to_class_name(name: str) -> str:
    return to_camel_case(namespace(name))

type Case = tuple[PyExpr | None, list[PyStmt]]

is_node_name = f'is_{prefix}node'
is_token_name = f'is_{prefix}token'
is_syntax_name = f'is_{prefix}syntax'
for_each_child_name = f'for_each_{prefix}child'

node_class_name = to_class_name('node')
token_class_name = to_class_name('token')
syntax_class_name = to_class_name('syntax')

T = TypeVar('T', covariant=True)

def list_comma(it: Iterator[T] | Sequence[T]) -> list[tuple[T, PyComma | None]]:
    if not is_iterator(it):
        it = iter(it)
    out: list[tuple[T, PyComma | None]] = []
    prev: T | None = None
    while True:
        try:
            curr = next(it)
        except StopIteration:
            if prev is not None:
                out.append((prev, None))
            break
        if prev is not None:
            out.append((prev, PyComma()))
        prev = curr
    return out

def build_cond(cases: list[Case]) -> list[PyStmt]:
    if len(cases) == 0:
        return []
    test, body = cases[0]
    if len(cases) == 1 and test is None:
        return body
    assert(test is not None)
    first = PyIfCase(test=test, body=body)
    alternatives: list[PyElifCase] = []
    last = None
    for test, body in cases[1:]:
        if test is None:
            last = PyElseCase(body=body)
            break
        alternatives.append(PyElifCase(test=test, body=body))
    return [ PyIfStmt(first=first, alternatives=alternatives, last=last) ]

def build_is_none(value: PyExpr) -> PyExpr:
    return PyInfixExpr(
        left=value,
        op='is',
        right=PyNamedExpr(name='None')
    )

def build_infix(it: Iterable[PyExpr] | Iterator[PyExpr], op: str, init: PyExpr) -> PyExpr:
    if not is_iterator(it):
        it = iter(it)
    try:
        out = next(it)
    except StopIteration:
        return init
    for expr in it:
        out = PyInfixExpr(left=out, op=op, right=expr)
    return out

def build_or(iter: Iterable[PyExpr]) -> PyExpr:
    return build_infix(iter, 'or', PyNamedExpr(name='False'))

def build_and(iter: Iterable[PyExpr]) -> PyExpr:
    return build_infix(iter, 'and', PyNamedExpr(name='True'))

def build_union(it: list[PyExpr] | Iterator[PyExpr]) -> PyExpr:
    return build_infix(it, '|', PyNamedExpr(name='Never'))

def build_isinstance(expr: PyExpr, ty: PyExpr) -> PyExpr:
    return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=expr), PyPosArg(expr=ty) ]))

specs = grammar_to_specs(grammar)

def gen_py_type(ty: Type) -> PyExpr:
    if isinstance(ty, NodeType):
        return PyNamedExpr(name=to_class_name(ty.name))
    if isinstance(ty, TokenType):
        return PyNamedExpr(name=to_class_name(ty.name))
    if isinstance(ty, ListType):
        return PySubscriptExpr(expr=PyNamedExpr(name='list'), slices=list_comma([ gen_py_type(ty.element_type) ]))
    if isinstance(ty, PunctType):
        return PySubscriptExpr(expr=PyNamedExpr(name='Punctuated'), slices=list_comma([ gen_py_type(ty.element_type), gen_py_type(ty.separator_type) ]))
    if isinstance(ty, TupleType):
        return PySubscriptExpr(expr=PyNamedExpr(name='tuple'), slices=list_comma(gen_py_type(element) for element in ty.element_types))
    if isinstance(ty, UnionType):
        out = gen_py_type(ty.types[0])
        for element in ty.types[1:]:
            out = PyInfixExpr(left=out, op='|', right=gen_py_type(element))
        return out
    if isinstance(ty, ExternType):
        return rule_type_to_py_type(ty.name)
    if isinstance(ty, NoneType):
        return PyNamedExpr(name='None')
    if isinstance(ty, NeverType):
        return PyNamedExpr(name='Never')
    raise RuntimeError(f'unexpected {ty}')

def rule_type_to_py_type(type_name: str) -> PyExpr:
    if type_name == 'String':
        return PyNamedExpr(name='str')
    if type_name == 'Integer':
        return PyNamedExpr(name='int')
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyNamedExpr(name='float')
    if type_name == 'Float' or type_name == 'Float64':
        return PyNamedExpr(name='float')
    raise RuntimeError(f"unexpected rule type '{type_name}'")

def is_optional(ty: Type) -> bool:
    # if isinstance(ty, NoneType):
    #     return True
    if isinstance(ty, UnionType):
        for element in flatten_union(ty):
            if isinstance(element, NoneType):
                return True
    return False

def gen_instance_check(name: str, target: PyExpr) -> PyExpr:
    spec = specs.lookup(name)
    if isinstance(spec, VariantSpec):
        return PyCallExpr(operator=PyNamedExpr(name=f'is_{namespace(name)}'), args=list_comma([ PyPosArg(expr=target) ]))
    if isinstance(spec, NodeSpec) or isinstance(spec, TokenSpec):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name=to_class_name(name))) ]))
    raise RuntimeError(f'unexpected {spec}')

def gen_shallow_test(ty: Type, target: PyExpr) -> PyExpr:
    if isinstance(ty, NodeType):
        return gen_instance_check(ty.name, target)
    if isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name=to_class_name(ty.name))) ]))
    if isinstance(ty, NoneType):
        return build_is_none(target)
    if isinstance(ty, TupleType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='tuple')) ]))
        #return ast.BoolOp(left=test, op=ast.And(), values=[ make_and(gen_test(element, ast.Subscript(target, ast.Constant(i))) for i, element in enumerate(ty.element_types)) ])
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='list')) ]))
    if isinstance(ty, PunctType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='Punctuated')) ]))
    if isinstance(ty, UnionType):
        return build_or(gen_shallow_test(element, target) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    if isinstance(ty, NeverType):
        return PyNamedExpr(name='False')
    raise RuntimeError(f'unexpected {ty}')

def gen_rule_type_test(type_name: str, target: PyExpr) -> PyExpr:
    if type_name == 'String':
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='str')) ]))
    if type_name == 'Integer':
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='int')) ]))
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='float')) ]))
    if type_name == 'Float' or type_name == 'Float64':
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyPosArg(expr=target), PyPosArg(expr=PyNamedExpr(name='float')) ]))
    raise RuntimeError(f"unexpected rule type '{type_name}'")


def cst() -> str:

    def is_default_constructible(ty: Type, allow_empty_sequences: bool = True) -> bool:
        if isinstance(ty, ListType):
            return allow_empty_sequences
        if isinstance(ty, PunctType):
            return allow_empty_sequences
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, NodeType):
            spec = specs.lookup(ty.name)
            if not isinstance(spec, NodeSpec): # if it's a VariantSpec
                return False
            return all(is_default_constructible(field.ty, allow_empty_sequences) for field in spec.members)
        if isinstance(ty, TokenType):
            spec = specs.lookup(ty.name)
            assert(isinstance(spec, TokenSpec))
            return spec.is_static
        if isinstance(ty, TupleType):
            return all(is_default_constructible(element, False) for element in ty.element_types)
        if isinstance(ty, UnionType):
            counter = 0
            for element_type in ty.types:
                if is_default_constructible(element_type, allow_empty_sequences):
                    counter += 1
            return counter == 1
        raise RuntimeError(f'unexpected {ty}')

    def gen_default_constructor(ty: Type) -> PyExpr:
        if isinstance(ty, NoneType):
            return PyNamedExpr(name='None')
        if isinstance(ty, NodeType) or isinstance(ty, TokenType):
            return PyCallExpr(operator=PyNamedExpr(name=to_class_name(ty.name)))
        if isinstance(ty, ListType):
            return PyCallExpr(operator=PyNamedExpr(name='list'))
        if isinstance(ty, PunctType):
            # FIXME maybe add the generic arguments?
            return PyCallExpr(operator=PyNamedExpr(name='Punctuated'))
        if isinstance(ty, TupleType):
            return PyTupleExpr(elements=list_comma(gen_default_constructor(element_type) for element_type in ty.element_types))
        if isinstance(ty, UnionType):
            # This assumes we already detected that there is exactly one
            # default-constrcuctible member in the union type
            for ty in ty.types:
                if is_default_constructible(ty):
                    return gen_default_constructor(ty)
        raise RuntimeError(f'unexpected {ty}')

    def gen_initializers(field_name: str, field_type: Type, in_name: str, assign: Callable[[PyExpr], PyStmt]) -> tuple[Type, list[PyStmt]]:

        def collect(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], has_none: bool) -> tuple[Type, list[PyStmt]]:
            cases: list[Case] = []
            types: list[Type] = []
            for coerce_ty, coerce_body in coercions(ty, in_name, assign, has_none):
                cases.append((gen_shallow_test(coerce_ty, PyNamedExpr(name=in_name)), coerce_body))
                types.append(coerce_ty)

            res_ty = simplify_type(UnionType(types))

            # For very simple fields, there's no need to do any checks. We
            # assume the type checker catches whatever error the user makes.
            if len(cases) == 1:
                return res_ty, cases[0][1]

            cases.append((
                None,
                [
                    PyRaiseStmt(
                        expr=PyCallExpr(
                            operator=PyNamedExpr(name='ValueError'),
                            args=list_comma([ PyPosArg(expr=PyConstExpr(literal=f"the field '{field_name}' received an unrecognised value'")) ])
                        )
                    )
                ]
            ))

            return res_ty, build_cond(cases)

        def coercions(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], has_none: bool) -> Generator[tuple[Type, list[PyStmt]], None, None]:

            if isinstance(ty, UnionType):

                types = list(flatten_union(ty))

                for member_ty in types:
                    if isinstance(member_ty, NoneType):
                        has_none = True

                for member_ty in types:
                    yield from coercions(member_ty, in_name, assign, has_none)

                return

            if isinstance(ty, NoneType):
                yield NoneType(), [ assign(PyNamedExpr(name='None')) ]
                return

            # Now that we've handled union types and empty types, we can
            # attempt to construct the type from a certain default value.
            # This can only happen if `None` is not already used by the type
            # itself. We continue processing the other types after this
            # operation.
            if not has_none and is_default_constructible(ty):
                yield NoneType(), [ assign(gen_default_constructor(ty)) ]

            if isinstance(ty, NodeType):

                spec = specs.lookup(ty.name)

                # spec can also be a VariantSpec so we need to run isinstance
                if isinstance(spec, NodeSpec) and len(spec.members) == 1 and not has_none:
                    # TODO maybe also coerce spec.members[0].ty recursively?
                    single_ty = spec.members[0].ty
                    yield single_ty, [
                        assign(
                            PyCallExpr(
                                operator=PyNamedExpr(name=to_class_name(ty.name)),
                                args=list_comma([ PyPosArg(expr=PyNamedExpr(name=in_name)) ])
                            )
                        )
                    ]

                yield ty, [ assign(PyNamedExpr(name=in_name)) ]

                return

            if isinstance(ty, TokenType):

                spec = specs.lookup(ty.name)
                assert(isinstance(spec, TokenSpec))

                # If a token is not static, like an identifier or a string,
                # then we might be able to coerce the token based on the data
                # that it wraps.
                if not spec.is_static:

                    yield ExternType(spec.field_type), [
                        assign(
                            PyCallExpr(
                                operator=PyNamedExpr(name=to_class_name(ty.name)),
                                args=list_comma([ PyPosArg(expr=PyNamedExpr(name=in_name)) ])
                            )
                        )
                    ]

                yield ty, [ assign(PyNamedExpr(name=in_name)) ]

                return

            if isinstance(ty, PunctType):

                new_elements_name = f'new_{in_name}'
                first_element_name = f'first_{in_name}_element'
                second_element_name = f'second_{in_name}_element'
                element_name = f'{in_name}_element'
                elements_iter_name = f'{in_name}_iter'
                value_name = f'{in_name}_value'
                new_value_name = f'new_{in_name}_value'
                separator_name = f'{in_name}_separator'
                new_separator_name = f'new_{in_name}_separator'

                value_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_value_name: PyAssignStmt(pattern=PyNamedPattern(name=name), expr=value)
                value_type, value_stmts = collect(ty.element_type, value_name, value_assign, False)

                separator_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_separator_name: PyAssignStmt(pattern=PyNamedPattern(name=name), expr=value)
                separator_type, separator_stmts = collect(ty.separator_type, separator_name, separator_assign, False)

                coerced_ty = UnionType([
                    ListType(value_type),
                    ListType(TupleType([ value_type, make_optional(separator_type) ])),
                    PunctType(value_type, separator_type),
                ])

                yield coerced_ty, [
                    PyAssignStmt(
                        pattern=PyNamedPattern(name=new_elements_name),
                        expr=PyCallExpr(operator=PyNamedExpr(name='Punctuated'))
                    ),
                    PyAssignStmt(
                        pattern=PyNamedPattern(name=elements_iter_name),
                        expr=PyCallExpr(operator=PyNamedExpr(name='iter'), args=list_comma([ PyPosArg(expr=PyNamedExpr(name=in_name)) ])),
                    ),
                    PyTryStmt(
                        body=[
                            PyAssignStmt(
                                pattern=PyNamedPattern(name=first_element_name),
                                expr=PyCallExpr(operator=PyNamedExpr(name='next'), args=list_comma([ PyPosArg(expr=PyNamedExpr(name=elements_iter_name)) ]))
                            ),
                            PyWhileStmt(
                                expr=PyNamedExpr(name='True'),
                                body=[
                                    PyTryStmt(
                                        body=[
                                            PyAssignStmt(
                                                pattern=PyNamedPattern(name=second_element_name),
                                                expr=PyCallExpr(operator=PyNamedExpr(name='next'), args=list_comma([ PyPosArg(expr=PyNamedExpr(name=elements_iter_name)) ]))
                                            ),
                                            *build_cond([
                                                (
                                                    # FIXME does not handle nested tuples
                                                    build_isinstance(PyNamedExpr(name=first_element_name), PyNamedExpr(name='tuple')),
                                                    [
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(name=value_name),
                                                            expr=PySubscriptExpr(expr=PyNamedExpr(name=first_element_name), slices=list_comma([ PyConstExpr(literal=0) ])),
                                                        ),
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(name=separator_name),
                                                            expr=PySubscriptExpr(expr=PyNamedExpr(name=first_element_name), slices=list_comma([ PyConstExpr(literal=1) ])),
                                                        ),
                                                    ]
                                                ),
                                                (
                                                    None,
                                                    [
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(name=value_name),
                                                            expr=PyNamedExpr(name=first_element_name),
                                                        ),
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(name=separator_name),
                                                            expr=PyNamedExpr(name='None'),
                                                        ),
                                                    ]
                                                )
                                            ]),
                                            *value_stmts,
                                            *separator_stmts,
                                            PyExprStmt(
                                                expr=PyCallExpr(
                                                    operator=PyAttrExpr(expr=PyNamedExpr(name=new_elements_name), name='append'),
                                                    args=list_comma([
                                                        PyPosArg(expr=PyNamedExpr(name=new_value_name)),
                                                        PyPosArg(expr=PyNamedExpr(name=new_separator_name))
                                                    ])
                                                )
                                            ),
                                            PyAssignStmt(
                                                pattern=PyNamedPattern(name=first_element_name),
                                                expr=PyNamedExpr(name=second_element_name),
                                            ),
                                        ],
                                        handlers=[
                                            PyExceptHandler(
                                                expr=PyNamedExpr(name='StopIteration'),
                                                body=[
                                                    *build_cond([
                                                        (
                                                            # FIXME does not handle nested tuples
                                                            build_isinstance(PyNamedExpr(name=first_element_name), PyNamedExpr(name='tuple')),
                                                            [
                                                                PyAssignStmt(
                                                                    pattern=PyNamedPattern(name=value_name),
                                                                    expr=PySubscriptExpr(expr=PyNamedExpr(name=first_element_name), slices=list_comma([ PyConstExpr(literal=0) ])),
                                                                ),
                                                                PyExprStmt(
                                                                    expr=PyCallExpr(
                                                                        operator=PyNamedExpr(name='assert'),
                                                                        args=list_comma([ PyPosArg(expr=build_is_none(PySubscriptExpr(expr=PyNamedExpr(name=first_element_name), slices=list_comma([ PyConstExpr(literal=1) ])))) ])
                                                                    )
                                                                )
                                                            ]
                                                        ),
                                                        (
                                                            None,
                                                            [
                                                                PyAssignStmt(
                                                                    pattern=PyNamedPattern(name=value_name),
                                                                    expr=PyNamedExpr(name=first_element_name),
                                                                )
                                                            ]
                                                        )
                                                    ]),
                                                    *value_stmts,
                                                    PyExprStmt(
                                                        expr=PyCallExpr(
                                                            operator=PyAttrExpr(expr=PyNamedExpr(name=new_elements_name), name='append'),
                                                            args=list_comma([ PyPosArg(expr=PyNamedExpr(name=new_value_name)) ])
                                                        )
                                                    ),
                                                    PyBreakStmt(),
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ],
                        handlers=[
                            PyExceptHandler(
                                expr=PyNamedExpr(name='StopIteration'),
                                body=[ PyPassStmt() ]
                            )
                        ]
                    ),
                    assign(PyNamedExpr(name=new_elements_name))
                ]

                return

            if isinstance(ty, ListType):

                # Generates:
                #
                # out_name = list()
                # for element in in_name:
                #     ...
                #     out_name.append(new_element_name)

                new_elements_name = f'new_{in_name}'
                element_name = f'{in_name}_element'
                new_element_name = f'new_{in_name}_element'

                element_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name=name), expr=value)
                element_type, element_stmts = collect(ty.element_type, element_name, element_assign, False)

                yield ListType(element_type), [
                    PyAssignStmt(
                        pattern=PyNamedPattern(name=new_elements_name),
                        expr=PyCallExpr(operator=PyNamedExpr(name='list'))
                    ),
                    PyForStmt(
                        pattern=PyNamedPattern(name=element_name),
                        expr=PyNamedExpr(name=in_name),
                        body=[
                            *element_stmts,
                            PyExprStmt(
                                expr=PyCallExpr(
                                    operator=PyAttrExpr(
                                        expr=PyNamedExpr(name=new_elements_name),
                                        name='append'
                                    ),
                                    args=list_comma([ PyPosArg(expr=PyNamedExpr(name=new_element_name)) ])
                                )
                            )
                        ]
                    ),
                    assign(PyNamedExpr(name=new_elements_name))
                ]

                return

            if isinstance(ty, TupleType):

                # Generates:
                #
                # element_0 = field[0]
                # new_element_0 = ...
                # ...
                # out_name = (new_element_0, new_element_1, ...)

                required: list[Type] = []

                for element_type in ty.element_types:
                    if not is_default_constructible(element_type, allow_empty_sequences=False):
                        required.append(element_type)

                if len(required) == 1:

                    main_type = required[0]

                    def first_assign(value: PyExpr):
                        assert(isinstance(ty, TupleType)) # Needed to keep Pyright happy
                        # Generates for example: self.field = (Dot(), $value, Dot())
                        return assign(
                            PyTupleExpr(
                                elements=list_comma(value if el_ty == main_type else gen_default_constructor(el_ty) for el_ty in ty.element_types)
                            )
                        )

                    yield from coercions(main_type, in_name, first_assign, True)

                new_elements: list[PyExpr] = []
                new_element_types: list[Type] = []

                # Generates for example: assert(isinstance(in_name, ty))
                orelse: list[PyStmt] = [
                    PyExprStmt(
                        expr=PyCallExpr(
                            operator=PyNamedExpr(name='assert'),
                            args=list_comma([ PyPosArg(expr=gen_shallow_test(ty, PyNamedExpr(name=in_name))) ])
                        )
                    )
                ]

                for i, element_type in enumerate(ty.element_types):

                    element_name = f'{in_name}_{i}'
                    new_element_name = f'new_{in_name}_{i}'
                    element_assign = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name=name), expr=value)

                    new_elements.append(PyNamedExpr(name=new_element_name))

                    orelse.append(
                        PyAssignStmt(
                            pattern=PyNamedPattern(name=element_name),
                            expr=PySubscriptExpr(
                                expr=PyNamedExpr(name=in_name),
                                slices=list_comma([ PyConstExpr(literal=i) ])
                            )
                        )
                    )

                    new_element_type, new_element_stmts = collect(element_type, element_name, element_assign, False)

                    orelse.extend(new_element_stmts)

                    new_element_types.append(new_element_type)

                orelse.append(assign(PyTupleExpr(elements=list_comma(new_elements))))

                yield TupleType(new_element_types), orelse

                return

        return collect(field_type, in_name, assign, False)

    stmts: list[PyStmt] = []

    for spec in specs:

        if isinstance(spec, NodeSpec):

            body: list[PyStmt] = []
            params: list[PyParam] = []
            init_body: list[PyStmt] = []

            for field in spec.members:

                # param_type = get_coerce_type(field.ty)
                # tmp = f'{field.name}__coerced'

                assign: Callable[[PyExpr], PyStmt] = lambda value, field=field: PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern(name='self'), name=field.name), annotation=gen_py_type(field.ty), expr=value)
                param_type, param_init = gen_initializers(field.name, field.ty, field.name, assign)

                init_body.extend(param_init)

                param_type_str = emit(gen_py_type(param_type))
                params.append(PyNamedParam(
                    pattern=PyNamedPattern(name=field.name),
                    annotation=PyConstExpr(literal=param_type_str),
                    default=PyNamedExpr(name='None') if is_optional(param_type) else None
                ))

            # args = ast.arguments(args=[ ast.arg('self') ], kwonlyargs=params, defaults=[], kw_defaults=params_defaults)
            body.append(PyFuncDef(
                name='__init__',
                params=list_comma([ PyNamedParam(pattern=PyNamedPattern(name='self')), PySepParam(), *params ]),
                return_type=PyNamedExpr(name='None'),
                body=init_body
            ))

            #for field in element.members:
            #     body.append(ast.AnnAssign(target=PyNamedExpr(name=field.name), annotation=gen_type(field.ty), simple=True))

            stmts.append(PyClassDef(name=to_class_name(spec.name), bases=list_comma([ '_BaseNode' ]), body=body))

            continue

        if isinstance(spec, TokenSpec):

            body: list[PyStmt] = []

            if spec.is_static:

                body.append(PyPassStmt())

            else:

                init_body: list[PyStmt] = []

                init_body.append(PyExprStmt(expr=PyCallExpr(operator=PyAttrExpr(expr=PyCallExpr(operator=PyNamedExpr(name='super')), name='__init__'), args=[ (PyKeywordArg(name='span', expr=PyNamedExpr(name='span')), None) ])))

                params: list[PyParam] = []
                params.append(PyNamedParam(pattern=PyNamedPattern(name='self')))

                # value: Field | None = None
                params.append(PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=build_union([ rule_type_to_py_type(spec.field_type), PyNamedExpr(name='None') ]), default=PyNamedExpr(name='None')))

                # span: Span | None = None
                params.append(PyNamedParam(pattern=PyNamedPattern(name='span'), annotation=build_union([ PyNamedExpr(name='Span'), PyNamedExpr(name='None') ]), default=PyNamedExpr(name='None')))

                init_body.append(PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern(name='self'), name='value'), expr=PyNamedExpr(name='value')))

                body.append(PyFuncDef(name='__init__', params=list_comma(params), body=init_body))

            stmts.append(PyClassDef(name=to_class_name(spec.name), bases=list_comma([ '_BaseToken' ]), body=body))

            continue

        if isinstance(spec, VariantSpec):
            # ty = PyNamedExpr(name=to_class_case(element.members[0]))
            # for name in element.members[1:]:
            #     ty = ast.BinOp(left=ty, op=ast.BitOr(), right=PyNamedExpr(name=to_class_case(name)))

            cls_name = to_class_name(spec.name)

            assert(len(spec.members) > 0)
            py_type = PyConstExpr(literal=emit(build_union(PyNamedExpr(name=to_class_name(name)) for name in spec.members)))
            stmts.append(PyAssignStmt(pattern=PyNamedPattern(name=cls_name), annotation=PyNamedExpr(name='TypeAlias'), expr=py_type))

            params: list[PyParam] = []
            params.append(PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=PyNamedExpr(name='Any')))
            stmts.append(PyFuncDef(
                name=f'is_{namespace(spec.name)}',
                params=list_comma(params),
                return_type=PySubscriptExpr(expr=PyNamedExpr(name='TypeGuard'), slices=list_comma([ PyNamedExpr(name=cls_name) ])),
                body=[
                    PyRetStmt(expr=build_or(gen_instance_check(name, PyNamedExpr(name='value')) for name in spec.members))
                ],
            ))

            continue

        assert_never(spec)

    node_names: list[str] = []
    token_names: list[str] = []
    for spec in specs:
        if isinstance(spec, TokenSpec):
            token_names.append(spec.name)
        elif isinstance(spec, NodeSpec):
            node_names.append(spec.name)

    # Generates:
    #
    # Token = Comma | Dot | Ident | ...
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(name=token_class_name),
            expr=build_union(PyNamedExpr(name=to_class_name(name)) for name in token_names)
        )
    )

    # Generates:
    #
    # Node = Foo | Bar | ...
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(name=node_class_name),
            expr=build_union(PyNamedExpr(name=to_class_name(name)) for name in node_names)
        )
    )

    # Generates:
    #
    # Syntax = Token | Node
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(name=syntax_class_name),
            expr=build_union([ PyNamedExpr(name=token_class_name), PyNamedExpr(name=node_class_name) ])
        )
    )

    ## Generates:
    ##
    ## def is_token(value: Any) -> TypeGuard[Token]:
    ##     return isinstance(value, _BaseToken)
    #stmts.append(PyFuncDef(
    #    name=is_token_name,
    #    params=list_comma([
    #        PyNamedParam(
    #            pattern=PyNamedPattern(name='value'),
    #            annotation=PyNamedExpr(name='Any')
    #        )
    #    ]),
    #    return_type=PySubscriptExpr(
    #        expr=PyNamedExpr(name='TypeGuard'),
    #        slices=list_comma([ PyNamedExpr(name=token_class_name) ])
    #    ),
    #    body=PyRetStmt(
    #        expr=PyCallExpr(
    #            operator=PyNamedExpr(name='isinstance'),
    #            args=list_comma([
    #                PyPosArg(expr=PyNamedExpr(name='value')),
    #                PyPosArg(expr=PyNamedExpr(name='_BaseToken'))
    #            ])
    #        )
    #    )
    #    # body=PyRetStmt(expr=make_or(PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyNamedExpr(name='value'), PyNamedExpr(name=to_class_name(name)) ])) for name in token_names))
    #))

    ## Generates:
    ##
    ## def is_token(value: Any) -> TypeGuard[Node]:
    ##     return isinstance(value, _BaseNode)
    #stmts.append(PyFuncDef(
    #    name=is_node_name,
    #    params=list_comma([
    #        PyNamedParam(
    #            pattern=PyNamedPattern(name='value'),
    #            annotation=PyNamedExpr(name='Any')
    #        )
    #    ]),
    #    return_type=PySubscriptExpr(
    #        expr=PyNamedExpr(name='TypeGuard'),
    #        slices=list_comma([ PyNamedExpr(name=node_class_name) ])
    #    ),
    #    body=PyRetStmt(
    #        expr=PyCallExpr(
    #            operator=PyNamedExpr(name='isinstance'),
    #            args=list_comma([
    #                PyPosArg(expr=PyNamedExpr(name='value')),
    #                PyPosArg(expr=PyNamedExpr(name='_BaseNode'))
    #            ])
    #        )
    #    )
    #    # body=PyRetStmt(expr=make_or(PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyNamedExpr(name='value'), PyNamedExpr(name=to_class_name(name)) ])) for name in node_names))
    #))

    ## Generates:
    ##
    ## def is_syntax(value: Any) -> TypeGuard[Syntax]:
    ##    return is_token(value) or is_node(value)
    #stmts.append(PyFuncDef(
    #    name=is_syntax_name,
    #    params=list_comma([ PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=PyNamedExpr(name='Any')) ]),
    #    body=PyRetStmt(
    #        expr=PyInfixExpr(
    #             left=PyCallExpr(
    #                operator=PyNamedExpr(name=is_node_name),
    #                args=list_comma([ PyPosArg(expr=PyNamedExpr(name='value')) ])
    #            ),
    #            op='or',
    #            right=PyCallExpr(
    #                operator=PyNamedExpr(name=is_token_name),
    #                args=list_comma([ PyPosArg(expr=PyNamedExpr(name='value')) ])
    #            )
    #        )
    #    )
    #))

    return emit(PyModule(stmts=stmts))

def visitor() -> str:

    generate_temporary = NameGenerator()

    proc_name = 'proc'
    syntax_param_name = 'node'

    def gen_proc_call(ty: Type, target: PyExpr) -> Generator[PyStmt, None, None]:
        if isinstance(ty, NoneType):
            yield PyPassStmt()
            return
        if isinstance(ty, TokenType) or isinstance(ty, NodeType):
            yield PyExprStmt(expr=PyCallExpr(operator=PyNamedExpr(name=proc_name), args=list_comma([ PyPosArg(expr=target) ])))
            return
        if isinstance(ty, TupleType):
            for i, element_type in enumerate(ty.element_types):
                tmp = generate_temporary(prefix='element_')
                yield PyAssignStmt(pattern=PyNamedPattern(name=tmp), expr=PySubscriptExpr(expr=target, slices=list_comma([ PyConstExpr(literal=i) ])))
                yield from gen_proc_call(element_type, PyNamedExpr(name=tmp))
            return
        if isinstance(ty, ListType):
            element_name = generate_temporary(prefix='element_')
            yield PyForStmt(pattern=PyNamedPattern(name=element_name), expr=target, body=list(gen_proc_call(ty.element_type, PyNamedExpr(name=element_name))))
            return
        if isinstance(ty, PunctType):
            element_name = generate_temporary(prefix='element_')
            separator_name = generate_temporary(prefix='separator_')
            yield PyForStmt(
                pattern=PyTuplePattern(
                    elements=list_comma([
                        PyNamedPattern(name=element_name),
                        PyNamedPattern(name=separator_name)
                    ]),
                ),
                expr=target,
                body=list(gen_proc_call(ty.element_type, PyNamedExpr(name=element_name)))
            )
            return
        if isinstance(ty, UnionType):
            cases: list[Case] = []
            for element_type in ty.types:
                cases.append((
                    gen_shallow_test(element_type, target),
                    list(gen_proc_call(element_type, target))
                ))
            cases.append((None, [ PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr(name='ValueError'))) ]))
            yield from build_cond(cases)
            return
        raise RuntimeError(f'unexpected {ty}')

    body: list[PyStmt] = []

    body.append(PyIfStmt(first=PyIfCase(
        test=PyCallExpr(
            operator=PyNamedExpr(name=is_token_name),
            args=list_comma([ PyPosArg(expr=PyNamedExpr(name=syntax_param_name)) ])
        ),
        body=PyRetStmt(),
    )))

    for spec in specs:

        # We're going to start a new scope, so all previous temporary names may be used once again
        generate_temporary.reset()

        if isinstance(spec, TokenSpec):
            continue
        if isinstance(spec, NodeSpec):
            if_body: list[PyStmt] = []
            for field in spec.members:
                if_body.extend(gen_proc_call(field.ty, PyAttrExpr(expr=PyNamedExpr(name=syntax_param_name), name=field.name)))
            if_body.append(PyRetStmt())
            body.append(PyIfStmt(first=PyIfCase(
                test=PyCallExpr(
                    operator=PyNamedExpr(name='isinstance'),
                    args=list_comma([
                        PyPosArg(expr=PyNamedExpr(name=syntax_param_name)),
                        PyPosArg(expr=PyNamedExpr(name=to_class_name(spec.name)))
                    ])
                ),
                body=if_body
            )))
            continue
        if isinstance(spec, VariantSpec):
            continue

        assert_never(spec)

    return emit(PyFuncDef(
        name=for_each_child_name,
        params=list_comma([
            PyNamedParam(
                pattern=PyNamedPattern(name=syntax_param_name),
                annotation=PyNamedExpr(name=syntax_class_name)
            ),
            PyNamedParam(
                pattern=PyNamedPattern(name=proc_name),
                annotation=PySubscriptExpr(expr=PyNamedExpr(name='Callable'), slices=list_comma([ PyListExpr(elements=list_comma([ PyNamedExpr(name=syntax_class_name) ])), PyNamedExpr(name='None') ]))
            )
        ]),
        body=body,
    ))

def lexer_logic() -> str:

    generate_temporary = NameGenerator()

    def make_charset_predicate(element: CharSetElement, target: PyExpr) -> PyExpr:
        if isinstance(element, str):
            return PyInfixExpr(left=target, op='==', right=PyConstExpr(literal=element))
        if isinstance(element, tuple):
            low, high = element
            return PyNestExpr(expr=PyInfixExpr(
                left=PyInfixExpr(
                    left=PyCallExpr(
                        operator=PyNamedExpr(name='ord'),
                        args=list_comma([ PyPosArg(expr=target) ])
                    ),
                    op='>=',
                    right=PyConstExpr(literal=ord(low))
                ),
                op='and',
                right=PyInfixExpr(
                    left=PyCallExpr(
                        operator=PyNamedExpr(name='ord'),
                        args=list_comma([ PyPosArg(expr=target) ])
                    ),
                    op='<=',
                    right=PyConstExpr(literal=ord(high))
                )
            ))
        assert_never(element)

    stmts: list[PyStmt] = []
    i = 0

    def noop() -> list[PyStmt]: return [ PyPassStmt() ]

    def brk() -> list[PyStmt]: return [ PyBreakStmt() ]

    def lex_visit(expr: Expr, rule_name: str, success: Callable[[], list[PyStmt]], fail: Callable[[], list[PyStmt]]) -> list[PyStmt]:

        nonlocal i

        out: list[PyStmt] = []

        if isinstance(expr, LitExpr):
            for ch in expr.text:
                ch_name = f'c_{i}'
                i += 1
                out.append(PyAssignStmt(pattern=PyNamedPattern(name=ch_name), expr=PyCallExpr(operator=PyAttrExpr(expr=PyNamedExpr(name='self'), name='_get_char'))))
                out.extend(build_cond([(
                    PyInfixExpr(left=PyNamedExpr(name=ch_name), op='!=', right=PyConstExpr(literal=ch)),
                    fail()
                )]))

        elif isinstance(expr, SeqExpr):
            def make_chain(n: int) -> list[PyStmt]:
                if n == len(expr.elements):
                    return success()
                return lex_visit(expr.elements[n], rule_name, lambda: make_chain(n+1), fail)
            out.extend(make_chain(0))

        elif isinstance(expr, CharSetExpr):
            ch_name = f'c_{i}'
            i += 1
            out.append(PyAssignStmt(pattern=PyNamedPattern(name=ch_name), expr=PyCallExpr(operator=PyAttrExpr(expr=PyNamedExpr(name='self'), name='_get_char'))))
            out.extend(build_cond([(
                build_or(make_charset_predicate(element, PyNamedExpr(name=ch_name)) for element in expr.elements),
                fail()
            )]))

        elif isinstance(expr, RepeatExpr):

            if expr.min > 0:
                min_body = lex_visit(expr.expr, rule_name, noop, fail)
                out.append(PyForStmt(
                    pattern=PyNamedPattern(name='_'),
                    expr=PyCallExpr(operator=PyNamedExpr(name='range'), args=list_comma([ PyPosArg(expr=PyConstExpr(literal=0)), PyPosArg(expr=PyConstExpr(literal=expr.min)) ])),
                    body=min_body
                ))
            if expr.max > 0:
                if expr.max == POSINF:
                    max_body = lex_visit(expr.expr, rule_name, brk, brk)
                    out.append(PyWhileStmt(expr=PyNamedExpr(name='True'), body=max_body))
                else:
                    max_body = lex_visit(expr.expr, rule_name, brk, brk)
                    out.append(PyForStmt(
                        pattern=PyNamedPattern(name='_'),
                        expr=PyCallExpr(operator=PyNamedExpr(name='range'), args=list_comma([ PyPosArg(expr=PyConstExpr(literal=0)), PyPosArg(expr=PyConstExpr(literal=expr.max - expr.min)) ])),
                        body=max_body
                    ))
                out.extend(success())

        elif isinstance(expr, ChoiceExpr):
            out: list[PyStmt] = []
            def try_next(k: int) -> list[PyStmt]:
                if k == 0:
                    return fail()
                return lex_visit(expr.elements[k], rule_name, success, lambda: try_next(k-1))
            return out

        else:
            raise RuntimeError(f'unexpected {expr}')

        return out

    def make_toplevel_fail(rule_name: str) -> Callable[[], list[PyStmt]]:
        return lambda: [ PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr(name='ScanError'), args=[])) ]

    def make_toplevel_success(rule_name: str) -> Callable[[], list[PyStmt]]:
        return lambda: [ PyRetStmt(expr=PyCallExpr(operator=PyNamedExpr(name=rule_name), args=list_comma([]))) ]


    for rule in grammar.rules:
        if not rule.is_token:
            continue
        if rule.expr is not None:
            stmts.extend(lex_visit(rule.expr, rule.name, make_toplevel_success(rule.name), make_toplevel_fail(rule.name)))

    return emit(PyModule(stmts=stmts))

