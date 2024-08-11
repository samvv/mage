
from typing import Iterator, Iterable
import marko.inline
from magelang.repr import *
from magelang.lang.python.cst import *
from magelang.logging import warn
from magelang.util import to_camel_case, is_iterator

type Case = tuple[PyExpr | None, list[PyStmt]]

def namespaced(name: str, prefix: str) -> str:
    return prefix + name if prefix else name

def to_class_name(name: str, prefix: str) -> str:
    return to_camel_case(namespaced(name, prefix))

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
        op=PyIsKeyword(),
        right=PyNamedExpr('None')
    )

def build_infix(it: Iterable[PyExpr] | Iterator[PyExpr], op: PyInfixOp, init: PyExpr) -> PyExpr:
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
    return build_infix(iter, PyOrKeyword(), PyNamedExpr('False'))

def build_and(iter: Iterable[PyExpr]) -> PyExpr:
    return build_infix(iter, PyAndKeyword(), PyNamedExpr('True'))

def build_union(it: list[PyExpr] | Iterator[PyExpr]) -> PyExpr:
    return build_infix(it, PyVerticalBar(), PyNamedExpr('Never'))

def build_isinstance(expr: PyExpr, ty: PyExpr) -> PyExpr:
    return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ expr, ty ])

def gen_py_type(ty: Type, prefix: str) -> PyExpr:
    if isinstance(ty, NodeType) or isinstance(ty, VariantType) or isinstance(ty, TokenType):
        return PyNamedExpr(to_class_name(ty.name, prefix))
    if isinstance(ty, ListType):
        return PySubscriptExpr(expr=PyNamedExpr('Sequence'), slices=[ gen_py_type(ty.element_type, prefix) ])
    if isinstance(ty, PunctType):
        return PySubscriptExpr(expr=PyNamedExpr('Punctuated'), slices=[ gen_py_type(ty.element_type, prefix), gen_py_type(ty.separator_type, prefix) ])
    if isinstance(ty, TupleType):
        return PySubscriptExpr(expr=PyNamedExpr('tuple'), slices=list(gen_py_type(element, prefix) for element in ty.element_types))
    if isinstance(ty, UnionType):
        out = gen_py_type(ty.types[0], prefix)
        for element in ty.types[1:]:
            out = PyInfixExpr(left=out, op=PyVerticalBar(), right=gen_py_type(element, prefix))
        return out
    if isinstance(ty, ExternType):
        return rule_type_to_py_type(ty.name)
    if isinstance(ty, NoneType):
        return PyNamedExpr('None')
    if isinstance(ty, NeverType):
        return PyNamedExpr('Never')
    assert_never(ty)

def rule_type_to_py_type(type_name: str) -> PyExpr:
    if type_name == 'String':
        return PyNamedExpr('str')
    if type_name == 'Integer':
        return PyNamedExpr('int')
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyNamedExpr('float')
    if type_name == 'Float' or type_name == 'Float64':
        return PyNamedExpr('float')
    raise AssertionError(f"unexpected rule type '{type_name}'")

def gen_rule_type_test(type_name: str, target: PyExpr) -> PyExpr:
    if type_name == 'String':
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('str') ])
    if type_name == 'Integer':
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('int') ])
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('float') ])
    if type_name == 'Float' or type_name == 'Float64':
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('float') ])
    raise AssertionError(f"unexpected rule type '{type_name}'")

def gen_shallow_test(ty: Type, target: PyExpr, prefix: str) -> PyExpr:
    if isinstance(ty, VariantType):
        return PyCallExpr(operator=PyNamedExpr(f'is_{namespaced(ty.name, prefix)}'), args=[ target ])
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr(to_class_name(ty.name, prefix)) ])
    if isinstance(ty, NoneType):
        return build_is_none(target)
    if isinstance(ty, TupleType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('tuple') ])
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('list') ])
    if isinstance(ty, PunctType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('Punctuated') ])
    if isinstance(ty, UnionType):
        return build_or(gen_shallow_test(element, target, prefix) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    if isinstance(ty, NeverType):
        return PyNamedExpr('False')
    assert_never(ty)

def gen_deep_test(ty: Type, target: PyExpr, *, prefix: str) -> PyExpr:
    if isinstance(ty, VariantType):
        return PyCallExpr(operator=PyNamedExpr(f'is_{namespaced(ty.name, prefix)}'), args=[ target ])
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr(to_class_name(ty.name, prefix)) ])
    if isinstance(ty, NoneType):
        return build_is_none(target)
    if isinstance(ty, TupleType):
        return build_and([
            PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('tuple') ]),
            *(gen_deep_test(element, PySubscriptExpr(target, slices=[ PyConstExpr(i) ]), prefix=prefix) for i, element in enumerate(ty.element_types))
        ])
    if isinstance(ty, ListType):
        return PyInfixExpr(
            left=PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('list') ]),
            op=PyAndKeyword(),
            right=PyCallExpr(
                PyNamedExpr('all'),
                args=[
                    PyGeneratorExpr(
                        gen_deep_test(ty.element_type, PyNamedExpr('element'), prefix=prefix),
                        generators=[ PyComprehension(PyNamedPattern('element'), target) ]
                    )
                ]
            ),
        )
    if isinstance(ty, PunctType):
        return PyInfixExpr(
            left=PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('Punctuated') ]),
            op=PyAndKeyword(),
            right=PyCallExpr(
                PyNamedExpr('all'),
                args=[
                    PyGeneratorExpr(
                        gen_deep_test(ty.element_type, PyNamedExpr('element'), prefix=prefix),
                        generators=[ PyComprehension(PyNamedPattern('element'), target) ]
                    )
                ]
            ),
        )
    if isinstance(ty, UnionType):
        return build_or(gen_deep_test(element, target, prefix=prefix) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    if isinstance(ty, NeverType):
        return PyNamedExpr('False')
    assert_never(ty)


def get_marko_element_text(el: Any) -> str:
    if isinstance(el, marko.inline.RawText):
        out = ''
        for child in el.children:
            out += child
        return out
    else:
        raise NotImplementedError()

def is_default_constructible(ty: Type, *, specs: Specs, allow_empty_sequences: bool = True) -> bool:
    visited = set()
    def visit(ty: Type, allow_empty_sequences: bool) -> bool:
        if isinstance(ty, ExternType):
            return False
        if isinstance(ty, NeverType):
            return False
        if isinstance(ty, ListType):
            return allow_empty_sequences and not ty.required
        if isinstance(ty, PunctType):
            return allow_empty_sequences and not ty.required
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, VariantType):
            return False
        if isinstance(ty, NodeType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = specs.lookup(ty.name)
            assert(isinstance(spec, NodeSpec))
            return all(visit(field.ty, allow_empty_sequences) for field in spec.members)
        if isinstance(ty, TokenType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = specs.lookup(ty.name)
            assert(isinstance(spec, TokenSpec))
            return spec.is_static
        if isinstance(ty, TupleType):
            return all(visit(element, False) for element in ty.element_types)
        if isinstance(ty, UnionType):
            # We assume the type has been simplified, such that singleton
            # union types do not occur. Otherwise, we did have to recurse
            # on the single union type member.
            return False
        assert_never(ty)
    return visit(ty, allow_empty_sequences)

def gen_default_constructor(ty: Type, *, specs: Specs, prefix: str) -> PyExpr:
    assert(is_default_constructible(ty, specs=specs))
    if isinstance(ty, NoneType):
        return PyNamedExpr('None')
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr(to_class_name(ty.name, prefix)))
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr('list'))
    if isinstance(ty, PunctType):
        # FIXME maybe add the generic arguments?
        return PyCallExpr(operator=PyNamedExpr('Punctuated'))
    if isinstance(ty, TupleType):
        return PyTupleExpr(elements=list(gen_default_constructor(element_type, specs=specs, prefix=prefix) for element_type in ty.element_types))
    if isinstance(ty, UnionType):
        # This assumes we already detected that there is exactly one
        # default-constrcuctible member in the union type
        for ty in flatten_union(ty):
            if is_default_constructible(ty, specs=specs):
                return gen_default_constructor(ty, specs=specs, prefix=prefix)
    raise RuntimeError(f'unexpected {ty}')

def merge_similar_types(ty: Type) -> Type:
    types = []
    list_element_types = []
    list_required = True
    punct_value_types = []
    punct_sep_types = []
    punct_required = True
    # TODO merge tuples of same length
    for ty_2 in flatten_union(ty):
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
            types.append(ty_2)
    if list_element_types:
        types.append(ListType(UnionType(list_element_types), list_required))
    if punct_value_types or punct_sep_types:
        assert(punct_value_types)
        assert(punct_sep_types)
        types.append(PunctType(UnionType(punct_value_types), UnionType(punct_sep_types), punct_required))
    return simplify_type(UnionType(types))

def gen_initializers(field_name: str, field_type: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], *, specs: Specs, prefix: str) -> tuple[Type, list[PyStmt]]:

    def collect(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], forbid_none: bool) -> tuple[Type, list[PyStmt]]:

        cases: list[Case] = []
        types: list[Type] = []
        for coerce_ty, coerce_body in coercions(ty, in_name, assign, forbid_none):
            cases.append((gen_shallow_test(coerce_ty, PyNamedExpr(in_name), prefix), coerce_body))
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
                        operator=PyNamedExpr('ValueError'),
                        args=[ PyConstExpr(f"the field '{field_name}' received an unrecognised value'") ]
                    )
                )
            ]
        ))

        return res_ty, build_cond(cases)

    def coercions(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], forbid_none: bool) -> Generator[tuple[Type, list[PyStmt]], None, None]:

        if isinstance(ty, UnionType):

            types = list(flatten_union(ty))

            for element_type in types:
                if isinstance(element_type, NoneType):
                    forbid_none = True

            rejected = set()
            out = []
            for element_type in types:
                for coerced_type, coerced_stmts in coercions(element_type, in_name, assign, True):
                    for i, (ty, _) in enumerate(out):
                        if do_types_shallow_overlap(ty, coerced_type):
                            rejected.add(i)
                            continue
                    out.append((coerced_type, coerced_stmts))

            for i, (ty, stmts) in enumerate(out):
                if i in rejected:
                    continue
                yield ty, stmts

            return

        if isinstance(ty, NoneType):
            yield NoneType(), [ assign(gen_default_constructor(ty, specs=specs, prefix=prefix)) ]
            return

        # Now that we've handled union types and empty types, we can
        # attempt to construct the type from a certain default value.
        # This can only happen if `None` is not already used by the type
        # itself. We continue processing the other types after this
        # operation.
        if not forbid_none and is_default_constructible(ty, specs=specs):
            yield NoneType(), [ assign(gen_default_constructor(ty, specs=specs, prefix=prefix)) ]

        if isinstance(ty, VariantType):
            yield ty, [ assign(PyNamedExpr(in_name)) ]
            return

        if isinstance(ty, NodeType):

            spec = specs.lookup(ty.name)
            assert(isinstance(spec, NodeSpec))

            optional_fields: list[Field] = []
            required_fields: list[Field] = []

            for field in spec.members:
                if is_default_constructible(field.ty, specs=specs):
                    optional_fields.append(field)
                else:
                    required_fields.append(field)

            if len(required_fields) == 0:

                if not forbid_none:
                    yield NoneType(), [
                        assign(PyCallExpr(PyNamedExpr(to_class_name(ty.name, prefix))))
                    ]

            elif len(required_fields) == 1:

                required_type = required_fields[0].ty

                def new_assign(value):
                    return assign(
                        PyCallExpr(
                            operator=PyNamedExpr(to_class_name(ty.name, prefix)),
                            args=[ value ]
                        )
                    )

                yield from coercions(required_type, in_name, new_assign, forbid_none)

            yield ty, [ assign(PyNamedExpr(in_name)) ]

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
                            operator=PyNamedExpr(to_class_name(ty.name, prefix)),
                            args=[ PyNamedExpr(in_name) ]
                        )
                    )
                ]

            yield ty, [ assign(PyNamedExpr(in_name)) ]

            return

        if isinstance(ty, PunctType):

            assert(is_default_constructible(ty.separator_type, specs=specs))

            new_elements_name = f'new_{in_name}'

            if is_static(ty.element_type, specs=specs):
                yield ExternType(integer_rule_type), [
                    PyAssignStmt(PyNamedPattern(new_elements_name), expr=PyCallExpr(PyNamedExpr('Punctuated'))),
                    PyForStmt(PyNamedPattern('_'), PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyNamedExpr(in_name) ]), body= [
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(new_elements_name), 'append'), args=[ gen_default_constructor(ty.element_type, specs=specs, prefix=prefix) ])),
                    ]),
                    assign(PyNamedExpr(new_elements_name)),
                ]

            first_element_name = f'first_{in_name}_element'
            second_element_name = f'second_{in_name}_element'
            element_name = f'{in_name}_element'
            elements_iter_name = f'{in_name}_iter'
            value_name = f'{in_name}_value'
            new_value_name = f'new_{in_name}_value'
            separator_name = f'{in_name}_separator'
            new_separator_name = f'new_{in_name}_separator'

            value_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_value_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)
            value_type, value_stmts = collect(ty.element_type, value_name, value_assign, True)

            separator_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_separator_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)
            separator_type, separator_stmts = collect(ty.separator_type, separator_name, separator_assign, True)

            coerced_ty = UnionType([
                ListType(value_type, ty.required),
                ListType(TupleType([ value_type, make_optional(separator_type) ]), ty.required),
                PunctType(value_type, make_optional(separator_type), ty.required),
            ])

            yield coerced_ty, [
                PyAssignStmt(
                    pattern=PyNamedPattern(new_elements_name),
                    expr=PyCallExpr(operator=PyNamedExpr('Punctuated'))
                ),
                PyAssignStmt(
                    pattern=PyNamedPattern(elements_iter_name),
                    expr=PyCallExpr(operator=PyNamedExpr('iter'), args=[ PyNamedExpr(in_name) ]),
                ),
                PyTryStmt(
                    body=[
                        PyAssignStmt(
                            pattern=PyNamedPattern(first_element_name),
                            expr=PyCallExpr(operator=PyNamedExpr('next'), args=[ PyNamedExpr(elements_iter_name) ])
                        ),
                        PyWhileStmt(
                            expr=PyNamedExpr('True'),
                            body=[
                                PyTryStmt(
                                    body=[
                                        PyAssignStmt(
                                            pattern=PyNamedPattern(second_element_name),
                                            expr=PyCallExpr(operator=PyNamedExpr('next'), args=[ PyNamedExpr(elements_iter_name) ])
                                        ),
                                        *build_cond([
                                            (
                                                # FIXME does not handle nested tuples
                                                build_isinstance(PyNamedExpr(first_element_name), PyNamedExpr('tuple')),
                                                [
                                                    PyAssignStmt(
                                                        pattern=PyNamedPattern(value_name),
                                                        expr=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(literal=0) ]),
                                                    ),
                                                    PyAssignStmt(
                                                        pattern=PyNamedPattern(separator_name),
                                                        expr=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(literal=1) ]),
                                                    ),
                                                ]
                                            ),
                                            (
                                                None,
                                                [
                                                    PyAssignStmt(
                                                        pattern=PyNamedPattern(value_name),
                                                        expr=PyNamedExpr(first_element_name),
                                                    ),
                                                    PyAssignStmt(
                                                        pattern=PyNamedPattern(separator_name),
                                                        expr=gen_default_constructor(ty.separator_type, specs=specs, prefix=prefix),
                                                    ),
                                                ]
                                            )
                                        ]),
                                        *value_stmts,
                                        *separator_stmts,
                                        PyExprStmt(
                                            expr=PyCallExpr(
                                                operator=PyAttrExpr(PyNamedExpr(new_elements_name), 'append'),
                                                args=[
                                                    PyNamedExpr(new_value_name),
                                                    PyNamedExpr(new_separator_name)
                                                ]
                                            )
                                        ),
                                        PyAssignStmt(
                                            pattern=PyNamedPattern(first_element_name),
                                            expr=PyNamedExpr(second_element_name),
                                        ),
                                    ],
                                    handlers=[
                                        PyExceptHandler(
                                            expr=PyNamedExpr('StopIteration'),
                                            body=[
                                                *build_cond([
                                                    (
                                                        # FIXME does not handle nested tuples
                                                        build_isinstance(PyNamedExpr(first_element_name), PyNamedExpr('tuple')),
                                                        [
                                                            PyAssignStmt(
                                                                pattern=PyNamedPattern(value_name),
                                                                expr=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(0) ]),
                                                            ),
                                                            PyExprStmt(
                                                                expr=PyCallExpr(
                                                                    operator=PyNamedExpr('assert'),
                                                                    args=[ build_is_none(PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(1) ])) ]
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                    (
                                                        None,
                                                        [
                                                            PyAssignStmt(
                                                                pattern=PyNamedPattern(value_name),
                                                                expr=PyNamedExpr(first_element_name),
                                                            )
                                                        ]
                                                    )
                                                ]),
                                                *value_stmts,
                                                PyExprStmt(
                                                    expr=PyCallExpr(
                                                        operator=PyAttrExpr(PyNamedExpr(new_elements_name), 'append'),
                                                        args=[ PyNamedExpr(new_value_name) ]
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
                            expr=PyNamedExpr('StopIteration'),
                            body=[ PyPassStmt() ]
                        )
                    ]
                ),
                assign(PyNamedExpr(new_elements_name))
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

            if is_static(ty.element_type, specs=specs):
                yield ExternType(integer_rule_type), [
                    PyAssignStmt(PyNamedPattern(new_elements_name), expr=PyCallExpr(PyNamedExpr('list'))),
                    PyForStmt(PyNamedPattern('_'), PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyNamedExpr(in_name) ]), body= [
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(new_elements_name), 'append'), args=[ gen_default_constructor(ty.element_type, specs=specs, prefix=prefix) ])),
                    ]),
                    assign(PyNamedExpr(new_elements_name)),
                ]

            element_name = f'{in_name}_element'
            new_element_name = f'new_{in_name}_element'

            element_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)
            element_type, element_stmts = collect(ty.element_type, element_name, element_assign, True)

            yield ListType(element_type, ty.required), [
                PyAssignStmt(
                    pattern=PyNamedPattern(new_elements_name),
                    expr=PyCallExpr(operator=PyNamedExpr('list'))
                ),
                PyForStmt(
                    pattern=PyNamedPattern(element_name),
                    expr=PyNamedExpr(in_name),
                    body=[
                        *element_stmts,
                        PyExprStmt(
                            expr=PyCallExpr(
                                operator=PyAttrExpr(
                                    expr=PyNamedExpr(new_elements_name),
                                    name='append'
                                ),
                                args=[ PyNamedExpr(new_element_name) ]
                            )
                        )
                    ]
                ),
                assign(PyNamedExpr(new_elements_name))
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
                if not is_default_constructible(element_type, specs=specs, allow_empty_sequences=False):
                    required.append(element_type)

            if len(required) == 1:

                main_type = required[0]

                def first_assign(value: PyExpr):
                    assert(isinstance(ty, TupleType)) # Needed to keep Pyright happy
                    # Generates for example: self.field = (Dot(), $value, Dot())
                    return assign(
                        PyTupleExpr(
                            elements=list(value if el_ty == main_type else gen_default_constructor(el_ty, specs=specs, prefix=prefix) for el_ty in ty.element_types)
                        )
                    )

                yield from coercions(main_type, in_name, first_assign, True)

            new_elements: list[PyExpr] = []
            new_element_types: list[Type] = []

            # Generates for example: assert(isinstance(in_name, ty))
            orelse: list[PyStmt] = [
                PyExprStmt(
                    expr=PyCallExpr(
                        operator=PyNamedExpr('assert'),
                        args=[ gen_shallow_test(ty, PyNamedExpr(in_name), prefix) ]
                    )
                )
            ]

            for i, element_type in enumerate(ty.element_types):

                element_name = f'{in_name}_{i}'
                new_element_name = f'new_{in_name}_{i}'
                element_assign = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)

                new_elements.append(PyNamedExpr(new_element_name))

                orelse.append(
                    PyAssignStmt(
                        pattern=PyNamedPattern(element_name),
                        expr=PySubscriptExpr(
                            expr=PyNamedExpr(in_name),
                            slices=[ PyConstExpr(literal=i) ]
                        )
                    )
                )

                new_element_type, new_element_stmts = collect(element_type, element_name, element_assign, False)

                orelse.extend(new_element_stmts)

                new_element_types.append(new_element_type)

            orelse.append(assign(PyTupleExpr(elements=new_elements)))

            yield TupleType(new_element_types), orelse

            return

    return collect(field_type, in_name, assign, False)

